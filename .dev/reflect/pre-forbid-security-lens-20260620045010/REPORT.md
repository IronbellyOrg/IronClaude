# Reflect REPORT — UC-1 (pre-execution, coverage-only)

- **Mode**: pre (UC-1) · resolved via §3.2 rule 5 (`--spec` only, no tasklist → coverage-only pass)
- **Spec audited**: `.dev/brainstorms/20260620T044238-forbid-security-lens-default/merged-requirements.md`
- **Tier reached**: 1 (single domain = markdown/docs edits, narrow blast radius; no escalation triggers)
- **Calibrated confidence (findings)**: 0.92 — every finding re-grounded by fresh grep + `git ls-files` this turn
- **Coverage verdict**: **0.80 → BELOW 0.90 floor.** 2 gaps block a clean pass; both are amendable in-place.
- **Evidence-validator**: all 24 cited `file:line` references in the spec re-verified accurate (0 dropped). 5 SPEC.md "hostile"/eval-grader hits correctly **excluded** from scope (no over-reach).

---

## Coverage Matrix (behavior-surface → edit)

| # | Required surface | Spec edit | Status |
|---|------------------|-----------|--------|
| R1 | Per-domain persona matrices (code/arch/incident/product/research) | EDIT-1a | ✅ mapped |
| R2 | Enterprise override (ref L19 + SKILL L212 + SPEC L217) | EDIT-1b/2a/4 | ✅ mapped |
| R3 | `security` instruction-template row (keep for explicit path) | EDIT-1d | ✅ mapped |
| R4 | Worked examples + round-trip vectors (ref L46-48/94/142-143; SKILL L243; SPEC L242) | EDIT-1e/1f/1g/2c/4 | ✅ mapped |
| R5 | Socratic security probe Q14 (socratic L59) | EDIT-3 | ✅ mapped |
| R6 | Runtime guard / `auto_excluded_personas` set | EDIT-1c/2b | ✅ mapped |
| R7 | Explicit-path preservation (`--personas security` still works) | constraints + EDIT-1d | ✅ mapped |
| R8 | Command + user-guide prose (command L81/89; docs L105/113) | EDIT-5 | ✅ mapped |
| **R9** | **`plugins/superclaude/commands/brainstorm.md` — tracked command mirror** | **— none —** | ❌ **GAP** |
| **R10** | **Compliance-adjacent Socratic probes scoping (incident Q17, process Q17)** | **— undeclared —** | ⚠️ **SCOPE GAP** |

**coverage_pct = 8/10 = 0.80** (parsed-surface basis). R10 is arguably out-of-scope (raising the effective ceiling to ~8.5/9.5 ≈ 0.89), but neither gap is *declared* in the spec, so the floor is not met.

---

## Gap Registry

### G1 — `plugins/superclaude/commands/brainstorm.md` is an unaddressed, tracked, security-bearing surface (MEDIUM-HIGH)

**Evidence (this turn):**
- `git ls-files --error-unmatch` → **TRACKED**; `git check-ignore` → **not ignored**.
- `make build-plugin` writes to `dist/plugins/superclaude` (Makefile L65), **not** repo-root `plugins/` → repo-root `plugins/` is a hand-maintained tracked mirror, not regenerated build output.
- It is a **divergent, older v1-style file** with 4 *additional* security references the src/ v2 file lacks:
  - frontmatter `personas: [architect, analyzer, frontend, backend, security, devops, project-manager]` (L7)
  - L39 "Multi-persona orchestration across architecture, analysis, frontend, backend, **security** domains"
  - L82 "Parallel exploration paths with frontend, backend, and **security** personas"
  - L90 "Comprehensive validation with **security**, devops, and architect personas"

**Impact:** Leaving it untouched means the tracked/distributable plugin surface still advertises and seeds the security lens — directly contradicting the goal. The spec's "4 source files" enumeration is incomplete.

