# Command nuance: /sc:test

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Focus: how it differs from simply running the related test; flags by complexity; footprint a checker could see (CI via `.github` Actions is the validation gate per the repo `CLAUDE.md`).

Path keys: `cmd` = `/home/coder/.claude/commands/sc/test.md`; `HWW` = `/home/coder/.claude/HOW-WE-WORK.md`; `CVP` = `command-value-by-phase.md`; `VO` = `validation-oneoff-sc-task-vs-sc-implement.md`.

## 1. Status and role

- Does: "Execute tests with coverage analysis and automated quality reporting" (cmd:3). Runs the project's existing runner, reports coverage and failure analysis; does not write tests (cmd:98-106). Standalone and invokable; NOT retired. Frontmatter: `category: utility`, `complexity: enhanced`, `mcp-servers: [playwright]`, `personas: [qa-specialist]` (cmd:4-7).
- Phase: Implement (verify), also Bug fix step 3a (HWW:131, 311). Backing protocol skill `~/.claude/skills/sc-test-protocol/` DOES NOT EXIST (`ls` returned "No such file or directory"). Expected, not a defect: HWW:232 says commands whose file names no skill, "for example `/sc:help`, `/sc:explain`, `/sc:test`", run from their own file. The only similarly named skill, `sc-validate-tests-protocol`, tests `/sc:task` tier rules and is unrelated (HWW:285).
- Overlaps: the plain test runner (the real alternative), test steps inside `/task` (HWW:18, 81) and `/sc:implement` (VO E3.5), `/sc:troubleshoot --type test` (HWW:125). Does not call or depend on `/sc:task` or `/sc:tasklist`. No skill calls `/sc:test` programmatically: every hit is a suggested next step in prose (`implement.md:140,144`; `sc-implement-protocol/SKILL.md:159`; `spawn.md:210`; `cleanup-audit.md:119`; `sc-cleanup-audit-protocol/SKILL.md:171`).

## 2. Flags

Usage line, the only flag definition anywhere: `/sc:test [target] [--type unit|integration|e2e|all] [--coverage] [--watch] [--fix]` (cmd:22). There is no protocol skill, so cmd is the complete flag source. The command file defines no flag defaults; the one default behaviour is inferred from the "Basic Test Execution" example.

| Flag / arg | Values | Default | What it changes (cited) | Worth using when | Avoid when |
|---|---|---|---|---|---|
| `target` (positional) | path to a file or directory | whole project (inferred from example cmd:66-68, "Discovers and runs all tests") | Scopes discovery to that path, e.g. `src/components` (cmd:74). Guide examples pass a test file or folder (HWW:131, 172) | Always, when the related test or folder is known up front. It is what makes this equivalent to "run the related test" | Never omit it on a repo with a slow suite: the no-target form runs everything (cmd:66-68) |
| `--type` | `unit` \| `integration` \| `e2e` \| `all` | not stated; no-flag example implies all (cmd:66-68) | Narrows the category (cmd:22, 74). `e2e` auto-activates Playwright MCP for browser testing, cross-browser and visual checks (cmd:43, 81-84) | `unit` for a fast loop on one module. `e2e` only when a browser-facing product exists. HWW:172 says add it "to narrow" | `e2e` where there is no UI or Playwright is not wired (UI presence in this repo is UNVERIFIED, CVP U15). Do not pass it just to look thorough |
| `--coverage` | switch | off; but the no-flag example already "generates pass/fail summary and basic coverage" (cmd:68), while `--coverage` gives "detailed coverage metrics" (cmd:75) | Adds a coverage report and metrics (cmd:30, 36, 52, 75) | Routing table lists it as the mandatory flag for bug step 3a (HWW:311) and for the `tests` row (HWW:319). Use when someone will read the numbers | When the repo has no coverage tooling: none of `pytest.ini`, `tox.ini`, `package.json`, `Makefile`, `.coveragerc` exists at this repo's root (checked), and the main tests are bash scripts. What it would do here is UNVERIFIED |
| `--watch` | switch | off | Continuous run on file changes (cmd:39, 58-59, 86-90) | Interactive local dev loop only | Any unattended or scripted session (a watch never returns). Never in a pipeline step. Behaviour in a non-interactive session is UNVERIFIED |
| `--fix` | switch | off | "automatic simple failure fixes" (cmd:89-90) | Rarely: trivial failures during a watch loop | Whenever the diff must stay reviewable or a ledger-style record is wanted. The file does not say WHAT it edits (source or tests). Its own Boundaries say it will not "make destructive changes to test files without explicit permission" and will not modify test framework configuration (cmd:106, 104): the flag and the boundary are not reconciled |

