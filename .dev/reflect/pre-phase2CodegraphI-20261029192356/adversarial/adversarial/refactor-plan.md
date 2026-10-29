# Refactoring Plan: Merge into Base (Variant A)

## Overview
- Base: Variant A (reviewer 1 card, sonnet:analyzer, `variant-1-original.md`)
- Incorporating strengths from: Variant B (reviewer 2 card), the debate rounds, and the Round 2.5 invariant probe (`invariant-probe.md`)
- Planned changes: 19. The target is a merged finding list M-01 to M-19, one entry per distinct defect, in a markdown document.
- Risk level: Medium overall. The merge rewrites the classification of six base findings and the fixes of several.
- Classification rule (applies to every change; both advocates REJECTed A-002):
  - **drift** = a plan-made divergence from the spec.
  - **necessary** = a defect copied verbatim from the spec (origin `inherited-from-spec`). Its fix departs from the spec text.
  - **authorized** = a plan addition backed by a spec or plan rule, even when its form is defective.
  - Reflect-artifact errors are labelled drift with origin `reflect-artifact`.
- Calibration rule (from the team lead):
  - Findings rated **wrong** are dropped. None were.
  - Findings rated **overstated** are kept at minor only: R1-06, R1-11, P2R2-6.
- Every merged entry carries: id, sources, class, origin, severity, plan_ref, spec_ref, claim, fix.

## Planned Changes

### Change 1: M-01 plan:48 `.claude/` guard (base R1-01, merged with P2R2-7)
- **Source**: Base R1-01; Variant B P2R2-7 (Task 1 part); debate X-001 and A-001; INV-019 (fix verified)
- **Target**: Merged finding M-01 (restructure)
- **Rationale**: X-001 won by A at 97%. Resolution of the open disagreement: R1-01 is right about the mechanism, and P2R2-7 is right that the addition is authorized. P2R2-7's "fix: None" is wrong.
- **Content**:
  - class authorized; origin plan; severity important
  - plan_ref "plan:48; plan:21"; spec_ref "source.md:436; source.md:440-442; source.md:445; source.md:755"
  - Claim:
    - The guard implements the §7 hard rule (source.md:755, plan:23) but is not in the spec's T0 acceptance (source.md:440-442).
    - As written, `git diff --name-only HEAD~1 HEAD | rg '^\.claude/' | rg -v '^\.claude/settings\.json$'` exits 1 under pipefail on a clean commit and on a settings.json-only commit, and exits 0 when it prints a violation (orchestrator run). It contradicts plan:21.
    - The `test -z "$(pipeline)"` repair in R1-01 passes vacuously when `HEAD~1` cannot resolve (Round 2, both advocates).
  - Fix (one fenced block, both lines in the same shell):
    - `git diff --name-only HEAD~1 HEAD > /tmp/p2-t1-files.txt`
    - `if rg '^\.claude/' /tmp/p2-t1-files.txt | rg -v '^\.claude/settings\.json$'; then exit 1; fi`
- **Risk**: Low

### Change 2: M-02 Task 16 scope checks abort the exit-0 block (base R1-02, merged with P2R2-1)
- **Source**: R1-02; P2R2-1; advocate A Round 1 concession 10 and Round 2 New evidence 2; advocate B Round 2 item 7; INV-001 to INV-005
- **Target**: Merged finding M-02 (restructure)
- **Rationale**: C-001 was won by A at 95%; A-002 makes it inherited. INV-001 (HIGH) shows that the consensus `|| echo` fix would pass Task 16 with a kept user-scope entry.
- **Content**:
  - class necessary; origin inherited-from-spec; severity important
  - plan_ref "plan:275-286 (plan:277, 278, 286); plan:27"; spec_ref "source.md:197; source.md:209-211; source.md:705; source.md:709-716; source.md:757-765"
  - Claim:
    - The user-scope (plan:277) and local-scope (plan:278) `jq -e` lines open the exit-0 block, which is copied from source.md:709-716. A hit aborts lines 279-284, so the registration, version, `mcp get`, `--list` and doctor outputs that the G6 comment needs are lost.
    - A local-scope hit is a user action, not a plan failure (plan:286, source.md:211).
    - A user-scope failure from a kept entry keeps T12 open until the user acts (source.md:210, 705). But no human item covers it (plan:27, source.md:757-765), and the executor cannot see the retire step's printed commands, which were shown in the human's `./update.sh` terminal.
  - Fix:
    - (a) Run each scope check as a recorded line: `rc=0; jq -e '<filter>' ~/.claude.json || rc=$?`, then save rc to `/tmp/p2-t16-us.rc` (user) or `/tmp/p2-t16-ls.rc` (local), then `test "$rc" -le 1`. rc 1 means a hit. A missing or corrupt file (rc 2 or 5) still fails.
    - (b) Add read-only `jq` lines that print `claude mcp remove <key> --scope user` for each offending user-scope key, and `cd <project-key> && claude mcp remove <name> --scope local` for each local hit. Put these in the G6 comment.
    - (c) End the block with `test "$(cat /tmp/p2-t16-us.rc)" -eq 0`. User scope stays gating; local scope stays report-only.
    - (d) Add a seventh, non-blocking human item: the user runs the printed user-scope command. Task 16 stays open and is reported in G6.
