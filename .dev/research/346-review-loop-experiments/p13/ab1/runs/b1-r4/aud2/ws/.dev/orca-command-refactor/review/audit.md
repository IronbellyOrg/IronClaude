review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (first review of the whole document, labelled audit; FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (295 lines), sha256 `4e04817fb543edcb9c65e6cba29debf913eabe4a8ae7675d2f06bb264208171f`.
- Baseline: none given, none needed (first review).
- Reviewer model actually used: claude-sonnet-5-5.
- Binding context read first: `.dev/orca-command-refactor/README.md:1-38`.
- Citation rule: every `path:line` below was checked against a file inside the workspace. `src/`, `tests/`, `CLAUDE.md`, `EVIDENCE.md`, `~/.claude/commands|skills` are not in the sandbox, so a claim that rests only on them is marked UNVERIFIED. Spec lines are `SPEC:N`, `INV-A:N` = `inventory/commands-a.md`, `INV-B:N` = `inventory/commands-b.md`, `CAPS:N` = `inventory/orca-capabilities.md`.
- Panel (fixed order): Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker (always active), Newman, Hohpe (architecture). Crispin, Gregory, Hightower not seated (testing/compliance not in `--focus`), except that Crispin validated the Guard Condition Boundary Table.

## Summary

The spec is internally well built: counts conserve (43 = 21 + 22 at `SPEC:76`; 10 + 27 + 6 re-counted from the three tables at `SPEC:81-92`, `SPEC:97-125`, `SPEC:130-137`; the 37 non-coordinator commands appear exactly once across the P1-P4 rows at `SPEC:159-162`, and the phase tags in 3.1/3.2 agree with them), and the Orca facts it cites match the capabilities inventory (spot-checked 47 `CAPS:` lines, all found as quoted). One blocking defect: an acceptance check that cannot pass for commands the same document says have no such flag or contract. Everything else is Medium or minor.

=== REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL, blocking) AC-1.2 requires a contract and `--output <dir>` from P1 commands that the spec says have neither
- Location: `SPEC:206` (AC-1.2), against `SPEC:159`, `SPEC:62` (WC-4), `SPEC:86`, `SPEC:85`, `SPEC:112`, `SPEC:167`.
- Grading sentence: An implementer who follows the stated text as written builds a P1 live check that runs "each P1 command with `--unattended --output <dir>`" and requires `all steps pass`, including 7.2 step 4 `test -s <contract>` (`SPEC:193`); and builds a phase gate that says "A phase passes only when every check in its block ... passes" (`SPEC:167`). The P1 row (`SPEC:159`) lists `load` ("usage line only, no section"), whose row says "Report: none" and "use it as a step inside another worker's brief" (`SPEC:112`) and which AC-1.1 itself excludes (`SPEC:205`); it also lists `index-repo` ("Brief must pass: none", report `PROJECT_INDEX.md`, `SPEC:86`) and `cleanup-audit` (`--pass <N>`, `SPEC:85`), which WC-4 names as having no output flag (`SPEC:62`). Those commands accept neither `--unattended` nor `--output <dir>` and write no contract, so AC-1.2 cannot pass, P1 never passes, and "Later phases do not start until the earlier phase's checks ... pass" (`SPEC:154`) blocks P2-P4. The statement is wrong because AC-1.1 and 3.2 already carve `load` out and WC-4 already says which commands have no output flag; AC-1.2 does not.
- Expert: Wiegers (testability), Adzic (the example in the check contradicts the per-command rows).
- Recommendation: narrow AC-1.2 to "each P1 command that has a contract row" and name the exceptions (`load`; for `index-repo`, `cleanup-audit`, `workflow` the brief flags are those of their 3.1 rows, not `--output <dir>`). Delete rather than add: one clause.
- Priority: High. Quality impact: completeness and testability each about -1 until fixed.

=== ARCHITECTURE ANALYSIS ===

