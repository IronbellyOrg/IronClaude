review: 3 of 3

# Spec-panel re-review 3 (critique mode, focus: requirements, architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `4e04817fb543edcb9c65e6cba29debf913eabe4a8ae7675d2f06bb264208171f`
- baseline: `.dev/orca-command-refactor/specs/history/spec-v2.md`, sha256 `f33929128f30fe63da2c9835b134305b0ef77d6fc1b02b5c98f2a04864840102`
- prior: `.dev/orca-command-refactor/review/round2.md`, sha256 `82a2e9469b98c4b4e11a873ae07f7fe5b84cc5611d223048f8fab0b5298faa5d` (header `review: 2 of 3`, last line `verdict: FAIL`, so N = 3; the review-3 halt applies only to a prior at `review: 3`)
- reviewer model: claude-sonnet-5-5
- panel: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (always active). Roles: CANDIDATE = the `@file`, BASELINE = spec-v2.md, PRIOR = round2.md.
- sandbox note: `README.md:3` and the inventories (`inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`) are the only checkable evidence. Citations the spec makes to `cmd/`, `sk/`, `CAPS:` lines are re-used from the inventories (`INV-A`, `INV-B`); source files are not in the workspace, so any `path:line` into them that I did not see in an inventory is UNVERIFIED.
- Guard Condition Boundary Table: the changed lines add guards only of the form "no output given" (WC-4); that single guard is tabled below. No other guard changed.

## Step 1: evidence block (`diff -w BASELINE CANDIDATE`)

Diff output: 8 hunks, all copied verbatim from the diff. `<` lines are BEFORE (baseline), `>` lines are AFTER (candidate). Long single-line table rows are quoted at the changed clause; the full line is the one at the cited candidate line.

Hunk 1 (candidate line 52, 2.1 Terms, "Contract file")
- BEFORE: `Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions ...`
- AFTER: `Each changed command except `/sc:load` adds a short `## Unattended mode` section that lists only its own gate resolutions ...`

Hunk 2 (candidate line 62, WC-4)
- BEFORE: `... or the parent directory of the file passed as `--output <file>`; a command whose section 3 row names a different fixed path (adversarial) uses that path. With no output given in the brief the command stops before doing work. ...`
- BEFORE: `... `status` (one of `succeeded`, `partial`, `failed`, `blocked`; an existing contract's own status values are mapped to these) ...`
- BEFORE: `... It is written on success, failure, blocked and partial outcomes, including stops before any other output exists, and is complete before `worker_done` is sent. ...`
- AFTER: `... or the parent directory of the file passed as `--output <file>`; each worker gets its own such directory, and two workers never share one (L1, WC-11). A command whose section 3 row names a different fixed path (adversarial) uses that path. A command with no output flag (cleanup-audit, index-repo, troubleshoot) writes the contract into the directory of the report its 3.1 row names, and the coordinator learns the path from `worker_done --report-path` (L1). Any other command given no output stops before doing work and writes no contract; the worker ends `failed` (WC-5). ...`
- AFTER: `... `status` (one of `succeeded`, `partial`, `failed`, `blocked`; a command that already writes a contract keeps its own status field and adds `status` with these values beside it) ...`
- AFTER: `... It is written on success, failure, blocked and partial outcomes, as long as its directory exists, and is complete before `worker_done` is sent. ...`

Hunk 3 (candidate line 76, section 3 intro)
- BEFORE: `Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.`
- AFTER: `Every changed command except `/sc:load` also gains the `## Unattended mode` section (section 2.1; L5). Phase numbers refer to section 6.`

Hunk 4 (candidate line 87, init-lite row, Resume column)
- BEFORE: `Fresh `--output` file per attempt (WC-6)`
- AFTER: ``--output` file in a fresh directory per attempt (WC-4, WC-6)`

Hunk 5 (candidate line 92, workflow row, Small fix column)
- BEFORE: `Write the contract for pre-creation STOPs too (WC-4 "every outcome") (P1)`
- AFTER: `None. A STOP before the package id exists has no directory and writes no contract (WC-4, L1) (P1)`

Hunk 6 (candidate lines 176-181, AC-C5)
- BEFORE: ``git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \| grep -E '^-' \| grep -v '^--- a/'` | prints nothing: edits are additive ...`
- AFTER: `... the AC-C5 command in the block under 7.1 | prints nothing: edits are additive ...` followed by a new fenced block: `git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md | grep -E '^-' | grep -v '^--- a/'`

