VERDICT: PASS

## Blocking defects

None.

## Notes (do not change the verdict)

1. Priority wording. The live issue's own Priority section says "Medium" (degraded behaviour with a workaround, rule table in refs/create.md line 77), and its severity is "medium". findings.md says "P1" and cites the workaround only as the reason for "Not P0". The scale P0/P1 is not the issue's Urgent/High/Medium/Low scale, and findings.md does not say how P1 maps to the issue's "Medium". This is a judgment call, so it is a note: state the mapping or the reason for rating above the issue.
2. Next step 3 says to keep `ALLOWED_ORCA` unchanged "unless a new call is needed". Following the `worker-list` cursor needs a new `worker-list` template with a cursor flag. The code only has the one `worker-list --run <run> --json` template (`probes.py:58`, built at `:131`), `probes.py:1157` reads only `page.hasMore`, and `tests/sweep/test_probes_allowlist.py:372` pins `len(set(ALLOWED_ORCA)) == 10`. Issue 757 (body, line 97) also says the sweep package keeps "10 read-only Orca commands". So that step very likely touches the pinned allowlist and the 10-command claim, and whether Orca has a cursor flag is not checked anywhere (UNVERIFIED). The hedge in the text keeps the sentence true, but the size M estimate is not harmed.
3. "Blocks #757": issue 766 (Related issues) says a watcher "could never see a class change" for these workers, which supports a soft dependency. Issue 757 itself lists "changing what the sweep classifies or probes" as out of scope, so "blocks" is better read as "limits the usefulness of".
4. Step 1 says to anchor "the quoted form" too. `_QUOTED_CONTRACT_RE` (`probes.py:1089`) requires a quote directly before a `/`, so a quoted relative path is not matched today. Only the bare regex (`:1087`) has the problem. Harmless extra wording.
5. WC-16 is cited without a line. The issue cites `WORKER-CONTRACT.md:290`. The heading is at line 288 and the loop text at 290. Fine.

## Verified as true

- Live issue 766: OPEN, label `bug`, created 2026-11-24T17:18:29Z, 0 comments. It states the three causes and the checkout commit 0dd726d18. It does not say how to resolve the 590 overlap beyond relating them, and its Related section proposes the 590 merge, matching step 5.
- Code at HEAD a7ae3dd30: `_CONTRACT_PATH_RE` at `probes.py:1087` has no left boundary. `_contract_candidates` is at `:1092`. Outside root is recorded at `:1415`. `report_folders` is at `models.py:29-42` and resolves relative folders against the worktree. `NOTE_TAIL_ONLY` is defined at `classify.py:58`, added at `:624`, and `_force_unknown` is at `:358-366`, applied at `:961`. `TRANSCRIPT_TAIL`, `WORKER_LIST_PAGE` and `shows` are at `probes.py:88`, `:89`, `:129`. `:1157-1161` sets `state.truncated` and never follows the cursor.
- `git log` for `src/superclaude/cli/sweep` ends at b46ecc1bd (2026-11-16, PR 579), preceded by 4d3c0b126 (PR 539). Nothing newer. The package is unchanged since the commits named.
- `gh pr list --state all --search 766` returns `[]`: no PR for 766.
- States: #590, #757, #534, #706, #339 are all OPEN. PR 539 MERGED 2026-11-14; PR 579 MERGED 2026-11-17T00:29:45Z (commit dated 2026-11-16 in git).
- `ALLOWED_ORCA` is 10 templates at `probes.py:49-60`; the test directory `tests/sweep/` exists with the named files.
- Required headings are present in the required order; no placeholders; the unmeasured figures and the intent of tail-only forcing are marked UNVERIFIED.

## What I checked

Read findings.md in full; re-read the cited lines in `probes.py`, `classify.py`, `models.py`; ran `git log` on the sweep package; ran `gh issue view` for 766 (body and comment count), 590, 757, 534, 706, 339; ran `gh pr list --search 766` and `gh pr view` for 539 and 579; checked the allowlist test pin and the cursor handling. I did not run tests, and did not re-measure the live Run figures.
