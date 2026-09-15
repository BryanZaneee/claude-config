---
name: repo-conventions
description: Install the standard CONTRIBUTING.md and .github/pull_request_template.md into a repository, and hold READMEs to the standard shape including screenshots. Use when starting a new repo, or when asked to add or refresh contributing guidelines, a PR template, branch strategy, commit conventions, or README screenshots.
version: 2
---

# Repo conventions

Install the canonical governance files. The assets in `assets/` are canon —
copy them, do not regenerate, paraphrase, reorder, or "improve" them.

## Install

| Asset | Destination |
| --- | --- |
| `assets/CONTRIBUTING.md` | `CONTRIBUTING.md` (repo root) |
| `assets/pull_request_template.md` | `.github/pull_request_template.md` |
| `assets/gitmessage` | `.gitmessage` — only if the repo has none |
| `assets/README_TEMPLATE.md` | `README.md` — only if the repo has none; otherwise see README below |

Copy with `cp`. If a destination already exists, `diff` it against the asset,
show the user, and ask before overwriting. Never silently clobber.

## README

`assets/README_TEMPLATE.md` is the standard: a title with a one-line "what it
is" description, then **Installation**, **Usage**, **Contributing**, and
**License** (the license linked, not a bare `MIT`). New repo with no README →
copy it and fill it in.

An existing README is **never** rewritten to the skeleton. Check it has the
five beats above, add whichever are missing, and leave everything else alone —
a mature README carries sections the template has no slot for, and those are
the point of it. Equivalent headings count: a `Quick start` that installs and
runs is Installation + Usage, don't split it.

**Ask the user before removing or renaming any existing section**, unless the
content is moving somewhere else in the same pass. Adding is safe; deleting is
their call.

Keep the Contributing section short — link the repo's `CONTRIBUTING.md` as the
source of truth and add only what that file cannot know: how to run this
repo's tests, and anything that must never be committed.

Section order for a repo with a visible surface: pitch, screenshots, quickstart,
architecture, configuration, license. Screenshots sit directly under the one-line
pitch, before Installation. See Visuals below.

## Visuals

Any repo with a UI (web, desktop, TUI, or a CLI with meaningful terminal output)
gets a `docs/screenshots/` folder and at least one image embedded in the README
directly under the one-line pitch, before the quickstart. Library-only repos with
no visible surface are exempt; say so in one line in the PR rather than skipping
silently.

**Minimum set by surface type.**

| Surface | Minimum |
| --- | --- |
| Web or desktop UI | the primary screen with realistic fixture data, plus one screen per headline feature named in the pitch |
| TUI | one capture per major view |
| CLI | one terminal capture of the main command's output and one of the test run |

**Capture method is reproducible, not manual.** Web: a Playwright spec or script
that reuses the e2e setup (the `screenshots.spec.ts` in labelcheck's `web/e2e/`
is the pattern: opt-in flag, same web servers, same fixture reset). TUI or CLI: a
script that runs the command at a fixed terminal size and pipes it through a
renderer (termshot, freeze, or a Playwright page loading an HTML or xterm.js
dump), so anyone can regenerate the set. Commit the script and document the one
command that regenerates everything.

**Format and size.** WebP preferred, PNG acceptable. Each file under 300 KB.
Width 1400 to 1600 px for full screens. Light theme by default; include dark
only if the app ships a dark theme, and then pair them.

**Content rules.** Fixture or synthetic data only. Never a real account, key,
IP, hostname, or personal detail in a frame. Strip the browser chrome. No
annotations or arrows baked into the image; put that in the README caption.

**README embedding.** `<img>` or a Markdown image with descriptive alt text, a
one-line italic caption under each, and at most four images before the
quickstart. Link the folder for the rest.

**Secret guard.** Where a repo has a pre-commit secret guard, it must also reject
image filenames that look like they contain a hostname or an IP address.

## Exceptions

**FedStack repos** run a different PR template (Summary / Why / Changes /
Testing / AI code-review checklist / ADR). Leave an existing one alone; install
`CONTRIBUTING.md` only.

## The develop variant

The shipped file is trunk-based (`feature/* → main`) and documents `develop` as
an opt-in variant. That default stands unless **both** hold:

- a real staging environment deploying from a branch other than prod
- versioned releases consumed by someone other than the author

Only when both look true, ask the user whether to adopt `develop`. If they say
yes, edit the installed `CONTRIBUTING.md`:

- Branch Strategy diagram → `feature/* ──▶ develop ──▶ main`, and state that
  `develop` is the default branch so PRs target it
- Workflow steps 1–2 branch from `develop`; step 5 opens the PR into `develop`
- Add a Releases sub-point: `develop` → `main` on a fixed cadence (weekly or
  per milestone), PR titled `release: v<version>`, merged with a merge commit,
  then tagged
- Hotfixes section: branch from `main`, PR into `main`, tag, then **immediately
  merge `main` back into `develop`**
- Branch Protection already covers both branches — leave it
- Delete the now-redundant "Variant: adding a develop branch" section

If they say no, or the criteria don't hold, the file stays exactly as shipped,
variant section included.

## Report

Say which files were written, then name the GitHub-side steps the doc assumes
but the skill can't do — branch protection rules, required status checks,
auto-delete head branches, CODEOWNERS. Do not attempt them via `gh`.

## Out of scope

Installing husky/commitlint/release-please, writing CI workflows, creating
`.env.example`. CONTRIBUTING documents those; wiring them is a separate ask.

## Changelog

- v2: Visuals section, README section order, screenshot rule for the secret guard.
- v1: CONTRIBUTING, PR template, gitmessage, README template.
