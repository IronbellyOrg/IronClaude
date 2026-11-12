---
title: "Spec: Orchestrator Mode Phase 1, read-only /sc:sweep and WC-14 (#339)"
base_variant: opus:architect
sources:
  - V1 variant-1-opus-architect.md (base)
  - V2 variant-2-opus-analyzer.md
  - V3 variant-3-haiku-backend.md
convergence: 1.00
gate_status: BLOCKED_BY_INVARIANTS
gate_reason: "INV-005 owner sign-off not recorded"
---

<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (opus:architect) -->
<!-- Merge date: 2026-11-08T04:55:40Z -->

# Spec: Orchestrator Mode Phase 1, read-only `/sc:sweep` and WC-14 (#339)

<!-- Source: Base (original, modified) per Changes 1, 2, 38, 42 -->

| Field | Value |
|---|---|
| Document | Merged spec from three variants |
| Base | Variant 1 (opus, architect, emphasis "maintainability and extension scaffolding") |
| Date | 2026-11-08 |
| Status | Merged spec after adversarial debate; release gated on INV-005 owner sign-off (section 13) |

Provenance tags name the variant line or Round 3 line each changed text came from. V1 = architect, V2 = analyzer, V3 = backend.

Citation key: `V1:148` is line 148 of variant 1 (likewise `V2:` and `V3:`); `V1R3:22` is line 22 of `debate/round3-final-v1.md` (likewise `V2R3:` and `V3R3:`). Text without an inline tag is unchanged V1 text. Each numbered section carries a `Provenance:` line naming its sources.

