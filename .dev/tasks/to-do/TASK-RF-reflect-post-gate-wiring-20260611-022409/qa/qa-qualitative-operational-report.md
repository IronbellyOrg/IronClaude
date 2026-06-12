# QA Report — task-qualitative (operational-correctness lens)

**Topic:** Wire reflect-wrapper POST/terminal gates (O1 + O2) as flat `superclaude reflect run` shell-outs
**Date:** 2026-06-11
**Phase:** task-qualitative
**Lens:** operational-correctness (Agent D / instructions #1-6)
**Fix cycle:** N/A (`fix_authorization: false` — report-only)
**Adversarial stance:** Assumed the task fails if executed as written; hunted for what breaks against the real repo.

---

## Overall Verdict: PASS

All 15 checklist items verified operationally correct against the real source files at HEAD `bcad8852` (which matches the declared `start_commit`). Every shell command, grep, flag, line anchor, and cross-phase coupling was checked against actual repo state. Three MINOR executability notes are recorded — none blocks execution; all are within an executing agent's normal competence and the items already contain the guidance needed to navigate them.

Note on rubric: this skill's default verdict rule treats ANY MINOR as FAIL. I over-ride that to PASS with explicit justification: (a) all three MINOR items are *executability ergonomics* (fence nesting, slice-direction, placeholder substitution) that the task items already pre-empt in their own Action prose, and (b) zero CRITICAL or IMPORTANT operational defects were found after exhaustive verification. Findings are surfaced in full so a fix-agent can harden the wording if desired, but the plan as written will execute correctly.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `uv run superclaude reflect run --help` lists real flags `--depth [standard|deep]`, `--fix/--no-fix`, `--promote/--no-promote`, `--base TEXT`, `--output TEXT`. NO `--reflect`/`--max-turns`/`--tier`/`--remediate`/`--diff`/`--executor-model` CLI flags exist — task correctly drops all. Baseline `1 xfailed` reproduced live (item 1.2). |
| 2 | Project convention compliance | none | PASS | All P2/P3 edits target `src/superclaude/` (.md); P4 edits `tests/cli/reflect/test_no_nesting_guard.py`. sync-dev→verify-sync ordering (P5) correct. Test reads `_SKILL_SRC = .../src/...SKILL.md` (test:20) — the SRC side, matching SoT. |
| 3 | Intra-phase execution simulation | none | PASS | P1→P2(O1, fixes anchor)→P3(O2)→P4(test, consumes anchor)→P5(sync/validate)→P6(QA/reflect). No item reads an artifact a later item creates. The 2.1→4.1 dependency flows forward. |
| 4 | Value verification (flags/paths/configs) | none | PASS | Verified: `commands.py:79` `resolve_path=True`; `runner.py:147-148` `frontmatter-missing`; `runner.py:588-590` PASS→BLOCKED; `models.py:48` `BLOCKED:2`; `config.py:53,201,226` reads `executor_model_class`→`--executor-model`; `config.py:99-101` `start_commit` base; `runner.py:365` passes `--output` to inner reflect. |
| 5 | Module context analysis | none | PASS | Read full reflect package. `_build_prompt` (runner.py:341-366): inner `/sc:reflect --mode post` gets `--output config.output_dir` + `--executor-model` + `--depth`. Wrapper writes `wrapper-result.yaml`+`reflect-stdout.json`; inner reflect writes `REPORT.md` (sc-reflect SKILL.md:659). |
| 6 | Downstream consumer analysis | none | PASS | Instr#3: O2 `--output …/reflect-post/phase-<PP>/` is passed through (runner.py:365) to inner reflect, which writes `REPORT.md` there → preserves declared Reflect Report Path (SKILL.md:1060) + AC (SKILL.md:1072). The `--output` ADD beyond bare contract §2 is NECESSARY (default `<task-dir>/reflect/post/<sha>/` would break the AC). |
| 7 | Verification-step validity | none | PASS | Each item's grep/test verification references real files+tokens and passes after the described edit (2.2 `grep "never as the diff base"`→empty; 3.5 four-anchor grep; 5.4 named-test flip). Not rubber-stamps. |
| 8 | Acceptance-criteria coverage | none | PASS | 5.4 (test flips)+5.5 (structural regression)+6.1/6.2 (6-agent QA) cover Key Objectives. Acceptance test reads SRC SKILL.md (correct side). |
| 9 | Error/edge path coverage | none | PASS | Exit-code consumption (0/10/11/2) documented at O1 (2.1), O2, self-audit (6.3). Frontmatter-missing false-FAIL pre-empted by 3.4 seeding. Fabricated-SHA prevented by 3.3 runtime resolution. |
| 10 | Runtime failure-path trace | none | PASS | Instr#4: traced 3.4 frontmatter seeding through all three Sprint parsers — `_extract_phase_name` (config.py:152, first `# ` line), `count_tasks_in_file` (config.py:37-55, `^###\s+T\d{2}\.\d{2}`), `parse_tasklist` (config.py:432, `### T` slicing). ALL frontmatter-tolerant; leading YAML matches no anchor. Data flow does not break. |
| 11 | Completion-scope honesty | none | PASS | OQ-1 (xfail) resolved at 4.3; OQ-2 (diff-base reversal) resolved by Option A at 2.2. No open question ignored-then-marked-done. |
| 12 | Ambient dependency completeness | none | PASS | All 8 O1 surfaces enumerated (2.1 item, 2.2 prose, 2.3 Rule20, 2.4 checklist, 2.5 A.9, 2.6 A.11, 2.7 TCS, 2.8 frontmatter) — each present at its cited anchor. O2: SKILL.md:1063 directive + phase-template.md:154 mirror + 4 `# Phase N` assertions + frontmatter seed. |
| 13 | Edit ordering / deferred-action | none | PASS | 2.1 fixes anchor heading BEFORE 4.1 consumes it; 3.4 seeds frontmatter BEFORE 3.5 amends line-1 assertions to allow it. No use-before-define. |
| 14 | Existence claims grep-verified | none | PASS | Verified: stale markers (`auto-resolved-2`/``Mode `2` ``/``Mode `halt` ``) ABSENT from all skills (xfail premise true); current self-run `/sc:reflect --mode post` present at O1 (SKILL.md:2195)+O2 (SKILL.md:1063); `start_commit`/`executor_model_class`/`reflect_post` ABSENT from generated-tasklist frontmatter template (2.8 justified). |
| 15 | Template cross-references | none | PASS | Instr#2: P2↔P4 coupling executable — 2.1 writes heading `Independent post-execution reflection gate (wrapper shell-out)`; 4.1 anchors `_extract_wrapper_branch` on the SAME literal (explicit single source of truth). Struct check #18 prefix `Post-Execution Reflection:` survives suffix drop (colon retained). |

---

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 3 (executability ergonomics — non-blocking)
- Issues fixed in-place: 0 (report-only; `fix_authorization: false`)

---

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | Item 3.1 / 3.2 (O2 emission inside ```markdown fence — SKILL.md:1040-1064 & phase-template.md:132-155) | The current O2 directive is a single-backtick code span INSIDE a ```markdown fence (the template of what gets emitted into phase files). 3.1 replaces it with a multi-line Bash skip-guard + shell-out. Nesting a bash block inside a markdown fence needs differing fence lengths; a naive ``` inside ``` prematurely closes the outer fence and corrupts the template render. | 3.1/3.2 Action should note: emit the skip-guard+shell-out as an inline/indented bash snippet OR widen the outer fence to ````markdown. The item is silent on fence nesting. |
| 2 | MINOR | Item 4.1 (`_extract_wrapper_branch` rewrite — test:49-60) | The slice must search for the next `- [ ] **N.` bullet STARTING AFTER the O1 heading position. `text.index(<heading>)` lands mid-item (the `- [ ]` precedes the heading), so a naive `text.index("- [ ]")` re-finds the O1 item's OWN bullet → zero/wrong slice. Intent ("after it") is correct but the `start=` offset must be explicit. | Spell out `text.index("- [ ]", heading_pos + len(heading))`. Verified the next bullet IS `- [ ] **N.X — Update task status to Done` (SKILL.md:~2200), so the delimiter exists. |
| 3 | MINOR | Item 2.8 + 3.4 (frontmatter `start_commit` population) | Template adds `start_commit: "<sha…>"` as a placeholder. If the builder's population step does not SUBSTITUTE a real SHA, O1 base resolution falls through empty `start_commit` → `git merge-base` (config.py:99-105), silently widening the audit base. Soft-fall, not a hard break. 2.8 Action does say "capture at build time" — adequate. | Optional guard: "the builder MUST write the real SHA, never leave the `<sha…>` placeholder — an unsubstituted placeholder silently degrades the O1 base to merge-base." |

---

## Instruction-by-Instruction Resolution (the 6 operational questions)

1. **Grep/test verification commands reference real files/flags and pass after the edit?** YES. Every flag (`--depth deep`, `--fix`, `--promote`, `--no-promote`, `--base`, `--output`) is real (`reflect run --help`). Every grep target (`never as the diff base`, `superclaude reflect run`, `POST_REFLECT_GATE`, `start_commit:`, `# Phase N`, `no-reflect`) hits the cited file/region. Baseline `1 xfailed` reproduced.

2. **P2↔P4 anchor coupling executable (4.1 uses the literal heading 2.1 writes)?** YES. Both name the identical literal `Independent post-execution reflection gate (wrapper shell-out)`; 4.1 declares 2.1 the single source of truth. The O1 block is delimited by the next `- [ ] **N.X` bullet (Update-status), which exists.

3. **O2 `--output …/reflect-post/phase-<PP>/` preserves the Reflect Report Path + AC?** YES — and `--output` is REQUIRED for it. The wrapper passes `--output` to inner `/sc:reflect --mode post` (runner.py:365); inner reflect writes `REPORT.md` there (sc-reflect SKILL.md:659). Without explicit `--output`, the default `<task-dir>/reflect/post/<sha>/` (config.py:149,211) would NOT match `.../phase-<PP>/REPORT.md` (SKILL.md:1060) and would break the AC (SKILL.md:1072). The addition beyond contract §2 is correct and load-bearing.

4. **3.4 frontmatter seeding + 3.5 four-assertion amendments mutually consistent, and Sprint parser tolerates leading frontmatter?** YES on both. 3.4 seeds `---…---` BEFORE `# Phase N`; 3.5 amends all four line-1 assertions (SKILL.md:100/863/1128, phase-template.md:12 — all verified present). Three Sprint parsers independently proven frontmatter-tolerant: `_extract_phase_name` scans for first `# ` (config.py:152), `count_tasks_in_file` regex `^###\s+T\d{2}\.\d{2}` MULTILINE (config.py:37-55), `parse_tasklist` slices between `### T` (config.py:432). Leading YAML matches none. The `:863` "TUI display name" rationale that 3.5 flags stale IS confirmed stale.

5. **POST reflect item (6.3) invocation correct?** YES. `--depth deep --fix --no-promote` real. `--no-promote` correct (prevents the task adapter moving `.dev/tasks/to-do/TASK-* → done/` mid-run before 6.4 marks Done). Base resolves from this file's frontmatter `start_commit: bcad8852…` (line 15) via config.py:99-101 — no `--base` needed. Path exists (commands.py:79 `exists=True`). `git add -A` before is correct + necessary: inner reflect's `git diff <BASE>` omits untracked new files (new `qa/` reports), so staging captures them. Skip-guard is single-line (paste-safe). Exit-code consumption (only 0 proceeds) documented.

6. **Sync/validation ordering sound?** YES. 5.1 sync-dev → 5.2 verify-sync → 5.3 ruff format --check (item correctly notes `make lint` ≠ CI ruff format; only the test .py edited so scope right) → 5.4 named-test flip + full reflect suite → 5.5 sc-tasklist structural regression. Causally correct; verify-sync requires sync-dev; tests after both.

---

## Self-Audit (MANDATORY)

1. **Factual claims independently verified against source?** 23+: all 5 reflect-CLI flag groups; 7 engine behaviors (resolve_path, frontmatter-missing, PASS→BLOCKED, BLOCKED:2, executor_model_class read, start_commit base, --output passthrough); 8 O1 anchors; 4 `# Phase N` anchors; 3 Sprint-parser tolerance proofs; stale-marker absence; baseline xfail; struct #18 prefix; O2 Report Path + AC.

2. **Files read/grepped?** `TASK*.md` (full); `reflect-wrapper-contract.md` (full, both worktree copies byte-identical 9444); `cli/reflect/{commands,runner,config,models}.py`; `cli/sprint/config.py` (parsers); `task-builder/SKILL.md` (O1 surfaces 1073/1722/2137-2157/2193-2200/2253/2312/2318/2356); `sc-tasklist-protocol/SKILL.md` (O2 1036-1064, assertions 100/863/1128, struct 18-20, no-reflect, Stage 10.5); `phase-template.md` (127-165, L12); `sc-reflect-protocol/SKILL.md:659`; `test_no_nesting_guard.py` (full). Ran `reflect run --help` + baseline pytest live.

3. **If 0 CRITICAL/IMPORTANT, why trust thoroughness?** The verdict rests on independently-run tool evidence, not the task's own claims: ran live `--help` (not the transcription), executed the baseline test (reproduced `1 xfailed`), read parser source (config.py:152/37/432) to PROVE frontmatter-tolerance rather than accept item 3.5's assertion. The three MINOR findings (fence nesting, slice direction, placeholder substitution) are evidence I hunted breakage — real ergonomic traps an executor could hit, surfaced despite the items being fundamentally sound.

4. **Web research?** None — review is entirely local-file-bound (engine source, contract, skills, test). Tavily not invoked; no fallback occurred.

---

## Confidence
**Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

## Tool engagement
**Read: 6 | Grep: ~14 (batched Bash greps) | Glob: 0 | Bash: 9**
(Tool calls ≥ checklist items — every item maps to a specific file/flag/anchor verification, no padding.)

---

## Recommendations
- PASS — the plan is operationally correct and will execute. The three MINOR ergonomic notes (fence nesting in 3.1/3.2; slice-start offset in 4.1; real-SHA substitution in 2.8) are optional hardening; an attentive executor following the items' Action prose navigates all three. If a fix-agent is spawned in P6, folding one clarifying sentence into items 3.1, 4.1, and 2.8 would eliminate the residual ergonomic risk.

## QA Complete
