# Round 2 advocate: Variant 2 (sonnet, analyzer)

- Round: 2 of 2 (rebuttals; this advocate goes second, after advocate 1). Variant defended: `variant-2-sonnet-analyzer.md` (V2). Others: V1 = opus architect, V3 = haiku backend, DA = `diff-analysis.md`, A1 and A3 = the other advocates' files in this folder.
- Status: complete. Nothing else was edited. Paths are relative to the repo root unless stated. New live checks are N1 to N7 (section 3); Q-numbers are criticisms (section 1).

## 1. Responses to criticisms of Variant 2

Raised by A1 (rounds 1 and 2), A3 (round 1) and DA. "Conceded" means the final spec should not keep V2's text.

| # | Criticism (raised by) | Answer |
|---|---|---|
| Q1 | "UNSET means send to a person" is false (DA X-007, A1, A3) | Conceded in R1. N2 below sizes it: of 2,368 states with S, M or C unset, the sketch lowers 336 below SHOW_USER. The fix is a rule, not the sentence. |
| Q2 | `core/REVIEW-SEVERITY.md` has no `.claude/` copy and no `verify-sync` coverage (A1, A3, DA) | Conceded in R1; A1's N5 holds (`Makefile:178` runs `diff -rq` over each skill folder). Final location is the skill folder. |
| Q3 | My drift manifest is a list with no per-carrier version or stage (A1 R1) | Conceded. My staged rollout cannot be tested as "these files new, those old" without a row per carrier. A1's `registry.yaml` is the fix; N6 changes where its paths point. |
| Q4 | `consumer-unknown` as non-blocking Medium is an unsafe unknown branch (A1, A3) | Partly conceded. A later sweep is mitigation, but GR7 is a code check (does the flawed text appear uncorrected in the final decision-basis sections), not a re-read, and the final gate exists where it matters (N3). The tag stays only for intermediate gates with a guaranteed sweep, never for conditions 2 or 3, never at the last gate. A3's "keep the old label" keeps run 2's over-blocking at the five upstream gates that caused it. |
| Q5 | L1 ("undecidable dispute is Medium `disputed`") conflicts with GR5 ("blocking stands unless code disproves the consumer") (A3 weakness 6) | Conceded: V2 contradicts itself. Resolution: the rule already requires a blocking finding to name its condition and evidence. A blocking grade that names a consumer and is not disproved by code stands. One that names none is invalid and becomes `disputed` Medium. Nothing is demoted for missing evidence, which is A3's rule. |
| Q6 | `accepted-blocker` at the cap is an automatic pass (A3 weakness 6) | Rejected. L3 offers it as one of three choices to a person at the escalation halt. Under `--unattended` a gate resolves by default, flag or `blocked` (`WORKER-CONTRACT.md` WC-2), never by the consolidator. |
| Q7 | Ledger key "location plus quote hash" breaks when a line moves; no single writer, revision or atomic replace (A3, A1) | Conceded. V3's identity tuple, revision counter and atomic replace replace my key. |
| Q8 | Filing as Option A has no recovery after a lost reply (A3, DA C-011) | Conceded. `issue.md` has no preview or dry-run (DA V-26) and one filing covers many rows, so state is per batch. My per-row `status` and `issue` columns cannot show "posting, reply lost". V3's batch marker and states are needed. |
| Q9 | `resolve now` runs a fix agent with no re-review (A3 C-007) | Conceded on my own evidence: RC3 says fix passes cause new defects (NEW-1, NEW-2) and L2 catches only mechanical ones. Resolve-now becomes separately authorized normal work (V3) with its own gate; a one-location mechanical fix may use L2 checks only. |
| Q10 | Privacy: D3 "else use the LLM judge only" (A3 weakness 4) | Conceded. A privacy denial covers every external judge not separately approved (V3 5.4). |
| Q11 | D8 on the `qa.md` four answers is not answered (DA coverage) | Conceded. Answer: the classifier does not fill them in v1 (A-010, `pragmatic.md:228`). |
| Q12 | D4 says "never auto-downgrades" but stage 4 allows classifier gating (my own text; A1, A3 on X-005) | Conceded. `variant-2:561` lets stage 4 gate on classifier output after two clear windows, which D4 forbids. Take V3's wording: authority is a separate owner decision. |
| Q13 | `[E]` claims: "highest severity" also in task-builder and tech-research; WC-4 line 35 "allows extra keys" | Both retracted (N4, N5). |
| Q14 | RT7 40 percent is a placeholder (A1) | Agreed; the spec text says "set from stage 1 data", no number. |
| Q15 | Classifier path left to the plan (A1 S-007) | Conceded: the plan must reach classifier code only through a `superclaude review` CLI (repo `CLAUDE.md` bars `src/superclaude/` paths in primitives). |

