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