Does not exist (absent from cmd; do not assume): `--depth` (belongs to `/sc:workflow`, `/sc:troubleshoot`, etc., VO E1.4), `--spec`, `--tasklist`, `--resume`, `--ledger`, `--framework`, `--parallel`, `--no-coverage`, `--compliance`, `--output`. Test generation is explicitly out of scope: "Will Not: Generate test cases" (cmd:104); use `bmad-qa-generate-e2e-tests` or the spec/task file instead (HWW:173).

## 3. Scope x complexity matrix

Plain statement: the command itself does not vary by task complexity. It has no tiers, no `--depth`, and no complexity formula (no TCS use; cmd has no such text). What varies is the SIZE OF THE TEST TARGET, so the bands below are JUDGMENT bands on test-target signals (the brief allows proposed thresholds when labelled; no file gives one).

Band definitions (all (J)):
- LOW: one named test file or test command, known before starting (HWW:16, 131).
- MEDIUM: a test folder or module, still named up front (HWW:172 example `tests/billing/`), no special infrastructure.
- HIGH: the whole suite, tests spanning subsystems, e2e/browser tests, or tests that need infrastructure. In THIS repo that means the contract suite, which the AIDev02 gate builds an image for and runs inside it (`.github/workflows/coder-ci-aidev02-contract.yml:1`, 1158-1163).

Reasons shared by the cells: `/task` already runs tests and an audit (HWW:18, 81; "do not re-run ... the tests yourself", HWW:81; "Do not repeat a skill's own checks", HWW:226). `/sc:implement` runs tests only if they exist, scoped to the task's files, and never as the pass/fail (VO E3.5; `implement.md:128`), and tells the user `/sc:test` is "Optional ... not gates" (`implement.md:140`). The repo gate is CI (repo `CLAUDE.md` Development Practices). So no cell is REQUIRED for the COMMAND. What is mandatory is the ACTIVITY "run the related test" (HWW:16, 119, 311), by any means.

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | WORTH IT (J): `/sc:test <test file>`; the plain runner is equally valid. Proposed one-off minimum is a plain edit plus the related test (VO verdict item 2; PROPOSED, not confirmed by Ryan) | OPTIONAL (J): `/sc:test <folder> --type unit` | N/A (J): HWW:22 hard limit (>5 edits or >1 source file) moves the work out of a one-off |
| B bug fix | WORTH IT: `/sc:test <test path> --coverage`. Guide names exactly this as step 3a for a small fix (HWW:131, 311) | OPTIONAL (J): the `/sc:workflow` + `/sc:implement` route runs tests as it goes (HWW:117); add `/sc:test <folder>` only for a regression sweep beyond the task's files | SKIP (J): `/task-builder` + `/task` runs tests and a final audit (HWW:18, 81, 133) |
| S single story | OPTIONAL (J): `/sc:implement` ran scoped tests (HWW:117, 119) | WORTH IT (J): `/sc:test <module folder> --type unit\|integration` once before commit, because `/sc:implement`'s tests are scoped to the task's files and not a pass/fail (VO E3.5) | OPTIONAL (J): story run through `/task`, whose end-of-run tests apply (HWW:18); add only for a coverage figure (`--coverage`) |
| F multi-story feature | SKIP (J): HWW:81, 226 | SKIP (J): same | OPTIONAL (J): one `/sc:test --type all --coverage` after the last phase if coverage numbers are wanted and a local runner exists; otherwise CI |
| R multi-feature release | OPTIONAL (J): few features, CI covers it | WORTH IT (J): `/sc:test --type all` as a pre-push integration signal across features | WORTH IT (J): `--type all --coverage`, plus `--type e2e` only if a UI exists. Pre-push signal only: CI remains the gate |
| N new product | N/A (J): a new product is not LOW | OPTIONAL (J): `/task` runs tests per phase (HWW:18, 81) | OPTIONAL (J): `--type e2e` if a UI product exists (UNVERIFIED, CVP U15) |

