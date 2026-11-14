# A.10 Task-File Validation: Fix Log (fix round 1)

**Task file:** `TASK-RESEARCH-review-panel-unify-20261113-155942.md`
**Findings source:** `qa/qa-task-validation-consolidated.md` (4 blocking: B-1, S-1, S-2, M-5 promoted)
**Date:** 2026-11-13
**Scope held:** report-only task; no /sc:workflow, no roadmap; E2 stays at commit 4a22d74213f93837d00c2c314075dd967b9a98e3; frontmatter `reflect_post_mode: skill` unchanged. Minor notes M-1..M-4, M-6..M-9 and structure minors not fixed.

## Fix entries

### S-1 (IMPORTANT): Section 4 gaps not forced into Section 8 plan

- **Items edited:** Step 5.1 synth-02 item (line 280); Step 5.4 synth-06 item (line 302).
- **synth-02 changes:** (1) the Gap Analysis table spec now requires every row's Notes cell to begin with `Track: M<n>` or `Track: none (drop: <reason>)` and defines the fixed MIGRATION-TRACK LABELS (M1 shared-core contract; M2 reflect onto core; M3 tasklist and spec consumers; M4 future consumers (PR review, rf-qa replacement)); (2) the C8 unwired-capability instruction no longer says "link it to the Section 8 migration step that wires it" (a step that did not exist yet) but "tag it with the migration track (M1-M4) whose Section 8 steps will wire it", noting synth-06 must cover every Critical/Important gap; (3) the ensuring clause now checks the track tag on every row. Table columns unchanged (Gap / Current State / Target State / Severity / Notes), so the synthesis-gate column check still holds.
- **synth-06 changes:** (1) inputs now include `${TASK_DIR}synthesis/synth-02-target-gaps.md` and `${TASK_DIR}gaps-and-questions.md` (both exist before Step 5.4: synth-02 is written in Step 5.1, the gaps log in earlier phases); (2) the four old track headings (M1 reflect shadow / M2 tasklist / M3 spec-panel / M4 hooks) replaced by the same fixed labels, defined with byte-identical text to synth-02 (Grep count of the full label sentence = 2); (3) step tables gain a `Closes gaps` column; (4) new `#### Gap coverage` table at the end of 8.2 with the rule "every CRITICAL or IMPORTANT gap in Section 4 maps to at least one Section 8 step or an explicit drop with a reason"; (5) the ensuring clause checks the labels and the coverage table.
- **Not changed:** the owner-required ORDER paragraph (line 274); Step 5.4 still runs after synth-04/05, and synth-02 already exists by then. Report-only scope kept (no dates, sprints or workflow plan added).

### B-1 (IMPORTANT): >3000-line partition rule not carried by the lens items

- **Items edited:** the 13 lens items in Steps 6.2-6.4 (lines 354, 356, 358, 360, 362, 366, 368, 370, 372, 374, 378, 380, 382); the Step 6.5 consolidation item (line 386).
- **Lens items:** each now opens with `PARTITION CHECK FIRST:` stating: if the ### Phase Gate Findings section records the >3000-line partition rule from the Step 6.1 measure item (`wc -l`), run the lens as two instances in the same parallel message with `Assigned sections: 1-5` (output `qa/qa-lens-<lens>-a.md`) and `Assigned sections: 6-10` (output `qa/qa-lens-<lens>-b.md`), tick only when both exist; otherwise run one instance as written. Each item names its own full `-a`/`-b` paths; Grep confirmed each `-a`/`-b` stem matches that item's existing single output name (13 of 13), including `implementation-concreteness` for the implementation-plan-concreteness lens.
- **Step 6.5 consolidation item:** the vague "plus `-a`/`-b` instances if the report was partitioned" is replaced by an explicit rule: when partitioned, read both instance reports of all 13 lenses (26 files), treat the pair as the lens report (lens FAIL if either instance fails), and do not count the absent single file as missing; the missing-report rule now also covers a missing instance report.
- **Not changed:** item 348 (Step 6.1 measure) already records the rule correctly.

### S-2 (IMPORTANT): late report change skipped the fidelity and anti-omission gates

