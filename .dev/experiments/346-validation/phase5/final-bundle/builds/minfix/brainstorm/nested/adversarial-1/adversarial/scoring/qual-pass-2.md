# Qualitative scoring, pass 2 (reverse order: C, B, A)

Rubric: `sc-adversarial-protocol/refs/scoring-protocol.md` section A.2 (30 binary criteria, CEV protocol). MET needs a quoted citation `variant:line`; no evidence means NOT MET; no partial credit. Source requirements: `seed-brief.md`. Correctness checks used read-only ground truth: `src/superclaude/commands/spec-panel.md`, `tests/skills/`, `src/superclaude/cli/install_skills.py`, `phase4/AB-REPORT.md`, `phase4/ARMB-REPORT.md`.

Variant keys: C = `variant-3-haiku-backend.md`, B = `variant-2-sonnet-analyzer.md`, A = `variant-1-opus-architect.md`.

Ground-truth facts used in several verdicts:

- GT-1: `tests/skills/test_worker_contract.py:831-839` (`_check_no_unattended_sections`) globs `src/superclaude/commands/*.md` for a `## Unattended mode` heading and asserts the set equals `UNATTENDED_COMMANDS`. Current `src/superclaude/commands/spec-panel.md` (486 lines) has that heading at line 451. A copy that keeps it adds `spec-panel-minfix` to the set and fails that test unless the list is edited.
- GT-2: `src/superclaude/cli/install_skills.py:40-59` strips only the `sc-` prefix: `sc-<x>` is skipped when `commands/<x>.md` exists and does not activate it. `sc-fixcheck` and `sc-spec-panel-minfix-protocol` are installed; `sc-spec-panel-minfix` would be skipped.
- GT-3: `tests/skills/test_spec_panel_review_loop.py:20-21` pins only `src/` and `plugins/` `spec-panel.md`; the seven-bullet pin does not apply to a new variant file.
- GT-4: ARMB-REPORT results table: R3 proxy 8/4/6/5/6/1, R3 blocking (427 grading) Arm B 4 and 1, growth after cycle 2 +57.7/+69.3/+23.1/+36.3/+27.8/+32.1%, means 6.0/5.5/3.5 and 63.5/29.7/30.0%; it prints the bar as 44.5% (AB-REPORT prints 44.4%).

## Variant C (variant-3-haiku-backend.md)

