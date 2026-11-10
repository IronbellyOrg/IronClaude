model: claude-opus-5-5 family: claude rung: top family-fallback: the GPT T1 model gpt-6.1-sol (T1Model02) has no verified spawn path in this harness (refs/retry.md "GPT spawn path: none verified"); adviser B ran on the strongest reachable model; Agent model parameter: opus
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T3.AC1 | **Separators.** Both rounds left T3.AC1 unmet for two causes: separators chosen wrongly where reverted and kept text meet (review-1.md:6, review-2.md:8), and an incomplete `depends:` closure (review-1.md:7, review-2.md:9). The rebuild picks a separator only from the emitted unit's own side or the unit before it there (attempt-2.diff:203). It stores an equal unit's base counterpart but never uses it to choose the separator (attempt-2.diff:205), so a revised separator carrying a table row's closing ` \|` lands after restored base text. Any such defect then trips the re-check safety net at attempt-2.diff:284-289, which restores the whole baseline and drops in-budget fixes. The source only allows a whole-baseline restore when the raw size check still fails (source.md:62, plan:92). **Depends.** `stale` collects only entries named as a hunk's claimant (attempt-2.diff:265), and the closure test at attempt-2.diff:234 never sees an entry whose quote is not in the baseline, which has no claimant (attempt-2.diff:161-162). | Choose each separator from adjacency in the output, using either side's index. Check every point where the output switches sides by splitting the rebuilt text into units again and requiring the exact expected unit sequence. Delete the re-check safety net. Define a reverted entry as source.md:50 does (no kept hunk attributed to it) and close `depends:` over those entries. |
| T3.AC2 | Marked met (review-2.md:5). But the table is the last block of `PROP_BASE` (attempt-2.diff:476-477), so no edit ever deletes the sentence after a table row, which is how the reviewer's 32-in-1,500 failures arose (review-2.md:8). The only guard was the safety-net label (attempt-2.diff:530), which says nothing about whether in-budget fixes survive. | Keep `Random(346)` and the 200 cases on `PROP_BASE`. Add 200 cases on a second base with a table between paragraphs and a heading after it. Assert that kept findings survive, not that a label is absent. |
| T3.AC3 | Met. The only write is the atomic spec write (review-2.md:6, attempt-2.diff:290-291). | Keep it. The new checks run in memory only, and nothing else is written. |
| T3.AC4 | Met: 64 passed and lint clean (review-2.md:7, extras-2.log:3-4). | Keep. Re-run after the changes. |

differs-by: no re-check safety net. Each separator where the output switches from base text to revised text, or skips a unit, is picked from a fixed candidate list by splitting the rebuilt text into units again and requiring the exact expected unit sequence. A bad separator is fixed where it occurs instead of throwing away every fix. The whole baseline is restored only when the raw size check fails.

steps:
1. Re-apply these parts of attempt-2.diff unchanged, since no review faulted them (review-1.md:3-5, review-2.md:5-7): the `btail` addition in `analyze` (:94-110), `split_region` (:21-71), `new_key` and `attribute` (:142-185), `moved_closure` (:239-256), the `cmd_check` dispatch (:310), and the tests at :327-463 and :535-596. The property test at :466-532 is rewritten in step 6.
2. Replace `depends_closure` and `stale` (attempt-2.diff:225-236, :265, :278) with a closure over entries:
   - `kept` = hunks with `h.entry` set whose `h.entry.finding` is not in `bad`.
   - A reverted entry is any ledger entry that has no hunk in `kept`. This covers unattributed entries with a claimant (F1.2), entries whose quote is not in the baseline (F2.2), and entries with no hunk at all.
   - Loop until nothing changes: any entry whose `depends:` names a reverted entry adds its finding to `bad`.
   - Run the closure before the cycle-cap loop and after each cap revert. Keep the cap ordering at attempt-2.diff:272-273.
3. Rewrite `rebuild` (replaces attempt-2.diff:192-222). Build the list of output units:
   - Equal unit: revised unit `j`, with `bidx=i` and `ridx=j`.
   - Kept part: its revised units, with `ridx=j` only.
   - Reverted part: its base units, with `bidx=i` only.

   Separator before unit Y, given the previous unit X:
   - `rseps[Y.ridx]` if both have `ridx` and `Y.ridx == X.ridx+1`.
   - Else `bseps[Y.bidx]` if both have `bidx` and they are consecutive.
   - Else it is a junction (step 4). The first unit uses `rseps[0]` or `bseps[0]` when its index is 0, else it is a junction.

   Tail: `rtail` if the last unit has `ridx == len(ru)-1`; else `btail` if it has `bidx == len(bu)-1`; else `rtail`. With an empty revert set, the output must equal `rev_text` byte for byte.
4. Junction check. Go left to right. At each junction, take the first candidate for which `units(<text so far> + sep + Y.raw)` gives exactly the expected norms up to Y. Candidates, in order:
   - (a) Y's own-side separator before Y.
   - (b) X's own-side separator after X (or that side's tail if X is last on its side).
   - (c) X's trailer (X-side text after X up to the first `\n`) + `\n\n` + Y's leader (Y-side text after the last `\n` before Y; if that separator has no newline, `| ` when `Y.kind == "cell"`, else empty).

   After the last junction, compare `units(full)` norms with the expected norms once more. If no candidate fits, or the final comparison fails, call `fail("INTERNAL", ...)` before writing anything.
5. In `enforce` (attempt-2.diff:258-299), delete the `recheck` branch (:284-286). Restore the whole baseline only when the rebuilt size minus the baseline size is above `RAW_SIZE_LIMIT`, and then list every blocking id. Keep the write-if-changed step, the re-read and the exit code from the re-check.
6. Tests in `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/tests/skills/test_sc_fixcheck.py`:
   - The F2.1 repro from review-2.md:8. Assert the spec equals the baseline with only F1's replacement, and `restored-baseline=no`.
   - The F2.2 repro from review-2.md:9. Assert `reverted=` includes F1 and L1's text is gone.
   - An entry with no hunk at all, whose dependant gets reverted.
   - An empty revert set leaves the bytes identical.
   - Property test: keep the 200 `Random(346)` cases on `PROP_BASE`. Add 200 cases on a second base: a paragraph, then a table, then a paragraph, then `## Tail` and one sentence. `random_edit` gains a cell edit and a deletion of the sentence after a table row. Drop the `reason=recheck` assertion (attempt-2.diff:530). Instead, when the output says `restored-baseline=no`, assert that every finding with `status=fixed` in a plain `check` before `--enforce`, and not in `ENFORCE reverted=`, has the same finding line after `--enforce`. Keep the plain-`check` exit-0 assertion.
7. Run `uv run pytest tests/skills/test_sc_fixcheck.py -v` and `make lint`. As a local shake-out (not committed), run 2,000 property cases on each base with a few extra seeds, and record the counts in `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/artifacts/t3-extra-seeds.txt`.

Not handled by this design: a revert that restores only one of a pair of fence markers flips the code-block state for the rest of the file. Step 4 then fails with exit 70 and writes nothing, instead of failing silently. No review raised it, and the fuzz bases contain no fences.
