# Merge Execution Log

## Metadata
- Base: Variant 1 (opus:architect), `variant-1-opus-architect.md`
- Executor: merge-executor agent
- Changes applied: 42 of 42 planned (41 applied as planned, 1 applied with a deviation: Change 13, narrowed)
- Status: success, with gate_status BLOCKED_BY_INVARIANTS (INV-005 owner sign-off not recorded)
- Timestamp: 2026-11-08T05:15:35Z
- Merged output: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/adversarial/merged-output.md`
- Plan: `refactor-plan.md` in this folder, after review 3
- Reviews: `refactor-plan-review.md`, `refactor-plan-review-2.md`, `refactor-plan-review-3.md` (all in this folder). Review 3's one blocking finding (P1) is carried as an open gap in merged section 18, G-1. No further fix pass and no fourth review were run.

Provenance convention used (Change 1): a `Provenance:` line under every numbered heading (19 lines: sections 1 to 18 plus 17.1), an HTML `<!-- Source: ... -->` comment under each, and inline `[source; Change N]` tags on changed text only. Text without an inline tag is unchanged V1 text.

## Changes Applied
Merged section numbers are used in Target and After. V1 section N maps to merged section N+1 for V1 sections 5 to 11, and V1 sections 12, 13, 14 map to merged 15, 16, 17 (Change 40).

### Change 1: Provenance convention for every merged section
- **Status**: Applied
- **Source**: Plan process requirement; text from V1, V2, V3, V1R3, V2R3, V3R3
- **Target**: Base, header block and every numbered section
- **Before**: V1 carried no provenance annotations.
- **After**: Header comment block, a citation key, a `Provenance:` line and a Source comment under each of the 19 numbered headings, inline tags on changed text.
- **Provenance tag**: `<!-- Source: Base (original, modified) per Changes 1, 2, 38, 42 -->` (header)
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 2: Correct every seed-brief reference
- **Status**: Applied
- **Source**: Conv:324 (Conv P3.7 item 1); task instruction
- **Target**: Base, header block and section 1
- **Before**: Relative `../../seed-brief.md` style references.
- **After**: The absolute path `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/seed-brief.md` in the header (line 32) and in section 18, G-2. A grep for `../../seed-brief` finds no hit.
- **Provenance tag**: `[Conv:324; Change 2]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: Run binding, Orca-down behaviour and exit codes (High risk)
- **Status**: Applied
- **Source**: V3R3:31 (final text); V1R3:22, V2R3:24; V3:161-166
- **Target**: Base, FR-002, FR-018, FR-019; section 5.1; section 11 Orca rows, No Run bound row, output-dir row
- **Before**: V1 let a sweep without a binding exit 0 and treated Orca-down without a binding as a degraded report.
- **After**: Without `--run`, an unavailable lookup exits 2 with `Orca unavailable; no Run binding could be established: pass --run <id>` and a confirmed missing binding exits 2 with `no Run bound: pass --run <id>`; neither writes a report or success JSON. With an explicit or established binding, a later unavailable result continues disk-only and exits 0 after publication. Exit 0 means the report was published. Exit 1 covers allowlist misses and report write failures, with no success JSON. FR-002 carries three tests plus a fourth gated on step 1.0a. A grep for "exit 0" finds only the FR-001 `CliRunner` AC, the FR-002 and FR-019 tests that publish with a binding, and section 5.1's "exit 0 means ... published"; none says a run without a binding exits 0.
- **Provenance tag**: `[V3R3:31; INV-001; Change 3]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 4: Four-class Orca result classifier
- **Status**: Applied
- **Source**: V3R3:32; V1R3:23, V2R3:25 (Conv:273)
- **Target**: Base, section 8 seam description; section 11 Orca rows; new FR-026
- **Before**: V1 had one undifferentiated Orca failure path.
- **After**: Every `_orca` result is `ok`, `no_binding`, `unavailable` or `call_failed` (section 8); FR-026 holds five tests; an empty zero-exit `run-current` body is `unavailable`, never `no_binding`; section 11 has a `call_failed` row.
- **Provenance tag**: `[V3R3:32; INV-002; Change 4]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: Tri-state person-started with a completeness guard
- **Status**: Applied
- **Source**: V3R3:33; V1R3:24, V2R3:26 (Conv:274); V3R3:55 (INV-009)
- **Target**: Base, section 7 data model, rule 7 and rule 8; FR-010
- **Before**: `person_started: bool`, true for any unjoined transcript.
- **After**: `person_started: bool | None`; True only with a complete negative join; None never becomes idle or Historical; three incomplete-case ACs.
- **Provenance tag**: `[V3R3:33; INV-003; Change 5]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Rule 2 declines when proof is missing, with a test that exercises the decline
- **Status**: Applied
- **Source**: V3R3:53, V1R3:42 (note text), V2R3:44; Conv:255, Conv:326
- **Target**: Base, section 7 rule 2; FR-009
- **Before**: V1 rule 2 had no decline path for unreadable fencing evidence, and its test used a blocked contract.
- **After**: With unreadable fencing evidence rule 2 declines and attaches `Orca: exited; fenced evidence not readable`; two AC cases, neither using a blocked contract (the INV-007 rule-2 test correction).
- **Provenance tag**: `[V3R3:53; INV-007; Change 6]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 7: Accepted risks needing owner sign-off, and scoped lock claims
- **Status**: Applied
- **Source**: V3R3:34 (risk statement); V1R3:25, V2R3:27; Conv:275
- **Target**: Base, new section 13; NFR-002; section 8 lock paragraph; section 9 coverage header; section 11 index.lock row; section 12 R3
- **Before**: Unscoped claims that the sweep never takes the lock (V1:180, V1:259, V1:275).
- **After**: Section 13 holds only INV-005 with the V3R3:34 risk statement verbatim, "Owner sign-off: not recorded.", and a statement that it is an accepted risk, not a requirement. No `GIT_OPTIONAL_LOCKS` sentence or other mitigation for `_orca` appears there. All lock-free claims are scoped to the sweep's own `_git` calls; the coverage header prints `Orca read verbs' git effects on worker worktrees: UNVERIFIED`.
- **Provenance tag**: `<!-- Source: V3R3:34 risk statement, inserted per Changes 7 and 40 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 8: Open warnings section for INV-008, INV-011 and INV-017
- **Status**: Applied
- **Source**: Conv:308-318; V1R3:43, V3R3:54; V1R3:45, V2R3:47, V3R3:56; V1R3:48, V2R3:49
- **Target**: Base, new section 14; section 9 coverage header; FR-015
- **Before**: Section did not exist.
- **After**: Section 14 holds the three entries as the plan states them, plus the Review 3 note under INV-017 (no requirement makes `binary not found: orca-ide` visible without `--run`; it is visible in the report coverage header only when `--run` is passed). The untracked-paths limitation line is in the section 9 header and the untracked-directory rule is in FR-015.
- **Provenance tag**: `<!-- Source: Round 3 texts, inserted per Changes 8 and 40 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 9: Orca binary resolution with the corrected skill citation
- **Status**: Applied
- **Source**: V1R3:48, V2R3:49; orca-cli SKILL.md lines 21-27; Conv:325
- **Target**: Base, section 8 seam; section 9 coverage header; NFR-003; section 11 binary-not-found row
- **Before**: `["orca-ide", *args]` and a "never bare" wording in V1R3.
- **After**: `_orca` runs `ORCA_CLI_COMMAND` if set, else `orca-ide`, stated as a deliberate deviation from SKILL.md:27 (the bare orca wording correction). The resolved binary is in the coverage header; the binary-not-found row gives `unavailable` with reason `binary not found: orca-ide`; NFR-003's expected argv[0] follows the resolution. A grep for "never bare" finds no hit.
- **Provenance tag**: `[V1R3:48; Change 9]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Round 3 agreed texts for INV-004, INV-006, INV-010, INV-015
- **Status**: Applied
- **Source**: V1R3:40, V3R3:51; V1R3:41, V2R3:43, V3R3:52; V1R3:49; V1R3:50; Conv:308, Conv:320
- **Target**: Base, section 9 header; section 7 data model; FR-020; NFR-005
- **Before**: V1 lacked these agreed texts.
- **After**: The agreed texts are in place: the 50-call cap counts only `worker-show` calls (FR-020), NFR-005's test injects `now` and the output path, and the section 7 and section 9 additions.
- **Provenance tag**: `[V1R3:50; INV-015; Change 10]` and similar
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 11: `worker-list` pagination gated on step 1.0a, with lower-bound totals
- **Status**: Applied
- **Source**: V3R3:42, Conv:263; V2:63; V3:63, V3:274; V3:114, V3:299
- **Target**: Base, section 8 template; FR-005; FR-020; section 9 header
- **Before**: No pagination rule; totals were exact.
- **After**: Pagination gated on step 1.0a; partial rows kept and deduplicated; unknown totals shown as lower bounds and reconciled.
- **Provenance tag**: `[V3:114, V3:299; Change 11]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 12: JSON stdout contract
- **Status**: Applied
- **Source**: V3R3:43, Conv:264; V2:139-141, V2:81; V3:167-177, V3:185
- **Target**: Base, FR-017, NFR-009, section 7 row model, section 9 JSON block; section 5.2
- **Before**: V1 had a smaller key set and no rule on when JSON prints.
- **After**: Success JSON prints only after publication; row key `class` plus `rule`, `evidence`, `notes`, `safe_to_close`; zero counts; ID-only `waiting`. The sentence "Failed publication exits 1 without success JSON or overwriting an earlier observation" is kept, as review 3 found it consistent.
- **Provenance tag**: `[V3R3:43; Change 12]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 13: Collision-safe report path and re-run behaviour
- **Status**: Deviated (applied in narrowed form)
- **Source**: V3:179-187, V3:133-134, V3:187; owner rule in the Step 5 task brief; `refactor-plan-review-3.md` finding P1
- **Target**: Base, FR-017 path clause; section 9 path; new section 5.3
- **Before**: One fixed dated path that a second sweep in the same second would overwrite.
- **After**: Section 5.3 holds the base name, collision suffix, exclusive reservation, no lifecycle change, the footer `Report complete`, and the owner wording only: "Every run that publishes a report writes a new dated file and never reuses or overwrites an earlier path; a run that exits 2 writes nothing." AC: two report-publishing sweeps with the same injected `now` produce two files.
- **Deviation and reason**: The plan's integration point also says "a run that exits 1 or 2 writes no report". Review 3 (P1) found that the exit-1 half has no full source support and conflicts with V3:184, V3:356 and V3:357. Per the task brief, the clause was narrowed to the owner wording and no exit-1 write rule is stated as a requirement. Section 5.3 says so explicitly, and the exit-1 question is recorded as open gap G-1 in section 18, which quotes V3:184, V3:356 and V3:357 verbatim. V1:265's allowlist-miss "no report written" is not carried as a requirement; the section 11 allowlist-miss row states exit 1 and no success JSON only.
- **Provenance tag**: `[Change 13, narrowed to the owner wording; see section 18]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 14: Report section set and order
- **Status**: Applied
- **Source**: V2:207-217, V2:211; V3:297-307; V3:15, V3:197, V3:298
- **Target**: Base, section 9 section list and header
- **Before**: V1's shorter section list, with could-not-determine after working rows.
- **After**: A 12-item section order ending with the footer `Report complete`; source coverage, Shift Brief and "What I could not determine" sections; collection interval in the header; FR-011 points to the section 9 order.
- **Provenance tag**: `[Change 14]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 15: Next inspection on every session row
- **Status**: Applied
- **Source**: V3:303, V3:316
- **Target**: Base, section 9 Sessions section (V1 section 8, V1:228)
- **Before**: The Sessions row had no next action column.
- **After**: A `next inspection` column whose value is an inspection step only, never a stop, retry, release, merge or removal; V1's "no action controls" sentence kept; AC that every cell is non-empty and holds none of the five verbs.
- **Provenance tag**: `[V3:303; Change 15]`, `[V3:316; Change 15]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 16: WC-14 end condition, pin and presentation
- **Status**: Applied
- **Source**: V3:324-325, V3R3:44, Conv:265; V2:225-229
- **Target**: Base, section 10 WC-14 text and pins (V1 section 9, V1:240 and V1:248)
- **Before**: "every Task it created has settled and been admitted", shown as a blockquote, with three pin phrases.
- **After**: "until every Task it created is settled and every result has been inspected and its admission or rejection recorded" plus "It never stops watching on its own."; the rule is a fenced block under its own heading `### WC-14. Coordinator loop`; `RULE_PHRASES["WC-14"]` holds four pins including "it is never posted" and "It never stops watching on its own"; V1's count-free test rename kept; owner approval of the contract text still required.
- **Provenance tag**: `[Change 16]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 17: Periodic sweep duty without a scheduler or cadence
- **Status**: Applied
- **Source**: V3:326-328; V3R3:56; owner order in `coordinator-never-stop-polling.md` line 11
- **Target**: Base, section 10 (V1:240, V1:245); section 16 OQ-7 (V1:314)
- **Before**: A periodic sweep was "allowed by this text but not required" and "a cron sweep stays an operator choice".
- **After**: WC-14 gains "It sweeps on every wake and keeps a periodic sweep scheduled while work remains."; section 10 notes and OQ-7 say "a periodic sweep is a coordinator duty while work remains; Phase 1 sets no cadence and adds no scheduler", with a cross-reference to the INV-011 warning in section 14. V3:405's five-minute cadence was not adopted. A grep for "operator choice" finds no hit.
- **Provenance tag**: `[V3:326-328; Change 17]`, `[V3:326-328; V3R3:56; Change 17]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 18: "Recommends nothing" with the verb list
- **Status**: Applied
- **Source**: V3:335; V1:240, V1:244; V3:105
- **Target**: Base, section 10 closing sentence and note; section 16 OQ-8; section 9 ACs
- **Before**: "The sweep recommends none of these actions."
- **After**: "The sweep recommends nothing: no stop, retry, release, merge or removal." in WC-14 and OQ-8; AC that no rendered fixture report text proposes any of the five actions. A grep for "recommends none" finds no hit.
- **Provenance tag**: `[V3:335; Change 18]`, `[V3:105; Change 18]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 19: Extra WC-14 sentences on duty and heartbeat
- **Status**: Applied
- **Source**: V3:328-329; V2R3:27
- **Target**: Base, section 10 WC-14 text
- **Before**: WC-14 had neither sentence.
- **After**: "Phase 1 adds this duty, not a scheduler." and "A missing heartbeat is absence, never death." appended. The optional lock sentence was not used (the plan permits but does not require it), and V2:228's unscoped observer guarantee is absent.
- **Provenance tag**: `[V3:328-329; Change 19]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 20: PR #422 sequencing
- **Status**: Applied
- **Source**: V3R3:45, Conv:266; V1:313
- **Target**: Base, section 10 sequencing note (V1:248); section 16 OQ-6 (V1:313); section 12 R8 mitigation
- **Before**: "PR #422 lands ... before the contract edit", which allowed WC-14 to slip out of done; R8 said "new-file PR first if needed".
- **After**: V3R3:45's text in section 10 and OQ-6: new package, command, skill and docs first; verify overlap with PR #422 before editing the contract; rebase if #422 merges first; WC-14 and its pins stay deliverables of this PR; the text states sequencing, not #422's status. R8's mitigation now reads "Step 1.16a sequencing as OQ-6 states it (section 16); WC-14 stays a deliverable of this PR".
- **Provenance tag**: `[V3R3:45; Change 20]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (R8 conflict removed, see Contradiction Re-Scan)

### Change 21: Git allowlist of one status template, root by path walk
- **Status**: Applied
- **Source**: V2:200-203; debate resolution X-004
- **Target**: Base, section 8 git allowlist (V1:197-202); FR-004 default root; NFR-003 negative cases; section 2 out-of-scope list
- **Before**: The allowlist included a `rev-parse --show-toplevel` template used to find the root.
- **After**: `ALLOWED_GIT` holds exactly `git --no-optional-locks -C <path> status --porcelain --branch`; the default root is found by walking up with plain reads to the first directory holding `.git` as a file or folder; AC that the walk accepts both and records no `_git` argv; V1:202's unmerged-commits statement kept; negative cases include `rev-parse`, `log`, `branch` and `--version`.
- **Provenance tag**: `[V2:203; Change 21]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 22: One isolated real-git control test
- **Status**: Applied
- **Source**: V2:98, V2:245, V2:100; debate-transcript.md:195, :221
- **Target**: Base, NFR-002, NFR-001, NFR-013, FR-025 acceptance
- **Before**: No real-git test; FR-025's checks stood alone.
- **After**: One marked real-git test in an isolated `tmp_path` repository holds all four real-git assertions (control, positive and negative `check-ignore`, `.dev/sweeps/` write leaves status unchanged); an absent rewrite in the control is reported as inconclusive for that assertion only; FR-025 says its checks run inside this test; NFR-001 and NFR-013 keep subprocess entry points patched to raise everywhere else; the test proves nothing about Orca read verbs.
- **Provenance tag**: `[Change 22]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 23: Read-only snapshot test contents
- **Status**: Applied
- **Source**: V2:97, V2:100
- **Target**: Base, NFR-001 acceptance
- **Before**: The snapshot fields were not named.
- **After**: V1's isolated `HOME`, `XDG_STATE_HOME` and "exactly one added file" kept; the snapshot is (path, size, mtime_ns, sha256) for every file under the root, `HOME` and the XDG dirs, including a fixture `~/.claude/`.
- **Provenance tag**: `[Change 23]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 24: Budget with per-call remaining time and byte limits
- **Status**: Applied
- **Source**: V3:124-125, V3:137
- **Target**: Base, FR-020; section 7 Budget
- **Before**: Fixed 10 s per call with no byte limits.
- **After**: V1's injected `Budget` (50 / 10 s / 90 s) kept; each call's timeout is the lesser of 10 s and the remaining total; byte limits 1 MiB, 256 KiB and 8 MiB marked "proposed; rationale required before release"; a read that hits a limit marks the source unscanned with a reason.
- **Provenance tag**: `[Change 24]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 25: `sanitize()` adds HTML neutralizing
- **Status**: Applied
- **Source**: V3:317-318
- **Target**: Base, FR-016
- **Before**: V1's FR-016 text had no HTML neutralizing rule.
- **After**: V1's text kept, plus "and neutralizes Markdown HTML so no untrusted text becomes an active tag or link."; `<script>` and a Markdown link added to the injection fixture.
- **Provenance tag**: `[Change 25]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 26: `--output` validation through symlinks and without overlap
- **Status**: Applied
- **Source**: V3:156-157
- **Target**: Base, FR-004
- **Before**: FR-004 had no symlink or overlap rule.
- **After**: The check uses the resolved path and forbids overlap with any input package or transcript directory; ACs for an escaping symlinked `--output` and for `--output` equal to a package directory, both exit 2 and write nothing.
- **Provenance tag**: `[Change 26]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 27: Disk discovery scope and symlink checks
- **Status**: Applied
- **Source**: V2:64, V2:247; V3:288-292
- **Target**: Base, section 8 disk readers (V1:204); section 11 symlink-escape row
- **Before**: The read targets had no symlink rule.
- **After**: Fixed patterns only, never a recursive walk; every resolved path checked with `resolve()` to stay inside its root; an escaping symlink is rejected and reported; ccsession files read directly, never through `ccsession --list`; the F9 symlink-escape fixture is an AC.
- **Provenance tag**: `[Change 27]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 28: Forbidden-verb test adds a negative `worker-read` case
- **Status**: Applied
- **Source**: V2:99
- **Target**: Base, FR-021 acceptance
- **Before**: Static forbidden-list test only.
- **After**: V1's static test over `ALLOWED_ORCA` kept, plus "Negative test: a `worker-read` argv passed to `_orca` raises before any subprocess starts."
- **Provenance tag**: `[V2:99; Change 28]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 29: Failure-mode table as the union, with a test column
- **Status**: Applied
- **Source**: V2:237-247; V3:347-358
- **Target**: Base, section 11 table (V1 section 10, V1:254-267)
- **Before**: Twelve rows in Mode / Detection / Behaviour / Exit columns, with no test column.
- **After**: Columns Mode / Detection / Behaviour / Exit / Test. V1's rows as amended by Changes 3, 4, 7 and 9, plus V2's rows not already present (including symlink escape, F9) and V3's rows: input changed during reading, duplicate Dispatch, process killed, remote host. Also present: empty `run-current` body (FR-026 test 5) and `call_failed`. V2's "git too old" row not added. Every row names its test.
- **Provenance tag**: `<!-- Source: Base (original, modified) per Changes 3, 4, 7, 9, 13, 29 -->` and per-row tags
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 30: Package states block removal, including archive-blocked
- **Status**: Applied
- **Source**: V2:160-168, V2:168
- **Target**: Base, section 7 package-state table (V1:164); FR-013
- **Before**: `archive-blocked` was "no by itself" for removal and was not in FR-013's blocking list.
- **After**: The archive-blocked row says "yes, printed in Package state column"; FR-013 lists archive-blocked with a fixture. V1's six states including `unknown` kept; V1:167 unchanged; `unknown` not added to FR-013.
- **Provenance tag**: `[V2:160-168; Change 30]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 31: Partial contracts stay usable-not-yet-judged; finished never means admitted
- **Status**: Applied
- **Source**: V3:228-229
- **Target**: Base, section 7 rule 6 (V1:152)
- **Before**: Rule 6 had the "partial: usable not yet judged" note only.
- **After**: The note kept and "Finished never means admitted." appended; AC that a finished row's JSON and report text never say admitted or accepted.
- **Provenance tag**: `[V3:228-229; Change 31]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 32: "Ownership review", never "foreign"
- **Status**: Applied
- **Source**: V3:226, V3:301
- **Target**: Base, section 7 rule 4 (V1:150); section 8 task-list row; section 9 report section 4
- **Before**: The ready Task row carried no review label.
- **After**: "a ready Task (creator: could not determine), labelled for ownership review". A grep for "foreign" finds no hit.
- **Provenance tag**: `[V3:226; Change 32]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 33: Person-started readability and activity-window exemptions
- **Status**: Applied
- **Source**: V3:93, V3:234-237
- **Target**: Base, FR-010; section 7
- **Before**: No readability rule and no exemptions from the activity window.
- **After**: A transcript must be readable to count; an unknown timestamp is never idle; open Tasks, explicit waits and unread-report candidates are exempt from the activity window and never go to Historical; one fixture per exemption.
- **Provenance tag**: `[Change 33]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 34: Rollback keeps the ignore line and never removes `.dev/tasks/`
- **Status**: Applied
- **Source**: V3:425-431, V3:427
- **Target**: Base, section 17 rollback (V1 section 14, V1:330)
- **Before**: V1's rollback rows with no ordering rule for the ignore line and no `.dev/tasks/` row.
- **After**: V1's rows kept verbatim; the ignore line is reverted only after deciding where existing reports go; a row saying rollback never removes `.dev/tasks/` or any file in it.
- **Provenance tag**: `[V3:427; Change 34]`, `[Change 34]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 35: `.gitignore` check in both directions and the self-observation risk
- **Status**: Applied
- **Source**: V2:93; V2:262, V2:265
- **Target**: Base, FR-025 acceptance; section 12 risk table
- **Before**: Positive `.dev/sweeps/` check only; no self-observation risk.
- **After**: FR-025's AC adds `git check-ignore .dev/tasks/to-do/x.md` fails, inside the one real-git test of Change 22. The self-observation risk is added as R10 (the plan calls it R8; renumbered, see New IDs).
- **Provenance tag**: `[V2:93; Change 35]`, `[V2:262, V2:265; Change 35]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 36: Risk table gains impact
- **Status**: Applied
- **Source**: V2:253-263
- **Target**: Base, section 12 risk table (V1 section 11)
- **Before**: A Likelihood column only.
- **After**: A "Likelihood / impact" column; every risk has an impact rating; V1's rows and mitigations kept, R3 with Change 7's scoped text, R8's mitigation aligned to Change 20.
- **Provenance tag**: `[Change 36]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 37: GQ and open-question table layouts
- **Status**: Applied
- **Source**: V2:271-285, V2:289-298
- **Target**: Base, section 15 GQ table (V1 section 12); section 16 open questions (V1 section 13)
- **Before**: The GQ table had no root cause; open questions had no IDs.
- **After**: The GQ table keeps V1's rows and "Where" column and adds a "Root cause" column; open questions carry IDs OQ-1 to OQ-9 with V1's rows and answers, the PR #422 row replaced by Change 20 and the cron row by Change 17.
- **Provenance tag**: `[Change 37]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 38: Evidence provenance statement
- **Status**: Applied
- **Source**: V2:9
- **Target**: Base, header (V1:12), merged line 32
- **Before**: V1:12 did not name the Round 3 files or a rule for quoting the git version.
- **After**: The debate's Round 3 files are named as additional sources by absolute path, and any quoted host git version must be recorded with the date it was checked. V2's quoted version number was not copied, as it was not re-checked.
- **Provenance tag**: `[V2:9; Change 38]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 39: Separate verification checklist
- **Status**: Applied
- **Source**: V3:414-423
- **Target**: Base, new section 17.1
- **Before**: Section did not exist.
- **After**: A checklist by requirement ID of every AC (FR, NFR, failure-mode tests) plus the NFR-012 repo gates. V3:421's live disposable-Run check left out. INV-005 owner sign-off listed as a release precondition that is not a test.
- **Provenance tag**: `[Change 39]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 40: Section order and renumbering
- **Status**: Applied
- **Source**: V3:148; V1 section order
- **Target**: Base, whole document
- **Before**: V1's 14 numbered sections.
- **After**: V1's sections kept in order with new section 5 (CLI contract and re-run idempotency, 5.1 to 5.3) after section 4, new sections 13 (accepted risks) and 14 (open warnings) after Risks, 17.1 (checklist) and 18 (open gaps). FR-017 and FR-018 cross-reference section 5. Every internal section reference was updated (see New IDs and renumbering).
- **Provenance tag**: `<!-- Source: ... inserted per Changes ... and 40 -->` on new sections
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 41: Read only the needed `worker-show` fields
- **Status**: Applied
- **Source**: V2:63
- **Target**: Base, section 7 data model (merged line 230)
- **Before**: No statement on unread fields.
- **After**: "The parser reads only the `worker-show` fields this model needs and ignores the others; an unknown field is not an error (section 11, unknown schema field row)."
- **Provenance tag**: `[V2:63; Change 41]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 42: Expand GQ, WC and other short forms on first use
- **Status**: Applied
- **Source**: None in the variants; base weakness W-9
- **Target**: Base, header terms list (merged lines 34 to 42)
- **Before**: Short forms were not expanded.
- **After**: A terms list: GQ, WC, REPORT and GAPS as V1:12 defines them, and Run, Task and Dispatch as Orca terms, the last marked UNVERIFIED because no source read here defines them.
- **Provenance tag**: `**Terms.** [Change 42]`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

