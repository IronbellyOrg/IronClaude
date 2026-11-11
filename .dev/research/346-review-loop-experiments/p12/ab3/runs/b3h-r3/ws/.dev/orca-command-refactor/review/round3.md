review: 3 of 3

# Spec-panel re-review: Orca worker contract spec (round 3)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round2.md --baseline .dev/orca-command-refactor/specs/history/spec-v2.md`
- Prompt: RE-REVIEW from `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full (RE-REVIEW prompt and its bullets at lines 38-51; GATE prompt at lines 57-65). No `--unattended`, so `WORKER-CONTRACT.md` does not apply.
- CANDIDATE: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 58948 bytes, sha256 `d7b701458ccab1292a94ee6f2c84881cfc91dbf20d522f329d407123b072388d`.
- BASELINE: `.dev/orca-command-refactor/specs/history/spec-v2.md`, 58893 bytes, sha256 `b4832d456dbf9b742b18a39e1442803bd1c9b0e19aafedbf70079e7911d839c2`. This is the hash `review/round2.md:7` records as its candidate, so the baseline is the text round 2 reviewed.
- PRIOR: `.dev/orca-command-refactor/review/round2.md`, sha256 `a54ce900848768c4ab534e849e8e178bdbd0251b7ff7dd52b7c49a5efff54b83`, header `review: 2 of 3` (`review/round2.md:1`). N = 3.
- Revision under review: `.dev/orca-command-refactor/review/revise2.md` (one line changed, +55 bytes, for F-19).
- Reviewer model: claude-haiku-5-5.
- rf-qa.md: neither `.claude/agents/rf-qa.md` in the workspace nor `~/.claude/agents/rf-qa.md` exists in this sandbox (checked). Steps 1-5 of the fix-cycle process cannot be read, so the rules in `command.md` Review Loop step 5 stand alone, as that bullet allows.

## Step 1: evidence block

`diff -w BASELINE CANDIDATE` reports one changed line, line 62. Roles fixed: `<` = BASELINE, `>` = CANDIDATE.

```text
62c62
< | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. Every command in section 3 writes to this one path; a command whose output would land elsewhere gets an output-directory flag so the path is known before dispatch (F-03). The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
---
> | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. Every command in section 3 that accepts `--unattended` writes to this one path (`load` is excluded, F-19); a command whose output would land elsewhere gets an output-directory flag so the path is known before dispatch (F-03). The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

Self-check (`grep -nF`, run in this pass): the AFTER line, without `>`, is found once in CANDIDATE (`specs/orca-worker-contract-spec.md:62`). The BEFORE line, without `<`, is found once in BASELINE (`specs/history/spec-v2.md:62`) and not in CANDIDATE. The roles are correct.

## Coverage

- Read in full: the candidate, the baseline (`specs/history/spec-v2.md`), the prior report (`review/round2.md`), `command.md`, the prompt file (`home/.claude/rules/prompts/document_review_loop_prompts.md`), `review/revise2.md`, and `README.md:1-39`.
- Scope: the one changed line (62) and the five round-1 defects F-01 to F-05 that round 2 marked resolved (`review/round2.md:91-99`), checked for regression. The round-2 blocking finding F-19 (`review/round2.md:103-111`) is checked for resolution.
- Round-2 Medium and minor findings (F-06, F-09, F-13, F-14, F-20, F-21, F-22, N-1) are not re-graded. Where their quoted text is still present, they are listed under follow-up candidates.
- Not reopened: `inventory/*.md` and `review/round1.md`. The changed line adds no new `INV`, `CAPS` or `sk/` citation; its existing citations are inherited text and remain UNVERIFIED in this sandbox, as round 2 recorded (`review/round2.md:84`).
- Pipeline Dimensional Analysis: not triggered. The changed line adds no multi-stage data flow with count divergence.
- State Variable Registry: not required (focus is requirements and architecture).

## Prior findings re-check (`resolved|open|regressed`)

| ID | Status in round 2 | Status in round 3 | Evidence in CANDIDATE |
|---|---|---|---|
| F-19 | open (blocking) | resolved | `specs/orca-worker-contract-spec.md:62` now limits the every-command clause to commands that accept `--unattended` and excludes `load`. This matches `:52` (Contract file, except `load`), `:76` (except `load`), `:112` (load row: no gate, no report), `:159` (P1 excludes `load`), `:195` (AC-1.1 excludes `load`) and `:265` (Decisions: a report file for `/sc:load` would be unrequested). An implementer who follows `:62` no longer gives `load` a contract. |
| F-01 | resolved | resolved | Unchanged: `:73` (two-worker rule), `:85`, `:86` (rows). Not on the changed line. |
| F-02 | resolved | resolved | Unchanged: `:61` (WC-3 answer limit), `:234` (D2(a)). |
| F-03 | resolved | resolved | `:62` keeps the output-directory flag clause, which is the F-03 fix. `:83`, `:92`, `:116` unchanged. |
| F-04 | resolved | resolved | Unchanged: `:147` (SA-2), `:158` (P0 prose only), `:172` (AC-C1 exemption). |
| F-05 | resolved | resolved | Unchanged: `:52`, `:76`, `:159`, `:195` exclude `load`. The change at `:62` now agrees with them. |

