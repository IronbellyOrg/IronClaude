# Research: Root-plugin compatibility gate review, first attempt

- **Topic type:** Independent spec-compliance QA
- **Scope:** Task 1 and plan-wide constraints
- **Status:** FAIL
- **Closed verdict:** `missing`
- **Persistence:** Reviewer-returned findings, gaps and takeaways persisted verbatim by the parent because the reviewer cannot write Markdown reports.
- **Date:** 2026-10-24
- **Template:** src/superclaude/templates/modularization-template-review/codebase-research_template.md

---

## Findings

### Acceptance criterion 1: Contract inventory and verified mappings

[CODE-VERIFIED] **UNMET.** The contract lists the 26 allowed command paths and 22 candidate source/destination pairs. However, command and agent mappings remain predictions marked `verified: false`; actual skill identifiers and plugin-relative lookup behavior remain unverified. Recording these unknowns honestly does not satisfy the required verified mapping.

Evidence: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/plugin-contract.json:2273-2751`.

### Acceptance criterion 2: Required dependencies and optional integrations

[CODE-VERIFIED] **UNMET.** The contract explicitly retains `"required_closure": null`. Its candidate file list does not establish the complete required calibration, citation-validation, restricted-reviewer and real adversarial-merge dependency mapping, or separate all optional integrations from required audit functionality. No completed result from the separate resource-tracing research is assumed.

Evidence: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/plugin-contract.json:2550-2711`.

### Acceptance criterion 3: Isolated native loader mapping proof

[CODE-VERIFIED] **UNMET; blocking handling is correct.** The stronger bare-session raw initialization explicitly rejects the plugin with `homepage: Invalid URL`. It lists only built-in plugins and no root-plugin command, skill or agent registrations. The successful model response and process result prove only that the model answered `INVENTORY_ONLY`, not that the plugin loaded.

Evidence: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/loader-bare-session.stdout.txt:3-7`.

### Acceptance criterion 4: Preservation and no external mutation

[CODE-VERIFIED] **MET within the inspected task operations.** The preservation record reports no changed protected files, restored retired assets, added candidate resources, tracked differences or index differences. Independent review checks found an empty product-only diff against the requested snapshot, identical isolated/source command, agent and skill directories, and matching isolated/source manifest hashes. The inspected harnesses write within task evidence and isolation directories and contain no remote mutation operation.

Evidence: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/preservation-check.json:2-14`.

### Manifest-preservation conflict

[CODE-VERIFIED] **A successful gate is infeasible with the observed native client and these preserved manifest bytes.** The client rejects the manifest before registering the root plugin. The plan requires both byte preservation and native mapping proof; when a protected edit is necessary, it explicitly requires stopping and obtaining revised written scope.

Evidence: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/plans/02-root-plugin.md:16-18,34-41`.

[CODE-VERIFIED] The contract correctly records the protected-manifest conflict instead of declaring compatibility or silently repairing it.

Evidence: `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/plugin-contract.json:2684-2720`.

### Classification

- **Binary verdict:** `FAIL`
- **Closed verdict:** `missing`
- **Unmet acceptance criteria:** 1, 2, 3
- **Met acceptance criterion:** 4, within inspected operations
- **extra_scope:** `[]`
- **misunderstood:** `[]`
- **Task advancement:** Blocked

## Gaps

- [UNVERIFIED] Actual root-plugin command, skill and agent mappings.
- [UNVERIFIED] Complete required dependency mapping and optional integration classification.
- [UNVERIFIED] Plugin-only audit runtime. It was correctly not exercised after compatibility failed.
- **Report-write limitation:** Higher-priority developer instructions prohibit this reviewer from writing report Markdown files. This report is returned in final text for the parent to persist verbatim. No report-file write or completed on-disk review is claimed by this reviewer.

## Key Takeaways

**Task 1 fails with closed verdict `missing`.** Product preservation holds, but native compatibility and complete dependency proof do not.

**Recommended action:** Keep Task 1 blocked and request revised written scope for the necessary protected-manifest correction. Do not change the manifest, advance to Task 2, or run later audit proofs under the current failed gate.
