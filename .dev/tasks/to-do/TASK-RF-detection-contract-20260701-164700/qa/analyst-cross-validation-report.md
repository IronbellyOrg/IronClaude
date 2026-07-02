# Research Cross-Validation Report (Partition 1 of 1)

**Topic:** task-builder research for locked detection contract setup flow
**Date:** 2026-07-01
**Analysis type:** completeness-verification / cross-validation lens
**Scope:** assigned research files only
**Verdict:** PENDING

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports if additional partitions exist.]

---

## Files Analyzed

| # | File | Status | Scope contribution |
|---|------|--------|--------------------|
| 1 | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/01-file-inventory.md` | Complete | File inventory, expected package files, existing seams, likely tests |
| 2 | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/02-patterns-integration.md` | Complete | Integration seams, pr-submit arming gate, reflect CLI command-shape recommendation, source-of-truth rules |
| 3 | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/03-validation-tests.md` | Complete | Acceptance-aligned tests, side-effect guards, validation commands |
| 4 | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/research/04-template-examples.md` | Complete | MDTM template constraints, QA gate pattern, post-reflect wrapper conventions |

## Cross-File Consistency Matrix

| Topic | 01 Inventory | 02 Patterns | 03 Validation | 04 Template | Consistency |
|-------|--------------|-------------|---------------|-------------|-------------|
| New package location | `src/superclaude/pr_submit/contract_setup/` (`01`:21-35, 140-145) | Implied helper/reflect status consumes existing `DetectionContract`; docs may change (`02`:40-57, 77-84) | "new shared helper under `src/superclaude/pr_submit/`" and test files (`03`:40-137, 217-219) | Not applicable | CONSISTENT enough; 03 is less specific but not conflicting |
| Existing arm gate preserved | Preserve `DetectionContract.for_arming()` and fail-closed semantics (`01`:35-46, 107-110) | Arm gate is Wave 1 and must halt before Monitor side effects (`02`:13-25, 48-57) | Existing T-210/local override tests remain regression anchors (`03`:19-32, 170-178) | Not applicable | CONSISTENT |
| Reflect readiness surface | Likely new Click subcommand in `commands.py` (`01`:75-88, 101-119) | Recommends `superclaude reflect contract-status` sibling subcommand (`02`:5-10, 40-47) | Tests both flag-on-`run` option and tasklist-free behavior; names `--contract-status`, `--validate`, `--repo`, `--pr` (`03`:33-39, 153-168) | Post-reflect wrapper remains `superclaude reflect run <ABS_TASKLIST> --depth deep --fix --promote` (`04`:36-42, 66) | CONFLICT: command-shape is not unified |
| No-side-effect statement | No arm/push/reply/resolve/retrigger; no monitor side effects (`01`:51-66, 111-119) | Recommended exact text includes no monitor, no poll/push/reply/resolve/retrigger/resume (`02`:59-75) | Required substring includes "No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed." (`03`:138-151) | Not applicable | DIVERGENT wording/scope |
| Test placement | Mostly `tests/pr_submit/test_contract_setup_*.py`; optional reflect-side test (`01`:101-119) | Exact halt text tests in `test_detection_contract.py`, `test_monitor_arm.py`, `test_cli_smoke.py` (`02`:27-39, 71-75) | New dedicated modules plus `tests/cli/reflect/test_contract_status_cli.py` (`03`:40-168) | MDTM tasks should use phase handoffs and QA gates (`04`:27-35) | PARTIAL CONFLICT: multiple competing reflect test locations and whether to extend existing vs create dedicated modules |
| Validation commands | No commands listed | Not listed | UV-only pytest/ruff/sync commands (`03`:179-215) | UV-only included as task constraint (`04`:59-67) | CONSISTENT |
| `.claude/` treatment | New Python modules under `src`; no `.claude/` edits required (`01`:140-145) | If docs change, edit `src/...` first and sync; do not edit/stage `.claude/` (`02`:77-84) | Assert no writes under `.claude/` (`03`:123-137, 170-175) | Uses `.claude/templates/...` as primary template source but also says no `.claude/` staging/direct mirror edits (`04`:5-17, 51-57) | WATCH: reading `.claude` template is acceptable, but generated task should cite source-of-truth template path if available |
| Raw payload redaction | Noted in expected evidence/report roles (`01`:27-34, 123-130) | Contract-status should inspect/parse only, no live polling (`02`:48-57) | Strong redaction tests with sentinel body (`03`:85-103, 170-178) | Not applicable | CONSISTENT |

## Findings

### Finding 1: Reflect contract-status command shape conflicts across research files

