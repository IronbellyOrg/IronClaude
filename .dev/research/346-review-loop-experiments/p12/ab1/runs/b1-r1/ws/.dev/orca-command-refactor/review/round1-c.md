review: 1 of 3

# /sc:spec-panel review, round 1 (critique mode, focus requirements,architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (57763 bytes)
- baseline: none (first review; no `--re-review`, no `--baseline`)
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:29-36`. This file is ONE of the three first-review reports; the three-report MERGE and the VERIFY step belong to the coordinator (`document_review_loop_prompts.md:34-35`).
- Improve step: not run; no revised specification written, candidate untouched.
- Citation key: `S:N` = line N of the candidate. `INV-A/B`, `CAPS` = the three files under `.dev/orca-command-refactor/inventory/` (`commands-a.md`, `commands-b.md`, `orca-capabilities.md`). Source-tree citations (`cmd/`, `sk/`, `CLAUDE.md`, `Makefile`, `src/...`) and Orca's live guides cannot be checked in this sandbox (only the three inventories, the README and the candidate exist), so every claim resting on them is UNVERIFIED here and was taken only as the inventories report it.
- Coverage: whole candidate read (286 lines); all 43 per-command rows counted; every `INV-*` and `CAPS:*` citation I used was opened and compared with the quoted claim. Not covered: any claim that rests only on a source-tree file (UNVERIFIED), the spec's own "340 citations re-read" claim (S:285, UNVERIFIED).

## Quick checks that held

- 10 + 27 + 6 = 43 and the section 3 rows match the inventories' split (A: 5/13/3, `INV-A` summary; B: 5/14/3, `INV-B:280,289`). Phase lists add up (P1 9, P2 15, P3 4, P4 3).
- `CAPS` citations for WC-1, WC-3, WC-5, WC-6, WC-7, WC-8, R1 to R5, D1, D5 point at lines that say what the spec claims (e.g. `CAPS:97-103` depth 1, `CAPS:58-64` ask/resume, `CAPS:72-77` worker_done/outcome).
- Two citations do not point at the claimed line (Medium M5 below).

## === REQUIREMENTS ANALYSIS ===

Experts in order: Wiegers (lead), Adzic, Cockburn.

### B1 (CRITICAL by label, blocking by consequence). WC-3 lets a blocked gate be answered by `ask`; AC-2.2 and AC-4.1 require the opposite outcome for the same input
- Expert: Wiegers (testability), Adzic (example), Whittaker (Divergence Attack: both branches apply at once).
- Texts: S:60 (WC-2 (c): on a gate the command writes `status: blocked` "and stops"); S:61 (WC-3: "When a gate would resolve as blocked and the worker session holds a preamble, the session **may instead** ask the coordinator once ... wait, then re-invoke"); S:200 (AC-2.2: gate-trigger run, pass = "`worker_done --outcome failed`; contract `status: blocked` ...; step 2 never shows `agentWait`"); S:208 (AC-4.1 same shape). `CAPS:58,129` (an `ask`-blocked worker is healthy; `agentWait` is how a parked worker shows).
- Wrong outcome: an implementer who follows WC-3 as written builds a worker session that, on the gate input of AC-2.2, calls `ask` and waits. That session sends no `worker_done --outcome failed` and the run is parked, so AC-2.2 fails for a worker that followed the spec. The acceptance criterion cannot be passed by a stated, permitted behaviour. Neither WC-3 nor S:73 (section 2.3, the brief) says which of the two the coordinator selects per Task, so the coordinator cannot make AC-2.2 deterministic.
- Recommendation: state per Task which resolution the brief selects (for example a brief line "on a blocked gate: stop and report" versus "on a blocked gate: ask"), and make AC-2.2 and AC-4.1 name the "stop and report" form.
- Priority: High. Quality-impact: removes the one acceptance check for the whole gate-conversion phase.

### B2 (CRITICAL by label, blocking by consequence). WC-4 puts the report at `<output-dir>/return-contract.yaml`, but the spec's own rows pass file-valued `--output` for tdd, init-lite and spec-panel, and AC-2.2 tests tdd that way
- Expert: Wiegers (traceability), Adzic.
- Texts: S:62 (WC-4: `<output-dir>` "is the directory the coordinator passed (`--output` / `--output-dir`)", path "known before dispatch"); S:90 (tdd: "`--output <file>`", report = "the TDD at `--output`"); S:87 (init-lite: "`--output <file>`"); S:120 (spec-panel: "add `--output`", contract added); S:200 (AC-2.2: "`/sc:tdd "auth" --unattended --output <file>` ... contract `status: blocked`"); S:195-196 and S:182 step 4 (`test -s <contract>` on that path); S:148 (SA-3 ties the contract to "the new output flag"). Evidence: `INV-B:222,225` (tdd `--output` is the final TDD file), `INV-B:182,185` (spec-panel has no output flag today). Outside the listed evidence, the command definition `command.md:460-461` (this sandbox) keeps `--output` file-valued and uses a separate `--report-dir` for the contract directory, which is the split the spec does not make.
- Wrong outcome: an implementer who follows WC-4 literally for tdd builds the contract at `<file>/return-contract.yaml`, a path under a regular file that cannot exist. A worker told `--output docs/x/TDD_AUTH.md` has no directory to write to, so the "known before dispatch" path (S:62, S:73) does not exist and AC-2.2 step 4 cannot be run.
- Recommendation: add one directory-valued flag for the contract (or state the rule "contract goes in the directory of a file-valued `--output`, or in `--output` when it is a directory") and apply it to the rows at S:87, S:90, S:120 and to AC-2.2.
- Priority: High.

### Medium findings (follow-up candidates, never block, never in the Reviser brief)
- **M1. `--post-pr` is relied on but never shown to exist.** S:100 and S:67 (WC-9: a default turns on "only through the command's own explicit flag") say posting returns "only with an explicit `--post-pr` in the brief". The inventories only record the negative flag `--no-post-pr` (`INV-A:38,78`); no positive flag appears in them (grep over all three inventories). The same row says "Other required change: none". An implementer must guess whether to add the flag or whether the outward action is simply unreachable under `--unattended`. AC-2.4 (S:202) only tests the off case. Missing requirement, so Medium.
- **M2. AC-C1 and SA-2 disagree about the contract file.** S:172 (AC-C1: the grep over `src/superclaude/{commands,skills,agents,core}` must print nothing, "every phase", S:169); S:147 (SA-2: "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file"); S:158 (P0 adds `WORKER-CONTRACT.md` and "an Orca section" to `HOW-WE-WORK.md`, both under `core/`, which AC-C1 scans). If either file writes `orca orchestration ask` (the form WC-3 describes, S:61) AC-C1 fails; the spec does not say the allowed mention avoids that form or that AC-C1 excludes those two files. Needs a guess about wording, so Medium.
- **M3. AC-1.1 requires a `## Unattended mode` section in every 3.1 and 3.2 command in P1, while other text defers or excludes some.** S:159 and S:195 ("every command in sections 3.1-3.2"); S:154 and S:162 (implement, post-release, pr-submit wait for D2 to D4 in P4); S:240 (D3 (a): "no pr-submit changes in Phase 4"); S:84 and S:87 (brainstorm and init-lite: "Small fix: None"); `INV-B:90` (pr-submit "Will Not: run headless", `cmd/pr-submit.md:85` per the inventory, UNVERIFIED here), which neither section 3 nor D3 addresses. Under the recommended D3 (a) the test demands a section for a command the spec says stays with the coordinator. Medium: depends on choosing one reading.
- **M4. WC-6 "fresh output directory" and WC-4 fixed path pull apart on retry.** S:64 (WC-6: a command "writes each run into a fresh output directory"; 23 of the 27 rows and reflect say "fresh dir"); S:62 and S:73 (the directory is fixed in the brief before dispatch); `CAPS:116` (a retry is `worker-start --task <id> --retry-of`, i.e. the same Task, whose brief carries the same directory; whether the retry reuses the Task spec is UNVERIFIED). Either the command makes a sub-directory (then the contract is not at `<output-dir>/return-contract.yaml`) or the coordinator passes a new directory per attempt (then 2.3 must say so). Undefined, so Medium.
- **M5. Two `CAPS` citations point at the wrong line.** S:22 (E2) cites `CAPS:161` for `[H:worker-start]` line 38 / `--agent claude`; `CAPS:161` is the pr-submit top-level rule. S:69 (WC-11) and S:73 (section 2.3) cite `CAPS:115` for "`[G:placement]` lines 8-11: workers share the current worktree"; `CAPS:115` is "Worktrees are never deleted by these verbs" and no inventory line has the placement-sharing quote (grep for "placement" finds lines 17, 23, 90, 115, 116, 122 only). The claims may be true in the live guide (UNVERIFIED), but the cited line does not support them.
- **M6. No coordinator procedure after a `blocked` report.** S:63 (WC-5 maps `blocked` to `--outcome failed`) and `CAPS:90` (a failed Task keeps its dependents blocked until a `--retry-of` replacement completes it). Section 2.3 (S:73) lists what the brief carries and what happens after `worker_done`, but not how the coordinator answers `blocked_question` (retry worker with the answer as a flag, how many attempts, which directory). Missing requirement, Medium.
- **M7. Counting rule for AC-1.1 (Pipeline Dimensional Analysis, FR-17 to FR-19 applied by consequence).** See the Quantity Flow Diagram below: 37 commands enter P1's "accepted by every command" scope (S:159) but 3 of them are held to P4 (S:162), so 34 can be done in P1. The FR-19 label would be CRITICAL; graded by consequence it needs the choice already described in M3, so it is Medium and folded into M3.

