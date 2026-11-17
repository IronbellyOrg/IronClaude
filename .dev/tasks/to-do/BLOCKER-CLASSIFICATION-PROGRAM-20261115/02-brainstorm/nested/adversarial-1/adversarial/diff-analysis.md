# Diff Analysis: SPEC Comparison (blocker classification, record and offer)

## Metadata

- Generated: 2026-11-15T02:09:50Z
- Artifact type: SPEC (requirements and design options), all three answering `02-brainstorm/seed-brief.md`
- Variants compared: 3 (Variant 1 opus architect, Variant 2 sonnet analyzer, Variant 3 haiku backend)
- Total differences found: 65 (structural, content, contradictions and unique contributions)
- Categories: structural (12), content (22), contradictions (13), unique (18)
- Shared assumptions: 14 (STATED 10, UNSTATED 3, CONTRADICTED 1); promoted [SHARED-ASSUMPTION] points: 4
- Level tags (S, C, X, A rows, 61 in all): L1 3, L2 29, L3 29
- Inputs (folder `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/`):
  - `nested/adversarial-1/adversarial/variant-1-opus-architect.md` (537 lines)
  - `nested/adversarial-1/adversarial/variant-2-sonnet-analyzer.md` (691 lines)
  - `nested/adversarial-1/adversarial/variant-3-haiku-backend.md` (637 lines)
  - `seed-brief.md` (67 lines) and `blocker_truth_table_sketch.py` (77 lines)

Level distribution per category:

| Category | L1 | L2 | L3 | Rows |
|---|---|---|---|---|
| Structural (S) | 2 | 10 | 0 | 12 |
| Content (C) | 1 | 9 | 12 | 22 |
| Contradictions (X) | 0 | 4 | 9 | 13 |
| Shared assumptions (A) | 0 | 6 | 8 | 14 |
| Total | 3 | 29 | 29 | 61 |

- Live fact checks made for this analysis: 30 (Grep, Read, `grep`, `stat`, `cmp`, two `uv run python` runs of the truth-table sketch); listed in the rows and in "Fact checks that settle contradictions"

## Structural Differences

Variant 1 = opus architect (`variant-1-opus-architect.md`, 537 lines). Variant 2 = sonnet analyzer (`variant-2-sonnet-analyzer.md`, 691 lines). Variant 3 = haiku backend (`variant-3-haiku-backend.md`, 637 lines).

| # | Area | Variant 1 | Variant 2 | Variant 3 | Level | Severity |
|---|---|---|---|---|---|---|
| S-001 | Top-level organization | 16 sections (0 to 15); weight on shared package (7), extension points (8), file list (9), rollout (11) | 17 sections plus 15b "order of work"; adds a root-cause section (2) and a worked-examples section (5) before the ledger | 14 sections; one-sentence-per-line prose; adds an operational failure-mode section (12); no examples section | L2 | Low |
| S-002 | Evidence labelling | "(checked)" inline marks plus a 17-row verification table (15.1) and a false-claims list (15.2) | every repo statement tagged [V], [E], [J] or [U]; 18 spot checks (16.1); 8 false or weak input claims (16.2) | no inline tags; a 12-row "spot-checked" table (14) and a short corrections paragraph | L1 | Medium |
| S-003 | Root-cause analysis | none as a section; problem statement lists 4 maintenance problems | six causes RC1 to RC6, each mapped to a remedy; RC1 (wording) is only one of six | none; problem statement is 4 short paragraphs | L2 | High |
| S-004 | Worked examples | inline examples inside the class table (P3-001, P3-002, NEW-1, NEW-2) | 14 graded cases (10 from run 2 Gate 1, 4 constructed) with old versus proposed verdict and the named consumer | none | L2 | Medium |
| S-005 | Shape of the single source | a delegate-only skill folder `sc-review-severity/` with 6 files: `SKILL.md`, `refs/rule.md`, `refs/scale-map.md`, `refs/follow-up-ledger.md`, `refs/classifier-questions.md`, `refs/registry.yaml` | one file `core/REVIEW-SEVERITY.md` holding a marked block plus long text | one file `core/REVIEW-SEVERITY.md` plus a "generated parity copy" for plugin consumers | L2 | High |
| S-006 | Ledger structure | header block (4 fields) plus one 12-column table | header block plus two tables: full Medium rows (13 columns) and short Note rows | metadata (7 fields) plus four fixed tables: Items (13 columns), Observations, Offers, Filings | L2 | High |
| S-007 | Classifier code layout | four layers L1 questions, L2 state builder, L3 judges, L4 decision; code under `src/superclaude/cli/review/` with a CLI `superclaude review classify --ledger` (the `review` click group exists, verified `src/superclaude/cli/review/__init__.py:14`) | location left to the plan ("location is a plan decision") | judge request and response contract specified; production path deliberately not chosen | L2 | Medium |
| S-008 | Extension contracts | dedicated section 8: new gate, judge, scale, deliverable kind, rule change | none | none | L2 | Low |
| S-009 | Rollout stage count | 5 stages (0 measure, 1 scaffold and shadow, 2 broadcast and QA family, 3 remaining copies, 4 optional gating) | 5 stages (0 with 0a/0b/0c, 1 shadow and ledger with old rule, 2 reach points, 3 other copies, 4 own-scale primitives) | 6 stages (0 evidence, 1 offline contract, 2 shadow, 3 default pilot, 4 propagate, 5 optional authority) | L2 | Medium |
| S-010 | Test plan shape | 9 existing modules in a table plus new T1 to T8 | 8 existing modules plus new T1 to T9 | 8 modules plus 2 fixtures plus a transitive module, then an unnumbered acceptance-case list | L2 | Medium |
| S-011 | Metrics and triggers shape | M1 to M7 plus 5 numbered revert triggers | M1 to M10 plus RT1 to RT8 with a statistical-power column | unnumbered metric bullets plus incident-style disable rules | L2 | Medium |
| S-012 | Risks and decisions tables | K1 to K11 with likelihood and impact; D1 to D11 | R1 to R13 with an evidence column; D1 to D13 | 11 failure modes with a required response, no likelihood; 10 unnumbered decision rows | L1 | Low |

