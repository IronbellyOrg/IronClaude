# Reviewer brief 2 — persona: qa (model class haiku, reviewer t4-1)

## T1 card excerpt

## Coverage verdict

Parsed coverage 1.00 (12/12 design sections the task vocabulary names are mapped).
Union coverage 0.80: four requirement rows from design section 18 (coordinator-approved
amendments A0-A6, dated 2026-10-31, which "override any earlier text they contradict") are
not satisfied by the plan as written.

## Findings (Tier 1)

T1-F1 [MAJOR, contradiction] Task 7 pins superseded completion semantics.
Task 7 body says `codex_review_state` has "completion time = `updated_at`" and its AC makes
"two summary comments" classify `polling`. Amendment A1 (design s18) redefines completion as
the LATER of the marker `updated_at` and the newest completing review's `submitted_at`;
amendment A3 makes multiple valid markers resolve to the latest `updated_at` (only same-time
ties poll). An executor following Task 7 verbatim implements both rules wrong and writes
tests asserting the wrong behavior.
citations: plan:91,95 -> spec(design):439-443,452-454

T1-F2 [MAJOR, contradiction] Task 2's second AC asserts A0 reversed.
Plan AC: "A local override YAML without Codex fields still loads (Codex identities empty, so
Codex is disabled for that override)". A0: absent keys FALL BACK to shipped values; only an
explicit empty/null disables. The executor would write a test pinning the wrong semantics.
Ground truth: progress.md records the coordinator overturning exactly this mid-run ("T2:
Ruling: accept T2 F1.1 ... yes-fallback"), and shipped detection.py:157-158 implements A0 —
evidence the contradiction was live, not theoretical.
citations: plan:44 -> spec(design):434-437, progress.md T2 Ruling

T1-F3 [MAJOR, missing requirement] Amendment A6 (root-selection later-of rule) is in no task.
A6 overrides design s7's "created no later than completion" wording after a live PR 337
incident (root stamped 1s after review submission polled to terminal_timeout, 622 s). Task 7
passes "the marker time" to `_thread_findings` — the pre-A6 rule. No task, AC or test item
carries A6. (Shipped classifier.py:321 implements A6; again corrected outside the plan.)
citations: spec(design):467-479 -> plan:91 (absent)

T1-F4 [MINOR, partial] A2's augment-absent-continue rule lacks an AC.
When Augment alone hits TERMINAL_AUGMENT_NO_RESPONSE with Codex present, the run must record
reviewer_absent{augment} and CONTINUE with Codex. Task 12 says only "Wave 1 records
reviewer_absent / reviewer_incomplete"; no AC pins the continue rule or A2's absent-set
input to the wait outcomes (Task 8 signature has no absent-set parameter).
citations: spec(design):445-449 -> plan:102,147

T1-F5 [MINOR, weak AC] Task 15's grep AC cannot enforce its rule.
"`grep -n "the Augment review" CLAUDE.md docs/user-guide/commands.md` returns no pr-submit
sentence that omits Codex" — grep returns the matching lines; deciding none is a pr-submit
sentence that omits Codex is judgment, not the grep's exit state. Recurring repo pattern:
grep-count ACs do not gate exact rule text (deviation-patterns, shadow04/shadow06).
citations: plan:182

T1-F6 [MINOR, partial] A5 report/dedup specifics only partially in Task 12.
"flagged by: augment, codex" report line, fix_applied per member fix_key, and "S5 wait covers
only re-triggered reviewers" appear in the design amendment but not in Task 12's bullet list.
citations: spec(design):459-466 -> plan:147
End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:11:33Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-implementTheDesi-20261031-182028/TASK-WF-implementTheDesi-20261031-182028.md:1-183

```md
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementTheDesi-20261031-182028
version: "1"
priority: Medium
created_date: "2026-10-31"
---

# Make /sc:pr-submit handle Codex review threads like Augment

Source: ./source.md
Goal: /sc:pr-submit detects, polls, classifies, re-grades, verifies, fixes (Medium or higher), replies to, resolves and re-triggers Codex (chatgpt-codex-connector) review threads through the same path as Augment threads, with Augment-only, Codex-only, both and neither PRs all handled, as specified in .dev/pr-submit-codex/design/pr-submit-codex-design.md (the design; section numbers below refer to it).

## Constraints

- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.

## Phase 1: Core models, contract and run-log

## Task 1: Add the reviewer field and the two reviewer events to the models

Edit src/superclaude/pr_submit/models.py per design sections 7 and 13: add `reviewer: str = "augment"` to `Finding`, add `EventType.REVIEWER_ABSENT = "reviewer_absent"` and `EventType.REVIEWER_INCOMPLETE = "reviewer_incomplete"`, and update the class docstrings that state the member count (39 → 41). Update tests/pr_submit/test_run_log.py test_eventtype_is_39_members_with_silence_events to assert 41 members including the two new values.

Acceptance criteria:
- `len(EventType) == 41` and both new values exist; `Finding(path="a", line=1, body="b").reviewer == "augment"`.
- `uv run pytest tests/pr_submit/test_run_log.py -q -p no:cacheprovider` passes.

## Task 2: Add the Codex fields to the detection contract

Edit src/superclaude/pr_submit/detection.py and the YAML block in src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md per design section 14: `codex_bot_login` (shipped "chatgpt-codex-connector[bot]"), `codex_app_slug` (shipped "chatgpt-codex-connector"), `codex_retrigger_phrase` (default "@codex review"). `from_yaml` trims the identities like the Augment ones. Direct `DetectionContract()` construction keeps both Codex identities empty (fail-safe, same as Augment), while the shipped ref supplies the real values.

Acceptance criteria:
- `DetectionContract.load()` returns the two Codex identities and the "@codex review" phrase; `DetectionContract()` has empty Codex identities.
- A local override YAML without Codex fields still loads (Codex identities empty, so Codex is disabled for that override) and existing tests in tests/pr_submit/test_detection_contract.py pass.

## Task 3: Fold re-trigger count by cycle and rebuild absent reviewers

Depends on: Task 1

Edit src/superclaude/pr_submit/run_log.py `rebuild_state` per design sections 5 and 12: `rereview_request_count` counts distinct `cycle_id` values of `rereview_requested` events (an event without `cycle_id` counts once each), and a new `absent_reviewers` sorted list is folded from `reviewer_absent` events' `reviewer` field.

Acceptance criteria:
- Two `rereview_requested` events with the same `cycle_id` and different `reviewer` rebuild to `rereview_request_count == 1`; two events without `cycle_id` rebuild to 2.
- A `reviewer_absent{reviewer:"codex"}` event rebuilds to `absent_reviewers == ["codex"]`.
- Existing tests in tests/pr_submit/test_run_log.py, test_review_retrigger.py and test_crash_recovery.py pass.

## Phase 2: Codex adapter, merge and dedup in the core

## Task 4: Generalise thread selection and activity over an identity set

Edit src/superclaude/pr_submit/classifier.py per design section 14: `_thread_findings(threads, contract, completed, identities=None)` uses the given identity set (default: the Augment identities, so Augment behaviour is unchanged), and a new `has_reviewer_activity(payload, identities)` returns whether any review or comment, or any thread root, is authored by those identities. `has_augment_activity` keeps its current result.

Acceptance criteria:
- With no `identities` argument every existing classifier test passes unchanged (`uv run pytest tests/pr_submit/test_cosmos_review.py tests/pr_submit/test_cosmos_protocol.py tests/pr_submit/test_silence.py -q -p no:cacheprovider`).
- An Augment payload that also contains Codex-rooted unresolved threads yields the same `actionable_finding_comments` result as without them.

## Task 5: Carry the reviewer name through finding normalisation

Depends on: Task 1

Edit src/superclaude/pr_submit/severity_router.py `finding_from_comment`: read an optional text `reviewer` key from the root (default "augment"; a non-text value raises `ValueError` like the other text fields) and pass it to `Finding`. No change to `remap_severity` or `route`.

Acceptance criteria:
- `finding_from_comment({...,"reviewer":"codex","severity_hint":"medium"}).reviewer == "codex"`; a root without the key gives "augment".
- tests/pr_submit/test_severity_router.py passes.

## Task 6: Add the reviewer adapter table and the Codex priority parser

Depends on: Task 2

Create src/superclaude/pr_submit/reviewers.py per design sections 4, 7 and 14 with: `REVIEWERS = ("augment", "codex")`, `reviewer_identities(contract, reviewer)`, `retrigger_phrase(contract, reviewer)` (Augment: first `accepted_trigger_phrases` entry, i.e. "auggie review"; Codex: `codex_retrigger_phrase`), `reviewer_activity(payload, contract)`, `parse_codex_priority(body)` (exactly one `![P<n> Badge](https://img.shields.io/badge/P<m>-...)` with n == m in 0-3 on the first non-blank line, colour ignored, else None) and `codex_severity_hint(priority)` (P0 critical, P1 high, P2 medium, P3 low, None → None). No gh or git tokens.

Acceptance criteria:
- `parse_codex_priority` returns "P0".."P3" for the four badges and None for no badge, two badges, P4, and alt/URL mismatch.
- `route(remap_severity(finding_from_comment(root)))` for roots carrying the mapped hint gives `--depth deep --fix` for P0 and P1, `--fix` for P2, report-only for P3, and `--fix` (Medium fail-safe) for a malformed badge.

## Task 7: Classify Codex completion and select Codex finding roots

Depends on: Task 4, Task 5, Task 6

Add to src/superclaude/pr_submit/reviewers.py per design section 7: `codex_review_state(payload, contract, *, watermark=None, current_head_sha=None)` (exactly one Codex-authored issue comment with one bounded `<!-- codex-review-state:v1 {JSON} -->` marker, duplicate keys rejected, `code_review.status`/`commit_sha`/`has_any_findings` validated, completion time = `updated_at`, no later than `observed_at`, strictly newer than the watermark when given), `classify_codex(...)` returning polling/clean/findings by the design's Codex gate state rules (requires the payload completeness flags like the Augment gate), `codex_finding_comments(...)` (unresolved Codex-rooted threads through `_thread_findings` with the Codex identities and the marker time, each root dict gaining `reviewer: "codex"`, `codex_priority` and `severity_hint`), and `list_review_threads(payload, contract)` returning every Augment- or Codex-rooted thread (resolved or not) as `{reviewer, path, line, original_line, is_resolved, priority, severity, thread_id, comment_id}` for reports. Then run the read-only dry check: `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh --pr 336 --repo IronbellyOrg/IronClaude` piped into `uv run python` calling `list_review_threads` with `DetectionContract.load()`, saving the output to ./artifacts/t7-dry-check-pr336.txt.

Acceptance criteria:
- A PR 334-shaped payload (completed, `has_any_findings:false`, no Codex review) classifies `clean`; a PR 336-shaped payload (three unresolved Codex roots with P2 badges) classifies `findings` with three roots carrying `reviewer == "codex"` and `severity_hint == "medium"`.
- Running status, wrong head, two summary comments, malformed or duplicate-key JSON, `updated_at` after `observed_at`, and `updated_at` not newer than the watermark each classify `polling`.
- ./artifacts/t7-dry-check-pr336.txt lists the three resolved Codex threads of PR 336 with priority P2 and severity Medium.

## Task 8: Add per-reviewer wait outcomes and the merge truth table

Depends on: Task 6

Add to src/superclaude/pr_submit/reviewers.py per design section 6: `augment_wait_outcome(state, next_state)` (pending / done / absent / incomplete from the existing gate state and `poll_outcome` result), `codex_wait_outcome(state, *, active, elapsed, timeout, silence_timeout, other_settled)` and `merge_wait(augment, codex)` returning `{"outcome", "used", "absent", "incomplete"}` with outcome in polling / clean / findings / declined / no_response / timeout, exactly per the design's merge table rows.

Acceptance criteria:
- Every row of the design section 6 merge table has a matching assertion (Augment only, Codex only, both done, neither present, pending on either side, incomplete combinations, Augment declined).
- An inactive Codex is `absent` as soon as Augment is settled, and before that only at the silence deadline.

## Task 9: Add cross-reviewer dedup, pending re-triggers and package exports

Depends on: Task 1, Task 6

Add to src/superclaude/pr_submit/reviewers.py per design sections 9 and 12: `dedup_groups(findings)` (group by path and `line`, falling back to `original_line` when `line` is None, input order kept, every finding kept) and `pending_retriggers(events, cycle_id, present)` (present reviewers without a `rereview_requested` event for that `cycle_id`; an event without `reviewer` counts as augment). Export the public reviewers functions and `has_reviewer_activity` from src/superclaude/pr_submit/__init__.py.

Acceptance criteria:
- Augment and Codex findings on the same path and line form one group of two; different lines form separate groups; a null `line` groups by `original_line`.
- After a log holding only `rereview_requested{cycle_id:"c1", reviewer:"augment"}`, `pending_retriggers(events, "c1", ["augment","codex"]) == ["codex"]`.
- `from superclaude.pr_submit import merge_wait, classify_codex, dedup_groups` works.

## Phase 3: Tests

## Task 10: Write the Codex unit tests and fixtures

Depends on: Task 7, Task 8, Task 9

Create tests/pr_submit/test_codex_reviews.py and fixtures under tests/pr_submit/fixtures/ (codex-clean-pr334.json, codex-findings-pr336.json built from the real shapes in design section 2) covering design section 16 items 1-5, 7 and 8: badge parsing for P0-P3 and malformed badges, severity mapping, Codex completion and gate states, reviewer detection and `merge_wait` for Augment only / Codex only / both / neither, Augment classification unchanged with Codex threads present, `dedup_groups`, and the run-log folds (41 events, distinct-cycle re-trigger count, `absent_reviewers`, `pending_retriggers`).

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_codex_reviews.py -q -p no:cacheprovider` passes, with each listed area having at least one test.
- `uv run pytest tests/pr_submit -q -p no:cacheprovider` passes; output saved to ./artifacts/t10-pytest-pr-submit.log.

## Task 11: Generalise the script wording and test reply-resolve on a Codex thread

Depends on: Task 10

Edit the header comments and messages of src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh, retrigger-review.sh and poll-augment-review.sh to name review findings from Augment or Codex instead of Augment only (design sections 10 and 11; logic, arguments, exit codes and file names unchanged; the retrigger default body stays "auggie review"). Add to tests/pr_submit/test_codex_reviews.py a test that runs reply-resolve-thread.sh against a fake `gh` on PATH (the adapter pattern in tests/pr_submit/test_cosmos_poll.py) with a Codex-rooted thread, and a test that retrigger-review.sh posts the given `--body "@codex review"`.

Acceptance criteria:
- The reply-resolve test shows the reply POST to the Codex root comment id followed by the resolveReviewThread mutation on that thread id; an already resolved Codex thread is skipped without a reply.
- tests/pr_submit/test_cosmos_poll.py, test_static_grep.py, test_review_retrigger.py and test_edge_cases.py still pass.

## Phase 4: Skill, refs and command

## Task 12: Update SKILL.md for two reviewers

Depends on: Task 9

Edit src/superclaude/skills/sc-pr-submit-protocol/SKILL.md per design sections 4-13: the description, Purpose and attended poll loop name Augment and Codex; the snapshot gate code block adds the Codex gate and `merge_wait` exactly as in design section 14; Wave 1 records `reviewer_absent` / `reviewer_incomplete`; Waves 2-4 use `dedup_groups` and name the reviewer in run-log events; Wave 6 re-triggers each present reviewer via `pending_retriggers` and `retrigger_phrase` with a per-reviewer watermark; the Output Contract adds `reviewers`; `terminal_augment_no_response` is described as no configured reviewer responding. Then run make sync-dev and make verify-sync.

Acceptance criteria:
- SKILL.md references only installed-safe names (the `superclaude.pr_submit` package, `scripts/...`, `refs/...`); `grep -n 'src/superclaude' src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` finds no new hit.
- make verify-sync passes and tests/pr_submit/test_skill_parse.py passes.

## Task 13: Update the detection, poll, severity and verification refs

Depends on: Task 12

Edit, in src/superclaude/skills/sc-pr-submit-protocol/refs/: detection-contract.md prose (Codex identities, the codex-review-state:v1 marker contract, badge parser, observed-format caveat), augment-poll.md (one snapshot for both reviewers, per-reviewer wait outcomes, merge table, Codex absence rule), severity-routing.md (P0-P3 → hint mapping table, reviewer-neutral wording), finding-verify.md (per-finding verdicts inside dedup groups) and troubleshoot-dispatch.md (group seed with every verified body and the reviewer names). Keep T-N50 purity for severity-routing.md (no gh or git tokens).

Acceptance criteria:
- Each of the five refs names Codex where it previously said Augment-only behaviour, matching design sections 5-9.
- tests/pr_submit/test_static_grep.py and test_skill_parse.py pass; make verify-sync passes after make sync-dev.

## Task 14: Update the reply, re-trigger, loop-guard and state-machine refs and the command

Depends on: Task 12

Edit, in src/superclaude/skills/sc-pr-submit-protocol/refs/: thread-reply.md (Augment or Codex root id), review-retrigger.md (per-reviewer phrase including "@codex review" marked UNVERIFIED for summary-marker update, per-reviewer watermark, `pending_retriggers`), loop-guard.md (41 event types listed, distinct-cycle INV-R1 fold, `reviewer` field, `absent_reviewers`) and state-machine.md (reviewers merged before the FSM, no new state, no-response meaning); and src/superclaude/commands/pr-submit.md (description, Arming and Boundaries name both reviewers and the Codex contract fields).

Acceptance criteria:
- loop-guard.md lists all 41 event types including reviewer_absent and reviewer_incomplete; state-machine.md and loop-guard.md stay free of gh and git tokens.
- tests/pr_submit/test_static_grep.py, test_skill_parse.py and tests/skills/test_primitive_dual_surface_lookup.py pass; make sync-dev then make verify-sync pass.

## Phase 5: User docs and changelog

## Task 15: Update the user-facing docs and the changelog

Depends on: Task 14

Edit only the sentences that state Augment-only pr-submit behaviour: CLAUDE.md (the mandatory-way paragraph: waits for the Augment and Codex reviews), docs/user-guide/commands.md (the /sc:pr-submit "When to use" paragraph), docs/guides/tdd-skill-release-guide.md and docs/guides/prd-skill-release-guide.md (needs the Augment Code or Codex review app). Add an Unreleased entry to CHANGELOG.md describing Codex support, the fail-open reviewer detection, the P0-P3 mapping, dedup, per-reviewer re-trigger and the UNVERIFIED re-review marker update. Run make lint and the named pytest set.

Acceptance criteria:
- `grep -n "the Augment review" CLAUDE.md docs/user-guide/commands.md` returns no pr-submit sentence that omits Codex.
- make lint passes; `uv run pytest tests/pr_submit tests/skills/test_primitive_dual_surface_lookup.py tests/unit/test_cli_install.py tests/core/test_how_we_work_routing_table.py -q -p no:cacheprovider` passes with output saved to ./artifacts/t15-pytest.log.
```

### .dev/pr-submit-codex/design/pr-submit-codex-design.md:1-479

```md
# Design: /sc:pr-submit handles Codex review threads like Augment

- Command: `/sc:design pr-submit-codex-reviews --type component --format spec`
- Date: 2026-10-31
- Branch: `feat/pr-submit-codex-reviews`
- Status: complete (validated against the code read in section 3 and the PR 334/335/336 data in section 2)

## 1. Problem and goal

`/sc:pr-submit` (command `src/superclaude/commands/pr-submit.md`, skill
`src/superclaude/skills/sc-pr-submit-protocol/`, deterministic core `src/superclaude/pr_submit/`)
only polls, verifies, fixes, replies to and resolves review threads from Augment
(`augmentcode[bot]` / `augmentcode`). On PRs 335 and 336 the ChatGPT Codex Connector bot left five
P2 review threads that the monitor never saw, so they were fixed by hand.

Goal: Codex review threads go through exactly the same path as Augment threads: detect, poll,
classify, re-grade, verify, diagnose, fix (Medium or higher), validate, push, reply, resolve,
re-trigger, loop-guard. Low and Nit stay report-only. Augment-only PRs behave exactly as today;
Codex-only PRs work; PRs with neither reviewer end as today.

Non-goals: Codex "security review" results, Codex answering questions or editing the PR
(`@codex address that feedback`), any other review bot.

Scope note: the deterministic core `src/superclaude/pr_submit/` is part of the skill (SKILL.md
defers every classification decision to it and forbids a second body parser), so the Codex parser
lives there, not in the markdown or the bash scripts.

## 2. Evidence: what Codex actually posts (observed on PRs 334, 335, 336)

Read with `gh api graphql` and `gh api repos/IronbellyOrg/IronClaude/...` on 2026-10-31.

| Surface | Observed shape |
|---|---|
| Author | REST `user.login` = `chatgpt-codex-connector[bot]` (`type: Bot`); GraphQL `author.login` = `chatgpt-codex-connector`. Same two-shape pattern as Augment. |
| Summary issue comment | One PR conversation comment created seconds after the PR opens and **edited in place** (`created_at` 14:38:21, `updated_at` 14:40:37 on PR 335). Body starts `<!-- codex-pull-request-review-summary -->` then `<!-- codex-review-state:v1 {JSON} -->`. JSON: `{"code_review":{"commit_sha":"<40 hex>","has_any_findings":bool,"has_unresolved_findings":bool,"status":"completed"},"security_review":{...}}`. |
| Clean review | PR 334: summary with `code_review.status:"completed"`, `has_any_findings:false`; **no formal review, no review thread, and no visible reaction**. The marker is the only completion evidence. |
| Review with findings | One formal review (`state: COMMENTED`, `commit_id` = reviewed head) whose body starts `<!-- codex-review-receipt:v1 -->` and `### 💡 Codex Review`, plus one inline root comment per finding, each the root of its own review thread (`pull_request_review_id` set, `in_reply_to_id` null, `line` null once outdated, `original_line` set). |
| Finding body | First line: `**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  <title>**`, then prose, then `Useful? React with 👍 / 👎.`, then `<!-- codex-code-review-finding:v1 -->`. Only P2 (yellow) occurs in this repo's history; P0, P1, P3 colours were not observed. |
| Stale marker | After the five threads were resolved, `has_unresolved_findings` still read `true`: the summary is not updated on resolve, so threads (not the marker) are the source of truth for open findings. |
| Re-review on push | Not observed: PRs 334, 335, 336 each got one Codex review ("Review trigger: PR opened") although later commits were pushed. |
| Documented triggers | The bot's own text: "Reviews are triggered when you open a pull request for review, mark a draft as ready, comment "@codex review"". OpenAI docs (https://learn.chatgpt.com/docs/third-party/github): "In a pull request comment, mention `@codex review`", and an optional "Automatic review" setting. |

## 3. Current system (read before designing)

- **Poll script** `scripts/poll-augment-review.sh`: one repo-pinned snapshot (PR metadata, REST
  reviews, REST issue + inline comments, GraphQL review threads with root comment, author,
  `pullRequestReview{commit{oid}}`), completeness flags, `observed_at`. It is already
  reviewer-neutral in what it fetches: Codex's summary comment, review and threads are all in the
  snapshot today. Nothing in it filters by author.
- **Classifier** `pr_submit/classifier.py`: `classify` / `actionable_finding_comments` share one
  selection; identities come only from `contract.augment_bot_login` / `augment_app_slug`.
  `_thread_findings` selects unresolved roots authored by those identities, validated against a
  completion review time. Cosmos completion uses a validated HTML-comment JSON marker.
- **Severity** `pr_submit/severity_router.py`: `finding_from_comment` (explicit `severity_hint`
  wins, else one `**Severity:**` line, else Medium fail-safe) → `remap_severity` → `route`
  (Critical/High `--depth deep --fix`, Medium `--fix`, Low/Nit report-only).
- **FSM** `pr_submit/fsm.py`: `poll_outcome` (Augment silence/timeout), `transition` table,
  INV-001 increment at `S5_AWAITING_REREVIEW → S2_CLASSIFY` on `rereview_attributed`.
- **Run log** `pr_submit/run_log.py`: closed `EventType` enum (39 members), `rebuild_state`
  folds `rereview_requested` as a plain count (INV-R1: `rereview_request_count <= max_rounds`).
- **Recovery** `pr_submit/recovery.py`: a landed push resumes at S5a unless a
  `rereview_requested` event exists for that `cycle_id`.
- **Reply/resolve** `scripts/reply-resolve-thread.sh`: identifies the thread by root
  `databaseId` (optionally `--thread-id`), replies, then `resolveReviewThread`. The logic is
  author-independent; only its header wording says "Augment".
- **Re-trigger** `scripts/retrigger-review.sh`: one issue-comment POST, body defaults to
  `auggie review`, already parameterised by `--body`.
- **Detection contract** `refs/detection-contract.md` YAML + `DetectionContract` dataclass:
  Augment identities and decline regexes; optional local override.
- **Plugin twins**: `plugins/superclaude/` has no pr-submit command or skill, so the mirror rule
  has nothing to update here (checked with `find plugins -iname '*pr-submit*'`: no result).

## 4. Design overview: one reviewer-agnostic path, one small adapter per reviewer

The snapshot is already shared (one poll per round covers both bots). What differs per reviewer
is only: who the author is, how completion is proven, how severity is read, and what comment asks
for a re-review. Everything after "a list of normalized `Finding` objects" is already
reviewer-agnostic and is reused unchanged.

```text
poll-augment-review.sh  (one snapshot, unchanged data)
        │
        ├── augment adapter: classify / actionable_finding_comments   (existing, unchanged)
        └── codex adapter:   classify_codex / codex_finding_comments  (new, same gate rules)
        │
merge_wait()  ── per-reviewer wait outcome → one round outcome (pure truth table)
        │
dedup_groups() ── group same path+line across reviewers
        │
finding_from_comment → remap_severity → route        (existing; Codex sets severity_hint)
evidence-validator → troubleshoot → fix → VAL         (existing)
push triad → reply-resolve-thread.sh per thread       (existing script, wording generalised)
retrigger-review.sh per present reviewer              (existing script, --body per adapter)
```

Adapter table (new module `pr_submit/reviewers.py`), values read from the detection contract so a
local override can change or blank them:

| Field | augment | codex |
|---|---|---|
| identities | `augment_bot_login`, `augment_app_slug` | `codex_bot_login` (`chatgpt-codex-connector[bot]`), `codex_app_slug` (`chatgpt-codex-connector`) |
| completion proof | formal review / Cosmos marker (existing) | `codex-review-state:v1` marker, `code_review.status == "completed"` for the expected head |
| severity | `severity_hint` / `**Severity:**` line (existing) | P0-P3 badge on the first line (section 7) |
| re-trigger body | `auggie review` (existing) | `codex_retrigger_phrase` = `@codex review` |
| silence poke | yes, L3, once (existing INV-S1) | no (section 5) |
| decline | "abnormally large" (existing) | none |

A blank identity set disables that reviewer (it is never present). No new provider abstraction
beyond this table: two reviewers, one dict, no class hierarchy.

## 5. Reviewer detection and fail-open

A reviewer is **present** on the PR when the snapshot holds at least one entry authored by its
identities (a review, an issue or inline comment, or a thread root):
`reviewer_activity(payload, contract) -> {"augment": bool, "codex": bool}`.

- Codex posts its summary comment seconds after a PR opens, long before any review (Augment's
  reviews on PRs 335/336 took about 4-5 minutes), so a connected repository shows Codex activity
  within the first polls. Codex with no activity when Augment's wait outcome is already settled,
  or by the silence deadline (`--silence-timeout`, default 300 s), is **absent**: the run appends
  `reviewer_absent{reviewer:"codex"}` and ignores Codex for the rest of the run (no wait, no
  re-trigger). There is no Codex silence poke: posting `@codex review` on a repository without the
  Codex connector only produces an error reply, and absence here means "not installed".
- Augment keeps its existing silence path unchanged (optional single L3 poke, then
  `TERMINAL_AUGMENT_NO_RESPONSE` when it alone decides the run). When Augment reaches that
  silence outcome but Codex is present, Augment is recorded absent (`reviewer_absent{reviewer:
  "augment"}`) and the round continues with Codex alone.
- Absence is sticky and rebuilt from the run log on `--resume` (`rebuild_state()["absent_reviewers"]`).
- Neither reviewer present: unchanged `TERMINAL_AUGMENT_NO_RESPONSE` (status value kept for
  compatibility; its message now says "no configured reviewer (Augment, Codex) responded").

Augment-only PR: Codex becomes absent no later than the poll on which Augment settles (or at
the silence deadline if Augment is still pending), so the wait never runs longer than today and
every Augment outcome, status and event is the same as today plus one `reviewer_absent` event. Codex-only PR: Augment's silence outcome marks it absent; Codex's
result drives the round.

## 6. Polling both reviewers in one round, and the terminal conditions

Each poll runs the existing Augment snapshot gate and, on the same snapshot with the same
`expected_head`, the Codex gate. Each reviewer gets a **wait outcome**:

| Wait outcome | augment (from existing gate + `poll_outcome`) | codex (`codex_wait_outcome`) |
|---|---|---|
| `pending` | `polling` and `poll_outcome` is `S2_CLASSIFY` or `S5C_SILENCE_REREQUEST` | no completion yet, and (active, not timed out) or (inactive, before silence deadline, and Augment not settled) |
| `done` | gate state `clean` / `findings` / `declined` | gate state `clean` / `findings` |
| `absent` | `TERMINAL_AUGMENT_NO_RESPONSE`, or already absent | inactive at silence deadline, or already absent |
| `incomplete` | `TERMINAL_TIMEOUT` (partial activity) | active but no completion at `--timeout` |

`merge_wait(augment, codex)` (pure, row-tested) maps the pair to the round outcome:

| augment | codex | round outcome |
|---|---|---|
| `pending` | any | keep polling |
| any | `pending` | keep polling |
| `done: declined` | any settled | `declined` (existing S5b fallback; Codex `findings` join the fallback's single Waves 2-6 re-entry) |
| `done` | `done` | `findings` if either has findings, else `clean` |
| `done` | `absent` / `incomplete` | Augment's state (Codex incomplete is reported) |
| `absent` / `incomplete` | `done` | Codex's state (Augment's condition is reported) |
| `absent` | `absent` | `TERMINAL_AUGMENT_NO_RESPONSE` (unchanged) |
| `incomplete` | `absent` / `incomplete` | `TERMINAL_TIMEOUT` (unchanged) |
| `absent` | `incomplete` | `TERMINAL_TIMEOUT` (partial reviewer activity, no classified review) |

Both reviewers share the one `--timeout` wall clock and one `--poll-interval`; no second wait is
added. In the S5 re-review wait only reviewers that were re-triggered in this cycle are waited
for; a reviewer that is `incomplete` at S5 expiry is reported and the other's attributed result
is used. The re-review is **attributed** (the INV-001 edge) when at least one re-triggered
reviewer reaches `done` (clean or findings) attributed to the pushed SHA; `timeout` when none
does; `declined` when Augment declines (existing).

## 7. Parsing Codex findings and mapping P0-P3 onto severity routing

**Completion** (`codex_review_state(payload, contract, expected_head, watermark)`): exactly one
issue comment authored by a Codex identity carries one `<!-- codex-review-state:v1 {JSON} -->`
marker (bounded length, JSON object, duplicate keys rejected, same as the Cosmos marker). Valid
when `code_review.status` is a string, `code_review.commit_sha` is 40 hex,
`code_review.has_any_findings` is a boolean. Completed only when `status == "completed"`,
`commit_sha == expected_head`, the comment's `updated_at` is a parseable aware time no later than
`observed_at`, and (with a watermark) strictly newer than the watermark. Anything else (two
summary comments, malformed JSON, `running`, wrong head, missing time) is `polling`, never clean.
The `security_review` object is ignored.

**Findings** (`codex_finding_comments`): unresolved review threads whose root is Codex-authored,
selected by the existing `_thread_findings` rules generalised to take an identity set and a
completion time (root-only, unique ids, `pullRequestReview` with a commit, nullable current
line, `original_line` hint, created no later than completion). Resolved threads are excluded;
older unresolved Codex roots stay visible (same as Augment).

**Codex gate state**: completion missing → `polling`; selection invalid → `polling`; unresolved
roots → `findings`; none and `has_any_findings` false → `clean`; none, `has_any_findings` true
and a Codex formal review exists for the expected head (its threads were all resolved) → `clean`;
otherwise `polling` (findings promised but not yet visible).

**Badge parser** (`parse_codex_priority(body) -> "P0".."P3" | None`): the body must contain
exactly one badge image `![P<n> Badge](https://img.shields.io/badge/P<m>-<colour>?...)` with
`n == m` and `n` in 0-3, on the first non-blank line. Colour is not checked (only P2 yellow was
observed). Zero badges, two badges, `P4`, or alt/URL disagreement → `None`.

**Mapping** onto the existing tiers (the priority is the reviewer's own hint, exactly like
Augment's `**Severity:**` line):

| Codex | `severity_hint` | Route after `remap_severity` (no category, default confidence) |
|---|---|---|
| P0 | `critical` | `--depth deep --fix` |
| P1 | `high` | `--depth deep --fix` |
| P2 | `medium` | `--fix` |
| P3 | `low` | report-only |
| malformed / none | not set | Medium fail-safe (existing NFR-4 rule) → `--fix` after verification |

`codex_finding_comments` adds `severity_hint`, `reviewer: "codex"` and `codex_priority` to each
selected root dict; `finding_from_comment` already gives an explicit hint precedence. Augment
roots get `reviewer: "augment"`. `Finding` gains one field, `reviewer: str = "augment"`.

## 8. Re-grade, verification and troubleshoot dispatch (reused)

No change to `remap_severity`, `route`, `refs/finding-verify.md` (evidence-validator, verified /
unverified, no round for unverified) or `refs/troubleshoot-dispatch.md` (seed, `--scope`,
routes, never `--depth quick --fix`). The refs change only their wording from "Augment finding"
to "review finding (Augment or Codex)" and the seed names the reviewer.

## 9. Dedup when both reviewers flag the same line

PR 336 had Augment and Codex threads on the same three lines with the same defect.
`dedup_groups(findings) -> list[list[Finding]]` (pure) groups findings by
`(path, line if line is not None else original_line)`, in input order, and keeps every finding.

- Severity and route of a group = the highest remapped tier in the group.
- Verification still produces one verdict **per finding** (one evidence-validator batch); a
  group is dispatched only if at least one member is verified, with every verified body in the
  troubleshoot seed, so two different claims on one line are both fixed, never silently merged.
- One diagnosis and one set of edits per group (no double fix); `fix_applied` is recorded for
  each member's `fix_key`.
- Every verified thread in the group gets its own reply and resolve, all citing the cycle's one
  fix SHA. An unverified or Low/Nit member is handled as today: no reply, no resolve, listed in
  the report.
- The report lists a group once, with "flagged by: augment, codex".

## 10. Reply and resolve

`scripts/reply-resolve-thread.sh` already identifies a thread only by its root `databaseId`
(and optional `--thread-id`), checks the PR's threads completely, skips a resolved thread, replies
first and then resolves. None of that depends on the author, so a Codex root works unchanged. The
change is wording only: the header and messages say "review finding" instead of "Augment
finding"; no second copy of the script. `refs/thread-reply.md` says the `<COMMENT_ID>` is the
Augment or Codex root id. The reply text (`build_reply`) is unchanged; the reply on a Codex
thread is posted by the operator's identity like any other reply.

## 11. Re-trigger after a push

Neither bot reviews a pushed commit by itself in this repository (section 2). After the push,
reply and resolve, and only when the cycle applied edits, the SKILL posts one re-trigger comment
**per present reviewer** with `scripts/retrigger-review.sh --pr <N> --repo "$REPO" --body
<adapter phrase>`: `auggie review` for Augment (unchanged), `@codex review` for Codex. Each post is
preceded by a write-ahead `rereview_requested{cycle_id, reviewer}` check: a reviewer that already
has one for this `cycle_id` is not posted again (crash safety, INV-R1). Each reviewer gets its own
watermark (UTC recorded right after its own successful POST), used only for that reviewer's
completion attribution.

`@codex review` is the trigger documented by OpenAI and by the bot's own summary text. Whether a
Codex re-review after `@codex review` updates the same summary comment with the new
`commit_sha` (as the marker format implies) has not been observed in this repository:
**UNVERIFIED** until the dry run in this task's PR shows it. If the marker is not updated, the
Codex re-review wait ends `incomplete` at `--timeout` and the run continues with Augment (fail
open), so the gap cannot hang the loop.

The S5b decline fallback keeps its "no second re-trigger" rule for both reviewers. The silence
poke stays Augment-only.

## 12. Loop guard, round counter and the re-trigger count

- One remediation cycle covers the findings of **both** reviewers from one round outcome: one fix
  commit, one push, one `round_counter` tick (INV-001 edge unchanged, fired once per cycle when the
  merged S5 outcome is attributed). `max_rounds=N` still means at most N pushes.
- `rereview_request_count` (INV-R1, `<= max_rounds`) now counts **cycles that were re-triggered**,
  not comments: `rebuild_state` folds `rereview_requested` by distinct `cycle_id` (an event with no
  `cycle_id` still counts once each, so old logs rebuild to the same number). Two comments in one
  cycle (Augment + Codex) count once.
- `recovery.resolve_crash_window` keeps its rule (resume at S5a when no `rereview_requested` exists
  for the cycle). At S5a the SKILL posts only for present reviewers that have no
  `rereview_requested{cycle_id, reviewer}` yet (`pending_retriggers(run_log, cycle_id,
  present)`), so a crash between the two posts neither skips Codex nor double-posts Augment.

## 13. Run-log events and state machine naming the reviewer

- Add two `EventType` members (39 → 41): `reviewer_absent` (`{reviewer}`; fail-open, sticky,
  folded into `rebuild_state()["absent_reviewers"]`) and `reviewer_incomplete` (`{reviewer,
  phase: "initial"|"rereview"}`; a present reviewer that did not complete by `--timeout` while the
  other reviewer's result was used).
- Events that concern one reviewer carry a `reviewer` field: `poll_result` (per-reviewer wait
  outcomes), `review_detected`, `findings_normalized`, `finding_verified`, `finding_unverified`,
  `route_decision`, `reply_posted`, `thread_resolved`, `rereview_requested`. Missing `reviewer`
  means `augment` (old logs).
- No new FSM state or edge: the two reviewers are merged **before** the FSM sees an outcome
  (section 6). `state-machine.md` gets a short "reviewers" paragraph saying so, and that
  `TERMINAL_AUGMENT_NO_RESPONSE` means no configured reviewer responded.
- Output contract gains `reviewers`: `{"augment": "present"|"absent"|"incomplete", "codex": ...}`.
  The `status` enum is unchanged.

## 14. Interfaces (new and changed)

All in the pure core (no `gh`/`git` tokens, NFR-6 / T-N50 purity kept).

```python
# pr_submit/detection.py — DetectionContract gains (defaults baked, YAML-overridable):
codex_bot_login: str | None = "chatgpt-codex-connector[bot]"
codex_app_slug: str | None = "chatgpt-codex-connector"
codex_retrigger_phrase: str = "@codex review"
# DetectionContract() direct construction keeps EMPTY identities for both reviewers (fail-safe).

# pr_submit/classifier.py — generalised, Augment behaviour unchanged:
def _thread_findings(threads, contract, completed, identities=None) -> list[dict] | None
def has_reviewer_activity(payload, identities: set[str]) -> bool

# pr_submit/reviewers.py — new
REVIEWERS = ("augment", "codex")
def reviewer_identities(contract, reviewer: str) -> set[str]
def retrigger_phrase(contract, reviewer: str) -> str
def reviewer_activity(payload, contract) -> dict[str, bool]
def parse_codex_priority(body: str) -> str | None            # "P0".."P3" or None
def codex_severity_hint(priority: str | None) -> str | None  # critical/high/medium/low
def codex_review_state(payload, contract, *, watermark=None, current_head_sha=None) -> dict | None
def classify_codex(payload, contract, *, watermark=None, current_head_sha=None) -> str
def codex_finding_comments(payload, contract, *, watermark=None, current_head_sha=None) -> list[dict]
def codex_wait_outcome(state, *, active, elapsed, timeout, silence_timeout, other_settled) -> str
def augment_wait_outcome(state, next_state) -> str
def merge_wait(augment: tuple[str, str], codex: tuple[str, str]) -> dict
#   -> {"outcome": "polling"|"clean"|"findings"|"declined"|"no_response"|"timeout",
#       "used": [...reviewers], "absent": [...], "incomplete": [...]}
def dedup_groups(findings: list[Finding]) -> list[list[Finding]]
def list_review_threads(payload, contract) -> list[dict]     # all bot threads, any state, for reports
def pending_retriggers(run_log_events: list[dict], cycle_id, present: list[str]) -> list[str]

# pr_submit/models.py
Finding.reviewer: str = "augment"
EventType.REVIEWER_ABSENT = "reviewer_absent"; EventType.REVIEWER_INCOMPLETE = "reviewer_incomplete"

# pr_submit/run_log.py — rebuild_state: rereview_request_count by distinct cycle_id;
#   new "absent_reviewers" list folded from reviewer_absent.
```

SKILL snapshot gate (normative, extends the existing block):

```python
aug = existing gate (unchanged)                       # review_state, findings, routes
cx_state = classify_codex(payload, contract, watermark=wm.get("codex"), current_head_sha=expected_head)
cx_roots = codex_finding_comments(...same args...) if cx_state == "findings" else []
# same normalization rule: empty selection or ValueError -> cx_state = "polling"
decision = merge_wait((augment_wait_outcome(review_state, nxt), review_state),
                      (codex_wait_outcome(cx_state, ...), cx_state))
```

## 15. Files changed

| File | Change |
|---|---|
| `src/superclaude/pr_submit/reviewers.py` | new: adapter table, Codex parser/classifier, merge, dedup, thread listing, pending re-triggers |
| `src/superclaude/pr_submit/classifier.py` | identity parameter on `_thread_findings`; `has_reviewer_activity` |
| `src/superclaude/pr_submit/detection.py` | Codex contract fields |
| `src/superclaude/pr_submit/models.py` | `Finding.reviewer`; two event types |
| `src/superclaude/pr_submit/run_log.py` | distinct-cycle re-trigger count; `absent_reviewers` |
| `src/superclaude/pr_submit/severity_router.py` | carry `reviewer` into `Finding` |
| `src/superclaude/pr_submit/__init__.py` | export the new public functions |
| `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` | reviewer-agnostic wording; gate extended; re-trigger per reviewer; output `reviewers` |
| `.../refs/detection-contract.md` | Codex identity, marker and badge contract; YAML fields |
| `.../refs/augment-poll.md` | one snapshot serves both reviewers; per-reviewer wait outcomes and `merge_wait` |
| `.../refs/severity-routing.md` | P0-P3 mapping row; reviewer-neutral wording |
| `.../refs/finding-verify.md`, `troubleshoot-dispatch.md` | wording; dedup groups; seed names reviewer |
| `.../refs/thread-reply.md` | Augment or Codex root id |
| `.../refs/review-retrigger.md` | per-reviewer phrase, watermark, `pending_retriggers` |
| `.../refs/loop-guard.md` | 41 events; distinct-cycle INV-R1 fold; reviewer field |
| `.../refs/state-machine.md` | reviewers merged before the FSM; no-response meaning |
| `.../scripts/reply-resolve-thread.sh`, `retrigger-review.sh`, `poll-augment-review.sh` | header/message wording only (file names kept: tests and installers reference them) |
| `src/superclaude/commands/pr-submit.md` | description and arming text name both reviewers |
| `tests/pr_submit/test_codex_reviews.py` (+ fixtures) | new tests (section 16) |
| `tests/pr_submit/test_run_log.py` | 39 → 41 events |
| `CLAUDE.md`, `docs/user-guide/commands.md`, `docs/guides/tdd-skill-release-guide.md`, `docs/guides/prd-skill-release-guide.md` | where they state Augment-only behaviour |
| `CHANGELOG.md` | Unreleased entry |

No `plugins/superclaude/` twin exists for pr-submit. No installed primitive gains a
`src/superclaude/` path (the refs keep referring to the `superclaude.pr_submit` package).

## 16. Tests

New `tests/pr_submit/test_codex_reviews.py`, fixtures built from the real PR 334/336 shapes:

1. `parse_codex_priority`: P0, P1, P2, P3 → label; no badge, two badges, `P4`, alt/URL mismatch → `None`.
2. Severity mapping: P0/P1 → `--depth deep --fix`, P2 → `--fix`, P3 → report-only, malformed → Medium `--fix`.
3. `codex_review_state` / `classify_codex`: completed clean (PR 334 shape) → `clean`; findings
   (PR 336 shape, unresolved) → `findings` with 3 roots, `reviewer=="codex"`, hint `medium`;
   `running`, wrong head, duplicate summary, malformed JSON, `updated_at` after `observed_at` or not
   newer than watermark → `polling`; resolved threads only + Codex review on head → `clean`.
4. Reviewer detection: `reviewer_activity` and `merge_wait` rows for Augment only, Codex only,
   both, neither (and the pending / incomplete rows).
5. Augment classification unchanged when Codex threads are present in the payload (Codex roots
   never leak into `actionable_finding_comments`).
6. `reply-resolve-thread.sh` on a Codex-rooted thread with a fake `gh` on PATH (the
   `test_cosmos_poll.py` adapter pattern): replies to the root id, then resolves that thread.
7. `dedup_groups`: Augment + Codex on the same path/line → one group of two; different lines →
   two groups; `original_line` used when `line` is null.
8. Run log: 41 event types; `rereview_request_count` counts distinct cycles;
   `absent_reviewers` rebuilt; `pending_retriggers` after a crash between two posts.

Commands (named files only): `uv run pytest tests/pr_submit -q -p no:cacheprovider`,
`uv run pytest tests/skills/test_primitive_dual_surface_lookup.py tests/unit/test_cli_install.py
tests/core/test_how_we_work_routing_table.py -q -p no:cacheprovider`, `make sync-dev`,
`make verify-sync`, `make lint`. Dry check: `poll-augment-review.sh --pr 336 --repo
IronbellyOrg/IronClaude` piped to `list_review_threads` lists the three resolved Codex threads as P2
/ Medium.

## 17. Out of scope, risks and UNVERIFIED items

- **UNVERIFIED**: the summary marker is updated in place after an `@codex review` re-review (only
  "PR opened" reviews were observed). Fail-open covers it (section 11).
- **UNVERIFIED**: P0, P1, P3 badge colours; the parser ignores colour.
- **UNVERIFIED**: Codex posts no decline/size-limit message in a documented format; a usage-limit
  reply is plain activity without completion, so Codex ends `incomplete` (fail open).
- The `codex-review-state:v1` marker is an observed integration format, not a public API (same
  standing as the Cosmos marker); a format change makes Codex `polling` → `incomplete`, never a
  false clean.
- Risk: a Codex connector whose summary comment appears only after Augment has settled is marked
  absent for the run. Observed latency (seconds vs Augment's minutes) makes this unlikely; the
  report names the absent reviewer so the operator can re-run with `--pr <N>`.
- Risk: same path+line findings describing different defects are grouped; mitigated because each
  keeps its own verdict and both bodies go into one diagnosis.
- Out of scope: Codex security review results; reacting to 👍/👀 reactions (not fetched; the
  marker is sufficient).

## 18. Amendments from the plan review (coordinator-approved 2026-10-31)

Source: the pre-execution plan review in
`.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/reflect-pre/adversarial/merged-verdict.yaml`
(finding ids M-NN). Approved by the Orca coordinator on 2026-10-31. These sections override any
earlier text they contradict. Each amendment is pinned by at least one test in `tests/pr_submit/`.

- **A0 (M-05, Task 2 Ruling).** Section 14's Codex contract fields use key-presence semantics in
  `DetectionContract.from_yaml`: an absent `codex_bot_login` / `codex_app_slug` falls back to the
  shipped value, so an override written by contract setup keeps Codex on; an explicit empty or
  null value disables Codex. Direct `DetectionContract()` construction keeps them empty.
- **A1 (M-01, M-03).** Codex completion time is the later of (a) the summary comment's
  `updated_at` and (b) the `submitted_at` of the newest Codex formal review whose commit is the
  expected head, when such a review exists. Both must be parseable aware times no later than
  `observed_at`; the watermark test (strictly newer) uses this later time. `_thread_findings`
  receives it through an explicit keyword `completed_at`, so a Codex root created after the
  marker edit but no later than the review submission is still selected.
- **A2 (M-02, M-09, M-24).** The wait outcomes take the set of reviewers already absent as an
  input: a reviewer in that set, or a reviewer whose identity set is empty, is `absent` at once
  and is never `pending`. When Augment's own silence outcome (`TERMINAL_AUGMENT_NO_RESPONSE`)
  fires while Codex is present, the run records `reviewer_absent{reviewer: "augment"}` and
  continues through `merge_wait` with Codex; it does not stop at that outcome. Only when both
  reviewers are absent does the run end `terminal_augment_no_response`.
- **A3 (M-10).** When several Codex summary comments carry a valid `codex-review-state:v1`
  marker, the one with the latest `updated_at` is used (as Augment uses its latest review); two
  distinct markers with the same latest time are ambiguous and stay `polling`.
- **A4 (M-06, M-07, M-08, M-11).** Each re-trigger POST is recorded as
  `rereview_requested{cycle_id, reviewer, timestamp}` where `timestamp` is the UTC time taken
  right after that reviewer's successful POST. On `--resume` the per-reviewer watermark is the
  `timestamp` of that reviewer's latest `rereview_requested` for the cycle; the resume reuses the
  `cycle_id` of the dangling push record (never a new one); and every resume at S5a or S5 of a
  re-triggered cycle first calls `pending_retriggers` and posts the reviewers still missing.
- **A5 (M-12, M-13, M-14, M-16, M-27).** The SKILL text states explicitly the rules already in
  sections 6, 9, 13 and 5: a dedup group routes at its members' highest remapped tier, is
  diagnosed and fixed once with `fix_applied` recorded for every member's `fix_key`, and every
  verified member's thread is replied to and resolved; the report shows "flagged by"; the S5
  wait covers only the re-triggered reviewers, is attributed when at least one reaches `done`
  on the pushed SHA, and records `reviewer_incomplete{phase: "rereview"}`; S5b fallback
  re-entry includes the merged Codex findings; the nine events of section 13 carry `reviewer`;
  and resume reads `rebuild_state()["absent_reviewers"]`.
- **A6 (PR 337 live run, 2026-10-31).** On PR 337 Augment's review was submitted at 21:22:29Z and
  its only root comment was stamped 21:22:30Z, so the rule "a root created after completion means a
  newer review is still running" polled until `terminal_timeout` (622 s). For root selection the
  completion time of either reviewer is therefore the later of (a) the completion time above
  (Augment: the completed review's `submitted_at`; Codex: A1) and (b) the `createdAt` of the
  reviewer's own roots whose `pullRequestReview` is a completing formal review (same review id, every
  commit equal to that review's commit). For Augment the completing review is the selected latest
  review; for Codex it is each Codex formal review on the expected head. A newer root from any other
  review, or from an older head, still polls. The fix is in `_thread_findings`, shared by both
  reviewers; the attribution rules (submission strictly newer than the watermark, no later than
  `observed_at`) are unchanged. Overrides the "created no later than completion" wording in
  section 7. Pinned by `tests/pr_submit/test_cosmos_review.py::test_a6_*` (verbatim PR 337 snapshot
  `fixtures/cosmos-pr337.json`) and `test_codex_reviews.py::test_a6_*`.
```

## Coverage slice

coverage_schema: uc1-two-pass/1.5.0
spec: .dev/tasks/done/TASK-WF-implementTheDesi-20261031-182028/source.md
spec_delegates_to: .dev/pr-submit-codex/design/pr-submit-codex-design.md (the operative requirement source)
tasklist: .dev/tasks/done/TASK-WF-implementTheDesi-20261031-182028/TASK-WF-implementTheDesi-20261031-182028.md
parsed_count: 12
inferred_count: 8
coverage_pct: 1.0            # parsed-only: 12/12 design sections named by tasks are mapped
coverage_pct_union: 0.8       # 16/20 (parsed 12 + inferred 8; 4 union rows not satisfied by any task)
coverage_undefined: false
coverage_degraded: null       # inferred(8) <= parsed(12), no parsed-sparse guard

rows:
  - id: D-04    source: parsed    req: "design s4 adapter table + reviewer-agnostic path"            task: T6      status: covered
  - id: D-05    source: parsed    req: "design s5 reviewer detection + fail-open absence"            task: T8,T12  status: covered
  - id: D-06    source: parsed    req: "design s6 one-round polling + merge truth table"             task: T7,T8   status: covered
  - id: D-07    source: parsed    req: "design s7 Codex parsing + P0-P3 mapping"                     task: T6,T7   status: covered
  - id: D-08    source: parsed    req: "design s8 re-grade/verify/dispatch reused, wording only"     task: T13     status: covered
  - id: D-09    source: parsed    req: "design s9 cross-reviewer dedup groups"                       task: T9,T13  status: covered
  - id: D-10    source: parsed    req: "design s10 reply/resolve wording"                            task: T11     status: covered
  - id: D-11    source: parsed    req: "design s11 per-reviewer re-trigger + watermark"              task: T12,T14 status: covered
  - id: D-12    source: parsed    req: "design s12 loop guard + distinct-cycle count"                task: T3,T9   status: covered
  - id: D-13    source: parsed    req: "design s13 events name reviewer + output reviewers field"    task: T1,T12  status: covered
  - id: D-14    source: parsed    req: "design s14 interfaces incl. detection contract fields"       task: T2,T6   status: covered
  - id: D-16    source: parsed    req: "design s16 test matrix items 1-8"                            task: T10,T11 status: covered
  - id: INF-001 source: inferred  req: "design s1 non-goals (no security review, no @codex address, no other bots)"   task: Constraints  status: covered (containment: 'do not add behaviour it does not describe')
    quote: "Non-goals: Codex security review results, Codex answering questions or editing the PR, any other review bot."
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:21-22
  - id: INF-002 source: inferred  req: "A0 override key-presence semantics"             task: T2      status: CONTRADICTED (plan AC asserts the reverse)
    quote: "an absent codex_bot_login / codex_app_slug falls back to the shipped value ... an explicit empty or null value disables Codex"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:434-437
  - id: INF-003 source: inferred  req: "A1 completion = later of marker updated_at and completing review submitted_at"   task: none    status: CONTRADICTED (Task 7 pins pre-A1 'completion time = updated_at')
    quote: "Codex completion time is the later of (a) the summary comment's updated_at and (b) the submitted_at of the newest Codex formal review whose commit is the expected head"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:439-443
  - id: INF-004 source: inferred  req: "A3 multiple valid markers: latest updated_at wins; only same-time ties poll"     task: none    status: CONTRADICTED (Task 7 AC pins 'two summary comments -> polling')
    quote: "the one with the latest updated_at is used ... two distinct markers with the same latest time are ambiguous and stay polling"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:452-454
  - id: INF-005 source: inferred  req: "A2 absent-set input; Augment no-response with Codex present records absent and continues"   task: partial (T8 lacks absent-set input; T12 records the event but no AC pins the continue rule)   status: partial
    quote: "a reviewer in that set, or a reviewer whose identity set is empty, is absent at once ... it does not stop at that outcome"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:445-449
  - id: INF-006 source: inferred  req: "A4 per-reviewer POST timestamp watermark; resume reuses dangling cycle_id; pending_retriggers at every resume"   task: T9,T12 (resume cycle_id reuse unstated)   status: covered-partial
    quote: "On --resume the per-reviewer watermark is the timestamp of that reviewer's latest rereview_requested for the cycle; the resume reuses the cycle_id of the dangling push record"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:454-458
  - id: INF-007 source: inferred  req: "A5 SKILL states dedup route/diagnose-once/reply-all/flagged-by/S5-only-retriggered rules"   task: T12 (subset)   status: covered-partial
    quote: "a dedup group routes at its members' highest remapped tier, is diagnosed and fixed once with fix_applied recorded for every member's fix_key"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:459-466
  - id: INF-008 source: inferred  req: "A6 root-selection later-of rule (PR 337 live-run amendment, overrides s7 'created no later than completion')"   task: none    status: UNMAPPED
    quote: "the completion time of either reviewer is therefore the later of (a) the completion time above ... and (b) the createdAt of the reviewer's own roots"
    citation: .dev/pr-submit-codex/design/pr-submit-codex-design.md:467-479

unmapped_requirements: []                      # parsed-only
unmapped_requirements_union:
  - "INF-003 (A1) contradicted by Task 7 text"
  - "INF-004 (A3) contradicted by Task 7 AC"
  - "INF-008 (A6) absent from every task"
  - "INF-005 (A2) partial: augment-absent-continue rule has no AC"
notes: >-
  Section 18 amendments are dated 2026-10-31 (coordinator-approved after this plan was
  generated) and explicitly override earlier design text. The tasklist was never reconciled:
  it encodes the pre-amendment semantics for exactly the three rules the amendments changed
  most (override keys, completion time, multiple markers) and omits A6 entirely. Execution
  caught A0 via a coordinator ruling (progress.md T2 'Ruling' line) and the shipped code
  follows A0/A6, i.e. the plan's defects were corrected by humans mid-run, not by the plan.
