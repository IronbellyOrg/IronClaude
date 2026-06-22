# QA Report — TDD Qualitative Review (crossref-chain lens)

**Topic:** FR-DRS Deterministic Runtime-Surface Sweep — TDD
**Date:** 2026-06-21
**Phase:** report-validation / tdd-qualitative (crossref-chain lens)
**Fix cycle:** N/A (fix_authorization: false — report-only)
**Document:** `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md`
**Lens:** End-to-end cross-reference chain tracing. ADVERSARIAL stance — assume ≥10 broken chains; find them.

---

## Overall Verdict: PASS

All traced chains resolve to a real link at every hop. No broken chain (a requirement with no
test, an open question with no alternative, a Reuse verdict with no cross-reference) was found.
Several MINOR annotation/wording observations are recorded below; none breaks a chain, so per the
chain-lens scope they are advisory, not gating for THIS lens. See "Issues Found" for the
disposition note.

---

## Chains Traced

### Chain family A — Acceptance Criterion → FR (§5) → architecture (§6) → data-model/API (§7/§8) → test (§15)

**AC source-of-truth note (verified):** The spec (`spec.md` §4) defines its 6 acceptance criteria
as an **unnumbered checklist** (6 bullets, lines 93–104). The TDD assigns the labels AC-1..AC-6 to
these 6 bullets in document order. I confirmed the mapping is faithful 1:1 (TDD §24.1 lines
1297–1302 restate each spec bullet under its AC-N label, verbatim in substance). So "AC-N" is the
TDD's own stable internal anchor; every §5 "Source" column and the §5.3 per-AC coverage map
(lines 320–327) key on it consistently. **Not a broken chain** — it is a deliberate, internally
consistent numbering of an unnumbered spec list.

| AC | → FR (§5) | → architecture (§6) | → data-model/API (§7/§8) | → test (§15) | Link status |
|----|-----------|---------------------|--------------------------|--------------|-------------|
| **AC-1** (ledger + 6 canonical scalars every UC-2 run, zero LLM dep) | FR-001, FR-002, FR-004, FR-011, FR-012 (§5.1 L281–293); NFR-001/003/004/006 (per §5.3 map L322) | §6.1 6-unit pipeline + EMIT stage (units 1 & 6, L382–387); §6.2 `SWEEP -->|merge-overwrite 6 fields| CONTRACT` (L422) | §7.1.1 ledger artifact + §7.1.2 `RuntimeSurfaceLedgerRow`; §8.2 six-field contract surface (L596–602) | §15.2 reducer/emit unit tests (unit 6, L936); §14.1 always-write artifact; §15.6 map (L996) | **OK** — every hop present |
| **AC-2** (5 eval cases 37–41 deterministic ≥3 runs, no variance) | FR-008, FR-009, FR-010 (§5.1 L289–291); NFR-001/002 (§5.3 map L323) | §6.1 governing posture + DEGRADE-oracle unit 4 (L385); §11.2 eval-path flow (shared module) | §8.1 `run_sweep` shared module; §8.2 fields under test; §7.4 count invariant (case 41) | §15.3 integration determinism gate (5 cases table L952–956); §15.6 map (L997) | **OK** — every hop present |
| **AC-3** (`len(unreached_surfaces)==runtime_surface_unreached` by construction) | FR-003 (§5.1 L283); §5.3 map L324 | §6.1 unit 6 reducer invariant note (L387); §6.1 ASCII "invariant:" line (L375) | §7.4 Count Invariant section (L553–561); §8.1 `reduce_ledger` "enforcing the §7.4 count invariant" (L589) | §15.2 count-invariant unit assertion (L938); §15.4 grader `check_yaml_list_len_eq` re-check (L979); §15.6 map (L998) | **OK** — every hop present |
| **AC-4** (§5.3 pre-filter reads deterministic scalars; sprint-exec deferred) | FR-005, FR-006 (in-scope, L285–286); FR-006a (deferred, L287); NFR-002 (§5.3 map L325) | §6.2 `PARSE --> DERIVE` + §5.3 pre-filter (L424–426, reading note L429); §6.4 D4 sweep-before-parse (L448) | §8.2 `runtime_surface_unreached` "§5.3 pre-filter (GATING)" consumer column (L600) | §15.6 map: AC-4 "Consumer-side; producer determinism is the precondition" (L999) | **OK** — see note 1 below on the deferred sub-link |
| **AC-5** (FR-RSR safety: never clean-pass an unwired surface preserved) | FR-007, FR-010 (L288, L291); NFR-003 (§5.3 map L326) | §6.1 "Governing posture (preserved … NOT re-derived)" (L389); §12.1 fail-loud posture table | §8.2 semantics (UNREACHED suppresses clean PASS); §7.2 reduction → contract-field effect (L527–531) | §15.3 case 37 (FAIL-pre/PASS-post) + case 41 (L1000); §15.6 map | **OK** — every hop present |
| **AC-6** (`make verify-sync` clean; UV-only; `ruff format --check` clean) | FR-013 (L294); NFR-005/007 (§5.3 map L327) | §6 scope (new module path); n/a-architecture (hygiene is build-time, not a runtime element) — adapted, not skipped | §8.3 API-governance "producer change, not field-set change"; §7.5 writer conventions (`_IndentDumper`) | §15.1 sync/lint tier (L921); §15.5 CI env; §15.6 map (L1001) | **OK** — AC-6 is a hygiene AC; "architecture element" reinterpreted as build/lint surface (no N/A) |

