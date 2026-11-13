# Reviewer 3 brief (refactorer), UC-1 pre-execution reflection, Tier 2

You are reviewer 3 of 3. You are read-only: you may Read, Grep and Glob; you must not edit, write, move or delete anything, and you run no shell commands. Return one reviewer card as your reply (the orchestrator saves it). Audit the plan against its spec using only the evidence below and what you can Read.

Persona: refactorer. Look at structure: task ordering and declared dependencies, files edited by several tasks, repository pins (tests that fail when text or counts change), import and layering problems, work that lands in the wrong task.

Rules for evidence:
- Plan under review: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`. Spec it implements: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`. Cite plan and spec lines with role plan or spec and that repo-relative path.
- The spec says it read the repository at master `e8db2fe66`. The plan was executed afterwards, so the live checkout (HEAD) now holds the finished implementation and is NOT the code the plan was written against. Read repository facts from the base-commit copy under `.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/` (same layout as the repository). Do not cite HEAD code as a defect of the plan; a claim that is true only at HEAD is later change, not a plan defect. Put code evidence in the claim text as `path:line` of the base copy; citations objects point only at the plan or spec.
- The code graph index describes HEAD, not the base commit: do not use it for base-commit facts.
- Do not read anything under `.dev/tasks/` and do not read other reflect or eval run directories; they hold the execution history, not the evidence.
- Report a defect only when you can show it from a cited line. If a plan line is wrong, say what it should say. A zero-finding card is valid when you state which rows you verified.
- Mark severity MAJOR or CRITICAL only when an implementer following the plan would produce a wrong outcome or the plan cannot be carried out; otherwise MINOR.

## T1 card excerpt

## Facts verified at the base commit (all hold)

- F1 enum has exactly 43 members: `models.py:3` and `models.py:24` say "43", `run_log.py:117` says "43 closed".
- F2 `_NEW_KEY_DEFAULTS` at `tests/pr_submit/test_run_log.py:312`, exact key-set asserts at lines 403-404.
- F3/F13 `recovery.py:40-42` holds `BRANCH_A_LANDED = "landed"`, `BRANCH_B_NOT_LANDED = "not_landed"`, `BRANCH_C_AMBIGUOUS = "ambiguous"`; `recovery.py:37` imports `RunLog`.
- F4 `conflicts.py:46` `CONFLICT_CYCLE_PREFIXES = ("sync-", "conflict-")`, `conflicts.py:1242` `is_conflict_cycle`.
- F5 `fsm.py:104` is the one enum flag; `SkillArgs` at `fsm.py:54`.
- F6/F7/F12 pins: `CORE_PURE_FILES` (`test_static_grep.py:37`), `_RESOLUTION_SCRIPTS` (`test_static_grep.py:479`), `WRITE_VERB_RE` and `WRITE_VERB_CLASSIFICATION` (`tests/skills/test_worker_contract.py:1098`, `:1166`).
- No import cycle: `run_log` would import `merge_guard`, which imports only `conflicts`; `conflicts` imports `fsm` and `models`; `fsm` imports `loop_guard`, `models`, `severity_router`. None of them imports `run_log` or `recovery`.
- `tests/pr_submit/__init__.py` exists, so Task 11 importing a helper from another test module resolves.

## Risk surface

- Tests outside `tests/pr_submit` and `tests/skills/test_worker_contract.py` run only in Task 13 (spec line 301 says a repo-wide pin escaped two earlier reviews). A late failure there would force an edit to a file whose classification entries are already written, and a later edit of a classified line makes the entry stale.
- Release-gate items G1 (live part), G2 (live part), G4, G5, G6 are explicitly recorded OPEN (plan line 24, spec lines 326-335); the plan does not claim them verified.
- Dependency lines: Task 6 depends only on Task 1 though Task 9 (flag row) needs it, which is satisfied transitively through Task 9.

## Recommendations

