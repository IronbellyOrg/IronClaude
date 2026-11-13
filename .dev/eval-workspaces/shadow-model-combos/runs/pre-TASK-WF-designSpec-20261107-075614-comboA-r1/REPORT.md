# Reflect REPORT — pre-TASK-WF-designSpec-20261107-075614-comboA-r1

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.75
citations_total: 49
citations_revalidated: 26
citations_dropped: 1
citations_inferred: 1
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 26` — size of the re-Read sample (100% of MAJOR-finding citations + 40% of MINOR-finding citations).
> - `citations_dropped: 1` — drops observed in the sample only. This gates status (§11.2: ≥1 dropped → partial).
> - `citations_dropped_extrapolated: 2` — population-level estimate, `round(1 × (49 / 26))`. Recording-only; does not gate.
>
> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined.

## Summary

**WHAT:** This UC-1 pre-execution audit of the frozen spec↔plan pair for the `/sc:pr-submit` merge guard (issue #375) found **2 blocking MAJOR defects** and 16 further minor defects in the plan. Verdict: **plan is not ready to execute as written.** The run reached Tier 2 (pinned via `--tier 2`), with shadow-engine panel measurement; three heterogeneous reviewers (sonnet/analyzer, haiku/qa, opus/refactorer) produced 24 findings, merged adversarially (convergence 0.917, base opus:refactorer) into 18.

**WHY partial:** The evidence validator dropped 1 unfounded citation (MF1's `spec:210` — that line pairs requests by `idempotency_key` but does not support the event-field-instruction claim; the finding survives on its other citations). Per §11.2, ≥1 dropped citation forces `status: partial`. This is a citation defect, not a finding rejection — no finding was dropped.

**Coverage:** parsed-sparse (0 Pass-1 IDs; the spec labels requirements FR-1..FR-23 in an external merged-requirements doc, not inline). Pass-2 inference produced 15 quote-pinned rows; all 15 matched a task → `coverage_pct_union: 1.0`. The Tier-1 stop was correctly forbidden; Tier 2 was pinned regardless.

**Attribution note:** This is a pre-execution audit. The spec's facts are pinned at base commit e8db2fe6; the feature has since landed at HEAD (commit 0b8a5801d). No finding rests on HEAD source text — the plan was audited against the frozen spec only, per the binding attribution rule in each reviewer brief.

## Blocking findings

### MF1 (MAJOR, blocking, missing-requirement) — Task 8 drops the event-field construction from the protocol ref
- **Location:** plan:124-130 (Task 8); spec:182-185, spec:240
- **Mapped requirement:** FR-7, FR-21 (INF-008)
- **Evidence:** spec:182-185 defines the `draft_guard_requested`/`draft_guard_settled` event fields including `idempotency_key = guard:<run_id>:<cycle_id>:<to>:a<k>`; spec:240 says the ref `refs/merge-guard.md` carries "the procedure of sections 3 and 4.1 to 4.4"; plan:124 narrows Task 8's inputs to "sections 3, 4.1, 4.5, 4.6 and 5", dropping 4.2-4.4, so the protocol ref never states the event-field construction, and no AC gates it. The scenario driver in Task 11 writes its own events (plan:166), so nothing exercises the ref's event instructions.
- **Classification rationale:** A plan executor following Task 8 as written ships a protocol ref that omits the idempotency-key format — a load-bearing crash-recovery contract. This is a missing-requirement defect, blocking because the omission is silent (no AC catches it).
- **Calibrated confidence:** 0.75
- **Default remediation:** Add section 4.2 (event fields) to Task 8's ref scope and add an AC that the ref states the `idempotency_key` format and the `k` increment rule; cite spec:182-185.
- **Note:** The evidence validator dropped the `spec:210` citation from this finding's original claim (that line covers the `pending_requests` matcher, not the event-field instructions). The finding survives on `spec:182-185` + `plan:124-130` + `spec:240`.

### MF2 (MAJOR, blocking, unpassable-check) — Task 11's ACs gate test names, not the behaviours they must assert
- **Location:** plan:166-173 (Task 11), specifically AC at plan:169; spec:307-320, spec:315-318
- **Mapped requirement:** FR-7, FR-16, FR-21, FR-22 (INF-009, INF-014)
- **Evidence:** plan:169 requires the test file to *define* twelve named tests; the ACs gate the trace order, crash-window construction via the real `detect_crash_window`/`resolve_crash_window`, and forbidden calls — but not FR-16's release-failure behaviours (one retry, `already_in_state` counts as confirmed, `release_pending` reported), crash before/after each request and settle, short timeline, or moved head. spec:315-318 maps those behaviours to named tests, but no plan AC asserts the behaviours, so tests with empty bodies pass.
- **Classification rationale:** An unpassable-check defect: the AC is satisfied by defining names without asserting the mapped behaviour. Blocking because an executor can ship twelve stub tests and pass every AC.
- **Calibrated confidence:** 0.80
- **Default remediation:** Add per-behaviour ACs to Task 11 for FR-16 (retry-once, already-in-state, release_pending), the crash-boundary matrix, short-timeline hold, and moved-head halt; each AC must name the assertion, not the test name.

## Non-blocking findings (MAJOR/MINOR)

### MF3 (MAJOR, contradiction) — Tasks 9/10/12/13 read Task 1's output without declaring the dependency
- **Location:** plan:134-137, plan:148, plan:154, plan:179-182, plan:190-195; spec:363
- **Evidence:** spec:363 requires "a task depends on every earlier task whose output it imports or consumes (... the protocol tasks need the pre-build record)". Tasks 9, 10, 12, 13 all read `./artifacts/pre-build-gate.md` (Task 1's output) but none declares `Depends on: Task 1`; the order holds only transitively via Task 8. Refutes T1 hypothesis H3.
- **Remediation:** Add `Depends on: Task 1` to Tasks 9, 10, 12, 13. Confidence 0.80.

### MF4 (MINOR, unpassable-check) — Wave 0 bullet AC fails the real bullet read literally
- **Location:** plan:137, plan:140; spec:241
- **Evidence:** plan:137 requires the Wave 0 bullet to say "at L3 with `--merge-guard off` ... no draft call is made"; plan:140's AC fails the bullet when it "names an L3 or `draft` condition". Only the body's "gate wording" qualifier makes it passable; read literally the real bullet fails its own AC. Same tension in spec:241.
- **Remediation:** Reword the AC to "names an L3-only or draft-only *load* gate" (distinguishing the load clause from the print clause). Confidence 0.65.

### MF5 (MINOR, missing-requirement) — corrupt-line still-raises invariant ungated
- **Location:** spec:208; plan:85-90 (Task 5 ACs)
- **Evidence:** spec:208 states "A corrupt line still raises, as it does today"; Task 5's ACs cover only legacy and well-formed guard logs and name no existing test that pins the raise.
- **Remediation:** Add an AC to Task 5 that `rebuild_state()` raises on a corrupt line after the `draft_guard` fold is added, or name the existing test that pins it. Confidence 0.72.

### MF6 (MINOR, missing-requirement) — engage row 11 auto_merge_armed note ungated
- **Location:** spec:143; plan:73
- **Evidence:** spec:143 (engage row 11) requires `notes` to carry `auto_merge_armed` when set; Task 4's ACs assert only action, reason, cause per row.
- **Remediation:** Add an AC asserting `notes` carries `auto_merge_armed` on the ENGAGE row when the read reports it armed. Confidence 0.65.

### MF7 (MINOR, contradiction) — byte-pin uses start-text only
- **Location:** spec:377; plan:38; plan:150-154
- **Evidence:** Task 10 claims the S5a and Wave 6 pre-push sentences are "asserted byte-identical by comparing the live text with string constants", but Task 1 records only their "literal start text"; a prefix comparison cannot detect an edit later in the sentence.
- **Remediation:** Record the full pinned sentence (not just its start) in Task 1, and assert full-string equality in Task 10. Confidence 0.75.

### MF8 (MINOR, missing-requirement) — halt message content ungated
- **Location:** spec:274; plan:129
- **Evidence:** spec:274's engage-failure trace requires the halt message to name `--merge-guard off` and print the clear command; Task 8/11 ACs gate only the `draft_guard_unavailable` reason and the halt.
- **Remediation:** Add an AC asserting the halt message text. Confidence 0.75.

### MF9 (MINOR, contradiction) — clear command literal form differs across tasks
- **Location:** plan:124, plan:185, plan:195; spec:247
- **Evidence:** Task 8 writes `gh pr ready <N> --repo "$REPO"`; Task 13 and spec:247 write `gh pr ready <N> --repo <REPO>`; Task 12's AC demands "the exact clear command" without naming the form. Tests written per task can disagree on the literal text. (Judge note: both forms are fit for their context — shell variable in the ref, placeholder in docs — the actionable part is naming the form in Task 12's AC.)
- **Remediation:** Task 12's AC should name which literal form is asserted, or accept both with an explicit note. Confidence 0.80.

### MF10 (MINOR, contradiction) — cycle-id minting written into two places
- **Location:** spec:251; plan:124, plan:127, plan:150
- **Evidence:** spec:251 requires "exactly one source" for the cycle id (open item O1). Task 10's Wave 3 bullet "mints the cycle id" while Task 8 puts minting in "the single place named by Task 1 O1"; no AC ties the Wave 3 bullet to the O1 place.
- **Remediation:** Add an AC that the Wave 3 bullet's minting references the same single place O1 names. Confidence 0.60.

### MF11 (MINOR, missing-requirement) — user_override fold sets no disabled_cause
- **Location:** spec:206, spec:112; plan:60-61
- **Evidence:** spec:206's fold row `settled(any, skipped, user_override)` sets phase DISABLED and `owned_draft=False` but no `disabled_cause`; spec:112's guard_status needs cause `user_override` to report `user_override`. Task 3's fold cases omit the row and guard_status is tested on a hand-built guard, so the two can disagree. (Inherited spec gap.)
- **Remediation:** Make the fold row set `disabled_cause = user_override`, and add a Task 3 AC for it. Confidence 0.70.

### MF12 (MINOR, missing-requirement) — RELEASE_PENDING not_applied fold case untested
- **Location:** spec:201, spec:366; plan:60
- **Evidence:** spec:201 says a ready request settled `not_applied` after a failed release returns to RELEASE_PENDING; Task 3's AC names only the HELD case, so a fold that hard-codes HELD for ready requests passes.
- **Remediation:** Add a Task 3 AC for the RELEASE_PENDING not_applied case. Confidence 0.75.

### MF13 (MINOR, missing-requirement) — draft_guard_unavailable halt→unavailable mapping has no owner
- **Location:** spec:112; plan:61
- **Evidence:** spec:112 says "A halt with reason `draft_guard_unavailable` reports `unavailable`", but `guard_status(guard, mode, ordinal)` cannot see a halt and no Task 3 or 8 AC maps it. An engage halt at row 3 or row 8 writes no guard record, so guard_status reports `released`, not `unavailable`.
- **Remediation:** State where the halt→unavailable mapping lives (SKILL report logic, not the pure core) and add an AC. Confidence 0.75.

### MF14 (MINOR, missing-requirement) — O2 front-matter script grant has no owning task
- **Location:** spec:340; plan:108, plan:137, plan:142
- **Evidence:** spec:340 (O2) asks how scripts are granted in the SKILL front matter; no task explicitly adds a grant there. Task 7 adds the script to test lists and to "any script list O2 shows is required"; Task 9's SKILL.md edit list omits the front matter. If a grant is needed, Task 9's `test_conflict_sync_protocol` run fails loudly. (Downgraded from MAJOR: the failure is loud, not silent.)
- **Remediation:** Add the SKILL front-matter script grant to Task 9's edit list, conditional on the O2 finding. Confidence 0.60.

### MF15 (MINOR, contradiction) — two new test files absent from the spec files-to-change table
- **Location:** spec:297; plan:124, plan:166
- **Evidence:** spec:297 lists `test_merge_guard.py` and `test_set_draft_state.py` as the new test files; Task 8 creates `test_merge_guard_protocol.py` and Task 11 creates `test_merge_guard_scenarios.py`, neither in the table. The plan does not record the deviation.
- **Remediation:** Note the test-file deviation in the plan (a Necessary deviation per §10.2), or add the two files to the spec table. Confidence 0.80.

### MF16 (MINOR, contradiction) — 12th named test narrowed vs its spec mapping
- **Location:** spec:320; plan:169, plan:112
- **Evidence:** spec:320 maps exit codes 0/1/2/127, `--repo` on every call, and the legacy fold to `test_guard_script_contract_scoping_and_legacy_fold`; Task 11 narrows it to the legacy fold and scoping, testing exit codes only in Task 7's file. Coverage exists but the named mapping diverges.
- **Remediation:** Either keep exit-code assertions in the named test or document the relocation. Confidence 0.65.

### MF17 (MINOR, other) — unordered tasks edit shared files
- **Location:** plan:85, plan:106-108, plan:134-137, plan:179-182
- **Evidence:** Tasks 5 and 7 both edit `test_static_grep.py` (CORE_PURE_FILES and `_RESOLUTION_SCRIPTS`); Tasks 9 and 12 (each depending only on Tasks 6 and 8) both extend `test_merge_guard_protocol.py` and may both add WRITE_VERB_CLASSIFICATION entries. Parallel execution risks conflicting edits.
- **Remediation:** Add an ordering note or serialize Tasks 5/7 and 9/12. Confidence 0.60.

### MF18 (MINOR, unpassable-check) — Task 2 grep-43 AC has no mechanical pass condition
- **Location:** plan:49
- **Evidence:** Task 2's third AC (`grep -rn "43" ...` "shows no remaining claim that the enum has 43 members") is a manual reading of a bare grep; "43" can match unrelated text and there is no mechanical pass condition.
- **Remediation:** Replace with a positive assertion (e.g., grep for `exactly 43 members` / `The 43 event types` returns zero hits) and an assertion that `45` appears. Confidence 0.55.

## Rejected findings

| Source | Claim | Reason |
|---|---|---|
| R3-F3 | Task 13's `Depends on: Task 2` is a no-op superset (confirms T1 H2) | Not a defect. spec:363 asks for complete declaration and does not forbid redundancy; Task 13's full-suite run consumes Task 2's test changes. An explicit edge is consistent with the rule. |

Superseded orchestrator hypothesis: T1 card H3 ("every consumer declares its producers") is refuted by MF3.

## Inferred requirements (Pass 2)

15 quote-pinned inferred rows (INF-001..INF-015), all matched to tasks; 3 sampled (INF-006 source.md:353, INF-010 source.md:255, INF-013 source.md:326-341) by the evidence validator — all quotes matched their cited lines, 0 dropped. Full matrix: artifacts/coverage-matrix.yaml.

## Inferred-claim audit

- `citations_inferred: 1` (T1 hypothesis H2 "superset dependency" was tagged `[INFERRED]`; it was rejected at merge, so it does not enter a finding).
- Inferred-fraction: `1 / 49` = 0.02.

## Recommendations

### R-001: Gate Task 11's behaviours, not its test names (P0)
- **File:** plan (Task 11 ACs, plan:169-173)
- **Change:** Add per-behaviour ACs for FR-16 (retry-once, already-in-state-as-confirmed, release_pending), the crash-boundary matrix (before/after each request and settle), short-timeline hold, and moved-head halt; each AC names the assertion, not the test name.
- **Verifier:** A stub test with an empty body fails the new ACs; re-Read Task 11 AC list confirms each behaviour is asserted.
- **Linked:** MF2
- **Priority:** P0

### R-002: Restore section 4.2 to Task 8's ref scope (P0)
- **File:** plan (Task 8, plan:124)
- **Change:** Add spec section 4.2 (event fields) to Task 8's protocol-ref inputs and add an AC that the ref states the `idempotency_key` format (`guard:<run_id>:<cycle_id>:<to>:a<k>`) and the `k` increment rule.
- **Verifier:** Re-Read Task 8 scope line confirms 4.2 is listed; AC asserts the key format text.
- **Linked:** MF1
- **Priority:** P0

### R-003: Declare the Task 1 dependency on Tasks 9/10/12/13 (P1)
- **File:** plan (Tasks 9, 10, 12, 13)
- **Change:** Add `Depends on: Task 1` to each of the four tasks that read `./artifacts/pre-build-gate.md`.
- **Verifier:** Each task's Depends-on block lists Task 1.
- **Linked:** MF3
- **Priority:** P1

### R-004: Tighten the pass-gate and literal-form ACs (P1)
- **File:** plan (Tasks 2, 8, 9, 10, 12)
- **Change:** MF4 (reword Wave 0 AC to distinguish load gate from print clause), MF7 (record full pinned sentence, assert full equality), MF9 (name the clear-command form in Task 12's AC), MF18 (replace grep-43 with a positive assertion).
- **Verifier:** Each reworded AC is mechanically falsifiable; re-Read confirms the literal text is named.
- **Linked:** MF4, MF7, MF9, MF18
- **Priority:** P1

### R-005: Close the fold/guard_status wiring and missing-AC gaps (P2)
- **File:** plan (Tasks 3, 4, 5) + spec (sections 4.1, 4.2)
- **Change:** MF5 (corrupt-line raise AC), MF6 (auto_merge_armed note AC), MF11 (user_override sets disabled_cause), MF12 (RELEASE_PENDING not_applied AC), MF13 (halt→unavailable mapping owner).
- **Verifier:** Each named behaviour has a Task AC that fails on a wrong implementation.
- **Linked:** MF5, MF6, MF11, MF12, MF13
- **Priority:** P2

### R-006: Record the test-file deviation and sequencing (P2)
- **File:** plan (Tasks 5, 7, 8, 9, 11, 12)
- **Change:** MF14 (add front-matter grant to Task 9 conditional on O2), MF15 (record the two extra test files as a Necessary deviation), MF16 (keep or document the exit-code relocation), MF17 (serialize Tasks 5/7 and 9/12).
- **Verifier:** Plan records each deviation; dependency notes prevent parallel-edit conflicts.
- **Linked:** MF14, MF15, MF16, MF17
- **Priority:** P2

## Shadow-panel telemetry (measurement only; legacy rotation authoritative)

- t2_engine: shadow (requested + effective). panel_parity: true (panel resolve = legacy rotation: sonnet/haiku/opus).
- Reviewers: t1b-1 (sonnet/analyzer), t4-1 (haiku/qa), t1a-1 (opus/refactorer). findings_block_compliance: 2/3 first-parse valid, 3/3 after 1 bounded re-ask (reviewer-3 F6/F10 claims >300 chars).
- Calibrated findings: 24/24. cluster_agreement: 0.31 (telemetry only). calibration_coverage: 24/24.
- identity_source: requested-pinned. identity_mismatch_suspected: true (reviewer-2 haiku pin self-reported "OpenAI GPT"; 4th sighting in this workspace — no verified-independence claim).
- judge_identity: "opus (claude-gw-tier3 orchestrator session)". judge_class_collision: unknown (sc-adversarial contract names no separate judge record).
- debate_skipped_similar: false. Manifest stages advanced in order: resolved→dispatched→collected→calibrated→clustered→debated→validated.
- verify-citations pre-check: 62 checked / 62 flagged missing-file (expected — input snapshot is package-only; repo-file citations are not in it; all join the EV re-read set, none dropped by the validator for that reason).

## Grounding Gaps

No grounding gaps. The single dropped citation (MF1's `spec:210`) is recorded in the MF1 note above; the finding survived on its other citations, so no §10.6 gap row applies. `needs_human_decision: false`.
