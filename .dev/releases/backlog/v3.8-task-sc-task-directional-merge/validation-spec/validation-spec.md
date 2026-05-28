<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: variant-2 (combined score 0.947) -->
<!-- Incorporated: variant-1 (steelman, 0.727), variant-3 (security-probe, 0.921) -->
<!-- Merge date: 2026-05-15 -->
<!-- Source plan: .dev/releases/current/task-sc-task-directional-merge/artifacts/final-merge-plan.md -->
<!-- Convergence: 0.86 (threshold 0.85); 0 HIGH-severity unaddressed invariants after Round 3 -->

---
spec_type: validation
target_release: task-sc-task-directional-merge
stance: synthesized (steelman + adversarial-attack + security-probe)
focus: [tradeoffs, invariants, failure-modes, evidence]
source_plan: .dev/releases/current/task-sc-task-directional-merge/artifacts/final-merge-plan.md
plan_assertions_under_validation:
  - "PASS. ZERO OPEN FINDINGS." (source line 46)
  - "18/18 compat hazards MITIGATED" (source line 43)
  - "INV-01..INV-05 SURVIVE — demonstrated, not asserted" (source line 472)
invariant_anchor_source: extension-point-contracts.md:11-17
convergence_score: 0.86
unaddressed_high_invariants: 0
---

# Validation Spec — Final Merge Plan (synthesized verdict)

## 1. Verdict — three-clause synthesis

<!-- Source: V2 § 1 + V1 § 1 + V3 § 11 (restructured to balanced verdict) -->

The source plan's headline claim — **"PASS. ZERO OPEN FINDINGS"** (source line 46) — is decomposed into three independently true sub-claims, each surviving only at the layer it was authored against:

1. **Closures resolve the Phase-7-named findings.** The eight closures F-01..F-08 cleanly resolve the open findings the prior phase named; the V/C/K verdicts carry forward zero-drift; the ledger is not re-litigated; the 10-step canonical sequence has a defensible shape backed by hazard-derived sequencing constraints S-1..S-3. The plan is *correctly dispositioned at the level it defines disposition*. This clause holds.
2. **Closure predicates are under-specified against degenerate inputs.** Eighteen falsifiable gaps live inside the closures themselves: F-02's grep enforcement is occurrence-order against an alternation pattern; F-03 covers `git_status=dirty` but not the four other observable states; F-04 collapses four on-disk states into a three-token predicate; the 79 row-instance / 65 distinct CR-ID condensation arithmetic is asserted without enumeration; the 67-row vs 65-CR-ID delta is not reconciled. The plan is *under-specified at the predicate-precision layer*. This clause holds.
3. **Six timeline / tooling-layer hazards survive at a layer the row-level mitigations do not reach.** The plan's failure-mode register lives in `compat-hazard-report.md` HZ-01..HZ-18 and is per-row, per-acceptance-criterion, per-pre-commit-gate. Six additional hazards — PRD soft-block, rebase-split bypass, worktree race, residual-reference survival, in-flight semantic exposure (96 task files), deferred regenerator drift — live across the merge timeline and the tooling boundary. None re-open a rejected-ledger entry. The plan is *binding at the row level, fragile at the operational level*. This clause holds.

**Synthesized verdict.** The plan is binding in the procedural sense that downstream implementers have a documented paper trail; it is *not* binding in the strong operational sense the source line 462 closure paragraph asserts. Thirty falsifiable acceptance criteria (AC-ATK-01..18 + AC-SM-01..12) gate the upgrade from "procedurally binding" to "operationally binding." A Phase 7.5 patch sprint addressing the 18 closure-predicate gaps + 6 timeline-layer hazards closes the residual surface.

---

## 2. Defense overlay — what the plan correctly disposes

<!-- Source: V1 §§ 2–3 (incorporated as defense overlay) -->

Before enumerating the gaps, this section names what the plan gets right. Each TU and ME below is paired with the specific invariant(s) it protects and the alternative disposition that would have weakened the invariant. This overlay is the answer to "what must downstream implementers preserve verbatim?"

### Transfer Units (TU-1..TU-8) — V/C/K verdicts validated

| TU | Verdict | Invariants protected | Why the verdict is correct | Alternative that would weaken INV |
|---|---|---|---|---|
| TU-1 (`Tier:` field + Gate 1 + per-item marker) | ADOPT | INV-05, INV-01, INV-04 | `Tier:` is metadata, not work-definition; per-item marker is ME-1-bound "tier-conditioned read" | ADAPT with embedded runtime classifier re-introduces D09b (REJECTed at source line 87 / 206) |
| TU-2 (Critical / Trivial Path Override) | ADOPT | INV-05, INV-01 | F-02 sentinel + row-1 ordering grep make CR-7 structurally bounded | ADAPT (reorder calls) lets `tier_field_validate` race ahead, violating INV-05 |
| TU-3 (Gate 2 Verification roster widening) | ADAPT | INV-03, ME-2 | Widening to `[rf-qa, quality-engineer]` permitted because ME-2 keeps rf-qa present | ADOPT verbatim risks replacing rf-qa; REJECT leaves STRICT under-verified |
| TU-4 (D15b Layer 2 pre-flight) | ADAPT | INV-01, INV-04 | Re-framed as Task Log emission, not gate; warns-and-continues on dirty git | ADOPT-as-gate (Reading B) authors new HALT semantic that INV-01 forbids |
| TU-5 (TFEP baseline snapshot) | ADOPT | INV-04, INV-03 | Baseline YAML on disk pre-F1 is what makes resumability hold | ADAPT to in-memory baseline breaks INV-04 across resumption |
| TU-6 (TFEP Prohibitions + Carve-outs) | ADOPT | INV-02 | Reinforces F2 (additive within existing catalog) | ADAPT (re-author list) risks dropping an F2 entry |
| TU-7 (TFEP Escalation trigger) | ADOPT | INV-03, ME-2 | Third invocation point; F-05 authorized widening with three-prong defense | REJECT forces new gate (D25 REJECTed); ADAPT to sibling violates ME-2 |
| TU-8 (TFEP Incident reporting) | ADOPT | INV-04 | Side-effect file; survives session boundaries; no in-task heading | ADAPT to in-task remediation block breaks INV-04 |

