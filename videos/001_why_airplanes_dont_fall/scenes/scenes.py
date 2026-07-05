"""
Why Airplanes Don't Fall - Scene Classes

Production-quality Manim scenes using the studio/ library.
Each scene inherits from StudioScene and uses brand helpers.
"""

from manim import *  # noqa: F403

from studio.base import StudioScene
from studio.styles import *  # noqa: F403


class Intro(StudioScene):
    """Opening hook: 400 tons, 80 elephants, and a question."""

    def construct(self):
        # Weight reveal
        weight_num = brand_text("400", font_size=FONT_SIZE_HERO, color=BRAND_LIGHT)
        weight_unit = brand_text(" TONS", font_size=FONT_SIZE_HERO, color=BRAND_SECONDARY)
        weight = VGroup(weight_num, weight_unit).arrange(RIGHT, buff=0.1)
        weight.move_to(UP * 1.5)

        self.play(FadeIn(weight_num, scale=0.3), run_time=FADE_SLOW)
        self.pause_beat()
        self.play(FadeIn(weight_unit, shift=LEFT * 0.5), run_time=FADE_FAST)
        self.pause_medium()

        # Elephant comparison
        elephants_text = brand_text(
            "= 80 elephants", font_size=FONT_SIZE_SUBTITLE, color=BRAND_MUTED
        )
        elephants_text.next_to(weight, DOWN, buff=0.6)
        self.play(FadeIn(elephants_text, shift=UP * 0.3), run_time=FADE_NORMAL)
        self.pause_medium()

        # Transform to plane shape
        plane_text = brand_text(
            "And somehow... it flies.",
            font_size=FONT_SIZE_BODY,
            color=BRAND_LIGHT,
        )
        plane_text.next_to(elephants_text, DOWN, buff=0.6)
        self.play(Write(plane_text), run_time=WRITE_SPEED)
        self.pause_medium()

        # The big question
        self.fade_out_all()
        self.pause_beat()

        how = brand_text("How?", font_size=FONT_SIZE_HERO, color=BRAND_PRIMARY)
        how.move_to(POS_CENTER)
        self.play(FadeIn(how, scale=1.5), run_time=FADE_SLOW)
        self.pause_medium()
        self.fade_out_all()


