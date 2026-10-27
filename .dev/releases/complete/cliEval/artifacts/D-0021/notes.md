# D-0021 — implementation notes

## Decisions made during the documentation pass

1. **R3 revision tag rather than a fresh D-10 entry.** Roadmap row 86 asks
   for an *update* to `decisions.md` (queue + status + cross-reference), not
   a new architectural decision. The R3 revision log and an explicit
   "OPS-001 Closure" section are the right vehicle for that update; minting
   a D-10 ADR would imply a new decision being made, which is not what
   OPS-001 actually requests.

2. **"QUEUED FOR SIGN-OFF" as a status string (not "PROPOSED")**. The R2
   bodies used `🟡 PROPOSED`. The OPS-001 AC specifically says "queued for
   sign-off" — a distinct sign-off lifecycle stage that means "decision body
   is frozen, awaiting maintainer signature." `🟠` was chosen to visually
   distinguish from the 🟡-proposed and 🟢-approved states.

3. **Sign-off date column populated with `2026-05-20` rather than `—`.**
   The date the decision was queued is durable evidence; the maintainer
   signature column remains empty until the sign-off pass.

4. **OQ-2 excluded from the OPS-001 §B table.** Row 86 explicitly names
   OQ-1, OQ-3, OQ-7, OQ-8, OQ-10. OQ-2 (eval body shapes) has its own
   resolution path under R-021 dependents and is scoped to M5 entry, not
   M1 exit. Listing it would dilute the OPS-001-specific responsibility.

5. **OQ-1 framing as "resolved by the sign-off pass itself."** OQ-1
   technically reads "remaining `decisions.md` open-question items"; SC5
   resolves it at M6 exit. Within M1 scope, OPS-001 contributes to OQ-1
   resolution by queueing the sign-off — the actual flip to 🟢 by the
   maintainer is the closing event. Stating this explicitly avoids the
   future-reader trap of thinking OQ-1 is still untouched.

6. **Implementation-gate column lists file paths AND task IDs.** A future
   reader following an ADR forward to its enforcement site benefits from
   both: the file path lets them grep; the task ID lets them find the
   build evidence under `evidence/T<id>/`.

7. **`evidence/T01.25/decisions_diff.md` as the primary evidence artefact.**
   For an EXEMPT documentation task, the right evidence is the textual
   delta of the file changed. A diff is reproducible and reviewable; a
   shell command transcript is not.

## Why no roadmap-side edits

`roadmap.md` row 86 is the *requirement*; touching it to mark "OPS-001
done" would (a) edit the requirement-text in the same task that satisfies
it (audit-trail anti-pattern), and (b) is the responsibility of the
release-level state tracker (`.roadmap-state.json` step records), not a
phase-1 documentation task.

## Why no `.roadmap-state.json` edits

Same reasoning + the D-9 ADR explicitly defers `.roadmap-state.json`
edits per maintainer instruction. T01.25 stays in the same lane.
