# Review of the five Jev experiments (research report 3) and the planning decisions

Planner review, 2026-11-10. Sources: `$SP/p15/RESEARCH-REPORT-3.md` (condensed owner report), owner decisions D1-D6 (`$SP/p14/DECISIONS-ADDENDUM.md`), the Stage 2 baseline and harnesses (`$SP/p11`, `$SP/p12/ab2`, `$SP/p13/ab1..ab3`, `$SP/p14/haiku-baseline`), the defect catalog (`$SP/p13/catalog/catalog.json`), the typesafe-ai skill and the live TypeSafe docs (snapshot `$SP/p15/_docs/`, fetched 2026-11-10: `jev-1.14.0` is the current versioned id; $0.042 per million input tokens; 64k/32k context limits; 429/529 retry guidance). Report benchmark numbers and URLs remain UNVERIFIED.

## 0. "Five solutions" vs "three designs"

The report has five experiments; E1 and E4 are two gates of ONE component (fix-closure check). All five are planned: four implementation plans (PLAN-E1E4, PLAN-E2, PLAN-E3, PLAN-E5) plus PLAN-0 for the shared adapter and the central matrix. If the owner's "three designs" meant the three conditional end-to-end studies that can realistically reach a live phase (E4, E2, E3), those are exactly the plans with live harnesses; E5's live stage is BLOCKED by design (needs a scope amendment).

## 1. What the residual is made of, and where each experiment acts

Stage 2 arm 3 (n=6) converged 6/6, yet two frozen audits per final find 1.50 blockers per audit (11 of 12 audits FAIL). Of the 9 first-audit blockers, about 5 were never found by the run's R1 and about 4 were found, "fixed", accepted by the scoped re-review and found again by the audit (`$SP/p13/plans/REVIEW-OF-SOLUTIONS.md` section 1).

| Experiment | Acts on | Can it reduce residual blockers? | Report's framing |
|---|---|---|---|
| E1/E4 fix-closure | the ~4 "found, then survived" | yes in principle (stricter closure), but in E4 Jev only auto-closes; the stricter part is the conventional checker it falls back to | cost (replace narrow checks) |
| E2 priority hints | the ~5 "never found" | possibly, by steering R1 attention | quality at equal attention |
| E3 confirmation screen | precision of R1 blockers before the first revision | no direct recall gain; can avoid unneeded edits | cost (verifier stage) |
| E5 assurance routing | delivery decision after a provisional PASS | only by spending the remaining slot more cleverly; static "always use it" is a strong comparator | cost/assurance |

## 2. Per-experiment review

### E1 (offline replay): sound; runnable here; strict gate
- Sound: selective automation (Jev may only auto-close; everything else falls back), decomposition into defect removal / obligation preservation / supplied-dependency conflict / context sufficiency, code-owned hashes, no-op detection, history-based "regressed", all-or-nothing response validation. This is the skill's "judgments from Jev, decisions in code" pattern, and the report's failure list (moves, partial branches, coupled blockers, injected claims, option order, paraphrase, timeouts, alias drift) maps onto test categories one to one.
- Weak: (a) the decisive risk is packet-only judgment versus whole-document truth (a distant dependency not retrieved); only `context_sufficient` guards it, and only the real S1 stratum measures it. (b) 360 synthetic cases written by one implementer: family-level splits and held-out-only novel categories mitigate authorship bias, not remove it. (c) "Zero false closures in 200 with >= 30% automation" is strict; with 0 errors in N automated closures the one-sided 95% upper bound is still 3/N. (d) The real S1 stratum is small (an estimated 50-70 finding-level packets from 27 revision events) and every packet comes from one spec.
- Runnable: yes, fully; Jev cost < $0.10 for everything; labor is the labeling (~115 offline worker steps for smoke + full).
- Kill: one adjudicated false automatic closure in the 40-case smoke stops E1 and blocks E4.

### E4 (end-to-end, gated on E1): runnable; small absolute stakes
- The saving is bounded by the narrow checks it replaces. B and C share everything except the conventional checker work on the packets Jev auto-closes (both arms let the re-reviewer skip closed findings). A checker costs roughly 10-20k output tokens per revision against a loop of about 115k, so at 50% automation B saves about 5-8% of C's loop. The report's ">= 20% median total-pipeline cost reduction vs matched C" is therefore very unlikely on loop-only accounting: the expected E4 verdict is INCONCLUSIVE (or DROP-2 if B saves nothing), even if Jev is safe. The plan keeps the report's criterion (pre-registration) and also reports the narrow-stage saving; changing the criterion is an owner decision (INDEX open question) and must be made before E4 data exist.
- C (conventional checker on the same packets) is itself a new stricter-closure design. Its comparison with arm A is the most interesting quality signal of the whole program and lands in the matrix as a CONTROL row with numbers.
- Six runs per arm cannot show rare-error safety; attribution of a residual blocker to a Jev closure uses theme + cited-line matching, eyeballed.

