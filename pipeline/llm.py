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

    Uses the system_prompt (unique per stage) as the primary signal for detection,
    falling back to prompt content analysis.
    """
    sys_lower = (system_prompt or "").lower()

    # Use system prompt as primary signal (each stage has a unique one)
    if "research assistant" in sys_lower:
        return _placeholder_research()
    elif "script writer" in sys_lower:
        return _placeholder_script()
    elif "visual director" in sys_lower:
        return _placeholder_storyboard()
    elif "animation engineer" in sys_lower:
        return _placeholder_animation_plan()
    elif "manim expert" in sys_lower:
        return _placeholder_manim_code()
    else:
        return f"[PLACEHOLDER] Generated response for prompt ({len(prompt)} chars)"


def _placeholder_research() -> str:
    return """topic: "Why Airplanes Don't Fall"

hook_ideas:
  - "A Boeing 747 weighs 400 tons. That's 80 elephants. And somehow... it flies."
  - "Everything your teacher told you about how planes fly? Mostly wrong."
  - "Right now, 10,000 planes are in the air. Not one of them should be."

surprising_facts:
  - A plane wing generates over 300,000 pounds of lift at cruising speed
  - Planes can fly perfectly well upside down, which disproves the simple Bernoulli explanation
  - The Wright brothers tested over 200 wing shapes before finding one that worked
  - Air hitting a wing is deflected downward at roughly 10 degrees
  - A paper airplane uses the exact same physics as a 747

misconceptions:
  - "Air travels faster over the curved top because the path is longer
    (equal transit time theory) - debunked by NASA"
  - "Bernoulli's principle alone explains all lift - it actually
    requires Newton's third law too"
  - "Heavier planes need bigger wings - actually they just need
    more speed or angle"

analogies:
  - "Stick your hand out a car window and tilt it up - that push you feel IS lift"
  - "A wing is like a water ski - it deflects fluid downward and rides the reaction force up"
  - "Think of air as thick honey and the wing as a spoon pressing through it"

