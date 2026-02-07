# Architectural Patterns

Universal design patterns and component organization strategies applicable across projects.

## Two-File Documentation Pattern

Every directory uses two files for LLM-optimized context:
- **CLAUDE.md** - Tabular navigation index (~200 tokens). Contains file/directory descriptions and "When to read" triggers. Minimizes auto-loaded context.
- **README.md** - Invisible knowledge (~500 tokens). Architecture decisions, invariants not obvious from code. Loaded only when CLAUDE.md trigger fires.

Rationale: Separates navigation (always loaded) from knowledge (just-in-time). Prevents context window pollution while maintaining discoverability.

## Module Organization (Book Pattern)

Skills and complex modules follow standardized section ordering:
1. SHARED PROMPTS - Reusable prompt constants
2. CONFIGURATION - Module-level settings
3. SYSTEM PROMPTS - Agent initialization (if needed)
4. MESSAGE TEMPLATES - Step-delimited messages
5. PARSING FUNCTIONS - Response extraction
6. MESSAGE BUILDERS - Construct prompts
7. DOMAIN LOGIC - Business operations
8. WORKFLOW - Orchestration entry point

Rationale: Dependencies before use. No forward references. Consistent structure enables fast navigation across unfamiliar code.

## Agent Delegation Pattern

Use specialized agents for distinct concerns:
- **architect** (Opus) - Designs plans, never implements
- **developer** (Sonnet) - Translates specs into code+tests
- **technical-writer** (Sonnet) - Documents existing systems
- **quality-reviewer** (Sonnet) - Production risk detection
- **debugger** (Sonnet) - Root cause analysis

Rationale: Role specialization improves output quality. Different models match different cognitive demands (Opus for planning, Sonnet for execution).

## Hierarchical Memory Pattern

Three-tier memory structure:
1. **Quick reference** (memory.md) - Recent learnings, auto-loaded
2. **Session index** (MASTER-MEMORY.md) - Chronological summaries
3. **Detailed sessions** (sessions/YYYY-MM-DD/S-N-MEM.md) - Full context

Rationale: Optimizes for session start speed. Quick reference provides immediate context without scanning full history. Index enables temporal browsing. Details preserved for deep dives.
