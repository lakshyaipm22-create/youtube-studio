"""
Why Airplanes Don't Fall — V2 (manim-voiceover)

Single-file video: narration + animation perfectly synced.
Render: manim render -qh airplane_v2.py WhyAirplanesFly

Uses manim-voiceover for automatic voice-animation synchronization.
Each `with self.voiceover()` block holds until narration finishes.
"""

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

# ── Palette ──────────────────────────────────────────────────────────────────
BG = "#1A1A2E"
PRIMARY = "#6C63FF"
ACCENT = "#00D9A6"
CORAL = "#FF6584"
LIGHT = "#F5F5F5"
MUTED = "#8892B0"
WARNING_CLR = "#FFB347"
ERROR_CLR = "#FF4444"

config.background_color = BG
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


# ── Custom Mobjects ──────────────────────────────────────────────────────────
class Wing(VGroup):
    """Airfoil cross-section with labeled parts."""

    def __init__(self, width=5.0, height=1.0, color=LIGHT, **kwargs):
        super().__init__(**kwargs)
        # Asymmetric ellipse representing airfoil
        airfoil = Ellipse(width=width, height=height, color=color, stroke_width=2)
        airfoil.set_fill(BG, opacity=0.5)
        # Flatten the bottom slightly by stretching
        airfoil.stretch(0.6, 1, about_point=airfoil.get_bottom())
        self.airfoil = airfoil
        self.add(airfoil)


