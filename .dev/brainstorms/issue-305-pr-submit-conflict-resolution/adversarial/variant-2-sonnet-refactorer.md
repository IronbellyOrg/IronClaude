---
title: "Spec: merge-conflict resolution for sc:pr-submit (issue #305)"
variant: variant-2-sonnet-refactorer
persona: refactorer (technical debt, simplification, minimal-risk transformation)
status: draft-for-adversarial-merge
sources:
  - .dev/brainstorms/issue-305-pr-submit-conflict-resolution/seed-brief.md
  - .dev/brainstorms/issue-305-pr-submit-conflict-resolution/enrichment/codebase-context.md
  - .dev/research/issue-305-conflict-resolution/03-roi-scored-list.md (Items scored above 5)
---

# Spec: merge-conflict resolution for sc:pr-submit (issue #305)

## 1. Summary and decision record

### 1.1 The recommendation in six lines

1. **Mechanism mix:** one new pure-Python module (`pr_submit/conflicts.py`), one new lazy-loaded ref (`refs/conflict-sync.md`), three small scripts (probe, evidence, finish), two new run-log events, one new flag (`--sync-tier`). No new agent, no new template, no new FSM state or edge, and **no change to any push, gate or transition code in `fsm.py`** (the existing `push_parent_ok`, `evaluate_push_decision` and `build_push_triad` stay byte-identical and keep their pinned tests; the only `fsm.py` edit is the `--sync-tier` argument, about 6 lines).
2. **Tiers:** Tier 0 none/behind-only (report, no action); Tier 1 regenerate-only (`uv.lock` in v1); Tier 2 text and tree conflicts resolved by stated intent; Tier 3 anything else (halt, nothing pushed). Classification is a pure function over a probe that never touches the worktree. Tier never decreases inside a cycle.
3. **When:** detect early and read-only (end of Wave 0, L1+), **act late** in a new SKILL-owned **Wave 8a** that runs after the review phase settles and before the CI wait. It follows the existing "CI phase" precedent: SKILL-owned, no FSM edges, no reviewer re-trigger, no thread reply, no round consumed.
4. **Publish:** a single merge commit `M` made by `git merge --no-commit --no-ff <base_sha>` on the PR branch, pushed as a plain fast-forward `git push origin M:<HEAD_BRANCH>`. A new sibling check `merge_parent_ok(parents, pre_push_sha, base_sha)` accepts exactly two parents in exactly that order. `push_parent_ok` is not loosened.
5. **One commit per cycle stays true:** a cycle is either a *fix* cycle (one fix commit) or a *sync* cycle (one merge commit). They never share a push. Sync cycles have their own cap (`SYNC_CAP = 2`) and their own counters; `round_counter`, `max_rounds`, `push_count` and `rereview_request_count` do not move.
6. **Delivery:** four independently shippable phases (P0 detect and report, P1 Tier 1 plus the publish machinery, P2 Tier 2, P3 late re-sync during the CI wait). Ship P0 first: it is read-only and already fixes the "CI polls forever on a conflicted PR" blind spot.

### 1.2 Why this shape (refactorer lens)

The existing skill is already carrying debt: `SKILL.md` is 331 lines with single bullets over 5,000 characters (Wave 6 is one bullet), pinned by dozens of literal-substring assertions. Every design choice below is judged first by *how little of that surface it has to touch*:

| Debt hot spot | Treatment |
|---|---|
| `push_parent_ok` is pinned to "exactly one parent" (`fsm.py:582-600`, `tests/pr_submit/test_pre_pr_checks.py:216-222`) | Add a **sibling**, never a flag or a loosening. The two functions are mutually exclusive by construction (1 parent vs 2 parents), so neither can accept the other's commit. |
| `evaluate_push_decision` is the INV-016 five-predicate conjunction (`fsm.py:173-204`) and predicate 5 means "grounded finding edits" | Do not stretch it. A sibling `evaluate_sync_decision` has its own four predicates. |
| The push triad and recovery have no push-kind field (`fsm.py:236-288`, `recovery.py:57-171`) | Put `kind: "sync"` only on sync records. Absence means fix, so old run-logs and all existing record-shape tests are unchanged. |
| The event enum is closed at 41 and pinned in two tests (`models.py:22-90`, `test_run_log.py:168`, `test_codex_reviews.py:441`) | Add exactly two events (`sync_started`, `sync_concluded`), edit the two pins once, and reuse `terminal_halted` with new `reason` values for every halt. |
| `SKILL.md` must keep exactly one python block (`test_cosmos_protocol.py:36`, `test_codex_reviews.py:688`) | All new procedure lives in the ref. `SKILL.md` grows by a bounded handful of lines (NFR-9). |
| The create path both rebases and halts when behind (`SKILL.md:267` vs `:220-223`, `:315`) | Settle it by clarifying wording only; the pins at `test_static_grep.py:656-661` stay green (Appendix A). |

### 1.3 What "done" looks like (maps to the seed's success criteria)

- L3, mechanical conflicts only (`uv.lock`): one merge commit, pushed fast-forward, CI re-polled on the new head, PR mergeable.
- L3, text conflicts, `--sync-tier 2`: per-file stated intent recorded, evidence-validator confirms, VAL green, one merge commit pushed; unclear intent halts with nothing pushed.
- Semantic or high-risk: halt, nothing pushed, worktree restored.
- L1 reports the plan and proposes; L2 leaves the validated resolution as an uncommitted merge in progress; L0 is byte-identical to today.
- All existing tests pass; new tests pin the tiering, the merge-parent rule and the halts.

## 2. Grounding: facts this spec relies on

Repo facts (re-checked in this session; line numbers are from the current worktree):

| # | Fact | Source |
|---|---|---|
| G1 | The ordinal is a ceiling on one FSM; the core decides, `SKILL.md` sequences and does git/gh I/O | `SKILL.md:36-41` |
| G2 | Wave table; each wave lazy-loads its own ref | `SKILL.md:252-265` |
| G3 | Wave 0 rebases if behind on the create path; on `--pr` it only reports commits behind | `SKILL.md:267` |
| G4 | STOP block and Error Handling row say HALT for "behind base branch on the create path" | `SKILL.md:220-223`, `:315` |
| G5 | The suite pins BOTH the rebase wording and the HALT wording, so the "contradiction" is encoded as intentional | `tests/pr_submit/test_static_grep.py:656-661` |
| G6 | Head binding reads `--json headRefName,headRefOid,isCrossRepository` (substring pinned) | `SKILL.md:268`, `test_static_grep.py:636` |
| G7 | Wave 6: one fix commit per cycle, `git add -- <paths>`, `git commit --only -- <paths>`, `OPERATOR_PENDING` refusal, pre-push head guard (`pr_head_ok`, then `push_parent_ok`, then "The deterministic core DECIDES"), push triad, `git push origin <target_sha>:<target_branch>` | `SKILL.md:274`, pins `test_static_grep.py:664-755` |
| G8 | `push_parent_ok` fails closed on anything but exactly one parent equal to `pre_push_sha` | `fsm.py:593-600` |
| G9 | `build_push_triad` records carry run_id, cycle_id, key, pre_push_sha, target_sha, target_branch, target_remote and nothing about kind | `fsm.py:236-288` |
| G10 | `rebuild_state` adds every `push_completed` to `push_count` and `pushed_commit_shas`; `rereview_requested` is folded by distinct `cycle_id` | `run_log.py:204`, `:238-241` |
| G11 | Recovery matches a dangling `push_initiated` by idempotency key; Branch A resumes at S5a or S5; the recovered record copies a fixed key tuple | `recovery.py:57-80`, `:112-147` |
| G12 | The CI phase is SKILL-owned: no new FSM edges, a CI push skips S5a/S6/RESOLVING and re-polls CI on the new head | `refs/state-machine.md` section 5.2c, `SKILL.md:277` |
| G13 | Wave 8 arms only after Augment `clean`/`REPORT_ONLY`/`HALT_MAX_ROUNDS`/`TERMINAL_AUGMENT_NO_RESPONSE`; a human gate maps to `HALT_HUMAN` unless Augment already halted | `SKILL.md:277` |
| G14 | Nothing in src/, the skill, the command or tests reads `mergeable` or `mergeStateStatus` | enrichment section 3 |
| G15 | T-N50 bans the tokens `git` and `gh` in `fsm.py`, `ci.py`, `state-machine.md` and five more files; a new core file must join the set or stay equally clean | `test_static_grep.py:37-51`, `:132-143` |
| G16 | The force-push scan regex covers every `.md` and `.sh` in the skill folder, so even a prose mention such as "never run git push --force" fails it | `test_static_grep.py:758-776` |
| G17 | `evidence-validator` is read-only (Read, Grep, Glob) and re-reads file:line citations | `agents/evidence-validator.md:1-9` |
| G18 | The command "Will Not" sentence "push any commit besides the cycle's one fix commit" is pinned | `commands/pr-submit.md:85`, `test_static_grep.py:754-755` |
| G19 | Reviewer completion is keyed to the expected head: `_selection` passes `expected` into `_completion_reviews` (verify the equality semantics during implementation) | `classifier.py:446-461` |

Behaviours of git verified empirically in a scratch repo (git 2.47.3) while writing this spec:

- `git merge-tree --write-tree <ours> <theirs>` exits 0 on a clean merge and 1 on conflicts, never touches the index or worktree (it writes only unreachable tree objects), and its full form lists every conflicted path with `<mode> <oid> <stage>`. Stage sets seen: `123` content conflict, `13` modify/delete (deleted by the base side). A binary conflict prints "Cannot merge binary files". `--name-only` drops the stage data, so the probe must use the full form (with `-z`).
- `git commit --only -m x -- <path>` during a merge fails with "cannot do a partial commit during a merge". The merge commit therefore needs its own commit step (plain `git commit -F <file>` after exact-path staging).
- `git diff --numstat <merge-base> <side> -- <path>` prints `-  -  <path>` for a binary file.

External facts (not verifiable offline; the spec uses them as hints, never as gates): GitHub computes `mergeable` asynchronously and can return UNKNOWN; `pull_request` workflows do not start while a PR has a merge conflict; `gh pr view --json` exposes `mergeable`, `mergeStateStatus` and `baseRefName` (probe the field list with `gh pr view --help`, the same pattern as the CI-wait preflight at `SKILL.md:225-230`).

## 3. Mechanism mix: what to build, what to reject

Selection rule: a piece earns its place only if (a) it carries a safety property that prose cannot enforce, or (b) it removes work that would otherwise be repeated per run, and (c) its test and maintenance cost is lower than the failure it prevents. ROI ids are from `03-roi-scored-list.md` (score above 5 only).

### 3.1 Adopt

