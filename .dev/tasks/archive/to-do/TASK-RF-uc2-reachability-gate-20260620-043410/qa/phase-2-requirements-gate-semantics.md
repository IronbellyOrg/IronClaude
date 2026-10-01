# QA Report — Phase-Gate Qualitative (Requirements Patch FR-RH1 Semantics)

**Topic:** FR-RH1 UC-2 contracted-sink reachability gate — requirements amendment semantic fidelity
**Date:** 2026-06-20
**Phase:** phase-gate-qualitative (lens: requirements-patch-fr-rh1-semantics)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT-ONLY)
**Adversarial stance:** Assume the patched requirements accidentally preserved unsafe pre-patch semantics. Goal = find every semantic leak.

---

## Method

Read in full: AMENDMENT (`FR-RH1-v1-amendment.md`), CANONICAL REPORT (ground truth,
`pre-uc2-reachability-gate-20260620-041729/REPORT.md`), VERDICT (`requirements-patch-verdict.md`),
REQUIREMENTS MAP (`fr-rh1-requirements-map.md`), STALE SOURCE (`merged-requirements.md`, abbrev MR).

For each rule R1–R9 + R7 consistency + authority assertion: traced the amendment clause against the
REPORT worked rule, then independently confirmed the cited stale MR lines actually contain the unsafe
pre-patch text the amendment claims to supersede (the adversarial concern is a *carried* unsafe clause,
not just a paraphrase).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| R1 | Regression/`unreachable` is REAL-BOOT-ONLY; no static-binding-absence+oracle_mismatch ⇒ unreachable path survives | PASS | See R1 below |
| R2 | `--no-reachability` telemetry-only (no gap, no needs_human_decision, no status:partial) | PASS | See R2 below |
| R3 | spec-and-tasklist-absent telemetry-only (no gap, no reachability_unproven, no status change) | PASS | See R3 below |
| R4 | reachability fields ship under `1.6.0`, never `1.5.0`; 1.5.0 reserved D13-only | PASS | See R4 below |
| R8 | zero-cost claims replaced by bounded caps; no `..._added_tokens/turns: 0` survives | PASS | See R8 below |
| R9 | semantic fallback advisory-only; explicit `durable_sink:`/`@sink` SOLE v1 blocking trigger | PASS | See R9 below |
| R7c | `unreachable>0 ⟹ real_boot ∧ regression ∧ vrd≥unreachable`; `unproven>0 ⟹ gap ∧ needs_human_decision` | PASS | See R7 below |
| AUTH | amendment asserts authority over MR so implementer won't pick up a stale clause | PASS | See AUTH below |

---

## Detailed findings

### R1 — Regression/`unreachable` is REAL-BOOT-ONLY (CRITICAL check) — PASS

REPORT ground truth (`REPORT:36,44-47`): `unreachable` is set ONLY when a real-boot verifier runs and
observes the contracted sink absent. The verdict table row (`REPORT:44`) condition is the bare
"**Real boot ran and observed the contracted sink absent**" — the original OR-branch
("binding unambiguously absent AND oracle_mismatch confirmed") is deleted, and `REPORT:47` explicitly
states this "resolves the original contradiction."

Amendment (`AMD:30-36`): R1 says `unreachable` is set "**ONLY** when a real-boot verifier runs and
observes the contracted sink **absent**." Static signals (missing binding, discarded emitter result,
oracle mismatch) → "at most `unproven`." `AMD:35-36` adds the explicit negative clause:
"**No clause may permit 'static binding absence AND oracle_mismatch ⇒ unreachable/Regression'.**
Such a verdict is `unproven`, never Regression." Safety closure `AMD:113-115` repeats it.

Adversarial leak check — did any unsafe pre-patch OR-branch survive as a LIVE requirement?
- MR:92 (verdict table) carries the stale `unreachable` OR-branch "binding unambiguously absent AND
  oracle_mismatch confirmed." Confirmed present verbatim at MR line 92.