### Manifest Exceptions (ME-1..ME-9) — load-bearing analysis

- **ME-1 (per-item dispatch forbidden) — load-bearing.** Audit gate that prevents per-item marker from becoming a runtime classifier. Without ME-1, D09b functionally returns; F1 progress monotonicity erodes.
- **ME-2 (rf-qa never replaced, never displaced) — load-bearing.** INV-03's floor. Every roster widening (TU-3, TU-7) is permitted only because ME-2 keeps rf-qa present at all three invocation points.
- **ME-3 (no new HALT semantics in F1) — load-bearing.** INV-01 progress guarantee. The F-03 closure leans directly on ME-3 to forbid refuse-entry on a dirty git tree.
- **ME-4, ME-5, ME-7, ME-8 (collective) — HELD without per-row deltas.** Fence ancillary donor patterns that no F-01..F-08 finding re-opened.
- **ME-6 (M1 atomicity) — load-bearing.** The seven foundation rows are mutually-presupposing; landing them in separate commits leaves intermediate states that fail their own pre-commit gates.
- **ME-9 (donor-ceremony drop audit) — load-bearing.** R-RULE-11 boundary; the 10 donor-ceremony drops remain dropped; ME-9 is the audit hook at the Step 5 commit.

### Sequencing constraints — necessity at the shape level

S-1 (HZ-03 — in-flight PRD precondition), S-2 (HZ-06 + HZ-07 — CLI runtime atomicity), and S-3 (HZ-14 — Makefile sync-rule atomicity) are correctly *shaped*. Operational fragility is addressed in §§ 7–8 below.

---

## 3. Empirical exposure — 96 in-flight MDTM task files

<!-- Source: V3 § 2 (in-flight MDTM enumeration, live grep evidence) -->

Live grep across `.dev/tasks/` returns the following empirical exposure:

| Pattern | Files |
|---|---|
| `/sc:task` OR `sc-task-protocol` OR `task-unified` (union) | **96** |
| `/sc:task` | 92 |
| `sc-task-protocol` | 8 |
| `task-unified` | 30 |

The named S-1 precondition target — `TASK-PRD-20260514-121039` — has `status: "🟠 Doing"` and emits **149+ references to `/sc:task`** across its subtree: `research/01-features-and-user-flows.md` (36), `synthesis/synth-01-features-ux.md` (37), `research/02-architecture-and-integration.md` (19), the task file itself (21), `research-notes.md` (9). The PRD's subagent prompts explicitly name PRIMARY ARTIFACTS including `src/superclaude/commands/task.md` and `src/superclaude/skills/sc-task-protocol/SKILL.md` — files CR-DEP-01 stubifies and CR-DEP-03 hard-deletes.

Other in-flight tasks referencing deprecation surfaces: `TASK-TDD-20260514-121250` (invariant-preservation research), `TASK-RF-20260515-195758` (git-history audit), `TASK-RF-20260403-tasklist-e2e`, `TASK-RESEARCH-20260403-sprint-task-exec`. None carry a `Tier:` frontmatter field today; under CR-FM-03 they default to `STANDARD` at resume.

**Implication.** The plan's "NO migration" promise (source line 214) and the "INV-04 SURVIVES" claim (source line 86) are auditable only at the *parse layer*. At the *semantic layer*, 96 files contain checklist-level references to deprecated surfaces that CR-FM-03's "validates clean" check does not see. This is the load-bearing finding for INV-04 in this validation.

---

## 4. INV-04 — parse-level vs semantic-level resumability

<!-- Source: V3 § 7 + V2 § 2.3 (parse-vs-semantic restructure) -->

The plan asserts INV-04 SURVIVES (source line 86) on three grounds: CR-FM-03 compat shim, TU-5 baseline YAML on disk, TU-8 incident-report file on disk, task-log lines append-only. This holds at the *schema layer* — every existing TASK-* file parses cleanly under the merged surface.

At the *semantic layer*, three exposures survive:

1. **Content-level deprecated-surface references (96 files).** A resumed task whose checklist text reads "spawn `/sc:task` for the next item" or "follow `sc-task-protocol` Phase 3" hits a stubified command (CR-DEP-01) or a deleted skill (CR-DEP-03). CR-FM-03 detects the parse, not the content. The task transitions to `⚪ Blocked` per its own exception clauses (if any exist); INV-01 holds by transition; INV-04 is technically satisfied (the task is "resumable") but the *meaningful resume path is dead*.
2. **Default-STANDARD strips implicit STRICT.** Many in-flight checklists embed STRICT-equivalent obligations ("spawn rf-qa here", "halt on test regression") that pre-date the formal `Tier:` field. Defaulting to STANDARD silently downgrades those checklist items; INV-03 holds at the skill layer but the task's checklist layer loses precedence.
3. **CR-FM-03 shim has no sunset binding.** A future audit row that drops the default-fall-through bricks every TASK-* file authored under the shim. The shim's lifetime is unbounded; the plan does not bind a sunset condition.

**Closure obligation.** Extend CR-FM-03 with a content-level audit at resume time: `grep -E "(/sc:task\b|sc-task-protocol|task-unified)"` against the task body; on match, emit `gate-1.5: legacy-surface-reference detected file=<path> action=warn-and-continue surface=<symbol>` and route the resume through a one-shot acknowledgment gate. The HALT disposition MUST be warn-and-continue per ME-3 (refuse-entry would weaken INV-01). This is **AC-ATK-18**.

Add a shim sunset audit row CR-AUDIT-FM-03-SUNSET declaring CR-FM-03 binding for at least N task generations or until an explicit migration row lands.

---

## 5. CR-TASK-* attacks — predicate precision

<!-- Source: V2 § 3 (CR-TASK-* attacks) + V1 R2 (F-03 asymmetry distinction) -->

### 5.1 CR-TASK-01 / CR-TASK-04 sentinel comments (source lines 118, 215, 218)

