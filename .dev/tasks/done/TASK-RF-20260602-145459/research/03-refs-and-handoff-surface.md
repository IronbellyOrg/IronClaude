# Research 03 — Refs files + Wave-6 handoff surface + inline contract

Status: Complete
Date: 2026-06-02
Track: Implement 4 Medium-Complexity Serena Adoptions (FR-RV3-MED.1–4)
Spec: `.dev/releases/current/Reflect-V3.5-Serena_Mediums/05-spec-medium-complexity.md` (§4.2 + §5 read)
Scope: `src/superclaude/skills/sc-reflect-protocol/refs/*.md` and SKILL.md §9

All citations are `file:line` against files read this turn. Worktree-relative source root:
`src/superclaude/skills/sc-reflect-protocol/`. Unverifiable spec claims tagged `[UNVERIFIED]`;
contradictions tagged `[CODE-CONTRADICTED]`.

---

## 0. OQ-M8 RESOLUTION — Contract is INLINE in SKILL.md §9 (return-contract.yaml ABSENT)

**CONFIRMED.** `refs/return-contract.yaml` does **NOT** exist. The full refs/ directory listing
holds exactly 11 files, none named `return-contract.yaml`:
`cost-profile.yaml, coverage-mapping.md, deviation-taxonomy.md, grader-extensions.md,
input-resolution.md, ops-integration.md, promotion-adapters.md, reflection-rubric.md,
remediation-handoff.md, report-template.md, reviewer-spec.md`.

The contract lives **inline in `SKILL.md` §9** ("Output Contract (Versioned)"):

- `SKILL.md:487` — `## 9. Output Contract (Versioned)`
- `SKILL.md:489` — "Two-block contract: stable + telemetry. Written to
  `<output>/return-contract.yaml` AND returned inline." (Note: `<output>/return-contract.yaml`
  is a **per-run artifact path**, not a ref source file — this is the only place the string
  `return-contract.yaml` appears, and it is the runtime output, confirming there is no committed
  `refs/return-contract.yaml`.)
- `SKILL.md:491` — `### 9.1 Stable contract (contract_version: 1.0)`
- `SKILL.md:601` — `### 9.2 Telemetry (non-stable)`

**Impact on the builder:** spec §4.2 lists
`refs/return-contract.yaml (if present — see OQ-M6)` as a candidate modified file. It is NOT
present. **ALL §5 contract additions and the `contract_version` bump edit SKILL.md §9.1/§9.2
directly — there is no YAML file to touch.** The §4.2 row for `return-contract.yaml` is
therefore a no-op; the SKILL.md §6.1/§9/§10.4/§14/§4.0/§4.1 row is where the contract work lands.

### §9.1 stable block boundary (exact)

The §9.1 stable YAML block is a single fenced block:

- **Opens** at `SKILL.md:493` (```` ```yaml ````), first field `contract_version: "1.0"` at
  `SKILL.md:494`.
- **Closes** at `SKILL.md:597` (```` ``` ````); the last field is `promotion_pending: bool`
  (`SKILL.md:596`).
- `SKILL.md:599` — "Each flag has a one-line semantics description in
  `refs/report-template.md`. Contract version is `v1.0`." (This is the second place the version
  string must bump to `1.1.0`/`1.2.0` per OQ-M6 — line 491 heading AND line 599 prose.)

**Sub-block anchors inside §9.1 for the new fields (spec §4.5 data model):**

- `# UC-1 specific` block — `SKILL.md:503-507` (ends at `best_practice_grade`). FR-1's
  `hierarchy_slice_path` + `hierarchy_coverage_pct` add here.
- `# UC-2 specific` block — `SKILL.md:509-517`. FR-4's `verification_ran`,
  `verification_invocations`, `verification_failures`, `verification_regressions_detected`,
  `verification_skip_reason` add here.
- `# Asymmetric-cost flags` block — `SKILL.md:555-562`. `regression_present: bool` already
  exists at **`SKILL.md:557`** (spec §4.5 correctly calls this an EXISTING field; FR-4 only
  changes its *source* to verified, no schema change).
- `# Tier 3` block — `SKILL.md:550-553` (`remediation_offered`/`remediation_accepted`/
  `task_file_path`). FR-3's `handoff_memory_key` adds here (spec §4.5 labels it "§9.1 Tier 3
  block" — matches).

