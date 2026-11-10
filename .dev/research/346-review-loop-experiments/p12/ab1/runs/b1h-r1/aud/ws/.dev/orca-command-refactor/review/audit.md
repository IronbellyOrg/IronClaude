review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md

Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit, first review, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`).

## Header
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `1a2d2f425ac57ef3f2392d0bfdf09996e8bf26606b0e7b94ee731ab5d177867d` (294 lines, 60176 bytes)
- baseline: none given, `--re-review` not given: first review of the full document
- reviewer model used: claude-sonnet-5-5
- panel (requirements + architecture focus): Wiegers (lead), Adzic, Cockburn, Fowler (lead), Newman, Hohpe, Nygard, plus Whittaker (always active; review order 6 per command)
- shared context read first: `.dev/orca-command-refactor/README.md` (sha256 `086e5b82...2069e`). Checkable evidence: `inventory/commands-a.md` (`b6e39f74...`), `inventory/commands-b.md` (`65e8be12...`), `inventory/orca-capabilities.md` (`b0d2d507...`). Notation: `S:N` = spec line N, `INV-A:N`/`INV-B:N`/`CAPS:N` as in the spec.

## Coverage
Read all 294 lines of the candidate. Checked against the inventories: the 10 / 27 / 6 split (A: 5 ready, 13 needs-change, 3 coordinator-only, `INV-A:73`; B: 5 ready, 14 needs-change, 3 coordinator-only, `INV-B:280-289`; the sums match S:76), the phase-to-command assignment (all 37 workers and 6 coordinator-only are placed, counts below), the CAPS lines behind WC-1, WC-3, WC-5, WC-10, R1 to R5 (`CAPS:44-47,52,58-80,97-103,116,129-130,145-151,155-161`), and the reflect/tasklist rows (`INV-B:109,207-215,310`). Did not cover: any `cmd/`, `sk/`, `CLAUDE.md`, `HOW-WE-WORK.md`, `src/superclaude/cli/install_core.py`, `pyproject.toml`, `Makefile`, Orca guide or `EVIDENCE.md` path:line citation. None of those files exists in this workspace; they are marked UNVERIFIED unless an inventory line quotes them. This includes the spec's own claims of a 11-location re-read (S:11) and a 340-citation re-check (S:293), and the E5 grep (S:25). The Pipeline Dimensional Analysis below was applied to the phase rollout.

Clause overridden from the brief: none.

## Grading note
Blocking findings below each carry the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." Findings that need a guess about which reading the implementer picks, or that are a requirement the document never states, are Medium and sit under follow-up candidates.

## === REQUIREMENTS ANALYSIS ===

### B-1 CRITICAL (blocking) [Wiegers, Whittaker (sequence attack), Fowler]: Phase 1 ships `--unattended` on 37 commands while the behavior it promises arrives in P2-P4
Priority High. Quality impact: breaks the safety property of the whole contract for the interval between phases.

Grading sentence: An implementer who follows the stated text as written builds, in P1, an `--unattended` flag and `## Unattended mode` section on every command in sections 3.1 and 3.2 (S:159 "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"; S:79; S:203 AC-1.1), while the gate and outward-default resolutions land only in P2 (S:160), P3 (S:161) and P4 (S:162). X is wrong because WC-2 (S:60) defines `--unattended` as "never calls AskUserQuestion, never ends its turn on a chat question" and WC-9 (S:67) turns every outward default off under it, and S:73 tells the coordinator to put `--unattended` in every brief "from Phase 1 on". After P1, `/sc:auggie-review <PR> --unattended` is accepted and still posts to GitHub by default (`cmd/auggie-review.md:51-54` via `INV-A:98`, UNVERIFIED directly; the row that fixes it is tagged P2, S:100), and `/sc:cleanup --unattended` still waits on its approval prompt (`INV-A:96`; row tagged P2, S:103). The "no-op" parenthesis at S:159 covers only commands without a gate, so the text does not say what the flag does on a command that has a gate before its phase. AC-1.1 (S:203) cannot detect it: it checks that a section exists and names `return-contract.yaml` and the contract path, not that the gate resolutions are present. S:154 ("each phase ... leaves standalone behaviour unchanged") says nothing about this window, and S:154 also says later phases do not start until earlier checks pass, so the window is the intended end state of P1.