**Recommendation:** Either (a) add it as **EDIT-7** (strip `security` from frontmatter + L39/L82/L90 prose), OR (b) consciously declare it out-of-scope with a reason (e.g., "plugins/ is slated for regeneration from src/; tracked copy is stale"). Do not leave it silently unaddressed. **Provenance is unverified** — confirm whether `plugins/` is regenerated from `src/` before choosing (a) vs (b); reflect could not find a Makefile target that writes repo-root `plugins/`.

### G2 (R10) — Compliance/policy-framed Socratic probes are neither included nor excluded (MEDIUM)

**Evidence:** `socratic-templates.md` L91 (incident Q17 "What policy / SLO / **compliance** angle does this touch?") and L178 (process Q17 "What's the **audit / compliance** angle?").

**Impact:** These are an *adjacent* governance/compliance lens, distinct from the security/threat-model lens the user named. The spec addressed only the code/deep security-reviewer Q14 and is silent on these. A strict reading of "security lens" might pull them in; a literal reading (user explicitly discussed only the "security reviewer" frame) leaves them out.

**Recommendation:** Add a one-line **explicit scope ruling** to the spec — recommended: **out-of-scope** (compliance/policy ≠ security threat lens; removing them would over-reach beyond the user's stated intent). Surface, don't silently decide.

### G3 — "17 sites" count is inaccurate (LOW)

The spec's summary says "17 sites"; the actual security-bearing line count across the 4 SoT files + 2 docs is ~24 (and 25 with the plugins mirror). The edit set is enumerated by section so behavior is unaffected, but the number is wrong. **Recommendation:** drop the count or correct to "~24 lines across 5 tracked files (+2 docs)."

### G4 — Indirect enterprise auto-trigger path not explained (LOW)

`socratic-templates.md` L30 auto-classifies `--strategy enterprise` on topic keywords (compliance, SOC2, SOX, HIPAA, …). So a compliance-themed topic indirectly routes to the enterprise persona list. EDIT-1b/2a (drop security from enterprise list) + the EDIT-1c guard **do** close this vector, but the spec never names it. **Recommendation:** add a sentence noting the indirect path is closed by the enterprise-list edit + guard, so a reviewer sees it's covered.

---

## What the spec got RIGHT (independently confirmed)

- **All 24 cited line numbers are accurate** (re-Read this turn) — no citation drift.
- **Keeping the `security` instruction-template row (EDIT-1d) is correct** — required for the `--personas security` explicit path; deleting it would break R7.
- **The guard's explicit-vs-auto distinction is sound** — `auto_excluded_personas` filtered unless `p ∈ explicit --personas` correctly preserves "unless specifically instructed."
- **No over-reach into the eval grader** — SPEC.md L523/L552/L603/L642/L708 "hostile reviewer" / "hostile-reviewer objections" are the *grader's* adversarial stance, unrelated to the security persona; the spec correctly left them alone. A naive `grep hostile` replace would have wrongly hit these.
- **No hidden enrichment vector** — Wave 2A enrichment uses `/sc:analyze --focus quality`, not `--focus security`.

---

## Verdict

**AMEND-THEN-PROCEED.** The mechanism design (guard + reusable exclusion set + de-defaulting + dialogue-lens removal) is correct and the 4-file edit set is accurate. But coverage is **0.80 < 0.90** because of **G1 (untracked-in-spec `plugins/` mirror with 4 live security refs)** and **G2 (undeclared compliance-probe scope)**. Resolve G1 (edit-or-exclude with provenance check) and G2 (explicit scope ruling), fold in G3/G4, and the spec reaches ≥0.95 coverage and is safe to hand to task-builder / implementation.

**Stable contract:**
```yaml
contract_version: "1.0"
mode: pre
status: success
tier_reached: 1
coverage_pct: 0.80
coverage_floor: 0.90
coverage_met: false
calibrated_confidence: 0.92
citations_dropped: 0
missing_requirements: ["plugins/ command mirror (G1)", "compliance-probe scope ruling (G2)"]
recommended_additions: ["EDIT-7 plugins mirror or explicit exclusion", "scope ruling on compliance Q17s", "correct site count (G3)", "note indirect enterprise trigger closed (G4)"]
over_reach_avoided: ["SPEC.md hostile-reviewer eval-grader lines"]
verdict: amend-then-proceed
```