### §9.2 telemetry block boundary (exact)

- **Opens** at `SKILL.md:603` (```` ```yaml ````), first field `wave_durations_ms` at
  `SKILL.md:604`.
- **Closes** at `SKILL.md:618` (```` ``` ````); last field `memory_misses: <int>`
  (`SKILL.md:617`).
- Existing `degraded_components: [<list>]` at `SKILL.md:610` (the fail-open token sink —
  FR-1 `type_hierarchy:backend_error` and FR-4 `execute_shell_command` skip tokens land here per
  spec §5 "Fail-open `degraded_components` tokens").

All FR-1/2/3/4 `_invoked`/`_ran`/status/`hierarchy_*`/`onboarding_*`/`handoff_*`/`verify_*`
telemetry fields (spec §4.5 §9.2 block) add inside `SKILL.md:603-618`, **no contract bump**
(spec §5: telemetry is non-contractual per §9.4).

---

## 1. refs/remediation-handoff.md (FR-3) — Wave-6 handoff surface (FULL READ)

File: `refs/remediation-handoff.md`, 138 lines. This is the **concrete integration target for
FR-3** (`prepare_for_new_conversation` / `reflect/handoff-{slug}-{timestamp}`). Full structure:

| Section | Lines | What it owns |
|---|---|---|
| Loader/gating preamble | `:1-5` | Loaded by Wave 6 only when `--remediate` set AND ≥1 remediable deviation; "Reflect itself never fixes code" |
| `## BUILD_REQUEST template` | `:7-83` | The verbatim prompt reflect constructs + spawns `rf-task-builder` via Skill invocation |
| `## Opt-in prompt` | `:85-104` | yes/no operator prompt shown BEFORE invoking task-builder (no auto-execute) |
| `## Default-remediation guidance per deviation class` | `:106-117` | Table deciding whether Wave 6 even reaches the opt-in prompt |
| `## Field-by-field mapping from reflect contract to BUILD_REQUEST` | `:119-138` | Maps each BUILD_REQUEST field to its §9.1 contract source |

### Existing Wave 6 BUILD_REQUEST chain (the thing FR-3 must warm-start)

The chain is: **Wave 5 produces deviation register/report → Wave 6 short-circuit check
(`:117`) → opt-in prompt (`:89-104`) → construct BUILD_REQUEST (`:11-83`) → spawn
`rf-task-builder` (`subagent_type: "rf-task-builder", mode: "bypassPermissions"`, `:13-15`).**

The BUILD_REQUEST `RESEARCH DIR` field (`:62-70`) points task-builder at reflect's own artifacts:
```
RESEARCH DIR: <output>/reflect/<run_id>/
  # - report.md            (Wave 5 synthesized report)
  # - deviation-register.md (per-item classification)
  # - grounding-gaps.md    (known unverified claims)
  # - hypothesis-cards/    (root-cause-analyst cards)
  # - adversarial/merged.md (T2 only — reviewer verdict)
```
This is the cold-handoff today: task-builder re-derives context by **reading reflect's
output-dir artifacts** from disk. FR-3's `reflect/handoff-{slug}-{timestamp}` Serena memory is a
*warm* alternative/supplement to this dir read — it carries the rubric scores + deviation set +
evidence packet as a memory blob so the next conversation resumes warm rather than re-reading
(spec FR-RV3-MED.3 description; spec §2 third bullet).

### WHERE FR-3's three sub-mechanisms land (precise insertion points)

1. **`reflect/handoff-{slug}-{timestamp}` memory schema + write.** FR-3 says write it "at Wave
   5/6, immediately BEFORE the task-builder handoff." In this ref that is **before `:13`** (the
   `Agent: subagent_type: "rf-task-builder"` spawn). Recommended insertion: a NEW section
   between `## Opt-in prompt` (`:85-104`) and `## Default-remediation guidance` (`:106`), OR a
   new subsection at the head of `## BUILD_REQUEST template` (after `:9`, before the prompt
   fence at `:11`), titled e.g. `## Tier-3 warm-start handoff memory (FR-3)`. The memory key is
   `reflect/handoff-{slug}-{timestamp}` and its payload = rubric scores + deviation set +
   evidence packet + reviewer verdicts (spec FR-3 description).
   - **NEW BUILD_REQUEST field needed:** add a `HANDOFF_MEMORY_KEY: reflect/handoff-{slug}-{ts}`
     line to the prompt template (`:11-83`) and a matching row to the field-by-field mapping
     table (`:119-138`, after the `RESEARCH DIR` row at `:134`), so task-builder is told the key
     to `read_memory` for warm start. This is the concrete "pass its key to task-builder" wiring
     from spec FR-3.1/FR-3.3.

