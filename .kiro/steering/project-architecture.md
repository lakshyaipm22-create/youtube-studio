# Project Architecture

## Repository Structure

```
youtube-studio/
├── studio/           # Reusable Manim utilities (grow organically)
├── pipeline/         # Batch automation (AI drafts, research)
├── assets/           # Shared SVGs, fonts, music, sounds
├── prompts/          # AI prompt templates
├── videos/           # One folder per video (Shorts)
├── catalog.yaml      # Master video index
├── manim.cfg         # Manim config
├── Makefile          # Utility commands
└── pyproject.toml    # Dependencies
```

## Video = One Self-Contained .py File

Each Short is one Python file. Renders to vertical MP4 + SRT.

```
videos/NNN_slug/
├── scenes/video_name.py    # THE video (narration + animation)
└── assets/                 # Video-specific assets (if needed)
```

## Technology Stack

| Component | Tool |
|-----------|------|
| Animation | Manim Community Edition |
| Voice + Sync | manim-voiceover + GTTSService |
| Format | 1080×1920 vertical @ 60fps |
| Subtitles | Auto-generated .srt |
| Duration | 45-60 seconds |

## Key Dependencies

```
manim>=0.18.0
manim-voiceover>=0.4.0
gtts
sox (system)
ffmpeg (system)
```

## Render Command

```bash
manim render -qh videos/NNN/scenes/video.py ClassName     # 1080p final
manim render -ql videos/NNN/scenes/video.py ClassName     # 480p preview
```

## Git Strategy

- Feature branches → PR → merge to main (auto-merge if CI passes)
- Branch naming: `video/NNN-slug`, `feat/`, `fix/`
- Rendered videos: NEVER committed
- Source .py files: ALWAYS committed
- CI: Ruff lint + format check + tests

## Scalability

- One folder per Short, numbered 001-999
- Batch produce 5-7 per session
- Target: 30+ Shorts per month
