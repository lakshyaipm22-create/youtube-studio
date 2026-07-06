# Production Workflow

## Format: YouTube Shorts / Instagram Reels

**45-60 seconds. Vertical (1080×1920). One fact per video.**

## One Command to Render

```bash
manim render -qh videos/NNN_slug/scenes/video.py ClassName
```

Produces: `.mp4` (vertical) + `.srt` (subtitles)

## Video File Template (Shorts)

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

BG = "#0e1116"
# ... palette constants

config.background_color = BG
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60

class TopicName(VoiceoverScene, MovingCameraScene):
    def setup(self):
        VoiceoverScene.setup(self)
        MovingCameraScene.setup(self)
        self.set_speech_service(GTTSService(lang="en", tld="com"))
        self.camera.frame.set(width=9, height=16)

    def construct(self):
        self.hook()
        self.explain()
        self.payoff()
```

## 3-Act Structure (50 seconds)

| Act | Time | Purpose | Words |
|-----|------|---------|-------|
| Hook | 0-8s | Shocking statement | 20-25 |
| Explain | 8-45s | Visual explanation | 70-100 |
| Payoff | 45-55s | "Wow" reveal | 20-30 |

**Total: 100-150 words. No more.**

## Production Workflow

1. **Choose fact** — one mind-blowing statement (1 min)
2. **Write .py file** — 3 methods, 100-150 words narration (AI generates, human reviews)
3. **Preview** at 480p: `manim render -ql video.py ClassName` (1 min render)
4. **Watch** — engaging? pacing? (30 sec)
5. **Fix** if needed (5 min)
6. **Final render** at 1080p: `manim render -qh video.py ClassName` (2-3 min)
7. **Upload** to YouTube Shorts + Instagram Reels

**Human time per Short: 10-15 minutes.**
**Target: 1 Short per day, batch 5-7 in one session.**

## Batch Production

Generate 5-7 Shorts in one Kiro session:
```
"Generate 5 YouTube Shorts about: [topic1], [topic2], [topic3], [topic4], [topic5]"
```

Each one is an independent .py file. Render all, review all, upload all.

## File Structure

```
videos/
├── 001_phone_vs_apollo/scenes/phone_vs_apollo.py
├── 002_paper_42_folds/scenes/paper_folds.py
├── 003_neutron_star_weight/scenes/neutron_star.py
└── ...
```

## Upload Strategy

- YouTube Shorts: vertical MP4, no edits needed
- Instagram Reels: same file, add caption in app
- TikTok: same file, add caption in app
- All three platforms from one render

## Quality Gate

Before uploading:
> "Would I stop scrolling for this?"
> "Would I share this?"
> "Is the payoff satisfying?"
