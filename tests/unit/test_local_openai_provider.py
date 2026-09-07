"""Unit tests for the local LLM provider (OpenAI-compatible server)."""

import json

import pytest

from lotusette.core.llm import LLMFactory, Message
from lotusette.core.llm.local_openai_provider import LocalOpenAIProvider, LocalVLLMProvider


class TestLocalProviderFactory:
    """Tests for creating the local provider through the factory."""

    def test_create_local_provider(self):
        """The 'local' provider name builds a LocalOpenAIProvider."""
        provider = LLMFactory.create_provider(
            provider_name="local",
            model="mistralai/Ministral-3-14B-Instruct-2512-GGUF:Q4_K_M",
            base_url="http://localhost:8080/v1",
        )
        assert isinstance(provider, LocalOpenAIProvider)
        assert provider.model == "mistralai/Ministral-3-14B-Instruct-2512-GGUF:Q4_K_M"
        assert provider.provider_name == "local"

    @pytest.mark.parametrize("alias", ["local-vllm", "llamacpp", "ollama", "LOCAL"])
    def test_provider_aliases(self, alias):
        """Legacy and server-specific names resolve to the same provider."""
        provider = LLMFactory.create_provider(provider_name=alias, model="test-model")
        assert isinstance(provider, LocalOpenAIProvider)
        assert provider.provider_name == "local"

    def test_legacy_class_name_is_an_alias(self):
        """LocalVLLMProvider is kept as an alias of the renamed class."""
        assert LocalVLLMProvider is LocalOpenAIProvider

    def test_configuration_is_forwarded(self):
        """Factory arguments reach the provider instance."""
        provider = LLMFactory.create_provider(
            provider_name="local",
            model="test-model",
            temperature=0.5,
            max_tokens=500,
            base_url="http://test:8000/v1",
        )
        assert provider.temperature == 0.5
        assert provider.max_tokens == 500
        assert provider.base_url == "http://test:8000/v1"

    def test_trailing_slash_is_stripped(self):
        """A base_url with a trailing slash must not produce a double slash."""
        provider = LocalOpenAIProvider(model="m", base_url="http://localhost:8080/v1/")
        assert provider.base_url == "http://localhost:8080/v1"

    def test_local_provider_requires_model(self):
        """The local provider has no sensible default model."""
        with pytest.raises(ValueError, match="Model name is required"):
            LLMFactory.create_provider(provider_name="local")

    def test_unsupported_provider(self):
        """An unknown provider name is rejected with the list of valid ones."""
        with pytest.raises(ValueError, match="Unsupported LLM provider"):
            LLMFactory.create_provider(provider_name="local-transformers", model="m")

    def test_factory_supports_all_providers(self):
        """Each supported provider can be instantiated."""
        assert LLMFactory.create_provider("openai", api_key="test").provider_name == "openai"
        assert LLMFactory.create_provider("claude", api_key="test").provider_name == "claude"
        assert LLMFactory.create_provider("local", model="test-model").provider_name == "local"


class TestRequestPayload:
    """The request body must stay compatible with llama.cpp and Ollama."""

    def test_payload_only_uses_standard_openai_fields(self):
        """No vLLM-specific parameter may leak into the request body."""
        provider = LocalOpenAIProvider(model="m", temperature=0.3, max_tokens=42)
        payload = provider._payload([Message(role="user", content="salut")], stream=False)

        assert set(payload) == {"model", "messages", "temperature", "max_tokens", "stream"}
        assert payload["model"] == "m"
        assert payload["temperature"] == 0.3
        assert payload["max_tokens"] == 42
        assert payload["stream"] is False
        assert payload["messages"] == [{"role": "user", "content": "salut"}]

    def test_payload_stream_flag(self):
        """The stream flag is passed through to the server."""
        provider = LocalOpenAIProvider(model="m")
        assert provider._payload([], stream=True)["stream"] is True

    def test_authorization_header_is_always_present(self):
        """llama.cpp ignores the header, but it must be well-formed."""
        provider = LocalOpenAIProvider(model="m", api_key="EMPTY")
        assert provider._headers["Authorization"] == "Bearer EMPTY"
        assert provider._headers["Content-Type"] == "application/json"


class _FakeContent:
    """Minimal stand-in for aiohttp's streaming response content."""

    def __init__(self, lines):
        self._lines = lines

    def __aiter__(self):
        async def _gen():
            for line in self._lines:
                yield line

        return _gen()


class _FakeResponse:
    def __init__(self, *, json_body=None, lines=None):
        self._json_body = json_body
        self.content = _FakeContent(lines or [])

    def raise_for_status(self):
        return None

    async def json(self):
        return self._json_body

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False


