# sc:reflect UC-1 pre-execution report: orchestrator-mode Phase 1 tasklist

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.78
citations_total: 117                # distinct cited ranges (about 243 citation occurrences)
citations_revalidated: 108           # evidence-validator: 117 - 8 dropped - 1 corrected
citations_dropped: 8                 # see "Evidence-validator results" below
citations_corrected: 1
citations_inferred: 1
citation_budget_policy: full_reread  # --depth deep forces full_reread
coverage_degraded: null
```

## Run context

- **Spec:** `docs/designs/orchestrator-mode.md` (1013 lines).
- **Tasklist:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` (355 items).
- **Mode:** pre (UC-1). **Tier reached:** 2. `artifacts/tier_decision.yaml` records `selected_tier: 2`, forced by the `--depth deep` override (section 5.1). The rubric would also have escalated: Tier-1 confidence 0.75 is below 0.85, S_domains is 5 and S_dev_density is 0.437.
- **Input drift:** none. `input_tree_sha256` (04f3f9658ad7eebd8f0e1193fc00823eb4fb3e919ec24b841d739a6e5bc5b3e1, 61 files) was recomputed in Wave 5 and matched (audit.log steps 0.4 and 5.x).
- **Reviewers:** three Tier-2 reviewers on the aliases claude-gw-tier1b, claude-gw-tier2 and claude-gw-tier1a. `t2_model_class_diversity: full`.
- **t2_vendor_diversity:** single. All three aliases are Anthropic models. This is a warning only.
- **calibrator_diversity:** degraded. Each card was calibrated by a model class other than its own reviewer's, but all three classes were also reviewers.
- **executor_class_resolved:** false. UC-1 runs before execution, so there is no executor.
- **Adversarial merge:** sc-adversarial-protocol Mode A over 3 variants. The base is variant-2 (scores: V2 0.847, V1 0.737, V3 0.717). `convergence_score: 1.00`: all 39 diff points were agreed by at least 2 of 3 advocates. `convergence_status: BLOCKED_BY_INVARIANTS`: the debate did not address three HIGH invariant-probe items, INV-001, INV-002 and INV-009. The merge folded all three into its fixes: INV-001 and INV-002 into Change 1 (F-01), INV-009 into Change 3 (F-03). The merge log reports 25 changes applied, 0 deviated, and 43 citations read with 0 broken.
- **Status:** `partial`. The adversarial return contract reports `status: partial` because convergence is BLOCKED_BY_INVARIANTS. No merge or validation step failed. The evidence-validator finished with 8 citations dropped, 1 corrected and no grounding gaps, so the status stays `partial` for the convergence reason only.

Citation aliases (copied from `adversarial/merged-verdict.yaml` `path_aliases`):

| Alias | Path |
|---|---|
| TL | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` |
| DESIGN | `docs/designs/orchestrator-mode.md` |
| research/04 | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/04-design-fixes-r3.md` |
| coverage-matrix | `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/coverage-matrix.yaml` |
| WORKER-CONTRACT.md | `src/superclaude/core/WORKER-CONTRACT.md` |
| test_worker_contract.py | `tests/skills/test_worker_contract.py` |
| conftest.py | `tests/cli/reflect/conftest.py` |
| contracts/__init__.py | `src/superclaude/contracts/__init__.py` |

## Verdict summary

Do not run the tasklist as written. Three HIGH findings block correct execution:

1. **F-01:** every owner gate deadlocks. This covers the shared HALT procedure, the inline text in 7.2 to 7.12, and 7.15.
2. **F-02:** the 8.3 `grep -c` count check can fail a correct module and pass an incomplete one.
3. **F-03:** 7.16 forbids the two commands its own step (6) must run.

The merged verdict has 23 findings: HIGH 3, MEDIUM 6, LOW 14. The evidence-validator dropped F-17 (LOW), so 22 survive: HIGH 3, MEDIUM 6, LOW 13. Requirement coverage after Tier-2 tracing is high: 0.95 of parsed rows and 0.941 of the union. The defects are in how the gates and checks are written, not in missing requirements. Calibrated confidence is 0.78 and the best-practice grade is 3 of 5.

## Coverage

| Measure | Tier 1 (literal ID tokens) | Tier 2 (traced, merged) |
|---|---|---|
| Parsed rows | 66 of 120 = 0.55 | 114 of 120 = 0.95 |
| Union (120 parsed + 15 inferred) | 76 of 135 = 0.563 | 127 of 135 = 0.941 |
| Union rows not covered | 59 | 8 |

**Why Tier 1 reported 0.55.** The Tier-1 matcher counted a row as covered only when the exact requirement ID appeared as a word-boundary token in the item text. Fuzzy matching was off, and "X to Y" ranges were not expanded (`coverage-matrix.yaml`, `matching` block). An item that delivers a requirement without writing its ID was counted as unmapped. The Tier-2 reviewers traced each requirement to the item that delivers it. Of the 127 covered union rows, 62 are covered by ID and 65 are covered in substance only (no literal ID). Those 65 rows explain the rise from 0.55.

Merged ledger: covered 62, covered in substance 65, partial 5, missing 2, false match 1. The per-card ledgers held 76 (V1), 51 (V2) and 24 (V3) rows, with 16 overlaps, which gives 135 unique rows.

Rows not fully covered:

| Row | Kind | Merged status | Finding |
|---|---|---|---|
| GQ-111 | parsed | missing | F-05 |
| GQ-112 | parsed | missing | F-05 |
| GQ-113 | parsed | partial | F-05 |
| SP-28 | parsed | partial | F-09 |
| step-1.0a | parsed | partial | F-19 |
| D6 | parsed | partial | F-06 |
| INF-013 | inferred | partial | F-08 |
| INF-001 | inferred | false match | F-05 |

