# Project Architecture

Structural rules for the youtube-studio repository.
These decisions are final and should not be revisited without major cause.

## Repository Structure

```
youtube-studio/
├── studio/           # Reusable Manim library (channel SDK)
├── pipeline/         # Automation scripts (CLI tools)
├── assets/           # Shared assets (SVGs, fonts, music, sounds)
├── prompts/          # AI prompt templates (global)
├── videos/           # One folder per video (numbered)
│   └── _template/    # Scaffolding template
├── output/           # Rendered output (gitignored)
├── catalog.yaml      # Master index of all videos
├── manim.cfg         # Manim render configuration
├── Makefile          # All production commands
├── ANIMATION_GUIDE.md # Extended animation reference
└── pyproject.toml    # Python dependencies
```

## Structural Rules

- **Do not reorganize the folder structure.** It is settled.
- **Do not add category subdirectories** under `videos/`. Flat numbered folders scale to 500+.
- **Do not add new top-level directories** without explicit user approval.
- **`studio/` is minimal.** Only 4 core files exist (styles, base, intro, outro). Add more only after 3+ repetitions.
- **`pipeline/` scripts are CLI tools.** Each is invoked via Makefile. No inter-script imports.
- **`output/` is always gitignored.** Never commit rendered media.
- **`catalog.yaml` is the video database.** Updated by `pipeline/new_video.py`.
- **`assets/manifest.yaml`** (when created) is the AI-readable asset index.

## Video Folder Standard

Every video folder contains exactly:

```
videos/NNN_slug/
├── video.yaml       # Metadata + scene order (machine-readable)
├── script.md        # Narration script
├── storyboard.md    # Visual plan per scene
├── scenes.py        # All Manim scene classes
├── notes.md         # References, prompts used, production notes
└── research/        # Research materials, PDFs, screenshots
```

Do not add extra files or subfolders to this structure without explicit need.
Video-specific assets go in `videos/NNN/assets/` (created only when needed, not by default).

## Technology Stack (Locked)

| Component | Tool | Change Policy |
|-----------|------|---------------|
| Animation | Manim Community Edition | Pin version in pyproject.toml |
| TTS Primary | Kokoro-82M | May upgrade version, not replace |
| TTS Fallback | Edge-TTS | Stable fallback, keep available |
| Subtitles | faster-whisper | May upgrade model size |
| Audio/Video | FFmpeg + pydub | Industry standard, won't change |
| Scripting | Python 3.10+ | Follow Manim's Python support |

## Automation Interface

All production commands go through the Makefile:
- `make new` — scaffold video
- `make render` / `make preview` — render scenes
- `make voice` — generate voiceover
- `make subs` — generate subtitles
- `make export` — final assembly
- `make produce` — full pipeline

New automation must be added as Makefile targets backed by `pipeline/` scripts.
Never require manual multi-step CLI invocation.

## Scalability Decisions

- Video numbering: 3-digit prefix (001-999). No renumbering. Gaps acceptable.
- Catalog: single `catalog.yaml` file. Split by year only if exceeding 500 entries.
- Assets: flat within category folders. Only add subfolders when 20+ files in one category.
- Studio library: grows organically. Maximum target: ~15 modules after 200 videos.

## Git Strategy

- Never commit to main directly. Always use feature branches.
- Branch naming: `feat/description`, `fix/description`, `video/NNN-slug`
- Commit messages: conventional commits (`feat:`, `fix:`, `docs:`, `video:`)
- Rendered output, generated audio, and generated subtitles are NEVER committed.
- Large binary assets (fonts, music) are committed directly (not LFS) unless individual files exceed 10MB.
