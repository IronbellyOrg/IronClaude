review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: missing (no `--re-review`/`--baseline`; first review of the full document)
- reviewer model: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:29-36`. This file is ONE of the three first reviews; the coordinator runs the other two in fresh contexts and applies the MERGE rule.
- evidence checkable in this sandbox: the spec, `README.md`, `inventory/commands-a.md` (`INV-A`), `inventory/commands-b.md` (`INV-B`), `inventory/orca-capabilities.md` (`CAPS`). Every citation of `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `/opt/Orca/...` is UNVERIFIED here and was only checked through the inventory line that quotes it.
- coverage: whole document (sections 1-9, Decisions, UNVERIFIED), the 43-command split, WC-1..WC-12, SA-1..SA-6, P0-P4, AC-C1..AC-4.3, D1-D5; spot-checked 31 `CAPS:` lines and 10 `INV-A/INV-B` lines against their spec use. Not covered: the per-row `cmd/`/`sk/` line citations in section 3 (no source tree in the sandbox).

## Verified facts (no finding)
- Command count conserves: 21 (`INV-A:3`) + 22 (`INV-B:3`) = 43. Ready 5 (A) + 5 (B) = 10 (spec lines 81-92); needs-change 13 (A) + 14 (B) = 27 (spec lines 99-125, counted row by row); coordinator-only 3 + 3 = 6 (spec lines 132-137). The split agrees with the inventories' own groupings (`INV-B:289-299`, `INV-A:76-83`).
- R1 (nesting depth 1) matches `CAPS:97-103`, including the spec's own UNVERIFIED flag on which call sites enforce it (spec line 33 vs `CAPS:103`).
- WC-5 outcome vocabulary (`succeeded|failed` only) matches `CAPS:73`; heartbeat-not-needed-in-`ask` matches `CAPS:64`; the 5-minute cadence matches `CAPS:130`.
- Pipeline Dimensional Analysis (FR-17): not triggered. The phases and the 10/27/6 split are a partition, not a filtering pipeline, and the counts conserve (above).

## === REQUIREMENTS ANALYSIS ===

