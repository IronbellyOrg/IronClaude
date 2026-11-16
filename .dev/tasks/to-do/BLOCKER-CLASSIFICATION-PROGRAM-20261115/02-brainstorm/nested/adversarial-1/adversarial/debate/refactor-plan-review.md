# Independent review of refactor-plan.md

Status: complete. Reviewer wrote only this file. No git write, nothing sent to GitHub, no Jev or TypeSafe call. Reviewer did not write the plan or any variant.

Paths below are relative to the repo root `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel` unless stated. F = the adversarial folder `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/nested/adversarial-1/adversarial/`. PC-nn, BW-nn, LC-nn, INV-nnn, OD-nn are the plan's own ids.

## Summary

- BLOCKING: 3 (RB-1, RB-2, RB-3).
- MINOR: 15 (RM-1 to RM-15).
- Coverage (check 1): all 28 V1 or V3 winner points are mapped to a planned change. Two of them drop a V3 element without a stated reason (RM-1).
- Invariants (check 2): all 38 rows are present. Of the 9 HIGH UNADDRESSED rows, 6 have a concrete, testable requirement or owner decision (INV-007, 008, 009, 015, 023, 027; notes in RM-5 to RM-7, RM-11, RM-12). INV-001 leans on a mechanism that does not exist (RB-1), INV-034 is incomplete (RB-2), INV-026 carries a wrong target (RB-3).
- Live facts (check 4): 20 fact rows re-checked, covering well over 8 repo facts. 17 hold as stated, 2 are incomplete (rows 10 and 11, RM-14 and RM-4), 1 does not hold (row 18, RB-1).

## 1. Coverage of V1 and V3 winners

The 28 points whose winner in `F/debate/scoring-matrix.md` is V1 or V3, each checked against the plan's "Coverage check" table and the planned change it names:

| Winner | Points and plan mapping |
|---|---|
| V3 (19 points) | C-002 PC-07; C-006 PC-19; C-007 PC-20; C-008 PC-16; C-009 PC-18; C-010 PC-22; C-011 PC-21; C-014 PC-09; C-015 PC-12; C-019 PC-23 and BW-14; C-022 PC-04; S-006 PC-16; X-003 PC-08; X-005 PC-14; X-006 PC-11; X-007 PC-09; X-009 PC-13; X-012 PC-19; X-013 PC-26 |
| V1 (9 points) | C-005 PC-03; C-018 PC-25; C-020 PC-26; S-005 PC-01; S-007 PC-15; S-008 PC-25; S-010 PC-03 and PC-26; X-001 PC-01; X-002 PC-02 |

Count check: 19 plus 9 is 28. By prefix: C 14 (C-002, 005, 006, 007, 008, 009, 010, 011, 014, 015, 018, 019, 020, 022), S 5 (S-005, 006, 007, 008, 010), X 9 (X-001, 002, 003, 005, 006, 007, 009, 012, 013). All 28 are in the plan's table. None is missing. Each mapped PC was read against the point's matrix evidence and carries it. The plan also states its partial exclusions with reasons (S-006 always-present tables, C-015 budgets as guarantees, C-010 six keys).

RM-1 (MINOR) is the only mapping defect: C-009 and C-010 each lose a V3 element with no stated reason (see below).

## 2. Invariants

All 38 INV rows are in the plan's "Invariant resolutions" table (Grep `^\| INV-0nn \|` gives 40 hits: 38 table rows plus INV-011 and INV-026 repeated in "Changes NOT Being Made"). The tallies match the probe (ADDRESSED 14, UNADDRESSED 24, HIGH 9).

Each of the 9 HIGH UNADDRESSED rows:

