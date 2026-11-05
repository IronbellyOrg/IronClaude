1c738296ed9aca394c1fa18bf48a877834d8553f
Review one task for spec compliance.

Task brief: Task T14 (plan file /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md, lines 256-267); AC ids T14.AC1 to T14.AC3 are the bullets under `Acceptance criteria:` in source order.

## Task 14: Pin the full P1 command set, AC-1.4 and the nested propagation text in `tests/skills/test_worker_contract.py`

Depends on: Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13

Files: `tests/skills/test_worker_contract.py` only; spec AC-1.1 and AC-1.4.

Add these tests. A completeness test: `set(UNATTENDED_EXPECT) == set(P1_COMMANDS)` and `len(P1_COMMANDS) == 16`, and for each of `load`, `pr-submit`, `agent`, `git`, `help`, `pm`, `spawn`, `swarm-wizard` and `issue` the command file, when it exists, has no section. The existing set-equality test `test_unattended_sections_match_the_listed_commands` already fails for any other command that has the section, so the P2 to P4 commands need no list here. AC-1.4: the adversarial skill's `SKILL.md` contains `adversarial/return-contract.yaml`; the adversarial section names `<output>/return-contract.yaml` and says it lists that file in `artifacts`; the workflow ref `refs/return-contract.md` states the worker contract is written in `--report-dir` for pre-creation STOPs. Brainstorm: the section contains `research enrichment is off` (AC-1.1). Nested propagation: for every command, each name in `UNATTENDED_EXPECT[cmd].get("nested", [])` (brainstorm: `analyze` and `adversarial`; every other command: none, so workflow's reflect step, which runs without the flag, is not listed) appears in its section as `nested/<name>-`, and a command with no nested names has no `nested/` text in its section. A removed-phrase negative test for each of the AC-1.4 assertions. Keep the existing P0 contract assertions (the brief guard's four refusal conditions, the three exact reason texts, the case-3 prefix, the never-as-worker list, the nested propagation rule and the guard line before the `Command:` lines) unchanged: they are already pinned by `RULE_PHRASES` and must still pass.

Acceptance criteria:
- [T14.AC1] `uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes, and the output shows a `test_unattended_section_content` case for each of the sixteen commands (`uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider -k test_unattended_section_content --collect-only | grep -c 'test_unattended_section_content\['` prints `16`).
- [T14.AC2] `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` names `<output>/adversarial/return-contract.yaml`, and `grep -n 'return-contract.yaml' src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md` shows the worker-contract section (spec AC-1.4).
- [T14.AC3] `uv run ruff check tests/skills/test_worker_contract.py` and `uv run ruff format --check tests/skills/test_worker_contract.py` exit 0.
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
Start sha: 1c738296ed9aca394c1fa18bf48a877834d8553f
Diff against the start snapshot: diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 8d703a76..06c13334 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -791,6 +791,207 @@ def test_unattended_section_check_forbids_nested_text_without_a_nested_list():
         _check_unattended_section(text, {"flags": [], "phrases": []})
 
 
+# --- full P1 set, AC-1.4 and nested propagation ----------------------------
+
+# Commands that never get the section in P1 (later phases extend the converted set;
+# the set-equality test above already fails for any other command with a section).
+NOT_CONVERTED_IN_P1 = (
+    "load",
+    "pr-submit",
+    "agent",
+    "git",
+    "help",
+    "pm",
+    "spawn",
+    "swarm-wizard",
+    "issue",
+)
+
+_ADVERSARIAL_SKILL = _REPO / "src/superclaude/skills/sc-adversarial-protocol/SKILL.md"
+_WORKFLOW_RETURN_REF = (
+    _REPO / "src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md"
+)
+_ADVERSARIAL_OWN_CONTRACT = "<output>/adversarial/return-contract.yaml"
+_WORKER_CONTRACT_HEADING = "## Worker contract (`--unattended`)"
+
+
+def _check_p1_set(commands, expect) -> None:
+    assert len(commands) == 16, f"P1 lists {len(commands)} commands, not 16"
+    assert len(set(commands)) == 16, "P1_COMMANDS has a duplicate"
+    assert set(expect) == set(commands), (
+        f"UNATTENDED_EXPECT and P1_COMMANDS differ: {sorted(set(expect) ^ set(commands))}"
+    )
+
+
+def _check_no_section_in(names) -> None:
+    for name in names:
+        path = Path(_THIS.COMMANDS_DIR) / f"{name}.md"
+        if path.exists():
+            text = path.read_text(encoding="utf-8")
+            assert not re.search(r"^## Unattended mode\s*$", text, re.M), (
+                f"{name} has an `## Unattended mode` section"
+            )
+
+
+def _check_adversarial_skill(text: str) -> None:
+    assert _ADVERSARIAL_OWN_CONTRACT in text, f"skill lacks {_ADVERSARIAL_OWN_CONTRACT}"
+
+
+def _check_adversarial_section(section: str) -> None:
+    assert "<output>/return-contract.yaml" in section, "section lacks the worker path"
+    assert re.search(
+        r"lists[^.\n]*`"
+        + re.escape(_ADVERSARIAL_OWN_CONTRACT)
+        + r"`[^.\n]*`artifacts`",
+        section,
+    ), "section does not say the worker contract lists the own contract in `artifacts`"
+
+
+def _check_workflow_ref(text: str) -> None:
+    assert _WORKER_CONTRACT_HEADING in text, "ref lacks the worker contract section"
+    section = text.split(_WORKER_CONTRACT_HEADING, 1)[1].split("\n## ", 1)[0]
+    assert "<report-dir>/return-contract.yaml" in section, "ref lacks the report path"
+    assert "--report-dir" in section, "ref does not tie the file to --report-dir"
+    assert re.search(r"pre-creation STOP\s*→\s*`failed`", section), (
+        "ref does not cover pre-creation STOPs"
+    )
+
+
+def _check_brainstorm_research_off(section: str) -> None:
+    assert "research enrichment is off" in section, "section lacks the research line"
+
+
+def _check_nested_text(section: str, expect: dict) -> None:
+    nested = expect.get("nested", [])
+    for name in nested:
+        assert f"nested/{name}-" in section, f"section lacks nested/{name}-"
+    if not nested:
+        assert "nested/" not in section, "section names a nested directory"
+
+
+def _read(path: Path) -> str:
+    return path.read_text(encoding="utf-8")
+
+
+# (id, text getter, check, phrases whose removal must make the check fail)
+_AC14_CASES = (
+    (
+        "adversarial-skill",
+        lambda: _read(_ADVERSARIAL_SKILL),
+        _check_adversarial_skill,
+        [_ADVERSARIAL_OWN_CONTRACT],
+    ),
+    (
+        "adversarial-section",
+        lambda: _unattended_section("adversarial"),
+        _check_adversarial_section,
+        ["<output>/return-contract.yaml", "lists", "`artifacts`"],
+    ),
+    (
+        "workflow-ref",
+        lambda: _read(_WORKFLOW_RETURN_REF),
+        _check_workflow_ref,
+        [
+            _WORKER_CONTRACT_HEADING,
+            "<report-dir>/return-contract.yaml",
+            "--report-dir",
+            "pre-creation STOP",
+        ],
+    ),
+    (
+        "brainstorm-section",
+        lambda: _unattended_section("brainstorm"),
+        _check_brainstorm_research_off,
+        ["research enrichment is off"],
+    ),
+)
+_AC14_REMOVALS = [
+    (case, getter, check, phrase)
+    for case, getter, check, phrases in _AC14_CASES
+    for phrase in phrases
+]
+
+
+def test_p1_command_set_is_complete():
+    _check_p1_set(P1_COMMANDS, UNATTENDED_EXPECT)
+    for name in P1_COMMANDS:
+        assert (Path(_THIS.COMMANDS_DIR) / f"{name}.md").exists(), name
+
+
+def test_p1_set_check_fails_on_a_missing_extra_or_repeated_command():
+    with pytest.raises(AssertionError):
+        _check_p1_set(P1_COMMANDS[:-1], UNATTENDED_EXPECT)
+    with pytest.raises(AssertionError):
+        _check_p1_set(P1_COMMANDS + ("extra",), UNATTENDED_EXPECT)
+    with pytest.raises(AssertionError):
+        _check_p1_set(P1_COMMANDS[:-1] + (P1_COMMANDS[0],), UNATTENDED_EXPECT)
+    without_test = {k: v for k, v in UNATTENDED_EXPECT.items() if k != "test"}
+    with pytest.raises(AssertionError):
+        _check_p1_set(P1_COMMANDS, without_test)
+    with pytest.raises(AssertionError):
+        _check_p1_set(P1_COMMANDS, dict(UNATTENDED_EXPECT, extra={}))
+
+
+@pytest.mark.parametrize("name", NOT_CONVERTED_IN_P1)
+def test_unconverted_command_has_no_unattended_section(name):
+    _check_no_section_in([name])
+
+
+def test_no_section_check_fails_when_an_unconverted_command_has_one(
+    tmp_path, monkeypatch
+):
+    cmds = tmp_path / "commands"
+    cmds.mkdir()
+    (cmds / "load.md").write_text(
+        "# load\n\n## Unattended mode\n\nx\n", encoding="utf-8"
+    )
+    monkeypatch.setattr(_THIS, "COMMANDS_DIR", cmds)
+    with pytest.raises(AssertionError):
+        _check_no_section_in(["load"])
+    # A command whose file does not exist is skipped.
+    _check_no_section_in(["issue"])
+
+
+@pytest.mark.parametrize(
+    ("case", "getter", "check"),
+    [(c[0], c[1], c[2]) for c in _AC14_CASES],
+    ids=[c[0] for c in _AC14_CASES],
+)
+def test_ac_1_4_assertion_holds(case, getter, check):
+    check(getter())
+
+
+@pytest.mark.parametrize(
+    ("case", "getter", "check", "phrase"),
+    _AC14_REMOVALS,
+    ids=[f"{c}:{p}" for c, _, _, p in _AC14_REMOVALS],
+)
+def test_ac_1_4_check_fails_when_phrase_removed(case, getter, check, phrase):
+    text = getter()
+    check(text)
+    with pytest.raises(AssertionError):
+        check(text.replace(phrase, ""))
+
+
+@pytest.mark.parametrize("cmd", sorted(UNATTENDED_EXPECT))
+def test_nested_propagation_text_matches_the_nested_list(cmd):
+    _check_nested_text(_unattended_section(cmd), UNATTENDED_EXPECT[cmd])
+
+
+def test_only_brainstorm_lists_nested_commands():
+    listed = {c: e["nested"] for c, e in UNATTENDED_EXPECT.items() if e.get("nested")}
+    assert listed == {"brainstorm": ["analyze", "adversarial"]}
+
+
+def test_nested_check_fails_on_nested_text_without_a_nested_list():
+    # workflow's reflect step runs without the flag, so workflow lists no nested name.
+    section = _unattended_section("workflow")
+    expect = UNATTENDED_EXPECT["workflow"]
+    _check_nested_text(section, expect)
+    with pytest.raises(AssertionError):
+        _check_nested_text(section + "\nnested/reflect-<n>/\n", expect)
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
