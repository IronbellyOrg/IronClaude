review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (first review, whole document)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec. This is a first review of the full document, not a re-review and not a scoped PASS.
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `395733f7a06e7778fe5ef57a893a4bf2e96dc6f3da91a7e9826eea38dedbd783`
- baseline: none (no `--re-review` and no `--baseline` given, so this is a first review by default)
- reviewer model: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full)
- binding context read: `.dev/orca-command-refactor/README.md` (read in full)
- panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, always active). Review order per the command: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe. Crispin, Gregory and Hightower are outside the two requested focus areas and were not run.

## Citation conventions and what was checkable

- `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. Loop prompt file = `~/.claude/rules/prompts/document_review_loop_prompts.md`.
- The sandbox holds only the README, the three inventories, the candidate and the loop prompt file. Every citation the spec makes into `src/`, `tests/`, `docs/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `.dev/codegraph-migration/`, `.dev/evals/` or `/opt/Orca` is **UNVERIFIED** here unless an inventory line quotes it. Where this report relies on such a fact it says "via INV-x:N".
- I checked the arithmetic and cross-references inside the document directly. Details are in "What I covered".

## Verdict summary

Two blocking findings, both stated-text contradictions inside the acceptance and contract rules. The decision itself (Orca coordinates, commands stay units of work), the rejected alternative, the per-command split (10 / 27 / 6), the phase assignment per command and the open decisions are internally consistent and are backed by the inventories.

| id | severity (label) | graded | one line |
|---|---|---|---|
| F-1 | CRITICAL | blocking | WC-4 treats `--output` as a directory; the spec's own tdd and init-lite rows and AC-2.2 pass `--output <file>` |
| F-2 | MAJOR | blocking | AC-1.2 requires `--unattended --output <dir>` and a contract from "each P1 command"; load, workflow, index-repo and cleanup-audit cannot meet it |
| M-1 to M-9 | MAJOR/MINOR | Medium | follow-up candidates, listed below |

## === REQUIREMENTS ANALYSIS ===

### F-1 (blocking). WC-4 defines `<output-dir>` as the `--output` value, but the spec elsewhere makes `--output` a file for several commands
- Severity: CRITICAL. Priority: High. Expert: Wiegers (lead), Whittaker (Sentinel Collision Attack). Quality-impact estimate: Testability and Consistency each drop about 2 points.
- Whittaker form: I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:62 (WC-4)** fails when **the caller passes a file to `--output`**. Concrete attack: coordinator brief `/sc:tdd "auth" --unattended --output docs/TDD_AUTH.md` (the form AC-2.2 itself uses, SPEC:200). Before: no contract. WC-4 says the contract is `<output-dir>/return-contract.yaml` where `<output-dir>` is the directory passed as `--output`. After: the path is `docs/TDD_AUTH.md/return-contract.yaml`, which cannot be created next to a regular file. State trace: `--output` = file, contract path = child of a file, write fails or the contract lands somewhere the coordinator never learns.
- Grading sentence: an implementer who follows the stated text as written builds a contract path `<--output value>/return-contract.yaml` for every command, and for tdd and init-lite that path is invalid because the spec itself says their `--output` is a file.
- Evidence of the contradiction:
  - WC-4: "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (SPEC:62).
  - tdd row: brief passes "`--output <file>`", report today "the TDD at `--output`" (SPEC:90; INV-B:222 "TDD file at `--output`").
  - init-lite row: "`--output <file>`" (SPEC:87; INV-A:55 "`.dev/superclaude/context-audit.md` or `--output`").
  - AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and expects "contract `status: blocked` with a non-empty `blocked_question`" (SPEC:200). The same file-valued `--output` is implied for spec-panel, document, explain, recommend and research, whose rows say "add `--output`", "write to a file" or "explicit output" (SPEC:107-108, 115-116, 120) without saying directory or file.
  - Section 2.3 says the brief states "the output directory, so the report path is known before dispatch" (SPEC:73). For a file-valued `--output` there is no stated directory.
- Recommendation (narrow): define one rule for where the contract goes when `--output` is a file, or name a separate directory flag for the contract. Delete "`--output` / `--output-dir`" from WC-4 unless every command's `--output` is directory-valued. Restate AC-2.2 with that path.
- Reviser may touch: SPEC:62, SPEC:73 and the AC-2.2 command at SPEC:200 only.