**Attack.** The sentinel `# CR-7 ORDERING — load-bearing: path_override_check FIRST. Do not reorder.` is a markdown comment in `SKILL.md`. Markdown comments are not load-bearing to any interpreter — they are documentation. The "ordering" is procedural, not enforced. The CR-FM-04 grep checks for the comment string's presence, not for any operational effect.

**Closure obligation.** Either (a) move the load-bearing ordering into an executable artifact (pytest fixture, YAML schema, JSON ordering manifest) and grep that; or (b) downgrade the sentinel claim from "binding" (source line 118) to "informational" and remove the F-02 MEDIUM-severity closure status. **AC-ATK-13.**

### 5.2 CR-TASK-02 task-level malform — input-invalid vs environment-non-ideal

**Attack as originally framed (V2 § 3.2).** "Malformed `Tier:` rejected" is a HALT at pre-loop entry. F-03 forbids new HALT semantics on dirty-tree (an environmental condition). Why is parse-rejection allowed to halt when git-dirty is not?

**Asymmetry resolution (V1 R2).** CR-TASK-02 is a *parse-error* HALT (the task file is structurally invalid input). Git-dirty is an *environmental* condition (the task file is valid; surrounding state is not ideal). Different categories: invalid-input vs valid-input-under-non-ideal-conditions. The asymmetry is justified.

**Closure obligation.** A unified pre-loop HALT policy table with two row categories: (a) input-invalid → HALT; (b) environment-non-ideal → WARN-CONTINUE. Every new pre-flight condition maps to one row. **AC-ATK-10** (amended).

### 5.3 CR-TASK-03 per-item marker (source lines 217, 102–105)

**Attack.** "Tier-conditioned reads only" is a phrase, not a test. No enumerable list of tier-conditioned reads exists. The closure relies on ME-1 design-time review, not a runtime guard.

**Closure obligation.** A closed enumeration of authorized per-item marker consumers (current list = {CR-TASK-07 baseline-skip}); any new consumer requires a new manifest exception, audited at the row level. **AC-ATK-05.**

### 5.4 CR-TASK-06 git_status — three failure modes, one named (source lines 124–134)

**Attack.** F-03 closes only `git_status=dirty`. Three other states are unspecified: (i) `git` not installed (exit 127); (ii) directory is not a git repo (`git status` exits non-zero); (iii) `git status` hangs (large repo / filesystem lock / NFS).

**Closure obligation.** A five-row matrix for `git_status`: {clean, dirty, tool-absent, not-a-repo, error-other} × {emit Task Log line, action}. All five rows bound; action ∈ {WARN-CONTINUE, GRACEFUL-SKIP}; no HALT (per ME-3). **AC-ATK-02.**

### 5.5 CR-TASK-07 / CR-TASK-09 baseline trinary (source lines 138–148)

**Attack.** AC-CR-TASK-09-F04 collapses three distinct on-disk states — `absent` (no file), `empty` (zero bytes), `malformed` (YAML parse error or schema violation) — into one log token. These states are observable at different layers; observer order determines the classification. A file containing `null` parses to an empty Python object — is that `empty` or `malformed`?

**Closure obligation.** A four-state table {absent, empty, parse-fail, schema-fail} with the specific observation tool named for each (`os.path.exists` → `os.path.getsize` → `yaml.safe_load` → `<schema>`). Observation order pinned. Disposition for each state: classification=new in all four cases (over-escalate per F-04). **AC-ATK-03.**

### 5.6 CR-TASK-08 prohibitions catalog (source line 234)

**Attack.** "F1 continues" — unspecified behavior when a prohibition fires inside a verifier subagent context (mid-phase rf-qa invocation per F-05). Halt verifier? Continue verifier but halt parent? Continue both?

**Closure obligation.** Prohibition disposition matrix across {root F1, verifier-spawned F1, mid-phase rf-qa context}. **AC-ATK (new — incorporated in AC-ATK-11 generalization).**

### 5.7 CR-TASK-09 mid-phase INV-03 widening — precedent risk

**Attack.** § 0 of the source plan declares the mid-phase invocation "authorized INV-03 surface extension" with three justifications: (a) routes to existing identity, (b) uses existing spawn pattern, (c) named by TU-7. Each of (a)/(b)/(c) is satisfied by *any* future widening that reuses rf-qa identity and the `SKILL.md:191-198` spawn pattern. The closure establishes a paragraph-level surface-widening precedent procedurally lower-cost than authoring a manifest exception. Obligation #7 (source line 425) does not retroactively bind the F-05 author's own pattern.

**Closure obligation.** Either (a) F-05 itself must be backed by a retroactive manifest exception (ME-10) named in the manifest, or (b) the plan must explicitly note that § 0 mid-phase routing was authorized under a one-time procedural carve-out that does NOT generalize. **AC-ATK-11.**

### 5.8 CR-TASK-10 incident-report seven-field schema (source line 236)

**Attack.** "Seven-field schema" — the seven field names are not enumerated. A resumed task that reads an older incident file with a different field count sees undefined behavior.

**Closure obligation.** Enumerate the seven field names and types; bind a schema file check in CR-FM-04 audits. **AC-ATK-12 (combined).**

### 5.9 CR-TASK-11 md5sum (source line 242) — LOW severity

**Attack.** `md5sum` is collision-vulnerable. Defeats audit's evidentiary value for adversarial scenarios; negligible for accidental collision.

**Closure obligation.** Replace md5sum with sha256sum in CR-TASK-11 / CR-DEP-02 / CR-DIST-02 audits — mechanical change. **AC-ATK-09 (demoted to LOW).**

### 5.10 CR-TASK-12 seven-diff fragility post-CR-DEP-03 (source lines 244, 254, 367, 422)

**Attack.** CR-TASK-12 runs six verbatim diffs against donor strings (source line 244). After CR-DEP-03 (source line 253), the donor file is hard-deleted. The six diffs target a non-existent file post-Step-6. The audit cannot re-fire after Step 6.

**Closure obligation.** Either (a) snapshot the donor strings into a frozen test fixture (e.g., `tests/fixtures/donor-blocks/`) before Step 6 and re-run diffs against the fixture; or (b) explicitly mark CR-TASK-12 as Step-4-only with an obligation to re-author a successor audit at Step 6. **AC-ATK-06.**

