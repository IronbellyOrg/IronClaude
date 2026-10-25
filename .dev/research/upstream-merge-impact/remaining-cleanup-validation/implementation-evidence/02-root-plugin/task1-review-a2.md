# Research: Revised root-plugin compatibility gate

- **Topic type:** Independent adversarial acceptance review
- **Scope:** Task 1 after user-approved homepage correction
- **Status:** FAIL
- **Closed verdict:** `missing`
- **Persistence:** Fresh reviewer findings persisted verbatim by parent before use; this review predates the user's second scope revision.
- **Date:** 2026-10-24
- **Template:** src/superclaude/templates/modularization-template-review/codebase-research_template.md

## Findings

Task 1 independent review: FAIL; verdict=missing; extra_scope=[]; misunderstood=[].

[CODE-VERIFIED] AC1 MET: contract records retained command/agent mappings, all 22 candidate source/destinations, the 26 allowed command paths, skills and plugin-root lookup rule at /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/plugin-contract.json:2273-2887. I independently recomputed all 2,259 non-manifest protected hashes: zero differences; original/corrected manifest hashes also match.

[CODE-VERIFIED] AC2 UNMET: the contract's required_closure is still null and blockers is empty; candidate filenames/frontend identities are not a required-versus-optional dependency-edge map. Evidence: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/plugin-contract.json:2830-2831. This does not fault Task 1 for not yet installing Task 3 resources; it faults the missing Task 1 source-requirement mapping/classification required by /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/plans/02-root-plugin.md:36-40. The separate closure agent's pending work has not been assumed complete.

[CODE-VERIFIED] AC3 UNMET overall, although native identity discovery succeeds: actual candidate inventory lists sc:sc-* commands, sc:sc-reflect-protocol and sc:sc-adversarial-protocol, six new roles and retained specialists, but no scan/refactor/migrate/deploy/code-to-spec commands. Inventory: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/loader-candidates-init.json:50-82,132-166. Raw candidate/external session logs each show the real plugin init, an INVENTORY_ONLY response and successful result, not an audit run. Unresolved references must remain blocking under /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/plans/02-root-plugin.md:41; contract blockers=[] does not record the confirmed incompatible references.

[CODE-VERIFIED] AC4 MET for observable local scope: diff against 2f98141c36d9599c40d719b63aca7d70af8ac3d5 deletes exactly the empty homepage line and scoped product status has only that manifest modified, with no untracked product additions. Independent byte comparison confirms every other manifest byte unchanged and the original baseline hash retained. Evidence: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/02-root-plugin/plugin-contract.json:2866-2870. Probe records use an external temporary cwd, isolated HOME/config and strict empty MCP; no evidence of user-global or remote mutation was found.

## Gaps

[CODE-VERIFIED] Confirmed blocking written-scope conflict: real runnable recommendations reference absent scan and refactor at /config/workspace/IronClaude/.dev/worktrees/ci-followup/commands/sc-recommend.md:145,165,186; absent migrate at :406; absent deploy at :498. The spec workflow invokes absent code-to-spec at /config/workspace/IronClaude/.dev/worktrees/ci-followup/commands/sc-spec-panel.md:351-357. These are actual advertised commands, not pseudo memory paths or namespace prose. I exclude /sc:sc namespace descriptions, plan/execution/evaluation memory pseudo-paths and ./sc:authentication_service from this finding.

[CODE-VERIFIED] Namespace-only spelling cannot register an absent command. Honest unavailable annotations in these two root commands are NOT permitted by the current scope: namespace-only edits are mandated and other prose remains byte-identical, with only two help-row deletions and reflection behavior excepted. Evidence: /config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/plans/02-root-plugin.md:17-18,22,54,57-58. Neither substituting a different command nor labeling these examples external is merely a namespace correction; both require revised written scope. Existing optional-unavailable permission does not override those explicit restrictions.

## Key Takeaways

The homepage fix closes the manifest-loading blocker, not Task 1. Recommended action: record the five absent command targets as blockers, obtain a narrowly written scope revision allowing honest unavailable annotations (or another explicitly approved disposition) in the two named commands, finish the required-versus-optional source closure map, and repeat Task 1 review before Task 2 product edits. No product files or report files were edited; no full test suite, retries or troubleshoot reports were read.

| Status | Result |
|---|---|
| DONE | Independently verified manifest-only diff, protected hashes, native mappings and five genuinely absent command targets. |
| NEXT | Persist this review; keep Task 1 blocked pending written-scope revision and source-closure evidence. |