### F1 - CRITICAL-by-consequence, BLOCKING: AC-1.1 and the P1 sweep contradict the `/sc:load` row and its recorded Decision
- Expert: Wiegers (traceability), Adzic (acceptance example).
- Stated texts that contradict:
  - Spec line 195 (AC-1.1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - Spec line 159 (P1): the `--unattended` flag is "accepted by every command in sections 3.1 and 3.2", and line 76: "Every changed command also gains the `## Unattended mode` section"; WC-4 (line 62): in unattended mode the command "writes `<output-dir>/return-contract.yaml`" on every outcome.
  - Spec line 112 (`load` row, section 3.2): Report column "none (see note)", Resume "n/a", "use it as a step inside another worker's brief, not as its own Task", Phase "P1 (usage line only)". Spec line 265 (Decisions): "Use it inside a brief ... a report file would be an unrequested addition. Only its usage-line defect is fixed." `INV-B:65` supports that: "it only loads context into the current session and writes no file".
- Wrong outcome (grading sentence): An implementer who follows the stated text as written builds either an AC-1.1 test that fails on `load` (it has no `## Unattended mode` section and no contract by the row and the Decision), or a `load` that gains a section and a contract file that the row and Decision say must not exist; both cannot hold, so the P1 gate "every check in its block passes" (spec line 167) cannot be met by following the spec, and the phase can never be declared passed without picking which of the two texts to break.
- Same contradiction, smaller scope: `/sc:init-lite` is in section 3.1 with "Small fix: None" (line 87) yet is inside the P1 sweep of "every command in 3.1" (line 159) and AC-1.1/AC-1.2. Noted under this id, not a separate finding.
- Recommendation: narrow AC-1.1 and the P1 sentence to "every command in 3.1-3.2 except `load`" (or say `load` gets a section that states it writes no contract). Prefer narrowing over adding.
- Priority: High. Quality impact: acceptance gate for P1 is unsatisfiable as written.

## === ARCHITECTURE ANALYSIS ===
(Fowler, Newman, Hohpe, Nygard). The central decision (section 1: coordinator on top, commands unchanged units, no Orca calls inside commands) is internally consistent with R1-R5 and with `CAPS:97-103,145-150,155-161`. No blocking architecture finding. Items below are Medium (a requirement the document never states, or a reading the implementer must guess).

### Guard Condition Boundary Table (Nygard, Crispin, Whittaker)
Guards identified: WC-10 wait threshold (line 68), WC-5 outcome mapping (line 63), WC-2 gate resolution (line 60), WC-6 resume-or-fresh-dir (line 64), nesting depth 1 (line 33), D1 flag token (line 51). Six input classes are a menu; classes that cannot occur are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-10 wait split | WC-10, line 68 | Zero/Empty | wait of 0 s | n/a | no rule needed (no wait) - class left out: nothing blocks | OK |
| WC-10 wait split | WC-10, line 68 | Typical | 3 min single call | false | no split needed | OK |
| WC-10 wait split | WC-10, line 68 | Maximum/Overflow | 3600 s eval | true | split into waits of at most 4 min (cli-eval row, line 104) | OK |
| WC-10 wait split | WC-10, line 68 | Legitimate Edge Case | single call of 4.5 min | unspecified (threshold ">5 min", target "<=4 min") | not stated | GAP (M3) |
| WC-5 outcome | WC-5, line 63 | Zero/Empty | no report file exists | true | `--outcome failed` | OK |
| WC-5 outcome | WC-5, line 63 | Sentinel Value Match | report exists, `status` not one of the four values / unparseable | unspecified | not stated | GAP (minor) |
| WC-5 outcome | WC-5, line 63 | Legitimate Edge Case | `partial` | true | `succeeded`, body states `partial` | OK |
| WC-2 gate | WC-2, line 60 | Typical | gate hit, no default, no flag | true | `status: blocked`, stop | OK |
| WC-2 gate | WC-2, line 60 | Sentinel Value Match | `--unattended` inside quoted content | unspecified in this spec | defined only in the command file, not here | GAP (minor, outside candidate) |
| WC-6 resume | WC-6, line 64 | Legitimate Edge Case | resume flag passed but on-disk state missing/corrupt | unspecified | not stated | GAP (minor) |
| Depth fence | R1, line 33 | Maximum/Overflow | depth 2 call | true | refused `nested_worker_depth_exceeded` (`CAPS:97-101`) | OK |

No GAP names a concrete wrong outcome an implementer produces with no extra assumption, so none is blocking (FR-8/FR-9 graded by consequence). The table is complete for the guards enumerated, so FR-10 does not block synthesis.

### Whittaker adversarial findings (all below blocking)
- Sequence Attack on WC-3 vs WC-2(c) vs WC-5 (lines 60-63): the command first writes `status: blocked` and stops; WC-3 then lets the worker `ask`, "re-invoke or resume the command with the answer", and WC-5 says send `worker_done` once. State trace: contract=blocked -> ask answered -> re-invoke -> contract overwritten to succeeded -> one `worker_done`. The spec never says the re-invocation overwrites the blocked contract, nor that a coordinator reading the file in between sees `blocked` while the worker is healthy. Reading is inferable; Medium (M5).
- Divergence Attack on AC-2.2 (line 200): it requires `worker_done --outcome failed` for a gate hit, but WC-3 allows the worker to `ask` and continue. A worker following WC-3 produces `succeeded`, failing the check unless the brief forbids `ask`. Needs a guess about the brief; Medium (M5).

## Medium findings (warnings; follow-up candidates, not in the Reviser brief)
- M1 (Wiegers/Nygard) `/sc:workflow` contract path is not "known before dispatch". WC-4 (line 62) and section 2.3 (line 73) require a path known before dispatch, and WC-4 requires the file "including stops before any other output exists". The workflow row (line 92) passes only `--handoff none`, the contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml` with a fresh package each run, and the "pre-creation STOPs" fix (line 92, AC-1.4 line 198) names no directory (no package or id exists yet; `INV-B:272-273`). 7.2 step 3 (line 182) checks "report path is the WC-4 contract path". The implementer must invent a location. Medium because it needs a guess; recommend stating one fixed location for that case.
- M2 (Fowler/Nygard) `/sc:tasklist` row (line 122) departs from its own evidence without a Decision. It passes `--unattended` to each reflect so the headless auto-accept applies, but `INV-B:46` and `INV-B:215` recommend dropping `--remediate` in Stage 10.5 and running reflect fan-out at the worker's top level, and `INV-B:210,314` mark subagent-to-agent nesting UNVERIFIED. The spec states the fan-out is "inside Claude Code's nesting limit, `INV-A:14`", but `INV-A:14` only quotes the three-layer docs rule and does not trace worker -> tasklist -> reflect subagent -> reviewers -> adversarial. Auto-accepting remediation also lets reflect hand off to workflow/task-builder inside a tasklist run, which WC-9 does not address. No AC covers tasklist's `--unattended` path (AC-2.1..2.3 are generic). Also UNVERIFIED #9 (line 280) says reflect does not treat a worker as headless, so tasklist and reflect are both edited in P2 with no stated order.
- M3 (Nygard/Crispin) WC-10 (line 68) leaves single calls of 4-5 minutes undefined (threshold ">5 min" vs target "<=4 min") and applies the split rule in rows only for cli-eval and pr-submit. Long single calls are plausible for `/sc:build`, `/sc:test`, `/sc:research` (rows lines 101, 123, 116 say nothing). The wait-splitting change in P2 has no acceptance check: AC-2.2/AC-2.3 (lines 200-201) do not test heartbeat spacing; only P4 AC-4.3 (line 210) does, for pr-submit.
- M4 (Fowler) SA-2 (line 147) allows an Orca mention "inside the contract file" while AC-C1 (line 172) greps `src/superclaude/core` (where `WORKER-CONTRACT.md` is to live, line 52) and passes only on empty output; if the contract names `orca orchestration ask` as WC-3 suggests, AC-C1 fails. The pattern is also written with `\|` inside a Markdown table; as an ERE it is a literal pipe, so the check would need unescaping to run as printed.
- M5 (Adzic) see the two Whittaker traces above (WC-3 vs WC-2/WC-5, AC-2.2).
- M6 (Nygard/Wiegers) WC-9 and D4 (lines 67, 245): "turns on only through the command's own explicit flag written in the brief", but the brief is written by the coordinator, an agent; the worker cannot tell a user-authorized flag from a coordinator-chosen one. D4(a) puts the control on the coordinator quoting the user, with no check anywhere in the AC set (AC-2.4, AC-4.2 test only the off state).
- M7 (Wiegers) Requirements WC-1, WC-3, WC-7, WC-11, WC-12 have no acceptance check (AC-C1..AC-4.3 cover WC-2, WC-4, WC-5, WC-8, WC-9, WC-10 only partly). WC-11 is also not met by two "ready" rows with fixed outputs: `cleanup-audit` fixed `.claude-audit/` is acknowledged (line 85); `index-repo` writes `PROJECT_INDEX.md` at a fixed location (line 86) with no WC-11 note.

## Minor notes
- Line 79 says the 10 ready commands "run as workers now", but 9 of the 10 carry a P1 or P2 small fix (lines 83-92); the heading should say "run now with the brief's flags".
- `validate-roadmap` and `validate-tests` list resume as "n/a" (lines 124-125) while WC-6 (line 64) says a command either resumes or uses a fresh directory.
- Section 1.2 E5 and E2/E3 rest on commands and files not readable here (UNVERIFIED in this sandbox); the spec's own line 285 says a fresh validator re-checked about 340 citations, which is not checkable here either.

## follow-up candidates
M1, M2, M3, M4, M5, M6, M7 and the minor notes above. Per the Review Loop, the session asks the user once per loop whether to open an issue for them; this run is a sub-run with no user prompt and creates none (record only).

## Reviser brief
Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding and report the byte size before and after, with the bytes added and deleted per finding id. Minor and Medium findings are not authorized edits, including through "apply all findings".

Blocking finding ids:
- F1: AC-1.1 (spec line 195) and the P1 sweep (spec lines 76, 159) require a `## Unattended mode` section naming `return-contract.yaml` for every command in 3.1-3.2, while the `load` row (line 112) and Decision (line 265) say `load` writes no report and gets only a usage-line fix. Wrong outcome: P1's acceptance gate cannot pass without breaking one of the two stated texts.

verdict: FAIL
