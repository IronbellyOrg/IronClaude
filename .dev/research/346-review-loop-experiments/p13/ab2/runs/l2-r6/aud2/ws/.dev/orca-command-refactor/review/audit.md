review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document, first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec, a first review of the full document
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `e83580105a91cbd66307f4ec8d971d860124f6e64bbad15157d508a0bfc3be1e`
- baseline: none given (first review, `--re-review` and `--baseline` both absent, so nothing is recorded as missing)
- reviewer model: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full; hard gate satisfied)
- panel (fixed order, this focus): Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Nygard, Whittaker (active in every panel), Newman, Hohpe
- iterations: one review whatever `--iterations` says; Improve step not run and no revised specification written (brief: write only this file)
- evidence available: `README.md` and the three files under `inventory/` only. `EVIDENCE.md`, `src/`, `CLAUDE.md`, `install_core.py` and the skill/command files are not in the workspace, so every citation to them is UNVERIFIED here. Citations to `INV-A`, `INV-B`, `CAPS` and `README.md` were spot-checked and are marked verified where they were.

## Coverage statement

Covered: all 285 lines. Recounted the 10/27/6 split from the section 3 tables (10 + 27 + 6 = 43; per-phase counts 9 + 11 + 4 + 3 = 27; P2 list = 15 = 11 rows + reflect, release-split, tdd, troubleshoot). Checked 22 CAPS citations (CAPS:44-53, 58-80, 97-103, 107-116, 129-130, 145-162), 22 INV-A citations and 21 INV-B citations against the inventories. Cross-checked requirements WC-1..WC-12, SA-1..SA-6, section 6 phases, section 7 acceptance checks and D1-D5 against each other.
Not covered: any claim whose only source is outside the workspace (UNVERIFIED list at the end); behaviour of the real commands.

## Grading method

Each blocking finding carries the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" with no extra assumption. A finding that needs a guess, or a requirement the spec never states, is Medium and sits under follow-up candidates.

## Guard Condition Boundary Table (mandatory artifact, built before synthesis)

Triggered: the spec states thresholds and guards (60 s readiness, 5 min heartbeat, 4 min wait, depth 1, confidence 0.70, three failures, status sets). Responsibility: Nygard (construction), Crispin's completeness role folded into Adzic/Wiegers here because the focus did not select her, Whittaker (attack). Classes left out are given one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `<output-dir>` is a directory | WC-4 (spec:62), section 3 intro (spec:76) | Typical | `--output <dir>` (adversarial, brainstorm) | dir | contract at `<dir>/return-contract.yaml` | OK |
| `<output-dir>` is a directory | WC-4 (spec:62); tdd (spec:90); init-lite (spec:87) | Legitimate Edge Case | `--output docs/tdd/auth.md` (a file) | no directory passed | none: contract path undefined | GAP (see B-1) |
| `<output-dir>` is a directory | WC-4 (spec:62); cleanup-audit (spec:85); index-repo (spec:86) | Zero/Empty | no output flag in the brief | no directory passed | none: the brief passes nothing | GAP (see B-1) |
| report-file existence | WC-5 (spec:63) | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| contract `status` value | WC-5 (spec:63), WC-4 (spec:62) | Sentinel Value Match | `status` outside the four-value set, or an existing contract's own vocabulary (workflow, `INV-B:272`) | unknown | not specified; "keep their fields" and "fixed four-value set" (spec:62, 262) can collide | GAP (see M-3) |
| contract freshness | 7.2 step 4 (spec:183), WC-6 (spec:64) | One/Minimal | retry reuses the same `--output`, run dies before writing | stale file exists | `test -s` passes on the first attempt's file | GAP (see M-1) |
| heartbeat vs wait | WC-10 (spec:68) | Maximum/Overflow | single wait of exactly 5 min, or 4 min 30 s | 5 min cadence vs 4 min cap | cap is 4 min; 4-5 min band covered by "at most 4" | OK |
| heartbeat vs wait | WC-10 (spec:68) | Zero/Empty | wait of 0 | n/a | class cannot occur (a wait of 0 is no wait) | OK (omitted: cannot occur) |
| readiness fallback | WC-1 (spec:59) | Typical | prompt falls back "well inside" 60 s | true | "well inside" is not a number; evidence says 30 s passes, above about 45 s fails | GAP (see M-4) |
| task confidence | task row (spec:121) | Legitimate Edge Case | confidence 0.70 to 0.89 | not below 0.70 | not stated for task; only below 0.70 resolves as blocked | GAP (see M-5) |
| nesting depth | R1, WC-8 (spec:33, 66) | Typical | depth 1 | worker may not start workers | forbidden | OK |
| `--unattended` token | D1 (spec:228), section 2.1 (spec:51) | Sentinel Value Match | quoted specification text containing the string `--unattended` | ambiguous | not specified: standalone token rule absent | GAP (see M-2) |
| `ask` timeout | WC-3 (spec:61) | Maximum/Overflow | timeout | pending | resume same message ID; no duplicate | OK |
| `check` after fencing | WC-12 (spec:70) | Legitimate Edge Case | `consumer_fenced` | true | stop, no `worker_done` | OK |

