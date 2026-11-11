review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Kind: labelled whole-document audit of the final spec, a first review of the whole document (FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `84aa3fdce83498845e1a3cf58e05e4b1f83a15e38b34520e6f0393658bd74d26`
- Baseline: not given (first review); `baseline: missing` not applicable because no `--re-review` was requested.
- Reviewer model actually used: claude-sonnet-5-5
- Panel (fixed order, requirements and architecture focus): Wiegers (lead), Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe. Crispin, Gregory and Hightower were not seated because `testing` and `compliance` are not in `--focus`; Crispin validated the boundary table only.
- Evidence rule: only `inventory/commands-a.md` (INV-A), `inventory/commands-b.md` (INV-B) and `inventory/orca-capabilities.md` (CAPS) are checkable here. A citation into `src/`, `~/.claude`, `CLAUDE.md`, `EVIDENCE.md`, `pyproject.toml`, the codegraph README or an Orca guide that is not quoted in CAPS is marked UNVERIFIED.

## Coverage statement

Covered: all 285 lines. Read the whole spec and the README. Cross-checked against the inventories: the 10 / 27 / 6 split (recounted from `spec:81-92`, `spec:97-125`, `spec:132-137` and from INV-A:3 / INV-B:3 / INV-B:289: 5+3+13 in A, 5+3+14 in B, so 10 ready, 6 coordinator-only, 27 change, total 43 holds); the phase assignment of all 27 rows (P1 = 9, P2 = 11 + 4 ready commands = 15, P3 = 4, P4 = 3, which matches `spec:159-162` and the "nine plus six" in AC-2.2 at `spec:200`); roughly 35 INV-A / INV-B line citations and roughly 30 CAPS line citations. Every INV and CAPS line sampled says what the spec attributes to it. Not covered: the roughly 340 citations into `cmd/`, `sk/`, `EVIDENCE.md`, `CLAUDE.md`, `install_core.py`, `pyproject.toml` and `HOW-WE-WORK.md`; these are UNVERIFIED here (the spec's own claim of an independent re-check, `spec:285`, is self-attestation and is not counted as evidence).

## Summary

The decision (Orca coordinates, commands stay units of work, section 1) is well argued and its counter-design is rejected on evidence that checks against CAPS (`CAPS:97-103`, `CAPS:145-150`). Section 1.4 states the evidence gaps plainly. The count arithmetic is consistent. Two stated texts cannot be built or passed as written (F1, F2). Eleven Medium and several minor items are listed under follow-up candidates.

## Findings

Finding ids are stable for re-review. Severity is by consequence (review loop bullet 2).

=== REQUIREMENTS ANALYSIS ===

### F1 (blocking, MAJOR, High) Wiegers, Adzic: the P0 acceptance check cannot pass as written

Grading sentence: An implementer who follows the stated text as written builds a P0 smoke run in which `/sc:troubleshoot` writes only `REPORT.md`, and then AC-0.4 requires step 3 of the live check to pass, which demands "its `--outcome` matches the contract's `status` under WC-5" and "its report path is the WC-4 contract path"; that cannot pass, because no contract exists until P1 and the spec says so itself.

- Step 3 pass condition: `spec:182`. AC-0.4 says "steps 1-3 and 5-7 pass; step 4 is `test -s` on the command's existing report file ... no contract exists until P1": `spec:194`.
- WC-5 on the same text: the outcome is `succeeded` only "when the contract parses"; "no report, an empty or unparseable contract" is `--outcome failed` (`spec:63`). With no contract in P0, WC-5 as written makes a successful troubleshoot run end `failed`, while AC-0.4 step 3 asks the outcome to match a status that does not exist.
- The report path for troubleshoot is `REPORT.md` (`spec:91`, INV-B:49), not `return-contract.yaml`; adversarial's contract is at an unfixed path until P1 (`spec:83`, INV-A:60); workflow's is at `.dev/tasks/to-do/<id>/` (`spec:92`, INV-B:272), which is not the WC-4 `<output-dir>` path (`spec:62`).
- Why it matters: P0 is the gate that "reopens section 1" on failure (`spec:194`), and the spec says later phases do not start until the checks pass (`spec:154`). A check that cannot pass, or a worker obeying WC-5 and reporting `failed` for a good run, blocks or corrupts the one live test of the whole decision.
- Recommendation: in AC-0.4 restate step 3 for P0 only: exactly one `worker_done`, outcome judged against the existing report file (non-empty and, for workflow, the existing contract), report path equal to that file; and say in WC-5 or section 2.3 that before P1 the "no contract" clause does not apply to the ready commands. Narrow, no new mechanism.

### F2 (blocking, MAJOR, High) Nygard, Whittaker: P1 gives gated commands an accepted-but-inert `--unattended`, and section 2.3 tells the coordinator to pass it from P1 on

Grading sentence: An implementer who follows P1 as written adds `--unattended` to every command in sections 3.1 and 3.2 "a no-op where a command has no gate" while the gate conversions arrive only in P2 to P4, and a coordinator who follows section 2.3 passes `--unattended` "from P1 on"; the worker therefore runs, for example, `/sc:auggie-review <PR> --unattended` with PR posting still on by default, which is wrong because WC-9 says that default must be off under `--unattended`.

- P1 scope: `spec:159` ("the `--unattended` flag accepted by every command in sections 3.1 and 3.2"). Gate resolutions for gated commands: auggie-review, cleanup, improve, task, tdd, troubleshoot and others are P2 (`spec:160`), implement, post-release, pr-submit are P4 (`spec:162`).
- Coordinator duty: `spec:73` ("the exact command line including `--unattended` (from P1 on ...)").
- The behaviour that must be off: `spec:67` (WC-9), `spec:100` (auggie-review row; `cmd/auggie-review.md:51-54` posts by default, UNVERIFIED here). The spec's own rule that "the flag means a person is absent" (`spec:51`, `spec:60`) is violated by an inert flag: the worker would stall on `AskUserQuestion` (task confidence, tdd bare topic) or perform an outward default.
- AC-1.1 requires the `## Unattended mode` section on every command in sections 3.1 and 3.2 at P1 (`spec:195`) and AC-1.2 live-tests only the P1 commands (`spec:196`), so nothing detects the inert flag.
- Sequence attack (FR-2.4): P1 passes; P2 not yet started; coordinator dispatches a P2 command with the flag. State trace: before = PR has N reviews; after = N+1, posted by a "no person, no outward action" worker.
- Recommendation (delete or narrow): in P1 add `--unattended` only to commands with no gate, and until a command's own phase lands let it stop with `status: blocked` ("gate conversion not yet shipped") when `--unattended` is passed; or state in section 2.3 that a coordinator passes `--unattended` only to commands whose phase has passed. One of the two sentences, not both.

=== ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The layering (coordinator above, worker top-level session, command with no Orca call, `spec:16`, `spec:213`) is consistent with CAPS (`CAPS:97-103`, `CAPS:147-150`, `CAPS:155-161`), and the rejected-alternative table (R1-R5, `spec:31-37`) holds against CAPS. Medium items follow.

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium (warnings; each needs the implementer to pick a reading or concerns a requirement the spec never states):

- **M1 Wiegers/Nygard: `/sc:pr-submit` has a documented "Will Not: run headless" boundary the spec never mentions.** INV-B:90 quotes `cmd/pr-submit.md:85` and `SKILL.md:225`. The pr-submit row (`spec:114`) and D3(b) (`spec:241`) design a worker mode without reconciling it. Under D3(a) (recommended) nothing is built, but section 3.2 still counts pr-submit among the 27 and P1 gives it the `--unattended` section (see M2).
- **M2 Cockburn/Fowler: pr-submit is simultaneously a change target and "coordinator only if D3(a)".** AC-1.1 (`spec:195`) and P1 (`spec:159`) require its `## Unattended mode` section; D3(a) says "no pr-submit changes in Phase 4" (`spec:240`); `spec:139` says it is a worker candidate only if D3 is accepted. The 27 / 10 / 6 totals (`spec:76`) assume D3(b).
- **M3 Wiegers: contract location for file-valued `--output` is ambiguous.** WC-4 defines `<output-dir>` as the directory passed (`spec:62`) and lists init-lite and tdd under "the file `--output` names". Section 3.1 gives the same file as the deliverable (`spec:87`, `spec:90`). A reader can build the contract at the deliverable path (overwrite), beside it, or in a directory. Same for spec-panel, whose row says only "add `--output`" (`spec:120`; INV-B:182 says no `--output` exists), and for analyze, build, design and similar rows. State "beside the file, as `<file-dir>/return-contract.yaml`" or "in `--report-dir`" once.
- **M4 Nygard/Whittaker: WC-11 says two workers in one worktree "must never write the same file" (`spec:69`), but three ready commands write fixed paths.** cleanup-audit `.claude-audit/` (`spec:85`, noted as one audit at a time), index-repo `PROJECT_INDEX.md` (`spec:86`, INV-A:53), init-lite default `.dev/superclaude/context-audit.md` (`spec:87`, INV-A:55). Only cleanup-audit carries the serialization note; section 2.3 (`spec:73`) lists no "never run two of these at once" duty for the coordinator.
- **M5 Newman/Hohpe: tasklist row contradicts the inventory it cites and hides an UNVERIFIED.** The row says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (`spec:122`). INV-B:215 says the fan-out "must run at the worker's top level, not inside subagents" and INV-B:210 marks nested spawning UNVERIFIED; the spec does not carry that UNVERIFIED into its list (`spec:271-285`). Passing `--unattended` to each reflect also turns on headless auto-accept of `--remediate`, which then runs a hand-off inside those subagents.
- **M6 Adzic: AC-2.2 expects `blocked` + `failed` for nine commands (`spec:200`), but WC-3 lets a worker holding a preamble `ask` the coordinator instead (`spec:61`).** A conforming worker that asks, gets an answer and finishes `succeeded` fails the check; the check does not say the brief must withhold `ask` for it.
- **M7 Whittaker: behaviour of a section-4 command given `--unattended` is undefined.** Section 4 says they "get no `--unattended` mode" (`spec:128`); nothing says refuse or ignore. Zero/degenerate case: `/sc:git commit ... --unattended` from a worker.
- **M8 Crispin/Nygard: AC-C1 is narrower than SA-2 and its own scope contradicts SA-2/P0.** The grep covers `src/superclaude/core` (`spec:172`) while SA-2 permits a caller-channel mention in the contract file (`spec:147`) and P0 adds an Orca section to `HOW-WE-WORK.md` (`spec:158`, `spec:150`). The regex is case-sensitive and lists four sub-commands, yet the spec itself writes the placeholder `ORCA orchestration` (`spec:167`, `spec:180`); `orca-cli`, `orca status` and `ORCA ...` text pass unnoticed. The raw cell also carries markdown `\|` escapes.
- **M9 Wiegers: WC-1 has no number.** "Well inside the readiness limit" (`spec:59`); the evidence it cites is 30 s passing and "above about 45 s fails again" under a 45 s limit (CAPS:49 quotes `EVIDENCE.md:39,45`; the `:56` figure is UNVERIFIED here). No acceptance check in section 7 covers WC-1.
- **M10 Nygard: WC-10 / AC-4.3 set a hard 240 s per tool call for pr-submit (`spec:68`, `spec:210`) while the poll-script runtime is UNVERIFIED (`spec:283`).** The check may be unachievable with the existing scripts; the row (`spec:114`) already says "confirm".
- **M11 Fowler: cli-eval wait splitting rewrites existing eval-timeout text (`spec:104`) but SA-4's list of permitted existing-line changes omits it (`spec:149`); AC-C5 only inspects command files (`spec:176`) while most edits land in skills.** INV-A:65 says the worker only "must keep sending heartbeats", via the Monitor tool, which is not a single blocking call.

Minor notes:

- n1: E2 (`spec:22`) cites `EVIDENCE.md:45` (answered after `input_accepted`) for "same tools as a person"; that line proves readiness, not tool parity.
- n2: E3 (`spec:23`) lists PR #329 as support while section 1.4(1) (`spec:43`) says the same run proves only the nested route; read together they are honest, read alone E3 overstates (INV-A:35 itself says "proven as a direct Orca-worker skill call").
- n3: Contract status `blocked` (`spec:62`) collides in name with Orca's Task status `blocked` (CAPS:89), though it maps to Orca `failed`; a one-line note would avoid coordinator confusion.
- n4: `partial` maps to `succeeded` (`spec:63`, `spec:263`); the spec admits the body then carries the truth. A coordinator that keys only on Orca outcome loses it.
- n5: AC-C5 `grep -E '^-[^-]'` (`spec:176`) misses deleted blank lines and deleted lines beginning `--`/`---` (frontmatter).
- n6: P1 counts `load` among commands that accept the flag (`spec:159`) but AC-1.1 exempts it (`spec:195`).
- n7: The task row blocks only at confidence below 0.70 (`spec:121`); the 0.70 to 0.89 band is not addressed (the inventory records only the `<0.70` rule, INV-B:199).
- n8: UNVERIFIED #14 (`spec:285`) is self-attestation of a citation check; it is not evidence for this review.
- n9: Dual-surface rule for the contract file path (installed `~/.claude/WORKER-CONTRACT.md` only, `spec:52`) cannot be checked against `CLAUDE.md` here: UNVERIFIED.

## Guard Condition Boundary Table (spec contains thresholds and guards)

Leaders: Nygard (build), Crispin (completeness), Whittaker (attack). Classes left out are given a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| contract `status` mapping | WC-5 `spec:63` | Zero/Empty | no file, empty file | no match | `--outcome failed` | OK |
| contract `status` mapping | WC-5 `spec:63` | Sentinel Value Match | value outside the four | no match | `--outcome failed` | OK |
| contract `status` mapping | WC-5 `spec:63` | Legitimate Edge Case | `partial` | match | `--outcome succeeded` | OK |
| contract `status` mapping | WC-5 + AC-0.4 `spec:63,194` | Typical in P0 | no contract exists | n/a | WC-5 says `failed`, AC-0.4 says match the contract | GAP (see F1) |
| `--unattended` gate | WC-2 `spec:60` + P1 `spec:159` | Typical | gated command, flag passed, phase not shipped | not defined | flag accepted, gate still active | GAP (see F2) |
| heartbeat wait size | WC-10 `spec:68` | Maximum/Overflow | single call over 4 min | true | split into waits of at most 4 min | OK |
| heartbeat wait size | WC-10 `spec:68`, `spec:114` | Legitimate Edge Case | pr-submit poll runtime | unknown | "confirm" (runtime UNVERIFIED, `spec:283`) | GAP (Medium, M10) |
| readiness fallback | WC-1 `spec:59` | Typical | prompt fallback of 30 s | pass (CAPS:49) | "well inside" 60 s, no number | GAP (Medium, M9) |
| nesting depth | WC-8 `spec:66` | Maximum/Overflow | worker calls `worker-start` | refused (depth 1, CAPS:97-99) | forbidden | OK |
| nesting depth | WC-8 `spec:66` | Legitimate Edge Case | worker calls `task-create` | unknown | forbidden anyway (CAPS:103) | OK |
| task confidence | task row `spec:121` | Typical | below 0.70 | true | blocked | OK |
| task confidence | task row `spec:121` | Legitimate Edge Case | 0.70 to 0.89 | not stated | not specified | GAP (minor, n7) |
| `--unattended` on coordinator-only command | section 4 `spec:128` | Legitimate Edge Case | `/sc:git ... --unattended` | not stated | not specified | GAP (Medium, M7) |
| one report path per worker | WC-11 `spec:69` | Typical | two workers, fixed-path command | collision | cleanup-audit only noted | GAP (Medium, M4) |

Left out: "One/Minimal" for all guards (no count-based guard has a distinct minimal behaviour in the text).

## Pipeline Dimensional Analysis and Quantity Flow Diagram (FR-17 to FR-21)

Trigger: the spec describes a multi-stage inventory-to-phase flow where counts change.

```text
[Source: 43 commands in cmd/ (INV-A:3 21 + INV-B:3 22)]
   --> [Triage] --> 10 ready (5 A + 5 B) | 27 change (13 A + 14 B) | 6 coordinator-only (3 A + 3 B)
   --> [Phasing of the 37 workers]
         P0: 0 command edits (3 smoke runs of ready commands)
         P1: 9 change + 4 ready-fixes (adversarial, cleanup-audit, index-repo, workflow)
         P2: 11 change + 4 ready (reflect, release-split, tdd, troubleshoot) = 15
         P3: 4 change
         P4: 3 change              9 + 11 + 4 + 3 = 27   OK
   --> [Consumer: AC-1.1 asserts a section on all 37 minus load = 36]   <-- phase mismatch with F2 / M2
   --> [Consumer: AC-2.2 splits P2's 15 as 9 blocked-path + 6 default-path]   OK
```

No count mismatch (CRITICAL under FR-19) found: 43, 37, 27, 15 and 9 + 6 all reconcile. The one dimensional inconsistency is AC-1.1's all-36 assertion at P1 against the per-phase delivery of gate behaviour (F2) and pr-submit's conditional status (M2).

## Whittaker adversarial notes (FR-3 format, folded into the findings above)

- I can break this specification by **Sequence Attack**. The invariant at **P1 / section 2.3 (`spec:159`, `spec:73`)** fails when **a coordinator passes `--unattended` to a P2-P4 command before its phase**. Concrete attack: auggie-review run with the flag in the P1 to P2 window; before: PR with N reviews; after: N+1 (F2).
- I can break this specification by **Zero/Empty Attack**. The invariant at **AC-0.4 step 3 (`spec:182`, `spec:194`)** fails when **the contract file does not exist**. Concrete attack: troubleshoot succeeds, writes `REPORT.md` only; WC-5 forces `failed`, step 3 expects a match (F1).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 status vocabulary (`spec:62`)** fails when **the contract value `blocked` meets Orca's own Task status `blocked` (CAPS:89)**; mapping to `failed` is stated, but the shared word is a coordinator trap (n3).
- Accumulation and Divergence attacks found no further specification-level breaks beyond M4 and M6.

## Reviser brief

Blocking finding ids: F1, F2. Revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