| Dimension | # | Criterion | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|---|
| Completeness | 1 | Covers all explicit requirements | Met: additive variant, 427 bullets/cap kept, mechanical gate with residuals, logged override, escalate-not-expand, cap unchanged, S1 bars, attribution, falsification | C:5 "Keep PR 427's grading, changed-line review, seven bullets and three-review cap. Deliver only an additive `/sc:spec-panel-minfix` command"; C:98 "A finding needing more space gets `escalate`, never an invented larger fix"; C:126 "Only exit 0 plus matching current input hashes permits re-review" (zero over-budget reaches review); C:345 "**Falsification:**" | MET (1) |
| Completeness | 2 | Edge cases and failure scenarios | Met | C:275 "Test at least: identical-input idempotence; a zero-edit ledger with explicit escalations; a valid 60-word boundary and 61-word rejection; multibyte UTF-8 ..."; failure table C:329-343 | MET (1) |
| Completeness | 3 | Dependencies and prerequisites | Met | C:289 "Before a measured loop, show that a fresh worker loaded the new command and executed the installed checker on a tiny valid and invalid fixture ... If the helper is absent, halt" | MET (1) |
| Completeness | 4 | Success/completion criteria | Met | C:313 "R3 open critical+major proxy ... at most 3; each replicate below both controls"; C:319 "Keep all D10/D11 conditions: proxy mean at most 3 ..., growth at most 44.4%" | MET (1) |
| Completeness | 5 | Explicit out-of-scope | Met | C:158 "No CLI registration, package dependency, global rule, routing guide, `/sc:reflect`, rf-qa agent or `/sc:implement` change is part of this variant."; C:347 "Skip a package CLI, database, automatic patch engine ..." | MET (1) |
| Correctness | 1 | No factual errors | Met: every checked figure matches ground truth | C:12 "R3 proxy 6 and 1, mean 3.5; actual blocking 4 and 1; growth 27.8% and 32.1%" (= GT-4); C:319 "Do not round the published 44.4% bar upward because one report printed 44.5%" (= GT-4); C:160 source-path lookup in Tool Coordination (= spec-panel.md:220); C:317 "12,288 gross bytes ... approximately 21.3%" (12,288/57,763 = 21.27%) | MET (1) |
| Correctness | 2 | Feasible with stated constraints | Not met: (a) C:149 "Copy the current `spec-panel.md`" keeps `## Unattended mode`, which fails GT-1, while C:158 says existing tests "must remain green" and lists no edit for it; (b) the freeze/check steps are coordinator duties ("Use the helper's `freeze` operation ... **before dispatching the reviser**", C:47) yet briefs stay unchanged except the command name and the coordinator does not read the variant command (C:126 "not extra instructions pasted into briefs") | C:149; C:158; C:47; C:126; GT-1 | NOT MET (0) |
| Correctness | 3 | Terminology consistent | Not met: the gate folder is named two ways | C:47 "It creates `cycle-1/state.json` exclusively"; C:68 "`cycle-1/ledger.json`"; versus C:126 "`minfix-cycle-N/` (N is that report's review number) contains `state.json`, `freeze-receipt.json`, `ledger.json` and `check.json`" | NOT MET (0) |
| Correctness | 4 | No internal contradictions | Met: budget numbers agree across sections | C:58 "Blocking MAJOR ... 60 \| 512 \| 120 \| 0 \| 0 \| 2" equals C:245-246 `"limits": {"added_words": 60, "added_bytes": 512, "removed_words": 120, "new_headings": 0, "new_ids": 0, "normative_added": 2}`; C:18 "An escalation is a safe stopping outcome, **not** an experimental clean pass" consistent with C:321 | MET (1) |
| Correctness | 5 | Claims supported by evidence/rationale | Met | C:9-16 evidence table with "Consequence for this design" column, e.g. C:16 "A real checker answers the checkability objection" | MET (1) |
| Structure | 1 | Logical ordering | Met | C:20 "## 2. Mechanism (each loop step, in order)" with Step 1 (C:22) through Step 6 (C:124); sections 1 to 8 run problem, mechanism, causes, changes, install, measurement, risks, questions | MET (1) |
| Structure | 2 | Consistent hierarchy depth | Met: `##` sections, `###` subsections only under 2 and 4, no orphan | C:22 "### Step 1 ..."; C:143 "### Maintainer change set"; C:273 "### Required runtime tests" | MET (1) |
| Structure | 3 | Separation of concerns | Met | C:145 "Paths in this table are repository editing destinations, not runtime lookups."; C:130 "## 3. Causes removed and causes left" separate from mechanism | MET (1) |
| Structure | 4 | Navigation aids | Met (cross-references) | C:285 "New gate paths use the convention in section 2"; C:155 "including data-integrity and rejection cases below" | MET (1) |
| Structure | 5 | Artifact-type conventions | Met: the eight required brainstorm-variant sections | C:3 "## 1. Problem and evidence" ... C:349 "## 8. Open questions" | MET (1) |
| Clarity | 1 | Unambiguous language | Met: rules are definite; "should" appears only 4 times, mostly in open questions | C:62 "No budget banking between findings or cycles ... Deletions cannot purchase additions."; C:122 "More than one grant, an unused grant or a grant to a non-blocker fails closed." | MET (1) |
| Clarity | 2 | Concrete | Met | C:189-190 literal `freeze`/`check` invocations; C:209 "Use `re.findall(...)` as lossless tokens" | MET (1) |
| Clarity | 3 | Section purpose statements | Met | C:5 "**Decision:** treat a revision as a bounded transaction ..."; C:145 table purpose sentence | MET (1) |
| Clarity | 4 | Acronyms/terms defined on first use | Not met | C:12 "R3 proxy 6 and 1" ("proxy" undefined at first use); C:297 "Compare to D10 controls"; C:299 "Retain D5 metrics" (D10, D5 never defined) | NOT MET (0) |
| Clarity | 5 | Actionable next steps | Met | C:259-267 exit table column "Coordinator action"; C:358 "Implementation must follow a checked plan after this design is selected" | MET (1) |
| Risk Coverage | 1 | >=3 risks with probability and impact | Not met: the risk table gives consequence and containment, no probability for any risk | C:329 "Failure mode / Consequence and containment" header (no probability column or per-risk likelihood). No evidence found — searched sections 3, 6, 7, 8 | NOT MET (0) |
| Risk Coverage | 2 | Mitigation for each risk | Met | C:331-343 each row has containment, e.g. C:339 "One grant/cycle, hard maxima, no pooled budgets and digest binding restrict volume." | MET (1) |
| Risk Coverage | 3 | Failure modes and recovery | Met | C:262 "Valid inputs, policy/attribution failure / One cut-down attempt, then escalate"; C:341 "The last accepted copy remains recoverable" | MET (1) |
| Risk Coverage | 4 | External dependencies and their failure | Met | C:342 "Checker or installation is skipped ... Receipt absence invalidates the treatment"; C:289 "Run the helper through `uv run --no-project python`, so the old checkout's package/dependency graph cannot control its imports" | MET (1) |
| Risk Coverage | 5 | Monitoring/validation mechanism | Met | C:291 "Maintain an install watcher for all treatment files and the original command."; C:307 "Show the SHA-linked evidence chain for every accepted cycle" | MET (1) |
| Invariant & Edge | 1 | Collection boundaries (empty/single/max) | Met | C:216 "at most 2 MiB per specification/report/JSON input, 256 findings and 256 edits"; C:195 "It rejects empty files"; C:275 "a zero-edit ledger" | MET (1) |
| Invariant & Edge | 2 | State interactions across components | Met | C:126 "Re-run the checker and compare its inputs to the supplied report before reviewing, so an old PASS cannot admit a later candidate."; C:49 "both hashes are checked again after revision and before the next review" | MET (1) |
| Invariant & Edge | 3 | Guard-condition gaps | Met | C:195 "rejects duplicate JSON keys and unknown schema fields ... out-of-range or non-boundary byte offsets ... overlapping edits, no-op edits" | MET (1) |
| Invariant & Edge | 4 | Count divergence (off-by-one, inclusive/exclusive) | Met | C:90 "Offsets are zero-based half-open **baseline** byte ranges"; C:214 "Enforce limits at equality-inclusive boundaries"; C:275 "a valid 60-word boundary and 61-word rejection" | MET (1) |
| Invariant & Edge | 5 | Interaction effects | Met | C:62 "A shared edit has one owning finding id; optional `also_answers` links do not pool allowances."; C:335 "Coupled fixes ... Aggregated per-finding budgets may punish the correct fix." | MET (1) |

