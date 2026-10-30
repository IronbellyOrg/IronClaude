<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A (sonnet:analyzer) -->
<!-- Merge date: 2026-10-29T20:21:08Z -->

# Merged Reviewer Findings: Phase 2 plan (issue #323)

<!-- Source: refactor-plan.md, Overview (classification rule) -->
## Classification rule

These rules apply to every change. Both advocates REJECTed A-002.

- **drift** = a plan-made divergence from the spec.
- **necessary** = a defect copied verbatim from the spec (origin `inherited-from-spec`). Its fix departs from the spec text.
- **authorized** = a plan addition backed by a spec or plan rule, even when its form is defective.
- Reflect-artifact errors are labelled drift with origin `reflect-artifact`.

Calibration rule (from the team lead):

- Findings rated **wrong** are dropped. None were.
- Findings rated **overstated** are kept at minor only: R1-06, R1-11, P2R2-6.

Every merged entry carries: id, sources, class, origin, severity, plan_ref, spec_ref, claim, fix.

## Findings

### M-01 plan:48 `.claude/` guard

<!-- Source: Base R1-01 (original, modified) + Variant B P2R2-7 (Task 1 part); debate X-001, A-001; INV-019 — merged per Change #1 -->
```yaml
id: M-01
sources:
  - R1-01
  - P2R2-7 (Task 1 part)
  - X-001
  - A-001
  - INV-019
class: authorized
origin: plan
severity: important
plan_ref: "plan:48; plan:21"
spec_ref: "source.md:436; source.md:440-442; source.md:445; source.md:755"
claim: |-
  - The guard implements the §7 hard rule (source.md:755, plan:23) but is not in the spec's T0 acceptance (source.md:440-442).
  - As written, `git diff --name-only HEAD~1 HEAD | rg '^\.claude/' | rg -v '^\.claude/settings\.json$'` exits 1 under pipefail on a clean commit and on a settings.json-only commit, and exits 0 when it prints a violation (orchestrator run). It contradicts plan:21.
  - The `test -z "$(pipeline)"` repair in R1-01 passes vacuously when `HEAD~1` cannot resolve (Round 2, both advocates).
fix: |-
  One fenced block, both lines in the same shell:
    git diff --name-only HEAD~1 HEAD > /tmp/p2-t1-files.txt
    if rg '^\.claude/' /tmp/p2-t1-files.txt | rg -v '^\.claude/settings\.json$'; then exit 1; fi
```

### M-02 Task 16 scope checks abort the exit-0 block

<!-- Source: Base R1-02 (original, modified) + Variant B P2R2-1; advocate A Round 1 concession 10 and Round 2 New evidence 2; advocate B Round 2 item 7; INV-001 to INV-005 — merged per Change #2 -->
```yaml
id: M-02
sources:
  - R1-02
  - P2R2-1
  - advocate A Round 1 concession 10
  - advocate A Round 2 New evidence 2
  - advocate B Round 2 item 7
  - INV-001
  - INV-002
  - INV-003
  - INV-004
  - INV-005
class: necessary
origin: inherited-from-spec
severity: important
plan_ref: "plan:275-286 (plan:277, 278, 286); plan:27"
spec_ref: "source.md:197; source.md:209-211; source.md:705; source.md:709-716; source.md:757-765"
claim: |-
  - The user-scope (plan:277) and local-scope (plan:278) `jq -e` lines open the exit-0 block, which is copied from source.md:709-716. A hit aborts lines 279-284, so the registration, version, `mcp get`, `--list` and doctor outputs that the G6 comment needs are lost.
  - A local-scope hit is a user action, not a plan failure (plan:286, source.md:211).
  - A user-scope failure from a kept entry keeps T12 open until the user acts (source.md:210, 705). But no human item covers it (plan:27, source.md:757-765), and the executor cannot see the retire step's printed commands, which were shown in the human's `./update.sh` terminal.
fix: |-
  (a) Run each scope check as a recorded line: `rc=0; jq -e '<filter>' ~/.claude.json || rc=$?`, then save rc to `/tmp/p2-t16-us.rc` (user) or `/tmp/p2-t16-ls.rc` (local), then `test "$rc" -le 1`. rc 1 means a hit. A missing or corrupt file (rc 2 or 5) still fails.
  (b) Add read-only `jq` lines that print `claude mcp remove <key> --scope user` for each offending user-scope key, and `cd <project-key> && claude mcp remove <name> --scope local` for each local hit. Put these in the G6 comment.
  (c) End the block with `test "$(cat /tmp/p2-t16-us.rc)" -eq 0`. User scope stays gating; local scope stays report-only.
  (d) Add a seventh, non-blocking human item: the user runs the printed user-scope command. Task 16 stays open and is reported in G6.
```