FR-8/FR-9 gate: three GAP rows name a concrete wrong outcome (B-1 rows); the rest are Medium. FR-10: table complete, every class either has a row or a one-line reason; synthesis proceeds.

Pipeline Dimensional Analysis (FR-17): not triggered. The spec has a phase plan, not a data flow whose stage output counts differ. `--focus correctness` is not active, so no State Variable Registry is produced.

## === REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL, blocking, High priority): the contract path is undefined for file-valued and absent output flags
Experts: Wiegers (lead), Adzic, Whittaker (Sentinel Collision, FR-2.3).
Texts that conflict:
- WC-4 says the default contract path is `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (spec:62), and the section 3 intro repeats "else `<output-dir>/return-contract.yaml`" (spec:76).
- The section 3.1 rows say `--output <file>` for tdd (spec:90, report "the TDD at `--output`") and init-lite (spec:87), and the inventory confirms the TDD output is a file path such as `docs/[domain]/TDD_[COMPONENT-NAME].md` (`INV-B:222`). cleanup-audit and index-repo take no output flag in the brief at all (spec:85-86, "none"; `INV-A:42`, `INV-A:53`).
Wrong outcome: an implementer who follows the stated text for tdd builds a contract at `docs/tdd/TDD_AUTH.md/return-contract.yaml` (impossible) or, by taking the parent directory, at `docs/tdd/return-contract.yaml`. Two tdd workers writing into the same `docs/tdd/` then overwrite one contract (breaks WC-11, spec:69). For cleanup-audit and index-repo the text names no directory, so the coordinator cannot "derive that path from the brief" (spec:62). It is wrong because acceptance check AC-2.2 (`/sc:tdd "auth" --unattended --output <file>`, spec:200) and 7.2 step 4 (`test -s <contract>`, spec:183) cannot be run: there is no contract path to test, and `worker_done --report-path` (WC-4) has nothing to carry.
Recommendation (Wiegers): state one rule for file-valued outputs, for example a sibling `<output-file>.return-contract.yaml`, and one named location for the commands with no output flag; add them to the section 3 rows for tdd, init-lite, spec-panel, recommend, explain, cleanup-audit and index-repo.
Quality impact: Completeness +2, Testability +2.

### B-2 (MAJOR, blocking, High): AC-1.1 and the P1 scope contradict the `load` row
Experts: Wiegers, Adzic.
Texts that conflict:
- AC-1.1 asserts that "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" (spec:195). P1 says the `--unattended` flag is "accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (spec:159). The section 3 intro says "Every changed command also gains the `## Unattended mode` section" (spec:76).
- The `load` row says report "none (see note)", resume "n/a", and "use it as a step inside another worker's brief, not as its own Task"; its P1 scope is "usage line only" (spec:112, 159; Decisions row spec:265, `INV-B:31,65`).
Wrong outcome: an implementer who follows the `load` row edits only the Usage line, and AC-1.1 then fails because `load.md` has no Unattended section naming `return-contract.yaml`. An implementer who follows AC-1.1 adds a contract-naming section to a command the spec says writes no contract, which also breaks the SA-4 additive-only limit (spec:149) and the Decisions row "a report file would be an unrequested addition" (spec:265). Both cannot hold, and the acceptance criterion cannot pass under the row as written.
Recommendation (Wiegers): exclude `load` from AC-1.1 and from the P1 flag list by name, or give it a one-line Unattended section that says it writes no contract.
Quality impact: Consistency +1, Testability +1.