No architecture finding reaches blocking. The decision itself (Orca on top, commands as units; `SPEC:16`, `SPEC:29-37`) is consistent with the evidence in the capabilities inventory (`CAPS:97-101`, `CAPS:147-150`, `CAPS:155-161`), and the spec states its own evidence gaps plainly (`SPEC:41-45`, `SPEC:282`).

## Guard Condition Boundary Table (Nygard builds, Crispin checks completeness, Whittaker attacks)

Classes left out are named with a one-line reason under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 output dir resolution | `SPEC:62` | Zero/Empty | no `--output-dir`, no `--output`, no row path | no dir | stop before work, no contract, worker ends `failed` | OK |
| G1 | `SPEC:62` | One/Minimal | `--output report.md` in repo root | parent = `.` | contract lands in a directory other workers may share; "two workers never share one" is a coordinator duty, not enforced | GAP (M-6) |
| G1 | `SPEC:62` | Typical | `--output <dir>/` | dir | `<dir>/return-contract.yaml` | OK |
| G1 | `SPEC:62`, `SPEC:85`, `SPEC:87` | Legitimate Edge | fixed or default dirs (`.claude-audit/`, `.dev/superclaude/`) re-used by a second run | stale contract present | `test -s` (`SPEC:193`) passes on the old file; no rule says to clear or timestamp it | GAP (M-7) |
| G2 outcome mapping | `SPEC:63` | Zero/Empty | no report, or `status` missing or not one of four | invalid | `--outcome failed` | OK |
| G2 | `SPEC:63`, `SPEC:273` | Typical / Edge | `partial`; audit verdict FAIL | true | `succeeded`, body states `partial` or the verdict | OK |
| G2 | `SPEC:61`, `SPEC:63` | Legitimate Edge | worker dies after writing a contract, before `worker_done` | no done | no rule; coordinator "sees only through `worker-show`'s `agentWait` or a missing report" (`SPEC:44`), but the report exists | GAP (M-9) |
| G3 wait split | `SPEC:68` | One/Minimal | single tool call at exactly 4 min, heartbeat every 5 min | true | specified (4 min leaves margin, `SPEC:276`) | OK |
| G3 | `SPEC:114`, `SPEC:293` | Typical / Legitimate Edge | pr-submit poll script runtime plus sleep | unknown | explicitly UNVERIFIED and deferred to P4 | OK (declared, D3-gated) |
| G3 | `SPEC:104` | Maximum/Overflow | eval timeout 3600 s | exceeds 4 min | split into waits of at most 4 min | OK |
| G4 readiness | `SPEC:59` | Typical / Maximum | prompt 0-30 s fallback; 45 s+ fails; default 60 s | pass/fail | 30 s rule, evidence `EVIDENCE.md:45,56` via `CAPS:49` | OK |
| G5 task confidence | `SPEC:121` | Sentinel/boundary | < 0.70 blocked; exactly 0.70 | false at 0.70 | proceeds (inventory: prompt only below 0.70, `INV-B:45`) | OK |
| G6 `--unattended` detection | `SPEC:51`, `SPEC:238` | Sentinel Value Match | `--unattended` appearing inside a quoted prompt or topic (for example `/sc:tdd "explain --unattended"`) | undefined | spec fixes only "flag versus detecting the preamble"; no tokenisation rule | GAP (M-8) |
| G7 nesting depth | `SPEC:33` | Maximum/Overflow | worker calls `worker-start` | depth 2 > 1 | refused `nested_worker_depth_exceeded` (`CAPS:99`) | OK |

Left out: G1 Maximum (a path has no capacity bound in this spec); G2 One/Minimal (no count variable); G3 Zero (no zero-length wait is meaningful); G4 Zero/Sentinel (no sentinel); G5 Zero/Maximum (confidence is a 0-1 score fixed by the command, not by this spec); G6 Zero (the flag is present or absent); G7 Zero/Typical (depth 0 is the coordinator, `CAPS:97`).
Pipeline Dimensional Analysis: not triggered (no data-flow stage whose output count differs from input count; the only count relations, 43 = 10 + 27 + 6 and 37 = 15 + 15 + 4 + 3, were re-counted and hold). Quantity Flow Diagram not produced.