- **Risk**: Medium (block rewrite)

### Change 3: M-03 `$E` undefined in Task 5 (base R1-03, merged with P2R2-2)
- **Source**: R1-03; P2R2-2; X-002 (B 95%); INV-023
- **Target**: M-03 (modify; class necessary → drift)
- **Content**:
  - class drift; origin plan; severity minor
  - plan_ref "plan:107"; spec_ref "source.md:533-534; source.md:540"
  - Claim: plan:107 uses `$E`, which only source.md:534 defines. The plan dropped the definition, and under `set -u` the line aborts on an unbound variable.
  - Fix (one fenced block):
    - `MT=$(sed -n 's/^Selected MCP_TOOLS: //p' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md); test -n "$MT"`
    - `E=$(jq -cn --arg t "$MT" …)` exactly as source.md:534
    - `jq -e --argjson e "$E" '. == $e' .dev/codegraph-migration/evidence/P2-add-json-shape.json`
- **Risk**: Low

### Change 4: M-04 `./artifacts/` paths resolve to the never-staged project root (split from base R1-04, merged with P2R2-4)
- **Source**: R1-04 (path part); P2R2-4; C-004 (B 95%); X-003 (A 92%); INV-008; INV-009
- **Target**: M-04 (new entry from split)
- **Content**:
  - class drift; origin plan; severity important (minor for the prose-only refs at plan:79 and plan:237)
  - plan_ref "plan:79, 85, 237, 253, 272, 287; plan:24"; spec_ref "none (the spec has no ./artifacts paths); user rule: the project-root artifacts/ is never staged"
  - Claim:
    - Blocks run from the repo root, so `./artifacts/...` resolves to the project-root `artifacts/` instead of the package's `artifacts/` that plan:24 stages.
    - The package folder has no `artifacts/` directory yet (verified), so a copy into it fails under `-e`.
    - Task 3's client runs from `$W/repo`, which is deleted (source.md:527), so relative outputs are lost.
  - Fix:
    - Use the literal path `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/artifacts/<file>` in each block, not a Constraints `$ART`, which is unbound in separate blocks.
    - `mkdir -p` that directory in Task 3 and Task 14.
    - Task 3 captures the absolute worktree root before entering `$W` and writes `t3-run1.json` and `t3-run2.json` there before `rm -rf "$W"`.
- **Risk**: Low

### Change 5: M-05 Task 14 never writes its required evidence files (split from base R1-04)
- **Source**: R1-04 (Task 14 part); X-004 (A 93%); INV-007; INV-010
- **Target**: M-05 (new entry from split)
- **Content**:
  - class drift; origin plan; severity important
  - plan_ref "plan:237; plan:242-253; plan:259"; spec_ref "source.md:669-684"
  - Claim:
    - The block writes only `/tmp`, but plan:253 requires `t14-final-run.txt` and `t14-new-failures.txt` under artifacts.
    - Copy lines added after plan:247 never run when the gate fails. A failing plan:247 also skips the plan:248 `perf.json` restore.
    - Task 14 commits only when a fix was needed, so its staged evidence blocks Task 15's `rebase onto origin/master`.
  - Fix:
    - Copy `/tmp/p2-final-run.txt` right after plan:243, and `/tmp/p2-new-failures.txt` right after plan:246, into the package artifacts path.
    - Move the `perf.json` restore ahead of `test ! -s`.
    - Always commit the Task 14 evidence (for example `test(codegraph): record final gate evidence`).