Subtotals C: Completeness 5/5; Correctness 3/5; Structure 5/5; Clarity 4/5; Risk Coverage 4/5; Invariant & Edge Case 5/5.

**Total C: 26/30; qual_score = 26/30 = 0.867.**

## Variant B (variant-2-sonnet-analyzer.md)

| Dimension | # | Criterion | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|---|
| Completeness | 1 | Covers all explicit requirements | Met: bullets 1-7 byte-identical (pins in GT-3 apply only to the original), logged reasoned override, escalate-not-expand, cap unchanged, attribution, invalid replicate when the checker is not honoured, falsification | B:254 "Bullet 6 (the Reviser contract) is kept byte for byte"; B:178 "Override (ledger `override: gap-fill \| multi-site \| contradiction: <reason of at least 10 words>`) ... Overrides are printed in the report and in the receipt"; B:132 "A finding that none of these can answer inside its budget is listed `escalated`, never expanded."; B:381 "V7 (mechanism honoured) ... `exit` = 0" | MET (1) |
| Completeness | 2 | Edge cases and failure scenarios | Met | B:327 tests 1-19 (e.g. "MAJOR fix of 81 added words: exit 2"); B:442-456 "Ways the mechanism can make the loop worse" table | MET (1) |
| Completeness | 3 | Dependencies and prerequisites | Met | B:106 "stops with `E-FIXCHECK-MISSING` at the start of every run if ... cannot run"; B:360 "Pre-flight before dispatch ... must print a 64-hex hash and exit 0" | MET (1) |
| Completeness | 4 | Success/completion criteria | Met | B:378 "Bar, fixed now and the same as D11: (a) review-3 critical+major proxy mean at most 3 ... (b) growth ... at most 44.4% ... (c) effect larger than the larger within-arm spread" | MET (1) |
| Completeness | 5 | Explicit out-of-scope | Met | B:247 "not changed \| `HOW-WE-WORK.md` (both copies), `pragmatic.md` S1-S5, `docs/guides/*`"; B:340 "### 4.6 Later adopters (not part of this change)" | MET (1) |
| Correctness | 1 | No factual errors | Met: checked figures and repo claims match ground truth | B:9 "control mean 6.0, arm A 5.5, Arm B 3.5 (r1 = 6, r2 = 1)" (= GT-4); B:87 transition ratios "0.72 ... 0.66" (recomputed from the ARMB proxy rows: 0.715 and 0.66); B:241 "486 lines in `src/` ... 'Native reasoning' at line 221 ... the `plugins/` copy still has the 472-line text" (= spec-panel.md:221, wc 486/472); B:242 served-by-command rule (= GT-2) | MET (1) |
| Correctness | 2 | Feasible with stated constraints | Not met: the repository variant keeps the current file's `## Unattended mode` section and test M2 locks that in, which fails GT-1; `test_worker_contract.py` is not in B's "may need a row" list | B:362 "the repository file is the same change applied to current `src/`"; B:331 "M2 faithful copy: after removing the frontmatter, the command-name substitution, bullet 8 and the `## Fix Budget` section, the file equals `src/superclaude/commands/spec-panel.md` line for line"; B:248 list omits `tests/skills/test_worker_contract.py`; GT-1 | NOT MET (0) |
| Correctness | 3 | Terminology consistent | Met: class names and numbers identical in every place | B:174-176 table "C ... 120 \| 80 \| 80 \| 6", "M ... 80 \| 50 \| 50 \| 4", "m ... 12 \| 0 \| 0 \| 1" = B:273-275 = B:296-298 `BUDGETS` | MET (1) |
| Correctness | 4 | No internal contradictions | Not met: the minor budget is 12 words in one place and 0 / "untouched" in others | B:133 "no edit beyond the minor budget (12 words, net 0, one entry). Their disposition row reads `deferred (minor, fixcheck budget 0)`"; B:226 "Text a minor finding names is left untouched, so it stays `origin=unchanged` ... \| minor budget 0" versus B:223 "Minor budget is 12 words and net 0, 36 per cycle" and B:233 F22 example editing a minor finding's text | NOT MET (0) |
| Correctness | 5 | Claims supported by evidence/rationale | Met | B:89-98 replay table "cap on words added per MAJOR blocking fix ... 80 (proposed) \| 11 \| 449"; B:42-50 chain table | MET (1) |
| Structure | 1 | Logical ordering | Met | B:100 "## 2. Mechanism (each loop step, in order)" with Step 0 (B:104) through Step 5 (B:213) | MET (1) |
| Structure | 2 | Consistent hierarchy depth | Met | B:7 "### 1.1"... B:89 "### 1.6"; B:237 "### 4.1" ... B:340 "### 4.6"; B:374 "### 6.1" | MET (1) |
| Structure | 3 | Separation of concerns | Met | B:216 "## 3. Causes removed and causes left" separate from B:235 "## 4. Exact changes"; B:458 "### 7.3 What is prose only, and the residual risk" | MET (1) |
| Structure | 4 | Navigation aids | Met (cross-references) | B:98 "which is why section 7 lists under-fixing first"; B:128 "(the reviewer's own recommendation exceeds the class gross cap ...)"; B:170 "derivation in section 1.6 and section 6" | MET (1) |
| Structure | 5 | Artifact-type conventions | Met | B:5 "## 1. Problem and evidence" ... B:469 "## 8. Open questions" | MET (1) |
| Clarity | 1 | Unambiguous language | Met: rules are definite; "should" appears 4 times, two in open-question headings | B:202-206 exit table; B:211 "Only `enforce --in-place` ever writes the spec" | MET (1) |
| Clarity | 2 | Concrete | Met | B:183-193 literal checker report; B:353-355 literal install commands | MET (1) |
| Clarity | 3 | Section purpose statements | Met | B:102 "Shape in one paragraph: ..."; B:218 "Target (constraint 1): reach a clean PASS, or a justified escalation" | MET (1) |
| Clarity | 4 | Acronyms/terms defined on first use | Not met | B:9 "427 (AB-REPORT, ARMB-REPORT, D10/D11/D12)" (D-ids undefined); B:378 "Validity V1-V6 as in D10/D11" (V1-V6 undefined) | NOT MET (0) |
| Clarity | 5 | Actionable next steps | Met | B:479 "**First implementation task: replay harness.** Run the finished script over the six recorded loops"; B:200 exit table column "reviser action" | MET (1) |
| Risk Coverage | 1 | >=3 risks with probability and impact | Not met: the risk table (B:444) has failure, why, detection, mitigation, residual; no probability per risk. Outcome probabilities at B:409 are for the bar, not for listed risks | B:444 header "# \| failure \| why it can happen (evidence) \| detection \| mitigation \| residual" — searched sections 6.3, 6.4, 7.1-7.3 | NOT MET (0) |
| Risk Coverage | 2 | Mitigation for each risk | Met | B:446-456 mitigation column filled in every row, e.g. B:446 "`large` and 2 overrides per cycle; one pre-registered retry at 100/60" | MET (1) |
| Risk Coverage | 3 | Failure modes and recovery | Met | B:204 "2 \| over budget ... \| cut the named entries down once, else `enforce`"; B:211 "`enforce` ... restores the baseline text for every hunk of every finding that fails" | MET (1) |
| Risk Coverage | 4 | External dependencies and their failure | Met | B:106 `E-FIXCHECK-MISSING`; B:451 "The reviser does not run the checker, or the task brief outranks the Reviser brief" | MET (1) |
| Risk Coverage | 5 | Monitoring/validation mechanism | Met | B:381 "V7 (mechanism honoured)"; B:358 "The existing install watcher ... gets two more sha256 lines" | MET (1) |
| Invariant & Edge | 1 | Collection boundaries (empty/single/max) | Met | B:203 "unreadable or empty file"; B:211 "It refuses to run without a ledger that has at least one entry (exit 1)"; B:327 test 11 "a fifth flag among four blocking ids is ignored" | MET (1) |
| Invariant & Edge | 2 | State interactions across components | Met | B:131 "refuses (exit 1, `STALE-BASE`) if its sha256 differs from `reviewed_sha256`"; B:318 `verify` "a silent re-run of check compared with the receipt totals, so a hand-written receipt is caught" | MET (1) |
| Invariant & Edge | 3 | Guard-condition gaps | Met | B:166 "The checker also derives the real `op` of the hunk ... and refuses a mislabelled entry"; B:453 "`snapshot` and `check` validate that every id of the block appears in the report body" | MET (1) |
| Invariant & Edge | 4 | Count divergence (off-by-one, inclusive/exclusive) | Met | B:327 "2. MAJOR fix of 81 added words: exit 2 ... 4. minor fix of 13 words, or of 12 words with net +1: exit 2"; B:450 "renumbering ... creates 'new ids' (AC-1.4 becomes AC-1.5)" | MET (1) |
| Invariant & Edge | 5 | Interaction effects | Met | B:48 "N3 ... cross-fix interaction; both followed their recommendations"; B:447 "the ctl-r1 residue findings are what propagation prevents, and the flg-r2 N3/N6 findings are what propagation causes" | MET (1) |