| Piece | What it is | Why it earns its place | Cost |
|---|---|---|---|
| **A1. `pr_submit/conflicts.py`** (pure core) | `classify_conflicts`, `merge_parent_ok`, `evaluate_sync_decision`, `sync_fail_state`, `build_sync_triad`, `resolution_record_ok`, `mergeability_hint`, constants `SYNC_CAP`, `TIER2_MAX_FILES`, recipe and path tables | Everything that gates a push or picks a tier is deterministic, exhaustively unit-testable and fail-closed. Mirrors `ci.py` (a standalone pure module, no git/gh tokens, in the T-N50 set). Keeps `fsm.py` untouched. | About 250 lines, one test file. |
| **A2. `refs/conflict-sync.md`** (one ref, lazy) | The procedure for Wave 0 reporting and Wave 8a: commands, tier procedures, record format, HALT message text, resume rules | `SKILL.md` is already over-dense; a ref loads only when a conflict is actually in play, so Tier 0 pays nothing. Host of the resolution-record format and HALT text (see rejection R2). | About 150 lines; static-grep tests. |
| **A3. `scripts/probe-merge.sh`** | Read-only: fetch `origin <base>`, record `base_sha`, detect a foreign git operation and a dirty index, run `git merge-tree --write-tree -z`, add per-path binary flag, optionally append GitHub `mergeable`/`mergeStateStatus`; emits **one JSON line** (same contract as `poll-ci-checks.sh`). Takes `--repo`. | Keeps git I/O out of the core and out of `SKILL.md` prose; one deterministic call replaces 6 to 8 ad hoc calls; R-26, R-43, J-16, J-17, S-38 become data fields. It is the only way Tier 0 to Tier 3 classification can run without mutating the worktree. | About 90 lines of bash; real-repo tests. |
| **A4. `scripts/collect-conflict-evidence.sh`** (Tier 2 only) | For one path: writes stage 1/2/3 blobs, `git log --left-right --merge -- <path>`, and both merge-base diffs into `<output-dir>/sync/<cycle>/<n>/`, output bounded | Implements S-12, S-13, S-14, R-112, R-181 as one bounded call. Also solves a hard constraint: `evidence-validator` can only Read/Grep/Glob files, so the stage blobs must exist as files. Tier 0 and Tier 1 never run it, so cost layers with complexity. | About 60 lines. |
| **A5. `scripts/finish-merge.sh`** | The commit gate: verifies the merge is ours (`MERGE_HEAD` equals the recorded `base_sha`), no unmerged paths, no conflict markers introduced, staged paths are a subset of `(files changed by base since merge-base) union (resolved paths)`, then runs `git commit -F <msg>` (hooks on) and prints `{merge_sha, parents}` | Concentrates every pre-commit safety check in one place that real-repo tests can exercise; R-11, J-56, J-60, J-61, J-63 live here. | About 90 lines. |
| **A6. Inline git/uv calls in the ref** | `git merge --no-commit --no-ff`, `git add -- <path>`, `git rm -- <path>`, `uv lock`, `uv lock --check`, `git merge --abort`, `git rev-list --parents -n 1`, `git push origin <sha>:<branch>` | These steps are one-liners whose next step depends on the previous output or on judgment; wrapping them in a script adds nothing. | None beyond the ref text. |
| **A7. Reuse `evidence-validator`** | One read-only spawn per Tier 2 cycle, over `resolution.md` plus the evidence directory | Independent check on the highest-risk automated step (model-authored resolution pushed at L3), at zero new primitives. Same pattern as Wave 3. | One spawn per Tier 2 cycle. |
| **A8. Two run-log events** | `sync_started` (write-ahead, before the merge) and `sync_concluded` (outcome, record path, merge sha) | Resume must tell "our merge in progress" from "the operator's" (J-17, S-05); a bracket is the minimum that does so. Halts reuse `terminal_halted` with a `reason`. | Edit two pinned counts (41 to 43). |
| **A9. `kind: "sync"` marker + 2 small edits** | `run_log.py`: a `push_completed` with `kind: "sync"` counts into `sync_push_count`, not `push_count`, and `sync_started` events fold into a `sync_cycles` list. `recovery.py`: copy `kind` and `base_sha` into the recovered record; Branch A of a sync resumes at `S2_CLASSIFY`, never S5 | Closes the recorded gap that recovery cannot tell a merge push from a fix push (enrichment section 2), and keeps the `push_count <= max_rounds` contract true. | About 15 lines plus tests. |
| **A10. Flag `--sync-tier {0,1,2}`** (default 1 for the first release) | Ceiling on the tier the skill may act on; 0 = detect and report only | Gives a two-stage rollout without a code change: ship Tier 2 dark, flip the default after evidence. Needs `SkillArgs`, `parse_args` and the command table (`fsm.py:73-99` area) | About 10 lines plus 3 tests. |
| **A11. Edits to `SKILL.md`, command, `state-machine.md`** | Wave table row, one Wave 8a bullet, one Wave 0 sentence, output-contract rows, Will Not bullet, Error Handling rows, section 5.2d in `state-machine.md` (no git tokens) | Required for the skill to be coherent; each edit is additive and keeps all pins. | NFR-9 budget. |

### 3.2 Reject

| # | Rejected piece | Reason | Revisit trigger |
|---|---|---|---|
| R1 | **New agent** (a `conflict-resolver`) | The skill's rule is that the main session performs every side effect (`SKILL.md:82-84`); a resolver agent would need Bash and write access, contradicting that. A read-only variant duplicates `evidence-validator`. A new agent also adds an installed primitive, a dual-surface lookup test and a prompt to maintain. R-173 and J-39 (ROI 6 and 8) say the attended session does the judgment. | Tier 2 resolutions routinely exceed one session's context. |
| R2 | **New template file** for the resolution record or HALT text | No second consumer exists; HALT text already lives inline in `SKILL.md` and is pinned verbatim there (G7); `src/superclaude/templates/` has no matching family. A template is one more installed path to test and sync. | A second skill (for example a standalone `/sc:merge`) needs the same record. |
| R3 | **New FSM states or edges** (`S_SYNC`, `sync_conflict` event) | `transition()` silently ignores unknown edges (`fsm.py:801-802`) and `state-machine.md` claims to be the complete enumeration, so a new state costs `models.py`, `transition()`, the doc and the row-by-row tests. The CI phase proves a SKILL-owned phase works (G12). | A conflict outcome must change a later FSM decision, which none does today. |
| R4 | **Loosening `push_parent_ok`** (accept two parents) or adding a `kind` parameter | It exists so a fast-forward push cannot publish extra local commits (`fsm.py:585-587`); a looser check weakens the fix path for the sake of the sync path and breaks the pinned `merge` test id. A sibling function cannot weaken the old one. | Never. |
| R5 | **Reusing `evaluate_push_decision`** with `applied_edits := files changed` | Predicate 5 means "grounded finding edits" (INV-016); overloading it makes the audit record lie. | Never. |
| R6 | **Dispatch to `/sc:troubleshoot`** | Troubleshoot diagnoses defects from a finding seed (`refs/troubleshoot-dispatch.md`); a merge conflict is not a defect to diagnose, and the seed shape (issue, scope, type) adds ceremony without evidence. | None. |
| R7 | **mergiraf**, `suggest-pr-split`, `meta-route`, `categorize-conflicts` as scripts, `conflict-status`, sbse recombine (R-64 to R-73, R-37 to R-39, R-23 to R-25, R-40 to R-50, R-101) | New external dependency (forbidden by the seed), or routing frameworks that duplicate a 40-line pure function; scored 1 to 6 by the research. | A measured Tier 2 failure rate above an agreed bar. |
| R8 | **`gh pr update-branch`** for behind-only | Server-side merge produces a head the local checkout does not have and skips local VAL; it cannot resolve conflicts anyway. | A maintainer wants a no-checkout path for Tier 0 only. |
| R9 | **A user-override channel** (R-19, R-20) | The skill is attended but has no override prompt; any "override" is a re-run with a different flag. Adding a mid-run override creates an unreviewed authority path. | None. |
| R10 | **Blanket side-taking and hard resets** (R-13, R-14, R-15) as options | Forbidden outright (FR-21). | Never. |
| R11 | **Global git config changes** (`merge.conflictStyle`, `rerere`) | Seed constraint. Use per-invocation `-c merge.conflictStyle=zdiff3` and `-c rerere.enabled=false` (R-128 forbids silently replaying a historical resolution). | None. |
| R12 | **Rebasing the PR branch** | Rewrites a published head and needs a force-push. | Never. |
| R13 | **Arbitrary conflict-count abort thresholds** (R-33 to R-36) | Scored 1 to 3. A single cost guard `TIER2_MAX_FILES` is kept instead, as a tunable constant. | After 10 real runs. |
| R14 | **Whitespace check `git diff --check --cached`** (R-161, ROI 6) | VG-3 and VG-4 already cover format; inherited whitespace in merged base content would trigger unrelated cleanup, which R-169 forbids. | None. |

### 3.3 Net effect on the primitive inventory

| Surface | Before | After |
|---|---|---|
| Core modules in `pr_submit/` | 11 files | +1 (`conflicts.py`) |
| Refs | 11 | +1 (`conflict-sync.md`) |
| Scripts | 4 | +3 |
| Agents | no change | 0 new |
| Templates | no change | 0 new |
| Commands | `pr-submit.md` | one flag row, one Will Not clause |
| `fsm.py` | as is | push, gate and transition code: **0 lines**; argument parser: about 6 lines |
| `models.py` | 41 events | 43 events |
| FSM states | 23 | 23 |
| Python blocks in `SKILL.md` | 1 | 1 |

## 4. Tier model: process cost grows only with conflict complexity

### 4.1 Cost ladder

| Tier | Meaning | Calls | Model reasoning | Agent spawn | Pushes |
|---|---|---|---|---|---|
| 0 | No conflict (clean, or behind only) | `fetch`, `merge-tree` (inside `probe-merge.sh`) | none | none | none (report only) |
| 1 | Mechanical: every conflicted path is a regenerate-from-source file with a registered recipe | Tier 0 calls + `merge`, `uv lock`, `uv lock --check`, `add`, `finish-merge.sh`, VAL | none | none | one merge commit |
| 2 | Text or tree conflicts resolved by stated intent | Tier 1 calls + one `collect-conflict-evidence.sh` per file | one intent statement pair per file | one `evidence-validator` | one merge commit |
| 3 | Semantic or high-risk, or anything unclassifiable | Tier 0 calls; abort if a merge was started | none after detection | none | none, halt |

### 4.2 Classification rule (pure, `classify_conflicts`)

Input is the probe's `conflicts` array: per path `{path, stages, modes{base,ours,theirs}, binary}`, where `stages` is the string of index stages present (`"123"` both sides modified, `"13"` deleted by the base side and modified here, `"12"` the reverse, `"23"` added on both sides) and `ours` is the PR branch. Each path gets exactly one class from the **first matching rule** below; the tier is the maximum over paths. Any shape no rule recognises is `halt:unknown_shape` (fail closed).