- **Severity:** Critical
- **Files:** `02-patterns-integration.md`, `03-validation-tests.md`, with supporting ambiguity in `01-file-inventory.md`
- **Evidence:** `02-patterns-integration.md:9` says a new `contract-status` fits as an additional `@reflect_group.command(...)` sibling rather than inside `run()`. `02-patterns-integration.md:42-45` repeats that `run` is not the right place because it requires a tasklist and launches/derives reflect-run configuration. By contrast, `03-validation-tests.md:159-168` proposes help coverage "if implemented as flags on `reflect run`" and tests flags `--contract-status`, `--validate`, `--repo`, and `--pr`, including a tasklist-free invocation despite `commands.py` currently requiring `tasklist`. `01-file-inventory.md:77-80` says a likely implementation location is a new Click subcommand in `commands.py`, but does not name whether it is a sibling subcommand or flags on `run`.
- **Why it matters:** The MDTM tasklist cannot safely encode implementation or tests until the CLI surface is pinned. A sibling command implies tests such as `superclaude reflect contract-status --repo ... --pr ...`; flags-on-run implies `superclaude reflect run --contract-status ...` and must handle the required `tasklist` argument differently.
- **Required resolution:** Pick one surface before task generation. The stronger cross-file consensus is the sibling subcommand because `02` gives the clearest implementation rationale and `01` aligns with a "new Click subcommand". Update the validation-test plan to remove the flags-on-`run` branch or explicitly mark it as rejected.

### Finding 2: Operator-facing no-side-effect halt text has divergent required wording

- **Severity:** Important
- **Files:** `02-patterns-integration.md`, `03-validation-tests.md`, with related constraints in `01-file-inventory.md`
- **Evidence:** `02-patterns-integration.md:61-64` recommends exact text: `HALT: detection contract is locked:false (or absent) — run the R1 probe first and flip locked:true before arming (T-210). No monitor armed; no poll, push, reply, resolve, retrigger, or resume was started.` `03-validation-tests.md:144-147` requires a different stable substring: `No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.` `01-file-inventory.md:53-66` and `01-file-inventory.md:117-119` emphasize no arm/push/resume side effects but do not settle the exact phrase.
- **Why it matters:** Tests that assert exact or stable substrings will fail if task implementers follow the other research file. The lists also differ semantically: `02` includes `poll` and `resume`; `03` includes `comments` and `retries` and omits `poll`/`resume`.
- **Required resolution:** Define one canonical halt sentence in the tasklist and have all tests assert that canonical form. A merged sentence should include the existing T-210 loader wording plus the no-side-effect categories from both files if the product requirement requires them.

### Finding 3: Reflect CLI test placement and scope are fragmented

- **Severity:** Important
- **Files:** `01-file-inventory.md`, `02-patterns-integration.md`, `03-validation-tests.md`
- **Evidence:** `01-file-inventory.md:117` suggests `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_reflect_cli.py` or reflect-side tests. `02-patterns-integration.md:38` and `02-patterns-integration.md:75` recommend adding reflect CLI output tests under `/config/workspace/IronClaude/tests/cli/reflect/test_cli_smoke.py`. `03-validation-tests.md:155-168` suggests either adding to `test_cli_smoke.py` or creating `/config/workspace/IronClaude/tests/cli/reflect/test_contract_status_cli.py`.
- **Why it matters:** Fragmented placement is not inherently wrong, but the generated MDTM tasklist should avoid duplicate, overlapping tests across `tests/pr_submit/` and `tests/cli/reflect/`. CLI behavior belongs under `tests/cli/reflect/`; pure setup helper behavior belongs under `tests/pr_submit/`.
- **Required resolution:** Encode a single test ownership rule: helper/state/writer tests under `tests/pr_submit/test_contract_setup_*.py`; Click command exposure/output/no-ReflectRunner-launch tests under `tests/cli/reflect/test_contract_status_cli.py` or a clearly scoped addition to `test_cli_smoke.py`, not both.

### Finding 4: Evidence test coverage is named in inventory but underrepresented in validation strategy commands

- **Severity:** Important
- **Files:** `01-file-inventory.md`, `03-validation-tests.md`
- **Evidence:** `01-file-inventory.md:29` lists a dedicated `evidence.py` module with `EvidenceBundle`, `load_evidence()`, SHA-256 hashing, and surface mapping. `01-file-inventory.md:113` proposes `/config/workspace/IronClaude/tests/pr_submit/test_contract_setup_evidence.py`. `03-validation-tests.md:85-121` covers validation reports, redaction, omitted surfaces, repo mismatch, hash mismatch, cross-PR, and staleness, but its command set at `03-validation-tests.md:183-185` omits `test_contract_setup_evidence.py` entirely.
- **Why it matters:** Evidence loading and hashing are core to the design target and lock safety. If the generated tasklist follows only `03` commands, it may skip a dedicated evidence loader test file even though `01` identifies it as a first-class module.
- **Required resolution:** Add either a dedicated `test_contract_setup_evidence.py` to the recommended scoped pytest command or explicitly fold each evidence-loader invariant into `test_contract_setup_validation.py` and state that no separate evidence test module will be created.

### Finding 5: Template source path should be reconciled with source-of-truth discipline

