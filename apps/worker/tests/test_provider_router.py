import pytest

from src.providers.claude import ClaudeProvider
from src.providers.mock import MockLLMProvider
from src.providers.router import IngestionRouter, create_default_router


class FakeProvider:
    def __init__(
        self,
        name,
        *,
        healthy=True,
        fail=False,
        max_context_tokens=2_000_000,
        is_stub=False,
    ):
        self._name = name
        self.healthy = healthy
        self.fail = fail
        self._max_context_tokens = max_context_tokens
        self.is_stub = is_stub
        self.health_calls = 0
        self.extract_calls = 0

    @property
    def name(self):
        return self._name

    @property
    def max_context_tokens(self):
        return self._max_context_tokens

    @property
    def cost_per_million_tokens_input(self):
        return 0.0

    @property
    def cost_per_million_tokens_output(self):
        return 0.0

    async def health_check(self):
        self.health_calls += 1
        return self.healthy

    async def extract_structured_data(self, raw_content, extraction_schema):
        self.extract_calls += 1
        if self.fail:
            raise RuntimeError(f"{self.name} failed")
        return {"provider": self.name}


@pytest.mark.asyncio
async def test_healthy_gemini_is_used_first():
    gemini = FakeProvider("gemini")
    fallback = FakeProvider("fallback")
    router = IngestionRouter(primary=gemini, fallback=fallback)

    result = await router.extract(b"small payload", {"type": "v7"})

    assert result == {"provider": "gemini"}
    assert gemini.extract_calls == 1
    assert fallback.extract_calls == 0
    assert router.last_provider_used == "gemini"


@pytest.mark.asyncio
async def test_fallback_runs_only_when_it_is_a_real_provider():
    gemini = FakeProvider("gemini", fail=True)
    fallback = FakeProvider("real-fallback")
    router = IngestionRouter(primary=gemini, fallback=fallback)

    result = await router.extract(b"small payload", {"type": "v7"})

    assert result == {"provider": "real-fallback"}
    assert fallback.extract_calls == 1
    assert router.last_provider_used == "real-fallback"


@pytest.mark.asyncio
async def test_stub_fallback_is_not_called_in_production_path():
    gemini = FakeProvider("gemini", fail=True)
    stub = FakeProvider("claude-stub", is_stub=True)
    router = IngestionRouter(primary=gemini, fallback=stub)

    with pytest.raises(RuntimeError, match="No production fallback provider configured"):
        await router.extract(b"small payload", {"type": "v7"})

    assert stub.health_calls == 0
    assert stub.extract_calls == 0


@pytest.mark.asyncio
async def test_large_payload_does_not_try_smaller_fallback():
    gemini = FakeProvider("gemini", fail=True, max_context_tokens=2_000_000)
    fallback = FakeProvider("smaller-real-provider", max_context_tokens=1_000_000)
    router = IngestionRouter(primary=gemini, fallback=fallback)
    large_payload = b"x" * 4_000_004

    with pytest.raises(RuntimeError, match="Large payload requires gemini"):
        await router.extract(large_payload, {"type": "v7"})

    assert fallback.health_calls == 0
    assert fallback.extract_calls == 0


def test_claude_provider_is_explicitly_marked_non_productive_stub():
    assert ClaudeProvider().is_stub is True


def test_default_production_router_does_not_include_claude_stub(monkeypatch):
    monkeypatch.setenv("USE_MOCK", "0")
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "present-but-stubbed")

    router = create_default_router()

    assert router.primary.name.startswith("gemini")
    assert router.fallback is None


def test_default_router_uses_mock_provider_when_use_mock_enabled(monkeypatch):
    monkeypatch.setenv("USE_MOCK", "1")

    router = create_default_router()

    assert isinstance(router.primary, MockLLMProvider)
    assert router.fallback is None
