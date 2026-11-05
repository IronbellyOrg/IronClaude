# Design: merge-conflict resolution for sc:pr-submit (issue #305)

## 0. Document control

| Field | Value |
|---|---|
| Command | `/sc:design` `--type component --format spec` (flow: Analyze, Plan, Design, Validate, Document) |
| Issue | IronbellyOrg/IronClaude#305 |
| Branch | `ironbelly/issue-305-pr-submit-conflicts` (base commit `119622e3`) |
| Inputs | `.dev/brainstorms/issue-305-pr-submit-conflict-resolution/merged-requirements.md` (the merged spec, cited as "spec section N"); `adversarial/debate-transcript.md`; `adversarial/invariant-probe.md` (cited as INV-NNN); `adversarial/merge-log.md`; `.dev/research/issue-305-conflict-resolution/03-roi-scored-list.md` ("Items scored above 5") |
| Status | Design for approval. Next step: `/sc:workflow` turns section 13 into a plan, then `/sc:implement`. |
| Late re-sync (P3) | Out of this release; tracked as #361 |

**Revision 2** (answers `REVIEW-1.md`; the minor findings M1 to M5 and M11 to M14 stay as review notes):

- **B1:** the Wave 8a router gets a row: Tier 1 at L1 with a preserved terminal returns `report` / `tier1_l1_preserved`. The monotonicity property is now stated exactly (hooks `wave0` and `wave8a`, preserved rows included; `c_initial` excluded because its domain is L3 only). The 12.1 test text matches (sections 4.4, 9, 12.1).
- **B2:** every crash-recovery branch of a `sync` / `merge` push now closes its cycle with `sync_concluded{recovered: true}`: Branch A, C and halt directives in `resolve_crash_window_plan`, and Branch B in the SKILL after the re-drive. Restart and halt rows of `conflict_resume_plan` close the cycle too. A new `superseded` fold flag and row 3b fail closed on a stale open cycle. A cycle invariant is stated, and new tests cover it, including "conflict crash, then a later fix crash" (sections 4.6, 4.7, 4.8, 5.3, 6.3, 6.4, 12.2).
- **B3:** `sync_started` records `review_terminal` (the Wave 8 entering outcome; null at `C-initial`). The fold carries it, along with `hook`, in the open cycle; `ResumePlan` gains `hook`. Restart rows pass both on, and row 4c halts `resume_unrepresentable` when the value is invalid. Tests added (sections 4.6, 4.7, 4.8, 5.2, 6.3, 12.1, 12.2).
- **M6:** the rejected-push record carries the triad's `idempotency_key` and common fields, followed by `sync_concluded{halted}` (4.6 step 12).
- **M7:** `finish-merge.sh --precheck` takes only `--base-sha`; the manifest exists only for commit mode (4.6 step 5, 7.2, 8.2).
- **M8:** `conflicts.py` defines its own branch literals and never imports `recovery`; equality with `recovery.BRANCH_*` is pinned by a test (5.1, 5.2, 5.3).
- **M9:** `REPORT_REASONS` and `HALT_REASONS` overlap by design in exactly eight named reasons; whether a reason halts comes from the row's `status`. The overlap is pinned (5.2, 9).
- **M10:** new `SKILL.md` edit E13 replaces the head-binding sentence "a branch Wave 0 rebased needs a force-push ..." with "this skill never rewrites a published branch". It mentions no force flag and changes no line count (8.1, 12.1, 13).

**Revision 4** (answers `REVIEW-3.md` n1, n3, n4): `ResumePlan.target_sha` added (5.2); the SKILL's Branch B close is guarded by "cycle still open" (4.8); new test `test_branch_b_redrive_landed_closes_cycle_once` (12.2).

**Revision 3** (answers `REVIEW-2.md`; the minor notes m7 and m9 were fixed in one line each, and none is left open):

