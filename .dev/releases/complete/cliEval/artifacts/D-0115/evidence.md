# D-0115 — Evidence Inventory

**Task:** T06.13 — Assemble OPS-005 release checklist
**Deliverable:** `docs/eval/release-checklist.md`
**Date:** 2026-05-21

## Per-file evidence inventory

| File | Purpose | Lines / Bytes | Verified |
|------|---------|---------------|----------|
| `docs/eval/release-checklist.md` | OPS-005 release checklist (T06.13 / D-0115). 10 numbered sections; consumes OPS-004 by reference. | ~158 lines | Same-dir + `../../`-relative link audit at `evidence/T06.13/link-audit.log`. |
| `.dev/releases/current/cliEval/artifacts/D-0115/spec.md` | Per-deliverable spec — checklist summary, AC map, partial-attestation rationale, files landed, failure-mode analysis. | — | Authored this commit. |
| `.dev/releases/current/cliEval/artifacts/D-0115/notes.md` | Design rationale: why a separate checklist, OPS-004 inheritance pattern, partial-attestation framing, no-audit-test trade-off. | — | Authored this commit. |
| `.dev/releases/current/cliEval/artifacts/D-0115/evidence.md` | This file. | — | — |
| `.dev/releases/current/cliEval/evidence/T06.13/summary.md` | AC-by-AC verification table + walk-through attestation per §. | — | Authored this commit. |
| `.dev/releases/current/cliEval/evidence/T06.13/link-audit.log` | `test -f` per linked path. 24 `../../`-relative + 5 same-dir = 29 unique links, all PASS, EXIT_CODE=0. | — | Captured this commit. |

## Inherited evidence (consumed by reference, not re-captured)

| Origin task | Path | Consumed at |
|-------------|------|-------------|
| T06.01 | `evidence/T06.01/summary.md` + `artifacts/D-0105/spec.md` | release-checklist §3, summary §"§3 ADR sign-offs". |
| T06.07 | `evidence/T06.07/summary.md` | release-checklist §2.1, summary §2 row 2.1. |
| T06.08 | `evidence/T06.08/loc-eval-bodies.log` + `evidence/T06.08/loc-harness-py.log` + `evidence/T06.08/summary.md` + `artifacts/D-0111/spec.md` | release-checklist §4 SC4 + §6 row 6.1. |
| T06.09 | `evidence/T06.09/grep-status-resolved.log` + `evidence/T06.09/oq-enumeration.log` + `artifacts/D-0112/spec.md` | release-checklist §4 SC5. |
| T06.10 | `evidence/T06.10/dep-diff.log` + `evidence/T06.10/make-verify-deps.log` + `artifacts/D-0113/spec.md` | release-checklist §4 SC3. |
| T06.11 | `evidence/T06.11/{01..05}-*.log` + `docs/eval/validation-commands.md` + `artifacts/D-0114/spec.md` | release-checklist §5 (rows 5.1–5.4 + audit test). |

## Link audit summary

From `evidence/T06.13/link-audit.log`:

```
TOTAL_OK=24   # ../../-relative links into the repo
TOTAL_FAIL=0
EXIT_CODE=0

TOTAL_OK=5    # same-directory docs/eval/ links
TOTAL_FAIL=0
EXIT_CODE=0
```

## Open evidence (deferred behind B1 / B2)

| Item | Source | Closure path |
|------|--------|--------------|
| End-to-end `eval run --suite real --eval E1` PASS log | release-checklist §5 row 5.4 + §6 row 6.6 | T06.11-FU01 (helper functions) + T06.11-FU02 (ptytest vendoring) — both named in release-checklist §7.1 with owner RyanW. |
| Release-gate sign-off | release-checklist §8 row 3 | Populated when the walk-through is re-performed post-B1/B2 closure. |

## Verification commands

```bash
# 1. Confirm the checklist document exists.
test -f docs/eval/release-checklist.md && echo OK

# 2. Confirm the spec/notes/evidence triad exists.
ls -la .dev/releases/current/cliEval/artifacts/D-0115/

# 3. Confirm the T06.13 evidence root exists with summary + link-audit.
ls -la .dev/releases/current/cliEval/evidence/T06.13/

# 4. Re-run the link audit (idempotent).
bash -c '
  fail=0
  while IFS= read -r rel; do
    if [ -e "docs/eval/$rel" ]; then ok=$((ok+1)); else fail=$((fail+1)); fi
  done < <(grep -oE "\(\.\./\.\./[^)#]+" docs/eval/release-checklist.md | sed -E "s/^\(//" | sort -u)
  echo "fail=$fail"
'
```

All four commands above exit 0 on the current tree (2026-05-21).
