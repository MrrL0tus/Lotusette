"""Local LLM provider using HuggingFace Transformers.

Ce provider permet d'utiliser des modèles locaux directement via Transformers,
sans serveur intermédiaire. Idéal pour les petits modèles et le développement.

Exemples de modèles compatibles:
- microsoft/phi-2
- TinyLlama/TinyLlama-1.1B-Chat-v1.0
- mistralai/Mistral-7B-Instruct-v0.2
- openai/gpt-oss-20b (si disponible)
"""

import logging
from typing import AsyncIterator, List, Optional

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread

from .base import BaseLLM, LLMResponse, Message

logger = logging.getLogger(__name__)


class LocalTransformersProvider(BaseLLM):
    """Provider for local LLM using HuggingFace Transformers."""

    def __init__(
        self,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        device: Optional[str] = None,
        cache_dir: Optional[str] = None,
        load_in_8bit: bool = False,
        load_in_4bit: bool = False,
    ):
        """Initialize the local Transformers provider.

        Args:
            model: HuggingFace model identifier (e.g., 'microsoft/phi-2')
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            device: Device to use ('cuda', 'cpu', or None for auto)
            cache_dir: Directory to cache models
            load_in_8bit: Load model in 8-bit precision (requires bitsandbytes)
            load_in_4bit: Load model in 4-bit precision (requires bitsandbytes)
        """
        super().__init__(model, temperature, max_tokens)
        
        # Déterminer le device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        self.cache_dir = cache_dir
        self.load_in_8bit = load_in_8bit
        self.load_in_4bit = load_in_4bit
        
        logger.info(f"Initializing local Transformers provider with model: {model}")
        logger.info(f"Device: {self.device}")
        
        # Charger le tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model,
            cache_dir=cache_dir,
            trust_remote_code=True,
        )
        
        # S'assurer qu'un pad_token existe
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Configuration de chargement
        model_kwargs = {
            "cache_dir": cache_dir,
            "trust_remote_code": True,
        }
        
        if load_in_8bit:
            model_kwargs["load_in_8bit"] = True
        elif load_in_4bit:
            model_kwargs["load_in_4bit"] = True
        elif self.device == "cuda":
            model_kwargs["torch_dtype"] = torch.float16
        
        # Charger le modèle
        logger.info("Loading model... This may take a while.")
        self.model = AutoModelForCausalLM.from_pretrained(model, **model_kwargs)
        
        # Déplacer sur le device si pas de quantification
        if not (load_in_8bit or load_in_4bit):
            self.model = self.model.to(self.device)
        
        self.model.eval()
        logger.info("Model loaded successfully!")

    def _format_messages(self, messages: List[Message]) -> str:
        """Format messages into a prompt string.
        
        Cette méthode peut être surchargée pour des formats spécifiques à certains modèles.
        """
        formatted = ""
        for msg in messages:
            if msg.role == "system":
                formatted += f"System: {msg.content}\n\n"
            elif msg.role == "user":
                formatted += f"User: {msg.content}\n\n"
            elif msg.role == "assistant":
                formatted += f"Assistant: {msg.content}\n\n"
        
        # Ajouter le prompt pour la réponse de l'assistant
        formatted += "Assistant:"
        return formatted

    async def generate(self, messages: List[Message], stream: bool = False) -> LLMResponse:
        """Generate a response from the local model.

        Args:
            messages: List of conversation messages
            stream: Whether to stream the response (not used in non-stream mode)

        Returns:
            LLMResponse containing the generated text
        """
        if stream:
            # Pour le mode stream, utiliser generate_stream à la place
            full_response = ""
            async for chunk in self.generate_stream(messages):
                full_response += chunk
            
            return LLMResponse(
                content=full_response,
                model=self.model.config._name_or_path,
                finish_reason="stop",
            )
        
        # Format du prompt
        prompt = self._format_messages(messages)
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to(self.device)
        
        # Générer
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_tokens,
                temperature=self.temperature,
                do_sample=self.temperature > 0,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        # Décoder uniquement les nouveaux tokens
        generated_tokens = outputs[0][inputs.input_ids.shape[1]:]
        response_text = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
        
        return LLMResponse(
            content=response_text.strip(),
            model=self.model.config._name_or_path,
            tokens_used=len(outputs[0]),
            finish_reason="stop",
        )

    async def generate_stream(self, messages: List[Message]) -> AsyncIterator[str]:
        """Generate a streaming response from the local model.

        Args:
            messages: List of conversation messages

        Yields:
            Chunks of generated text
        """
        # Format du prompt
        prompt = self._format_messages(messages)
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to(self.device)
        
        # Créer un streamer
        streamer = TextIteratorStreamer(
            self.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
        )
        
        # Paramètres de génération
        generation_kwargs = {
            **inputs,
            "max_new_tokens": self.max_tokens,
            "temperature": self.temperature,
            "do_sample": self.temperature > 0,
            "pad_token_id": self.tokenizer.pad_token_id,
            "eos_token_id": self.tokenizer.eos_token_id,
            "streamer": streamer,
        }
        
        # Lancer la génération dans un thread séparé
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        
        # Yield les chunks au fur et à mesure
        for text in streamer:
            yield text
        
        thread.join()

    @property
    def provider_name(self) -> str:
        """Return the name of the LLM provider."""
        return "local-transformers"