Sources read for this spec: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/seed-brief.md` (whole) [Conv:324; Change 2]; REPORT Section 8 Phase 1 (lines 1216-1340); GAPS lines 118-140; `synthesis/phase7-summary.md`; `enrichment/codebase-context.md`; `src/superclaude/core/WORKER-CONTRACT.md` lines 20-79 and 104-159; a grep of `.gitignore`. REPORT = the research report, GAPS = `gaps-and-questions.md`, both in `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/`. Anything not traced to those reads is marked UNVERIFIED. Additional sources: the Round 3 files at `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/adversarial/adversarial/debate/round3-final-v1.md`, `round3-final-v2.md` and `round3-final-v3.md`. The host git version, if quoted, must be recorded with the date it was checked. [V2:9; Change 38]

**Terms.** [Change 42]

- GQ = a gap question row in `gaps-and-questions.md` (GAPS).
- WC = a numbered rule in `WORKER-CONTRACT.md`.
- REPORT and GAPS are as defined above.
- Run, Task and Dispatch are Orca orchestration terms, used as Orca's read verbs name them; their exact definitions are not restated in the sources read here (UNVERIFIED).
- CND = could not determine.
- AC = acceptance criterion.
- K-1, K-4 and similar K- labels are cited from the REPORT; their full meaning is not stated in the sources read here (UNVERIFIED).

## 1. Problem and scope

Provenance: V1 (base, original)

<!-- Source: Base (original) -->

**Problem.** A person running many Claude Code sessions across Orca worktrees must open each one to learn whether it is working, waiting for them, stuck, finished or safe to close. The worker contract has no rule that the coordinator keeps polling, re-arms an expired wait or sweeps on a schedule (seed brief line 17; `WORKER-CONTRACT.md:45` is the only match for those words, REPORT line 48 via phase7 summary).

**Goal of Phase 1.** One coordinator-only, read-only command that observes one worktree tree, classifies every Orca worker and every person-started Claude session over a 6 h activity window, and writes one dated Markdown report; plus the WC-14 coordinator-loop rule in the worker contract.

**Success metric.** The person answers "who needs me, and what is safe to close" from one report, without opening a child session (seed brief line 47).

**Scope.**

- One worktree tree: a feature worktree and its Orca child worktrees (seed brief line 26).
- Inputs: Orca read verbs, one `git status` per worktree, task-package ledgers and contracts on disk, ccsession tab map and transcript files. No new store.
- Output: one dated report file under `<root>/.dev/sweeps/` and JSON on stdout. That file is the only write.
- Deliverables: package `src/superclaude/cli/sweep/`, command `src/superclaude/commands/sweep.md`, skill `src/superclaude/skills/sc-sweep-protocol/`, tests under `tests/sweep/`, WC-14 and the never-as-worker addition, routing registries and docs (REPORT steps 1.1 to 1.29).

**Architectural stance.** Phase 1 is the first of six phases. Its code must be the stable read model the later phases build on, so this spec fixes four extension points now and keeps everything else minimal: the ordered rule table in `classify.py`, the exact read allowlist table in `probes.py`, the versioned JSON output, and a hard split between read code (this package) and any future write code (a separate package with its own seam). Nothing speculative is built; the points are shapes, not features.

## 2. Out of scope (Phases 2 to 6)

Provenance: V1 (base, modified per Change 21)

<!-- Source: Base (original, modified) per Change 21 -->

Phase numbers are the REPORT's, not a source's (REPORT line 1324). None is designed here.

| Phase | What | Blocker | Extension point |
|---|---|---|---|
| 2 `/sc:close` | Act on safe-to-close REVIEW rows after the person confirms | Section 4 refusals turned into executed checks, "all commits pushed" and the `.dev/tasks/` rule; removal only through `orca worktree rm`; named instruction plus confirmation at the moment of action; contract edits after PR #422 (REPORT line 1328) | Reads sweep JSON schema v1 as a hint only, re-probes before acting; own package and own write allowlist (FR-021) |
| 3 Resume | Resume a stalled (proved) or frozen session as a new Task | WC-6 and WC-10; needs positive stall proof, never `unverifiable` (REPORT line 1329) | New rows in the classify rule table, never a reorder |
| 4 Trust layer | One permission mode, fixed message types, signed narrow grants | `CCSESSION_PERMISSIONS=default` mode mismatch; no Macaroon or Biscuit design; comment-3 research and debate first (REPORT line 1330) | None in the sweep package |
| 5 Orchestrator of orchestrators | Sweep several coordinators' Runs | Version-2 work after the comment-3 research (REPORT line 1331) | Repeatable `--run`; `scope` field in JSON |
| 6 Management-server relay | Relay results through a management server | Owner must define "management server" (GQ-66); no standing service (REPORT line 1332) | JSON schema v1 |

("Section 4 refusals" in the Phase 2 row refers to `WORKER-CONTRACT.md`, not to this spec.)

Also out of Phase 1: `check --peek` and `check --all` (gated on a probe of 06 Gaps 1, 2 and 18, REPORT line 1302); `--include-remote` until its cost is measured (GQ-22); any `gh` call; `gate-list`, `worker-read`, `run-list`, `git stash list`, `git log`, `git branch`, `git rev-parse` and `git --version` (GQ-104, GQ-109, GQ-110, this spec section 8). [V2:203; Change 21]

## 3. Functional requirements

Provenance: V1 (base) + V3R3 (INV-001, INV-002, INV-003, INV-007) + V2 + V3 (Changes 3, 4, 5, 6, 8, 10, 11, 12, 13, 21, 24, 25, 26, 28, 30, 33, 35)

<!-- Source: Base (original, modified) per Changes 3-6, 8, 10-13, 21, 24-26, 28, 30, 33, 35 -->

Each acceptance criterion (AC) is checked with the two seams mocked (section 8) unless it says "live". The only exception is the one marked real-git test of NFR-002, which runs `git` inside `tmp_path` only. [V2:98; Change 22]

| ID | Requirement | Acceptance criterion |
|---|---|---|
| FR-001 | `superclaude sweep run [--run <id>]... [--window <N>h\|<N>d] [--root <dir>] [--output <dir>]` exists, registered with the deferred-import pattern in `cli/main.py` (REPORT step 1.7). | `superclaude sweep --help` and `sweep run --help` exit 0 under `CliRunner` (step 1.13). |
| FR-002 | Run selection. `--run` is repeatable. Without `--run`, call `run-current`. An unavailable lookup exits 2 with `Orca unavailable; no Run binding could be established: pass --run <id>`; a confirmed missing binding exits 2 with `no Run bound: pass --run <id>`. Neither case writes a report or success JSON. With an explicit Run, or a binding already established by a successful lookup, a later unavailable result stops further Orca reads, retains already collected evidence, marks remaining Orca sources unscanned, adds the `Orca unavailable` banner and `orca_available: false`, and permits disk-only continuation. Exit 0 requires successful report publication; write failure exits 1 without success JSON. [V3R3:31; INV-001] No `run-list` fallback (GQ-104). | Three tests [V3R3:31]: (1) no `--run` plus first-call failure: one `_orca` argv recorded, exit 2, no report, no JSON; (2) explicit `--run` plus first-call failure: one `_orca` argv recorded, report published, exit 0; (3) binding R1 established, then second-call failure: two `_orca` argv recorded, report published, exit 0. Only (2) and (3) publish. A fourth test, gated on step 1.0a because the no-binding shape is UNVERIFIED [V3R3:32]: a fixture of the captured no-binding `run-current` JSON with zero exit and no `--run` exits 2 with `no Run bound: pass --run <id>`, writes no report and no success JSON, and records no `worker-list` or `worker-show` argv. [V1R3:22; Change 3] |
| FR-003 | `--window` default `6h`; anything other than a positive integer plus `h` or `d` is a usage error (exit 2). | Parser cases `6h`, `3d` pass; `0h`, `6`, `6m`, `-1h` exit 2. |
| FR-004 | `--output` default `<root>/.dev/sweeps/`; a resolved path outside `<root>/.dev/` is a usage error. The check uses the resolved path, so a symlink cannot lead outside `<root>/.dev/`, and the output directory must not overlap any input package or transcript directory. [V3:156-157; Change 26] Default `--root` is found by walking up from the current directory with plain reads to the first directory holding `.git`, as a file (linked worktree) or a folder; no `_git` call is made for it. [V2:203; Change 21] | `--output /tmp/x` exits 2 and writes nothing. A symlinked `--output` that escapes `<root>/.dev/` exits 2 and writes nothing; `--output` equal to a package directory exits 2 and writes nothing. [Change 26] The root walk accepts both a `.git` file and a `.git` folder and records no `_git` argv. [Change 21] |
| FR-005 | The sweep lists every Orca Task/Dispatch row of the selected Runs, every worktree under the tree, and every person-started session (FR-010). Totals that cannot be known are shown as lower bounds, and visible, historical and omitted counts must reconcile. [V3:114, V3:299; Change 11] | Fixture with 3 workers, 2 worktrees, 1 person session yields 6 rows in JSON and in the report; `<shown>/<total>` equal. |
| FR-006 | Each session row gets exactly one class from section 7, chosen by the ordered rule table. | Parametrized test, one case per section 7 rule (REPORT rules 1-7 plus idle); each class name is reached at least once. |
| FR-007 | `classify` receives a `SweepContext` holding `now`, `window` and `window_start` (GQ-103(2)). | A row with transcript mtime 5 h old is idle-eligible only when window is under 5 h; same row, window 6 h, is not idle. |
| FR-008 | "Could not determine" is its own class, never folded into stalled or idle; `unverifiable`, a late heartbeat, a stale `liveStatus` or a missing row give it (WC-10, `WORKER-CONTRACT.md:45`). | Fixtures for each of the four inputs give `could not determine`, never `stalled (proved)`. |
| FR-009 | Stalled (proved) only from Orca's own exit proof with no `worker_done` and no fencing evidence; with fencing evidence unreadable rule 2 declines and attaches the note; the row is classified by later rules, and by the fallback if none matches (REPORT step 1.3 rules 2, 3; GQ-84). [V3R3:53; INV-007; Change 6] | Two cases, neither using a blocked contract [Conv:326; Change 6]: (1) an exited row with unreadable fencing evidence and a `guard refused:` body classifies as finished (rule 6) and carries the note `Orca: exited; fenced evidence not readable`; (2) an exited row with unreadable fencing evidence and nothing else classifies as could not determine through rule 8 and carries the same note. |
| FR-010 | A person-started session is a transcript under a scanned root's project key that the ccsession tab map joins to no Orca row; one with no activity inside the window goes to Historical sessions (GQ-108). Represent `person_started` as True, False or None. A positive transcript-to-worker join makes it False. Only when every scoped Run's worker list is complete, no relevant list or join is unscanned or truncated, and the tab map is read and the join completed may an unjoined transcript be True. Otherwise it is None. None never becomes idle or Historical; an origin-unknown transcript is could not determine, with an explicit reason such as Orca unavailable, worker list truncated, worker list call failed or tab map unreadable. Idle requires True and the existing readability and activity-window conditions. [V3R3:33; INV-003; Change 5] The C-014 full-page lower-bound note and this completeness guard apply together; counting only discovered rows does not establish a complete negative join. [V3R3:55; INV-009] A transcript must be readable to count; an unknown timestamp is never idle; open Tasks, explicit waits and unread-report candidates are exempt from the activity window and never go to Historical. [V3:93, V3:234-237; Change 33] | Complete-negative-join case: fixture with 2 transcripts, one mapped to an Orca row, one not; only the unmapped one is person-started; an 8 h old unmapped one is listed under Historical. Incomplete cases [V3R3:33]: an older transcript during an outage; an older unjoined transcript after a full page with uncaptured continuation; an incomplete list after `call_failed`. All three remain visible and unknown, not Historical. Exemptions [Change 33]: one fixture each for an unreadable transcript, an unknown timestamp, an open Task, an explicit wait and an unread-report candidate; none becomes idle or Historical. |
| FR-011 | Waiting on a person comes first among the classification sections of the report, after the header and source coverage, split into (a) explicit questions, oldest first, tie-break by ID, unknown age in its own group, and (b) blocked by policy, never with question text (REPORT step 1.5). [Change 14] | Rendered heading order test against the section 9 order; sort test with 3 ages plus one unknown. |
| FR-012 | Safe-to-close is a separate two-part REVIEW value (terminal, worktree), each `yes`, `no` or `could not determine`. Phase 1 never prints `worktree removable: yes`. | Over all fixtures, no row has `safe_to_close.worktree == "yes"`. |
| FR-013 | A worktree is `removable: no` with the condition named when status shows uncommitted changes, an unpushed branch (ahead or no upstream), an unsaved path under `.dev/tasks/`, a frozen plan, a package in state unfinished, archive-blocked, interrupted-archive or conflict, or an active package shared with another worktree. [V2:160-168; Change 30] | One fixture per condition, including archive-blocked; each prints `no` plus its named reason. |
| FR-014 | Package states are read per package folder: `unfinished`, `archive-blocked`, `interrupted-archive`, `conflict`, `archived`, `unknown` (section 7; GQ-102, GQ-105). | Fixture per state, including one package id in both `to-do/` and `done/` giving `conflict`. |
| FR-015 | One package id is "shared" only when it is active in two or more worktrees; active means that worktree's single `git status` shows a changed or untracked path inside that package folder (GQ-101). A reported untracked package directory (one `?? .dev/tasks/to-do/<id>/` line) counts as package activity; absent untracked output is not proof that no package is active (section 14, INV-008). [V1R3:43, V3R3:54; Change 8] | Shared-folders fixture: 3 worktrees with the same 44 committed, unchanged folders give no shared flag; one folder modified in 3 worktrees gives one line naming all 3. A fixture with one `?? .dev/tasks/to-do/<id>/` line marks that package active. |
| FR-016 | Every untrusted string passes `sanitize()`, which strips ESC/CSI/OSC, C0/C1 controls, carriage returns and bidi controls, folds newlines to a space, and escapes the pipe character with a backslash (REPORT step 1.5; GQ-107), and neutralizes Markdown HTML so no untrusted text becomes an active tag or link. [V3:317-318; Change 25] | Injection fixture includes `a\|b`, an ANSI sequence, a bidi override, a `<script>` tag and a Markdown link; the rendered table keeps its column count and no untrusted text renders as an active tag or link. |
| FR-017 | The report is written to `<output>/<YYYYMMDD-HHMMSS>-sweep.md`, or its collision-suffixed form (section 5.3). [Change 13] JSON on stdout: schema version 1, additive-only compatibility, golden key-set test and row key `class`; per-row `rule`, `evidence`, `notes` and `safe_to_close`, never yes in Phase 1; explicit zero counts and `waiting.a`/`waiting.b` as stable-ID lists. Markdown and JSON share the observation model. Print the one success JSON object only after report publication. Failed publication exits 1 without success JSON or overwriting an earlier observation. [V3R3:43; Change 12] Every key is always present (REPORT step 1.6). | Key-set and type test on stdout. File exists at the dated path or its suffixed form, and an existing file is never overwritten; two report-publishing sweeps with the same injected `now` produce two files. [Change 13] Stdout holds no success JSON when the report write is made to fail; zero counts are present; `waiting.a` and `waiting.b` hold IDs only. [Change 12] |
| FR-018 | Exit codes: 0 means collection completed and the report was successfully published (could-not-determine rows allowed) [V3:161; C-016]; 1 internal error with `[sweep ...]` stderr prefix, including an argv outside the allowlist and any report write failure; 2 usage error, including no Run binding and Orca unavailable before a binding is established. [Change 3] Full contract in section 5.1. | One test per code. |
| FR-019 | Orca unavailable (`runtime_unavailable` or another unavailable cause, section 8). Without `--run`, call `run-current`. An unavailable lookup exits 2 with `Orca unavailable; no Run binding could be established: pass --run <id>`; a confirmed missing binding exits 2 with `no Run bound: pass --run <id>`. Neither case writes a report or success JSON. With an explicit Run, or a binding already established by a successful lookup, a later unavailable result stops further Orca reads, retains already collected evidence, marks remaining Orca sources unscanned, adds the `Orca unavailable` banner and `orca_available: false`, and permits disk-only continuation. Exit 0 requires successful report publication; write failure exits 1 without success JSON. [V3R3:31; INV-001] Disk-only continuation uses discovery from `--root` fixed patterns only, and every unscanned Orca source prints `unscanned: orca unavailable`. | The same three tests as FR-002 [V3R3:31]: no `--run` plus first-call failure (one `_orca` argv, exit 2, no report, no JSON); explicit `--run` plus first-call failure (one `_orca` argv, report published, exit 0); binding R1 established, then second-call failure (two `_orca` argv, report published, exit 0). Only the last two publish. [Change 3] |
| FR-020 | Per-sweep bounds: at most 50 `worker-show` calls, 10 s per call, 90 s total probe budget; once reached, no new probe starts and remaining rows print could not determine with `unscanned: call bound reached` (REPORT step 1.4). The cap of 50 counts only `worker-show` calls; every call counts toward the 90 s total. [V1R3:49; INV-010] Each call's timeout is the lesser of 10 s and the remaining total budget. Proposed byte limits: 1 MiB per contract or ledger read, 256 KiB transcript tail, 8 MiB subprocess output; proposed, rationale required before release. A read that hits a limit marks that source unscanned with a reason. [V3:124-125, V3:137; Change 24] When the cap is reached, the header says so and the row total is a lower bound. [A-107; Change 11] | Fixture with 60 rows: exactly 50 `worker-show` argv recorded, 10 rows bound-reached, `summary.bound_reached == 10`, header states the cap was reached and the total is a lower bound. A fixture with 20 s remaining passes a per-call timeout no greater than the remaining budget. A contract fixture over 1 MiB marks that source unscanned with a reason. |
| FR-021 | Read and write code never share a seam or a table: the sweep package holds no write verb, and no later phase adds one to it. | Static test that `probes.ALLOWED_ORCA` holds no verb from a fixed forbidden list (`check`, `ask`, `reply`, `send`, `inbox`, `open`, `worker-start`, `task-create`, `task-update`, `dispatch`, `stop`, `rm`). Negative test: a `worker-read` argv passed to `_orca` raises before any subprocess starts. [V2:99; Change 28] |
| FR-022 | `/sc:sweep` command and `sc-sweep-protocol` skill. The command's Activation block invokes the skill by installed path `~/.claude/skills/sc-sweep-protocol/SKILL.md`, with the project `.claude/` copy as dual surface. The skill calls `superclaude sweep run` from PATH first, then `uv run superclaude sweep run` on "command not found". No `## Unattended mode` section (REPORT steps 1.14-1.16). | `tests/commands/test_sweep_command.py` asserts each of these and both `allowed-tools` literals. |
| FR-023 | WC-14 "Coordinator loop" is added to `WORKER-CONTRACT.md` (section 10) and `/sc:sweep` joins the never-as-worker list; both are pinned in `tests/skills/test_worker_contract.py` (REPORT steps 1.17-1.19). | `RULE_PHRASES["WC-14"]` and the 9-entry `NEVER_AS_WORKER` pass; `sweep` absent from `UNATTENDED_COMMANDS`. |
| FR-024 | Routing registries and docs: `_POST_REFRESH_ADDITIONS`, `HOW-WE-WORK.md` "Other commands" row and "Orca coordination" bullet, its plugin byte copy, `_OTHER_COMMANDS`, user guide row, developer-guide never-as-worker copy, CHANGELOG (REPORT steps 1.20-1.24b). | `tests/recommend`, `tests/core` and `tests/commands/test_routing_plugin_parity.py` pass. |
| FR-025 | `.dev/sweeps/` is added to `.gitignore` (GQ-106). A grep on 2026-11-08 found no `sweeps` entry today. | Inside the one marked real-git test of NFR-002 [Change 22]: with a copy of the repository's `.gitignore`, `git check-ignore .dev/sweeps/x.md` succeeds; `git check-ignore .dev/tasks/to-do/x.md` fails (the path is not ignored) [V2:93; Change 35]; writing a file under `.dev/sweeps/` leaves `git status --porcelain` unchanged. |
| FR-026 | Orca result classes. Every `_orca` result is classified once as `ok`, `no_binding`, `unavailable` or `call_failed`, as section 8 states. [V3R3:32; INV-002; Change 4] Step 1.0a capture is a precondition for the result parser, because `ok` and `no_binding` require captured shapes. [Conv:273] | (1) Each unavailable cause on call one (launch `OSError`, call timeout, `runtime_unavailable` in stdout or stderr, nonzero exit, invalid response), parametrized [V1R3:23]; (2) a middle `worker-show` exit 1 in a 3-row Run while the other rows continue and `orca_available` stays true [V2R3:25]; (3) a later zero-exit malformed body classified `call_failed`, not `ok` or `no_binding` [V3R3:32]; (4) a fixture of the captured no-binding JSON classified `no_binding`, gated on step 1.0a [V1R3:23]; (5) an empty zero-exit `run-current` body on call one classified `unavailable`, never `no_binding` [V3R3:32]. |

