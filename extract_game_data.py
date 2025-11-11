#!/usr/bin/env python3
"""
Total War PHARAOH DYNASTIES - Game Data Extractor

Extracts and parses units, buildings, and factions data from pack files.
Exports to JSON and CSV formats for easy analysis.
"""

import os
import sys
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse


class GameDataExtractor:
    """Extract and parse game data from Total War PHARAOH pack files."""

    def __init__(self, extracted_dir: str = "./extracted", output_dir: str = "./output"):
        """
        Initialize the extractor.

        Args:
            extracted_dir: Directory containing extracted pack files
            output_dir: Directory for output files (JSON/CSV)
        """
        self.extracted_dir = Path(extracted_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Localization data (key -> text)
        self.localization = {}

    def load_localization(self, lang: str = 'en'):
        """Load localization data for text lookups."""
        print(f"\n📚 Loading {lang.upper()} localization data...")

        local_pack = self.extracted_dir / f"local_{lang}"
        if not local_pack.exists():
            print(f"⚠️  Warning: Localization pack not found at {local_pack}")
            print(f"   Extract local_{lang}.pack for text descriptions")
            return

        # Find all text/localization files
        text_files = list(local_pack.rglob("*.txt"))
        text_files.extend(local_pack.rglob("*.tsv"))

        count = 0
        for file_path in text_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        # TSV format: key\ttext
                        if '\t' in line:
                            parts = line.strip().split('\t', 1)
                            if len(parts) == 2:
                                self.localization[parts[0]] = parts[1]
                                count += 1
            except Exception as e:
                continue

        print(f"✓ Loaded {count} localization entries")

    def get_text(self, key: str) -> str:
        """Get localized text for a key."""
        return self.localization.get(key, key)

    def find_db_file(self, pattern: str) -> Optional[Path]:
        """Find a database file matching pattern."""
        db_dir = self.extracted_dir / "data_db" / "db"
        if not db_dir.exists():
            return None

        # Try exact match first
        exact_match = db_dir / pattern
        if exact_match.exists():
            return exact_match

        # Try pattern matching
        matches = list(db_dir.glob(f"{pattern}*"))
        if matches:
            return matches[0]

        return None

    def parse_tsv_file(self, file_path: Path) -> List[Dict]:
        """Parse a TSV file into a list of dictionaries."""
        if not file_path.exists():
            return []

        rows = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Read header
                header_line = f.readline().strip()
                if not header_line:
                    return []

                headers = header_line.split('\t')

                # Read data rows
                for line in f:
                    values = line.strip().split('\t')
                    if len(values) == len(headers):
                        row = dict(zip(headers, values))
                        rows.append(row)
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

        return rows

    def extract_units(self) -> Dict:
        """Extract unit data."""
        print("\n" + "="*70)
        print("EXTRACTING UNITS DATA")
        print("="*70)

        # Check if data_db is extracted
        data_db = self.extracted_dir / "data_db"
        if not data_db.exists():
            print("\n❌ Error: data_db pack not extracted!")
            print("\n📦 Please extract first:")
            print("   Using RPFM GUI: Open data_db.pack → Right-click → Extract")
            print("   Or see EXTRACTION_GUIDE.md for details")
            return {}

        units_data = {
            'metadata': {
                'source': 'Total War PHARAOH DYNASTIES',
                'type': 'units',
                'extracted_from': ['data_db.pack', 'local_en.pack']
            },
            'units': []
        }

        # Find unit tables
        db_dir = data_db / "db"
        print(f"\n🔍 Searching for unit tables in: {db_dir}")

        unit_tables = [
            "land_units_tables",
            "main_units_tables",
            "units_tables",
            "unit_stats_land_tables",
            "land_units"
        ]

        found_tables = []
        for table_name in unit_tables:
            table_file = self.find_db_file(f"{table_name}.tsv")
            if table_file:
                found_tables.append((table_name, table_file))
                print(f"✓ Found: {table_file.name}")

        if not found_tables:
            print("\n⚠️  No unit tables found!")
            print("   Available tables:")
            if db_dir.exists():
                for f in sorted(db_dir.glob("*.tsv"))[:20]:
                    print(f"   - {f.name}")
            return units_data

        # Parse unit data
        print(f"\n📊 Parsing unit data...")
        for table_name, table_file in found_tables:
            rows = self.parse_tsv_file(table_file)
            print(f"   {table_name}: {len(rows)} entries")

            for row in rows:
                unit = {
                    'key': row.get('key', ''),
                    'source_table': table_name
                }

                # Get text data
                if 'key' in row:
                    unit['name'] = self.get_text(f"units_name_{row['key']}")
                    unit['description'] = self.get_text(f"units_description_{row['key']}")

                # Common unit stats
                stat_fields = [
                    'melee_attack', 'melee_defence', 'charge_bonus',
                    'armour', 'health', 'speed', 'morale',
                    'cost', 'upkeep', 'recruitment_cost',
                    'num_men', 'class', 'category', 'tier'
                ]

                for field in stat_fields:
                    if field in row:
                        unit[field] = row[field]

                # Add all other fields
                for key, value in row.items():
                    if key not in unit and key not in ['source_table']:
                        unit[key] = value

                units_data['units'].append(unit)

        units_data['metadata']['total_units'] = len(units_data['units'])

        print(f"\n✓ Extracted {len(units_data['units'])} units")
        return units_data

    def extract_buildings(self) -> Dict:
        """Extract building data."""
        print("\n" + "="*70)
        print("EXTRACTING BUILDINGS DATA")
        print("="*70)

        data_db = self.extracted_dir / "data_db"
        if not data_db.exists():
            print("\n❌ Error: data_db pack not extracted!")
            return {}

        buildings_data = {
            'metadata': {
                'source': 'Total War PHARAOH DYNASTIES',
                'type': 'buildings',
                'extracted_from': ['data_db.pack', 'local_en.pack']
            },
            'buildings': [],
            'building_chains': []
        }

        db_dir = data_db / "db"
        print(f"\n🔍 Searching for building tables in: {db_dir}")

        building_tables = [
            "building_levels_tables",
            "buildings_tables",
            "building_chains_tables"
        ]

        found_tables = []
        for table_name in building_tables:
            table_file = self.find_db_file(f"{table_name}.tsv")
            if table_file:
                found_tables.append((table_name, table_file))
                print(f"✓ Found: {table_file.name}")

        if not found_tables:
            print("\n⚠️  No building tables found!")
            return buildings_data

        # Parse building data
        print(f"\n📊 Parsing building data...")
        for table_name, table_file in found_tables:
            rows = self.parse_tsv_file(table_file)
            print(f"   {table_name}: {len(rows)} entries")

            for row in rows:
                building = {
                    'key': row.get('key', ''),
                    'source_table': table_name
                }

                # Get text data
                if 'key' in row:
                    building['name'] = self.get_text(f"building_name_{row['key']}")
                    building['description'] = self.get_text(f"building_description_{row['key']}")

                # Common building fields
                stat_fields = [
                    'building_chain', 'level', 'cost', 'construction_time',
                    'building_category', 'building_group'
                ]

                for field in stat_fields:
                    if field in row:
                        building[field] = row[field]

                # Add all other fields
                for key, value in row.items():
                    if key not in building and key not in ['source_table']:
                        building[key] = value

                if 'chain' in table_name.lower():
                    buildings_data['building_chains'].append(building)
                else:
                    buildings_data['buildings'].append(building)

        buildings_data['metadata']['total_buildings'] = len(buildings_data['buildings'])
        buildings_data['metadata']['total_chains'] = len(buildings_data['building_chains'])

        print(f"\n✓ Extracted {len(buildings_data['buildings'])} buildings")
        print(f"✓ Extracted {len(buildings_data['building_chains'])} building chains")
        return buildings_data

    def extract_factions(self) -> Dict:
        """Extract faction data."""
        print("\n" + "="*70)
        print("EXTRACTING FACTIONS DATA")
        print("="*70)

        data_db = self.extracted_dir / "data_db"
        if not data_db.exists():
            print("\n❌ Error: data_db pack not extracted!")
            return {}

        factions_data = {
            'metadata': {
                'source': 'Total War PHARAOH DYNASTIES',
                'type': 'factions',
                'extracted_from': ['data_db.pack', 'local_en.pack']
            },
            'factions': []
        }

        db_dir = data_db / "db"
        print(f"\n🔍 Searching for faction tables in: {db_dir}")

        faction_tables = [
            "factions_tables",
            "faction_groups_tables",
            "faction_traits_tables"
        ]

        found_tables = []
        for table_name in faction_tables:
            table_file = self.find_db_file(f"{table_name}.tsv")
            if table_file:
                found_tables.append((table_name, table_file))
                print(f"✓ Found: {table_file.name}")

        if not found_tables:
            print("\n⚠️  No faction tables found!")
            return factions_data

        # Parse faction data
        print(f"\n📊 Parsing faction data...")
        for table_name, table_file in found_tables:
            rows = self.parse_tsv_file(table_file)
            print(f"   {table_name}: {len(rows)} entries")

            for row in rows:
                faction = {
                    'key': row.get('key', ''),
                    'source_table': table_name
                }

                # Get text data
                if 'key' in row:
                    faction['name'] = self.get_text(f"factions_name_{row['key']}")
                    faction['description'] = self.get_text(f"factions_description_{row['key']}")

                # Common faction fields
                stat_fields = [
                    'faction_group', 'subculture', 'culture',
                    'is_playable', 'home_region'
                ]

                for field in stat_fields:
                    if field in row:
                        faction[field] = row[field]

                # Add all other fields
                for key, value in row.items():
                    if key not in faction and key not in ['source_table']:
                        faction[key] = value

                factions_data['factions'].append(faction)

        factions_data['metadata']['total_factions'] = len(factions_data['factions'])

        print(f"\n✓ Extracted {len(factions_data['factions'])} factions")
        return factions_data

    def export_to_json(self, data: Dict, filename: str):
        """Export data to JSON file."""
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved: {output_path}")

    def export_to_csv(self, data: Dict, filename: str):
        """Export data to CSV file."""
        output_path = self.output_dir / filename

        # Get the main data list
        if 'units' in data:
            items = data['units']
        elif 'buildings' in data:
            items = data['buildings']
        elif 'factions' in data:
            items = data['factions']
        else:
            return

        if not items:
            return

        # Get all unique keys
        all_keys = set()
        for item in items:
            all_keys.update(item.keys())

        fieldnames = sorted(all_keys)

        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(items)

        print(f"💾 Saved: {output_path}")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Extract units, buildings, and factions data from Total War PHARAOH"
    )

    parser.add_argument(
        'data_types',
        nargs='+',
        choices=['units', 'buildings', 'factions', 'all'],
        help='Data types to extract'
    )

    parser.add_argument(
        '--extracted-dir',
        default='./extracted',
        help='Directory with extracted pack files (default: ./extracted)'
    )

    parser.add_argument(
        '--output-dir',
        default='./output',
        help='Output directory for JSON/CSV files (default: ./output)'
    )

    parser.add_argument(
        '--lang',
        default='en',
        help='Language for localization (default: en)'
    )

    parser.add_argument(
        '--format',
        choices=['json', 'csv', 'both'],
        default='both',
        help='Output format (default: both)'
    )

    args = parser.parse_args()

    # Expand 'all' to all data types
    if 'all' in args.data_types:
        data_types = ['units', 'buildings', 'factions']
    else:
        data_types = args.data_types

    # Initialize extractor
    extractor = GameDataExtractor(args.extracted_dir, args.output_dir)

    # Load localization
    extractor.load_localization(args.lang)

    # Extract requested data
    for data_type in data_types:
        if data_type == 'units':
            data = extractor.extract_units()
            if data and data.get('units'):
                if args.format in ['json', 'both']:
                    extractor.export_to_json(data, 'units.json')
                if args.format in ['csv', 'both']:
                    extractor.export_to_csv(data, 'units.csv')

        elif data_type == 'buildings':
            data = extractor.extract_buildings()
            if data and data.get('buildings'):
                if args.format in ['json', 'both']:
                    extractor.export_to_json(data, 'buildings.json')
                if args.format in ['csv', 'both']:
                    extractor.export_to_csv(data, 'buildings.csv')

        elif data_type == 'factions':
            data = extractor.extract_factions()
            if data and data.get('factions'):
                if args.format in ['json', 'both']:
                    extractor.export_to_json(data, 'factions.json')
                if args.format in ['csv', 'both']:
                    extractor.export_to_csv(data, 'factions.csv')

    print("\n" + "="*70)
    print("EXTRACTION COMPLETE")
    print("="*70)
    print(f"\n📁 Output saved to: {args.output_dir}/")
    print("\n💡 To view your data:")
    print(f"   cat {args.output_dir}/units.json")
    print(f"   cat {args.output_dir}/units.csv")


if __name__ == "__main__":
    main()
