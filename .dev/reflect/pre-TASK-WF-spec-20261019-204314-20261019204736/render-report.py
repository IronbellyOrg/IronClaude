"""Render the bounded advisory PRE report from review-only artifacts."""
import json
from pathlib import Path
O=Path(__file__).parent
R=Path('/config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP')
S=R/'.dev/tasks/to-do/TASK-WF-spec-20261019-204314/source.md'
P=S.with_name('TASK-WF-spec-20261019-204314.md')
M=json.loads((O/'artifacts/coverage-matrix.yaml').read_text())
text=f'''# Codebase Memory PRE Review

```yaml
contract_version: 1.7.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.73
confidence_scope: initial T1 card only; no final merged or per-card T2 calibration
coverage_degraded: parsed-sparse
coverage_pct: null
coverage_pct_union: 0.7745
citation_budget_policy: full_reread
```

## Verdict and boundaries

This is a **partial advisory PRE review**, not implementation approval, a completed adversarial verdict, or evidence of product correctness. The plan and source remain unchanged. No implementation, tests, builds, remote installation, native removal, git mutation, publication or task promotion occurred. Review-generated files are confined to this worktree's `.dev/reflect/`.

The five phases and seven implementation-bearing tasks cover acquisition, registration, removal, command integration, framework provisioning, regression authoring and documentation. Scope/dependency structure is coherent. No HIGH/MEDIUM confirmed plan omission was established in the bounded review. LOW acceptance-precision concerns remain advisory and unmerged. **The parent must not modify the plan based on these findings.**

## Coverage matrix

- Parsed requirement IDs: **0**. Parsed-only coverage is **null**, not 0% or 100%.
- Quote-pinned inferred rows: **102**; deterministic matches: **79**; literal nonmatches: **23**; union **77.45%**.
- These are literal-containment results, **not 23 demonstrated omissions**. The semantic crosswalk in `artifacts/nonmatch-dispositions.yaml` provides support pointers without changing deterministic counts. Compound rows and task-wide vocabulary also create false positives and misattribution, so a match is not proof of exact acceptance coverage.
- Extraction limit: the implementation-time revalidation imperative in {S}:44 is not a matrix row; it is addressed by {P}:25 and :36. Therefore the matrix is not proof of exhaustive atomization.
- Routing: parsed-sparse is a table-wide Tier-2 prefilter; code/tests/docs also triggers rule 4. Seven tasks; three domains; literal S_dev_density = 23/102 = 0.22549. This density is not a defect estimate.

## Findings and advisory gap registry

### F-01 — Exact user registration is the main implementation risk; already owned by Task 2

Existing lookup treats nonzero/error as absence ({R}/src/superclaude/cli/install_mcp.py:546-566); command parsing flattens argv ({R}/src/superclaude/cli/install_mcp.py:569-594); generic reconciliation checks command but not target scope ({R}/src/superclaude/cli/install_mcp.py:697-704) and can remove without an explicit scope ({R}/src/superclaude/cli/install_mcp.py:719-725). Task 2 already requires failure/absence distinction, exact user-scope verification, lossless stale-entry rollback, path-space and shadowing tests ({P}:61-70), consistent with {S}:102. **Not a missing task.**

[INFERRED] A supported, lossless hidden-user-entry lookup/restore mechanism still needs proof during authorized implementation. This review has not established external CLI capability. Advisory verifier: Task 2's existing registry/Tavily test obligations; no action or plan edit authorized now.

### F-02 — Existing shell helper is unsuitable for blindly reused native lifecycle calls

The POSIX helper executes a joined command with `shell=True` ({R}/src/superclaude/cli/install_mcp.py:121-128). Task 1 explicitly requires direct argv execution and bounded installer-tree termination ({P}:40 and :46). This is an implementation trap in reusing existing helpers, **not a plan contradiction**. Advisory verifier during authorized implementation: the already-planned native argv/timeout/cleanup tests, including Task 3's removal cases ({P}:91).

### F-03 — LOW acceptance-precision candidate: positive dry-run disclosures

The source explicitly requires dry-run to show planned acquisition/registration/removal, source URL, user-level effects and index retention ({S}:117). Task 4 explicitly prohibits dry-run mutation/prompts but does not individually restate those positive display assertions ({P}:111); Task 6 likewise emphasizes prompt/mutation isolation ({P}:145). The explicit MCP path mentions disclosed setup ({P}:109), while the most explicit URL/destination disclosure acceptance line is in framework-install Task 5 ({P}:122).

This is an **acceptance-test precision risk**, not an established missing behavior: the frozen source remains authoritative and Task 4 imports its relevant sections ({P}:20 and :101). A reviewer labeled it a LOW wording gap; it has not survived an adversarial adjudication. Advisory verifier: positive output assertions when implementing the existing Task 4, with no plan rewrite now.

### F-04 — Do not promote the claimed uninstall-scope omission into a confirmed gap

One reviewer claimed uninstall scope validation lacked a per-task assertion. The global constraint explicitly limits the **full native lifecycle** to user scope and rejects other scopes before native effects ({P}:21), and Task 4 validates complete selections/options before any effects ({P}:103). Removal tests cover unsupported modes/scopes ({P}:113). The source obligation is {S}:108. Thus a claimed complete omission is not supported; at most, there is a LOW test-specificity watchpoint. No new task is warranted by this review.

### F-05 — Live upstream merge safety is an intentionally open release gate

Source requires separate authorization and a disposable-environment live smoke ({S}:151). Task 7 preserves that procedure and release block ({P}:156-164). Mocked tests cannot prove upstream companion-file merge preservation. This gate remains **pending**, not passed and not a workflow omission. No live smoke ran here.

## Grounding gaps and unfinished mandatory protocol stages

- Serena is bound to the main checkout; activation/current-config tools are not exposed. Worktree-correct symbolic referrers/diagnostics, memory hydration/persistence and scripted think checkpoints could not run. Exact-path Reads and focused Auggie retrieval are the fallback. No config changes were attempted. `grounding-gaps.yaml` records these limits.
- Executor class is unresolved. The resolved reviewer aliases are Sonnet/Haiku/Opus, with Haiku mapped to a different provider. Vendor/model diversity of aliases does not prove runtime anti-confirmation sufficiency.
- Independent blind T1 calibration is **0.73** (five scores: .70/.58/.90/.75/.72). The first coarse-anchor result was superseded after the same blind instance received the actual five-dimension continuous rubric. The semantic nonmatch crosswalk was not in its card; no retroactive score uplift is claimed.
- Tier-2 restricted reviewer cards are collected separately. **Independent per-card Tier-2 calibration and the full sc-adversarial debate/scoring/merge were not completed in this bounded advisory review.** The skill is installed; it is NOT falsely reported unavailable. There is no merge method, convergence score or completed merged verdict. This unfinished mandatory work independently forces `status: partial`; raw reviewer agreement is not a substitute.
- Evidence validation is the final independent citation gate. Its artifact records actual checks and drops; a zero-drop outcome is an audit flag, not a fabricated clean verdict. Input hashes are rechecked separately.
- Remediation was not requested. No handoff or task-builder execution. UC-1 promotion is not applicable.

## Inferred requirements (Pass 2)

Each quote below is load-bearing extraction evidence, not a non-load-bearing inferred opinion. Deterministic matching uses unique case-folded alphanumeric words, a fixed stopword set recorded in `artifacts/coverage-matrix.yaml`, a 0.6 threshold, and single-task best match with first-task tiebreak. Global constraints are not injected into individual tasks. All quotes are limited to two sentence spans and pinned to exact source lines.

| ID | Verbatim quote | Citation | Match result |
|---|---|---|---|
'''
for row in M['matrix']:
    quote=row['quote'].replace('|','\\|').replace('\n',' ')
    match=', '.join(row['matched_task_ids']) or 'none (literal matcher)'
    text+=f"| {row['requirement_id']} | {quote} | {row['citation']} | {match}; {row['containment_ratio']:.4f} |\n"
text+='\nPostscript: Independent validation results and any dropped claims/rows are in `artifacts/evidence-validation.yaml`. Machine quote check found no mismatches before dispatch. No semantic crosswalk was used to inflate the deterministic union percentage.\n'
(O/'REPORT.md').write_text(text)
print(f'Rendered {O / "REPORT.md"} with {len(M["matrix"])} inferred rows.')
