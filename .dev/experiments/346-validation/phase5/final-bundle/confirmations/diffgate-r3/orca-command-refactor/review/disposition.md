# Disposition of review 1 findings: orca-worker-contract-spec.md

Task: task_547bc8d547b9 (Task 6, revise the spec). Inputs: `.dev/orca-command-refactor/review/spec-panel.md` (review 1 of 3), `.dev/orca-command-refactor/review/diffgate-loop/reviser-brief-r1.md` (task list: blocking ids only), `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited). Line numbers `doc-r1.md:N` refer to the reviewed byte copy `.dev/orca-command-refactor/review/diffgate-loop/doc-r1.md`.

## 1. Method
- Read the shared rules (`.dev/orca-command-refactor/README.md:29-38`), the reviser brief (`reviser-brief-r1.md:6-21`), the review (`spec-panel.md:1-135`) and the whole spec. Before editing, `cmp` showed the spec identical to `doc-r1.md`.
- Re-read each source a blocking finding depends on (2026-11-09, this worktree): `src/superclaude/commands/workflow.md:12,42`; `src/superclaude/skills/sc-workflow-protocol/SKILL.md:24,26,66,72`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7,39`; `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:427-436`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md:659,665`; `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:283-290,335,340`; `src/superclaude/commands/auggie-review.md:51`; `CLAUDE.md:9-11`; `src/superclaude/commands/troubleshoot.md:82` and `src/superclaude/commands/adversarial.md:146` (each names its skill); `.dev/orca-command-refactor/inventory/commands-a.md:60` (no fixed adversarial contract file; earlier workers wrote it under `adversarial/`).
- Ran `git check-ignore -v .dev/reviews/x .dev/troubleshoot/x .claude-audit/x .dev/orca-command-refactor/x`: no output, exit 1, so none of these paths is ignored (supports R1.7). Ran the AC-C1 grep: no output today.
- Scope rule: the brief lists only the blocking findings, and fixcheck lets only open blocking ids own a hunk (`~/.claude/skills/sc-diffgate/scripts/diffgate.py:908-917`). So the six minor findings are recorded here and not applied (`reviser-brief-r1.md:3-4,19`).
- Spec size: 57763 bytes before, 61101 bytes after (fixcheck `bytes_before` / `bytes_after`). "now :N" below means line N of the edited spec.

## 2. Disposition table
One row per finding in `spec-panel.md:79-94`. Verified = whether the cited evidence holds when re-read.

| # | Blocking | Verified | Disposition | Where (edited spec) / reason |
|---|---|---|---|---|
| R1.1 | yes | Yes: AC-1.1 covered all 3.1-3.2 commands (`doc-r1.md:195`), the load row gives no report (`doc-r1.md:112`), Decisions rejects one (`doc-r1.md:265`) | applied | AC-1.1 now excepts `/sc:load` (now :195); section 3 intro excepts `/sc:load` (now :76); load row states it gets no `--unattended` and no `## Unattended mode` section (now :112). Decisions row on load unchanged, now consistent. |
| R1.2 | yes | Yes: P1 put `--unattended` on every 3.1-3.2 command (`doc-r1.md:159`); auggie-review posts with "No confirmation prompt" (`src/superclaude/commands/auggie-review.md:51`) | applied | P1 scope: the flag and section land only for P1 commands and 3.1 commands with no later-phase fix; every other command gets them in its own phase, and a 3.2 command is not dispatched before then (now :159). Section 3 intro "in the phase its row names" (now :76). AC-1.1 asserts converted-so-far commands and none of a later phase (now :195). |
| R1.3 | yes | Yes: `--output` raises `E-LEGACY` (`src/superclaude/commands/workflow.md:42`); the package name carries the run timestamp (`workflow.md:12`); no yaml on a pre-creation STOP (`src/superclaude/skills/sc-workflow-protocol/SKILL.md:26`; `refs/return-contract.md:39`) | applied | WC-4 names workflow as the one exception (now :62); 2.3 brief duty notes workflow takes no output dir (now :73); workflow row replaces the unlocatable pre-creation-STOP fix with the discovery rule and WC-5's "no report" branch (now :92); SA-4 drops the workflow fix (now :149); P1 commands list (now :159); 7.2 step 3 pass rule for workflow (now :182); AC-1.2 runs workflow without `--output` (now :196); AC-1.4 drops the workflow check (now :198). Choice recorded in section 3 below. |
| R1.4 | yes | Yes: the skill names no contract file (`src/superclaude/skills/sc-adversarial-protocol/SKILL.md:427-436`); the row said `<output>/adversarial/return-contract.yaml` (`doc-r1.md:83`) vs WC-4 `<output-dir>/return-contract.yaml` (`doc-r1.md:62`) | applied | Adversarial row now fixes the path to `<output>/return-contract.yaml` (now :83); AC-1.4 checks that exact path (now :198); SA-4 wording (now :149). |
| R1.5 | yes | Yes: WC-3 is optional ("may instead ask", `doc-r1.md:61`); AC-2.2 expected `blocked`/`failed` (`doc-r1.md:200`) | applied | WC-3 applies only when the brief does not forbid asking (now :61); AC-2.2's brief forbids the `ask` branch (now :200). |
| R1.6 | yes | Yes: WC-3 re-run (`doc-r1.md:61`), WC-4 brief dir (`doc-r1.md:62`) and WC-6 fresh dir (`doc-r1.md:64`) gave no single answer | applied | WC-3: the re-run reuses the brief's `<output-dir>`, its contract replaces the blocked one and lists only its own files (now :61); WC-6: the fresh directory is per retry Dispatch, not per re-run (now :64). |
| R1.7 | yes | Yes: `git check-ignore` printed nothing for the output locations; workers share a worktree by default (`.dev/orca-command-refactor/inventory/orca-capabilities.md:115`, as cited by the review) | applied | 7.2 step 6 compares against a pre-dispatch `git status --short` snapshot, and live checks in one worktree run one at a time (now :185). |
| R1.8 | yes | Yes: P0 adds core Orca text (`doc-r1.md:158`) that AC-C1 scans (`doc-r1.md:172`); no rule kept command lines out | applied | P0 row: both core files name the lifecycle messages and point to Orca's own guide and the dispatch preamble for exact command lines, so AC-C1 matches nothing (now :158). |
| R1.9 | yes | Yes: `CLAUDE.md:9-11` requires the Skill tool call; WC-7 (`doc-r1.md:65`) and AC-0.4 (`doc-r1.md:194`) did not | applied | WC-7 requires the Skill tool call when the command file names a skill (now :65); AC-0.4 verifies that call in the transcript (now :194). |
| R1.10 | no (minor) | Plausible; the duration is UNVERIFIED per the review (`spec-panel.md:88,109`) | rejected | Minor finding, outside the reviser brief (`reviser-brief-r1.md:3-4`); a hunk owned by a minor id fails fixcheck (`diffgate.py:916-917`). Left as a note for a later review. |
| R1.11 | no (minor) | Yes: WC-1 has no phase scope or AC (`doc-r1.md:59,158-162`) | rejected | Minor, outside the reviser brief (`reviser-brief-r1.md:3-4`). |
| R1.12 | no (minor) | Yes: wording conflict between `doc-r1.md:51` and `doc-r1.md:67-69` | rejected | Minor wording, outside the reviser brief (`reviser-brief-r1.md:3-4`). |
| R1.13 | no (minor) | Yes: `^-[^-]` misses a deleted blank line (`doc-r1.md:176`) | rejected | Minor, outside the reviser brief (`reviser-brief-r1.md:3-4`). |
| R1.14 | no (minor) | Partly: package count UNVERIFIED (`spec-panel.md:110`) | rejected | Minor, outside the reviser brief (`reviser-brief-r1.md:3-4`). |
| R1.15 | no (minor) | Yes: 2.3 omits serializing cleanup-audit (`doc-r1.md:73,85`) | rejected | Minor, outside the reviser brief (`reviser-brief-r1.md:3-4`). The R1.7 one-at-a-time rule (now :185) covers live checks only, not this duty. |
| R1.16 | yes | Yes: workflow `status: success \| partial \| failed` (`src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`); reflect adds `dry-run` (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:665`); brainstorm the same (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:340`); adversarial `"success"` (`src/superclaude/skills/sc-adversarial-protocol/SKILL.md:436`), which brainstorm reads (`sc-brainstorm-protocol/SKILL.md:283-290`) | applied | WC-4: existing contracts keep `success`/`dry-run` and add only missing fields and `blocked` (now :62); WC-5 maps `success` and `dry-run` to succeeded and any unlisted value to failed (now :63); 7.2 step 4 accepts the kept values (now :183); Decisions "Status vocabulary" row updated (now :262). |