---

## 6. CR-DEP-* / CR-DIST-* / CR-REF-* / CR-DOC-* attacks — traceability and disambiguation

<!-- Source: V2 §§ 4–5 (verbatim adoption) -->

### 6.1 CR-DEP-03 procedural authorization chain — no verifier role bound (source lines 174–188, 253)

**Attack.** The F-07 chain — sprint goal → T06.03 → § 2 rubric → § 4 traceability → structural precondition — names document references but no **role** that signs off on the hard-deletion. INV-03 binds rf-qa as a role; F-07 binds a paper trail.

**Closure obligation.** Name a verifier role (rebind `rf-qa` as the F-07 chain-integrity verifier). The role spawns at Step 6 pre-commit and confirms chain links are intact. **AC-ATK-07.**

### 6.2 S-1 PRD precondition — no time-bounded abort (source lines 319–325, 373)

**Attack.** S-1 requires TASK-PRD-20260514-121039 to complete before Step 5. "Infeasible" is undefined; no time-bounded abort. If PRD stalls indefinitely, Step 5 is soft-blocked.

**Closure obligation.** Step 5 pre-condition extends to: (a) `--max-wait` (e.g., 14 days) past which option (b) snapshot auto-invokes with merge-message annotation; (b) require PRD final commit to embed pinned git-SHA refs at every `[CODE-VERIFIED]` tag; (c) extend CR-DEP-05 grep to flag post-Step-5 docs asserting `[CODE-VERIFIED]` against the stubified body. **AC-ATK-08** (V3-enhanced).

### 6.3 CR-DEP-04 / CR-DEP-05 — gate-point and grep-scope ambiguity

**Attack.** CR-DEP-04 "directory absence" does not specify gate point; CR-DEP-05 grep does not specify file extensions, excluded paths, or hidden directories.

**Closure obligation.** Specify gate point in Step 6 pre-commit; explicit `find` / `grep` invocation with scope flags. **AC-ATK-14.**

### 6.4 Bucket-condensation 79 → 65 unenumerated (source line 69)

**Attack.** § 2.2 reports "79 rows including bucket sub-IDs, condensed into 65 distinct CR-IDs." 14 + 2 + 5 + 39 + 6 + 13 = 79 is asserted on source line 69 but the inverse mapping is absent. AC #1 traceability promise is defeated.

**Closure obligation.** A condensation table: 79 row-instances → 65 CR-IDs with the bucket sub-row mapping enumerated. **AC-ATK-04.**

### 6.5 67 vs 65 mismatch — duplicate CR-IDs unnamed (source lines 17, 28, 36, 69)

**Attack.** Source line 17 says "67 row-line-items / 65 distinct CR-IDs"; source line 36 asserts PASS over 67 rows. The two extra rows (67 − 65 = 2) are not named.

**Closure obligation.** Name the two row-line-items that share a CR-ID; state which row carries PASS verdict (or whether both do and what the duplication means). **AC-ATK-04 (extended).**

### 6.6 CR-DOC-01 Step 5 vs Step 8 ambiguity (source lines 375, 397)

**Attack.** CR-DOC-01 is listed as atomic with Step 5 AND as fallback in Step 8 ("if not landed in Step 5"). Disambiguation rule missing.

**Closure obligation.** Binding disposition: CR-DOC-01 MUST land in Step 5; Step 8 is the fallback only if Step 5's pre-commit gate fails AND a hot-fix is authorized. **AC-ATK-15.**

### 6.7 CR-DOC-13 R-RULE-11 audit scope (source line 411)

**Attack.** "Final audit row over CR-DOC-01..12" — but R-RULE-11 spans ALL 65 CR-IDs, not just CR-DOC-*. Audit under-cast.

**Closure obligation.** Either rename CR-DOC-13 to a scoped doc-only audit, or widen scope to all 65. **AC-ATK-14 (companion).**

### 6.8 CR-REF-18 cluster root unnamed (source line 295)

**Attack.** "`DEPRECATION-NOTE.md` exists at cluster root" — cluster root unnamed.

**Closure obligation.** Name the cluster root path explicitly. **AC-ATK-14 (companion).**

---

## 7. Sequencing-constraint probes (S-1, S-2, S-3) — timeline-layer hazards

<!-- Source: V3 §§ 3–5 (sequencing constraint probes + operational mitigations) -->

### 7.1 S-1 PRD-precondition probe (deep)

The plan-level fix in § 6.2 above closes the predicate ambiguity. Operationally, three hazard classes survive:

- **PRD stalls 30+ days in `🟠 Doing`.** No time-bounded abort; ship pressure produces unilateral invocation of option (b) without decision record. **Mitigation:** `--max-wait` 14d default.
- **PRD abandoned.** No row in § 6 names disposition for abandoned PRDs. **Mitigation:** `--max-wait` plus a named abandonment authority.
- **PRD completes but outputs cite deleted surfaces.** PRD deliverable carries `[CODE-VERIFIED]` tags pinned to `task.md`, `SKILL.md`, `COMMANDS.md:86-119`, `ORCHESTRATOR.md:151-213`. After Step 5 all four mutate or vanish. **Mitigation:** pinned-git-SHA disclaimer at every `[CODE-VERIFIED]` tag; extend CR-DEP-05 grep to flag post-Step-5 docs asserting verification against the stubified body.

### 7.2 S-2 atomic-commit probe (rebase-split bypass)

**Hazard.** Pre-commit pytest gate runs on `git commit`, **not on rebase**. `git rebase -i` permits commit-split. A rebase that splits Step 5 into "CR-DEP-01 only" + "everything else" creates a transient broken state. If pushed (force-push to a feature branch the merge-sprint executor later reads), that SHA becomes a bisection landing point with broken runtime.

**Concrete sequence.** Author commits Step 5 atomically. Reviewer requests CR-DOC-01 wording tweak. Author runs `git rebase -i HEAD~3` + `edit`, amends, splits with `git reset HEAD^ && git add -p`. Intermediate state passes pre-commit gate (working tree still carries unstaged CR-REF-01). Split intermediate commit lands and is pushed. Master then carries one SHA where `/sc:task` is stubified but `sprint/process.py` still emits `/sc:task`. Any sprint run or bisection pinned to that SHA dies.

