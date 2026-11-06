| # | Dimension | Criterion (short) | A verdict | A evidence | B verdict | B evidence |
|---|---|---|---|---|---|---|
| 1 | Completeness | Covers all explicit requirements (4 lenses) | MET | Headings at A:7 Safety, A:12 Reliability, A:17 How a person works day to day, A:21 Implementation cost | MET | B:12 Safety, B:16 Reliability, B:21 How a person works day to day, B:24 Implementation cost (plus B:7 Strongest case) |
| 2 | Completeness | Edge cases and failure scenarios | MET | A:8 quoted-argument case `/sc:troubleshoot "the worker ignores --unattended"`; A:19 forgotten flag stalls with no worker_done; A:9 env var set in non-worker terminal | MET | B:13 env var set in non-worker tab, `/sc:cleanup --interactive` loses prompts; B:19 `claude --print` signal would not fire for a worker; B:14 preamble on same command line |
| 3 | Completeness | Dependencies and prerequisites | MET | A:15 "a command accepts the flag only once its gates are converted (SPEC:187-195)"; A:18 brief template in WORKER-CONTRACT.md | MET | B:5 depends on `orca-ide skills get orchestration` 1.4.237; B:25 AC-C1 grep needs an exception; B:14 relies on live preamble in context |
| 4 | Completeness | Success or completion criteria | MET | A:13 "AC-1.1 asserts per phase which commands carry an ## Unattended mode section"; A:8 AC-2.8 live check | NOT MET | B:17 says "Not mechanically testable"; B:25 mentions AC-C1 only as a cost. No criterion for when the option counts as working |
| 5 | Completeness | Explicit out of scope | NOT MET | No out-of-scope statement; A:3 states a position, not an exclusion list | NOT MET | B:18 quotes spec non-goal 1, but as an argument against the option, not a scoping statement of the paper |
| 6 | Correctness | No factual errors or hallucinated claims | MET | Cited lines held up in the advocates' spot-checks (SPEC:55, 73, 187-195, 257, 269, 329, 395 verified). A:9 live-session observation is unverified but not contradicted | NOT MET | B:19 states as fact that the `--print` signal "would not fire", but SPEC:391 says "assumed not" (UNVERIFIED item 9); B:14 says preamble is on the command line citing CAPS:47, which only covers the task argv |
| 7 | Correctness | Approach feasible within stated constraints | MET | A:22 commands are prompts, so the model applies the parse rule; the quoted-argument rule exists for that reason | NOT MET | B:18 itself says the option violates non-goal 1 (SPEC:314) and SA-2, and B:17 says it is not mechanically testable, so it fails the stated constraints |
| 8 | Correctness | Terminology consistent and accurate | MET | "unattended", "standalone token", "person's run", "brief" used the same way at A:3, A:8, A:18 | MET | "detection", "preamble", "dispatched worker", "ordinary terminal agent" used consistently at B:3, B:8, B:13 |
| 9 | Correctness | No internal contradictions | MET | A:3 "Nothing in the environment... turns it on" vs A:23 "can be added as an extra trigger" is a future option, not a conflict | NOT MET | B:9 "Detection removes that whole failure class" vs B:17 "a wrong guess by the model is invisible until a run stalls"; also B:8 "not a guess" vs B:14 "relies on the model noticing prose" |
| 10 | Correctness | Claims supported by evidence or rationale | MET | Nearly every bullet carries a SPEC or CAPS line (A:8, A:9, A:13, A:14, A:22) | MET | Bullets carry SPEC, CAPS or [G] lines (B:8, B:9, B:13, B:18, B:19, B:25), although two are overstated (see 6) |
| 11 | Structure | Logical section ordering | MET | Position A:3, key A:5, then the four lenses A:7-A:23 | MET | Position B:3, key B:5, case for B:7, then the four lenses B:12-B:25 |
| 12 | Structure | Consistent hierarchy depth | MET | One H1 (A:1) and H2 lens sections only | MET | One H1 (B:1) and H2 sections only |
| 13 | Structure | Separation of concerns | MET | Each lens holds its own material; A:14-15 caller-neutral and phase-gating under Reliability | NOT MET | "Strongest case" (B:9, B:10) repeats Reliability and Cost content; B:14 puts a testability point under Safety and B:17 repeats it under Reliability |
| 14 | Structure | Navigation aids | MET | Citation key at A:5 maps SPEC:N and CAPS:N to files so a reader can navigate | MET | Citation key at B:5 maps SPEC:N, CAPS:N and [G] N to sources |
| 15 | Structure | Follows decision-option paper conventions | MET | Titled "D1 option (a)" (A:1), states a position (A:3), evaluates by lens, names a weakness (A:19) | MET | Titled "D1 option (b)" (B:1), states a position (B:3), strongest case, then evaluates by lens |
| 16 | Clarity | Unambiguous language (no hedges) | MET | Firm wording: "cannot switch a person's run" (A:8), "Detection would misfire" (A:9); no "might" or "as appropriate" | MET | Firm wording: "Environment detection is unsafe" (B:13), "Not mechanically testable" (B:17); no listed hedge words |
| 17 | Clarity | Concrete rather than abstract | MET | Example `/sc:troubleshoot "the worker ignores --unattended"` (A:8); 11 workers (A:9) | MET | Example `/sc:cleanup --interactive` (B:13); 11 handle values (B:13); 35 commands (B:10) |
| 18 | Clarity | Each section has one clear purpose | MET | Four sections, each one lens, summarizable in one sentence | MET | Five sections, each one lens or the case for the option |
| 19 | Clarity | Acronyms and terms defined at first use | NOT MET | SA-1 first used at A:9 and WC-9 at A:10 without definition; AC-1.1, AC-2.8 and "7.2" never explained | NOT MET | SA-1 (B:13), SA-2 (B:18), AC-C1 (B:25) and [G] used without definition |
| 20 | Clarity | Actionable next steps or decision points | NOT MET | Paper advocates a position; no next step or decision request. A:23 only says changing later is cheap | NOT MET | No next step or decision request; B:22 and B:25 only state costs |
| 21 | Risk coverage | At least 3 risks with probability and impact | NOT MET | Risks exist (A:9 misfire, A:19 forgotten flag, A:8 misparse) but none gets probability plus impact; "observed" is the only likelihood cue | NOT MET | Risks exist (B:13, B:14, B:17, B:19) but none gets probability plus impact |
| 22 | Risk coverage | Mitigation for each risk | MET | Misfire to flag immune (A:9); misparse to standalone-token rule (A:8); forgotten flag to brief template and stall proof (A:19) | NOT MET | B:13 to B:19 list problems with no mitigation except the preamble route being "safer" (B:14); nothing for model mis-detection (B:17) or coupling (B:18) |
| 23 | Risk coverage | Failure modes and recovery procedures | NOT MET | Failure mode named (A:19 stall, no worker_done) but only after-the-fact detection, no recovery steps | NOT MET | Failure modes named (B:17 stall or vanished prompt) with no recovery procedure |
| 24 | Risk coverage | External dependencies and their failures | MET | A:19 Orca reports a stalled worker as healthy (CAPS:52); A:9 `worker-list` and env var; A:14 other callers | MET | B:13 `worker-list` vs env var; B:19 Orca launches Claude interactively; B:9 Orca reports waiting worker as healthy |
| 25 | Risk coverage | Monitoring or validation mechanism | MET | A:13 AC-1.1 plus live 7.2 checks; A:8 AC-2.8; A:19 step-3 stall proof | NOT MET | B:17 says there is no token to grep and no mechanical test; no validation mechanism is offered |
| 26 | Invariant and edge | Boundaries: zero, one, many; empty or quoted arguments | MET | A:8 quoted argument; A:13 per-phase set of commands; A:14 `claude -p`/CI callers with no Orca | MET | B:18 callers with no Orca (`claude -p`, CI); B:10 "35 commands"; quoted arguments are not addressed |
| 27 | Invariant and edge | State variable interactions across components | MET | A:9 `ORCA_TERMINAL_HANDLE` vs `worker-list` handles; A:18 coordinator writes flag, command reads it | MET | B:13 same variable vs worker-list; B:14 preamble in conversation context vs command line |
| 28 | Invariant and edge | Guard condition gaps | MET | A:19 missing flag has no guard; A:22 parse is model-applied, not code; A:9 UNVERIFIED item 13 | MET | B:14 and B:17 detection relies on the model noticing prose; B:13 env var guard fails in a person's tab |
| 29 | Invariant and edge | Count divergence (off-by-one, inclusive/exclusive, counts) | NOT MET | "11 workers" (A:9) is an observation, not a divergence scenario; no count-mismatch case | NOT MET | "11" and "35" (B:13, B:10) stated, no count-divergence scenario |
| 30 | Invariant and edge | Interaction effects when components combine | MET | A:10 flag plus WC-9 outward defaults vs auggie-review posting default; A:15 flag plus phase gating | MET | B:13 env route plus SA-1 plus outward defaults; B:25 detection text plus AC-C1 grep exception |

## Dimension subtotals

| Dimension | A | B |
|---|---|---|
| Completeness (1-5) | 4/5 | 3/5 |
| Correctness (6-10) | 5/5 | 2/5 |
| Structure (11-15) | 5/5 | 4/5 |
| Clarity (16-20) | 3/5 | 3/5 |
| Risk coverage (21-25) | 3/5 | 1/5 |
| Invariant and edge (26-30) | 4/5 | 4/5 |

**Total: A = 24/30, B = 17/30**

Notes: Verdicts for A were decided before B was read. Factual spot-checks used the advocate files only for citation accuracy (B:19 and B:14 overstate their sources; A's 2026-11-02 observation is unverified in both papers and counted as not disproved).