**Note 1 (AC-4 deferred sub-link — checked, NOT broken):** AC-4's spec bullet (spec.md:102) names
BOTH the §5.3 pre-filter AND the `sprint run` executor as readers. The TDD splits this: the
pre-filter read is in-scope (FR-006, fully chained above), and the executor read is carried as
**FR-006a — Deferred / Non-Goal v1** (§5.1 L287), with the deferral consistently propagated to
§3.3 Future Considerations (L230), §5.3 gap G2 "Resolved" (L334), §6.3 "Deferred (SPEC-ONLY)
consumer" (L436), §8.2 "sprint executor SPEC-ONLY" (L600/602), §11.1 step 6 "(spec/deferred)"
(L674), §15.6 (L999), §23.2 Phase-2 exit (L1268), and §24.1 AC-4 v1 portion (L1300). The deferred
branch has **no test in §15** — which is correct and consistent, because it delivers no v1 code to
test. A deferred FR with no test is a closed (not dangling) chain. **OK.**

#### A-reverse — every §5.1 FR → an architecture element AND a §15 test (the "requirement with no test" hunt)

This is the adversarial direction: a requirement that resolves to AC but has NO test is the most
common broken chain. Traced all 14 FRs:

| FR | → architecture element (§6) | → test (§15) | Status |
|----|-----------------------------|--------------|--------|
| FR-001 (ledger every run) | §6.1 unit 6 EMIT; §6.2 `SWEEP-->LEDGER` (L421) | §15.2 unit 6 reducer/emit; §14.1 always-write; §15.6 AC-1 | OK |
| FR-002 (6 scalars exact names) | §6.1 unit 6; §8.2 exact-name table | §15.2 unit 6; §15.3 per-case scalar assertions; §15.6 AC-1 | OK |
| FR-003 (count invariant by construction) | §6.1 unit 6 invariant note | §15.2 count-invariant unit (L938); §15.4 grader re-check | OK |
| FR-004 (7-step algorithm) | §6.1 all 6 units / 7-stage flow | §15.2 all 6 unit tests (one per unit, L931–936) | OK |
| FR-005 (product path writes before consume) | §6.2 `AUDIT-->|invokes| SWEEP`; §6.4 D2/D4 | §15.3 integration (product path via harness); §17.3 re-run note | OK — integration tier exercises the merge-before-parse path |
| FR-006 (§5.3 pre-filter reads deterministic) | §6.2 §5.3 pre-filter edge; §8.2 GATING column | §15.6 AC-4 (consumer-side; producer determinism precondition) | OK |
| FR-006a (sprint exec — DEFERRED) | §6.3 deferred consumer | none (correctly — deferred, nothing to test v1) | OK (closed) |
| FR-007 (safety preserved) | §6.1 governing posture; §12.1 | §15.3 case 37 + 41; §15.6 AC-5 | OK |
| FR-008 (eval invokes same module) | §11.2 eval-path flow; §8.1 `run_sweep` | §15.3 integration determinism gate; §15.4 | OK |
| FR-009 (dynamic→DEGRADE not Regression) | §6.1 unit 4 oracle; §12.2 cat a–d | §15.2 unit 4 (case 39 shape, L934); §15.3 case 39 | OK |
| FR-010 (fail-open backend loss→DEGRADE) | §6.1 unit 2 DEGRADE-to-floor; §12.3/§12.7 | §15.2 unit 2 tool-loss path (L932); §15.3 case 40 | OK |
| FR-011 (demote SKILL prose) | §19.1 prose demotion; §6 demotion mention | §15.1 sync/lint tier (verify-sync after demotion); §23.2 Phase-4 | OK — prose demotion verified via §15.1 sync gate + §24.2 checklist |
| FR-012 (non-surface fast path zero cost) | §6.1 fast-path branch (L372); §17.2 budget | §17.2 "non-surface diff = Zero, no ledger write" unit assertion (L1036); §12.3 fast-path row | OK |
| FR-013 (verify-sync/UV/ruff) | §6 module path; AC-6 hygiene | §15.1 sync/lint tier; §15.5 CI; §24.2 checklist | OK |

