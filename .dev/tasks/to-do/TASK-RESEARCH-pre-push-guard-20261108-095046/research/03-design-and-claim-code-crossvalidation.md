# Research: Design section 19 and claim-code cross-validation

**Investigation type:** Doc Analyst
**Scope:** docs/designs/sc-issue-launch-level-hook.md section 19; orca_worktree.py; install_hooks.py
**Status:** Complete
**Date:** 2026-11-08

---

## 1. Subsection 19.6 source artifacts (design lines 536-545)

Glob run from the worktree root, 2026-11-08.

| Design line | Artifact path | Exists? | Evidence |
|---|---|---|---|
| 540 | `.dev/brainstorms/20261106-l2-prepush-decisions/q1-install-place/run-4/merged-answer.md` | NO | Glob `.dev/brainstorms/20261106-l2-prepush-decisions/**/*` returned no files |
| 541 | `.dev/brainstorms/20261106-l2-prepush-decisions/q2-chaining/run-4/merged-q2-answer.md` | NO | same Glob, no files |
| 542 | `.dev/brainstorms/20261106-l2-prepush-decisions/q3-removal/run-4/merged-answer.md` | NO | same Glob, no files |
| 543 | `.dev/brainstorms/20261106-l2-prepush-decisions/q4-testing/run-4/answer-merged.md` | NO | same Glob, no files |
| 538 | sibling `adversarial/return-contract.yaml` files | NO | the whole `20261106-l2-prepush-decisions/` directory is absent |

Extra check (corrected in the Gate 1 cycle 0 fix, 2026-11-08): the earlier statement here, that Glob `.dev/brainstorms/2026110[56]*` returned no files and that the line-487 corpus is absent, was wrong. A fresh Glob `.dev/brainstorms/2026110[56]*/**/*.md` returns 48 files in two directories: `20261105-024132-issue-claim-orca-worktree-flag/` (23 `.md` files) and `20261105-170229-launch-level-hook/` (25 `.md` files). The historical corpus named at design line 487 therefore EXISTS and is git-tracked (`git ls-files .dev/brainstorms/20261105-170229-launch-level-hook/` lists 27 files; last commit touching it: `4f7e3e7e feat(hooks): retain originating session identity for governed Bash jobs (#414)`). Every file design line 487 names is present: `merged-requirements.md`, `enrichment/research-light.md`, `adversarial/adversarial/plan-review.md`, `plan-review-2.md`, `plan-review-3.md`, and `adversarial/adversarial/refactor-plan.md`. Only the `20261106-l2-prepush-decisions/` tree of section 19.6 is absent (`git ls-files .dev/brainstorms/20261106-l2-prepush-decisions/` lists 0 files).

Re-check of section 19 statements against the line-487 corpus: no D19 row in this file rests on that corpus. The rows tagged "source artifact absent" (D19-10, D19-17, D19-33, D19-49, D19-52 to D19-56) all cite the section 19.6 run-4 artifacts or "Q artifacts", which are in the absent `20261106-l2-prepush-decisions/` tree, so their tags do not change. The corpus does hold the earlier L2 discussion, for context only: `merged-requirements.md:1384` ("Alternative L2. A `pre-push` git hook ... installed per linked worktree by the claim script, which receives the real remote ref names on stdin and refuses any update of `refs/heads/master` or `refs/heads/main` under any level"), and its rejection reason at `adversarial/adversarial/refactor-plan.md:1158` ("Shared with the person's own pushes via the common git directory; cannot tell which session called; `--no-verify` skips them") and `adversarial/adversarial/variant-1-opus-architect.md:135`. That rejection reason agrees with design line 493 (no session id) and with 04 E30 (common-dir hook placement).

**Key Takeaways**

- None of the four Q1-Q4 run-4 artifacts, nor their return contracts, exists in this checkout. Every section 19 statement that rests on them (lines 510, 514 "Q1/Q2's advisory 'continue claim'", 524, 534 "Q artifacts report local hook invocation", 540-543) is tagged [UNVERIFIED: source artifact absent from checkout].
- The placement decision of 19.2 (one owned shared `hooks/pre-push` plus a private-worktree marker) therefore has no inspectable evidence here; only the design's own summary of it.

---

## 2. Code unit: `l2_status` (orca_worktree.py:1012-1029)

File: `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`.

**What it runs.** One subprocess, no shell: `git -C <wt> rev-parse --git-path hooks/pre-push` (line 1020), through `run()` (lines 123-147). `run()` never raises: `TimeoutExpired` gives `timed_out=True`; `FileNotFoundError`, `PermissionError` and any other `OSError` give `missing=True` (lines 136-146). `Result.ok` is `rc == 0 and not timed_out and not missing` (line 97).

**Data flow.** worktree path `wt` in -> git's own hook-path answer (stdout, stripped, line 1021) -> `absent` when the git call failed or printed nothing (lines 1022-1023) -> `hook = Path(wt) / out` (line 1024, comment: "a relative answer is relative to wt") -> `present-unverified` when `hook.is_file()` and `os.access(hook, os.X_OK)`, else `absent` (lines 1025-1029).

**Relative versus absolute answers.** `Path(wt) / out` returns `out` unchanged when `out` is absolute (pathlib semantics), so one expression handles both. Observed with git 2.47.3 in a disposable `/tmp` directory (removed afterwards; no push run):

