35dc0c5eda74b884f51938ea9ad669361ca2a8b4
Review one task for spec compliance.

Task brief: Task T1 (plan file /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md, lines 48-69); AC ids T1.AC1 to T1.AC4 are the bullets under `Acceptance criteria:` in source order.

## Task 1: Record the baselines and add the P1 data-driven section checks to `tests/skills/test_worker_contract.py`

Before any edit in this plan, record these baselines under `./artifacts/` (inputs, not evidence; they may contain failures that exist before this plan):
- Run `make sync-dev`, then `make verify-sync`, and save the output and exit code to `./artifacts/verify-sync-baseline.txt` (a fresh worktree may have no or stale `.claude/` copies).
- `uv run pytest tests/skills/ -q -rf -p no:cacheprovider` to `./artifacts/ac-c3-baseline.txt` (spec AC-C3).
- `uv run pytest tests/core tests/commands tests/recommend tests/cli tests/cli_portify tests/unit tests/roadmap -q -rf -p no:cacheprovider --ignore=tests/cli/eval/test_perf_home_setup.py` to `./artifacts/t1-baseline-wider.txt`.
- `make lint` (it runs the architecture lint and `uv run ruff check .`) to `./artifacts/lint-baseline.txt`, with its exit code, and `uv run ruff format --check tests/skills/test_worker_contract.py tests/commands/test_workflow_command.py tests/commands/test_graph_command.py tests/commands/test_impact_command.py tests/skills/test_brainstorm_protocol.py` to `./artifacts/format-baseline.txt`.
- `./artifacts/t1-accepted-failures.md` lists every test that fails in either test baseline, each labelled `pre-existing`, and states that the five other baseline files exist.

Then edit `tests/skills/test_worker_contract.py` only:
- Add a module constant `P1_COMMANDS`, the sixteen command names in this order: adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow, analyze, build, business-panel, design, document, explain, index, test.
- Add a module dict `UNATTENDED_EXPECT`, empty for now, mapping a command name to a dict with the keys `flags` (tokens the section must contain), `phrases` (further text it must contain) and the optional key `nested` (list of nested command names that receive `--unattended`; an absent key means an empty list). Replace the empty `UNATTENDED_COMMANDS = frozenset()` with `frozenset(UNATTENDED_EXPECT)` and update its comment and the module docstring to say "after P1".
- Add a helper `_unattended_section(name)` that returns the text from the line `## Unattended mode` up to the next line that starts with `## `, reading `Path(_THIS.COMMANDS_DIR) / f"{name}.md"`, and a helper `_check_unattended_section(text, expect)` that asserts the text contains `return-contract.yaml`, `~/.claude/WORKER-CONTRACT.md`, `--report-dir`, every token in `expect["flags"]` (matched as a whole token with `re.search(rf"(?<![\w-]){re.escape(tok)}(?![\w-])", text)`, so `-i` is not satisfied by `--interactive`), every phrase in `expect["phrases"]` and `nested/<name>-` for every name in `expect.get("nested", [])` (and no `nested/` text when that list is empty), does not contain `src/superclaude/`, and does not match the Python form of Check SCAN, `re.compile(r"\borca(-ide)?\s+(orchestration|worktree|terminal|agent)\b", re.I)` (the POSIX class of the grep form means something else in Python, so the grep text is not reused).
- Add `test_unattended_section_content` parametrized over `sorted(UNATTENDED_EXPECT)`, and `test_unattended_section_check_fails_when_token_removed` parametrized over every (command, token) pair of the dict, which removes the token from the section text (with the same whole-token pattern) and expects the helper to raise `AssertionError`. Both are empty parametrizations now and fill as tasks add entries.
- Add one self-contained negative test that builds a synthetic section in `tmp_path` and shows the helper fails when the contract path, `return-contract.yaml`, `--report-dir`, a required phrase is missing, a listed nested name has no `nested/<name>-` text, `src/superclaude/` is present, or a sentence naming `orca worktree` is present.
- Rename `test_no_command_has_unattended_mode_section_after_p0` to `test_unattended_sections_match_the_listed_commands`. It still calls `_check_no_unattended_sections`, which now compares the commands that have the section with `UNATTENDED_COMMANDS`.