## Whittaker attack findings

- Sequence attack: WC-3 re-invokes the command after an `ask` answer and rewrites the contract (`SPEC:61`), while WC-6 sends fresh-dir commands to a new directory on every run (`SPEC:64`, most 3.2 rows say "fresh dir"). I can break this specification by re-invoking a "fresh dir" command: the invariant at WC-3/WC-6 fails when the rewrite target and the fresh directory differ; concrete attack: run 1 writes `<d1>/return-contract.yaml` (blocked), the worker re-invokes with the answered flag, the command makes `<d2>`, `worker_done --report-path` points at `<d2>` while `<d1>` still says `blocked`. Graded M-5 (needs a reading choice).
- Sentinel collision: see G6 / M-8.
- Divergence attack: AC-2.2 expects `worker_done --outcome failed` at a gate (`SPEC:210`), WC-3 lets the worker `ask` instead of ending (`SPEC:61`, "may"); both branches apply at once. M-3.
- Zero/Empty, Accumulation: no failing invariant found beyond G1/G2 above.

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium (warnings; each needs a guess about which reading an implementer picks, or states a missing requirement):

- M-1 (Wiegers/Fowler) `SPEC:73` requires every brief to carry `--unattended`, but the flag reaches ready commands only in P1/P2 (`SPEC:159-160`) and `SPEC:158` says P0 "gets value before any command changes". The P0 brief template (`SPEC:158`) would add a flag `/sc:troubleshoot`, `/sc:tdd`, `/sc:reflect`, `/sc:release-split` do not yet accept. Fix by saying the template adds `--unattended` only from the command's phase.
- M-2 (Nygard) WC-3 says the session "never relays an answer as a `/sc:implement` Ruling (D2)" (`SPEC:61`) but D2 option (b) allows exactly that (`SPEC:245`) and AC-4.1 anticipates it (`SPEC:218`). Make WC-3 say "unless D2(b)".
- M-3 (Adzic) AC-2.2 (`SPEC:210`) cannot be deterministic while WC-3 makes `ask` optional (`SPEC:61`) and 7.2 step 3 expects exactly one `worker_done` (`SPEC:192`); say which the test brief tells the worker to do.
- M-4 (Crispin) 7.2 step 5 (`SPEC:194`) searches the transcript for `AskUserQuestion`; the contract text WC-2 and each `## Unattended mode` section name that tool, and the worker reads them, so a text search may match a compliant run. Say "tool call named `AskUserQuestion`".
- M-5 WC-3 re-invoke versus WC-6 fresh directory (attack above, `SPEC:61`, `SPEC:64`).
- M-6 (Cockburn/Wiegers) The spec adds a path flag named `--output` to about 15 commands (`SPEC:99-125` "add `--output`" or "add a report path") without saying file or directory, while ready commands already differ (`--output <dir>` for adversarial and brainstorm, `--output <file>` for tdd, init-lite; `SPEC:83-84`, `SPEC:87`, `SPEC:90`) and WC-4 has a dual rule (`SPEC:62`). A file-valued `--output` in the repo root puts the contract in a shared directory. Note also `--output-dir` in WC-4 is named only for auggie-review (`SPEC:100`). The `/sc:spec-panel` definition in this sandbox already resolved the same question differently: `--report-dir` is the directory and `--output` is file-valued (`command.md:460`); align the spec's vocabulary with it.
- M-7 (Nygard) Stale contract in re-used or fixed directories (G1); only "fresh dir" commands are safe. State "delete or timestamp before work" or require the worker to compare the file's mtime to dispatch time.
- M-8 (Whittaker) `--unattended` token detection (G6). The sandbox command definition fixes it as "a standalone argument token outside any quoted argument" (`command.md:459`); the spec leaves it to D1 (`SPEC:238`).
- M-9 (Nygard) No rule for a worker that dies after the contract is written but before `worker_done` (G2); the coordinator cannot tell a finished run from a crashed one by the file alone. A `finished_at` field or "coordinator trusts `worker_done` only" would close it.
- M-10 (Wiegers) WC-1 is owned by "Launch setup, not commands" (`SPEC:59`) but no phase in `SPEC:156-162` and no AC in `SPEC:199-220` changes or checks the launch path; only the 7.2 step 1 `state: ready` pass (`SPEC:190`) touches it.
- M-11 (Hohpe) The mechanism that makes a worker run `/sc:x ...` is unspecified: the task reaches Claude as argv text (`CAPS:47`) after an Orca preamble, and a slash command is recognised only at the start of a message; `SPEC:16` and `SPEC:65` say "runs the command directly" and the PR #329 route was an Agent-tool wrapper (`SPEC:43`). P0 smoke runs (`SPEC:158`, AC-0.4 `SPEC:204`) will show it; add one line saying whether the worker uses the Skill tool or the slash form.
- M-12 (Cockburn) `SPEC:238` (D1 example) passes `--output .dev/troubleshoot/login/` to `/sc:troubleshoot`, yet WC-4 lists troubleshoot as a command with no output flag (`SPEC:62`) and the inventory records none (`INV-B:243-244` region, no `--output` for troubleshoot; the default is `.dev/troubleshoot/<slug>-<timestamp>/`). Use a flag the spec defines.
- M-13 (Newman) `--unattended` combined with `--interactive` is refused for cleanup, improve, roadmap, explain (`SPEC:103,110,118,108`) but only "never" in the brief for adversarial, brainstorm, release-split (`SPEC:83-84,89`); no rule says what the command does if both arrive.