## === ARCHITECTURE ANALYSIS ===

Experts in order: Fowler (lead), Nygard, Newman, Hohpe.

- **Fowler (boundaries).** The central decision (Orca coordinates, commands stay units of work, S:16, S:29-37) is consistent with the evidence it cites: depth 1 (`CAPS:97-101`), `worker_done` only from the dispatched pane (`CAPS:76,150`), runtime_unavailable outside Orca (`CAPS:147`). The shared-contract-file approach (S:52) keeps the interface in one place; no defect found in the boundary itself.
- **Nygard (failure modes).** Stall-without-`worker_done` is correctly identified as the real failure (S:44, `CAPS:129`); WC-10 and AC steps 2 and 3 cover it. Gap found: nothing says what the worker does if the command crashes before writing any contract (WC-5 covers "no report exists" → failed, S:63, which is enough). No blocking finding. M6 is the operational gap.
- **Newman (interface evolution).** The status vocabulary (S:62) and the `--unattended` flag are versionless; with 27 commands changed over four phases, a coordinator cannot tell a P1 command from a P0 command at dispatch time. Not stated as a requirement, so only noted (minor N2).
- **Hohpe (data flow).** Report flow: command → `return-contract.yaml` → `worker_done --report-path` → coordinator reads (S:62). `CAPS:79` says Orca does not check the file (UNVERIFIED); the spec handles that by making the coordinator open it (S:62, S:73). Sound, subject to B2 (the path must exist).