Caveats from the merged ledger:

- A delegated row is covered only if the delegate item runs as written (A-001, INV-018). The three HIGH findings make that assumption unsafe until they are fixed.
- FR-010 is counted as covered in substance, but it reads ambiguously after research/04 edit 4 (F-12).
- DESIGN constraint B2 has no row in the matrix (F-23), so the 135-row union leaves it out.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | "`/task-builder` must copy the same rule into the task file: cite GAPS line 138 for counts and never edit the REPORT." | DESIGN:80 | Tier 1: containment 0.71 (7.26). Tier 2: false match (F-05) |
| INF-002 | "`report.py` keeps only pure code: `sanitize`, `render`, `SECTIONS`, the fixed strings and `CHECKED_ORCA_VERSION`. No `write_report` exists." | DESIGN:88 | Tier 1: containment 0.67 (8.12). Tier 2: covered |
| INF-003 | "Decision: write a temp file in the output directory, `fsync` it, then publish it under the report name with `os.link`, which fails when the name exists." | DESIGN:101 | Tier 1: containment 0.87 (9.1). Tier 2: covered |
| INF-004 | "`_publish` runs only after every exit-2 check, `collect`, `classify_all` and `render` have succeeded, so a usage error or an internal error in those steps never reaches the filesystem." | DESIGN:103 | Tier 1: containment 0.67 (9.1). Tier 2: covered |
| INF-005 | "B1: imports go one way, `commands -> {probes, classify, report} -> models`." | DESIGN:215 | Tier 1: containment 0.60 (2.12). Tier 2: covered (V2 verdict kept, X-010) |
| INF-006 | "B3: the read allowlist lives only in `probes.py`. Phase 2 `/sc:close` gets its own package, seam and allowlist; nothing in this package grows a write verb (FR-021)." | DESIGN:217 | Tier 1: none (best 14.14 at 0.52). Tier 2: covered |
| INF-007 | "B4: the command and skill are thin: no parsing, no classification, no file writes." | DESIGN:218 | Tier 1: none (best 11.9 at 0.56). Tier 2: covered |
| INF-008 | "B5: no type is redeclared from `superclaude.contracts`." | DESIGN:219 | Tier 1: none (best 8.14 at 0.50). Tier 2: covered |
| INF-009 | "R1, R2 and R3 land in one commit. Editing R1 or R2 without R3 fails the parity test." | DESIGN:705 | Tier 1: none (best 13.4 at 0.50). Tier 2: covered |
| INF-010 | "R1 and R6 avoid the words stop, retry, release, merge and removal in the sweep's description." | DESIGN:707 | Tier 1: containment 0.75 (11.3). Tier 2: covered |
| INF-011 | "No `.claude/` path is staged; `make sync-dev` then `make verify-sync` (step 1.25) refresh the dev copies." | DESIGN:708 | Tier 1: containment 0.77 (14.1). Tier 2: covered |
| INF-012 | "The pattern names `.dev/sweeps/` only. It does not cover `.dev/tasks/`, which stays tracked and always staged (CLAUDE.md rule)." | DESIGN:719 | Tier 1: none (best 7.1 at 0.56). Tier 2: covered |
| INF-013 | "An autouse fixture patches `subprocess.run`, `subprocess.Popen` and `os.system` to raise `AssertionError`. It steps aside only for a test carrying the existing `integration` marker, which is used by exactly one test, the real-git test below." | DESIGN:731 | Tier 1: containment 0.75 (8.8). Tier 2: partial (F-08) |
| INF-014 | "Where the REPORT text and this design differ, this design wins (section 13, REPORT differences)." | DESIGN:902 | Tier 1: containment 0.67 (5.4). Tier 2: covered (V2 verdict kept, X-010) |
| INF-015 | "They go into step 1.4a because the real-git test created there copies the repository `.gitignore`, so its FR-025 check-ignore assertions fail until the line exists." | DESIGN:942 | Tier 1: containment 0.68 (8.17). Tier 2: covered |

"Tier 2: covered" means covered or covered in substance in the merged ledger. The ledger does not split those two statuses per INF row.

POSTSCRIPT: no INF row has been dropped yet. The evidence-validator records any dropped row and its reason here.

## Deviations

Classification note: UC-1 runs before execution, so no executed work exists to sort into the four deviation categories (authorized, necessary, drift, regression). Each block gives the merged verdict's gap class instead and marks the category n/a. Wave 5 does not re-judge any finding.

### HIGH (blocks correct execution)

### Deviation D-01 (F-01): Every owner gate deadlocks a correct run

- **Severity:** HIGH. Gap class `gate-deadlock`.
- **Location:** TL:989
- **Mapped tasklist items:** 6.2; the shared procedure at TL:1140; 7.2, 7.4, 7.6, 7.8, 7.10, 7.12, 7.15, 7.16, 14.7; the HALT rule at TL:192; the phase rule at TL:978.
- **Spec section:** the DESIGN section 15.2 owner gates (as named at TL:1138).
- **Evidence:**
  - TL:989 (6.2): "Branch 1: if `status` is PENDING or `Chosen:` is empty, apply the HALT rule ... and STOP." No step copies the owner's answer into the file before this test. TL:982 writes `status: PENDING` with empty `Chosen:`, `Decided by:` and `Decision source:` lines, and TL:978 says "Nothing in this phase resolves it on the owner's behalf." A correct run therefore always takes Branch 1.
  - TL:1140: "Every HALT item below follows the item 6.2 procedure: Branch 1 (PENDING or empty `Chosen:`) applies the HALT rule". Fixing the shared procedure alone leaves the inline HALT text deadlocked (INV-001); see TL:1151, TL:1165, TL:1179, TL:1193, TL:1207 and TL:1221.
  - TL:1242 (7.15): "Branch 1: if `Run id:` is empty, apply the HALT rule ... Branch 2: set `status: RESOLVED`". Nothing copies the Run id in first, and Branch 2 has no condition and no check that the person supplied the id. This item was excluded from the earlier fix scope (INV-002).
  - TL:192: the HALT rule ends with "STOP, and do not tick the item" and has no rule for resuming after the owner answers.
  - TL:2481-2484 (14.7) carry the weaker Branch 2 wording.
  - Further anchors from the merged verdict: TL:982-992, TL:988, TL:1138, TL:1242-1248, TL:2488. (TL:184 and TL:1298-1314 were dropped by the evidence-validator: neither holds HALT or owner-answer text.)
