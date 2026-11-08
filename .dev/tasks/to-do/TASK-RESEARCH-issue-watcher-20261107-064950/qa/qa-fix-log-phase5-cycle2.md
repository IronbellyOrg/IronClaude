# Fix log: Phase 5 synthesis gate (Gate 2), fix cycle 2

**Date:** 2026-11-07
**Agent:** rf-qa (fix_authorization: true; the only agent allowed to edit synthesis files in this cycle)
**Input:** `qa/qa-consolidated-findings-phase5-cycle2.md` (1 blocking finding; no minor findings listed)
**Edit scope:** `synthesis/synth-04-plan-questions-evidence.md` only. No research file edit. Targeted Edit calls only.

Status: Complete (one entry for the single blocking finding below, then a summary).

---

## Finding 1 (consolidated #1): the truncation guard tested the filtered page length, so it could not fire

**Status:** FIXED. Eight targeted edits, all in `synthesis/synth-04-plan-questions-evidence.md`.

Problem confirmed by reading the file: the guard in step 4.2 and the "Truncated read" scenario tested "still full (100 items)", but `events-jq` and `marker-jq` (call-table block) already reduced each page to label events or comment ids, so a raw page of 100 holding 40 label events came back with 40 items and the guard could not fire.

| Place (line numbers after the edits) | Change |
|---|---|
| jq block (lines 194-195) | `events-jq` and `marker-jq` now return `{n: length, items: [...]}`: `n` is the raw page length taken before any `select`, `items` the filtered list as before |
| paragraph after the jq block (line 198) | Added the rule: the page-end test uses `n`, never the length of `items`, with the 100-events/40-label-events example; marked [DESIGN] and tied to the repo precedent `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh:69-70` (`count="$(jq 'length' ...)"`, then `if [ "$count" -lt 100 ]` ends the read) and `:74` (fails when the end was not reached) |
| call table, "Label events" and "Own claim marker" rows, Returns column (lines 190-191) | Returns now says per page `{n, items}` (raw page length plus the filtered list) |
| step 4.2 (line 205) | Replaced "still full (100 items)" with: pages are read while `n == 100`; a page with `n < 100` ends the read with a complete list; if page `max_pages` is read and `n` is still 100, both `label_events` and `own_claim_comment_ids` raise `CommandError("E-GH-TRUNCATED")`; the test is on `n`, not `len(items)`; an output that is not an object with integer `n` and list `items` raises `E-GH-FAILED` |
| step 4.4 fixtures (line 207) | Events and comments fixtures are RAW REST pages (before any jq filter), so the filters and `n` are exercised |
| step 4.5 (line 208) | Truncation tests now use raw pages of 100 events with fewer than 100 label events (for example 40), served through the real filter string (`jq -c` on the raw fixture) as `{n: 100, items: [40 entries]}`; added the case that a raw page with `n == 100` and fewer than 100 filtered items does NOT end the read; a raw page with `n < 100` ends it. Applies to both `label_events` and `own_claim_comment_ids` |
| step 6.1 (PATH stub installer, line 295) | For `gh api ... --jq <filter>` the stub pipes the raw fixture page through `jq -c "<filter>"` with the filter it received, so the real filters produce `{n, items}` in the e2e tests [DESIGN] |
| "Truncated read" scenario (line 283) | Rewritten: raw pages of 100 with fewer than 100 label events (filtered `items` shorter than 100 while `n == 100`) for every page up to `max_pages` give `approval-unverifiable` (no `orca` call, no store write); the comments fixture likewise gives `claim-marker-unverifiable`; a page with `n == 100` and short filtered items followed by a page with `n < 100` is read to its end and decided normally; a single page with `n < 100` is decided normally |

Unchanged on purpose: run_cycle steps 5 and 6 and the `approval-unverifiable` / `claim-marker-unverifiable` mapping (they depend only on `E-GH-TRUNCATED`, whose trigger is now correct); the `max_pages = 5` [PROPOSAL] value.

Evidence read this session: `synth-04` lines 170-295 before the edits and a Grep of the edited places after; `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh:47` (fail-incomplete comment), `:69-70` (raw `length` test against 100), `:74` (`[ "$completed" = true ] || return 1`). Every new statement is either that file:line or the logic of the plan itself, labelled [DESIGN] or [PROPOSAL]. No external or doc-only claim added.

Verification: Grep over `synthesis/` for `still full` returns no hit; `n == 100` / `n < 100` appear in the step 4.2, step 4.5 and "Truncated read" lines; `{n: ` appears in both jq filters and step 4.5.

---

## Summary

| Item | Count |
|---|---|
| Blocking findings in the input | 1 |
| Blocking findings fixed | 1 |
| Blocking findings not fixed | 0 |
| Minor findings fixed | 0 (minor findings stay notes) |
| Files edited | 1 (`synthesis/synth-04-plan-questions-evidence.md`) |
| Research files edited | 0 |