### M-03 `$E` undefined in Task 5

<!-- Source: Base R1-03 (original, modified: class necessary → drift) + Variant B P2R2-2; debate X-002; INV-023 — merged per Change #3 -->
```yaml
id: M-03
sources:
  - R1-03
  - P2R2-2
  - X-002
  - INV-023
class: drift
origin: plan
severity: minor
plan_ref: "plan:107"
spec_ref: "source.md:533-534; source.md:540"
claim: |-
  plan:107 uses `$E`, which only source.md:534 defines. The plan dropped the definition, and under `set -u` the line aborts on an unbound variable.
fix: |-
  One fenced block:
    MT=$(sed -n 's/^Selected MCP_TOOLS: //p' .dev/codegraph-migration/evidence/P2-mcp-tools-schema.md); test -n "$MT"
    E=$(jq -cn --arg t "$MT" …)   # exactly as source.md:534
    jq -e --argjson e "$E" '. == $e' .dev/codegraph-migration/evidence/P2-add-json-shape.json
```

### M-04 `./artifacts/` paths resolve to the never-staged project root

<!-- Source: Base R1-04 (path part, split) + Variant B P2R2-4; debate C-004, X-003; INV-008, INV-009 — merged per Change #4 -->
```yaml
id: M-04
sources:
  - R1-04 (path part)
  - P2R2-4
  - C-004
  - X-003
  - INV-008
  - INV-009
class: drift
origin: plan
severity: "important (minor for the prose-only refs at plan:79 and plan:237)"
plan_ref: "plan:79, 85, 237, 253, 272, 287; plan:24"
spec_ref: "none (the spec has no ./artifacts paths); user rule: the project-root artifacts/ is never staged"
claim: |-
  - Blocks run from the repo root, so `./artifacts/...` resolves to the project-root `artifacts/` instead of the package's `artifacts/` that plan:24 stages.
  - The package folder has no `artifacts/` directory yet (verified), so a copy into it fails under `-e`.
  - Task 3's client runs from `$W/repo`, which is deleted (source.md:527), so relative outputs are lost.
fix: |-
  - Use the literal path `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/artifacts/<file>` in each block, not a Constraints `$ART`, which is unbound in separate blocks.
  - `mkdir -p` that directory in Task 3 and Task 14.
  - Task 3 captures the absolute worktree root before entering `$W` and writes `t3-run1.json` and `t3-run2.json` there before `rm -rf "$W"`.
```

### M-05 Task 14 never writes its required evidence files

<!-- Source: Base R1-04 (Task 14 part, split); debate X-004; INV-007, INV-010 — merged per Change #5 -->
```yaml
id: M-05
sources:
  - R1-04 (Task 14 part)
  - X-004
  - INV-007
  - INV-010
class: drift
origin: plan
severity: important
plan_ref: "plan:237; plan:242-253; plan:259"
spec_ref: "source.md:669-684"
claim: |-
  - The block writes only `/tmp`, but plan:253 requires `t14-final-run.txt` and `t14-new-failures.txt` under artifacts.
  - Copy lines added after plan:247 never run when the gate fails. A failing plan:247 also skips the plan:248 `perf.json` restore.
  - Task 14 commits only when a fix was needed, so its staged evidence blocks Task 15's `rebase onto origin/master`.
fix: |-
  - Copy `/tmp/p2-final-run.txt` right after plan:243, and `/tmp/p2-new-failures.txt` right after plan:246, into the package artifacts path.
  - Move the `perf.json` restore ahead of `test ! -s`.
  - Always commit the Task 14 evidence (for example `test(codegraph): record final gate evidence`).
```

