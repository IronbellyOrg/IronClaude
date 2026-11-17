# Merged verdict: reflect-pre panel, TASK-WF-designSpec-20261107-075614 (comboA-r1)

- Mode A, depth standard. Base variant: V3 (opus:refactorer). Convergence 0.917 (11 of 12 diff points). Unresolved conflicts: 0.
- Source cards: reviewer-1 (sonnet:analyzer, R1), reviewer-2 (haiku:qa, R2), reviewer-3 (opus:refactorer, R3).
- Confidence: the panel calibration of the source finding (panel/cards/reviewer-N.md); where several reviewers filed the same defect, the highest is kept.
- Blocking rule: a finding is blocking when a plan executor following the plan as written would ship a wrong or unverified artifact.

Citation legend (frozen inputs only):
- `plan:N` = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`
- `spec:N` = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`

## Verdict summary

| | Count |
|---|---|
| Merged findings | 18 |
| CRITICAL | 0 |
| MAJOR | 3 (2 blocking) |
| MINOR | 15 |
| Rejected source findings | 1 |

Plan readiness: **not ready**. MF1 and MF2 are blocking.

## Accepted findings

| ID | Severity | Blocking | Category | Claim | Conf | Citations | Sources |
|---|---|---|---|---|---|---|---|
| MF1 | MAJOR | true | missing-requirement | Task 8 builds the ref from spec sections 3, 4.1, 4.5, 4.6 and 5 and drops 4.2, so the protocol never states the event fields: `idempotency_key` `guard:<run_id>:<cycle_id>:<to>:a<k>`, `k` per cycle and direction, first-request baseline. No AC gates them, and the scenario driver writes its own events. | 0.75 | spec:182-185; spec:210; plan:124-130 | R2-F1 |
| MF2 | MAJOR | true | unpassable-check | Task 11's ACs gate the twelve test names, the trace order, crash-window construction and forbidden calls, but not FR-16 (one release retry, already-in-state as confirmed, release_pending report), crash before/after each request and settle, short timeline or moved head. Empty bodies pass. | 0.80 | plan:169; plan:166-173; spec:307-320; spec:315-318 | R1-F1; R2-F2 |
| MF3 | MAJOR | false | contradiction | Tasks 9, 10, 12 and 13 read `./artifacts/pre-build-gate.md` (Task 1's output) but none declares `Depends on: Task 1`; the order holds only through Task 8. This breaks the spec's complete-dependency rule, which names this exact case, and refutes T1 hypothesis H3. | 0.80 | spec:363; plan:134-137; plan:148; plan:154; plan:179-182; plan:190-195 | R3-F2 (supersedes T1 H3) |
| MF4 | MINOR | false | unpassable-check | Task 9 requires the Wave 0 bullet to say "at L3 with --merge-guard off ... no draft call is made", yet its AC fails the bullet when it "names an L3 or draft condition". Only the body's "gate wording" qualifier makes it passable; read literally, the AC fails the real bullet. Same tension in the spec. | 0.65 | plan:137; plan:140; spec:241 | R1-F2; R3-F1 |
| MF5 | MINOR | false | missing-requirement | The spec says a corrupt run-log line still raises after the `draft_guard` fold is added, but no AC gates it: Task 5's ACs cover only legacy and well-formed guard logs and name no existing test that pins the raise. | 0.72 | spec:208; plan:85-90 | R1-F6 (part); R2-F4; R3-F9 |
| MF6 | MINOR | false | missing-requirement | Engage row 11 must carry `auto_merge_armed` in `notes`, but Task 4's ACs assert only action, reason and cause per row, so a decision that drops the note passes. | 0.65 | spec:143; plan:73 | R1-F6 (part) |
| MF7 | MINOR | false | contradiction | Task 10 says the S5a and Wave 6 pre-push sentences are proven byte-identical, but Task 1 records only their literal start text; a prefix comparison cannot detect an edit later in the sentence. | 0.75 | spec:377; plan:38; plan:150-154 | R2-F3; R3-F5 |
| MF8 | MINOR | false | missing-requirement | The spec's engage-failure trace requires the halt message to name `--merge-guard off` and print the clear command; Task 8 and Task 11 ACs gate only the `draft_guard_unavailable` reason and the halt, not the message content. | 0.75 | spec:274; plan:129 | R1-F5 |
| MF9 | MINOR | false | contradiction | The clear command is written `--repo "$REPO"` in Task 8 and `--repo <REPO>` in Task 13 and the spec, and Task 12's AC demands "the exact clear command" without naming the form, so tests written per task can disagree on the literal text. | 0.80 | plan:124; plan:185; plan:195; spec:247 | R3-F8 |
| MF10 | MINOR | false | contradiction | Task 10's Wave 3 bullet "mints the cycle id", while Task 8 puts minting in the single place Task 1 O1 names. No AC ties the Wave 3 bullet to the O1 place, so the spec's exactly-one-source rule can break. | 0.60 | spec:251; plan:124; plan:127; plan:150 | R1-F8; R3-F12 |
| MF11 | MINOR | false | missing-requirement | Fold row `settled(any, skipped, user_override)` sets phase DISABLED but no `disabled_cause`, while guard_status needs cause `user_override` to report `user_override`. Task 3's fold cases omit the row and guard_status is tested on a hand-built guard, so the two can disagree. Inherited spec gap. | 0.70 | spec:206; spec:112; plan:60-61 | R1-F3 |
| MF12 | MINOR | false | missing-requirement | A ready request settled `not_applied` after a failed release must return to RELEASE_PENDING. Task 3's AC names only the HELD case plus a generic restore check with no stated direction, so a fold that hard-codes HELD for ready requests can pass. | 0.75 | spec:201; spec:366; plan:60 | R3-F11 (narrowed) |
| MF13 | MINOR | false | missing-requirement | No task owns the rule that a `draft_guard_unavailable` halt reports `unavailable`: guard_status(guard, mode, ordinal) cannot see a halt and no Task 3 or 8 AC maps it. An engage halt at row 3 or row 8 writes no guard record, so guard_status reports `released`. | 0.75 | spec:112; plan:61 | R1-F4 |
| MF14 | MINOR | false | missing-requirement | O2 asks how scripts are granted in the SKILL front matter, but no task explicitly adds a grant: Task 7 adds the script to test lists and to "any script list O2 shows is required", and Task 9's SKILL.md edit list omits the front matter. If a grant is needed, Task 9's test run fails loudly. | 0.60 | spec:340; plan:108; plan:137; plan:142 | R3-F4 (downgraded from MAJOR) |
| MF15 | MINOR | false | contradiction | Task 8 creates `test_merge_guard_protocol.py` and Task 11 creates `test_merge_guard_scenarios.py`; neither is in the spec's files-to-change table, which puts the section 7 tests in `test_merge_guard.py` and `test_set_draft_state.py`. The plan does not record the deviation. | 0.80 | spec:297; plan:124; plan:166 | R3-F6 |
| MF16 | MINOR | false | contradiction | The spec maps exit codes 0/1/2/127, `--repo` on every call and the legacy fold to `test_guard_script_contract_scoping_and_legacy_fold`; Task 11 narrows it to the legacy fold and scoping, and tests exit codes only in Task 7's file. Coverage exists, but the named mapping diverges. | 0.65 | spec:320; plan:169; plan:112 | R3-F7 |
| MF17 | MINOR | false | other | Unordered tasks edit shared files: Tasks 5 and 7 both edit `test_static_grep.py`, and Tasks 9 and 12 (each depending only on Tasks 6 and 8) both extend `test_merge_guard_protocol.py`. Parallel execution risks conflicting edits. | 0.60 | plan:85; plan:106-108; plan:134-137; plan:179-182 | R3-F10 |
| MF18 | MINOR | false | unpassable-check | Task 2's third AC (`grep -rn "43" ...` "shows no remaining claim that the enum has 43 members") needs a manual reading of the grep output; it has no mechanical pass condition and "43" can match unrelated text. | 0.55 | plan:49 | R1-F7 |

## Rejected findings

| Source | Claim (short) | Reason |
|---|---|---|
| R3-F3 | Task 13's `Depends on: Task 2` is a no-op superset (confirms T1 H2) | Not a defect. spec:363 asks for complete declaration and does not forbid redundancy, and Task 13's full-suite run (plan:195) consumes Task 2's test changes (plan:44). An explicit edge is consistent with the rule. |

Superseded orchestrator hypothesis (not a reviewer finding): T1 card H3 ("every consumer declares its producers") is refuted by MF3.

## Judge notes

- MF1 is blocking. spec:240 states the ref carries "sections 3 and 4.1 to 4.4", but the plan narrows that to 3, 4.1, 4.5, 4.6 and 5 (plan:124). The Task 11 scenario driver builds its own events (plan:166), so no test exercises the ref's event-field instructions.
- MF2 is blocking. This was decided by applying the rule (X-002, 65%): no AC anywhere in Tasks 3 to 11 fails on an empty FR-16 retry-once test.
- MF9's two forms are each fit for their context: a shell variable in the protocol ref and a placeholder in the docs. The actionable part is to name the form in Task 12's AC.
