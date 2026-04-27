# MY WORKFLOW

I have been using Claude Code daily since its inception, and using Claude
prior to Claude Code even being released. With this in mind, I am well-aware
of how the code can rot away and degrade with larger context and sessions.
The technical debt that comes from using vanilla Claude can be painful, as
the agent does not know what it doesn't know, and neither do you until
it's too late.

Agentic coding tends to fall apart over the long term. Technical debt piles
up because the agent cannot see it, and the code is coming out so fast
you can't catch it either. This is much more an engineering and context
management issue than a tooling one.

This collection of skills is meant to ensure the AI can always get the
context it needs, while also being able to cleanly organize this information
back to you.

# QUICK START

Clone into your Claude Code configuration directory:

```bash
# Per-project
git clone https://github.com/BryanZaneee/claude-config.git .claude

# Global (new setup)
git clone https://github.com/BryanZaneee/claude-config.git ~/.claude

# Global (existing ~/.claude)
cd ~/.claude
git remote add workflow https://github.com/BryanZaneee/claude-config.git
git fetch workflow
git merge workflow/main --allow-unrelated-histories
```

# SKILLS

This config has three workflow surfaces:

- **Script skills**: Python-backed workflows under `skills/scripts/`.
  Their `SKILL.md` files usually say "the script IS the workflow";
  the user still invokes them like any other skill with `/<skill-name>`.
- **Direct and reference skills**: prompt-level skills that do their work
  from `SKILL.md` instructions or local reference docs.
- **HTML diagram commands**: slash commands in `commands/` that load the
  visual-explainer workflow and write standalone HTML artifacts.

## Script Skills

Script skills are normal skills from the user side. Call them by name:

```bash
/planner
/deepthink
/codebase-analysis
```

Internally, these are structured Python workflows. The public skill entry
lives in `skills/<name>/SKILL.md`, the explanation lives in
`skills/<name>/README.md`, and the implementation lives under
`skills/scripts/skills/<python_name>/`.

| Skill | Use when | Docs |
| ----- | -------- | ---- |
| `planner` | Complex implementation needs planning, QR gates, execution, and docs | [README](skills/planner/README.md) |
| `codebase-analysis` | You need evidence-backed repository orientation before planning | [README](skills/codebase-analysis/README.md) |
| `deepthink` | The question is analytical and you do not know the answer shape yet | [README](skills/deepthink/README.md) |
| `problem-analysis` | You need root cause analysis, not solution design | [README](skills/problem-analysis/README.md) |
| `decision-critic` | You want a decision stress-tested instead of affirmed | [README](skills/decision-critic/README.md) |
| `refactor` | Working code feels structurally messy or debt-prone | [README](skills/refactor/README.md) |
| `prompt-engineer` | A prompt or prompt ecosystem is underperforming | [README](skills/prompt-engineer/README.md) |
| `incoherence` | Docs, specs, and implementation may disagree | [README](skills/incoherence/README.md) |
| `arxiv-to-md` | arXiv papers need conversion into agent-readable markdown | [README](skills/arxiv-to-md/README.md) |
| `memory-manager` | Project or global Claude memory needs initialization or capture | [README](skills/memory-manager/README.md) |

## Direct And Reference Skills

Not every skill is a Python workflow.

| Skill | Use when | Docs |
| ----- | -------- | ---- |
| `doc-sync` | The CLAUDE.md/README.md hierarchy needs bootstrapping, audit, or repair | [README](skills/doc-sync/README.md) |
| `cc-history` | You need to query Claude Code conversation history files | [README](skills/cc-history/README.md) |

## HTML Diagram Commands

The visual HTML workflows live in `commands/`, not as script skills.
They load the `visual-explainer` skill, gather and verify facts first,
then write standalone HTML to `~/.agent/diagrams/` and open the result
in the browser.

Use them when the output should be read visually, with diagrams, tables,
review cards, state machines, or a slide-like narrative.

