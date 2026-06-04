# /sc:reflect UC-1 Pre-Execution Audit — REVISED Proposal (Re-Verification Pass 2)

**Mode:** UC-1 (pre-execution coverage / gap / best-practice audit)
**Target:** `.dev/proposals/reflect-in-task-builder.md` (revised, dated 2026-06-04)
**Driving spec:** R1–R4 (embedded in prompt) + 4 revision-round acceptance criteria
**Grounded against:** `src/superclaude/skills/task-builder/SKILL.md` (2190 lines), `src/superclaude/commands/reflect.md`, `src/superclaude/skills/sc-reflect-protocol/{SKILL.md,refs/}`
**Date:** 2026-06-04
**Verdict:** **PARTIAL** (close to PASS — no design-level gaps; residual issues are wiring-accuracy defects in the TCS extraction rules and one contract field-name error, all fixable in-place before implementation)

---

## 1. Per-requirement coverage (R1–R4)

### R1 — PRE gate `/sc:reflect --mode pre --remediate` after tasklist creation → **COVERED**

- New step **A.10.7** inserted between A.10.5 (qualitative gate) and A.11 (present results). Insertion point verified: A.10.5 ends at SKILL.md:1194, A.11 begins at SKILL.md:1398 — the gap is real and the placement is valid (proposal §6.1).
- Invokes `--mode pre --remediate` (proposal §6.1 step 2). Both flags exist on the real surface: `--mode pre` (reflect.md:68), `--remediate` (reflect.md:89).
- Authority model is **advisory-blocking with sign-off** (Decision A3), which correctly honors `feedback_human_decision_items_must_halt.md` — the gate annotates + surfaces a remediation offer but never auto-mutates the tasklist. Additive-only Edit to `## Open Questions` (proposal §6.1 step 4).
- `reflect_pre` frontmatter sign-off block defined (proposal §6.1 step 5). Frontmatter is the correct home — SKILL.md:1866-1885 confirms the generated frontmatter is freely extensible (`related_docs`, `tags`, etc. already present).
- Loop policy = **0 auto-loops** (§6.1 step 6) — correctly avoids the unattended-mutation failure mode.

**One wiring defect (see §3, R1-D1):** §6.1 step 3 says reflect returns `missing_requirements` and step 4 appends `missing_requirements`. The real UC-1 contract field is **`unmapped_requirements`** (reflect SKILL.md:653, 822-823). `missing_requirements` does not exist as a contract field. Design intent is unaffected; the field name must be corrected before implementation.

### R2 — generated tasklist's LAST task is `/sc:reflect --mode post --remediate`, fresh session → **COVERED**

- POST gate is templated as the **penultimate** final-phase item (immediately before `Update task status to Done`), preserving anti-orphaning. Verified against the real structure: the Done item is `N.X` at the final phase (SKILL.md:1928-1935) and "Task completion items inside final phase (anti-orphaning)" is an enforced validation criterion (SKILL.md:1969). Placing reflect as `N.(X-1)` is structurally compatible.
- Note: the driving spec says "VERY LAST task." The proposal makes reflect the *penultimate* item with the status-to-Done item last, because anti-orphaning **requires** the Done item to be terminal. This is a correct, necessary reconciliation of two constraints — not a gap. The proposal is explicit about it (§6.2 + §2.2).
- Fresh-session, executor-disjoint handoff (Decision B3): writes a `reflect_post: PENDING` sentinel and surfaces a paste-ready command for the operator to run in a NEW session — honoring `feedback_sc_reflect_vs_inline_rfqa.md` (the load-bearing independence is executor-disjoint reviewer classes). The item HALTs (does not self-resolve) per `feedback_human_decision_items_must_halt.md`.
- Emitted deterministically via a new Critical Rule companion to #16, reusing the verified QA-gate-emission machinery (Rule #16 at SKILL.md:2030 with its "MALFORMED if omitted" guard pattern). The proposal correctly mirrors that MALFORMED pattern for the new rule.
- Uses `/sc:reflect` for the gate and `/task` (never `/sc:task`) for execution — honors `feedback-no-sctask-on-task-builder-tasklists.md` (proposal §6.2 + §2.4).

### R3 — `--spec` used with `--mode pre` IF a spec is known → **COVERED**

