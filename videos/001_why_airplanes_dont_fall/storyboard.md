# Storyboard: Why Airplanes Don't Fall

## Scene 1: Intro (Hook)
Duration: 15s

Visual Goal: Create awe at the impossibility of flight, trigger immediate curiosity.

| Time | Element | Animation | Notes |
|------|---------|-----------|-------|
| 0.0s | "400" text (giant) | Entrance: scale up from zero | FONT_SIZE_HERO, BRAND_LIGHT |
| 1.5s | "TONS" text | Entrance: FadeIn slam from right | Next to 400, BRAND_SECONDARY |
| 3.0s | 80 elephant icons (grid) | Entrance: stagger FadeIn, 0.2s delay | Small icons filling area below |
| 6.0s | Elephants morph | Transform: VGroup morphs into 747 silhouette | Satisfying visual payoff |
| 8.0s | "And somehow... it flies" | Entrance: Write | Below plane, BRAND_LIGHT |
| 10.0s | "10,000 planes right now" | Entrance: FadeIn shift up | Supporting text |
| 12.0s | "How?" text | Entrance: FadeIn scale 1.5x | Center, BRAND_PRIMARY, dramatic |
| 14.0s | All elements | Exit: fade_out_all | Clean transition to next scene |

SVGs Needed: boeing-747-silhouette.svg, elephant-icon.svg
Camera: Static, subtle zoom on "How?" at 12s
Transition to Next: Fade to dark, 0.3s pause

## Scene 2: WindAndWing (The Wrong Answer + Hand Analogy)
Duration: 45s

Visual Goal: Debunk the textbook explanation, then introduce the correct intuition through the hand-out-window analogy.

| Time | Element | Animation | Notes |
|------|---------|-----------|-------|
| 0.0s | "What Your Teacher Said" title | Entrance: Write | POS_TITLE |
| 2.0s | Wing cross-section (ellipse) | Entrance: Create (draw outline) | Center, BRAND_LIGHT fill |
| 4.0s | Top airflow arrow (curved) | Entrance: GrowArrow | CurvedArrow, BRAND_PRIMARY |
| 5.5s | Bottom airflow arrow (straight) | Entrance: GrowArrow | Straight, BRAND_MUTED |
| 7.0s | "Longer path = faster" label | Entrance: Write | Small text near top arrow |
| 9.0s | Red "X" stamp | Entrance: FadeIn + scale bounce | Over diagram, rotated, BRAND_ERROR |
| 11.0s | Upside-down plane icon | Entrance: FadeIn from right | Proving the point |
| 13.0s | Wing diagram + wrong stamp | Exit: FadeOut | Clear the slate |
| 15.0s | Car silhouette driving | Entrance: slide in from left | Simple car shape |
| 17.0s | Hand out window (flat rectangle) | Entrance: FadeIn | Positioned at car window |
| 19.0s | Hand tilts upward | Transform: Rotate 15 degrees | Key moment, slight zoom |
| 21.0s | Air deflection arrows (3x down) | Entrance: stagger GrowArrow | Showing air pushed down |
| 23.0s | Lift arrow (up, thick) | Entrance: GrowArrow + label | BRAND_ACCENT, "LIFT" label |
| 26.0s | "You just created lift" text | Entrance: Write | POS_FOOTER |
| 29.0s | Hand morphs into wing shape | Transform: smooth morph | Arrows persist through morph |
| 32.0s | Wing with same arrows | Transform: context shift | Now it looks like aircraft wing |
| 35.0s | All elements | Exit: fade_out_all | Prepare for Newton |

SVGs Needed: car-silhouette.svg, upside-down-plane.svg
Camera: Subtle zoom on hand-tilt moment (19s), reset at 29s
Transition to Next: Fade, 0.3s dark pause

## Scene 3: LiftExplained (Newton + Bernoulli)
Duration: 40s

Visual Goal: Show both Newton's law and Bernoulli's principle, then merge them into the unified explanation.

