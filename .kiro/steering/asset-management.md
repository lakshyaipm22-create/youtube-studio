# Asset Management

Rules for organizing, finding, and using assets across the project.

## Asset Locations

| Type | Path | Tracked in Git? |
|------|------|----------------|
| SVG illustrations | `assets/svg/{category}/` | Yes |
| Fonts | `assets/fonts/` | Yes (unless > 10MB) |
| Background music | `assets/music/` | Yes (unless > 10MB) |
| Sound effects | `assets/sounds/` | Yes |
| Raster images | `assets/images/` | Yes |
| Video-specific assets | `videos/NNN/assets/` | Yes |
| Rendered output | `output/` | No (gitignored) |
| Generated audio | `output/` | No (gitignored) |

## SVG Library Categories

```
assets/svg/
├── people/       # Characters, avatars, teams
├── business/     # Office, presentations, meetings
├── finance/      # Money, charts, banking
├── technology/   # Computers, servers, phones, code
├── science/      # Lab, atoms, biology, chemistry
├── maps/         # World maps, country outlines
├── icons/        # UI icons, symbols, checkmarks
└── arrows/       # Directional arrows, pointers
```

## SVG-First Rule

When a concept can be represented visually:
1. Check `assets/manifest.yaml` for existing SVG
2. If match found: use it
3. If no match: check if an appropriate free SVG exists online
4. If nothing suitable: use Manim primitives as last resort

SVGs instantly make videos look professional. Primitives look amateurish.

## Asset Manifest

`assets/manifest.yaml` is the AI-readable index of all reusable assets.

Every SVG entry has:
- `path`: file path relative to repo root
- `keywords`: terms that would trigger this asset's use
- `colors`: brand colors it uses
- `default_height`: suggested Manim height

When generating scenes, always consult the manifest to find appropriate visuals.
When adding new SVGs, always add an entry to the manifest.

## Naming Conventions

- SVG files: `descriptive_name.svg` (snake_case, no numbers)
- Music files: `mood_description.mp3` (e.g., `chill_ambient.mp3`)
- Sound effects: `action_description.wav` (e.g., `whoosh_fast.wav`)
- Fonts: original name from source (e.g., `Inter-Regular.ttf`)

## Shared vs. Video-Specific

- If used by 2+ videos → lives in `assets/` (shared)
- If used by exactly 1 video → lives in `videos/NNN/assets/` (specific)
- If something starts video-specific but gets reused → move it to shared

## Recommended Free Sources

- SVG illustrations: unDraw, Storyset, SVG Repo
- Icons: Heroicons, Tabler Icons, Simple Icons
- Music: YouTube Audio Library, Pixabay Music
- Sound effects: Pixabay Sound Effects, Freesound.org
- Fonts: Google Fonts (Inter, JetBrains Mono)
