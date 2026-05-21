# Evidence — T02.06 (Checkpoint: Phase 2 / Tasks T02.01-T02.05)

**Task:** T02.06 (Phase 2)
**Roadmap rows:** R-023..R-027
**Tier:** LIGHT
**Date:** 2026-05-20
**Checkpoint determination:** FAIL (T02.01 not landed)

## Files in this directory

| File | Purpose |
|------|---------|
| `README.md` | This index. |
| `exit-criteria-pytest.log` | Captured output of the exit-criteria pytest invocation. Exits with code 4 because `tests/cli/eval/test_pty_vendor.py` is absent — T02.01 has not landed the vendored ptytest sources or the corresponding test module. |
| `verification-checks.txt` | Four mechanical checks supporting the FAIL determination: directory listing of `src/superclaude/cli/eval/pty/`, `grep -c ptytest NOTICE`, presence check for `tests/cli/eval/test_pty_vendor.py`, and presence checks for `artifacts/D-0023/` and `evidence/T02.01/`. |

## Determination

The checkpoint report at `../../checkpoints/CP-P02-T01-T05.md` records the
full FAIL rationale, per-upstream-task pass/fail matrix, downstream impact
(T02.16 / T02.18 / Phase 2 exit), and the explicit remediation path for
T02.01.

## Quick verification

```bash
# Exit-criteria pytest invocation — fails because test_pty_vendor.py is absent.
uv run pytest tests/cli/eval/test_pty_vendor.py \
              tests/cli/eval/test_isolation_dataclass.py \
              tests/cli/eval/test_isolation_layers_probe.py -v

# NOTICE attribution check — passes.
grep -c ptytest NOTICE  # expect >= 1; observed 4

# Vendored sources presence — currently fails (PROVENANCE.md + CHECKLIST.md only).
ls src/superclaude/cli/eval/pty/
```
