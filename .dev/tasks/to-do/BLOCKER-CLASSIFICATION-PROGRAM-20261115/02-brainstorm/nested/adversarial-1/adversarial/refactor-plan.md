# Refactoring Plan: Merge into Base (Variant 2, sonnet:analyzer)

Status: complete (Step 4 plan only; the merge is not executed here). Only this file was written. No git write, nothing sent to GitHub, no Jev or TypeSafe call.

## Overview

- Base: Variant 2 (sonnet:analyzer), `variant-2-sonnet-analyzer.md`, chosen by the level-1 tiebreaker (`base-selection.md`: V1 0.921, V2 0.883, margin 3.8 percent; Round 2 points won V1 9, V2 19, V3 19).
- Incorporating strengths from: Variant 1 (opus:architect: skill-folder home, fenced digest, registry, scale map, CLI boundary, test inventory) and Variant 3 (haiku:backend: ledger data contract, consent binding, batch filing, missing-input policy, judge contract, privacy scope, authority as a separate decision).
- Also incorporating: the invariant probe (38 findings; all 9 HIGH UNADDRESSED resolved below), `jev-uses.md` version 2 and `blocker_truth_table_sketch.py` version 2.
- Planned changes: 33 (PC-01 to PC-33). Base-defect corrections are grouped in PC-32 (BW-01 to BW-16).
- Risk level: Medium overall. Five changes are High (PC-08, PC-10, PC-16, PC-21, PC-24); each is a requirement a later `/sc:workflow` plan must test, not a spec-text risk.
- Short names: V1, V2, V3 = the three variants; A1, A2, A3 = the Round 2 advocate files; INV-nnn = `invariant-probe.md`; LC-nn = live checks made for this plan (next section); percentages after a point id are the scoring-matrix confidence.

## Live checks made for this plan

All run in this session against the repo root `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel` (paths below are relative to it). Anything else is cited from the debate files and labelled UNVERIFIED where it carries weight.

| # | Check | Result |
|---|---|---|
| LC-01 | `uv run --no-project python blocker_truth_table_sketch.py` (no bytecode) | `cases 6400 monotonicity violations (answered states) 0 silent-demotion violations 0` |
| LC-02 | Probe importing the sketch v2 | `verdict(N,N,N,N,UNSET,Y)` = SHOW_USER (INV-007 case, was NOTE); `verdict(UNSET,N,N,Y,N,N)` = SHOW_USER (X-007 case, was FOLLOW_UP); 0 states with S, M or C at U or UNSET fall below SHOW_USER; 256 of 26,880 UNSET-to-answer moves lower the verdict: 240 are moves to N (intended) and 16 are SHOW_USER to FOLLOW_UP with D = N and both W and E unset; verdict counts BLOCKING 3,664, SHOW_USER 2,664, FOLLOW_UP 56, NOTE 16 |
| LC-03 | Read `02-brainstorm/jev-uses.md` | line 7 revision note (version 2, six decisive questions); 139 and 149 the new missing-answer rules; 195 still gives `min(pW, pD)` as the W-and-D confidence; 242 still says `LlmJudge` uses "the same ten Noul questions"; 277 recommendation 4 (shared rubric) unchanged |
| LC-04 | Grep `highest severity\|more severe` (case-insensitive) under `src/superclaude`, then `higher severity\|max(imum)? severity\|worst (severity\|rating)\|highest (rating\|grade)` | 13 prose merge lines in 10 files: `skills/task/SKILL.md:252,361`, `skills/tech-reference/SKILL.md:510,513`, `skills/readme/SKILL.md:542,547`, `skills/tdd/refs/build-request-template.md:122`, `skills/operational-guide/SKILL.md:511`, `agents/rf-qa.md:83`, `agents/rf-qa-qualitative.md:84`, `agents/rf-analyst.md:75`, `templates/documents/agent_template_qa.md:85`, `templates/documents/agent_template_analysis.md:466`. Also `skills/sc-auggie-review-protocol/SKILL.md:228` ("keep the higher severity") and code in `cli/roadmap/remediate_parser.py:55,301,365`; unrelated ranks in `cli/pipeline/fmea_classifier.py` and `pr_submit/severity_router.py`. `plugins/superclaude`: 0 matches |
| LC-05 | Grep `Grade every review finding as blocking or minor` under `src/superclaude` | 11 files, 11 occurrences |
| LC-06 | Read `src/superclaude/cli/install_skills.py:100-104` | an existing skill folder is skipped unless `force` |
| LC-07 | Grep `src/superclaude/cli/install_user_setup.py` | 77-78: without `force` an existing file is kept and listed as stale; 117-118: "were NOT updated (run with --force or `superclaude update` to refresh"; 186-197: output styles use the same copy routine |
| LC-08 | Grep `src/superclaude/cli/install_core.py` | 58 globs `core/*.md`; 70 skips an existing destination unless `force` |
| LC-09 | Read `src/superclaude/hooks/hooks.json:160-177`, `hooks/scripts/pragmatic-subagent.js`; Grep `pragmatic` in `plugins/superclaude` | 173 registers `node "$HOME/.claude/hooks/pragmatic-subagent.js"`; script line 7 reads `~/.claude/output-styles/pragmatic.md`, line 15 injects it whole, line 21 exits 1 if missing; plugin tree: no file |
| LC-10 | Read `src/superclaude/commands/issue.md:1-50` | 19 "Both modes post directly to GitHub; nothing is shown for approval first"; 21 rule 10 still governs issues filed without `/sc:issue`; 25 explicit only; 40 `--depth` sets how hard it "fills the body"; 41-42 mode and type "chosen by a worker when omitted"; 46 no repository, dry-run or preview option |
| LC-11 | Read `src/superclaude/core/WORKER-CONTRACT.md:14-55` | 23 never-as-worker list includes `/sc:issue`; 31 WC-2 (no person-blocking step, unattended only); 32-39 WC-4 (one report file); 33 enumerates the top-level keys; 34 gitignored paths stay out of `artifacts`; 39 "the coordinator opens it"; 47 WC-11 one writer per file |
| LC-12 | Read `src/superclaude/output-styles/pragmatic.md:218-232` | 221 reviewers hunt "false claims"; 225 the definition; 226 minors never rechecked; 228 own-model exemption; 229 S5 label rule; 230 Medium, "asks the user once per loop"; 231 spec-panel scale and "a reviewer never suppresses such a finding" |
| LC-13 | Grep `src/superclaude/agents/rf-qa.md` | 111 S5; 152 "Any incomplete file = FAIL"; 162 "Any untagged doc claim = FAIL"; 168 "Will this gap reduce report quality? → IMPORTANT"; 170 "Any CRITICAL or IMPORTANT gap = overall FAIL"; 182-183 PASS/FAIL by label; 327 "Flag exact duplicates as IMPORTANT"; 389, 476 count CRITICAL and IMPORTANT as blocking |
| LC-14 | Read `skills/task/SKILL.md:286-297`, Grep it for follow-up; Read `skills/tech-research/SKILL.md:412-421` | task 290-292: one final validation pass, nothing about a ledger; its only follow-up text is the Follow-Up Items log (156, 361). tech-research 415-419: Gate 5 enumerates findings, reads no ledger |
| LC-15 | Read `Makefile:108-182` | sync-dev copies each skill folder whole (112-125), agents, commands to `.claude/commands/sc/` (132-136), hook scripts, `session-init.sh`, templates; no `core/`, `rules/` or `output-styles/`; verify-sync runs `diff -rq` per skill (178) |
| LC-16 | `ls ~/.claude/commands/sc` and `src/superclaude/commands`; Grep `follow-up\|Medium\|concrete wrong outcome` | `spec-panel-armb`, `-diffgate`, `-ledger`, `-ponytail`, `-stoprule` exist only installed; `src` has `spec-panel.md` only; each variant has 1 or 2 matching lines |
| LC-17 | Grep `split("\|")` in `src/superclaude/cli/review` | `card_convert.py:250` and `telemetry.py:162` split on every bare pipe |
| LC-18 | Grep `sc-tasklist-protocol/SKILL.md`; Read `sc-reflect-protocol/SKILL.md:1538-1541` | "High or Medium" or "Medium (blocking)" on 7 lines (1439, 1450, 1531, 1567, 1571, 1610, 1614); reflect 1540: Drift and Regression block promotion |
| LC-19 | Grep `tests/` for rule-pin symbols | 11 files match; `tests/skills/test_spec_panel_review_loop.py:15` imports `CANONICAL_CAP_TEXT` (a transitive pin no variant lists); the `"src/superclaude" not in` assertion also matches unrelated modules (pr_submit tests, `test_task_workspace_lifecycle.py`, `test_review_brief_placement.py`), so the set depends on the pattern |
| LC-20 | `ls` | `src/superclaude/skills/sc-review-severity` absent; `plugins/superclaude/skills` holds 4 skills (confidence-check, sc-implement-protocol, sc-recommend, sc-workflow-protocol) |
| LC-21 | Grep `.gitignore` | 250 `.dev/pr-monitor/` |
| LC-22 | Grep `MDTM (` in `src/superclaude/core` | `CLAUDE.md:80` and `HOW-WE-WORK.md:18` define MDTM as "the task-file/checklist format" |

