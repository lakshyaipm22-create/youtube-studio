# Assets

Shared assets used across all videos.

## Structure

```
assets/
├── svg/              # SVG illustrations (the core visual library)
│   ├── people/       # Characters, avatars, teams
│   ├── business/     # Office, meetings, presentations
│   ├── finance/      # Money, charts, banking
│   ├── technology/   # Computers, phones, code, servers
│   ├── science/      # Lab, atoms, experiments
│   ├── maps/         # World maps, country outlines
│   ├── icons/        # UI icons, symbols, logos
│   └── arrows/       # Directional arrows, pointers
├── fonts/            # Brand typography files (.ttf, .otf)
├── images/           # Raster images (logos, backgrounds, photos)
├── music/            # Background music tracks
└── sounds/           # Sound effects (whoosh, click, pop)
```

## Rules

1. **Shared assets only.** If an asset is used by ONE video, put it in `videos/NNN/assets/`.
2. **SVGs are preferred** over raster images for Manim (they scale perfectly).
3. **Name files descriptively:** `person_coding_laptop.svg`, not `img_003.svg`.
4. **Keep music/sounds small.** Use MP3 for music, WAV for short sound effects.

## Recommended Free SVG Sources

- [unDraw](https://undraw.co/) — Free illustrations, customizable colors
- [Storyset](https://storyset.com/) — Animated/static illustrations
- [SVG Repo](https://www.svgrepo.com/) — 500k+ free SVG icons/illustrations
- [Heroicons](https://heroicons.com/) — Clean UI icons
- [Tabler Icons](https://tabler.io/icons) — 5000+ open source icons
- [Simple Icons](https://simpleicons.org/) — Brand/logo icons

## Fonts to Install

Download and place in `assets/fonts/`:
- [Inter](https://rsms.me/inter/) — Primary body font
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/) — Code font
