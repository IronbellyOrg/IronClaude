# Red-Team A2 — Alternatives + Generalization (system-architect, adversarial)

Verdict: **simplest fail-closed change** = a grounding-obligation (two sub-claims) routed through the
**existing** evidence-validator (§11.2) + §10.6 Grounding Gaps + contract HALT. No new ledger as a *gate*,
no new wave, no 5th taxonomy category, no sub-command. The heavy proposal's static scan + real-boot are
*recall aids*, not the gate, and as specified are overfit to Go.

## Findings
1. **Rubric-only via dimension #4: REJECT as sufficient.** A weak dim-4 only dilutes `C` (rubric.md:11) →
   C<0.85 → §5.3 rule-6 ESCALATE (not HALT) → T2. And T2 can't fix a **missing-evidence** problem:
   §11.0/§11.4 anti-confirmation is conditional and presumes representational bias, not a shared blind spot
   (all reviewers read the same passing tests + same diff). Rubric-only fails open like the bug. **But**
   dimension #1 (Citation grounding) routed through the evidence-validator (§11.2) DOES block fail-closed —
   that's the lever.
2. **Mandatory --tasklist: REJECT blanket, ADOPT scoped.** `--tasklist` is recommended-not-required
   (reflect.md:27, SKILL.md:68); hard input is --diff/--task-log (reflect.md:28). Mandating a spec for ALL
   UC-2 breaks the legacy `--type task --validate` caller / sc:troubleshoot Wave 6 Phase D (reflect.md:198-200).
   Resolution: gate is **spec-conditional**; no spec → emit a Grounding Gap, never STOP.
3. **5th taxonomy category: REJECT.** §17.7 item 6 (SKILL.md:1799) settled it. An unreached sink at audit time
   IS an evidence-insufficiency → §10.6 captures it losslessly (required fields SKILL.md:984-1008). Only loss is
   searchability → add an **optional `gap_kind: unreachable-sink|oracle-mismatch` discriminator** (additive, like
   the optional reuse fields SKILL.md:996-1001).
4. **Sub-command vs in-line: REJECT opt-in.** An opt-in gate that defaults off **silent-passes the exact
   fail-open bug it targets** (the bug looks green; nobody opts in). Always-on, side-effect-conditional (no
   requirement → no-op, mirroring step-3b `find_implementations` SKILL.md:480).
5. **Generalization: the Go-specific detectors are OVERFIT.** `SetDefault`/`_ =`/facade-nil miss tx-rollback,
   tmpdir-wipe, zero-subscriber. The language-agnostic INVARIANT to encode = **two grounded sub-claims per
   side-effect requirement: (a) REACHABILITY** — executed path from entry/composition root to the
   side-effecting call, result not discarded; **(b) ORACLE-ADMISSIBILITY** — the verification observes the
   *contracted* sink, not a proxy. Ungroundable → Grounding Gap (fail-closed). The oracle half is the more
   general and more important half (catches journald/tmpdir/zero-subscriber alike). Static detectors = fail-open
   advisory recall aids only (reuse-auditor posture SKILL.md:492), never the gating mechanism.
