# Animation Quality Guide

This document defines the animation standards for every video in this channel.
Kiro and all contributors must follow these rules when generating Manim scenes.

---

## Core Philosophy

**Think like an animator, not a programmer.**

Prioritize viewer engagement over minimizing code. Prefer visually appealing motion,
object transformations, camera movement, layered animations, SVG illustrations,
and reusable patterns over static text and primitive shapes.

---

## The Golden Rule

> Before writing any Manim code, first decide what the viewer should be
> looking at every single second of the scene.

---

## Scene Design Process

For every scene, follow this order:

1. **Define the visual goal.** What should the viewer understand after watching?
2. **Decide camera movement.** Static, zoom, pan, or follow?
3. **Decide the animation sequence.** What appears, transforms, moves, and exits?
4. **Decide object transformations.** Morph, scale, recolor, reposition?
5. **Decide pacing.** Fast energy or slow emphasis?
6. **Decide transitions.** How does this scene connect to the next?
7. **Then — and only then — write Manim code.**

---

## Animation Rules

### Timing & Pacing

- Never leave the screen static for more than 3 seconds.
- Every new concept must introduce a visual change.
- Animate objects IN (entrance) and OUT (exit) — don't just `self.add()`.
- Use stagger delays (0.2s) when revealing lists or groups.
- Match animation speed to narration rhythm.

### Visual Hierarchy

- One focal point at a time. Don't compete for attention.
- Dim or shrink non-active elements (don't remove them).
- Use size to indicate importance (bigger = more important).
- Use color to indicate category or state.
- Use position consistently (title top, content center, captions bottom).

### Motion & Transformation

- Prefer `Transform` and `ReplacementTransform` over `FadeOut` + `FadeIn`.
- Objects should move WITH purpose (toward related objects, along logical paths).
- Use `shift` animations to guide the eye in a direction.
- Avoid teleporting objects (always animate position changes).
- Use `rate_func` variations for personality (ease_in, ease_out, there_and_back).

### SVG Illustrations

- Use SVG illustrations whenever possible instead of primitive shapes.
- SVGs from `assets/svg/` make videos look professional instantly.
- Animate SVGs: fade in, scale up, slide in from sides.
- Combine SVGs with text labels and arrows for context.
- Match SVG color to brand palette using `.set_color()`.

### Text & Typography

- Avoid text-only scenes. Always pair text with visuals.
- Limit on-screen text to 2 lines maximum at once.
- Use `brand_text()` and `brand_title()` from styles.py.
- Animate text appearing (Write, FadeIn with shift) — never instant.
- Remove text when it's no longer relevant.

### Camera

- Camera should feel natural, not jerky.
- Subtle zoom (1.0 → 1.2) draws attention to detail.
- Pan to follow a sequence or timeline.
- Reset camera before new sections.
- Don't overuse camera movement — it's seasoning, not the meal.

### Transitions Between Scenes

- Every scene should end with a clear exit animation.
- Use `self.fade_out_all()` as default transition.
- For related scenes: transform key object into next scene's starting point.
- For new topics: full fade to dark + brief pause + new entrance.
- Never cut abruptly (no jarring instant switches).

### Color

- Use brand colors from `studio/styles.py` consistently.
- BRAND_PRIMARY (#6C63FF) — main elements, highlights.
- BRAND_ACCENT (#00D9A6) — success, tips, positive.
- BRAND_SECONDARY (#FF6584) — attention, contrast.
- BRAND_WARNING (#FFB347) — caution, gotchas.
- BRAND_ERROR (#FF4444) — mistakes, anti-patterns.
- Dim inactive elements with BRAND_MUTED (#8892B0).

---

## What NOT to Do

- Don't create "slide deck" animations (static text + bullet points).
- Don't show a wall of code all at once — reveal line by line.
- Don't use Manim defaults for colors/fonts — always use brand styles.
- Don't leave objects on screen after they're discussed.
- Don't animate everything at the same speed — vary for emphasis.
- Don't forget the exit animation.
- Don't use primitive circles/squares when an SVG would be clearer.

---

## Viewer Retention Optimization

- First 5 seconds must have motion (hooks viewer).
- Change something visual every 3-5 seconds minimum.
- Build complexity gradually (simple → detailed).
- Summarize with clear visual recap before transitions.
- End scenes on a visual "question" that the next scene answers.

---

## Quality Checklist

Before rendering a scene, verify:

- [ ] Every object has an entrance animation
- [ ] Every object has an exit animation
- [ ] No static frames longer than 3 seconds
- [ ] Brand colors used consistently
- [ ] Text is readable (font size, contrast, screen time)
- [ ] SVGs used where appropriate
- [ ] Camera movement serves a purpose
- [ ] Transition to next scene is smooth
- [ ] Pacing matches narration timing