## New IDs and renumbering
New IDs:
- FR-026: the four-class Orca result classifier (Change 4), the next free V1 FR ID.
- R10: the self-observation risk (Change 35). The plan names it "R8", taken from V2:262, but V1 already uses R1 to R9, so it takes the next free V1 risk ID.
- No new NFR; NFR-014 is not used.

Section mapping:

| V1 section | Merged section |
|------------|----------------|
| 1 to 4 | 1 to 4 |
| (new) | 5 CLI contract and re-run idempotency, with 5.1 to 5.3 |
| 5 to 11 | 6 to 12 |
| (new) | 13 Accepted risks needing owner sign-off |
| (new) | 14 Open warnings |
| 12, 13, 14 | 15, 16, 17 |
| (new) | 17.1 Verification checklist |
| (new) | 18 Open gaps |

Cross-references updated:
- R8 points to section 16 (was section 13).
- The GQ table "Where" column: section 6 becomes 7, section 7 becomes 8, section 14 becomes 17.
- OQ-3 reads "The section 10 text".
- FR-023 points to section 10.
- FR-017 and FR-018 point to section 5.

## Executor choices
Choices the plan left to the executor, or that the task brief fixed:
1. Change 13 narrowed to the owner wording, with the exit-1 question carried as G-1 (the only deviation).
2. Section 9 header-line wording for the coverage lines added by Changes 7, 8 and 9.
3. The per-call timeout (Change 24) is placed in the `subprocess.run` call of each seam.
4. Rule 8 also covers `person_started` None, so None never reaches idle or Historical (Change 5).
5. Change 12's sentence "Failed publication exits 1 without success JSON or overwriting an earlier observation" kept, as review 3 found it consistent with its sources.
6. WC-14 keeps V1's last sentence ("The coordinator decides and performs any action under those rules."); the optional lock sentence of Change 19 is not used; Change 17's sentence is used verbatim.
7. The self-observation risk is numbered R10, not R8.
8. Impact ratings for Change 36: R1 high, R2 high, R3 high, R4 medium, R5 high, R6 medium, R7 high, R8 medium, R9 low, R10 low.
9. The section 11 allowlist-miss row states exit 1 and no success JSON only, with no "no report written" clause, so no exit-1 write rule is a requirement.
10. R8's mitigation aligned to Change 20, replacing V1's "new-file PR first if needed".
11. The GQ-108 summary row ("Person-started = transcript joined to no Orca row") kept as a summary that points to FR-010, per Change 37.

