## Response to criticisms (each, counter-evidence or concession)
1. **R2-1 at medium.** Concession. The same bullet already says the count is 0 and "no backslash before a backtick" (`TASK-WF-spec-20261022-211556.md:94`). The span is not copyable, but the pass rule is. Low is the right label. The fix is still a fenced command.
2. **R2-3 reopens a closed decision.** Concession. `source.md:35` and `source.md:44` already say one paragraph and change nothing else. `TASK-WF-spec-20261022-211556.md:26` and `:150` already list the neighbors. A question before Task 9 adds a stall, not new information.
3. **INF-045 "partial, where null".** Concession. A partial needs a location. The tasklist never mentions the 300-vs-3,000 note (`TASK-WF-spec-20261022-211556.md:17-28`, `:146-160`; `source.md:47`). The verdict is gap.
4. **R2-6 low vs R2-4 medium.** Counter. They are not the same defect. R2-6 is a line slice on text that other Task 5 bullets also touch (`TASK-WF-spec-20261022-211556.md:88-91`). R2-4 is the only check on those README paragraphs and the badge (`TASK-WF-spec-20261022-211556.md:141-143`). A wrong badge or "this job is not advisory" has no second net. Medium there, low on the slice.
5. **Two of ten findings are matrix bookkeeping.** Concession. R2-9 and R2-10 say "No tasklist edit". They do not support `not_ready`. Eight findings are about the tasklist; those two are not.

## Updated assessment of Variant 1
Variant 1 is the stronger defect list. It found the warning bullet that passes a deleted or non-advisory sentence (`TASK-WF-spec-20261022-211556.md:90`) and the sync check that never diffs the unchanged commit body, including `git add -f docs/.framework-sync-commit` (`TASK-WF-spec-20261022-211556.md:112-113`, `pull-sync-framework.yml:89-105`). It also found the throwaway-repo and render-SHA setup gaps. Its Round 2 move on X-001 is right: `not_ready` means rewrite those bullets, then run. It does not mean the scope or Fix 1-4 coverage is wrong. What it still underweights is Task 8 and `<decided file input>` (`TASK-WF-spec-20261022-211556.md:124`, `:141-143`), both of which it has now conceded.

## New evidence
`pyproject.toml:38` declares `"pyyaml>=6.0"` inside `dependencies`. The orchestrator check shows `gh` is authenticated and `can_approve_pull_request_reviews` is `true` (`artifacts/shared-assumption-checks.md:3-5`). `.venv` and `uv.lock` are gitignored (same file, lines 8-9). A-002 is resolved in Variant 1's favor. A-003 stays unverified because pytest was not run.

## Final per-point positions for the 5 unresolved points (table: point | winner V1/V2/tie | one-line reason)
| Point | Winner | Reason |
|---|---|---|
| C-001 | tie | The span at `TASK-WF-spec-20261022-211556.md:94` is uncopyable, but the parenthetical states the rule, so the fight is only the severity label. |
| C-003 | tie | Both replace the line slices at `:88` and `:91` with a text anchor; Variant 1's block assertion is the stronger of the two same fixes. |
| C-005 | tie | The linear chain still runs Task 7 after Task 2, so `source.md:40` is misstated, not broken. |
| X-001 | V2 | `:90`, `:113`, and `:143` pass a wrong edit, and `source.md:38` makes that a gate. |
| A-002 | V1 | `pyproject.toml:38` declares `pyyaml>=6.0`, so `uv run` can import it. |