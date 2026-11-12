# Refactoring Plan: Merge into Base (Variant 1)

## Overview
- Base: Variant 1 (opus:architect), `variant-1-opus-architect.md`, combined score 0.913 (V2 0.865, V3 0.787). The lead over V2 is under 5%, so the debate-point tiebreak decided it. The selection was forced by score because the gate status is BLOCKED_BY_INVARIANTS (INV-005 is an accepted risk awaiting owner sign-off).
- Incorporating strengths from: Variant 2 (opus:analyzer, `variant-2-opus-analyzer.md`) and Variant 3 (haiku:backend, `variant-3-haiku-backend.md`), plus the Round 3 final texts in `debate/round3-final-v1.md` (V1R3), `debate/round3-final-v2.md` (V2R3) and `debate/round3-final-v3.md` (V3R3).
- Planned changes: 42 (of which 10 are base-weakness fixes, tagged W-1 to W-10 in their titles)
- Risk level: Medium (overall). One change (Change 3, INV-001) is High.

Citation key used in this plan. `V1:148` is line 148 of variant 1, and likewise `V2:` and `V3:`. `V1R3:22` is line 22 of `debate/round3-final-v1.md`, and likewise `V2R3:` and `V3R3:`. `Conv:` is `convergence-tracking.md`, `Diff:` is `diff-analysis.md`, `BS:` is `base-selection.md`, `Probe:` is `invariant-probe.md`, all in this directory (`/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/adversarial/adversarial/`). Point IDs (S, C, X, A, U, INV) refer to `diff-analysis.md` and `invariant-probe.md`. Winner and confidence come from the scoring matrix in `debate-transcript.md` and from Conv P3.2 to P3.4. "M V1+V3" means a named merge of those variants.

Instructions to the merge-executor:
1. Start from V1 unchanged. Apply the changes below in order. Where two changes touch the same V1 line, the later change works on the text the earlier change left.
2. Quoted final texts are copied exactly, except that the seed path is corrected (Change 2) and the binary wording is corrected (Change 9).
3. Do not copy any text this plan lists under "Changes NOT Being Made".
4. Do not add em dashes. Keep plain English.

## Planned Changes

### Change 1: Provenance convention for every merged section (from all variants)
- **Source**: This plan (orchestrator process requirement); applies to text from V1, V2, V3 and V1R3, V2R3, V3R3.
- **Target**: Base, every top-level section and the header block (insert)
- **Rationale**: The task requires each merged section to name its source variants, and the merge-log must be traceable to the scoring matrix.
- **Integration point**: (a) Directly under each numbered section heading, insert one line `Provenance: V1` or, for example, `Provenance: V1 + V3 (C-019, C-020)`, naming every variant whose text the section now contains and the point IDs that brought it in. (b) Each requirement row, table row or sentence whose text changed carries an inline tag in square brackets at its end, for example `[V3:303; C-038]` or `[V3R3:31; INV-001]`. Unchanged V1 text carries no inline tag. (c) Add one line to the header block: "Provenance tags name the variant line or Round 3 line each changed text came from. V1 = architect, V2 = analyzer, V3 = backend." (d) New sections created by this plan (Accepted risks, Open warnings, CLI contract) carry the same `Provenance:` line.
- **Risk**: Low. Annotation only; no requirement text changes.

### Change 2: Correct every seed-brief reference (reviewer correction)
- **Source**: Conv P3.7 item 1 (Conv:324); task instruction.
- **Target**: Base, header block V1:12 and section 1 V1:16-20, plus any `Seed:` or `../../seed-brief.md` reference carried in from V1R3, V2R3 or V3R3 (replace)
- **Rationale**: V1R3:6, V2R3:6 and V3R3:27 cite `../../seed-brief.md`, which resolves to a file that does not exist. The real seed is at the brainstorm root.
- **Integration point**: Replace the bare `seed-brief.md` at V1:12 and every relative seed path with the absolute path `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/seed-brief.md`. Line numbers into the seed (for example "seed brief line 27" at V1:88) are unchanged. Never write `../../seed-brief.md` in the merged spec.
- **Risk**: Low. Path text only.

### Change 3: Run binding, Orca-down behaviour and exit codes (INV-001, X-001, C-015, C-016; base weakness W-1, from Variant 3 with V1R3 and V2R3 parts)
- **Source**: V3R3:31 (final text), built from V1R3:22, V2R3:24 and V3R3:31 as Conv:272 records; V3:161-166 for the exit-0 meaning.
- **Target**: Base, section 3 FR-002 (V1:52), FR-018 (V1:68), FR-019 (V1:69); section 10 rows at V1:256, V1:257 and V1:266 (replace)
- **Rationale**: Base weakness W-1: V1 exits 0 when Orca is down with no `--run` (V1:68-69, V1:256), which contradicts the seed's "no `--run` and no `run-current` binding exits 2". Round 3 reversed X-001 and C-015 to V3 (Conv P3.2; V1R3:54 is stale per Conv:328). INV-001 is RESOLVED with all three advocates agreeing (Conv:272). C-016 went to V3 at 90%.
- **Integration point**: (a) Replace the FR-002 requirement cell and the FR-019 requirement cell with this text, verbatim from V3R3:31: "Without `--run`, call `run-current`. An unavailable lookup exits 2 with `Orca unavailable; no Run binding could be established: pass --run <id>`; a confirmed missing binding exits 2 with `no Run bound: pass --run <id>`. Neither case writes a report or success JSON. With an explicit Run, or a binding already established by a successful lookup, a later unavailable result stops further Orca reads, retains already collected evidence, marks remaining Orca sources unscanned, adds the `Orca unavailable` banner and `orca_available: false`, and permits disk-only continuation. Exit 0 requires successful report publication; write failure exits 1 without success JSON." Keep V1's "`--run` is repeatable" and "No `run-list` fallback (GQ-104)" in FR-002. FR-019 keeps V1's "discovery from `--root` fixed patterns only" for the continuation case. (b) Replace the FR-002 and FR-019 acceptance cells with three tests: no `--run` plus first-call failure (one `_orca` argv, exit 2, no report, no JSON); explicit `--run` plus first-call failure (one `_orca` argv, report published, exit 0); binding R1 established, then second-call failure (two `_orca` argv, report published, exit 0). Only the last two publish (V3R3:31). Add a fourth required test, gated on step 1.0a because the no-binding shape is UNVERIFIED (V3R3:32): a fixture of the captured no-binding `run-current` JSON with zero exit and no `--run` exits 2 with `no Run bound: pass --run <id>`, writes no report and no success JSON, and records no `worker-list` or `worker-show` argv. This keeps V1:52's test of the confirmed missing binding, the second exit-2 case of INV-001 (V3R3:31; V1R3:22). (c) Replace FR-018 with: "Exit codes: 0 means collection completed and the report was successfully published (could-not-determine rows allowed) [V3:161; C-016]; 1 internal error with `[sweep ...]` stderr prefix, including an argv outside the allowlist and any report write failure; 2 usage error, including no Run binding and Orca unavailable before a binding is established." Delete "and Orca down" from the exit-0 clause. (d) Section 10: replace the V1:256 "Orca absent ... | 0" row with two rows, "Orca unavailable before a binding: exit 2, no report" and "Orca unavailable after an explicit or established binding: banner, disk-only continuation, exit 0 after publication". Replace the V1:257 "No Run bound" row's detection "`run-current` empty and no `--run`" with "zero-exit `run-current` with the captured no-binding shape (UNVERIFIED until step 1.0a) and no `--run`", and its behaviour "Usage message (FR-002)" with "`no Run bound: pass --run <id>`, no report, no success JSON (FR-002)"; its exit stays 2. An empty `run-current` body is an invalid response, so on the first call it is `unavailable`, not a missing binding (V3R3:32; Change 4); it still exits 2 without `--run`, with the Orca-unavailable message (V3R3:31). Replace V1:266 so a write failure exits 1 and prints no success JSON.
- **Risk**: High. It changes three FR rows, three failure-mode rows and the exit-code contract that the skill, the JSON tests and Change 12 depend on; a partial edit leaves V1's exit-0 text in place and contradicts the seed.

