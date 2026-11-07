```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.6867
citations_total: 26
citations_revalidated: 26
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
citation_count_scope: file-line evidence items; 21 source quotes plus 5 body ranges
command_claims_passed_through: 3
coverage_degraded: parsed-sparse
evidence_validator_ran: true
zero_drop_flag: true
```

# Pre-execution advisory review

## Review result
**Plan verdict: PASS, with minor advisory notes. No blocking plan defect was established.** The three reviewer cards underwent independent calibration and an actual adversarial merge. The merge resolved all 11 debate points (convergence 1.00), selected reviewer 3 as its base, and retained six minor notes. Its evidence is in `adversarial/merged-verdict.yaml`, `adversarial/merged-review.md`, `adversarial/debate-transcript.md` and `adversarial/merge-log.md`.

The mean of the three independently calibrated card confidences is **0.6867** (0.72, 0.66, 0.68). Agreement is not confidence: 1.00 convergence does not raise that score or establish runtime correctness. This is an advisory plan review, not authorization from this session to execute or a claim that the implementation is complete.

**Self-Audit:** the review actively checked every quote-pinned source obligation, both tasks and their global constraints, the existing installer early return and caller, captured child output, the existing executable prerequisite, normal installer help, the forced/default paths, and preservation of supervised-worker/internal-agent boundaries. Lexical misses were not silently converted into measured full coverage. Existing code gaps were not mislabeled as post-execution regressions. The original input tree remains unchanged.

## Coverage matrix

The source contains no labeled requirement IDs. Two tasks were parsed. Pass 2 extracted 21 quote-pinned requirements, of which the fixed containment matcher mapped 13 to a single task (61.90%). Parsed-only coverage is null, not zero; union coverage is 0.6190. The unmapped-density signal is 8/21 = 0.380952. `coverage_degraded: parsed-sparse` forces the second-tier review. The review invocation has standard depth; the plan's quick-depth metadata does not override it.

The matcher uses case-folded unique alphanumeric content words, a recorded fixed stopword set, and a 0.60 threshold against each task's text. Global Constraints are not duplicated into each task. Thus lexical misses are not automatically substantive omissions. Exact ratios and word rules are in `artifacts/coverage-matrix.json`; runnable matching and its assertions are in `artifacts/match-coverage.py`. Semantic coverage is assessed separately against the whole plan, including Inputs and Constraints.

## Inferred requirements (Pass 2)

All quotes below are verbatim spans of `.dev/tasks/to-do/TASK-WF-fixIssue412SVeri-20261106-215543/source.md:1`. The citation column `source.md:1` resolves to that package source, not this review directory. Each row has `source: inferred`, meaning quote-pinned extraction rather than an unsupported report claim.

| Requirement | Verbatim source quote | Citation | Deterministic match |
|---|---|---|---|
| INF-001 | Fix issue #412's verified instruction-delivery gaps, not Orca shell behavior. | source.md:1 | None |
| INF-002 | Add an explicit globally loaded rule in src/superclaude/core/CLAUDE.md and matching src/superclaude/skills/ccsession-tag/README.md guidance | source.md:1 | Task 1 |
| INF-003 | new ccsession-backed Claude sessions use Claude (CLI), never New Terminal | source.md:1 | Task 1 |
| INF-004 | programmatic creation uses the version-matched Orca agent launch or worktree create --agent | source.md:1 | Task 1 |
| INF-005 | explicit terminal surface when CLI required | source.md:1 | Task 1 |
| INF-006 | Reserve terminal create for shells. | source.md:1 | Task 1 |
| INF-007 | Preserve supervised worker-start/dispatch-preamble rules and internal Agent-tool subagents. | source.md:1 | Task 1 |
| INF-008 | Repair src/superclaude/cli/install_user_setup.py so install_user_setup(force=True) requests safe refresh even with existing Orca guides | source.md:1 | Task 2 |
| INF-009 | ordinary nonforce setup still skips existing copies. | source.md:1 | Task 2 |
| INF-010 | Do not forward --force to Orca or overwrite edited guides | source.md:1 | Task 2 |
| INF-011 | show meaningful skipped/warning output rather than claiming refresh succeeded. | source.md:1 | None |
| INF-012 | Add minimal regression checks in tests/cli/test_install_user_setup.py and tests/core/test_orca_session_launch_guidance.py with observed pre-fix failures | source.md:1 | Task 2 |
| INF-013 | force propagation, default skip and nonfatal absent/failing Orca. | source.md:1 | Task 2 |
| INF-014 | Canonical edits only then make sync-dev and make verify-sync | source.md:1 | Task 2 |
| INF-015 | never stage .claude mirrors, stage .dev/tasks. | source.md:1 | Task 2 |
| INF-016 | No commit/push/PR, global install or other repo edits. | source.md:1 | None |
| INF-017 | Issue412 already contains verified refresh-introducing PR245 and intentional Orca CLI-label PR29074, not shell-causation proof. | source.md:1 | None |
| INF-018 | Actual failing agent transcript and a historical New Terminal semantic-change PR remain unverified; preserve boundary. | source.md:1 | None |
| INF-019 | Current diagnosis independent validation returned partial with static findings verified; runtime cause UNDETERMINED. | source.md:1 | None |
| INF-020 | User explicitly authorizes execution after reading checked plan. | source.md:1 | None |
| INF-021 | Two-phase bounded plan, no verification-only task. | source.md:1 | None |