State trace (Whittaker, FR-2.4 sequence attack): I can break this specification by **Sequence Attack**. The invariant at **S:60 / S:67** (under `--unattended` no prompt, no outward default) fails when **a coordinator follows S:73 after P1 merges but before P2**. Concrete attack: before, auggie-review has `--no-post-pr` default off and no `--unattended`; P1 adds `--unattended` as accepted-but-no-op; coordinator brief `/sc:auggie-review 123 --unattended --output d/`; after, the worker posts a PR review and ends its turn on the plain-chat remediation offer (`INV-A:62`), so there is an outward action and a silent stall with no `worker_done`, the exact failure the spec names as the real one (S:44).

Pipeline Dimensional Analysis (FR-19, a count mismatch is CRITICAL): N = 37 commands receive the flag in P1 (S:159); M = 15 have their gate behavior fixed at the end of P1 (9 P1 commands, S:159; plus adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow, which are ready with the stated flags, S:81-92). 22 commands accept the flag with the gate unresolved: 11 needs-change plus 4 ready commands with small fixes in P2 (S:160), roadmap and save in P3 (S:161), and implement, post-release, pr-submit in P4 (S:162). Counts reconcile to 27 needs-change (9+11+4+3) and 10 ready.

Recommendation: add the flag and the `## Unattended mode` section to a command in the same phase that implements its gate and outward-default resolution (so P1 covers only the commands whose resolution is already complete), and rewrite S:73 so "from Phase 1 on" is "from the phase that lists the command". If the flag must land early, state that before its phase the flag makes the command write `status: blocked` and stop. Update AC-1.1 to be per-phase.

### Requirements-bucket notes
Wiegers: WC-1 to WC-12 each have an owner and evidence column (S:57-70), which is good traceability. Adzic: examples are present for D1 (S:236) and several ACs (S:208). Cockburn: primary actor is the coordinator; the person is addressed by SA-1 to SA-6.

## === ARCHITECTURE ANALYSIS ===

### B-2 MAJOR (blocking) [Nygard, Crispin lens, Fowler]: the live worker check cannot pass for workflow, cleanup-audit or index-repo
Priority High. Quality impact: AC-0.4 and AC-1.2 fail on the spec's own designed behavior, so Phase 0 (which runs `/sc:workflow`) cannot pass and a failure there "reopens section 1" (S:202).

Grading sentence: An implementer who follows the stated text as written builds the check in S:193 step 6, whose pass condition for a report-only command is "only files under the brief's output directory appear", and applies it to `/sc:workflow` (AC-0.4 S:202, AC-1.2 S:204), and the check is wrong because the same spec says the workflow package "stays at `.dev/tasks/to-do/<id>/`" while only the contract goes to `<output-dir>` (S:92), and that cleanup-audit's "fixed `.claude-audit/` stays the default" with `--output-dir` added only for the contract (S:85) and index-repo keeps `PROJECT_INDEX.md` at its implied location (S:86, `INV-A:53`). In every one of those runs `git status --short` lists paths outside the output directory, so step 6 fails although the command behaved as specified. For `/sc:workflow` in P0 there is no output directory at all in the brief (S:158, S:202 pass `--handoff none` only), so the pass condition has no referent. Two stated texts contradict each other.

Recommendation: change step 6 to compare `git status --short` with the command's own declared write set (output directory plus the fixed locations named in the section 3 row: `.dev/tasks/to-do/<id>/`, `.claude-audit/`, `PROJECT_INDEX.md`, `PROJECT_INDEX.json`), and name that set per command in the brief template.

### Architecture-bucket notes
Fowler: the decision (coordinator on top, commands as units) is coherent and the rejected alternative R1 to R5 is well argued against `CAPS:97-103,145-151` (checked). The contract file as a single shared document (S:52) is a clean separation. Newman: the contract file schema (status, command, report_path, artifacts, blocked_question, S:62) has no version field; adding fields later has no compatibility story (see follow-up M-9). Hohpe: the integration is a file pointer plus one `worker_done` carrying an outcome (S:63, `CAPS:79` states the pointer is unchecked), and the spec correctly assigns the open-and-check duty to the coordinator (S:62, S:73).

