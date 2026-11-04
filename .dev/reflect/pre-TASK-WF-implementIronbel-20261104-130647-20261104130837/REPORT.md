# Reflect report: pre-execution review of the issue #357 plan

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.72
citations_total: 25
citations_revalidated: 25
citations_dropped: 2
citations_inferred: 1
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Spec: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/source.md
Tasklist: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md
Tier decision: Tier 2 (rule 4, four domains; coverage_degraded parsed-sparse pre-filter). Reviewers: sonnet/analyzer, haiku alias glm-5.3/qa, opus/refactorer; calibrator opus (calibrator_diversity degraded); merge via sc-adversarial-protocol (convergence 0.92, BLOCKED_BY_INVARIANTS on INV-004 and INV-027). Merged verdict: adversarial/merged-verdict.yaml.

## Coverage

Pass 1 found 0 labeled IDs; Pass 2 inferred 12 requirements from source.md:1. coverage_pct null (parsed-only); coverage_pct_union 0.75; unmapped by the word-overlap rule: INF-001, INF-002, INF-006. Semantic review (artifacts/coverage-matrix.yaml semantic_notes) finds INF-001 and INF-006 delivered by Tasks 1-3 and INF-002 (read the issue first) a process step reflected in the Constraints. Every issue Done-when bullet maps to a task.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | block bare python, python3, pip and pip3 in Bash tool calls with a PreToolUse hook, ... | source.md:1 | none (0.58) |
| INF-002 | Read the issue in full first (gh issue view 357 --repo IronbellyOrg/IronClaude) | source.md:1 | none (0.30) |
| INF-003 | uv run python | source.md:1 | Task 1 |
| INF-004 | uv pip | source.md:1 | Task 1 |
| INF-005 | uvx | source.md:1 | Task 1 |
| INF-006 | commands that only mention python in paths, patterns or quoted text | source.md:1 | none (0.50) |
| INF-007 | src/superclaude/hooks/hooks.json, plugins/superclaude/hooks/hooks.json | source.md:1 | Task 1 (real: Task 3) |
| INF-008 | src/superclaude/hooks/scripts/, plugins/superclaude/hooks/scripts/ | source.md:1 | Task 1 |
| INF-009 | src/superclaude/cli/install_hooks.py | source.md:1 | Task 3 |
| INF-010 | the existing PreToolUse freshness-pre-edit hook as the model | source.md:1 | Task 3 (real: Task 1) |
| INF-011 | the bare call to replace in .../read-parse.md:8 | source.md:1 | Task 5 |
| INF-012 | the Done-when list, which is the acceptance criteria | source.md:1 | Task 1 |

## Blocking findings (implement-time amendments; the plan file is not edited)

### B-1: Task 3 breaks an existing test that no task runs
- Evidence: tests/hooks/test_freshness_subagent_start_policy.py:102-105 asserts no PreToolUse registration has matcher "Bash"; the plan adds one at TASK-WF-implementIronbel-20261104-130647.md:73; Task 4 runs only tests/cli and tests/unit (TASK-WF-implementIronbel-20261104-130647.md:95).
- Fix: replace the assertion with an allowlist (Bash-matcher PreToolUse commands == {block-bare-python.sh}); run tests/hooks/ in Task 4; name the supersession in the PR body. (R1-F1, AMD-01)

### B-2: Task 2's own criterion cannot be met
- Evidence: TASK-WF-implementIronbel-20261104-130647.md:64 requires `;` in an allowed case; the allowed list at TASK-WF-implementIronbel-20261104-130647.md:58 has no unquoted `;` chain (its only `;` characters sit inside a quoted `python -c` string).
- Fix: add allowed `;` cases. (R1-F2, AMD-02)

### B-3: Quoted command substitution runs bare python unblocked
- Evidence: TASK-WF-implementIronbel-20261104-130647.md:37 makes text inside double quotes never a command word, so `x="$(python3 -c 1)"` passes, against the Done-when at TASK-WF-implementIronbel-20261104-130647.md:19.
- Fix: nested command contexts for `$(` and backticks inside double quotes. (R1-F5, AMD-04)

### B-4: The split rule is not a shell lexer
- Evidence: heredoc bodies are scanned as ordinary lines (TASK-WF-implementIronbel-20261104-130647.md:40); apostrophes in bodies or comments desync quote state; the multi-line `git commit -m "$(cat <<'EOF' ...)"` form is wrongly blocked.
- Fix: one stateful awk scanner on stdin with quote, comment, continuation, nested-context and heredoc states (M-SCANNER rules (a)-(f), AMD-03, AMD-05).

## Minor findings
R1-F3 (Task 5 refinement note), R1-F4 (continuation inside the scanner), R1-F6 (fail-open by construction, jq-missing test, jq precondition), R1-F7 (run Task 1 before Task 5), R1-F8 (Goal wording; MDTM template follow-up), R1-F9 (CHANGELOG scope addition), R1-F10 (default-HOME install test), R1-F11 (~200 KB stdin case), M-HEREDOC-TEXT, M-TASK7 (no bypassPermissions; refusal is blocked not pass), M-CONSTRAINTS (Constraints line 20 says Task 6 for the live check: TASK-WF-implementIronbel-20261104-130647.md:20), M-ARRAY, M-CEILINGS, M-AWK-LOCALE, M-COVERAGE. Details: adversarial/merged-verdict.yaml.

## Grounding Gaps (dropped citations)

The Wave 5 evidence validator re-read all 25 citations and dropped 2; the claims below were removed from the body.

### Gap G-1
- Hunk ref: B-4, "invariant probe ran 15 bash cases where python ran unblocked or a path was blocked (adversarial/invariant-probe.md)"
- Evidence missing: invariant-probe.md states no count of 15 (27 rows; E-labels E1-E15 plus E9b, E9c; E2 and E14 are different case kinds) and the citation had no line.
- Why not classifiable: unsupported count.
- Next evidence needed: cite specific rows (INV-003 to INV-013) if the claim is reinstated.

### Gap G-2
- Hunk ref: minor findings, "templates/workflow/02_mdtm_template_complex_task.md:965"
- Evidence missing: path does not resolve from the repo root; the file is src/superclaude/templates/workflow/02_mdtm_template_complex_task.md (line and content correct).
- Why not classifiable: unresolvable path as written.
- Next evidence needed: none for the finding itself (R1-F8 in adversarial/merged-verdict.yaml keeps it); cite the full src/ path when reused.

## Inferred-claim audit
- `citations_inferred: 1`
- [INFERRED] `claude -p --settings <file>` merges its hooks with the user's hooks; the hooks documentation states merging across settings levels but does not name `--settings` explicitly.

## Recommendations

### R-001: Apply AMD-01..AMD-08 during /sc:implement and record them in progress.md
- File: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/progress.md (created by /sc:implement)
- Change: record each amendment against the task it changes; implement Task 1 with the M-SCANNER rules; add the listed Task 2 cases; narrow the pinned test; run tests/hooks in Task 4.
- Verifier: `uv run pytest tests/hooks tests/cli/test_install_hooks.py -q` passes; the M-SCANNER E-cases are parametrized ids in tests/hooks/test_block_bare_python.py.
- Linked: B-1, B-2, B-3, B-4
- Priority: P0
