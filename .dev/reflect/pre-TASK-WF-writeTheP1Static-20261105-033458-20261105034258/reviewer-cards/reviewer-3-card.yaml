reviewer: 3
persona: refactorer
model: opus
verdict: PARTIAL
note: persisted by the orchestrator from the reviewer's returned card (the agent hit its turn limit once and was resumed to return the card); claims shortened, evidence kept. t1_ref is null on every finding because the reviewer did not see the T1 finding ids.
findings:
  - id: R3-01
    t1_ref: F-001
    stance: confirm
    title: Task 15's path-list check will fail on files that were already changed before the plan
    severity: should-fix
    claim: >-
      The worktree already has M .dev/orca-command-refactor/decisions/APPROVED.md and the untracked .dev/reflect
      folder; both show in git status --short, so a correct run fails the equality or the executor lists paths it did
      not change.
    evidence:
      - 'plan:289 "The repo-path list in the report equals the output of `git status --short` for the working tree, ignoring paths under `.dev/tasks/` and the `.claude/` folder."'
      - 'plan:284 "the exact list of repo paths this plan created or changed"'
    tag: Grounded
    fix: Save git status --short as a baseline in Task 1 and compare against paths new since it, or scope the comparison to src tests plugins.

  - id: R3-02
    t1_ref: null
    stance: new
    title: init-lite hands its work to the Python CLI, and the plan never keeps the new flags away from it or says who writes the contract
    severity: should-fix
    claim: >-
      The skill's preferred path runs superclaude init-lite with the flags it was given, and the command's Activation
      passes a fixed flag list. Task 8 adds a --report-dir row to the skill's Inputs table but not to the Activation
      pass-through, and does not say the skill must keep both flags off the CLI call (src/superclaude/cli/ is not
      editable) or that the skill itself writes <report-dir>/return-contract.yaml, including on --dry-run.
    evidence:
      - 'src/superclaude/skills/sc-init-lite-protocol/SKILL.md:57 "Preferred implementation: shell out to `superclaude init-lite` with the resolved flags via Bash and relay its output."'
      - 'src/superclaude/commands/init-lite.md:52 "Pass the following context (user-provided flags, pass-through):"'
      - 'plan:44 "or any Python module under `src/superclaude/cli/`."'
    tag: Grounded
    fix: >-
      In Task 8 add Activation bullets (added lines only) passing --unattended and --report-dir; state in the skill that
      both flags are removed from the CLI call and the skill writes the worker contract after the CLI returns on every
      outcome including --dry-run; add a grep acceptance check for each.

  - id: R3-03
    t1_ref: null
    stance: new
    title: graph and impact do not say where the worker contract goes when the brief passes --report-dir
    severity: should-fix
    claim: >-
      Tasks 4 and 5 accept --output-dir or --report-dir but only say the worker fields are added to the existing
      <output-dir>/return-contract.yaml. Under WC-4 the --report-dir case needs a separate
      <report-dir>/return-contract.yaml listing the command's own contract in artifacts. For graph the screen-only
      default writes no contract of its own. Task 3 states both cases; graph and impact leave the executor to guess.
    evidence:
      - 'plan:109 and plan:124 (worker fields added to the existing <output-dir>/return-contract.yaml)'
      - 'spec:72 "Where its own contract lives elsewhere ... the worker contract at `<report-dir>/return-contract.yaml` lists that file in `artifacts`"'
    tag: Grounded
    fix: Copy brainstorm's two-case wording into Tasks 4 and 5 and add the --report-dir placement to the UNATTENDED_EXPECT phrases.

  - id: R3-04
    t1_ref: null
    stance: new
    title: Task 14's nested-propagation test has no rule for what counts as "names a nested invocation"
    severity: should-fix
    claim: >-
      Task 14 says every command whose section names a nested invocation (today only brainstorm) writes
      nested/<command>-<n>/. Task 9's workflow section names its reflect step, which runs without the flag, so a
      literal check catches workflow and fails, or the executor invents a rule.
    evidence:
      - 'plan:261 "Nested propagation: every command whose section names a nested invocation (today only brainstorm) writes `nested/<command>-<n>/` for it."'
      - 'plan:184 "the reflect step runs as today, without `--unattended` and without `--remediate`"'
      - 'src/superclaude/skills/sc-workflow-protocol/SKILL.md:58'
    tag: Grounded
    fix: Add a data field UNATTENDED_EXPECT[cmd]["nested"] listing the nested commands that receive the flag (brainstorm: analyze, adversarial) and assert nested/<c>- only for those.

  - id: R3-05
    t1_ref: null
    stance: new
    title: The lint comparison does not say whether a new size warning counts as a violation
    severity: minor
    claim: >-
      make lint warns (exit 0) for a command file over 200 lines. adversarial.md is about 183 lines and grows in Task
      2; brainstorm.md is already over 200. "No new violation" could judge a correct run FAIL.
    evidence:
      - 'Makefile:406 "elif [ \"$$lines\" -gt 200 ]; then"'
      - 'plan:281 "no new violation and no new unformatted file"'
    tag: Grounded
    fix: State that a violation means a lint ERROR or a ruff finding; new Check-3 size warnings are recorded and do not fail.

  - id: R3-06
    t1_ref: null
    stance: new
    title: The pre-existing test list and the baseline runs do not match, and one named test is unrelated
    severity: minor
    claim: >-
      Task 6 runs tests/test_cleanup_audit_structure.py, which checks the Python pipeline under
      src/superclaude/cli/cleanup_audit, not the edited Markdown, and it is in neither baseline run. Task 15 says the
      wider run shows all sixteen pre-existing files of the Constraints, but seven of them are under tests/skills/,
      which the wider run does not include.
    evidence:
      - 'tests/test_cleanup_audit_structure.py:17 "BASE_DIR = Path(\"src/superclaude/cli/cleanup_audit\")"'
      - 'plan:53 "uv run pytest tests/core tests/commands tests/recommend tests/cli tests/cli_portify tests/unit tests/roadmap"'
      - 'plan:276 "which also lists the sixteen pre-existing test files of the Constraints and shows each passing"'
    tag: Grounded
    fix: Drop tests/test_cleanup_audit_structure.py from Task 6 or add it to the baseline; have Task 15 read the sixteen files from the combined AC-C3 and wider results.

  - id: R3-07
    t1_ref: null
    stance: new
    title: The --output rule in the workflow tests also covers the refs Task 9 edits, but the plan states it only for workflow.md
    severity: minor
    claim: >-
      test_output_flag_is_retired_everywhere checks every line of the command, the skill and all five refs, and the
      parse ref must not contain E-MISSING-DIR. Task 9 states the retired/Never rule only for the workflow.md section
      although it adds a Worker flags section to input-parse.md and a missing-directory error.
    evidence:
      - 'tests/commands/test_workflow_command.py:124 "assert re.search(r\"retired|E-LEGACY|Never\", line), (name, line)"'
      - 'tests/commands/test_workflow_command.py:127 "assert \"E-OUTPUT-PATH\" not in parse and \"E-MISSING-DIR\" not in parse"'
    tag: Grounded
    fix: In Task 9 apply the --output rule to the SKILL.md and refs edits too and forbid naming the error E-MISSING-DIR.

  - id: R3-08
    t1_ref: null
    stance: new
    title: '"Final boundaries heading" in the Constraints disagrees with the tasks for files that have two boundaries headings'
    severity: minor
    claim: >-
      brainstorm.md, workflow.md and cleanup-audit.md have ## Boundaries and later ## CRITICAL BOUNDARIES. The
      Constraints say "final boundaries heading" but the tasks say "before ## Boundaries".
    evidence:
      - 'src/superclaude/commands/brainstorm.md:145 "## Boundaries"'
      - 'src/superclaude/commands/brainstorm.md:177 "## CRITICAL BOUNDARIES"'
      - 'plan:24 "placed immediately before the file''s final boundaries heading"'
    tag: Grounded
    fix: Replace "final boundaries heading" with "the first ## Boundaries heading".

  - id: R3-09
    t1_ref: null
    stance: new
    title: New init-lite text contradicts an existing Boundaries line that cannot be reworded
    severity: minor
    claim: >-
      Task 8 says the contract is written also on --dry-run; the command's Will Not still says "Write anything when
      --dry-run is set", and the additive-only rule keeps that line.
    evidence:
      - 'src/superclaude/commands/init-lite.md:94 "- Write anything when `--dry-run` is set"'
    tag: Grounded
    fix: Add an "except under --unattended, the worker contract" line next to init-lite.md:94, as Task 6 does for cleanup-audit.

  - id: R3-10
    t1_ref: null
    stance: new
    title: The helper reuses Check SCAN's POSIX regex, which Python does not read the same way
    severity: minor
    claim: >-
      The regex uses [[:space:]] and grep's -i flag; Python re reads [[:space:]] as a different character set, so the
      Orca check in the helper would quietly not work.
    evidence:
      - 'plan:29 "grep -rniE ''\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b''"'
      - 'plan:60 "and does not match the Check SCAN regular expression"'
    tag: Grounded
    fix: Give the Python form re.compile(r"\borca(-ide)?\s+(orchestration|worktree|terminal|agent)\b", re.I) and add a negative case.

self_audit:
  - Read the whole plan, source.md, spec sections 2.1, 2.2, 3.1, 3.2, 5, 6 and 7.1-7.4.
  - Checked the test_worker_contract.py harness and read the graph, impact and workflow command tests in full.
  - Checked the heading layout of all 17 command files and brainstorm's Wave 2A, 3 and 4.
  - Checked the init-lite, cleanup-audit and adversarial return-contract sections, the Makefile lint and sync targets and the plugin parity tests.
  - Not verified - whether local master is up to date for the merge-base additive check, the AC-C6 profile glob behaviour, and the T1 finding ids.
