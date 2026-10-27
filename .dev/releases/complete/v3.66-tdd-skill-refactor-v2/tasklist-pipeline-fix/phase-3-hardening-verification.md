# Phase 3 -- Hardening + End-to-End Verification

Fix the latent dict-vs-list crash in DeviationRegistry and run the full pipeline end-to-end to verify all fixes work together.

---

### T03.01 -- Normalize findings dict-vs-list in DeviationRegistry.load_or_create

| Field | Value |
|---|---|
| Why | `DeviationRegistry.load_or_create()` (convergence.py:111) does `findings.items()` assuming dict. If `findings` is a list (legacy format or corruption), this crashes with `AttributeError: 'list' object has no attribute 'items'`. The fix in `executor.py` handles this for deviation-analysis, but the convergence path (spec-fidelity convergence loop) doesn't. |
| Effort | S |
| Risk | Low |
| Risk Drivers | backward-compat |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Verification Method | Unit test |
| MCP Requirements | None |
| Fallback Allowed | No |
| Sub-Agent Delegation | No |

**File:** `src/superclaude/cli/roadmap/convergence.py`
**Lines:** ~111-113 (after `findings = data.get("findings", {})`)

**Deliverables:**
1. List-to-dict normalization in `load_or_create`

**Steps:**
1. **[PLANNING]** Read `DeviationRegistry.load_or_create` (convergence.py:100-129) to confirm the dict assumption
2. **[EXECUTION]** Add normalization after `findings = data.get("findings", {})` at line ~111:
   ```python
   if isinstance(findings, list):
       findings = {
           f.get("stable_id", str(i)): f
           for i, f in enumerate(findings)
       }
   ```
3. **[VERIFICATION]** Run `uv run pytest tests/roadmap/ -v --tb=short` to verify no regression

**Acceptance Criteria:**
- `load_or_create` handles both dict and list `findings` without crash
- Dict format is preserved as-is (no unnecessary conversion)
- List format is converted to dict keyed by `stable_id` (or index fallback)

**Dependencies:** None (independent fix)
**Rollback:** Remove normalization; only affects legacy/corrupted registries

---

### T03.02 -- End-to-end pipeline verification

| Field | Value |
|---|---|
| Why | All fixes from Phases 1-3 must work together. The pipeline has never completed through deviation-analysis, remediate, and certify. This task verifies the full pipeline completes end-to-end with `--resume`. |
| Effort | L |
| Risk | High |
| Risk Drivers | end-to-end, external dependencies (ClaudeProcess LLM calls if convergence re-triggers) |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Verification Method | Pipeline run + artifact inspection |
| MCP Requirements | None |
| Fallback Allowed | Yes — if pipeline fails at a new step, diagnose and fix inline |
| Sub-Agent Delegation | No |

**Steps:**
1. **[PLANNING]** Run `uv run pytest tests/ --tb=short -q` one final time to confirm all fixes are clean
2. **[EXECUTION]** Run pipeline: `superclaude roadmap run /config/workspace/IronClaude/.dev/releases/current/v3.66-tdd-skill-refactor-v2/tdd-command-layer-spec.md --resume`
3. **[VERIFICATION]** Check `.roadmap-state.json` — all steps should have `status: "PASS"`
4. **[VERIFICATION]** Check `spec-deviations.md`:
   - `slip_count` > 0 (should be 14)
   - `routing_fix_roadmap` contains DEV-N IDs
   - `analysis_complete: true`
5. **[VERIFICATION]** Check `remediation-tasklist.md`:
   - Has YAML frontmatter with `total_findings`, `actionable`, `skipped`
   - Lists findings with DEV-N IDs under severity headings
6. **[VERIFICATION]** Check `certification-report.md`:
   - `certified: true`
   - `remediation_mode: tasklist-only`
   - `certification_scope: analysis-only`
   - Per-finding results table present
7. **[COMPLETION]** If any step fails, diagnose root cause and apply targeted fix before re-running

**Acceptance Criteria:**
- Pipeline completes through all steps including certify without crash or HALT
- All output files exist with valid frontmatter
- `.roadmap-state.json` records certify step with `status: "PASS"`

**Dependencies:** T01.03, T02.03, T03.01
**Rollback:** N/A (verification-only; fixes are individual rollback targets)