2. **`prepare_for_new_conversation` invocation.** Invoked at the write point above. Because the
   tool **signature is unverified (OQ-M1)**, the ref must say "probe the live MCP surface before
   parameter-dependent wiring" (spec FR-3.6). Emits `handoff_memory_written: true` +
   `handoff_memory_key: ...` to audit.log BEFORE the `:13` spawn (spec FR-3.1).

3. **`write_memory` fallback.** When `prepare_for_new_conversation` is context-excluded
   (default in `ide-assistant`/`claude-code`), fall back to `mcp__serena__write_memory` with an
   inline-built summary blob, emit `handoff_persist_method: write_memory_fallback`, still hand the
   key to task-builder (spec FR-3.3). The spec says this **extends the existing SKILL.md:1067
   "Serena `write_memory` fails at Wave 5" error-matrix row** — so the fallback wiring is
   co-located in SKILL.md §14, and remediation-handoff.md only needs the *handoff-key
   propagation* + the `handoff_persist_*` audit fields. Both-fail path → `handoff_persist_failed:
   true`, surface findings WITHOUT the key, never block report (spec FR-3.4).

### FR-3 no-op / retention notes

- **FR-3.5 (no `--remediate`):** the ref already short-circuits Wave 6 entirely at `:117`
  ("emit 'No Tier 3 remediation warranted...'") and the loader preamble `:3` gates on
  `--remediate`. So `handoff_memory_key: null` falls out naturally — no handoff step runs. The
  builder need not add a guard; the existing gating already covers it. Document that the handoff
  write is nested INSIDE the existing `--remediate` + remediable-deviation gate.
- **FR-3.7 / M-ARC2 (retention):** the `reflect/handoff-*` prefix must be added to the
  low-spec FR-RV3-LOW.8 retention sweep. The sweep is NOT in remediation-handoff.md; the existing
  retention rule lives in `SKILL.md:383` ("keep last 20 entries per key; expire >90 days").
  remediation-handoff.md is NOT the place for the sweep edit — only a cross-reference note
  belongs here (the sweep prefix extension is a SKILL.md §6.3 / low-spec coordination item).

**[UNVERIFIED]** spec citation `02-matrix:194,369` ("largest research gap", `prepare_for_new_
conversation` signature) — `02-matrix-medium-complexity.md` was deleted from this branch (git
status shows `D .dev/releases/backlog/Reflect-V3-Serena/02-matrix-medium-complexity.md`); the
matrix line cites could not be re-verified here. The OQ-M1 runtime-probe requirement stands
regardless.

---

## 2. refs/reflection-rubric.md (FR-1, FR-4) — S_dev_density sub-terms

File: `refs/reflection-rubric.md`, 163 lines. Two relevant surfaces: the 5-dimension `C` score
(`:9-71`) and the **3 structural signals** (`:74-113`), of which `S_dev_density` is the FR-1/FR-4
target.

### How S_dev_density is currently defined

- `### S_dev_density` header at **`:102`**.
- **Definition (`:104`):** "For UC-2: `unmapped_diff_hunks / total_hunks`. For UC-1:
  `unmapped_spec_requirements / total_requirements`."
- **Range (`:106`):** Float `0.00-1.00`.
- **Threshold semantics (`:108-112`):** `≤ 0.05` strict T1 STOP eligible; `≤ 0.10` rule-2 path;
  `> 0.20` automatic ESCALATE (rule 5).

**Key finding:** S_dev_density today is a **single ratio with NO sub-terms** — it is purely
`unmapped/total`. The spec (§4.2 row 2, §5 "New rubric inputs") says to "Add `S_dev_density`
sub-terms: hierarchy-gap count (FR-1), verification-failure weight (FR-4)." There is currently
**no sub-term structure to extend** — the builder must INTRODUCE a sub-term decomposition under
`### S_dev_density` (`:102-112`). This is additive structure, not an edit to an existing list.

