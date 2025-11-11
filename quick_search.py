#!/usr/bin/env python3
"""
Quick Search Tool for Total War PHARAOH

Use this to search for specific data types without full extraction.
This script helps you identify which pack files to extract first.
"""

import sys
from pathlib import Path
import json


class QuickSearchGuide:
    """Interactive guide to help find specific data."""

    def __init__(self):
        with open('pack_files.json', 'r') as f:
            self.pack_data = json.load(f)

    def show_menu(self):
        """Show main search menu."""
        print("\n" + "="*70)
        print("TOTAL WAR PHARAOH - QUICK SEARCH GUIDE")
        print("="*70)
        print("\nWhat type of data are you looking for?\n")

        options = {
            '1': ('Unit Stats & Data', self.search_units),
            '2': ('Building Information', self.search_buildings),
            '3': ('Faction Data', self.search_factions),
            '4': ('Technologies & Research', self.search_technologies),
            '5': ('Character Data', self.search_characters),
            '6': ('Campaign Mechanics', self.search_campaign),
            '7': ('Battle Mechanics', self.search_battle),
            '8': ('Resources & Economy', self.search_economy),
            '9': ('Localization/Text', self.search_text),
            '10': ('All Game Data (Database)', self.search_database),
            'q': ('Quit', None)
        }

        for key, (label, _) in options.items():
            print(f"  [{key}] {label}")

        print()
        choice = input("Enter your choice: ").strip().lower()

        if choice in options and options[choice][1]:
            options[choice][1]()
        elif choice == 'q':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice!")
            self.show_menu()

    def search_units(self):
        """Guide for finding unit data."""
        print("\n" + "="*70)
        print("UNIT DATA SEARCH")
        print("="*70)
        print("\nTo find unit stats and information:\n")
        print("📦 Extract these pack files (in order):")
        print("   1. data_db.pack    - Contains unit stats tables")
        print("   2. units.pack      - Contains unit definitions")
        print("   3. data.pack       - Contains additional unit data")
        print("   4. local_en.pack   - Contains unit names/descriptions")
        print("   5. chariot.pack    - Chariot-specific units")
        print("\n📁 Look in these locations after extraction:")
        print("   - data_db/db/land_units_*.tsv")
        print("   - data_db/db/unit_stats_*.tsv")
        print("   - units/units/")
        print("\n🔍 Search commands:")
        print("   grep -ri 'unit_name' ./extracted/data_db/")
        print("   find ./extracted -name '*unit*'")
        print("\n💡 Common fields in unit tables:")
        print("   - key: Unit identifier")
        print("   - melee_attack: Attack value")
        print("   - melee_defence: Defense value")
        print("   - armour: Armor value")
        print("   - health: Hit points")
        print("   - speed: Movement speed")
        self._show_extraction_command(['data_db.pack', 'units.pack', 'local_en.pack'])

    def search_buildings(self):
        """Guide for finding building data."""
        print("\n" + "="*70)
        print("BUILDING DATA SEARCH")
        print("="*70)
        print("\nTo find building information:\n")
        print("📦 Extract these pack files:")
        print("   1. data_db.pack    - Building tables and stats")
        print("   2. data.pack       - Building definitions")
        print("   3. local_en.pack   - Building names/descriptions")
        print("\n📁 Look in these locations:")
        print("   - data_db/db/building_*.tsv")
        print("   - data_db/db/building_chains*.tsv")
        print("   - data/buildings/")
        print("\n🔍 Search commands:")
        print("   grep -ri 'building_name' ./extracted/data_db/")
        print("   find ./extracted -name '*building*'")
        self._show_extraction_command(['data_db.pack', 'data.pack', 'local_en.pack'])

    def search_factions(self):
        """Guide for finding faction data."""
        print("\n" + "="*70)
        print("FACTION DATA SEARCH")
        print("="*70)
        print("\nTo find faction information:\n")
        print("📦 Extract these pack files:")
        print("   1. data_db.pack    - Faction tables")
        print("   2. data.pack       - Faction definitions")
        print("   3. local_en.pack   - Faction names/descriptions")
        print("\n📁 Look in these locations:")
        print("   - data_db/db/factions*.tsv")
        print("   - data_db/db/faction_groups*.tsv")
        print("   - data/factions/")
        print("\n🔍 Search commands:")
        print("   grep -ri 'faction' ./extracted/data_db/db/")
        self._show_extraction_command(['data_db.pack', 'local_en.pack'])

    def search_technologies(self):
        """Guide for finding technology data."""
        print("\n" + "="*70)
        print("TECHNOLOGY & RESEARCH SEARCH")
        print("="*70)
        print("\nTo find technology/research data:\n")
        print("📦 Extract these pack files:")
        print("   1. data_db.pack    - Technology tables")
        print("   2. data.pack       - Tech tree definitions")
        print("   3. local_en.pack   - Tech names/descriptions")
        print("\n📁 Look in these locations:")
        print("   - data_db/db/technologies*.tsv")
        print("   - data_db/db/technology_*")
        print("   - data/technologies/")
        self._show_extraction_command(['data_db.pack', 'local_en.pack'])

    def search_characters(self):
        """Guide for finding character data."""
        print("\n" + "="*70)
        print("CHARACTER DATA SEARCH")
        print("="*70)
        print("\nTo find character information:\n")
        print("📦 Extract these pack files:")
        print("   1. data_db.pack    - Character tables")
        print("   2. data.pack       - Character definitions")
        print("   3. local_en.pack   - Character names/text")
        print("\n📁 Look in these locations:")
        print("   - data_db/db/characters*.tsv")
        print("   - data_db/db/character_skills*.tsv")
        print("   - data_db/db/character_traits*.tsv")
        self._show_extraction_command(['data_db.pack', 'local_en.pack'])

    def search_campaign(self):
        """Guide for finding campaign mechanics."""
        print("\n" + "="*70)
        print("CAMPAIGN MECHANICS SEARCH")
        print("="*70)
        print("\nTo find campaign mechanics data:\n")
        print("📦 Extract these pack files:")
        print("   1. data_special.pack - Special campaign mechanics")
        print("   2. data.pack         - Campaign definitions")
        print("   3. data_db.pack      - Campaign tables")
        print("\n📁 Look in these locations:")
        print("   - data_special/")
        print("   - data/campaigns/")
        print("   - data_db/db/campaign_*.tsv")
        self._show_extraction_command(['data_special.pack', 'data.pack', 'data_db.pack'])

    def search_battle(self):
        """Guide for finding battle mechanics."""
        print("\n" + "="*70)
        print("BATTLE MECHANICS SEARCH")
        print("="*70)
        print("\nTo find battle mechanics data:\n")
        print("📦 Extract these pack files:")
        print("   1. data.pack         - Battle definitions")
        print("   2. data_db.pack      - Battle tables")
        print("   3. units.pack        - Unit battle stats")
        print("\n📁 Look in these locations:")
        print("   - data_db/db/battle_*.tsv")
        print("   - data/battles/")
        self._show_extraction_command(['data.pack', 'data_db.pack', 'units.pack'])

    def search_economy(self):
        """Guide for finding economy/resources data."""
        print("\n" + "="*70)
        print("RESOURCES & ECONOMY SEARCH")
        print("="*70)
        print("\nTo find resource and economy data:\n")
        print("📦 Extract these pack files:")
        print("   1. data_db.pack    - Economy tables")
        print("   2. data.pack       - Resource definitions")
        print("   3. local_en.pack   - Resource names")
        print("\n📁 Look in these locations:")
        print("   - data_db/db/resources*.tsv")
        print("   - data_db/db/pooled_resources*.tsv")
        print("   - data_db/db/trade_*.tsv")
        self._show_extraction_command(['data_db.pack', 'local_en.pack'])

    def search_text(self):
        """Guide for finding localization/text."""
        print("\n" + "="*70)
        print("LOCALIZATION & TEXT SEARCH")
        print("="*70)
        print("\nTo find game text and descriptions:\n")
        print("📦 Extract these pack files:")
        print("   1. local_en.pack   - English text")
        print("   2. local_fr.pack   - French text")
        print("   3. local_ge.pack   - German text")
        print("   ... (other languages)")
        print("\n📁 Look in these locations:")
        print("   - local_en/text/")
        print("   - local_en/db/")
        print("\n🔍 All game text is here:")
        print("   - Unit names and descriptions")
        print("   - Building names and descriptions")
        print("   - Technology names")
        print("   - Event text")
        print("   - UI text")
        self._show_extraction_command(['local_en.pack'])

    def search_database(self):
        """Guide for finding all database tables."""
        print("\n" + "="*70)
        print("ALL DATABASE TABLES")
        print("="*70)
        print("\nTo access ALL game data tables:\n")
        print("📦 Extract this pack file:")
        print("   data_db.pack - Master database with all tables")
        print("\n📁 Contains structured data in TSV format:")
        print("   - Units, buildings, technologies")
        print("   - Factions, characters, traits")
        print("   - Battle mechanics, campaign rules")
        print("   - Resources, economy, diplomacy")
        print("   - Effects, abilities, skills")
        print("\n💡 This is the BEST place to start!")
        print("   It contains most of the structured game data in an")
        print("   easy-to-read table format (TSV = Tab-Separated Values)")
        print("\n🔍 After extraction, explore:")
        print("   ls ./extracted/data_db/db/")
        print("   ls ./extracted/data_db/db/*.tsv | wc -l  # Count tables")
        self._show_extraction_command(['data_db.pack'])

    def _show_extraction_command(self, pack_files):
        """Show extraction commands for specified packs."""
        print("\n" + "-"*70)
        print("🚀 EXTRACTION COMMANDS:")
        print("-"*70)
        print("\nStep 1: Install RPFM (if not installed)")
        print("   Download from: https://github.com/Frodo45127/rpfm/releases")
        print("\nStep 2: Extract pack files")
        print(f"\n   Using RPFM GUI:")
        print(f"   - Open RPFM")
        print(f"   - File → Open → select pack file")
        print(f"   - Right-click → Extract")
        print("\n   Using Python script:")
        for pack in pack_files:
            print(f"   python3 pack_extractor.py extract {pack}")
        print("\nStep 3: Search the extracted data")
        print("   python3 pack_extractor.py search 'your_search_term'")
        print("   grep -ri 'your_search_term' ./extracted/")
        print("\n" + "="*70)
        input("\nPress Enter to return to menu...")
        self.show_menu()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Quick search mode
        search_term = ' '.join(sys.argv[1:])
        print(f"\nQuick recommendations for searching: '{search_term}'\n")

        search_lower = search_term.lower()

        recommendations = {
            'unit': ['data_db.pack', 'units.pack', 'local_en.pack'],
            'building': ['data_db.pack', 'data.pack', 'local_en.pack'],
            'faction': ['data_db.pack', 'local_en.pack'],
            'tech': ['data_db.pack', 'local_en.pack'],
            'character': ['data_db.pack', 'local_en.pack'],
            'resource': ['data_db.pack', 'local_en.pack'],
            'economy': ['data_db.pack', 'data.pack'],
            'battle': ['data.pack', 'data_db.pack', 'units.pack'],
            'campaign': ['data_special.pack', 'data.pack', 'data_db.pack']
        }

        found = False
        for keyword, packs in recommendations.items():
            if keyword in search_lower:
                print(f"📦 Recommended pack files to extract:")
                for pack in packs:
                    print(f"   - {pack}")
                print(f"\n🔍 After extraction, try:")
                print(f"   python3 pack_extractor.py search '{search_term}'")
                print(f"   grep -ri '{search_term}' ./extracted/")
                found = True
                break

        if not found:
            print("💡 Not sure which packs contain this data.")
            print("   Start with: data_db.pack (contains most game data)")
            print(f"\n   Then search: grep -ri '{search_term}' ./extracted/")
    else:
        # Interactive mode
        guide = QuickSearchGuide()
        try:
            guide.show_menu()
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
