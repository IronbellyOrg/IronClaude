<!-- Provenance: merged verdict card produced by merge-executor from adversarial/refactor-plan.md (8 planned changes) -->
<!-- Base: Variant 1 reviewer-1 analyzer (adversarial/variant-1-original.md) -->
<!-- Incorporated: Variant 2 reviewer-2 qa (R2-QA-002); Variant 3 reviewer-3 refactorer (R3-1 analysis, R3-3, R3-4, R3-5, R3-6 part, R3-10, R3-12, R3-A1); invariant probe (INV-001 to INV-009) -->
<!-- Merge date: 2026-11-08 -->

# Merged Verdict Card: reflect reviewers on TASK-WF-spec-20261108-181616

```yaml
# Source: Change 8 (header) -- refactor-plan.md
merged_from: [variant-1, variant-2, variant-3]
plan: .dev/tasks/to-do/TASK-WF-spec-20261108-181616/TASK-WF-spec-20261108-181616.md
spec: .dev/tasks/to-do/TASK-WF-spec-20261108-181616/source.md
convergence_score: 0.97
blocking_findings: [C-003]
findings:
  # Source: variant-1 F1; severity blocking -> minor per Change 1 (scoring matrix C-002)
  - id: C-002
    card_id: F1
    severity: minor
    category: ordering
    claim: "Task 3's begin must exit 5 on prior-verdict mismatch and seal's prior link needs 'confirmed and open in review N-1', but final-status derivation lands in Task 4 and compute_verdict in Task 5."
    evidence: ["plan:57", "plan:60", "plan:68", "plan:77", "source.md:62", "source.md:64"]
    recommendation: "Move status/verdict computation into Task 3 (Tasks 4-5 extend it), or move the prior-verdict-mismatch part of begin and its test to Task 5."
    source: variant-1

  # Source: variant-1 F2; severity blocking -> minor per Change 1 (scoring matrix C-001)
  - id: C-001
    card_id: F2
    severity: minor
    category: ordering
    claim: "Task 5's finalize label-count line uses 'the same function as Task 6's count', but Task 6 depends on Task 5 (confirms T1 A1)."
    evidence: ["plan:77", "plan:80", "plan:83", "plan:87"]
    recommendation: "Define the label-count function (including form-only dropped claims) in Task 5 or Task 3; Task 6 only wraps it as the count subcommand."
    source: variant-1

  # Source: variant-1 F3; claim and recommendation rewritten per Change 2 (Round 2 mechanism; invariant-probe INV-001, INV-002, INV-003)
  - id: C-003
    card_id: F3
    severity: blocking
    category: acceptance
    claim: >-
      Task 7 replay cannot pass as written. Without --re-review, begin sets N = 1, the ratchet is off,
      and the per-claim assertion that claims on text unchanged since v2 are late-found fails; with
      --re-review on the real control-r1 round-2 report, begin exits 5 because that report has no
      sentinel prior (no valid sentinel, spec= hash or matching verdict). Blocking reason: Task 7's
      fixture list names no prior report and the plan forbids synthetic substitutes, so the replay
      assertion can never pass; this is not merely an unstated scaffold design, since Task 3 already
      builds sentinel-bearing tmp_path prior reports under the read-ahead rule (INV-003). Even with a
      prior report, the first seal on the fixture always exits 3 on the 28 real changed hunks that hold
      no claim or checked line (INV-001), and the expected split is taken from the same changed-line set
      the ratchet computes, decided by an unstated quote-line choice (INV-002). Uncovered-hunk handling
      in replay is unspecified.
    evidence: ["plan:96", "plan:99", "plan:57", "plan:60", "plan:77", "source.md:62", "source.md:64", "source.md:93", "source.md:193"]
    recommendation: >-
      Name the prior review-2 report in Task 7's fixture list and have the test build it with a sentinel
      in tmp_path as declared scaffolding. Seal a second (final) time, or add checked lines for the 28
      real changed hunks, and say which (INV-001). Fix the quote-line rule as the line the report cites,
      record it per claim, and do not derive the expected split from the code under test (INV-002).
      Say whether replay adds checked lines or asserts only ratchet statuses.
    source: variant-1

  # Source: variant-1 F4; extended per Change 3 with variant-3 R3-1 (equality-test lock-in) and invariant-probe INV-004 (E-SKILL-MISSING line)
  - id: C-004
    card_id: F4
    severity: minor
    category: deviation
    claim: >-
      spec-panel.md Usage line 23 advertises --unattended; Task 9 keeps it, so the variant advertises a
      flag it refuses; Task 10 replaced-block list and Task 9 acceptance do not cover it. Task 10's
      equality test treats that line as inherited, so a fix would fail it, locking the Usage line in.
      The E-SKILL-MISSING rule Task 9 adds is, as its own line, not in Task 10's exhaustive
      replaced-block list, so the equality test against spec-panel.md fails unless the rule is folded
      into the activation line.
    evidence: ["src/superclaude/commands/spec-panel.md:23", "src/superclaude/commands/spec-panel.md:451-462", "src/superclaude/commands/spec-panel.md:456", "src/superclaude/commands/spec-panel.md:459", "plan:21", "plan:123", "plan:135", "source.md:115", "source.md:256"]
    recommendation: >-
      Drop the --unattended Usage line (or token) in Task 9, add it to Task 10's replaced blocks, add
      grep -c -- '--unattended' = 0 to Task 9 acceptance. Also add the E-SKILL-MISSING rule line to
      Task 10's replaced-block list, or fold the rule into the activation line.
    source: variant-1

  # Source: variant-1 F5 (unchanged)
  - id: C-005
    card_id: F5
    severity: minor
    category: coverage
    claim: "Spec test 'two claims on one prior counted once' is in no task acceptance list and the rule is stated nowhere in Tasks 3-5."
    evidence: ["source.md:128", "plan:60", "plan:71", "plan:80"]
    recommendation: "Add the case and the rule to Task 3 or Task 5."
    source: variant-1

  # Source: variant-1 F6 (unchanged)
  - id: C-006
    card_id: F6
    severity: minor
    category: coverage
    claim: "Task 12 stages before Tasks 13-14 create INSTALL.md and briefs; nothing stages them and Task 13's git diff --cached check only sees Task 12's staging."
    evidence: ["plan:27", "plan:161", "plan:172", "plan:182"]
    recommendation: "Stage .dev/brainstorms/346-stoprule/ and .dev/tasks at the end of Tasks 13 and 14."
    source: variant-1

  # Source: variant-1 F7; severity minor -> not-a-defect per Change 1 (scoring matrix C-007)
  - id: C-007
    card_id: F7
    severity: not-a-defect
    category: ordering
    claim: "Task 13 must list Task 14's templates and Task 14's acceptance requires INSTALL.md to list eleven files, but Task 14 has no instruction to edit INSTALL.md."
    evidence: ["plan:172", "plan:180", "plan:190"]
    recommendation: "Check the list in Task 13's acceptance, or have Task 14 update INSTALL.md."
    source: variant-1

  # Source: variant-1 F8 (unchanged)
  - id: C-010
    card_id: F8
    severity: minor
    category: coverage
    claim: "Writers of final/verdict ledger lines, the source of sentinel brief=/grader_model=/ratchet=, and parent= (escalation g) are unspecified."
    evidence: ["source.md:34", "source.md:69-70", "source.md:73", "plan:77"]
    recommendation: "Name the writer subcommands and the source of brief= in Task 5; define parent= or drop it."
    source: variant-1

  # Source: variant-1 F9 (unchanged)
  - id: C-011
    card_id: F9
    severity: minor
    category: coverage
    claim: "apply-audit defines real:true only for claims; a real:true on a seeded unclaimed hunk has no defined outcome."
    evidence: ["plan:68", "source.md:68"]
    recommendation: "Define the outcome (e.g. FAIL) with a test in Task 4."
    source: variant-1

  # Source: variant-1 F10 (unchanged; its quote-line rule is also folded into C-003 via INV-002)
  - id: C-012
    card_id: F10
    severity: minor
    category: risk
    claim: "Task 7's hand-transcribed quotes decide anchored vs late-found; the quote-selection rule is unstated."
    evidence: ["plan:96", "source.md:93", "source.md:193"]
    recommendation: "Quote the line the report cites and record the choice per claim."
    source: variant-1

  # Source: variant-1 F11; extended per Change 5 with variant-3 R3-6 (src/superclaude scan; script-relative default rubric path)
  - id: C-013
    card_id: F11
    severity: minor
    category: acceptance
    claim: >-
      The stdlib import grep is only in Task 3; Tasks 4-6 extend the script unchecked.
      test_worker_contract.py scans new primitives for git/gh write verbs. stoprule.py and
      canaries.json not in the static src/superclaude scan; default --rubric path must be
      script-relative.
    evidence: ["plan:26", "plan:61", "plan:20", "tests/skills/test_worker_contract.py:1940-1951", "plan:25", "plan:57", "plan:135"]
    recommendation: >-
      Repeat the import grep in Task 6; forbid git/gh write-verb text in new files in Tasks 3 and 8.
      Scan stoprule.py and canaries.json; build the default --rubric path from Path(__file__); test
      from a tmp copy.
    source: variant-1

  # Source: variant-1 F12 (unchanged; variant-2 R2-QA-001 merged here as minor, see not_made)
  - id: C-008
    card_id: F12
    severity: minor
    category: coverage
    claim: "Measurement copy not produced by any task (not a plan defect: section 3 omits it); INSTALL.md's 'differ only in lines from master' is unverified. Control r1 files exist in the sibling checkout."
    evidence: ["source.md:163", "plan:172", "plan:96"]
    recommendation: "Task 13 records the repo copy's line count and diff against the 472-line base instead of asserting; name exact source paths in Task 7."
    source: variant-1

  # Source: variant-2 R2-QA-002; inserted per Change 4; severity blocking -> minor (scoring matrix C-009)
  - id: C-009
    card_id: R2-QA-002
    severity: minor
    category: acceptance
    claim: "Task 3 keeps a withdrawn claim's id and claimed label but not its prior link, which Task 6 needs to exclude withdrawn carried priors from the new-finding count; the fixture does not test this."
    evidence:
      - ".dev/tasks/to-do/TASK-WF-spec-20261108-181616/TASK-WF-spec-20261108-181616.md:57"
      - ".dev/tasks/to-do/TASK-WF-spec-20261108-181616/TASK-WF-spec-20261108-181616.md:87"
      - ".dev/tasks/to-do/TASK-WF-spec-20261108-181616/TASK-WF-spec-20261108-181616.md:90"
      - ".dev/tasks/to-do/TASK-WF-spec-20261108-181616/source.md:173"
    recommendation: "Require the first-pass form line to keep prior with id and claimed; add a test with a withdrawn new MAJOR (counted) and a withdrawn carried MAJOR (excluded)."
    source: variant-2

  # Source: variant-3 R3-3; inserted per Change 5
  - id: C-014
    card_id: R3-3
    severity: minor
    category: acceptance
    claim: "FR-8/FR-9 rewrite, bullet 7 suffix and no-unattended sentence have no positive check; equality test excludes them."
    evidence: ["source.md:105", "src/superclaude/commands/spec-panel.md:328", "src/superclaude/commands/spec-panel.md:329", "plan:126", "plan:135"]
    recommendation: "Assert the new wording in test_spec_panel_stoprule.py."
    source: variant-3

  # Source: variant-3 R3-4; inserted per Change 5
  - id: C-015
    card_id: R3-4
    severity: minor
    category: risk
    claim: "test_review_severity_rule.py scans only git-tracked files; Tasks 10 and 12 run it before staging."
    evidence: ["tests/skills/test_review_severity_rule.py:35", "tests/skills/test_review_severity_rule.py:38", "tests/skills/test_review_severity_rule.py:448", "plan:140", "plan:161", "plan:165"]
    recommendation: "Stage first, then run pytest in Task 12."
    source: variant-3

  # Source: variant-3 R3-5; inserted per Change 5
  - id: C-016
    card_id: R3-5
    severity: minor
    category: risk
    claim: "Task 12 omits tests/agents, tests/docs, tests/cli which scan new files."
    evidence: ["tests/agents/test_tavily_tool_parity.py:31", "tests/agents/test_tavily_tool_parity.py:34", "tests/docs/test_retired_docs_absent.py:40", "plan:165"]
    recommendation: "Add them or run the whole suite."
    source: variant-3

  # Source: variant-3 R3-10; inserted per Change 5; classified drift (see confirmed_deviations)
  - id: C-018
    card_id: R3-10
    severity: minor
    category: scope
    claim: "offline-demotion-audit.md and replay-gate.md are section 5 procedures outside the plan's stated scope."
    evidence: ["plan:19", "plan:184", "source.md:143", "source.md:170", "source.md:180"]
    recommendation: "Cite an owner decision or drop them."
    source: variant-3

  # Source: variant-3 R3-12; inserted per Change 5
  - id: C-020
    card_id: R3-12
    severity: minor
    category: acceptance
    claim: "Task 10 allows only the _POST_REFRESH_ADDITIONS line to change, leaving its comment stale."
    evidence: ["tests/recommend/test_routing_refresh.py:29", "tests/recommend/test_routing_refresh.py:33", "tests/recommend/test_routing_refresh.py:648", "plan:141"]
    recommendation: "Allow one comment line naming #346."
    source: variant-3

  # Source: variant-3 R3-A1 (advisory); inserted per Change 5 as minor; source gives no recommendation, so the recommendation restates the advisory as an action
  - id: C-021
    card_id: R3-A1
    severity: minor
    category: advisory
    claim: "Integration Patterns examples still call plain /sc:spec-panel."
    evidence: ["src/superclaude/commands/spec-panel.md:430", "src/superclaude/commands/spec-panel.md:436", "source.md:104", "plan:123"]
    recommendation: "Decide whether the Integration Patterns examples should call the variant command; as written they follow source.md:104 literally."
    source: variant-3

  # Source: invariant-probe INV-005 (MEDIUM, UNADDRESSED); inserted per Change 6 as minor
  - id: INV-005
    card_id: INV-005
    severity: minor
    category: state_variables
    claim: >-
      `check` recomputes every status and the verdict, and `begin` recomputes the prior report's verdict.
      Recomputing `late-found` needs the baseline, the spec and the N-1 report; recomputing `minor-form`
      needs the spec and the evidence files under `--root`. The plan gives `check` no argument list, and
      the coordinator template runs `check` on the report only. `check` must therefore either take
      unstated inputs or trust recorded `final` lines, which is weaker than "recompute".
    evidence: ["plan:77", "source.md:74", "plan:57", "plan:184"]
    recommendation: "Give check and begin the inputs recomputation needs, or have the ledger store what they need to recompute statuses from the report alone."
    source: invariant-probe

  # Source: invariant-probe INV-006 (MEDIUM, UNADDRESSED); inserted per Change 6 as minor
  - id: INV-006
    card_id: INV-006
    severity: minor
    category: state_variables
    claim: >-
      The review number has two unchecked sources. Bullets 1 and 4 keep the reviewer-written header rule
      `review: N of 3` verbatim, while the script takes N from the sentinel `review=N/3`. `check`
      compares the sentinel, the computed block and the last line, not the header. If the header and
      the sentinel disagree, nothing detects it.
    evidence: ["spec-panel.md:258", "spec-panel.md:261", "plan:123", "plan:57", "plan:77"]
    recommendation: "Make one source authoritative for N, or have check compare the header with the sentinel."
    source: invariant-probe

  # Source: invariant-probe INV-007 (MEDIUM, UNADDRESSED); inserted per Change 6 as minor
  - id: INV-007
    card_id: INV-007
    severity: minor
    category: count_divergence
    claim: >-
      `m1_open_confirmed` = sentinel `confirmed` + frozen `unresolved-prior`. The never-batched rule names
      only the frozen prior blockers themselves, so a single new claim with a valid `prior` link is
      batched, can be graded `confirmed`, and counts again next to its still-open frozen prior: two
      counts for one defect with only one claim. M1 has a "<= 3" bar and F1a stops the run at M1 >= 4.
    evidence: ["plan:87", "plan:68", "source.md:186", "source.md:201"]
    recommendation: "Count a defect once in m1_open_confirmed when a single claim is linked to an open frozen prior, and state the rule alongside C-005."
    source: invariant-probe

  # Source: invariant-probe INV-008 (MEDIUM, UNADDRESSED); inserted per Change 6 as minor
  - id: INV-008
    card_id: INV-008
    severity: minor
    category: guard_conditions
    claim: >-
      `begin` sets N = 1 whenever `--re-review` is absent. A dispatch that omits the flags restarts the
      count, so exit 4 can never fire. The cap therefore still depends on the coordinator passing flags.
      Inherited from the spec; the plan's install note limits use to Arm B.
    evidence: ["plan:57", "source.md:62", "source.md:150", "plan:184", "plan:172"]
    recommendation: "State that the review cap depends on the coordinator passing --re-review, or make begin detect an existing prior report instead of resetting N."
    source: invariant-probe

  # Source: invariant-probe INV-009 (MEDIUM, UNADDRESSED); inserted per Change 6 as minor
  - id: INV-009
    card_id: INV-009
    severity: minor
    category: interaction_effects
    claim: >-
      An `incomplete`-only FAIL gives the NONE brief and no spec edit, so the next review has an empty
      changed-line set. A prior link is valid only for a claim confirmed in N-1, so earlier `unconfirmed`
      claims cannot anchor. Every re-raised defect becomes `late-found` and never loops; only the
      PASS-time audit can reinstate it. One grader outage therefore turns real defects into items that
      never loop. Inherited from the spec; no task tests the path.
    evidence: ["plan:77", "plan:57", "plan:68", "source.md:71", "source.md:243"]
    recommendation: "Define how claims re-raised after an incomplete-only FAIL anchor, and add a test for the grader-outage path."
    source: invariant-probe

# Source: Change 7 (base keep) -- variant-1 confirmed A2/A3, debate X-004/S-002; drift mapped to C-018 (variant-3 R3-10)
confirmed_deviations:
  - deviation: "Removal of the Unattended section from the variant"
    classification: authorized
    basis: "Owner ruling in the plan's Constraints (variant-1 A3)"
  - deviation: "Edit of tests/recommend/test_routing_refresh.py"
    classification: necessary
    basis: "Exact-set command check must change for the new command (variant-1 A2)"
  - deviation: "Section-5 templates offline-demotion-audit.md and replay-gate.md"
    classification: drift
    basis: "C-018: outside the plan's stated scope with no owner citation"
deviation_counts: {authorized: 1, necessary: 1, drift: 1, regression: 0}

# Source: refactor-plan.md "Changes NOT Being Made"
not_made:
  - {id: C-017, card_id: R3-7, reason: "Rubric hash read from artifact: consensus not-a-defect."}
  - {id: C-019, card_id: R3-11, reason: "Category frontmatter: consensus not-a-defect; source.md 3.3 lists exact keys."}
  - {id: C-007, card_id: F7, reason: "INSTALL ordering: consensus not-a-defect (kept in findings at severity not-a-defect, not as a defect)."}
  - {id: C-008, card_id: R2-QA-001, reason: "V2 QA-001 as blocking drift: conceded by its own advocate; merged as F12 minor."}
```