**IMPORTANT cross-ref:** the *actual computation* of `S_dev_density` is NOT in
reflection-rubric.md — it is in **`refs/coverage-mapping.md`** (`## S_dev_density calculation`,
see §7 below). reflection-rubric.md defines the *threshold semantics*; coverage-mapping.md
defines the *formula*. **FR-1/FR-4 sub-terms touch BOTH files** — the spec §4.2 list omits
coverage-mapping.md (gap flagged in §7).

### WHERE FR-1 hierarchy-gap term + FR-4 verification-failure weight add

- **FR-1 hierarchy-gap term** → new sub-term under `### S_dev_density` (`:102`). Defined by
  FR-1's `hierarchy_gaps_found` telemetry (spec FR-1.2) and `hierarchy_coverage_pct =
  registered_subtypes / total_subtypes_in_hierarchy` (spec FR-1.3). A type whose transitive
  subtype family is under-registered raises structural ambiguity → feeds S_dev_density upward.
  Recommended: add a "Sub-terms (V3-Serena medium)" block after the Definition line `:104`.
- **FR-4 verification-failure weight** → same sub-term block. Driven by
  `verification_failures` / `verification_regressions_detected` (spec §4.5). A verified test
  failure on a claimed-passing hunk is the strongest unmapped-confidence signal. Note: per the
  spec exit-code taxonomy, `ruff`/`mypy` exit-1 feeds `S_dev_density` ONLY (NOT
  `regression_present`) — so the verification-failure *weight* here is specifically the
  lint/type-finding channel, distinct from the Regression channel that goes to §10.4.

### Caveat: deviation-category vocabulary mismatch (NOT a contradiction, but builder must note)

reflection-rubric.md dimension 3 (`:38-46`) names the deviation categories
`{Aligned, Refinement, Drift, Regression}` (`:39`), whereas deviation-taxonomy.md and SKILL.md
§10 use `{Authorized, Necessary, Drift, Regression}`. This is a pre-existing vocabulary skew in
the rubric ref, **independent of this spec** — flagging so the builder does not "fix" it as part
of FR-1/FR-4 (out of scope; would be drift). Tag: pre-existing, not introduced by FR-RV3-MED.

---

## 3. refs/deviation-taxonomy.md (FR-4) — Regression-class signals

File: `refs/deviation-taxonomy.md`, 121 lines. The Regression class is at `## Regression`
(`:69-81`).

### How Regression-class signals are currently listed

- `## Regression` header at **`:69`**; Definition `:71`.
- **Detection signals (`:73-78`):**
  - `:75` — diff hunk contradicts spec acceptance criterion (textual/behavioral via
    `get_diagnostics_for_file`).
  - **`:77`** — "A test that previously passed now fails after the diff **(detect via task log
    or by re-running tests if `--rerun-tests` set)**." ← THE OPT-IN PATH FR-4 SUBSUMES.
  - `:78` — documented invariant / `@invariant` comment violated.
- **Gold-standard reference (`:79`):** "test-suite state pre/post (**from task log or re-run**)".
- **Default remediation (`:81`):** unconditional Tier 3 + unconditional Tier-2 escalation
  (§5.3 rule 3).

**Mirror in SKILL.md §10.4:** identical text at `SKILL.md:725` ("detect via task log or by
re-running tests if `--rerun-tests` set") and `SKILL.md:728` gold-standard. The spec §4.2
SKILL.md row says "§10.4: replace opt-in `--rerun-tests` with default-on verification feeding
`verification_regressions_detected`." So **both `refs/deviation-taxonomy.md:77,79` AND
`SKILL.md:725,728` must be edited in lockstep** — they are duplicated prose.

### WHERE FR-4's exit-code→deviation-class taxonomy / verification_regressions_detected slot in

The spec §4.2 row for deviation-taxonomy.md: "Note `verification_regressions_detected` as the
deterministic §10.4 Regression signal (FR-4)." Precise edits:

1. **Replace the opt-in signal at `:77`** — change "(detect via task log or by re-running tests
   if `--rerun-tests` set)" → default-on verification: a non-zero exit classified Regression by
   the exit-code taxonomy sets `verification_regressions_detected += 1` → `regression_present:
   true`.