| Repo shape | `rev-parse --git-path hooks/pre-push` answer | Resolved by `l2_status` to |
|---|---|---|
| main checkout, default lookup | `.git/hooks/pre-push` (relative) | `<wt>/.git/hooks/pre-push` |
| linked worktree | `/tmp/.../main/.git/hooks/pre-push` (absolute, common git dir) | the common dir's hook |
| main checkout, `core.hooksPath=myhooks` (relative value) | `myhooks/pre-push` (relative) | `<wt>/myhooks/pre-push` |
| this worktree (`issue-441`, linked) | `/home/coder/workspaces/IronClaude/.git/hooks/pre-push` | absent today: that file does not exist (`ls` reported no such file) |

These rows are local observations of one git version, not code proof of git's behaviour in general.

**What it reports (observed by calling the real `l2_status` through `uv run --no-project python` against those repos):**

| Case | Result |
|---|---|
| no `pre-push` file | `absent` |
| `pre-push` exists, mode 0644 (not executable) | `absent` |
| `pre-push` exists, mode 0755 | `present-unverified` (both the main checkout and its linked worktree, because they share the common dir) |
| `core.hooksPath` set and an executable hook there | `present-unverified`; an executable hook at the default path is then ignored |
| `pre-push` is a directory | `absent` (`is_file()` false) |
| path that is not a git repository | `absent` (git exits nonzero) |
| `git` not on PATH | `absent` (`run()` returns `missing=True`) |

The pytest `test_ir6_l2_status_follows_the_git_hook_path` (tests/skills/test_issue_orca_worktree.py:1686-1729) pins five of these cases (no-file, not-executable, foreign-executable, hooks-path, hooks-path-elsewhere) on a linked worktree and asserts the hook file is never modified.

**Present-unverified, not verified.** The docstring (lines 1013-1019) says the function "never claims to know what the hook enforces". It reads no file content, checks no owner, version line or ownership marker, and does not run the hook. Any executable at git's hook path, including a foreign hook or a `pre-commit`-framework shim, yields `present-unverified`. The call-site comment (lines 1307-1308) repeats: it "looks for no ownership marker (design section 19.2) and never touches the hook".

**Edge cases not handled.** (a) `git` missing, a timeout and "not a repository" all fold into `absent`; the caller cannot tell "no hook" from "could not ask git". (b) `os.access(..., X_OK)` is true for root on any file with any x bit; not relevant to the normal user case. (c) A symlink named `pre-push` is followed by `is_file()`. (d) No separate check of `extensions.worktreeConfig` or a per-worktree `core.hooksPath`; whatever git answers for `-C wt` is used, which is the correct source.

**Pattern.** Path resolution goes through git (`rev-parse --git-path`), never assumes `.git` is a directory. This matches design line 510 for the read side.

**Dependencies.** Called once, at orca_worktree.py:1311 inside `cmd_launch` (Grep for `l2_status` finds only the definition, the call and a docstring mention at 1036). Its answer feeds two consumers: the `W-L2-ABSENT` note (line 1312) and the `L2 pre-push:` layer line in `session_report` (lines 1061-1067, called at 1376 with the same `l2` value, so they always agree).

**Key Takeaways**

- `l2_status` is a read-only, presence-and-executable probe of git's effective pre-push path. It is the natural post-install check for an L2 installer, but today it cannot tell "our L2 guard" from "any executable".
- An L2 installer would need its own ownership/content check (design line 512); `l2_status` would then need a third state (for example `present-owned`) to stop reporting `present-unverified` for the real guard.

---

## 3. Code unit: `W-L2-ABSENT` remedy, why text and call site (orca_worktree.py:778-799, 1305-1312, 1376-1385)

**Remedy text** (REMEDY table, lines 789-792):

> "the L2 layer is not built yet and the limits are enforced by the L1 guard only; the agent was started"

**Why text** (`L2_ABSENT_WHY`, lines 796-799):

> "the worktree has no executable pre-push hook at git's hook path, so no L2 pre-push layer checks this session's pushes"

**Comment above it** (lines 794-795): "IR-7 (design section 13) says refuse; this plan builds no L2 layer, so the claim warns instead and the launch goes ahead."

**Call site and IR-7 comment** (lines 1305-1312):

```python
hook = "installed"
notes: list[tuple[str, str]] = []
# IR-7 as a warning, before publish_pending: reads the hook path only, looks
# for no ownership marker (design section 19.2) and never touches the hook.
# To make it the design's refusal, add after the l2_notes line:
# if l2_notes: return emit(launch_result("failed", l2_notes, enforcement_hook=hook))
l2 = l2_status(wt)
l2_notes = [("W-L2-ABSENT", L2_ABSENT_WHY)] if l2 == "absent" else []
```

**Order inside `cmd_launch` (lines 1253-1388).** already-launched check (1262-1278) -> stale-prompt check (1279-1281) -> IR-4 `enforcement_preflight` (1287-1304, refuses with `W-ENFORCEMENT-ABSENT`, `enforcement_hook="missing"`) -> `l2_status` (1311-1312) -> `publish_pending` (1315) -> `orca agent launch ... --prompt "[sc-launch:v1:<nonce>] ..."` (1330-1334) -> ccsession screen check (1356-1365) -> `record_launch` (1368) -> `session_report(wt, l2, inode)` (1376) -> `launch_result("launched", notes + l2_notes, ...)` (1377-1385). `launch_result` (1203-1220) makes the FIRST note the `warning` field and appends the rest to `detail` as `also <code>: <why> (<remedy>)`, so a ccsession warning takes precedence and `W-L2-ABSENT` then appears only in `detail` (pinned by tests/skills/test_issue_orca_worktree.py:1554).

