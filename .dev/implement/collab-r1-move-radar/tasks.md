# Task enumeration for DESIGN.md (r1-move-radar)

The design has no checkbox list and no `## Task N` headings. Its numbered lists (2.1, 2.4, 5.2, 6.4) are behaviour
steps of one script, and its `T-n` / `F-n` ids are test ids, so enumerating them one by one would split single
scripts across dozens of tasks. The executor groups the design by its own file tables (section 1) and acceptance
criteria (section 6.5); every AC below quotes the design. Scope is not widened: each task covers only rows the design
lists. Orchestrator constraints (from the invocation) are global constraints for every task.

| Task | Covers (DESIGN.md) | AC |
|---|---|---|
| T1 | 1.1 config + frozen inputs; 1.3 `g-base.sh`, `g-pins.sh` | T1.AC1 every 1.1 file exists with the stated content; T1.AC2 `manifest.json` has 3 base SHAs written by `g-base.sh` (G-BASE manifest part) and the G-PINS pass condition of 6.3 holds (pins written, catalogue 0 ground-truth hits) |
| T2 | 1.2 `sandbox.sh`, `radar-index.sh` | T2.AC1 interfaces as in 1.2; T2.AC2 T-2 passes; T2.AC3 the G-BASE sandbox conditions of 6.3 hold (no `.dev/reflect`, own plan folder absent, designSpec repaired-code check) |
| T3 | 1.2 `radar-classify.jq`, `msg-validate.sh`, `radar-hook.sh`, `settings-gen.sh`; 2.2-2.5 | T3.AC1 behaviour of 2.2-2.5; T3.AC2 T-3..T-9, T-10 (settings part), F-6, F-7, F-14 pass (F-13 moved to T4: it needs the runner's stub `claude`) |
| T4 | 1.2 `run-reviewer.sh`, `h2_normalize.py`, `values.py`; 2.6, 2.7, 4 (R-05) | T4.AC1 behaviour of 2.6/2.7; T4.AC2 T-10 (cmd part), T-11, T-12, T-13, F-8, F-9, F-10 (runner part), F-13 pass |
| T5 | 1.2 `collab_summary.py`, `anon.sh`, `results.py`, `alarms.py`, `cleanup-sessions.sh`; 2.8, 2.9, 5.3, 5.4 | T5.AC1 behaviour as specified; T5.AC2 T-14..T-19, F-1..F-4 (summary part), F-11, F-12 pass |
| T6 | 1.2 `launch.sh`; 1.3 `gate0-check.sh`, `spike4.sh`; 4; 5.1; 5.2 | T6.AC1 launch steps and exit codes of 5.1/5.2, kill switch of 4; T6.AC2 T-10 gate order, F-4/F-5/F-10/F-11/F-12 launch parts pass |
| T7 | 6.5 AC-1 | `uv run pytest …/r1-move-radar/tests -q` exits 0 with T-1..T-19 and F-1..F-14 collected and passed (no skips) |
| T8 | 1.3 `s0-hooks.sh`, `s2-resume.sh`, `reqs3-actrate.sh`; 6.3 S0, S2, REQ-S3 | Spikes run under the gateway lock; records written; `gate0.json` decided mechanically |
| T9 | 6.4 smoke (S3); 6.5 AC-3, AC-4, AC-5 | Smoke rows run (as far as Gate 0 allows) and each 6.4 condition is checked and recorded |
| T10 | Orchestrator deliverable | `IMPLEMENTATION.md` with file list, run commands for the 3 panels and PANEL_COLLAB=0, test counts, spike and smoke results, every unmet requirement with reason |

Not run here (orchestrator constraint "no full panel runs"): Spike 4 (3 full collab-0 rows per panel) and AC-6/AC-8 rows.
