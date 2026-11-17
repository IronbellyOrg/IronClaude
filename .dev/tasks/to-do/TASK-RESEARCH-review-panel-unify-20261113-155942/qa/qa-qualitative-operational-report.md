# QA Report — Task File Qualitative Review (Operational Correctness lens)

**Topic:** TASK-RESEARCH-review-panel-unify-20261113-155942 (E1/E2/E3 review-panel unification research)
**Date:** 2026-11-13
**Phase:** task-qualitative
**Lens:** operational-correctness
**Fix cycle:** N/A (fix_authorization: false — report only)
**Reviewer:** rf-qa-qualitative

---

## Overall Verdict: FAIL

Three blocking operational defects, all in Phase 5 Step 5.2 (the adversarial step), each with a small fix. Everything else checked (paths, refs, commands, producer and consumer file names, gate strings, Phase 7 scope) would run as written; nine minor notes are listed.

**Drift baseline (BUILD_REQUEST.GOAL, from spawn prompt and task file line 109):** run a Deep tech-research investigation comparing E1 (reflect Tier 2 panel, branch ironbelly/shadow-runs), E2 (tasklist review-panel study at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only) and E3 (#346 review loop on origin/master) and produce RESEARCH-REPORT-review-panel-unification.md with (a) overlap matrix, (b) value inventory, (c) conflict log with /sc:adversarial on undecided conflicts, (d) target architecture, (e) future-use-case check. Report only.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | AX-1 | FAIL | Ran every command class: `git cat-file -t 4a22d742…` = commit; 17 E2 `git show` paths resolve (`git cat-file -e`), manifest.md = 16 lines, COMBO-REPORT.md = 506 lines (match items); `origin/master:src/superclaude/cli/review/__init__.py` resolves; 9874d63fb and c2e3347d3 are commits; the agent-12 `uv run pytest --collect-only …` command exits 0 (1182 collected); `uv run python scripts/reflect_shadow_exit.py` runs and writes nothing without `--out` (script :402-405), exit 1 (Stage 2 FAIL). FAIL because the `sc:adversarial --compare` call (line 290) uses space-separated paths the command cannot parse (B-1), and the Step 5.2 verify Grep pattern can never match (B-3). |
| 2 | Project convention compliance | AX-2 | FAIL | uv for every Python run; origin = IronbellyOrg/IronClaude (`git remote -v`); no `git show master:`; Step 7.3 runs `git add .dev/tasks` only, no commit; `git check-ignore` shows the task folder is not ignored; `git add --dry-run .dev/tasks` lists 18 files, no error. FAIL because the dynamic sub-checklist breaks the /task executor's item-adding rule (B-2). The `.claude/agent-memory` staging point is minor (M-2). |
| 3 | Intra-phase execution order simulation | none | PASS | Walked Phases 1-7: synth-04 before Step 5.2; synth-05 after the 5.2 verify item; synth-06 after synth-05; gaps-and-questions.md made in Step 3.3 before synth-01/02/04/07 read it; web files made in Phase 4 before synth-02/03/04/05 read them; Step 6.8 records the hash before Step 7.1 compares it. |
| 4 | Signature/value verification (cited anchors) | AX-1 | PASS (note) | Grep-verified: findings.py SEVERITIES :14, `_REF_TOKEN` :29, `refs_norm` :321; findings_v2 LENSES :36, DEVIATION_CLASSES :38; card_convert MAX_REF_TEXT :85 = 200, MAX_CLAIM :86 = 300; ledger `merge_round` :107, `apply_revision` :301, `verdict` :363; panel `select_env` :485, `resolve_slot` :500, `resolve` :565; cluster `cluster_v2` :381, `clusters_kept` :447; manifest `record_attempt` :331; severity_router `_CATEGORY_TABLE` :34; `__init__.py` names `lint_cmd`/`estimate_cmd` :24-25; contract `derive_verdict` :138; 20 file line counts match the items exactly. `_ID_TOKEN` is at :23, not :22 (M-5). |
| 5 | Module context (sibling consistency) | none | PASS | Every item that uses TASK_DIR, the `-cycle2` names or the `-a`/`-b` partition names uses the same convention as the item that consumes the file (see check 6). |
| 6 | Downstream consumer analysis (producer to consumer paths) | none | PASS | Tallied every output name in the task file: 7 synth names, 12 research names, 4 web names and every `qa/*.md` name each have exactly one spelling; the 6.6, 6.7 and 6.7b decision items read the exact `-cycle2` names their verifiers write; Step 6.5 reads `qa-lens-<lens>-a/-b.md` exactly as the 13 partitioned lens items write them; synth-07 lists the synth-05/06 names Steps 5.3/5.4 write. |
| 7 | Verification-step validity | AX-4 | FAIL | Step 5.2 verify item: the Grep pattern `Adversarial result:** pending` (line 294) returns 0 matches on the task file, which holds that marker 3 times; the escaped form `Adversarial result:\*\* pending` returns 3 (B-3). Step 6.1's Grep for `[CONTRADICTION:` fails loudly ("unclosed character class") (M-9). |
| 8 | Coverage of the primary use case | AX-4 | PASS (note) | The gates reach every required content (a)-(e). The synthesis-gate lenses still check "C01-C13" (lines 308, 316) while synth-04 requires C01-C14 (line 284), so C14 is enforced only by synth-04's own clause (M-1). |
| 9 | Error path coverage | AX-3 | PASS (note) | Every item has a blocker path. The exit script's expected exit 1 is not stated as expected (M-3). |
| 10 | Runtime failure path trace | AX-1 | FAIL | Trace of Step 5.2: entry step (3) calls `/sc:adversarial`, which splits `--compare` on commas (protocol SKILL.md:563), gets one path and stops with "requires at least 2 files, got 1" (:569). The entry then logs "debate failed", synth-05 treats every undecided conflict as an open question, and the owner's requirement for recorded debates is not met. |
| 11 | Completion scope honesty | none | PASS | Phase 7 has no `/sc:workflow`, no roadmap and no `/tech-reference`; Step 7.3 stages `.dev/tasks` and forbids commit, push and PR; Step 7.4 records the session's next step. |
| 12 | Ambient dependency completeness | AX-3 | PASS (note) | All 103 named repository, home and E2 paths exist (batch check, 0 missing); agent types rf-assembler, rf-analyst, rf-qa and rf-qa-qualitative exist in `~/.claude/agents/`; the `sc:adversarial` skill is listed. Notes: no prompt gives the absolute repository root (M-4); RUN2-QUEUED.md in the task folder is not fenced off (M-8). |
| 13 | Sequencing red flags (dynamic items, cycles) | AX-2 | FAIL | Dynamic items are appended without DYNAMIC CONTENT markers (B-2). Re-running ticked items in a new fix cycle works but cannot be resumed cleanly (M-7). |
| 14 | Existence claims verified | AX-1 | PASS (note) | All existence claims hold. The count "tests/cli/reflect/ (12 files)" is wrong: there are 38 `test_*.py` files (M-5). |
| 15 | Template cross-references | none | PASS | The scope-slice sections the prompts name exist (00: 2.1-2.7, 3, 5.1-5.6, 6, 7, 8; 01: 1.5, 2-4, 6; 02: 1-6; 03: 1.2, 2-5, 7; 04: 0.1, 0.8, 0.11-0.15, 2, 3, 4, and 6 item 10 with F-19, O-8 and MR:142; 05: 1A-1D, 2-4, 6). research-notes.md has EXISTING_FILES, SOLUTION_RESEARCH, SUGGESTED_PHASES (12 rows) and AMBIGUITIES_FOR_USER. tech-research SKILL.md has the Lens, Fidelity and Anti-Omission prompt sections (:1048, :1159, :1202). |

## Summary

- Checks passed: 10 / 15 (5 of them with minor notes)
- Checks failed: 5 (checks 1, 2, 7, 10 and 13, all tracing to the same three blocking findings)
- Critical issues: 0; Important (blocking): 3; Minor (notes): 9
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Axis | Location | Issue | Required Fix |
|---|----------|------|----------|-------|-------------|
| B-1 | IMPORTANT (blocking) | AX-1 | Task file line 290, Step 5.2 item 1, ENTRY TEMPLATE step (3) | `--compare <dir>/proposal-a.md <dir>/proposal-b.md` passes the two files separated by a space. `/sc:adversarial` takes "Comma-separated file paths" (`~/.claude/commands/sc/adversarial.md:15,39,58`), and the protocol "Split[s] --compare value on commas" then stops with "Adversarial comparison requires at least 2 files, got <N>" (`~/.claude/skills/sc-adversarial-protocol/SKILL.md:563-569`). Every debate entry would stop, record `debate failed`, and synth-05 would treat every undecided conflict as an open question. The syntax came from BUILD-REQUEST.md:42 (placeholder form); the intent (compare the two proposals) is clear. `--depth standard`, `--focus correctness,risk,test-coverage` (free-form, comma-separated) and `--output <dir>/` are valid. | Change step (3) to `--compare .dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/reviews/adversarial/<slug>/proposal-a.md,.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/reviews/adversarial/<slug>/proposal-b.md` (one comma, no space). Keep the other flags. |
| B-2 | IMPORTANT (blocking) | AX-2 | Line 290 (append instruction) and lines 531-533 (`### Phase 5 Adversarial Sub-Checklist`) | The task (frontmatter `task_type: dynamic`, line 61) adds `- [ ]` items at run time, but has no `<!-- DYNAMIC CONTENT START: … -->` / `<!-- DYNAMIC CONTENT END: … -->` markers (grep: 0 hits). The /task executor forbids adding checklist items outside those markers (`~/.claude/skills/task/SKILL.md:119`, F4 :157 and :161), and template 02 I6 (`~/.claude/templates/workflow/02_mdtm_template_complex_task.md:557-572`) defines the markers as the only permitted place. A compliant executor must log the item as incorrect and ask the user (`task/SKILL.md:118`), which halts the run at Step 5.2. | Keep the owner-requested Task Log location. Put `<!-- DYNAMIC CONTENT START: adversarial-debates -->` and `<!-- DYNAMIC CONTENT END: adversarial-debates -->` inside `### Phase 5 Adversarial Sub-Checklist`, and change item 1 of Step 5.2 to append the entries (or the single "No adversarial run needed" line) between the two markers. |
| B-3 | IMPORTANT (blocking) | AX-4 | Line 294, Step 5.2 item 3 | The check "Grepping … for `Adversarial result:** pending` (expected: no match)" cannot fail: as a ripgrep regex, `:**` matches no literal asterisks. Tested on the task file, which holds that marker 3 times: the pattern as written returns 0 matches, while `Adversarial result:\*\* pending` returns 3. A missed write-back into synth-04 would pass this check silently, and synth-05 would start on a pending conflict. | Replace the pattern with `Adversarial result:\*\* pending` (or tell the executor to search for the fixed string `Adversarial result:** pending`). |
| M-1 | MINOR | AX-4 | Lines 308 (synthesis-accuracy partition 1) and 316 (structure partition 1) | The synthesis-gate lenses check options for "C01-C13" and require "C01-C13 at minimum", while synth-04 requires C01-C14 (line 284, the A.10.25 fix AL-B4). C14 (`panel-size-cost`) is enforced only by synth-04's own ensuring clause. | Change both to C01-C14. |
| M-2 | MINOR | AX-2 | Line 454, Step 7.3 | The clause "no `.claude/` path is staged" can conflict with the task folder's own `.claude/agent-memory/` (it exists with rf-analyst, rf-qa, rf-qa-qualitative, rf-task-builder subfolders). The root `.gitignore` rule `.claude/*` (line 127) is root-anchored: `git check-ignore` reports `.dev/tasks/…/.claude/agent-memory/rf-qa-qualitative/MEMORY.md` as not ignored. The folders are empty today, but if any agent saves memory there, `git add .dev/tasks` stages it and the clause cannot be met. | Say the clause covers the repository-root `.claude/` only, or tell agents not to write memory inside the task folder. |
| M-3 | MINOR | AX-3 | Agent 7 (line 194), agent 11 (line 202), Phase 3 evidence partition 2 (line 226) | `scripts/reflect_shadow_exit.py` exits 1 when Stage 2 is not met (run today: `OVERALL: FAIL (shadow runs 13 of 20)`, exit 1). The prompts do not say exit 1 is an expected result, so an agent may log it as a command failure. | Add "exit code 1 means the Stage 2 exit criteria are not met; record the output, it is not a blocker". |
| M-4 | MINOR | AX-3 | All agent prompts; Steps 6.8 (line 440) and 7.1 (line 446) `sha256sum`; line 226 exit-script re-run | Every path is relative (`.dev/tasks/…`, `scripts/…`) and no prompt states the absolute repository root (only Steps 1.2 and 7.3 do, and subagents do not see them). In this QA run the subagent's primary working directory was the task folder, where those relative paths do not resolve. | Add `Repository root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel` next to every TASK_DIR definition, and "from the repository root" to the two `sha256sum` commands. |
| M-5 | MINOR | AX-1 | Lines 194, 204 and 131 | "the twelve files in `tests/cli/reflect/`" and "`tests/cli/reflect/` (12 files)": the folder holds 38 `test_*.py` files (the "12" in research-notes.md:46 seems to mix it up with the 12 reflect files in `tests/review/`). `_ID_TOKEN` is at `telemetry.py:23`, not :22. Agents Glob and read the source, so this corrects itself. | Change the count to "list with Glob" (no number), and :22 to :23. |
| M-6 | MINOR | AX-2 | Line 246 | "re-executing the five Step 3.2 items above … and then this item again": only four items sit above it (the Phase 5 equivalent at line 338 correctly says four). | Change "five" to "four". |
| M-7 | MINOR | AX-3 | Decision items at lines 246, 338, 396, 416, 436 | A new fix cycle re-runs items that are already `[x]`. The executor's rules say "never go backward to re-execute items" (`task/SKILL.md:608`) and on resume "Do NOT re-execute any `- [x]` items" (:537). The decision items instruct the re-run and the skill's own gate protocol allows repeats (:258), so it runs, but after a restart in mid cycle 2 nothing unchecked marks where cycle 2 stopped. | Optional: in each decision item, log `Cycle N+1 started` and the last finished sub-step in the Execution Log so a resume can find its place. |
| M-8 | MINOR | AX-3 | Task folder root `RUN2-QUEUED.md` | The file names commit c2ddeb1b and the run-2 hand-off paths. The gates treat any such reference as blocking, but no item tells agents to ignore this file, and agents that Glob the task folder will see it. | Add to Key Constraints: "Ignore `RUN2-QUEUED.md`; it is out of scope for this run." |
| M-9 | MINOR | AX-4 | Line 348, Step 6.1 measure item | Grep for `[CONTRADICTION:` is rejected by ripgrep ("unclosed character class"). The failure is loud, so the executor will notice it. Also, the Mode A protocol merges the two proposals and records a base selection; the write-back template's `winner <A or B>` does not name which output file to read (for example `adversarial/base-selection.md`). | Use `\[CONTRADICTION:`; name `<slug>/adversarial/base-selection.md` and the merged file as the debate result files. |

## Actions Taken

None (fix_authorization: false). No file other than this report was created or modified.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

See `## Self-Audit` below.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for B2 self-containment of all 104 items, including the B-1 split-rule fix in the 13 lens items.
- Relied on rf-qa PASS for frontmatter, sections and Task Log structure, Phase 5 order, fix-loop halt ordering and owner scope rules.
- Relied on rf-qa PASS for S-1 (M1-M4 track labels and gap coverage), S-2 (late-change gate re-runs) and M-5 (cycle-2 file names). I did not re-check the halt-message wording.
- Relied on the A.10.25 alignment fixes AL-B1..AL-B4 and the orchestrator's grep counts. I re-checked only C14 (3 hits, confirmed).
- Relied on rf-qa for the 7 TB-Add structural items.

**(b) Independent semantic checks (≥1 required, INV-019):**
- `/sc:adversarial` flag syntax, checked against `~/.claude/commands/sc/adversarial.md:15,39,58` and protocol `SKILL.md:563-569`. The structural PASS (self-containment, Phase 5 order) could not catch that the command cannot parse the call (B-1).
- Whether the /task F1 loop can run the dynamic sub-checklist, checked against `~/.claude/skills/task/SKILL.md:92,118-119,157,161` and template 02 I6 :557-572, plus a grep for markers (0). Structural PASS did not cover how the executor behaves (B-2).
- Gate patterns run for real: the Grep tool with `Adversarial result:** pending` gave 0 matches against 3 present occurrences, and `[CONTRADICTION:` gave a regex error (B-3, M-9).
- Command dry-runs: E2 `git cat-file -e` on 17 paths, the `origin/master` blob, `uv run pytest --collect-only` (exit 0, 1182), `reflect_shadow_exit.py` (exit 1, read-only), `git add --dry-run .dev/tasks`, and `git check-ignore` on the task-local `.claude` path (M-2, M-3).
- A tally of every producer and consumer file name (synth, research, web, qa) found exactly one spelling for each.

1. **Factual claims verified independently:** about 140. That is 103 path existence checks, 17 E2 git paths, 4 refs, 20 line counts, 22 symbol anchors, 5 command dry-runs, 3 regex tests and the scope-section headings.
2. **Files read:** the full task file (lines 1-578), BUILD-REQUEST.md:42, RUN2-QUEUED.md, research-notes.md headings, the headings of the 6 scope slices, `~/.claude/commands/sc/adversarial.md` (:15-80, :130-195), `~/.claude/skills/sc-adversarial-protocol/SKILL.md:550-629`, `~/.claude/skills/task/SKILL.md:83-182` plus greps, template 02 :540-584, `scripts/reflect_shadow_exit.py` (grep for writes), `.gitignore` (`.claude` rules), and greps of rf-qa.md and rf-analyst.md.
3. **Zero issues claimed?** No. There are 3 blocking and 9 minor findings, each with a tool-evidenced location.
4. **Web research:** none performed. Every check was local, so no Tavily or fallback calls were made.

## Confidence Gate

- **Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 13 | Grep: 9 | Glob: 0 | Bash: 14 (one policy-format batch script covered the 103-path, E2 and refs checks)
- Unchecked items: none. Unverifiable items: none. I did not run the actual `/sc:adversarial` debate. B-1 rests on the command and protocol text, not on a live run.

## Recommendations

1. Fix B-1, B-2 and B-3 (three one-line edits in Step 5.2 and the Task Log sub-checklist section), then re-run this lens or a single verifier on Step 5.2 before starting `/task`.
2. Apply M-1, M-4 and M-8 in the same pass. They are cheap and remove likely false blockers at the gates.

## QA Complete

VERDICT: FAIL