## Content Differences

Rows marked "Verified:" record a live check made for this analysis (Grep, Read, `grep`, `stat`, `cmp` or `uv run python`), with the file and line used.

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Level | Severity |
|---|---|---|---|---|---|---|
| C-001 | Blocking condition 1 (consequence) | "A decision rests on it": a design choice, recommendation, destination, outcome or a number the recommendation depends on would be wrong or unsupported | "Decision": counterfactual on a **named** consumer; adds "acceptance check" and "the stated reason for such an item is false or unsupported" | "Consequential error": adds "required behavior"; "A wrong number used in an acceptance check blocks even if a recommendation stays the same" | L3 | High |
| C-002 | Conditions 2 and 3 | Missing deliverable, section or step, presence checked by code first; Safety includes "act outside the declared scope" | Missing "named by the task, the template or the acceptance criteria"; Safety same as V1 | Missing includes "explicit contractual obligation" and "absent or contradicted in substance"; Protected risk requires the reviewer to "name the affected action and evidence, not merely write 'security'"; unverified protected-risk claims are "not notes" | L3 | Medium |
| C-003 | Names of the non-blocking classes | FOLLOW_UP (today's Medium) and NOTE (today's minor) | Medium and Note (keeps the existing word Medium) | follow-up ("called Medium where useful") and note | L1 | Low |
| C-004 | Required per-finding justification | `why_not_blocking` must name which condition fails; cannot be empty for FOLLOW_UP (R3) | every finding carries `rests_on` (`none`, `unknown`, or the named consumer); a finding without it is invalid (GR2) | `nonblocking_basis`: "Which blocking conditions were tested and why none applies" | L3 | Medium |
| C-005 | Drift-test design | registry-driven: T1 digest equality per `refs/registry.yaml` row, T2 reverse scan of `src/` and `plugins/`, T3 pointer order, T4 scale map, T5 ledger schema | manifest of carriers plus a reverse scan for the block's opening phrase and the old P1 phrase | "canonical content, generated byte parity, reference reachability and markers"; mismatched consumer retains the old gate | L2 | Medium |
| C-006 | Offer wording and options | 4 options (resolve now, one issue, one per weakness, keep); notes never offered alone; one-line no-question form below a threshold (D5: 10 notes) | 4 options, "File one issue" marked Recommended; shows counts plus the first five rows; `consumer-unknown` rows first | 3 options (resolve as separate work, file one, leave); notes opt-in for filing; offer names exact ids and a snapshot digest | L2 | Low |
| C-007 | "Resolve now" semantics | one fix pass, no re-review unless the fix edits a span cited by a blocking finding (R9) | one fix agent on picked ids, runs L2 mechanical checks, stops if a picked item proves decision-bearing; no re-review loop | "separately authorized work after the gate"; re-enters normal scope and planning rules | L3 | Medium |
| C-008 | Ledger identity and persistence | `FU-<gate>-<n>` stable within the run; `status` written back so nothing is offered twice | `FU-<gate>-<n>` stable across reviews; de-dup key = location plus quote hash | `FU-000001` run-scoped, never recycled; identity tuple digest; Observations table; `revision` with atomic rewrite; stale-writer and corrupt-file rules | L3 | High |
| C-009 | Ledger location per primitive | 5-row table: `qa/follow-ups.md` for task family; `<report-dir>` for spec-panel and reflect; implement index over `notes.md`; pr-submit under `.dev/pr-monitor/`; tasklist beside `ValidationReport.md` | 5-row table: same task and spec-panel paths; implement keeps `notes.md` with a pointer row; pr-submit keeps its own list | one rule: `<run-report-dir>/qa/follow-ups.md` when a QA dir exists, else `<run-report-dir>/follow-ups.md`; nested runs keep separate ledgers | L2 | Medium |
| C-010 | Unattended contract keys | `follow_up_ledger`, `follow_up_counts {follow_up, note, show_user}` | `follow_up_ledger` plus "a count" | six keys: `follow_up_schema`, `follow_up_ledger`, `follow_up_count`, `note_count`, `follow_up_capture_state`, `follow_up_offer_state`. Verified: no `follow_up` key exists today (0 matches in `src/superclaude/core/WORKER-CONTRACT.md`) | L2 | Medium |
| C-011 | One-issue filing | B1: `/sc:issue --create @<file> --mode feature --type <area> --depth quick` | Option A: same path with `--mode bug --depth standard` | no flags fixed; adds a batch-id marker, `prepared`/`posting`/`reconcile`/`filed` states and "Never retry creation until absence ... has been established". Verified for all three: `src/superclaude/commands/issue.md` has no `--repo`, `--dry-run` or `--preview` (Grep, 0 matches) | L3 | Medium |
| C-012 | Classifier question set | all 10 questions (W, D, E, M, S, C decisive; T, F, I, G explanatory) | 6 questions only; drops T, F, I, G from the gating path; rewords S to "in a way the task did not ask for"; option Q replaces D at upstream gates | all 10; "T, F, I and G explain follow-up placement; they never cancel S, M or a confirmed obligation" | L2 | Medium |
| C-013 | Source of `decision_basis` | 5-row table by deliverable kind; unknown kind leaves D UNSET, so wrong-outcome findings go to SHOW_USER | 5-row table plus three ways (producer-declared, reviewer-named, code check); recommends B plus C, A only for upstream outputs; upstream research inputs have no basis today | 5-row table; "Other: caller-supplied basis with evidence; otherwise UNSET and no automatic downgrade" | L3 | Medium |
| C-014 | Description of the sketch's UNSET behaviour | says `wrong()` returns N for (N, UNSET) and calls this "the more useful behaviour"; spec text must match the code | counts 432 of 18,432 UNSET-to-answered moves that lower the verdict (216 on D, 108 on W, 108 on E); requires a separate UNSET test | the sketch returns FOLLOW_UP with S UNSET; monotonicity loop excludes UNSET; "The code wins as the description of today's sketch, not as the desired policy". Verified (uv run python on `blocker_truth_table_sketch.py`): all three statements are true; `wrong(N, UNSET)` = N and `wrong(UNSET, N)` = N; 432 lowering moves exactly as V2 says | L3 | High |
| C-015 | Judge runtime bounds | chain Jev, LlmJudge, ReviewerJudge, plus FixtureJudge; 3 replicates, spread above 0.20 is U | same chain; replicates vary field order to defeat vendor caching; `finding-grader` precedent is installed only. Verified: `~/.claude/agents/finding-grader.md` exists, `src/superclaude/agents/finding-grader.md` does not | adds 10 s attempt, one retry, 30 s per-finding budget, circuit breaker, cache key list, labels hidden from the judge to reduce anchoring | L3 | Medium |
| C-016 | Guardrail sets | R1 to R10; sampled audit of 10 percent, at least 3 rows; escalation by stated consequence | GR1 to GR11; vocabulary scan for safety words; final-gate sweep GR7; seeded-defect recall; blind auditor shown no rule text | 13 bullets; "Review all protected-risk disagreements, not just a random subset"; preserve regression before monotonicity | L3 | Medium |
| C-017 | Consolidation and fix-pass changes | consolidation only appends non-blocking rows to the ledger; merge rule unchanged | L1 replaces "highest severity wins"; L2 fix pass runs mechanical checks before re-review; L3 adds an `accepted-blocker` choice at the cap; L4 consumer line per phase output. Verified: `src/superclaude/skills/task/SKILL.md:252` contains "highest severity" | "Consolidate repeated observations into one finding identity"; merge rule unchanged; caps unchanged | L3 | High |
| C-018 | Own-scale primitives | tasklist Medium becomes FOLLOW_UP at stage 3; reflect Drift change only if D7 (not v1); spec-panel CRITICAL narrowed; roadmap validate prompt gets the conditions | tasklist Medium aligned after data (D7); reflect deferred (D6); spec-panel CRITICAL and dimensional-mismatch narrowed | tasklist only "in an explicitly reviewed adapter stage"; reflect unchanged in v1; adds the rf-qa-qualitative contradiction floor as a separate approval. Verified: tasklist "High or Medium (blocking)" occurs 4 times (`sc-tasklist-protocol/SKILL.md:1439,1610,1614` plus one more line); reflect gate at `sc-reflect-protocol/SKILL.md:1540` | L2 | Medium |
| C-019 | File-change list and counts | P1 11 files/11 lines; cap P3 12 files; S5 7 files; `follow-up candidates` 3 files/7; `2 fix cycles` 22 files/120 lines; totals "11 group A, about 9 group B, 1 new skill folder of 6 files" | same P1 list; `2 fix cycles` "22 files and 139 times [E]"; estimate 30 to 40 source files | same P1 list; "22 files and 120 matching lines, not 120 literal occurrences. The enrichment's 139 occurrences counts repeated matches within lines"; adds `issue.md`, `sc-issue-protocol/refs/create.md`, `Makefile`, build script, `install_core.py`, plugin twins. Verified: P1 11 files, 11 lines; cap 12 files; S5 7 files; `follow-up candidates` 3 files, 7 lines; `2 fix cycles` 22 files, 120 lines, 139 occurrences by `grep -o`. All three are right on their own measure; V3's explanation of 139 is correct | L2 | Medium |
| C-020 | Existing test inventory | 9 modules: the 8 from enrichment plus `tests/review/test_review_rules_text.py` (pins `"src/superclaude" not in TEXT`) | 8 modules plus 2 fixtures | 8 modules plus 2 fixtures plus transitive `tests/audit/test_invariant_preservation_NFR_6_through_10.py`. Verified: `test_review_rules_text.py:92` asserts `"src/superclaude" not in TEXT`; `test_invariant_preservation_NFR_6_through_10.py:95-101` imports `FAIL_BULLET` and `PASS_BULLET` from `test_nfr_conv_9_zero_trust`; both fixtures exist. Union is 10 modules; no variant lists all 10 | L2 | Medium |
| C-021 | Use of run-2 evidence | accepts "about 25 minutes" and "about 45 percent on research gates (one sample)" | treats the override as a retrospective re-grade; the 5 downgrade candidates were fixed anyway; Gate 1 passed at review 3 | treats run-2 numbers as "historical observations from the inputs, not independently reproduced" | L2 | Medium |
| C-022 | Mirrors and install drift | project `.claude/` holds 6 P1 copies; Grep tool skips gitignored folders so use plain `grep`; plugin holds none | `.claude/` copies listed as [E]; R10 install drift (`install_core.py:70` skips existing files) | "Existing non-forcing installs can keep stale consumers; mixed versions must be detected"; running loop pins its rule version. Verified: `grep -rlF` finds 6 P1 copies under `.claude/` (rf-qa, rf-qa-qualitative, 2 document templates, 2 MDTM templates) and 0 under `plugins/`; `install_core.py` skips an existing destination unless forced | L3 | Medium |

