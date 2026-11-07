# Adversarial Debate Transcript

Subject: the P2 static plan `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md`, reviewed against `source.md` and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
Variants are three independent reviewer outputs: V1 (sonnet, analyzer), V2 (haiku, qa), V3 (opus, refactorer).

## Metadata

- Depth: standard
- Rounds completed: 2, plus the Round 2.5 invariant probe (`invariant-probe.md`)
- Convergence achieved: 100% (16 of 16 scored points)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3
- Gate status: BLOCKED_BY_INVARIANTS (INV-001, INV-002)

Round files:

- Round 1: `rounds/round1-advocate-1.md`, `rounds/round1-advocate-2.md`, `rounds/round1-advocate-3.md`
- Round 2: `rounds/round2-advocate-1.md`, `rounds/round2-advocate-2.md`, `rounds/round2-advocate-3.md`
- Round 2.5: `invariant-probe.md`

## Round 1

### Advocate for Variant 1 (sonnet, analyzer) - `rounds/round1-advocate-1.md`

- **Position**: V3 should be the spine of the merge. V1 contributes findings V3 lacks.
- **Steelman of others**: V3 has the widest coverage and the only nested-call sweep. V2 has the cleanest evidence.
- **Key strengths claimed**: U-004 (task-builder CLI-mode `reflect run --fix --promote` gate), U-005 (spec-panel socratic), the `refs/return-contract.md` coherence point on C-002, the per-gate phrase inventory (R1-F10).
- **Weaknesses identified in others**: R3-F1 overstates its harm; V2 has no nested-call sweep.
- **Concessions**: R3-F1 is a real P1; C-003 goes to V2's scope; R1-F6 rested on a misread of D-P2-13; R1-F9 should be dropped; R1-F8 partly; V1's "none" and "authorized" classes were wrong; X-001 is P1; plan:248 settles FR-G5.
- **Assumptions**: A-001 QUALIFY (premise false: `sc-cli-eval-protocol/SKILL.md:138-139` labels the safety flags); A-002 QUALIFY; A-003 ACCEPT.

### Advocate for Variant 2 (haiku, qa) - `rounds/round1-advocate-2.md`

- **Position**: merge, with V2's evidence form and severity calls kept.
- **Steelman of others**: V3's nested sweep finds defects V2 missed; V1's conditional gate is real.
- **Key strengths claimed**: correct P1 on cli-eval (R2-F1); relationship-level negatives for gate phrases (R2-F2); full 15-command scope of "left out (WC-4)" (R2-F3); lowest false-claim rate.
- **Weaknesses identified in others**: V3 overstates severity and harm; V1 misclassifies several findings.
- **Concessions**: V2 missed the nested calls; R2-F4 is acceptable at P3; R2-F5 is a matrix gap, not drift; the uniform "Drift" label was wrong.
- **Assumptions**: same verdicts as V1 (A-001 QUALIFY, A-002 QUALIFY, A-003 ACCEPT), noting that WC-7 fan-out is unchanged.

### Advocate for Variant 3 (opus, refactorer) - `rounds/round1-advocate-3.md`

- **Position**: V3 as the base.
- **Steelman of others**: V2 has the best evidence form and the right cli-eval severity; V1 found U-004 and C-004.
- **Key strengths claimed**: the nested-call sweep (R3-F1 tasklist Stage 9 `sc:task`, R3-F4 release-split `sc:analyze`, R3-F5 reflect Wave 1B `tech-research`); the parametrized WC-4 test (R3-F11); the `verified_ok` checks.
- **Weaknesses identified in others**: V2's narrow coverage; V1's classification errors.
- **Concessions**: R3-F1 harm (commit/push) overstated; R3-F2 partly; R3-F3 test-pin claim; R3-F6; R3-F7; R3-F12; R3-F13; the uniform drift label; missed U-004 and C-004; X-001 is P1.
- **Assumptions**: A-003 is STATED (spec:62), not an assumption.

## Round 2

### Advocate for Variant 1 - `rounds/round2-advocate-1.md`

- **Rebuttals**: keeps U-004 and the per-gate phrase lists; accepts V3 as base.
- **New evidence**: Task 16 must depend on Task 12; the Task 20 literal must change with the R3-F1 fix; spec:77 names task-builder:2237; A-003 is STATED; the loop-back at task-builder:1607 requires `<n>`.
- **Concessions carried**: all Round 1 concessions stand.
- **Final positions**: S-001 V3, S-002 merge, S-003 V2, C-001 merge, C-002 merge, C-003 merge, C-004 merge, C-005 V2 (P3), C-006 V3, C-007 merge, C-008 merge, X-001 V2 (P1), X-002 V3 (drift), A-001 qualify, A-002 qualify, A-003 accept (STATED).

