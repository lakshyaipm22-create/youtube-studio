# Animation & Visual Design Standards

This file governs how animations are designed and coded.
Subordinate to `youtube-strategy.md` — every animation decision serves viewer retention.

## Core Principle

Think like an animator for a 500K-subscriber educational channel.
Every frame should look like a screenshot worth sharing.

## Technical Foundation

- Use `VoiceoverScene` + `MovingCameraScene` (dual inheritance)
- Use `manim-voiceover` with `GTTSService` for auto voice-animation sync
- Config: 1920x1080, 60fps, dark background (#0e1116 or #0D0D1A)
- Each `with self.voiceover(text=...)` block = one animation beat

## Visual Rules

### Background
- NEVER use a flat single color
- Use dark navy (#0e1116) which has inherent depth
- Optionally add a subtle gradient or vignette for premium feel

### Frame Density (The #1 Improvement)
Every frame should have multiple layers:
- Section title or context (top)
- Main visual (center)
- Labels, annotations, measurements
- Subtitle bar or narration text (bottom)
- Never a single lonely object on empty background

### Color Palette (Proven)
- Background: `#0e1116` (deep navy-black)
- Gold: `#F5C842` (emphasis, numbers, key reveals)
- Teal: `#2DCDC6` (positive, actions, CTAs)
- Coral/Red: `#FF6B6B` (danger, wrong, attention)
- Soft white: `#E8E8F0` (body text)
- Muted: `#6B6B8A` (secondary info)
- Purple: `#7B5EA7` (categories, labels)
- Green: `#4CAF7D` (success, correct)

### Typography Hierarchy
- Impact numbers: font_size=80-96, BOLD, GOLD
- Section titles: font_size=34-40, BOLD, BLUE/TEAL
- Key statements: font_size=44-52, BOLD, topic color
- Body text: font_size=28-32, normal weight, SOFT_WHT
- Labels: font_size=20-24, normal, GREY
- Annotations: font_size=18-22, ITALIC, MUTED

### Animation Variety (Never Repeat)
Use at minimum 7+ different animation types per video:
- `FadeIn` (with shift/scale) — default entrances
- `Write` — for text that viewer reads
- `Create` — for shapes, lines, arrows
- `GrowFromCenter` / `GrowFromEdge` — for bars, charts
- `LaggedStart` — for groups (stagger reveals)
- `Transform` / `ReplacementTransform` — for morphing
- `Indicate` / `Circumscribe` / `Flash` — for emphasis
- `Rotate` — for transformations
- Camera zoom — for focus moments

NEVER use the same animation type twice in a row.

### Engagement Techniques (Use 3+ Per Video)
- Counter animations (number scaling up with FadeIn)
- Comparison layouts (before/after, side-by-side)
- Bar charts growing with `GrowFromEdge`
- Dot/grid spreading patterns
- Interactive questions ("What do you think?")
- Quote cards with background boxes
- Emphasis with `Indicate()`, `Circumscribe()`, `Flash()`
- Scale comparisons (objects next to each other for size)

### Custom Objects (Build Rich Visuals)
- Buildings with windows (Rectangle + grid of small rectangles)
- Earth/Moon/planets (Circle with fill and label)
- Distance diagrams (BraceBetweenPoints + label)
- Growing bar charts (Rectangle + GrowFromEdge)
- Spreading dots (for growth/virus visualization)
- Paper fold (Rectangle that stretches vertically)

### Camera
- Use `MovingCameraScene` for camera control
- Widen frame for Earth-Moon scale shots: `self.camera.frame.animate.set_width(16)`
- Save/restore state: `self.camera.frame.save_state()` / `Restore(self.camera.frame)`
- Never move camera without purpose

### Transitions
- `FadeOut(*self.mobjects)` between major sections
- Within a section: remove objects individually before adding new ones
- Never cut abruptly — always animate out before in

## Known Manim CE Bugs
- `GrowArrow` is BROKEN (TypeError: scale_tips) — use `Create()` for arrows
- `Integer` / `MathTex` require LaTeX installed — use `Text()` with formatted strings
- `Cross()` sometimes triggers LaTeX — use two diagonal Lines instead

## Pre-Render Checklist
- [ ] Dark background, not flat color
- [ ] Multiple visual layers per frame
- [ ] 7+ different animation types used
- [ ] No static frames > 3 seconds
- [ ] Section titles present
- [ ] Colors from brand palette
- [ ] At least 3 engagement techniques used
- [ ] Camera movement where appropriate
- [ ] Each voiceover block has corresponding animations filling the time

## File References
- #[[file:.kiro/steering/youtube-strategy.md]] — Content strategy
- #[[file:.kiro/steering/production-workflow.md]] — Production workflow
