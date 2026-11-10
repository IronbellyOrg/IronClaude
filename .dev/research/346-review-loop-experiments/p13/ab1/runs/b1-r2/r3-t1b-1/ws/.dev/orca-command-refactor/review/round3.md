review: 3 of 3
# Spec-panel critique, re-review 3 (scoped: changed lines + prior blockers)

- mode: critique; focus: requirements, architecture; re-review of `.dev/orca-command-refactor/review/round2.md` (its header is `review: 2 of 3`, so N = 3)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `8fb661981967c14a5a823b50e2afa1ac31cb20523338e235d7b1b568eeb0705a`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v2.md`, sha256 `aaef3909fef4429e5147203dd015e1d769b2800db3aeffa1df9ee8fced190c7c` (equals the candidate hash recorded in round2.md:3, so the baseline is the text round 2 reviewed)
- prior: `.dev/orca-command-refactor/review/round2.md`, sha256 `4892a3dff5f7deb04fb56507878082ae995278ea1bbfaa6ae451ed1ec7880061`
- reviewer model: claude-sonnet-5-5
- read first: `.dev/orca-command-refactor/README.md` (binding context); `~/.claude/rules/prompts/document_review_loop_prompts.md` (RE-REVIEW prompt, followed in order)
- evidence limit: the only checkable evidence is `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Any citation to `src/`, `sk/`, `cmd/` or `EVIDENCE.md` files is UNVERIFIED here (not in the workspace); I rely on the inventory line that quotes it.
- not run: `superclaude review panel resolve` / `review merge` (no such command in the sandbox); one reviewer, as the prompt allows when the command is absent.

## Step 1: evidence block (diff -w BASELINE CANDIDATE)

Changed hunks: candidate lines 62-64 (WC-4, WC-5, WC-6), 73 (section 2.3), 194-196 (AC-0.4, AC-1.1, AC-1.2). Nothing else changed.

BEFORE (baseline), verbatim changes only (long table cells abbreviated with `[...]` where the text is unchanged):

- WC-4 (baseline): `[...] workflow and research take no output flag, so their contract sits beside the main deliverable (workflow: .dev/tasks/to-do/<id>/return-contract.yaml) and the worker passes that path as --report-path. It follows the return-contract pattern [...] the one exception is a workflow stop before its package exists, which has no contract, so the no-report rule of WC-5 applies [L1]. [...]`
- WC-5 (baseline): `--outcome failed when the report says failed or blocked, or no report exists, is empty, or has a status outside the four values [L1]; --outcome succeeded otherwise [...]`
- WC-6 (baseline): `The coordinator's retry brief names a new output directory (section 2.3), so a stale contract is never read as the retry's [L1].`
- Section 2.3 (baseline): `the output directory or file, a new one on every retry (WC-4, WC-6) [L1] [...] the coordinator opens the report file and checks its status and verdict before any dependent Task starts, because succeeded also covers partial and a FAIL audit (WC-5) [L1]`
- AC-0.4 (baseline): `[...] step 3 passes with the command's existing report file as --report-path and --outcome matching its status; step 4 is test -s on that file [...]`
- AC-1.1 (baseline): `[...] every command in the P1 row (section 6) has a ## Unattended mode section naming return-contract.yaml and ~/.claude/WORKER-CONTRACT.md, and that no section-4 command has one`
- AC-1.2 (baseline): `7.2 live check on each P1 command with --unattended --output <dir>`

AFTER (candidate), verbatim changes only:

- WC-4 (candidate:62): `[...] and the worker passes that path as --report-path; where the output location is fixed, the contract sits in it: cleanup-audit .claude-audit/return-contract.yaml, index-repo beside PROJECT_INDEX.md; where only a report path is named (troubleshoot REPORT.md), beside that report (N3, L1). [...] the one exception is a workflow stop before its package exists, which has no contract and no place to write one: the worker puts the exact question in the first sentence of the worker_done body and sends no --report-path (WC-5) [L1, N7].`
- WC-5 (candidate:63): `[...] has a status outside the four values [L1]; a Markdown report with no status field (what a command writes before its phase adds the contract) counts as succeeded when non-empty (N6, L1); --outcome succeeded otherwise [...]`
- WC-6 (candidate:64): `The coordinator's retry brief names a new output directory where the command has an output flag, and deletes the old return-contract.yaml before a retry of a fixed-output command (section 2.3), so a stale contract is never read as the retry's [L1, N2].`
- Section 2.3 (candidate:73): `the output directory or file, a new one on every retry, or for a fixed-output command the old contract deleted first (WC-4, WC-6) [L1, N2] [...] the coordinator opens the contract and checks its status before any dependent Task starts, and reads the verdict from report_path where the command has one, because succeeded also covers partial and a FAIL audit (WC-5) [L1, N4]`
- AC-0.4 (candidate:194): `[...] --outcome matching its status (succeeded for a non-empty Markdown report with no status field, WC-5); step 4 is test -s on that file [...]`
- AC-1.1 (candidate:195): `[...] every command in the P1 row (section 6) except /sc:load has a ## Unattended mode section naming return-contract.yaml and ~/.claude/WORKER-CONTRACT.md, and that /sc:load and no section-4 command has one [L1]`
- AC-1.2 (candidate:196): `7.2 live check on each P1 command except /sc:load, with --unattended and the output flag its section 3 row gives (--output <dir> or <file>; none for workflow, cleanup-audit and index-repo, whose contract sits where WC-4 says) [L1, N1]`