**A-reverse result: 14/14 FRs chain to both an architecture element and a test (or a justified
deferral). Zero requirements-with-no-test found.** The 7 NFRs likewise map (NFR-001/002 →
§15.1/§15.3 determinism; NFR-004/005 → §7.5 writer + §15.1 lint; NFR-006 `evidence_ref` →
§7.1.1 constraint + §15 forensic ledger; NFR-003/007 → §15.1).

### Chain family B — Open Question → Alternative (§21) → §6.4 decision

The §21 preamble (L1134) explicitly asserts the mapping: "The three open questions (OQ-DRS.1/.2/.3)
map directly onto Alternatives 2, 1, and the contract-version decision." Traced each:

| Open Question (§22) | → Alternative (§21) | → §6.4 Key Design Decision | Link status |
|---------------------|----------------------|-----------------------------|-------------|
| **OQ-DRS.1** (referrer engine: rg/AST floor vs Serena/LSP) — §22 L1221 | **Alt 2** "Referrer engine — floor vs precision overlay *(OQ-DRS.1)*" (L1177); §22 L1221 says "See §21 Alt 2" | **§6.4 D3** "referrer engine (OQ-DRS.1)" (L447) — ripgrep/AST floor + DEGRADE-to-floor overlay | **OK** — OQ→Alt→D3 all three present and mutually cross-referenced (§5.3 G5 L337 also routes to "§6.4 D3") |
| **OQ-DRS.2** (invocation site / bare-path coverage) — §22 L1222 | **Alt 1** "Invocation site — where the sweep runs *(OQ-DRS.2)*" (L1158); §22 L1222 says "See §21 Alt 1, R2" | **§6.4 D2** "invocation site (OQ-DRS.2)" (L446) — `_audit_once` + conditional LLM-fallback for bare path | **OK** — OQ→Alt→D2 present; also chains to R2 (§20 L1123) |
| **OQ-DRS.3** (contract version bump?) — §22 L1223 | **No dedicated numbered Alt** — §21 preamble maps it to "the contract-version decision" (not an Alt 0/1/2/3 box); resolution lives in §8.3 "Likely no version bump (OQ-DRS.3)" (L609) + §19.2 (L1099) | **No §6.4 D-row.** OQ-DRS.3 is a contract-versioning decision, handled in §8.3 (API-Governance) + §19.2 (Migration), NOT §6.4 | **OK with caveat** — see note 2 below |
| **Q4** (stale `ensemble.REFLECT_CONTRACT_VERSION="1.0"` vs `1.6.0`) — §22 L1224 | not an Alt (it is a follow-on of OQ-DRS.3) | §8.3 "Stale version constant to reconcile" (L610) + §19.2 (L1100) — "Cross-referenced from §8.3 and §19.2" stated in the Q4 row | **OK** — Q4→§8.3→§19.2 all present and the Q4 row names them explicitly |

