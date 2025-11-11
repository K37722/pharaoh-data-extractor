#!/usr/bin/env python3
"""
Total War PHARAOH DYNASTIES Pack Files Manager

This script provides utilities to list, search, and analyze pack files
from Total War PHARAOH DYNASTIES game data.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional


class PackFilesManager:
    """Manager for Total War PHARAOH DYNASTIES pack files."""

    def __init__(self, json_file: str = "pack_files.json"):
        """Initialize the manager with pack files data."""
        self.json_file = json_file
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load pack files data from JSON file."""
        json_path = Path(__file__).parent / self.json_file
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_all_files(self) -> List[str]:
        """Get a list of all pack files."""
        all_files = []
        for category in self.data['categories'].values():
            all_files.extend(category['files'])
        return sorted(all_files)

    def get_files_by_category(self, category: str) -> List[str]:
        """Get pack files for a specific category."""
        if category not in self.data['categories']:
            available = ', '.join(self.data['categories'].keys())
            raise ValueError(f"Category '{category}' not found. Available: {available}")
        return self.data['categories'][category]['files']

    def get_files_by_language(self, lang_code: str) -> Dict[str, List[str]]:
        """Get audio and localization files for a specific language."""
        lang_code = lang_code.lower()
        if lang_code not in self.data['languages']:
            available = ', '.join(self.data['languages'].keys())
            raise ValueError(f"Language '{lang_code}' not found. Available: {available}")

        audio_files = [f for f in self.data['categories']['audio']['files']
                      if f.endswith(f"_{lang_code}.pack")]
        local_files = [f for f in self.data['categories']['localization']['files']
                      if f.endswith(f"_{lang_code}.pack")]

        return {
            'language': self.data['languages'][lang_code],
            'audio': audio_files,
            'localization': local_files
        }

    def search_files(self, search_term: str) -> List[str]:
        """Search for pack files matching a term."""
        search_term = search_term.lower()
        all_files = self.get_all_files()
        return [f for f in all_files if search_term in f.lower()]

    def get_statistics(self) -> Dict:
        """Get statistics about pack files."""
        stats = {
            'total_files': self.data['total_pack_files'],
            'categories': {}
        }

        for cat_name, cat_data in self.data['categories'].items():
            stats['categories'][cat_name] = {
                'count': len(cat_data['files']),
                'description': cat_data['description']
            }

        stats['languages_count'] = len(self.data['languages'])

        return stats

    def list_categories(self) -> Dict[str, str]:
        """List all categories with their descriptions."""
        return {
            name: data['description']
            for name, data in self.data['categories'].items()
        }

    def list_languages(self) -> Dict[str, str]:
        """List all supported languages."""
        return self.data['languages']

    def print_summary(self):
        """Print a summary of pack files."""
        print(f"╔══════════════════════════════════════════════════════════════╗")
        print(f"║  {self.data['game']:^58}  ║")
        print(f"╠══════════════════════════════════════════════════════════════╣")
        print(f"║  Total Pack Files: {self.data['total_pack_files']:<42}  ║")
        print(f"║  Data Directory: {self.data['data_directory']:<44}  ║")
        print(f"╚══════════════════════════════════════════════════════════════╝")
        print()

        print("Categories:")
        print("-" * 64)
        for cat_name, cat_data in self.data['categories'].items():
            count = len(cat_data['files'])
            print(f"  {cat_name:<15} ({count:>2} files): {cat_data['description']}")

        print()
        print(f"Supported Languages: {len(self.data['languages'])}")
        print("-" * 64)
        for code, name in self.data['languages'].items():
            print(f"  {code}: {name}")


def main():
    """Main function to demonstrate usage."""
    import sys

    manager = PackFilesManager()

    # If no arguments, print summary
    if len(sys.argv) == 1:
        manager.print_summary()
        print("\nUsage examples:")
        print("  python pack_files_manager.py list              # List all files")
        print("  python pack_files_manager.py category audio    # List audio files")
        print("  python pack_files_manager.py language en       # List English files")
        print("  python pack_files_manager.py search terrain    # Search for 'terrain'")
        return

    command = sys.argv[1].lower()

    if command == "list":
        print("All Pack Files:")
        print("-" * 64)
        for file in manager.get_all_files():
            print(f"  {file}")
        print(f"\nTotal: {len(manager.get_all_files())} files")

    elif command == "category" or command == "cat":
        if len(sys.argv) < 3:
            print("Available categories:")
            for name, desc in manager.list_categories().items():
                print(f"  {name}: {desc}")
        else:
            category = sys.argv[2]
            try:
                files = manager.get_files_by_category(category)
                print(f"Pack files in category '{category}':")
                print("-" * 64)
                for file in files:
                    print(f"  {file}")
                print(f"\nTotal: {len(files)} files")
            except ValueError as e:
                print(f"Error: {e}")

    elif command == "language" or command == "lang":
        if len(sys.argv) < 3:
            print("Available languages:")
            for code, name in manager.list_languages().items():
                print(f"  {code}: {name}")
        else:
            lang_code = sys.argv[2]
            try:
                result = manager.get_files_by_language(lang_code)
                print(f"Pack files for {result['language']} ({lang_code}):")
                print("-" * 64)
                print(f"\nAudio files:")
                for file in result['audio']:
                    print(f"  {file}")
                print(f"\nLocalization files:")
                for file in result['localization']:
                    print(f"  {file}")
            except ValueError as e:
                print(f"Error: {e}")

    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: python pack_files_manager.py search <term>")
        else:
            search_term = sys.argv[2]
            results = manager.search_files(search_term)
            print(f"Search results for '{search_term}':")
            print("-" * 64)
            if results:
                for file in results:
                    print(f"  {file}")
                print(f"\nFound {len(results)} file(s)")
            else:
                print("  No files found")

    elif command == "stats":
        stats = manager.get_statistics()
        print("Pack Files Statistics:")
        print("-" * 64)
        print(f"Total files: {stats['total_files']}")
        print(f"Supported languages: {stats['languages_count']}")
        print("\nBy category:")
        for cat_name, cat_stats in stats['categories'].items():
            print(f"  {cat_name:<15} {cat_stats['count']:>2} files")

    else:
        print(f"Unknown command: {command}")
        print("\nAvailable commands: list, category, language, search, stats")


if __name__ == "__main__":
    main()
