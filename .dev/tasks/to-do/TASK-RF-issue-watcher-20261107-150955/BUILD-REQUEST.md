# BUILD REQUEST

Source: user (direct /task-builder call, run as step 5 of the issue-331 chain)
Task Directory: .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/
TASK_ID: TASK-RF-issue-watcher-20261107-150955
TASK_FILE: .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
SPEC: docs/designs/issue-watcher.md

GOAL: Build an MDTM task file (template 02) that implements the GitHub issue watcher exactly as designed in `docs/designs/issue-watcher.md` (IronbellyOrg/IronClaude issue 331; the design was produced by /sc:design from the finalized spec `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md`). Deliverables the task must produce: the `superclaude issue-watch` Click package under `src/superclaude/cli/issue_watch/` (`__init__`, `runner`, `github`, `predicates`, `record`, `launch`, `audit`, `cycle`, `cli`), its two-line registration in `src/superclaude/cli/main.py`, the test suite under `tests/issue_watch/` (per-module unit tests, the cross-cutting tests of design section 12, fixtures under `fixtures/_assumed_shape/`, stubs written at test time), and the owner runbook `docs/designs/issue-watcher-setup.md`. Everything is tested with fakes or PATH stubs only; nothing is deployed, installed, scheduled or run live.

WHY: Issue 331 asks for an automated watcher that polls GitHub every 5 minutes for approved issues and starts `/sc:issue --claim <N>` in the owner's workspace. The owner decided option A (workspace-side poller), claim-only scope and an integer-only prompt (D1 to D3). This task builds the repo-side part that can be tested with mocks. The driving design is `docs/designs/issue-watcher.md`; where the design and research disagree, `research/06-gap-fill-decisions.md` wins (it supersedes research files 01 to 05 and research-notes.md).

TASK_ID_PREFIX: TASK-RF

TEMPLATE: 02 (read /home/coder/.claude/templates/workflow/02_mdtm_template_complex_task.md; the project copy `.claude/templates/workflow/` does not exist in this checkout; `src/superclaude/templates/workflow/02_...` is byte-identical)

QA_INTENSITY: standard

QA_GATE_REQUIREMENTS: PER_PHASE. Follow research/06 DF-08, Table 1.6 and the phase plan (Section 2): 10 phases P1 to P10; four intermediate gates (Gate A after P3, Gate B after P5, Gate C after P7, Gate D after P8), each 6 agents = 3 rf-qa + 3 rf-qa-qualitative with lens focus, report-only; then in P9 the Final M3 gate (7 agents = 3 rf-qa + 3 rf-qa-qualitative + 1 domain lens `rf-qa` for AC-1..AC-25 coverage) FIRST, then the M4 source-fidelity gate (3 agents: design fidelity D, spec fidelity S, cross-source contradiction D vs S); total 34 lens agents; fix agent (fix_authorization true, one only) and fix-verification agents follow a FAIL; max 2 fix cycles per gate with the retry-monotonicity halt guards (regression, then monotonicity) of the skill; no gate after P1 or P10. Every gate agent is its own `- [ ]` item with a fully embedded lens-specific prompt, adversarial stance, and report path under the task folder `qa/`. Serialized fix authorization (M3/I20). The M4 prompts carry the DEVIATION list of DF-40 (29 rows) so a listed departure is not reported as drift.

VALIDATION_REQUIREMENTS: use the exact gate commands of research/06 Table 1.2 (G-1 to G-11): `uv run pytest tests/issue_watch/ -v`; the named affected subset in G-2 (NOT the whole `make test`: DF-05); `make lint`; `uvx --offline ruff@0.15.20 format --check ...` and `check` (the pinned ruff; bare `uv run ruff` resolves to 0.17.3); the xdist run `uv run --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/ -q` (G-3, no SKIP); `make verify-deps`; `make sync-dev` then `make verify-sync`; G-7 Python-3.10 grep; G-8; G-9 (exactly five commands); G-10 (no change to pyproject.toml, Makefile, CI, `.claude/`); G-11 file hygiene.

TESTING_REQUIREMENTS: UNIT plus INTEGRATION (PATH-stub end-to-end test, crash injection C1 to C5 with five reruns each, concurrency, AST tests). Test files, fixtures, phases and expected results exactly per research/06 Section 2 and design sections 11, 12 and 17. No new pytest marker (`--strict-markers`), no new dependency, no hypothesis; Python 3.10 floor (no tomllib, no datetime.UTC); tests safe under xdist; no file written outside tmp_path.

EXECUTION_CONTEXT_INSTRUCTION: The builder MUST populate the `## Execution Context` section of the template: References (this GOAL verbatim, the WHY summary, related-doc ids for the design, spec-final, research/06), Source areas (named modules: the issue_watch package, the CLI registry, tests/issue_watch, the runbook; NO file:line paths), Key constraints (UV only; every gh call names `--repo IronbellyOrg/IronClaude`; only a validated integer reaches the launch prompt; nothing live; never stage or commit `.claude/`; stop rule for the checkpoint commit).