| Order | Rule | Class | Source |
|---|---|---|---|
| 1 | any side mode `160000` | `halt:submodule` | R-43, R-56 |
| 2 | any side mode `120000` | `halt:symlink` | fail closed |
| 3 | modes differ between ours and theirs (mode-only or mode-plus-content) | `halt:mode_change` | fail closed |
| 4 | path matches the protected globs (`.github/workflows/**`, `.github/actions/**`, `.claude/settings.json`, `.claude/settings.local.json`) | `halt:protected` | blast radius of a bad CI or permissions file |
| 5 | path matches a migration pattern (`migrations/`, `alembic/versions/`, `db/migrate/`) | `halt:migration` | R-54, S-53 |
| 6 | `binary` is true | `halt:binary` | R-57 |
| 7 | basename is in the recipe table (`uv.lock` -> recipe `uv-lock`) and `stages == "123"` | `regen:<recipe>` | R-58, R-189, J-48 |
| 8 | basename is a known lockfile name without a recipe (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, `Pipfile.lock`, `flake.lock`) or ends in `.lock` | `halt:lockfile_no_recipe` | R-59, J-48 (use only the manager the lockfile names) |
| 9 | path is under `generated/`, `dist/`, `build/` or matches `*.generated.*` and has no recipe | `halt:generated_no_recipe` | R-59 |
| 10 | `stages == "123"` | `text:content` | R-149 |
| 11 | `stages in {"13","12"}` | `text:modify_delete` | R-154, S-39 |
| 12 | `stages == "23"` | `text:add_add` | S-40 |
| 13 | anything else | `halt:unknown_shape` | fail closed |

Tier assignment, applied after the per-path classes:

| Condition | Tier |
|---|---|
| probe reports `clean` (no conflicts) | 0 |
| at least one `halt:*` class | 3 |
| number of `text:*` paths is greater than `TIER2_MAX_FILES` (default 8) | 3, reason `too_many_files` |
| at least one `text:*` class (regen paths may accompany them) | 2 |
| all paths are `regen:*` | 1 |

Notes that make the table safe and small:

- **No tree conflict is Tier 1.** A modify/delete or add/add only surfaces when both sides changed the path, so there is no purely mechanical answer (R-154 says "determine which intent supersedes"). They are Tier 2 with a mandatory kind label and a dropped-behaviour line. This rejects the idea of an "obvious-answer tree conflict" tier; revisit only if field logs show a repeating mechanical shape.
- **Recipes are data.** The core holds `REGEN_RECIPES = {"uv.lock": "uv-lock"}`; the ref maps the recipe id to its command. Adding a recipe is a table row plus a ref row, not new code paths.
- **Manifest first (R-58).** When `pyproject.toml` also conflicts it is `text:content` (Tier 2); `uv lock` runs only after it is resolved and staged.
- **Cap by flag.** If `tier > sync_tier_cap` the plan's action is `report` with reason `tier_above_cap`; the plan still prints (FR-4).

### 4.3 Exit criteria per tier

| Tier | Exit to "commit" requires all of | Exit to "halt" when |
|---|---|---|
| 0 | n/a. Report "N commits behind, no conflicts" and continue Wave 8. | n/a |
| 1 | (a) the merge started with `MERGE_HEAD == base_sha`; (b) `uv lock` exit 0 and `uv lock --check` exit 0 after the manifest is final; (c) `finish-merge.sh` passes every guard; (d) VAL green | recipe command fails, `--check` fails, any guard fails, VAL red after the one retry |
| 2 | everything in Tier 1 minus the recipe, plus: (e) for every `text:*` file a record entry with `kind`, one-sentence `ours_intent`, one-sentence `theirs_intent`, `resolution`, `behavior_after` and `dropped` (R-18, R-156, S-29); (f) `resolution_record_ok(record)` returns no problems; (g) `evidence-validator` confirms every entry; (h) no third behaviour (S-26) | an intent cannot be stated in one sentence (R-18), the kind is `semantic` by the high-suspicion checklist (R-180, R-251), the validator marks an entry unsupported after one revision pass, a file is unreadable (R-84), any Tier 1 halt condition |
| 3 | n/a. Print the HALT message (FR-10); nothing pushed. | n/a |

**Escalation is monotone.** A cycle that starts as Tier 1 or 2 may escalate to Tier 3 at any point; it never de-escalates, and it never retries a halted cycle in the same run. The cap on retries inside a tier is one revision pass (validator disagreement) and one VAL retry, matching the existing "a validation retry does not tick the round counter" rule (`SKILL.md:291`).

### 4.4 High-suspicion checklist for Tier 2 (R-180, R-251, S-26)

Before resolving a `text:*` file the model must check, using the evidence bundle: does either side change a function signature, a type or schema, a dependency, a constant or env var, or a public API, while the other side adds or changes callers (R-180)? Does one side remove an old API or column while consumers remain (R-251)? A yes on any item makes the file `kind: semantic` and the cycle Tier 3. The model may use `git grep` for the symbol (R-181) as a read-only check.

## 5. Where it runs in the sc:pr-submit flow

### 5.1 Placement decision: detect early, act late

Three placements were weighed.

| Option | Fit | Verdict |
|---|---|---|
| **A. Act before Wave 1** (resolve first, then review) | Reviewers see a conflict-free head. But a push moves the head, so reviewers must be re-triggered and the first wait run with the S5 attribution parameters (`pushed_sha`, per-reviewer watermarks), because completion is keyed to the expected head (G19). That drags S5a machinery, `rereview_requested` accounting (INV-R1 `<= max_rounds`) and the run-log baseline ordering into the sync design. The run-log is also not initialised until Wave 1 (`SKILL.md:269`). | Reject: highest coupling. |
| **B. Act after the review phase, before the CI wait** (new Wave 8a) | One call site. Reuses the CI-phase precedent verbatim: SKILL-owned, no FSM edges, no re-trigger, no thread reply, CI re-polled on the new head (G12). Sees the *latest* base, so base drift during a long review is covered by construction. CI does not start on a conflicted PR (external), so resolving just before the CI wait is exactly where the wait would otherwise stall. | **Adopt.** |
| **C. Act only during the CI wait** (when CI reports nothing) | Latest information, but wastes the first `--timeout` window before noticing. | Keep only as the P3 re-sync trigger. |

Cost of choosing B: a Tier 3 halt arrives after the review phase has spent its rounds. That is acceptable because review fixes are already pushed and the halt reports the review outcome alongside (same shape as a CI human-gate after `HALT_MAX_ROUNDS`, `SKILL.md:277`). To avoid learning about a Tier 3 conflict only at the end, detection runs **early and read-only** at the end of Wave 0 (L1+), so the operator sees the tier and the plan before any review round is spent.

### 5.2 Wave table additions

```text
Wave 0 (end, L1+):  detect + report the conflict plan        <- loads refs/conflict-sync.md ONLY if the probe reports conflicts
Wave 8a (L1+):      re-probe, then act per ordinal            <- loads refs/conflict-sync.md
                    runs after the review phase settles, before the CI poll loop is entered
```

`refs/conflict-sync.md` is never loaded when the probe is Tier 0, so a normal PR pays for two read-only calls and nothing else.

### 5.3 Probe contract (`scripts/probe-merge.sh --repo "$REPO" --pr <N> --base <base> --head-branch <HEAD_BRANCH>`)

One JSON line on stdout; a non-zero exit is a prerequisite failure (reported, never retried as "polling"), the same convention as `SKILL.md:56-58`:

```json
{"ok": true, "merge_tree_supported": true,
 "base_ref": "origin/main", "base_sha": "<40hex>", "head_sha": "<40hex>", "merge_base": "<40hex>",
 "behind": 3, "ahead": 2,
 "foreign_op": null, "index_clean": true,
 "clean": false,
 "conflicts": [{"path": "uv.lock", "stages": "123",
                "modes": {"base": "100644", "ours": "100644", "theirs": "100644"}, "binary": false}],
 "github": {"mergeable": "CONFLICTING", "merge_state": "DIRTY"}}
```

Rules:

- The script runs `git fetch origin <base>` (origin only; never another remote) and takes `base_sha` from `git rev-parse origin/<base>` after the fetch. `base` is the PR's own `baseRefName` (read with `gh pr view <N> --repo "$REPO" --json baseRefName,mergeable,mergeStateStatus`), falling back to the resolved `--base`.
- `merge_tree_supported` is set by a capability probe (`git merge-tree --write-tree` against `HEAD HEAD`), never by parsing a version number (`SKILL.md:225-230` pattern). If false, the probe returns `ok: true, clean: null` and the skill degrades to report-only using the GitHub fields.
- `foreign_op` is non-null when any of `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `sequencer` exists under `git rev-parse --git-path` (worktree-aware, J-16, J-17, S-05).
- `index_clean` is `git diff --cached --quiet`. Unstaged or untracked operator files are tolerated (git itself refuses a merge that would overwrite them); a staged file is not, because a plain merge commit would include it.
- `github.*` are advisory: `null` on any read failure (never a halt). Local `merge-tree` is the source of truth; a disagreement is reported as `github_disagrees` and changes nothing.
- The script performs no worktree or index mutation. It may leave unreachable tree objects (documented, harmless).

### 5.4 Behaviour by ordinal

| Ordinal | End of Wave 0 | Wave 8a |
|---|---|---|
| **L0** | Nothing. The FSM never leaves `S0_IDLE`; the L0 sentence and AC-1 stay byte-identical (`test_static_grep.py:650-653`). | Never reached. |
| **L1** | Probe, classify, print the plan (R-51): tier, per-path class and reason, what would run. No merge, no edits. | Re-probe; print the plan again only if the tier or paths changed. Proposes "resolve these? y/n" for Tier 1 and 2 (same shape as the `PROPOSED` state) and applies nothing. |
| **L2** | Same as L1. | Tier 1 and 2: perform the local resolution through VAL, then **stop with the merge in progress and uncommitted** (no commit, no push, no reply), report `status: halt_before_push`. Tier 3: print the HALT message; the preflight classification means no merge was started, so nothing needs undoing. |
| **L3** | Same as L1. | Tier 1 and 2 within `sync_tier_cap`: full cycle through commit and push (section 6), then continue to the CI wait on the new head. Tier 3 or above cap: HALT, nothing pushed. |

Why L2 ends the run instead of continuing: a worktree mid-merge breaks the later fix cycle (the fix commit uses `git commit --only`, which git refuses during a merge, and `OPERATOR_PENDING` would flag every merged file). Wave 8a is the last mutating phase, so ending there loses nothing. The merge in progress is *ours*, recorded by `sync_started`, so a re-run recognises it (FR-17).

### 5.5 Wave 8a gate on the Wave 8 arming outcomes

| Review outcome entering Wave 8 | Wave 8a action |
|---|---|
| Augment `clean` / `REPORT_ONLY` (merged clean or findings reported) | Acts per the table above, **regardless of `round_counter`** (it consumes no round). |
| `HALT_MAX_ROUNDS` / `TERMINAL_AUGMENT_NO_RESPONSE` (wait-only paths, `ci_wait_autofix` false) | Report-only: print the plan and the reason "wait-only path". No merge, no push. (Conservative; see OQ-4.) |
| `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED` / L0 | Wave 8 is not armed, so Wave 8a does not run. The early Wave 0 report already informed the operator. |

On a Tier 3 halt after an ordinary review outcome, the FSM takes the existing human-gate route to `HALT_HUMAN`; after `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE` the retained terminal status is preserved and the sync halt is reported alongside it, exactly as for a CI human-gate (`SKILL.md:277`). No new FSM edge is needed.

### 5.6 Interaction with rounds, caps and reviewers

| Item | Behaviour |
|---|---|
| `round_counter` / `max_rounds` | Untouched. The counter ticks only on `S5 -> S2` (`state-machine.md` section 5.1 and INV-001); Wave 8a never enters S5. |
| `push_count` (contract: at most `max_rounds`; INV-R2: `push_count <= max_rounds + 1`) | Untouched: a sync `push_completed` folds into the new `sync_push_count`. |
| `SYNC_CAP` | 2 sync cycles per run (initial plus one P3 re-sync). Counted from `sync_started` events via `rebuild_state()["sync_cycles"]`. The cap is evaluated by `evaluate_sync_decision`. |
| Reviewer re-trigger | None. A sync push does not call `retrigger-review.sh` and writes no `rereview_requested`. `rereview_request_count` is therefore unchanged. This mirrors the CI-phase push (`SKILL.md:277`: "do not call `retrigger-review.sh`, reply, or resolve"). Consequence: reviewers never see `M`; the resolution record in the merge commit body is the human-visible audit (FR-11). |
| Thread reply / resolve | None (there are no threads in a sync cycle). |
| Impact warning (`sc:impact-protocol`) | Not invoked; the advisory VG-1 test suggestion in VAL already covers changed areas. |
| Late conflict while polling CI (P3) | If the CI poll payload carries `merge_state` CONFLICTING, or the CI wait is stuck at `polling` with no checks and GitHub reports CONFLICTING, run Wave 8a once more (subject to `SYNC_CAP`, Tier 0 and 1 only: a late Tier 2 halts with reason `late_conflict`, because no reviewer would see the new resolution). |

### 5.7 Run-log events and write-ahead order

Exactly two new `EventType` members (41 to 43):

| Event | Written | Payload |
|---|---|---|
| `sync_started` | before the merge command (write-ahead) | `run_id, cycle_id, base_ref, base_sha, pre_push_sha, tier, sync_tier_cap, paths` |
| `sync_concluded` | when the cycle ends | `cycle_id, outcome` in `{pushed, left_in_progress, aborted, halted, report_only}`, `merge_sha` or null, `record_path`, `dropped` (list of strings) |

Order for an L3 cycle: `sync_started` -> (merge, resolve, VAL, commit) -> `push_decision{kind: sync}` -> `push_initiated{kind: sync}` (fsynced before the push) -> push -> `push_completed{kind: sync}` -> `sync_concluded{pushed}`. Halts append `sync_concluded{halted}` then `terminal_halted{reason}` with these new reasons: `sync_tier3`, `sync_dirty_index`, `sync_foreign_operation`, `sync_merge_failed`, `sync_marker_left`, `sync_unmerged_left`, `sync_staged_unexpected`, `sync_commit_failed`, `sync_head_mismatch`, `sync_range_mismatch`, `sync_base_moved`, `sync_cap`, `late_conflict`. No other event type is added (reasons are free-text fields of an existing event, like `pr_head_mismatch`).

### 5.8 `--resume` crash recovery

Recovery has three mid-cycle states, each decidable from the run-log plus read-only git state.

| Observed on resume | Meaning | Action |
|---|---|---|
| `sync_started` with no `sync_concluded`, no `push_initiated` for the cycle, `MERGE_HEAD` exists and equals the recorded `base_sha` | Our merge was interrupted before commit | Continue the cycle: re-read the probe, resume Tier 2 at the first path still unmerged (J-40 one file at a time), then finish. |
| `MERGE_HEAD` exists but no matching `sync_started` (or a different sha) | Someone else's operation | HALT `sync_foreign_operation`. Never touch it (J-17). |
| `sync_started`, no `MERGE_HEAD`, local `HEAD == pre_push_sha` | The merge never started or was aborted | Restart the cycle; nothing to undo. |
| `sync_started`, local `HEAD` is a 2-parent commit `[pre_push_sha, base_sha]`, no `push_initiated` | Crash between commit and push | Re-run the pre-push guard, then the triad and push. |
| Dangling `push_initiated` with `kind: "sync"` | The existing three-way crash window | `resolve_crash_window` behaves as today, except Branch A of a sync returns `S2_CLASSIFY` (never S5, so no round tick, no re-trigger); Branch B re-drives the push of the recorded `target_sha` with the sync guard using the record's own `base_sha`; Branch C halts as today. |

The recovered `push_completed` copies `kind` and `base_sha` (a two-key extension of the fixed tuple at `recovery.py`, `resolve_crash_window`), so the `rebuild_state` fold counts it as a sync push.

## 6. Publishing the resolution without a force-push

### 6.1 Why a merge commit, and why it is safe

Integrating the base into an already-published PR head without rewriting history means exactly one thing: a merge commit on the PR branch. Its parents are `[pr_head, base_tip]`, so `pr_head` is an ancestor of `M` and `git push origin M:<HEAD_BRANCH>` is a plain fast-forward. Nothing is rewritten; rollback is a normal revert commit (`git revert -m 1 M`, recorded in the ref for the operator).

The reason `push_parent_ok` forbids extra commits is that a fast-forward publishes every commit between the PR head and the target (`fsm.py:585-587`). For `M` that risk is bounded by construction: the only commits `M` adds to the PR branch besides itself are ancestors of `base_sha`, which is a commit that was just fetched from `origin/<base>` and therefore already exists on the remote. The exact parent rule below pins that.

### 6.2 Exact parent rule: `merge_parent_ok`

```text
merge_parent_ok(target_parents, pre_push_sha, base_sha) -> bool
  true iff ALL hold:
    target_parents is a list with exactly 2 entries
    pre_push_sha and base_sha are str and each matches [0-9a-fA-F]{40} in full
    both parents are str and each matches [0-9a-fA-F]{40} in full   (no whitespace, no short ids)
    target_parents[0].lower() == pre_push_sha.lower()               (first parent is the PR head)
    target_parents[1].lower() == base_sha.lower()                   (second parent is the recorded base tip)
    pre_push_sha.lower() != base_sha.lower()
  anything else (None, wrong type, 0/1/3 parents, swapped order, bad id) -> false
```

Properties the tests must assert: `push_parent_ok` returns false for every input `merge_parent_ok` accepts, and `merge_parent_ok` returns false for every input `push_parent_ok` accepts (disjoint by parent count), so a mis-routed commit can never pass the other check. `base_sha` is the value recorded in `sync_started`, never re-read from a ref.

### 6.3 The sync decision: `evaluate_sync_decision`

A sibling of `evaluate_push_decision` (which stays untouched), returning a `SyncDecision` dataclass with one flag per predicate, evaluated immediately before the push:

| Predicate | Holds when |
|---|---|
| `s1_ordinal` | `monitor_ordinal >= 3` |
| `s2_validated` | `validation_status == "validated"` |
| `s3_tier_allowed` | `tier in (1, 2)` and `tier <= sync_tier_cap` and no halt reason is set |
| `s4_under_cap` | `prior_sync_cycles < SYNC_CAP` (count of earlier `sync_started`, excluding this cycle) |

`authorized` is the conjunction. `sync_fail_state(decision)` maps a block: `s3` false -> `HALT_HUMAN`; `s4` false -> report-only (`sync_cap`); `s1` or `s2` false -> report-only. There is deliberately no `applied_edits` predicate; the audit record names the four predicates (`p1_ordinal`, `p2_validated`, `p3_tier_allowed`, `p4_under_cap`) and carries `kind: "sync"`.

### 6.4 Procedure, step by step (L3; L2 stops after step 8, L1 never starts)

| Step | Action (exact) | Fail behaviour |
|---|---|---|
| 1 | Re-read the PR head (`gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository`) and require `pr_head_ok(<local branch>, <local HEAD sha>, headRefName, headRefOid, isCrossRepository)` (local `HEAD` is the live PR head), `headRefName == HEAD_BRANCH`, and local `HEAD == pre_push_sha` (the stored value), so an unpublished local commit can never become the first parent of `M`. Also require `HEAD_BRANCH != <base>` (J-26) and that the checkout is the current worktree (J-91). | `terminal_halted` reason `sync_head_mismatch`; nothing started. |
| 2 | Run `probe-merge.sh` again (fresh `base_sha`, fresh classification). Require `foreign_op == null` and `index_clean == true` (J-17, J-18). Plan = `classify_conflicts(...)`. | `sync_foreign_operation` or `sync_dirty_index`; message says commit or discard your own staged files, never stash (J-20). |
| 3 | Append `sync_started{...}` (write-ahead). | n/a |
| 4 | `git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>` (by SHA, so the target cannot move; per-invocation `-c`, no stored config; `rerere` off so no historical resolution is replayed, R-128; no `--no-verify`). Exit 0 with `MERGE_HEAD` present means a clean merge (possible if the base changed again); exit 1 with unmerged paths is the expected conflict; exit 1 with no `MERGE_HEAD` means git refused (local changes would be overwritten). | Refusal: `sync_merge_failed`, nothing started, message lists git's own file list and says to commit or discard those files yourself. |
| 5 | Resolve per tier. Tier 1: the recipe of 6.5 (seed the one named lock file from the PR side, `uv lock`, `uv lock --check`, `git add -- uv.lock`). Tier 2: one file at a time, `git add -- <path>` (or `git rm -- <path>` for a deletion) as each is finished (J-40, J-56). Never `git add -A`, `git add .`, `--ours .`, `--theirs .`, `-X ours`, `-X theirs`, `-s ours` (FR-21). | Any halt condition: if the resolution is not complete, `git merge --abort` (allowed only because `MERGE_HEAD == base_sha` is verified) and `sync_concluded{aborted}`; the worktree is restored. |
| 6 | Tier 2 only: write `resolution.md` (format in 6.6), run `resolution_record_ok`, then spawn `evidence-validator` once over `resolution.md` and the evidence directory. One revision pass allowed. | Unsupported after the revision pass: abort, Tier 3 `sync_tier3`. |
| 7 | VAL (section 6.7). | Red after the single retry: abort or leave per 6.8, `terminal_halted` via the existing `VALIDATION_FAIL` route. |
| 8 | **L2 stops here:** `sync_concluded{left_in_progress}`, report `halt_before_push`, and tell the operator: "The merge of `origin/<base>`@<base_sha> is resolved and validated but not committed. Review it, then run `git commit` yourself and push; or `git merge --abort`." | n/a |
| 9 | `scripts/finish-merge.sh` with the recorded `base_sha`, the resolved-paths list and the commit-message file (6.6). It verifies: `MERGE_HEAD == base_sha`; `git diff --name-only --diff-filter=U` empty; no conflict markers **introduced** in resolved paths (count of marker lines in the result must not exceed the count in the stage-1 blob, so legitimate documentation examples pass; R-11); staged paths are a subset of (files changed on the base side since the merge-base) union (resolved paths); then `git commit -F <msg>` with hooks on. It prints `{merge_sha, parents}`. | Hook rejection: output reported verbatim (J-61), no amend (J-63: the merge commit does not exist yet), `sync_commit_failed`, merge left in progress with resolution intact. Any other guard failure: `sync_marker_left`, `sync_unmerged_left` or `sync_staged_unexpected`. |
| 10 | Set `target_sha := merge_sha`. **Pre-push head guard, in this order:** (a) re-read the PR head and require `pr_head_ok(<local branch>, pre_push_sha, ...)` and `headRefName == HEAD_BRANCH` (compare the stored `pre_push_sha`, never local HEAD); (b) read `git rev-list --parents -n 1 <target_sha>`, drop the first id, require `merge_parent_ok(<parents>, pre_push_sha, base_sha)`; (c) require `git merge-base --is-ancestor <base_sha> origin/<base>` after a fresh `git fetch origin <base>` (the second parent is still on the real base). | (a) `sync_head_mismatch`; (b) `sync_range_mismatch`; (c) `sync_base_moved`. All: nothing pushed, no push record, the local merge commit named in the message so the operator can drop or push it. |
| 11 | Core DECIDES: `evaluate_sync_decision`, then `build_sync_triad` writes `push_decision` -> `push_initiated` (fsynced before the push) -> `push_completed`, keyed on the existing pre-push key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>` (`cycle_id` is a fresh `sync-<n>` id; the key format is reused as is). | Blocked decision: `sync_fail_state`, nothing pushed. |
| 12 | `git push origin <target_sha>:<HEAD_BRANCH>` (never an upstream or parent remote, never the default or protected branch, never forced). Then `pre_push_sha := target_sha`. | git rejecting a non-fast-forward is the backstop if the PR head moved after the guard, exactly as for fix pushes (`SKILL.md:305`). |
| 13 | Append `sync_concluded{pushed, merge_sha}`. Re-enter Wave 8 with `wait_sha = target_sha`: switch to `poll-ci-checks.sh`, re-poll CI on the new head. No re-trigger, no reply, no resolve. | n/a |