| INV | Resolution | Concrete and testable? | Verdict |
|---|---|---|---|
| INV-001 | PC-04 (a) to (e) | (a) to (c) yes, checked against `install_skills.py:102-104` and `install_user_setup.py:77-78,196-197`. (d) names a brake that does not exist (RB-1). (e) is a choice between two tools and does not say which registry it reads (RM-10) | RB-1, RM-10 |
| INV-007 | PC-09: `wrong()` reads a missing partner as U | yes; reproduced: `verdict(N,N,N,N,UNSET,Y)` is SHOW_USER | pass |
| INV-008 | PC-10 GR12 upgrade-only route | yes (tag, attended and unattended behaviour, counted key); authority and absence gaps in RM-5 | pass, RM-5 |
| INV-009 | PC-08 default keeps the label; OD14 for deferral with three stated preconditions and a seeded test | yes; OD14 has a recommendation | pass, RM-6, RM-7 |
| INV-015 | PC-23: 13 lines in 10 files, staged, reverse scan | yes; the count reproduces (section 4 row 1) | pass |
| INV-023 | PC-17 entity codec and fixtures | yes; the codec round-trips by inspection (`&` first on encode, `&amp;` last on decode); fence gap in RM-12 | pass, RM-12 |
| INV-026 | PC-21 OD15 plus a floor (posted body byte-equal to the approved body, marker present, else `reconcile`) | the floor is testable; the recommended command carries a hard-coded repository (RB-3); the size bound is unnamed (RM-13) | RB-3, RM-13 |
| INV-027 | PC-06 precedence sentence in every v2 digest and `pragmatic.md` | the text is testable (registry test); the behaviour measure points at the wrong metric (RM-11) | pass, RM-11 |
| INV-034 | PC-24 | rewrite or keep as a named mechanical gate, with M12 as falsifier, is testable; the inventory omits a verbatim-pinned floor in the same pilot family (RB-2) and several rf-qa lines (RM-14) | RB-2, RM-14 |

No resolution uses "should consider" wording. Two rows conflict with another change: INV-001 (d) with PC-06 (RB-1), and INV-008 with INV-011 (RM-5).

## 3. Internal contradictions between planned changes

| # | Topic | Position A | Position B | Grade |
|---|---|---|---|---|
| C-1 | Where a reviewer-blocking finding with no nameable consumer is recorded | PC-08: "A finding whose consumer cannot be named keeps the reviewer's label, is tagged `consumer-unknown`, counted separately and listed first in the offer." | BW-12: "one naming none goes back to the reviewer once (GR2); still none: the label stands, tag `disputed`, listed first" | MINOR (RM-2) |
| C-2 | Whether `unsettled` rows are in the offer | PC-19: "`unsettled` rows are counted apart from confirmed non-blockers and kept out of their offer set." | PC-30: "the row is tagged `unsettled` and shown first in the end-of-run offer"; PC-08: `consumer-unknown` rows "listed first in the offer" | MINOR (RM-3) |
| C-3 | Counting `consumer-unknown` and `unsettled` rows | PC-08 and PC-19 say each is "counted separately" or "apart" | PC-22 fixes three keys, `follow_up_counts {follow_up, note, show_user}`, with no slot for either | MINOR (RM-3) |
| C-4 | Classifier authority | PC-14 and PC-28: "Own-scale adapters and classifier authority are owner decisions, not stages"; PC-30: "With no classifier authority (PC-14)" | PC-10: a judge answer S = Y or U on a non-blocking row forces a person prompt (attended) or `worker_status: partial` (unattended), "active in every stage including shadow" | MINOR (RM-5) |
| C-5 | Attended halts | PC-30: "SHOW_USER never halts an attended run in version 1" (INV-011, person away) | PC-10: attended rows "shown to the person before the gate passes", with no absence rule, so INV-011's concern returns through PC-10 | MINOR (RM-5) |
| C-6 | The digest rule against unknown consequence | PC-02 digest is V2 4.1 ("A finding is **Blocking** only when at least one of these holds") plus "Unknown is not no" | PC-08: an unknown-consumer finding "keeps the reviewer's label", so a finding can block with none of conditions 1 to 3 shown to hold; the exact digest sentence is not given and the digest is pinned word for word | MINOR (RM-6) |
| C-7 | Option Q for upstream gates | "Decisions settled": V2's "option Q for upstream gates kept" (V2 7.2: Q is "the finding names a specific later reader", it replaces D) | PC-02 and PC-09: "Unknown is not no"; a finding that names no reader gives Q = N, read as D = N, which lands in FOLLOW_UP in the table | MINOR (RM-7) |
| C-8 | Offer cadence across stages | PC-19 and PC-28 stage 2: the task skill and tech-research make a once-per-run offer | `pragmatic.md:230` still tells the top-level session to ask "once per loop" until stage 3 moves it, and `tests/skills/test_review_severity_mapping.py:72,128` pin that text | MINOR (RM-8) |

