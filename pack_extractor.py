#!/usr/bin/env python3
"""
Total War PHARAOH Pack File Extractor

This script provides utilities to extract and search data from Total War PHARAOH pack files.
Pack files are proprietary CA (Creative Assembly) archive format used in Total War games.

Requirements:
- RPFM (Rusted PackFile Manager) or similar tool for pack file extraction
- OR: Total War modding tools
"""

import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re


class PackExtractor:
    """Extractor for Total War PHARAOH pack files."""

    def __init__(self, game_data_dir: str, output_dir: str = "./extracted"):
        """
        Initialize the extractor.

        Args:
            game_data_dir: Path to Total War PHARAOH data directory
            output_dir: Directory where extracted files will be saved
        """
        self.game_data_dir = Path(game_data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load pack files list
        with open('pack_files.json', 'r') as f:
            self.pack_data = json.load(f)

    def list_pack_files(self) -> List[Path]:
        """List all available pack files in the game directory."""
        pack_files = []
        for pack_file in self.game_data_dir.glob("*.pack"):
            pack_files.append(pack_file)
        return sorted(pack_files)

    def verify_pack_files(self) -> Tuple[List[str], List[str]]:
        """
        Verify which pack files from the JSON exist in the game directory.

        Returns:
            Tuple of (found_files, missing_files)
        """
        all_packs = []
        for category in self.pack_data['categories'].values():
            all_packs.extend(category['files'])

        found = []
        missing = []

        for pack_name in all_packs:
            pack_path = self.game_data_dir / pack_name
            if pack_path.exists():
                found.append(pack_name)
            else:
                missing.append(pack_name)

        return found, missing

    def get_pack_info(self, pack_file: Path) -> Dict:
        """
        Get information about a pack file (size, modification date, etc.).

        Args:
            pack_file: Path to the pack file

        Returns:
            Dictionary with pack file info
        """
        if not pack_file.exists():
            return {'error': 'File not found'}

        stat = pack_file.stat()
        return {
            'name': pack_file.name,
            'path': str(pack_file),
            'size_bytes': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'modified': stat.st_mtime
        }

    def extract_pack_with_rpfm(self, pack_file: Path, rpfm_path: str = "rpfm") -> bool:
        """
        Extract a pack file using RPFM tool.

        Args:
            pack_file: Path to the pack file to extract
            rpfm_path: Path to RPFM executable

        Returns:
            True if extraction successful, False otherwise
        """
        output_path = self.output_dir / pack_file.stem

        try:
            # RPFM command line extraction
            # Note: Adjust command based on RPFM CLI interface
            cmd = [rpfm_path, "extract", str(pack_file), str(output_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✓ Extracted {pack_file.name} to {output_path}")
                return True
            else:
                print(f"✗ Failed to extract {pack_file.name}: {result.stderr}")
                return False

        except FileNotFoundError:
            print(f"Error: RPFM not found at {rpfm_path}")
            return False
        except Exception as e:
            print(f"Error extracting {pack_file.name}: {e}")
            return False

    def search_extracted_files(self, search_term: str, file_extensions: List[str] = None) -> List[Dict]:
        """
        Search for a term in extracted files.

        Args:
            search_term: Term to search for
            file_extensions: List of file extensions to search (e.g., ['.xml', '.txt'])

        Returns:
            List of matches with file path, line number, and content
        """
        if not self.output_dir.exists():
            print(f"Output directory {self.output_dir} does not exist. Extract pack files first.")
            return []

        matches = []
        pattern = re.compile(re.escape(search_term), re.IGNORECASE)

        for file_path in self.output_dir.rglob('*'):
            if not file_path.is_file():
                continue

            # Filter by extension if specified
            if file_extensions and file_path.suffix.lower() not in file_extensions:
                continue

            # Skip binary files
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if pattern.search(line):
                            matches.append({
                                'file': str(file_path.relative_to(self.output_dir)),
                                'line': line_num,
                                'content': line.strip()
                            })
            except Exception:
                # Skip files that can't be read as text
                continue

        return matches

    def find_data_files(self, data_types: List[str] = None) -> Dict[str, List[Path]]:
        """
        Find specific types of data files in extracted content.

        Args:
            data_types: List of data types to look for (e.g., ['db', 'xml', 'lua'])

        Returns:
            Dictionary mapping data types to lists of file paths
        """
        if data_types is None:
            data_types = ['db', 'xml', 'lua', 'txt', 'json', 'csv']

        results = {dt: [] for dt in data_types}

        for data_type in data_types:
            pattern = f"*.{data_type}"
            files = list(self.output_dir.rglob(pattern))
            results[data_type] = files

        return results

    def generate_extraction_report(self, output_file: str = "extraction_report.txt"):
        """Generate a report of extracted files and their structure."""
        if not self.output_dir.exists():
            print(f"Output directory {self.output_dir} does not exist.")
            return

        report_path = Path(output_file)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("TOTAL WAR PHARAOH DYNASTIES - EXTRACTION REPORT\n")
            f.write("="*80 + "\n\n")

            # List all extracted directories
            f.write("Extracted Pack Files:\n")
            f.write("-"*80 + "\n")

            for pack_dir in sorted(self.output_dir.iterdir()):
                if pack_dir.is_dir():
                    file_count = sum(1 for _ in pack_dir.rglob('*') if _.is_file())
                    f.write(f"\n{pack_dir.name}/\n")
                    f.write(f"  Files: {file_count}\n")

                    # List file types
                    extensions = {}
                    for file_path in pack_dir.rglob('*'):
                        if file_path.is_file():
                            ext = file_path.suffix.lower() or 'no_extension'
                            extensions[ext] = extensions.get(ext, 0) + 1

                    if extensions:
                        f.write("  File types:\n")
                        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
                            f.write(f"    {ext}: {count}\n")

            f.write("\n" + "="*80 + "\n")

        print(f"Report generated: {report_path}")


class DataSearcher:
    """Advanced searcher for specific game data."""

    def __init__(self, extracted_dir: str = "./extracted"):
        """Initialize the searcher."""
        self.extracted_dir = Path(extracted_dir)

    def search_tables(self, table_name: str) -> List[Path]:
        """Search for database tables by name."""
        # Total War uses .tsv files for some data tables
        results = []
        for pattern in [f"*{table_name}*.tsv", f"*{table_name}*.csv", f"*{table_name}*"]:
            results.extend(self.extracted_dir.rglob(pattern))
        return results

    def search_units(self, unit_name: str) -> List[Dict]:
        """Search for unit data."""
        # Look in common unit data files
        search_patterns = [
            "*/units/*",
            "*/unit_stats/*",
            "*/land_units/*",
            "*units*.xml",
            "*units*.tsv"
        ]

        results = []
        for pattern in search_patterns:
            files = self.extracted_dir.glob(pattern)
            for file in files:
                # Search in file content
                try:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if unit_name.lower() in content.lower():
                            results.append({
                                'file': str(file),
                                'type': 'unit_data'
                            })
                except Exception:
                    continue

        return results

    def search_buildings(self, building_name: str) -> List[Dict]:
        """Search for building data."""
        search_patterns = [
            "*/buildings/*",
            "*buildings*.xml",
            "*buildings*.tsv"
        ]

        results = []
        for pattern in search_patterns:
            files = self.extracted_dir.glob(pattern)
            for file in files:
                try:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if building_name.lower() in content.lower():
                            results.append({
                                'file': str(file),
                                'type': 'building_data'
                            })
                except Exception:
                    continue

        return results

    def find_all_data_tables(self) -> Dict[str, List[str]]:
        """Find all data tables in extracted files."""
        tables = {
            'tsv': [],
            'csv': [],
            'xml': [],
            'lua': [],
            'json': []
        }

        for ext in tables.keys():
            files = self.extracted_dir.rglob(f"*.{ext}")
            tables[ext] = [str(f.relative_to(self.extracted_dir)) for f in files]

        return tables


def main():
    """Main function with CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Total War PHARAOH Pack File Extractor and Searcher"
    )

    parser.add_argument(
        '--game-dir',
        type=str,
        help='Path to Total War PHARAOH data directory',
        default='/TotalWarPharaohDynastiesData/data/'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        help='Directory for extracted files',
        default='./extracted'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List command
    subparsers.add_parser('list', help='List all pack files')

    # Verify command
    subparsers.add_parser('verify', help='Verify pack files exist')

    # Info command
    info_parser = subparsers.add_parser('info', help='Get info about pack files')
    info_parser.add_argument('pack_name', nargs='?', help='Specific pack file name')

    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract pack files')
    extract_parser.add_argument('pack_name', nargs='?', help='Specific pack to extract (or all)')
    extract_parser.add_argument('--rpfm', type=str, help='Path to RPFM tool')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search in extracted files')
    search_parser.add_argument('term', help='Search term')
    search_parser.add_argument('--ext', nargs='+', help='File extensions to search')

    # Find tables command
    subparsers.add_parser('tables', help='Find all data tables')

    # Report command
    subparsers.add_parser('report', help='Generate extraction report')

    args = parser.parse_args()

    extractor = PackExtractor(args.game_dir, args.output_dir)

    if args.command == 'list':
        pack_files = extractor.list_pack_files()
        print(f"Found {len(pack_files)} pack files:\n")
        for pf in pack_files:
            info = extractor.get_pack_info(pf)
            print(f"  {pf.name:<30} {info['size_mb']:>8.2f} MB")

    elif args.command == 'verify':
        found, missing = extractor.verify_pack_files()
        print(f"\n✓ Found: {len(found)} pack files")
        print(f"✗ Missing: {len(missing)} pack files")
        if missing:
            print("\nMissing files:")
            for m in missing:
                print(f"  - {m}")

    elif args.command == 'info':
        if args.pack_name:
            pack_path = Path(args.game_dir) / args.pack_name
            info = extractor.get_pack_info(pack_path)
            print(json.dumps(info, indent=2))
        else:
            pack_files = extractor.list_pack_files()
            for pf in pack_files[:10]:  # Show first 10
                info = extractor.get_pack_info(pf)
                print(f"{info['name']}: {info['size_mb']} MB")

    elif args.command == 'extract':
        rpfm = args.rpfm or 'rpfm'
        print(f"Note: This requires RPFM tool at: {rpfm}")
        print("Please install RPFM: https://github.com/Frodo45127/rpfm")

    elif args.command == 'search':
        results = extractor.search_extracted_files(args.term, args.ext)
        print(f"\nFound {len(results)} matches for '{args.term}':\n")
        for match in results[:50]:  # Show first 50
            print(f"{match['file']}:{match['line']}")
            print(f"  {match['content'][:100]}")
            print()

    elif args.command == 'tables':
        searcher = DataSearcher(args.output_dir)
        tables = searcher.find_all_data_tables()
        print("\nData Tables Found:")
        print("-"*80)
        for ext, files in tables.items():
            if files:
                print(f"\n{ext.upper()} files ({len(files)}):")
                for f in files[:10]:  # Show first 10
                    print(f"  {f}")
                if len(files) > 10:
                    print(f"  ... and {len(files) - 10} more")

    elif args.command == 'report':
        extractor.generate_extraction_report()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