R re-rating under the multi-feature definition (brief ruling 2): the rating stays WORTH IT, but the reason changes. The old reading ("a release assembles and ships work already built", CVP:139) had `/sc:test` valued as a final check of assembled work; under the new definition the value is cross-feature regression, which is a stronger case. See section 7.

## 4. Choose this or the neighbour

| Neighbour | Decision rule (signals) | Cites |
|---|---|---|
| Plain test runner (`bash <script>`, `pytest <file>`, etc.) | Use the plain runner when the related test is one named file and its run command is known (LOW). It satisfies "run the related test" (HWW:16, 304). Use `/sc:test` when you need ANY of: coverage figures, framework auto-detection because the runner is unknown, a written failure analysis, or Playwright e2e. What `/sc:test` adds over the plain runner is auto-detect, coverage report, failure analysis with recommendations, e2e via Playwright (cmd:27-31, 35-38, 43). What it does NOT add: no spec trace, no acceptance criteria, no independent reviewer, no ledger, no named output file | cmd:25-39, 98-100; HWW:16 |
| Tests inside `/task` or `/sc:implement` | If the work went through `/task`, do not run `/sc:test` again for the same scope (HWW:81, 226). If it went through `/sc:implement`, `/sc:test` is the only step that gives a whole-folder pass/fail, because implement's test run is scoped and not a verdict (VO E3.5) | HWW:81, 119, 226; `implement.md:128,140` |
| `/sc:troubleshoot --type test` | Failure obvious from the output and the fix is small: stay in `/sc:test`. Failure unexplained, intermittent, or spanning areas: switch to `/sc:troubleshoot ... --type test` (it diagnoses and writes `REPORT.md`; `/sc:test` only "analyses") | HWW:124-125, 311; CVP:175 |
| `bmad-qa-generate-e2e-tests` | Needs new tests written: use the generator. `/sc:test` only runs existing suites (cmd:98, 104) | cmd:98, 104; CVP:151 |
| `/sc:validate-tests` | Name collision only: it tests `/sc:task` tier rules, a contributor tool. Never a substitute | HWW:285 |
| CI (`.github` Actions) | CI is the validation gate; one-off local validation scripts are discouraged. A local `/sc:test` result is a convenience signal and never replaces the CI result. In this repo most validation is bash contract tests that run in a built image, so a local run may not be able to reproduce the gate at all | repo `CLAUDE.md` "Development Practices"; `PROJECT_INDEX.md` Pipeline; `coder-ci-aidev02-contract.yml:1,1158-1163` |

## 5. What a scheduled checker can see

Footprint of `/sc:test` itself: none defined; transcript only.

| Item | Finding | Cite |
|---|---|---|
| Ledger / frontmatter / task-file entry | None. No ledger, no `.dev/` folder, no frontmatter key is defined for this command | cmd (whole file) |
| Report file | The command lists the Write tool for "Coverage reports and test summaries" but gives no path, name, or format | cmd:52 |
| Guide's view | Routing row `tests` has `changes_files: no`, meaning it only answers or saves a report under `.dev/`, `claudedocs/` or the tool's own output folder | HWW:297, 319 |
| Observed in this repo (2026-10-27) | No test or coverage output found: `.gitignore` has no coverage/junit/test-results entries; `claudedocs/` (11 entries) has no file with "test" or "coverage" in its name; no `.dev/test*`, `.dev/coverage*`, `coverage/`, `htmlcov/` | `ls`, `grep` on the worktree |
| Runner side effects | Depends on the runner chosen (coverage data files, caches). Not observed: UNVERIFIED | - |
| In-session text | A pass/fail summary and recommendations printed to the transcript (cmd:28-31, 63-69). Not machine-readable | cmd |

