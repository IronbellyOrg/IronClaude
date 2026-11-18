# Round 1 advocate: Variant 1 (opus, architect)

- Round: 1 of 2. Variant defended: `variant-1-opus-architect.md`. Persona: architect. Instruction: prioritize maintainability and extension scaffolding.
- Inputs read in full: the three variants and `diff-analysis.md` (same folder).
- Status: complete. Nothing else was edited.
- My own live checks this round (beyond V-01 to V-30), labelled L1 to L11 below:
  - L1 `Makefile:108-123`: `sync-dev` loops `src/superclaude/skills/*/` into `.claude/skills/`; no `core` step anywhere in the target.
  - L2 `Makefile:166-196`: `verify-sync` diffs every `src/superclaude/skills/*/` against `.claude/skills/` in both directions.
  - L3 Glob: `.claude/skills/sc-bare-review/SKILL.md` exists; `.claude/REVIEW-SEVERITY.md` and `.claude/WORKER-CONTRACT.md` do not; `plugins/superclaude/skills/` holds 4 skills.
  - L4 `src/superclaude/skills/sc-bare-review/SKILL.md:3` ends "Delegate-only" plus "no slash command"; Grep finds no other `src` SKILL.md with that marker.
  - L5 `tests/skills/test_review_severity_rule.py`: `canonical_rule_bullets` at 79, hard-coded `S1_S3_FILES = (` at 181, `S5_FILES = S1_S3_FILES[:6]` at 193, `CANONICAL_CAP_TEXT` at 215.
  - L6 `scripts/build_superclaude_plugin.py:16` `PLUGIN_SRC = ROOT / "plugins" / "superclaude"`; line 76 copies `agents, commands, hooks, rules, scripts, skills` from that tree only.
  - L7 `src/superclaude/output-styles/pragmatic.md:221` reviewer brief hunts "false claims"; 225 to 231 hold S1 to S5, Medium ("once per loop") and the spec-panel scale.
  - L8 `blocker_truth_table_sketch.py:5` `ORDER` has NOTE, FOLLOW_UP, SHOW_USER, BLOCKING only; line 68 skips moves with `UNSET in (base[i], new)`.
  - L9 `install_core.py:58` globs `core/*.md`, line 70 skips an existing file unless `force`; `install_skills.py:102` does the same for an existing skill folder.
  - L10 `skills/task/SKILL.md:252` matches "highest severity"; `gate1-cycle-control.md:20` names NEW-1 and NEW-2 as the open findings that forced the last fix cycle.
  - L11 `tests/skills/test_review_severity_mapping.py` contains "Medium" 8 times (Grep count).

## Position summary

Variant 1 is the only variant whose single source can be kept in step on both surfaces with tooling that already runs (`sync-dev` and `verify-sync` cover skills, not `core/`), and the only one that turns every later change (new gate, judge, scale, deliverable kind, stage switch, revert) into a registry row checked by a parametrized test. Its classifier safety details are weaker than Variant 3's and its evidence and root-cause work weaker than Variant 2's; the final spec should keep V1's skeleton (sections 7, 8, 9.2, 11) and graft those parts in.

## Steelman of Variant 2

Strongest form: the wording of `pragmatic.md:225` is only one of six causes (RC1 to RC6). "Preserve the highest severity rating" at `task/SKILL.md:252` (L10) re-creates over-blocking at every 15-reviewer gate whatever the rule says; fix passes that introduce defects (NEW-1, NEW-2) cost a whole cycle a pipe count would have saved; upstream gates have no decision basis, so any "does a decision rest on it" rule is unevaluable there. V2 then measures the guardrail instead of asserting it: Wilson bounds, a "3 divided by n" ceiling, triggers stated as interval bounds, seeded recall, a retrospective escape test. It also caught that the run-2 "25 minutes" is not in the file times and that NEW-1 changed a Destination cell. What it gets right: root cause, evidence labelling, worked cases and statistics; on those four the final spec should copy V2, not V1.

