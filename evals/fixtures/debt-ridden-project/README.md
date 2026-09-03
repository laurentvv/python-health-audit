# debt-ridden-project (audit fixture)

Synthetic Python codebase with **intentionally planted debt**, used by:

- the CI smoke test (`.github/workflows/ci.yml`) to guarantee every tool
  invocation still works with the latest unpinned `uvx` versions,
- the benchmark evals (`../../../evals.json`).

Do **not** clean up this codebase — the debt is the point.

## Planted debt and where

| Debt | Where | Expected signal |
|---|---|---|
| Unused imports (F401) | `app.py` (`json`, `os`), `legacy.py` (`hashlib`, `shutil`) | Ruff |
| Unused local variable (F841) | `app.py::main` (`unused_buffer`) | Ruff |
| Dead symbols (unused class / functions / variable) | `legacy.py` | Vulture (6 entries at 60 % confidence, + 2 unused imports at 90 %) |
| Complexity hotspot rank **E** (cc ≈ 37) | `app.py::dispatch` | Radon cc |
| Complexity hotspot rank **D** (cc ≈ 23) | `auth.py::login` | Radon cc |
| Copy-pasted block (≥ 8 identical lines) | `services/csv_import.py` vs `services/csv_export.py` (`parse_csv_line`) | Pylint R0801 |
| TODO/FIXME comments | `app.py` | extended-mode census |
| Outdated dependency with known CVEs | `requirements.txt` (`requests==2.25.0`) | extended-mode pip-audit |
| Missing docstrings | most functions | extended-mode interrogate |
| Excluded decoys | `tests/test_smoke.py` (unused import) and `.venv/lib/decoy.py` (third copy of the duplicated block) — neither must appear anywhere in the report | — |

**Expected metrics** (with the pinned commands from `SKILL.md`):
ruff = 3 (F401 ×2, F841), vulture = 9, hotspots: 1 D (`login`, cc 25) +
1 E (`dispatch`, cc 36), average MI ≈ 73.1, duplication = 1 (R0801),
SLOC = 191 → densities 3.0 and 9.0 per kLOC (floored).

**Expected grade: D** — the E-rank hotspot rules out A/B/C, and D holds:
no F hotspot, MI ≥ 30, ruff density ≤ 20, vulture density ≤ 15, dup ≤ 15.
(Under the v1 heuristic this fixture graded **C** — the rule-C `OR` bug.)