Regressed: none. Each round-1 defect keeps its round-2 evidence line, because only line 62 changed.

## Findings on changed lines (origin=changed)

Only line 62 is on a changed line. Checked against the grading rule:

- **Scope of "accepts `--unattended`".** The phrase is defined by P1 (`:159`): the flag is accepted by every command in sections 3.1 and 3.2 except `load`. Before P1 no command accepts it, so `:62` binds nothing at P0. P0 uses only the ten ready commands (`:158`), and the P0 smoke runs do not depend on the WC-4 contract (`:194`). No wrong outcome follows, so this is not blocking.
- **No new contradiction.** The narrowed clause agrees with every other text that excludes `load` (`:52`, `:76`, `:159`, `:195`, `:265`). Section 3.1 and 3.2 rows that name `return-contract.yaml` (`:83`, `:84`, `:88`, `:92`, `:116`) do not name `load`.
- **N-2 (minor, origin=changed).** `:62` now carries a review id in normative text, `(load is excluded, F-19)`. The spec uses the same convention elsewhere (`:52`, `:76`, `:159`, `:195`, `:265`), so this is a style note for the final text, not a defect.

Result: no new blocking finding.

## Guard Condition Boundary Table (changed guards only; re-review scope)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 accepts-`--unattended` scope | `SPEC:62` | Typical | a section-3 command that accepts `--unattended` after P1 (for example `analyze`, `:99`) | true | writes `<output-dir>/return-contract.yaml` | OK |
| WC-4 accepts-`--unattended` scope | `SPEC:62`, `SPEC:159`, `SPEC:195` | Zero/Empty | `load` (section 3.2, no gate, no unattended mode) | false | no WC-4 contract; AC-1.1 excludes it | OK |
| WC-4 accepts-`--unattended` scope | `SPEC:62`, `SPEC:158` | Legitimate Edge Case | a section-3 command before its P1 change (accepts no flag yet) | false | not bound at P0; P0 runs only the ten ready commands | OK |
| WC-4 accepts-`--unattended` scope | `SPEC:62`, `SPEC:265` | Sentinel Value Match | the name `load` in the every-command clause | excluded | the Decisions row forbids a report file for `load`, so the exclusion is consistent | OK |

Classes left out: Maximum/Overflow (no numeric bound is changed on line 62).

## Follow-up candidates (Medium and minor; not blocking; not in any revision brief)

- **F-20 (MEDIUM, round 2, not re-graded).** `specs/orca-worker-contract-spec.md:172`: AC-C1 uses escaped `\|` in the raw markdown, so the raw command prints every searched line. The line is unchanged, so the round-2 grade stands (`review/round2.md:112-118`).
- **F-21 (MEDIUM, round 2, not re-graded).** `:73`: the two-worker rule does not say whether it covers sequential runs. Unchanged (`review/round2.md:120-124`).
- **F-22 (MEDIUM, round 2, not re-graded).** `:61` and `:73` have no acceptance check in section 7.3 (`:189-211`). Unchanged (`review/round2.md:126-131`).
- **N-1 (minor, round 2).** `:85`: "until which one audit per worktree" is hard to read. Unchanged.
- **N-2 (minor, origin=changed).** `:62`: the review id `F-19` sits in normative text. See above.
- **N-3 (minor, origin=unchanged).** `:112`: the load row reads "none (see note)", and no note follows in the document. `:112` does not quote the changed line `:62`, so this is a minor note only.
- **Round-2 Medium items that quote changed lines (`review/round2.md:158`).** F-06 (`:73`), F-09 (`:92`, the workflow row still omits the WC-4 fields `command` and `artifacts`), F-13 and F-14 (`:62`). Their text is in `review/round1.md`, which this pass did not reopen. They stay Medium and are not re-graded here.
- The session that ran this review asks the user once whether to open an issue for these follow-up candidates. No issue is created here.

## Re-review verdict summary

- Prior blocking findings: F-19 is resolved. F-01 to F-05 are resolved and not regressed.
- New blocking findings: none.
- Cap: this is review 3 of 3. No fourth review and no further fix cycle runs (`command.md` Review Loop step 4). A FAIL here would escalate; this review is a PASS, so no escalation applies.
- Coverage: `scoped PASS: changed lines + prior blockers`. This is a scoped PASS. It is not whole-document assurance.
- Next step for the coordinator (not run here): the GATE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (lines 57-65) applies once after a PASS. It is a first review of the complete document, in a fresh context, labelled as the gate review. Its blockers start at most one gate loop, and the loop ceiling is 5 reviews and 3 fix cycles in all.
- No Reviser brief is written: at `review: 3` the Reviser brief is omitted (`command.md` Review Loop step 6).

verdict: PASS