### Quantity Flow Diagram (Pipeline Dimensional Analysis)
```text
[Inventories: 43 commands] --> [Verdict split] --> [10 ready | 27 needs-change | 6 coordinator-only]
                                                      |
                                                      v
                                   [P1 scope S:159: "every command in 3.1 and 3.2" = 37]
                                   [P4 hold S:162: implement, post-release, pr-submit = 3]  <-- 37 in scope, 34 doable in P1
                                   [AC-1.1 S:195: asserts a section in all 37]              <-- MISMATCH (Medium, see M3)
```

## === ADVERSARIAL ANALYSIS (Whittaker) ===

Attack methodologies applied: Zero/Empty, Divergence, Sentinel Collision, Sequence, Accumulation. Findings use the panel template; severity graded by consequence.

1. I can break this specification by **Divergence Attack**. The invariant at **WC-3 versus AC-2.2 (S:61, S:200)** fails when **a worker on a gate input takes the permitted `ask` branch**. Concrete attack: before, brief = `/sc:tdd "auth" --unattended --output f` (bare topic, gate); the worker holds a preamble. After: worker calls `ask`, `agentWait` becomes non-null, no `worker_done`; AC-2.2 expects `failed` and a blocked contract. This is B1.
2. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (S:62)** fails when **`--output` is a file**. Concrete attack: before, `--output docs/TDD_AUTH.md`; after, contract path `docs/TDD_AUTH.md/return-contract.yaml` cannot be created, `test -s` fails. This is B2.
3. I can break this specification by **Sequence Attack**. The invariant at **WC-6 plus WC-4 (S:62, S:64)** fails when **a retry reuses the Task's brief**. Concrete attack: attempt 1 fails and wrote `<dir>/return-contract.yaml` (status blocked); attempt 2 starts via `--retry-of` with the same `<dir>`; if the command opens the file early or crashes before rewriting it, the coordinator reads attempt 1's blocked contract as attempt 2's result. MAJOR by label; Medium by consequence (relies on the retry-reuse assumption, `CAPS:116` UNVERIFIED). This is M4.
4. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (S:63)** fails when **a legitimate `status: partial` collides with success**. Concrete attack: before, a run finishes with `partial` and a missing deliverable; after, `--outcome succeeded` is sent and the coordinator's ready-wave starts dependents (`CAPS:86,90`) on a deliverable that is not there. The spec states the choice and its rationale (S:263), so this is a stated design decision, not a defect: minor note N1.
5. I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (S:68)** fails when **a poll-plus-sleep iteration exceeds the 4-minute cap**: pr-submit's poll script runtime is UNVERIFIED (S:114, S:283); the spec admits it. No finding beyond the stated UNVERIFIED item.

