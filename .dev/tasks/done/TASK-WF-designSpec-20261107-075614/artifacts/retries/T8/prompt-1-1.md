68b9da66f0b14bac92cd6226f8ac1429a65c8d99
Review one task for spec compliance.

Task brief: ## Task 8: Write the protocol reference `refs/merge-guard.md`

Depends on: Task 1
Depends on: Task 4
Depends on: Task 7

Create `src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md` from ./source.md sections 3, 4.1, 4.5, 4.6 and 5, as protocol steps (read with `scripts/set-draft-state.sh --read`, decide with `superclaude.pr_submit.merge_guard`, append the `draft_guard_requested` event with fsync before the call, run `scripts/set-draft-state.sh --to`, append `draft_guard_settled`) for: Engage at the end of Wave 3 (L3, only when at least one verified finding of Medium severity or higher is routed to a fix, once per cycle id; review-fix cycles and CI-fix cycles; mints the cycle id with `fix_cycle_id` in the single place named by Task 1 O1 and reuses it as the `cycle_id` of the push triad and of `rereview_requested`; prints the clear command `gh pr ready <N> --repo "$REPO"` once); Pre-push (the script `--read` must show `OPEN` at the pre-push head guard step before `push_decision`, otherwise halt `pr_not_open`, push nothing, report the local commit); Release (after `push_completed`, head equals `target_sha`, or zero-edit proof with this cycle's applied-edit count, before reply, resolve and the S5a re-trigger; one retry; `already in target state` counts as confirmed); Foreign toggle and unreadable timeline handling; Exit report (the `merge_guard` field mapping of `guard_status`, the held-exit list with the clear command, and for the L2 line a pointer to the SKILL.md output table, which carries the literal text; the ref holds no second copy of it); Resume, loaded from Wave 0 at every ordinal and in both modes (`resume_decision` rows, the three `RECONCILE` reasons, the `landed`, `not_landed` and `ambiguous` branch strings, `published` computed with `held_cycle_published` so that a push that completed normally before the crash also releases, and held-guard reporting when the mode is `off` or the ordinal is below 3). Every fenced command line starts with `gh`, `git`, `uv`, `make`, `jq` or a `scripts/` path that exists; every `gh` line is repo-scoped; the text contains no `src/superclaude` string, no python fence and no `file:NNN` pointer. Create `tests/pr_submit/test_merge_guard_protocol.py` with the static checks. As the last step, once the ref text is final, add one `WRITE_VERB_CLASSIFICATION` entry in `tests/skills/test_worker_contract.py` for every line of the ref that matches `gh pr` or `gh api` (exact stripped line, category `never-worker`, the standard pr-submit reason). Run `make sync-dev`.

Acceptance criteria:
- T8.AC1: The ref has a section for each of Engage, Pre-push, Release, Exit report and Resume, states the single place where the guard-enabled cycle id is minted (matching the O1 finding in `./artifacts/pre-build-gate.md`), and the Resume section states that it also runs on `--resume` below ordinal 3 and with `--merge-guard off`.
- T8.AC2: `tests/pr_submit/test_merge_guard_protocol.py` asserts: the ref exists, its fenced commands pass the allowed-program rule, every `gh` line passes the repo-scope check used in `tests/pr_submit/test_static_grep.py`, `scripts/set-draft-state.sh` is a file, and the ref does not contain `src/superclaude`; the test passes under `uv run pytest tests/pr_submit/test_merge_guard_protocol.py -q`.
- T8.AC3: The ref states that engage failure and an unreadable timeline at engage halt with `terminal_halted` reason `draft_guard_unavailable` before any edit, that an exit with unpublished or uncertain work leaves the PR draft and reports `held`, that the Engage section names the Medium-or-higher routed-finding trigger and "once per cycle", and that Resume uses `published` and the recovery branch strings; the protocol test asserts each of these phrases is present.
- T8.AC4: `uv run pytest tests/skills/test_worker_contract.py -q` passes and `make verify-sync` exits 0.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: 68b9da66f0b14bac92cd6226f8ac1429a65c8d99
Diff against the start snapshot: NEW FILE src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md (full contents, 13057 bytes):
# Merge Guard (MG) — hold the PR as a draft while a fix cycle runs (issue #375)

This ref is the protocol for the **merge guard**. At `--monitor 3` a PR that is green but is
about to be remediated is turned into a draft as soon as a verified finding of Medium severity or
higher is routed to a fix, and is marked ready again only when that cycle's fix push is confirmed on
the PR head (or a zero-edit cycle is proven). Every failure, override, crash, resume and exit path
leaves the PR in a known, reported state.

> **NOTE (split of duties, NFR-6).** The deterministic core **DECIDES** and this skill **PERFORMS**,
> the same split as the push triad and the re-trigger. The decisions are the functions of
> `superclaude.pr_submit.merge_guard` (`engage_decision`, `release_decision`, `resume_decision`,
> `classify_toggles`, `guard_status`, `fix_cycle_id`, `next_cycle_number`, `pending_requests`,
> `held_cycle_published`); the folded state is `rebuild_state()["draft_guard"]` of the run log. All
> GitHub I/O is `scripts/set-draft-state.sh`. The guard phases (`engage_pending`, `held`,
> `release_pending`, `released`, `disabled`) are fold values, not `MonitorState` members.

## 1. The five steps of every mutation

Every draft or ready change runs the same five steps, in order:

1. **Read** with the script (live state, head, timeline count).
2. **Decide** with the core function for the moment (Engage, Release or Resume).
3. **Request**: append `draft_guard_requested` to the run log (the append is fsynced) **before** the call.
4. **Mutate** with the script.
5. **Settle**: append `draft_guard_settled` with the outcome.

The script is the only place that talks to GitHub:

```bash
scripts/set-draft-state.sh --pr <N> --repo "$REPO" --read
scripts/set-draft-state.sh --pr <N> --repo "$REPO" --to draft
scripts/set-draft-state.sh --pr <N> --repo "$REPO" --to ready
```

Each call prints one JSON line. `--read` gives `ok`, `state`, `isDraft`, `headRefOid`,
`autoMergeRequest`, `transitions` and `complete`; `--to` gives `ok`, `state`, `isDraft`, `headRefOid`,
`changed` and `error` (`not_open`, `read_failed`, `mutation_failed` or `verify_failed`). It is
idempotent: a PR already in the target state answers `changed: false`, so a retry or a resume re-issue
is safe. Build the `GuardRead` of the core from the `--read` line.

| Event | Fields |
|---|---|
| `draft_guard_requested` | `run_id`, `cycle_id`, `to` (`draft` or `ready`), `idempotency_key`, `timestamp`; the first request of the run also carries `timeline_baseline` (the `transitions` of the read) and `original_is_draft` (the `isDraft` of the read) |
| `draft_guard_settled` | `run_id`, `cycle_id`, `to`, `idempotency_key`, `outcome` (`confirmed`, `failed` or `skipped`), `changed`, `cause`; a skip that has no request also carries `original_is_draft` |

The `idempotency_key` is `guard:<run_id>:<cycle_id>:<to>:a<k>`, where `k` is 1 plus the number of
earlier requests with the same cycle and direction, so a retry is its own request.

## 2. Engage (end of Wave 3, L3 with `--merge-guard draft`)

**Trigger.** Engage runs once per cycle id, at the end of Wave 3, only when at least one verified
finding of Medium severity or higher is routed to a fix: the Medium-or-higher routed-finding trigger.
It applies to a review-fix cycle and to a CI-fix cycle (Wave 8). It never runs for a conflict-merge
cycle (`sync-` and `conflict-` ids) and never below ordinal 3 or with `--merge-guard off`; the core
returns `NOOP` for those, with reason `ordinal`, `mode_off` or `conflict_cycle`.

**Cycle id (the single place it is minted).** This section is the one place where the
guard-enabled cycle id is minted: call `fix_cycle_id(kind, next_cycle_number(<run-log events>, kind))`
once, with kind `fix` for a review-fix cycle and kind `ci` for a CI-fix cycle (ids `fix-<n>` and
`ci-<n>`). Use that id unchanged as the `cycle_id` of `push_decision`, `push_initiated` and
`push_completed`, and of `rereview_requested`, so the guard, the push and the re-trigger of one cycle
share one key. With `--merge-guard off` nothing is minted here and the existing behaviour stands.

**Steps.** Read, then decide with `engage_decision(mode, ordinal, cycle_id, guard, read)` where `guard`
is the folded state. Act on the answer:

| Action | What to do |
|---|---|
| `ENGAGE` | Request `draft` (with `timeline_baseline` and `original_is_draft` on the first request of the run), run `--to draft`, settle `confirmed` (`changed` as printed). The phase is now `held`. Print the clear command once. When the decision notes carry `auto_merge_armed`, add that auto-merge is armed to the report. |
| `SKIP_ALREADY_DRAFT` | The PR was a draft before this run: settle `skipped` with cause `already_draft` (carrying `original_is_draft: true`), never mutate, and keep going. The phase is `disabled` and the report says `off`. |
| `SKIP_USER_OVERRIDE` | Settle `skipped` with cause `user_override`; no more draft calls this run; keep going and report `user_override`. |
| `RETRY_RELEASE` | A release is still pending and the draft is owned: run the Release steps first, then decide again. |
| `HOLD` | Ownership is unproven: do not mutate, keep going and report `unavailable`. |
| `HALT_PR_NOT_OPEN` | Halt `terminal_halted` with reason `pr_not_open`; push nothing. |
| `HALT_UNAVAILABLE` | Halt before any edit: see below. |
| `NOOP` | Nothing to do (already held, disabled or inert). |

**Engage failure.** An engage failure, and an unreadable timeline at engage (reason `read_failed` or
`timeline_unreadable`), halt with `terminal_halted` reason `draft_guard_unavailable` before any edit.
A failed `--to draft` is settled `failed` first. The message names `--merge-guard off` as the way to
run without the guard and prints the clear command. No retry is made at engage.

**The clear command.** Print it once, when the engage settles `confirmed`, and again in every held
report (section 6), with `<N>` and `"$REPO"` filled in:

```bash
gh pr ready <N> --repo "$REPO"
```

## 3. Pre-push (Wave 6, at the pre-push head guard step, before `push_decision`)

Read with the script. The PR must show `OPEN`; otherwise halt `terminal_halted` with reason
`pr_not_open`, push nothing, and report the local commit `<target_sha>` that holds the fixes. This
read applies whatever the guard phase is, including `disabled`, and at every ordinal that reaches the
push. It comes in addition to the head check of the pre-push head guard, never in place of it.

## 4. Release (after `push_completed`, before reply, resolve and the S5a re-trigger)

Release runs after `push_completed` (Wave 6, or Wave 8 for a CI-fix cycle, before the CI re-poll) and
**before** any reply, resolve or re-trigger, so reviewers see a ready PR. Read, then decide with
`release_decision(mode, ordinal, cycle_id, guard, read, applied_edits, target_sha, push_completed)`.
`applied_edits` is this cycle's count of applied edits, not the run-wide field, so a zero-edit cycle
after a fixing cycle still releases with cause `no_edits`.

| Action | What to do |
|---|---|
| `RELEASE` | Request `ready`, run `--to ready`, settle `confirmed` with the decision's cause: `pushed` (head equals `target_sha` after `push_completed`) or `no_edits` (the cycle applied no edit, so there is nothing to publish). |
| `HOLD` | Keep the PR draft and report `held` with the reason (`head_mismatch`, `push_not_completed`, `read_failed` or `timeline_unreadable`) and the clear command; keep going. |
| `SKIP_USER_OVERRIDE` | Settle `skipped` with cause `user_override`; keep pushing and replying; report `user_override`. |
| `HALT_PR_NOT_OPEN` | Halt `terminal_halted` with reason `pr_not_open`; report the local commit. |
| `NOOP` | Nothing is held (or the guard is inert): continue. |

**Release failure.** Retry once: a failed `--to ready` is settled `failed`, then requested again with
the next `:a<k>` key. An answer of `changed: false` (already in the target state) counts as confirmed.
A second failure is settled `failed`, the phase stays `release_pending`, the run keeps going and the
report says `held (release pending)` with the clear command.

## 5. Foreign toggle and unreadable timeline

One login serves the person and the agent, so no actor is used. `classify_toggles(guard, read)` compares
the draft and ready transitions on the PR timeline with the count the guard made itself (plus slack for
calls that failed or were never settled) and returns `ok`, `foreign` or `unreadable`.

- **Foreign** (someone else changed the draft state): settle `skipped` with cause `user_override`, make
  no more draft calls this run, keep pushing, and report `user_override`.
- **Unreadable** (the timeline call failed, the list is incomplete, or events are missing): at engage
  this halts (section 2); at a later checkpoint do not release, report `held (timeline unreadable)`
  with the clear command, and keep pushing.

## 6. Exit report

The output field `merge_guard` is `guard_status(guard, mode, ordinal)`:

| Value | Meaning |
|---|---|
| `off` | The guard did not act: ordinal below 3, `--merge-guard off`, or the PR was already a draft. |
| `released` | The guard acted and the PR is ready again (or the guard never had to act). |
| `held` | The PR is a draft held by this run. Report the reason and the clear command. |
| `user_override` | Someone else changed the draft state; the guard stood down. |
| `unavailable` | The guard could not act or prove ownership (engage failure, ownership unproven). |

Every exit after engage that has no confirmed push and no zero-edit proof leaves the PR draft and
reports `held`, with the reason and the clear command. That covers a validation failure after engage,
a halt before the push, a rejected or failed push, a push whose landing is uncertain, a release that
could not be confirmed, an unreadable timeline and a merged or closed PR. Exits with unpublished or
uncertain work never release the PR.

For a fresh `--monitor 2` run that applies fixes and halts before the push, the final report also
carries the L2 line. Its literal text lives in the output table of `SKILL.md`, which every run loads;
this ref holds no second copy of it.

## 7. Resume (loaded from Wave 0 at every ordinal and in both modes)

Wave 0 loads this section on `--resume` and whenever the run log already holds guard events. It also
runs on `--resume` below ordinal 3 and with `--merge-guard off`, because a held guard from an earlier
run must be reported (and an unsettled request reconciled) before any edit, release or re-trigger.

Gather the inputs, then decide with
`resume_decision(mode, ordinal, guard, read, pending, dangling_branch, published)`:

- `guard`: the folded `draft_guard` state.
- `pending`: `pending_requests(<run-log events>)`, the guard requests with no settle.
- `dangling_branch`: the result of crash recovery for a dangling push: `None`, or one of the strings
  `landed`, `not_landed` or `ambiguous`.
- `published`: `held_cycle_published(<run-log events>, guard)`, true when the held cycle's
  `push_completed` is in the log, written normally or synthesized by recovery. It is the only way
  resume learns that a push completed normally before the crash.
- `read`: a live read with the script, or none when it failed.
- Also pass the held cycle's `target_sha` (from its push record) and this cycle's `applied_edits` as
  the keyword arguments of the same names: row 4 re-enters `release_decision` and needs the head proof.

| Row | Action | What to do |
|---|---|---|
| 1 | `NOOP` | No guard record: nothing to do. |
| 2 | `REPORT_HELD` | Ordinal below 3 or `--merge-guard off`, and the phase is not `released` or `disabled`: no mutation; report `held` with the clear command. |
| 3 | `RECONCILE` | An unsettled request exists. Reason `resume_reconciled`: the live state matches the request and the transition count is the run's plus one, so settle `confirmed` with `changed: true` and cause `resume_reconciled`. Reason `not_applied`: the live state does not match, so settle `skipped` with cause `not_applied`; the phase returns to the one before the request and the next cycle engages normally. Reason `ambiguous`: anything else; hold, report, no mutation. |
| 4 | release | Phase `held` and the push landed (`landed`) or `published` is true: re-enter the Release steps (section 4) with `push_completed` true, then run the S5a logic of `refs/review-retrigger.md`. |
| 5 | `NOOP` | `not_landed` while held: the re-driven push will run, so keep the PR draft (`held_through_redrive`). |
| 6 | `HOLD` | `ambiguous`: the remote tip is unknown, so hold (`ambiguous_remote_tip`). |
| 7 | `RETRY_RELEASE` | A release is pending and the draft is owned: run the Release steps. |
| 8 | `HOLD` | A release is pending, ownership is not proven and the PR is a live draft: hold (`ownership_unproven`). |
| 9 | `NOOP` | Nothing to do. |

Unsettled requests are always reconciled first, so no edit, release or re-trigger runs on an unknown
state. After resume the usual Engage, Pre-push, Release and Exit report steps apply to the cycles that
follow.

NEW FILE tests/pr_submit/test_merge_guard_protocol.py (full contents, 8020 bytes):
"""Static checks for the merge-guard protocol text (issue #375).

Covers ``refs/merge-guard.md`` (and, from the SKILL.md wiring task on, the lines that
load it): its sections, the single place a cycle id is minted, the fenced-command
rules shared with the other refs, and drift guards that tie the names used in the
text to the pure module ``superclaude.pr_submit.merge_guard``.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from superclaude.pr_submit import merge_guard as mg
from tests.pr_submit.test_static_grep import _GH_CMD, _command_lines, _repo_scoped

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-pr-submit-protocol"
REF = SKILL_DIR / "refs" / "merge-guard.md"
ALLOWED_PROGRAMS = frozenset({"git", "gh", "uv", "make", "jq"})


def _text() -> str:
    return REF.read_text(encoding="utf-8")


def _section(heading: str) -> str:
    """The ``## <heading ...>`` section up to the next ``## `` heading, as prose:
    hand-wrapping is not part of the contract, so whitespace is collapsed."""
    text = _text()
    match = re.search(rf"^## [0-9]+\. {re.escape(heading)}.*$", text, re.M)
    assert match, f"no section starting {heading!r}"
    end = re.search(r"^## ", text[match.end() :], re.M)
    body = (
        text[match.start() : match.end() + end.start()]
        if end
        else text[match.start() :]
    )
    return " ".join(body.split())


# --- file and sections ----------------------------------------------------------


def test_the_ref_exists_and_the_script_it_names_is_a_file():
    assert REF.is_file()
    assert (SKILL_DIR / "scripts" / "set-draft-state.sh").is_file()


@pytest.mark.parametrize(
    "heading", ["Engage", "Pre-push", "Release", "Exit report", "Resume"]
)
def test_the_ref_has_a_section_for_each_step(heading):
    assert _section(heading).strip()


def test_the_title_names_the_merge_guard():
    assert "merge guard" in _text().splitlines()[0].lower()


# --- the shared command rules ---------------------------------------------------


def test_fenced_commands_start_with_an_allowed_program_or_an_existing_script():
    lines = [line.strip() for _n, line in _command_lines(REF) if line.strip()]
    assert lines, "the ref has no fenced command"
    for line in lines:
        first = line.split()[0]
        if first.startswith("scripts/"):
            assert (SKILL_DIR / first).is_file(), first
        else:
            assert first in ALLOWED_PROGRAMS, line


def test_every_gh_line_of_the_ref_is_repo_scoped():
    offenders = [
        f"{number}: {line.strip()}"
        for number, line in _command_lines(REF)
        if _GH_CMD.search(line) and not _repo_scoped(line)
    ]
    assert not offenders, offenders


def test_the_ref_carries_no_source_path_python_fence_or_line_pointer():
    text = _text()
    assert "src/superclaude" not in text
    assert "```python" not in text
    assert re.search(r"\.(py|md|sh):[0-9]+", text) is None


def test_the_ref_names_no_force_or_push_form():
    """The script flips the draft flag only; the ref never tells anyone to push."""
    assert re.search(r"\bgit push\b", _text()) is None


# --- the single minting place ---------------------------------------------------


def test_the_cycle_id_is_minted_only_in_the_engage_section():
    text = _text()
    assert text.count("fix_cycle_id(") == 1
    assert "fix_cycle_id(" in _section("Engage")
    engage = _section("Engage")
    assert "single place" in engage
    assert "`fix-<n>`" in engage and "`ci-<n>`" in engage
    for event in (
        "push_decision",
        "push_initiated",
        "push_completed",
        "rereview_requested",
    ):
        assert event in engage, event


# --- the phrases the protocol must state ----------------------------------------


def test_engage_names_the_trigger_and_once_per_cycle():
    engage = _section("Engage")
    assert "Medium-or-higher routed-finding trigger" in engage
    assert "once per cycle" in engage
    assert "verified" in engage


def test_engage_failure_halts_before_any_edit_with_the_pinned_reason():
    engage = _section("Engage")
    assert (
        "`terminal_halted` reason `draft_guard_unavailable` before any edit" in engage
    )
    assert "unreadable timeline at engage" in engage


def test_unpublished_or_uncertain_exits_leave_the_pr_draft_and_report_held():
    report = _section("Exit report")
    assert "leaves the PR draft and reports `held`" in report
    assert "unpublished or uncertain work" in report
    assert "clear command" in report


def test_pre_push_halts_on_a_pr_that_is_not_open():
    pre_push = _section("Pre-push")
    assert "`OPEN`" in pre_push
    assert "`pr_not_open`" in pre_push
    assert "before `push_decision`" in pre_push
    assert "`disabled`" in pre_push


def test_release_runs_after_publication_and_before_reply_resolve_and_retrigger():
    release = _section("Release")
    assert "after `push_completed`" in release
    assert "before any reply, resolve or re-trigger" in release or (
        "before reply, resolve and the S5a re-trigger" in release
    )
    assert "`no_edits`" in release and "`pushed`" in release
    assert "Retry once" in release
    assert "`changed: false`" in release


def test_resume_runs_below_ordinal_3_and_with_the_flag_off_and_uses_published():
    resume = _section("Resume")
    assert (
        "also runs on `--resume` below ordinal 3 and with `--merge-guard off`" in resume
    )
    assert "`published`" in resume
    assert "held_cycle_published" in resume
    for branch in ("`landed`", "`not_landed`", "`ambiguous`"):
        assert branch in resume, branch
    for reason in ("`resume_reconciled`", "`not_applied`", "`ambiguous`"):
        assert reason in resume, reason
    assert "`target_sha`" in resume


def test_the_l2_line_is_not_copied_into_the_ref():
    assert "still mergeable" not in _text()


# --- drift guards against the pure module ---------------------------------------


def test_every_core_function_the_ref_names_exists_in_the_module():
    text = _text()
    names = set(
        re.findall(
            r"\b(engage_decision|release_decision|resume_decision|classify_toggles|"
            r"guard_status|fix_cycle_id|next_cycle_number|pending_requests|"
            r"held_cycle_published|fold_draft_guard)\b",
            text,
        )
    )
    assert names >= {
        "engage_decision",
        "release_decision",
        "resume_decision",
        "classify_toggles",
        "guard_status",
        "fix_cycle_id",
        "next_cycle_number",
        "pending_requests",
        "held_cycle_published",
    }
    for name in names:
        assert callable(getattr(mg, name)), name


def test_every_action_name_in_the_tables_is_a_guard_action():
    members = {member.name for member in mg.GuardAction}
    # `OPEN` is a PR state, the only other upper-case token the ref uses.
    named = set(re.findall(r"`([A-Z][A-Z_]+)`", _text())) - {"OPEN"}
    assert named, "the ref names no action"
    assert named <= members, named - members


def test_every_reason_the_ref_names_is_returned_by_the_module():
    source = Path(mg.__file__).read_text(encoding="utf-8")
    for reason in (
        "mode_off",
        "ordinal",
        "conflict_cycle",
        "pr_not_open",
        "read_failed",
        "timeline_unreadable",
        "head_mismatch",
        "push_not_completed",
        "no_edits",
        "pushed",
        "held_through_redrive",
        "ambiguous_remote_tip",
        "ownership_unproven",
        "resume_reconciled",
        "not_applied",
        "already_draft",
        "user_override",
    ):
        assert f'"{reason}"' in source, reason
        assert f"`{reason}`" in _text() or reason in _text(), reason


def test_the_ref_lists_every_guard_status_value():
    table = _section("Exit report")
    for value in ("off", "released", "held", "user_override", "unavailable"):
        assert f"| `{value}` |" in table, value

diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 17ea43d0..d40562fd 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -1914,6 +1914,14 @@ WRITE_VERB_CLASSIFICATION = {
         "never-worker",
         "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
     ),
+    (
+        "src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md",
+        "gh pr",
+        'gh pr ready <N> --repo "$REPO"',
+    ): (
+        "never-worker",
+        "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
+    ),
     (
         "src/superclaude/skills/sc-reflect-protocol/SKILL.md",
         "git worktree add",

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
