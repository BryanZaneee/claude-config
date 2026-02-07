# Common Pitfalls

Frequent mistakes across projects with prevention strategies.

## Temporal Contamination in Comments

Anti-pattern: "Added X", "Changed to Y", "TODO: Z", "Fixed bug in..."

Comments describe change history instead of code purpose. Creates maintenance burden as code evolves.

Prevention: Use timeless present tense. Describe WHY code exists, not WHAT changed. Example:
- Bad: "// Changed to use async/await instead of callbacks"
- Good: "// Async/await enables error handling via try/catch"

## Premature Abstraction

Anti-pattern: Creating helpers, utilities, or abstractions for single-use operations.

Leads to: unnecessary indirection, harder debugging, future constraints.

Prevention: Only abstract after third repetition (Rule of Three). Prefer inline code duplication over premature generalization.

## Action Factory Functions

Anti-pattern: `def actions(flag=False)` returning different operations based on flag.

Creates: hidden control flow, harder testing, coupled concerns.

Prevention: Use separate well-named constants or functions for each action variant. Explicit over implicit.

## Backwards-Compatibility Hacks

Anti-pattern: Renaming unused _vars, re-exporting types, adding "// removed" comments.

Creates: code archaeology burden, false positive search results, maintenance confusion.

Prevention: If certain something is unused, delete completely. Version control preserves history.

## Destructive Operations as Shortcuts

Anti-pattern: Using `--force`, `--no-verify`, `reset --hard`, `rm -rf` to bypass obstacles.

Risk: lost work, bypassed safety checks, hidden underlying issues.

Prevention: Investigate root cause before destructive action. Example: resolve merge conflicts instead of discarding changes, fix pre-commit issues instead of --no-verify.

## Over-Engineering Simple Tasks

Anti-pattern: Adding error handling, feature flags, abstractions, configurability to straightforward one-time operations.

Creates: complexity without benefit, longer implementation time, harder maintenance.

Prevention: Minimum complexity for current requirement. Trust internal code guarantees. Only validate at system boundaries (user input, external APIs).
