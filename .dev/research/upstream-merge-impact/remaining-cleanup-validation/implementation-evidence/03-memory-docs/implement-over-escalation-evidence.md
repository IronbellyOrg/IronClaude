# Evidence: /sc:implement escalated five attempts over low-severity findings

Written 2026-10-24 while the operator-requested sixth review of Task 1 was still running. Facts come from the session transcript and the files named below. Severity labels in the "my judgment" column are the orchestrator's own and are UNVERIFIED by the reviewers (reviewers labelled severity only where noted).

## 1. Run identity

- Command: `/sc:implement .dev/research/upstream-merge-impact/remaining-cleanup-validation/plans/03-memory-docs.md` (legacy, non-managed source; 4 tasks, run stopped inside Task 1).
- Task 1: "Align the two primary memory guides". Docs-only. Two files changed: `docs/user-guide/memory-system.md`, `docs/memory/README.md`. Four acceptance criteria (T1.AC1 to T1.AC4).
- Ledger: `.dev/implement/03-memory-docs-f5865990/progress.md`. Retry files: `.dev/implement/03-memory-docs-f5865990/retries/` (briefs `T1_brief-3.md` to `T1_brief-5.md`; per-task folder `T1/` with `review-2.md` to `review-5.md`, `approach-*.md`, `attempt-*.diff`, `advice-*.md`, `revert-*.log`).
- Outcome: Task 1 ended in `halt review=5 reason=ladder-end` (E-HALT-QA). Tasks 2 to 4 and the final independent review never ran. A human then said "fix task 1"; the orchestrator fixed the findings and started a sixth review (operator review, protocol Resume row H).
- Evidence folder for the product work: `.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/03-memory-docs/` (claim matrix `t1-claim-matrix.md`, review diffs `t1-review-*.diff`).

## 2. Timeline

Numbering follows the ledger: A1 = first implementation, A2 = the one allowed fix pass, A3 to A5 = ladder attempts written from advisers' briefs. Review text for the A1 review was not saved to disk (only the transcript has it); reviews A2 to A5 are on disk.

