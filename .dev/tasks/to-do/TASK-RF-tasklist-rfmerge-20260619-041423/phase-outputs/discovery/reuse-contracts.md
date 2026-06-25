# Reuse-Contract Reference — task-builder SKILL.md (no-fork sources)

**Confirmed:** 2026-06-19 (Step 1.5). Source: `src/superclaude/skills/task-builder/SKILL.md` (2527 lines).
These are the VERBATIM contracts P1/P2/P3 must reuse byte-for-byte. Any fork is a HALT.
The em-dash `—` (U+2014, NOT a hyphen `-`) is preserved exactly where it appears.

---

## Contract 1 — DM-003 / DNSP Synthetic Finding Protocol (reused by P3)

**Heading (line 873):** `**DNSP Synthetic Finding Protocol (PR-03 - paradigm-neutral, the BASE proposal of this release):**`

**7 named emission fields (lines 877-883), verbatim:**

| Field | Value / rule |
|---|---|
| `severity` | fixed literal `HIGH` (case-sensitive; non-overridable; R-113) |
| `source` | fixed literal `"synthetic-dnsp"` (case-sensitive; non-overridable; R-114) |
| `affected_range` | the failed agent's `assigned_files` slice copied **verbatim, byte-for-byte** (no normalization/whitespace edits; R-115) |
| `evidence` | NEVER blank — canonical wire value is the spawn-log path; when unavailable substitute `<!-- evidence-absence: no-spawn-log: <reason> -->` stub citing the absence (R-116) |
| `recommendation` | fixed byte-exact literal `Manual review required — partition agent failed twice` (em-dash; case-sensitive; NO leading/trailing whitespace; NO suffix — the old `on this range` extension is REMOVED drift; R-117) |
| `dedup_key` | 2-element YAML list `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`; 2nd element MUST be from the closed vocab below (R-118) |
| `found_n_times` | int, default `1` on first emission; +1 per within-cycle dedup-key collapse (R-119) |

**Closed exhaust-point vocabulary (R-118/R-120):** `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`.
Free-form descriptions (e.g. `"second retry"`, `"gap-fill round 2"`) are REJECTED.

**Wire-shape (R-120/R-121):** emitted as a structured Markdown block in the agent's **normal output
stream** (same stdout/report channel real findings use) — NO sideband channel, NO out-of-band metadata.

**All-agents-fail guard (line 895 + R-122):** three mutually-exclusive paths gated on partition-cohort
success count BEFORE any emission:
- **Path A (zero succeeded):** existing fix-cycle escalation; **NO synthetic emits**.
- **Path B (≥1 success AND ≥1 exhaust):** synthetic-dnsp emits **ALONGSIDE** real findings (strictly additive, never replaces).
- **Path C (all succeeded):** no synthetic; normal merge.

**Merge semantics (R-127, line 911):** strictly additive (post-merge real count = pre-merge real count
+ synthetic count); HIGH non-overridable across merge; within-cycle collapse (R-123) before gate eval;
cross-cycle composition (R-124/INV-012) before the PR-02 monotonicity comparison; a present
synthetic-dnsp record causes **FAIL until manual review**; the gap-fill cycle MUST NOT auto-resolve it.

**Cross-cycle vs regression (R-124/line 1305):** a synthetic re-emitted with identical `dedup_key` on
cycle n+1 after appearing on cycle n is a **DEDUP case, NOT a regression** — contributes 1 (not 2) to
`|F_{n+1}|`; `dedup_key ∈ FAIL_n` implies `dedup_key ∉ PASS_n`, so it cannot trip regression.

### P3 task-side pins (from research/08 R-1, design note Step 1.6)
- Stage-7 exhaust-point is **`retry-1`** (single-retry ladder; no vocab extension).
- `dedup_key` shape on the tasklist side: `["<stage7_affected_range>", "retry-1"]`.
- `affected_range` re-bound to the Stage-7 2N fan-out unit (legitimate MAP, not a copy of the
  partition-cohort R-122/INV-021 machinery).

---

## Contract 2 — `## Execution Context` 3-subfield contract (reused by P1)

**Instruction (lines 1066-1069):**
- **References:** BUILD_REQUEST GOAL verbatim; WHY summary; related-doc IDs (R-001, R-002, ...)
- **Source areas:** named modules/packages identified in research — **NEVER specific file:line paths**
  (e.g., "rf-qa agent prompts", "task-builder skill body")
