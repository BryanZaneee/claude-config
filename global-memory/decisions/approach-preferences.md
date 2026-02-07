# Approach Preferences

Preferred development methodologies and workflow patterns.

## Planning Before Implementation

**Preference:** Explore → Plan → Execute for non-trivial changes.

**Rationale:**
- Reduces wasted effort from wrong approach
- Enables user review before code written
- Clarifies requirements and edge cases upfront
- Plans persist across `/clear`, preserving reasoning

**When to skip:** Trivial single-file changes, obvious bug fixes, simple feature additions with clear requirements.

## Integration Tests Over Unit Tests

**Preference:** Integration > property > unit testing hierarchy.

**Rationale:**
- Integration tests validate actual behavior, not implementation details
- Unit tests become brittle with refactoring
- Property tests find edge cases unit tests miss

**Usage:**
- Integration: API endpoints, user workflows, component interactions
- Property: Complex logic with many input variations
- Unit: Pure functions with no dependencies

## Batched Operations Over Sequential

**Preference:** Batch independent operations when possible.

**Rationale:** Parallel tool calls reduce total latency. Single message with multiple Bash/Read/Grep calls faster than sequential messages.

**When not to batch:** Operations with dependencies (e.g., Write before git commit, mkdir before file creation).

## Timeless Present Tense

**Preference:** Comments and documentation describe current state, not change history.

**Rationale:**
- Change history lives in git
- Comments describe intent and rationale
- Prevents temporal drift ("Added X in 2024" meaningless in 2026)

**Examples:**
- Avoid: "Changed to async/await", "TODO: refactor", "Fixed bug"
- Prefer: "Async/await enables try/catch error handling", "Current implementation O(n²), optimize when dataset grows"

## Evidence-Based Debugging

**Preference:** Gather evidence before forming hypotheses.

**Rationale:**
- Prevents shotgun debugging
- Faster root cause identification
- Enables learning from mistakes

**Workflow:** Reproduce → Collect logs → Identify last good state → Hypothesis → Test → Document.

## Manual Memory Capture Over Automatic

**Preference:** User explicitly invokes memory capture for sessions.

**Rationale:**
- Prevents memory pollution from routine operations
- User knows when meaningful work occurred
- Conscious curation ensures high signal-to-noise

**Trade-off:** Requires user discipline to invoke capture. Automatic would be convenient but risks noise.