These history and diagnosis statements are requirements to preserve the source's evidence boundary. This review did not independently re-investigate the issue, its history or its incident cause. The execution sentence does not authorize implementation by this review-only session.

## Best-practice compliance
Advisory grade: 4/5. The proposed change is bounded to the shared helper/caller, existing instruction surfaces and their tests. It adds no launch wrapper, dependency or output parser; preserves positional compatibility, executable identification, timeout and nonfatal failure handling; and requires red/green evidence and final synchronization. The remaining point reflects wording-level verification specificity, not an observed product failure: reviewers requested explicit checks for exit-zero safe-skip messages and for the shell versus agent-terminal wording. These are minor notes, not grounds for changing the plan in this session.

No library migration or third-party API redesign is proposed. External best-practice lookup was not required; version-matched local Orca help supplies the relevant installer and launch distinction. The architecture and safety assessment is about the proposed strategy, not a claim that any future implementation passes its tests.

## Gap registry
No blocking gap is registered. The merged review retained these six minor notes; none triggers remediation or a plan edit in this session:

1. **Exit-zero safe-skip output:** the future mocked tests should distinguish skip text on stdout, skip text only on stderr, and empty child output. Existing guide presence cannot prove a refresh. This refines the output requirement already in the plan's Task 2 Inputs and acceptance criteria.
2. **Explicit shell prohibition:** Task 1's acceptance text says "distinguish", while its source requires "never New Terminal". The source is explicitly an input to Task 1, so the prohibition remains binding. Keeping it explicit in the resulting guidance and static checks avoids a wording ambiguity, not a newly discovered behavior change.
3. **Existing documentation-test reader:** `tests/core/test_codegraph_guide.py:137-174` reads the core instructions and contains placement-sensitive assertions. Including it in the future wider regression evidence is a minor verification suggestion; no failure was observed. Other test suggestions in the merged card are labeled leads, not proven affected tests.
4. **Shared time budget:** the forced path will request Orca installation before the plugin step, sharing the existing deadline. The merged review recommends recording the plugin outcome in mocked forced-path evidence, not redesigning the budget or adding a new task. This is a bounded planning risk, not an observed regression.
5. **Compatibility and failure wording:** the new optional force argument should preserve the existing positional parameters and be forwarded by keyword. Forced refresh failures with guides already present must not claim that a refresh succeeded. These refine the existing compatibility and accurate-reporting criteria.
6. **Earlier checks are optional:** running routing and synchronization checks immediately after Task 1 could surface issues earlier, but Task 2 already delivers those checks by design. Their placement is not a missing deliverable.

The invariant probe recorded no unaddressed HIGH finding. Its MEDIUM/LOW entries remain non-blocking verification notes. Sparse labeling, shared constraints outside the matcher, and the future execution gate explain lexical misses; the 13/21 measured value remains unchanged. The separate reviewer claim of 21/21 semantic coverage is judgment, not a measured replacement.

Original wrong helper-line and brief-local plan-line citations were excluded before synthesis. Failed lookups and their disposition are recorded in `artifacts/negative-evidence.yaml`.

## Evidence and limitations
### Verified existing implementation