Subtotals B: Completeness 5/5; Correctness 3/5; Structure 5/5; Clarity 4/5; Risk Coverage 4/5; Invariant & Edge Case 5/5.

**Total B: 26/30; qual_score = 26/30 = 0.867.**

## Variant A (variant-1-opus-architect.md)

| Dimension | # | Criterion | CLAIM | EVIDENCE | VERDICT |
|---|---|---|---|---|---|
| Completeness | 1 | Covers all explicit requirements | Not met: seed success criterion "zero unapproved over-budget fixes reach a review" is not met by design; an over-budget fix reaches the review and is only not credited, and the validity checks do not catch a reviser who ran the checker and ignored exit 2 | A:365 "reviser runs the checker and obeys exit 2 \| prose, backstopped by the re-review's own run \| one review spent on an over-budget fix that is then not credited"; A:308 "V-M2: a ledger and a `fixcheck.json` exist for each cycle" (existence only) | NOT MET (0) |
| Completeness | 2 | Edge cases and failure scenarios | Met | A:231-244 test table (e.g. "edit with no ledger line \| exit 2, `unattributed`"); A:347-355 "Ways the mechanism could make the loop worse" | MET (1) |
| Completeness | 3 | Dependencies and prerequisites | Met | A:151 "A subcommand reaches a worker only after a package reinstall ... The skill-script pattern ... is established"; A:271 "test ! -e ~/.claude/commands/sc/spec-panel-minfix.md && test ! -e ~/.claude/skills/fix-budget" | MET (1) |
| Completeness | 4 | Success/completion criteria | Met | A:322 "Seed-brief criteria: R3 proxy mean 3 or fewer with every replicate better than every control ... and growth 44.4% or less"; A:324-330 failure criteria | MET (1) |
| Completeness | 5 | Explicit out-of-scope | Met | A:140 "`spec-panel.md`, its plugin copy, `HOW-WE-WORK.md`, `pragmatic.md` and the 427 pin tests are not touched"; A:256 "### 4.5 Later adopters (assessment, not part of this change)" | MET (1) |
| Correctness | 1 | No factual errors | Not met: arithmetic error in the calibration ceiling (2 + 11 + 1 = 14, not 13); the growth ceiling is labelled bytes but computed in words | A:82 "Expected cycle-1 ceiling at 13 blocking findings (2 `C`, 11 `B`, 1 `L`): 160 + 440 + 150 = 750"; A:314 "growth after two fix cycles (bytes) ... hard ceiling about 16% (... at most 870 added words in cycle 1 ... 390 in cycle 2 ..., against an 8,148-word draft)" | NOT MET (0) |
| Correctness | 2 | Feasible with stated constraints | Met: the plan avoids both repo traps that the other variants hit (GT-1, GT-2), and the coordinator gets no new duty so briefs change only by the command name | A:162 "The `## Unattended mode` section (master lines 451-461) is removed. Reason: `tests/skills/test_worker_contract.py:831-839` requires the set of commands with that heading to equal its list exactly" (= GT-1); A:151 "`sc-spec-panel-minfix` would be swept away at install" (= GT-2); A:37 "The coordinator gets no new duty" | MET (1) |
| Correctness | 3 | Terminology consistent | Met | A:80 definitions of **site**, **normative words**, **condition words**, **new id**, **new heading**, used the same way in A:73-78 and A:189-196 | MET (1) |
| Correctness | 4 | No internal contradictions | Met: script constants equal the budget table; exit-3 handling stated the same in both places | A:76-78 "`B` ... 40 \| 30 \| 2 \| 1 \| 1 \| 1 \| 0 \| 0", "`C` ... 80 \| 60 \| 3 \| 2 \| 2 \| 2 \| 0 \| 0", "`L` ... 150 \| 120 \| 4 \| 4 \| 3 \| 3 \| 1 \| 0" = A:189-191 `CLASSES`; A:109 "re-review records `fixcheck: input-error <message>` and continues without it" = A:174 "checker exit 1 or 3 is recorded and the re-review continues without it" | MET (1) |
| Correctness | 5 | Claims supported by evidence/rationale | Met | A:13-20 measured table; A:29 "N5 quotes \"(F22)\", `spec-panel-round2.md:120`"; A:82 "Calibration: 62-79% of 427-arm per-finding additions already fit 40 words" | MET (1) |
| Structure | 1 | Logical ordering | Met | A:35 "## 2. Mechanism (each loop step, in order)": A:39 "2.1 Review N", A:52 "2.2 Fix cycle", A:64 "2.3 Review N+1" | MET (1) |
| Structure | 2 | Consistent hierarchy depth | Met | A:39 "### 2.1" ... A:112 "### 2.6"; A:155 "### 4.1" ... A:256 "### 4.5"; A:334 "### 7.1" ... A:357 "### 7.3" | MET (1) |
| Structure | 3 | Separation of concerns | Met | A:357 "### 7.3 What is prose and what is mechanical" table separate from risks; A:112 "### 2.6 What changes against 427's Reviser contract" | MET (1) |
| Structure | 4 | Navigation aids | Met (cross-references) | A:144 "Derived copy of `spec-panel.md` (section 4.1)"; A:370 "Falsification criteria are fixed in section 6" | MET (1) |
| Structure | 5 | Artifact-type conventions | Met | A:5 "## 1. Problem and evidence" ... A:372 "## 8. Open questions" | MET (1) |
| Clarity | 1 | Unambiguous language | Met: rules are definite; "should" appears 4 times, three in open-question headings | A:61 "An escalated finding gets no edit and stays open. Escalate, never expand."; A:116 "the checker breaches any site attributed to an unlisted id or to no id" | MET (1) |
| Clarity | 2 | Concrete | Met | A:44-49 literal Reviser-brief machine lines; A:283 literal `sed -E` substitution | MET (1) |
| Clarity | 3 | Section purpose statements | Met | A:7 "**Problem in one sentence.**"; A:37 "Three parts, nothing else: a **budget class** ..., a **ledger** ..., and one **stdlib checker**" | MET (1) |
| Clarity | 4 | Acronyms/terms defined on first use | Not met | A:151 "(D9; `~/.local/bin/superclaude` is 5.0.0)" (D9 not defined at first use); A:308 "**Validity (in addition to D10 V1-V6).**" (D10, V1-V6 undefined); A:298 "D5 M1-M5" | NOT MET (0) |
| Clarity | 5 | Actionable next steps | Met | A:325 "drop minfix as a standalone fix and test it only in combination with a verdict-side change"; A:262 "Promotion of minfix itself = fold bullets 2, 5 and 6 into `spec-panel.md` (both copies) ..., then delete the variant" | MET (1) |
| Risk Coverage | 1 | >=3 risks with probability and impact | Not met: one risk carries a likelihood word ("likeliest", A:350); the other six give no probability | A:349-355 risks 1-7. No evidence of probability for at least 3 risks — searched sections 6, 7.1-7.3 | NOT MET (0) |
| Risk Coverage | 2 | Mitigation for each risk | Met | A:349 "Mitigations: class `C` (3 sites), the rename rule, one `L` per report"; A:350 "Mitigation: narrow the rule instead of rewriting dependents"; A:353 "a dry run of the checker on one real cycle"; A:352 "Escalation needs a reason naming the smallest fix found"; A:361-368 residual table | MET (1) |
| Risk Coverage | 3 | Failure modes and recovery | Met | A:105-110 exit table with "who acts" (e.g. "2 \| breach ... \| reviser cuts down or reverts (step 7)"); A:62 "restore each breaching finding's sites to `revert_to`" | MET (1) |
| Risk Coverage | 4 | External dependencies and their failure | Met | A:180 "(if that script is absent, use the project `.claude/skills/fix-budget/scripts/fixcheck.py`)"; A:276 "a change mid-arm voids it (V6 as in D10)"; A:110 "1 \| the checker crashed (Python traceback) \| treated as exit 3" | MET (1) |
| Risk Coverage | 5 | Monitoring/validation mechanism | Met | A:302-306 metrics M6-M10; A:308 "V-M1 ... V-M2 ... V-M3 ... A replicate that fails one is 'variant not honoured'" | MET (1) |
| Invariant & Edge | 1 | Collection boundaries (empty/single/max) | Met | A:233 "no edits, valid report \| exit 0"; A:243 "whitespace-only change \| exit 0, zero sites"; A:244 "S1-sized input (generated 1,500 units) \| finishes under 5 s"; A:193 "MAX_L = 1" | MET (1) |
| Invariant & Edge | 2 | State interactions across components | Met | A:42 "427's coordinator copy for `--baseline` stays as it is; the two should be equal"; A:66 "This run is authoritative: it does not matter whether the reviser ran the checker" | MET (1) |
| Invariant & Edge | 3 | Guard-condition gaps | Met | A:50 "The checker rejects (exit 3) an override line whose id is not `L`, an `L` without an override line, and a second `L`"; A:99 `ledger_errors` codes "old-not-in-baseline\|new-not-in-revised\|bad-json\|unknown-id\|add-without-reason" | MET (1) |
| Invariant & Edge | 4 | Count divergence (off-by-one, inclusive/exclusive) | Met | A:237 "`B` fix with 3 sites; same fix as a 3-site rename \| exit 2 / exit 0" (limit 2); A:209-210 "a site matched by k ids splits its words evenly"; A:80 rename "counts as one site" | MET (1) |
| Invariant & Edge | 5 | Interaction effects | Met | A:350 "**Cross-site inconsistency.** ... If a third place ... still states the old behaviour, review 2 flags it"; A:31 "New condition clauses are new guards, and FR-8 makes their GAP rows MAJOR"; A:379 "Composition with the other themes" | MET (1) |