### E2 (priority hints): likely NO-GO-OFFLINE at Stage 0; expensive if not
- The recurring themes are lexically linked: T2 is a path collision (shared path/basename), T3 an explicit section reference (AC-0.4 -> 7.2 step 3); the static rule (explicit links, shared ids/paths) should already rank them in its top 12. Jev headroom is plausible only for novel defects without lexical links. Stage 0 measures this with zero paid calls.
- Every live run reviews the SAME spec: each arm's hint list is essentially one fixed artifact. Live n=6 measures reviewer variance under one list; generalization rests on the replay.
- Cost if it advances: about 210 offline worker steps (mostly the conventional router replay) plus 30 live runs: the most expensive experiment.
- Confound: the audit is a sonnet first review; hints that steer a sonnet R1 toward audit-like themes can look good to the audit.

### E3 (confirmation screen): most likely to reach live; low risk, small effect
- Safe by construction: Jev can only confirm; negatives belong to the conventional verifier; exceptions (CRITICAL) are code-owned. A false confirmation reproduces arm A's behavior (A sends every R1 blocker to the reviser unverified), so the report's asymmetric-loss pilot (200 + 300) is deferred.
- The saving is at most one verifier worker per run (~15k tokens); a 20% verifier-stage reduction is detectable at n=6, a quality difference is not.
- Overlap: `$SP/p12/ab2` (verify gate at every review) is running; E3's B (verify before the first revision only) differs, so p12/ab2 is not reused as a control; the matrix shows both.

### E5 (assurance routing): NO-GO-OFFLINE predicted, at zero cost
- With 11 of 12 Sonnet-baseline audits and every Haiku-baseline audit finding a blocker, the minimum required route after a provisional PASS is almost always "use the remaining slot", which is exactly the static rule. Headroom packets (adequate spec on which static spends a review) are expected to be 0-1 of about 15-20: below the pre-registered 2 packets / 10%.
- The live stage additionally needs an owner amendment (cap-neutral scope). Without it E5 live is BLOCKED.

## 3. Likely NO-GO offline, at zero marginal cost

- **E5**: zero Jev calls and zero workers; computed from audits on disk by one implementer session; expected NO-GO-OFFLINE (static dominates at a ~90% residual base rate).
- **E2 Stage 0**: zero Jev calls, ~7 offline labeling workers; expected NO-GO-OFFLINE or very small headroom (historical themes are lexically linked).
- E1 smoke and E3 falsifier cost under $0.05 of Jev each plus 14-35 offline workers; their outcomes are genuinely open.

## 4. Threats to validity (all plans)

