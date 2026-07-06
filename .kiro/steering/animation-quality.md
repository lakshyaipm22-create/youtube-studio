# Animation & Visual Design Standards

Governs all animation for YouTube Shorts (45-60s, vertical 1080×1920).

## Technical Foundation

- `VoiceoverScene` + `MovingCameraScene` (dual inheritance)
- `manim-voiceover` with `GTTSService` for auto voice-animation sync
- **Config: 1080×1920 (VERTICAL), 60fps, background "#0e1116"**
- Each `with self.voiceover(text=...)` block = 2-3 sentences max

## Vertical Frame Config

```python
config.background_color = "#0e1116"
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
```

Camera frame for vertical:
```python
self.camera.frame.set(width=9, height=16)
```

## Shorts-Specific Visual Rules

### Pace: New Visual Every 3 Seconds
- Shorts viewers are FASTER than long-form viewers
- If nothing changes for 3 seconds, they swipe away
- Every voiceover block must have multiple animations inside

### Text Size: BIGGER Than Long-Form
- Titles: font_size=48-56 (must be readable on phone)
- Body: font_size=32-40
- Labels: font_size=24-28
- Never below font_size=22 for anything

### Layout: VERTICAL Stacking
- Objects stack top-to-bottom, NOT left-to-right
- Title at top (UP * 6)
- Main visual in center
- Labels/numbers below
- Keep content in center 70% of frame (safe zone for UI overlays)

### Frame Density
- Phone screen is small — fill it MORE than horizontal
- Every frame: title + visual + number/label minimum
- No lonely object floating in space

## Color Palette

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

Higher contrast than long-form (phone screens in sunlight need it).

## Helper Methods (Use in Every Short)

```python
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

## Animation Variety (7+ Types Per Short)

Even in 50 seconds, use at minimum 7 different animation types:
- `FadeIn` (with scale or shift)
- `Write` / `DrawBorderThenFill`
- `Create` (for lines, arrows)
- `GrowFromEdge` / `GrowFromCenter` (for bars)
- `LaggedStart` (for groups)
- `Indicate` / `Circumscribe` / `Flash` (for emphasis)
- Camera zoom (`self.camera.frame.animate`)
- `Transform` / `ReplacementTransform`

## Known Manim Bugs (Avoid)

- `GrowArrow()` — BROKEN. Use `Create()`.
- `Integer()` / `MathTex()` — need LaTeX. Use `Text()`.
- `Cross()` — sometimes needs LaTeX. Use two Lines.
- `interpolate_color()` with hex strings — wrap in `ManimColor()`.

## Engagement Techniques for Shorts

- **Number reveal**: Big text scaling in with `FadeIn(scale=1.5)`
- **Scale comparison**: Tiny object vs huge object
- **Flash for "wow" moment**: `Flash(obj, color=GOLD, flash_radius=2)`
- **Circumscribe for key fact**: draws attention
- **Camera zoom**: zoom into tiny detail, zoom out to reveal scale

## Pre-Render Checklist

- [ ] Duration: 45-60 seconds (check narration word count: 100-150 words)
- [ ] Vertical format (1080×1920)
- [ ] Hook in first 3 seconds
- [ ] New visual every 3 seconds
- [ ] 7+ animation types used
- [ ] Text readable at phone size (font_size ≥ 22)
- [ ] Payoff moment near the end
- [ ] No dead frames
