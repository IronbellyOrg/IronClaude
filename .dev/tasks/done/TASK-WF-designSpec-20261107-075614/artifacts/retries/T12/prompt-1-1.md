3b6516e58c42203874a29e16489922f0e0f543bb
Review one task for spec compliance.

Task brief: ## Task 12: Document the flag in the command file

Depends on: Task 6
Depends on: Task 8

Edit `src/superclaude/commands/pr-submit.md`, using the pins recorded in `./artifacts/pre-build-gate.md`: add `[--merge-guard {draft,off}]` to the `argument-hint` front matter line (after `--conflict-max-tier`), a row `--merge-guard {draft,off}` with default `draft` in the Options table (effective only at `--monitor 3`; `off` prints "Remediation is unprotected: --merge-guard off."), and a short "Merge guard" section next to "Merge-conflict handling" covering: when the PR becomes a draft, when it becomes ready, the held outcome and the clear command, the unreadable-timeline rule, and that drafts and ready transitions may affect reviewers and workflows (gates G4 and G5 are OPEN and not claimed verified, the PR body states the release gate). The text must not contain `src/superclaude`. Extend `tests/pr_submit/test_merge_guard_protocol.py` with assertions for the flag row, the argument-hint entry and the new section. As the last step, once the command text is final, add one `WRITE_VERB_CLASSIFICATION` entry in `tests/skills/test_worker_contract.py` for every line of the file that newly matches `gh pr` or `gh api` (exact stripped line, category `never-worker`, the standard pr-submit reason). Run `make sync-dev`.

