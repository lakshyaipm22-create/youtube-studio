"""
Your Phone Is a Million Times More Powerful Than the Moon Landing Computer.
Render: manim render -qh phone_vs_apollo.py PhoneVsApollo
"""

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

# ── Palette ──────────────────────────────────────────────────────────
BG = "#0e1116"
GOLD = "#F5C842"
TEAL = "#2DCDC6"
CORAL = "#FF6B6B"
SOFT_WHT = "#E8E8F0"
MUTED = "#6B6B8A"
PURPLE = "#7B5EA7"
GREEN = "#4CAF7D"

config.background_color = BG
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60


class PhoneVsApollo(VoiceoverScene, MovingCameraScene):
    def setup(self):
        VoiceoverScene.setup(self)
        MovingCameraScene.setup(self)
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        self.camera.frame.set(width=16, height=9)

    def construct(self):
        self.section_hook()
        self.section_apollo()
        self.section_what_it_did()
        self.section_your_phone()
        self.section_real_scale()
        self.section_why_exponential()
        self.section_punchline()
        self.section_outro()

    # ── 1. HOOK ──────────────────────────────────────────────────────
    def section_hook(self):
        title = Text("Phone vs Moon Computer", font_size=34, color=TEAL).to_edge(UP, buff=0.5)

        with self.voiceover(
            text="In 1969, NASA sent humans to the Moon using a computer "
            "with less power than your calculator."
        ):
            self.play(Write(title), run_time=0.6)

            # Old computer
            old_comp = VGroup(
                Rectangle(
                    width=2.0,
                    height=2.5,
                    color=MUTED,
                    fill_color="#1a1a2e",
                    fill_opacity=1,
                    stroke_width=2,
                ),
                Rectangle(
                    width=1.4,
                    height=0.8,
                    color=MUTED,
                    fill_color="#0a0a1a",
                    fill_opacity=1,
                    stroke_width=1,
                ).shift(UP * 0.5),
                *[
                    Dot(point=DOWN * 0.6 + RIGHT * (i - 1) * 0.3, color=MUTED, radius=0.06)
                    for i in range(4)
                ],
            ).shift(LEFT * 3.5)
            year_old = Text("1969", font_size=24, color=MUTED).next_to(old_comp, DOWN, buff=0.3)

            self.play(FadeIn(old_comp, shift=UP * 0.3), run_time=0.8)
            self.play(Write(year_old), run_time=0.4)

        with self.voiceover(
            text="Today, the phone in your pocket has a million times more "
            "processing power. Not twice. Not ten times. A million."
        ):
            # Phone
            phone = VGroup(
                RoundedRectangle(
                    width=1.2,
                    height=2.2,
                    corner_radius=0.12,
                    color=TEAL,
                    fill_color="#0a2020",
                    fill_opacity=1,
                    stroke_width=2,
                ),
                RoundedRectangle(
                    width=1.0,
                    height=1.7,
                    corner_radius=0.05,
                    color=TEAL,
                    fill_color="#051515",
                    fill_opacity=1,
                    stroke_width=1,
                ).shift(UP * 0.1),
            ).shift(RIGHT * 3.5)
            year_new = Text("Today", font_size=24, color=TEAL).next_to(phone, DOWN, buff=0.3)

            self.play(FadeIn(phone, shift=UP * 0.3), Write(year_new), run_time=0.8)

            # The big number
            mult = Text("1,000,000×", font_size=72, color=GOLD, weight=BOLD)
            mult.move_to(ORIGIN)
            self.play(FadeIn(mult, scale=1.8), run_time=0.6)
            self.play(Indicate(mult, scale_factor=1.1, color=GOLD), run_time=0.6)

        self.play(FadeOut(*self.mobjects), run_time=0.5)

    # ── 2. THE APOLLO COMPUTER ───────────────────────────────────────
    def section_apollo(self):
        sec_title = Text("The Apollo Guidance Computer", font_size=34, color=PURPLE).to_edge(
            UP, buff=0.5
        )

        with self.voiceover(
            text="The Apollo Guidance Computer had 74 kilobytes of memory. "
            "That's not enough to store a single photo from your phone."
        ):
            self.play(Write(sec_title), run_time=0.5)

            # Computer visual
            agc = VGroup(
                Rectangle(
                    width=3.0,
                    height=2.0,
                    color=MUTED,
                    fill_color="#1a1a2e",
                    fill_opacity=1,
                    stroke_width=2,
                ),
                Text("AGC", font_size=28, color=MUTED, weight=BOLD).shift(UP * 0.3),
                Text("Apollo Guidance\nComputer", font_size=16, color=MUTED).shift(DOWN * 0.3),
            ).shift(LEFT * 3 + DOWN * 0.5)
            self.play(FadeIn(agc, shift=RIGHT * 0.3), run_time=0.8)

            # Memory bar - tiny
            mem_bar_bg = Rectangle(
                width=5,
                height=0.4,
                color=MUTED,
                fill_color="#0a0a14",
                fill_opacity=1,
                stroke_width=1,
            )
            mem_bar_bg.shift(RIGHT * 1.5 + UP * 0.5)
            mem_bar = Rectangle(
                width=0.03,
                height=0.4,
                color=CORAL,
                fill_color=CORAL,
                fill_opacity=0.9,
                stroke_width=0,
            )
            mem_bar.align_to(mem_bar_bg, LEFT)
            mem_label = Text("74 KB", font_size=28, color=CORAL, weight=BOLD)
            mem_label.next_to(mem_bar_bg, RIGHT, buff=0.3)

            self.play(FadeIn(mem_bar_bg), run_time=0.3)
            self.play(FadeIn(mem_bar), Write(mem_label), run_time=0.5)

        with self.voiceover(
            text="It ran at 0.043 megahertz. Your microwave has a faster processor."
        ):
            speed = Text("0.043 MHz", font_size=52, color=GOLD, weight=BOLD)
            speed.shift(RIGHT * 1.5 + DOWN * 1.2)
            self.play(FadeIn(speed, scale=1.3), run_time=0.6)

            micro = Text("Your microwave: faster", font_size=22, color=CORAL, slant=ITALIC)
            micro.next_to(speed, DOWN, buff=0.3)
            self.play(Write(micro), run_time=0.5)
            self.play(Indicate(micro, color=CORAL), run_time=0.5)

        self.play(FadeOut(*self.mobjects), run_time=0.5)

    # ── 3. WHAT IT DID ───────────────────────────────────────────────
    def section_what_it_did(self):
        sec_title = Text("But Look What It Did", font_size=34, color=GREEN).to_edge(UP, buff=0.5)

        with self.voiceover(
            text="But here's what's incredible. That tiny computer navigated "
            "three humans across 240,000 miles of space. It calculated "
            "trajectories, managed thrust, and landed them on the Moon."
        ):
            self.play(Write(sec_title), run_time=0.5)

            # Earth-Moon diagram
            earth = Circle(radius=0.6, color=BLUE, fill_color=BLUE_E, fill_opacity=0.8)
            earth.shift(LEFT * 4.5 + DOWN * 0.5)
            earth_lbl = Text("Earth", font_size=18, color=BLUE_B).next_to(earth, DOWN, buff=0.2)

            moon = Circle(radius=0.35, color=GREY_A, fill_color=GREY_B, fill_opacity=0.8)
            moon.shift(RIGHT * 4.5 + DOWN * 0.5)
            moon_lbl = Text("Moon", font_size=18, color=GREY_A).next_to(moon, DOWN, buff=0.2)

            self.play(FadeIn(earth), Write(earth_lbl), run_time=0.5)
            self.play(FadeIn(moon), Write(moon_lbl), run_time=0.5)

            # Distance line
            path_line = Line(
                earth.get_right() + RIGHT * 0.1,
                moon.get_left() + LEFT * 0.1,
                color=GOLD,
                stroke_width=2,
            )
            self.play(Create(path_line), run_time=1.0)

            # Distance label
            brace = BraceBetweenPoints(
                earth.get_bottom() + DOWN * 0.5,
                moon.get_bottom() + DOWN * 0.5,
                direction=DOWN,
                color=TEAL,
            )
            dist_lbl = Text("240,000 miles", font_size=22, color=TEAL)
            dist_lbl.next_to(brace, DOWN, buff=0.15)
            self.play(GrowFromCenter(brace), Write(dist_lbl), run_time=0.8)

            # Astronaut dots traveling
            dots = VGroup(*[Dot(color=SOFT_WHT, radius=0.08) for _ in range(3)])
            dots.arrange(DOWN, buff=0.15).move_to(earth.get_right() + RIGHT * 0.3)
            self.play(FadeIn(dots), run_time=0.3)
            self.play(dots.animate.move_to(moon.get_left() + LEFT * 0.3), run_time=1.5)

        with self.voiceover(text="With less computing power than a musical greeting card."):
            # Greeting card
            card = VGroup(
                Rectangle(
                    width=1.8,
                    height=1.3,
                    color=CORAL,
                    fill_color="#2a0d0d",
                    fill_opacity=1,
                    stroke_width=2,
                ),
                Text("♪", font_size=36, color=CORAL),
            ).shift(DOWN * 2.5 + RIGHT * 3)
            card_lbl = Text("Greeting card", font_size=18, color=CORAL)
            card_lbl.next_to(card, DOWN, buff=0.15)
            self.play(FadeIn(card, scale=0.8), Write(card_lbl), run_time=0.6)
            self.play(Indicate(card, scale_factor=1.1, color=GOLD), run_time=0.5)

        self.play(FadeOut(*self.mobjects), run_time=0.5)

    # ── 4. YOUR PHONE ────────────────────────────────────────────────
    def section_your_phone(self):
        sec_title = Text("Your Phone Today", font_size=34, color=TEAL).to_edge(UP, buff=0.5)

        with self.voiceover(
            text="Your iPhone has 6 gigabytes of RAM. That's eighty thousand "
            "times more memory than Apollo."
        ):
            self.play(Write(sec_title), run_time=0.5)

            # Side by side bars
            bar_label_a = Text("Apollo: 74 KB", font_size=20, color=MUTED)
            bar_label_a.shift(LEFT * 3 + UP * 1.5)
            bar_a = Rectangle(
                width=0.05,
                height=0.4,
                color=CORAL,
                fill_color=CORAL,
                fill_opacity=0.8,
                stroke_width=0,
            )
            bar_a.next_to(bar_label_a, DOWN, buff=0.3).align_to(bar_label_a, LEFT)

            bar_label_p = Text("Phone: 6 GB", font_size=20, color=TEAL)
            bar_label_p.shift(LEFT * 3 + DOWN * 0.5)
            bar_p = Rectangle(
                width=5.0, height=0.4, color=TEAL, fill_color=TEAL, fill_opacity=0.8, stroke_width=0
            )
            bar_p.next_to(bar_label_p, DOWN, buff=0.3).align_to(bar_label_p, LEFT)

            self.play(Write(bar_label_a), FadeIn(bar_a), run_time=0.5)
            self.play(Write(bar_label_p), run_time=0.3)
            self.play(GrowFromEdge(bar_p, LEFT), run_time=1.2)

            mult = Text("×80,000", font_size=40, color=GOLD, weight=BOLD)
            mult.shift(RIGHT * 2 + UP * 0.5)
            self.play(FadeIn(mult, scale=1.5), run_time=0.5)

        with self.voiceover(
            text="Its processor runs at 3.5 gigahertz. That's a hundred thousand times faster."
        ):
            speed_comp = (
                VGroup(
                    Text("Apollo: 0.043 MHz", font_size=24, color=MUTED),
                    Text("Phone: 3,500 MHz", font_size=24, color=TEAL),
                )
                .arrange(DOWN, buff=0.4)
                .shift(DOWN * 2)
            )
            self.play(
                LaggedStart(*[FadeIn(t, shift=RIGHT * 0.3) for t in speed_comp], lag_ratio=0.3),
                run_time=0.8,
            )

            mult2 = Text("×100,000", font_size=44, color=GOLD, weight=BOLD)
            mult2.next_to(speed_comp, RIGHT, buff=0.8)
            self.play(FadeIn(mult2, scale=1.5), run_time=0.5)
            self.play(Circumscribe(mult2, color=GOLD, buff=0.1), run_time=0.6)

        self.play(FadeOut(*self.mobjects), run_time=0.5)

    # ── 5. THE REAL SCALE ────────────────────────────────────────────
    def section_real_scale(self):
        sec_title = Text("Putting It In Perspective", font_size=34, color=GOLD).to_edge(
            UP, buff=0.5
        )

        with self.voiceover(
            text="If the Apollo computer were a single drop of water, your "
            "phone would be an Olympic swimming pool."
        ):
            self.play(Write(sec_title), run_time=0.5)

            # Drop of water
            drop = Circle(radius=0.15, color=BLUE, fill_color=BLUE, fill_opacity=0.8).shift(
                LEFT * 4 + DOWN * 0.5
            )
            drop_lbl = Text("Apollo\n(1 drop)", font_size=18, color=MUTED)
            drop_lbl.next_to(drop, DOWN, buff=0.3)
            self.play(FadeIn(drop, scale=2), Write(drop_lbl), run_time=0.6)

            # Swimming pool
            pool = Rectangle(
                width=5.0,
                height=2.0,
                color=BLUE,
                fill_color=BLUE_E,
                fill_opacity=0.4,
                stroke_width=2,
            )
            pool.shift(RIGHT * 1.5 + DOWN * 0.5)
            pool_lbl = Text("Your Phone\n(Olympic pool)", font_size=18, color=TEAL)
            pool_lbl.next_to(pool, DOWN, buff=0.3)
            self.play(GrowFromCenter(pool), Write(pool_lbl), run_time=1.0)
            self.play(Flash(pool.get_center(), color=TEAL, num_lines=8), run_time=0.6)

        with self.voiceover(
            text="If Apollo were a bicycle, your phone would be a fleet of rockets."
        ):
            self.play(FadeOut(drop, drop_lbl, pool, pool_lbl), run_time=0.3)

            # Bicycle (simple)
            bike = VGroup(
                Circle(radius=0.3, color=MUTED, stroke_width=2).shift(LEFT * 0.4),
                Circle(radius=0.3, color=MUTED, stroke_width=2).shift(RIGHT * 0.4),
                Line(LEFT * 0.4 + UP * 0.3, RIGHT * 0.1 + UP * 0.5, color=MUTED, stroke_width=2),
                Line(LEFT * 0.4, RIGHT * 0.1 + UP * 0.5, color=MUTED, stroke_width=2),
            ).shift(LEFT * 4 + DOWN * 0.5)
            bike_lbl = Text("Apollo", font_size=18, color=MUTED).next_to(bike, DOWN, buff=0.3)
            self.play(FadeIn(bike), Write(bike_lbl), run_time=0.5)

            # Rockets
            rockets = VGroup()
            for i in range(5):
                rocket = VGroup(
                    Rectangle(
                        width=0.3,
                        height=1.0,
                        color=CORAL,
                        fill_color=CORAL,
                        fill_opacity=0.7,
                        stroke_width=1,
                    ),
                    Polygon(
                        [0, 0.5, 0],
                        [-0.15, 0.3, 0],
                        [0.15, 0.3, 0],
                        color=CORAL,
                        fill_color=CORAL,
                        fill_opacity=0.9,
                        stroke_width=0,
                    ),
                ).shift(RIGHT * (i * 0.8) + DOWN * 0.5)
                rockets.add(rocket)
            rockets.move_to(RIGHT * 2 + DOWN * 0.3)
            rocket_lbl = Text("Your Phone", font_size=18, color=TEAL)
            rocket_lbl.next_to(rockets, DOWN, buff=0.3)
            self.play(
                LaggedStart(*[FadeIn(r, shift=UP * 0.3) for r in rockets], lag_ratio=0.15),
                Write(rocket_lbl),
                run_time=1.0,
            )

        self.play(FadeOut(*self.mobjects), run_time=0.5)

    # ── 6. WHY EXPONENTIAL ───────────────────────────────────────────
    def section_why_exponential(self):
        sec_title = Text("Moore's Law", font_size=34, color=PURPLE).to_edge(UP, buff=0.5)

        with self.voiceover(
            text="How did we get here? Moore's Law. Every two years, computing "
            "power roughly doubles. For fifty-five years straight."
        ):
            self.play(Write(sec_title), run_time=0.5)

            # Bar chart
            decades = ["1970", "1980", "1990", "2000", "2010", "2020"]
            heights = [0.2, 0.5, 1.0, 1.8, 3.0, 4.5]
            bars = VGroup()
            labels = VGroup()
            for i, (decade, h) in enumerate(zip(decades, heights, strict=True)):
                bar = (
                    Rectangle(
                        width=0.9,
                        height=h,
                        color=interpolate_color(ManimColor(PURPLE), ManimColor(GOLD), i / 5),
                        fill_color=interpolate_color(ManimColor(PURPLE), ManimColor(GOLD), i / 5),
                        fill_opacity=0.85,
                        stroke_width=1,
                    )
                    .align_to(DOWN * 2.5, DOWN)
                    .shift(RIGHT * (i - 2.5) * 1.3)
                )
                lbl = Text(decade, font_size=16, color=MUTED).next_to(bar, DOWN, buff=0.15)
                bars.add(bar)
                labels.add(lbl)

            for _i, (bar, lbl) in enumerate(zip(bars, labels, strict=True)):
                self.play(GrowFromEdge(bar, DOWN), FadeIn(lbl), run_time=0.4)

        with self.voiceover(
            text="Those quiet doublings, each one barely noticeable, compounded "
            "into something staggering."
        ):
            # Highlight last two bars
            self.play(
                bars[-1].animate.set_color(GOLD),
                bars[-2].animate.set_color(CORAL),
                run_time=0.6,
            )
            self.play(
                Indicate(bars[-1], scale_factor=1.1, color=GOLD),
                run_time=0.6,
            )

            doubles_lbl = Text(
                "Doubles every 2 years", font_size=24, color=TEAL, weight=BOLD
            ).to_edge(DOWN, buff=0.6)
            self.play(Write(doubles_lbl), run_time=0.5)

        self.play(FadeOut(*self.mobjects), run_time=0.5)

    # ── 7. THE PUNCHLINE ─────────────────────────────────────────────
    def section_punchline(self):
        with self.voiceover(
            text="And here's the part that should terrify and excite you "
            "equally. We use this godlike computing power mostly to scroll "
            "social media, argue with strangers, and watch cat videos."
        ):
            # Phone in center
            phone = RoundedRectangle(
                width=1.5,
                height=2.8,
                corner_radius=0.15,
                color=TEAL,
                fill_color="#0a1a1a",
                fill_opacity=1,
                stroke_width=2,
            )
            self.play(FadeIn(phone, scale=0.8), run_time=0.5)

            # Icons around it
            social = Text("📱 Social", font_size=20, color=MUTED)
            social.next_to(phone, UL, buff=0.5)
            argue = Text("💬 Arguments", font_size=20, color=CORAL)
            argue.next_to(phone, UR, buff=0.5)
            cats = Text("🐱 Cat Videos", font_size=20, color=GOLD)
            cats.next_to(phone, DOWN, buff=0.8)

            self.play(
                LaggedStart(
                    FadeIn(social, shift=DOWN * 0.2),
                    FadeIn(argue, shift=DOWN * 0.2),
                    FadeIn(cats, shift=UP * 0.2),
                    lag_ratio=0.3,
                ),
                run_time=0.8,
            )

        with self.voiceover(
            text="We carry the Moon landing in our pockets and use it to order pizza."
        ):
            pizza = Text("🍕", font_size=52).shift(RIGHT * 3)
            self.play(FadeIn(pizza, scale=2), run_time=0.5)

            punchline = Text(
                "The Moon landing fits in your pocket.",
                font_size=28,
                color=GOLD,
                weight=BOLD,
            ).to_edge(DOWN, buff=0.6)
            self.play(Write(punchline), run_time=0.7)
            self.play(Indicate(punchline, scale_factor=1.05, color=GOLD), run_time=0.5)

        self.play(FadeOut(*self.mobjects), run_time=0.5)

    # ── 8. OUTRO ─────────────────────────────────────────────────────
    def section_outro(self):
        with self.voiceover(
            text="The next time you pick up your phone, remember: you're "
            "holding more computing power than every computer that existed "
            "in 1969. Combined."
        ):
            # Grid of old computers (like 100-doors pattern)
            grid = VGroup()
            for _i in range(50):
                r = Rectangle(
                    width=0.35,
                    height=0.5,
                    color=MUTED,
                    fill_color="#1a1a2e",
                    fill_opacity=0.8,
                    stroke_width=1,
                )
                grid.add(r)
            grid.arrange_in_grid(rows=5, cols=10, buff=0.08).shift(UP * 0.5)
            grid_lbl = Text("Every computer in 1969", font_size=20, color=MUTED).next_to(
                grid, DOWN, buff=0.3
            )

            self.play(
                LaggedStart(*[FadeIn(r) for r in grid], lag_ratio=0.01),
                run_time=1.2,
            )
            self.play(Write(grid_lbl), run_time=0.5)

        with self.voiceover(
            text="What you do with it is up to you. Subscribe for more impossible facts."
        ):
            # VS phone
            vs = Text("VS", font_size=36, color=GOLD, weight=BOLD)
            phone_icon = RoundedRectangle(
                width=0.8,
                height=1.4,
                corner_radius=0.1,
                color=TEAL,
                fill_color="#0a2020",
                fill_opacity=1,
                stroke_width=2,
            )
            vs_group = VGroup(vs, phone_icon).arrange(RIGHT, buff=0.4)
            vs_group.to_edge(DOWN, buff=1.2)
            self.play(FadeIn(vs_group, shift=UP * 0.3), run_time=0.5)

            # What will you do?
            self.play(FadeOut(grid, grid_lbl, vs_group), run_time=0.4)

            # Subscribe CTA
            sub_box = RoundedRectangle(
                width=6,
                height=1.5,
                corner_radius=0.15,
                color=CORAL,
                fill_color="#1a0a0a",
                fill_opacity=1,
                stroke_width=2,
            )
            sub_txt = Text("SUBSCRIBE", font_size=42, color=CORAL, weight=BOLD)
            sub_txt.move_to(sub_box).shift(UP * 0.1)
            sub_sub = (
                Text("More impossible facts. Every week.", font_size=18, color=MUTED)
                .move_to(sub_box)
                .shift(DOWN * 0.4)
            )
            self.play(FadeIn(sub_box), Write(sub_txt), FadeIn(sub_sub), run_time=0.6)
            self.play(Indicate(sub_box, scale_factor=1.04, color=GOLD), run_time=0.6)

        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.5)
