# Asset Management

## Primary Visual Approach: Build With Manim

For most videos, build visuals directly in Manim using composed shapes:
- Buildings: Rectangle + grid of small Rectangles (windows)
- Planets: Circle with fill_color and label
- Bar charts: Rectangles with GrowFromEdge
- People: Simplified geometric compositions
- Diagrams: Lines, Arrows, BraceBetweenPoints, labels

This is FASTER than finding/downloading SVGs and produces consistent style.

## When to Use External SVGs

Only when Manim primitives can't represent the concept:
- Detailed illustrations (animals, complex machinery)
- Brand logos
- Country maps
- Scientific diagrams too complex to build from shapes

## Asset Locations

| Type | Path | Notes |
|------|------|-------|
| Shared SVGs | `assets/svg/{category}/` | For reuse across videos |
| Video-specific | `videos/NNN/assets/` | One-off visuals |
| Music | `assets/music/` | Background tracks |
| Sounds | `assets/sounds/` | Effects (whoosh, ding) |

## Color Palette (Standard Across All Videos)

```python
BG = "#0e1116"        # Deep navy background
GOLD = "#F5C842"      # Emphasis, key numbers
TEAL = "#2DCDC6"      # Positive, actions
CORAL = "#FF6B6B"     # Danger, wrong, attention
SOFT_WHT = "#E8E8F0"  # Body text
MUTED = "#6B6B8A"     # Secondary info
PURPLE = "#7B5EA7"    # Categories
GREEN = "#4CAF7D"     # Success, correct
```

Copy this palette into every video file. Consistency = brand recognition.

## Proven Visual Patterns (From Reference Videos)

1. **Scale comparison**: Object A next to Object B (building vs stack)
2. **Earth-Moon diagram**: Two circles, line between, BraceBetweenPoints below
3. **Growing bars**: Rectangle with GrowFromEdge, year labels below
4. **Dot spread**: Dots multiplying outward in rings (viral growth)
5. **Paper fold**: Rectangle that stretches vertically in a loop
6. **Number reveal**: Large bold Text with FadeIn(scale=1.5)
7. **Quote card**: RoundedRectangle background + italic text
8. **Comparison grid**: Small rectangles in grid (100 doors, pixels)

## Free Music Sources

- YouTube Audio Library (pre-cleared)
- Pixabay Music (CC0)
- Uppbeat (free tier)