### Coverage of the seed brief's required spec shape

Not diff points (no IDs, not counted); a checklist against `seed-brief.md:53` and the open questions at lines 41 to 49. "Yes" means the variant has a section that answers the item.

| Required item (seed brief) | Variant 1 | Variant 2 | Variant 3 |
|---|---|---|---|
| Problem statement | Yes (1) | Yes (1, plus root cause 2) | Yes (1) |
| Goals and non-goals | Yes (2, G1 to G6) | Yes (3, G1 to G7) | Yes (2, 8 goals) |
| Rule with three conditions and never-downgraded class | Yes (3) | Yes (4.1, quotable paragraph) | Yes (3) |
| Record-and-offer: flow | Yes (4.1, 5 steps) | Yes (6.1, 6 steps) | Yes (4.1, 9 steps) |
| Record-and-offer: ledger format | Yes (4.2) | Yes (6.2) | Yes (4.2 to 4.4) |
| Record-and-offer: offer wording | Yes (4.3) | Yes (6.3) | Yes (4.5) |
| Record-and-offer: unattended behaviour | Yes (4.4) | Yes (6.4) | Yes (4.6) |
| Record-and-offer: batching into one issue | Yes (4.5, B1 to B3) | Yes (6.5, A to C) | Yes (4.5) |
| Classifier: questions, truth table, confidence | Yes (5.2) | Yes (7.2 to 7.4) | Yes (5.1, 5.3) |
| Classifier: key dependency, fallback judges, shadow mode | Yes (5.4, 5.5) | Yes (7.5) | Yes (5.4, 5.5) |
| Guardrails | Yes (6, R1 to R10) | Yes (8, GR1 to GR11) | Yes (6, 13 bullets) |
| Shared rule document and drift test | Yes (7.2 to 7.4) | Yes (9.1, 9.2) | Yes (7) |
| Which primitives keep their own scale | Yes (7.5, 11 families) | Yes (9.3, 7 rows) | Yes (7, 8 rows) |
| File list from Grep with counts and patterns | Yes (9.1 P1 to P8 with patterns) | Yes (10.1 to 10.3) | Yes (8, 4 patterns) |
| Tests that pin the rule text and what changes | Yes (10) | Yes (11) | Yes (9) |
| Rollout stages | Yes (11) | Yes (12) | Yes (10) |
| Metrics and revert triggers | Yes (12) | Yes (13) | Yes (11) |
| Risks | Yes (13) | Yes (14) | Yes (12) |
| Owner decisions with a recommendation | Yes (14, D1 to D11) | Yes (15, D1 to D13) | Yes (13, 10 rows) |
| What was verified and not | Yes (15) | Yes (16) | Yes (14) |
| Open question: reconcile 21 files and 109 occurrences | Yes (explains the 21 as listed paths, 8 without the sentence) | Yes (same explanation, [E]) | Partly (states the figure is not reproduced; does not explain the 21) |
| Open question: may the classifier fill `qa.md`'s four answers | Yes (5.5 and D8: no in v1) | Not answered (D8 covers a "rests on" qualifier only) | Yes (decision row: no in v1) |
| Open question: where `decision_basis` comes from | Yes (5.3) | Yes (4.3) | Yes (5.2) |
| Open question: privacy and key request | Yes (D1, D2) | Yes (D3) | Yes (two decision rows) |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Level | Impact |
|---|---|---|---|---|---|---|
| X-001 | Where the shared rule lives, and whether it gets both surfaces | "Recommendation: a delegate-only skill, `src/superclaude/skills/sc-review-severity/`. It is the only location that satisfies both surfaces" | "`src/superclaude/core/REVIEW-SEVERITY.md` ... **Recommended**" | "Proposed canonical authoring file: `src/superclaude/core/REVIEW-SEVERITY.md`. ... with project `.claude/REVIEW-SEVERITY.md` as the explicit development surface" | L2 | High |
| X-002 | What each carrier holds | "a short, fenced digest block copied verbatim into each primitive ... one pointer line to the full rule" (about six bullets) | "Every consumer carries that block inline, word for word" (the one paragraph of 4.1) and "A pointer alone depends on a reviewer choosing to read a file" | "Prefer short references plus a rule-version marker over eleven hand-edited full definitions" | L2 | High |
| X-003 | Outcome when the consequence cannot be established | "if you still cannot tell, the finding is shown to the user (the classifier's SHOW_USER outcome), not filed silently" | table row "could not be established: Medium, tagged `consumer-unknown`, listed first in the offer" (non-blocking, never halts) | "Unknown is not no. An unavailable input or ambiguous consequence requires escalation, or retention of the protocol's existing label, never automatic demotion" | L3 | High |
| X-004 | Offer cadence | "At the end of the top-level run (not per gate, not per loop), the top-level session reads the ledger and makes one offer" | "once per run, plus at any escalation halt" | "At loop completion, the attended top-level session offers the recorded set once" and "One offer covers the loop's final consolidated set, not each fix cycle". Verified: today's text is "once per loop" (`src/superclaude/output-styles/pragmatic.md:230`) | L3 | Medium |
| X-005 | May the classifier ever auto-downgrade | stage 4: "only the downgrade path, and only above tau_down, may move a reviewer's blocking label to FOLLOW_UP" | "It never auto-downgrades." (D4: "No auto-downgrade") | stage 5: "Owner explicitly authorizes a calibrated routing policy"; "Allow classifier demotion after shadow? Separate decision" | L3 | High |
| X-006 | Confidence for a BLOCKING W-and-D path | "for BLOCKING by W and D it is min(pW, pD)"; "auto-confirm blocking needs 0.70" | "`min(pW, pD)` is an upper bound on the joint probability, so it flatters a confirm"; report ordinal bands until calibrated | "a high minimum cannot by itself justify confidence that both conditions hold"; "dependence-safe lower bound is max(0, pW + pD - 1)". Verified: the input itself says "the min is an upper bound under any correlation" (`02-brainstorm/jev-uses.md:194`); V1 adopts it as the confirm score without restating that limit | L3 | Medium |
| X-007 | A missing (UNSET) safety answer | R1 covers only "S = U lifts to SHOW_USER"; calls the sketch's behaviour "the more useful behaviour" | "UNSET means 'send to a person'" | "It can also return FOLLOW_UP with S UNSET ... That permits a missing safety answer to look safer than an uncertain answer"; required policy: missing decisive inputs or unresolved safety produce SHOW_USER | L3 | High |
| X-008 | Scope of the monotonicity claim | "it printed `cases 4096 monotonicity violations 0` (checked)"; new test T6 "monotone in every input" | "'Monotone in every input' holds on the answered scale N, U, Y only"; 432 lowering moves | "Its monotonicity loop excludes comparisons involving UNSET, so its check is narrower than an unconditional claim". Verified: the sketch's check skips moves where `UNSET in (base[i], new)` (`blocker_truth_table_sketch.py:67-69`); output `cases 4096 monotonicity violations 0` is true; V1's T6 as worded would fail against the sketch | L3 | Medium |
| X-009 | Privacy of the LLM fallback judge | "Everything except `JevJudge` works without a key: ... the five validation runs with `LlmJudge`"; D1 "otherwise run with `LlmJudge` only" | D3 "else use the LLM judge only" | "Privacy denial skips all unapproved external judges, including the fallback model" | L3 | Medium |
| X-010 | Gate 1 cost of the table-pipe defects | "Gate 1 needed a third review and a second fix cycle (about 25 minutes) for the two table defects alone" | "The stated cost 'about 25 minutes' ... is not supported by file times"; "It is loose to say the defects 'failed a gate'" | "It reports an additional fix cycle taking about 25 minutes ... not independently reproduced" | L2 | Medium |
| X-011 | Grade of NEW-1 and NEW-2 | listed as a NOTE example: "a table-pipe defect that changes no cell a later phase reads (NEW-1, NEW-2)" | "Blocking if a consumer reads the table by column position, else Note"; quotes the verifier that Destination reads wrong | rule only: "A table defect that changes a destination blocks; a cosmetic pipe defect need not" | L3 | Medium |
| X-012 | Are SHOW_USER items ledger rows | `class` column holds "FOLLOW_UP, NOTE or SHOW_USER" | SHOW_USER rows get tag `unsettled` in the ledger | "`follow-up` or `note`; unresolved classifier decisions stay outside this non-blocking set" | L3 | Low |
| X-013 | Number of existing test modules that pin the rule | 9 (adds `tests/review/test_review_rules_text.py`) | "Eight test modules pin the rule or the Medium text" | "That count is not exhaustive: live Read also found a transitive PASS/FAIL pin in `tests/audit/test_invariant_preservation_NFR_6_through_10.py`". Verified (C-020): both extra modules are real pins; the correct union is 10 | L2 | Low |

