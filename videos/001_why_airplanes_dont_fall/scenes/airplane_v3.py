"""
Why Airplanes Don't Fall - V3 (Professional Quality)
Render: manim render -qh airplane_v3.py WhyAirplanesFlyV3
"""

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

# -- Palette -----------------------------------------------------------------
BG = "#0D0D1A"
BG_LIGHTER = "#141428"
GOLD = "#F5C842"
TEAL = "#2DCDC6"
CORAL = "#FF6B6B"
SOFT_WHT = "#E8E8F0"
MUTED = "#6B6B8A"
PURPLE = "#7B5EA7"
GREEN = "#4CAF7D"
DARK_BAR = "#0A0A14"

config.background_color = BG
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


# -- Custom Mobjects ---------------------------------------------------------
class BackgroundGradient(VGroup):
    """Full-screen gradient background with vignette effect."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Radial gradient approximation using concentric rectangles
        layers = 8
        for i in range(layers, 0, -1):
            opacity = 0.03 + (i / layers) * 0.12
            rect = Rectangle(
                width=16 * (i / layers),
                height=9 * (i / layers),
                fill_color=BG_LIGHTER,
                fill_opacity=opacity,
                stroke_width=0,
            )
            self.add(rect)
        # Vignette: dark edges
        vignette_top = Rectangle(
            width=16, height=2, fill_color=BLACK, fill_opacity=0.3, stroke_width=0
        ).move_to(UP * 3.5)
        vignette_bot = Rectangle(
            width=16, height=2, fill_color=BLACK, fill_opacity=0.4, stroke_width=0
        ).move_to(DOWN * 3.5)
        vignette_left = Rectangle(
            width=2, height=9, fill_color=BLACK, fill_opacity=0.2, stroke_width=0
        ).move_to(LEFT * 7)
        vignette_right = Rectangle(
            width=2, height=9, fill_color=BLACK, fill_opacity=0.2, stroke_width=0
        ).move_to(RIGHT * 7)
        self.add(vignette_top, vignette_bot, vignette_left, vignette_right)


class Airfoil(VGroup):
    """Realistic airfoil cross-section with camber."""

    def __init__(self, width=5.0, thickness=0.8, color=SOFT_WHT, **kwargs):
        super().__init__(**kwargs)
        # Upper surface (more curved)
        upper_points = [
            [-width / 2, 0, 0],
            [-width / 4, thickness * 0.7, 0],
            [0, thickness * 0.5, 0],
            [width / 4, thickness * 0.25, 0],
            [width / 2, 0, 0],
        ]
        # Lower surface (flatter)
        lower_points = [
            [-width / 2, 0, 0],
            [-width / 4, -thickness * 0.15, 0],
            [0, -thickness * 0.2, 0],
            [width / 4, -thickness * 0.1, 0],
            [width / 2, 0, 0],
        ]
        upper = VMobject(color=color, stroke_width=2.5)
        upper.set_points_smoothly([np.array(p) for p in upper_points])
        lower = VMobject(color=color, stroke_width=2.5)
        lower.set_points_smoothly([np.array(p) for p in lower_points])

        # Fill the shape
        full_shape = VMobject(color=color, stroke_width=2.5)
        all_pts = upper_points + lower_points[::-1]
        full_shape.set_points_smoothly([np.array(p) for p in all_pts])
        full_shape.set_fill(BG_LIGHTER, opacity=0.6)

        self.upper = upper
        self.lower = lower
        self.body = full_shape
        self.add(full_shape)


class FlowingAir(VGroup):
    """Animated air particles flowing over/under an airfoil."""

    def __init__(
        self,
        center=ORIGIN,
        n_top=6,
        n_bottom=4,
        spread=4.0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.flow_arrows_top = VGroup()
        self.flow_arrows_bot = VGroup()

        for i in range(n_top):
            x_offset = -spread / 2 + i * (spread / (n_top - 1))
            arrow = Arrow(
                start=center + UP * 0.6 + LEFT * 0.5 + RIGHT * x_offset,
                end=center + UP * 0.6 + RIGHT * 0.5 + RIGHT * x_offset,
                color=TEAL,
                stroke_width=2,
                buff=0,
                max_tip_length_to_length_ratio=0.2,
            )
            self.flow_arrows_top.add(arrow)

        for i in range(n_bottom):
            x_offset = -spread / 2 + i * (spread / max(n_bottom - 1, 1))
            arrow = Arrow(
                start=center + DOWN * 0.5 + LEFT * 0.3 + RIGHT * x_offset,
                end=center + DOWN * 0.5 + RIGHT * 0.3 + RIGHT * x_offset,
                color=MUTED,
                stroke_width=1.5,
                buff=0,
                max_tip_length_to_length_ratio=0.2,
            )
            self.flow_arrows_bot.add(arrow)

        self.add(self.flow_arrows_top, self.flow_arrows_bot)


class SubtitleBar(VGroup):
    """Persistent subtitle bar at the bottom of the screen."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bar = Rectangle(
            width=16,
            height=1.2,
            fill_color=DARK_BAR,
            fill_opacity=0.85,
            stroke_width=0,
        ).move_to(DOWN * 3.85)
        self.text = Text("", font_size=22, color=SOFT_WHT)
        self.text.move_to(self.bar.get_center())
        self.add(self.bar, self.text)

    def update_text(self, scene, new_text, max_width=13.5):
        """Return animations to update subtitle text."""
        new_txt = Text(new_text, font_size=22, color=SOFT_WHT)
        if new_txt.width > max_width:
            new_txt.scale(max_width / new_txt.width)
        new_txt.move_to(self.bar.get_center())
        old_text = self.text
        self.text = new_txt
        self.remove(old_text)
        self.add(new_txt)
        return [FadeOut(old_text, run_time=0.15), FadeIn(new_txt, run_time=0.2)]