## Review findings not applied
Review reports (all in `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/adversarial/adversarial/`):
- `refactor-plan-review.md`
- `refactor-plan-review-2.md`
- `refactor-plan-review-3.md`

Carried into the merged spec:
- Review 3 P1 (blocking): handled by the Change 13 deviation and recorded as open gap G-1 in section 18. Not fixed in the plan; no further fix pass and no fourth review were run.
- Review 3 p1 (minor): recorded as a note under INV-017 in section 14. No stderr or requirement change was made for it.

Not applied: the other minor notes of reviews 1 to 3 (including M1 to M12 and m1 to m8). They stay in the review reports.

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. One H1 title; H2 sections 1 to 18; H3 subsections 5.1 to 5.3, 17.1, the WC-14 rule heading, the INV entries and G-1 to G-3. No level is skipped.
- Section ordering: PASS. V1's order is kept; new sections sit where Change 40 places them; numbers run 1 to 18 without gaps.
- Document flow: PASS. Each numbered heading has a `Provenance:` line (19 lines for 19 numbered headings). No `STUB`, `TODO` or `TBD` text remains. No em dash appears.

### Internal References
- Section references: all "section N" references in the body were checked against the merged numbering after Change 40, including the GQ "Where" column, OQ-3, FR-017, FR-018, FR-023, R8 and the section 11 rows that cite section 18. All resolved.
- Change tags: every change from 1 to 42 has at least one provenance tag in the merged spec.
- Seed path: the absolute seed-brief path is used; `../../seed-brief` has 0 hits.
- Result: references resolved, 0 broken. PASS.