## 4. Non-functional requirements

Provenance: V1 (base) + V2 + V1R3 (Changes 9, 10, 21, 22, 23, 40)

<!-- Source: Base (original, modified) per Changes 9, 10, 21, 22, 23, 40 -->

| ID | Requirement | Acceptance criterion |
|---|---|---|
| NFR-001 | Read-only: the report file and its directory are the only filesystem change (REPORT step 1.11). | Snapshot-diff test with `HOME` and `XDG_STATE_HOME` inside the isolated root: exactly one added file (plus the `--output` dir if new). The snapshot is (path, size, mtime_ns, sha256) for every file under the root, `HOME` and the XDG dirs, including a fixture `~/.claude/`. [V2:97; Change 23] `subprocess.run`, `Popen` and `os.system` are patched to raise in every test except the one marked real-git test of NFR-002, which may run `git` only inside `tmp_path`. [V2:100; Change 22] |
| NFR-002 | Lock-free git for the sweep's own `_git` calls: every `_git` argv starts `git --no-optional-locks -C <path>` and the seam sets `GIT_OPTIONAL_LOCKS=0` in the child environment (GQ-103(1); section 8). This says nothing about Orca read verbs (section 13). [Change 7] | Recorded-argv test: every argv has `--no-optional-locks` at index 1; env test on the seam. One marked real-git test in an isolated `tmp_path` repository holds every real-git assertion in the spec [V2:98; Change 22]: (1) the control: a plain `git status` rewrites the index while `git --no-optional-locks status` does not; if the control shows no rewrite, only this assertion is reported as inconclusive; (2) with a copy of the repository's `.gitignore`, `git check-ignore .dev/sweeps/x.md` succeeds; (3) `git check-ignore .dev/tasks/to-do/x.md` fails [Change 35]; (4) writing a file under `.dev/sweeps/` leaves `git status --porcelain` unchanged. This test proves nothing about Orca read verbs. [Change 22] |
| NFR-003 | Exact allowlist: every recorded `_orca` argv equals one allowlisted template after placeholder substitution, never a prefix match (REPORT step 1.10). | Full-sweep recording test, whose expected argv[0] is `ORCA_CLI_COMMAND` if set, else `orca-ide` (section 8) [V1R3:48; Change 9], plus negative cases (`check`, `inbox`, `worker-read`, `gate-list`, extra flag) that raise `ValueError`. Git negative cases: `rev-parse`, `log`, `branch` and `--version` passed to `_git` raise `ValueError`. [Change 21] |
| NFR-004 | Pure core: `classify.py` and `report.render` import no `subprocess`, `click`, `os` or `shutil`, and do no I/O. | AST import test over both modules. |
| NFR-005 | Determinism: same `SweepInput` and same `SweepContext` give a byte-identical report and JSON. | Render twice from one fixture; assert equal bytes. The test injects `now` and the output path. [V1R3:50; INV-015; Change 10] |
| NFR-006 | No import-time side effects: `sweep/__init__.py` exports `sweep_group` lazily (REPORT step 1.1). | Importing `superclaude.cli.sweep` records no seam call. |
| NFR-007 | Bounded runtime: total probe time 90 s or less; the skill runs the Bash call with timeout 120000 ms. | FR-020 test; static check of the skill text. |
| NFR-008 | Safety over completeness over convenience (seed brief line 27): a lost or unscanned source never resolves a question, fails a session, lifts a freeze or yields a recommendation. | Source-loss fixture: affected rows are could not determine with the `unscanned:` reason. |
| NFR-009 | Schema stability: JSON carries `schema_version: 1`; a key is never removed or renamed within v1; additions only. The key set includes the row keys `class`, `rule`, `evidence`, `notes` and `safe_to_close` from the start (FR-017). [V3R3:43; Change 12] | Golden key-set test; a change to the key set fails unless `schema_version` changes. |
| NFR-010 | Rule-order stability: the class precedence is the order of `classify.RULES`, pinned by name. | Test asserts `[r.name for r in RULES]` equals the section 7 list. [Change 40] |
| NFR-011 | Installed primitives use `~/.claude/...` paths only; no `src/superclaude/` path in the command or skill (CLAUDE.md rule). | `tests/commands/test_sweep_command.py` path assertion; step 1.28 grep. |
| NFR-012 | Repo gates: `make sync-dev`, `make verify-sync`, `make lint`, `uv run ruff format --check src/ tests/` and the affected tests pass; `.claude/` never staged except `settings.json`. | CI and local run of REPORT steps 1.25-1.27. |
| NFR-013 | No live Orca, ccsession or Claude launch in tests. | Tests run with the seams patched and real subprocess entry points patched to raise (NFR-001), except the one marked real-git test of NFR-002, which may run `git` only inside `tmp_path`. [V2:100; Change 22] |

## 5. CLI contract and re-run idempotency

Provenance: V3 (new section, Change 40) + V3R3 (INV-001) + V1 (Changes 3, 12, 13, 40)

<!-- Source: Variant 3, CLI contract and re-run idempotency (V3:148-187), per Changes 3, 12, 13, 40 -->

This section holds the exit-code contract, the stdout JSON rule and the re-run rules. FR-002, FR-017, FR-018 and FR-019 point here. [V3:148; Change 40]

### 5.1 Exit codes

- Exit 0 means collection completed and the report was successfully published. Could-not-determine rows are allowed. Exit 0 includes bounded and partial observations, and Orca-unavailable observations after an explicit or established Run binding; it is never an all-clear. [V3:161-162; C-016; Change 3]
- Exit 1 means an internal error, with the `[sweep ...]` stderr prefix. It includes an argv outside the allowlist and any report write failure. A run that exits 1 prints no success JSON. [V3R3:31; Change 3]
- Exit 2 means a usage error. It includes invalid arguments, no Run binding, and Orca unavailable before a binding is established. Without `--run`, an unavailable `run-current` lookup exits 2 with `Orca unavailable; no Run binding could be established: pass --run <id>`, and a confirmed missing binding exits 2 with `no Run bound: pass --run <id>`. Neither case writes a report or success JSON. [V3R3:31; INV-001; Change 3]
- With an explicit Run, or a binding already established by a successful lookup, a later unavailable result does not change the exit code: the sweep continues disk-only and exits 0 after publication (FR-019). [V3R3:31; Change 3]

### 5.2 Stdout JSON

- Print one JSON object on stdout only after successful report publication; diagnostics use stderr. [V3:167; Change 12]
- Schema version 1, additive-only compatibility, golden key-set test (NFR-009). Required top-level keys: `schema_version`, `observed_at`, `scope`, `window`, `orca_available`, `sources`, `rows`, `waiting`, `summary`, `report_path`. [V3:169-171; Change 12]
- Absent optional values are null, never omitted; class counts include zero values. [V3:172; Change 12]
- `waiting` has `a` and `b` lists of stable session IDs, not duplicate session records. `summary` contains counts per class, `total` and `bound_reached`. [V3:174-175; Change 12]
- Each row carries the key `class`, plus `rule`, `evidence`, `notes` and `safe_to_close`; `safe_to_close` is never yes in Phase 1. [V3R3:43; Change 12]
- Markdown and JSON share the observation model. [V3R3:43; V3:177; Change 12]
- Failed publication exits 1 without success JSON or overwriting an earlier observation. [V3R3:43; Change 12]

### 5.3 Report path and re-run