### Fact checks that settle contradictions

- X-001 (location). `Makefile` sync-dev (lines 108 to 158) copies `skills/`, `agents/`, `commands/`, hook scripts, `session-init.sh` and `templates/`; it has no `core/` step. `.claude/WORKER-CONTRACT.md` does not exist, so the core precedent has no project copy. V1 is right that `core/` gets no project `.claude/` surface; V3's `.claude/REVIEW-SEVERITY.md` names a path nothing creates today (V3 itself says the plan "must add generation"). `src/superclaude/cli/install_core.py` globs `core/*.md` and skips only existing destinations unless forced, so a new core name installs with no installer change (V2 and V3 right). Plugin: `scripts/build_superclaude_plugin.py:16` sets `PLUGIN_SRC = ROOT / "plugins" / "superclaude"` and line 76 copies that tree's `agents, commands, hooks, rules, scripts, skills`; a new `src/` skill or `src/` rule reaches the plugin only by a hand copy, so V1's "In the plugin build: yes" for `rules/prompts` overstates it. `plugins/superclaude/skills/` holds 4 skills (V1 right). The seed brief (fact 3) names `core/REVIEW-SEVERITY.md`; V1 departs from it with a stated reason, which is not a factual error.
- X-007 (UNSET safety). `uv run python` on the sketch: of the 1,024 states with S = UNSET, 511 give BLOCKING, 297 SHOW_USER, 108 FOLLOW_UP and 108 NOTE; `verdict(UNSET,N,N,Y,N,N)` = FOLLOW_UP while `verdict(U,N,N,Y,N,N)` = SHOW_USER. V3 is right. V2's "UNSET means 'send to a person'" is false for S, and for D = UNSET with wrong = N (`verdict(N,N,N,N,N,UNSET)` = NOTE). V1's R4 claim "D = UNSET never gives FOLLOW_UP for a wrong-outcome finding" is true (`WD` rows `(Y, UNSET)` and `(U, UNSET)` are SHOW_USER, sketch lines 29 to 30).
- X-008 (monotonicity). The sketch's check skips moves where `UNSET in (base[i], new)` (lines 67 to 69). Its output `cases 4096 monotonicity violations 0` is true. Counting the skipped moves: 18,432 UNSET-to-answered moves, 432 lower the verdict (D 216, W 108, E 108), exactly as V2 says.
- X-010 (Gate 1 cost). `stat`: `qa-consolidated-findings-phase3.md` 11:58:47, `gate1-cycle-control.md` 12:20:21, `grading-override.md` 12:48:30 on 2026-11-14 (mtimes predate the 23:30 commit, so they are original write times). `gate1-cycle-control.md:24` header says "12:23", later than the file's last write; line 38 says "Final verdict: PASS at review 3". V2's reading holds; the seed brief's "Gate 1 cost about 25 minutes extra" is not supported by these timestamps (about 22 minutes for the whole loop after consolidation).
- X-011 (NEW-1). `gate1-cycle-control.md:9`: NEW-1 has "8 pipes instead of 7, the Destination cell reads wrong". V1's example assumes the opposite of the recorded effect; under V1's own table-shape rule the row is condition 1 if a parser reads that cell.
- Seed-brief reconciliation. The seed's "`2 fix cycles` alone matches 22 files, 139 times" is an occurrence count (`grep -rhoF` gives 139; matching lines are 120). No variant contradicts it once the measure is named.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | Variant 1 | Extension contracts (section 8): a new gate, judge, severity scale or deliverable kind is "one registry row plus tests"; an unsupported deliverable kind degrades to "ask", not to "hide" | Medium |
| U-002 | Variant 1 | `refs/registry.yaml` listing every digest carrier with kind, stage and digest version, so each stage switch and revert is a mechanical, test-checked edit; legacy rows tolerated until stage 3 makes T2 strict | High |
| U-003 | Variant 1 | Method caveat: the Grep tool skips gitignored folders, so counting `.claude/` mirror copies needs plain `grep` (verified: 6 copies found by `grep -rlF`, see C-022) | Medium |
| U-004 | Variant 1 | Scale-map table with a row per severity family, each label mapped to BLOCKING, FOLLOW_UP or NOTE, plus a test that each named file and label exists (T4) | Medium |
| U-005 | Variant 1 | Notes that templates already instantiated under `.dev/tasks/` keep the old text and are deliberately not migrated | Low |
| U-006 | Variant 2 | Root-cause model RC1 to RC6: "highest severity wins" merging (`task/SKILL.md:252`, verified), fix-induced defects, upstream gates without a decision basis, no record path, word overload; the rule change alone addresses only RC1 | High |
| U-007 | Variant 2 | Fix-pass mechanical checks (L2: pipe count, byte-present quotes, recounts) and an `origin: fix-induced` tag with metric M9; directly targets the NEW-1/NEW-2 cycle | High |
| U-008 | Variant 2 | Statistical design: Wilson intervals, "3 divided by n" upper bound, revert trigger stated as a lower interval bound (RT2: 4 of 60), audit strata and oversampling | High |
| U-009 | Variant 2 | Seeded-defect recall test and a retrospective escape test on run 2 (stage 0b) that does not depend on the rule that graded the findings | Medium |
| U-010 | Variant 2 | Final-gate sweep GR7: every open Medium is re-tested against the final deliverable's decision-basis sections, closing the upstream-gate gap | Medium |
| U-011 | Variant 2 | Critique of the validation design: circular labels when Score levels reuse the human rubric, selection bias of a blocking-only table, rows without a decision basis | Medium |
| U-012 | Variant 2 | Worked grading of 10 real Gate 1 findings plus 4 constructed cases, including a bundled finding split into parts (P3-007) | Medium |
| U-013 | Variant 3 | Ledger concurrency and crash safety: single writer, `revision` counter, atomic replace, stale-writer re-read, malformed ledger preserved and reported as capture failure | High |
| U-014 | Variant 3 | Idempotent filing protocol: batch id digest in the issue body, `prepared`/`posting`/`reconcile`/`filed` states, never blind-retry creation, fork-only targeting | High |
| U-015 | Variant 3 | Consent binding: an offer records `set_digest`; a changed set or materially changed body needs renewed consent; `answer_source` points at the user's own instruction | Medium |
| U-016 | Variant 3 | Judge request and response contract: labels and author hidden from the judge, probability validation, typed failures, time budgets, circuit breaker, cache key including decision-basis digest | Medium |
| U-017 | Variant 3 | Mapping of the four existing record shapes (rf-qa table, implement notes line, troubleshoot follow-up task, reflect deviation block) into the ledger contract | Medium |
| U-018 | Variant 3 | Secret and payload logging policy: key only in the process environment, digests by default, opt-in restricted full-payload logging, no hidden unredacted twin | Low |