### F-2 (blocking). AC-1.2 cannot pass for every command the P1 row names
- Severity: MAJOR, graded blocking because the acceptance criterion cannot pass on the stated text. Priority: High. Expert: Wiegers, Adzic. Quality-impact estimate: Testability drops about 2 points.
- Grading sentence: an implementer who follows the stated text builds Phase 1 exactly as the P1 row says, and AC-1.2 then fails on four of the thirteen named commands.
- Evidence:
  - P1 row names load, workflow, index-repo and cleanup-audit among its commands (SPEC:159).
  - AC-1.2: "7.2 live check on each P1 command with `--unattended --output <dir>`" and "all steps pass" (SPEC:196). 7.2 step 3 requires the report path to be "the WC-4 contract path" and step 4 requires a contract file with a valid `status` (SPEC:182-183).
  - load: the P1 row gives "usage line only" and "none (see note)" for the report, with no `--unattended` and no contract (SPEC:112, 159). AC-1.1 correctly says "load excepted" (SPEC:195); AC-1.2 does not.
  - workflow: the contract path is inside a generated package directory and `--output` does not apply; the spec calls this a WC-4 exception (SPEC:62, 92, 182). `--output <dir>` is not a workflow flag in the spec.
  - index-repo: brief passes "none"; output is `PROJECT_INDEX.md` at an implied location (SPEC:86; INV-A:53).
  - cleanup-audit: output dir is fixed, `--pass <N>` (SPEC:85; INV-A:42).
- Recommendation (narrow): restate AC-1.2 as "each P1 command that gains `--unattended`, using the flags its section 3 row lists", and exempt load by name. Do not add flags to commands to make the criterion pass.
- Reviser may touch: SPEC:196 only.

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The central decision holds and is backed by the evidence:
- Orca does not schedule (CAPS:92) and workers are top-level sessions (CAPS:161, CAPS:155), so a coordinator-on-top design needs no command-side Orca calls (SPEC:16, 22-27).
- The rejected alternative fails on a verified depth setting of 1 (CAPS:97-101), on standalone use (CAPS:147-149) and on the pane-bound `worker_done` (CAPS:76, 150) (SPEC:33-37).
- The spec states its evidence gaps plainly: no direct-route end-to-end run exists, the 60 s limit concerns pre-input questions, and subagent lifecycle messages are forbidden regardless (SPEC:41-45; CAPS:52, 129, 159-160).
- Fowler/Nygard checks: coordinator owns planning, retries and release; commands own work and one report; the single shared contract file is written once (SPEC:52, 264). That is a clean separation.

Architecture concerns that stay Medium are listed as M-2, M-3, M-6 and M-7 below.

## === Medium findings (follow-up candidates, never blocking, never in the Reviser brief) ===

