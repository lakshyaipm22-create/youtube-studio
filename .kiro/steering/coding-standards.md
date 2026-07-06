# Coding Standards

Rules for all Python/Manim code in this repository.

## Video Scene Files (Shorts: 45-60s, Vertical)

### Structure
```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

BG = "#0e1116"
GOLD = "#F5C842"
TEAL = "#2DCDC6"
CORAL = "#FF6B6B"
SOFT_WHT = "#E8E8F0"
MUTED = "#6B6B8A"
PURPLE = "#7B5EA7"
GREEN = "#4CAF7D"

config.background_color = BG
config.pixel_width = 1080    # VERTICAL
config.pixel_height = 1920   # VERTICAL
config.frame_rate = 60

class VideoName(VoiceoverScene, MovingCameraScene):
    def setup(self):
        VoiceoverScene.setup(self)
        MovingCameraScene.setup(self)
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        self.camera.frame.set(width=9, height=16)

    def construct(self):
        self.hook()
        self.explain()
        self.payoff()

    def make_title(self, text, color=TEAL):
        title = Text(text, font_size=44, color=color, weight=BOLD)
        title.to_edge(UP, buff=0.8)
        underline = Line(
            title.get_corner(DL) + DOWN * 0.12,
            title.get_corner(DR) + DOWN * 0.12,
            color=color, stroke_width=2,
        )
        return VGroup(title, underline)

    def clear_all(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
```

### Key Differences from Long-Form
- **Vertical config**: pixel_width=1080, pixel_height=1920
- **Camera frame**: width=9, height=16 (not 16×9)
- **3 sections max**: hook() → explain() → payoff()
- **100-150 words total** narration
- **No section_outro with subscribe CTA** — Shorts don't need it
- **Larger font sizes** — minimum 22, titles 44-56

### Things That DON'T Work (Avoid)
- `GrowArrow()` — use `Create()` for arrows
- `Integer()` / `MathTex()` — use `Text()` for all numbers
- `Cross()` — use two diagonal Lines
- `ChangeDecimalToValue()` — use Text with FadeIn(scale=1.5)

### Things That Work Great
- `BraceBetweenPoints()` for measurements
- `Flash()` for emphasis
- `GrowFromEdge()` / `GrowFromCenter()` for bars
- `Indicate()` / `Circumscribe()` for highlighting
- `LaggedStart()` for staggered reveals
- Camera frame manipulation for zoom effects

## General Python

- Python 3.10+
- Ruff: line-length 100, rules E/F/I/UP/B
- F403/F405 (wildcard imports) allowed in video files
- Import order: stdlib → third-party (blank line) → first-party

## Naming Conventions

- Video files: `descriptive_name.py` (e.g., `phone_vs_apollo.py`)
- Scene classes: PascalCase (e.g., `PhoneVsApollo`)
- Video folders: `NNN_snake_case/`
- Methods: `hook`, `explain`, `payoff` (3-act structure)