- **Risk**: Low

### Change 6: M-06 Task 3 real-hash criterion has no before-hash (split from base R1-04, merged with P2R2-3)
- **Source**: R1-04 (hash part); P2R2-3; C-002 (B 93%); INV-012; INV-013
- **Target**: M-06 (new entry; class relabelled authorized per INV-013 for consistency with M-01)
- **Content**:
  - class authorized; origin plan; severity minor
  - plan_ref "plan:86; plan:73-77; plan:23"; spec_ref "source.md:522; source.md:525; source.md:755"
  - Claim:
    - The before/after hash criterion is backed by the §7 hard rule and the Leg B H0/H1 guard, but no step records a before-hash outside Leg B, so the criterion is unverifiable.
    - Task 3 runs as several shell invocations, so a shell variable H0 does not survive to the end.
    - Leg A uses a sandbox HOME, so the real risk is near zero.
  - Fix:
    - First action: `jq -S '.mcpServers' ~/.claude.json | sha256sum > /tmp/p2-t3-h0.txt`.
    - Last line: `test "$(jq -S '.mcpServers' ~/.claude.json | sha256sum)" = "$(cat /tmp/p2-t3-h0.txt)"`.
- **Risk**: Low

### Change 7: M-07 Task 16 writes an in-repository artifact the spec forbids (new)
- **Source**: P2R2-7 calibrator note; shared assumption A-003 (CONTRADICTED); both advocates' A-003 comments; INV-022
- **Target**: M-07 (insert)
- **Content**:
  - class drift; origin plan; severity minor
  - plan_ref "plan:272; plan:287; plan:24"; spec_ref "source.md:706; source.md:719"
  - Claim: Task 16 writes `./artifacts/t16-live-verify.txt`, although T12 is "Files: none in the repository; the outputs go only into the issue-#323 comment". After the merge there is no commit point, so the file would stay untracked, against the always-staged rule.
  - Fix: Write to `/tmp/p2-t16-live-verify.txt`. Paste it, with the M-02 markers, into the G6 comment. Drop the file clause from plan:272 and plan:287.
- **Risk**: Low

### Change 8: M-08 U11 assigned to the wrong task (base R1-05)
- **Source**: R1-05; INV-016
- **Target**: M-08 (modify; origin inherited)
- **Content**:
  - class necessary; origin inherited-from-spec; severity important
  - plan_ref "plan:92; plan:96; plan:104"; spec_ref "source.md:101; source.md:296; source.md:466; source.md:486"
  - Claim: U11 tests the `claude --version` check that source.md:101 places in the phase function Task 5 creates (`install_mcp.py`). Yet Task 4's gate must pass U1-U11 (copied from source.md:466).
  - Fix:
    - Move U11 to Task 5: the plan:92 list, the plan:96 gate ("U1-U10, U20-U22, U24") and plan:104 ("U11-U19, U23, U25").
    - Check whether U22 (source.md:307, "the version dir's launcher is registered") also needs Task 5. UNVERIFIED.
- **Risk**: Low

### Change 9: M-09 `&&` / `!` lines do not gate inside blocks (base R1-07)
- **Source**: R1-07; INV-015; INV-020; orchestrator run
- **Target**: M-09 (modify; class drift → necessary; drop the plan:84 citation; add plan:163 and source.md:602, 637)
- **Content**:
  - class necessary; origin inherited-from-spec; severity important
  - plan_ref "plan:162, 163, 165, 202, 203, 244"; spec_ref "source.md:601, 602, 604, 636, 637, 675; source.md:625"
  - Claim: Under `bash -euo pipefail`, errexit ignores a failing left side of `&&` and any `! cmd` (orchestrator run). These checks therefore do not fail the block mid-way. source.md:625 knows this rule but applies it only to T6.
  - Fix: One condition per line. Write negatives as `if cmd; then exit 1; fi`. Keep the positive grep before its negative.
- **Risk**: Low

