review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document, first review)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 57927 bytes)
- candidate sha256: `7d31f7c49bc684b022504fe6730429f5c5b09ff3a76841344026b64dde9565a6`
- baseline: not given, none needed (first review); `--re-review`: not given
- reviewer model actually used: claude-sonnet-5-5 (Sonnet 5.5)
- command: `/sc:spec-panel @<candidate> --mode critique --focus requirements,architecture` (format standard, 1 iteration). The review-loop prompts file was read in full first; the FIRST-REVIEW prompt and its grading check are applied below.
- precedence: no brief clause was overridden. The brief's "do not edit anything else" is followed: no revised specification is written (the Improve step is not run).
- citation key: `SPEC:N` = line N of the candidate. `README:N`, `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `.dev/orca-command-refactor/README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`. Any `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `EVIDENCE.md`, `.dev/codegraph-migration/` or Orca-guide citation that exists only inside those files is UNVERIFIED here: the sandbox holds no source tree, so I can check only the spec and the three inventories.

## Coverage (what was and was not checked)

- Read in full: README, the spec (285 lines), `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`.
- Checked: every `INV-A:`, `INV-B:` and `CAPS:` line citation in SPEC:21-37, 59-70, 83-125, 128-139, 147, 161-165, 213-222, 260-285 against the inventory line it names (all landed on the stated content); the 43 / 10 / 27 / 6 totals and the per-phase totals (see Quantity Flow Diagram); every WC, SA and AC id against the others.
- Not checked (UNVERIFIED): all `src/superclaude/...:N` citations, `CLAUDE.md:N`, `install_core.py`, `pyproject.toml:38` (PyYAML), `Makefile`, `EVIDENCE.md`, the PR #329 run files and the Orca guide output. They are used only as carried by the inventories. The spec's own claim of an independent citation check (SPEC:285) was not re-run.
- The review-loop rule on asking the user about follow-up candidates: not asked (no user channel in this sandbox). No issue is opened.

## Findings summary

| id | severity (graded by consequence) | bucket | status |
|---|---|---|---|
| F-1 | CRITICAL, blocking | requirements / architecture | open |
| F-2 | MAJOR, blocking | requirements | open |
| F-3 | MAJOR, blocking | requirements | open |
| M-1 to M-14 | Medium (labels MAJOR or MINOR; no blocking sentence holds) | various | follow-up candidates |
| N-1 to N-5 | MINOR notes | various | follow-up candidates |

Blocking: 3. Medium: 14. Minor: 5.

---

## === REQUIREMENTS ANALYSIS ===

### F-1 [CRITICAL, blocking, priority High] Phase 1 scope, AC-1.1 and the per-command phase tags give three different command counts, and AC-1.1 contradicts open decision D3
- Experts: Wiegers (lead), Fowler (count annotation), Whittaker (divergence attack).
- Issue (stated texts that contradict):
  - SPEC:159 (P1 scope): the `--unattended` flag is accepted by "every command in sections 3.1 and 3.2 except load". That is 10 + 26 = 36 commands.
  - SPEC:159 (P1 "Commands" column) names 9 commands from 3.2 (analyze, build, business-panel, design, document, explain, index, test, load) plus fixes to 4 from 3.1 (adversarial, cleanup-audit, index-repo, workflow): 13 commands.
  - SPEC:195 (AC-1.1) requires, once P1 passes, a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` in all 36.
  - The phase tags in SPEC:99-125 put implement, post-release and pr-submit in P4 (3 commands), and SPEC:154 and SPEC:225 say P4 "waits for D2-D4" while P1-P3 "need no user decision".
  - SPEC:240 (D3 option (a), the recommendation): "no pr-submit changes in Phase 4". SPEC:139: pr-submit "stays a worker candidate only if the user accepts D3".
- Grading sentence: An implementer who follows the stated text as written builds P1 so that pr-submit (and implement, post-release) get the `## Unattended mode` section and the flag, because AC-1.1 fails otherwise; and the same implementer, following D3 (a) and SPEC:154, makes no pr-submit change before the user decides. The two cannot both hold. AC-1.1 is an acceptance criterion that either fails on the recommended D3 path or forces a command edit that the spec says depends on an unanswered user decision. Both outcomes are wrong.
- Concrete trace (Whittaker, divergence): P1 done with D3 = (a): pr-submit has no section; AC-1.1 asserts the section for every 3.1-3.2 command except load; AC-1.1 fails; P2 "does not start until the earlier phase's checks pass" (SPEC:154); the rollout stalls at P1 on the recommended path.
- Recommendation: restrict the AC-1.1 set and the P1 flag sentence to the commands whose phase tag is P1 plus the 3.1 commands P1 fixes (13), or move the pr-submit, implement and post-release rows out of the AC-1.1 set until D2-D4 are answered. State once which phase gives each command its section. Narrow rather than add.
- Priority: High. Quality impact: Testability 6 to 8; Consistency 5 to 8.

