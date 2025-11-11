# Quick Start Guide

## TL;DR - What You Need to Know

### The Pack Files Problem

Total War PHARAOH stores data in `.pack` files (like ZIP files). To get the data out, you need to extract them.

### Three Paths Forward

#### 🌟 Path 1: Find Existing Data (NO TOOLS NEEDED - Easiest!)

Someone may have already extracted this data.

**Search for:**
- "Total War Pharaoh units database"
- "Pharaoh game data spreadsheet"
- Total War modding forums/discord

**If you find it → You're done!** Skip all the extraction stuff.

#### 🔧 Path 2: Use RPFM (Standard Method)

RPFM = Tool that extracts pack files

**Steps:**
1. Install RPFM → See `RPFM_MAC_INSTALL.md`
2. Extract pack files → See `EXTRACTION_GUIDE.md`
3. Parse data → Use `python3 extract_game_data.py all`

**Pros:** Most reliable, full control
**Cons:** Need to install RPFM

#### 🐍 Path 3: Python-Only (If Possible)

Use Python libraries to read pack files directly (no RPFM).

**Status:** I can research and implement this if you want!

## What Do You Want to Do?

### Option A: I Just Want the Data
→ Let's search for existing extracted data
→ Check community resources
→ Use wikis/databases

### Option B: I Want to Extract It Myself
→ Install RPFM (see `RPFM_MAC_INSTALL.md`)
→ Extract packs (see `EXTRACTION_GUIDE.md`)
→ Run `python3 extract_game_data.py all`

### Option C: Skip RPFM, Use Python Only
→ Let me research Python pack file libraries
→ I'll create a pure Python solution
→ May or may not work depending on available libraries

## Quick Commands (If You Have Extracted Data)

If you already have the pack files extracted in `./extracted/`:

```bash
# Extract units, buildings, and factions
python3 extract_game_data.py all

# Or extract specific data
python3 extract_game_data.py units
python3 extract_game_data.py buildings
python3 extract_game_data.py factions

# Output will be in ./output/ as JSON and CSV
ls ./output/
```

## What's in This Repository

```
pack_files.json              - List of all 37 pack files
pack_files_manager.py        - Browse pack files by category
quick_search.py              - Find which packs to extract
extract_game_data.py         - Parse units/buildings/factions data

EXTRACTION_GUIDE.md          - Detailed extraction guide
RPFM_MAC_INSTALL.md         - How to install RPFM on Mac
ALTERNATIVES.md              - Do you really need RPFM?
README.md                    - Full documentation
```

## Decision Tree

```
Do you have the game files?
│
├─ NO → Use online resources (wikis, community databases)
│
└─ YES → Do you want to extract yourself?
    │
    ├─ NO → Search for existing extracted data
    │
    └─ YES → Choose extraction method:
        │
        ├─ RPFM (standard) → RPFM_MAC_INSTALL.md
        │
        └─ Python only → Tell me, I'll research this
```

## Need Help Deciding?

**Tell me:**
1. Do you have the game installed?
2. What specific data do you need? (units, buildings, factions, etc.)
3. Is this one-time or ongoing?
4. Preference: Quick & easy vs Full control?

I'll recommend the best path for you! 🎯
