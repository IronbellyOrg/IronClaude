# R3 — Reuse Surfaces (Exact reusable APIs/surfaces for sc:submit-pr)

**Status: Complete**

Researcher: R3 (Reuse Surfaces)
Spec: `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md`
Scope: What existing code `sc:submit-pr` REUSES — the severity rubric (C3 `severity-routing.md`),
the grounding/verification discipline (C3a `finding-verify.md`), and the `/sc:troubleshoot`
seeding/flag/severity-reuse contract (C3b `troubleshoot-dispatch.md`).

**Hard rule for the builder:** these are *reuse-by-reference* surfaces. C3/C3a/C3b refs must
**DEFER TO** the existing files (cite their path + section) and must NOT copy/restate/fork the
content. Drift between a copied rubric and the source rubric is exactly the failure these refs exist
to prevent.

---

## TARGET 1 — Severity rubric (C3 `severity-routing.md` DEFERS TO this)

### File
`src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md` (173 lines, full read)

### Reusable surface (the complete schema C3 must consume, not reinvent)

The rubric is the **single source** for severity grading. Spec FR-3.1 ("Re-grade via reused severity
rubric; Augment's self-reported severity is a hint, not authoritative") maps 1:1 onto this file's
opening contract: *"Auggie's `severity_hint` is a starting point, not authoritative … every finding
is remapped through this rubric so the report grades consistently"* (severity-rubric.md:3).

**(a) Five tiers — decision-term definitions** (severity-rubric.md:12-61):

| Tier | Decision meaning | Defining condition (abbrev.) |
|------|------------------|------------------------------|
| 🔴 Critical | Block merge | exploitable security / data-integrity / crash-on-default-path / compliance (lines 13-23) |
| 🟠 High | Should fix before merge | latent security / non-default-path correctness / resource leak / API-contract break / concurrency hazard / arch drift (lines 24-36) |
| 🟡 Medium | Fix if cheap, else follow-up | code-quality w/ consequences / perf trajectory / single anti-pattern / test gap off critical path / stale docs (lines 37-46) |
| 🟢 Low | Nice-to-have | real but cost>benefit / opportunistic / pre-existing-elsewhere (lines 48-53) |
| 💬 Nit | Style/naming/comments | naming/comments/style — **"Skip nits entirely if a linter/formatter … is configured and CI will catch them"** (lines 55-61) |

**(b) Severity-remap algorithm — the 5-step pipeline** (severity-rubric.md:63-101). This is the exact
function C3's `re-grade` must call. Steps:

1. Start from Augment's `severity_hint` (line 67).
2. **Category override table** (lines 70-87) — category is more reliable than the hint. Provides a
   `floor` and `ceiling` per category (`security`/`data-integrity`/`correctness`/`concurrency`/
   `resource-leak`/`api-contract`/`performance`/`architecture`/`layering`/`anti-pattern`/`dead-code`/
   `tests`/`docs`/`logging`/`naming`-`style`). E.g. `security (exploitable today)` floor = Critical;
   `naming/style` ceiling = Nit.
3. **Confidence adjustment** (lines 89-93): `low` → drop one tier; `medium`/`high` → no change.
   (Spec T-302 `severity_hint=critical` but `confidence=low` → downgrade to High is *exactly* this rule.)
4. **Diff-locality adjustment** (lines 93-96): `in_diff:false` AND pre-existing-untouched → drop one tier.
5. **Cross-source agreement bonus** (lines 97-100, `--depth deep` only): single-source → drop one tier
   unless category floor blocks.

**(c) Decision-mode summary** (severity-rubric.md:163-172): counts→recommendation map
(`critical>0` → Block merge; `critical==0 && high>0` → Request changes; …). C3 can reuse this verbatim
for its route-decision rollup. Note line 172: the recommendation does **NOT** translate to
`--approve`/`--request-changes` — this aligns with spec §1.3 non-goal (no merge-state mutation).

### How C3 (`severity-routing.md`) consumes it WITHOUT re-implementing
- C3's `re-grade` is a thin adapter: map Augment's emitted finding fields (`severity_hint`,
  `category`, `confidence`, `in_diff` — locus per `detection-contract.md`) into the rubric's input
  shape, then **apply the 5-step algorithm by reference** to `severity-rubric.md:63-101`. The ref
  text should read "apply the severity-remap algorithm defined in
  `sc-auggie-review-protocol/refs/severity-rubric.md` §Severity-remap algorithm" — not copy the table.
- The category→floor/ceiling table (lines 70-87) is the load-bearing reuse. T-301
  (`severity_hint=low` but category=security → Critical) is a direct test of the floor row.
- **Tier→troubleshoot routing is C3-OWNED, NOT in the rubric.** The rubric stops at producing a tier;
  the `{Medium→--fix, High/Critical→--depth deep --fix, Low/Nit→report-only}` map (FR-3.2) is
  `severity-routing.md` new logic. Keep that boundary crisp: rubric = grade; C3 = grade→tier→route.
- QD-6 "rubric tested independently": the rubric already ships calibration examples
  (severity-rubric.md:104-152, five worked cases). C6 tests for T-301/T-302 should assert against
  those same shapes so the reuse is provably faithful.

---

## TARGET 2 — Grounding / verification discipline (C3a `finding-verify.md` models on this)

This is the model for **verify-before-remediate** (FR-3.5): an external Augment finding must
independently ground in real code before a remediation round/push is spent. Three reuse sources:

### 2.1 The hallucination contract (the verbatim discipline to mirror)
**File:** `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:22`
> "Every finding emitted in the final report must cite a `file:line` that exists in the repo at the
> time of review. Findings that cannot be grounded are dropped, not downgraded."

`sc-troubleshoot-protocol/SKILL.md:24` states the identical contract. C3a's purity boundary (spec
NFR-6: no `gh`/`git` in the verify wave) matches this read-only posture.

