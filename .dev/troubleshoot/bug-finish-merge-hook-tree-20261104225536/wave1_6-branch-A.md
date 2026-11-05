# Wave 1.6 Branch A (log-call inspection), persisted on receipt; degraded: false

query_target: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh (lines 271-298, steps 6-9)

| line | call_type | level | richness | note |
|---|---|---|---|---|
| 272 | handler | none | n/a | `git commit -F` stdout+stderr to $TMP/commit.out; hook output lands there too |
| 273-274 | handler | error | rich | output replayed verbatim, then `hook_rejected` (covers every commit failure) |
| 276 | print (stderr) | info | rich | on success, commit and hook output replayed to stderr |
| 279 | handler | none | silent | rev-list stderr discarded; failure becomes an empty PARENTS_LINE |
| 283-286 | handler | error | rich | parents_mismatch prints the parents line and expected ids |
| 289-290 | handler | error | rich | git status failure reported with stderr |
| 291 | handler | error | minimal | tree_dirty without path or new SHA |
| 292 | handler | error | minimal | stderr discarded; exit 1 and >1 both tree_dirty |
| 295-296 | print (stdout) | info | n/a | success JSON: merge_sha and parents only, no tree id |
| 297 | handler | error | minimal | jq failure after the commit labelled usage |

- Nothing reports that a hook changed the staged content: no record of the index before the commit, no comparison of HEAD^{tree} after it. A re-staged hook edit is committed silently; an unstaged one is caught only as a bare tree_dirty after the commit landed.
