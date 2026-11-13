# Reviewer 3 brief (persona: refactorer)

You are auditing a PLAN (tasklist) against its driving SPEC before any execution (UC-1, pre-execution). You are read-only: no Bash, no edits. Read files from the repository root /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel with Read/Grep/Glob. The plan and spec paths are:
- spec: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md
- plan: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md

Note: the repository already holds a landed implementation of this plan. Do NOT treat the presence of landed code as evidence about the plan; audit the plan text against the spec text. Do not open any path under .dev/tasks/done/ .

Report only defects you can ground with a file:line citation into the plan or spec (quote verbatim, short). A defect is real when an executor following the plan literally would produce a wrong, missing or untestable result, or when plan and spec contradict. Do not pad: zero findings is valid. Keep at most 8 findings.

## T1 card excerpt

Persona focus (refactorer): structure, ordering and ownership. Check task dependencies (every Depends on line), which task edits which file, tasks that edit the same file or test file, the place where classification entries and make sync-dev must run, and any task whose scope is too large or whose order makes a later criterion unsatisfiable (spec section 6 and section 10, Tasks 1, 7 to 13).

## Structural signals

- S_scope: 13 tasks; S_domains: 4 (python core, shell script, protocol prose, docs); S_dev_density (union): 3/40 = 0.075 (matcher misses, see above).
- Recommended rubric result: ESCALATE. Tier 2 is pinned by the caller (`--tier 2`), so the pin decides.
- Grounding note: the repository already contains the landed implementation of this plan (files named by the plan exist). Plan claims were checked against existing symbols (all named tests and constants resolve); no finding relies on the landed code being absent or present.

### Findings of the T1 author relevant to you

1. [0.80] Task 8 builds `refs/merge-guard.md` "from ./source.md sections 3, 4.1, 4.5, 4.6 and 5" and omits section 4.2 (plan line 124). Section 4.2 holds the only definition of the event fields the SKILL must append: `timeline_baseline` and `original_is_draft` on the first request only, `idempotency_key = guard:<run_id>:<cycle_id>:<to>:a<k>`, and what `k` counts (spec lines 182-185). No Task 8 acceptance criterion names any event field (plan lines 126-130). Task 3's fold reads these fields; nothing in the plan makes the protocol write them. A ref without them gives events the fold cannot interpret (no `baseline` makes `classify_toggles` subtract from nothing).
2. [0.70] Task 9 requires the Wave 0 bullet to "carry no L3 or `draft` condition" and its test to fail "when it names an L3 or `draft` condition" (plan lines 137, 140), yet the same task requires the bullet to say that "at L3 with `--merge-guard off`" the unprotected line prints once (plan line 137). The sentence the task requires names L3. The spec has the same tension (source.md line 241). An implementer must guess whether the test forbids the word or a gate.
5. [0.55] Task 10's acceptance criteria never check the cycle-id reuse that spec section 4.6 requires (the id minted at the end of Wave 3 is the `cycle_id` of the push triad and of `rereview_requested`, spec line 251). Task 8 states it in the ref and Task 11 checks the event order, but no protocol-text test pins the reuse in `SKILL.md`.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T03:02:30Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:283-302