**When it fires.** Only when `l2 == "absent"`. A foreign executable hook gives `present-unverified` and NO warning (test row "foreign-executable", tests/skills/test_issue_orca_worktree.py:1691, 1727).

**Effect on status.** Never changes the launch outcome: the agent is already started when `W-L2-ABSENT` is emitted, status is `launched`. The skill doc agrees: `src/superclaude/skills/sc-issue-protocol/SKILL.md:150` ("`W-L2-ABSENT` means the agent was started with no L2 pre-push layer").

**Key Takeaways**

- The code implements IR-7 as a non-blocking warning, deliberately and with an in-code note giving the one-line change that would turn it into the design's refusal.
- The trigger is "no executable at git's pre-push path", not "no accepted, owned L2". A conflict (foreign hook) is silent, which differs from design line 514 (see D19-15).

---

## 4. Code unit: `install_hooks.py` (whole file, 612 lines)

File: `src/superclaude/cli/install_hooks.py`. Public entry `install_hooks(target_path=None, force=False)` (lines 153-243).

**What it installs.**

1. Scripts: every name in `_FRESHNESS_SCRIPTS` (lines 42-94) plus `_LEGACY_SCRIPTS = ["session-init.sh"]` (line 95), copied by `_copy_scripts` (lines 251-290) into `hooks_dir = target_path.parent / "hooks"` (line 173), i.e. `~/.claude/hooks/` by default; `shutil.copy2` then `os.chmod(0o755)` (lines 284-285); an existing file is skipped unless `force` (279-281). The list includes `launch-job-identity.sh` (line 90) and `launch-level-guard.sh` (line 93).
2. Claude Code settings: `_merge_settings` (lines 298-491) merges `src/superclaude/hooks/hooks.json` registrations into `~/.claude/settings.json`, with a timestamped backup (331-343) and atomic write (`_atomic_write_json`, 507-523). Ownership is by exact command string (`_owns_command`, 123-129; `_owns_registration`, 132-139).
3. Seed data: `_SEED_FILES` (101-103), `auggie-projects.txt.example` -> `~/.claude/auggie-projects.txt`, only when absent (`_deploy_seed_files`, 556-587).
4. Helper only: `validate_session_id` (602-611), not called by `install_hooks`.

**Does any code path write a git hook?** NO. Every write target derives from `target_path` (the Claude settings file) and its parent: `hooks_dir` (173), `target_path` (477), backup (335-337), `dest_root=target_path.parent` (228). The file never runs `git`, never imports `subprocess`, never calls `rev-parse`, never reads or writes `.git/hooks`, `core.hooksPath` or `extensions.worktreeConfig`. Grep of `src/` for `hooksPath|worktreeConfig|pre-push|prepush` finds no installer; the only L2-related hits are `orca_worktree.py` (l2_status, W-L2-ABSENT text) and the issue skill docs. The "hooks" this file installs are Claude Code hooks, a different mechanism from git hooks.

**Integration opportunity.** An L2 installer is not a natural fit for `install_hooks.py`: that module is user-global (`~/.claude`), while a git pre-push hook is per-repository (common git dir or `core.hooksPath`). Design line 565 places installation in "a future claim launcher", i.e. next to `cmd_launch` in `orca_worktree.py`, between the IR-4 preflight (1287) and the `l2_status` probe (1311), which would then serve as the post-install check. A shippable hook body could still live in `src/superclaude/hooks/scripts/` and be distributed by `_FRESHNESS_SCRIPTS`, but note `make verify-sync` requires every script there to be listed (comment at lines 62-64).

**Key Takeaways**

- `install_hooks.py` installs Claude Code hook scripts and `settings.json` registrations only; it has no git-hook code path.
- No code in the repository installs, owns or verifies a git `pre-push` hook. The L2 layer of section 19.2-19.5 is entirely unbuilt.

---

## 5. Claim table: section 19 (design lines 489-578)

Paths: `ow` = `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`; `ih` = `src/superclaude/cli/install_hooks.py`; `jid` = `src/superclaude/hooks/scripts/launch-job-identity.sh`; `llg` = `src/superclaude/hooks/scripts/launch-level-guard.sh`. Git-behaviour statements stay [UNVERIFIED] by rule and are listed as `UNVERIFIED-GIT` in Gaps.

### 19.1 Actor selection and B-CTX (lines 491-506)

