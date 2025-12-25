"""Anthropic Claude LLM provider implementation."""

import logging
from typing import AsyncIterator, List, Optional

from anthropic import AnthropicError, AsyncAnthropic

from .base import BaseLLM, LLMResponse, Message

logger = logging.getLogger(__name__)


class ClaudeProvider(BaseLLM):
    """Anthropic Claude provider implementation."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-opus-20240229",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """Initialize Claude provider.

        Args:
            api_key: Anthropic API key
            model: Model to use (e.g., claude-3-opus-20240229, claude-3-sonnet-20240229)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        """
        super().__init__(model=model, temperature=temperature, max_tokens=max_tokens)
        self.client = AsyncAnthropic(api_key=api_key)
        logger.info(f"Initialized Claude provider with model: {model}")

    async def generate(self, messages: List[Message], stream: bool = False) -> LLMResponse:
        """Generate a response using Claude API.

        Args:
            messages: List of conversation messages
            stream: Whether to stream (not used in non-streaming version)

        Returns:
            LLMResponse with generated text
        """
        try:
            # Claude requires system message to be separate
            system_message = None
            conversation_messages = []

            for msg in messages:
                if msg.role == "system":
                    system_message = msg.content
                else:
                    conversation_messages.append(msg.to_dict())

            logger.debug(f"Sending {len(conversation_messages)} messages to Claude")

            # Prepare kwargs
            kwargs = {
                "model": self.model,
                "messages": conversation_messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }

            if system_message:
                kwargs["system"] = system_message

            response = await self.client.messages.create(**kwargs)

            # Extract text content from response
            content = (
                response.content[0].text if response.content and len(response.content) > 0 else ""
            )
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            finish_reason = response.stop_reason

            logger.debug(f"Received response, tokens used: {tokens_used}")

            return LLMResponse(
                content=content,
                model=self.model,
                tokens_used=tokens_used,
                finish_reason=finish_reason,
            )

        except AnthropicError as e:
            logger.error(f"Claude API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in Claude provider: {e}")
            raise

    async def generate_stream(self, messages: List[Message]) -> AsyncIterator[str]:
        """Generate a streaming response using Claude API.

        Args:
            messages: List of conversation messages

        Yields:
            Chunks of generated text
        """
        try:
            # Claude requires system message to be separate
            system_message = None
            conversation_messages = []

            for msg in messages:
                if msg.role == "system":
                    system_message = msg.content
                else:
                    conversation_messages.append(msg.to_dict())

            logger.debug(
                f"Starting streaming generation with {len(conversation_messages)} messages"
            )

            # Prepare kwargs
            kwargs = {
                "model": self.model,
                "messages": conversation_messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stream": True,
            }

            if system_message:
                kwargs["system"] = system_message

            async with self.client.messages.stream(**kwargs) as stream:
                async for text in stream.text_stream:
                    yield text

        except AnthropicError as e:
            logger.error(f"Claude streaming error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in Claude streaming: {e}")
            raise

    @property
    def provider_name(self) -> str:
        """Return provider name."""
        return "claude"