| Command | Use when |
| ------- | -------- |
| `/generate-web-diagram` | Lightweight standalone HTML explanation or architecture diagram |
| `/generate-visual-plan` | Visual implementation spec with state/API/edge cases and tests |
| `/diff-review` | Visual before/after review of a diff, branch, commit, or PR |
| `/plan-review` | Visual review of a proposed plan against the current codebase |
| `/project-recap` | Current-state recap with recent decisions and cognitive debt hotspots |
| `/generate-slides` | Magazine-quality HTML slide deck |
| `/fact-check` | Verify generated HTML or markdown against the actual codebase |

Examples:

```bash
/generate-web-diagram how the auth service talks to billing
/generate-visual-plan add resumable uploads to the media pipeline
/diff-review HEAD
/plan-review plans/my-feature.md
/project-recap 2w
/generate-slides the launch architecture
/fact-check ~/.agent/diagrams/my-review.html
```

# DEFAULT WORKFLOW

The workflow for anything non-trivial is explore -> plan -> execute.
This takes longer, but produces cleaner results.

## 1. Explore

Figure out what you are actually dealing with. Get a feel for the shape
of the solution.

This part is pretty free-form. If the project or the surface area is
especially large, use the `codebase-analysis` skill to properly explore
the code before proposing anything.

## 2. Think It Through

This step is optional, but I reach for `deepthink` more than any other
skill. It handles analytical questions where I do not yet know what
shape the answer should take: taxonomy design, trade-offs, definitional
questions, evaluative judgments, exploratory investigations.

It auto-detects complexity. Quick mode reasons directly. Full mode
launches parallel sub-agents with different analytical perspectives and
synthesizes through agreement patterns. Both self-verify.

For most analytical questions deepthink is enough. I only reach for the
specialized skills when the question is clearly scoped:

- `problem-analysis`: root cause analysis specifically
- `decision-critic`: stress-testing a specific decision

## 3. Plan

```bash
/planner write a plan to plans/my-feature.md
```

The planner runs the plan through review cycles: technical writer for
clarity, quality reviewer for completeness, until it passes.

The planner captures all the decisions, tradeoffs, and information that
is not visible from the code so that context does not get lost.

## 4. Clear Context

Run `/clear` and start fresh. Everything needed for execution should be
in the plan.

## 5. Execute

```bash
/planner execute plans/my-feature.md
```

The planner delegates to sub-agents. It never writes code directly. Each
milestone goes through the developer, then the technical-writer and the
quality-reviewer. No milestone starts until the previous one has passed
review. Where it can, it runs tasks in parallel.

# PRINCIPLES

This workflow is built around 4 goals.

## Context Management

Each task gets exactly the information it needs. Sub-agents start with a
fresh context window, so architectural knowledge has to live somewhere
persistent.

CLAUDE.md and README.md play distinct roles. The split is the core
context contract for this config, not just a naming preference.

### CLAUDE.md

Claude loads these automatically when it enters a directory. The
repo-root CLAUDE.md keeps its standard meaning: project-wide
instructions, build/test commands, conventions, and top-level context
Claude needs every session.

Nested CLAUDE.md files are small indexes. They should be a tabular map
of filenames, descriptions, and "read when..." triggers, not prose
documentation. When Claude opens `app/web/controller.py`, it retrieves
the indexes along that path and can use their triggers to decide what
to read next.

### README.md

README.md is for invisible knowledge, the stuff you cannot learn by
reading the source: architecture decisions, rejected alternatives,
invariants that are not obvious from code, and the reasoning behind a
design. The test is simple: if a developer could learn it by reading
source files, it does not belong here.

Claude reads README.md when a CLAUDE.md trigger, explicit prompt, or
workflow step makes that context relevant.

With this setup the indexes load automatically and stay tiny, and the
detailed knowledge only shows up when it is actually relevant.

The technical writer agent is what keeps all the token budgets in line.
Roughly 200 tokens for CLAUDE.md, 500 for the README, 100 for function
docs, 150 for module docs. These limits force discipline, if you are
blowing past them, it is usually a sign you are documenting too much.
Function docs include a "use when..." phrase so the agents know when to
reach for them.

The workflow skills treat this hierarchy as a shared contract:

- `planner` reads project and subdirectory CLAUDE.md files while
  planning, captures invisible knowledge in plan state, and has the
  technical-writer update CLAUDE.md/README.md after implementation.
- `codebase-analysis` uses CLAUDE.md and README.md as evidence during
  repository orientation, so downstream plans start from real project
  context instead of guesswork.
- `doc-sync` audits the hierarchy directly, migrates explanatory
  content out of CLAUDE.md and into README.md, and rebuilds missing or
  stale indexes.
- `technical-writer` and `quality-reviewer` enforce the same split
  during documentation and review passes.
- Analytical skills like `deepthink`, `problem-analysis`,
  `decision-critic`, and `refactor` do not maintain the hierarchy
  themselves, but when they need project context they should treat
  CLAUDE.md as navigation and README.md as rationale.

The planner workflow maintains the hierarchy automatically. If you
bypass the planner, you maintain it yourself.

## Planning Before Execution

Agents tend to make mistakes the moment they transition from the plan you
wrote with them into actually executing it. This workflow separates the
planning from the execution so the agent can catch those differences in
review rather than letting them compound.

Plans capture why decisions were made, what alternatives were considered,
and what risks we are taking. Plans are written to files, that way when
context gets cleared, the plan is still there.

## Review Cycles

Execution is split into many milestones. Smaller units are easier to
validate and keep the agent honest at each step. Without that it becomes
a waterfall: one small oversight early on and the agents compound each
mistake until the result is unusable.

Quality gates run at every stage. A technical writer agent checks clarity.
A quality reviewer checks completeness. The loop runs until both of them
pass.

Plans pass review before execution begins. During execution, each
milestone passes review before the next one starts. If the implementation
starts drifting from the plan, I want to know while the drift is still
cheap to fix.

## Cost-Effective Delegation

The coordinator delegates to smaller agents, Haiku for the
straightforward work, Sonnet for moderate complexity. Prompts get injected
just-in-time so the smaller models get exactly the guidance they need at
each step and nothing else.

When quality review fails or the same problem keeps coming back, the
coordinator escalates to a stronger model. I reserve the expensive models
for real ambiguity, not routine work.

# DOES THIS ACTUALLY WORK?

I have not run formal benchmarks, so take this with a grain of salt. What
I can tell you is what I have seen using this workflow to build and
maintain real applications entirely with Claude Code.

The problems I used to hit constantly are mostly gone:

- **Ambiguity.** You ask an AI agent "make me a sandwich" and it comes back
  with a grilled cheese. Technically correct, not what you meant. The
  planning phase forces that kind of misunderstanding to surface before
  you have built the wrong thing.
- **Code hygiene.** Without review cycles the same utility function gets
  reimplemented fifteen times across a codebase. The quality reviewer
  catches it. The technical writer keeps docs consistent.
- **Agent-navigable docs.** Function docs include "use when..." triggers.
  CLAUDE.md tells the agent which files matter for a given task. The
  agent stops guessing which code is relevant.

Is it better than writing code by hand? I think so, but I can't speak for
everyone. This workflow is opinionated. I work full stack, so the patterns
have been hammered on from both sides, backend systems and frontends
alike.

# IMPLEMENTATION NOTES

## Script Skill Structure

Before modifying a script skill, read [skills/README.md](skills/README.md).
It defines the "book" structure used by these files:

- shared prompts
- configuration
- system prompts
- message templates
- parsing functions
- message builders
- domain logic
- step definitions
- output formatting
- entry point

That structure is part of the workflow. Prompt text stays visible,
builders compose it, and step definitions remain table-driven.

## Documentation Contract

For the full CLAUDE.md and README.md format specification, read
[conventions/documentation.md](conventions/documentation.md). The short
version is:

- CLAUDE.md is navigation: what is here and when to read it.
- README.md is invisible knowledge: why the code is shaped this way.
- The planner maintains this automatically when you use it end to end.
- If you bypass the planner, you maintain the hierarchy yourself.

The skill catalog above is the reference. Each skill README has the full
workflow breakdown when you need the detailed version.
