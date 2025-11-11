# CLAUDE CODE WORKING RULES

## CRITICAL: ALWAYS ASK BEFORE GUESSING
- Never assume file locations, file formats, or directory structures
- Always request command output before writing code
- One step at a time - wait for confirmation

## INFORMATION GATHERING FIRST
Before writing ANY code, you MUST ask for information:
- "Run this command and send me the output: [command]"
- "What do you see when you run: ls -la [directory]"
- "Run: file [filepath] - what is the file type?"

NEVER guess. ALWAYS ask.

### MULTIPLE QUERY COMMANDS
IF you need multiple pieces of information before continuing, you CAN combine them:

Example:
```bash
# Run all these commands and send me ALL outputs:

# 1. Find game directory
find ~/Library -name "*Pharaoh*" -type d 2>/dev/null | pbcopy && pbpaste

# 2. Check Python version
python3 --version | pbcopy && pbpaste

# 3. List game files
ls -la [game-directory] | pbcopy && pbpaste
```

This way I get all information needed in one round.

### AUTO-COPY TO CLIPBOARD (Mac)
Add `| pbcopy && pbpaste` to commands so output is automatically copied:
```bash
# Without auto-copy:
git status

# With auto-copy (PREFERRED):
git status | pbcopy && pbpaste
```

The `pbcopy` copies to clipboard, `pbpaste` shows output in terminal.
You can then just Cmd+V to paste the result.

## SYNC BETWEEN CLAUDE CODE WEB AND LOCAL ENVIRONMENT

### CRITICAL: When Claude Code creates/modifies files
You MUST provide commands to sync changes to local environment:
```bash
# 1. Pull changes from Claude Code to local
git pull origin main

# 2. Verify what changed
git log -1 --stat | pbcopy && pbpaste

# 3. Open in local IDE (Cursor)
cursor .
# OR
code .
```

### WORKFLOW: Claude Code → Local → Test → Push

**After Claude Code makes changes:**
```bash
# Step 1: Sync from Claude Code to local
git pull origin main | pbcopy && pbpaste

# Step 2: Review changes
git diff HEAD~1 | pbcopy && pbpaste

# Step 3: Open in Cursor to review
cursor .

# Step 4: Test locally
python3 explore.py | pbcopy && pbpaste

# Step 5: If changes needed, commit from local
git add .
git commit -m "[description]"
git push origin main | pbcopy && pbpaste
```

## CODE DELIVERY FORMAT
Every time you write code, you MUST provide:

📝 WHAT WE'RE BUILDING:
[Brief explanation]

💾 FILES:
[List files and their purpose]

🔄 SYNC COMMANDS (run FIRST):
```bash
# Pull Claude Code changes to local
git pull origin main | pbcopy && pbpaste

# Open in Cursor
cursor .
```

✅ TEST COMMANDS (run in exact order):
1️⃣ pwd
2️⃣ python3 [script].py | pbcopy && pbpaste
3️⃣ Expected output: [describe]

📊 GIT COMMANDS (if you made local changes):
```bash
git status | pbcopy && pbpaste
# [wait for analysis]
git add [files]
git commit -m "[message]"
git push origin main | pbcopy && pbpaste
```

⏸️ STOP HERE - Wait for results

## GIT STATUS ANALYSIS
When user sends git status output:
1. Analyze what changed
2. Explain the changes
3. Provide specific git commands WITH pbcopy:
```bash
# Add files
git add [specific files]

# Commit with descriptive message
git commit -m "[descriptive message]"

# Push to main
git push origin main | pbcopy && pbpaste
```

## WORKFLOW
1. Ask for information (never assume)
   - Can combine multiple query commands if needed
   - Always use | pbcopy && pbpaste for easy copying
2. Wait for output
3. Write code based on ACTUAL data (in Claude Code web)
4. **PROVIDE SYNC COMMANDS** (git pull to get changes locally)
5. Provide test commands (with pbcopy)
6. Wait for results
7. If local changes made: analyze git status
8. Provide git commands (with pbcopy)
9. Repeat

## KEY ENVIRONMENTS
- **Claude Code Web**: Where you write code
- **Local Mac Terminal (Oh My Zsh)**: Where user tests
- **Local IDE (Cursor)**: Where user reviews code

Always provide commands to sync between these environments!