Better evidence for a checker that wants to know "were the tests run":

- CI check results on the PR. The gate workflows (`coder-template-main`, `coder-ci-aidev02-contract`, `coder-ci-validate`) run on push and PR (`PROJECT_INDEX.md` Entry points and Pipeline; `coder-ci-aidev02-contract.yml:1`). Per repo `CLAUDE.md`, CI is the validation gate, so a green check is stronger evidence than any trace of `/sc:test`.
- Test files in the diff (`.github/contract-tests/test-*.sh`, `ci-timing/test_*.py`) for changes that should come with a test.
- For work that went through `/sc:implement`: its ledger `extras=...test:...` field records a scoped test run if one existed (`refs/ledger.md` as quoted in VO "Footprint" table). For `/task`: the Task Log in the task file (HWW:18, 89).

## 6. Expected-step rule

- Count the ACTIVITY, not the command: "related test run, or CI green on the PR" is expected for T, B, and S whenever source changed (HWW:16, 119, 311). Never flag a missing `/sc:test` invocation as a skipped step at any scope or complexity, because plain runners, `/task`, `/sc:implement` and CI all satisfy the activity.
- The only place the guide names the command as a step is B LOW (small fix), `/sc:test <test path> --coverage` (HWW:131, 311). A checker may accept either that or an equivalent plain run there; it cannot tell them apart, since `/sc:test` leaves no footprint. Absence is fine for F (tests are inside `/task`, HWW:81), for all N, and for S/B when a plan executor ran.

## 7. Proposed changes to command-value-by-phase.md

Proposals only; that file was not edited. Line numbers are as read on 2026-10-27.

| # | Where | Current text | Proposed text |
|---|---|---|---|
| P1 | CVP:150, 2.4 row `/sc:test`, S cell | S = WORTH IT | S = OPTIONAL (J). WORTH IT only at MEDIUM test-target size (a module folder, once before commit), because `/sc:implement` and `/task` already run tests (HWW:81, 117, 226; VO E3.5) |
| P2 | CVP:150, same row, T / B / F / R / N cells | T WORTH IT, B WORTH IT, F OPTIONAL, R WORTH IT, N OPTIONAL | Ratings unchanged. Add a complexity qualifier in Notes: T WORTH IT at LOW only; B WORTH IT at LOW (guide step 3a), SKIP at HIGH; F SKIP at LOW/MEDIUM, OPTIONAL at HIGH. R: rating unchanged, rationale re-based (see P5) |
| P3 | CVP:150, same row, Notes | "Running the related test is mandatory in the guide (levels 2, 3, bug route 3a); this command is one way. F: `/task` runs tests itself. Does not write tests. Also in Bug-fix phase" | "The ACTIVITY (run the related test) is mandatory in the guide (levels 2, 3, bug route 3a); this command is one way, not a gate: `implement.md:140` calls it optional, CI is the gate (repo `CLAUDE.md`). Flags: `[target] [--type unit\|integration\|e2e\|all] [--coverage] [--watch] [--fix]` (`test.md:22`); no `--depth`. Does not write tests (`test.md:104`). No backing protocol skill (`sc-test-protocol` absent; expected, HWW:232). Leaves no file footprint. Guide names it only in bug step 3a with `--coverage` (HWW:311). Avoid `--watch` in unattended runs; `--fix` is undefined (see section 8)" |
| P4 | CVP:180 | "`/sc:test` (reproduce, then confirm; 2.4)" | "`/sc:test` (confirm the fix after a failing test was written and the fix made, HWW:131, 311; 2.4)". The command file does not reproduce bugs; it runs existing tests (`test.md:98`) |
| P5 | CVP:139 and Section 4 Release row (CVP:256) | R reading: "a release assembles and ships work already built ... unless they check the assembled result"; additions list "`/sc:test` full run" | Under the multi-feature release definition (brief ruling 2): `/sc:test --type all [--coverage]` stays WORTH IT at MEDIUM and HIGH as a cross-feature regression signal before push, labelled "pre-push signal; CI is the gate". Rating did not change; the reason did. In this repo a full local run may not reproduce the gate, because the contract suite runs inside a built image (`coder-ci-aidev02-contract.yml:1,1158-1163`) |
| P6 | CVP:253 (Bug fix) | step 3 "run the test"; additions "`/sc:test`, `/code-review`" | Step 3: "run the test (`/sc:test <test path> --coverage` per HWW:131, 311, or the plain runner)". Drop `/sc:test` from the additions because it is now in the path |
| P7 | CVP:254 (Single story) and CVP:252 (One-off) | additions include `/sc:test` | S: "`/sc:test <module>` at MEDIUM complexity only". T: unchanged (WORTH IT at LOW; the proposed one-off minimum, plain edit plus related test, is still PROPOSED per VO) |
| P8 | CVP:276 footprint row | "`/code-review`, `/security-review`, `/sc:test`, ... No file footprint stated anywhere I read" | Split out `/sc:test`: "none defined. `test.md:52` lists a Write for 'coverage reports and test summaries' with no path; routing row `tests` is `changes_files: no` (HWW:319). Nothing found in `claudedocs/`, `.gitignore`, `.dev/` on 2026-10-27. A checker should use CI check status and test files in the diff instead" |
| P9 | CVP:281 (Unverified preamble) | "`/sc:test` ... I read only the usage and flag lines (grep)" | `/sc:test` file read in full (107 lines) for this nuance pass; no protocol skill exists |