### 2.2 The file:line validation pass (the concrete grounding procedure to reuse)
**File:** `sc-auggie-review-protocol/SKILL.md:198-213` (Wave 3, "Validate & Synthesize").
The reusable procedure is **step 3, "File:line validation pass (non-negotiable)"** (lines 206-209):

- For each finding, **`Read` the cited file at the cited line range**; confirm the line exists and
  (where possible) confirm the cited snippet actually appears on that line (line 207).
- For PR/diff mode, additionally confirm the line is within the diff hunks (line 208).
- For `needs-grounding` findings, attempt grounding via `mcp__auggie__codebase-retrieval` or `Grep`;
  promote on success, **drop and log** on failure (line 209).

This is precisely the **structural** half of FR-3.5. The spec distinguishes (FR-3.5 / EC-9): missing
`file:line` → *structural drop* (this Wave-3 procedure); location-exists-but-defect-doesn't-reproduce
→ *false-positive demote to report-only*. C3a reuses this Read-the-cited-line procedure as its
floor, then adds the reproduce-the-defect check on top.

### 2.3 The independent cross-check pattern (the model for "does the defect actually reproduce")
**File:** `sc-auggie-review-protocol/SKILL.md:183, 214-215`. `--depth deep` spawns the
`auggie-reviewer` agent via `Task` to run an **independent review pass that does not see Auggie's
findings yet** (line 183), then Wave 3 step 6 cross-checks: findings present in only one source are
marked `source: auggie-only | claude-only | both` (line 215). This independent-second-pass shape is
the model for C3a's parallel verification fan-out (FR-3.5 / T-342: "N findings → verification
dispatched in parallel, one batched message").

`sc-troubleshoot-protocol` reinforces this with two reusable evidence agents (both already in the
agent registry — see R1):
- **`evidence-validator`** (troubleshoot SKILL.md:409): spawned via `Task` with
  `report_draft_path`, `evidence_section_locator`, `output_path`, `allow_command_reexec=false`;
  "Reads every cited `file:line`, drops mismatches, returns the verified evidence set." This is the
  closest existing agent to what C3a needs — a read-only, citation-dropping validator. **C3a should
  reuse `evidence-validator` (Task-spawned) rather than write a new verifier agent.**
- **`confidence-calibrator`** (troubleshoot SKILL.md:260): re-grades a hypothesis card against a
  rubric "without the formation context (anchoring is reduced)." Same blind-regrade philosophy FR-3.1
  applies to severity.

### How C3a (`finding-verify.md`) consumes it WITHOUT re-implementing
- Reuse the **hallucination-contract wording** (SKILL.md:22) verbatim as C3a's governing rule.
- Reuse the **Wave-3 step-3 file:line validation procedure** (SKILL.md:206-209) as C3a's grounding
  floor; cite it, don't fork it.
- **Spawn the existing `evidence-validator` agent** (Task) for the read-only "cited line exists +
  snippet matches" check; layer the "defect reproduces" judgment on top (the delta FR-3.5 adds over
  EC-9's structural drop).
- Mirror the **independent-pass / cross-check** shape (SKILL.md:183/215) for the parallel fan-out and
  the `verified | unverified` verdict, where `unverified` → report-only, no round consumed.

---

## TARGET 3 — `/sc:troubleshoot` seeding/flag/severity-reuse contract (C3b `troubleshoot-dispatch.md`)

