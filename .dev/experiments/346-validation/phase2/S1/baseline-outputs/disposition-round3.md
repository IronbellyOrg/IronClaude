# Disposition of spec-panel round-3 findings and the three simplifications

Task: task_34d329dd457f (Task 10, final constrained revision). Planning only.
Inputs: `.dev/orca-command-refactor/review/spec-panel-round3.md` (cited `R3:N`), the spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (cited `SPEC:N` for the frozen v3 file, identical to `specs/history/spec-v3-after-round2.md`, 414 lines, 92,194 bytes; `rSPEC:N` for the file after this revision), inventories (`INV-A:N`, `INV-B:N`, `CAPS:N`).
Output: this file, plus edits to the spec.

## Method
- Read in full before any edit: `.dev/orca-command-refactor/README.md` (1-38), `R3` (1-281), the spec (1-414). `cmp` showed the spec identical to `specs/history/spec-v3-after-round2.md` (both 92,194 bytes) before editing.
- Evidence re-read live on 2026-11-02 for every new or changed citation: `src/superclaude/skills/sc-init-lite-protocol/SKILL.md:59-66` (63: "**Default = report only** — the only write is the marked report at `output`"); `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:92` ("Write: Report generation restricted to `.claude-audit/` output directory"); `src/superclaude/commands/cleanup-audit.md:112` ("Audit reports written to `.claude-audit/` directory only"); `CAPS:84-128` (90: dependents of a cancelled Task stay blocked; 116: retry form and circuit breaker; 125: absence never authorizes retry); `CLAUDE.md:299` (worktrees live under `./.dev/worktrees/`); `orca orchestration worker-start --help` in this Orca terminal, build `1.4.237-aidev02.0e4491a95e92` (line 18: `--worktree` accepts `path:<path>`; line 47: `--retry-of` rule).
- Rules applied (from the brief, binding): S1-S3 replace machinery; each M finding gets the smallest wording change; nothing new is added unless a finding names it missing; text unrelated to M1-M14 and S1-S3 is untouched; the spec must end smaller than 92,194 bytes.
- After the edits: `git status --short` printed `?? .dev/orca-command-refactor/` and `?? .dev/review-loop-convergence/`; no tracked file changed. The second untracked folder was not created by this task.

