"""
Video: Why Airplanes Don't Fall

Timing-synchronized scenes. Each scene's total duration matches
the corresponding narration segment from timing.yaml.

Scene mapping to timing.yaml:
  Intro         → timing scenes: Intro (12.8s)
  WindAndWing   → timing scenes: WindAndWing + TheRealExplanationPart1 (36.5s)
  LiftExplained → timing scenes: LiftExplained + BernoulliJoins (32.3s)
  MythBust      → timing scenes: MythBust + TheSecretVariable (35.1s)
  Outro         → timing scenes: Outro (23.3s)

Total target: ~143s (2:23)
"""

from pathlib import Path

from manim import *  # noqa: F403, F405

from studio.base import StudioScene
from studio.styles import *  # noqa: F403, F405
from studio.timing import load_timing

# Load timing for this video
VIDEO_DIR = Path(__file__).resolve().parent.parent
TIMING = load_timing(VIDEO_DIR)


def _scene_dur(*names: str) -> float:
    """Sum durations of multiple timing scenes."""
    total = 0.0
    for name in names:
        s = TIMING.get_scene(name)
        if s:
            total += s.duration
    return max(total, 5.0)  # minimum 5s safety


class Intro(StudioScene):
    """Hook: 400 tons, 80 elephants, somehow it flies."""

    def construct(self):
        target = _scene_dur("Intro")

        # "400 TONS" scales up
        tons = brand_text("400", font_size=FONT_SIZE_HERO, color=BRAND_PRIMARY)
        tons_label = brand_text("TONS", font_size=FONT_SIZE_TITLE, color=BRAND_LIGHT)
        tons_label.next_to(tons, RIGHT, buff=0.3)
        tons_group = VGroup(tons, tons_label).move_to(UP * 1.0)

        self.play(FadeIn(tons, scale=1.5), run_time=1.0)
        self.play(FadeIn(tons_label, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(1.5)

        # "= 80 elephants"
        elephants = brand_text("= 80 elephants", font_size=FONT_SIZE_BODY, color=BRAND_MUTED)
        elephants.next_to(tons_group, DOWN, buff=0.5)
        self.play(FadeIn(elephants, shift=UP * 0.2), run_time=0.8)
        self.wait(1.0)

        # "And somehow... it flies"
        flies = brand_text(
            "And somehow... it flies.", font_size=FONT_SIZE_SUBTITLE, color=BRAND_ACCENT
        )
        flies.move_to(DOWN * 1.5)
        self.play(Write(flies), run_time=1.2)
        self.wait(1.5)

        # "How?"
        self.fade_out_all()
        self.pause_beat()
        how = brand_text("How?", font_size=FONT_SIZE_HERO, color=BRAND_PRIMARY)
        self.play(FadeIn(how, scale=1.5), run_time=0.8)

        # Pad remaining time
        elapsed = 1.0 + 0.5 + 1.5 + 0.8 + 1.0 + 1.2 + 1.5 + FADE_NORMAL + PAUSE_BEAT + 0.8
        remaining = target - elapsed
        if remaining > 0:
            self.wait(remaining)

        self.fade_out_all()


class WindAndWing(StudioScene):
    """Debunk the myth + hand-out-window analogy."""

    def construct(self):
        target = _scene_dur("WindAndWing", "TheRealExplanationPart1")

        # Part 1: The wrong textbook answer
        title = self.make_title("What Your Teacher Said")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.wait(1.0)

        # Wing cross-section
        wing = Ellipse(width=5, height=1.0, color=BRAND_LIGHT, stroke_width=2)
        wing.set_fill(BRAND_DARK, opacity=0.5)
        wing.move_to(POS_CENTER)
        self.play(Create(wing), run_time=1.0)
        self.wait(2.0)

        # Arrows showing airflow
        top_path = Arc(radius=2.5, start_angle=PI * 0.8, angle=-PI * 0.6, color=BRAND_PRIMARY)
        top_path.shift(UP * 0.3)
        self.play(Create(top_path), run_time=1.5)
        self.wait(1.5)

        bot_line = Line(LEFT * 2.5 + DOWN * 0.5, RIGHT * 2.5 + DOWN * 0.3, color=BRAND_MUTED)
        self.play(Create(bot_line), run_time=0.8)
        self.wait(2.0)

        # WRONG stamp
        wrong = brand_text("WRONG", font_size=FONT_SIZE_HERO, color=BRAND_ERROR)
        wrong.rotate(PI / 12)
        self.play(FadeIn(wrong, scale=2.0), run_time=0.5)
        self.wait(2.0)

        self.fade_out_all()
        self.wait(1.0)

        # Part 2: Hand out car window
        title2 = self.make_title("The Car Window Test")
        self.play(Write(title2), run_time=WRITE_SPEED)
        self.wait(1.0)

        # Hand (rectangle)
        hand = Rectangle(width=2.5, height=0.25, color=BRAND_LIGHT, stroke_width=2)
        hand.set_fill(BRAND_LIGHT, opacity=0.7)
        self.play(FadeIn(hand), run_time=0.5)
        self.wait(1.5)

        # Wind lines
        wind = VGroup(
            *[
                Line(
                    LEFT * 4 + UP * (i * 0.3 - 0.6),
                    LEFT * 2.5 + UP * (i * 0.3 - 0.6),
                    color=BRAND_MUTED,
                    stroke_width=1,
                    stroke_opacity=0.5,
                )
                for i in range(5)
            ]
        )
        self.play(Create(wind), run_time=0.5)
        self.wait(1.0)

        # Tilt hand
        self.play(Rotate(hand, angle=PI / 12), run_time=0.8)
        self.wait(1.5)

        # Lift arrow
        lift = Arrow(
            hand.get_center(), hand.get_center() + UP * 2, color=BRAND_ACCENT, stroke_width=4
        )
        lift_label = brand_text("LIFT", font_size=FONT_SIZE_BODY, color=BRAND_ACCENT)
        lift_label.next_to(lift, RIGHT, buff=0.2)
        self.play(Create(lift), run_time=0.8)
        self.play(FadeIn(lift_label), run_time=0.3)
        self.wait(2.0)

        # "You just created lift"
        reveal = brand_text(
            "You just created lift.", font_size=FONT_SIZE_SUBTITLE, color=BRAND_LIGHT
        )
        reveal.move_to(DOWN * 2.5)
        self.play(Write(reveal), run_time=1.0)

        # Pad to target
        elapsed = (
            WRITE_SPEED
            + 1.0
            + 1.0
            + 2.0
            + 1.5
            + 1.5
            + 0.8
            + 2.0
            + 0.5
            + 2.0
            + FADE_NORMAL
            + 1.0
            + WRITE_SPEED
            + 1.0
            + 0.5
            + 1.5
            + 0.5
            + 1.0
            + 0.8
            + 1.5
            + 0.8
            + 0.3
            + 2.0
            + 1.0
        )
        remaining = target - elapsed
        if remaining > 0:
            self.wait(remaining)

        self.fade_out_all()


class LiftExplained(StudioScene):
    """Newton's third law + Bernoulli's principle = the real answer."""

    def construct(self):
        target = _scene_dur("LiftExplained", "BernoulliJoins")

        # Newton's Third Law
        title = self.make_title("Newton's Third Law")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.wait(1.5)

        # Wing pushing air down
        wing = Ellipse(width=4, height=0.6, color=BRAND_LIGHT, stroke_width=2)
        wing.move_to(ORIGIN)
        self.play(Create(wing), run_time=0.8)
        self.wait(1.0)

        # Down arrows (action)
        down_arrows = VGroup(
            *[
                Arrow(
                    wing.get_center() + RIGHT * (i - 1.5) * 1.0,
                    wing.get_center() + DOWN * 2 + RIGHT * (i - 1.5) * 1.0,
                    color=BRAND_PRIMARY,
                    stroke_width=2,
                )
                for i in range(4)
            ]
        )
        action_label = brand_text("Action", font_size=FONT_SIZE_CAPTION, color=BRAND_PRIMARY)
        action_label.next_to(down_arrows, DOWN, buff=0.2)
        self.play(*[Create(a) for a in down_arrows], run_time=1.0)
        self.play(FadeIn(action_label), run_time=0.3)
        self.wait(2.0)

        # Up arrow (reaction)
        up_arrow = Arrow(
            wing.get_center() + DOWN * 0.3,
            wing.get_center() + UP * 2.5,
            color=BRAND_ACCENT,
            stroke_width=5,
        )
        reaction_label = brand_text(
            "Reaction = LIFT", font_size=FONT_SIZE_CAPTION, color=BRAND_ACCENT
        )
        reaction_label.next_to(up_arrow, RIGHT, buff=0.2)
        self.play(Create(up_arrow), run_time=1.0)
        self.play(FadeIn(reaction_label), run_time=0.3)
        self.wait(3.0)

        self.fade_out_all()
        self.wait(1.0)

        # Bernoulli's principle
        title2 = self.make_title("But That's Only Half")
        self.play(Write(title2), run_time=WRITE_SPEED)
        self.wait(1.5)

        # Airfoil with pressure zones
        wing2 = Ellipse(width=5, height=1.2, color=BRAND_LIGHT, stroke_width=2)
        wing2.move_to(ORIGIN)
        self.play(Create(wing2), run_time=0.8)
        self.wait(1.0)

        # Low pressure label on top
        low_p = brand_text("Low pressure", font_size=FONT_SIZE_CAPTION, color=BRAND_ACCENT)
        low_p.next_to(wing2, UP, buff=0.5)
        high_p = brand_text("High pressure", font_size=FONT_SIZE_CAPTION, color=BRAND_SECONDARY)
        high_p.next_to(wing2, DOWN, buff=0.5)
        self.play(FadeIn(low_p, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(high_p, shift=UP * 0.2), run_time=0.5)
        self.wait(2.5)

        # "Pressure difference pushes wing up"
        explanation = brand_text(
            "Pressure difference → net upward force", font_size=FONT_SIZE_BODY, color=BRAND_LIGHT
        )
        explanation.move_to(DOWN * 2.5)
        self.play(Write(explanation), run_time=1.2)
        self.wait(2.0)

        # "Both Newton AND Bernoulli"
        self.fade_out_all()
        self.pause_beat()
        both = brand_text("The answer: BOTH", font_size=FONT_SIZE_TITLE, color=BRAND_ACCENT)
        self.play(FadeIn(both, scale=1.2), run_time=0.8)

        # Pad
        elapsed = (
            WRITE_SPEED
            + 1.5
            + 0.8
            + 1.0
            + 1.0
            + 0.3
            + 2.0
            + 1.0
            + 0.3
            + 3.0
            + FADE_NORMAL
            + 1.0
            + WRITE_SPEED
            + 1.5
            + 0.8
            + 1.0
            + 0.5
            + 0.5
            + 2.5
            + 1.2
            + 2.0
            + FADE_NORMAL
            + PAUSE_BEAT
            + 0.8
        )
        remaining = target - elapsed
        if remaining > 0:
            self.wait(remaining)

        self.fade_out_all()


class MythBust(StudioScene):
    """Debunk equal transit time + reveal angle of attack."""

    def construct(self):
        target = _scene_dur("MythBust", "TheSecretVariable")

        # The myth
        title = self.make_title("The Biggest Myth")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.wait(1.5)

        myth_text = brand_text(
            '"Air on top must arrive at the same time"', font_size=FONT_SIZE_BODY, color=BRAND_MUTED
        )
        myth_text.move_to(ORIGIN)
        self.play(Write(myth_text), run_time=1.5)
        self.wait(2.5)

        # Cross it out
        cross = Line(myth_text.get_left(), myth_text.get_right(), color=BRAND_ERROR, stroke_width=4)
        self.play(Create(cross), run_time=0.5)
        self.wait(1.5)

        # "No physical law requires this"
        debunk = brand_text(
            "No physical law requires this.", font_size=FONT_SIZE_SUBTITLE, color=BRAND_LIGHT
        )
        debunk.move_to(DOWN * 1.5)
        self.play(FadeIn(debunk, shift=UP * 0.2), run_time=0.8)
        self.wait(2.5)

        self.fade_out_all()
        self.wait(1.0)

        # The secret: angle of attack
        title2 = self.make_title("The Secret Variable")
        self.play(Write(title2), run_time=WRITE_SPEED)
        self.wait(1.5)

        # Wing at angle
        wing = Rectangle(width=4, height=0.2, color=BRAND_LIGHT, stroke_width=2)
        wing.set_fill(BRAND_LIGHT, opacity=0.5)
        wing.rotate(PI / 15)
        wing.move_to(ORIGIN)
        self.play(FadeIn(wing), run_time=0.5)
        self.wait(1.0)

        # Angle arc
        angle_arc = Arc(radius=1.5, start_angle=0, angle=PI / 15, color=BRAND_ACCENT)
        angle_label = brand_text("Angle of Attack", font_size=FONT_SIZE_CAPTION, color=BRAND_ACCENT)
        angle_label.next_to(angle_arc, RIGHT, buff=0.3)
        self.play(Create(angle_arc), FadeIn(angle_label), run_time=0.8)
        self.wait(2.5)

        # "More angle = more lift (up to a point)"
        more_lift = brand_text(
            "More angle = more lift", font_size=FONT_SIZE_BODY, color=BRAND_LIGHT
        )
        more_lift.move_to(DOWN * 2.0)
        self.play(Write(more_lift), run_time=1.0)
        self.wait(2.0)

        # Increase angle animation
        self.play(Rotate(wing, angle=PI / 20), run_time=1.5)
        self.wait(2.0)

        # Pad
        elapsed = (
            WRITE_SPEED
            + 1.5
            + 1.5
            + 2.5
            + 0.5
            + 1.5
            + 0.8
            + 2.5
            + FADE_NORMAL
            + 1.0
            + WRITE_SPEED
            + 1.5
            + 0.5
            + 1.0
            + 0.8
            + 2.5
            + 1.0
            + 2.0
            + 1.5
            + 2.0
        )
        remaining = target - elapsed
        if remaining > 0:
            self.wait(remaining)

        self.fade_out_all()


class Outro(StudioScene):
    """Recap + CTA."""

    def construct(self):
        target = _scene_dur("Outro")

        # Recap title
        title = self.make_title("So Why Don't Planes Fall?")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.wait(2.0)

        # Three key points
        points = [
            "1. Wings deflect air downward (Newton)",
            "2. Curved shape creates pressure difference (Bernoulli)",
            "3. Angle of attack controls how much lift",
        ]

        point_group = VGroup()
        for i, point_text in enumerate(points):
            p = brand_text(point_text, font_size=FONT_SIZE_BODY, color=BRAND_LIGHT)
            p.move_to(UP * (0.5 - i * 1.0) + LEFT * 0.5)
            p.align_to(LEFT * 4.5, LEFT)
            point_group.add(p)
            self.play(FadeIn(p, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(1.5)

        self.wait(2.0)

        # "Next time you fly..."
        self.fade_out_all()
        self.pause_beat()
        closing = brand_text(
            "Next time you fly... look at the wing.",
            font_size=FONT_SIZE_SUBTITLE,
            color=BRAND_ACCENT,
        )
        self.play(FadeIn(closing, shift=UP * 0.2), run_time=0.8)
        self.wait(3.0)

        # Subscribe
        self.fade_out_all()
        self.pause_beat()
        sub = brand_text("Subscribe for more", font_size=FONT_SIZE_BODY, color=BRAND_PRIMARY)
        self.play(FadeIn(sub), run_time=0.5)

        # Pad
        elapsed = (
            WRITE_SPEED
            + 2.0
            + 3 * (0.6 + 1.5)
            + 2.0
            + FADE_NORMAL
            + PAUSE_BEAT
            + 0.8
            + 3.0
            + FADE_NORMAL
            + PAUSE_BEAT
            + 0.5
        )
        remaining = target - elapsed
        if remaining > 0:
            self.wait(remaining)

        self.fade_out_all()