Minor (notes):
- n-1 `SPEC:11`, `SPEC:25` ("grep ... run 2026-11-02"), `SPEC:295` (item 14, 340 citations re-read, 9 defects) rest on runs and files outside the workspace: UNVERIFIED here. The two inventories' own citation-check lines are present and say what the spec says (`INV-A:106`, `INV-B:320`).
- n-2 AC-1.4 (`SPEC:208`) greps for the string `return-contract.yaml` in the adversarial skill; the inventory says the skill already requires a contract without naming a file (`INV-A:60`), so the grep may pass before the fix. Grep for `adversarial/return-contract.yaml`.
- n-3 7.2 step 2 passes when `agentWait` is "never non-null"; Orca says an absent field means it never looked (`CAPS:129`). Say "present and null".
- n-4 `SPEC:76` counts `load` among "27 needing a change" though its only change is a usage line (`SPEC:112`); `brainstorm` is in the P1 row with "None" (`SPEC:84`). Harmless.
- n-5 `INV-A:35` calls the codegraph adversarial run "proven as a direct Orca-worker skill call"; `SPEC:43` correctly says the brief used an Agent-tool wrapper. The spec is the more careful of the two; no change.
- n-6 AC-C5 (`SPEC:180`) uses `master...HEAD` while `README.md:7` names a feature branch; confirm `master` exists locally in the executing worktree.

Issue offer: the session is asked once per loop whether to open an issue for the follow-up candidates (command.md Review Loop bullet 3). No user answer was available in this sandbox, so none was asked and no issue was created.

Coverage: whole document read once, lines 1-295 of the candidate; README; all three inventories sampled at every line the spec cites for the checks above (47 `CAPS:` lines, the `INV-A`/`INV-B` lines at `SPEC:26`, `37`, `128`, `230`, `270-278`); counts and phase membership re-counted from the tables; section 7 checks read against sections 2, 3, 6. Not covered: any `src/`, `tests/`, `CLAUDE.md`, `EVIDENCE.md` or `~/.claude` citation (UNVERIFIED, not in the sandbox); the `[G]`/`[H:...]` Orca guide text beyond what `orca-capabilities.md` quotes.

Reviser brief
Blocking finding ids: B-1.
Rules (restating Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Medium and minor findings (M-1 to M-13, n-1 to n-6) are not part of this brief and must not be edited.

verdict: FAIL
