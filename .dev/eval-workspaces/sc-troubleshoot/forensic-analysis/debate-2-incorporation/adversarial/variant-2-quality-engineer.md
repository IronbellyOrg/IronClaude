# Variant 2 — Quality Engineer Advocate: Incorporation Recommendations

**Voice**: opus:quality-engineer — partial to enforceability, schema rigor, testable invariants, deterministic-failure modes. Skeptical of "behavioral" guarantees not backed by code that fails loud when violated.

## Position summary

v2's hallucination contract is *behavioral* and the eval evidence shows the fallback path (inline-validate when `evidence-validator` agent unavailable) is exercised more often than is comfortable — 4 of 8 eval logs explicitly note simulated-inline calibration or validation. That undermines the contract. Forensic's *architectural* contract (orchestrator can't read source) is genuinely stronger, but converting v2 wholesale is too expensive. The QE position: **adopt forensic's enforceability discipline narrowly — schema conformance, MCP concurrency cap, return contract typing, repeat-failure detection — without adopting forensic's pipeline topology**. The QE list is more aggressive than the architect's, because the QE values defense-in-depth.

## Steelman of forensic's design

Every claim in forensic's design is paired with a testable invariant. Schemas are versioned (9 of them at M2 gate per `roadmap-2.md:215-217`). Token budgets are *targets* with `budget_status` observability fields. `test-strategy-2.md` mandates interleave ratio 1:1 — every authoring task pairs with a test/validation task. "Behavioral contract testing, not implementation testing" is the right testing philosophy. The 25-criterion adversarial rubric is mechanical and reproducible. None of this is accidental — forensic learned from 22 spec-amendment proposals before authoring began.

## Steelman of v2's design

v2's two-agent hallucination contract is genuinely innovative: `evidence-validator` for citation grounding + `confidence-calibrator` for anchoring-bias mitigation. Together they cover both the "I made up a `file:line`" failure mode AND the "I overconfidently graded my own work" failure mode. The eval evidence shows both fire correctly when available. Lazy ref-loading per wave keeps the skill load envelope tight. The conditional escalation gates are *correct* for triage workload.

## Concrete recommendations

### INCORPORATE (5 items — defense-in-depth)

1. **Schema-conformance test set for templates** (subset of C-013)
   - WHY: `refs/hypothesis-card-template.md`, `refs/report-template.md`, and the audit-log header/footer are *documentation*. Nothing fails if an agent emits a card missing a required field. The eval logs already show free-form variation; one schema-conformance test per template would catch silent regressions.
   - CHANGE: Add `tests/skills/sc-troubleshoot-protocol/test_template_schemas.py` with three tests:
     a. Hypothesis card has all required headings (Claim / Evidence / Proposed Fix / Confidence / Risks / "If I'm wrong it's probably because")
     b. REPORT.md has all required sections (Header / Summary / Diagnosis / Evidence / Proposed Fix / Alternative Fixes Considered / Risk + Rollback / Next Steps)
     c. Audit log has well-formed `SC:TROUBLESHOOT:TARGET` and `SC:TROUBLESHOOT:SUMMARY` blocks
   - WHICH WAVE: Wave 1, Wave 3, Wave 5 outputs all validated.
   - COST: ~1 day to author. ~50 lines of pytest each. Adds two minutes to `make test`.

2. **Per-server MCP concurrency cap (NFR-010 ≤3)** (from C-008)
   - WHY: Tier 2 with 4 hypothesis agents × 3 Serena queries each = 12 simultaneous calls. There is no enforcement. The first regression of "auggie rate-limited" will be a partial-grounded Tier 2 with no clear remediation. Forensic's per-server cap is enforceable in-prompt and worth ~30 tokens to specify.
   - CHANGE: Add to `SKILL.md:176-179` Wave 3 MCP enrichment step: "Issue at most 3 simultaneous queries per MCP server. When 4 hypothesis agents are spawned, agents must serialize their MCP calls per-server within their brief."
   - WHICH WAVE: Wave 3 (Tier 2 enrichment).
   - COST: Prompt update only. Negligible.

3. **Repeat-failure detection in Wave 0** (adapted from U-004 escalation gradient)
   - WHY: Re-running `/sc:troubleshoot` against the same symptom produces a fresh slug+timestamp dir but no memory of the prior pass. If the prior pass was Tier 1 with confidence 0.6, the user is likely re-running because they didn't trust it — the tool should know that and auto-elevate.
   - CHANGE: Wave 0 scans `<output-dir-root>/troubleshoot-*` for prior audit logs in the last 24h matching the current scope or first 100 chars of issue. If found:
     a. Surface notice in chat: "Previously diagnosed: <prior REPORT path>. Confidence was <X>."
     b. Force `--depth deep` if not already.
     c. Set `repeat_invocation_count` in the audit-log header.
   - WHICH WAVE: Wave 0.
   - COST: Light. Glob + audit-log header parse. ~30 lines of behavior in SKILL.md.

4. **Typed output contract via JSON Schema** (extends C-012)
   - WHY: Today the output contract is described in a Markdown table (`SKILL.md:37-54`). Callers parse the return dict with no schema. If a field is renamed, callers break silently. A JSON Schema in `refs/output-contract-schema.json` makes the contract machine-validatable.
   - CHANGE: Add `refs/output-contract-schema.json` matching the dict table. Add a Wave 5 step: validate the return dict against the schema before returning; on mismatch, write `status: partial` and surface the validation error.
   - WHICH WAVE: Wave 5.
   - COST: Medium. One schema file + validation step. ~100 lines including schema + validation logic.

5. **`test_is_wrong` flag in return contract** (from C-012)
   - WHY: When the diagnosis concludes "the test expectation is outdated, not the code", that's a critical verdict the caller must surface to the user. Today it's prose in REPORT.md and missed by tooling. Forensic surfaces this as `test_is_wrong` (`forensic-spec.md:1953-1984`). This is one boolean.
   - CHANGE: Add to output contract (`SKILL.md:37-54`) + JSON Schema (#4). Add Wave 5 detection rule (during REPORT.md synthesis, if the chosen fix is "modify the test rather than the code", set `test_is_wrong: true`).
   - WHICH WAVE: Wave 5.
   - COST: Trivial. Additive field.

### ADAPT (3 items — forensic's invariant restated for v2's harness)

6. **Adversarial fallback chain — 3 levels not 1** (adapted from forensic P-011)
   - FORENSIC: 3-level chain (retry `--depth quick` → single Sonnet scoring agent 60s/1000-token cap → emit as-is with `debate_status: "skipped"`).
   - ADAPT: v2 today (`SKILL.md:344`) has one fallback ("pick highest-confidence Tier 2 fix proposal"). Adopt the *full* chain: Level 1 retry sc:adversarial with `--depth quick`; Level 2 spawn single `quality-engineer` agent with rubric + 60s timeout + 1k-token cap to score competing fixes; Level 3 only if both fail — fall through to current "pick highest-confidence" with `debate_status: "skipped"` in audit.
   - WHICH WAVE: Wave 4 error handling.
   - COST: Light. Two new rows in error matrix.

7. **Stale-codebase detection on multi-invocation runs** (adapted from forensic FR-053)
   - FORENSIC: stale-codebase detection on resume via `git rev-parse HEAD` or mtime fallback.
   - ADAPT: When repeat-failure-detection (#3) finds a prior run, also capture current `git rev-parse HEAD` and compare against the prior. If HEAD diverged, surface "codebase changed since last troubleshoot — citations from prior REPORT may be stale" in the new audit header.
   - WHICH WAVE: Wave 0 (alongside #3).
   - COST: One Bash command + diff check. Trivial.

8. **Coordinated graceful-degradation levels in MCP handling** (adapted from C-008/C-014)
   - FORENSIC: 4-level degradation (Full → Reduced precision (Serena down) → Reduced depth (Sequential down) → Minimal (all MCP down, `--depth quick` enforced)).
   - ADAPT: v2's error matrix has component-by-component fallbacks but no *named overall mode*. Add a `degraded_mode` field to the audit header that summarises (full/reduced-grounding/reduced-debate/minimal) so the report's "Grounding Gaps" section can surface the cumulative degradation. The eval audit logs already capture component failures individually — this collates them.
   - WHICH WAVE: Wave 0 + Wave 5 (summary).
   - COST: Light. Tracked as an audit-header field.

### REJECT (forensic positions QE explicitly does NOT recommend)

- **Orchestrator-as-dispatcher with token cap** (U-003): the eval evidence shows v2's reader model produces verified-citation reports. The QE wants enforceable invariants, but the v2 invariants are *already* paired with verification (`evidence-validator`). Adding architectural withhold-access would force a complete refactor with no measurable failure-mode improvement.
- **Always-debate Phase 2 + 3b** (C-009): adversarial cost on consensus-diagnosis is pure waste.
- **8-phase pipeline / subprocess model** (C-003, C-004): the QE values testability, and v2's in-session Task model is already more testable than subprocess subprocess pipes (no mock-claude-subprocess scaffolding needed).
- **`--tier × --depth` two-axis mode** (C-010, U-001): adds a knob without a justifying failure mode.
- **Sprint-runner integration** (U-002): v2 has no sprint audience; the QE doesn't add machinery without a consumer.

## QE verdict

v2's *behavioral* contracts are good but under-defended. The eval evidence shows several agents simulated inline rather than running as Task subprocesses — that's the fallback path firing. Forensic's enforceability discipline doesn't need to be imported wholesale; it needs to be retrofitted as schemas, caps, and detection rules around v2's existing waves. The five INCORPORATE and three ADAPT items together convert v2 from "behaviorally correct" to "behaviorally correct with defense-in-depth."

Total cost estimate: ~3-5 engineering days. Total risk: low (all additive; nothing changes existing successful paths).

Final confidence: 0.91 on the 5 INCORPORATEs (each has a concrete failure mode and a small, testable mitigation), 0.78 on the 3 ADAPTs (need calibration in eval but the failure modes are real), 0.85 on the RJECTs (forensic positions are workload-mismatched and would harm v2's strongest paths).