- The base name is `<output>/<YYYYMMDD-HHMMSS>-sweep.md`, UTC timestamp from `SweepContext.now`. [V1:210; Change 13]
- If the name exists, add a collision suffix. [V3:181; Change 13]
- Reserve the path exclusively (create-new, never overwrite). [V3:182; Change 13]
- A sweep changes no lifecycle state and advances no cursor. [V3:179; Change 13]
- Every run that publishes a report writes a new dated file and never reuses or overwrites an earlier path; a run that exits 2 writes nothing. [Change 13, narrowed to the owner wording; see section 18]
- The report ends with the footer line `Report complete`. [V3:187; Change 13]
- This spec states no rule about files left on disk by a run that exits 1. That question is an open gap (section 18).

AC: two report-publishing sweeps with the same injected `now` produce two files (FR-017). [Change 13]

## 6. Architecture and component boundaries (A1 layout)

Provenance: V1 (base, original; renumbered from V1 section 5 per Change 40)

<!-- Source: Base (original) -->

Option A1 (REPORT line 1098): a Python CLI with a pure classifier and one probe module, called by a thin command and a protocol skill. A4 (extend `sc-crash-recovery`) is rejected because that skill allows `git stash` and has scanner bugs (REPORT line 325); a skill-only sweep is rejected because it cannot be mock-tested (K-4).

**Package layout** (six modules, matching REPORT steps 1.1 to 1.6; no seventh module):

| Module | Role | May import | Must not import |
|---|---|---|---|
| `__init__.py` | Lazy `__getattr__` export of `sweep_group`, as `cli/recommend/__init__.py:12-20` (REPORT step 1.1) | `commands` (lazily) | anything at import time |
| `models.py` | Frozen dataclasses, class-name `str` constants, `SweepContext`, `SweepInput`, `SweepResult`, `JSON_SCHEMA_VERSION = 1` | stdlib `dataclasses`, `datetime`, `pathlib` (types only) | every other sweep module |
| `classify.py` | Pure: `RULES`, `classify`, `policy_of`, `package_state`, `mark_shared_packages`, `safe_to_close`, `classify_all(SweepInput, SweepContext) -> SweepResult` | `models` | `probes`, `report`, `commands`, `subprocess`, `click`, `os` |
| `probes.py` | The two seams, `ALLOWED_ORCA`, `ALLOWED_GIT`, the call `Budget`, disk readers, `collect(ctx, runs, root) -> SweepInput` | `models`, `subprocess`, `os`, `json` | `classify`, `report`, `click` |
| `report.py` | `sanitize`, pure `render(SweepResult, SweepContext) -> str`, and `write_report(text, output_dir, now) -> Path`, the package's only write | `models` | `probes`, `classify`, `subprocess`, `click` |
| `commands.py` | Click group `sweep`, subcommand `run`: parse options, build `SweepContext`, call `collect`, `classify_all`, `render`, `write_report`, echo JSON | all of the above, `click`, `json` | nothing extra |

**Data flow.** `commands` builds `SweepContext(now, window, window_start, root, runs)` once. `probes.collect` returns a `SweepInput`: raw observations only, no derived class. `classify.classify_all` turns it into a `SweepResult` (rows with class, policy and safe-to-close; worktrees with package states and shared flags). `report.render` and the JSON builder both read only `SweepResult`. This three-stage split is the maintainability core: every behaviour except the seams is a pure function of two frozen values, so every test in `tests/sweep/` except the seam and read-only tests builds a `SweepInput` directly from fixtures.

**Boundary rules (pinned by tests).**

- B1. Dependency direction is one way: `commands -> {probes, classify, report} -> models`. An AST import test fails on any other edge (extends NFR-004).
- B2. `classify` and `render` never see a `Path` they could open: paths are data only.
- B3. The read allowlist lives only in `probes.py`. A later phase that writes (Phase 2 `/sc:close`) gets its own package, its own write seam and its own allowlist; it may import `sweep.models`, `sweep.classify` and `sweep.probes.collect`, and must re-collect before any action rather than trust a stored report or JSON (FR-021).
- B4. Command and skill are thin: all logic sits in the CLI; the skill only runs the CLI, reads the report path from JSON and summarises it. No classification text is duplicated in Markdown primitives.
- B5. `superclaude.contracts` names are not re-declared under `src/superclaude/cli/` (lint Check 11, REPORT line 1227).

**Extension points fixed now (shape only, no extra code).**

| Point | Where | How a later phase extends it |
|---|---|---|
| Rule table | `classify.RULES: tuple[Rule, ...]` | Insert a named rule at a stated position; NFR-010 makes the reorder visible in review |
| Read allowlist | `probes.ALLOWED_ORCA: tuple[ArgvTemplate, ...]` | Add one template after a recorded read-only probe (REPORT step 1.0a method); never a write verb (FR-021) |
| Sources | `SourceCoverage` rows built by `collect` | A new source adds one coverage row; the report header lists it with no renderer change |
| Machine output | JSON `schema_version: 1` | Additive keys only; Phase 2, 5 and 6 consume it |

## 7. Data model and classification states

Provenance: V1 (base) + V2 + V3 + V3R3 (INV-003, INV-006, INV-007) (Changes 5, 6, 10, 12, 30, 31, 32, 33, 41)

<!-- Source: Base (original, modified) per Changes 5, 6, 10, 12, 30-33, 41 -->

All types are frozen dataclasses in `models.py`. Class and state names are plain `str` constants (printed as they are), collected in tuples, as REPORT step 1.2 decides. Fields added by this spec for GQ-103(3) are marked (new).

