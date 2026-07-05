# Script Writer Prompt Template

Use this prompt to generate a first draft of a video script.

---

## Prompt

Write a YouTube video script about **{TOPIC}**.

**Target audience:** {AUDIENCE — e.g., beginners learning programming}
**Video length:** {DURATION — e.g., 3-4 minutes}
**Tone:** Educational, clear, engaging. Like explaining to a smart friend.
**Series context:** {SERIES — e.g., Part 3 of Python Basics}

### Structure requirements:

1. **Hook (first 10 seconds):** Start with a question, surprising fact, or relatable problem. Never start with "In this video..."
2. **Intro (15 seconds):** Brief context. What will the viewer learn?
3. **Main content (2-3 minutes):** Break into 2-4 clear sections. Each section should be one key idea.
4. **Recap (15 seconds):** Summarize the 2-3 most important takeaways.
5. **Outro (10 seconds):** CTA (subscribe, next video teaser).

### Script format:

```
# Scene 1: Hook
[VISUAL: description of what the viewer sees]
NARRATION: What the narrator says.

# Scene 2: Introduction
[VISUAL: description]
NARRATION: ...
```

### Rules:
- Write for spoken delivery (short sentences, natural rhythm)
- Each scene should be self-contained (one idea per scene)
- Include [VISUAL] directions — describe what should be animated
- Keep vocabulary simple but not condescending
- No filler phrases ("um", "basically", "you know")
- Every sentence should earn its place