| ID | Design line | Claim (short) | Tag | Evidence |
|---|---|---|---|---|
| D19-1 | 493 | Ordinary human push in the same worktree is never restricted by launch policy | [UNVERIFIED] | No L2 code exists (section 4); vacuously nothing restricts pushes at push time today. No code to verify the invariant against |
| D19-2 | 493 | Git's pre-push inputs are remote name/location and ref-update records; no Claude session id | [UNVERIFIED] | Git behaviour; UNVERIFIED-GIT |
| D19-3 | 493 | Marker is only an eligibility hint; env values, pane key, branch or path never authority | [UNVERIFIED] | No L2 selector exists. Related: `jid` `identify()` selects by `/proc` kernel session + job record + governed record (jid:215-242), no env label; but its store is HOME-based (design 557 admits this) |
| D19-4 | 495 | Controller-process candidate is historical; scoped integration binds each Bash job (19.7) | [CODE-VERIFIED] | jid:2 "not a sandbox or controller-PID binding"; per-call adaptation jid:440-483 |
| D19-5 | 497-502 | Historical steps 1-4 (ancestor PID record, bounded parent walk) not adopted | [CODE-VERIFIED] | No ancestry walk: jid:253 "No bounded ancestry walk ... is interpreted as ordinary"; `members()` scans `/proc` by kernel session (jid:251-264) |
| D19-6 | 504 | OB-CTX/B-CTX completion evidence not observed | [UNVERIFIED] | Status claim; no evidence artifact checked in scope |
| D19-7 | 506 | Claim code launches governed pipelines and refuses one when L1 not effective | [CODE-VERIFIED] | ow:1287-1304 (refusal, `W-ENFORCEMENT-ABSENT`), ow:1330-1334 (launch) |
| D19-8 | 506 | The L2 layer this section selects for is not built | [CODE-VERIFIED] | ih has no git-hook path (section 4); REMEDY text ow:789-791 "the L2 layer is not built yet" |
| D19-9 | 506 | Activation conditional, no root service, human isolation not weakened | [UNVERIFIED] | Intent; no L2 code |

### 19.2 Placement and coexistence (lines 510-514)

| ID | Design line | Claim (short) | Tag | Evidence |
|---|---|---|---|---|
| D19-10 | 510 | Run-4 merged artifacts prefer one owned shared `hooks/pre-push` + private-worktree marker, no config change, no forwarding | [UNVERIFIED: source artifact absent from checkout] | Section 1 Glob |
| D19-11 | 510 | Resolve common/private Git paths using Git, never assume `.git` is a directory | [CODE-VERIFIED] (read side only) | ow:1020 `git -C wt rev-parse --git-path hooks/pre-push`; no installer exists for the write side |
| D19-12 | 510 | Existing `pre-commit`, `commit-msg` and other hooks remain untouched | [CODE-VERIFIED] (vacuous) | No code writes git hooks (ih:173-228 write targets; ow l2_status read-only, ow:1307-1308); test asserts no modification tests/skills/test_issue_orca_worktree.py:1729 |
| D19-13 | 512 | Install only if default lookup, no foreign pre-push, publication/self-test succeeds | [UNVERIFIED] | No installer. Note `l2_status` honours `core.hooksPath` and treats a foreign hook as `present-unverified` |
| D19-14 | 512 | Publish complete executable without replacing existing file; recheck owned version/content; header alone not ownership proof | [UNVERIFIED] | No installer; `l2_status` checks no ownership (ow:1012-1029) |
| D19-15 | 512 | Do not enable `extensions.worktreeConfig`, migrate `core.hooksPath`, shadow, stub or replay foreign hooks | [CODE-VERIFIED] (absence) | Grep `hooksPath|worktreeConfig` in `src/` finds only the ow:1015 docstring |
| D19-16 | 514 | Conflict or unsupported lookup: preserve files/config, report `W-L2-ABSENT` with the reason | [CODE-CONTRADICTED] | Files are preserved, but `W-L2-ABSENT` fires only for `absent` (ow:1312) with one fixed reason (ow:796-799). A conflict (foreign executable hook) reports `present-unverified` and NO warning (tests/skills/test_issue_orca_worktree.py:1691, 1727); unsupported lookup is never detected or named |
| D19-17 | 514 | "Unlike Q1/Q2's advisory 'continue claim'" | [UNVERIFIED: source artifact absent from checkout] | Section 1 |
| D19-18 | 514 | Do not launch a governed pipeline advertised as protected when accepted L2 is absent | [CODE-CONTRADICTED] | ow:1311-1312 then publish/launch continues (1315-1388); REMEDY ow:789-792 "the agent was started"; comment ow:794-795. Mitigation: the launch does not advertise L2 protection; layer line says "absent ... L1 guard only" (ow:1061-1063). Doc-internal: 19.8 line 574 records the warning choice |
| D19-19 | 514 | Ordinary/no-pipeline claim unaffected | [CODE-VERIFIED] | `l2_status` sole call site ow:1311 inside `cmd_launch`; SKILL.md:150 "no launch is attempted ... for `--pipeline none`" |

### 19.3 Update stream and limits (lines 518-520)