class WindAndWing(StudioScene):
    """Debunk the textbook myth, then explain via hand-out-window analogy."""

    def construct(self):
        self._show_wrong_answer()
        self._show_hand_analogy()

    def _show_wrong_answer(self):
        """Part 1: Show and debunk the equal transit time myth."""
        title = self.make_title("What Your Teacher Said")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.pause_beat()

        # Wing cross-section
        wing = Ellipse(width=5, height=1.0, color=BRAND_LIGHT, stroke_width=2)
        wing.set_fill(BRAND_DARK, opacity=0.5)
        wing.move_to(POS_CENTER)
        self.play(Create(wing), run_time=FADE_NORMAL)
        self.pause_beat()

        # Curved top arrow (longer path)
        top_arrow = CurvedArrow(
            LEFT * 2.5 + UP * 0.8,
            RIGHT * 2.5 + UP * 0.3,
            angle=-0.4,
            color=BRAND_PRIMARY,
        )
        self.play(GrowArrow(top_arrow), run_time=FADE_NORMAL)
        self.pause_beat()

        # Straight bottom arrow
        bot_arrow = Arrow(
            LEFT * 2.5 + DOWN * 0.6,
            RIGHT * 2.5 + DOWN * 0.3,
            color=BRAND_MUTED,
            stroke_width=2,
        )
        self.play(GrowArrow(bot_arrow), run_time=FADE_NORMAL)
        self.pause_short()

        # Label
        longer_label = brand_text(
            "Longer path = faster?", font_size=FONT_SIZE_CAPTION, color=BRAND_MUTED
        )
        longer_label.next_to(top_arrow, UP, buff=0.2)
        self.play(FadeIn(longer_label), run_time=FADE_FAST)
        self.pause_medium()

        # WRONG stamp
        wrong = brand_text("WRONG", font_size=FONT_SIZE_HERO, color=BRAND_ERROR)
        wrong.move_to(POS_CENTER)
        wrong.rotate(PI / 12)
        self.play(FadeIn(wrong, scale=2.0), run_time=FADE_FAST)
        self.pause_medium()

        self.fade_out_all()
        self.pause_beat()

    def _show_hand_analogy(self):
        """Part 2: The hand-out-the-car-window analogy."""
        title = self.make_title("The Car Window Test")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.pause_beat()

        # Hand (flat rectangle)
        hand = Rectangle(width=2.5, height=0.25, color=BRAND_LIGHT, stroke_width=2)
        hand.set_fill(BRAND_LIGHT, opacity=0.7)
        hand.move_to(POS_CENTER)
        self.play(FadeIn(hand), run_time=FADE_NORMAL)
        self.pause_short()

        # Wind streaks (show motion context)
        wind_lines = VGroup(
            *[
                Line(
                    LEFT * 5 + UP * (i * 0.4 - 0.8),
                    LEFT * 3.5 + UP * (i * 0.4 - 0.8),
                    color=BRAND_MUTED,
                    stroke_width=1,
                    stroke_opacity=0.5,
                )
                for i in range(5)
            ]
        )
        self.play(Create(wind_lines), run_time=FADE_FAST)
        self.pause_beat()

        # Tilt the hand
        self.play(Rotate(hand, angle=PI / 12), run_time=FADE_NORMAL)
        self.pause_beat()

        # Air deflection arrows going down
        air_down = VGroup(
            *[
                Arrow(
                    hand.get_center() + RIGHT * (i - 1) * 0.8 + DOWN * 0.2,
                    hand.get_center() + RIGHT * (i - 1) * 0.8 + DOWN * 1.8,
                    color=BRAND_MUTED,
                    stroke_width=2,
                    max_tip_length_to_length_ratio=0.2,
                )
                for i in range(4)
            ]
        )
        self.play(
            *[GrowArrow(a) for a in air_down],
            run_time=FADE_NORMAL,
        )
        self.pause_beat()

        # Lift arrow going up
        lift_arrow = Arrow(
            hand.get_center() + DOWN * 0.2,
            hand.get_center() + UP * 2.2,
            color=BRAND_ACCENT,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.15,
        )
        lift_label = brand_text("LIFT", font_size=FONT_SIZE_BODY, color=BRAND_ACCENT)
        lift_label.next_to(lift_arrow, RIGHT, buff=0.2)

        self.play(GrowArrow(lift_arrow), run_time=FADE_NORMAL)
        self.play(FadeIn(lift_label, shift=LEFT * 0.2), run_time=FADE_FAST)
        self.pause_medium()

        # Reveal text
        reveal = brand_text(
            "You just created lift.", font_size=FONT_SIZE_SUBTITLE, color=BRAND_LIGHT
        )
        reveal.move_to(POS_FOOTER)
        self.play(Write(reveal), run_time=WRITE_SPEED)
        self.pause_medium()

        self.fade_out_all()