## Disposition table
17 rows: 3 simplifications applied; of the 14 findings (`R3:247-260`), 9 applied (M1 in part), 5 superseded, 0 rejected outright (M1's IDs and live fan-in check are rejected, see its row). "Where" cites the revised spec (`rSPEC:N`, 405 lines).

| # | Item (short) | Disposition | What changed | Where |
|---|---|---|---|---|
| S1 | Cap fan-in at the merge maximum of 10; delete the staged merge | **Applied** | The coordinator plans N ≤ 10 (`cmd/adversarial.md:15`); a re-run replaces its input, so admitted ≤ 10; merge only with ≥ 2 admitted. The staged-merge sentence is deleted, and the Decisions row now records "Cap". | Fan-in rule `rSPEC:87`; Decisions "Fan-in upper bound" `rSPEC:377` |
| S2 | Every live check in a fresh disposable worktree; delete the snapshot machinery | **Applied** | 7.2 now runs one worker in a fresh disposable worktree holding the phase's edits, under `.dev/worktrees/` (`CLAUDE.md:299`), started with `--worktree path:<disposable worktree>` (`worker-start --help` line 18) and removed after step 7. Step 0 (`touch` marker, `git status -uall --ignored` snapshot) is deleted; step 6 is plain `git status --porcelain` in that worktree, and states that ignored paths are not checked. AC-0.4's step list changes from "0-3" to "1-3". The Decisions row is rewritten. | 7.2 intro `rSPEC:235`; step 1 `rSPEC:236`; step 6 `rSPEC:245`; AC-0.4 `rSPEC:254`; Decisions "Worktree-change detection in 7.2" `rSPEC:380` |
| S3 | Every retry is a new Task; delete the same-brief `--retry-of` rule and AC-1.7 | **Applied** | WC-6 is rewritten as one rule: the coordinator never uses `--retry-of`; every retry is a new Task with its own output and report directory, recording the old Task ID; the circuit-breaker and "not while unsettled" limits and the `send --to dispatch` sentence are kept. WC-6 (a)/(b)/(c) labels are gone, so every "WC-6 (a)" reference now reads "WC-6". The reading guide drops the (b) classification. AC-1.7 and the "Same-brief retry eligibility" Decisions row are deleted; the 7.4 WC-6 row maps to AC-2.6 only. The 2.3 dependent bullet no longer refers to a `--retry-of` replacement. | WC-3 `rSPEC:67`; WC-6 `rSPEC:70`; 2.3 dependent bullet `rSPEC:85`; fan-in `rSPEC:87`; reading guide `rSPEC:99`; AC-2.6 `rSPEC:268`; 7.4 WC-6 `rSPEC:298`; Decisions "Retry channel" `rSPEC:366`, "Dependent creation" `rSPEC:375` |
| M1 | 2.3 rules unchecked; `WORKER-CONTRACT.md` contents unchecked | **Applied in part** | AC-0.1 now also runs `tests/skills/test_worker_contract.py` (already a P0 deliverable, `rSPEC:181`), which asserts the file states each rule 2.1 assigns to it and the 2.3 dependent-creation and fan-in rules; 7.4 gains a row mapping those 2.3 rules to AC-0.1. **Rejected parts:** new CO-1/CO-2 IDs and a P2 live fan-in check, because the brief's guardrail prefers the smallest change and a static assertion closes "no check" for both named gaps; the coordinator is a session, not a command under test (`rSPEC:316`, non-goal 3). | AC-0.1 `rSPEC:251`; 7.4 `rSPEC:304` |
| M2 | Ask path re-runs in place whatever the re-run safety; approval gates have no answer flag | **Applied** | WC-3's ask path now applies only at a gate that fires before the command writes any output except its blocked contract and whose answer fits an existing argument or flag; any other gate is reported blocked. This excludes review-translation's post-output gate and the cli-portify/task approval gates without editing their rows. | WC-3 `rSPEC:67` |
| M3 | "Exactly one report directory" depends on unstated flag types | **Applied** | 2.1 now says the directory-valued flags are the command's *existing* ones, and an output flag a section 3 row adds is file-valued, so those commands always take `--report-dir` (the review's second option, one sentence instead of nine row edits). | Report directory term `rSPEC:57` |
| M4 | Contract write breaks init-lite's and cleanup-audit's write-scope rules | **Applied** | init-lite row: "None" becomes an `--unattended` amendment of Safety Invariant 3 (`sk/sc-init-lite-protocol/SKILL.md:63`). cleanup-audit row: adds the `--unattended` amendment of its `.claude-audit/`-only scope (`cmd/cleanup-audit.md:112`; `sk/sc-cleanup-audit-protocol/SKILL.md:92`). SA-4's list of named fixes gains "init-lite and cleanup-audit write scope". | cleanup-audit `rSPEC:108`; init-lite `rSPEC:110`; SA-4 `rSPEC:172` |
| M5 | Staged merge has no rule above 100 inputs | **Superseded by S1** | The staged merge no longer exists; N is capped at 10. | — |
| M6 | AC-1.7 can pass vacuously | **Superseded by S3** | AC-1.7 is deleted. | — |
| M7 | 7.2 step 6 false-fails on `.venv/` and tool caches | **Superseded by S2** | Step 6 no longer lists ignored paths, and `.venv/`, `.pytest_cache/`, `__pycache__/` are ignored (`.gitignore:56,48,2` per `R3:21`). | — |
| M8 | Two Resume cells cannot be classified for same-brief retry | **Superseded by S3** | No classification exists: every retry is a new Task; a Resume cell now only names what the new Task may pass. | — |
| M9 | Implement row drops "while D2 is (a)" | **Applied** | The row now reads "while D2 is (a), a Ruling halt is never asked". | Implement row `rSPEC:132` |
| M10 | AC-4.3 hardcodes 5 minutes | **Applied** | "at most 5 minutes apart" becomes "at most the preamble's cadence apart". | AC-4.3 `rSPEC:276` |
| M11 | 7.2 step 0 uses `<task_id>` before step 1 creates it | **Superseded by S2** | Step 0 is deleted. | — |
| M12 | AC-1.5 expects the absence that 7.2 steps 3-4 fail on | **Applied** | AC-1.5 now runs "as a 7.2 live check whose steps 3-4 are replaced by this row's conditions". | AC-1.5 `rSPEC:261` |
| M13 | `/sc:spawn` row prescribes the up-front DAG | **Applied** | The row now says the coordinator creates the Tasks itself, each dependent only after its inputs settle (section 2.3). | `/sc:spawn` row `rSPEC:159` |
| M14 | "readers" half of the adversarial rationale cites a line naming no reader | **Applied (narrowed)** | "and readers" is deleted, so the claim is exactly what `INV-A:35` supports. Citing `ensemble.py:567-578` instead was the review's option; deleting is smaller and the WC-4 rule does not depend on the reader. | Decisions "Adversarial's worker contract" `rSPEC:376` |

## Independent verification and fixes
A fresh-context agent diffed the old and new spec against this table (read-only). It confirmed the size, every `rSPEC` line number, the 9/5 counts and that no stale reference to WC-6 (a)/(b)/(c), AC-1.7, step 0, the snapshot or "5 minutes apart" remains. Its verdict was **FAIL**, with 8 defects, each fixed by a wording change on an existing line (no line added):

