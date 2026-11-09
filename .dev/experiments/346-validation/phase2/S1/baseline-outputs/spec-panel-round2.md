# Spec panel round 2: independent re-review of the revised Orca worker contract spec

Task: task_3315a06c4bad (Task 7, independent re-review). Planning only; no file other than this one was written.
Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
Inputs: revised spec (cited `SPEC:N`, line N of the file as read on 2026-11-02, 403 lines), round-1 review `.dev/orca-command-refactor/review/spec-panel.md` (`PANEL:N`), `.dev/orca-command-refactor/review/disposition.md` (`DISP:N`), inventories (`INV-A:N`, `INV-B:N`, `CAPS:N`).

## Verdict
**FAIL.** 13 new findings: 1 CRITICAL, 9 MAJOR, 3 MINOR (section 5), plus 2 overstated citations (C1, C2, which are findings N13 and N6).
- **Part 1 (round-1 findings):** all 24 defects round 1 named are gone from the spec text; none was rejected or silently dropped. For 10 of them the fix introduced or exposed a new defect (section 2).
- **Part 2 (citations):** every citation on the 172 revised lines was re-read against the live file or live `orca ... --help` output. None points at a wrong line; 2 are overstated (section 3).
- **Part 3 (panel):** the new defects cluster in the new machinery: retry routing (N1, N2, N3), the report directory (N4, N6, N12), the gate policy (N7, N9), the fan-in upper bound (N5), and the new check scripts (N8, N10, N11). The core decision (Orca coordinates; commands stay Orca-free) still holds.

No Self-Audit is included because the verdict is FAIL.

## 1. Method
- **Read in full:** `.dev/orca-command-refactor/README.md` (1-38), the revised spec (1-403), `PANEL` (1-200), `DISP` (1-73), `CAPS:40-188`, and `~/.claude/commands/sc/spec-panel.md` (1-462; the command names no skill, so it runs from its own file).
- **What the revision changed.** The pre-revision spec survives as a Claude Code file-history backup, `/home/coder/.claude/file-history/3bb70411-6b34-4a6c-b0de-81ffdbae7944/2d815cfd5e9a74d2@v1` (285 lines; its line 78 is the old heading `### 3.1 Ready today (10)`). A line diff against the revised spec gave 172 added or changed lines (revised `SPEC` lines 4, 40, 53-56, 64-68, 72-73, 77-92, 95-100, 106, 113, 116, 130, 135, 137, 179-180, 185-196, 200, 203-250, 256-315, 333, 361, 366-373, 395-402). Part 2 checks every `path:line`, `CAPS`/`INV` and `--help` line citation found on those lines.
- **Orca help, read live** inside this Orca terminal with `orca` (`/home/coder/.config/orca/linux-orca-cli-shim/orca`, version `1.4.237-aidev02.0e4491a95e92`, the same build as `CAPS:8`): `orchestration worker-start --help`, `task-update --help`, `send --help`, `task-create --help`. "Line N" below means line N of that command's own output.
- **Source lines** were printed with bounded read-only `sed`/`awk` batches under `/tmp/ironclaude-batch.*` (removed on exit), or with the Read tool.
- **Run, not inferred:** AC-C1 on today's tree (prints nothing; a positive sample line matched, count `1`); `git status --porcelain=v1` versus `-uall` on this worktree; `git check-ignore -v` on default output paths; the AC-C5 `awk` filter on a sample numstat line; a grep of the spec for escaped pipes; `git help diff` for three-dot semantics. Nothing in the repo was written except this file.
- **Panel mode.** Critique; focus requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard); Whittaker in every panel. The input is not a TDD or PRD (no `parent_doc`/`coordinator` frontmatter, no PRD headings: `SPEC:1-13`), so steps 6a-6d do not apply. Step 6 "Improve" is not run: the brief forbids editing the spec.

## 2. Part 1: round-1 finding resolution
Each row checks the revised spec text itself, not `DISP`. "Resolved" means the defect `PANEL` named is gone from the spec text. "Resolved, new defect" means the named defect is gone but the fix introduced or exposed a new one, numbered in section 5 (`N#`).

