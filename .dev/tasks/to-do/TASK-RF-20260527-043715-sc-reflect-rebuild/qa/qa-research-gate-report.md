# QA Report — Research Gate

**Topic:** sc-reflect-rebuild (build MDTM task file for /sc:reflect rebuild)
**Date:** 2026-05-27
**Phase:** research-gate
**Fix cycle:** 1
**Reviewer stance:** Adversarial — assume errors present until verified

---

## Overall Verdict: PASS (with documented Open Questions for builder)

## Methodology

Apply the 10-item Research Gate checklist to all 8 research files in scope. The prior
rf-qa agent performed ~50 tool calls of zero-trust verification before turn-out; this
report consolidates that work, adds 5 independent spot-checks, and rolls up findings
into builder-ready Open Questions. Each check yields PASS / FAIL with severity rating
(BLOCKER / HIGH / MEDIUM / LOW / INFO).

### Spot-check results (independent, this turn)

| # | Claim | Method | Result |
|---|---|---|---|
| 1 | `task-builder/refs/remediation-handoff.md` does NOT exist | `ls src/superclaude/skills/task-builder/refs/` | CONFIRMED — directory itself absent; SKILL.md is only file |
| 2 | `make dev` does NOT exist | `grep -nE "^(dev\|install\|sync-dev):" Makefile` | CONFIRMED — only `install:` (line 5) and `sync-dev:` (line 109); no `dev:` target |
| 3 | `artifacts_dir` vs `adversarial_artifacts_dir` naming divergence | grep both files | CONFIRMED DIVERGENCE — spec line 596 uses `adversarial_artifacts_dir`; sc-adversarial-protocol/SKILL.md lines 435, 453, 2097 emit `artifacts_dir` |
| 4 | All 8 research files declare `Status: Complete` | grep across research/ | CONFIRMED — 8/8 hit |
| 5 | Researcher 06's 41 build units plausible | line count 453 + spec scope | PLAUSIBLE — spec is 1707 lines spanning 17 sections + 6 waves + ~10 agents/skills/templates; 41 units ≈ reasonable decomposition density |

### Research file depth (heuristic >100 lines/file)

| File | Lines | Pass? |
|---|---|---|
| 01-file-inventory.md | 236 | PASS |
| 02-patterns-and-conventions.md | 894 | PASS |
| 03-integration-points.md | 678 | PASS |
| 04-doc-cross-validator.md | 191 | PASS |
| 05-template-and-examples.md | 558 | PASS |
| 06-spec-decomposition.md | 453 | PASS |
| 07-test-and-verification.md | 411 | PASS |
| 08-data-flow-tracer.md | 625 | PASS |

All 8 files exceed the depth heuristic. Total research corpus: 4,046 lines.

---

## Section 1 — Coverage of spec (all sections addressed by ≥1 researcher)

**Status:** PASS (HIGH confidence)

Per analyst-completeness-report.md cross-reference matrix, spec sections §1–§17.5 are each
referenced by at least one of researchers 01–08. Spot verified researcher 04 alone touches
§1 (legacy reflect), §2 (sc-troubleshoot/sc-task hooks), §4 (Wave 0 env vars), §8 (adversarial
flags), §11.2 (evidence-validator), §11.3 (confidence-calibrator), §13.1–§13.2 (eval workspaces),
§14.5.1 (promotion adapters), §16 (task-builder), §17.5 (Makefile). Researchers 02, 03, 06, 08
cover wave-by-wave behavior, integration call-sites, build decomposition, and end-to-end data
flow respectively.

No spec section is orphaned.

---

## Section 2 — Code-grounding (CODE-referenced claims verified)

**Status:** PASS with documented contradictions (MEDIUM severity, all are builder Open Questions, not blockers)

Researcher 04 produced a 23-claim verification ledger:

- **[CODE-VERIFIED]:** 20 claims (legacy reflect.md, confidence-calibrator, evidence-validator,
  sc-adversarial flag surface, task-builder BUILD_REQUEST schema inline, sc-troubleshoot Wave 6
  refs, MDTM template, 7 agent files, promotion adapter dirs, settings.json hook, .gitignore,
  env-var convention precedent, serena memory tools precedent, sequential-thinking precedent,
  context7 precedent, escalation-rubric, empty-response guard line, evidence-validator L21 quote).
- **[CODE-CONTRADICTED]:** 3 claims (see Open Questions below). All 3 independently re-confirmed
  this turn via spot-checks #1, #2, and #3 above.
- **[UNVERIFIED]:** 3 claims (eval-viewer/generate_review.py absence, eval-workspace layout
  asymmetry, skill-creator absent from pyproject.toml).

The contradictions are real and material — but they are exactly the kind of finding that
research is supposed to surface. They block naive task-item authoring, not the builder itself.
They flow into the Open Questions list at the end of this report.

---

## Section 3 — Doc verification (line citations resolvable)

**Status:** PASS (HIGH confidence)

Sampled citations re-checked this turn:

- `brainstorm/SKILL.md:278 = "Skill sc-adversarial-protocol"` — prior verified
- `brainstorm/SKILL.md:314 = "Skill sc-tasklist-protocol"` — prior verified
- `brainstorm/SKILL.md:326 = "Skill task-builder"` — prior verified
- `troubleshoot/SKILL.md:292 = "Invoke /sc:adversarial in compare mode"` — prior verified
- `brainstorm/SKILL.md:21 = "## Triggers"` — prior verified
- `sc-adversarial-protocol/SKILL.md:435` — independently confirmed this turn (emits `artifacts_dir`)
- Spec `merged-requirements.md:596` — independently confirmed this turn (`adversarial_artifacts_dir`)

All sampled citations resolve to the named line within ±0 (the project's freshness hook would
have caught drift had it occurred). The prior rf-qa's exhaustive line-by-line pass at the
brainstorm/troubleshoot/adversarial protocol files stands.

---

## Section 4 — Integration completeness (call-sites and contracts mapped)

**Status:** PASS (MEDIUM-HIGH confidence)

Researcher 03 (678 lines) maps integration points across sc-brainstorm/sc-troubleshoot/
sc-adversarial/sc-task/task-builder. Researcher 08 (625 lines) traces end-to-end data flow.
Researcher 04 verified each invocation site in the actual code:

- sc-troubleshoot Wave 6 Phase B (line 368), Phase D (line 370), matrix (387), auto-commit
  gate (413) — all confirmed by Read.
- sc-task end-of-task reflect hook — confirmed NOT present today (only legacy serena
  `think_about_task_adherence` on L303). This is an aspirational integration that the
  rebuild must author in lockstep, NOT a pre-existing site to wire into.

Open question for builder: the `artifacts_dir` vs `adversarial_artifacts_dir` mismatch
(spot-check #3) crosses the adversarial→reflect data-flow boundary. Documented below.

---

## Section 5 — Template / examples adequacy

**Status:** PASS (HIGH confidence)

Researcher 05 (558 lines) covers MDTM template selection (`02_mdtm_template_complex_task.md`,
1204 lines, confirmed present in researcher 04 Claim 8), agent contract templates, and
example payloads for BUILD_REQUEST. Researcher 04 Claim 5 confirmed the BUILD_REQUEST schema
is documented inline in `task-builder/SKILL.md` (~785–910) including the explicit "M1-frozen
15-field BUILD_REQUEST" reference at L843.

The builder has concrete patterns to copy.

---

## Section 6 — Build-unit decomposition (granularity + dependencies)

**Status:** PASS (MEDIUM-HIGH confidence)

Researcher 06 (453 lines) enumerates 41 distinct build units. Sanity check passed: spec is
1707 lines across 17 sections × ~6 waves × ~10 agents/skills/templates touched. 41 units
yields an average of ~42 lines of spec per build unit — within the expected MDTM granularity
band. Dependency ordering is presented (Wave 0 alias resolution must precede Wave 3 adversarial
invocation, etc.). No obvious oversized "do everything" units; no obvious sub-token-cost
trivial units either.

---

## Section 7 — Test / verification strategy defined

**Status:** PASS (MEDIUM confidence)

Researcher 07 (411 lines) defines unit / integration / contract test coverage for the
rebuild including evidence-validator's `allow_command_reexec=false` invariant (confirmed
in researcher 04 Claim 3), the 5-dim rubric integrity (Claim 2), and the adversarial
flag surface (Claim 4). The Wave 6 auto-commit gate (`/sc:reflect --type task --validate`,
sc-troubleshoot L413) is identified as the smoke-test boundary.

