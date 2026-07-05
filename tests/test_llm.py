"""Tests for the LLM abstraction module."""

import pytest

from pipeline.llm import generate


class TestPlaceholderDetection:
    """Test that placeholder mode returns correct output type based on system_prompt."""

    def test_research_placeholder(self, monkeypatch: pytest.MonkeyPatch):
        """Research assistant system_prompt triggers research placeholder."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        result = generate(
            "Research this topic",
            system_prompt="You are a research assistant for educational videos.",
        )
        assert "topic" in result.lower()
        assert "hook_ideas" in result
        assert "key_facts" in result

    def test_script_placeholder(self, monkeypatch: pytest.MonkeyPatch):
        """Script writer system_prompt triggers script placeholder."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        result = generate(
            "Write a script",
            system_prompt="You are a YouTube script writer.",
        )
        assert "Scene" in result
        assert "VISUAL" in result

    def test_storyboard_placeholder(self, monkeypatch: pytest.MonkeyPatch):
        """Visual director system_prompt triggers storyboard placeholder."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        result = generate(
            "Create a storyboard",
            system_prompt="You are a visual director for educational YouTube animations.",
        )
        assert "Scene" in result
        assert "Duration" in result
        assert "Animation Sequence" in result

    def test_animation_plan_placeholder(self, monkeypatch: pytest.MonkeyPatch):
        """Animation engineer system_prompt triggers animation plan placeholder."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        result = generate(
            "Create animation plan",
            system_prompt="You are a Manim animation engineer.",
        )
        assert "scenes" in result
        assert "duration" in result
        assert "animations" in result

    def test_manim_code_placeholder(self, monkeypatch: pytest.MonkeyPatch):
        """Manim expert system_prompt triggers code placeholder."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        result = generate(
            "Generate manim code",
            system_prompt="You are a Manim expert.",
        )
        assert "from manim import" in result
        assert "class" in result
        assert "def construct" in result

    def test_unknown_prompt_returns_generic(self, monkeypatch: pytest.MonkeyPatch):
        """Unknown system_prompt returns a generic placeholder."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        result = generate("Hello world", system_prompt="You are a chef.")
        assert "[PLACEHOLDER]" in result

    def test_no_system_prompt_returns_generic(self, monkeypatch: pytest.MonkeyPatch):
        """No system_prompt returns a generic placeholder."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        result = generate("Hello world")
        assert "[PLACEHOLDER]" in result


class TestGenerateInterface:
    """Test the generate() function interface contract."""

    def test_returns_string(self, monkeypatch: pytest.MonkeyPatch):
        """generate() always returns a string."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        result = generate("test prompt")
        assert isinstance(result, str)

    def test_returns_nonempty(self, monkeypatch: pytest.MonkeyPatch):
        """generate() never returns an empty string in placeholder mode."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        result = generate("test prompt")
        assert len(result) > 0

    def test_accepts_all_parameters(self, monkeypatch: pytest.MonkeyPatch):
        """generate() accepts prompt, system_prompt, and model parameters."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        # Should not raise
        result = generate(
            "test",
            system_prompt="system",
            model="gpt-4",
        )
        assert isinstance(result, str)

    def test_placeholder_mode_without_api_key(self, monkeypatch: pytest.MonkeyPatch):
        """Without OPENAI_API_KEY, generate uses placeholder mode."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        result = generate("test prompt", system_prompt="You are a research assistant.")
        # Should return research placeholder, not raise an error
        assert "hook_ideas" in result

    def test_generic_placeholder_includes_prompt_length(self, monkeypatch: pytest.MonkeyPatch):
        """Generic placeholder includes the prompt character count."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        prompt = "x" * 42
        result = generate(prompt)
        assert "42" in result
