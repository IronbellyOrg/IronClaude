review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `ecccef2cd605be2429bee0a2ca58d7ed10decc68e84a2d03445f68dc64843d1c`
- baseline: none given, `--re-review` not given: this is a first review of the whole document, labelled whole-document audit
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`
- panel (focus requirements, architecture; Whittaker always active): Wiegers (lead), Adzic, Cockburn, Fowler (lead), Newman, Hohpe, Nygard, Whittaker
- evidence rule: only `.dev/orca-command-refactor/README.md` and the three files under `inventory/` exist in the sandbox. Every `src/`, `~/.claude`, Orca-JS and `.dev/codegraph-migration` / `EVIDENCE.md` citation was checked only as quoted inside those inventories and is marked UNVERIFIED where it is not checkable. Spec citations of the form `INV-A:N`, `INV-B:N` and `CAPS:N` were checked against the inventory line named; a sample of 40 of them matched (for example `CAPS:44-45`, `CAPS:73`, `CAPS:97-101`, `CAPS:145-149`, `INV-A:62`, `INV-B:272`, `INV-B:311`).

## Summary

The decision (Orca on top, commands stay the units of work) is supported by the inventories and is internally consistent, and the counts conserve. The spec has one blocking defect: WC-4's rule for placing the contract file contradicts WC-11 for the very `--output <file>` commands the spec lists. Eleven Medium findings and several minor notes follow.

## === REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL as labelled by Wiegers; blocking) WC-4's file-parent rule makes parallel workers share one contract file, which WC-11 forbids

- Expert: Wiegers (traceability and consistency), Whittaker (Divergence attack, section below).
- Location: `specs/orca-worker-contract-spec.md:62` (WC-4), `:69` (WC-11), `:87` (init-lite `--output <file>`), `:90` (tdd `--output <file>`), `:120` (spec-panel "add `--output`"), `:73` (section 2.3), `:195-196` (AC-1.1, AC-1.2).
- Stated text: WC-4 writes `<output-dir>/return-contract.yaml` and says "when `--output` is a file, `<output-dir>` is that file's parent directory". WC-11 says "Two workers in one worktree must never write the same file."
- Grading sentence: An implementer who follows the stated text as written builds a contract written to the parent directory of each `--output <file>`, so two workers that write sibling files (two `/sc:tdd` workers with `--output docs/<domain>/TDD_A.md` and `docs/<domain>/TDD_B.md`, the default layout quoted at `inventory/commands-b.md:222`, or two `/sc:spec-panel` or `/sc:init-lite` workers with files in one folder) both write `<dir>/return-contract.yaml`, and that is wrong because WC-11 forbids two workers writing the same file and because worker A's `worker_done --report-path` then points at a file that worker B overwrote, so the coordinator reads the wrong `status`.
- This is two stated texts that contradict each other, so it is blocking. No guess about the implementer's reading is needed: the collision follows from the file-parent rule whenever two output files share a folder, and the spec's own default layout produces that. The same collision exists for this run itself (`review/audit.md` and `review/spec-panel.md` would share `review/return-contract.yaml`).
- Side effect: the contract is also dropped into tracked folders such as `docs/<domain>/`, an unrequested file in a person's tree (SA-3, `:148`).
- Recommendation (prefer narrowing): make the contract path independent of `--output` when `--output` is a file. Smallest fix: for a file-valued `--output`, name the contract `<output-file-stem>.return-contract.yaml` beside the file, or require the brief to pass a directory-valued flag for the contract. Rationale: one name per worker output removes the collision without a new mechanism. Priority: High. Quality impact: Consistency +2, Testability +1.

## Medium findings (warnings, not blocking; listed under follow-up candidates)

Each Medium finding is a requirement the document never states, or needs a guess that the implementer picks the worse of two allowed readings. None triggers a revision.

### M-1 (MAJOR as labelled; Medium by grading) WC-6 "fresh output directory" does not say who creates it, and one reading breaks WC-4's "known before dispatch"
- Expert: Wiegers, Hohpe. Location: `:64` (WC-6), `:62` (WC-4), `:73`; used by about 20 rows in column "Resume (WC-6)" of `:99-125`.
- WC-6 says a command without a resume flag "writes each run into a fresh output directory". If the command creates a new directory per run, the contract is no longer at the path the brief gave before dispatch (WC-4); if the coordinator supplies a new directory per attempt, the coordinator brief (section 2.3, `:73`) never says so and WC-6's owner "Command" is wrong. Recommendation: state in section 2.3 that the coordinator passes a new output directory per attempt (`--retry-of` included) and that the command never creates one itself. Priority: Medium.

### M-2 (MAJOR as labelled; Medium) AC-3.2 and the roadmap row start fresh in the same directory, overwriting the first attempt
- Expert: Nygard, Whittaker (Sequence attack). Location: `:205` (AC-3.2), `:118` (roadmap row), `:64` (WC-6).
- With an existing `<dir>/.session-memory.md` and no resume flag, roadmap "starts fresh" in `<dir>`. WC-6 says a retry "must not corrupt the first attempt's output". A coordinator that retries with the same `--output` and forgets the resume flag destroys the earlier run. This needs the guess that the coordinator reuses the directory, so it is Medium. Recommendation: under `--unattended`, a non-empty output directory without the resume flag resolves as blocked (WC-2 (c)) instead of starting fresh. Priority: Medium.

### M-3 (MAJOR as labelled; Medium) No rule for nested `/sc:` invocations: `--unattended` propagation and contract-name collision
- Expert: Fowler, Hohpe. Location: `:60` (WC-2), `:122` (tasklist is the only row that passes `--unattended` down), `inventory/commands-a.md:39,44` (brainstorm calls adversarial; cli-eval create calls spec-panel and adversarial), `inventory/commands-b.md:119,121,271` (release-split calls brainstorm and adversarial; workflow calls reflect).
- Only tasklist to reflect is specified. Every other nested command call either inherits `--unattended` (unstated) or runs in person mode and can stall, and two commands writing `<output>/return-contract.yaml` in the same directory overwrite each other. Recommendation: add one sentence to the contract file requirements: a nested `/sc:` call receives `--unattended` and its own output subdirectory. Priority: Medium.

### M-4 (MAJOR as labelled; Medium) Claude Code tool-permission prompts are an unaddressed stall class
- Expert: Nygard, Cockburn. Location: `:60` (WC-2), `:59` (WC-1), `:22` (E2), `inventory/orca-capabilities.md:50,129`.
- WC-1 covers launch-path prompts and WC-2 covers command-defined gates. A worker is an interactive Claude session; a tool-approval prompt (Write, Bash, `uv run`, `gh api`) parks it the same way and is invisible to the coordinator (`CAPS:129`). The spec says nothing about the worker's permission mode or allow list. Whether such prompts appear depends on the user's settings: UNVERIFIED. Recommendation: add a brief-template line that the worker launch must have the needed tools pre-approved, and keep 7.2 step 2 (`agentWait` check) as the detector. Priority: Medium.

### M-5 (MAJOR as labelled; Medium) The coordinator's handling of a silent stall or a missing `worker_done` is not specified
- Expert: Nygard, Newman. Location: `:44` (names the "silent stall" as the real failure mode), `:73` (section 2.3 starts after `worker_done`), `:180-186` (7.2).
- The spec says the coordinator sees a stall only through `agentWait` or a missing report, but gives no rule for what it does next (wait limit, `ask` versus `worker-stop`, retry with `--retry-of`). Orca's recovery rules exist (`CAPS:126`, `CAPS:111`, `CAPS:116`) but are not tied in. Recommendation: one row in section 2.3 pointing to those rules and a wait limit per command class. Priority: Medium.

### M-6 (MINOR/Medium) Commands with a fixed output location and no output flag: contract location is undefined or pollutes the root
- Expert: Wiegers, Whittaker (Zero/Empty attack). Location: `:62` ("a command with a fixed output location writes the contract there"), `:86` (index-repo, `PROJECT_INDEX.md` at the repo root, `inventory/commands-a.md:53`), `:85` (cleanup-audit fixed `.claude-audit/`), `:69` (WC-11).
- For index-repo the rule puts `return-contract.yaml` in the repo root, and a second command with a root-level location would collide. WC-11 only gets an acceptance check for `/sc:save` (AC-3.4, `:207`). Recommendation: say where the contract goes when the coordinator can pass no directory. Priority: Medium.

### M-7 (Medium) AC-C1 scans the two core files that P0 creates or edits, and SA-2 only exempts "a changed command"
- Expert: Fowler. Location: `:172` (AC-C1 scans `src/superclaude/core`), `:147` (SA-2), `:158` (P0 adds `WORKER-CONTRACT.md` and an Orca section to `HOW-WE-WORK.md`), `:25` (E5, HOW-WE-WORK has no Orca mention today).
- An implementer who writes `orca orchestration ...` in `WORKER-CONTRACT.md` or in the routing-guide Orca section fails AC-C1; one who uses the placeholder `ORCA` (as 7.2 does, `:167`) passes it, because grep is case-sensitive. The spec does not say which. Recommendation: either exempt the two files in AC-C1 or require the placeholder form there. Priority: Low-Medium.

### M-8 (Medium) WC-4's four-value `status` set versus contracts that already exist
- Expert: Wiegers, Adzic. Location: `:62` ("keep their fields and add the missing ones"), `:183` (7.2 step 4 asserts the four values), `inventory/commands-b.md:272` (workflow contract has `status`; its value set is not inventoried), `inventory/commands-b.md:112`.
- If an existing `status` field uses other values, "keep their fields" and the step 4 assertion cannot both hold. The existing vocabularies are UNVERIFIED (not in the inventories). Recommendation: list each existing contract's `status` values in section 3.1 or map them in WC-5. Priority: Medium.

### M-9 (Medium) Some requirements have no acceptance check, and WC-3's "answer as a flag" has no flag for many gates
- Expert: Adzic, Crispin-style testability. Location: `:61` (WC-3), `:64` (WC-6), `:69` (WC-11), `:70` (WC-12), `:109` (implement), `:232-236` (D2), `:166-210` (section 7).
- No AC exercises the `ask` path (WC-3), the resume or fresh-run behaviour (WC-6), parallel-safe writes beyond `/sc:save` (WC-11) or `check` before `worker_done` (WC-12). WC-3 says the worker re-invokes the command "with the answer as a flag", yet gates such as the tdd clarification, the recommend question and cli-portify approval have no such flag in section 3. For `/sc:implement`, WC-3 as written lets the worker ask the coordinator, while `inventory/commands-a.md:66` says a coordinator's reply is not a Ruling; D2 settles it only in Phase 4. Recommendation: add one AC each, and say in WC-3 that gates with no answer flag resolve as blocked only. Priority: Medium.

### M-10 (Medium) Section 1.4 point 2 versus argv prompt injection
- Expert: Nygard. Location: `:44`, `inventory/orca-capabilities.md:47`, `inventory/orca-capabilities.md:52`.
- The spec says a command's own question "comes after readiness, so it does not fail `worker-start`". `CAPS:47` records that for Claude the task is passed on the command line, so the command may start running before Orca sees the fresh input box. Whether an immediate `AskUserQuestion` then fails `agent_readiness` is not shown by `EVIDENCE.md:39` (a wrapper prompt) and is UNVERIFIED. WC-2 forbids the prompt in unattended mode either way, so the effect is limited to the accuracy of the stated risk. Recommendation: soften the sentence to UNVERIFIED. Priority: Low.

### M-11 (Medium, UNVERIFIED) Completeness of the "43 commands" scope
- Expert: Cockburn. Location: `:76` ("The 43 commands in `cmd/`"), `inventory/commands-a.md:3`, `inventory/commands-b.md:3`, `:25` (E5).
- Each inventory fixes its scope as an explicit list of names, not a directory listing. The skills catalog shown to this reviewer also lists `sc:graph`, `sc:impact` and `sc:issue`, which neither inventory mentions, and `sc:issue` is described there as creating an Orca worktree. If those commands exist in the audited worktree, the count, E5 ("no command calls Orca today") and AC-C1 are wrong. This cannot be checked in the sandbox (no `src/`). Recommendation: record `ls src/superclaude/commands | wc -l` in the spec. Priority: Medium.

## === ARCHITECTURE ANALYSIS ===

Fowler (lead), Newman, Hohpe, Nygard. The boundary is sound: Orca coordination stays outside commands (`:16`, `:28-39`), rejection reasons R1-R5 hold against `CAPS:97-103,145-150`, and the single shared contract file follows the installed-path rule. Architecture findings are B-1 (one flag, `--output`, means file or directory depending on the command, which is the root cause of the collision) and M-1, M-3, M-5 above.

Further architecture notes (minor, no verdict effect):
- N-1 `--output`, `--output-dir` and `--report-dir`-style names differ per command (`inventory/commands-a.md:38` uses `--output-dir`; `:62` writes "`--output` / `--output-dir`"). A single directory-valued flag name for the contract would remove the file-versus-directory special case. Fowler.
- N-2 Decisions table `:263` maps `partial` to `succeeded`, so a dependent Task starts on a partial result unless the coordinator reads the body first (`:73`). Documented trade-off; no change required. Hohpe.
- N-3 Section 6 calls P1 "commands with no gate" (`:159`) but business-panel, explain, test and index carry refusal or "does not wait" rules in `:102,108,111,123`. Wording only. Cockburn.
- N-4 Section 6 says phases 1-3 "need no user decision" (`:154`) while D1 and D4 (`:227-247`) affect P1 and P2 commands; section 9 (`:225`) resolves it by "proceed on the recommendations". Wording only.
- N-5 SA-3 (`:148`) allows the contract when the new output flag is passed, WC-4 (`:62`) writes it in unattended mode only. Align the wording.
- N-6 E3 (`:23`) cites `invocation_method: "skill-direct"` as support, while section 1.4 point 1 (`:43`) says that run proves only the nested route. Both can be true; say so in E3. UNVERIFIED (source not in sandbox).
- N-7 AC-C5 (`:176`) fails on any edited existing line, so adding a flag to a Usage line fails it unless the flag goes on a new line.
- N-8 `--post-pr` (`:100`, WC-9) is named as an existing explicit flag; the inventory shows only `--no-post-pr` (`inventory/commands-a.md:38`). UNVERIFIED that `--post-pr` exists.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Positioned after Fowler and Nygard. Scope: specification correctness only.

- **FR-2.1 Zero/Empty.** I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (`:62`)** fails when **no directory is passed or the command has a fixed root location**. Concrete attack: `/sc:index-repo --unattended` with no flag; state before: no contract; state after: `return-contract.yaml` in the repo root, a second root-level command overwrites it. Severity MAJOR; graded Medium (M-6).
- **FR-2.2 Divergence.** I can break this specification by **Divergence Attack**. The invariant at **WC-4 (`:62`) versus WC-11 (`:69`)** fails when **`--output` is a file and two workers share the parent folder**. Concrete attack: workers A and B run tdd with `docs/x/TDD_A.md` and `docs/x/TDD_B.md`; both write `docs/x/return-contract.yaml`; B finishes last; A reports `--outcome succeeded` with a path whose `status` is B's `blocked`. Finding B-1, blocking.
- **FR-2.3 Sentinel Collision.** I can break this specification by **Sentinel Collision Attack**. The invariant at **the filename `return-contract.yaml` (`:62`, `:261`)** fails when **a nested command or an existing contract uses the same name in the same directory**. Concrete attack: release-split runs nested brainstorm with the same `--output`; brainstorm writes `<output>/return-contract.yaml` (`inventory/commands-a.md:39`), release-split overwrites it later; an early stop leaves the nested one as the parent's report. Findings M-3, M-8.
- **FR-2.4 Sequence.** I can break this specification by **Sequence Attack**. The invariant at **WC-6 (`:64`) and AC-3.2 (`:205`)** fails when **a retry runs without the resume flag in an existing directory**. Concrete attack: roadmap attempt 1 dies after Wave 3; the retry omits the resume flag; "starts fresh" overwrites `roadmap.md` and `.session-memory.md` of attempt 1. Finding M-2. Also: WC-2 (c) writes `blocked`, then WC-3 re-invokes with an answer; the second run overwrites the blocked contract in the same directory (acceptable, but unstated; folded into M-1).
- **FR-2.5 Accumulation.** I can break this specification by **Accumulation Attack**. The invariant at **WC-11 (`:69`)** fails when **N workers in one worktree use commands with a fixed output location** (`.claude-audit/` at `:85`, `PROJECT_INDEX.md` at `:86`). The spec limits this to prose ("one audit per worktree at a time") with no check. Folded into M-6. No overflow or circuit-breaker defect found: `CAPS:80` says a worker's own `failed` report does not count toward the three-failure breaker.

## Guard Condition Boundary Table

Trigger present (thresholds, status sets, boolean flags). Classes left out are listed with one-line reasons. Nygard built, Crispin checked completeness, Whittaker attacked entries.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| readiness limit (WC-1) | `:59` | Typical | prompt answered/fallback at 30 s | true | passes (`CAPS:49`) | OK |
| readiness limit (WC-1) | `:59` | Maximum/Overflow | fallback above about 45 s | false | start fails (`CAPS:49`) | OK |
| readiness limit (WC-1) | `:59` | Legitimate Edge Case | `--timeout-ms` raised | true | allowed per start (`CAPS:45`); upper bound UNVERIFIED (`CAPS:54`) | OK |
| `--unattended` switch (D1) | `:51`, `:227-229` | Zero/Empty | flag absent | false | today's behaviour (SA-1, `:146`) | OK |
| `--unattended` switch (D1) | `:51` | Typical | flag present | true | WC-2 gate resolutions per section 3 | OK |
| `--unattended` switch (D1) | `:60` | Sentinel Value Match | nested `/sc:` call without the flag | false | not specified | GAP (M-3) |
| gate resolution (WC-2) | `:60` | Typical | gate hit, no default, no flag | true | blocked contract and stop | OK |
| gate resolution (WC-2) | `:61` | Legitimate Edge Case | blocked, answer arrives via `ask` | true | re-invoke "with the answer as a flag"; no flag exists for several gates | GAP (M-9) |
| `<output-dir>` (WC-4) | `:62` | Zero/Empty | no directory passed | n/a | undefined for fixed-root commands | GAP (M-6) |
| `<output-dir>` (WC-4) | `:62` | Typical | directory passed | true | `<dir>/return-contract.yaml` | OK |
| `<output-dir>` (WC-4) | `:62`, `:69` | Legitimate Edge Case | `--output` is a file, sibling files exist | true | parent folder shared by workers | GAP (B-1, blocking) |
| `<output-dir>` (WC-4) | `:62` | Sentinel Value Match | nested command writes same filename | true | not specified | GAP (M-3) |
| `status` (WC-4/WC-5) | `:62-63` | Typical | succeeded/partial/failed/blocked | true | mapped to Orca outcome | OK |
| `status` (WC-4/WC-5) | `:63` | Zero/Empty | no report exists | true | `--outcome failed` | OK |
| `status` (WC-4/WC-5) | `:62`, `:183` | Sentinel Value Match | existing contract with another value set | false | not specified (vocabulary UNVERIFIED) | GAP (M-8) |
| resume or fresh run (WC-6) | `:64`, `:205` | Zero/Empty | no resume flag, directory non-empty | true | roadmap "starts fresh" in same directory | GAP (M-2) |
| resume or fresh run (WC-6) | `:64` | Legitimate Edge Case | fresh directory | true | who creates it is unstated | GAP (M-1) |
| wait split (WC-10) | `:68` | Typical | single wait under 5 min | true | no split | OK |
| wait split (WC-10) | `:68`, `:210` | Maximum/Overflow | single wait over 5 min (eval 3600 s) | true | split into waits of at most 4 min; checked only in AC-4.3 | OK |
| outward default (WC-9) | `:67` | Typical | `--unattended` without authorization flag | true | outward action off | OK |
| outward default (WC-9) | `:67`, `:100` | Legitimate Edge Case | authorization via a flag the command lacks | true | `--post-pr` existence UNVERIFIED | GAP (N-8) |
| `--monitor 1` (pr-submit) | `:114` | Typical | refused under `--unattended` | true | refused | OK |
| ask timeout (WC-3) | `:61` | Maximum/Overflow | ask times out | true | resume the same message ID | OK |

Classes omitted: "One/Minimal" for all guards (no case differs from Typical); "Maximum/Overflow" for the `--unattended` switch and `status` (boolean and enumerated, cannot overflow); "Sentinel" for the readiness limit (no sentinel value). Every GAP above has a finding in this report, so FR-8 and FR-9 are satisfied: one is blocking (B-1), the rest are Medium because none names a wrong outcome without an extra assumption.

## Pipeline Dimensional Analysis (FR-17)

Not triggered as a data pipeline: the spec has no stage whose output count differs from its input count except the command classification. Count conservation was checked instead: 21 + 22 = 43 commands (`inventory/commands-a.md:3,73`, `inventory/commands-b.md:3,278`); 5 + 5 = 10 ready (`:83-92` has 10 rows), 13 + 14 = 27 needs-change (`:99-125` has 27 rows), 3 + 3 = 6 coordinator-only (`:132-137` has 6 rows); 10 + 27 + 6 = 43. Phase lists: P2 row lists 15 commands and the section 3 rows marked P2 also number 15 (11 in 3.2 plus reflect, release-split, tdd, troubleshoot). No mismatch.

## Panel consensus and disagreements

- Consensus: the decision, the rejection of the alternative, the standalone-safety section and the phase order are sound and well evidenced.
- Consensus: B-1 must be fixed before any command is edited, because every later phase builds on the contract path.
- Disagreement (resolved by grading): Nygard and Whittaker rated M-2 and M-5 as MAJOR; under the grading rule they need a coordinator error or an unstated procedure, so they are Medium.

## Coverage

Read in full: the spec (lines 1-285), `README.md`, all three inventories, the command definition and the review-loop prompts file. Checked: internal consistency of WC-1 to WC-12, SA-1 to SA-6, sections 3 to 9, all count and phase lists, and a 40-citation sample against the inventories. Not checked (UNVERIFIED, outside the sandbox): every `src/superclaude/...` line, Orca JS and `orca-ide` output, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `CLAUDE.md` line numbers, and the claimed 2026-11-02 greps and citation validator runs (`:11`, `:25`, `:285`). Whole-document assurance: this is a first review, not a scoped PASS.

## Follow-up candidates

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11.
Minor notes: N-1 to N-8.
The session that ran this review could not ask the user whether to open an issue for them (this run is a non-interactive worker); the coordinator should ask the user once for this loop. No issue was created.

## Brief clauses overridden

None. The brief (read `README.md` first, cite `path:line`, write only the output file) was followed as written.

## Reviser brief

Blocking finding ids: **B-1**

Contract for the reviser (restated from the command's Review Loop, bullet 6; you read this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, with the bytes added and deleted per finding id. Repair only B-1 in `specs/orca-worker-contract-spec.md` (WC-4 at line 62, and the rows at lines 87, 90 and 120 only if the repair needs them). Leave the Medium findings and minor notes alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
