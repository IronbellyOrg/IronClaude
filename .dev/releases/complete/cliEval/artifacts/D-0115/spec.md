# D-0115 — OPS-005 cliEval v1 Release Checklist

**Task:** T06.13 (Phase 6, Roadmap OPS-005 / R-114)
**Deliverable:** `docs/eval/release-checklist.md` assembling release evidence + follow-up plan; cross-references all OPS-004 commands.
**Status:** PARTIAL — checklist document landed and walk-through verified on the current tree. Three of the four OPS-004 commands attest GREEN; command 4 carries the B1/B2 partial waiver inherited from T06.11 / D-0114. Follow-ups inventoried with named successor tasks + owners.
**Date:** 2026-05-21

## Purpose

OPS-005 (roadmap row R-114) assembles the v1 release evidence into a single walk-through document. The release-gate reviewer reads one file (`docs/eval/release-checklist.md`) and confirms every M6 exit-gate prerequisite has landed by following the embedded links into:

- `decisions.md` (ADRs + closures + sign-off table)
- `docs/eval/validation-commands.md` (OPS-004 4-command sequence)
- `.dev/releases/current/cliEval/evidence/T0{1..6}.xx/` (per-task evidence captures)
- `src/superclaude/cli/eval/suites/README.md` (suite naming + `quick.yaml` follow-up)

T06.13 lands the canonical document and walks through every row on the current tree.

## Checklist summary (one row per §)

| § | Title | Rows | Verdict |
|---|-------|------|---------|
| 1 | Contract | 1 table | Quadrant index recorded — ADRs / SCs / OPS-004 / Follow-ups. |
| 2 | Pre-flight (Linux + UV + checkout) | 3 | All 3 PASS on the current tree. |
| 3 | ADR sign-offs (SC1 — D-1..D-10) | 9 ADRs | 🟢 All 9 signed off by RyanW (2026-05-20). |
| 4 | Success criteria (SC1..SC5) | 5 | 🟢 All 5 RESOLVED. `grep -c "status: resolved" decisions.md` = 16 (gate ≥ 10). |
| 5 | Validation commands (OPS-004) | 4 commands + 1 audit test | **3 of 4 PASS, 1 PARTIAL** (command 4 B1/B2 waiver). 23/23 audit test cases PASS. |
| 6 | Full-run artifacts (SC2 + retention + sync) | 6 rows | 5 PASS, 1 DEFERRED (row 6.6 — end-to-end run artifact; deferred behind B1/B2). |
| 7 | Follow-ups | 5 items (B1, B2, DOC-OQ9, AC2, MIG-003, `quick.yaml`, MIG-001) | All named with successor tasks + owners. |
| 8 | Sign-off | 3 rows | RyanW signed for ADRs + SCs; release-gate row reserved for re-attestation post-B1/B2. |
| 9 | Acceptance map (T06.13) | 4 ACs | All 4 ACs traceable into §§3–7. |
| 10 | Cross-references | 14 cross-links | All resolve on the current tree (link audit below). |

## Acceptance criteria → evidence map

| AC (T06.13) | Evidence |
|-------------|----------|
| `docs/eval/release-checklist.md` lists `eval doctor`, `make verify-sync`, targeted tests, full-run artifacts, follow-ups. | §5 row 5.3 (`eval doctor`), §5 row 5.2 (`make verify-sync`), §5 row 5.1 (targeted pytest). §6 rows 6.1–6.6 (full-run artifacts: 15-eval coverage, suite README, sync, retention, runtime/retry, end-to-end artifact). §7 four sub-sections naming five follow-up clusters. |
| Each checklist item links to evidence under `TASKLIST_ROOT/evidence/`. | §3 ADRs link `decisions.md` + `artifacts/D-0105/spec.md` + `evidence/T06.01/summary.md`. §4 SCs link `decisions.md` per-SC sections + `evidence/T06.08`/`T06.09`/`T06.10` logs + per-SC spec.md. §5 OPS-004 rows link `evidence/T06.11/01..05*`. §6 links suite README + `docs/eval/retention.md` + `runtime.md` + `retry.md` + `scratch-roots.md`. |
| Follow-ups section names MIG-003 (T06.15) and `quick.yaml` deferral. | §7.2 MIG-003 row (T06.15 owner RyanW); §7.3 `quick.yaml` row (DOC-OQ6 deferral, README §"Planned follow-up — `quick.yaml`"). |
| `TASKLIST_ROOT/artifacts/D-0115/spec.md` records the checklist summary. | This file. |