```markdown
## 6. Files to change

| File | Kind | Notes |
|---|---|---|
| `src/superclaude/pr_submit/merge_guard.py` | new | section 4.1 |
| `src/superclaude/pr_submit/models.py` | edit | 2 members, docstring and count |
| `src/superclaude/pr_submit/run_log.py` | edit | `rebuild_state` key, append docstring count |
| `src/superclaude/pr_submit/fsm.py` | edit | flag, `SkillArgs`, `parse_args` |
| `src/superclaude/pr_submit/__init__.py` | edit | export the public guard names |
| `src/superclaude/skills/sc-pr-submit-protocol/scripts/set-draft-state.sh` | new | section 4.4 |
| `.../refs/merge-guard.md` | new | section 4.5 |
| `.../SKILL.md`, `.../refs/state-machine.md`, `.../refs/loop-guard.md` | edit | additive only (loop-guard: the 43 to 45 enumeration text) |
| `src/superclaude/commands/pr-submit.md` | edit | flag and section |
| `docs/user-guide/commands.md`, `docs/user-guide/flags.md` | edit | flag and paragraph |
| `tests/pr_submit/test_merge_guard.py`, `test_set_draft_state.py` | new | section 7 |
| `tests/skills/test_worker_contract.py` | edit | one `WRITE_VERB_CLASSIFICATION` entry per new hit line (section 4.7); added last in each task that writes a file with hits |
| `tests/pr_submit/test_run_log.py`, `test_codex_reviews.py`, `test_static_grep.py`, `test_skill_parse.py` | edit | count 43 to 45 at `test_run_log.py:171-175` and `test_codex_reviews.py:441`; `"draft_guard": None` at `test_run_log.py:312`; `merge_guard.py` into the zero-token file set; script lists only after checking each list's purpose; flag default and choices test mirroring `--conflict-max-tier` |

After editing under `src/superclaude/`: `make sync-dev`, then `make verify-sync`. Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because `tests/cli/test_verify_sync_hooks.py` runs `make verify-sync` inside the full suite; the final task also runs `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q`. A repo-wide pin (F12) escaped two reviews because only `tests/pr_submit` was run, so the final task runs the FULL suite (`uv run pytest -q tests`) and compares its failures with the base-commit record. Record `make lint`, `uv run ruff format --check src/ tests/` and the full-suite result (`uv run pytest -q tests`: pass count and every failing test id) on the base commit before the first code edit (pre-existing failures are not this feature's). Never stage `.claude/`. Unchanged and must still pass: `test_idempotency.py:89` (7 sets), the one-python-fence tests, `test_conflict_sync_protocol.py:576` (no `src/superclaude` text in skill or command files).

```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:358-378

```markdown
## 10. Plan authoring notes (for the workflow that builds the plan from this design)

These come from a review of the first plan built from this design; they are requirements on the plan, not on the code.

- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, the test that asserts the event count), never by bare line number: earlier tasks edit the same files and line numbers drift.
- Declare dependencies completely, one `Depends on:` line per dependency: a task depends on every earlier task whose output it imports or consumes (the run-log wiring task and the scenario-test task both need the decision functions; the protocol tasks need the pre-build record).
- The protocol wiring covers the Wave 0 resume and `off` hook as well as Waves 3, 6 and 8 (section 4.5), with a test for each bullet.
- Run `make sync-dev` at the end of each task that edits `src/superclaude/skills/` or `src/superclaude/commands/`, and run the sync-hook tests named in section 6 in the final task.
- The fold, `guard_status`, resume-reason and per-cycle `applied_edits` rules of sections 3 and 4.1 each get an acceptance criterion that a wrong implementation would fail.
- The pre-build record task states the release-gate decision of section 8 and records the base-commit lint result.
- Update the 43-member enumeration in `refs/loop-guard.md` in the event-enum task.
- Protocol prose written by the plan never carries `file:NNN` pointers and never contains the words `evidence-validator` or `conflict-intent.md` on a new SKILL.md line.

Added in v3 (from the review of the second plan):

- Classification entries (section 4.7): the task that writes `scripts/set-draft-state.sh`, the task that writes `refs/merge-guard.md`, the task that edits `src/superclaude/commands/pr-submit.md` and any task that adds a `SKILL.md` line with `gh pr` or `gh api` each ends with adding its `WRITE_VERB_CLASSIFICATION` entries (exact stripped line, category `never-worker`) and runs `uv run pytest tests/skills/test_worker_contract.py -q`. The final task runs the full suite and compares it with the base-commit record.
- The L2 line is written into the SKILL.md output table; its acceptance criterion is a test that the literal line is in `SKILL.md`, and a fresh L2 run must not depend on loading the ref.
- Resume: the plan passes `published` and the recovery branch strings of F13; the crash scenario tests derive branches from a real `RunLog` through `detect_crash_window` and `resolve_crash_window`, never by injecting `"A"`, `"B"` or `"C"`.
- Fold: the plan states that a settled `not_applied` of either direction returns to `phase_before_request` and that a first record erased by it makes the next request a first request again; the acceptance criteria test both directions and the fresh baseline.
- Test hygiene: scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions (pytest would collect them twice); "no push after a `pr_not_open` halt" is asserted on `RunLog.read_events()` (no `push_initiated` or `push_completed` after the halt), because the fake `gh` log cannot see a `git push`; the byte-identical checks for the pinned S5a and Wave 6 pre-push sentences compare against literal string constants taken from the existing pins, not against `git show HEAD:`; the repo-pin proof for the new script is the recorded fake-`gh` argument log plus a static scan inside `test_set_draft_state.py` that every `gh` line carries `--repo` or a `repos/` path (the `test_t105_runtime_repo_pin` test covers only the poll script).
- The Wave 3 and Wave 0 bullet acceptance criteria assert wording and position, not headings: the Wave 3 bullet names the routed-finding trigger and "once per cycle"; the Wave 0 bullet sits before the Wave 1 bullet and has no L3 or `draft` condition.
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:116-157

```markdown
## Phase 3: Protocol text

