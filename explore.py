#!/usr/bin/env python3
"""
Total War Pharaoh Dynasties - Data Extractor MVP
Explores game directory and identifies accessible data files.
"""

import os
import sys
from pathlib import Path
from collections import defaultdict
import xml.etree.ElementTree as ET


class GameDataExplorer:
    """Explores Total War Pharaoh game data directory."""

    def __init__(self, game_data_path):
        self.game_path = Path(game_data_path)
        self.file_categories = defaultdict(list)
        self.readable_files = []
        self.pack_files = []

    def explore(self):
        """Main exploration method."""
        print(f"🔍 Exploring: {self.game_path}")
        print("=" * 80)

        if not self.game_path.exists():
            print(f"❌ ERROR: Path does not exist: {self.game_path}")
            return False

        # Step 1: Scan all files
        print("\n📁 SCANNING FILES...")
        self.scan_directory()

        # Step 2: Categorize files
        print("\n📊 FILE CATEGORIES:")
        self.display_categories()

        # Step 3: Try reading accessible files
        print("\n📖 READING ACCESSIBLE FILES:")
        self.read_accessible_files()

        # Step 4: Analyze .pack files
        print("\n📦 PACK FILES FOUND:")
        self.analyze_pack_files()

        # Step 5: Search for unit data
        print("\n⚔️  SEARCHING FOR UNIT DATA:")
        self.search_unit_data()

        return True

    def scan_directory(self):
        """Recursively scan the game directory."""
        try:
            for item in self.game_path.rglob('*'):
                if item.is_file():
                    ext = item.suffix.lower()
                    if not ext:
                        ext = '.no_extension'
                    self.file_categories[ext].append(item)

                    # Track .pack files separately
                    if ext == '.pack':
                        self.pack_files.append(item)

            total_files = sum(len(files) for files in self.file_categories.values())
            print(f"✅ Found {total_files} files in {len(self.file_categories)} categories")

        except PermissionError as e:
            print(f"❌ Permission denied: {e}")
        except Exception as e:
            print(f"❌ Error scanning: {e}")

    def display_categories(self):
        """Display file categories sorted by count."""
        sorted_categories = sorted(
            self.file_categories.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )

        for ext, files in sorted_categories[:15]:  # Top 15 categories
            print(f"  {ext:20s} : {len(files):4d} files")

        if len(sorted_categories) > 15:
            remaining = sum(len(files) for ext, files in sorted_categories[15:])
            print(f"  {'(other types)':20s} : {remaining:4d} files")

    def read_accessible_files(self):
        """Try to read text and XML files."""
        # Focus on potentially readable files
        readable_extensions = ['.txt', '.xml', '.json', '.ini', '.cfg', '.no_extension']

        files_read = 0
        for ext in readable_extensions:
            if ext not in self.file_categories:
                continue

            for file_path in self.file_categories[ext][:5]:  # Read first 5 of each type
                try:
                    rel_path = file_path.relative_to(self.game_path)

                    # Try reading as text
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1000)  # Read first 1000 chars

                    print(f"\n  📄 {rel_path}")
                    print(f"     Size: {file_path.stat().st_size} bytes")

                    if ext == '.xml':
                        # Try parsing as XML
                        try:
                            tree = ET.parse(file_path)
                            root = tree.getroot()
                            print(f"     XML Root: <{root.tag}> with {len(root)} children")
                        except:
                            print(f"     Preview: {content[:100]}...")
                    else:
                        # Show text preview
                        lines = content.split('\n')[:3]
                        for line in lines:
                            if line.strip():
                                print(f"     {line[:70]}")

                    self.readable_files.append(file_path)
                    files_read += 1

                except Exception as e:
                    pass  # Skip unreadable files

        if files_read == 0:
            print("  ⚠️  No easily readable text files found (most data in .pack files)")

    def analyze_pack_files(self):
        """Analyze .pack files."""
        if not self.pack_files:
            print("  ⚠️  No .pack files found")
            return

        print(f"  Found {len(self.pack_files)} .pack files:")

        # Sort by size
        sorted_packs = sorted(self.pack_files, key=lambda x: x.stat().st_size, reverse=True)

        total_size = 0
        for pack_file in sorted_packs[:10]:  # Show top 10
            size = pack_file.stat().st_size
            total_size += size
            size_mb = size / (1024 * 1024)
            rel_path = pack_file.relative_to(self.game_path)
            print(f"    {size_mb:8.1f} MB - {rel_path}")

        if len(sorted_packs) > 10:
            remaining_size = sum(p.stat().st_size for p in sorted_packs[10:])
            total_size += remaining_size
            print(f"    ... and {len(sorted_packs) - 10} more files ({remaining_size / (1024*1024):.1f} MB)")

        print(f"\n  Total .pack data: {total_size / (1024*1024):.1f} MB")
        print(f"  ⚠️  These files need specialized extraction tools (e.g., RPFM)")

    def search_unit_data(self):
        """Search for unit-related data in accessible files."""
        unit_keywords = ['unit', 'soldier', 'warrior', 'troop', 'battalion', 'regiment']
        findings = []

        # Search in readable files
        for file_path in self.readable_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()

                for keyword in unit_keywords:
                    if keyword in content:
                        rel_path = file_path.relative_to(self.game_path)
                        findings.append((rel_path, keyword))
                        break

            except:
                pass

        if findings:
            print("  Found potential unit data references:")
            for file_path, keyword in findings:
                print(f"    '{keyword}' in {file_path}")
        else:
            print("  ⚠️  No unit data found in accessible files")
            print("  💡 Unit data is likely in .pack files - need extraction tool")

    def generate_report(self, output_file='findings.md'):
        """Generate a findings report."""
        report_path = Path(__file__).parent / output_file

        with open(report_path, 'w') as f:
            f.write("# Total War Pharaoh Dynasties - Data Exploration Findings\n\n")
            f.write(f"**Explored Path:** `{self.game_path}`\n\n")

            # File statistics
            f.write("## File Statistics\n\n")
            total_files = sum(len(files) for files in self.file_categories.values())
            f.write(f"- **Total Files:** {total_files}\n")
            f.write(f"- **File Types:** {len(self.file_categories)}\n")
            f.write(f"- **Pack Files:** {len(self.pack_files)}\n\n")

            # Categories
            f.write("## File Categories (Top 10)\n\n")
            f.write("| Extension | Count |\n")
            f.write("|-----------|-------|\n")
            sorted_categories = sorted(
                self.file_categories.items(),
                key=lambda x: len(x[1]),
                reverse=True
            )
            for ext, files in sorted_categories[:10]:
                f.write(f"| `{ext}` | {len(files)} |\n")

            # Readable files
            f.write("\n## Accessible Files\n\n")
            if self.readable_files:
                for file_path in self.readable_files:
                    rel_path = file_path.relative_to(self.game_path)
                    f.write(f"- `{rel_path}`\n")
            else:
                f.write("*No easily readable files found.*\n")

            # Pack files
            f.write("\n## Pack Files (Largest 10)\n\n")
            sorted_packs = sorted(self.pack_files, key=lambda x: x.stat().st_size, reverse=True)
            f.write("| Size (MB) | File |\n")
            f.write("|-----------|------|\n")
            for pack_file in sorted_packs[:10]:
                size_mb = pack_file.stat().st_size / (1024 * 1024)
                rel_path = pack_file.relative_to(self.game_path)
                f.write(f"| {size_mb:.1f} | `{rel_path}` |\n")

            # Next steps
            f.write("\n## Next Steps\n\n")
            f.write("1. **Install RPFM** - Tool to extract .pack files\n")
            f.write("2. **Extract key .pack files** - Focus on largest files likely containing unit data\n")
            f.write("3. **Locate unit tables** - Look for database tables with unit stats\n")
            f.write("4. **Parse extracted data** - Build parser for extracted tables\n")

        print(f"\n💾 Report saved to: {report_path}")


def main():
    """Main entry point."""
    # Default game path
    game_path = "/Users/jensholm/Library/Application Support/Steam/steamapps/common/Total War PHARAOH DYNASTIES/TotalWarPharaohDynastiesData/data"

    # Allow override via command line
    if len(sys.argv) > 1:
        game_path = sys.argv[1]

    print("=" * 80)
    print("🏺 TOTAL WAR PHARAOH DYNASTIES - DATA EXTRACTOR MVP")
    print("=" * 80)

    explorer = GameDataExplorer(game_path)

    if explorer.explore():
        explorer.generate_report()
        print("\n✅ Exploration complete!")
        print("\n📋 Next: Review findings.md for next steps")
    else:
        print("\n❌ Exploration failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