class LiftExplained(StudioScene):
    """Newton's third law AND Bernoulli's principle - the real answer is both."""

    def construct(self):
        self._show_newton()
        self._show_bernoulli()
        self._merge_both()

    def _show_newton(self):
        """Newton's third law explanation."""
        title = self.make_title("Newton's Third Law")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.pause_beat()

        # Wing shape
        wing = Polygon(
            LEFT * 2.5,
            RIGHT * 2.5 + UP * 0.1,
            RIGHT * 2.5 + DOWN * 0.1,
            LEFT * 2.5 + DOWN * 0.3,
            color=BRAND_LIGHT,
            stroke_width=2,
        )
        wing.set_fill(BRAND_LIGHT, opacity=0.3)
        wing.move_to(POS_CENTER)
        self.play(Create(wing), run_time=FADE_NORMAL)
        self.pause_beat()

        # Air pushed DOWN arrows
        air_down_arrows = VGroup(
            *[
                Arrow(
                    wing.get_center() + RIGHT * (i - 1.5) * 1.2 + DOWN * 0.3,
                    wing.get_center() + RIGHT * (i - 1.5) * 1.2 + DOWN * 2.0,
                    color=BRAND_PRIMARY,
                    stroke_width=3,
                )
                for i in range(4)
            ]
        )
        action_label = brand_text("Action: air DOWN", font_size=FONT_SIZE_CAPTION)
        action_label.next_to(air_down_arrows, DOWN, buff=0.2)

        self.play(
            *[GrowArrow(a) for a in air_down_arrows],
            run_time=FADE_NORMAL,
        )
        self.play(FadeIn(action_label), run_time=FADE_FAST)
        self.pause_beat()

        # Reaction: wing pushed UP
        lift_arrow = Arrow(
            wing.get_center() + UP * 0.2,
            wing.get_center() + UP * 2.5,
            color=BRAND_ACCENT,
            stroke_width=5,
        )
        reaction_label = brand_text(
            "Reaction: wing UP", font_size=FONT_SIZE_CAPTION, color=BRAND_ACCENT
        )
        reaction_label.next_to(lift_arrow, RIGHT, buff=0.2)

        self.play(GrowArrow(lift_arrow), run_time=FADE_NORMAL)
        self.play(FadeIn(reaction_label), run_time=FADE_FAST)
        self.pause_medium()

        # Pulse the lift arrow for emphasis
        self.play(
            lift_arrow.animate.scale(1.2),
            run_time=FADE_FAST,
        )
        self.play(
            lift_arrow.animate.scale(1 / 1.2),
            run_time=FADE_FAST,
        )
        self.pause_short()
        self.fade_out_all()

    def _show_bernoulli(self):
        """Bernoulli's principle explanation."""
        title = self.make_title("Bernoulli's Principle")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.pause_beat()

        # Wing with pressure zones
        wing = Ellipse(width=5, height=1.2, color=BRAND_LIGHT, stroke_width=2)
        wing.set_fill(BRAND_DARK, opacity=0.5)
        wing.move_to(POS_CENTER)
        self.play(Create(wing), run_time=FADE_NORMAL)
        self.pause_beat()

        # Low pressure zone above (blue)
        low_p = Rectangle(width=4.5, height=1.2, color=BRAND_PRIMARY, stroke_width=0)
        low_p.set_fill(BRAND_PRIMARY, opacity=0.2)
        low_p.next_to(wing, UP, buff=0.0)
        low_label = brand_text("LOW pressure", font_size=FONT_SIZE_CAPTION, color=BRAND_PRIMARY)
        low_label.next_to(low_p, UP, buff=0.1)

        self.play(FadeIn(low_p), run_time=FADE_NORMAL)
        self.play(FadeIn(low_label), run_time=FADE_FAST)
        self.pause_beat()

        # High pressure zone below (red/warm)
        high_p = Rectangle(width=4.5, height=1.0, color=BRAND_SECONDARY, stroke_width=0)
        high_p.set_fill(BRAND_SECONDARY, opacity=0.2)
        high_p.next_to(wing, DOWN, buff=0.0)
        high_label = brand_text("HIGH pressure", font_size=FONT_SIZE_CAPTION, color=BRAND_SECONDARY)
        high_label.next_to(high_p, DOWN, buff=0.1)

        self.play(FadeIn(high_p), run_time=FADE_NORMAL)
        self.play(FadeIn(high_label), run_time=FADE_FAST)
        self.pause_medium()

        self.fade_out_all()

    def _merge_both(self):
        """Combine Newton and Bernoulli into unified explanation."""
        # Newton side
        newton_title = brand_text("Newton", font_size=FONT_SIZE_TITLE, color=BRAND_PRIMARY)
        newton_title.move_to(UP * 2.5 + LEFT * 3)

        newton_arrow = Arrow(ORIGIN, DOWN * 1.5, color=BRAND_PRIMARY, stroke_width=3)
        newton_arrow.move_to(LEFT * 3 + DOWN * 0.3)

        self.play(Write(newton_title), run_time=WRITE_SPEED)
        self.play(GrowArrow(newton_arrow), run_time=FADE_NORMAL)
        self.pause_beat()

        # Bernoulli side
        bern_title = brand_text("Bernoulli", font_size=FONT_SIZE_TITLE, color=BRAND_SECONDARY)
        bern_title.move_to(UP * 2.5 + RIGHT * 3)

        bern_arrow = Arrow(ORIGIN, UP * 1.5, color=BRAND_SECONDARY, stroke_width=3)
        bern_arrow.move_to(RIGHT * 3 + DOWN * 0.3)

        self.play(Write(bern_title), run_time=WRITE_SPEED)
        self.play(GrowArrow(bern_arrow), run_time=FADE_NORMAL)
        self.pause_medium()

        # Plus sign
        plus = brand_text("+", font_size=FONT_SIZE_HERO, color=BRAND_ACCENT)
        plus.move_to(POS_CENTER + UP * 0.5)
        self.play(FadeIn(plus, scale=2.0), run_time=FADE_NORMAL)
        self.pause_beat()

        # The answer
        self.fade_out_all()
        self.pause_beat()

        answer = brand_text(
            "The real answer: BOTH",
            font_size=FONT_SIZE_HERO,
            color=BRAND_PRIMARY,
        )
        answer.move_to(POS_CENTER)
        self.play(FadeIn(answer, scale=0.5), run_time=FADE_SLOW)
        self.pause_long()
        self.fade_out_all()


