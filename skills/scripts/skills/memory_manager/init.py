"""Project memory initialization module."""

import argparse
import sys
from pathlib import Path


# SHARED PROMPTS
PROJECT_MEMORY_CLAUDE_MD = """# memory/

Session-based project memory and learning capture.

## Files

| File               | What                              | When to read                      |
| ------------------ | --------------------------------- | --------------------------------- |
| `memory.md`        | Recent learnings, quick reference | Start of every session            |
| `MASTER-MEMORY.md` | Chronological session index       | Finding specific past session     |
| `README.md`        | Memory system architecture        | Understanding memory organization |

## Subdirectories

| Directory   | What                          | When to read                   |
| ----------- | ----------------------------- | ------------------------------ |
| `sessions/` | Date-organized detailed files | Researching past work patterns |

## Usage

Read `memory.md` at session start for context continuity.
Session files: `sessions/YYYY-MM-DD/S-N-MEM.md`
"""

PROJECT_MEMORY_README = """# Project Memory Architecture

## Overview

Session-based memory captures learnings from each development session. Enables context continuity across conversations and preserves invisible knowledge not evident from code or git history.

## Structure

**memory.md** - Quick reference loaded at session start. Contains 3-5 most recent sessions' key learnings. Updated automatically after each session capture. Token budget: ~300 tokens max.

**MASTER-MEMORY.md** - Chronological index of all sessions. Each entry: date, session number, 1-2 sentence summary, key topics. Enables fast temporal browsing without reading full session files.

**sessions/** - Detailed session files organized by date:
- Format: `YYYY-MM-DD/S-N-MEM.md`
- Sequential numbering (S-1, S-2, S-3) per day
- Full schema: context, goals, bugs, patterns, decisions, invisible knowledge

## Memory Lifecycle

**Session Start:**
- Agent reads memory.md for quick context
- Consults MASTER-MEMORY.md if searching for specific past work
- Drills into session files via references when needed

**Session End (user-triggered):**
- Memory skill analyzes conversation history
- Extracts learnings per schema
- Creates sessions/YYYY-MM-DD/S-N-MEM.md
- Updates MASTER-MEMORY.md with summary
- Refreshes memory.md with recent learnings

## Design Decisions

**Why date-based subdirectories?** Human-readable chronological browsing. Prevents flat directory pollution. Aligns with temporal recall patterns.

**Why memory.md separate from MASTER-MEMORY.md?** Quick context loading without processing full history. Memory.md optimized for auto-loading, MASTER-MEMORY.md for searching.

**Why session numbering resets per day?** Natural temporal grouping. S-1-MEM.md, S-2-MEM.md within same day clearer than global sequential numbering.

## Integration

Memory integrates with:
- Skills: Planner can inject memory context into planning
- Agents: All agents can reference memory via Read tool
- Conventions: Follows temporal.md (timeless present) and documentation.md (token budgets)
"""

MEMORY_MD_INITIAL = """# Recent Learnings

No sessions captured yet. This file will be populated after first session capture.

Use memory-manager skill to capture session learnings.
"""

MASTER_MEMORY_INITIAL = """# Session Index

Chronological index of all sessions with summaries.

## Format

Each entry:
- **YYYY-MM-DD Session N:** 1-2 sentence summary
- **Key Topics:** topic1, topic2, topic3

---

No sessions captured yet.
"""


# CONFIGURATION
MODULE_NAME = "memory_manager.init"


# DOMAIN LOGIC
def create_project_memory(project_dir: Path) -> None:
    """Create project memory directory structure.

    Args:
        project_dir: Root directory of the project
    """
    memory_dir = project_dir / "memory"
    sessions_dir = memory_dir / "sessions"

    # Check if already exists
    if memory_dir.exists():
        print(f"Memory directory already exists at {memory_dir}")
        print("Skipping initialization (operation is idempotent)")
        return

    # Create directories
    memory_dir.mkdir(parents=True, exist_ok=True)
    sessions_dir.mkdir(exist_ok=True)

    # Write documentation files
    claude_md = memory_dir / "CLAUDE.md"
    readme_md = memory_dir / "README.md"
    memory_md = memory_dir / "memory.md"
    master_memory_md = memory_dir / "MASTER-MEMORY.md"

    claude_md.write_text(PROJECT_MEMORY_CLAUDE_MD)
    readme_md.write_text(PROJECT_MEMORY_README)
    memory_md.write_text(MEMORY_MD_INITIAL)
    master_memory_md.write_text(MASTER_MEMORY_INITIAL)

    print(f"✓ Created memory structure at {memory_dir}")
    print(f"✓ Created CLAUDE.md and README.md")
    print(f"✓ Initialized memory.md and MASTER-MEMORY.md")
    print(f"✓ Created sessions/ subdirectory")


# WORKFLOW
def main():
    """Main entry point for project memory initialization."""
    parser = argparse.ArgumentParser(
        description="Initialize project memory structure"
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        required=True,
        help="Root directory of the project"
    )

    args = parser.parse_args()

    if not args.project_dir.exists():
        print(f"Error: Project directory does not exist: {args.project_dir}")
        sys.exit(1)

    create_project_memory(args.project_dir)


if __name__ == "__main__":
    main()
