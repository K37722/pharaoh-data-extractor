cat > CLAUDE.md << 'EOF'
# CLAUDE CODE WORKING RULES

Read this file to understand HOW to work with me. 
The WHAT to build will be provided in the conversation.

## CRITICAL: ONLY ASK WHEN YOU NEED INFORMATION

- **If you already have the information** (from our conversation or context) → proceed with code
- **If you're missing information** (file paths, formats, structure) → ask for it first
- Never guess or assume - but don't ask for things you already know

**Examples:**
- ✅ I told you the game path → use it, don't ask again
- ✅ You saw the directory structure → use it in your code
- ❌ You don't know the file format → ask me to check it
- ❌ You're not sure if a directory exists → ask me to verify

## SYNC BETWEEN CLAUDE CODE WEB AND LOCAL ENVIRONMENT

### Claude Code works in BRANCHES
You create a branch like: `claude/feature-name-[id]`

When you create/modify files, provide commands to sync to my local:
```bash
# 1. Fetch all branches
git fetch origin | pbcopy && pbpaste

# 2. Checkout your branch (replace with actual branch name)
git checkout claude/[your-branch-name]

# 3. Pull latest changes
git pull | pbcopy && pbpaste

# 4. Open in Cursor
cursor .
```

**IMPORTANT:** Always tell me your branch name so I can checkout the right branch!

## INFORMATION GATHERING

### Combine multiple query commands when possible:
Instead of asking 5 separate times, combine into one block:
```bash
{
echo "=== COMMAND 1 ===" && [command1] && \
echo -e "\n=== COMMAND 2 ===" && [command2] && \
echo -e "\n=== COMMAND 3 ===" && [command3]
} | tee >(pbcopy)
```

### Always use pbcopy for Mac clipboard:
```bash
# Auto-copy output to clipboard
command | pbcopy && pbpaste
```

## CODE DELIVERY FORMAT

Every time you write code, provide:

📝 WHAT WE'RE BUILDING:
[Brief explanation]

💾 FILES:
[List files and their purpose]

🔄 SYNC COMMANDS (run FIRST):
```bash
# My branch: claude/[branch-name]

# Fetch and checkout my branch
git fetch origin
git checkout claude/[branch-name]
git pull | pbcopy && pbpaste

# Open in Cursor
cursor .
```

✅ TEST COMMANDS (run in local terminal):
```bash
1️⃣ pwd
2️⃣ python3 script.py | pbcopy && pbpaste
```

Expected output: [describe]

📊 AFTER TESTING - Check status:
```bash
git status | pbcopy && pbpaste
# [send me output]
```

⏸️ STOP HERE - Wait for results

## GIT STATUS ANALYSIS

When I send git status output from your branch:

**If changes look good:**
```bash
# Merge your branch to main
git checkout main
git merge claude/[branch-name] | pbcopy && pbpaste
git push origin main | pbcopy && pbpaste
```

**If I made local changes:**
```bash
git add [specific files]
git commit -m "[descriptive message]"
git push origin claude/[branch-name] | pbcopy && pbpaste
```

## COMPLETE WORKFLOW

1. I ask you to build something
2. You create a branch: `claude/feature-name-[id]`
3. **You tell me the branch name**
4. You write code in that branch
5. **You give me commands to checkout your branch**
6. I fetch, checkout, and pull your branch
7. I review in Cursor and test in terminal
8. I send you git status
9. If good → I merge to main
10. If changes needed → I push to your branch
11. Repeat

## KEY ENVIRONMENTS

- **Claude Code Web**: Where you write code (in branches)
- **Local Mac Terminal (Oh My Zsh)**: Where I test
- **Cursor IDE**: Where I review code

## BRANCH NAMING

You typically create branches like:
- `claude/feature-name-[random-id]`
- Example: `claude/pharaoh-data-extractor-mvp-011CV25wL5rXTGxK7HPJFx7c`

Always tell me the full branch name!

---

*This file contains only HOW to work. The WHAT to build is in the conversation.*
EOF