# Restriction #5 — Spec at TUIBBS-scp v1-MVP/epics.md immutable

**Verdict:** **PASS**

## Spec path verification

```
ls /config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/epics.md
→ /config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/epics.md  (exists)
```

The spec lives in a sibling repository (TUIBBS-scp), distinct from IronClaude. This IronClaude task has no read/write access to the TUIBBS-scp tree as part of any production-code change — verified by inspection of all 4 changed files (none reference `/config/workspace/TUIBBS-scp/`).

## IronClaude-side proxy check

`git status --short` in the IronClaude repo (per restriction-1 audit) lists ONLY:
- `src/superclaude/cli/roadmap/structural_checkers.py`
- `tests/roadmap/test_convergence.py`
- `tests/roadmap/test_remediate_executor.py`
- `tests/roadmap/test_structural_checkers.py`
- `tests/roadmap/test_structural_checkers_properties.py` (new)
- Untracked `.dev/tasks/...` task-workspace artifacts

None of these files modify or proxy the TUIBBS-scp spec.

## Verdict

PASS — no IronClaude file references or modifies the spec path; no `.md` content under `/config/workspace/TUIBBS-scp/` is written, touched, or read-then-staged by this task.
