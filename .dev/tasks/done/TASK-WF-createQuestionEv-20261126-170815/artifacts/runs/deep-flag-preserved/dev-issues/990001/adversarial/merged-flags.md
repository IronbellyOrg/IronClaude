<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (issue-worker-t1) -->
<!-- Merge date: 2026-11-26T19:08:00Z -->

# Flags decision (merged)

<!-- Source: Base (original) -->
- Decided by: issue-worker-t1 (evidence verdict), debated against the user's flags
- Depth: deep

| Field | Value | Reason |
|---|---|---|
| Mode | feature | The description asks for new output (a skills count as the last line), not a fix of broken behaviour; today `install` ends with the Step 10 retire step and the exit-code check, with no count line (src/superclaude/cli/main.py:271-296); `install_all_skills` already reports per-category counts but no total (src/superclaude/cli/install_skills.py:119-147); no doc promises a final count line. |
| Type | cli | The change lives in the `superclaude install` click command (src/superclaude/cli/main.py:46, steps at 202-296) and its skills installer module (src/superclaude/cli/install_skills.py:62). |
| Issue type | Feature | derived by the rule in `refs/labels.md` from the mode and the area |
| Complexity | Complex | follows depth (deep = Complex) |

<!-- Source: Variant 1 (original), metadata and Mode row — merged per Change #1 -->
## Filing

The user passed `--mode bug --type cli`. The issue is filed with the user's flags (mode bug, issue type Bug, label `bug`), and the evidence verdict above is posted as dissent in the pushback comment. Both advocates agreed the user's flag stays authoritative.

<!-- Source: shared assumptions A-001, A-002 (both advocates QUALIFY) — merged per Changes #2 and #3 -->
## Agreed qualifications

- A-001: the count line must be the last line on every path: after the Step 10 retire step (which can print a warning) and also when the run ends in `sys.exit(1)` (src/superclaude/cli/main.py:271-296).
- A-002: "copied" means the installed bucket of `install_all_skills` (src/superclaude/cli/install_skills.py:119). Skipped existing skills (without `--force`), skills served by `/sc:` commands and failed skills are not counted. When nothing is installed (the early "No skills to install" return, src/superclaude/cli/install_skills.py:142-143) the line still prints 0.