### Change 10: M-10 `uv run --no-project` yaml import (base R1-08)
- **Source**: R1-08; INV-014
- **Target**: M-10 (modify; origin inherited; claim narrowed)
- **Content**:
  - class necessary; origin inherited-from-spec; severity minor
  - plan_ref "plan:216"; spec_ref "source.md:649-651"
  - Claim: pyyaml is a project dependency (pyproject.toml). The probe found that `--no-project` still works in this checkout because uv finds `.venv`, so it fails only where no `.venv` exists.
  - Fix (optional): make `uv run python -c …` the primary command.
- **Risk**: Low

### Change 11: M-11 `grep -i connected` matches "Disconnected" (base R1-09)
- **Source**: R1-09; INV-024
- **Target**: M-11 (keep)
- **Content**:
  - class necessary; origin inherited-from-spec; severity minor
  - plan_ref "plan:282"; spec_ref "source.md:714; source.md:374-375"
  - Fix: After the positive grep, add `if grep -iE 'disconnected|not connected|failed' /tmp/p2-t12-get.txt; then exit 1; fi`, as in layer 2 step 5.
- **Risk**: Low

### Change 12: M-12 Task 2 drops the T0b coordinator report (base R1-10)
- **Source**: R1-10
- **Target**: M-12 (keep)
- **Content**:
  - class drift; origin plan; severity minor
  - plan_ref "plan:54"; spec_ref "source.md:448"
  - Fix: The Task 2 completion message states whether Phase 1 already carried the amendments or this task made them.
- **Risk**: Low

### Change 13: M-13 Task 6 `--list` Ready line depends on Task 7 (base R1-06, overstated)
- **Source**: R1-06 (calibrator: overstated)
- **Target**: M-13 (keep at minor; class necessary, origin inherited)
- **Content**:
  - class necessary; origin inherited-from-spec; severity minor
  - plan_ref "plan:120; plan:125; plan:131"; spec_ref "source.md:142; source.md:561-563; source.md:573"
  - Claim: The §2.8 block includes the "Ready for Serena retirement" line, which needs `codegraph_ready()` from Task 7. Task 6's acceptance does not check that line, so this is an ordering ambiguity only.
  - Fix: Task 6 states that the Ready line lands in Task 7, and Task 7's acceptance checks it.
- **Risk**: Low

### Change 14: M-14 Task 13 sandbox fallback only by reference (base R1-11, overstated)
- **Source**: R1-11 (calibrator: overstated)
- **Target**: M-14 (keep at minor)
- **Content**:
  - class drift; origin plan; severity minor
  - plan_ref "plan:223-227"; spec_ref "source.md:416"
  - Claim: The §4.2 Notes fallback for `claude mcp get` is included only through plan:19 and plan:223.
  - Fix: One sentence naming the fallback (stdio `initialize` + `tools/list`, `serverInfo.name == codegraph`), recorded in `P2-layer2.md`.
- **Risk**: Low

### Change 15: M-15 T1 coverage-matrix false attributions (from Variant B P2R2-5)
- **Source**: P2R2-5 with the calibrator's U23 correction; C-003 (B 90%)
- **Target**: M-15 (insert)
- **Content**:
  - class drift; origin reflect-artifact; severity minor
  - plan_ref "artifacts/coverage-matrix.yaml:319-325; artifacts/coverage-matrix.yaml:454-461"; spec_ref "source.md:289; source.md:308"
  - Claim: INF-037 (U4) is matched to Task 7, and INF-056 (U23) is matched to Task 3. The true carriers are Task 4 and Task 5. No requirement is lost.
  - Fix: Correct `matched_task_ids` (INF-037 → Task 4, INF-056 → Task 5).
- **Risk**: Low

### Change 16: M-16 T1 coverage-matrix under-sampling (from Variant B P2R2-6, overstated)
- **Source**: P2R2-6 (calibrator: overstated)
- **Target**: M-16 (insert at minor)
- **Content**:
  - class drift; origin reflect-artifact; severity minor
  - plan_ref "artifacts/coverage-matrix.yaml"; spec_ref "source.md:59-193, 216-234, 254-272, 323-418, 727-741 (§6 has INF-093 and §8 has INF-104)"
  - Fix: Annotate the T1 card that these spans have no matrix rows, and that their coverage rests on the by-reference triage.
- **Risk**: Low

