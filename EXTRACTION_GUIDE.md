# Pack File Extraction and Search Guide

## Overview

Total War PHARAOH pack files (`.pack`) are proprietary CA (Creative Assembly) archive formats. To extract and search data from them, you need specialized tools.

## Required Tools

### 1. RPFM (Rusted PackFile Manager) - RECOMMENDED
- **GitHub**: https://github.com/Frodo45127/rpfm
- **Downloads**: https://github.com/Frodo45127/rpfm/releases
- **Platforms**: Windows, Linux, macOS
- **Features**:
  - GUI and CLI support
  - Extract pack files
  - View tables, images, text files
  - Edit and repack files

### 2. Alternative: Total War Assembly Kit
- Official CA modding tools
- Limited to specific Total War games
- May not support all PHARAOH features

## Installation

### RPFM on Linux/Mac:
```bash
# Download latest release
wget https://github.com/Frodo45127/rpfm/releases/latest/download/rpfm-linux.zip

# Extract
unzip rpfm-linux.zip

# Make executable
chmod +x rpfm

# Move to PATH (optional)
sudo mv rpfm /usr/local/bin/
```

### RPFM on Windows:
1. Download `rpfm-windows.zip` from releases
2. Extract to a folder
3. Run `rpfm.exe`

## Extraction Methods

### Method 1: GUI Extraction (Easiest)

1. Open RPFM
2. File → Open → Select `.pack` file
3. Browse the pack file contents
4. Right-click folder → Extract
5. Choose output directory

### Method 2: CLI Extraction (Automation)

```bash
# Extract single pack file
python3 pack_extractor.py extract data.pack --rpfm /path/to/rpfm

# Extract multiple packs
for pack in data.pack data_db.pack units.pack; do
    python3 pack_extractor.py extract $pack --rpfm rpfm
done
```

### Method 3: Batch Extraction Script

```bash
#!/bin/bash
# extract_all.sh

GAME_DIR="/TotalWarPharaohDynastiesData/data"
OUTPUT_DIR="./extracted"
RPFM="rpfm"  # or /path/to/rpfm

# Priority packs (most likely to contain useful data)
PRIORITY_PACKS=(
    "data.pack"
    "data_db.pack"
    "data_special.pack"
    "units.pack"
    "local_en.pack"
)

mkdir -p "$OUTPUT_DIR"

echo "Extracting priority packs..."
for pack in "${PRIORITY_PACKS[@]}"; do
    echo "Extracting $pack..."
    $RPFM extract "$GAME_DIR/$pack" "$OUTPUT_DIR/${pack%.pack}"
done

echo "Done!"
```

## What Data to Extract First

### Priority 1: Core Game Data
These contain most gameplay-related information:

1. **data.pack** - Main game data
   - Unit stats
   - Building data
   - Technologies
   - Characters
   - Factions

2. **data_db.pack** - Database tables
   - Structured data in TSV/CSV format
   - Easy to parse and search
   - Contains most numerical data

3. **data_special.pack** - Special game rules
   - Campaign mechanics
   - Battle mechanics
   - Special abilities

### Priority 2: Units and Models
4. **units.pack** - Unit definitions
5. **chariot.pack** - Chariot-specific data
6. **variants.pack** / **variants2.pack** - Unit variants

### Priority 3: Localization
7. **local_en.pack** - English text
   - All in-game text
   - Descriptions
   - Helps understand data keys

### Lower Priority:
- **audio_*.pack** - Sound files (large, less relevant for data extraction)
- **terrain*.pack** - Map data (large files)
- **models.pack** - 3D models (very large)
- **shaders.pack** - Graphics shaders
- **movies.pack** - Video files

## Searching Extracted Data

### 1. Using Our Tools

```bash
# Search for specific term in all extracted files
python3 pack_extractor.py search "unit_name" --ext .xml .tsv .txt

# Find all data tables
python3 pack_extractor.py tables

# Generate extraction report
python3 pack_extractor.py report
```

### 2. Using grep (Quick searches)

```bash
# Search in extracted directory
grep -r "search_term" ./extracted/

# Search only in specific file types
grep -r --include="*.xml" "unit_name" ./extracted/

# Case-insensitive search with line numbers
grep -rni "faction_name" ./extracted/
```

### 3. Using find (Locate files)

```bash
# Find all XML files
find ./extracted -name "*.xml"

# Find files containing specific name
find ./extracted -name "*units*"

# Find TSV/CSV database files
find ./extracted -name "*.tsv" -o -name "*.csv"
```

## Common Data Locations

After extraction, look for these directories/files:

### Database Tables (TSV/CSV files)
- `data_db/db/`
- Contains tables like:
  - `units_tables.tsv`
  - `buildings_tables.tsv`
  - `factions_tables.tsv`
  - `technologies_tables.tsv`

### Unit Data
- `units/`
- `data/units/`
- Look for XML or TSV files

### Text/Localization
- `local_en/text/`
- `local_en/db/`
- Contains all English game text

### Scripts
- `scripts/` or `data/scripts/`
- Lua scripts for game logic

## Example: Finding Unit Stats

```bash
# 1. Extract core packs
python3 pack_extractor.py extract data.pack
python3 pack_extractor.py extract data_db.pack
python3 pack_extractor.py extract units.pack

# 2. Find unit-related files
find ./extracted -name "*unit*" -type f

# 3. Search for specific unit
grep -ri "spearmen" ./extracted/data_db/
grep -ri "spearmen" ./extracted/units/

# 4. Look at database tables
cat ./extracted/data_db/db/land_units_tables.tsv

# 5. Get localized names
grep "spearmen" ./extracted/local_en/text/*.txt
```

## Example: Finding Building Data

```bash
# Extract and search
python3 pack_extractor.py extract data_db.pack
find ./extracted/data_db -name "*building*"
grep -ri "temple" ./extracted/data_db/db/
```

## Tips for Efficient Searching

### 1. Start Small
Don't extract everything at once. Start with:
- `data.pack`
- `data_db.pack`
- `local_en.pack`

### 2. Use the Right Tools
- **RPFM GUI**: Browse and explore structure
- **Python scripts**: Automated searching
- **grep/find**: Quick command-line searches

### 3. Understand Data Structure
Total War games typically organize data as:
- **Database tables** (TSV/CSV) - Structured numerical data
- **XML files** - Configuration and definitions
- **Lua scripts** - Game logic
- **Text files** - Localization

### 4. Look for Keys
Many data files use keys/IDs that link to localized text:
- Find key: `unit_egy_spearmen_0`
- Look up text: `local_en/text/` contains description

## Verification

Check if pack files exist:
```bash
python3 pack_extractor.py verify
```

List pack files with sizes:
```bash
python3 pack_extractor.py list
```

Get info about specific pack:
```bash
python3 pack_extractor.py info data.pack
```

## Next Steps

1. **Install RPFM** - Get the extraction tool
2. **Extract core packs** - Start with data.pack, data_db.pack
3. **Explore structure** - Use RPFM GUI to browse
4. **Search for your data** - Use our Python tools or grep
5. **Document findings** - Note where important data is located

## What Are You Looking For?

Tell me what specific data you're trying to find:
- Unit stats?
- Building information?
- Faction data?
- Technologies?
- Campaign mechanics?
- Character data?

I can create targeted search scripts for specific data types!
