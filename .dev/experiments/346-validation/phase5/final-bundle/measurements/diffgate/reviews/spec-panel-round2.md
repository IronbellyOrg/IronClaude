# Spec panel review: orca-worker-contract-spec.md

review: 2 of 3

Task: task_85fee554b945 (Task 7, independent re-review). Reviewer did not write or revise the spec. Date: 2026-11-09.
Command: `/sc:spec-panel-diffgate @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --diffgate-dir .dev/orca-command-refactor/review/diffgate-loop --expect-round 2` (skill loaded with the Skill tool).
Repo root: /home/coder/workspaces/worktrees/IronClaude/exp346-v-diffgate (HEAD `2cb683f5c`). `SPEC:N` = line N of `review/diffgate-loop/doc-r2.md`, which is byte-identical to the revised spec (`cmp` exit 0; both sha256 `6c68d0ec...8d17`, the `doc_sha` in `review/disposition.md:55`). `SPEC-OLD:N` = line N of `doc-r1.md`. `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md`. `SURF:N` = `review/diffgate-loop/surface-r2.md`.

## Loop status
- `diffgate.py status --dir .dev/orca-command-refactor/review/diffgate-loop` (read-only, 2026-11-09) returned `"review": 2, "state": "open", "halt": null, "surface": ".../surface-r2.md"`. `--expect-round 2` matches, so this is a re-review of the computed surface (16 hunks H2.1-H2.16, 8% of lines, `SURF:4`), with the whole spec read as context.
- The `verdict:` line is not written by this reviewer; the coordinator's `check` step appends `close-r2.md` (`~/.claude/commands/sc/spec-panel-diffgate.md`, Review Loop bullet 3 and Diffgate bullet 4). The brief's binary verdict is given in prose in section 5.

## 1. Round-1 finding resolution table
Each row was judged from the revised spec text and the live sources, not from `disposition.md`'s claim.

