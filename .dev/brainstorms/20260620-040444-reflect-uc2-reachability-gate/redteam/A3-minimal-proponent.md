# Red-Team A3 — Minimal Correct Gate (backend-architect, proponent/refiner)

Position: the gate is NEEDED (bug is real, current reflect is blind). Minimal form catches it with three
cheap signals derivable from artifacts the §6.1 chain ALREADY collects:
1. **missing_binding** — `find_referencing_symbols` on the sink's binder (already step 4, SKILL.md:463); zero
   refs in the entrypoint file = unbound.
2. **discarded_emitter_result** — step-6 re-Read of the emitter hunk (SKILL.md:475); `_ =`/unchecked = fail-open.
3. **oracle_mismatch** — string compare of the acceptance oracle's asserted sink vs `contracted_sink`.

Static signals are T1, zero new tool budget. Real-boot = best-effort step-5.5 `execute_shell_command`
(already T1, cost-profile T1=3-8k). Verdict (A3's original, fail-closed): `missing_binding AND
(discarded_emitter OR oracle_mismatch)` ⇒ `unreachable` → `regression_present`; partial ⇒ `unproven` →
Grounding Gap. Rides existing contract fields (contract.py:315/319) — NO consumer change; contract.py:66-82
tolerates the new fields.

Delivered: full concrete additive per-file edits (SKILL.md §6.1 step 5.6, §10.4 bullet, §9.1 block, §17.6
rows, §17.7 item; reflect.md flag `--no-reachability`; refs/{deviation-taxonomy, reviewer-spec,
report-template, reflection-rubric, cost-profile}) + 2 fixtures + 3 test functions.

**Merge note:** A3's edit *structure* is adopted wholesale in `merged-requirements.md`. A3's *default
classification* (static-proven contradiction → auto-Regression) is OVERRIDDEN by the A1/A2 convergence:
default → `unproven`/Grounding Gap (which does NOT trip §5.3 rule-3 → Tier-1 preserved), static scan demoted
to advisory-L2, auto-Regression reserved for a real-boot-PROVEN contradiction only. This keeps "never silent
pass" while eliminating false-Regression + rule-3 drag + halt-fatigue.