Hunk 7 (candidate lines 192-193, 7.2 steps 3 and 4)
- BEFORE: `... its report path is the WC-4 contract path (in P0, the command's existing report file).`
- BEFORE: ``4. `test -s <contract>` and `uv run python -c "...assert d['status'] in {...}..." <contract>` ... **Pass:** both exit 0.`
- AFTER: `... its report path is the WC-4 contract path (in P0 there is no contract: the outcome is `succeeded` and the path is the command's existing report file, L17).`
- AFTER: ``4. `test -s <contract>` and (from P1; in P0 only `test -s` on the command's existing report file, which for `/sc:troubleshoot` is markdown, L17) `uv run python -c "..." <contract>` ...`

Hunk 8 (candidate lines 203-204, 208, AC-0.3, AC-0.4, AC-1.4)
- BEFORE: AC-0.3 check `git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md \| grep -E '^-' \| grep -v '^--- a/'`; AC-0.4 pass `step 4 uses the command's existing report file, since the contract arrives in P1`; AC-1.4 `... and the workflow return-contract ref` / `adversarial names one fixed path; workflow states the contract is written for pre-creation STOPs`
- AFTER: AC-0.3 `The AC-C5 command with `src/superclaude/core/HOW-WE-WORK.md` in place of the command file (L2)`; AC-0.4 pass `step 4 is `test -s` on the command's existing report file only, since the contract and its YAML assertion arrive in P1 (L17)`; AC-1.4 check `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md`, pass `adversarial names one fixed path`

Self-check: every AFTER line was found with `grep -nF` in the candidate and every BEFORE line in the baseline (no MISSING output); roles are not swapped. A synthetic input confirmed that the new AC-C5 pipeline prints deleted lines (`-gone`, `-- a/x y`) and drops only the `--- a/<file>` header.

## Prior blocking findings

| Prior id | Status | Re-check against the AFTER text only |
|---|---|---|
| L1 | resolved | R2-1: `candidate:62` now says "each worker gets its own such directory, and two workers never share one (L1, WC-11)", consistent with WC-11 (`candidate:69`). R2-2: `candidate:62` names the three flagless ready commands and gives them a contract location; every other command with no output stops with `failed` under WC-5 (`candidate:63`, "no report exists"). R2-6: status mapping is now a rule (own field kept, `status` added beside it); the workflow pre-creation case is decided in `candidate:92` and AC-1.4 (`candidate:208`), with no remaining text that asks for a pre-creation contract (`grep pre-creation` finds none). |
| L2 | resolved | The AC-C5 command is a fenced block with plain `|` (`candidate:178-181`); AC-0.3 reuses it (`candidate:203`). The synthetic run shows it flags deleted lines. The same escaped-pipe form survives in AC-C4 (`candidate:175`), which L2 did not name; see N2 (not blocking). |
| L4 | resolved | AC-C1 block (`candidate:183-186` region, hunk list shows no change) and its plain-`|` note are untouched, and no changed line adds an `orca` verb to a command, skill or agent file (SA-2, `candidate:147`). |
| L5 | resolved | The general text no longer gives `/sc:load` a section: `candidate:52` and `candidate:76` now say "except `/sc:load`", agreeing with the P1 row (`candidate:159`, "load (usage line only, no section)"), the 3.2 load row (`candidate:112`) and AC-1.1 (`candidate:205`). A residual AC-1.2 mismatch is N1 (not blocking). |
| L17 | resolved | 7.2 step 3 and step 4 no longer assert a YAML status on a markdown file in P0 (`candidate:192-193`), and AC-0.4 matches (`candidate:204`). `/sc:troubleshoot`'s REPORT.md is markdown (`INV-B:241-242`, "`report_path` (REPORT.md)"), so `test -s` is passable. |

## Findings on changed lines

Origin is `changed` unless marked. Medium and minor findings are listed under follow-up candidates and never fail this review.

### === REQUIREMENTS ANALYSIS ===

- N3 (MINOR, Wiegers, origin=changed, priority Low): 2.3 still says the coordinator states "the output directory, so the report path is known before dispatch (WC-4)" (`candidate:73`), while the changed WC-4 now lets cleanup-audit, index-repo and troubleshoot (and workflow) report the path only through `worker_done --report-path` (`candidate:62`). A coordinator following 2.3 alone believes it must supply a directory for a command that has no flag for one; the WC-4 text corrects it, so the reader is not led to a wrong build. Note only.
- N1 (MEDIUM, Adzic, origin=unchanged, depends on the changed WC-4 clause and the changed load exclusion at `candidate:52,62,76`, priority Medium): AC-1.2 runs "each P1 command with `--unattended --output <dir>`" (`candidate:206`), and the P1 row lists load, cleanup-audit and index-repo (`candidate:159`). The changed WC-4 says cleanup-audit and index-repo have no output flag (`candidate:62`), and load gets no section and so, by the P1 row, no `--unattended` flag. The grading sentence "an implementer who follows AC-1.2 as written builds a live check that passes `--output` to a command that has no such flag" holds only if "each P1 command" is read to include those three; AC-1.1 shows the author excepted load there, and 3.2 says load is a step inside another worker's brief, not its own Task. The text allows the worse reading, so this is Medium, not blocking. `INV-A:42,53` shows both commands write fixed locations (`.claude-audit/`, `PROJECT_INDEX.md`), which agrees with WC-4.

### === ARCHITECTURE ANALYSIS ===

- L7 (MEDIUM carried, Fowler, origin=unchanged, depends on changed WC-4 at `candidate:62`): the D1 example `/sc:troubleshoot "login fails" --unattended --output .` (`candidate:238`) passes `--output` to the command that WC-4 now says has no output flag. `INV-B:242` names only a default folder `.dev/troubleshoot/<slug>-<timestamp>/` (`cmd/troubleshoot.md:56`, UNVERIFIED in sandbox beyond the inventory). The changed line sharpens an open Medium finding; it does not make it blocking, because D1 is an open-decision example, not a requirement.
- Hohpe check, contract location: `candidate:62` makes the contract path derivable from `worker_done --report-path` for flagless commands and from the brief for the rest, a single rule with one named exception set. No second location is introduced. `INV-B:242` also records that troubleshoot already writes a `return-contract.yaml` when `--caller task-unified` (`SKILL.md:104,175,570`, UNVERIFIED beyond the inventory); the spec's "keeps its own fields and adds the missing ones" covers it.
- Nygard check, failure when the output directory does not exist: "as long as its directory exists" (`candidate:62`) is a deliberate narrowing; a stop with no directory ends `failed` via WC-5 and the coordinator still gets a `worker_done`. No hidden stall.

### Guard Condition Boundary Table (changed guards only; scoped re-review rule)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| output given | WC-4 (`candidate:62`) | Zero/Empty | no `--output-dir`, no `--output` | true (stop) | other commands stop before work, no contract, worker `failed` (WC-5); the three flagless ready commands write beside their report; workflow uses its package id | OK |
| output given | WC-4 | Legitimate Edge Case | `--output <file>` whose parent directory is shared by two workers | n/a | "each worker gets its own such directory, and two workers never share one" | OK |
| output given | WC-4 | Sentinel Value Match | `--output .` (D1 example) | n/a | not specified; `.` is a shared directory, which the new sentence forbids | OK (the example, L7, is Medium) |
| directory exists | WC-4 | Zero/Empty | directory absent at stop time | false | no contract; `failed` via WC-5 | OK |

Classes left out: One/Minimal and Maximum/Overflow cannot occur for a boolean-style "output given" guard.

### Whittaker adversarial pass (changed text only)

- Sequence attack on 7.2 in P0: step 3 now sets outcome `succeeded` with no contract; if a smoke command is actually blocked or fails in P0, `succeeded` is asserted by the check text regardless. I can break this specification by **Sequence Attack**. The invariant at **7.2 step 3 (`candidate:192`)** fails when **a P0 smoke run ends blocked**. Concrete attack: troubleshoot hits a stop in P0, writes no contract, the worker sends `--outcome failed`, step 3 says the outcome must be `succeeded`, so the check fails and AC-0.4 reports a "reopen section 1" failure for a command that behaved correctly. This needs the P0 smoke input to hit a stop; the three listed smoke inputs are real symptoms and small changes meant to succeed. MINOR, note only.
- Divergence attack on WC-4's two exception clauses: a command that is both flagless and has a fixed path in its row (cleanup-audit: `.claude-audit/pass<N>-summary.md`, `candidate:85`) satisfies both; both give the same directory, so no conflict.

## Coverage and limits

- Covered: all 8 changed hunks; every prior blocking finding; the dependents of the changed lines (WC-5, WC-11, 2.3, AC-1.1, AC-1.2, AC-1.4, AC-C5, 7.2 steps 3-4, the P1 row, the 3.1 and 3.2 rows named above, D1).
- Not covered: unchanged sections not tied to a changed line; the contents of `cmd/`, `sk/`, `~/.claude` (not in the sandbox, so every `cmd/` and `sk/` line the spec cites is UNVERIFIED except where an inventory repeats it); no live Orca run.
- Newly discovered older defect (the prompt asks to record it): N2.

## Follow-up candidates (Medium and minor; none blocks)

- N1 (Medium): add "except `/sc:load`" and an "or no output flag" clause to AC-1.2 (`candidate:206`).
- L7 (Medium, carried): the D1 example passes `--output` to troubleshoot (`candidate:238`).
- N2 (Medium, older defect, origin=unchanged, found at review 3; first appears in the baseline): AC-C4 (`candidate:175`) still writes the pipes as `\|`. Copied raw into a shell, git receives `|` as an argument, reports an ambiguous argument and exits non-zero with nothing on stdout, so "prints nothing" can pass while a `.claude/` path is staged (`CLAUDE.md:16` is the rule it guards; UNVERIFIED in the sandbox). It is the same defect class as L2, in a line L2 did not name. I grade it Medium and not blocking because the line is unchanged, the Review Loop makes an unchanged-line finding a note unless it quotes a changed line that depends on it, and the changed note at `candidate:177` states the right convention for the block that follows it. The user may want it fixed before P0 starts; fix by moving AC-C4 into a fenced block like AC-C5.
- N3 (minor): reconcile 2.3 (`candidate:73`) with the WC-4 exceptions.
- Remaining prior non-blocking findings L3, L6, L8-L16 are unchanged by this revision and stay open as recorded in `review/round2.md`; they do not affect this verdict.
- Per the Review Loop, the session that ran this review asks the user once whether to open an issue for these; none is created without an answer. This sandbox has no user, so the list is only recorded.

## Loop state

Review 3 of 3. No blocking finding is open, so there is no escalation and no Reviser brief (the Reviser brief is omitted at `review: 3`). Whole-document assurance would need a separate, labelled first review whose blockers are escalated, never a fourth review.

coverage: scoped PASS: changed lines + prior blockers

## Findings block

```findings-v1
{"id": "N1", "severity": "MAJOR", "blocking": false, "category": "unpassable-check", "anchor": "7.2 live check on each P1 command with `--unattended --output <dir>`", "anchor2": "A command with no output flag (cleanup-audit, index-repo, troubleshoot)", "refs": ["AC-1.2", "WC-4", "P1"], "claim": "AC-1.2 asks for --output on every P1 command although WC-4 says cleanup-audit and index-repo have no output flag and load gets no unattended mode."}
{"id": "N2", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "git diff --cached --name-only \\| grep '^\\.claude/'", "refs": ["AC-C4", "7.1"], "claim": "Copied raw, the escaped pipes make git reject the command with no stdout, so the check that no .claude path is staged can pass falsely."}
{"id": "N3", "severity": "MINOR", "blocking": false, "category": "contradiction", "anchor": "the output directory, so the report path is known before dispatch (WC-4)", "anchor2": "the coordinator learns the path from `worker_done --report-path` (L1)", "refs": ["2.3", "WC-4"], "claim": "2.3 says the path is known before dispatch while WC-4 lets some commands report it only afterwards."}
{"id": "L7", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "Example: `/sc:troubleshoot \"login fails\" --unattended --output .", "anchor2": "A command with no output flag (cleanup-audit, index-repo, troubleshoot)", "refs": ["D1", "WC-4", "3.1"], "claim": "The D1 example gives an output flag to troubleshoot, which WC-4 lists as having none."}
{"prior": "L1", "status": "resolved"}
{"prior": "L2", "status": "resolved"}
{"prior": "L4", "status": "resolved"}
{"prior": "L5", "status": "resolved"}
{"prior": "L17", "status": "resolved"}
```

verdict: PASS
