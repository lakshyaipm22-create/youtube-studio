# Production Workflow

## The Proven Approach: One File Per Video

Each video is a **single Python file** using `manim-voiceover`.
Narration and animation live together — perfectly synced, no pipeline needed.

### File Structure

```
videos/NNN_slug/
├── video_name.py    # THE video (narration + animation + everything)
└── assets/          # Video-specific SVGs/images (if needed)
```

Rendering produces: `.mp4` (video) + `.srt` (subtitles) automatically.

### Render Command

```bash
manim render -qh videos/001_topic/video.py MainScene     # 1080p production
manim render -ql videos/001_topic/video.py MainScene     # 480p preview
```

### Video File Template

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

BG = "#0e1116"
GOLD = "#F5C842"
TEAL = "#2DCDC6"
CORAL = "#FF6B6B"
# ... palette constants

config.background_color = BG
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60

class VideoName(VoiceoverScene, MovingCameraScene):
    def setup(self):
        VoiceoverScene.setup(self)
        MovingCameraScene.setup(self)
        self.set_speech_service(GTTSService(lang="en", tld="com"))

    def construct(self):
        self.section_hook()
        self.section_explanation()
        self.section_takeaway()

    def section_hook(self):
        with self.voiceover(text="Narration here"):
            self.play(...)
```

### Why This Works

- **Zero sync issues** — `with self.voiceover()` holds until speech finishes
- **One file** — impossible to get out of sync across files
- **One render** — produces video + audio + subtitles
- **Easy to iterate** — change narration, re-render, done

### The Old Pipeline (Deprecated for Video Creation)

The `produce.py` pipeline stages (research → script → storyboard → etc.) are useful for:
- AI-generating a first draft of narration text
- Batch research across many topics
- NOT for final video production

Final videos are always hand-crafted single .py files.

### Workflow for Producing a Video

1. **Choose topic** (human, 1 min)
2. **Research** (AI draft or manual, 5 min review)
3. **Write the .py file** — narration + animation together (AI generates, human refines)
4. **Preview render** at 480p (`manim render -ql`)
5. **Watch it** — is it engaging? boring? out of pace?
6. **Iterate** sections that don't work
7. **Final render** at 1080p (`manim render -qh`)
8. **Upload** to YouTube

### Human Time Per Video: 15-30 minutes

Most time goes into reviewing and refining the AI-generated .py file.
Rendering is automated. Voice is automated. Subtitles are automated.