Self-check: each of the 7 AFTER lines was found by `grep -cF` in the candidate (count 1 each) and each of the 7 BEFORE lines in the baseline (count 1 each). Roles are not swapped.

## Prior blocking findings

| prior id | sub-item | status | basis |
|---|---|---|---|
| L1 | main: AC-1.1/AC-1.2 required the section and contract for every P1-row command, but load is exempt | resolved | AFTER candidate:195 and :196 now exempt `/sc:load` and assert it has no section; this matches candidate:76 ("except `/sc:load`") and the load row at candidate:112 ("P1 (usage line only)"). The two sides no longer contradict. |
| L1 | N1: AC-1.2 passed `--output <dir>` to every P1 command | resolved | AFTER candidate:196 uses "the output flag its section 3 row gives" and names workflow, cleanup-audit and index-repo as having none. Consistent with candidate:62 (WC-4) and candidate:92. A residual naming gap is recorded as L37 (Medium). |
| L1 | N2: a new output directory on every retry cannot be given for fixed-output commands | resolved (residual Medium L31, L32) | AFTER candidate:64 and :73 split the rule: new directory where an output flag exists, delete the old contract for fixed-output commands. The fixed-output half of the defect is gone. Whether a new directory also applies to resume-capable commands is a reading question, graded Medium (L31). |
| L1 | N3: fixed-output or report-path-only commands had no contract location | resolved (residual Medium L35) | AFTER candidate:62 names cleanup-audit (`.claude-audit/`, `INV-A:42`), index-repo (beside `PROJECT_INDEX.md`, `INV-A:53`, location itself UNVERIFIED there) and troubleshoot (beside `REPORT.md`, `INV-B:242`), plus a generic "report path only" clause. |
| L1 | N4: coordinator must check a verdict the contract does not carry | resolved | AFTER candidate:73 reads the verdict from `report_path`, a field WC-4 requires (candidate:62). |
| L1 | N7: workflow pre-creation stop is a blocked gate with nowhere to write | resolved (residual Medium L36) | AFTER candidate:62 sends the question in the `worker_done` body with no `--report-path`; `CAPS:72-74` supports omitting `--report-path` when there is no real value, and `INV-B:272` confirms workflow writes no contract for pre-creation stops. WC-5 (candidate:63) maps "no report exists" to `--outcome failed`, so the path is coherent. |
| L1 | N6: troubleshoot's Markdown report has no status | resolved (residual Medium L33) | AFTER candidate:63 and :194 define a non-empty Markdown report with no `status` as succeeded; step 4 stays `test -s`. `INV-B:242` shows troubleshoot writes `return-contract.yaml` only with `--caller task-unified`, so the pre-P2 route is the Markdown report, which the new clause covers. |
| L7 | (resolved in round 2; claim text not in round2.md, matched by its refs P0, SA-2, SA-5, WC-8) | resolved | None of its refs sits on a changed line (hunks are 62-64, 73, 194-196). Claim text UNVERIFIED because round2.md does not restate it. |
| L9 | (refs 1.1, 3, AC-3.1, AC-3.3, SA-4, WC-7) | resolved | Same: no ref is on a changed line. Claim text UNVERIFIED. |
| L11 | (ref WC-11) | resolved | WC-11 (candidate:69) is unchanged and the new WC-6 deletion rule for fixed-output commands agrees with its one-at-a-time rule. |

## Findings on changed lines (and dependents)

No finding passes the grading check. For each, "An implementer who follows the stated text as written builds X" needs a guess about which of two allowed readings is chosen, or rests on a requirement the document never states, so each is Medium.

### === REQUIREMENTS ANALYSIS ===