C3b dispatches **verified** findings to `/sc:troubleshoot`. R5 owns the Monitor/arming runtime; R3
owns the **seeding + flag + scope-passing contract**.

### 3.1 The real troubleshoot flag surface (authoritative — correct a spec mismatch)
**File:** `sc-troubleshoot-protocol/SKILL.md:103` (Wave 0 flag parse). Optional flags:
`--type`, `--depth`, `--fix`, `--no-escalate`, `--models`, `--output-dir`, `--no-mcp`,
`--no-diagnosability-audit`, `--diagnosability-handoff`, `--reset-diagnosability-rounds`.
`--depth` values: `quick | standard | deep` (SKILL.md:277-279). `--scope` is a required-input
alternative (SKILL.md:31).

**⚠️ BUILDER FLAG-CONTRACT FINDING (must be honored in C3b):**
- Spec FR-3.2 routes **Medium → `troubleshoot --fix`** and **High/Critical →
  `troubleshoot --depth deep --fix`**. The `--depth deep --fix` combo is **valid**.
- **BUT `--depth quick` + `--fix` is an explicit STOP/conflict** (`sc-troubleshoot-protocol/SKILL.md:131`:
  "conflicting flags (`--depth quick` with `--fix`)"). So C3b must **never** emit `--depth quick`
  alongside `--fix`. The spec's Medium route (`--fix` with no `--depth`) defaults to
  `--depth standard` (SKILL.md:279) — that is the safe form; do not "optimize" it to `--depth quick`.
- `--fix` only *authorizes* Tier 3; it does NOT auto-apply. `--fix` gates Wave 6, which requires
  **`REPORT.md` success (not partial) AND explicit user accept** (SKILL.md:439). C3b must not assume
  `--fix` means the fix lands unattended.

### 3.2 How a finding is seeded into troubleshoot (the reusable contract)
The spec's FR-3.3 ("Seed troubleshoot with finding body + file:line + evidence so troubleshoot does
not re-derive") maps onto troubleshoot's **Required Input** (SKILL.md:28-33): an *issue description*
(free text / error / stack trace) **and/or** a **`--scope`** (file, dir, or symbol). Wave 0 step 3
"Resolve `--scope` to a concrete path/symbol … narrow auggie/serena queries to that target"
(SKILL.md:112) and Wave 1 grounds the symptom in that scope (SKILL.md:144).

So the seeding contract C3b must produce per verified finding:
- **issue description** ← the Augment finding `body` + `recommendation` + `evidence` excerpt.
- **`--scope <file>`** (or `<file>:<symbol>`) ← the finding's grounded `file:line` (T-320 asserts the
  mock troubleshoot receives a `scope` containing the file:line from the finding).
- **`--type`** ← derivable from the rubric category (security/perf/test/etc.) so troubleshoot skips
  its own auto-detect (SKILL.md:104-111); optional but reduces re-derivation.
- **`--fix`** ← present for Medium+ routes per FR-3.2 (with the `--depth` rule in 3.1 above).

### 3.3 Severity→tier reuse boundary
Troubleshoot has its OWN tiering (Tier 1/2/3 via `refs/escalation-rubric.md`, SKILL.md:20). That is
**internal to troubleshoot** and distinct from C3's severity tier. The reuse contract:
- C3 grades severity (via Target-1 rubric) → routes to a `--depth` (`deep` for High/Critical).
- `--depth deep` then **forces troubleshoot's own Tier-2 escalation** (escalation-rubric.md:60-61:
  "`--depth deep` set → ESCALATE, `escalation_reason: forced_by_depth_deep`").
- So the High/Critical → `--depth deep` route is the *seam* where C3's severity hands off to
  troubleshoot's escalation. C3b does NOT reimplement troubleshoot's escalation rubric — it only
  chooses the `--depth` ordinal that drives it.

### 3.4 The Tier-3/task-builder handoff (reusable pattern, governs what troubleshoot does after fix)
**File:** `sc-troubleshoot-protocol/refs/remediation-handoff.md` (full read) + SKILL.md:437-448.
Wave 6 builds a `BUILD_REQUEST` (GOAL "Apply the fix described in `<REPORT.md path>`", WHY=Summary,
WHERE=cited files, TEMPLATE generic/complex by file count) and invokes `task-builder` via `Skill`
(remediation-handoff.md:38-66). Key reusable invariants C3b/§5 must respect:
- **Never auto-execute** the task file — `/task` is always user-initiated (remediation-handoff.md:78-92,
  SKILL.md:447). This aligns with the spec's autonomy-gate / `needs_human_decision` HALT discipline.
- Wave 6 only fires on a **`success` (not `partial`) report** (SKILL.md:439) — a useful precedent for
  the spec's "don't spend a round on a non-grounded finding."