| Round-1 finding | Disposition claim (`review/disposition.md`) | Spec text now | Verdict | Evidence |
|---|---|---|---|---|
| R1.1 report location unknowable (blocking) | Applied (`disposition.md:31`) | WC-4 adds `--report-dir <dir>`, separate from each command's own output flags; refusal when missing (no work, no file, outcome `failed`); workflow pre-creation STOPs covered (`SPEC:62`); brief carries it (`SPEC:73`); workflow row forbids `--output` (`SPEC:92`); every `--unattended` check run passes it (`SPEC:167`) | **Resolved** in WC-4. A residual in the unchanged AC-1.2 is new finding R2.1. | Live: `sk/sc-workflow-protocol/SKILL.md:24` (`--output` retired → `E-LEGACY`), `:26` (no yaml on pre-creation STOP); `refs/return-contract.md:39`; `cmd/tdd.md:49`, `cmd/init-lite.md:32` (file-valued `--output`); `grep -rlE -- '--report-dir\|--unattended' src/superclaude/commands src/superclaude/skills` printed nothing, so the new flags collide with no existing flag. |
| R1.2 `status` field collision (blocking) | Applied (`disposition.md:32`) | Field renamed `worker_status`; existing contracts and their `status` kept; explicit mapping `success`→`succeeded`, `partial`→`partial`, gate stop→`blocked`, `failed`/other→`failed`; same-path contracts gain top-level keys, otherwise a separate file (`SPEC:62`); step 4 asserts `d['worker_status']` (`SPEC:183`) | **Resolved.** Adversarial's nested `return_contract:` no longer breaks step 4 because `worker_status` is a new top-level key or a separate file. | Live: `refs/return-contract.md:7`; `sk/sc-adversarial-protocol/SKILL.md:432,436`; `sk/sc-reflect-protocol/SKILL.md:250` |
| R1.3 retry directory conflict (blocking) | Applied (`disposition.md:33`) | "each attempt's brief, a `--retry-of` retry included, names a new `--report-dir`" (`SPEC:64`, also `SPEC:73`) | **Not resolved (open).** Orca gives a `--retry-of` attempt no new brief: the retry must name the failed Task (`--task`; "`--spec` creates a new one"), and no verb changes a Task's spec (`task-update` takes only `--status`/`--result`). The retry therefore receives the first attempt's brief and `--report-dir`, which is the R1.3 attack. Creating a new Task instead is what Orca's guide forbids ("Do not route around that boundary with a new Run, Task, or unrelated Dispatch", `CAPS:116`). | `orca orchestration worker-start --help` Notes: "--retry-of needs --task naming the failed Task (--spec creates a new one)"; `orca orchestration task-update --help` Usage line (no spec flag); `orca-ide skills get orchestration --reference recovery-and-cleanup` lines 112-113 ("Name the failed Task with `--task`, since `--spec` creates a new one"). Orca 1.4.245. That a retry's preamble TASK block is exactly the stored Task spec is inferred, not observed (UNVERIFIED). |
| R1.4 WC-7 lacks the Skill call (blocking) | Applied (`disposition.md:34`) | WC-7 requires loading the command's skill with the Skill tool before any other step (`SPEC:65`); step 5 searches the transcript for that Skill call (`SPEC:184`); AC-0.4 requires it (`SPEC:194`) | **Resolved.** The check is feasible: this worker's own `worker-read --source transcript` output contains `"type": "tool-call"` blocks with `"name": "Skill"` and the text `sc:spec-panel-diffgate`. | Live: `src/superclaude/core/CLAUDE.md:73` ("When a message starts with `/sc:<name>`"); `orca orchestration worker-read --dispatch ctx_a260ae0a556b --source transcript --limit 200 --json` (2026-11-09): 22 tool-call blocks, names `Bash`, `Read`, `Write`, `Skill`. |
| R1.5 AC-C1 scans the contract file (blocking) | Applied (`disposition.md:35`) | AC-C1 adds `grep -v '^src/superclaude/core/WORKER-CONTRACT\.md:'` (`SPEC:172`); SA-2 names the exclusion (`SPEC:147`) | **Resolved.** `grep -rn` prints `path:line:text`, so the anchored exclusion matches every hit in that file and nothing else. The new SA-2 wording introduces minor R2.3. | `SPEC:172`; `SPEC:147` |
| R1.6 load vs AC-1.1 (blocking) | Applied (`disposition.md:36`) | AC-1.1 exempts `/sc:load` by name (`SPEC:195`) | **Resolved** for AC-1.1. The same conflict remains in the unchanged AC-1.2 (`SPEC:196`), recorded inside R2.1. | `SPEC:112,195,196,265` |
| R1.7 no parse rule for `--unattended` (blocking) | Applied (`disposition.md:37`) | Only a standalone token outside any quoted argument counts (`SPEC:51`); D1 (a) points to the rule (`SPEC:228`) | **Resolved** for the quoted-topic attack. An unquoted free-text topic still switches the mode; minor R2.4. | `SPEC:51,228` |
| R1.8 3.1 understates P1 edits (minor) | Rejected, minor (`disposition.md:38`) | `SPEC:79` unchanged ("The only command changes are the small fixes in the last column") | Not resolved; stays a minor note. | `SPEC:79,84,87,159` |
| R1.9 stale baseline (minor) | Rejected, minor (`disposition.md:39`) | `SPEC:4` still names `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs` | Not resolved; stays a minor note. | `SPEC:4` |
| R1.10 WC-10 covers unsplittable Agent calls (minor) | Rejected, minor (`disposition.md:40`) | `SPEC:68` unchanged | Not resolved; stays a minor note. | `SPEC:68` |
| R1.11 step-2 cadence vs 900 s wait (minor) | Rejected, minor (`disposition.md:41`) | Step 2 "at least once per 5 minutes" (`SPEC:181`), step 3 `--timeout-ms 900000` (`SPEC:182`) | Not resolved; stays a minor note. | `SPEC:181,182` |
| R1.12 transcript tool-call content UNVERIFIED (minor) | Rejected, minor (`disposition.md:42`) | Step 5 unchanged in method (`SPEC:184`) | The concern is now cleared by evidence (see the R1.4 row): the transcript source records tool-call names. The spec still cites no evidence for it; minor note. | `worker-read` run above; `CAPS:131` |
| R1.13 WC-5 exactly-once vs WC-12 fenced (minor) | Rejected, minor (`disposition.md:43`) | `SPEC:63` still "exactly once" with no fenced exception | Not resolved; stays a minor note. | `SPEC:63,70` |

