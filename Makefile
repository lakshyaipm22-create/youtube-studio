# YouTube Studio - Production Commands
# Usage: make <command> [options]
#
# Examples:
#   make new title="What is Python?"
#   make new title="Variables" series=python-basics tags="python,beginner"
#   make preview v=001_what_is_python s=Intro
#   make render v=001_what_is_python
#   make voice v=001_what_is_python
#   make subs v=001_what_is_python
#   make export v=001_what_is_python
#   make produce v=001_what_is_python

.PHONY: new preview render render-4k voice subs export produce help

# === SCAFFOLDING ===

new: ## Create a new video folder: make new title="Title" [series=name] [tags="a,b"]
	python pipeline/new_video.py "$(title)" \
		$(if $(series),--series "$(series)") \
		$(if $(tags),--tags "$(tags)")

# === RENDERING ===

preview: ## Quick preview (480p): make preview v=VIDEO_FOLDER s=SceneName
	manim render -ql videos/$(v)/scenes.py $(s)

render: ## Render all scenes (1080p 60fps): make render v=VIDEO_FOLDER
	python pipeline/render.py $(v)

render-4k: ## Render all scenes (4K 60fps): make render-4k v=VIDEO_FOLDER
	python pipeline/render.py $(v) --quality 4k

render-scene: ## Render one scene (1080p): make render-scene v=VIDEO_FOLDER s=SceneName
	python pipeline/render.py $(v) --scene $(s)

# === AUDIO ===

voice: ## Generate voiceover: make voice v=VIDEO_FOLDER [engine=kokoro|edge]
	python pipeline/voiceover.py videos/$(v)/script.md \
		$(if $(engine),--engine $(engine))

voice-edge: ## Generate voiceover with Edge-TTS: make voice-edge v=VIDEO_FOLDER
	python pipeline/voiceover.py videos/$(v)/script.md --engine edge

# === SUBTITLES ===

subs: ## Generate subtitles from voiceover: make subs v=VIDEO_FOLDER
	python pipeline/subtitles.py output/$(v)/voiceover.wav

# === EXPORT ===

export: ## Final video export: make export v=VIDEO_FOLDER [music=path]
	python pipeline/export.py $(v) \
		$(if $(music),--music "$(music)")

export-subs: ## Export with burned subtitles: make export-subs v=VIDEO_FOLDER
	python pipeline/export.py $(v) --burn-subs

# === FULL PIPELINE ===

produce: ## Full pipeline (voice → render → subs → export): make produce v=VIDEO_FOLDER
	@echo "🎬 Starting full production pipeline for: $(v)"
	@echo ""
	make voice v=$(v)
	make render v=$(v)
	make subs v=$(v)
	make export v=$(v)
	@echo ""
	@echo "✅ Production complete: output/$(v)/final.mp4"

# === UTILITIES ===

list: ## List all videos and their status
	@echo "📹 Videos:"
	@ls -d videos/[0-9]* 2>/dev/null || echo "   No videos yet. Run: make new title=\"Your Title\""

clean: ## Remove output for a video: make clean v=VIDEO_FOLDER
	rm -rf output/$(v)
	@echo "🧹 Cleaned: output/$(v)"

clean-all: ## Remove ALL rendered output
	rm -rf output/
	@echo "🧹 Cleaned all output"

# === HELP ===

help: ## Show this help message
	@echo "YouTube Studio - Production Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Variables:"
	@echo "  v=VIDEO_FOLDER  Video folder name (e.g., 001_what_is_python)"
	@echo "  s=SCENE_NAME    Scene class name (e.g., Intro)"
	@echo "  title=TITLE     Video title for new videos"
	@echo "  series=NAME     Series name (optional)"
	@echo "  tags=TAGS       Comma-separated tags (optional)"
	@echo "  engine=ENGINE   TTS engine: kokoro or edge (optional)"
	@echo "  music=PATH      Background music file path (optional)"