No contradiction found on: ledger location (PC-18 replaces V2 6.6 and nothing else states a path), number of classifier questions (six everywhere; sketch line 43 `verdict(s, m, c, w, e, d)`; PC-09, PC-11, BW-15 and "Decisions settled" agree), order of stages 0 to 4 (PC-04, PC-05, PC-08 OD14 and PC-28 agree), or who may enable intermediate deferral (OD14 only). Checked by reading every PC that names these positions.

## 4. Live fact checks

All against the live tree on 2026-11-15. "Holds" means the plan's statement is right as written.

| # | Plan statement | Check | Result |
|---|---|---|---|
| 1 | LC-04: "highest severity wins" is 13 lines in 10 files | Grep `highest severity\|more severe` over `src/superclaude`, then Grep with `-o` for the verb phrase | Holds. 13 hits: `task/SKILL.md:252,361`; `tech-reference/SKILL.md:510,513`; `readme/SKILL.md:542,547`; `tdd/refs/build-request-template.md:122`; `operational-guide/SKILL.md:511`; `rf-qa.md:83`; `rf-qa-qualitative.md:84`; `rf-analyst.md:75`; `agent_template_qa.md:85`; `agent_template_analysis.md:466`; 10 distinct files. Plus `sc-auggie-review-protocol/SKILL.md:228`; `plugins/superclaude` 0 hits. Task-builder and tech-research have none. PC-23's stage split (5 and 8) adds to 13 |
| 2 | LC-05: 11 files, 11 occurrences of the grade sentence | Grep count | Holds |
| 3 | BW-14: "22 files, 120 matching lines, 139 occurrences" for `2 fix cycles` | Grep count plus `grep -rF` line, occurrence and file counts | Holds (139, 120, 22) |
| 4 | PC-26: 11 test modules | Glob for the 11 names | Holds; all 11 exist; `test_spec_panel_review_loop.py:15` imports `CANONICAL_CAP_TEXT`; `test_review_rules_text.py:92` has `"src/superclaude" not in TEXT`; `test_review_severity_rule.py:181-193` has `S1_S3_FILES` and `S5_FILES = S1_S3_FILES[:6]` |
| 5 | LC-10 and OD15: the `/sc:issue` flow | Read `commands/issue.md:19,21,25,40-42,46`, `sc-issue-protocol/SKILL.md:72-76`, `refs/create.md:61` | Holds: posts directly, body never shown for approval, explicit only, no `--repo`, dry-run or preview option, rule 10 still governs other filing. It also resolves the repository from `origin` only (RB-3) |
| 6 | LC-06, LC-07, LC-08: installers skip existing files | Read `install_skills.py:100-104`; Grep `install_user_setup.py`, `install_core.py` | Holds: 102-104; 77-78, 117-118, 186-197; 58, 70. The skill installer's `sc-` handling (`install_skills.py:40-59`) would not remove `sc-review-severity` (there is no `commands/review-severity.md`) |
| 7 | LC-09: the injection hook | Read `hooks.json:169-177`, `hooks/scripts/pragmatic-subagent.js` | Holds: line 173; script lines 7, 15, 21; `plugins/superclaude` has no `pragmatic` match |
| 8 | LC-11: worker contract lines | Read `WORKER-CONTRACT.md:14-55` | Holds: 23 (never-as-worker includes `/sc:issue`), 31 (WC-2), 33 (top-level keys), 34 (ignored paths), 36 (mapping), 39, 47 |
| 9 | LC-12: `pragmatic.md` lines | Read `pragmatic.md:216-233` | Holds: 221, 225-231 |
| 10 | LC-13: `rf-qa.md` FAIL lines | Grep | Holds for the listed lines (152, 162, 168-170, 182-183, 327, 389, 476); the list is incomplete (RM-14) |
| 11 | LC-01, LC-02: sketch figures | `uv run --no-project python` on the sketch plus an import probe, no bytecode | Holds: `cases 6400 ... 0 ... 0`; BLOCKING 3,664, SHOW_USER 2,664, FOLLOW_UP 56, NOTE 16; both the INV-007 and X-007 cases give SHOW_USER; 0 states with S, M or C at U or UNSET below SHOW_USER; 256 of 26,880 UNSET-to-Y/U/N moves lower the verdict, 240 of them to N. Incomplete: UNSET to NA adds 72 of 2,560 (RM-4) |
| 12 | LC-15: Makefile | Read `Makefile:108-182` | Holds: skill folders synced whole when `SKILL.md` exists (112-125); commands to `.claude/commands/sc` (132-136); no `core/`, `rules/`, `output-styles/`; `diff -rq` per skill (178) |
| 13 | LC-17: codec readers | Grep `split("|")` in `cli/review` | Holds: `card_convert.py:250`, `telemetry.py:162` |
| 14 | LC-18: tasklist and reflect | Grep, Read | Holds: 7 tasklist lines (1439, 1450, 1531, 1567, 1571, 1610, 1614); reflect line 1540 |
| 15 | LC-16, LC-20, LC-21, LC-22 | `ls`, Grep | Hold: five spec-panel variants installed only; `src` has `spec-panel.md` only; `sc-review-severity` absent; plugin has 4 skills; `.gitignore:250` `.dev/pr-monitor/`; MDTM defined at `CLAUDE.md:80` and `HOW-WE-WORK.md:18` |
| 16 | LC-14: no final gate reads a ledger | Read `task/SKILL.md:286-297`, `tech-research/SKILL.md:410-421` | Holds: the final validation (290-292) and Gate 5 (415-419) name no ledger |
| 17 | LC-03: `jev-uses.md` lines | Read 137-150, Grep | Holds: 139, 149 (new missing-answer rules), 195 (`min(pW, pD)`), 206 ("never silently upgrades"), 277 |
| 18 | PC-04 (d) and V2 GR11: the grading-override file mechanism "keeps working" | Grep `grading-override` under `src/` and `tests/` | Does NOT hold as a mechanism: no shipped file reads it (RB-1) |
| 19 | PC-15: the `review` click group | Read `cli/review/__init__.py:14-36` | Holds. The group already has `ledger_cmd` and `merge_cmd` (RM-15) |
| 20 | PC-24: `tests/audit/test_nfr_conv_9_zero_trust.py` and its transitive importer exist | Glob | Files exist; contents not re-read |

