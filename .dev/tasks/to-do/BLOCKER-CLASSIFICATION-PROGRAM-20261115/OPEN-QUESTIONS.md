# Open questions and decisions: blocker classification (#552) and Review Panel unification

Single index of where decisions live, what the owner has answered, and what is still open. Documentation only: nothing here authorizes code changes, tests, issue filing, merges or implementation. Last updated 2026-11-16.

## 0. State on 2026-11-16 after the cuts debate

The owner asked for an adversarial debate on the proposed cuts and to proceed with the cuts that survived. Five read-only reviews (`/ponytail ultra`) proposed the cuts; three agents then debated them (`cuts-debate/adversarial/`); the merged result is `cuts-debate/final-cuts.md`. Result: 54 tasks in 5 plan packages became 19 tasks in 4 packages (stage 0: 3 tasks, stage 1: 2 tasks and absorbs stage 2's one surviving task, stage 3: 10, stage 4: 4; the stage 2 package is withdrawn). Section 3 below summarises what was cut and kept. Everything under "Pending" in section 4 is a recommendation, not an owner answer.

## 1. Where the sources are

| Topic | Source of truth |
|---|---|
| Blocker programme owner decisions OD1 to OD17 (options and recommendations) | `02-brainstorm/merged-requirements.md` section 15 (line 1023) in this folder; repeated in `09-plan-input.md` line 30 |
| Owner go for each stage | `stage-requests/README.md` (stage ledger) |
| Review Panel open items | `.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/MERGED-review-panel-unification.md` section 9.12 (line 9350); reviewed blob `5620c5d4be813fc3967d667fc76e0539ced86a9b` |
| Plan review findings per stage | `.dev/reflect/pre-TASK-WF-blockerStage<N>-*/` (`REPORT.md` where written, else `adversarial/merged-review-card.md`) |

Owner answers of 2026-11-16 are recorded in section 2 below as the owner gave them. Section 15 of the spec still shows the earlier recommendations and has not been edited.

## 2. Owner answers (2026-11-16)

### 2.1 Jev and blocker classification (#552)
- Investigate Jev for blocker classification. Data access and sharing stays a separate decision (OD3). No credentials, external transmission, paid evaluation or implementation are implied.
- The five-run experiment used Claude as a stand-in, not Jev. It does not prove Jev quality or ledger performance.
- Real blocking findings keep their established refactor and review process. The model-usage warning-only rule does not make all blocker handling informational.

### 2.2 Current workflow and legacy commands
- The active workflow is `/sc:workflow` and `/sc:implement`.
- `sprint run` in its current form is obsolete and is not tested as the current workflow.
- `/sc:task` and task-builder commands are to be retired, without evaluating them. This is a decision, not a claim that removal has happened.
- Only Sprint run and its CLI suite are evaluated, for measurable benefit versus retirement. Any return must be refactored around workflow and implement and properly evaluated. No outcome is assumed.
- Obsolete-command testing is not revived as if it represented the current workflow.

### 2.3 Review Panel unification
- **PR sequence:** merge one PR before opening the next. Sequencing guidance only.
- **Distinct models:** if the panel cannot fill every seat with a different model it may continue and may pass, while clearly disclosing reduced diversity. Duplicate models are never presented as independent. Other verdict criteria and real blocking findings are not waived.
- **Post-gate issues:** the identified issues should be fixed (desired outcome only).
- **Finding claim length:** 2,000 characters maximum. Supersedes the 300-character truncation and the intermediate open cap. Unlimited is not approved. No code claimed. Over-cap behaviour beyond the no-arbitrary-truncation concern is not decided and must not be invented.
- **Missing roster:** a review may complete with a warning when at least two valid reviewer reports exist and there are no obvious signs of failure.
- **Per-seat configuration:** deferred; no design inferred.
- **Exit outcomes:** must be distinguishable. Numeric assignments are not decided.
- **Review-ledger format version:** keep the existing one; backwards compatibility is not a concern. This does not settle whether `follow-ups/1` replaces or augments `review-ledger/1` (see 3.1).
- **Finding-grouping engines:** fix only the newer one for now.
- **Restricted reviewer launcher:** reuse the existing one, subject to verifying it meets the needs. If a second launcher is needed, extract the security policies into a shared module. Design decision only; suitability not verified.
- **Checkout-local `.claude` mirror:** keep the CI check; refresh a live checkout only on explicit request, never automatically from an installed release.
- **Installed-instruction path checks (G10):** keep the checks that stop installed instructions referencing repository-only paths.
- **Combined review-loop, severity and plugin-routing coverage:** earlier answer was to keep it and merge it into a single check. The later installation correction (below) must be read together with it.
- **Installation context correction:** IronClaude is not installed as a plugin. Assume the Coder template, or a git clone followed by SuperClaude installation. Reassess whether plugin-parity coverage is relevant; keep review-loop and severity checks. This is not a decision to remove plugin parity.
- **Static QA coverage:** keep static QA checks for active workflows; remove task-builder-specific checks as part of the task-builder retirement.
- **G16 safeguard:** remove it. Its architecture lint is duplicated under G9, which stays. The PR reminder's value is unverified, and the lost prompt is a recorded trade-off.
- **Salvage from malformed reviewer reports:** remove the proposed salvage of individual blocking findings. No separate handling or verdict policy for malformed reports is approved.
- **Q68 run log and integrity checks:** keep the existing run log, durability and partial-write handling checks and commit-identity checks. Not shown to have run or passed.

### 2.4 Session handling
Acknowledge an answer once, briefly, without repeating it; then move to the next applicable question. Do not invent questions or give duplicate receipts.

## 3. Scope after the cuts (what the plans now contain)

**Kept (the minimal programme).** Change the rule text where reviewers read it at run time and copy it atomically into all ten pinned files in one change; change the Medium offer in `pragmatic.md` from per loop to per run; the safety vocabulary scan as a standalone `superclaude review safety-scan` command; the approved `/sc:implement` final-step carrier in print-only form (prints `notes.md` minors, runs the scan, asks nothing; `refs/qa.md` untouched; plugin twin copied byte for byte because two tests pin it); the old-versus-new regrade as the one check that the new text keeps the real blockers (a lower bound); revert trigger RT1 worded "any real blocker found in a Medium list" plus the owner reading the first five runs' Medium lists; the post-fix mechanical-check helper (purpose unverified, kept); the existing ten-file copy test, one reverse scan and installed-path checks; owner-kept items (CI mirror check, G10, static QA checks for active workflows, Q68 run log, `review-ledger/1`).

**Cut.** The classifier and Jev machinery; the `follow-ups/1` ledger, codec, filing state machine, sweep, `follow-ups` command group, worker-contract keys and shadow summary (no new list file: the list is the reviewers' own "follow-up candidates" plus `notes.md`); the `sc-review-severity` skill folder, registry, scale map, doctor check and drift tests T1 to T17; the allow-list and `exempt-by-retirement` concept; the seeded-recall experiment and hash-bound rulings; the five-shadow-run gate and the stage 2 shadow stage; baselines M1, M12, M10b; stage 0 Tasks 2, 3, 5 to 8; the per-stage owner summaries except the stage 3 note that stage 4 reads; the plugin mirror and parity test.

**Review Panel (outside the plans, no code written).** Build later: claim cap 2,000 characters; two valid reports required only when two or more reviewers launched (keep the existing parsable-finding behaviour, the Q68 run log and integrity checks); distinct exit codes; clustering fix in the newer engine only; disclose reduced diversity; keep `review-ledger/1`. Do not build: raw-id launcher, run record and telemetry, `verify-run`, per-slot keys, older-engine fix, salvage of malformed reports.

### 3.1 Plan packages

| Stage | Package | Tasks now | Review history | State |
|---|---|---|---|---|
| 0 | `TASK-WF-blockerStage0-20261116-021044` | 3 | first review NEEDS-REVISION (2 blocking), revised; not re-reviewed | trimmed 2026-11-16; one reviewer pass owed |
| 1 | `TASK-WF-blockerStage1-20261116-030154` | 2 | three reviews, last NEEDS-REVISION (1 blocking, in a cut task) | trimmed and absorbs stage 2's print step; one reviewer pass owed |
| 2 | `TASK-WF-blockerStage2-20261116-030156` | 0 | reviews unfinished or superseded | withdrawn into stage 1 |
| 3 | `TASK-WF-blockerStage3-20261116-030158` | 10 | three reviews, last NEEDS-REVISION (3 blocking, all in cut tasks) | trimmed; one reviewer pass owed |
| 4 | `TASK-WF-blockerStage4-20261116-030206` | 4 | three reviews, last PASS (0 blocking, 7 Medium) | trimmed; one reviewer pass owed |

Reports: `.dev/reflect/pre-TASK-WF-blockerStage<N>-*/REPORT.md` (the subagents could not write them; the main session wrote them from the marked report bodies).

## 4. Open questions and decisions, trimmed

Everything here is a recommendation from the cuts debate until the owner says otherwise.

### 4.1 Pending: needs an owner answer (recommendation in brackets)
- OD1 skill folder for the full rule [no new folder; edit the carriers].
- OD2 how often the follow-up list is offered [once per run, plus at an escalation halt].
- OD5 gap-list or open-question entry counts as decision basis [no].
- OD9 who supplies the decision basis [reviewer-named, code-checked where quotable].
- OD11 replace "highest severity wins" in consolidation [yes at all lines, runtime-read ones first; the retired task and task-builder files stay unedited].
- OD12 grade a form defect as Decision when a named program consumer reads it by position [yes, folded into the digest wording, no parsing code].
- OD15 how the one issue is filed [the top-level session posts with explicit `--repo`; no digest, read-back or overflow handling].
- OD16 `rf-qa-qualitative` Rule 6 [option (b): rewrite and re-pin its one test].
- Review Panel: exit-code numbers (code 12 is unused at `ledger_cmd.py:13`) and the quorum denominator [count of reports received].
- Confirm that plugin parity is not removed: the plans add no plugin mirror but still copy the two `sc-implement-protocol` files to their plugin twin because two tests pin them.
- Confirm the two MDTM templates and the four rule prompts take the atomic copy of the rule text in stage 3 (the existing test pins them), while who dispatches those prompts is still unchecked.

### 4.2 Deferred until named evidence exists
- OD3 and the Jev investigation: until a fresh, unseen set shows reviewer labels over-block; nothing leaves the machine meanwhile.
- OD6 (no reflect data), OD7 (tasklist is in no plan), OD14 (needs real data; "never" holds).
- Per-seat configuration, over-cap claim behaviour (keep reject-and-warn), plugin parity beyond the pinned twins, the post-gate engine (`ensemble.py`).
- A cross-reviewer follow-up list file: add one plain file only if the owner later wants one list per run across reviewers.

### 4.3 Dropped or out of version 1
OD4 as a question (one-line non-goal: the classifier has no authority), OD8, OD10, OD13, OD17 (grep for citations in kept tasks owed), the replace-or-augment question about `follow-ups/1` against `review-ledger/1` (the follow-up ledger is not built), ledger version skew (backwards compatibility is not a concern), run 1's 48 migration steps, the five changed outcomes of the Review Panel report.

### 4.4 Decisions the plan author made that the owner has not confirmed
- The carrier is print-only because `refs/qa.md:225` says the final summary never asks the user anything and `qa.md` is on the do-not-edit list. Under `/sc:implement` a normal run keeps minors in `notes.md` unprinted today (`qa.md:225` and `:301` print only for legacy, N=1 and skip-final runs), so the print step is what makes the approved carrier work.
- `/sc:task`, task-builder and `rf-task-builder` are not edited; tests that pin only them are not re-pinned.
- Stage 3 and stage 4 stay separate packages with separate owner gos; the atomic copy into all ten files happens in stage 3.
- The post-fix helper (stage 3's `fixcheck`) is kept although its purpose is unverified once the ledger is cut.

### 4.5 Owed checks
Reachability of the four `rules/prompts/*_qa_prompt.md` files; whether anything reads the stage ledger README fields; one mechanical dependency check plus one reviewer pass of each trimmed package; the mapping of the REQ-01 block onto the five bullet positions the severity test reads (written into stage 3 Task 2).

### 4.6 Reviewer pass of the trimmed plans (2026-11-16): fixed, and minor follow-ups left open

One independent reviewer read each trimmed package. Stage 0: PASS. Stage 1: one blocking (Constraints named two edited files, Task 1 edits a third), fixed. Stage 3: one blocking (a Task 5 check that was already true today), fixed. Stage 4: PASS. Fixed with them: stage 3 entry check now requires the stage 0 RT1 reword, rollback removes created files, stage 4's rule-prompt `consumer-unknown` check scoped to the rewritten line.

Minor follow-ups, not fixed (minor findings never trigger a fix pass):
- Stage 0: name the grep flag (`-F` or `-E`) for the cap pattern; make the scan table rows per scope (`src` against `.claude`); spell out the section 10.3 merge-rule patterns; add an exact-case check for "any real blocker found in a Medium list" (stage 3 greps it in lower case); the RT1 "Detects" cell and RK8's "held-out half" still describe cut work; the spec's stage 0 row still lists step 0b.
- Stage 1: define what the scan's count includes; say what `--unattended` prints for an empty file; say whether `auth_token` counts as a hit; fix the paragraph's position inside the Done section; spell out the managed notes path.
- Stage 3: none open beyond the fixes.
- Stage 4: `recruiting_expert` principle 8 keeps its bare "benefit of the doubt" sentence; Task 4 is mostly verification; `skill_template.md` gets no merge text because it has no merge step; name the file where Task 1 records the cap and HALT counts.