- **Items edited:** Step 6.8 final-validation item (line 440); Step 7.1 confirm-final-state item (line 446).
- **Step 6.8:** a `no` on a report-content row (missing section or missing required content (a)-(e)) still routes back to Step 6.5, and the item now says that after that fix the following re-run in this order against the changed report: (1) Step 6.6 verification items plus the 6.6 decision item; (2) the whole Step 6.7 fidelity gate; (3) the whole Step 6.7b anti-omission gate; (4) Step 6.8 again (new checklist, new hash). Each gate runs as its next cycle within its own 2-fix-cycle cap and halt rules. If any cap is already used up, any gate HALTs, or a gate-PASS row is `no`, the task sets `status` to "🔴 Blocked" with `blocker_reason`, records the open blocking findings, escalates to the user and stops.
- **Step 7.1:** on a hash mismatch, the old "re-run the two Step 6.6 verification items" is replaced by the same 6.6, 6.7, 6.7b, 6.8 re-run sequence, followed by a repeat of the hash comparison, with the same cap and HALT/escalate rule.

### M-5 (promoted to IMPORTANT): decision items read only the cycle-1 verification files

- **Items edited:** the Step 6.6 decision item (line 396), the Step 6.7 fidelity decision item (line 416), and the Step 6.7b anti-omission decision item (line 436).
- **Change:** each now reads "the verification files of the CURRENT cycle only" and names both sets: cycle 1 `qa-fix-verification.md` / `qa-fix-verification-qualitative.md` (likewise `qa-fidelity-verification-{structural,content}.md` and `qa-anti-omission-verification-{structural,content}.md`), and cycle 2 the same names with `-cycle2` before `.md`. A cycle-1 verdict must never be taken as the cycle-2 verdict, and the previous cycle's files are read only for the regression check. The cycle-2 names were checked against the verifier items' own output rules (lines 392, 394, 414, 434: "on cycle 2 use/add `-cycle2` before `.md`"), and they match.
- **Checked, not changed:** the Phase 3 (line 246) and Phase 5 (line 338) decision items say "both verification reports" and do not hard-code cycle-1 names, so they do not have this defect.

## Post-fix checks

- `^- \[ \]` count still 104 (no items added or removed; all fixes are in-item edits).
- Frontmatter `reflect_post_mode: skill` unchanged (line 28).
- Every E2 commit reference is still 4a22d74213f93837d00c2c314075dd967b9a98e3 (or its prefix 4a22d742); no other commit added.
- No /sc:workflow or roadmap instruction added; report-only scope kept.
- Grep counts: migration-track label sentence 2 (synth-02 and synth-06, identical); `PARTITION CHECK FIRST` 13; `verification files of the CURRENT cycle only` 3; `re-run IN THIS ORDER` 2.

## Could not fix

- None. All 4 blocking findings (B-1, S-1, S-2, M-5) were applied.
- Minor notes M-1 to M-4, M-6 to M-9 and the structure minors were left alone on purpose (record-only under the review severity rule).
- One limit to note: the S-2 re-runs overwrite the fixed-name fidelity and anti-omission agent reports (`qa-source-fidelity-report-N.md`, `qa-anti-omission-report-N.md`). The history is kept in each gate's consolidated file, which appends a `## Cycle N` section. This is not a blocking defect, and it was not changed so the scope stays narrow.

## A.10.25 alignment fixes

Source: `qa-task-validation-consolidated.md` section "A.10.25 research-alignment findings". Files edited: the task file (T) and `research/research-notes.md` (N). No checklist item was added or removed (104 `- [ ]` items before and after).

| ID | Lines edited | Change | Replacements |
|---|---|---|---|
| AL-B1 | T: 118, 167, 182, 184, 186, 188, 190, 192, 194, 196, 198, 200, 202, 204, 224, 240, 372, 406. N: 32 (E2 prefix definition), 131 | `.dev/eval-workspaces/tasklist-review-panel/` became `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` (replace-all). No HANDOFF path used the root form, so none was touched. The two bare `git ls-tree ... tasklist-review-panel/` calls (T:192, T:196) now list the study folder, which is where the packages and samples are. N:57 `E2:../HANDOFF-review-panel-unification.md` now resolves to the correct root file. | T: 30, N: 2 |
| AL-B2 | T: 198 (agent 9, question 7) | `git show master:src/superclaude/cli/review/__init__.py` became `git show origin/master:...`, plus a note that local `master` is stale. This was the only git read of a master ref; other "master" words are prose (for example "E3 ... on master") and were left alone. | T: 1 |
| AL-B3 | T: 122, 182, 200 (4 paths), 372, 408. N: 68, 118, 127 | `src/superclaude/cli/pr_submit/` became `src/superclaude/pr_submit/` (replace-all). Checked with Glob: `src/superclaude/pr_submit/{models,reviewers,fsm,severity_router}.py` exist. | T: 8, N: 3 |
| AL-B4 | T: 202 (agent 11), 284 (synth-04), 298 (synth-05) | Agent 11: added question (8), Tier 2 cost versus worth: E2 ceiling about 2-2.5 of 14 and "sonnet alone most catches per token", 37 of 38 pre runs escalate (MR:142), H-A unmeasured, O-8 rubric-first. Inputs are slice 04 sections 0.1, 2 (F-19) and 4 (O-8), and section 0.1 was added to the item's slice 04 reading list. Synth-04: slice 04 (sections 0.1, 2, 4 and 6 assignment 10) added to its inputs. Conflict `C14 panel size versus cost (panel-size-cost)` added after C13, and the item's own check changed from C01-C13 to C01-C14. Synth-05: slice 04 (sections 0.1, 2 and 4) added to its inputs. Facts checked against `research/scope/04-this-session-artifacts.md` lines 20, 26, 237, 316 and 333. | T: 3 items, 5 edits |

