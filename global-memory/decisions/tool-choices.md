# Tool Choices

Technology selection decisions with rationale and trade-offs.

## Testing Framework: pytest + hypothesis

**Choice:** pytest for test execution, hypothesis for property-based testing.

**Rationale:**
- pytest: Industry standard, excellent fixture system, clear assertion failures
- hypothesis: Finds edge cases missed by example-based tests, generates test data automatically

**Trade-offs:** Hypothesis tests slower than unit tests, but catch more bugs. Use selectively for complex logic with many input variations.

**When to use:**
- pytest: All tests (integration, property, unit)
- hypothesis: Functions with complex input domains, parsing logic, data transformations

## Documentation: Markdown (CommonMark)

**Choice:** Markdown for all documentation, following CommonMark spec.

**Rationale:**
- Human-readable as plain text
- LLM-optimized (training data includes extensive markdown)
- Version control friendly (text-based diffs)
- Universal tooling support

**Trade-offs:** No rich formatting (vs HTML/LaTeX), but simplicity outweighs limitations for technical documentation.

## Configuration: YAML + JSON

**Choice:** YAML for human-edited config, JSON for machine-generated data.

**Rationale:**
- YAML: Readable, supports comments, less verbose than JSON
- JSON: Strict spec, no ambiguity, universal parsing support

**Usage:**
- YAML: Convention registry, skill metadata, agent definitions
- JSON: Session transcripts, cache files, settings

## Model Selection: Opus for Planning, Sonnet for Execution

**Choice:** Claude Opus 4.6 for architect role, Claude Sonnet 4.5 for developer/reviewer/technical-writer roles.

**Rationale:**
- Opus: Superior reasoning for complex planning, trade-off analysis
- Sonnet: Cost-effective for well-defined tasks, faster response time

**Cost impact:** Opus ~5x more expensive than Sonnet. Reserve for planning where reasoning quality critical.

## Memory Format: Markdown over JSON

**Choice:** Session memory files as markdown, not JSON.

**Rationale:**
- Human-readable and editable
- Better for LLM consumption (trained on documentation)
- Easier to browse and search
- Still validates via Pydantic before write

**Trade-offs:** Manual parsing vs direct JSON.parse(), but tooling handles conversion transparently.
