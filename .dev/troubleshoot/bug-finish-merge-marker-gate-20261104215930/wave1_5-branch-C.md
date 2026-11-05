# Wave 1.5 Branch C (semantic restrictions), persisted on receipt; degraded: true (auggie not in the analyst roster; Grep/Read fallback)

| source_file:line | quoted_text (abridged) | applies_to |
|---|---|---|
| source.md:817 | step 4 counts lines matching `^(<{7}|\|{7}|={7}|>{7})( |$)`; count must not exceed the stage-1 count | A1: widening departs from the literal spec text; must stay a relative count (introduced markers only); deleted paths stay skipped |
| source.md:818 | step 5: index blob must equal merge-tree blob for non-manifest paths, both absent equal; "proves the commit changes nothing beyond the auto-merge result plus the resolved paths" | C2: a mode comparison serves the stated purpose; keep --no-renames, manifest skip, both-absent-equal, token staged_unexpected |
| source.md:1176 | INV-016 `--no-renames` on every diff feeding the finish gate | any new diff-type read carries --no-renames |
| source.md:1163 | OQ-25 decided: unresolved paths equal the probe's merge-tree blob | C2 extends this decision |
| source.md:756 | script rules: set -u -o pipefail, one stdout line, details on stderr, exit 0/2, temp files under the git dir, no push/stash/config write/hook-skip/amend/src path | all fixes |
| source.md:797 | finish gate changes the repository only by one commit | fixes add read-only inspection only |
| source.md:824 | FINISH_FAIL token to halt-reason map | reuse `markers` (A1) and `staged_unexpected` (C2); no new token |
| finish-merge.sh:19-26 | one-line stdout contract; closed exit-token list | no stdout diagnostics; no new token |
| test_conflict_scripts.py:1068-1088 | static rules: exactly one `git commit` match, no stash/force words anywhere, no git add/checkout/reset/config, no gh | new text must avoid these words, including in comments |
| test_conflict_scripts.py:770 (F2), :788 (F3) | introduced marker detected; marker already in stage-1 not counted | A1 fix keeps relative comparison |
| test_conflict_scripts.py:802 (F4), F5 | staged_unexpected with the path on stderr | C2 fix keeps the path in the detail |
| test_conflict_sync_protocol.py:419 | FR-21 prohibited-operation scan | same rules |

Conclusion: no restriction forbids widening the marker match or adding a mode comparison; both are extensions consistent with the stated purpose and must keep the token set, stdout contract, static-text rules and F2-F5 green.
