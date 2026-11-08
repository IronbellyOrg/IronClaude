# QA Report - Task Qualitative Review (lens: operational-correctness)

**Topic:** TASK-RESEARCH-issue-watcher-20261107-064950 (issue #331 research task file)
**Date:** 2026-11-07
**Phase:** task-qualitative
**Fix cycle:** N/A (first qualitative review of the task file after the A.10.25 alignment fixes)
**Status:** Complete

BUILD-REQUEST GOAL baseline (verbatim, from BUILD-REQUEST.md line 12): "Conduct a technical investigation on existing solutions and design inputs for a GitHub issue watcher and routing service (GitHub issue #331 of IronbellyOrg/IronClaude: a watcher that finds issues that are tagged, human-approved, in a GitHub Project and in Backlog status, and makes the right developer's Coder workspace start a new session running `/sc:issue --claim <N>`), and produce a structured research report with findings, gap analysis, options (workspace-side poller, GitHub Action plus listener, central microservice, hybrids), and a concrete implementation recommendation that fits this repository (commands, skills, CLI code, docs; no live deployment)." Drift axis (AX-1) is ACTIVE.

---

## Evidence log (appended incrementally)

Task file read end to end (469 lines, 335,092 bytes; every checklist item, lines 171-370, plus Task Log and Deviations).

### E1. Cited repo anchors re-read at the cited line (own sed reads, this run)
All of these matched what the task prompts say they contain: `commands/issue.md` lines 8, 15, 24, 45-51, 68, 71, 79; `sc-issue-protocol/SKILL.md` 70-72, 82-85; `origin_repo.py` 28-49, 105-137; `WORKER-CONTRACT.md` 23 (never-as-worker list contains `/sc:issue`) and 39 (WC-8); `ccsession-tag/README.md` 21, 228-234, 272; `core/CLAUDE.md` 45-53; `orca-capabilities.md` 66 (pull-only); `sc-issue-launch-level-hook.md` 6-10, 23, 41, 52; `launch-job-identity.sh` 1-8; `test.yml` 3-8; `boundary-guard.yml` 25-26; `contract3-generator-constraint-lint.yml` 22-23; `pr_submit/ci.py` 10-15 (imports `re`, `.classifier`, `.models`) and 25 (`classify_checks`); `cli/main.py` 521 (`sprint_group`) and 561 (`reflect_group`); `Makefile` 13/48/53/109/166 (`test`, `lint`, `format`, `sync-dev`, `verify-sync`). `grep schedule .github/workflows` returns nothing (no schedule trigger). `launch-level-guard.sh` does not exist (design-only, as the task says). `.github/workflows/orca-upstream-monitor.yml` is absent here (it is a Coder-repo path inside the quoted #477 text, not a repo-local claim). `enrichment/research-deep.md` is absent (it is the item 7.2 output, correct).
`codebase-context.md` line 21 carries the CORRECTION about `ci.py` (file mtime 07:33), so the task's "was corrected" statement is true.

### E2. Agent types and tools (read from the agent list and `~/.claude/agents/`)
`rf-task-researcher`, `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, `rf-assembler` all exist as files and all list Write and Edit. `rf-task-researcher` lists `mcp__tavily__tavily_search`, `mcp__tavily__tavily_extract`, `WebFetch`, `WebSearch`, so the web items need no `general-purpose` swap (the Deviations note covering that swap is a harmless contingency). `general-purpose` has all tools. Subagent_type tally in the task file: rf-qa 27, rf-qa-qualitative 16, rf-task-researcher 7, rf-analyst 4, general-purpose 4, rf-assembler 1. Gate counts match BUILD-REQUEST (Gate 1 = 3, Gate 2 = 3, Gate 3 = 3+3+1 = 7, Gate 4 = 2, Gate 5 = 2 rf-analyst, verification rounds of 2).

### E3. Output-path scan
Every `qa/`, `synthesis/`, `research/`, `phase-outputs/{reports,plans}` file name appears at least 3 times (creator plus readers); no orphan name. Forward-read scan: no item reads a file a later item creates. `phase-outputs/` does not exist yet and is created in Step 1.2 before any use.

### E4. Defects found by own tool work
- Output collision. `qa/` already holds `qa-fix-log.md` (the A.10 validation-round fix log) and `qa-fix-verification.md` (the A.10 verification, "VERDICT PASS"). Gate 3 writes the same two names: Step 6.5 (fix agent log, or the "no fix agent needed" log), Step 6.6 (verification agent report) and Step 6.6 decision item (reads both). `grep -c "a10-task-validation|qa-task-validation|move the validation|validation-round|qa-task-research-alignment"` on the task file = 0. Nothing tells the executor to move or rename the old files. Consequences: (1) the first Write of an agent overwrites the validation-round evidence; (2) Write on an existing file the agent has not Read fails, so the "no fix agent needed" branch can error; (3) if a Gate 3 agent dies before its first write, the decision item reads the stale A.10 "PASS" as a Gate 3 verification result.
- Halt wire string. The task file writes the regression halt message five times as `Regression detected on Item X.Y, previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` and calls it byte-exact. The authoritative wire string (`~/.claude/skills/task-builder/SKILL.md:1293`, the API-004 table; `tests/audit/test_regression_halt_pass1_fail2.py` header, which asserts U+2014) uses an em-dash instead of the comma after `X.Y`. `[HALT-MONOTONICITY] |F|=<n>` matches. Order (regression, then monotonicity, then cap) matches SKILL.md:1278/1309.
- gh presupposition. Agent 02's prompt (line 187) says "the expected answer, which you must confirm or refute with your own search, is 'none found'" for a search of "the whole of `src/superclaude` and `tests/`". For `src/superclaude` that is true (grep for a quoted `gh` argv element in src .py files: no hits). For `tests/` it is false: `tests/pr_submit/test_conflict_e2e.py:104` runs `subprocess.run(argv, ...)` and line 167 calls `_run(["gh", *args], ...)` against a PATH stub `gh` written by `install_gh_stub` (line 138-141); `test_static_grep.py`, `test_cosmos_poll.py`, `test_conflict_scripts.py`, `test_codex_reviews.py` also write `gh` stub executables. That PATH-stub approach is the repo's actual way of mocking `gh`, which is the answer to the same prompt's question (5), but question 3 is framed to expect none.
- Staging. The task never stages `.dev/tasks/`. `grep "git add|staged|staging"` on the task file: no matches; the tech-research SKILL.md has no staging step either; `git status` shows the package and `.dev/brainstorms/...` and `.dev/issues/331/` untracked. Convention (global CLAUDE.md rule 4): `.dev/tasks/` is always staged, never left untracked.

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | AX-3, AX-2 | FAIL | Commands are read-only (`mkdir -p`, `stat -c`, `wc -w -c`, Glob) and valid here; every cited path exists (E1). But Step 6.5/6.6 Write `qa/qa-fix-log.md` and `qa/qa-fix-verification.md`, which already exist (issues 1). And the five "byte-exact" regression halt strings differ from the API-004 wire string (issue 2). |
| 2 | Project convention compliance | AX-3 | FAIL | No item edits `src/` or `.claude/` (read-only research respected; `.dev/brainstorms/.../enrichment/research-deep.md` is the only write outside the package and BUILD-REQUEST authorizes it). Source-of-truth and sync rules are not touched. But no item stages `.dev/tasks/` (issue 4). UV rule: only `uv run pytest` appears (inside the synth-04 prompt), no bare python/pip. |
| 3 | Intra-phase execution order simulation | none | PASS | Walked Phases 1-7 item by item. Every read has an earlier writer: gaps file (Step 3.4 tail) before Step 4.1 and 5.1; synth-04 explicitly after synth-03; Step 6.1 validation before Step 6.5; verdict files (3.4, 5.5, 6.6, 6.7, 6.8) before Step 7.1/7.3. `phase-outputs/` created in Step 1.2. Glob `research/0*.md` matches only 01-03 (`research-notes.md` starts with r). |
| 4 | Function signature verification | none | PASS | Doc-task adaptation: every documented signature/anchor was re-read (E1): `classify_checks` at ci.py:25, `main.add_command(<group>, name=...)` at main.py:521/561, Makefile target lines, workflow trigger lines. All match. |
| 5 | Module context analysis (incl. cross-symbol input shape) | none | PASS | The shared input is the claim argument: `issue.md:8` says `--claim <number|url>` and `origin_repo.py` resolves both a number and a URL (E-FOREIGN-REPO at :28-49, :137). Agent 01 question 8 asks exactly how the argument is validated and whether the prompt can be the single line, so the integer-only rule is tested against both consumers. |
| 6 | Downstream consumer analysis | AX-3 | FAIL | The Step 6.6 decision item reads `qa-fix-verification.md` and `qa-fix-verification-qualitative.md`; the first name already exists with a stale PASS from the validation round (issue 1). Other consumers (inventory, gaps file, verdicts, Step 7.1/7.3 readers) point at files their producers create. |
| 7 | Test validity | none | PASS | Verification steps are substantive: re-read at least 15 cited locations (Gate 3 evidence lens), re-fetch 5+ URLs (domain lens), 6+ URLs (fidelity 2), exhaustive enumeration with an adds-up count (anti-omission), `wc -w -c` plus Grep for `ci.py` and `codebase-context.md` on the condensed copy. No placeholder-style assertions. |
| 8 | Test coverage of primary use case | none | PASS | TESTING_REQUIREMENTS is N/A (BUILD-REQUEST line 41); the deliverable-level check is Gate 3 to 5 plus validation checklist, covering TEMPLATE_COMPLIANCE, EVIDENCE_TRAIL, CROSS_VALIDATION (BUILD-REQUEST line 40) and three end-to-end chains (security, listener, session launch) in the crossref lens. |
| 9 | Error path coverage | none | PASS | Every item carries a blocker-logging clause with the templated format and a completion gate; halt guards, 2-cycle cap and escalation exist per gate; missing-report cases are handled ("MISSING ... blocking process finding"). |
| 10 | Runtime failure path trace | AX-3 | FAIL | Traced Gate 3 end to end: fix agent Write on an existing, unread `qa-fix-log.md` can error; verification agent Write overwrites A.10 evidence; a dead agent leaves a stale PASS that the decision item can read (issue 1). The other four gates use suffixed names (`-phase3`, `-phase5`, `-fidelity-`, `-anti-omission-`) and are unaffected. |
| 11 | Completion scope honesty | none | PASS | Open questions are carried to Section 9, not closed by assertion; owner decisions D1-D3 are recorded as decided; UNVERIFIED parts of the `orca agent launch` contract go to Section 9; the cap-and-escalate rule forbids converting open blocking findings to notes. (Minor note M1 on branch wording.) |
| 12 | Ambient dependency completeness | none | PASS | Frontmatter start/completion updates (1.1, 7.5), Task Summary stub replacement (7.4), Execution Log entries, directories (1.2), inventories (2.2, 4.2), verdict files, presentation summary, post-completion validation all have a creating item. Staging is the one omission (issue 4, scored under check 2). |
| 13 | Kwarg sequencing red flags | none | PASS | No deferred-action pattern lacks a completion item. Items that "pass" a new input to an agent (brief into the web prompts, file lists into fidelity prompts) are preceded by the item step that builds that input. Cycle-2 sub-steps 3a-3d are ordered and each file name is created before it is read. |
| 14 | Function existence claims verified | AX-1 | FAIL | `ci.py` not a `gh` wrapper: verified (imports only `re`, `.classifier`, `.models`). "No `schedule:` trigger": verified. `launch-level-guard.sh` absent: verified. "None found" for `gh` calls under `tests/`: contradicted by `tests/pr_submit/test_conflict_e2e.py:104,167` (issue 3). |
| 15 | Template cross-references | none | PASS | Step 7.3 maps I17 items 1-6 (template lines 679-686 read). PG.5 pattern (template line 1394) and "max cycles per I16 gate-type table / 2 fix cycles, 3 reviews, HALT and escalate" (template lines 657, 757, 1094, 1123) match the task's gate wording. Skill standard-intensity counts (SKILL.md lines 397-414) match the gate items. |

Additional operational checks (lens focus), all re-run by me:
| Check | axis | Result | Evidence |
|---|---|---|---|
| Referenced agent types exist and can do the job | none | PASS | E2. |
| Web agents have web tools; fallback explicit | none | PASS | `rf-task-researcher` lists Tavily and WebSearch/WebFetch; prompts name Tavily first and `provider=WebSearch` annotation on fallback; Deviations line 455 states the `general-purpose` swap rule if ever needed. |
| Parallel spawning instructions | none | PASS | Each parallel group is declared "MAY be spawned in one message" and says to mark items individually; Step 6.2-6.4 batch of seven is consistent with Gate 3 = 7; synth-04 serialized after synth-03. |
| Halt conditions match skill rules (max 2 fix cycles) | AX-2 | FAIL | Cap and order match; the wire string does not (issue 2). |
| Condensed copy writes to the right path within size limit | none | PASS | Path is `.dev/brainstorms/20261107-064825-github-issue-watcher/enrichment/research-deep.md`; `enrichment/` exists (Glob/ls); size rule is "at most about 5000 tokens", checked with `wc -w -c` at 3500 words / 20000 chars, with "condense further" fallback. |
| Read-only constraint respected | none | PASS | No item edits source, installs or deploys; web agents are "read-only web access only"; Gate fix agents edit only report, research or synthesis files in the task folder. |

## Summary
- Checks passed: 10 / 15 (checklist) ; lens-specific operational checks 5 of 6 pass
- Checks failed: 5 checklist rows (1, 2, 6, 10, 14), caused by 4 distinct blocking issues
- Critical issues: 0
- Blocking (IMPORTANT) issues: 4
- Issues fixed in-place: 0 (fix_authorization: false)
- Axis lens status: AX-1 active (BUILD-REQUEST GOAL captured verbatim above); no goal drift found: the task keeps the options A/B/C/hybrid scope, the 10-section report, the no-live-deployment limit and the Phase 7 condensed copy.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Task file Steps 6.5, 6.6 (lines 303, 307, 311) versus `qa/qa-fix-log.md` and `qa/qa-fix-verification.md` on disk | Gate 3 uses the same file names as the validation-round files already in `qa/`; no item moves them. Overwrite destroys the A.10 evidence, Write on an existing unread file errors, and a stale PASS can be read by the Step 6.6 decision item. AX-3. | Add to Step 1.2 (before any other item) a Bash `mkdir -p .../qa/a10-task-validation/` and `mv` of `qa/qa-task-validation-*.md`, `qa/qa-fix-log.md`, `qa/qa-fix-verification.md`, `qa/qa-task-research-alignment-report.md` into it, and make Step 1.2's "no other files are created" wording allow it; or rename the Gate 3 outputs (for example `qa-fix-log-phase6.md`, `qa-fix-verification-phase6.md`) in lines 303, 307, 309 (qualitative name is already unique), 311 and Step 7.3. |
| 2 | IMPORTANT | Lines 219, 269, 311, 327, 343 (five identical halt strings; also the Step 3.4 text) | The "byte-exact" regression halt message has a comma after `X.Y`; the API-004 wire string (task-builder SKILL.md:1293; asserted with U+2014 in `tests/audit/test_regression_halt_pass1_fail2.py`) has an em-dash: `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` A downstream matcher on the wire string will miss the task's text. AX-2. | In all five places replace `X.Y,` with `X.Y —` (em-dash with the surrounding spaces as in SKILL.md:1293), or drop the words "byte-exact" and state the string is a house variant; the first option matches the skill rule the lens asks for. |
| 3 | IMPORTANT | Line 187 (Step 2.1, agent 02 prompt, question 3 and the verification clause) | Says the expected search result for Python `gh` calls under `src/superclaude` AND `tests/` is "none found". True for `src/superclaude`; false for `tests/pr_submit/` (`test_conflict_e2e.py:104,167` builds `["gh", *args]` and runs it via `subprocess.run` against a PATH stub; four other test files write `gh` stubs). A "none found" research answer would be wrong and would then fail the Gate 1 and Gate 3 evidence checks or, worse, enter the report. AX-1 (cited fact out of sync with source). | Re-scope the expectation: "no Python module under `src/superclaude` builds a `gh` call (expected: none found); for `tests/`, report where tests build or stub `gh` (for example `tests/pr_submit/test_conflict_e2e.py` lines 104, 138-141, 167 use a PATH stub `gh` executable) and say that this stub approach is the repo's mocking pattern". Keep the statement "no Python `gh` wrapper exists" (still true) in Section 2.3/8 requirements. |
| 4 | IMPORTANT | Phase 7 (no item) and Step 7.3 | Nothing stages `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/` (git status: untracked); convention requires `git add .dev/tasks` and never leaving it untracked. AX-3. | Add a Step 7.x item before the final frontmatter update: run `git add .dev/tasks` (stage only, no commit) and record it in the Execution Log; or state in the task file that the orchestrator stages after completion. Note `.dev/brainstorms/` is not covered by the rule; leave it to the orchestrator. |

Minor notes (never fail the review, not rechecked):
- M1 (AX-4): decision-item wording "IF the consolidated findings listed no blocking finding, OR both verification reports are PASS, record PASS" (lines 219, 269, 311, 327, 343) also matches when the gate had no blocking finding but a verification agent reports FAIL; the second branch ("either report FAIL") then overlaps. State that a FAIL verification report always selects the FAIL branch.
- M2: Step 3.1 runs the evidence rf-qa in the same parallel message as the analyst while telling it to read the analyst report "if it exists"; nondeterministic but harmless (it falls back to full verification).
- M3: the task file is 335 KB (about 85K tokens); an executor that loads it whole spends a large share of its context. Items are self-contained, so reading by item is workable.
- M4: Gate 2 structure prompt (line 251) says "12-item checklist" and then lists 13 items.
- M5: the embedded addendum text contains the phrase "pending owner decision" (inside a prohibition); synthesis agents copying it verbatim would trip the "appears nowhere" checks. Tell the agents to paraphrase.
- M6: Step 7.2 lists eight mandatory sections for a copy capped at about 3500 words; feasible, but the "condense further" fallback could conflict with the mandatory sections; say which sections shrink first.

## Actions Taken
None (fix_authorization: false; task file not modified).

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)
See ## Self-Audit below.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS (`qa/qa-fix-verification.md`, "VERDICT PASS", all six blocking findings I-1..I-5 and B-1 fixed) for: section numbering and Step/Phase structure, frontmatter shape (35 keys), item structure (64 `- [ ]` items, completion gates), TB-Add structural checks, byte-identical embedded addenda block in the six prompts, and the Phase 1-7 item counts. I did not re-run these.
- Relied on the B2 and phase-structure lens PASS rows in `qa/qa-task-validation-consolidated.md` for self-containment of items and for the cycle-2 sub-step naming scheme.

**(b) Independent semantic checks (at least 1 required, INV-019), where the producer PASS was insufficient:**
- Output-name collision between the A.10 validation-round files and Gate 3 outputs: the structural verdict never looks at what is already on disk in `qa/`. Found by `ls qa/` plus `grep -c` on the task file for any move or rename instruction (0 hits), then reading `qa-fix-log.md` and `qa-fix-verification.md` headers (they are the validation-round files).
- Halt wire string: structure PASS only checks that the string is present. I compared it with `~/.claude/skills/task-builder/SKILL.md:1293` and the `tests/audit/test_regression_halt_pass1_fail2.py` header and found the em-dash/comma mismatch.
- gh-wrapper "none found" claim: the structural PASS cannot judge a factual presupposition. I grepped `src/superclaude` and `tests/` for `"gh"` argv construction and read `tests/pr_submit/test_conflict_e2e.py:98-108,130-170`, which refuted the `tests/` half.
- Convention compliance: `git status --short` and `grep -c "git add|staged|staging"` on the task file and tech-research SKILL.md showed no staging step anywhere.
- Anchor drift (AX-1): re-read about 45 cited file:line anchors from the agent prompts (E1); all current. The A.10.25 alignment edits (`ci.py` correction, no-inbound relaxation, intended-owner filter) are consistent with `codebase-context.md` line 21 and `research-notes.md` line 30.

## Recommendations
- Fix issues 1-4 in the task file (all small text edits plus one new `git add` item), then re-verify only those four. Minor notes need no action.
- This is the first qualitative review of this lens: no prior cycle, so cycle count for this gate is 1 of at most 3 reviews.

## Confidence Gate
- **Confidence:** Verified: 15/15 checklist rows | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (10 rows PASS, 5 rows FAIL with tool evidence; verdict is FAIL because of the blocking issues, not because of low confidence)
- **Tool engagement:** Read: 12 (task file in 9 chunks, BUILD-REQUEST, producer reports, template) | Grep: 21 | Glob: 0 | Bash: 14 (existence loop over 40 paths, anchor reads, tests/gh search). Read+Grep+Glob = 33 is at least the 15 checklist items.

## QA Complete

VERDICT: FAIL