- The auggie-review remediation-handoff
  (`sc-auggie-review-protocol/refs/remediation-handoff.md:1-194`) is the *longer* five-phase variant
  (design → task-builder → reflect-analyze → execute → reflect-validate) and its firing condition
  (`critical + high >= 1`, lines 11-13) is a direct analog to FR-3.2's High/Critical routing — useful
  reference if the builder wants the richer chain, but the troubleshoot variant is the leaner match
  for "dispatch a single verified finding."

### How C3b (`troubleshoot-dispatch.md`) consumes it WITHOUT re-implementing
- Treat `/sc:troubleshoot` as a black-box command with the **flag contract in 3.1**. C3b's job is to
  *construct the invocation string + scope/issue seed* (3.2), not to reach inside troubleshoot's waves.
- Honor the `--depth quick` × `--fix` conflict: emit `--fix` (Medium) or `--depth deep --fix`
  (High/Critical) — never `--depth quick --fix`.
- Let `--depth deep` be the lever that triggers troubleshoot's own Tier-2 (3.3); don't duplicate the
  escalation rubric.
- Inherit the **user-gated, never-auto-execute** Tier-3 discipline (3.4) — it dovetails with the
  spec's autonomy ceiling and `needs_human_decision` override (FR-4.4).

---

## Cross-target summary (for the builder)

| New ref | DEFERS TO (reuse-by-reference) | Exact surface | Do NOT |
|---------|-------------------------------|---------------|--------|
| C3 `severity-routing.md` | `sc-auggie-review-protocol/refs/severity-rubric.md` | 5-tier defs (12-61) + 5-step remap algorithm (63-101) + category floor/ceiling table (70-87) + decision-mode map (163-172) | copy the rubric; invent a new tier scheme; embed routing in the rubric |
| C3a `finding-verify.md` | `sc-auggie-review-protocol/SKILL.md` (hallucination contract :22, Wave-3 file:line pass :206-209, independent-pass :183/215) + `evidence-validator` agent (`troubleshoot SKILL.md:409`) | Read-cited-line grounding floor + spawn `evidence-validator` (Task, read-only) + parallel independent cross-check verdict `verified|unverified` | write a new verifier agent; mutate code (NFR-6 purity); conflate structural-drop (EC-9) with false-positive demote |
| C3b `troubleshoot-dispatch.md` | `sc-troubleshoot-protocol/SKILL.md` (flags :103/:131/:277-279, scope seed :31/:112/:144) + `refs/remediation-handoff.md` | invocation construction: issue=finding body+evidence, `--scope <file:line>`, `--type <category>`, `--fix` / `--depth deep --fix` | emit `--depth quick --fix` (STOP); reimplement troubleshoot's escalation rubric; auto-execute the Tier-3 task |

### Top builder warnings (load-bearing)
1. **Flag conflict:** `--depth quick` + `--fix` is a troubleshoot STOP condition
   (`sc-troubleshoot-protocol/SKILL.md:131`). C3b's Medium route = `--fix` (→ defaults to
   `--depth standard`); High/Critical = `--depth deep --fix`. Never `--depth quick --fix`.
2. **Rubric is grade-only:** tier→troubleshoot routing (FR-3.2) is NEW C3 logic, NOT in
   `severity-rubric.md`. Keep grade (reuse) and route (new) in separate sections.
3. **Reuse `evidence-validator`, don't author a new agent** for C3a's grounding floor
   (`troubleshoot SKILL.md:409` — already registered, read-only, citation-dropping).
4. **All three refs are reuse-by-reference:** cite source file + section; do not copy content
   (drift is the failure these refs prevent — matches the spec's whole verify-before-remediate thesis).

---

## Summary
C3 reuses the auggie-review **severity rubric** wholesale (5-step remap algorithm at
`severity-rubric.md:63-101`, category floor/ceiling at :70-87) and adds only the tier→troubleshoot
route map on top. C3a models **verify-before-remediate** on auggie-review's hallucination contract
(`SKILL.md:22`) + Wave-3 file:line validation pass (`SKILL.md:206-209`) + independent cross-check
(`:183/:215`), and should **spawn the existing `evidence-validator` agent** (`troubleshoot SKILL.md:409`)
rather than build a new verifier. C3b constructs `/sc:troubleshoot` invocations using the real flag
surface (`SKILL.md:103`) and scope-seed contract (`:31/:112/:144`), with the **critical caveat** that
`--depth quick` + `--fix` is a STOP condition (`:131`) — so Medium → `--fix` (standard), High/Critical
→ `--depth deep --fix`, never `--depth quick --fix`. All three new refs must DEFER TO their sources by
citation, never copy them.