class AirflowArrows(VGroup):
    """Animated airflow arrows over/under a wing."""

    def __init__(self, wing_center, color_top=PRIMARY, color_bot=MUTED, **kwargs):
        super().__init__(**kwargs)
        # Top arrows (faster, longer)
        for i in range(4):
            x = -2.0 + i * 1.2
            arr = Arrow(
                start=wing_center + UP * 0.8 + LEFT * 0.6 + RIGHT * x,
                end=wing_center + UP * 0.8 + RIGHT * 0.6 + RIGHT * x,
                color=color_top,
                stroke_width=2,
                buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
            self.add(arr)
        # Bottom arrows (slower, shorter)
        for i in range(3):
            x = -1.5 + i * 1.2
            arr = Arrow(
                start=wing_center + DOWN * 0.6 + LEFT * 0.4 + RIGHT * x,
                end=wing_center + DOWN * 0.6 + RIGHT * 0.4 + RIGHT * x,
                color=color_bot,
                stroke_width=2,
                buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
            self.add(arr)


# ── Main Scene ───────────────────────────────────────────────────────────────
class WhyAirplanesFly(VoiceoverScene, MovingCameraScene):
    """Complete educational video: Why Airplanes Don't Fall."""

    def setup(self):
        VoiceoverScene.setup(self)
        MovingCameraScene.setup(self)
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        self.camera.frame.set(width=16, height=9)

    def construct(self):
        self.hook()
        self.wrong_answer()
        self.hand_analogy()
        self.newton_explains()
        self.bernoulli_adds()
        self.the_real_answer()
        self.myth_bust()
        self.outro()

    # ── HOOK ─────────────────────────────────────────────────────────────────
    def hook(self):
        with self.voiceover(text="A Boeing 747 weighs four hundred tons. That's eighty elephants."):
            # Big number reveal
            tons = Text("400", font_size=96, color=PRIMARY, weight=BOLD)
            tons_label = Text("TONS", font_size=48, color=LIGHT)
            tons_label.next_to(tons, RIGHT, buff=0.3)
            tons_grp = VGroup(tons, tons_label).move_to(UP * 0.5)

            self.play(FadeIn(tons, scale=1.5), run_time=0.8)
            self.play(FadeIn(tons_label, shift=RIGHT * 0.3), run_time=0.4)

            # Elephants
            elephants = Text("= 80 🐘", font_size=36, color=MUTED)
            elephants.next_to(tons_grp, DOWN, buff=0.5)
            self.play(FadeIn(elephants, shift=UP * 0.2), run_time=0.5)

        with self.voiceover(text="And somehow, it flies."):
            flies = Text("And somehow... it flies.", font_size=32, color=ACCENT)
            flies.next_to(elephants, DOWN, buff=0.6)
            self.play(Write(flies), run_time=0.8)

        with self.voiceover(
            text="Right now there are ten thousand planes above you. "
            "Not a single one of them should be there. So what is keeping them up?"
        ):
            self.play(FadeOut(tons_grp, elephants, flies), run_time=0.4)
            how = Text("What keeps them up?", font_size=52, color=PRIMARY, weight=BOLD)
            self.play(FadeIn(how, scale=1.2), run_time=0.6)
            self.play(Indicate(how, scale_factor=1.05, color=ACCENT), run_time=0.5)

        self.play(FadeOut(how), run_time=0.4)

    # ── WRONG ANSWER ─────────────────────────────────────────────────────────
    def wrong_answer(self):
        with self.voiceover(
            text="You probably learned this in school. The wing is curved on top, "
            "so air travels a longer path, moves faster, and creates low pressure. "
            "The plane gets sucked upward."
        ):
            title = Text("What Your Textbook Said", font_size=36, color=MUTED)
            title.to_edge(UP, buff=0.6)
            self.play(Write(title), run_time=0.5)

            # Wing
            wing = Wing(width=5, height=1.2)
            wing.move_to(ORIGIN)
            self.play(Create(wing.airfoil), run_time=0.8)

            # Curved path on top
            top_arc = ArcBetweenPoints(
                LEFT * 2.5 + UP * 0.9,
                RIGHT * 2.5 + UP * 0.4,
                angle=-0.5,
                color=PRIMARY,
            )
            self.play(Create(top_arc), run_time=0.8)

            # Straight path on bottom
            bot_line = Line(LEFT * 2.5 + DOWN * 0.4, RIGHT * 2.5 + DOWN * 0.2, color=MUTED)
            self.play(Create(bot_line), run_time=0.5)

            # "Longer path" label
            longer = Text("Longer path = faster?", font_size=20, color=MUTED)
            longer.next_to(top_arc, UP, buff=0.2)
            self.play(FadeIn(longer), run_time=0.3)

        with self.voiceover(
            text="Sounds clean. But there's a problem. If that were the whole story, "
            "planes could never fly upside down. But they can."
        ):
            # WRONG stamp
            wrong = Text("INCOMPLETE", font_size=56, color=ERROR_CLR, weight=BOLD)
            wrong.rotate(PI / 15)
            self.play(FadeIn(wrong, scale=2.0), run_time=0.4)
            self.play(Indicate(wrong, scale_factor=1.1), run_time=0.5)

        self.play(FadeOut(*self.mobjects), run_time=0.4)

    # ── HAND ANALOGY ─────────────────────────────────────────────────────────
    def hand_analogy(self):
        with self.voiceover(
            text="Let's start with something you've done a hundred times. "
            "Put your hand out a car window."
        ):
            title = Text("The Car Window Test", font_size=36, color=ACCENT)
            title.to_edge(UP, buff=0.6)
            self.play(Write(title), run_time=0.5)

            # Hand (flat rectangle)
            hand = RoundedRectangle(
                width=2.5,
                height=0.25,
                corner_radius=0.05,
                color=LIGHT,
                fill_color=LIGHT,
                fill_opacity=0.7,
                stroke_width=2,
            )
            self.play(FadeIn(hand), run_time=0.4)

            # Wind streaks
            wind = VGroup(
                *[
                    Line(
                        LEFT * 4.5 + UP * (i * 0.35 - 0.7),
                        LEFT * 3.0 + UP * (i * 0.35 - 0.7),
                        color=MUTED,
                        stroke_width=1.5,
                        stroke_opacity=0.5,
                    )
                    for i in range(5)
                ]
            )
            self.play(
                LaggedStart(*[Create(line) for line in wind], lag_ratio=0.1),
                run_time=0.6,
            )

        with self.voiceover(text="Keep it flat — nothing happens. Now tilt it up slightly."):
            self.play(Rotate(hand, angle=PI / 12), run_time=0.8)

        with self.voiceover(
            text="Feel that push? That force shoving your hand upward? "
            "That IS lift. The exact same physics keeping a 747 in the air."
        ):
            # Deflection arrows going down
            deflect = VGroup(
                *[
                    Arrow(
                        hand.get_center() + RIGHT * (i - 1) * 0.8 + DOWN * 0.15,
                        hand.get_center() + RIGHT * (i - 1) * 0.8 + DOWN * 1.6,
                        color=MUTED,
                        stroke_width=2,
                        buff=0,
                        max_tip_length_to_length_ratio=0.2,
                    )
                    for i in range(4)
                ]
            )
            self.play(
                LaggedStart(*[Create(a) for a in deflect], lag_ratio=0.1),
                run_time=0.6,
            )

            # Lift arrow
            lift = Arrow(
                hand.get_center() + DOWN * 0.15,
                hand.get_center() + UP * 2.0,
                color=ACCENT,
                stroke_width=5,
                buff=0,
                max_tip_length_to_length_ratio=0.12,
            )
            lift_lbl = Text("LIFT", font_size=28, color=ACCENT, weight=BOLD)
            lift_lbl.next_to(lift, RIGHT, buff=0.15)
            self.play(Create(lift), run_time=0.6)
            self.play(FadeIn(lift_lbl, shift=LEFT * 0.1), run_time=0.3)

        with self.voiceover(text="A wing is just a fancy version of your tilted hand."):
            # Morph hand into airfoil
            new_wing = Wing(width=4, height=0.8).move_to(hand.get_center())
            self.play(
                ReplacementTransform(hand, new_wing.airfoil),
                FadeOut(wind, deflect, lift, lift_lbl),
                run_time=1.0,
            )

        self.play(FadeOut(*self.mobjects), run_time=0.4)

    # ── NEWTON ───────────────────────────────────────────────────────────────
    def newton_explains(self):
        with self.voiceover(
            text="Newton's third law. Every action has an equal and opposite reaction."
        ):
            title = Text("Newton's Third Law", font_size=36, color=PRIMARY, weight=BOLD)
            title.to_edge(UP, buff=0.6)
            self.play(Write(title), run_time=0.5)

            # Wing
            wing = Wing(width=4.5, height=0.8).move_to(ORIGIN)
            self.play(Create(wing.airfoil), run_time=0.6)

        with self.voiceover(
            text="The wing pushes air downward. Air pushes the wing upward. "
            "That upward push is lift."
        ):
            # Down arrows (action)
            down_arrows = VGroup(
                *[
                    Arrow(
                        ORIGIN + RIGHT * (i - 1.5) * 1.0,
                        ORIGIN + DOWN * 1.8 + RIGHT * (i - 1.5) * 1.0,
                        color=CORAL,
                        stroke_width=3,
                        buff=0.2,
                        max_tip_length_to_length_ratio=0.15,
                    )
                    for i in range(4)
                ]
            )
            action_lbl = Text("Air pushed DOWN", font_size=20, color=CORAL)
            action_lbl.next_to(down_arrows, DOWN, buff=0.15)

            self.play(
                LaggedStart(*[Create(a) for a in down_arrows], lag_ratio=0.1),
                run_time=0.8,
            )
            self.play(FadeIn(action_lbl), run_time=0.3)

            # Up arrow (reaction = lift)
            up_arrow = Arrow(
                ORIGIN + UP * 0.4,
                ORIGIN + UP * 2.5,
                color=ACCENT,
                stroke_width=6,
                buff=0,
                max_tip_length_to_length_ratio=0.1,
            )
            react_lbl = Text("LIFT", font_size=28, color=ACCENT, weight=BOLD)
            react_lbl.next_to(up_arrow, RIGHT, buff=0.15)
            self.play(Create(up_arrow), run_time=0.6)
            self.play(FadeIn(react_lbl), run_time=0.3)
            self.play(Indicate(react_lbl, scale_factor=1.2, color=ACCENT), run_time=0.5)

        with self.voiceover(text="Simple. Brutal. But only half the story."):
            half = Text("Only HALF the story...", font_size=28, color=WARNING_CLR)
            half.to_edge(DOWN, buff=0.6)
            self.play(FadeIn(half, shift=UP * 0.2), run_time=0.5)

        self.play(FadeOut(*self.mobjects), run_time=0.4)

    # ── BERNOULLI ────────────────────────────────────────────────────────────
    def bernoulli_adds(self):
        with self.voiceover(
            text="Here's the other half. Bernoulli's principle. Faster air creates lower pressure."
        ):
            title = Text("Bernoulli's Principle", font_size=36, color=PRIMARY, weight=BOLD)
            title.to_edge(UP, buff=0.6)
            self.play(Write(title), run_time=0.5)

            # Wing
            wing = Wing(width=5, height=1.0).move_to(ORIGIN)
            self.play(Create(wing.airfoil), run_time=0.6)

        with self.voiceover(
            text="Air moves faster over the curved top of the wing. "
            "Faster flow means lower pressure above. Higher pressure below pushes up."
        ):
            # Pressure labels
            low_p = Text("LOW pressure", font_size=22, color=ACCENT, weight=BOLD)
            low_p.next_to(wing.airfoil, UP, buff=0.6)
            high_p = Text("HIGH pressure", font_size=22, color=CORAL, weight=BOLD)
            high_p.next_to(wing.airfoil, DOWN, buff=0.6)

            self.play(FadeIn(low_p, shift=DOWN * 0.2), run_time=0.4)
            self.play(FadeIn(high_p, shift=UP * 0.2), run_time=0.4)

            # Push-up arrows from below
            push_arrows = VGroup(
                *[
                    Arrow(
                        wing.airfoil.get_bottom() + DOWN * 0.5 + RIGHT * (i - 1) * 1.5,
                        wing.airfoil.get_bottom() + UP * 0.1 + RIGHT * (i - 1) * 1.5,
                        color=CORAL,
                        stroke_width=2,
                        buff=0,
                        max_tip_length_to_length_ratio=0.2,
                    )
                    for i in range(3)
                ]
            )
            self.play(
                LaggedStart(*[Create(a) for a in push_arrows], lag_ratio=0.15),
                run_time=0.6,
            )

        with self.voiceover(
            text="This pressure difference creates an additional upward force. "
            "Combined with Newton's reaction force — that's your total lift."
        ):
            # Big combined lift arrow
            big_lift = Arrow(
                DOWN * 2.5,
                UP * 2.5,
                color=ACCENT,
                stroke_width=8,
                buff=0,
                max_tip_length_to_length_ratio=0.08,
            ).shift(RIGHT * 4)
            big_lbl = Text("TOTAL\nLIFT", font_size=24, color=ACCENT, weight=BOLD)
            big_lbl.next_to(big_lift, RIGHT, buff=0.2)
            self.play(Create(big_lift), FadeIn(big_lbl), run_time=0.8)

        self.play(FadeOut(*self.mobjects), run_time=0.4)

    # ── THE REAL ANSWER ──────────────────────────────────────────────────────
    def the_real_answer(self):
        with self.voiceover(
            text="So the real answer? It's not Newton OR Bernoulli. It's both. Working together."
        ):
            both = Text("BOTH.", font_size=64, color=ACCENT, weight=BOLD)
            self.play(FadeIn(both, scale=1.5), run_time=0.6)

            sub = Text(
                "Newton + Bernoulli = Full explanation",
                font_size=28,
                color=LIGHT,
            )
            sub.next_to(both, DOWN, buff=0.5)
            self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.5)
            self.play(Indicate(both, scale_factor=1.08, color=PRIMARY), run_time=0.5)

        self.play(FadeOut(both, sub), run_time=0.4)

    # ── MYTH BUST ────────────────────────────────────────────────────────────
    def myth_bust(self):
        with self.voiceover(
            text="But here's the myth you need to unlearn. "
            "The textbook says air on top must arrive at the trailing edge "
            "at the same time as air on the bottom. The equal transit time theory."
        ):
            myth_title = Text("The Myth: Equal Transit Time", font_size=32, color=WARNING_CLR)
            myth_title.to_edge(UP, buff=0.6)
            self.play(Write(myth_title), run_time=0.5)

            myth_text = Text(
                '"Air on top must arrive at the same time\nas air on the bottom."',
                font_size=24,
                color=MUTED,
            )
            myth_text.move_to(ORIGIN)
            self.play(Write(myth_text), run_time=0.8)

        with self.voiceover(
            text="No physical law requires this. Wind tunnel experiments show "
            "the air on top actually arrives FIRST. The equal transit time idea is simply wrong."
        ):
            # Cross it out
            cross = Cross(myth_text, color=ERROR_CLR, stroke_width=4)
            self.play(Create(cross), run_time=0.5)

            wrong_lbl = Text("WRONG", font_size=48, color=ERROR_CLR, weight=BOLD)
            wrong_lbl.next_to(myth_text, DOWN, buff=0.6)
            self.play(FadeIn(wrong_lbl, scale=1.5), run_time=0.4)
            self.play(Indicate(wrong_lbl, scale_factor=1.1), run_time=0.4)

        with self.voiceover(
            text="And the secret variable that pilots actually control? "
            "Angle of attack. Tilt the wing more, get more lift. Up to a point."
        ):
            self.play(FadeOut(myth_title, myth_text, cross, wrong_lbl), run_time=0.3)

            # Wing that tilts
            wing_bar = RoundedRectangle(
                width=4,
                height=0.2,
                corner_radius=0.05,
                color=LIGHT,
                fill_color=LIGHT,
                fill_opacity=0.6,
                stroke_width=2,
            )
            self.play(FadeIn(wing_bar), run_time=0.3)

            # Angle arc
            angle_arc = Arc(radius=2.0, start_angle=0, angle=PI / 12, color=ACCENT)
            angle_lbl = Text("Angle of Attack", font_size=22, color=ACCENT, weight=BOLD)
            angle_lbl.next_to(angle_arc, RIGHT, buff=0.2)

            self.play(Rotate(wing_bar, angle=PI / 12), run_time=0.8)
            self.play(Create(angle_arc), FadeIn(angle_lbl), run_time=0.5)

            more = Text("More angle → more lift", font_size=24, color=LIGHT)
            more.to_edge(DOWN, buff=0.8)
            self.play(FadeIn(more, shift=UP * 0.2), run_time=0.4)

            # Tilt more
            self.play(Rotate(wing_bar, angle=PI / 18), run_time=0.6)

        self.play(FadeOut(*self.mobjects), run_time=0.4)

    # ── OUTRO ────────────────────────────────────────────────────────────────
    def outro(self):
        with self.voiceover(text="So next time you're on a plane and hit turbulence, remember:"):
            remember = Text("Next time you fly...", font_size=36, color=LIGHT)
            self.play(Write(remember), run_time=0.6)

        with self.voiceover(
            text="Four hundred tons of metal is being held up by the same physics "
            "that pushes your hand up out a car window. Newton and Bernoulli, working together."
        ):
            self.play(FadeOut(remember), run_time=0.3)
            points = (
                VGroup(
                    Text("✓ Newton's 3rd law (action/reaction)", font_size=24, color=ACCENT),
                    Text(
                        "✓ Bernoulli's principle (pressure difference)", font_size=24, color=PRIMARY
                    ),
                    Text("✓ Angle of attack (pilot's control)", font_size=24, color=WARNING_CLR),
                )
                .arrange(DOWN, buff=0.4, aligned_edge=LEFT)
                .move_to(ORIGIN)
            )

            self.play(
                LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in points], lag_ratio=0.3),
                run_time=1.2,
            )

        with self.voiceover(
            text="If this made flight click for you, subscribe. "
            "We break down one impossible-sounding question every week."
        ):
            self.play(FadeOut(points), run_time=0.3)
            sub_box = RoundedRectangle(
                width=6,
                height=1.5,
                corner_radius=0.15,
                color=CORAL,
                fill_color="#2A0D1A",
                fill_opacity=1,
                stroke_width=2,
            )
            sub_txt = Text("SUBSCRIBE", font_size=42, color=CORAL, weight=BOLD)
            sub_txt.move_to(sub_box).shift(UP * 0.1)
            sub_sub = Text("One impossible question. Every week.", font_size=18, color=MUTED)
            sub_sub.move_to(sub_box).shift(DOWN * 0.4)
            self.play(FadeIn(sub_box), Write(sub_txt), FadeIn(sub_sub), run_time=0.6)
            self.play(Indicate(sub_box, scale_factor=1.04, color=PRIMARY), run_time=0.6)

        # Final fade
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.5)