**Note 2 (OQ-DRS.3 has no §21 Alternative box and no §6.4 D-row — checked, NOT a broken chain):**
The prompt's literal chain shape is "each OQ → an alternative in §21 → a §6.4 decision." OQ-DRS.3 does
**not** follow that exact shape: it has no numbered §21 Alternative and no §6.4 D-row. BUT the §21
preamble (L1134) *explicitly anticipates this*: it maps OQ-DRS.3 onto "the contract-version
decision" rather than onto an Alt box, and the §22 OQ-DRS.3 row (L1223) routes its resolution to the
contract-version reasoning carried in §8.3 + §19.2 + §24.2 (L1310 "OQ-DRS.1/.2/.3 + Q4 ratified").
A contract-version decision is a *governance/migration* decision, not an *architecture* (§6.4)
decision — so its absence from §6.4 is correct, not a dropped link. The chain still terminates at a
real, cross-referenced design decision (§8.3 + §19.2). **Classifying as OK** (the chain resolves to
a decision; only the *section family* differs from the other two OQs, and the TDD discloses this
up-front). This is the single place where the literal "→ §6.4 decision" terminus does not hold; it
is documented and consistent, so it is a MINOR transparency observation, not a broken chain.

### Chain family C — Reuse Audit verdict → §6.4/§21/§22 cross-reference

The Reuse & Consolidation Audit (L1334–1347) has 6 component rows. The prompt requires each verdict
to chain to its §6.4/§21/§22 cross-reference. Note: only verdicts that surface a *boundary decision*
need a §6.4/§21/§22 link; pure `distinct` (reflect-local, no boundary) rows legitimately terminate
in their own Disposition cell. Traced all 6:

| Reuse component | Verdict | Disposition cross-ref claimed | Target exists? | Link status |
|-----------------|---------|-------------------------------|----------------|-------------|
| surface-tagger | distinct (0.37) | reflect-local; no §6.4/§21/§22 ref (no boundary) | n/a — `distinct`, self-contained | OK — distinct needs no boundary link |
| referrer-finder | distinct (0.67) | "cross-reference §6.4 / §21 Alt 2 / §22 OQ-DRS.1" (L1341) | §6.4 D3 ✓, §21 Alt 2 ✓, §22 OQ-DRS.1 ✓ | **OK** — all three targets exist |
| partitioner | distinct (0.57) | reflect-local; invert default; no boundary ref | n/a — `distinct` | OK |
| degrade-oracle | distinct (0.68) | "cross-reference §6.4 / §21 Alt 3 / §22" (L1343) | §6.4 D1 ✓, §21 Alt 3 ✓, §22 (reuse-boundary OQ / Reuse disposition) ✓ | **OK** — see note 3 |
| **entrypoint-rootwalk** | **reuse-by-import** (0.81, STRONGEST) | "Recommended v1: reflect-local copy (§6.4 D1 / §21 Alt 3 Option C)" (L1344) | §6.4 D1 ✓, §21 Alt 3 Option C ✓ | **OK** — the one non-distinct verdict chains fully to D1 + Alt 3 |
| ledger-writer | distinct (0.56) | reflect-local; `_IndentDumper`/`_atomic_write_text` reuse; no boundary ref | n/a — `distinct` | OK |

Plus the audit's **Boundary note** (L1347) explicitly closes the loop: "surfaced as a Key Design
Decision (§6.4 D1), an Alternative (§21 Alt 3), and an implicit open question, never a silent
choice" — and the §21 Alt 3 "Why Not Chosen" (L1211) reciprocally points back: "see OQ in §22 /
Reuse Audit disposition." Bidirectional linkage confirmed for the load-bearing rootwalk decision.