## Verification step result

T06.13 step 5 ("Walk through the checklist on the current tree") was executed by following every link in §§3–7 and confirming the target file or section exists. 27 of 27 referenced paths resolve. The walk-through evidence is captured at `.dev/releases/current/cliEval/evidence/T06.13/summary.md` along with a per-link audit and the verbatim per-row attestation.

## OPS-004 inheritance

OPS-005 consumes OPS-004 by reference for the four validation commands. The release-checklist embeds OPS-004's outcomes in §5 with one-row-per-command and links back to the canonical contract at `docs/eval/validation-commands.md` for the per-command details (purpose, evidence, blocker analysis). This avoids drift: the OPS-004 audit test (`tests/cli/eval/test_validation_commands.py`) is the single enforcement point for the command list, evidence filenames, and B1/B2 enumeration. If OPS-004 changes, OPS-005 picks up the new contract automatically because it does not duplicate the per-command body.

## Partial-attestation rationale

§5 row 5.4 (`uv run superclaude eval run --suite real --eval E1`) and §6 row 6.6 (end-to-end run artifact) are marked PARTIAL/DEFERRED. Two blockers prevent full attestation:

- **B1** — `_new_run_id` and `_default_output_dir` helpers undefined at `src/superclaude/cli/eval/commands.py:1467-1469`. Inherited from OPS-004 §5; tracked as successor task **T06.11-FU01** with owner RyanW.
- **B2** — ptytest M2 vendoring incomplete (`src/superclaude/cli/eval/pty/__init__.py` missing); `eval doctor` reports `vendored.ptytest` SOFT-SKIP. Inherited from OPS-004 §5; tracked as successor task **T06.11-FU02** with owner RyanW.

The partial path is authorised by `Fallback Allowed: Yes` on T06.11 phase metadata and rolled forward into T06.13. The release-checklist names both blockers explicitly in §7.1, lists their successor tasks, and reserves §8 row 3 (release-gate sign-off) for re-attestation once command 4 + row 6.6 are GREEN.

## Files landed

| File | Status |
|------|--------|
| `docs/eval/release-checklist.md` | Created — v1.0 (T06.13 initial author). |
| `.dev/releases/current/cliEval/artifacts/D-0115/spec.md` | This file. |
| `.dev/releases/current/cliEval/artifacts/D-0115/notes.md` | Created — design rationale, OPS-004 inheritance pattern, partial-attestation framing. |
| `.dev/releases/current/cliEval/artifacts/D-0115/evidence.md` | Created — per-link inventory + walk-through audit. |
| `.dev/releases/current/cliEval/evidence/T06.13/summary.md` | Created — AC-by-AC verification table + 27-path link audit + walk-through attestation. |
| `.dev/releases/current/cliEval/evidence/T06.13/link-audit.log` | Created — `test -f` per linked path, all PASS. |

## Failure-mode analysis