- **Classification:** n/a (UC-1).
- **Classification rationale:** cards R2-G7 and R2-G2, plus new evidence from V1 and V3; debate points C-002 and X-001; invariants INV-001 to INV-008. R2-G2 rated itself HIGH as a gate bypass; calibration made it MEDIUM and merged it here.
- **Default remediation:** Add a transcription step before each branch test, HALT only on an empty answer, require a current-session owner quote before RESOLVED, and add an else-branch and a resume clause (R-01).

### Deviation D-02 (F-02): The 8.3 count check gives wrong results both ways

- **Severity:** HIGH. Gap class `broken-verification`.
- **Location:** TL:1434
- **Mapped tasklist item:** 8.3.
- **Spec section:** DESIGN section 7.2 Data model (DESIGN:447-468).
- **Evidence:**
  - TL:1434: "every class and constant name in DESIGN section 7.2 appears once (`grep -c` per name)". `grep -c` counts every line that contains the name. A name that is both defined and used, such as `SessionRow`, which `ClassifiedRow` holds as `row: SessionRow` (TL:1431), returns more than 1, so a correct module fails. A loose pattern also matches a name that is mentioned but never defined, so an incomplete module can pass.
  - The Verification line prints no explicit list of the names it expects. The action at TL:1431 does name the classes and the constants (`JSON_SCHEMA_VERSION`, `CLASSES`, `PACKAGE_STATES`, `SAFE_VALUES`), so the merged claim that the name set omits the DESIGN 7.2 constants is REFUTED by the evidence-validator; DESIGN:466 and DESIGN:468 were dropped from this sentence. `ClassifiedRow` is a builder decision at TL:1431.
  - Further anchors: TL:1426-1435.
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G5, plus new evidence from V1 and V2; debate point C-007; invariants INV-012 to INV-014.
- **Synthesis note:** TL:1434 does say "class and constant name". So the gap is that the check gives no explicit name list and uses a counting method that cannot work, not that it excludes constants by its wording. The evidence-validator confirmed this reading and refuted the merged claim "the name set omits the DESIGN 7.2 constants" (TL:1431 names them).
- **Default remediation:** Replace `grep -c` with an anchored definition pattern, expect exactly 1 per name, and list the names explicitly (R-02).

### Deviation D-03 (F-03): 7.16 forbids the commands its own step (6) runs

- **Severity:** HIGH. Gap class `self-contradicting-gate`.
- **Location:** TL:1258
- **Mapped tasklist items:** 7.16, 7.24.
- **Spec section:** DESIGN section 15.1, capture item 13 (DESIGN:894), and section 7.3 `ALLOWED_ORCA` (as named at TL:1248).
- **Evidence:**
  - TL:1248: "The ONLY commands allowed" are the eight templates at TL:1249-1256.
  - TL:1258, step (6): "Resolve the tab-map folder with `echo "${XDG_STATE_HOME:-$HOME/.local/state}/ccsession/orca-tabs/"`, record the printed path, then list that folder with `ls -la <printed path>`".
  - TL:1260: the check requires that "every command in the file is one of the eight templates or a file read". The two step (6) commands fail it. The forbidden list at TL:1257 names `check`, but the TL:1260 grep pattern does not.
  - TL:1314 (7.24 lens): prove that "every command in readonly-probe.md is one of the eight ALLOWED_ORCA templates of DESIGN 7.3 or a file read ... Each breach is BLOCKING."
  - DESIGN:894 says of `orca-tabs/` "(read the files only)" and does not say how the entries are listed.
- **Classification:** n/a (UC-1).
- **Classification rationale:** cards R2-G3, T1 F3, and new evidence from V2; debate point C-001; invariants INV-009 to INV-011. INV-009 found that allowing `echo` alone is not enough, because TL:1248, TL:1260 and the 7.24 lens would still reject it.
- **Default remediation:** Allow exactly the two step (6) commands in all four texts together, and add `check` to the TL:1260 grep (R-03).

### MEDIUM

### Deviation D-04 (F-04): The 14.11 lens does not name the FR-023 and FR-024 test folders

- **Severity:** MEDIUM. Gap class `lens-scope`.
- **Location:** TL:2509
- **Mapped tasklist item:** 14.11.
- **Spec section:** DESIGN:777, DESIGN:778.
- **Evidence:** TL:2509, DESIGN:777, DESIGN:778 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R1-G3 and new evidence from V1; debate point C-006.
- **Default remediation:** Name the test folders in the lens and state that NFR-012 has no test by design (R-04).

### Deviation D-05 (F-05): The GAPS line 138 rule is not carried into Key Constraints

