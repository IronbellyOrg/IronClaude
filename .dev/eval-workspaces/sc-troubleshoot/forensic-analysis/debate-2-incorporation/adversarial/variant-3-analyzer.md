# Variant 3 — Analyzer Advocate: Incorporation Recommendations

**Voice**: opus:analyzer — partial to frequency-weighted pragmatism, skeptical of solutions to unlikely scenarios, prioritises day-1 implementation impact, discounts theoretical concerns.

## Position summary

The user's question is "what improves v2 *reliably*". The analyzer answers by frequency-weighting failure modes against the eval evidence. v2 has 8 eval cases; the failure modes that *actually appeared* are:
1. `evidence-validator` / `confidence-calibrator` ran "simulated inline" in dispatch evals — observed 4/8 times.
2. Free-form audit log header/footer variation across runs (different timestamp formats, different MCP-availability strings) — observed 4/8 times.
3. Inline simulation when fixture files don't exist — observed 2/8 times.
4. No prior-pass awareness — not yet observed but obvious.

The failure modes that *did not appear* in the eval evidence:
- Citation fabrication (eval validators caught none, suggesting either v2 is well-grounded or the inline fallback was lenient — the analyzer treats this as inconclusive, not as proof of safety).
- Sprint-runner integration gaps — v2 has no sprint audience, so this is workload-mismatched.
- Resume / checkpoint failures — v2 has no resume primitive, but the eval workload is short-running, so this hasn't bitten yet.

The analyzer recommends 4 narrow INCORPORATEs and 1 ADAPT, all driven by observed failure modes. The rest of forensic is rejected as solutions to problems v2 doesn't have.

## Steelman of forensic's design

Forensic's design quality is high — 22-proposal spec amendment process, 25-criterion adversarial rubric, 58 success criteria, 10 test files, behavioral-contract testing philosophy. The discipline is admirable. The two-axis mode (`--tier × --depth`) is genuinely more flexible than v2's single axis. The architectural hallucination contract is genuinely stronger than v2's behavioral one. The sprint-runner integration solves a real problem for *its* workload.

## Steelman of v2's design

v2 ships. The eval evidence shows it works on real cases (security IDOR, performance regression, flaky test, missing import). The Tier-1-stop-on-high-confidence path is the right common-case optimisation. The two-agent hallucination contract is the right shape for an in-session command. The lazy ref-loading is operationally sensible.

## Concrete recommendations driven by eval evidence

### INCORPORATE (4 items — driven by observed failure modes)

