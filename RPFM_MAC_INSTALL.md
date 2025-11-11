# Installing RPFM on macOS

RPFM (Rusted PackFile Manager) is the tool needed to extract Total War pack files. Here's how to install it on your Mac.

## Option 1: Download Pre-built Binary (Easiest)

### Step 1: Download RPFM

Visit the releases page:
```
https://github.com/Frodo45127/rpfm/releases
```

Download the macOS version:
- Look for the latest release
- Download: `rpfm-macos.zip` or `rpfm-release-macos-x86_64.zip`
- For M1/M2 Macs: Look for ARM64 version if available

### Step 2: Extract and Install

```bash
# Navigate to Downloads
cd ~/Downloads

# Extract the zip file
unzip rpfm-*.zip

# Make it executable
chmod +x rpfm

# Move to a directory in your PATH
sudo mv rpfm /usr/local/bin/

# Verify installation
rpfm --version
```

### Step 3: Fix macOS Security (if needed)

If you get a security warning:

1. Go to **System Preferences → Security & Privacy**
2. Click "Open Anyway" for rpfm
3. Or run:
```bash
xattr -d com.apple.quarantine /usr/local/bin/rpfm
```

## Option 2: Build from Source

If pre-built binaries don't work:

### Requirements

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Install Qt5 (required for RPFM GUI)
brew install qt@5

# Install CMake
brew install cmake
```

### Build RPFM

```bash
# Clone the repository
git clone https://github.com/Frodo45127/rpfm.git
cd rpfm

# Build (this takes 5-15 minutes)
cargo build --release

# The binary will be at: target/release/rpfm
# Move it to your PATH
sudo cp target/release/rpfm /usr/local/bin/

# Verify
rpfm --version
```

## Option 3: Use Docker (Alternative)

If you have Docker installed:

```bash
# Pull RPFM docker image (if available)
docker pull rpfm/rpfm:latest

# Run RPFM in container
docker run -v /path/to/game/data:/data -v ./extracted:/output rpfm/rpfm extract /data/data.pack /output
```

## Troubleshooting

### "rpfm: command not found"

Check if `/usr/local/bin` is in your PATH:
```bash
echo $PATH
```

Add it to your shell config (~/.zshrc for Oh My Zsh):
```bash
export PATH="/usr/local/bin:$PATH"
```

Then reload:
```bash
source ~/.zshrc
```

### "Cannot open rpfm because it is from an unidentified developer"

Remove the quarantine attribute:
```bash
xattr -d com.apple.quarantine /usr/local/bin/rpfm
```

Or right-click the file in Finder → Open → Click "Open" when prompted.

### M1/M2 Mac Compatibility Issues

If RPFM doesn't work natively on Apple Silicon:

1. **Use Rosetta 2**:
```bash
arch -x86_64 rpfm --version
```

2. **Build from source** with native ARM support:
```bash
rustup target add aarch64-apple-darwin
cargo build --release --target aarch64-apple-darwin
```

## Using RPFM

### GUI Mode (Recommended for browsing)

```bash
# Just run rpfm to open GUI
rpfm
```

Then:
1. File → Open → Select `.pack` file
2. Browse contents
3. Right-click folder → Extract

### CLI Mode (For automation)

Check available commands:
```bash
rpfm --help
```

Extract a pack file:
```bash
rpfm extract /path/to/data.pack ./extracted/data/
```

## Quick Test

Verify RPFM works with your game:

```bash
# List contents of a pack file
rpfm list /TotalWarPharaohDynastiesData/data/data.pack

# Extract data_db.pack (small test)
mkdir -p ./test_extract
rpfm extract /TotalWarPharaohDynastiesData/data/data_db.pack ./test_extract/

# Check if it worked
ls ./test_extract/
```

## Alternative Tools (if RPFM doesn't work)

### 1. PFM (PackFile Manager)
- Older but more stable on some systems
- Download: https://github.com/Frodo45127/PFM

### 2. CA's Official Tools
- Total War Assembly Kit (if available for PHARAOH)
- Check Steam: Total War PHARAOH → Tools

### 3. Manual extraction using Python libraries
If all else fails, there are Python libraries that can read pack files:
- `python-totalwar` (if available)
- Custom parsers based on CA pack format documentation

## Next Steps

Once RPFM is installed:

1. **Test extraction**:
```bash
rpfm extract /TotalWarPharaohDynastiesData/data/data_db.pack ./extracted/
```

2. **Use our extraction tools**:
```bash
python3 extract_game_data.py all
```

3. **Explore the data**:
```bash
cat ./output/units.json
```

## Getting Help

If you're still having trouble:

1. **Check RPFM issues**: https://github.com/Frodo45127/rpfm/issues
2. **Total War modding discord**: Usually has RPFM help channels
3. **Let me know** - I can help troubleshoot or create alternative extraction methods

---

**Quick Install Summary for Mac:**

```bash
# Download from GitHub releases
open https://github.com/Frodo45127/rpfm/releases

# After download:
cd ~/Downloads
unzip rpfm-*.zip
chmod +x rpfm
sudo mv rpfm /usr/local/bin/
xattr -d com.apple.quarantine /usr/local/bin/rpfm
rpfm --version

# Test it
rpfm --help
```
