# Wave 1.6 Branch A (log-call inspection), persisted on receipt; degraded: false

query_target: src/superclaude/skills/sc-pr-submit-protocol/scripts/finish-merge.sh

| line | call_type | level | richness | note |
|---|---|---|---|---|
| 44 | print (stderr) | error | n/a | fail(): `finish-merge: <detail>` is the only free-text diagnostic channel |
| 45 | print (stdout) | error | n/a | `FINISH_FAIL <reason>`; `markers` shared by 4 sites, `staged_unexpected` by 3 |
| 208 | handler | none | silent | count_markers: width-7 regex; other widths add 0; nothing printed on pass |
| 210 | handler | none | silent | grep rc>1 returns silently |
| 221 | handler | none | silent | step 4 skips any path whose `:0:` lookup fails, unlogged |
| 223 | handler | error | rich | staged blob unreadable: git stderr + path |
| 224 | handler | error | minimal | "cannot count markers in <path>" |
| 228 | handler | error | rich | stage-1 blob unreadable (token `usage`) |
| 229 | handler | error | minimal | stage-1 count failed |
| 232 | handler | error | rich | introduced markers: path + both counts (fires only for width-7 markers) |
| 237, 239 | handler | error | rich | diff failures with git stderr |
| 246, 247 | handler | none | silent | rev-parse errors swallowed; blob id only, mode never read |
| 249 | handler | error | minimal | staged_unexpected names the path, not the compared ids or the list it came from |
| 193 | handler | error | rich | unmerged paths listed |
| 201 | handler | error | minimal | tree_dirty without a path |
| 256 | handler | error | rich | commit output replayed verbatim |
| 268 | handler | error | rich | parents_mismatch with values |
| 277 | print (stdout) | info | n/a | success JSON; no record that steps 4/5 ran |

Summary: failures are attributable by token + stderr detail; the two defects are silent false passes (no output on the passing path), which a hermetic regression test observes directly through exit code and the resulting commit.
