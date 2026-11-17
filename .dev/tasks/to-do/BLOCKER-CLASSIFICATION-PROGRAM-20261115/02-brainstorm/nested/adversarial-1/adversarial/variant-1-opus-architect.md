# Variant 1 (architect): blocker classification, record and offer, one source of truth

Status: Complete (requirements and design options; no code; nothing edited outside this file)
Date: 2026-11-15

## 0. How to read this variant

- Persona: architect. Lens: maintainability and extension scaffolding. The sections on the shared rule package (7), extension points (8), the file list (9) and the staged rollout (11) carry the weight; every other section is complete enough for this variant to stand alone.
- Kind of document: requirements and design options only. No code. The truth-table logic is referenced by path (`.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/blocker_truth_table_sketch.py`), not copied.
- Sources (all under the program folder unless a full path is given): `02-brainstorm/seed-brief.md`, `02-brainstorm-context-preamble.md`, `00-issue-description.md`, `02-brainstorm/jev-uses.md`, the three files in `02-brainstorm/enrichment/`, and `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/grading-override.md`. Facts taken from those files are cited to them; facts I re-checked live are marked "(checked)" and listed in section 15.
- Words used in this document:
  - "Gate": any review step that can stop a run (a QA phase gate, a spec review loop, a tasklist validation pass, a reflect promotion gate).
  - "Primitive": a command, skill, agent, template, rule prompt or output style that `superclaude install` copies into `~/.claude/`.
  - "Digest block": a short, fenced copy of the rule inside a primitive, checked by a test against the one source text.
  - "Shared rule package": the one place the full rule lives (proposed below as a delegate-only skill, a skill with no slash command of its own).
  - "Follow-up": a finding that is real but changes no decision; it is recorded and offered, never fixed inside the gate.
  - "Judge": whatever answers the classifier's yes/no questions (Jev, another model, the reviewer's own label, or a fixed test file).

## 1. Problem statement

Review gates call too many findings "blocking". A blocking finding stops the run, forces a fix cycle and a re-review even when the finding changes no decision. In research run 2 a wrong docstring label, a miscounted "four versus six meanings", and two one-character table-pipe defects each failed a gate; Gate 1 needed a third review and a second fix cycle (about 25 minutes) for the two table defects alone (`00-issue-description.md`; `enrichment/severity-models-and-loops.md` section 7).

The cause is in the rule text. The shared definition says "Blocking is a real defect: wrong behaviour, a false claim, a missing required deliverable, or a security or data-loss risk" (checked: `src/superclaude/output-styles/pragmatic.md:225`). "A false claim" has no consequence filter, so any false sentence blocks.

The rule is a maintenance problem as much as a wording problem:

1. The same sentence is copied verbatim into 11 files under `src/superclaude/` (checked, section 9), and a test forces the copies to match the output style word for word (checked: `tests/skills/test_review_severity_rule.py:181-203`). Changing the rule means a coordinated edit across 11 files plus their tests.
2. About 10 other severity families exist with their own words (`enrichment/severity-models-and-loops.md` section 5). Some map onto the shared rule, some must not. There is no written map, so the same word means different things: `important` and `medium` are non-blocking in `card_convert.py` (checked: line 82) while `IMPORTANT` is blocking in rf-qa (checked: `src/superclaude/agents/rf-qa.md:111`); Medium is blocking in the tasklist loop (checked: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1614`) and a warning in the output style (checked: `pragmatic.md:230`).
3. A partial fix already exists (the Medium class and `follow-up candidates`, `pragmatic.md:230`), but no code performs the "ask once per loop" step, no file format exists for the list, and the rf-qa family, `/task`, tech-research, reflect, pr-submit and `/sc:implement` do not carry it (`enrichment/follow-up-and-issue-mechanisms.md` section 1).
4. The issue text's "21 files and 109 occurrences" does not reproduce; the code says 11 files for the definition sentence (section 9 reconciles this).

## 2. Goals and non-goals

### Goals

| # | Goal | How we know it is met |
|---|---|---|
| G1 | Real blockers are still found and still stop the gate. | No drop in confirmed blocking findings in the sampled audit (section 12); security, data-loss and safety findings never downgraded. |
| G2 | Findings that change no decision are recorded, never fixed inside the gate, and offered to the user once per run. | Every gate in scope writes a follow-up ledger; the offer appears once per top-level run. |
| G3 | One source of truth for the rule, with a test that fails on any drift. | Changing the rule is one edit to the shared text plus a mechanical re-paste of digest blocks that the drift test checks. |
| G4 | Every other severity scale has a written mapping onto the shared outcomes (BLOCKING, FOLLOW_UP, NOTE) or a written reason to stay separate. | The scale-mapping table in the shared package has a row per family; a test checks each row names an existing file. |
| G5 | A blocker classifier with a confidence score exists, runs in shadow mode first, and never needs an API key to be useful. | The classifier runs with the fallback judge; its verdict is recorded beside the reviewer's label. |
| G6 | New gates, new judges and new severity scales can be added without editing the rule text or the classifier's decision table. | Section 8 extension contracts; each is one registry row plus tests. |

### Non-goals

- No code, no edits under `src/`, `tests/`, `.claude/` or `~/.claude/` in this step. A `/sc:workflow` plan comes first because more than five source files change (`02-brainstorm-context-preamble.md` item 8).
- Not meeting the 35 percent score target strictly; the owner said it "doesn't need to be strictly met" (`02-brainstorm-context-preamble.md` item 8).
- Not changing the loop caps (2 fix cycles, 3 reviews), the regression halt or the monotonicity halt. They keep counting blocking findings only; they shrink because "blocking" shrinks.
- Not rewriting code-assigned scales (roadmap structural checkers, audit wiring gate, pipeline detectors, PR severity router); they stay (`enrichment/severity-models-and-loops.md` table 5).
- Not changing `/sc:implement`'s own model in v1 (it already derives severity from four yes/no answers, `jev-uses.md` section 1).
- No automatic issue creation; no Jev API call, no account, no key request.

## 3. The proposed rule in plain words

A finding is **blocking** only when at least one of these three conditions holds:

1. **A decision rests on it.** A design choice, recommendation, destination, outcome, or a number or fact the deliverable's recommendation depends on would be wrong or unsupported if the text stays as it is. A false statement that feeds such a decision is blocking; a false statement that feeds nothing is not.
2. **A required deliverable or required section is missing**, or a required step was not done. Presence is checked by code first (does the section exist); the judgment is only whether what exists does the job.
3. **Security, data-loss or safety-boundary risk.** Following the text, or running the code it quotes, would delete, overwrite or expose data or a secret, or act outside the declared scope. This class is never downgraded, whatever the label, the classifier or the judge says.

Everything else is **not blocking** and falls into one of two recorded classes:

| Class | Meaning | Examples (from `grading-override.md` and run 2) | What happens |
|---|---|---|---|
| FOLLOW_UP (today's "Medium") | a real weakness, but no decision rests on it | a miscount whose conclusion is unaffected; a stale figure when a sibling file carries the discoverable correction; two research files disagreeing on a figure no recommendation uses (P3-002) | written to the follow-up ledger with evidence and a one-line "why not blocking"; offered to the user once |
| NOTE (today's "minor") | cosmetic: wording, formatting, style, a wrong tag or line number on a true claim | wrong label on a true docstring claim (P3-001); a table-pipe defect that changes no cell a later phase reads (NEW-1, NEW-2) | one ledger line; never offered on its own; never rechecked |

Rules that travel with the definition:

- **Grade by consequence, not by label.** A reviewer's CRITICAL, IMPORTANT, MAJOR or High is information, not the verdict (same stance as `pragmatic.md:229` and `spec-panel.md:259`, checked).
- **Do not downgrade to avoid work.** If you cannot tell whether a decision rests on the text, name the downstream use and grade by it; if you still cannot tell, the finding is shown to the user (the classifier's SHOW_USER outcome), not filed silently.
- **Never pass open blocking findings.** Loop caps, regression and monotonicity halts are unchanged and count blocking findings only.
- **A protocol with its own severity model keeps it** (today's S4 bullet, `pragmatic.md:228`), but must publish its mapping onto the three outcomes in the shared package (section 7.5).
- **Table-shape defects:** a formatting defect is a NOTE only when it does not change the meaning of a cell that a later phase or a script reads. A pipe that splits a column a parser reads is condition 1 (a destination becomes wrong). Run 2's reviewer and the override disagreed on exactly this row (`enrichment/severity-models-and-loops.md` section 7, NEW-1 and NEW-2); the rule must name the reader of the cell, so this disagreement becomes checkable.

## 4. Record-and-offer behaviour

### 4.1 Flow

1. A reviewer grades each finding under section 3 and writes it into its own report as today, with one new field per non-blocking finding: `why not blocking` (one line naming which of the three conditions fails).
2. The gate's consolidation step (the step that already merges lens reports, for example `/task` step 6, `enrichment/severity-models-and-loops.md` section 6) appends every FOLLOW_UP and NOTE row to the run's follow-up ledger. Only blocking findings go to the fix agent and count toward the loop controls.
3. In shadow mode (stage 1, section 11) the classifier verdict and its confidence are written into the same ledger row beside the reviewer's label; nothing else changes.
4. At the end of the top-level run (not per gate, not per loop), the top-level session reads the ledger and makes one offer. Rows marked SHOW_USER are the exception: in an attended run, from stage 2 on, they are asked at the gate where they arise, because they might be blocking.
5. The user's answer is written back into each row's `status` column, so a re-run never offers or files a row twice.

Why once per run and not once per loop: `pragmatic.md:230` says "once per loop"; a run with five gates would then ask five times. One question at the end is the smaller interruption and matches the run-2 override ("the follow-up list is reported to the owner at the end (one question ...)", `grading-override.md` line 25). This is a deliberate change of wording and is listed as owner decision D4.

### 4.2 Follow-up ledger format

One file per run, `follow-ups.md`, placed next to the gate's existing outputs (from `enrichment/follow-up-and-issue-mechanisms.md` section 2):

| Gate family | Ledger path |
|---|---|
| `/task`, tech-research, task-builder (all have a `qa/` folder) | `<task folder>/qa/follow-ups.md` |
| spec-panel, reflect (attended or unattended) | `<report-dir>/follow-ups.md` |
| `/sc:implement` | `<run artifacts>/follow-ups.md`, built from the existing per-task `notes.md` files (the notes files stay; the ledger is an index over them) |
| pr-submit | `.dev/pr-monitor/pr-<N>-<timestamp>/follow-ups.md` (Low and Nit rows only; its own router decides, section 7.5) |
| tasklist validation | the bundle's report folder, beside `ValidationReport.md` |

Fixed shape (one header block plus one table; the column set is defined once in the shared package and the drift test checks the header line):

- Header lines: `ledger_schema: 1`, `run: <run id or task folder>`, `rule_version: <digest version>`, `judge_chain: <for example llm:<model> > reviewer>`.
- Columns, in order:

| Column | Content |
|---|---|
| `id` | `FU-<gate>-<n>`, stable within the run |
| `gate` | gate name, for example `phase-3-qa` |
| `class` | FOLLOW_UP, NOTE or SHOW_USER |
| `native_label` | the reviewer's own word (IMPORTANT, MAJOR, Medium, Low, drift) kept as information |
| `location` | `path:line` or section |
| `finding` | one sentence |
| `evidence` | excerpt or pointer, marked verified or unverified |
| `why_not_blocking` | which condition fails, for example "no recommendation uses this figure" |
| `proposed_fix` | one line |
| `suggested_type` | bug, docs, refactor, test, observability (reuses the troubleshoot report's types, `enrichment/follow-up-and-issue-mechanisms.md` section 2) |
| `classifier` | verdict, confidence, judge id, or `unavailable` (empty before stage 1) |
| `status` | open, resolved, filed #N, ignored |

The shape borrows from three existing records rather than inventing a fourth: the rf-qa issues table, `/sc:implement`'s `notes.md` line, and troubleshoot's `## Follow-up tasks` (same source).

### 4.3 Offer wording

Attended run, once at the end:

> N follow-ups were recorded in `<ledger path>` (F real weaknesses, M notes). None of them blocked a gate. What should happen to them?
> 1. Resolve the F weaknesses now (one fix pass, no re-review unless a fix touches a blocking finding).
> 2. File them as one issue (a checklist of F items; notes are attached as a collapsed list).
> 3. File each weakness as its own issue.
> 4. Keep them in the ledger only.

Rules: no issue is created without the user's answer (unchanged from `pragmatic.md:230`); NOTE rows are never offered one by one; when F is 0 and M is under a threshold (owner decision D5, recommended 10) the offer is one line ("M notes recorded in `<path>`; nothing to decide") and asks nothing.

### 4.4 Unattended runs

- A worker never asks and never files (WORKER-CONTRACT WC-2; `/sc:issue` is on the never-as-worker list, checked: `src/superclaude/core/WORKER-CONTRACT.md:23`). It writes the ledger, lists it in the contract's `artifacts`, and keeps `worker_status: succeeded` because follow-ups never fail a gate.
- New optional contract keys (proposal; no such field exists today, checked: 0 matches for `follow_up` in `WORKER-CONTRACT.md`): `follow_up_ledger: <path>`, `follow_up_counts: {follow_up: F, note: M, show_user: S}`. Consumers already must tolerate unknown keys (`enrichment/follow-up-and-issue-mechanisms.md` section 4).
- SHOW_USER rows in an unattended run: the reviewer's own label stands (no regression from today), and the row is flagged `unsettled`. If the reviewer label was blocking, the gate behaves as today.
- A coordinator reading results must open the ledger when `follow_up_counts.follow_up` or `show_user` is above 0; this is a one-line addition to the coordinator reading rule.

### 4.5 Batching into one issue

Today `/sc:issue --create` takes one description and files one issue; it has no ledger input, no batch mode and no unattended path (`enrichment/follow-up-and-issue-mechanisms.md` section 3).

| Option | What it takes | Trade-off |
|---|---|---|
| B1 (recommended for v1) | The top-level session renders the chosen ledger rows into one description file (a checklist, one line per row with location and evidence) and runs `/sc:issue --create @<that file> --mode feature --type <area> --depth quick`; it then writes `filed #N` back into each row. | No change to `/sc:issue`; one Complexity and one type for the batch; uses the existing person-facing path. |
| B2 | Add a `--from-ledger <path>` input to `/sc:issue --create` that reads rows, groups them, and writes issue numbers back itself. | Cleaner and testable, but a new feature in a command that has its own tests and worker tiers; do it only if B1 is used often. |
| B3 | Rule 10 by hand (copy `~/.claude/ISSUE-BACKLOG.md`, fill, `gh issue create --repo IronbellyOrg/IronClaude ...`). | Works without `/sc:issue`, but sets no type, Complexity or label; the rule-10 example omits `--repo` (same source), so the batch renderer must add it. |

Option 3 of the offer ("each as its own issue") is B1 run once per row; above a small count (recommended 5) the session should suggest option 2 instead.

## 5. The blocker classifier and its Jev use

This section adopts the design in `jev-uses.md` and adds only the architecture: where each part lives, and which parts are data rather than code so they can change without a code review of the decision logic.

### 5.1 The four layers

| Layer | What it holds | Where it lives (proposal) | Changes how |
|---|---|---|---|
| L1 Questions | the 10 atomic yes/no questions W, D, E, M, S, C, T, F, I, G with their `criteria.true` and `criteria.false` text (`jev-uses.md` section 3) | a text file in the shared rule package (`refs/classifier-questions.md`), versioned | a wording edit bumps the question-module version; every result records it |
| L2 State builder | code that fills the state fields (`finding.quote`, `finding.span`, `finding.stated_outcome`, `finding.evidence`, `deliverable.kind`, `decision_basis`, `required_items`, `constraints`) and reads anchors back before any judge sees them | package code under `src/superclaude/cli/review/` (the `review` command group already exists, checked: `cli/review/__init__.py:14`) | Python change with unit tests |
| L3 Judges | the `Judge` interface with `JevJudge`, `LlmJudge`, `ReviewerJudge`, `FixtureJudge` (`jev-uses.md` section 6) | package code beside L2 | a new judge is a new class plus a registry row (section 8.2) |
| L4 Decision | the truth table: bands, precedence, the W-by-D grid, the S lift; plus verdict confidence and routing thresholds | package code; thresholds in one small config file next to it | the table has property tests (every combination has one outcome; monotone in every input); thresholds change only from the calibration report |

The one command exposed to primitives is a package CLI (proposal: `superclaude review classify --ledger <path>`), because installed primitives must reach package behaviour through the `superclaude` CLI, never by a `src/superclaude/` path (repo CLAUDE.md rule).

### 5.2 Questions, truth table and confidence (summary of `jev-uses.md`)

- Never one question "is this a blocker?" (Jev is literal and the house meaning of "blocking" differs from the everyday one). Six questions feed the blocking side (W wrong outcome, D a decision depends, E evidence shows a false statement, M required item missing, S safety or data risk, C quoted constraint broken); four feed the explanation side (T pointer drift on a true claim, F cosmetic only, I intent inferable, G suggestion not defect).
- Each probability becomes Y, N, U (unsettled) or UNSET (skipped or failed; a failed call is never N). Bands start at 0.30 and 0.70; S uses 0.10 and 0.30 so safety flags early.
- Precedence: S = Y is BLOCKING; else M = Y or C = Y is BLOCKING; else look up (wrong = W or E, D) in a 4-by-4 grid; an unsettled S lifts any lower verdict to SHOW_USER.
- Outcomes: BLOCKING, FOLLOW_UP, NOTE, SHOW_USER (a person decides), UNDETERMINED (go to the next judge).
- The design sketch is at `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/blocker_truth_table_sketch.py`. I ran it in this session with `uv run python`: it printed `cases 4096 monotonicity violations 0` (checked).
- Verdict confidence is computed by code by the weakest link: for BLOCKING by W and D it is min(pW, pD); for FOLLOW_UP and NOTE it is 1 minus the union-bound chance that a blocking path completes. Jev's own `confidence` field is never the gate.
- Routing: auto-downgrade needs confidence at least 0.85; auto-confirm blocking needs 0.70; otherwise SHOW_USER. The classifier never silently upgrades a non-blocking label to blocking.
- Stability: pin `jev-1.14.0`, send each bundle 3 times, take the median, treat a spread above 0.20 as U.

One input disagreement, where the code wins: `jev-uses.md` section 4 step 3 says "wrong" is "N only if both are N". The sketch's `wrong()` (checked: lines 17-25) returns N when one of W and E is N and the other is UNSET. The sketch is the more useful behaviour (a skipped E question should not force U when W is a clear no), but the spec text must say what the code does: "N when at least one is N and neither is Y or U".

### 5.3 Where `decision_basis` comes from (the D question's input)

D cannot be answered without a list of what the deliverable rests on, and no review output carries that list today (`jev-uses.md` risk 3). The state builder fills it per deliverable kind; when it cannot, D is UNSET and wrong-outcome findings fall to SHOW_USER, never to FOLLOW_UP.

| Deliverable kind | Source of `decision_basis` | Source of `required_items` |
|---|---|---|
| research report | the Recommendation section, any destination or value-inventory table, quoted numbers in those sections | the template's required section list |
| spec, PRD, TDD | requirements table, acceptance criteria, non-goals | template section list |
| tasklist or plan | acceptance criteria per task, the dependency table | the plan template's required fields |
| code | the task's acceptance criteria, the plan's Constraints and Non-goals (same anchors qa.md uses) | the task's declared outputs |
| other | empty (D is UNSET) | empty |

Extension point: a new deliverable kind is one row here plus one extractor in the state builder (section 8.4).

### 5.4 The key dependency and the fallback chain

- Every Jev call needs a key sent as a Bearer token; none exists in this environment, and none was requested (`jev-uses.md` section 6). The key is a dependency of `JevJudge` only.
- Judge chain at run time: `JevJudge`, then `LlmJudge` (a different model class from the reviewer that wrote the finding), then `ReviewerJudge` (today's behaviour). Every ledger row records which judge produced the verdict, because results from different judges are not comparable.
- Everything except `JevJudge` works without a key: the question module, the table and its property tests, the four judge classes, pre-written request payloads, and the five validation runs with `LlmJudge`.
- Privacy: finding text from a private fork would leave the machine. TypeSafe states zero data retention only "for enterprise customers" (`jev-uses.md` section 6). This is owner decision D1.

### 5.5 Shadow mode, then advisory, then gating

- Shadow (stage 1): the classifier runs after the reviewer, writes its verdict and confidence into the ledger, and changes nothing.
- Advisory (stage 2): the verdict is shown beside the reviewer label in the consolidated findings and the offer; still the reviewer's grade under the new rule decides.
- Gating (stage 4, optional): only the downgrade path, and only above tau_down, may move a reviewer's blocking label to FOLLOW_UP; S never moves; SHOW_USER asks. Whether to ever enter this stage is owner decision D6.
- The classifier does not fill `/sc:implement` qa.md's four checklist answers in v1 (`jev-uses.md` decision J3).

## 6. Guardrails against hiding real defects

| # | Guardrail | Mechanism | Where it is enforced |
|---|---|---|---|
| R1 | Safety, data-loss and safety-boundary findings are never downgraded | condition 3 of the rule; S = Y is BLOCKING first in the table; S uses a lower band; S = U lifts to SHOW_USER | rule text (pinned by test) and the table's property test |
| R2 | Required-deliverable test | presence checked by code before any judgment; M = Y is BLOCKING | state builder plus table |
| R3 | Decision-basis test | the reviewer must name the downstream use when it says "no decision rests on it" (`why_not_blocking` column cannot be empty for FOLLOW_UP) | ledger schema check |
| R4 | Unknown is not minor | if the reviewer or the classifier cannot tell, the outcome is SHOW_USER, never FOLLOW_UP | rule text and table (D = UNSET never gives FOLLOW_UP for a wrong-outcome finding) |
| R5 | No downgrade to avoid work | sentence in the rule text, copied from `grading-override.md` line 23 | digest block |
| R6 | Sampled audit of non-blocking rows | each run, a fresh reviewer (not the one that graded) re-grades a random sample of FOLLOW_UP and NOTE rows (recommended: 10 percent, at least 3 rows) under the same rule; any upgrade to blocking is counted as an escaped defect | stage 2 onward; metric M3 |
| R7 | Escalation with a stated consequence | a reviewer who believes a non-blocking-looking finding must block writes the concrete wrong outcome and who produces it; that sentence makes it blocking under condition 1 | rule text |
| R8 | Anchor read-back | the quote must be byte-present and the evidence excerpt read before any judge sees the finding (qa.md precedent); unverified evidence cannot support an auto-downgrade | state builder |
| R9 | Re-review only when a blocking finding is fixed | resolving follow-ups (offer option 1) triggers no re-review unless the fix edits a span cited by an open or fixed blocking finding | rule text for the top-level session |
| R10 | The classifier never upgrades silently and never gates before shadow evidence | routing rule; stage gate in section 11 | classifier code and the rollout checklist |

## 7. One source of truth: shared rule package, digest blocks and drift tests

### 7.1 What exists today (the baseline to improve, not to throw away)

The repo already has a single source of truth and a drift test; it is just in the wrong place and too rigid:

- Source: `pragmatic.md` lines 225-229 are S1 to S5 (checked). The test reads them by position: `canonical_rule_bullets()` finds the binary-verdict bullet and takes exactly the next five lines, asserting each opening phrase (checked: `tests/skills/test_review_severity_rule.py:78-96`).
- Copies: a hard-coded tuple of 10 files (`S1_S3_FILES`, checked: lines 181-192) must contain S1-S3 verbatim after whitespace flattening; the first 6 must also contain S5 (line 193).
- Broadcast: `pragmatic.md` reaches every subagent, because the hook `src/superclaude/hooks/scripts/pragmatic-subagent.js` reads `~/.claude/output-styles/pragmatic.md` and injects it as `additionalContext` on `SubagentStart` (checked: lines 7-15). I saw that injection at the start of this very session.

Weaknesses for maintenance:

| Weakness | Consequence |
|---|---|
| The source is a position inside an output style | any bullet added above S1 or between S1 and S5 breaks every importer of `canonical_rule_bullets()`; the Medium bullet had to be placed directly after S5 for the same reason (`test_review_severity_mapping.py` pins "the line right after S5") |
| The copy list is a Python tuple | a new copy is invisible to the test until someone edits the tuple; a stray copy elsewhere is never flagged |
| Copies carry the whole rule | a rule change is an 11-file edit; the full rule (examples, scale map, ledger format) cannot grow without growing 11 files and every subagent's context |
| No scale map | ten families interpret "blocking" independently |
| No home for the ledger format, offer wording or classifier questions | they would become a twelfth, thirteenth and fourteenth copied text |

### 7.2 Options for the shape of the single source

| Option | How primitives get the rule | Strength | Weakness |
|---|---|---|---|
| A. Status quo, copy and pin | full verbatim copies, test against `pragmatic.md` | no runtime read; proven | all weaknesses above |
| B. Pure pointer | each primitive says "read the rule at `<path>` first" | one text; tiny primitives | every reviewer pays a Read and a failure mode at run time; a reviewer that skips the Read grades by memory; precedent shows it needs a fail-closed sentence (`spec-panel.md:268`: "if it cannot be read, return `incomplete` and review nothing", checked) |
| C. Digest plus pointer (recommended) | a short, fenced digest block copied verbatim into each primitive, checked against one source; one pointer line to the full rule for detail | grading works with no Read; the full rule can grow freely; drift is mechanical to detect; adding a copy is a registry row | two artifacts to keep in step (the digest section and the full rule), solved by putting both in one file |

Recommendation: C. The digest is what a reviewer needs to grade (about six bullets); the full rule is what a consolidator, a coordinator or an unsure reviewer needs (examples, the scale map, the ledger format, the offer).

### 7.3 Where the shared rule package lives

The location decides whether the repo's dual-surface rule can be met at all (an installed primitive names the installed copy first and the project `.claude/` copy second, per the repo CLAUDE.md).

| Location | Installed without code change | Project `.claude/` copy (second surface) | Checked by `make verify-sync` | In the plugin build | Precedent |
|---|---|---|---|---|---|
| `src/superclaude/core/REVIEW-SEVERITY.md` | yes (checked: `install_core.py:58` globs `core/*.md`) | no (sync-dev has no `core/` step, checked: `Makefile` has no `core/` reference) | no | no (`enrichment/rule-copies-and-tests.md` 4.2) | `~/.claude/WORKER-CONTRACT.md`, read by path from 81 source files (checked count), single surface |
| `src/superclaude/rules/prompts/review_severity.md` | yes (rule group `prompts`, checked: `install_user_setup.py:34`) | no | no | yes | `spec-panel.md:268` reads `~/.claude/rules/prompts/document_review_loop_prompts.md`, single surface (checked) |
| `src/superclaude/templates/...` | yes (enrichment 4.3) | yes (enrichment 4.1) | yes | no | MDTM templates |
| `src/superclaude/skills/sc-review-severity/` (delegate-only skill) | yes (`install_all_skills`) | yes (checked: `Makefile:112-125` copies every skill folder with a `SKILL.md`) | yes (enrichment 4.1) | yes, folder is in the build list (enrichment 4.2), but the plugin's `skills/` is hand-kept and holds only 4 skills today (checked) | `sc-bare-review` is a delegate-only skill in `src/` (its description ends "Delegate-only", then "no slash command", checked: its `SKILL.md:3`) |

Recommendation: a delegate-only skill, `src/superclaude/skills/sc-review-severity/`. It is the only location that satisfies both surfaces and gets `make verify-sync` drift checking for free, and a skill folder can also hold the question module and, later, small scripts. The cost is one more line in the skill listing; its description says "Delegate-only, no slash command" like `sc-bare-review`.

Proposed contents (file names are proposals):

| File | Holds | Read by |
|---|---|---|
| `SKILL.md` | purpose, who reads which ref, the rule version, "Delegate-only, no slash command" | humans and the skill loader |
| `refs/rule.md` | the full rule: the three conditions, the two recorded classes, examples from run 2, the table-shape rule, "do not downgrade to avoid work", R1-R10, and the **digest section** between markers | unsure reviewers, consolidators; the drift test |
| `refs/scale-map.md` | one row per severity family (7.5) | consolidators that receive another scale; the scale-map test |
| `refs/follow-up-ledger.md` | ledger schema 1, gate-family paths, the offer wording, unattended behaviour, batching option B1 | consolidation steps, the top-level session, coordinators |
| `refs/classifier-questions.md` | the question module text, versioned (stage 1 onward) | the package classifier (copied into the package at build time or read from the installed path; decided in the plan) |
| `refs/registry.yaml` | every carrier of the digest: path, carrier kind (output style, agent, template, rule prompt, skill, command), stage, digest version, own-scale flag | the drift tests; humans planning a change |

### 7.4 Digest block and pointer line

- The digest is about six bullets: (1) the three blocking conditions; (2) FOLLOW_UP and NOTE are recorded, never fail a review, never trigger a fix pass, are never rechecked; (3) the loop cap sentence, unchanged word for word (`at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`, which `CANONICAL_CAP_TEXT` pins); (4) a protocol with its own severity model keeps it and publishes its mapping; (5) grade by consequence, not by label, on any scale; (6) never downgrade security, data-loss or safety-boundary findings, and do not downgrade to avoid work.
- Fence: an opening and closing HTML comment carrying the digest version (for example `review-severity:digest v2 begin` and `... end`). Comments are cheap, visible to the model, and grep-able.
- Pointer line, directly after the fence, naming both surfaces in the order the repo CLAUDE.md sets for skills (installed first): "Full rule, scale map and follow-up ledger format: `~/.claude/skills/sc-review-severity/refs/rule.md` (in a dev checkout without an install: `.claude/skills/sc-review-severity/refs/rule.md`)." Never a `src/superclaude/` path.
- Reading the pointer is not required to grade. It is required for the steps that write the ledger or make the offer; if neither surface can be read there, the step writes non-blocking findings into its own report as today and records `ledger: unavailable`. It never blocks a gate for that reason.
- `pragmatic.md` keeps a digest too (it is the broadcast carrier, 7.1). Because every subagent receives the whole output style, its digest must stay short; the Medium and spec-panel bullets at lines 230-231 move into the full rule and the scale map.

### 7.5 Which primitives keep their own scale, and how each maps

"Keeps" means the primitive's own words and logic stay; the row in `refs/scale-map.md` records how its labels land on BLOCKING, FOLLOW_UP and NOTE so the ledger and the metrics speak one language.

| Family (where) | Keeps own scale? | Native label to shared outcome | Change needed to align with the rule |
|---|---|---|---|
| CRITICAL / IMPORTANT / MINOR lens scale (rf-qa, rf-qa-qualitative, task, task-builder, tech-research, templates) | no, it is the shared rule's home | label is information; outcome by the three conditions | S5 wording: "CRITICAL and IMPORTANT findings are blocking" (7 files, checked) becomes "grade by the conditions; the label is information" |
| `/sc:spec-panel` CRITICAL / MAJOR / MINOR (`spec-panel.md:259`, checked) | yes | CRITICAL: BLOCKING; MAJOR: BLOCKING if it names a concrete wrong outcome, else FOLLOW_UP; MINOR: NOTE | small: limit CRITICAL to conditions 1-3 (stoprule already limits it, `rubric.md:10` per enrichment); its `follow-up candidates` list becomes the ledger |
| stoprule rubric v1, finding-grader, diffgate and ledger variants (installed only, no `src/` copy per enrichment section 0) | yes, frozen | B1+B2+B3: BLOCKING; else NOTE or FOLLOW_UP | none in this branch; record the mapping; a rubric change "is a new version" (enrichment) |
| `/sc:implement` qa.md (four checklist answers) | yes (`pragmatic.md:228`, checked) | B1 ac-outcome-missing: condition 2; B3 harmful-effect: condition 3; B4 constraint breach: BLOCKING (own); B2 false-claim: BLOCKING (broader than the rule); minor and note: NOTE | none in v1; option for later: a "rests on" qualifier on B2 (owner decision D8) |
| reflect deviation taxonomy (promotion gate, `sc-reflect-protocol/SKILL.md:1540`, checked) | yes | Regression: BLOCKING; Drift: BLOCKING today; Necessary, Authorized: NOTE | proposal: Drift is BLOCKING only when a condition holds; otherwise FOLLOW_UP with "authorize or revert" in the offer (owner decision D7) |
| tasklist High / Medium / Low (`sc-tasklist-protocol/SKILL.md:1614`, checked) | yes | High: BLOCKING; Medium: BLOCKING today; Low: NOTE | Medium becomes FOLLOW_UP unless a condition holds; synthetic DNSP HIGH stays blocking |
| roadmap validate BLOCKING / WARNING / INFO (prompt in `cli/roadmap/validate_prompts.py` per enrichment) | yes | BLOCKING: BLOCKING; WARNING: FOLLOW_UP; INFO: NOTE | put the three conditions into the validator prompt (a Python string change, stage 3) |
| `card_convert.py` word translator (checked: line 82) | yes, it is a translator, not a rule | `blocking, blocker, major, high, must-fix, p1, critical, p0`: blocking; `minor, medium, low, should-fix, important, nit, info, p2, p3`: not blocking | none; document that `important` maps to not blocking here, unlike rf-qa |
| findings-v1/v2 boolean `blocking` | yes | the boolean is the outcome | later: the classifier may write the boolean (stage 4 only) |
| PR router Critical..Nit, Auggie rubric | yes, code-assigned | Low and Nit: NOTE rows in the ledger | none; "Medium routes to `--fix`" is a separate decision |
| roadmap structural, audit wiring, pipeline detectors, adversarial invariant probe, cli-portify | yes, code-assigned or not a review loop | not mapped | none; listed in the scale map as "out of scope" so nobody re-asks |

## 8. Extension points: new gates, new judges, new severity scales

Every extension is "add a row, satisfy a contract, the existing tests pick it up". No extension edits the rule text or the truth table.

### 8.1 Adding a new gate

Contract (what a new review gate must do):

1. Paste the digest block and pointer line; add a row to `refs/registry.yaml` with its carrier kind and stage. The drift tests are parametrized over the registry, so the new file is checked with no test edit.
2. Write `follow-ups.md` in schema 1 at the gate family's path (or add a path row to `refs/follow-up-ledger.md` for a new family).
3. Send only BLOCKING findings to the fix step and count only those in the loop controls.
4. Under `--unattended`, list the ledger in the contract's `artifacts` and set `follow_up_counts`.
5. If it has its own scale, add a scale-map row (8.3).

### 8.2 Adding a new judge

Contract: a judge answers one question about one finding state and returns a probability in 0 to 1, or a failure (never "no" on failure); it reports a stable judge id and version (for example `llm:<model>@<date>`). Steps: implement the interface, add the judge id to the chain config, run the five calibration runs against the scored table with the same question-module version, and publish the reliability table. A judge may be placed ahead of `LlmJudge` only if it matches or beats it on agreement and flip rate (`jev-uses.md` recommendation 2). `FixtureJudge` exists so the table and the routing can be tested without any model.

### 8.3 Adding a new severity scale

Contract: one row in `refs/scale-map.md` with the family name, the file that defines it, each native label, the shared outcome per label, and either "graded by the conditions" or "keeps own model because <reason>". A scale-map test checks that each row's file exists and each native label appears in it. The ledger always keeps `native_label`, so metrics can compare scales.

### 8.4 Adding a new deliverable kind

Contract: one row in the `decision_basis` table (5.3) and one extractor in the state builder. Without it, D is UNSET and wrong-outcome findings go to SHOW_USER (the safe default), so an unsupported kind degrades to "ask", not to "hide".

### 8.5 Changing questions, thresholds or the rule

| Change | Required with it |
|---|---|
| question wording | bump the question-module version; re-run the five runs; every result records the version |
| a new question | bump the version; the table's exhaustiveness and monotonicity property tests must still pass (the sketch shows why: its first draft had 511 monotonicity violations, `jev-uses.md` section 4) |
| thresholds | change only from a calibration report on a training half, checked on a held-out half |
| rule text | bump the digest version; migrate registry rows by stage; the drift test allows mixed versions only as the registry declares |
| the later 5-level severity Score | one Score question whose level sentences are the same sentences as the human 1-to-5 scoring rubric (`jev-uses.md` section 3), stored once in the question module |

## 9. Files and primitives that would change (from Grep)

### 9.1 Patterns and counts (run live in this session on `src/superclaude/`, case-sensitive)

| Id | Pattern | Files | Occurrences | Meaning |
|---|---|---|---|---|
| P1 | `Grade every review finding as blocking or minor` | 11 | 11 | the definition sentence (S1) |
| P2 | `Minor findings never fail a review` | 11 | 11 | S2, same 11 files |
| P3 | `at most 2 fix cycles \(3 reviews\)` | 12 | 12 | the cap (S3): the 11 plus `commands/spec-panel.md` |
| P4 | `CRITICAL and IMPORTANT findings are blocking` | 7 | 7 | S5 label map |
| P5 | `follow-up candidates` | 3 | 7 | the Medium mechanism (`pragmatic.md` 1, `spec-panel.md` 3, `document_review_loop_prompts.md` 3) |
| P6 | `2 fix cycles` | 22 | 120 lines | the cap family, wider than the rule |
| P7 | `High or Medium \(blocking\)` | 1 | 4 | tasklist protocol, Medium blocks |
| P8 | `drift == 0` | 1 | 1 | reflect promotion gate |

Reconciling the issue's "21 files, 109 occurrences": no pattern reproduces it (enrichment found none either; P6 is the nearest by files). The 21 is a count of listed paths, not of copies: the issue draft's notes say 19 shared-rule paths plus `spec-panel.md` and `card_convert.py` (`enrichment/rule-copies-and-tests.md` 1.1; `draft-notes.md:15` in the issue draft folder records the 11 and marks 109 unverified, checked). Of those 19 paths, 8 do not carry the definition at all (rf-task-builder and 7 skill entry points; they carry the cap). The spec uses P1 = 11 files.

Mirrors (checked with `grep -rlF` because the Grep tool skips gitignored folders and returned 0 for `.claude/`): the project `.claude/` holds 6 copies of P1 (rf-qa, rf-qa-qualitative, 2 document templates, 2 MDTM templates), and `.claude/agents/rf-qa.md` is byte-identical to `src` (`cmp`). The plugin tree holds none of the 11 (checked: no `rf-qa*.md`, no `output-styles/`, no MDTM templates under `plugins/superclaude/`).

### 9.2 Change list by group and stage

Group A: the 11 P1 carriers. Each replaces S1, S2 and S5 (where present) with the digest block and pointer line; S3 text stays word for word. Stage in brackets (section 11).

| File (under `src/superclaude/`) | P1 line (checked) | Carrier kind | Stage |
|---|---|---|---|
| `output-styles/pragmatic.md` | 225 (S1-S5 at 225-229; Medium and spec-panel bullets 230-231 move to the full rule) | output style, broadcast to every subagent | 2 |
| `agents/rf-qa.md` | 108 | agent | 2 |
| `agents/rf-qa-qualitative.md` | 108 | agent | 2 |
| `templates/documents/agent_template_qa.md` | 161 | template | 3 |
| `templates/documents/skill_template.md` | 828 | template | 3 |
| `templates/workflow/01_mdtm_template_generic_task.md` | 644 | template | 3 |
| `templates/workflow/02_mdtm_template_complex_task.md` | 655 | template | 3 |
| `rules/prompts/automated_qa_workflow_qa_prompt.md` | 11 | rule prompt | 3 |
| `rules/prompts/doc_code_analyst_qa_prompt.md` | 27 | rule prompt | 3 |
| `rules/prompts/documentation_expert_qa_prompt.md` | 28 | rule prompt | 3 |
| `rules/prompts/recruiting_expert_qa_prompt.md` | 27 | rule prompt | 3 |

Group B: variants with their own wording or loop logic (aligned, not replaced).

| File | What changes | Stage |
|---|---|---|
| `commands/spec-panel.md` (259-261, checked) | CRITICAL limited to the three conditions; `follow-up candidates` list written as the ledger; pointer line | 3 |
| `rules/prompts/document_review_loop_prompts.md` (P5: 3 hits) | briefs say "write FOLLOW_UP and NOTE rows to the ledger"; structure pins kept | 3 |
| `skills/task/SKILL.md` (P6: 7 lines; Follow-Up Items at 361, checked) | consolidation writes the ledger; fix agent gets BLOCKING only (already says "minors-only spawns no fix agent", enrichment) | 2 |
| `skills/tech-research/SKILL.md` (P6: 17) and `skills/task-builder/SKILL.md` (P6: 3), `agents/rf-task-builder.md` | ledger path under `qa/`; gate tables say "follow-ups recorded" | 2 |
| `skills/sc-tasklist-protocol/SKILL.md` (P7: 4) | Medium becomes FOLLOW_UP unless a condition holds | 3 |
| `skills/sc-reflect-protocol/SKILL.md` (P8 at 1540) | only if owner decision D7 is yes: Drift without a condition becomes FOLLOW_UP | 3 |
| `core/WORKER-CONTRACT.md` | optional contract keys `follow_up_ledger`, `follow_up_counts`; coordinator reading rule | 2 |
| `cli/roadmap/validate_prompts.py` (enrichment, line 130 not checked) | the three conditions in the validator prompt | 3 |

Group C: new files. `skills/sc-review-severity/` (`SKILL.md` plus the five refs in 7.3); package code for the classifier under `cli/review/` (stage 1); new test modules (section 10); optionally a plugin mirror of the skill with a parity test (stage 3, owner decision D9).

Group D: no change. The P6 cap family outside groups A and B (roadmap, readme, tech-reference, operational-guide skills, the two build-request templates, `core/HOW-WE-WORK.md`): the cap counts blocking findings, so a narrower "blocking" needs no edit there. `cli/review/card_convert.py`, `findings_v2.py`, the PR router, `/sc:implement` qa.md: unchanged in v1. Installed-only files (stoprule skill, finding-grader, spec-panel variants) have no `src/` copy on this branch (enrichment section 0) and are out of scope here.

Totals: 11 group A files, about 9 group B files, 1 new skill folder of 6 files, 1 to 2 new package modules, 2 new test modules plus edits to the existing ones in section 10. Well over five files, so a `/sc:workflow` plan is required before any edit.

## 10. Tests that pin the rule text and what changes

### 10.1 Existing pins (from `enrichment/rule-copies-and-tests.md` section 3; file presence checked by Glob)

| Test module | What it pins | What breaks | Change in the plan |
|---|---|---|---|
| `tests/skills/test_review_severity_rule.py` | S1-S5 by position after the binary-verdict bullet (`canonical_rule_bullets()`, lines 78-96, checked); S1-S3 verbatim in 10 files (`S1_S3_FILES`, 181-192, checked); S5 in 6; `CANONICAL_CAP_TEXT`; banned phrases; 161 + 139 edit-table rows | any rewording or move of S1-S5 | `canonical_rule_bullets()` reads the digest from `refs/rule.md` instead of positions in `pragmatic.md`; `S1_S3_FILES` becomes "rows of `registry.yaml`"; cap and banned-phrase tests unchanged; edit-table rows whose `new` text is S1/S2 are re-pinned |
| `tests/skills/test_review_severity_mapping.py` | Medium and spec-panel bullets must sit directly after S5 in `pragmatic.md`, and spec-panel literals in `src` and `plugins` | moving bullets 230-231 | literals move to assertions on `refs/rule.md` and `refs/scale-map.md`; spec-panel literals updated with its own edit |
| `tests/skills/test_implement_severity_static.py` (P1 pin, lines 485-498 per enrichment) | exact S2 and S4 strings | rewording S2 or S4 | S4 kept word for word; S2 assertion moves to the digest |
| `tests/skills/test_review_loop_extension.py` | cap bullet in spec-panel | cap rewording | none (cap unchanged) |
| `tests/skills/test_review_prompt_overrides.py` | zero-finding and "no minimum count" sentences | removing those sentences | none; they are not part of the digest and stay |
| `tests/audit/test_nfr_conv_9_zero_trust.py` | rf-qa PASS and FAIL bullets in `src` and `.claude/` | rewording "Any CRITICAL or IMPORTANT gap" | reword the FAIL bullet to "any blocking gap" and re-pin both surfaces |
| `tests/audit/test_severity_floor_unweakened.py` | SHA-256 of rf-qa-qualitative's Critical Rules block | any edit in that block | re-pin the hash with a reviewed note; Rule 6 stays verbatim |
| `tests/audit/test_dnsp_all_agents_fail_bypass.py` | rf-team-lead fix-cycle rule hash | only if that line changes | none expected |
| `tests/review/test_review_rules_text.py` | structure of the review-loop prompts file and `"src/superclaude" not in TEXT` (checked: line 92) | structural moves | keep; the ledger sentence goes inside an existing section |

`canonical_rule_bullets` is imported or called in 3 test modules (checked: 9 occurrences across `test_review_severity_rule.py`, `test_implement_severity_static.py`, `test_review_severity_mapping.py`), so changing its source is one function edit with three callers, not a rewrite.

### 10.2 New tests (proposal)

| Id | Test | Fails when |
|---|---|---|
| T1 digest equality | every registry row's file has exactly one digest block whose flattened body equals the digest section of `refs/rule.md` for that row's version | a copy drifts, is duplicated or is missing |
| T2 reverse scan | any tracked file under `src/` or `plugins/` that contains a digest fence or the legacy P1 sentence must be a registry row | an unregistered copy appears; after stage 3, any legacy P1 sentence remains |
| T3 pointer line | each carrier's pointer names `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, and the carrier contains no `src/superclaude` | dual-surface order breaks or a source path leaks |
| T4 scale map | each scale-map row names an existing file and each native label appears in it | a family is renamed or removed without the map |
| T5 ledger schema | the column header in `refs/follow-up-ledger.md` equals the schema constant used by the classifier code | the format drifts between doc and code |
| T6 truth table | every input combination yields exactly one outcome; monotone in every input; S = Y is always BLOCKING | the decision logic regresses |
| T7 plugin parity (if D9 is yes) | plugin copy of the skill is byte-equal to `src` | the hand-kept plugin tree drifts |
| T8 install | after `superclaude install` into a temp home, `~/.claude/skills/sc-review-severity/refs/rule.md` exists | packaging misses the skill |

`make verify-sync` already diffs `src/superclaude/skills/` against `.claude/skills/` (enrichment 4.1), so the second surface is checked without a new test.

## 11. Rollout stages

Design principle: every stage is additive or switches a small, named set of carriers, and the registry's per-row `stage` and `digest version` make each switch (and each revert) a mechanical edit the drift tests check.

| Stage | What changes | Files touched | Behaviour change | Entry criteria | Exit criteria |
|---|---|---|---|---|---|
| 0 Measure | nothing in `src/`; the program scores 30+ historical blocking findings blind (three agents, 1 to 5), derives blocker characteristics, runs the classifier 5 times with `LlmJudge` | program folder only | none | this spec reviewed | reliability table, agreement and flip rate reported; question set confirmed or revised |
| 1 Scaffold and shadow | add the `sc-review-severity` skill (rule, digest v2, scale map, ledger format, registry with all 11 carriers at `stage: legacy, digest v1`); add the classifier package code and CLI; add T1-T6 and T8 (T1 accepts v1 for legacy rows; T2 accepts the legacy P1 sentence only in registered rows) | new skill folder, new package module, new tests; no existing carrier edited | none at any gate; `superclaude review classify` can be run on any finished run's findings and writes verdicts beside reviewer labels | stage 0 report | classifier run in shadow on at least 3 real runs; ledger format exercised by hand on them |
| 2 Broadcast and QA family | switch `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md` to digest v2; `/task`, tech-research, task-builder, rf-task-builder write `qa/follow-ups.md` and the top-level session makes the end-of-run offer; WORKER-CONTRACT keys; classifier advisory in the offer; sampled audit R6 starts | 3 carriers plus 4 loop files plus `WORKER-CONTRACT.md`; existing pins re-pointed (10.1) | the run-2 kind of findings stop failing gates in the rf-qa family | stage 1 exit; owner approves D3, D4 | 5 attended runs with metrics M1-M6 inside the revert thresholds |
| 3 Remaining copies and own-scale alignments | 4 templates, 4 rule prompts to digest v2; spec-panel and review-loop prompts aligned; tasklist Medium; roadmap validate prompt; reflect Drift only if D7; plugin mirror if D9; T2 becomes strict (no legacy P1 sentence anywhere in `src/` or `plugins/`) | about 12 files | every gate in scope uses one meaning of blocking | stage 2 exit | T2 strict passes; no metric trigger fired for 2 weeks of use |
| 4 Optional gating | the classifier may auto-downgrade a reviewer's blocking label to FOLLOW_UP above tau_down; `JevJudge` first only if D1 and D2 are yes and it beat `LlmJudge` in calibration | classifier config only | fewer SHOW_USER prompts | owner decision D6 | ongoing metrics |

Templates note: task files already generated from the old MDTM templates keep the old text. T2 scans `src/` and `plugins/` only; old task folders under `.dev/tasks/` are not migrated.

Revert per stage: stage 1 is deletion of new files only. Stage 2 and 3 are "set the affected registry rows back to v1 and restore their v1 digest text" (the v1 text stays in `refs/rule.md` as a historical section until stage 3 has been stable for one release), plus switching the ledger offer off in the loop files.

## 12. Metrics and revert triggers

| Id | Metric | Source | Target direction |
|---|---|---|---|
| M1 | blocking findings per gate (median, per gate family) | consolidated findings | down; run 2 suggests about 45 percent on research gates (one sample) |
| M2 | fix cycles per gate and gate wall time | cycle-control files | down |
| M3 | escaped-defect rate: share of sampled FOLLOW_UP and NOTE rows that a fresh reviewer upgrades to blocking | sampled audit R6 | at or below 5 percent |
| M4 | classifier agreement with the validated labels, per-finding flip rate across 5 runs, reliability by confidence bin | stage 0 and shadow runs | report, no target before calibration |
| M5 | SHOW_USER share | ledger | below 20 percent once calibrated (a higher share means the classifier is not deciding) |
| M6 | offer outcomes: resolved, filed, kept, ignored; issues filed from the ledger later closed as real defects | ledger `status` column, issue tracker | report |
| M7 | drift test failures on master | CI | 0 |

Revert triggers (any one):

1. Any security, data-loss or safety-boundary finding found in a FOLLOW_UP or NOTE row (single event; R1 failed).
2. M3 above 10 percent in two consecutive measured runs of the same gate family.
3. A blocking defect reaches a later gate or a merged change and is traced to a downgraded finding.
4. M1 and M2 do not fall after 5 runs of a gate family (the change costs attention and saves nothing).
5. The owner judges the end-of-run offer to be noise (for example, it is answered "keep in ledger only" in most runs while M3 shows real defects in the rows).

## 13. Risks

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| K1 | Real defects hidden in the ledger | medium | high | R1-R10; sampled audit; revert trigger 1 and 2 |
| K2 | `decision_basis` missing for many deliverables, so D is UNSET and most findings go to SHOW_USER | high at first | medium (more questions, no hidden defects) | 5.3 extractors per kind; SHOW_USER is safe by design; metric M5 |
| K3 | Reviewers keep grading by memory of the old rule | medium | medium | digest in every carrier; T1 and T2; the broadcast output style carries it to every subagent |
| K4 | Pragmatic output style grows and every subagent pays for it | medium | low | digest is shorter than today's S1-S5 plus lines 230-231; detail moves to the skill refs |
| K5 | The pointer surface cannot be read in some environment (plugin-only install, no dev mirror) | medium for plugin users | low | grading never needs the pointer; ledger steps fail open (`ledger: unavailable`); plugin mirror per D9 |
| K6 | Registry becomes a second thing to forget | low | medium | T2 reverse scan finds unregistered copies; adding a gate without a row fails CI |
| K7 | Classifier overfits 30 to 40 rows | medium | medium | held-out half; wording written once from characteristics; no per-case clauses (`jev-uses.md` risk 4) |
| K8 | Privacy of finding text sent to TypeSafe | n/a until D1 | high | no call before D1; excerpts only; secret redaction; fallback judges work without it |
| K9 | Mixed meanings during rollout (stage 2 carriers on v2, templates on v1) | certain for a while | low to medium | registry records the version per carrier; the ledger header records `rule_version`; stage 3 closes the gap |
| K10 | Changing reflect's Drift gate changes a promotion outcome users rely on | medium | medium | owner decision D7; off by default |
| K11 | The input counts this spec rests on drift again | medium | low | every count in section 9 has its pattern; the plan re-runs them before editing |

## 14. Owner decisions, each with a recommendation

| # | Decision | Recommendation |
|---|---|---|
| D1 | May finding text (excerpts from the private fork) be sent to TypeSafe's API? | Only if the account has zero data retention or the processing contract is accepted; otherwise run with `LlmJudge` only (`jev-uses.md` J1). |
| D2 | Request a TypeSafe key and a small budget? | Only after D1 is yes; the five runs cost about $0.08 at the listed price, unverified (`jev-uses.md` J2). |
| D3 | Adopt the three-condition rule as the framework default (stage 2)? | Yes, after the stage 1 shadow evidence. |
| D4 | One offer per top-level run instead of "once per loop"? | Yes; SHOW_USER items are still asked at their gate in attended runs. |
| D5 | Threshold below which notes-only results are reported without a question | 10 notes. |
| D6 | May the classifier ever gate (auto-downgrade)? | Not before stage 3 is stable and calibration shows agreement and flip rate at least as good as the reviewer baseline; never for S. |
| D7 | Change reflect's promotion gate so Drift without a condition is a follow-up? | Not in v1; record the mapping and measure how many Drift rows would flip first. |
| D8 | Add a "rests on" qualifier to `/sc:implement`'s B2 false-claim answer, or let the classifier fill qa.md's four answers? | No in v1 (`jev-uses.md` J3); qa.md already derives severity mechanically. |
| D9 | Mirror the shared skill into `plugins/superclaude/` with a parity test? | Yes at stage 3, when the plugin's `spec-panel.md` points at it; until then plugin users keep today's text. |
| D10 | Location of the shared rule: delegate-only skill (recommended), `core/`, or `rules/prompts/`? | Delegate-only skill `sc-review-severity`: the only option with both surfaces and free `make verify-sync` checking (7.3). |
| D11 | Is the last-resort fallback "the reviewer's label stands"? | Yes, no regression from today (`jev-uses.md` J4). |

## 15. What was verified and what was not

### 15.1 Load-bearing claims I checked live in this session (17)

| # | Claim (source that made it) | How checked | Result |
|---|---|---|---|
| 1 | The definition sentence is in 11 files (seed brief, enrichment) | Grep P1 on `src/superclaude` | true: 11 files, 11 lines, line numbers in 9.2 |
| 2 | `follow-up candidates` is in 3 files, 7 times (enrichment) | Grep count | true |
| 3 | `2 fix cycles` matches 22 files (enrichment) | Grep count | true: 22 files, 120 matching lines |
| 4 | `pragmatic.md` 225-231 hold S1-S5, the Medium bullet and the spec-panel bullet (preamble, enrichment) | Read lines 222-232 | true |
| 5 | `install_core.py` globs `core/*.md` at line 58 (seed brief, enrichment) | Read lines 10-79 | true; existing destination files are skipped without force (line 70) |
| 6 | `canonical_rule_bullets()` takes the five lines after the binary-verdict bullet; `S1_S3_FILES` lists 10 files (enrichment) | Read test lines 60-99 and 178-209 | true |
| 7 | Medium is blocking in the tasklist loop at `SKILL.md:1614` (seed brief) | Grep | true; the phrase appears 4 times in that file |
| 8 | Reflect's Drift blocks promotion at `SKILL.md:1540` (seed brief) | Grep `drift == 0` and `Drift and Regression block` | true, line 1540 |
| 9 | `card_convert.py` maps `important` and `medium` to non-blocking (enrichment) | Grep | true, line 82 (and docstring line 37) |
| 10 | `/sc:issue` is on the never-as-worker list (enrichment) | Grep `WORKER-CONTRACT.md` | true, line 23 |
| 11 | `make sync-dev` does not copy `core/`, `rules/` or `output-styles/` (enrichment) | Grep and Read `Makefile` | true: no such references; skills copied at 112-125 |
| 12 | The plugin tree holds none of the 11 carriers (enrichment) | Glob and Grep on `plugins/superclaude/` | true: no rf-qa agents, no output styles, no MDTM templates |
| 13 | S5 is in 7 files (enrichment) | Grep count | true |
| 14 | Rule groups are `core`, `contextual`, `prompts` and are excluded from auto-load (enrichment) | Grep `install_user_setup.py` | true: line 34, `claudeMdExcludes` at 167-176 |
| 15 | The output style reaches every subagent (enrichment 0) | Read `hooks/scripts/pragmatic-subagent.js` | true: `SubagentStart` hook injects `~/.claude/output-styles/pragmatic.md` |
| 16 | The truth-table sketch covers 4096 cases with 0 monotonicity violations (`jev-uses.md`) | `uv run python` on the sketch | true: printed `cases 4096 monotonicity violations 0` |
| 17 | The project `.claude/` mirror carries the rule and matches `src` (enrichment 1.3) | `grep -rlF` and `cmp` | true: 6 files; `rf-qa.md` identical |

Also checked for this design: `spec-panel.md:259` grading bullet and `:268` single-surface read of the review-loop prompts; the `review` click group at `cli/review/__init__.py:14`; `sc-bare-review` is a delegate-only skill in `src/`; `canonical_rule_bullets` appears in 3 test modules; 0 matches for `follow_up` in `WORKER-CONTRACT.md`; the 10 named test modules exist (Glob).

### 15.2 Claims in the inputs found false or imprecise

1. "21 source files, 109 occurrences" (preamble item 1, issue text): false as a count of copies. The definition is in 11 files; 21 is a count of listed paths; no pattern gives 109.
2. The preamble lists 19 paths as carrying the definition; 8 of them (rf-task-builder and 7 skill entry points) carry the cap wording, not the definition (enrichment 1.1, consistent with my P1 Grep).
3. `jev-uses.md` section 4 step 3 says "wrong" is "N only if both are N"; the sketch's code (lines 17-25) returns N when one is N and the other is UNSET. The code wins; the spec text must match it.
4. Method caveat, not an input error: the Grep tool skips gitignored folders, so it reports 0 copies in the project `.claude/`; a plain `grep` finds 6. Any plan step that counts mirror copies must not use the Grep tool for `.claude/`.

### 15.3 Not verified

- `cli/roadmap/validate_prompts.py:130`, `rf-task-builder.md:383-389`, `test_implement_severity_static.py:485-498`, the 161 and 139 edit-table row counts, and the stoprule rubric lines: taken from the enrichment files, not re-read.
- Whether a delegate-only skill's refs can be read reliably by every agent kind at run time (the digest design avoids depending on it for grading).
- The run-2 percentages: taken from `grading-override.md` (read) and not recomputed; the override itself calls them an orchestrator estimate.
- Nothing about Jev's accuracy, calibration, latency or price for this task; no call was made.
- How many reflect Drift rows, tasklist Medium rows or spec-panel CRITICAL rows would flip under the rule: not measured.
