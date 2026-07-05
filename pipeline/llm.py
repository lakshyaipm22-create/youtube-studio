"""
YouTube Studio - LLM Abstraction

Simple interface for text generation using OpenAI-compatible APIs.
Falls back to structured placeholder output when no API key is available,
allowing the pipeline to run end-to-end for testing.

Environment variables:
    OPENAI_API_KEY    - API key for the provider
    OPENAI_BASE_URL   - Base URL for compatible providers (optional)
    OPENAI_MODEL      - Default model name (optional, defaults to gpt-4o-mini)
"""

import os


def generate(
    prompt: str,
    system_prompt: str | None = None,
    model: str | None = None,
) -> str:
    """Generate text using an OpenAI-compatible LLM.

    Args:
        prompt: The user prompt to send.
        system_prompt: Optional system prompt for context/instructions.
        model: Model name override. Defaults to OPENAI_MODEL env var or gpt-4o-mini.

    Returns:
        Generated text response as a string.

    If OPENAI_API_KEY is not set, returns placeholder output so the pipeline
    can run end-to-end without an API key.
    """
    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        return _placeholder_response(prompt, system_prompt)

    return _call_api(prompt, system_prompt, model, api_key)


def _call_api(
    prompt: str,
    system_prompt: str | None,
    model: str | None,
    api_key: str,
) -> str:
    """Call the OpenAI-compatible API."""
    try:
        from openai import OpenAI
    except ImportError as err:
        raise RuntimeError(
            "openai package not installed. Install with: pip install 'youtube-studio[ai]'"
        ) from err

    base_url = os.environ.get("OPENAI_BASE_URL")
    resolved_model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    client = OpenAI(api_key=api_key, base_url=base_url)

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=resolved_model,
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content or ""


def _placeholder_response(prompt: str, system_prompt: str | None = None) -> str:
    """Generate structured placeholder output for testing without an API key.

    Detects the type of request from the prompt content and returns
    appropriate placeholder data.
    """
    prompt_lower = prompt.lower()

    if "research" in prompt_lower and ("yaml" in prompt_lower or "facts" in prompt_lower):
        return _placeholder_research()
    elif "script" in prompt_lower and "narration" in prompt_lower:
        return _placeholder_script()
    elif "storyboard" in prompt_lower or "scene plan" in prompt_lower:
        return _placeholder_storyboard()
    elif "animation" in prompt_lower and "plan" in prompt_lower:
        return _placeholder_animation_plan()
    elif "manim" in prompt_lower or "scenes.py" in prompt_lower:
        return _placeholder_manim_code()
    else:
        return f"[PLACEHOLDER] Generated response for prompt ({len(prompt)} chars)"


def _placeholder_research() -> str:
    return """topic: Placeholder Topic
hook_ideas:
  - Did you know this surprising fact?
  - What if everything you believed about this was wrong?
key_facts:
  - First important fact about the topic
  - Second important fact with supporting detail
  - Third fact that connects to viewer experience
misconceptions:
  - Common misconception that most people believe
  - Another widespread misunderstanding
analogies:
  - Simple analogy comparing concept to everyday experience
  - Another analogy using familiar objects
sources:
  - Research paper or textbook reference
  - Expert explanation or documentary
"""


def _placeholder_script() -> str:
    return """# Scene 1: Hook
[VISUAL: Eye-catching animation that grabs attention]
Have you ever wondered why this works the way it does?

# Scene 2: Introduction
[VISUAL: Title card with topic name]
Today we are going to explore this concept step by step.

# Scene 3: Core Concept
[VISUAL: Animated diagram showing the main idea]
Here is the key insight. Think of it like this simple analogy.

The main principle works because of these three factors.

# Scene 4: Example
[VISUAL: Concrete example with animations]
Let us see this in action with a real example.

Watch how this transforms when we apply what we learned.

# Scene 5: Recap
[VISUAL: Summary with key points highlighted]
Remember these three things: first, second, and third.

# Scene 6: Outro
[VISUAL: Subscribe button animation]
If this helped you understand, hit subscribe for more.
"""


