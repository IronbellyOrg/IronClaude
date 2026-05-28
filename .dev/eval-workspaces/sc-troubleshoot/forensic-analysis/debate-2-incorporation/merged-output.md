# Incorporation Classifications — All 31 Substantive Differences

**Purpose**: Final classification table covering all 31 substantive differences from `debate-1-differences/merged-output.md`, with adversarial-debate-derived verdicts.

**Verdicts**:
- **INCORPORATE** — forensic's approach is reliably better; v2 should adopt (with adaptations where noted).
- **REJECT** — forensic's approach is wrong for v2's workload; v2 should keep its current shape.
- **ADAPT** — forensic's approach has merit, but a modified form fits v2 better.
- **DEFER** — would need eval data before deciding.
- **SHARED** — both designs already do this or both approaches are equivalent for v2's workload; no change needed.

## Classification Table

| ID | Title | Tier | Cluster | Verdict | Rationale (≤2 sentences) |
|----|-------|------|---------|---------|--------------------------|
| S-001 | Top-level shape (single doc vs multi-file bundle) | T1 | — | SHARED | Different artifact types serving different consumers; both correct for their workloads. |
| S-002 | Section count for spec content | T1 | — | SHARED | Documentation-style choice; no behavioral impact. |
| S-003 | Refs strategy (monolithic vs lazy-per-wave) | T4 | — | SHARED — v2 better | v2's lazy-per-wave is the right call for an in-session skill; no incorporation. |
| S-004 | Authored layering | T2 | — | SHARED | Both layer command → skill → refs → agents; same pattern. |
| S-005 | Document type (analysis vs implementation) | T4 | — | SHARED | Different deliverable shapes; no behavior delta. |
| C-001 | Scope of problems addressed | T1 | — | REJECT | Forensic's project-wide-sweep on no-symptom is wrong for v2's symptom-driven workload (v2's STOP rule is correct — see `eval-wave0-stop-vague-input/`). |
| C-002 | Activation mechanism | T2 | — | SHARED — v2 better | v2's aggressive keyword-trigger surface is the right fit for an interactive command. |
| C-003 | Tier / phase structure | T1 | — | REJECT | Forensic's 8 always-on phases would destroy v2's Tier-1-stop-on-high-confidence path (eval-3 missing-import: 60s, confidence 1.0). |
| C-004 | Execution model (subprocess vs in-session) | T3 | A | REJECT | v2's in-session Task model is correct for interactive use; subprocess pipeline solves a problem v2 doesn't have. |
| C-005 | Orchestrator role (dispatcher vs reader) | T3 | A | REJECT | v2's reader model paired with `evidence-validator` post-hoc gives equivalent hallucination resistance without the architectural conversion cost. |
| C-006 | Agent inventory (subprocess vs Task) | T3 | A | REJECT | v2's two new agent files (`evidence-validator`, `confidence-calibrator`) are the right shape for in-session use. |
| C-007 | Model tiering (Haiku/Sonnet/Opus matrix) | T4 | — | REJECT | v2's per-agent default + `--models` override is simpler and adequate; forensic's matrix is overkill without an Opus-orchestrator pin. |
| C-008 | MCP usage by phase (routing table + concurrency cap) | T4 | — | INCORPORATE (cap subset) | Per-server concurrency cap (≤3) is a cheap latent-risk mitigation; routing table is workload-specific and rejected. |
| C-009 | Adversarial coupling pattern (always vs maybe) | T2 | — | REJECT | v2's skip-on-consensus is the right cost optimization; eval-3 missing-import would waste 30-60k tokens under always-debate. |
| C-010 | Two-axis vs single-axis mode (`--tier × --depth` vs `--depth` only) | T2 | — | REJECT | v2's conditional escalation gates give equivalent cost control without the orthogonal knob; cognitive overhead unjustified. |
| C-011 | Token budget profile (per-phase table vs per-tier band) | T4 | — | REJECT | v2's per-tier band is the right granularity for an interactive command; per-phase caps add enforcement complexity for no observed overrun. |
| C-012 | Output contract (`test_is_wrong` flag) | T1 | — | INCORPORATE | `test_is_wrong: bool` in return contract is high-leverage / low-cost for the asymmetric "test is the bug" case; rest of forensic's contract fields are TFEP-specific and rejected. |
| C-013 | Test strategy (10-file gated infra vs eval-workspaces) | T2 | — | INCORPORATE (schema subset) | Schema-conformance tests for hypothesis-card + REPORT.md + audit-log are cheap and address observed format variation; rest of forensic's M6 machinery is overkill. |
| C-014 | Failure handling (coordinated chain vs per-component matrix) | T2 | — | ADAPT | Insert single-agent scoring fallback intermediate level before "pick highest-confidence" for adversarial failure; rest of forensic's chain (git rollback, subprocess SIGTERM) doesn't apply to v2. |
| C-015 | CLI / sprint-runner integration | T3 | A | REJECT | v2 has no sprint-runner audience; `sprint/tfep.py` solves a problem v2's workload doesn't have. |
| C-016 | Hallucination contract (paired w/ U-003/U-005) | T1 | — | SHARED — orthogonal | v2's post-hoc validation (`evidence-validator` + `confidence-calibrator`) is functionally equivalent for v2's harness; neither dominates. |
| C-017 | Remediation chain (auto-re-launch vs user-initiated) | T1 | — | REJECT | v2's diagnosis-first + user-initiated `/task` is correct for an interactive symptom-triage tool; auto-re-launch is sprint-pipeline-specific. |
| C-018 | Lifecycle / checkpointing | T3 | — | INCORPORATE (repeat-detection subset) | Wave 0 repeat-failure detection in last 24h is high-leverage; full resume primitive is deferred because v2's interactive workload doesn't yet need it. |
| U-001 | `--tier × --depth` two-axis mode (forensic-only) | T2 | — | REJECT | See C-010. |
| U-002 | `sprint/tfep.py` CLI module (forensic-only) | T3 | A | REJECT | See C-015. |
| U-003 | Orchestrator-as-dispatcher prohibition (forensic-only) | T1 | A | REJECT | See C-005. |
| U-004 | 3-tier escalation gradient (forensic-only) | T3 | — | INCORPORATE (Wave-0 repeat-detection subset) | The "repeat trigger → escalate depth" behavior is the high-leverage subset; the full TFEP `EscalationState` is rejected as sprint-runner-specific. |
| U-005 | `evidence-validator` + `confidence-calibrator` agent files (v2-only) | T1 | — | SHARED | v2 already has these; no change needed; nothing to incorporate from forensic. |
| U-006 | Lazy ref loading per wave (v2-only) | T4 | — | SHARED — v2 better | v2 already has this; no change needed. |
| A-001 | Shared assumption: adversarial-debate-as-adjudication | shared | — | NO ACTION | Both designs depend on this; the choice isn't forensic-introduced; addressing it is out-of-scope for incorporation work. |
| A-002 | Shared assumption: static-Markdown-report | shared | — | NO ACTION | Both depend on this; same rationale as A-001. |

## Verdict Counts

- **INCORPORATE**: 5 items — C-008 (cap subset), C-012 (`test_is_wrong`), C-013 (schema subset), C-018 (repeat-detect), U-004 (Wave-0 detection)
- **ADAPT**: 1 item — C-014 (single-agent adversarial fallback)
- **REJECT**: 14 items — C-001, C-003, C-004, C-005, C-006, C-007, C-009, C-010, C-011, C-015, C-017, U-001, U-002, U-003
- **DEFER**: 3 items — JSON Schema for output contract, stale-codebase detection, named degradation modes (these are QE's deferred items from Round 2; not in the 31-diff catalogue but surfaced by the debate)
- **SHARED / NO ACTION**: 11 items — S-001, S-002, S-003, S-004, S-005, C-002, C-016, U-005, U-006, A-001, A-002

Total: 31 + 3 deferred-items = 34 verdicts. (The 3 deferreds are debate-surfaced, not in the original 31; they appear here because the incorporation report needs to enumerate them.)

## Final Convergence Statement

100% unanimous after Round 2 rebuttals across all 31 diff points. No HIGH-severity UNADDRESSED invariants. 5 MEDIUM-severity invariants surfaced as implementation gotchas (see `incorporation-report.md` for details).

The full actionable roadmap — with which v2 files change, which waves change, why each item ships, and the recommended order of operations — lives in `incorporation-report.md`.