### M-06 Task 3 real-hash criterion has no before-hash

<!-- Source: Base R1-04 (hash part, split) + Variant B P2R2-3; debate C-002; INV-012, INV-013 (relabelled authorized) — merged per Change #6 -->
```yaml
id: M-06
sources:
  - R1-04 (hash part)
  - P2R2-3
  - C-002
  - INV-012
  - INV-013
class: authorized
origin: plan
severity: minor
plan_ref: "plan:86; plan:73-77; plan:23"
spec_ref: "source.md:522; source.md:525; source.md:755"
claim: |-
  - The before/after hash criterion is backed by the §7 hard rule and the Leg B H0/H1 guard, but no step records a before-hash outside Leg B, so the criterion is unverifiable.
  - Task 3 runs as several shell invocations, so a shell variable H0 does not survive to the end.
  - Leg A uses a sandbox HOME, so the real risk is near zero.
fix: |-
  - First action: `jq -S '.mcpServers' ~/.claude.json | sha256sum > /tmp/p2-t3-h0.txt`.
  - Last line: `test "$(jq -S '.mcpServers' ~/.claude.json | sha256sum)" = "$(cat /tmp/p2-t3-h0.txt)"`.
```

### M-07 Task 16 writes an in-repository artifact the spec forbids

<!-- Source: Variant B P2R2-7 calibrator note; shared assumption A-003 (CONTRADICTED) and both advocates' A-003 comments; INV-022 — merged per Change #7 -->
```yaml
id: M-07
sources:
  - P2R2-7 (calibrator note)
  - A-003 (CONTRADICTED)
  - advocate A A-003 comment
  - advocate B A-003 comment
  - INV-022
class: drift
origin: plan
severity: minor
plan_ref: "plan:272; plan:287; plan:24"
spec_ref: "source.md:706; source.md:719"
claim: |-
  Task 16 writes `./artifacts/t16-live-verify.txt`, although T12 is "Files: none in the repository; the outputs go only into the issue-#323 comment". After the merge there is no commit point, so the file would stay untracked, against the always-staged rule.
fix: |-
  Write to `/tmp/p2-t16-live-verify.txt`. Paste it, with the M-02 markers, into the G6 comment. Drop the file clause from plan:272 and plan:287.
```

### M-08 U11 assigned to the wrong task

<!-- Source: Base R1-05 (original, modified: origin inherited); INV-016 — merged per Change #8 -->
```yaml
id: M-08
sources:
  - R1-05
  - INV-016
class: necessary
origin: inherited-from-spec
severity: important
plan_ref: "plan:92; plan:96; plan:104"
spec_ref: "source.md:101; source.md:296; source.md:466; source.md:486"
claim: |-
  U11 tests the `claude --version` check that source.md:101 places in the phase function Task 5 creates (`install_mcp.py`). Yet Task 4's gate must pass U1-U11 (copied from source.md:466).
fix: |-
  - Move U11 to Task 5: the plan:92 list, the plan:96 gate ("U1-U10, U20-U22, U24") and plan:104 ("U11-U19, U23, U25").
  - Check whether U22 (source.md:307, "the version dir's launcher is registered") also needs Task 5. UNVERIFIED.
```

### M-09 `&&` / `!` lines do not gate inside blocks

<!-- Source: Base R1-07 (original, modified: class drift → necessary; plan:84 citation dropped; plan:163 and source.md:602, 637 added); INV-015, INV-020; orchestrator run — merged per Change #9 -->
```yaml
id: M-09
sources:
  - R1-07
  - INV-015
  - INV-020
  - orchestrator run
class: necessary
origin: inherited-from-spec
severity: important
plan_ref: "plan:162, 163, 165, 202, 203, 244"
spec_ref: "source.md:601, 602, 604, 636, 637, 675; source.md:625"
claim: |-
  Under `bash -euo pipefail`, errexit ignores a failing left side of `&&` and any `! cmd` (orchestrator run). These checks therefore do not fail the block mid-way. source.md:625 knows this rule but applies it only to T6.
fix: |-
  One condition per line. Write negatives as `if cmd; then exit 1; fi`. Keep the positive grep before its negative.
```