### Post-edit Grep checks

| Check | Task file | research-notes.md |
|---|---|---|
| `cli/pr_submit` | 0 | 0 |
| `git show master:` | 0 | 0 |
| `tasklist-review-panel/` total | 30 | 2 |
| of which `tasklist-review-panel/20261111-a1/` | 30 | 2 |
| of which `tasklist-review-panel/HANDOFF-review-panel-unification.md` | 0 | 0 |
| `20261111-a1/20261111-a1` (double prefix) | 0 | 0 |
| `panel-size-cost` | 2 | n/a |

### Could not fix / not changed

- All four findings were applied.
- Not changed, to keep the scope narrow: the Phase 5 QA lens items (T:308 and T:316) still say "C01-C13 at minimum". That stays true now that C14 exists, but those lenses will not check C14 by name. This is a minor note, not a blocking defect.
- T:194 "C1 and C6 compare against HEAD, not master" is a risk statement, not a git read, so it was left as is.

## A.10.5 qualitative fixes

Source: `qa/qa-qualitative-consolidated.md` (cycle 1: Q-B1..Q-B4 blocking, Q-M1..Q-M4 promoted). Files edited: the task file (T) and `BUILD-REQUEST.md` (BR, Q-B1 command form only). All edits are inside existing items or in the Task Log section; no checklist item was added or removed. Record-only minor notes were not touched.

| ID | Lines edited | Change |
|---|---|---|
| Q-B1 | T:290 (Step 5.2 item 1, ENTRY TEMPLATE step 3); BR:42 | `--compare <dir>/proposal-a.md <dir>/proposal-b.md` became `--compare <dir>/proposal-a.md,<dir>/proposal-b.md` (one comma, no space), matching `~/.claude/commands/sc/adversarial.md:39` ("Comma-separated file paths (2-10 existing files)"). `--depth`, `--focus`, `--output` unchanged. BR:42 placeholder form became `--compare <proposal-a path>,<proposal-b path>`. |
| Q-B2 | T:290 (Step 5.2 item 1, two places); T:533-535 (`### Phase 5 Adversarial Sub-Checklist`) | Added `<!-- DYNAMIC CONTENT START: adversarial-debates -->` and `<!-- DYNAMIC CONTENT END: adversarial-debates -->` (marker form from template 02 I6, lines 559-560) inside the sub-checklist section, after its existing explanatory comment (which now says entries go only between the markers). Step 5.2 item 1 now adds the per-conflict `- [ ]` entries, and the alternative `No adversarial run needed` line, ONLY between those markers and keeps both markers unchanged, citing the /task executor rule (task SKILL.md:119, :157, :161). The Task Log location the owner asked for is kept. |
| Q-B3 | T:294 (Step 5.2 verify item) | The check now searches synth-04 for the FIXED STRING `Adversarial result:** pending` (`grep -cF 'Adversarial result:** pending' <file>`, or the Grep tool with the escaped pattern `Adversarial result:\*\* pending`) and states the expected count 0. Tested on the task file, which holds the marker 3 times: `grep -cF` = 3 and the escaped pattern = 3, so the check can now fail. |
| Q-B4 | T:446 (Step 7.1) | On a hash mismatch the item now routes through Step 6.5 first: step (0) appends a `## Cycle N` section to `qa/qa-consolidated-findings-phase6.md` with one BLOCKING row `report changed after final validation` (IMPORTANT, old hash -> new hash, source Step 7.1, fix: re-check every section against its cited evidence, fix or mark [UNVERIFIED]) and `\|F_n\|` = 1, then runs the Step 6.5 fix item (single rf-qa fix agent), so the two Step 6.6 verifiers no longer skip; then (1) 6.6 verifiers + decision, (2) 6.7, (3) 6.7b, (4) 6.8, then the hash comparison again, each within its own cap and halt rules (existing text kept). It states the 6.5 consolidation item is not re-run on this path because the lens reports did not change. |
| Q-M1 | T:308, T:316 | "C01-C13" became "C01-C14" (2 replacements). `grep -cF 'C01-C13'` = 0; `C01-C14` = 3 (284, 308, 316). |
| Q-M2 | T:194 (agent 7), T:202 (agent 11), T:226 (Phase 3 evidence partition 2) | Each run of `uv run python scripts/reflect_shadow_exit.py` now says exit code 1 is expected (Stage 2 exit criteria not met; at task creation OVERALL FAIL, 13 of 20 shadow runs) and the agent records the output and exit code instead of treating it as a tool failure. Re-run today from the repository root: `OVERALL: FAIL (shadow runs 13 of 20)`, exit 1. |
| Q-M3 | T:167 (Phase 1, unchanged); 70 agent prompts: the 12 Phase 2 research prompts (182-204) and the 58 prompts with `Task directory:` (216-244, 278-336, 346-394, 402-414, 432-434) | Phase 1 Step 1.2 already states the absolute root (T:167), so it was not duplicated. Every agent prompt that runs commands (all Phase 2 research agents run `git show`/`uv run`; the gate, fix, verifier, assembler, lens and fidelity prompts run Grep/Bash checks) now opens its context with `Repository root: \`/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel\` (run every command and resolve every relative path from there).` (2 replace-all edits: 12 + 58 = 70). Not added to the 4 web agents (260-266) or the 4 anti-omission agents (422-428), which run no repository commands, nor to the ENTRY TEMPLATE proposal agents (read only). |
| Q-M4 | T:454 (Step 7.3) | "no `.claude/` path is staged" became "no repository-root `.claude/` path is staged", with the check `git diff --cached --name-only \| grep '^\.claude/'` printing nothing or only `.claude/settings.json`, and a statement that paths under `.dev/tasks/` (including a task-folder `.claude/agent-memory/` subfolder) are part of the `.dev/tasks` staging and allowed. `git add -f` ban kept. |