Acceptance criteria:
- [T1.AC1] The six files named above exist under `./artifacts/`, and `git status --short` shows no tracked file changed by the baseline runs.
- [T1.AC2] `uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes, and `grep -c 'test_no_command_has_unattended_mode_section_after_p0' tests/skills/test_worker_contract.py` prints `0`.
- [T1.AC3] `grep -nE '^(P1_COMMANDS|UNATTENDED_EXPECT|UNATTENDED_COMMANDS)' tests/skills/test_worker_contract.py` shows all three constants, and `P1_COMMANDS` has exactly the sixteen names.
- [T1.AC4] `uv run ruff check tests/skills/test_worker_contract.py` and `uv run ruff format --check tests/skills/test_worker_contract.py` exit 0.
Global constraints: (plan `## Constraints`, plan lines 17-44, verbatim)
## Constraints

- Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` is called "the spec" below, and "spec section N" means its section N. `./source.md` is the inline brief that started this plan. The spec is the authority; where a task cites a section it names the rows the task needs. Decisions: `.dev/orca-command-refactor/decisions/APPROVED.md`, including the 2026-11-05 heartbeat decision (looser reading of spec section 7.2 step 5 condition 4; WC-10 unchanged; P0 verdict PASS). That decision changes nothing in this static plan; it governs how the later live plan reads heartbeat gaps.
- This is the static plan of Phase P1 (spec section 6, last paragraph: each phase plan has a static part and a live part). It covers AC-1.1 and AC-1.4 (spec section 7.3) and the common checks AC-C1 to AC-C6 (spec section 7.1). The live checks AC-1.2, AC-1.3, AC-1.5, AC-1.6, AC-1.7 and AC-1.8 and the P1 phase report belong to the P1 live plan, which is written after this plan's checks pass. P2 to P4 get their own plans later.
- No task in this plan commits, pushes, installs into `~/.claude`, starts an Orca worker, runs an Orca command or asks the owner a question. Between this plan and the live plan, the coordinator session asks the owner, commits and runs the install as spec section 7.2 states, outside any plan run. Nothing under the `.claude/` folder is staged, ever (repo `CLAUDE.md`, "Never Stage or Commit `.claude/` Contents"); `make sync-dev` writes only gitignored `.claude/` copies. `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing.
- `src/superclaude/` is the source of truth. Installed primitives use installed paths only: a new section or sentence never contains `src/superclaude/` and never names an Orca command (spec SA-2; Check SCAN below). The only file under `src/superclaude/core/` that describes the coordinator side is `WORKER-CONTRACT.md`, and this plan does not edit it. The brief-flag table in that file lists the P0-era constraints; the general "Report directory" rule in its section 1 already covers the extra report directory that `--unattended` needs for index-repo and init-lite, so no table row changes.
- Mirrors. UNVERIFIED item 8 of the spec is resolved by the repo's own rule (`src/superclaude/commands/README.md`, step 3): only `help.md`, `recommend.md`, `workflow.md` and `implement.md` are copied byte-for-byte to `plugins/superclaude/commands/`, and `tests/commands/test_workflow_command.py::test_plugin_mirror_matches_src` plus `tests/commands/test_routing_plugin_parity.py` pin them. Of the files this plan edits, only `workflow.md` and the `sc-workflow-protocol` skill (which has a plugin copy) are pinned, so only they are mirrored (Task 9). The other plugin command copies (brainstorm, build, document, index-repo, index, load and test are identical today; analyze, business-panel, design and explain already differ) are not touched.
- Section skeleton. Every `## Unattended mode` section is a level-2 heading written exactly like that, placed immediately before the file's first `## Boundaries` heading (business-panel.md has only `## CRITICAL BOUNDARIES` and uses that; index-repo.md has neither and the section goes after `## Output Format`; graph.md and impact.md name their own anchors in their tasks), and holds only the command's own resolutions. It contains, in this order: an opening sentence that names `~/.claude/WORKER-CONTRACT.md` as the home of the shared rules and tells the reader to read it first; the switch (applies only when `--unattended` is a standalone argument token outside any quoted argument, otherwise nothing in the section applies and no contract is written: spec SA-1 and SA-3); the report directory (exactly one of `--report-dir <dir>` or the command's own directory flag, named per task; if the command has none, `--report-dir` only; `--report-dir` follows the same path rules as the command's own directory flag where it has one: never inside `.git/` or `.codegraph/`, never under the distributable skill, agent or command folders of a `.claude/` folder, created if missing and writable; a report directory that fails them counts as no report directory known, so nothing is written there and the refusal is printed in chat only, as section 1 of `~/.claude/WORKER-CONTRACT.md` says); the contract (`<report-dir>/return-contract.yaml` written on every outcome with `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts` and `reason` when failed, naming this command's deliverables for `report_path` and `artifacts`); the person-mode refusals of this command, in every spelling the command accepts (the short form `-i`, the `=` form such as `--format=interactive` or `--mode=socratic`) (refused before any work, contract `worker_status: failed` with the refused flag in `reason`); the gate resolutions of this command (for a no-gate command, the single statement that it has none); the nested invocations of this command (or "none"); and the outward-action rule (the command pushes, commits and stages nothing under `--unattended`, spec WC-9). The section never repeats the shared rules' wording, the exact error text or the status mapping; it points to the contract file.
- Test data. `tests/skills/test_worker_contract.py` gets one entry per command in a dict `UNATTENDED_EXPECT` (Task 1 creates it empty): the command name maps to a dict with `flags` (tokens its section must contain), `phrases` (further text it must contain) and `nested` (the names of the nested commands that receive `--unattended` from this command; an empty list for every command except brainstorm). Each command task adds its own entry in the same task, so the suite is green after every task.
- Check SCAN (spec AC-C1; run after every task that edits a command, skill or core file). Pass: prints nothing.

  ```sh
  grep -rniE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' \
    src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \
    src/superclaude/hooks src/superclaude/templates plugins/superclaude \
    | grep -v '^src/superclaude/skills/ccsession-tag/' \
    | grep -v '^src/superclaude/core/WORKER-CONTRACT\.md:' \
    | grep -v '^src/superclaude/core/HOW-WE-WORK\.md:' \
    | grep -v '^plugins/superclaude/core/WORKER-CONTRACT\.md:' \
    | grep -v '^plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK\.md:'
  ```

- Check ADDITIVE (spec AC-C5 / SA-4). For every command file a task edits, `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/commands/<name>.md | awk '$2 != 0'` prints nothing. Edits to command files are added lines; an existing line is never reworded. The only two command files exempt are `business-panel.md` (the frontmatter move deletes the fence lines) and `load.md` (the usage-line fix replaces one line); their tasks say so. Skill and test files have no such rule.
- Check WRITEVERB (spec AC-0.9). New text in any command or skill file must not contain the audit's write-verb phrases: `git add`, `git commit`, `git push`, `git merge`, `git stash`, `git update-ref`, `git worktree add` or `remove`, `gh pr`, `gh api`. The test `tests/skills/test_worker_contract.py::test_every_write_verb_hit_is_classified` and `::test_classification_table_has_no_stale_entries` must still pass, so no classified line is edited. The one classified P1 line is the `.dev/tasks/` staging sentence in `src/superclaude/skills/sc-workflow-protocol/SKILL.md` (category `deferred:P1`); it stays word for word.
- Test commands. Every pytest run in this plan passes `-p no:cacheprovider`. After every test, lint or sync run, `git status --short` shows no tracked file changed by the run itself. The wider test run always passes `--ignore=tests/cli/eval/test_perf_home_setup.py`, because that test rewrites a tracked evidence file. UV for every Python command; no bare `python`, `python3` or `pip`.
- Pre-existing tests that read the files this plan edits, and must still pass: `tests/commands/test_workflow_command.py`, `tests/commands/test_graph_command.py`, `tests/commands/test_impact_command.py`, `tests/commands/test_routing_plugin_parity.py`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_codegraph_adoption.py`, `tests/skills/test_primitive_dual_surface_lookup.py`, `tests/skills/test_tier2_tavily_consistency.py`, `tests/skills/test_repo_inventory_nongit.py`, `tests/skills/test_worker_contract.py`, `tests/cli_portify/test_brainstorm_gaps.py`, `tests/cli/test_init_lite.py`, `tests/unit/test_cli_install.py`, `tests/roadmap/test_threshold_registry.py`, `tests/core/test_how_we_work_routing_table.py` and `tests/recommend/test_routing_refresh.py`. The graph and impact tests pin frontmatter, section order and word lists; the workflow tests pin the `--output` retirement (every line of the command, skill or a ref that contains `--output` must also contain `retired`, `E-LEGACY` or `Never`).
- Decisions this plan makes where the spec is silent or ambiguous (each is also reported to the coordinator). D-P1-1: the spec can be read two ways for graph and impact. Its worker field `command` is the exact command line, but their own contracts already write a `command` key holding the short name (`graph`, `impact`). This plan keeps the existing key and value (spec WC-4: an existing contract keeps every existing field), counts it as the worker `command` field and adds no second key; the owner approved this on 2026-11-05 (decisions file, section "P1 owner decisions"). D-P1-2: for the seven report-style no-gate commands (analyze, build, design, explain, index, test, business-panel) `--output <file>` is new and optional; under `--unattended` without it the report goes to `<report-dir>/<name>-report.md`, so the contract always has a `report_path`. D-P1-3: brainstorm's own status `dry-run` maps to `worker_status: succeeded` with `report_path: null` (the spec's mapping list lacks it). D-P1-4: the nested propagation rule (spec section 2.1) is applied to brainstorm: its adversarial call and its `/sc:analyze` enrichment get `--unattended` and a nested report directory; research enrichment and the `tasklist` and `task` handoffs are skipped and recorded. The owner confirmed this on 2026-11-05 after an adversarial debate (decisions file, section "P1 owner decisions"): spec section 2.1's nested rule applies to every called command that accepts the flag in this phase, and the spec's "from P2" wording covers research enrichment only. D-P1-5: workflow skips a `--handoff implement` under `--unattended` (implement has gates and accepts the flag only in P4) and records it in the package contract as `partial` with an `unresolved` line; its reflect step runs as today (gate-free without `--remediate`). D-P1-6: graph refuses `init` under `--unattended`. D-P1-7: document requires an explicit `--output` for the external, api and guide types under `--unattended`. D-P1-8: a failing test suite is a verdict in the `/sc:test` report, not a failed run; `worker_status` is `failed` only when the runner could not run. D-P1-9: adversarial's `report_path` is its merged output (null when the merge was not reached). D-P1-10: cleanup-audit's `--pass all` final report is named `.claude-audit/final-report.md`. D-P1-11: init-lite writes the worker contract also on `--dry-run`, so the exception in its skill covers Safety Invariant 2 as well as 3 (the spec row names only 3). D-P1-12: a command's consent line is never answered under `--unattended` by assuming consent: analyze modifies no source and design changes no architecture; `/sc:test --fix` is the caller's consent for non-destructive fixes only, and a destructive change to a test file is never made; `/sc:index` overwrites no existing manual documentation and writes only the `--output` path the caller passed (or the default report file).
- Nothing in this plan edits `WORKER-CONTRACT.md`, `HOW-WE-WORK.md`, `KNOWN_CORE_FILES`, any agent file, any other command or skill, or any Python module under `src/superclaude/cli/`.
Start sha: 35dc0c5eda74b884f51938ea9ad669361ca2a8b4
Diff against the start snapshot: diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index a61828ba..18576e48 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -1,9 +1,11 @@
-"""Static checks for the Orca worker contract (~/.claude/WORKER-CONTRACT.md), Phase P0.
+"""Static checks for the Orca worker contract (~/.claude/WORKER-CONTRACT.md), Phases P0 and P1.
 
 The contract file is read through the module-level CONTRACT_PATH and the command
 files through COMMANDS_DIR, so the negative tests can point both at a tmp_path copy.
 Each rule is pinned by phrases that carry its meaning, not only its label. The
 phrases are copied here as data; the tests never read the plan's artifacts.
+After P1 the commands that have an `## Unattended mode` section are exactly the
+keys of UNATTENDED_EXPECT, and each section is checked against its entry there.
 CI-safe, no network.
 """
 
@@ -250,9 +252,36 @@ NEVER_AS_WORKER = (
     "/sc:pr-submit",
 )
 
-# Commands with an `## Unattended mode` section after P0 (./source.md section 6
-# table: none). Later phases extend this set.
-UNATTENDED_COMMANDS: frozenset = frozenset()
+# The sixteen commands that get an `## Unattended mode` section in P1, in the order
+# of the spec's phase table.
+P1_COMMANDS = (
+    "adversarial",
+    "brainstorm",
+    "cleanup-audit",
+    "graph",
+    "impact",
+    "index-repo",
+    "init-lite",
+    "workflow",
+    "analyze",
+    "build",
+    "business-panel",
+    "design",
+    "document",
+    "explain",
+    "index",
+    "test",
+)
+
+# command -> {"flags": tokens its section must contain (whole tokens),
+#             "phrases": further text it must contain,
+#             "nested": optional list of nested commands that receive --unattended}.
+# Each command task adds its own entry in the task that converts the command.
+UNATTENDED_EXPECT: dict = {}
+
+# Commands with an `## Unattended mode` section after P1 (./source.md section 6
+# table). Later phases extend this set.
+UNATTENDED_COMMANDS: frozenset = frozenset(UNATTENDED_EXPECT)
 
 _TEMPLATE_HEADING = "## 5. Coordinator brief template"
 
@@ -348,6 +377,68 @@ def _check_no_unattended_sections() -> None:
     )
 
 
+# Python form of Check SCAN (the grep form's POSIX class means something else in re).
+_ORCA_NAME_RE = re.compile(
+    r"\borca(-ide)?\s+(orchestration|worktree|terminal|agent)\b", re.I
+)
+
+
+def _token_re(tok: str) -> re.Pattern:
+    """A whole-token pattern: `-i` is not found inside `--interactive`."""
+    return re.compile(rf"(?<![\w-]){re.escape(tok)}(?![\w-])")
+
+
+def _unattended_section(name: str) -> str:
+    """The text of `## Unattended mode` up to the next `## ` heading."""
+    lines = (
+        (Path(_THIS.COMMANDS_DIR) / f"{name}.md").read_text(encoding="utf-8")
+    ).splitlines()
+    start = next(
+        (i for i, ln in enumerate(lines) if ln.rstrip() == "## Unattended mode"), None
+    )
+    assert start is not None, f"{name}: no `## Unattended mode` section"
+    end = next(
+        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
+        len(lines),
+    )
+    return "\n".join(lines[start:end])
+
+
+def _check_unattended_section(text: str, expect: dict) -> None:
+    for need in (
+        "return-contract.yaml",
+        "~/.claude/WORKER-CONTRACT.md",
+        "--report-dir",
+    ):
+        assert need in text, f"section lacks {need!r}"
+    for tok in expect.get("flags", []):
+        assert _token_re(tok).search(text), f"section lacks flag {tok!r}"
+    for phrase in expect.get("phrases", []):
+        assert phrase in text, f"section lacks {phrase!r}"
+    nested = expect.get("nested", [])
+    for name in nested:
+        assert f"nested/{name}-" in text, f"section lacks nested/{name}-"
+    if not nested:
+        assert "nested/" not in text, "section names a nested directory"
+    assert "src/superclaude/" not in text, "section names a src/superclaude/ path"
+    assert not _ORCA_NAME_RE.search(text), "section names an Orca command"
+
+
+def _removals() -> list:
+    """Every (command, kind, token) of UNATTENDED_EXPECT, for the removed-token tests."""
+    out = []
+    for cmd in sorted(UNATTENDED_EXPECT):
+        entry = UNATTENDED_EXPECT[cmd]
+        out += [(cmd, "flag", t) for t in entry.get("flags", [])]
+        out += [(cmd, "phrase", t) for t in entry.get("phrases", [])]
+        out += [(cmd, "nested", f"nested/{n}-") for n in entry.get("nested", [])]
+    return out
+
+
+def _remove(text: str, kind: str, tok: str) -> str:
+    return _token_re(tok).sub("", text) if kind == "flag" else text.replace(tok, "")
+
+
 # --- positive checks -------------------------------------------------------
 
 
@@ -364,10 +455,27 @@ def test_brief_template_puts_guard_line_before_first_command_line():
     _check_guard_before_command(_contract())
 
 
-def test_no_command_has_unattended_mode_section_after_p0():
+def test_unattended_sections_match_the_listed_commands():
     _check_no_unattended_sections()
 
 
+@pytest.mark.parametrize("cmd", sorted(UNATTENDED_EXPECT))
+def test_unattended_section_content(cmd):
+    _check_unattended_section(_unattended_section(cmd), UNATTENDED_EXPECT[cmd])
+
+
+@pytest.mark.parametrize(
+    ("cmd", "kind", "tok"),
+    _removals(),
+    ids=[f"{c}:{k}:{t}" for c, k, t in _removals()],
+)
+def test_unattended_section_check_fails_when_token_removed(cmd, kind, tok):
+    text = _unattended_section(cmd)
+    _check_unattended_section(text, UNATTENDED_EXPECT[cmd])
+    with pytest.raises(AssertionError):
+        _check_unattended_section(_remove(text, kind, tok), UNATTENDED_EXPECT[cmd])
+
+
 def test_every_repo_setup_line_is_gated():
     _check_repo_setup_gated(_contract())
 
@@ -464,6 +572,80 @@ def test_unattended_section_check_fails_on_unlisted_command(tmp_path, monkeypatc
         _check_no_unattended_sections()
 
 
+_SYNTHETIC_SECTION = (
+    "## Unattended mode\n\n"
+    "Read ~/.claude/WORKER-CONTRACT.md first. Report directory: --report-dir <dir>;\n"
+    "the contract is <report-dir>/return-contract.yaml. Refuses --interactive.\n"
+    "Nested: nested/analyze-<n>/ gets the flag. It has the gate phrase alpha-gate.\n"
+)
+_SYNTHETIC_EXPECT = {
+    "flags": ["-i", "--interactive"],
+    "phrases": ["alpha-gate"],
+    "nested": ["analyze"],
+}
+
+
+def _synthetic_section(tmp_path, monkeypatch, body: str) -> str:
+    cmds = tmp_path / "commands"
+    cmds.mkdir(exist_ok=True)
+    (cmds / "synthetic.md").write_text(
+        "# synthetic\n\n"
+        + body
+        + "\n## Boundaries\n\nsrc/superclaude/ here is outside.\n",
+        encoding="utf-8",
+    )
+    monkeypatch.setattr(_THIS, "COMMANDS_DIR", cmds)
+    return _unattended_section("synthetic")
+
+
+def test_unattended_section_helper_reads_only_its_own_section(tmp_path, monkeypatch):
+    # `-i` is not listed in the synthetic section, and `--interactive` does not satisfy it.
+    text = _synthetic_section(tmp_path, monkeypatch, _SYNTHETIC_SECTION)
+    assert "src/superclaude/" not in text
+    with pytest.raises(AssertionError):
+        _check_unattended_section(text, _SYNTHETIC_EXPECT)
+    ok = dict(_SYNTHETIC_EXPECT, flags=["--interactive"])
+    _check_unattended_section(text, ok)
+    _check_unattended_section(text + " -i\n", _SYNTHETIC_EXPECT)
+
+
+@pytest.mark.parametrize(
+    "mutate",
+    [
+        lambda s: s.replace("return-contract.yaml", "the-file"),
+        lambda s: s.replace("~/.claude/WORKER-CONTRACT.md", "the-contract"),
+        lambda s: s.replace("--report-dir", "--dir"),
+        lambda s: s.replace("alpha-gate", "beta"),
+        lambda s: s.replace("nested/analyze-", "nested/other-"),
+        lambda s: s + "See src/superclaude/skills/x.\n",
+        lambda s: s + "Then run orca worktree create.\n",
+    ],
+    ids=[
+        "no-contract-file",
+        "no-contract-path",
+        "no-report-dir",
+        "no-phrase",
+        "no-nested-name",
+        "src-path",
+        "orca-name",
+    ],
+)
+def test_unattended_section_check_fails_on_synthetic_defects(
+    tmp_path, monkeypatch, mutate
+):
+    ok = dict(_SYNTHETIC_EXPECT, flags=["--interactive"])
+    good = _synthetic_section(tmp_path, monkeypatch, _SYNTHETIC_SECTION)
+    _check_unattended_section(good, ok)
+    with pytest.raises(AssertionError):
+        _check_unattended_section(mutate(good), ok)
+
+
+def test_unattended_section_check_forbids_nested_text_without_a_nested_list():
+    text = _SYNTHETIC_SECTION
+    with pytest.raises(AssertionError):
+        _check_unattended_section(text, {"flags": [], "phrases": []})
+
+
 # --- AC-0.9: git and GitHub write-verb audit -------------------------------
 #
 # Scans the installed primitives' source for git and gh write verbs. The hit

Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

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