Subtotals A: Completeness 4/5; Correctness 4/5; Structure 5/5; Clarity 4/5; Risk Coverage 4/5; Invariant & Edge Case 5/5.

**Total A: 26/30; qual_score = 26/30 = 0.867.**

## Summary

| Variant | Completeness | Correctness | Structure | Clarity | Risk Coverage | Invariant & Edge | Total | qual_score | Edge floor (>=1/5) |
|---|---|---|---|---|---|---|---|---|---|
| C (variant-3-haiku-backend) | 5 | 3 | 5 | 4 | 4 | 5 | 26/30 | 0.867 | 5/5, eligible |
| B (variant-2-sonnet-analyzer) | 5 | 3 | 5 | 4 | 4 | 5 | 26/30 | 0.867 | 5/5, eligible |
| A (variant-1-opus-architect) | 4 | 4 | 5 | 4 | 4 | 5 | 26/30 | 0.867 | 5/5, eligible |

Notes for the merge:

- All three tie at 26/30 and lose a point on the same two criteria (Clarity 4: experiment ids D5/D9/D10/V1-V6 undefined; Risk 1: no per-risk probability).
- What tells them apart is in Correctness and Completeness. B and C copy the current `spec-panel.md` with its `## Unattended mode` section, which breaks `test_worker_contract.py:831-839` (GT-1); A removes that section and gives the reason. C also has two names for the gate folder, and B states the minor budget as both 12 and 0. A lets an over-budget fix reach a review (it is only not credited), which misses the seed's "zero unapproved over-budget fixes reach a review"; C blocks review on any nonzero checker result, and B invalidates the replicate.
- A pass-1 evaluator scoring in forward order may disagree at these boundaries. Recheck these verdicts first: C/B Correctness 2 (GT-1) and A Completeness 1.