POST_REFLECT_GATE: ENABLED
  TASK_FILE: .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
  CLI_MODE: false (skill mode: `reflect_post_mode: skill`; frontmatter has NO start_commit and NO executor_model_class)
  SPEC_PATH: docs/designs/issue-watcher.md
  DEPTH: derive from the TCS FER of the skill over the finished MDTM file (O4 floor `standard`)
  BASE: per research/06 DF-07: the SHA written by the P10 item that runs `git rev-parse HEAD` immediately before the single local checkpoint commit item; the verbatim POST runner prompt uses `--diff <BASE SHA>..HEAD`. The task file carries exactly one local checkpoint commit item before the POST reflect item, no push item and no PR item; HALT on any commit or hook failure; never --no-verify; never git add -A; never .claude/. After the Done item a final `git add .dev/tasks` (staging only). The POST reflect item remains penultimate and the Done item last, both in the final phase P10 (anti-orphaning).

DOCUMENTATION STALENESS WARNINGS: The design (docs/designs/issue-watcher.md) is documentation. research/02 re-verified its citations: 45 CODE-VERIFIED, 3 CODE-CONTRADICTED (C14 collision claim false; C21 `--method GET` applies only to G3, G4, G7; the PATH-stub pattern lives in test_conflict_scripts.py:167-179), 8 UNVERIFIED (gh and Orca reply shapes, GraphQL schema, stderr substrings). UNVERIFIED shapes may enter the task only as `_assumed_shape` fixtures plus a short note, never as invented facts. Do NOT create items based on [CODE-CONTRADICTED] claims; use the corrections in research/02 and research/06.

RESEARCH DIR: .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/ (read ALL files)
- 01-cli-package-conventions.md: CLI layout, main.py registration text and position (after line 561), lint rules
- 02-integration-points-and-citation-check.md: reused code, citation verification, gaps G1 to G14
- 03-test-and-verification.md: tests, PATH-stub pattern, gates, xdist, ruff pin
- 04-template-and-examples.md: MDTM template 02 rules, two code-plus-tests examples
- 05-work-breakdown.md: module APIs, test list, FR/NFR map, traps
- 06-gap-fill-decisions.md: AUTHORITATIVE register DF-01 to DF-60, gate commands, crash table, stub protocol, GraphQL drafts, QA gate map, 10-phase plan, item-author lookup table, Round 2 and Round 3 change logs (supersedes 01 to 05 on conflict)

QUALITY GATE RESULTS (reports in qa/): the research gate ran three reviews; gap-fill rounds 1 and 2 (06) fixed all blocking findings except four small text defects found by the third review, which the coordinator approved fixing without a fourth review (the third exception of this work; recorded in 06 Round 3 change log): they are applied but unverified by a further review. Minor notes from the r3 reports are listed in the 06 Round 3 change log; fold them into the relevant items. The final reports: qa/*-r3.md where present (depth and completeness agents returned report text in their messages; the findings are summarized in 06).

OPEN QUESTIONS (document in the task file's Open Questions / Deviations section; do not make them the basis of an item): the 29 DEVIATION = yes rows of DF-40 with their D/S lines; owner questions Q1 to Q4 (design line 866) resolved by following the design's stated choice; spec-vs-design deviations X1 to X5 (DF-50); the tension between SKILL.md line 2140 and template I19 gate sizing (DF-08); the commit authority of DF-07 is inferred from the coordinator dispatch brief [SOURCE: coordinator brief].

REMAINING GAPS: UNVERIFIED gh/Orca shapes and GraphQL schema (fixtures only); Python 3.10 compatibility verified by reading (no 3.10 interpreter locally); pre-commit tools not installed locally (hygiene checked by G-11 and DF-58); full-suite `make test` runs in CI only.

CRITICAL: GRANULARITY: one checklist item per source file, per test file, per fixture group, per gate agent, per gate command run. Expect about 160 items. No batch items. Items follow B2 (context + action + output + verification + completion gate), cite the design sections and DF ids they implement (research/06 Section 3 lookup table gives the exact D/S line ranges), embed the exact gate commands, and bind every code reference to file:line evidence or an `<!-- evidence-absence: ... -->` comment (TB-Add-8). Agent-spawning items embed their full prompts. Parallel batches are stated explicitly. Placeholders (TBD/TODO/FIXME) are forbidden.

CRITICAL: QA GATE ENCODING per M3, M4, I19, I20, I21, I22 as stated in QA_GATE_REQUIREMENTS above. The M4 fidelity gate is mandatory (output exceeds 500 lines and transforms a design into code).

ESCALATION: you are a subagent with no team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, TaskList or broadcast TASK_READY. Return the task file path as your final output. If blocked, build the best file you can and note the gap in the Task Log; user-intent ambiguity goes to the Open Questions section.

INCREMENTAL TASK FILE WRITING (mandatory, never one shot): create the file first with frontmatter, title, overview, key objectives, prerequisites; then append each phase with one Edit per phase (for large phases one Edit per step group); then the Task Log section. Frontmatter: `reflect_post_mode: skill`, `spec_path: docs/designs/issue-watcher.md`, `qa_intensity: standard`, status "🟡 To Do", `task_type: static`.

STEPS: 1 read the template (PART 1 completely); 2 read ALL research files (06 first); 3 follow PART 1 rules; 4 populate Execution Context; 5 encode QA gates per above; 6 create the task file incrementally per PART 2; 7 return the task file path and the item count per phase.
