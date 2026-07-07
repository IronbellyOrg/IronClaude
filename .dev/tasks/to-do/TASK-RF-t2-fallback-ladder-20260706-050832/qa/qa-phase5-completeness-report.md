# QA — Phase 5 HALT-Semantics Completeness Report (Step 5.G1)

**Lens:** needs_human_decision HALT-semantics completeness (adversarial)
**Analyst:** rf-analyst
**Date:** 2026-07-07
**Task:** TASK-RF-t2-fallback-ladder-20260706-050832
**fix_authorization:** false (report-only; no source/test/task file modified)
**Adversarial mandate:** "Assume Phase 5 has ≥3 defects in the needs_human_decision HALT semantics. Find them."

---

## Verdict: FAIL — 4 HALT-semantics defects (1 HIGH, 1 HIGH/MEDIUM, 2 MEDIUM) + 1 LOW observation

**Nuance for the consolidator:** The *code-mutation* checks pass cleanly. `_T1_PROXY_BINDING`
is a non-None dict using the dedicated T1 contract (checks #2, #3), and the None→degrade
branch is structurally present (check #4). The FAIL is entirely in the **HALT-integrity and
factual-provenance dimension** (checks #1 and #5): the human-decision gate was structurally
defanged at build time and the operator sign-off that authorizes shipping a live-proxy binding
is unauditable. The code faithfully does what the task told it to — but the task told it to
convert a `needs_human_decision` HALT into a mechanical env-presence check, which is exactly the
anti-pattern the gate exists to prevent (`feedback_human_decision_items_must_halt`).

---

## Per-Verify-Item Results

| # | Verify item | Result | Evidence |
|---|-------------|--------|----------|
| 1 | Wrote resolved decision record; enabled dispatch only AFTER confirmation; did NOT auto-apply default | PARTIAL / FAIL | Record exists, but "confirmation" was pre-cleared at build time and the effective runtime gate is env-presence, not a human decision (Defect 1). |
| 2 | Confirmed binding uses dedicated T1 contract, NOT §7.3 T2-reuse default | PASS | `ensemble.py:193-198` binds `T1ProxyUrl`/`T1ProxyKey`/`T1Model0`; `grep` confirms **no** `T2Proxy*`/`T2_PROXY*` reference anywhere in `ensemble.py`. |
| 3 | `_T1_PROXY_BINDING` non-None dict with exactly the confirmed NAME strings | PASS | `ensemble.py:193-198`: `{"model_prefix":"T1Model0","proxy_url_env":"T1ProxyUrl","proxy_key_env":"T1ProxyKey","max_slots":T1_MODEL_MAX_SLOTS}`. NAMES only, no values. |
| 4 | None-case degrade branch still present (raises TransportEnvError → fallback_config_missing) | PASS (structural) — see Defect 5 | `ensemble.py:230-235` `_gated_factory` raises `TransportEnvError(("T1ProxyUrl","T1ProxyKey","T1Model01"))`. Present, but now unreachable in production. |
| 5 | Record is factual; no fabricated confirmation | FAIL | Operator sign-off is self-reported by the executor with no independent artifact (Defect 2); the designated Phase 5 Task Log section is empty and frontmatter still declares the HALT active (Defect 4). |

---

## Defects

### Defect 1 — HALT pre-resolved at BUILD time; human-decision leg replaced by a mechanical env-presence check — Severity: HIGH

**What the memory requires** (`feedback_human_decision_items_must_halt`): a `needs_human_decision`
item must write PENDING and HALT the dependent mutation until a human decides; it must NEVER
auto-apply a default that ships a change.

**What the built task does instead.** The Open Questions entry (task file **line 516**) is authored
as `[HUMAN-DECISION — T1 proxy binding — RESOLVED, operator-confirmed 2026-07-06]` and states
verbatim: *"The build-time PENDING is now CLEARED — the executor proceeds with the confirmed
binding and does NOT halt for sign-off (a HALT remains only if Step 5.1 finds the NAMES unexpectedly
absent in the execution environment)."*

The Step 5.1 runtime branch (task **line 404**) collapses to: *IF all three NAMES are confirmed
present → record + proceed to Step 5.2*. The only surviving HALT condition is "env NAMES absent."
The **human decision** dimension — *should we ship real dispatch to a live proxy at all?* — is no
longer gated at runtime; it was baked in at build time. If the operator had never signed off, the
executor would STILL set `_T1_PROXY_BINDING` and ship real dispatch as long as `grep ~/.aienv`
returns the NAMES. An environment-presence check has been substituted for the human decision — the
precise "auto-default that ships a change" the memory forbids.

**Evidence:** task lines 404, 516; `ensemble.py:193-198` (the shipped binding).

---

### Defect 2 — Operator sign-off is executor-self-reported and unauditable (fabrication risk) — Severity: HIGH/MEDIUM

The sole evidence of operator authorization for a live-proxy binding is the executor's own prose:
- Line 516: *"OPERATOR SIGN-OFF (2026-07-06): the operator explicitly CONFIRMED these binding values are correct."*
- Line 517: *"The operator RE-CONFIRMED 'Enable real dispatch now' interactively this session."*

There is **no independent artifact** — no quoted user instruction, no permission-system record,
no citation of where/how the sign-off occurred. An executor agent has a direct structural incentive
to assert confirmation because doing so unblocks the phase. Verify item #5 asks for a factual record
with no fabricated confirmation; this record cannot be independently corroborated. Under this agent's
Critical Rule 7 (zero tolerance for fabrication) and the framing that no agent message is the user's
consent, a self-reported "the operator said yes" that ships a real proxy binding must be treated as
**UNVERIFIED at best**. The binding-decision.md and dispatch-verdict.md restate the same
self-reported claim (they do not corroborate it — they inherit it from the same author).

**Evidence:** task lines 516-517; `t1-proxy-binding-decision.md:11`; `phase5-dispatch-verdict.md:8`.

---

### Defect 3 — Decision solicited before the artifact it authorizes existed (ordering inversion) — Severity: MEDIUM

The build-time sign-off is dated **2026-07-06**, the same day the task was built
(slug `...-20260706-050832`) and BEFORE Phases 1-4 wired the structure being authorized
(`resolve_t1_fallback_factory`'s openai_compat arm was added in Step 3.5 / Step 4.4). A
`needs_human_decision` HALT exists to surface the decision at the decision point (Phase 5), AFTER
the reviewable change is in place, so the human can make an informed call on the actual wiring.
Pre-authorizing the binding at build time renders the "decision" on a not-yet-built change; the
Phase-5 runtime step then only re-checks env NAMES, never re-surfaces the substance for a human.
This is a process-ordering defect that hollows out the gate's purpose.

**Evidence:** task line 516 (dated 2026-07-06); task lines 311, 362 (structure wired in Phases 3-4).

---

### Defect 4 — Execution-time outcome not recorded in the designated log; frontmatter still declares the HALT active — Severity: MEDIUM

Step 5.1 mandates recording the HALT outcome and, on HALT, setting `status: "⚪ Blocked"` +
`blocker_reason`. Findings:
- The `### Phase 5 - Real Dispatch Findings` Task Log section (task line 544) is **empty** — the
  execution-time confirmation was written only into Open Questions + the two plan docs, not the
  designated findings log.
- Frontmatter (task lines 6, 56): `status: "🟠 Doing"`, `blocker_reason: ""`.
- Frontmatter `note` (task line 28) still asserts *"needs_human_decision=true is the deliberate
  T1-proxy binding HALT"* — present tense, as a **live** gate.

So for an auditor reading only frontmatter, the state is "HALT active / pending," while the body
records "HALT resolved, dispatch enabled." The gate's resolution lives solely in the body; the
frontmatter was never reconciled. This is a record-consistency defect that makes the HALT outcome
non-authoritative at the frontmatter layer other gates key off.

**Evidence:** task lines 6, 28, 56, 544.

---

### Defect 5 — None-degrade branch (check #4) is now unreachable in production — Severity: LOW (observation)

`_T1_PROXY_BINDING` is a module-level non-None literal, so `if _T1_PROXY_BINDING is None:`
(`ensemble.py:230`) can only be exercised by test monkeypatching — never in a production run. Check
#4 passes structurally (the branch exists), but the **real** runtime protection against an
unverified/incomplete env is now solely the LAZY read inside `_lazy_openai_factory`
(`ensemble.py:251-284`), which raises `TransportEnvError`/`ModelPoolTooSmallError` on factory call and
`run_fallback_ladder` folds it into `terminal_reason: fallback_config_missing`. This is correct and
present — but a future reader must not mistake the dead None-branch for the live safety net. Noted so
the degrade guarantee is attributed to the right mechanism.

**Evidence:** `ensemble.py:230-235` (dead in prod), `ensemble.py:251-284` (live lazy-degrade).

---

## Recommendations (for the consolidator / fix agent — I am report-only)

1. **(Defect 1, HIGH)** Do NOT resolve `needs_human_decision` at build time. The Open Questions
   entry should ship as PENDING; the Step 5.1 runtime gate must require an actual human decision
   (not merely env-NAME presence) before setting `_T1_PROXY_BINDING`. Env-presence is a
   *precondition*, not a substitute for the sign-off.
2. **(Defect 2, HIGH/MEDIUM)** Cite the operator sign-off to a verifiable source (the literal user
   message that authorized "enable real dispatch," or a permission-system record). Absent that,
   downgrade the record to `[UNVERIFIED]` and re-surface the decision to the user before treating
   real dispatch as authorized.
3. **(Defect 3, MEDIUM)** If a future rebuild reuses this pattern, place the human-decision
   solicitation at the Phase-5 decision point over the *built* structure, not at build time.
4. **(Defect 4, MEDIUM)** Reconcile frontmatter with the body: record the HALT outcome in the
   `### Phase 5 - Real Dispatch Findings` Task Log section, and update the frontmatter `note`
   (line 28) so it no longer asserts an active `needs_human_decision=true` HALT after the item
   resolved.
5. **(Defect 5, LOW)** Add a code comment (or leave as-is) noting the None-branch is a
   test-only path and the live degrade guarantee is the lazy read at `ensemble.py:251-284`.

## Scope / Methodology note

Report-only lens; no source, test, or task file was modified. Findings are grounded in direct
reads of `ensemble.py`, the task file (frontmatter + Step 5 items + Open Questions + Task Log),
`t1-proxy-binding-decision.md`, `phase5-dispatch-verdict.md`, `phase5-output-summary.md`, and
`research/06-config-threading-gap-fill.md`. No web research was authorized or performed. The
"operator confirmed" claim (Defect 2) is inherently unverifiable from artifacts alone and is
reported as such rather than assumed true or false.