### Change 4: Four-class Orca result classifier (INV-002, from Variant 3 with V2 parts)
- **Source**: V3R3:32 (final text), parts from V1R3:23, V2R3:25 and V3R3:32 (Conv:273).
- **Target**: Base, section 7 seam description at V1:177; section 10 rows for Orca failure; FR-019 acceptance (replace and append)
- **Rationale**: V1:177 catches `(OSError, subprocess.SubprocessError)` once and treats every failure as global unavailability. INV-002 is RESOLVED on four classes, the 2 of 3 position (Conv:273). Debate evidence: V3R3 remaining disagreements 1 and 2 (V3R3:61-62).
- **Integration point**: Replace the V1:177 sentence with this text, verbatim from V3R3:32: "Classify each `_orca` result once as `ok`, `no_binding`, `unavailable` or `call_failed`. First apply the unavailable checks: launch `OSError`, call timeout, or `runtime_unavailable` in stdout or stderr. Also treat nonzero exit or invalid response on the first Orca call as unavailable. Stop further Orca calls after unavailable. A later nonzero exit or invalid response without those unavailable signals is `call_failed`: mark that source or row unscanned, preserve its failure reason, leave dependent evidence unknown, and continue independent reads within budget. Invalid response includes empty or unparseable stdout and JSON that cannot establish the operation's captured success or no-binding shape. `no_binding` applies only to zero-exit `run-current` with the captured explicit no-binding shape, never to an empty body, arbitrary null or a missing field guessed to mean no binding. Those shapes remain UNVERIFIED until step 1.0a. `ok` requires the captured success shape. Use `orca call failed (exit <n>)` for nonzero exit and `orca call failed (invalid response)` for response failure, retaining the actual exit separately. An earlier successful call plus a later `call_failed` does not prove global runtime health; per-source failures remain visible even when `orca_available` stays true." Add the ACs: each unavailable cause on call one (parametrized, V1R3:23); a middle `worker-show` exit 1 in a 3-row Run while the other rows continue and `orca_available` stays true (V2R3:25); a later zero-exit malformed body classified `call_failed`, not `ok` or `no_binding` (V3R3:32); a fixture of the captured no-binding JSON classified `no_binding`, gated on step 1.0a (V1R3:23); an empty zero-exit `run-current` body on call one classified `unavailable`, never `no_binding` (V3R3:32). Add one sentence to section 7: "Step 1.0a capture is a precondition for the result parser, because `ok` and `no_binding` require captured shapes." (Conv:273).
- **Risk**: Medium. New seam behaviour with three tests; depends on step 1.0a shapes that are UNVERIFIED today.

### Change 5: Tri-state person-started with a completeness guard (INV-003, INV-009, A-006; base weakness W-10, from Variant 3 with V2 parts)
- **Source**: V3R3:33 (final text), parts from V1R3:24, V2R3:26 and V3R3:33 (Conv:274); V3R3:55 for INV-009.
- **Target**: Base, section 6 data model V1:136, rule 7 at V1:153, FR-010 at V1:60 (replace)
- **Rationale**: Base weakness W-10: V1's `person_started: bool` lets an unjoined transcript during an outage or after a truncated list become idle or Historical. A-006 stands with its condition amended to tri-state (Conv:256). INV-003 is RESOLVED; V1's "scanned" is replaced by V2's "complete" (V3R3:63).
- **Integration point**: (a) V1:136: change `person_started: bool` to `person_started: bool | None`. (b) Insert after FR-010's requirement, verbatim from V3R3:33: "Represent `person_started` as True, False or None. A positive transcript-to-worker join makes it False. Only when every scoped Run's worker list is complete, no relevant list or join is unscanned or truncated, and the tab map is read and the join completed may an unjoined transcript be True. Otherwise it is None. None never becomes idle or Historical; an origin-unknown transcript is could not determine, with an explicit reason such as Orca unavailable, worker list truncated, worker list call failed or tab map unreadable. Idle requires True and the existing readability and activity-window conditions." (c) V1:153 rule 7: require `person_started is True`. (d) Add the three ACs from V3R3:33: older transcript during an outage; older unjoined transcript after a full page with uncaptured continuation; incomplete list after `call_failed`. All remain visible and unknown, not Historical. Keep V1's existing FR-010 fixture as the complete-negative-join case. (e) Add the INV-009 sentence: "The C-014 full-page lower-bound note and this completeness guard apply together; counting only discovered rows does not establish a complete negative join." (V3R3:55).
- **Risk**: Medium. Changes a type, a rule condition and FR-010 tests; links to Change 11.

### Change 6: Rule 2 declines when proof is missing, with a test that exercises the decline (INV-007, C-003, X-002; base weakness W-2, merged V1+V2+V3)
- **Source**: V3R3:53, V1R3:42 (note text only), V2R3:44; Conv:255; Conv P3.7 item 3 (Conv:326).
- **Target**: Base, section 6 rule 2 at V1:148; FR-009 at V1:59 (replace)
- **Rationale**: Base weakness W-2: V1:148 makes rule 2 return could not determine when fencing evidence is unreadable, which can hide a later rule's independently proved waiting or finished evidence. C-003 is a merge V1+V2+V3 at 90% with the text amended so rule 2 declines; X-002's winner is unchanged with the same amendment (Conv:255). Reviewer correction: V1R3:42's AC uses a `blocked` contract, which rule 1 catches first, so it does not test rule 2.
- **Integration point**: (a) V1:148: rule 2 matches only `exited` plus `worker_done_seen is False` plus `fenced_evidence == "absent"`; otherwise it declines (no match) and attaches the note `Orca: exited; fenced evidence not readable` (V1R3:42) to the row for later rules. Text from V3R3:53: "Later rules may use their own sufficient evidence. Only the final fallback returns could not determine when none matches." (b) FR-009: replace "with fencing evidence unreadable it is could not determine" with "with fencing evidence unreadable rule 2 declines and attaches the note; the row is classified by later rules, and by the fallback if none matches". (c) Replace the FR-009 acceptance with two cases: an exited row with unreadable fencing evidence and a `guard refused:` body classifies as finished (rule 6) and carries the note; an exited row with unreadable fencing and nothing else classifies as could not determine through rule 8 and carries the note. Do not use a blocked contract in this test.
- **Risk**: Medium. Changes rule semantics; a wrong test would pass without testing rule 2, which is why the AC is specified.

