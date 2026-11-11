review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (critique mode, focus requirements,architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d7bacfaaecc8fff9a059e1e70fe785b1e6c52aecb2a57c161ca8d51cdcb3aa3c`
- baseline: none given (first review of the whole document, labelled whole-document audit)
- reviewer model used: claude-sonnet-5-5
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full, as the command's hard gate requires, `command.md:266-268`).
- citation convention: `spec:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `command.md:N` = the command definition given to this run.

## Coverage (what was covered, what could not be)

Covered: all of the spec (spec:1-288). Checked against the inventories: the 43-command split (counted 10 rows at spec:81-92, 27 rows at spec:97-125, 6 rows at spec:130-137; 21 in `INV-A:3` plus 22 in `INV-B:3`; the 10/27/6 split matches 5+13+3 in A and 5+14+3 in B); the phase table against the section 3 rows (P1 9, P2 11, P3 4, P4 3 = 27, and the 4 ready commands that get a P2 fix); every `CAPS:` line the spec cites for Orca facts (CAPS:44-47, 52, 58-68, 72-80, 97-103, 116, 130, 145-151, 155-161, 178-188 all say what the spec claims); the `INV-A:` and `INV-B:` lines for the contract gaps, gates and UNVERIFIED lists (INV-A:60-66, 76-83, 90-98, 106, 113-120; INV-B:43, 112, 272, 285-299, 311, 320-323).

Not checkable in this sandbox, so UNVERIFIED: every `cmd/`, `sk/`, `ag/`, `CLAUDE.md:N`, `HOW-WE-WORK.md:N`, `pyproject.toml:38`, `Makefile:N`, `install_core.py:N` and `EVIDENCE.md:N` / `.dev/codegraph-migration/...` citation made directly by the spec (they are not in the workspace); the claims that rest on them are accepted only as far as the inventory lines that quote them agree (for example `EVIDENCE.md:39,45` is quoted at `CAPS:31,49` and `INV-A:13`). The 340-citation re-check claimed at spec:288 is not reproducible here.

One extra input outside the workspace's `.dev/` tree: `command.md` itself already carries an `## Unattended mode` section (command.md:455-465). It is used below only as evidence of how the same contract was later read by an implementer, never as a requirement on the candidate.

## Prior blocking findings

None (first review).

## === REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn)

### F-01 BLOCKING (CRITICAL by consequence): AC-0.4 cannot pass as written, and its failure rule reopens the central decision

- Grading sentence: an implementer who follows the stated text as written runs the three P0 smoke runs, applies 7.2 step 3 as AC-0.4 says ("steps 1-3 and 5-7 pass"), and builds a check that can never pass, and that is wrong because step 3 requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (spec:182) while AC-0.4 itself says the contract "arrives in P1" (spec:194). In P0 `/sc:troubleshoot` reports `REPORT.md` (spec:91), `/sc:workflow` reports `.dev/tasks/to-do/<id>/return-contract.yaml`, which is not a directory the coordinator chose (spec:92), and `/sc:adversarial` writes its contract in a place "not fixed" until the P1 fix (spec:83). So for all three commands step 3 fails by construction, and "a failure here reopens section 1" (spec:194), i.e. a spec-induced false failure reopens the decision the whole document rests on.
- Expert: Adzic (a scenario that cannot pass), Wiegers (testability).
- Recommendation: change only AC-0.4 so that step 3 in P0 checks "exactly one `worker_done`, its `--outcome` follows the command's own report as WC-5 would read it, its `--report-path` names the command's existing report file", the same carve-out the text already gives step 4.
- Priority: High. Quality impact: Testability 6 -> 9; removes a false reopen of section 1.

## Follow-up candidates (Medium and minor; none triggers a revision, none is in the Reviser brief)

### Medium, requirements

- **F-02 Medium (MAJOR label): P1 scope and AC-1.1 pull P2-P4 work into P1.** P1 says `--unattended` is "accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (spec:159) and AC-1.1 asserts every one of the 37 commands has a `## Unattended mode` section naming `return-contract.yaml` (spec:196), while the gate resolutions, report files and contract for 25 of them arrive in P2-P4 (spec:160-162; rows spec:99-125). The text needs a guess about whether P1 writes gate text for commands that do not yet resolve gates. In the window between P1 and P2 a coordinator following section 2.3 (spec:73) would pass `--unattended` to `/sc:tdd` or `/sc:task` that still prompt, which is the silent stall WC-2 forbids (spec:60). Recommendation: state that until its phase lands a command's `--unattended` is not usable in a brief, or limit AC-1.1 to the commands whose phase has landed. Priority Medium. Expert: Wiegers.
- **F-03 Medium: where the contract goes is undefined for several commands.** WC-4 puts the contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is what the coordinator passed "(`--output` / `--output-dir`)" (spec:62). But `--output` is a file for `/sc:tdd` (spec:90) and `/sc:init-lite` (spec:87); `/sc:spec-panel` and 8 more rows say only "add `--output`" (spec:99,101,106,107,111,120,123) without saying file or directory; `/sc:load` gets a contract but no output flag (spec:112) although AC-1.2 passes `--output <dir>` to every P1 command (spec:197). Flag names also differ by row: `--output <dir>`, `--output <file>`, `--output-dir`, `--pass` (spec:83-85,92,105,116). When `--unattended` is given with no output location the spec says nothing (only post-release requires one, spec:113), although WC-4 demands a contract "including stops before any other output exists". Evidence that this is a real fork in the road: the later `command.md` had to add a third name, `--report-dir`, because "`--output` is file-valued" and to refuse the run when it is missing (command.md:460). Recommendation: add one table of "output flag, kind, contract path" per command to section 3 or the contract file. Priority Medium. Expert: Wiegers, Fowler (interface consistency).
- **F-04 Medium: WC-6 "fresh output directory" collides with WC-4's coordinator-chosen directory, and a re-invoke can leave a stale `blocked` contract.** WC-6 tells 19 rows to write "each run into a fresh output directory" (spec:64 and the "fresh dir" cells); WC-4 fixes the path before dispatch (spec:62). A retry whose brief repeats the same `<output-dir>` either overwrites in place (not fresh) or writes a subfolder (contract not at the path the coordinator will read). WC-3 re-invokes the command after an `ask` into the same place (spec:61), so a `status: blocked` contract from the first attempt is on disk until the second finishes; if the second dies early the coordinator reads the wrong status. Recommendation: say that the coordinator gives each retry a new `<output-dir>`, and that a command removes or overwrites an existing contract at start. Priority Medium. Expert: Nygard, Wiegers.
- **F-05 Medium: `partial` maps to `succeeded` but is never defined, and Orca treats `succeeded` as settling the Task.** WC-5 sends `partial` to `--outcome succeeded` (spec:63) and the Decisions row justifies it as "a usable deliverable" (spec:266); WC-4 lists `partial` without saying what qualifies (spec:62). A `succeeded` report settles the Task, which makes dependent Tasks ready (`CAPS:77`, `CAPS:84-92`), and section 1.3 proposes dependent chains such as troubleshoot workers then one adversarial worker (spec:39). The spec leans on the coordinator opening the report (spec:73), so the harm needs the coordinator to skip that. Recommendation: define `partial` as "deliverable usable, named gaps listed in the contract" and have the coordinator rule check `status` before starting dependents. Priority Medium. Expert: Adzic, Nygard.
- **F-06 Medium: requirements with no acceptance check, and one check with no subject.** WC-1 (spec:59) has no phase item and no AC beyond the generic `state: ready` in 7.2 step 1 (spec:180); WC-3's ask relay and resume-by-ID have no AC (AC-2.2 tests only the blocked path, spec:202); WC-10 wait splitting is checked only for pr-submit (AC-4.3, spec:213), not for cli-eval, which the spec names (spec:104); WC-12 `check`/`consumer_fenced` has none (spec:70). AC-0.5 runs `pytest ... -k outcome` "on planted contracts" (spec:195), but WC-5 is a prose rule for a model and non-goal 3 forbids new programs (spec:218), so nothing exists to map a status to an outcome. Recommendation: add the missing checks, or say AC-0.5 asserts the mapping text in `WORKER-CONTRACT.md`. Priority Medium. Expert: Wiegers, Crispin.
- **F-07 Medium: `--unattended` token rules are not specified.** D1 chooses an explicit flag because it "cannot misfire on a person" (spec:231), but nothing says it counts only as a standalone argument outside quoted content. Specs and topics are passed as quoted text (for example `/sc:tdd "auth"`, spec:202); a quoted input that contains the string would flip the mode. The later `command.md` added exactly this rule (command.md:459). Recommendation: add the one sentence to WC-2. Priority Medium. Expert: Whittaker (sentinel collision).
- **F-08 Medium: WC-11 is a "must never" with no mechanism for commands that edit code in a shared worktree.** WC-11 says two workers in one worktree "must never write the same file" (spec:69), workers share the current worktree by default (`CAPS:115`), and cleanup, improve, document, implement and task edit existing files (spec:103,107,109,110,121) whose targets the command cannot promise in advance; only `save` and default output paths are handled. Recommendation: put "disjoint targets or separate worktrees" in the brief checklist of 2.3. Priority Medium. Expert: Nygard.
- **F-09 Medium: existing contract vocabularies are not reconciled with the four-value `status`.** WC-4 says commands with a contract "keep their fields and add the missing ones" (spec:62) and fixes `status` to four values; the workflow contract already carries a `status` and a version (`contract 1.1`, `INV-B:272`) whose values this inventory does not list. If its values differ, two requirement sentences disagree. No `contract_version` field is required, so a coordinator cannot tell vintages apart. UNVERIFIED which values exist (the file is not in the workspace). Recommendation: add the mapping per existing contract and a version field. Priority Medium. Expert: Newman (versioning).
- **F-10 Medium: coverage of the command set is asserted, not checked.** The spec says "The 43 commands in `cmd/`" (spec:76) from two inventories dated 2026-11-02 (`INV-A:3`, `INV-B:3`); AC-1.1 checks the two lists against each other (spec:196) but nothing enumerates the directory, so a command added later is in neither list. The command list available to this session also shows `sc:graph`, `sc:impact` and `sc:issue`, which appear in neither `INV-A:3` nor `INV-B:3` (UNVERIFIED, the directory is not in the workspace). Recommendation: add a test that lists `cmd/*.md` and fails on a name in none of sections 3.1, 3.2, 4. Priority Medium. Expert: Wiegers (traceability).
- **F-11 Medium: WC-3 passes the coordinator's answer "verbatim as the flag"** (spec:61) with no rule on quoting or validation. A free-text answer that contains another flag (for example a post flag that WC-9 holds off, spec:67) could reach the command line if the worker concatenates it. Needs a careless implementer, hence Medium. Recommendation: say the answer is one quoted value and never parsed for flags. Priority Medium. Expert: Whittaker.
- **F-12 Medium: workflow pre-creation STOP contract is unconditional in AC-1.4 but SA-3 allows new files only in unattended mode.** AC-1.4 requires "workflow states the contract is written for pre-creation STOPs" (spec:199); the current text says it is not written then (`INV-B:272`); SA-3 (spec:148) forbids a plain run writing a new file. Readable consistently only by assuming AC-1.4 means unattended. Recommendation: add "under `--unattended`". Priority Low-Medium.

### Medium, architecture

- **F-13 Medium: crash and early-death behaviour of the report.** WC-4 requires the contract "on every outcome" (spec:62); a killed, context-exhausted or timed-out worker cannot write it, and the only fallback is WC-5's "no report exists -> failed" (spec:63). Whether Orca bounds a Dispatch's run time is UNVERIFIED (`CAPS:188`, spec:285). Recommendation: write a `status: running` stub at the start, so a stale stub is distinguishable from a missing file. Priority Medium. Expert: Nygard.
- **F-14 Medium: tasklist and reflect interplay is chosen without a Decisions entry.** The tasklist row has Stage 10.5 pass `--unattended` to each reflect so the headless auto-accept rule applies (spec:122); the inventory recommended calling reflect without `--remediate` and running the fan-out at the worker's top level (`INV-B:215`), and noted that who answers the offer inside subagents is unknown (`INV-B:323` item 8). Auto-accepting a remediation hand-off starts more nested work and writes more files than the inventory option. Depth is asserted "inside Claude Code's nesting limit" (spec:122) without counting tasklist -> reflect -> reviewers -> adversarial advocates (`INV-B:36`, `INV-A:14`). Recommendation: add the choice and the depth count to Decisions. Priority Medium. Expert: Fowler, Newman.
- **F-15 Medium: D3 option (b) sits against the command's own text.** The inventory records "Will Not: run headless / imply a daemon" for pr-submit (`INV-B:90`); D3(b) and the pr-submit row (spec:114,244) do not address it. Recommended option is (a), so no wrong outcome unless the user picks (b). Priority Low-Medium.
- **F-16 Medium: interface shape.** One flag, `--unattended`, bundles three concerns (no gates, outward defaults off, contract on, spec:51,60,67). That is a defensible choice (D1), but a caller who wants a contract without losing prompts has no way to ask; SA-1 only protects the opposite direction. Priority Low. Expert: Fowler.

### Minor notes (never fail the review)

- Leftover reviewer tags `[M2]`, `[M4]`, `[M7]`, `[M9]`, `[M10]`, `[B1]` are scattered through the final text (for example spec:61,63,83,92,105,112) and point at a review file that is not part of the spec.
- `Phases 1-3 need no user decision` (spec:154) versus `Phases 0-3 can proceed on the recommendations` (spec:228): D1 is a decision that P0 and P1 depend on.
- SA-4 lists the allowed rewrites of existing lines (spec:149) but not the `Usage` line change that adding `[--unattended]` to every command implies; AC-C5 (spec:176) would flag an in-place edit. Appending a new line avoids it, as `command.md:22-23` does.
- 7.2 step 4 relies on PyYAML as "a declared dependency, `pyproject.toml:38`" (spec:183); `CLAUDE.md` lists only pytest, click and rich as dependencies. UNVERIFIED either way.
- E3 cites `invocation_method: "skill-direct"` as support (spec:23) while 1.4(1) says the direct route is unproven (spec:43). The text is honest about it; reading order could mislead.
- The CAPS line citation in WC-5 (`CAPS:76-77`, spec:63) points at the pane and settle rules, which support the sentence about sending once; the outcome rule itself is `CAPS:73`.

## === ARCHITECTURE ANALYSIS === (Fowler lead, Newman, Hohpe, Nygard)

- Decision soundness: the main decision (Orca on top, commands unchanged units) is supported by `CAPS:97-103` (depth 1, so a command cannot start workers), `CAPS:148-150` (lifecycle messages only from the dispatched pane) and `INV-A:90`, `INV-B:285-286` (controller commands). I found no stated text that contradicts it. The two honest gaps (spec:43-45) are real and P0 tests them.
- Boundaries (Fowler): coordinator-only list of six is consistent with both inventories (`INV-A:90-92`, `INV-B:285-287`); `/sc:git` is worded more softly than `INV-A:91` ("every operation") but lands in the same place.
- Integration (Hohpe): report by file pointer plus `--report-path` metadata that Orca does not check (`CAPS:79`) is stated correctly; ordering and duplicates are covered by "exactly once" (spec:63) and resume-by-ID (spec:61).
- Reliability (Nygard): silent stall is the main failure mode and is covered by `agentWait` polling (spec:181); unfinished: F-13 (crash), F-04 (stale file), WC-10 beyond two commands (see G2 below).
- Evolution (Newman): no contract version field (F-09); the plugin mirror question is declared UNVERIFIED item 8 (spec:282) but no AC covers `plugins/superclaude/commands/`.

## Whittaker attacks (every finding in the command's template)

1. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-2 / D1 (spec:60,231)** fails when **a quoted input contains the text `--unattended`**. Concrete attack: before, `/sc:spec-panel "…the user passes --unattended…"` runs attended; after, the mode switches on, prompts vanish, outward defaults go off. Severity MAJOR -> Medium (F-07).
2. I can break this specification by **Sequence Attack**. The invariant at **WC-3 / WC-4 (spec:61-62)** fails when **the command is re-invoked after an `ask` and dies before writing**. Concrete attack: attempt 1 writes `status: blocked` to `<out>/return-contract.yaml`; the coordinator answers; attempt 2 crashes; the file still reads `blocked`; the worker reports `failed` for the wrong reason. Medium (F-04, F-13).
3. I can break this specification by **Divergence Attack**. The invariant at **WC-5 (spec:63)** fails when **`status: partial`**. Concrete attack: contract says `partial` with the key deliverable missing; Orca marks the Task completed; `task-list --ready` offers the dependent Task. Medium (F-05).
4. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (spec:62)** fails when **no output location is passed**. Concrete attack: `/sc:analyze X --unattended` with no `--output`; the contract has no place to go; "written on every outcome" cannot hold. Medium (F-03).
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (spec:68)** fails when **a command makes a single tool call longer than 5 minutes that is not one of the two named commands**. Concrete attack: `/sc:test` or `/sc:build` runs a 12-minute Bash call; no heartbeat; no AC fails (AC-4.3 covers pr-submit only). Medium (F-06).
6. Sequence attack on AC-0.4 / 7.2 step 3 is F-01 (blocking).

## Guard Condition Boundary Table

Classes left out: "Maximum/Overflow" for G1, G5 (a status or a confidence value has no capacity); "Sentinel" for G2, G3, G4, G5 (no sentinel value in that guard).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 outcome mapping | spec:63 | Zero/Empty | `status: ""` | falls to failed | `--outcome failed` | OK |
| G1 outcome mapping | spec:63 | One/Minimal | report file missing | falls to failed | `--outcome failed` | OK |
| G1 outcome mapping | spec:63 | Typical | `succeeded` | succeeded | `--outcome succeeded` | OK |
| G1 outcome mapping | spec:63 | Sentinel Value Match | `done` | not in set | `--outcome failed` | OK |
| G1 outcome mapping | spec:62-63 | Legitimate Edge Case | `partial` | succeeded | maps to succeeded; "usable" never defined | GAP (F-05, Medium) |
| G2 wait split | spec:68 | Zero/Empty | no long wait | n/a | none needed | OK |
| G2 wait split | spec:68 | Typical | 3-minute wait | within 4 min | heartbeat between waits | OK |
| G2 wait split | spec:68,213 | Legitimate Edge Case | exactly 240 s | within | AC-4.3 says "exceeds 240 s" fails | OK |
| G2 wait split | spec:68,104,114 | Maximum/Overflow | one tool call over 5 min in a command other than cli-eval, pr-submit | breaches | unspecified | GAP (F-06, Medium) |
| G3 readiness | spec:59 | Typical | 30 s startup prompt fallback | passes | passes (`EVIDENCE.md:45` via `CAPS:49`) | OK |
| G3 readiness | spec:59 | Legitimate Edge Case | fallback above ~45 s | fails | fails again | OK |
| G3 readiness | spec:59 | Maximum/Overflow | `--timeout-ms` very large | not stated | upper bound UNVERIFIED (`CAPS:31`); no owner or phase for WC-1 | GAP (F-06, Medium) |
| G4 depth | spec:33,66 | Zero/Empty | coordinator at depth 0 | may dispatch | OK | OK |
| G4 depth | spec:33,66 | Typical | worker at depth 1, max 1 | refused | command must not call `worker-start` (WC-8) | OK |
| G4 depth | spec:255 | Maximum/Overflow | setting raised to 2 (D5 b) | would allow | WC-8 still forbids; consistent | OK |
| G5 task confidence | spec:121 | Zero/Empty | 0.0 | below 0.70 | blocked | OK |
| G5 task confidence | spec:121 | Legitimate Edge Case | exactly 0.70 | "below" is false | proceeds (source `cmd/task.md:93` UNVERIFIED) | OK |
| G6 mode switch | spec:51,231 | Typical | `--unattended` standalone | on | on | OK |
| G6 mode switch | spec:231 | Sentinel Value Match | `--unattended` inside quoted input | unspecified | unspecified | GAP (F-07, Medium) |
| G6 mode switch | spec:62 | Zero/Empty | mode on, no output location | unspecified | unspecified | GAP (F-03, Medium) |
| G7 ask relay | spec:61 | Typical | answer arrives | relay | passed as flag value | OK |
| G7 ask relay | spec:61 | Zero/Empty | empty answer | unspecified | unspecified | GAP (F-11, Medium) |
| G7 ask relay | spec:61 | Sentinel Value Match | answer containing a flag | unspecified | passed "verbatim" | GAP (F-11, Medium) |
| G7 ask relay | spec:61,284 | Legitimate Edge Case | ask timeout | pending | resume same ID | OK |

FR-8/FR-9 graded by consequence: every GAP above names a wrong outcome that needs an implementer's guess or a careless reading, so each is Medium (follow-up), none blocking. FR-10: the table is complete for the guards the spec states; the table was built before this synthesis.

## Quantity Flow Diagram (Pipeline Dimensional Analysis: classification of commands into phases)

```text
[Source: 43 commands (INV-A 21 + INV-B 22)] --> [Stage 1: classify] --> [10 ready | 27 needs-change | 6 coordinator-only]   (10+27+6 = 43, no loss)
                                                  |
                                                  v
                                   [Stage 2: assign phase]
                                     P0 smoke: 3 of the 10 ready
                                     P1: 9 (needs-change) + fixes to 4 ready (adversarial, cleanup-audit, index-repo, workflow)
                                     P2: 11 (needs-change) + 4 ready get gate fixes (reflect, release-split, tdd, troubleshoot)
                                     P3: 4   P4: 3          (9+11+4+3 = 27, no loss)
                                                  |
                                                  v
                  [Consumer AC-1.1: expects the 37 in sections 3.1+3.2 and none of the 6]   <-- count correct for the two lists
                  [Consumer "43 in cmd/" (spec:76): no check against the directory]          <-- UNCHECKED (F-10)
```

No count mismatch in the lists themselves; the one open edge is the unchecked directory total.

## Reviser brief

Blocking finding ids: F-01. Rules (restating Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Medium and minor findings (F-02 to F-16 and the notes) are not to be edited. No brief clause was overridden.

Open-issue question: the session that ran this review would ask the user once whether to open an issue for the follow-up candidates; this run has no user, so it records the list only and creates none.

verdict: FAIL
