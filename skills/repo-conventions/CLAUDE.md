# repo-conventions/

Install the canonical governance files and hold READMEs to the standard shape.
Assets are canon: copy them, never regenerate or paraphrase them.

## Files

| File        | What                                                   | When to read                |
| ----------- | ------------------------------------------------------ | --------------------------- |
| `SKILL.md`  | Install steps, README rules, Visuals rules, exceptions | Using this skill            |
| `README.md` | Why the assets are verbatim, what is out of scope      | Understanding the design    |

## Assets

| Asset                              | Destination                          |
| ---------------------------------- | ------------------------------------ |
| `assets/CONTRIBUTING.md`           | `CONTRIBUTING.md`                    |
| `assets/pull_request_template.md`  | `.github/pull_request_template.md`   |
| `assets/gitmessage`                | `.gitmessage` (only if none)         |
| `assets/README_TEMPLATE.md`        | `README.md` (only if none)           |

No scripts. Everything is `cp` plus a short report.