- **Severity:** MEDIUM. Gap class `missing-requirement`.
- **Location:** TL:155-165 (Key Constraints; corrected by the evidence-validator from TL:1326-1331, which is item 7.26)
- **Mapped tasklist items:** Key Constraints; GQ-111, GQ-112 (no item); GQ-113 (partial).
- **Spec section:** DESIGN:78-80.
- **Evidence:** DESIGN:78: "wherever this design or a later task needs the gaps-log count, it cites GAPS line 138: 113 rows, 88 open, 25 resolved." DESIGN:80: "`/task-builder` must copy the same rule into the task file". The Key Constraints at TL:1326-1331 do not carry the rule.
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G1 (self-rated HIGH, calibrated MEDIUM); debate points C-005, C-015, X-008.
- **Synthesis note:** the merged verdict's claim text reads "88 resolved, 25 open". DESIGN:78 reads "88 open, 25 resolved". The fix must copy the DESIGN wording.
- **Default remediation:** Add the rule with the DESIGN:78 counts and GQ-113 to Key Constraints, and mark INF-001 as a false match (R-05).

### Deviation D-06 (F-06): The 7.4 gate approves worker-contract text it never shows

- **Severity:** MEDIUM. Gap class `approval-scope`.
- **Location:** TL:1156-1168
- **Mapped tasklist items:** 7.3, 7.4; coverage row D6.
- **Spec section:** WC-16 (DESIGN:5, DESIGN:988).
- **Evidence:** DESIGN:5, DESIGN:988, TL:1156-1168, TL:2877, WORKER-CONTRACT.md:110 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G4. Kept separate from F-01 per INV-021.
- **Default remediation:** Put the full text and cadence into 7.3, and make 7.4 require approval of that text. Apply this together with the F-01 edit at 7.4 (R-06).

### Deviation D-07 (F-07): Item 8.1 gives one PASS for six gate files

- **Severity:** MEDIUM. Gap class `weak-verification`.
- **Location:** TL:1417-1421
- **Mapped tasklist item:** 8.1.
- **Spec section:** n/a.
- **Evidence:** TL:1417-1421 (copied from the merged verdict). One missing file can hide behind a single PASS.
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G6 (self-rated HIGH, calibrated MEDIUM); debate point X-008.
- **Default remediation:** Check each of the six gate files separately (R-07).

### Deviation D-08 (F-08): The 8.9 guard has no negative test

- **Severity:** MEDIUM. Gap class `missing-negative-test`.
- **Location:** TL:1467-1476
- **Mapped tasklist items:** 8.9; coverage row INF-013.
- **Spec section:** DESIGN:731 (INF-013).
- **Evidence:** TL:1467-1476 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G8 (self-rated HIGH, calibrated MEDIUM); debate points X-007, X-008.
- **Default remediation:** Add a test that proves the guard rejects a bad input, and relabel INF-013 (R-08).

### Deviation D-09 (F-09): No item delivers the SP-28 rationale

- **Severity:** MEDIUM. Gap class `missing-deliverable`.
- **Location:** TL:1535-1539
- **Mapped tasklist items:** 14.9, 8.18; coverage row SP-28.
- **Spec section:** DESIGN item 19 (DESIGN:987).
- **Evidence:** DESIGN:987, TL:1535-1539 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G10; debate point C-009.
- **Default remediation:** Add an SP-28 rationale deliverable to 14.9 (R-09).

### LOW

### Deviation D-10 (F-10): Nothing HALTs on a CHANGED anchor in item 1.4

[INFERRED] Claim: nothing HALTs when item 1.4 records an anchor as CHANGED; TL:224 only adds a note and TL:233 handles MOVED and a missing file. No reviewer card holds this finding; it comes from the invariant probe only and was not calibrated.

- **Severity:** LOW. Gap class `missing-halt`.
- **Location:** TL:233
- **Mapped tasklist item:** 1.4.
- **Spec section:** n/a.
- **Evidence:** TL:224, TL:229-234, WORKER-CONTRACT.md:110, test_worker_contract.py:25, test_worker_contract.py:155-173 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** debate point A-007, new evidence from V1, invariant INV-017. Kept at LOW, not INV-017's MEDIUM.
- **Default remediation:** Add one HALT sentence for a CHANGED anchor to TL:233 (R-10).
- **[INFERRED] notes:** [INFERRED] no reviewer card cites this gap directly; the evidence-validator confirmed TL:233 (item 1.4 has no CHANGED HALT; TL:224 belongs to item 1.3).

### Deviation D-11 (F-11): The 5.5 pin greps check only the :545 form

- **Severity:** LOW. Gap class `weak-verification`.
- **Location:** TL:796
- **Mapped tasklist item:** 5.5.
- **Spec section:** DESIGN:677-680, DESIGN:686.
- **Evidence:** TL:796, TL:827 (copied from the merged verdict; the card cited TL:792, corrected to TL:796).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G3.
- **Default remediation:** Grep every pinned line form (R-11).

### Deviation D-12 (F-12): FR-010 is ambiguous after research/04 edit 4

- **Severity:** LOW. Gap class `ambiguous-wording`.
- **Location:** TL:251
- **Mapped tasklist items:** 2.2, the nine scope notes, 3.1; coverage row FR-010.
- **Spec section:** FR-010 as edited by research/04.
- **Evidence:** research/04:90, research/04:115-116, research/04:148, TL:249, TL:293-349, TL:423, TL:425 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** cards R3-G1 and new evidence from V3; debate points C-003, X-002, A-001; invariants INV-015, INV-016. The rule is ambiguous, not lost, so this is LOW rather than MEDIUM.
- **Default remediation:** Write "one or more matching rows" consistently or drop the "verbatim" claim at TL:251 (R-12).

### Deviation D-13 (F-13): The 3.1 fallback points at the wrong DESIGN section

- **Severity:** LOW. Gap class `wrong-pointer`.
- **Location:** TL:425
- **Mapped tasklist item:** 3.1.
- **Spec section:** the observation rules, DESIGN:494-505.
- **Evidence:** TL:425, research/04:148 (copied from the merged verdict; the card cited TL:423, corrected to TL:425).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G2.
- **Default remediation:** Point the fallback at DESIGN:494-505 (R-13).

### Deviation D-14 (F-14): Item 11.1 omits the sweep cadence

