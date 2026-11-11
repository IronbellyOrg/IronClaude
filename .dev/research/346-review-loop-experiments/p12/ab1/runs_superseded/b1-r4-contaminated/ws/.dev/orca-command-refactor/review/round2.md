review: 2 of 3

# Re-review (critique mode, focus requirements,architecture)

- candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md, sha256 a86859da35221feef00405e0c095e0a2d20bb75210af188b81511d9626e0e50d (58235 bytes)
- baseline: .dev/orca-command-refactor/specs/history/spec-v1.md, sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d (57763 bytes)
- prior: .dev/orca-command-refactor/review/round1.md, sha256 c211c18e984ac772faafc27939bf17564c140520e1fe7ea03756d18f5f24e8a2 (prior header `review: 1 of 3`, verdict FAIL)
- reviewer model used: claude-sonnet-5-5
- read first: the review-loop prompts file (~/.claude/rules/prompts/document_review_loop_prompts.md, RE-REVIEW prompt) and .dev/orca-command-refactor/README.md. Inventory citations below are checked only where I opened the file in the workspace; any citation I could not open is marked UNVERIFIED.
- Roles fixed by the table in the prompt: CANDIDATE = revised spec, BASELINE = spec-v1.md, PRIOR = round1.md. Not inferred from reading order.
- Brief clauses overridden: none. The brief names no scope wider than the changed lines and the prior blocking findings.

## Step 1: evidence block

`diff -w BASELINE CANDIDATE` gives 8 changed lines (4 before, 4 after, 3 hunks: 62c62, 159c159, 194,195c194,195). Changed lines copied verbatim (long table rows are shortened with `[...]` where the text is unchanged; the changed words are complete).

BEFORE (baseline), lines starting `<`:

- spec-v1.md:62: `... In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern [...]`
- spec-v1.md:159: `... the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate); output flags for commands that lack one; [...]`
- spec-v1.md:194: `... steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1`
- spec-v1.md:195: `... asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes`

AFTER (candidate), lines starting `>`:

- spec:62: `... where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`); when `--output` is a file (tdd, init-lite, spec-panel), `<output-dir>` is that file's parent directory, which the brief must dedicate to the run (M3); adversarial is the stated exception at `<output>/adversarial/return-contract.yaml` (M3). It follows the return-contract pattern [...]`
- spec:159: `... the `--unattended` flag accepted by every command in sections 3.1 and 3.2 whose phase is P1 (a no-op where a command has no gate); commands of P2-P4 gain it in their own phase (M5); output flags for commands that lack one; [...]`
- spec:194: `... steps 1-3 and 5-7 pass; steps 3 and 4 use the command's existing report file (its path for the report-path match, its stated outcome for `--outcome`), since the contract arrives in P1 (M2). Record the results in the phase report; a failure here reopens section 1`
- spec:195: `... asserts that every command in sections 3.1-3.2 whose phase is P1 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command and none of pr-submit, implement, post-release (P4) has one yet (M5) | passes`

Self-check (run): each AFTER fragment was found with `grep -nF` in the candidate at lines 62, 159, 194, 195 (the three "stated exception", "steps 3 and 4 use the command's existing report file" and "whose phase is P1 has" probes each matched once); the BEFORE fragments exist in the baseline at the same line numbers (the diff is line-for-line, so no role swap). Roles are correct.

## Prior blocking findings table

| id | prior status | now | evidence (AFTER text only) |
|---|---|---|---|
| M2 | blocking, confirmed | resolved | spec:194 now says "steps 3 and 4 use the command's existing report file (its path for the report-path match, its stated outcome for `--outcome`)". The failing condition of M2 was step 3 (spec:182, unchanged) requiring "the contract's `status`" and "the WC-4 contract path", which do not exist in P0; spec:194 now relaxes step 3 the same way it relaxes step 4. For troubleshoot the existing report is `REPORT.md` (spec:91), and the contract arrives in P1 (spec:159). The check can now pass in P0. |
| M3 | blocking, confirmed | resolved | spec:62 now states one rule for `--output` as a file: the contract goes in the file's parent directory, dedicated to the run, for tdd, init-lite and spec-panel; adversarial is the stated exception at `<output>/adversarial/return-contract.yaml`, matching spec:83. `/sc:tdd "auth" --unattended --output <file>` (AC-2.2, spec:200) now has a defined contract path (`<parent of file>/return-contract.yaml`), so `test -s <contract>` (spec:183) has a path to test. Residual cases that M3 listed but the fix does not cover (cleanup-audit, index-repo, post-release, spec-panel flag) are Medium, see follow-up candidates F1 and F2. |
| M5 | blocking, confirmed | resolved | spec:159 and spec:195 now limit the P1 flag and AC-1.1 to commands whose phase is P1, and AC-1.1 asserts that pr-submit, implement and post-release (P4) have no section yet. The conflict with spec:154 and spec:225 ("Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4") and with D3(a) ("no pr-submit changes in Phase 4", spec:240) is gone: the three commands are P4 rows at spec:109, 113, 114 and spec:162. AC-1.1 can pass on the recommended path. |