class _FakeSession:
    def __init__(self, response):
        self._response = response
        self.calls = []

    def post(self, url, json=None, headers=None):
        self.calls.append({"url": url, "json": json, "headers": headers})
        return self._response

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False


@pytest.fixture
def patch_session(monkeypatch):
    """Replace aiohttp.ClientSession with a scripted fake."""

    def _patch(response):
        session = _FakeSession(response)
        monkeypatch.setattr(
            "lotusette.core.llm.local_openai_provider.aiohttp.ClientSession",
            lambda *args, **kwargs: session,
        )
        return session

    return _patch


class TestGenerate:
    """Non-streaming generation."""

    @pytest.mark.asyncio
    async def test_generate_parses_response(self, patch_session):
        """A standard OpenAI response body is mapped onto LLMResponse."""
        session = patch_session(
            _FakeResponse(
                json_body={
                    "model": "served-model",
                    "choices": [
                        {"message": {"content": "Bonjour !"}, "finish_reason": "stop"},
                    ],
                    "usage": {"total_tokens": 17},
                }
            )
        )
        provider = LocalOpenAIProvider(model="m", base_url="http://localhost:8080/v1")

        response = await provider.generate([Message(role="user", content="salut")])

        assert response.content == "Bonjour !"
        assert response.model == "served-model"
        assert response.tokens_used == 17
        assert response.finish_reason == "stop"
        assert session.calls[0]["url"] == "http://localhost:8080/v1/chat/completions"

    @pytest.mark.asyncio
    async def test_generate_without_usage_block(self, patch_session):
        """llama.cpp may omit the usage block; that is not an error."""
        patch_session(_FakeResponse(json_body={"choices": [{"message": {"content": "ok"}}]}))
        provider = LocalOpenAIProvider(model="m")

        response = await provider.generate([Message(role="user", content="salut")])

        assert response.content == "ok"
        assert response.tokens_used is None
        assert response.finish_reason == "stop"


def _sse(*payloads):
    """Encode payloads as server-sent event lines."""
    lines = [f"data: {json.dumps(p)}".encode() for p in payloads]
    lines.append(b"data: [DONE]")
    return lines


class TestGenerateStream:
    """Streaming generation."""

    @pytest.mark.asyncio
    async def test_stream_yields_content_deltas(self, patch_session):
        """Each delta with content is yielded in order."""
        patch_session(
            _FakeResponse(
                lines=_sse(
                    {"choices": [{"delta": {"role": "assistant"}}]},
                    {"choices": [{"delta": {"content": "Bon"}}]},
                    {"choices": [{"delta": {"content": "jour"}}]},
                    {"choices": [{"delta": {}, "finish_reason": "stop"}]},
                )
            )
        )
        provider = LocalOpenAIProvider(model="m")

        chunks = [c async for c in provider.generate_stream([Message(role="user", content="x")])]

        assert chunks == ["Bon", "jour"]

    @pytest.mark.asyncio
    async def test_stream_skips_blank_and_malformed_lines(self, patch_session):
        """Keep-alive blanks and unparseable payloads must not break the stream."""
        patch_session(
            _FakeResponse(
                lines=[
                    b"",
                    b": ping",
                    b"data: {not json}",
                    b'data: {"choices": [{"delta": {"content": "ok"}}]}',
                    b"data: [DONE]",
                    b'data: {"choices": [{"delta": {"content": "apres-done"}}]}',
                ]
            )
        )
        provider = LocalOpenAIProvider(model="m")

        chunks = [c async for c in provider.generate_stream([Message(role="user", content="x")])]

        assert chunks == ["ok"]

    @pytest.mark.asyncio
    async def test_stream_handles_empty_choices(self, patch_session):
        """Some servers emit a final chunk with an empty choices list."""
        patch_session(
            _FakeResponse(
                lines=_sse(
                    {"choices": []},
                    {"choices": [{"delta": {"content": "a"}}]},
                )
            )
        )
        provider = LocalOpenAIProvider(model="m")

        chunks = [c async for c in provider.generate_stream([Message(role="user", content="x")])]

        assert chunks == ["a"]

    @pytest.mark.asyncio
    async def test_generate_with_stream_true_collects_full_text(self, patch_session):
        """generate(stream=True) consumes the stream and returns the whole reply."""
        patch_session(
            _FakeResponse(
                lines=_sse(
                    {"choices": [{"delta": {"content": "Bon"}}]},
                    {"choices": [{"delta": {"content": "jour"}}]},
                )
            )
        )
        provider = LocalOpenAIProvider(model="m")

        response = await provider.generate([Message(role="user", content="x")], stream=True)

        assert response.content == "Bonjour"