Summary: of the 7 blocking findings, 6 are resolved in the spec text and R1.3 stays open. The 6 minor findings were declined by rule and remain as notes.

## 2. Citation-check table
Every `path:line` citation (and every Orca fact) added or changed by hunks H2.1-H2.16, re-read on 2026-11-09 against the live file at HEAD `2cb683f5c` or Orca 1.4.245 `--help`/guide output.

| # | Spec location | Citation | Claim it supports | Live text read | Result |
|---|---|---|---|---|---|
| C1 | `SPEC:62` (WC-4) | `sk/sc-workflow-protocol/SKILL.md:24,44` | workflow retires `--output`; package id generated at run time | `:24` "`--output` is retired → `E-LEGACY`"; `:44` id like `TASK-WF-authLogin-20261001-063000` | Correct |
| C2 | `SPEC:62` | `sk/sc-workflow-protocol/refs/return-contract.md:39` | pre-creation STOPs write no contract | `:39` "`E-LEGACY` including retired `--output` ... **no package directory, no yaml**" | Correct |
| C3 | `SPEC:62` | `cmd/tdd.md:49` | tdd `--output` is file-valued | "Output path for the final TDD document" | Correct |
| C4 | `SPEC:62` | `cmd/init-lite.md:32` | init-lite `--output` is file-valued | default `<project-root>/.dev/superclaude/context-audit.md`, "Report output path" | Correct |
| C5 | `SPEC:62` | `sk/sc-workflow-protocol/refs/return-contract.md:7` | workflow already uses `status` | `status: success \| partial \| failed` | Correct |
| C6 | `SPEC:62` | `sk/sc-adversarial-protocol/SKILL.md:432,436` | adversarial uses `status` nested under `return_contract:` | `:432` `return_contract:`; `:436` `status: "success" # success \| partial \| failed` | Correct |
| C7 | `SPEC:62` | `sk/sc-reflect-protocol/SKILL.md:250` | reflect has a stop value `stopped-precondition` | `:250` "STOPs with `status: stopped-precondition`" | Correct, narrow: the value belongs to the opt-in reviewer-isolation step (`--isolate-reviewers`, `:247`). WC-4 says "for example", so not overstated. |
| C8 | `SPEC:64` (WC-6) | `CAPS:58` | "the question itself stays recorded in the Run" | `CAPS:58` quotes `[H:ask]` lines 3 and 5 (usage; "block until answered"); the durable-record facts are at `CAPS:59` ("defaults to its owning Run mailbox") and `CAPS:60` ("Timeout leaves the question pending") | **Wrong line**: the claim is true (this run's preamble also says `ask` "durably records a question in this Dispatch's Run"), but `CAPS:58` does not say it. Minor R2.5. |
| C9 | `SPEC:64`, `SPEC:73` (WC-6, 2.3) | `CAPS:116` (unchanged cite, new claim built on it) | a `--retry-of` attempt's brief names a new `--report-dir` | `CAPS:116` and `worker-start --help`: retry needs `--task` naming the failed Task; `task-update --help`: no spec flag | **Contradicted**: no Orca verb gives a retry a different brief. Prior R1.3 stays open. |
| C10 | `SPEC:65` (WC-7) | `src/superclaude/core/CLAUDE.md:73` | the Skill rule fires only on a message starting with `/sc:` | "When a message starts with `/sc:<name>` and that command's file ... says to invoke a skill, invoke the matching skill with the Skill tool before any other output" | Correct |
| C11 | `SPEC:92` (workflow row) | `sk/sc-workflow-protocol/SKILL.md:24,58,66,72` | `--output` retired; reflect wave; contract wave; Will list | `:24` E-LEGACY; `:58` Wave 4 reflect; `:66` writes `<pkg>/return-contract.yaml`; `:72` "one new package ... Never overwrites" | Correct |
| C12 | `SPEC:183` (step 4) | `pyproject.toml:38` | PyYAML is a declared dependency | `"pyyaml>=6.0",` | Correct |
| C13 | `SPEC:184` (step 5) | none cited | the transcript shows the Skill tool call | `worker-read --source transcript` on this dispatch returned `tool-call` blocks named `Skill` | Claim true; uncited (minor R1.12 note, unchanged) |
| C14 | `SPEC:195` (AC-1.1) | "its 3.2 row and the Decisions table" | load has no report | `SPEC:112` "none (see note)"; `SPEC:265` "a report file would be an unrequested addition" | Correct |
| C15 | `SPEC:147` (SA-2) | "AC-C1 excludes that one file"; "The only allowed mention of Orca is inside the contract file" | only the contract file may mention Orca | `SPEC:172` excludes two paths (`skills/ccsession-tag/` and the contract); `src/superclaude/skills/ccsession-tag/ccsession:485` runs `orca terminal rename` | **Wrong**: AC-C1 excludes one directory and one file, and the ccsession-tag skill mentions and runs Orca. Minor R2.3. |
| C16 | `SPEC:262` (Decisions) | `CAPS:73` | Orca accepts only `succeeded` or `failed` | `[H:send]` line 37 "worker_done requires --outcome succeeded or --outcome failed" | Correct |
| C17 | `SPEC:62` | "adversarial's `<output>/adversarial/`" (no line cited) | adversarial's own artifacts live under `adversarial/` | `sk/sc-adversarial-protocol/SKILL.md:435` `artifacts_dir: "<path to adversarial/ directory>"` | Correct |

Result: 12 correct, 1 claim true but uncited (C13), 1 wrong line (C8), 1 wrong statement (C15), 1 contradicted by Orca's CLI (C9), 1 correct but narrow (C7).

## 3. New findings
Scope: the 16 surface hunks, and unchanged lines a hunk breaks (Review Loop bullet 5). Panel: Wiegers (lead, requirements), Adzic, Cockburn; Fowler (lead, architecture), Nygard, Whittaker, Newman, Hohpe.

=== REQUIREMENTS ANALYSIS ===

**Karl Wiegers.** The revision makes WC-4 exact: one flag, one file, one field, one mapping (`SPEC:62`). Two checks that consume that interface were not brought along. AC-1.2 (`SPEC:196`, unchanged) still runs "7.2 live check on each P1 command with `--unattended --output <dir>`". The P1 command list includes the workflow fix (`SPEC:159`), and H2.6 now tells every brief "never `--output`" for workflow because it stops with `E-LEGACY` (`SPEC:92`; `sk/sc-workflow-protocol/SKILL.md:24`). The same list includes `/sc:load` (`SPEC:159`), which H2.12 exempted from AC-1.1 because it has no report (`SPEC:195`), yet AC-1.2 runs the full 7.2 check on it, whose steps 3-4 require the WC-4 contract (`SPEC:182-183`). **R2.1, MAJOR, blocking.**

**Gojko Adzic.** Given P0, before any command edit (`SPEC:158`), When the coordinator runs AC-0.4 on `/sc:workflow "<small change>" --handoff none`, Then AC-0.4 requires "steps 1-3 and 5-7 pass" and exempts only step 4 (`SPEC:194`). H2.11 rewrote step 3 to "its `--outcome` matches the contract's `worker_status` under WC-5" (`SPEC:182`). No P0 command writes `worker_status` (it arrives in P1, `SPEC:159`), so step 3 cannot pass for any of the three smoke runs, and AC-0.4 says "a failure here reopens section 1". The step-3 clause "its report path is the WC-4 contract path" was already unmeetable in P0 before the revision; H2.11 adds a second unmeetable clause on the same line instead of scoping step 3 for P0. **R2.2, MAJOR, blocking.**

**Alistair Cockburn.** WC-6 now names the right actor: the coordinator owns the directory per attempt (`SPEC:64`). The goal fails at the system boundary, though: the coordinator's only retry action is `worker-start --task <id> --retry-of <dispatch>`, and Orca offers no way to give that attempt a different brief (see section 1, R1.3 row). The actor is right; the actor cannot perform the step. This keeps R1.3 open rather than raising a new id.

=== ARCHITECTURE ANALYSIS ===

**Martin Fowler.** The port is now clean: `--unattended` plus `--report-dir` in, `<report-dir>/return-contract.yaml` with `worker_status` out, and no collision with any existing flag (`grep -rlE -- '--report-dir|--unattended'` over `src/superclaude/commands` and `src/superclaude/skills` printed nothing). The same-path rule for commands that already own a contract (add top-level keys, else write a separate file, `SPEC:62`) answers R1.2 without breaking adversarial's nested shape (`sk/sc-adversarial-protocol/SKILL.md:432`).

**Michael Nygard.** WC-5's `blocked → failed` still does not trip the circuit breaker (`CAPS:80`). The failure mode R1.3 described is unchanged in practice: attempt 1 writes `<report-dir>/return-contract.yaml` with `worker_status: blocked`; the coordinator retries with `--retry-of`; Orca re-dispatches the same Task, whose spec carries the same `--report-dir`; attempt 2 overwrites attempt 1's report. WC-6's own guarantee ("must not corrupt the first attempt's output", `SPEC:64`) fails.

**James Whittaker.**
- I can break this specification by **Sequence Attack**. The invariant at **WC-6 (`SPEC:64`)** fails when **the coordinator retries a failed attempt as Orca requires**. Concrete attack: before, Task T's spec says `--report-dir .dev/r/a1/`; attempt 1 writes `.dev/r/a1/return-contract.yaml` (`worker_status: blocked`); the coordinator runs `worker-start --task T --retry-of <d1>` (the only retry form, `worker-start --help`); after, attempt 2 reads the same spec and writes `.dev/r/a1/return-contract.yaml` again, replacing attempt 1's evidence. This is prior R1.3, still open.
- I can break this specification by **Sentinel Collision Attack**. The invariant at **2.1 Unattended mode (`SPEC:51`)**, "a person's run cannot switch by accident", fails when **a person types an unquoted free-text topic containing the token**. Concrete attack: `/sc:troubleshoot worker ignores --unattended flag` (no quotes); `--unattended` is a standalone token outside any quoted argument, so the mode turns on; WC-4 then finds no `--report-dir` and the run stops with an error instead of diagnosing. The behaviour is defined (a visible refusal, not lost prompts), so this is **R2.4, MINOR**: the sentence overclaims.
- I can break this specification by **Zero/Empty Attack** on **WC-4 (`SPEC:62`)** with `--unattended` and no `--report-dir`: the spec now defines the result (no work, no file, error, outcome `failed`). No finding.

**Sam Newman.** H2.8 rewrote SA-2 from "the only allowed mention of Orca in a changed command" (`SPEC-OLD:147`) to "The only allowed mention of Orca is inside the contract file ... AC-C1 excludes that one file" (`SPEC:147`). That widens the rule to every file and makes it false today: `src/superclaude/skills/ccsession-tag/ccsession:485` runs `orca terminal rename`, and AC-C1 excludes that directory as well (`SPEC:172`). The check is right; the sentence is wrong. **R2.3, MINOR** (intent is inferrable from AC-C1 and from E5, `SPEC:25`).

**Gregor Hohpe.** WC-6's added sentence "the question itself stays recorded in the Run (`CAPS:58`)" is true, but `CAPS:58` only quotes `ask`'s usage line and "block until answered"; the durable-pending facts are at `CAPS:59-60`. **R2.5, MINOR** (citation line).

### Guard Condition Boundary Table
Guards inside the surface hunks only (Review Loop bullet 5): G1 `worker_status` mapping (H2.2, `SPEC:62-63`), G3 mode selector parse rule (H2.1, `SPEC:51`), G4 report write with `--report-dir` (H2.2, `SPEC:62,64`).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 worker_status mapping | WC-4/WC-5, `SPEC:62-63` | Zero/Empty | no contract file | failed | `--outcome failed` ("or no report exists") | OK |
| G1 worker_status mapping | WC-4/WC-5, `SPEC:62-63` | One/Minimal | command result `success` | `succeeded` | `--outcome succeeded` | OK |
| G1 worker_status mapping | WC-4/WC-5, `SPEC:62-63` | Typical | WC-2 (c) gate stop | `blocked` | `--outcome failed`, `blocked_question` set | OK |
| G1 worker_status mapping | WC-4/WC-5, `SPEC:62-63` | Maximum/Overflow | an unlisted stop value, e.g. `stopped-precondition` | `failed` | "any other stop value → failed" | OK |
| G1 worker_status mapping | WC-4/WC-5, `SPEC:62-63` | Sentinel Value Match | existing contract with nested `return_contract.status` at the same path | new top-level `worker_status` | "adds the fields above as new top-level keys" | OK |
| G1 worker_status mapping | WC-4/WC-5, `SPEC:62-63` | Legitimate Edge Case | `partial` | `partial` | `--outcome succeeded`, status in first body sentence | OK |
| G3 mode selector | 2.1, `SPEC:51` | Zero/Empty | token absent | person mode | today's behaviour (SA-1) | OK |
| G3 mode selector | 2.1, `SPEC:51` | One/Minimal | `--unattended` as a standalone token | unattended | WC-2 resolutions | OK |
| G3 mode selector | 2.1, `SPEC:51` | Typical | coordinator brief with `--unattended --report-dir <dir>` | unattended | per section 3 row | OK |
| G3 mode selector | 2.1, `SPEC:51` | Maximum/Overflow | token given twice | unattended | inferrable: same as once | OK |
| G3 mode selector | 2.1, `SPEC:51` | Sentinel Value Match | token inside a person's quoted topic | person mode | "part of that argument and leaves the mode off" | OK |
| G3 mode selector | 2.1, `SPEC:51` | Legitimate Edge Case | token inside an unquoted free-text topic | unattended | WC-4 refusal (missing `--report-dir`): visible error, no work | OK (overclaim noted, R2.4) |
| G4 report write | WC-4/WC-6, `SPEC:62,64` | Zero/Empty | `--unattended` without `--report-dir` | refuse | no work, no file, error naming the flag; outcome `failed` | OK |
| G4 report write | WC-4/WC-6, `SPEC:62,64` | One/Minimal | `--report-dir` names a missing directory | write | "creates the directory if it is missing" | OK |
| G4 report write | WC-4/WC-6, `SPEC:62,64` | Typical | first attempt, fresh directory | write | contract written on every outcome | OK |
| G4 report write | WC-4/WC-6, `SPEC:62,64` | Maximum/Overflow | session dies mid-run | no write | WC-5 "no report exists" → `failed` | OK |
| G4 report write | WC-4/WC-6, `SPEC:62,64` | Sentinel Value Match | `--retry-of` attempt whose Task spec still names attempt 1's `--report-dir` | overwrite | spec assumes a new brief per attempt, which Orca cannot supply | GAP (prior R1.3, still open, `fr=8`) |
| G4 report write | WC-4/WC-6, `SPEC:62,64` | Legitimate Edge Case | WC-3 re-invocation in the same worker | overwrite own `blocked` report | "same attempt ... its report replaces the `blocked` report" | OK |

FR-10: all three surface guards enumerated, every cell populated; the one GAP row maps to open prior R1.3 (`fr=8`). No multi-stage pipeline with changing counts is in the surface, so no Quantity Flow Diagram (FR-17 not triggered).

### Numbered new findings
Blocking follows the loop's grading (`sev=critical`, `fr=8/9`, or `major` with a concrete wrong outcome). The brief's rule is stricter: any finding of any severity makes the verdict FAIL.

| # | Finding | Severity | Blocking | Section | Evidence (path:line) | Recommendation |
|---|---|---|---|---|---|---|
| 1 (R2.1) | AC-1.2 runs the full 7.2 check "with `--unattended --output <dir>`" on each P1 command, but the P1 list includes the workflow fix, which H2.6 now forbids `--output` for (it stops `E-LEGACY`), and `/sc:load`, which has no report and which H2.12 exempted from AC-1.1 only; steps 3-4 require the WC-4 contract. | MAJOR | yes | 7.3 AC-1.2 (unchanged, broken by H2.6) | `SPEC:92,159,182-183,195,196`; `sk/sc-workflow-protocol/SKILL.md:24`; `sk/sc-workflow-protocol/refs/return-contract.md:39` | Say which P1 commands AC-1.2 covers, pass each command's own output flag (none for workflow), and exempt load as AC-1.1 does (High). |
| 2 (R2.2) | 7.2 step 3 now requires the outcome to match "the contract's `worker_status`", and AC-0.4 requires step 3 to pass in P0, when no command writes `worker_status` yet; AC-0.4's smoke runs cannot pass and "a failure here reopens section 1". | MAJOR | yes | 7.2 step 3 (H2.11); 7.3 AC-0.4 (H2.12) | `SPEC:158,159,182,194` | Scope step 3's contract clauses to P1 and later, or say AC-0.4 checks step 3 against the command's existing report (High). |
| 3 (R2.3) | SA-2 now says the only allowed Orca mention is in the contract file and that "AC-C1 excludes that one file"; AC-C1 also excludes `skills/ccsession-tag/`, which runs `orca terminal rename`. | MINOR | no | 5 SA-2 (H2.8) | `SPEC:147,172,25`; `src/superclaude/skills/ccsession-tag/ccsession:485` | Restore "in a changed command" or name the ccsession-tag exception (Low). |
| 4 (R2.4) | "a person's run cannot switch by accident" overclaims: an unquoted free-text topic containing `--unattended` switches the mode; the result is a defined refusal, not lost prompts. | MINOR | no | 2.1 Unattended mode (H2.1); 9 D1 (a) (H2.15) | `SPEC:51,62,228` | Narrow the sentence to quoted arguments (Low). |
| 5 (R2.5) | WC-6 cites `CAPS:58` for "the question itself stays recorded in the Run"; that line quotes only `ask`'s usage; the support is `CAPS:59-60`. | MINOR | no | 2.2 WC-6 (H2.2) | `SPEC:64`; `CAPS:58,59,60` | Cite `CAPS:59-60` (Low). |

Prior R1.3 (MAJOR, `fr=8`, blocking) stays open; it is a carried finding, not a new one, and is listed in the Diffgate block as `PRIOR R1.3 open`.

## 4. Diffgate run record
- Read-only calls only, as the command requires: `status` (section "Loop status") and `check --dir .dev/orca-command-refactor/review/diffgate-loop --report .dev/orca-command-refactor/review/spec-panel-round2.md --dry-run` (2026-11-09), which printed `"exit": 0`, `"message": "dry run: report would be accepted; nothing written"`, `"errors": []`, `"verdict": "FAIL"`, `"blocking": 3`, `"blocking_ids": ["R2.1", "R2.2", "R1.3"]`, `"acceptance": "clean"`, `"deferred": []`, `"proxy_all": 3`, `"halt": null`.
- Not run by this worker: `check` without `--dry-run` (records the report, writes `result-r2.json`, `reviser-brief-r2.md` and `close-r2.md`, whose `verdict_line` becomes this report's last line). That is the coordinator's step.
- After a FAIL at review 2 the loop allows one more fix cycle; review 3 is the last (`~/.claude/commands/sc/spec-panel-diffgate.md`, Review Loop bullet 4).
- Note: the brief places this report at `review/spec-panel-round2.md`, outside `--diffgate-dir`; `check` accepts any `--report` path, and the dry run above used this one.

## 5. Verdict
**FAIL.** Under the brief's rule any finding of any severity fails, and this review has 3 blocking findings (R2.1, R2.2 and open prior R1.3) plus 3 minor notes (R2.3-R2.5) and 6 declined round-1 minor notes (R1.8-R1.13). The diffgate dry run derives the same verdict (`"verdict": "FAIL"`, section 4). No Self-Audit is required because the verdict is not PASS; what was checked is listed in sections 1-3.

Blocking findings for the next reviser:
1. **R1.3 (open):** a `--retry-of` attempt cannot receive a new brief in Orca, so WC-6's per-attempt `--report-dir` does not happen and a retry overwrites attempt 1's report (`SPEC:64,73`; `worker-start --help`; `task-update --help`; `CAPS:116`).
2. **R2.1:** AC-1.2 (`SPEC:196`) passes `--output` to workflow (forbidden by `SPEC:92`) and runs the contract check on `/sc:load` (no report, `SPEC:112,195`).
3. **R2.2:** 7.2 step 3 (`SPEC:182`) requires `worker_status`, which no P0 command writes, yet AC-0.4 (`SPEC:194`) requires step 3 in P0.

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| Repo root | the spec's stated root (`SPEC:4`); this worktree | The brief names this worktree; the stated root does not exist (prior minor R1.9). README's worktree line (`.dev/orca-command-refactor/README.md:8`) names the same missing path; the brief overrides it. |
| R1.3: open prior vs new finding | mark `PRIOR R1.3 open`; mark resolved and raise a new id | The revision's mechanism (new brief per retry) does not exist in Orca, so R1.3's stated outcome (a `--retry-of` worker overwrites attempt 1) still happens. Open is the accurate status. |
| R1.6: resolved vs open | open because AC-1.2 has the same conflict; resolved for AC-1.1 plus a new finding | R1.6's text and outcome name AC-1.1, which is fixed. The AC-1.2 conflict is filed as R2.1, anchored on the hunk (H2.6) that makes AC-1.2 contradict the spec. |
| R2.2 severity | minor (an implementer may infer step 3 also uses the existing report); major | AC-0.4 literally says "steps 1-3 ... pass" and "a failure here reopens section 1", so a literal run produces a false signal against the core decision. Major with a concrete outcome. |
| R2.4 severity | major (SA-1 break); minor | WC-4's refusal rule makes the accidental switch a visible error with no work done, so no silent behaviour change; the defect is an overclaiming sentence. |
| Verdict line | write `verdict:` myself; leave it to the coordinator's `check` | The command reserves it for the coordinator (`~/.claude/commands/sc/spec-panel-diffgate.md`, Review Loop bullet 3); the brief's PASS/FAIL is given in section 5 prose. |
| Live Orca evidence | cite help text only; also read this worker's own transcript | `worker-read` on this worker's own dispatch is read-only and settles whether the R1.4 check is feasible; done once, with `--limit 200`. |

## Diffgate findings
PRIOR R1.1 resolved by=H2.2
PRIOR R1.2 resolved by=H2.2
PRIOR R1.3 open quote="each attempt's brief, a `--retry-of` retry included, names a new `--report-dir`"
PRIOR R1.4 resolved by=H2.2
PRIOR R1.5 resolved by=H2.10
PRIOR R1.6 resolved by=H2.12
PRIOR R1.7 resolved by=H2.1
FINDING R2.1 sev=major at=196 via=H2.6 via_quote="never `--output` (retired, `E-LEGACY`, R1.1)" anchor="each P1 command with `--unattended --output <dir>`" outcome="the AC-1.2 run of the P1 workflow fix stops with E-LEGACY and sends --outcome failed, and the /sc:load run writes no contract so 7.2 steps 3-4 fail, so P1 cannot pass or the implementer adds a load contract against its row" :: AC-1.2 passes --output to workflow and runs the contract check on load
FINDING R2.2 sev=major at=182 hunk=H2.11 anchor="matches the contract's `worker_status` under WC-5 (R1.2)" outcome="AC-0.4 requires step 3 in P0, when no command writes worker_status, so all three P0 smoke runs fail step 3 and section 1 is reopened on a false signal" :: step 3 needs worker_status that no P0 command writes
FINDING R2.3 sev=minor at=147 hunk=H2.8 anchor="AC-C1 excludes that one file (R1.5)" :: SA-2 now forbids the ccsession-tag Orca use that AC-C1 also excludes
FINDING R2.4 sev=minor at=51 hunk=H2.1 anchor="so a person's run cannot switch by accident (R1.7)" :: an unquoted free-text topic containing the token still switches the mode
FINDING R2.5 sev=minor at=64 hunk=H2.2 anchor="the question itself stays recorded in the Run (`CAPS:58`)" :: CAPS:58 does not state the recorded-question fact


Reviser brief: your task list is `.dev/orca-command-refactor/review/diffgate-loop/reviser-brief-r2.md` (blocking ids R2.1, R2.2, R1.3). Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; write the fix map only inside your own disposition file, as a `## Diffgate fixmap` block with a `doc_sha:` first line and one line per changed hunk naming its blocking ids, or `declined <id> <reason>`; run the script's read-only `fixcheck --dry-run --map <disposition file>` until it exits 0; report the byte size before and after, which `fixcheck` prints. The next review refuses to open while any hunk maps to no listed finding.

verdict: FAIL
