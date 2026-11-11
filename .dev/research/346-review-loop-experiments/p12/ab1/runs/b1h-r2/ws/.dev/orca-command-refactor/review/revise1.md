# Revise 1: repair of the confirmed blocking findings

Revise brief: "Repair only the blocking findings M1, M2, M3, M6, M7, M8, M9, M11, M12, M13 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`." (REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:60-63`.)

Confirmed ids come from the VERIFY reply `.dev/orca-command-refactor/review/verify-1.md`, last line `confirmed: M1, M2, M3, M6, M7, M8, M9, M11, M12, M13` (verify-1.md:last line). The Reviser brief in `review/round1.md:161` lists the same ten ids. Rejected ids M4, M5 and M10 are not in IDS and are not edited (see the last section).

Inputs read: `.dev/orca-command-refactor/README.md` (shared context), `review/round1.md`, `review/verify-1.md`, the spec, and the inventories `inventory/commands-a.md` and `inventory/commands-b.md`. Every inventory citation below was checked by reading the cited line inside the workspace. The `cmd/`, `sk/` and `src/` citations that remain in the spec from earlier revisions were not re-read here (they are outside this workspace), so the spec keeps them as they were.

## Byte accounting

Method: each edit was applied as an exact string replacement (each old string matched exactly once). Bytes added = UTF-8 bytes of the new string; bytes deleted = UTF-8 bytes of the old string. A later relocation of one M8 block was made with two Edit calls, reported as the M8 relocation line.

| Measure | Value |
|---|---|
| Candidate before (`specs/history/spec-v1.md`, identical to the candidate reviewed in verify-1.md) | 57763 bytes, 285 lines, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| Candidate after | 60747 bytes, 294 lines, sha256 `feaa1a31e42a8514d14628b790b646be58d5aee3914f33cd26e8e8f6a0037350` |
| Net change | +2984 bytes |

Per finding id (edits, bytes added, bytes deleted, net):

| Id | Edits | Added | Deleted | Net |
|---|---|---|---|---|
| M1 | 7 | 1266 | 614 | +652 |
| M2 | 3 | 400 | 221 | +179 |
| M3 | 1 | 320 | 112 | +208 |
| M6 | 2 | 533 | 134 | +399 |
| M7 | 1 | 153 | 78 | +75 |
| M8 | 1 (+ relocation) | 666 | 269 | +397 (+154 from relocation) = +551 |
| M9 | 1 | 233 | 116 | +117 |
| M11 | 1 | 233 | 83 | +150 |
| M12 | 2 | 304 | 174 | +130 |
| M13 | 4 | 700 | 177 | +523 |
| Total | 22 + 1 relocation | | | +2984 |

The per-id nets sum to the total: 652 + 179 + 208 + 399 + 75 + 551 + 117 + 150 + 130 + 523 = 2984.

M8 relocation: the AC-C1 fenced block first went inside the table (which broke AC-C2 to AC-C5 out of the table). It was moved below the table, and one introductory sentence was added. The move itself is net zero for the block. Net +154 is the introductory sentence and its blank lines.

## Finding rows

| Id | Applied where (spec line, after revision) | Action |
|---|---|---|
| M1 | WC-4 header and path rule, `:62`; section 2.3 report-path clause, `:73`; section 3 definition of "Contract", `:76`; cleanup-audit and index-repo rows, `:85-86` (no change to the path text); init-lite row `:87`; tdd row `:90`; workflow row `:92` (its run-time path is covered by WC-4); research row `:116`; P1 scope list `:159` | Applied. The contract path is now fixed per command: a directory `--output` gives `<output-dir>/return-contract.yaml` (adversarial keeps its `<output>/adversarial/...` path, cited `INV-A:60`, which lists the two real locations); a file `--output` gives a sibling file; run-time paths (workflow, research) are passed in `worker_done --report-path` and read then. The contradictory "known before dispatch" claim now applies only where WC-4 gives a fixed path. init-lite is added to the P1 fixes list because its contract is new. |
| M2 | WC-4 exception for workflow pre-creation STOPs, `:62` (added "except workflow's pre-creation STOPs (M2; section 3, `INV-B:272`)"); workflow row `:92` (the pre-creation STOP is now reported as `worker_done --outcome failed` with the STOP in the body, no contract); AC-1.4 `:204` (checks that workflow states pre-creation STOPs write no contract) | Applied by the drop option named in M2's recommendation. A pre-creation STOP has no package directory, so no path exists for a contract. SA-3 (`:148`) is unchanged and now holds for workflow. Source: `INV-B:272` says "Not written for pre-creation STOPs". |
| M3 | P1 row `:159`: `--unattended` is refused with an error by auggie-review, task, pr-submit and post-release until their P2 or P4 change lands | Applied. These four are the commands in sections 3.1-3.2 with an outward default (`INV-A:38` for auggie-review; `INV-B:94` for pr-submit; `INV-B:297` for task and post-release). WC-9 (`:67`) is now met in P1. Their `## Unattended mode` sections still exist (AC-1.1). |
| M6 | AC-0.4 `:200` (step 3's report clause and step 4 use each command's existing report: troubleshoot `REPORT.md`, `INV-B:49`; workflow and adversarial existing `return-contract.yaml` must be non-empty and parse as YAML; the four-value `status` and `command` assertions move out of P0); AC-1.2 `:202` (those assertions apply in P1) | Applied as recommended. Troubleshoot's report is `REPORT.md` (`INV-B:49`), and its contract exists only with `--caller task-unified`, so the P0 check cannot use the YAML assertion. |
| M7 | WC-9 `:67`: "a coordinator's `ask` answer never supplies that flag (M7; WC-3)" | Applied. This is the sentence that closes the flag route from WC-3 into WC-9. |
| M8 | AC-C1 row `:172` now refers to the block below; the AC-C1 block (fenced) with the first grep and a positive control sits after the table at `:178-184`; the pattern now uses plain `|` (the escaped `\|` made grep -E match nothing, tested in the sandbox, exit 1) | Applied. The positive control printed its planted line in the sandbox (exit 0) with plain `|`. A table cell cannot hold a plain `|`, which is why the pattern is set out in a block. |
| M9 | WC-5 `:63`: `--outcome failed` also when the report is empty, unparseable or has a status outside the four values | Applied. A zero-byte or unknown-status contract no longer falls under "otherwise". |
| M11 | WC-3 `:61`: a gate guarding a Ruling, an outward action or a safety boundary resolves as blocked, and no `ask` answer supplies it (D2, D4, WC-9) | Applied. This is the exclusion M11 asked for. The implement row and D2 were not edited: WC-3 now carries the exclusion, which is what M11's recommendation requires ("add an exclusion to WC-3"). |
| M12 | section 2.3 `:73`: `--unattended` included "from P1 on (P0 runs omit it, AC-0.4)"; AC-0.4 `:200`: P0 runs use the stated flags only, no `--unattended` | Applied. Section 2.3 and section 3.1 (`:79`, "run as workers now if the brief uses the stated flags") now say the same thing. |
| M13 | section 2.3 `:73`: at most one cleanup-audit or index-repo Task per worktree at a time (WC-11); cleanup-audit row `:85` now refers to section 2.3; index-repo row `:86`: location "UNVERIFIED, `INV-A:53`", with the fixed path serialized; new check AC-1.5 `:205` | Applied, using the coordinator-rule option. The two rows were not moved out of section 3.1, so the 10 / 27 / 6 counts in `:76` are unchanged. |

## Rejected or not in IDS (not edited)

| Id | Status | Reason |
|---|---|---|
| M4 | Not in IDS; not edited | The verifier rejected it (`verify-1.md`, M4 row): the texts conflict, but the safety branch needs a re-keyed trigger that SA-6 says is not done, and row 88 never says `--remediate` applies code. It stays a noted item in round1.md. |
| M5 | Not in IDS; not edited | The verifier rejected it (`verify-1.md`, M5 row): the failure depends on wording the spec leaves open. The M8 fix changes the AC-C1 pattern, so M5's exclusion question stays open for the next re-review. |
| M10 | Not in IDS; not edited | The verifier rejected it (`verify-1.md`, M10 row): AC-1.1 checks only that the section names `return-contract.yaml`, and a load section that names it while writing no contract passes that check. |

## Verdict

No PASS is awarded. This pass repaired the ten confirmed ids only. The next step is the RE-REVIEW prompt (`review: 2 of 3`) against the baseline `specs/history/spec-v1.md`, using this report as the prior report, with the revised candidate sha256 `feaa1a31e42a8514d14628b790b646be58d5aee3914f33cd26e8e8f6a0037350`.

## Coverage and self-check

- Read: the README, the REVISE prompt, round1.md, verify-1.md, the spec before and after, and the cited lines of commands-a.md (`:35`, `:38`, `:53`, `:60`) and commands-b.md (`:39`, `:49`, `:52`, `:94`, `:272`, `:297`).
- Run: the AC-C1 pattern forms in the sandbox (plain `|` matched, escaped `\|` did not). No repo command was run and nothing outside the spec and this file was written.
- Not checked: the `cmd/`, `sk/` and `src/` citations that the spec carried over from earlier revisions. They remain as they were and are outside this workspace.
