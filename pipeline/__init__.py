"""
YouTube Studio - Production Pipeline

Automation scripts for the complete video production workflow:
- new_video: Scaffold a new video folder
- voiceover: Generate narration audio from script
- subtitles: Generate SRT from audio
- render: Render Manim scenes
- export: Final assembly (stitch + mix + export)

Usage via Makefile:
    make new title="What is Python?"
    make voice v=001_what_is_python
    make render v=001_what_is_python
    make subs v=001_what_is_python
    make export v=001_what_is_python
    make produce v=001_what_is_python   # Full pipeline
"""