## Findings

### Blocking

**RB-1 (BLOCKING). The immediate revert brake in PC-04 (d) rests on a mechanism no shipped file implements.**
PC-04 (d): "the immediate brake that needs no reinstall is the per-run grading-override file (V2 GR11), and RT1 acts through it first". INV-001 (HIGH) asks how a safety revert reaches installed machines, and this is the only no-reinstall answer. Evidence: Grep `grading-override` over `src/` and `tests/` finds nothing. The file existed only inside run 2's folder (`TASK-RESEARCH-review-panel-run2-20261114-075454/qa/grading-override.md`), written by the orchestrator and handed to reviewers by hand. V2 GR11 (`F/variant-2-sonnet-analyzer.md:403`) marks it "[V]" because the file exists, not because anything reads it. Three gaps: nothing says which prompts name the file, who writes it, or its format; run 2's file loosened grading, while a safety revert needs the old, stricter definition; and PC-06 says the instructions of the agent, skill or command win over other text, so an override file that is not part of a carrier loses to the carrier. A plan that follows PC-04 would ship RT1 ("any safety-class escape") with no working action behind it.
Fix: either specify the override (path under the run report directory, format, the one sentence every carrier digest carries to read it, and its precedence over the carrier in PC-06), or drop (d) and state that the only brake is the three-step revert, with the install check as detection.