| id | label | expert | finding (what the text does, why it is Medium) |
|---|---|---|---|
| M-1 | MAJOR -> Medium | Wiegers | SPEC:79 says ready commands report their named file "until Phase 1 adds the contract", but the P1 row (SPEC:159) names none of tdd, troubleshoot, release-split. Their contract is first demanded by AC-2.2 and AC-2.3 (SPEC:200-201) in P2. WC-4 (SPEC:62) already requires the contract under `--unattended`, so the right reading is available; the phase label is wrong. Troubleshoot writes `return-contract.yaml` only with `--caller task-unified` today (INV-B:242). |
| M-2 | MAJOR -> Medium | Nygard | WC-6 says a command without a resume flag "writes each run into a fresh output directory" (SPEC:64), while WC-4 fixes the contract at `<output-dir>/return-contract.yaml` with the directory passed by the coordinator and known before dispatch (SPEC:62). For the many "fresh dir" rows (SPEC:99-125) the text does not say whether the coordinator passes a new directory per retry or the command creates a subdirectory. The first reading is workable; the second would break the report path. Section 2.3 does not list "new output directory on retry" among what the brief carries (SPEC:73). |
| M-3 | MAJOR -> Medium | Fowler | SA-2 allows an Orca mention in the contract file "as an example of a caller's question channel" (SPEC:147), and P0 adds an Orca section to HOW-WE-WORK.md plus the contract file, both under `src/superclaude/core` (SPEC:158). AC-C1 greps `src/superclaude/core` for `orca(-ide) (orchestration|worktree|terminal|agent)` and requires no output in every phase (SPEC:172). If either new text names `orca orchestration ask`, P0 fails its own check. Whether it does is not stated. |
| M-4 | MAJOR -> Medium | Adzic | WC-4 fixes `status` to four values and the check asserts them for every contract (SPEC:62, 183), yet the same WC-4 says commands that already write a contract "keep their fields" (SPEC:62). The existing statuses of workflow, brainstorm, reflect and adversarial contracts are not listed anywhere (INV-B:272 names `status` without values). The Decisions row says copying each command's own statuses was rejected (SPEC:262). If an existing value differs, "keep" and "one of four" conflict. |
| M-5 | MINOR/Medium | Cockburn | SPEC:159 justifies P1 with "No person gate is involved", but P1 rows resolve gates: business-panel refuses socratic mode, explain refuses interactive format, test refuses `--watch`, index states the knowledge-base mode does not wait (SPEC:102, 108, 111, 123). SPEC:154 says "Phases 1-3 need no user decision", while D1 (how a command knows it is unattended) is open and every P1 change depends on it (SPEC:51, 227-230). The spec is written for the recommended flag, so the effect is documentation inconsistency only. |
| M-6 | MAJOR -> Medium | Newman | pr-submit "Will Not: run headless / imply a daemon" (INV-B:90, via `cmd/pr-submit.md:85`, UNVERIFIED here) is not mentioned in the pr-submit row, in D3 or in the P4 plan (SPEC:114, 238-242). Because D3 recommends (a) and P4 waits for the user, no wrong build follows today, but option (b) is presented as only a matter of heartbeats and summary files. |
| M-7 | MINOR/Medium | Newman | Design-level evidence leans on a rule that is scoped to this run: README:31 ("No git commits, pushes, PRs or GitHub comments") is cited as the reason `/sc:git` is coordinator-only and as support for WC-9 (SPEC:67, 133). README:31 binds this planning run's workers, not the product. The independent evidence (INV-A:91, INV-B:309-311) already supports the verdict. |
| M-8 | MINOR/Medium | Hohpe | The spec's E3 cites the PR #329 run and `invocation_method: "skill-direct"` as proof the design "has worked before" (SPEC:23), while section 1.4(1) says that run used an Agent-tool subagent and proves only the nested route (SPEC:43). The inventories label adversarial "proven" and "ready-as-Orca-worker (proven in PR #329 run)" (INV-A:13, INV-A:35). The spec's own caution is the correct one; the E3 row and the inventory wording overstate. `.dev/codegraph-migration/` paths are UNVERIFIED here. |
| M-9 | MAJOR -> Medium | Crispin-style completeness (via Nygard/Whittaker) | AC-0.4 step 4 uses "the command's existing report file" for adversarial (SPEC:194), but its contract filename is not fixed today (INV-A:60, SPEC:83). The smoke run therefore has no named file to check until P1. The coordinator can find it by listing the output directory. |

## Minor notes (never fail the review)

- N-1. 7.2 step 5 searches the transcript for `AskUserQuestion` (SPEC:184); a transcript that merely reads a skill file containing that word would match. Say "a tool call named `AskUserQuestion`".
- N-2. AC-1.3 runs a command "in a scratch worktree" (SPEC:197). Whether that worktree is created through Orca under the repo's worktree rule is not stated (the rule is in `CLAUDE.md`, UNVERIFIED here).
- N-3. tasklist passes `--unattended` to each reflect so reflect's headless auto-accept rule applies to `--remediate` (SPEC:122), whereas INV-B:215 recommended dropping `--remediate`. The spec's choice means remediation handoff can run unattended inside tasklist. What reflect's auto-accept then does is UNVERIFIED here (INV-B:109).
- N-4. index-repo and cleanup-audit have fixed output locations, so two such workers in one worktree clash. SPEC:85 notes it for cleanup-audit only; index-repo (SPEC:86) is not noted.
- N-5. WC-3 allows a worker to `ask` instead of ending `blocked`, but AC-2.2 expects `failed` plus `status: blocked` (SPEC:61, 200). Fine for gate-trigger runs; say AC-2.2 runs without the `ask` path.

## Adversarial analysis (Whittaker, five attacks)

