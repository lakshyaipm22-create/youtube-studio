# YouTube Studio

A production system for creating educational YouTube videos using Manim animations and AI.

Designed for a solo creator producing 100+ videos with consistent quality,
reusable components, and an automated pipeline from script to final export.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -e .

# 2. Create your first video
make new title="What is Python?" series=python-basics tags="python,beginner"

# 3. Write your script
# Edit: videos/001_what_is_python/script.md

# 4. Design your storyboard
# Edit: videos/001_what_is_python/storyboard.md

# 5. Code your scenes
# Edit: videos/001_what_is_python/scenes.py

# 6. Preview a scene (fast, low quality)
make preview v=001_what_is_python s=Intro

# 7. Produce the full video (voice + render + subtitles + export)
make produce v=001_what_is_python

# 8. Find your video at: output/001_what_is_python/final.mp4
```

---

## Project Structure

```
youtube-studio/
├── studio/           # Reusable Manim library (your channel's SDK)
│   ├── styles.py     # Colors, fonts, timing constants
│   ├── base.py       # StudioScene base class
│   ├── intro.py      # Branded intro animation
│   └── outro.py      # Branded outro animation
│
├── pipeline/         # Automation scripts
│   ├── new_video.py  # Scaffold new video folders
│   ├── voiceover.py  # Script → AI narration (Kokoro/Edge-TTS)
│   ├── subtitles.py  # Audio → SRT subtitles (faster-whisper)
│   ├── render.py     # Render Manim scenes
│   └── export.py     # Final assembly (FFmpeg)
│
├── assets/           # Shared assets
│   ├── svg/          # SVG illustration library
│   ├── fonts/        # Brand typography
│   ├── images/       # Logos, backgrounds
│   ├── music/        # Background tracks
│   └── sounds/       # Sound effects
│
├── prompts/          # AI prompt templates
├── videos/           # One folder per video
│   └── _template/    # Copy this for new videos
│
├── ANIMATION_GUIDE.md  # Animation quality standards
├── catalog.yaml        # Master index of all videos
├── Makefile            # All production commands
├── manim.cfg           # Render settings
└── pyproject.toml      # Python dependencies
```

---

## Production Workflow

```
Research → Script → Storyboard → Animation Design → Manim Code → Voice → Render → Export
```

| Stage | Command | Tool |
|-------|---------|------|
| Create video | `make new title="..."` | pipeline/new_video.py |
| Preview scene | `make preview v=... s=...` | Manim (-ql) |
| Generate voice | `make voice v=...` | Kokoro-82M / Edge-TTS |
| Render scenes | `make render v=...` | Manim (-qh, 1080p60) |
| Generate subs | `make subs v=...` | faster-whisper |
| Final export | `make export v=...` | FFmpeg |
| **Full pipeline** | **`make produce v=...`** | All of the above |

---

## Make Commands

```bash
make help           # Show all available commands

# Scaffolding
make new title="Title" [series=name] [tags="a,b,c"]

# Rendering
make preview v=FOLDER s=SceneName     # 480p quick preview
make render v=FOLDER                  # 1080p 60fps production
make render-4k v=FOLDER               # 4K 60fps
make render-scene v=FOLDER s=Scene    # Single scene

# Audio
make voice v=FOLDER                   # Kokoro TTS (default)
make voice-edge v=FOLDER              # Edge-TTS (cloud, no GPU)

# Subtitles & Export
make subs v=FOLDER                    # Generate SRT
make export v=FOLDER                  # Final YouTube MP4
make export-subs v=FOLDER             # Export with burned subtitles

# Full Pipeline
make produce v=FOLDER                 # Everything in one command

# Utilities
make list                             # List all videos
make clean v=FOLDER                   # Delete output for one video
make clean-all                        # Delete all output
```

---

## Writing Scenes

Every video's scenes inherit from `StudioScene`:

```python
from manim import *
from studio.base import StudioScene
from studio.intro import IntroScene
from studio.outro import OutroScene
from studio.styles import *

class Intro(IntroScene):
    TITLE = "What is Python?"
    SUBTITLE = "A Beginner's Guide"

class WhatIsPython(StudioScene):
    def construct(self):
        title = self.make_title("The Basics")
        self.play(FadeIn(title, shift=DOWN * 0.3))
        self.pause_medium()

        # Load an SVG illustration
        laptop = self.load_svg("assets/svg/technology/laptop.svg")
        laptop.move_to(POS_CENTER)
        self.play(FadeIn(laptop, scale=0.8))
        self.pause_medium()

        self.fade_out_all()

class Outro(OutroScene):
    NEXT_VIDEO = "Variables Explained"
```

---

## Tool Stack

| Tool | Purpose | License |
|------|---------|---------|
| [Manim CE](https://www.manim.community/) | Animation engine | MIT |
| [Kokoro-82M](https://github.com/hexgrad/kokoro) | AI voice generation | Apache 2.0 |
| [Edge-TTS](https://github.com/rany2/edge-tts) | Cloud TTS (fallback) | MIT |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Subtitle generation | MIT |
| [FFmpeg](https://ffmpeg.org/) | Audio/video processing | LGPL |
| [pydub](https://github.com/jiaaro/pydub) | Audio manipulation | MIT |

---

## System Requirements

- Python 3.10+
- FFmpeg (system install)
- LaTeX (for Manim math rendering, optional)
- ~2GB disk for AI models (Kokoro + Whisper)

---

## Adding Reusable Components

Only add a new module to `studio/` after you've copied the same animation
into 3+ videos. Start minimal, grow organically.

```bash
# When you notice repetition, create a module:
# studio/bullets.py, studio/code.py, studio/comparisons.py, etc.
```

See `ANIMATION_GUIDE.md` for animation quality standards.