### Advocate for Variant 2 - `rounds/round2-advocate-2.md`

- **Rebuttals of V1**: `--fix --promote` is not an outward action; "launches with no safety inputs" is overstated; V3's `verified_ok` must be bounded.
- **New evidence**: the eval-docs-loader digest is authoritative for cli-eval flags (`sc-cli-eval-protocol/SKILL.md:30-33,46-58`); `_artifacts_clause` reads only the first matching line (`tests/skills/test_worker_contract.py:770-775`); `_check_unattended_section` checks presence only (test:509-512); the task-builder CLI gate writes its output at task-builder:2239.
- **Final positions**: S-001 merge, S-002 merge, S-003 V2, C-001 to C-004 merge, C-005 V2 (P3), C-006 merge, C-007 merge, C-008 merge, X-001 V2 (P1), X-002 V3, A-001 merge/qualify, A-002 merge/qualify, A-003 V3 (accept, STATED).

### Advocate for Variant 3 - `rounds/round2-advocate-3.md`

- **Rebuttals**: concedes push in R3-F1 but restores a conditional commit: a TFEP inside a nested `sc:task` keeps the committed-report default (`sc-task-protocol/SKILL.md:61,266`) because Stage 9 passes no `--unattended`. Concedes the `verified_ok` wording (bounded per-check claims), drops the R3-F13 example, narrows R3-F6 to the tasklist handoff and R3-F7 to the Safety Threshold clause, drops the R3-F2 FR-G5/`--no-pty` part (plan:248). Sides with V2 against V1 on `--fix --promote` and on "no safety inputs".
- **New evidence**: (1) NEW finding: troubleshoot `--diagnosability-handoff` calls `Skill sc:workflow-protocol` (`sc-troubleshoot-protocol/refs/diagnosability-audit.md:245,250`; `SKILL.md:645`; `troubleshoot.md:148`); Task 11 nests only `adversarial` (plan:220); "diagnosability" appears 0 times in the plan; the unflagged workflow runs `git add .dev/tasks` (`sc-workflow-protocol/SKILL.md:28`), breaking WC-9 (spec:77). P1 drift. (2) R3-F1 has a second harm: the impact path `.dev/impact/task-<slug>` (`sc-task-protocol/SKILL.md:94`) lies outside the report dir (WC-4, WC-11). (3) The R3-F1 fix must change two test literals. (4) The C-002 fix must reach the line `_artifacts_clause` reads.
- **Final positions**: S-001 merge, S-002 merge, S-003 V2, C-001 to C-004 merge, C-005 V2 (P3), C-006 merge (V3 lead), C-007 merge, C-008 merge, X-001 V2 (P1), X-002 V3 (drift), A-001 qualify, A-002 qualify, A-003 accept.

Orchestrator evidence E-1: the `--diagnosability-handoff` packaging via `sc:workflow-protocol` is confirmed at `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md:245`.

## Round 2.5: Invariant Probe - `invariant-probe.md`

21 invariants probed: 10 ADDRESSED, 11 UNADDRESSED.

| ID | Severity | Status | Summary |
|---|---|---|---|
| INV-001 | HIGH | UNADDRESSED | cli-eval safety-flag subset is undefined, so the P1 block cannot be tested |
| INV-002 | HIGH | UNADDRESSED | nested blocked/failed status has no propagation (sc-task Step 4 has no blocked branch; tasklist Stage 9 gates only on completion) |
| INV-003 | MEDIUM | UNADDRESSED | diagnosability handoff step 3 reads `.dev/tasks/to-do/<id>/return-contract.yaml`; a nested workflow writes elsewhere |
| INV-004 | MEDIUM | UNADDRESSED | `UNATTENDED_EXPECT` nested lists in Tasks 8, 11, 16 must equal the Task 20 literal |
| INV-009 | MEDIUM | UNADDRESSED | nested task needs `--report-dir` plus retained `--compliance strict`; no AC pins it |
| INV-011 | MEDIUM | UNADDRESSED | cli-eval spec-panel/document are command-only; the technical-writer agent route yields no nested dir |
| INV-016 | MEDIUM | UNADDRESSED | Task 12 `report_path` undefined for a non-TFEP run |
| INV-017 | MEDIUM | UNADDRESSED | the C-002 fix must widen the exemption or scope the clause check |
| INV-018 | MEDIUM | UNADDRESSED | task-builder CLI gate: whole-run vs staging-only undecided |
| INV-005 | LOW | UNADDRESSED | empty nested list means the `nested/` token is forbidden in skip wording |
| INV-010 | LOW | UNADDRESSED | `--unattended` placement inside a quoted string |

