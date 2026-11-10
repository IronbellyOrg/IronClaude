# Prompt 03: Stage C operator (end-to-end panel runs, live)

You operate the PN1 review loop for the shortlisted panels. Read `p20/live-evals/README.md` first; it names the constants you must set in `harness/harness.py` and how reviewers are launched here (from `probe.json`).

Setup, once:
1. Check out the PR branch that holds the panel code (`346Claude-pn4-live-panel-7slot` or its merge) so `uv run superclaude review panel resolve` works, and note its commit SHA in `stage-c/RUN-INFO.md`.
2. `render.py panels --out stage-c/panels --t2b-models <ids from the owner> --tiers <the tier file of that checkout>`; validate every shortlisted panel with `superclaude review panel validate`.
3. `render.py schedule --out stage-c/schedule.json --reps 6 --seed <seed from RUN-INFO> --panels <shortlist ids>`.

For each run in `schedule.json`, in order, holding the number of runs in flight constant at the value in `RUN-INFO.md`:
1. Set `PN_ENV=gateway PN_PANEL=<panel file> PN_TIERS=stage-c/panels/eval-tiers.json PN_PREFIX=<panel id lowercase>`; build the run, then drive it with `advance.py` exactly as the replicate did (`python3 advance.py <run>` prints `LAUNCH <alias> <prompt path>` lines; launch each as a sub-agent on the alias printed, using the mechanism recorded in `probe.json`; the harness marks it launched).
2. Never launch the adjudicator (`ADJ`) or the audits on anything but Sonnet. Never launch anything on Fable / Tier 0.
3. If a requested model silently falls back to another, stop that run, record it in `stage-c/ANOMALIES.md` and relaunch the step once; if it repeats, mark the run lost (do not substitute a model).
4. Record start time and slot index per run in `stage-c/slots.json`.
5. A run is finished when its state phase is `complete` (audits included).

Do not score anything yourself. When all runs are complete, hand off to Prompt 04 (scoring) with the list of final specs `runs/<run>/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
Final reply per finished batch: counts of complete / lost runs and the path of `ANOMALIES.md`.