2. **Add `verification_regressions_detected` as a named deterministic detection signal** under
   `## Regression` (`:73-78`) — it is the verified-source signal, distinct from the textual /
   diagnostics signals.
3. **Embed (or cross-reference) the exit-code → deviation-class taxonomy** (spec §3 FR-4 table,
   "C2"): `pytest` 1 → Regression; `pytest` 2/3/124 → Grounding Gap (§10.6); `pytest` 5 → Drift
   (§10.3); `ruff`/`mypy` 1 → `S_dev_density` only. This taxonomy spans FOUR taxonomy sections
   (Regression `:69`, Drift `:56-67`, the §10.6 Grounding Gap parallel artifact `:97-120`, and
   the rubric's `S_dev_density`). Recommended: add a new subsection (e.g.
   `## Verification exit-code → deviation-class mapping (FR-4)`) AFTER `## Classification
   precedence` (`:83-95`) and BEFORE `## Grounding-gaps parallel artifact` (`:97`), because it
   touches all four classes and naturally reads after the precedence rules.

**Precedence interaction:** the existing `## Classification precedence` (`:83-95`,
Regression > Drift > Necessary > Authorized) must be respected — the spec exit-5→Drift mapping
is explicitly "respects §10.5 precedence by evidence, not by assignment" (spec FR-4 table note).
The new exit-code table assigns by *evidence* (which class the exit code signals), then
precedence resolves multi-signal collisions. The builder must NOT let exit-code assignment
bypass the precedence union rule (`:95`).

---

## 4. refs/reviewer-spec.md (FR-1, FR-4) — Wave-3 step 3B.0 per-reviewer brief grounding

File: `refs/reviewer-spec.md`, 95 lines. The Wave-3 step 3B.0 brief package is at
`## Brief template` (`:9-56`).

### The step 3B.0 brief grounding structure today

- **Step 3B.0** materializes one brief per reviewer at `<output>/reviewer-briefs/reviewer-<N>.md`
  (`:11-17`).
- A brief MUST contain **exactly three sections, in this order** (`:23-24`):
  1. **`## T1 card excerpt`** (`:26-30`) — persona-relevant slice of the T1 reflection card.
  2. **`## Grounding hunks`** (`:32-37`) — the GROUNDING SECTION. `file:line` excerpts from
     Wave 1A's grounding pass; H2 heading + one H3 per hunk, each H3 = `file:line-range` ref with
     a language-tagged fenced code block (`:35`). "Each hunk preserves the `file:line` ref so the
     `evidence-validator` agent can re-Read it at the Wave 5 final gate" (`:37`).
  3. **`## Coverage slice`** (`:39-52`) — coverage-matrix rows this reviewer owns.
- **Contract emission (`:54-56`):** on 3B.0 completion, emit
  `reviewer_briefs_materialized: <N>`.

### WHERE FR-1 hierarchy slice + FR-4 verification results add

Spec §4.2: "Add hierarchy slice (FR-1) + verification results (FR-4) to the Wave 3 step 3B.0
per-reviewer brief grounding section (SKILL.md:245)." The "grounding section" = `## Grounding
hunks` (`:32-37`). Two options the builder must choose between:

- **Option A (extend `## Grounding hunks`):** add the FR-1 hierarchy-slice excerpt and FR-4
  verification-result excerpt as additional grounding hunks under `## Grounding hunks` (`:32`).
  Pro: keeps the "exactly three sections" invariant (`:23`). Con: hierarchy/verify outputs are
  not `file:line` source excerpts (the H3-per-hunk shape at `:35` assumes source ranges) — a
  `<output>/artifacts/hierarchy-slice.yaml` ref (FR-1 contract `hierarchy_slice_path`) and a
  `<output>/verify-logs/invocations.yaml` ref (FR-4 `evidence_ref`) are artifact paths, not
  source lines.
- **Option B (new brief subsection):** add a fourth optional section, which **breaks the
  "exactly three sections" invariant** at `:23-24` — the builder would then also need to update
  that invariant line. Higher blast radius.

