# Debugging Strategies

Evidence-based investigation techniques and root cause analysis patterns.

## Evidence-First Debugging

Gather evidence before forming hypotheses:
1. Reproduce the problem consistently
2. Collect logs, stack traces, error messages
3. Identify last known good state
4. Form hypothesis based on evidence
5. Test hypothesis with minimal changes
6. Document root cause and solution

Anti-pattern: Guessing at solutions without evidence. Leads to shotgun debugging and obscures actual root cause.

## Minimal Reproduction

Isolate the problem to smallest possible context:
- Remove unrelated code paths
- Simplify data inputs to minimum failing case
- Eliminate environment-specific factors
- Create standalone test case demonstrating issue

Rationale: Smaller reproduction surface makes root cause obvious. Enables faster hypothesis testing.

## Binary Search Debugging

When problem occurred "somewhere" in recent changes:
1. Identify last known good state (commit, configuration)
2. Identify first known bad state
3. Test midpoint between good and bad
4. Repeat on failing half until single change isolated

Works for: regressions, broken builds, configuration issues, dependency conflicts.

## Clean Slate Validation

When environment suspected:
- Fresh virtual environment
- Clean dependency installation
- Default configuration
- Minimal test case

Distinguishes between: code bugs vs environment corruption vs configuration drift.

## Artifact Cleanup

After debugging session concludes, remove all debug code:
- Temporary console.log / print statements
- Commented-out experimental code
- Debug-only configuration flags
- Test data files created for reproduction

Rationale: Debug artifacts obscure code intent and create maintenance burden. Clean code reflects production state only.
