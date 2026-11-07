# Reflect report: plan TASK-WF-scIssueClaimPipe-20261107-063237 (UC-1, pre-execution)

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.78
citations_total: 202
citations_revalidated: 202
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

**Verdict: FAIL.** The plan has 6 blocking findings (B-1 to B-6) and 6 further Drift findings of MEDIUM severity. Reflect is advisory inside `/sc:workflow`, so the plan stays as written and the findings travel with the package. `confidence_calibrated` is the mean of the three reviewer cards' calibrated scores (0.78, 0.77, 0.80); the Tier 1 card scored 0.81.

## Coverage

- Pass 1 parsed requirement ids: 0 (the design labels requirements P, D, FR, ST, OB; the matcher knows R-, REQ-, SPEC-, T-). `coverage_pct` is null by definition.
- Pass 2 inferred rows: 56, each with a verbatim quote that a script confirmed on its cited line.
- `coverage_pct_union`: 0.9107 (51 of 56); `S_dev_density` (union): 0.0893.
- Unmapped rows: INF-001, INF-004, INF-048, INF-050, INF-056. Content-level disposition: INF-001 (Orca is a dependency) is absent from the plan Constraints (finding m-1); the other four are constraint or negative requirements carried by the plan's Constraints section.
- Tier decision: Tier 2, forced by the parse-density guard (0 parsed ids, 56 inferred), also by three domains (code, tests, docs) and by calibrated confidence 0.81 below 0.85. Reviewers: sonnet (analyzer), haiku (qa), opus (refactorer); calibrator diversity degraded and vendor diversity single (all gateway ids are Anthropic); executor class not resolved.
- Adversarial merge: base variant 1, convergence 100% (25 of 25 points), invariant probe 14 findings with one HIGH recorded as blocking finding B-3.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | Orca is a dependency. No code, warning, option or document text exists only for a project without Orca. | source.md:39 | unmapped (best Task 6, ratio 0.5) |
| INF-002 | `--submit` is a second flag, valid with `--pipeline full` only. | source.md:41 | covered by Task 3 (ratio 0.667) |
| INF-003 | The agent is started with `orca agent launch --agent claude --surface terminal`, a Claude CLI session. | source.md:45 | covered by Task 6 (ratio 0.778) |
| INF-004 | Nothing here builds the hook. The level must be readable by the hook from state the agent cannot edit (section 6). | source.md:46 | unmapped (best Task 7, ratio 0.583) |
| INF-005 | `--pipeline` or `--submit` with `--create`: STOP `E-CLAIM-ONLY-FLAG` | source.md:80 | covered by Task 3 (ratio 1.0) |
| INF-006 | A `--pipeline` value that is not one of the three: STOP, list `worktree`, `full`, `none`. | source.md:81 | covered by Task 3 (ratio 1.0) |
| INF-007 | `--submit` with a value, or with `--pipeline worktree` or `--pipeline none` or no `--pipeline`: STOP `E-SUBMIT-NEEDS-FULL` | source.md:82 | covered by Task 3 (ratio 1.0) |
| INF-008 | `commands/issue.md` gets `version: "1.1.0"` | source.md:86 | covered by Task 3 (ratio 0.857) |
| INF-009 | `$HOME/.claude/state/launch-level/pending/<nonce>`. Built from path parts in the script, directories `0700`, files `0600`. | source.md:120 | covered by Task 6 (ratio 0.8) |
| INF-010 | `secrets.token_hex(16)`: 32 lowercase hex characters, new for every launch | source.md:121 | covered by Task 6 (ratio 0.778) |
| INF-011 | exactly one word, no spaces: `worktree`, `full` or `full-submit`. `--pipeline none` writes nothing. | source.md:122 | covered by Task 3 (ratio 0.727) |
| INF-012 | written to a temporary name that does not match the nonce pattern, then `os.rename` to `<nonce>` | source.md:123 | covered by Task 6 (ratio 0.625) |
| INF-013 | written before `orca agent launch`; removed if the launch fails | source.md:124 | covered by Task 6 (ratio 0.857) |
| INF-014 | `--prompt` starts with `[sc-launch:v1:<nonce>] ` | source.md:125 | covered by Task 6 (ratio 1.0) |
| INF-015 | no launch (`W-LAUNCH-FAILED`); the claim never starts an agent whose level it could not record | source.md:126 | covered by Task 6 (ratio 0.778) |
| INF-016 | `enforcement_hook` (contract field) is `installed` when `$HOME/.claude/hooks/launch-level-guard.sh` exists and is executable, else `missing`. | source.md:132 | covered by Task 6 (ratio 0.875) |
| INF-017 | `ok: false` is STOP `E-ORCA-REQUIRED` with the script's `detail`. | source.md:138 | covered by Task 4 (ratio 1.0) |
| INF-018 | `next-steps.md` gets its `Plan boundary: after step <K>` line (FR-26). | source.md:144 | covered by Task 5 (ratio 0.75) |
| INF-019 | It is written before Wave 7 so the copy carries it. | source.md:145 | covered by Task 7 (ratio 1.0) |
| INF-020 | Wave 7 runs only after both comments are posted. | source.md:147 | covered by Task 4 (ratio 0.833) |
| INF-021 | Runs when `<L>` is not `none` and Wave 7 `status` is `created` or `reused` (FR-21) | source.md:153 | covered by Task 7 (ratio 0.8) |
| INF-022 | The claim `status` stays `success` through any Wave 7 or Wave 8 failure | source.md:161 | covered by Task 4 (ratio 0.889) |
| INF-023 | One JSON object on stdout. Exit 0 for every runtime outcome; exit 2 only for bad arguments (argparse). | source.md:165 | covered by Task 1 (ratio 1.0) |
| INF-024 | Every subprocess runs without a shell, with a timeout (120 s; `preflight` 30 s; each `terminal read` 15 s) and captured output. | source.md:165 | covered by Task 1 (ratio 0.857) |
| INF-025 | `{"ok": true}` when it exits 0, prints JSON with `ok: true` and `result.runtime.reachable: true` | source.md:169 | covered by Task 1 (ratio 1.0) |
| INF-026 | `--submit` with `--level worktree` is bad arguments (exit 2). | source.md:173 | covered by Task 1 (ratio 0.714) |
| INF-027 | Unusable (FR-15): `ok != true`, `result.truncated == true`, `result.hostScope.omittedHostIds` non-empty, zero rows, or no row with `isMainWorktree: true` | source.md:192 | covered by Task 2 (ratio 1.0) |
| INF-028 | Dedupe by row `id`; the first key with a hit decides. | source.md:193 | covered by Task 2 (ratio 0.857) |
| INF-029 | a failed `git fetch origin` with the ref present continues with `W-ORIGIN-BASE-STALE` (FR-16). | source.md:194 | covered by Task 2 (ratio 1.0) |
| INF-030 | Never one recursive directory copy. | source.md:195 | covered by Task 2 (ratio 1.0) |
| INF-031 | a differing untracked file is renamed to `<name>.prev` (replacing an older `.prev`), then copied and named. | source.md:195 | covered by Task 2 (ratio 0.9) |
| INF-032 | It keeps an existing `launch` entry. It is never copied. | source.md:197 | covered by Task 2 (ratio 0.833) |
| INF-033 | Read `<D>/worktree.json` through the record guard. | source.md:207 | covered by Task 6 (ratio 1.0) |
| INF-034 | A `launch` entry exists: `already_launched` with its `at` time; no `orca` call, no record written. | source.md:208 | covered by Task 6 (ratio 1.0) |
| INF-035 | No `--model` or `--effort` (AD FR-22). | source.md:211 | covered by Task 2 (ratio 0.6) |
| INF-036 | then `orca terminal read --terminal <handle> --screen --json` up to 5 times, 2 s apart. | source.md:212 | covered by Task 6 (ratio 1.0) |
| INF-037 | Write `launch: {level, submit, at}` (UTC ISO time) into `<D>/worktree.json`, whatever the shim result, because an agent exists. | source.md:213 | covered by Task 6 (ratio 0.938) |
| INF-038 | It never runs `git worktree add`, `orca worktree rm`, a commit, a push or a stage (FR-12). | source.md:215 | covered by Task 2 (ratio 1.0) |
| INF-039 | The `full` and `common` blocks never contain the tokens `/sc:pr-submit`, `git push`, `git commit` or `--monitor` | source.md:228 | covered by Task 5 (ratio 0.923) |
| INF-040 | `launch_status` is `not_requested` for `none` and when Wave 7 `failed`. | source.md:256 | covered by Task 7 (ratio 0.857) |
| INF-041 | A launch is never attempted when the worktree `status` is `failed` (FR-21). | source.md:283 | covered by Task 2 (ratio 0.75) |
| INF-042 | Nothing under `.claude/` is edited or staged; `make sync-dev` produces it. | source.md:287 | covered by Task 4 (ratio 0.625) |
| INF-043 | Copied in whole from the main checkout (untracked there) so it is committed with the PR; this design cites it | source.md:296 | covered by Task 2 (ratio 0.667) |
| INF-044 | Stays under 500 lines. | source.md:303 | covered by Task 4 (ratio 1.0) |
| INF-045 | then byte-copy the file to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | source.md:306 | covered by Task 9 (ratio 1.0) |
| INF-046 | B2 row rewritten (section 2), new rows B16 to B18, and short "Amended 2026-11-07" notes in sections 1, 4, 7, 14, 16, 20 pointing to this design. | source.md:307 | covered by Task 8 (ratio 0.958) |
| INF-047 | every new reference inside the primitives to another primitive uses the installed path and the script is called as `<skill base>/scripts/orca_worktree.py`, never a `src/superclaude/` path (FR-14). | source.md:312 | covered by Task 2 (ratio 0.636) |
| INF-048 | The Orca and git seams are faked; no test calls a real `orca`, `gh` or the network. | source.md:316 | unmapped (best Task 2, ratio 0.444) |
| INF-049 | the pending record is a regular file of mode `0600` holding exactly `worktree`, `full` or `full-submit` | source.md:335 | covered by Task 6 (ratio 1.0) |
| INF-050 | The old MR cases FO-5 and AC-5 (no `orca`) are not built | source.md:359 | unmapped (best Task 2, ratio 0.5) |
| INF-051 | A missing hook script is a warning (`W-ENFORCEMENT-ABSENT`), not a refusal, for every level | source.md:371 | covered by Task 6 (ratio 0.889) |
| INF-052 | No automatic retry of a launch and no `--retry-launch` in version 1 | source.md:377 | covered by Task 3 (ratio 0.6) |
| INF-053 | `docs/user-guide/commands.md` and the `/sc:issue` row of `HOW-WE-WORK.md` are updated in the same change | source.md:382 | covered by Task 9 (ratio 0.846) |
| INF-054 | `make verify-sync` passes, the tests of section 13 pass, `make lint` and the pinned ruff format check pass, the `src/superclaude` path grep shows no new hit. | source.md:419 | covered by Task 9 (ratio 0.8) |
| INF-055 | Running any live claim, worktree create or agent launch against a real issue. | source.md:31 | covered by Task 2 (ratio 0.6) |
| INF-056 | The enforcement hook (`launch-level-guard.sh`, its L2 `pre-push` layer, `jq` and registration checks): issue #394. | source.md:29 | unmapped (best Task 6, ratio 0.467) |