**Recommendation for the builder:** Option A, adding hierarchy/verify as grounding-hunk entries
that carry the artifact-path ref (`hierarchy-slice.yaml` / `verify-logs/invocations.yaml`) so the
evidence-validator can still re-Read them at Wave 5 (`:37` requires the ref be preserved). This
keeps the three-section invariant intact. The FR-1 slice is per-reviewer-persona-filtered (the
`analyzer`/`architect` reviewer gets the hierarchy slice; `qa` gets verify results) consistent
with the existing persona-filtering rule (`:33` "filtered to those the reviewer's persona will
actually cite").

**Note:** the SKILL.md:245 anchor cited by the spec is the §4.3 Wave 3 detail (`SKILL.md:243`
`### 4.3 Wave 3 — Detailed step addition`); reviewer-spec.md is the ref it points to (cross-ref
at `SKILL.md:420` "See `refs/reviewer-spec.md`..."). Both surfaces are in scope: the brief
*template* lives in reviewer-spec.md, the wave-step *wiring* in SKILL.md §4.3.

---

## 5. refs/ops-integration.md (FR-2, FR-4) — operator WARN-message catalog

File: `refs/ops-integration.md`, 210 lines.

### CODE-CONTRADICTED: there is NO general "operator WARN-message catalog" today

The spec §4.2 row says "Add the FR-2/FR-4 operator WARN-message catalog entries (context-excluded,
read-only-disabled, mutation-denied)." **There is no section titled "WARN catalog" or any
generalized operator-WARN registry in ops-integration.md.** The only WARN body present is the
**single-purpose Vendor-heterogeneity WARN** (`## Vendor-heterogeneity WARN`, `:86-116`), which
provides one templated operator-facing message body (`:103-114`) for the §4.0 step 0.6 vendor
check. Tag: **[CODE-CONTRADICTED]** — the "catalog" the spec presumes does not yet exist as a
structure; the builder must CREATE the catalog section, using the existing Vendor-heterogeneity
WARN (`:103-116`) as the established format/precedent.

The document's stated scope (`:5-12`) lists six things it owns; "operator WARN catalog" is not
among them — only "the vendor-heterogeneity WARN body referenced by §4.0 step 0.6" (`:10`). So
the builder is genuinely ADDING a new responsibility to this ref.

### WHERE the FR-2 / FR-4 WARN entries go

Recommended: a NEW section (e.g. `## Serena-adoption operator WARN catalog (V3-Serena medium)`)
inserted AFTER `## Vendor-heterogeneity WARN` (`:86-116`) and BEFORE `## Metrics ingestion
config` (`:118`) — so all operator-facing WARN bodies are co-located, following the established
`[reflect][WARN] ...` body format from `:106-114`. Entries the spec enumerates:

- **FR-4 `read-only-disabled`** — spec FR-4.7: WARN "verification triangle disabled by Serena
  `read_only: true`; verdict will degrade to LSP-only signals" + `verification_skip_reason:
  read-only-project`.
- **FR-4 `context-excluded`** — spec FR-4.4: tool excluded from active context →
  `verification_ran: false` + `verification_skip_reason: tool-unavailable` + Grounding Gap;
  loud-never-silent (spec G-2).
- **FR-4 `mutation-denied`** — spec FR-4.5: command matching the no-mutation denylist
  (`git commit|push`, `pip install`, `rm`, repo-path redirects) → `verify_blocked_reason:
  "mutation-denied"`, never invoked.
- **FR-4 `metachar-denied`** — spec FR-4.2b / NFR-8 (C1): any shell control char
  (`; | & $ \` > < newline ( )`) → `verify_blocked_reason: "metachar-denied"`. (Spec §4.2 row
  lists only context-excluded/read-only/mutation-denied, but the metachar-denied WARN is implied
  by FR-4.2b — builder should include it for completeness.)
- **FR-2 onboarding `context-excluded`** — spec FR-2.3: `--onboard` set but tool excluded →
  `onboarding_ran: false`, `onboarding_skipped_reason: "context-excluded"`, WARN telling the
  operator to switch context, NEVER a hard STOP.
- **FR-2 onboarding `budget-exceeded`** — spec NFR-7 (M-CMP1): `onboarding_budget_exceeded: true`
  WARN when onboarding breaches the §15 T1 band hard-kill at 1.25×. (Not in the §4.2 row text but
  required by NFR-7; builder should include.)

