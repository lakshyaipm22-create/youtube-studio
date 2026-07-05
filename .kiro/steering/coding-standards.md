# Coding Standards

Rules for all Python/Manim code in this repository.

## Manim Scene Code

### Inheritance & Imports

- All scenes inherit from `StudioScene` (from `studio/base.py`)
- Always import: `from studio.styles import *`
- Always import: `from studio.base import StudioScene`
- Use `from studio.intro import IntroScene` and `from studio.outro import OutroScene` for bookend scenes

### Use Brand Helpers (Never Raw Manim)

- Text: `brand_text()`, `brand_title()` — never raw `Text()`
- Code: `brand_code()` — never raw `Code()`
- Colors: `BRAND_PRIMARY`, `BRAND_ACCENT`, etc. — never hex strings in scene code
- Fonts: `FONT_PRIMARY`, `FONT_CODE` — never string literals

### Use Constants (Never Magic Numbers)

- Timing: `FADE_NORMAL`, `PAUSE_MEDIUM`, `STAGGER_DELAY` — never raw floats
- Positions: `POS_TITLE`, `POS_CENTER`, `POS_LEFT` — never raw coordinate vectors
- Sizes: `FONT_SIZE_TITLE`, `FONT_SIZE_BODY` — never raw integers
- Pauses: `self.pause_beat()`, `self.pause_medium()` — never raw `self.wait(0.5)`

### Scene Structure

- One `scenes.py` file per video with multiple scene classes
- Scene classes listed in render order in `video.yaml`
- Keep scenes focused: one concept per scene class
- Only split into multiple files if a video has 10+ scene classes

## Pipeline Code

- Scripts in `pipeline/` are standalone CLI tools
- Each script has argparse with `--help`
- Each script works from the repo root via Makefile
- Use `pathlib.Path` for all file operations
- Use `yaml.safe_load()` for YAML (never `yaml.load()`)

## General Python

- Python 3.10+ (use `X | None` not `Optional[X]`)
- Type hints on function signatures
- Docstrings on all public functions and classes
- No wildcard imports in pipeline code (only in scenes where `from studio.styles import *` is the convention)

## Reusability Rule

Only extract code to `studio/` after the same pattern appears in 3+ videos.
Do not pre-build reusable modules speculatively.
Grow the library organically from real repetition.

## Naming Conventions

- Video folders: `NNN_snake_case_title/` (e.g., `001_what_is_python/`)
- Scene classes: PascalCase describing content (e.g., `WhyPythonIsPopular`)
- Module files: snake_case (e.g., `text_animations.py`)
- Constants: UPPER_SNAKE_CASE
- Functions: snake_case
- Never rename video folders after creation (gaps in numbering are acceptable)