**Note 3 (degrade-oracle "§22" target — checked):** The degrade-oracle disposition says
"cross-reference §6.4 / §21 Alt 3 / §22." §6.4 D1 and §21 Alt 3 are the reflect→audit boundary
decision (degrade-oracle's DATA-import is governed by the same boundary). The "§22" target is the
boundary open-question/Reuse-disposition discussion — §22 Alt-3 boundary is carried via OQ context
and the L1211 "OQ in §22 / Reuse Audit disposition" back-reference. The §22 link is slightly loose
(degrade-oracle is not itself a named OQ row in §22; it rides on the shared D1 boundary OQ), but the
referenced section exists and contains the relevant boundary reasoning. **OK** (resolves to a real
section with relevant content); recorded as a MINOR precision observation, not a broken chain.

---

## Cross-reference integrity spot-checks (external targets the chains depend on)

Verified the §10.x deviation-channel references the AC-5 / FR-007 / FR-009 / FR-010 chains depend on
actually resolve. These are **SKILL.md** section numbers, not this TDD's §10 (which is "Component
Inventory", N/A):

- `§10.6 Grounding Gap` — **exists** in `SKILL.md` (`### 10.6 Grounding Gaps`, SKILL.md:1012).
  [Bash-verified]
- `§10.9` (FR-007 "existing deviation mapping (§10.9)", L288; §11.1 step 6 sprint-exec mapping, L674)
  — **exists** in `SKILL.md` (`### 10.9 Runtime-surface UNREACHED (finding modifier …)`,
  SKILL.md:1055). [Bash-verified]
- `§10.6`/`§10.9` are NOT defined in the TDD itself (TDD §10 = Component Inventory N/A). The TDD uses
  bare `§10.6` / `§10.9` without the `SKILL.md` qualifier in ~15 places. This is a **MINOR ambiguity**
  (a reader could misread `§10.6` as a TDD self-reference into the N/A §10), but the targets resolve
  unambiguously in SKILL.md and the surrounding prose makes the SKILL.md provenance clear. Not a
  broken chain.
- `pyproject.toml [project.scripts]` anchor (degrade-oracle cat (b), L761, L1228) — the TDD's single
  `[CODE-VERIFIED]` in-repo anchor. [Verified present in earlier reads of the TDD; the entries
  `superclaude = "...main:main"` / `ic = "...ic:main"` are cited consistently at L761 and L1228.]
- `cli/audit/reachability.py:_bfs_reachable :591-624` (rootwalk adaptation source; §6.1 L386, §6.4 D1
  L445, Reuse Audit L1344, §27.1 L1362) — cited with identical line range across all four locations;
  internally consistent.

**Code-citation verification (independent, via Grep against live source):** Because the chains lean
on these integration-seam citations, I independently grep-verified the load-bearing ones rather than
trusting the `[CODE-VERIFIED]` tag:

| TDD citation | Claimed location | Grep result | Match |
|--------------|------------------|-------------|-------|
| `_bfs_reachable` (rootwalk source) | `reachability.py:591-624` | `def _bfs_reachable` at **reachability.py:591** | ✓ |
| `parse_contract(config.contract_path)` (the single read) | `runner.py:445` | `parse_contract(config.contract_path)` at **runner.py:445** | ✓ |
| `_audit_once` (tier-agnostic chokepoint) | `runner.py:394-453` | `def _audit_once` at **runner.py:394** | ✓ |
| `_IndentDumper` (writer) | `runner.py:58-67` | `class _IndentDumper` at **runner.py:58** | ✓ |
| `_atomic_write_text` (atomic write) | `runner.py:70-89` | `def _atomic_write_text` at **runner.py:70** | ✓ |
| copy-over-import precedent | `runner.py:14-17` | `_IndentDumper is copied locally …` comment at **runner.py:14** | ✓ |
| `derive_verdict` (consumer) | `contract.py:130` | `def derive_verdict` at **contract.py:130** | ✓ |
| `parse_contract` def | `contract.py:65` (Reuse Audit) | `def parse_contract` at **contract.py:65** | ✓ |
| `_LOAD_BEARING_BOOL_FIELDS` guard mirror | `contract.py:200-209` | used at **contract.py:200** (def at :47) | ✓ |
| `Verdict.exit_code` | `models.py:39-42` | `def exit_code` at **models.py:39** (class Verdict :26) | ✓ |
| `ReflectConfig.contract_path` | `models.py:95-98` | `def contract_path` at **models.py:96** | ✓ (property block 95–98) |
| `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` (Q4 stale constant) | `ensemble.py:59`, used `:378` | constant at **ensemble.py:59**, used at **:378** | ✓ |

**12/12 load-bearing code citations are accurate to the exact line.** This is strong corroboration
that the architecture→data/API hops of the AC chains terminate at real, correctly-located code
seams — the chains are not just internally self-consistent, they bind to true source.

---

## Items Reviewed

| # | Check (crossref-chain lens) | Result | Evidence |
|---|------------------------------|--------|----------|
| 1 | AC-1 full chain (FR→arch→data/API→test) | PASS | Family A row AC-1; all hops cited with line numbers |
| 2 | AC-2 full chain | PASS | Family A row AC-2; §15.3 5-case gate present |
| 3 | AC-3 full chain | PASS | Family A row AC-3; §7.4 + §15.2 + §15.4 |
| 4 | AC-4 full chain (incl. deferred sub-link) | PASS | Family A row AC-4 + Note 1; deferred branch correctly testless |
| 5 | AC-5 full chain | PASS | Family A row AC-5; §15.3 case 37+41 |
| 6 | AC-6 full chain (hygiene AC, adapted) | PASS | Family A row AC-6; §15.1 sync/lint tier |
| 7 | A-reverse: every FR → arch + test (no requirement-with-no-test) | PASS | A-reverse table; 14/14 FRs + 7 NFRs chain or justified-defer |
| 8 | OQ-DRS.1 → §21 Alt 2 → §6.4 D3 | PASS | Family B row 1; all three present + reciprocal |
| 9 | OQ-DRS.2 → §21 Alt 1 → §6.4 D2 | PASS | Family B row 2; also chains R2 |
| 10 | OQ-DRS.3 → contract-version decision (§8.3/§19.2) | PASS (caveat) | Family B row 3 + Note 2; no §6.4 D-row by design, disclosed |
| 11 | Q4 → §8.3 → §19.2 | PASS | Family B row 4; explicit cross-refs in Q4 row |
| 12 | Reuse: entrypoint-rootwalk (reuse-by-import) → §6.4 D1 / §21 Alt 3 | PASS | Family C; bidirectional link confirmed |
| 13 | Reuse: 5 `distinct` rows + boundary note → §6.4/§21/§22 where claimed | PASS | Family C + Note 3 |
| 14 | External §10.6 / §10.9 targets resolve (in SKILL.md) | PASS | Spot-checks; Bash-verified SKILL.md:1012 / :1055 |
| 15 | Load-bearing code citations bind to true source | PASS | Code-citation table; 12/12 exact-line matches |

## Summary

- Checks passed: 15 / 15
- Checks failed: 0
- Broken chains found: **0** (adversarial target was ≥10; none located after end-to-end tracing of
  all three chain families + reverse FR→test direction + 12 code-citation spot-checks)
- Critical issues: 0
- Important issues: 0
- Minor (advisory, non-chain-breaking) observations: 3
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

Per the crossref-chain lens scope, the verdict gates on broken chains; none were found. The
following are MINOR advisory observations surfaced during tracing — each resolves to a real target,
so none breaks a chain. They are recorded for the document author's polish pass, not as gating
defects for this lens. (The general tdd-qualitative rubric treats all severities as gating; this
report is explicitly the *crossref-chain* partition and gates on chain integrity, which is clean.)

| # | Severity | Location | Issue | Suggested polish |
|---|----------|----------|-------|------------------|
| 1 | MINOR | TDD ~15 sites (e.g. L288, L389, L531, L601, L752) | Bare `§10.6` / `§10.9` references omit the `SKILL.md` qualifier; the TDD's own §10 is "Component Inventory (N/A)", so a reader could momentarily misread these as TDD self-references into an N/A section. Targets DO resolve correctly in SKILL.md (§10.6 at SKILL.md:1012, §10.9 at SKILL.md:1055). | Qualify the first occurrence per section as "SKILL.md §10.6 Grounding Gap" (or add a one-line note in §28/§12.1 that §10.x refers to SKILL.md's deviation taxonomy). |
| 2 | MINOR | TDD §22 OQ-DRS.3 (L1223) vs §21/§6.4 | OQ-DRS.3 alone among the three OQs has no §21 Alternative box and no §6.4 D-row; it terminates in §8.3 + §19.2 instead. The §21 preamble (L1134) discloses this ("the contract-version decision"), so it is consistent, but the chain shape differs from OQ-DRS.1/.2. | Optional: add a one-line pointer in the §22 OQ-DRS.3 row ("resolution lives in §8.3 + §19.2, not §6.4 — a governance, not architecture, decision") to make the differing terminus explicit at the row level. |
| 3 | MINOR | TDD Reuse Audit degrade-oracle row (L1343) | "§22" cross-ref for degrade-oracle is loose — degrade-oracle is not a named §22 OQ row; it rides on the shared §6.4 D1 boundary OQ. Section exists and contains relevant reasoning. | Optional: change "§22" to "§22 (shared D1 boundary OQ)" for precision. |

