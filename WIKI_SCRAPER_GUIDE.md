# Wiki Scraper Guide

## What It Does

The wiki scraper extracts units, buildings, and factions data from Total War Wiki (totalwar.fandom.com) and exports it to JSON and CSV files.

**Pros:**
- ✅ No pack file extraction needed
- ✅ No RPFM installation required
- ✅ Works on any platform (Mac, Linux, Windows)
- ✅ Gets ~70-80% of game data
- ✅ Ready to use immediately

**Cons:**
- ❌ May not have 100% of data (wiki might be incomplete)
- ❌ No hidden/unreleased content
- ❌ Depends on wiki quality

## Installation

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Or install manually
pip3 install requests beautifulsoup4 lxml
```

## Usage

### Scrape Everything

```bash
python3 wiki_scraper.py all
```

This will scrape:
- All units
- All buildings
- All factions

Output goes to `./wiki_data/` directory.

### Scrape Specific Data

```bash
# Only units
python3 wiki_scraper.py units

# Only buildings
python3 wiki_scraper.py buildings

# Only factions
python3 wiki_scraper.py factions
```

### Custom Output Directory

```bash
python3 wiki_scraper.py all --output-dir ./my_data
```

## Output Files

After scraping, you'll get:

```
wiki_data/
├── units.json          # All units in JSON format
├── units.csv           # All units in CSV format
├── buildings.json      # All buildings in JSON format
├── buildings.csv       # All buildings in CSV format
├── factions.json       # All factions in JSON format
├── factions.csv        # All factions in CSV format
└── summary.json        # Scraping summary with counts
```

## Viewing the Data

### JSON Files (structured data)

```bash
# View units
cat ./wiki_data/units.json | head -50

# Pretty print with Python
python3 -m json.tool ./wiki_data/units.json

# Search for specific unit
grep -i "spearmen" ./wiki_data/units.json
```

### CSV Files (spreadsheet format)

```bash
# View in terminal
cat ./wiki_data/units.csv

# Open in Excel/Numbers
open ./wiki_data/units.csv

# View with column command
column -t -s',' ./wiki_data/units.csv | less
```

## Data Structure

### Units Data

Each unit includes:
- **name**: Unit name
- **type**: Unit type/class (infantry, chariot, etc.)
- **faction**: Associated faction (if any)
- **stats**: Dictionary of stats (attack, defense, etc.)
- **abilities**: List of special abilities
- **description**: Unit description
- **url**: Link to wiki page

### Buildings Data

Each building includes:
- **name**: Building name
- **type**: Building type/category
- **effects**: List of effects
- **cost**: Construction cost
- **description**: Building description

### Factions Data

Each faction includes:
- **name**: Faction name
- **culture**: Cultural group
- **leader**: Starting leader name
- **bonuses**: List of faction bonuses
- **units**: List of unique units
- **starting_region**: Starting region name
- **description**: Faction description
- **url**: Link to wiki page

## How It Works

1. **Fetches wiki pages** from totalwar.fandom.com
2. **Parses HTML** to extract structured data
3. **Exports to JSON and CSV** for easy use
4. **Respects server** with delays between requests

## Troubleshooting

### "No module named 'requests'"

Install dependencies:
```bash
pip3 install -r requirements.txt
```

### "Connection timeout"

Check your internet connection or try again later:
```bash
python3 wiki_scraper.py all
```

### "Could not fetch page"

The wiki page might not exist or has moved. The scraper will skip it and continue.

### Not Enough Data

The wiki may not have complete data for all units/buildings/factions. This is normal - wikis are community-maintained and may be incomplete.

**For complete data**, you'll need to use RPFM to extract from game files.

## Comparison: Wiki Scraper vs Pack Extraction

| Feature | Wiki Scraper | Pack Extraction (RPFM) |
|---------|--------------|------------------------|
| **Setup Time** | 1 minute | 15-30 minutes |
| **Requirements** | Python only | RPFM tool |
| **Mac Support** | ✅ Works | ⚠️ RPFM has no Mac GUI |
| **Data Completeness** | ~70-80% | 100% |
| **Hidden Content** | ❌ No | ✅ Yes |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Data Accuracy** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Best For** | Quick data, no setup | Complete data, modding |

## Example Workflow

### Quick Analysis

```bash
# 1. Scrape the data
python3 wiki_scraper.py all

# 2. View summary
cat ./wiki_data/summary.json

# 3. Open units in spreadsheet
open ./wiki_data/units.csv

# 4. Search for specific data
grep -i "egyptian" ./wiki_data/factions.json
```

### Data Processing

```python
import json

# Load units data
with open('./wiki_data/units.json', 'r') as f:
    units = json.load(f)

# Filter Egyptian units
egyptian_units = [u for u in units if 'egypt' in u.get('faction', '').lower()]

# Count by type
from collections import Counter
types = Counter(u.get('type', 'Unknown') for u in units)
print(types)
```

## Next Steps

After scraping wiki data:

1. **Analyze the data** - Open CSV files in Excel/Numbers
2. **Combine with other sources** - Merge with game data if available
3. **Report issues** - If you find missing data, consider contributing to the wiki
4. **Upgrade to pack extraction** - If you need 100% complete data, use RPFM

## Contributing to the Wiki

If you find missing data in the scraped results, consider helping the Total War community:

1. Visit: https://totalwar.fandom.com
2. Create an account
3. Add missing unit/building/faction data
4. Help future modders and players!

## Limitations

- **Wiki quality**: Data completeness depends on wiki contributors
- **Page structure**: If wiki changes format, scraper may need updates
- **Rate limiting**: Scraper adds delays to respect the server
- **No images**: Currently only extracts text data (not images)

## Future Enhancements

Planned improvements:
- Image downloading
- More detailed stat extraction
- Technology tree scraping
- Character/skill data
- Battle map information

---

**Questions?** Check the main README.md or other documentation files!