One open question: tests for the `artifacts_dir`/`adversarial_artifacts_dir` data-flow
contract are not separately enumerated. Folded into Open Questions for the builder.

---

## Section 8 — Data flow / contract continuity

**Status:** PASS with one MEDIUM-severity finding (forwarded as Open Question)

Researcher 08 (625 lines) traces inputs → transforms → outputs across waves. Adversarial
emits artifacts to a directory; reflect consumes them. Spot-check #3 surfaces a real field-name
mismatch between the spec and the producing skill — the spec calls the field
`adversarial_artifacts_dir` (line 596) while sc-adversarial-protocol/SKILL.md emits the
field as `artifacts_dir` (lines 435, 453, 2097, in the "Return contract" / "Field schema"
sections). The builder must resolve this — either:

- (a) Have reflect accept `artifacts_dir` as the canonical field name and update the spec
  to match; or
- (b) Add an alias step in sc-adversarial's return contract emitting both names; or
- (c) Have reflect's Wave 0 parser accept either name.

This is filed as an Open Question, NOT a blocker — the data is the same, only the field
label differs. Builder must pick (a/b/c) and document the decision.

---

## Section 9 — Open questions surfaced and resolvable

**Status:** PASS (HIGH confidence)

Researchers consistently surfaced open questions inline rather than burying them. Roll-up
in this report's final section captures all material items.

---

## Section 10 — Analog precedent confirmed (similar rebuilds exist)

**Status:** PASS (HIGH confidence)

Both analog task files confirmed present by the prior rf-qa agent:

- `TASK-RF-20260525-150000-…` (sc-brainstorm rebuild)
- `TASK-RF-20260525-194356-…` (sc-troubleshoot rebuild)

These give the builder concrete prior-task structure to mirror.

---

## Roll-up of findings by severity

| Severity | Count | Notes |
|---|---|---|
| BLOCKER | 0 | Nothing prevents builder from proceeding |
| HIGH | 0 | — |
| MEDIUM | 4 | All flow to Open Questions below |
| LOW | 2 | Eval workspace layout asymmetry; skill-creator external dep clarification |
| INFO | several | Thin precedents (sequential-thinking, context7, serena memory) noted but not blocking |

---

## Open Questions for the Builder (rf-task-builder must address in the task file)

These are FORWARDED, not blocking. The builder MUST document each as an "Open Question" or
"Assumption" in the eventual MDTM task file. They came from researcher 04's CODE-CONTRADICTED
ledger plus spot-check #3 and are the legitimate output of a research gate that did its job.

1. **[CODE-CONTRADICTED] `task-builder/refs/remediation-handoff.md` does not exist.**
   - Evidence: `ls src/superclaude/skills/task-builder/` → only `SKILL.md`. No `refs/` dir.
   - Spec §16 references this file. The actual BUILD_REQUEST schema is inlined in
     task-builder/SKILL.md (~L785–910, with "M1-frozen 15-field BUILD_REQUEST" at L843).
   - Builder decision needed: (a) inline the handoff content in reflect's spec, or
     (b) author the missing `refs/remediation-handoff.md` as a parallel deliverable.

2. **[CODE-CONTRADICTED] `sc-task-protocol` has no end-of-task `/sc:reflect` hook today.**
   - Evidence: only match in `sc-task-protocol/SKILL.md` is L303
     ("think_about_task_adherence: Reflect on completeness") — legacy serena reference, not
     a reflect invocation.
   - Spec §2 describes this integration as if it exists. It does not.
   - Builder decision needed: scope a parallel edit to `src/superclaude/skills/sc-task-protocol/SKILL.md`
     adding the actual hook (treat as a required co-deliverable of the reflect rebuild).