## Guard Condition Boundary Table

Guards with numeric, boolean or sentinel conditions found in the candidate: G1 `--unattended` switch (S:51, S:16); G2 WC-5 outcome mapping (S:63); G3 WC-10 wait thresholds 5 min heartbeat / 4 min wait (S:68, S:266); G4 nesting depth ≤ 1 (S:33, WC-8 S:66); G5 `consumer_fenced` (S:70); G6 readiness limit 60 s (S:59). Classes left out are given with the one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 `--unattended` present | S:51, S:60 | Zero/Empty | flag absent | false | SA-1: today's behaviour unchanged (S:146) | OK |
| G1 | S:51, S:60 | Sentinel Value Match | flag inside a quoted argument or as a value of another flag | ambiguous | not specified (the tokenising rule appears only in the sandbox command text `command.md:459`, not in the candidate) | GAP (Medium: undefined edge case, no concrete wrong outcome stated) |
| G1 | S:51 | Legitimate Edge Case | person types `--unattended` | true | S:228 says a person never types it; no refusal specified | GAP (Medium) |
| G2 outcome map | S:63 | Zero/Empty | no report exists | true | `failed` | OK |
| G2 | S:63 | Typical | `succeeded` | false | `succeeded` | OK |
| G2 | S:63 | Legitimate Edge Case | `partial`; audit verdict FAIL | n/a | `succeeded`, body states status (S:63, S:263) | OK |
| G2 | S:63 | Legitimate Edge Case | `blocked` with `ask` taken (WC-3) | n/a | contradicts AC-2.2 | GAP (blocking: B1) |
| G3 wait cap | S:68 | One/Minimal | wait of exactly 5 min | true (">5") not triggered | cap says "longer than 5 minutes" and split to "at most 4"; a 5.0-minute wait is neither | GAP (Medium: boundary at exactly 5 min, heartbeat cadence "every 5 minutes" S:68) |
| G3 | S:68 | Maximum/Overflow | eval timeout 3600 s (S:68) | true | split into waits ≤ 4 min | OK |
| G4 depth ≤ 1 | S:33, S:66 | Typical | worker tries `worker-start` | true | refused; WC-8 forbids the call | OK |
| G4 | S:276 | Legitimate Edge Case | `task-create` at depth 1 | unknown | forbidden by WC-8 whether or not Orca allows it | OK |
| G5 `consumer_fenced` | S:70 | Typical | `check` returns it | true | stop, no `worker_done` | OK |
| G5 | S:70 | Zero/Empty | empty `check` | false | `CAPS:67`: empty never means replaced; not repeated in the candidate | OK |
| G6 readiness 60 s | S:59 | Maximum/Overflow | fallback of 45 s or more | true | "well inside"; the evidence line says it fails above about 45 s (S:59) but WC-1 gives no number | GAP (Medium) |

