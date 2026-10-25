## Response to criticisms

- **R1-12 (Task 9's positive check catches a premature run).** I concede this is wrong for Task 8. Task 8's acceptance bullets (`TASK-...md:163-168`) read only the README, never the workflow files. A README written before Tasks 5 and 6 would pass. Task 9's positive check (`:185`) only gates Task 9. My "optional" severity was too low. The orchestrator's renumbering (research task immediately before the Codecov edit, then a single-parent chain 2→1 … 9→8) shows `source.md:82` can be met in full, so the gap is a real, fixable spec miss. I withdraw the log-precondition idea as the primary fix.
- **R1-9 (line 30) and R1-8 (premature conclusion).** I concede both. `source.md:81` lists the leftover lines and omits line 30, which is about retired local scripts, not the publish paragraph. `source.md:80` tells Task 9 to record the 3,000 conclusion for the user to confirm, and the plan does so (`:176`). Neither is a defect.
- **R1-3 (boundary-guard.yml whole-document comparison).** I concede it is not an M-10 requirement, because `source.md:57` names only pull-sync-framework.yml and test.yml. The risk is still real: `runs-on`, `env` and `fetch-depth: 0` (`boundary-guard.yml:38-48`) are unprotected. I downgrade it from "missed requirement" to optional hardening.
- **R1-7 (C3).** I concede. `source.md:55` makes `advisory` mandatory on the warning line. Omitting it is a wrong edit, and `:96` is the spec. The only residue is that the instruction at `:84` is looser than its own check, which V2 also noted.
- **R1-1 and R1-2 stand.** V2's Round 1 concedes both. They are the strongest mediums on either card.

## Updated assessment of Variant 2

- **R2-1 is right in substance.** The ancestor gap is a literal `source.md:82` miss. The orchestrator's renumbering shows it is satisfiable, and V2's example chain was the weaker fix (V2 concedes this).
- **R2-5 is a good catch.** Task 7's "do not edit t2" is checked only by the `Decision:` count (`:140,147`). I missed it.
- **R2-4 is a valid low point.** `ci.py:19,77` match only on `boundary`, so forbidding the bare word `required` in the job name (`:95`) is stricter than the source.
- **R2-2 over-claims.** V2 concedes `source.md:39` is directory-level.
- **R2-3 gets the `-z` order backwards.** The order error is immaterial in the end. Once both paths are recorded, line 184 already fails a new path outside the allow-list. The gap that remains is hashing the old path as `MISSING`, which is my half.
- **Verdict.** V2's "not_ready" is the correct label.

## New evidence

- **A-001 is verified at runtime.** `~/.claude/skills/sc-implement-protocol/SKILL.md:97` says "Default sequential in source order". Parallel runs need an explicit `independent` or `parallel-ok` marker. The tasklist marks none, so Tasks 3–6 do run before Tasks 8–9.
  - This confirms the prose rule at `:31` works in practice.
  - It does not make the Depends graph meet `source.md:82`, which is a structural requirement.
- **A source-valid fix exists for the chain.** The orchestrator's renumbering has Task 7 depending on the Codecov research task, not the sync task. That also resolves the "single-parent chain" worry I raised against V2.
- **Task 1 baseline.** The baseline `git status` I ran already lists 48 `.dev/reflect/` entries. Task 1 hashes those files, and Task 9's `cmp` (`:183`) has no exemption. R1-1 is therefore not hypothetical.

## Final positions for C-001, C-003, C-004, X-001, X-003, A-001

| point | winner | reason |
|---|---|---|
| C-001 | V2 | `source.md:39` sets the check at directory level and `TASK-...md:184` follows it. Contract3 (`source.md:46-47`) is a low residual, not a medium spec break. Conceded. |
| C-003 | V1 (narrow) | `source.md:70` needs deleted or renamed paths recorded. The unfilled part is hashing the old path as `MISSING`, which V1 states. V2's new-path-fails half is already covered by line 184 once both paths are recorded, and V2 has the `-z` order backwards. |
| C-004 | V2 | `source.md:55` makes `advisory` mandatory and `:96` enforces it. A reword without the word is a wrong edit, so there is no check defect. Only the looser instruction wording at `:84` remains. |
| X-001 | V2 | Cycle 1 was refused on medium acceptance defects with zero highs (`source.md:51,53,67`). V1's own R1-1 and R1-2 are the same class, so "ready_with_notes" understates them. |
| X-003 | V2 | Same reason as C-004. C3 is not a plan defect. |
| A-001 | V1 (ACCEPT) | `SKILL.md:97` shows sequential source-order execution, and the tasklist marks no task independent. My earlier QUALIFY was only that the claim was unverified. That ordering still does not satisfy `source.md:82`, which is a separate point already settled for V2 in C-002 and X-002. |