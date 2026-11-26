| Status | Result |
|---|---|
| DONE | Wrote the design: `.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/DESIGN.md` (492 lines, all seven parts you asked for). |
| DONE | Wrote the worker contract: `.../r1-move-radar/design-report/return-contract.yaml` (status succeeded). |
| DONE | Had it checked by three independent reviews (`design-report/review-1.md` to `review-3.md`) and fixed every blocking problem they found. |
| NEXT | Decide one question for the haiku panel (below), then hand `DESIGN.md` to an implementer. |

RUNS: nothing. This is a design only, and no code or test exists yet. NOT BUILT: every file in section 1 of the design.

**Review status.** The third review found one last problem: the timing measurement counted the first response of each session as a turn of about 0 seconds, which pulled the 90th-percentile turn time down. I fixed it in section 2.6 and test T-12. The review limit had been reached, so that one fix has not been independently re-checked.

**One decision for you (Q-1 in section 7.3).** On the haiku + 2x luna panel, the source's time rule allows haiku zero hints at planning values, because haiku is the slowest reviewer.
- With the rule kept (my recommendation and the design's default), that panel only tests the timed reading prompts sent to the two lunas.
- Giving haiku one hint would push its planned finish to about 286 s. That is past the "finish now" signal (275 s), so the +35% time target would likely be broken.
- Spike 4 may settle this on its own: haiku gets one hint if its measured final-report turn is 12.3 s or less.

**Choices that differ from the source:**
- **Judge outputs.** The unchanged `judge-one.sh` has the old workspace folder hard-coded. It is passed a relative "combo" path that starts in that folder and resolves into the radar folder, so the judge's files land there and nothing is written to the old workspace.
- **Starting commits.** Each package's plan-time commit is missing from this clone. The fallback is the commit just before each package's merged change: `0e486ab8d`, `38eb3c58a` and `5fa680778`.
- **Sonnet and haiku take ember's search role** on their panels, and the two lunas there get their own hint count.

**Recommended action:** answer Q-1, then hand `DESIGN.md` to the implementer. Its Gate 0 checks (section 6.3), starting with the check that hooks fire on all four models, have to pass before any collaboration run.

I did not check two things: whether hooks deliver hints to the gateway models at all (the first Gate 0 check), and whether five designs running at once stay within the gateway limits (at most 10 sessions, at most 4 ember). If hooks don't fire, every collaboration run behaves like the baseline.