### F-2 [MAJOR, blocking, priority High] WC-4 defines the contract location from an output DIRECTORY, but section 3.1 gives two ready commands a FILE-valued `--output`
- Experts: Wiegers (lead), Adzic, Hohpe (message/report contract).
- Issue (stated texts that contradict):
  - SPEC:62 (WC-4): the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)".
  - SPEC:87 (init-lite) and SPEC:90 (tdd): the brief passes `--output <file>`, and the report is "the TDD at `--output`" (INV-B:225, `cmd/tdd.md` via INV-B:222: a single TDD file).
  - SPEC:183 (7.2 step 4): `test -s <contract>` and a YAML load must pass for every command under test; AC-1.1 (SPEC:195) requires tdd and init-lite to name `return-contract.yaml`.
- Grading sentence: An implementer who follows WC-4 as written for `/sc:tdd ... --output docs/auth/TDD_AUTH.md` builds a contract at `docs/auth/TDD_AUTH.md/return-contract.yaml`, which is a path under a regular file and cannot be created; the 7.2 step 4 check cannot pass for tdd or init-lite.
- Related gaps of the same family, graded Medium in M-2: workflow (no `--output`; path contains a run-time `<id>`, SPEC:92) and research, save, recommend (no output dir flag; SPEC:116, 119, 115).
- Recommendation: add one sentence to WC-4 that says where the contract goes when `--output` names a file (for example a sibling named `<output-stem>.return-contract.yaml`, or a separate `--report-dir`), and say that the 7.2 step 4 path is the one `worker_done --report-path` carries. Do not add more.
- Priority: High. Quality impact: Testability 6 to 8.

### F-3 [MAJOR, blocking, priority High] `/sc:cli-portify` under `--unattended` can only ever end `blocked`, yet AC-2.3 requires a `succeeded` happy path
- Experts: Cockburn (lead, goal and actor), Wiegers, Adzic (example).
- Issue (stated texts that contradict):
  - SPEC:105 (cli-portify, P2): "each of the three approval gates resolves as blocked with the artifact to review named in the contract". No default (WC-2 (a)) and no caller-supplied approval flag (WC-2 (b)) is defined for any of the three gates (INV-A:45: gates after Phases 1 and 2, before Phase 3, and before delivery).
  - SPEC:60 (WC-2) lists three resolution routes per gate; SPEC:61 (WC-3) says re-invoke "with the answer as a flag", but no approval flag exists for cli-portify. The new `--resume <contract>` flag (SPEC:105) "uses the existing `resume_phase`/`resume_substep` fields", and the spec does not say whether resuming counts as approving the gate that blocked.
  - SPEC:201 (AC-2.3): a happy-path run "per P2 command with every required flag in the brief" must pass 7.2 with `--outcome succeeded`.
- Grading sentence: An implementer who follows the cli-portify row as written builds a command that stops `blocked` at the first approval gate on every run; AC-2.3 for cli-portify then cannot pass, because no flag listed for it removes the gate.
- Concrete trace: run 1 `/sc:cli-portify <wf> --unattended --output D` stops after Phase 2 with `status: blocked`, `blocked_question: approve phase 3?`; run 2 with `--resume D/return-contract.yaml` restarts at `resume_phase` (the phase that blocked, or the next one: unspecified); the gate fires again or is skipped without an approval record; in neither reading does the spec produce a `succeeded` run through three gates.
- Recommendation: either name an approval input (one flag per gate, or one `--approve-gates` flag in the brief) or state that cli-portify is excluded from AC-2.3 and always ends `blocked` until a person approves. Choose the narrower.
- Priority: High. Quality impact: Completeness 6 to 8.

### M-1 [Medium, Whittaker sequence attack] A flag accepted before its gate resolution exists
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:159 vs SPEC:160 and SPEC:67 (WC-9)** fails when **P1 is done and P2 is not**. Concrete attack: after P1, auggie-review (tagged P2, SPEC:100) accepts `--unattended` as a flag whose gate part is not yet converted; the brief template (SPEC:73) tells the coordinator to include `--unattended`; the command still posts to the PR by default (INV-A:38) and offers remediation. Not blocking: the SPEC:159 parenthetical "(a no-op where a command has no gate)" leaves the gated case unstated, so it needs a guess about which reading the implementer picks.
- Recommendation: one clause: until its phase lands, a gated command does not accept `--unattended` (or refuses it).

