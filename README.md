# Total War PHARAOH DYNASTIES - Data Extractor

A Python-based tool for managing and exploring pack files from Total War PHARAOH DYNASTIES.

## Overview

This project provides utilities to work with the 37 pack files from Total War PHARAOH DYNASTIES. It includes:

- **Structured JSON data** with categorized pack files
- **Pack file manager** for searching, listing, and analyzing pack files
- **Extraction tools** for extracting and searching inside pack files
- **Quick search guide** for finding specific game data
- **Language support** for 12 different languages

## Pack Files Inventory

### Total Pack Files: 37

Located in: `/TotalWarPharaohDynastiesData/data/`

### Categories

| Category | Files | Description |
|----------|-------|-------------|
| **Audio** | 14 | Audio files for different languages and game sounds |
| **Localization** | 12 | Localization files for different languages |
| **Terrain** | 4 | Terrain and map data |
| **Data** | 3 | Core game data and database files |
| **Visual** | 5 | Models, units, UI, and visual assets |
| **Variants** | 2 | Unit and model variants |
| **Core** | 2 | Core game files and boot data |

### Supported Languages

- 🇧🇷 Brazilian Portuguese (br)
- 🇨🇳 Chinese - Simplified (cn)
- 🇨🇿 Czech (cz)
- 🇬🇧 English (en)
- 🇫🇷 French (fr)
- 🇩🇪 German (ge)
- 🇮🇹 Italian (it)
- 🇰🇷 Korean (kr)
- 🇵🇱 Polish (pl)
- 🇪🇸 Spanish (sp)
- 🇹🇷 Turkish (tr)
- 🇹🇼 Chinese - Traditional (zh)

## Files

### Data Files
- `pack_files.json` - Structured data containing all pack files organized by category

### Tools
- `pack_files_manager.py` - Manage and list pack files by category/language
- `pack_extractor.py` - Extract and search data from pack files
- `quick_search.py` - Interactive guide to find specific game data

### Documentation
- `README.md` - This file
- `EXTRACTION_GUIDE.md` - Detailed guide for extracting and searching pack files
- `CLAUDE.md` - Development workflow rules

## Quick Start

### 1. Find What You're Looking For

Not sure which pack files to extract? Use the interactive guide:

```bash
python3 quick_search.py
```

Or get quick recommendations:

```bash
python3 quick_search.py unit stats
python3 quick_search.py buildings
python3 quick_search.py faction data
```

### 2. Extract Pack Files

See `EXTRACTION_GUIDE.md` for detailed instructions.

**Requirements:**
- RPFM (Rusted PackFile Manager): https://github.com/Frodo45127/rpfm/releases

**Quick extraction:**
```bash
# List pack files with sizes
python3 pack_extractor.py list --game-dir /path/to/TotalWarPharaohDynastiesData/data/

# Verify pack files
python3 pack_extractor.py verify --game-dir /path/to/game/data/

# Extract specific pack (requires RPFM)
python3 pack_extractor.py extract data_db.pack --rpfm /path/to/rpfm
```

### 3. Search Extracted Data

```bash
# Search for specific term
python3 pack_extractor.py search "unit_name"

# Search in specific file types
python3 pack_extractor.py search "building" --ext .xml .tsv

# Find all data tables
python3 pack_extractor.py tables

# Generate extraction report
python3 pack_extractor.py report
```

## Usage

### Pack Files Manager

List and manage pack files without extraction:

```bash
# Show summary
python3 pack_files_manager.py
```

### List All Pack Files

```bash
python3 pack_files_manager.py list
```

### Browse by Category

```bash
# List available categories
python3 pack_files_manager.py category

# List files in a specific category
python3 pack_files_manager.py category audio
python3 pack_files_manager.py category terrain
python3 pack_files_manager.py category data
```

### Browse by Language

```bash
# List available languages
python3 pack_files_manager.py language

# List all files for a specific language
python3 pack_files_manager.py language en
python3 pack_files_manager.py language fr
```

### Search for Files

```bash
python3 pack_files_manager.py search terrain
python3 pack_files_manager.py search audio
python3 pack_files_manager.py search local
```

### Get Statistics

```bash
python3 pack_files_manager.py stats
```

## Python API

You can also use the `PackFilesManager` class in your own Python scripts:

