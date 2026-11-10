review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (/sc:spec-panel, critique, focus requirements,architecture)

Short names: `S:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `CAPS:N`, `INV-A:N`, `INV-B:N` = line N of the files under `.dev/orca-command-refactor/inventory/`. These are the only checkable evidence in this sandbox. Any `src/...`, `CLAUDE.md`, `.dev/evals/...` or `.dev/codegraph-migration/...` citation is UNVERIFIED: none of those paths exist in the workspace (it holds only `.dev/orca-command-refactor/`). A claim resting only on such a citation is carried as the spec's own claim, not confirmed here.

## Header
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `060d1fb59804955f83e92638dceec3c2655f94b7c59c399f7112f8a8c9bfd1d2`
- baseline: not given (first review of the whole document; no `--re-review`, no `--baseline`)
- reviewer model used: claude-sonnet-5-5
- mode: critique; focus: requirements, architecture; brief precedence: nothing in the brief was overridden
- coverage: whole document (`S:1-285`), the README, and the three inventories (read in full for `CAPS` and `INV-A`; `INV-B:1-60` and `INV-B:280-323` read, the middle per-command notes were not re-read). Cross-checked the 43-command split, the phase membership lists, the acceptance checks against the section 3 rows, and the `CAPS:` line numbers the spec cites.

## What I checked and found sound
- Command counts: 21 + 22 = 43 (`S:76`, `INV-A:3`, `INV-B:3`). Section 3.1 has 10 rows (`S:83-92`), section 3.2 has 27 rows (`S:99-125`), section 4 has 6 (`S:132-137`). The P1/P2/P3/P4 membership in `S:159-162` matches the Phase column of section 3 (9 + 15 + 4 + 3, plus the 4 section 3.1 P1 fixes, plus brainstorm and init-lite with no phase = 37).
- The 10/27/6 split matches the inventories (`INV-A:73`, `INV-B:280-297`).
- Every `CAPS:` line reference I spot-checked lands on the quoted fact (for example `CAPS:92`, `CAPS:97-101`, `CAPS:145-151`, `CAPS:155-161`, `CAPS:176-188`).
- The unverified items in `S:271-285` are honest and match `CAPS:174-188`.

## === REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn)

### B-1 (CRITICAL, blocking): cli-portify cannot reach `succeeded` in unattended mode
- Location: `S:105` (cli-portify row), `S:61` (WC-3), `S:60` (WC-2), `S:201` (AC-2.3), `S:200` (AC-2.2).
- Grading sentence: an implementer who follows the stated text as written builds a cli-portify unattended mode in which each of its three approval gates "resolves as blocked" (`S:105`), and the only unblock route is "re-invoke or resume the command with the answer as a flag" (`S:61`). The row defines no flag that carries an approval; the only new flag is `--resume <contract>`, which restarts at `resume_phase`/`resume_substep` (`S:105`), and that resumed run reaches the same gate and blocks again. The built command can never pass its first approval gate, and AC-2.3 ("Happy-path run per P2 command with every required flag in the brief" ends `--outcome succeeded`, `S:201`) cannot pass for it. The gate list itself is evidenced at `INV-A:45`, `INV-A:79`.
- Expert: Wiegers (testability: no acceptance path), Adzic (no concrete example of an approved run), Cockburn (the primary actor's goal, a completed port, is unreachable).
- Recommendation: either name an approval flag (WC-2 route (b)) per gate, or move cli-portify to section 4 or to a documented "approvals given by a person only" row, and remove it from the AC-2.3 set.
- Priority: High. Quality impact: removes one unreachable acceptance path.
- Origin: first review, whole document.

## === ARCHITECTURE ANALYSIS === (Fowler lead, Newman, Hohpe, Nygard)
No blocking architecture finding. The decision itself (Orca on top, commands as units) is well argued and its weak points are disclosed at `S:41-45`; the rejected alternative has checkable reasons (`S:31-37`, `CAPS:97-103`, `CAPS:145-150`). The architecture findings below are Medium.

## Guard Condition Boundary Table (Nygard construct, Crispin completeness, Whittaker attack)
Guards in the spec: unattended switch, readiness limit, wait-split rule, depth fence, report-file rule. Input classes the guard cannot meet are left out with one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` token present | `S:51`, `S:60` | Zero/Empty (flag absent) | no flag | false | today's behaviour unchanged (SA-1, `S:146`) | OK |
| `--unattended` token present | `S:51`, `S:159` | Legitimate Edge Case (command not yet converted: dispatched in P1 while its gate lands in P2) | `auggie-review --unattended` in P1 | true | `S:159` says the flag is "a no-op where a command has no gate"; for a command WITH a gate before its phase, nothing is stated | GAP (see M-2) |
| report-directory flag in brief | `S:62` | Zero/Empty (flag omitted) | none | true | refused before any work, writes nothing; WC-5 maps to `failed` | OK |
| report-directory flag in brief | `S:62`, `S:88` | Legitimate Edge Case (inner invocation with no brief, tasklist Stage 10.5 calls reflect with only `--unattended`) | `reflect --unattended` | true | `S:122` passes only `--unattended`; WC-4 refuses a run with no output flag | GAP (see M-3) |
| report-directory flag in brief | `S:62` | Legitimate Edge Case (directory already holds an earlier run's `return-contract.yaml`) | non-empty dir | n/a | "fresh dir" per row; no rule that the dir must be empty | GAP (see M-6) |
| approval gate resolves blocked | `S:60-61`, `S:105` | Sentinel Value Match (gate with no unblock flag) | cli-portify gates | true | no flag | GAP (B-1) |
| approval gate resolves blocked | `S:60`, `S:121` | Typical | task confidence 0.69 | true | blocked, contract, stop | OK |
| `ask` allowed when blocked | `S:61` | Legitimate Edge Case (gate-trigger acceptance test) | worker holds preamble | true | worker "may" ask (`S:61`) while AC-2.2 expects `failed`+`blocked` (`S:200`) | GAP (see M-5) |
| wait-size rule | `S:68` | Maximum/Overflow (blocking call over 5 min) | 3600 s eval | true | split into waits of at most 4 min | OK |
| wait-size rule | `S:68`, `S:114` | One/Minimal (poll plus sleep iteration) | pr-submit iteration | unknown | poll-script runtime UNVERIFIED (`S:283`) | GAP (UNVERIFIED, noted, not a defect of the spec) |
| nested-worker depth | `S:66`, `CAPS:97-98` | Typical (depth 1) | 1 | true | `worker-start` from a command refused, so WC-8 forbids it | OK |
| nested-worker depth | `S:66` | Legitimate Edge Case (depth raised, D5) | 2 | false | D5 (a) keeps 1 | OK |
| `partial` outcome | `S:63` | Legitimate Edge Case | `status: partial` | n/a | maps to `succeeded`, body states `partial` | OK |
| `load` has no contract | `S:112`, `S:195` | Zero/Empty (no report) | none | n/a | AC-1.1 excludes `load`; WC-5 "no report exists" maps `failed` | GAP (see M-7) |
Input classes left out: Maximum for the depth fence (the fence is a fixed integer), Sentinel Match for the report flag (no reserved value).

## Pipeline Dimensional Analysis
Not triggered: the document has no data pipeline whose stage output count differs from input count; the only count conservation (43 = 10 + 27 + 6, phase counts 37) was verified above and holds.

## Adversarial analysis (Whittaker; Sequence, Sentinel Collision, Divergence, Accumulation)
- Sequence attack. The spec asserts `--unattended` is in every brief "from P1 on" (`S:73`) while a command's gate conversion lands in P2-P4 (`S:97-125`). Concrete attack: in P1 the coordinator dispatches `/sc:auggie-review <PR> --unattended`; P1 only "accepts" the flag (`S:159`); posting stays on until P2 (`S:100`, `S:160`). Result: a PR review is posted to GitHub in a run the coordinator believes is unattended, against WC-9 (`S:67`). Graded Medium (M-2): the text allows the better reading that a command is dispatched only after its phase, but never says so.
- Sentinel Collision attack. The fixed name `return-contract.yaml` is also the name reflect, brainstorm and workflow already write (`S:261`, `S:84`, `S:88`, `S:92`). When one command runs another inside the same `--output` directory (tasklist Stage 10.5 calls reflect, `S:122`), the inner contract can overwrite the outer one. The spec states a per-directory rule only for coordinator-level Tasks (`S:73`). Medium (M-3).
- Divergence attack. `S:139` says pr-submit "stays a worker candidate only if the user accepts D3", while section 3.2 counts it among the 27 commands that change (`S:114`, `S:76`) and AC-1.1 requires it to carry the unattended section after P1 (`S:195`). Under D3 (a) ("no pr-submit changes in Phase 4", `S:240`) the stated texts diverge on whether pr-submit is edited at all. Medium (M-4): needs a guess about which text wins.
- Accumulation attack. None found beyond M-6.

## Follow-up candidates (Medium and minor; none blocks)
- M-1 (Medium, was labelled MAJOR-class): tasklist row states "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit" as fact (`S:122`), but `INV-B:46` marks the nesting of reflect inside Stage 10.5 subagents UNVERIFIED and reflect itself fans out (reviewers, adversarial, validator, `INV-B:36`). The claim is stated without a trace of layers. Recommend: mark UNVERIFIED and add it to `S:271-285`.
- M-2 (Medium): P1 says `--unattended` is accepted by every command, a "no-op where a command has no gate" (`S:159`); `S:73` puts `--unattended` in every brief from P1. Nothing says a command may be dispatched only after its own phase lands. See Sequence attack above.
- M-3 (Medium): tasklist Stage 10.5 passes only `--unattended` to each reflect (`S:122`); WC-4 refuses a run whose brief omits the output flag (`S:62`); and the reflect row replaces its timestamped default with `--output` (`S:88`). Whether an inner call carries a directory, and which, is unstated; two reflects could also share one directory with tasklist's own contract.
- M-4 (Medium): D3 (a) versus AC-1.1 and section 3.2 for pr-submit; the same pattern for implement (D2) and post-release (D4): `S:154` says Phases 1-3 need no user decision, yet AC-1.1 (`S:195`) asks P1 to place an `## Unattended mode` section, whose content is "its own gate resolutions" (`S:52`), in commands whose resolutions are decided only at P4.
- M-5 (Medium): WC-3 lets the worker "ask the coordinator" instead of ending blocked (`S:61`); AC-2.2 expects `worker_done --outcome failed` and `status: blocked` (`S:200`). A test brief that does not forbid `ask` can legitimately end in a wait, not a failure. Recommend: say the acceptance brief tells the worker not to ask.
- M-6 (Medium): "fresh dir" is the resume answer for about 20 commands (`S:99-125`), but no rule says a brief-named directory must be empty or that a stale `return-contract.yaml` from an earlier run is removed before the new run writes. A coordinator opening the report after a crash (`S:62`: written on every outcome) can read an old file. WC-3's "re-invoke the command with the answer" (`S:61`) reuses the same directory with the same risk.
- M-7 (Medium): `load` is counted among the 27 commands that change (`S:76`) and `S:159` says `--unattended` is accepted by every command in 3.1 and 3.2, but AC-1.1 excludes it (`S:195`) and its row writes no contract (`S:112`); WC-5 would map "no report exists" to `failed` for a `load` worker. The spec's own advice (use `load` inside another brief, `S:112`, `S:265`) avoids it, but the contradiction is not resolved in WC-5.
- M-8 (Medium): outward-action off-switches that need flags the inventories do not show. WC-9 says an outward default "turns on only through the command's own explicit flag" (`S:67`); auggie-review's `--post-pr` (`S:100`) and the task `commit`/`push` authorization (`S:121`) name no existing flag (`INV-A:38` shows only `--no-post-pr`; the task flag is not in `INV-B:45`). The flags would be new, and the section 3 rows do not list them as added.
- M-9 (Medium): tasklist `--unattended` makes each reflect "follow the existing headless auto-accept rule" (`S:88`, `S:122`, `S:151`), but the spec never says what that rule does (accepts remediation, hands off to /sc:workflow?). Its citations (`sk/sc-reflect-protocol/refs/remediation-handoff.md:239-247`) are UNVERIFIED here, and `S:280` records that an Orca worker is assumed not to be headless.
- M-10 (Medium): save writes only per-session keys (`S:119`, WC-11 `S:69`), but no row says how a later `/sc:load` finds them; the resume value of a saved state is lost to the coordinator.
- m-1 (minor): the document cites review labels never defined in it: `B-1` to `B-5`, `F-03`, `R2-01`, `SA-1` to `SA-3` used as tags in rows (`S:61`, `S:62`, `S:73`, `S:88-92`, `S:146`, `S:182`, `S:194-195`, `S:241`). A reader of the spec alone cannot resolve `B-4` or `F-03`.
- m-2 (minor): AC-1.3 uses `claude -p` (`S:197`), which is the headless mode that `S:280` says reflect keys on; harmless for analyze, misleading for the other P1 commands.
- m-3 (minor): `S:154` says Phases 1-3 need no user decision, while D1 (flag versus detection) governs P1 and D5 governs P2 fan-out; `S:225` says Phases 0-3 proceed on recommendations. Reword once.
- m-4 (minor): AC-C1 (`S:172`) forbids four `orca` subcommands but the guard text of SA-2 (`S:147`) forbids any `orca` or `orca-ide` command; `orca-ide skills get` or `orca status` would pass the check.
- m-5 (minor): the `ready today` heading (`S:78`) says the only command changes are small fixes, yet every 3.1 command also gains the unattended section (`S:76`, `S:195`) and workflow needs a new `--output` flag (`S:92`).
- m-6 (minor): item 14 of the spec's UNVERIFIED list (`S:285`) records a past validator pass inside a list titled UNVERIFIED items; it is a status note, not an open item.

The session that ran this review would ask the user once whether to open an issue for the follow-up candidates; this worker cannot ask, so nothing was created and the list is only recorded.

## Dependencies touched
README scope (`README.md:6`, `README.md:30`): planning only, honoured by the spec (`S:222`). The spec edits no `src/`. Its P0 proposes edits to `HOW-WE-WORK.md` and mirrors (`S:158`); that is a plan, not an action.

## Reviser brief
Blocking finding ids: B-1.
Rules for the reviser (restated from the command, the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, with bytes added and deleted per finding id. Leave Medium and minor findings alone; do not award yourself a PASS.

verdict: FAIL
