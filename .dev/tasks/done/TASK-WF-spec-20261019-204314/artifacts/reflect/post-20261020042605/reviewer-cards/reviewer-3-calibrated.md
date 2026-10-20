---
reviewer_id: R3
independently_calibrated_confidence: 0.80
calibrator_diversity: degraded
---

# Reviewer 3 card — refactorer / boundary lens

Requested model slot: opus. Source and docs read in current worktree; no command/test execution. Parent has not adjudicated these findings.

## T7 coverage

All seven documentation ACs have surfaces, with disclosure gaps noted below. Linux-only default setup/menu/flags/user scope/prerequisites are disclosed (docs/user-guide/mcp-installation.md:7,9,46,48,73,121,208; docs/reference/mcp-server-guide.md:21-22). Full companions/index-preserving consent/outcomes/updater: guide221-233, reference47-50. Trust/reuse/update/list/force/target/dry-run: guide17,21-25,188. Optional runtime versus provisioning: docs/mcp/mcp-optional-design.md:1-26. Live gate procedure and block: guide309-321 and package artifacts/t7-live-smoke-gate.md. README edits are limited to install enumeration:64,75. Main help already reflects the component: src/superclaude/cli/main.py:50-52,313-322.

Disclosures missing: option 0 whole-selection failure at unsupported native scope/platform (guide46,73); provenance permission rule for group-writable canonical directories (guide25,223). These are visibility gaps, not proof that all declared behaviors are absent.

## W1-D1 — regression refuted; necessary consequence, documentation gap

Option 0 includes native (src/superclaude/cli/install_mcp.py:1284-1285); native validation at:1311-1314 rejects invalid scope/platform for the entire request. Baseline all-server ability changed, but three requirements together force the new request result: source.md:78 includes native in option 0, source.md:80 rejects invalid native scope before any write, and Task4 requires complete selection validation before effects. The reviewer's numeric Task4 anchors in its initial return were imprecise; the quoted requirements are in the supplied plan's Task4 section, not a new rule. Other-only project/local behavior remains tested in tests/cli/test_install_codebase_memory.py:1183-1190. Native Windows was unsupported in source.md:90; Mac exclusion has operator direction. Silently skipping native would change design, not repair a demonstrated regression. Add visibility/test coverage if desired rather than assume partial mutation is permitted.

## W1-D2 — advisory correctness gap, no spec-relative regression

Reachable conditional chain: ccsession mkdir (src/superclaude/cli/install_ccsession.py:37) precedes native (main.py:224 then255) and inherits umask. A 0775 canonical directory passes discovery's owner/type check (native source545-547), but post-upstream proof writing calls binary identity/directory check and rejects mode &0o022 (:92-95,173-175,682-701). Shared caller returns failure at install_mcp.py:846-848 and framework aggregate exits1. Retry reuse at native:597-605 can succeed without proof, so removal remains refused while its guard rejects that mode.

The spec does not define exact receipt predicates; fail-closed removal is consistent with ownership constraints. The inconsistency lies between sibling reuse/discovery and proof/removal predicates, so it is a no-spec advisory correctness gap. Actual host defaults and upstream mode changes were not observed; do not claim umask002 is universal or that live upstream preserves0775 without evidence.

## W1-D3 — no confirmed regression; advisory availability limit

Canonical uses absolute rather than resolved HOME (native source:55). Whole-path resolve mismatch at:88,489,539-544 rejects a link anywhere above HOME, including root-owned aliases. That can repeatedly fail native provisioning/removal on such hosts. Safe fail-closed direction is consistent with source; no spec-anchored invariant requires supporting trusted ancestor aliases. No HOME-symlink fixture was seen. Reviewer calls the broad ancestor treatment an advisory availability/correctness observation, not a security regression.

## Newly alleged canonical deviation

LOW drift: src/superclaude/cli/main.py:327 rejects mcp --list with --dry-run or non-user --scope even though those are not mutation modes. Baseline accepted them, while source.md:76 limits list rejection to mutation combinations. Current docs guide:50 disclose the stricter behavior but do not themselves provide prior user authorization. This is a compatibility/validation-scope finding, not a data-loss claim; independent debate should decide its contract interpretation.

Linux-only setup/non-Linux required-phase exit1 is authorized by operator direction plus source.md:90, disclosed guide:9. No other verified canonical deviation was found. Twelve whole reuse candidates were distinct in the bounded audit; no blocking duplicate was established.

## Ordering and limitations

Full selection validation precedes consent and non-dry prerequisites (src/superclaude/cli/install_mcp.py:1299-1334); framework native runs last and affects exit status (main.py:254-275); list returns without mutation (main.py:94-187,326-332). No new execution proof exists. Actual released installer modes, companion merge safety, persistent background processes, and a live MCP response remain separate blocked live-smoke evidence.

Evidence-only recommendations: isolated option-0 project/platform cases; a 0775 canonical-directory case covering first attempt/retry/removal; a HOME ancestor alias case locking intended guard behavior. Explain all-selection limits and the permission requirement in the guide. No code fix, test execution or live operation occurred.


## Independent blind calibration

```json
{
  "reviewer": 3,
  "card_tier": 2,
  "calibrator_model_override": "opus",
  "calibrator_diversity": "degraded",
  "scores": {
    "citation_grounding": 0.82,
    "coverage_completeness": 0.8,
    "deviation_classification_clarity": 0.85,
    "risk_surface_coverage": 0.85,
    "recommendation_actionability": 0.7
  },
  "confidence_calibrated": 0.8,
  "confidence_exact": 0.804,
  "formula": "(0.82+0.80+0.85+0.85+0.70)/5=0.804; rounded0.80",
  "self_reported_confidence": null,
  "notes": [
    "Current whole-selection, list-flag and permission-guard mechanisms were source-verified; baseline/operator/some doc support lacked exact anchors or were not spot-checked.",
    "D1 necessary interpretation is defensible under full source; D2/D3 are no-spec advisories rather than automatically regressions.",
    "List rejecting non-mutating scope/dry-run is a valid low drift candidate under source76; debate must decide, not an inherited final finding.",
    "No real umask/upstream/retry execution occurred. Risk and next-verifier precision remain limited.",
    "Opus calibrator shares one reviewer class; documented fallback diversity is degraded, not fully disjoint."
  ]
}
```
