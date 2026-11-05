reviewer: 2
persona: qa
model: haiku
verdict: PARTIAL
note: persisted by the orchestrator from the reviewer's returned card; claims shortened, evidence kept.
findings:
  - id: R2-01
    t1_ref: F-006
    stance: confirm
    title: business-panel deletion bound is tight but arithmetically correct; no fix needed
    severity: minor
    claim: >-
      The Task 11 criterion "at most 4 deleted lines" is exactly the worst case: the old block is heading, blank,
      yaml fence, --- , 6 key lines, ---, closing fence; the longest common subsequence keeps --- and the 6 keys, so
      at most 4 lines are deleted. The criterion also requires the keys and values unchanged.
    evidence:
      - 'plan:223 "shows at most 4 deleted lines (the old heading line, the two code-fence lines and at most one blank line)"'
      - 'src/superclaude/commands/business-panel.md:1-11'
    tag: Grounded
    fix: none

  - id: R2-02
    t1_ref: F-007
    stance: confirm
    title: Tasks 10 and 11 bundle three commands each; every file is still named per task
    severity: minor
    claim: >-
      Each bundled task names every file it edits and carries per-file acceptance criteria, so the no-bulk-task
      discipline holds; the cost is only reviewer view size.
    evidence:
      - 'plan:195 "## Task 10: Convert `/sc:analyze`, `/sc:build` and `/sc:design`"'
      - 'plan:199 "Files: `src/superclaude/commands/analyze.md`, `src/superclaude/commands/build.md` and `src/superclaude/commands/design.md`"'
    tag: Grounded
    fix: none

  - id: R2-03
    t1_ref: null
    stance: new
    title: Section placement contradiction - skeleton says before the final boundaries heading; Tasks 3, 6 and 9 say before ## Boundaries in the three files that have two boundaries headings
    severity: should-fix
    claim: >-
      brainstorm.md, workflow.md and cleanup-audit.md each have both ## Boundaries and a later ## CRITICAL BOUNDARIES,
      so their final boundaries heading is ## CRITICAL BOUNDARIES, while Tasks 3, 6 and 9 say "before ## Boundaries".
      The executor must guess which anchor wins; both pass the grep-based criteria, so the guess is silent.
    evidence:
      - 'plan:24 "placed immediately before the file''s final boundaries heading (`## Boundaries`, or `## CRITICAL BOUNDARIES` in business-panel.md ...)"'
      - 'plan:94 "the `## Unattended mode` section before `## Boundaries`" (Task 3)'
      - 'src/superclaude/commands/brainstorm.md:145 "## Boundaries" and :177 "## CRITICAL BOUNDARIES"'
      - 'src/superclaude/commands/workflow.md:63 "## Boundaries" and :78 "## CRITICAL BOUNDARIES"'
      - 'src/superclaude/commands/cleanup-audit.md:87 "## Boundaries" and :101 "## CRITICAL BOUNDARIES"'
    tag: Grounded
    fix: >-
      Pick one anchor and make the four sites agree: amend the skeleton to name the first ## Boundaries heading (or
      change Tasks 3/6/9 to ## CRITICAL BOUNDARIES).

  - id: R2-04
    t1_ref: null
    stance: new
    title: tests/test_cleanup_audit_structure.py is required to pass in Task 6 but appears in neither baseline and not in the Constraints list
    severity: should-fix
    claim: >-
      Task 6 runs tests/test_cleanup_audit_structure.py, which sits directly under tests/; the AC-C3 baseline runs
      tests/skills/ only and the wider baseline names other directories, so a pre-existing failure there would fail
      Task 6 with no accepted-failures record.
    evidence:
      - 'plan:147 "uv run pytest tests/skills/test_worker_contract.py tests/skills/test_codegraph_adoption.py tests/test_cleanup_audit_structure.py -q"'
      - 'plan:52-53 (baseline commands)'
      - 'plan:42 (sixteen-file list; the file is absent)'
      - 'tests/test_cleanup_audit_structure.py:39 "def test_file_exists(self, filename):"'
    tag: Grounded
    fix: Add the file to the Constraints list and run it once in Task 1 so t1-accepted-failures.md covers it.

  - id: R2-05
    t1_ref: F-003
    stance: confirm
    title: D-P1-1 redefines the worker command field for graph and impact, contradicting WC-4's field definition
    severity: should-fix
    claim: >-
      The plan detects the collision and lists it in the report, but adopts the deviation unilaterally; the live plan
      and coordinator automation will see "graph", not the command line, and 7.2 step 4 only asserts non-empty.
    evidence:
      - 'spec:72 "`command` (the exact command line)"'
      - 'src/superclaude/skills/sc-graph-protocol/SKILL.md:116 "command: graph"'
      - 'src/superclaude/skills/sc-impact-protocol/SKILL.md:74 "| `command` | string | `impact` |"'
      - 'plan:43 "D-P1-1: ... The existing key is kept as is ..."'
      - 'plan:284 (spec observations list)'
    tag: Grounded
    fix: >-
      Get the coordinator or owner to ratify D-P1-1 (record it in APPROVED.md or as an owner-signed line in the static
      report), or have the graph and impact sections state that command carries the short name.

  - id: R2-06
    t1_ref: null
    stance: new
    title: init-lite amends Safety Invariants 2 and 3 where the spec row names only Invariant 3
    severity: minor
    claim: >-
      The spec's small fix names Safety Invariant 3; Task 8 amends 2 and 3 because the contract is required on
      --dry-run. The extension is necessary but is a spec delta decided inside a task body, not in the D-P1 list.
    evidence:
      - 'spec:147 "amend Safety Invariant 3 (\"the only write is the marked report\", ...) to allow the contract (P1)"'
      - 'src/superclaude/skills/sc-init-lite-protocol/SKILL.md:62-63'
      - 'plan:169'
    tag: Grounded
    fix: Add the invariant-2 extension to the D-P1 decision list (D-P1-11).

  - id: R2-07
    t1_ref: null
    stance: new
    title: Plugin command copies for the converted commands other than workflow go stale by design
    severity: minor
    claim: >-
      No test pins those copies and the plan documents the policy, but the stale set should be visible to the
      coordinator before the plugin is next built.
    evidence:
      - 'plan:23'
      - 'src/superclaude/commands/README.md:9'
      - 'tests/commands/test_routing_plugin_parity.py:43'
    tag: Grounded
    fix: Add one line to Task 15's report inventory naming the plugin command copies left stale by P1.

self_audit:
  - Read the full plan, source.md and the whole spec.
  - Verified all 17 command files exist and their real ## headings (surfaced R2-03).
  - Verified the named anchors in the adversarial, graph, impact, brainstorm, init-lite, cleanup-audit and workflow skills.
  - Verified the pinning tests and that no test pins the plugin copies other than the README four.
  - Walked every P1-relevant spec span against the plan; the seven unmapped matrix rows are matcher misses, not coverage gaps.
  - Dropped as findings - D-P1-4 (spec-consistent), D-P1-3 (reported in Task 15), the workflow reflect-step disposition (compliant).