| attack | target | result |
|---|---|---|
| FR-2.1 Zero/Empty | WC-5 "no report exists" (SPEC:63) and AC step 4 `test -s` (SPEC:183) | An empty or unparseable contract: the check fails it, but WC-5 does not say what the worker reports. The text covers "no report exists" only. Medium (M-4 area); no wrong outcome follows for the coordinator because step 4 catches it. |
| FR-2.2 Divergence | WC-4 directory versus file `--output` | Produces F-1. |
| FR-2.3 Sentinel Collision | `status: blocked` versus the Orca outcome set | `blocked` maps to `failed` (SPEC:63); the Task then needs `--retry-of`. Orca's own-failed report does not trip the circuit breaker (CAPS:80), so consistent. No finding. |
| FR-2.4 Sequence | WC-12 `check` before `worker_done` versus `consumer_fenced` (SPEC:70) | Consistent with CAPS:66-67. No finding. |
| FR-2.5 Accumulation | WC-10 split waits of 4 minutes (SPEC:68) for cli-eval evals of up to 3600 s | About 15 or more heartbeat-bounded waits per eval; no counter limit is stated and none is needed. No finding. |

## Mandatory artifact: Guard Condition Boundary Table

Guards found: WC-5 outcome mapping, WC-10 wait threshold, WC-4 contract existence, the blocked gate resolution (WC-2 c), D1 unattended switch, AC-C5 "no removed lines". Classes that cannot occur are omitted with a reason below the table. All cells populated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| outcome map (status to `--outcome`) | SPEC:63 | Zero/Empty | no contract file | true | `--outcome failed` | OK |
| outcome map | SPEC:63 | Zero/Empty | empty or unparseable contract | n/a | not stated; AC step 4 fails it (SPEC:183) | GAP (Medium, M-4 area) |
| outcome map | SPEC:63 | Typical | `status: succeeded` | true | `--outcome succeeded` | OK |
| outcome map | SPEC:63 | Sentinel Value Match | `status: partial` | true | `--outcome succeeded`, body states `partial` | OK |
| outcome map | SPEC:63 | Legitimate Edge Case | `status: blocked` | true | `--outcome failed` | OK |
| outcome map | SPEC:63 | Legitimate Edge Case | existing contract status outside the four values | n/a | not stated | GAP (Medium, M-4) |
| heartbeat wait split | SPEC:68 | Typical | single call over 5 min | true | split into waits of at most 4 min | OK |
| heartbeat wait split | SPEC:68 | Maximum/Overflow | eval timeout 3600 s | true | split into at most 4-minute waits | OK |
| heartbeat wait split | SPEC:68 | Legitimate Edge Case | single call of 4 to 5 min | false | not required to split; heartbeat can slip; allowed | OK |
| contract path | SPEC:62 | Typical | `--output` is a directory | true | `<dir>/return-contract.yaml` | OK |
| contract path | SPEC:62, 87, 90 | Legitimate Edge Case | `--output` is a file | n/a | not stated | GAP (blocking, F-1) |
| contract path | SPEC:62, 92 | Legitimate Edge Case | workflow generated package dir | true | exception stated, path read from the created package | OK |
| gate resolution (c) | SPEC:60 | Zero/Empty | empty `blocked_question` | n/a | AC-2.2 requires non-empty (SPEC:200); WC-2 does not say so | GAP (Medium, minor) |
| unattended switch | SPEC:51, 227-230 | Typical | `--unattended` in the brief | true | unattended mode on | OK |
| unattended switch | SPEC:227-230 | Zero/Empty | flag absent | false | standalone behaviour unchanged (SA-1, SPEC:146) | OK |
| additive-edit check | SPEC:176 | Zero/Empty | no changed lines | true | prints nothing, passes | OK |
| additive-edit check | SPEC:176, 149 | Legitimate Edge Case | named defect fix removes a line | n/a | excluded by SA-4 and the check's wording | OK |

Classes left out: "One/Minimal" and "Maximum/Overflow" for the contract-path, switch and additive-edit guards, because those guards are boolean or path-shaped and have no count or magnitude.

FR-8 (GAP status) generated: blocking for the file-valued `--output` row (F-1), Medium for the other two GAP rows. FR-9 (blank behavior) generated: the same three rows. FR-10 satisfied: the table is complete before the synthesis below.

## Mandatory artifact: Pipeline Dimensional Analysis and Quantity Flow Diagram

