# Stack Ranking + Adversarial Debate

## Full inventory (18 proposals)

### One-off candidates (12)

| # | Name | Agent | Complexity |
|---|------|-------|------------|
| 1 | `task_classification_contract` | 1 | simple |
| 2 | `command_validation_errors` | 1 | medium |
| 3 | `troubleshoot_escalation_contract` | 2 | medium |
| 4 | `tasklist_deterministic_shape` | 2 | medium |
| 5 | `rf_task_builder_template_handoff_contract` | 3 | medium |
| 6 | `audit_wiring_delete_guard_contract` | 3 | medium |
| 7 | `freshness_blocks_existing_unread_edit` | 4 | simple |
| 8 | `auggie_first_sticky_until_matching_tool` | 4 | medium |
| 9 | `eval_real_no_pty_smoke` | 5 | simple |
| 10 | `roadmap_tasklist_validation_pipeline` | 5 | complex |
| 11 | `sync_dev_idempotent_and_complete` | 6 | medium |
| 12 | `isolated_install_force_registers_components_and_pytest_plugin` | 6 | medium |

### Recurring candidates (6)

| # | Name | Agent | Complexity |
|---|------|-------|------------|
| 13 | `slash_command_drift_watch` | 1 | medium |
| 14 | `adversarial_task_quality_drift` | 2 | complex |
| 15 | `agent_grounding_drift_meta_eval` | 3 | simple |
| 16 | `hook_latency_and_telemetry_schema_drift` | 4 | medium |
| 17 | `installer_idempotence_release_gate` | 5 | medium |
| 18 | `installer_sync_drift_continuous` | 6 | simple |

## Ranking criteria

1. **Blast radius** — safety failures > correctness > drift > cosmetic
2. **Eval-fit** — does it require LLM/PTY/end-to-end behavior, or could a unit/CI test cover it cheaper?
3. **Cost-to-run** — simple > medium > complex (cheaper evals run more often)
4. **Catches real bugs** — has this class of failure shipped before, or is it mathematically possible?

## Round 1 ranking (PROPOSED)

### One-off (top 5)

1. `freshness_blocks_existing_unread_edit` — load-bearing safety hook, only end-to-end PTY testable
2. `eval_real_no_pty_smoke` — meta-smoke catches CLI plumbing rot
3. `task_classification_contract` — strict HTML output contract, prone to prompt drift
4. `sync_dev_idempotent_and_complete` — touches CLAUDE.md absolute rule
5. `audit_wiring_delete_guard_contract` — prevents catastrophic file deletion

### Recurring (top 3)

1. `installer_sync_drift_continuous` — guards the src/.claude SoT discipline
2. `hook_latency_and_telemetry_schema_drift` — silent degradation detection
3. `agent_grounding_drift_meta_eval` — prompt-drift watchdog for agents

## Adversarial debate

### CHALLENGE A: `sync_dev_idempotent_and_complete` doesn't fit eval framework

**Position:** This is a Makefile assertion (`make sync-dev && make verify-sync && make sync-dev && make verify-sync`). A pre-commit hook + CI step covers it cheaper. Spending an eval slot here wastes a slot.

**Counter:** The eval framework is YAML+PTY+isolated-HOME. For a Makefile test, you'd still want isolated-HOME (avoid polluting working tree). But the operation doesn't *need* the Claude Code PTY — it's pure shell.

**Verdict:** DROP from top 5. Replace with `tasklist_deterministic_shape` which tests LLM-pipeline determinism (genuinely eval-framework territory).

### CHALLENGE B: `eval_real_no_pty_smoke` is meta-circular

**Position:** Using the eval CLI to test the eval CLI doesn't catch the case where the eval CLI itself is broken (the test never runs).

**Counter:** False premise. If eval CLI is broken, smoke fails fast and CI red. The smoke covers the report-artifact contract (summary.md/json/yaml, junit.xml) which is fragile and customer-facing. Skip-path semantics (15 evals skipped with `--no-pty`) is a frequent regression vector.

**Verdict:** KEEP, but lower priority (#5 not #2). It's a sanity canary, not a high-leverage safety test.

### CHALLENGE C: `task_classification_contract` is LLM-flaky

**Position:** Asserting on LLM-generated HTML comment markers is flaky and prompt-version-sensitive. Will produce false positives in CI.

**Counter:** The contract is enforced by the skill text itself (`<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` is a marker the protocol mandates as first output). If the marker is missing, the protocol IS broken. Determinism comes from the skill, not the model.

**Verdict:** KEEP at #3. Flakiness risk acknowledged but contract is binary.

### CHALLENGE D: `installer_sync_drift_continuous` is duplicated by pre-commit hook

**Position:** `make verify-sync` already runs as a pre-commit hook + has a CI job. Recurring eval here is redundant.

**Counter:** Pre-commit can be bypassed; CI runs only on PR. A scheduled nightly eval catches drift introduced via direct merges, rebases, or environment-specific tooling differences.

**Verdict:** KEEP at #1 — independent, scheduled, catches what CI/pre-commit miss.

### CHALLENGE E: `agent_grounding_drift_meta_eval` overlaps `adversarial_task_quality_drift`

**Position:** Both test agent prompt drift; one suffices.

**Counter:** `agent_grounding_drift` tests a NARROW property (citation re-verification) cheaply. `adversarial_task_quality` is complex and tests a broader surface. The narrow+cheap eval is better for nightly cadence; the complex one is too expensive for routine runs.

**Verdict:** KEEP grounding; DROP adversarial drift from top 3.

### CHALLENGE F: `audit_wiring_delete_guard_contract` is hard to fixture

**Position:** Building a fixture repo with provider/registry/Callable/import requires substantial setup. The cost-to-value may not justify it.

**Counter:** This is a HIGH-severity safety eval. The fixture lives once, the value compounds. CLAUDE.md and audit-* agents already document the wiring rule — the eval just operationalizes it.

**Verdict:** KEEP. Move to #4 to acknowledge fixture cost.

## Final ranking (POST-DEBATE)

### One-off (top 5)

1. **`freshness_blocks_existing_unread_edit`** — safety hook, PTY-required
2. **`task_classification_contract`** — strict output contract, deterministic skill-side
3. **`audit_wiring_delete_guard_contract`** — catastrophic-loss prevention
4. **`tasklist_deterministic_shape`** — LLM pipeline determinism (promoted; replaces sync_dev)
5. **`eval_real_no_pty_smoke`** — meta-canary for eval CLI plumbing

### Recurring (top 3)

1. **`installer_sync_drift_continuous`** — SoT discipline guard, scheduled
2. **`hook_latency_and_telemetry_schema_drift`** — silent-degradation detection
3. **`agent_grounding_drift_meta_eval`** — prompt-drift watchdog

## Dropped (post-debate)

- `sync_dev_idempotent_and_complete` — better as pre-commit/CI, not eval-framework fit
- `command_validation_errors` — lower blast radius
- `troubleshoot_escalation_contract` — overlaps task_classification in fragility profile
- `rf_task_builder_template_handoff_contract` — complex setup, lower priority
- `auggie_first_sticky_until_matching_tool` — covered partially by recurring hook eval
- `roadmap_tasklist_validation_pipeline` — too complex, covered by CLI unit tests
- `isolated_install_force_registers_components_and_pytest_plugin` — overlaps installer_sync recurring
- `slash_command_drift_watch` — overlaps task_classification + audit_wiring one-offs
- `adversarial_task_quality_drift` — too complex for recurring cadence
- `installer_idempotence_release_gate` — overlaps installer_sync recurring
