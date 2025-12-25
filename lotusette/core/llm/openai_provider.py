"""OpenAI LLM provider implementation."""

import logging
from typing import AsyncIterator, List, Optional

from openai import AsyncOpenAI, OpenAIError

from .base import BaseLLM, LLMResponse, Message

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLM):
    """OpenAI GPT provider implementation."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: Model to use (e.g., gpt-4-turbo-preview, gpt-3.5-turbo)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        """
        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)
        self.client = AsyncOpenAI(api_key=api_key)
        logger.info(f"Initialized OpenAI provider with model: {model}")

    async def generate(self, messages: List[Message], stream: bool = False) -> LLMResponse:
        """Generate a response using OpenAI API.

        Args:
            messages: List of conversation messages
            stream: Whether to stream (not used in non-streaming version)

        Returns:
            LLMResponse with generated text
        """
        try:
            # Convert messages to OpenAI format
            openai_messages = [msg.to_dict() for msg in messages]

            logger.debug(f"Sending {len(messages)} messages to OpenAI")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else None
            finish_reason = response.choices[0].finish_reason

            logger.debug(f"Received response, tokens used: {tokens_used}")

            return LLMResponse(
                content=content,
                model=self.model,
                tokens_used=tokens_used,
                finish_reason=finish_reason,
            )

        except OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI provider: {e}")
            raise

    async def generate_stream(self, messages: List[Message]) -> AsyncIterator[str]:
        """Generate a streaming response using OpenAI API.

        Args:
            messages: List of conversation messages

        Yields:
            Chunks of generated text
        """
        try:
            openai_messages = [msg.to_dict() for msg in messages]

            logger.debug(f"Starting streaming generation with {len(messages)} messages")

            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        except OpenAIError as e:
            logger.error(f"OpenAI streaming error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI streaming: {e}")
            raise

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "openai"
