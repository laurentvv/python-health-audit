# python-health-audit

[![Skill](https://img.shields.io/badge/skill-v1.0-5b2ddb?style=flat-square)](python-health-audit/SKILL.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Pass rate: 100%](https://img.shields.io/badge/pass%20rate-100%25-brightgreen?style=flat-square)](#benchmark)
[![GitHub](https://img.shields.io/badge/GitHub-laurentvv%2Fpython--health--audit-181717?style=flat-square&logo=github)](https://github.com/laurentvv/python-health-audit)

> A read-only static audit skill for Python projects: one command, one Markdown report, one A–F grade.

`python-health-audit` is a **Kilo / Claude Code skill** that any developer (lead, solo, acquirer) can invoke to get an instant, opinionated health check of a Python codebase. It runs four industry-standard linters through [`uvx`](https://docs.astral.sh/uv/) — no virtualenv, no install — and writes a single `rapport_sante_python.md` at the root of the audited project.

---

## Why

| Without the skill | With the skill |
|---|---|
| Remember 4 CLI invocations + flags + exclusions | One natural-language request |
| Stitch outputs from Ruff, Vulture, Radon, Pylint by hand | One Markdown report with deterministic A–F grade |
| Risk of `ruff --fix` / `pylint --fix` mutating source | Strict read-only guarantee |
| Ad-hoc structure every time | Stable 5-section template + 3-item action plan |

## Install

The skill works in any agent runtime that supports the [skill format](https://kilo.ai/docs) (Kilo, Claude Code, skills.sh).

```powershell
# Kilo
kilo skills add https://github.com/laurentvv/python-health-audit

# Claude Code
claude skills add https://github.com/laurentvv/python-health-audit

# npx / skills.sh
npx skills add https://github.com/laurentvv/python-health-audit --skill python-health-audit
```

## Usage

Open your agent in the Python project you want to audit and ask, in plain English (or French):

```
I'm taking over a 3-year-old Flask project. Can you give me a full health check
before I start refactoring? The code lives in ./backend. Tell me where the
technical debt is.
```

The agent will:

1. `cd` into the target project (or use the `workdir` parameter)
2. Run sequentially, capturing all stdout + stderr in memory:
   - `uvx ruff check .` — local dead code (unused imports, unused vars)
   - `uvx vulture . --min-confidence 80` — global dead code (unused symbols)
   - `uvx radon cc . -a -nc` — cyclomatic complexity hotspots
   - `uvx radon mi .` — Maintainability Index per file
   - `uvx pylint --disable=all --enable=duplicate-code (...)` — copy-paste detection
3. Compute an **A–F grade** from the metrics (deterministic heuristic, see below)
4. Write `rapport_sante_python.md` at the root of the audited project

That's it. No source files are touched.

## Example output

```markdown
# Python Health Report — backend

Generated on 2026-06-04 11:09 by python-health-audit.

## 1. Executive Summary
- Global grade: C
- Reason: Grade C assigned — Ruff reports 21 findings (just above the 20
  threshold), but only 1 C/D hotspot (`login` in `auth.py`) and average MI
  at 71.64 keep the project out of D/F territory.

## 2. Dead Code
### 2.1 Local — Ruff
21 findings (20 unused imports F401 + 1 undefined name F821). All fixable
mechanically; no auto-fix applied per audit policy.

### 2.2 Global — Vulture
13 entries at confidence ≥ 80%.

> ⚠️ Vulture produces false positives by construction (global static
> detection). Verify each entry before removal.

## 3. Complexity Hotspots (Radon)
| Rank | File:Line       | Block  |
|------|-----------------|--------|
| D    | backend/auth.py | `login`|

## 4. Code Duplication (Pylint)
No duplication detected — Pylint `duplicate-code` reports 10.00/10.

## 5. Recommended Action Plan
1. **Fix the F821 undefined name in `backend/app.py:18`** — latent runtime crash.
2. **Reduce complexity of `login` (rank D, 22)** — extract validation chain.
3. **Purge the 20 unused imports flagged by Ruff F401** — mechanical cleanup.
```

## Grading heuristic

The grade is computed deterministically. First matching rule wins (A → F):

| Grade | Criteria |
|-------|----------|
| **A** | Ruff = 0 **AND** 0 C/D/E/F hotspot **AND** average MI ≥ 80 **AND** 0 Pylint duplication |
| **B** | Ruff ≤ 5 **AND** 0 E/F hotspot **AND** average MI ≥ 65 |
| **C** | (Ruff ≤ 20) **OR** (≤ 3 C/D hotspots); average MI ≥ 50 |
| **D** | ≥ 1 E hotspot **OR** average MI ∈ [30, 49] |
| **F** | ≥ 1 F hotspot **OR** average MI < 30 **OR** Vulture > 20 entries |

- **Average MI** = arithmetic mean of `radon mi` scores per file.
- **Hotspot** = function/class graded C, D, E or F by Radon cc (A and B hidden).
- **Duplication** = at least one pair returned by Pylint `duplicate-code`.

## Constraints (what the skill will NOT do)

1. **Strict read-only** — no `Edit` / `Write` / `Set-Content` on `.py` files. The only artifact written is the report itself.
2. **No auto-fix** — never invokes `ruff --fix`, `autoflake`, `radon raw` with rewrite, or `pylint --fix`.
3. **Silent execution** — no progress messages in chat. Only the path of the generated report is returned.

## Benchmark

Tested against 2 realistic prompts × 2 configurations (with vs without the skill), on a synthetic Python codebase with intentional debt (dead code, complexity hotspot, copy-paste).

| Configuration | Pass rate | Detail |
|---|---|---|
| **With skill** | **100%** (13/13) | eval-1: 8/8, eval-2: 5/5 |
| Without skill (baseline) | 29% (4/13) | eval-1: 3/8, eval-2: 1/5 |
| **Delta** | **+71 pp** | — |

The baseline (no skill) consistently fails to:
- Produce the expected `rapport_sante_python.md` filename (agents invent `AUDIT.md`, `AUDIT_REPORT.md`, etc.)
- Follow the 5-section template and the 3-item action plan
- Display the A–F grade
- Include the Vulture false-positive warning

Reproduce: see `evals/evals.json` and the [iteration-1 artifacts archived in the v1.0 release](https://github.com/laurentvv/python-health-audit/releases/tag/v1.0).

## Repository structure

```
skills-generator/
├── README.md
├── LICENSE
├── .gitignore
└── python-health-audit/
    ├── SKILL.md          # frontmatter + role / objective / steps / grading / format / constraints
    └── evals/
        └── evals.json    # 2 benchmark test cases
```

## Compatibility

| Runtime | Status |
|---|---|
| Kilo | ✅ supported |
| Claude Code | ✅ supported |
| Other MCP-aware agents | ✅ if they read the SKILL.md frontmatter format |

Required on the host machine:
- [`uv`](https://docs.astral.sh/uv/) (provides the `uvx` command) — **or** `pipx` as fallback
- PowerShell 7+ on Windows, bash on Linux/macOS

## Contributing

This is a single-skill repo. To iterate:

1. Edit `python-health-audit/SKILL.md`.
2. Add / modify test prompts in `python-health-audit/evals/evals.json`.
3. Re-run benchmarks with the [`skill-creator`](https://github.com/Kilo-Org/skills/tree/main/skill-creator) workflow.
4. Open a PR — describe the change in the skill's behavior, not just the file diff.

## License

MIT — see [LICENSE](LICENSE).
