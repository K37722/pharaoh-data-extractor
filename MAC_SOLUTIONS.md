# Mac Solutions for Total War Pack File Extraction

## The Problem
RPFM (the standard tool) has **NO official Mac build** yet.
Developer says: "MacOS: You'll know it when I manage to compile it for Mac."

## Your Real Mac Options

### ✅ Option 1: tw_unpack (Rust CLI Tool) - RECOMMENDED

**What it is:**
Open-source Total War pack file unpacker written in Rust

**Installation:**
```bash
# Install Rust (if not installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Install tw_unpack
cargo install tw_unpack

# Verify installation
tw_unpack --help
```

**Usage:**
```bash
# Extract a pack file
tw_unpack /path/to/data.pack -o ./extracted/data/

# Extract with verbose output
tw_unpack /path/to/data_db.pack -o ./extracted/data_db/ -v

# Extract all priority packs
tw_unpack /path/to/data.pack -o ./extracted/data/
tw_unpack /path/to/data_db.pack -o ./extracted/data_db/
tw_unpack /path/to/local_en.pack -o ./extracted/local_en/
```

**Pros:**
- ✅ Native Mac support (Rust compiles for Mac)
- ✅ Command-line (easy to script)
- ✅ Open source
- ✅ Maintained by Total War modding community

**Cons:**
- ❌ No GUI (command-line only)
- ❌ May not support all pack versions (test first)

**Then use my tools:**
```bash
python3 extract_game_data.py all
```

---

### ✅ Option 2: RPFM-CLI (Command-Line RPFM)

**What it is:**
Command-line version of RPFM

**Installation:**
```bash
# Install Rust (if not installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Install RPFM-CLI
cargo install rpfm_cli

# Verify installation
rpfm_cli --help
```

**Usage:**
```bash
# Check available commands
rpfm_cli --help

# Extract pack file (syntax may vary)
rpfm_cli -e /path/to/data.pack -o ./extracted/
```

**Pros:**
- ✅ Official RPFM tool (CLI version)
- ✅ Should work on Mac via Rust

**Cons:**
- ❌ CLI syntax may be complex
- ❌ Documentation limited
- ❌ Not tested extensively on Mac

---

### ⚠️ Option 3: Wine/CrossOver (Run Windows RPFM)

**What it is:**
Run the Windows version of RPFM on Mac using Wine

**Installation:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Wine
brew install --cask wine-stable

# Or use CrossOver (paid, more polished)
# https://www.codeweavers.com/crossover
```

**Download Windows RPFM:**
- https://github.com/Frodo45127/rpfm/releases
- Download Windows .zip version

**Run with Wine:**
```bash
wine rpfm.exe
```

**Pros:**
- ✅ Full GUI version of RPFM
- ✅ All RPFM features available

**Cons:**
- ❌ Requires Wine setup
- ❌ May have compatibility issues
- ❌ Slower than native

---

### 🐍 Option 4: Build My Python Parser

**What it is:**
Develop a complete Python pack file parser

**Status:**
I started this in `python_pack_reader.py` but it needs:
- 40-80 hours of development
- Reverse-engineering pack format
- Testing with all pack types

**Pros:**
- ✅ Pure Python (no dependencies)
- ✅ Native Mac support
- ✅ Open source

**Cons:**
- ❌ Requires significant development time
- ❌ May not handle all pack versions
- ❌ Not ready yet

**I can do this if you want!**

---

### 🕷️ Option 5: Wiki Scraper (No Extraction Needed)

**What it is:**
Scrape Total War Wiki for game data

**What I'll build:**
```python
# Scrape wiki for units, buildings, factions
python3 wiki_scraper.py --output ./wiki_data/

# Output: JSON and CSV files
ls ./wiki_data/
# units.json, buildings.json, factions.json
# units.csv, buildings.csv, factions.csv
```

**Pros:**
- ✅ No pack file extraction needed
- ✅ Works on any platform
- ✅ Quick to implement (2-3 hours)
- ✅ Gets 70-80% of data

**Cons:**
- ❌ Not 100% complete (wiki may miss data)
- ❌ Less accurate than game files
- ❌ No hidden/unreleased content

**I can build this RIGHT NOW!**

---

## My Mac Recommendation

### Best Path Forward:

**1. Try tw_unpack FIRST (5 minutes):**
```bash
# Quick install
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
cargo install tw_unpack

# Test with one pack
tw_unpack /path/to/data_db.pack -o ./test_extract/ -v

# If it works, extract all priority packs
tw_unpack /path/to/data.pack -o ./extracted/data/
tw_unpack /path/to/data_db.pack -o ./extracted/data_db/
tw_unpack /path/to/local_en.pack -o ./extracted/local_en/

# Parse the data
python3 extract_game_data.py all
```

**2. If tw_unpack doesn't work:**

**Quick solution:** Let me build the wiki scraper (2-3 hours)
- Gets you 70-80% of the data
- No extraction needed
- Works immediately

**OR**

**Complete solution:** Try RPFM-CLI or Wine (more setup)
- Gets you 100% of the data
- More complex setup

---

## What Do You Want to Do?

**🦀 Option A: Try tw_unpack** (5 minutes)
- I'll guide you through installation
- Test if it works with PHARAOH
- If yes → extract and parse
- If no → move to Plan B

**🕷️ Option B: Build wiki scraper** (I do the work)
- I'll create the tool
- You get data in 2-3 hours
- 70-80% complete but easier

**🍷 Option C: Try Wine/RPFM** (15-30 minutes)
- Install Wine
- Run Windows RPFM
- Full features but more complex

**🐍 Option D: Develop Python parser** (long-term)
- I build a complete solution
- Takes 40-80 hours
- Perfect for community contribution

**Which sounds best?** 🎯