1. Add to Task 4 the inputs `release_decision` needs when `resume_decision` row 4 re-enters it (state where `cycle_id`, `applied_edits` and `target_sha` come from) and an acceptance case that fails when `target_sha` is taken from the live read.
2. Rewrite the Wave 0 acceptance in Task 9 so the test checks position and the literal `off` line, and separates "applies at every ordinal" from the `off` print condition.
3. Make Task 2's `grep` criterion name the files and the exact strings that must be gone (`exactly 43`, `43 closed`, `The 43 event types`).
4. In Tasks 7, 8 and 12 say "every line that `WRITE_VERB_RE` matches", not only `gh pr` and `gh api`.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T05:18:25Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:17-27

(plan Constraints)

`````markdown
## Constraints

- Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
`````

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:29-33

(Phase 1 and Task 1 heading)

`````markdown
## Phase 1: Contracts and pure core

## Task 1: Write the pre-build record `./artifacts/pre-build-gate.md`

Create `./artifacts/pre-build-gate.md` in this package from ./source.md sections 6, 8 and 10. First record the base-commit state: run `make lint`, `uv run ruff format --check src/ tests/` and the full suite `uv run pytest -q tests` before any code edit and write each exit code, the pass count and every failing test id (or "clean") into the file, so later failures can be told apart from this feature's. Then record the release-gate decision of ./source.md section 8 in the owner's words: the build proceeds with no GitHub calls (fake `gh` in tests); gates G1 (live part), G2 (live part), G4, G5 and G6 are a release gate that the owner runs on a disposable fork PR before the feature is merged or turned on by default; the user guide states that draft behaviour is unverified until then; the PR body states the gate plainly; the run that opens the PR must pass `--merge-guard off`. Then close the open items by reading the code: O1, where `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` (Wave 3 to Wave 6 and Wave 8 text) and `refs/loop-guard.md` assign a fix or CI cycle's `cycle_id` today and whether any test under `tests/pr_submit/` pins a value; O2, how scripts are granted and invoked in the SKILL front matter and what `test_allowed_tools_cover_every_program` in `tests/pr_submit/test_conflict_sync_protocol.py` and the `_RESOLUTION_SCRIPTS` tests in `tests/pr_submit/test_static_grep.py` require of a new script; O3, every exact-text pin and line-content rule (for example `test_intent_and_validator_lines_say_tier_2`, `test_skill_forbids_force_push`, the wait-only sentences pinned for `refs/state-machine.md`, and the `WRITE_VERB_CLASSIFICATION` table with its stale-entry test in `tests/skills/test_worker_contract.py`) on `SKILL.md`, `refs/state-machine.md`, `refs/loop-guard.md` and `src/superclaude/commands/pr-submit.md` that the later additive edits must avoid; O4, that the S5a re-trigger sentence in `SKILL.md` stays unchanged and where the new release sentence goes relative to it; and the literal start text of the S5a sentence and of the Wave 6 pre-push sentence as the existing pins write them, so later tests can compare against string constants.
`````

### .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/src/superclaude/pr_submit/conflicts.py:25-36

(base commit e8db2fe66)

```python
import base64
import re
from dataclasses import dataclass

try:
    import tomllib
except ImportError:  # Python 3.10: no TOML parser; lock_trust_findings fails closed
    tomllib = None

from .fsm import run_validation_gates
from .models import MonitorState

```

### .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/src/superclaude/pr_submit/fsm.py:100-112

(base commit e8db2fe66)

```python
    parser.add_argument("--output-dir", dest="output_dir", default=None)
    parser.add_argument("--resume", default=None)
    parser.add_argument("--pr", type=int, default=None)
    parser.add_argument(
        "--conflict-max-tier",
        dest="conflict_max_tier",
        type=int,
        choices=[0, 1, 2],
        default=DEFAULT_CONFLICT_MAX_TIER,
    )
    return parser


```

### .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/tests/pr_submit/test_static_grep.py:37-52

(base commit e8db2fe66)