## Shared Assumptions

For each point all three variants agree on, the question is what must be true for the agreement to hold. STATED = at least one variant states the precondition; UNSTATED = none does; CONTRADICTED = repo evidence or a variant's own material contradicts it.

| # | Point all three agree on | What must be true | Classification | Level | Impact |
|---|---|---|---|---|---|
| A-001 | The definition sentence lives in 11 files under `src/superclaude` | the exact P1 sentence is the carrier of the meaning; paraphrases elsewhere are handled separately. Verified: 11 files, 11 lines. V2 alone notes the reviewer brief at `pragmatic.md:221` also tells reviewers to hunt "false claims" (verified by Read) | STATED | L2 | Medium |
| A-002 | Three blocking conditions (consequence, missing, safety) replace the defect-kind list | a gate reviewer can see what the deliverable rests on when it grades | STATED (V2 RC4, V1 5.3, V3 UNSET rule) | L3 | High |
| A-003 | Cap stays at 2 fix cycles (3 reviews); halts count blocking only | the cap text and `CANONICAL_CAP_TEXT` stay word for word. Verified: `tests/skills/test_review_severity_rule.py:215` pins it | STATED | L3 | Low |
| A-004 | No issue without the user's answer; unattended runs only record | someone with authority reads the ledger after an unattended run | STATED (V1 coordinator rule, V2 R5, V3 4.6) | L3 | Medium |
| A-005 | Classifier thresholds are fitted on 30 or more blind-scored past findings produced by other program steps | that table will exist, be large enough, and cover non-blocking-but-real cases | UNSTATED | L2 | High |
| A-006 | The ledger is a Markdown file named `follow-ups.md` | Markdown table rows survive pipes, newlines and backticks in finding text (the exact defect behind NEW-1/NEW-2) | STATED (V3 only: "choose and test one escaping convention for pipes") | L3 | Medium |
| A-007 | `pragmatic.md` is the broadcast carrier that reaches every subagent | the SubagentStart hook is registered wherever reviews run and `~/.claude/output-styles/pragmatic.md` is installed | UNSTATED | L2 | Medium |
| A-008 | Required items and decision basis come from "the template's required section list" or headings | templates expose required sections in a form code can read | UNSTATED | L3 | Medium |
| A-009 | The verdict set includes UNDETERMINED, which hands the finding to the next judge | the decision table emits UNDETERMINED when no usable answer exists | CONTRADICTED | L3 | Medium |
| A-010 | `/sc:implement` `refs/qa.md` keeps its own four-answer model in v1 | its broader `false-claim` blocker is an accepted divergence. Verified: `pragmatic.md:228` names it as the exemplar protocol with its own model | STATED | L2 | Low |
| A-011 | Shadow mode first; no Jev call, account or key in this step | no key exists. Input check only (`jev-uses.md:15`), not re-run here | STATED | L2 | Low |
| A-012 | Medium and Note findings are never rechecked | a later fix cannot turn a recorded item into a decision-bearing one unnoticed | STATED (V1 R6 audit, V2 GR7 sweep, V3 linked escalation) | L3 | Medium |
| A-013 | Filing goes through `/sc:issue --create @file` from an attended session | `/sc:issue` takes an `@path` description and is never a worker. Verified: `WORKER-CONTRACT.md:23` never-as-worker list includes `/sc:issue` | STATED | L2 | Low |
| A-014 | Installed copies pick up the new rule | installs are refreshed; `install_core.py` skips existing files unless forced | STATED (V2 R10, V3 stale-install rule; V1 notes line 70 only as a fact) | L3 | Medium |