- **Key constraints:** top 1-3 invariants from QA_GATE/VALIDATION/TESTING requirements or research findings

**REQUIRED + degradation (line 1231):** "This section is REQUIRED in every task file (except GOAL-only
with no source areas, where it degrades to **References-only**). Do NOT include specific file:line paths
in the block header."

**TB-Add-7 (line 1389):** every `Source areas:` entry reappears in at least one item's Context field;
the block itself contains **NO specific file:line references**. INACTIVE if no Execution Context block exists.

**TB-Add-8 (line 1390):** per-item Context evidence binding — every item Context that references a code
surface carries a file:line citation OR an `<!-- evidence-absence: ... -->` comment (proves the
"no specific paths" rule is confined to the header; INV-015 scope-confinement).

### P1 task-side pins (research/08 R-2/R-4)
- Block attaches to the phase-file **TASK BODY** (Stage 4 compute / Stage 5 render), **NOT** index-level
  (do not conflate with P5).
- Reuse the EXACT sub-field names (References / Source areas / Key constraints); no renamed/forked variant.
- NO `Ensuring:` clause; Acceptance Criteria remains the single source of truth.
- Deterministic emission: emit IFF ≥1 resolvable roadmap ref (reuse the existing 4.1c resolve/None gate);
  Source areas listed when present else degrade to References-only; omit block when no ref resolves;
  same roadmap → same block; NEVER emit invented file paths.

---

## Contract 3 — PR-02 Retry Monotonicity (reused by P2)

**Heading (line 1263):** `**Retry Monotonicity Protocol (FR-CONV.5 / PR-02 -- strengthens zero-trust QA against oscillation):**`

**Byte-exact halt strings (lines 1282-1283), preserve em-dash:**
- Monotonicity halt: `[HALT-MONOTONICITY] |F|=<n>` — `<n>` = integer cardinality `|F_{n+1}|` at the cycle the guard fires.
- Regression halt: `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` — `X.Y` = regressed item id; `N` = prior-PASS cycle.

**Monotonicity guard (line 1267):** record `F_n` (count of remaining gate failures) at end of each cycle;
if `F_{n+1} >= F_n` (did NOT **strictly shrink**) HALT + emit monotonicity halt. Fires only on strict
non-shrink; `F_{n+1} = F_n - 1` (slow convergence) continues to the cap. Consulted only when `|F_n| > 0`
AND only after regression check passes.

**Regression detection (line 1268):** record the PASS set each cycle; if any item that PASSed at cycle n
is FAILing at n+1, HALT immediately + emit regression halt. Fires only on previously-PASS items.

**Precedence rule (line 1270):** regression detection ALWAYS runs BEFORE monotonicity; when both would
trigger, the regression halt is emitted and monotonicity is NOT consulted on the regressed item.

**4-step ordering rule (lines 1294-1303):** `regression → monotonicity → hard-cap → proceed`, run in this
exact order, EXIT on first match. Strict ordering invariant: regression exits before monotonicity;
monotonicity before hard-cap; hard-cap before proceed. Producers MUST NOT reorder/skip.

**F-set = post-dedup cardinality (line 1299):** the monotonicity check uses `|F_{n+1}|` cardinality **after dedup**.

**Independent counters (line 1261):** each counter keeps its own halt-precedence state — counters are
NEVER collapsed across gates.

### P2 task-side pins (research/08 R-8 + adversarial-validation.md:141 + OQ-PRE-1)
- Cap is **2 TOTAL passes** (k∈{2}, one re-patch pass), **NOT** task-builder's 3-cap.
- Re-run the **FULL Stage-7 2N validation set** each pass (not subset-only) so previously-PASS regressions
  are detectable.
- Loop fenced **before Stage 10.5** with a provable non-overlap predicate
  `set(P2_loop_findings) ∩ set(stage_10_5_reflect_pre_findings) == ∅`.
- **OQ-PRE-1 refinement:** `F_k` counts only **patchable (non-synthetic) findings** — exclude
  `source: "synthetic-dnsp"` records from the P2 monotonicity/regression comparison (a synthetic
  persists across cycles by design = DEDUP, not regression, per R-1 + INV-012). Fold into Phase 4/5
  design; add a Phase 5 test asserting a persistent synthetic does NOT trip the P2 monotonicity halt.