key_facts:
  - Wings work by deflecting air downward (Newton's third law - equal and opposite reaction)
  - The curved shape creates lower pressure above the wing (Bernoulli's principle)
  - Angle of attack is the most important variable for lift generation
  - Both Newton and Bernoulli contribute to lift - the real answer is both together
  - Stall happens when the angle of attack gets too steep and airflow separates
  - Flaps and slats change the wing shape for different flight phases

thumbnail_idea: "A massive 747 balanced on a tiny finger with arrows
  showing invisible forces - text says 400 TONS?!"

sources:
  - "NASA Glenn Research Center - Beginner's Guide to Aeronautics"
  - "Feynman Lectures on Physics Vol. II - Chapter on fluid dynamics"
  - "Cambridge University Engineering Department - How Do Wings Work?"
"""


def _placeholder_script() -> str:
    return """# Scene 1: Hook

[VISUAL: A massive Boeing 747 appears, with "400 TONS" text scaling up dramatically]

A Boeing 747 weighs 400 tons. That is 80 elephants stacked together.

[VISUAL: 80 tiny elephant icons fill the screen, then morph into a plane silhouette]

And right now, there are 10,000 of these in the sky. Not falling.

How?

# Scene 2: The Wrong Answer

[VISUAL: A classic wing cross-section diagram draws in, with airflow arrows]

You probably learned this in school. Air goes over the curved top,
travels a longer path, moves faster, creates low pressure. Plane goes up.

[VISUAL: The "longer path" explanation appears, then a red X stamps over it]

Sounds clean. Sounds elegant. And it is mostly wrong.

If that were true, planes could never fly upside down. But they can.

# Scene 3: The Hand Out the Window

[VISUAL: A car driving, with a hand sticking out the window at an angle]

Here is the real explanation, and it starts with something you have done a hundred times.

Stick your hand out a car window. Tilt it up slightly. Feel that push?

[VISUAL: The hand tilts, arrows show air being deflected downward, hand pushes up]

You just created lift. That is literally how a wing works.

# Scene 4: Newton Gets Involved

[VISUAL: Newton's third law equation appears, then transforms into wing + air arrows]

When a wing hits air, it shoves the air downward.
Newton's third law says: if you push air down, the air pushes you up.

That push is lift. Simple as that.

[VISUAL: Split screen showing deflected air going DOWN and wing being pushed UP]

But wait. There is more going on.

# Scene 5: Bernoulli Joins the Party

[VISUAL: Wing shape with pressure gradient visualization - blue low pressure above, red below]

The curved shape of the wing does matter. It creates a pressure difference.

Lower pressure above, higher pressure below. This is Bernoulli's contribution.

[VISUAL: Merge Newton arrows and Bernoulli pressure into one unified diagram]

The real answer? It is both. Newton and Bernoulli working together.

# Scene 6: The Secret Variable

[VISUAL: Wing rotating to different angles, with lift arrow changing size]

But here is what actually controls whether a plane flies or falls: the angle of attack.

Tilt the wing up more? More lift. Tilt too much? The air cannot follow the surface anymore.

[VISUAL: Smooth airflow becomes turbulent, lift arrow collapses - "STALL" text appears]

That is a stall. And that is what pilots actually worry about.

# Scene 7: Outro

[VISUAL: Recap diagram showing wing with both Newton and Bernoulli forces labeled]

So next time you see a plane overhead, remember:
it is not magic. It is just pushing air down really, really hard.

[VISUAL: Subscribe button animates in with channel logo]

If this made flight click for you, subscribe. Next time: why boats do not sink.
"""


def _placeholder_storyboard() -> str:
    return """## Scene 1: Hook
Duration: 12s

Visual Goal: Create awe at the impossibility of flight, trigger curiosity

Animation Sequence:

| Time | Element | Animation | Notes |
|------|---------|-----------|-------|
| 0.0s | Boeing 747 silhouette | Entrance: FadeIn from bottom | Large, imposing |
| 1.5s | "400 TONS" text | Entrance: scale up from zero | BRAND_SECONDARY color |
| 3.0s | 80 elephant icons | Entrance: stagger FadeIn across grid | 0.2s delay each |
| 6.0s | Elephants | Transform: morph into plane shape | Satisfying visual payoff |
| 8.0s | "10,000 in the sky right now" | Entrance: Write | Below the plane |
| 10.0s | "How?" text | Entrance: FadeIn, scale 1.5x | Center, dramatic |
| 11.0s | All elements | Exit: FadeOut | Clean transition |

SVGs Needed: boeing-747-silhouette.svg, elephant-icon.svg
Camera: Static, zoom in slightly on "How?"
Transition to Next: Fade to dark, brief pause

## Scene 2: The Wrong Answer
Duration: 18s

Visual Goal: Show the common explanation, then debunk it

| Time | Element | Animation | Notes |
|------|---------|-----------|-------|
| 0.0s | Wing cross-section | Entrance: Create (draw) | Classic textbook style |
| 2.0s | Airflow arrows (top) | Entrance: GrowArrow, stagger | Show curved path |
| 4.0s | Airflow arrows (bottom) | Entrance: GrowArrow | Show straight path |
| 6.0s | "Longer path = faster" label | Entrance: Write | Textbook explanation |
| 9.0s | Red X stamp | Entrance: FadeIn + scale bounce | Over the whole diagram |
| 11.0s | Upside-down plane | Entrance: FadeIn from right | Proves the point |
| 14.0s | Question mark | Entrance: GrowFromCenter | If Bernoulli alone, this is impossible |
| 16.0s | All elements | Exit: FadeOut | Prepare for correct answer |

SVGs Needed: wing-crosssection.svg, red-x-stamp.svg
Camera: Static
Transition to Next: Slide left

## Scene 3: The Hand Out the Window
Duration: 20s

Visual Goal: Make the correct explanation feel intuitive via everyday experience

| Time | Element | Animation | Notes |
|------|---------|-----------|-------|
| 0.0s | Car silhouette driving | Entrance: slide in from left | Simple, recognizable |
| 2.0s | Hand sticking out window | Entrance: FadeIn | Flat hand |
| 4.0s | Hand tilts upward | Transform: rotate 15 degrees | Key moment |
| 5.0s | Air deflection arrows | Entrance: GrowArrow downward | Shows air being pushed |
| 7.0s | Upward force arrow | Entrance: GrowArrow upward | Reaction force |
| 9.0s | "You just created lift" text | Entrance: Write | Below the diagram |
| 12.0s | Car morphs into wing shape | Transform: smooth morph | Connection moment |
| 15.0s | Wing with same arrows | Transform: arrows stay, context changes | Continuity |
| 18.0s | All elements | Exit: fade_out_all | Clean slate |

SVGs Needed: car-silhouette.svg, hand-flat.svg
Camera: Static, subtle zoom on tilt moment
Transition to Next: Fade

## Scene 4: Newton and Bernoulli Together
Duration: 25s

Visual Goal: Show both forces working as one unified system

| Time | Element | Animation | Notes |
|------|---------|-----------|-------|
| 0.0s | "Newton's Third Law" title | Entrance: Write | POS_TITLE |
| 2.0s | Wing with air deflection | Entrance: Create | Air going DOWN |
| 5.0s | Reaction arrow (lift) | Entrance: GrowArrow UP | Equal and opposite |
| 8.0s | Divider line | Entrance: Create | Split screen |
| 9.0s | "Bernoulli's Principle" title | Entrance: Write | Right side |
| 11.0s | Pressure gradient colors | Entrance: FadeIn | Blue above, red below |
| 14.0s | Divider | Exit: Uncreate | Merge the two |
| 16.0s | Unified diagram | Transform: merge both | Both forces on one wing |
| 19.0s | "The real answer: BOTH" text | Entrance: FadeIn, scale emphasis | Center, bold |
| 22.0s | All elements | Exit: FadeOut | Prepare for next |

SVGs Needed: None (use Manim primitives and arrows)
Camera: Static
Transition to Next: Fade to dark

## Scene 5: Outro
Duration: 10s

Visual Goal: Recap and call to action

| Time | Element | Animation | Notes |
|------|---------|-----------|-------|
| 0.0s | Final recap wing diagram | Entrance: FadeIn | Simple, clean |
| 2.0s | Key labels | Entrance: stagger Write | Newton + Bernoulli |
| 5.0s | "Subscribe" CTA | Entrance: FadeIn with shift | BRAND_PRIMARY color |
| 7.0s | Channel logo | Entrance: FadeIn | Small, bottom |
| 9.0s | All elements | Exit: FadeOut | Clean ending |

SVGs Needed: channel-logo.svg
Camera: Static
Transition to Next: Fade to black
"""


def _placeholder_animation_plan() -> str:
    return """scenes:
  - name: Hook
    duration: 12
    objects:
      - type: Text
        content: "400 TONS"
        position: center
        font_size: 56
        color: BRAND_SECONDARY
      - type: Text
        content: "How?"
        position: center
        font_size: 48
        color: BRAND_LIGHT
    animations:
      - action: FadeIn
        target: text_0
        time: 0.0
        run_time: FADE_NORMAL
      - action: FadeIn
        target: text_1
        time: 8.0
        run_time: FADE_SLOW
      - action: FadeOut
        target: all
        time: 11.0

  - name: WrongAnswer
    duration: 18
    objects:
      - type: Text
        content: "The Textbook Answer"
        position: top
        font_size: 44
      - type: Arrow
        start: left
        end: right
        color: BRAND_PRIMARY
      - type: Text
        content: "WRONG"
        position: center
        font_size: 56
        color: BRAND_ERROR
    animations:
      - action: Write
        target: text_0
        time: 0.0
      - action: GrowArrow
        target: arrow_0
        time: 3.0
      - action: FadeIn
        target: text_1
        time: 9.0
        run_time: FADE_FAST
      - action: FadeOut
        target: all
        time: 16.0

  - name: HandWindow
    duration: 20
    objects:
      - type: Text
        content: "You just created lift"
        position: bottom
        font_size: 36
      - type: Arrow
        direction: up
        color: BRAND_ACCENT
      - type: Arrow
        direction: down
        color: BRAND_MUTED
    animations:
      - action: GrowArrow
        target: arrow_1
        time: 5.0
      - action: GrowArrow
        target: arrow_0
        time: 7.0
      - action: Write
        target: text_0
        time: 9.0
      - action: FadeOut
        target: all
        time: 18.0

  - name: NewtonBernoulli
    duration: 25
    objects:
      - type: Text
        content: "Newton's Third Law"
        position: top_left
        font_size: 36
      - type: Text
        content: "Bernoulli's Principle"
        position: top_right
        font_size: 36
      - type: Text
        content: "The real answer: BOTH"
        position: center
        font_size: 44
        color: BRAND_PRIMARY
    animations:
      - action: Write
        target: text_0
        time: 0.0
      - action: Write
        target: text_1
        time: 9.0
      - action: FadeIn
        target: text_2
        time: 19.0
        run_time: FADE_SLOW
      - action: FadeOut
        target: all
        time: 23.0

  - name: Outro
    duration: 10
    objects:
      - type: Text
        content: "Subscribe for more"
        position: center
        font_size: 42
        color: BRAND_PRIMARY
    animations:
      - action: FadeIn
        target: text_0
        time: 5.0
      - action: FadeOut
        target: all
        time: 9.0
"""


def _placeholder_manim_code() -> str:
    return '''"""Auto-generated Manim scenes for educational video."""

from manim import *  # noqa: F403

from studio.base import StudioScene
from studio.styles import *  # noqa: F403


class Hook(StudioScene):
    """Opening hook - 400 tons in the sky."""

    def construct(self):
        # Weight reveal
        weight = brand_text("400 TONS", font_size=FONT_SIZE_HERO, color=BRAND_SECONDARY)
        weight.move_to(POS_CENTER)
        self.play(FadeIn(weight, scale=0.5), run_time=FADE_SLOW)
        self.pause_medium()

        # Elephant comparison
        subtitle = brand_text("= 80 elephants", font_size=FONT_SIZE_SUBTITLE)
        subtitle.next_to(weight, DOWN, buff=0.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=FADE_NORMAL)
        self.pause_medium()

        # The question
        self.fade_out_all()
        self.pause_beat()

        question = brand_text("And somehow... it flies.", font_size=FONT_SIZE_TITLE)
        question.move_to(POS_CENTER)
        self.play(Write(question), run_time=WRITE_SPEED)
        self.pause_medium()

        how = brand_text("How?", font_size=FONT_SIZE_HERO, color=BRAND_PRIMARY)
        how.move_to(POS_CENTER + DOWN * 1.5)
        self.play(FadeIn(how, scale=1.5), run_time=FADE_SLOW)
        self.pause_medium()
        self.fade_out_all()


class WrongAnswer(StudioScene):
    """Debunk the equal transit time myth."""

    def construct(self):
        title = self.make_title("What Your Teacher Said")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.pause_beat()

        # Wing cross section
        wing = Ellipse(width=5, height=1.2, color=BRAND_LIGHT)
        wing.set_fill(BRAND_DARK, opacity=0.8)
        wing.move_to(POS_CENTER)
        self.play(Create(wing), run_time=FADE_NORMAL)

        # Top arrow (longer path)
        top_arrow = CurvedArrow(
            LEFT * 2.5 + UP * 0.2, RIGHT * 2.5 + UP * 0.2,
            angle=-0.5, color=BRAND_PRIMARY
        )
        bot_arrow = Arrow(LEFT * 2.5 + DOWN * 0.2, RIGHT * 2.5 + DOWN * 0.2, color=BRAND_MUTED)
        self.play(GrowArrow(top_arrow), run_time=FADE_NORMAL)
        self.pause_beat()
        self.play(GrowArrow(bot_arrow), run_time=FADE_NORMAL)
        self.pause_medium()

        # Stamp it wrong
        wrong = brand_text("WRONG", font_size=FONT_SIZE_HERO, color=BRAND_ERROR)
        wrong.move_to(POS_CENTER)
        wrong.rotate(PI / 12)
        self.play(FadeIn(wrong, scale=2.0), run_time=FADE_FAST)
        self.pause_medium()
        self.fade_out_all()


class HandWindow(StudioScene):
    """The hand-out-the-window analogy for lift."""

    def construct(self):
        title = self.make_title("The Car Window Test")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.pause_beat()

        # Hand representation
        hand = Rectangle(width=2, height=0.3, color=BRAND_LIGHT)
        hand.set_fill(BRAND_LIGHT, opacity=0.8)
        hand.move_to(POS_CENTER)
        self.play(FadeIn(hand), run_time=FADE_NORMAL)
        self.pause_beat()

        # Tilt the hand
        self.play(Rotate(hand, angle=PI / 12), run_time=FADE_NORMAL)
        self.pause_beat()

        # Air arrows going down
        air_arrows = VGroup(*[
            Arrow(
                hand.get_center() + RIGHT * (i - 1) + UP * 0.5,
                hand.get_center() + RIGHT * (i - 1) + DOWN * 1.5,
                color=BRAND_MUTED, stroke_width=2
            )
            for i in range(3)
        ])
        self.play(
            *[GrowArrow(a) for a in air_arrows],
            run_time=FADE_NORMAL,
        )
        self.pause_beat()

        # Lift arrow going up
        lift = Arrow(
            hand.get_center() + DOWN * 0.3,
            hand.get_center() + UP * 2.0,
            color=BRAND_ACCENT, stroke_width=4
        )
        lift_label = brand_text("LIFT", font_size=FONT_SIZE_BODY, color=BRAND_ACCENT)
        lift_label.next_to(lift, RIGHT, buff=0.2)
        self.play(GrowArrow(lift), FadeIn(lift_label), run_time=FADE_NORMAL)
        self.pause_medium()

        # Reveal
        reveal = brand_text("You just created lift.", font_size=FONT_SIZE_SUBTITLE)
        reveal.move_to(POS_FOOTER)
        self.play(Write(reveal), run_time=WRITE_SPEED)
        self.pause_medium()
        self.fade_out_all()


class BothForces(StudioScene):
    """Newton AND Bernoulli - the real answer is both."""

    def construct(self):
        # Newton side
        newton_title = brand_text("Newton", font_size=FONT_SIZE_TITLE, color=BRAND_PRIMARY)
        newton_title.move_to(UP * 2.5 + LEFT * 3)
        self.play(Write(newton_title), run_time=WRITE_SPEED)

        newton_desc = brand_text("Push air down\\nAir pushes you up", font_size=FONT_SIZE_BODY)
        newton_desc.move_to(LEFT * 3)
        self.play(FadeIn(newton_desc, shift=UP * 0.3), run_time=FADE_NORMAL)
        self.pause_medium()

        # Bernoulli side
        bern_title = brand_text("Bernoulli", font_size=FONT_SIZE_TITLE, color=BRAND_SECONDARY)
        bern_title.move_to(UP * 2.5 + RIGHT * 3)
        self.play(Write(bern_title), run_time=WRITE_SPEED)

        bern_desc = brand_text(
            "Fast air = low pressure\\nWing gets sucked up",
            font_size=FONT_SIZE_BODY,
        )
        bern_desc.move_to(RIGHT * 3)
        self.play(FadeIn(bern_desc, shift=UP * 0.3), run_time=FADE_NORMAL)
        self.pause_medium()

        # Merge
        plus = brand_text("+", font_size=FONT_SIZE_HERO, color=BRAND_ACCENT)
        plus.move_to(POS_CENTER)
        self.play(FadeIn(plus, scale=2.0), run_time=FADE_NORMAL)
        self.pause_beat()

        # The answer
        self.fade_out_all()
        answer = brand_text(
            "The real answer: BOTH", font_size=FONT_SIZE_HERO, color=BRAND_PRIMARY
        )
        answer.move_to(POS_CENTER)
        self.play(FadeIn(answer, scale=0.5), run_time=FADE_SLOW)
        self.pause_long()
        self.fade_out_all()


class Outro(StudioScene):
    """Recap and subscribe CTA."""

    def construct(self):
        # Recap line
        recap = brand_text(
            "It is not magic. It is just pushing air down.",
            font_size=FONT_SIZE_SUBTITLE,
        )
        recap.move_to(UP * 1.0)
        self.play(Write(recap), run_time=WRITE_SPEED)
        self.pause_medium()

        # CTA
        cta = brand_text("Subscribe for more", font_size=FONT_SIZE_TITLE, color=BRAND_PRIMARY)
        cta.move_to(DOWN * 0.5)
        self.play(FadeIn(cta, shift=UP * 0.3), run_time=FADE_NORMAL)
        self.pause_long()
        self.fade_out_all()
'''