- L31 (MAJOR label, Medium, origin=changed, Wiegers): WC-6 (candidate:64) and section 2.3 (candidate:73) tell the coordinator to name a new output directory on every retry "where the command has an output flag". WC-6's own first rule says a command with a resume flag resumes from its on-disk state. For a command that has both an output flag and a resume flag (for example roadmap, `--output <dir>` and `--resume` over `.roadmap-state.json`, candidate:118; adversarial `--pipeline-resume`, candidate:83), a literal reading gives a fresh directory that holds no state to resume. Whether the state lives in the output directory is not stated for these commands (UNVERIFIED in the inventories), so the wrong outcome needs a guess. Recommendation: say that the new-directory rule applies only to commands run without their resume flag.
- L32 (MAJOR label, Medium, origin=changed, Nygard): the contract-deletion rule in WC-6 fires only "before a retry of a fixed-output command". A second, non-retry run in the same fixed location (a later `--pass` of cleanup-audit in `.claude-audit/`, `INV-A:42`; an `mode=update` re-run of index-repo, `INV-A:53`) leaves the earlier run's `return-contract.yaml` in place. If the new worker dies before writing one, the coordinator reads a stale `succeeded`. `worker_done --outcome` (WC-5) and the contract's `command` field (WC-4) are partial guards, but 2.3 tells the coordinator to check `status` only. No AC checks the deletion at all (see round-2 L6). Recommendation: delete before every run of a fixed-output command, or compare `command`.
- L33 (MINOR, origin=changed, Wiegers): WC-5 sends any `status` outside the four values to `--outcome failed` (candidate:63), and AC-0.4 (candidate:194) says the outcome must match "its status" for workflow and adversarial, whose existing contracts already carry their own `status`. Their vocabulary is not shown in the inventories (`INV-B:272` names the field only), so a successful pre-P1 run could be mapped to failed. UNVERIFIED.
- L34 (MINOR, origin=changed, Wiegers): the P1 scope cell says "for the commands in this row only (a no-op where a command has no gate)" while the same row lists "load (usage line only)" and lists adversarial, cleanup-audit, index-repo only as "fixes" (candidate:159). AC-1.1 (candidate:195) and AC-1.2 (candidate:196) settle the intent (load has no section; cleanup-audit and index-repo are live-checked with `--unattended`), so this is wording, not a contradiction.
- L37 (MINOR, origin=changed, Adzic): AC-1.2 runs each P1 command with "the output flag its section 3 row gives", but several P1 rows give no flag name ("add a report path", "add an output path", candidate:101,102,106). A test author must invent the name. The phase that adds the flag can fix the name, so no wrong build follows from the text.

### === ARCHITECTURE ANALYSIS ===

- L35 (MINOR, origin=unchanged, depends on the changed WC-4 generic clause): cli-portify ("file location unnamed", candidate:105) and save ("contract naming the file written", candidate:119) still have no stated contract location; the new clause covers only "a report path is named". Both are P2/P3 rows, so the phase plan can fix them. Quotes the changed line it depends on (candidate:62).
- L36 (MAJOR label, Medium, origin=changed, Nygard): the N7 exception leaves two loose ends. (a) WC-2 forbids ending a turn on a chat question (candidate:60) while the workflow stop must still show the question to the worker so it can copy it into the `worker_done` body; (b) 2.3 tells the coordinator to "open the contract" (candidate:73) and does not say to read the `worker_done` body when no contract exists. WC-5 also says the body's first sentence states "the report's status and verdict" (candidate:63), which does not exist here. An implementer can resolve all three by reading the exception as controlling. Recommendation: add "or the `worker_done` body when WC-4's workflow exception applies" to 2.3.

### === Guard Condition Boundary Table (changed guards only) ===

Guards on changed lines: (G1) WC-5 outcome mapping; (G2) WC-6 deletion/new-directory rule; (G3) AC-1.1/1.2 `/sc:load` exemption; (G4) WC-4 N7 exception.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 status check | WC-5, candidate:63 | Zero/Empty | empty report | failed | `--outcome failed` | OK |
| G1 | WC-5 | One/Minimal | non-empty Markdown, no `status` | succeeded | `--outcome succeeded` (new clause) | OK |
| G1 | WC-5 | Typical | `status: partial` | succeeded | succeeded with status in the body | OK |
| G1 | WC-5 | Sentinel Value Match | `status: blocked` | failed | `--outcome failed` | OK |
| G1 | WC-5 | Legitimate Edge Case | existing contract with a `status` value outside the four (workflow/adversarial before P1) | failed | not stated whether pre-P1 vocabulary is mapped | GAP (Medium, L33) |
| G2 retry rule | WC-6, candidate:64 | Typical | output flag, no resume flag | n/a | new directory | OK |
| G2 | WC-6 | Legitimate Edge Case | output flag and resume flag together | n/a | both a new directory and resume on-disk state are stated | GAP (Medium, L31) |
| G2 | WC-6 | One/Minimal | fixed-output command, retry | n/a | old contract deleted | OK |
| G2 | WC-6 | Legitimate Edge Case | fixed-output command, later non-retry run | n/a | not stated | GAP (Medium, L32) |
| G3 load exemption | AC-1.1, candidate:195 | Typical | `/sc:load` | exempt | no section, no contract | OK |
| G3 | AC-1.1 | Legitimate Edge Case | command in P1 "fixes" list only (adversarial) | not exempt | section expected (inferred from AC-1.2) | OK (wording only, L34) |
| G4 workflow exception | WC-4, candidate:62 | Zero/Empty | stop before package exists | n/a | question in `worker_done` body, no `--report-path` | OK |

