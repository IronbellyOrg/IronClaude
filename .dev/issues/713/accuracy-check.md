## Accuracy check for #713

**Verdict:** current

Checked against `origin/master` at `2ea524514154bde03258a7d7d8a0265c371609af`, and the pull requests merged since the issue was opened (0, list truncated: no).

| # | Claim in the issue (quoted) | Status today (still true / changed / gone) | Evidence (path:line, PR #number or commit) |
|---|---|---|---|
| 1 | "Disposable target for the #442 live observations (T2)." | still true | #442 remains open and requests real-session launch-level observations using disposable work. At the checked commit, `.dev/issues/442/observation-runbook.md` explicitly uses `ob-442/$t.txt` with content `ob-442 $t` for disposable observation targets. This establishes purpose, not a claim that any observation passed. |
| 2 | "create the file ob-442/T2.txt" | still true | At the checked commit, `git ls-tree -r --name-only origin/master -- ob-442` returns no entries. Direct filesystem inspection also reports that both `ob-442/` and `ob-442/T2.txt` do not exist in this checkout. Creation remains outstanding. |
| 3 | "holding the single line ob-442 T2" | still true | The target file is absent, so the requested content has not been delivered on the checked default branch or in this checkout. The observation runbook's target naming/content pattern agrees with this request. |
| 4 | "The only change wanted" / "Touch nothing else." | still true | These are scope requirements. #713 has no comments changing them; the scout lists no merged pull requests or default-branch commits since creation, hence no changed files to assess. No guard, configuration, or test changes are requested. |
| 5 | "Close without merging anything." | still true | #713 is OPEN and has no comments revising this instruction. This is the requested completion rule, not permission for this accuracy-check worker to close anything. |
| 6 | "The observation run's governed sessions (T2)" | still true | This states the intended audience. The runbook defines disposable observation targets; whether this particular T2 session has run is Not known yet. |

Directory convention checked: the default-branch observation runbook explicitly prescribes this disposable `ob-442/<target>.txt` pattern. No matches for that path pattern were found in the searched `src/`, `docs/`, or `tests/` trees. The checkout's `.dev/README.md:3-7` gives a general rule placing development workspaces and iteration outputs under `.dev/`; it does not document `ob-442/` as a reusable product directory. Keep this issue's explicit disposable target separate from general development outputs; there is no evidence that the requested path has become obsolete.

### Merged pull requests that touch this issue

| PR | Title | Relevant files | Effect on the issue |
|---|---|---|---|
| None | None merged since creation | None | No intervening merged pull requests or changed files were listed in `scout.md`. |

<!-- sc:issue:accuracy-check -->
