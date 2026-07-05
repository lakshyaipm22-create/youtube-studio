# Animation Quality Standards

This steering file ensures Kiro generates professional-quality Manim animations
optimized for viewer engagement and retention.

## Animator Mindset

When generating animations, think like a professional motion graphics designer,
not a programmer. Prioritize:

- Visually appealing motion and smooth transitions
- Object transformations and morphs over simple fades
- Camera movement to guide attention
- Layered animations (multiple things happening with stagger)
- SVG illustrations from `assets/svg/` over primitive shapes
- Reusable animation patterns from `studio/`

## Scene Generation Process

When asked to generate a scene, ALWAYS follow this process:

1. **Define the visual goal.** What should the viewer understand visually?
2. **Decide camera movement.** Static, zoom, pan, or follow?
3. **Design the animation sequence.** What appears, transforms, moves, exits?
4. **Decide object transformations.** Morph, scale, recolor, reposition?
5. **Plan pacing.** Match narration rhythm. Vary speed for emphasis.
6. **Plan transitions.** Connect this scene to the next smoothly.
7. **Then generate Manim code.**

Do NOT jump straight to writing Manim code. Design first.

## Mandatory Rules

- Never leave the screen static for more than 3 seconds
- Always animate new objects (FadeIn, Write, Create — never just `self.add()`)
- Always animate object exits (FadeOut, Uncreate — never just `self.remove()`)
- Avoid text-only scenes — always pair text with visuals
- Use SVG illustrations whenever appropriate
- Use brand colors from `studio/styles.py` consistently
- Limit on-screen text to 2 lines maximum at once
- Use stagger delays (0.2s) when revealing lists or groups
- Camera movement should serve a purpose (don't move for no reason)
- Transitions between scenes must be smooth (never abrupt cuts)

## Code Standards

- Always inherit from `StudioScene` (from `studio/base.py`)
- Always import styles: `from studio.styles import *`
- Use `brand_text()`, `brand_title()`, `brand_code()` — never raw Manim Text()
- Use timing constants (FADE_NORMAL, PAUSE_MEDIUM) — never magic numbers
- Use position constants (POS_TITLE, POS_CENTER) — never raw coordinates
- Use `self.pause_beat()`, `self.pause_medium()` — never raw `self.wait(0.5)`

## File References

- #[[file:ANIMATION_GUIDE.md]] — Full animation quality guidelines
- #[[file:studio/styles.py]] — Brand colors, fonts, timing constants
- #[[file:studio/base.py]] — StudioScene base class
- #[[file:prompts/guidelines.md]] — Brand voice and content rules

## Optimization Target

Optimize every animation decision for **viewer retention**, not code elegance.
A viewer who stays engaged for 3 minutes is worth more than clean code.
