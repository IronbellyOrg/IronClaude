# Research: FX2/FX1 briefs

Status: Complete
Date: 2026-07-03
Researcher: R4 (Deep tier, task-builder)
Scope: 3 files (read fully) —
- `src/superclaude/agents/rf-qa-qualitative.md` (1143 lines)
- `src/superclaude/agents/reflect-reviewer.md` (133 lines)
- `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` (154 lines)

All paths below are relative to the worktree root
`/config/workspace/IronClaude/.dev/worktrees/pr209-harden/`.

---

## CRITICAL FRAMING CORRECTION (read first)

The task brief describes FX2 as *"rename/augment the mis-scoped `internal-consistency`
lens so it checks CODE function-to-function invariants… currently it only checks doc/CLI
string parity (blindspot B14)."*

**There is NO lens literally named `internal-consistency` in `rf-qa-qualitative.md`.**
The token `internal-consistency` (hyphenated, as a lens id) does not appear anywhere in the
file (verified by full read + grep). What actually exists are three *separate* structures
that carry the "internal consistency" idea, none of them a single renamable "lens":

1. **Verification Principle #3 "Internal consistency"** (rf-qa-qualitative.md:92) — a
   *document*-level principle (section-vs-section claims, numbers matching). This is the
   doc/string-parity flavor the brief calls "doc/CLI string parity."
2. **doc-qualitative checklist item 4 "Internal consistency"** (rf-qa-qualitative.md:755) —
   one-line fallback-phase check: "No contradictions between sections."
3. **task-qualitative "Code Compatibility" checklist group, items 4–6**
   (rf-qa-qualitative.md:671-676) — the *code*-level checks (signature / module / consumer).
   This is the group F1's cross-symbol invariant belongs in.

**Implication for the task-builder:** FX2 cannot be a literal rename of a named lens
(none exists). It must be phrased as **augmenting the task-qualitative Code Compatibility
group** (the correct scope for CODE function-to-function invariants) — most naturally a
new checklist item 6.5/7 or an augmentation of item 5 (Module context analysis) / item 6
(Downstream consumer analysis). See §1 for the exact insertion form. Anchoring FX2 to a
non-existent `internal-consistency` lens id will fail rf-qa-qualitative's own
task-qualitative item 14 ("Function existence claims require verification") and AX-5
(invented-content).

---

## 1. rf-qa-qualitative.md — lens/checklist structure + FX2 insertion point

### 1a. What "lens" formalism actually exists: the Five Adversarial Axes (PR-07)

The only structure in this file that is called a **lens** is the **Five Adversarial Axes**,
defined for the task-qualitative phase. Heading anchor (rf-qa-qualitative.md:580):

> `#### Five Adversarial Axes (PR-07 -- applied as a sharpening overlay across all 15 checks below)`

Intro prose form (rf-qa-qualitative.md:582):

> "These axes are NOT new checks -- they are adversarial lenses that sharpen the existing
> 15-item checklist. For every finding you record, annotate which axis fired in the Items
> Reviewed table (`axis: drift | contradictions | omissions | weakened-criteria |
> invented-content`). Pick the most-specific axis…"

Each axis charter has a fixed sub-form (verbatim AX-2, rf-qa-qualitative.md:597-605):

> "- **AX-2 Contradictions** (kebab alias: `contradictions`) -- Do two items in the task (or two
>   artifacts, or two sections of one artifact) assert mutually incompatible facts about the same
>   subject? … **Finding example (return-type mismatch pattern):** Section A states
>   `build_axis_overlay()` returns `dict[str, Axis]`, while Section B's call site unpacks the same
>   function's return value as `list[Axis]`… Annotate `axis: AX-2` with severity >= IMPORTANT."

**Axis charter form = `- **AX-N Name** (kebab alias: \`name\`) -- <charter question prose>.
**Finding example (<pattern name>):** <worked example>. Annotate \`axis: AX-N\`.`**

**DO NOT add a 6th axis (AX-6) for FX2.** The Axis-column vocabulary is a **closed set**
enforced in many places: `{AX-1, AX-2, AX-3, AX-4, AX-5, none}` (rf-qa-qualitative.md:639),
the HTML-comment schema in the Output Format (rf-qa-qualitative.md:838-857), and the
Summary block rules (rf-qa-qualitative.md:865-868). Adding AX-6 is high-blast-radius (breaks
every "closed set" assertion + the TEST-009-style fixtures). The cross-symbol invariant is a
**check**, not an adversarial-drift axis — it belongs in the checklist, and any finding it
produces annotates an existing axis (most likely **AX-2 Contradictions** — "two artifacts
assert incompatible facts about the same subject" already fits sibling-function-shape
disagreement, or **AX-3 Omissions**).

