# FR-RH2.7 Diff Proof — frozen files byte-unchanged (Step 3.5)

**Date:** 2026-06-22
**Baseline cross-ref:** `phase-outputs/discovery/frozen-files-baseline.md` (both files CLEAN at task start).

## Command

```bash
cd /config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3 && \
  git diff -- src/superclaude/cli/reflect/contract.py src/superclaude/cli/reflect/models.py
```

## Output

```
(empty — no diff)
```

## Verdict: PASS

`git diff` printed NOTHING for both `contract.py` and `models.py`. Combined with the Phase-1 baseline (both clean at start), this proves `derive_verdict` and the `Verdict` exit-code map are byte-identical to `start_commit`. The `AdversarialResult` dataclass lives in `ensemble.py`, NOT `models.py`, so `models.py` stays byte-clean. FR-RH2.7 (the governing backward-compat invariant) is satisfied.
