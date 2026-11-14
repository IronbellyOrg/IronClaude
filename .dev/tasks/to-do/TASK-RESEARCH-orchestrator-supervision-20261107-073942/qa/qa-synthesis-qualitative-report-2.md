# QA Report — Synthesis Coherence Review (report-qualitative, Partition 2 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339), synthesis coherence
**Date:** 2026-11-07
**Phase:** report-qualitative (synthesis gate, Phase 5)
**Fix cycle:** N/A
**Fix authorization:** false (report only; no synthesis file edited)
**Assigned files:** `synthesis/synth-04-options-recommendation.md`, `synthesis/synth-05-implementation-plan.md`, `synthesis/synth-06-questions-evidence.md`

Pre-review sha256 of assigned files (for the no-modification check):

- synth-04 `be5b9116594c463a973aa91ddcc90c98d02b99e47a32d2e7bb08acd5fb07f7e7`
- synth-05 `68b559410c5543566c3f4c892704abea1fa52cdbc93afa362e5233473306186c`
- synth-06 `69103a6c6d82151ddf71d2d30bffb6d24a796013a9be0177ad7632c327382ed4`

[PARTITION NOTE: Cross-file checks limited to assigned subset plus the research files it cites. Full cross-file verification requires merging both partition reports.]

---

## Overall Verdict: FAIL

5 blocking findings (IMPORTANT) and 7 minor notes. The NB-4 allowlist re-check passes.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Problem statement matches findings | PASS | synth-04 answers the question that was asked: how Phase 1 supervises with a read-only, coordinator-only sweep. Constraints K-1 to K-6 trace to research-notes:150-231 and scope-03:99. It does not drift into Phase 2-4 work. |
| 2 | Current state analysis is current | PASS (note) | Spot-checked against current code. Lazy subcommand registration is at `src/superclaude/cli/main.py:553-561`. The lazy `__getattr__` in the `recommend` package is at `src/superclaude/cli/recommend/__init__.py:12-17`. The never-as-worker list is at `WORKER-CONTRACT.md:23`, pinned at `tests/skills/test_worker_contract.py:245-254`. The sc-crash-recovery `allowed-tools` line is at `SKILL.md:4`. All four match. The one exception is the stale count text (I-1). |
| 3 | Options are genuinely distinct | PASS | The four options differ on where the classifier lives, how it is tested and how it is installed. A1 is a CLI plus a command plus a skill. A2 is a skill only. A3 is a skill plus a skill-local stdlib script. A4 extends crash-recovery. A1 versus A3 is the narrowest gap, but synth-04 names a real difference: A1 is installed with the package and pinned by pytest, while A3 runs from `~/.claude/skills/`. |
| 4 | Recommendation follows from analysis | PASS | In synth-04's comparison (lines 176-185), A1 scores best on K-4 (mock-testable) and K-5 (argv allowlist enforced in code). A4 is rejected as code-contradicted because crash-recovery allows `Bash(git stash *)` (`sc-crash-recovery/SKILL.md:4`). The recommendation at line 191 matches research-notes:227. |
| 5 | Implementation plan is actionable | PASS | synth-05 steps 1.1-1.24 name the files, tests and pins. The step 1.3 precedence matches research-notes Section C, and step 1.6 follows the `main.add_command` pattern verified in check 2. Phase 1 stays read-only and coordinator-only, and its only write is `--output`. Phases 2-4 are recorded in one line each (lines 116-124). |
| 6 | Gaps are honest | FAIL | I-4: synth-05 settles the owner-decision rows GQ-10, GQ-11 and GQ-35 without saying so and leaves them out of OQ-11. synth-06 rows 8, 9 and 30 still list them as owner decisions. |
| 7 | External research is relevant | PASS | synth-05 section 8.3 (lines 230-249) ties each web-01 and web-02 row to a plan step. web-02 was treated as a normal research source, as instructed. The rejected and excluded rows are named (lines 248-249). |
| 8 | Scale claims are substantiated | PASS | The paging claims are bounded: worker-list returns 100 rows newest first, is paged on `page.nextCursor`, and costs at worst ceil(N/100) + N calls (synth-05:62). There is no unbounded scale claim. |
| 9 | Risk assessment is complete | FAIL | I-2: the plan (synth-04:60, synth-05:62) and synth-06 row 17 disagree on whether `--include-remote` is on by default. Its runtime cost (GQ-22) is [UNVERIFIED], so that risk has no consistent handling. |
| 10 | Evidence trail is complete | FAIL | I-5: synth-06 row 33 merges GQ-38 with GQ-48 and gives GQ-38 the GQ-48 resolution, so GQ-38's trail ends at the wrong answer. |
| 11 | No circular reasoning | PASS (note) | synth-04 and synth-05 cite research and qa files (scope-01 to scope-04, 05, 06, research-notes, qa-nb4-fix-log), not themselves. One exception: synth-05 X-6 cites synth-02 C2 for a count, which is synthesis citing synthesis and also points at the wrong item (I-1). |
| 12 | Conclusion is proportionate | FAIL | I-1 and I-3. Two resolution cells are false or restate the defect. synth-06 row 58 (GQ-84) gives as its resolution the same ordering the QA finding flagged as the problem. |