| ID | Design line | Claim (short) | Tag | Evidence |
|---|---|---|---|---|
| D19-20 | 518 | Each stdin record is `<local-ref> <local-oid> <remote-ref> <remote-oid>` | [UNVERIFIED] | Git behaviour; UNVERIFIED-GIT. Only a TEST policy parses it: tests/hooks/test_launch_job_identity.py:1203-1205 |
| D19-21 | 518 | Refuse the entire push, nonzero status, if field 3 is exactly `refs/heads/main` or `refs/heads/master` (create/update/delete/force) | [UNVERIFIED] | No production hook. Git's "nonzero aborts the whole push" is UNVERIFIED-GIT. Test policy compares field 3 exactly (test_launch_job_identity.py:1205) |
| D19-22 | 518 | Zero OIDs and `(delete)` are ordinary Git control values | [UNVERIFIED] | Git behaviour; UNVERIFIED-GIT |
| D19-23 | 518 | Empty stream allows; malformed governed stream refuses with distinct diagnostic | [UNVERIFIED] | No code. Test policy would crash with a ValueError on malformed input, not a distinct diagnostic (test_launch_job_identity.py:1204) |
| D19-24 | 518 | Stream until EOF; no truncation or ref-count inference | [UNVERIFIED] | No code |
| D19-25 | 518 | No hardcoded SHA-1 length needed (SHA-format independence) | [UNVERIFIED] | Git behaviour; UNVERIFIED-GIT |
| D19-26 | 518 | Unselected ordinary pushes allowed without output or stream inspection | [UNVERIFIED] | No code. Test policy reads the stream for every actor (test_launch_job_identity.py:1203) |
| D19-27 | 520 | `refs/tags/main`, `refs/heads/mainline`, `refs/heads/ma`, `refs/heads/feature/main` not protected | [UNVERIFIED] | No code |
| D19-28 | 520 | Mapped source-only refspec resolving to protected heads is protected because field 3 is authoritative | [UNVERIFIED] | Git behaviour; UNVERIFIED-GIT |
| D19-29 | 520 | L2 adds no local commit/merge restriction and does not know the correct remote | [UNVERIFIED] | No L2 code |
| D19-30 | 520 | `--no-verify`, per-process hooksPath overrides, direct send-pack, API/programmatic ref writes bypass local pre-push | [UNVERIFIED] | Git behaviour; UNVERIFIED-GIT |
| D19-31 | 520 | Visible bypass forms remain checked by L1 | [CODE-VERIFIED] (partial) | llg:528 classes `push|send-pack|http-push` as PUSH; llg:532 classes `hookspath`, `alias.`, `pushurl`, `insteadof`, `set-url` as UNKNOWN. Whether every API/MCP ref write is covered was not traced (PreToolUse matcher includes `mcp__.*(...update_ref|create_ref...)`, src/superclaude/hooks/hooks.json:116) |
| D19-32 | 520 | Same-user modification, detachment remain limitations; no universal AC-6 or hostile sandbox | [CODE-VERIFIED] (disclaimer) | jid:2, jid:7-9 |

### 19.4 Release and removal (lines 524-526)

| ID | Design line | Claim (short) | Tag | Evidence |
|---|---|---|---|---|
| D19-33 | 524 | Private-worktree eligibility data may disappear with Git worktree removal; Q artifacts report that Git behaviour | [UNVERIFIED: source artifact absent from checkout] | Section 1; also UNVERIFIED-GIT |
| D19-34 | 524 | Actual Orca removal remains unverified | [UNVERIFIED] | Self-declared |
| D19-35 | 524 | Shared hook file may remain installed and inert; not all L2 files vanish with one worktree | [UNVERIFIED] | No hook. Supporting observation: a linked worktree's hook path resolves to the common dir (section 2 table), so a default-lookup hook would be shared |
| D19-36 | 526 | Deleting level/approval files is the release route and invalidates L2 membership | [CODE-VERIFIED] (job identity side only) | Release instruction ow:1053-1060 (`rm sessions/<id>` and `.ok`); `identify()` returns `ordinary`/`released` when the governed record is gone, jid:238-241. No L2 consumer exists |
| D19-37 | 526 | Retained marker must not restrict humans; no marker-lift or config-unset command | [CODE-VERIFIED] (absence) | No worktree marker is written by ow (Grep `marker` in ow: only unrelated hits at 359-381, 730, and the comment at 1308); no config-unset code |
| D19-38 | 526 | Re-add/rename, stale records, concurrent sessions in lifecycle tests; renames keep identity | [UNVERIFIED] | No L2 tests |
| D19-39 | 526 | No whole shared-hook deletion during single-session release | [CODE-VERIFIED] (absence) | No code deletes git hooks; ow unlink calls are temp files (181, 1093) and the pending record on a failed launch (1337) |

### 19.5 Tests and observed checks (lines 530-534)

| ID | Design line | Claim (short) | Tag | Evidence |
|---|---|---|---|---|
| D19-40 | 530 | Tests use production installation, real Git, pytest temp bare remote, clone and linked worktrees; assert hook evidence and before/after remote refs | [UNVERIFIED] | No production installation exists. Closest: `LocalPushFixture` (tests/hooks/test_launch_job_identity.py:1175-1232), self-labelled "Disposable TEST POLICY, not the production O-22 pre-push installation"; bare remote + clone, writes `.git/hooks/pre-push` directly (1214-1232), evidence log 1182, remote ref read 1255-1259 |
| D19-41 | 530 | Coverage list: create/update/delete/force, refspec, mapped source-only, mixed (protected last), empty, SHA-format, exact-name edges, bypasses | [UNVERIFIED] | No L2 tests; git parts UNVERIFIED-GIT |
| D19-42 | 530 | Synthetic direct-hook inputs only for malformed/padded records Git does not send | [UNVERIFIED] | No tests; "Git does not normally send" is UNVERIFIED-GIT |
| D19-43 | 532 | Actor cases (same worktree agent+human, ordinary session, main, sibling, nested, release/resume/clear, stale PID, unreadable ancestry) | [UNVERIFIED] | No L2 tests |
| D19-44 | 532 | Text-layer leaks marked separately from combined L1+L2 results | [UNVERIFIED] | No L2 tests |
| D19-45 | 534 | OB-H3 uses a real claim's installation and a disposable local bare destination, never a real origin | [UNVERIFIED] | OB-H3 not run (design 576) |
| D19-46 | 534 | Check effective hook presence/executable ownership and process membership | [UNVERIFIED] | Observation requirement. `l2_status` covers presence + executable only, not ownership or membership (ow:1025-1029) |
| D19-47 | 534 | Fixture refs must actually reach pre-push (not up-to-date / non-fast-forward rejection) | [UNVERIFIED] | Git behaviour (rejection before pre-push); UNVERIFIED-GIT |
| D19-48 | 534 | Dry-run supplements, does not replace ref-state assertions; Git documents dry-run as not sending updates | [UNVERIFIED] | Git behaviour; UNVERIFIED-GIT |
| D19-49 | 534 | Q artifacts report local hook invocation | [UNVERIFIED: source artifact absent from checkout] | Section 1 |
| D19-50 | 534 | No transport-specific proof for the real fork claimed | [UNVERIFIED] | Disclaimer; nothing to check |