- **Severity:** LOW. Gap class `missing-constraint`.
- **Location:** TL:1952
- **Mapped tasklist item:** 11.1.
- **Spec section:** the worker-contract cadence.
- **Evidence:** TL:1952, TL:773, TL:787, TL:2258 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G5; debate point C-012.
- **Default remediation:** Add "at most once every 5 minutes" to 11.1 (R-14).

### Deviation D-15 (F-15): Item 13.6 adds a CHANGELOG bullet DESIGN R8 does not ask for

- **Severity:** LOW. Gap class `scope-drift`.
- **Location:** TL:2293
- **Mapped tasklist item:** 13.6.
- **Spec section:** DESIGN R8 (DESIGN:701).
- **Evidence:** TL:2293, DESIGN:701 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G6; debate point C-013.
- **Default remediation:** Drop the CHANGELOG bullet (R-15).

### Deviation D-16 (F-16): Item 8.3 does not run the contracts architecture lint

- **Severity:** LOW. Gap class `missing-check`. Paired with F-02 on item 8.3.
- **Location:** TL:1430
- **Mapped tasklist item:** 8.3.
- **Spec section:** n/a.
- **Evidence:** contracts/__init__.py:1-6, contracts/__init__.py:35-36, contracts/__init__.py:302-313, TL:1430 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R3-G8; debate point C-014.
- **Default remediation:** Add `make lint-architecture` to 8.3 (R-16).

### Deviation D-17 (F-17): DROPPED by the evidence-validator

- **Merged claim:** the 8.8 fake seam does not record argv and env.
- **Why dropped:** both citations are unfounded. TL:1467 says `patch_git` records `(cwd, args, timeout)` and the env, and `patch_orca` records argv, so it contradicts the claim. `tests/cli/reflect/conftest.py:59-74` holds a `patch_git` that records nothing, so it cannot be the model to copy. No surviving evidence; the finding is removed.

### Deviation D-18 (F-18): Item 14.5 counts the whole tree instead of the five DESIGN folders

- **Severity:** LOW. Gap class `weak-verification`.
- **Location:** TL:2470
- **Mapped tasklist item:** 14.5.
- **Spec section:** DESIGN:939.
- **Evidence:** TL:2470, DESIGN:939 (copied from the merged verdict; DESIGN:940, the pipx help check, was dropped by the evidence-validator).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R1-G6, count part only. The pipx clause was dropped (X-006).
- **Default remediation:** Run `git diff` over the five folders (R-18).

### Deviation D-19 (F-19): Item 7.17 does not name DESIGN open item 3 and the M2 route

- **Severity:** LOW. Gap class `missing-pointer`.
- **Location:** TL:1265
- **Mapped tasklist items:** 7.17; coverage row step-1.0a.
- **Spec section:** DESIGN open item 3 (DESIGN:971); DESIGN:874.
- **Evidence:** DESIGN:874, DESIGN:971, TL:1258, TL:1265 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R1-G1, naming part only; the target was corrected to open item 3 (X-005); invariant INV-020.
- **Default remediation:** Add one line to 7.17 naming open item 3 and M2 (R-19).

### Deviation D-20 (F-20): Items 8.6 and 9.2 verify by counts, not content

- **Severity:** LOW. Gap class `weak-verification`.
- **Location:** TL:1453-1456
- **Mapped tasklist items:** 8.6, 9.2.
- **Spec section:** n/a.
- **Evidence:** TL:1453-1456, TL:1634 (copied from the merged verdict; the card cited TL:1635-1636, corrected to TL:1634).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G4, in part.
- **Default remediation:** Replace the line counts and `git diff --stat` with content and placement checks (R-20).

### Deviation D-21 (F-21): Several FR and NFR ids are not written on their delivery items

- **Severity:** LOW. Gap class `traceability`.
- **Location:** items 12.1, 8.10, 8.6, 10.7, 10.3 (TL:1784 was dropped by the evidence-validator: it is item 10.2 and does write its ids).
- **Mapped tasklist items:** 12.1, 8.10, 8.6, 10.7, 10.3.
- **Spec section:** DESIGN:777, DESIGN:783.
- **Evidence:** TL:2677 (copied from the merged verdict). TL:2677 is a 14.x QA item, not a delivery item.
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R1-G2, in part; debate point C-004.
- **Default remediation:** Write each id on its delivery item (R-21).

### Deviation D-22 (F-22): The final summary item omits the DESIGN commit grouping

- **Severity:** LOW. Gap class `missing-step`.
- **Location:** TL:2754
- **Mapped tasklist item:** 14.46.
- **Spec section:** DESIGN:705, DESIGN:932.
- **Evidence:** DESIGN:705 reads "R1, R2 and R3 land in one commit. Editing R1 or R2 without R3 fails the parity test." Also TL:2254 and TL:2754 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R1-G4, in part; debate point C-010.
- **Default remediation:** Add the commit-grouping line to 14.46 (R-22).

### Deviation D-23 (F-23): DESIGN constraint B2 has no coverage-matrix row

- **Severity:** LOW. Gap class `traceability`.
- **Location:** coverage-matrix:232-237
- **Mapped tasklist item:** unmapped (coverage-matrix B2 row).
- **Spec section:** DESIGN:215-219 (B1 to B5).
- **Evidence:** DESIGN:216 reads "B2: `classify` and `render` treat every path as data only ... which the NFR-004 import test enforces". Also coverage-matrix:849-880 and TL:1784-1785 (copied from the merged verdict).
- **Classification:** n/a (UC-1).
- **Classification rationale:** card R2-G9, matrix part only. The import-check part was dropped because DESIGN:216 already holds the NFR-004 import test (X-004).
- **Default remediation:** Add a B2 row mapped to NFR-004 (R-23).