### B-3 (MAJOR, blocking, High): P1 adds `--unattended` to gated, outward-acting commands before their gate conversion
Experts: Nygard, Whittaker (Sequence Attack, FR-2.4), Fowler.
Texts that conflict:
- P1 delivers "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (spec:159). Gate conversion is P2 (spec:160), drift fixes P3, and implement, post-release and pr-submit are P4 (spec:162). Section 2.3 tells the coordinator to put `--unattended` in every brief (spec:73); WC-2 and WC-9 define the flag as "no person-blocking step" and "any default that pushes, opens a PR, posts, installs ... is off" (spec:60, 67).
- auggie-review posts to the PR by default with no prompt (`cmd/auggie-review.md:51-54` via spec:67, `INV-A:98`); post-release has VM, real-target install, commit and PR steps (spec:113).
Wrong outcome: after P1 an implementer has built a flag that auggie-review, cleanup, task, post-release and pr-submit accept but ignore until P2 or P4. A coordinator that follows 2.3 passes `--unattended` believing WC-9 holds, and auggie-review posts to the PR and ends its turn on the chat offer (`INV-A:62`). It is wrong because the flag's stated meaning (WC-2, WC-9) is not true for those commands, and the phase text says the flag is accepted while "each phase is independently useful" (spec:154). The result is an outward action under a flag that promises none, which is a safety-boundary risk.
Recommendation (Nygard): in P1 accept the flag only for commands whose gate and outward-default resolutions ship in the same phase; before that phase the command should refuse `--unattended` (fail closed). State this in the P1 and P2 rows.
Quality impact: Completeness +1, safety of the rollout +3.

## === ARCHITECTURE ANALYSIS ===

Verified positives (Fowler, Newman, Hohpe): the decision (section 1.1) is consistent with the evidence it cites. The nesting-depth refusal (`CAPS:97-103`), the dispatched-pane rule for `worker_done` (`CAPS:76,150`), the "do not emit lifecycle messages without a preamble" rule (`CAPS:148`) and the circuit-breaker note (`CAPS:80`) all say what the spec says. The boundary between coordinator and commands (a flag, a report file, resume) is narrow and one-directional. Section 1.4 states its three evidence gaps honestly, and section 4 follows the inventories' coordinator-only split (`INV-A:90`, `INV-B:285-287`).

No architecture-only blocking finding. Architecture issues that are Medium are listed below (M-1, M-6, M-7).

## Follow-up candidates (Medium and minor; none triggers a revision)

### Medium