### 19.6 Provenance (lines 538-545)

| ID | Design line | Claim (short) | Tag | Evidence |
|---|---|---|---|---|
| D19-51 | 538 | Auggie unavailable; codegraph/native tools used | [UNVERIFIED] | Historical process statement |
| D19-52 | 538 | Sibling `adversarial/return-contract.yaml` files exist | [UNVERIFIED: source artifact absent from checkout] | Section 1 |
| D19-53 | 540 | q1 run-4 `merged-answer.md`: partial, marker-only isolation insufficient | [UNVERIFIED: source artifact absent from checkout] | Section 1 |
| D19-54 | 541 | q2 run-4 `merged-q2-answer.md`: shared-path branch only, no forwarding/stubs | [UNVERIFIED: source artifact absent from checkout] | Section 1 |
| D19-55 | 542 | q3 run-4 `merged-answer.md`: worktree cleanup useful, retained human restriction rejected | [UNVERIFIED: source artifact absent from checkout] | Section 1 |
| D19-56 | 543 | q4 run-4 `answer-merged.md`: success label, local fixture target chosen | [UNVERIFIED: source artifact absent from checkout] | Section 1 |
| D19-57 | 545 | Measurements are historical; panel did not rerun them; official refs establish protocol semantics, not runtime proof | [UNVERIFIED] | Disclaimer; the four reference URLs were not fetched in this pass |

### 19.7 Scoped job identity foundation (lines 549-565)

| ID | Design line | Claim (short) | Tag | Evidence |
|---|---|---|---|---|
| D19-58 | 549 | Implementation is `launch-job-identity.sh`, byte-identical plugin mirror, installer distribution | [CODE-VERIFIED] | File exists; `cmp` src vs `plugins/superclaude/hooks/scripts/launch-job-identity.sh` rc=0; ih:90 |
| D19-59 | 549 | Stdlib Python body runs through UV on Linux | [CODE-VERIFIED] | jid:566 `exec uv run --no-project python -I -c ...`; Linux check jid:461-462 |
| D19-60 | 549 | Tests in `tests/hooks/test_launch_job_identity.py`; installer coverage in `tests/cli/test_install_hooks.py` | [CODE-VERIFIED] | Both files exist; Grep counts 15 mentions of the launch scripts in test_install_hooks.py |
| D19-61 | 551 | Adapter acts only for a governed session; copies `tool_input`, changes only `command`, returns `updatedInput` without `permissionDecision` | [CODE-VERIFIED] | jid:442 `governed(root, sid)`; jid:477-481; header jid:14-15 |
| D19-62 | 551 | Ordinary and non-Bash events unchanged | [CODE-VERIFIED] | Early exit with no store jid:20-23; registration matcher `Bash` src/superclaude/hooks/hooks.json:126; a bound non-Bash event is refused, not rewritten (jid:444-445, 484-486) |
| D19-63 | 553 | PreToolUse creates no ticket; emits `execute SESSION TOOL_ID COMMAND`; `execute` creates and consumes the request | [CODE-VERIFIED] | jid:473-476, 492-511 |
| D19-64 | 553 | `prepare` and `run` remain explicit caller APIs | [CODE-VERIFIED] | jid:538-555 |
| D19-65 | 555 | Supervisor per kernel session, subreaper, waits for descendants, preserves exit status | [CODE-VERIFIED] (partial) | Header jid:3-5; subreaper jid:294, 466-468. Wait loop and stdio preservation not traced in this pass |
| D19-66 | 557 | `identify [PID]` emits governed/ordinary/unknown; release by deleting origin's record | [CODE-VERIFIED] | jid:215-244, 530-537 |
| D19-67 | 559 | Fresh Bash shell; `cd` does not persist; `setsid` escapes | [CODE-VERIFIED] | jid:475 `/bin/bash`; header jid:7-9, 16-17 |
| D19-68 | 561 | UV absent: jq may establish an exact bound session and block; ordinary calls silent | [CODE-VERIFIED] | jid:25-53 |
| D19-69 | 561 | Future governed launcher must check these prerequisites | [CODE-VERIFIED] | ow:929-938 (jq, uv, guard commands, process interfaces via `process_interface_gaps` ow:841-871), ow:1001-1008 (identity registration) |
| D19-70 | 563 | `TASK-WF-authorizedNarrow-20261106-214325` retains `artifacts/live-harness-events.jsonl` | [CODE-VERIFIED] (existence only) | `.dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/artifacts/live-harness-events.jsonl` exists (in `done/`); content not read |
| D19-71 | 565 | This increment does not implement production pre-push install/release policy | [CODE-VERIFIED] (absence) | Section 4 |