### 6.5 Tier 1 recipe detail (`uv-lock`)

1. Resolve all non-lock conflicts first (none in Tier 1; a `pyproject.toml` conflict makes the cycle Tier 2).
2. Seed the one named file from the PR side with `git checkout --ours -- uv.lock`. This is a single explicit path, not the forbidden blanket form (R-13, R-14); it is needed because a lock file full of conflict markers is unparseable and a from-scratch resolve could upgrade unrelated dependencies. Then run `uv lock` (network may be needed; failure is a halt, not a retry loop) and `uv lock --check`. See OQ-6 for the "ours" seed versus the base-side seed.
3. `git add -- uv.lock`.
4. Report in the commit body: "uv.lock regenerated from the merged pyproject.toml; dependency versions that changed: <diff of the lock summary>".

### 6.6 Resolution record and commit message (inline in the ref, no template file)

`<output-dir>/sync/<cycle_id>/resolution.md`, one section per `text:*` file, fields in this order:

```text
## <path>
kind: trivial | additive | competing | structural | modify-delete | add-add | semantic   (R-149; semantic => Tier 3)
root_cause: <one phrase: what made git unable to merge>                                (R-146)
ours_intent: <one sentence, what this PR's side does>                                   (R-18)
theirs_intent: <one sentence, what the base side does>                                  (R-18)
resolution: keep_both(<order>) | take_ours | take_theirs | synthesized
behavior_after: <one sentence describing behaviour after the merge>                     (R-156)
dropped: none | <behaviour dropped and why>                                             (S-29)
evidence: <stage files / commits consulted>                                             (R-112, S-12..14)
```

The merge commit message is generated from this file: subject `Merge origin/<base> into <HEAD_BRANCH> (sc:pr-submit sync, tier <t>)`, a body with one line per resolved file (`kind`, `resolution`, `dropped`), and the repository's required attribution lines appended at commit time. It contains intents, never file content, so no secret can enter it (the run-log redaction patterns still apply to the run-log).

`resolution_record_ok(record)` is pure and returns a list of problems: every `text:*` path has an entry; no field empty; `ours_intent` and `theirs_intent` each one sentence (no newline, one terminal stop); `kind != "semantic"`; `dropped` present; `resolution` in the enum; `behavior_after` present. Any problem means no commit.

### 6.7 Validation (VAL reuse, no new gates)

The VAL gate list is unchanged (`SKILL.md:279-291`). Inputs for a sync cycle: `changed-area` = the resolved paths; `is_cross_cutting(resolved_paths)` decides VG-2 as today, and **any resolved path under `src/superclaude/pr_submit/` or any `pyproject.toml` conflict forces VG-2**. Tier 1 adds `uv lock --check` to VG-1. VG-5 (`make verify-sync`) runs when a resolved path is under a synced component. A failing gate triggers the existing single retry; a retry must not introduce changes unrelated to the failure (R-169).

### 6.8 Where an unfinished merge is left

- Halt before the resolution is complete (Tier 3 discovered mid-way, validator disagreement, VAL red after retry): **`git merge --abort`** (ours verified), worktree and index restored, `sync_concluded{aborted}`. An abandoned half-resolution is worse for the operator than a clean tree plus the preserved `resolution.md` and evidence files.
- Resolution complete and validated but the run must stop (L2, or a commit hook rejecting): **leave the merge in progress** (J-53) so nothing the model produced is lost.

### 6.9 Staging, stash and hook rules (summary of what the static tests pin)

Exact-path staging only; the merge's own auto-merged paths are already staged by git, and `finish-merge.sh` proves the staged set is within the expected set. Never stash (J-20, shared stash stack). Never `reset --hard`. Never check out the base branch (J-06) or touch another worktree or branch (J-05, J-91). Never `--no-verify`, never amend. No `.claude/` staging except `.claude/settings.json`, and that file is itself `halt:protected` if it conflicts.

## 7. Requirements

Priority key: **M** must, **S** should. Every FR lists a verifiable acceptance criterion (AC). Research ids in brackets show where an adopted item lands.

### 7.1 Functional requirements