### M-2 [Medium] Contract location undefined for commands with no output-directory input
- SPEC:62 requires the path "known before dispatch". Workflow's contract path contains a run-time `<id>` (SPEC:92, INV-B:272), and SPEC:92 asks for it "for pre-creation STOPs too" where no `<id>` directory exists. Research (SPEC:116: "contract naming the generated path"), save (SPEC:119) and recommend (SPEC:115) have no output-dir flag. Missing requirement, not a stated text that does harm.

### M-3 [Medium] `--unattended` without an output directory, and the token inside quoted text
- Zero/Empty attack: SPEC:73 says the brief carries the output directory; no rule covers `--unattended` with none (WC-4 says "the directory the coordinator passed", SPEC:62). Sentinel Collision attack: `--unattended` appearing inside a quoted topic (for example `/sc:tdd "document the --unattended flag"`) is not distinguished from the switch; D1 option (a) calls the flag "testable by grep and cannot misfire on a person" (SPEC:228), which does not cover quoted text. Both are requirements the document never states.

### M-4 [Medium] "refused under --unattended" has no defined outcome
- "Refused" appears in SPEC:102, 103, 108, 110, 114, 118, 123. WC-4 allows four statuses and WC-5 maps two outcomes; a refusal is neither a question (`blocked`, which carries `blocked_question`) nor a run (`failed`). The implementer must guess which status and which report the refusal writes.

### M-5 [Medium] WC-6 "fresh output directory" does not say who creates it, and a retry can overwrite
- SPEC:64: a command with no resume flag "writes each run into a fresh output directory". 23 of the 27 SPEC:99-125 rows say "fresh dir". If the command makes a subdirectory, the WC-4 path `<output-dir>/return-contract.yaml` is wrong; if the coordinator passes a new directory, 2.3 (SPEC:73) does not tell it to do so on `--retry-of`. For commands that do have a resume flag (roadmap), AC-3.2 (SPEC:205) specifies "starts fresh" into an existing directory with a prior `.session-memory.md`, which overwrites the first attempt's output. Needs a guess about the retry brief, so not blocking.

### M-6 [Medium] Authorization flags that WC-9 and D4 rely on are not defined for several commands
- SPEC:67 and SPEC:245 say outward actions turn on "only through the command's own explicit flag written in the brief". SPEC:113 (post-release) lists "Other required change: none" and names no flag for VM, real install, commit or PR; SPEC:121 (task) refuses `commit`/`push` "unless authorized" with no flag. With no flag the authorization path does not exist, so the safe default holds but D4 (a) cannot be carried out. Missing requirement.

### M-7 [Medium] Acceptance and traceability gaps (Wiegers)
| WC | Verifying check | Gap |
|---|---|---|
| WC-1 | none | "well inside the readiness limit" (SPEC:59) is unquantified and no check covers it |
| WC-2 | AC-2.2, 7.2 steps 2 and 5 | covered |
| WC-3 | none | the `ask` path is never exercised; AC-2.2 (SPEC:200) expects `failed` plus `blocked`, which a conforming worker that uses `ask` (allowed by WC-3) would not produce |
| WC-4 | 7.2 step 4, AC-1.1 | blocked by F-2 for file-valued outputs |
| WC-5 | 7.2 step 3 | covered |
| WC-6 | none | no check that a retry leaves the first attempt's output intact |
| WC-7 | AC-0.4 step 5 only | P1-P4 reuse 7.2 step 5, which searches `AskUserQuestion` only (SPEC:184), not an Agent-tool wrapper |
| WC-8 | AC-C1 | covered by grep |
| WC-9 | AC-2.4, AC-4.2 | covered for auggie-review and post-release only; task `commit`/`push` has none |
| WC-10 | AC-4.3 | pr-submit only; cli-eval's wait split (SPEC:104) has none |
| WC-11 | AC-3.4 | save only |
| WC-12 | none | no check |

### M-8 [Medium] The brief and contract do not say how the worker invokes the command
- SPEC:65 (WC-7) says the worker "runs the command directly in its own session" and AC-0.4 checks "no Agent-tool wrapper", but nothing says how: typed slash text in a task spec that follows an Orca preamble is not a message that starts with `/sc:` (project CLAUDE.md rule on Skill invocation: UNVERIFIED here), and 13 of 21 inventory-A commands have no skill (INV-A:70). The invocation mechanism is the core of the "direct route" that SPEC:43 says is unproven, and is not in 2.3 (SPEC:73).