### Contradiction Re-Scan
Greps run on the merged spec and their results:
- "exit 0": only the FR-001 `CliRunner` AC, the FR-002 and FR-019 tests that publish with a binding, and section 5.1's definition. No text lets a run without a binding exit 0.
- "every run": only section 5.3 and G-1, both the owner wording.
- "No Run bound": only the section 11 row label; the other hits are the `no Run bound:` message.
- "never bare", "foreign", "cls": 0 hits.
- "the sweep never takes", "operator choice", "recommends none", "Accepted risks)": 0 hits.
- `GIT_OPTIONAL_LOCKS`: only NFR-002, the section 8 `_git` lines and the GQ-103(1) row; none in section 13.

Found and fixed during the merge: V1's R8 mitigation ("new-file PR first if needed") contradicted Change 20; it now follows the Change 20 sequencing.

Noted, not a contradiction: the GQ-108 summary row simplifies the person-started rule but points to FR-010, which holds the tri-state rule.

Open, not a contradiction in the spec: the exit-1 file question is stated as gap G-1 and no requirement takes a side.

Result: 0 new contradictions. PASS.

## Summary
- Planned: 42
- Applied: 42 (41 as planned, 1 deviated: Change 13, narrowed)
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
- Gate status: BLOCKED_BY_INVARIANTS until the INV-005 owner sign-off is recorded (section 13); open gaps G-1 to G-3 in section 18.