### 1b. Checklist item form (the correct home for FX2)

Checklists are grouped by `##### <Group Name>` sub-headings; each item is a numbered bold
lead-in + prose. The task-qualitative **Code Compatibility** group and its three items
(rf-qa-qualitative.md:670-676) — verbatim:

> `##### Code Compatibility`
>
> "4. **Function signature verification** — For each item that modifies a function, read the
>    actual function in the target source file. Verify: (a) the function exists at the described
>    location, (b) the described modification is compatible with the actual signature (parameter
>    names, types, return type), (c) the function's call sites won't break from the change…
>
> 5. **Module context analysis** — For each item that adds or modifies a function, read the full
>    module (not just the function). Check for module-level constants, imports, decorators, and
>    ambient dependencies that the new/modified function must interact with. If the module has
>    `_OUTPUT_FORMAT_BLOCK` as a constant used by sibling functions and the new function doesn't
>    reference it, that's likely an omission…
>
> 6. **Downstream consumer analysis** — For each item that changes an output format, schema, or
>    return value, trace all consumers of that output…"

**FX2 insertion recommendation (evidence-based):** Add a new item **inside the Code
Compatibility group**, immediately after item 6 (rf-qa-qualitative.md:676) — a
"Cross-symbol input-shape invariant" check. Its form MUST match the numbered-bold-prose
item shape above and be scoped to CODE (sibling functions sharing an input must agree on
its shape/contract). This directly catches F1 (`diagnose()` file-only guard vs sibling
`load_evidence()` / `_evidence_sha256()` accepting a dir). Item 5 ("Module context
analysis") is the nearest existing kin (it already reads the full module and reasons about
sibling functions/constants) — FX2 can be framed as either a new item or a targeted
augmentation of item 5's charter to add "sibling functions that consume the same input
parameter must agree on its accepted shape (file vs dir, str vs Path, scalar vs list); a
guard in one that its siblings don't share is a latent inconsistency."

**Downstream wiring FX2 must also touch** (so the new item is not orphaned):
- **Adaptation Guidance table** (rf-qa-qualitative.md:699-715) — every task-qualitative item
  has a "Doc Task Adaptation" row; a new item needs a matching row (Ban-N/A rule, item 9,
  rf-qa-qualitative.md:98, forbids leaving any check N/A).
- **Item count** — the group header says "Checklist (15 items)" (rf-qa-qualitative.md:660);
  adding an item makes it 16 and the Parallel-Partitioning note "For task files with >15
  checklist items" (rf-qa-qualitative.md:738) references the count.
- **Adversarial-axis annotation** — a finding from the new item still annotates an existing
  AX-1..AX-5 axis (recommend AX-2), preserving the closed-set vocabulary.

### 1c. All existing checklist "phases" (lenses) in the file

There is no flat "lens list"; the file is organized into **QA Phases**, each with its own
checklist. Enumerated (heading anchors):
- `prd-qualitative` (rf-qa-qualitative.md:133) — 23-item checklist.
- `report-qualitative` (rf-qa-qualitative.md:233) — 12 items.
- `tdd-qualitative` (rf-qa-qualitative.md:284) — 14 items, incl. an `##### Internal Consistency`
  group (rf-qa-qualitative.md:307-315: API-contract + data-model consistency).
- `tech-ref-qualitative` (rf-qa-qualitative.md:355) — 12 items.
- `ops-guide-qualitative` (rf-qa-qualitative.md:422) — 14 items.
- `readme-qualitative` (rf-qa-qualitative.md:493) — 12 items.
- `task-qualitative` (rf-qa-qualitative.md:560) — 15 items + Five Adversarial Axes overlay.
  **← this is FX2's phase (code-level).**
- `doc-qualitative` (rf-qa-qualitative.md:743) — 8-item fallback, item 4 "Internal consistency".
- `Fix Cycle` (rf-qa-qualitative.md:777).

The generic **Verification Principles** (rf-qa-qualitative.md:87-101) apply across all phases;
Principle #3 "Internal consistency" (rf-qa-qualitative.md:92) is document-level, NOT code-level:

> "3. **Internal consistency**: Claims in one section must not contradict claims in another.
>    Numbers must match across sections. Terminology must be consistent throughout."

If FX2 also wants a cross-cutting statement, augmenting Principle #3 to add a code clause is
possible, but the *operative* enforcement must land in the task-qualitative checklist (§1b),
because principles are advisory framing and the per-item checklist is what gets counted by
the Confidence Gate Protocol (rf-qa-qualitative.md:914-963).

---

## 2. Phase-2 / Phase-4 gate semantics location (for FX5 "Phase-4 FAIL rule" + FX3 "Phase-2 gate prerequisite")

**Important scope note:** the literal tokens "Phase 2" / "Phase 4" as *pipeline phase
numbers* are **task-builder `SKILL.md` phase numbers**, NOT defined in
`rf-qa-qualitative.md`. In this file, "phase" means a *QA phase* (prd-qualitative, etc.), and
gate/FAIL semantics live in two places:

**(a) Per-phase Verdict blocks — the FAIL rule form.** Each phase ends with a `### Verdict`
block. The **task-qualitative** verdict (the code-review phase FX5 cares about),
rf-qa-qualitative.md:732-735 — verbatim:

> `### Verdict (task-qualitative)`
>
> "- **PASS** — All checks pass, no issues of any severity.
> - **FAIL** — Any issues exist (CRITICAL, IMPORTANT, or MINOR). List each with specific
>   remediation. ALL issues must be resolved before proceeding — no severity level is exempt."

This "any issue at any severity ⇒ FAIL, ALL must resolve before proceeding" is the **FAIL-rule
shape** an FX5 "Phase-4 FAIL rule" should mirror. Severity definitions that feed it are at
`### Severity Ratings (task-qualitative)` (rf-qa-qualitative.md:717-721).

**(b) Confidence Gate Protocol — the numeric gate.** rf-qa-qualitative.md:914-963. This is the
computed PASS/FAIL gate ("confidence = VERIFIED / (TOTAL - UNVERIFIABLE) * 100";
"confidence >= 95% AND UNCHECKED == 0: eligible for PASS", rf-qa-qualitative.md:935-939). Any
new FX2 checklist item automatically enters TOTAL here, so FX5's Phase-4 FAIL rule and FX3's
Phase-2 prerequisite interact with this gate by construction.