## Taxonomy Coverage

| Level | Points | Count |
|---|---|---|
| L1 (surface: form, wording, single-claim accuracy) | S-003, C-006, C-007, C-008, X-002 | 5 |
| L2 (structural: plan/test/check consistency) | S-001, S-002, C-002, C-003, C-004, C-005, A-002 | 7 |
| L3 (contract/semantic: worker-contract guarantees) | C-001, X-001, A-001, A-003 | 4 |

Coverage check: every level has at least one point. PASS.

## Scoring Matrix

Rows come from the Round 2 final positions. Confidence rules: unanimous 90-100, majority 60-89, split 50; 100 only where every advocate conceded.

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 sections | L2 | merge (V3 sections, `verified_ok` bounded) | 90 | V2 and V3 say merge, V1 says V3; same outcome: V3 structure with bounded per-check claims (round2-advocate-3 s1) |
| S-002 finding counts | L2 | merge (V3 spine) | 95 | All three: V3 spine plus V1/V2 unique findings, conceded items dropped |
| S-003 evidence form | L1 | V2 | 95 | Unanimous: repo-relative file:line evidence |
| C-001 cli-eval safety block | L3 | merge (V2 finding, P1) | 90 | Unanimous merge; remedy form (name flags vs owner policy) left to INV-001 |
| C-002 workflow.md:72 stale clause | L2 | merge (V3 spine + V1 return-contract.md) | 90 | Unanimous merge; fix must reach the line `_artifacts_clause` reads (test:770-775); pin claim of R3-F3 conceded |
| C-003 "left out (WC-4)" scope | L2 | merge (V2 scope + V3 test shape) | 95 | Unanimous; only plan:97 and plan:110 pin the phrase |
| C-004 gate phrase label vs resolution | L2 | merge (V2 negatives + V1 inventory) | 95 | Unanimous |
| C-005 Task 21 path list | L2 | V2 (P3) | 95 | Unanimous; V3 dirty-folder example dropped (plan:372) |
| C-006 D-P2-1 research arms | L1 | merge (V3 lead) | 90 | V1 says V3, V2 and V3 say merge with V3 lead |
| C-007 instruction/check collisions | L1 | merge | 95 | Unanimous (Task 12 vs ADDITIVE/WRITEVERB; Task 17 vs one-line budget) |
| C-008 deviation classification | L1 | merge (four classes per finding) | 95 | Unanimous; every advocate conceded its uniform or off-taxonomy labels |
| X-001 cli-eval severity | L3 | V2 (P1) | 100 | Every advocate conceded P1 (V3 from P2, V1 from its broader framing) |
| X-002 workflow class | L1 | V3 (drift) | 95 | Unanimous; one-line cap is the plan's own choice |
| A-001 safety flags nameable | L3 | merge (assumption QUALIFIED) | 90 | Unanimous qualify; flags nameable from `sc-cli-eval-protocol/SKILL.md:128-153`, digest authoritative |
| A-002 one-line cap | L2 | merge (assumption QUALIFIED) | 90 | Unanimous qualify; cap is plan:41, not spec |
| A-003 nested rule covers unlisted calls | L3 | V3 (ACCEPTED as STATED) | 95 | Unanimous accept; spec:60 and spec:62 |

Direct variant wins: V2 3 (S-003, C-005, X-001), V3 2 (X-002, A-003), V1 0. Merges: 11, of which V3 leads S-001, S-002, C-002 and C-006.

## Convergence Assessment

- Points resolved: 16 of 16
- Alignment: 100%
- Threshold: 80%
- Debate convergence: MET
- Invariant gate: 2 HIGH UNADDRESSED rows
- **Status: BLOCKED_BY_INVARIANTS** (blocking: INV-001, INV-002)
- MEDIUM warnings: INV-003, INV-004, INV-009, INV-011, INV-016, INV-017, INV-018
- LOW notes: INV-005, INV-010
- Unresolved points: none at the winner level.

Residual remedy-level choices (owner decisions, not unresolved points):

1. C-001 / A-001 / INV-001: name the cli-eval safety-flag subset in the plan, or carry the cli-eval section as blocked-pending-decision.
2. C-002 / INV-017: widen the ADDITIVE exemption to two lines for workflow.md, or scope `_artifacts_clause` to the correct line.
3. New finding (troubleshoot `--diagnosability-handoff`) / INV-003: nest `workflow` and change the return-contract path, or refuse the flag under `--unattended`.