```python
from pack_files_manager import PackFilesManager

# Initialize the manager
manager = PackFilesManager()

# Get all pack files
all_files = manager.get_all_files()

# Get files by category
audio_files = manager.get_files_by_category('audio')
terrain_files = manager.get_files_by_category('terrain')

# Get files by language
english_files = manager.get_files_by_language('en')
print(f"English audio: {english_files['audio']}")
print(f"English localization: {english_files['localization']}")

# Search for specific files
results = manager.search_files('terrain')

# Get statistics
stats = manager.get_statistics()
print(f"Total files: {stats['total_files']}")

# Print summary
manager.print_summary()
```

## Complete Pack Files List

### Audio Files (14)
- `audio.pack` - Main audio pack
- `audio_br.pack` - Brazilian Portuguese audio
- `audio_cn.pack` - Chinese (Simplified) audio
- `audio_cz.pack` - Czech audio
- `audio_en.pack` - English audio
- `audio_fr.pack` - French audio
- `audio_ge.pack` - German audio
- `audio_it.pack` - Italian audio
- `audio_kr.pack` - Korean audio
- `audio_m.pack` - Additional audio (music/misc)
- `audio_pl.pack` - Polish audio
- `audio_sp.pack` - Spanish audio
- `audio_tr.pack` - Turkish audio
- `audio_zh.pack` - Chinese (Traditional) audio

### Localization Files (12)
- `local_br.pack` - Brazilian Portuguese localization
- `local_cn.pack` - Chinese (Simplified) localization
- `local_cz.pack` - Czech localization
- `local_en.pack` - English localization
- `local_fr.pack` - French localization
- `local_ge.pack` - German localization
- `local_it.pack` - Italian localization
- `local_kr.pack` - Korean localization
- `local_pl.pack` - Polish localization
- `local_sp.pack` - Spanish localization
- `local_tr.pack` - Turkish localization
- `local_zh.pack` - Chinese (Traditional) localization

### Terrain Files (4)
- `terrain.pack` - Main terrain data
- `terrain2.pack` - Additional terrain data
- `terrain3.pack` - Additional terrain data
- `terrain4.pack` - Additional terrain data

### Data Files (3)
- `data.pack` - Main game data
- `data_db.pack` - Database files
- `data_special.pack` - Special game data

### Visual Assets (5)
- `models.pack` - 3D models
- `units.pack` - Unit models and data
- `ui.pack` - User interface assets
- `chariot.pack` - Chariot-specific models
- `shaders.pack` - Shader files

### Variants (2)
- `variants.pack` - Model variants
- `variants2.pack` - Additional model variants

### Core Files (2)
- `boot.pack` - Boot/initialization data
- `movies.pack` - Video files

## Development

This project is developed using Claude Code in branches. Current branch:

```
claude/list-game-pack-files-011CV2G9p7aXmCAahpqXucga
```

### Sync to Local Environment

```bash
# Fetch all branches
git fetch origin

# Checkout the Claude Code branch
git checkout claude/list-game-pack-files-011CV2G9p7aXmCAahpqXucga

# Pull latest changes
git pull

# Open in your editor
cursor .
```

## Recommended Workflow

### For Finding Specific Data:

1. **Start with `quick_search.py`** - Tells you which packs to extract
2. **Read `EXTRACTION_GUIDE.md`** - Learn how to extract pack files
3. **Install RPFM** - Download from GitHub releases
4. **Extract priority packs** - Usually `data_db.pack`, `data.pack`, `local_en.pack`
5. **Search extracted files** - Use `pack_extractor.py` or `grep`

### Most Useful Pack Files:

| Pack File | Contains | Priority |
|-----------|----------|----------|
| `data_db.pack` | All database tables (TSV format) - units, buildings, factions, etc. | ⭐⭐⭐ HIGH |
| `data.pack` | Core game definitions and mechanics | ⭐⭐⭐ HIGH |
| `local_en.pack` | All English text (names, descriptions) | ⭐⭐ MEDIUM |
| `data_special.pack` | Campaign mechanics and special rules | ⭐⭐ MEDIUM |
| `units.pack` | Unit models and data | ⭐ LOW (unless modding) |

### What Are You Looking For?

Tell me what data you need, and I can create targeted extraction scripts:
- 📊 Unit stats and abilities
- 🏛️ Building chains and effects
- 👑 Faction bonuses and traits
- 🔬 Technologies and research
- ⚔️ Battle mechanics
- 🗺️ Campaign mechanics
- 💰 Economy and resources
- 🎭 Character skills and traits

## Next Steps

Planned enhancements:
- Automated RPFM integration
- Data visualization tools
- Database query interface
- Mod comparison tools
- Data export to CSV/JSON

## License

This is a tool for working with Total War PHARAOH DYNASTIES data. The game and all pack files are property of Creative Assembly and SEGA.