Not prior blocking findings (the VERIFY step rejected them, round1.md:12, 73, 98): M1 and M4. They are notes, unactioned. Their rows are not re-graded here. (M1's texts, AC-1.1 and the load row at spec:112, are not on a changed line: AC-1.1 changed only by the phase scope, and `load` is still "P1 (usage line only)".)

## New findings on lines changed against the baseline

None blocking. Checked each changed line for a wrong outcome an implementer would produce.

| id | origin | grade | finding |
|---|---|---|---|
| N1 | changed | Medium | spec:194 (AC-0.4) says steps 3 and 4 use "the command's existing report file", but step 4 as written (spec:183) runs `yaml.safe_load` on `<contract>` and asserts `d['status']` and `d['command']`. For troubleshoot the existing report is `REPORT.md` (spec:91), which is markdown. An implementer reads "uses the existing report file" as the `test -s` part only or as the whole of step 4; this needs a guess about which. It is not a stated text that contradicts, so Medium (follow-up candidate F3). |
| N2 | changed | minor | The new WC-4 text lists spec-panel as a command whose `--output` is a file, while spec:120 still says "add `--output`". The two agree (the flag is to be added). The sandbox definition of the command already has a file-valued `--output` and a separate `--report-dir` (command.md:23, 460-461, outside the workspace, UNVERIFIED as evidence for this spec); see F2. |

## Findings on unchanged lines (all minor notes unless they quote a changed line)

- I1 (origin=unchanged, minor): spec:182 (step 3 of 7.2) still says "the contract's `status`" and "the WC-4 contract path". It is overridden for P0 by spec:194 and correct for P1 onward. Minor because spec:194, the changed line, resolves it.
- I2 (origin=unchanged, minor): load row (spec:112) "usage line only" against AC-1.1 requiring a contract-naming section on every P1 command. Same text as the rejected M1; not regraded.

## Requirements analysis (Wiegers, Adzic, Cockburn), scoped to changed lines

- Wiegers: the three changed requirements (WC-4 location, P1 flag scope, AC-0.4/AC-1.1 pass conditions) are now testable. The WC-4 rule has a definite directory for file-valued `--output`; the one remaining ambiguity is for commands with no output flag (F1).
- Adzic example, `/sc:tdd "auth" --unattended --output .dev/x/auth-tdd.md`: before the revision `<output-dir>` = `.dev/x/auth-tdd.md` (a file, untestable); after, the contract is `.dev/x/return-contract.yaml`. State trace: contract absent -> command runs -> `.dev/x/return-contract.yaml` written with `status: blocked`. Passes AC-2.2.
- Cockburn: the primary actor of AC-0.4 is the P0 smoke-run implementer; after the fix the relaxed pass conditions name what to compare (report path and stated outcome).

## Architecture analysis (Fowler, Newman, Hohpe, Nygard), scoped to changed lines

- Fowler: the only boundary change is the addition of one rule to WC-4 (file-valued output; adversarial exception). It adds no section or mechanism. The `<output>/adversarial/` sub-directory exception is a named inconsistency inside one table cell; it is stated, not hidden, and tied to the row at spec:83.
- Newman: `--unattended` stays an additive interface; moving its introduction into each command's own phase (spec:159) removes the interim state in which a command accepted the flag without converting its gates (the concern of rejected M4 does not need a fix, but the change reduces the interim window).
- Hohpe: report hand-off stays a pull model (worker passes the contract path, coordinator opens it); no change.
- Nygard: a parent directory "dedicated to the run" (spec:62) is a precondition on the brief; if the coordinator passes a shared directory, two workers could overwrite one `return-contract.yaml`. WC-11 (spec:69) already says two workers in one worktree must never write the same file, so the dedication rule is consistent with it and the failure is covered by a stated rule (no finding).

## Whittaker adversarial analysis (changed lines only)

- I can break this specification by **Divergence Attack**. The invariant at **spec:62** ("`<output-dir>` is that file's parent directory") fails when **`--output` is a bare filename with no directory part**. Concrete attack: `/sc:init-lite --unattended --output context-audit.md`; before: no contract; after: parent is `.` (the worktree root), and the contract is `./return-contract.yaml`, in the shared worktree root where a second concurrent worker writes the same name. WC-11 (spec:69) forbids the collision, and "which the brief must dedicate to the run" (spec:62) forbids the brief. The text covers the case, so no finding. Minor.
- I can break this specification by **Sequence Attack**. The invariant at **spec:159 vs spec:162** fails when **a coordinator runs a P2 command with `--unattended` after P1 only**. Concrete attack: `/sc:auggie-review <PR> --unattended` after P1; before the revision the flag was accepted with the outward default still on; after, the command does not yet accept the flag (the flag arrives in P2), so the coordinator sees an unrecognised argument, not a silent post. The wrong outcome of the prior M4 no longer exists on the changed text. No finding.
- Zero/Empty, Sentinel Collision and Accumulation attacks: nothing on the changed lines names a concrete wrong outcome. Pipeline Dimensional Analysis is not triggered (the phase table is sequencing, not a data pipeline).

## Guard Condition Boundary Table (changed-line guards only)

Guards: G-A WC-4 `--output` is a file (spec:62); G-B P1 flag scope "phase is P1" (spec:159, 195); G-C AC-0.4 P0 relaxation (spec:194). Classes left out: Maximum/Overflow for G-A, G-B, G-C (presence or enum tests, no capacity); Sentinel Value Match for G-B and G-C (no sentinel).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G-A `--output` is a file | spec:62 | Zero/Empty | no `--output` | false | post-release: "require an explicit `--output` ... else blocked" (spec:113); where the blocked contract goes is not stated; cleanup-audit and index-repo have no output flag (spec:85, 86) | GAP (Medium, F1) |
| G-A | spec:62, 90, 200 | Typical | `--output .dev/x/auth-tdd.md` | true | contract at `.dev/x/return-contract.yaml`, parent dedicated to the run | OK |
| G-A | spec:62 | One/Minimal | `--output auth.md` (no directory part) | true | parent is `.`; collision covered by WC-11 (spec:69) and the "dedicate" clause | OK |
| G-A | spec:62, 83 | Legitimate Edge Case | `--output <dir>` for adversarial | exception | `<output>/adversarial/return-contract.yaml` | OK |
| G-B phase is P1 | spec:159, 195 | Typical | analyze, build, test | true | section and flag in P1; AC-1.1 asserts | OK |
| G-B | spec:159, 195 | Legitimate Edge Case | `load` (P1, usage line only, no report) | true | AC-1.1 requires the section; the load row (spec:112) writes no report | GAP (note; same text as rejected M1, not regraded) |
| G-B | spec:159, 195 | Sentinel-like | pr-submit under D3(a) (never a worker) | false | AC-1.1 asserts it has no section "yet"; consistent with D3(a) (spec:240) | OK |
| G-C P0 relaxation | spec:194 | Typical | troubleshoot, `REPORT.md` | true | path match and stated outcome from `REPORT.md` | OK |
| G-C | spec:194 vs 183 | Legitimate Edge Case | step 4 YAML parse of a markdown report | ambiguous | step 4 "uses the existing report file" but the parse assertion is for YAML | GAP (Medium, F3) |

Table complete: every guard is enumerated, every cell populated, omitted classes carry their reason (FR-10 satisfied). GAP rows are Medium (no concrete wrong outcome without an extra guess), not blocking under FR-8. `--focus correctness` is not active: no State Variable Registry.

## Coverage

Covered: the 8 changed lines against the baseline (3 hunks), the 3 prior blocking findings (M2, M3, M5), and the lines these changes depend on (spec:62, 69, 83, 85-87, 90, 109, 112-114, 120, 154, 159, 162, 182-183, 194-195, 200, 225, 240). Not covered: unchanged text elsewhere in the spec (not reviewed; whole-document assurance needs a separately labelled first review). Inventory files were not re-read except where cited above; citations to `INV-*`, `CAPS:*` and `cmd/*` inside the spec are carried from the spec and UNVERIFIED by this review.

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium (warnings):

- F1: WC-4 (spec:62) names `<output-dir>` as "the directory the coordinator passed", but cleanup-audit (output dir fixed, spec:85) and index-repo (location implied, spec:86) have no flag, and post-release (spec:113) requires `--output` without saying file or directory or where a blocked contract goes with no `--output`. Source: the prior round1 follow-up on M3 (round1.md:123 and :136, "G2 Zero/Empty"); not new, still open.
- F2: the spec-panel row (spec:120) says "add `--output`", but the sandbox definition of the command already has a file-valued `--output` and a separate `--report-dir` that carries the contract (command.md:23, 460-461). WC-4 as revised would put spec-panel's contract at the parent of `--output`; the command defines `<report-dir>/return-contract.yaml`. UNVERIFIED in the workspace (the inventory at INV-B:177-185 describes an older command with no `--output`).
- F3: AC-0.4 step 4 for a markdown `REPORT.md` (see N1).

Minor: I1, I2 (above), N2.

Noted, unactioned (carried from round1.md): M1 and M4.

The session that ran this review asks the user once for this loop whether to open an issue for the follow-up candidates and creates none without the answer.

## Reviser brief

none: no open blocking finding. (Reviser contract unchanged: revise only text a blocking finding names; add no rule, mechanism or section; cite the finding id; prefer deleting or narrowing; report byte sizes.)

coverage: scoped PASS: changed lines + prior blockers

verdict: PASS
