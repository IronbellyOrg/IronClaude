# Owner decisions, 2026-11-12 (QUESTION-OBSERVATION pass)

Provenance, stated plainly: the owner gave these instructions in the executor's session on 2026-11-12. The executor typed this file from the owner's words; it is not a file the owner wrote. The quotes are exact.

| Owner words (2026-11-12) | Meaning |
|---|---|
| "Start 1" | Run the observer as place 1: a foreground command in the coordinator's own terminal, which holds the Run. |
| (after the executor listed the three steps, step 1 being a pass record that accepts the Q-1 failure and names `run_93bfa00cae2b`) "Do it" | Record that QUESTION-OBSERVATION passes for R2 on these terms, then flip the live-read guard. |

## The pass, on these terms

- **Accepted:** Q-1 FAIL (`artifacts/q1-result.md` of the release 2 plan). The observer reads only from the terminal that holds the Run. A terminal that holds no Run is fenced out (`consumer_fenced`). `run-use` stays forbidden.
- **Run:** `run_93bfa00cae2b`, the coordinator's own Run, read from the coordinator's terminal with `--types question`, one call per cycle (decisions 6 and 8, `owner-decisions-20261111.md`).
- **Still true, not waived:** the message rate and identity on real traffic are unmeasured (the Task 17 sample is synthetic, accepted by the owner as such on 2026-11-11); non-consumption by a non-owner is unverified; the label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost` stays on screen.