## Guard Condition Boundary Table (Nygard lead, Crispin completeness, Whittaker attack)
Guards found in the spec: WC-5 outcome mapping, WC-10 wait split, WC-4 contract-path derivation, WC-1 readiness fallback, WC-8 depth. Classes left out are named with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome | S:63 | Zero/Empty | no report exists | failed | `--outcome failed` | OK |
| WC-5 outcome | S:63 | Zero/Empty | report exists but is a stale file from an earlier attempt | not defined | none; WC-4 (S:62) has no "overwrite or delete at start" rule, WC-6 (S:64) reuses the brief's directory | GAP (see M-4) |
| WC-5 outcome | S:63 | One/Minimal | `status: partial` | succeeded | `--outcome succeeded`, body states `partial` | OK |
| WC-5 outcome | S:63 | Typical | `status: blocked` | failed | `--outcome failed` | OK |
| WC-5 outcome | S:63 | Sentinel Value Match | `status` outside the four values | not defined | none; AC step 4 (S:191) asserts membership but WC-5 does not say which outcome | GAP (see M-4) |
| WC-5 outcome | S:63 | Legitimate Edge Case | audit verdict FAIL with `status: succeeded` | succeeded | succeeded | OK |
| WC-10 wait split | S:68 | Typical | single wait 3 min | true | allowed | OK |
| WC-10 wait split | S:68 | Legitimate Edge Case | wait exactly 4 min, plus tool latency, heartbeat every 5 min | true | "at most 4 minutes" leaves 1 min margin (S:274) | OK |
| WC-10 wait split | S:68 | Maximum/Overflow | wait of 5 min or more | false | must be split | OK |
| WC-10 wait split | S:68 | Zero/Empty | not applicable: a zero-length wait cannot starve a heartbeat | n/a | n/a | OK |
| WC-4 contract path | S:62 | Typical | `--output d/` | `d/return-contract.yaml` | defined | OK |
| WC-4 contract path | S:62 | Typical | `--output a/x.md` | `a/x.return-contract.yaml` | defined | OK |
| WC-4 contract path | S:62 | Sentinel Value Match | `--output a/x.md` and `a/x.txt`, or two Tasks given the same `d/` | same contract path | none; the stem rule drops the extension, and 2.3 (S:73) requires only "the output directory" | GAP (see M-3) |
| WC-4 contract path | S:62 | Zero/Empty | `--output ""` or an unwritable directory | not defined | none; the contract must be written "on every outcome", but where it goes when the directory cannot be written is not stated | GAP (minor, n-3) |
| WC-1 readiness | S:59 | Maximum/Overflow | fallback 30 s ok, about 45 s fails (`EVIDENCE.md:45,56` via S:59, UNVERIFIED directly) | per evidence | "well inside" the 60 s limit | OK |
| WC-8 depth | S:66 | Typical / Maximum | depth 1, worker calls `worker-start` | refused with `nested_worker_depth_exceeded` | WC-8 forbids the call (`CAPS:97-101`) | OK |
| WC-8 depth | S:66 | Legitimate Edge Case | depth-1 worker calls `task-create` | unknown | forbidden anyway; UNVERIFIED `CAPS:103,180` | OK (stated) |

FR-8 / FR-9 handling: the GAP rows concern a requirement the document never states (no overwrite rule, no unknown-status mapping, no collision rule), none is a stated text that does harm on its own, so each is Medium and listed below. The table is complete under FR-10.

## Quantity Flow Diagram (Fowler, Whittaker)
```text
[Source: 43 commands]
   |-- 6 coordinator-only (agent, git, help, pm, spawn, swarm-wizard) --> no flag (S:128-137)
   `-- 37 workers --> [P1 flag + section: N=37 (S:159)]
          |-- 10 ready: adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow (6, gate-free)
          |                    reflect, release-split, tdd, troubleshoot (4, gate fix in P2)
          `-- 27 needs-change: P1 9 | P2 11 | P3 4 | P4 3
   gate behavior complete at end of P1: M=15 (9 + 6)   <-- MISMATCH: 22 commands hold the flag with the gate unresolved (B-1)
   [P2: 15 commands (11 + 4)] --> [P3: 4] --> [P4: 3]   (sum 22 = 15+4+3)
   Consumer: coordinator brief (S:73) expects --unattended to mean no gate "from Phase 1 on"   <-- MISMATCH for the 22
```