### 19.8 Implementation status (lines 569-578)

| ID | Design line | Claim (short) | Tag | Evidence |
|---|---|---|---|---|
| D19-72 | 571 | L1 guard `launch-level-guard.sh` with byte-identical plugin copy | [CODE-VERIFIED] | `cmp` src vs plugin rc=0. Exit 0/2 semantics not traced here |
| D19-73 | 572 | Two registrations (UserPromptSubmit, PreToolUse with section 13 matcher) in both hooks.json files | [CODE-VERIFIED] | src hooks.json: UserPromptSubmit block from 44, guard at 67; PreToolUse from 84, guard at 120 with matcher at 116. Plugin hooks.json: UserPromptSubmit 34/guard 48; PreToolUse 54/guard 90, identity 100 |
| D19-74 | 573 | Installer entry `"launch-level-guard.sh"` in `_FRESHNESS_SCRIPTS` | [CODE-VERIFIED] | ih:93 |
| D19-75 | 574 | IR-1/IR-2: pending launch record and prompt mark | [CODE-VERIFIED] | `PENDING_PARTS` ow:772; `publish_pending` ow:1071; prompt mark ow:1333 |
| D19-76 | 574 | IR-4 read-only preflight refuses with `W-ENFORCEMENT-ABSENT`; no agent starts, no record written | [CODE-VERIFIED] | ow:919-1009; ow:1282-1304 (order comment and refusal before `publish_pending`) |
| D19-77 | 574 | IR-5: new session and nonce per claim | [CODE-VERIFIED] (nonce part) | `publish_pending` returns a fresh nonce, ow:1315; "new session" not traced |
| D19-78 | 574 | IR-6: release instruction and L1/L2 status lines | [CODE-VERIFIED] | `session_report` ow:1032-1068 |
| D19-79 | 574 | IR-7 as warning `W-L2-ABSENT`; launch continues; owner had not answered | [CODE-VERIFIED] | ow:789-799, 1307-1312, 1376-1385. Conflicts with design 514 and IR-7 at line 355 (doc-internal) |
| D19-80 | 574 | IR-3 documentation only; no code writes `pipeline.json` | [CODE-VERIFIED] | Grep `pipeline\.json` in ow: no match |
| D19-81 | 576 | L2 layer of 19.2-19.5 pending, needs its own plan after B-CTX | [CODE-VERIFIED] (absence) | Section 4 |
| D19-82 | 576 | No governed claim used on a real issue until OB-H1 item 1, OB-H2, OB-H3 pass | [UNVERIFIED] | Process rule; no code gate found (cmd_launch has no OB check) |
| D19-83 | 578 | Pending launch records are not pruned | [CODE-VERIFIED] | The only `pending.unlink` is on a failed `orca agent launch`, ow:1337 |

**Key Takeaways**

- 83 statements: the L2-specific contract (19.2-19.5) is almost entirely [UNVERIFIED] because no L2 code exists; the 19.7/19.8 foundation statements are largely [CODE-VERIFIED].
- Two [CODE-CONTRADICTED]: D19-16 (a foreign hook is silent, not `W-L2-ABSENT`) and D19-18 (the governed launch proceeds when L2 is absent). D19-18 is a deliberate, documented divergence (ow:794-795, design 574), not drift.

---

## Gaps and Questions

### Git-behaviour claims for the experiment cross-check

- UNVERIFIED-GIT D19-2 (design line 493): git's pre-push hook receives only the remote name and location as arguments and ref-update records on stdin; no Claude session id.
- UNVERIFIED-GIT D19-20 (design line 518): each stdin record is `<local-ref> <local-oid> <remote-ref> <remote-oid>`, space separated, one per line.
- UNVERIFIED-GIT D19-21 (design line 518): a nonzero pre-push exit refuses the entire push (no ref is updated, including unprotected refs in the same push), for create, update, delete and force forms.
- UNVERIFIED-GIT D19-22 (design line 518): zero OIDs (create/delete) and `(delete)` as local ref are the normal values git sends.
- UNVERIFIED-GIT D19-23 (design line 518): an empty stdin stream occurs (for example nothing to push) and is a valid input.
- UNVERIFIED-GIT D19-25 (design line 518): destination selection needs no hardcoded SHA-1 length (SHA-256 repositories send longer OIDs).
- UNVERIFIED-GIT D19-28 (design line 520): a source-only or configured (`remote.<n>.push`, `push.default`) refspec that maps to `refs/heads/main|master` appears as field 3 = that protected ref.
- UNVERIFIED-GIT D19-30 (design line 520): `--no-verify`, a per-process `-c core.hooksPath=...` override, direct `git send-pack`, and API/programmatic ref writes bypass the local pre-push hook.
- UNVERIFIED-GIT D19-33 (design line 524): private-worktree data (per-worktree git dir content) disappears with `git worktree remove`.
- UNVERIFIED-GIT D19-35 (design line 524): a linked worktree's default hook lookup is the shared common git dir (observed once locally with git 2.47.3, see section 2, but not proven in general).
- UNVERIFIED-GIT D19-42 (design line 530): git does not normally send malformed or padded records.
- UNVERIFIED-GIT D19-47 (design line 534): an up-to-date ref is not sent to pre-push and a non-fast-forward is rejected before pre-push runs.
- UNVERIFIED-GIT D19-48 (design line 534): `git push --dry-run` sends no updates, yet (per the Q artifacts) still invokes the local pre-push hook.
- UNVERIFIED-GIT D19-41 (design line 530): forced updates, deletes, mixed protected/unprotected pushes and refspec forms all reach pre-push with the expected field-3 values.