### Promoted shared-assumption points

| # | Tag | Assumption | Impact | Status |
|---|---|---|---|---|
| A-005 | [SHARED-ASSUMPTION] | The 30-plus blind-scored findings table will exist in time and suit calibration. The seed brief says "step 01 inventory was empty when this ran" (`seed-brief.md:25`). No variant says what happens to stages 0 to 2 if the table is late, small, or holds only past blocking findings (V2 names the selection bias but not the missing-table case) | High: every classifier stage and every threshold depends on it; the rule change does not | Open, unverified |
| A-007 | [SHARED-ASSUMPTION] | Broadcast via the output style reaches every reviewer. Verified: `src/superclaude/hooks/scripts/pragmatic-subagent.js:7-18` injects the installed file unconditionally and exits 1 if it is missing; whether the hook is registered in every environment (plugin-only installs, other users) was not checked | Medium: if not registered, the digest or block in `pragmatic.md` never reaches subagents and only per-file copies grade | Open, partly verified |
| A-008 | [SHARED-ASSUMPTION] | Templates give a machine-readable required-section list for the M question and for decision-basis extraction. Not checked by any variant or here | Medium: without it, M and D fall to UNSET more often, raising SHOW_USER or (V2) `consumer-unknown` share | Open, unverified |
| A-009 | [SHARED-ASSUMPTION] | UNDETERMINED is a table outcome. Verified: the sketch's `ORDER` has only NOTE, FOLLOW_UP, SHOW_USER, BLOCKING (`blocker_truth_table_sketch.py:5`), and an all-UNSET input returns SHOW_USER, not UNDETERMINED; `jev-uses.md:150` defines UNDETERMINED as "no usable answer at all". The trigger for moving to the next judge is therefore undefined in table terms | Medium: the fallback chain can stall at SHOW_USER instead of trying the next judge | Contradicted by the sketch |