### Change 17: M-17 Task 2 "commit only if a file changed" (from Variant B P2R2-7)
- **Source**: P2R2-7; INV-018
- **Target**: M-17 (insert)
- **Content**:
  - class authorized; origin plan; severity minor
  - plan_ref "plan:54"; spec_ref "source.md:459"
  - Claim: The conditional commit is an authorized addition, because it avoids an empty commit. But with `.dev/tasks` always staged, a ledger-only change satisfies "a file changed".
  - Fix: The condition names `phase-1-removal-spec.md` or the facts file.
- **Risk**: Low

### Change 18: M-18 Task 7 retire-test selector can be empty (new; INV-006 HIGH)
- **Source**: reviewer 1 calibrator `extra_risk`; INV-006; orchestrator check (`rg -l install_retired_mcp tests` rc 1, `install_retired_mcp.py` absent, pyproject.toml:108 `testpaths = ["tests"]`)
- **Target**: M-18 (insert)
- **Content**:
  - class necessary; origin inherited-from-spec; severity important
  - plan_ref "plan:131; plan:134-135"; spec_ref "source.md:572; source.md:576-577"
  - Claim: If `$(rg -l install_retired_mcp tests)` is empty (true in this checkout today), plan:134 runs only the other two files, and plan:135 runs the whole suite with `-k "codegraph and serena"`. That is a false pass on the Serena-retirement gate.
  - Fix:
    - `F=$(rg -l -g '*.py' install_retired_mcp tests)` (the assignment aborts under `-e` when nothing matches)
    - `test -n "$F"`
    - `uv run pytest $F …`
- **Risk**: Low

### Change 19: M-19 Acceptance checks that pass vacuously (new; INV-011, INV-017)
- **Source**: INV-011; INV-017
- **Target**: M-19 (insert)
- **Content**:
  - class necessary; origin inherited-from-spec; severity minor
  - plan_ref "plan:21; plan:167; plan:217; plan:228"; spec_ref "source.md:606; source.md:661"
  - Claim:
    - `test -z "$(comm -13 <baseline> <fail>)"` (plan:167) passes if the baseline is missing.
    - `tail -1 … P2-layer2.md` (plan:228) exits 0 whatever the last line is.
    - `rg -n codegraph` (plan:217, plan-added) passes on any mention.
  - Fix:
    - plan:21 says acceptance commands "exit 0 if and only if the criterion passes".
    - plan:167 becomes `comm -13 … > /tmp/p2-t5-new.txt` followed by `test ! -s /tmp/p2-t5-new.txt`.
    - plan:228 becomes `test "$(tail -1 .dev/codegraph-migration/evidence/P2-layer2.md)" = LAYER2_OK`.
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| X-001 | P2R2-7: plan:48 is benign, fix "None" | Exit status inverted (orchestrator run plus both advocates); B conceded in Round 1 |
| C-001 | P2R2-1: record the local-scope command in the t16 artifact | source.md:706 forbids in-repo files for T12; B withdrew this in Round 2 |
| A-002 | Both cards' "drift" for verbatim spec copies (R1-02, R1-07, P2R2-1) | Both advocates REJECTed A-002; these become necessary/inherited |
| C-004 | Base R1-04: `ART=` defined once in Constraints | Unbound in separately run `-euo pipefail` blocks (source.md:445); base conceded |
| X-001 fix | Base R1-01: `test -z "$(pipeline)"` | Passes vacuously when `git diff HEAD~1` cannot run (Round 2 New evidence 1) |
| A-001 | Advocate B Round 1: write every "prints nothing" bullet as `test -z "$(…)"` | Withdrawn in Round 2; replaced by the file-first or if-form rule and M-19 |
| plan:277 | Advocate A Round 1: exempt user scope like local scope | Withdrawn in Round 2: source.md:210 and :705 keep T12 open for user scope |
| plan:84 | Base R1-07 citation of plan:84 | Standalone bullet; `A && B` gates on its own (calibrator, both advocates) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | plan:48 fix unsound | Revert to R1-01 wording with the vacuous-pass caveat |
| 2 | Medium | Task 16 block rewrite could leave a gating gap | Revert to the C-001 consensus (report-only) and keep INV-001 open |
| 3-19 | Low | Additive or relabel only | Remove the inserted entry or restore the base label |

## Review Status
- [x] Auto-approved (default; non-interactive)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-10-29T20:40:00Z