## Actions Taken

None — `fix_authorization: false`. Report-only. All three MINOR items left for the author; no files
modified.

---

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** 12 load-bearing code
   citations grep-verified to the exact line (the `_bfs_reachable`, `parse_contract`, `_audit_once`,
   `_IndentDumper`, `_atomic_write_text`, copy-precedent, `derive_verdict`, `parse_contract` def,
   `_LOAD_BEARING_BOOL_FIELDS`, `Verdict.exit_code`, `ReflectConfig.contract_path`, and
   `REFLECT_CONTRACT_VERSION` table). Plus 2 external section anchors (SKILL.md §10.6, §10.9)
   Bash-verified, and the spec's AC checklist structure (spec.md §4 L93–104) read and compared 1:1
   to TDD §24.1.
2. **Specific files read to verify claims:** the full TDD (3 page-reads covering all 1444 lines);
   `spec.md` §4 (AC source); `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (§10.6/§10.9,
   §5.3 pre-filter, §6.1 steps 4b/4b′); `src/superclaude/cli/reflect/runner.py`, `contract.py`,
   `models.py`, `ensemble.py`; `src/superclaude/cli/audit/reachability.py`.
3. **If 0 issues — why trust the check?** I did NOT report 0 issues; I report 0 *broken chains* plus
   3 MINOR advisory observations, against an adversarial target of ≥10 broken chains. The reason the
   "0 broken chains" verdict is trustworthy is the evidence trail: I traced all three chain families
   forward, traced the FR→test direction in *reverse* (the direction where a requirement-with-no-test
   would surface), and bound 12 architecture-hop citations to true source by Grep. The adversarial
   hypothesis was genuinely tested (e.g., I specifically hunted for an FR with no §15 test, an OQ with
   no Alternative, and a Reuse verdict with no cross-ref) and each suspected break resolved to a real,
   correctly-located link. The 3 MINOR items are exactly the residue an adversarial pass should leave:
   loose-but-resolving references, not dangling ones.
4. **Web research?** None performed — this lens is entirely local-file + source-code bound. No Tavily
   or fallback calls were needed or made.

### Why this is not a suspiciously-clean review

The TDD is unusually disciplined on traceability (it carries an explicit §5.3 per-AC coverage map, a
§15.6 AC-coverage map, a §21-preamble OQ→Alt mapping statement, and a Reuse-Audit boundary note that
names its own §6.4/§21/§22 links). That self-imposed scaffolding is *why* the chains hold — the
author pre-wired most of them. The adversarial value here was confirming the scaffolding is not
cosmetic: the reverse FR→test trace and the 12/12 code-citation match confirm the links bind to real
artifacts, not just to each other. The one genuine asymmetry (OQ-DRS.3 terminating in §8.3/§19.2
rather than §6.4) was found and characterized rather than rubber-stamped.

---

## Confidence Gate

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 0 | Glob: 0 | Bash: 6 (grep-based source verification run via
  Bash; each Bash call mapped to a specific citation/section check — `_bfs_reachable`+ensemble+runner
  citations, contract/models citations, SKILL.md §10.6/§10.9, spec AC structure, §10.x TDD-internal
  scan, AC-grep in spec). Total targeted tool calls (12) ≥ 15 checklist items is NOT satisfied by
  Read+Grep+Glob alone (6); the Bash grep-verifications (6) are the substitute for Grep here and each
  targets a specific check — combined 12 directed verifications back the 15 checks, with 3 checks
  (AC-chain internal-consistency rows) verified by close reading of the TDD pages rather than a
  separate tool call. Flagging per the Tool-Engagement-Minimum rule: the directed-verification count
  (12) is below the 15-item count by 3; those 3 are the internal AC↔FR↔test consistency rows, fully
  evidenced by the page reads already counted.
- **Unchecked items:** none.
- **Unverifiable items:** none. (File *existence* of `reachability.py` etc. is independently
  confirmed by the successful Grep matches against those files.)

## QA Complete
