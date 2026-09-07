"""Local LLM provider talking to an OpenAI-compatible HTTP server.

Ce provider ne dépend d'aucune spécificité vLLM : il parle le contrat
`/v1/chat/completions` d'OpenAI, que servent aussi bien `llama-server`
(llama.cpp) qu'Ollama ou vLLM. Le corps de requête n'utilise que des champs
standards (`model`, `messages`, `temperature`, `max_tokens`, `stream`).

Serveur recommandé, llama.cpp — pas de GPU CUDA obligatoire, fonctionne sur
CPU seul :

    llama-server -hf mistralai/Ministral-3-14B-Instruct-2512-GGUF:Q4_K_M \\
        -c 16384 --port 8080 --host 127.0.0.1

Voir docs/MODELS.md pour le choix du modèle selon la machine.
"""

import json
import logging
from collections.abc import AsyncIterator

import aiohttp

from .base import BaseLLM, LLMResponse, Message

logger = logging.getLogger(__name__)

# Un modèle local peut mettre plusieurs minutes à rendre une réponse longue.
# On ne borne donc pas la durée totale, seulement l'inactivité du socket :
# un serveur qui ne répond plus doit lever une erreur, pas figer le CLI.
DEFAULT_SOCK_READ_TIMEOUT = 120.0
DEFAULT_CONNECT_TIMEOUT = 10.0


class LocalOpenAIProvider(BaseLLM):
    """Provider for a local LLM server exposing an OpenAI-compatible API."""

    def __init__(
        self,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        base_url: str = "http://localhost:8080/v1",
        api_key: str = "EMPTY",
        sock_read_timeout: float = DEFAULT_SOCK_READ_TIMEOUT,
    ):
        """Initialize the local provider.

        Args:
            model: Nom du modèle annoncé au serveur. llama.cpp l'ignore et sert
                le modèle chargé au démarrage ; Ollama et vLLM s'en servent.
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            base_url: URL de base du serveur, terminée par /v1
            api_key: Jeton d'authentification. llama.cpp et Ollama l'ignorent,
                mais l'en-tête doit être présent pour les serveurs qui le
                vérifient.
            sock_read_timeout: Délai maximal sans octet reçu, en secondes.
        """
        super().__init__(model, temperature, max_tokens)

        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = aiohttp.ClientTimeout(
            total=None,
            connect=DEFAULT_CONNECT_TIMEOUT,
            sock_read=sock_read_timeout,
        )

        logger.debug(f"Initializing local LLM provider with model: {model}")
        logger.debug(f"Server URL: {self.base_url}")

    @property
    def _headers(self) -> dict:
        """HTTP headers sent with every request."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _payload(self, messages: list[Message], stream: bool) -> dict:
        """Build the request body.

        Ne contient que des champs de l'API OpenAI, afin de rester compatible
        avec llama.cpp, Ollama et vLLM sans branchement par serveur.
        """
        return {
            "model": self.model,
            "messages": [msg.to_dict() for msg in messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": stream,
        }

    def _connection_error(self, error: Exception) -> RuntimeError:
        """Build a helpful error when the server cannot be reached."""
        return RuntimeError(
            f"Impossible de joindre le serveur LLM local sur {self.base_url}. "
            f"Vérifiez qu'il tourne, par exemple avec :\n"
            f"    llama-server -hf <modèle> -c 8192 --port 8080\n"
            f"Erreur : {error}"
        )

    async def generate(self, messages: list[Message], stream: bool = False) -> LLMResponse:
        """Generate a response from the local server.

        Args:
            messages: List of conversation messages
            stream: Si vrai, consomme le flux et renvoie la réponse complète.

        Returns:
            LLMResponse containing the generated text
        """
        if stream:
            # Pour un affichage au fil de l'eau, utiliser generate_stream.
            full_response = ""
            async for chunk in self.generate_stream(messages):
                full_response += chunk

            return LLMResponse(
                content=full_response,
                model=self.model,
                finish_reason="stop",
            )

        url = f"{self.base_url}/chat/completions"

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    url, json=self._payload(messages, stream=False), headers=self._headers
                ) as response:
                    response.raise_for_status()
                    response_data = await response.json()

            choice = response_data["choices"][0]
            content = choice["message"]["content"]
            finish_reason = choice.get("finish_reason", "stop")

            tokens_used: int | None = None
            if "usage" in response_data:
                tokens_used = response_data["usage"].get("total_tokens")

            return LLMResponse(
                content=content,
                model=response_data.get("model", self.model),
                tokens_used=tokens_used,
                finish_reason=finish_reason,
            )

        except aiohttp.ClientError as e:
            logger.debug(f"Error connecting to local LLM server: {e}")
            raise self._connection_error(e) from e
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

    async def generate_stream(self, messages: list[Message]) -> AsyncIterator[str]:
        """Generate a streaming response from the local server.

        Args:
            messages: List of conversation messages

        Yields:
            Chunks of generated text
        """
        url = f"{self.base_url}/chat/completions"

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(
                    url, json=self._payload(messages, stream=True), headers=self._headers
                ) as response:
                    response.raise_for_status()

                    async for raw_line in response.content:
                        line = raw_line.decode("utf-8").strip()

                        if not line or not line.startswith("data: "):
                            continue

                        data_str = line[len("data: ") :]

                        if data_str == "[DONE]":
                            break

                        try:
                            chunk_data = json.loads(data_str)
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse JSON: {data_str}")
                            continue

                        choices = chunk_data.get("choices") or []
                        if not choices:
                            continue

                        content = choices[0].get("delta", {}).get("content", "")
                        if content:
                            yield content

        except aiohttp.ClientError as e:
            logger.debug(f"Error connecting to local LLM server: {e}")
            raise self._connection_error(e) from e
        except Exception as e:
            logger.error(f"Error generating streaming response: {e}")
            raise

    @property
    def provider_name(self) -> str:
        """Return the name of the LLM provider."""
        return "local"


# Ancien nom, conservé pour ne pas casser les imports existants.
LocalVLLMProvider = LocalOpenAIProvider
