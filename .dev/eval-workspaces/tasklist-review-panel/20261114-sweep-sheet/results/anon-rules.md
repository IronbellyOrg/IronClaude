# Redaction rules of the blind-judge anonymiser (step 0.6)

Source read: `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/tmp-scripts/anon-b11.sh` (the script that made the
`merged-anon.md` files of the earlier study). No ground-truth or score file was opened.

## What anon-b11.sh does, in order

1. Picks a random one-letter label from `Q R S T U V` that is not yet a folder under the combo, writes
   `label-key.json` (`label`, `combo`) next to it and the report to `<label>/merged-anon.md`.
2. Replaces the whole study root (`$EVAL`) with `<EVAL>` (`sed "s|$EVAL|<EVAL>|g"`).
3. Finds reviewer ids with `\bt[0-9a-z]+-[0-9]+\b`, sorts them (`sort -u`) and replaces the k-th with `R<k>` with
   `sed -i "s/\bID\b/R<k>/g"`.
4. Blanks the path of the candidate line: `candidate: <EVAL>/.../candidate.md sha256` becomes
   `candidate: <candidate file> sha256`.
5. Blanks every report path of the reviewers list: `report <EVAL>/...` becomes `report <redacted>`.

## What bin/anon.sh keeps, changes and adds

| Rule | anon-b11.sh | bin/anon.sh |
|---|---|---|
| random label | one letter, six values | `j` plus six hex digits (16.7 million values), never an existing folder of the output root |
| root paths | `$EVAL` only | the run folder, `SB`, `EVAL`, `SW` and `REPO`, each to `<RUN>`, `<SB>`, `<EVAL>`, `<SW>`, `<REPO>` (the run folder first, because it sits under `SW` or `/tmp`) |
| candidate line | `candidate: <EVAL>/... sha256` only | any `candidate: ... sha256` line |
| report paths | `report <EVAL>/...` | `report <RUN>...` (a path tagged by an earlier rule) and `report /...` |
| reviewer ids | `t[0-9a-z]+-[0-9]+`, sorted, `R1..Rn` | `t[0-9]+[a-z]*-[0-9]+` plus every id named in the reviewers list, sorted, `R1..Rn`; word boundaries, so `test-1` is not an id |
| key file | written in the combo folder (names the combo) | none: the caller (`bin/judge-batch.sh`) keeps the label-to-run key in the run folder, never in the scoring folder |

## Why

The judge reads `merged-anon.md` by a path that contains the label only, so the path names no arm, run, reviewer or model
(REQ-43). Both the file name and the text must carry nothing the report itself does not already carry.
