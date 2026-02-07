"""Session memory capture workflow."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from .schema import SessionMemory, MasterMemoryEntry


# SHARED PROMPTS
MEMORY_SCHEMA_EXAMPLE = """
Session Memory Schema:
- session_number: Sequential number for the day (1, 2, 3...)
- date: YYYY-MM-DD format
- time: HH:MM format
- context:
  - working_directory: Primary working directory
  - primary_goal: Main objective of the session
  - duration: Approximate duration (e.g., "~2 hours")
- goals_accomplished: List of specific outcomes achieved
- bugs_fixed: List with description, root_cause, solution, prevention
- patterns_discovered: Reusable architectural or debugging insights
- problem_solutions: List with problem and solution pairs
- future_avoidance: Prevention strategies for mistakes
- notable_decisions: List with description, rationale, trade_offs, alternatives_rejected
- invisible_knowledge: Rationale not evident from code
- references:
  - related_sessions: List of session references
  - files_modified: List of file paths
  - external_links: List of URLs
"""


# CONFIGURATION
MODULE_PATH = "skills.memory_manager.capture"


# MESSAGE TEMPLATES

# --- STEP 1: ANALYZE ---
ANALYZE_INSTRUCTIONS = """Extract session information from the conversation history.

Analyze the current conversation and identify:
1. Primary working directory
2. Main goal or objective of this session
3. Specific goals that were accomplished
4. Any bugs that were fixed (with root causes and solutions)
5. Patterns or insights discovered
6. Notable decisions made with rationale
7. Any invisible knowledge (WHY things were done certain ways)

Focus on learnings that would be valuable for future sessions. Ignore routine operations.

Output your analysis as a structured summary following the memory schema.
"""

# --- STEP 2: STRUCTURE ---
STRUCTURE_INSTRUCTIONS = """Structure the session learnings per the memory schema.

Convert your analysis into the proper session memory format:

{schema_example}

Ensure all fields follow conventions:
- Use timeless present tense (describe what WAS learned, not what WAS done)
- Avoid change-relative language ("Added X", "Fixed Y", "TODO")
- Focus on WHY and learnings, not just WHAT changed
- Include prevention strategies for bugs
- Document rationale for decisions

Output the structured data as JSON matching the SessionMemory schema.
"""

# --- STEP 3: PERSIST ---
PERSIST_INSTRUCTIONS = """Write the session memory to files.

Based on the structured session data:
1. Determine the session file path: sessions/YYYY-MM-DD/S-N-MEM.md
2. Write the session file in markdown format
3. Update MASTER-MEMORY.md with a 1-2 sentence summary
4. Update memory.md with recent learnings (keep 3-5 most recent)

Ensure:
- Session numbering is sequential per day
- Date subdirectories are created as needed
- MASTER-MEMORY.md maintains chronological order
- memory.md stays within ~300 token budget

Output confirmation of files written with paths.
"""


# PARSING FUNCTIONS
def parse_session_data(json_str: str) -> SessionMemory:
    """Parse and validate session data from JSON string.

    Args:
        json_str: JSON string matching SessionMemory schema

    Returns:
        Validated SessionMemory instance

    Raises:
        ValidationError: If data doesn't match schema
    """
    data = json.loads(json_str)
    return SessionMemory(**data)


# MESSAGE BUILDERS
def build_analyze_message() -> str:
    """Build step 1 message for analysis."""
    return ANALYZE_INSTRUCTIONS


def build_structure_message() -> str:
    """Build step 2 message for structuring."""
    return STRUCTURE_INSTRUCTIONS.format(schema_example=MEMORY_SCHEMA_EXAMPLE)


def build_persist_message() -> str:
    """Build step 3 message for persistence."""
    return PERSIST_INSTRUCTIONS


# DOMAIN LOGIC
def get_next_session_number(project_dir: Path, date_str: str) -> int:
    """Determine next session number for the given date.

    Args:
        project_dir: Project root directory
        date_str: Date in YYYY-MM-DD format

    Returns:
        Next sequential session number (1, 2, 3...)
    """
    sessions_dir = project_dir / "memory" / "sessions" / date_str
    if not sessions_dir.exists():
        return 1

    # Find existing session files
    existing = list(sessions_dir.glob("S-*-MEM.md"))
    if not existing:
        return 1

    # Extract numbers and find max
    numbers = []
    for f in existing:
        # Parse S-N-MEM.md format
        try:
            num = int(f.stem.split("-")[1])
            numbers.append(num)
        except (IndexError, ValueError):
            continue

    return max(numbers) + 1 if numbers else 1


def write_session_file(
    project_dir: Path,
    session: SessionMemory
) -> Path:
    """Write session memory file.

    Args:
        project_dir: Project root directory
        session: Validated session memory data

    Returns:
        Path to written session file
    """
    sessions_dir = project_dir / "memory" / "sessions" / session.date
    sessions_dir.mkdir(parents=True, exist_ok=True)

    session_file = sessions_dir / f"S-{session.session_number}-MEM.md"

    # Format session as markdown
    content = f"""# Session {session.session_number} - {session.date} {session.time}

## Context