| Attempt | Review verdict | What the reviewer found (reviewer's own severity label where given) | My judgment: should it block? |
|---|---|---|---|
| A1 | extra | D1 guard behavior overstated ("did not change" vs "no new .md files, same byte size"); D2 the "not implemented" table rows contradicted the PM agent's own Serena restore and docs/mistakes notes; D3 a claim-matrix table row had an unescaped pipe; D4 (minor) "bad lines are harmless" wording was too broad; extra scope: README summary lines for two Task 4 passages rewritten. | Yes for D1, D2 (wrong facts written by the executor) and the Task 4 scope breach (a plan constraint). D3 cosmetic, D4 minor. |
| A2 | extra | One defect, labelled "low": the new "Explicit API" usage snippet, if run from a checkout, appends a synthetic row to the tracked `docs/memory/solutions_learned.jsonl` (`review-2.md`). | Yes. The plan forbids seeding production data. |
| A3 | extra | D1 README described the old-layout sample file as matching the lookup fields (wrong); D2 `jq -c .` check "to find invalid lines" misses the rows that actually make the lookup raise; D3 (low) two Task 4 README bullets reworded; D4 (low) one "who calls what" sentence ambiguous (`review-3.md`). | Mostly yes (D1, D2 are wrong or misleading statements; D3 scope). D4 minor. |
| A4 | missing | One defect, labelled "low severity (T1.AC4)": two true statements had no row in the task-owned claim matrix; wording "manual" vs "agent-written" suggested (`review-4.md`). The reviewer wrote "Task 1 is substantively done." | No. Should have passed with a note. |
| A5 | missing | (1) tar backup recipe at `docs/memory/README.md:119` writes into the current directory; (2) `chmod 644 docs/memory/*.jsonl` at `docs/memory/README.md:208` changes data-file modes (both lines were in the ORIGINAL text, not added by the task); (3) matrix lacked rows for "nothing measured", "old figures removed" and file/link existence; (4) the saved snippet script and its saved output did not match (`review-5.md`). The reviewer ruled AC1 to AC3 met. | Mostly no. (1) and (2) are inherited text and the criterion forbids only NEW unsafe recipes; (3) paperwork; (4) a real but trivial evidence flaw. |

Per-attempt cost, subagent tokens as reported by the tool results: reviewers 159,467 (A1), 138,243 (A2), 172,174 (A3), 162,495 (A4), 163,601 (A5) = about 796,000; advisers 68,008 (first escalation-1 adviser, rejected on a citation rule), 82,208 (critique), 113,484 and 113,885 (escalation 2) = about 378,000. Total about 1.17 million subagent tokens, 4 reverts, 9 subagent spawns for reviews and advisers, for a docs-only task whose last two failures were small. A sixth review (operator review) added more.

## 3. Mechanisms that produced the loop (read these files)

All paths are under `src/superclaude/skills/sc-implement-protocol/` unless stated.

1. **No severity in the verdict.** `refs/qa.md:35-52`: closed enum `compliant | missing | extra | misunderstood | cannot-verify`; any unmet AC gives `missing`, any non-empty `extra_scope` gives `extra` (step 5). A one-word nit and a data-corrupting defect map to the same verdict.
2. **Any non-compliant verdict starts the ladder.** `SKILL.md:129` (Q5: one fix pass, then the ladder) and `refs/retry.md:5-14` (attempt ladder A3 to A5, `blocked` + `halt review=5 reason=ladder-end`). `refs/retry.md:34-53`: per-run cap `RETRY_BUDGET = 8` tasks, no per-task token cap, no severity input.
3. **The only way out of a low-severity halt is a human.** `refs/qa.md:54-68` (Halt table, Ruling rule). A Ruling needs clear user confirmation in the current conversation; there is no automatic accept-with-note path.
4. **Each review is a fresh adversarial audit of the whole diff.** `refs/qa.md:3-12, 76-78` ("Do not trust the implementer's report"; one reviewer per review; no memory of earlier reviews). Different reviewers found different low-severity items each time, so the defect set moved (A3: sample-file text; A4: matrix rows; A5: inherited recipes). Nothing says a later review may not re-open or newly raise minor items on text earlier reviews accepted or that predates the task.
5. **Acceptance criterion about evidence reviews the evidence.** T1.AC4 ("claim matrix cites live source for each corrected behavior") made the task-owned matrix a reviewed artifact, so A4 and A5 failed on the paperwork, not on the product text.
6. **Output style rule.** `/config/.claude/output-styles/pragmatic.md:212` (source copy `src/superclaude/output-styles/pragmatic.md`): "Any issue of ANY severity (CRITICAL, IMPORTANT, or MINOR) MUST result in a FAIL verdict; a 'minor issues still pass' allowance is PROHIBITED." This is the user's own output style, active in the orchestrating session. It directly conflicts with passing low-severity findings. The brainstorm must say where it applies (per-task QA, final review, both, neither).
7. **Orchestrator-added review criteria.** The `qa.md` reviewer contract is: this file, the task brief, the diff (`refs/qa.md:84-88`). The orchestrator's reviewer prompts for A2 to A5 added "compliant only if there are zero defects of any severity" (from rule 6, not from the protocol), and for A5 added "every sentence asserting a fact needs a matrix row", which is stricter than T1.AC4. The protocol has no rule stopping the orchestrator from doing this.
8. **Revert-and-reapply cycle.** Each ladder step reverted both guides to the start state (`refs/retry.md:148-182`) and the next brief began with "apply attempt-N.diff", so most of the work was thrown away and put back. Small local defects (a sentence, a missing matrix row) do not need a revert or an adviser.
9. **Adviser answer rejected on a citation-stability technicality.** `refs/retry.md:78-86`: an answer citing a task-owned evidence file created after Q0 fails the parent check and triggers a critique adviser (one extra spawn), although every cited line existed and said what was claimed.

## 4. Replay cases the new design must satisfy

Use these as acceptance tests for the spec. Inputs are on disk except A1.

| Case | Input | Required outcome |
|---|---|---|
| R-A1 | A1 findings D1, D2 and the Task 4 scope breach (summarised above) | Block (at least until fixed). |
| R-A2 | `T1/review-2.md` snippet writes to the tracked production file | Block. |
| R-A3 | `T1/review-3.md` | Brainstorm decides and justifies: D1 and D2 are wrong or misleading statements, D3 and D4 low. |
| R-A4 | `T1/review-4.md` | Pass with a recorded note; no further attempt. |
| R-A5 | `T1/review-5.md` | Pass with recorded notes for findings 1 to 3; finding 4 either fixed in place or noted; no ladder escalation. |

Expected end state: this run finishes Task 1 without human intervention by the 3rd attempt, with the minor findings written down as notes, and the final independent review still runs.

## 5. User requirements (verbatim intent)

- There was no reason for this to go this far. It should have passed without human intervention by the 3rd attempt.
- Low-severity findings must be passed as the attempts progress (3rd, and definitely 4th or 5th).
- Use `/ponytail-review` to help identify the severity of a finding.
- The last part of the brainstorm: invoke `/ponytail` to review `/sc:implement` as a whole and propose exactly three simplifications to add to the spec.

## 6. Constraints for the eventual change

- Source of truth is `src/superclaude/`; installed copies come from `make sync-dev` / `superclaude install`; never stage `.claude/` mirrors (project CLAUDE.md).
- Installed primitives must not reference `src/superclaude/...` paths (project CLAUDE.md).
- The ledger grammar in `refs/ledger.md` is regex-parsed and pinned by tests; changes must be backward compatible with existing ledgers.
- Managed packages (`refs/managed-workspace.md`) share the same QA and ladder; the managed archive FINAL review must stay mandatory.
