review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (S below; S:N = line N of it)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: missing (first review; no `--re-review` or `--baseline` given)
- reviewer model used: claude-sonnet-5-5
- command: `/sc:spec-panel @specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`; format standard-critique; Whittaker active (every panel)
- review loop prompts read in full: `~/.claude/rules/prompts/document_review_loop_prompts.md` (FIRST-REVIEW prompt applied)
- panel: `superclaude review panel resolve` and `superclaude review merge` are not installed in this sandbox (`which superclaude` printed nothing), so one reviewer ran and no merge script was used. This report is the single reviewer's report.
- coverage: all 285 lines of S read; 9 `CAPS:` ranges (44-46, 52, 58-64, 72-80, 97-103, 129-130, 145-161, 177-188) read and matched; `INV-A:1-12, 33-56, 76-120` and `INV-B:3, 43, 47, 272, 285-296, 301, 311, 320, 323` read; command definition `command.md` read in full. Not covered: every `cmd/…`, `sk/…`, `EVIDENCE.md`, `orca-data.json`, `Makefile`, `CLAUDE.md`, `pyproject.toml` citation in S, because none of those files exists inside the sandbox. Each such citation is **UNVERIFIED** (the S:11 claim that 11 locations were re-read, and S:285 item 14's "340 citations checked", are likewise UNVERIFIED). Only the three inventories and README are checkable evidence.
- Arithmetic checks that held: 21+22=43 (INV-A:3, INV-B:3); 10 ready + 27 changes + 6 coordinator-only = 43 (S:76-126, S:130-137; INV-A coordinator list at INV-A:93-99, INV-B:285-287, B-ready 5 + A-ready 5); phase split 9+11+4+3=27 across S:99-125 against S:159-162.

## Guard Condition Boundary Table (triggered: thresholds and guards in S)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` output location | WC-4 (S:62) | Zero/Empty | no `--output`/`--output-dir` passed | no dir | not specified in S (only WC-5 "no report exists" -> failed, S:63) | GAP (M3) |
| `--unattended` output location | WC-4 (S:62) | Legitimate Edge Case | file-valued `--output <file>` (tdd, init-lite: S:87,90; AC-2.2 S:200) | `<file>/return-contract.yaml` | contradicts the 3.1 brief | GAP (F1) |
| heartbeat/wait split | WC-10 (S:68) | Typical | wait 6 min (> 5) | split to <= 4 min | specified | OK |
| heartbeat/wait split | WC-10 (S:68) vs AC-4.3 (S:210) | Legitimate Edge Case | single call of 4.5 min | WC-10: no split; AC-4.3: fails ("no single tool call exceeds 240 s") | two thresholds | GAP (M1) |
| ask / blocked | WC-2(c), WC-3, WC-5 (S:60,61,63) | Sequence | gate hit with live preamble | contract `blocked` written, then ask, then worker_done failed? | order not fixed | GAP (M2) |
| outcome mapping | WC-5 (S:63) | Typical / Sentinel | `partial`, audit verdict FAIL | `succeeded` | specified | OK |
| readiness limit | WC-1 (S:59) | Maximum/Overflow | prompt fallback of 45 s | borderline | S cites "above about 45 s it fails again" (EVIDENCE.md:56, UNVERIFIED) | OK, UNVERIFIED |
| nesting depth | WC-8, R1 (S:33,66) | Typical | depth 1 | worker-start refused | specified (enforcing call sites UNVERIFIED, CAPS:103) | OK |
| task confidence | 3.2 task row (S:121) | Sentinel Value Match | confidence exactly 0.70 | "below 0.70" -> blocked | 0.70 itself falls to the command's own rule (cmd/task.md:93, UNVERIFIED) | OK, UNVERIFIED |
| unattended-mode selector | D1 (S:227-230) | Sentinel Value Match | `--unattended` as a quoted argument | n/a | not addressed in S (the in-sandbox command.md:459 does address it) | GAP (note) |

Classes left out: Maximum/Overflow for WC-4 (no capacity concept); Zero/Empty for WC-10 (no zero-length wait is meaningful).

## Quantity Flow (pipeline dimensional analysis)

```text
[43 commands] -> [3.1 ready: 10] + [3.2 changes: 27] + [4 coordinator-only: 6] = 43   (conserved)
[3.2: 27] -> P1 9 + P2 11 + P3 4 + P4 3 = 27                                          (conserved)
[3.1: 10] -> P1 fixes 4 (adversarial, cleanup-audit, index-repo, workflow) + P2 gate changes 4 (reflect, release-split, tdd, troubleshoot) + no-change 2 (brainstorm, init-lite)
P1 scope text "flag accepted by every command in 3.1 and 3.2" = 37 commands, but P1 owns 9 + 4 = 13 command rows   <-- MISMATCH (see F3)
AC-1.1 asserts a contract-naming section on 37 commands; the load row (S:112) says report "none"                 <-- MISMATCH (see F2)
```

## === REQUIREMENTS ANALYSIS ===

**F1 - CRITICAL/MAJOR - Wiegers, Adzic, Whittaker (Divergence + Sentinel Collision) - blocking**
Whittaker: I can break this specification by **Divergence Attack**. The invariant at **WC-4 (S:62)** fails when **`--output` is file-valued**. Concrete attack: the 3.1 tdd row tells the brief to pass `--output <file>` (S:90) and AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` (S:200). WC-4 defines the report as `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (S:62). Before: `--output /x/tdd.md`. After, per WC-4 as written: `/x/tdd.md/return-contract.yaml`, a path under a regular file, so the write fails and AC-2.2 step 4 (S:183) cannot find a contract. init-lite (S:87), research and spec-panel (S:116,120) have the same shape. The command definition under review confirms the clash: it states `--output` is file-valued and uses `--report-dir` for the directory (command.md:22-23, 460). S never names that second flag.
Recommendation: one sentence in WC-4 that the contract directory is a separate value (a `--report-dir`-style flag, or the parent directory of a file-valued `--output` with a unique name), and fix the 3.1/3.2 rows and AC-2.2 to match. Priority High.

**F2 - MAJOR - Wiegers - blocking**
Contradiction on `/sc:load`. The 3.2 load row says report "none (see note)" and "use it as a step inside another worker's brief, not as its own Task" (S:112); the Decisions table says "a report file would be an unrequested addition" (S:265). AC-1.1 requires "every command in sections 3.1-3.2" to have an `## Unattended mode` section "naming `return-contract.yaml`" (S:195), and P1 gives every 3.1/3.2 command the flag (S:159). An implementer who follows AC-1.1 gives load a contract section; one who follows S:112/S:265 fails AC-1.1. Recommendation: exclude load from AC-1.1 and the P1 flag clause (narrowing, no new text). Priority High.

**F3 - MAJOR - Cockburn, Nygard, Whittaker (Sequence Attack) - blocking**
P1 puts "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)" (S:159), while WC-2 says "Under `--unattended` the command never calls `AskUserQuestion`" (S:60). Gate conversion for cleanup, improve, cli-eval, cli-portify, task, tdd, troubleshoot and the rest only comes in P2 (S:160), P3 (S:161) and P4 (S:162). Concrete attack: after P1 ships, `/sc:cleanup <dir> --unattended` is accepted, is not a no-op because it has gates (S:103), and still prompts. The coordinator sees a healthy worker parked on a person-only prompt with no `worker_done`, the exact silent stall S:44 and WC-2 exist to prevent. AC-1.2 live-tests only P1 commands (S:196), so nothing catches it, and the claim at S:154 that each phase is independently useful fails. Recommendation: in P1 restrict the flag to the commands whose gates are resolved in P1 (the no-gate ones), or state that later-phase commands must not be dispatched until their phase passes. Priority High.

**M1 - MAJOR but Medium (no wrong outcome without a guess) - Crispin**
WC-10 splits waits "longer than 5 minutes" into at most 4 minutes (S:68); AC-4.3 and the pr-submit row use 240 s / "under 4 minutes" (S:114, S:210). A wait of 4 to 5 minutes passes WC-10 and fails AC-4.3, and with the 5-minute heartbeat cadence it risks a missed heartbeat. Align the trigger to 4 minutes.

**M2 - Medium - Wiegers**
WC-3 (ask then re-invoke), WC-2(c) (write `blocked` and stop) and WC-5 (blocked -> `worker_done --outcome failed`) do not say whether `ask` happens before or after the blocked contract is written, or whether the re-invoked run overwrites that contract (S:60,61,63). Both readings are implementable.

**M3 - Medium - Whittaker (Zero/Empty)**
S never says what a command does under `--unattended` with no output directory. The command under review refuses before any work and prints the refusal in chat only (command.md:460); S leaves it to WC-5 "no report exists" (S:63). A missing requirement, not a stated text that does harm.

**M4 - Medium - Wiegers, Adzic**
WC-4 and 2.3 say the report path is "known before dispatch" (S:62,73), but the workflow row's contract path is `.dev/tasks/to-do/<id>/return-contract.yaml` (S:92) with an id the command generates (INV-B:272), so the coordinator cannot know it before dispatch. Workable because the worker passes the path in `--report-path`, but the sentence is false for workflow.

**M5 - Medium - Wiegers**
The spec-panel row says "add `--output`" (S:120) from INV-B:43 ("Review document, no path"), while the command definition supplied to this review already lists `--output <file>`, `--report-dir`, `--improve` and an Unattended-mode section pointing at `~/.claude/WORKER-CONTRACT.md` (command.md:23, 455-466). The row is stale against that file; whether `cmd/spec-panel.md` in the repo matches either is UNVERIFIED.

## === ARCHITECTURE ANALYSIS ===

Fowler/Newman/Hohpe/Nygard: the core decision holds up on the evidence that can be checked. Commands as units with a thin file-based contract is a sound boundary (S:16, S:1.3 R1-R5), and the R1 depth rationale matches CAPS:97-101 and the UNVERIFIED enforcement note at CAPS:103, which S:33 repeats. The coordinator/worker split of lifecycle messages (WC-7, WC-12) matches CAPS:72-77, CAPS:145-161.

**F4 - MAJOR - Whittaker (Accumulation/Sequence), Crispin - blocking**
AC-C5 (S:176) is the only mechanical check of SA-4's "additive" rule (S:149) and of SA-1's standalone guarantee, which S:142 calls a "hard requirement on every phase". Its command is `git diff -U0 master...HEAD -- <file> | grep -E '^-[^-]'`, "prints nothing". `diff` renders a deleted markdown bullet `- b` as `-- b`, which `^-[^-]` excludes. Tested in the sandbox: old file `- a`, `- b`, `---`; new file `- a`: `diff -U0 old new | grep -E '^-[^-]'` printed nothing (exit 1) while the diff shows `-- b` and `----` deleted. Commands, skills and the routing guide contain many bullets and `---` delimiters, so an implementer can delete them and AC-C5 (and AC-0.3, S:193, same pattern) reports a pass. Recommendation: use `grep -E '^-' | grep -vE '^---'` on the `--- a/…` header only, or `git diff --numstat` with deleted count 0. Priority High.

**M6 - Medium - Newman, Hohpe**
The contract has no version field and the status vocabulary is fixed to four values (S:62) while existing contracts keep "their fields" (workflow contract 1.1, INV-B:272). Evolution and the existing `status` values of workflow, brainstorm, reflect and adversarial are not mapped; WC-5 relies on the four values. Add a `contract_version` and a status-mapping note when this is next touched.

**M7 - Medium - Wiegers**
AC-C1 (S:172) greps `src/superclaude/core`, but P0 adds the contract file and an Orca section there (S:158); SA-2 allows Orca mention only inside the contract file (S:147), and the contract's WC-3 mentions the `ask` command. The pattern `orca(-ide)? (orchestration|worktree|terminal|agent)` would trip on those, and misses `orca status`, `orca open` and `orca-ide skills get`. Scope the exclusion to the contract file and widen the verb list.

**Minor notes**
- Commands brainstorm and init-lite (3.1, fix "None") are inside P1's "every command in 3.1" clause (S:159) but not in its Commands column (S:159), so their owning phase is implicit.
- E5 and AC-C1 baseline greps (S:25) cannot be checked here: UNVERIFIED.
- S:285 item 14 reports an independent citation check, and S:11 a re-read of 11 locations; neither is checkable here and neither lowers the UNVERIFIED status of the cited files.
- D1 is silent on a quoted `--unattended` argument (S:227-230); the command under review handles it (command.md:459). Not a requirement S states.
- Markdown-escaped `\|` inside the AC-C1 backticks (S:172) must be unescaped when copied to a shell.

## follow-up candidates

Medium: M1 (WC-10 vs AC-4.3 threshold), M2 (ask/blocked ordering), M3 (no output dir), M4 (workflow path not known before dispatch), M5 (stale spec-panel row), M6 (no contract version / status mapping), M7 (AC-C1 scope and pattern).
Minor: brainstorm/init-lite phase placement; UNVERIFIED checks of E5/AC-C1/S:285-14; D1 quoted-token case; `\|` escaping in AC-C1.
Per the Review Loop, the running session asks the user once whether to open an issue for these; none was created.

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", "anchor2": "a precise component prompt, not a bare topic; `--output <file>`", "refs": ["WC-4", "AC-2.2", "3.1"], "claim": "WC-4 builds the contract path under a directory taken from --output, but tdd and init-lite pass --output as a file, so the contract is written under a regular file and the AC-2.2 contract check cannot pass."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "anchor2": "none: use it as a step inside another worker's brief, not as its own Task", "refs": ["AC-1.1", "P1", "3.2 load", "Decisions"], "claim": "AC-1.1 forces a return-contract section onto /sc:load while its row and the Decisions table say it gets no report file."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "the `--unattended` flag accepted by every command in sections 3.1 and 3.2", "anchor2": "Under `--unattended` the command never calls `AskUserQuestion`", "refs": ["WC-2", "P1", "P2", "P3", "P4", "AC-1.2"], "claim": "After P1, commands whose gates convert only in P2-P4 accept --unattended yet still prompt, so a worker stalls silently and no P1 check catches it."}
{"id": "F4", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \\| grep -E '^-[^-]'", "refs": ["AC-C5", "AC-0.3", "SA-4", "SA-1"], "claim": "The additive-edit check ignores deleted lines that begin with a dash because diff shows a deleted '- b' as '-- b', so an implementer deleting a bullet or --- line passes AC-C5."}
{"id": "M1", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "must be split into waits of at most 4 minutes", "anchor2": "no single tool call exceeds 240 s", "refs": ["WC-10", "AC-4.3"], "claim": "A wait of 4 to 5 minutes passes WC-10 but fails AC-4.3."}
{"id": "M2", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "the session may instead ask the coordinator once with the preamble's `ask` command", "refs": ["WC-2", "WC-3", "WC-5"], "claim": "Order of ask, blocked contract and worker_done is not fixed."}
{"id": "M3", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "where `<output-dir>` is the directory the coordinator passed", "refs": ["WC-4"], "claim": "Behavior with no output directory under --unattended is not stated."}
{"id": "M4", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "One report file, known before dispatch, written on every outcome.", "anchor2": "`.dev/tasks/to-do/<id>/return-contract.yaml`", "refs": ["WC-4", "3.1 workflow"], "claim": "The workflow contract path contains a generated id, so it is not known before dispatch."}
{"id": "M5", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "add `--output`; contract", "refs": ["3.2 spec-panel"], "claim": "The row may be stale against a command definition that already has --output and --report-dir."}
{"id": "M6", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)", "refs": ["WC-4"], "claim": "No contract version or mapping from existing contracts' status values."}
{"id": "M7", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "prints nothing (SA-2, WC-8)", "refs": ["AC-C1", "SA-2", "P0"], "claim": "AC-C1 scans core/ where P0 adds Orca text and misses orca status/open/skills."}
```

## Reviser brief

Revise only text a blocking finding names: **F1, F2, F3, F4**. Revise only the text those findings name; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings (M1-M7) alone. Return the candidate once and do not award yourself a PASS. Ordering note: this brief sits just above the verdict line as the command requires; the Findings block is the last section before it.

verdict: FAIL