class MythBust(StudioScene):
    """Debunk equal transit time and show angle of attack / stall."""

    def construct(self):
        self._debunk_transit_time()
        self._show_angle_of_attack()

    def _debunk_transit_time(self):
        """Show that equal transit time is wrong."""
        title = self.make_title("The Myth")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.pause_beat()

        # The myth text
        myth_text = brand_text(
            "Equal Transit Time",
            font_size=FONT_SIZE_SUBTITLE,
            color=BRAND_MUTED,
        )
        myth_text.move_to(POS_CENTER + UP * 0.5)
        self.play(Write(myth_text), run_time=WRITE_SPEED)
        self.pause_short()

        # Explanation
        explanation = brand_text(
            "Air splits and meets at the back at the same time",
            font_size=FONT_SIZE_CAPTION,
            color=BRAND_MUTED,
        )
        explanation.next_to(myth_text, DOWN, buff=0.4)
        self.play(FadeIn(explanation, shift=UP * 0.2), run_time=FADE_NORMAL)
        self.pause_medium()

        # Strikethrough
        strike_line = Line(
            myth_text.get_left() + LEFT * 0.2,
            myth_text.get_right() + RIGHT * 0.2,
            color=BRAND_ERROR,
            stroke_width=4,
        )
        self.play(Create(strike_line), run_time=FADE_NORMAL)
        self.pause_beat()

        # NASA debunked
        nasa_text = brand_text(
            "Debunked by NASA",
            font_size=FONT_SIZE_CAPTION,
            color=BRAND_ERROR,
        )
        nasa_text.move_to(POS_FOOTER)
        self.play(FadeIn(nasa_text, shift=UP * 0.2), run_time=FADE_NORMAL)
        self.pause_medium()

        self.fade_out_all()
        self.pause_beat()

    def _show_angle_of_attack(self):
        """Show angle of attack and stall."""
        title = self.make_title("Angle of Attack")
        self.play(Write(title), run_time=WRITE_SPEED)
        self.pause_beat()

        # Wing at neutral angle
        wing = Rectangle(width=4, height=0.2, color=BRAND_LIGHT, stroke_width=2)
        wing.set_fill(BRAND_LIGHT, opacity=0.6)
        wing.move_to(POS_CENTER)
        self.play(FadeIn(wing), run_time=FADE_NORMAL)
        self.pause_beat()

        # Small lift arrow
        lift = Arrow(
            wing.get_center(),
            wing.get_center() + UP * 1.0,
            color=BRAND_ACCENT,
            stroke_width=3,
        )
        self.play(GrowArrow(lift), run_time=FADE_NORMAL)
        self.pause_short()

        # Increase angle - more lift
        self.play(
            Rotate(wing, angle=PI / 18),  # ~10 degrees
            lift.animate.put_start_and_end_on(wing.get_center(), wing.get_center() + UP * 1.8),
            run_time=FADE_NORMAL,
        )
        self.pause_short()

        # More angle
        angle_label = brand_text(
            "More angle = more lift", font_size=FONT_SIZE_BODY, color=BRAND_ACCENT
        )
        angle_label.move_to(POS_FOOTER)
        self.play(FadeIn(angle_label), run_time=FADE_FAST)
        self.pause_medium()

        # Too much angle - STALL
        self.play(FadeOut(angle_label), run_time=FADE_FAST)

        self.play(
            Rotate(wing, angle=PI / 12),  # Another 15 degrees
            lift.animate.put_start_and_end_on(wing.get_center(), wing.get_center() + UP * 0.3),
            run_time=FADE_SLOW,
        )
        self.pause_beat()

        # Stall indicator
        stall_text = brand_text("STALL", font_size=FONT_SIZE_HERO, color=BRAND_ERROR)
        stall_text.move_to(POS_CENTER + DOWN * 1.5)
        self.play(FadeIn(stall_text, scale=1.5), run_time=FADE_FAST)
        self.pause_beat()

        too_much = brand_text(
            "Too much angle = airflow separates = no lift",
            font_size=FONT_SIZE_CAPTION,
            color=BRAND_MUTED,
        )
        too_much.move_to(POS_FOOTER)
        self.play(FadeIn(too_much, shift=UP * 0.2), run_time=FADE_NORMAL)
        self.pause_medium()

        self.fade_out_all()