**RB-2 (BLOCKING). PC-24 omits a fixed severity floor in the pilot family that a test forbids softening.**
PC-24 inventories only `rf-qa.md` lines. The stage 3 pilot is "`pragmatic.md` and the rf-qa family" (PC-06, PC-28), and `rf-qa-qualitative.md` is in that family. `src/superclaude/agents/rf-qa-qualitative.md:990` Rule 6 reads "Contradictions are always IMPORTANT or CRITICAL ... that's never minor". IMPORTANT is blocking there, so a contradiction that nothing rests on must block, against the new rule "the label is information, never the grade". `tests/audit/test_severity_floor_unweakened.py:57-61` pins Rule 6 verbatim ("with no softening verbs") and hashes the whole Critical Rules block. The same text is in `templates/documents/agent_template_qa.md:333` (stage 4). PC-26 lists that test among the 11 pins, but no PC says what happens to Rule 6 or whether the owner re-pins a test named "severity floor unweakened". Result: either M12 (rf-qa FAIL counts flat) is falsified by design, or the stage 3 edit fails the pin.
Fix: add `rf-qa-qualitative.md:990` and `agent_template_qa.md:333` to PC-24 with a stated decision: keep as a named mechanical gate mapped to a condition, or rewrite and re-pin as an owner decision with a recommendation.

**RB-3 (BLOCKING). PC-21 and OD15 hard-code the repository, against the one existing mechanism and the installed-primitive rule.**
PC-21 recommends `gh issue create --repo IronbellyOrg/IronClaude ...` and its title says "fork only"; the INV-013 row says "stop when origin is not the fork". The rule ships to `~/.claude` of other projects (`02-brainstorm/seed-brief.md:31`, repo `CLAUDE.md` rule on installed primitives). `sc-issue-protocol/SKILL.md:72` resolves `<R>` from `origin` only ("Nothing else is consulted"), and line 191 forbids touching any other repository. As written, in any project other than this fork the feature either cannot file (the stop guard) or, if an agent copies the literal command, posts that project's review findings into the IronClaude tracker. The spec has no owner decision limiting filing to this repository.
Fix: write the target as `<R>` resolved from `origin` (reuse `sc-issue-protocol/scripts/origin_repo.py`), keep the explicit `--repo <R>` and `repos/<R>/...` forms, and add a separate guard: when `<R>` is the IronClaude repository it must be `IronbellyOrg/IronClaude`, never the upstream parent. Or record as an owner decision that follow-up filing is IronClaude-only in version 1.

### Minor (recorded as notes)