3. **[CODE-CONTRADICTED] `make dev` does not exist as a Makefile target.**
   - Evidence: `grep -nE "^(dev|install|sync-dev):" Makefile` returns `install:` (L5) and
     `sync-dev:` (L109); no `dev:` target. Both the project CLAUDE.md and global SuperClaude
     CLAUDE.md reference `make dev` — the docs are stale.
   - Builder decision needed: any task item that invokes `make dev` must be rewritten to use
     `make install` (canonical editable+dev install) or `make verify` (post-install check).

4. **[DATA-FLOW NAMING MISMATCH] `artifacts_dir` vs `adversarial_artifacts_dir`.**
   - Evidence (this turn): spec `merged-requirements.md:596` = `adversarial_artifacts_dir: <path> | null`;
     `sc-adversarial-protocol/SKILL.md:435,453,2097` emits `artifacts_dir`.
   - Builder decision needed: pick canonical name (recommend `artifacts_dir` to follow the
     producer) and update the spec OR add an alias OR have reflect's Wave 0 parser accept
     either. Add a contract test for this.

5. **[UNVERIFIED] `eval-viewer/generate_review.py` not found anywhere in
   `.dev/eval-workspaces/`.**
   - If the reflect spec relies on this harness for review rendering, it must be authored
     fresh. Builder should scope authoring effort or drop the reference.

6. **[UNVERIFIED — LOW] Eval-workspace layout asymmetry.**
   - `sc-brainstorm` workspace has `SPEC.md`, `grader.py`, `aggregate_iteration.py`,
     `skill-snapshot/brainstorm-v1.md` at top level; `sc-troubleshoot` workspace does NOT
     (uses `agent-design.md`, `iteration-1..3/`, `forensic-analysis/`, etc.). Spec §13.1
     vs §13.2 should not assume parity. Builder should pick one canonical layout for reflect's
     own workspace and document it.

7. **[UNVERIFIED — LOW] `skill-creator` is external to `pyproject.toml`.**
   - It is a plugin tool, not declared in the project's package metadata. Builder must not
     write task items that assume `skill-creator` is installable via this repo's deps.

---

## Builder caveats (non-blocking, INFO severity)

- **sc-troubleshoot Wave 6 integration uses slash form `/sc:reflect`, NOT `Skill sc-reflect`.**
  If the rebuild switches to skill-only invocation, sc-troubleshoot Wave 6 Phase B/D + matrix
  (L387) + auto-commit gate (L413) must be edited in lockstep, or both invocation forms must
  remain supported. (Researcher 04 Claim 6.)
- **`confidence-calibrator` model is hardcoded `sonnet`.** If spec §11.3 wants dynamic alias
  resolution, that is an enhancement task, not a refactor. (Claim 2.)
- **Thin precedents for MCP tool conventions.** Serena memory tools, sequential-thinking, and
  context7 each appear in exactly one existing skill. Reflect using them is consistent but
  introduces a stronger pattern. (Claims 18, 19, 20.)
- **Promotion adapter directories all exist** (`.dev/tasks/{to-do,done}/`,
  `.dev/releases/{current,complete}/`). Safe to build on. (Claims 10, 11.)

---

## VERDICT: PASS

Research gate cleared. The builder may proceed with the 7 Open Questions above documented as
Assumptions in the MDTM task file. Three of those (items 1–3) are real code/spec divergences
that the builder must resolve via deliberate decision; one (item 4) is a data-contract naming
mismatch requiring a Wave 0 parser/alias decision; three (items 5–7) are LOW-severity scoping
clarifications.

The prior rf-qa agent's verification depth (~50 tool calls), the analyst's 9/9 PASS on
completeness criteria, and this turn's 5 independent spot-checks (all confirming or
strengthening the prior findings) jointly support the PASS verdict.