### M-9 [Medium] `--unattended` before P1 exists, and the brief template
- SPEC:73 tells the coordinator to put `--unattended` in the command line; SPEC:81 and SPEC:194 give ready-today commands a brief without it. For free-text commands (tdd, troubleshoot, workflow) a not-yet-supported `--unattended` token becomes part of the prompt text. Add one sentence to 2.3: omit `--unattended` until the command's phase lands.

### M-10 [Medium] Status vocabulary and existing contracts
- SPEC:62: commands that already write a contract "keep their fields and add the missing ones". Their existing `status` values are not shown in the inventories (INV-B:272 names the field, not its values), while WC-4 and 7.2 step 4 (SPEC:183) require one of four. If an existing contract uses another value, the check fails or the field is overwritten. Also a zero-byte or unparseable contract is not covered by WC-5 ("no report exists", SPEC:63). Whittaker zero/empty and sentinel attacks; needs a guess.

### M-11 [Medium] Precedence between a documented default and a caller value
- WC-2 gives (a) default, (b) caller flag, (c) blocked, with no precedence (SPEC:60). SPEC:116: research `--unattended` "pins `--strategy planning`"; a brief that also passes `--strategy intent` has two stated outcomes. Same shape for `--r1-scope custom` (SPEC:89).

### M-12 [Medium] Evidence cited for a standing rule is a rule of this one run
- SPEC:67 and SPEC:133 cite `README:31` ("No git commits, pushes, PRs or GitHub comments") as the reason outward defaults are off and `/sc:git` is coordinator-only. README:29-31 binds workers of this run only. The conclusion is defensible on other grounds (SPEC:133 also cites the command text), so no wrong outcome; the citation is overstated.

---

## === ARCHITECTURE ANALYSIS ===

### M-13 [Medium, Nygard] No bound on retries of `blocked` and `failed` workers
- Accumulation attack. The invariant at **SPEC:263 (Decisions, `partial`/failed rows) with CAPS:80** fails when **a worker reports `failed` for a blocked gate**: Orca's circuit breaker counts failed `worker-start` attempts, not a worker's own `failed` report (CAPS:80, CAPS:116). Concrete attack: Task T blocks at a gate; the worker sends `--outcome failed`; the coordinator retries with `--retry-of`; the same gate blocks again, with no input changed; this repeats without limit. SPEC:73 lists what the coordinator owes each worker but sets no retry rule for a `blocked` contract. Not blocking: the loop needs a coordinator that ignores `blocked_question`.
- Recommendation: one sentence in 2.3: a `blocked` Task is retried only with a changed brief.

### M-14 [Medium, Nygard / Whittaker] WC-10 covers poll waits but not other long tool calls; liveness effect unverified
- SPEC:68: split a command step that blocks "a single tool call" longer than 5 minutes into waits of at most 4 minutes. An Agent-tool fan-out call (tdd 2-10+ agents, cleanup-audit waves, troubleshoot Tier 2: SPEC:21-24, INV-A:42, INV-B:221) is also a single blocking call and cannot be split by the command. The spec does not say whether the 5-minute heartbeat is then required, and whether heartbeat age affects Orca's liveness verdict is UNVERIFIED (CAPS:130, CAPS:182). Mixed into this: the contract file may be unreadable (`~/.claude/WORKER-CONTRACT.md` absent or older than the command): SPEC:52 has each command "point to the installed contract path", and no behavior is given if it cannot be read (the AC-0.1 check, SPEC:191, covers the installer list only).

### Architecture observations (no finding)
- Fowler: the decision to keep Orca outside the commands (SPEC:16-39) is consistent with all five rejection reasons R1-R5 and with CAPS:97-103, 145-149; the single shared contract file plus a short per-command section (SPEC:52) avoids repeating rules 36 times. Shotgun-surgery risk remains (36 edits); F-1 is where the spec's own counts do not close.
- Newman: the contract has no version field (compare the existing workflow contract "1.1", INV-B:272), so a later change to the four statuses cannot be detected by a coordinator (see N-4).
- Hohpe: `worker_done` "exactly once" (SPEC:63) with a lost response: Orca offers `--retry-request` for mutations (CAPS:117); WC-5 does not say to use it (see N-5).
- Hightower: the Orca-aware surface stays one launcher plus the contract file (SPEC:25), which is operationally simple.