- MR:130-132 (§4.1 step 5.6 prose) carries "real-boot observed … — OR binding unambiguously absent AND
  `oracle_mismatch` confirmed ⇒ `unreachable`." Confirmed present at MR lines 130-132.
- MR:235 (§4.12 taxonomy table) carries the same OR-branch. Confirmed at MR line 235.
- All three are named in the AMD §6 override table (`AMD:92-94,98`) and marked **SUPERSEDED → real-boot
  only / drop the OR branch**. The verdict file (`requirements-patch-verdict.md:9`) independently audits
  the `binding unambiguously absent` string across all 5 occurrences and confirms every MR occurrence is
  superseded, every AMD occurrence is override prose.

Result: The unsafe path exists ONLY in the historical MR artifact and is explicitly overridden; the
authoritative requirements (AMD R1) carry the real-boot-only rule plus an explicit prohibition. **PASS.**

### R2 — `--no-reachability` is telemetry-only — PASS

REPORT (`REPORT:49-68`): `--no-reachability` sets only `reachability_gate_ran: false` +
`reachability_skip_reason: --no-reachability`; "MUST NOT create or append to `grounding-gaps.yaml`,
MUST NOT set `needs_human_decision`, and MUST NOT force `status: partial`."

Amendment (`AMD:38-41`): R2 states exactly this — ledger null, scanned/unreachable/unproven = 0,
`reachability_real_boot_ran: false`; "MUST NOT create/append `grounding-gaps.yaml`, MUST NOT set
`needs_human_decision`, MUST NOT force `status: partial`." Closure `AMD:116-117` restates.

Leak check: MR:138 (§4.1) and MR:191 (§4.7 reflect.md flag row) both say `--no-reachability`
"records the skip in Grounding Gaps." Confirmed verbatim at MR lines 138 and 191. Both named in the AMD
§6 override table (`AMD:96-97`) → **SUPERSEDED → telemetry-only; no Grounding Gap.** Verdict file row 2
(`verdict.md:10`) confirms. **PASS.**

### R3 — spec-and-tasklist-absent is telemetry-only — PASS

REPORT (`REPORT:70-89`): neither `--spec` nor `--tasklist` → no blocking gate; may emit non-blocking
telemetry but "MUST NOT create a Grounding Gap, MUST NOT set `needs_human_decision`, and MUST NOT change
the run status." Skip reason `spec-and-tasklist-absent`. Invariant (`REPORT:80-87`) sets
scanned/unreachable/unproven = 0.

Amendment (`AMD:43-46`): R3 matches — telemetry-only, "MUST NOT create a Grounding Gap, set
`needs_human_decision`, set `reachability_unproven`, or change status." Skip reason
`spec-and-tasklist-absent`. Note AMD goes slightly stronger than REPORT by adding the explicit
"set `reachability_unproven`" prohibition — a safe narrowing, consistent with the invariant.