| # | Round-1 finding (`PANEL:118-141`) | Spec text checked | Result | Evidence |
|---|---|---|---|---|
| 1 | Retry cannot carry a new brief | WC-6 (a)/(b)/(c) `SPEC:68`; WC-3 last sentence `SPEC:65`; worked example `SPEC:87-92`; AC-2.6, AC-2.7 `SPEC:273-274` | **Resolved, new defects N1, N2, N3.** A changed brief now goes to a new Task, which `task-create` supports (`task-create --help` line 3: `--spec <text>`), and an unchanged brief to `--retry-of` (`worker-start --help` line 47). But the WC-6 (b) live check has no valid P2 subject (N2) and omits the placement flags the retry needs (N3), and 2.3 still lets a dependent be created up front on an input whose retry must be a new Task (N1). | `worker-start --help` line 47: "--retry-of needs --task naming the failed Task (--spec creates a new one) and does not inherit placement; repeat the intended --on/worktree and --agent/terminal choices"; `SPEC:83`, `SPEC:97` |
| 2 | New `status` values clash with existing contracts | WC-4 `SPEC:66`, WC-5 `SPEC:67`, 7.2 step 4 `SPEC:244` | **Resolved, new defect N4.** The new top-level `worker_status` field and explicit mapping remove the clash; step 4 now asserts `worker_status`. Exposed: where adversarial's worker contract lives is now ambiguous (N4). | `sk/sc-workflow-protocol/refs/return-contract.md:7`; `sk/sc-adversarial-protocol/SKILL.md:432,436`; `sk/sc-reflect-protocol/SKILL.md:250` |
| 3 | Fan-in has no rule for blocked or partial inputs | Fan-in rule `SPEC:85`; 1.3 `SPEC:40`; 2.3 `SPEC:79-83` | **Resolved, new defect N5.** Blocked, failed, partial and fewer-than-2 cases now have rules. The upper end (more than 10 admitted inputs) has none (N5). | `cmd/adversarial.md:15` ("2-10 existing files") |
| 4 | Contract location not known before dispatch | Report directory `SPEC:55`; WC-4 `SPEC:66`; rows `SPEC:106,113,130,135,137` | **Resolved, new defects N4, N6.** Every command now has a report directory. But the rule's precedence is wrong or unstated for commands that own a directory-valued output flag and also get `--report-dir` (pr-submit, N6), and adversarial's two candidate paths conflict (N4). | `cmd/pr-submit.md:55` (`--output-dir <dir>`, "Run-log + artifacts dir") |
| 5 | AC-C1 trips on P0's own core files | AC-C1 `SPEC:203-210` | **Resolved.** The two files are excluded by exact path; every other core file is still scanned. Run on today's tree: prints nothing. A sample line `...orca orchestration send...` still matches (count `1`), so the check is not blind. | Run in this review (section 1) |
| 6 | Escaped pipes inside table cells | 7 intro `SPEC:200`; blocks `SPEC:204-230,235-250,285-291` | **Resolved.** `grep -n '\\|'` on the spec matches only line 200, the sentence that explains the rule. | Run in this review |
| 7 | `^-[^-]` misses removed lines | AC-C5 `SPEC:227-230`; AC-0.3 `SPEC:258`; block `SPEC:289-290` | **Resolved, new defect N8.** `--numstat` with `awk '$2 != 0'` counts every deleted line (sample `3	0	file.md` printed nothing). But the diff range `master...HEAD` excludes uncommitted edits, so the check passes vacuously before a commit (N8). | `git help diff`: "git diff A...B is equivalent to git diff $(git merge-base A B) B" |
| 8 | WC-10 ignores Agent-tool fan-out | WC-10 `SPEC:72`; AC-4.3 `SPEC:282`; Decisions `SPEC:372` | **Resolved, new defect N10.** The gap during fan-out is accepted and the coordinator is told not to act on a late heartbeat. The heartbeat duty itself now has no live check under the recommended D3 (a) (N10). | `CAPS:111`, `CAPS:125`; `cmd/troubleshoot.md:76` |
| 9 | P1 makes every command accept `--unattended` early | P1 row `SPEC:180`; table `SPEC:185-195` | **Resolved.** Recounted: P1 14 (6 from 3.1, 8 from 3.2), P2 15 (4 + 11), P3 4, P4 2 (+pr-submit under D3 (b)); 14 + 15 + 4 + 2 = 35; plus load and pr-submit = 37 = 10 + 27. Each row's Phase column matches the table. | `SPEC:120-146` (Phase column); `SPEC:99-113` |
| 10 | AC-1.1 cannot pass in P1 | AC-1.1 `SPEC:262` | **Resolved.** The test now asserts only the P1 list and asserts absence elsewhere. | `SPEC:190` |
| 11 | AC-2.2 depends on a worker choice | WC-3 `SPEC:65`; 2.3 `SPEC:77`; AC-2.2 `SPEC:269` | **Resolved, new defects N7, N9.** The brief now fixes the policy. But the ask policy says "asks once" with no rule for a second gate (N7), and nothing stops the ask policy being used for implement, which would relay a Ruling that D2 (a) forbids (N9). | `SPEC:111` (tdd has two gates); `sk/sc-implement-protocol/refs/qa.md:238` |
| 12 | `--unattended` with no output directory | `SPEC:55`; WC-4 `SPEC:66`; AC-1.5 `SPEC:266` | **Resolved, new defect N12.** Behaviour is defined and checked. The fixed error text names `--output <dir>`, which is wrong for commands whose `--output` is a file or banned (N12). | `cmd/workflow.md:42` |
| 13 | `partial` releases dependents unchecked | 2.3 `SPEC:79-82`; Decisions `SPEC:368` | **Resolved.** The coordinator must read and record usability before dependents start. | `CAPS:77`, `CAPS:92` |
| 14 | Step 6 false-fails on a dirty or shared worktree | 7.2 intro and steps 0, 6 `SPEC:233-237,247-250`; AC-3.4 `SPEC:279` | **Resolved, new defect N11.** The snapshot removes the false fail. The snapshot method itself misses writes in untracked directories, in ignored paths and to already-modified files, so step 6 can now false-pass (N11). | Run in this review: `git status --porcelain=v1` printed one line `?? .dev/orca-command-refactor/`; `-uall` printed 8 files |
| 15 | Traceability gaps | 7.4 `SPEC:293-315`; AC-0.5, AC-0.6 `SPEC:260-261` | **Resolved, new defect N10.** Every WC and SA row has a check; WC-12's fenced branch is stated as UNVERIFIED rather than claimed. WC-10's heartbeat duty is unchecked under D3 (a) (N10). | `SPEC:307`, `SPEC:345` |
| 16 | Stall detection relies only on sampled `agentWait` | 7.2 steps 2-3 `SPEC:239-240` | **Resolved.** Step 3 adds the final-turn transcript proof Orca names. | `CAPS:126` |
| 17 | No parse rule for quoted `--unattended` | `SPEC:53`; D1 (a) `SPEC:333`; AC-2.8 `SPEC:275` | **Resolved.** | — |
| 18 | `--unattended` with `--interactive` unspecified | `SPEC:54`, `SPEC:97`; AC-1.6 `SPEC:267` | **Resolved.** One rule for every command, with a failed contract naming the flag. | — |
| 19 | Worker-session rules duplicated from the preamble | `SPEC:56`; WC-10 `SPEC:72` | **Resolved.** The contract file defers to the preamble for verb syntax and cadence. | `CAPS:130` |
| 20 | AC-0.1 does not prove installation | `SPEC:56`; AC-0.1 `SPEC:256`; block `SPEC:287` | **Resolved.** The block calls `install_core_files(target_path=d)`, which copies every `core/*.md` (`install_core.py:53,62-71`) and returns `success = len(failed) == 0` (`install_core.py:99-100`), so the assert is meaningful. | `src/superclaude/cli/install_core.py:27-29,53,62-71,99-100` |
| 21 | "Ready today" overstates readiness | `SPEC:95,99-100`; P0 `SPEC:179`; AC-0.4 `SPEC:259` | **Resolved.** | — |
| 22 | No schema version | WC-4 `SPEC:66`; step 4 `SPEC:244`; `SPEC:367` | **Resolved.** `worker_contract_version: "1"` is asserted as the string `'1'`, matching the quoted value in WC-4. | `sk/sc-workflow-protocol/refs/return-contract.md:6` |
| 23 | AC-1.3 uses `claude -p` | AC-1.3 `SPEC:264` | **Resolved.** | — |
| 24 | Transcript may not name tool calls | AC-0.6 `SPEC:261`; step 5 `SPEC:246` | **Resolved.** P0 records the answer and step 5 states its fallback. | `CAPS:131` |

Summary: 24 of 24 round-1 defects are gone from the spec text (none rejected by `DISP`, none silently dropped). For 10 of them (rows 1, 2, 3, 4, 7, 8, 11, 12, 14, 15) the fix introduced or exposed a new defect, listed in section 5. `DISP`'s `rSPEC:N` locations were spot-checked for all 24 rows and each pointed at the right revised line.