### Post-fix checks (A.10.5)

| Check | Result |
|---|---|
| `grep -c '^- \[[ x]\]'` on the task file | 104 (unchanged) |
| `grep -F -- '--compare'` on the task file | 11 hits: 1 is the Step 5.2 debate call with the comma-joined pair `.../<slug>/proposal-a.md,.../<slug>/proposal-b.md`; the other 10 are `/sc:adversarial --compare --merge` prose about the later report merge (no paths). No space-separated proposal pair remains (`proposal-a\.md \.dev` count 0). |
| DYNAMIC CONTENT markers | `<!-- DYNAMIC CONTENT START: adversarial-debates -->` once (line 534) and `<!-- DYNAMIC CONTENT END: adversarial-debates -->` once (line 535), both between `### Phase 5 Adversarial Sub-Checklist` (531) and `### Phase 6 Findings` (537); total `<!-- DYNAMIC CONTENT` count in the file = 2. Step 5.2 names the markers without the `<!--` delimiters, so they are not duplicated. |
| `grep -cF 'C01-C13'` | 0 |
| Step 5.2 completion check | uses fixed-string matching (`grep -cF`) or the escaped Grep pattern, expected count 0; both forms find the 3 markers present in the task file. |
| Scope | `c2ddeb1` 0 hits; `RUN2` 0 hits; E2 references only `4a22d74213f93837d00c2c314075dd967b9a98e3` (97) or its prefix `4a22d742` (5); `reflect_post_mode: skill` unchanged; no `/sc:workflow` or roadmap instruction added. |
| Q-B4 routing | `route through Step 6.5 first` 1 hit, `report changed after final validation` 1 hit (Step 7.1). |
| BR:42 | `--compare <proposal-a path>,<proposal-b path>` |

### Could not fix / not changed (A.10.5)

- All 4 blocking findings and all 4 promoted fixes were applied.
- T:386 (Step 6.5 consolidation item) still says it runs "whenever Step 6.8 or Step 7.1 routed the task back here". Step 7.1 now enters Step 6.5 at the fix item and says why the consolidation item is skipped on that path, so behaviour is defined; the 386 wording was left alone to keep the edit narrow.
- The `sha256sum` commands in Steps 6.8 (T:440) and 7.1 (T:446) are run by the executor, not a subagent, and use paths relative to the root that Phase 1 (T:167) states; "from the repository root" was not added to them (part of M-4's wider suggestion, not of Q-M3).
- Record-only minor notes (tests/cli/reflect count, `_ID_TOKEN` line, "five" vs four at T:246, mid-cycle resume, `[CONTRADICTION:` regex at T:348, web phase gate, >3000-line lens split) were not touched, as instructed.