## Planned Changes

Each change: source, target in the base (section numbers are V2's), integration approach, rationale with debate evidence, risk.

### PC-01: Shared rule lives in a delegate-only skill folder (from V1)
- Source: V1 7.3 (location table and contents), 7.4; convergence item 1 of A1, A2 and A3.
- Target: V2 9.1 and D1 (replace).
- Approach: replace. New home `src/superclaude/skills/sc-review-severity/`: `SKILL.md` ("Delegate-only, no slash command"), `refs/rule.md` (full rule plus the fenced digest), `refs/scale-map.md`, `refs/follow-up-ledger.md`, `refs/classifier-questions.md`, `refs/registry.yaml`. Pointer line names `~/.claude/skills/sc-review-severity/refs/rule.md` first, then `.claude/skills/sc-review-severity/refs/rule.md`; never a `src/` path.
- Rationale: X-001 V1 93 percent unanimous; S-005 V1 92 percent unanimous; V2 conceded in R1 and R2 (Q2), V3 conceded (A3 R2 row 1). LC-15: the skill folder is synced whole and `diff -rq` checked; `core/` has no sync step. LC-20: the folder does not exist yet.
- Risk: Medium. Pointer staleness after a rule change is handled by PC-04.

### PC-02: Fenced, versioned digest plus one pointer line in every carrier (from V1, text from V2 and V3)
- Source: V1 7.2 option C and 7.4 (fence `review-severity:digest vN begin` and `end`); digest text = V2 4.1 paragraph plus V3 3 sentences "name the affected action and evidence" and "Unknown is not no"; cap sentence word for word.
- Target: V2 9.2 (replace the "block word for word" design) and the lead-in of V2 4.1.
- Approach: replace.
- Rationale: X-002 V1 80 percent unanimous; A3 conceded references-only, A2 moved to V1 (R2 X-002). LC-09: no `pragmatic` hook in the plugin tree, so only text inside each carrier reaches plugin-only installs. A-001 QUALIFY 87 percent: the brief at `pragmatic.md:221` ("false claims", LC-12) changes in the same edit. A-003 ACCEPT 95 percent: `CANONICAL_CAP_TEXT` stays word for word.
- Risk: Medium (test churn; INV-031).

### PC-03: Registry and registry-driven drift tests (from V1, paths from A2, surfaces from A3)
- Source: V1 7.3 registry row, 10.2 T1 to T5; A2 R2 N6 (install-root-relative paths); A3 R2 item 1 (explicit surface mapping).
- Target: V2 9.2 bullets 3 and 4, V2 11 T1 (replace).
- Approach: replace. Each row: logical path (`output-styles/pragmatic.md`, `skills/task/SKILL.md`), kind, surfaces (src, installed, project `.claude/`, plugin, installed-only), stage, digest version, own-scale flag. Commands map `commands/<n>.md` in src to `commands/sc/<n>.md` installed and in `.claude/` (LC-15). Tests over the registry: digest equality, reverse scan of `src/` and `plugins/` for the old sentence and the fence opener, pointer order, precedence sentence present (PC-06), no `src/superclaude` in any carrier. The installed-only spec-panel variants (LC-16) get rows with surface `installed-only`, excluded from CI and named in OD10.
- Rationale: C-005 V1 87 percent unanimous; S-010 V1 66 percent; A2 Q3 conceded that its manifest had no stage. INV-030: `output-styles/` and `rules/` are not synced (LC-15), so carrier drift is the registry tests' job; the spec never cites verify-sync for carriers. INV-029.
- Risk: Medium.

### PC-04: Delivery to installed copies; what a switch or revert really costs (from V3, INV-001)
- Source: V3 7 ("A bare promise ... is false"; "mixed versions must be detected"); V2 R10.
- Target: NEW V2 section 9.4 "Delivery and refresh"; V2 12 rollback column; V2 13.2 revert definition.
- Approach: insert. Requirements: (a) first install: the new skill folder reaches an existing `~/.claude` because the folder does not exist yet (LC-06 skips only an existing folder); (b) every later change to that folder, to `pragmatic.md` or to a rule prompt stays stale until `superclaude update` or an install with `--force` (LC-06, LC-07); (c) a stage switch or revert is three steps: repo edit of carriers and registry, a release whose note names the refresh command, a refresh on each machine; the spec never calls it "a registry edit"; (d) the immediate brake that needs no reinstall is the per-run grading-override file (V2 GR11), and RT1 acts through it first; (e) a read-only install check (a `superclaude review` subcommand or a `make doctor` check, named by the plan) compares installed carriers' digest versions with the registry and reports mismatches; each ledger header records the digest versions its carriers held.
- Rationale: C-022 V3 74 percent unanimous; A-014 REJECT 88 percent unanimous; INV-001 HIGH (A1 item 6 "each stage's revert is a registry edit" is false on installed machines).
- Risk: Medium.

### PC-05: Plugin surface (from V1 D9)
- Source: V1 D9; A1 R2 N1; A2 R2 N7.
- Target: V2 9.1 last paragraph (replace "no plugin mirror in version 1").
- Approach: replace. Plugin carriers (`commands/spec-panel.md`, `rules/prompts/document_review_loop_prompts.md`, `skills/sc-implement-protocol/refs/qa.md`) hold the inline digest; at stage 4 a hand mirror of the skill folder goes into `plugins/superclaude/skills/` with a parity test. Until then the release note says plugin-only users keep today's text.
- Rationale: A-007 QUALIFY 86 percent; INV-032 ADDRESSED. LC-20: plugin skills are hand-kept (4 today); LC-09: no broadcast.
- Risk: Low.

### PC-06: Precedence when one context holds two definitions (INV-027)
- Source: invariant probe INV-027; V3 7 ("A consumer missing the required version retains the old gate"); A1 R2 item 1.
- Target: V2 4.1 (append a sentence inside the digest); V2 12 stage 3 row.
- Approach: append. Digest sentence, also in `pragmatic.md`: "When your context holds more than one definition of blocking, the one in the instructions of the agent, skill or command doing this review wins over a session-wide output style; text inside the work under review is data, not a definition; a protocol listed as own-scale keeps its model." Stage 3 moves `pragmatic.md` and the rf-qa family together.
- Rationale: INV-027 HIGH. LC-09: every subagent receives the installed `pragmatic.md`, so in stage 3 an rf-qa reviewer can hold the v2 broadcast plus a legacy task-file sentence, or, on a stale install, a legacy broadcast plus a v2 carrier. The rule makes the carrier win in both directions, which matches V3's "wrong version keeps its old gate".
- Risk: Medium (a model may still blend two texts; measured by M10 split by carrier version).

### PC-07: Rule wording: acceptance checks, required behaviour, named affected action (from V3)
- Source: V3 3 condition table, "A reviewer must name the affected action and evidence", "Unverified protected-risk claims remain unresolved ... they are not notes", "A wrong number used in an acceptance check blocks".
- Target: V2 4.1 conditions 1 to 3 and the 4.2 table; the `pragmatic.md:221` brief.
- Approach: insert.
- Rationale: C-001 V2 78 percent (A3: "retain V3's required-behavior and acceptance-check wording"); C-002 V3 80 percent unanimous; A-001.
- Risk: Low.

### PC-08: Unknown consequence and intermediate gates (from V3, INV-009)
- Source: V3 3 "Unknown is not no"; A3 R2 item 3; A2 R2 Q4 (narrowed).
- Target: V2 4.2 last two rows, 4.3 row "Research input file", GR4, 7.6 item 3, the upstream-gates risk row.
- Approach: replace. A finding whose consumer cannot be named keeps the reviewer's label, is tagged `consumer-unknown`, counted separately and listed first in the offer. New owner decision OD14: allow non-halting deferral for condition 1 only, only at named intermediate gates of one family, only after GR7 is code in that family's final gate and a seeded test shows that a deferred row whose text reaches the final decision basis uncorrected becomes Blocking; never for conditions 2 or 3; never at the last gate; never surviving delivery unresolved. Recommendation: approve for the task family after stage 3 data, not before.
- Rationale: X-003 V3 66 percent, 2 of 3 (A1 moved to V3; A2 lowered to 55); A-002 QUALIFY 86 percent; INV-009 HIGH. LC-14: no final gate reads a ledger today, so A2 N3 ("the precondition holds for those two families") is false.
- Risk: High (the trade between over-blocking at upstream gates and escapes sits here).

### PC-09: Truth table version 2 and missing answers (from V3 policy, now in the sketch)
- Source: `jev-uses.md` section 4 version 2; sketch v2; V3 5.3 required policy; A-008 qualification.
- Target: V2 7.3 (replace the whole subsection); V2 7.2 (add the NA state); V2 11 T2.
- Approach: replace. Rules: `wrong()` reads a missing or unsettled partner as U; any U or UNSET on S, M or C lifts a verdict below SHOW_USER to SHOW_USER and never lowers BLOCKING; NA (read as N) only for M and C and only when the deliverable kind is declared to have no required-item or constraint list, never when an extractor failed or is missing (that is UNSET, A-008); UNDETERMINED is a typed judge-chain failure outside the table (A-009); three property tests (one verdict per combination, monotone over answered states, no silent demotion); the 16 remaining SHOW_USER to FOLLOW_UP moves are stated as intended (D = N rules out BLOCKING); the (wrong N, D Y) NOTE cell is counted per run. Delete "UNSET means send to a person".
- Rationale: X-007 V3 95 percent; C-014 V3 89 percent; X-008 V2 88 percent; A-009 REJECT 94 percent; INV-007, INV-010, INV-014, INV-016. LC-01, LC-02.
- Risk: Medium.

### PC-10: A safety finding labelled minor is caught during the run (INV-008)
- Source: invariant probe INV-008; V2 GR1 vocabulary scan; V3 6 "Review all protected-risk disagreements"; `pragmatic.md:231`.
- Target: V2 8.1 (new GR12); V2 6.4 unattended bullet; V2 7.5 shadow paragraph.
- Approach: insert. Upgrade-only safety route, active in every stage including shadow: when the GR1 scan hits a non-blocking row, or a judge answers S = Y or U on a row a reviewer graded non-blocking, the row is tagged `protected-risk-dispute` and is never written as a plain follow-up. Attended: shown to the person before the gate passes. Unattended: `worker_status: partial`, counted in `follow_up_counts.show_user`, named in the final report line. Both: the row joins the all-disagreements protected-risk review. It can only raise, never lower.
- Rationale: INV-008 HIGH; C-016 V2 82 percent ("add all protected-risk disputes"). LC-12: line 231 forbids suppression but nothing enforces it in-run; LC-03: `jev-uses.md` says the classifier "never silently upgrades".
- Risk: High (the only path where shadow output reaches a gate; false hits cost attention).

### PC-11: Confidence: honest bound and bands (from V3)
- Source: V3 5.3 (`max(0, pW + pD - 1)`); V2 7.4 bands kept.
- Target: V2 7.4 first bullet (replace).
- Approach: replace. The non-blocking union-bound score is reported, never used as a gate.
- Rationale: X-006 V3 82 percent unanimous; A1 conceded K2; A2 moved (R2 X-006). LC-03: `jev-uses.md:195` still uses the min; the merged spec overrides it and says so.
- Risk: Low.

### PC-12: Judge request and response contract, runtime bounds, cache key, secrets (from V3)
- Source: V3 5.2 and 5.4; V2 7.4 field-order replicates.
- Target: NEW V2 7.7.
- Approach: insert. Labels and author hidden from the judge; typed failures; a 10-second attempt and a 30-second budget as pilot parameters, not service guarantees; circuit breaker; cache key including the decision-basis digest; key only in the process environment.
- Rationale: C-015 V3 73 percent unanimous; U-016, U-018; INV-005.
- Risk: Low.

### PC-13: Privacy denial covers every external judge; no key, no call (from V3)
- Source: V3 5.4.
- Target: V2 7.5 judge table and D3 ("else use the LLM judge only").
- Approach: replace.
- Rationale: X-009 V3 90 percent; A1 K11 and A2 Q10 conceded; A-011 ACCEPT 80 percent (2 of 3).
- Risk: Low.

### PC-14: Classifier authority is an owner decision, tied to the judge measured (from V3)
- Source: V3 10 stage 5 ("never implied by completion of stage 4"); INV-012.
- Target: V2 12 stage 4 (remove classifier gating), D4 (rewrite), 7.5 "Gating, if it ever happens".
- Approach: replace. Evidence for authority must come from the same judge id and version that would hold it; `LlmJudge` results do not transfer to Jev.
- Rationale: X-005 V3 77 percent unanimous; A1 K9 and A2 Q12 conceded (V2 stage 4 contradicted its own D4).
- Risk: Low.

### PC-15: Classifier reached only through the review CLI (from V1)
- Source: V1 5.1.
- Target: V2 10.4 row "classifier package" (replace "location is a plan decision").
- Approach: replace. Primitives call a `superclaude review` subcommand; module layout stays a plan choice.
- Rationale: S-007 V1 80 percent unanimous (A3 changed); INV-038; the `review` click group at `cli/review/__init__.py:14` (diff V-29, probe L20).
- Risk: Low.

### PC-16: Ledger data contract (from V3, with V2 fields)
- Source: V3 4.1 to 4.3 (single writer, run-scoped ids, identity tuple, Observations, states, revision, atomic replace, preserved corrupt file, `capture_state`); V2 6.2 (`rests_on`, tags, short Notes table, sort order, five rows in the offer).
- Target: V2 6.2 (restructure).
- Approach: restructure. Offers and Filings records appear on first use. Cross-run rule (INV-002): a new run on the same deliverable matches prior `declined`, `filed` and `resolved` rows by identity tuple without the run namespace and does not re-offer or re-file them.
- Rationale: C-008 V3 89 percent; S-006 V3 67 percent (tables on use, A3 conceded); A2 Q7 conceded. INV-002, INV-006, INV-022, INV-025.
- Risk: High (most new machinery; stage 1 offline tests carry it).

### PC-17: Ledger cell codec (decision between three proposals)
- Source: A3 R2 item 5 (entity encoding); A2 R2 (evidence outside cells, id-keyed fenced block); V3 4.2 round-trip rule.
- Target: V2 6.2 (new paragraph "Cell encoding").
- Approach: insert. One reversible entity layer for free-text cells: `&` to `&amp;` first, then pipe to `&#124;`, backtick to `&#96;`, `<` to `&lt;`, `>` to `&gt;`, newline to `&#10;`, carriage return to `&#13;`, a leading or trailing space to `&#32;`; decode in reverse with `&amp;` last. Verbatim evidence goes in an id-keyed fenced block below the table, never in a cell. One reader and writer for this ledger only; round-trip fixtures with pipes, backticks, literal entities, Unicode and multiline text. A3's JSON layer is not adopted (the entity layer is already reversible); add it only if a fixture fails.
- Rationale: A-006 QUALIFY 88 percent hid three incompatible codecs (conformity point); INV-023 HIGH. LC-17: `card_convert.py:250` and `telemetry.py:162` split on every bare pipe, so A1's `\|` mis-splits under a naive reader; entities hold no pipe.
- Risk: Medium.

### PC-18: Ledger location: one rule, two exceptions (from V3)
- Source: V3 4.1 path rule; A1 K15.
- Target: V2 6.6 (replace the table).
- Approach: replace. `<run-report-dir>/qa/follow-ups.md` when a QA directory exists, else `<run-report-dir>/follow-ups.md`; `/sc:implement` keeps `notes.md` with a pointer row; pr-submit keeps its own list.
- Rationale: C-009 V3 69 percent unanimous. LC-21 and LC-11: `.dev/pr-monitor/` is gitignored and ignored paths stay out of `artifacts`.
- Risk: Low.

### PC-19: Offer consent binding and unsettled rows (from V3, cadence from V2)
- Source: V3 4.5 (exact ids, `set_digest`, notes opt-in, resume shows and does not re-ask, a changed set needs new consent); V1 4.3 one-line no-question form.
- Target: V2 6.3 (append) and 6.1 step 5.
- Approach: append. Cadence stays V2's: once per run plus at an escalation halt. `unsettled` rows are counted apart from confirmed non-blockers and kept out of their offer set.
- Rationale: C-006 V3 68 percent; X-012 V3 65 percent (2 of 3); X-004 V2 71 percent; INV-004, INV-022.
- Risk: Low.

### PC-20: "Resolve now" is separately authorized work (from V3)
- Source: V3 3 last line; V3 12 last row.
- Target: V2 6.7 (replace).
- Approach: replace. A one-location mechanical fix may use the L2 checks alone; anything else re-enters normal scope and its own gate.
- Rationale: C-007 V3 67 percent (2 of 3); A2 Q9 conceded on its own RC3 evidence (NEW-1 and NEW-2 came from a fix).
- Risk: Low.

### PC-21: One-issue filing: exact body, batch marker, states, size, fork only (from V3, INV-026, INV-024)
- Source: V3 4.5 (batch id digest, `prepared`, `posting`, `reconcile`, `filed`, never blind retry, fork only).
- Target: V2 6.5 (replace the option verdicts), 6.1 step 6, the non-goal on `/sc:issue`.
- Approach: replace. New owner decision OD15 with recommendation: version 1 posts the approved body file itself from the attended top-level session after an explicit filing answer, through the rule-10 path with `gh issue create --repo IronbellyOrg/IronClaude --title "<title>" --body-file <filled copy of ~/.claude/ISSUE-BACKLOG.md>`, then reads the posted body back and compares its digest with `body_digest` before rows become `filed`. Requirement floor on any path: the posted body is byte-equal to the approved body and carries the batch marker, else rows stay `reconcile`. Size: the body holds ids, one-line finding, location and the ledger path; evidence stays in the staged ledger; above a size bound the body is split into parts sharing the batch id (the GitHub limit of about 65,536 characters is UNVERIFIED).
- Rationale: C-011 V3 90 percent; A-013 QUALIFY 86 percent; INV-026 HIGH; INV-024; INV-013. LC-10: `/sc:issue` writes the body itself after consent (lines 40-42) and posts with no preview (19), so neither digest nor marker survives it; line 21 keeps rule 10 for issues not filed through it; line 25 (explicit only) means a generic "yes" cannot invoke it.
- Risk: High.

### PC-22: Worker return contract: three keys, visible capture failure
- Source: A2 R2 item 3, A3 R2 item 6; V3 4.6 ("Capture failure makes the run partial or failed").
- Target: V2 6.4 bullet 2 (replace); V2 10 file list (`core/WORKER-CONTRACT.md`).
- Approach: replace. Keys `follow_up_ledger`, `follow_up_counts {follow_up, note, show_user}`, `follow_up_capture_state`; `incomplete` maps to `worker_status: partial`, added to the WC-4 mapping; the coordinator duties name the three keys as things to read.
- Rationale: C-010 V3 68 percent, but two of three proposals trim V3's six keys (conformity point); A-004 QUALIFY 84 percent; INV-003, INV-017. LC-11: line 33 enumerates keys, so each key is a contract edit; line 39: the coordinator opens the contract.
- Risk: Medium.

### PC-23: Consolidation merge rule (L1): full inventory and a reverse-scan pin
- Source: V2 4.4 L1 (kept); A1 R2 N2; A3 R2 N5; INV-015; LC-04.
- Target: V2 4.4 L1 "Where" cell, 2.2 RC2, 10.3, 11 T5.
- Approach: replace. L1 covers 13 lines in 10 files. Stage 3: `task/SKILL.md:252,361`, `rf-qa.md:83`, `rf-qa-qualitative.md:84`, `rf-analyst.md:75`. Stage 4: `tech-reference/SKILL.md:510,513`, `readme/SKILL.md:542,547`, `tdd/refs/build-request-template.md:122`, `operational-guide/SKILL.md:511`, `agent_template_qa.md:85`, `agent_template_analysis.md:466`. `sc-auggie-review-protocol/SKILL.md:228` is a code-review dedupe on its own scale: a scale-map row, unchanged in version 1. `remediate_parser.py` is code-assigned (out of scope with the roadmap checkers). T5 becomes a reverse scan for `highest severity`, `more severe rating` and `higher severity` over `src/` and `plugins/`, with the scale-map rows as the allowlist.
- Rationale: C-017 V2 94 percent unanimous, but the vote hid "three lines" (conformity point); C-019 V3 60 percent (name both measures).
- Risk: Medium.

### PC-24: rf-qa fixed FAIL triggers in the pilot family (INV-034)
- Source: invariant probe INV-034.
- Target: V2 4.4 (new L6), 10.3 QA agents row, 12 stage 3, 13.1.
- Approach: insert. The stage 3 inventory lists `rf-qa.md:152, 162, 168-170, 182-183, 327, 389, 476` (LC-13). Each is either rewritten to "grade by the three conditions; the label is information", or kept as a named mechanical gate mapped to condition 2 (Missing) when a template requires the item (likely for 152 and 162), with the keep recorded in the scale map. Line 327 becomes Note unless a condition holds. `tests/audit/test_nfr_conv_9_zero_trust.py` and its transitive importer change in the same step.
- Rationale: INV-034 HIGH; no Round 2 item listed these lines, and rf-qa is the stage 3 pilot.
- Risk: High (the pilot can show no benefit if these are missed; M12 is the falsifier).

### PC-25: Scale map with explicit inventory and adapter approvals (from V1, V3)
- Source: V1 7.5 (eleven families); V1 8.3 (as one "how to add a row" paragraph, no code); V3 7 (separate adapter approvals).
- Target: V2 9.3 (summary plus a pointer to `refs/scale-map.md`); D6, D7, D10.
- Approach: restructure. Additions: the auggie-review dedupe row (LC-04); tasklist on 7 lines (LC-18); reflect 1540 (LC-18). Shadow comparisons read the reviewer's native label through the scale map, never the `card_convert.py` boolean (INV-028).
- Rationale: C-018 V1 63 percent; S-008 V1 64 percent (paragraph only, A1 K5); INV-028, INV-036.
- Risk: Low.

### PC-26: Test inventory: named patterns, at least 11 modules (from V1, V3)
- Source: V1 10.1 (`test_review_rules_text.py`); V3 9 (transitive pin); LC-19.
- Target: V2 11 table and lead-in.
- Approach: replace. The 8 enrichment modules plus `tests/review/test_review_rules_text.py`, `tests/audit/test_invariant_preservation_NFR_6_through_10.py` and `tests/skills/test_spec_panel_review_loop.py` (imports `CANONICAL_CAP_TEXT` at line 15). The spec names each pattern; the plan re-runs them. `S1_S3_FILES` and its `[:6]` slice are replaced by registry rows in the same step as the fence (INV-031).
- Rationale: C-020 V1 57 percent (2 of 3); X-013 V3 57 percent (2 of 3); INV-019.
- Risk: Low.

### PC-27: Guardrail measurement corrections (from A3 N6, V3, V1)
- Source: A3 R2 N6; V3 6 and 11; V1 revert trigger 1.
- Target: V2 8.2 "Report" row; 13.2 RT1 and RT2.
- Approach: replace. Per-stratum Wilson intervals with the sampling fraction; RT2 computed on a separate simple random sample of non-blocking rows (oversampled strata are diagnostic only); every protected-risk disagreement reviewed, not sampled; RT1 a single event.
- Rationale: C-016 V2 82 percent ("add all protected-risk disputes and N6's sampling correction"); S-011 V2 89 percent; INV-037.
- Risk: Medium.

### PC-28: Rollout restructure, one stage 3 entry condition
- Source: convergence items 6 (A1, A2) and 8 (A3); V3 10 stages 0 and 1.
- Target: V2 12 and 15b (restructure).
- Approach: restructure. 0 Measure: 0a table and five fixture or approved-judge runs (only if the table exists), 0b retrospective escape test, 0c paired re-grade (only if the table exists), inventory freeze (re-run every Grep). 1 Offline scaffold: skill folder, registry all `legacy`, codec, ledger adapters, fixture judge, property tests, crash, reconcile and consent tests, install check; no carrier edited. 2 Shadow beside the old rule: task skill and tech-research write the ledger and make the offer, reviewers emit `rests_on`, classifier in shadow, PC-10 live. 3 Pilot: `pragmatic.md` and the rf-qa family to v2, L1 stage 3 lines, L2, PC-24. 4 Propagate: templates, rule prompts, builders, remaining L1 lines, spec-panel narrowing, plugin mirror, strict reverse scan. Stage 3 entry: 0b result written; at least 5 shadow runs observed with zero safety misses and no capture failure (an observation minimum, not a safety claim); seeded recall (8.3) met; 0c as well when the table exists; owner go. Own-scale adapters and classifier authority are owner decisions, not stages.
- Rationale: S-009 V2 75 percent, but three different entry conditions (conformity point); A-005 QUALIFY 89 percent; INV-018.
- Risk: Medium.

### PC-29: Risk table with likelihood, impact and required responses (from V1, V3)
- Source: V1 13 columns; V3 12 required responses.
- Target: V2 14 (restructure); risk ids renamed RK1 onward (BW-03).
- Approach: restructure. New rows: stale installs (INV-001), mixed contexts (INV-027), installed-only variants (INV-029), loops not reached (INV-036), weak debate majority (INV-021).
- Rationale: risk.1 NOT MET for V2 in both passes; S-012 V2 49 percent (2 of 3, V3 responses grafted).
- Risk: Low.

### PC-30: SHOW_USER never halts an attended run in version 1 (INV-011)
- Source: V2 6.4 unattended rule, extended.
- Target: V2 6.1 and 7.5.
- Approach: insert. With no classifier authority (PC-14), the reviewer's label stands, the row is tagged `unsettled` and shown first in the end-of-run offer; the only in-gate prompt is PC-10.
- Rationale: INV-011 MEDIUM; LC-11 line 31: WC-2 covers unattended runs only.
- Risk: Low.

### PC-31: Metrics additions
- Source: INV-035, INV-034, INV-012.
- Target: V2 13.1 (append M11 to M13).
- Approach: append. M11: each extra fix cycle attributed to fix-induced, definition-driven or other findings. M12: rf-qa FAIL count per pilot gate (flat counts falsify the pilot). M13: shadow results split by judge id and version.
- Risk: Low.

### PC-32: Base defect corrections BW-01 to BW-16
- Source: the diff analysis, both scoring passes, A2's own concessions; section below.
- Target: as listed per BW row.
- Approach: replace (text corrections).
- Risk: Low.

### PC-33: Verification section refresh
- Target: V2 16 (append 16.4 "Checks made for the merge" with LC-01 to LC-22; re-label any [E] claim this plan confirmed as [V], and correct any it contradicted).
- Approach: append.
- Risk: Low.

## Base weaknesses to fix (carried by PC-32 unless another PC is named)

| # | Defect in V2 | Found by | Fix |
|---|---|---|---|
| BW-01 | 7.3 "UNSET means send to a person"; its 4,096 and 432 counts describe sketch v1 | diff X-007; pass 1 correctness.1 | PC-09: sketch v2 rules, 6,400 combinations, three property checks, 16 intended moves (LC-01, LC-02) |
| BW-02 | 4.2 `consumer-unknown` non-blocking Medium against 7.3 and 7.6 item 3 (same situation, two outcomes) | pass 1 IC; A2 conceded | PC-08 |
| BW-03 | "R2" is the run-2 folder (section 0) and a risk id (14); "D" is a classifier question and the decision ids | pass 1 correctness.3 | keep `R2` for the folder; risks become RK1 onward; owner decisions become OD1 onward |
| BW-04 | 11 "Eight test modules" and "the nine paths below" over an 8-row table | pass 1 IC; X-013 | PC-26 (at least 11 modules, patterns named) |
| BW-05 | L1 says "highest severity" also sits in task-builder and tech-research [E] | A2 Q13 retracted; LC-04 | PC-23 (13 lines in 10 files) |
| BW-06 | MDTM, WC-2, WC-4, SHOW_USER, UNDETERMINED used without definition | pass 1 clarity.4 | glossary rows: MDTM "the task-file/checklist format" (LC-22); WC-2 and WC-4 = numbered rules in `~/.claude/WORKER-CONTRACT.md` (LC-11); verdict names from `jev-uses.md` section 4 |
| BW-07 | Risk table has no likelihood or impact | risk.1 NOT MET | PC-29 |
| BW-08 | Line 85 points at "section 4.6"; the changes are in 4.4 | pass 1 DC | correct the reference |
| BW-09 | 6.4 "WC-4 line 35 allows extra keys" | A2 N4 retracted; LC-11 line 33 | PC-22 |
| BW-10 | D8 does not answer whether the classifier may fill `qa.md`'s four answers | diff coverage table; A2 Q11 | add: no in version 1 (`jev-uses.md` J3) |
| BW-11 | 9.1 and D1 recommend `core/REVIEW-SEVERITY.md` | X-001 | PC-01 |
| BW-12 | L1 "undecidable dispute is `disputed` Medium" against GR5 "blocking stands unless code disproves it" | A2 Q5 conceded; A3 R2 section 2 | a blocking grade that names a consumer not disproved by code stands; one naming none goes back to the reviewer once (GR2); still none: the label stands, tag `disputed`, listed first; never demoted for missing grounding |
| BW-13 | RC6 and 10.3 list tasklist lines 1439, 1610, 1614 only | LC-18 | 7 lines (1439, 1450, 1531, 1567, 1571, 1610, 1614) |
| BW-14 | 10.3 "`2 fix cycles` 22 files and 139 times [E]" | C-019 | "22 files, 120 matching lines, 139 occurrences", with the measure named |
| BW-15 | 7.2 and 7.5 rely on `jev-uses.md`, which still says ten questions for `LlmJudge` (line 242) and the min as confirm score (195) | LC-03 | the spec states six questions and PC-11's bound, and notes the two stale lines |
| BW-16 | 6.1 step 6 "Filing writes the issue number back into the ledger rows" (per-row state) | A2 Q8 conceded | PC-21 batch states |

## Invariant resolutions

Type: REQ = requirement written into the merged spec; OD = owner decision with a recommendation; RISK = risk row; ACC = accepted with reason; ADDR = already addressed (where).

| ID | Severity, status | Type | Resolution and location in the merged spec |
|---|---|---|---|
| INV-001 | HIGH, UNADDR | REQ | PC-04: first install versus skip-existing; a switch or revert is repo edit plus release plus refresh; per-run override is the immediate brake; install check |
| INV-002 | MED, UNADDR | REQ | PC-16 cross-run rule: identity tuple without run namespace; no re-offer or re-file of declined, filed or resolved rows |
| INV-003 | MED, UNADDR | REQ | PC-22: `follow_up_capture_state: incomplete` maps to `worker_status: partial` in WC-4 |
| INV-004 | LOW, ADDR | ADDR | V3 4.5 offer rules via PC-19 |
| INV-005 | LOW, ADDR | ADDR | V3 5.4 cache key via PC-12 |
| INV-006 | LOW, ADDR | ADDR | V3 4.3 `superseded` with reason `escalated` via PC-16 |
| INV-007 | HIGH, UNADDR | REQ | PC-09: `wrong()` reads a missing partner as U (sketch v2, LC-02) |
| INV-008 | HIGH, UNADDR | REQ | PC-10: upgrade-only safety route in every stage |
| INV-009 | HIGH, UNADDR | OD | PC-08: default keeps the reviewer's label; OD14 may enable deferral only after GR7 is wired and tested (recommended for the task family after stage 3) |
| INV-010 | LOW, ADDR | ADDR | PC-09: lift on S, M, C (LC-02: 0 states below SHOW_USER) |
| INV-011 | MED, UNADDR | REQ | PC-30: SHOW_USER never halts in version 1; collected into the offer |
| INV-012 | MED, UNADDR | REQ | PC-14 and M13: authority evidence from the same judge id and version |
| INV-013 | LOW, ADDR | ADDR | PC-21: `--repo IronbellyOrg/IronClaude`; stop when origin is not the fork |
| INV-014 | LOW, ADDR | ADDR | PC-09: UNDETERMINED is a typed failure outside the table |
| INV-015 | HIGH, UNADDR | REQ | PC-23: 13 lines in 10 files, staged; auggie row; reverse-scan pin |
| INV-016 | MED, UNADDR | REQ | PC-09: the 72 moves are now 16 (LC-02), all SHOW_USER to FOLLOW_UP with D = N; stated as intended and pinned by the silent-demotion test |
| INV-017 | MED, UNADDR | REQ | PC-22: three keys |
| INV-018 | MED, UNADDR | REQ | PC-28: one stage 3 entry condition |
| INV-019 | MED, UNADDR | REQ | PC-26: patterns named, at least 11 modules, the plan re-runs them |
| INV-020 | LOW, UNADDR | REQ | the spec states 11 files and 11 occurrences with the pattern (LC-05); the family count is the scale-map list, not a remembered number |
| INV-021 | LOW, UNADDR | ACC | a caveat about this debate, not about the design; recorded in section 16 and as an RK row (PC-29); no requirement |
| INV-022 | LOW, ADDR | ADDR | V3 header-only ledger is valid; V1 one-line form (PC-16, PC-19) |
| INV-023 | HIGH, UNADDR | REQ | PC-17: entity codec, fenced evidence block, round-trip fixtures |
| INV-024 | MED, UNADDR | REQ | PC-21: body holds ids and summaries; split above a size bound |
| INV-025 | LOW, ADDR | ADDR | V3 identity tuple via PC-16 |
| INV-026 | HIGH, UNADDR | OD | PC-21: OD15 filing path (recommended: rule-10 `gh issue create --repo ... --body-file`); requirement floor: the posted body equals the approved body digest |
| INV-027 | HIGH, UNADDR | REQ | PC-06: precedence sentence in every v2 digest and in `pragmatic.md`; the pilot switches broadcast and rf-qa together |
| INV-028 | MED, UNADDR | REQ | PC-25: shadow reads the native label via the scale map, not the `card_convert` boolean; glossary line on "Medium" |
| INV-029 | MED, UNADDR | RISK + OD | PC-03 rows marked `installed-only`; OD10 decides align or retire; risk row (PC-29) |
| INV-030 | LOW, ADDR | ADDR | PC-03: carrier drift by registry tests; the spec never cites verify-sync for carriers (LC-15) |
| INV-031 | LOW, ADDR | ADDR | PC-26: tuple, slice and fence change in one step |
| INV-032 | LOW, ADDR | ADDR | PC-05: inline digest now, plugin mirror and parity test at stage 4 |
| INV-033 | LOW, ADDR | ADDR | base non-goal and 9.3: `qa.md` keeps its model (`pragmatic.md:228`, LC-12) |
| INV-034 | HIGH, UNADDR | REQ | PC-24: listed lines rewritten or kept as named mechanical gates; pins updated; M12 falsifier |
| INV-035 | MED, ADDR | ADDR plus REQ | base L2 fix-pass checks; PC-31 M11 attributes each extra cycle |
| INV-036 | MED, UNADDR | RISK + OD | PC-25 and PC-29: tasklist (OD7) and reflect (OD6) named as not reached by stages 1 to 4, so their over-blocking continues until those decisions |
| INV-037 | MED, UNADDR | REQ | PC-27: per-stratum intervals; RT2 on a representative sample |
| INV-038 | LOW, ADDR | ADDR | PC-15: `review` click group |

HIGH tally: 7 resolved by a requirement (INV-001, 007, 008, 015, 023, 027, 034); 2 by an owner decision with a requirement floor (INV-009, INV-026).

## Coverage check: every diff point whose Round 2 result is not V2

| Point | R2 result | Carried by | Note |
|---|---|---|---|
| A-001 | QUALIFY | PC-02, PC-07 | the brief at `pragmatic.md:221` changes with the definition |
| A-002 | QUALIFY | PC-08 | |
| A-003 | ACCEPT | PC-02 | cap sentence word for word |
| A-004 | QUALIFY | PC-22 | |
| A-005 | QUALIFY | PC-28 | |
| A-006 | QUALIFY | PC-17 | |
| A-007 | QUALIFY | PC-05 | |
| A-008 | QUALIFY | PC-09 | NA never for a failed or missing extractor |
| A-009 | REJECT | PC-09 | |
| A-010 | ACCEPT | base (non-goals, 9.3) | already in V2 |
| A-011 | ACCEPT | PC-13 | |
| A-012 | QUALIFY | PC-16, PC-08 | linked escalation; GR7 |
| A-013 | QUALIFY | PC-21 | |
| A-014 | REJECT | PC-04 | |
| C-002 | V3 | PC-07 | |
| C-005 | V1 | PC-03 | |
| C-006 | V3 | PC-19 | |
| C-007 | V3 | PC-20 | |
| C-008 | V3 | PC-16 | |
| C-009 | V3 | PC-18 | |
| C-010 | V3 | PC-22 | content trimmed to three keys |
| C-011 | V3 | PC-21 | |
| C-014 | V3 | PC-09 | |
| C-015 | V3 | PC-12 | budgets as pilot parameters only |
| C-018 | V1 | PC-25 | |
| C-019 | V3 | PC-23, BW-14 | |
| C-020 | V1 | PC-26 | |
| C-022 | V3 | PC-04 | |
| S-005 | V1 | PC-01 | |
| S-006 | V3 | PC-16 | "four fixed tables always present" not carried: tables appear on first use (A3 conceded) |
| S-007 | V1 | PC-15 | |
| S-008 | V1 | PC-25 | one paragraph, no code |
| S-010 | V1 | PC-03, PC-26 | |
| X-001 | V1 | PC-01 | |
| X-002 | V1 | PC-02 | |
| X-003 | V3 | PC-08 | |
| X-005 | V3 | PC-14 | |
| X-006 | V3 | PC-11 | |
| X-007 | V3 | PC-09 | |
| X-009 | V3 | PC-13 | |
| X-012 | V3 | PC-19 | |
| X-013 | V3 | PC-26 | |

Points not carried: none in full. Partial exclusions are named in the Note column (S-006 always-present tables, C-015 budgets as guarantees, C-010 six keys) and in "Changes NOT Being Made".

## Conformity points

| Point | Position the merged spec takes | Why, with the live fact |
|---|---|---|
| C-017 | Replace label-max merging at all 13 lines in 10 files, staged (PC-23); the auggie-review dedupe is an own-scale row; T5 is a reverse scan | LC-04 found 13 lines in 10 files plus `sc-auggie-review-protocol/SKILL.md:228`; the Round 2 "three lines" missed 10 of them |
| A-006 | One entity codec, evidence in a fenced block (PC-17) | LC-17: two readers in `cli/review` split bare pipes, so `\|` is unsafe; A3's JSON layer adds nothing an entity layer lacks |
| C-010 | Three keys and an explicit WC-4 edit (PC-22) | LC-11 line 33 enumerates keys; `follow_up_offer_state` has no worker writer (A2 R2) |
| X-003 | Unknown keeps the reviewer's label by default; deferral only by OD14 after GR7 is wired (PC-08) | LC-14: `task/SKILL.md:290-292` and `tech-research/SKILL.md:415-419` read no ledger, so the "precondition holds" vote rested on a false fact |
| S-009 | One stage 3 entry condition (PC-28) | the three proposals named three conditions; the 0c branch cannot run without the table (A-005, `seed-brief.md:25`) |

## Decisions settled by this plan

- Shared rule home and copies: PC-01, PC-02, PC-03, PC-05. First install versus installers that skip existing files, and the real revert path: PC-04.
- Unknown consequence, UNSET answers, intermediate gates: PC-08 (default keeps the label; OD14), PC-09 (sketch v2 rules), PC-30.
- "Highest severity wins": 13 lines in 10 files plus one own-scale row (LC-04), PC-23.
- A security finding labelled minor: PC-10.
- Ledger escaping and its reader: PC-17.
- `/sc:issue` consent and body digest: PC-21 and OD15.
- Mixed-version stages with the injected pragmatic output style: PC-06.
- rf-qa hard FAIL triggers: PC-24.
- Classifier questions: six decisive (S, M, C, W, E, D), as in sketch v2 `verdict(s, m, c, w, e, d)` at line 43; V2's reworded S and its option Q for upstream gates kept; T, F, I, G are optional explanations in shadow only and never cancel S, M or C.
- Guardrail measurement: V2 8.2 and 8.3 with the PC-27 corrections and PC-10.
- Rollout: PC-28. Classifier authority: an owner decision, PC-14.

## Changes NOT Being Made

| Point | Non-base approach rejected | Reason and evidence |
|---|---|---|
| X-011 | V1 NEW-1 and NEW-2 as NOTE examples | X-011 V2 90 percent; `gate1-cycle-control.md:9` says the Destination cell reads wrong; A1 K1 conceded |
| X-008 | V1 T6 "monotone in every input" | X-008 V2 88 percent; A1 K3 conceded; sketch v2 claims it over answered states only (LC-01) |
| X-006 | V1 `min(pW, pD)` as the confirm score | X-006 V3; `jev-uses.md:195` itself calls it an upper bound |
| X-005 | V1 stage 4 auto-downgrade | X-005 V3 77 percent; A1 K9 conceded |
| C-012 | V1 and V3 ten questions | C-012 V2 89 percent; sketch v2 takes six inputs (LC-01) |
| C-021, X-010 | V1 "about 25 minutes" and 45 percent as a measured gain | C-021 V2 93 percent; X-010 V2 91 percent; file times give about 22 minutes |
| S-011 | V1 M3 5 percent target and trigger 2 | S-011 V2 89 percent; untestable at n = 60; A1 K6 conceded |
| C-009 | V1 pr-submit ledger under `.dev/pr-monitor/` | gitignored (LC-21) and barred from `artifacts` (LC-11 line 34) |
| C-007 | V1 and V2 resolve-now without its own gate | C-007 V3; A2 Q9 conceded |
| X-009 | V1 and V2 "LLM judge only" on privacy denial | X-009 V3 90 percent; A1 K11 and A2 Q10 conceded |
| C-010 | V1 "ledger: unavailable" fail-open; V3 six keys | capture state must be visible (PC-22); `follow_up_offer_state` has no writer |
| S-008 | V1 extension contracts as a spec section that becomes plan work | S-008 accepted only as a paragraph (A1 K5) |
| INV-011 | V1 D4 "SHOW_USER items are still asked at their gate" | WC-2 covers unattended runs only (LC-11 line 31); no classifier authority in version 1 |
| C-018 | V1 tasklist Medium becomes FOLLOW_UP at stage 3 | C-018 retains V3's separate adapter approval; tasklist stays OD7 |
| X-001 | V3 `core/REVIEW-SEVERITY.md` with `.claude/REVIEW-SEVERITY.md` | X-001 V1 93 percent; no sync step creates the project copy (LC-15) |
| X-002 | V3 short references without inline text | X-002 V1 80 percent; A3 conceded; the plugin has no broadcast (LC-09) |
| S-006 | V3 four tables always present | tables on first use; A3 conceded that empty tables must not force work |
| X-006 | V3 non-blocking union bound as a routing gate | reported only; it collapses to zero with four mid-sized terms (A2 R2 section 2; A3 conceded) |
| A-006 | A1 `\|` and `<br>` codec; A3 JSON layer | LC-17 for the first; the second adds no reversibility (PC-17) |
| INV-026 | V2 Option A and V3 "pass that description through the existing create flow" | LC-10: `/sc:issue` writes the body after consent and posts without preview |
| C-002 | V3 "called Medium where useful" | vague (pass 1 clarity.1); V2 keeps "Medium" as the defined word (C-003 V2) |
| C-015 | V3 time budgets as fixed requirements | pilot parameters only (A3 R2 item 7) |
| S-009 | A1 "0b and 0c" and A2 "0b plus 5 runs" as sufficient | PC-28 combines them; five runs are a minimum count, not proof (A3 R2) |
| U-011 | `jev-uses.md` recommendation 4 (shared rubric) | V2 7.6 circularity critique kept in the base |

## Risk Summary

| Change | Risk | Impact if failed | Rollback |
|---|---|---|---|
| PC-01 | Medium | pointer resolves nowhere | keep the inline digest; the pointer is detail only |
| PC-02 | Medium | pinned tests break | revert to V2 9.2 block text |
| PC-03 | Medium | drift goes undetected | fall back to a fixed manifest test |
| PC-04 | Medium | stale machines grade by old text | release note plus forced refresh; per-run override |
| PC-05 | Low | plugin users keep old text | additive; remove the mirror |
| PC-06 | Medium | blended definitions in a pilot context | revert pilot rows to legacy |
| PC-07 | Low | wordier rule | revert to V2 4.1 phrasing |
| PC-08 | High | upstream over-blocking stays, or escapes if OD14 is approved early | keep the default (label stands); withdraw OD14 |
| PC-09 | Medium | more SHOW_USER rows | revert to V2 7.3 text with only the BW-01 correction |
| PC-10 | High | attention cost from false safety hits | narrow the vocabulary list; route S = Y only |
| PC-11 | Low | none | revert to bands only |
| PC-12 | Low | none | drop the subsection |
| PC-13 | Low | none | none needed |
| PC-14 | Low | none | none needed |
| PC-15 | Low | none | the plan chooses another CLI entry |
| PC-16 | High | ledger machinery too heavy for version 1 | keep Items and Observations only |
| PC-17 | Medium | round-trip failures | add A3's JSON layer |
| PC-18 | Low | none | revert to the V2 6.6 table |
| PC-19 | Low | none | revert to V2 6.3 |
| PC-20 | Low | none | revert to V2 6.7 |
| PC-21 | High | duplicate or unbound issue posts | filing disabled; the ledger stays readable |
| PC-22 | Medium | contract edit conflicts | keep one path key only |
| PC-23 | Medium | merge re-inflation survives | widen the reverse scan |
| PC-24 | High | the pilot shows no benefit | keep triggers as recorded mechanical gates |
| PC-25 | Low | none | revert to the V2 9.3 table |
| PC-26 | Low | a pin missed | re-run the patterns |
| PC-27 | Medium | trigger lacks power | pool windows longer |
| PC-28 | Medium | stage gate too strict | the owner relaxes entry by decision |
| PC-29 | Low | none | revert to V2 14 |
| PC-30 | Low | none | none needed |
| PC-31 | Low | none | drop the metric rows |
| PC-32 | Low | none | per-row revert |
| PC-33 | Low | none | none needed |

## Review Status

- [x] Auto-approved (default; the run is unattended)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-15T03:06:31Z

## Plan Review Amendments (binding on the merge)

An independent reviewer checked this plan (`debate/refactor-plan-review.md`: 3 BLOCKING findings, 15 MINOR). The orchestrator accepted every finding. The merge executor MUST apply each amendment below, and where an amendment conflicts with an earlier plan row, the amendment wins. Facts re-checked by the orchestrator: `origin_repo.py` exists in both `~/.claude/skills/sc-issue-protocol/scripts/` and `src/superclaude/skills/sc-issue-protocol/scripts/`; a `doctor` target exists in the Makefile (line 23).

### Blocking findings

| Id | Amendment |
|---|---|
| RB-1 | Replace PC-04 (d). The per-run grading-override file is NOT a revert brake: no shipped file reads it (Grep over `src/` and `tests/`, per the review), and a carrier would win over it under PC-06. The spec states that the only brake is the three-step revert (edit the registry row and the digest, reinstall or force-refresh, re-run the drift test), with detection by the install check of PC-04 (e). The unreinstalled machines that keep the new rule until a refresh are named as a residual risk with the release-note mitigation, and the safety revert trigger RT1 acts through the three-step revert, not through an override file. Remove "per-run override" from the PC-04 row of the Risk Summary and from GR11 where it is described as a brake. If the owner wants a no-reinstall brake, it is a new owner decision (a named file every carrier digest reads, with format, writer and precedence stated), not a given. |
| RB-2 | Extend PC-24 with `src/superclaude/agents/rf-qa-qualitative.md:990` (Rule 6, "Contradictions are always IMPORTANT or CRITICAL ... never minor") and `src/superclaude/templates/documents/agent_template_qa.md:333` (same text; stage 4). `tests/audit/test_severity_floor_unweakened.py:57-61` pins Rule 6 verbatim and hashes the Critical Rules block. New owner decision OD16: either (a) keep Rule 6 as a named mechanical gate mapped to condition 1 (a contradiction is blocking when it touches a decision basis, a quoted number or a required deliverable), or (b) rewrite Rule 6 so that a contradiction nothing rests on is a follow-up, and re-pin the test to the new text in the same change. Recommendation: (b), at stage 3 (rf-qa family pilot) with the test re-pinned in the same change, because Rule 6 is exactly the "contradiction is blocking whatever its consequence" case the issue targets; until the owner decides, Rule 6 stays and metric M12 notes it as a known counter-example. The stage 0 inventory of fixed FAIL lines is a frozen Grep with named patterns (see RM-14). |
| RB-3 | Replace the hard-coded repository in PC-21, OD15 and the INV-013 row. The filing target is `<R>`, resolved from the `origin` remote with the existing `origin_repo.py` (the one mechanism `sc-issue-protocol` uses, `sc-issue-protocol/SKILL.md:72`), and every `gh` form is spelled with that `<R>` (`--repo <R>`, `repos/<R>/...`), never the `{owner}/{repo}` placeholder. A separate guard: when `<R>` is the IronClaude repository it must be `IronbellyOrg/IronClaude`, never the upstream parent `SuperClaude-Org/SuperClaude_Framework`; any other resolution means stop and record only. Recommended command shape for the consent-bound body: `gh issue create --repo <R> --title ... --body-file <the approved file>`. Owner decision OD15 gains the option "follow-up filing is limited to this repository in version 1" with a recommendation of yes for version 1. |

### Minor findings (adopted as requirements or notes)

| Id | Amendment |
|---|---|
| RM-1 | PC-18: the ledger path is fixed before dispatch; nested ledgers appear only through nested contracts and are never double-counted; the ledger is listed in `artifacts` only when it is a tracked path. PC-22: add one sentence for each. |
| RM-2 | One tag only: `consumer-unknown`. The BW-12 outcome (re-asked once, still no consumer) is `consumer-unknown` with a `reasked` flag; `disputed` is dropped. |
| RM-3 | One table: tags `unsettled`, `consumer-unknown` and `protected-risk-dispute` are all counted in the single `show_user` counter of PC-22 (three keys stay), the row tag gives the detail, and all three groups are listed first in the end-of-run offer as "needs your decision". They are not in the consent set for batch filing unless the user selects them. |
| RM-4 | Add a test: NA is reachable only from the deliverable-kind declaration, never from a failed or skipped call (`tri(q, None)` gives UNSET). State the 72 extra lowering moves from UNSET to NA on M or C (2,560 moves) as intended. |
| RM-5 | PC-14 names PC-10 (a judge answer S = Y or U on a non-blocking row forces a person prompt) as the only exception to "no classifier authority", and adds an absence rule: with no person reachable, record the row, mark the run `partial`, do not wait. |
| RM-6 | The digest sentence for unknown consequence is: "If no consumer can be established, keep the reviewer's own label and tag the row `consumer-unknown`." It is part of the pinned digest. |
| RM-7 | In the option Q mapping, a failed lookup reads as UNSET, never N. |
| RM-8 | In stage 2 the per-run offer of the carrier replaces, not adds to, the broadcast "once per loop" ask for that run; the broadcast ask applies only at gates with no carrier offer; the two test pins on that text (`tests/skills/test_review_severity_mapping.py:72,128`) move at stage 3. |
| RM-9 | Stage 2 owns the GR7 final-gate sweep and the `core/WORKER-CONTRACT.md` edit of PC-22. |
| RM-10 | The install check is a `make doctor` check backed by a pytest test, and both read the packaged (source) registry, not an installed `registry.yaml` (the installed skill folder is skipped once present, `install_skills.py:102`). |
| RM-11 | Drop the claim that blending is "measured by M10 split by carrier version" (M10 is classifier agreement). Add metric M10b: the share of reviewer runs that saw two different rule versions (injected style versus carrier digest), per carrier version. |
| RM-12 | PC-17: the evidence block uses a fence longer than any backtick run inside it; add a fixture with a triple-backtick line. |
| RM-13 | PC-21: name the size bound (starting value 60,000 characters, UNVERIFIED against GitHub's limit, to be confirmed in the plan), say that overflow parts are comments on the same issue sharing the batch id, and require reconcile to find all parts. |
| RM-14 | PC-24's inventory is a frozen Grep, not a remembered list: patterns `= FAIL`, `that's a FAIL`, `regardless of severity`, `highest severity`, `never minor`, `always IMPORTANT`, run over `src/superclaude/{agents,skills,templates,rules}` at stage 0 and stored with the stage 0 results. Known extra rf-qa lines: 221, 316, 333, 334, 494, 548. |
| RM-15 | PC-16 and PC-17 must state their relation to the existing typed finding ledger (`src/superclaude/cli/review/ledger.py`, schema `review-ledger/1`, its `review ledger` command and the `sc-review-ledger` skill): version 1 is a separate human-readable markdown ledger in the run folder, with a mapping rule to `review-ledger/1` rows left to the plan, and a run of the `reuse-auditor` agent before any new writer or reader is built; PC-15's new subcommand must not clash with the existing `review` command names. |