1. **Arm A is historical.** The "current canonical unchanged" arm is the Stage 2 baseline (2026-11-10 00:38-02:05 UTC), not re-run (instruction). Fresh arms are interleaved in blocks with each other, so B-vs-C comparisons are drift-matched; comparisons with A carry drift risk. A shared 2-replicate drift check is offered as an owner option (INDEX).
2. **Audit instrument bias.** The frozen audit is a sonnet first review with the same FIRST-REVIEW prompt; designs that add sonnet-like checking look better to it. Two audits per final; replica agreement required.
3. **Correlated blindness.** Labelers (sonnet + haiku), conventional comparators (sonnet) and the audit share one vendor; Jev is a different model family, which is a genuine decorrelation source but also means Jev disagreements with labels are not automatically Jev errors. Mitigation: L2 on Haiku, adjudication explicit, accuracy also reported against L2-only labels, kappa reported.
4. **One spec.** All live runs and the real offline strata come from S1. Synthetic families provide breadth for the replays only.
5. **Test-arm rules insertions.** E2/E3/E4 add one rules line to the test arms (hints / verification block / prior-blocker checks), identical across that experiment's fresh arms and absent from A. The B-vs-C contrast isolates the model choice; the A contrast carries the insertion.
6. **Packet vs document.** Jev and the conventional comparators see packets; labels use whole documents (by design: that is where the real risk is).
7. **Harness realism.** The harness plays the coordinator; whether a real `/sc:spec-panel` coordinator would compute packets and call Jev is not tested.
8. **Haiku sandbox discipline.** A Haiku worker wrote outside its sandbox in the Haiku baseline (a3-r6). With a Jev key on disk (`$SP/.jev.env`, same OS user) a misbehaving worker could read it; the key is a throwaway, it is never in the environment of any worker, and a transcript key scan runs after every phase.
9. **Privacy.** Real S1 text and Stage 2 artifacts are sent to Jev (owner's own documents; authorized). Zero data retention is not activated for this key (default retention unspecified): recorded in every plan, not a blocker.

## 5. Order, dependencies, kill criteria

| Step | Depends on | Kill / advance (pre-registered) | NO-GO record in the matrix |
|---|---|---|---|
| PLAN-0 adapter + matrix + live probe | - | probe: returned model must equal `jev-1.14.0` and the validator must accept the real response; else all paid phases wait for the owner | - |
| E5 zero-call | PLAN-0 (results writer; optional) | headroom < 2 packets or < 10% -> NO-GO-OFFLINE | gate row `E5-zero-call` NO-GO-OFFLINE; `k5*` BLOCKED |
| E1 smoke (40) | PLAN-0, probe | any false automatic closure -> NO-GO-OFFLINE | `E1-smoke` NO-GO-OFFLINE; `f4b`/`f4c` BLOCKED |
| E1 replay (120 + 200) | smoke GO | calibration: no admissible policy >= 30% automation -> NO-GO; held-out: 0 false closures, >= 30% automation, >= 20% stage cost reduction, <= 2 extra false opens, conservative failures -> GO-E4 | `E1-replay` NO-GO-OFFLINE; E4 BLOCKED |
| E4 live (12 + 8 runs) | E1 GO-E4 | DROP-1 attributable incorrect closure; DROP-2 no saving vs C; DROP-3 quality; ADOPT needs BLK <= both controls and >= 20% median loop saving vs C | `f4b` verdict, `f4c` CONTROL |
| E3 falsifier (60 + 40) | PLAN-0, probe | exception/insufficient/API-failure safety; automation >= 20%; false-confirmation margin <= +0.10 over the conventional verifier; perturbation tolerances | `E3-falsifier` NO-GO-OFFLINE; `g3*` BLOCKED |
| E3 live (12 + 8 runs) | falsifier GO | DROP-1 harmful edit / exception / hidden blocker; DROP-2 no saving vs B; DROP-3 quality; ADOPT needs automation >= 20%, >= 20% verifier-stage saving, BLK <= B | `g3c` verdict, `g3b` CONTROL |
| E2 Stage 0 (24) | PLAN-0 | extraction loss -> fix; H = 0 -> NO-GO-OFFLINE | `E2-stage0` NO-GO-OFFLINE; `h2*` BLOCKED |
| E2 replay (120 + 240 + 40) | Stage 0 GO | Jev >= static + 8 of 160 held-out defect cases -> GO-LIVE | `E2-replay` NO-GO-OFFLINE |
| E2 live (18 + 12 runs) | replay GO | DROP-1 escalations/growth; DROP-2 vs A; DROP-3 vs static; ADOPT BLK <= 0.83 and <= static - 0.33, cost <= 1.10 x static | `h2j` verdict, `h2s`/`h2r` CONTROL |
| E5 probe / replay / live | headroom; live also owner amendment | see PLAN-E5 | BLOCKED rows until then |

## 6. How the owner's rules land

- D1: every live rule has three zones (ADOPT / INCONCLUSIVE / DROP); offline gates add NO-GO-OFFLINE and BLOCKED; the report's numeric thresholds are kept and converted (below).
- D2: all live cost clauses use loop-only output tokens of model workers (`R_LOOP` vs 100,424; `R_B` printed); Jev tokens/USD reported apart and never added.
- D3: Haiku stratum n=4 per fresh arm (loop workers incl. checkers/verifiers/routers on Haiku; audits Sonnet), judged on HR vs the shared Haiku baseline, never pooled.
- D4: one +3 Sonnet extension per experiment, applied to every fresh arm.
- D5: private clones, no worktrees, no Orca, no PR, push to origin only.
- D6: the report's per-run ceilings (2M tokens, 40 requests, 60 min, $100; Jev 60 attempts / 5M / $1 / 10 s; audit 500k / 8 / 20 min / $25) and campaign caps ($2,305 / $3,055) are removed; "exceeding any cap escalates" is removed. The only money is the Jev API: $5 offline + $1 live per experiment, enforced as pre-flight reservations (an offline phase that does not fit refuses to START; a live J step that cannot draw falls back to the conventional path and the run continues). No live rule needed the D6 L-conversion: every report cost rule is relative to a matched arm (C, B, static) or a percentage of stage cost, not a limit on loop+audit tokens.

## 7. Decisions taken (program level)

1. No `src/superclaude/` edits in p15: test-arm rules files are generated from the frozen rules plus one sha-pinned insertion per experiment; adoption would be a separate product change.
2. Frozen command/rules are read from disk with sha asserts (the baseline commit `69ac8b33` is not on the remote; `origin/master` lacks the rules file).
3. Arm A = baseline data for every experiment; no fresh "current" arm (drift recorded; optional drift check offered).
4. The report's 3-option Choices with "uncertain/insufficient" are implemented as Nouls with a companion null-case Noul and a middle band (skill guidance); Choices only where options are mutually exclusive (E5 probe).
5. Labels: L1 sonnet + L2 haiku + sonnet adjudicator, blind to author intent and model outputs; E5 zero-call labels come from the frozen audits.
6. Implementer sessions are split at every gate so no authoring or harness effort is spent behind a failed gate.
7. Every outcome (including NO-GO and BLOCKED) writes `results.json` and lands in `$SP/central/MATRIX.md` next to the p12/p13/p14 designs.