1. **Audit-log header/footer normalization** (eval evidence-driven; partial-adopt forensic's schema rigor from C-013)
   - WHY: The eval audit logs show 4 different timestamp formats, 3 different MCP-availability strings, 2 different output-dir absolute-vs-relative conventions. A downstream consumer (e.g. a "troubleshoot history" command) cannot parse these reliably. Forensic's schema-conformance philosophy applied narrowly here is high-value.
   - CHANGE: Define `refs/audit-log-schema.md` specifying:
     - ISO-8601 timestamps with `Z` suffix
     - MCP availability as comma-separated lowercase tokens (`auggie,serena,context7,tavily,sequential` or `none`)
     - Absolute paths only
     - Required fields per header / footer block
   - Add a Wave 5 step: validate the final audit log against the schema; on mismatch, prepend a `# NORMALIZED` line and rewrite to conform.
   - WHICH WAVE: All waves write; Wave 5 normalizes.
   - COST: Light. ~50 lines of schema + ~30 lines validation logic.

2. **`test_is_wrong` flag in return contract** (high-leverage / low-cost; from C-012)
   - WHY: The "the test is the bug, not the code" verdict is asymmetrically costly to miss. Forensic surfaces it as a top-level boolean. v2 today buries it in prose. The eval evidence doesn't show this case yet, but it's the kind of finding where missing it means the user applies the wrong fix — exactly the failure mode the tool exists to prevent.
   - CHANGE: Add `test_is_wrong: bool` to output contract (`SKILL.md:37-54`). Add detection rule in Wave 5 synthesis.
   - WHICH WAVE: Wave 5.
   - COST: Trivial. Additive.

3. **Per-server MCP concurrency cap (≤3)** (forensic NFR-010 / C-008)
   - WHY: Tier 2 with 4 hypothesis agents × MCP queries can saturate Serena/auggie. The eval workload was light enough not to hit this, but it's a latent risk. Cheap to mitigate.
   - CHANGE: One-sentence addition to Wave 3 MCP enrichment (`SKILL.md:176-179`).
   - WHICH WAVE: Wave 3.
   - COST: Negligible.

4. **Repeat-failure / prior-pass detection in Wave 0** (adapted from forensic U-004)
   - WHY: Users re-running `/sc:troubleshoot` against the same symptom is a frequent enough pattern to merit detection. The current behavior (fresh slug+timestamp dir, no memory) loses learning across runs. Forensic's escalation gradient solves an analogous problem (TFEP repeat-trigger counts).
   - CHANGE: Wave 0 scans prior audit logs in the last 24h for scope or issue-prefix match. If found, emit chat notice and force `--depth deep`.
   - WHICH WAVE: Wave 0.
   - COST: Light. Glob + parse + emit.

### ADAPT (1 item)

5. **Coordinated adversarial fallback** (forensic 3-level chain → v2 2-level chain; from C-014)
   - WHY: Adversarial failure isn't yet observed in v2 evals, but forensic's mitigation is a small, well-defined chain. Adopting the *intermediate level* (single scoring-agent retry) without the rest is the high-leverage subset.
   - CHANGE: Modify `SKILL.md:344` error row for `sc:adversarial-protocol` failure to include intermediate single-agent scoring retry before falling back to "pick highest-confidence."
   - WHICH WAVE: Wave 4 error handling.
   - COST: One additional row + ~3 sentences of behavior.

### REJECT (everything else — frequency-weighted)

The analyzer's reject list is the broadest of the three voices:

- **Orchestrator-as-dispatcher** (U-003): the failure mode (citation fabrication) hasn't bitten in 8 evals. v2's behavioral mitigation appears to work. The cost of architectural conversion (refactor every wave, redesign agents, rebuild evals) is enormous relative to the unmeasured benefit.
- **8-phase pipeline** (C-003): would slow the Tier-1-only path (currently ~60s for missing-import) by adding always-on phases. Cost destruction.
- **Subprocess pipeline** (C-004): v2 has no sprint audience. No driver.
- **Sprint-runner integration** (U-002 / C-015): no audience. Pure overhead.
- **Always-debate** (C-009): the eval evidence shows Wave 4 skip-on-consensus correctly suppresses adversarial for high-confidence single-hypothesis cases. Forcing always-debate would add ~30-60k tokens per invocation for no observed benefit.
- **`--tier × --depth` two-axis** (C-010, U-001): the conditional escalation gates already give v2 the cost control forensic's `--tier` provides. The orthogonal `--depth quick|standard|deep` is already there. Adding `--tier` on top is redundant.
- **Heavyweight test infrastructure** (most of C-013): the 58 SC + 10 test files + canned-artifact fixtures per phase boundary is right for forensic's scale (8 phases, multiple schemas) and wrong for v2's scale (3 tiers, 7 waves, 5 refs). Adopt the schema-conformance narrowly (see #1 above) and reject the rest.
- **Token-budget table per phase** (C-011): v2's per-tier band already exists in `SKILL.md:354-359`. Adding per-wave hard caps adds enforcement complexity for no observed overrun.
- **Selective git rollback** (forensic FR-TFEP-10): v2 doesn't apply code, ever. No rollback target.
- **Worktree isolation** (forensic NFR-008): v2 doesn't write code, ever. No isolation need.
- **Stale-codebase detection** on resume (forensic FR-053): v2 has no resume primitive; the QE's adaptation (#7 in their variant) is a stretch. The analyzer would defer this until a resume primitive exists.

## Analyzer verdict

v2 is the right shape for symptom-driven debugging. Forensic's design is the right shape for project-wide investigation and sprint-runner integration. The two designs are *mostly orthogonal*. Of the 31 substantive differences, 4 INCORPORATE + 1 ADAPT is the honest read; the rest are workload-mismatched.

Total cost estimate: ~2-3 engineering days. Total benefit: defense-in-depth against observed eval failure modes (audit-log format drift, prior-pass blindness), addition of a high-signal flag (`test_is_wrong`), and one latency-risk mitigation (MCP concurrency cap).

The analyzer's REJECT list is the longest of the three voices because the analyzer is most willing to say "this solves a problem we don't have." That's the honest answer when the question is "what reliably improves v2."

Final confidence: 0.93 on the 4 INCORPORATEs (each has either eval-observed motivation or clear cost/leverage asymmetry), 0.82 on the 1 ADAPT (forensic's mitigation is real but v2 hasn't yet exercised the failure mode), 0.95 on the broad REJECT list (the workload mismatch is structural and demonstrated).