## 2. Updated assessment of Variants 1 and 3

- V1: A1 conceded most of its 17 listed criticisms, including the ones I weighted most (monotone claim, "highest severity", stage 4, UNSET, six questions). What remains is real: the skill-folder location, the registry, the CLI boundary, the fenced digest. I withdraw my R1 weakness on extension contracts as far as A1 narrowed it (a paragraph, no code) and my claim that V1 switches the rule before evidence exists: V1 stage 1 edits no carrier (`variant-1` section 11). What V1 still lacks is paired `rests_on` data before the switch, which A1 accepts.
- V3: A3 conceded X-001, X-002, S-003, S-004, six questions and the uncalibrated numbers, which removes most of my objections. V3's strongest parts (identity, batch filing, UNSET policy, privacy scope, judge contract) are right and I adopt them. Still weak: no worked examples, "retain the old label" at every unknown gate, and its non-blocking bound `1 - min(1, pS + pM + pC + ...)` goes to zero with four mid-sized terms. A3's 90 to 95 confidence figures are higher than a design preference with no run data supports.
- A1's rebuttal moved toward V2 on S-009, C-012 and X-004; I move toward V1 and V3 on location, ledger, filing, privacy and authority. What remains open is small and listed in section 3.

## 3. New evidence (live checks this round)

