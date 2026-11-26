# G0-SURF calibration

- Rows: `EVAL/TASK-WF-*/reviews/combos/g1-ember-luna2-r*/t*-[0-9].md` (36 historical EL2 reviewer reports, 86 findings; read only).
- Starting regex of DESIGN 3.3: ember 0.0%, luna 4.8% (`result-starting-regex.json`): far under the 15-30% band.
- Calibrated regex (now in `config/routing.json`, re-pinned): adds `artifacts? path|location|folder`, `line anchors|numbered|references`, `line numbers` (plural) and `stale`. Result: ember 22.7% (10/44), luna 16.7% (7/42), both inside 15-30% (`result.json`).
- `result.json` lists all 17 matches (there are only 17 in the data set) and 20 sampled non-matches. The human read the design asks for has NOT been done; a person should read those 37 claims before the first arm.