## Task 8: Write the protocol reference `refs/merge-guard.md`

Depends on: Task 1
Depends on: Task 4
Depends on: Task 7

Create `src/superclaude/skills/sc-pr-submit-protocol/refs/merge-guard.md` from ./source.md sections 3, 4.1, 4.5, 4.6 and 5, as protocol steps (read with `scripts/set-draft-state.sh --read`, decide with `superclaude.pr_submit.merge_guard`, append the `draft_guard_requested` event with fsync before the call, run `scripts/set-draft-state.sh --to`, append `draft_guard_settled`) for: Engage at the end of Wave 3 (L3, only when at least one verified finding of Medium severity or higher is routed to a fix, once per cycle id; review-fix cycles and CI-fix cycles; mints the cycle id with `fix_cycle_id` in the single place named by Task 1 O1 and reuses it as the `cycle_id` of the push triad and of `rereview_requested`; prints the clear command `gh pr ready <N> --repo "$REPO"` once); Pre-push (the script `--read` must show `OPEN` at the pre-push head guard step before `push_decision`, otherwise halt `pr_not_open`, push nothing, report the local commit); Release (after `push_completed`, head equals `target_sha`, or zero-edit proof with this cycle's applied-edit count, before reply, resolve and the S5a re-trigger; one retry; `already in target state` counts as confirmed); Foreign toggle and unreadable timeline handling; Exit report (the `merge_guard` field mapping of `guard_status`, the held-exit list with the clear command, and for the L2 line a pointer to the SKILL.md output table, which carries the literal text; the ref holds no second copy of it); Resume, loaded from Wave 0 at every ordinal and in both modes (`resume_decision` rows, the three `RECONCILE` reasons, the `landed`, `not_landed` and `ambiguous` branch strings, `published` computed with `held_cycle_published` so that a push that completed normally before the crash also releases, and held-guard reporting when the mode is `off` or the ordinal is below 3). Every fenced command line starts with `gh`, `git`, `uv`, `make`, `jq` or a `scripts/` path that exists; every `gh` line is repo-scoped; the text contains no `src/superclaude` string, no python fence and no `file:NNN` pointer. Create `tests/pr_submit/test_merge_guard_protocol.py` with the static checks. As the last step, once the ref text is final, add one `WRITE_VERB_CLASSIFICATION` entry in `tests/skills/test_worker_contract.py` for every line of the ref that matches `gh pr` or `gh api` (exact stripped line, category `never-worker`, the standard pr-submit reason). Run `make sync-dev`.

Acceptance criteria:
- The ref has a section for each of Engage, Pre-push, Release, Exit report and Resume, states the single place where the guard-enabled cycle id is minted (matching the O1 finding in `./artifacts/pre-build-gate.md`), and the Resume section states that it also runs on `--resume` below ordinal 3 and with `--merge-guard off`.
- `tests/pr_submit/test_merge_guard_protocol.py` asserts: the ref exists, its fenced commands pass the allowed-program rule, every `gh` line passes the repo-scope check used in `tests/pr_submit/test_static_grep.py`, `scripts/set-draft-state.sh` is a file, and the ref does not contain `src/superclaude`; the test passes under `uv run pytest tests/pr_submit/test_merge_guard_protocol.py -q`.
- The ref states that engage failure and an unreadable timeline at engage halt with `terminal_halted` reason `draft_guard_unavailable` before any edit, that an exit with unpublished or uncertain work leaves the PR draft and reports `held`, that the Engage section names the Medium-or-higher routed-finding trigger and "once per cycle", and that Resume uses `published` and the recovery branch strings; the protocol test asserts each of these phrases is present.
- `uv run pytest tests/skills/test_worker_contract.py -q` passes and `make verify-sync` exits 0.

## Task 9: Wire the Wave 0 resume and `off` hook, the flag row, the output row and the wave line into `SKILL.md`

Depends on: Task 6
Depends on: Task 8

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` additively, using the pins and line-content rules recorded in `./artifacts/pre-build-gate.md`: one new bullet under Wave 0, written as a flat line before the Wave 1 bullet, that applies at every ordinal and in both modes and carries no L3 or `draft` condition; it states that on `--resume`, or when the run log already holds guard events, the ref `refs/merge-guard.md` (Resume and Exit report) is loaded before Wave 1 and before any edit, release or re-trigger, and that at L3 with `--merge-guard off` the line "Remediation is unprotected: --merge-guard off." is printed once and no draft call is made. Add one `--merge-guard {draft,off}` row to the Required Input flag table beside `--conflict-max-tier`; one row `merge_guard` to the output table (values `off`, `released`, `held`, `user_override`, `unavailable`) that also carries the literal L2 line "PR #N is still mergeable; this run's fixes are local only." so a fresh L2 run prints it without loading the ref; and one line in the wave-structure list. No new python fence. Where a new line would contain `gh pr` or `gh api`, rephrase it (for example "print the clear command from the ref") so that no classification entry is needed; if one is unavoidable, add its `WRITE_VERB_CLASSIFICATION` entry as the last step. Extend `tests/pr_submit/test_merge_guard_protocol.py` with a test for the Wave 0 bullet (it names `--resume`, sits before the Wave 1 bullet, contains no `L3 only` or `draft` gate wording and contains the literal `off` line), one for the flag row, one for the output row including the literal L2 line, and one for the wave-structure line. Run `make sync-dev`.

Acceptance criteria:
- The Wave 0 test fails when the bullet is placed after the Wave 1 bullet, when it names an L3 or `draft` condition, or when the literal `off` line is missing, and passes on the real file.
- A test asserts the literal text "PR #N is still mergeable; this run's fixes are local only." is present in `SKILL.md` itself (not only in the ref), so a fresh L2 run needs no ref load.
- `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_cosmos_protocol.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_merge_guard_protocol.py tests/skills/test_worker_contract.py -q` passes with no edit to any existing test expectation other than those listed in Tasks 2, 5, 7 and 8.
- `SKILL.md` still has exactly one python code fence and no `src/superclaude` string, and the new lines contain neither `evidence-validator` nor `conflict-intent.md`.
- `make verify-sync` exits 0.

## Task 10: Wire the Wave 3, Wave 6 and Wave 8 bullets into `SKILL.md` and the overlay note into `refs/state-machine.md`

Depends on: Task 9

Edit `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` additively: one new bullet under each of Wave 3, Wave 6 and Wave 8 that loads `refs/merge-guard.md` only at L3 with `--merge-guard` `draft`, written as new sentences after, never inside, the pinned sentences. The Wave 3 bullet states that engage happens at the end of Wave 3 only when at least one verified finding of Medium severity or higher is routed to a fix, once per cycle id, and mints the cycle id; the Wave 6 bullet states that Pre-push runs at the pre-push head guard step before `push_decision` and that Release runs after `push_completed` and before reply, resolve and the S5a re-trigger; the Wave 8 bullet states that a CI-fix cycle engages with kind `ci` and releases after `push_completed` before the CI re-poll. The S5a re-trigger sentence and the Wave 6 pre-push sentence stay byte-identical. Edit `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` with a short overlay note that guard phases are folded values, not `MonitorState` members, without the words `gh` or `git` and outside the wait-only sentences pinned for that file. Avoid `gh pr` and `gh api` on new lines (refer to "the clear command from the ref"); add a `WRITE_VERB_CLASSIFICATION` entry as the last step for any new line that cannot avoid them. Extend `tests/pr_submit/test_merge_guard_protocol.py` with one test per bullet (each gated on L3 and `draft`) and one for the overlay note. Run `make sync-dev`.

Acceptance criteria:
- The Wave 3 bullet test asserts the sentence names the Medium-or-higher routed-finding trigger and "once per cycle" and fails when either phrase is deleted (an unconditional "engage at the end of Wave 3" does not pass); the Wave 6 test asserts the Pre-push sentence and the Release-before-reply-resolve-re-trigger order; the Wave 8 test asserts the CI-fix sentence; each test fails when its sentence is removed.
- The S5a re-trigger sentence and the Wave 6 pre-push sentence are asserted byte-identical by comparing the live text with string constants (the literal start text recorded in `./artifacts/pre-build-gate.md`, as the existing pins write them), not with `git show HEAD:`; `SKILL.md` has one python fence and no `src/superclaude` string; no new line contains `evidence-validator` or `conflict-intent.md`.
- `uv run pytest tests/pr_submit -q` and `uv run pytest tests/skills/test_worker_contract.py -q` pass and `make verify-sync` exits 0.

## Phase 4: Scenario tests
```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:175-200

```markdown
## Phase 5: Command and user docs

## Task 12: Document the flag in the command file

Depends on: Task 6
Depends on: Task 8

Edit `src/superclaude/commands/pr-submit.md`, using the pins recorded in `./artifacts/pre-build-gate.md`: add `[--merge-guard {draft,off}]` to the `argument-hint` front matter line (after `--conflict-max-tier`), a row `--merge-guard {draft,off}` with default `draft` in the Options table (effective only at `--monitor 3`; `off` prints "Remediation is unprotected: --merge-guard off."), and a short "Merge guard" section next to "Merge-conflict handling" covering: when the PR becomes a draft, when it becomes ready, the held outcome and the clear command, the unreadable-timeline rule, and that drafts and ready transitions may affect reviewers and workflows (gates G4 and G5 are OPEN and not claimed verified, the PR body states the release gate). The text must not contain `src/superclaude`. Extend `tests/pr_submit/test_merge_guard_protocol.py` with assertions for the flag row, the argument-hint entry and the new section. As the last step, once the command text is final, add one `WRITE_VERB_CLASSIFICATION` entry in `tests/skills/test_worker_contract.py` for every line of the file that newly matches `gh pr` or `gh api` (exact stripped line, category `never-worker`, the standard pr-submit reason). Run `make sync-dev`.

Acceptance criteria:
- `grep -n "merge-guard" src/superclaude/commands/pr-submit.md` shows the argument-hint entry, the Options row and the section heading, and the section states default-on at monitor 3, the exact clear command and that the behaviour is unverified until the owner's disposable-PR run.
- `uv run pytest tests/pr_submit -q` passes, including the command-file checks in `tests/pr_submit/test_conflict_sync_protocol.py`, `uv run pytest tests/skills/test_worker_contract.py -q` passes (every new `gh pr` line classified, none stale), and `make verify-sync` exits 0.

## Task 13: Document the flag in the user guides, sync, and run the final checks

Depends on: Task 2
Depends on: Task 10
Depends on: Task 11
Depends on: Task 12

Edit `docs/user-guide/commands.md`: add `[--merge-guard {draft,off}]` to the `/sc:pr-submit` usage line and a paragraph after the "Merge conflicts" paragraph describing the guard, its default, the `held` state, the clear command `gh pr ready <N> --repo <REPO>` and that draft behaviour is unverified until the owner runs the disposable-PR gate. Edit `docs/user-guide/flags.md`: add a `--merge-guard` row beside the `--conflict-max-tier` row with values `draft` (default) and `off`. Then run `make sync-dev`, `make verify-sync`, `make lint`, `uv run ruff format --check src/ tests/`, the full suite `uv run pytest -q tests`, and `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q`, and write the outputs, the full-suite pass count and every failing test id (compared with the base-commit record of Task 1) to `./artifacts/final-checks.md`.

Acceptance criteria:
- `grep -n "merge-guard" docs/user-guide/commands.md docs/user-guide/flags.md` shows the usage entry, the paragraph and the flags row; the paragraph names the clear command and the unverified-until-release-gate statement.
- `make verify-sync` exits 0, the full suite `uv run pytest -q tests` shows no failing test id that is absent from the base-commit record of Task 1, and `uv run pytest tests/cli/test_verify_sync_hooks.py tests/unit/test_cli_install.py -q` passes; `make lint` and `uv run ruff format --check src/ tests/` exit 0, or every remaining failure is listed in `./artifacts/final-checks.md` as present in the base-commit record of Task 1.
- `git status --short` lists changes only under `src/superclaude/`, `tests/`, `docs/user-guide/`, `.dev/` and gitignored `.claude/` mirrors; no `.claude/` path other than `.claude/settings.json` is staged, and `.dev/tasks` is staged with `git add .dev/tasks`.
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-018 ref loaded at waves 3,6,8 | T8 | covered | plan:124 |
| INF-019 wave 0 bullet | T9 | covered | plan:137 |
| INF-022 state-machine overlay | T10 | covered | plan:150 |
| INF-023 pr-submit.md | T12 | covered | plan:182 |
| INF-024 user guide | T13 | covered | plan:195 |
| INF-027 classification entries | T7,T8,T9,T10,T12 | covered | plan:22 |
| INF-029,039 final suite | T13 | covered | plan:195 |
