---
name: memory-manager
module: skills.memory_manager
description: Session memory capture and global memory management
---

# Memory Manager Skill

Manages project-level session memory and global memory patterns.

## Operations

### Initialize Project Memory
Creates memory directory structure for a project:
- memory/ directory with subdirectories
- CLAUDE.md and README.md documentation
- Empty memory.md and MASTER-MEMORY.md files
- sessions/ directory for detailed session files

**Invocation:**
"Use your memory-manager skill to initialize memory for this project"

### Capture Session
Three-step workflow to capture session learnings:
1. **Analyze** - Extract session info from conversation history
2. **Structure** - Organize learnings per memory schema
3. **Persist** - Write session file, update MASTER-MEMORY.md and memory.md

**Invocation:**
"Use your memory-manager skill to capture this session"

### Setup Global Memory
One-time initialization of global memory structure:
- Creates ~/.claude/global-memory/ directory
- Sets up patterns/ and decisions/ subdirectories
- Creates CLAUDE.md, README.md, index.md
- Populates initial pattern and decision files

**Invocation:**
"Use your memory-manager skill to setup global memory"

## Implementation

Python modules in `~/.claude/skills/scripts/skills/memory_manager/`:
- `init.py` - Project memory initialization
- `capture.py` - Session capture workflow
- `global_init.py` - Global memory setup
- `schema.py` - Pydantic validation schemas

All modules follow book pattern structure.