## 3. Part 2: citation check of revised or added citations
Scope: every citation on a line the revision added or changed (section 1). "OK" = the cited line says what the spec says it says. Citations whose text is unchanged from the original and that sit on unchanged lines are out of scope (round 1 and the inventories' own checks covered them).

### 3.1 Wrong or overstated citations
| # | Spec location | Citation | What the spec claims | What the source says | Verdict |
|---|---|---|---|---|---|
| C1 | AC-0.5 `SPEC:260` | `EVIDENCE.md:45,56` | Start must return "in under 45 s, the margin the earlier evidence found safe" | `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:45`: start "returned after 34s" with the wrapper question's 30 s fallback. `:56`: "Raising `CCSESSION_ASK_TIMEOUT` above about 45 seconds would make supervised workers fail again". 45 s is a ceiling for the wrapper's *question timeout*, not a measured safe *start duration*; a 45 s fallback would give a start of about 49 s, which the evidence calls failing. | **Overstated** (new finding N13) |
| C2 | WC-4 `SPEC:66` (list of locations the coordinator "cannot know") and pr-submit row `SPEC:135` | `sk/sc-pr-submit-protocol/SKILL.md:170` | pr-submit's deliverable `monitor-run-<PR>.jsonl` lands where the coordinator cannot know before dispatch, so the contract goes to `--report-dir` | `SKILL.md:170` names the run log file only. `cmd/pr-submit.md:55`: `--output-dir <dir>` (default `.dev/pr-monitor/pr-<N>-<ts>/`) "Run-log + artifacts dir", and `INV-B:92` records the same. The directory is caller-set; only the file name carries the PR number. By the spec's own rule (`SPEC:55`) a passed `--output-dir` *is* the report directory. | **Overstated** (new finding N6) |

### 3.2 Citations checked and found correct
| Spec line(s) | Citation | Check |
|---|---|---|
| 56 | `src/superclaude/cli/install_core.py:33,53,62-70` | 33 docstring "Copies all .md files"; 53 `glob("*.md")`; 62-70 copy loop (`shutil.copy2` at 70). OK |
| 56 | `install_core.py:13-24`, `:12,152` | 12 comment "list_installed_core_files reports only these"; 13-24 the frozenset; 152 the filter. OK |
| 56 | `CLAUDE.md:83,408` | 83 `core doc` row `~/.claude/<FILE>.md`; 408 "Core framework files (`.md`) → `~/.claude/`". OK |
| 64 | `CAPS:52`, `CAPS:129`, `INV-A:62`, `INV-A:76-83`, `INV-B:292` | waiting worker is "healthy, not failed"; plain chat offer; gate tables. OK |
| 65 | `CAPS:58-61`, `CAPS:64` | ask usage, resume by ID, never a local prompt; no heartbeat while in `ask`. OK |
| 66 | `cmd/workflow.md:12,42` | 12 generated `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>`; 42 `--output` retired. OK |
| 66, 106 | `cmd/cleanup-audit.md:112` (and `:112-117`) | "Audit reports written to `.claude-audit/` directory only". OK |
| 66, 130 | `cmd/implement.md:58` (and `:57-58,74`) | 57 implicit `--resume`; 58 ledger default `.dev/implement/<slug>/progress.md`; 74 print ledger path. OK |
| 66 | `cmd/research.md:103` | `claudedocs/research_[topic]_[timestamp].md`. OK |
| 66, 367 | `sk/sc-workflow-protocol/refs/return-contract.md:7` | `status: success \| partial \| failed`. OK |
| 66, 367 | `sk/sc-adversarial-protocol/SKILL.md:432`, `:436` | 432 `return_contract:`; 436 `status: "success"  # success \| partial \| failed`. OK |
| 66, 367 | `sk/sc-reflect-protocol/SKILL.md:250` | `status: stopped-precondition`. OK |
| 66 | `CAPS:72-74`, `CAPS:79`; `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41`; `INV-B:272`; `sk/sc-brainstorm-protocol/SKILL.md:335`; `INV-A:97` | report path only with real values; Orca does not read the file (UNVERIFIED there); workflow contract shape and post-creation STOP rule; brainstorm writes `<output>/return-contract.yaml`. OK |
| 67 | `CAPS:73`, `CAPS:76-77` | outcome mandatory; dispatched pane; settles Task. OK |
| 68 | `worker-start --help` line 47 | "--retry-of needs --task naming the failed Task (--spec creates a new one) and does not inherit placement ...". OK (the spec quotes only the first clause; the placement clause matters for N3) |
| 68, 370 | `task-update --help` line 3 | Usage: `--id --status [--result] [--run] [--from] [--retry-request]`; no spec field. OK |
| 68 | `send --help` line 39 | "Use --to dispatch:<id> for attempt-specific coordinator guidance; Orca durably relays it to a connected worker server." OK |
| 68, 370, 400 | `CAPS:46-47`, `CAPS:46`, `CAPS:47` | exit 0 only for ready; Claude task passed in argv. OK |
| 68 | `CAPS:116`, `CAPS:125` | circuit breaker, no routing around it with a new Task; absence never authorizes retry. OK |
| 68 | `INV-A:35-55`, `INV-B:31-52` | column (e) resume per command. OK |
| 72 | `cmd/troubleshoot.md:76` | Tier 2 "2-4 specialist agents fan out in parallel ... +4-15 min". OK |
| 72 | `CAPS:111`, `CAPS:125`, `CAPS:126`, `CAPS:130` | never release on heartbeat; absence never authorizes stop/retry/release; positive stall proofs; cadence from the preamble. OK (111 names release only; 125 covers stop and retry) |
| 72 | `cmd/pr-submit.md:49`; `sk/sc-pr-submit-protocol/SKILL.md:46-64` | "Per-wait wall-clock timeout"; one foreground poll then sleep ≥ `--poll-interval`, repeat. OK |
| 72 | `sk/sc-cli-eval-protocol/SKILL.md:151-152`; `INV-A:65` | "per-eval timeouts can reach 3600s". OK |
| 73 | `cmd/save.md:42-45`; `CAPS:115` | unchanged citations on a changed line; `CAPS:115` placement default. OK |
| 77 | `CAPS:115`, `CAPS:107-113` | placement; release/retain. OK |
| 79 | `CAPS:77`, `CAPS:92` | settles on valid `worker_done`; Run does not schedule. OK |
| 83 | `CAPS:90` | failed Task keeps dependents blocked until a `--retry-of` replacement completes it. OK |
| 85 | `cmd/adversarial.md:15` | "2-10 existing files". OK |
| 95 | `INV-A:3`, `INV-B:3` | scope lists hold 21 and 22 command names. OK (counted) |
| 106 | `sk/sc-cleanup-audit-protocol/SKILL.md:76,113`; `INV-A:42` | `progress.json` resume; `.claude-audit/pass1-summary.md`. OK |
| 113 | `cmd/workflow.md:12`, `:42`; `sk/sc-workflow-protocol/refs/return-contract.md:39`; `SKILL.md:58,66,72`; `INV-B:52,267-275` | 39 "STOPs before the package exists ... chat only — no package directory, no yaml". OK |
| 130 | `sk/sc-implement-protocol/refs/qa.md:231-238`; `sk/sc-implement-protocol/SKILL.md:35`; `INV-A:51,66` | halt row, Ruling rule; `E-NO-RULING`. OK |
| 135 | `sk/sc-pr-submit-protocol/SKILL.md:37-39,46-64,66-68,141,170,189-197,237-246`; `cmd/pr-submit.md:25,39,49,55-56`; `INV-B:34,87-95` | each line exists and says what the row uses. OK as line references; see C2 for the use of `:170` |
| 137 | `cmd/research.md:25,103,123-132`; `src/superclaude/agents/deep-research-agent.md:40-56`; `INV-B:38,127-135` | 25 `--strategy planning\|intent\|unified`; agent 40-44 "Planning-Only ... Direct execution without clarification". OK |
| 200 | `CAPS:145` | `orca-ide` outside, `orca` shim inside. OK |
| 217 | `.dev/codegraph-migration/orchestration/README.md:42` | "W1 observed 27 failures and 16 errors ... compare against a recorded baseline". OK |
| 222 | `CLAUDE.md:16` | "## ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents". OK |
| 239-240, 395 | `CAPS:126`, `CAPS:129` | final-turn proof; `agentWait`. OK |
| 241 | `pyproject.toml:38` | `"pyyaml>=6.0"`. OK |
| 274, 401 | `task-update --help` line 21 | "To cancel a Task, stop or abandon its worker, then set --status failed --result cancelled; a later worker-start --retry-of reopens it." OK |
| 366 | `INV-B:272`, `INV-A:39`, `INV-B:112`, `INV-A:35` | carried from the original row. `INV-A:35` says the adversarial skill "names no filename; real runs wrote `<output>/adversarial/return-contract.yaml`". "Already write `return-contract.yaml`" holds for real runs only. OK as carried |
| 367 | `return-contract.md:6` | `contract_version: "1.1"`. OK |
| 368 | `CAPS:80` | a worker's own `failed` report does not count toward the breaker. OK |
| 369 | `CLAUDE.md:72-83` | installed-path rule and table. OK |
| 396, 397, 399 | `CAPS:131`, `CAPS:130`, `CAPS:67` | transcript source; cadence; `consumer_fenced`. OK |
| `DISP` "Where applied" | every `rSPEC:N` location in `DISP:21-44` and `DISP:47` | each points at the revised line it names (checked against the revised spec). OK |

Result: 2 of the checked citations are overstated (C1, C2); none is missing or points at the wrong line.

## 4. Part 3: spec panel (critique, requirements + architecture)
Mandatory artifacts triggered: the Guard Condition Boundary Table (the spec has guards: report-directory resolution `SPEC:55`, fan-in count `SPEC:85`, gate policy `SPEC:65`, retry kind `SPEC:68`, and the check guards in 7.1-7.2) and Pipeline Dimensional Analysis (the fan-in flow at `SPEC:85`). Advisory: a later `--focus correctness` pass is still recommended (numeric guards at `SPEC:72,85,260`; a multi-stage fan-in).

### 4.1 Requirements analysis
=== REQUIREMENTS ANALYSIS ===

**Karl Wiegers (requirements quality).** The revision closed the round-1 traceability gaps with a real table (`SPEC:293-315`), and the WC rows now name an owner and a mechanism. Two requirement pairs contradict each other. WC-6 (b) allows a same-brief `--retry-of` for any command that "resumes from its on-disk state without a new flag ... or rewrites its contract whole" (`SPEC:68`), while the section 3 reading guide says a named resume mechanism means a same-brief retry is safe and "fresh dir" means a new Task (`SPEC:97`); every named mechanism in P2 is a flag (`SPEC:110-111,126`), which WC-6 (a) says needs a new brief. AC-2.7 then names no command (N2). And the report-directory rule says a command's own directory-valued output flag wins (`SPEC:55`), while the pr-submit row and AC-4.3 put the contract "in `--report-dir`" although pr-submit owns `--output-dir` (`cmd/pr-submit.md:55`) (N6). "How would you validate WC-6 (b) in P2? You cannot pick a subject that both sections accept."

**Gojko Adzic (specification by example).** The worked example (`SPEC:87-92`) is the improvement round 1 asked for, and it holds up against Orca's real verbs (`task-create --help` line 3). Two examples are missing. The ask policy has no example with a second gate, and tdd has two (`SPEC:111`: topic-only clarification and nested `/task` "ask the user"); AC-2.6 expects exactly "one `question` message, one reply" (`SPEC:273`), which a second gate breaks (N7). The worked example also shows that "the answer as a flag" (`SPEC:65`) is not how tdd takes an answer: T2 changes the positional topic (`SPEC:91`).

**Alistair Cockburn (actors and goals).** The person who answers a blocked question is now an actor in the worked example (`SPEC:90`). The person who gives an implement Ruling is the actor D2 protects (`SPEC:337-341`), but the ask policy (`SPEC:65`, `SPEC:77`) lets the coordinator, another agent, stand in that actor's place, and nothing ties the ask policy to D2 (N9). The goal "the coordinator decides what runs next" (`SPEC:79`) has a failure extension for `blocked` inputs only (`SPEC:83`); a `failed` input whose retry must be a new Task strands a dependent created up front the same way (N1).

### 4.2 Architecture analysis
=== ARCHITECTURE ANALYSIS ===

**Martin Fowler (interfaces and boundaries).** The `worker_status` field beside the command's own `status` (`SPEC:66`) is a clean answer to round-1 finding 2, and versioning it separately from workflow's `contract_version` avoids a second collision. The report-directory interface is still not single-valued. For adversarial it gives two homes: WC-4 puts the worker contract at `<report-dir>/return-contract.yaml` with `<report-dir>` = `--output <dir>`, and cites adversarial's nested `return_contract:` block as a contract that keeps its fields in that same file (`SPEC:66`); the 3.1 row moves adversarial's own contract to `<output>/adversarial/return-contract.yaml` (`SPEC:104`), a different directory; AC-1.4 asserts "one fixed path" without saying which (`SPEC:265`) (N4). When a brief passes both an own output flag and `--report-dir`, `SPEC:55` picks the own flag silently; no row says whether that is an error (N6).

**Sam Newman (evolution).** The per-phase flag table (`SPEC:185-195`) fixes round-1 finding 9 and reconciles to 37. The new `worker_contract_version: "1"` gives evolution a hook. No new evolution defect.

**Gregor Hohpe (integration and messages).** Choosing a new Task over `send --to dispatch:<id>` for a changed brief (`SPEC:68`) is justified by the argv launch (`CAPS:47`); `send --help` line 39 says the follow-up is "durably" relayed but not when it is read, which supports the choice. The dependency channel is the weak point: Orca releases a dependent only when its exact dependency Task completes (`CAPS:90`), so every retry that becomes a new Task (all "fresh dir" commands, `SPEC:97`) silently orphans any dependent created with `--deps` on the old Task. `SPEC:83` guards this only for inputs that "can end `blocked`" (N1). The fan-in rule has a lower bound but no upper one (N5).

**Michael Nygard (failure modes).** WC-10 now states the fan-out heartbeat gap honestly and forbids acting on a late heartbeat (`SPEC:72`). The live check that proves a worker stayed inside its own directories is not reliable: `git status --porcelain=v1` collapses an untracked directory to one line, skips ignored paths and shows an already-modified file the same way after a second edit, so step 6 (`SPEC:247-250`) and AC-1.5's "no file written (step 6 empty)" (`SPEC:266`) can pass while a worker wrote elsewhere (N11). The deletions check reads only committed history (`SPEC:229,290`; three-dot diff compares the merge base with `HEAD`), so it passes vacuously on uncommitted phase edits (N8). Under the recommended D3 (a), the only heartbeat check (AC-4.3, `SPEC:282`) never runs (N10).

### 4.3 Adversarial analysis (Whittaker)
=== ADVERSARIAL ANALYSIS ===

**A1. Sequence attack (MAJOR, N1).** I can break this specification by **Sequence Attack**. The invariant at **2.3 dependent-creation rule (`SPEC:83`)** fails when **a coordinator creates a dependent up front on an input that can only fail, not block**. Concrete attack: (1) T1 = `/sc:analyze src/ --unattended --output .dev/a1/` (no gate, `SPEC:120`), T2 = `/sc:design ...` created with `--deps ["T1"]`, which `SPEC:83` allows because analyze "can end `blocked`" is false. (2) T1 crashes; analyze's Resume cell is "fresh dir" (`SPEC:120`), so its retry is a new Task T1' (`SPEC:97`, WC-6 (a)). (3) T1' succeeds. State after: T1 is `failed`, T2 still depends on T1 and stays blocked "until a `--retry-of` replacement completes it" (`CAPS:90`), which WC-6 (a) never creates. T2 never runs.

**A2. Divergence attack (MAJOR, N2).** I can break this specification by **Divergence Attack**. The invariant at **WC-6 (b) (`SPEC:68`) versus the section 3 reading guide (`SPEC:97`)** fails when **AC-2.7 picks its subject**. Concrete attack: the tester picks `/sc:tdd` (named resume `--resume <task-file>`, `SPEC:111`). `SPEC:97` says a named mechanism makes a same-brief `--retry-of` safe; `SPEC:68` says a resume *flag* is a changed brief, so WC-6 (a). The tester picks `/sc:troubleshoot` instead ("fresh dir", `SPEC:112`): `SPEC:97` says new Task; `SPEC:68` (b) still permits `--retry-of` if the contract is rewritten whole. Either choice satisfies one section and violates the other, so AC-2.7's pass is undefined.

**A3. Sequence attack (MAJOR, N7).** I can break this specification by **Sequence Attack**. The invariant at **WC-3 ask policy, "asks once" (`SPEC:65`)** fails when **the re-invoked command hits a second gate**. Concrete attack: T3 = `/sc:tdd "auth" --unattended ...` with `On a blocked gate: ask the coordinator` (AC-2.6, `SPEC:273`). Run 1 blocks on the topic gate; the worker asks; the coordinator answers; run 2 reaches the nested `/task` "ask the user" gate (`SPEC:111`) and writes `worker_status: blocked` again. WC-3 allowed one ask. State after: either the worker asks a second time (AC-2.6's "one `question` message" fails) or it reports `failed` (AC-2.6's "`worker_done --outcome succeeded`" fails). The spec does not say which.

**A4. Sentinel collision attack (MAJOR, N9).** I can break this specification by **Sentinel Collision Attack**. The invariant at **D2 (a) "keep the rule" (`SPEC:339`)** fails when **the coordinator's brief for `/sc:implement` carries `On a blocked gate: ask the coordinator`**, which `SPEC:77` allows for any Task. Concrete attack: implement halts `E-HALT-QA` and writes `worker_status: blocked` with the Ruling question (`SPEC:130`); the worker asks; the coordinator replies "approved"; the worker re-invokes implement with that answer. A coordinator reply is "another agent's message" (`sk/sc-implement-protocol/refs/qa.md:238`). The relay that D2 (b) puts to the user's decision happens under D2 (a) with no decision.

**A5. Accumulation attack (CRITICAL, N5).** I can break this specification by **Accumulation Attack**. The invariant at **fan-in rule (`SPEC:85`)** fails when **more than 10 inputs are admitted**. Concrete attack: the coordinator dispatches 12 `/sc:troubleshoot` workers (nothing bounds N); all 12 end `succeeded`. The rule says "Create the merge Task only when the admitted count is within the merge command's input range (2 to 10 files for adversarial)" and defines only the "fewer than 2" fallback. State after: 12 admitted, no merge, no defined next step; `/sc:adversarial --compare` accepts at most 10 (`cmd/adversarial.md:15`).

**A6. Divergence attack (MAJOR, N6).** I can break this specification by **Divergence Attack**. The invariant at **report directory (`SPEC:55`)** fails when **a brief passes both an own directory-valued output flag and `--report-dir`**. Concrete attack: pr-submit under D3 (b) with `--output-dir .dev/pr/42/ --report-dir .dev/pr/42-report/`. `SPEC:55` makes `.dev/pr/42/` the report directory; the pr-submit row (`SPEC:135`) and AC-4.3 (`SPEC:282`) expect the contract in `--report-dir`. The coordinator, which knows the path "before dispatch" (WC-4), opens `.dev/pr/42-report/return-contract.yaml`, which does not exist, and treats the run as failed (WC-5: no contract → `failed`).

### 4.4 Guard condition boundary table
Nygard built it, Crispin checked completeness, Whittaker attacked the entries. Every GAP row maps to a finding of MAJOR or higher (FR-8). All cells are filled, so synthesis is not blocked (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 report directory | `SPEC:55,66` | Zero/Empty | neither own dir flag nor `--report-dir` | none | No work, fixed chat error, `failed`, no contract | OK |
| G1 | `SPEC:55` | One/Minimal | only `--report-dir <d>` | `<d>` | Contract at `<d>/return-contract.yaml` | OK |
| G1 | `SPEC:55` | Typical | own `--output <dir>` (brainstorm) | `<dir>` | Contract at `<dir>/return-contract.yaml` | OK |
| G1 | `SPEC:55,135,282` | Maximum/Overflow | own `--output-dir` and `--report-dir`, different values | own flag by `SPEC:55`; `--report-dir` by `SPEC:135,282` | Contradictory | GAP (N6) |
| G1 | `SPEC:66,108,111` | Sentinel Value Match | `--output <file>` (tdd, init-lite), no `--report-dir` | none (not directory-valued) | Error; the fixed text tells the caller to pass `--output <dir>` (N12, MINOR wording) | OK |
| G1 | `SPEC:66,104,265` | Legitimate Edge Case | adversarial `--output <dir>` | `<dir>` or `<dir>/adversarial/` | Two conflicting homes | GAP (N4) |
| G2 fan-in admitted count A | `SPEC:85` | Zero/Empty | A = 0 | no merge | Report the failure to the person | OK |
| G2 | `SPEC:85` | One/Minimal | A = 1 | no merge | Report the single result | OK |
| G2 | `SPEC:85` | Typical | A = 3 | merge | Merge Task lists dropped inputs | OK |
| G2 | `SPEC:85` | Maximum/Overflow | A = 12 | outside range | Unspecified | GAP (N5) |
| G2 | `SPEC:81,85` | Sentinel Value Match | `partial` judged unusable | not admitted | Handled like `failed` | OK |
| G2 | `SPEC:85` | Legitimate Edge Case | `blocked` input answered, re-run as a new Task | waits | Merge waits for the new Task or drops it with a reason | OK |
| G3 gate policy | `SPEC:65` | Zero/Empty | no policy line | report blocked | Default stated | OK |
| G3 | `SPEC:65` | One/Minimal | `report blocked` | — | Blocked contract, `worker_done --outcome failed` | OK |
| G3 | `SPEC:65` | Typical | `ask the coordinator`, one gate | ask once | Re-invoke, contract replaced | OK |
| G3 | `SPEC:65,111,273` | Maximum/Overflow | `ask`, re-run hits a second gate | "asks once" | Unspecified | GAP (N7) |
| G3 | `SPEC:65,77,339` | Sentinel Value Match | `ask` policy on an implement Ruling halt under D2 (a) | ask | Relayed Ruling not excluded | GAP (N9) |
| G3 | `SPEC:65` | Legitimate Edge Case | answer arrives after the worker settled | — | New Task (WC-6 (a)) | OK |
| G4 retry kind | `SPEC:68` | Zero/Empty | first attempt | none | Normal run | OK |
| G4 | `SPEC:68,274` | One/Minimal | failed start, same brief, `--retry-of` as AC-2.7 writes it | (b) | Refused: no `--agent`/`--terminal`; placement not inherited (`worker-start --help` lines 3, 47) | GAP (N3) |
| G4 | `SPEC:68,97,274` | Typical | crash of a P2 command, same brief | (a) or (b) | Sections disagree | GAP (N2) |
| G4 | `SPEC:68` | Maximum/Overflow | 3 failed starts | breaker | Task failed; no new Task to route around it (`CAPS:116`) | OK |
| G4 | `SPEC:68` | Sentinel Value Match | earlier attempt reads `unverifiable` | no retry | Absence never authorizes retry (`CAPS:125`) | OK |
| G4 | `SPEC:83,97` | Legitimate Edge Case | failed "fresh dir" input with a dependent created by `--deps` | new Task | Dependent stays blocked forever (`CAPS:90`) | GAP (N1) |
| G5 step 6 attribution | `SPEC:247-250` | Zero/Empty | worker writes nothing | empty diff | Pass | OK |
| G5 | `SPEC:247-250` | One/Minimal | one new file in a tracked, clean directory outside the brief's dirs | new `??` line | Fail, correctly | OK |
| G5 | `SPEC:247-250` | Typical | writes only under a new output dir | new `?? <dir>/` line | Pass | OK |
| G5 | `SPEC:247-250` | Maximum/Overflow | new file inside a directory already untracked before dispatch | no new line (collapsed) | False pass | GAP (N11) |
| G5 | `SPEC:247-250,266` | Sentinel Value Match | write to an ignored path (`.superclaude/`, `.dev/pr-monitor/`) | no line | False pass | GAP (N11) |
| G5 | `SPEC:247-250` | Legitimate Edge Case | second edit to a tracked file already modified before dispatch | same ` M` line | False pass | GAP (N11) |
| G6 deletions check | `SPEC:229,290` | Zero/Empty | no edits | empty | Pass | OK |
| G6 | `SPEC:229,290` | One/Minimal | one committed deleted line | `x 1 path` | Fail, correctly | OK |
| G6 | `SPEC:229,290` | Typical | committed additive edit | `n 0 path` | Pass | OK |
| G6 | `SPEC:229,290` | Maximum/Overflow | many committed files, one with deletions | that row printed | Fail, correctly | OK |
| G6 | `SPEC:229,290` | Sentinel Value Match | edits present only in the working tree | empty (three-dot compares commits) | False pass | GAP (N8) |
| G6 | `SPEC:227` | Legitimate Edge Case | removed `-- item` bullet, committed | counted | Fail, correctly | OK |

### 4.5 Pipeline dimensional analysis (Fowler + Whittaker)
The fan-in flow at `SPEC:85` is the only multi-stage count-changing flow.

```text
[Coordinator: N input Tasks]  (N unbounded)
        |
        v  all N settle (SPEC:85)
[S succeeded] [P partial] [B blocked] [F failed]          S + P + B + F = N
        |          |            |            |
        |   usable U <= P   re-run as new Task or drop   retry or drop
        v          v            v            v
[Admitted A = S + U + R]   (R = re-run replacements that succeeded)
        |
        +-- A < 2        : no merge; report to person           (SPEC:85)  OK
        +-- 2 <= A <= 10 : merge Task, dropped inputs listed     (SPEC:85)  OK
        +-- A > 10       : no rule                               <-- MISMATCH
[Consumer: /sc:adversarial --compare expects 2-10 files]  (cmd/adversarial.md:15)
```

Consistency check: with N = 12 and all succeeded, A = 12 while the consumer accepts at most 10, and the spec defines no step for A > 10. Classified CRITICAL under FR-19 (N5), the same rule round 1 applied to its finding 3.

### 4.6 Expert consensus and disagreements
**Consensus.** The revision fixed what round 1 named; every new defect sits in the new machinery (retry routing, report directory, gate policy, the new check scripts), not in the core decision. The core decision (Orca coordinates, commands stay Orca-free) still stands on `CAPS:97-98`, `CAPS:76` and `SPEC:34`, and no expert disputed it.

**Disagreements.**
- *N5 severity.* Hohpe would rate it MAJOR because a coordinator can choose N ≤ 10. Whittaker holds CRITICAL under FR-19 because nothing in the spec bounds N. Kept CRITICAL for consistency with round 1's finding 3.
- *N3 severity.* Fowler would rate it MINOR because a coordinator can read the help text. Crispin holds MAJOR because the check is written as a literal command and fails for the wrong reason, the same class as round-1 finding 6. Kept MAJOR.
- *N12.* Kept MINOR: behaviour is specified (the run stops); only the hint text misleads.

### 4.7 Quality scores
```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-02
  round: 2
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin]
  focus_areas: [requirements, architecture]
  mode: critique
quality_assessment:
  overall_score: 7.0      # round 1: 5.5
  clarity: 8.0
  completeness: 7.0       # N1, N5, N7
  testability: 6.0        # N2, N3, N8, N10, N11
  consistency: 6.5        # N2, N4, N6, N9
critical_issues: [N5]
major_issues: [N1, N2, N3, N4, N6, N7, N8, N9, N11]
minor_issues: [N10, N12, N13]
adversarial_analysis: sections 4.3-4.5; GAP rows map to N1-N9, N11
```

Testing, compliance and Gregory/Hightower lenses were outside the requested focus; Crispin appears only where an acceptance check is defective.

## 5. New findings
Severity: CRITICAL = provably wrong; MAJOR = ambiguous, incomplete or unsatisfiable under attack (and every GAP row, FR-8); MINOR = wording or citation, behaviour inferable. All 13 were introduced or exposed by the revision; none repeats a round-1 finding. Listed by ID; N5 is the most severe.

1. **N1. A dependent created up front strands when its input fails and must be retried as a new Task.** MAJOR. Section 2.3 (`SPEC:83`), with 3 intro (`SPEC:97`) and WC-6 (a) (`SPEC:68`). `SPEC:83` forbids up-front `--deps` only for inputs that "can end `blocked`". But "fresh dir" commands (most of section 3, for example analyze `SPEC:120`, troubleshoot `SPEC:112`) retry only as a new Task (`SPEC:97`), and Orca keeps a dependent blocked "until a `--retry-of` replacement completes it" (`CAPS:90`). Evidence and trace: Whittaker A1 (section 4.3). Recommendation: create a dependent only after its inputs settle whenever any input's retry would be a new Task, or state that the coordinator re-creates dependents against the replacement Task.
2. **N2. WC-6 (b) and the section 3 reading guide disagree on which commands may use a same-brief `--retry-of`, so AC-2.7 has no defined subject.** MAJOR. WC-6 (`SPEC:68`); section 3 intro (`SPEC:97`); AC-2.7 (`SPEC:274`). `SPEC:68` (b): resume "without a new flag" or rewrite the contract whole; a resume flag is a changed brief, so (a). `SPEC:97`: any named resume mechanism makes a same-brief retry safe, and "fresh dir" means a new Task. Every named mechanism among P2 commands is a flag (release-split `--resume-from` `SPEC:110`, tdd `--resume <task-file>` `SPEC:111`, cli-portify `--resume <contract>` `SPEC:126`); the other P2 cells are "fresh dir", "fresh file", "n/a", or "add a resume input, or fresh run" (`SPEC:121-143`). AC-2.7 says only "one P2 worker". Recommendation: make `SPEC:97` match WC-6 (b) (flag-based resume is WC-6 (a)), and name AC-2.7's subject, for example a command whose re-run rewrites its contract whole (init-lite, "Re-run overwrites its marked report", `SPEC:108`), moving AC-2.7 to the phase that adds that command's flag.
3. **N3. AC-2.7's retry command omits the placement and agent flags Orca requires on `--retry-of`.** MAJOR. AC-2.7 (`SPEC:274`); WC-6 (b) (`SPEC:68`). `SPEC:274` writes `worker-start --task <task_id> --retry-of <dispatch_id>`. `orca orchestration worker-start --help` line 3 requires `(--agent <agent> | --terminal <handle>)`, and line 47 says `--retry-of` "does not inherit placement; repeat the intended --on/worktree and --agent/terminal choices". Orca's own form is `worker-start --task <task_id> --retry-of <dispatch_id> --worktree <explicit_placement> --agent <agent> --json` (`CAPS:116`). Run verbatim, the check is refused for a reason unrelated to WC-6. WC-6 (b) also does not tell the coordinator to repeat placement. Recommendation: write the full form in AC-2.7 and add "repeat `--worktree` and `--agent`" to WC-6 (b), citing line 47's second clause.
4. **N4. Adversarial's worker contract has two conflicting homes.** MAJOR. WC-4 (`SPEC:66`); 3.1 adversarial row (`SPEC:104`); AC-1.4 (`SPEC:265`). WC-4: report directory = `--output <dir>`, contract at `<dir>/return-contract.yaml`, and "A command that already writes `return-contract.yaml` in the report directory keeps every existing field, including ... nested blocks such as adversarial's `return_contract:`". The 3.1 row's P1 fix puts adversarial's own contract at `<output>/adversarial/return-contract.yaml`, a different directory; past runs wrote there and one level deeper (`INV-A:60`). AC-1.4 asserts "adversarial names one fixed path" without naming it. A coordinator cannot tell whether to open `<dir>/return-contract.yaml` (worker fields only) or `<dir>/adversarial/return-contract.yaml` (merged). Recommendation: state one layout: either adversarial writes its contract (with the worker fields) at `<output>/return-contract.yaml`, or the worker contract at `<output>/` lists `<output>/adversarial/return-contract.yaml` in `artifacts`; then drop adversarial from WC-4's "same file" example and make AC-1.4 assert the chosen path.
5. **N5. The fan-in rule has no step when more than 10 inputs are admitted.** CRITICAL (FR-19 dimensional mismatch). Section 2.3 fan-in rule (`SPEC:85`); 1.3 (`SPEC:40`). The rule creates the merge only when the admitted count is "within the merge command's input range (2 to 10 files for adversarial, `cmd/adversarial.md:15`)" and defines a fallback only for "fewer than 2". Nothing bounds N. Trace: N = 12, all succeeded, A = 12, no merge and no next step (section 4.5). Recommendation: cap N at the merge command's maximum when the coordinator plans the fan-out, or define a staged merge (for example batches of at most 10, then a merge of the batch results).
6. **N6. Report-directory precedence is contradicted for pr-submit and unstated when a brief passes both flags.** MAJOR. 2.1 report directory (`SPEC:55`); WC-4 (`SPEC:66`); pr-submit row (`SPEC:135`); AC-4.3 (`SPEC:282`). `SPEC:55`: the own directory-valued flag (`--output-dir <dir>` included) is the report directory "when the brief passes one, otherwise" `--report-dir`. pr-submit owns `--output-dir <dir>`, "Run-log + artifacts dir" (`cmd/pr-submit.md:55`; `INV-B:92`), yet `SPEC:135` and `SPEC:282` put the contract "in `--report-dir`", and WC-4 lists pr-submit's run log among locations the coordinator cannot know before dispatch (citation C2). Trace: Whittaker A6. Recommendation: say that a brief passes exactly one of the two (refuse both under `--unattended`, like a person-mode flag), and fix the pr-submit row and AC-4.3 to use `--output-dir` as its report directory.
7. **N7. The ask policy's "asks once" has no rule for a second gate, and "the answer as a flag" does not fit commands that take the answer positionally.** MAJOR. WC-3 (`SPEC:65`); tdd row (`SPEC:111`); AC-2.6 (`SPEC:273`); worked example (`SPEC:91`). tdd has two gates under `--unattended` (topic-only clarification and nested `/task` "ask the user", `SPEC:111`); AC-2.6's T3 expects exactly "one `question` message, one reply, then one `worker_done --outcome succeeded`". If the re-run blocks again, WC-3 says neither "ask again" nor "report blocked". The worked example's T2 changes the positional topic (`SPEC:91`), not a flag. Trace: Whittaker A3. Recommendation: define the bound (for example "at most one ask per gate; a second blocked result after an answered ask is reported as blocked"), say "the answer as the command's argument or flag", and make AC-2.6 T3 use an input that reaches only one gate or accept the stated second-gate outcome.
8. **N8. The deletions check passes vacuously on uncommitted edits.** MAJOR. AC-C5 (`SPEC:227-230`), AC-0.3 (`SPEC:258`), AC-2.1's SA-6 check (`SPEC:268`), block `SPEC:289-290`. All run `git diff --numstat master...HEAD -- <file>`. `git help diff`: "git diff A...B is equivalent to git diff $(git merge-base A B) B", a commit-to-commit diff; working-tree and staged edits are not in it. The spec never requires the phase's edits to be committed before the check, and this repo commits only when asked (`CLAUDE.md:37`: "Staging is not committing: commit only when asked"). Recommendation: diff the working tree against the merge base (`git diff --numstat $(git merge-base master HEAD) -- <file>`, which includes uncommitted edits), or state that the check runs only after the phase commit.
9. **N9. Nothing stops the ask policy from relaying an implement Ruling under D2 (a).** MAJOR. WC-3 (`SPEC:65`); 2.3 brief contents (`SPEC:77`); implement row (`SPEC:130`); D2 (`SPEC:337-341`); AC-4.1 (`SPEC:280`). 2.3 lets the coordinator choose either policy for any Task. Under the ask policy the coordinator's reply becomes the input of the re-invoked implement run, which is the relay D2 (b) puts to the user and D2 (a) rejects, because "another agent's message" is not acceptance (`sk/sc-implement-protocol/refs/qa.md:238`). AC-4.1 does not state the policy line. Trace: Whittaker A4. Recommendation: under D2 (a), require `On a blocked gate: report blocked` for implement briefs (and refuse the ask policy for a Ruling halt), and put the policy line in AC-4.1.
10. **N10. WC-10's heartbeat duty has no live check under the recommended D3 (a).** MINOR. 7.4 WC-10 row (`SPEC:307`); AC-4.3 (`SPEC:282`); D3 (`SPEC:345`). WC-10 maps to AC-2.1 (a static assertion about cli-eval's wait size) and AC-4.3, which runs only "If D3 allows pr-submit as a worker". 7.2 has no heartbeat step. Recommendation: add a heartbeat-spacing assertion (outside fan-out) to 7.2 step 5, so every live check covers it.
11. **N11. 7.2 step 6 can pass while a worker wrote outside its directories.** MAJOR. 7.2 steps 0 and 6 (`SPEC:234-237,247-250`); AC-1.5 (`SPEC:266`). `git status --porcelain=v1` (default untracked mode) collapses an untracked directory into one line: on this worktree it printed only `?? .dev/orca-command-refactor/`, while `-uall` printed 8 files, including this review written after the snapshot would have been taken. It also omits ignored paths: `git check-ignore -v` shows `.superclaude/` (`.gitignore:114`) and `.dev/pr-monitor/` (`.gitignore:246`) ignored, which are save's memory and pr-submit's default run-log directories. A second edit to a tracked file already modified before dispatch keeps the same ` M` line. Each case gives an empty diff in step 6, so AC-1.5's "no file written (step 6 empty)" can also pass falsely. Recommendation: snapshot with `git status --porcelain=v1 -uall --ignored` plus content hashes of already-modified files (or run live checks in a fresh worktree), and compare those.
12. **N12. The fixed missing-directory error names `--output <dir>`, which is wrong for several commands.** MINOR. WC-4 (`SPEC:66`, "`unattended mode needs --output <dir> or --report-dir <dir>`"). workflow bans `--output` (`E-LEGACY`, `cmd/workflow.md:42`); tdd and init-lite take `--output <file>` (`SPEC:108,111`); auggie-review and pr-submit use `--output-dir` (`SPEC:121`, `cmd/pr-submit.md:55`). Following the hint breaks workflow (STOP) and points a tdd caller at a directory for a file flag. Recommendation: make the text name `--report-dir <dir>` only, or let each command's `## Unattended mode` section print its own flag.
13. **N13. AC-0.5's 45-second threshold is attributed to evidence that does not establish it.** MINOR. AC-0.5 (`SPEC:260`); citation C1. `EVIDENCE.md:45` measured a 34 s start with a 30 s wrapper fallback; `EVIDENCE.md:56` says a *fallback setting* above about 45 s fails. Neither measures 45 s as a safe start duration. Recommendation: cite the 34 s measurement and state 45 s as a chosen margin under the 60 s default (`CAPS:44`), or derive the threshold from the 60 s limit.

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| How to find "citations added or changed by the revision" | Trust `DISP`'s "Where applied" list; diff against the pre-revision spec | Diff: the original survives in Claude Code file history (section 1), so the changed-line set is mechanical rather than taken from the reviser's own account. |
| Scope of the citation check | Every citation in the spec; citations on changed lines | Changed lines, as the brief asks. Unchanged lines were covered by round 1 and the inventories' own checks; one carried citation on a changed line (`INV-A:35` at `SPEC:366`) was still read. |
| Orca executable | `orca-ide`; `orca` | `orca`: this session runs inside an Orca terminal, where the README allows the shim (`.dev/orca-command-refactor/README.md:17`); `which` showed it execs the same build. |
| Prove check defects by running them | Argue from git semantics; run read-only commands | Ran `git status --porcelain=v1` and `-uall`, `git check-ignore -v`, AC-C1 and the `awk` filter. Nothing was written to the repo. The three-dot behaviour was taken from `git help diff`, because showing it live would need an edit to a tracked file. |
| Severity of N5 | MAJOR; CRITICAL | CRITICAL under the command's FR-19 rule, matching round 1's finding 3. |
| Severity of N3 | MINOR; MAJOR | MAJOR: a literal check command that is refused is the same class as round-1 finding 6. |
| Step 6 "Improve" | Write an improved spec; review only | Review only: the brief forbids editing the spec. |
| Verdict rule | Allow minor issues; binary | Binary, per the brief: any finding of any severity is FAIL. |

## UNVERIFIED items
1. Whether `/sc:implement`, which will execute each phase plan (`SPEC:197`), commits before the phase's acceptance checks run. If it does, N8 is mitigated in practice but still unstated in the spec. Not read.
2. Whether `worker-start --retry-of` without `--agent` is refused at argument parsing or later. The usage line (`worker-start --help` line 3) marks the group as required; the call was not run, because creating a retry would affect live orchestration state.
3. Whether a nested command invoked by another command under `--unattended` (for example tasklist's Stage 10.5 reflect fan-out) writes worker fields into its own contract. Checked and not raised as a finding: tasklist gives each reflect its own `--output TASKLIST_ROOT/validation/reflect-pre/phase-<P>/` (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md`, Stage 10.5 command block), so no report-directory collision follows.
4. Whether Orca's `--deps` can be edited after creation to point at a replacement Task (N1). `task-update --help` shows only `--status` and `--result` (line 3); no other verb was read.
5. Carried from the spec and still open: its UNVERIFIED items 1-21 (`SPEC:381-401`). Item 22 (`SPEC:402`, no fresh-context citation check of the revisions) is answered by section 3 of this review.
