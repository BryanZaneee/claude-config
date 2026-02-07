# Memory Manager Skill Architecture

## Overview

Memory manager skill provides three operations:
1. Project memory initialization - Create directory structure
2. Session capture - Extract and persist learnings from conversations
3. Global memory setup - One-time initialization of cross-project patterns

## Implementation Structure

Python modules in `~/.claude/skills/scripts/skills/memory_manager/`:

**schema.py** - Pydantic models for validation:
- SessionMemory - Full session schema
- MasterMemoryEntry - Summary index entry
- QuickMemory - Recent learnings for memory.md

**init.py** - Project memory initialization:
- Creates memory/ directory structure
- Writes CLAUDE.md and README.md templates
- Initializes empty memory.md and MASTER-MEMORY.md
- Creates sessions/ subdirectory

**capture.py** - Session capture workflow:
- Step 1: Analyze conversation history, extract session info
- Step 2: Structure learnings per schema (goals, bugs, patterns, decisions)
- Step 3: Persist to session file, update MASTER-MEMORY.md and memory.md

**global_init.py** - Global memory setup:
- Creates ~/.claude/global-memory/ structure
- Writes documentation (CLAUDE.md, README.md, index.md)
- Creates pattern and decision files with initial content

## Design Decisions

**Why Pydantic for validation?** Ensures schema compliance before file writes. Type-safe data handling. Clear error messages for malformed data.

**Why three-step capture workflow?** Separates concerns (analysis, structuring, persistence). Enables inspection at each stage. Aligns with workflow lib patterns.

**Why book pattern structure?** Consistent organization across all skills. Dependencies before use. No forward references.

**Why separate init from capture?** Initialization is one-time setup. Capture is recurring operation. Different concerns, different modules.

## Integration

Uses shared workflow library:
- `subagent_dispatch()` - If delegation needed
- `format_step()` - Step-delimited message formatting
- `format_file_content()` - File content display

Follows memory.md conventions:
- Timeless present tense
- Token budget enforcement
- Schema compliance
- Session numbering rules