- **Working Directory**: {session.context.working_directory}
- **Primary Goal**: {session.context.primary_goal}
"""
    if session.context.duration:
        content += f"- **Duration**: {session.context.duration}\n"

    content += "\n## Goals Accomplished\n\n"
    for goal in session.goals_accomplished:
        content += f"- {goal}\n"

    if session.bugs_fixed:
        content += "\n## Bugs Fixed\n\n"
        for bug in session.bugs_fixed:
            content += f"### {bug.description}\n\n"
            content += f"- **Root Cause**: {bug.root_cause}\n"
            content += f"- **Solution**: {bug.solution}\n"
            if bug.prevention:
                content += f"- **Prevention**: {bug.prevention}\n"
            content += "\n"

    if session.patterns_discovered:
        content += "## Patterns Discovered\n\n"
        for pattern in session.patterns_discovered:
            content += f"- {pattern}\n"
        content += "\n"

    if session.problem_solutions:
        content += "## Problem-Solution Pairs\n\n"
        for ps in session.problem_solutions:
            content += f"### Problem\n{ps.problem}\n\n"
            content += f"### Solution\n{ps.solution}\n\n"

    if session.future_avoidance:
        content += "## Future Avoidance\n\n"
        for avoidance in session.future_avoidance:
            content += f"- {avoidance}\n"
        content += "\n"

    if session.notable_decisions:
        content += "## Notable Decisions\n\n"
        for decision in session.notable_decisions:
            content += f"### {decision.description}\n\n"
            content += f"- **Rationale**: {decision.rationale}\n"
            if decision.trade_offs:
                content += f"- **Trade-offs**: {decision.trade_offs}\n"
            if decision.alternatives_rejected:
                content += f"- **Alternatives Rejected**: {', '.join(decision.alternatives_rejected)}\n"
            content += "\n"

    if session.invisible_knowledge:
        content += "## Invisible Knowledge\n\n"
        for knowledge in session.invisible_knowledge:
            content += f"- {knowledge}\n"
        content += "\n"

    if session.references:
        content += "## References\n\n"
        for ref_type, ref_list in session.references.items():
            if ref_list:
                content += f"- **{ref_type.replace('_', ' ').title()}**: {', '.join(ref_list)}\n"

    session_file.write_text(content)
    return session_file


def update_master_memory(
    project_dir: Path,
    session: SessionMemory,
    summary: str,
    key_topics: list[str]
) -> None:
    """Update MASTER-MEMORY.md with new session entry.

    Args:
        project_dir: Project root directory
        session: Session memory data
        summary: 1-2 sentence summary of session
        key_topics: List of main topics covered
    """
    master_file = project_dir / "memory" / "MASTER-MEMORY.md"

    entry = f"\n## {session.date} Session {session.session_number}\n\n"
    entry += f"{summary}\n\n"
    entry += f"**Key Topics:** {', '.join(key_topics)}\n"

    # Append to file
    current = master_file.read_text()
    if "No sessions captured yet" in current:
        # Replace placeholder
        current = current.replace("No sessions captured yet.", "")

    master_file.write_text(current + entry)


def update_memory_md(
    project_dir: Path,
    session: SessionMemory,
    summary: str
) -> None:
    """Update memory.md with recent learnings.

    Args:
        project_dir: Project root directory
        session: Session memory data
        summary: Brief summary of session
    """
    memory_file = project_dir / "memory" / "memory.md"

    # Create a simple entry
    entry = f"\n## Session {session.session_number} ({session.date})\n\n{summary}\n"

    # For simplicity, just append for now
    # In production, would maintain only 3-5 most recent
    current = memory_file.read_text()
    if "No sessions captured yet" in current:
        current = "# Recent Learnings\n"

    memory_file.write_text(current + entry)


# WORKFLOW
def get_step_guidance(step: int, module_path: str, **kwargs) -> Dict[str, Any]:
    """Get guidance for each workflow step.

    Args:
        step: Current step number
        module_path: Module path for invocation
        **kwargs: Additional arguments (unused)

    Returns:
        Dict with title, actions, and next command
    """
    if step == 1:
        return {
            "title": "Analyze Conversation",
            "actions": build_analyze_message(),
            "next": f"python3 -m {module_path} --step 2"
        }
    elif step == 2:
        return {
            "title": "Structure Session Data",
            "actions": build_structure_message(),
            "next": f"python3 -m {module_path} --step 3"
        }
    elif step == 3:
        return {
            "title": "Persist Session Memory",
            "actions": build_persist_message(),
            "next": None
        }
    else:
        return {
            "title": "Invalid Step",
            "actions": f"Step {step} is not valid. Use steps 1-3.",
            "next": None
        }


def main():
    """Main entry point for session capture workflow."""
    parser = argparse.ArgumentParser(
        description="Capture session memory"
    )
    parser.add_argument("--step", type=int, required=True)
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project root directory"
    )

    args = parser.parse_args()

    guidance = get_step_guidance(args.step, MODULE_PATH)

    # Simple output format
    print(f"=== {guidance['title']} ===\n")
    print(guidance['actions'])
    if guidance.get('next'):
        print(f"\n\nNext: {guidance['next']}")


if __name__ == "__main__":
    main()