- Decision C2 (best-effort capture + graceful degrade): spec path resolved at A.2 in priority order (explicit `--spec` → `@file` in GOAL → `SPEC:`/`PRD:`/`TDD:` BUILD_REQUEST field → none). Threaded into the PRE `--spec` and the POST item `{SPEC_PATH}` placeholder (proposal §6.3).
- Correctly handles the absent-spec case: UC-1 hard-STOPs without `--spec` (verified: reflect.md:32, input-resolution.md:57). The proposal degrades to `reflect_pre: {verdict: skipped, reason: no-spec}` rather than deadlocking — the right call, since C1 (require spec) would block the common natural-language-goal path.
- `--spec` and `--tasklist` both exist on the real surface (reflect.md:72-73).

### R4 — `depth` invoked in BOTH instances, deterministic where possible → **COVERED (design) / PARTIAL (extraction-rule accuracy)**

- Depth derived for both gates from one Tasklist Complexity Score (TCS); PRE carries raw TCS-derived depth, POST carries `max(tcs-derived, standard)` (proposal §5.5). Both gates invoke `--depth`. ✓
- `--depth quick|standard|deep` maps to T1-only / T1-then-rubric / force-T2 — verified accurate (reflect.md:78; input-resolution.md:16; reflect SKILL.md:73, 361).
- The TCS is **pure arithmetic over 7 integer signals** with fixed weights and thresholds — genuinely deterministic at the arithmetic level. Inference is bounded to a ±4-TCS window around each band edge (§5.4), which is honest about S2's ×4 leverage.
- Cost rationale verified: T1 ≈ 3-8k Claude tokens, T2 ≈ 35-70k (cost-profile.yaml:38-39, 50-51). The "deep is ~10× quick" cost driver behind a conservative formula is real.

**Two extraction-rule accuracy defects (see §3, R4-D1 and R4-D2):** S5 and S7's frozen extraction rules cite tokens/markers that **do not exist** in the generated MDTM output. This does not break the determinism *claim* (the arithmetic is still deterministic), but it means those signals will compute to 0 on every real tasklist, silently under-counting complexity. Must be fixed before implementation or the formula is partially inert.

---

## 2. Revision-round acceptance criteria (the 4 specific fixes)

### AC-1 — `--executor-model` ONLY on POST, NEVER on PRE → **LANDED**