### M-10 `uv run --no-project` yaml import

<!-- Source: Base R1-08 (original, modified: origin inherited; claim narrowed); INV-014 — merged per Change #10 -->
```yaml
id: M-10
sources:
  - R1-08
  - INV-014
class: necessary
origin: inherited-from-spec
severity: minor
plan_ref: "plan:216"
spec_ref: "source.md:649-651"
claim: |-
  pyyaml is a project dependency (pyproject.toml). The probe found that `--no-project` still works in this checkout because uv finds `.venv`, so it fails only where no `.venv` exists.
fix: |-
  Optional: make `uv run python -c …` the primary command.
```

### M-11 `grep -i connected` matches "Disconnected"

<!-- Source: Base R1-09 (original; claim kept verbatim, fix per plan); INV-024 — merged per Change #11 -->
```yaml
id: M-11
sources:
  - R1-09
  - INV-024
class: necessary
origin: inherited-from-spec
severity: minor
plan_ref: "plan:282"
spec_ref: "source.md:714; source.md:374-375"
claim: |-
  `grep -i connected` also matches Disconnected / Not connected; no negative check as in layer 2 step 5.
fix: |-
  After the positive grep, add `if grep -iE 'disconnected|not connected|failed' /tmp/p2-t12-get.txt; then exit 1; fi`, as in layer 2 step 5.
```

### M-12 Task 2 drops the T0b coordinator report

<!-- Source: Base R1-10 (original; claim kept verbatim, fix per plan) — merged per Change #12 -->
```yaml
id: M-12
sources:
  - R1-10
class: drift
origin: plan
severity: minor
plan_ref: "plan:54"
spec_ref: "source.md:448"
claim: |-
  Spec T0b requires the outcome to be reported to the coordinator in the completion message; Task 2 drops it.
fix: |-
  The Task 2 completion message states whether Phase 1 already carried the amendments or this task made them.
```

### M-13 Task 6 `--list` Ready line depends on Task 7

<!-- Source: Base R1-06 (original, modified: kept at minor as overstated; class necessary, origin inherited) — merged per Change #13 -->
```yaml
id: M-13
sources:
  - R1-06 (calibrator: overstated)
class: necessary
origin: inherited-from-spec
severity: minor
plan_ref: "plan:120; plan:125; plan:131"
spec_ref: "source.md:142; source.md:561-563; source.md:573"
claim: |-
  The §2.8 block includes the "Ready for Serena retirement" line, which needs `codegraph_ready()` from Task 7. Task 6's acceptance does not check that line, so this is an ordering ambiguity only.
fix: |-
  Task 6 states that the Ready line lands in Task 7, and Task 7's acceptance checks it.
```

### M-14 Task 13 sandbox fallback only by reference

<!-- Source: Base R1-11 (original, modified: kept at minor as overstated; class necessary → drift) — merged per Change #14 -->
```yaml
id: M-14
sources:
  - R1-11 (calibrator: overstated)
class: drift
origin: plan
severity: minor
plan_ref: "plan:223-227"
spec_ref: "source.md:416"
claim: |-
  The §4.2 Notes fallback for `claude mcp get` is included only through plan:19 and plan:223.
fix: |-
  One sentence naming the fallback (stdio `initialize` + `tools/list`, `serverInfo.name == codegraph`), recorded in `P2-layer2.md`.
```

### M-15 T1 coverage-matrix false attributions