Critique, with counter-evidence:
1. Location. V2 recommends `core/REVIEW-SEVERITY.md` and marks the Makefile and build script [E], unread. L1 and L3 show `core/` gets no project `.claude/` copy (`.claude/WORKER-CONTRACT.md` is absent), so the repo CLAUDE.md dual-surface rule cannot be met there and `verify-sync` never checks it.
2. Its block carries no version marker and no per-carrier stage, so its own staged rollout (stages 2 and 3) cannot be tested as "these files on new text, those on old"; its manifest is a list, the same weakness as the `S1_S3_FILES` tuple (L5).
3. "UNSET means send to a person" is false for S and for D with wrong = N (V-17); `consumer-unknown` as a non-blocking Medium is a loosening V2 itself flags (R2), and its RT7 threshold of 40 percent is a placeholder.
4. Classifier location is left to the plan, so nothing yet stops a primitive from naming package code by a `src/superclaude/` path; V1 5.1 fixes the boundary at a `superclaude review` CLI (click group verified, V-29).

## Steelman of Variant 3

Strongest form: the hard part is not the rule, it is the operations around it. `/sc:issue --create` posts with no dry-run or preview (V-26), so a lost reply after success plus a naive retry files duplicate issues; V3's batch marker plus `prepared`, `posting`, `reconcile`, `filed` states is the only design that is safe to repeat. A ledger written by several gate owners needs one writer, a revision counter and atomic replace. A missing safety answer must never look safer than an uncertain one (the sketch returns FOLLOW_UP for S = UNSET, V-17), `min(pW, pD)` is an upper bound, and a privacy denial must also skip the fallback model. What it gets right: idempotent filing, ledger concurrency, UNSET safety, confidence math, privacy scope, judge contract; I adopt each.

Critique, with counter-evidence:
1. Its "project `.claude/REVIEW-SEVERITY.md` as the explicit development surface" names a file no mechanism creates (L1, L3); V3 admits the plan "must add generation", which means new Makefile and build-script code that V1's location does not need.
2. "Prefer short references plus a rule-version marker" is option B (pure pointer). A reviewer that skips the Read grades from memory; the repo precedent needs a fail-closed sentence (`spec-panel.md:268`, V1 7.2). V3's own rule "a consumer missing the required version retains the old gate" means a carrier nobody updated silently keeps the old meaning, and without a registry nothing lists which carriers those are.
3. Four fixed Markdown tables (Items with 13 columns, Observations, Offers, Filings) multiply the parse risk V3 names (pipes, backticks); V3 says an escaping convention must be chosen but does not choose one.
4. It deliberately picks no classifier path and gives no worked examples or numeric triggers, so it is the least plannable of the three for a `/sc:workflow` step.

## Strengths claimed (Variant 1)

1. Location with both surfaces and free drift checking (X-001, S-005). V1 7.3 picks a delegate-only skill. L1 and L2: `sync-dev` copies every skill folder and `verify-sync` diffs it both ways; L3: the precedent `sc-bare-review` exists in both `src` and `.claude/skills/`; L4: it is already the delegate-only pattern. No other location gets the second surface without new tooling.
2. Registry-driven drift tests (C-005, U-002). Today's copy list is a Python tuple (L5, line 181) and the S5 set is "the first 6" by slice (line 193): a new copy is invisible and a reordering silently changes the S5 set. V1 T1 to T3 parametrize over `refs/registry.yaml`, T2 reverse-scans `src/` and `plugins/` for any fence or legacy P1 sentence, and each row carries `stage` and `digest version`, so mixed-version rollout (K9) is declared and tested, and a revert is "set rows back to v1" (V1 11).
3. Extension contracts (S-008, U-001). V1 8.1 to 8.5: a new gate, judge, scale or deliverable kind is a row plus a contract the existing tests pick up; an unsupported kind leaves D UNSET and degrades to "ask", not "hide" (8.4). Neither other variant says how the design survives its second year.
4. Digest plus pointer (X-002). Grading never depends on a runtime Read (the inline-reliability point V2 also makes), while the full rule, scale map, ledger schema and question module grow in one place instead of eleven. `pragmatic.md` is broadcast to every subagent (V-30, L7), so moving lines 230 and 231 out of it (V1 7.4) cuts context for every agent.
5. A written scale map with a test (U-004, C-018). V1 7.5 maps eleven families onto BLOCKING, FOLLOW_UP, NOTE, including the `card_convert.py:82` versus `rf-qa.md:111` conflict on `important`; T4 fails when a mapped file or label disappears.
6. Package boundary for the classifier (S-007). Four layers with questions as versioned data, thresholds in config, table under property tests, exposed only through a `superclaude` CLI as the repo CLAUDE.md requires for installed primitives.
7. Stage-tagged file list (C-019). V1 9.2 ties each of the 11 P1 carriers (line numbers match V-01) and each group-B file to a rollout stage, the shape a `/sc:workflow` plan needs.