- N1. NEW-1's real defect is "unescaped `|` inside a backticked command, 8 pipes instead of 7" (`.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/gate1-cycle-control.md:9`). The repo already writes `\|` in cells (`src/superclaude/mcp/MCP_Tavily.md:54-57`), so A1's escaping convention is right. But five Python files split a table row on a bare `|` (`compression.py`, `cli/sprint/config.py`, `cli/roadmap/gates.py`, `cli/roadmap/cosmetic_remediator.py`, `cli/roadmap/spec_parser.py`; Grep), so a ledger reader that splits naively mis-splits `\|`, and my L2 pipe-count check must count unescaped pipes only. Grep finds no pipe-count text in `src/` today, so L2's check is new code.
- N2. Sketch run (`uv run python`, import of `blocker_truth_table_sketch.py`): 2,368 of 4,096 states have S, M or C UNSET and the sketch lowers only 336 of them below SHOW_USER (S answered but M or C UNSET: 1,344 states, 120 lowered). A1's rule "unset S, M or C never yields FOLLOW_UP or NOTE" changes 8.2 percent of states, not a flood.
- N3. Final gates exist where `consumer-unknown` would be used: `task/SKILL.md:290` (after the last phase gate and before Done, a final validation pass) and `tech-research/SKILL.md:415` (Gate 5, "MANDATORY at every intensity"). A1's precondition for the tag (a guaranteed later sweep) holds for those two families.
- N4. `core/WORKER-CONTRACT.md:34-35` has no rule that consumers tolerate unknown return keys; line 35 says a command keeps its own fields and adds the worker fields beside them, the reverse direction. My reading in V2 was wrong; new keys need an explicit contract edit.
- N5. Grep `highest severity` (case-insensitive) under `src/superclaude`: `skills/task/SKILL.md:252` and `:361`, `skills/tech-reference/SKILL.md:513`, plus an unrelated `cli/pipeline/fmea_classifier.py`. None in task-builder or tech-research. L1's file list becomes these three.
- N6. A1's registry sits in the skill folder, which installs to `~/.claude/skills/`. `src/superclaude` already appears in 52 files under `skills/` (grep -rl) and the repo `CLAUDE.md` check says to justify each hit. Registry rows should hold install-root-relative paths (`skills/task/SKILL.md`, `output-styles/pragmatic.md`) so one row resolves in `src/`, `~/.claude/` and `.claude/`. The pin at `tests/review/test_review_rules_text.py:92` covers one prompt file only, so it does not forbid this either way.
- N7. Plugin carriers: Grep finds no "pragmatic" under `plugins/superclaude/hooks`, and `src/superclaude/hooks/hooks.json:173` registers the hook in the source tree (confirms A1's N1).

**A1's convergence proposal, item by item.** Accept: item 1 (skill folder, fenced digest plus pointer, registry, wrong-version carrier keeps its old gate, plugin hand mirror), item 4 (six questions, T F I G optional), item 5 (blind audit, strata, seeded recall, Wilson triggers, protected-risk review) and most of item 6. Change: item 1, registry paths per N6. Item 2, accept the UNSET rule (N2) and the narrow `consumer-unknown` condition (N3), with one added line: at the last gate an unknown consumer keeps today's label. Item 3, add three things: escaped `\|` only with one shared reader and writer (N1); verbatim evidence quotes in an id-keyed fenced block below the table, not in a cell (the NEW-1 defect class is free text in a delimited cell); worker keys cut from six to three (N4: every key is a contract edit, and a worker never offers, so `follow_up_offer_state` has no writer). Item 6, if the scored table is late, stage 0c (paired re-grade of the table) cannot run, so stage 3 needs 0b plus at least 5 shadow runs, not "0b and 0c".

## 4. Convergence proposal (one position per open topic)

1. **Rule location and copies.** Delegate-only skill `sc-review-severity/` holds the rule. Each carrier holds one fenced, version-marked digest inline (V2's paragraph plus "name the affected action" and "unknown is not no") and one pointer line to the installed path, never a `src/` path. `refs/registry.yaml` lists carriers by install-root-relative path with kind, stage and digest version; tests (digest equality, reverse scan of `src/` and `plugins/`, pointer order) run over it. A loop pins its rule version in the ledger header; a carrier at the wrong version keeps its old gate and reports a mismatch.
2. **Unknown consequence and UNSET.** Classifier: an unset or unsettled S, M or C, or a wrong-by-D path with D unset, goes to SHOW_USER (attended) or "reviewer label stands, row tagged `unsettled`" (unattended); UNDETERMINED is a judge-chain failure outside the table. Reviewer: `consumer-unknown` Medium only for condition 1, only at an intermediate gate, only when the final-gate sweep GR7 is guaranteed to read the row; otherwise the old label stands. Conditions 2 and 3 never.
3. **Ledger contract.** One `follow-ups.md` per run at V3's one path rule (implement keeps `notes.md` with a pointer row; pr-submit keeps its own list, and its `.dev/pr-monitor/` is gitignored at `.gitignore:250`). Header: V3 metadata. Items table (identity tuple, `rests_on`, `nonblocking_basis`, tags) plus V2's short Notes table; Offers and Filings records created on first use, filing state per batch (V3). Single writer, atomic replace, escaping as in section 3. Worker keys: `follow_up_ledger`, `follow_up_counts {follow_up, note, show_user}`, `follow_up_capture_state`.
4. **Classifier questions.** Six decisive (S, M, C, W, E, D) with S reworded; T, F, I, G only as optional explanations in shadow; versioned in `refs/classifier-questions.md`.
5. **Guardrail measurement.** V2's design (blind auditor with no rule text, strata with oversampling, seeded recall, the 0b escape test, Wilson-bound triggers, RT1 zero tolerance for safety) plus V3's review of every protected-risk disagreement and GR7. Every rate is reported with its n.
6. **Rollout.** 0 measure (0a, 0b, 0c when the table exists); 1 scaffold, registry all `legacy`, no carrier edited; 2 shadow with the old rule deciding, ledger and offer live, reviewers also emit `rests_on`; 3 pilot (`pragmatic.md`, rf-qa family, L1 over the three lines in N5, L2); 4 propagate and plugin mirror. Own-scale primitives and any classifier authority are separate owner decisions, not stages.

## 5. Updated point table

Asterisk = preference changed from my Round 1, reason in the evidence cell. Confidence is in the design preference, not a measured probability.

| Point | Preferred | Confidence | One-line evidence |
|---|---|---|---|
| S-001 | V2 | 55 | Cause and examples first, but A1 is right that V1's sections 7, 8, 9, 11 are what a plan executes; graft both. |
| S-002 | V2 | 70 | Tags work, but my `[E]` on WC-4 and on "highest severity" in two skills were wrong (N4, N5); labels need a recheck. |
| S-003 | V2 | 92 | RC2 is wider than I said: three lines (N5). |
| S-004 | V2 | 88 | 14 graded cases; only V2 applies the rule to real Gate 1 rows. |
| S-005 | V1 | 85 | Raised from 58: `Makefile:178` whole-folder `diff -rq`; all advocates agree. |
| S-006 | V3* | 52 | Changed: one filing covers many rows, so state is per batch and my per-row columns cannot hold "posting" (Q8). Offers and Filings created on use. |
| S-007 | V1 | 70 | CLI boundary keeps primitives free of `src/` paths (Q15). |
| S-008 | V1* | 52 | Changed: A1 narrowed it to a paragraph with no code, and "unsupported kind degrades to ask" matches the UNSET rule. |
| S-009 | V2 | 68 | Stage 2 shadow gathers `rests_on` pairs with the old rule deciding; A1 agrees. |
| S-010 | V1 | 52 | Registry-driven tests; union of 10 modules; add V3's crash and stale-write cases. |
| S-011 | V2 | 85 | Wilson-bound RT2 is the only trigger testable at n = 60. |
| S-012 | V2 | 52 | Evidence column; V3's required responses grafted; low stakes. |
| C-001 | V2 | 70 | Named consumer, acceptance check, "stated reasons count". |
| C-002 | V3 | 68 | "Name the affected action"; unverified protected risk is not a note. |
| C-003 | V2 | 55 | Keeping "Medium" avoids churn in pinned tests; add a glossary line. |
| C-004 | V2 | 70 | `rests_on` is checkable; keep V3's `nonblocking_basis` beside it. |
| C-005 | V1 | 80 | Raised from 60: registry replaces the tuple and the `[:6]` slice; N6 sets the path form. |
| C-006 | V3* | 55 | Changed: exact ids and `set_digest` bind consent; my wording was cosmetics. Keep counts plus five rows. |
| C-007 | V3* | 58 | Changed: my own RC3 shows fix passes introduce defects, so resolve-now needs its own gate (Q9). |
| C-008 | V3 | 85 | Identity tuple, revision, atomic replace beat location plus hash (Q7). |
| C-009 | V3* | 58 | Changed: one path rule; `.gitignore:250` and `WORKER-CONTRACT.md:34` bar a pr-submit path under `.dev/pr-monitor/` from `artifacts`. |
| C-010 | V3* | 52 | Changed: capture state must be visible (Q7, N4); trim V3's six keys to three. |
| C-011 | V3 | 85 | No dry-run in `issue.md` (DA V-26); state per batch. |
| C-012 | V2 | 85 | `verdict(s, m, c, w, e, d)` reads six inputs (sketch line 35). |
| C-013 | V2 | 78 | Three basis sources; upstream inputs have none today. |
| C-014 | V3 | 75 | S UNSET gives FOLLOW_UP or NOTE in 216 of 1,024 states; N2 sizes the fix. |
| C-015 | V3 | 55 | Budgets, breaker, hidden labels; add my field-order replicates. |
| C-016 | V2 | 75 | Blind audit, seeded recall, GR7; add V3's protected-risk review. |
| C-017 | V2 | 88 | L1 and its pin must cover `task/SKILL.md:252,361` and `tech-reference/SKILL.md:513`. |
| C-018 | V1 | 55 | Scale map with a test over eleven families; V3's tasklist caution. |
| C-019 | V3 | 55 | Right measure for 120 versus 139; wider file list. |
| C-020 | V3 | 55 | Union is 10 modules; no variant lists all. |
| C-021 | V2 | 90 | File times give about 22 minutes, not 25. |
| C-022 | V3 | 60 | Loops pin a version; installers skip existing files. |
| X-001 | V1 | 88 | Raised from 60: all three advocates agree; whole-folder drift check. |
| X-002 | V1* | 65 | Changed: versioned fence plus pointer; the plugin has no broadcast (N7), so inline is needed. Digest text is V2's paragraph. |
| X-003 | V2 | 55 | Lowered from 62: `consumer-unknown` kept only under the N3 condition; elsewhere V3's old label. |
| X-004 | V2 | 62 | Once per run plus at an escalation halt, where a person is already asked. |
| X-005 | V3* | 62 | Changed: V2 contradicts itself (Q12); V3's separate owner decision is consistent. |
| X-006 | V3* | 62 | Changed: for the blocking path V3's lower bound is the honest one; keep my ordinal bands for reporting. |
| X-007 | V3 | 90 | S UNSET with W Y and D N returns FOLLOW_UP in the sketch. |
| X-008 | V2 | 80 | Sketch lines 67 to 69 skip UNSET moves; 432 lowering moves. |
| X-009 | V3 | 80 | Privacy denial covers every unapproved external judge (Q10). |
| X-010 | V2 | 90 | `stat` times and the PASS at review 3. |
| X-011 | V2 | 85 | `gate1-cycle-control.md:9`: the Destination cell reads wrong (N1). |
| X-012 | V3* | 55 | Changed: `unsettled` rows must not count as confirmed non-blocking; list and count them apart in the offer. |
| X-013 | V3 | 60 | Union of 10 verified by DA. |
| A-001 | QUALIFY* | 80 | Changed from ACCEPT: 11 files holds, but `pragmatic.md:221` and paraphrases are outside the count. |
| A-002 | QUALIFY | 80 | Upstream gates lack a basis; consumer line plus the N3 sweep. |
| A-003 | ACCEPT | 90 | Cap text pinned at test line 215. |
| A-004 | QUALIFY | 75 | Coordinator must read counts and capture state. |
| A-005 | QUALIFY | 85 | Seed brief: inventory was empty; stage 3 needs 0b plus shadow runs if the table is late. |
| A-006 | QUALIFY | 85 | NEW-1 is a pipe defect; N1 gives the convention and its reader limits. |
| A-007 | QUALIFY | 88 | N7: no plugin hook match. |
| A-008 | QUALIFY | 65 | UNVERIFIED; unknown routes to SHOW_USER. |
| A-009 | REJECT | 90 | Sketch `ORDER` has no UNDETERMINED. |
| A-010 | ACCEPT | 88 | `pragmatic.md:228` exemption; Q11. |
| A-011 | ACCEPT | 85 | No key, no call. |
| A-012 | QUALIFY | 75 | Needs GR7 and the audit. |
| A-013 | QUALIFY | 78 | No dry-run; batch marker needed. |
| A-014 | REJECT* | 80 | Changed from QUALIFY: as worded, "installed copies pick up the new rule" is false; `install_core.py:70` and `install_skills.py:102` skip existing destinations. |
