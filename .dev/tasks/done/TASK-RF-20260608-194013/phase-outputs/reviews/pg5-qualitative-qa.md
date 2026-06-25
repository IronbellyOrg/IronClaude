# QA Report — task-qualitative (PG-5 spec-intent assessment)

**Topic:** task-builder `--reflect <none|0|1|2|auto>` 3-mode POST reflect gate dial
**Date:** 2026-06-09
**Phase:** task-qualitative (operational / spec-intent assessment of an EXECUTED deliverable)
**Fix cycle:** N/A (initial qualitative pass)
**fix_authorization:** true (src/superclaude/... only; never .claude/)
**Deliverable state:** UNCOMMITTED working-tree edits on top of HEAD `ab2dae1a`

**Files under review:**

- `src/superclaude/skills/task-builder/SKILL.md` (A.9 producer, §6 templates, frontmatter, Rule 19, Rule 20, validation bullet, depth reconciliation)
- `src/superclaude/agents/rf-qa.md` (TB-Add-9: V1–V16 + per-mode active map + MODE-MATCH)
- Spec: `.dev/brainstorms/20260608-191030-reflect-flag-post-gate/merged-requirements.md`

---

## Overall Verdict: FAIL

One CRITICAL defect (J7 / AX-3): the F3 executor-disjointness persistence machinery (Critical
Rule 20 + the `start_commit` capture comment) was left keyed to the **retired** legacy field
`POST_REFLECT_GATE: ENABLED`, which the refactor removed from the live BUILD_REQUEST schema.
For every new (default Mode-2) build the trigger is now dead, so `start_commit` /
`executor_model_class` are not persisted — silently re-opening the exact audit-F3 weakening the
rule exists to prevent, and undercutting the thesis's "clean subsumption" claim. Plus 2 MINOR
clarity items. The seven thesis judgments are otherwise delivered.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| J1 | Single producer is genuine (m computed once at A.9) | PASS | SKILL.md:1056 "resolved exactly once, here at A.9"; §6/frontmatter/rf-qa all READ `reflect_post_mode`, none recompute; §6.5 provenance prefix (2096) only displays predicate inputs |
| J2 | `auto` is thin band-reading wrapper, no 2nd model | PASS | SKILL.md:1064 reuses TCS/S5/S6 from `## Reflect Depth (Deterministic TCS)` (2213+); S5 ×5 (2225), S6 ×4 (2226), O1/O2/O3/O4 (2248-2261) all pre-existing; predicate authors no scoring |
| J3 | Fallback fail-closed (fixed-2 AND auto→2) | PASS | RESOLVE_AUTO Stage 2 returns `2-degraded-halt` on `risk_mode==2 ∧ W==false` (1076); ladder prose (1082) applies identically to fixed-2 + auto→2; never Mode 1, never STOP |
| J4 | FR-3 reconciliation coherent (Mode 1 inline; Rule 19 conditioned) | PASS | Rule 19 (2205) scopes "MUST NOT run inline" to 2/halt/*-degraded; explicitly excludes Mode 1; §6.2 runtime nested-executor HALT (2075); no residual blanket prohibition (2082/2091 are mode-local) |
| J5 | 8-value oracle coherent end-to-end (degraded-auto) | PASS | `auto-resolved-2-degraded-halt` present on every surface; rf-qa active map (385) + MODE-MATCH (401) + V2 8-value set (387-388) all handle the 8th value; no fall-through gap |
| J6 | Mechanically-provable emitted-item == oracle | PASS | MODE-MATCH discriminates all swap pairings (V6/V8 for 1↔2; V5/V9 vs V15 for 1↔halt); AT-MISMATCH-1 catchable |
| J7 | No orphaned/contradictory cross-references | **FAIL** | Critical Rule 20 (2207) + F3 capture comment (2050) still trigger on retired `POST_REFLECT_GATE: ENABLED`; depth reconciliation (2255-2263) internally consistent |

## Summary
- Checks passed: 6 / 7 thesis judgments
- Checks failed: 1 (J7)
- Critical issues: 1
- Important issues: 0
- Minor issues: 2
- Issues fixed in-place: 1 CRITICAL (see Actions Taken)

## Per-Judgment Evidence (adversarial trace)

### J1 — Single producer is genuine — PASS

`m` is computed exactly once at A.9: SKILL.md:1056 "The effective POST mode `m` is resolved
**exactly once, here at A.9**, before the BUILD_REQUEST is populated; no downstream surface
(frontmatter writer, emitted item, rf-qa) recomputes it." Every other surface READS the
`reflect_post_mode` oracle rather than re-deriving:

- Frontmatter writer (2001) stamps the resolved value.
- §6 templates (2074, 2083, 2096) state `reflect_post_mode: <value>` as an Output, not a
  recomputation.
- rf-qa TB-Add-9 (rf-qa.md:381) "Read the frontmatter oracle `reflect_post_mode` FIRST".
- The §6.5 `auto` provenance prefix (2096) only *displays* `S6/S5/TCS` for audit; it does not
  re-run the predicate.

No second producer found. The `auto` predicate, wrapper probe `W`, fallback ladder, and the
fixed-1 advisory all live inside the single A.9 block (1056–1086). Thesis claim "EXACTLY ONE
producer (the builder, at A.9)" delivered.

### J2 — `auto` is a thin band-reading wrapper, not a second complexity model — PASS

SKILL.md:1064 explicitly reuses "the same `TCS`, `S5`, `S6` already computed for the POST
`--depth`" and reads "the **resolved** depth band (after overrides O1/O2/O3 and the bounded ±4
tiebreaker, §4.4/INV-004)". The referenced section `## Reflect Depth (Deterministic TCS)`
exists at 2213; S5 (×5, line 2225), S6 (×4, line 2226), TCS formula (2233), O1/O2/O3/O4
(2248–2261) are all pre-existing. RESOLVE_AUTO (1066–1078) authors NO scoring/derivation — it
branches on the existing integers. Depth reconciliation note (2255–2263) closes with "NO
depth-derivation logic is authored into any emitted item (NFR-1)". NFR-1/NFR-5 delivered.

### J3 — Fallback is fail-closed (NFR-8) for BOTH fixed-2 and auto→2 — PASS

- `auto→2` path: RESOLVE_AUTO Stage 2 (1073–1077) returns `"2-degraded-halt"` when
  `risk_mode==2 ∧ W==false`, with the inline comment "NEVER silently inline Mode 1".
- fixed-`2` path: the Unified fallback ladder prose (1082) applies the same `W` probe to "a
  resolved risk-Mode 2 (a fixed `--reflect 2` OR `auto→2`)" → §6.4 manual-HALT; "NEVER degrades
  to Mode 1 ... and NEVER STOPs the build". Recorded as `2-degraded-halt` (fixed) /
  `auto-resolved-2-degraded-halt` (auto). Matches spec §8.2 table rows verbatim. Both ladders
  traced; both fail-closed to the executor-disjoint manual gate.

### J4 — FR-3 reconciliation is coherent — PASS

Rule 19 (2205) correctly conditions the inline prohibition: "The 'MUST NOT run reflect inline in
the executor's biased context' prohibition applies to modes `2` / `halt` / `*-degraded-halt` —
it does **NOT** apply to Mode 1, which DOES run `/sc:reflect` inline (same-session, audit-only)
guarded by the FR-11 top-level-executor precondition + the nested-executor HALT branch." The
§6.2 Mode-1 Verification (2075) implements the FR-11 runtime self-check: "If the executor is an
Agent-tool subagent → write `reflect_post: {verdict: blocked, reason: mode1-nested-executor}`
and HALT". Grep confirms the only other "NOT run reflect inline" strings are mode-local: 2082
(inside Mode-2 Action) and 2091 (inside the halt Action) — no residual blanket prohibition
contradicting Mode 1. The silent-Tier-2-loss risk (R3) is guarded at runtime, the PRIMARY guard
per FR-11.

### J5 — The 8-value oracle is coherent end-to-end (hardest case: `auto→2`, wrapper absent) — PASS

Walking `--reflect auto` resolving to risk-Mode 2 with `W=false`:

1. A.9 RESOLVE_AUTO Stage 2 returns `"2-degraded-halt"` (1076); §6.5 (2096) maps this to the
   §6.4 manual-HALT item with `reflect_post_mode: auto-resolved-2-degraded-halt`.
2. Template emitted: §6.4 (2087) — byte-identical legacy halt item + the single
   `<!-- wrapper-absent: degraded from Mode 2 -->` Context comment.
3. Frontmatter value written: `auto-resolved-2-degraded-halt` (enumerated in the frontmatter
   doc 2001 and rf-qa V2 387–388).
4. rf-qa validation: active map (rf-qa.md:385) includes `auto-resolved-2-degraded-halt` →
   {V1,V2,V3,V4,V15,V16}; MODE-MATCH (rf-qa.md:401) `∈ {halt, 2-degraded-halt,
   auto-resolved-2-degraded-halt} ⇒ V15 ∧ V16`; V16 (398) value set includes it. No surface
   rejects or drops the 8th value. OQ-1 closed.

### J6 — Mechanically-provable emitted-item == oracle — PASS

MODE-MATCH discriminates every swap pairing from the frontmatter field alone:

- `mode:1` + Mode-2 shell-out item → V6 fails (Mode-1 must have NO `superclaude reflect run`).
- `mode:2` + Mode-1 inline item → V8 fails (Mode-2 must have NO inline `/sc:reflect`).
- `mode:1` + halt item → V5 fails (no `--depth standard` inline) AND V9 fails (halt item carries
  `--remediate`).
- `mode:halt` + Mode-1 inline item → V15 fails (not byte-identical to legacy halt).

AT-MISMATCH-1 (swap Mode-1/Mode-2 templates) is catchable by V6/V8 as the spec requires. The
active set per mode contains the shape-discriminating assertions; no mode's active set is too
weak to discriminate.

### J7 — No orphaned/contradictory cross-references — FAIL (CRITICAL)

The depth reconciliation (2255–2263) is internally consistent (O4 preserved-and-strengthened;
O1/O2/O3 retained; mode-fixes-depth) and the validation bullet (2148) / Rule 19 (2205) / A.9
prose all point to TB-Add-9 as the single shape authority without duplicating the assertion set.

**HOWEVER** — two surfaces still trigger on the **retired** field `POST_REFLECT_GATE: ENABLED`:

- **Critical Rule 20 (SKILL.md:2207)** — "When the BUILD_REQUEST specifies `POST_REFLECT_GATE:
  ENABLED`, the builder MUST populate `executor_model_class:` ... and ... `start_commit:`".
- **F3 capture comment (SKILL.md:2050)** — "when `POST_REFLECT_GATE: ENABLED` ... MUST ALSO
  write `start_commit:` ... Conditioned on POST_REFLECT_GATE: ENABLED".

The refactor RETIRED `POST_REFLECT_GATE` as a live BUILD_REQUEST field (schema block at 856 now
emits `REFLECT_POST_MODE: 2`; `POST_REFLECT_GATE` survives ONLY as a deprecated read-time alias,
comment 862–863). So **no new build emits `POST_REFLECT_GATE: ENABLED`** — the default build
emits `REFLECT_POST_MODE: 2`. The literal trigger of Rule 20 + the F3 comment is therefore
**dead** for every new build.

Consequence (silent weakening, AX-3 omission): Mode 2 (§6.3, line 2082) derives
`--executor-model {EXECUTOR_CLASS}` and the wrapper resolves `<BASE>` from frontmatter
`start_commit` (`src/superclaude/cli/reflect/config.py:50-56,185-190`, cited in Rule 20 itself).
With the persistence rule keyed to a field that is never present, a default `--reflect 2` build
will NOT persist `start_commit` / `executor_model_class`, the wrapper falls back to dropping
`--executor-model` and to `git merge-base` for `<BASE>` — re-opening exactly the audit-F3
executor-disjoint weakening Rule 20 was authored to close. This contradicts the thesis claim that
the dial cleanly "SUBSUMES" the legacy knobs: the subsumption was applied to the schema and the
templates but NOT to the F3 persistence trigger that depended on the subsumed field.

This is the kind of cross-reference that "bites teams months later": the structural/qualitative
gates pass (the item bodies are all correct), but a runtime-critical side-effect (audit-trail
persistence feeding the wrapper) is silently disabled by a stale conditional.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | SKILL.md:2207 (Rule 20) + SKILL.md:2050 (F3 comment) | F3 persistence of `start_commit` + `executor_model_class` is keyed on the RETIRED field `POST_REFLECT_GATE: ENABLED`; new builds emit `REFLECT_POST_MODE` instead, so the trigger is dead and Mode 2's wrapper silently loses precise `<BASE>` + `--executor-model` (re-opens audit F3) | Re-condition both on the new oracle: fire when `reflect_post_mode` resolves to any non-`none` value |
| 2 | MINOR | SKILL.md:1066-1078 | RESOLVE_AUTO pseudocode shows literal `TCS >= 35` (raw) while prose (1064) says "resolved depth band"; relies on reader carrying the qualifier into the pseudocode | Optional: annotate the `TCS >= 35` line `# resolved TCS`. Mirrors spec §4.2/§4.4 split; not blocking |
| 3 | MINOR | SKILL.md:2260 | "rf-qa still asserts (`--depth quick` on any non-`halt` mode = MALFORMED)" — rf-qa asserts depth only for Mode 1 (V5's `--depth standard`); Mode 2 carries no depth literal | Optional: soften to "rf-qa asserts `--depth standard` for Mode 1 (V5); Mode 2 depth is wrapper-internal". Not a behavior defect |

## Actions Taken (fix_authorization: true — src/ only)

CRITICAL issue #1 fixed in-place in `src/superclaude/skills/task-builder/SKILL.md`:

- **F3 capture comment (SKILL.md:2050)** — retargeted the trigger from `when POST_REFLECT_GATE:
  ENABLED` to `when the resolved reflect_post_mode is ANY non-none value`, enumerating the 7
  non-`none` modes, and updated the rationale to name both the Mode-2 wrapper and the
  halt/degraded manual command as `<BASE>` consumers. Condition now reads
  `reflect_post_mode != none`.
- **Critical Rule 20 (SKILL.md:2207)** — retargeted the trigger identically (from
  `POST_REFLECT_GATE: ENABLED` to `reflect_post_mode != none`), added an explicit NOTE that the
  trigger was retargeted off the retired alias (and why keying on it would dead-trigger the
  default build and re-open F3), corrected the reversibility cite `NFR-3 → NFR-2` (byte-for-byte
  reversibility is NFR-2 in the spec), and clarified that mode `none` needs neither key.

**Verification of the fix:**

- `grep "POST_REFLECT_GATE: ENABLED"` over SKILL.md → the only remaining hits are the dial-doc
  description (43), the §5 alias-map comment (863), and Rule 20's own explanatory NOTE (2207).
  No live persistence/emission **trigger** is keyed to the retired field any longer.
- `make sync-dev` + `make verify-sync` → "✅ All components in sync."
- V15 byte-identity re-checked post-fix: halt arm (2089–2094) `diff` vs the v15-anchor snapshot
  = empty (still byte-identical; my edits did not shift or touch the halt arm).
- markdownlint: my edited lines (2050, 2207) produce zero errors under the repo ruleset
  (`.markdownlint.json`, via `markdownlint-cli` v1 in `.pre-commit-config.yaml`). The MD060
  noise from `markdownlint-cli2` is on pre-existing tables (2241/2299/2323/2399) and is not in
  the repo's enabled rule set.

Issues #2 and #3 (MINOR, optional clarity) left unaddressed by design — they are
documentation-clarity polish that mirror the spec's own structure (the spec carries the same
§4.2-pseudocode / §4.4-prose split) and are NOT behavior defects. Per the task-qualitative
"ALL findings must be resolved" rule they are listed for the orchestrator; neither blocks the
thesis and neither changes emitted behavior.

## Confidence Gate

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
  (all 7 thesis judgments traced to live file:line evidence; the one FAIL is fully diagnosed and
  fixed + re-verified)
- **Tool engagement:** Read: 9 | Grep: 6 | Glob: 0 | Bash: 9
- No UNCHECKED items. No UNVERIFIABLE items.

## Self-Audit (MANDATORY)

1. **Factual claims independently verified against source:** All 7 judgments. Key independent
   verifications: (a) re-ran the V15 byte-identity diff myself (snapshot vs live 2089–2094, rc=0)
   rather than trusting the executor's `v15-byte-check.txt`; (b) grepped all `reflect_post_mode` /
   `POST_REFLECT_GATE` / inline-prohibition strings to confirm single-producer + Rule-19
   conditioning + the dead-trigger defect; (c) read the A.9 producer (1056–1086), the TCS section
   (2213–2261), the §6 templates, and rf-qa TB-Add-9 (380–407) directly; (d) traced the 8th-value
   (`auto-resolved-2-degraded-halt`) through active map + MODE-MATCH + V2/V16 myself.
2. **Files read to verify claims:** merged-requirements.md (full, both pages);
   src/superclaude/skills/task-builder/SKILL.md (diff + targeted reads of 1053–1087, 2048–2051,
   2055–2096, 2145–2148, 2205–2209, 2213–2263); src/superclaude/agents/rf-qa.md (diff + 378–408);
   the executed phase artifacts (v15-anchor-snapshot.md, v15-byte-check.txt,
   self-consistency-walkthrough.md) — treated as a map, independently re-verified, not relied on.
3. **Why trust this review found a real issue:** It did NOT return 0 issues — the adversarial
   pass surfaced a CRITICAL dead-trigger that all prior structural + qualitative gates (and the
   executor's own self-consistency walkthrough, which checked the 5 mode-bearing surfaces but did
   NOT check the F3 persistence trigger) missed, because it is a side-effect conditional OUTSIDE
   the mode-bearing surfaces the walkthrough enumerated. The defect was verified by reasoning
   about the runtime data flow (default build emits REFLECT_POST_MODE, not POST_REFLECT_GATE →
   trigger dead → wrapper loses `<BASE>`/`--executor-model`), then fixed and re-verified.
4. **Web research:** none performed — this review is entirely local-file-bound (spec + edited
   source + cited config.py path). Tavily not invoked; no fallback triggered.

## Recommendations

1. **Accept the in-place CRITICAL fix** (Rule 20 + F3 comment retargeted to the
   `reflect_post_mode != none` oracle). The thesis is now delivered end-to-end including the F3
   audit-trail side-effect.
2. **Optionally** apply the two MINOR clarity polishes (#2 pseudocode `# resolved TCS`
   annotation; #3 soften the Mode-2 depth-assertion wording) before sign-off — low effort, no
   behavior change.
3. Re-run rf-qa structural `task-integrity` (TB-Add-9) is NOT required for this fix — the change
   touches Rule 20 / the F3 comment, not the TB-Add-9 assertion set or any emitted-item template.

## Overall Thesis Verdict

The refactor **delivers the central thesis** — ONE dial (`--reflect <none|0|1|2|auto>`) that
subsumes the three knobs, with EXACTLY ONE producer at A.9 and a mechanically-provable
emitted-item == `reflect_post_mode` oracle (TB-Add-9 V1–V16 + MODE-MATCH discriminates every
mode pairing including the 8th degraded-auto value). Six of seven adversarial judgments PASS on
first read. The single FAIL (J7) was NOT a thesis-coherence failure but an **incomplete
subsumption**: the dial correctly replaced the legacy field in the schema and templates, but one
runtime-critical side-effect trigger (the audit-F3 `start_commit`/`executor_model_class`
persistence) was left keyed to the retired `POST_REFLECT_GATE: ENABLED`, which would silently
re-open the F3 executor-disjoint weakening for every default build. That defect is now fixed
in-place and re-verified (sync clean, V15 byte-identity intact, no live trigger on the retired
field). **Post-fix: the thesis is delivered cleanly.** Verdict stands at FAIL for this pass
(the CRITICAL was present in the deliverable as reviewed); the orchestrator should accept the
applied fix and, after confirming, treat the gate as cleared.

## QA Complete
