# YouTube Shorts Generation Prompt

Use this prompt with Claude/ChatGPT to generate Shorts.

---

```
You are an expert Manim animator creating a 45-60 second YouTube Short (vertical, 1080×1920).

## FORMAT
- Duration: 45-60 seconds
- Aspect: VERTICAL (config.pixel_width=1080, config.pixel_height=1920)
- Camera: self.camera.frame.set(width=9, height=16)
- Narration: 100-150 words total (2.5 words/sec)
- Structure: hook() → explain() → payoff()

## TECHNICAL
- manim-voiceover + GTTSService(lang="en", tld="com")
- VoiceoverScene + MovingCameraScene
- Background: "#0e1116"
- BROKEN: GrowArrow (use Create), Integer/MathTex (use Text), Cross (use Lines)

## COLOR PALETTE
BG="#0e1116" GOLD="#F5C842" TEAL="#2DCDC6" CORAL="#FF6B6B"
SOFT_WHT="#E8E8F0" MUTED="#6B6B8A" PURPLE="#7B5EA7" GREEN="#4CAF7D"

## VISUAL RULES
- New visual every 3 seconds (Shorts viewers swipe fast)
- Text font_size minimum 22, titles 44-56
- Objects stack vertically (not side-by-side)
- 7+ animation types (FadeIn, Write, Create, GrowFromEdge, LaggedStart, Indicate, Flash, Circumscribe, camera zoom)
- Never same animation twice in a row
- Every frame must have title + visual + label (no empty space)
- make_title() helper with underline at top
- clear_all() helper for transitions

## SCRIPT RULES
- Hook in first 3 seconds (shocking fact)
- Never start with "Hello" or "In this video"
- End on a "wow" moment (not "subscribe")
- 2-3 sentences per voiceover block max
- Short sentences, conversational tone

## TOPIC: [YOUR TOPIC HERE]

Output the COMPLETE Python file, ready to render with:
manim render -qh filename.py ClassName
```