## Medium and minor findings (follow-up candidates; none blocks, none enters the Reviser brief)

Medium (warnings):
- M-1 [Nygard, Wiegers]: WC-3 (S:61) lets the worker relay a coordinator's answer as a flag on re-invocation, with only the `/sc:implement` Ruling excepted. WC-9 (S:67) says outward actions turn on "only through the command's own explicit flag written in the brief", and D4 (S:252-255) says only a user's instruction naming the action may authorize it. For post-release the gate is "explicit pre-tag choice, else blocked" and VM/install/commit/PR off unless authorized (S:113); a blocked question that asks "authorize install?" can be answered by the coordinator, an agent, through `ask`, which is the route D4 option (a) was meant to close. The text does not say a relayed answer cannot supply a WC-9 flag. Requirement not stated, so Medium. Suggest one sentence in WC-3 excluding flags WC-9 governs.
- M-2 [Adzic, Crispin]: AC-2.2 (S:208) expects `worker_done --outcome failed` and `status: blocked` for a gate-trigger run, but WC-3 (S:61) allows the worker to `ask` instead of ending, after which the run can end `succeeded`. Which one the AC observes depends on whether the brief forbids `ask`; the brief template (S:73) does not say. Suggest the AC state "the brief tells the worker not to `ask`".
- M-3 [Hohpe, Whittaker (sentinel collision)]: contract path uniqueness. The stem rule (S:62) maps `a/x.md` and `a/x.txt` to one contract name, and nothing requires the coordinator to give each Task its own output directory (S:73 says only "the output directory"; WC-11, S:69, speaks about default output paths, not the contract). Two workers handed the same directory (for example several `/sc:troubleshoot` workers, S:39) overwrite each other's `return-contract.yaml`, and the coordinator then opens the wrong report. Also unclear whether rows that say "add a report path" or "add an output path" (S:101-103,106-108,110-111,123: build, cleanup, design, document, explain, improve, index, test) mean a directory or a file, which selects between two different contract names; AC-1.2 (S:204) fixes only the P1 case (`--output <dir>`), not cleanup and improve in P2.
- M-4 [Nygard, Whittaker (sequence attack)]: stale or invalid contract. WC-6 (S:64) re-runs a retry into the same brief, and WC-4 (S:62) has no rule to remove or overwrite an earlier contract at start. A retry that dies before writing leaves the first attempt's file, and a `partial` stale file maps to `succeeded` under WC-5. Also no mapping for a `status` outside the four values. "Fresh output directory" (S:64, S:99-125) does not say who allocates it: the command (then the path is not known before dispatch, contradicting S:62 and S:73) or the coordinator (then the brief must say so).
- M-5 [Fowler, Nygard]: tasklist and reflect (S:88, S:122). Under `--unattended`, reflect "follows the existing headless auto-accept rule" and tasklist passes `--unattended` to each Stage 10.5 reflect. `INV-B:109` says that rule auto-accepts remediation for auto-fixable registers and skips the gates, and `INV-B:215` recommended calling reflect without `--remediate` instead. The spec therefore makes an unattended tasklist run start remediation handoffs (workflow or task-builder) per phase inside Agent-tool subagents, an effect no brief asked for and which does not appear in the tasklist row's report column (S:122). The claim "one layer below the worker, inside Claude Code's nesting limit" (S:122, `INV-A:14`) does not count the reflect reviewers or the remediation handoff below those subagents (`INV-B:212`, UNVERIFIED whether nested spawns work). Stated choice differs from the inventory's recommendation without a Decisions row.
- M-6 [Crispin]: AC-C5 (S:176) and AC-0.3 (S:201) use `grep -E '^-[^-]'` on `git diff -U0`. A removed markdown bullet appears as `-- text`, which the pattern excludes (checked: of `-- removed bullet`, `-| removed row |`, `-plain removed` only the last two match). Deleted bullets are the main line shape in command files, so the additive-edit check can pass while a bullet is deleted. Use `git diff --numstat` deleted counts or `grep '^-' | grep -v '^---'`.
- M-7 [Crispin]: AC-2.4 (S:210) compares `gh api .../reviews --jq length` and `.../comments --jq length` before and after. Without `--paginate` each call returns at most the first page (30 by default), so on a PR that already has 30 or more entries a new post leaves the count unchanged and the check passes while the command posted. Add `--paginate` and sum.
- M-8 [Wiegers]: AC-1.1 (S:203) demands that every command in 3.1-3.2 has an `## Unattended mode` section naming `return-contract.yaml`. `/sc:load` is in 3.2 with report "none" and resume "n/a" (S:112) and is changed in P1 for its usage line only (S:159). The AC and the row disagree about load; the same applies to the P1 label "Report files and commands with no gate" (S:159) for test `--watch`, explain and business-panel refusals (S:102,108,123), which are gate resolutions.
- M-9 [Newman]: the contract schema (S:62) has no version field and no statement of which fields a coordinator may rely on, while P1 to P4 add fields over time and commands that "keep their fields and add the missing ones".

