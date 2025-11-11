# Python-Only Pack File Extraction

## Status: Experimental / Partial Implementation

I've created a Python-only pack file reader (`python_pack_reader.py`), but here's the honest assessment:

## The Challenge

Total War pack files use **CA's proprietary format** that:
- Changes between game versions (PFH3, PFH4, PFH5, PFH6)
- Uses complex compression algorithms
- Has undocumented binary structures
- Requires reverse-engineering to fully parse

## What Works

The Python script can:
- ✅ Read pack file headers
- ✅ Identify pack file versions
- ✅ Detect file signatures
- ✅ Show basic pack information
- ✅ Analyze pack structure

## What Doesn't Work Yet

- ❌ Full index parsing (file table)
- ❌ File extraction
- ❌ Decompression
- ❌ Database file parsing

## Why This is Hard

To implement a full Python extractor, we'd need to:

1. **Reverse-engineer the format** - Study RPFM's Rust source code
2. **Handle multiple versions** - PHARAOH might use PFH5 or PFH6
3. **Implement decompression** - Multiple compression schemes used
4. **Parse binary structures** - Complex nested data structures
5. **Test extensively** - Ensure it works with all pack types

**Estimated effort:** 40-80 hours of development + testing

## Alternatives

### Option 1: Use RPFM (Recommended) ⭐

**Time:** 5-10 minutes
**Reliability:** 100%
**Effort:** Minimal

```bash
# Download RPFM
# Extract pack files
# Done!
```

See: `RPFM_MAC_INSTALL.md`

### Option 2: Find Existing Data 🌟

**Time:** 10-30 minutes
**Reliability:** High (if data exists)
**Effort:** Just searching

Search for:
- "Total War Pharaoh database"
- Community modding resources
- Extracted data repositories

### Option 3: Use Python Libraries 🐍

Check if libraries exist:

```bash
python3 python_pack_reader.py check-libs
```

Try installing:
```bash
# These may or may not exist
pip search totalwar
pip search "ca pack"
pip search "total war"
```

### Option 4: Develop Full Python Parser 🔧

If you want to contribute to developing this:

1. **Study RPFM source:**
   ```bash
   git clone https://github.com/Frodo45127/rpfm.git
   # Study: rpfm/src/packfile/
   ```

2. **Read pack format docs:**
   - Total War modding forums
   - RPFM documentation
   - Community reverse-engineering notes

3. **Implement parser:**
   - Start with one pack version (PFH5)
   - Test with small pack files
   - Expand to full format

4. **Share with community:**
   - Publish as Python package
   - Help other Total War modders

## Using the Current Python Script

### Check for Python libraries:

```bash
python3 python_pack_reader.py check-libs
```

### Analyze a pack file:

```bash
python3 python_pack_reader.py analyze /path/to/data.pack
```

This will show:
- Pack file version
- Number of files
- Size information
- Format details

### Attempt extraction (not fully working):

```bash
python3 python_pack_reader.py extract /path/to/data.pack --output ./extracted
```

This will explain current limitations.

## My Recommendation

### For Your Use Case:

Since you want units, buildings, and factions data:

**Best Option: Use RPFM**

1. **Time investment:** 10 minutes to install
2. **Reliability:** 100% - It's the standard tool
3. **One-time setup:** Install once, extract many packs
4. **Works immediately:** No development needed

**Steps:**
```bash
# 1. Download RPFM (see RPFM_MAC_INSTALL.md)
wget https://github.com/Frodo45127/rpfm/releases/latest/download/rpfm-macos.zip

# 2. Install
unzip rpfm-macos.zip
chmod +x rpfm
sudo mv rpfm /usr/local/bin/

# 3. Extract
rpfm extract /path/to/data_db.pack ./extracted/

# 4. Parse with Python
python3 extract_game_data.py all

# Done! You have your data
```

### Alternative: Skip Extraction Entirely

**Search for existing data first:**

1. Google: "Total War Pharaoh units database"
2. Check: r/totalwar subreddit
3. Check: Total War Discord servers
4. Check: Modding forums

Someone may have already done this work!

## Contributing to Python Parser

Want to help develop the full Python parser?

**What we need:**
- CA pack format documentation
- Test pack files (small ones)
- Time to reverse-engineer format
- Rust knowledge (to read RPFM source)

**Potential impact:**
- Help entire Total War modding community
- Make data extraction easier
- Enable Python-based Total War tools

## Questions?

**"Should I spend time on Python parser?"**
- If you need data NOW → No, use RPFM
- If you want to contribute to community → Yes!
- If you enjoy reverse-engineering → Yes!

**"Is RPFM hard to install?"**
- No! Usually takes 5-10 minutes
- See: `RPFM_MAC_INSTALL.md`

**"Can't we just use existing data?"**
- Maybe! Search first before extracting
- Community often shares databases

## Summary

| Method | Time | Reliability | Effort |
|--------|------|-------------|--------|
| **RPFM** | 10 min | ⭐⭐⭐⭐⭐ | ⭐ |
| **Find existing data** | 30 min | ⭐⭐⭐⭐ | ⭐ |
| **Python libraries** | Variable | ⭐⭐⭐ | ⭐⭐ |
| **Develop parser** | 40-80 hrs | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**My advice:** Use RPFM. It's the right tool for the job! 🎯

---

**Want me to:**
- Help you install RPFM?
- Search for existing data online?
- Guide you through extraction?

Just let me know! 🚀