Leak check: the dangerous pre-patch behavior is the *spec-absent diff-side probe → single `unproven`
row → Grounding Gap*. MR:71-75 (§3.1 spec-absent default) and MR:93 (verdict table: `unproven` … "or
spec absent") and MR:133-138 (§4.1: "spec/tasklist absent ⇒ `unproven` → §10.6 Grounding Gap") and
MR:236 (taxonomy: "spec absent" → Grounding Gap) all carry the stale fail-to-`unproven` behavior.
Confirmed at those MR lines. AMD §6 override table row `:133-138` (`AMD:95`) → **SUPERSEDED →
telemetry-only skip `spec-and-tasklist-absent`.** Verdict file row 3 (`verdict.md:11`) confirms MR:93/236
superseded and notes MR:161 (the skip-reason enum listing `spec-and-tasklist-absent`) is consistent with
R3, not stale. **PASS.**

### R4 — reachability fields ship under `1.6.0`, never `1.5.0` — PASS

REPORT (`REPORT:91-101`): reachability stable fields are additive top-level → contract `1.6.0`;
`1.5.0` "must continue to mean only the D13 additive contract: `coverage_pct_union`, `coverage_degraded`,
and `unmapped_requirements_union`."

Amendment (`AMD:48-51`): R4 matches — "ship under `contract_version: '1.6.0'`, **never `1.5.0`**";
every fixture/template/eval/version-test bearing reachability fields uses `1.6.0`; "`1.5.0` remains the
D13-only set." R6 producer-fixture assertions (`AMD:62`) and R7 (`AMD:69`) both pin `1.6.0`.

Leak check: MR:274 and MR:309 — the two MR self-test fixtures — both carry reachability fields under
`contract_version: "1.5.0"` (MR:270 even instructs "bump `contract_version` to `'1.5.0'`"). Confirmed
verbatim at MR lines 274 and 309. AMD §6 override row `:270,:274,:309` (`AMD:101`) → **SUPERSEDED →
`1.6.0`.** Verdict file row 4 (`verdict.md:12`) confirms. **PASS.** (The requirements-map `:19-20`
independently re-derives `1.6.0` from `REPORT:91-99`.)

### R8 — zero-cost claims replaced by bounded caps — PASS

REPORT (`REPORT:211-227`): replaces `reachability_gate_added_tokens: 0` /
`reachability_gate_added_turns: 0` with `..._added_tool_classes: 0`,
`..._added_turns_per_side_effect_requirement: "1-3"`, `..._max_side_effect_requirements_scanned: 12`,
`..._added_turns_cap: 36`, `..._real_boot_invocations_cap: 1`; overflow >12 → `reachability_sampled:
true` + non-blocking coverage warning.

Amendment (`AMD:76-81`): R8 reproduces all five bounded fields verbatim and adds the explicit negative:
"**No `reachability_gate_added_tokens: 0` / `..._turns: 0` may remain.**"

Leak check: MR:257 (`reachability_gate_added_tokens: 0`) and MR:258 (`reachability_gate_added_turns: 0`)
confirmed verbatim. AMD §6 override row `:257-258` (`AMD:99`) → **SUPERSEDED → bounded caps.** Verdict
file rows 5–6 (`verdict.md:13-14`) confirm. **PASS.**

### R9 — semantic fallback advisory-only; explicit annotation SOLE v1 trigger — PASS

REPORT (`REPORT:229-239`): v1 uses explicit `durable_sink:` / `@sink` as "the only blocking trigger";
without an explicit annotation, semantic classification "may record an advisory candidate but MUST NOT
set `reachability_unproven`, MUST NOT write a reachability Grounding Gap, and MUST NOT affect `status`."

Amendment (`AMD:83-86`): R9 matches — "v1 blocking trigger = explicit machine-readable `durable_sink:`
/ `@sink` ONLY"; semantic classification "may record an advisory candidate but MUST NOT set
`reachability_unproven`, write a reachability Grounding Gap, or affect `status`." Closure `AMD:118`
restates: explicit annotation is "the sole v1 blocking trigger."

Leak check: the dangerous pre-patch behavior is MR:66-69 (§3.1 resolution order) where semantic
classification is the *second* resolution path and an unresolvable semantic sink → "the row is `unproven`
(not skipped, not Regression)" — i.e., semantic classification CAN drive `unproven` (a blocking gap).
Confirmed at MR lines 66-69. AMD §6 override row `:67-69` (`AMD:100`) → **SUPERSEDED → advisory telemetry
only; no `unproven`/gap/status.** Verdict file row 7 (`verdict.md:15`) confirms MR:67. **PASS.**

### R7 consistency — invariant arithmetic — PASS

Required by the spawn prompt: the amendment must state
`unreachable>0 ⟹ real_boot_ran ∧ regression_present ∧ verification_regressions_detected ≥
reachability_unreachable` and `unproven>0 ⟹ grounding_gaps_path ∧ needs_human_decision`.

Amendment (`AMD:73-74`): R7 states verbatim —
"`unreachable>0 ⟹ real_boot_ran ∧ regression_present ∧ verification_regressions_detected ≥
reachability_unreachable`; `unproven>0 ⟹ grounding_gaps_path non-null ∧ needs_human_decision`."

Cross-check vs REPORT (`REPORT:199-208`): the `if reachability_unreachable > 0` block requires
`reachability_real_boot_ran: true`, `regression_present: true`,
`verification_regressions_detected: ">= reachability_unreachable"`; the `if reachability_unproven > 0`
block requires `grounding_gaps_path: <non-null path>` + `needs_human_decision: true`. Arithmetic matches
exactly (the `≥` relation, not `==`, is preserved — correct, since one unreachable could co-exist with
other regressions). R6 producer-fixture (`AMD:62-64`) is internally consistent with R7: it asserts
`reachability_unproven: 1` together with `needs_human_decision: true` + `status: partial` + a
`grounding-gaps`-routed ledger row (`gap_kind: oracle-mismatch`), satisfying the `unproven>0` invariant;
and `reachability_unreachable: 0` so the unreachable invariant is vacuously satisfied. **PASS.**

### AUTH — amendment asserts authority over merged-requirements.md — PASS

Frontmatter (`AMD:3-5`): `status: amendment-authoritative`, `supersedes: merged-requirements.md`,
`canonical_source:` → the REPORT path. Body **Authority rule** (`AMD:23-26`): "For FR-RH1
implementation, **this amendment + `REPORT` R1–R9 are the ONLY authoritative requirements source.** Where
any clause in `merged-requirements.md` conflicts with R1–R9 below, the clause in `merged-requirements.md`
is **SUPERSEDED and MUST NOT be implemented**." The §6 override table (`AMD:88-104`) names every stale
clause by line with an explicit corrected rule and an "Override" disposition column. The verdict file
(`verdict.md:3`) reinforces: "Authoritative source for implementation = `FR-RH1-v1-amendment.md` +
`REPORT`"; and the requirements-map patch-note (`map:48-49`) flags the same. An implementer who reads the
amendment first (the authoritative artifact) is directed away from every stale MR clause by line number.
**PASS.**

A residual note (MINOR, non-blocking): `merged-requirements.md` itself carries **no** in-file banner
pointing to the amendment — its frontmatter still reads `status: merged-requirements` with no
`superseded-by` field. An implementer who opens MR *directly* (bypassing the amendment) gets no inline
signal that MR:92/130-132/138/191/235/257-258/274/309/67-69 are dead. The companion-amendment strategy
is explicitly sanctioned (non-destructive, parallel-session-safe per `AMD:19-21`) and the authority chain
is sound *through the amendment*, so this does not reintroduce unsafe semantics and is not a FAIL. It is
recorded as a hardening opportunity only.

---

## Self-Audit

1. **Claims independently verified against source:** 8 semantic checks (R1, R2, R3, R4, R8, R9, R7c,
   AUTH). For each, both the amendment clause AND the cited stale MR line(s) were read and compared
   against the canonical REPORT — not taken on the verdict file's word. The verdict file's own
   `binding unambiguously absent` / `records the skip in Grounding Gaps` / `1.5.0` / zero-cost /
   `semantic classification` string findings were re-confirmed at the actual MR line numbers (92, 130-132,
   138, 191, 235, 257-258, 274, 309, 66-69).
2. **Files read in full:** FR-RH1-v1-amendment.md (119 lines), REPORT.md (271 lines),
   requirements-patch-verdict.md (31 lines), fr-rh1-requirements-map.md (50 lines),
   merged-requirements.md (425 lines).
3. **Why trust this review:** the adversarial concern (a *carried* unsafe clause) was tested by reading
   each named stale MR line directly and confirming it is (a) genuinely present as unsafe pre-patch text
   AND (b) explicitly named + overridden in the AMD §6 table. The one finding that surfaced (no in-file
   supersession banner on MR) is recorded; it is a navigational hardening note, not a semantic leak,
   because the authority chain through the amendment is intact.
4. **Web research:** none performed — this review is entirely local-file-bound. No Tavily/fallback used.

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 0

(6 Reads vs 8 checks: the 5 input files were each read in full once, plus 1 report re-Read for the
freshness gate. Each check was verified against content from those whole-file reads — no check relied on
content outside the read set. Grep was unnecessary because every cited line was within the fully-read
files; line-number citations were confirmed against the cat -n output.)

---

## Summary

- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (MR has no in-file `superseded-by` banner — navigational hardening only, not a
  semantic leak; the authority chain through the amendment is sound)
- Issues fixed in-place: 0 (REPORT-ONLY)

The amendment faithfully encodes the SAFE, narrowed v1 semantics from the canonical patched REPORT and
does NOT reintroduce any unsafe pre-patch behavior. Every dangerous pre-patch clause (non-real-boot
Regression, `--no-reachability`/spec-absent writing Grounding Gaps, reachability fields under `1.5.0`,
zero-cost claims, semantic classification as a blocking trigger) exists only in the historical
`merged-requirements.md` artifact and is explicitly named-and-superseded by the AMD §6 override table.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `merged-requirements.md:1-11` (frontmatter) | MR carries no in-file pointer to the authoritative amendment (`status: merged-requirements`, no `superseded-by:` field). An implementer opening MR directly — bypassing the amendment — gets no inline signal that the stale clauses are dead. Authority chain is still sound *through the amendment*, so no semantic leak. | Add a frontmatter `superseded-by: FR-RH1-v1-amendment.md` field and/or a top-of-file banner: "SUPERSEDED for FR-RH1 implementation — authoritative source is FR-RH1-v1-amendment.md + REPORT R1–R9." Non-blocking. |

## Recommendations

- Proceed to Phase 3 / implementation on the **amendment + REPORT R1–R9**, never on the stale
  `merged-requirements.md` clauses (matching the verdict file's disposition).
- Optionally apply the MINOR hardening (MR frontmatter `superseded-by` banner) to make the historical
  artifact self-disclosing for any implementer who opens it directly.

## VERDICT: PASS

- R1 (CRITICAL) — PASS: `unreachable`/Regression is real-boot-only; AMD:35-36 + AMD:113-115 explicitly
  prohibit static-binding-absence+oracle_mismatch ⇒ unreachable; MR:92/130-132/235 OR-branches confirmed
  superseded (AMD §6 rows :92,:130-132,:235), not carried.
- R2 — PASS: `--no-reachability` telemetry-only (AMD:38-41); MR:138/191 "records the skip in Grounding
  Gaps" superseded (AMD §6 rows :138,:191).
- R3 — PASS: spec-and-tasklist-absent telemetry-only (AMD:43-46, adds explicit no-`reachability_unproven`
  prohibition); MR:93/133-138/236 superseded (AMD §6 row :133-138).
- R4 — PASS: reachability fields ship under `1.6.0`, 1.5.0 reserved D13-only (AMD:48-51); MR:274/309
  superseded (AMD §6 row :270,:274,:309).
- R8 — PASS: zero-cost replaced by 5 bounded caps + explicit "must not remain" (AMD:76-81); MR:257-258
  superseded (AMD §6 row :257-258).
- R9 — PASS: semantic fallback advisory-only, explicit `durable_sink:`/`@sink` sole v1 blocking trigger
  (AMD:83-86, AMD:118); MR:66-69 superseded (AMD §6 row :67-69).
- R7 consistency — PASS: AMD:73-74 states both invariants verbatim; matches REPORT:199-208 arithmetic
  (`≥` relation preserved); R6 producer-fixture internally consistent.
- AUTH — PASS: AMD frontmatter + Authority rule (AMD:23-26) + §6 line-by-line override table assert
  authority over MR; verdict.md:3 + map:48-49 corroborate.
- MINOR (non-blocking, does not affect verdict) — MR carries no in-file `superseded-by` banner
  (`merged-requirements.md:1-11`).

## QA Complete