## Weaknesses identified in the others

1. V2 and V3 both pick `core/` and neither reads the Makefile live (V2 marks it [E]); L1 to L3 show `core/` has no project surface and no `verify-sync` coverage.
2. V2's manifest and V3's references have no per-carrier stage or version list, so their staged rollouts are not mechanically testable (L5 shows the tuple pattern they repeat).
3. V2's "UNSET means send to a person" is false (V-17); V2's T2 would pin a rule the sketch does not implement.
4. V2's `consumer-unknown` Medium makes every upstream finding non-blocking until L4 consumer lines exist (V2 R2 admits it).
5. V3's development surface `.claude/REVIEW-SEVERITY.md` does not exist and nothing creates it (L3, V-10).
6. V3's four-table Markdown ledger raises the pipe-escaping risk that produced NEW-1 and NEW-2 (L10) without fixing a convention.
7. V3 leaves the classifier path unchosen and V2 leaves it to "a plan decision": both defer the boundary that decides whether installed primitives stay path-clean.

## Concessions

I accept every V1 item in the diff analysis's "claims found false or overstated", each for the stated reason:
- WORKER-CONTRACT "81 source files": wrong; V-28 gives 58 files (2 `.pyc`). The point it served (core is single-surface) still stands on L3.
- Plugin build "yes" for the skill and `rules/prompts`: overstated; L6 shows the build copies the hand-kept `plugins/superclaude/` tree only. Plugin reach for any location needs a hand mirror plus a parity test (V1 D9, T7).
- NEW-1 and NEW-2 as NOTE examples: wrong; `gate1-cycle-control.md:9` says the Destination cell reads wrong. Under V1's own table-shape rule they are condition 1 when a parser reads that cell; V2 case 6 is the right wording.
- T6 "monotone in every input": wrong across UNSET (432 lowering moves, V-17; L8 line 68). Adopt V2 T2 and V3: monotone on N, U, Y plus a separate missing-input test.

Further concessions: X-006 (V1 used `min(pW, pD)` as the confirm score; V3's `max(0, pW + pD - 1)` is the honest lower bound); X-007 (V1 R1 covers S = U only; S = UNSET must give SHOW_USER, per V3); C-014 (calling the sketch's UNSET handling "more useful" was wrong for S); X-009 (privacy denial must skip the fallback LLM too); X-010 and C-021 (the 25-minute figure is not supported); C-017 (V1 left "highest severity wins" in place; V2 L1 is needed); S-002, S-003, S-004, S-011 (V2's labelling, root cause, examples and statistics are better); C-008, C-011 (V3's ledger identity and idempotent filing are better).

## Shared assumptions

| A-NNN | Verdict | One sentence |
|---|---|---|
| A-001 | QUALIFY | 11 files is right (V-01), but `pragmatic.md:221` also tells every reviewer to hunt "false claims" (L7) and must change with the definition or it re-imports the old meaning. |
| A-002 | QUALIFY | The three conditions are right, but condition 1 is only evaluable where a decision basis exists, so upstream gates need V2's consumer line or V2 GR7's final-gate sweep. |
| A-003 | ACCEPT | `CANONICAL_CAP_TEXT` at test line 215 (L5) pins the cap, and a narrower "blocking" shrinks the loops without touching it. |
| A-004 | QUALIFY | True only if the coordinator reading rule names the ledger counts as something to open (V1 4.4, V2 R5); otherwise an unattended ledger is never read. |
| A-005 | QUALIFY | The rule, ledger and drift tests must not wait for the scored table; only classifier stages gate on it, and the spec needs a branch for a late, small or blocking-only table. |
| A-006 | QUALIFY | Markdown is fine for humans but the schema must fix one escaping convention and a round-trip test (V3), folded into V1 T5. |
| A-007 | QUALIFY | The hook injects the installed file (V-30) but registration in plugin-only installs is unverified, which is why per-carrier digests must stay as the backstop. |
| A-008 | QUALIFY | Unverified by anyone; the plan must check it, and until then M and D fall to UNSET and route to SHOW_USER rather than to a downgrade. |
| A-009 | REJECT | `ORDER` has no UNDETERMINED (L8, line 5); it must be defined as a judge-chain outcome (no usable answer) outside the table, not a table verdict. |
| A-010 | ACCEPT | `pragmatic.md:228` (L7) already exempts `/sc:implement`, and all three variants keep it in v1. |
| A-011 | ACCEPT | No key exists and none may be requested, so shadow-first with `LlmJudge` or fixtures is the only possible start. |
| A-012 | QUALIFY | "Never rechecked inside the loop" is right, but V2 GR7's final-gate sweep and V1 R6's sampled audit are needed so a later fix cannot make a row decision-bearing unseen. |
| A-013 | QUALIFY | The attended `/sc:issue --create @file` path is right (V-26, V-27), but it has no dry-run, so V3's batch marker and reconcile state are needed before any retry. |
| A-014 | REJECT | A new core file or skill installs, but an edited carrier does not: `install_core.py:70` and `install_skills.py:102` (L9) skip existing destinations unless forced, so mixed versions are the default and must be detected. |

