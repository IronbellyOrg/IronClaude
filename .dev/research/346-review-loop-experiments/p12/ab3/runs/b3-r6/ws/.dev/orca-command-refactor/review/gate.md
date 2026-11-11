review: 1 of 3

# Gate review: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- prompt followed: GATE prompt (`~/.claude/rules/prompts/document_review_loop_prompts.md:57-64`), graded with the FIRST-REVIEW grading check (`:35`). Fresh context: I had read no earlier report of this loop. Brief text applied: `:64`.
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines, sha256 `361193fc0635fb15c8c62bef7845f79c10650c2ce1378fb6cefbbb9b882a7ae8`
- baseline: not given and not needed (first review). prior: none.
- reviewer model: claude-sonnet-5-5
- unattended: the final reply is DONE only, so I could not ask the user whether to open an issue for the follow-up candidates. They are only recorded (`command.md:260`).
- Evidence limit: the workspace holds only `.dev/orca-command-refactor/`. Every citation into `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `EVIDENCE.md` or the Orca install is UNVERIFIED by me. Citations into `inventory/*.md` and `README.md` were checked (below).

## Coverage
Whole document, all 9 sections plus Decisions and UNVERIFIED list (`spec:1-285`). Focus areas: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard); Whittaker ran as always. Checked against the inventories:
- Count arithmetic: 21 (`INV-A:3`) + 22 (`INV-B:3`) = 43; 10 ready (`spec:81-92`) + 27 needing change (`spec:97-125`, I counted 27 rows) + 6 coordinator-only (`spec:130-137`) = 43. Holds. Needs-change 13 (A) + 14 (B) = 27 matches `INV-B:289`.
- Phase table covers every one of the 27 rows exactly once (P1 9, P2 11 with 4 ready-command fixes, P3 4, P4 3; `spec:159-162`).
- Inventory and capability lines the spec leans on, spot-checked and found as cited: `INV-A:35,36,43,52,60-62,76-83,90,94-98,106,113,118-120`; `INV-B:3,57-65,272,285-287,289-299,301,311,320,323`; `CAPS:10-21,44-46,52,58-64,72-80,86,92,97-103,115,129-130,145-151,155-161,178-188`.
- Not covered: whether `src/` files say what the spec says; the 11 re-read locations (`spec:11`) and the 9 fixes (`spec:285`) are the spec's own attestations, UNVERIFIED here.
- Pipeline Dimensional Analysis (FR-17): not triggered. The phase/command partition is not a data pipeline with N != M stages; the only count flow is 43 = 10 + 27 + 6, which conserves. No Quantity Flow Diagram needed.
- Correctness focus not requested: no State Variable Registry.

## === REQUIREMENTS ANALYSIS ===

Wiegers: the contract requirements WC-1..WC-12 (`spec:57-70`) are mostly testable, each with an owner and evidence. Acceptance checks AC-C1..AC-4.3 (`spec:170-210`) give runnable commands and pass conditions. Traceability from WC to AC is good except where noted.

**F-1 [label MAJOR, graded Medium] Contract file for the "ready" commands is not assigned to any phase.** WC-4 says that in unattended mode the command writes `return-contract.yaml` "at the path its section 3 row names", default `<output-dir>/...` or `<file>.return-contract.yaml` (`spec:62`). But section 3.1 says "The only command changes are the small fixes in the last column" (`spec:79`), and for tdd, troubleshoot and release-split the "Report today" column names the deliverable (the TDD, `REPORT.md`, `release-split-report.md`), not a contract (`spec:89-91`). AC-2.2 and AC-2.3 then require `contract status: blocked` and a contract-based `--outcome` for every P2 command (`spec:200-201`, via 7.2 step 3-4, `spec:182-183`). Reading `spec:76` ("every command in a phase scope that lists `--unattended` gains the section") together with WC-4's default path closes the gap, but that is a precedence guess between `spec:79` and `spec:62`; so Medium. Expert: Wiegers. Recommendation: add "contract (WC-4 default path)" to the P2 small-fix cells for tdd, troubleshoot, release-split (and say the same for reflect's existing file). Priority: Medium. Quality impact: Completeness +1.

**F-2 [MAJOR, Medium] Nothing tells the coordinator not to dispatch gate-bearing commands before they get `--unattended`.** `spec:154` says "before then the coordinator briefs it without the flag". For `/sc:implement` (halt gate, P4), `/sc:post-release` (P4), `/sc:pr-submit` (P4) and every P2/P3 gate command, a worker briefed without the flag stalls silently: Orca reports a worker on a prompt as "healthy, not failed" (`CAPS:52,129`, quoted in `spec:60`). Section 2.3 (`spec:73`) lists what the brief must carry but has no "do not dispatch before phase X" rule, and section 3.1 covers only the 10 ready commands. An implementer of P0's brief template (`spec:158`) would produce a template with no such guard. The harm needs the coordinator to dispatch early, hence Medium. Expert: Nygard (what happens when this fails). Recommendation: one line in 2.3: a section 3.2 command is dispatched only from the phase in its Phase column. Priority: High among the follow-ups. Impact: Testability.

**F-3 [MAJOR, Medium] WC-11 is stated absolute, then violated by listed ready commands.** WC-11: "Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug" (`spec:69`). Section 3.1 keeps `cleanup-audit` with a fixed output dir ("one audit per worktree at a time (WC-11)", `spec:85`), `index-repo` writing `PROJECT_INDEX.md` (`spec:86`) and init-lite's fixed default (`spec:87`). The mitigation is a coordinator behaviour (serialize), not stated in 2.3 (`spec:73`). Two concurrent workers on cleanup-audit would clobber each other only if the coordinator dispatches them in one wave (the ready-wave pattern, `CAPS:86`), which the spec never forbids. Medium. Expert: Fowler. Recommendation: add the one-at-a-time constraint to the 2.3 brief list, or relax WC-11 to "unless the row says one at a time".

**F-4 [MAJOR, Medium] The common check AC-C1 is wider than the rule it enforces.** SA-2 bans Orca commands in "command, skill or agent" files (`spec:147`). AC-C1 greps `src/superclaude/core` too and "prints nothing" must hold in every phase (`spec:172`). P0 adds `core/WORKER-CONTRACT.md` and an Orca section in `core/HOW-WE-WORK.md` (`spec:158`), and SA-2 itself allows Orca mentions in the contract file (`spec:147`). If either file writes `orca-ide orchestration ...` or `orca worktree ...`, AC-C1 fails P0 although SA-2 allows it. Needs a guess about the wording of those files, so Medium. Recommendation: exclude the two named core files from AC-C1 or narrow its path list to commands, skills and agents.

**F-5 [MAJOR, Medium] AC-1.1's negative assertion breaks in P2 under AC-C3.** The P1 test asserts "no other command and no section-4 command has one yet" (`spec:195`) in `tests/skills/test_worker_contract.py`, which P2 extends (`spec:199`). AC-C3 requires no previously passing test to fail (`spec:174`). A fixed-set negative assertion would fail in P2. "Yet" implies phase-relative, but the text does not say the set is parameterized. Medium. Recommendation: say the expected set grows per phase.

**F-6 [MAJOR, Medium] P2 implements the switches D4 decides, while the document says P1-P3 need no decision.** `spec:154` and `spec:225` say Phases 0-3 proceed on the recommendations; D4 lists auggie-review `--post-pr` and task `commit`/`push` as affected (`spec:244`), and both rows are P2 (`spec:100,121`). Under D4(b) "Never", the explicit `--post-pr` path in `spec:100` would not exist. The default-off half is safe under both options, the opt-in half is not. Medium. Recommendation: P2 does the default-off half only; the opt-in flag waits for D4.

**F-7 [Medium] AC-0.4 depends on a report file adversarial does not yet fix.** AC-0.4 passes `--outcome succeeded` "when the command's existing report file was written" (`spec:194`). Adversarial's contract filename is unfixed until P1 (`spec:83`, `INV-A:60`: workers wrote it in two places). The brief passes `--output <dir>`, so the deliverables exist, but "its existing report file" is undefined for that smoke run. Recommendation: name the adversarial file the P0 check inspects.

**F-8 [Medium] WC-1 and WC-12 have no deliverable or check.** WC-1 assigns the fix to "Launch setup, not commands" (`spec:59`); no phase in `spec:158-162` changes any launch setup, and 7.2 step 1 only observes `state: ready` (`spec:180`). WC-12 (`spec:70`) has no AC. Recommendation: either mark both as coordinator-side preconditions in 2.3 or give each a check. Related: WC-3 lets the worker ask instead of stop (`spec:61`) while AC-2.2 expects `--outcome failed` (`spec:200`); the brief must pick one (Adzic: give the example).

**F-9 [Medium] "Apply only items the file already allows without approval" is not defined for cleanup and improve.** The rows (`spec:103,110`) rely on the command text (`cmd/cleanup.md:116-127`, UNVERIFIED here) and admit the rollback mechanism is UNVERIFIED (`INV-A:43,52`, checked). The spec does not say which edits those are or require a clean tree first. Data-loss risk is bounded by git and the changed-file list, so Medium. Recommendation: require the brief to state a clean worktree, or name the allowed item classes.

**F-10 [Medium] What the reflect headless auto-accept does is not stated where tasklist depends on it.** Tasklist Stage 10.5 under `--unattended` makes each reflect auto-accept `--remediate` (`spec:122`; reflect row `spec:88`; SA-6 `spec:151`). The inventory only says it "auto-accepts for auto-fixable registers" (`INV-B:107-115` area, line text read at the reflect block); whether that launches `sc:workflow` or writes outside the output dir is not stated. Recommendation: one sentence on its scope, or keep `--no-reflect` as the worker default.

## === ARCHITECTURE ANALYSIS ===

Fowler/Newman: the decision (Orca above, commands as units; `spec:13-39`) is sound against the evidence. Boundaries are clean: one shared contract file, per-command sections that only list their gates (`spec:52`), no Orca calls in commands (SA-2, WC-8). Rejection reasons R1-R5 trace to `CAPS:97-103,145-150` (checked). Section 1.4 states honestly that no direct-route run exists (`spec:43`, `INV-B:323` checked) and P0 tests that first (`spec:158,194`). Hohpe: the report-file-as-message pattern plus `worker_done --report-path` pointing at it fits Orca's metadata-only handling (`CAPS:79`, checked). Nygard: failure modes are covered by blocked/failed/partial mapping (WC-5), retry (WC-6) and heartbeats (WC-10); the open gap is F-2. Versioning: `--unattended` is additive (SA-4), so old callers are unaffected.

Architecture-side notes (all non-blocking): the plugin mirror `plugins/superclaude/commands/` is flagged UNVERIFIED (`spec:279`), but P1-P4 edit commands and AC-C2 only runs `make verify-sync`; the spec defers it to each phase plan, which is acceptable. Two sources of truth for the unattended rule (contract file plus per-command sections) are tied together by AC-1.1 and AC-2.1.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

- I can break this specification by **Sequence Attack**. The invariant at **section 6 line 154 ("briefs it without the flag")** fails when **the coordinator dispatches implement before P4**. Concrete attack: before P4, worker for `/sc:implement` hits `E-HALT-QA`; ends turn on a chat question; `worker-show` shows `agentWait` non-null but the coordinator polls only per 7.2 (test-time) not per the brief; no `worker_done` ever. Rated Medium (see F-2).
- **Accumulation Attack** on WC-11: two cleanup-audit workers in one worktree both write `.claude-audit/` (`spec:85`); second overwrites `progress.json`. Medium (F-3).
- **Sentinel Collision** on the status field: `partial` maps to `succeeded` (`spec:63,263`); a coordinator reading only `--outcome` cannot tell a partial run from a full one, which the spec covers by the body's first sentence (WC-5). No finding.
- **Zero/Empty Attack** on WC-4: an empty `blocked_question` with `status: blocked`; AC-2.2 requires non-empty (`spec:200`) but WC-4 itself does not (`spec:62`). Minor note (m-1).
- **Divergence Attack** on D1: `ORCA_TERMINAL_HANDLE` in a person's own tab is UNVERIFIED (`spec:229,284`); the spec avoids it by recommending the flag. No finding.

## Guard Condition Boundary Table
Classes left out are given with a reason after each guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| readiness limit 60 s | WC-1 `spec:59` | Zero/Empty | `--timeout-ms` 0 or absent | default 60 s | `CAPS:44` falls back to default; spec silent on wording | OK |
| readiness limit 60 s | WC-1 `spec:59` | Typical | prompt with 30 s fallback | pass | `EVIDENCE.md:45,56` as quoted (UNVERIFIED) | OK |
| readiness limit 60 s | WC-1 `spec:59` | Maximum/Overflow | fallback above about 45 s | fail | "well inside" with no number | GAP (Medium, F-8) |
| heartbeat 5 min / wait 4 min | WC-10 `spec:68` | Typical | 3 min wait | true | heartbeat between waits | OK |
| heartbeat 5 min / wait 4 min | WC-10 `spec:68` | Maximum/Overflow | single tool call 6 min | false | split into <= 4 min waits | OK |
| heartbeat 5 min / wait 4 min | WC-10 `spec:68` | Legitimate Edge Case | exactly 4 min / 5 min | boundary | "at most 4 minutes" | OK |
| report status mapping | WC-5 `spec:63` | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| report status mapping | WC-5 `spec:63` | Sentinel Value Match | `status: partial`; audit verdict FAIL | succeeded | maps to `succeeded`, body states status | OK |
| report status mapping | WC-5 `spec:63` | Legitimate Edge Case | `blocked` with empty `blocked_question` | failed | WC-4 does not require non-empty | GAP (minor, m-1) |
| task confidence 0.70 | `spec:121` | Legitimate Edge Case | exactly 0.70 | not stated | row says "below 0.70" blocked | OK |
| nested depth 1 | R1/WC-8 `spec:33,66` | Maximum/Overflow | worker calls `worker-start` | refused | `nested_worker_depth_exceeded`; WC-8 forbids | OK |
| nested depth 1 | R1/WC-8 `spec:33,66` | Legitimate Edge Case | `task-create` at depth 1 | unknown | UNVERIFIED, forbidden either way | OK |
| `--unattended` token | D1 `spec:228` | Zero/Empty | flag absent | false | SA-1 unchanged behavior | OK |
| `--unattended` token | D1 `spec:228` | Legitimate Edge Case | pre-phase command given the flag | not stated | "briefs it without the flag" only | GAP (Medium, F-2) |

Left out: One/Minimal and Sentinel for readiness and heartbeat (no meaningful case); Zero/One/Max for task confidence (a single float threshold, only the boundary matters); Zero and Typical for depth (fixed setting 1, `CAPS:98`).

## follow-up candidates (Medium and minor; none blocking)
Medium: F-1, F-2, F-3, F-4, F-5, F-6, F-7, F-8, F-9, F-10 (details above).
Minor notes:
- m-1: WC-4 does not say `blocked_question` is non-empty when `status: blocked`, while AC-2.2 requires it (`spec:62,200`).
- m-2: Section 6 calls P1's eight commands "no-gate" (`spec:159`) though business-panel, explain, test and index each get a refusal or non-wait statement under `--unattended` (`spec:102,108,111,123`).
- m-3: "ladder rung 2" in the Decisions table (`spec:261`) is not defined in this document.
- m-4: The spec-panel row says "add `--output`" (`spec:120`). The `/sc:spec-panel` command definition supplied to me already has `--output` and a separate `--report-dir` that gets `<report-dir>/return-contract.yaml` (`command.md:23,460-461`), unlike WC-4's `<file>.return-contract.yaml` rule (`spec:62`). I cannot tell which version is newer; check before P2.
- m-5: `spec:11` and `spec:285` assert citation re-checks I could not repeat; all `src/` and `CLAUDE.md` citations are UNVERIFIED.
- m-6: `spec:195` and `spec:197` give shell examples (`claude -p ...`) whose scratch-worktree setup is not described; fine for a plan.

## Brief handling
No brief clause was overridden. I added no minimum finding count and treated no minor finding as blocking.

Reviser brief: none (no blocking findings; nothing to revise).

verdict: PASS