**Mitigation.** § 7 obligation #3 of the source plan extends: add a **structural barrier** — server-side pre-push hook (or CI check) that re-greps `/sc:task\b` against `src/superclaude/cli/` **on the commit landing at master**, not the working tree, and rejects the push if grep matches AND the same commit does not also delete the donor `task.md` body. Binds the six rows at the merge-policy layer. **AC-ATK-17.**

### 7.3 S-3 sync-rule probe (worktree race)

**Hazard.** CLAUDE.md authorizes parallel sessions via `git worktree`. Session A on `feat/task-merge` runs `make sync-dev` at T+0; Session B on `feat/other-feature` (worktree per CLAUDE.md) writes `.claude/skills/sc-task-protocol-experimental/` at T+0.1. The prune loop enumerated at T+0 includes that directory and deletes it at T+0.2. Session B loses uncommitted work; `verify-sync` in B's tree fails on next run.

**Mitigation.** § 7 obligation #1 of the source plan extends: require `flock` on `.claude/skills/` during prune, and a post-prune `find -type d` diff against the expected directory set. **AC-ATK-16.**

---

## 8. Post-CR-DEP-03 residual-reference probe — CR-DEP-06 proposal

<!-- Source: V3 § 6 (CR-DEP-06 residual-reference manifest) -->

After CR-DEP-03 hard-deletes the donor SKILL.md, residuals survive that the plan's audits do not scope:

- **CR-TASK-12 seven-diff audit** (source lines 367, 422) runs **before** Step 6 deletion. Scripts source-controlled; future re-run post-deletion errors rather than passing clean. Audit should be **single-use** and snapshot-frozen (see § 5.10).
- **CR-REF-BUCKET-A, C, D, E, F, G, H** are "leave-as-is" per Step 9 (source line 405). Archived debate / refactor / analysis files may retain `/sc:task` strings. CR-DEP-05 and CR-REF-12 grep audits scope to `[src]` and `[.claude]`, not to `.dev/releases/backlog/` or bucket archive. A future auto-rewriter could "fix" archived text against a deleted surface.
- **`docs/generated/*`.** Step 10 (source line 409) defers regeneration. Between Step 6 and the next regenerator run, generated docs describe `/sc:task` as live without a frozen-pre-merge banner.

**Mitigation.** Add **CR-DEP-06** — a one-shot post-Step-6 grep that emits a structured manifest of every surviving deprecation-surface string outside authorized leave-as-is buckets, with per-string disposition. **AC-ATK-18 (companion).**

---

## 9. INV-01..INV-05 attack vectors — merged table

<!-- Source: V2 § 6 (attack vector table) + V3 § 9 (invariant corrections) -->

| Invariant | Closure clause leaned on | Attack | V3 augmentation |
|---|---|---|---|
| INV-01 (F1 loop semantics) | F-03 dirty-tree warn-continue (source line 130); F-02 sentinel comments (source line 118) | § 5.4 unspecified git failure modes; § 5.1 markdown comments cannot enforce executable ordering | F-03 input-invalid vs environment-non-ideal asymmetry distinction resolves; AC-ATK-02 binds 5-row matrix |
| INV-02 (Prohibited-actions F2) | TU-6 "reinforces F2" (source line 84) | § 5.6 disposition unspecified for verifier-spawned and mid-phase rf-qa contexts | — |
| INV-03 (Phase-gate rf-qa) | F-05 "authorized widening" (source lines 25–26) | § 5.7 establishes paragraph-level surface-widening precedent obligation #7 does not retroactively bind | SKILL.md:191-198 line-anchor brittle; extend CR-FM-04 to anchor that block |
| INV-04 (Resumability) | CR-FM-03 shim, TU-5 baseline, TU-8 incident (source line 86) | § 4 shim has no sunset binding; § 5.8 incident schema unspecified; § 5.4 git-failure-mode divergence | **HIGHEST EXPOSURE:** 96 in-flight files contain content-level deprecated-surface references CR-FM-03 does not see |
| INV-05 (Refusal-of-definition) | "TU-1 Tier: is metadata, not work-definition" (source line 87) | § 5.3 per-item marker consumer list open; CR-FM-01 closed-enum normalization rules unspecified | — |

---

## 10. Concrete attack scenarios — predicate-layer + timeline-layer

<!-- Source: V2 § 7 (A..G) + V3 § 8 (H-1..H-4) — merged scenario register -->

### Predicate-layer scenarios (V2)

**Scenario A — CR-FM-04 grep false positive (INV-01).** `[src]/skills/task/SKILL.md` contains the three function calls in WRONG order at the row 1 site (`tier_field_validate(); path_override_check(); gate_1_dispatch()`), but a docstring 200 lines earlier reads "the canonical order is `path_override_check`, `tier_field_validate`, `gate_1_dispatch`." Action: run the F-02 grep. Result: grep returns the three names in correct line order (docstring fires first). Commit gate passes. Broken code lands. **Invariant broken:** INV-01.

**Scenario B — `git` not installed on CI worker (INV-01, INV-04).** CI worker image has `git` removed. STRICT pre-flight runs `git_status_clean_tree_check`. Action: subprocess `git status` exits 127. State after: F-03 closure handles only `git_status=dirty`; the 127 exit is undefined. Implementer A treats as graceful-skip; implementer B treats as HALT. **Invariant broken:** INV-01 if HALT; INV-04 if two CI runtimes diverge.

**Scenario C — baseline file contains `null` (INV-03).** `research/test-baseline.yaml` exists, 5 bytes, content `null\n`. Action: AC-CR-TASK-09-F04 fires. Observer 1 (`yaml.safe_load` → `None`) calls it `empty`; Observer 2 (`os.path.getsize` → 5) calls it not-empty. State after: closure logs `reason=empty` OR `reason=malformed` depending on observer order. **Invariant broken:** INV-03 (floor preserved but content non-deterministic).