Trigger: multi-stage flow where output count differs from input count (SPEC:75-76 split, SPEC:154-162 phases). Fowler annotated; Whittaker attacked every divergence point.

```text
[Inventories: 43 commands (INV-A:3 = 21, INV-B:3 = 22)]
   --> [Split: ready 10 | needs-change 27 | coordinator-only 6]  (10+27+6 = 43, checked row by row, SPEC:81-137)
   --> [Phase assignment, section 3.2 "Phase" column: P1 9 | P2 11 | P3 4 | P4 3 = 27; plus ready-command fixes P1 4 and P2 4 (SPEC:85-91, 159-160)]
   --> [Consumer: section 6 P-rows list P1 9 + 4 fixes, P2 15 (11 + 4 ready), P3 4, P4 3]  (consistent)
   --> [Consumer: AC-1.1 asserts Unattended section on "every command in the P1 row, load excepted"  (SPEC:195)]
   --> [Consumer: AC-1.2 runs 7.2 on "each P1 command"  (SPEC:196)]  <-- MISMATCH: load, workflow, index-repo, cleanup-audit (F-2)
   --> [Consumer: AC-2.2, AC-2.3 expect a contract from tdd, troubleshoot, release-split  (SPEC:200-201)]  <-- not scheduled in the P1 row (M-1)
```

Counts that conserve: 43 total, 27 in section 3.2, 27 in the Phase column, 6 in section 4. The only count divergence is between the P1 row's command set and the commands AC-1.2 exercises (F-2).

## Expert commentary by panel member

- Wiegers: the requirements are mostly measurable (WC-1 to WC-12 each carry owner and evidence). The two blocking findings are testability defects, not missing requirements.
- Adzic: AC-2.2 is a good degenerate example (bare topic, no `--suite`) but uses a file-valued `--output` that WC-4 cannot place (F-1).
- Cockburn: primary actor (the coordinator) and goal are clear; section 2.3 states what the coordinator owes each worker. Retry briefs are not covered (M-2).
- Fowler: separation of coordinator and command is clean; no Orca calls enter commands (SA-2). M-3 is the only place where the checks and the allowance disagree.
- Nygard: failure modes are covered: stall, blocked, partial, fenced consumer, no report. The empty-contract case is the one gap (guard table).
- Newman/Hohpe: the contract file is a stable, versionable shared interface; status vocabulary evolution is not addressed (M-4).

## Follow-up candidates

M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9 and notes N-1 to N-5 above. Offer to open an issue for them: **not asked** (no user in this sandbox; recorded only, no issue created).

## What I covered

- Read in full: the command definition, README, the three inventories, the candidate and the loop prompt file.
- Checked inside the document: the 43 / 10 / 27 / 6 arithmetic against INV-A:3, INV-B:3, SPEC:81-137; the phase of every section 3.2 row against section 6 and the P-row lists; WC-1 to WC-12 against the acceptance checks in section 7; D1 to D5 against section 3 and section 6; the Orca facts the spec quotes (E1, E2, E4, R1 to R5, WC-3, WC-5, WC-7, WC-8, WC-10, WC-12) against the CAPS lines they cite, all of which exist and say what the spec says.
- Not checkable here (UNVERIFIED): every `src/`, `tests/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `.dev/codegraph-migration/`, `.dev/evals/` and `/opt/Orca` citation not quoted by an inventory, and the spec's own statements that it re-read 11 locations and that an evidence-validator re-read about 340 citations (SPEC:11, 285).
- Not done: no improved specification was written (the brief forbids editing anything else, and the command's Will Not forbids modifying a spec without consent). No `--focus correctness` artifacts (State Variable Registry) apply because that focus was not requested.
- Overrides: the brief named no clause that widens scope or regrades a finding, so no brief clause was overridden.

## Reviser brief

Repair only the blocking findings F-1, F-2 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

- F-1: SPEC:62 (WC-4 `<output-dir>` definition), SPEC:73 (section 2.3 output directory), and the AC-2.2 command at SPEC:200. Make the contract location well defined when `--output` is a file, or stop equating `--output` with the contract directory.
- F-2: SPEC:196 (AC-1.2). Restrict it to the P1 commands that gain `--unattended` and the flags their rows list; name load as excepted.

verdict: FAIL