- **M-1 (Nygard, Whittaker; MAJOR label, Medium grade): retry and stale-contract handling is split across two owners.** WC-6 makes the command write "each run into a fresh output directory" (spec:64), but WC-4 fixes the contract at the directory the coordinator passed and derives the path before dispatch (spec:62), and section 2.3 does not require a new directory per attempt (spec:73). A `worker-start --retry-of` that reuses `--output` overwrites or mixes with the first attempt, and 7.2 step 4 (`test -s`, spec:183) accepts a stale first-attempt contract if the retry dies before writing. The spec never states who supplies the fresh directory or how freshness is checked. Needs a guess about which owner is meant, so Medium. Suggest: coordinator passes a distinct directory per attempt; check the contract's mtime or add a `run_id` field.
- **M-2 (Whittaker, FR-2.3 Sentinel Collision; Medium): the `--unattended` token has no parsing rule.** D1 (spec:228) and section 2.1 (spec:51) say a flag in the brief selects the mode but not that it counts only as a standalone argument token outside quoted content. A topic such as `/sc:tdd "document the --unattended flag"` can switch the mode on. The spec recommends testing by grep (spec:228), which cannot tell the two cases apart. Medium: the harm needs a user input containing the string.
- **M-3 (Wiegers; Medium): status vocabulary collision.** WC-4 says commands that already write a contract "keep their fields and add the missing ones" (spec:62) and the Decisions row fixes `status` to four values (spec:262). The inventories show existing contracts with their own `status` (workflow, contract 1.1, `INV-B:272`) and do not give their value sets. If an existing set differs, the YAML assertion in 7.2 step 4 (spec:183) fails for a correct existing contract. Needs a guess about the existing values.
- **M-4 (Wiegers; Medium): WC-1 has no number.** "Well inside the readiness limit (default 60 s)" (spec:59) is untestable. The cited evidence gives 30 s passing and about 45 s failing (`EVIDENCE.md:45,56`, UNVERIFIED here; `CAPS:49`). State a maximum such as 30 s.
- **M-5 (Adzic; Medium): task confidence band 0.70 to 0.89.** The task row resolves only "below 0.70" as blocked (spec:121); `INV-A:36` shows the same threshold family has a 0.70-0.89 "present alternatives, ask questions" band for agent. Whether task asks in that band is not stated, so a worker could still stall. Add the band to the row or state that it proceeds.
- **M-6 (Fowler, Cockburn; Medium): phase gating understates the user decisions.** Section 6 says "Phases 1-3 need no user decision" (spec:154) and section 9 says "Phases 0-3 can proceed on the recommendations" (spec:225), yet D4 lists auggie-review `--post-pr` and task `commit`/`push` as affected (spec:244), and both rows are P2 (spec:100, 121, 160). If the user picks D4 (b) "Never", the P2 rows that let a brief re-enable posting are wrong. State that P2's outward-action re-enable clauses wait for D4.
- **M-7 (Hohpe, Newman; Medium): section 2.3 requires `--unattended` in every brief, but P0 commands do not accept it yet.** 7.2 step 1 builds the brief "per section 2.3" (spec:180), and AC-0.4 runs the three smoke commands without the flag (spec:194, 3.1 "brief must pass" column spec:81-92) because the flag arrives in P1. Say that P0 briefs omit the flag. Also, AC-0.4 step 4 "uses the command's existing report file", but the 7.2 YAML assertion expects the four-value `status`, so the step 4 check cannot be applied as written to adversarial (`INV-A:60`: no fixed contract filename).
- **M-8 (Newman; Medium): P1 puts gate resolutions into the "no gate" phase.** P1 is described as "No person gate is involved" (spec:159), but its rows include business-panel (`--mode socratic` refused), explain (`--format interactive` refused), index and test (`--watch` refused) (spec:102, 108, 111, 123). Harmless to order, but the phase rationale and the AC-1.2 live check (all steps pass) do not cover a refusal path. Add one refusal-path check to AC-1.2.
- **M-9 (Nygard; Medium): `AC-C5` and `SA-4` conflict on Usage lines.** SA-4 says edits are additive (spec:149) and AC-C5 requires `grep -E '^-[^-]'` to print nothing (spec:176). Adding `--unattended` to an existing Usage code line is a removed-line diff. State that the flag goes on a new line, or allow Usage-line edits in AC-C5.
- **M-10 (Hohpe; Medium): AC-C1 may reject its own P0 deliverable.** P0 adds an Orca section to `HOW-WE-WORK.md` and a brief template to `WORKER-CONTRACT.md`, both under `src/superclaude/core` (spec:158). AC-C1 greps `core` for `orca(-ide) orchestration|worktree|terminal|agent` and expects no hits (spec:172). SA-2 allows an Orca mention "as an example ... inside the contract file" (spec:147). Whether the HOW-WE-WORK section may contain such command text is not stated. Narrow AC-C1's path list or exempt those two files.
- **M-11 (Adzic; Medium): evidence citation E2 points at the wrong line.** Spec:22 cites `CAPS:161` for "`[H:worker-start]` line 38, `--agent claude`"; `CAPS:161` is the pr-submit top-level rule, and the inventory does not quote `[H:worker-start]` line 38 anywhere I could find (`CAPS:49` quotes only the `EVIDENCE.md:39` text). The claim itself is plausible; the citation does not support it.