Acceptance criteria:
- T12.AC1: `grep -n "merge-guard" src/superclaude/commands/pr-submit.md` shows the argument-hint entry, the Options row and the section heading, and the section states default-on at monitor 3, the exact clear command and that the behaviour is unverified until the owner's disposable-PR run.
- T12.AC2: `uv run pytest tests/pr_submit -q` passes, including the command-file checks in `tests/pr_submit/test_conflict_sync_protocol.py`, `uv run pytest tests/skills/test_worker_contract.py -q` passes (every new `gh pr` line classified, none stale), and `make verify-sync` exits 0.
Global constraints: - Edit canonical files under `src/superclaude/` only, then run `make sync-dev`; do not stage `.claude/` mirror files. Use UV for every Python command (`uv run pytest ...`, `uv run ruff ...`).
- The new pure module `src/superclaude/pr_submit/merge_guard.py` and every file already listed in `CORE_PURE_FILES` of `tests/pr_submit/test_static_grep.py` (including `refs/state-machine.md` and `refs/loop-guard.md`) must contain no whole word `gh` or `git` on any line, comments included. The module must not import `recovery` (an import cycle through `run_log`).
- Protocol and command text must not contain the string `src/superclaude`; `SKILL.md` must keep exactly one python code fence; edits to `SKILL.md` and `refs/state-machine.md` are additive sentences, bullets and rows placed after, never inside, the sentences pinned by `tests/pr_submit/test_static_grep.py` and `tests/pr_submit/test_conflict_sync_protocol.py`. A new `SKILL.md` line must not name `evidence-validator` or `conflict-intent.md` (a line-content test allows those words only on lines that also say "Tier 2") and must not use wording that the forbidden-force-push line test rejects; Task 1 lists the exact line-content rules before any edit.
- Every new line under `src/superclaude/skills/`, `src/superclaude/commands/` or `src/superclaude/agents/` that contains `gh pr`, `gh api` or a git write verb needs one entry in `WRITE_VERB_CLASSIFICATION` in `tests/skills/test_worker_contract.py` (key: repo-relative path, verb text, exact stripped line; category `never-worker` with the standard pr-submit reason text of the neighbouring entries). Add each entry last in the task that writes the file, because editing a classified line later makes the entry stale and fails `test_classification_table_has_no_stale_entries`; run `uv run pytest tests/skills/test_worker_contract.py -q` in that task.
- Cite tests and constants by symbol name (for example `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`, `CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`), never by line number, in plan text, task artifacts and the protocol prose this plan produces. Protocol prose carries no `file:NNN` pointers.
- No test or task may call GitHub. Script tests use a fake `gh` executable on `PATH`. The behaviour that needs a disposable fork PR (gates G1 live part, G2 live part, G4, G5 and G6 of ./source.md section 8) is recorded as OPEN and is a release gate, never claimed verified.
- Scope limits (non-goals of ./source.md): no labels, commit statuses or rulesets; ordinals 0 to 2 change only by one report line; conflict-merge cycles (Tier 1 and Tier 2) are never engaged; the guard is not held through re-review or CI; a second concurrent run on the same PR is unsupported.
- Owner decisions already accepted (listed in the ./source.md header and section 8) are fixed: draft not label; engage at the end of Wave 3; default on at `--monitor 3`; release on the confirmed push before replies and the re-trigger; unreadable timeline or unpublished exit keeps the PR draft; build now with no GitHub calls, release gate for G4 and G5.
- Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/`, because the full test suite runs `make verify-sync` through `tests/cli/test_verify_sync_hooks.py`.
Start sha: 3b6516e58c42203874a29e16489922f0e0f543bb
Diff against the start snapshot: diff --git a/src/superclaude/commands/pr-submit.md b/src/superclaude/commands/pr-submit.md
index 6427aa49..4ec996b2 100644
--- a/src/superclaude/commands/pr-submit.md
+++ b/src/superclaude/commands/pr-submit.md
@@ -5,7 +5,7 @@ category: quality
 complexity: advanced
 mcp-servers: [auggie]
 personas: [analyzer, architect, security, qa, devops]
-argument-hint: "[--monitor {0,1,2,3}] [--max-rounds N≤5] [--poll-interval ≥30] [--timeout 600] [--silence-timeout 300] [--base <branch>] [--head <branch>] [--title ...] [--body ...] [--pr <N>] [--conflict-max-tier {0,1,2}] [--output-dir <dir>] [--resume <run-log.jsonl>]"
+argument-hint: "[--monitor {0,1,2,3}] [--max-rounds N≤5] [--poll-interval ≥30] [--timeout 600] [--silence-timeout 300] [--base <branch>] [--head <branch>] [--title ...] [--body ...] [--pr <N>] [--conflict-max-tier {0,1,2}] [--merge-guard {draft,off}] [--output-dir <dir>] [--resume <run-log.jsonl>]"
 version: "1.0"
 ---
 
@@ -52,6 +52,7 @@ Explicit only — two activation paths:
 | `--head <branch>` | — | PR head branch. |
 | `--pr <N>` | — | Attach to an existing PR instead of opening one. |
 | `--conflict-max-tier {0,1,2}` | 0 | Highest merge-conflict tier to act on: 0 (default) detect and report only; 1 also regenerate a conflicted root `uv.lock` (Tier 1, opt-in because `uv lock` can run the PR's build code); 2 also resolve text conflicts by stated intent (Tier 2, off by default). Tier 3 always halts at L3. Tier 1 halts before `uv lock` when the merged `pyproject.toml` declares `build-system.backend-path`, a non-empty `project.dynamic`, or a path or editable `[tool.uv.sources]` entry. Conflict resolution and validation run the project's build and test code, so run pr-submit only on PRs from collaborators you trust with your credentials. |
+| `--merge-guard {draft,off}` | draft | Effective only at `--monitor 3`. `draft` holds the PR as a draft while a fix cycle runs and marks it ready again once the fix push is confirmed (see "Merge guard"); `off` leaves the PR untouched and prints "Remediation is unprotected: --merge-guard off." once. |
 | `--title` / `--body` | — | PR title / body. |
 | `--output-dir <dir>` | `.dev/pr-monitor/pr-<N>-<ts>/` | Run-log + artifacts dir. |
 | `--resume <jsonl>` | — | Reconstruct state from a write-ahead run-log. |
@@ -77,6 +78,21 @@ After a merge push, CI is checked against the new head. Expected checks that hav
 
 The protocol's `refs/conflict-mechanical.md` owns detection, validation and recovery; `refs/conflict-intent.md` adds Tier 2 judgment and evidence requirements. Load them through the protocol, not as a replacement for its mandatory activation.
 
+## Merge guard (`--merge-guard`)
+
+`--merge-guard {draft,off}` is on by default (`draft`) and acts only at `--monitor 3`. Below that, and with `off`, the skill makes no draft or ready change. A run at `--monitor 2` that applies fixes and halts before the push reports that the PR is still mergeable and the fixes are local only.
+
+- **When the PR becomes a draft:** at the end of Wave 3, when at least one verified finding of Medium severity or higher is routed to a fix, once per fix cycle (a CI-fix cycle counts as its own cycle). The PR becomes a draft before any edit, so nobody merges it while the fix exists only locally. A PR that was already a draft is left alone and this run never makes it ready.
+- **When it becomes ready:** only after the cycle's fix push is confirmed on the PR head (or a cycle that applied no edit is proven), and before any reply, resolve or re-trigger comment, so the reviewers see a ready PR.
+- **Held outcome:** an exit with unpublished or uncertain work (a validation failure, a halt before the push, a rejected or failed push, a push whose landing is unknown, a release that could not be confirmed, a PR that was merged or closed) leaves the PR a draft. The output then reports `merge_guard: held` with the reason and the clear command, which marks the PR ready by hand once you have checked it:
+
+```text
+gh pr ready <N> --repo "$REPO"
+```
+
+- **Unreadable timeline:** the guard decides from the PR's draft and ready history. If that history cannot be read, the guard never marks the PR ready: at the start of a cycle the run halts with reason `draft_guard_unavailable` before any edit, and at a later checkpoint it keeps the PR a draft and reports `held`. If someone else changes the draft state, the guard stands down and reports `user_override`.
+- **Effects on reviewers and workflows:** drafts and ready transitions may change which reviews and workflows run. Whether the Augment and Codex reviews and the CI workflows behave as expected on a draft or on a ready transition (release gates G4 and G5 of the design) is unverified until the owner's run on a disposable PR; do not rely on it, and the PR body states this release gate. Pass `--merge-guard off` to run without the guard.
+
 ## Behavioral Flow
 
 This command does ONLY parse + environment-validate + handoff. It parses the flags, verifies the PR target is the resolved origin repo (origin's `owner/repo`, never an upstream parent the host's CLI might default to), and hands off to the protocol skill via the Activation section below. The full behavioral specification — the FSM, the detection contract, severity routing, verify-before-remediate, troubleshoot dispatch, validation gates, the push triad, reply/resolve, and the loop guard — lives in the skill.
@@ -92,7 +108,7 @@ This command does ONLY parse + environment-validate + handoff. It parses the fla
 
 Pass the following context:
 
-- `--monitor` ordinal (0/1/2/3) and `--max-rounds` / `--poll-interval` / `--timeout` / `--silence-timeout` / `--conflict-max-tier`.
+- `--monitor` ordinal (0/1/2/3) and `--max-rounds` / `--poll-interval` / `--timeout` / `--silence-timeout` / `--conflict-max-tier` / `--merge-guard`.
 - PR context: `--base` / `--head` / `--title` / `--body`, or the existing PR number (`--pr <N>`).
 - `--output-dir` and `--resume` if supplied.
 

diff --git a/tests/pr_submit/test_merge_guard_protocol.py b/tests/pr_submit/test_merge_guard_protocol.py
index f4d4c553..8e80f8e1 100644
--- a/tests/pr_submit/test_merge_guard_protocol.py
+++ b/tests/pr_submit/test_merge_guard_protocol.py
@@ -681,3 +681,80 @@ def test_the_state_machine_overlay_says_guard_phases_are_folded_values():
         assert f"`{phase.name}`" in prose, phase
         assert phase.name not in MonitorState.__members__
     assert re.search(r"\bgh\b|\bgit\b", note) is None
+
+
+# --- the command file (argument hint, Options row, "Merge guard" section) ---------
+
+COMMAND = REPO_ROOT / "src" / "superclaude" / "commands" / "pr-submit.md"
+CLEAR_COMMAND = 'gh pr ready <N> --repo "$REPO"'
+
+
+def _command() -> str:
+    return COMMAND.read_text(encoding="utf-8")
+
+
+def _command_section() -> str:
+    text = _command()
+    start = text.index("## Merge guard")
+    return " ".join(text[start : text.index("\n## ", start + 1)].split())
+
+
+def test_the_command_argument_hint_names_the_flag_after_the_conflict_flag():
+    hint = next(
+        line for line in _command().splitlines() if line.startswith("argument-hint:")
+    )
+    assert "[--merge-guard {draft,off}]" in hint
+    assert hint.index("--conflict-max-tier") < hint.index("--merge-guard")
+
+
+def test_the_command_options_row_has_the_flag_default_and_off_line():
+    rows = [
+        line for line in _command().splitlines() if line.startswith("| `--merge-guard")
+    ]
+    assert len(rows) == 1
+    row = rows[0]
+    assert row.startswith("| `--merge-guard {draft,off}` | draft |")
+    assert "Effective only at `--monitor 3`" in row
+    assert OFF_LINE in row
+
+
+def test_the_command_flag_appears_in_the_hint_the_row_and_the_section_heading():
+    lines = [
+        n for n, line in enumerate(_command().splitlines()) if "merge-guard" in line
+    ]
+    kinds = {
+        "hint": any(
+            _command().splitlines()[n].startswith("argument-hint:") for n in lines
+        ),
+        "row": any(
+            _command().splitlines()[n].startswith("| `--merge-guard") for n in lines
+        ),
+        "heading": any(
+            _command().splitlines()[n].startswith("## Merge guard") for n in lines
+        ),
+    }
+    assert all(kinds.values()), kinds
+
+
+def test_the_command_section_states_default_on_clear_command_and_unverified_gates():
+    section = _command_section()
+    assert section.startswith("## Merge guard (`--merge-guard`)")
+    assert "on by default (`draft`) and acts only at `--monitor 3`" in section
+    assert CLEAR_COMMAND in _command()
+    assert "Medium severity or higher" in section and "once per fix cycle" in section
+    assert "only after the cycle's fix push is confirmed" in section
+    assert "`merge_guard: held`" in section
+    assert (
+        "never marks the PR ready" in section and "`draft_guard_unavailable`" in section
+    )
+    assert "release gates G4 and G5" in section
+    assert "unverified until the owner's run on a disposable PR" in section
+    assert "the PR body states this release gate" in section
+    assert "src/superclaude" not in _command()
+    assert "## Unattended mode" not in _command()
+
+
+def test_the_command_clear_command_is_one_repo_scoped_fenced_line():
+    fenced = [line.strip() for _n, line in _command_lines(COMMAND) if line.strip()]
+    assert CLEAR_COMMAND in fenced
+    assert all(_repo_scoped(line) for line in fenced if _GH_CMD.search(line))

diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index d40562fd..7605addf 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -1922,6 +1922,14 @@ WRITE_VERB_CLASSIFICATION = {
         "never-worker",
         "/sc:pr-submit is on the never-as-worker list (decision D3); its PR, poll and reply calls never run in a worker",
     ),
+    (
+        "src/superclaude/commands/pr-submit.md",
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
