## Response to criticisms

- The `-z` rename order in R2-3 is wrong. A throwaway rename prints `R  new\0old\0`: the new path comes first, then the old path. R2-3 said "status, then old path, then new path." That is the non-`-z` order, reversed. Once both paths are recorded as their own lines, `TASK-WF-specR1-20261023-031725.md:184` already fails a new path outside the allow-list. The part still missing from the plan is hashing the old path as `MISSING`, which is Variant 1's half (`source.md:70`).
- R1-1 and R1-2 stand. Variant 2 never filed them. They remain the strongest mediums: the hash `cmp` at `TASK-WF-specR1-20261023-031725.md:183` has no tooling exemption, and `:128` locks `--head` only on `gh pr create`.
- R2-2 over-claimed. Already conceded. `source.md:39` and `source.md:70` set the final check at directory level, and `:184` follows them.
- A-001 was rejected only because the runner was unverified. That was wrong. `~/.claude/skills/sc-implement-protocol/SKILL.md:97` says "Default sequential in source order" and "Unmarked = sequential." This tasklist marks no task `independent` or `parallel-ok`, so Tasks 3–6 run before Tasks 8–9. That does not make the Depends graph meet `source.md:82`. That miss stays settled for Variant 2 under C-002 and X-002.

## Updated assessment of Variant 1

Variant 1 is the stronger card on checks that pass a wrong edit or fail a correct run. R1-1 and R1-2 are real, R1-6 has the rename order right, and the Round 2 concessions on R1-3, R1-7, R1-8, R1-9, and the Task 8 positive-check claim are correct. The ancestor gap is still a literal `source.md:82` miss, and the orchestrator's renumbering (Codecov research immediately before the Codecov edit, then one chain `2→1` … `9→8`) shows both sentences of that line can hold at once. Variant 2's example chain was the weaker fix. "not_ready" is still the right label, because of R1-1 and R1-2, not because of the directory scope check.

## New evidence

- Rename bytes, then the temp directory removed: `52 20 20 6e 65 77 00 6f 6c 64 00`, which is `R  new\0old\0`.
- `~/.claude/skills/sc-implement-protocol/SKILL.md:97`, read directly: sequential in source order unless the source marks a set independent. This tasklist does not.
- `artifacts/shared-assumption-checks.md:15-16`: renumbering 1 baseline, 2 GitHub settings, 3 three-dot proof, 4 boundary-guard, 5 sync, 6 Codecov research, 7 Codecov edit, 8 workflows README, 9 scope. Task 7 still depends on the research task, not on the sync task, and Tasks 8 and 9 then have every earlier edit as an ancestor.

## Final positions for C-001, C-003, C-004, X-001, X-003, A-001

| point | winner | reason |
|---|---|---|
| C-001 | V2 | `source.md:39` and `:70` set a directory check; `:184` follows it. Contract3 (`source.md:46-47`) is a low residual. Conceded by Variant 1. |
| C-003 | V1 | Measured `-z` order is new path, then old path. R2-3 reversed it. The unfilled rule is `MISSING` for the old path; line 184 already fails an out-of-allow-list new path once it is recorded. |
| C-004 | V2 | `source.md:55` requires the word `advisory`; `:96` enforces it. A reword without that word is a wrong edit. Only the looser instruction at `:84` remains. |
| X-001 | V2 | Not ready. R1-1 and R1-2 are the medium class `source.md:51` already refused. "ready_with_notes" understates them. |
| X-003 | V2 | C3 is not a plan defect. Same reason as C-004. |
| A-001 | V1 | ACCEPT. `SKILL.md:97` verifies sequential source order, so the Round 1 REJECT is withdrawn. That runtime fact still does not satisfy `source.md:82`, which stays Variant 2's under C-002 and X-002. |