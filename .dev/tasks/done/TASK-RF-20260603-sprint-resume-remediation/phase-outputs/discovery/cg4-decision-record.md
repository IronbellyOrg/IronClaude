# DECISION RECORD — CG-4 (sprint auto-resume partial-work gate)

**Status:** AWAITING OPERATOR RULING (`needs_human_decision: true`)
**Created:** 2026-06-03
**Driving audit:** `.dev/reflect/post-sprint-auto-resume-20260603003009/REPORT.md` (F-1; verdict `needs_human_decision: true`, promotion BLOCKED on strict-gate conditions 4 & 8)
**Spec corpus:** `.dev/brainstorms/20260602-sprint-auto-resume-default/{design.md, merged-requirements.md}`
**Source research (verbatim quotes):** `.dev/tasks/to-do/TASK-RF-20260603-sprint-resume-remediation/research/05-spec-cg4.md` §1–§5

> This record SURFACES a genuine spec self-contradiction and presents BOTH resolutions neutrally.
> The RECOMMENDED DEFAULT is a recommendation, **not** a decision. The executor MUST NOT adopt it
> automatically — the `RULING:` line stays blank until an operator decides. F-2/F-3/F-4 proceed
> regardless; only F-1 and the §7/§4(c)/FR-2.4 spec reconciliation wait on this ruling.

---

## QUESTION (binary)

Does bare `sprint run --yes` proceeding past **REPORTED-but-not-quarantined** partial work satisfy
FR-2.4(a) *"boundary half-finished work cleaned OR explicitly assessed-and-accepted"*?

This is a binary ruling. The two options are mutually exclusive on the `--yes`/CI path; the
interactive path is unaffected (an operator who sees the prompt and assents IS "assessed-and-accepted").

## AUTHORITY IN CONFLICT

| Passage | Exact target | What it says | Status |
|---------|--------------|--------------|--------|
| design §7 (happy path) | `design.md:292-296`, key line `design.md:293` | `report half-written T03.4 outputs (copy→.resume-quarantine-<ts>/ if opted in); passed=True` — quarantine opt-in, `passed=True` | **implemented** (`integrity.py:314` `return accept_suspect or report.validated_last`) |
| design §4(c) (hard-gate formula) | `design.md:184-187`, key line `design.md:186` | `passed = validated_last AND (no unresolved suspects) AND (partial work quarantined or accepted)` | NOT implemented (3rd conjunct absent from `_verdict`) |
| FR-2.4 (hard gate) | `merged-requirements.md:85-87` | resume MUST NOT proceed until (a) boundary half-finished work is cleaned or explicitly assessed-and-accepted, AND (b) last completed task doubly validated | (b) implemented; (a) bypassed on `--yes` |

**Both §7 and §4(c) cite FR-2.4 as their authority** — §4(c):184 says "(FR-2.4 — hard gate)" while
§7:293 enacts the soft "report + passed=True" reading. The spec contradicts itself about what
FR-2.4 *means* on the non-interactive path. This cannot be resolved in code alone (the
implementation already had to pick one — it picked §7); it needs an **authoritative operator ruling**.

## OPTIONS

### [ ] Option YES — §7 governs; F-1 is as-designed

- **Reading:** On `--yes`/CI, "printing the plan + the operator pre-authorizing via `--yes`" IS a
  form of acceptance. The resume engine re-runs the boundary task, so the half-written outputs are
  about to be overwritten anyway — quarantine is a courtesy, not a safety precondition.