## Deviations

The findings below are the merged card (`adversarial/adversarial/merged-output.md`) rendered in place. Every finding is class Drift; each carries its location, evidence, classification rationale (What diverged), remediation (Fix) and fix location. No finding maps to a tasklist item in the Wave 1B sense: the subject is the tasklist itself.

## Blocking findings

<!-- Source: Base (original) finding 2, reclassified per Change 1; Invariant probe INV-001 and INV-002 merged per Change 2 -->

### B-1 The plan never accounts for the write-verb audit

- **Class:** Drift. **Severity:** HIGH
- **Location:** plan:64, plan:105-107, plan:130-133 (Tasks 2, 5 and 7). Base location: plan:30-33, 49-64, 95-108, 128-135.
- **What diverged:**
  - The plan never mentions the write-verb audit in `tests/skills/test_worker_contract.py`. That audit scans every file under the skills, commands and agents folders for `git add`, `commit`, `push`, `merge`, `stash`, `update-ref`, `worktree add|remove` and `gh pr|api`.
  - Each hit must be classified by its exact stripped line text. `test_every_write_verb_hit_is_classified` and `test_classification_table_has_no_stale_entries` fail on an unclassified hit or on an edited classified line.
  - Task 5's template contains "Do not run ... git commit, git push" and `git push`, and Task 2's grep expects such text in the script. No task names `test_worker_contract.py`.
  - The suite will certainly fail from Task 5 on. The first gate that catches it is Task 7's `tests/skills` run, and no task tells the implementer how to fix it.
  - INV-002: Tasks 1, 3 and 4 also edit files in the audited roots. The template's push and commit lines, which the launched agent runs, need a category chosen (the list at tests/skills/test_worker_contract.py:1081-1087 includes `never-worker` and `no-command`, and the existing sc-issue keys already use `never-worker`); the plan does not say which. A read-only label is checked only for `gh api` lines.
  - INV-001 (LOW within this finding): SKILL.md:72, SKILL.md:135 and refs/claim.md:9 are already classified. Editing any of them without updating its key fails the stale-key test. The probe's claim that `--submit` makes those lines false is rejected.