---

## Pipeline Dimensional Analysis (FR-17 to FR-19, triggered: the spec describes a multi-stage classification and rollout where counts change between stages)

Pipeline detection (Fowler): classification of `cmd/` into ready / needs-change / coordinator-only (SPEC:76), then assignment of 27 to phases (SPEC:99-125), then the per-phase scope and acceptance sets (SPEC:159-162, 195-210).

### Quantity Flow Diagram (FR-21)

```text
[Source: 43 commands (INV-A 21 + INV-B 22)]
   --> [Stage 1: classify] --> [Ready today: 10]       (SPEC:83-92; INV-A 5 + INV-B 5)  OK
                           --> [Needs change: 27]      (SPEC:99-125; INV-A 13 + INV-B 14) OK
                           --> [Coordinator-only: 6]   (SPEC:132-137; INV-A 3 + INV-B 3)  OK     10+27+6 = 43 conserved

[Needs change: 27] --> [Stage 2: phase tag, SPEC:99-125] --> P1 9, P2 11, P3 4, P4 3  = 27 conserved
[Ready today: 10]  --> [Stage 2b: small fixes] --> P1 4 (adversarial, cleanup-audit, index-repo, workflow)
                                                 --> P2 4 (reflect, release-split, tdd, troubleshoot)
                                                 --> none 2 (brainstorm, init-lite)             = 10 conserved
   P1 "Commands" column (SPEC:159): 9 + 4 = 13
   P2 "Commands" column (SPEC:160): 11 + 4 = 15

[Consumer A: P1 scope sentence, SPEC:159]  expects 36  (10 + 27 - load)       <-- MISMATCH vs 13
[Consumer B: AC-1.1, SPEC:195]             asserts 36                         <-- MISMATCH vs 13, and vs P4 (3) and D3(a)
[Consumer C: AC-1.2, SPEC:196]             live-checks "each P1 command except load" = 8   (consistent with 13/9 reading)
[Consumer D: 3.2 "27" in header]           counts load although load gets no flag, no section, no contract (SPEC:112)
```

Consistency check (Whittaker, FR-18 step 4): the counts 43, 10, 27, 6 and the phase totals close exactly. The mismatch is between the 13 commands the phase table names for P1 and the 36 commands that the P1 scope sentence and AC-1.1 operate on. It is recorded as F-1 (FR-19: dimensional mismatch is CRITICAL; the concrete values are 13 versus 36, and 3 of the 36 are tagged P4).

---

## Guard Condition Boundary Table (hard gate, completed before synthesis)

