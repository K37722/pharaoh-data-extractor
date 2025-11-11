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

## CODE DELIVERY FORMAT
Every time you write code, you MUST provide:

📝 WHAT WE'RE BUILDING:
[Brief explanation]

💾 FILES:
[List files and their purpose]

✅ TEST COMMANDS (run in exact order):
1️⃣ pwd
2️⃣ python [script].py
3️⃣ Expected output: [describe]

📊 GIT COMMANDS:
1️⃣ git status
2️⃣ Send me output - I'll analyze and give next steps

⏸️ STOP HERE - Wait for results

## GIT STATUS ANALYSIS
When I send git status output:
1. Analyze what changed
2. Explain the changes
3. Provide specific git commands

## WORKFLOW
1. Ask for information (never assume)
2. Wait for output
3. Write code based on ACTUAL data
4. Provide test commands
5. Wait for results
6. Analyze git status
7. Provide git commands
8. Repeat
```

Lagre og lukk editoren (vanligvis `:wq` hvis vim, eller `Ctrl+X` hvis nano).

## Steg 7: Start arbeidet

Nå kan du starte med første spørsmål til Claude:
```
I want to extract data from Total War Pharaoh Dynasties game files on my Mac. 
This is a proof of concept - we'll start simple.

What's the first command I should run to find where the game is installed?