Classes left out: Maximum/Overflow does not apply to any of these guards (no counts or sizes). Sentinel match for G2 and G3 cannot occur (no sentinel value).

## Pipeline Dimensional Analysis

Not triggered: the changed lines hold no multi-stage count-changing pipeline.

## Adversarial probes (Whittaker, changed lines only)

- Sequence Attack on G2: pass-1 worker writes `.claude-audit/return-contract.yaml` (`succeeded`); pass-2 worker is started with no retry, dies before writing; the coordinator opens the stale file and sees `succeeded`. State before: contract(pass 1). After: still contract(pass 1). Recorded as L32 (Medium), because `worker_done` outcome is also available.
- Divergence Attack on WC-6: `--output <dir>` plus `--resume` — see L31.
- Zero/Empty Attack on WC-5: empty file maps to failed; an `artifacts: []` or empty `blocked_question` is not tested here and is outside the changed lines.

## What I covered

Every changed hunk (7 lines) and each prior blocking finding (L1 with its 6 sub-items, plus L7, L9, L11 as resolved). Dependents read in full: sections 2.3, 3.1, 3.2, 4, 5, 6, 7.1-7.3, 8, 9 (candidate:73-246). Not covered: unchanged text without a changed-line dependency, which stays as round 2 left it (round-2 non-blocking items L2-L30 are unchanged and remain open follow-up candidates, not re-graded). Whole-document assurance is not given; it needs a separate, labelled first review and its blockers would be escalated, not start a fourth review.

## follow-up candidates

Medium: L31, L32, L36. Minor: L33, L34, L35, L37. Plus round-2 open items L2-L6, L8, L10, L12-L30 (unchanged, see round2.md). The session that runs the loop asks the user once whether to open an issue for these; this reviewer created none and asked nothing.

coverage: scoped PASS: changed lines + prior blockers

## Findings block

```findings-v1
{"prior": "L1", "status": "resolved"}
{"prior": "L7", "status": "resolved"}
{"prior": "L9", "status": "resolved"}
{"prior": "L11", "status": "resolved"}
{"id": "L31", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "The coordinator's retry brief names a new output directory where the command has an output flag", "anchor2": "resumes from its on-disk state when given its resume flag", "refs": ["WC-6", "2.3"], "claim": "A new output directory on retry may leave a resume-capable command with no state to resume, depending on a reading the text allows."}
{"id": "L32", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "deletes the old `return-contract.yaml` before a retry of a fixed-output command", "refs": ["WC-6", "2.3", "WC-4"], "claim": "A later non-retry run in a fixed location can leave a stale succeeded contract, and no AC checks the deletion."}
{"id": "L33", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "has a `status` outside the four values [L1]", "anchor2": "`--outcome` matching its status (succeeded for a non-empty Markdown report with no status field, WC-5)", "refs": ["WC-5", "AC-0.4"], "claim": "Existing workflow or adversarial contracts may use other status words, and WC-5 would map a good run to failed (UNVERIFIED)."}
{"id": "L34", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "for the commands in this row only (a no-op where a command has no gate)", "anchor2": "load (usage line only)", "refs": ["P1", "AC-1.1", "AC-1.2"], "claim": "The P1 scope cell reads as giving load a section, which AC-1.1 forbids; AC-1.1 controls."}
{"id": "L35", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "contract (fields already defined; file location unnamed)", "anchor2": "contract naming the file written", "refs": ["WC-4", "3.2"], "claim": "cli-portify and save still name no contract location."}
{"id": "L36", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "the worker puts the exact question in the first sentence of the `worker_done` body and sends no `--report-path` (WC-5)", "anchor2": "the coordinator opens the contract and checks its `status` before any dependent Task starts", "refs": ["WC-2", "WC-4", "WC-5", "2.3"], "claim": "The workflow pre-creation exception leaves the coordinator step and WC-2 and WC-5 wording unadjusted; the exception can be read as controlling."}
{"id": "L37", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "the output flag its section 3 row gives (`--output <dir>` or `<file>`", "anchor2": "add a report path; contract", "refs": ["AC-1.2", "3.2"], "claim": "Several P1 rows name no output flag, so the live check cannot name it."}
```

verdict: PASS