| Drift pattern | Caught by | Notes |
|---|---|---|
| OPS-004 command list re-negotiated without a checklist update | `tests/cli/eval/test_validation_commands.py` already pins the 4-command list. OPS-005 §5 cites OPS-004 by reference rather than duplicating, so the audit catches both documents in one commit. | Updating the command list requires changing OPS-004 + the audit test + this checklist's §5 in lockstep. |
| Sign-off row in §8 left stale after B1/B2 close | Manual walk-through of §8 row 3 ("release-gate reviewer") at re-attestation time. | The "_pending_" placeholder is the visible drift marker. |
| Follow-up successor task closed without unflipping §7.1 row | Re-walk through OPS-004 §5 "Closure path" steps — the explicit ordered post-close edits cite §5 row 5.4 and §6 row 6.6 by name. | T06.11-FU01 / FU02 closure ticket SHOULD list this checklist's §5 + §6 + §7.1 + §8 row 3 as required-edit sites. |
| Evidence link rots after a file rename | `evidence/T06.13/link-audit.log` re-run on each release. | The walk-through is repeatable: `for f in $(grep -oE '\(\.\./\.\./[^)]+\)' docs/eval/release-checklist.md | sed -E 's/^\(|\)$//g'); do test -e "docs/eval/$f" && echo "$f OK" || echo "$f MISSING"; done` (run from repo root). |

## Cross-references

- **OPS-004 / T06.11 / D-0114:** `docs/eval/validation-commands.md` — pinned 4-command sequence consumed by §5.
- **SC1..SC5 / T06.01, T06.08, T06.09, T06.10 / D-0105, D-0111, D-0112, D-0113:** Per-SC closure entries in `decisions.md` consumed by §4.
- **AC1 / T06.07 / D-0110:** Linux-only declaration consumed by §2.1.
- **AC2 / T06.05 / D-0109:** CI deferral consumed by §7.2.
- **DOC-OQ6 / T06.04 / D-0108:** Suite naming + `quick.yaml` follow-up consumed by §6.2 + §7.3.
- **DOC-OQ8 / T06.03 / D-0107:** Time-offset contract referenced in §10.
- **DOC-OQ9 / T06.02 / D-0106:** macOS roadmap entry consumed by §7.2.
- **MIG-001 / T06.14 / D-0116:** Source sync migration consumed by §7.4.
- **MIG-003 / T06.15 / D-0117:** Platform follow-up plan consumed by §7.2.
- **M6 exit gate / T06.16 / D-CP06:** Consumes this artifact as the OPS-005 attestation.

## Regeneration / future updates

To re-walk the checklist after a code change:

```bash
# 1. Re-execute OPS-004 §6 reproduction recipe (captures T06.11 evidence)
( uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v 2>&1; \
  echo "EXIT_CODE=$?" ) > .dev/releases/current/cliEval/evidence/T06.11/01-targeted-pytest.log
( make verify-sync 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/02-make-verify-sync.log
( uv run superclaude eval doctor 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/03-eval-doctor.log
( uv run superclaude eval run --suite real --eval E1 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/04-eval-run-E1.log

# 2. Re-audit OPS-004 doc structure
uv run pytest tests/cli/eval/test_validation_commands.py -v

# 3. Re-walk OPS-005 link audit
bash -c '
  cd /config/workspace/IronClaude
  fail=0
  grep -oE "\(\.\./\.\./[^)#]+" docs/eval/release-checklist.md | sed -E "s/^\(//" | sort -u | \
  while read rel; do
    full="docs/eval/$rel"
    if [ -e "$full" ]; then
      echo "OK  $rel"
    else
      echo "FAIL $rel"; fail=1
    fi
  done
'
```

When B1 + B2 close and command 4 / row 6.6 attest GREEN, update:

- `release-checklist.md` §5 row 5.4 from ❌ to ✅.
- `release-checklist.md` §6 row 6.6 from DEFERRED to PASS with a link to the new full-run artifact.
- `release-checklist.md` §7.1 add a "**Closed:** <date>" line per follow-up.
- `release-checklist.md` §8 row 3 (release-gate reviewer) populated with name + date + decision.
- `decisions.md` OPS-005 entry status to `resolved`.
- This file's "Verification step result" section to record the full pass.