## 3. Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| R1.3: how `/sc:workflow` meets WC-4 | (a) add an unattended-only flag naming the package id; (b) restore an output flag; (c) exempt workflow from "known before dispatch", the worker reports the path the run prints, and a pre-creation STOP reports `failed` with no contract | (c). `--output` was retired on purpose (`src/superclaude/commands/workflow.md:42`) and the skill forbids any yaml before the package exists (`src/superclaude/skills/sc-workflow-protocol/SKILL.md:26`); (a) and (b) add a mechanism no finding asked for. WC-5 already turns "no report exists" into `failed`. |
| R1.16: keep or rename existing status values | rename to the four-value set; keep `success`/`dry-run` and accept them | Keep. Brainstorm routes on adversarial's `status` (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:283-290`), so a rename breaks a current reader (SA-1). |
| R1.2: stop gated commands accepting `--unattended` early | define a P1 meaning for gated commands; add the flag per phase | Per phase: the meaning of the flag on a gated command is its P2-P4 gate resolution, so it lands with that resolution. |
| R1.5: make AC-2.2 deterministic | accept either outcome; forbid `ask` in the check's brief | Forbid `ask` in the brief: AC-2.2 exists to test the command's own `blocked` path (WC-2 (c)). |
| R1.7: stop earlier output failing step 6 | ignore output dirs in `.gitignore`; snapshot before dispatch | Snapshot: it needs no repo change and also covers documented artifacts outside the output directory. |
| Minor findings | apply them; record only | Record only: the brief excludes them and fixcheck rejects a hunk owned by a minor id. |

## 4. UNVERIFIED items
1. Whether every reader of the workflow, reflect and adversarial contracts tests the literal `success`; only the brainstorm reader was traced (`spec-panel.md:112`). The R1.16 fix keeps the values either way.
2. Whether a `/sc:` line inside an Orca preamble is ever expanded as a slash command (`spec-panel.md:111`). The R1.9 fix requires the Skill call either way.
3. Whether a command that does not yet define `--unattended` refuses it or ignores it; not traced. The R1.2 fix avoids depending on it by not dispatching such commands with the flag.

## Diffgate fixmap
doc_sha: 874c3f1665ea295583feb505b72645c5b8564dcbe2c4bd961e0313b14d56a8e2
H2.1 R1.5,R1.6,R1.3,R1.16,R1.9
H2.2 R1.3
H2.3 R1.1,R1.2
H2.4 R1.4
H2.5 R1.3
H2.6 R1.1
H2.7 R1.3,R1.4
H2.8 R1.8,R1.2,R1.3
H2.9 R1.3,R1.16,R1.7
H2.10 R1.9,R1.1,R1.2,R1.3,R1.4,R1.5
H2.11 R1.16