- `src/superclaude/cli/install_user_setup.py:230-243`: the helper accepts only home and deadline and returns early when all three guide files exist. This is the precise existing gap the force-gated refresh proposal targets.
- `src/superclaude/cli/install_user_setup.py:245-263`: the command captures stdout and stderr, but the post-run return paths use only exit status and file presence. This supports the proposed visible skip/warning-output check. It is a source-level observation, not an observed incident cause.
- `src/superclaude/cli/install_user_setup.py:434-444`: the enclosing setup accepts force and forwards it to other helpers, but the Orca call receives only deadline. The plan changes the shared helper and this caller rather than adding a launch wrapper.
- `src/superclaude/skills/ccsession-tag/README.md:211-226`: the current README documents the Claude executable prerequisite. The plan explicitly retains it instead of claiming every agent launch already uses ccsession.

### Observed diagnostics

The fixed read-only command `timeout 120 env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE uv run --no-sync ruff check --no-fix --no-cache src/superclaude/cli/install_user_setup.py tests/cli/test_install_user_setup.py` exited 0 with `All checks passed!`. See `verify-logs/invocations.yaml` and its stdout/stderr files. This is baseline lint only, not a pytest pass or implementation validation.

Read-only Orca discovery completed: `orca skills get orca-cli --json` and `orca-ide skills install --help` exited 0. Captured excerpts and provenance are in `artifacts/orca-discovery.md`. The guide distinguishes agent-launch routes from shell creation. Installer-specific help states normal installation updates owned unmodified copies, skips edited/foreign copies, and reports skips as warnings. No live installation, dry run, UI interaction or session launch was executed.

### Review limits and degraded components

Auggie codebase retrieval was unavailable; a fresh codegraph index plus native file reads/search supplied grounding. No abstract-symbol implementor obligation or new duplicate component was proposed. Post-execution runtime-surface, sink-reachability, cross-task interaction and promotion checks do not apply to this pre-execution review.

Reviewer aliases were sonnet, haiku and opus; underlying gateway models/vendors could not be established. Executor identity was unavailable, and all three alias slots were consumed by reviewers, leaving calibration model separation degraded. Ensemble pressure was applied; bias neutralization is not established.

Memory persistence and the global cross-run metrics append were intentionally suppressed because this session is authorized to write only its review outputs. No plan, source, product code, settings, global file or other repository was edited. No implementation, remediation, global setup, commit, push, PR, GitHub mutation, Orca Task or Orca Run was performed.

## Inferred-claim audit
`citations_inferred: 0`; inferred fraction = 0/26 = 0.00. The independent evidence gate revalidated all 26 file-line evidence items with zero drops; three command claims passed through without re-execution. See `artifacts/evidence-validation.md`. The zero-drop result is retained as an audit flag, not a runtime-quality guarantee. The inferred-requirement rows are verbatim source extraction with load-bearing citations, not unsupported `[INFERRED]` report claims. No runtime-causation, global-refresh success or UI-success inference is used to support this review. Reviewer suggestions about possible future test failures remain explicitly non-blocking verification notes.

## Recommendations
No corrective plan change is required by this advisory verdict. The existing plan and source remain untouched. These are verifier details for the owning session to consider during separately authorized execution, not instructions being executed here.

### Recommendation R-001: Make the requested skip-output checks concrete

- **File:** `tests/cli/test_install_user_setup.py`.
- **Change:** Within the planned minimal tests, cover stdout-only skip text, stderr-only skip text and empty output on a forced exit-zero request with the guides already present. Assert visible skip text where supplied and no unsupported refresh-success claim.
- **Verifier:** Run the related installer tests with observed pre-fix failure and post-fix success during the planned implementation; preserve output in the plan's `artifacts/t2-tests.log`.
- **Linked deviations:** none; minor verifier refinement of Task 2.
- **Priority:** P2.

### Recommendation R-002: Keep the source's prohibition explicit in the planned guidance

- **Files:** `src/superclaude/core/CLAUDE.md`, `src/superclaude/skills/ccsession-tag/README.md` and the planned `tests/core/test_orca_session_launch_guidance.py`.
- **Change:** In the changes already requested by Task 1, state that ccsession-backed Claude CLI sessions use the agent route, never New Terminal; distinguish an explicit terminal surface on an agent launch from shell creation while preserving supervised and internal-agent boundaries.
- **Verifier:** Observe the planned static guidance checks fail before the instruction edit and pass afterwards. These checks verify wording, not UI runtime success. Relevant existing core-document tests can join the already-planned wider regression evidence.
- **Linked deviations:** none; minor wording/verifier refinement of Task 1.
- **Priority:** P2.

No remediation package, implementation invocation or new task was authored. This review ends with the machine-readable contract and the requested receipt for the owning session.