## Gap registry

| ID | Severity | Gap class | Affected items | Coverage rows touched | Recommendation |
|---|---|---|---|---|---|
| F-01 | HIGH | gate-deadlock | 6.2, shared procedure, 7.2, 7.4, 7.6, 7.8, 7.10, 7.12, 7.15, 7.16, 14.7, HALT rule | all delegated rows (A-001) | R-01 |
| F-02 | HIGH | broken-verification | 8.3 | none | R-02 |
| F-03 | HIGH | self-contradicting-gate | 7.16, 7.24 | none | R-03 |
| F-04 | MEDIUM | lens-scope | 14.11 | none | R-04 |
| F-05 | MEDIUM | missing-requirement | Key Constraints | GQ-111, GQ-112, GQ-113, INF-001 | R-05 |
| F-06 | MEDIUM | approval-scope | 7.3, 7.4 | D6 | R-06 |
| F-07 | MEDIUM | weak-verification | 8.1 | none | R-07 |
| F-08 | MEDIUM | missing-negative-test | 8.9 | INF-013 | R-08 |
| F-09 | MEDIUM | missing-deliverable | 14.9, 8.18 | SP-28 | R-09 |
| F-10 | LOW | missing-halt | 1.4 | none | R-10 |
| F-11 | LOW | weak-verification | 5.5 | none | R-11 |
| F-12 | LOW | ambiguous-wording | 2.2, nine scope notes, 3.1 | FR-010 | R-12 |
| F-13 | LOW | wrong-pointer | 3.1 | none | R-13 |
| F-14 | LOW | missing-constraint | 11.1 | none | R-14 |
| F-15 | LOW | scope-drift | 13.6 | none | R-15 |
| F-16 | LOW | missing-check | 8.3 | none | R-16 |
| ~~F-17~~ | LOW | test-design | 8.8 | none | dropped by the evidence-validator |
| F-18 | LOW | weak-verification | 14.5 | none | R-18 |
| F-19 | LOW | missing-pointer | 7.17 | step-1.0a | R-19 |
| F-20 | LOW | weak-verification | 8.6, 9.2 | none | R-20 |
| F-21 | LOW | traceability | 12.1, 8.10, 8.6, 10.7, 10.3 | none | R-21 |
| F-22 | LOW | missing-step | 14.46 | none | R-22 |
| F-23 | LOW | traceability | coverage-matrix | B2 (no row) | R-23 |

## Not carried

The merge dropped or narrowed these reviewer items (from `not_carried` in the merged verdict):

- R1-G5 and R3-G9: confirmations, not gaps (C-011, S-007, M-7).
- R3-G10: refuted by TL:982 and TL:989 (X-001).
- R1-G6 pipx clause: false, because TL:2488 shows `pipx run --spec` installs the dependencies (X-006). The count part survives as F-18.
- R1-G1 "open item 2" target and "no owner step" claim: DESIGN:971 is open item 3 (X-005). Only the naming survives as F-19.
- R2-G9 import-check part: DESIGN:216 already holds the NFR-004 import test (X-004). Only the matrix part survives as F-23.
- R2-G2 label and severity (gate bypass, HIGH): calibrated MEDIUM and merged into F-01.
- R2-G1, R2-G6, R2-G8 self-rated HIGH: calibrated MEDIUM (X-008), carried as F-05, F-07, F-08.
- R3-G7 missing-reuse class: downgraded to a test-design preference (X-012), carried as F-17.
- R3-G1 "rule lost" at MEDIUM: the rule is ambiguous, not lost (X-002, C-003), carried as F-12 at LOW.
- V3 INF-005 and INF-014 false-match verdicts: V2 verdicts kept (X-010).
- V1 "2.16 is an edit": 2.16 is a QA lens, TL:347 (X-003).
- R1-G2 new QA item: the id mapping in F-21 covers it.
- S-008 deviation category: no variant has one; accepted as is (M-5).

## Best-practice grade

**Grade: 3 of 5.** Card grades: V1 4, V2 2, V3 4.

Reasons (from the merged verdict):

- Plus: the gates are well specified, with explicit HALT rules and named owner lines.
- Plus: the design-fix edits anchor by heading, not by line number, so they survive line drift.
- Minus: three HIGH defects block correct execution: the owner-gate deadlock (F-01), the 8.3 count check (F-02) and the 7.16 command allowance (F-03).

**Calibrated confidence: 0.78.** This is the mean of the three calibrated card confidences: V1 0.68, V2 0.85, V3 0.80 (exact mean 0.7767). Two or more sources hold each of the three HIGH findings. The Tier-1 card was calibrated at 0.75 and escalated.

## Evidence-validator results

Mode `full_reread` (depth deep). 117 distinct cited ranges re-Read; 108 revalidated, 8 dropped, 1 corrected. All 15 inferred-requirement quotes matched their DESIGN lines, so no INF row was dropped and `coverage_pct_union` is unchanged.

| Report site | Citation | Outcome |
|---|---|---|
| D-01 further anchors | TL:184 | dropped: no HALT text within 3 lines (the rule is at TL:192) |
| D-01 further anchors | TL:1298-1314 | dropped: lens items 7.22 to 7.24, no Branch or owner-answer step |
| D-02 | DESIGN:466, DESIGN:468 | dropped: the "constants omitted" claim is refuted by TL:1431; the counting-method gap stands |
| D-17, R-17 | TL:1467, conftest.py:59-74 | dropped: TL:1467 shows argv and env are recorded; the finding is removed |
| D-18 | DESIGN:940 | dropped: it is the pipx help check, not the folder list |
| D-21 | TL:1784 | dropped: item 10.2, which writes its ids |
| D-05, R-05 | TL:1326-1331 | corrected to TL:155-165 (Key Constraints) |