**Scenario D — CR-TASK-12 audit after CR-DEP-03 (INV-01).** Step 4 ran; seven-diff audit passed. Step 6 lands CR-DEP-03; donor file hard-deleted. Step 7 introduces a regression in row 1 ordering. Re-run of CR-TASK-12 attempted. State after: six of seven diffs error on missing donor file. Regression lands undetected. **Invariant broken:** INV-01.

**Scenario E — Per-item marker with no consumer (INV-05).** Future contributor adds a new behavior `verbose_logging` gated by per-item `(Tier: STRICT)`. ME-1 review procedural, design-time review skipped. Action: per-item marker drives new consumer not in F-01 negative list and not in any positive list. State after: New consumer ships; ME-1 audit gate does not retroactively flag it. **Invariant broken:** INV-05.

**Scenario F — S-1 unbounded wait (operational, not invariant).** TASK-PRD-20260514-121039 stalls 30 days. Step 5 blocked per S-1. No deadline triggers options (b) or (c). Whole merge sequence frozen. **Invariant broken:** none directly; AC #3 binding effectiveness eroded.

**Scenario G — md5 collision in CR-TASK-11 (R-RULE-10).** Adversarial commit crafts `[.claude]` mirror with same md5 as `[src]` original but different content. CR-TASK-11 audit passes; `make verify-sync` returns 0. Runtime reads `[.claude]` and behaves differently from `[src]`. **Invariant broken:** INV-04 indirectly.

### Timeline-layer scenarios (V3)

**Scenario H-1 — PRD stalls; merge bypassed.** Day 0: PRD `🟠 Doing`. Day 14: 2/4 research subagents complete; analyst blocked on a research-gate question. Day 28: deprecation ship pressure; reviewer invokes S-1 option (b) "snapshot." Day 30: Step 5 lands. Remaining subagent reads stubified `task.md` and emits `[CODE-CONTRADICTED]` tags; PRD findings become self-contradictory. INV-04 holds (file parses); deliverable is corrupted. **Invariant broken:** AC #3 + PRD output integrity.

**Scenario H-2 — Rebase splits Step 5.** Author commits Step 5 atomically. Reviewer requests CR-DOC-01 wording tweak. Author runs `git rebase -i HEAD~3` + `edit`, amends, splits commit. Intermediate state passes pre-commit gate. Split intermediate commit lands and is pushed. Master carries one SHA where `/sc:task` is stubified but `sprint/process.py` still emits `/sc:task`. Any sprint run pinned to that SHA is dead. **Invariant broken:** S-2 atomicity assertion.

**Scenario H-3 — Worktree race during sync-dev prune.** Session A on `feat/task-merge` runs `make sync-dev` at T+0. Session B on `feat/other-feature` (worktree per CLAUDE.md) writes `.claude/skills/sc-task-protocol-experimental/` at T+0.1. Prune loop enumerated at T+0 includes that directory and deletes it at T+0.2. Session B loses uncommitted work; `verify-sync` in B's tree fails. **Invariant broken:** R-RULE-10 source-of-truth discipline operationally.

**Scenario H-4 — Resumed task hits deleted PRIMARY ARTIFACT.** TASK-RESEARCH-20260403-sprint-task-exec research subagent prompt names `src/superclaude/skills/sc-task-protocol/SKILL.md` as PRIMARY ARTIFACT. Pre-merge: parked at checklist item 7/14. Post-CR-DEP-03: resumed. CR-FM-03 validates clean. Subagent spawned at item 8 fails `Read` on the deleted file. Task transitions to `⚪ Blocked`. INV-01 holds by transition; INV-04 *technically* satisfied (resumable) but meaningful resume path is dead. **Invariant broken:** INV-04 semantic guarantee.

---

## 11. Consolidated acceptance criteria

<!-- Source: V2 § 8 (AC-ATK-01..15) + V3 § 10 mitigations (AC-ATK-16..18) + V1 § 7 (AC-SM-01..12) -->

### 11.1 Gap-closure acceptance criteria (AC-ATK-01..18) — what the plan MUST add

| AC | Closure obligation |
|---|---|
| **AC-ATK-01** | Replace F-02 alternation grep with line-range-pinned or AST-level check that verifies call-site order |
| **AC-ATK-02** | Five-row matrix for `git status` failure modes (clean / dirty / tool-absent / not-a-repo / error-other) bound to CR-TASK-06 |
| **AC-ATK-03** | Disambiguate baseline trinary into four states {absent, empty, parse-fail, schema-fail} with observation order pinned |
| **AC-ATK-04** | Enumerate 79 → 65 condensation table; name the 2 duplicate CR-IDs in the 67-row PASS roll-up |
| **AC-ATK-05** | Closed enumeration of authorized per-item marker consumers; new consumers require new manifest exception |
| **AC-ATK-06** | Snapshot donor strings into frozen fixture before Step 6 OR mark CR-TASK-12 Step-4-only with successor-audit obligation |
| **AC-ATK-07** | Add verifier role (rebind `rf-qa`) to F-07 procedural authorization chain; spawn at Step 6 pre-commit |
| **AC-ATK-08** | S-1 enhanced: `--max-wait` 14d default + auto-invoke option (b) + pinned git-SHA at every `[CODE-VERIFIED]` tag + CR-DEP-05 grep extension |
| **AC-ATK-09** | Replace md5sum with sha256sum in CR-TASK-11 / CR-DEP-02 / CR-DIST-02 audits (LOW severity, mechanical) |
| **AC-ATK-10** | Unified pre-loop HALT policy table with input-invalid vs environment-non-ideal row categories |
| **AC-ATK-11** | F-05 either backed by retroactive ME-10 or explicitly marked as one-time non-generalizing carve-out |
| **AC-ATK-12** | Bind CR-FM-03 shim lifetime (sunset audit row); enumerate CR-TASK-10 seven fields; bind CR-FM-01 canonicalization table |
| **AC-ATK-13** | Either move CR-7 / CR-8 ordering into executable artifact OR downgrade sentinel claim from "binding" to "informational" |
| **AC-ATK-14** | Specify CR-DEP-05 grep scope, CR-REF-18 cluster root path, CR-DEP-04 gate point |
| **AC-ATK-15** | CR-DOC-01 Step 5 vs Step 8 disambiguation: MUST in Step 5; Step 8 fallback only on Step-5 pre-commit-gate failure |
| **AC-ATK-16** (V3) | `flock` discipline on `.claude/skills/` during `make sync-dev` prune; post-prune dir-diff |
| **AC-ATK-17** (V3) | Server-side pre-push hook re-grepping landing commit (not working tree) for `/sc:task` in CLI sources |
| **AC-ATK-18** (V3) | Extend CR-FM-03 with content-level audit at resume time + warn-and-continue HALT disposition + one-shot ack gate; add CR-DEP-06 residual-reference manifest |