| Time | Element | Animation | Notes |
|------|---------|-----------|-------|
| 0.0s | "Newton's Third Law" title | Entrance: Write | POS_TITLE, BRAND_PRIMARY |
| 2.0s | Wing shape (center) | Entrance: Create | Simple clean wing |
| 4.0s | Blue arrows deflecting air DOWN | Entrance: stagger GrowArrow | Below wing, BRAND_PRIMARY |
| 6.0s | Green arrow pushing wing UP | Entrance: GrowArrow | Above wing, BRAND_ACCENT |
| 7.0s | "Action" label (down) | Entrance: FadeIn | Near blue arrows |
| 8.0s | "Reaction" label (up) | Entrance: FadeIn | Near green arrow |
| 10.0s | "This is lift" text | Entrance: Write | Below diagram |
| 12.0s | Reaction arrow pulses | Transform: scale 1.3x then back | Emphasis |
| 14.0s | Newton section | Transform: slides to left half | Making room |
| 16.0s | Vertical divider line | Entrance: Create | Center divider |
| 17.0s | "Bernoulli's Principle" title | Entrance: Write | Right side, BRAND_SECONDARY |
| 19.0s | Wing with pressure gradient | Entrance: FadeIn | Blue above (low P), red below (high P) |
| 22.0s | Pressure labels | Entrance: stagger FadeIn | "Low pressure" / "High pressure" |
| 25.0s | Divider line | Exit: Uncreate | Preparing to merge |
| 27.0s | Both diagrams merge | Transform: slide together onto one wing | Key visual payoff |
| 30.0s | Unified wing (both forces shown) | Transform: combined arrows + colors | Everything together |
| 33.0s | "The real answer: BOTH" text | Entrance: FadeIn scale emphasis | Center, BRAND_PRIMARY, large |
| 36.0s | Pause for absorption | Hold | Let viewer process |
| 38.0s | All elements | Exit: fade_out_all | Clean transition |

SVGs Needed: None (all Manim primitives: arrows, shapes, gradients)
Camera: Static throughout, zoom on merge moment (27s)
Transition to Next: Fade to dark

## Scene 4: MythBust (Equal Transit Time + Angle of Attack)
Duration: 35s

Visual Goal: Explicitly debunk the equal transit time myth with evidence, then show what really matters (angle of attack) and what happens when it goes wrong (stall).

| Time | Element | Animation | Notes |
|------|---------|-----------|-------|
| 0.0s | "The Myth" title | Entrance: Write | POS_TITLE |
| 2.0s | Old wing diagram returns | Entrance: FadeIn | Same textbook style |
| 3.0s | Air particles split at leading edge | Entrance: animated dots | Moving along top and bottom |
| 5.0s | Top particles arrive FIRST | Transform: top dots reach end faster | Key visual proof |
| 7.0s | "They DON'T meet up!" text | Entrance: FadeIn | BRAND_ERROR, emphasis |
| 9.0s | "Equal Transit Time" strikethrough | Transform: line draws through text | Debunked |
| 11.0s | "Debunked by NASA" citation | Entrance: FadeIn | Small, credible |
| 13.0s | Old diagram | Exit: FadeOut | Moving on |
| 15.0s | "Angle of Attack" title | Entrance: Write | New section |
| 17.0s | Wing at 0 degrees | Entrance: Create | Horizontal, small lift arrow |
| 19.0s | Wing rotates to 5 degrees | Transform: Rotate | Lift arrow grows |
| 21.0s | Wing rotates to 10 degrees | Transform: Rotate | Lift arrow grows more |
| 23.0s | Wing rotates to 15 degrees | Transform: Rotate | Approaching limit |
| 25.0s | Smooth airflow above wing | Exit: breaks into turbulent swirls | Airflow separation |
| 27.0s | Lift arrow collapses | Transform: shrink to zero | Dramatic loss of lift |
| 28.0s | "STALL" text | Entrance: FadeIn flash, BRAND_ERROR | Large, dramatic |
| 30.0s | Brief explanation text | Entrance: Write | "Too much angle = no lift" |
| 33.0s | All elements | Exit: fade_out_all | Transition to outro |

SVGs Needed: None (animated dots and arrows suffice)
Camera: Static, zoom in during stall sequence (23-28s)
Transition to Next: Fade to dark

## Scene 5: Outro (Recap + CTA)
Duration: 12s

Visual Goal: Leave the viewer with a clean mental model and a reason to subscribe.

| Time | Element | Animation | Notes |
|------|---------|-----------|-------|
| 0.0s | Clean wing diagram | Entrance: FadeIn | Final, elegant version |
| 1.0s | Newton arrows (down + up) | Entrance: stagger GrowArrow | Blue down, green up |
| 3.0s | Bernoulli gradient | Entrance: FadeIn | Blue above, red below |
| 4.0s | "Newton + Bernoulli" label | Entrance: Write | Below wing |
| 6.0s | Wing diagram | Exit: FadeOut upward | Satisfying exit |
| 7.0s | "Subscribe for more" text | Entrance: FadeIn shift up | BRAND_PRIMARY |
| 8.5s | "Next: Why Ships Don't Sink" | Entrance: FadeIn | BRAND_MUTED, teaser |
| 11.0s | All elements | Exit: FadeOut | Clean ending |

SVGs Needed: None
Camera: Static
Transition to Next: Fade to black (end of video)
