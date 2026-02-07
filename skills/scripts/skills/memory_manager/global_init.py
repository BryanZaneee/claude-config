"""Global memory initialization module."""

import sys
from pathlib import Path


# CONFIGURATION
GLOBAL_MEMORY_DIR = Path.home() / ".claude" / "global-memory"


# DOMAIN LOGIC
def create_global_memory() -> None:
    """Create global memory directory structure.

    Creates ~/.claude/global-memory/ with:
    - patterns/ subdirectory
    - decisions/ subdirectory
    - CLAUDE.md, README.md, index.md
    """
    # Check if already exists
    if GLOBAL_MEMORY_DIR.exists():
        print(f"Global memory directory already exists at {GLOBAL_MEMORY_DIR}")
        print("Skipping initialization (operation is idempotent)")
        return

    # Create directories
    patterns_dir = GLOBAL_MEMORY_DIR / "patterns"
    decisions_dir = GLOBAL_MEMORY_DIR / "decisions"

    GLOBAL_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    patterns_dir.mkdir(exist_ok=True)
    decisions_dir.mkdir(exist_ok=True)

    print(f"✓ Created global memory structure at {GLOBAL_MEMORY_DIR}")
    print(f"✓ Created patterns/ and decisions/ subdirectories")
    print(f"✓ Global memory ready for pattern population")


# WORKFLOW
def main():
    """Main entry point for global memory initialization."""
    create_global_memory()


if __name__ == "__main__":
    main()