- **Consequence for F-1:** F-1 downgrades to *as-designed* (REPORT.md:35 — "Necessary deviation +
  residual safety gap"). No gate tightening.
- **HARD PREREQUISITE:** the F-2 path-surfacing **MUST** land, so that "reported" is *meaningful* —
  today `--yes` proceeds without even printing the partial paths, so the operator's `--yes` is
  uninformed consent. YES is only defensible if the paths are shown.
- **Spec edits:**
  - `design.md:186` (§4(c)) — re-word the `(partial work quarantined or accepted)` conjunct to
    `(partial reported AND (quarantined OR --yes/assented))`.
  - `merged-requirements.md:85-87` (FR-2.4) — clarify that on the non-interactive path,
    "`--yes` + a printed partial-paths report" constitutes "explicitly assessed-and-accepted".
  - `design.md:293` (§7) — unchanged.
  - `integrity.py:314` `_verdict` — unchanged (already §7).
- **Downstream:** F-1 → closed as-designed (no gate change). F-2 → MANDATORY (the informedness fix;
  blocking for this option).

### [ ] Option NO — §4(c)/FR-2.4 govern; tighten the gate

- **Reading:** "Assessed-and-accepted" requires a *positive* disposition of the partial work —
  either it is quarantined (cleaned) or a human/flag explicitly accepts THAT SPECIFIC partial work.
  A blanket `--yes` (which exists for the *drift* prompt, NFR-4/FR-3.4) is NOT consent to proceed
  over un-cleaned partial work. Silent proceed defeats the "non-idempotent seam is suspect" thesis
  (`merged-requirements.md:30-33`).
- **Consequence for F-1:** F-1 is a genuine **safety gap** — the gate must change. On `--yes`/CI,
  partial work present ⇒ either auto-quarantine (clean) OR hard-STOP with `blocking_reasons` until
  the operator passes an explicit accept flag (e.g. `--accept-partial`).
- **Spec edits:**
  - `design.md:293` (§7) — replace the unconditional `passed=True` with
    `passed=True only if (partial quarantined OR --accept-partial)`.
  - `design.md:186` (§4(c)) — unchanged (already correct).
  - `merged-requirements.md:85-87` (FR-2.4) — unchanged (already correct).
  - `integrity.py:314` `_verdict` — ADD third conjunct + `--accept-partial` flag. **Code change is
    DEFERRED to F-1, which is conditional on this ruling — NOT implemented in this task.**
- **Downstream:** F-1 → fixed via gate tightening (follow-up task). F-2 → still wanted (visibility),
  but no longer the sole safety mechanism.

## RECOMMENDED DEFAULT (recommendation only — NOT a decision)

**YES + F-2-as-prerequisite.** Rationale (from `05-spec-cg4.md` §2 / REPORT.md:35-39):

1. The implementation already shipped §7, passed 9 in-band gates; the re-run-overwrites-the-boundary
   design makes half-written outputs transient by construction — quarantine value is low.
2. The report adjudicates F-1 as *"Necessary deviation + residual safety gap"* (REPORT.md:35), NOT a
   clean regression — *"The implementation resolved toward §7 and logged it → Necessary"* (:39). The
   residual gap it names is precisely *"paths not shown (see F-2)"* — the fix is F-2, not gate-tightening.
3. The honest blocker is informedness, not quarantine. Land F-2 and `--yes` becomes informed
   pre-consent — a reasonable reading of "assessed-and-accepted" for an unattended pipeline.
4. **NO-leaning counter-evidence (recorded for the operator):** on pure CI nobody reads the printed
   paths in real time, so "informed consent" is weaker than interactive. If the team weights
   non-idempotent-seam safety above CI-ergonomics, NO (`--accept-partial`, default STOP-on-partial
   under `--yes`) is the conservative choice.

## RULING

```
RULING: *YES + F-2-as-prerequisite (operator)   DATE: 06/02/2026   BY: Ryan W
```

> **EXECUTOR STATUS (2026-06-03, UPDATED):** `RULING: YES + F-2-as-prerequisite` — recorded by
> operator **Ryan W (2026-06-02)**. The executor has now applied the YES-branch Step 1.5 spec
> amendment: `design.md` §4(c) partial conjunct re-worded to
> `(partial reported AND (quarantined OR --yes/assented))`, and `merged-requirements.md` FR-2.4
> clarified that "`--yes` + a printed partial-paths report" == "explicitly assessed-and-accepted".
> §7 and `integrity.py:_verdict` are UNCHANGED (already §7). **F-1 = closed as-designed (no gate
> change)**; the F-2 prerequisite (partial-path surfacing) already LANDED in Phase 3. Handoff:
> `phase-outputs/plans/cg4-ruling.md` → `RULING: YES`. **Promotion strict-gate condition 8
> (needs_human_decision==false) is now CLEARED.**

## SECONDARY — F-4 sub-decision (smaller-scope, same family)

design §4(a) (`design.md:148-154`) narrowed AC-3 `:141-143` ("phase 2 tail double-validated first").
**Ruling needed:** on PHASE-granularity hard crash, MUST the gate reach into the prior completed
phase and double-validate its tail?

- **Report adjudication:** F-4 = Necessary deviation / coverage gap (REPORT.md:53-57).
- **Recommended:** YES — amend §4(a) + add the CG-3 test. (Unlike CG-4, F-4 has no `--yes`-gate
  ambiguity; it is a straightforward under-delivery of AC-3 and is remediated in Phase 4 of this task.)

```
F-4 SUB-RULING: Not the prior completed phase but the prior completed task (operator)   DATE: 06/02/26   BY: Ryan W
```