The existing WARN body format precedent to follow (`:106-114`): a `[reflect][WARN] <title>`
header line, indented context lines (resolved state, suggested override), and a mandatory
disclaimer line. The catalog entries should each name: the trigger condition, the emitted
`*_skip_reason` / `*_blocked_reason` field, and the loud-never-silent posture.

---

## 6. Other refs the spec §4.2 MISSED but a FR actually touches

The spec §4.2 Modified Files list does NOT include these two refs, yet FR-1/FR-4 functionally
require edits to them. Builder should add them to scope.

### 6a. refs/coverage-mapping.md — MISSED, FR-1 + FR-4 (S_dev_density formula owner)

File: `refs/coverage-mapping.md`, 7250 bytes. This ref **owns the actual `S_dev_density`
computation** that reflection-rubric.md only thresholds:

- `:5-7` — produces `coverage matrix`, `coverage_pct`, `unmapped_requirements`, AND "derives the
  `S_dev_density` structural signal consumed by the §5.3 tier-decision rubric."
- `## S_dev_density calculation` at **`:89`** with the formulas:
  `:95` UC-1 `S_dev_density = unmapped_requirements_count / total_requirements_count`;
  `:97` UC-2 `S_dev_density = unmapped_diff_hunks_count / total_diff_hunks_count`.
- `## Compute summary fields` at `:32`: `coverage_pct = matched_count / total_count` (`:32`).

**Why it's in scope:** FR-1's `hierarchy_coverage_pct = registered_subtypes /
total_subtypes_in_hierarchy` (spec FR-1.3) is a coverage ratio that parallels this file's
`coverage_pct` formula, and FR-1/FR-4's `S_dev_density` SUB-TERMS (spec §5 "New rubric inputs")
modify the very formula at `:95,:97`. reflection-rubric.md (§2 above) defines the threshold;
**coverage-mapping.md defines the math** — the sub-term decomposition must land here too, or the
formula and the threshold-doc diverge. **Recommend: add coverage-mapping.md to §4.2.**

### 6b. refs/grader-extensions.md — MISSED, FR-4 (eval-assertion owner)

File: `refs/grader-extensions.md`, 16301 bytes. Owns the `grader.py` assertion types for
sc-reflect eval cases (`:3-5`). The §8.1 eval cases (`serena-verify-exitcodes`,
`serena-verify-injection`, `serena-execute-verify`) assert on contract/audit fields that need
these assertion types:

- `:19` row 7 — `deviation_class_matches` (report register vs annotated fixture) → directly
  validates FR-4.3 exit-code → deviation-class taxonomy.
- `:110-131` — `yaml_list_contains` (canonical example: `deviation-ledger.yaml` field
  `deviations[*].deviation_class` contains `regression`) → validates FR-4
  `verification_regressions_detected` → Regression promotion-block.
- `:89,:94-101` — `regex_absent` for "false-clean-pass detection" (assert a regression-laden
  report does NOT contain `verdict: clean_pass`) → validates the FR-4 false-PASS closure.

**Why it's in scope:** the FR-4 eval cases (spec §8.1) cannot assert exit-code taxonomy or
regression promotion-block without new/extended grader assertions (e.g. an audit-row assertion
for `verify_blocked_reason: metachar-denied` zero-invocation, and a `verification_regressions_
detected ≥ 1` yaml assertion). The "9 truly-new types" header (`:3`) would need a 10th/11th for
the verification-injection (`metachar-denied` zero-invocation) and exit-code-taxonomy cases.
**Recommend: add grader-extensions.md to §4.2** (or note eval-authoring will extend it
downstream — but the assertion-type contract is a build-time decision, not eval-author-time).

> Coverage note: the spec partially anticipates this — §10 "For sc:tasklist" defers OQ-M9 (full
> exit-code table) to eval-authoring. But the *grader assertion type* needed to TEST the table is
> a grader-extensions.md addition, distinct from the table itself.

---

## 7. FR → ref-file edit map (summary for the builder)

