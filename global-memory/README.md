# Global Memory Architecture

## Overview

Global memory stores cross-project patterns, decisions, and insights that transcend individual projects. Unlike project-level memory (session-based learnings), global memory captures universal knowledge applicable across all development work.

## Structure

**index.md** - Central cross-reference index linking to all pattern and decision files. Enables quick navigation to relevant knowledge areas.

**patterns/** - Reusable solutions to recurring problems:
- architectural-patterns.md - System design patterns, component organization
- debugging-strategies.md - Investigation techniques, root cause analysis
- common-pitfalls.md - Frequent mistakes and prevention strategies
- technology-insights.md - Framework-specific knowledge, API patterns

**decisions/** - Documented choices and rationale:
- tool-choices.md - Technology selection decisions with trade-offs
- approach-preferences.md - Preferred methodologies and workflows

## Design Rationale

**Why separate from project memory?** Project memory captures session-specific context (what was accomplished, bugs fixed). Global memory captures timeless knowledge (how to approach problems, which tools work best). Mixing creates noise and dilutes both.

**Why categorized files instead of flat structure?** Categories enable faster navigation. Architectural patterns have different usage context than debugging strategies. Separation by concern improves discoverability.

**Why manual population instead of automatic extraction?** Pattern recognition requires judgment about universality. Automatic extraction risks capturing project-specific details as universal patterns. Manual curation ensures high signal-to-noise ratio.

## Integration

Agents consult global memory when:
- Encountering unfamiliar architectural decisions
- Debugging recurring issue types
- Choosing between alternative technical approaches
- Needing framework-specific best practices

Global memory accessed on-demand, not auto-loaded. Prevents context pollution with irrelevant knowledge.