### 11.2 Positive-validation acceptance criteria (AC-SM-01..12) — what the steelman validates

| AC | Testable claim | Validation method |
|---|---|---|
| AC-SM-01 | All eight V/C/K verdicts (TU-1..TU-8) match `transfer-manifest.md` § 4 byte-for-byte | Diff TU-row table at source lines 54–63 against manifest § 4 |
| AC-SM-02 | Each ME-1..ME-9 traces to ≥1 CR-row acceptance-criterion or sequencing constraint | Cross-grep ME-N against § 5 row text and § 6 constraint text |
| AC-SM-03 | `invariant-survival-walkthrough.md` worked example demonstrates INV-01..INV-05 survive on the merged surface | Independent re-read of walkthrough § 2 + § 3 |
| AC-SM-04 | F-01..F-08 each cite a re-readable Phase 7 artifact line range | Grep § 4 dispositions for Phase 7 artifact references |
| AC-SM-05 | S-1..S-3 each cite a named hazard (HZ-NN) in `compat-hazard-report.md` | Grep § 6 for HZ-03, HZ-06, HZ-07, HZ-14 |
| AC-SM-06 | 67-row count and 10-step commit sequence unchanged from `merge-master.md` § 1 + § 6 | Row-count + step-count checks |
| AC-SM-07 | CR-FM-04 ordering greps return three function names in expected order against `[src] skills/task/SKILL.md` | Execute the two greps at source lines 116–117, 243 |
| AC-SM-08 | CR-TASK-12 returns 7 zero-diff invocations (6 donor strings + 1 sentinel-comment block) | Execute the seven diffs after Step 1 lands |
| AC-SM-09 | Step 5 commit contains exactly the rows named at source line 375 | Inspect merge commit file list |
| AC-SM-10 | Step 6 commit contains exactly the rows named at source line 381 | Inspect merge commit file list |
| AC-SM-11 | Zero ledger entries from `rejected-features-ledger.md` re-proposed across the 65 distinct CR-IDs | Cross-grep ledger CR-IDs against § 5 |
| AC-SM-12 | Pre-commit gates for Steps 1, 5, 6 all return 0 on clean checkout | Execute the gates at source lines 351, 377, 387 |

---

## 12. Unnamed tradeoffs — eight closures, eight costs

<!-- Source: V2 § 9 (tradeoffs the plan does not name) -->

- **F-01 closure tradeoff.** Naming the consumption shape "tier-conditioned read" widens INV-05 attack surface by making "read" semantically open-ended. Cost of closing F-01 is implicit grant of unbounded read channel.
- **F-02 closure tradeoff.** Two greps + sentinel comment shifts enforcement from structural ordering to documentation discipline. If SKILL.md is auto-generated by any future tool, sentinel comments could be stripped without triggering grep — because function names remain in source order. Coupling between audit tool and source-file editing toolchain is unbound.
- **F-03 closure tradeoff.** Reading A (warn-and-continue) preserves INV-01 but exposes the runtime to dirty-tree-induced behavior divergence in downstream commits. A warned-and-continued dirty tree could land partial state into the merge sequence.
- **F-04 closure tradeoff.** Over-escalate floods the rf-qa queue. Plan notes "possibly-noisier escalation queue" but does not specify when "noisy" becomes a refusal trigger.
- **F-05 closure tradeoff.** Mid-phase rf-qa routing means the verifier sees in-progress state instead of phase-complete state. Reuses spawn pattern but does not address the semantic shift: rf-qa was designed to verify completed work, not adjudicate in-flight escalations.
- **F-06 closure tradeoff.** Citing `extension-point-contracts.md:11-17` means line-pinned reference is brittle to any edit. Formatting commit adding one line above the anchor block silently breaks the citation.
- **F-07 closure tradeoff.** Procedural authorization without verifier role means chain is auditable only by humans reading linked docs. Automation cannot enforce it. CR-DEP-03's irreversibility (hard-delete) compounds the cost.
- **F-08 closure tradeoff.** Correcting "five" to "six" is mechanical, but does not audit downstream references to "five" in other Phase 6 artifacts (`merge-master.md:7` still says "five"). Inconsistency persists in chain of trust.

---

## 13. Failure-mode coverage gaps — beyond HZ-01..HZ-18

<!-- Source: V2 § 10 (failure modes orthogonal to row-level mitigations) -->

- **FM-01 (filesystem).** `make verify-sync` returns 0 on successful sync but does not check for symlink divergence between `[src]` and `[.claude]`. If `[.claude]` is symlinked to `[src]` (defeats R-RULE-10), md5sum / sha256sum / content checks pass trivially.
- **FM-02 (timing).** Step 5 atomic across six rows. If any pytest invocation flakes intermittently, atomicity guarantee creates a no-progress state where commit cannot land but soft-deprecation has been authored locally. Rollback policy unspecified.
- **FM-03 (concurrent edits).** Two implementation sub-agents running in parallel could land conflicting edits to SKILL.md at row 1 vs row 10. Atomic-merge obligation is at commit level, not edit level.
- **FM-04 (CI / local divergence).** `uv run pytest` on local machine and on CI may surface different results if env vars differ (`PYTHONHASHSEED`, locale, timezone). Pre-commit gate does not pin env.
- **FM-05 (mkdocs build).** Step 8 gate is `mkdocs build` returns 0 broken-link warnings. mkdocs version not pinned. Version upgrade changing broken-link semantics could pass or fail same source tree.
- **FM-06 (deferred regen).** Step 10 commits with "docs/generated/*: refresh deferred to next regenerator run." Next regenerator run unscheduled. If it never runs, `docs/generated/*` permanently disagrees with `docs/` source.
- **FM-07 (encoding).** None of the greps specify text encoding. UTF-16-authored markdown silently passes every grep with no matches.
- **FM-08 (file rename).** Hard-deletion at CR-DEP-03 is via procedural chain. If donor file renamed (e.g., `*.deprecated`) rather than deleted, absence check passes but file persists. R-RULE-11 violation indirect.