def _placeholder_storyboard() -> str:
    return """## Scene 1: Hook
Duration: 10s

Visual Goal: Grab attention with a surprising visual

Animation Sequence:
1. [0.0s] Question text fades in at center
2. [2.0s] Supporting visual draws in below
3. [5.0s] Elements transform to reveal the answer hint
4. [8.0s] Transition fade to next scene

Manim Objects: Text, SVGMobject, VGroup
Transition: Fade out all

## Scene 2: Core Concept
Duration: 45s

Visual Goal: Explain the main idea with clear visuals

Animation Sequence:
1. [0.0s] Title text appears
2. [3.0s] Diagram builds piece by piece
3. [15.0s] Labels and arrows highlight connections
4. [30.0s] Animation shows the process in action
5. [40.0s] Key takeaway text appears below

Manim Objects: Text, Arrow, Circle, Rectangle, VGroup
Transition: Slide left

## Scene 3: Example
Duration: 30s

Visual Goal: Concrete example reinforcing the concept

Animation Sequence:
1. [0.0s] Example setup appears
2. [5.0s] Step-by-step walkthrough with highlights
3. [20.0s] Result revealed with emphasis
4. [25.0s] Comparison to concept diagram

Manim Objects: Text, NumberLine, Dot, Arrow
Transition: Fade out

## Scene 4: Outro
Duration: 10s

Visual Goal: Clean ending with call to action

Animation Sequence:
1. [0.0s] Summary points fly in
2. [5.0s] Subscribe CTA animates
3. [8.0s] Channel logo fades in

Manim Objects: Text, SVGMobject
Transition: Fade to black
"""


def _placeholder_animation_plan() -> str:
    return """scenes:
  - name: Hook
    duration: 10
    objects:
      - type: Text
        content: "Did you know?"
        position: center
        font_size: 48
      - type: SVGMobject
        file: assets/svg/question.svg
        position: below_center
        scale: 0.5
    animations:
      - action: FadeIn
        target: text_0
        time: 0.0
      - action: DrawBorderThenFill
        target: svg_0
        time: 2.0
      - action: FadeOut
        target: all
        time: 8.0

  - name: CoreConcept
    duration: 45
    objects:
      - type: Text
        content: "The Main Idea"
        position: top
        font_size: 36
      - type: Circle
        radius: 1.5
        position: center
        color: "#6C63FF"
      - type: Arrow
        start: left
        end: right
    animations:
      - action: Write
        target: text_0
        time: 0.0
      - action: Create
        target: circle_0
        time: 3.0
      - action: GrowArrow
        target: arrow_0
        time: 15.0

  - name: Example
    duration: 30
    objects:
      - type: Text
        content: "Real Example"
        position: top
        font_size: 36
      - type: NumberLine
        range: [0, 10]
        position: center
    animations:
      - action: Write
        target: text_0
        time: 0.0
      - action: Create
        target: numberline_0
        time: 5.0

  - name: Outro
    duration: 10
    objects:
      - type: Text
        content: "Subscribe for more!"
        position: center
        font_size: 42
    animations:
      - action: FadeIn
        target: text_0
        time: 0.0
      - action: FadeOut
        target: all
        time: 8.0
"""


def _placeholder_manim_code() -> str:
    return '''"""Auto-generated Manim scenes."""

from manim import *  # noqa: F403


class Hook(Scene):
    """Opening hook scene."""

    def construct(self):
        title = Text("Did you know?", font_size=48)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))


class CoreConcept(Scene):
    """Main concept explanation."""

    def construct(self):
        title = Text("The Main Idea", font_size=36)
        title.to_edge(UP)
        circle = Circle(radius=1.5, color="#6C63FF")

        self.play(Write(title))
        self.play(Create(circle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(circle))


class Example(Scene):
    """Concrete example."""

    def construct(self):
        title = Text("Real Example", font_size=36)
        title.to_edge(UP)
        line = NumberLine(x_range=[0, 10, 1])

        self.play(Write(title))
        self.play(Create(line))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(line))


class Outro(Scene):
    """Closing scene."""

    def construct(self):
        text = Text("Subscribe for more!", font_size=42)
        self.play(FadeIn(text))
        self.wait(2)
        self.play(FadeOut(text))
'''