Guards identified in the spec: the `--unattended` switch (G1), the gate-resolution routes (G2), the status-to-outcome mapping (G3), the heartbeat and wait thresholds (G4), the readiness limit (G5), the nesting depth (G6), the confidence threshold (G7), the pr-submit monitor level (G8), the retry rule (G9), the parallel-write rule (G10), the outward-action default (G11), the contract-file read (G12). Classes left out are given with a one-line reason under the table. Responsibility: Nygard built, Crispin checked completeness, Whittaker attacked.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| G1 `--unattended` present | SPEC:51, 228, 146 | Zero/Empty | flag absent | false | Today's behavior unchanged (SA-1, SPEC:146) | OK |
| G1 `--unattended` with output dir | SPEC:62, 73 | Zero/Empty | flag present, output dir `""` / missing | true | Not specified (WC-4 assumes a directory was passed) | GAP (M-3) |
| G1 `--unattended` token | SPEC:228 | Sentinel Value Match | `--unattended` inside a quoted topic | true (by grep) | Not specified | GAP (M-3) |
| G1 `--unattended` + person flag | SPEC:60, 102-123 | Legitimate Edge Case | `--interactive`, `--watch`, `--mode socratic`, `--monitor 1` | true | "refused", outcome and status undefined | GAP (M-4) |
| G1 `--unattended` on gated command, gates not yet built | SPEC:159-160 | Legitimate Edge Case | P1 done, P2 not | true | "a no-op where a command has no gate"; gated case unstated | GAP (M-1) |
| G1 `--unattended` + section-4 command | SPEC:128 | Legitimate Edge Case | `/sc:pm --unattended` | true | "get no `--unattended` mode"; the effect of passing it is unstated | GAP (N-2) |
| G2 gate route (a)/(b)/(c) | SPEC:60 | Typical | one route applies | true | Documented per command (SPEC:99-125) | OK |
| G2 gate route precedence | SPEC:60, 116 | Legitimate Edge Case | default (a) and caller value (b) both set | true | No precedence | GAP (M-11) |
| G2 cli-portify gates | SPEC:105, 201 | Legitimate Edge Case | all three gates, happy path | true | only "blocked" defined; AC-2.3 needs `succeeded` | GAP (F-3) |
| G3 status to outcome | SPEC:63 | Zero/Empty | no report file | true | `--outcome failed` | OK |
| G3 status to outcome | SPEC:63 | Zero/Empty | file exists, zero bytes or invalid YAML | false (no "no report") | Not specified | GAP (M-10) |
| G3 status to outcome | SPEC:62 | Sentinel Value Match | `status` outside the four values (an existing contract's own value) | false | Not specified | GAP (M-10) |
| G3 status to outcome | SPEC:63 | Typical | `succeeded` | true | `--outcome succeeded` | OK |
| G3 status to outcome | SPEC:63, 263 | Legitimate Edge Case | `partial`; audit verdict FAIL; `blocked` | true | `succeeded`; `succeeded`; `failed` | OK |
| G4 wait size, heartbeat | SPEC:68 | Typical | wait of 3 minutes | true | Heartbeat between waits | OK |
| G4 wait size, heartbeat | SPEC:68, 266 | Legitimate Edge Case | wait of exactly 4 minutes; 5-minute cadence | true | "at most 4 minutes" holds | OK |
| G4 wait size, heartbeat | SPEC:68 | Maximum/Overflow | one non-wait tool call over 5 minutes (Agent fan-out) | true | Not specified | GAP (M-14) |
| G4 wait size, heartbeat | SPEC:68, 104 | Maximum/Overflow | eval timeout 3600 s | true | Split into waits of at most 4 minutes (cli-eval row) | OK |
| G5 readiness limit | SPEC:59 | Typical | fallback at 30 s | true | Passes (EVIDENCE.md:45 via CAPS:49) | OK |
| G5 readiness limit | SPEC:59 | Maximum/Overflow | fallback at 50 s (inside the 60 s default, past the 45 s seen to fail) | unknown | "well inside" is unquantified; "above about 45 s fails again" holds for the 45 s `--timeout-ms` used in that test, not the default (CAPS:49) | GAP (N-3) |
| G6 nesting depth | SPEC:33, 66 | One/Minimal | depth 1, worker calls `worker-start` | true | Refused `nested_worker_depth_exceeded`; WC-8 forbids the call | OK |
| G6 nesting depth | SPEC:252 | Maximum/Overflow | user raises depth to 2 (D5 (b)) | true | WC-8 still forbids a command calling Orca | OK |
| G7 confidence below 0.70 | SPEC:121 | Legitimate Edge Case | 0.69 / exactly 0.70 / 0.0 | true / false / true | Below 0.70 blocked; 0.70 proceeds; 0.0 blocked | OK |
| G8 pr-submit monitor level | SPEC:114 | Legitimate Edge Case | `--monitor 1` / `--monitor 3` | true / false | 1 refused (outcome undefined, M-4); 3 allowed | OK |
| G8 pr-submit monitor level | SPEC:114 | Legitimate Edge Case | `--monitor 0` or `2` | unknown | Not specified; the level semantics are UNVERIFIED in the sandbox | GAP (M-4) |
| G9 retry rule | SPEC:64 | Legitimate Edge Case | `--retry-of` on a resume-capable command, brief omits the resume flag | true | roadmap starts fresh over existing output (SPEC:205) | GAP (M-5) |
| G9 retry rule | SPEC:73, 263 | Maximum/Overflow | N repeated `blocked` retries | true | No bound; the breaker does not count a worker's own failure (CAPS:80) | GAP (M-13) |
| G10 parallel write | SPEC:69, 85, 86 | Legitimate Edge Case | two workers, fixed output (`.claude-audit/`, `PROJECT_INDEX.md`) | true | cleanup-audit: "one audit per worktree at a time"; index-repo: not addressed; 2.3 does not carry the duty | GAP (M-7 row WC-11; N-1) |
| G11 outward default | SPEC:67, 100 | Typical | auggie-review, `--unattended`, no `--post-pr` | true | No post, no offer | OK |
| G11 outward default | SPEC:67, 113, 121 | Legitimate Edge Case | brief authorizes commit / install / VM | true | "the command's own explicit flag", none defined | GAP (M-6) |
| G12 contract file read | SPEC:52, 191 | Zero/Empty | `~/.claude/WORKER-CONTRACT.md` missing | true | Not specified | GAP (M-14) |

Left out classes (one line each): G1 One/Minimal and Maximum/Overflow (a boolean switch has no count); G2 Zero/Empty (a gate with no resolution cannot exist: every gate row names one); G3 Maximum/Overflow (the four statuses are a closed set, covered by the Sentinel row); G5 Zero/Empty (a fallback of 0 s is below the typical case); G6 Zero/Empty and Sentinel (the setting falls back to the default when malformed, CAPS:100); G7 Zero/One/Maximum beyond the three rows (confidence is a number in 0..1 produced by the checker); G8 Zero/Empty (the flag is an ordinal, not a collection); G12 One/Maximum (a file is present or not).

FR-8 / FR-9 grading: every GAP above was graded by consequence. Three GAP groups name a concrete wrong outcome and are the blocking findings F-1, F-2, F-3; the rest are Medium (they need a guess or are requirements the document never states) and are listed above. FR-10: the table is complete (all cells populated, guards enumerated, omitted classes explained).

---

## Whittaker adversarial analysis (FR-3 template, summary)

- I can break this specification by **Divergence Attack**. The invariant at **SPEC:159, 195 (P1 scope, AC-1.1)** fails when **the P1 command set is read from the phase column rather than the scope sentence**. Concrete attack: 13 commands edited in P1 (SPEC:159 column); AC-1.1 asserts 36; 23 assertions fail, 3 of them (implement, post-release, pr-submit) cannot be satisfied before D2-D4; the rollout stops. Severity: CRITICAL (F-1).
- I can break this specification by **Divergence Attack**. The invariant at **SPEC:62 vs SPEC:87, 90 (WC-4 vs `--output <file>`)** fails when **the command is tdd or init-lite**. Concrete attack: `--output docs/a/TDD.md` gives `<output-dir>` = a file; the contract path is under a file; `test -s` fails. Severity: MAJOR (F-2).
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:105 (cli-portify gates)** fails when **gate 1 fires on the unattended run and the resume carries no approval**. Concrete attack: run 1 blocked at gate 1; run 2 `--resume` restarts at the blocked phase and blocks again; run 3 repeats; no `succeeded` state is reachable. Severity: MAJOR (F-3).
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:159-160** fails when **P1 lands before P2**. Concrete attack: see M-1. Severity: Medium.
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:228** fails when **`--unattended` is inside a quoted prompt**. Concrete attack: see M-3. Severity: Medium.
- I can break this specification by **Accumulation Attack**. The invariant at **SPEC:73 with CAPS:80** fails when **the same gate blocks on every retry**. Concrete attack: see M-13. Severity: Medium.
- I can break this specification by **Zero/Empty Attack**. The invariants at **SPEC:62-63** fail when **the contract is empty or invalid, or no output dir was given**. Concrete attack: see M-3, M-10. Severity: Medium.

## Expert consensus

- Wiegers, Adzic, Cockburn: the requirement set (WC-1 to WC-12) is well formed and has owners and evidence; the defects are in the acceptance set and the count and path rules (F-1, F-2, F-3, M-7).
- Fowler, Newman, Hohpe, Nygard: the architectural decision is sound and well evidenced; its gaps are interfaces at the edges (file versus directory output, retry bound, version field).
- Crispin, Gregory: the live check in 7.2 is concrete and mostly pass/fail; WC-1, WC-3, WC-6, WC-12 have no check (M-7).
- Hightower: operationally minimal; no change.
- Disagreement: none recorded between experts.
- Advisory (not forced): the spec has numeric thresholds (SPEC:59, 68, 121, 252), count-changing stages (43 to 10 / 27 / 6 to phases) and guard conditions, so `--focus correctness` is recommended for the next review.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  sha256: 7d31f7c49bc684b022504fe6730429f5c5b09ff3a76841344026b64dde9565a6
  review_date: 2026-11-10
  review: "1 of 3"
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.0
  clarity: 8
  completeness: 6.5
  testability: 6.5
  consistency: 6.5
critical_issues:
  - {id: F-1, category: requirements, severity: CRITICAL, expert: Wiegers/Fowler/Whittaker, issue: "P1 scope 13 vs AC-1.1 36; AC-1.1 vs D3(a)", recommendation: "align AC-1.1 and the P1 flag sentence with the phase column"}
  - {id: F-2, category: requirements, severity: MAJOR, expert: Wiegers/Adzic, issue: "WC-4 output-dir vs file-valued --output (tdd, init-lite)", recommendation: "one sentence for the file-valued case"}
  - {id: F-3, category: requirements, severity: MAJOR, expert: Cockburn/Wiegers, issue: "cli-portify has no route to succeeded; AC-2.3 requires it", recommendation: "name an approval input or exclude it from AC-2.3"}
expert_consensus: [architecture decision sound, requirements well owned, acceptance set has count and path defects]
improvement_roadmap:
  immediate: [F-1, F-2, F-3]
  short_term: [M-1, M-2, M-4, M-5, M-6, M-7, M-8, M-13]
  long_term: [M-3, M-9, M-10, M-11, M-12, M-14, N-1, N-2, N-3, N-4, N-5]
adversarial_analysis: see "Whittaker adversarial analysis" above
```

## follow-up candidates (Medium and minor; never trigger a revision, never in the Reviser brief)

Medium: M-1 flag accepted before its gate exists (SPEC:159-160); M-2 contract location for commands with no output dir and workflow's run-time `<id>` (SPEC:92, 115, 116, 119); M-3 `--unattended` without output dir, and inside quoted text (SPEC:62, 73, 228); M-4 "refused" has no outcome (SPEC:102-123); M-5 fresh-dir ownership and roadmap overwrite on retry (SPEC:64, 205); M-6 no authorization flags for post-release and task commit/push (SPEC:67, 113, 121, 245); M-7 acceptance coverage for WC-1, 3, 6, 7, 9, 10, 11, 12 (table above); M-8 how the worker invokes the command (SPEC:65, 73, 194); M-9 omit `--unattended` before a command's phase lands (SPEC:73, 81); M-10 status vocabulary of existing contracts, empty or invalid contract (SPEC:62, 63, 183); M-11 default versus caller value precedence (SPEC:60, 116); M-12 `README:31` cited as a standing rule (SPEC:67, 133); M-13 no retry bound for `blocked` workers (SPEC:73, 263); M-14 long non-wait tool calls and unreadable contract file (SPEC:52, 68, 191).

Minor notes:
- N-1: index-repo writes the fixed `PROJECT_INDEX.md` at the repo root (SPEC:86, INV-A:53) and is called ready, so two workers collide; cleanup-audit's fixed `.claude-audit/` is acknowledged (SPEC:85) but 2.3 (SPEC:73) carries no "one at a time per worktree" duty.
- N-2: the effect of passing `--unattended` to a section-4 command is unstated (SPEC:128).
- N-3: WC-1 "well inside the readiness limit" is unquantified, and "above about 45 s it fails again" (SPEC:59) comes from a test run with a 45 s limit (CAPS:49), not the 60 s default.
- N-4: the contract has no version field (compare INV-B:272, contract 1.1).
- N-5: WC-5 "exactly once" (SPEC:63) does not mention `--retry-request` for a lost `worker_done` response (CAPS:117).
- Also noted: the id `B-1` (SPEC:112, 159, 195, 196) is used but never defined in the spec (the meaning is given inline, so no wrong outcome); SPEC:122 claims tasklist's reflect fan-out is "inside Claude Code's nesting limit" citing INV-A:14, while INV-B:210 and INV-B:314 mark nested spawning UNVERIFIED and the spec's own UNVERIFIED list (SPEC:271-285) omits it; the AC-C5 grep (SPEC:176) flags any changed existing line, and adding a flag to an existing Usage line is such a change for most commands (named defects in SA-4 excepted); AC-C1 (SPEC:172) greps `src/superclaude/core`, the directory that P0 writes the contract file and the Orca routing section into (SPEC:158), so those two files must avoid the matched strings; D4's scope (SPEC:244) names P2 commands while SPEC:154 says P1-P3 need no decision; `pyproject.toml:38` PyYAML claim (SPEC:183) is UNVERIFIED here.

## Reviser brief

Blocking finding ids: F-1, F-2, F-3.

Rules (restated from the command's Review Loop, Reviser contract; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS.

- F-1: SPEC:159 (P1 scope sentence), SPEC:195 (AC-1.1), SPEC:99-125 phase tags for implement, post-release, pr-submit, SPEC:240 (D3 (a)). Make the P1 flag set, the phase column and AC-1.1 name the same commands.
- F-2: SPEC:62 (WC-4), SPEC:87, SPEC:90, SPEC:183. State where the contract goes when `--output` is a file.
- F-3: SPEC:105 (cli-portify row), SPEC:201 (AC-2.3). Define how an unattended cli-portify reaches `succeeded`, or exclude it from AC-2.3.

verdict: FAIL
