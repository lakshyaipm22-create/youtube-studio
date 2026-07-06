# Asset Management

## Build With Manim (Primary Approach)

For Shorts, build ALL visuals with Manim primitives:
- Rectangles, Circles, Lines, Arrows, Polygons
- Text with bold/italic/color variation
- VGroups composed into objects (buildings, phones, planets)
- BraceBetweenPoints for measurements

Faster than finding SVGs. Consistent style. Works every time.

## Color Palette (Copy Into Every Video)

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

## Proven Visual Patterns for Shorts

1. **Big number reveal**: Text(font_size=80+) with FadeIn(scale=1.5)
2. **Scale comparison**: Tiny object next to huge object (vertical stack)
3. **Growing bar**: Rectangle + GrowFromEdge (vertical growth works great for vertical video)
4. **Earth-Moon line**: Two circles + Line + BraceBetweenPoints
5. **Grid of objects**: arrange_in_grid (doors, computers, etc.)
6. **Quote card**: RoundedRectangle + italic text
7. **Cash stack**: Green rectangles staggered with LaggedStart
8. **Stretching object**: Rectangle that stretches (paper fold)

## Vertical Layout Tips

- Stack objects TOP to BOTTOM (not left-right)
- Use UP * 5-6 for top, DOWN * 5-6 for bottom
- Center content in middle 70% (avoid edge clipping)
- Bigger everything (phone screens are small)

## When to Use SVGs

Only if Manim primitives genuinely can't represent the concept.
For 45-second Shorts, simple geometry almost always works better.
