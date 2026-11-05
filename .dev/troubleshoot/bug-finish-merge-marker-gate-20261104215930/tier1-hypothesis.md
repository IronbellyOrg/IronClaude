# Hypothesis: the finish gate checks a narrower view of the index than `git commit` records (marker width fixed at 7, entries compared by blob id only), so wider markers and mode/type changes pass

**Agent**: root-cause-analyst (lens; worker troubleshoot-analyst)
**Tier**: 1
**Timestamp**: written by the parent on receipt (see audit.log)
**Cause class**: Logic regression (a design gap the script follows exactly: the gate predicate is weaker than the property it proves)
**Claim class**: `mixed`
**Evidence class**: `runtime_observed` (parent probe, tier1-observation.md ## Probe)
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned (script follows source.md:817-818 literally; the fix moves it toward the purpose stated at :818)
runs-in=src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:208 and :246-249 @ local operator checkout (bash, git)

producer-citation-check: skipped — menu absent or empty (producers.md: observation-kind trace, header-only table)

## Claim
One root cause: the finish gate checks a narrower view of each index entry than the commit records. Step 4 counts only lines starting with exactly 7 marker characters (:208), while git sizes markers from the `conflict-marker-size` attribute and the merge command does not override it (conflict-mechanical.md:76). Step 5 compares only blob ids (:246-248); a blob id excludes the file mode, so a staged mode change (or file vs symlink with the same bytes) outside the manifest gives equal ids and is committed.

## Evidence
| # | Kind | Source | Content |
|---|---|---|---|
| E1 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:208 | width fixed at 7; used for the staged blob (:224) and the stage-1 blob (:229) |
| E2 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:76 | merge command with no marker-size override |
| E3 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh:246-249 | index vs merge-tree compared by object id only |
| E4 | test_assertion | tests/pr_submit/test_conflict_scripts.py:775-827 | F2-F5 cover 7-wide markers and content-only staging; no attribute or mode test |
| E5 | command_output | tier1-observation.md `## Probe` | parent-run falsification probe on the unfixed script (see that section) |

Git behaviours: (a) markers are written at the conflict-marker-size width; (b) a blob id hashes bytes only, mode lives in the entry; (c) `git diff --cached --name-only <tree>` lists mode-only differences. behaviour-definition: rows 1-3 (behaviour-definitions.md).

## Proposed Fix
(A1) Step 4: read the width per manifest path with read-only `git check-attr -z conflict-marker-size -- "$path"` (third NUL field); default 7 when empty or not a positive integer; `count_markers <file> <width>` builds `^(<{w}|[|]{w}|={w}|>{w})( |$)`. Exact width (not `{7,}`), same width for the stage-1 blob, token `markers` unchanged.
(C2) Step 5: replace the union + blob-id comparison with one read-only `git diff --cached --name-only --no-renames -z "$MT_OID"` (index vs merge tree: content, mode and type); any listed path not in the manifest fails `staged_unexpected "the index differs from the merge-tree result at $path"`.
No git write command added; `--no-renames` kept; exactly one `git commit` match; no stash/force/merge/add/checkout words.
Files: finish-merge.sh (:205-251); tests/pr_submit/test_conflict_scripts.py (F2b attribute width; F6 mode change; F6b symlink swap). The archived design (.dev/tasks/done/.../source.md) is not edited; the deviation is recorded in the PR reply.

## Confidence
Self-reported 0.65 (calibrator re-grades).

## Risks
- A1: check-attr reads attributes at finish time; a .gitattributes change during the merge could differ from the width git used. Unknown width values fall back to 7.
- C2: diff.ignoreSubmodules could hide gitlink changes (same exposure as today); `--ignore-submodules=none` closes it.

## If I'm wrong, it's probably because...
`git diff --cached --name-only <tree>` omits mode-only entries, or git ignores the attribute when writing markers.

## Falsification standard
F2b and F6 against the UNFIXED script: A1 is disproved if F2b returns `FINISH_FAIL markers`; C2 is disproved if F6 returns `FINISH_FAIL staged_unexpected`. The claim predicts exit 0 with a merge_sha in both.

## Alternatives considered
- `{7,}` widening: rejected (false halts on reST/Markdown underlines; misses widths below 7).
- per-path `ls-files -s` vs `ls-tree`: rejected (pathspec globbing; two calls per path).
