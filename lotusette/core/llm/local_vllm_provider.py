"""Local LLM provider using vLLM server.

Ce provider se connecte à un serveur vLLM local qui expose une API compatible OpenAI.
vLLM est optimisé pour l'inférence haute performance avec des modèles locaux.

Avantages de vLLM:
- Très performant (PagedAttention, continuous batching)
- API compatible OpenAI (facile à utiliser)
- Supporte de nombreux modèles (LLaMA, Mistral, etc.)
- Bon pour la production et les modèles moyens/grands

Installation de vLLM:
    pip install vllm

Démarrage d'un serveur vLLM:
    python -m vllm.entrypoints.openai.api_server \\
        --model mistralai/Mistral-7B-Instruct-v0.2 \\
        --host 0.0.0.0 \\
        --port 8001

Pour plus d'infos: https://docs.vllm.ai/
"""

import logging
from typing import AsyncIterator, List, Optional

import aiohttp

from .base import BaseLLM, LLMResponse, Message

logger = logging.getLogger(__name__)


class LocalVLLMProvider(BaseLLM):
    """Provider for local LLM using vLLM server with OpenAI-compatible API."""

    def __init__(
        self,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        base_url: str = "http://localhost:8001/v1",
        api_key: str = "EMPTY",
    ):
        """Initialize the local vLLM provider.

        Args:
            model: Model name (doit correspondre au modèle chargé dans vLLM)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            base_url: URL de base du serveur vLLM (défaut: http://localhost:8001/v1)
            api_key: API key (pas nécessaire pour vLLM local, mais requis par l'API)
        """
        super().__init__(model, temperature, max_tokens)
        
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        
        logger.info(f"Initializing vLLM provider with model: {model}")
        logger.info(f"Server URL: {base_url}")

    async def _make_request(
        self,
        messages: List[Message],
        stream: bool = False,
    ) -> dict:
        """Make a request to the vLLM server.

        Args:
            messages: List of conversation messages
            stream: Whether to stream the response

        Returns:
            Response dictionary from the server
        """
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        data = {
            "model": self.model,
            "messages": [msg.to_dict() for msg in messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": stream,
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                response.raise_for_status()
                return await response.json()

    async def generate(self, messages: List[Message], stream: bool = False) -> LLMResponse:
        """Generate a response from the vLLM server.

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
                model=self.model,
                finish_reason="stop",
            )
        
        try:
            response_data = await self._make_request(messages, stream=False)
            
            choice = response_data["choices"][0]
            content = choice["message"]["content"]
            finish_reason = choice.get("finish_reason", "stop")
            
            # Extraire les informations d'usage si disponibles
            tokens_used = None
            if "usage" in response_data:
                tokens_used = response_data["usage"].get("total_tokens")
            
            return LLMResponse(
                content=content,
                model=response_data.get("model", self.model),
                tokens_used=tokens_used,
                finish_reason=finish_reason,
            )
        
        except aiohttp.ClientError as e:
            logger.error(f"Error connecting to vLLM server: {e}")
            raise RuntimeError(
                f"Failed to connect to vLLM server at {self.base_url}. "
                f"Make sure the vLLM server is running. Error: {e}"
            )
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    async def generate_stream(self, messages: List[Message]) -> AsyncIterator[str]:
        """Generate a streaming response from the vLLM server.

        Args:
            messages: List of conversation messages

        Yields:
            Chunks of generated text
        """
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        data = {
            "model": self.model,
            "messages": [msg.to_dict() for msg in messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True,
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as response:
                    response.raise_for_status()
                    
                    # Lire le stream ligne par ligne
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        
                        # Ignorer les lignes vides
                        if not line:
                            continue
                        
                        # Les lignes commencent par "data: "
                        if line.startswith("data: "):
                            data_str = line[6:]  # Enlever "data: "
                            
                            # Vérifier si c'est la fin du stream
                            if data_str == "[DONE]":
                                break
                            
                            try:
                                import json
                                chunk_data = json.loads(data_str)
                                
                                # Extraire le contenu du delta
                                if "choices" in chunk_data and len(chunk_data["choices"]) > 0:
                                    delta = chunk_data["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    
                                    if content:
                                        yield content
                            
                            except json.JSONDecodeError:
                                logger.warning(f"Failed to parse JSON: {data_str}")
                                continue
        
        except aiohttp.ClientError as e:
            logger.error(f"Error connecting to vLLM server: {e}")
            raise RuntimeError(
                f"Failed to connect to vLLM server at {self.base_url}. "
                f"Make sure the vLLM server is running. Error: {e}"
            )
        except Exception as e:
            logger.error(f"Error generating streaming response: {e}")
            raise

    @property
    def provider_name(self) -> str:
        """Return the name of the LLM provider."""
        return "local-vllm"