Left out, with reason: G1 One/Minimal and Maximum (a boolean flag has no size); G2 Maximum (no count); G4 Zero/Empty (depth is never zero for a worker); G5 Maximum and Sentinel (no numeric input); G6 Zero/Empty (a zero timeout falls back to the 60 s default, `CAPS:44`).

FR-8 / FR-9 result: the GAP rows other than G2/blocked name no concrete wrong outcome, so they are Medium (listed under follow-up candidates as M8 to M10 below). The table is complete, so synthesis was not blocked (FR-10).

## Follow-up candidates (Medium and minor; not in the Reviser brief; not a reason to revise)

Medium: M1 (`--post-pr`), M2 (AC-C1 versus SA-2), M3 (AC-1.1 scope, incl. M7 count mismatch and pr-submit "Will Not: run headless"), M4 (fresh dir versus fixed path on retry), M5 (CAPS:161 and CAPS:115 citations), M6 (no procedure after `blocked`), M8 (`--unattended` edge cases: quoted token, typed by a person), M9 (exactly-5-minute wait boundary in WC-10), M10 (WC-1 gives no number for "well inside" the 60 s limit).
Minor notes: N1 (`partial` maps to `succeeded`, a stated choice, S:263); N2 (no version marker lets a coordinator tell which commands carry the contract); N3 (S:11 and S:285 report spot-checks that this sandbox cannot confirm); N4 (AC-C5, S:176, forbids removed lines, but adding a flag to a Usage line edits that line; may fail for flag additions).

Per the Review Loop, the session that ran this review asks the user once per loop whether to open an issue for these; this worker cannot ask, so the coordinator owns that question. Nothing is created here.

## Verification and merge notes for the coordinator

- Merge/duplicate keys: B1 cites S:61 and S:200; B2 cites S:62 and S:90 (and S:200).
- Both blocking findings quote only text inside the candidate, so the VERIFY prompt can check them with `grep -nF` on the candidate alone.

## Reviser brief

Blocking finding ids: B1, B2.

Reviser contract (restated from the command, the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

- B1: texts S:60-61 (WC-2 (c), WC-3) and S:200, S:208 (AC-2.2, AC-4.1). Stated wrong outcome: a worker following WC-3 asks and waits on the gate input where AC-2.2/AC-4.1 require `worker_done --outcome failed` with a blocked contract, so the acceptance check cannot pass.
- B2: texts S:62 (WC-4), S:87, S:90, S:120 (file-valued `--output`) and S:200 (AC-2.2 with `--output <file>`). Stated wrong outcome: WC-4 puts the contract at `<output-dir>/return-contract.yaml` where `--output` is a file, so the path is `<file>/return-contract.yaml`, which cannot exist.

verdict: FAIL
