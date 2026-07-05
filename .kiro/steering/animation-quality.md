# Animation & Visual Design Standards

This file governs how animations are designed and coded.
It is subordinate to `youtube-strategy.md` — every animation decision serves viewer retention.

## Core Principle

Think like an animator, not a programmer.
Prioritize viewer engagement over minimizing code.

## Scene Design Process (Mandatory)

Before writing ANY Manim code, complete these steps:

1. Define the visual goal — what should the viewer understand?
2. Decide camera movement — static, zoom, pan, or follow?
3. Design the animation sequence — what appears, transforms, moves, exits?
4. Decide object transformations — morph, scale, recolor, reposition?
5. Plan pacing — match narration rhythm, vary speed for emphasis
6. Plan transitions — smooth connection to next scene
7. THEN write Manim code

## Visual Rules

- Never leave the screen static for more than 3 seconds
- Always animate entrances (FadeIn, Write, Create — never `self.add()`)
- Always animate exits (FadeOut, Uncreate — never `self.remove()`)
- Avoid text-only scenes — always pair text with visuals
- Use SVG illustrations from `assets/svg/` over primitive shapes
- Limit on-screen text to 2 lines maximum
- Use stagger delays (0.2s) when revealing groups
- Prefer Transform/ReplacementTransform over FadeOut + FadeIn
- Objects move with purpose (toward related objects, along logical paths)
- One focal point at a time — don't compete for attention

## Camera Rules

- Subtle zoom (1.0 → 1.2) to draw attention
- Pan to follow sequences or timelines
- Reset camera before new sections
- Never move the camera without purpose

## Transition Rules

- Every scene ends with a clear exit animation
- Default: `self.fade_out_all()`
- Related scenes: transform key object into next scene's starting point
- New topics: full fade to dark + brief pause + new entrance
- Never cut abruptly

## SVG-First Policy

- Use SVG illustrations whenever the concept can be represented visually
- Check `assets/manifest.yaml` for available assets before creating primitives
- Animate SVGs: fade in, scale up, slide in
- Match SVG colors to brand palette with `.set_color()`

## What NOT to Do

- Don't create "slide deck" animations (static text + bullet points)
- Don't show a wall of code all at once — reveal progressively
- Don't use Manim default colors/fonts — always use brand styles
- Don't leave objects on screen after they're discussed
- Don't animate everything at the same speed — vary for emphasis
- Don't use primitive circles/squares when an SVG would be clearer

## Viewer Retention Visual Rules

- First 5 seconds must have motion
- Change something visual every 3-5 seconds
- Build complexity gradually (simple → detailed)
- End scenes on a visual "question" the next scene answers

## Pre-Render Checklist

Before committing a scene:
- [ ] Every object has entrance + exit animation
- [ ] No static frames > 3 seconds
- [ ] Brand colors used consistently
- [ ] Text readable (font size, contrast, screen time)
- [ ] SVGs used where appropriate
- [ ] Camera movement serves a purpose
- [ ] Pacing matches narration timing

## File References

- #[[file:ANIMATION_GUIDE.md]] — Detailed guide (extended reference)
- #[[file:studio/styles.py]] — Brand colors, fonts, timing constants
- #[[file:studio/base.py]] — StudioScene base class