```python
CORE_PURE_FILES = [
    SKILL_DIR / "refs" / "state-machine.md",
    SKILL_DIR / "refs" / "severity-routing.md",
    SKILL_DIR / "refs" / "loop-guard.md",
    # V1.1: the auggie-fallback ref carries NO gh token (it documents the
    # `> Skill sc:auggie-review-protocol` invocation + a flag table, not a gh api call),
    # so it joins the zero-token set. The gh-BEARING review-retrigger.md + retrigger-review.sh
    # are DELIBERATELY excluded (covered by the T-1101 fork-pin test instead) —
    # mirroring how thread-reply.md / augment-poll.md are excluded for the same reason.
    SKILL_DIR / "refs" / "auggie-fallback.md",
    PR_SUBMIT_PKG / "fsm.py",
    PR_SUBMIT_PKG / "severity_router.py",
    PR_SUBMIT_PKG / "loop_guard.py",
    PR_SUBMIT_PKG / "ci.py",
    # issue #305: the conflict core is pure (no version-control tokens)
    PR_SUBMIT_PKG / "conflicts.py",
```

### .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/tests/pr_submit/test_conflict_sync_protocol.py:587-610

(base commit e8db2fe66)

```python
def test_allowed_tools_cover_every_program():
    """Every `MECHANICAL_RULES` argv[0] and the first word of every fenced command
    line in the two refs is git, gh, uv, make, jq or a `scripts/` path, and each of
    those programs is granted as `Bash(<prog> *)` in the SKILL front matter."""
    front = _read(SKILL_MD).split("\n---\n", 1)[0]
    tools_line = next(
        line for line in front.splitlines() if line.startswith("allowed-tools:")
    )
    granted = set(re.findall(r"Bash\((\S+) \*\)", tools_line))
    programs = set()
    for rule in MECHANICAL_RULES:
        programs.add(rule.regenerate[0])
        if rule.check:
            programs.add(rule.check[0])
    scripts = set()
    for path in NEW_REFS:
        for word in _fenced_first_words(path):
            if word.startswith("scripts/"):
                scripts.add(word)
            else:
                programs.add(word)
    assert programs <= ALLOWED_PROGRAMS, programs - ALLOWED_PROGRAMS
    assert programs <= granted, programs - granted
    for script in scripts:
```

### .dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r3/artifacts/base-e8db2fe6/src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh:1-52

(base commit e8db2fe66; the model for the new script)

```bash
#!/usr/bin/env bash
#
# retrigger-review.sh — S5a re-trigger wrapper for sc:pr-submit (R1 / FR-8).
#
# Purpose : Post one re-trigger comment on the PR's conversation thread so a
#           reviewer re-reviews the just-pushed remediation commit: `auggie review`
#           (the default) for Augment, `--body "@codex review"` for Codex. The SKILL
#           calls this once per present reviewer. A push does NOT auto-trigger a
#           re-review by either bot; each reviews only on PR-open or an explicit
#           trigger comment.
# Usage   : retrigger-review.sh --pr <N> [--repo <owner/repo>] [--body <phrase>]
# Exit    : 0 on a completed post; 2 on usage error (bad/missing/non-numeric --pr);
#           127 on a missing dependency (gh not on PATH — an environment failure, NOT
#           CLI misuse); 1 on a failed post.
# Spec    : merged-spec-v1.1-addendum.md FR-8 / INV-R1; refs/review-retrigger.md.
#           All gh I/O is isolated here (NFR-6). The gh api path pins the RESOLVED
#           repos/${REPO}/... (origin's owner/repo, never the upstream parent).
#
# Source of truth lives in src/superclaude/; do not edit the .claude/ mirror.

set -euo pipefail

die() { printf 'retrigger-review: %s\n' "$1" >&2; exit "${2:-1}"; }

PR=""
REPO=""
BODY="auggie review"
while [ $# -gt 0 ]; do
    case "$1" in
        --pr) [ $# -ge 2 ] || die "missing value for --pr <N>" 2; PR="$2"; shift 2 ;;
        --repo) [ $# -ge 2 ] || die "missing value for --repo <owner/repo>" 2; REPO="$2"; shift 2 ;;
        --body) [ $# -ge 2 ] || die "missing value for --body <phrase>" 2; BODY="$2"; shift 2 ;;
        *) die "unknown argument: $1" 2 ;;
    esac
done

[ -n "$PR" ] || die "missing required --pr <N>" 2
[ -n "$BODY" ] || die "empty --body is not allowed" 2
# Require a numeric PR — a stringified None/empty/garbage would otherwise build a
# malformed ``issues/<PR>/comments`` target (e.g. .../issues/None/comments → 404).
case "$PR" in ''|*[!0-9]*) die "invalid --pr value (must be a positive integer): $PR" 2 ;; esac
# Missing gh is an ENVIRONMENT failure, not CLI misuse — exit 127 (command-not-found),
# distinct from the usage-error exit 2 above.
command -v gh >/dev/null 2>&1 || die "gh CLI not found on PATH" 127

# Resolve the target repo (owner/repo). The SKILL normally passes --repo; absent it,
# resolve from the current checkout (the origin remote, then gh repo view). The
# issue-comment POST target is COMPUTED — never a literal owner/repo (de-hardcoded).
REPO="${REPO:-$(git remote get-url origin 2>/dev/null | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##' || true)}"
[ -n "$REPO" ] || REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)"
[ -n "$REPO" ] || die "could not resolve target repo (pass --repo <owner/repo>)" 2

```