- **Evidence:**
  - tests/skills/test_worker_contract.py:1090-1094 (AUDIT_ROOTS), :1098-1101 (WRITE_VERB_RE), :1103-1105 (the five categories)
  - tests/skills/test_worker_contract.py:1131-1152 (`_scan_write_verbs`), :1155-1162 (`_check_all_classified`)
  - tests/skills/test_worker_contract.py:2124-2195 (sc-issue keys; validator-corrected range), :2199-2200, :2203-2208 (the two tests), :2220-2226 (the read-only check, `gh api` only)
  - src/superclaude/skills/sc-issue-protocol/SKILL.md:72, :135; src/superclaude/skills/sc-issue-protocol/refs/claim.md:9
  - plan:64, plan:105-107, plan:133; source.md:309-310 (the design's change table leaves out the test file)
- **Orchestrator verification:** AUDIT_ROOTS, WRITE_VERB_RE, `_scan_write_verbs` and the two tests were re-Read at tests/skills/test_worker_contract.py:1090-1155 and 2199-2205.
- **Fix:**
  - Name `tests/skills/test_worker_contract.py` in every task that adds or edits a write-verb line (Tasks 1 to 5 and 7), and add it to their acceptance runs.
  - State that each new hit needs an exact-text classification entry with one of the five categories. Decide which category the template's push and commit lines get.
  - When a task edits an already-classified line, update its key in the same task.
  - Also add the file to the design's change table (source.md:309-310). This is not a precondition.
- **Fix location:** plan only. **Sources:** V1 finding 2; INV-001; INV-002; Round 2 (all three advocates: Drift HIGH)

<!-- Source: Base (original) finding 3; Variant 3 advisory 2, INV-003, INV-005 merged per Change 3 -->

### B-2 The worktree output carries no tracked-files data

- **Class:** Drift. **Severity:** MEDIUM-HIGH
- **Location:** plan:49, plan:57, plan:84; source.md:177, source.md:195
- **What diverged:**
  - The skill prints "untracked, do not stage" only when no file under `<wt>/.dev/issues/<N>/` is tracked. The `worktree` output (`status, path, branch, match_key, warning, detail`) has no tracked-file field; tracked files appear only in the free-text `detail`.
  - The script owns every worktree git call, so Task 4's claim.md step has no way to know the answer.
  - INV-005: the field belongs in the subcommand's stdout (a fixed key set, plan:49), not in the `worktree.json` `{path,status}` record (source.md:197). Adding it to the record would change the record guard and the launch inputs.
  - INV-003 (data loss): when `git ls-files` fails, `run()` returns a failed result and does not raise (plan:34). The tracked set then reads as empty, and a differing tracked file is renamed to `.prev` and overwritten. Neither source.md:195 nor plan:57 makes the copy fail in that case.
- **Evidence:** source.md:158, :165, :177, :195, :197; plan:34, plan:49, plan:57, plan:84
- **Fix:**
  - Amend design §8.3 to add a machine-readable tracked-files field to the `worktree` stdout. The field must tell "none tracked" apart from "unknown".
  - When `git ls-files` fails, the copy must fail without overwriting any differing file.
  - Then Task 2 implements and tests both, and Task 4's claim.md step reads the field.
- **Fix location:** design first. **Sources:** V1 finding 3; V3 advisory 2; INV-003; INV-005

<!-- Source: Variant 3 advisory 3 (C-013) and INV-007, merged per Change 4 -->

### B-3 The launch prompt is not fork-safe

- **Class:** Drift. **Severity:** HIGH (security: exposure to the wrong repository; INV-007 grade; debate C-013 was MEDIUM before the probe)
- **Location:** plan:101 (the template's `submit` block); source.md:226
- **What diverged:**
  - The `submit` block's "check that no PR is already open" step can be written as `gh pr list --head <branch>` with no `--repo`.
  - The fork-safety scan covers only `_FORK_FILES` (SKILL.md, refs/*.md and the agents). Templates are not in that set.
  - A launched agent could therefore reach the upstream repository while every test passes. The same gh line is also a write-verb hit (B-1).
- **Evidence:** source.md:226; plan:101; tests/skills/test_issue_protocol.py:288 (`_FORK_FILES`); tests/skills/test_issue_worker_agents.py:31-48 (`gh_lines_missing_repo`)
- **Fix:**
  - Design §9: every gh call in the `submit` block names `--repo IronbellyOrg/IronClaude`.
  - Design §13: extend `_FORK_FILES` to cover `templates/launch-prompt.md`, or add a pin that scans it.
  - Then Task 5 writes the template to match, and Task 7 adds the test.
- **Fix location:** design first. **Sources:** V3 advisory 3 / C-013; INV-007

<!-- Source: Invariant probe INV-004, added per Change 5 -->

### B-4 The plan would replace the shared return contract

- **Class:** Drift. **Severity:** MEDIUM (blocking)
- **Location:** plan:130 ("replace the claim-mode return contract"); source.md:241
- **What diverged:**
  - SKILL.md:101-115 is one return contract shared by both modes. It carries `status`, `issue_number` and `next_steps_path`, and source.md:161 still needs `status`.
  - The design says the ten fields "replace" the fixed list for claim mode, and Task 7 repeats that.
  - A literal replacement drops those fields or changes create mode. ST-10 only checks that the ten fields are present, so it would still pass.
- **Evidence:** src/superclaude/skills/sc-issue-protocol/SKILL.md:101-115; source.md:161, :241, :244-253, :356; plan:130
- **Fix:**
  - Design §10: extend the shared contract with the claim-mode fields instead of replacing it. Keep `status`, `issue_number`, `next_steps_path` and create mode unchanged.
  - Task 7 then edits SKILL.md to match, and ST-10 checks that the kept fields are still present.
- **Fix location:** design first. **Sources:** INV-004

<!-- Source: Base (original) finding 5; Variant 3 advisory 1 and INV-006 merged per Change 6 -->

### B-5 ST-4 has no workable matching rule

- **Class:** Drift. **Severity:** MEDIUM (blocking)
- **Location:** plan:130 (ST-4); source.md:350
- **What diverged:**
  - ST-4 bans the Orca link flags in the skill, refs, command and script, but gives no rule for matching them.
  - A substring scan fails on existing text: `--pr` is a prefix of `--prompt`; `--issue-url` and `--issue-number` already appear at refs/claim.md:49 and in clickup_claim.py; and prose such as refs/tiers.md:25 (the "`--model` flag") sits outside any orca command line.
  - The new script itself must contain `--agent`, `--prompt` and `--surface`.
  - INV-006: Task 9's format check (plan:162) wraps the launch argv, so `"--model",` sits on its own line. A line-by-line scan then misses it and cannot scope the outside-the-launch-call exemption.
- **Evidence:** source.md:350; src/superclaude/skills/sc-issue-protocol/refs/claim.md:49; src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py:247-248; src/superclaude/skills/sc-issue-protocol/refs/tiers.md:25; plan:130, plan:162
- **Fix:**
  - Design §13 ST-4: match whole tokens only, and only on orca command lines, with the launch call excluded.
  - For `scripts/orca_worktree.py`, find the launch argv by parsing the file with `ast` instead of scanning lines.
  - Then Task 7 implements the rule.
- **Fix location:** design first. **Sources:** V1 finding 5; V3 advisory 1; INV-006

<!-- Source: Base (original) findings 6 and 9; Variant 2 findings 1-3 and Variant 3 findings 5-7 merged per Change 7 -->

### B-6 Required tests and safeguards have no owning task

- **Class:** Drift. **Severity:** MEDIUM. The Task 6 safeguards are MEDIUM (V2 grade); the ARG-1 part is LOW-MEDIUM.
- **Location:** plan:41-43 (Task 1), plan:86, plan:116, plan:119 (Task 6), plan:130 (Task 7)
- **What diverged:** no task owns the following required deliverables.
  - (a) LA-7 (source.md:340) is not among LA-1 to LA-6 (plan:119).
  - (b) ARG-1 (source.md:341) must hold for every subcommand. Task 1 can test only `preflight`, and a missing-required-argument check cannot be tested on `preflight` (plan:41-43). `worktree`, `prompt` and `launch` get no ARG-1 case.
  - (c) No explicit ST-5 case pins the template row (source.md:351). The existing inventory test (tests/skills/test_issue_protocol.py:131-141) already requires a files-table row for every template, so the row is covered implicitly; the missing piece is the named pin.
  - (d) ST-6 has no Wave 8 half (source.md:352). Wave 8 exists only after Task 7.
  - (e) Task 6 drops design step 5's timeout instruction that `detail` must say to check Orca before re-running (source.md:211; D9 at :377). A timeout writes no `launch` entry, so `already_launched` does not catch a re-run, and a duplicate agent can start.
  - (f) Task 6 drops the `hand_command` note that a hand-started agent is not governed by the hook (source.md:211).
  - (g) Task 6 drops "The pending record stays" (source.md:212). LA-3 asserts none of (e) to (g).
- **Evidence:** source.md:211, :212, :340, :341, :351, :352, :377; plan:41-43, plan:116, plan:119, plan:130
- **Fix:**
  - Task 6: add an LA-7 case. Copy source.md:211-212 into Task 6's steps, with LA assertions for (e) to (g).
  - Tasks 2, 5 and 6: add one ARG-1 case each, for `worktree`, `prompt` and `launch`.
  - Task 7: pin the ST-5 template row and add the ST-6 Wave 8 half.
- **Fix location:** plan only. **Sources:** V1 findings 6 and 9; V2 findings 1-3; V3 findings 5-7

## Non-blocking findings (Drift, MEDIUM)

<!-- Source: Base (original) finding 1, reclassified per Change 1, merged per Change 8 -->

### M-1 The inventory test is red between tasks

- **Class:** Drift. **Severity:** MEDIUM
- **Location:** plan:30 and plan:95 (the tasks that create the files); plan:86 and plan:130 (where the table rows arrive, late)
- **What diverged:**
  - The two-way inventory test requires a files-table row for every file under refs, templates and scripts.
  - Task 1 creates `scripts/orca_worktree.py`, but its row arrives in Task 4. Task 5 creates `templates/launch-prompt.md`, but its row arrives in Task 7.
  - The acceptance runs of Tasks 1, 2, 3, 5 and 6 use `-k` or single-file filters, so they never run the whole file.
  - The gap closes by itself and never gates: at Task 4's acceptance for the script row (plan:89 runs the whole test_issue_protocol.py), and at Task 7's (plan:133) for the template row.
- **Evidence:** tests/skills/test_issue_protocol.py:131-141; plan:41, 62, 75, 89, 106, 119, 133
- **Fix:** add the files-table row in Task 1 (for the script) and in Task 5 (for the template).
- **Fix location:** plan only. **Sources:** V1 finding 1; Round 2

<!-- Source: Base (original) finding 4; INV-008 merged per Change 8 -->

### M-2 One warning field, and no `enforcement_hook` value on `already_launched`

- **Class:** Drift. **Severity:** MEDIUM
- **Location:** plan:116, plan:119; plan:56-59
- **What diverged:**
  - The `launch` output has one `warning` field, but W-ENFORCEMENT-ABSENT and W-LAUNCH-NOT-CCSESSION can both apply to a launched result. The design does not say which takes precedence.
  - A temporary HOME has no hook script, so `enforcement_hook` is missing in LA-5 too.
  - For `already_launched`, the design returns before step 3, so `enforcement_hook` has no defined value.
  - INV-008: the `worktree` step has the same collision. W-ORIGIN-BASE-STALE and the `.prev` W-WORKTREE-COPY-FAILED can both apply. plan:59 keeps only the code that set the status, so the remedy for the other code is lost.
- **Evidence:** source.md:203, :208-209, :212, :253; plan:56-59
- **Fix:**
  - The design states the precedence, or makes `warning` carry every code that applies, for both `launch` and `worktree`.
  - The design defines `enforcement_hook` on `already_launched`.
  - Then Tasks 2 and 6 follow the design.
- **Fix location:** design first. **Sources:** V1 finding 4; INV-008

<!-- Source: Variant 3 finding 4 (C-007); Base (original) findings 7 and 8 merged per Change 8 -->

### M-3 Stale claim text in SKILL.md and commands/issue.md

- **Class:** Drift. **Severity:** MEDIUM for SKILL.md steps 6 and 7; LOW for the two `description` fields and the other command text
- **Location:** plan:70-72, plan:86, plan:130
- **What diverged:**
  - SKILL.md:87-88: step 7 says "Print the next-steps.md path and STOP". Task 4 changes step 7 only so that it continues to the worktree step, and Task 7 never adds the Wave 5 prompt call or Wave 8 to steps 6 and 7. A reader who follows SKILL.md stops before the launch.
  - The frontmatter `description` of SKILL.md (:3) and of commands/issue.md (:3) still says the claim then stops. The design names the SKILL.md description (source.md:303), but Tasks 4 and 7 leave it out, and the design leaves out the command's description.
  - issue.md:71 ("After a claim, open next-steps.md and run its commands in your own session") and issue.md:100 (Related Commands) are not in Task 3.
  - The Outputs row (issue.md:68) will list launch-prompt.md, although that file is not written for `--pipeline none` (source.md:236).
- **Evidence:** src/superclaude/skills/sc-issue-protocol/SKILL.md:3, :87, :88; src/superclaude/commands/issue.md:3, :68, :71, :100; source.md:236, :302-303
- **Fix:**
  - Tasks 4 and 7 rewrite SKILL.md steps 6 and 7 to cover Waves 5, 7 and 8 at each level, and update SKILL.md:3.
  - Task 3 updates issue.md:3, :68, :71 and :100. The Outputs row says that launch-prompt.md is not written for `none`.
- **Fix location:** plan only. **Sources:** V3 finding 4 (C-007); V1 findings 7 and 8; V2 finding 4

<!-- Source: Variant 3 finding 2 (C-009), merged per Change 8 -->

### M-4 Tasks 7 and 9 do not depend on Task 3

- **Class:** Drift. **Severity:** MEDIUM
- **Location:** plan:124, plan:153
- **What diverged:**
  - Tasks 7 and 9 consume Task 3's flags and STOP codes (plan:130 requires its text to match), but neither lists Task 3 as a dependency. Task 5 depends on Task 1 only (plan:97).
  - This replaces the base card's note that the task order is sound.
- **Evidence:** plan:97, plan:124, plan:130, plan:153
- **Fix:** add Task 3 to the dependencies of Tasks 7 and 9.
- **Fix location:** plan only. **Sources:** V3 finding 2 (C-009)

<!-- Source: Invariant probe INV-009, merged per Change 8 -->

### M-5 A re-claim rewrites the running agent's prompt

- **Class:** Drift. **Severity:** MEDIUM
- **Location:** source.md:145, :195, :208
- **What diverged:**
  - On a re-claim at a new level, Wave 5 rewrites launch-prompt.md (source.md:145) and Wave 7 copies it into the worktree (source.md:195). Only after that does Wave 8 return `already_launched` (source.md:208).
  - The running agent's prompt file then no longer matches the level in its launch record.
- **Evidence:** source.md:145, :195, :208
- **Fix:** the design states that, when a launch record already exists, Waves 5 and 7 do not replace the prompt file the running agent uses. The plan's tasks then follow the design.
- **Fix location:** design first. **Sources:** INV-009

<!-- Source: Round 2 new item N-001 (advocate 3), merged per Change 8 -->

### M-6 A create timeout looks the same as a failed create

- **Class:** Drift. **Severity:** MEDIUM (grouped here by the refactoring plan; Round 2 advocate 3 proposed LOW)
- **Location:** plan:34, plan:56, plan:62
- **What diverged:**
  - source.md:194 says a create that times out must be followed by a second list, while a nonzero exit fails at once.
  - Task 1's `run()` returns "a failed result" on a timeout, a nonzero exit or a missing binary (plan:34); the plan does not say the timeout is marked apart from the others.
  - Task 2 needs to tell these apart (plan:56). FO-6 covers a hang at the timeout in general (source.md:326); no case names a create timeout followed by the second list (plan:62 lists only case ids).
  - The wording at source.md:165 ("a timeout is a failed command") encourages treating them the same.
  - Effect: a worktree created during a timeout is reported `failed` with no record. A rerun recovers it through the marker lookup.
- **Evidence:** source.md:165, :194; plan:34, plan:56, plan:62
- **Fix:**
  - Task 1's `run()` marks timeouts.
  - Task 2 handles a create timeout with the second list, and adds an FO case for it.
  - Optionally, reword source.md:165.
- **Fix location:** plan only. **Sources:** N-001 (Round 2)

## Minor findings and notes

<!-- Source: Variant 2 finding 5, Variant 3 findings 8-10, Variant 3 note U-004, INV-010, INV-013 merged per Change 9 -->

All items here are Drift and non-blocking. Debate points C-014 (directory modes for the pending store's intermediate folders) and C-015 (the `already_launched` time field and the naming of the `-k` filter) are recorded as A-1 to A-3 under Advisory correctness gaps.

### m-1 Constraints do not record the Orca dependency

- **Class:** Drift. **Severity:** LOW. **Location:** plan:17-26. **Fix location:** plan only. **Sources:** V2 finding 5 (C-010)
- **What diverged:** Constraints include the Orca-flag rule (plan:22) but not that `--pipeline worktree|full` depends on Orca being installed (design P1).
- **Evidence:** plan:17-26; source.md:39
- **Fix:** add the Orca dependency to Constraints.

### m-2 Task 2 is too large (note)

- **Class:** Drift. **Severity:** LOW. **Location:** plan:45-64. **Fix location:** plan only. **Sources:** V3 finding 10 (C-011)
- **What diverged:** Task 2 carries the whole `worktree` subcommand: create, list again, copy, record and warning.
- **Evidence:** plan:45-64; source.md:189-197
- **Fix:** optionally, split Task 2.

### m-3 The format check runs only in Task 9 (note)

- **Class:** Drift. **Severity:** LOW. **Location:** plan:162. **Fix location:** plan only. **Sources:** V3 finding 9 (C-011, partly withdrawn in Round 2)
- **What diverged:** the implement protocol runs `make lint` after every task as a non-gating extra, which is why most of V3's lint point was withdrawn. The format check is not among those extras, so `ruff format --check` first runs in Task 9.
- **Evidence:** plan:162; ~/.claude/skills/sc-implement-protocol/SKILL.md:146, :152; Makefile:48-50
- **Fix:** run the format check in every task that edits `scripts/orca_worktree.py` (Tasks 1, 2, 5 and 6).

### m-4 Design-doc edits placed in Phase 3

- **Class:** Drift. **Severity:** LOW. **Location:** plan:139-149 (Task 8). **Fix location:** plan only. **Sources:** V3 finding 8 (C-011)
- **What diverged:** design §16 places the design-doc edits B2 and B16 in Phase 1 (source.md:405) and B17 and B18 in Phase 2 (source.md:406), but the plan puts all of them in Task 8 (Phase 3). Both phases ship in one PR.
- **Evidence:** source.md:405-406; plan:139-149
- **Fix:** move Task 8 earlier, or record why it moved.

### m-5 The pending store only grows

- **Class:** Drift. **Severity:** LOW. **Location:** source.md:212. **Fix location:** design first. **Sources:** INV-010
- **What diverged:** the design says "The pending record stays", but the hook that would consume pending records (#394) is not built, so nothing ever cleans them up.
- **Evidence:** source.md:212
- **Fix:** the design states who prunes pending records, or records that they keep growing until #394 lands.

### m-6 Task 9 never runs tests/docs

- **Class:** Drift. **Severity:** LOW. **Location:** plan:160. **Fix location:** plan only. **Sources:** INV-013
- **What diverged:** Task 9's test list leaves out `tests/docs`, although that folder exists.
- **Evidence:** plan:160; tests/docs/test_retired_docs_absent.py
- **Fix:** add `tests/docs` to Task 9's test list.

### m-7 The HOW-WE-WORK row must be ASCII

- **Class:** Drift. **Severity:** LOW. **Location:** plan:157 (Task 9 routing-row instruction; the test run is at plan:160). **Fix location:** plan only. **Sources:** INV-013
- **What diverged:** the new `/sc:issue` routing row must be ASCII-only, and Task 9 does not say so.
- **Evidence:** tests/core/test_how_we_work_routing_table.py:342-347; plan:160
- **Fix:** state the ASCII-only rule in Task 9.

### m-8 The literal `--repo` is banned in commands/issue.md (note, ADDRESSED)

- **Class:** Drift. **Severity:** LOW. **Location:** plan:75 (Task 3 acceptance). **Fix location:** plan only. **Sources:** V3 note (U-004); INV-012
- **What diverged:** nothing. `tests/commands/test_issue_command.py` asserts that the literal `--repo` does not appear in issue.md, and Task 3's acceptance run executes that test. The note is kept so the implementer writes the fork rule in issue.md without the literal flag.
- **Evidence:** tests/commands/test_issue_command.py:99-103; plan:75
- **Fix:** none needed; the implementer only needs to be aware of it.

## Advisory correctness gaps (non-gating)

<!-- Source: Base (original) correctness_gaps_advisory, kept per Change 10 -->

### A-1 Directory modes in the pending store

- **Class:** Drift. **Severity:** LOW. **Location:** source.md:120. **Fix location:** plan only. **Sources:** V1 advisory 1 (C-014)
- **What diverged:** `os.makedirs(mode=0o700)` applies the mode only to the leaf directory, so the intermediate state directories get default modes. LA-2 asserts only the pending directory.
- **Evidence:** source.md:120, :335
- **Fix:** create each level with mode 0o700, or chmod the parent directories, and extend LA-2 to the intermediate directories.

### A-2 Which field carries the `already_launched` time

- **Class:** Drift. **Severity:** LOW. **Location:** plan:116. **Fix location:** plan only. **Sources:** V1 advisory 2 (C-015)
- **What diverged:** the schema has `launched_at`, but the prose says "its at time", and plan:116 does not say which field carries it.
- **Evidence:** source.md:159, :203, :208; plan:116
- **Fix:** Task 6 names `launched_at` as the field.

### A-3 The `-k` filter selects the whole module

- **Class:** Drift. **Severity:** LOW. **Location:** plan:62. **Fix location:** plan only. **Sources:** V1 advisory 3 (C-015)
- **What diverged:** `-k "FO or worktree"` matches the module name `test_issue_orca_worktree.py`, so it selects the whole file. The filter's name overstates its scope.
- **Evidence:** plan:62
- **Fix:** drop the filter, or name the test ids.

## Rejected or withdrawn

<!-- Source: refactor-plan.md "Changes NOT Being Made" -->

| Diff point | Rejected alternative | Why rejected |
|---|---|---|
| S-002, X-001 | V1 and V3's Regression label for the test-order window | Round 2: all three advocates accepted Drift. The final repository state is correct, and the check is non-gating. |
| X-004 / V3 finding 5 | "ARG-1 and LA-7 never named" at MEDIUM, as written | Overstated: Task 1 tests a bad-subcommand exit, and Task 5 tests `--submit` with `worktree`. Only the missing per-subcommand coverage is kept (B-6). |
| Wave 6 hand-off overlap | V1's new LOW issue | Advocates 2 and 3 showed that plan:124-133 gives Task 7 the final wording. Not a separate defect. |
| C-011 lint gate | V3 finding 9 as a deviation | Withdrawn in Round 2: `make lint` runs after each task as a non-gating extra (~/.claude/skills/sc-implement-protocol/SKILL.md:132-154). The format-check gap is kept as m-3. |
| INV-001 premise | The probe's "`--submit` makes the classified lines false" | The classified lines describe the skill, which remains the only writer. A launched agent is a separate session. |
| A-005 | "Green between tasks is required" | Rejected as a universal rule. Only the acceptance gates and the final state must be green. |
## Recommendations

### Recommendation R-1: Name the write-verb audit in the plan and classify the new lines
- **File:** .dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md (Tasks 1 to 5 and 7) and tests/skills/test_worker_contract.py
- **Change:** name test_worker_contract.py in every task that adds or edits a git or gh write-verb line; add an exact-text classification entry per new hit; update the key when a classified line is edited.
- **Verifier:** `uv run pytest tests/skills/test_worker_contract.py -q` passes after Task 5 and after Task 7.
- **Linked deviation(s):** B-1
- **Priority:** P0

### Recommendation R-2: Return tracked-files data from the worktree step and never overwrite on an unknown tracked set
- **File:** docs/designs/sc-issue-claim-pipeline-flag.md (section 8.3), then Tasks 2 and 4 of the plan
- **Change:** add a machine-readable tracked-files field to the `worktree` stdout that tells none tracked from unknown; fail the copy when `git ls-files` fails.
- **Verifier:** a Task 2 test asserts the field and a Task 2 test asserts no file is renamed or overwritten when `git ls-files` fails.
- **Linked deviation(s):** B-2
- **Priority:** P0

### Recommendation R-3: Make the launch prompt fork-safe and scan it
- **File:** docs/designs/sc-issue-claim-pipeline-flag.md (sections 9 and 13), src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md (created by Task 5), tests/skills/test_issue_protocol.py (Task 7)
- **Change:** every gh call in the submit block names `--repo IronbellyOrg/IronClaude`; the fork-safety scan covers the template.
- **Verifier:** `uv run pytest tests/skills/test_issue_protocol.py -q` includes a case that fails on a gh line without `--repo` in templates/launch-prompt.md.
- **Linked deviation(s):** B-3
- **Priority:** P0

### Recommendation R-4: Extend the shared return contract instead of replacing it
- **File:** docs/designs/sc-issue-claim-pipeline-flag.md (section 10), src/superclaude/skills/sc-issue-protocol/SKILL.md (Task 7)
- **Change:** add the claim-mode fields next to the existing ones; keep `status`, `issue_number`, `next_steps_path` and create mode unchanged.
- **Verifier:** ST-10 asserts the ten new fields and the kept fields.
- **Linked deviation(s):** B-4
- **Priority:** P0

### Recommendation R-5: Give ST-4 a whole-token, orca-command-only rule that survives formatting
- **File:** docs/designs/sc-issue-claim-pipeline-flag.md (section 13, ST-4), tests/skills/test_issue_protocol.py (Task 7)
- **Change:** match whole tokens on orca command lines only, exclude the launch call, and find the argv list with `ast`.
- **Verifier:** the test passes on the current tree and fails when a `--model` token is planted in the script's list call.
- **Linked deviation(s):** B-5
- **Priority:** P0

### Recommendation R-6: Add the missing required tests and the dropped Task 6 safeguards
- **File:** plan Tasks 1, 2, 5, 6 and 7
- **Change:** add LA-7, a bad-argument case for each subcommand, the ST-5 template row, the ST-6 Wave 8 half, the timeout "check Orca" detail, the hand_command note and the "pending record stays" rule.
- **Verifier:** `uv run pytest tests/skills/test_issue_orca_worktree.py -q` includes those cases by id.
- **Linked deviation(s):** B-6
- **Priority:** P1

### Recommendation R-7: Fix ordering and wording in the plan
- **File:** plan Tasks 1, 3, 4, 5, 7 and 9
- **Change:** add the SKILL.md files-table row in the task that creates each file (Tasks 1 and 5); make Tasks 7 and 9 depend on Task 3; cover SKILL.md steps 6 and 7 and the description lines; mark timeouts in `run()` and add a create-timeout case; define warning precedence and the `already_launched` hook value in the design.
- **Verifier:** the whole `tests/skills/test_issue_protocol.py` passes after Task 1 and after Task 5; `grep -n 'then stop' src/superclaude/commands/issue.md src/superclaude/skills/sc-issue-protocol/SKILL.md` finds nothing after Tasks 3 and 4.
- **Linked deviation(s):** M-1 to M-6
- **Priority:** P1

### Recommendation R-8: Record the minor items
- **File:** plan Constraints and Task 9
- **Change:** add the Orca dependency to Constraints; add `tests/docs` and the ASCII rule to Task 9; optionally split Task 2.
- **Verifier:** reading the plan; `uv run pytest tests/docs -q`.
- **Linked deviation(s):** m-1 to m-8, A-1 to A-3
- **Priority:** P2

How to apply these: `/sc:workflow` never edits a plan from reflect findings. The design-first items (R-2 to R-5, and the design half of R-7) need `docs/designs/sc-issue-claim-pipeline-flag.md` amended before the plan is right. The plan-only items can be carried out by the implementer.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: 0 / 202 = 0.00
- Every claim in this report is Grounded (cited) or was dropped; the validator-confirmed citation checks are listed in `artifacts/evidence-validation.md`.
