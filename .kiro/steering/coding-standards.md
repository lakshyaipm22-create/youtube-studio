# Coding Standards

Rules for all Python/Manim code in this repository.

## Video Scene Files (Primary Output)

### Structure
- One `.py` file per video
- Inherits from `VoiceoverScene` + `MovingCameraScene`
- Section methods: `self.section_hook()`, `self.section_explanation()`, etc.
- Each section contains multiple `with self.voiceover(text=...)` blocks
- 2-4 sentences max per voiceover block (keeps animations tight)

### Setup Pattern
```python
def setup(self):
    VoiceoverScene.setup(self)
    MovingCameraScene.setup(self)
    self.set_speech_service(GTTSService(lang="en", tld="com"))
    self.camera.background_color = "#0e1116"
```

### Color Constants (Top of File)
```python
BG = "#0e1116"
GOLD = "#F5C842"
TEAL = "#2DCDC6"
CORAL = "#FF6B6B"
SOFT_WHT = "#E8E8F0"
MUTED = "#6B6B8A"
PURPLE = "#7B5EA7"
GREEN = "#4CAF7D"
```

### Config (Top of File)
```python
config.background_color = BG
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60
```

### Import Pattern
```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
```

### Things That DON'T Work (Avoid)
- `GrowArrow()` — use `Create()` for arrows
- `Integer()` / `MathTex()` — require LaTeX, use `Text()` instead
- `Cross()` — sometimes needs LaTeX, use two diagonal `Line()` objects
- `ChangeDecimalToValue()` — needs Integer/DecimalNumber (LaTeX)
- Multiline strings in `Text()` — use separate Text objects or `\n`

### Things That DO Work Well
- `BraceBetweenPoints()` for distance labels
- `Flash()` for emphasis moments
- `GrowFromEdge()` / `GrowFromCenter()` for bars and shapes
- `interpolate_color()` for color gradients across groups
- `Indicate()` / `Circumscribe()` for highlighting
- `LaggedStart()` for staggered group reveals
- Camera frame manipulation via `self.camera.frame.animate`

## Studio Library (Legacy)

The `studio/` package (styles.py, base.py, intro.py, outro.py) was built
for the multi-file pipeline approach. For new videos using manim-voiceover,
define colors/constants directly in the video file instead.

The studio library remains available for utility functions that prove
useful across 3+ videos. Grow it organically.

## Pipeline Code

Scripts in `pipeline/` are standalone CLI tools for batch operations.
They are NOT part of the video rendering workflow.

## General Python

- Python 3.10+
- Type hints on function signatures
- Ruff: line-length 100, rules E/F/I/UP/B
- F403/F405 (wildcard imports) allowed in video scene files
- Import order: stdlib → third-party (blank line) → first-party (blank line)

## Naming Conventions

- Video files: `descriptive_name.py` (e.g., `paper_folding.py`)
- Scene classes: PascalCase (e.g., `PaperFolding`, `WhyAirplanesFly`)
- Video folders: `NNN_snake_case/` (e.g., `001_why_airplanes_dont_fall/`)
- Section methods: `section_hook`, `section_explanation`, `section_takeaway`
- Custom Mobject classes: PascalCase (e.g., `Wing`, `Door`, `SubtitleBar`)
