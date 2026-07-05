# Production Workflow

How videos are produced from idea to export.
This defines the order of operations and what each stage produces.

## Pipeline Stages

```
1. Topic Validation → 2. Pre-Production → 3. Script → 4. Storyboard →
5. Animation Design → 6. Manim Code → 7. Voice → 8. Render →
9. Subtitles → 10. Quality Review → 11. Export
```

## Stage Details

### 1. Topic Validation (Human + AI)

Before committing to a video, validate:
- Does this topic have a large potential audience?
- Is there a curiosity hook? ("Wait... really?")
- Can it be explained visually with animation?
- Is it evergreen (views for years)?
- Can it fit in 3-4 minutes?

Output: Go/no-go decision.

### 2. Pre-Production (AI generates, human reviews)

Produce:
- 10 clickable title options
- 5 thumbnail concepts
- Video outline with hook, retention plan, and structure

### 3. Script Writing (AI drafts, human edits)

Rules:
- Conversational tone, simple English, short sentences
- Hook in first 5-10 seconds (never "Hello everyone")
- One concept per video
- Every sentence must be animatable
- Natural humor, no filler
- Refer to #[[file:.kiro/steering/youtube-strategy.md]] for full script rules

### 4. Storyboard (AI generates, human approves)

For each scene:
- What the viewer sees every second
- Object entrances, movements, exits
- Camera behavior
- Timing aligned to narration

### 5. Animation Design (AI generates)

Translate storyboard into technical plan:
- Which Manim objects and SVGs
- Animation sequence with timestamps
- Required assets from manifest
- Transitions between scenes

### 6. Manim Code (AI generates, may need human fixes)

Write scene classes following coding-standards.md.
Reference the storyboard for timing and animation-quality.md for technique.

### 7-11. Automated Pipeline

```bash
make produce v=NNN_slug
```

This runs: voice → render → subtitles → (quality review when implemented) → export.

## Human Touchpoints

| Stage | Human Involvement | Time |
|-------|-------------------|------|
| Topic selection | Decision | 1 min |
| Research review | Verify flagged claims | 3 min |
| Script edit | Refine AI draft | 10-15 min |
| Storyboard review | Approve visual plan | 5 min |
| Scene review | Check for issues | 5-10 min |
| Quality review | Final approval | 2 min |
| **Total** | | **~30 min/video** |

## Status Tracking

Video status in `video.yaml` progresses through:
```
draft → scripted → storyboarded → animated → rendered → published
```

Update status as each stage completes.

## Automation Boundary

- Stages 7-11 are fully automated (no human needed)
- Stages 3-6 are AI-generated with human review
- Stages 1-2 are human decisions assisted by AI

The goal is ~80% automation by time, with human effort focused on creative decisions only.