## Summary

- Total structural differences: 12 (High: S-003, S-005, S-006)
- Total content differences: 22 (High: C-001, C-008, C-014, C-017)
- Total contradictions: 13 (High: X-001, X-002, X-003, X-005, X-007)
- Total unique contributions: 18 (High value: U-002, U-006, U-007, U-008, U-013, U-014)
- Total shared assumptions: 14; promoted [SHARED-ASSUMPTION]: A-005 (High), A-007, A-008, A-009 (CONTRADICTED)
- Highest-severity items: X-001 (rule location and its two surfaces), X-003 (what "unknown consequence" yields: SHOW_USER, non-blocking Medium, or keep the old label), X-007 (a missing safety answer can yield FOLLOW_UP or NOTE in the sketch), X-005 (auto-downgrade allowed or never), X-002 (inline text versus reference), C-017 (whether consolidation's "highest severity wins" changes), A-005 (calibration table may not exist)

### Variant claims found false or overstated by live check

| Variant | Claim | Finding |
|---|---|---|
| Variant 1 | `~/.claude/WORKER-CONTRACT.md` is "read by path from 81 source files (checked count)" | Not reproduced: `grep -rlF 'WORKER-CONTRACT.md' src/superclaude` gives 58 files (2 of them `.pyc`), 65 with `plugins/`; 110 occurrences under `src/superclaude` |
| Variant 1 | `rules/prompts` location is "In the plugin build: yes" | Overstated: the build copies the hand-kept `plugins/superclaude/` tree (`build_superclaude_plugin.py:16,76`), not `src/` |
| Variant 1 | NEW-1 and NEW-2 as NOTE examples of "a table-pipe defect that changes no cell a later phase reads" | Contradicted by `gate1-cycle-control.md:9` ("the Destination cell reads wrong") |
| Variant 1 | Test T6 "monotone in every input" as a property of the table | Not true of the sketch across UNSET (432 lowering moves); holds only on N, U, Y |
| Variant 2 | "UNSET means 'send to a person'" | False for S = UNSET (108 FOLLOW_UP and 108 NOTE states) and for D = UNSET with wrong = N (NOTE) |
| Variant 2 | "Eight test modules pin the rule" | Incomplete: `test_invariant_preservation_NFR_6_through_10.py` and `test_review_rules_text.py` also pin text |
| Variant 3 | Project `.claude/REVIEW-SEVERITY.md` is "the explicit development surface" | No mechanism creates it today: `Makefile` sync-dev has no `core/` step and `.claude/WORKER-CONTRACT.md` is absent; V3 flags that the plan must add generation |

### Variant claims confirmed where variants disagreed or the inputs were challenged

- V2 and V3 on `2 fix cycles`: 120 matching lines and 139 occurrences are both correct measures (22 files).
- V2's run-2 timing and "gate passed at review 3" (`gate1-cycle-control.md:24,38`; `stat` times) and marker counts (838 occurrences, 825 lines, 64 files of "minor under grading override").
- V2's 432 of 18,432 UNSET-to-answered moves (D 216, W 108, E 108); V3's S = UNSET to FOLLOW_UP; V1's and V3's reading of `wrong()` against `jev-uses.md:138` ("N only if both are N"): the sketch returns N for (N, UNSET) and (UNSET, N).
- V3's transitive pin and V1's `test_review_rules_text.py:92` pin; V1's 6 `.claude/` mirror copies and the Grep-tool caveat; V2's `finding-grader` installed-only; V2's "spec-panel differs between src and plugin" (`cmp`: differ at line 23; review-loop prompts identical).
- All three: 11 files carry the definition sentence; `/sc:issue` has no `--repo`, `--dry-run` or `--preview`; `/sc:issue` is on the never-as-worker list (`WORKER-CONTRACT.md:23`).

### Verification log

All paths are relative to the repo root unless they start with `~`. Nothing was edited except this file.

| # | Check | Method | Result |
|---|---|---|---|
| V-01 | P1 sentence `Grade every review finding as blocking or minor` under `src/superclaude` | `grep -rlF` and `grep -rnF` | 11 files, 11 lines |
| V-02 | `2 fix cycles` under `src/superclaude` | `grep -rlF`, `grep -rhF`, `grep -rhoF` | 22 files, 120 lines, 139 occurrences |
| V-03 | S5 `CRITICAL and IMPORTANT findings are blocking` | `grep -rlF` | 7 files (pragmatic, rf-qa, rf-qa-qualitative, 2 document templates, 2 MDTM templates) |
| V-04 | S5 test scope | Grep `tests/skills/test_review_severity_rule.py` | `S1_S3_FILES` at 181; `S5_FILES = S1_S3_FILES[:6]` at 193; `CANONICAL_CAP_TEXT` at 215 |
| V-05 | `canonical_rule_bullets` definition and callers | Grep | defined at line 79; 9 occurrences in 3 modules (5, 2, 2) |
| V-06 | Cap `at most 2 fix cycles (3 reviews)` | `grep -rlF` | 12 files |
| V-07 | `follow-up candidates` | `grep -rn`, `grep -rlF` | 7 lines in 3 files (pragmatic, spec-panel, review-loop prompts) |
| V-08 | Rule text at `pragmatic.md:220-231` | Read | S1 at 225, S4 at 228, S5 at 229, Medium at 230 ("once per loop"), spec-panel scale at 231; reviewer brief "false claims" at 221 |
| V-09 | `make sync-dev` coverage | `sed -n 108,158p Makefile` | skills, agents, commands, hook scripts, `session-init.sh`, templates; no `core/`, `rules/`, `output-styles/` |
| V-10 | Core project mirror precedent | `ls` | `.claude/WORKER-CONTRACT.md` absent; `.claude/REVIEW-SEVERITY.md` absent; `~/.claude/WORKER-CONTRACT.md` present |
| V-11 | Core installer | `sed` of `src/superclaude/cli/install_core.py` | `KNOWN_CORE_FILES` lists 12 names; `core_source.glob("*.md")`; existing destination skipped unless `force` |
| V-12 | Plugin build source | Grep and `sed` of `scripts/build_superclaude_plugin.py` | `PLUGIN_SRC = ROOT / "plugins" / "superclaude"` (line 16); copies `agents, commands, hooks, rules, scripts, skills` (line 76) |
| V-13 | Plugin skills | `ls plugins/superclaude/skills` | 4 skills (confidence-check, sc-implement-protocol, sc-recommend, sc-workflow-protocol) |
| V-14 | Mirror copies of P1 | `grep -rlF` over `.claude` and `plugins` | 6 under `.claude/`, 0 under `plugins/` |
| V-15 | Plugin twin parity | `cmp` | `spec-panel.md` differs at line 23; `document_review_loop_prompts.md` identical |
| V-16 | Sketch run | `uv run python blocker_truth_table_sketch.py` | `cases 4096 monotonicity violations 0`; `tri(S,0.2) U` |
| V-17 | Sketch UNSET probe | `uv run python` importing the sketch | 432 of 18,432 UNSET-to-answered moves lower the verdict (D 216, W 108, E 108); S = UNSET gives 108 FOLLOW_UP and 108 NOTE of 1,024; all-UNSET gives SHOW_USER; no UNDETERMINED in `ORDER` |
| V-18 | `wrong()` versus its description | Grep `jev-uses.md`; sketch probe | `jev-uses.md:138` "N only if both are N"; sketch `wrong(N, UNSET)` = N and `wrong(UNSET, N)` = N |
| V-19 | Confidence bound in the input | Grep `jev-uses.md` | line 194: "the min is an upper bound under any correlation" |
| V-20 | Transitive pin | Read `tests/audit/test_invariant_preservation_NFR_6_through_10.py:88-103` | imports `FAIL_BULLET`, `PASS_BULLET` from `test_nfr_conv_9_zero_trust` |
| V-21 | Source-path pin | Grep `tests/review/test_review_rules_text.py` | line 92 `assert "src/superclaude" not in TEXT` |
| V-22 | Consolidation merge rule | Grep `src/superclaude/skills/task/SKILL.md` | "highest severity" at line 252 |
| V-23 | Run-2 Gate 1 timing and outcome | `stat`; Read `gate1-cycle-control.md` | mtimes 11:58:47, 12:20:21, 12:48:30; header "12:23" at line 24; PASS at review 3 (line 38); Destination cell wrong (line 9) |
| V-24 | Run-2 marker volume | `grep -rhoF`, `-rhF`, `-rlF` | "minor under grading override": 838 occurrences, 825 lines, 64 files |
| V-25 | Installed-only primitives | `ls` | `finding-grader.md` and `sc-spec-panel-stoprule-protocol` only under `~/.claude/` |
| V-26 | `/sc:issue` flags | Grep `src/superclaude/commands/issue.md` | no `--repo`, `--dry-run` or `--preview` |
| V-27 | Worker contract | Grep `src/superclaude/core/WORKER-CONTRACT.md` | `/sc:issue` on never-as-worker list (line 23); 0 matches for `follow_up` |
| V-28 | Worker-contract reference count | `grep -rlF`, `grep -rhoF` | 58 files under `src/superclaude` (2 `.pyc`), 65 with `plugins/`, 110 occurrences; V1's 81 not reproduced |
| V-29 | Other cited anchors | Grep | `cli/review/__init__.py:14` click group `review`; `sc-bare-review/SKILL.md:3` "Delegate-only"; `card_convert.py:82` word set; `rf-qa.md:111` S5; tasklist phrase on 4 lines; reflect gate at 1540 |
| V-30 | Broadcast hook | Read `src/superclaude/hooks/scripts/pragmatic-subagent.js` | reads `~/.claude/output-styles/pragmatic.md` and injects it on SubagentStart; exits 1 if missing; registration not checked |