- **N1:** `conflict_resume_plan` takes `dangling` (the `detect_crash_window` result).
  - Row 4b (`crash_window`) now applies only when `dangling` belongs to the open cycle.
  - New row 4b' covers an open cycle with a dangling push that no crash record matches (an interrupted or `push_failed` Branch B re-drive). It halts `resume_unrepresentable`, closes the cycle exactly once, names `target_sha`, and never retries.
  - The following were reworded to match: the Branch B closing row, 4.6 step 12, the section 9 `push_failed` row (plus a new 4b' row), D-8, 14 V8 and 16 V8; the "exactly as in step 12" claim is gone.
  - Two tests added (a crash during the re-drive; a re-drive ending `push_failed`).
- **m1:** the 4.7 cycle invariant is restated precisely. A crash or a `push_failed` halt may leave an attempt open; the next `--resume` closes it through row 4b or 4b'.
- **m2:** row 1 (`push_rejected`) closes an open cycle; the closing rule now lists rows 1, 3b, 4c, 4b', 6 and 8.
- **m3:** `prior_conflict_cycles` excludes the current `cycle_id` everywhere, through the new pure helper `prior_conflict_cycles(...)`. A restart therefore never hits `sync_cap`, and the B3 restart test asserts `prior_conflict_cycles == 0`.
- **m4** (one line): a `c_initial` restart re-runs from step 0 with the FSM at `S2_CLASSIFY`.
- **m5:** the Branch C order (`terminal_halted` first, then `sync_concluded`) is stated as the one exception, with the reason it is safe; a test pins it.
- **m6:** the fold copies `expect_checks` from the cycle's `push_initiated` into the open-cycle entry. Row 4 reads it there, and a missing or non-bool value reads as `True`.
- **m7** (one line): "L1 proposes" and the proposal prompt are qualified with "after `clean` / `REPORT_ONLY`" in 4.2, 8.1 E10 and 8.2 row 3.
- **m8:** row 4c also checks `hook` and is evaluated before rows 4, 5 and 7 (rows are now in evaluation order).
- **m9** (one line): the section 9 overlap sentence now says `router_unreachable` always halts.

Every `file:line` below was read in this session against the worktree. Paths are repository-relative. Where this design departs from the spec, the departure is named and justified in section 10.

## 1. Summary

One release of `sc:pr-submit` that makes a PR with merge conflicts a handled case instead of a silent CI stall:

1. **Precursor.** At `--monitor 1` and above the create path no longer rebases and no longer halts when the branch is behind its base; being behind is reported (Tier 0). `--monitor 0` keeps today's rebase byte for byte.
2. **P0, detect and report (read-only).** At the end of Wave 0 (L1+) the skill checks for a git operation in progress, reads GitHub's `mergeable` / `mergeStateStatus`, and only when GitHub says `CONFLICTING` (or stays `UNKNOWN`) runs a read-only local probe (`git merge-tree --write-tree`), classifies every conflicted path into a tier, and prints the plan.
3. **P1, Tier 1 plus the publish machinery.** A conflicted root `uv.lock` (and nothing else) is regenerated with `uv lock` at Wave 8 entry ("Wave 8a"), committed as one merge commit `M = merge(PR head, base tip)`, and pushed as a plain fast-forward. New sibling gates (`merge_parent_ok`, `evaluate_sync_decision`), a push `kind` on every push record, a kind-aware run-log fold and `--resume`, a finish gate script, and an `expect_checks` CI keyword make this safe. Tier 3 (submodule, symlink, mode, protected, migration, binary, unknown lock or generated file, too many files, unclassifiable) halts at the end of Wave 0 at L3. Nothing is ever force-pushed; every existing push safeguard stays.
4. **P2, Tier 2, shipped off.** Text and tree conflicts resolved by stated intent, at `C-initial` (before the first review poll), through exactly one new FSM edge `(S2_CLASSIFY, "conflicting")` and a widened S5a re-trigger rule. Enabled only by `--conflict-max-tier 2`; the default is 1.

Proof in this release is hermetic real-git tests in pytest temporary directories (local bare repository as `origin`, `gh` stubbed, no network). Live runs are post-release follow-ups (section 14).

Net surface: one new core module (`pr_submit/conflicts.py`), two new refs, three new scripts, one changed script option, two new run-log events (41 to 43), one flag, one FSM edge. No new agent, template, FSM state or idempotency set.

## 2. Scope and binding constraints

### 2.1 Release scope

| In this release | Out of this release |
|---|---|
| Precursor (create path at L1+), P0, P1, P2 (dark) of the spec (spec section 9) | P3 late re-sync during the CI wait (#361): the `merge_state` field in the CI poll payload and a second Wave 8a trigger (spec FR-25) |
| Hermetic real-git tests, including end-to-end Tier 1 and Tier 2 local scenarios | The live gates: 5 real PRs (P0), 10 real text-conflict runs (P2), one manual live L3 run on a repository that tracks `uv.lock` (P1). They are post-release follow-ups (section 14), not release blockers |
| `--conflict-max-tier {0,1,2}`, default 1 | Flipping the default to 2 (decided after the P2 live gate, OQ-1) |

Everything in spec section 11 ("Out of scope") stays out: rebasing, history rewriting, PR splitting, external merge tools, rerere, cross-repo heads, resolving in another worktree, a user-override channel, `gh pr update-branch`, migration/submodule/binary/protected/unknown-lockfile resolution.

### 2.2 Constraints this design respects

| # | Constraint | How the design keeps it |
|---|---|---|
| C1 | Never force-push. The force-push scan (`tests/pr_submit/test_static_grep.py:758-776`) runs over every `.md` and `.sh` in the skill folder, so no new text may even mention a force flag after the words "git push" on one line | The only push text is `git push origin <target_sha>:<HEAD_BRANCH>`; prohibitions are written in words ("never forced"). A new static test (section 12.1) also requires every `git push` line in the new files to be exactly that form |
| C2 | `push_parent_ok` and `evaluate_push_decision` unchanged | Sibling functions in `conflicts.py` (`merge_parent_ok`, `evaluate_sync_decision`). `fsm.py:173-219` and `:582-600` are not edited |
| C3 | One commit per cycle | A cycle is a fix cycle (one fix commit), a sync cycle (Tier 1, one merge commit) or a merge cycle (Tier 2, one merge commit); they never share a push |
| C4 | Pre-push head guard | Every conflict push re-runs the head check with the stored `pre_push_sha`, then `merge_parent_ok`, then a base-ancestry check (section 4.6 step 10) |
| C5 | Exact-path staging; never stash; never `--no-verify`; never amend | Staging is `git add -- <path>` / `git rm -- <path>` per resolved path; the merge's own auto-merged paths are staged by git and proven by the finish gate. A static scan over the new refs and scripts forbids the literal commands (section 12.1) |
| C6 | T-N50: no `git` / `gh` token in the core-pure files (`test_static_grep.py:37-51`, `:132-143`) | `conflicts.py` joins `CORE_PURE_FILES`; `fsm.py`, `ci.py`, `state-machine.md` and `loop-guard.md` edits are written token-free. The new refs are not core-pure (they hold git commands), like `thread-reply.md` |
| C7 | Installed primitives never reference `src/superclaude/` | No new ref, script, SKILL or command text names a `src/superclaude/` path. The new scripts do not copy the existing header line `poll-ci-checks.sh:14` |
| C8 | `--repo` pinned on every `gh` call; nothing contacts the upstream | Every new `gh` line carries `--repo "$REPO"` or a `repos/<owner/repo>/` path; `probe-merge.sh` refuses to fetch unless `origin` resolves to `--repo`; fetch and push target `origin` only |
| C9 | Never stage `.claude/` (except `.claude/settings.json`) | `.claude/settings.json` and `.claude/settings.local.json` are `halt:protected` when conflicted, so no conflict cycle ever stages a `.claude/` path |
| C10 | L0 byte-identical | No hook runs at L0; the AC-1 sentence (`SKILL.md:267`, pinned at `test_static_grep.py:650-653`) is not edited |
| C11 | `SKILL.md` keeps exactly one python block (`test_cosmos_protocol.py:36`, `test_codex_reviews.py:688`) and grows by at most 15 lines | All procedure lives in the two new refs; `SKILL.md` gets prose and table rows only (section 8.1 counts the lines: +15) |
| C12 | The pinned fragments of spec section 8.4 stay byte-identical | Listed and asserted in section 12.2 |

## 3. Grounding in the current code

| # | Fact | Source (read this session) |
|---|---|---|
| G1 | `SkillArgs`, `build_arg_parser`, `parse_args` define the flag surface; `--monitor` uses argparse `choices` | `src/superclaude/pr_submit/fsm.py:50-134` |
| G2 | `evaluate_push_decision` is the INV-016 five-predicate conjunction; `push_fail_state` maps a block | `fsm.py:173-219` |
| G3 | `build_push_triad` emits `push_decision`, `push_initiated`, `push_completed` with a fixed `common` dict and no kind field; the predicates dict reads `PushDecision` fields | `fsm.py:238-288` |
| G4 | `push_parent_ok` fails closed on anything but exactly one 40-hex parent equal to `pre_push_sha` | `fsm.py:582-600` |
| G5 | `transition()` is an edge table; `(S2_CLASSIFY, "findings")` applies the round gate then goes to `S2B_VERIFY`; an unknown edge returns the same state | `fsm.py:716-802` (findings edge `:741-748`, unknown edge `:801-802`) |
| G6 | `run_skill` re-triggers only when `result.applied_edits > 0` | `fsm.py:1137` |
| G7 | L2 sets `S4_HALT_BEFORE_PUSH` when the push decision is not authorized at ordinal below 3 | `fsm.py:1118-1124` |
| G8 | `classify_checks` returns `clean` for a non-dict payload or an empty check list, `polling` on a head mismatch or an explicit `polling` with no checks | `src/superclaude/pr_submit/ci.py:22-46` |
| G9 | `EventType` has exactly 41 members; the count is stated in the module docstring and the class docstring | `src/superclaude/pr_submit/models.py:3-7`, `:22-90` |
| G10 | `RunLog.append` rejects unknown event types; its docstring says "41" | `src/superclaude/pr_submit/run_log.py:108-131` (`:111`) |
| G11 | `rebuild_state` adds every `push_completed` to `push_count` and `pushed_commit_shas`; `rereview_requested` is folded by distinct `cycle_id` | `run_log.py:161-260` (`:198-206`, `:238-241`) |
| G12 | Seven idempotency sets | `run_log.py:27-35`; pinned `tests/pr_submit/test_idempotency.py:89` |
| G13 | `detect_crash_window` treats a key as finalized by `push_completed` or `push_aborted_or_not_landed`; `resolve_crash_window` copies a fixed key tuple and returns S5a/S5 (A), `S4_PUSHING` (B), `HALT_HUMAN` (C) | `src/superclaude/pr_submit/recovery.py:57-80`, `:83-171` (tuple `:98-110`) |
| G14 | The package exports FSM, classifier, reviewer and model names through `__all__` | `src/superclaude/pr_submit/__init__.py:21-108` |
| G15 | `allowed-tools` permits `gh`, `git`, `uv`, `make`, `jq` | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:4` |
| G16 | STOP block halts when behind base on the create path; Error Handling row says the same | `SKILL.md:220-223`, `:315` |
| G17 | Wave 0 rebases on the create path at every ordinal; `--pr` never rebases | `SKILL.md:267` |
| G18 | Wave 0 head binding reads `--json headRefName,headRefOid,isCrossRepository` and binds `HEAD_BRANCH` and `pre_push_sha` | `SKILL.md:268` |
| G19 | Wave 6: one fix commit, exact-path staging, pre-push head guard, `push_parent_ok`, "The deterministic core DECIDES", `git push origin <target_sha>:<target_branch>`, S5a only when `applied_edits > 0` | `SKILL.md:274` |
| G20 | Wave 8 is SKILL-owned; wait-only after `HALT_MAX_ROUNDS` / `TERMINAL_AUGMENT_NO_RESPONSE`; an L3 CI push skips S5a/S6/RESOLVING; "Only parsed empty required **and** all-checks lists prove there are no Actions" | `SKILL.md:277` |
| G21 | `push_count` described as "== `max_rounds` at most" while Wave 6b states `push_count <= max_rounds + 1` | `SKILL.md:239` vs `:275` |
| G22 | The wait-only sentences | `refs/state-machine.md:144-146`, `refs/ci-poll.md:28-29`, `SKILL.md:277` |
| G23 | CI-poll contract: two parsed empty arrays justify `clean` | `refs/ci-poll.md:21`; script `scripts/poll-ci-checks.sh:64-78` |
| G24 | `poll-ci-checks.sh` probes `gh pr checks --help` for `--json` before any query | `scripts/poll-ci-checks.sh:39-43` |
| G25 | Pins this release edits: `test_static_grep.py:658` and `:660` (create path), `test_run_log.py:165-169` and `test_codex_reviews.py:441` (41 events) | read this session |
| G26 | `test_edge_cases.py:267` only needs one of "Wrong origin", "behind", "wrong-owner" in `SKILL.md` | read this session |
| G27 | The install test lists every installed skill file by name (presence check) | `tests/unit/test_cli_install.py:248-262`, `_assert_present` at `:496-500` |
| G28 | `uv.lock` is gitignored in this repository, so Tier 1 is a no-op here (INV-033) | `.gitignore:169`, `:222` |
| G29 | The repository runs the `check-merge-conflict` pre-commit hook (INV-032) | `.pre-commit-config.yaml:19` |
| G30 | Package version 5.0.0; the changelog has an `[Unreleased]` section; the command frontmatter says `version: "1.0"` and was not bumped by earlier pr-submit features (#337) | `pyproject.toml:7`, `CHANGELOG.md:5`, `src/superclaude/commands/pr-submit.md:9` |
| G31 | No cycle-id format rule exists anywhere in the skill or core | grep of `refs/`, `SKILL.md`, `reviewers.py` this session |
| G32 | The FX5 gate-helper drift alarm scans only the four `contract_setup` modules, so new `pr_submit` helpers are not subject to it | `tests/pr_submit/conftest.py:117-139`, `:184-196` |

Git behaviour verified in a scratch repository this session (git 2.47.3, uv 0.11.8, jq 1.7):

- `git merge-tree --write-tree -z <ours> <theirs>` writes `<tree-oid>\0`, then one `<mode> <oid> <stage>\t<path>\0` record per conflicted index entry, then an empty field, then informational messages. Exit 1 on conflicts, 0 when clean. A modify/delete with the file deleted by the base side showed stages `1` and `2` (stage set `"12"`, not `"13"` as the spec's examples say; both are classified the same way). `git merge-tree --write-tree HEAD HEAD` exits 0 (usable as a capability probe).
- A bash variable cannot hold NUL bytes, so the probe must not pass `-z` output through `$(...)`; it base64-encodes the raw bytes from a temporary file (section 7.1).
- `uv lock` and `uv lock --check` succeed offline (`UV_OFFLINE=1`) for a zero-dependency `pyproject.toml`, which makes a hermetic Tier 1 test possible.

## 4. Architecture

### 4.1 Components

```text
                  SKILL.md (sequencing, I/O, operator text)
                     |            |                 |
        lazy refs:  refs/conflict-mechanical.md   refs/conflict-intent.md (Tier 2 only)
                     |                                  |
   scripts (git I/O, one JSON line each):               |
     probe-merge.sh  (read-only: ops check, fetch origin <base>, merge-tree, numstat)
     finish-merge.sh (finish gate; the only script that commits)
     collect-conflict-evidence.sh (Tier 2: stage blobs, log, both merge-base diffs)
     poll-ci-checks.sh --evidence-sha (commit-scoped check evidence)
                     |
   deterministic core (pure, no git/gh tokens):
     conflicts.py  parse, classify, plan, route (conflict_action), gates
                   (merge_parent_ok, merge_preflight_ok, evaluate_sync_decision),
                   validation status, cycle ids, resolution record, commit message,
                   resume plans
     fsm.py        flag, should_retrigger, build_push_triad keywords, one P2 edge
     ci.py         classify_checks(expect_checks=...), expect_checks_after_push
     run_log.py    kind-aware fold, conflict cycles, open cycle, push_rejected
     recovery.py   key tuple + kind/base_sha, resolve_crash_window_plan
     models.py     +2 events (43)
```

Division of labour is the existing one (`SKILL.md:36-41`): the core decides, the SKILL sequences and performs every side effect, scripts do bounded I/O and print one JSON line. `evidence-validator` (read-only) is the only agent used, once per Tier 2 cycle.

### 4.2 Flow by hook

| Hook | When | Ordinals | What runs | Ref loaded |
|---|---|---|---|---|
| **Wave 0 operation check** | Before `gh pr create` or the `--pr` attach | L1+ | `scripts/probe-merge.sh --ops-only --repo "$REPO"`; a non-null `foreign_op` halts `foreign_op_in_progress` (on `--resume`, `conflict_resume_plan` decides first, section 4.8) | none (unless resuming an open conflict cycle) |
| **Precursor** | Wave 0 before create | L0 rebases if behind (unchanged); L1+ reports "N commits behind" | none | none |
| **Wave 0 conflict check** | After the head binding | L1+ | `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus`, re-read up to 3 times 10 s apart while `UNKNOWN`; `mergeability_hint`; if `needs_probe`: `probe-merge.sh` full mode, `conflict_plan`, print the plan (FR-4), `conflict_action(hook="wave0")` | `conflict-mechanical.md` only when the probe runs |
| **C-initial** | Wave 1, after the run-log is initialized and the monitor armed, before the first review poll | L3 only, only when Wave 0 returned reason `tier2_planned` | GitHub re-read, re-probe, `conflict_plan`, `conflict_action(hook="c_initial")`; on `resolve_push`: `transition(S2_CLASSIFY, "conflicting")` and the merge cycle of section 4.6 with push kind `merge` | `conflict-mechanical.md` and `conflict-intent.md` |
| **Wave 8a** | Wave 8 entry, after the review outcome is one of `clean` / `REPORT_ONLY` / `HALT_MAX_ROUNDS` / `TERMINAL_AUGMENT_NO_RESPONSE`, before the CI poll loop | L1+ | GitHub re-read; when `needs_probe`: re-probe, `conflict_plan`, `conflict_action(hook="wave8a", entering=...)`; Tier 1 cycle with push kind `sync` at L3, local resolution at L2, proposal at L1 (after `clean` / `REPORT_ONLY` only); otherwise the CI-wait skip and the status of section 4.5 | `conflict-mechanical.md` only when the probe runs |
| **End of the CI wait** | Before sending `transition(clean)` | L1+ | When any hook this run read `conflicting` (or the run was resumed), one more `gh pr view ... --json mergeable`; `CONFLICTING` means no `transition(clean)`: `terminal_halted`, reason `late_conflict` (re-sync is #361) | none |

A Tier 0 run therefore costs one `ops-only` probe call (local, no fetch) and one `gh pr view` read per hook (Wave 0 and Wave 8a), plus up to 3 re-reads on `UNKNOWN`. It loads no ref, runs no fetch, no model reasoning and no agent (NFR-4, restated per hook, see section 10.5 D-12).

### 4.3 Tier model and classification rules

**Inputs.** The probe JSON (section 7.1), parsed by `parse_probe`: the raw `merge-tree -z` bytes, the two `numstat -z` listings that mark binary paths, and the list of rule programs found on PATH. `group_entries` builds one `ConflictEntry` per path: `stages` is the sorted string of stages present (`"123"`, `"12"`, `"13"`, `"23"`, ...), `modes` and `oids` per side (`base` = stage 1, `ours` = stage 2 = the PR head, `theirs` = stage 3 = the base tip), `binary` from either numstat listing.

**Per-path class: first matching rule wins** (`classify_path`):

| Order | Rule | Class | Research |
|---|---|---|---|
| 0 | path contains a control character (any code point below 0x20, or 0x7f) | `halt:unsafe_path` | fail closed; lets every script use tab/newline-separated manifests safely |
| 1 | any side mode `160000` | `halt:submodule` | R-43, R-56 |
| 2 | any side mode `120000` | `halt:symlink` | fail closed |
| 3 | `ours` and `theirs` both present and their modes differ | `halt:mode_change` | fail closed |
| 4 | path starts with `.github/workflows/` or `.github/actions/`, or equals `.claude/settings.json` or `.claude/settings.local.json` | `halt:protected` | blast radius; C9 |
| 5 | a path segment sequence is `migrations`, `alembic/versions` or `db/migrate` | `halt:migration` | R-54, S-53 |
| 6 | `binary` is true | `halt:binary` | R-57 |
| 7 | path equals a `MechanicalRule.pattern` exactly (root-anchored; shipped: `uv.lock`), `stages == "123"`, and every program in the rule's `regenerate` and `check` argv[0] is in the probe's `programs` list | `regen:<pattern>` | R-58, R-189, J-48, INV-025, INV-033 |
| 8 | basename is in `LOCKFILE_NAMES` (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, `Pipfile.lock`, `flake.lock`, `uv.lock`) or ends in `.lock` | `halt:lockfile_no_recipe` | R-59, J-48 |
| 9 | a path segment is `generated`, `dist`, `build` or `__snapshots__`, or the basename contains `.generated.` or ends in `.snap` | `halt:generated_no_recipe` | R-59, R-60 (snapshots fold in here) |
| 10 | `stages == "123"` | `text:content` | R-149 |
| 11 | `stages in {"12", "13"}` | `text:modify_delete` | R-154, S-39 |
| 12 | `stages == "23"` | `text:add_add` | S-40 |
| 13 | anything else | `halt:unknown_shape` | fail closed |

A tracked `uv.lock` is implied by stage set `123` (it exists in the base, ours and theirs trees), so no separate "tracked" fact is needed; an ignored `uv.lock` never conflicts. A nested `pkg/uv.lock` fails rule 7 (not the exact root path) and lands in rule 8.

**Plan tier** (`conflict_plan`, first matching row):

| Condition | Tier | Plan reason |
|---|---|---|
| `hint` is `clean`, `behind` or `blocked` (GitHub `MERGEABLE`; `blocked` is `mergeStateStatus == BLOCKED`, its own row); no probe was run | 0 | `no_conflict`, `behind_only` or `blocked` |
| the probe script exited 2 (`probe_failed=True`) | `None` (unclassified) | `probe_failed` |
| probe JSON parsed, `merge_tree_supported` false | `None` | `merge_tree_unsupported` |
| probe JSON malformed, truncated, or any field invalid | 3 | `probe_malformed` |
| probe `clean` true (no conflicted path) | 0 | `no_conflict` (plus `github_disagrees` when the hint was `conflicting`) |
| at least one `halt:*` class | 3 | the first halt class, for example `halt:binary` |
| more than `TIER2_MAX_FILES` (8) `text:*` paths | 3 | `too_many_files` |
| at least one `text:*` path (`regen:*` paths may accompany them) | 2 | `text_conflict` |
| every path is `regen:*` | 1 | `regen_only` |

`regen:*` paths do not count toward `TIER2_MAX_FILES` (OQ-9). In a Tier 2 cycle, `regen:*` paths are handled by their rule after the text paths are resolved and staged (manifest first, R-58), so a conflicted `pyproject.toml` plus `uv.lock` is Tier 2 (OQ-10).

**Escalation is monotone inside a cycle**: a cycle that starts as Tier 1 or 2 can escalate to Tier 3 (halt) at any step and never de-escalates or retries in the same run. Between hooks, the latest probe decides (OQ-23).

### 4.4 The routing table (`conflict_action`)

`conflict_action` is the only conflict routing decision (spec FR-26). Notation: `P` = the Wave 8 entering outcome is a preserved terminal (`halt_max_rounds` or `no_response`); `H` = `None` when `P`, else `"terminal_halted"`. `status = None` means "continue the run"; a non-`None` status ends the run with that output-contract status (the SKILL appends `terminal_halted{reason}` for `terminal_halted`). Rows are evaluated top to bottom inside each hook.

**Domain guard (evaluated first).** Any input outside its domain gives the fail-closed default row `ConflictAction("halt", "router_unreachable", "terminal_halted", skip_ci=True)`: `hook` not in `("wave0", "c_initial", "wave8a")`; `ordinal` not an int in 0..3; `conflict_max_tier` not an int in 0..2; `plan_tier` not in `{None, 0, 1, 2, 3}`; `round_counter`, `max_rounds` or `prior_conflict_cycles` not a non-negative int; `entering` not `None` at `wave0` / `c_initial`; `entering` not in `("clean", "report_only", "halt_max_rounds", "no_response")` at `wave8a`; `c_initial` at an ordinal other than 3. Then `ordinal == 0` at any valid hook gives `ConflictAction("none", "l0")` (L0 never calls the router; this row only makes a mistaken call harmless). The caller always passes `prior_conflict_cycles` = distinct ids in `conflict_cycles` other than the current `cycle_id` (section 4.8), so a resume restart of a cycle is not counted against `SYNC_CAP` by its own earlier attempt.

**`wave0`** (ordinals 1 to 3):

| Plan tier | Condition | action | reason | status |
|---|---|---|---|---|
| `None` | | `report` | the plan reason (`probe_failed` / `merge_tree_unsupported`) | `None` |
| 0 | | `report` | the plan reason | `None` |
| 1 | `conflict_max_tier < 1` | `report` | `tier_above_cap` | `None` |
| 1 | | `report` | `tier1_planned` | `None` |
| 2 | `conflict_max_tier < 2` | `report` | `tier_above_cap` | `None` |
| 2 | `ordinal < 3` | `report` | `tier2_report_only` | `None` |
| 2 | `ordinal == 3` | `report` | `tier2_planned` | `None` |
| 3 | `ordinal < 3` | `report` | `conflict_tier3` | `None` |
| 3 | `ordinal == 3` | `halt` | `conflict_tier3` | `terminal_halted` |

**`c_initial`** (ordinal 3 only; entered only after a `wave0` result of `tier2_planned`; the plan is the fresh re-probe):

| Plan tier | Condition | action | reason | status | extras |
|---|---|---|---|---|---|
| `None` | | `report` | the plan reason | `None` | |
| 0 | | `none` | `no_conflict` | `None` | |
| 1 | | `none` | `tier1_deferred` (Wave 8a acts) | `None` | |
| 2 | `conflict_max_tier < 2` | `report` | `tier_above_cap` | `None` | |
| 2 | `max_rounds - round_counter < 2` | `report` | `no_round_budget` | `None` | |
| 2 | `prior_conflict_cycles >= SYNC_CAP` | `report` | `sync_cap` | `None` | |
| 2 | | `resolve_push` | `tier2_merge` | `None` | `fsm_event="conflicting"`, `push_kind="merge"` |
| 3 | | `halt` | `conflict_tier3` | `terminal_halted` | |

**`wave8a`** (ordinals 1 to 3; `skip_ci` is true on every row except the two marked):

| Plan tier | Condition | action | reason | status | extras |
|---|---|---|---|---|---|
| `None` | | `halt` if `H` else `report` | the plan reason | `H` | |
| 0 | `github_conflicting` false | `none` | `no_conflict` | `None` | `skip_ci=False` |
| 0 | `github_conflicting` true | `halt` if `H` else `report` | `github_disagrees` | `H` | |
| 1 | `conflict_max_tier < 1` | `halt` if `H` else `report` | `tier_above_cap` | `H` | |
| 1 | `prior_conflict_cycles >= SYNC_CAP` | `halt` if `H` else `report` | `sync_cap` | `H` | |
| 1 | `ordinal == 1` and `P` | `report` | `tier1_l1_preserved` | `None` | |
| 1 | `ordinal == 1` | `propose` | `tier1_proposed` | `"proposed"` | |
| 1 | `ordinal == 2` and `P` | `report` | `tier1_l2_preserved` | `None` | |
| 1 | `ordinal == 2` | `resolve_local` | `tier1_local` | `"halt_before_push"` | |
| 1 | `ordinal == 3` | `resolve_push` | `tier1_sync` | `None` | `skip_ci=False`, `push_kind="sync"` |
| 2 | `conflict_max_tier < 2` | `halt` if `H` else `report` | `tier_above_cap` | `H` | |
| 2 | | `halt` if `H` else `report` | `late_conflict` | `H` | |
| 3 | | `halt` if `H` else `report` | `conflict_tier3` | `H` | |

Properties pinned by tests (section 12.1): every reachable row is asserted; the default row is reached by each domain violation; **ordinal monotonicity**, stated exactly: for `hook` in `("wave0", "wave8a")` and every fixed value of the other inputs inside their domains (`plan_tier`, `entering` valid for the hook, `conflict_max_tier`, `round_counter`, `max_rounds`, `prior_conflict_cycles`, `github_conflicting`), and for `L` in 0, 1, 2: `rank(action(L)) <= rank(action(L+1))`, with `rank`: `none` 0, `report` 1, `halt` 1, `propose` 2, `resolve_local` 3, `resolve_push` 4 (INV-010). Preserved-terminal rows are included and satisfy it (Wave 8a Tier 1 with `P`: L1 `report`, L2 `report`, L3 `resolve_push`). `c_initial` is excluded by definition: its domain is L3 only, and an L0 to L2 call reaches the fail-closed default row, which is a domain violation, not a lower ordinal doing less. Tier 2 is acted on only at L3 at `C-initial`; at L1 and L2 Tier 2 is reported and never resolved (OQ-21).

### 4.5 Final status rules

| Situation | Status | Event |
|---|---|---|
| Tier 3 at the end of Wave 0, L3 | `terminal_halted` | `terminal_halted{reason: conflict_tier3, tier: 3, paths}` (appended to the run-log when one exists, the `SKILL.md:268` shape) |
| A `wave8a` row with `status = "terminal_halted"` (entered from `clean` / `REPORT_ONLY`) | `terminal_halted` | `terminal_halted{reason}`; the FSM takes the human-gate route to `HALT_HUMAN`; the CI wait is skipped with reason `pr_conflicting` |
| A `wave8a` row with `status = None` and `P` | the preserved status (`terminal_max_rounds` or `terminal_augment_no_response`) | none; the conflict reason is reported alongside it, the same shape as a CI human-gate (`SKILL.md:250`) |
| L1 Tier 1 at Wave 8a from `clean` / `REPORT_ONLY` | `proposed` | none; the plan and `CONFLICT_PROPOSE_PROMPT` are printed; CI wait skipped `pr_conflicting` |
| L2 Tier 1 resolved at Wave 8a from `clean` / `REPORT_ONLY` | `halt_before_push` | `sync_concluded{left_in_progress}`; the caller sets `S4'_HALT_BEFORE_PUSH` (`fsm.py:1118-1124` precedent) |
| A conflict cycle halts mid-way | `terminal_halted` (or the preserved status when `P`; `VALIDATION_FAIL` maps to `terminal_halted`) | `sync_concluded{halted or aborted}` then `terminal_halted{reason}` |
| CI clean after a run that saw a conflict, but `mergeable` reads `CONFLICTING` again | `terminal_halted`, reason `late_conflict` | `terminal_halted{reason: late_conflict}`; never `transition(clean)` (INV-027) |
| CI wait expires after a conflict push with `expect_checks` true and no check ever registered | the existing Wave 8 CI timeout outcome | the report line carries reason `ci_not_started`; never `clean`, never "tests passed" |

The `status` enum (`SKILL.md:236`) gains no member.

### 4.6 The merge cycle procedure

Runs for `resolve_push` (Tier 1 at Wave 8a with push kind `sync`; Tier 2 at `C-initial` with push kind `merge`) and `resolve_local` (Tier 1 at Wave 8a, L2, stops after step 8). L1 never starts it. This is the normative order that `refs/conflict-mechanical.md` carries; each failure names its halt reason (section 9). "Abort" always means `git merge --abort`, allowed only after `MERGE_HEAD == base_sha` was verified, followed by `sync_concluded{aborted}`.

The Wave 8 entering outcome (`clean`, `report_only`, `halt_max_rounds` or `no_response`; null at `C-initial`) is called `review_terminal` throughout the cycle: it is the `entering` argument of every `conflict_action` call, it is written into `sync_started` (step 3), and it is passed to `build_push_triad` (step 11), so a resumed cycle has a durable source for it (section 4.8).

| Step | Action | On failure |
|---|---|---|
| 0 | Tier 2 only: `transition(S2_CLASSIFY, "conflicting", {monitor_ordinal, round_counter, max_rounds})`. `HALT_MAX_ROUNDS` ends the cycle before anything is touched (unreachable after the router's `no_round_budget` row, kept as the FSM's own gate). | n/a |
| 1 | **Head check.** The hook's single GitHub read is `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,isCrossRepository`. Require `pr_head_ok(<local branch>, <local HEAD>, headRefName, headRefOid, isCrossRepository)`, `headRefName == HEAD_BRANCH`, local `HEAD == pre_push_sha`, and `HEAD_BRANCH != baseRefName` (J-26). The checkout is the current worktree (J-91); a detached HEAD fails `pr_branch_ok` (J-15). | `sync_head_mismatch`; nothing started |
| 2 | **Fresh probe.** The hook's `probe-merge.sh` call (it runs after step 1 at an acting hook, so the cycle uses exactly one probe). Require `foreign_op == null` (J-16, J-17) and `merge_preflight_ok(<decoded status_b64>)` (tracked tree clean, untracked tolerated; J-18, INV-008). `plan := conflict_plan(...)`; route again with `conflict_action`; only `resolve_push` / `resolve_local` continue. | `sync_foreign_operation`; `merge_preflight_dirty` naming the files (never stash, J-20); nothing merged |
| 3 | **Write-ahead.** `cycle_id := conflict_cycle_id(tier, len(conflict_cycles) + 1)` (or the reused open cycle id on a resume restart). Append `sync_started{...}` (section 4.7). | n/a |
| 4 | **Merge by SHA.** `git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>` (per-invocation config only; no stored config; rerere off, R-128; hooks on). Then read `git diff --name-only --diff-filter=U` and require it to equal the plan's conflicted path set. | exit 1 without `MERGE_HEAD` (git refused, for example local changes would be overwritten): `sync_merge_failed`, git's file list in the message, `sync_concluded{halted}`. Exit 0, or an unmerged set that differs from the probe: abort, `sync_merge_failed` (the probe and the merge disagree on the same `base_sha`) |
| 5 | **Resolve.** Tier 1: `scripts/finish-merge.sh --base-sha <base_sha> --precheck` (worktree changes only on unmerged paths; precheck mode takes no manifest, which is written only at step 9), then for the `uv.lock` rule: `git checkout --ours -- uv.lock`, `uv lock`, `uv lock --check`, `git add -- uv.lock` (R-58, R-189, S-46). Tier 2: `refs/conflict-intent.md`, one file at a time (J-40), staging each finished path with `git add -- <path>` or `git rm -- <path>` (J-56); then any `regen:*` path by its rule after `--precheck`. | precheck `tree_dirty`: abort, `merge_preflight_dirty`. A `uv` command fails: abort, `sync_merge_failed` (no retry loop). Tier 2 halt conditions: abort, `sync_tier3` |
| 6 | **Tier 2 only: record and grounding check.** Write `<output-dir>/sync/<cycle_id>/resolution.md`; `resolution_record_ok(parse_resolution_record(text), plan.text_paths)` must return `[]`; spawn `evidence-validator` once over `resolution.md` and the evidence directory; one revision pass. | still unsupported after one revision, or any record problem: abort, `sync_tier3` |
| 7 | **VAL.** Tier 1 results: `VG-1` = the rule's check command (`uv lock --check`; the changed area is the lock file, which has no tests), `VG-3`, `VG-4`, `VG-5` only when a resolved path is under a synced component. Tier 2: `VG-1` targeted tests over the resolved paths (plus the rule check when a `regen:*` path is in the cycle), `VG-2` `make test` mandatory, `VG-3`, `VG-4`, `VG-5` when applicable. `validation_status := conflict_validation_status(tier, results)`. One retry, which must not introduce changes unrelated to the failure (R-169) and does not tick `round_counter`. Tier 1 adds the report line "no tests ran for the regenerated lock file; CI on the merge head is the test signal". | red after the retry: abort, `sync_validation_failed` (Tier 2: `transition(S7_VALIDATING, "validation_failed")` to `VALIDATION_FAIL`). The message notes that a red base can cause this and names the command to check `origin/<base>` (OQ-26) |
| 8 | **L2 stops here** (`resolve_local`): `sync_concluded{left_in_progress}`, status `halt_before_push`, operator text: "The merge of `origin/<base>`@<base_sha> is resolved and validated but not committed. Review it, then run `git commit` yourself and push; or `git merge --abort`." | n/a |
| 9 | **Finish gate and commit.** Write the message file (`merge_commit_message(...)` plus the session's attribution lines, OQ-13) and the manifest (`finish_manifest(listing, resolved_paths)`), then `scripts/finish-merge.sh --base-sha <base_sha> --merge-tree-oid <oid> --manifest <file> --message-file <file>` (section 7.2). `target_sha := merge_sha`. | `FINISH_FAIL` token mapped per section 7.2. `hook_rejected`: hook output verbatim (J-61), merge left in progress with the resolution intact, no amend (J-63), `sync_commit_failed`. `tree_dirty` after the commit: `merge_preflight_dirty`, the local merge commit named, nothing pushed |
| 10 | **Pre-push head guard (order: head, parent, base ancestry; X-009).** (a) Re-read `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository`; require `pr_head_ok(<local branch>, pre_push_sha, ...)` and `headRefName == HEAD_BRANCH` (the stored `pre_push_sha`, never local HEAD). (b) `git rev-list --parents -n 1 <target_sha>`, drop the first id, require `merge_parent_ok(<parents>, pre_push_sha, base_sha)`. (c) `git fetch origin <base>` then `git merge-base --is-ancestor <base_sha> origin/<base>`. Before the first conflict push of the run, read `gh repo view "$REPO" --json mergeCommitAllowed,rebaseMergeAllowed,squashMergeAllowed` and print one advisory line; never halt on it (OQ-32). | (a) `sync_head_mismatch`; (b) `sync_range_mismatch`; (c) `sync_base_moved`. All: nothing pushed, no push record, the local merge commit named so the operator can push or drop it |
| 11 | **Core DECIDES.** `decision := evaluate_sync_decision(...)`; blocked means `sync_fail_state(decision)` and nothing is pushed. `expect_checks := expect_checks_after_push(checks_seen_this_run=..., pre_push_evidence=<poll-ci-checks.sh --evidence-sha pre_push_sha>, base_evidence=<... base_sha>)`. Then `build_push_triad(..., decision=decision, push_kind=<"sync" or "merge">, base_sha=base_sha, review_terminal=<the cycle's review_terminal, sync only>, expect_checks=expect_checks)`; append `push_decision`, then `push_initiated` (fsynced before the push), keyed on the unchanged pre-push key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`. | `sync_cap` (s4) or report-only (s1, s2); `HALT_HUMAN` (s3) |
| 12 | **Push.** `git push origin <target_sha>:<HEAD_BRANCH>` (origin only, never the default or protected branch, never forced). Exit 0: append `push_completed`, then `pre_push_sha := target_sha`; read `mergeStateStatus` once and print a reason line if it is `BLOCKED`. | Non-zero exit whose stderr contains `[rejected]`, `non-fast-forward`, `fetch first` or `hook declined`: append `push_aborted_or_not_landed{rejected: true, stderr_tail}` carrying the triad's `idempotency_key` and common fields (`run_id`, `cycle_id`, `pre_push_sha`, `target_sha`, `target_branch`, `target_remote`, `kind`, `base_sha`), so `detect_crash_window` (`recovery.py:66-76`) treats the key as finalized, then `sync_concluded{halted, reason: push_rejected}`, and halt `push_rejected` (never re-driven, INV-035). Any other non-zero exit (network, auth, a local pre-push hook): no record, the `push_initiated` stays dangling and the cycle stays open (no `sync_concluded`), halt `push_failed` with stderr verbatim (J-77, J-83). For the cycle's **first** push, `--resume` settles it by the existing three-way remote check (section 4.8 row 4b) and closes the cycle. For a **Branch B re-drive**, the key is already finalized, so `--resume` halts `resume_unrepresentable` and closes the cycle without retrying (row 4b') |
| 13 | **After the push.** Tier 1: append `sync_concluded{pushed, merge_sha}`; re-enter the Wave 8 CI wait with `wait_sha := target_sha` and the recorded `expect_checks`; no re-trigger, no reply, no resolve (`SKILL.md:277` CI-push precedent). Tier 2: append `sync_concluded{pushed, merge_sha}`; `transition(S4_PUSHING, "pushed")`, `S6_REPLYING` and `RESOLVING` with zero threads, `should_retrigger(0, "merge")` is true, so S5a re-triggers the configured reviewers (section 8.3), then the S5 wait is the run's first review wait | n/a |

Revert of a pushed merge commit is always a new commit, `git revert -m 1 <merge_sha>`; the L2 and L3 reports print it (K13).

### 4.7 Run-log events, push kinds and counting

**Two new event types (41 to 43), used by both conflict tiers** (OQ-17 / C-029 / X-011):

| Event | Written | Payload (all required unless marked) |
|---|---|---|
| `sync_started` | step 3, before the merge command (write-ahead) | `run_id`, `cycle_id` (`sync-<n>` for Tier 1, `conflict-<n>` for Tier 2), `tier` (1 or 2), `kind` (`"sync"` or `"merge"`), `hook` (`"wave8a"` or `"c_initial"`), `base_ref` (`origin/<base>`), `base_sha`, `pre_push_sha`, `merge_tree_oid`, `conflict_max_tier`, `review_terminal` (the Wave 8 entering outcome `clean` / `report_only` / `halt_max_rounds` / `no_response` when `hook == "wave8a"`; null when `hook == "c_initial"`), `paths` (list of conflicted paths), `resumed` (bool, true on a resume restart) |
| `sync_concluded` | when the cycle ends, including every crash-recovery branch of a conflict push (section 4.8, "Closing the cycle") | `cycle_id`, `outcome` in `{pushed, left_in_progress, aborted, halted}`, `merge_sha` (or null), `record_path` (or null; Tier 2), `dropped` (list of strings; Tier 2, empty for Tier 1), `reason` (or null), `recovered` (bool, true when appended by the resume path) |

**Invariant (stated precisely).** For each `sync_started` (an attempt of a cycle), exactly one `sync_concluded` for the same `cycle_id` is appended, and it is appended before any `push_initiated` of another cycle. It comes at the latest in the first `--resume` that reads the run-log. The only ways an attempt can be left open at the end of a session are:

1. a crash; or
2. a `push_failed` halt (section 4.6 step 12, or a failed Branch B re-drive), which deliberately leaves the cycle open with its `push_initiated` dangling.

In both cases the next `--resume` closes it, through row 4b (the three-way remote check) or row 4b' (halt), never through a later cycle's rows. A resume restart closes the old attempt (`sync_concluded{aborted}`) before re-opening the same id with `sync_started{resumed: true}`, and the new attempt follows the same rule. A run whose operator never resumes after a `push_failed` halt keeps the attempt open in its log. That is harmless, because the run has ended `terminal_halted`, and the output contract reports `sync_outcome: halted`.

Report-only detection writes no event (the plan is printed); every halt reuses `terminal_halted` with a `reason` (section 9). No other event type is added.

**Push kinds.** `kind` in `{"fix", "merge", "sync", "ci"}` is written on all three push records through `build_push_triad(..., push_kind=...)`. Absent means `fix`, so legacy run-logs and the existing fix-push record shape are unchanged. Wave 6 fix pushes keep calling the builder without `push_kind`. The Wave 8 CI push passes `push_kind="ci"`, `review_terminal` and `expect_checks=True` (closes INV-002). Sync and merge pushes also pass `base_sha`; `sync` and `ci` pass `review_terminal` (the Wave 8 entering outcome: `clean`, `report_only`, `halt_max_rounds` or `no_response`).

**Counting** (INV-018):

| Counter | Rule |
|---|---|
| `push_count` | every landed `push_completed` whose `kind` is absent, `fix`, `ci` or `merge`; Tier 1 sync pushes are excluded. Bound: `push_count <= max_rounds + 1` (the fallback's one push), which is what `SKILL.md:275` already states; `SKILL.md:239` is reworded to match |
| `sync_push_count` | landed `push_completed` with `kind: "sync"`; at most `SYNC_CAP = 1` |
| `conflict_cycles` | distinct `cycle_id`s of `sync_started`, first-seen order; `SYNC_CAP = 1` bounds this list for the whole run, across both tiers (INV-019) |
| `round_counter` | unchanged rule: ticks only on the INV-001 edge. A Tier 2 merge cycle ticks once when its re-review is attributed; a Tier 1 sync cycle never ticks |
| `rereview_request_count` | Tier 2: +1 per merge cycle (folded by `cycle_id`); Tier 1: unchanged |
| `pushed_commit_shas` | every landed push, any kind (unchanged) |

**Event sequences.**

```text
L3 Tier 1 (Wave 8a):  sync_started -> push_decision{kind:sync} -> push_initiated{kind:sync} -> push_completed{kind:sync}
                      -> sync_concluded{pushed} -> (CI wait on target_sha, expect_checks)
L2 Tier 1 (Wave 8a):  sync_started -> sync_concluded{left_in_progress}           status halt_before_push
L3 Tier 2 (C-initial): sync_started{tier:2} -> push_decision{kind:merge} -> push_initiated{kind:merge}
                      -> push_completed{kind:merge} -> sync_concluded{pushed} -> rereview_requested{cycle_id}...
                      -> (S5 wait) -> round_incremented
Halt mid-cycle:       sync_started -> ... -> sync_concluded{aborted|halted, reason} -> terminal_halted{reason}
Halt before a cycle:  terminal_halted{reason}            (for example conflict_tier3, foreign_op_in_progress)
Rejected push:        ... push_initiated -> push_aborted_or_not_landed{rejected:true, stderr_tail}
                      -> sync_concluded{halted, reason: push_rejected} -> terminal_halted{reason: push_rejected}
```

**Cycle ids.** `sync-` and `conflict-` are reserved prefixes (`is_conflict_cycle`). Fix cycles have no format rule today (G31); `refs/loop-guard.md` gains the sentence that a fix cycle's `cycle_id` never starts with either prefix, and a test proves `is_conflict_cycle` rejects representative fix-cycle ids.

### 4.8 Resume

Two pure planners decide; the SKILL acts.

**`conflict_resume_plan(state, *, foreign_op, merge_head_sha, local_head_sha, local_head_parents, dangling)`**: called on `--resume` right after the Wave 0 operation check. Inputs:

- `state = rebuild_state()`;
- the facts from `probe-merge.sh --ops-only`, plus `git rev-parse HEAD` and `git rev-list --parents -n 1 HEAD`;
- `dangling = recovery.detect_crash_window(run_log)` (the record or `None`).

Rows are evaluated in table order (the labels are identifiers, not positions); the first match wins:

| # | Condition | `directive` | Reason / note |
|---|---|---|---|
| 1 | `state["push_rejected"]` | `halt` | `push_rejected` (a rejected push is never re-driven); when a cycle is still open (a crash between the rejected record and its `sync_concluded`), it is closed per the rule below |
| 2 | no open conflict cycle, `foreign_op` is null | `none` | normal resume (the existing head binding and crash-window check follow) |
| 3 | no open conflict cycle, `foreign_op` non-null (including an L2 `left_in_progress` merge) | `halt` | `foreign_op_in_progress` |
| 3b | the open cycle is `superseded` (a `push_initiated` of another cycle was written after it; only possible if an earlier recovery failed to close it) | `halt` | `resume_unrepresentable`; fail closed rather than route by a stale cycle |
| 4c | the open cycle's `hook` is missing or not in `("wave8a", "c_initial")`; or `hook == "wave8a"` and its `review_terminal` is missing or not in `ENTERING_OUTCOMES`; or `hook == "c_initial"` and `review_terminal` is not null | `halt` | `resume_unrepresentable` (B3: rows 4, 5 and 7 need a valid `hook` and `review_terminal`; checked before any of them) |
| 4 | the open cycle has a `push_completed` (crash after the push, before `sync_concluded`) | `complete_after_push` | append `sync_concluded{pushed, recovered: true}`. `sync`: enter the Wave 8 CI wait at `wait_sha = target_sha` with `expect_checks` taken from the open-cycle entry; the fold copies it from the cycle's `push_initiated`, and a missing or non-bool value reads as `True` (fail closed: never a false `clean`). `merge`: resume at `S5A_RETRIGGER_REVIEW` (`pending_retriggers` posts only the reviewers still missing) |
| 4b | the open cycle has a `push_initiated` and no `push_completed`, **and** `dangling` is a record whose `cycle_id` equals the open cycle's | `crash_window` | `resolve_crash_window_plan` settles it by the three-way remote check and closes the cycle (below). This is reached by a crash, or by a `push_failed` of the cycle's **first** push (step 12) |
| 4b' | the open cycle has a `push_initiated` and no `push_completed`, and `dangling` is `None` or belongs to another cycle | `halt` | `resume_unrepresentable`: the push record's key was already finalized by an earlier Branch B record, so `detect_crash_window` cannot match it. This happens with a crash during a Branch B re-drive, or a re-drive that ended `push_failed` (N1). No push is retried. Append `sync_concluded{halted, reason: resume_unrepresentable, recovered: true}` once. The message names `cycle_id` and `target_sha` and tells the operator to compare them with the PR head (`gh pr view <N> --repo "$REPO" --json headRefOid`): if the PR head equals `target_sha`, the merge landed, so re-run with `--pr <N>`; otherwise push or drop the local merge commit yourself, then re-run |
| 5 | `foreign_op == "MERGE_HEAD"` and `merge_head_sha` equals the open cycle's `base_sha` | `abort_and_restart` | our own interrupted merge: abort it (ownership verified), append `sync_concluded{aborted, recovered: true}`, and restart the cycle under the same `cycle_id` (`sync_started{resumed: true}`) at the open cycle's `hook`, with `entering := review_terminal` from the open cycle (carried in `ResumePlan.hook` and `ResumePlan.review_terminal`). A `wave8a` cycle restarts at step 1. A `c_initial` cycle restarts at step 0 with the FSM set to `S2_CLASSIFY` (no review has run before `C-initial`, so this equals the first attempt; `round_counter` is unchanged because rounds tick only on the INV-001 edge) |
| 6 | `foreign_op` non-null otherwise | `halt` | `sync_foreign_operation` (J-17) |
| 7 | `local_head_sha == open.pre_push_sha` | `restart` | the merge never started or was aborted; append `sync_concluded{aborted, recovered: true}` and restart under the same `cycle_id`, `hook` and `review_terminal`, at the same step as row 5 |
| 8 | anything else, including a local two-parent commit `[pre_push_sha, base_sha]` with no `push_initiated` | `halt` | `resume_unrepresentable`: a local merge commit that no `push_initiated` covers is never pushed without its finish gate and VAL (OQ-22); the message names it so the operator can push or drop it |

**Closing rule for the resume rows.** Every `halt` row that finds an open cycle (1, 3b, 4c, 4b', 6, 8) appends `sync_concluded{halted, reason, recovered: true}` exactly once, before `terminal_halted`. The `ResumePlan` carries `cycle_id` so the SKILL appends for that id only, and only when `rebuild_state()["open_conflict_cycle"]` still names it. Restart rows close the old attempt with `sync_concluded{aborted}` before the new `sync_started{resumed: true}`; the fold treats the pair as one cycle id (`conflict_cycles` counts it once).

**`prior_conflict_cycles` at a restart.** Everywhere it is computed (the `conflict_action` call at the restarted hook and `evaluate_sync_decision` at step 11), `prior_conflict_cycles` is the number of distinct ids in `conflict_cycles` **other than the current `cycle_id`**. For a fresh cycle the new id is not yet in the list, so the count equals `len(conflict_cycles)`. For a restart the reused id is excluded, so a restart never hits `sync_cap` because of its own earlier attempt.

**`crash_resume_plan(dangling, branch, fsm_state)`**: called by `recovery.resolve_crash_window_plan` after the unchanged `resolve_crash_window` has appended its recovery event. `kind := dangling.get("kind") or "fix"`.

| `kind` | Branch A (landed) | Branch B (not landed) | Branch C (ambiguous) |
|---|---|---|---|
| `fix`, absent | `fsm`, `state = fsm_state` (S5a or S5, byte-equal to today) | `fsm`, `S4_PUSHING` (today) | `halt`, `HALT_HUMAN`, `ambiguous_remote_tip` (today) |
| `merge` | `fsm`, `fsm_state` (S5a or S5; S5a re-triggers because `should_retrigger(0, "merge")`) | `fsm`, `S4_PUSHING`, `check_merge_parent=True`, `base_sha` from the record: the re-driven push runs the head guard with the record's `pre_push_sha` and `merge_parent_ok` instead of `push_parent_ok` | as `fix` |
| `sync` | `wave8_ci_wait`, `wait_sha = target_sha`, `review_terminal` and `expect_checks` from the record | `redrive_then_wave8`, `rerun_guard=True`, `check_merge_parent=True`; after the re-driven push, the same Wave 8 directive | as `fix` |
| `ci` | `wave8_ci_wait` as `sync` | `redrive_then_wave8`, `rerun_guard=True`, `check_merge_parent=False` (the guard's `push_parent_ok` applies) | as `fix` |
| unknown string | `halt`, `resume_unrepresentable` | same | same |

For `sync` and `ci`: a missing or unknown `review_terminal`, or (for `sync`) a missing 40-hex `base_sha`, gives `halt`, `resume_unrepresentable`. A missing `expect_checks` reads as true (fail closed). `sync` and `ci` never resume into `S4_PUSHING`, S5a or S5 (INV-001). The recovered `push_completed` (Branch A) copies `kind` and `base_sha` so the fold counts it under the right kind.

**Closing the cycle on every crash-recovery branch (B2).** For a dangling push of kind `sync` or `merge` (a conflict cycle), the cycle is closed exactly once:

| Branch | Who appends | What |
|---|---|---|
| A (landed) | `recovery.resolve_crash_window_plan`, right after `resolve_crash_window` appended the recovered `push_completed` | `sync_concluded{cycle_id, outcome: pushed, merge_sha: target_sha, recovered: true}` |
| B (not landed) | the SKILL, after the re-driven push, and only while `rebuild_state()["open_conflict_cycle"]` still names the dangling record's `cycle_id` (the same "still open" guard as the wrapper and the halt rows). When the cycle is already closed (after Branch C, or a 3b / 4c closure whose key stayed unfinalized), the resume still settles the push by the three-way check and re-drives it as recorded, but appends no second `sync_concluded`, so `sync_outcome` keeps its first value | Exit 0: `sync_concluded{pushed, merge_sha: target_sha, recovered: true}` after the new `push_completed`. A guard failure or a rejected push: the halt's own rule, `sync_concluded{halted, reason, recovered: true}`. A **`push_failed`** re-drive: no `sync_concluded` now. The re-drive's `push_initiated` reuses a key that the Branch B record already finalized, so the next `--resume` cannot settle it by the remote check. It reaches row 4b', which halts `resume_unrepresentable` and closes the cycle once. A crash anywhere during the re-drive reaches row 4b' the same way. `--resume` never retries a re-drive |
| C (ambiguous) | `recovery.resolve_crash_window_plan` | `sync_concluded{halted, reason: ambiguous_remote_tip, recovered: true}`, appended **after** the `terminal_halted{ambiguous_remote_tip}` that the unchanged `resolve_crash_window` writes (`recovery.py:161-170`). This is the one exception to "`sync_concluded` before `terminal_halted`". It is safe because both are appended in the same wrapper call before any other action, and `rebuild_state` folds each event independently of their relative order. The Branch C test pins this order |
| any `halt` directive from `crash_resume_plan` (`resume_unrepresentable`) | `recovery.resolve_crash_window_plan` | `sync_concluded{halted, reason: resume_unrepresentable, recovered: true}` |

Kinds `fix`, `ci` and absent have no conflict cycle and append nothing new (byte-equal to today for `fix` / absent). The wrapper finds the cycle by the dangling record's `cycle_id` and appends only when `is_conflict_cycle(cycle_id)` and that cycle is open in `rebuild_state()`; it never appends twice. After any of these, a later `--resume` in the same run sees no open cycle (or a fresh one), so a later fix-push crash window reaches `detect_crash_window` through row 2 and the existing recovery. A conflict cycle whose Branch B re-drive did not complete never routes through `detect_crash_window` again: row 4b requires a matching dangling record, and row 4b' fails closed otherwise. That keeps conflict cycles out of the pre-existing finalized-key gap (section 14 V8), which still affects fix pushes.

## 5. Core module `superclaude.pr_submit.conflicts`

### 5.1 Module rules

- File: `src/superclaude/pr_submit/conflicts.py`. Standard library only: `base64`, `re`, `dataclasses`, `typing`. Internal imports: `from .models import MonitorState` and `from .fsm import run_validation_gates`. `fsm.py`, `models.py`, `run_log.py` and `ci.py` never import `conflicts` (no import cycle); `recovery.py` does, so `conflicts.py` never imports `recovery` (it defines its own branch literals, section 5.2).
- No I/O, no clock, no environment reads, no `anthropic` import (T-N41), and no `git` / `gh` token anywhere, docstrings and comments included (T-N50). Write "version control", "the probe", "the merge" instead. The word "merge", `MERGE_HEAD`, `.github/` paths and `uv` are fine (the T-N50 regex is `\bgh\b|\bgit\b`).
- Every public function fails closed: malformed input raises `ValueError` where the contract says so, and otherwise returns the most restrictive answer (`False`, Tier 3, the default `halt` row, `"failed"`, a problem list, a `halt` resume directive). No function returns an action on input it cannot interpret.
- Expected size: about 450 lines; one test file (`tests/pr_submit/test_conflicts_core.py`).

### 5.2 Constants and data types

```python
SYNC_CAP: int = 1                 # conflict cycles per run, both tiers together (INV-019)
TIER2_MAX_FILES: int = 8          # text:* paths; regen:* paths do not count (OQ-9)
MAX_PROBE_BYTES: int = 102_400    # the probe truncates above this; a truncated probe is Tier 3
CONFLICT_CYCLE_PREFIXES: tuple[str, ...] = ("sync-", "conflict-")
HOOKS: tuple[str, ...] = ("wave0", "c_initial", "wave8a")
ENTERING_OUTCOMES: tuple[str, ...] = ("clean", "report_only", "halt_max_rounds", "no_response")
PRESERVED_OUTCOMES: tuple[str, ...] = ("halt_max_rounds", "no_response")
ACTIONS: tuple[str, ...] = ("none", "report", "propose", "resolve_local", "resolve_push", "halt")
PUSH_KINDS: tuple[str, ...] = ("fix", "merge", "sync", "ci")
FOREIGN_OPS: tuple[str, ...] = ("MERGE_HEAD", "rebase-merge", "rebase-apply",
                                "CHERRY_PICK_HEAD", "REVERT_HEAD", "sequencer")
CONFLICT_PROPOSE_PROMPT: str = "resolve these conflicts? y/n"
PROTECTED_PREFIXES: tuple[str, ...] = (".github/workflows/", ".github/actions/")
PROTECTED_PATHS: tuple[str, ...] = (".claude/settings.json", ".claude/settings.local.json")
MIGRATION_SEGMENTS: tuple[tuple[str, ...], ...] = (("migrations",), ("alembic", "versions"), ("db", "migrate"))
LOCKFILE_NAMES: tuple[str, ...] = ("package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Cargo.lock",
                                   "poetry.lock", "Pipfile.lock", "flake.lock", "uv.lock")
GENERATED_SEGMENTS: tuple[str, ...] = ("generated", "dist", "build", "__snapshots__")
RECORD_KINDS: tuple[str, ...] = ("trivial", "additive", "competing", "structural",
                                 "modify-delete", "add-add", "semantic")
RECORD_RESOLUTIONS: tuple[str, ...] = ("keep_both", "take_ours", "take_theirs", "synthesized")
RECORD_FIELDS: tuple[str, ...] = ("kind", "root_cause", "ours_intent", "theirs_intent",
                                  "resolution", "behavior_after", "dropped", "evidence")
REPORT_REASONS: frozenset[str]    # every reason conflict_action can return, in any row (section 4.4)
HALT_REASONS: frozenset[str]      # every reason ever written to terminal_halted (section 9)
# The two sets overlap by design: a reason is reported at one hook or ordinal and halts at
# another. The intersection is exactly {"tier_above_cap", "conflict_tier3", "probe_failed",
# "merge_tree_unsupported", "github_disagrees", "sync_cap", "late_conflict", "router_unreachable"},
# pinned by a test so a new reason must be placed deliberately.
BRANCH_LANDED: str = "landed"            # equal to recovery.BRANCH_A_LANDED (pinned by a test)
BRANCH_NOT_LANDED: str = "not_landed"    # equal to recovery.BRANCH_B_NOT_LANDED
BRANCH_AMBIGUOUS: str = "ambiguous"      # equal to recovery.BRANCH_C_AMBIGUOUS

@dataclass(frozen=True)
class MechanicalRule:              # adding a rule = one row here + one parametrized test row
    pattern: str                   # exact repository-root-relative path, never a bare basename
    kind: str                      # "lockfile" | "generated"
    sources: tuple[str, ...]       # paths the output is derived from (documentation and report)
    regenerate: tuple[str, ...]    # argv; argv[0] must be in SKILL.md allowed-tools
    check: tuple[str, ...] = ()    # argv; argv[0] must be in SKILL.md allowed-tools

MECHANICAL_RULES: tuple[MechanicalRule, ...] = (
    MechanicalRule("uv.lock", "lockfile", ("pyproject.toml",), ("uv", "lock"), ("uv", "lock", "--check")),
)

@dataclass(frozen=True)
class StageRecord:
    mode: str                      # 6 octal digits
    oid: str                       # 40 hex
    stage: int                     # 1, 2 or 3
    path: str

@dataclass(frozen=True)
class MergeTreeListing:
    tree_oid: str                  # 40 hex: the written merge tree
    records: tuple[StageRecord, ...]

@dataclass(frozen=True)
class ProbeResult:
    merge_tree_supported: bool
    base_ref: str
    base_sha: str
    head_sha: str
    merge_base: str
    behind: int
    ahead: int
    foreign_op: str | None
    tree_clean: bool
    status_porcelain: str          # decoded status_b64
    clean: bool | None             # None when merge_tree_supported is False
    listing: MergeTreeListing | None
    binary_paths: frozenset[str]
    programs: frozenset[str]

@dataclass(frozen=True)
class ConflictEntry:
    path: str
    stages: str                    # "123", "12", "13", "23", ...
    modes: dict[str, str | None]   # keys "base", "ours", "theirs"
    oids: dict[str, str | None]
    binary: bool

@dataclass(frozen=True)
class PathClass:
    path: str
    stages: str
    cls: str                       # "halt:<x>" | "regen:<pattern>" | "text:<x>"
    reason: str

@dataclass(frozen=True)
class ConflictPlan:
    tier: int | None               # 0..3, or None when unclassified
    reason: str                    # plan reason (section 4.3)
    hint: str                      # mergeability_hint value
    github_conflicting: bool       # hint == "conflicting"
    paths: tuple[PathClass, ...]
    text_paths: tuple[str, ...]
    regen_paths: tuple[str, ...]
    base_sha: str | None
    head_sha: str | None
    merge_tree_oid: str | None
    behind: int | None
    listing: MergeTreeListing | None

@dataclass(frozen=True)
class ConflictAction:
    action: str                    # one of ACTIONS
    reason: str
    status: str | None = None      # None = continue; else "terminal_halted" | "proposed" | "halt_before_push"
    skip_ci: bool = False
    fsm_event: str | None = None   # "conflicting" on the c_initial resolve_push row
    push_kind: str | None = None   # "sync" | "merge" on resolve rows

@dataclass(frozen=True)
class SyncDecision:
    predicate_1_ordinal: bool
    predicate_2_validated: bool
    predicate_3_tier_allowed: bool
    predicate_4_under_cap: bool
    authorized: bool
    kind: str                      # "sync" | "merge"

    @property
    def audit_predicates(self) -> dict[str, bool]:
        return {"p1_ordinal": ..., "p2_validated": ..., "p3_tier_allowed": ..., "p4_under_cap": ...}

@dataclass(frozen=True)
class ResumePlan:
    directive: str                 # "none" | "fsm" | "wave8_ci_wait" | "redrive_then_wave8"
                                   # | "abort_and_restart" | "restart" | "complete_after_push"
                                   # | "crash_window" | "halt"
    state: MonitorState | None = None
    reason: str | None = None
    cycle_id: str | None = None
    kind: str | None = None
    wait_sha: str | None = None
    target_sha: str | None = None  # the open cycle's recorded push target (row 4b' message; N1 tests)
    base_sha: str | None = None
    review_terminal: str | None = None
    hook: str | None = None        # restart rows: the open cycle's hook ("wave8a" | "c_initial")
    expect_checks: bool | None = None
    rerun_guard: bool = False
    check_merge_parent: bool = False
```

### 5.3 Functions

| Signature | Contract (inputs, output, fail-closed behaviour) |
|---|---|
| `mergeability_hint(mergeable: object, merge_state: object) -> str` | Case-insensitive. `"conflicting"` when `mergeable == CONFLICTING` or `merge_state == DIRTY`; `"unknown"` when `mergeable` is `UNKNOWN`, `None`, not a string, or any other value; `"behind"` when `MERGEABLE` and `merge_state == BEHIND`; `"blocked"` when `MERGEABLE` and `BLOCKED`; `"clean"` for `MERGEABLE` with any other state. Never raises. (`"blocked"` is a fifth value beyond the spec's four so the `BLOCKED` row reports its own reason.) |
| `needs_probe(hint: str) -> bool` | True only for `"conflicting"` and `"unknown"`. |
| `parse_stage_records(raw: str) -> MergeTreeListing` | `raw` is the decoded `merge-tree --write-tree -z` output. First NUL field is the tree OID (40 hex). Then records `<mode> <oid> <stage>\t<path>` until the first empty field; everything after it (informational messages) is ignored. Raises `ValueError` on: bad tree OID, a mode that is not 6 octal digits, an OID that is not 40 hex, a stage outside 1..3, an empty path, a duplicate `(path, stage)`, a missing tab. An output with only the tree OID gives an empty `records`. |
| `parse_numstat_binary(raw: str) -> frozenset[str]` | `raw` is decoded `diff --numstat -z --no-renames` output: records `<added>\t<deleted>\t<path>`. A record whose `added` and `deleted` are both `-` is binary. Raises `ValueError` on a record without two tabs or with non-numeric, non-`-` counts. |
| `parse_probe(payload: object) -> ProbeResult` | Validates the full-mode probe JSON of section 7.1: `ok is True`, `mode == "full"`, 40-hex `base_sha` / `head_sha` / `merge_base`, non-negative int `behind` / `ahead`, `foreign_op` null or in `FOREIGN_OPS`, bool `tree_clean`, `truncated is False`, strict base64 for every `*_b64` field (`base64.b64decode(..., validate=True)` then UTF-8 decode, no replacement), `programs` a list of strings. When `merge_tree_supported` is false, `clean` must be null and the listing fields null. Raises `ValueError` on anything else. |
| `group_entries(listing: MergeTreeListing, binary_paths: frozenset[str]) -> tuple[ConflictEntry, ...]` | One entry per path in first-seen order; `stages` sorted; `modes` / `oids` keyed `base` (1), `ours` (2), `theirs` (3), `None` when the stage is absent. |
| `classify_path(entry: ConflictEntry, *, programs: frozenset[str], rules: tuple[MechanicalRule, ...] = MECHANICAL_RULES) -> PathClass` | The 14-row first-match table of section 4.3. A non-`ConflictEntry`, a non-string path or an unexpected `stages` value gives `halt:unknown_shape`. |
| `conflict_plan(*, hint: str, probe: object \| None, probe_failed: bool = False, rules: tuple[MechanicalRule, ...] = MECHANICAL_RULES, tier2_max_files: int = TIER2_MAX_FILES) -> ConflictPlan` | The plan-tier table of section 4.3. `probe is None and not probe_failed` with a hint that `needs_probe` is a caller error and gives tier 3, reason `probe_malformed`. `parse_probe` or `parse_stage_records` raising gives tier 3, reason `probe_malformed`. Never raises. Does not take the cap: every cap decision is the router's (section 10.5 D-3). |
| `conflict_action(*, hook: str, plan_tier: int \| None, ordinal: int, entering: str \| None, conflict_max_tier: int, round_counter: int, max_rounds: int, prior_conflict_cycles: int, github_conflicting: bool, plan_reason: str = "") -> ConflictAction` | Section 4.4, including the domain guard (default row `halt` / `router_unreachable`) and the L0 row. `prior_conflict_cycles` is the number of distinct ids in `rebuild_state()["conflict_cycles"]` other than the current `cycle_id`: `len(conflict_cycles)` for a fresh cycle, one less for a resume restart (section 4.8). Never raises. |
| `merge_preflight_ok(porcelain: object) -> tuple[bool, list[str]]` | `porcelain` is decoded `status --porcelain=v1 --untracked-files=no -z` output. `(True, [])` only for the empty string. Otherwise `(False, paths)` with every path named (both paths of a rename record). A `??` record (untracked, which the flag should exclude) is ignored. A non-string, or a record it cannot parse, gives `(False, ["<unparsable status>"])`. |
| `merge_parent_ok(target_parents: list[str] \| None, pre_push_sha: str \| None, base_sha: str \| None) -> bool` | True iff `target_parents` is a list of exactly 2 strings, all four ids are 40-hex in full (no whitespace, no short ids), `parents[0] == pre_push_sha`, `parents[1] == base_sha` (case-insensitive), and `pre_push_sha != base_sha`. Everything else, including swapped order, 0/1/3 parents, `None`, wrong types: false. Disjoint from `fsm.push_parent_ok` by parent count. |
| `evaluate_sync_decision(*, monitor_ordinal: int, validation_status: str, tier: int, conflict_max_tier: int, halt_reason: str \| None, prior_conflict_cycles: int, round_counter: int, max_rounds: int) -> SyncDecision` | `p1 = monitor_ordinal >= 3`; `p2 = validation_status == "validated"`; `p3 = tier in (1, 2) and tier <= conflict_max_tier and halt_reason is None`; `p4 = prior_conflict_cycles < SYNC_CAP` and, for tier 2, also `round_counter < max_rounds`. `prior_conflict_cycles` counts earlier conflict cycles, excluding the current `cycle_id`. `authorized = p1 and p2 and p3 and p4`; `kind = "sync"` for tier 1, `"merge"` for tier 2, `"sync"` with `p3 = False` for any other tier. Non-int inputs make the affected predicate false. No `applied_edits` predicate exists. |
| `sync_fail_state(decision: SyncDecision) -> MonitorState` | `p3` false: `HALT_HUMAN`; else `p4` false: `REPORT_ONLY` (the SKILL reports reason `sync_cap`); else `p1` or `p2` false: `REPORT_ONLY`. Called only for a blocked decision; an authorized one also returns `REPORT_ONLY` (never a push state). |
| `conflict_validation_status(tier: int, results: dict[str, bool]) -> str` | `run_validation_gates(results)`, and for tier 2 additionally `"failed"` unless `results.get("VG-2") is True`. Any tier other than 1 or 2: `"failed"`. |
| `conflict_cycle_id(tier: int, n: int) -> str` | `"sync-<n>"` for tier 1, `"conflict-<n>"` for tier 2, `n >= 1`; `ValueError` otherwise. |
| `is_conflict_cycle(cycle_id: object) -> bool` | True only for a string starting with a reserved prefix. |
| `prior_conflict_cycles(conflict_cycles: object, cycle_id: object) -> int` | Number of distinct string ids in `conflict_cycles` other than `cycle_id`; the only way callers compute the `prior_conflict_cycles` argument of `conflict_action` and `evaluate_sync_decision` (section 4.8). A non-list input returns `SYNC_CAP` (fail closed: the cap is treated as reached). |
| `finish_manifest(listing: MergeTreeListing, resolved_paths: list[str]) -> str` | One line per resolved path, `<stage-1 oid or ->\t<path>\n`, in listing order. `ValueError` when a resolved path is not in the listing, appears twice, or contains a control character. |
| `parse_resolution_record(text: str) -> dict[str, dict[str, str]]` | Parses the `resolution.md` format of section 8.3: `## <path>` headings, then `<field>: <value>` lines. `ValueError` on a duplicate heading, a duplicate field, an unknown field, or a field line before the first heading. |
| `resolution_record_ok(record: dict[str, dict[str, str]], text_paths: tuple[str, ...]) -> list[str]` | Problems, empty when valid: every `text:*` path has an entry and no extra entry exists; every `RECORD_FIELDS` field present and non-empty; `ours_intent`, `theirs_intent`, `behavior_after` each one sentence (no newline, exactly one terminal `.`, `!` or `?`, at the end); `kind` in `RECORD_KINDS` and not `semantic` (semantic means Tier 3); `resolution` is one of `RECORD_RESOLUTIONS` (`keep_both` may carry `(<order>)`); `dropped` is `none` or a non-empty explanation. Non-dict input gives `["record is not a mapping"]`. |
| `merge_commit_message(*, base_ref: str, head_branch: str, tier: int, rule_patterns: tuple[str, ...] = (), record: dict[str, dict[str, str]] \| None = None, lock_changes: str = "") -> str` | Subject `Merge <base_ref> into <head_branch> (sc:pr-submit sync, tier <t>)`. Body: Tier 1, one line per rule path, "uv.lock regenerated from the merged pyproject.toml" and `lock_changes` (a summary of changed package versions the SKILL computes from `git diff --stat` of the lock); Tier 2, one line per path with `kind`, `resolution`, `dropped`. Intents and labels only, never file content (NFR-7). The SKILL appends the session's attribution lines. `ValueError` on tier not 1 or 2, or tier 2 without a record. |
| `crash_resume_plan(dangling: dict, branch: str, fsm_state: MonitorState) -> ResumePlan` | Section 4.8 table 2. `branch` is compared by string against `BRANCH_LANDED` / `BRANCH_NOT_LANDED` / `BRANCH_AMBIGUOUS` (the values `recovery.py:28-30` returns; no import of `recovery`); an unknown branch or kind gives `halt` / `resume_unrepresentable`. Pure: it appends nothing (the wrapper of section 6.4 appends `sync_concluded`). |
| `conflict_resume_plan(state: dict, *, foreign_op: str \| None, merge_head_sha: str \| None, local_head_sha: str \| None, local_head_parents: list[str] \| None, dangling: dict \| None) -> ResumePlan` | Section 4.8 table 1 in table order, including rows 1 (closes an open cycle), 3b, 4c (invalid `hook` or `review_terminal`), 4b (only when `dangling["cycle_id"]` is the open cycle's) and 4b' (a dangling push no crash record matches: `halt`, `resume_unrepresentable`, `target_sha` in the plan); every halt plan that finds an open cycle carries its `cycle_id` so the SKILL closes it once; row 4 returns `expect_checks` from the open cycle (`True` when missing); restart rows return `cycle_id`, `hook` and `review_terminal` from the open cycle. A `state` without the keys of section 6.3 gives `halt` / `resume_unrepresentable`. Pure: the `sync_concluded` events the rows name are appended by the SKILL. |

## 6. Changes to existing core modules

### 6.1 `fsm.py`

Not edited: `evaluate_push_decision`, `push_fail_state` (`:173-219`), `push_idempotency_key` (`:227-235`), `push_parent_ok` (`:582-600`), `needs_rebase` (`:603-610`, OQ-14), every existing `transition()` edge. All new text is T-N50 clean.

1. **Constant** after `fsm.py:36`: `DEFAULT_CONFLICT_MAX_TIER = 1`.
2. **`SkillArgs`** (`:50-70`): append the last field `conflict_max_tier: int = DEFAULT_CONFLICT_MAX_TIER` after `pr` (appending keeps positional construction compatible).
3. **`build_arg_parser`** (`:73-99`), before `return parser`:
   ```python
   parser.add_argument(
       "--conflict-max-tier",
       dest="conflict_max_tier",
       type=int,
       choices=[0, 1, 2],
       default=DEFAULT_CONFLICT_MAX_TIER,
   )
   ```
   argparse rejects `3` (and any non-int) with `SystemExit`, the same mechanism as `--monitor` (`:76-78`).
4. **`parse_args`** (`:121-134`): pass `conflict_max_tier=ns.conflict_max_tier` to `SkillArgs(...)`.
5. **New pure helper** after `push_fail_state` (`:219`):
   ```python
   def should_retrigger(applied_edits: int, push_kind: str | None = None) -> bool:
       """S5a re-trigger rule: a cycle that applied grounded edits, or a Tier 2
       merge cycle (push kind "merge"), which applies no finding edit but publishes
       authored code that the reviewers must see (issue #305, P2)."""
       return (isinstance(applied_edits, int) and applied_edits > 0) or push_kind == "merge"
   ```
6. **`build_push_triad`** (`:238-288`) gains four keyword-only arguments, all defaulting to `None`; with all four `None` the output is byte-identical to today (pinned by a recorded fixture, section 12.1):
   ```python
   def build_push_triad(*, run_id, cycle_id, round_counter, pre_push_sha, target_sha,
                        target_branch, target_remote, decision,
                        push_kind: str | None = None,
                        base_sha: str | None = None,
                        review_terminal: str | None = None,
                        expect_checks: bool | None = None) -> list[dict]:
   ```
   - `push_kind` not `None` and not in `("fix", "merge", "sync", "ci")`: `ValueError`.
   - `common` (`:259-267`) gets `"kind": push_kind` and `"base_sha": base_sha` appended after `target_remote`, each only when not `None`.
   - `push_initiated` gets `"review_terminal"` and `"expect_checks"` (each only when not `None`), after `remote_ref`; `push_completed` gets `"expect_checks"` the same way.
   - `predicates`: when `decision` is a `PushDecision`, the existing five-key dict (`:273-279`) unchanged; otherwise `dict(decision.audit_predicates)` (a `conflicts.SyncDecision`; duck-typed through the attribute so `fsm.py` does not import `conflicts`). An object with neither shape raises `AttributeError` (a programming error, never a silent push record).
7. **The one P2 edge** in `transition()`, right after the `(S2_CLASSIFY, "findings")` block (`:741-748`):
   ```python
   if edge == (MonitorState.S2_CLASSIFY, "conflicting"):
       # Issue #305 (P2): a Tier 2 merge cycle at C-initial. Same round gate as
       # findings; then the G-edit ceiling (S3_FIXING at L2+, else PROPOSED).
       if should_halt_rounds(
           int(ctx.get("round_counter", 0)),
           int(ctx.get("max_rounds", DEFAULT_MAX_ROUNDS)),
       ):
           return MonitorState.HALT_MAX_ROUNDS
       return MonitorState.S3_FIXING if gate_edit(ordinal) else MonitorState.PROPOSED
   ```
   The `needs_human_decision` pre-gate (`:729-731`) still applies first. The router only emits this event at L3, so `PROPOSED` is reachable only through a direct call; it keeps the edge honest to the ceiling.
8. **The widened S5a clause** at `fsm.py:1137`: `if result.applied_edits > 0:` becomes `if should_retrigger(result.applied_edits):`. `run_skill` drives fix cycles only, so its behaviour is unchanged; the widening is exercised through `should_retrigger` and the SKILL text.

### 6.2 `ci.py`

1. `classify_checks(payload: dict, *, wait_sha: str | None = None, expect_checks: bool = False) -> str`. With `expect_checks` false the body is unchanged (pins at `tests/pr_submit/test_ci_classify.py:36-42` stay green). With `expect_checks` true: a non-dict payload returns `polling` (instead of `clean`), and an empty or missing chosen check list returns `polling` (head mismatch already returns `polling` at `:31-32`). A nonempty list classifies exactly as today.
2. New pure setter:
   ```python
   def expect_checks_after_push(*, checks_seen_this_run: bool,
                                pre_push_evidence: int | None,
                                base_evidence: int | None) -> bool:
       """True when the push's CI wait must see at least one check before clean.
       Evidence values are check counts from the commit-scoped evidence read;
       -1 (failed or unparsable read) and None count as "had checks" (fail closed)."""
   ```
   Returns `checks_seen_this_run is True or pre_push_evidence != 0 or base_evidence != 0`, where a non-int evidence value counts as non-zero. Only all three reading zero gives `False`.
3. Module docstring: add one sentence on `expect_checks`; no shell or version-control token.

### 6.3 `run_log.py`

`IDEMPOTENCY_SETS` (`:27-35`) is unchanged (still 7). `append` docstring `:111`: "41" becomes "43". `rebuild_state` (`:161-260`):

1. New state keys (initialized in the dict at `:175-189`): `"sync_push_count": 0`, `"conflict_cycles": []`, `"open_conflict_cycle": None`, `"push_rejected": False`.
2. New fold branches in the `elif` chain:
   - `sync_started`: append `cycle_id` to `conflict_cycles` if unseen; set `open[cycle_id] = {**ev, "push_initiated": False, "push_completed": False, "target_sha": None, "expect_checks": None, "superseded": False}` (the copied payload includes `hook` and `review_terminal`; a resume restart re-opens the same id).
   - `sync_concluded`: `open.pop(cycle_id, None)`.
   - `push_initiated`: when `ev["cycle_id"]` is open, set its `push_initiated` true, its `target_sha`, and its `expect_checks` (copied from the record; a missing or non-bool value is stored as `True`, fail closed, so `conflict_resume_plan` row 4 never passes `None` or a defaulted `False` to `classify_checks`); for every other open cycle, set `superseded` true (a later push of a different cycle means that cycle was never closed; `conflict_resume_plan` row 3b halts on it).
3. The `push_completed` branch (`:238-241`) becomes kind-aware: `kind = ev.get("kind") or "fix"`; `kind == "sync"` increments `sync_push_count`, every other kind increments `push_count`; `pushed_commit_shas` still records `target_sha`; when `cycle_id` is open, set its `push_completed` true.
4. `push_aborted_or_not_landed` with `rejected is True`: `push_rejected = True` (a new `elif`; the existing chain has no branch for this event).
5. After the loop: `state["open_conflict_cycle"]` is the open entry whose `sync_started` came last, or `None`; `state["conflict_cycles"]` keeps first-seen order (not sorted).
6. Docstring: document the four keys and that a log without `kind` or conflict events rebuilds exactly as before (NFR-12).

### 6.4 `recovery.py`

1. The key tuple (`:98-110`) gains `"kind"` and `"base_sha"` (still copied only `if k in dangling`, so a legacy record yields byte-equal recovery events).
2. New wrapper, after `resolve_crash_window`:
   ```python
   def resolve_crash_window_plan(run_log: RunLog, dangling: dict, *, remote_reachable: bool | None,
                                 observed_remote_sha: str | None = None) -> ResumePlan:
       """Kind-aware resume: run the unchanged three-way resolution, then map its
       result through conflicts.crash_resume_plan (fix/merge/absent keep today's
       state; sync/ci re-enter the Wave 8 CI wait, never S4/S5a/S5)."""
       branch, state = resolve_crash_window(run_log, dangling, remote_reachable=remote_reachable,
                                            observed_remote_sha=observed_remote_sha)
       plan = crash_resume_plan(dangling, branch, state)
       cycle_id = dangling.get("cycle_id")
       open_cycle = run_log.rebuild_state()["open_conflict_cycle"]
       if (is_conflict_cycle(cycle_id) and open_cycle is not None
               and open_cycle.get("cycle_id") == cycle_id):
           if plan.directive == "halt":
               outcome, reason, merge_sha = "halted", plan.reason, None
           elif branch == BRANCH_A_LANDED:
               outcome, reason, merge_sha = "pushed", None, dangling.get("target_sha")
           else:
               outcome = None          # Branch B: the SKILL closes the cycle after the re-drive
           if outcome is not None:
               run_log.append({"event_type": "sync_concluded", "cycle_id": cycle_id,
                               "outcome": outcome, "merge_sha": merge_sha, "record_path": None,
                               "dropped": [], "reason": reason, "recovered": True})
       return plan
   ```
   Branch C maps to `plan.directive == "halt"` (reason `ambiguous_remote_tip`), so it closes the cycle as `halted`. The append happens once: the open-cycle check makes a second call a no-op.
   `resolve_crash_window` keeps its signature and return value; its callers in tests (`test_crash_recovery.py:263`, `:310`, `:344`, `test_codex_reviews.py:489`, `test_augment_review_remediation.py:145`) are untouched. The SKILL's resume text calls the wrapper.
3. Module docstring: one paragraph on push kinds; still no version-control token.

### 6.5 `models.py` and every event-count pin site

`EventType` gains, after `REVIEWER_INCOMPLETE` (`models.py:90`):

```python
    # --- merge-conflict cycles (issue #305), both tiers - the 42nd-43rd ---
    SYNC_STARTED = "sync_started"
    SYNC_CONCLUDED = "sync_concluded"
```

No other model changes (`SyncDecision` lives in `conflicts.py`; `MonitorState`, `TERMINAL_STATES`, `PushDecision`, `SkillResult` unchanged). Every site that states the count, all edited in the same commit:

| Site | Edit |
|---|---|
| `src/superclaude/pr_submit/models.py:3-7` | "exactly 41 members" becomes "exactly 43 members"; add "plus the two conflict-cycle events `sync_started` and `sync_concluded`" |
| `models.py:23-33` | "EXACTLY 41 members" becomes "EXACTLY 43 members"; same addition |
| `src/superclaude/pr_submit/run_log.py:111` | "one of the 41 closed" becomes "one of the 43 closed" |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/loop-guard.md:86-99` | heading "The 41 event types" becomes "The 43 event types (... + conflict cycles)"; "EXACTLY 41 members" becomes 43; append `sync_started`, `sync_concluded` to the list |
| `tests/pr_submit/test_run_log.py:165-169` | see section 12.2 |
| `tests/pr_submit/test_codex_reviews.py:441` | `== 41` becomes `== 43` |
| PR checklist step | `grep -rn '\b41\b' src/superclaude/pr_submit tests/pr_submit src/superclaude/skills/sc-pr-submit-protocol` shows no event-count hit (QA-6); `test_run_log.py:204` (`RunLog(41, ...)`, a PR number) is not a count |

### 6.6 `__init__.py`

Add to the module docstring (`:1-19`) one clause naming `conflicts`. Add imports and an `__all__` group `# merge conflicts (issue #305)`:

```python
from .conflicts import (
    MECHANICAL_RULES, SYNC_CAP, TIER2_MAX_FILES, ConflictAction, ConflictPlan,
    MechanicalRule, ResumePlan, SyncDecision, conflict_action, conflict_cycle_id,
    conflict_plan, conflict_resume_plan, conflict_validation_status, crash_resume_plan,
    evaluate_sync_decision, finish_manifest, is_conflict_cycle, merge_commit_message,
    merge_parent_ok, merge_preflight_ok, mergeability_hint, needs_probe, prior_conflict_cycles,
    parse_resolution_record, resolution_record_ok, sync_fail_state,
)
from .fsm import should_retrigger   # added to the existing fsm import line
```

The import order keeps `fsm` before `conflicts` resolution-wise (conflicts imports fsm; fsm never imports conflicts).

## 7. Scripts

Rules for every new script (NFR-10, NFR-6, C7): `#!/usr/bin/env bash`, `set -u -o pipefail` (no blanket `-e`; each step checks its own exit), mode `100755` in git, no stdin read, no prompt, exactly one stdout line (a JSON object on success, a `<SCRIPT>_FAIL <reason>` token on failure) with details on stderr, exit `0` on success and `2` on failure. Each git command that can block (fetch) runs under `timeout 60` when `timeout` exists on PATH. Temporary files go only under `$(git rev-parse --git-path sc-pr-submit-tmp)` and are removed by an EXIT trap; nothing is written outside the repository's git directory and the given output directory. No script contains a `git push` line, a stash, a stored config write, a hook-skipping flag, an amend, or a `src/superclaude/` path. The header comment names the script, its purpose, usage, output and exit contract, like `poll-ci-checks.sh:1-12`.

### 7.1 `scripts/probe-merge.sh` (new)

Read-only probe. It never changes the index, the worktree, `HEAD` or any branch; it may write unreachable tree objects (documented, harmless) and it updates `refs/remotes/origin/<base>` through the fetch.

```text
probe-merge.sh --repo <owner/repo> --ops-only
probe-merge.sh --repo <owner/repo> --base <branch> [--program <name>]...
```

Steps, full mode:

1. Parse arguments; `--repo` missing: `PROBE_FAIL usage`.
2. `git rev-parse --is-inside-work-tree` must print `true`: else `PROBE_FAIL not_a_worktree`.
3. Resolve `owner/repo` from `git remote get-url origin` with the same `sed` expression as `SKILL.md:267` and `poll-ci-checks.sh:34`; it must equal `--repo`: else `PROBE_FAIL origin_mismatch` (the fetch can only ever reach the fork).
4. `foreign_op`: the first of `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `sequencer` whose `git rev-parse --git-path <name>` exists (worktree-aware, J-16). `merge_head`: `git rev-parse -q --verify MERGE_HEAD` or null. In `--ops-only` mode the script stops here and prints `{"ok": true, "mode": "ops", "foreign_op": <name or null>, "merge_head": <sha or null>}`.
5. `git check-ref-format --branch <base>` must succeed: else `PROBE_FAIL bad_base`.
6. `status`: `git status --porcelain=v1 --untracked-files=no -z` written to a temp file; `tree_clean` is true when it is empty; `status_b64` is its base64.
7. `timeout 60 git fetch --no-tags origin <base>`; failure: `PROBE_FAIL fetch_failed` (stderr says "cannot reach remote origin", J-77). `base_sha := git rev-parse --verify 'refs/remotes/origin/<base>^{commit}'`, missing: `PROBE_FAIL fetch_failed`.
8. `head_sha := git rev-parse --verify 'HEAD^{commit}'`; `merge_base := git merge-base HEAD <base_sha>`, none: `PROBE_FAIL no_merge_base`; `git rev-list --left-right --count <base_sha>...HEAD` gives `behind` and `ahead`.
9. Capability: `git merge-tree --write-tree HEAD HEAD` exit 0 sets `merge_tree_supported` (never a version parse, NFR-11). When false: print the JSON with `merge_tree_supported: false`, `clean: null` and every `*_b64` merge field null, exit 0.
10. `git merge-tree --write-tree -z HEAD <base_sha>` into a temp file. Exit 0: `clean: true`; exit 1: `clean: false`; any other exit: `PROBE_FAIL merge_tree_failed`.
11. When not clean: `git diff --numstat -z --no-renames <merge_base> HEAD` and `... <merge_base> <base_sha>` into temp files (INV-016).
12. Any captured file above `102400` bytes: print the JSON with `truncated: true` and the `*_b64` fields null (the core then classifies Tier 3, `probe_malformed`), exit 0.
13. `programs`: for each `--program <name>`, include it when `command -v <name>` succeeds.
14. Print one line with `jq -nc` (base64 via `base64 | tr -d '\n'`, portable):

```json
{"ok": true, "mode": "full", "merge_tree_supported": true,
 "base_ref": "origin/main", "base_sha": "<40hex>", "head_sha": "<40hex>", "merge_base": "<40hex>",
 "behind": 3, "ahead": 2, "foreign_op": null, "merge_head": null,
 "tree_clean": true, "status_b64": "",
 "clean": false, "merge_tree_b64": "<base64>", "numstat_ours_b64": "<base64>", "numstat_theirs_b64": "<base64>",
 "programs": ["uv"], "truncated": false}
```

Exit: `0` on any completed probe; `2` with `PROBE_FAIL <reason>` for `usage`, `not_a_worktree`, `origin_mismatch`, `bad_base`, `fetch_failed`, `no_merge_base`, `merge_tree_failed`. The SKILL calls it with `--program uv` (the programs of `MECHANICAL_RULES`).

### 7.2 `scripts/finish-merge.sh` (new)

The finish gate: the only new script that changes the repository, and only by one `git commit -F`.

```text
finish-merge.sh --base-sha <40hex> --precheck
finish-merge.sh --base-sha <40hex> --merge-tree-oid <40hex> --manifest <file> --message-file <file>
```

The manifest is the `finish_manifest` text: one `<stage-1 oid or ->\t<path>` line per resolved path. It is written at step 9, so precheck mode neither needs nor accepts `--manifest`, `--merge-tree-oid` or `--message-file` (passing one is `FINISH_FAIL usage`); commit mode requires all three.

`--precheck` (before a regenerate; no commit):

1. `git rev-parse -q --verify MERGE_HEAD` exists, else `FINISH_FAIL no_merge_head`; equals `--base-sha` (case-insensitive), else `FINISH_FAIL foreign_merge`.
2. `git diff --name-only --no-renames -z` (worktree against index) lists only paths that are currently unmerged (`git diff --name-only --diff-filter=U -z`), else `FINISH_FAIL tree_dirty`.
3. Print `{"precheck": "ok"}`.

Commit mode, in order:

1. The two `MERGE_HEAD` checks above.
2. `git diff --name-only --diff-filter=U` empty, else `FINISH_FAIL unmerged`.
3. `git diff --quiet --no-renames` (no unstaged change to a tracked file, so the index equals the validated worktree), else `FINISH_FAIL tree_dirty`.
4. Markers (R-11): for each manifest path still in the index, count lines matching `^(<{7}|\|{7}|={7}|>{7})( |$)` in `git show :<path>`; the count must not exceed the same count in `git cat-file blob <stage-1 oid>` (0 for `-`). Else `FINISH_FAIL markers`. A path resolved by deletion is skipped.
5. Staged set (INV-013, INV-016): let `P` = `git diff --cached --name-only --no-renames -z HEAD` united with `git diff --name-only --no-renames -z HEAD <merge-tree-oid>`. For every path in `P` that is not a manifest path, the index blob (`git rev-parse -q --verify :<path>`) must equal the merge-tree blob (`git rev-parse -q --verify <merge-tree-oid>:<path>`), both absent counting as equal. Else `FINISH_FAIL staged_unexpected`. This proves the commit changes nothing beyond the auto-merge result plus the resolved paths.
6. `git commit -F <message-file>` with hooks on. Non-zero exit: copy git's output to stderr verbatim, `FINISH_FAIL hook_rejected` (the merge stays in progress).
7. `git rev-list --parents -n 1 HEAD` must be exactly `[<new>, <old HEAD>, <base-sha>]`, else `FINISH_FAIL parents_mismatch`.
8. `git status --porcelain=v1 --untracked-files=no -z` empty and `git diff --quiet HEAD`, else `FINISH_FAIL tree_dirty`.
9. Print `{"merge_sha": "<40hex>", "parents": ["<old HEAD>", "<base-sha>"]}`.

Token to halt reason: `no_merge_head` and `foreign_merge` to `sync_foreign_operation`; `unmerged` to `sync_unmerged_left`; `markers` to `sync_marker_left`; `staged_unexpected` to `sync_staged_unexpected`; `hook_rejected` and `usage` to `sync_commit_failed`; `tree_dirty` to `merge_preflight_dirty`; `parents_mismatch` to `sync_range_mismatch`.

### 7.3 `scripts/collect-conflict-evidence.sh` (new)

Decision: a script, not inline calls (section 10.5 D-9). Tier 2 only; never run for Tier 0 or 1.

```text
collect-conflict-evidence.sh --path <p> --out <dir> --base-sha <40hex> --merge-base <40hex> [--max-bytes 204800]
```

1. `MERGE_HEAD` exists and equals `--base-sha`, else `EVIDENCE_FAIL foreign_merge`.
2. `--out` does not exist or is an empty directory; created with `mkdir -p`. Else `EVIDENCE_FAIL out_not_empty`.
3. Writes into `--out`, each file cut at `--max-bytes` with a last line `[sc:pr-submit: truncated at <N> bytes]`:
   - `stage1`, `stage2`, `stage3`: `git show :1:<p>`, `:2:<p>`, `:3:<p>` for each stage that `git ls-files -u -z -- <p>` lists (S-12, S-13, S-14); an absent stage is listed in `missing`.
   - `worktree`: the current file with its conflict markers (zdiff3: three sides, S-17); unreadable: `EVIDENCE_FAIL unreadable` (R-84).
   - `log.txt`: `git log --oneline --left-right --merge -- <p>` (R-112).
   - `diff-ours.txt`: `git diff --no-renames <merge-base> HEAD -- <p>`; `diff-theirs.txt`: `git diff --no-renames <merge-base> <base-sha> -- <p>` (both merge-base diffs, R-112, R-181).
4. Whole run under 60 s (`timeout` per command when available); exceeding it: `EVIDENCE_FAIL timeout`.
5. Print `{"dir": "<out>", "files": ["stage1", ...], "missing": ["stage3"], "truncated": false}`.

The SKILL passes `--out <output-dir>/sync/<cycle_id>/<n>/` (`<n>` = the path's 1-based position in `plan.text_paths`). `EVIDENCE_FAIL` of any kind escalates the cycle to Tier 3 (`sync_tier3`).

### 7.4 `scripts/poll-ci-checks.sh --evidence-sha` (changed)

New mode, additive; the existing poll is unchanged.

```text
poll-ci-checks.sh --evidence-sha <40hex> [--repo <owner/repo>]
```

1. Argument loop (`:22-28`) accepts `--evidence-sha`. In this mode `--pr` is not required.
2. After `gh` / `jq` presence and the existing `REPO` resolution (`:31-36`), and **before** the `gh pr checks --help` probe (`:39-43`, which the evidence read does not need): validate the SHA as 40 hex, else exit 2 `invalid --evidence-sha`.
3. `gh api "repos/${REPO}/commits/${SHA}/check-runs?per_page=1" --jq .total_count` and `gh api "repos/${REPO}/commits/${SHA}/status" --jq .total_count`, each `|| true`. Both parse as non-negative integers: `n = a + b`; otherwise `n = -1` (fail closed: counts as "had checks").
4. Print `{"evidence_sha": "<sha>", "evidence_checks": <n>, "source": "ci"}`, exit 0.

Header comment (`:3-12`) gains the usage and output lines for the new mode. The existing `src/superclaude/` header line (`:14`) is pre-existing; this change adds no new one.

## 8. Skill, ref and command changes

All paths below are under `src/superclaude/skills/sc-pr-submit-protocol/` unless named otherwise. New prose never names a `src/superclaude/` path, never quotes a force flag after "git push", and states prohibitions in words. After editing: `make sync-dev`, `make verify-sync`; stage only `src/` and `tests/` (never the `.claude/` mirrors).

### 8.1 `SKILL.md`

Thirteen edits, net **+15 lines** (the budget of NFR-9; there is no line-count assertion). The python block count stays 1. Each edit is an exact replacement or insertion.

**E1. Required Input table**, insert after the `--resume` row (`:218`), +1 line:

```text
| `--conflict-max-tier {0,1,2}` | No (default 1) | Highest merge-conflict tier the skill may act on: 0 detect and report only, 1 also regenerate a conflicted root `uv.lock` (Tier 1), 2 also resolve text conflicts by stated intent (Tier 2, off by default). Tier 3 never resolves. |
```

**E2. STOP block** (`:220-223`, precursor), replace the four lines with four lines:

```text
**STOP** if `--monitor >= 1` and the PR cannot be confirmed on the resolved target repo (origin's
`owner/repo`, parsed from `git remote get-url origin`): a wrong origin, or a returned URL whose `owner/repo` ≠ the resolved target → HALT,
instruct the operator to close the misrouted PR. Being behind the base branch is not a STOP at L1+:
Wave 0 reports how many commits behind (Tier 0) and the conflict check below classifies any conflict.
```

**E3. Output Contract.** Replace the `push_count` row (`:239`) and insert three rows after it, +3 lines:

```text
| `push_count` | int | Landed fix, CI and Tier 2 merge pushes (`kind` on every push record; Tier 1 sync pushes are counted in `sync_push_count`); `<= max_rounds + 1` with the fallback's single push; 0 below L3. |
| `sync_tier` | int or null | Highest merge-conflict tier seen this run (0 to 3; null when it could not be classified). |
| `sync_outcome` | enum | `none` / `report_only` / `left_in_progress` / `pushed` / `aborted` / `halted`. |
| `sync_push_count` | int | Landed Tier 1 sync pushes (`kind: "sync"`, at most `SYNC_CAP = 1`); never counted in `push_count`. |
```

**E4. Wave table** (inside the `text` fence, `:254-265`), +3 lines: after the `Wave 0` line insert the first, after the `Wave 1` line the second, after the `Wave 8` line the third:

```text
Wave 0c: (L1+) conflict check + report      ← loads refs/conflict-mechanical.md ONLY when the probe runs
C-initial: (L3, Tier 2) merge cycle before the first review poll ← loads refs/conflict-mechanical.md + refs/conflict-intent.md
Wave 8a: (L1+) act on a conflict before the CI wait ← loads refs/conflict-mechanical.md ONLY when the probe runs
```

**E5. Wave 0 bullet** (`:267`, precursor plus the operation check), replace the substring

`and rebase if behind `origin/<base>` (with `--pr <N>`, at any level, do not rebase: the PR head is already published, so report how many commits it is behind instead).`

with

`and rebase if behind `origin/<base>` only at L0 (at L1+ the create path does not rebase and does not halt: the branch is already published when `gh pr create` runs, so report how many commits it is behind, a Tier 0 result; with `--pr <N>`, at any level, do not rebase: the PR head is already published, so report how many commits it is behind instead). At L1+, also before creating or attaching, run `scripts/probe-merge.sh --ops-only --repo "$REPO"`: a non-null `foreign_op` (a merge, rebase, cherry-pick, revert or sequencer operation in progress) → HALT before Wave 1 with status `terminal_halted`, reason `foreign_op_in_progress`, nothing created (on `--resume`, `conflict_resume_plan` in `refs/conflict-mechanical.md` decides first).`

Both pinned fragments survive verbatim: "rebase if behind `origin/<base>`" and "with `--pr <N>`, at any level, do not rebase". The AC-1 sentence later in the same bullet is untouched.

**E6. New bullet** after the head-binding bullet (`:268`), +1 line:

```text
- **Wave 0 conflict check (L1+ only; L0 skips it):** after the head binding, read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus` (re-read an `UNKNOWN` up to 3 times, 10 s apart) and normalise it with `superclaude.pr_submit.conflicts.mergeability_hint`. Only `conflicting` or a persistent `unknown` loads `refs/conflict-mechanical.md` and runs `scripts/probe-merge.sh`; follow that ref to classify, print the plan before any edit, and route with `conflict_action(hook="wave0")` (Tier 3 at L3 halts here: `terminal_halted`, reason `conflict_tier3`, nothing touched). Any other hint is Tier 0: report "<N> commits behind, no conflicts" (or the `BLOCKED` reason) and continue; no ref is loaded.
```

**E7. Wave 1 bullet** (`:269`), append after its last sentence ("`--monitor 0` remains no-monitor."), 0 lines:

` **C-initial (L3, Tier 2, only when Wave 0 planned it under `--conflict-max-tier 2`):** after arming and before the first review poll, load `refs/conflict-intent.md` and run the Tier 2 merge cycle of `refs/conflict-mechanical.md` through `transition(S2_CLASSIFY, "conflicting")`; its S5 wait is the run's first review wait.`

**E8. Wave 6 bullet** (`:274`, P2 S5a widening), replace the substring

`AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`), post`

with

`AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`) or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`), post`

The pins at `test_static_grep.py:689` ("Next, when the cycle applied edits (a zero-edit cycle has no fix commit") and `:750` (state-machine.md) are different sentences and stay unchanged.

**E9. Wave 8 bullet** (`:277`), five substring replacements, 0 lines:

| # | Old substring | New substring |
|---|---|---|
| a | `load `refs/ci-poll.md`. These are` | `load `refs/ci-poll.md`, then run Wave 8a (below) before the CI poll loop. These are` |
| b | `classify_checks(payload, wait_sha=<sha at flip or last push>)` | `classify_checks(payload, wait_sha=<sha at flip or last push>, expect_checks=<the value recorded for that push, else false>)` |
| c | `without fetching logs, editing, or pushing.` | `without fetching logs, editing, or pushing a fix; the single Tier 1 sync push of Wave 8a (`SYNC_CAP = 1`) is the only push a wait-only path allows, and it is not a fix.` |
| d | `so this push too carries only the cycle's one fix commit.` | `so this push too carries only the cycle's one fix commit; its triad passes `push_kind="ci"`, `review_terminal` and `expect_checks=True`.` |
| e | `Only parsed empty required **and** all-checks lists prove there are no Actions.` | `Only parsed empty required **and** all-checks lists, with `expect_checks` false, prove there are no Actions; with `expect_checks` true an empty list is `polling`, and expiry is the CI timeout with reason `ci_not_started`, never clean.` |

The pinned substrings "An L3 CI push runs the Wave 6 pre-push head guard and push triad with `target_branch := HEAD_BRANCH`" and "runs the guard's parent check (`push_parent_ok`)" (`test_static_grep.py:694-698`) are untouched.

**E10. New bullet** after the Wave 8 bullet, +1 line:

```text
- **Wave 8a (L1+, conflict act before the CI wait; same entry outcomes as Wave 8):** read `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus,headRefName,headRefOid,isCrossRepository` (same `UNKNOWN` re-reads). Only `conflicting` or a persistent `unknown` loads `refs/conflict-mechanical.md`, re-probes and acts on `conflict_action(hook="wave8a", entering=<review outcome>)`: at L3 a Tier 1 conflict becomes one sync merge commit pushed fast-forward (no round, no re-trigger, no reply, no resolve; the one push a wait-only path allows), then the CI wait runs on the new head with `expect_checks`; L2 leaves it resolved and validated but uncommitted (`halt_before_push`, only after `clean` / `REPORT_ONLY`); L1 proposes (also only after `clean` / `REPORT_ONLY`). A PR still conflicting with nothing pushed skips the CI wait with reason `pr_conflicting` (GitHub runs no `pull_request` checks on it) and ends with the status `conflict_action` returns. When any hook this run read `conflicting`, re-read `mergeable` before sending `transition(clean)`; `CONFLICTING` → `terminal_halted`, reason `late_conflict` (late re-sync: #361).
```

**E11. Will Do and Will Not Do**, one bullet each, +2 lines:

```text
- Detect merge conflicts at Wave 0 (L1+), report the tier and plan before any edit, and resolve only within `--conflict-max-tier` and the ordinal ceiling, publishing a resolution only as one merge commit of the recorded base tip, pushed fast-forward.
```

```text
- Rebase a published PR head (at L1+ the create path no longer rebases), stash, take one side for a whole tree, commit a merge without `scripts/finish-merge.sh`, or push a merge commit whose parents are not exactly the PR head and the recorded base tip (`merge_parent_ok`).
```

(The existing force-push bullet `:305` stays verbatim; it is pinned at `test_static_grep.py:761`.)

**E12. Error Handling.** Replace the row at `:315` and insert four rows after it, +4 lines:

```text
| Wrong origin / wrong-owner URL | HALT; instruct operator to close the misrouted PR (FM-11). |
| Behind base branch (create path at L1+, or `--pr`) | Tier 0 report ("<N> commits behind"); no rebase, no halt. At L0 the create path still rebases. |
| A merge, rebase, cherry-pick, revert or sequencer operation is in progress (L1+) | `terminal_halted`, reason `foreign_op_in_progress`, before anything is created; finish or abort that operation yourself, then re-run. |
| Merge conflict that needs a human (Tier 3: submodule, symlink, mode change, protected or migration path, binary, lock or generated file without a rule, more than 8 text files, unclassifiable) | L3: `terminal_halted` at the end of Wave 0, reason `conflict_tier3`, nothing touched or pushed; L1/L2: reported and the run continues; HALT message from `refs/conflict-mechanical.md`. |
| A conflict cycle stops (dirty tree, foreign merge, guard, finish gate, VAL, rejected or failed push) | `terminal_halted` with the reason from `refs/conflict-mechanical.md` (`merge_preflight_dirty`, `sync_*`, `push_rejected`, `push_failed`); nothing pushed unless the message says the push landed; never stash, never discard your files. |
```

**E13. Head-binding HALT message** (`:268`, revision 2): the sentence "a branch Wave 0 rebased needs a force-push" can no longer happen (head binding is L1+ only and L1+ no longer rebases), and the force-push scan forbids any force-flag mention, so replace the substring

`(push if you are ahead; a branch Wave 0 rebased needs a force-push, which this skill never does for you; `git pull --ff-only` if you are behind)`

with

`(push if you are ahead; `git pull --ff-only` if you are behind; this skill never rewrites a published branch)`

0 lines; no test pins the old wording (checked with a grep of `tests/`). The new text names no force flag and has no "git push" on the line.

Line budget: E1 1 + E3 3 + E4 3 + E6 1 + E10 1 + E11 2 + E12 4 = 15; E2, E5, E7, E8, E9, E13 change no line count.

### 8.2 `refs/conflict-mechanical.md` (new)

Loaded only when a hook runs the probe (Tier 1 and up); a Tier 0 run never loads it. Code examples use `bash` or `text` fences only (never `python`). Not in the T-N50 set (it holds git commands). Target size about 120 lines. It refers to "the Wave 6 pre-push head guard" by name and states only the delta (NFR-9: no duplicated guard text).

| Section | Normative content |
|---|---|
| **1. When this ref applies** | Loads when Wave 0, `C-initial` or Wave 8a runs the probe. Terms: "ours" = the PR head checked out here, "theirs" = the recorded base tip `base_sha` (S-09). The core decides (`superclaude.pr_submit.conflicts`); this ref sequences. Tier 2 steps also need `refs/conflict-intent.md` (Tier 2 only). |
| **2. Detection** | The GitHub read (fenced: `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus` at Wave 0; with `,headRefName,headRefOid,isCrossRepository` at the acting hooks), `UNKNOWN` re-read up to 3 times 10 s apart, a failed read means null hints and the probe runs (OQ-8). The probe (fenced: `scripts/probe-merge.sh --repo "$REPO" --base <baseRefName> --program uv`); a non-zero exit is a prerequisite failure, reported, never retried as polling; then `conflict_plan(hint=..., probe=<json or None>, probe_failed=<exit 2>)`. Once the probe ran, its result is the truth for action; a `CONFLICTING` hint with a clean probe is reported as `github_disagrees` (K2). |
| **3. The plan report (FR-4, R-51)** | Printed before any edit at every hook that probes: the tier, each conflicted path with its class and reason, the action this ordinal would take (`conflict_action`), and the `CONFLICT_PROPOSE_PROMPT` at L1 Wave 8a only after `clean` / `REPORT_ONLY` (after a preserved terminal the router reports `tier1_l1_preserved` and no prompt is printed). At a later hook, print again only when the tier or the path set changed. L0 prints nothing. |
| **4. Tier 3 HALT message (FR-10, R-210, R-212, J-13)** | Exact template: "HALT (`<reason>`): merging `origin/<base>`@<base_sha> into `<HEAD_BRANCH>` needs a human decision. File <k>/<n>: `<path>` (`<class>`). [This PR's side appears to <one sentence>; the base side appears to <one sentence>.] Nothing was changed and nothing was pushed. To continue: on `<HEAD_BRANCH>`, merge `origin/<base>` yourself, resolve and commit, push, then re-run with `--pr <N>`." The bracketed sentences are omitted when classification stopped before reading content (always at Wave 0). Any halt ends the run; nothing later runs. |
| **5. The merge cycle** | Steps 1 to 13 of section 4.6 of this design, in that order, each with its fenced command line(s) and its failure reason. Step 5 carries the `uv.lock` rule (fenced: `scripts/finish-merge.sh --base-sha <base_sha> --precheck`, `git checkout --ours -- uv.lock`, `uv lock`, `uv lock --check`, `git add -- uv.lock`; seed from the PR side because a lock full of markers is unparseable and a from-scratch resolve could upgrade unrelated pins, OQ-6). Step 5 and step 6 for Tier 2 point to `refs/conflict-intent.md`. Step 9 (fenced: `scripts/finish-merge.sh ... --message-file <file>`) and its token-to-reason map. |
| **6. VAL for a conflict cycle** | Section 4.6 step 7 verbatim: the gate results per tier, `conflict_validation_status`, the single retry rule (R-169), the "no tests ran for the regenerated lock file" line, the red-base hint. The impact advisory of VG-1 is not invoked for conflict cycles. |
| **7. Publish** | The Wave 6 pre-push head guard delta: compare the stored `pre_push_sha`; then `merge_parent_ok(<parents>, pre_push_sha, base_sha)` in place of `push_parent_ok`; then `git fetch origin <base>` and `git merge-base --is-ancestor <base_sha> origin/<base>`. The advisory read (fenced: `gh repo view "$REPO" --json mergeCommitAllowed,rebaseMergeAllowed,squashMergeAllowed`). "The deterministic core DECIDES": `evaluate_sync_decision`, the evidence reads (fenced: `scripts/poll-ci-checks.sh --evidence-sha <pre_push_sha> --repo "$REPO"` and the same for `<base_sha>`), `expect_checks_after_push`, `build_push_triad(..., push_kind=..., base_sha=..., review_terminal=..., expect_checks=...)`. The push (fenced: `git push origin <target_sha>:<HEAD_BRANCH>`), "never forced", origin only. Rejected versus failed push handling and the post-push `BLOCKED` line (section 4.6 step 12). |
| **8. After the push** | Tier 1: `sync_concluded{pushed}`, the Wave 8 CI wait on `wait_sha = target_sha` with `expect_checks`, no `retrigger-review.sh`, no reply, no resolve, no round. Tier 2: S6 and RESOLVING with zero threads, then S5a (see `refs/conflict-intent.md`, Tier 2). The skip rule: a PR still conflicting with nothing pushed skips the CI wait with reason `pr_conflicting`. |
| **9. Where an unfinished merge is left** | Abort when the resolution is incomplete (Tier 3 found mid-way, validator disagreement, VAL red after the retry, a `uv` failure); `resolution.md` and the evidence files are kept in the output dir. Leave the merge in progress only when the resolution is complete and validated but the run must stop (L2 step 8; `hook_rejected` at step 9) (OQ-19, J-53). |
| **10. Resume** | Section 4.8 of this design: `conflict_resume_plan` rows (abort-and-restart of our own interrupted merge only on `--resume` with a matching `base_sha`; a foreign or L2 merge in progress halts) and `recovery.resolve_crash_window_plan` rows per push kind; a `sync` or `ci` push never resumes into the review states; a rejected push is never re-driven; a conflict push that no crash record can match (an interrupted or `push_failed` Branch B re-drive) halts `resume_unrepresentable` with its `target_sha` named and is never retried (row 4b'); every resume halt closes an open cycle exactly once. |
| **11. Prohibited operations (in words)** | Never stash (the stash stack is shared by every worktree), never skip hooks, never amend, never stage everything, never take one side for a whole tree or a whole merge (only the one named lock file is seeded from the PR side), never hard-reset, never check out the base branch or touch another worktree or branch, never write stored git configuration, never replay a recorded resolution, never push anywhere but `origin` and the PR head branch, never push a rewritten history. |
| **12. Halt reasons and messages** | The table of section 9 of this design (reason, when, operator message, recovery), including the `merge_preflight_dirty` message: "Your checkout has uncommitted changes to tracked files: <paths>. Nothing was merged or pushed. Commit or discard those changes yourself (never stash: the stash is shared by every worktree), then re-run with `--pr <N>`." |
| **13. Revert** | A pushed merge commit is reverted by a new commit: `git revert -m 1 <merge_sha>`. Never by rewriting history. |

**Pinned phrases** (asserted by `test_conflict_sync_protocol.py`, section 12.1): `git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>`; `git push origin <target_sha>:<HEAD_BRANCH>`; `git checkout --ours -- uv.lock`; `uv lock --check`; `git add -- uv.lock`; `merge_parent_ok(<parents>, pre_push_sha, base_sha)`; `git merge-base --is-ancestor <base_sha> origin/<base>`; `The deterministic core DECIDES`; `evaluate_sync_decision`; `sync_started`; `reason `pr_conflicting``; `--evidence-sha`; `expect_checks`; `push_rejected`; `push_failed`; `git revert -m 1 <merge_sha>`; `Nothing was changed and nothing was pushed.`; `never stash`. Order pins: the head check and `merge_preflight_ok` come before `sync_started`, which comes before the merge command; the head re-read comes before `merge_parent_ok`, before `--is-ancestor`, before `The deterministic core DECIDES`, before the push line.

### 8.3 `refs/conflict-intent.md` (new)

Loaded only for Tier 2 at `C-initial`. Not core-pure. Target size about 90 lines.

| Section | Normative content |
|---|---|
| **1. Scope** | Tier 2 only, L3 only, `--conflict-max-tier 2` only. The attended main session does the judgment (J-39, R-173): no new agent, no second model client. "Ours" is this PR, "theirs" is the base tip (S-09). |
| **2. Evidence, one file at a time (J-40)** | For each `text:*` path in plan order: fenced `scripts/collect-conflict-evidence.sh --path <p> --out <output-dir>/sync/<cycle_id>/<n>/ --base-sha <base_sha> --merge-base <merge_base>`. Read the three stage files as three sides and compare each side with the base (stage 1) to tell which side changed a line and which merely has it (S-12, S-13, S-14, S-17); read `log.txt` and both merge-base diffs (R-112). A read-only `git grep <symbol>` is allowed to find callers (R-181). `EVIDENCE_FAIL` of any kind, or an unreadable file, escalates to Tier 3 (`sync_tier3`, R-84). |
| **3. High-suspicion checklist (R-180, R-251, S-26)** | Before editing a file: does either side change a function signature, a type or schema, a dependency, a constant or environment variable, or a public API while the other side adds or changes callers? Does one side remove an old API, field or column while consumers remain? Any yes: the file's kind is `semantic` and the cycle escalates to Tier 3. |
| **4. Kind and rule per kind** | `trivial` (adjacent edits split artificially): combine both (R-150); one side changed one part of a line and the other another part: combine both changes into the line (S-18). `additive`: keep both, in a stated order (R-151). `competing`: pick or synthesize by intent, subject to section 5 (R-152). `structural` (move or rename against edit): apply the edit at the moved or renamed location (R-153). `modify-delete`: decide which intent supersedes; the deletion wins only when the edit is shown obsolete, else restore the file and keep the edit (R-154, S-39). `add-add`: merge the two files' contents, never keep one and drop the other silently (S-40). Name the structural root cause in one phrase (R-146). |
| **5. Intent rules** | Edit a file only when each side's intent can be stated in one sentence; otherwise stop: Tier 3 (R-18, R-05). Do not invent a behaviour that neither side wrote (S-26). Before staging, write one sentence describing the behaviour after the merge; if you cannot, you do not understand the resolution yet (R-156). When a side's behaviour is dropped, say which and why in `dropped` (S-29). Stage each finished file at once with `git add -- <path>`, or `git rm -- <path>` for a deletion (J-56). |
| **6. The resolution record** | `<output-dir>/sync/<cycle_id>/resolution.md`, one section per `text:*` path, fields in this order: `## <path>`, `kind:`, `root_cause:`, `ours_intent:`, `theirs_intent:`, `resolution:` (`keep_both(<order>)`, `take_ours`, `take_theirs`, `synthesized`), `behavior_after:`, `dropped:` (`none` or the behaviour and why), `evidence:` (the stage files and commits consulted). Validated by `resolution_record_ok`; any problem means no commit. |
| **7. Grounding check** | Spawn `evidence-validator` (read-only: Read, Grep, Glob) once over `resolution.md` and the evidence directory; it checks that each entry's intents and `behavior_after` are grounded in the stage files and diffs. One revision pass; still unsupported: abort, Tier 3 (`sync_tier3`). Mandatory in this release (OQ-12). |
| **8. Commit message** | `merge_commit_message(..., tier=2, record=...)`: one line per file with `kind`, `resolution`, `dropped`; intents, never file content; the session's attribution lines appended. |
| **9. After the merge push** | S6 and RESOLVING run with zero threads. S5a re-triggers because the push kind is `merge` (`should_retrigger`). At `C-initial` no reviewer has been observed yet, so the re-trigger targets the **configured reviewers** (those with non-blank identities in the detection contract, `reviewer_identities(contract, r)`) through `pending_retriggers(<events>, cycle_id, <configured reviewers>)`; each POST's watermark starts that reviewer's S5 attribution, so a review of the pre-merge head is never attributed (INV-030). The S5 wait is the run's first review wait; its attributed outcome ticks `round_counter` once. |
| **10. Findings after a merge (INV-031)** | For the rest of the run, a review finding on a path that the PR's own diff does not touch (`git diff --name-only origin/<base>...HEAD`, read once after the merge push) is `REPORT_ONLY` with reason `base_authored` at Wave 3; it consumes no round. |

**Pinned phrases**: `scripts/collect-conflict-evidence.sh`; `evidence-validator`; `One revision pass`; `one sentence`; `dropped`; `high-suspicion`; `configured reviewers`; `base_authored`; `git add -- <path>`; `git rm -- <path>`; each record field name in order.

### 8.4 `refs/state-machine.md`

Stays in the T-N50 set: the new text has no `git` / `gh` token. The INV-016 blockquote (`:161-179`, pinned at `test_static_grep.py:749-750`) is not edited.

1. **Wait-only sentence** (`:144-146`): replace "A spent round budget and a silence terminal permit **waiting only**: CI findings are `REPORT_ONLY`, never an additional fix or push." with "A spent round budget and a silence terminal permit **waiting only**: CI findings are `REPORT_ONLY`, never an additional fix or fix push. The single exception is the one Tier 1 sync push (5.2d), which is not a fix." (The original is hard-wrapped across `:144-146`; replace the wrapped text and re-wrap at the file's width. The new pin compares prose-joined text, like `test_static_grep.py:746-748`.)
2. **New section 5.2d**, inserted after 5.2c (before `## 5.3`):

```text
### 5.2d Conflict cycles (issue #305): Tier 1 is SKILL-owned, Tier 2 adds one edge

- **Tier 1 (push kind `sync`)** runs at Wave 8 entry, before the CI wait, with no FSM edge,
  exactly like the CI phase (5.2c): no round, no re-trigger, no reply, no resolve. It counts in
  `sync_push_count`, never in `push_count`, and a run has at most `SYNC_CAP = 1` conflict cycle
  (both tiers together). After `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE` that terminal
  stays and the sync outcome is reported alongside it. At L2 the resolution is left validated and
  uncommitted; the caller sets `S4'_HALT_BEFORE_PUSH` only when Wave 8 was entered from `clean` or
  `REPORT_ONLY`.
- **Tier 2 (push kind `merge`)** adds exactly one edge: `(S2_CLASSIFY, conflicting)` goes to
  `HALT_MAX_ROUNDS` when the round gate fires (the same gate as `findings`), else to `S3_FIXING`
  (L2+) or `PROPOSED` (L1) by G-edit. The cycle then follows the existing edges
  `S3_FIXING → S7_VALIDATING → S4_PUSHING → S6_REPLYING → RESOLVING` (zero threads)
  `→ S5a_RETRIGGER_REVIEW → S5_AWAITING_REREVIEW → S2_CLASSIFY`, and ticks `round_counter` once
  on the INV-001 edge. The S5a re-trigger fires when `applied_edits > 0` or the push kind is `merge`.
- A conflict push is authorized by the sibling conjunction `evaluate_sync_decision` (ordinal,
  validated, tier allowed, under cap), never by the 5.3 conjunction, whose predicate (5) means
  grounded finding edits. Its parent check is `merge_parent_ok`: exactly two parents, the stored
  pre-push SHA first and the recorded base tip second.
- **Tier 3 never enters the FSM.** At L3 it halts before arming (`terminal_halted`, reason
  `conflict_tier3`); a Tier 3 found by a later hook takes the human-gate route to `HALT_HUMAN`, or is
  reported alongside a preserved terminal.
```

(The arrow glyphs are the ones the file already uses at `:104`; no em dash.)

### 8.5 `refs/ci-poll.md`

1. `:21`: replace "only two parsed empty arrays justify `clean`." with "only two parsed empty arrays, with `expect_checks` false, justify `clean`; with `expect_checks` true an empty chosen list is `polling` (see Expected checks after a push)."
2. Wave 8 entry table rows `:28-29`, last cell: `No: CI findings → `REPORT_ONLY`` becomes `No: CI findings → `REPORT_ONLY` (the one Tier 1 sync push of Wave 8a is the only push allowed here, and it is not a fix)`; the `TERMINAL_AUGMENT_NO_RESPONSE` row's `No` becomes `No (the one Tier 1 sync push excepted)`.
3. After the table, one sentence: "When the PR is still conflicting and no merge commit was pushed, the SKILL skips the CI wait with reason `pr_conflicting`: GitHub runs no `pull_request` checks on a conflicting PR, so the lists would read empty."
4. New section after "Log fetch":

```text
## Expected checks after a push (`expect_checks`)

Right after a push the new head has no checks yet, so an empty list must not read as `clean`
when the repository has checks. The SKILL sets `expect_checks` once per push with
`superclaude.pr_submit.ci.expect_checks_after_push` and records it on the push records, so
`--resume` reuses it. Evidence for the replaced head and the base tip is commit-scoped:
```

```bash
scripts/poll-ci-checks.sh --evidence-sha <sha> --repo <owner/repo>
gh api repos/<owner/repo>/commits/<sha>/check-runs --jq .total_count
gh api repos/<owner/repo>/commits/<sha>/status --jq .total_count
```

followed by: "The script runs the two reads and prints `{"evidence_sha": "<sha>", "evidence_checks": <n>, "source": "ci"}`, with `n = -1` on a failed or unparsable read. `-1` counts as having checks (fail closed). Only when checks were not seen earlier in the run and both evidence reads are 0 is an empty list `clean`. With `expect_checks` true, expiry is the existing Wave 8 CI timeout with reason `ci_not_started`; it is never `clean` and the report never says tests passed."

Both `gh api` lines carry a `repos/<owner/repo>/` path, so they satisfy `_repo_scoped` (`test_static_grep.py:103-129`).

### 8.6 `refs/loop-guard.md`

In the T-N50 set; token-free edits only.

1. `:86` heading: "The 41 event types (§11.3 + §12.1 + V1.1 §6.1 + silence + reviewers)" becomes "The 43 event types (§11.3 + §12.1 + V1.1 §6.1 + silence + reviewers + conflict cycles)".
2. `:88`: "EXACTLY 41 members" becomes "EXACTLY 43 members"; the sentence adds "and the 2 conflict-cycle events (`sync_started`, `sync_concluded`)"; the list gains the two names at its end.
3. One sentence in the run-log schema section: "The `cycle_id` prefixes `sync-` and `conflict-` are reserved for conflict cycles (Tier 1 and Tier 2); a fix cycle's `cycle_id` never starts with either."

### 8.7 `commands/pr-submit.md`

1. `argument-hint` (`:8`): insert `[--conflict-max-tier {0,1,2}]` after `[--pr <N>]`.
2. Options table (`:42-56`), new row after `--pr <N>`:
   `| `--conflict-max-tier {0,1,2}` | 1 | Highest merge-conflict tier to act on: 0 detect and report only; 1 also regenerate a conflicted root `uv.lock` (Tier 1); 2 also resolve text conflicts by stated intent (Tier 2, off by default). Tier 3 always halts at L3. |`
3. Activation context (`:75`): "`--monitor` ordinal (0/1/2/3) and `--max-rounds` / ..." gains "/ `--conflict-max-tier`".
4. Will Not (`:85`): replace "push any commit besides the cycle's one fix commit (it halts with `push_range_mismatch` instead, so unreviewed local commits are never published);" with "push any commit besides the cycle's one fix commit (it halts with `push_range_mismatch` instead, so unreviewed local commits are never published), except a conflict cycle's one merge commit, whose parents must be exactly the PR head and the recorded base tip (`merge_parent_ok`); rebase a published PR head (at L1+ the create path no longer rebases);". The pinned clause (`test_static_grep.py:755`) stays verbatim. `version: "1.0"` (`:9`) is not bumped (G30).

## 9. Halt and report reasons

Every halt is `terminal_halted{reason, ...}` (an existing event; reasons are free text like `pr_head_mismatch`), preceded by `sync_concluded{halted or aborted, reason}` when a cycle had started. Nothing is pushed unless the row says so. Messages end with the recovery steps; none tells the operator to discard a file holding their own changes, and none suggests stashing.

| Reason | Raised at | Operator message (summary; full text in `refs/conflict-mechanical.md` section 12) |
|---|---|---|
| `foreign_op_in_progress` | Wave 0 operation check; resume row 3 | A merge, rebase, cherry-pick, revert or sequencer operation is in progress (named). Nothing was created or pushed. Finish or abort it yourself, then re-run. For a merge left by an earlier L2 run: commit and push it yourself, or abort it, then re-run |
| `conflict_tier3` | Wave 0 (L3); `C-initial`; Wave 8a from `clean` / `REPORT_ONLY` | the Tier 3 template (section 8.2, row 4) |
| `late_conflict` | Wave 8a Tier 2; end of the CI wait when `mergeable` reads `CONFLICTING` again | PR #N conflicts with `origin/<base>`; a text conflict is resolved only before the first review (`--conflict-max-tier 2`, L3). Nothing was pushed for it. Late re-sync is #361 |
| `tier_above_cap` | Wave 8a | The conflict is Tier t, above `--conflict-max-tier c`. Nothing was pushed. Re-run with a higher cap or resolve it yourself |
| `github_disagrees` | Wave 8a | GitHub reads conflicting, a local merge of `origin/<base>`@sha is clean; CI was not waited for. Re-run in a few minutes |
| `probe_failed`, `merge_tree_unsupported` | Wave 8a (tier unclassified) | Conflict detection could not run (reason); the PR reads conflicting, so CI was not waited for |
| `sync_cap` | Wave 8a; `sync_fail_state` (s4) | A conflict cycle already ran in this run (at most one). Nothing more was pushed |
| `merge_preflight_dirty` | step 2; precheck `tree_dirty`; post-commit `tree_dirty` | Uncommitted changes to tracked files: paths. Commit or discard them yourself (never stash), then re-run. After a commit: the local merge commit is named |
| `sync_foreign_operation` | step 2 `foreign_op`; `FINISH_FAIL no_merge_head` / `foreign_merge`; resume row 6 | Another operation owns the checkout. It was not touched |
| `sync_merge_failed` | step 4 (git refused, or probe and merge disagree); step 5 `uv` failure | git's own file list, or the failing command's output; the merge was aborted |
| `sync_marker_left`, `sync_unmerged_left`, `sync_staged_unexpected` | step 9 finish gate | The guard that failed and the paths; the merge stays in progress with nothing committed |
| `sync_commit_failed` | step 9 `hook_rejected` | Hook output verbatim; the merge stays in progress with the resolution intact; commit it yourself after fixing the cause, or abort |
| `sync_head_mismatch` | step 1; step 10(a) | The PR head moved or the checkout is not the PR head; the local merge commit is named when one exists |
| `sync_range_mismatch` | step 10(b); `FINISH_FAIL parents_mismatch` | The commit's parents are not exactly the PR head and the recorded base tip |
| `sync_base_moved` | step 10(c) | The recorded base tip is no longer on `origin/<base>` (the base was rewritten) |
| `sync_tier3` | steps 5 to 6 (Tier 2 escalation: semantic, intent not statable, validator disagreement, evidence failure, unreadable file) | Tier 3 template plus the reason; the merge was aborted; `resolution.md` kept |
| `sync_validation_failed` | step 7 | The red gate; a red base can cause this (command to check `origin/<base>` given); the merge was aborted |
| `push_rejected` | step 12; resume row 1 | git's rejection verbatim; never re-driven |
| `push_failed` | step 12 (first push or Branch B re-drive) | The push failed (stderr verbatim). After a first push, `--resume` checks whether it landed (three-way remote check, row 4b). After a failed re-drive, `--resume` does not retry: it halts `resume_unrepresentable` (row 4b'), and the operator compares `target_sha` with the PR head |
| `resume_unrepresentable` (row 4b') | `--resume` with an open conflict cycle whose dangling push no crash record matches | The merge commit `target_sha` of cycle `cycle_id` may or may not be on the PR. Nothing more was pushed. If the PR head (`gh pr view <N> --repo "$REPO" --json headRefOid`) equals it, re-run with `--pr <N>`; otherwise push or drop it yourself |
| `resume_unrepresentable` | `crash_resume_plan`, `conflict_resume_plan` | The run-log cannot place the conflict cycle safely; a local merge commit is named so the operator can push or drop it |
| `router_unreachable` | `conflict_action` default row | Internal routing error; nothing was changed |

Report-only reasons (no halt by themselves): `no_conflict`, `behind_only`, `blocked`, `tier1_planned`, `tier2_planned`, `tier2_report_only`, `tier1_deferred`, `tier1_proposed`, `tier1_l2_preserved`, `tier1_local`, `tier1_sync`, `tier2_merge`, `no_round_budget`, `l0`, `tier1_l1_preserved`. The router's reason set (`REPORT_REASONS`) and the halt set (`HALT_REASONS`) deliberately overlap in exactly eight reasons, which are router return values that end the run `terminal_halted` on some rows: seven of them halt at one hook or entering outcome and are only reported at another, and `router_unreachable` always halts (it is in `REPORT_REASONS` only because the router returns it): `tier_above_cap`, `conflict_tier3`, `probe_failed`, `merge_tree_unsupported`, `github_disagrees`, `sync_cap`, `late_conflict`, `router_unreachable`. Whether a reason halts is decided by the `ConflictAction.status` of the row, never by the reason string. CI-side report reasons: `pr_conflicting` (CI wait skipped), `ci_not_started` (CI expiry with no registered check). Wave 3 report reason: `base_authored`.

## 10. Decision register

Every item below is decided; the implementer faces no open design choice. "Spec" means the spec's recommendation was taken; "Changed" means evidence or a fail-closed preference led elsewhere.

### 10.1 Open questions OQ-1 to OQ-32

| ID | Decision | Rationale |
|---|---|---|
| OQ-1 | Default `--conflict-max-tier 1` in this release (Spec) | Default 2 would push model-resolved text merges for every L3 user before the P2 live gate |
| OQ-2 | Behind-only (`BEHIND`) is report-only (Spec) | A clean sync is the same machinery and can be enabled later by one router row; no evidence yet that it is wanted |
| OQ-3 | Closed: Tier 2 re-triggers reviewers through the P2 edge and the widened S5a rule; Tier 1 does not (Spec) | J-66: a Tier 2 resolution is authored code |
| OQ-4 | Closed: Tier 1 acts on all four armed Wave 8 outcomes at L3 and keeps a preserved status; L2 only reports after a preserved terminal (Spec) | INV-003; section 4.4 |
| OQ-5 | Closed: hermetic real-git tests in pytest temporary directories are the release proof (Spec) | User scope decision |
| OQ-6 | Seed `uv.lock` from the PR side (`git checkout --ours -- uv.lock`), then `uv lock` (Spec) | The PR side's pins are kept; `uv lock` adds what the merged manifest requires. Verified on a real conflict post-release (section 14) |
| OQ-7 | Closed: at L1+ the create path neither rebases nor halts when behind (Spec) | AD-7 of the spec |
| OQ-8 | No capability probe for the `gh pr view` fields; a failed or unparsable read gives null hints and the probe runs (Spec) | Correct without the hints; the probe is the source of truth |
| OQ-9 | `TIER2_MAX_FILES = 8`; `regen:*` paths do not count (Spec value; counting decided) | The cap bounds model work, and regenerated files cost no model work |
| OQ-10 | A conflicted `pyproject.toml` is Tier 2 (`text:content`); `uv lock --check` joins VG-1 and VG-2 is mandatory at Tier 2 anyway (Spec, strengthened by OQ-16) | High suspicion is covered by the checklist and full tests |
| OQ-11 | Closed: the caller sets `S4'_HALT_BEFORE_PUSH` only when Wave 8 was entered from `clean` / `REPORT_ONLY` (Spec) | `fsm.py:1118-1124` precedent |
| OQ-12 | `evidence-validator` is mandatory for Tier 2 (Spec) | Only independent check on a model-authored push; its disagreement rate is a post-release measurement |
| OQ-13 | The SKILL writes the commit message file with `merge_commit_message` plus the session's attribution lines; `finish-merge.sh` only commits it (Spec) | Keeps attribution policy out of the script |
| OQ-14 | Leave `needs_rebase` and its docstring as is (Spec) | L0 still rebases on the create path, so the docstring stays true; pinned by T-107 |
| OQ-15 | Reason `foreign_op_in_progress` (Spec default) | Matches the probe's `foreign_op` field |
| OQ-16 | **Changed:** VG-2 (`make test`) is mandatory for every Tier 2 cycle | Fail closed on the core residual risk K14; Tier 2 is opt-in, so the cost lands only on runs that asked for it. Enforced by `conflict_validation_status` |
| OQ-17 | **Decided:** no Tier 2 event types; both tiers use `sync_started` / `sync_concluded` with `tier` and `kind` fields; 41 to 43 | One write-ahead bracket serves both tiers' resume needs; fewest pin edits |
| OQ-18 | Guard order head, parent, base ancestry, decision (Spec) | Same order as Wave 6 (head then parent); the network check runs last |
| OQ-19 | Abort when the resolution is incomplete; leave in progress only when complete and validated (Spec) | A clean tree plus the kept `resolution.md` is better than a half-resolution, and a leftover merge would halt the next run's Wave 0 check anyway |
| OQ-20 | Wording fixed in sections 8.1 E9c, 8.4 item 1, 8.5 item 2 and pinned (section 12.2) | Meaning was agreed; this design writes the words |
| OQ-21 | **Decided (option B):** Tier 2 is resolved only at L3 at `C-initial`; at L1 and L2 it is reported, and at Wave 8a it is never resolved at any ordinal | Removes the L2-does-more-than-L3 inversion (INV-010); pinned by the ordinal-monotonicity property test |
| OQ-22 | **Decided:** a local two-parent merge commit with no `push_initiated` found on resume halts `resume_unrepresentable`; it is never pushed | Fail closed: its tree is unproven (operator or amended commit, INV-005); the crash window is tiny |
| OQ-23 | **Decided:** each acting hook re-probes and routes by the fresh plan through `conflict_action`; a tier rise at `C-initial` or Wave 8a follows the table (Tier 3: halt or human-gate route; Tier 2 at Wave 8a: `late_conflict`) | INV-011; one router covers every hook |
| OQ-24 | **Decided:** a tier above the cap is reported at Wave 0 and the review runs; at Wave 8a the CI wait is skipped (`pr_conflicting`) and the run ends `terminal_halted`, `tier_above_cap` (or alongside a preserved terminal) | INV-012; truthful status, no action above the cap |
| OQ-25 | **Decided (adopted):** the finish gate requires every staged or merge-changed path that is not resolved to equal the probe's merge-tree blob | Proves the commit adds nothing beyond the auto-merge plus the resolved paths (INV-013); one `rev-parse` per path |
| OQ-26 | **Decided:** no baseline VAL run on the base; a red VAL halts and the message names the command to check `origin/<base>` | A baseline doubles VAL cost; halting is safe and the operator can tell |
| OQ-27 | **Decided:** GitHub `CONFLICTING` with a clean local probe is Tier 0 for action, reported `github_disagrees`; at Wave 8a it skips the CI wait and ends `terminal_halted` from `clean` / `REPORT_ONLY` | INV-022; fail closed, because CI would not run on a PR GitHub calls conflicting |
| OQ-28 | **Decided:** when any hook saw a conflict, re-read `mergeable` before `transition(clean)`; `CONFLICTING` ends `terminal_halted`, `late_conflict` | INV-027; one extra read only on conflict runs |
| OQ-29 | **Decided:** accept the race; per-reviewer watermarks taken after the `C-initial` re-trigger POST and the existing head-equality gate never attribute a pre-merge review; a missing review ends in the existing `TERMINAL_TIMEOUT`. Measured in the P2 live runs | INV-030; bounded by existing gates, no new mechanism justified without evidence |
| OQ-30 | **Decided (adopted, path level):** after a merge push, a finding on a path the PR's own diff does not touch is `REPORT_ONLY` (`base_authored`) | INV-031; cheap and deterministic; line-level scoping deferred until evidence |
| OQ-31 | Not adopted: untracked files stay tolerated (Spec) | The tracked-tree check plus the finish gate already keep the committed tree equal to the validated tree; the shipped rule's input (`pyproject.toml`) is tracked in any uv project |
| OQ-32 | Not adopted: merge-method fields stay advisory; a rejected push halts `push_rejected` (Spec) | Branch policies are not reliably readable; the rejection is the backstop |

### 10.2 LOW items

| Item | Decision | Rationale |
|---|---|---|
| INV-016 | `--no-renames` on every diff that feeds the finish gate and the probe's numstat | Comparable path sets; a spurious halt otherwise |
| INV-019 | One bound for the whole run: `SYNC_CAP = 1` conflict cycle across both tiers | At most one merge commit per run, the simplest safe reading |
| INV-020 | 8, regenerated files not counted (OQ-9) | as OQ-9 |
| INV-021 | Tier 2 acts only when `max_rounds - round_counter >= 2` (`no_round_budget` otherwise) | The merge spends one round and leaves at least one for fixing review findings; covers `--max-rounds 0` and `1` |
| INV-025 | Handled: exact root-relative `pattern` | Rule 7 |
| INV-032 | Accepted: a commit hook that rejects legitimate marker lines halts `sync_commit_failed` with the merge left in progress | Safe failure; hooks stay on |

### 10.3 Unresolved diff points

| ID | Decision | Rationale |
|---|---|---|
| S-001 (document size) | No design impact; this design has its own structure | Presentation of the spec only |
| S-002 (front matter) | No design impact | Presentation |
| S-003 (heading counts) | No design impact | Presentation |
| S-004 (section order) | No design impact | Presentation |
| S-005 (decision record form) | Resolved in debate; this design records decisions in section 10 | n/a |
| S-006 (grounding section) | Resolved in debate; section 3 | n/a |
| S-007 (requirement format) | No design impact; requirements are referenced by the spec's FR / NFR ids | Presentation |
| C-028 / X-019 (VG-2 at Tier 2) | VG-2 mandatory at Tier 2 (OQ-16) | Fail closed |
| C-029 / X-011 (Tier 2 events and count) | No new Tier 2 events; total 43 (OQ-17) | Fewest pins |
| X-009 (guard order) | head, parent, base ancestry, decision (OQ-18) | Mirrors Wave 6 |

### 10.4 Merge-log executor notes

| Note | Decision |
|---|---|
| 1. "finish-merge.sh re-asserts the clean tree right before the regenerate" | `finish-merge.sh --precheck` runs right before the regenerate (step 5); commit mode runs at step 9. Two modes of one script, one gate implementation |
| 2. `FINISH_FAIL tree_dirty` mapped to `merge_preflight_dirty` | Kept; the post-commit case names the local merge commit |
| 3. The probe emits `binary_paths` raw | Changed: the probe emits the two raw `numstat -z` listings (base64) and the core's `parse_numstat_binary` derives binary paths; all parsing stays in tested Python. It also emits `merge_tree_b64` instead of a `stage_records` string (NUL-safe) |
| 4. FR-26 to FR-33 are restatements | No design impact; all covered |
| 5. Phase placement of unphased items | Moot: one release ships all of them |
| 6. Risk rows "Not rated" | No design impact; section 16 lists the residual risks |
| 7. `conflict_action` vocabulary | Adopted: `none`, `report`, `propose`, `resolve_local`, `resolve_push`, `halt`, plus `reason`, `status`, `skip_ci`, `fsm_event`, `push_kind` |
| 8. OQ-14 lost its "create path only" clause | Correct as is: `needs_rebase` is still used only by the L0 create path |
| Residue (4.3 (g) "confirms") | This design says "grounding check" throughout |

### 10.5 Additional design decisions made here

| ID | Decision | Rationale |
|---|---|---|
| D-1 | Base64 transport for `-z` listings and the status porcelain | Bash variables drop NUL bytes; base64 is portable (`base64 \| tr -d '\n'`) and the core decodes strictly |
| D-2 | Rule 0, `halt:unsafe_path`, for paths with control characters | Lets the manifest and every script use simple line formats without escaping |
| D-3 | `conflict_plan` never sees the cap; `conflict_action` owns every cap, budget and ordinal decision | Single router (spec NE6); the plan is pure shape classification |
| D-4 | `probe_failed` and `merge_tree_unsupported` give an unclassified plan (report only), while a malformed probe JSON gives Tier 3 | A prerequisite failure is not evidence of a dangerous conflict; a malformed result from a script that claimed success is (NFR-5) |
| D-5 | One uniform Wave 8a status rule: an unresolved conflict from `clean` / `REPORT_ONLY` ends `terminal_halted` at every ordinal (except L1 Tier 1 `proposed` and L2 Tier 1 `halt_before_push`); after a preserved terminal it is reported alongside | Truthful (INV-027), ordinal-monotone (INV-010), and no `transition(clean)` on a PR that cannot merge |
| D-6 | The acting hooks' GitHub read includes the head fields, so step 1 needs no extra call | Per-hook call ceiling (NFR-14) |
| D-7 | Step 4 requires the merge's unmerged set to equal the probe's set; a disagreement aborts | Same `base_sha`, same algorithm: a difference means something changed underneath (INV-022 safe side) |
| D-8 | A non-rejection push failure leaves `push_initiated` dangling and halts `push_failed`. For a cycle's first push, `--resume` settles it by the three-way remote check (row 4b). For a Branch B re-drive, whose key is already finalized, `--resume` halts `resume_unrepresentable` and closes the cycle without retrying (row 4b') | The push may have landed; the existing recovery is the right tool where it can match the record (J-77), and fail closed where it cannot (N1) |
| D-9 | Ship `collect-conflict-evidence.sh` as a script | The 200 KiB / 60 s bounds and the exact file layout are testable hermetically; `evidence-validator` can only read files |
| D-10 | `should_retrigger(applied_edits, push_kind)` in `fsm.py` carries the widened S5a rule; `run_skill` calls it with the fix default | One named predicate, testable as the zero-edit pair, no behaviour change for fix cycles |
| D-11 | `build_push_triad` takes either decision type, by `isinstance(PushDecision)` or the `audit_predicates` attribute | No builder duplication, no `fsm` to `conflicts` import |
| D-12 | NFR-4 restated: Tier 0 costs the local operation check plus one `gh pr view` read per hook (Wave 0 and Wave 8a), plus `UNKNOWN` re-reads | Wave 8a must read GitHub to notice a conflict that appeared during review |
| D-13 | `mergeability_hint` returns a fifth value, `blocked` | `BLOCKED` gets its own report reason (spec FR-2 own row) |
| D-14 | `probe-merge.sh` takes `--repo` and refuses to fetch unless `origin` resolves to it | Gives `--repo` a safety purpose in a script with no `gh` call; the fetch can only reach the fork |
| D-15 | On `--resume`, our own interrupted pre-commit merge is aborted and the cycle restarted under the same `cycle_id` (no partial Tier 2 resume) | Deterministic; `resolution.md` is kept as input; the same id keeps `SYNC_CAP` honest |
| D-16 | Snapshot paths (`__snapshots__/`, `*.snap`) are `halt:generated_no_recipe` | R-60 folded into rule 9 rather than resolved as text |

## 11. Research item map (the 74 items scored above 5)

One row per ID of `03-roi-scored-list.md` "Items scored above 5", in that file's order. **69 adopted, 5 rejected.**

| # | ID | ROI | Decision | Design element |
|---|---|---|---|---|
| 1 | R-02 | 8 | Adopt | Section 2.1 scope boundary: no git education, no blanket side sweeps, no force-push recovery, no general review inside the conflict path |
| 2 | R-05 | 10 | Adopt | Tier model (4.3): mechanical work automated (Tier 1), judgment explicit (Tier 2 record), halt when intent is unclear (8.3 row 5, Tier 3) |
| 3 | R-11 | 10 | Adopt | `finish-merge.sh` marker check (7.2 commit step 4), counting introduced markers only |
| 4 | R-13 | 9 | Adopt | Prohibited operations (8.2 row 11) and the FR-21 static regex (12.1); only the one named lock file is seeded from one side |
| 5 | R-14 | 9 | Adopt | Same as R-13 for the other side |
| 6 | R-15 | 10 | Adopt | Prohibited operations; static regex for a hard reset in the new files |
| 7 | R-18 | 9 | Adopt | 8.3 row 5 (one-sentence intents or Tier 3); `resolution_record_ok` one-sentence check |
| 8 | R-19 | 8 | Reject | No user-override channel: the skill has no mid-run override prompt; an override is a re-run with a different flag (spec 3.2 R9) |
| 9 | R-20 | 8 | Reject | Same as R-19 |
| 10 | R-26 | 6 | Adopt (simplified) | Unmerged paths listed by the probe's merge-tree records and by `git diff --name-only --diff-filter=U` in step 4 and the finish gate; no tab-separated status protocol |
| 11 | R-43 | 7 | Adopt | Rule 1 `halt:submodule` (mode `160000`) |
| 12 | R-51 | 7 | Adopt | The plan report before any edit (8.2 row 3, FR-4) |
| 13 | R-54 | 8 | Adopt | Rule 5 `halt:migration`; Tier 3 halt message shows the path |
| 14 | R-56 | 8 | Adopt | Rule 1 halt; the Tier 3 message names the path and class for the operator's choice |
| 15 | R-57 | 8 | Adopt | Rule 6 `halt:binary` from the numstat listings |
| 16 | R-58 | 9 | Adopt | Rule 7 and step 5: regenerate after the manifest is resolved and staged (Tier 2 handles `pyproject.toml` first) |
| 17 | R-59 | 9 | Adopt | Rules 8 and 9: halt when no rule names the source |
| 18 | R-60 | 6 | Reject | No snapshot regeneration; snapshot paths fold into rule 9 and halt (D-16) |
| 19 | R-84 | 8 | Adopt | `EVIDENCE_FAIL unreadable` escalates to Tier 3 (7.3, 8.3 row 2) |
| 20 | R-101 | 6 | Reject | No recombination subsystem; its read-only property is kept by the probe (7.1) |
| 21 | R-112 | 9 | Adopt | `collect-conflict-evidence.sh`: left-right log and both merge-base diffs (7.3) |
| 22 | R-128 | 7 | Adopt | `-c rerere.enabled=false` on the merge command (step 4) |
| 23 | R-146 | 7 | Adopt | `root_cause` field of the resolution record (8.3 row 6) |
| 24 | R-149 | 6 | Adopt | Record `kind` labels (`RECORD_KINDS`); `text:content` rule 10 |
| 25 | R-150 | 7 | Adopt | 8.3 row 4 `trivial` rule |
| 26 | R-151 | 8 | Adopt | 8.3 row 4 `additive` rule; `keep_both(<order>)` resolution |
| 27 | R-152 | 7 | Adopt | 8.3 row 4 `competing` rule, bounded by row 5 |
| 28 | R-153 | 9 | Adopt | 8.3 row 4 `structural` rule |
| 29 | R-154 | 9 | Adopt | Rule 11 `text:modify_delete`; 8.3 row 4 `modify-delete` rule |
| 30 | R-156 | 9 | Adopt | `behavior_after` field, one sentence, checked by `resolution_record_ok` |
| 31 | R-161 | 6 | Reject | No `--check` whitespace gate: VG-3 and VG-4 cover format, and inherited base whitespace would force unrelated cleanup (R-169) |
| 32 | R-169 | 8 | Adopt | Step 7 single VAL retry must not introduce unrelated changes |
| 33 | R-173 | 6 | Adopt | No new agent or model client; the attended session resolves (8.3 row 1) |
| 34 | R-180 | 9 | Adopt | High-suspicion checklist (8.3 row 3); a yes is Tier 3 |
| 35 | R-181 | 8 | Adopt | Both merge-base diffs in the evidence; read-only `git grep` for symbols (8.3 row 2) |
| 36 | R-189 | 9 | Adopt | `MECHANICAL_RULES` `uv.lock` rule: `uv lock`, `uv lock --check` |
| 37 | R-210 | 7 | Adopt | Tier 3 HALT template: file, operation, step k/n, branch (8.2 row 4) |
| 38 | R-212 | 7 | Adopt | Tier 3 template's one-sentence side descriptions (when content was read) |
| 39 | R-251 | 8 | Adopt | High-suspicion checklist: removal while consumers remain |
| 40 | S-05 | 7 | Adopt | Wave 0 operation check and probe `foreign_op` (7.1 step 4) |
| 41 | S-09 | 7 | Adopt | Ours/theirs defined in both refs (8.2 row 1, 8.3 row 1) |
| 42 | S-12 | 9 | Adopt | Evidence file `stage2` (`:2:<path>`) |
| 43 | S-13 | 9 | Adopt | Evidence file `stage3` (`:3:<path>`) |
| 44 | S-14 | 9 | Adopt | Evidence file `stage1` (`:1:<path>`); also the finish gate's marker baseline |
| 45 | S-17 | 8 | Adopt | `merge.conflictStyle=zdiff3` per invocation; three-side comparison rule (8.3 row 2) |
| 46 | S-18 | 6 | Adopt | 8.3 row 4: combine both partial-line changes (under `trivial`) |
| 47 | S-26 | 9 | Adopt | 8.3 row 5: never invent a third behaviour; validator grounding check |
| 48 | S-29 | 9 | Adopt | `dropped` field; commit-body line per file |
| 49 | S-38 | 9 | Adopt (simplified) | Tree conflicts found from merge-tree stage sets (rules 11, 12) instead of `status --short` codes |
| 50 | S-39 | 6 | Adopt | 8.3 row 4 `modify-delete`: deletion wins only when the edit is shown obsolete |
| 51 | S-40 | 7 | Adopt | Rule 12 `text:add_add`; 8.3 row 4 merge both contents |
| 52 | S-46 | 9 | Adopt | Step 5 `git add -- uv.lock` |
| 53 | S-53 | 8 | Adopt | Migrations are never touched (rule 5 halt), so no renumbering can happen |
| 54 | J-05 | 8 | Adopt | Only the checked-out PR head branch is merged into and pushed (step 1, step 12) |
| 55 | J-06 | 7 | Adopt | Never check out the base branch: the merge is by SHA from `origin/<base>`; static regex forbids any other checkout |
| 56 | J-13 | 7 | Adopt | Every `*_FAIL` token and halt ends the run (8.2 row 4) |
| 57 | J-15 | 6 | Adopt (reuse) | Detached HEAD fails `pr_branch_ok` (`fsm.py:525`, `:546`) in step 1 |
| 58 | J-16 | 8 | Adopt | `git rev-parse --git-path MERGE_HEAD` detection (7.1 step 4) |
| 59 | J-17 | 9 | Adopt | Foreign operation halts (`foreign_op_in_progress`, `sync_foreign_operation`) |
| 60 | J-18 | 8 | Adopt | `merge_preflight_ok` on the tracked tree; `merge_preflight_dirty` halt |
| 61 | J-20 | 9 | Adopt | Never stash: prohibited operations, static regex, every dirty-tree message |
| 62 | J-26 | 7 | Adopt | Step 1 `HEAD_BRANCH != baseRefName`; push only to `HEAD_BRANCH` |
| 63 | J-39 | 8 | Adopt | The attended session does the Tier 2 judgment; no resolver script or framework |
| 64 | J-40 | 6 | Adopt | One file at a time (8.3 row 2) |
| 65 | J-48 | 7 | Adopt | Rule 7 uses only the lockfile's own manager; rule 8 halts on every other lockfile |
| 66 | J-53 | 6 | Adopt (bounded) | Leave the merge in progress only when the resolution is complete (L2, hook rejection); abort otherwise (OQ-19) |
| 67 | J-56 | 8 | Adopt | Exact per-path staging as each file is finished |
| 68 | J-60 | 8 | Adopt | Hooks on; static regex forbids the hook-skipping flag in the new files |
| 69 | J-61 | 7 | Adopt | `FINISH_FAIL hook_rejected` copies the hook output verbatim |
| 70 | J-63 | 7 | Adopt | No amend after a hook failure (the merge commit does not exist yet); static regex |
| 71 | J-66 | 7 | Adopt | Tier 2 merge is reviewed: P2 edge, S5a re-trigger, a round spent |
| 72 | J-77 | 7 | Adopt | `PROBE_FAIL fetch_failed` ("cannot reach remote origin"); `push_failed` distinguished from `push_rejected` (D-8) |
| 73 | J-83 | 6 | Adopt | Push stderr reported verbatim in `push_rejected` / `push_failed` messages, which covers a pre-push hook failure |
| 74 | J-91 | 9 | Adopt | Current worktree only; no other worktree or branch touched; static regex forbids worktree commands in the new files |

## 12. Test plan

Conventions kept: pure helpers by direct calls with parametrized fail-closed shapes (the `test_pre_pr_checks.py:201-230` style); run-log tests with a real `RunLog` under `tmp_path`; skill text pinned by literal substrings; scripts run with `subprocess.run(..., timeout=...)` and a `gh` stub on `PATH` (the `test_static_grep.py:436-470` and `test_cosmos_poll.py:170-190` pattern). Real git runs only inside `tmp_path` repositories with a local bare repository as `origin`; no test touches the network, a live remote or the operator's `~/.claude`. Each real-git module begins with a capability skip: `pytest.skip` unless `git merge-tree --write-tree HEAD HEAD` succeeds in a scratch repository (never a version parse). Tests set `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, a fixed author and committer, and `UV_OFFLINE=1`, `UV_NO_CONFIG=1`, `UV_CACHE_DIR=<tmp>` for real `uv`.

### 12.1 New test files

| File | Covers | Required cases |
|---|---|---|
| `tests/pr_submit/test_conflicts_core.py` | Section 5 (FR-2, FR-12, FR-13, FR-15, FR-17, FR-23, FR-24, FR-26, NFR-5) | **Hint:** every `mergeable` x `mergeStateStatus` pair incl. `UNKNOWN`, `None`, lowercase, junk; `needs_probe`. **Parse:** `parse_stage_records` on the captured fixture (expects the exact records); each malformed shape raises (bad tree OID, bad mode, short OID, stage 0 and 4, empty path, duplicate `(path, stage)`, missing tab); messages after the empty field ignored; `parse_numstat_binary` binary and text rows and malformed rows; `parse_probe` rejects each invalid field, non-strict base64, `truncated: true`. **Classify:** one parametrized row per rule 0 to 13; boundaries: submodule beats binary; protected beats text; `uv.lock` with `"12"` or `"13"` is `halt:lockfile_no_recipe`; `pkg/uv.lock` with `"123"` is `halt:lockfile_no_recipe`; root `uv.lock` without `uv` in `programs` is `halt:lockfile_no_recipe`; `__snapshots__/x.snap` is `halt:generated_no_recipe`; a path with a tab is `halt:unsafe_path`. **Plan:** each plan-tier row; 8 text paths Tier 2, 9 Tier 3 `too_many_files`; regen plus text is Tier 2 and regen paths not counted; `BLOCKED` row; `probe_failed` and `merge_tree_unsupported` give `None`; malformed gives 3. **Router:** every reachable row of section 4.4 as a literal expected table; every domain violation reaches the default row; L0 row; the ordinal-monotonicity property exactly as stated in section 4.4: hooks `wave0` and `wave8a` only, ordinals 0 to 3, over the full product of the other in-domain inputs (tiers x entering valid for the hook x caps x budgets x prior cycles x hint flag), including the preserved-terminal rows; a separate assertion that every `c_initial` call at ordinals 0 to 2 returns the default row; and a literal check of the Wave 8a Tier 1 `P` column (L1 `report` / `tier1_l1_preserved`, L2 `report` / `tier1_l2_preserved`, L3 `resolve_push`). **Gates:** `merge_parent_ok` matrix (case-insensitive, trailing newline, leading space, swapped order, equal SHAs, 0/1/3 parents, `None`, non-list, short ids); disjointness: for every generated parent list, `push_parent_ok` and `merge_parent_ok` are never both true, and `push_parent_ok(p, pre)` is false for every `p` that `merge_parent_ok(p, pre, base)` accepts; `merge_preflight_ok` rows (clean, staged, unstaged, rename record, untracked `??` ignored, non-string, garbage); `evaluate_sync_decision` 16-row truth table for tier 1 and for tier 2 (with the `round_counter < max_rounds` term), `kind` per tier, invalid tier; cross-gate property: for the same ordinal and validation status, `p1`/`p2` equal `evaluate_push_decision`'s `predicate_1_ordinal`/`predicate_2_validated`; `sync_fail_state` mapping; `conflict_validation_status` (tier 2 without VG-2 is `failed`). **Cycle ids:** `conflict_cycle_id` values and `ValueError`; `is_conflict_cycle` true for both prefixes, false for `"c1"`, `"cB"`, `"round-0"`, `"cycle-1"`, a UUID, `None` (QA-8). **Record and message:** `finish_manifest` lines and its three `ValueError`s; `parse_resolution_record` valid and each `ValueError`; `resolution_record_ok` one test per problem class (missing entry, extra entry, empty field, two sentences, newline, no terminal stop, `semantic`, bad resolution, missing `dropped`); `merge_commit_message` subject format, no file content, tier 2 needs a record. **Resume:** `crash_resume_plan` parametrized kind {fix, merge, sync, ci, absent, junk} x branch {A, B, C, junk} against a literal expected table; missing `review_terminal` / `base_sha` cases; `conflict_resume_plan` one test per row of section 4.8, including row 3b (superseded open cycle halts), row 4c (a missing or unknown `hook` halts; a `wave8a` open cycle without a valid `review_terminal` halts; a `c_initial` cycle with a non-null one halts; 4c is evaluated before row 4), rows 4b and 4b' (a matching `dangling` gives `crash_window`; `None` or another cycle's record gives `halt` / `resume_unrepresentable` with `cycle_id` and `target_sha`), row 1 with and without an open cycle, a `c_initial` restart plan carrying `hook == "c_initial"` (which the SKILL restarts at step 0), `prior_conflict_cycles(["sync-1"], "sync-1") == 0` and `prior_conflict_cycles(["sync-1"], "sync-2") == 1`, and rows 5 and 7 returning the open cycle's `cycle_id`, `hook` and `review_terminal`; the branch literals `BRANCH_LANDED` / `BRANCH_NOT_LANDED` / `BRANCH_AMBIGUOUS` equal `recovery.BRANCH_A_LANDED` / `BRANCH_B_NOT_LANDED` / `BRANCH_C_AMBIGUOUS`; `REPORT_REASONS & HALT_REASONS` equals the eight-reason set of section 5.2. **Triad:** `build_push_triad` default call equals a literal recorded three-record list (the pre-change output, captured from the current `fsm.py:238-288` and pasted into the test); a `sync` call adds `kind`, `base_sha` to all three records and `review_terminal`, `expect_checks` where section 6.1 says; an invalid `push_kind` raises; a `SyncDecision` yields the four `p*` predicates. **Purity:** `conflicts.py` imports only the allowed modules (AST walk) |
| `tests/pr_submit/fixtures/merge_tree_conflict.z` | `parse_stage_records` | Raw NUL-separated output of `git merge-tree --write-tree -z pr main` from a scratch repository with one content conflict (`f.txt`, stages 1/2/3) and one modify/delete (`d.txt`, stages 1/2). The capture recipe (the exact git commands) is a comment at the top of the test |
| `tests/pr_submit/test_conflict_sync_protocol.py` | Skill text (FR-4 to FR-10, FR-14, FR-18 to FR-21, FR-27 to FR-31, FR-33, NFR-1, NFR-4, NFR-6, NFR-8, NFR-9) | The pinned phrases and order pins of sections 8.2 and 8.3; `SKILL.md` edits E1 to E13 (E13: "needs a force-push" absent from the head-binding bullet) present; SKILL still has one python block; every line of `SKILL.md` and `conflict-mechanical.md` naming `conflict-intent.md` or `evidence-validator` (in the new text) also says "Tier 2"; `collect-conflict-evidence.sh` named only in `conflict-intent.md`; every `gh` command line (via `test_static_grep._command_lines`) in the two refs and four scripts is `_repo_scoped`; every `git push` line in the new files is exactly `git push origin <target_sha>:<HEAD_BRANCH>`; **FR-21 prohibited-operation scan** over the two refs and three new scripts with one regex each: `\bgit\s+stash\b`, `--no-verify\b`, `--amend\b`, `\badd\s+(-A\|--all\|\.)(\s\|$\|`)`, `--(ours\|theirs)\s+(--\s+)?\.(\s\|$\|`)`, `\bcheckout\s+--(ours\|theirs)\s*(`\|$)`, `-X\s*(ours\|theirs)\b`, `-s\s+ours\b`, `\breset\s+--hard\b`, `\bcommit\s+--only\b`, `\bcommit\s+(-a\|--all)\b`, `\bgit\s+config\b`, `\bgit\s+worktree\b`, `\bgit\s+rebase\b`, `rerere\.enabled=true`, and every `\bgit\s+(checkout\|switch)\b` occurrence equals `git checkout --ours -- uv.lock`; no `src/superclaude` substring in the new refs, scripts, or the new SKILL / command text (NFR-8); the allowed-tools test: every `MECHANICAL_RULES` `regenerate[0]` / `check[0]` and the first word of every fenced command line in the two refs is `git`, `gh`, `uv`, `make`, `jq` or a `scripts/` path, and each of those programs appears as `Bash(<prog> *)` in the `SKILL.md:4` front matter; static call ceilings (NFR-14): the Tier 1 procedure in `conflict-mechanical.md` contains exactly one probe command, one `finish-merge.sh` commit-mode command and one push command |
| `tests/pr_submit/test_conflict_scripts.py` | `probe-merge.sh`, `finish-merge.sh`, `collect-conflict-evidence.sh`, `poll-ci-checks.sh --evidence-sha` (FR-1, FR-7, FR-11, FR-22, NFR-10, NFR-11) | Section 12.4 cases P1 to P12, F1 to F12, E1 to E4, C1 to C4 |
| `tests/pr_submit/test_conflict_e2e.py` | End-to-end local scenarios (P1 gate (a), and a scripted Tier 2 run) | Section 12.4 cases X1 to X3 |

### 12.2 Changed existing tests (exact edits)

| File and line | Edit |
|---|---|
| `tests/pr_submit/test_run_log.py:165` | Rename `test_eventtype_is_41_members_with_silence_and_reviewer_events` to `test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events`; docstring `:166-167` "EXACTLY 41 members" becomes "EXACTLY 43 members, including INV-S1, the two reviewer-presence events and the two conflict-cycle events" |
| `tests/pr_submit/test_run_log.py:168-169` | `== 41` becomes `== 43` in both asserts; add `assert EventType.SYNC_STARTED.value == "sync_started"` and `assert EventType.SYNC_CONCLUDED.value == "sync_concluded"` |
| `tests/pr_submit/test_run_log.py` (new functions) | `test_fold_sync_push_counts_in_sync_push_count_not_push_count`; `test_fold_fix_ci_merge_and_kindless_pushes_count_in_push_count`; `test_fold_old_log_without_kind_rebuilds_identically` (a recorded legacy log fixture: every pre-existing key equal, new keys at defaults); `test_fold_conflict_cycles_first_seen_order_and_open_cycle` (incl. a resume restart with the same id and `push_initiated` / `push_completed` flags); `test_fold_push_rejected`; `test_fold_open_cycle_carries_hook_and_review_terminal` (B3); `test_fold_push_of_another_cycle_marks_open_cycle_superseded` (B2 belt); `test_rebuild_state_with_a_conflict_push_in_the_fixture` (QA-1: fix push, sync push, merge push, rereview, round tick: exact `push_count`, `sync_push_count`, `round_counter`, `rereview_request_count`); `test_sync_concluded_payload_is_redacted` (a token-shaped string in `dropped` reaches the JSONL as `[REDACTED]`, NFR-7) |
| `tests/pr_submit/test_codex_reviews.py:441` | `assert len(EventType) == 41` becomes `== 43` |
| `tests/pr_submit/test_static_grep.py:37-51` | Append `PR_SUBMIT_PKG / "conflicts.py",` to `CORE_PURE_FILES` with the comment "issue #305: the conflict core is pure (no version-control tokens)". The new refs are deliberately not added |
| `tests/pr_submit/test_static_grep.py:654-661` | Replace the comment and the two pins: comment becomes "`--pr` never rebases a published head; the create path rebases only at L0; at L1+ being behind is a Tier 0 report, not a STOP." Keep `:656` and `:657` asserts verbatim. Replace `:658` with `assert "rebase if behind \`origin/<base>\` only at L0" in text`, `assert "Being behind the base branch is not a STOP at L1+" in text` and `assert "branch (\`origin/<default-branch>\`) on the create path" not in text`. Replace `:659-661` with `assert "\| Wrong origin / wrong-owner URL \|" in text` and `assert "\| Behind base branch (create path at L1+, or \`--pr\`) \|" in text` |
| `tests/pr_submit/test_static_grep.py` (new function) `test_wait_only_sentences_name_the_one_sync_exception` | Asserts the three new wait-only texts: `SKILL.md` "the single Tier 1 sync push of Wave 8a (`SYNC_CAP = 1`) is the only push a wait-only path allows, and it is not a fix"; `state-machine.md` (prose-joined like `:746-748`) "never an additional fix or fix push. The single exception is the one Tier 1 sync push (5.2d), which is not a fix."; `ci-poll.md` "the one Tier 1 sync push of Wave 8a is the only push allowed here, and it is not a fix" (INV-009, FR-33) |
| `tests/pr_submit/test_static_grep.py` (new function) `test_s5a_retrigger_widened_for_merge_cycles_only` | Wave 6 slice contains "or is a Tier 2 merge cycle (push kind `merge`; `superclaude.pr_submit.fsm.should_retrigger`)"; and re-asserts the unchanged `:689` and `:750` substrings (QA-3a) |
| `tests/pr_submit/test_crash_recovery.py` (new functions) | `test_resolve_crash_window_plan_by_kind` parametrized kind {fix, merge, sync, ci, absent} x branch {A, B, C} with a real `RunLog` and the exact `ResumePlan`; `test_recovered_push_completed_copies_kind_and_base_sha`; `test_legacy_record_recovery_events_unchanged` (byte-equal event dicts for a kind-less record); `test_rejected_push_record_is_not_a_crash_window` (the record carries `idempotency_key`; `detect_crash_window` returns `None` and `conflict_resume_plan` halts `push_rejected`); `test_conflict_crash_recovery_closes_the_cycle` parametrized kind {sync, merge} x branch {A, C, halt directive}: exactly one `sync_concluded{recovered: true}` with the outcome of section 4.8 and `open_conflict_cycle is None` afterwards, a second wrapper call appends nothing, kinds `fix` / `ci` / absent append no `sync_concluded`; `test_conflict_crash_then_later_fix_crash_resumes_into_fix_window` (B2: a `sync` crash window recovered through Branch A, then a fix cycle whose `push_initiated` dangles; `conflict_resume_plan` returns `none` and `detect_crash_window` returns the fix record); `test_restart_row_uses_recorded_review_terminal` (B3, m3: an open `wave8a` Tier 1 cycle `sync-1` with `review_terminal: "halt_max_rounds"` and `conflict_cycles == ["sync-1"]` restarts with that `entering`; the router is called with `prior_conflict_cycles == 0` (the reused id excluded) and returns `resolve_push` at L3; the same state with the id not excluded would give `sync_cap`, and the test computes the count with `prior_conflict_cycles(...)`); `test_branch_b_crash_during_redrive_halts_and_closes_once` (N1: `sync` dangling push, Branch B, the re-drive's `push_initiated` written, then a crash before its `push_completed`; the next resume gets `detect_crash_window(...) is None`, `conflict_resume_plan(..., dangling=None)` returns row 4b' `halt` / `resume_unrepresentable` with `target_sha`, exactly one `sync_concluded{halted, recovered: true}` is appended, `open_conflict_cycle is None` afterwards, and a third resume appends nothing and returns row 2 `none`); `test_branch_b_redrive_push_failed_then_resume_halts_and_closes_once` (N1: same, but the re-drive ends `push_failed` with no record; same assertions, and no push command is planned by any directive); `test_resume_row_1_closes_an_open_cycle` (m2: `push_rejected` set while a cycle is open gives one `sync_concluded{halted, reason: push_rejected}`); `test_resume_row_4_expect_checks_defaults_true` (m6: an open `sync` cycle with `push_completed` and no `expect_checks` on its `push_initiated` gives `ResumePlan.expect_checks is True`); `test_branch_b_redrive_landed_closes_cycle_once` (n4: a `sync` dangling push, Branch B, then the re-driven `push_completed` and the SKILL's guarded close give exactly one `sync_concluded{pushed, recovered: true}` and `open_conflict_cycle is None`; a later fix-cycle crash window then resumes into the fix window through row 2; a second close attempt for the closed cycle appends nothing); `test_branch_c_event_order` (m5: `terminal_halted{ambiguous_remote_tip}` then `sync_concluded{halted}`, each exactly once) |
| `tests/pr_submit/test_skill_parse.py` (new function) `test_conflict_max_tier_default_and_bounds` | `parse_args([]).conflict_max_tier == 1`; 0, 1, 2 accepted; `"3"` and `"x"` raise `SystemExit` |
| `tests/pr_submit/test_autonomy_gates.py` (new function) `test_transition_conflicting_edge` | In the `test_auggie_fallback.py:353-379` pattern: L3 with budget gives `S3_FIXING`; spent budget gives `HALT_MAX_ROUNDS`; L1 gives `PROPOSED`; `needs_human_decision` gives `HALT_HUMAN`; `(S2_CLASSIFY, "findings")` still gives `S2B_VERIFY` (unchanged) |
| `tests/pr_submit/test_loop_guard.py` (new function) `test_should_retrigger_zero_edit_pair` | `should_retrigger(0, "merge")` true; `should_retrigger(0, "fix")`, `(0, None)`, `(0, "sync")`, `(0, "ci")` false; `should_retrigger(1)` true; `run_skill` zero-edit rows still give `rereview_request_count == 0` (QA-3b) |
| `tests/pr_submit/test_ci_classify.py` (new functions) | `test_expect_checks_empty_matching_head_is_polling`; `test_expect_checks_nonempty_all_pass_is_clean`; `test_expect_checks_false_keeps_empty_clean`; `test_expect_checks_head_mismatch_is_polling`; `test_expect_checks_non_dict_payload_is_polling`; setter: `pre_push_evidence` 1 gives true; all zero gives false; `-1` gives true; `None` gives true; `pre_push_evidence` 0 with `base_evidence` 2 gives true; `checks_seen_this_run` true gives true. Existing tests `:20-70` unmodified |
| `tests/pr_submit/test_pre_pr_checks.py` (new function) `test_push_parent_ok_still_rejects_a_valid_merge_commit` | `merge_parent_ok([SHA, OTHER_SHA], SHA, OTHER_SHA)` true and `push_parent_ok([SHA, OTHER_SHA], SHA)` false. The `merge` parametrize id at `:216-222` is not touched |
| `tests/unit/test_cli_install.py:248-262` | Add `sc-pr-submit-protocol/refs/conflict-intent.md`, `sc-pr-submit-protocol/refs/conflict-mechanical.md`, `sc-pr-submit-protocol/scripts/collect-conflict-evidence.sh`, `sc-pr-submit-protocol/scripts/finish-merge.sh`, `sc-pr-submit-protocol/scripts/probe-merge.sh` to the expected installed list (presence check only) |

The spec's byte-identical fragments (spec section 8.4), asserted in `test_conflict_sync_protocol.py` as one regression test: "with `--pr <N>`, at any level, do not rebase"; "rebase if behind `origin/<base>`"; the Wave 6 guard wording (`pr_head_ok(<local branch>, pre_push_sha,`, `push_parent_ok(<parents>, pre_push_sha)`, `The deterministic core DECIDES`, `then set `pre_push_sha := target_sha``); "push any commit besides the cycle's one fix commit"; in `state-machine.md` "the commit to push must have exactly one parent, that same SHA" and "The parent check applies only when the cycle applied edits".

### 12.3 Existing tests that must stay green unmodified

Everything under `tests/pr_submit/` other than the edits listed in 12.2, in particular: `test_static_grep.py` except the two edited regions (T-N50 with `conflicts.py` added, T-N41, T-105, T-1101, the repo-scope tests, `test_skill_binds_checkout_and_push_target_to_pr_head` outside `:654-661`, `test_skill_forbids_force_push`, which now also scans the new refs and scripts); `test_cosmos_protocol.py` and `test_codex_reviews.py` (one python block; snapshot gate); `test_auggie_fallback.py` (V1.1 edges); `test_autonomy_gates.py`, `test_loop_guard.py`, `test_validation_gate.py` existing rows (zero-edit no-push, fence-post matrix, VG-3 vs VG-4); `test_crash_recovery.py`, `test_augment_review_remediation.py:145`, `test_codex_reviews.py:489` (`resolve_crash_window` unchanged); `test_ci_classify.py:20-70`; `test_idempotency.py:89` (`len(IDEMPOTENCY_SETS) == 7`); `test_pre_pr_checks.py` existing rows; `test_edge_cases.py:267`; `test_gate_helper_coverage.py` and `test_gate_helper_differentials.py` (G32: unaffected); `test_cosmos_poll.py`, `test_rate_limit.py`, `test_reply_resolve.py`, `test_review_retrigger.py`, `test_silence.py`, `test_timeout.py`, `test_monitor_arm.py`, `test_skill_parse.py` existing rows, all `test_contract_setup_*`; `tests/commands/test_impact_command.py:327-345`; `make verify-sync`.

### 12.4 Hermetic real-git scenarios

Fixture helper (in `test_conflict_scripts.py`, reused by the e2e file): `make_repos(tmp_path)` creates `origin.git` (bare) and a clone `work` with a `main` branch, a PR branch checked out, and a `gh` stub on `PATH` that records calls and serves canned JSON. The skill folder's scripts run from their source path.

**probe-merge.sh**

| Case | Setup | Assert |
|---|---|---|
| P1 | base advanced, no overlap | `clean: true`, `behind > 0`, records empty after parsing |
| P2 | content conflict | parsed stages `"123"`; `merge_tree_oid` 40 hex |
| P3 | file deleted on base, modified on PR | parsed stages `"12"` |
| P4 | binary file changed on both sides | path in the parsed binary set |
| P5 | staged change; unstaged change | `tree_clean: false` for both; decoded `status_b64` names the path |
| P6 | untracked file only | `tree_clean: true` |
| P7 | half-finished rebase (`rebase-merge` dir) | `foreign_op == "rebase-merge"`; `--ops-only` gives the same |
| P8 | any of the above | `git status --porcelain=v1 -z` and `git rev-parse HEAD` identical before and after |
| P9 | `--repo` missing; `--repo` not matching origin | exit 2, stdout `PROBE_FAIL usage` / `PROBE_FAIL origin_mismatch`, no fetch happened |
| P10 | origin unreachable (bare repo removed) | exit 2, `PROBE_FAIL fetch_failed` |
| P11 | stub `git` wrapper first on `PATH` that fails `merge-tree --write-tree` and passes everything else through | `merge_tree_supported: false`, `clean: null` (NFR-11) |
| P12 | a conflict listing above 100 KiB (many conflicting files) | `truncated: true`, `*_b64` null; the core classifies Tier 3 |

**finish-merge.sh**

| Case | Setup (after a real `git merge --no-commit --no-ff <base_sha>`) | Assert |
|---|---|---|
| F1 | one path left unmerged | `FINISH_FAIL unmerged`, no commit |
| F2 | a resolved file still holds an introduced marker | `FINISH_FAIL markers` |
| F3 | a resolved file whose stage-1 blob already had one marker line, result has one | success |
| F4 | an extra non-resolved path staged with content different from the merge-tree blob | `FINISH_FAIL staged_unexpected` |
| F5 | an auto-merged path reverted in the index to `HEAD` | `FINISH_FAIL staged_unexpected` |
| F6 | `--base-sha` not equal to `MERGE_HEAD`; no merge in progress | `FINISH_FAIL foreign_merge` / `no_merge_head` |
| F7 | unstaged edit to a tracked file | `FINISH_FAIL tree_dirty` |
| F8 | `--precheck` with an operator edit to a non-conflicted tracked file | `FINISH_FAIL tree_dirty`; with only unmerged paths differing: `{"precheck": "ok"}` |
| F9 | failing `pre-commit` hook in `.git/hooks` | `FINISH_FAIL hook_rejected`, hook output on stderr verbatim, no commit, `MERGE_HEAD` still present |
| F10 | clean resolution | exactly two parents `[old HEAD, base_sha]`; stdout JSON; `merge_parent_ok(parents, old_head, base_sha)` true; porcelain empty after |
| F11 | `git merge --abort` after a halt (the ref's abort step run by the test) | worktree, index and `HEAD` equal the pre-merge state |
| F12 | dirty `pyproject.toml` before the merge | the probe reports `tree_clean: false`; `merge_preflight_ok` false; the test asserts nothing was merged (FR-7) |

**collect-conflict-evidence.sh**: E1 content conflict writes exactly `stage1`, `stage2`, `stage3`, `worktree`, `log.txt`, `diff-ours.txt`, `diff-theirs.txt`; E2 modify/delete lists the missing stage; E3 `--max-bytes 64` writes the truncation marker and `truncated: true`; E4 non-empty `--out` gives `EVIDENCE_FAIL out_not_empty` and writes nothing.

**poll-ci-checks.sh --evidence-sha** (stub `gh`): C1 check-runs 2 plus statuses 0 gives `evidence_checks: 2`; C2 both 0 gives 0; C3 a failing `gh api` gives `-1`; C4 an invalid SHA exits 2; in all cases no `gh pr checks` call is made.

**End-to-end** (`test_conflict_e2e.py`):

| Case | Scenario | Assert |
|---|---|---|
| X1 (P1 gate (a), Tier 1, real `uv`, `skipif` uv absent) | Tracked zero-dependency `pyproject.toml` and `uv.lock`. PR branch changes `version`; base changes `requires-python` (separated by at least two unchanged lines, so `pyproject.toml` merges cleanly; the test asserts it is not in the conflict set); both branches commit different hand-written content on the same `uv.lock` line so `uv.lock` conflicts with stages `123`. Run: probe, `conflict_plan` (Tier 1), `conflict_action(hook="wave8a", ordinal=3, entering="clean")` is `resolve_push`, the step 3 to 12 commands as the ref lists them (`sync_started`, merge, precheck, seed, `uv lock`, `uv lock --check`, add, `finish-merge.sh`, guard (b) and (c), `evaluate_sync_decision`, `build_push_triad(push_kind="sync", ...)` appended to a real `RunLog`, `git push origin <target_sha>:<branch>` to the bare origin) | the bare origin's branch tip equals `merge_sha`; parents `[pr_head, base_sha]`; `uv lock --check` passes on the pushed tree; `rebuild_state()`: `push_count == 0`, `sync_push_count == 1`, `conflict_cycles == ["sync-1"]`, `round_counter == 0`, `open_conflict_cycle is None`; the `gh` stub saw no re-trigger call |
| X2 (Tier 1 with a stub `uv`) | Same repositories; a stub `uv` on `PATH` that writes a fixed valid lock and exits 0 | Same assertions; runs where real `uv` is absent |
| X3 (Tier 2, scripted resolution) | A two-file text conflict. The test plays the model: writes the resolved contents and a valid `resolution.md`, runs `collect-conflict-evidence.sh` for each path, `resolution_record_ok` returns `[]`, `git add -- <path>` per path, `finish-merge.sh`, `merge_parent_ok`, `evaluate_sync_decision(tier=2, ...)`, `build_push_triad(push_kind="merge", ...)`, push to the bare origin; then `transition` through `conflicting`, `edits_applied`, `validated`, `pushed`, `replied`, `resolved` and `should_retrigger(0, "merge")` | FSM states in order `S3_FIXING`, `S7_VALIDATING`, `S4_PUSHING`, `S6_REPLYING`, `RESOLVING`, `S5A_RETRIGGER_REVIEW`; `push_count == 1`, `sync_push_count == 0`; commit body lists both files with `kind`, `resolution`, `dropped` and contains no file content; a second variant with a `semantic` kind in the record is rejected before any commit |

Manual verification is never reported as a test pass (section 14 lists it separately).

### 12.5 Run order

`uv run pytest tests/pr_submit tests/unit/test_cli_install.py tests/commands -q`, then `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync`, then `make test` (VG-2 applies: `fsm.py` and `run_log.py` change).

## 13. Implementation order

Dependency-ordered; each step ends green on its own tests before the next starts. Suitable for `/sc:workflow` to turn into a plan (level 3: many files).

| Step | Work | Depends on | Done when |
|---|---|---|---|
| 1 | **Precursor.** `SKILL.md` E2, E5 (rebase sentence only, not the operation check yet), E12 first two rows, E13; `test_static_grep.py:654-661` rewrite | none | `test_static_grep.py` and `test_edge_cases.py` green; `:656`, `:657` unchanged |
| 2 | **Events.** `models.py` +2 members and both docstrings; `run_log.py:111` docstring; `refs/loop-guard.md` count and list; `test_run_log.py:165-169`, `test_codex_reviews.py:441` | none | `len(EventType) == 43`; QA-6 grep clean |
| 3 | **Core module.** `conflicts.py` (section 5), the fixture `merge_tree_conflict.z`, `test_conflicts_core.py` (all but the triad and resume rows); add `conflicts.py` to `CORE_PURE_FILES` | 2 (imports `MonitorState`) | T-N50, T-N41 and the core tests green |
| 4 | **fsm.py.** Flag, `should_retrigger`, `build_push_triad` keywords, the P2 edge, the `:1137` call; `test_skill_parse.py`, `test_autonomy_gates.py`, `test_loop_guard.py` additions; the triad rows of `test_conflicts_core.py` | 3 (`SyncDecision` for the triad test) | existing FSM suites unchanged and green |
| 5 | **ci.py.** `expect_checks` keyword and `expect_checks_after_push`; `test_ci_classify.py` additions | none | `test_ci_classify.py:20-70` unmodified and green |
| 6 | **run_log.py fold.** Section 6.3; `test_run_log.py` new functions | 2 | legacy-log fold test green |
| 7 | **recovery.py.** Key tuple, `resolve_crash_window_plan`; `test_crash_recovery.py` additions; the resume rows of `test_conflicts_core.py` | 3, 6 | existing recovery tests unmodified and green |
| 8 | **Exports.** `__init__.py` | 3, 4 | `from superclaude.pr_submit import conflict_action, should_retrigger` works |
| 9 | **Scripts.** `probe-merge.sh`, `finish-merge.sh`, `collect-conflict-evidence.sh` (mode 100755), `poll-ci-checks.sh --evidence-sha`; `test_conflict_scripts.py` (P, F, E, C cases) | 3 (the tests parse probe output with the core) | all script cases green; `test_skill_forbids_force_push` green over the new files |
| 10 | **Refs.** `refs/conflict-mechanical.md`, `refs/conflict-intent.md` (sections 8.2, 8.3); `refs/state-machine.md` (8.4); `refs/ci-poll.md` (8.5); `refs/loop-guard.md` cycle-id sentence (8.6) | 9 (command lines must match the scripts) | T-N50 green with the state-machine and loop-guard edits |
| 11 | **SKILL and command.** Remaining `SKILL.md` edits (E1, E3, E4, E5 operation check, E6 to E11, E12 last three rows); `commands/pr-submit.md` (8.7) | 10 | one python block; net +15 lines |
| 12 | **Static protocol tests.** `test_conflict_sync_protocol.py`; the two new `test_static_grep.py` functions; `test_pre_pr_checks.py` addition; `test_cli_install.py:248-262` list | 10, 11 | all green |
| 13 | **End-to-end.** `test_conflict_e2e.py` X1 to X3 | 4, 6, 9 | green (X1 skipped only when `uv` is absent; X2 always runs) |
| 14 | **Wrap-up.** CHANGELOG entry (section 15); `make sync-dev`; `make verify-sync`; section 12.5 run order; stage `src/`, `tests/`, `CHANGELOG.md` and `.dev/tasks/` only | all | every gate green |

## 14. Post-release verification follow-ups

Not release blockers (user scope decision). Each is reported as manual verification, never as a test pass.

| # | Follow-up | Gate it closes | Where |
|---|---|---|---|
| V1 | Compare the Wave 0 report with GitHub's own `mergeable` on at least 5 real PRs on `IronbellyOrg/IronClaude`; explain every disagreement | P0 gate (spec section 9) | this repository |
| V2 | One manual live L3 run with a real `uv.lock` conflict: one merge commit pushed fast-forward, no round spent, CI re-polled with `expect_checks` (observe INV-034: no early `clean`), GitHub `mergeable` is `MERGEABLE` afterwards, the merge-method advisory line, the post-push `BLOCKED` line. Also confirm base-added pins are not downgraded by the PR-side seed (OQ-6) | P1 gate (b) | a separate repository that tracks `uv.lock`, under `IronbellyOrg`, never upstream; creating it is the user's decision. `uv.lock` is not un-ignored here |
| V3 | At least 10 real text-conflict runs at `--conflict-max-tier 2`: zero silent behaviour loss found in review; the validator disagreement path; a deliberate semantic conflict halts with nothing pushed; reviewers re-triggered on the merge head (observe the INV-030 race); base-authored findings handled (INV-031); measure the `evidence-validator` disagreement rate (OQ-12) and the `TIER2_MAX_FILES` fit (OQ-9) | P2 gate; then the decision to flip the default to 2 (OQ-1) | IronbellyOrg repositories |
| V4 | `--resume` after killing the session at each crash point of section 4.8 (before the merge, mid-merge, after the commit, between `push_initiated` and the push, after the push) | resume behaviour | sandbox repository |
| V5 | The probe on a host whose git lacks `merge-tree --write-tree` degrades to report-only | NFR-11 in the field | any old-git host |
| V6 | Late re-sync during the CI wait | P3 | #361 |
| V7 | Docs follow-through with `/sc:post-release`: the user guide and the `docs/testing/v5.0.0/user/D07-pr-submit.md` test guide (it cites `SKILL.md` lines that move and the create-path rebase), and any doc stating 41 run-log events | external surface | docs |
| V8 | Pre-existing gap seen while reading `recovery.py:57-80`: after a Branch B re-drive, the re-driven `push_initiated` reuses a key already finalized by `push_aborted_or_not_landed`, so a second crash in the same window is not detected. Not caused or fixed by this release for fix and CI pushes. Conflict cycles are protected by `conflict_resume_plan` rows 4b and 4b', which halt instead of routing into the gap. File a separate issue with `~/.claude/ISSUE-BACKLOG.md` | robustness | new issue |

## 15. CHANGELOG entry and version note

**Version note.** No package version bump: `pyproject.toml:7` is `5.0.0`, and feature PRs add their entries under `## [Unreleased]` (`CHANGELOG.md:5`); the version moves at the next release gate. The command frontmatter `version: "1.0"` (`commands/pr-submit.md:9`) stays: earlier pr-submit features (#337) did not bump it. This is a release of `sc:pr-submit` within the unreleased package version.

**Entry** (insert under `## [Unreleased]`):

```markdown
### sc:pr-submit: merge-conflict detection and resolution (#305)

#### Added (pr-submit conflicts)

- At `--monitor 1` and above, the end of Wave 0 checks for a git operation in progress (halts `foreign_op_in_progress`), reads GitHub's `mergeable`, and only on a conflict runs a read-only local probe (`git merge-tree --write-tree`) that classifies every conflicted path into a tier and prints the plan before any edit.
- Tier 1: a conflicted root `uv.lock` is regenerated with `uv lock` at Wave 8 entry and published as one merge commit of the recorded base tip, pushed fast-forward (never forced). It spends no review round, re-triggers no reviewer, is counted in the new `sync_push_count`, and the CI wait then expects checks on the new head (`expect_checks`), so an empty check list right after the push is no longer read as clean.
- Tier 2 (off by default): text and tree conflicts resolved by stated intent before the first review, with a per-file resolution record, an `evidence-validator` grounding check, full tests, a reviewer re-trigger and one round. Enable with `--conflict-max-tier 2`.
- Tier 3 (submodule, symlink, mode change, protected or migration path, binary, lock or generated file without a rule, more than 8 text files, anything unclassifiable) halts at the end of Wave 0 at L3 with nothing touched, and is reported at L1 and L2.
- New flag `--conflict-max-tier {0,1,2}` (default 1); 0 detects and reports only.
- New core module `superclaude.pr_submit.conflicts`, refs `conflict-mechanical.md` and `conflict-intent.md`, scripts `probe-merge.sh`, `finish-merge.sh` and `collect-conflict-evidence.sh`, and `poll-ci-checks.sh --evidence-sha`.

#### Changed (pr-submit conflicts)

- At `--monitor 1` and above the create path no longer rebases or halts when the branch is behind its base; it reports how many commits behind. `--monitor 0` is unchanged.
- Every push record carries a `kind` (`fix`, `merge`, `sync`, `ci`); `--resume` uses it, so a crashed CI or sync push resumes into the CI wait instead of the review re-trigger path. Old run-logs read as `fix`.
- `push_count` counts fix, CI and Tier 2 merge pushes; Tier 1 sync pushes are in `sync_push_count`. The documented bound is `push_count <= max_rounds + 1`.
- The run-log event enum has 43 members (`sync_started`, `sync_concluded`).
- A PR that is still conflicting at Wave 8 with nothing pushed skips the CI wait (`pr_conflicting`) and ends `terminal_halted` instead of waiting for checks that GitHub will not run; a run that saw a conflict re-reads `mergeable` before claiming clean. Late re-sync during the CI wait is #361.
```

## 16. Residual risks

| # | Risk | Mitigation in this design | Residual |
|---|---|---|---|
| K1 / K14 | A Tier 2 resolution validates but drops behaviour | Default cap 1; one-sentence intents, `behavior_after`, `dropped`; `evidence-validator`; mandatory `make test`; re-review of the merge head; Tier 3 on doubt; revert path | Author and validator share model biases; the P2 live gate (V3) is the real control |
| K3 | `uv lock` needs the network or moves unrelated pins | PR-side seed; `uv lock --check`; lock summary in the commit body; failure halts | A forced re-resolve when the seed fails halts and needs a human |
| K8 | Reviewers never see a Tier 1 merge commit | Tier 1 is mechanical; the commit body is the audit; CI with `expect_checks` is the test signal | A human reviewer is the only reader |
| K11 / INV-032 | A legitimate marker example trips the gate or the repository hook | Gate counts only introduced markers | A side that adds a marker example halts; the `check-merge-conflict` hook can still reject the commit (`sync_commit_failed`) |
| INV-030 | The `C-initial` re-trigger races an in-flight open-time review | Per-reviewer watermarks after the POST and head equality | A missed review ends `TERMINAL_TIMEOUT`; measured in V3 |
| INV-033 | Tier 1 is a no-op in this repository (`uv.lock` ignored) | Hermetic X1 / X2 tests; V2 on another repository | Live Tier 1 evidence waits on V2 |
| V8 | Pre-existing second-crash detection gap after a Branch B re-drive | Conflict cycles fail closed through rows 4b / 4b' (halt, cycle closed, no retry) | Fix and CI pushes still have the gap; tracked as a separate issue |
