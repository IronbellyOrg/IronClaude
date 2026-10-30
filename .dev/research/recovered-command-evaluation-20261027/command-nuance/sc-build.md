# Command nuance: /sc:build

Written 2026-10-27. Brief: `command-nuance/_brief.md`. Focus: value in this repo given CI in `.github` Actions is the validation gate (`CLAUDE.md`, Development Practices); flags by complexity.

## 1. Status and role

- Does: "Build, compile, and package projects with intelligent error handling and optimization" (`~/.claude/commands/sc/build.md:3`). Phase: Implement (verify side). Standalone-invokable, NOT retired. Playwright MCP and `devops-engineer` persona are declared (`build.md:6-7`).
- **Backing protocol skill does not exist.** `ls /home/coder/.claude/skills/sc-build-protocol/` returned "No such file or directory", and no `sc-*build*` skill exists in `~/.claude/skills/`. Behaviour is the 108-line command file only; nothing is defined beyond it.
- Overlaps: `/sc:test` (runs tests), `/sc:troubleshoot --type build` (`troubleshoot.md:8,50`, diagnoses a broken build), `/task` (runs tests itself), and the CI workflows under `.github/workflows/`. `HOW-WE-WORK.md:269` lists it only under "installed but no workflow above routes to them": "Build or package the project." `sc-cli-portify-protocol/SKILL.md:584` lists it as an optional follow-up ("Build and compile after generating").

## 2. Flags

Usage line: `/sc:build [target] [--type dev|prod|test] [--clean] [--optimize] [--verbose]` (`build.md:22`). The command file defines no defaults and no flag semantics beyond the example comments; there is no protocol skill to define them.

| Flag / arg | Values | Default | What it changes (cited) | Worth using | Avoid |
|---|---|---|---|---|---|
| `[target]` | a component name, e.g. `frontend` | whole project (`build.md:66-68`) | "Builds specific project component with detailed output" (`build.md:82-84`) | When one buildable component exists and the others are slow | Never useful here for a Terraform-only change: this repo has no component to name (see section 8, U3) |
| `--type` | `dev`, `prod`, `test` | not stated; no-flag example uses "default configuration" (`build.md:66-68`) | Selects environment-specific config and optimization (`build.md:56`) | `--type test` before a manual test run if a test build target exists | `--type prod` in this repo: nothing here produces a prod bundle locally |
| `--clean` | boolean | off | "Clean production build" (`build.md:74-76`); exact meaning (wipe output dir? caches?) not defined | After a dependency or toolchain change, when a stale cache is the suspect | Routine runs: slower, and the command may not own the directory it cleans (UNVERIFIED) |
| `--optimize` | boolean | off | "Minification, tree-shaking, and deployment preparation" (`build.md:76`) | A JS/bundled front end where size matters | Anything not bundled. Terraform, shell and Docker work in this repo have no minify step |
| `--verbose` | boolean | off | "Real-time progress monitoring and diagnostic information" (`build.md:84`) | A build that fails with a thin message | Normal runs: floods the transcript |
| `--validate` | not defined | n/a | Appears ONLY in the example at `build.md:90` ("Development build with Playwright validation"). It is NOT in the usage line (`build.md:22`). Treat as undocumented. | Not recommended | Always, until the file defines it |

Does not exist (people may assume):

- `--depth` (that is `/sc:workflow`, `/sc:reflect`, `/sc:troubleshoot`; `/sc:build` has none).
- `--fix`, `--dry-run`, `--output-dir`, `--report-path`: not in `build.md`. The report location is undefined: "Write: Build reports and deployment documentation" (`build.md:52`) names no path.
- Any flag that installs dependencies or edits build config: banned, "Will Not: Modify build system configuration or create new build scripts; Install missing build dependencies or development tools; Execute deployment operations beyond artifact preparation" (`build.md:103-107`).

## 3. Scope x complexity matrix

**Does the command vary by complexity? No.** Its flags (section 2) pick an environment and an optimization level, not a depth of process; there is no `--depth` and no complexity tier in the file (`build.md:5` "complexity: enhanced" is a catalogue label, not a TCS value). What varies is whether a local build entry point exists and can run. So the bands below are defined by build-relevance signals (all JUDGMENT, marked `(J)` as a set), not by the TCS formula (`~/.claude/skills/task-builder/SKILL.md:2422-2433`, which scores task files, not builds).

Repo facts behind the cells:

- No `package.json`, `Makefile`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml` or `build.gradle` anywhere outside `.git`, `_bmad` and `node_modules` (find, 2026-10-27). Only Dockerfiles: `templates/VSCode-AIDev02/Dockerfile.coder`, `templates/VSCode-AIDev02/collector/Dockerfile`, and AIDev01 files.
- The image is built in CI: `docker buildx build ... --file "$TEMPLATE_DIR/Dockerfile.coder"` (`.github/workflows/coder-ci-aidev02-contract.yml:696`, also `:939`).
- The one real package build, `orca-build/build-deb.sh`, refuses to run outside Actions: `[[ ${GITHUB_ACTIONS:-} == true && ${GITHUB_RUN_ID:-} =~ ^[0-9]+$ ... ]]` (`orca-build/build-deb.sh:22`), header "Run only in the separately authorized Actions build" (`:2`), needs Linux x86_64 and Node v24 (`:24-25`). CI runs it in job `orca_derivative`, `workflow_dispatch` only, on `[self-hosted, big]` (`coder-ci-aidev02-contract.yml:219-221,308`).
- Project rule: "Validation should be done via the .github actions. One off validation scripts should be avoided" (`CLAUDE.md`, Development Practices).

Band definitions (this repo, J):

| Band | Signal |
|---|---|
| LOW | Change touches no build input: docs, markdown, shell under `scripts/`, Terraform `.tf`, contract-test scripts. |
| MEDIUM | Change touches an input to the image or package build (`Dockerfile.coder`, `orca-build/*`), so CI will rebuild. |
| HIGH | Change to the build itself: base image or apt pins, toolchain versions, `build-deb.sh` patches or pins. A build failure is the main risk. |

| Scope | LOW | MEDIUM | HIGH |
|---|---|---|---|
| T one-off | SKIP (J) | SKIP (J): CI builds it | N/A (J): more than one source file or more than 5 edits is level 3+ (`HOW-WE-WORK.md:22`) |
| B bug fix | SKIP (J) | SKIP (J): use `/sc:troubleshoot --type build` for a red build | OPTIONAL (J), only to reproduce locally, `--type dev --verbose`; likely cannot run here (`build-deb.sh:22`) |
| S single story | SKIP (J) | SKIP (J): push and let CI be the gate | OPTIONAL (J), same as B |
| F multi-story feature | SKIP (J) | OPTIONAL (J), `--type test` only if a local build target exists | OPTIONAL (J), `--verbose`; CI remains the gate |
| R multi-feature release | SKIP (J) | OPTIONAL (J) | OPTIONAL (J): the image build and the Orca package build and publish are CI jobs (`coder-ci-aidev02-contract.yml:308,370-438,696`) |
| N new product | SKIP (J) | OPTIONAL (J) | WORTH IT (J), only after the product has a build config; the command will not create one (`build.md:105`) |

No cell is REQUIRED: no Ryan pipeline names it (brief ruling 5), no routing row routes to it (`HOW-WE-WORK.md:269`), and the project gate is CI. For a repo that does have a bundler and local build, T/B/S MEDIUM would move to WORTH IT (J) as a pre-push smoke build; that is not this repo.

## 4. Choose this or the neighbour

| Neighbour | Decision rule | Cite |
|---|---|---|
| CI (`.github` Actions) | In this repo CI wins unless a local build is genuinely runnable. Push the commit and read the workflow result; do not build locally to "pre-validate". Use `/sc:build` only if a local toolchain exists AND you need the error before pushing. | `CLAUDE.md` Development Practices; `build-deb.sh:22` |
| `/sc:troubleshoot --type build` | A build is already failing: use troubleshoot (diagnosis, evidence, `REPORT.md`). `/sc:build` runs a build and parses errors; it has no hypothesis testing. | `troubleshoot.md:8,42,50`; `build.md:57` |
| `/sc:test` | Tests, not packaging: use `/sc:test`. Running the related test is the mandatory check at levels 2 and 3. | `HOW-WE-WORK.md:170` (section 3.8) |
| `/task` | `/task` runs the tests itself at the end; no separate `/sc:build` step is needed inside a task file. | `HOW-WE-WORK.md` level 4 row |
| `bmad-quick-dev` / `bmad-dev-story` | Not alternatives; they implement code. A build step after them is optional on the same terms as above. | `command-value-by-phase.md` 2.4 |

## 5. What a scheduled checker can see

None, transcript only. The command file says it uses Write for "Build reports and deployment documentation" (`build.md:52`) but names no path, no frontmatter key and no ledger; there is no protocol skill that could define one. A checker could see only a Bash call to a build tool in the session transcript (UNVERIFIED, no run observed). The authoritative build evidence in this repo is the GitHub Actions run (for example job `orca_derivative`, `coder-ci-aidev02-contract.yml:219-221`), which this command does not produce.

## 6. Expected-step rule

Never count `/sc:build` as an expected step at any scope or complexity in this repo: it is in none of Ryan's pipelines (brief ruling 5) and the validation gate is CI (`CLAUDE.md`). Its absence is always fine; its presence is not a deviation and must not be accepted as a substitute for a green CI run or for the related test.

## 7. Proposed changes to command-value-by-phase.md

Row `/sc:build` in section 2.4 (line 152).

Current: `| /sc:build | Build, compile, and package projects ... | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | OPTIONAL | Guide: "Build or package the project". CLAUDE.md says validation goes through .github Actions; local build is a convenience, CI is the gate |`

Proposed (this repo, J): `| ... | SKIP | SKIP | SKIP | OPTIONAL | OPTIONAL | OPTIONAL | No backing protocol skill exists, so flags are only those on the usage line (--type, --clean, --optimize, --verbose, [target]); --validate appears only in an example. Never REQUIRED. In this repo the image and Orca package builds run only in CI (build-deb.sh:22), and no package.json/Makefile exists, so a local run is rarely possible. For a build failure use /sc:troubleshoot --type build. HIGH-complexity N (after a build config exists): WORTH IT (J) |`

Changes by cell:

| Cell | Current | Proposed | Why |
|---|---|---|---|
| S | OPTIONAL | SKIP (this repo) | CI is the gate; no local build target (`build-deb.sh:22`, find result) |
| T, B, F, N | SKIP, SKIP, OPTIONAL, OPTIONAL | unchanged | B is OPTIONAL only at HIGH complexity (matrix) |
| R | OPTIONAL | OPTIONAL, unchanged | Re-rated under "multi-feature release including implementation and push": the release build is a CI job, local build adds nothing the gate does not; rating holds |

Related note for the merge step (not this command's row): the 2.4 intro (line 139) reads R as "assembles and ships work already built at story or feature size", so build-the-code commands rate SKIP for R. Under the new R definition a multi-feature release includes its own implementation, so that sentence no longer holds; `/sc:implement`, `/task` and others rated SKIP in R on that reading need re-rating by their own agents.

Line 276 (footprint table): add `/sc:build` to the "No file footprint stated anywhere" row.

## 8. Unverified items

| # | Item | Resolve by |
|---|---|---|
| U1 | No protocol skill exists, so how `--type` resolves, what `--clean` deletes, where reports are written, and what "intelligent error handling" does are all undefined | Read a run, or author the skill |
| U2 | `--validate` is used in an example (`build.md:90`) but not in the usage line (`build.md:22`); whether it is parsed is unknown | Run once, or fix the file |
| U3 | Claim "no local build target": based on a find for common manifests across the repo (excluding `.git`, `_bmad`, `node_modules`); only Dockerfiles found. Orca upstream is cloned in CI, not in the repo (`coder-ci-aidev02-contract.yml:308` uses `orca-upstream`) | Ask the team |
| U4 | Whether engineers' workspaces have Docker and Terraform to run a local build (test-18 is named `docker-cli-presence`; not opened) | Read `.github/contract-tests/test-18-docker-cli-presence.sh` |
| U5 | Whether Playwright MCP auto-activation (`build.md:42`) does anything useful for a non-UI repo; whether any product here has a UI is open (`command-value-by-phase.md` U15) | Ask the team |
| U6 | Undefined report path is a risk under the repo's secrets rule (never write env captures to a tracked path; `CLAUDE.md`, Secrets discipline): a build report could land in a tracked folder. Not observed | Run once in a scratch worktree |
| U7 | Whether the team has ever run it: the only repo hit outside the brainstorm folder is `.specstory/history/2026-10-26_21-44-12Z-pasted-content-id-c492.md`, not opened | Read that file or search transcripts |
| U8 | Other workflows (`coder-ci-orca-boot.yml`, `coder-ci-orca-proof.yml`, `coder-ci-validate.yml`) were only grepped for build commands, not read in full; there may be other build steps | Read them |
