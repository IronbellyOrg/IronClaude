cfa59be1342a8d38c0f56e9ca4cda494f7a02a2e
Review one task for spec compliance.

Task brief: ## Task 18: Add the static protocol and install tests

Depends on: Task 17

Create `tests/pr_submit/test_conflict_sync_protocol.py` with every case listed for it in source section 12.1 (pinned phrases and order pins of sections 8.2 and 8.3, edits E1 to E13 present, one python block, Tier 2 labelling, the evidence script named only in `conflict-intent.md`, repo-scoped `gh` lines, exact `git push` form, the FR-21 prohibited-operation regex scan, no `src/superclaude` text, the allowed-tools test, the static call ceilings) and the byte-identical fragment regression test of source section 12.2 (last paragraph). Add `test_wait_only_sentences_name_the_one_sync_exception` and `test_s5a_retrigger_widened_for_merge_cycles_only` to `tests/pr_submit/test_static_grep.py`, `test_push_parent_ok_still_rejects_a_valid_merge_commit` to `tests/pr_submit/test_pre_pr_checks.py`, and the five new installed file names to the expected list in `tests/unit/test_cli_install.py:248-262`.

Acceptance criteria:
- `uv run pytest tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_static_grep.py tests/pr_submit/test_pre_pr_checks.py tests/unit/test_cli_install.py -q` passes; log saved to `./artifacts/t18-tests.log`.
- The prohibited-operation scan fails when a forbidden command is added to a scratch copy of a new ref (demonstrated once and recorded in `./artifacts/t18-negative-check.txt`).
Global constraints: 
- The design in `./source.md` is the specification. Every section reference below (for example "source section 5.3") points into it. Where a task and the source disagree, the source wins; record the disagreement in the task's evidence.
- Never force-push, and never write a force flag after the words "git push" on any line of a `.md` or `.sh` file in `src/superclaude/skills/sc-pr-submit-protocol/` (the force-push scan in `tests/pr_submit/test_static_grep.py:758-776` covers every such file). The only push text is `git push origin <target_sha>:<HEAD_BRANCH>`; prohibitions are written in words.
- `push_parent_ok`, `evaluate_push_decision`, `push_fail_state`, `push_idempotency_key`, `needs_rebase` and every existing `transition()` edge in `src/superclaude/pr_submit/fsm.py` stay byte-identical (source section 6.1). `resolve_crash_window` in `recovery.py` keeps its signature and return value.
- T-N50: no `git` or `gh` token (regex `\bgh\b|\bgit\b`), docstrings and comments included, in `conflicts.py`, `fsm.py`, `ci.py`, `refs/state-machine.md`, `refs/loop-guard.md` and every other file in `CORE_PURE_FILES` (`tests/pr_submit/test_static_grep.py:37-51`).
- Installed primitives (`SKILL.md`, refs, scripts, `commands/pr-submit.md`) never name a `src/superclaude/` path in new text.
- Every `gh` call in new text carries `--repo "$REPO"` or a `repos/<owner/repo>/` path. Nothing contacts `SuperClaude-Org/SuperClaude_Framework`.
- Never stash, never use a hook-skipping flag, never amend, never stage everything; stage exact paths only.
- `SKILL.md` keeps exactly one python code block (`tests/pr_submit/test_cosmos_protocol.py:36`, `tests/pr_submit/test_codex_reviews.py:688`) and grows by at most 15 lines (source section 8.1).
- Edit `src/superclaude/`, then run `make sync-dev`; never stage `.claude/` paths except `.claude/settings.json`. `.dev/tasks/` is always staged (`git add .dev/tasks`), including this package and its `artifacts/`.
- Python through UV only (`uv run pytest ...`, `uv run python ...`). Run the tests each task names plus `tests/pr_submit/`, `tests/unit/test_cli_install.py` and `tests/commands/`; do not run the full suite (`make test`) or `tests/cli/eval/` as a directory (orchestrator brief; this overrides the `make test` step of source section 12.5).
- Real-git tests run only inside pytest temporary directories with a local bare repository as `origin`, a `gh` stub on `PATH`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, and for real `uv` `UV_OFFLINE=1`, `UV_NO_CONFIG=1`, `UV_CACHE_DIR=<tmp>` (source section 12 preamble). No test touches the network or `~/.claude`.
- Out of scope: P3 late re-sync (#361) and the post-release verification follow-ups V1 to V8 of source section 14; they are not implemented by this plan.
- Task evidence (test logs, grep output) goes under `./artifacts/` in this package.
Start sha: cfa59be1342a8d38c0f56e9ca4cda494f7a02a2e
Diff against the start snapshot: diff --git a/tests/pr_submit/test_conflict_sync_protocol.py b/tests/pr_submit/test_conflict_sync_protocol.py
new file mode 100644
index 00000000..87bb6e4b
--- /dev/null
+++ b/tests/pr_submit/test_conflict_sync_protocol.py
@@ -0,0 +1,579 @@
+"""Static protocol tests for the merge-conflict skill text (issue #305).
+
+Covers the skill text of design section 8 (FR-4 to FR-10, FR-14, FR-18 to FR-21,
+FR-27 to FR-31, FR-33, NFR-1, NFR-4, NFR-6, NFR-8, NFR-9, NFR-14): the pinned phrases
+and order pins of the two new refs, the thirteen `SKILL.md` edits E1 to E13, Tier 2
+labelling, repo-scoped `gh` lines, the one `git push` form, the FR-21
+prohibited-operation scan, the allowed-tools check, the static call ceilings and the
+byte-identical fragments of the spec (design section 12.2, last paragraph).
+
+Skill text is pinned by literal substrings, never by line numbers.
+"""
+
+from __future__ import annotations
+
+import re
+from pathlib import Path
+
+import pytest
+
+from superclaude.pr_submit.conflicts import MECHANICAL_RULES
+from tests.pr_submit.test_static_grep import _GH_CMD, _command_lines, _repo_scoped
+
+REPO_ROOT = Path(__file__).resolve().parents[2]
+SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-pr-submit-protocol"
+SKILL_MD = SKILL_DIR / "SKILL.md"
+COMMAND_MD = REPO_ROOT / "src" / "superclaude" / "commands" / "pr-submit.md"
+MECHANICAL_REF = SKILL_DIR / "refs" / "conflict-mechanical.md"
+INTENT_REF = SKILL_DIR / "refs" / "conflict-intent.md"
+STATE_MACHINE_REF = SKILL_DIR / "refs" / "state-machine.md"
+PROBE_SCRIPT = SKILL_DIR / "scripts" / "probe-merge.sh"
+FINISH_SCRIPT = SKILL_DIR / "scripts" / "finish-merge.sh"
+EVIDENCE_SCRIPT = SKILL_DIR / "scripts" / "collect-conflict-evidence.sh"
+POLL_CI_SCRIPT = SKILL_DIR / "scripts" / "poll-ci-checks.sh"
+
+NEW_REFS = (MECHANICAL_REF, INTENT_REF)
+NEW_SCRIPTS = (PROBE_SCRIPT, FINISH_SCRIPT, EVIDENCE_SCRIPT)
+NEW_FILES = NEW_REFS + NEW_SCRIPTS
+
+PUSH_LINE = "git push origin <target_sha>:<HEAD_BRANCH>"
+ALLOWED_PROGRAMS = frozenset({"git", "gh", "uv", "make", "jq"})
+
+
+def _read(path: Path) -> str:
+    return path.read_text(encoding="utf-8")
+
+
+def _prose(path: Path) -> str:
+    """The file as prose: hand-wrapping and blockquote markers are not the contract."""
+    return " ".join(_read(path).replace("\n> ", " ").split())
+
+
+def _assert_in_order(text: str, needles: tuple[str, ...]) -> None:
+    """Each needle is present and its first occurrence follows the previous one's."""
+    positions = []
+    for needle in needles:
+        assert needle in text, f"missing {needle!r}"
+        positions.append(text.index(needle))
+    for (a, pa), (b, pb) in zip(
+        zip(needles, positions), zip(needles[1:], positions[1:])
+    ):
+        assert pa < pb, f"{a!r} (at {pa}) must come before {b!r} (at {pb})"
+
+
+# --- Pinned phrases and order pins (design sections 8.2 and 8.3) --------------
+
+MECHANICAL_PINS = (
+    "git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit "
+    "--no-ff <base_sha>",
+    PUSH_LINE,
+    "git checkout --ours -- uv.lock",
+    "uv lock --check",
+    "git add -- uv.lock",
+    "merge_parent_ok(<parents>, pre_push_sha, base_sha)",
+    "git merge-base --is-ancestor <base_sha> origin/<base>",
+    "The deterministic core DECIDES",
+    "evaluate_sync_decision",
+    "sync_started",
+    "reason `pr_conflicting`",
+    "--evidence-sha",
+    "expect_checks",
+    "push_rejected",
+    "push_failed",
+    "git revert -m 1 <merge_sha>",
+    "Nothing was changed and nothing was pushed.",
+    "never stash",
+)
+
+
+@pytest.mark.parametrize("phrase", MECHANICAL_PINS)
+def test_conflict_mechanical_pinned_phrases(phrase):
+    assert phrase in _read(MECHANICAL_REF), phrase
+
+
+def test_conflict_mechanical_order_pins():
+    """The head check and `merge_preflight_ok` come before `sync_started`, which comes
+    before the merge command; the head re-read comes before `merge_parent_ok`, before
+    `--is-ancestor`, before "The deterministic core DECIDES", before the push line."""
+    text = _read(MECHANICAL_REF)
+    merge_cmd = "merge --no-commit --no-ff <base_sha>"
+    _assert_in_order(text, ("**Step 1. Head check.**", "sync_started", merge_cmd))
+    _assert_in_order(text, ("merge_preflight_ok", "sync_started", merge_cmd))
+    _assert_in_order(
+        text,
+        (
+            "**Step 10(a). Head re-read.**",
+            "merge_parent_ok(<parents>, pre_push_sha, base_sha)",
+            "--is-ancestor",
+            "The deterministic core DECIDES",
+            PUSH_LINE,
+        ),
+    )
+
+
+INTENT_PINS = (
+    "scripts/collect-conflict-evidence.sh",
+    "evidence-validator",
+    "One revision pass",
+    "one sentence",
+    "dropped",
+    "high-suspicion",
+    "configured reviewers",
+    "base_authored",
+    "git add -- <path>",
+    "git rm -- <path>",
+)
+
+RECORD_FIELDS = (
+    "kind",
+    "root_cause",
+    "ours_intent",
+    "theirs_intent",
+    "resolution",
+    "behavior_after",
+    "dropped",
+    "evidence",
+)
+
+
+@pytest.mark.parametrize("phrase", INTENT_PINS)
+def test_conflict_intent_pinned_phrases(phrase):
+    assert phrase in _read(INTENT_REF), phrase
+
+
+def test_conflict_intent_record_fields_in_order():
+    """Section 6 lists the record fields in the order the core parses them, and the
+    example section follows the same order."""
+    text = _read(INTENT_REF)
+    section = text[text.index("## 6. The resolution record") :]
+    section = section[: section.index("\n## 7.")]
+    _assert_in_order(
+        section, ("`## <path>`",) + tuple(f"`{f}:`" for f in RECORD_FIELDS)
+    )
+    example = section[section.index("> ## ") :]
+    _assert_in_order(example, tuple(f"\n> {f}: " for f in RECORD_FIELDS))
+
+
+# --- SKILL.md edits E1 to E13 (design section 8.1) ----------------------------
+
+SKILL_EDITS = {
+    "E1": (
+        "| `--conflict-max-tier {0,1,2}` | No (default 1) | Highest merge-conflict tier "
+        "the skill may act on: 0 detect and report only, 1 also regenerate a conflicted "
+        "root `uv.lock` (Tier 1), 2 also resolve text conflicts by stated intent (Tier 2, "
+        "off by default). Tier 3 never resolves. |",
+    ),
+    "E2": (
+        "**STOP** if `--monitor >= 1` and the PR cannot be confirmed on the resolved "
+        "target repo (origin's\n`owner/repo`, parsed from `git remote get-url origin`): "
+        "a wrong origin, or a returned URL whose `owner/repo` ≠ the resolved target → "
+        "HALT,\ninstruct the operator to close the misrouted PR. Being behind the base "
+        "branch is not a STOP at L1+:\nWave 0 reports how many commits behind (Tier 0) "
+        "and the conflict check below classifies any conflict.",
+    ),
+    "E3": (
+        "| `push_count` | int | Landed fix, CI and Tier 2 merge pushes (`kind` on every "
+        "push record; Tier 1 sync pushes are counted in `sync_push_count`); `<= "
+        "max_rounds + 1` with the fallback's single push; 0 below L3. |",
+        "| `sync_tier` | int or null | Highest merge-conflict tier seen this run (0 to 3; "
+        "null when it could not be classified). |",
+        "| `sync_outcome` | enum | `none` / `report_only` / `left_in_progress` / "
+        "`pushed` / `aborted` / `halted`. |",
+        '| `sync_push_count` | int | Landed Tier 1 sync pushes (`kind: "sync"`, at most '
+        "`SYNC_CAP = 1`); never counted in `push_count`. |",
+    ),
+    "E4": (
+        "Wave 0c: (L1+) conflict check + report      ← loads refs/conflict-mechanical.md "
+        "ONLY when the probe runs",
+        "C-initial: (L3, Tier 2) merge cycle before the first review poll ← loads "
+        "refs/conflict-mechanical.md + refs/conflict-intent.md",
+        "Wave 8a: (L1+) act on a conflict before the CI wait ← loads "
+        "refs/conflict-mechanical.md ONLY when the probe runs",
+    ),
+    "E5": (
+        "and rebase if behind `origin/<base>` only at L0 (at L1+ the create path does not "
+        "rebase and does not halt: the branch is already published when `gh pr create` "
+        "runs, so report how many commits it is behind, a Tier 0 result; with `--pr "
+        "<N>`, at any level, do not rebase: the PR head is already published, so report "
+        "how many commits it is behind instead). At L1+, also before creating or "
+        'attaching, run `scripts/probe-merge.sh --ops-only --repo "$REPO"`: a non-null '
+        "`foreign_op` (a merge, rebase, cherry-pick, revert or sequencer operation in "
+        "progress) → HALT before Wave 1 with status `terminal_halted`, reason "
+        "`foreign_op_in_progress`, nothing created (on `--resume`, "
+        "`conflict_resume_plan` in `refs/conflict-mechanical.md` decides first).",
+    ),
+    "E6": (
+        "- **Wave 0 conflict check (L1+ only; L0 skips it):** after the head binding, "
+        'read `gh pr view <N> --repo "$REPO" --json '
+        "baseRefName,mergeable,mergeStateStatus` (re-read an `UNKNOWN` up to 3 times, "
+        "10 s apart) and normalise it with "
+        "`superclaude.pr_submit.conflicts.mergeability_hint`. Only `conflicting` or a "
+        "persistent `unknown` loads `refs/conflict-mechanical.md` and runs "
+        "`scripts/probe-merge.sh`; follow that ref to classify, print the plan before "
+        'any edit, and route with `conflict_action(hook="wave0")` (Tier 3 at L3 halts '
+        "here: `terminal_halted`, reason `conflict_tier3`, nothing touched). Any other "
+        'hint is Tier 0: report "<N> commits behind, no conflicts" (or the `BLOCKED` '
+        "reason) and continue; no ref is loaded.",
+    ),
+    "E7": (
+        "`--monitor 0` remains no-monitor. **C-initial (L3, Tier 2, only when Wave 0 "
+        "planned it under `--conflict-max-tier 2`):** after arming and before the first "
+        "review poll, load `refs/conflict-intent.md` and run the Tier 2 merge cycle of "
+        "`refs/conflict-mechanical.md` through `transition(S2_CLASSIFY, "
+        '"conflicting")`; its S5 wait is the run\'s first review wait.',
+    ),
+    "E8": (
+        "AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or "
+        "is a Tier 2 merge cycle (push kind `merge`; "
+        "`superclaude.pr_submit.fsm.should_retrigger`), post",
+    ),
+    "E9": (
+        "load `refs/ci-poll.md`, then run Wave 8a (below) before the CI poll loop. "
+        "These are",
+        "classify_checks(payload, wait_sha=<sha at flip or last push>, "
+        "expect_checks=<the value recorded for that push, else false>)",
+        "without fetching logs, editing, or pushing a fix; the single Tier 1 sync push "
+        "of Wave 8a (`SYNC_CAP = 1`) is the only push a wait-only path allows, and it is "
+        "not a fix.",
+        "so this push too carries only the cycle's one fix commit; its triad passes "
+        '`push_kind="ci"`, `review_terminal` and `expect_checks=True`.',
+        "Only parsed empty required **and** all-checks lists, with `expect_checks` "
+        "false, prove there are no Actions; with `expect_checks` true an empty list is "
+        "`polling`, and expiry is the CI timeout with reason `ci_not_started`, never "
+        "clean.",
+    ),
+    "E10": (
+        "- **Wave 8a (L1+, conflict act before the CI wait; same entry outcomes as Wave "
+        '8):** read `gh pr view <N> --repo "$REPO" --json '
+        "baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,"
+        "isCrossRepository` (same `UNKNOWN` re-reads). Only `conflicting` or a "
+        "persistent `unknown` loads `refs/conflict-mechanical.md`, re-probes and acts on "
+        '`conflict_action(hook="wave8a", entering=<review outcome>)`: at L3 a Tier 1 '
+        "conflict becomes one sync merge commit pushed fast-forward (no round, no "
+        "re-trigger, no reply, no resolve; the one push a wait-only path allows), then "
+        "the CI wait runs on the new head with `expect_checks`; L2 leaves it resolved "
+        "and validated but uncommitted (`halt_before_push`, only after `clean` / "
+        "`REPORT_ONLY`); L1 proposes (also only after `clean` / `REPORT_ONLY`). A PR "
+        "still conflicting with nothing pushed skips the CI wait with reason "
+        "`pr_conflicting` (GitHub runs no `pull_request` checks on it) and ends with the "
+        "status `conflict_action` returns. When any hook this run read `conflicting`, "
+        "re-read `mergeable` before sending `transition(clean)`; `CONFLICTING` → "
+        "`terminal_halted`, reason `late_conflict` (late re-sync: #361).",
+    ),
+    "E11": (
+        "- Detect merge conflicts at Wave 0 (L1+), report the tier and plan before any "
+        "edit, and resolve only within `--conflict-max-tier` and the ordinal ceiling, "
+        "publishing a resolution only as one merge commit of the recorded base tip, "
+        "pushed fast-forward.",
+        "- Rebase a published PR head (at L1+ the create path no longer rebases), stash, "
+        "take one side for a whole tree, commit a merge without "
+        "`scripts/finish-merge.sh`, or push a merge commit whose parents are not exactly "
+        "the PR head and the recorded base tip (`merge_parent_ok`).",
+    ),
+    "E12": (
+        "| Wrong origin / wrong-owner URL | HALT; instruct operator to close the "
+        "misrouted PR (FM-11). |",
+        '| Behind base branch (create path at L1+, or `--pr`) | Tier 0 report ("<N> '
+        'commits behind"); no rebase, no halt. At L0 the create path still rebases. |',
+        "| A merge, rebase, cherry-pick, revert or sequencer operation is in progress "
+        "(L1+) | `terminal_halted`, reason `foreign_op_in_progress`, before anything is "
+        "created; finish or abort that operation yourself, then re-run. |",
+        "| Merge conflict that needs a human (Tier 3: submodule, symlink, mode change, "
+        "protected or migration path, binary, lock or generated file without a rule, "
+        "more than 8 text files, unclassifiable) | L3: `terminal_halted` at the end of "
+        "Wave 0, reason `conflict_tier3`, nothing touched or pushed; L1/L2: reported and "
+        "the run continues; HALT message from `refs/conflict-mechanical.md`. |",
+        "| A conflict cycle stops (dirty tree, foreign merge, guard, finish gate, VAL, "
+        "rejected or failed push) | `terminal_halted` with the reason from "
+        "`refs/conflict-mechanical.md` (`merge_preflight_dirty`, `sync_*`, "
+        "`push_rejected`, `push_failed`); nothing pushed unless the message says the "
+        "push landed; never stash, never discard your files. |",
+    ),
+    "E13": (
+        "(push if you are ahead; `git pull --ff-only` if you are behind; this skill "
+        "never rewrites a published branch)",
+    ),
+}
+
+
+@pytest.mark.parametrize("edit", sorted(SKILL_EDITS, key=lambda e: int(e[1:])))
+def test_skill_edit_present(edit):
+    text = _read(SKILL_MD)
+    for fragment in SKILL_EDITS[edit]:
+        assert fragment in text, f"{edit}: missing {fragment!r}"
+
+
+def test_skill_edits_cover_e1_to_e13():
+    assert sorted(SKILL_EDITS, key=lambda e: int(e[1:])) == [
+        f"E{i}" for i in range(1, 14)
+    ]
+
+
+def test_skill_replaced_text_is_gone():
+    """E5 and E13 replaced their old substrings; E13's force-push sentence is absent
+    from the head-binding bullet."""
+    text = _read(SKILL_MD)
+    assert "and rebase if behind `origin/<base>` (with `--pr <N>`" not in text
+    binding = text[text.index("**Wave 0 head binding (L1+ only") :]
+    binding = binding[: binding.index("\n- **Wave 0 conflict check")]
+    assert "needs a force-push" not in binding
+
+
+def test_skill_keeps_one_python_block():
+    fences = [
+        line for line in _read(SKILL_MD).splitlines() if line.startswith("```python")
+    ]
+    assert len(fences) == 1
+
+
+# --- Tier 2 labelling and where the evidence script is named -------------------
+
+# Pre-existing SKILL.md lines that name `evidence-validator` for finding verification
+# (Waves 2-3); they predate the conflict text and are not Tier 2 text.
+_PRE_EXISTING_VALIDATOR_LINES = (
+    "read-only evidence-validator before diagnosis or edits.",
+    "- **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent",
+)
+
+
+def test_intent_and_validator_lines_say_tier_2():
+    offenders = []
+    for path in (SKILL_MD, MECHANICAL_REF):
+        for lineno, line in enumerate(_read(path).splitlines(), 1):
+            if "conflict-intent.md" not in line and "evidence-validator" not in line:
+                continue
+            if path == SKILL_MD and "conflict-intent.md" not in line:
+                if any(old in line for old in _PRE_EXISTING_VALIDATOR_LINES):
+                    continue
+            if "Tier 2" not in line:
+                offenders.append(f"{path.name}:{lineno}: {line.strip()}")
+    assert not offenders, "lines without a Tier 2 label:\n" + "\n".join(offenders)
+    # The pre-existing exemptions still match real lines (no stale exemption).
+    skill = _read(SKILL_MD)
+    for old in _PRE_EXISTING_VALIDATOR_LINES:
+        assert old in skill, old
+
+
+def test_evidence_script_named_only_in_conflict_intent():
+    name = "collect-conflict-evidence.sh"
+    assert name in _read(INTENT_REF)
+    surfaces = [COMMAND_MD] + [
+        p
+        for p in sorted(SKILL_DIR.rglob("*"))
+        if p.is_file() and p.suffix in {".md", ".sh"}
+    ]
+    offenders = [
+        str(p.relative_to(REPO_ROOT))
+        for p in surfaces
+        if p not in (INTENT_REF, EVIDENCE_SCRIPT) and name in _read(p)
+    ]
+    assert not offenders, offenders
+
+
+# --- gh scoping and the one push form ----------------------------------------
+
+# A pre-existing error message in poll-ci-checks.sh (unchanged from master) quotes
+# `gh pr checks` inside a `die` string; it is text printed to the operator, not a gh
+# call. Exempted by exact content so any new unscoped gh line still fails.
+_GH_MESSAGE_LINES = {
+    POLL_CI_SCRIPT: (
+        "*) die \"installed gh lacks 'gh pr checks --json' (see 'gh --version'); "
+        "upgrade gh and confirm via 'gh pr checks --help' before CI wait\" 2 ;;",
+    ),
+}
+
+
+def test_gh_command_lines_are_repo_scoped():
+    offenders = []
+    for path in NEW_REFS + (
+        PROBE_SCRIPT,
+        FINISH_SCRIPT,
+        EVIDENCE_SCRIPT,
+        POLL_CI_SCRIPT,
+    ):
+        exempt = _GH_MESSAGE_LINES.get(path, ())
+        for lineno, line in _command_lines(path):
+            if not _GH_CMD.search(line) or _repo_scoped(line):
+                continue
+            if line.strip() in exempt:
+                continue
+            offenders.append(f"{path.name}:{lineno}: {line.strip()}")
+    assert not offenders, "unscoped gh command lines:\n" + "\n".join(offenders)
+    for path, lines in _GH_MESSAGE_LINES.items():
+        stripped = {line.strip() for _n, line in _command_lines(path)}
+        for line in lines:
+            assert line in stripped, f"stale exemption in {path.name}: {line!r}"
+
+
+def test_every_git_push_in_new_files_is_the_one_form():
+    seen = 0
+    for path in NEW_FILES:
+        for match in re.finditer(r"git push[^`\n]*", _read(path)):
+            assert match.group(0).strip() == PUSH_LINE, (path.name, match.group(0))
+            seen += 1
+    assert seen >= 1
+
+
+# --- FR-21 prohibited-operation scan -----------------------------------------
+
+PROHIBITED_OPERATIONS = (
+    r"\bgit\s+stash\b",
+    r"--no-verify\b",
+    r"--amend\b",
+    r"\badd\s+(-A|--all|\.)(\s|$|`)",
+    r"--(ours|theirs)\s+(--\s+)?\.(\s|$|`)",
+    r"\bcheckout\s+--(ours|theirs)\s*(`|$)",
+    r"-X\s*(ours|theirs)\b",
+    r"-s\s+ours\b",
+    r"\breset\s+--hard\b",
+    r"\bcommit\s+--only\b",
+    r"\bcommit\s+(-a|--all)\b",
+    r"\bgit\s+config\b",
+    r"\bgit\s+worktree\b",
+    r"\bgit\s+rebase\b",
+    r"rerere\.enabled=true",
+)
+_CHECKOUT_OR_SWITCH = re.compile(r"\bgit\s+(checkout|switch)\b")
+_ONLY_CHECKOUT = "git checkout --ours -- uv.lock"
+
+
+def prohibited_operation_hits(path: Path) -> list[str]:
+    """Every FR-21 hit in ``path``: one entry per regex match, plus every
+    `git checkout` / `git switch` that is not exactly the one lock-file checkout."""
+    text = _read(path)
+    hits = []
+    for pattern in PROHIBITED_OPERATIONS:
+        for match in re.finditer(pattern, text, flags=re.MULTILINE):
+            lineno = text.count("\n", 0, match.start()) + 1
+            hits.append(f"{path.name}:{lineno}: {pattern} -> {match.group(0)!r}")
+    for match in _CHECKOUT_OR_SWITCH.finditer(text):
+        if not text.startswith(_ONLY_CHECKOUT, match.start()):
+            lineno = text.count("\n", 0, match.start()) + 1
+            hits.append(f"{path.name}:{lineno}: checkout/switch -> {match.group(0)!r}")
+    return hits
+
+
+def test_prohibited_operation_patterns_catch_each_form():
+    """Each regex catches its forbidden form and passes the allowed lock checkout."""
+    forms = (
+        "git stash push",
+        "git commit --no-verify",
+        "git commit --amend",
+        "git add -A",
+        "git checkout --theirs -- .",
+        "`git checkout --ours`",
+        "git merge -Xours main",
+        "git merge -s ours main",
+        "git reset --hard HEAD",
+        "git commit --only -- f",
+        "git commit -a",
+        "git config user.name x",
+        "git worktree add ../x",
+        "git rebase main",
+        "git -c rerere.enabled=true merge",
+    )
+    for pattern, form in zip(PROHIBITED_OPERATIONS, forms):
+        assert re.search(pattern, form, flags=re.MULTILINE), (pattern, form)
+    for pattern in PROHIBITED_OPERATIONS:
+        assert re.search(pattern, _ONLY_CHECKOUT, flags=re.MULTILINE) is None, pattern
+    assert _CHECKOUT_OR_SWITCH.search("git switch main")
+
+
+@pytest.mark.parametrize("path", NEW_FILES, ids=lambda p: p.name)
+def test_fr21_prohibited_operation_scan(path):
+    hits = prohibited_operation_hits(path)
+    assert not hits, "prohibited operations:\n" + "\n".join(hits)
+
+
+def test_the_only_checkout_is_the_lock_file_seed():
+    found = [
+        (path.name, m.group(0))
+        for path in NEW_FILES
+        for m in _CHECKOUT_OR_SWITCH.finditer(_read(path))
+    ]
+    assert found == [("conflict-mechanical.md", "git checkout")]
+
+
+# --- NFR-8: no source-tree paths in installed text ---------------------------
+
+
+@pytest.mark.parametrize(
+    "path", NEW_FILES + (SKILL_MD, COMMAND_MD), ids=lambda p: p.name
+)
+def test_no_src_superclaude_path(path):
+    assert "src/superclaude" not in _read(path)
+
+
+# --- Allowed tools -------------------------------------------------------------
+
+
+def _fenced_first_words(path: Path) -> list[str]:
+    return [line.split()[0] for _n, line in _command_lines(path) if line.strip()]
+
+
+def test_allowed_tools_cover_every_program():
+    """Every `MECHANICAL_RULES` argv[0] and the first word of every fenced command
+    line in the two refs is git, gh, uv, make, jq or a `scripts/` path, and each of
+    those programs is granted as `Bash(<prog> *)` in the SKILL front matter."""
+    front = _read(SKILL_MD).split("\n---\n", 1)[0]
+    tools_line = next(
+        line for line in front.splitlines() if line.startswith("allowed-tools:")
+    )
+    granted = set(re.findall(r"Bash\((\S+) \*\)", tools_line))
+    programs = set()
+    for rule in MECHANICAL_RULES:
+        programs.add(rule.regenerate[0])
+        if rule.check:
+            programs.add(rule.check[0])
+    scripts = set()
+    for path in NEW_REFS:
+        for word in _fenced_first_words(path):
+            if word.startswith("scripts/"):
+                scripts.add(word)
+            else:
+                programs.add(word)
+    assert programs <= ALLOWED_PROGRAMS, programs - ALLOWED_PROGRAMS
+    assert programs <= granted, programs - granted
+    for script in scripts:
+        assert (SKILL_DIR / script).is_file(), script
+
+
+# --- NFR-14 static call ceilings -------------------------------------------------
+
+
+def test_static_call_ceilings_in_conflict_mechanical():
+    """One probe command, one `finish-merge.sh` commit-mode command, one push."""
+    lines = [line.strip() for _n, line in _command_lines(MECHANICAL_REF)]
+    probes = [line for line in lines if "scripts/probe-merge.sh" in line]
+    finish_commit = [
+        line
+        for line in lines
+        if "scripts/finish-merge.sh" in line and "--precheck" not in line
+    ]
+    pushes = [line for line in lines if re.search(r"\bgit\s+push\b", line)]
+    assert len(probes) == 1, probes
+    assert len(finish_commit) == 1, finish_commit
+    assert "--message-file" in finish_commit[0]
+    assert pushes == [PUSH_LINE]
+
+
+# --- Byte-identical spec fragments (design section 12.2, last paragraph) ---------
+
+
+def test_spec_byte_identical_fragments_survive():
+    skill = _read(SKILL_MD)
+    assert "with `--pr <N>`, at any level, do not rebase" in skill
+    assert "rebase if behind `origin/<base>`" in skill
+    wave6 = skill[skill.index("- **Wave 6 (L3 only):**") :]
+    wave6 = wave6[: wave6.index("\n- **Wave 6b")]
+    for fragment in (
+        "pr_head_ok(<local branch>, pre_push_sha,",
+        "push_parent_ok(<parents>, pre_push_sha)",
+        "The deterministic core DECIDES",
+        "then set `pre_push_sha := target_sha`",
+    ):
+        assert fragment in wave6, fragment
+    assert "push any commit besides the cycle's one fix commit" in _read(COMMAND_MD)
+    machine = _prose(STATE_MACHINE_REF)
+    assert "the commit to push must have exactly one parent, that same SHA" in machine
+    assert "The parent check applies only when the cycle applied edits" in machine
diff --git a/tests/pr_submit/test_static_grep.py b/tests/pr_submit/test_static_grep.py
index b9a53820..2317bde1 100644
--- a/tests/pr_submit/test_static_grep.py
+++ b/tests/pr_submit/test_static_grep.py
@@ -777,3 +777,58 @@ def test_skill_forbids_force_push():
         if path.is_file() and path.suffix in {".md", ".sh"}:
             hit = force.search(path.read_text("utf-8"))
             assert hit is None, (path, hit and hit.group(0))
+
+
+# --- Issue #305: merge-conflict cycles -----------------------------------------
+
+
+def _prose(path: Path) -> str:
+    """The file as prose: hand-wrapping and blockquote markers are not the contract."""
+    raw = path.read_text(encoding="utf-8")
+    return " ".join(raw.replace("\n> ", " ").split())
+
+
+def test_wait_only_sentences_name_the_one_sync_exception():
+    """INV-009 / FR-33: every wait-only sentence names the single Tier 1 sync push of
+    Wave 8a as the only push a wait-only path allows, and says it is not a fix."""
+    skill = _SKILL_MD.read_text(encoding="utf-8")
+    assert (
+        "the single Tier 1 sync push of Wave 8a (`SYNC_CAP = 1`) is the only push a "
+        "wait-only path allows, and it is not a fix"
+    ) in skill
+    machine = _prose(SKILL_DIR / "refs" / "state-machine.md")
+    assert (
+        "never an additional fix or fix push. The single exception is the one Tier 1 "
+        "sync push (5.2d), which is not a fix."
+    ) in machine
+    ci_poll = (SKILL_DIR / "refs" / "ci-poll.md").read_text(encoding="utf-8")
+    assert (
+        "the one Tier 1 sync push of Wave 8a is the only push allowed here, and it is "
+        "not a fix"
+    ) in ci_poll
+
+
+def test_s5a_retrigger_widened_for_merge_cycles_only():
+    """P2 / QA-3a: the Wave 6 S5a re-trigger is widened only for a Tier 2 merge cycle;
+    the zero-edit fix-commit sentence and the state-machine parent-check sentence are
+    unchanged."""
+    text = _SKILL_MD.read_text(encoding="utf-8")
+    wave6 = text[text.index("- **Wave 6 (L3 only):**") :]
+    wave6 = wave6[: wave6.index("\n- **Wave 6b")]
+    assert (
+        "or is a Tier 2 merge cycle (push kind `merge`; "
+        "`superclaude.pr_submit.fsm.should_retrigger`)"
+    ) in wave6
+    # The widening sits inside the S5a sentence, after the applied-edits condition.
+    assert (
+        "AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) "
+        "or is a Tier 2 merge cycle (push kind `merge`; "
+        "`superclaude.pr_submit.fsm.should_retrigger`), post"
+    ) in wave6
+    # Unchanged pins (test_skill_binds_checkout_and_push_target_to_pr_head).
+    assert (
+        "Next, when the cycle applied edits (a zero-edit cycle has no fix commit"
+        in wave6
+    )
+    machine = _prose(SKILL_DIR / "refs" / "state-machine.md")
+    assert "The parent check applies only when the cycle applied edits" in machine
diff --git a/tests/pr_submit/test_pre_pr_checks.py b/tests/pr_submit/test_pre_pr_checks.py
index 847067c7..7bb153a2 100644
--- a/tests/pr_submit/test_pre_pr_checks.py
+++ b/tests/pr_submit/test_pre_pr_checks.py
@@ -15,6 +15,7 @@ from __future__ import annotations
 
 import pytest
 
+from superclaude.pr_submit.conflicts import merge_parent_ok
 from superclaude.pr_submit.fsm import (
     needs_rebase,
     origin_ok,
@@ -228,3 +229,11 @@ def test_push_parent_ok_fails_closed_on_bad_ids(bad_sha):
     assert push_parent_ok([SHA], bad_sha) is False
     # Equal on both sides must still fail.
     assert push_parent_ok([bad_sha], bad_sha) is False
+
+
+def test_push_parent_ok_still_rejects_a_valid_merge_commit():
+    """Issue #305: a conflict cycle's merge commit passes its own gate
+    (`merge_parent_ok`) and is still refused by the fix-push gate, so the two parent
+    checks stay disjoint and `push_parent_ok` is unchanged."""
+    assert merge_parent_ok([SHA, OTHER_SHA], SHA, OTHER_SHA) is True
+    assert push_parent_ok([SHA, OTHER_SHA], SHA) is False
diff --git a/tests/unit/test_cli_install.py b/tests/unit/test_cli_install.py
index 23910020..bd0ca915 100644
--- a/tests/unit/test_cli_install.py
+++ b/tests/unit/test_cli_install.py
@@ -248,6 +248,8 @@ sc-post-release-protocol/templates/sysop-test-guide.md
 sc-post-release-protocol/templates/user-test-guide.md sc-pr-submit-protocol/SKILL.md
 sc-pr-submit-protocol/refs/auggie-fallback.md
 sc-pr-submit-protocol/refs/augment-poll.md sc-pr-submit-protocol/refs/ci-poll.md
+sc-pr-submit-protocol/refs/conflict-intent.md
+sc-pr-submit-protocol/refs/conflict-mechanical.md
 sc-pr-submit-protocol/refs/detection-contract.md
 sc-pr-submit-protocol/refs/finding-verify.md
 sc-pr-submit-protocol/refs/loop-guard.md
@@ -256,8 +258,11 @@ sc-pr-submit-protocol/refs/severity-routing.md
 sc-pr-submit-protocol/refs/state-machine.md
 sc-pr-submit-protocol/refs/thread-reply.md
 sc-pr-submit-protocol/refs/troubleshoot-dispatch.md
+sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh
+sc-pr-submit-protocol/scripts/finish-merge.sh
 sc-pr-submit-protocol/scripts/poll-augment-review.sh
 sc-pr-submit-protocol/scripts/poll-ci-checks.sh
+sc-pr-submit-protocol/scripts/probe-merge.sh
 sc-pr-submit-protocol/scripts/reply-resolve-thread.sh
 sc-pr-submit-protocol/scripts/retrigger-review.sh sc-recommend/SKILL.md
 sc-recommend/refs/delegation-vs-native-heuristics.md
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t18-tests.log b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t18-tests.log
new file mode 100644
index 00000000..af33190d
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t18-tests.log
@@ -0,0 +1,18 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-305-pr-submit-conflicts
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 224 items
+
+tests/pr_submit/test_conflict_sync_protocol.py ......................... [ 11%]
+..........................................                               [ 29%]
+tests/pr_submit/test_static_grep.py .....................                [ 39%]
+tests/pr_submit/test_pre_pr_checks.py .................................. [ 54%]
+......                                                                   [ 57%]
+tests/unit/test_cli_install.py ......................................... [ 75%]
+.......................................................                  [100%]
+
+============================= 224 passed in 1.59s ==============================
diff --git a/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t18-negative-check.txt b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t18-negative-check.txt
new file mode 100644
index 00000000..aae81b26
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-design-20261104-164423/artifacts/t18-negative-check.txt
@@ -0,0 +1,19 @@
+# T18 negative check: the FR-21 prohibited-operation scan fails on a scratch copy of refs/conflict-intent.md with one forbidden command appended
+$ mktemp -d /tmp/t18-negative.XXXXXXXX  -> /tmp/t18-negative.v4esz1rB
+$ cp src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md /tmp/t18-negative.v4esz1rB/conflict-intent.md
+$ printf '\n```bash\ngit stash push -m wip\n```\n' >> /tmp/t18-negative.v4esz1rB/conflict-intent.md
+$ tail -3 /tmp/t18-negative.v4esz1rB/conflict-intent.md
+```bash
+git stash push -m wip
+```
+$ PYTHONDONTWRITEBYTECODE=1 uv run python -c 'import sys; from pathlib import Path; from tests.pr_submit.test_conflict_sync_protocol import prohibited_operation_hits as h; real=h(Path("src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md")); bad=h(Path(sys.argv[1])); print("real ref hits:", real); print("scratch copy hits:", bad); sys.exit(1 if bad else 0)' /tmp/t18-negative.v4esz1rB/conflict-intent.md
+real ref hits: []
+scratch copy hits: ["conflict-intent.md:130: \\bgit\\s+stash\\b -> 'git stash'"]
+exit=1 (1 = the scan found the forbidden command)
+$ PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/pr_submit/test_conflict_sync_protocol.py -q -p no:cacheprovider -k fr21   # real refs unchanged, still clean
+======================= 5 passed, 62 deselected in 0.36s =======================
+$ rm -rf -- /tmp/t18-negative.v4esz1rB
+scratch dir removed
+$ git status --porcelain -- src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
+?? src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md
+(`??` = the ref is a new, untracked file of this release; the scratch edit never touched it.)

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
