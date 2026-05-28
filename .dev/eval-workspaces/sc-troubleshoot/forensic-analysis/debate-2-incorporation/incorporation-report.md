# `/sc:forensic` → `sc:troubleshoot` v2 — Incorporation Report

**Generated**: 2026-05-21 via `/sc:adversarial` Mode B simulation (3-advocate debate at `--depth standard` + Round 2.5 sufficiency-challenge invariant probe).
**Convergence**: 100% unanimous after Round 2 rebuttals across all 31 diff points + 3 debate-surfaced items.
**Inputs**:
- `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/forensic-analysis/forensic-breakdown.md`
- `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/forensic-analysis/debate-1-differences/merged-output.md`
- `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/*.md`
- `/config/workspace/IronClaude/src/superclaude/agents/{evidence-validator,confidence-calibrator}.md`
- `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/iteration-{1,3}/`

---

## 1. Executive Summary

`/sc:forensic` and `sc:troubleshoot` v2 are not competing designs. They target genuinely different workloads:

- **Forensic** = project-wide investigation with multi-phase data-flow contracts, subprocess pipeline, sprint-runner integration, and architectural hallucination resistance (orchestrator-as-dispatcher).
- **v2** = symptom-driven diagnosis with conditional escalation, in-session Task agents, aggressive auto-activation, and behavioral hallucination resistance (`evidence-validator` + `confidence-calibrator`).

The honest read of the 31 substantive differences from debate #1 is: **the two designs are mostly orthogonal, and v2 is approximately right for its workload**. Importing forensic's *core architectural moves* (subprocess pipeline, orchestrator-as-dispatcher with token cap, 8-phase always-on pipeline, sprint-runner integration) would harm v2 — they solve problems v2's interactive symptom-triage workload doesn't have, and they would destroy the Tier-1-stop-on-high-confidence path that the eval evidence shows working (eval-3 missing-import: 60s, confidence 1.0, no Tier 2 needed).

What is worth incorporating is a narrow set of *defense-in-depth* and *observability* improvements:

- **5 INCORPORATE** items, all narrow and additive (no architectural conversion required).
- **1 ADAPT** item that retrofits forensic's adversarial fallback chain to v2's per-component error matrix.
- **3 DEFER** items where forensic's idea is sound but v2 has no observed failure mode driving urgency.
- **14 REJECT** items where forensic's choice is workload-mismatched.
- **11 SHARED / NO ACTION** items where v2 already matches or is functionally equivalent.

The actionable list below is small *and that is the right answer*. The user asked for a real read, and the real read is: v2 is in good shape; forensic provides a handful of cheap wins around enforceability and asymmetric-cost flags; the rest is genuinely orthogonal.

**One-sentence verdict**: Forensic has 5-6 narrow, additive improvements worth shipping into v2; the architectural core of forensic is a different tool for a different workload and should remain so.

---

## 2. Per-Component Merits & Weaknesses

(Full analysis lives in `adversarial/merits-weaknesses.md`. Summary table here.)