class Outro(StudioScene):
    """Recap the key insight and call to action."""

    def construct(self):
        # Recap
        recap = brand_text(
            "Not magic. Just pushing air down.",
            font_size=FONT_SIZE_TITLE,
            color=BRAND_LIGHT,
        )
        recap.move_to(UP * 1.0)
        self.play(Write(recap), run_time=WRITE_SPEED)
        self.pause_medium()

        # Newton + Bernoulli summary
        summary = brand_text(
            "Newton + Bernoulli = Flight",
            font_size=FONT_SIZE_BODY,
            color=BRAND_MUTED,
        )
        summary.move_to(ORIGIN)
        self.play(FadeIn(summary, shift=UP * 0.3), run_time=FADE_NORMAL)
        self.pause_medium()

        # CTA
        self.fade_out_all()
        self.pause_beat()

        cta = brand_text("Subscribe for more", font_size=FONT_SIZE_TITLE, color=BRAND_PRIMARY)
        cta.move_to(UP * 0.5)
        self.play(FadeIn(cta, shift=UP * 0.3), run_time=FADE_NORMAL)
        self.pause_beat()

        next_vid = brand_text(
            "Next: Why Ships Don't Sink",
            font_size=FONT_SIZE_BODY,
            color=BRAND_MUTED,
        )
        next_vid.move_to(DOWN * 1.0)
        self.play(FadeIn(next_vid, shift=UP * 0.2), run_time=FADE_NORMAL)
        self.pause_long()
        self.fade_out_all()