**(c) The cross-file gate wiring** ("any gap regardless of severity = FAIL") lives in the
**task-builder `SKILL.md` §A.8 / §A.10 merge steps**, referenced from this file at
rf-qa-qualitative.md:83 (DNSP block: "treated as a real finding for the existing 'any gap
regardless of severity = FAIL' gating rule … pick-up wiring lands at T06.11"). So the
**Phase-2 gate prerequisite (FX3)** and **Phase-4 FAIL rule (FX5)** are most precisely wired
in `task-builder/SKILL.md` (out of R4's 3-file scope — flag to R6/R7), with this agent file
carrying the *checklist item* and its *Verdict FAIL rule* counterpart. The anchor proving the
SKILL.md ↔ agent handshake is rf-qa-qualitative.md:83 and the "Inherited Structural Verdict"
handshake at rf-qa-qualitative.md:1071-1096.

---

## 3. reflect-reviewer.md — reviewer slot/dimension structure + FX1 advisory slot

### 3a. How "slots/dimensions" are defined

`reflect-reviewer` is a **single restricted read-only agent** spawned N times as the
heterogeneous Tier-2 ensemble. It has **no named per-dimension slots**; instead:

- The **4 deviation categories** are its classification vocabulary (Role section,
  reflect-reviewer.md:21-26) — verbatim:

  > "You audit completed work against its driving spec/tasklist and classify **each**
  > divergence under the 4-category deviation taxonomy:
  > - **Authorized expansion** — …
  > - **Necessary deviation** — …
  > - **Drift** — …
  > - **Regression** — a change that breaks or removes previously-working behavior, or
  >   contradicts a load-bearing invariant."

- The **per-reviewer persona ("lens")** is supplied via the brief, NOT hard-coded as a
  distinct agent (reflect-reviewer.md:17 and the `persona_lens` input, reflect-reviewer.md:54):

  > "- `persona_lens`: the reviewer persona you adopt for this pass (e.g. correctness-focused,
  >   regression-focused, architecture-focused), supplied via the brief."

  and reflect-reviewer.md:17: "the persona lens is supplied through the per-reviewer brief,
  not through a distinct agent type."

- Output is a single **Deviations table** with a `Category` column
  (reflect-reviewer.md:80-91), plus an Adherence summary counting the 4 classes:

  > `| # | Category | Location | What diverged | Evidence (file:line) | Severity |`
  > …
  > "- Authorized expansion: <N> | Necessary deviation: <N> | Drift: <N> | Regression: <N>"

### 3b. What makes a finding advisory (raised-for-triage) vs auto-gating **in this brief**

**Key structural fact: `reflect-reviewer` itself NEVER gates.** It is read-only and only
**RETURNS** findings; the orchestrator persists and decides. Verbatim anchors:
- reflect-reviewer.md:36 (Safety Constraint): "You only RETURN your structured deviation
  findings; the orchestrator persists them."
- reflect-reviewer.md:55 (`output_path` input): "You do NOT write this file yourself… you
  return your structured findings and the orchestrator writes them."
- reflect-reviewer.md:65 (Responsibility 5): "Return a structured deviation list to the
  orchestrator. You do not write it to the repo — you RETURN it."

So **every reflect-reviewer finding is already "advisory" at the reviewer layer** — the
auto-gating decision is downstream (in the taxonomy + skill). The *auto-gating* semantics
live in `deviation-taxonomy.md`: **Regression is the only class that unconditionally
escalates** (deviation-taxonomy.md:85: "Regression is the **only class** that
*unconditionally* triggers a Tier 3 remediation offer… It also **unconditionally forces
escalation to Tier 2**"). Everything else's escalation is conditional. **This is the exact
lever FX1 must respect:** to keep a new correctness finding **advisory / raised-for-triage
and NEVER auto-gating**, it must be defined as a class that does NOT set `regression_present`
and does NOT enter the unconditional-escalation path.

### 3c. Where the additive "no-spec correctness" slot goes

FX1's advisory no-spec correctness slot should be added as a **new persona_lens value +
a new advisory finding-type**, NOT a new agent and NOT a 5th auto-gating category. Concretely:

1. **Role section (reflect-reviewer.md:21-26)** — add an advisory note that beyond the
   4 deviation classes (which are spec-relative), the reviewer MAY surface **no-spec
   correctness gaps** (bugs correct-to-spec but wrong-in-code, e.g. sibling functions
   disagreeing on input shape) and RAISE them for triage — explicitly marked non-gating.
2. **`persona_lens` (reflect-reviewer.md:54)** — the enum already includes
   "correctness-focused"; FX1 can formalize a `no-spec-correctness` lens value here.
3. **Output Format (reflect-reviewer.md:71-97)** — add an advisory sub-section (e.g.
   `## Correctness gaps (advisory — raised for triage, non-gating)`) SEPARATE from the
   Deviations table, so it never feeds the 4-class Adherence counts. This mirrors the
   taxonomy's own "parallel artifact" pattern (grounding-gaps) that keeps advisory items
   OUT of the gating ledger (deviation-taxonomy.md:129-154).
4. **Behavioral Mindset (reflect-reviewer.md:42)** already supports raising uncertain items:
   "A false PASS is worse than a false FAIL. Favor flagging… over rationalizing" — FX1's
   advisory slot is consistent with this and should cite it.

**Advisory-vs-gating discriminator to encode:** a finding is **advisory (raised-for-triage)**
when it is (a) returned in the separate correctness-gap sub-section, (b) does NOT increment
any `regression_present` / `verification_regressions_detected` counter, and (c) does NOT set
`needs_human_decision` in a way that forces `status: partial`. It is **auto-gating** only if
it maps to Regression per deviation-taxonomy.md:85. FX1 must keep the new slot in category (a).

---

## 4. deviation-taxonomy.md — 4-category format + FX1 "correctness-gap" 5th dimension

### 4a. HARD CONSTRAINT: the taxonomy is deliberately 4 categories, and a 5th was explicitly rejected

This is the single most important finding for FX1. The file asserts **"4 categories, not 5"
repeatedly and by design**, and records an explicit Kill-List rejection of a 5th:
- deviation-taxonomy.md:5: "The taxonomy is **4 categories** — `evidence-insufficient`
  findings route to a parallel artifact… not a 5th category."
- deviation-taxonomy.md:131: "The taxonomy is **4 categories**, not 5. There is no `unknown`
  deviation class."
- deviation-taxonomy.md:154: "The 5th deviation category was explicitly rejected in §17.7 Kill
  List; see that section for the rationale."
- Two later feeders explicitly "add **no 5th category**" and route to existing classes /
  the parallel artifact: FR-4 exit-code mapping (deviation-taxonomy.md:101-115) and FR-RH1
  reachability (deviation-taxonomy.md:117-127: "adds **no 5th category**").

**Implication for FX1:** Adding a literal 5th **deviation class** to
`deviation-ledger.yaml` DIRECTLY VIOLATES the file's load-bearing invariant and the §17.7
Kill List. FX1's "correctness-gap dimension" MUST be modeled the way this file already
models every non-4-class signal: **as an advisory parallel artifact / finding-modifier that
routes by evidence onto the existing classes OR into a separate advisory file — never a 5th
gating class.** The correct pattern to copy is the **Grounding-gaps parallel artifact**
(deviation-taxonomy.md:129-154) and the FR-RH1 "sibling finding-modifier, no new class"
framing (deviation-taxonomy.md:117-127). Presenting FX1 as "add a 5th category" will
guarantee a reflect/QA FAIL against this file's own invariant.

### 4b. Exact format of each category entry (the form to match)

Each of the 4 categories is a `## <Name>` section with **four bold-lead paragraphs**.
Verbatim, **Authorized** (deviation-taxonomy.md:26-38):

> `## Authorized`
>
> "**Definition.** A scope addition that was *explicitly* approved by an authoritative
> artifact…
>
> **Detection signals.**
> - Diff hunk maps to a tasklist item AND that tasklist item was added…
> - Task log contains explicit "user approved scope expansion to include X"…
> - Spec doc has a revision-history entry…
>
> **Gold-standard reference.** Updated tasklist file + revision-history of spec + task log…
>
> **Default remediation.** None. Document in the report. No Tier 3 task."

The other three follow the identical 4-part shape:
`## Necessary` (deviation-taxonomy.md:40-54), `## Drift` (deviation-taxonomy.md:56-71),
`## Regression` (deviation-taxonomy.md:73-85). The header note at deviation-taxonomy.md:9
states the contract: "Each category has: definition, detection signals, gold-standard
reference, default remediation."

The **Grounding-gaps parallel artifact** (the advisory pattern FX1 should mirror) is at
deviation-taxonomy.md:129-154, with its byte-exact YAML schema (deviation-taxonomy.md:139-146)
and "Non-empty consequences" block (deviation-taxonomy.md:148-153) that sets
`status: partial` + `needs_human_decision: true` WITHOUT being a deviation class.

### 4c. Where/how to add the "correctness-gap" dimension

**Recommended form (matches existing conventions, respects the 4-class invariant):** add a
new `## Correctness-gap (advisory parallel dimension — no 5th class)` section positioned
**alongside the FR-RH1 and Grounding-gaps sections** (after deviation-taxonomy.md:127,
before or after the Grounding-gaps parallel artifact at :129). It should:
- Open by restating "adds **no 5th category**" (mirroring deviation-taxonomy.md:119).
- Define a **finding-modifier / advisory routing**: a no-spec correctness gap (spec-conformant
  but code-wrong; e.g. F1 sibling-shape disagreement) is **raised for triage** into a
  parallel artifact (parallel to `grounding-gaps.yaml`), NOT `deviation-ledger.yaml`.
- Explicitly state it does NOT set `regression_present`, does NOT enter the §5.3 unconditional
  Tier-2 escalation, and does NOT increment `verification_regressions_detected` — i.e., it is
  advisory, never auto-gating (satisfying FX1's "NEVER auto-gating" constraint).
- Optionally add a small evidence-routing table like the FR-4 / FR-RH1 tables
  (deviation-taxonomy.md:105-115, :121-125) mapping the correctness evidence to
  advisory/none rather than to Regression.

If a routing onto existing classes is preferred instead of a parallel artifact, the honest
mapping is: a correctness gap that *contradicts a spec acceptance criterion or a documented
invariant* is already **Regression** (deviation-taxonomy.md:75, :82 "documented invariant…
violated"); a correctness gap with NO spec anchor (the F1 case — spec is silent) has no
existing home and is exactly why FX1's advisory parallel dimension is needed. That gap in
coverage is the load-bearing justification for FX1 and should be cited from
deviation-taxonomy.md:75/:82 (invariant clause is spec-relative; a *no-spec* invariant break
falls through).

---

## 5. Sync / Source-of-Truth note (verified)

All three files are **`src/superclaude/` Source-of-Truth files, tracked in git**; their
`.claude/` mirrors are **gitignored sync-dev output** and currently do not even exist on
disk in this worktree. Verified:
- `git ls-files` returns all three `src/superclaude/...` paths (tracked).
- `git check-ignore .claude/agents/rf-qa-qualitative.md` → matched (ignored).
- `ls .claude/agents/rf-qa-qualitative.md` → "No such file or directory" (mirror not
  materialized in this worktree).

**Editing rule for FX1/FX2 (BLOCKING):** edit ONLY the `src/superclaude/` files, then run
`make sync-dev` to regenerate `.claude/`, then `make verify-sync`. NEVER edit the `.claude/`
copies (they are regenerated and gitignored except `.claude/settings.json`). Per project
CLAUDE.md this is an ABSOLUTE rule — never `git add` any `.claude/{agents,skills}/...` path.

Target SoT paths for the two fixes:
- FX2 → `src/superclaude/agents/rf-qa-qualitative.md` (task-qualitative Code Compatibility
  group, ~line 676; + Adaptation Guidance table ~699-715; + item count 660/738).
- FX1 → `src/superclaude/agents/reflect-reviewer.md` (Role 21-26, persona_lens 54, Output
  Format 71-97) **and** `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`
  (new advisory `## Correctness-gap` section near :127/:129).

---

## Summary of load-bearing findings for the task-builder

1. **No `internal-consistency` lens exists** — FX2 must augment the **task-qualitative Code
   Compatibility group** (rf-qa-qualitative.md:670-676), NOT rename a non-existent lens.
   Recommend a new checklist item after item 6, or augment item 5 (Module context analysis).
   Findings annotate an existing **AX-2** axis; **do NOT add AX-6** (closed-set vocabulary,
   rf-qa-qualitative.md:639, enforced in ~4 places).
2. FX2 must also update the **Adaptation Guidance table** (rf-qa-qualitative.md:699-715), the
   **item count** ("15 items" → 16, rf-qa-qualitative.md:660 + partition note :738).
3. **Phase-4 FAIL rule (FX5)** mirrors the per-phase **Verdict** block form
   (rf-qa-qualitative.md:732-735); **Phase-2 gate prerequisite (FX3)** wires through the
   Confidence Gate Protocol (rf-qa-qualitative.md:914-963) and the SKILL.md §A.8/§A.10 merge
   handshake referenced at rf-qa-qualitative.md:83 — the numeric Phase-2/Phase-4 pipeline
   numbers live in **task-builder/SKILL.md**, out of R4's 3-file scope (flag to R6/R7).
4. **reflect-reviewer never gates** — it RETURNS findings (reflect-reviewer.md:36/55/65).
   FX1's advisory slot = new `persona_lens` value (reflect-reviewer.md:54) + a **separate
   advisory sub-section** in Output Format (reflect-reviewer.md:71-97) that stays OUT of the
   4-class Deviations table/counts. Auto-gating is downstream and Regression-only
   (deviation-taxonomy.md:85).
5. **deviation-taxonomy.md forbids a 5th class by design** (deviation-taxonomy.md:5, :131,
   :154 §17.7 Kill List). FX1's "correctness-gap dimension" MUST be an **advisory parallel
   artifact / finding-modifier** (mirror Grounding-gaps :129-154 and FR-RH1 "no 5th category"
   :117-127) — NOT a 5th gating deviation class. Framing it as a 5th category will fail the
   file's own load-bearing invariant.
6. **The coverage gap that justifies FX1**: existing Regression is spec-relative
   (deviation-taxonomy.md:75/:82 — "documented invariant… violated"). A **no-spec** invariant
   break (F1's `diagnose()` vs sibling shape mismatch, spec silent) has no home today → that's
   the load-bearing justification, advisory and non-gating.
7. **SoT confirmed**: all 3 are tracked `src/superclaude/` files; `.claude/` mirrors are
   gitignored and unmaterialized. Edit src → `make sync-dev` → `make verify-sync`. Never
   edit/stage `.claude/`.