| Component | Forensic strength | Forensic weakness | v2 strength | v2 weakness | Workload-fit verdict |
|---|---|---|---|---|---|
| Orchestrator role | Architectural hallucination resistance (Phase 6 cannot fabricate a `file:line` because it doesn't have the file) | Latency floor; rigid phase contracts | Single-turn diagnoses; lazy ref loading | Behavioral mitigation can fail (eval audit logs show inline-fallback fired 4/8 times) | Orthogonal — both correct for their harness |
| Tier/phase model | Data-flow gates; testable in isolation | Always runs all phases for the tier; no skip-on-consensus | Conditional escalation (Wave 2 gate, Wave 4 skip) | Less predictable cost | v2 better for triage |
| Agent inventory & lifecycle | Fresh context per subprocess; honest parallelism | File-IPC overhead; cannot stream partials | Two new agent files reusable by other skills | Some session-state carryover | Orthogonal |
| MCP usage & budgets | Per-server concurrency cap (≤3); per-phase routing table | Static budgets are targets, not enforced | `auggie`-first offload to free tier; tavily rate-cap | No per-server concurrency cap | INCORPORATE the cap subset |
| Failure handling & rollback | Coordinated 3-level adversarial fallback; selective git rollback | Rollback machinery wasted in diagnosis-first tool | 10-row per-component error matrix; eval-validated fallbacks | One-step adversarial fallback (could be a chain) | ADAPT the chain subset |
| Adversarial integration depth | Always-debate (Phase 2 + 3b); predictable cost | Pays adversarial cost on consensus | Skip-on-consensus; token thrift | Vulnerable to anchored consensus | v2 better; `confidence-calibrator` mitigates the blind spot |
| Hallucination contract | Withhold-access (architectural) | Validator-failure path nonexistent because there's no validator | Post-hoc validate + anchoring-mitigate (behavioral) | Validator can fail (and does, per eval evidence) | Orthogonal; both equivalent for their harness |
| Activation surface | Explicit + `--caller` | No keyword auto-activation | Aggressive keyword triggers; stack-trace recognition | False-positive risk | v2 better for interactive use |
| Output contract | `test_is_wrong` flag; YAML write-on-failure | TFEP-specific fields irrelevant to v2 | Audit log + structured dict | No `test_is_wrong` equivalent | INCORPORATE `test_is_wrong` |
| CLI / sprint-runner | `~450-line tfep.py` module; NDJSON detection | Workload-specific | Zero CLI integration | Cannot be called by sprint runners | Orthogonal |
| Test/eval strategy | 10 test files; 58 SC; schema-conformance; canned fixtures | Heavyweight for v2 scale | Eval-workspace cases as data | No automated pass/fail; format drift observed | INCORPORATE schema-conformance subset |

---

## 3. Classification Table — All 31 Differences

See `merged-output.md` for the canonical classification table. Summary:

| Verdict | Count | IDs |
|---|---|---|
| INCORPORATE | 5 | C-008 (subset), C-012, C-013 (subset), C-018 (subset), U-004 (subset) |
| ADAPT | 1 | C-014 |
| REJECT | 14 | C-001, C-003, C-004, C-005, C-006, C-007, C-009, C-010, C-011, C-015, C-017, U-001, U-002, U-003 |
| DEFER | 3 (debate-surfaced) | JSON Schema output contract, stale-codebase detection, named degradation modes |
| SHARED / NO ACTION | 11 | S-001, S-002, S-003, S-004, S-005, C-002, C-016, U-005, U-006, A-001, A-002 |

---

## 4. Incorporation Roadmap — Actionable Changes to v2

Order of operations is driven by frequency-weighted impact against observed eval failure modes. Items 1-3 ship first (driven by observed eval evidence); items 4-6 ship second (driven by latent-risk mitigation with strong analytic justification).

### 4.1 INCORPORATE #1 — `test_is_wrong` flag in return contract

- **WHICH v2 files change**:
  - `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — output contract table (lines 37-54), add row.
  - `src/superclaude/commands/troubleshoot.md` — return-surfacing example (lines 70-71), add the flag.
  - `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md` — add a "Test is wrong?" field in the Diagnosis section.
- **WHAT the change is**: Add `test_is_wrong: bool` field. Default `false`. Set `true` in Wave 5 synthesis when the chosen diagnosis is "the test expectation is outdated rather than the code is wrong" (detection: chosen fix modifies test assertions / expected values, not production code under test).
- **WHICH wave / agent**: Wave 5 synthesis (orchestrator-level), no agent change.
- **WHY it reliably improves effectiveness**: Asymmetric cost — missing this verdict means the user applies a code fix for what is actually a test-expectation update. Forensic's `forensic-spec.md:1953-1984` surfaces this as a top-level boolean for the same reason. The eval evidence hasn't yet shown this case, but the failure mode is well-understood and the mitigation is one bool.
- **COST**: ~30 min engineering; ~10 lines of skill changes; no token-cost change in the common case.
- **RISK**: Low. Additive field. Existing callers ignore unknown fields.
- **Eval verification**: Add to `iteration-4` (or next) eval an explicit "test-is-the-bug" case; assert `test_is_wrong: true` in the return dict.

### 4.2 INCORPORATE #2 — Wave 0 repeat-failure detection (24h scope)

- **WHICH v2 files change**:
  - `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — Wave 0 section (lines 71-105), add detection step.
  - `src/superclaude/commands/troubleshoot.md` — Examples section, add a "repeat invocation" example.
- **WHAT the change is**: In Wave 0, glob `<output-dir-root>/troubleshoot-*` for prior runs in the last 24h. Match against current `--scope` or first 100 chars of issue text. If found:
  - Emit chat notice: "Previously diagnosed [date]: see [REPORT path]. Confidence was [X]. Auto-elevating to `--depth deep`."
  - Force `--depth deep` (unless `--no-escalate` is set — `--no-escalate` wins per invariant INV-005).
  - Set `repeat_invocation_count` in audit-log header.
- **WHICH wave / agent**: Wave 0 (orchestrator-level).
- **WHY it reliably improves effectiveness**: Users re-running `/sc:troubleshoot` against the same symptom is a frequent pattern; current behavior creates a new slug+timestamp dir with no memory. Re-running is *signal* — usually the user didn't trust the prior pass. Forensic's `EscalationState` solves the analogous TFEP problem. The eval evidence doesn't yet show this case but it's high-frequency in expected use.
- **COST**: ~2 hours engineering; ~30 lines of skill changes; ~50 tokens added to Wave 0 prompt; Glob cost is trivial.
- **RISK**: Low-medium. Heuristic match may false-positive on different-but-similar symptoms (invariant INV-002, MEDIUM); the chat notice is informational and user can override.
- **Eval verification**: Add to next iteration a "re-invoke same scope" eval; assert chat notice fires and `--depth deep` is forced.

### 4.3 INCORPORATE #3 — Per-server MCP concurrency cap (≤3 simultaneous)

- **WHICH v2 files change**:
  - `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — Wave 3 MCP enrichment step (lines 176-179), add cap instruction.
- **WHAT the change is**: Add to Wave 3 MCP enrichment instruction: "Issue at most 3 simultaneous queries per MCP server. When 4 hypothesis agents are spawned, agents must serialise their MCP calls per-server within their brief (e.g., a hypothesis agent making 2 Serena queries is fine; 4 agents × 1 Serena query each is at the cap; 4 agents × 2 Serena queries simultaneously is not)."
- **WHICH wave / agent**: Wave 3 (orchestrator instruction; hypothesis agents inherit).
- **WHY it reliably improves effectiveness**: Forensic's NFR-010 (`forensic-spec.md:2127`) caps at ≤3 simultaneous per server. Without it, v2's Wave 3 fan-out can hit 4 agents × 3 Serena queries = 12 simultaneous calls — first incident will be a partial-grounded Tier 2 with no obvious remediation.
- **COST**: Negligible. Prompt update only.
- **RISK**: Low. Slightly slower in pathological cases; prevents rate-limit incidents.
- **Eval verification**: Add a synthetic "4-hypothesis-agent test" eval; assert no more than 3 simultaneous MCP calls per server appear in audit log (requires audit log to record MCP call ordering — see #4 below).

### 4.4 INCORPORATE #4 — Audit-log header/footer schema

- **WHICH v2 files change**:
  - **NEW**: `src/superclaude/skills/sc-troubleshoot-protocol/refs/audit-log-schema.md` — schema spec.
  - `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — Wave 5 final step (line 254-267), add normalisation step.
- **WHAT the change is**: Define `audit-log-schema.md` specifying:
  - ISO-8601 timestamps with `Z` suffix throughout.
  - MCP availability as comma-separated lowercase tokens: `auggie,serena,context7,tavily,sequential` or `none`.
  - Absolute paths for `output_dir`.
  - Required fields in `SC:TROUBLESHOOT:TARGET` block (issue, type, depth, scope, fix_authorized, no_escalate, mcps_available, output_dir).
  - Required fields in `SC:TROUBLESHOOT:SUMMARY` block (status, tier_reached, confidence, escalation_reason, hypothesis_count, adversarial_invoked, fix_authorized, duration_sec, **and new** `test_is_wrong`, `repeat_invocation_count`, `degraded_mode`).
  - Optional structured `mcp_calls` section recording per-server query count.
  - Add a Wave 5 step: validate final audit log against schema; on mismatch, prepend `# NORMALIZED <reason>` line and rewrite to conform.
- **WHICH wave / agent**: All waves write to audit; Wave 5 normalizes.
- **WHY it reliably improves effectiveness**: Observed eval failure mode — 4 of 8 eval audit logs show timestamp-format variation, MCP-availability string variation, output-dir absolute-vs-relative drift. A downstream "troubleshoot history" command, or any caller introspecting the audit log, will break on this drift. Forensic's schema-conformance philosophy applied narrowly here is high-leverage.
- **COST**: ~3 hours engineering; ~80 lines schema doc + ~40 lines validation logic in skill.
- **RISK**: Low. The schema codifies what is already mostly-the-case; the normalisation step is corrective rather than destructive.
- **Eval verification**: Re-run 4 prior eval cases with normalisation step; verify schema-compliant outputs.

### 4.5 INCORPORATE #5 — Schema-conformance tests for hypothesis-card + REPORT.md templates

- **WHICH v2 files change**:
  - **NEW**: `tests/skills/sc-troubleshoot-protocol/test_template_schemas.py` — pytest module.
  - `Makefile` — ensure new tests are picked up by `make test`.
- **WHAT the change is**: Three pytest cases:
  - **Hypothesis card schema**: asserts every hypothesis card in `.dev/eval-workspaces/sc-troubleshoot/**/tier*-hypothesis.md` (or `tier2-<agent>-hypothesis.md`) has all required headings: Claim / Evidence / Proposed Fix / Confidence / Risks / "If I'm wrong it's probably because…".
  - **REPORT.md schema**: asserts every `REPORT.md` in eval-workspaces has all required sections per `refs/report-template.md`.
  - **Audit-log schema**: asserts every `audit.log` matches the schema from #4 (header + footer well-formed, required fields present, ISO-8601 timestamps).
- **WHICH wave / agent**: Out-of-band (test infrastructure); applies to Wave 1, 3, 5 outputs.
- **WHY it reliably improves effectiveness**: Templates today are documentation, not enforcement. Schema-conformance tests catch silent regressions when an agent emits a card missing a required field. Forensic learned this lesson (`test-strategy-2.md:299-311` schema tests are gated at M6); v2 can adopt the lightweight subset.
- **COST**: ~1 day engineering; ~150 lines of pytest; adds ~30 seconds to `make test`.
- **RISK**: Low. One test file; doesn't touch runtime behavior.
- **Eval verification**: Tests themselves are the verification.

### 4.6 ADAPT #1 — Single-agent scoring fallback before "pick highest-confidence" (adversarial failure chain)

- **WHICH v2 files change**:
  - `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — Error Handling table (line 344), modify the `sc:adversarial-protocol fails in Wave 4` row.
- **WHAT the change is**: Today the fallback for `sc:adversarial-protocol` failure is one step: "Pick the highest-confidence Tier 2 fix proposal; note in audit and report header." Insert an intermediate step:
  1. **Level 1 retry**: Re-invoke `sc:adversarial-protocol` with `--depth quick` (cheaper, faster).
  2. **Level 2 single-agent scoring**: If Level 1 also fails, spawn a single `quality-engineer` agent via Task with: hypothesis cards + competing-fix files + escalation rubric. Token cap 1000, timeout 60s. Agent emits a one-line verdict + confidence per fix.
  3. **Level 3 current fallback**: If Level 2 also fails, fall back to "pick highest-confidence." Mark `debate_status: "skipped"` in audit + report header.
- **WHICH wave / agent**: Wave 4 error handling.
- **WHY it reliably improves effectiveness**: Forensic's 3-level chain (`forensic-spec.md:1786-1799` and proposal-verdicts.md:268-290) is well-justified. Single-agent scoring is much higher signal than naive highest-confidence selection. Adversarial failures are rare in eval evidence but the fallback path is currently shallow.
- **COST**: ~2 hours engineering; ~10 lines of skill changes + ~20 lines of fallback Task prompt; ~1000 tokens per fallback invocation (only when Level 1 fails).
- **RISK**: Low. Additive intermediate step in an already-rare failure path.
- **Eval verification**: Add a "force-adversarial-fail" eval case (mock failure); assert single-agent scoring fires and produces a verdict before final fallback.

---

## 5. Implementation Gotchas (from Round 2.5 invariant probe)

5 MEDIUM-severity items must be addressed in the change specs above. None block convergence but each is an implementation risk.

| INV ID | Category | Gotcha | Mitigation |
|---|---|---|---|
| INV-001 | guard_conditions | `test_is_wrong` may false-fire on deliberate test-expectation updates (e.g., legitimately changing an expected value to match a new API). | Detection rule must require explicit signal: "test expectation is outdated *and* code is correct". When the diagnosis is "API changed; both code and test need update", `test_is_wrong: false`. |
| INV-002 | state_variables | Repeat-failure detection may false-positive on different-but-similar symptoms. | Chat notice + user-overridable; do not silently force `--depth deep`. Surface the prior REPORT path so the user can verify the match. |
| INV-003 | count_divergence | MCP cap ≤3 ambiguity: per-server-simultaneous vs per-invocation. | Specify "≤3 simultaneous in-flight per MCP server" (matching forensic NFR-010 wording). |
| INV-004 | collection_boundaries | 24h TTL for repeat-detection is arbitrary. | Document as configurable in a follow-up; default 24h is fine for v1. |
| INV-005 | interaction_effects | `--no-escalate` × repeat-failure × `--depth deep` priority. | `--no-escalate` wins. Repeat-detection emits notice but does NOT force depth elevation when `--no-escalate` is set. |

---

## 6. Explicit Rejects — with Rationale

The 14 REJECT items are *not* sandbagging. Each is rejected because importing forensic's choice would either (a) destroy a v2 path the eval evidence shows working, (b) solve a problem v2's workload doesn't have, or (c) duplicate a mitigation v2 already has.

| REJECT | Why forensic's approach would harm v2 |
|---|---|
| C-001 (project-wide scope) | v2's STOP-on-no-symptom rule is correct for triage. Eval `eval-wave0-stop-vague-input` shows it works; project-wide-sweep would generate noise for a user with a specific symptom. |
| C-003 (8 always-on phases) | Would destroy Tier-1-stop-on-high-confidence (eval-3 missing-import: 60s, confidence 1.0). Phase 0 recon + Phase 2 debate add ~30-60k tokens per invocation for cases that don't need them. |
| C-004 (subprocess pipeline) | v2's in-session Task model fits the interactive harness. Subprocess pipeline requires `claude --print` orchestration that v2's audience doesn't have. |
| C-005 (orchestrator-as-dispatcher) | v2's reader model paired with `evidence-validator` post-hoc gives equivalent hallucination resistance. Conversion cost (refactor all waves, redesign agents) buys protection against a failure mode that hasn't been observed in 8 evals. |
| C-006 (subprocess agents) | v2's two new agent files (`evidence-validator`, `confidence-calibrator`) are independently addressable by other skills — better reusability than subprocess agents. |
| C-007 (Haiku/Sonnet/Opus matrix) | v2's per-agent default + `--models` override is simpler. Forensic's matrix requires Opus-orchestrator pin, which is overkill for an interactive command. |
| C-009 (always-debate) | Skip-on-consensus is the right cost optimization. Eval-3 missing-import would waste 30-60k tokens under always-debate for zero new information. |
| C-010 (`--tier × --depth` two-axis) | v2's conditional escalation gates give equivalent cost control. Adding `--tier` is a cognitive-overhead knob that controls something the rubric already controls. |
| C-011 (per-phase token caps) | v2's per-tier band is the right granularity. Per-phase hard caps add enforcement complexity for no observed overrun. |
| C-015 (sprint-runner integration) | v2 has no sprint-runner audience. Building `sprint/tfep.py` for v2 would be ~450 lines solving a problem v2's workload doesn't have. |
| C-017 (auto-re-launch remediation) | v2's diagnosis-first + user-initiated `/task` is correct for an interactive symptom-triage tool. Auto-re-launch is sprint-pipeline-specific. |
| U-001 (`--tier` flag) | See C-010. |
| U-002 (`sprint/tfep.py`) | See C-015. |
| U-003 (orchestrator-as-dispatcher) | See C-005. |

---

## 7. Open Questions / Defer-Until

3 items from the debate are deferred. Each has merit but no observed failure mode driving urgency. Each has an explicit defer-until criterion.

| DEFER | What forensic offers | Defer-until criterion |
|---|---|---|
| JSON Schema for output contract | Machine-validatable contract; caller-side regression detection. | Defer until a caller-side parse-break is observed OR until v2 has 3+ external skill consumers. The Markdown table in `SKILL.md:37-54` is adequate for v1. |
| Stale-codebase detection | `git rev-parse HEAD` comparison on resume. | Defer until v2 has a resume primitive. v2 today creates a new slug+timestamp dir per invocation; nothing to make stale. If repeat-detection (INCORPORATE #2) is later extended to "carry forward prior hypothesis cards," stale-codebase becomes relevant. |
| Named degradation modes (`degraded_mode` audit field) | Coordinated 4-level degradation (Full → Reduced precision → Reduced depth → Minimal). | Defer until eval evidence shows a multi-MCP failure case where the cumulative degradation is unclear from the per-component audit entries. Today's per-component error matrix is adequate. |

---

## 8. Roadmap — Order of Operations

Sequence the 5 INCORPORATE + 1 ADAPT in two waves. Wave A is driven by observed eval failure modes (ships first). Wave B is latent-risk mitigation (ships second). All items are independent — no inter-dependency forces ordering beyond cost-vs-value priority.

### Wave A (eval-evidence-driven; ship first)

1. **INCORPORATE #4 — Audit-log schema** (3h, low risk). Highest-observed format variation; downstream consumers most fragile.
2. **INCORPORATE #1 — `test_is_wrong` flag** (30min, low risk). Highest leverage per minute spent.
3. **INCORPORATE #5 — Schema-conformance tests** (1 day, low risk). Codifies enforcement for #4 and existing templates.

### Wave B (latent-risk mitigation; ship second)

4. **INCORPORATE #3 — MCP per-server concurrency cap** (15min, negligible risk). Cheap; latent-but-real risk.
5. **INCORPORATE #2 — Wave 0 repeat-failure detection** (2h, low-medium risk). High user-experience leverage; needs invariant gotchas addressed.
6. **ADAPT #1 — Single-agent adversarial fallback** (2h, low risk). Improves an already-rare failure path.

### Total cost estimate

- Engineering effort: ~2-3 days end-to-end including eval-case authoring.
- Token cost impact in steady state: negligible (audit-log schema adds ~50 tokens to Wave 5; MCP cap is prompt-level; `test_is_wrong` detection is one extra synthesis check).
- Risk: low; all items are additive and individually testable.

### Recommended eval coverage

Each item should land with:
- One new positive eval case (item fires as intended).
- One new negative eval case where applicable (item correctly does NOT fire).
- For #4 and #5: re-run existing 8 eval cases against new schemas to verify no regression.

---

## 9. Final Verdict

**Are forensic and v2 genuinely orthogonal designs?** Mostly yes. They share an adjudication primitive (adversarial debate) and a terminal artifact shape (Markdown report), and one core failure mode (citation fabrication), which they mitigate via architecturally-opposite mechanisms (withhold-access vs post-hoc-validate). Beyond that shared core, they target different workloads, fit different harnesses, and ship different value.

**Should v2 be refactored to look more like forensic?** No. The architectural conversion cost (subprocess pipeline, orchestrator-as-dispatcher, 8-phase always-on, sprint-runner module) would harm v2's strengths (Tier 1 thrift, in-session Task parallelism, aggressive auto-activation) without observed failure modes to justify the cost.

**Are there forensic ideas worth absorbing?** Yes — 5 narrow INCORPORATEs + 1 ADAPT. They are the cheap-but-real wins: a high-signal asymmetric-cost flag (`test_is_wrong`), enforceability schemas (audit-log, hypothesis-card, REPORT.md), a latent-risk cap (MCP per-server), an ergonomic improvement (repeat-failure detection), and a fallback chain extension (single-agent adversarial scoring).

**One-sentence final verdict**: Forensic offers v2 a handful of cheap defensive wins around enforceability and observability; the architectural core of forensic is a different tool for a different workload and should remain so — incorporate the narrow subset above and leave the rest alone.

---

## Appendix A — Provenance

This report is the product of:

1. `/sc:analyze` 4-way fan-out on forensic backlog (713-line breakdown synthesised from 12k lines / 29 files).
2. `/sc:adversarial` Run 1 — differences-only debate (3 advocates, `--depth standard`, Round 2.5 sufficiency probe): 31 substantive differences catalogued.
3. `/sc:adversarial` Run 2 — incorporation debate (this run): 3 advocates (architect / quality-engineer / analyzer), `--depth standard`, Round 2.5 sufficiency probe. Convergence 100% unanimous after Round 2. Base selected: QE (combined score 0.919). Architect's workload-mismatch framing and Analyzer's eval-evidence-driven prioritisation merged in.

Artifacts in `adversarial/`:
- `merits-weaknesses.md` — per-component analysis.
- `variant-1-architect.md` / `variant-2-quality-engineer.md` / `variant-3-analyzer.md` — 3 advocate cards.
- `debate-transcript.md` — full debate with scoring matrix and invariant probe.
- `base-selection.md` — hybrid scoring; QE selected.
- `merge-log.md` — 11/11 changes applied.

Top-level `merged-output.md` — classifications for all 31 differences with verdicts and rationale.

This `incorporation-report.md` — comprehensive recommendation deliverable.