- `SweepContext`: `now: datetime` (UTC, injected), `window: timedelta`, `window_start: datetime`, `root: Path`, `runs: tuple[str, ...]`.
- `OrcaObservation`: `liveness_verdict` (`live`, `unverifiable`, `exited` or None), `status`, `outcome`, `agent_wait: object | None`, `agent_wait_present: bool` (null versus absent, GQ-58), `parent`, `worktree_path`, `body_text`, `unsupervised: bool | None`, `terminal_state`, `next_action`, `worker_done_seen: bool | None` (new), `fenced_evidence: str` (new; `present`, `absent` or `unreadable`; always `unreadable` on live rows in Phase 1, REPORT step 1.3 rule 3), `task_spec_text: str | None` (new; source of the gate policy line).
- `worker_done_seen` is None on live rows, because no named live source establishes its absence. Stalled (proved) stays fixture-only until a source mapping exists. Missing proof never becomes False. [V1R3:41, V2R3:43, V3R3:52; INV-006; Change 10]
- The parser reads only the `worker-show` fields this model needs and ignores the others; an unknown field is not an error (section 11, unknown schema field row). [V2:63; Change 41]
- `ContractRecord`: `path`, `worker_status`, `blocked_question`, `reason`, `report_path: Path | None` (new), `artifacts: tuple[Path, ...]` (new), `command: str | None` (new).
- `SessionRow`: `id`, `person_started: bool | None` (True, False or None, FR-010) [V3R3:33; INV-003; Change 5], `orca: OrcaObservation | None`, `contract: ContractRecord | None`, `transcript_path`, `transcript_readable: bool | None` (new), `last_activity: datetime | None`, `gate_policy: str | None` (new; `report blocked`, `ask the coordinator`, or None when the spec cannot be read), and the ten #409 dimensions defaulting to `unknown` (REPORT step 1.2).
- `PackageRecord` (new): `id`, `location` (`to-do`, `done`, `both`), `has_final_line: bool | None`, `archiving_marker: bool`, `active: bool | None`, `state: str` (set by `classify.package_state`).
- `WorktreeState`: `path`, `status_read: bool`, `uncommitted`, `unpushed`, `dev_tasks_unsaved` (each `bool | None`, all parsed from the one status call), `changed_paths: tuple[str, ...]`, `packages: tuple[PackageRecord, ...]`, `shared_package_ids: tuple[str, ...]`, `frozen: bool | None`.
- `Classification`: the class name (emitted as the JSON row key `class`), `waiting_kind` (`a`, `b` or None), `rule: str` (new; name of the rule that matched, printed in JSON for audit), `evidence` (the field and source behind the class, printed in JSON and in the report's ledger rows) [V2:139-141; Change 12], `notes`.
- `SafeToClose`: `terminal`, `worktree` (each `yes`, `no`, `could not determine`), `reason`.
- `SourceCoverage`: `name`, `coverage`, `age_seconds`, `unscanned`.

**Session classes and precedence.** `classify` walks `RULES` in order; the first rule that returns a value wins. Policy (frozen or not) is computed separately by `policy_of` for every row (GQ-96: dimensions are independent).

| Order | Rule name | Class | Condition (REPORT step 1.3) |
|---|---|---|---|
| 1 | `blocked_contract` | waiting on a person (a) | Contract `worker_status: blocked` and rule 1's condition: Orca row settled, or `gate_policy == "report blocked"`, or a Ruling halt (`E-HALT-QA`, `E-NO-RULING`). Under `ask the coordinator` on a live unsettled row the rule declines and adds note "blocked contract under ask the coordinator; may be re-running"; with `gate_policy` None on a live row it returns could not determine with that note |
| 2 | `orca_exit_proof` | stalled (proved) | Matches only `liveness_verdict == "exited"`, `worker_done_seen is False` and `fenced_evidence == "absent"`. Otherwise it declines (no match); on an exited row whose fencing evidence is not readable (`fenced_evidence == "unreadable"` or `transcript_readable is False`) it attaches the note `Orca: exited; fenced evidence not readable` (GQ-84) for later rules. Later rules may use their own sufficient evidence. Only the final fallback returns could not determine when none matches. [V1R3:42, V3R3:53; INV-007; Change 6] |
| 3 | `fenced` | fenced | `fenced_evidence == "present"` (synthetic fixtures only in Phase 1) |
| 4 | `waiting_signal` | waiting on a person (a) or (b) | (a) non-null `agent_wait`; (b) frozen plan from a `failed` contract with a STOP code other than `E-RESUME-NEEDED`, or a ready Task (creator: could not determine), labelled for ownership review [V3:226; Change 32] |
| 5 | `working` | working | `live`, `in_progress`, `agent_wait_present` and null |
| 6 | `finished` | finished | Settled outcome and a parsed contract (`succeeded`, `partial` with note "partial: usable not yet judged", `failed`), or a `guard refused:` body. Finished never means admitted. [V3:228-229; Change 31] |
| 7 | `idle` | idle | `person_started is True` [Change 5] and `last_activity < window_start` within Historical rules; the transcript must be readable and the timestamp known; never for an open Task, an explicit wait or an unread-report candidate [V3:93, V3:234-237; Change 33]; never for an Orca row, never for a just-dispatched worker |
| 8 | `fallback` | could not determine | Everything else, including `unverifiable`, absent `agentWait` on an unsettled row, a context-only Dispatch, an active person session (note "person session, active"), and a `person_started` of None (FR-010) [Change 5] |

AC for rule 6: a finished row's JSON and report text never say admitted or accepted. [Change 31]

The REPORT numbers idle outside 1-7; this spec places it as rule 7 and the fallback as rule 8 so the table is total and ordered. Cross-cutting notes: non-null `parent` adds "WC-13 violation, review" (GQ-40). Never inputs to the class: `projection.stage.activity` and `resource.terminalState` (REPORT step 1.3).

**Package states** (precedence top to bottom, first match wins; read by `package_state`):

| State | Condition | Blocks worktree removal |
|---|---|---|
| `conflict` | Same id in `to-do/` and `done/` (GQ-102) | yes |
| `interrupted-archive` | `.archiving` marker present (checked with `os.stat`, never cleared) | yes, listed under Retained problems |
| `archive-blocked` | In `to-do/` and `progress.md` has a `FINAL:` line (GQ-105) | yes, printed in Package state column [V2:160-168; Change 30] |
| `unfinished` | In `to-do/`, ledger read, no `FINAL:` line | yes (refusal condition 4, `WORKER-CONTRACT.md:108`) |
| `archived` | In `done/` only | no |
| `unknown` | Ledger unreadable | prints could not determine |

**Safe-to-close.** Terminal releasable needs `terminal_state == "reclaimable"`, `next_action == "release"` and the result already read; the read is not observable, so Phase 1 prints `could not determine (result read not observable)` plus the Orca values; `retained` is never releasable. Worktree removable prints `no` with the first observed condition from FR-013, else `could not determine (report read, open PR and unmerged commits not observable)`.

## 8. Probe seams and argv allowlist

Provenance: V1 (base) + V1R3 + V2 + V2R3 + V3 + V3R3 (INV-002, INV-005, INV-017) (Changes 4, 7, 9, 11, 21, 24, 27, 32, 41)

<!-- Source: Base (original, modified) per Changes 4, 7, 9, 11, 21, 24, 27, 32, 41 -->

**Seams** (REPORT step 1.4). Both live in `probes.py`; nothing else in the package calls `subprocess`.

- `_orca` runs `[<binary>, *args]`, where `<binary>` is `ORCA_CLI_COMMAND` if set, else `orca-ide`. This is a deliberate safety deviation from orca-cli SKILL.md:27, which selects bare `orca` inside Orca-managed terminals; the sweep cannot reliably tell it is in one, and bare `orca` outside one starts the GNOME screen reader (SKILL.md:24-26). The resolved binary name is recorded in the report header (section 9). [V1R3:48, V2R3:49; INV-017; Change 9]
- `_git(cwd, *args) -> str` builds `["git", "--no-optional-locks", "-C", str(cwd), *args]` itself and passes `env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}`. A caller passes only the subcommand, so no call site can omit the flag. This is the first item built and the first test written (GQ-103(1)).
- Both use `subprocess.run(argv, capture_output=True, check=True, text=True, timeout=<per-call timeout>)`, check the argv against the allowlist before running, and raise. An argv outside the allowlist raises `ValueError` (exit 1, a bug, not a source loss). [Change 24 for the timeout]
- Orca result classes [V3R3:32; INV-002; Change 4]: Classify each `_orca` result once as `ok`, `no_binding`, `unavailable` or `call_failed`. First apply the unavailable checks: launch `OSError`, call timeout, or `runtime_unavailable` in stdout or stderr. Also treat nonzero exit or invalid response on the first Orca call as unavailable. Stop further Orca calls after unavailable. A later nonzero exit or invalid response without those unavailable signals is `call_failed`: mark that source or row unscanned, preserve its failure reason, leave dependent evidence unknown, and continue independent reads within budget. Invalid response includes empty or unparseable stdout and JSON that cannot establish the operation's captured success or no-binding shape. `no_binding` applies only to zero-exit `run-current` with the captured explicit no-binding shape, never to an empty body, arbitrary null or a missing field guessed to mean no binding. Those shapes remain UNVERIFIED until step 1.0a. `ok` requires the captured success shape. Use `orca call failed (exit <n>)` for nonzero exit and `orca call failed (invalid response)` for response failure, retaining the actual exit separately. An earlier successful call plus a later `call_failed` does not prove global runtime health; per-source failures remain visible even when `orca_available` stays true.
- Step 1.0a capture is a precondition for the result parser, because `ok` and `no_binding` require captured shapes. [Conv:273; Change 4]
- A launch failure because the binary is missing is an `unavailable` result with reason `binary not found: orca-ide` (or the `ORCA_CLI_COMMAND` value). [Change 9]
- A `Budget` object (50 `worker-show`, 90 s total) is passed into `collect`, never global, so tests set it per case. Each call's timeout is the lesser of 10 s and the remaining total budget. Proposed byte limits: 1 MiB per contract or ledger read, 256 KiB transcript tail, 8 MiB subprocess output; proposed, rationale required before release. A read that hits a limit marks that source unscanned with a reason. [V3:124-125, V3:137; Change 24]

Why lock-free git: WC-9 at `WORKER-CONTRACT.md:44` says a worker that finds `index.lock` in its worktree reports `blocked` with the path. A plain `git status` may refresh the index and take that lock, so a sweep whose own `_git` call lacked the flag could block a live worker. [Change 7] `--no-optional-locks` is in REPORT step 1.4 via GQ-103(1); the `GIT_OPTIONAL_LOCKS` variable is from git's own documentation, not from a repo file (UNVERIFIED here), and is kept as belt and braces. These safeguards cover the sweep's own `_git` calls only; whether Orca read verbs take optional git locks is the accepted risk in section 13. [V3R3:34; Change 7]

**Orca allowlist** (exact templates; `<run>` and `<dispatch>` must match an id regex fixed after the step 1.0a capture, UNVERIFIED shape today):

| Template | Purpose |
|---|---|
| `orchestration run-current` | Default Run binding (FR-002) |
| `orchestration worker-list --run <run> --json` | Rows, 100 per page; see the paging requirements below [Change 11] |
| `orchestration worker-show --dispatch <dispatch> --json` | Per-row detail, bounded at 50 (GQ-01) |
| `orchestration task-list --ready --run <run> --json` | Ready Task needing ownership review, rule 4 (b) (`WORKER-CONTRACT.md:129`) [Change 32] |
| `orchestration task-list --run <run> --json` | Task spec text for the gate policy line (GQ-103(3)) |
| `worktree ps --json` | Worktree discovery and `agentWait` (no `--agent-wait` filter) |

**`worker-list` paging and row identity** [V3R3:42, Conv:263, V2:63, V3:63, V3:274; Change 11]:

- Deduplicate Dispatch IDs and canonical roots.
- Retain every discovered row; unenriched rows above the 50-show cap are marked unknown.
- Unseen rows are not counted as known omissions.
- Duplicate Dispatch rows with contradictory state are kept as one identity with a conflict reason. [V3:63; U-026]
- The cursor template is admitted only after the step 1.0a capture, as one extra template. Until then the sweep makes one list call per Run, and a full 100-row page sets `truncated` and prints `Orca rows: 100 shown; total is a lower bound (paging not yet captured)`.
- Gated AC: once the cursor template exists, a 101-row fixture makes two list calls and at most 50 show calls. Until then, a 100-row fixture sets `truncated` and prints the lower-bound line.

Removed from the research allowlist by GQ-109: `gate-list`, `worker-read` (it consumes messages), and any `git stash` form. `run-list` is removed by GQ-104. `--include-remote` and `gh` are Phase 2 or later. Whether every template above takes `--json` exactly as written is UNVERIFIED and is the first thing the step 1.0a capture checks; a template that fails the capture is dropped, and its rows print could not determine.

**Git allowlist** (subcommand part only; the seam adds the prefix). `ALLOWED_GIT` holds exactly one template, so the full argv is `git --no-optional-locks -C <path> status --porcelain --branch`. [V2:203; X-004; Change 21]

| Template | Purpose |
|---|---|
| `status --porcelain --branch` | One call per worktree answers uncommitted, untracked, ahead/no-upstream, `.dev/tasks/` unsaved and active-package paths (GQ-110, GQ-101) |

The default `--root` comes from the path walk in FR-004, not from git. [Change 21] No `git log`, `git branch`, `git rev-parse`, `git --version`, `git stash list` or `git worktree list`. [Change 21] Unmerged commits and open PRs are not observed in Phase 1; that is acceptable because worktree removable is never `yes` (FR-012).

**Disk reads** (no seam needed, `os.stat` and open-for-read only): package `progress.md` and `.archiving` markers under `<worktree>/.dev/tasks/{to-do,done}/`, worker contract records named by the Orca row, transcripts under the scanned project keys, and the ccsession tab map. Each reader records a `SourceCoverage` row and never raises past `collect`. Disk discovery uses fixed patterns only, never a recursive walk. Every resolved path is checked with `resolve()` to stay inside its allowed root, and an escaping symlink is rejected and reported. ccsession files are read directly, never through `ccsession --list`. AC: the F9 symlink-escape fixture (section 11). [V2:64, V2:247, V3:288-292; Change 27]

## 9. Report format

Provenance: V1 (base) + V2 + V3 + V1R3 + V3R3 (INV-004, INV-005, INV-008, INV-017) (Changes 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 32)

<!-- Source: Base (original, modified) per Changes 7-15, 18, 32 -->

The layout copies the sections this research chose from #409 at `495eb96d` (header, Attention Ledger, Shift Brief; REPORT line 328) into the design, citing the commit, because #409 is unmerged. The renderer is one pure function per section, called in a fixed order from a tuple `SECTIONS`, so a later phase adds a section by appending one function (the same table pattern as `RULES`). The `SECTIONS` tuple holds the sections in the order below. [Change 14]

**File:** the path and re-run rules are in section 5.3. [Change 13]

**Header block:**

```text
READ ONLY . observed <UTC ISO time> . collected <start> to <end> (not an atomic runtime snapshot)
Scope: Runs <ids> . worktrees <n> . sessions <shown>/<total> . window <6h>
Orca binary: <resolved binary name>
Sources: <name> <coverage> (age <s>s) . ...   [one entry per SourceCoverage]
Messages coverage: partial
Orca read verbs' git effects on worker worktrees: UNVERIFIED
Untracked paths: hidden when status.showUntrackedFiles=no is set; absent untracked output is not proof that no package is active
```

- "Messages coverage: partial" is fixed text in Phase 1, because there is no non-consuming read of pending questions (GQ-02).
- The collection interval line states that the report is not an atomic runtime snapshot. [V3:15, V3:197, V3:298; Change 14]
- `Orca binary:` records the resolved binary name. [Change 9]
- The `Orca read verbs' git effects on worker worktrees: UNVERIFIED` line is always printed (section 13). [V3R3:34; Change 7]
- The untracked-paths line is the INV-008 named limitation (section 14). [V1R3:43, V3R3:54; Change 8]
- Whenever worktree discovery is incomplete, with or without `--run`, the header adds `child worktrees not discovered: Orca unavailable; worktree count is a lower bound`. [V1R3:40, V3R3:51; INV-004; Change 10]
- When the `worker-show` cap is reached, the header says so and the row total is a lower bound (FR-020). [A-107; Change 11]
- A full 100-row `worker-list` page adds `Orca rows: 100 shown; total is a lower bound (paging not yet captured)` (section 8). [Change 11]

**Sections, in order** [V2:207-217, V3:297-307; Change 14]:

1. Header (above).
2. `## Source coverage`: one row per `SourceCoverage`, with any `unscanned:` reason. [V3:297]
3. `## Waiting on a person (a)`: table `| ID | Age | Question | Requested by | Decision owner | Affected | Evidence |`, oldest first, then "unknown age". Under it: "Seen is not resolved" and "Answered: could not determine".
4. `## Waiting on a person (b)`: blocked by policy (frozen plan, a ready Task needing ownership review [Change 32]); no question text, the policy reason and evidence only.
5. `## Could not determine`: placed before working rows because an unknown can hide a person-wait. [V2:211]
6. `## Retained problems`: interrupted archives, conflict packages, shared active packages, WC-13 violations, call bound reached.
7. `## Sessions (<shown>/<total>)`: one row per session with the ten #409 dimensions, class, rule name, evidence [Change 12], safe-to-close (terminal, worktree), notes and a `next inspection` column. [V3:303; Change 15] The `next inspection` value is an inspection step only (what to read or check next), never a stop, retry, release, merge or removal. [V3:316; Change 15]
8. `## Worktrees`: path, uncommitted, unpushed, `.dev/tasks/` unsaved, Package state column, removable with reason.
9. `## Historical sessions`: person-started sessions with no activity inside the window (GQ-108).
10. `## Shift Brief`. [V3:306]
11. `## What I could not determine`. [V3:307]
12. Footer: "Inspection only." followed by the source list, then the final line `Report complete`. [V3:187; Change 13]

AC: the FR-011 heading-order test checks this order. [Change 14] AC: every Sessions row has a non-empty `next inspection` cell, and no cell contains stop, retry, release, merge or removal. [Change 15] AC: no rendered text in the fixture reports proposes a stop, retry, release, merge or removal. [V3:105; Change 18]

**Fixed strings:** an empty section prints "No matching records. This is not an all-clear."; any count over sessions prints "Distinct affected sessions: <N> (set union, not a sum)". The report holds no action controls, commands to paste, or advice to delete anything under `.dev/tasks/` (seed brief constraint).

**Stdout JSON (schema v1):** `schema_version`, `observed_at`, `scope`, `window`, `orca_available`, `sources`, `rows`, `waiting` (`a`, `b`), `summary` (count per class including zero counts, `bound_reached`, `total`), `report_path`. Each row carries `class`, `rule`, `evidence`, `notes` and `safe_to_close`. [Change 12] Every key is always present (null or empty when unknown). The full stdout rule is section 5.2. The skill reads only `report_path` and `summary`; Phases 2, 5 and 6 read `rows`.

## 10. WC-14 contract rule text (proposal)

Provenance: V1 (base) + V2 + V3 + V3R3 (INV-011, INV-012, INV-013) (Changes 7, 16, 17, 18, 19, 20, 32; renumbered from V1 section 9 per Change 40)

<!-- Source: Base (original, modified) per Changes 7, 16-20, 32, 40 -->

Placement: a new subsection after the fan-in rule at `WORKER-CONTRACT.md:156` and before `### Worked example` at `:158`. WC-14 is the next free ID (REPORT line 70). This text adapts the REPORT step 1.17 draft (G1 to G7) and is a proposal for GQ-04; the owner's GQ-11 answer is a hard gate before steps 1.17 to 1.19 are written.

The rule text is presented as a fenced Markdown block under its own heading. [V2:225-229; S-013; Change 16]

```markdown
### WC-14. Coordinator loop

The coordinator keeps watching its Run until every Task it created is settled and every result has been inspected and its admission or rejection recorded. It never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it. On every coordinator wake, the coordinator runs `/sc:sweep` and reads its report before it acts. It sweeps on every wake and keeps a periodic sweep scheduled while work remains. Phase 1 adds this duty, not a scheduler. The sweep's classes follow WC-10: only Orca's stall proofs make a worker stalled; anything else it cannot prove is could not determine. A missing heartbeat is absence, never death. The coordinator escalates to the person, and does not act alone, on: a failed or blocked result it cannot retry under WC-6, a partial result it judges unusable, a third brief-guard refusal, a ready Task it did not create, needing ownership review, a frozen plan, and a fan-in with fewer than 2 admitted inputs. Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged. The sweep report is a dated local file; it is never posted. The sweep recommends nothing: no stop, retry, release, merge or removal. The coordinator decides and performs any action under those rules.
```

Sources of the changed sentences: end condition and "It never stops watching on its own." [V3:324-325, V3R3:44; Change 16]; periodic sweep duty [V3:326-328; Change 17]; "Phase 1 adds this duty, not a scheduler." and the heartbeat sentence [V3:328-329; Change 19]; "a ready Task it did not create, needing ownership review" [V3:226, V3:301; Change 32]; "recommends nothing" with the verb list [V3:335, V1:240; Change 18]. The text holds no lock sentence; if one is added later, it is only "The sweep's own git reads do not take git's optional locks." [V2R3:27; Change 7, Change 19]

Choices in this text:

- The closing sentence takes the "recommends nothing" position (open owner decision 98b), with the verb list. It keeps the read/write split of section 6 in the contract itself: the classifier never becomes an actor, so Phase 2 cannot grow a "recommended action" column that a worker would read as an instruction. [Change 18; Change 40]
- "On every coordinator wake" ties the sweep to events the contract already has. A periodic sweep is a coordinator duty while work remains; Phase 1 sets no cadence and adds no scheduler. See section 16 and the INV-011 warning in section 14. [V3:326-328; Change 17]
- `/sc:sweep` joins the never-as-worker list (9 entries); the sweep stays out of `UNATTENDED_COMMANDS`.

**Pins** (`tests/skills/test_worker_contract.py`): `RULE_PHRASES["WC-14"] = ("WC-14", ["WC-14. Coordinator loop", "On every coordinator wake", "it is never posted", "It never stops watching on its own"])` [Change 16]; `NEVER_AS_WORKER` grows to 9; rename `test_never_as_worker_list_names_all_seven_commands` to `test_never_as_worker_list_names_every_listed_command` so the next addition does not need a rename. The pin test must match the final wording exactly.

**Sequencing:** new package, command, skill and docs first; verify current overlap with PR #422 before editing the contract. If #422 merges first, rebase this PR accordingly. WC-14 and its contract pins remain deliverables of this PR even if #422 stalls; no follow-up-PR escape from done. This states sequencing, not a claim about #422's current status. [V3R3:45, Conv:266; INV-013; Change 20]

Owner approval of this shared contract text remains required. [Change 16]

## 11. Failure modes

Provenance: V1 (base) + V2 + V3 + V3R3 (INV-001, INV-002, INV-005, INV-017) (Changes 3, 4, 7, 9, 29; renumbered from V1 section 10 per Change 40)

<!-- Source: Base (original, modified) per Changes 3, 4, 7, 9, 29, 40 -->

Each mode has a fixture in `tests/sweep/`. "CND" means could not determine. The Test column names the acceptance criterion or fixture that proves the behaviour. [V2:235-237; S-007; Change 29]

| Mode | Detection | Behaviour | Exit | Test |
|---|---|---|---|---|
| Orca unavailable before a binding [Change 3] | No `--run`, and the first `_orca` call (`run-current`) gives an `unavailable` result (section 8) | `Orca unavailable; no Run binding could be established: pass --run <id>` on stderr; no report, no success JSON (FR-002, FR-019) [V3R3:31] | 2 | FR-002 test (1) |
| Orca unavailable after an explicit or established binding [Change 3] | `unavailable` result on call one with `--run`, or on a later call after a successful binding | `Orca unavailable` banner and `orca_available: false`; no more `_orca`; collected evidence retained; disk-only discovery from `--root` fixed patterns; remaining Orca sources `unscanned: orca unavailable` (FR-019) [V3R3:31] | 0, after publication | FR-002 tests (2) and (3) |
| Empty `run-current` body [Change 3; Change 4] | Zero-exit `run-current` with empty stdout on call one | Invalid response, so `unavailable`, never `no_binding`; without `--run` it exits 2 with the Orca-unavailable message and writes no report [V3R3:31, V3R3:32] | 2 | FR-026 test (5) |
| No Run bound | Zero-exit `run-current` with the captured no-binding shape (UNVERIFIED until step 1.0a) and no `--run` [Change 3] | `no Run bound: pass --run <id>`, no report, no success JSON (FR-002) [Change 3] | 2 | FR-002 test (4), gated on step 1.0a |
| Orca binary not found [Change 9] | Launch `OSError` because the resolved binary is missing | `unavailable` with reason `binary not found: orca-ide` (or the `ORCA_CLI_COMMAND` value); then as the two Orca-unavailable rows above (see section 14, INV-017) | 2 without `--run`; 0 with a binding, after publication | FR-026 test (1), launch `OSError` case |
| Orca call failed on one row [Change 4] | A later nonzero exit or invalid response without an unavailable signal | `call_failed`: that source or row unscanned with `orca call failed (exit <n>)` or `orca call failed (invalid response)`; dependent evidence unknown; independent reads continue; `orca_available` stays true [V3R3:32] | 0, after publication | FR-026 tests (2) and (3) |
| Worktree removed mid-sweep | `_git` raises `CalledProcessError` or path gone at `os.stat` | That worktree row CND, `unscanned: worktree not readable`; others continue | 0 | Fixture deletes the directory between the two seams [V2:240] |
| Live worker holds `index.lock` | Not detected; avoided | The sweep's own `_git` calls never take it (NFR-002); Orca read verbs' effect is UNVERIFIED (see section 13) [Change 7] | 0 | NFR-002 recorded-argv and env tests, and the marked real-git control assertion |
| Unreadable transcript or contract | `OSError` on open | `transcript_readable False`; rules 2 and 1 decline; row CND with note | 0 | Truncated-JSONL fixture and an unreadable-contract fixture [V2:241] |
| Stale list data | `liveStatus` stale, or a row in the list missing from `worker-show` | CND (WC-10); never stalled. Where list and show disagree, show wins. [V2:242] | 0 | Fixture where list and show disagree; show wins [V2:242] |
| Slow worker | Late heartbeat only | CND, never stalled (WC-10, `WORKER-CONTRACT.md:45`) | 0 | Late-heartbeat live fixture is never `stalled (proved)` [V2:243]; FR-008 fixtures |
| Call bound or time budget reached | `Budget` exhausted | Remaining rows CND, `unscanned: call bound reached` (FR-020) | 0 | FR-020 60-row fixture |
| Unknown row schema field | Key missing in JSON | Field stays `unknown`; no exception | 0 | Fixture with one missing and one extra `worker-show` key (section 7 parser rule) |
| Allowlist miss | `ValueError` from the seam | `[sweep ...]` stderr, no success JSON [Change 13, see section 18] | 1 | NFR-003 negative cases; FR-021 `worker-read` negative test |
| Output dir not writable | `OSError` in `write_report` | `[sweep ...]` stderr; no success JSON; earlier reports are never overwritten [Change 3; V3R3:43] | 1 | FR-017 failed-write AC |
| Malicious text in a field | Control, pipe, bidi or HTML characters | `sanitize()` (FR-016) | 0 | FR-016 injection fixture |
| Symlink leads outside the root [V2:247; Change 29] | `resolve()` check on a discovered path | Escaping symlink rejected and reported; that source unscanned | 0 | F9 symlink-out fixture |
| Input changed during reading [V3:353; Change 29] | A file changes between two reads of one source | One plain re-read within budget; otherwise the row carries a conflict reason (inconsistent observation) | 0 | Fixture that changes a contract between two reads |
| Duplicate Dispatch with contradictory state [V3:354; Change 29] | Same Dispatch ID twice with different state | One identity with a conflict reason; no last-row-wins classification | 0 | Duplicate-Dispatch fixture (section 8 paging rules) |
| Process killed during output [V3:357; Change 29] | Report file without the `Report complete` footer | No partial report is presented as complete, because the footer is missing; the next sweep uses a new path (section 5.3) | none (process killed) | FR-011 heading-order test checks that `Report complete` is the last line; FR-017 AC that an existing file is never overwritten |
| Remote host not covered [V3:358; Change 29] | Sessions on a remote host are outside the scanned sources | CND coverage: unknown coverage and a lower-bound session count are printed, never "no sessions" | 0 | Remote-coverage fixture checks the Source coverage row and the lower-bound count |

## 12. Risks and mitigations

Provenance: V1 (base) + V2 (Changes 7, 35, 36; renumbered from V1 section 11 per Change 40)

<!-- Source: Base (original, modified) per Changes 7, 35, 36, 40 -->

The impact ratings are added by this merge; V1 rated likelihood only [V2:253; Change 36].

| Risk | Likelihood / impact | Mitigation |
|---|---|---|
| R1. The real `worker-list` and `worker-show` schema differs from the fixtures (GQ-01) | High / high | Step 1.0a capture before step 1.2; models keep every field optional; unknown stays unknown; fixtures regenerated from the capture |
| R2. "Waiting on a person" missed because questions cannot be read without consuming them (GQ-02) | High / high | `blocked_question` plus non-null `agentWait` as stand-ins; fixed "Messages coverage: partial" header so the gap is visible |
| R3. A sweep disturbs a live worker | Low for the sweep's own `_git` calls after NFR-002; Orca read verbs UNVERIFIED (section 13) / high [Change 7] | Seam-built `--no-optional-locks`, exact allowlist, forbidden-verb test, snapshot-diff test. These cover the sweep's own `_git` calls only; the Orca read verbs are an accepted risk in section 13 [Change 7] |
| R4. Rule precedence drifts as later phases add rules | Medium / medium | Named `RULES` tuple pinned by NFR-010; each rule has its own test; insertion position must be justified in the PR |
| R5. Phase 2 reuses the read seam to write | Medium / high | B3 plus FR-021: write verbs live in another package with its own seam; static test on `ALLOWED_ORCA` |
| R6. Consumers break on JSON changes | Medium / medium | `schema_version` and the golden key-set test (NFR-009) |
| R7. The coordinator reads "finished" as "safe to delete" | Medium / high | Safe-to-close is a separate field; worktree never `yes`; no deletion advice for `.dev/tasks/` |
| R8. Contract wording conflicts with PR #422 | Medium / medium | Step 1.16a sequencing as OQ-6 states it (section 16); WC-14 stays a deliverable of this PR [Change 20] |
| R9. Six modules grow into one large classifier file | Medium / low | One function per rule and per report section; the dependency test (B1) keeps them apart |
| R10. The report file dirties the worktree and shows up in `git status` [V2:262; Change 35] | Certain without FR-025 / low | FR-025's `.dev/sweeps/` ignore line, checked in both directions inside the one marked real-git test. Without it, the sweep reports its own previous report as an uncommitted change, so every second sweep reports a problem the sweep created [V2:262, V2:265] |

## 13. Accepted risks needing owner sign-off

Provenance: V1R3:25 + V2R3:27 + V3R3:34 (INV-005) (Change 7; new section per Change 40)

<!-- Source: V3R3:34 risk statement, inserted per Changes 7 and 40 -->

This section holds one accepted risk. It is not a requirement, and no requirement in this spec depends on it being resolved. Nothing here is a mitigation for `_orca`.

### INV-005. Orca read verbs and optional git locks

Risk statement [V3R3:34]:

> Whether Orca read verbs take optional git locks inside worker worktrees is UNVERIFIED. If they do, the sweep can disturb a live worker despite its direct `_git` safeguards. All lock-free claims are scoped to the sweep's own `_git` calls. The report states `Orca read verbs' git effects on worker worktrees: UNVERIFIED`. JSON-shape capture and mock argv tests do not prove the indirect effects safe. Owner sign-off on this residual risk is required before Phase 1 release; absent sign-off, the risk remains a blocker, not an approval inferred from debate agreement. An owner may commission separate verification outside this work, which authorizes no live launch.

Owner sign-off: not recorded.

## 14. Open warnings

Provenance: V1R3 + V2R3 + V3R3 (INV-008, INV-011, INV-017) (Change 8; new section per Change 40)

<!-- Source: Round 3 texts, inserted per Changes 8 and 40 -->

Each entry is an open MEDIUM warning. The partial text the variants agreed is applied in the body of this spec; what remains open is stated here.

### INV-008. Untracked paths and the fixed status template

The fixed status template can miss untracked paths. With `status.showUntrackedFiles=no` set, untracked paths are hidden; this is a named report limitation. A reported untracked package directory (one `?? .dev/tasks/to-do/<id>/` line) counts as package activity. Absent untracked output is not proof that no package is active. `--untracked-files=normal` is a candidate for separate verification, UNVERIFIED, and not part of this spec.

Applied in the body: the limitation line in the section 9 coverage header and the untracked-directory rule in FR-015.

### INV-011. Sweep cadence

The pin "It never stops watching on its own" is added (Change 16). A coordinator that sweeps rarely is not prevented, because no cadence is required in Phase 1. The 2026-11-05 owner order (re-arm after every expiry, keep a periodic sweep) is stronger than a cadence-free duty; whether a fixed cadence is needed is open.

Applied in the body: the WC-14 text in section 10 and OQ-7 in section 16.

### INV-017. Orca binary resolution

The sweep runs `ORCA_CLI_COMMAND` if set, else `orca-ide`. Whether the sweep's environment carries `ORCA_CLI_COMMAND` is UNVERIFIED. Inside an Orca-managed terminal the orca-cli skill selects bare `orca` (orca-cli SKILL.md:27), so where `orca-ide` is missing every sweep takes the outage path. That failure is visible as `binary not found: orca-ide` but not prevented.

Review 3 note: with no `--run`, a first-call unavailable result exits 2 with only `Orca unavailable; no Run binding could be established: pass --run <id>` and writes no report, so no requirement makes the `binary not found: orca-ide` visibility claim true on that path. The reason is visible in the report coverage header only when `--run` is passed (`refactor-plan-review-3.md` finding p1).

## 15. Resolution of GQ-101 to GQ-110, handling of GQ-111 to GQ-113

Provenance: V1 (base) + V2 (Change 37; renumbered from V1 section 12 per Change 40)

<!-- Source: Base (original, modified) per Changes 37, 40 -->

Source: GAPS lines 124-136. GQ-103(1) is built first, before any other probe code. The Root cause column is V2's analysis, not GAPS text [V2:269; Change 37].

| GQ | Root cause [V2:273-284] | Resolution in this spec | Where |
|---|---|---|---|
| GQ-103(1) | The sweep's own `git status` can refresh the index and take `index.lock`, triggering WC-9 in a live worker | Every `_git` argv built by the seam as `git --no-optional-locks -C <path>`, plus `GIT_OPTIONAL_LOCKS=0`; first commit and first test | NFR-002, section 8 |
| GQ-101 | Presence of a package folder was used as a proxy for "running here"; committed folders exist in every worktree | Count only packages active in a worktree (changed or untracked path inside the package folder, from the one status call); committed unchanged folders shared by every worktree are never flagged | FR-015, section 7 |
| GQ-102 | The state machine had no state for an id in both `to-do/` and `done/` | `conflict` is a package state (id in both `to-do/` and `done/`); it blocks removal and lists under Retained problems | FR-014, section 7 |
| GQ-103(2) | The window was a constant, so tests could not vary it | `SweepContext` with the window is a parameter of `classify_all` | FR-007 |
| GQ-103(3) | Precedence rules named fields the model did not have | New fields: `gate_policy` (from the Task spec), `worker_done_seen`, `transcript_readable`, `ContractRecord.report_path` and `artifacts` | section 7 |
| GQ-104 | A `run-list` fallback guessed scope, which spends the call bound on Runs the person did not ask about | No `run-list` fallback; no binding and no `--run` exits 2 | FR-002 |
| GQ-105 | Archive-blocked was not distinguishable from unfinished | `archive-blocked` = package in `to-do/` whose `progress.md` has a `FINAL:` line | FR-014 |
| GQ-106 | The output folder was not ignored and not in the rollback table | `.dev/sweeps/` in `.gitignore` and in the rollback table | FR-025, section 17 |
| GQ-107 | A pipe character in untrusted text splits a table cell | `sanitize()` escapes the pipe character | FR-016 |
| GQ-108 | Person-started sessions had no join rule and no age rule | Person-started = transcript joined to no Orca row; outside the window goes to Historical | FR-010 |
| GQ-109 | The allowlist held verbs with no consumer | `gate-list`, `worker-read` and stash removed from the allowlist | section 8, NFR-003 |
| GQ-110 | Several git calls per worktree multiplied lock exposure and runtime | One `git status --porcelain --branch` per worktree; a recorded-argv test counts them | section 8 |

GQ-111 to GQ-113 are stale citations inside the REPORT. They are carried, not fixed: the design does not edit the REPORT. Where the design needs a count it cites GAPS line 138 (113 rows, 88 open, 25 resolved), and it reads REPORT line 1537 ("Every open GQ row is cited") as covering GQ-01 to GQ-100 only.

## 16. Open questions with recommended answers

Provenance: V1 (base) + V2 + V3 + V3R3 (INV-011, INV-013) (Changes 17, 18, 20, 37; renumbered from V1 section 13 per Change 40)

<!-- Source: Base (original, modified) per Changes 17, 18, 20, 37, 40 -->

Row IDs OQ-1 onward follow V2's layout [V2:289; Change 37].

| ID | Question | Recommended answer | Why (architecture view) |
|---|---|---|---|
| OQ-1 | GQ-01: design for list plus `worker-show`, or capture the row schema first? | Both: design the models for list plus `worker-show` now, and run the step 1.0a capture before step 1.2 fixes fixtures | Optional fields cost nothing; the capture then only removes calls, it never changes a class rule |
| OQ-2 | GQ-02: what stands in for a non-consuming question read? | `blocked_question` from the contract plus non-null `agentWait`; header says "Messages coverage: partial" | No consuming verb ever enters the allowlist; the gap is shown, not hidden |
| OQ-3 | GQ-04: WC-14 wording | The section 10 text | Short, testable phrases for the pins |
| OQ-4 | #409 layout: copy or cite? | Copy the chosen sections into the design and cite `495eb96d` | An unmerged commit is not a stable dependency |
| OQ-5 | 6 h or 72 h window? | 6 h default, `--window` override; older person sessions go to Historical | Matches the issue; 72 h belongs to `sc-crash-recovery`, a different job |
| OQ-6 | PR #422 sequencing | New package, command, skill and docs first; verify current overlap with PR #422 before editing the contract. If #422 merges first, rebase this PR accordingly. WC-14 and its contract pins remain deliverables of this PR even if #422 stalls; no follow-up-PR escape from done. This states sequencing, not a claim about #422's current status. [V3R3:45; Conv:266; Change 20] | New files cannot conflict; the contract edit is the only shared surface |
| OQ-7 | Sweep cadence: wake only, or also scheduled? | WC-14 requires a sweep on every wake; a periodic sweep is a coordinator duty while work remains; Phase 1 sets no cadence and adds no scheduler [V3:326-328; V3R3:56; Change 17]. See section 14, INV-011. | The contract stays event-driven; a timer adds no new rule |
| OQ-8 | Closing sentence of WC-14 (decision 98b) | "The sweep recommends nothing: no stop, retry, release, merge or removal." [V3:335; Change 18] | Keeps the read/write split in the contract |
| OQ-9 | Package name `sc-sweep-protocol` with `name: sc:sweep-protocol` | Keep | Matches existing skill folders such as `sc-implement-protocol` (cited in `synthesis/phase7-summary.md`) |

## 17. Rollback

Provenance: V1 (base) + V3 (Change 34; renumbered from V1 section 14 per Change 40)

<!-- Source: Base (original, modified) per Changes 34, 40 -->

Phase 1 is additive, and its only runtime write is the report file, so rollback is one revert of the branch's commits as one unit (REPORT lines 1304-1320). No data migration.

| Item | Rollback |
|---|---|
| `src/superclaude/cli/sweep/` and `tests/sweep/` | Delete |
| `cli/main.py` deferred import and `add_command` lines | Remove |
| `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/`, `tests/commands/test_sweep_command.py` | Delete; run `make sync-dev` (whether it removes the `.claude/` copies is UNVERIFIED; check and delete them by hand if not, never stage them) |
| WC-14 in `WORKER-CONTRACT.md`, never-as-worker entry, `RULE_PHRASES`, `NEVER_AS_WORKER`, the test rename | Revert |
| `_POST_REFRESH_ADDITIONS` (`tests/recommend/test_routing_refresh.py:33`), `HOW-WE-WORK.md` "Other commands" row and "Orca coordination" bullet, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `_OTHER_COMMANDS` (`tests/core/test_how_we_work_routing_table.py`) | Revert together, so the byte copy stays equal |
| `docs/user-guide/commands.md`, developer guide never-as-worker copy, CHANGELOG | Revert; add a CHANGELOG revert entry |
| `.gitignore` `.dev/sweeps/` line | Keep until existing reports are dealt with, then remove (GQ-106). The ignore line is reverted only after deciding where existing reports go. [V3:427; Change 34] |
| Reports already written under `.dev/sweeps/` | Stay; they are ignored local files and the owner decides |
| `.dev/tasks/` [V3:425-431; Change 34] | Never removed: rollback removes no `.dev/tasks/` folder and no file in it |

Rollback check: `make verify-sync`, `make lint` and `uv run pytest tests/skills/test_worker_contract.py tests/recommend tests/core tests/commands` pass on the reverted tree.

### 17.1 Verification checklist

Provenance: V3 (Change 39, new subsection; the live disposable-Run check of V3:421 is left out)

<!-- Source: Variant 3 verification checklist (V3:414-423), inserted per Change 39 -->

Every item is checked with the seams mocked, except the one marked real-git test of NFR-002. No item launches a live Orca Run, ccsession or Claude session (NFR-013). [V3:414-423; Change 39]

- [ ] FR-001 to FR-026: every acceptance criterion in section 3 passes, including the step 1.0a gated cases of FR-002 test (4) and FR-026 test (4).
- [ ] NFR-001 to NFR-013: every acceptance criterion in section 4 passes, including the one marked real-git test of NFR-002.
- [ ] Section 5: the exit-code tests (one per code, FR-018), the success-JSON-after-publication tests (FR-017) and the two-files-for-one-`now` test.
- [ ] Section 11: every failure-mode row's named test passes.
- [ ] Section 10: the WC-14 pins and the 9-entry `NEVER_AS_WORKER` list pass in `tests/skills/test_worker_contract.py` (FR-023).
- [ ] NFR-012 repo gates: `make sync-dev`, `make verify-sync`, `make lint`, `uv run ruff format --check src/ tests/` and the affected tests pass; `.claude/` never staged except `settings.json`.
- [ ] Section 17 rollback check passes on a reverted tree, if a rollback is made.

Release precondition, not a test: the owner signs off on INV-005 (section 13). Until then Phase 1 is not released.

## 18. Open gaps

Provenance: merge record (Change 13 narrowed; `refactor-plan-review-3.md` finding P1) + V3 + seed brief (new section)

<!-- Source: Merge executor, recording gaps the plan and its reviews leave open -->

These gaps are not resolved by this spec. None of them is a requirement.

### G-1. Files left on disk after a run that exits 1

Section 5.3 states the owner rule: every run that publishes a report writes a new dated file and never reuses or overwrites an earlier path; a run that exits 2 writes nothing. No rule is stated for a run that exits 1. Review 3 found that the plan's added clause "a run that exits 1 or 2 writes no report" has no full source support (`refactor-plan-review-3.md` finding P1), so it is not carried. The sources point in different directions:

- V3:184: "On handled write failure, remove only this invocation's incomplete output if it can be identified safely"
- V3:356: "Output denied, full disk or partial write | Exit 1; no success JSON; preserve previous reports"
- V3:357: "Process killed during output | Partial file may remain without completion footer; next sweep uses a new path"

V1:265's allowlist-miss "no report written" is not carried as a requirement either; the section 11 allowlist-miss row states only the exit code and the absence of success JSON. What an exit-1 run leaves on disk must be decided at /sc:design.

### G-2. Seed brief open questions

The seed brief's open questions are at `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/seed-brief.md`, section "Open Questions". Section 16 gives recommended answers; the owner decides.

### G-3. GQ-101 to GQ-113 at /sc:design

GQ-101 to GQ-113 must be resolved at /sc:design, using section 15 as the proposed resolutions. GQ-103(1) comes first: `--no-optional-locks` on every `_git` call (NFR-002), before any other probe code.