- **Severity:** Minor
- **Files:** `02-patterns-integration.md`, `04-template-examples.md`
- **Evidence:** `04-template-examples.md:7-8` uses `.claude/templates/workflow/02_mdtm_template_complex_task.md` and `.claude/templates/workflow/01_mdtm_template_generic_task.md` as primary template sources. `02-patterns-integration.md:77-84` states `.claude/{skills,commands,agents,hooks,templates}` is gitignored sync-dev output and docs/component changes must be made under `src/superclaude/...` first, then synced. `04-template-examples.md:53-54` also says no `.claude/` staging or direct mirror edits.
- **Why it matters:** This is not a direct contradiction because reading `.claude` templates for examples is allowed, but a generated tasklist should avoid treating `.claude` as the authoritative editable source if source equivalents exist. The task-builder output should cite source-of-truth template/schema paths where possible and keep `.claude` references as runtime/dev-copy observations.
- **Required resolution:** In the MDTM tasklist, state that `.claude/templates/...` was checked as the active dev copy, but source edits/staging remain under `src/superclaude/...`; do not instruct any `.claude` edits or staging.

## Validation Command Consistency

| Command area | Research source | Status | Notes |
|--------------|-----------------|--------|-------|
| Scoped setup pytest | `03-validation-tests.md:183-185` | NEEDS REVISION | Omits dedicated evidence test file proposed by `01-file-inventory.md:113`; also assumes all listed test modules will exist. |
| Reflect CLI pytest | `03-validation-tests.md:187-191` | CONDITIONAL | Valid if reflect CLI changes are included; must be aligned to chosen CLI surface (sibling `contract-status` vs `run --contract-status`). |
| Existing regression pack | `03-validation-tests.md:193-197` | CONSISTENT | Matches `01`/`02` emphasis on preserving T-210, monitor arm, and autonomy behavior. |
| Project validation | `03-validation-tests.md:199-203` | CONSISTENT | Uses UV and scoped directories. |
| Ruff | `03-validation-tests.md:205-209` | CONSISTENT | Uses scoped ruff, aligning with project memory avoiding broad unrelated format churn. |
| Sync validation | `03-validation-tests.md:211-215` | CONSISTENT | Only needed if `src/superclaude/skills`, `src/superclaude/agents`, or `src/superclaude/commands` are edited; aligns with `02-patterns-integration.md:77-84` and `04-template-examples.md:51-57`. |

## Contradictions and Divergences Requiring Task-Builder Attention

1. **CLI surface must be pinned before task generation:** sibling `superclaude reflect contract-status` is recommended by `02`, while `03` still carries a flags-on-`reflect run` branch.
2. **Canonical halt/no-side-effect wording must be unified:** `02` and `03` propose different exact/stable phrases and different side-effect lists.
3. **Test file ownership must be normalized:** avoid duplicate reflect CLI tests across `tests/pr_submit/` and `tests/cli/reflect/`; assign helper vs Click behavior clearly.
4. **Evidence loader coverage must not be lost:** either add `test_contract_setup_evidence.py` to commands or explicitly integrate equivalent tests elsewhere.
5. **Template references should respect source-of-truth discipline:** `.claude` may be observed but should not become an edit/stage target.

## Cross-Validated Stable Claims

The following claims are consistent across the assigned research files and are safe for task-builder to use:

- The new implementation should be centered on a shared helper/package under `/config/workspace/IronClaude/src/superclaude/pr_submit/`, with `contract_setup/` as the most specific path named by inventory/design research.
- Existing `DetectionContract.for_arming()` fail-closed behavior must remain the arm path; setup/status must not make shipped `locked:false` armable.
- Operator-local locked contracts and generated probe/report artifacts belong under `/config/workspace/IronClaude/.dev/pr-monitor/`, not under source files or `.claude/` mirrors.
- Setup/status/validation paths must not arm Monitor, poll live GitHub, push, reply, resolve, retrigger, resume, or otherwise mutate PR state.
- Validation must prove candidate contracts against observed evidence and classifier behavior, not guessed defaults; raw payload bodies must be excluded from summaries/status output.
- MDTM task output should use Template 02-style complex task structure, B2 self-contained checklist items, explicit QA gates, and a penultimate post-reflect wrapper item before final Done/status update.
- All Python validation commands must use `uv run`, and component documentation edits must follow `src/superclaude/` source-of-truth plus `make sync-dev && make verify-sync` where applicable.

## Recommendations

- Resolve Findings 1 and 2 before synthesizing the final MDTM tasklist; both can cause implementation/test mismatch if left ambiguous.
- Treat Findings 3 and 4 as tasklist-structure fixes: name exact test files once and include all proposed first-class modules in scoped validation commands.
- Carry Finding 5 as a constraint in the generated tasklist rather than a blocker: no `.claude` edits or staging, and cite source-of-truth paths for editable components.

## Final Verdict

**VERDICT: FAIL**

The assigned research files are broadly aligned on the architecture and safety invariants, but they contain one critical unresolved conflict over the reflect CLI readiness surface and one important unresolved conflict over exact no-side-effect halt wording. These must be reconciled before task-builder emits an executable MDTM tasklist.
