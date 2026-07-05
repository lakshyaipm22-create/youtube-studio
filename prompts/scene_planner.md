# Scene Planner Prompt Template

Use this prompt after the script is written to design the visual animation.

---

## Prompt

I have a video script (below). Design the Manim animation for each scene.

**Script:**
{PASTE SCRIPT HERE}

**Available components:**
- `studio/base.py` — StudioScene (dark background, standard methods)
- `studio/intro.py` — IntroScene (branded intro with title)
- `studio/outro.py` — OutroScene (subscribe CTA)
- `studio/styles.py` — Brand colors, fonts, timing constants
- `assets/svg/` — SVG illustrations (people, tech, icons, arrows)

### For each scene, provide:

1. **Visual Goal:** What should the viewer be looking at? What's the key visual message?
2. **Animation Sequence:** Step-by-step what appears, transforms, or moves.
3. **Timing:** How long each animation takes (match narration pacing).
4. **Camera:** Any camera movements (zoom, pan, shift focus).
5. **Objects:** Which Manim objects/SVGs to use.
6. **Transitions:** How to move between this scene and the next.

### Design principles:
- Never leave the screen static for more than 3 seconds
- Every new concept gets a visual change
- Use SVG illustrations over primitive shapes when possible
- Animate IN (entrance) and animate OUT (exit) every element
- Maintain clear visual hierarchy (one focal point at a time)
- Use brand colors from styles.py consistently
- Prefer transformations and morphs over simple fade-in/fade-out

### Output format:

```
## Scene 1: [Name]
Duration: Xs

Visual Goal: [What the viewer should understand visually]

Animation Sequence:
1. [0.0s] Object A fades in at center
2. [0.5s] Object B draws in from left
3. [1.5s] Object A transforms into Object C
4. [2.5s] Camera zooms slightly toward C
5. [3.5s] Everything fades out

Manim Objects: Text, SVGMobject, Arrow, VGroup
SVGs needed: technology/server.svg, arrows/right.svg
Transition to next: Fade out all, brief pause
```