Special checks: D-05 confirmed (DESIGN:78 reads "113 rows, 88 open, 25 resolved"). D-10 confirmed: item 1.4 (TL:229-234) has no CHANGED HALT; TL:224 is item 1.3. No grounding gap was raised, so the Grounding Gaps heading is removed as the template requires.

## Inferred-claim audit

- `citations_inferred: 1` (F-10)
- Inferred fraction: `1 / 117` = 0.009

The WARN block is not triggered: inferred claims are far below half of all citations.

## Recommendations

### Recommendation R-01: Remove the owner-gate deadlock at every HALT site

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Edit 6.2, the shared procedure at TL:1140, the six inline items 7.2 to 7.12, 7.15 and 14.7:
  1. Add a transcription step before the branch test. In 7.15 it also copies Run id, Given by and Source.
  2. Branch 1 HALTs only when `Chosen:` is empty. In 7.15 it HALTs only when `Run id:` is empty.
  3. Branch 2 sets RESOLVED only when every line is filled and `Decision source:` quotes the owner's words from the current session. Use the same quote clause in 14.7 and 7.15, and recheck it in 7.16 before any live call.
  4. Add a final else-branch that HALTs.
  5. HALT if the owner's words are not in the current session.
  6. Add a resume clause to the HALT rule at TL:192 and TL:978.
  7. State the line count as "the header plus three named lines; OQ-8 keeps its three lines".
- **Verifier:** `grep -n "PENDING or"` on the tasklist returns 0 lines, and the else-branch sentence appears at 9 sites plus 7.15. Re-Read TL:192 to confirm the resume clause.
- **Linked deviation(s):** D-01, D-06 (apply the 7.4 edits together).
- **Priority:** P0

### Recommendation R-02: Replace the 8.3 grep -c count with an anchored definition check

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** At TL:1434, use the pattern `^(class NAME\b|NAME\s*[:=])` and expect exactly 1 match per name. List the names explicitly: the DESIGN 7.2 names at DESIGN:447-468, including `JSON_SCHEMA_VERSION`, `CLASSES`, `PACKAGE_STATES` and `SAFE_VALUES`, plus `ClassifiedRow`.
- **Verifier:** Re-Read TL:1434 to confirm the anchored pattern and the explicit name list. On a correct `models.py`, each name returns exactly 1.
- **Linked deviation(s):** D-02, D-16 (same item).
- **Priority:** P0

### Recommendation R-03: Allow the two step (6) discovery commands in all four 7.16 texts

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- **Change:** Allow exactly `echo "${XDG_STATE_HOME:-$HOME/.local/state}/ccsession/orca-tabs/"` and `ls -la <printed path>` in step (6). Edit four texts together: (a) TL:1248, (b) TL:1257-1258, (c) TL:1260, (d) the 7.24 lens at TL:1314. In addition:
  - Add `check` to the TL:1260 grep so it matches the TL:1257 forbidden list.
  - Drop the forbidden-list sentence expectation, because the grep runs over command records only.
  - Add one line to the 7.24 lens saying that `ls -la` of that folder is how its entries are listed (DESIGN:894 says "read the files only").
- **Verifier:** `grep -nE '^\$ (ls|echo)\b'` over `artifacts/readonly-probe.md` finds only the two step (6) commands. Re-Read TL:1260 to confirm `check` is in the pattern.
- **Linked deviation(s):** D-03
- **Priority:** P0

### Recommendation R-04: Name the FR-023 and FR-024 test folders in the 14.11 lens

- **File:** tasklist (TL)
- **Change:** At TL:2509, name tests/sweep/, tests/commands/, tests/skills/, tests/core/ or tests/recommend/, and state that NFR-012 has no test by design.
- **Verifier:** Re-Read TL:2509 to confirm the folder names and the NFR-012 sentence.
- **Linked deviation(s):** D-04
- **Priority:** P1

### Recommendation R-05: Carry the GAPS line 138 rule into Key Constraints

- **File:** tasklist (TL); the coverage ledger.
- **Change:** Add the rule to Key Constraints (TL:155-165) with the counts copied from DESIGN:78 (113 rows, 88 open, 25 resolved) and name GQ-113. Mark INF-001 as a false match.
- **Verifier:** Re-Read TL:155-165 to confirm the counts match DESIGN:78 word for word. Re-run `/sc:reflect --mode pre` and confirm that GQ-111 and GQ-112 are no longer missing.
- **Linked deviation(s):** D-05
- **Priority:** P1

### Recommendation R-06: Put the full worker-contract text into 7.3 and gate 7.4 on it

- **File:** tasklist (TL)
- **Change:** Put the full WC-16 text and cadence into 7.3 (TL:1156-1168), make the 7.4 gate require approval of that text, and mark D6 as partial in the ledger. Apply this together with the R-01 edit at 7.4.
- **Verifier:** Re-Read TL:1156-1168 to confirm the full text, the cadence and the approval clause.
- **Linked deviation(s):** D-06
- **Priority:** P1

### Recommendation R-07: Give each 8.1 gate file its own PASS line

- **File:** tasklist (TL)
- **Change:** At TL:1417-1421, check each of the six gate files separately, with its own PASS line.
- **Verifier:** Re-Read TL:1417-1421 to confirm six separate checks.
- **Linked deviation(s):** D-07
- **Priority:** P1

### Recommendation R-08: Add a negative guard test to 8.9

- **File:** tasklist (TL)
- **Change:** At TL:1467-1476, add a test proving the guard rejects a bad input. Relabel INF-013 as "construction assigned; verification partial, see F-08".
- **Verifier:** Re-Read TL:1467-1476 to confirm the negative test step and its expected failure.
- **Linked deviation(s):** D-08
- **Priority:** P1

### Recommendation R-09: Add the SP-28 rationale deliverable to 14.9

