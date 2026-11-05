reviewer: 1
persona: analyzer
model: sonnet
verdict: FAIL
note: persisted by the orchestrator from the reviewer's returned card; claims shortened, evidence kept.
findings:
  - id: R1-01
    t1_ref: null
    stance: new
    title: Task 4 and Task 5 never make the graph and impact skills accept --unattended or --report-dir, or write the contract for --report-dir
    severity: blocking
    claim: >-
      Both commands pass flags to their skill unchanged, and both skills have a closed flag table. The impact skill
      validates every flag in step 1 and answers bad flags with a blocked status; the graph skill's table is closed
      too. Both skills write the contract only when --output-dir is set. The plan edits only the contract-field rows
      and the Will Not write line. It does not add --unattended or --report-dir to the flag tables, to graph G-O, or
      to impact step 10, and it does not widen impact's write scope. So impact with --unattended --report-dir D is
      likely to end blocked, and nothing says who writes <report-dir>/return-contract.yaml or where impact.md goes
      under --report-dir. The static tests only grep text and cannot catch it; AC-1.2 would fail later.
    evidence:
      - 'src/superclaude/skills/sc-impact-protocol/SKILL.md:19-30 "## 1. Flags (step 1 validates them)" (no --unattended or --report-dir row)'
      - 'src/superclaude/skills/sc-impact-protocol/SKILL.md:177 "| bad flags | step 1 | blocked |"'
      - 'src/superclaude/skills/sc-impact-protocol/SKILL.md:182 "Write and Edit touch only `impact.md` and `return-contract.yaml` under `--output-dir`"'
      - 'src/superclaude/commands/impact.md:45 "Pass the user''s arguments unchanged."'
      - 'src/superclaude/skills/sc-graph-protocol/SKILL.md:23-28 (closed flag table)'
      - 'src/superclaude/skills/sc-graph-protocol/SKILL.md:64 "If `--output-dir` is set, write `<output-dir>/return-contract.yaml`."'
      - 'src/superclaude/skills/sc-graph-protocol/SKILL.md:85 "## `return-contract.yaml` (only with `--output-dir`)"'
      - 'src/superclaude/commands/graph.md:42 "Pass the user''s subcommand and flags unchanged."'
      - 'plan:111 and plan:126 (Task 4 and 5 skill edits are table rows only)'
    tag: Grounded
    fix: >-
      In Tasks 4 and 5, add --unattended and --report-dir to each skill's flag table (standalone-token parse, exactly
      one report directory, --report-dir treated as the contract directory). Change graph G-O and the "(only with
      --output-dir)" heading, and impact step 10, so the contract is written when --unattended and a report
      directory are given. Update impact's write-scope sentence. State where impact.md lands under --report-dir. Add
      a test that each skill's flag table names both flags.

  - id: R1-02
    t1_ref: null
    stance: new
    title: init-lite shells out to a strict click CLI that rejects --unattended and --report-dir; the plan does not say they stay out of the pass-through
    severity: should-fix
    claim: >-
      The skill's preferred path runs `superclaude init-lite` with the resolved flags. The CLI has six click options
      and no unknown-option allowance. Task 8 adds the two flags to the command and skill tables but never says they
      must not be forwarded, and the plan forbids edits under src/superclaude/cli/. A literal executor could forward
      them and get a click usage error; tests/cli/test_init_lite.py would not notice.
    evidence:
      - 'src/superclaude/skills/sc-init-lite-protocol/SKILL.md:57 "Preferred implementation: shell out to `superclaude init-lite` with the resolved flags via Bash"'
      - 'src/superclaude/skills/sc-init-lite-protocol/SKILL.md:25 "Any of `--project-root`, `--output`, `--dry-run`, `--scaffold`, `--force` are passed through from the command."'
      - 'src/superclaude/cli/init_lite.py:284-317 (six @click.option decorators)'
      - 'plan:44 and plan:171'
    tag: Grounded
    fix: >-
      In Task 8's SKILL.md edit add: --unattended and --report-dir are consumed by the skill/command and never
      forwarded to the CLI; the agent writes <report-dir>/return-contract.yaml itself. Add a phrase for it to the
      UNATTENDED_EXPECT entry.

  - id: R1-03
    t1_ref: null
    stance: new
    title: The Task 14 nested-propagation test cannot be written mechanically, and workflow also names a nested invocation
    severity: should-fix
    claim: >-
      The skeleton requires every section to name its nested invocations. Task 14 asserts every command whose section
      names a nested invocation (today only brainstorm) writes nested/<command>-<n>/. Workflow's Wave 4 calls reflect
      through the Skill tool, so its section names that call, and reflect does not accept the flag until P2 (D-P1-5).
      A generic test either fails for workflow or is hard-coded to brainstorm; Task 14 does not say how the test
      detects a nested invocation.
    evidence:
      - 'src/superclaude/skills/sc-workflow-protocol/SKILL.md:58 "Invoke `/sc:reflect --mode pre ... via Skill (`sc:reflect-protocol`), defaults for every other flag, no `--remediate`."'
      - 'plan:184 "the reflect step runs as today, without `--unattended` and without `--remediate`"'
      - 'plan:261 "every command whose section names a nested invocation (today only brainstorm) writes `nested/<command>-<n>/` for it"'
      - 'spec:62 "When the invoked command does not accept the flag yet, that step must be gate-free per its section 3 row, or the caller skips it"'
    tag: Grounded
    fix: >-
      Replace the generic test with two explicit ones: (a) brainstorm's section and skill name nested/analyze- and
      nested/adversarial-; (b) workflow's section names reflect as gate-free without --remediate and not passed the
      flag.

  - id: R1-04
    t1_ref: null
    stance: new
    title: The Task 1 helper must match the Check SCAN regex in Python, but the regex is POSIX and a literal copy would never match
    severity: should-fix
    claim: >-
      The expression uses [[:space:]], which Python re treats as an ordinary character set. A literal copy never
      matches "orca orchestration", so the assertion passes vacuously, and no negative test would expose it.
    evidence:
      - 'plan:29 "grep -rniE ''\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b''"'
      - 'plan:60 "and does not match the Check SCAN regular expression"'
    tag: Grounded
    fix: >-
      Give the Python form in Task 1: re.compile(r"\borca(-ide)?\s+(orchestration|worktree|terminal|agent)\b", re.I),
      and add a negative test that a section containing "orca worktree" makes the helper fail.

  - id: R1-05
    t1_ref: F-001
    stance: confirm
    title: The Task 15 path-list equality compares against an unfiltered git status
    severity: should-fix
    claim: >-
      At session start the tree held an uncommitted edit to APPROVED.md and an untracked .dev/reflect folder; neither
      is under .dev/tasks/ or .claude/ and neither is touched by the plan. git status --short also collapses
      untracked folders and carries status-letter prefixes, so "equals" is not literal.
    evidence:
      - 'plan:289 "The repo-path list in the report equals the output of `git status --short` for the working tree, ignoring paths under `.dev/tasks/` and the `.claude/` folder."'
    tag: Grounded
    fix: Use `git status --short --untracked-files=all -- src tests plugins`, compare paths only, and state the expected groups.

  - id: R1-06
    t1_ref: F-002
    stance: downgrade
    title: Brainstorm nested adversarial and analyze calls follow the general propagation rule
    severity: minor
    claim: >-
      Spec 2.1 is general; adversarial and analyze both accept the flag after P1. D-P1-4 is a faithful reading, not
      creep. Disclosure as D-P1-4 and in the Task 15 report is enough.
    evidence:
      - 'spec:62 "passes `--unattended` when the invoked command accepts it at this phase"'
      - 'spec:142 "from P2 it passes `--unattended` and a nested report directory (P2)"'
      - 'src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:273-280'
    tag: Grounded
    fix: None.

  - id: R1-07
    t1_ref: F-003
    stance: downgrade
    title: The command key collision in graph and impact is disclosed and bounded
    severity: minor
    claim: >-
      WC-4 wants the exact command line; WC-4 also says an existing contract keeps every existing field. The plan
      picks the second (D-P1-1) and Task 15 lists it. The 7.2 step 4 check only requires a non-empty command.
    evidence:
      - 'src/superclaude/skills/sc-graph-protocol/SKILL.md:90 "| `command` | string | `graph` |"'
      - 'src/superclaude/skills/sc-impact-protocol/SKILL.md:74 "| `command` | string | `impact` |"'
      - 'spec:72 "`command` (the exact command line)"'
    tag: Grounded
    fix: None; keep D-P1-1 and the Task 15 observation.

  - id: R1-08
    t1_ref: F-004
    stance: refute
    title: The spec states that a command with its own directory flag may also take --report-dir
    severity: minor
    claim: >-
      The spec sentence says --report-dir is the new flag "(for a command without such a flag, or a brief that does
      not pass it)"; the second alternative covers commands with their own flag. With "exactly one" and "both is
      refused" the skeleton is the stated rule, so no UNVERIFIED entry is needed.
    evidence:
      - 'spec:58 "(for a command without such a flag, or a brief that does not pass it)"'
      - 'plan:24 "exactly one of `--report-dir <dir>` or the command''s own directory flag"'
    tag: Grounded
    fix: Remove it from the UNVERIFIED list in the Task 15 report.

  - id: R1-09
    t1_ref: F-005
    stance: downgrade
    title: The seven unmapped rows are covered, so the coverage gap is a matcher artifact
    severity: minor
    claim: >-
      INF-001, 002 and 009 are covered at plan:19-20; INF-014 at plan:21; INF-010 by plan:22 and the Files lines of
      every task; INF-003 by the skeleton at plan:24; INF-006 by Tasks 2, 6, 7, 8, 9 and 13. The reviewer did not
      read the coverage-matrix file itself.
    evidence:
      - 'plan:19-22'
      - 'plan:24'
    tag: Grounded
    fix: None.

  - id: R1-10
    t1_ref: null
    stance: new
    title: adversarial's person-mode refusal names only --interactive; the command also has the -i alias (and -o)
    severity: minor
    claim: >-
      The Options table lists `--interactive | -i` and `--output | -o`. The flag parse rule counts standalone tokens,
      so -i is a person-mode flag that could slip through; the same holds for -o in the one-report-directory rule.
    evidence:
      - 'src/superclaude/commands/adversarial.md:68 "| `--interactive` | `-i` |"'
      - 'src/superclaude/commands/adversarial.md:69 "| `--output` | `-o` |"'
      - 'plan:79 "`--interactive` is refused"'
    tag: Grounded
    fix: Name -i and -o in the adversarial section and add -i to its UNATTENDED_EXPECT flags.

  - id: R1-11
    t1_ref: null
    stance: new
    title: WORKER-CONTRACT.md brief-flag table stays P0-era after P1 (index-repo "none", init-lite lacks --report-dir)
    severity: minor
    claim: >-
      The plan decides not to edit the table. A coordinator following it would omit --report-dir for index-repo and
      init-lite, and the worker would refuse (WC-4). WORKER-CONTRACT.md:184 still says "At P0 no command accepts it".
      Spec 3.1 says "none" for the same reason, so this is a spec observation, not a plan defect.
    evidence:
      - 'src/superclaude/core/WORKER-CONTRACT.md:196 "| `/sc:index-repo` | none |"'
      - 'src/superclaude/core/WORKER-CONTRACT.md:197 "| `/sc:init-lite` | `--output <file>` |"'
      - 'plan:22'
    tag: Grounded
    fix: Add this to the Task 15 spec observations; fix the table in a later phase.

  - id: R1-12
    t1_ref: null
    stance: new
    title: The make lint comparison with "no new violation" will see new WARN lines
    severity: minor
    claim: >-
      lint-architecture warns for any command over 200 lines; adding sections pushes files such as adversarial.md
      (182 lines now) over 200, so the WARN lines differ from the baseline although nothing fails. plan:281 does not
      say whether a WARN counts.
    evidence:
      - 'Makefile:406 "elif [ \"$$lines\" -gt 200 ]; then ... WARN [Check 3]"'
      - 'Makefile:403 "-gt 500 ... ERROR [Check 4]"'
      - 'plan:281 "no new violation and no new unformatted file"'
    tag: Grounded
    fix: Define pass as exit 0 and no new ERROR or ruff finding; record new WARN [Check 3] lines without failing.

  - id: R1-13
    t1_ref: null
    stance: new
    title: graph init refusal is placed in a section that follows the Init steps and the plan does not say who writes the failed contract
    severity: should-fix
    claim: >-
      The graph command runs the skill first and then the Init steps. The plan adds the refusal as a new section after
      Init and says the contract is failed with a reason, but not whether the refusal happens before the skill
      preflight (spec 2.1: "a stop before any work"), nor who writes the contract with reason, since only the skill
      writes it and its preflight may end in form: default.
    evidence:
      - 'src/superclaude/commands/graph.md:39-53 (Activation, then Init steps, then Boundaries)'
      - 'plan:109'
      - 'spec:57 "A refusal is a stop before any work: the command writes its contract with `worker_status: failed`"'
    tag: Grounded
    fix: >-
      Say in Task 4 that under --unattended the init positional is refused before the Skill call, that the skill
      writes the failed contract (reason: init runs only when the user types it), and give the skill-side wording.

self_audit:
  - Read the plan, source.md, APPROVED.md and WORKER-CONTRACT.md in full.
  - Read spec 2.1, WC-4, sections 3.1 and 3.2 rows, the section 6 table, 7.1 and 7.3.
  - Confirmed the 16-command list against spec section 6.
  - Read tests/skills/test_worker_contract.py (UNATTENDED_COMMANDS, the section check, the write-verb audit, the deferred:P1 entry).
  - Checked every named pre-existing test file exists, the workflow mirror set against the plugin mirror test, and the Makefile size limits.
  - Not verified - the coverage-matrix.yaml file itself, and whether the branch already has commits touching the command files. Codegraph was not used.