### Code contradictions

- D19-16 (line 514): a conflict (foreign executable `pre-push`) yields `present-unverified` with no warning; `W-L2-ABSENT` has one fixed reason and never names "conflict" or "unsupported lookup". Question for the plan: should a future installer add a `W-L2-CONFLICT` (or a reason field) so the design's "report with the reason" holds?
- D19-18 (line 514) and IR-7 (line 355) say refuse the governed launch when accepted L2 is absent; the code launches and warns (ow:1311-1312, 789-799). Design line 574 records the warning choice "the owner had not answered". Question for the owner: once L2 exists, does IR-7 become the refusal (the one-line change is written at ow:1309-1310)?

### Unverified design statements (no code, or source absent)

- Source artifact absent from checkout: D19-10, D19-17, D19-33, D19-49, D19-52, D19-53, D19-54, D19-55, D19-56 (the whole `.dev/brainstorms/20261106-l2-prepush-decisions/` tree is missing; the line-487 corpus `.dev/brainstorms/20261105-170229-launch-level-hook/` is present, see section 1). Question: were these artifacts committed on another branch or never committed?
- No L2 code exists for: D19-1, D19-3, D19-9, D19-13, D19-14, D19-21, D19-23, D19-24, D19-26, D19-27, D19-29, D19-35, D19-38.
- No L2 tests or observations exist for: D19-40, D19-41, D19-43, D19-44, D19-45, D19-46, D19-50.
- Status, process or disclaimer statements not checkable in code: D19-6, D19-34, D19-51, D19-57, D19-82.
- Partial verifications that need a later trace: D19-31 (L1 coverage of every API/MCP ref write), D19-65 (supervisor wait loop and stdio preservation), D19-70 (content of `live-harness-events.jsonl`), D19-72 (guard exit 0/2), D19-77 ("new session per claim").

### Design gaps for an L2 installer

- `l2_status` cannot tell an owned L2 guard from any executable; there is no ownership marker, version line or content hash to check (design 512 requires one).
- `l2_status` folds "git missing", "timeout" and "not a repository" into `absent`; an installer's preflight would want those distinct from "no hook".
- `install_hooks.py` is user-global (`~/.claude`) and has no git-hook path; per-repository installation would need new code, most naturally in `cmd_launch` before the `l2_status` probe (design 565).
- The only real-git pre-push code is a TEST policy (tests/hooks/test_launch_job_identity.py:1175-1232) that crashes on malformed records and inspects the stream for every actor; it is a starting fixture, not the production contract of 19.3.

---

## Stale Documentation Found

- **[STALE DOC]** design section 19.6 (lines 538-543): cites four `.dev/brainstorms/20261106-l2-prepush-decisions/.../run-4/...` files plus `return-contract.yaml` siblings; none exists in this checkout (`git ls-files` lists 0 files under that directory).
- Not stale (corrected in the Gate 1 cycle 0 fix): design line 487's corpus `.dev/brainstorms/20261105-170229-launch-level-hook/` exists and is git-tracked, with every file the line names (section 1). Line 487 itself says those files "have not been synchronized to this refinement", so their content may lag section 19, but the citation resolves.
- **[STALE DOC]** design IR-7 at line 355 ("refuses that governed launch") and section 19.2 line 514 ("do not launch a governed pipeline ... when accepted L2 is absent") describe a refusal; the code and design line 574 implement a warning. Line 355 also says "This is a requested interface, not existing claim capability", which is no longer true: a warning form of IR-7 exists.
- Not stale: the code comment ow:794 says "IR-7 (design section 13)"; IR-7 is at design line 355, inside `## 13. Registration, install and claim-feature interface requests` (lines 337-356), so the reference is accurate.
- Not stale: the `orca_worktree.py` module docstring (ow:45-51), `SKILL.md:150` and section 19.8 all agree with the code on `W-L2-ABSENT` being a non-blocking warning.

---

## Summary

Section 19 holds 83 checkable statements (D19-1 to D19-83). The L2 pre-push layer of 19.2-19.5 does not exist in code: `install_hooks.py` installs only Claude Code hook scripts and `~/.claude/settings.json` registrations and has no git-hook path, and no other source file writes a git hook. The only L2-related code is the read-only `l2_status` probe (ow:1012-1029), which asks git `rev-parse --git-path hooks/pre-push`, joins a relative answer to the worktree, and reports `absent` or `present-unverified` without checking ownership or content; `W-L2-ABSENT` is a non-blocking warning emitted after that probe (ow:1311-1312), contradicting the refusal in design lines 355 and 514 by documented choice. All four 19.6 source artifacts (the `20261106-l2-prepush-decisions/` tree) are absent; the separate line-487 historical corpus `20261105-170229-launch-level-hook/` is present but backs none of the section 19 rows. So placement, removal and dry-run claims that rest on them are unverified, and 14 git-behaviour claims are listed above for the experiment cross-check.