# -- Section Title Helper ----------------------------------------------------
class SectionTitle(VGroup):
    """Styled section title with optional subtitle."""

    def __init__(self, title_text, subtitle_text=None, color=GOLD, **kwargs):
        super().__init__(**kwargs)
        self.title = Text(title_text, font_size=40, color=color, weight=BOLD)
        self.title.to_edge(UP, buff=0.5)
        self.add(self.title)

        if subtitle_text:
            self.subtitle = Text(subtitle_text, font_size=22, color=MUTED, slant=ITALIC)
            self.subtitle.next_to(self.title, DOWN, buff=0.2)
            self.add(self.subtitle)


# -- Main Scene ---------------------------------------------------------------
class WhyAirplanesFlyV3(VoiceoverScene, MovingCameraScene):
    """Professional educational video: Why Airplanes Don't Fall."""

    def setup(self):
        VoiceoverScene.setup(self)
        MovingCameraScene.setup(self)
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        self.camera.frame.set(width=16, height=9)

        # Persistent elements
        self.bg = BackgroundGradient()
        self.subtitle_bar = SubtitleBar()

    def construct(self):
        # Add persistent background and subtitle bar
        self.add(self.bg)
        self.add(self.subtitle_bar)

        self.section_hook()
        self.section_wrong_answer()
        self.section_hand_analogy()
        self.section_newton()
        self.section_bernoulli()
        self.section_real_answer()
        self.section_myth_bust()
        self.section_outro()

    def show_subtitle(self, text):
        """Update the subtitle bar with new text."""
        anims = self.subtitle_bar.update_text(self, text)
        self.play(*anims)

    def clear_scene(self, *keep):
        """Fade out everything except background, subtitle bar, and specified."""
        to_remove = []
        for mob in self.mobjects:
            if mob is self.bg or mob is self.subtitle_bar:
                continue
            if mob in keep:
                continue
            to_remove.append(mob)
        if to_remove:
            self.play(
                *[FadeOut(m) for m in to_remove],
                run_time=0.4,
            )

    # == HOOK SECTION =========================================================
    def section_hook(self):
        with self.voiceover(
            text="A Boeing 747 weighs four hundred tons. That is the weight of eighty elephants."
        ):
            self.show_subtitle("A Boeing 747 weighs 400 tons - the weight of 80 elephants.")

            # Section title
            sec_title = SectionTitle("THE QUESTION", "Why don't airplanes fall?")
            self.play(GrowFromCenter(sec_title.title), run_time=0.6)
            if hasattr(sec_title, "subtitle"):
                self.play(FadeIn(sec_title.subtitle, shift=UP * 0.1), run_time=0.3)

            # Big number counter animation
            tons_num = Text("400", font_size=96, color=GOLD, weight=BOLD)
            tons_label = Text("TONS", font_size=44, color=SOFT_WHT, weight=BOLD)
            tons_label.next_to(tons_num, RIGHT, buff=0.3)
            tons_grp = VGroup(tons_num, tons_label).move_to(UP * 0.3)

            self.play(FadeIn(tons_grp, scale=1.8), run_time=0.8)

            # Elephants line
            elephants = Text("= 80 elephants", font_size=32, color=MUTED, slant=ITALIC)
            elephants.next_to(tons_grp, DOWN, buff=0.5)
            self.play(Write(elephants), run_time=0.5)

        with self.voiceover(text="And somehow, it flies."):
            self.show_subtitle("And somehow... it flies.")
            flies_txt = Text(
                "And somehow... it flies.",
                font_size=34,
                color=TEAL,
                weight=BOLD,
            )
            flies_txt.next_to(elephants, DOWN, buff=0.5)
            self.play(
                LaggedStart(
                    FadeIn(flies_txt, shift=LEFT * 0.3),
                    Indicate(flies_txt, color=GOLD, scale_factor=1.05),
                    lag_ratio=0.5,
                ),
                run_time=1.0,
            )

        with self.voiceover(
            text="Right now, ten thousand planes are above you. "
            "Not a single one should be there. What keeps them up?"
        ):
            self.show_subtitle("10,000 planes are above you right now. What keeps them up?")
            self.play(
                FadeOut(sec_title, tons_grp, elephants, flies_txt),
                run_time=0.4,
            )

            # Counter for planes
            planes_num = Text("10,000", font_size=80, color=CORAL, weight=BOLD)
            planes_label = Text("PLANES IN THE SKY", font_size=28, color=SOFT_WHT)
            planes_label.next_to(planes_num, DOWN, buff=0.3)
            planes_grp = VGroup(planes_num, planes_label).move_to(UP * 0.5)

            self.play(GrowFromCenter(planes_grp), run_time=0.6)
            self.play(Indicate(planes_num, scale_factor=1.1, color=GOLD), run_time=0.5)

            # Question
            question = Text(
                "What keeps them up?",
                font_size=48,
                color=GOLD,
                weight=BOLD,
            )
            question.next_to(planes_grp, DOWN, buff=0.8)
            self.play(Write(question), run_time=0.6)
            self.play(
                Circumscribe(question, color=GOLD, buff=0.15),
                run_time=0.8,
            )

        self.clear_scene()

    # == WRONG ANSWER SECTION =================================================
    def section_wrong_answer(self):
        with self.voiceover(
            text="You probably learned this in school. The wing is curved on top, "
            "so air travels a longer path, moves faster, and creates low pressure. "
            "The plane gets sucked upward."
        ):
            self.show_subtitle("The textbook explanation: curved top = longer path = low pressure")

            sec_title = SectionTitle("THE TEXTBOOK MYTH", "What school taught you", color=CORAL)
            self.play(
                LaggedStart(
                    FadeIn(sec_title.title, shift=DOWN * 0.2),
                    FadeIn(sec_title.subtitle, shift=DOWN * 0.1),
                    lag_ratio=0.3,
                ),
                run_time=0.7,
            )

            # Airfoil
            wing = Airfoil(width=5.5, thickness=0.9)
            wing.move_to(DOWN * 0.3)
            self.play(Create(wing.body), run_time=0.8)

            # Curved path on top (arc)
            top_arc = ArcBetweenPoints(
                LEFT * 2.5 + UP * 0.7,
                RIGHT * 2.5 + UP * 0.2,
                angle=-0.4,
                color=TEAL,
                stroke_width=2,
            )
            top_label = Text("Longer path?", font_size=18, color=TEAL, slant=ITALIC)
            top_label.next_to(top_arc, UP, buff=0.15)

            # Straight path on bottom
            bot_line = Line(
                LEFT * 2.5 + DOWN * 0.8,
                RIGHT * 2.5 + DOWN * 0.7,
                color=MUTED,
                stroke_width=2,
            )
            bot_label = Text("Shorter path", font_size=18, color=MUTED, slant=ITALIC)
            bot_label.next_to(bot_line, DOWN, buff=0.15)

            self.play(
                Create(top_arc),
                Create(bot_line),
                run_time=0.7,
            )
            self.play(
                FadeIn(top_label, shift=DOWN * 0.1),
                FadeIn(bot_label, shift=UP * 0.1),
                run_time=0.4,
            )

        with self.voiceover(
            text="Sounds clean. But there is a fatal problem. "
            "If that were the whole story, planes could never fly upside down. "
            "But they can."
        ):
            self.show_subtitle("Problem: If true, planes could never fly upside down!")

            # INCOMPLETE stamp
            stamp = Text("INCOMPLETE!", font_size=56, color=CORAL, weight=BOLD)
            stamp.rotate(PI / 14)
            stamp.move_to(wing.get_center())
            self.play(FadeIn(stamp, scale=2.5), run_time=0.4)
            self.play(Indicate(stamp, scale_factor=1.1, color=GOLD), run_time=0.6)

        self.clear_scene()

    # == HAND ANALOGY SECTION =================================================
    def section_hand_analogy(self):
        with self.voiceover(
            text="Let us start with something you have done a hundred times. "
            "Put your hand out a car window."
        ):
            self.show_subtitle("The car window test - something you already know")

            sec_title = SectionTitle(
                "THE CAR WINDOW TEST", "Intuition before equations", color=TEAL
            )
            self.play(DrawBorderThenFill(sec_title.title), run_time=0.6)
            self.play(FadeIn(sec_title.subtitle, shift=UP * 0.1), run_time=0.3)

            # Hand shape
            hand = RoundedRectangle(
                width=3.0,
                height=0.3,
                corner_radius=0.08,
                color=SOFT_WHT,
                fill_color=SOFT_WHT,
                fill_opacity=0.7,
                stroke_width=2,
            ).move_to(DOWN * 0.2)
            self.play(GrowFromCenter(hand), run_time=0.5)

            # Wind streaks
            wind_lines = VGroup(
                *[
                    Line(
                        LEFT * 5.5 + UP * (i * 0.3 - 0.6),
                        LEFT * 3.5 + UP * (i * 0.3 - 0.6),
                        color=MUTED,
                        stroke_width=1.5,
                        stroke_opacity=0.6,
                    )
                    for i in range(5)
                ]
            )
            self.play(
                LaggedStart(*[Create(ln) for ln in wind_lines], lag_ratio=0.08),
                run_time=0.6,
            )

        with self.voiceover(text="Keep it flat and nothing happens. Now tilt it up slightly."):
            self.show_subtitle("Flat = nothing. Tilt up = something pushes!")
            self.play(Rotate(hand, angle=PI / 10), run_time=0.8)

        with self.voiceover(
            text="Feel that push? That force shoving your hand upward? "
            "That IS lift. The exact same physics keeping a plane in the air."
        ):
            self.show_subtitle("That upward push IS lift - same physics as flight!")

            # Deflected air arrows going down
            deflect_arrows = VGroup(
                *[
                    Arrow(
                        hand.get_center() + RIGHT * (i - 1.5) * 0.7 + DOWN * 0.2,
                        hand.get_center() + RIGHT * (i - 1.5) * 0.7 + DOWN * 1.5,
                        color=MUTED,
                        stroke_width=2,
                        buff=0,
                        max_tip_length_to_length_ratio=0.2,
                    )
                    for i in range(4)
                ]
            )
            self.play(
                LaggedStart(*[Create(a) for a in deflect_arrows], lag_ratio=0.1),
                run_time=0.6,
            )

            # Lift arrow
            lift_arrow = Arrow(
                hand.get_center() + DOWN * 0.2,
                hand.get_center() + UP * 2.0,
                color=TEAL,
                stroke_width=5,
                buff=0,
                max_tip_length_to_length_ratio=0.1,
            )
            lift_label = Text("LIFT", font_size=30, color=TEAL, weight=BOLD)
            lift_label.next_to(lift_arrow, RIGHT, buff=0.15)
            self.play(Create(lift_arrow), run_time=0.6)
            self.play(FadeIn(lift_label, shift=LEFT * 0.1), run_time=0.3)
            self.play(
                Indicate(lift_label, scale_factor=1.2, color=GOLD),
                run_time=0.5,
            )

        with self.voiceover(text="A wing is just a more refined version of your tilted hand."):
            self.show_subtitle("A wing = a refined version of your tilted hand")
            new_wing = Airfoil(width=4.5, thickness=0.7)
            new_wing.move_to(hand.get_center())
            self.play(
                ReplacementTransform(hand, new_wing.body),
                FadeOut(wind_lines, deflect_arrows, lift_arrow, lift_label),
                run_time=1.0,
            )

        self.clear_scene()

    # == NEWTON SECTION =======================================================
    def section_newton(self):
        with self.voiceover(
            text="Newton's third law. Every action has an equal and opposite reaction."
        ):
            self.show_subtitle("Newton's Third Law: action and reaction")

            sec_title = SectionTitle(
                "NEWTON'S THIRD LAW",
                "Action and Reaction",
                color=PURPLE,
            )
            self.play(Write(sec_title.title), run_time=0.5)
            self.play(FadeIn(sec_title.subtitle, shift=UP * 0.1), run_time=0.3)

            # Wing
            wing = Airfoil(width=5.0, thickness=0.8)
            wing.move_to(DOWN * 0.2)
            self.play(DrawBorderThenFill(wing.body), run_time=0.7)

        with self.voiceover(
            text="The wing pushes air downward. Air pushes the wing upward. "
            "That upward push is lift."
        ):
            self.show_subtitle("Wing pushes air DOWN -> Air pushes wing UP = LIFT")

            # Action arrows (air pushed down)
            down_arrows = VGroup(
                *[
                    Arrow(
                        wing.get_center() + RIGHT * (i - 1.5) * 1.0,
                        wing.get_center() + DOWN * 1.8 + RIGHT * (i - 1.5) * 1.0,
                        color=CORAL,
                        stroke_width=3,
                        buff=0.15,
                        max_tip_length_to_length_ratio=0.15,
                    )
                    for i in range(4)
                ]
            )
            action_label = Text(
                "Air pushed DOWN (action)",
                font_size=20,
                color=CORAL,
                slant=ITALIC,
            )
            action_label.next_to(down_arrows, DOWN, buff=0.15)

            self.play(
                LaggedStart(*[Create(a) for a in down_arrows], lag_ratio=0.1),
                run_time=0.7,
            )
            self.play(FadeIn(action_label), run_time=0.3)

            # Reaction arrow (lift up)
            up_arrow = Arrow(
                wing.get_center() + UP * 0.3,
                wing.get_center() + UP * 2.5,
                color=TEAL,
                stroke_width=6,
                buff=0,
                max_tip_length_to_length_ratio=0.1,
            )
            react_label = Text("LIFT (reaction)", font_size=26, color=TEAL, weight=BOLD)
            react_label.next_to(up_arrow, RIGHT, buff=0.15)

            self.play(Create(up_arrow), run_time=0.5)
            self.play(GrowFromCenter(react_label), run_time=0.4)
            self.play(
                Circumscribe(react_label, color=TEAL, buff=0.1),
                run_time=0.6,
            )

        with self.voiceover(text="Simple. Powerful. But only half the story."):
            self.show_subtitle("Simple, powerful... but only HALF the story.")
            half_txt = Text(
                "Only HALF the story...",
                font_size=30,
                color=GOLD,
                weight=BOLD,
            )
            half_txt.to_edge(DOWN, buff=1.5)
            self.play(FadeIn(half_txt, shift=UP * 0.2), run_time=0.5)
            self.play(
                Indicate(half_txt, scale_factor=1.08, color=CORAL),
                run_time=0.5,
            )

        self.clear_scene()

    # == BERNOULLI SECTION ====================================================
    def section_bernoulli(self):
        with self.voiceover(
            text="Here is the other half. Bernoulli's principle. Faster air means lower pressure."
        ):
            self.show_subtitle("Bernoulli's Principle: faster air = lower pressure")

            sec_title = SectionTitle(
                "BERNOULLI'S PRINCIPLE",
                "Pressure and velocity",
                color=GREEN,
            )
            self.play(
                LaggedStart(
                    GrowFromCenter(sec_title.title),
                    FadeIn(sec_title.subtitle, shift=DOWN * 0.1),
                    lag_ratio=0.4,
                ),
                run_time=0.8,
            )

            # Wing with airflow
            wing = Airfoil(width=5.5, thickness=0.9)
            wing.move_to(DOWN * 0.3)
            self.play(Create(wing.body), run_time=0.6)

        with self.voiceover(
            text="Air moves faster over the curved top. "
            "Faster flow means lower pressure above. "
            "Higher pressure below pushes up."
        ):
            self.show_subtitle("Fast air on top = low pressure. Slow air below = high pressure.")

            # Flowing air visualization
            flow = FlowingAir(center=wing.get_center())
            self.play(
                LaggedStart(
                    *[Create(a) for a in flow.flow_arrows_top],
                    lag_ratio=0.08,
                ),
                run_time=0.6,
            )
            self.play(
                LaggedStart(
                    *[Create(a) for a in flow.flow_arrows_bot],
                    lag_ratio=0.1,
                ),
                run_time=0.5,
            )

            # Pressure labels
            low_p = Text("LOW pressure", font_size=22, color=TEAL, weight=BOLD)
            low_p.next_to(wing.body, UP, buff=0.8)
            high_p = Text("HIGH pressure", font_size=22, color=CORAL, weight=BOLD)
            high_p.next_to(wing.body, DOWN, buff=0.8)

            speed_top = Text("(fast)", font_size=16, color=TEAL, slant=ITALIC)
            speed_top.next_to(low_p, RIGHT, buff=0.2)
            speed_bot = Text("(slow)", font_size=16, color=CORAL, slant=ITALIC)
            speed_bot.next_to(high_p, RIGHT, buff=0.2)

            self.play(
                FadeIn(low_p, shift=DOWN * 0.2),
                FadeIn(speed_top, shift=DOWN * 0.2),
                run_time=0.4,
            )
            self.play(
                FadeIn(high_p, shift=UP * 0.2),
                FadeIn(speed_bot, shift=UP * 0.2),
                run_time=0.4,
            )

        with self.voiceover(
            text="This pressure difference adds an upward force. "
            "Combined with Newton, that gives you total lift."
        ):
            self.show_subtitle("Pressure difference + Newton's reaction = TOTAL LIFT")

            # Combined big lift arrow
            big_lift = Arrow(
                DOWN * 1.8 + RIGHT * 5,
                UP * 1.8 + RIGHT * 5,
                color=GOLD,
                stroke_width=7,
                buff=0,
                max_tip_length_to_length_ratio=0.08,
            )
            big_label = Text(
                "TOTAL\nLIFT",
                font_size=22,
                color=GOLD,
                weight=BOLD,
            )
            big_label.next_to(big_lift, RIGHT, buff=0.2)
            self.play(Create(big_lift), run_time=0.6)
            self.play(FadeIn(big_label, shift=LEFT * 0.1), run_time=0.3)

        self.clear_scene()

    # == THE REAL ANSWER SECTION ==============================================
    def section_real_answer(self):
        with self.voiceover(
            text="So the real answer? It is not Newton OR Bernoulli. It is both. Working together."
        ):
            self.show_subtitle("The real answer: Newton AND Bernoulli, working together.")

            sec_title = SectionTitle("THE REAL ANSWER", color=GOLD)
            self.play(Write(sec_title.title), run_time=0.5)

            # BOTH text - big impact
            both_txt = Text("BOTH.", font_size=72, color=GOLD, weight=BOLD)
            both_txt.move_to(UP * 0.2)
            self.play(FadeIn(both_txt, scale=2.0), run_time=0.5)
            self.play(
                Indicate(both_txt, scale_factor=1.08, color=TEAL),
                run_time=0.5,
            )

            # Equation-style subtitle
            equation = Text(
                "Newton + Bernoulli = Complete Explanation",
                font_size=26,
                color=SOFT_WHT,
            )
            equation.next_to(both_txt, DOWN, buff=0.6)
            self.play(Write(equation), run_time=0.7)

            # Visual: two boxes combining
            newton_box = RoundedRectangle(
                width=3,
                height=1.2,
                corner_radius=0.1,
                color=PURPLE,
                fill_color=PURPLE,
                fill_opacity=0.15,
                stroke_width=2,
            ).move_to(LEFT * 3.5 + DOWN * 1.8)
            newton_lbl = Text("Newton", font_size=20, color=PURPLE, weight=BOLD)
            newton_lbl.move_to(newton_box)

            bernoulli_box = RoundedRectangle(
                width=3,
                height=1.2,
                corner_radius=0.1,
                color=GREEN,
                fill_color=GREEN,
                fill_opacity=0.15,
                stroke_width=2,
            ).move_to(RIGHT * 3.5 + DOWN * 1.8)
            bernoulli_lbl = Text("Bernoulli", font_size=20, color=GREEN, weight=BOLD)
            bernoulli_lbl.move_to(bernoulli_box)

            self.play(
                FadeIn(newton_box, shift=RIGHT * 0.3),
                FadeIn(newton_lbl, shift=RIGHT * 0.3),
                FadeIn(bernoulli_box, shift=LEFT * 0.3),
                FadeIn(bernoulli_lbl, shift=LEFT * 0.3),
                run_time=0.6,
            )

            # Plus sign between
            plus = Text("+", font_size=36, color=GOLD, weight=BOLD)
            plus.move_to(DOWN * 1.8)
            self.play(GrowFromCenter(plus), run_time=0.3)

            # Merge into one
            combined_box = RoundedRectangle(
                width=6,
                height=1.2,
                corner_radius=0.1,
                color=GOLD,
                fill_color=GOLD,
                fill_opacity=0.15,
                stroke_width=2.5,
            ).move_to(DOWN * 1.8)
            combined_lbl = Text("FULL LIFT", font_size=24, color=GOLD, weight=BOLD)
            combined_lbl.move_to(combined_box)

            self.play(
                Transform(newton_box, combined_box),
                Transform(bernoulli_box, combined_box.copy()),
                Transform(newton_lbl, combined_lbl),
                Transform(bernoulli_lbl, combined_lbl.copy()),
                FadeOut(plus),
                run_time=1.0,
            )

        self.clear_scene()

    # == MYTH BUST SECTION ====================================================
    def section_myth_bust(self):
        with self.voiceover(
            text="But here is the myth you need to unlearn. "
            "The textbook says air on top must arrive at the trailing edge "
            "at the same time as air on the bottom. "
            "The equal transit time theory."
        ):
            self.show_subtitle("MYTH: Air on top arrives at same time as air on bottom")

            sec_title = SectionTitle(
                "MYTH BUSTED",
                "Equal Transit Time is WRONG",
                color=CORAL,
            )
            self.play(
                LaggedStart(
                    DrawBorderThenFill(sec_title.title),
                    FadeIn(sec_title.subtitle, shift=UP * 0.1),
                    lag_ratio=0.3,
                ),
                run_time=0.7,
            )

            # Quote box with the myth
            myth_quote = Text(
                '"Air on top must arrive at the same\ntime as air on the bottom."',
                font_size=24,
                color=MUTED,
                slant=ITALIC,
            )
            myth_quote.move_to(DOWN * 0.3)
            quote_box = SurroundingRectangle(
                myth_quote,
                color=MUTED,
                buff=0.3,
                stroke_width=1.5,
                corner_radius=0.1,
            )
            self.play(Write(myth_quote), Create(quote_box), run_time=0.8)

        with self.voiceover(
            text="No physical law requires this. Wind tunnel experiments show "
            "air on top actually arrives FIRST. "
            "Equal transit time is simply wrong."
        ):
            self.show_subtitle("FACT: Air on top arrives FIRST. No law requires equal time.")

            # Cross it out
            cross_l1 = Line(
                quote_box.get_corner(UL), quote_box.get_corner(DR),
                color=CORAL, stroke_width=5,
            )
            cross_l2 = Line(
                quote_box.get_corner(DL), quote_box.get_corner(UR),
                color=CORAL, stroke_width=5,
            )
            self.play(Create(cross_l1), Create(cross_l2), run_time=0.5)

            wrong_stamp = Text("WRONG", font_size=52, color=CORAL, weight=BOLD)
            wrong_stamp.next_to(myth_quote, DOWN, buff=0.7)
            self.play(FadeIn(wrong_stamp, scale=1.8), run_time=0.4)
            self.play(
                Circumscribe(wrong_stamp, color=CORAL, buff=0.1),
                run_time=0.6,
            )

        with self.voiceover(
            text="The secret variable that pilots actually control is the "
            "angle of attack. Tilt the wing more, get more lift. "
            "Up to a point."
        ):
            self.show_subtitle("Angle of Attack: the variable pilots actually control")

            self.play(
                FadeOut(
                    sec_title,
                    myth_quote,
                    quote_box,
                    cross_l1,
                    cross_l2,
                    wrong_stamp,
                ),
                run_time=0.3,
            )

            # Angle of attack demo
            aoa_title = Text(
                "ANGLE OF ATTACK",
                font_size=32,
                color=TEAL,
                weight=BOLD,
            )
            aoa_title.to_edge(UP, buff=0.6)
            self.play(FadeIn(aoa_title, shift=DOWN * 0.2), run_time=0.4)

            # Wing bar that tilts
            wing_bar = RoundedRectangle(
                width=4.5,
                height=0.22,
                corner_radius=0.06,
                color=SOFT_WHT,
                fill_color=SOFT_WHT,
                fill_opacity=0.65,
                stroke_width=2,
            )
            # Horizontal reference
            ref_line = DashedLine(LEFT * 3, RIGHT * 3, color=MUTED, stroke_width=1)
            self.play(FadeIn(wing_bar), Create(ref_line), run_time=0.4)

            # Tilt it
            self.play(Rotate(wing_bar, angle=PI / 10), run_time=0.8)

            # Angle arc
            angle_arc = Arc(
                radius=1.8,
                start_angle=0,
                angle=PI / 10,
                color=GOLD,
                stroke_width=2.5,
            )
            angle_label = Text(
                "Angle of Attack",
                font_size=20,
                color=GOLD,
                slant=ITALIC,
            )
            angle_label.next_to(angle_arc, RIGHT, buff=0.2)
            self.play(
                Create(angle_arc),
                FadeIn(angle_label),
                run_time=0.5,
            )

            # More lift annotation
            more_lift = Text(
                "More angle = more lift (to a point)",
                font_size=22,
                color=SOFT_WHT,
            )
            more_lift.to_edge(DOWN, buff=1.5)
            self.play(Write(more_lift), run_time=0.5)

            # Tilt further
            self.play(Rotate(wing_bar, angle=PI / 16), run_time=0.6)
            self.play(
                Indicate(more_lift, scale_factor=1.05, color=GOLD),
                run_time=0.4,
            )

        self.clear_scene()

    # == OUTRO SECTION ========================================================
    def section_outro(self):
        with self.voiceover(text="So next time you are on a plane and hit turbulence, remember:"):
            self.show_subtitle("Next time you fly, remember this...")

            sec_title = SectionTitle("RECAP", "Everything you need to know", color=TEAL)
            self.play(GrowFromCenter(sec_title.title), run_time=0.5)
            self.play(FadeIn(sec_title.subtitle, shift=UP * 0.1), run_time=0.3)

        with self.voiceover(
            text="Four hundred tons of metal is held up by the same physics "
            "that pushes your hand up out a car window. "
            "Newton and Bernoulli, working together."
        ):
            self.show_subtitle("400 tons held up by the same physics as your hand in the wind")

            self.play(FadeOut(sec_title), run_time=0.3)

            # Recap bullet points with typography hierarchy
            bullet_1 = Text(
                "Newton's 3rd Law",
                font_size=26,
                color=PURPLE,
                weight=BOLD,
            )
            bullet_1_desc = Text(
                "action / reaction",
                font_size=18,
                color=MUTED,
                slant=ITALIC,
            )
            bullet_1_desc.next_to(bullet_1, RIGHT, buff=0.3)
            row_1 = VGroup(bullet_1, bullet_1_desc)

            bullet_2 = Text(
                "Bernoulli's Principle",
                font_size=26,
                color=GREEN,
                weight=BOLD,
            )
            bullet_2_desc = Text(
                "pressure difference",
                font_size=18,
                color=MUTED,
                slant=ITALIC,
            )
            bullet_2_desc.next_to(bullet_2, RIGHT, buff=0.3)
            row_2 = VGroup(bullet_2, bullet_2_desc)

            bullet_3 = Text(
                "Angle of Attack",
                font_size=26,
                color=GOLD,
                weight=BOLD,
            )
            bullet_3_desc = Text(
                "the pilot's control",
                font_size=18,
                color=MUTED,
                slant=ITALIC,
            )
            bullet_3_desc.next_to(bullet_3, RIGHT, buff=0.3)
            row_3 = VGroup(bullet_3, bullet_3_desc)

            points = VGroup(row_1, row_2, row_3).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            points.move_to(UP * 0.3)

            self.play(
                LaggedStart(
                    FadeIn(row_1, shift=RIGHT * 0.3),
                    FadeIn(row_2, shift=RIGHT * 0.3),
                    FadeIn(row_3, shift=RIGHT * 0.3),
                    lag_ratio=0.3,
                ),
                run_time=1.2,
            )
            self.play(
                Circumscribe(points, color=GOLD, buff=0.3, stroke_width=2),
                run_time=0.8,
            )

        with self.voiceover(
            text="If this made flight click for you, subscribe. "
            "We break down one impossible sounding question every week."
        ):
            self.show_subtitle("Subscribe - one impossible question every week!")

            self.play(FadeOut(points), run_time=0.3)

            # Subscribe CTA box
            sub_box = RoundedRectangle(
                width=7,
                height=1.8,
                corner_radius=0.2,
                color=CORAL,
                fill_color="#1A0A10",
                fill_opacity=0.9,
                stroke_width=2.5,
            )
            sub_text = Text(
                "SUBSCRIBE",
                font_size=48,
                color=CORAL,
                weight=BOLD,
            )
            sub_text.move_to(sub_box.get_center() + UP * 0.2)
            sub_desc = Text(
                "One impossible question. Every week.",
                font_size=20,
                color=MUTED,
                slant=ITALIC,
            )
            sub_desc.next_to(sub_text, DOWN, buff=0.25)

            self.play(
                FadeIn(sub_box, scale=0.9),
                Write(sub_text),
                run_time=0.6,
            )
            self.play(FadeIn(sub_desc, shift=UP * 0.1), run_time=0.3)
            self.play(
                Indicate(sub_box, scale_factor=1.04, color=GOLD),
                run_time=0.7,
            )

        # Final fade
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.5)