### .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:dependency-lines

(Task headings and every `Depends on:` line of the plan, as `plan line: text`)

```text
31: ## Task 1: Write the pre-build record `./artifacts/pre-build-gate.md`
40: ## Task 2: Add the two guard events to the closed event enum and the enumeration texts
42: Depends on: Task 1
52: ## Task 3: Create `merge_guard.py` types, cycle ids, fold, pending matcher, published check and status mapping
54: Depends on: Task 2
66: ## Task 4: Add the toggle classifier and the three decision functions
68: Depends on: Task 3
80: ## Task 5: Fold the guard into the run log and export the public names
82: Depends on: Task 3
83: Depends on: Task 4
94: ## Task 6: Add the `--merge-guard` flag
96: Depends on: Task 1
104: ## Task 7: Create the GitHub I/O script `set-draft-state.sh`
106: Depends on: Task 1
118: ## Task 8: Write the protocol reference `refs/merge-guard.md`
120: Depends on: Task 1
121: Depends on: Task 4
122: Depends on: Task 7
132: ## Task 9: Wire the Wave 0 resume and `off` hook, the flag row, the output row and the wave line into `SKILL.md`
134: Depends on: Task 6
135: Depends on: Task 8
146: ## Task 10: Wire the Wave 3, Wave 6 and Wave 8 bullets into `SKILL.md` and the overlay note into `refs/state-machine.md`
148: Depends on: Task 9
159: ## Task 11: Write the scenario tests over the run log
161: Depends on: Task 3
162: Depends on: Task 4
163: Depends on: Task 5
164: Depends on: Task 7
177: ## Task 12: Document the flag in the command file
179: Depends on: Task 6
180: Depends on: Task 8
188: ## Task 13: Document the flag in the user guides, sync, and run the final checks
190: Depends on: Task 2
191: Depends on: Task 10
192: Depends on: Task 11
193: Depends on: Task 12
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-004: No new `MonitorState`. | Task 10 | covered | source.md:51 |
| INF-005: No `gh` or `git` word on any line, comments included (F6). | Constraints | covered | source.md:75 |
| INF-011: Add to `EventType` in `models.py` (43 to 45 | Task 2 | covered | source.md:175 |
| INF-015: `DEFAULT_MERGE_GUARD = "draft"` | Task 6 | covered | source.md:214 |
| INF-017: Modelled on `scripts/retrigger-review.sh` | Task 7 | covered | source.md:221 |
| INF-020: Loaded lazily at L3 Wave 3, Wave 6 and Wave 8. | Task 8 | covered | source.md:240 |
| INF-022: update it to 45 and name `draft_guard_requested` and `draft_guard_settled` | Task 2 | covered | source.md:242 |
| INF-031: Cite tests and constants by symbol name | Constraints | covered | source.md:362 |
| INF-032: Declare dependencies completely, one `Depends on:` line per dependency | none | unmapped (containment 0.33) | source.md:363 |
| INF-033: scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions | Task 11 | covered | source.md:377 |