| # | Defect | Fix | Where |
|---|---|---|---|
| V1 | WC-6 said "same brief", but each new Task's brief carries its own report directory, so no brief is ever unchanged and the circuit-breaker limit had nothing to act on | "whether or not its command line changes"; "an unchanged command line is never re-created after three failed starts" | WC-6 `rSPEC:70` |
| V2 | A mandatory new *output* directory breaks implement's implicit ledger resume and cleanup-audit's fixed `.claude-audit/` | WC-6 and the reading guide now require only a new *report* directory; a new output location applies only to start-over cells "where the command has one" | WC-6 `rSPEC:70`; reading guide `rSPEC:99` |
| V3 | init-lite's "Re-run overwrites", cleanup-audit's `progress.json` checkpoint and index-repo's `mode=update` fit no category of the new reading guide | The guide now treats "fresh dir/file/package", "n/a" and an overwriting re-run as start-over, and every other Resume cell as the way the new Task continues | Reading guide `rSPEC:99` |
| V4 | 2.1 still listed WC-6 among the command-side rules, but WC-6 is now coordinator-only | WC-6 moved to "the coordinator's rules (WC-6 and section 2.3, including its brief template)" | Contract file term `rSPEC:58` |
| V5 | AC-0.1 (M1 fix) tested for 2.3 rules that 2.1 never assigned to `WORKER-CONTRACT.md` | Same edit as V4: 2.1 now assigns section 2.3 to the file, so AC-0.1 and the P0 scope (`rSPEC:181`, "the contents section 2.1 assigns to it") agree | `rSPEC:58` |
| V6 | S2: the phase's own uncommitted edits in the disposable worktree would show in step 6's `git status` and false-fail | Step 6 passes only "every path it prints that the phase did not edit" against the brief's directories | 7.2 step 6 `rSPEC:245` |
| V7 | The new header line was in no row | Recorded here: one provenance line pointing to this file, following the Task 6 and Task 8 lines above it | Header `rSPEC:6` |
| V8 | The Decisions preamble credited rows 377 and 380 to Task 8 | Appended "Task 10 rewrote the fan-in and worktree-detection rows" | Decisions preamble `rSPEC:357` |

Not changed: section 1.1's "a resume or safe re-run" (`rSPEC:19`), which the agent flagged as describing the old rule. A new Task in its own report directory is a safe re-run, so the sentence is still true; it is also outside M1-M14 and S1-S3.

## Final size
`wc -c .dev/orca-command-refactor/specs/orca-worker-contract-spec.md` = **89,089 bytes** (was 92,194; 3,105 smaller), 405 lines (was 414). The frozen copy `specs/history/spec-v3-after-round2.md` is unchanged.

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| M3 fix form | State the type in nine rows; one rule in 2.1 | One rule: one sentence, and it removes the ambiguity for any later row too. |
| M2 fix form | List ask-eligible gates per row; one condition in WC-3 | One condition: it decides eligibility from facts each row already states, with no row edits. |
| M14 fix form | Cite `ensemble.py:567-578`; delete "and readers" | Delete: narrowing is preferred by the brief, and the remaining claim is fully supported by `INV-A:35`. |
| M1 scope | IDs, static test, live fan-in check; static test only | Static test in the existing P0 test file plus one 7.4 row; see the M1 row for the rejected parts. |
| S2 worktree placement | `--worktree new-child`; `path:` selector on a repo-made worktree | `path:` on a worktree under `.dev/worktrees/`, because the repo rule fixes the location (`CLAUDE.md:299`) and `new-child` placement is not under that rule's control (UNVERIFIED where Orca puts it). |
| S2 step numbering | Renumber 1-7 to 0-6; keep 1-7 | Keep 1-7, so only AC-0.4's "0-3" needed changing; no other check cites step 0. |
| UNVERIFIED item 23 in the spec (no fresh check of the Task 8 revisions) | Update it; leave it | Leave it: it is unrelated to M1-M14 and S1-S3, and the brief forbids touching unrelated text. `R3` section 3 answers it. |

## UNVERIFIED items and residual risks
1. Whether `worker-start --worktree path:<path>` accepts a git worktree Orca did not create (stated inline at `rSPEC:236`).
2. How the phase's uncommitted edits, and the `.claude/` copies from `make sync-dev` (gitignored, so absent from a fresh checkout), reach the disposable worktree. 7.2 now requires the worktree to "hold the phase's edits" but leaves the method to each phase plan. Which command copy a worker in that worktree loads (project `.claude/` or `~/.claude/`) was not checked.
3. S2 narrows step 6: writes to ignored paths are no longer detected. For `/sc:save` this is still covered by AC-3.4's hash check; for other commands an ignored-path write outside the brief would now pass.
4. S3 gives up Orca's own `--retry-of` path for failed starts (`CAPS:116`). Whether Orca's circuit breaker still bounds repeated new Tasks for the same brief is not mechanical: WC-6 keeps the rule that an unchanged brief is never re-created after three failed starts, which the coordinator must apply itself.
5. Carried, still open: the spec's UNVERIFIED items 1-23 (`rSPEC:383-405`).