- §6.1 step 2 is explicit: *"No `--executor-model` is passed at PRE — in `--mode pre` no executor has run, so excluding an executor class is a category error (the audit's G2)."*
- POST item carries `--executor-model {EXECUTOR_CLASS}` (§6.2 templated command, line 215) — correct, since an executor has run by then.
- Verified the underlying mechanic: `--executor-model` is an *exclusion* flag (removes the executor's class from the reviewer pool), not a model-selector (reviewer-spec.md:72-76). The proposal describes it correctly in §6.4.
- **Internally consistent.** Searched the whole proposal: `--executor-model` appears only in PRE-prohibition context and POST templated command + §6.4 explanation. No PRE occurrence.

### AC-2 — POST depth FLOORED at `standard` (POST ∈ {standard, deep}, never quick) → **LANDED**

- O4 (§5.3) is a HARD RULE: "POST gate depth ∈ {standard, deep} — it may NEVER be quick." Restated in §5.5 (`max(tcs-derived, standard)`), in the BUILD_REQUEST `DEPTH: <max(tcs-derived depth, standard)>` (§6.2), and in the templated command's `{DEPTH}` note (line 218).
- O4's rationale is **verified correct**: `--depth quick` = "STOP at T1" (reflect SKILL.md:361), which disables the Wave 3+ regression-escalation rubric — exactly the blindspot class the POST gate audits. Flooring at `standard` (T1-then-rubric) preserves escalation. The premise is grounded, not assumed.
- Consistent across all four mention sites. No `quick` POST path anywhere.

### AC-3 — Determinism claims honest; per-signal extraction rules frozen OR "byte-reproducible" downgraded → **LANDED**

- Each signal S1–S7 now carries a **Frozen Extraction Rule (FER)** column (§5.1 table). The prior unqualified "byte-reproducible" claim is gone — §5.4 now says **"deterministic given the frozen FERs"** and **"deterministic at both the input and arithmetic levels."** Searched the proposal: zero occurrences of "byte-reproducible" / "byte-reproducibility." The downgrade landed.
- S2's residual interpretive judgement is explicitly scoped to the ±4-TCS window with an auditable `tcs_boundary_inference` record (§5.4). This is the honest framing the AC asked for.
- **Caveat:** the FERs are *specified* (satisfying the AC literally), but two of them (S5, S7) reference non-existent tokens — see §3. So the claim "two implementers compute the same integer" holds (both get 0), but the integer is wrong. The honesty criterion is met; the *correctness* of two FERs is not. This is why the overall verdict is PARTIAL, not PASS.

### AC-4 — Zero residual `--reflectagent` / "sonnet default" / model-routing references → **LANDED**

- Grep of the proposal for `reflectagent`, `sonnet default`, `sonnet-by-default`, model-routing: the only matches are **explicit negations** — §1 line 21 ("introduces no model-routing flag and no 'sonnet-by-default' override"), §6 line 6, §6.4 ("No model-routing flag is introduced"), §8 step 3 ("No reflect-side model-routing flag is introduced; spawned reflect agents use the default subagent model").
- No `--reflectagent` flag anywhere. No routing machinery in exec summary, tables, decisions, or open questions. The deliberate-removal decision is correctly reflected as absence-by-design.
- Per the prompt's explicit instruction, this absence is CORRECT and is not flagged as a gap.

---

## 3. Residual gaps (must close before implementation)

### R1-D1 — Contract field-name error: `missing_requirements` → should be `unmapped_requirements` (LOW severity, certain)

- **Where:** proposal §6.1 step 3 ("Consume the reflect return contract (`status`, `coverage_pct`, `missing_requirements`, `run_id`)") and step 4 ("append `missing_requirements` to the tasklist's `## Open Questions`").
- **Reality:** the UC-1 contract has no `missing_requirements` field. The field is **`unmapped_requirements: [<list>]`** (reflect SKILL.md:653; confirmed as the consumer-facing field at SKILL.md:822-823 for the `sc:roadmap` and `sc:tasklist` gates). A separate field `missing_implementations` exists but is the FR-1 abstract-implementation field, not the coverage-gap list.
- **Impact:** A literal implementation would read a non-existent key and append an empty/undefined list to Open Questions. Pure rename fix.
- **Fix:** replace both occurrences of `missing_requirements` with `unmapped_requirements`.

### R4-D1 — S5 frozen extraction rule references a non-existent token (MEDIUM severity, certain)

- **Where:** §5.1 S5 = "Count items carrying the `needs_human_decision` flag / Open-Question-blocked items (TB-Add-3, SKILL.md:1974)."
- **Reality:** `grep "needs_human_decision"` against `task-builder/SKILL.md` returns **zero matches**. Generated MDTM items carry no `needs_human_decision` flag. TB-Add-3 (SKILL.md:1168, 1974) actually means *"each blocked item references its blocking Open Question by index in Context"* — i.e., the deterministic signal is a **Context-line reference to an `## Open Questions` entry**, not a `needs_human_decision` flag.
- **Impact:** S5 (weight ×5, the highest) will compute to 0 on every real tasklist, defeating override O1 ("any S5 > 0 ⇒ floor standard"), which exists specifically to honor `feedback_human_decision_items_must_halt.md`. The single most important complexity/halt signal is inert as written.
- **Fix:** re-anchor the S5 FER to the actual observable: count final-phase/blocked items whose **Context** field cites an `## Open Questions` index (the TB-Add-3 pattern), and/or count non-empty `## Open Questions` entries in the tasklist. (`## Open Questions` is a real, verified section — SKILL.md:1058, 1423, 1767.)

### R4-D2 — S7 frozen extraction rule cites the wrong literal marker (LOW-MEDIUM severity, certain)

- **Where:** §5.1 S7 = "Count phases containing the literal marker `spawn in SAME message` / parallel markers (SKILL.md:1963)."
- **Reality (two problems):** (a) The exact string `spawn in SAME message` does not appear; the real literal is **`spawned in the SAME message`** / **`in the SAME message`** (SKILL.md:418, 485) and `"spawn in SAME message"` only appears as a *table-cell description* at SKILL.md:1991, not as a marker in generated tasklists. (b) More fundamentally, lines 418/485/1991 are **task-builder's own research-phase orchestration instructions**, NOT content emitted into the generated MDTM file. A generated tasklist will not contain "SAME message" markers unless the builder is separately instructed to emit parallel-wave markers — which is not established.
- **Impact:** S7 (weight ×2) likely computes to 0 on generated tasklists; the "concurrency raises integration surface" signal is inert. Lower impact than S5 (lower weight, and concurrency is partially captured by S1/S2 breadth).
- **Fix:** either (a) re-anchor S7 to a marker the builder actually emits into the MDTM file (verify what parallel/wave markers, if any, appear in generated items — none was found in this audit), or (b) drop S7 and redistribute, documenting that generated tasklists do not currently carry machine-detectable concurrency markers.

### R4-D3 — S6 FER partially grounded; `tags` set is plausible but unverified in generated output (LOW severity, likely)

- **Where:** §5.1 S6 = count items with `type: 🔧 Refactor` OR a `tags:` value in `{security, risk, regression, breaking-change}`.
- **Reality:** `type: 🔧 Refactor` is real (frontmatter, SKILL.md:1870) — but it is a **single frontmatter field per tasklist**, not a per-item attribute, so "count items whose metadata carries `type: 🔧 Refactor`" is at most 0-or-1 per file, not a per-item count. The `tags:` values `{security, risk, regression, breaking-change}` are a *proposed* fixed set; no evidence the builder emits these specific tags into generated items (the frontmatter `tags` are placeholders `[tag1]/[tag2]` at SKILL.md:1882-1884). Override O2 ("any S6 > 0 ⇒ force deep") therefore rests on tags that may never be emitted.
- **Impact:** O2's regression-class force-to-deep could rarely fire. Medium-importance because O2 is the safety override for risk surfaces.
- **Fix:** clarify S6 as a file-level (not per-item) check on `type: 🔧 Refactor`, and either (a) confirm/establish that the builder emits the risk tag-set into generated items, or (b) anchor S6 to the BUILD_REQUEST `TESTING_REQUIREMENTS`/risk fields that the builder demonstrably consumes.

### R4-D4 — S1/S2 file-path regex excludes fenced code blocks but MDTM items embed paths in prose fields (LOW severity, possible)

- **Where:** §5.1 S1 regex applied "excluding fenced code blocks."
- **Observation:** the verified B2 item shape (SKILL.md:1916-1921) puts file paths in **Action/Output/Verification prose**, often as inline code spans or bare paths — generally not inside triple-fenced blocks, so the exclusion is probably safe. But some generated items DO use fenced command blocks (e.g., test commands) that legitimately contain paths the audit cares about. Excluding all fenced blocks may under-count S1/S2.
- **Impact:** minor under-count of breadth signals. Not a blocker; flag for FER tuning against the past-TASK-RF corpus the proposal itself recommends (§7 risk 3).
- **Fix:** during calibration, measure S1 with vs without the fenced-block exclusion on real tasklists and pick the variant that tracks true file breadth.

---

## 4. Depth-formula arithmetic sanity check

`TCS = 3·S1 + 4·S2 + 2·S3 + 2·S4 + 5·S5 + 4·S6 + 2·S7` (§5.2). Bands: ≤12 quick / 13–34 standard / ≥35 deep (§5.3).

- **Weights ↔ formula consistency:** the §5.1 weight column (×3/×4/×2/×2/×5/×4/×2) matches the §5.2 coefficients exactly, in S1..S7 order. ✓
- **Band boundaries are contiguous and non-overlapping:** ≤12, 13–34, ≥35. No gap, no overlap. ✓ (The exec-summary/§7 mention "12/34" as the anchors, consistent with the table's ≤12 and 13–34 upper edge of 34. Minor: §7 risk 3 says "thresholds (12/34)" — consistent.)
- **±4 boundary windows (§5.4):** "8–16 around the 12 edge, 31–39 around the 35 edge." Check: 12±4 = 8–16 ✓; 35±4 = 31–39 ✓. Arithmetic correct.
- **Override interaction sanity:**
  - O1 (S5>0 ⇒ floor standard): with S5 weight ×5, a single human-decision item adds ≥5 to TCS — could still land in the quick band (≤12) if all else is tiny, so O1's explicit floor is genuinely needed, not redundant. ✓ logically sound (but inert until R4-D1 is fixed).
  - O2 (S6>0 ⇒ force deep): a single risk item (×4) cannot alone reach 35, so O2's hard force is needed, not redundant. ✓ (sound, but contingent on R4-D3 fix).
  - O3 (item-count >40/>50 ⇒ floor standard): independent of TCS, references real TB-Add-2 bounds (track ≤40 / single ≤50, SKILL.md:1973). ✓ accurate.
  - O4 (POST floor standard): precedence over band stated; consistent with `max(tcs-derived, standard)` in §5.5. ✓
- **Override precedence:** O2 (force deep) > O4 (floor standard) > O1/O3 (floor standard) > band. The proposal states O2 "force deep" and O4 "floor standard" but does not give a single explicit total-order when O1+O2+O4 co-fire. In practice "force deep" dominates "floor standard" so the outcome is unambiguous (deep), but **a one-line precedence statement would remove all doubt** (minor; recommend adding).

**Arithmetic verdict:** the formula, weights, bands, and ±4 windows are internally consistent and correctly computed. The only formula-level weakness is that two inputs (S5, S7) are mis-anchored to non-existent tokens (§3) — the math is right, two of its operands are dead.

---

## 5. Best-practice compliance grade: 4/5

- **+** Honors all three constraining memories explicitly and correctly (executor-disjoint POST, halt-don't-mutate, no `/sc:task`).
- **+** Determinism downgrade is honest; ±4 inference window is well-scoped to S2's actual leverage.
- **+** Reuses verified existing machinery (Rule #16 emission, frontmatter extensibility, anti-orphaning placement) rather than inventing new surface.
- **+** Correctly excludes `--executor-model` from PRE (category-error awareness) and floors POST depth with a grounded rationale.
- **−** Three of seven TCS signal FERs (S5, S7, partially S6) are anchored to tokens/markers that do not exist in the real generated output — the FER table looks rigorous but is partially inert. This is the gap between "specified deterministically" and "specified correctly."
- **−** One contract field-name error (`missing_requirements`).

A 5/5 requires the FER re-anchoring (S5/S7/S6) and the field-name fix; nothing structural is missing.

---

## 6. Verdict: PARTIAL

The revised proposal is **design-complete and internally consistent** on all four driving requirements and **all four revision-round acceptance criteria landed**. There are **no design-level gaps** and no residual model-routing contamination. The deliberate removal of the 5th (`--reflectagent`/routing) requirement is correctly realized as absence-by-design and is not counted against it.

It is **PARTIAL rather than PASS** solely because of **wiring-accuracy defects** that a literal implementation would carry into broken behavior:

| ID | Severity | Fix | Blocks impl? |
|----|----------|-----|--------------|
| R1-D1 | LOW | `missing_requirements` → `unmapped_requirements` (2 sites) | Yes (reads dead key) |
| R4-D1 | MEDIUM | Re-anchor S5 FER to TB-Add-3 Open-Question-reference pattern (the `needs_human_decision` flag does not exist) | Yes (highest-weight signal inert; O1 never fires) |
| R4-D2 | LOW-MED | Re-anchor or drop S7 (`spawn in SAME message` is not emitted into generated tasklists) | Should fix (signal inert) |
| R4-D3 | LOW | Clarify S6 as file-level `type` check + verify risk-tag emission (O2 dependency) | Should fix |
| R4-D4 | LOW | Calibrate S1/S2 fenced-block exclusion against real corpus | No (tuning) |
| §4 precedence | TRIVIAL | Add one-line O2>O4>O1/O3>band total-order | No (clarity) |

**To reach PASS:** apply R1-D1, R4-D1, and R4-D2 (the three "Yes/Should-fix" rows). These are surgical edits to §5.1 and §6.1 — no design rework. Once the FER operands point at tokens that actually appear in generated MDTM files and the contract field name is corrected, the proposal is implementation-ready.

---

## 7. Grounding note (citations re-verified this pass)

All file:line citations below were Read/grepped during this audit, not carried from the proposal:

- task-builder pipeline A.10.5→A.11 gap: SKILL.md:1194, :1398 ✓
- Rule #16 + MALFORMED guard: SKILL.md:2030 ✓
- Anti-orphaning + Done item N.X: SKILL.md:1928-1935, :1969 ✓
- Frontmatter shape + `type: 🔧 Refactor`: SKILL.md:1866-1885 ✓
- TB-Add-2 bounds / TB-Add-3: SKILL.md:1973, :1168, :1974 ✓
- `needs_human_decision` absent: 0 grep matches in task-builder/SKILL.md ✓
- `SAME message` is research-orchestration not MDTM content: SKILL.md:418, 485, 1991 ✓
- `## Open Questions` real section: SKILL.md:1058, 1423, 1767 ✓
- reflect `--depth quick` = STOP at T1: reflect SKILL.md:361 (O4 premise) ✓
- reflect UC-1 requires `--spec` (STOP): reflect.md:32, input-resolution.md:57 ✓
- reflect contract field `unmapped_requirements` (not `missing_requirements`): reflect SKILL.md:653, 822-823 ✓
- `--executor-model` is exclusion not selector: reviewer-spec.md:72-76 ✓
- regression → unconditional T2: remediation-handoff.md:122 ✓
- cost bands T1 3-8k / T2 35-70k: cost-profile.yaml:38-39, 50-51 ✓
- proposal residual-grep: no `byte-reproducible`, no `--reflectagent`, no `sonnet default` except explicit negations ✓
