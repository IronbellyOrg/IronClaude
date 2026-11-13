# Review 3 (final) of r1-move-radar/DESIGN.md

Verdict: **FAIL**. The main part of N-1 is fixed. One leftover instance of the same defect remains in the same sentence: the rule for the first response measures a turn of about 0 s in every attempt file. The fix is one clause. Nothing new is blocking in the other three changed passages.

Paths: `D` = `r1-move-radar/DESIGN.md`. `A1` = `20261111-a1`. `F` = `A1/TASK-WF-design-20261108-041415/reviews/combos/b4-muse-ember-luna2/t4-1.attempt1.json`.

## 1. N-1 (how Spike 4 measures a turn): mostly fixed, one blocking remainder

### What is fixed (D:191)
- Entries are now grouped by `message.id`.
- A turn is measured from the latest tool-result entry before the response group to the last timestamp of that group.
- The final response is left out of `turn_p90` and feeds only `T_report_p90`.

### Fields checked with jq on F and on every A1 attempt file
- There are 1,275 array-shaped attempt files under A1.
- All 35,018 `assistant` entries have both `message.id` and `timestamp`.
- All 19,037 `user` entries that carry a `tool_result` have a `timestamp`.
- `tool_progress` and `system` entries have no timestamp, so the "entries without one are skipped" rule is needed and correct.

### Durations on F, using the D:191 rule
F has 5 response groups.

| Group | Measured from | Duration |
|---|---|---|
| `resp_078c…` | tool result at 02.014 | 3.46 s |
| `resp_0712…` | tool result at 05.614 (entry 5) | 4.51 s |
| `resp_0400…` | tool result at 10.222 | 8.58 s |
| `resp_05b8…` (final) | tool result at 18.958 | 58.3 s, goes to `T_report` only |

- These are plausible model-turn times, and they match review 2's hand values (3.5, 4.5 and 8.6 s).
- The four thinking blocks (entries 28-33) and the 7-entry parallel group (entries 15-21) now count as one turn each.
- Entries 6 and 7 are `user` text entries with earlier timestamps than entry 5. They are not tool results, so they do not affect the result.

### Remaining blocking defect, N-1a: the first response is a false turn of about 0 s
- D:191 says: "(for the first response, minus the first entry of the file)".
- In all 1,275 A1 attempt files, the first entry is `system` with no `timestamp`. Under the skip rule, the start therefore falls back to the response's own first entry, and the "turn" is only the time between that response's own blocks.
- I applied D:191 to the 366 `*.attempt1.json` files under `A1/TASK-WF-design-20261108-041415/reviews/combos`:
  - first-response "turns" have a median of 0.50 s;
  - 61 of the 366 are exactly 0;
  - the 90th percentile is 1.64 s;
  - real turns have a median of 7.8 s.
- One of these false values enters `turn_p90` from every file. This is the same symptom as N-1 (near-zero values that are not turns), at a smaller scale.
- Measured per model over all A1 combos (p90 with the first response included → without it):

| Model | With first response | Without it | Change |
|---|---|---|---|
| luna | 25.1 s | 28.1 s | −11% |
| haiku | 62.8 s | 68.5 s | −8% |
| sonnet | 42.2 s | 43.5 s | −3% |
| ember | 5.0 s | 5.2 s | −4% |

- `turn_p90` feeds `finish_offset`, `k`, the A-3 guard and A-2 (D:185-189), and the values file is frozen. A value that is biased low is written once and never corrected.
- Fix (one clause in D:191): leave the first response out of `turn_p90`, as the final response already is. Its real start, the CLI launch, is not in the file. Add a first-response case to the T-12 fixture (D:382).

### T-12 fixture text (D:382)
- It matches the new definition: a response split over three entries with one `message.id` counts as one turn; two parallel tool calls add no turn; the final response feeds only `T_report_p90`.
- It has no first-response case, which is why N-1a is not caught (see the fix above).

### Not blocking
- Subagent entries (non-null `parent_tool_use_id`) are not excluded. They appear in 1 of 1,275 A1 files (`combos/g3-sonnet-luna-ember-r4/t4-1.attempt1.json`, entries 10-38). Under D:191 they become extra turns of 2-11 s, which is negligible in the pool.
- S0 already covers how subagent calls reach the hook (D:418).

## 2. Other changed passages: no new blocking defect

### Section 5.2 step 6 (D:321), `anon_leak` quarantine
- The order is consistent:
  - `post` runs after `anon.sh` (D:60, D:109);
  - the judge (step 7) runs after step 6;
  - `quarantined` is an existing package status (D:312, D:347) that makes the row `incomplete` (D:361).
- False-positive check on the listed tokens, over the 319 A1 `merged-anon.md` files:
  - `\bc[01]\b` matches 1 file, a path to an A1 combo named `c1-…`. R1's anonymiser rewrites absolute `R1` and `A1DIR` paths to `<EVAL>` first (D:327), so that case does not occur here;
  - `radar` matches 0 files.
  - The check is workable.
- Not blocking:
  - Step 6 does not say who writes `QUARANTINED` for this case. `pre` writes it on exit 3 (D:60), but `post` is not said to write it or to exit 3.
  - No F-row tests `anon_leak > 0`; T-17 only checks that the key is present.
  - Suggested change: have `post` write `QUARANTINED` and exit 3, matching `pre`, and add an F-4-style case.

### T-10 row, added gate-order sentence (D:380)
The sentence: "fixture `gate0.json` lacking S3 → `rep` 0 accepted, `rep` 1 refused with exit 2; without S0 both refused". This matches:
- the section 6.3 intro (D:412): the smoke row needs G-BASE, G-PINS, S0, S2 and Spike 4, and rows with `rep` ≥ 1 also need S3;
- AC-2 (D:441), which now points to a test that exists. This clears review 2's note about it.

### Section 6.3 intro and AC-2 (D:412, D:441)
- They agree with each other and with line D:77, where `launch.sh` enforces the gate order.
- There is no self-dependency: S3's collab-0 half and Spike 4's collab-0 rows need only G-BASE and G-PINS.
- Not blocking: the preflight list in step 1 (D:316) does not list the `gate0.json` check, although D:77 states it.