### Minor notes (never fail the review)

- N-1: the spec uses an undefined tag "(F1)" at spec:62, 76, 182, 196, 198 and in the 7.2 pass conditions; no findings file defining F1 is in the workspace (`review/spec-panel.md` is absent). A reader of the final spec cannot resolve it.
- N-2: E3 cites `invocation_method: "skill-direct"` as support (spec:23), while section 1.4 (1) says the PR #329 run proves only the nested route (spec:43). `INV-A:35` calls it "proven as a direct Orca-worker skill call". The spec should say which reading it takes; section 1.4 is the safer one.
- N-3: section 3 labels 10 commands "ready today" yet 4 of them (reflect, release-split, tdd, troubleshoot) get P2 gate changes; consider "ready with stated inputs".
- N-4: Decisions row for `partial` (spec:263) states the circuit-breaker point with `CAPS:80` correctly (verified), but the row for WC-5 does not say that a `blocked` outcome sent as `failed` makes dependents wait for a `--retry-of` (`CAPS:116`, `CAPS:80`); say how a blocked worker is resumed after the answer arrives (WC-3 covers only the live-session path).
- N-5: the UNVERIFIED list item 14 reports a prior citation check by an agent; I could not reproduce it and did not rely on it.

## Citations checked (verified against workspace files)

- Counts and splits: `INV-A:3`, `INV-B:3`, `INV-B:289` (14 needs-change in B) match the spec's per-group totals.
- `CAPS:44-45,49,52` (readiness, `EVIDENCE.md:39` quotation), `CAPS:58-68` (ask), `CAPS:72-80` (`worker_done`), `CAPS:97-103` (depth), `CAPS:107-116`, `CAPS:115` (placement quotation), `CAPS:129-130`, `CAPS:145-151`, `CAPS:155-162`: content matches the spec's use.
- `INV-A:35,36,49,50,60,61,62,65,66,90,95,96,97,98,106`, `INV-B:31,65,105,112,222-225,272,285-287,292,294,296,299,301,311,320,323`: content matches the spec's use.
- `README.md:6,11-17,30,31`: match.

## UNVERIFIED (could not be checked in this sandbox)

`EVIDENCE.md:35,39,45,56`; every `cmd/*`, `sk/*` and `src/superclaude/cli/install_core.py` line; `CLAUDE.md:16,50,72-83,157,334,408`; `Makefile:68-74`; `pyproject.toml:38`; `src/superclaude/core/HOW-WE-WORK.md` lines; the E5 grep results; the `grep` and `diff` commands in section 7 (not run).

## Hook and brief handling

- Brief clauses overridden: none. The brief did not widen scope.
- The user was not asked about opening an issue for the follow-up candidates: this is a non-interactive sandbox run. No issue was created; the list above is only recorded.

## Reviser brief

Revise only the blocking findings B-1, B-2, B-3. Rules (restated from the command's Review Loop bullet 6, because the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing text to adding.
- Report the byte size of the file before and after, with the bytes added and deleted per finding id.
- Leave Medium and minor findings alone, and do not award yourself a PASS.

Findings:
- B-1: WC-4 and the section 3 intro define the contract path as `<output-dir>/return-contract.yaml`, but tdd and init-lite pass a file in `--output`, and cleanup-audit and index-repo pass no output at all. Fix the rule for those rows only.
- B-2: AC-1.1 and the P1 flag list require an Unattended section naming `return-contract.yaml` for every command in 3.1-3.2, but the `load` row writes no contract. Reconcile `load` with AC-1.1 and the P1 list.
- B-3: P1 accepts `--unattended` on commands whose gate and outward-default resolutions arrive in P2 or P4. Make the flag fail closed, or ship it with its resolutions, for those commands only.

verdict: FAIL
