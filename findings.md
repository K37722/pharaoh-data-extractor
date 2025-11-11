# Total War Pharaoh Dynasties - Data Exploration Findings

**Explored Path:** `/Users/jensholm/Library/Application Support/Steam/steamapps/common/Total War PHARAOH DYNASTIES/TotalWarPharaohDynastiesData/data`

## File Statistics

- **Total Files:** 346
- **File Types:** 9
- **Pack Files:** 37

## File Categories (Top 10)

| Extension | Count |
|-----------|-------|
| `.png` | 202 |
| `.cur` | 93 |
| `.pack` | 37 |
| `.txt` | 4 |
| `.no_extension` | 3 |
| `.xml` | 3 |
| `.dds` | 2 |
| `.json` | 1 |
| `.esf` | 1 |

## Accessible Files

- `manifest.txt`
- `language.txt`
- `feral/manifest.txt`
- `localisation/en/language.txt`
- `feral/default_keys_mac.xml`
- `text/credits.xml`
- `text/default_keys.xml`
- `feral/news.json`
- `.DS_Store`
- `campaigns/.DS_Store`
- `text/build_info`

## Pack Files (Largest 10)

| Size (MB) | File |
|-----------|------|
| 10928.6 | `units.pack` |
| 10723.0 | `terrain.pack` |
| 6932.9 | `models.pack` |
| 6908.9 | `variants.pack` |
| 6752.7 | `variants2.pack` |
| 6531.7 | `terrain2.pack` |
| 3985.1 | `ui.pack` |
| 3052.2 | `movies.pack` |
| 2953.4 | `audio.pack` |
| 2816.7 | `terrain4.pack` |

## Next Steps

1. **Install RPFM** - Tool to extract .pack files
2. **Extract key .pack files** - Focus on largest files likely containing unit data
3. **Locate unit tables** - Look for database tables with unit stats
4. **Parse extracted data** - Build parser for extracted tables