## Summary

- Checks passed: 8 of 12
- Checks failed: 4
- Critical issues: 0
- Important (blocking) issues: 5
- Minor issues (notes): 7
- Issues fixed in place: 0 (fix authorization false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | IMPORTANT | synth-04:220 (X-6); synth-05:260 (X-6) | synth-04 X-6 says `gaps-and-questions.md:125` still reads "Open: 76. Resolved: 24" with GQ-03 open, and synth-05 X-6 calls the count stale. Line 125 now reads "Open: 75. Resolved: 25 (GQ-03, ...)" and "Open blocking QA finding: none". synth-06:13 already uses 75/25, so the three files contradict each other. synth-05 X-6 also maps the count to "synth-02 C2", which is the test-file length item, not the gap count. | Remove X-6 from both tables, or restate it as "Resolved by the NB-4 fix pass (`qa/qa-nb4-fix-log.md`); the count is now 75/25". Drop the C2 mapping from synth-05 X-6. |
| I-2 | IMPORTANT | synth-06:45 (row 17, GQ-22) versus synth-04:60 and synth-05:62 (step 1.4) | synth-06 resolves GQ-22 as "Measure once; keep it off by default". The plan's default argv is `worker-list --run <id> --include-remote --json` (synth-05:62, synth-04:60), so the flag is on by default. gaps-and-questions:45 notes that remote rows read `unverifiable` without the flag, which is the plan's reason for turning it on. | Make the two agree. To match the plan, change synth-06 row 17 to: "On by default, because remote rows read unverifiable without it. Measure the cost once in Phase 1 and record it under Open Questions." |
| I-3 | IMPORTANT | synth-06:86 (row 58, GQ-84) | The resolution reads "Apply rule 2 before rule 7". That is the ordering QA finding M1 flagged as the problem. gaps-and-questions:107 says the plan must state that rule 2 needs the transcript read, and that an exited row with no `worker_done` and an unreadable transcript gives "could not determine". synth-05:161 states that correct resolution (steps 1.3 and 1.9). | Replace the row 58 resolution with: "Rule 2 (stalled, proved) needs the transcript read. An exited row with no `worker_done` and an unreadable transcript is 'could not determine' (synth-05 steps 1.3 and 1.9). Not a WC-10 break." |
| I-4 | IMPORTANT | synth-05:138, :158, :159 and :223 (OQ-11) versus synth-06:36, :37, :58 (rows 8, 9, 30) | gaps-and-questions lines 33-34 mark GQ-10 and GQ-11 "open (owner decision)", and line 158 lists GQ-35 under the still-open AMBIGUITY 9. synth-05 settles all three in the plan: a dated `--output` file under `.dev/`, a new WC-14, and a pin to `495eb96d`. But OQ-11 lists only G6, GQ-61 and GQ-63 as owner decisions, while synth-06 still lists all three as owner decisions. A reader of synth-05 alone would think the owner has nothing to decide on report location, rule ID or pinning. | Add GQ-10, GQ-11 and GQ-35 to synth-05 OQ-11 as "plan default, owner to confirm". Point synth-06 rows 8, 9 and 30 at those defaults, or mark the plan choices provisional in synth-05 section 8.1. |
| I-5 | IMPORTANT | synth-06:61 (row 33) | The row merges two different limits. GQ-38 is about worker-list `page.hasMore` past 100 rows, which the sweep pages through on `page.nextCursor` (gaps-and-questions:61). GQ-48 is about the message listing, which caps at 100 with no cursor (gaps-and-questions:71). The row's single resolution, "could not determine: message listing truncated at 100", is GQ-48's answer and is wrong for GQ-38. synth-05:151 and :156 keep the two separate. | Split row 33 into two rows. GQ-38: "Page on `page.nextCursor`; if `hasMore` past 100 rows stays unproven, report could not determine." GQ-48: the truncated-at-100 string. |

### Minor notes (non-blocking)

| # | Severity | Location | Note |
|---|----------|----------|------|
| M-1 | MINOR | synth-04:3, synth-06:3 | The class list omits `fenced`. The canonical list (research-notes:188, synth-05 step 1.2) includes it. |
| M-2 | MINOR | synth-06:49 (row 21) | It pins the `Bash(superclaude sweep:*)` form, while the GQ-26 source uses the space form `Bash(superclaude sweep *)`. |
| M-3 | MINOR | synth-06 rows 18, 27, 28, 50, 51 (lines 46, 55, 56, 78, 79) | These lag the plan's decisions. Row 18 says "pick one precedent", which the plan has already done. Row 27 says "window and Run ids", but the plan's scope line is the root (GQ-32). Row 28 says "print the omission count", but the plan lists everything (GQ-33). Row 50 says "leaning A1", but A1 is recommended. Row 51 states 6 h as settled, but synth-05 OQ-11 keeps it as an owner decision. Wording alignment only. |
| M-4 | MINOR | synth-06:221 | It says synth-05 is "planned; not yet written". synth-05 now exists. |
| M-5 | MINOR | synth-06:91 (row 63) | "Batch where the policy allows" misapplies the Bash batching policy. The N `worker-show` calls are subprocess calls made by the CLI, not agent Bash round trips, so the policy does not govern them. |
| M-6 | MINOR | synth-05:255 (X-1) | "runs `git stash` commands beyond `list`" overstates the case. The skill allows `Bash(git stash *)` (`sc-crash-recovery/SKILL.md:4`) and says it only proposes commands for the user to run (`SKILL.md:13`). Reword "runs" as "allows". |
| M-7 | MINOR | synth-06:31 (row 3) | It tells WC-14 to cite a private memory note (`coordinator-never-stop-polling.md`). WC-14 ships in the installed contract, where that note does not exist. Cite the owner order by date in prose instead. |

## NB-4 Re-check (executor extra 1)

Result: **PASS**.

- `research/scope-03-cli-patterns.md:99` carries the corrected allowlist. The allowed verbs are worker-list, worker-show, worker-read, `worktree ps` without `--agent-wait`, and the orchestration verbs task-list (`--ready`, `--run`), run-list, run-current and gate-list. Still forbidden: check, `--ack`, `--wait`, `--unread`, `check --format`, reply, ask, send, inbox, `worktree ps --agent-wait`, and any unknown verb. `qa/qa-nb4-fix-log.md` records the three edits.
- synth-04:18 and synth-06:11 carry the NB-4 note. synth-05:62 cites "`scope-03:99` after NB-4", with gate-list allowed and inbox forbidden. synth-06 row 29 says "`gate-list` is now allowed (NB-4)", and row 39 says "`inbox` stays forbidden".
- A grep of all three files for the old allowlist (gate-list or task-list listed as forbidden, or inbox allowed) found nothing.

## web-02 handling (executor extra 2)

`research/web-02-static-status-report-conventions.md` was treated as a normal research source. synth-05 8.3 rows 236 and 242-248 use it with plan-step mapping, and none was flagged as out of scope.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was in the spawn prompt, so there was nothing to rely on. Structural items such as section numbering and file existence were not the focus; the fallback was standalone checks on the cited lines.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Gap count currency: Grep of `gaps-and-questions.md` shows line 125 at "Open: 75. Resolved: 25". synth-04:220 and synth-05:260 claim it is still stale (I-1).
- `--include-remote` default: Grep shows synth-05:62 and synth-04:60 put it in the default argv, while synth-06:45 says off by default (I-2).
- GQ-84 resolution: gaps-and-questions:107 compared with synth-06:86 and synth-05:161 (I-3).
- Owner-decision rows: gaps-and-questions:33-34 and :158 compared with synth-05:138, :158, :159, :223 and synth-06:36, :37, :58 (I-4).
- GQ-38 versus GQ-48: gaps-and-questions:61 and :71 compared with synth-06:61 (I-5).
- Code citations: `cli/main.py:553-561`, `cli/recommend/__init__.py:12-17`, `WORKER-CONTRACT.md:23`, `test_worker_contract.py:245-254`, `sc-crash-recovery/SKILL.md:1-15`, `docs/designs/sc-issue-command.md:384` and `tests/recommend/test_routing_refresh.py:33` were all Read; each matches the synthesis claim that cites it.

Answers:
1. Claims independently verified against source: 22 (7 code citations, 10 gaps-and-questions rows, scope-03:99, research-notes Section C, the A1-A4 table, the canonical class list, and the NB-4 fix log).
2. Files read: the three synthesis files in full (synth-05 in two ranges), `gaps-and-questions.md` (grep), `research/research-notes.md:150-231`, `research/scope-03-cli-patterns.md:99`, `qa/qa-nb4-fix-log.md`, and the seven code and doc files listed in (b).
3. Not applicable: the review found 5 blocking issues.
4. No web research was performed; Tavily was not needed.

## Confidence

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement (this report and the pre-compaction reading):** Read: 22 | Grep: 9 | Glob: 0 | Bash: 2 (sha256sum)
- Tool engagement is above the 12-item checklist minimum.

## Recommendations

- Fix I-1 to I-5 in the synthesis files, then re-run this partition's review (fix cycle 1).
- Fold M-1 to M-7 into the same edit pass if convenient. They do not block.
- At assembly, make synth-06 section 9.1 the single place each GQ row's resolution is stated, and have synth-05 8.1 point to it rather than restate it. Most of the five blockers are drift between those two tables.

## QA Complete

## Verdict: FAIL