Minor (notes):
- n-1: E3 (S:23) cites `invocation_method: "skill-direct"` as support, while 1.4 (1) (S:43) says the PR #329 run proved only the nested route and `INV-A:35` calls adversarial "proven as a direct Orca-worker skill call". The spec is right to be cautious; E3 should carry the same caveat.
- n-2: WC-10 depends on a 5-minute heartbeat cadence taken from a worker preamble, not a guide (`CAPS:130`, acknowledged at S:68).
- n-3: no behavior when the output directory cannot be created or written (see table).
- n-4: a `blocked` Task ends `failed` (S:63), and a worker's own failed report does not trip the circuit breaker (`CAPS:80`), so a coordinator that retries blocked Tasks can retry without limit; the brief template (S:73) does not tell it to answer the question first.
- n-5: AC-0.2 (S:200) runs `cmp` on one mirror only; S:158 and CLAUDE.md require the level-table copy into `src/superclaude/core/CLAUDE.md` as well (UNVERIFIED, CLAUDE.md not in the workspace).
- n-6: the command definition read for this review (`command.md:455-465`) already describes `--unattended`, `--report-dir` and `<report-dir>/return-contract.yaml` for `/sc:spec-panel`, with `--output` file-valued. The spec's spec-panel row says "add `--output`; contract" (S:120) and its WC-4 names `--output / --output-dir` (S:62). Not graded: that file is not workspace evidence for the spec, but the flag name and the contract path differ, so the spec's rows may be out of date for that command.
- n-7: AC-C1's scan (S:181-183) matches four Orca subcommand words only, so it does not cover every form SA-2 forbids (for example `worker_done`).

UNVERIFIED citation groups (no file in the workspace): all `cmd/...`, `sk/...`, `src/superclaude/...`, `pyproject.toml:38`, `Makefile:68-74`, `plugins/...` (S:11, S:52, S:83-125, S:146-151, S:164, S:200, S:287); all `CLAUDE.md:N` (S:34, S:52, S:150, S:175, S:200, S:247, S:272, S:287); `HOW-WE-WORK.md:22,171,249,254`; `EVIDENCE.md:35-56`; `.dev/codegraph-migration/...` (S:23, S:43, S:174); Orca guide `[G]`/`[H:...]` line numbers except where `CAPS:N` quotes them (those quotes were read and match the spec's use).

Open question for the person who ran the review: whether to open an issue for the follow-up candidates. Not asked here (no interactive session); none created.

## Reviser brief
Repair only the blocking findings B-1, B-2 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Revise only text a blocking finding names. Add no rule, mechanism or section that a listed finding does not call for; prefer deleting or narrowing text over adding. Each added paragraph or table cites its finding id. Report the byte size of the candidate before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone, including through "apply all findings". Return the candidate once and do not award yourself a PASS.

verdict: FAIL