### Change 7: Accepted risks needing owner sign-off, and scoped lock claims (INV-005, C-025 lock sentence; base weakness W-3, from Variant 3 risk statement)
- **Source**: V3R3:34 (risk statement), V1R3:25, V2R3:27 (withdrawal of V2:228 and V2:245); Conv:275.
- **Target**: Base, new section "Accepted risks needing owner sign-off" placed after section 11 Risks; and V1:180, V1:259, V1:275, section 8 coverage header (insert and replace)
- **Rationale**: Base weakness W-3: V1:180 ("an unflagged sweep could block a live worker"), V1:259 ("the sweep never takes it") and V1:275 (R3 "Low after NFR-002") are unscoped and imply the sweep can never cause the lock case. INV-005 is ACCEPTED-RISK-OWNER-SIGNOFF and the only HIGH item left UNADDRESSED (Conv:279). It is a risk, not a requirement.
- **Integration point**: (a) New section with `Provenance: V1R3:25 + V2R3:27 + V3R3:34 (INV-005)` and one entry, quoting V3R3:34's risk statement only: "Whether Orca read verbs take optional git locks inside worker worktrees is UNVERIFIED. If they do, the sweep can disturb a live worker despite its direct `_git` safeguards. All lock-free claims are scoped to the sweep's own `_git` calls. The report states `Orca read verbs' git effects on worker worktrees: UNVERIFIED`. JSON-shape capture and mock argv tests do not prove the indirect effects safe. Owner sign-off on this residual risk is required before Phase 1 release; absent sign-off, the risk remains a blocker, not an approval inferred from debate agreement. An owner may commission separate verification outside this work, which authorizes no live launch." Add a line "Owner sign-off: not recorded." State that this entry is not a requirement. Do not include the sentence about `GIT_OPTIONAL_LOCKS=0` on `_orca` or any mitigation for `_orca`. (b) V1:180: scope to "a sweep whose own `_git` call lacked the flag could block a live worker". (c) V1:259 row: change "the sweep never takes it" to "the sweep's own `_git` calls never take it; Orca read verbs' effect is UNVERIFIED (see Accepted risks)". (d) V1:275 R3: change the likelihood text to "Low for the sweep's own `_git` calls after NFR-002; Orca read verbs UNVERIFIED (Accepted risks)". (e) Section 8 header lines: add the coverage line `Orca read verbs' git effects on worker worktrees: UNVERIFIED`. (f) WC-14 text (Change 16): if it mentions locks at all, use only V2R3:27's scoped sentence "The sweep's own git reads do not take git's optional locks." (C-025 M V2+V3).
- **Risk**: Medium. A new section plus four scoped edits; leaving any unscoped claim would contradict the accepted risk.

### Change 8: Open warnings section for INV-008, INV-011 and INV-017 (from Round 3 texts)
- **Source**: Conv P3.6 (Conv:308-318); V1R3:43, V3R3:54 (INV-008); V1R3:45, V2R3:47, V3R3:56 (INV-011); V1R3:48, V2R3:49 (INV-017); Probe INV-008, INV-011, INV-017.
- **Target**: Base, new section "Open warnings" placed after the Accepted risks section from Change 7 (insert)
- **Rationale**: All three remain MEDIUM UNADDRESSED warnings (Conv:311-313). No variant fully resolves any of them, so each is listed as open, and the partial text the variants agreed is applied in the body of the spec.
- **Integration point**: New section with `Provenance: V1R3 + V2R3 + V3R3 (INV-008, INV-011, INV-017)` and three entries. INV-008: "The fixed status template can miss untracked paths. With `status.showUntrackedFiles=no` set, untracked paths are hidden; this is a named report limitation. A reported untracked package directory (one `?? .dev/tasks/to-do/<id>/` line) counts as package activity. Absent untracked output is not proof that no package is active. `--untracked-files=normal` is a candidate for separate verification, UNVERIFIED, and not part of this spec." Also add that limitation line to the section 8 coverage header and the untracked-directory rule to FR-015. INV-011: "The pin 'It never stops watching on its own' is added (Change 16). A coordinator that sweeps rarely is not prevented, because no cadence is required in Phase 1. The 2026-11-05 owner order (re-arm after every expiry, keep a periodic sweep) is stronger than a cadence-free duty; whether a fixed cadence is needed is open." INV-017: "The sweep runs `ORCA_CLI_COMMAND` if set, else `orca-ide`. Whether the sweep's environment carries `ORCA_CLI_COMMAND` is UNVERIFIED. Inside an Orca-managed terminal the orca-cli skill selects bare `orca` (orca-cli SKILL.md:27), so where `orca-ide` is missing every sweep takes the outage path. That failure is visible as `binary not found: orca-ide` but not prevented."
- **Risk**: Low. Disclosure only, plus two small body edits.

### Change 9: Orca binary resolution with the corrected skill citation (X-009 amended, INV-017, from Variant 2 correction)
- **Source**: V1R3:48 (resolution), V2R3:49 (citation correction and reason text); `/home/coder/.claude/skills/orca-cli/SKILL.md` lines 21-27; Conv:325.
- **Target**: Base, section 7 seam at V1:175; section 10 failure rows (replace and append)
- **Rationale**: X-009's winner is V1 amended (Conv P3.1). Reviewer correction: V1R3:48 says "never bare `orca`", but orca-cli SKILL.md:27 selects bare `orca` inside Orca terminals.
- **Integration point**: Replace `["orca-ide", *args]` at V1:175 with: "`_orca` runs `[<binary>, *args]`, where `<binary>` is `ORCA_CLI_COMMAND` if set, else `orca-ide`. This is a deliberate safety deviation from orca-cli SKILL.md:27, which selects bare `orca` inside Orca-managed terminals; the sweep cannot reliably tell it is in one, and bare `orca` outside one starts the GNOME screen reader (SKILL.md:24-26)." Record the resolved binary name in the coverage header. Add a failure row: binary not found gives the unavailable class with reason `binary not found: orca-ide` (or the `ORCA_CLI_COMMAND` value). Update the NFR-003 recorded-argv test so its expected argv[0] follows the same resolution. Do not write "never bare `orca`" anywhere.
- **Risk**: Medium. Changes argv[0] in every exact-allowlist test.

### Change 10: Round 3 agreed texts for the other MEDIUM and LOW invariants (INV-004, INV-006, INV-010, INV-015, from all variants)
- **Source**: V1R3:40 and V3R3:51 (INV-004); V1R3:41, V2R3:43, V3R3:52 (INV-006); V1R3:49 (INV-010); V1R3:50 (INV-015); Conv:308, Conv:320.
- **Target**: Base, section 8 header (V1:221), section 6 data model, FR-020 (V1:70), NFR-005 (V1:85) (append)
- **Rationale**: These items have agreed Round 3 text (Conv P3.6) that is not in the V1 variant file.
- **Integration point**: INV-004: add the header line `child worktrees not discovered: Orca unavailable; worktree count is a lower bound`, applied whenever discovery is incomplete, with or without `--run` (V1R3:40, V3R3:51). INV-006: in section 6 state that `worker_done_seen` is None on live rows because no named live source establishes its absence; stalled (proved) stays fixture-only until a source mapping exists; missing proof never becomes False. INV-010: FR-020 states the cap of 50 counts only `worker-show` calls and every call counts toward the 90 s total. INV-015: NFR-005's test injects `now` and the output path.
- **Risk**: Low. Additive clarifications that all advocates agreed.

### Change 11: `worker-list` pagination gated on step 1.0a, with lower-bound totals (C-014, A-107, U-026, U-027, merged V1+V2+V3)
- **Source**: V3R3:42 and Conv:263 (final text); V2:63 (101-row AC); V3:63, V3:274 (dedupe, keep partial rows); V3:114, V3:299 (lower-bound totals).
- **Target**: Base, section 7 template at V1:187; FR-005 (V1:55); FR-020 (V1:70) (replace and append)
- **Rationale**: C-014 is M V1+V2+V3 at 90%, agreed 3 of 3 (Conv:263). A-107 was rejected in debate: the spec must not assume a Run fits in 50 rows, so cap exhaustion must be reported. V1:187 adds a cursor template whose flag is UNVERIFIED, with no gate on its tests.
- **Integration point**: Replace the V1:187 sentence with Conv:263's text: "V3's dedupe and keep-and-mark-partial rows; V1's cursor template admitted only after the step 1.0a capture; V2's 101-row AC (2 list calls) enabled only once that template exists; until then one list call per Run, and a full 100-row page sets `truncated` and prints `Orca rows: 100 shown; total is a lower bound (paging not yet captured)`." Write it as requirements: deduplicate Dispatch IDs and canonical roots; retain every discovered row, with unenriched rows above the 50-show cap marked unknown; unseen rows are not counted as known omissions (V3R3:42). Add to FR-005: totals that cannot be known are shown as lower bounds, and visible, historical and omitted counts must reconcile (V3:114, V3:299). Add to FR-020: when the cap is reached, the header says so and the row total is a lower bound (A-107). Add the gated AC: once the template exists, a 101-row fixture makes two list calls and at most 50 show calls; until then, a 100-row fixture sets `truncated` and prints the lower-bound line. Duplicate Dispatch rows with contradictory state are kept as one identity with a conflict reason (V3:63, U-026).
- **Risk**: Medium. Two ACs, one of them conditional on a capture that has not happened.

### Change 12: JSON stdout contract (C-017, C-037, INV-014, merged V1+V2+V3)
- **Source**: V3R3:43 and Conv:264 (final text); V2:139-141 and V2:81 (row `rule` and `evidence`); V3:167-177, V3:185 (zero counts, ID-only `waiting`, print after publication).
- **Target**: Base, FR-017 (V1:67), NFR-009 (V1:89), section 6 row model (V1:139), section 8 JSON block (V1:234) (replace and append)
- **Rationale**: C-017 is M V1+V2+V3 at 90%, agreed 3 of 3 (Conv:264); C-037 went to V2 at 75%. V1's key `class`, schema version 1 and golden key-set test stay; V2's key `cls` does not (X-012 to V1).
- **Integration point**: Rewrite FR-017's JSON clause from V3R3:43: "schema version 1, additive-only compatibility, golden key-set test and row key `class`; per-row `rule`, `evidence`, `notes` and `safe_to_close`, never yes in Phase 1; explicit zero counts and `waiting.a`/`waiting.b` as stable-ID lists. Markdown and JSON share the observation model. Print the one success JSON object only after report publication. Failed publication exits 1 without success JSON or overwriting an earlier observation." In section 6 add `evidence` (the field and source behind the class) next to `rule` at V1:139, and show it in the ledger rows (V2:139-141). Add ACs: stdout is empty of success JSON when the report write is made to fail; zero counts are present; `waiting.a` and `waiting.b` hold IDs only.
- **Risk**: Medium. The golden key-set test must be written with the added keys from the start, or NFR-009 fails.

### Change 13: Collision-safe report path and re-run behaviour (C-019, C-020, X-019, A-008; base weakness W-4, from Variant 3)
- **Source**: V3:179-187 (re-run section), V3:133-134 (NFR-006), V3:187 (footer).
- **Target**: Base, FR-017 path clause (V1:67), section 8 path (V1:210); new subsection in the CLI contract section of Change 40 (replace and insert)
- **Rationale**: Base weakness W-4: V1 has no re-run or collision rule (C-020), and two sweeps in the same second would overwrite or collide (X-019, A-008 contradicted by V3:134). C-019 and C-020 went to V3 at 95%; X-019 to V3 at 95%.
- **Integration point**: Keep V1's base name `<output>/<YYYYMMDD-HHMMSS>-sweep.md` (UTC). Add from V3:181-187: if the name exists, add a collision suffix; reserve the path exclusively (create-new, never overwrite); a sweep changes no lifecycle state and advances no cursor; every run that publishes a report writes a new dated file and never reuses or overwrites an earlier path, while a run that exits 1 or 2 writes no report (Change 3; V3:164); the report ends with the footer line `Report complete`. Change V1:67's AC from "file exists at the dated path" to "file exists at the dated path or its suffixed form, and an existing file is never overwritten". Add an AC: two report-publishing sweeps with the same injected `now` produce two files.
- **Risk**: Medium. Changes the path AC and the write primitive.

### Change 14: Report section set and order (C-018, X-014, U-016, U-027, U-032; base weakness W-5, merged V2+V3)
- **Source**: V2:207-217 and V2:211 (could-not-determine before working rows); V3:297-307 (source coverage, Shift Brief, "What I could not determine", footer); V3:15, V3:197, V3:298 (collection interval).
- **Target**: Base, section 8 section list V1:223-230 and header V1:221 (restructure)
- **Rationale**: Base weakness W-5: V1:208 claims to copy the Shift Brief but V1:223-230 has none (X-014, V1 conflicts with itself and with the seed). C-018 is M V2+V3 at 75%. X-014 is V2=V3 for the Shift Brief.
- **Integration point**: Replace the V1:223-230 list with this order: Header (with the coverage lines from Changes 7, 8, 9 and 10, and the collection interval with the statement that the report is not an atomic runtime snapshot, V3:298); Source coverage (V3:297); Waiting on a person (a) explicit questions; Waiting on a person (b) blocked by policy; Could not determine (placed before working rows because an unknown can hide a person-wait, V2:211); Retained problems; Sessions; Worktrees; Historical sessions; Shift Brief (V3:306); What I could not determine (V3:307); footer `Report complete` (Change 13). Keep V1's `SECTIONS` tuple of pure render functions (V1:208) and update its contents to this order. Update the FR-011 heading-order test to the new order.
- **Risk**: Medium. Restructures the renderer contract and the heading-order test.

### Change 15: Next inspection on every session row (C-038, X-015; base weakness W-6, from Variant 3)
- **Source**: V3:303 (next inspection in Sessions), V3:316 (inspection-only steps).
- **Target**: Base, section 8 Sessions row at V1:228 (append column)
- **Rationale**: Base weakness W-6: V1:228's Sessions row has no next action, so it misses the seed requirement that every session shows class, waiting-on and next action (S1 gap, BS). C-038 and X-015 went to V3 at 75%.
- **Integration point**: Add a `next inspection` column to the Sessions row at V1:228. Its value is an inspection step only (what to read or check next), never a stop, retry, release, merge or removal (ties to Change 18). Keep V1:232's "no action controls" sentence. Add an AC: every Sessions row has a non-empty `next inspection` cell, and no cell contains a verb from the Change 18 list.
- **Risk**: Low. One column and one test.

### Change 16: WC-14 end condition, pin and presentation (C-022, INV-012, S-013, from Variant 3 and Variant 2)
- **Source**: V3:324-325 and V3R3:44 (end condition and pin); Conv:265; V2:225-229 (fenced block with heading, S-013).
- **Target**: Base, section 9 WC-14 text at V1:240 and pins at V1:248 (replace and append)
- **Rationale**: C-022 went to V3 at 90%, agreed 3 of 3 (Conv:265). V1's "settled and been admitted" ignores rejected results. S-013 went to V2 at 95%. INV-012 is answered by C-022 (V3R3:57).
- **Integration point**: In V1:240, replace "every Task it created has settled and been admitted" with "until every Task it created is settled and every result has been inspected and its admission or rejection recorded" (V3:324-325), and add the sentence "It never stops watching on its own." Do not make this sentence depend on a Run-scoped task-list form (V3R3:44). Present the WC-14 text as a fenced Markdown block under its own heading, as V2:225-229 does, instead of a blockquote. At V1:248 add the fourth pin phrase "It never stops watching on its own" to `RULE_PHRASES["WC-14"]`, alongside V1's three pins, including "it is never posted" (X-017 to V1). Keep V1's count-free test rename (C-026). Owner approval of the shared contract text remains required.
- **Risk**: Medium. Edits shared contract text that needs owner approval; the pin test must match the final wording exactly.

### Change 17: Periodic sweep duty without a scheduler or cadence (C-023, X-008, INV-011, from Variant 3)
- **Source**: V3:326-328; V3R3:56; owner order recorded in `coordinator-never-stop-polling.md` line 11 (cited by V1R3:45).
- **Target**: Base, section 9 V1:240 and V1:245; section 13 V1:314 (replace)
- **Rationale**: C-023 and X-008 went to V3 at 90%. V1:245 and V1:314 call a cron sweep "an operator choice", which is weaker than the 2026-11-05 owner order (INV-011, Probe:17).
- **Integration point**: In WC-14 add: "It sweeps on every wake and keeps a periodic sweep scheduled while work remains." Replace V1:245's "allowed by this text but not required" and V1:314's "a cron sweep stays an operator choice" with "a periodic sweep is a coordinator duty while work remains; Phase 1 sets no cadence and adds no scheduler". Do not adopt V3:405's five-minute cadence (see Changes NOT Being Made). Cross-reference the INV-011 open warning (Change 8).
- **Risk**: Low. Contract wording; no code.

### Change 18: "Recommends nothing" with the verb list (C-024, X-003, from Variant 3 merged with V1)
- **Source**: V3:335; V1:240, V1:244.
- **Target**: Base, section 9 V1:240 and V1:244 (replace)
- **Rationale**: C-024 is M V1+V3 at 95%; X-003 is M V1+V3 (recommends nothing). V2's text that lets the sweep recommend stop-and-cancel, removal and a new Task is rejected.
- **Integration point**: Replace V1's "The sweep recommends none of these actions" with "The sweep recommends nothing: no stop, retry, release, merge or removal." (V3:335 verb list, V1 framing). Add an AC on the fixture reports: no rendered text proposes any of those five actions (V3:105).
- **Risk**: Low. One sentence and one negative test.

### Change 19: Extra WC-14 sentences on duty and heartbeat (C-025, merged V2+V3)
- **Source**: V3:328-329; V2R3:27 (scoped lock sentence).
- **Target**: Base, section 9 WC-14 text (append)
- **Rationale**: C-025 is M V2+V3 at 75%: the lock-free sentence scoped to direct `_git`, plus the heartbeat sentence.
- **Integration point**: Append to WC-14: "Phase 1 adds this duty, not a scheduler." and "A missing heartbeat is absence, never death." If a lock sentence is used, it is only "The sweep's own git reads do not take git's optional locks." (Change 7). Do not use V2:228's unscoped observer guarantee.
- **Risk**: Low. Wording only.

### Change 20: PR #422 sequencing (C-034, INV-013, merged V1+V3)
- **Source**: V3R3:45 and Conv:266 (final text); V1:313.
- **Target**: Base, section 9 V1:248; section 13 row at V1:313 (replace)
- **Rationale**: C-034 is M V1+V3 at 90%, agreed 3 of 3 (Conv:266). V1:248 ("PR #422 lands ... before the contract edit") allows WC-14 to slip out of done.
- **Integration point**: Replace with V3R3:45's text: "new package, command, skill and docs first; verify current overlap with PR #422 before editing the contract. If #422 merges first, rebase this PR accordingly. WC-14 and its contract pins remain deliverables of this PR even if #422 stalls; no follow-up-PR escape from done. This states sequencing, not a claim about #422's current status."
- **Risk**: Low. Sequencing text only.

### Change 21: Git allowlist of one status template, root by path walk (X-004, C-009, C-012, U-018, merged V1+V2)
- **Source**: V2:203 (path walk, no git call); V2:200-203; debate resolution X-004 M V1+V2.
- **Target**: Base, section 7 git allowlist V1:197-202, the `rev-parse --show-toplevel` template at V1:200; FR-004 default root (remove and replace)
- **Rationale**: X-004 is M V1+V2: exactly one status template; no `log`, `rev-parse`, `branch` or `--version`. C-009 is M V1+V2 at 90% (status only, root by path walk). C-012 went to V2 at 90% (path walk plus a `.git` file-or-folder AC).
- **Integration point**: Remove the `rev-parse --show-toplevel` template at V1:200. `ALLOWED_GIT` holds exactly `git --no-optional-locks -C <path> status --porcelain --branch`. Default `--root` is found by walking up from the current directory with plain reads to the first directory holding `.git`, as a file (linked worktree) or a folder. Add the AC: the walk accepts both a `.git` file and a `.git` folder and records no `_git` argv. Keep V1:202's statement that unmerged commits are not observed in Phase 1 (C-013 to V1). Update the exact-allowlist negative cases to include `rev-parse`, `log`, `branch` and `--version`.
- **Risk**: Medium. Removes a template V1 uses and adds a new discovery routine.

### Change 22: One isolated real-git control test (C-011, X-010, U-011, merged V1+V2)
- **Source**: V2:98 (NFR-002 control experiment), V2:245 (F7, test only, not its lock claim), V2:100.
- **Target**: Base, NFR-002 (V1:82), NFR-001 and NFR-013 subprocess rule (V1:81, V1:93), FR-025 acceptance (V1:75) (append and amend)
- **Rationale**: C-011 is M V1+V2 at 90%; X-010 went to V2 at 95% "as one isolated real-git test", and A-017 stands at 95% "qualified: one isolated real-git test allowed" (debate-transcript.md:195, :221). The count is therefore one test. A recorded-argv test alone does not show that the flag prevents the index rewrite.
- **Integration point**: Add to NFR-002's AC one marked real-git test in an isolated `tmp_path` repository. It holds every real-git assertion in the spec: (1) the control: a plain `git status` rewrites the index while `git --no-optional-locks status` does not; if the control shows no rewrite, only this assertion is reported as inconclusive (V2:98); (2) with a copy of the repository's `.gitignore`, `git check-ignore .dev/sweeps/x.md` succeeds (V1:75); (3) `git check-ignore .dev/tasks/to-do/x.md` fails (Change 35); (4) writing a file under `.dev/sweeps/` leaves `git status --porcelain` unchanged (V1:75). Amend V1:75's FR-025 AC to say its checks run inside this one marked test. Amend NFR-001 and NFR-013: real subprocess entry points stay patched to raise in every test except this one marked test, which may run `git` only inside `tmp_path`. This test proves nothing about Orca read verbs (Change 7).
- **Risk**: Medium. One exception to the no-real-subprocess rule; it must stay isolated.

### Change 23: Read-only snapshot test contents (C-028, merged V1+V2)
- **Source**: V2:97, V2:100.
- **Target**: Base, NFR-001 acceptance at V1:81 (amend)
- **Rationale**: C-028 is M V1+V2 at 75%.
- **Integration point**: Keep V1's isolated `HOME` and `XDG_STATE_HOME` and "exactly one added file". Specify the snapshot as (path, size, mtime_ns, sha256) for every file under the root, `HOME` and the XDG dirs, including a fixture `~/.claude/` (V2:97).
- **Risk**: Low. Test detail.

### Change 24: Budget with per-call remaining time and byte limits (C-029, U-023, merged V1+V3)
- **Source**: V3:124-125 (remaining time limits each call), V3:137 (byte limits).
- **Target**: Base, FR-020 (V1:70), section 7 Budget (V1:178) (append)
- **Rationale**: C-029 is M V1+V3 at 75%: injected Budget, per-call remaining time and byte limits.
- **Integration point**: Keep V1's injected `Budget` (50 / 10 s / 90 s). Add: each call's timeout is the lesser of 10 s and the remaining total budget. Add byte limits as proposed limits: 1 MiB per contract or ledger read, 256 KiB transcript tail, 8 MiB subprocess output. Mark them "proposed; rationale required before release". A read that hits a limit marks that source unscanned with a reason.
- **Risk**: Low. Bounded additions; the numbers are flagged as proposals.

### Change 25: `sanitize()` adds HTML neutralizing (C-030, U-031, merged V1+V3)
- **Source**: V3:317-318.
- **Target**: Base, FR-016 (V1:66) (append)
- **Rationale**: C-030 is M V1+V3 at 75%: fold line feeds to a space (V1, not V2's removal) plus HTML neutralizing.
- **Integration point**: Keep V1's FR-016 text. Append: "and neutralizes Markdown HTML so no untrusted text becomes an active tag or link." Add `<script>` and a Markdown link to the injection fixture.
- **Risk**: Low.

### Change 26: `--output` validation through symlinks and without overlap (C-040, U-030, from Variant 3)
- **Source**: V3:156-157.
- **Target**: Base, FR-004 (V1:54) (append)
- **Rationale**: C-040 went to V3 at 95%.
- **Integration point**: Append to FR-004: "The check uses the resolved path, so a symlink cannot lead outside `<root>/.dev/`, and the output directory must not overlap any input package or transcript directory." Add ACs for a symlinked `--output` that escapes and for `--output` equal to a package directory; both exit 2 and write nothing.
- **Risk**: Low.

### Change 27: Disk discovery scope and symlink checks (C-041, FR-006 of V2, merged V2+V3)
- **Source**: V2:64 (fixed patterns, no recursive walk, `resolve()` check, never `ccsession --list`), V2:247 (F9 symlink escape); V3:288-292.
- **Target**: Base, section 7 disk readers at V1:204 (append)
- **Rationale**: C-041 is M V2+V3 at 95%. V1:204 lists read targets with no symlink rule.
- **Integration point**: Append to V1:204: disk discovery uses fixed patterns only, never a recursive walk; every resolved path is checked with `resolve()` to stay inside its allowed root, and an escaping symlink is rejected and reported; ccsession files are read directly, never through `ccsession --list`. Add the F9 symlink-escape fixture as an AC.
- **Risk**: Low.

### Change 28: Forbidden-verb test adds a negative `worker-read` case (C-039, merged V1+V2)
- **Source**: V2:99.
- **Target**: Base, FR-021 acceptance (V1:71) (append)
- **Rationale**: C-039 is M V1+V2 at 75%: static forbidden list plus a negative `worker-read` test.
- **Integration point**: Keep V1's static test over `ALLOWED_ORCA`. Add a negative test: a `worker-read` argv passed to `_orca` raises before any subprocess starts.
- **Risk**: Low.

### Change 29: Failure-mode table as the union, with a test column (C-027, S-007, U-026; base weakness W-7, merged V1+V2+V3)
- **Source**: V2:237-247 (F1-F9 and the Test column); V3:347-358 (input change during read, duplicate Dispatch, process killed, remote host).
- **Target**: Base, section 10 table V1:254-267 (restructure)
- **Rationale**: Base weakness W-7: V1's failure table has no test column, so a mode can be listed without a check (S-007 to V2 at 75%). C-027 is M V1+V2+V3 at 95% (union of failure modes).
- **Integration point**: Columns become Mode / Detection / Behaviour / Exit / Test. Keep V1's 12 rows, as amended by Changes 3, 4, 7 and 9. Add V2's rows not already present, including symlink escape (F9). Add V3's rows: input changed during read (one plain re-read, then a conflict reason, V3:353-354), duplicate Dispatch with contradictory state (one identity with a conflict reason), process killed (no partial report presented as complete, because the footer is missing), remote host (could not determine). Do not add V2's "git too old" row, because the git version gate is not adopted (C-010 to V1). Every row names its test.
- **Risk**: Medium. Many rows; each needs a test name that exists in the plan of record.

### Change 30: Package states block removal including archive-blocked (C-006, X-006, merged V1+V2)
- **Source**: V2:160-168, V2:168.
- **Target**: Base, section 6 package-state table V1:158-167, the V1:164 sentence, FR-013 (V1:63) (replace)
- **Rationale**: C-006 is M V1+V2 at 90% ("V1's six states including `unknown`, with archive-blocked blocking removal", debate-transcript.md:148); X-006 is M V1+V2 ("removal blocked on archive-blocked with V1's state set", debate-transcript.md:191). Neither row makes `unknown` block removal.
- **Integration point**: Keep V1's six states including `unknown`, and keep V1:167 unchanged (an unreadable ledger prints could not determine). Replace V1:164's "no by itself, printed in Package state column" with "yes, printed in Package state column". Add `archive-blocked` to FR-013's list of blocking package states (V1:63), with a fixture. `unknown` is not added to FR-013 (see Changes NOT Being Made).
- **Risk**: Medium. Changes a removal rule; erring here only makes the sweep more conservative.

### Change 31: Partial contracts stay usable-not-yet-judged; finished never means admitted (C-004, from Variant 3)
- **Source**: V3:228-229.
- **Target**: Base, section 6 rule 6 at V1:152 (append)
- **Rationale**: C-004 went to V3 at 90%. X-018 stays with V1 (a finished class needs a parsed contract or a `guard refused:` body).
- **Integration point**: Keep V1:152's note "partial: usable not yet judged". Append the sentence "Finished never means admitted." Add an AC that a finished row's JSON and report text never say admitted or accepted.
- **Risk**: Low.

### Change 32: "Ownership review", never "foreign" (C-005, from Variant 3)
- **Source**: V3:226, V3:301.
- **Target**: Base, section 6 rule text at V1:150 (replace wording)
- **Rationale**: C-005 went to V3 at 75%.
- **Integration point**: Keep V1:150's "a ready Task (creator: could not determine)" and label such rows for "ownership review". The merged text never uses the word "foreign" for a Task.
- **Risk**: Low.

### Change 33: Person-started readability and activity-window exemptions (C-035, U-028, from Variant 3)
- **Source**: V3:93, V3:234-237.
- **Target**: Base, FR-010 (V1:60), rule 7 at V1:153 (append)
- **Rationale**: C-035 went to V3 at 90%.
- **Integration point**: Append to FR-010: a transcript must be readable to count; an unknown timestamp is never idle; open Tasks, explicit waits and unread-report candidates are exempt from the activity window and never go to Historical. Add one fixture per exemption.
- **Risk**: Low. Narrows idle and Historical further, in the same direction as Change 5.

### Change 34: Rollback keeps the ignore line and never removes `.dev/tasks/` (C-031, X-013, merged V1+V3)
- **Source**: V3:425-431, V3:427.
- **Target**: Base, section 14 rollback table V1:320-333 (append)
- **Rationale**: C-031 is M V1+V3 at 75%; X-013 is M V1+V3.
- **Integration point**: Keep V1:330's row. Add: the ignore line is reverted only after deciding where existing reports go (V3:427), and rollback never removes `.dev/tasks/` or any file in it.
- **Risk**: Low.

### Change 35: `.gitignore` check in both directions and the self-observation risk (FR-026 of V2, U-014, U-015, from Variant 2)
- **Source**: V2:93 (`git check-ignore` both directions); V2:262, V2:265 (R8).
- **Target**: Base, FR-025 (V1:75); section 11 risk table (append)
- **Rationale**: BS lists this as a V2 strength to incorporate. V1's AC only checks that `.dev/sweeps/` is ignored, not that `.dev/tasks/` stays tracked.
- **Integration point**: Append to FR-025's AC: `git check-ignore .dev/tasks/to-do/x.md` fails (the path is not ignored), alongside V1's positive `.dev/sweeps/` check. Add risk R8 from V2:262: without the ignore line, the sweep reports its own previous report as an uncommitted change.
- **Risk**: Low. Both `check-ignore` assertions run inside the one marked real-git test of Change 22, not in a test of their own (X-010, A-017).

### Change 36: Risk table gains impact (S-008; base weakness W-8, from Variant 2)
- **Source**: V2:253-263.
- **Target**: Base, section 11 table V1:271-281 (restructure columns)
- **Rationale**: Base weakness W-8: V1:271's risk table rates likelihood only, so a severe low-likelihood risk reads as minor. S-008 went to V2 at 95%.
- **Integration point**: Change the Likelihood column to "Likelihood / impact" and give every V1 risk an impact rating, keeping V1's risk rows and mitigations. R3 uses the scoped text from Change 7.
- **Risk**: Low.

### Change 37: GQ and open-question table layouts (S-009, S-010, from Variant 2)
- **Source**: V2:271-285 (Gap / Root cause / Resolution), V2:289-298 (OQ-1 to OQ-n IDs).
- **Target**: Base, section 12 table V1:287-300 and section 13 table V1:306-316 (restructure)
- **Rationale**: S-009 and S-010 went to V2 at 95%.
- **Integration point**: Section 12 keeps V1's GQ rows and its "Where" column, and adds a "Root cause" column. Section 13 gives each row an ID OQ-1 onward, keeping V1's rows and answers (C-032, C-033, C-042 stay with V1), with the C-034 row replaced by Change 20 and the cron row replaced by Change 17.
- **Risk**: Low.

### Change 38: Evidence provenance statement (S-012, from Variant 2)
- **Source**: V2:9.
- **Target**: Base, header block V1:12 (append)
- **Rationale**: S-012 went to V2 at 95%. V1 already lists exact line ranges read.
- **Integration point**: Append to V1:12 that the debate's Round 3 files are additional sources (named by absolute path) and that the host git version, if quoted, must be recorded with the date it was checked. Do not copy V2's quoted version number unless the merge-executor re-checks it.
- **Risk**: Low.

### Change 39: Separate verification checklist (S-011, from Variant 3, without the live check)
- **Source**: V3:414-423.
- **Target**: Base, new subsection at the end of section 14, "Verification checklist" (insert)
- **Rationale**: S-011 went to V3 at 90%.
- **Integration point**: Add a checklist that lists, by requirement ID, every AC the merged spec now holds (FR, NFR, failure-mode tests) plus the repo gates in NFR-012. Leave out V3:421's live disposable-Run check (X-016 V1=V2, no live check). Add the INV-005 owner sign-off as a release precondition that is not a test.
- **Risk**: Low.

### Change 40: Section order and renumbering (S-002, S-004, merged V1+V3)
- **Source**: V3:148 (CLI contract and re-run idempotency section); V1 section order.
- **Target**: Base, whole document (restructure)
- **Rationale**: S-002 is M V1+V3 at 75%. S-004 stays with V1 but notes that a merge must renumber where IDs collide.
- **Integration point**: Keep V1's 14 numbered sections in order. Insert a new section "CLI contract and re-run idempotency" after section 4 (NFR), holding the exit-code contract (Change 3), stdout JSON rule (Change 12) and re-run rules (Change 13), with cross-references from FR-017 and FR-018. Insert "Accepted risks needing owner sign-off" (Change 7) and "Open warnings" (Change 8) after Risks. Renumber the sections after each insertion. Keep V1's FR and NFR IDs; any new requirement gets the next free V1 ID (FR-026 onward, NFR-014 onward), never a V2 or V3 ID. Record the new IDs in the merge-log.
- **Risk**: Medium. Renumbering can break internal cross-references such as "section 6" and "section 7" in V1's ACs; each must be updated.

### Change 41: Read only the needed `worker-show` fields (FR-005 of V2, from Variant 2)
- **Source**: V2:63.
- **Target**: Base, section 7 Orca templates and section 6 data model (append)
- **Rationale**: BS lists this as a V2 strength to incorporate. Reading only what classification needs reduces exposure to unknown fields.
- **Integration point**: State that the parser reads only the `worker-show` fields the section 6 model needs and ignores others; an unknown field is not an error. This matches V1's existing "unknown schema field" failure row.
- **Risk**: Low.

### Change 42: Expand GQ, WC and other short forms on first use (base weakness W-9, no variant handles it better)
- **Source**: None; BS records V1's lack of expansion as a clarity weakness, and no variant expands them either.
- **Target**: Base, header block and first use in each section (insert)
- **Rationale**: Base weakness W-9: V1 uses GQ (gap question, from the GAPS file), WC (worker-contract rule), REPORT, GAPS, CND and similar short forms without expanding them.
- **Integration point**: Add a short terms list to the header: GQ = gap question in `gaps-and-questions.md`; WC = rule in `WORKER-CONTRACT.md`; REPORT and GAPS as V1:12 defines them; Run, Task and Dispatch as Orca terms. Expand each on first use in the body. Do not invent meanings: where a short form's meaning is not stated in a source, mark it UNVERIFIED.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| X-001, C-015 | V2 exits 0 when Orca is down with no `--run`, as a named exception (V2:57, V2:84) | Neither V2 nor V1 is kept on this point: Round 3 moved both to V3 (exit 2), and V2R3:24 itself withdrew exit 0. Change 3 replaces V1's text. |
| X-007 | V2 lists idle after rule 7 "anything else" (V2:155-156), so idle is unreachable | V1's rule 7 idle before the rule 8 fallback (V1:153-154) is reachable; X-007 went to V1. |
| X-009 | V2 runs bare `orca` (V2:175) while naming `orca-ide` elsewhere (V2:84) | Self-inconsistent; X-009 went to V1 amended (Change 9). |
| X-012 | V2 row key `cls` (V2:81) | V1's `class` (V1:234) won; renaming would break the golden key-set test. |
| X-003, C-024 | V2's WC-14 lets the sweep recommend stop-and-cancel, removal and a new Task (V2:228, V2:86) | Recommends nothing (Change 18); X-003 is M V1+V3. |
| C-022 | V2's "as shown by the Run's own task list" clause (V2:228) | Depends on an unverified Run-scoped task-list form (V3R3:44); C-022 went to V3. |
| C-025, INV-005 | V2's unscoped lock-free sentences (V2:228, V2:245) | Withdrawn by V2R3:27; only the scoped sentence survives (Change 7, Change 19). |
| INV-005 | V2R3:27 requires `GIT_OPTIONAL_LOCKS=0` on `_orca` with an AC | Unverified that Orca inherits or honours it (V3R3:64); it is a candidate mitigation only and is left out of the merged spec. |
| INV-008 | V2R3:45 adds `--untracked-files=normal` to the status template | UNVERIFIED and not agreed (Conv:316); listed only as a candidate in Open warnings (Change 8). |
| C-034 | V2's follow-up-PR route for WC-14 if #422 stalls (V2:295, V2:259) | WC-14 stays in this PR's done (Change 20). |
| C-014 | V2's unconditional paging AC on `page.nextCursor` (V2:63) | The cursor flag is UNVERIFIED; the AC is gated on step 1.0a (Change 11). |
| C-010, U-012 | V2's git version gate marking git sources `unscanned: git too old` (V2:176-180) | C-010 went to V1; no `--version` in the allowlist (X-004). |
| C-013, U-017 | V2's per-child `git log` for unmerged commits (V2:75) | C-013 went to V1; `log` is outside the one-template allowlist (X-004). |
| C-030 | V2 removes line feeds instead of folding them (V2:83) | C-030 is M V1+V3; V1's fold to a space keeps words apart. |
| S-005, S-006 | V2's data-flow and rejected-placements layout, and its 7.1 to 7.3 data-model subsections | S-005 and S-006 went to V1; V1's module table, B1 to B5 and extension points stay. |
| S-001, S-003 | V2 and V3 header and requirement formats | S-001 and S-003 went to V1; V1's tables stay. |
| X-016, U-029 | V3's separately authorized disposable-Run live check before release (V3:403, V3:421) | Conflicts with the seed's no-live-launch rule; X-016 is V1=V2. Release depends on owner sign-off (Change 7) instead. |
| C-023 | V3's recommended five-minute cadence (V3:405) | No cadence is required in Phase 1 (V3R3:56); the duty is kept without a number (Change 17). |
| C-007, X-005 | V3's plain-read comparison against a fixed base tree for active packages (V3:246, V3:284-285) | C-007 and X-005 went to V1; one status call answers GQ-101, and no base-reading argv exists. |
| C-008, X-011 | V3's five Orca forms without the non-ready `task-list --run` (V3:266-271) | C-008 and X-011 went to V1; V3 itself needs the gate policy that this form supplies (V3:202). |
| X-017, C-026 | V3's WC-14 without the pin "it is never posted" (V3:334) | X-017 and C-026 went to V1; V1's pins stay (Change 16 adds one). |
| X-018 | V3's "unreadable contract or transcript: not finished" (V3:352) | X-018 went to V1. |
| S-002 | V3's 12 unnumbered sections with no architecture section, and verification merged into rollback | S-002 is M V1+V3: only V3's CLI contract section is taken (Change 40); V1's architecture section stays. |
| C-033 | V3's "use this spec's section contract" for the #409 layout (V3:372, V3:407) | C-033 is V1=V2. |
| C-036 | V2's omission of the ten #409 dimensions | C-036 went to V1. |
| A-107 | Shared assumption that a typical Run fits within 50 rows | Rejected in debate; cap exhaustion is reported instead (Change 11). |
| INV-007 | V1R3:42's acceptance test with a `blocked` contract | Rule 1 catches it before rule 2, so it does not test the decline (Conv:326); Change 6 specifies a rule 6 case. |
| INV-017 | V1R3:48's "never bare `orca`" wording | Contradicts orca-cli SKILL.md:27 (Conv:325); Change 9 states the deviation instead. |
| C-006, X-006 | Adding `unknown` to FR-013's blocking package states (an earlier draft of Change 30) | No variant or debate row supports it: C-006 (debate-transcript.md:148) and X-006 (:191) decide only that archive-blocked blocks removal, V2:160-168 has no `unknown` state, and V1:167, which the plan keeps, prints could not determine for an unreadable ledger. |
| Seed path | `../../seed-brief.md` in V1R3:6, V2R3:6 and V3R3:27 | Resolves to a file that does not exist (Conv:324); Change 2 uses the absolute path. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|-----------------|----------|
| 1 | Low | Sections lose traceability to the debate | Remove `Provenance:` lines and inline tags |
| 2 | Low | Readers follow a dead seed path | Restore V1:12 wording |
| 3 | High | Exit-code contract left mixed (V1 exit 0 and V3 exit 2 both present); the skill and tests disagree with the seed | Revert FR-002, FR-018, FR-019 and the three section 10 rows to V1 together, never one at a time, and reopen X-001 |
| 4 | Medium | Row-local failures treated as global, or malformed bodies read as `ok` | Revert to V1:177 single catch; keep the INV-002 text in Open warnings |
| 5 | Medium | Outage transcripts reported as idle or Historical | Revert V1:136 and V1:153; keep the three ACs as open items |
| 6 | Medium | Rule 2 hides finished or waiting evidence, or the test does not exercise it | Revert V1:148; keep the corrected AC |
| 7 | Medium | Lock claims overstate safety; release proceeds without owner sign-off | Remove the new section and restore V1:180, V1:259, V1:275; INV-005 stays a blocker either way |
| 8 | Low | Known limitations hidden from readers | Remove the Open warnings section |
| 9 | Medium | Exact-argv tests fail, or wrong binary runs | Restore `["orca-ide", *args]` |
| 10 | Low | Agreed MEDIUM texts missing | Remove the appended lines |
| 11 | Medium | Paging tests written before the flag is known, or totals overstated | Restore V1:187 and drop the gated AC |
| 12 | Medium | Golden key-set test fails, or success JSON printed after a failed write | Restore V1 FR-017 key set |
| 13 | Medium | Reports overwritten, or path tests fail | Restore V1:67 path rule |
| 14 | Medium | Renderer order and heading test diverge | Restore V1:223-230 list and add only the Shift Brief |
| 15 | Low | Sessions lack a next step (S1 gap remains) | Remove the column |
| 16 | Medium | WC-14 pin test fails, or contract text changes without owner approval | Restore V1:240 and V1:248 |
| 17 | Low | Duty wording conflicts with the owner order | Restore V1:245 and V1:314 |
| 18 | Low | Report proposes actions | Restore V1:240 sentence |
| 19 | Low | Extra WC-14 sentences break pins | Remove the two sentences |
| 20 | Low | WC-14 deferred out of done | Restore V1:248 and V1:313 |
| 21 | Medium | Root discovery wrong in linked worktrees, or allowlist test fails | Restore the `rev-parse` template at V1:200 |
| 22 | Medium | Real git runs outside `tmp_path`, or a second real-git test appears | Remove the marked test and its exception; restore V1:75's FR-025 AC |
| 23 | Low | Snapshot test misses a write | Restore V1:81 AC |
| 24 | Low | Calls exceed the total budget, or reads unbounded | Remove the remaining-time and byte-limit lines |
| 25 | Low | HTML injected into the report | Remove the appended clause |
| 26 | Low | Output escapes through a symlink | Remove the appended clause |
| 27 | Low | Discovery follows an escaping symlink | Remove the appended rules |
| 28 | Low | `worker-read` slips through | Remove the negative test |
| 29 | Medium | Failure rows without tests, or rows contradict Changes 3 and 4 | Restore V1:254-267 and re-apply only Changes 3, 4, 7 and 9 |
| 30 | Medium | Worktree marked removable while archive-blocked | Restore V1:164 |
| 31 | Low | Finished read as admitted | Remove the sentence |
| 32 | Low | Rows labelled foreign | Restore V1:150 wording |
| 33 | Low | Open Tasks or waits hidden in Historical | Remove the exemptions |
| 34 | Low | Rollback deletes reports or `.dev/tasks/` | Restore V1:320-333 |
| 35 | Low | `.dev/tasks/` silently ignored | Remove the negative assertion from the Change 22 test and R8 |
| 36 | Low | Severe risks read as minor | Restore V1:271 columns |
| 37 | Low | GQ and OQ tables lose root cause or IDs | Restore V1 layouts |
| 38 | Low | Sources unclear | Restore V1:12 |
| 39 | Low | ACs not checked before release | Remove the checklist |
| 40 | Medium | Broken section cross-references or ID collisions | Restore V1 numbering and move inserted sections to an appendix |
| 41 | Low | Parser rejects unknown fields | Remove the sentence |
| 42 | Low | Short forms stay unexplained | Remove the terms list |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-08T04:21:15Z (session-context time; clock time UNVERIFIED)

Note: auto-approval covers this plan only. It is not owner sign-off for INV-005, which stays an unresolved conflict in the return contract (Change 7).
