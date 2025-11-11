#!/usr/bin/env python3
"""
Total War Pack File Reader (PFH5 Format)
Based on TotalWar-Modding/docs pack file format specification.
"""

import struct
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class PackFileEntry:
    """Represents a single file entry in the pack."""

    def __init__(self, path: str, size: int, offset: int, timestamp: Optional[int] = None):
        self.path = path
        self.size = size
        self.offset = offset
        self.timestamp = timestamp

    def __repr__(self):
        return f"PackFileEntry(path={self.path}, size={self.size}, offset={self.offset})"


class PFH5Reader:
    """Reader for Total War PFH5 pack files."""

    # Pack file type flags
    PACK_TYPE_BOOT = 0
    PACK_TYPE_RELEASE = 1
    PACK_TYPE_PATCH = 2
    PACK_TYPE_MOD = 3
    PACK_TYPE_MOVIE = 4

    # Bitmask flags
    FLAG_EXTENDED_HEADER = 0x100000
    FLAG_INDEX_ENCRYPTED = 0x008000
    FLAG_TIMESTAMP_IN_INDEX = 0x000400
    FLAG_DATA_PADDED = 0x000010

    def __init__(self, pack_path: str):
        self.pack_path = Path(pack_path)
        self.header = {}
        self.entries: List[PackFileEntry] = []
        self.file_data_offset = 0

        if not self.pack_path.exists():
            raise FileNotFoundError(f"Pack file not found: {pack_path}")

    def read_header(self) -> Dict:
        """Read and parse the 32-byte PFH5 header."""
        with open(self.pack_path, 'rb') as f:
            # Read 32-byte header (8 fields x 4 bytes)
            header_data = f.read(32)

            if len(header_data) < 32:
                raise ValueError("Invalid pack file: header too short")

            # Parse header fields
            preamble = header_data[0:4]
            if preamble != b'PFH5':
                raise ValueError(f"Invalid pack file: expected PFH5, got {preamble}")

            # Unpack header fields (little-endian)
            type_bitmask = struct.unpack('<I', header_data[4:8])[0]
            pf_index_count = struct.unpack('<I', header_data[8:12])[0]
            pf_index_size = struct.unpack('<I', header_data[12:16])[0]
            file_index_count = struct.unpack('<I', header_data[16:20])[0]
            file_index_size = struct.unpack('<I', header_data[20:24])[0]
            timestamp = struct.unpack('<I', header_data[24:28])[0]
            signature_pos = struct.unpack('<I', header_data[28:32])[0]

            # Extract pack type and flags
            pack_type = type_bitmask & 0x0F
            flags = type_bitmask & 0xFFFFFFF0

            self.header = {
                'preamble': preamble.decode('ascii'),
                'pack_type': pack_type,
                'type_bitmask': type_bitmask,
                'flags': flags,
                'pf_index_count': pf_index_count,
                'pf_index_size': pf_index_size,
                'file_index_count': file_index_count,
                'file_index_size': file_index_size,
                'timestamp': timestamp,
                'signature_pos': signature_pos,
                'has_extended_header': bool(flags & self.FLAG_EXTENDED_HEADER),
                'index_encrypted': bool(flags & self.FLAG_INDEX_ENCRYPTED),
                'has_timestamps': bool(flags & self.FLAG_TIMESTAMP_IN_INDEX),
                'data_padded': bool(flags & self.FLAG_DATA_PADDED),
            }

            return self.header

    def read_file_index(self) -> List[PackFileEntry]:
        """Read and parse the file index."""
        if not self.header:
            self.read_header()

        if self.header['index_encrypted']:
            print("⚠️  WARNING: File index is encrypted - cannot read without decryption")
            return []

        with open(self.pack_path, 'rb') as f:
            # Skip header (32 bytes) and extended header if present
            header_size = 32
            if self.header['has_extended_header']:
                header_size += 20

            # Skip PF index (we don't need it for simple extraction)
            f.seek(header_size + self.header['pf_index_size'])

            # Read file index
            file_index_data = f.read(self.header['file_index_size'])

            # Parse file entries
            entries = []
            current_offset = 0
            pos = 0

            for _ in range(self.header['file_index_count']):
                if pos >= len(file_index_data):
                    break

                # Read null-terminated file path (comes FIRST in actual format)
                path_end = file_index_data.find(b'\x00', pos)
                if path_end == -1:
                    break

                file_path = file_index_data[pos:path_end].decode('utf-8', errors='ignore')
                pos = path_end + 1

                # Read size (4 bytes, comes AFTER path)
                if pos + 4 > len(file_index_data):
                    break
                size = struct.unpack('<I', file_index_data[pos:pos+4])[0]
                pos += 4

                # Read timestamp if present (4 bytes)
                timestamp = None
                if self.header['has_timestamps']:
                    if pos + 4 > len(file_index_data):
                        break
                    timestamp = struct.unpack('<I', file_index_data[pos:pos+4])[0]
                    pos += 4

                # Create entry
                entry = PackFileEntry(file_path, size, current_offset, timestamp)
                entries.append(entry)

                # Calculate next offset (with padding if enabled)
                if self.header['data_padded']:
                    # Pad to 8-byte boundary
                    current_offset += ((size + 7) // 8) * 8
                else:
                    current_offset += size

            self.entries = entries

            # Calculate where file data starts
            self.file_data_offset = header_size + self.header['pf_index_size'] + self.header['file_index_size']

            return entries

    def list_files(self, pattern: Optional[str] = None) -> List[PackFileEntry]:
        """List all files in the pack, optionally filtered by pattern."""
        if not self.entries:
            self.read_file_index()

        if pattern:
            pattern_lower = pattern.lower()
            return [e for e in self.entries if pattern_lower in e.path.lower()]

        return self.entries

    def extract_file(self, entry: PackFileEntry, output_path: Optional[Path] = None) -> bytes:
        """Extract a single file from the pack."""
        if not self.entries:
            self.read_file_index()

        with open(self.pack_path, 'rb') as f:
            # Seek to file data
            f.seek(self.file_data_offset + entry.offset)
            data = f.read(entry.size)

        # Optionally write to file
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(data)

        return data

    def get_file_info(self) -> Dict:
        """Get summary information about the pack file."""
        if not self.entries:
            self.read_file_index()

        # Categorize files by extension
        extensions = {}
        total_size = 0

        for entry in self.entries:
            ext = Path(entry.path).suffix.lower()
            if not ext:
                ext = '.no_extension'

            if ext not in extensions:
                extensions[ext] = {'count': 0, 'size': 0}

            extensions[ext]['count'] += 1
            extensions[ext]['size'] += entry.size
            total_size += entry.size

        return {
            'file_count': len(self.entries),
            'total_size': total_size,
            'extensions': extensions,
            'header': self.header,
        }


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python3 pack_reader.py <pack_file> [command]")
        print("\nCommands:")
        print("  info           - Show pack file information (default)")
        print("  list           - List all files in pack")
        print("  list <pattern> - List files matching pattern")
        print("  extract <file> - Extract specific file")
        sys.exit(1)

    pack_file = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else 'info'

    try:
        reader = PFH5Reader(pack_file)

        if command == 'info':
            print(f"📦 Pack File: {pack_file}")
            print("=" * 80)

            reader.read_header()
            print("\n📋 HEADER INFO:")
            print(f"  Format: {reader.header['preamble']}")
            print(f"  Pack Type: {reader.header['pack_type']}")
            print(f"  File Count: {reader.header['file_index_count']}")
            print(f"  Encrypted: {reader.header['index_encrypted']}")
            print(f"  Has Timestamps: {reader.header['has_timestamps']}")

            if not reader.header['index_encrypted']:
                info = reader.get_file_info()
                print(f"\n📊 FILE STATISTICS:")
                print(f"  Total Files: {info['file_count']}")
                print(f"  Total Size: {info['total_size'] / (1024*1024):.1f} MB")

                print(f"\n📁 FILE TYPES (Top 10):")
                sorted_exts = sorted(
                    info['extensions'].items(),
                    key=lambda x: x[1]['count'],
                    reverse=True
                )
                for ext, data in sorted_exts[:10]:
                    size_mb = data['size'] / (1024 * 1024)
                    print(f"  {ext:20s} : {data['count']:6d} files ({size_mb:8.1f} MB)")

        elif command == 'list':
            pattern = sys.argv[3] if len(sys.argv) > 3 else None
            entries = reader.list_files(pattern)

            if pattern:
                print(f"📋 Files matching '{pattern}': {len(entries)}")
            else:
                print(f"📋 All files: {len(entries)}")

            print("=" * 80)
            for entry in entries[:100]:  # Limit to first 100
                size_kb = entry.size / 1024
                print(f"  {size_kb:10.1f} KB - {entry.path}")

            if len(entries) > 100:
                print(f"\n... and {len(entries) - 100} more files")

        elif command == 'extract':
            if len(sys.argv) < 4:
                print("Error: Please specify file to extract")
                sys.exit(1)

            file_path = sys.argv[3]
            entries = reader.list_files()

            # Find matching entry
            entry = None
            for e in entries:
                if e.path == file_path or e.path.endswith(file_path):
                    entry = e
                    break

            if not entry:
                print(f"❌ File not found: {file_path}")
                sys.exit(1)

            output_path = Path('extracted') / entry.path
            reader.extract_file(entry, output_path)
            print(f"✅ Extracted: {entry.path} -> {output_path}")

        else:
            print(f"❌ Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