## Point table

| Point | Preferred | Confidence | One-line evidence |
|---|---|---|---|
| S-001 | V1 | 60 | V1 0 weights sections 7, 8, 9, 11 that a plan executes; graft V2 sections 2 and 5 into it. |
| S-002 | V2 | 80 | [V]/[E]/[J]/[U] on every statement would have exposed V1's unrun claims (81 count, plugin "yes"). |
| S-003 | V2 | 85 | RC2 is real: `task/SKILL.md:252` "highest severity" (L10); V1 has no cause model. |
| S-004 | V2 | 80 | 14 graded cases, including the correct NEW-1 consumer test V1 got wrong. |
| S-005 | V1 | 75 | Skill folder is synced and verify-synced (L1, L2); `core/` is not (L3). |
| S-006 | V3 | 55 | Items, Offers and Filings carry identity and consent; keep V1's single schema definition and T5. |
| S-007 | V1 | 75 | Four layers behind a `superclaude review` CLI (V-29); V2 and V3 leave the path open. |
| S-008 | V1 | 85 | Only V1 8.1 to 8.5 says how gates, judges, scales and kinds are added. |
| S-009 | V1 | 60 | Registry `stage` per row makes each switch and revert a tested edit; add V2 stage 0b and paired stage-1 data. |
| S-010 | V1 | 60 | T1 to T8 are registry-parametrized; add V3's ledger, filing and stale-install cases. |
| S-011 | V2 | 85 | RT2 as a Wilson lower bound is the only trigger testable at n = 60. |
| S-012 | V2 | 55 | An evidence column per risk beats V1's unsourced likelihood ratings. |
| C-001 | V2 | 70 | Named consumer, "acceptance check" and "stated reasons count" are checkable; V1's wording is close. |
| C-002 | V3 | 70 | "Name the affected action" and "unverified protected risk is not a note" close a gap V1 leaves. |
| C-003 | V2 | 60 | Keeping "Medium" avoids renaming pinned text (8 hits in the mapping test, L11); classifier enum stays FOLLOW_UP. |
| C-004 | V2 | 65 | `rests_on` names a consumer code can check (GR3); keep V1's `why_not_blocking` beside it. |
| C-005 | V1 | 80 | Registry rows replace the hard-coded tuple at test line 181 and the `[:6]` slice at 193 (L5). |
| C-006 | V1 | 55 | A no-question one-liner below D5 cuts noise; add V3's exact ids and set digest. |
| C-007 | V2 | 65 | Mechanical checks and "stop if a picked item proves decision-bearing" are safer than V1 R9 alone. |
| C-008 | V3 | 80 | Run-scoped ids, identity tuple, revision and atomic replace; V1 has none. |
| C-009 | V1 | 55 | Per-family table reuses existing folders and extends by one row (V1 8.1 step 2). |
| C-010 | V3 | 60 | `follow_up_capture_state` makes a failed write visible; merge V1's counts object into it. |
| C-011 | V3 | 80 | `/sc:issue` has no dry-run (V-26); batch marker plus reconcile prevents duplicate issues. |
| C-012 | V3 | 60 | All 10 questions, with T, F, I, G never cancelling S, M or an obligation. |
| C-013 | V2 | 65 | Reviewer-named, code-checked basis; admits upstream inputs have none today. |
| C-014 | V3 | 85 | S = UNSET gives FOLLOW_UP or NOTE in 216 states (V-17); V1's "more useful" was wrong. |
| C-015 | V3 | 70 | Time budgets, circuit breaker and labels hidden from the judge are concrete and testable. |
| C-016 | V2 | 70 | GR7 final-gate sweep and seeded recall measure escapes; V1 R6 is a sample only. |
| C-017 | V2 | 80 | L1 replaces "highest severity wins" (L10); V1 leaves the main over-blocking merge in place. |
| C-018 | V1 | 60 | Written scale map with T4 covers eleven families; adopt V3's caution on tasklist and the contradiction floor. |
| C-019 | V1 | 60 | Each file tied to a stage (V1 9.2); add V3's 120 lines versus 139 occurrences explanation. |
| C-020 | V1 | 55 | V1 alone lists `test_review_rules_text.py:92`, which pins pointer text; add V3's transitive module (union 10). |
| C-021 | V2 | 85 | `stat` times give about 22 minutes for the whole loop (V-23); V1 repeated the 25-minute figure. |
| C-022 | V3 | 55 | Mixed-version detection matters: L9 shows both core and skills skip existing installs. |
| X-001 | V1 | 75 | Delegate-only skill: synced, verify-synced, precedent exists (L1 to L4); plugin line conceded. |
| X-002 | V1 | 70 | Inline digest in a versioned fence plus pointer: V2's reliability with one place to grow. |
| X-003 | V1 | 60 | SHOW_USER attended, reviewer label stands unattended (V1 4.4); matches V3, avoids V2's loosening. |
| X-004 | V2 | 60 | Once per run plus at an escalation halt, where the user is already being asked. |
| X-005 | V3 | 60 | A separate owner decision after audited shadow evidence; V1 pre-commits a stage 4 path. |
| X-006 | V3 | 85 | `jev-uses.md:194` itself says min is an upper bound; V3 gives the lower bound. |
| X-007 | V3 | 85 | `verdict(UNSET,N,N,Y,N,N)` = FOLLOW_UP (V-17); missing safety must route to SHOW_USER. |
| X-008 | V2 | 75 | Counts the 432 lowering moves and requires a separate UNSET test (L8, line 68). |
| X-009 | V3 | 80 | A privacy denial must cover the fallback LLM; V1 D1 sent excerpts to it by default. |
| X-010 | V2 | 85 | File mtimes and the late "12:23" header (V-23) undercut the 25-minute claim. |
| X-011 | V2 | 80 | `gate1-cycle-control.md:9`: Destination cell wrong, so the consumer test decides. |
| X-012 | V1 | 55 | Keep SHOW_USER rows recorded (tag `unsettled`) but outside the non-blocking offer set. |
| X-013 | V1 | 55 | V1's 9 includes the pointer-relevant pin; the correct answer is the union of 10 (V-20, V-21). |
| A-001 | QUALIFY | 80 | `pragmatic.md:221` brief also carries "false claims" (L7). |
| A-002 | QUALIFY | 75 | Condition 1 needs a decision basis that upstream gates lack (V2 RC4). |
| A-003 | ACCEPT | 90 | `CANONICAL_CAP_TEXT` pinned at test line 215 (L5). |
| A-004 | QUALIFY | 75 | The coordinator must be told to open the ledger (V1 4.4). |
| A-005 | QUALIFY | 80 | The diff analysis cites `seed-brief.md:25` (inventory empty); only classifier stages should wait. |
| A-006 | QUALIFY | 75 | NEW-1 was a pipe defect (L10); the ledger needs an escaping convention and round-trip test. |
| A-007 | QUALIFY | 70 | Hook verified (V-30); registration elsewhere unverified, so keep per-carrier digests. |
| A-008 | QUALIFY | 65 | Not checked by anyone (UNVERIFIED); unknown routes to SHOW_USER. |
| A-009 | REJECT | 85 | `ORDER` at sketch line 5 has no UNDETERMINED (L8). |
| A-010 | ACCEPT | 90 | `pragmatic.md:228` exemption (L7). |
| A-011 | ACCEPT | 85 | No key; shadow with fallback judges only. |
| A-012 | QUALIFY | 75 | Needs V2 GR7 sweep plus V1 R6 audit. |
| A-013 | QUALIFY | 75 | No dry-run (V-26); needs V3's batch marker. |
| A-014 | REJECT | 85 | `install_core.py:70` and `install_skills.py:102` skip existing files unless forced (L9). |