<!-- Source: Variant B P2R2-5 (with the calibrator's U23 correction); debate C-003 — merged per Change #15 -->
```yaml
id: M-15
sources:
  - P2R2-5 (calibrator U23 correction)
  - C-003
class: drift
origin: reflect-artifact
severity: minor
plan_ref: "artifacts/coverage-matrix.yaml:319-325; artifacts/coverage-matrix.yaml:454-461"
spec_ref: "source.md:289; source.md:308"
claim: |-
  INF-037 (U4) is matched to Task 7, and INF-056 (U23) is matched to Task 3. The true carriers are Task 4 and Task 5. No requirement is lost.
fix: |-
  Correct `matched_task_ids` (INF-037 → Task 4, INF-056 → Task 5).
```

### M-16 T1 coverage-matrix under-sampling

<!-- Source: Variant B P2R2-6 (calibrator: overstated; kept at minor) — merged per Change #16 -->
```yaml
id: M-16
sources:
  - P2R2-6 (calibrator: overstated)
class: drift
origin: reflect-artifact
severity: minor
plan_ref: "artifacts/coverage-matrix.yaml"
spec_ref: "source.md:59-193, 216-234, 254-272, 323-418, 727-741 (§6 has INF-093 and §8 has INF-104)"
claim: |-
  These spans have no matrix rows, and their coverage rests on the by-reference triage.
fix: |-
  Annotate the T1 card that these spans have no matrix rows, and that their coverage rests on the by-reference triage.
```

### M-17 Task 2 "commit only if a file changed"

<!-- Source: Variant B P2R2-7 (Task 2 part); INV-018 — merged per Change #17 -->
```yaml
id: M-17
sources:
  - P2R2-7
  - INV-018
class: authorized
origin: plan
severity: minor
plan_ref: "plan:54"
spec_ref: "source.md:459"
claim: |-
  The conditional commit is an authorized addition, because it avoids an empty commit. But with `.dev/tasks` always staged, a ledger-only change satisfies "a file changed".
fix: |-
  The condition names `phase-1-removal-spec.md` or the facts file.
```

### M-18 Task 7 retire-test selector can be empty

<!-- Source: reviewer 1 calibrator extra_risk (Variant A); INV-006 (HIGH); orchestrator check — merged per Change #18 -->
```yaml
id: M-18
sources:
  - reviewer 1 calibrator extra_risk
  - INV-006
  - orchestrator check (rg -l install_retired_mcp tests rc 1; install_retired_mcp.py absent; pyproject.toml:108 testpaths = ["tests"])
class: necessary
origin: inherited-from-spec
severity: important
plan_ref: "plan:131; plan:134-135"
spec_ref: "source.md:572; source.md:576-577"
claim: |-
  If `$(rg -l install_retired_mcp tests)` is empty (true in this checkout today), plan:134 runs only the other two files, and plan:135 runs the whole suite with `-k "codegraph and serena"`. That is a false pass on the Serena-retirement gate.
fix: |-
  F=$(rg -l -g '*.py' install_retired_mcp tests)   # the assignment aborts under -e when nothing matches
  test -n "$F"
  uv run pytest $F …
```

### M-19 Acceptance checks that pass vacuously

<!-- Source: invariant probe INV-011, INV-017 — merged per Change #19 -->
```yaml
id: M-19
sources:
  - INV-011
  - INV-017
class: necessary
origin: inherited-from-spec
severity: minor
plan_ref: "plan:21; plan:167; plan:217; plan:228"
spec_ref: "source.md:606; source.md:661"
claim: |-
  - `test -z "$(comm -13 <baseline> <fail>)"` (plan:167) passes if the baseline is missing.
  - `tail -1 … P2-layer2.md` (plan:228) exits 0 whatever the last line is.
  - `rg -n codegraph` (plan:217, plan-added) passes on any mention.
fix: |-
  - plan:21 says acceptance commands "exit 0 if and only if the criterion passes".
  - plan:167 becomes `comm -13 … > /tmp/p2-t5-new.txt` followed by `test ! -s /tmp/p2-t5-new.txt`.
  - plan:228 becomes `test "$(tail -1 .dev/codegraph-migration/evidence/P2-layer2.md)" = LAYER2_OK`.
```

<!-- Source: debate-transcript.md Round 3 note and invariant-probe.md Summary -->
## Unaddressed invariants

INV-001 and INV-006 were HIGH-severity and UNADDRESSED in the Round 2.5 invariant probe. At depth standard there is no Round 3, so neither was re-debated by the advocates. They are applied as corrections in this merge:

- INV-001 changes the M-02 fix: user scope keeps a deferred gate (`/tmp/p2-t16-us.rc`, final `test … -eq 0`).
- INV-006 becomes the new finding M-18: the retire-test selector must not be empty.

Both stay listed as unaddressed invariants in the return contract and are flagged for review.