---

## 14. Evidence-completeness audit — plan's own validation hooks (§ 9)

<!-- Source: V2 § 11 (EC-01..04) -->

- **EC-01.** Source line 447 says "Grepping § 4 for each F-01..F-08 disposition." Grep pattern unspecified. Reviewer using `grep -n "F-0"` vs `grep -n "F-01"` vs `grep -n "F-[0-9][0-9]"` gets different results.
- **EC-02.** Source line 449 says "Confirming § 5 carries the same 67 row-line-items as `merge-master.md` § 1." Comparison method unspecified — diff, manual count, hash? With four row-deltas, textual diff returns non-zero by design.
- **EC-03.** Source line 450 says "V/C/K verdicts carried forward unchanged." Carry-forward asserted; no audit step re-derives V/C/K. R-RULE-07 requires re-scoring on drift; plan claims zero drift but no-drift claim itself unaudited.
- **EC-04.** Source line 452 says "the reviewer recomputes a sample of the no-drift V/C/K assessments by picking 3 TUs." Three of eight = 37.5% sample. Sample-based audit cannot rule out a single drifted TU among unsampled five.

---

## 15. Residual risks — honest concessions from the defense side

<!-- Source: V1 § 6 (5 honest concessions; preserved verbatim with attribution) -->

The steelman acknowledges five places where the defense cannot fully cover the attacks. These are entry points downstream reviewers should re-read:

1. **The "tier-conditioned read" boundary is conceptually thin.** Plan acknowledges this (source line 97) and bounds with ME-1 + acceptance-criterion language, but a sufficiently determined refactor could describe a forbidden per-item dispatch as a "read" if it routes through a wrapper. Defense relies on R-RULE-11 audit discipline at design-time — human-process, not structural.
2. **The third rf-qa invocation point (F-05) widens INV-03's surface beyond the canonical anchor language.** Plan calls this "authorized" and documents three-prong defense, but anchor source (`extension-point-contracts.md:11-17`) was not amended to mention mid-phase routing. Authorization lives in this plan, not in the anchor.
3. **F-04 over-escalation is a load-volume bet on rf-qa.** Classifying every failure as `new` when baseline is absent could flood the verifier queue. Plan does not bound upper limit on this routing volume.
4. **S-1's mitigation hierarchy (a / b / c) is recorded but not decided.** Source line 325 leaves the choice "at Phase 7 execution time." Late-discovered infeasibility of (a) means options (b) or (c) get chosen under time pressure.
5. **The procedural authorization chain (F-07) is "not a manifest binding."** Source line 186 explicitly says so. Future reviewer applying strict-manifest-only discipline could insist on retroactive amendment despite the chain being documented.

---

## 16. Synthesized verdict

<!-- Source: V1 § 7 + V2 § 12 + V3 § 11 (three-clause synthesis) -->

**Clause 1 (defense holds).** The source plan's eight closures resolve the Phase-7-named open findings. The V/C/K verdicts carry forward zero-drift. The ledger is not re-litigated. The 10-step canonical commit sequence has a defensible shape backed by three hazard-derived sequencing constraints. At the level the plan defines disposition, **PASS** is correctly returned.

**Clause 2 (predicate precision is under-specified).** Eighteen falsifiable gaps survive at the closure-predicate layer: F-02 grep occurrence-order vs call-site-order; F-03 git-status five-mode coverage; F-04 baseline four-state observer-disagreement; CR-TASK-12 post-CR-DEP-03 audit lifetime; 79 → 65 condensation arithmetic unenumerated; 67-vs-65 duplicate-CR-ID unnamed; F-05 paragraph-level surface-widening precedent; F-07 procedural chain without verifier role; CR-FM-03 shim sunset binding; CR-TASK-10 seven-field schema enumeration; CR-FM-01 canonicalization rules; sentinel-comment type confusion; CR-DEP-05 grep scope; CR-REF-18 cluster root path; CR-DOC-01 Step 5 vs Step 8 disambiguation; CR-DEP-04 gate-point; CR-TASK-08 prohibition disposition in widened surface; md5 → sha256. **AC-ATK-01..15** close these.

**Clause 3 (timeline-layer hazards survive).** Six operational hazards live at the merge timeline and tooling boundary the plan's row-level mitigations do not reach: PRD soft-block (H-1), rebase-split bypass (H-2), worktree race (H-3), 96-file in-flight semantic exposure (H-4), residual `/sc:task` references in leave-as-is buckets and `docs/generated/*` (post-CR-DEP-03 surface), deferred regenerator drift. **AC-ATK-16..18 + CR-DEP-06** close these.

**Three-clause verdict.** "ZERO OPEN FINDINGS" is true *at the level the plan defines findings* (closures resolved their named items), false *at the predicate-precision level* (18 falsifiable gaps), and partially-true *at the operational level* (6 timeline-layer hazards survive). The plan is **binding in the procedural sense** that downstream implementers have a documented paper trail. Upgrade to **binding in the strong operational sense** requires a Phase 7.5 patch addressing the consolidated AC list (§ 11). The 18 gap-closures and 3 timeline-layer mitigations are independent of each other and can be parallelized across the patch sprint.

**Phase 7.5 patch scope.** 21 changes (AC-ATK-01..18 + CR-DEP-06 + S-4 PRD timeout + S-5 rebase-ban). None re-open a rejected-ledger entry. None re-litigate a closed finding. All are additive to the binding shape of the source plan.

**Recommendation to downstream reviewers.** Treat the source plan as the **structural authority** for the merge (its 67-row table, 10-step sequence, TU/ME bindings) and treat this validation spec as the **predicate-precision and operational-hardening authority**. Both are required for a defect-free implementation sprint.