| FR | SKILL.md (inline) | refs/ files to edit | New WHERE |
|----|-------------------|---------------------|-----------|
| **FR-1** `type_hierarchy` | §6.1 step 4.5 (after `:362`); §4.1 Wave 1B.3 (`:227-241`); §9.1 UC-1 block (`:503-507`) + §9.2 telemetry (`:603-618`); frontmatter `allowed-tools` | `reflection-rubric.md` S_dev_density sub-term (`:102`); `reviewer-spec.md` `## Grounding hunks` (`:32`); **`coverage-mapping.md` `:89-97` (MISSED)** | hierarchy-gap sub-term; hierarchy slice in brief; `hierarchy_coverage_pct` formula |
| **FR-2** `onboarding` | §4.0 step 0.7b (after `:134`/in §4.0 `:172-225`); §9.2 telemetry (`:603-618`) | `ops-integration.md` NEW WARN catalog (after `:116`) | onboarding context-excluded + budget-exceeded WARNs |
| **FR-3** `prepare_for_new_conversation` | §6.3/Wave 6 handoff; §14 row extends `:1067` (`write_memory` fallback); §9.1 Tier 3 block (`:550-553`) + §9.2 (`:603-618`) | **`remediation-handoff.md`** NEW handoff-memory section + `HANDOFF_MEMORY_KEY` BUILD_REQUEST field (`:11-83`) + mapping-table row (after `:134`) | handoff write BEFORE `:13` spawn; key propagation to task-builder |
| **FR-4** `execute_shell_command` | §6.1 step 5.5 (after `:363`); §10.4 `:725,:728` (replace opt-in); §14.5.2 cond-4 consumes (`:1097`); §9.1 UC-2 block (`:509-517`) + §9.2 (`:603-618`); frontmatter | `deviation-taxonomy.md` `:77,:79` + new exit-code section (after `:95`); `reflection-rubric.md` verify-weight sub-term (`:102`); `reviewer-spec.md` `## Grounding hunks` (`:32`); `ops-integration.md` WARN catalog (after `:116`); **`grader-extensions.md` (MISSED)** | exit-code→class taxonomy; verify-failure weight; verify results in brief; 4 WARN entries; new grader assertions |

**Inline-contract confirmation (OQ-M8):** no `refs/return-contract.yaml` edit anywhere — every
contract field add is a SKILL.md §9.1 (`:493-597`) or §9.2 (`:603-618`) inline edit. The §4.2
`return-contract.yaml` row is a confirmed no-op.

**Duplicated-prose lockstep edits the builder must not miss:**
- §10.4 Regression detection text is DUPLICATED in `deviation-taxonomy.md:77,79` AND
  `SKILL.md:725,728` — both must change together (FR-4).
- `S_dev_density` is split across `reflection-rubric.md:102-112` (threshold) AND
  `coverage-mapping.md:89-97` (formula) — both must change together (FR-1/FR-4).

---

## Status: Complete

All six in-scope refs read (`remediation-handoff.md`, `reflection-rubric.md`,
`deviation-taxonomy.md`, `reviewer-spec.md`, `ops-integration.md`) plus the two MISSED refs
(`coverage-mapping.md`, `grader-extensions.md`) and SKILL.md §9.1/§9.2, §6.1, §10.4, §14.5.2, §7.

Key resolutions:
1. **OQ-M8 RESOLVED:** `refs/return-contract.yaml` is ABSENT; contract is inline in SKILL.md
   §9.1 (`:491-599`, YAML fence `:493-597`) and §9.2 (`:601-618`, YAML fence `:603-618`). All §5
   contract additions edit SKILL.md directly.
2. **FR-3 surface mapped:** `remediation-handoff.md` Wave-6 BUILD_REQUEST chain (`:7-83`,
   spawn at `:13`); handoff-memory write lands BEFORE the spawn; new `HANDOFF_MEMORY_KEY` field +
   mapping-table row needed; `write_memory` fallback co-located in SKILL.md §14 (`:1067`).
3. **Two refs MISSED by spec §4.2:** `coverage-mapping.md` (S_dev_density formula owner, FR-1/4)
   and `grader-extensions.md` (FR-4 eval assertions). Recommend adding both to §4.2.
4. **[CODE-CONTRADICTED]:** ops-integration.md has no general WARN catalog — only the single
   Vendor-heterogeneity WARN (`:86-116`); the builder must CREATE the catalog section.
5. **Pre-existing skew (do not fix):** reflection-rubric.md dim-3 uses
   `{Aligned, Refinement, Drift, Regression}` (`:39`) vs taxonomy's
   `{Authorized, Necessary, Drift, Regression}` — out of scope for FR-RV3-MED.
