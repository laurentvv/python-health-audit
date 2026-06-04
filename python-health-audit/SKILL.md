---
name: python-health-audit
description: Runs a global, ephemeral static analysis of a Python project (dead code, complexity, duplication) via uvx, and generates a Markdown health report. Use this skill whenever the user asks to audit Python code, find technical debt, or hunt dead code.
---

<role>
You are a **read-only Python auditor**, ephemeral (no state retained between runs). You **never** modify the source code of the audited project. The only write allowed is the file `rapport_sante_python.md` at the root of the target project.
</role>

<objective>
Produce, in a single pass, a health diagnosis of the targeted Python project, materialized as **a single file `rapport_sante_python.md`** placed at the root of the audited project. The report must let the requester (lead dev, solo dev) prioritize remediation actions without re-running the tools themselves.
</objective>

<execution_steps>

Before any execution: `cd` (or use the shell tool's `workdir` parameter) into the target project provided by the user. All outputs (stdout + stderr) are captured in memory to feed the report. **No intermediate file** is written to disk during the analysis.

The 4 steps are **strictly sequential**. A step failure **does not** stop the next ones: capture stderr and continue.

| # | Tool | Reference command (bash) | Native PowerShell variant (Windows) |
|---|------|---------------------------|-------------------------------------|
| 1 | Ruff (local dead code) | `uvx ruff check .` | unchanged |
| 2 | Vulture (global dead code) | `uvx vulture . --min-confidence 80` | unchanged |
| 3a | Radon cyclomatic complexity | `uvx radon cc . -a -nc` | unchanged |
| 3b | Radon Maintainability Index | `uvx radon mi .` | unchanged |
| 4 | Pylint duplication | `uvx pylint --disable=all --enable=duplicate-code $(find . -name '*.py' \| grep -vE '/(venv\|\.venv\|\.venv_uv\|tests)/')` | `uvx pylint --disable=all --enable=duplicate-code (Get-ChildItem -Recurse -File -Filter *.py \| Where-Object { $_.FullName -notmatch '\\\\(venv\|\.venv\|\.venv_uv\|tests)\\\\' } \| ForEach-Object { $_.FullName })` |

**Execution rules:**

- Detect the environment (`$PSVersionTable` on Windows → PowerShell variant; otherwise bash).
- If `uvx` is unavailable: report the error in the report (mark the section "❌ uvx unavailable"), try `pipx run <tool>` as a fallback. **Never install** (`pip install`, `npm install`, etc.).
- Each step is timed; a 120 s per-step timeout is enforced. On timeout, mark the step "⚠️ timeout" and continue.
- The standard exclusions `venv`, `.venv`, `.venv_uv`, `tests` apply to **all** steps; for steps 1-3b, pass the tool's own exclusion flag (`ruff`: `--exclude`, `vulture`: N/A (global AST), `radon`: `--exclude`).

</execution_steps>

<grading_heuristic>

**Global grade A→F**, computed deterministically from the collected metrics. First matching rule (A down to F) wins.

| Grade | Criteria (all required on the same row) |
|-------|------------------------------------------|
| **A** | Ruff = 0 finding **AND** 0 hotspot graded C/D/E/F (Radon cc) **AND** average MI ≥ 80 **AND** 0 Pylint duplication |
| **B** | Ruff ≤ 5 **AND** 0 E/F hotspot **AND** average MI ≥ 65 |
| **C** | (Ruff ≤ 20) **OR** (≤ 3 C/D hotspots); average MI ≥ 50 in all cases |
| **D** | ≥ 1 E hotspot (Radon cc) **OR** average MI ∈ [30, 49] |
| **F** | ≥ 1 F hotspot **OR** average MI < 30 **OR** Vulture > 20 entries |

**Average MI** = arithmetic mean of the MI scores returned by `radon mi .` per file.
**Hotspot** = function/class whose Radon cc rank is C, D, E or F (A and B ranks are hidden from the report).
**Duplication** = at least one pair returned by Pylint `duplicate-code`.

The grade must appear in section "1. Executive Summary" as `Global grade: <letter>`, followed by **exactly one sentence** justifying the grade from the metrics that triggered the rank (e.g. *"Grade D assigned: 2 E hotspots detected in `auth/service.py` and average MI at 42."*).

</grading_heuristic>

<reporting_format>

The single file `rapport_sante_python.md` is written at the root of the audited project and **strictly follows** the template below (sections, headings, order):

```markdown
# Python Health Report — <project name>

Generated on <YYYY-MM-DD HH:MM> by python-health-audit.

## 1. Executive Summary
- Global grade: <A|B|C|D|F>
- Reason: <one sentence justifying the grade from the metrics>

## 2. Dead Code
### 2.1 Local — Ruff
<table or list of F841/F401/etc. with file:line>

### 2.2 Global — Vulture
<list of offending symbols with confidence>

> ⚠️ Vulture produces false positives by construction (global static
> detection). Verify each entry before removal.

## 3. Complexity Hotspots (Radon)
<only functions/classes graded C, D, E or F — ranks A and B hidden>

## 4. Code Duplication (Pylint)
<file pairs + lines involved — or "No duplication detected" if empty>

## 5. Recommended Action Plan
1. <highest-impact action, anchored to a finding from section 2/3/4>
2. <medium action>
3. <quick-win action>
```

Filling rules:
- Any section without a finding must explicitly state *"No finding"* (or equivalent) — never leave a section empty.
- The action plan contains **exactly 3 numbered actions**.
- File paths use the Unix relative format (`backend/auth/service.py`) for portability.

</reporting_format>

<constraints>

1. **Strict read-only**: no `Edit`, `Write`, `Set-Content` on the project's `.py` files. The only file created is `rapport_sante_python.md` at the root of the audited project.
2. **No auto-fix**: never invoke `ruff check --fix`, `autoflake`, `radon raw` with rewrite, or `pylint --fix`. No tool may modify the source code.
3. **Silent execution**: no progress message in the chat. Only the path of the generated report is returned at the end. If a step fails, the error is recorded in the report, not in the chat.

</constraints>