| ID | P | Requirement | Acceptance criteria |
|---|---|---|---|
| **FR-1** | M | **Probe.** `scripts/probe-merge.sh` emits the single-line JSON of section 5.3 and performs no worktree or index mutation. It fetches only `origin <base>`, uses the PR's `baseRefName`, detects `foreign_op` and `index_clean`, and sets `merge_tree_supported` by capability probe. [R-26, R-43, J-16, J-17, S-05, S-38] | (a) On a repo with a clean base, output has `clean: true`, `conflicts: []`; (b) with a content conflict, `conflicts[0].stages == "123"`; (c) with a base-side delete, stages `"13"`; (d) a binary conflict has `binary: true`; (e) a staged file gives `index_clean: false`; (f) a half-finished rebase gives a non-null `foreign_op`; (g) before and after `git status --porcelain=v1 -z` are identical; (h) non-zero exit on missing `--repo`. |
| **FR-2** | M | **Pure classification.** `conflicts.classify_conflicts(entries, *, sync_tier_cap, tier2_max_files=8)` implements the 13-rule table of 4.2 and the tier table, and returns a plan: `tier`, `action` in `{none, report, resolve, halt}`, per-path `class` and `reason`, `reasons` list. Core-pure (no `git`/`gh` tokens, no network). | Parametrized tests cover every rule and every boundary: submodule beats binary; protected beats text; `uv.lock` with stages `"13"` is `halt:lockfile_no_recipe`; 8 text files is Tier 2, 9 is Tier 3 `too_many_files`; unknown stage string is `halt:unknown_shape`; `tier > cap` gives `report`/`tier_above_cap`; empty input gives Tier 0; malformed entries (missing key, non-str path) fail closed to Tier 3. |
| **FR-3** | M | **Flag.** `--sync-tier {0,1,2}` (default 1 in the first release) in `SkillArgs`, `parse_args`, `build_arg_parser` and the command Options table. 0 means detect and report only. | `parse_args([])` yields 1; `--sync-tier 3` is rejected by argparse; the command table row exists; `fsm.py` still has no `git`/`gh` token. |
| **FR-4** | M | **Report before acting.** At the end of Wave 0 (L1+) and at Wave 8a entry, print the plan before any edit: tier, each path with class and reason, and the action the current ordinal would take. [R-51] | Static test: the ref contains the report step ahead of the merge step; L0 emits nothing. |
| **FR-5** | M | **Wave 8a placement.** One bullet in `SKILL.md` and one wave-table row; `refs/conflict-sync.md` loads lazily and only when the probe is not Tier 0. Entry only after the review phase settles with an outcome allowed by section 5.5. | Static test: wave table row present; `SKILL.md` has exactly one python block; the ref is not referenced from any other wave; Tier 0 path loads no ref. |
| **FR-6** | M | **Ordinal behaviour** exactly as the table in 5.4 (L0 nothing; L1 report and propose; L2 local resolution and stop with the merge in progress; L3 full cycle). | Scripted tests per ordinal assert the commands issued (via the ref's static text) and the run-log events; L2 appends no `push_*` event and no commit; L0 byte-identity sentence still present. |
| **FR-7** | M | **Start preconditions.** Before `sync_started`: pr_head check (6.4 step 1), `foreign_op == null`, `index_clean == true`, `HEAD_BRANCH != base`, current worktree only. `sync_started` is appended before the merge command (write-ahead). [J-05, J-16, J-17, J-18, J-26, J-91] | Static test pins the order: precondition text, then `sync_started`, then the merge command in the ref. Script test: dirty index makes the probe report `index_clean: false`. |
| **FR-8** | M | **Merge command.** `git -c merge.conflictStyle=zdiff3 -c rerere.enabled=false merge --no-commit --no-ff <base_sha>`; no `--no-verify`, no global config write, no stash. [J-60, J-20, R-128, S-17] | Static test: exact command string present; absent: `git config`, `git stash`, `--no-verify`, `rerere.enabled=true`. |
| **FR-9** | M | **Tier 1 recipe.** Seed the one named lock file with `git checkout --ours -- uv.lock`, then `uv lock`, `uv lock --check`, `git add -- uv.lock`. A failure of either `uv` command is a halt with `sync_merge_failed` and an abort. [R-58, R-189, S-46, J-48] | Static test: recipe order; recipe table maps `uv.lock` to `uv-lock` only; no other lockfile has a recipe. |
| **FR-10** | M | **Tier 3 halt message and abort.** Message names the file, the operation (merge of `origin/<base>`@sha into `<HEAD_BRANCH>`), the step `k/n`, the branch, and one sentence per side describing what it appears to do (both skipped when classification stopped before reading). It ends with explicit recovery steps and the statement that nothing was pushed. A mid-way halt runs `git merge --abort` only after verifying `MERGE_HEAD == base_sha`. [R-210, R-212, R-54, R-56, R-57, J-13] | Static test pins the message fragments; script test: abort restores a clean worktree and the original `HEAD`. |
| **FR-11** | M | **Finish guard script.** `finish-merge.sh` performs the checks of 6.4 step 9 and commits with `git commit -F <msg>` with hooks on. It prints `{merge_sha, parents}` JSON on success and a precise failure token otherwise. [R-11, J-56, J-61, J-63] | Real-repo tests: unmerged path refused; introduced marker refused; marker line already present in the stage-1 blob accepted; unexpected staged path refused; `MERGE_HEAD` mismatch refused; failing pre-commit hook refused with the hook output verbatim and no commit created; success yields exactly two parents `[HEAD, base_sha]`. |
| **FR-12** | M | **Merge parent rule.** `conflicts.merge_parent_ok` exactly as 6.2. | Matrix per 6.2 including case-insensitivity, trailing newline, swapped order, equal shas, 1 and 3 parents, bad ids; disjointness property against `push_parent_ok`. |
| **FR-13** | M | **Sync decision.** `evaluate_sync_decision` and `sync_fail_state` as 6.3. `fsm.evaluate_push_decision` is not modified. | Full truth table (16 rows) for the four predicates; `sync_fail_state` mapping; byte-for-byte unchanged `evaluate_push_decision` (existing tests pass untouched). |
| **FR-14** | M | **Push path.** Guard order head -> parent -> base-ancestor -> decision -> triad -> push, as 6.4 steps 10 to 12; push command `git push origin <target_sha>:<HEAD_BRANCH>`; `pre_push_sha := target_sha` after. `build_sync_triad` emits the three records in order with `kind: "sync"`, `base_sha`, and the unchanged idempotency key format. | Static test pins the order in the ref and the push command; unit test on `build_sync_triad` order, keys and fields; the force-push scan passes over the new ref and scripts. |
| **FR-15** | M | **One commit per cycle.** A sync cycle commits exactly the merge commit and never a fix commit; a fix cycle never merges. A cycle id prefixed `sync-` is never reused for a fix push. | Ref states the rule; unit test: `merge_parent_ok` rejects a one-parent fix commit and `push_parent_ok` rejects `M`. |
| **FR-16** | M | **Run-log.** Add `sync_started` and `sync_concluded` to `EventType`; `rebuild_state` gains `sync_cycles` (list of cycle ids from `sync_started`) and `sync_push_count`; a `push_completed` with `kind: "sync"` does not increment `push_count`; `pushed_commit_shas` still records `target_sha`. | `len(EventType) == 43` (both pins updated); fold tests including old logs without `kind`; `append` rejects unknown events as today. |
| **FR-17** | M | **Resume.** Recovery rules of 5.8; `resolve_crash_window` copies `kind` and `base_sha`; Branch A of a sync returns `S2_CLASSIFY`; kind-less records behave exactly as before. | Tests: sync Branch A/B/C results; recovered `push_completed` carries `kind`; existing recovery tests pass untouched; a foreign `MERGE_HEAD` is documented as `sync_foreign_operation`. |
| **FR-18** | M | **Post-sync CI.** After a pushed sync, Wave 8 polls CI with `wait_sha = target_sha`; no `retrigger-review.sh`, no reply, no resolve; `round_counter` and `rereview_request_count` unchanged. | Static test on the ref text; run-log fold test shows no `round_incremented` from a sync cycle. |
| **FR-19** | M | **Output contract and status.** Add `sync_tier` (int, 0 to 3), `sync_outcome` (enum `none`, `report_only`, `left_in_progress`, `pushed`, `aborted`, `halted`), `sync_push_count` (int). The `status` enum is unchanged; Tier 3 halts use `terminal_halted`, L2 uses `halt_before_push`. | Static test: three new rows in the Output Contract table; enum line unchanged. |
| **FR-20** | M | **Docs.** Update `SKILL.md` (wave table row, Wave 8a bullet, Wave 0 sentence, contract rows, Will Do and Will Not bullets, Error Handling rows), `commands/pr-submit.md` (flag row, Will Not clause), `refs/state-machine.md` (new section 5.2d: sync phase is SKILL-owned with no FSM edges; no `git`/`gh` tokens). The pinned fragments listed in section 8.4 are left byte-identical. | Pins in 8.4 pass; `make verify-sync` clean. |
| **FR-21** | M | **Prohibited operations** (static-greppable in the ref and scripts): blanket side-taking (`--ours`/`--theirs` with `.` or no path), `-X ours`, `-X theirs`, `-s ours`, hard reset during a conflict, stash in any form, `--no-verify`, `--amend`, `add -A`, `add .`, `commit --only` during a merge, force or `+` refspec pushes, checkout of the base branch, writes to global git config, edits to any path outside the current worktree. Prohibitions in prose use words, not the literal command (G16). [R-13, R-14, R-15, J-20, J-60, J-63, J-05, J-06, J-91] | A single static test with one regex per prohibition; the ref's prohibition paragraph passes its own scan. |
| **FR-22** | S | **Tier 2 evidence step.** `collect-conflict-evidence.sh --path <p> --out <dir>` writes stage 1/2/3 blobs, the left-right log and both merge-base diffs under the output dir, bounded to 200 KiB per file and 60 seconds, and writes nowhere else. [S-12 to S-14, R-112, R-181] | Real-repo test lists exactly the expected files; truncation marker present when the cap is hit. |
| **FR-23** | S | **Tier 2 resolution record and validator.** `resolution_record_ok` as 6.6; one `evidence-validator` spawn per Tier 2 cycle; one revision pass; failures escalate to Tier 3. [R-18, R-156, S-26, S-29, R-146, R-149] | Core tests for each problem class; ref static test for the spawn instruction and the single-revision rule. |
| **FR-24** | S | **Mergeability hint.** `conflicts.mergeability_hint(mergeable, merge_state)` normalises the GitHub fields to `conflicting`, `behind`, `clean`, `unknown`. Used for reporting and for the P3 late trigger only; never to override the local probe. | Table-driven tests incl. `UNKNOWN`, `None`, lowercase, junk strings. |
| **FR-25** | S | **P3 late re-sync.** `poll-ci-checks.sh` adds a `merge_state` field to its JSON line (appended after the existing keys); Wave 8 triggers Wave 8a once more under `SYNC_CAP`, Tier 0 and 1 only. | Existing `classify_checks` tests pass untouched; new payload-shape test; script test with a stubbed `gh`. |

### 7.2 Non-functional requirements

| ID | Requirement | Acceptance criteria |
|---|---|---|
| **NFR-1** | **No force-push, ever.** | The pinned scan (`test_static_grep.py:758-776`) passes over the new files; push command text is exactly `git push origin <sha>:<branch>`. |
| **NFR-2** | **Core purity.** `conflicts.py` has no `git`/`gh` token (docstrings included), imports no `anthropic`, performs no I/O. It joins `CORE_PURE_FILES`. | T-N50 and T-N41 pass with the file added. |
| **NFR-3** | **L0 byte-identical.** No new output, no new call at `--monitor 0`. | The AC-1 sentence assertion is unchanged and passes. |
| **NFR-4** | **Cost layering.** Tier 0 adds at most two read-only calls (fetch and merge-tree, both inside the probe script), no ref load, no model reasoning, no agent. Tier 1 adds no model reasoning and no agent. Only Tier 2 spawns an agent. | Static test: only the Tier 2 section of the ref mentions the evidence script and `evidence-validator`. |
| **NFR-5** | **Fail closed.** Any unparsable probe output, unknown stage shape, missing field, bad sha or unrecognised mode yields Tier 3 (or `unknown` for GitHub hints) and never an action. | Parametrized fail-closed tests for every core function. |
| **NFR-6** | **Repo pin and origin-only.** Every `gh` line in the new ref and scripts carries `--repo`; fetch and push target `origin` only; nothing contacts the upstream. | The existing fork-pin tests (T-1101 family) pass with the new files included. |
| **NFR-7** | **Secrets.** Run-log redaction applies to the new events; the commit message and `resolution.md` contain intents, never file content. | Redaction test on a `sync_concluded` payload containing a token-shaped string. |
| **NFR-8** | **Installed-path hygiene.** No `src/superclaude/` path in the new ref, scripts, command text or SKILL text. | `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` shows no new hit (CLAUDE.md check). |
| **NFR-9** | **Bounded growth of `SKILL.md`.** Net growth is at most 15 lines and no new python block; all procedure lives in the ref; no duplicated guard text (the ref refers to "the Wave 6 pre-push head guard" by name and states only the delta). | Line-count assertion in the static test (`<= 346`). |
| **NFR-10** | **Bounded scripts.** Each new script has a per-call timeout (60 s) and truncates output at 100 KiB with a visible marker; none reads stdin or prompts. | Script tests with an oversized fixture. |
| **NFR-11** | **Capability gate, not version parse.** Missing `git merge-tree --write-tree` degrades to report-only. | Script test with a stubbed `git` that fails the capability probe. |
| **NFR-12** | **Backward compatibility of artifacts.** Old run-logs (no `kind`, no sync events) rebuild identically; the fix-push record shape is unchanged. | Fold test on a recorded fixture; `build_push_triad` tests untouched. |
| **NFR-13** | **Post-change gates.** `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync`, and the full `make test` are green. | CI. |

## 8. Test plan

Conventions kept: pure helpers by direct calls with parametrized fail-closed shapes (as `test_pre_pr_checks.py:201-230`); run-log tests with a real `RunLog` under `tmp_path`; skill text pinned by literal-substring static tests; scripts by their own test file.

### 8.1 New test files

| File | Covers | Notes |
|---|---|---|
| `tests/pr_submit/test_conflicts_core.py` | FR-2, FR-12, FR-13, FR-15, FR-23, FR-24, `build_sync_triad`, NFR-5 | Table-driven. Includes the disjointness property between `push_parent_ok` and `merge_parent_ok`, the 16-row `SyncDecision` truth table, every classification rule and boundary (8 vs 9 files), unknown shapes, malformed entries, `resolution_record_ok` problem classes. |
| `tests/pr_submit/test_conflict_sync_protocol.py` | FR-4 to FR-10, FR-14, FR-18 to FR-21, NFR-4, NFR-6, NFR-8, NFR-9 | Static-grep over `SKILL.md`, `refs/conflict-sync.md`, the scripts and the command. Includes the prohibited-operations scan (FR-21), ordering pins (preconditions < `sync_started` < merge command; head check < `merge_parent_ok` < base-ancestor < DECIDES < push), tier headings, `--repo` on every `gh` line, Tier-2-only mentions of the evidence script and `evidence-validator`, absence of `src/superclaude`. |
| `tests/pr_submit/test_conflict_scripts.py` | FR-1, FR-11, FR-22, NFR-10, NFR-11 | Builds throwaway repos with `git init` plus a local bare repo as `origin` under `tmp_path` (no network, no gh: `gh` is a PATH stub). Skipped when `git merge-tree --write-tree` is unsupported (capability probe, not a version parse). Cases listed in FR-1 and FR-11, plus a `uv` PATH stub for the Tier 1 recipe order. |

### 8.2 Changed existing tests (exact edits)

| File | Edit | Why |
|---|---|---|
| `tests/pr_submit/test_run_log.py:168` | `len(EventType) == 41` becomes `43`; add fold tests for `sync_started`, `sync_push_count`, no `push_count` increment for `kind: "sync"`, old-log compatibility | FR-16, NFR-12 |
| `tests/pr_submit/test_codex_reviews.py:441` | same pinned count `41` to `43` | pinned count |
| `src/superclaude/pr_submit/models.py` docstring | "EXACTLY 41 members" updated to 43 (docstring, not a test, but it states the count) | accuracy |
| `tests/pr_submit/test_crash_recovery.py` | add sync Branch A/B/C cases, recovered record carries `kind` and `base_sha`, kind-less regression | FR-17 |
| `tests/pr_submit/test_skill_parse.py` | `--sync-tier` default, bounds, argparse rejection of 3 | FR-3 |
| `tests/pr_submit/test_static_grep.py:37-51` | add `PR_SUBMIT_PKG / "conflicts.py"` to `CORE_PURE_FILES`; the new ref is NOT added (it necessarily contains git commands, like `thread-reply.md`, which is also outside the set) | NFR-2 |
| `tests/unit/test_cli_install.py:248-262` | add the ref and three scripts to the expected installed list (presence check only, `:496-500`) | install surface |
| `tests/pr_submit/test_pre_pr_checks.py` | no change to `merge` parametrize id (`:216-222`); add one assertion that `push_parent_ok` still rejects a perfectly valid `merge_parent_ok` input | pins the refusal to loosen |
| `tests/pr_submit/test_ci_classify.py` or `test_cosmos_poll.py` | only for FR-25 (P3): payload shape with `merge_state`; existing cases untouched | P3 |

### 8.3 Pinned counts and static greps this design must not break

| Pin | Where | How the design stays safe |
|---|---|---|
| Exactly one python block in `SKILL.md` | `test_cosmos_protocol.py:36`, `test_codex_reviews.py:688` | New procedure is in the ref; code shown in the ref uses `text`/`bash` fences only, and `SKILL.md` gets prose only. |
| `len(EventType) == 41` | `test_run_log.py:168`, `test_codex_reviews.py:441` | Deliberately updated once to 43 (FR-16); no other event is added. |
| T-N50 (no `git`/`gh` token in the eight core-pure files) | `test_static_grep.py:37-51`, `:132-143` | `conflicts.py` is written clean and added to the set; the `state-machine.md` section 5.2d is written clean. The new ref is NOT in the set. |
| T-N41 (no `anthropic` import) | `test_static_grep.py:146-155` | `conflicts.py` imports only `re`, `dataclasses`, `typing` and `fsm.push_idempotency_key`. |
| Head-binding and push pins | `test_static_grep.py:627-755` | The Wave 6 bullet and the Wave 0 head-binding bullet are not edited. The only Wave 0 edit is an appended sentence that leaves every pinned substring intact (Appendix A). |
| Force-push scan over every `.md` and `.sh` | `test_static_grep.py:758-776` | No force form, and no prose of the form "git push" followed by a force flag. |
| Command Will Not sentence | `test_static_grep.py:754-755` | The pinned clause stays; a new clause is appended after it. |
| AC-1 L0 sentence | `test_static_grep.py:650-653` | Untouched. |
| `--json headRefName,headRefOid,isCrossRepository` substring | `test_static_grep.py:636` | The head-binding read is not changed; the probe uses its own `gh pr view ... --json baseRefName,mergeable,mergeStateStatus` call in a script. |
| `test_edge_cases.py:263-267` (matches "Wrong origin" / "behind" / "wrong-owner") | edge cases | The Error Handling row keeps its first cell. New rows are added below it. |
| `tests/commands/test_impact_command.py:327-345` | impact caller strings | Untouched. |

### 8.4 Fragments that must stay byte-identical (copy into a regression test)

1. `with \`--pr <N>\`, at any level, do not rebase`
2. `rebase if behind \`origin/<base>\``
3. `branch (\`origin/<default-branch>\`) on the create path`
4. `| Wrong origin / behind base branch (create path) / wrong-owner URL |`
5. The whole Wave 6 push-guard wording (`pr_head_ok(<local branch>, pre_push_sha,`, `push_parent_ok(<parents>, pre_push_sha)`, `The deterministic core DECIDES`, `then set \`pre_push_sha := target_sha\``)
6. `push any commit besides the cycle's one fix commit`
7. `the commit to push must have exactly one parent, that same SHA` and `The parent check applies only when the cycle applied edits` in `state-machine.md`

### 8.5 Manual verification (not automated; goes into the P1 and P2 hand-test notes)

- A real PR on a scratch fork with a `uv.lock` conflict: L1 report, L2 stop, L3 push, CI starts on the new head.
- A real text conflict at `--sync-tier 2`: the commit body shows the record; the validator disagreement path; a deliberate semantic conflict halts with nothing pushed.
- GitHub's own `mergeable` after the push is `MERGEABLE`.
- `--resume` after killing the session at each point of 5.8.
- Probe on a repo where `git merge-tree` is unavailable degrades to report-only.

### 8.6 Run order for the implementer

`uv run pytest tests/pr_submit tests/unit/test_cli_install.py tests/commands -q`, then `make lint`, `uv run ruff format --check src/ tests/`, `make verify-sync`, then `make test` (VG-2 is forced by `fsm.py`/`run_log` edits).

## 9. Minimal-risk transformation path (phasing)

Each phase is shippable alone, adds no behaviour that the next phase must undo, and has a go/no-go gate. This is the refactorer's core contribution: the riskiest element (publishing a model-resolved merge) arrives last and dark.

| Phase | Ships | Mutates repo or remote? | Go/no-go before the next phase |
|---|---|---|---|
| **P0 Detect and report** | `probe-merge.sh`, `conflicts.classify_conflicts`, `mergeability_hint`, the Wave 0 report and Wave 8a report-only path at every ordinal, wave-table row, `refs/conflict-sync.md` (report sections only), create-path wording clarification (Appendix A), `--sync-tier` flag parsed but only 0 acted on | No (a fetch of `origin <base>` only) | The report matched GitHub's own `mergeable` on at least 5 real PRs, or the disagreements are explained. |
| **P1 Tier 1 and the publish machinery** | `merge_parent_ok`, `evaluate_sync_decision`, `build_sync_triad`, the two events, run-log and recovery `kind` edits, `finish-merge.sh`, the `uv-lock` recipe, L2 stop, L3 push, post-sync CI re-poll | Yes (merge commit, fast-forward push) | A real `uv.lock` conflict end to end at L3, `--resume` exercised at each crash point, no change to any pre-existing test except the two count pins. |
| **P2 Tier 2** | `collect-conflict-evidence.sh`, the resolution record and `resolution_record_ok`, the validator step, the high-suspicion checklist, default stays `--sync-tier 1` | Yes, only when the operator passes `--sync-tier 2` | At least 10 real text-conflict runs with zero silent behaviour loss found in review; then decide to flip the default to 2 (OQ-1). |
| **P3 Late re-sync** | `merge_state` in the CI poll payload, the second Wave 8a trigger (Tier 0 and 1 only) | Yes | Observed need: at least one real run where the base moved during the CI wait. |

Rollback per phase is a code revert; at runtime `--sync-tier 0` restores today's behaviour (plus the report) with no other change. A pushed merge is reversed by a revert commit, never by rewriting history.

## 10. Risks

| # | Risk | Likelihood / impact | Mitigation | Residual |
|---|---|---|---|---|
| K1 | A model-resolved Tier 2 merge silently drops behaviour and is pushed at L3 | Medium / High | Default `--sync-tier 1`; mandatory one-sentence intents; `dropped` field in the commit body; independent `evidence-validator`; VAL; Tier 3 on any doubt; revert path | Validator and author share model biases; the dark-launch gate in P2 is the real control. |
| K2 | Local `merge-tree` and GitHub disagree about conflicts | Medium / Low | Local is the truth for action; GitHub is a hint; `github_disagrees` reported | Operator sees a PR that is still `CONFLICTING` after a push and must investigate. |
| K3 | `uv lock` needs network or changes unrelated pins | Medium / Medium | PR-side seed keeps pins; `uv lock --check`; report the lock diff in the commit body; failure is a halt | A forced re-resolve if the seed fails (halts, never auto-retried). |
| K4 | Hooks (`pre-commit`, `commit-msg`) reject the merge commit | Medium / Low | Hooks stay on; output reported verbatim; merge left in progress; no amend | Operator must finish by hand. |
| K5 | The pinned-substring tests make `SKILL.md` brittle | High / Medium | Additive edits only; Section 8.4 regression test of the untouchable fragments; `SKILL.md` growth capped (NFR-9) | None specific to this feature. |
| K6 | An L2 merge in progress confuses a later run | Low / Medium | `sync_started` marks it as ours; foreign operations halt; the L2 message tells the operator to commit or abort | A user who ignores both. |
| K7 | The base moves between probe and push | Medium / Low | Merge by recorded `base_sha`; fast-forward push unaffected; PR is "behind" again but mergeable | One more sync cycle on the next run. |
| K8 | Reviewers never see `M` | High / Low | Commit body carries the record; Tier 2 is opt-in; Tier 1 is mechanical | A human reviewer is the only reader of a Tier 2 resolution. If this is unacceptable, add a reviewer re-trigger variant (OQ-3). |
| K9 | The review phase has already run before a Tier 3 halt | Medium / Low | Early Wave 0 report; review results retained in the final report | Wasted review time. |
| K10 | `gh pr view --json mergeable,mergeStateStatus,baseRefName` field set varies by gh version | Low / Low | Failure yields `null` hints and falls back to local truth; capability text in the ref | None. |
| K11 | A conflict marker legitimately present in a file (docs, tests that discuss conflicts, this very repo) trips the guard | Medium / Low | Guard compares marker-line counts with the stage-1 blob, so only *introduced* markers fail | A file where a side added a legitimate marker example halts with `sync_marker_left`; human finishes. |
| K12 | Large Tier 2 cycles extend wall-clock at the end of the run | Medium / Low | `TIER2_MAX_FILES` cap; `--timeout` unaffected (it bounds waits, not resolution) | Cap value is a guess (OQ-9). |
| K13 | Reverting a merge commit is non-obvious (`-m 1`) | Low / Low | The ref and the L2 and L3 reports include the exact revert command | None. |

## 11. Out of scope

- Rebasing, force-push recovery, history rewriting of any kind (R-02, R-16 to R-38).
- PR decomposition or splitting (R-09, R-10, R-37 to R-39).
- Resolution by external tools (mergiraf and similar), snapshot or notebook special-casing, rerere (R-60, R-62, R-64 to R-69).
- Conflicts on the create path before a PR exists; that path keeps its rebase-or-halt behaviour (Appendix A).
- PRs whose head lives on a fork (cross-repo head): the skill never pushes there (existing rule), so it reports only.
- Cherry-pick, revert and rebase operations in progress: detected, then halted (J-17), never resumed or finished.
- Resolving conflicts in any worktree other than the current one, or merging the base into any branch other than the PR head (J-05, J-91).
- A user-override channel (R-19, R-20) and a separate conflict-only command.
- Server-side `gh pr update-branch`.
- Re-triggering reviewers after a sync, replying to threads, and giving a sync cycle a share of `max_rounds`.
- Migration, submodule, binary, protected-file and unknown-lockfile resolution: these halt by design.
- Changes to reviewer detection, severity routing, loop guard semantics or CI classification (other than the additive `merge_state` field in P3).

## 12. Open questions

| # | Question | Recommendation | Impact if wrong |
|---|---|---|---|
| OQ-1 | Default for `--sync-tier`: 1 or 2? | 1 for the first release; flip after the P2 gate. | Default 2 pushes model-resolved text merges for every L3 user on day one. |
| OQ-2 | Tier 0 behind-only with a branch rule "require up to date" (`mergeStateStatus` BEHIND): act or report? | Report only in v1; a clean `merge --no-commit` is the same machinery and can be enabled by a one-line policy flip. | A protected repo needs a manual update-branch click. |
| OQ-3 | Should a Tier 2 sync re-trigger reviewers so a bot sees the resolution? | No in v1 (keeps the FSM, round and INV-R1 untouched). If wanted, treat it as a separate follow-up that reuses the S5a machinery with `kind: "sync"` excluded from `rereview_request_count`. | Unreviewed model-resolved code reaches the PR. |
| OQ-4 | Should Wave 8a act on the wait-only paths (`HALT_MAX_ROUNDS`, `TERMINAL_AUGMENT_NO_RESPONSE`)? | Report only in v1. A sync consumes no round, so acting is defensible, but the "wait-only, no auto-fix" rule is simpler to keep whole. | PRs that exhaust rounds stay conflicted. |
| OQ-5 | Are real-repo script tests acceptable under "no live git network tests"? | Yes: local bare remote, no network, skipped without the capability. | If not, the scripts lose their only executable tests and only the static pins remain. |
| OQ-6 | Tier 1 lock seed: PR side (`--ours`) or base side? | PR side, because the manifest from the PR is merged in and `uv lock` then adds the base's new dependencies; verify on a real conflict that base-added pins are not downgraded. | Dependency drift in the lock file. |
| OQ-7 | Replace the create-path rebase with a sync merge? | No. Keep the current pins; clarify only (Appendix A). Reconsider when the create path shows real conflicts. | The wording tension persists. |
| OQ-8 | Which `gh pr view --json` fields are guaranteed (`mergeable`, `mergeStateStatus`, `baseRefName`)? | Probe at run time like the CI preflight; hints are optional. | Probe returns nulls; behaviour is still correct. |
| OQ-9 | `TIER2_MAX_FILES = 8`: right value? | Ship 8 as a named constant; revisit after 10 runs. | Too low halts easy conflicts; too high spends a long cycle. |
| OQ-10 | Is a `pyproject.toml` conflict Tier 2 or Tier 3 (dependency changes are high-suspicion, R-180)? | Tier 2 with forced VG-2 and `uv lock --check`. | A bad dependency merge reaches CI. |
| OQ-11 | Can the FSM reach its `HALT_HUMAN` / `S4'_HALT_BEFORE_PUSH` terminals from the Wave 8 position using only existing events? | Expected yes (the CI human-gate does it for `HALT_HUMAN`); if the L2 case has no existing event, report `halt_before_push` from the SKILL and record `sync_concluded`, with no new `MonitorState`. Verify in P1 with a driven `run_skill` test. | An extra FSM edge, which this design tries to avoid. |
| OQ-12 | Is the `evidence-validator` pass mandatory for Tier 2? | Yes in v1; measure its disagreement rate in P2 and relax if it never disagrees. | Extra spawn cost for no signal. |
| OQ-13 | Commit attribution lines on the merge commit | Follow the session's commit rules at commit time (the finish script takes the message from a file written by the skill). | Missing attribution. |
| OQ-14 | Should `needs_rebase` (T-107) be renamed or its docstring updated now that merging is the supported way to catch up? | Leave as is; it is pinned by T-107 and only used on the create path. | None. |

## 13. Index

### 13.1 Research items adopted (ids with ROI above 5) and where they land

| Items | Lands in |
|---|---|
| R-05, R-18, R-156, S-26, S-29 (halt when intent is not statable; no third behaviour; say what was dropped) | FR-10, FR-23, section 4.3, 6.6 |
| R-11 (no markers) | FR-11 (introduced-marker check) |
| R-13, R-14, R-15, J-20, J-60, J-63, J-05, J-06, J-91 (prohibited operations, no stash, no `--no-verify`, no amend, current worktree only) | FR-21, 6.9 |
| R-43, R-54, R-56, R-57, R-84 (submodule, migration, binary, unreadable halt) | FR-2 rules 1, 3, 5, 6; 4.3 |
| R-58, R-59, R-189, S-46, J-48 (generated and lock files regenerate from resolved sources; halt without a recipe; only the lockfile's manager) | FR-2 rules 7 to 9, FR-9, 6.5 |
| R-51, R-210, R-212 (report before editing; HALT message content) | FR-4, FR-10 |
| R-112, S-12, S-13, S-14, S-17, R-181 (stage reads, left-right log, both merge-base diffs, three-way comparison) | FR-22, 4.4 |
| R-146, R-149, R-150 to R-154 (root cause and kind labels; additive, structural, delete-versus-edit) | FR-23 record, 6.6 |
| R-180, R-251 (high-suspicion checklist; no API drop before consumers move) | 4.4 |
| S-05, S-09, J-13, J-15, J-16, J-17, J-18, J-26 (operation ownership, ours/theirs meaning, abort lines, detached head, dirty tree, default branch) | FR-1, FR-7 |
| S-38, S-39, S-40 (tree conflicts via status codes; delete-versus-edit; add/add) | FR-2 rules 11, 12 |
| J-39, J-40, J-53, J-56, J-61, J-66, R-173 (agent does the judgment, one file at a time, leave merge in progress when complete, exact staging, hook output verbatim, resolution is authored code, no extra LLM client) | 3.2 R1, 6.4, 6.8 |
| R-128 (never auto-apply a historical result) | FR-8 (`rerere.enabled=false`) |
| R-169 (no unrelated changes on retry) | 6.7 |
| R-02 (bounded scope) | section 11 |

Adopted in spirit, deliberately simplified: R-26 and R-40 (a probe JSON instead of a status script and categoriser), R-33 (one tunable file cap instead of rebase-step thresholds), R-17 (bulk operation only for the single regenerate category).

Considered and rejected from the above-5 set: R-19, R-20 (no override channel), R-60 (snapshots: fold into "generated without recipe"), R-101 (read-only recombination subsystem), R-161 (whitespace check duplicates VG-3 and VG-4), J-15 (already covered by `pr_branch_ok` rejecting `HEAD`), S-18 and S-39 overlaps (covered by the kind labels).

### 13.2 Files this design creates or edits

| Kind | Path |
|---|---|
| New | `src/superclaude/pr_submit/conflicts.py` |
| New | `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-sync.md` |
| New | `src/superclaude/skills/sc-pr-submit-protocol/scripts/probe-merge.sh`, `collect-conflict-evidence.sh`, `finish-merge.sh` |
| New tests | `tests/pr_submit/test_conflicts_core.py`, `test_conflict_sync_protocol.py`, `test_conflict_scripts.py` |
| Edit | `src/superclaude/pr_submit/models.py` (+2 events, docstring), `run_log.py` (two fold branches), `recovery.py` (key tuple + one conditional), `fsm.py` (argument only), `__init__.py` (exports) |
| Edit | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`, `refs/state-machine.md` (section 5.2d), `src/superclaude/commands/pr-submit.md` |
| Edit tests | see 8.2 |
| After editing | `make sync-dev`, `make verify-sync`; stage only the `src/` and `tests/` side, never `.claude/` mirrors |

### Appendix A. The create-path "rebase vs HALT" tension: resolution

The text says Wave 0 should "rebase if behind `origin/<base>`" (`SKILL.md:267`) and the STOP block and Error Handling row say a branch behind the base on the create path is a HALT (`SKILL.md:220-223`, `:315`). The suite pins both sentences and states the intent in a comment ("the create path still rebases, and only the create path halts when behind base", `test_static_grep.py:656-661`). The two are reconcilable without changing a pinned substring:

- **Reading that wins:** on the create path the branch is not yet a published PR head, so rewriting it locally is harmless. Wave 0 rebases it; the HALT applies only when the branch is *still* behind or the rebase cannot complete (a rebase that stops on a conflict is not continued; the operator is told to bring the branch up to date themselves and re-run).
- **Edit:** append one clarifying sentence to the Wave 0 bullet: "A rebase that stops on a conflict is not resolved here (the branch is not a PR head yet): stop and tell the operator to update the branch themselves, then re-run." Keep the STOP block and the Error Handling row as they are.
- **Why not delegate to the new feature:** the sync cycle needs a bound PR head (`HEAD_BRANCH`, `pre_push_sha`), which does not exist before `gh pr create`. Once the PR exists, Wave 0 and Wave 8a take over exactly as on the `--pr` path.

### Appendix B. Probe and finish script exit contract (for the implementer)

| Script | Success | Failure tokens (stdout, one line) | Exit |
|---|---|---|---|
| `probe-merge.sh` | the JSON of 5.3 | `PROBE_FAIL <reason>` (missing `--repo`, not a git worktree, fetch failed, parse failed) | 0 / 2 |
| `collect-conflict-evidence.sh` | `{"dir": "<path>", "files": [...], "truncated": false}` | `EVIDENCE_FAIL <reason>` | 0 / 2 |
| `finish-merge.sh` | `{"merge_sha": "<sha>", "parents": ["<ours>", "<base>"]}` | `FINISH_FAIL unmerged` / `markers` / `staged_unexpected` / `foreign_merge` / `hook_rejected` / `no_merge_head` | 0 / 2 |

None of the scripts reads stdin, prompts, or writes outside the repository's own git directory and the given output directory.