- **File:** tasklist (TL)
- **Change:** Add an SP-28 rationale deliverable to 14.9 for DESIGN item 19 (DESIGN:987). Refer to 8.18 as a "QA edge-case lens" (TL:1535-1539).
- **Verifier:** `grep -n "SP-28"` on the tasklist shows a 14.9 deliverable.
- **Linked deviation(s):** D-09
- **Priority:** P1

### Recommendation R-10: HALT on a CHANGED anchor in 1.4

- **File:** tasklist (TL)
- **Change:** Add one HALT sentence for a CHANGED anchor to TL:233.
- **Verifier:** Re-Read TL:229-234 to confirm the HALT covers CHANGED.
- **Linked deviation(s):** D-10
- **Priority:** P2

### Recommendation R-11: Grep every pinned line form in 5.5

- **File:** tasklist (TL)
- **Change:** At TL:796, grep 'line 545', 'line 865', 'line 470', 'line 398' and 'line 624'.
- **Verifier:** Re-Read TL:796 to confirm all five patterns.
- **Linked deviation(s):** D-11
- **Priority:** P2

### Recommendation R-12: Settle the FR-010 wording

- **File:** tasklist (TL); research/04.
- **Change:** Write "one or more matching rows" at 2.2 (TL:249), in the nine scope notes (TL:293-349) and at research/04:90, or drop the "verbatim" claim at TL:251. Reword TL:425.
- **Verifier:** The same FR-010 wording appears at all three places, or TL:251 no longer says "verbatim".
- **Linked deviation(s):** D-12
- **Priority:** P2

### Recommendation R-13: Point the 3.1 fallback at the observation rules

- **File:** tasklist (TL)
- **Change:** At TL:425, point the fallback at DESIGN:494-505.
- **Verifier:** Re-Read TL:425 to confirm the pointer.
- **Linked deviation(s):** D-13
- **Priority:** P2

### Recommendation R-14: Add the sweep cadence to 11.1

- **File:** tasklist (TL)
- **Change:** Add "at most once every 5 minutes" to 11.1 (TL:1952).
- **Verifier:** `grep -n "at most once every 5 minutes"` matches inside 11.1.
- **Linked deviation(s):** D-14
- **Priority:** P2

### Recommendation R-15: Drop the CHANGELOG bullet from 13.6

- **File:** tasklist (TL)
- **Change:** Remove the CHANGELOG bullet at TL:2293.
- **Verifier:** Re-Read 13.6 to confirm that no CHANGELOG bullet remains.
- **Linked deviation(s):** D-15
- **Priority:** P2

### Recommendation R-16: Run the architecture lint in 8.3

- **File:** tasklist (TL)
- **Change:** Add `make lint-architecture` to the 8.3 verification (TL:1430).
- **Verifier:** `grep -n "lint-architecture"` matches inside 8.3.
- **Linked deviation(s):** D-16
- **Priority:** P2

### Recommendation R-17: WITHDRAWN

- D-17 was dropped by the evidence-validator (TL:1467 already records argv and env). No change is recommended.

### Recommendation R-18: Check the five DESIGN folders in 14.5

- **File:** tasklist (TL)
- **Change:** At TL:2470, run `git diff` over the five folders named at DESIGN:939-940 and confirm that no `src/superclaude` path was added.
- **Verifier:** Re-Read TL:2470 to confirm the per-folder diff.
- **Linked deviation(s):** D-18
- **Priority:** P2

### Recommendation R-19: Name open item 3 and M2 in 7.17

- **File:** tasklist (TL)
- **Change:** Add one line to 7.17 (TL:1265) naming DESIGN open item 3 (DESIGN:971) and the M2 route.
- **Verifier:** Re-Read 7.17 to confirm the line.
- **Linked deviation(s):** D-19
- **Priority:** P2

### Recommendation R-20: Verify 8.6 and 9.2 by content and placement

- **File:** tasklist (TL)
- **Change:** Replace the line counts at TL:1453-1456 and the `git diff --stat` at TL:1634 with content and placement checks.
- **Verifier:** Re-Read both items to confirm that they quote the expected text and its anchor.
- **Linked deviation(s):** D-20
- **Priority:** P2

### Recommendation R-21: Write the FR and NFR ids on their delivery items

- **File:** tasklist (TL)
- **Change:** Write FR-023 on 12.1, NFR-003 on 8.10, FR-025 on 8.6, FR-002 on 10.7 and NFR-014 on 10.3.
- **Verifier:** Grep each id and confirm that it matches inside its delivery item.
- **Linked deviation(s):** D-21
- **Priority:** P2

### Recommendation R-22: Add the commit grouping to 14.46

- **File:** tasklist (TL)
- **Change:** Add the commit-grouping line (DESIGN:705, DESIGN:932) to 14.46 (TL:2754).
- **Verifier:** Re-Read 14.46 to confirm the line.
- **Linked deviation(s):** D-22
- **Priority:** P2

### Recommendation R-23: Add a B2 row to the coverage matrix

- **File:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/coverage-matrix.yaml`
- **Change:** Add a B2 row (DESIGN:216) mapped to NFR-004.
- **Verifier:** `grep -n "id: B2"` on the coverage matrix returns one row.
- **Linked deviation(s):** D-23
- **Priority:** P2

### Recommendation R-24: Re-run the pre-execution reflection after the P0 fixes

- **File:** n/a
- **Change:** After R-01 to R-03 land, run `/sc:reflect --mode pre --depth deep` again on the same spec and tasklist.
- **Verifier:** The new merged verdict has no HIGH finding, and `convergence_status` is not BLOCKED_BY_INVARIANTS.
- **Linked deviation(s):** none
- **Priority:** P0
- **Provenance:** orchestrator synthesis addition (Wave 5), not a merged-verdict finding.