## 8. Unverified items

| # | Item | Why unverified | What would resolve it |
|---|---|---|---|
| U1 | What `/sc:test` auto-detects and runs in THIS repo (bash contract tests, `ci-timing/test_*.py`, Terraform). No root runner config exists (`pytest.ini`, `tox.ini`, `package.json`, `Makefile`, `.coveragerc` all absent) | Command not run (brief rule: read-only) | A supervised run on a scratch branch |
| U2 | Default of `--type` when omitted | Only implied by the example (cmd:66-68) | Run it, or find the intended protocol |
| U3 | What `--fix` edits (source vs tests) and how it squares with "will not make destructive changes to test files without explicit permission" (cmd:106) | File says only "automatic simple failure fixes" (cmd:90) | Run it, or ask the command's author |
| U4 | Where "coverage reports and test summaries" are written (cmd:52) | No path given; none seen in repo | Run once and look |
| U5 | Whether `--coverage` works for bash tests; any coverage tool installed here | No coverage config found at root; tool availability not probed | Probe tools; run once |
| U6 | `--watch` behaviour in a non-interactive or agent session | Not stated | Run once |
| U7 | Whether the `personas: [qa-specialist]` and `mcp-servers: [playwright]` frontmatter keys actually load anything beyond the prose in cmd:41-45 | Frontmatter semantics not defined in any file read | Read the command loader or run once |
| U8 | Whether any CI workflow runs the four `ci-timing/test_*.py` files. A grep of `.github/workflows/*.yml` for `pytest`/`unittest` found nothing, but a script could call them indirectly | Grep only, workflows not read in full | Read the workflows that mention `ci-timing` |
| U9 | Whether the contract suite can run outside the image | Only workflow lines 1 and 1158-1163 read, not the whole workflow | Read `coder-ci-aidev02-contract.yml` and individual test headers |
| U10 | Whether `bmad-dev-story` / `bmad-quick-dev` run tests, so whether `/sc:test` duplicates them in the BMad lane | Those skills not read | Read both SKILL.md files |
| U11 | Whether `HOW-WE-WORK.md` on other engineers' machines matches this one (HWW:311 `--coverage` mandatory flag) | Home-directory file, not shared (CVP U17) | Compare `~/.claude` across engineers |
| U12 | The routing table's claim that it is "checked by tests" (HWW:297) and whether those tests enforce `--coverage` on the `bug` row | Not located (CVP U18) | Find the IronClaude tests |
| U13 | RESOLVED, not open: `implement.md:128` "Treat lint or tests as the pass/fail" sits under the "Will Not" heading at `implement.md:124`, and "Run lint/typecheck/tests when present and record them as extras" is at `implement.md:122` | Read lines 116-131 | - |
