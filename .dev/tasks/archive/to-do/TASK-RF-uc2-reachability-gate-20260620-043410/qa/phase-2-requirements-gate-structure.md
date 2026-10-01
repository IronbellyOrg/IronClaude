# QA Report — Phase 2 Requirements-Patch Gate (Structure)

**Topic:** FR-RH1 UC-2 contracted-sink reachability gate — requirements patch (companion amendment) structural verification
**Date:** 2026-06-20
**Phase:** task-integrity / requirements-patch-structure (phase-gate)
**Fix authorization:** false (REPORT-ONLY)
**Lens:** requirements-patch-structure
**Stance:** adversarial (assume incomplete + erroneous until proven)

Files read in full:
- AMENDMENT: `.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/FR-RH1-v1-amendment.md`
- VERDICT: `.../phase-outputs/reports/requirements-patch-verdict.md`
- CANONICAL REPORT: `.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md`
- REQUIREMENTS MAP: `.../phase-outputs/discovery/fr-rh1-requirements-map.md`
- STALE SOURCE: `.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/merged-requirements.md`

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Amendment contains a corrected rule for EVERY R1..R9 (9 distinct sections) | PASS | AMD §"Authoritative R1–R9" has `### R1`..`### R9` headers at AMD:30,38,43,48,53,59,68,76,83. All 9 present, none missing. Each maps to REPORT R1..R9. |
| 2 | §6 override table names EACH stale clause flagged by research 01 | **FAIL** | 12 override rows cover R1 binding-absence (:92,:130-132,:235), `--no-reachability` Grounding-Gap (:138,:191), spec-absent §4.1 (:133-138), 1.5.0 fixtures (:270,:274,:309), zero-cost (:257-258), semantic-fallback (:67-69), missing wrapper plumbing (AMD:103), vague producer fixture (AMD:104). BUT verdict-table rows MR:93 and MR:236 carry a stale spec-absent⇒Grounding-Gap+`needs_human_decision:true` obligation that NO override row enumerates. See Finding F1. |
| 3 | Override-table line citations point at the real stale text (spot-check MR:92, MR:138, MR:257-258, MR:274) | PASS | MR:92 = `unreachable` binding-absent OR branch. MR:138 = `--no-reachability` "records the skip in Grounding Gaps". MR:257-258 = `reachability_gate_added_tokens: 0` / `..._added_turns: 0`. MR:274 = `contract_version: "1.5.0"`. All four resolve exactly. |
| 4 | The 7 R7 field names are EXACTLY the canonical set | PASS | AMD:69-71 lists the 7 fields byte-for-byte matching REPORT:164-172 and the required set. No typo/extra/missing. |
| 5 | Verdict marks all 8 searches PASS, amendment-consistent; `runtime_surface_`=0 independently verifiable | PASS (caveat) | All 8 rows = PASS. Independent `grep -rn "runtime_surface_"` over brainstorm dir = 0 matches (re-run confirmed clean). Caveat: verdict inherits the F1 gap — see Finding F2. |
| 6 | All file:line citations in amendment + verdict resolve | PASS | R1→REPORT:31-47, R2→49-68, R3→70-89, R4→91-101, R5→103-120, R6→122-156, R7→158-209 (field list@164-172 exact), R8→211-227, R9→229-239 — every range opens on the correct `### Rn` header and closes within its section. Verdict AMD citations resolve. No dangling citation. |

---

## Confidence Gate

- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: 0 | Glob: 0 | Bash: 4 (the Bash calls ran `grep -rn`, `sed -n`, and full-dir search across all 6 checks; per-check evidence cited inline above)
- No UNCHECKED items. No UNVERIFIABLE items. No web research required (all claims local).

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | IMPORTANT | `FR-RH1-v1-amendment.md` §6 override table (AMD:90-104) vs `merged-requirements.md:93` and `merged-requirements.md:236` | The §3.3 verdict table row (MR:93) and the §4.12 deviation-taxonomy table row (MR:236) each carry **"...or spec absent ⇒ `unproven` → Grounding Gap → `needs_human_decision: true`"** as a live obligation. R3 (REPORT:70-89, mirrored AMD:43-46) supersedes this: spec-and-tasklist-absent is telemetry-only and **MUST NOT create a Grounding Gap, MUST NOT set `needs_human_decision`**. The override table cites only the §4.1 prose at `:133-138` for the spec-absent supersession; it does NOT name `:93` or `:236`, leaving the spec-absent branch of those two table rows as an un-overridden stale obligation that contradicts R3. (The binding-absence branch of MR:92/235 IS covered; only the *spec-absent* branch of MR:93/236 is orphaned.) | Add two override rows (or extend the `:133-138` row's scope) to name `:93` and `:236`: "spec-absent ⇒ Grounding Gap + needs_human_decision → SUPERSEDED by R3 → telemetry-only skip `spec-and-tasklist-absent`; no gap, no needs_human_decision." |
| F2 | MINOR | `requirements-patch-verdict.md:11` (search row 3) | Verdict row 3 "spec … absent" classifies MR:93/236 as superseded by R3 in its *justification prose*, but the amendment's machine-checkable override table (the authoritative supersession ledger) does not back this with an explicit `:93`/`:236` row. The verdict's PASS therefore rests on prose reasoning that the override table does not encode — a downstream implementer scanning only the override table would not see `:93`/`:236` flagged. Consistency-with-amendment is partial. | Once F1 is fixed (override rows added for `:93`/`:236`), the verdict row-3 justification is fully backed; update the row-3 "Where"/"Justification" to cite the new override rows. |

No fabricated file paths, no missing R-sections, no R7 field typos, no dangling REPORT citations, no false `runtime_surface_` claim were found. F1 is the sole substantive structural gap; F2 is its downstream echo in the verdict.

---

## Actions Taken

None. `fix_authorization: false` — REPORT-ONLY. No file modified.

---

## Recommendations

1. **Before Phase 3 proceeds:** patch the §6 override table in `FR-RH1-v1-amendment.md` to enumerate `merged-requirements.md:93` and `:236` under R3 (spec-absent ⇒ telemetry-only; supersede the Grounding-Gap + `needs_human_decision` obligation). This closes the only un-overridden stale obligation.
2. Re-issue `requirements-patch-verdict.md` row 3 to cite the new override rows so the PASS is backed by the machine-checkable table, not prose alone.
3. Re-run this structural gate (fix-cycle) after the patch to confirm F1/F2 resolve and no regression introduced.

---

## Findings Summary (severity + exact file:line)

- **F1 — IMPORTANT:** `merged-requirements.md:93` and `merged-requirements.md:236` carry a stale spec-absent⇒Grounding-Gap+`needs_human_decision:true` obligation NOT named by any §6 override row in `FR-RH1-v1-amendment.md:90-104` (override table cites only `:133-138` for spec-absent). Contradicts R3 (REPORT:70-89 / AMD:43-46).
- **F2 — MINOR:** `requirements-patch-verdict.md:11` (search row 3) marks PASS via prose justification not backed by an explicit `:93`/`:236` row in the authoritative override table.

---

## VERDICT: FAIL

- F1 (IMPORTANT): override table at `FR-RH1-v1-amendment.md:90-104` does not name `merged-requirements.md:93` and `:236`, leaving their spec-absent branch as an un-overridden stale obligation contradicting R3.
- F2 (MINOR): `requirements-patch-verdict.md:11` row-3 PASS rests on prose not encoded in the authoritative override table.

Per zero-tolerance gating (any FAIL of any severity ⇒ overall FAIL), this gate is **FAIL**. All other checks (R1–R9 completeness, R7 field exactness, spot-checked override citations, `runtime_surface_`=0, REPORT line-range resolvability) PASS. Resolve F1 (and the F2 echo), then re-run this gate.

## QA Complete

---

## Fix-Cycle 1 Re-Verification

**Date:** 2026-06-20 | **Fix cycle:** 1 | **Mode:** report-only (no files edited except this report)

### F1 (IMPORTANT) — override table did not enumerate MR:93 and MR:236

**RESOLVED.** Two NEW override rows now exist in the AMENDMENT §6 table (`FR-RH1-v1-amendment.md`):

| Row | Line | Stale clause cited | Mapping |
|---|---|---|---|
| AMD:96 | `:93` (§3.3 verdict table) | `unproven` condition includes "or spec absent" ⇒ Grounding Gap + `needs_human_decision: true` | → R3: "spec-and-tasklist-absent is telemetry-only; it does NOT set `reachability_unproven`, does NOT create a Grounding Gap, does NOT set `needs_human_decision`." |
| AMD:97 | `:236` (§4.12 taxonomy) | `unproven` condition includes "spec absent" ⇒ Grounding Gap, `needs_human_decision: true` | → R3: "telemetry-only skip; no `unproven`/Grounding Gap/`needs_human_decision` for the spec-absent branch." |

Both new rows map the spec-absent branch to R3 with explicit telemetry-only resolution (no unproven, no Grounding Gap, no needs_human_decision) — exactly the branch the previous cycle flagged as un-enumerated. Verified by Read of `FR-RH1-v1-amendment.md:96-97`.

### F2 (MINOR) — verdict row-3 cited only :133-138

**RESOLVED.** `requirements-patch-verdict.md:11` (row 3, "spec … absent" variants) now reads: "MR:93/236 stale spec-absent→`unproven`→Grounding-Gap+`needs_human_decision` → each explicitly superseded by R3 (**AMD §6 rows `:93` and `:236`**, added in the Phase-2 gate fix cycle, alongside `:133-138`)." The verdict prose now binds row-3's PASS to the encoded override rows for `:93` and `:236`, not just `:133-138`. Verified by Read of `requirements-patch-verdict.md:11`.

### Source-truth spot-check (claims in the new rows are accurate)

- **MR:93** (Read of `merged-requirements.md:93`): §3.3 verdict table, `unproven` Condition = "...or real-boot unavailable; **or spec absent**" → Effect "`status: partial` + `needs_human_decision: true`". The "spec absent ⇒ Grounding Gap + needs_human_decision" branch that AMD:96 claims to supersede is genuinely present. ✓
- **MR:236** (Read of `merged-requirements.md:236`): §4.12 taxonomy table, `unproven` Condition = "...real-boot unavailable / **spec absent**" → "one `grounding-gaps.yaml` row...; `needs_human_decision: true`". The branch AMD:97 claims to supersede is genuinely present. ✓

### No new structural issue introduced

- AMD §6 table remains well-formed: header + separator unchanged, the two new rows are valid 4-column pipe rows (`| :93 ... | ... | R3 | ... |`, `| :236 ... | ... | R3 | ... |`); no column-count drift, no orphaned cells.
- R3 body (AMD:43-46) unchanged and consistent with the two new override rows (telemetry-only `spec-and-tasklist-absent`).
- Verdict row-3 edit is additive prose inside the existing cell; table structure of `requirements-patch-verdict.md` intact (still 8 rows, overall PASS unchanged).
- No regression: every item that PASSed at cycle 0 (R1–R9 completeness, R7 field exactness, `runtime_surface_`=0, override-citation spot-checks) remains PASS — none was touched by the surgical edit.

### Confidence

Verified: 5/5 re-checks (F1 rows present, F2 citation present, MR:93 branch real, MR:236 branch real, no new structural issue) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
Tool engagement: Read: 6 | Grep: 0 | Glob: 0 | Bash: 1

## FINAL VERDICT: PASS