- **RM-1.** Coverage gap: V3 rules for C-009 and C-010 are not carried. V3 `variant-3-haiku-backend.md:97-98` fixes the ledger path "before dispatch", line 266 says "Nested ledgers appear through nested contracts; do not double-count them", and line 259 says to list the ledger in `artifacts` only "when eligible under existing tracked-path rules". The plan text has no match for "nested". `core/WORKER-CONTRACT.md:24` (nested report directories) and `:34` (ignored paths stay out of `artifacts`) make these real cases for the task skill. Add one sentence each to PC-18 and PC-22.
- **RM-2.** Two tags for one state: `consumer-unknown` (PC-08) and `disputed` (BW-12) for a blocking label with no consumer after one re-ask. V2 metrics M6 and M8 count them as different shares. Pick one tag.
- **RM-3.** Offer-set membership of `unsettled`, `consumer-unknown`, `disputed` and `protected-risk-dispute` rows is stated three ways (C-2), and PC-22's three counters have no slot for the separate counts (C-3). State one table: tag, in the consent set or not, which counter.
- **RM-4.** PC-09 states the 16 remaining lowering moves but not that UNSET to NA on M or C adds 72 more lowering moves out of 2,560 (reproduced). NA comes from a declared deliverable kind, so these are intended, but "never when an extractor failed" has no test. Add one: NA is reachable only from the deliverable-kind declaration, never from `tri(q, None)`.
- **RM-5.** PC-10 gives a judge answer upgrade power in shadow without an owner decision, and an attended prompt without an absence rule (C-4, C-5). Add one sentence to PC-14 naming PC-10 as the only exception, and an absence rule for an unreachable person (record, mark `partial`, do not wait).
- **RM-6.** The digest sentence for unknown consequence is not drafted (C-6). The digest is pinned word for word (A-003), so the plan should supply the sentence, for example "if no consumer can be established, keep the reviewer's own label and tag the row".
- **RM-7.** Option Q (V2 7.2) maps "no reader named" to N, which conflicts with "Unknown is not no" (C-7). Shadow only, so it costs measurement, not safety. Read Q = N from a failed lookup as UNSET.
- **RM-8.** The stage 2 per-run offer against the broadcast's "once per loop" and its two pins until stage 3 (C-8). Move the cadence change and its pins into stage 2, or make the stage 2 offer replace, not add to, the broadcast ask.
- **RM-9.** PC-28 gives no stage to the GR7 final-gate sweep (V2 8.1; PC-08 OD14 and the A-012 row depend on it) or to the `core/WORKER-CONTRACT.md` edit (PC-22). Assign both.
- **RM-10.** PC-04 (e) offers "a `superclaude review` subcommand or a `make doctor` check, named by the plan" and does not say which registry it reads. An installed `registry.yaml` is as stale as the carriers (the whole skill folder is skipped once present, `install_skills.py:102`), so the check must read the packaged registry. Name one tool and one source.
- **RM-11.** PC-06 says blending is "measured by M10 split by carrier version", but V2's M10 is classifier agreement (`F/variant-2-sonnet-analyzer.md:580`). Use a new metric or drop the claim.
- **RM-12.** PC-17: the fenced evidence block is verbatim, so evidence that itself contains a triple-backtick line closes the fence early. The fixture list names pipes, backticks, entities, Unicode and multiline text but not a fence line. Add a fence-length rule and a fixture.
- **RM-13.** PC-21: "one-issue filing" but "above a size bound the body is split into parts sharing the batch id" (several issues or comments?), and the bound has no value. Name the bound, say whether parts are comments or issues, and require reconcile to find all parts.
- **RM-14.** PC-24's `rf-qa.md` list is not complete. Same-class fixed FAIL lines also exist at 221 ("Generic steps ... = FAIL"), 316 ("Missing fields = FAIL"), 333 and 334 (count mismatch "that's a FAIL"), 494 and 548. Some may stay as mechanical gates, but the plan should say the inventory is a frozen Grep, not a remembered list (PC-28 stage 0 "re-run every Grep" is close; name the pattern).
- **RM-15.** PC-16 and PC-17 design a new ledger writer and reader and never mention the existing typed finding ledger `src/superclaude/cli/review/ledger.py` (schema `review-ledger/1`, atomic `save` at lines 52-60), its `review ledger` command (`cli/review/__init__.py:19-36`) or the `sc-review-ledger` skill. State reuse, extension or a deliberate separate format, and avoid a name clash with PC-15's new `review` subcommand.

## Checks with no finding

- Number of classifier questions: six (S, M, C, W, E, D) in PC-09, PC-11, BW-15, "Decisions settled" and the sketch. No plan text says ten or four except as a rejection.
- Ledger location: PC-18 is the only statement; LC-21 and LC-11 (`.gitignore:250`, `WORKER-CONTRACT.md:34`) support the two exceptions.
- Stage 3 entry condition: single (PC-28), consistent with PC-08 OD14 and PC-05.
- Who decides intermediate deferral: only OD14.
- Invariant table: no row marked ADDR whose cited change is missing; INV-029 and INV-036 carry RISK plus OD as stated.
