---
reviewer_id: R2
independently_calibrated_confidence: 0.78
calibrator_diversity: degraded
---

# Reviewer 2 card — QA

Requested model slot: haiku (configured alias observed as grok-4.7[1m]). Current source/test-body evidence only; no commands/tests executed. Original review plus its explicit citation erratum are represented here. Parent has not adjudicated the classifications.

## Assigned completion

T1/T3/T6 comprise 20 ACs. Reviewer reports 19 fully adherent plus one necessary Mac exclusion, with no drift or regression. The exclusion is supported by the operator's explicit Linux-first direction; the reviewer's necessary-versus-authorized label is preserved for calibration.

- T1: platform/scope rejection precedes effects; Linux aliases pass (src/superclaude/cli/install_codebase_memory.py:582-595; tests/cli/test_install_codebase_memory.py:46-76). Canonical/external reuse and ambiguous-state failure:529-610, tested:85-188. Acquisition-only curl/Bash:612-621; argv-only complete bootstrap:631-665. Absolute version probe:512-522. Structured expected failures:693-700. Authored isolated cases and real benign reaper fixtures exist; not freshly run.
- T3: command is canonical uninstall -y with explicit directory, no index-delete flag (native source:312-314). Receipt/identity uncertainty stops before process:304-311. Preview:74-78. Residual user-only cleanup and partial/absent handling: src/superclaude/cli/install_mcp.py:902-993. Relevant mock tests: tests/cli/test_install_codebase_memory.py:558-564,623-643,646-706 and tests/cli/test_install_mcp_tavily.py:920-995. Sentinels/updater stay, no blind second cleanup. Cases are authored, not freshly run.
- T6: all four files contain the declared matrix; cross_entry_lifecycle at tests/cli/test_install_codebase_memory.py:1278-1409 keeps production discovery, proof, registration and coordinators active with external process effects mocked. Native unlink is performed by the fake process boundary, not a live uninstaller (:1356-1363). CLI-only mcp_cli fixture has canned lifecycle values (:821-835), so those tests prove dispatch/validation, not external effects. This distinction is explicit. Historical execution artifact is 71 lines: artifacts/t6-cli-regressions.txt:49-53 records exit 0, 242 passed, one gated skip. Original 907-910 citation was a brief offset and was withdrawn/corrected after direct Read.

## Candidate dispositions

### W1-D1 — regression refuted

Option 0 or any selection containing native at project/local scope or unsupported platform is rejected before any selected effects: src/superclaude/cli/install_mcp.py:1284-1285,1311-1314,486-496. Full source requires whole-selection validation before effects and rejection of invalid native scope; silently dropping native is not the same contract. Valid mixed gateway/native requests execute both and aggregate runtime failures. Other-only project/local selections remain supported (tests/cli/test_install_codebase_memory.py:1179-1190). Mixed invalid scope is directly tested (:964-979); Windows follows the same unsupported-system predicate as Darwin (:982-988). Lack of a Windows/menu-zero-named test is not a new behavioral contract.

### W1-D2 — mechanism real, no confirmed regression

Group/other-write rejection is a real fail-closed ownership rule at native source:85-99,110-116. Discovery/reuse use a different predicate at:545-552,597-605. If released setup leaves a 0775 canonical directory, proof creation can fail after successful upstream execution at:673-700; retry can reuse without proof. ccsession mkdir at src/superclaude/cli/install_ccsession.py:37 follows the process umask, but no actual host/upstream mode was observed. Historical fixtures only show their own modes worked. This is an advisory sibling-contract mismatch, not demonstrated shipping false failure or spec regression.

### W1-D3 — regression refuted

Path.home().absolute preserves links; resolve mismatch at native source:88-89,538-544 rejects a symlinked ancestor before download. Source explicitly requires symlink/ownership ambiguity to fail closed. No real HOME was inspected, and no post-success false result was demonstrated.

## Canonical deviation / advisory separation

The reviewer labels Linux-only automation as necessary at native source:590, supported by package artifacts/operator-direction.md:5-8 and Darwin tests:64-76. No drift/regression was verified. Explicit operator authority may affect its final taxonomy label; this card does not invent missing user consent.

Advisory correctness gap: discovery accepts a user-owned canonical directory whose mode the proof/removal checks reject; source sibling predicates native:545-552 versus:85-99,102-116. No new code mutation is proposed here.

## Evidence limits and errata

No fresh verification. Current invocations.yaml is empty. Original operator-direction/capability-status/invocation citations came from brief hunks, not direct reads; the reviewer explicitly qualifies them. Product/test citations were direct reads. Later bookkeeping was read: two Click callbacks are DEGRADE by decorator oracle, never UNREACHED; four overlaps have three direct-text-cross-reference risk flags, with the explicit T3/T4 dependency overlap benign. Those are structural risks, not proof of defects.

Live released-binary/merge/MCP-handshake behavior remains pending separate authorization. No installation, removal, edits, or commands occurred. Evidence-only next step is an isolated 0775 compatibility case and sanctioned fresh verification when available; historical pass counts are not new results.


## Independent blind calibration

```json
{
  "reviewer": 2,
  "card_tier": 2,
  "calibrator_model_override": "opus",
  "calibrator_diversity": "degraded",
  "scores": {
    "citation_grounding": 0.85,
    "coverage_completeness": 0.85,
    "deviation_classification_clarity": 0.75,
    "risk_surface_coverage": 0.85,
    "recommendation_actionability": 0.6
  },
  "confidence_calibrated": 0.78,
  "confidence_exact": 0.78,
  "formula": "(0.85+0.85+0.75+0.85+0.60)/5=0.78",
  "self_reported_confidence": null,
  "notes": [
    "Spot-checked source/test/operator/log citations matched, including corrected historical test-evidence lines49-53.",
    "Necessary-versus-authorized Linux label and unanchored exact permission-mode policy reduced classification clarity; advisory correctness observations are not a fifth deviation class.",
    "Source/test bodies and historical results are correctly separated from fresh execution.",
    "Twenty assigned ACs are summarized rather than individually anchored; recommended next cases lack precise success criteria."
  ]
}
```
