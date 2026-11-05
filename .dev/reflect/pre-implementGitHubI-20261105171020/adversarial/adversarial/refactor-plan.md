# Refactoring Plan: Merge into Base (Variant B)

## Overview
- Base: Variant B (`variant-2-original.md`, reviewer 2, qa persona, haiku class), selected in `base-selection.md` (combined 0.8448 vs 0.8095; tiebreaker on debate wins 8 to 2)
- Incorporating strengths from: Variant A (`variant-1-original.md`, reviewer 1, analyzer persona, sonnet class) and the Round 2.5 invariant probe (`invariant-probe.md`, fault-finder)
- Merged artifact: one MERGED REVIEWER CARD in YAML with the variants' schema: `verdict`, `self_confidence`, `findings[]` (`id`, `claim`, `evidence`, `class`, `severity`, `plan_ref`, `recommended_change`), `not_checked`. Provenance goes in YAML comments above each finding (`# Source: ...`), so the schema stays unchanged.
- Planned changes: 13
- Risk level: Medium overall (four changes rewrite base findings; the rest are additive)

## Combined verdict for the merged card

**verdict: FAIL** — do not approve the plan as written. Three findings are blocking: an executor following the plan would either break `ccsession --help` or fail Task 5's own criterion (M-F1), cannot satisfy Task 1's red-log criterion (M-F2), and may start a real Claude Code session with `--dangerously-skip-permissions` during the mandated red run (M-F3). The remaining seven are minor.

**self_confidence: 0.85** (orchestrator-set, between the two calibrated values 0.82 and 0.87; it is not a new calibration, and the three probe-sourced findings have not been calibrated).

### Target finding list (final class from the 4-category taxonomy; definitions `sc-reflect-protocol/SKILL.md:985-1017`, precedence Regression > Drift > Necessary > Authorized at `:1056`)

| Merged id | plan_ref | Final class | Severity | Built from | Change # |
|---|---|---|---|---|---|
| M-F1 | Task 5 | Regression | blocking | B-F1 + A-F1 (C-001, C-002, U-003) + INV-008 | 1 |
| M-F2 | Task 1 | Regression (was Drift) | blocking | B-F2, narrowed (U-004) | 2 |
| M-F3 | Task 1 | Drift | blocking | INV-007 (Round 2.5 probe) | 3 |
| M-F4 | Constraints | Drift (A-F2 was Necessary deviation) | minor | B-F3 + A-F2 (C-003, X-001, X-002, U-001, U-008, A R2 N1, INV-011) | 4 |
| M-F5 | Constraints | Regression (latent) | minor | INV-017 (Round 2.5 probe) | 5 |
| M-F6 | Constraints | Drift | minor | INV-016 (Round 2.5 probe) + INV-003 | 6 |
| M-F7 | Task 9 | Regression (was Drift) | minor | B-F4 (U-005) + A-008 + C-005 | 7 |
| M-F8 | Task 3 | Drift | minor | B-F6 + A-F3 (C-004) + A-007 | 8 |
| M-F9 | Task 3 | Drift | minor | B-F5, narrowed (U-006) | 9 |
| M-F10 | Task 8 | Drift | minor | A-F4 (U-002) + INV-021 | 10 |
| (none) | — | — | — | B-F7 moved to a header comment (U-007) | 11 |
| (none) | — | — | — | INV-022 carried as the verdict rationale | 12 |

Order in the card: blocking first (M-F1, M-F2, M-F3), then minor in the order above.

## Planned Changes

### Change 1: Task 5 help sentinel — replace B's remedy with A's and couple the sentinel (from Variant A and the probe)
- **Source**: Variant A F1 (`claim`, `recommended_change`, evidence `ccsession:96-98`, `test_ccsession_tag.py:1134-1144`); `invariant-probe.md` INV-008
- **Target**: Base F1 → M-F1 (modify `recommended_change`, append evidence; keep `claim`, class Regression, severity blocking)
- **Rationale**: C-001 final call A by both advocates (A R2 55, B R2 60): B's primary remedy (retarget the awk marker) leaves the new paragraph below the stop line, so PLAN:100's positive assertion still fails, and B's alternative (move the paragraph above the marker) prints the Grep-tool rationale `ccsession:110-113` into `--help` (A R2 N3, conceded B R2 #8). U-003 (A-only, credited by B R2 steelman): PLAN:100's "no longer contains the word 'always' in the permissions paragraph" of `--help` is vacuous because that paragraph is never printed. C-002 final call A by both (70, 80): use `set -e` and `CLAUDE_BIN=` as negative tokens; B's `CC_CLAUDE_FLAGS=` can collide with a new usage example. INV-008 (MEDIUM, re-read: `ccsession:1652` regex `^# The wrapper always runs`; `ccsession:109`; PLAN:97 still instructs "Rewrite the sentence ... so it no longer says 'always'"): the consensus summary dropped A's sentinel clause, so the merged remedy must carry it explicitly and must also rewrite PLAN:97.
- **Integration point**: Replace base F1 `recommended_change` with: (1) put the usage entry `CCSESSION_PERMISSIONS=default ccsession <topic>` in the usage block next to `ccsession:96-97`, above the sentinel; (2) either keep line 109 starting with `# The wrapper always runs`, or change the regex at `ccsession:1652` in the same edit as the sentence; (3) rewrite PLAN:97's instruction and PLAN:100's criterion accordingly (the criterion checks the usage entry, not "always" in a paragraph `--help` never prints); (4) add a test that `--help` contains `CCSESSION_PERMISSIONS=default` and contains neither `set -e` nor `CLAUDE_BIN=`. Keep B's claim text, including "'always' occurs only on line 109 of that paragraph" (also at `ccsession:75, 98`, above the sentinel) and B's substring-test inventory.
- **Concrete anchors preserved**: `ccsession:1652`, `:109`, `:109-114`, `:96-97`, `:110-113`, `:121` (`set -e`), `:123` (`CLAUDE_BIN=`); PLAN:95, 97, 100; tests `test_ccsession_tag.py:157-169, 1134-1144, 2315-2323`, `test_ccsession_tiers.py:576-582`, `test_install_ccsession.py:224-238`.
- **Risk**: Medium — rewrites the base's remedy text.

### Change 2: Task 1 red-log criterion — narrow and reclassify (base finding, debate correction)
- **Source**: Base F2; A R2 response 1; B R2 response 3; B's calibrator note
- **Target**: Base F2 → M-F2 (modify `claim`, `class`)
- **Rationale**: U-004 final call B by both (90, 92). A R2 response 1: the first prong is decisive (the `CC_CLAUDE_FLAGS=--verbose` + `default` test passes on the old launcher because `ccsession:124` already lets a non-empty value replace the default); the second prong (the empty-`CC_CLAUDE_FLAGS` + `default` test being in both groups) is an ambiguity, since "the empty-`CC_CLAUDE_FLAGS` tests pass" can be read as the variable-unset one. B did not rebut that narrowing. Class: Drift is excluded by `SKILL.md:1009` ("Does NOT contradict any acceptance criterion"); the plan's own mandated test (PLAN:36) makes its own criterion (PLAN:39) unmeetable, which is `SKILL.md:1017` Regression ("contradicts an acceptance criterion"); B R2 #3 reached the same reading; B's calibrator: "F2 is an internal plan defect not Drift".
- **Integration point**: Rewrite the claim so the first prong carries it and the second is stated as an ambiguity; set `class: Regression`; keep `severity: blocking` and B's replacement criterion text verbatim.
- **Concrete anchors preserved**: PLAN:36, PLAN:39, `ccsession:124`, `source.md:1`; the replacement criterion text in B-F2 `recommended_change`.
- **Risk**: Low — label and claim narrowing; remedy unchanged.

### Change 3: Add INV-007 — the Task 1 bypass test can start the real Claude on the old launcher (Round 2.5 probe, fault-finder)
- **Source**: `invariant-probe.md` INV-007 (UNADDRESSED, MEDIUM)
- **Target**: new finding M-F3, `plan_ref: Task 1`, class Drift, severity blocking
- **Evidence re-read by the orchestrator**: PLAN:36 tells the executor to "call `subprocess.run` directly with `check=False`, as `test_help_and_unknown_profile_list_data_profiles` does"; that model test sets only `HOME` on a copy of `os.environ` (`test_ccsession_tag.py:1145-1153`), with no fake `CLAUDE_BIN` and no `CCSESSION_ENV_FILE`, unlike `_label_launch` (`:1177-1184`). `ccsession:123` defaults `CLAUDE_BIN` to `claude`; `ccsession:1868` execs it with `$CC_CLAUDE_FLAGS`, which on the old launcher still starts with `--dangerously-skip-permissions`. No `tests/**/conftest.py` sets `CLAUDE_BIN` (orchestrator grep: no match); `/usr/local/bin/claude` exists on this machine. PLAN:39 mandates running this test against the unchanged launcher.
- **Narrowed claim**: the evidence shows the red run reaches an `exec` of whatever `claude` is on `PATH`, with the bypass flag, from the pytest working directory. What that process then does is environment-dependent and was not executed: the fresh `HOME` may leave it without credentials, and pytest's default capture usually gives the child an empty standard input, so the probe's "possibly hanging on inherited stdin" is the less likely half. The finding stands on the first half.
- **Class and severity**: Drift — an unrequested test-setup choice with no rationale that contradicts no acceptance criterion (`SKILL.md:1003, 1009`). Blocking, because the plan instructs the executor to run it and the cost of the fix is one line.
- **Integration point**: insert after M-F2. `recommended_change`: build the `bypass` test on `_label_launch`'s environment (fake `CLAUDE_BIN`, `HOME`, `CCSESSION_ENV_FILE`) via the new `extra_env` argument, add `stdin=subprocess.DEVNULL` and a timeout, and assert the fake Claude did not run.
- **Risk**: Low — additive.

### Change 4: Global exit-2 scope — merge A-F2 into B-F3, correct the impact, the class and the list (debate corrections)
- **Source**: Base F3; Variant A F2 (U-001 orca trace); A R2 N1 and N4; `invariant-probe.md` INV-011 (LOW, folded in because it corrects this finding's own list)
- **Target**: Base F3 → M-F4 (modify `claim`, append evidence; keep class Drift, severity minor, `plan_ref: Constraints`)
- **Rationale**: X-002 final call B by both (68, 70): Drift, not A's "Necessary deviation" (`SKILL.md:987` requires a documented rationale; PLAN:22 gives none; conceded A R2 response 3). X-001 final call tie by both (55, 58): neither "cosmetic" (A) nor "breaks" (B) is exact. The agreed facts: no bypass leaks (`ccsession-orca:247, 249`, re-read); `--help`, `--list` and `--rm` fail visibly; the hook calls `--sync-name`, `--orca-tab-session` and `--orca-tab-clear` (`hooks/session-name.sh:196-212`) become silent no-ops in any session with the hook and a bad exported value (A R2 N4); the installer's `--migrate-names` (`install_ccsession.py:104-113`) is skipped silently (A R2 N1); `ccsession-orca` drops a valid `CCSESSION_NAME` with "not a valid session name; ignoring it" (`ccsession-orca:132-137`) and prints "the session-name question failed (status 2)" (`:204-212`) (U-001). INV-011: the union list still omits `--key`, `--orca-tab-reopen`, `--here`, `--refresh-models`, `--models-status`; re-read: line 124 precedes the whole dispatch at `ccsession:1671` onward, so the accurate statement is "every invocation, including `--help`".
- **Integration point**: rewrite the claim to the agreed impact; replace B's subcommand list with "every invocation, including `--help`" and give the named subcommands as examples only; drop "breaks tab-title cleanup and name listing". `recommended_change`: state the scope in Constraints and pin it with one test (bad value + `ccsession --help` exits 2, from A-F2); or defer only the exit to the launch paths under the constraint in M-F5.
- **Concrete anchors preserved**: exit status 2 (PLAN:22); `ccsession:124`, `:1671`; `ccsession-orca:132-137, 204-212, 247, 249`; `hooks/session-name.sh:196-212`; `install_ccsession.py:104-113`.
- **Risk**: Medium — merges two findings and rewrites the claim.

### Change 5: Add INV-017 — launch-scoping must keep the flag choice at line 124 (Round 2.5 probe, fault-finder)
- **Source**: `invariant-probe.md` INV-017 (UNADDRESSED, MEDIUM)
- **Target**: new finding M-F5, `plan_ref: Constraints`, class Regression (latent), severity minor
- **Evidence re-read by the orchestrator**: add-on profiles are sourced and can run `ccsession_profile_<name>` at `ccsession:819-836`; the env file is assigned at `:846` and sourced at `:847-849`; the dispatch starts at `:1671`. Both cards offer launch-scoping as a remedy (A-F2 "run the check only where a launch is about to happen"; B-F3 "move the validation onto the launch paths only"), and B R2 unresolved item 2 leaves it to the owner. If the whole `case` moves below `:847-849`, a value set in the env file starts choosing the current launch's flags (contradicting PLAN:23) and an env-file `CC_CLAUDE_FLAGS=""` starts taking the default instead of giving empty flags (contradicting PLAN:20 and `source.md:1` "Do NOT change how an empty CC_CLAUDE_FLAGS is handled").
- **Class**: Regression by `SKILL.md:1017` (it would contradict an explicit spec constraint), latent because the plan as written does not do it; severity minor.
- **Integration point**: insert after M-F4. `recommended_change`: if the check is launch-scoped, keep computing `_cc_default_flags` and `CC_CLAUDE_FLAGS` at line 124 and defer only the `exit 2`; say so in Constraints.
- **Risk**: Low — additive.

### Change 6: Add INV-016 — caller-passed flags still apply; the Goal overstates the spec (Round 2.5 probe, fault-finder)
- **Source**: `invariant-probe.md` INV-016 (UNADDRESSED, MEDIUM); INV-003 (LOW, folded into the same doc sentence)
- **Target**: new finding M-F6, `plan_ref: Constraints` (the Goal line PLAN:15 sits above Constraints), class Drift, severity minor
- **Evidence re-read by the orchestrator**: PLAN:15 Goal: "`ccsession` (directly and through `ccsession-orca`, ...) starts Claude without `--dangerously-skip-permissions`". `ccsession-orca:14-17` passes Orca's own arguments after `--claude-args` unchanged and `:247, 249` exec `ccsession --shim --claude-args "$@"`; every launch line appends `"$@"` (`ccsession:1799, 1801, 1859, 1861, 1866, 1868`); the tests model Orca's default option as `ORCA_DEFAULT = "--dangerously-skip-permissions"` (`test_ccsession_tag.py:1806-1811`). So an Orca tab started with `CCSESSION_PERMISSIONS=default` still runs with the bypass. The spec's wording ("ccsession adds no permission-bypass flag", `source.md:1`) still holds, and the Coder print-mode path (Task 2, `-p hello`) passes no such flag, so the issue-390 use case is unaffected. INV-003 (re-read `ccsession:819-836`): an add-on profile can reassign `CC_CLAUDE_FLAGS` after line 124, as can the env file.
- **Class**: Drift (the Goal and the planned docs state more than the spec and no task records the limit); severity minor.
- **Integration point**: insert after M-F5. `recommended_change`: reword PLAN:15 to "ccsession adds no `--dangerously-skip-permissions`", and add one sentence to the Task 5 header text, the Task 6 README row and the Task 9 bullet: flags the caller passes (such as Orca's default option) and flags set through `CC_CLAUDE_FLAGS`, an add-on profile or the env file still apply.
- **Risk**: Low — additive.

### Change 7: Env-file clause — correct the citation, reclassify, extend the test (base finding, debate correction)
- **Source**: Base F4; A-008 (both advocates QUALIFY in R2, A R2 adopts B's test); C-005
- **Target**: Base F4 → M-F7 (modify `claim`, `class`, `recommended_change`)
- **Rationale**: U-005 final call B by both (75, 80). C-005 final call B by both (85): the env file is assigned at `ccsession:846` and sourced at `:847-849`; state both instead of "sourcing at ccsession:846-849". A-008 agreed: the file cannot set `CCSESSION_PERMISSIONS` for the current launch, but a `CC_CLAUDE_FLAGS` set in it still replaces the flags, so PLAN:121's "this file is read after the launch flags are chosen" is imprecise. Class: this is an orchestrator consistency correction, not a debate ruling (the debate did not contest F4's label). The plan's steps make Task 9's own criterion (PLAN:148, "every behavior in the bullet matching the tests of Tasks 1 to 3") unmeetable for the env-file clause; by `SKILL.md:1009` and `:1017` with precedence `:1056` that is Regression, the same rule the debate applied to M-F2.
- **Integration point**: set `class: Regression`, keep `severity: minor`; `recommended_change`: one Task 1 test with `CCSESSION_PERMISSIONS=default` inside a `CCSESSION_ENV_FILE` asserting the launched argv still starts with `--dangerously-skip-permissions` (`_label_launch` already sets `CCSESSION_ENV_FILE`, `test_ccsession_tag.py:1182`), or drop the clause from Task 9's criterion; and reword PLAN:121 to "the variable is read before this file is sourced".
- **Concrete anchors preserved**: PLAN:23, 111, 121, 145, 148; `ccsession:124`, `:846`, `:847-849`; `test_ccsession_tag.py:1182`.
- **Risk**: Low — label change and an appended remedy clause.

### Change 8: Task 3 `CC_CLAUDE_FLAGS` leak — merge A-F3, extend to the unisolated tests (from Variant A and the shared-assumption ruling)
- **Source**: Base F6; Variant A F3; A-007 (both advocates QUALIFY in R2)
- **Target**: Base F6 → M-F8 (append to `recommended_change` and `evidence`; keep class Drift, severity minor)
- **Rationale**: C-004 final call B by both (60): B's tie to PLAN:40 is kept; A's alternative fix (pass `CC_CLAUDE_FLAGS=""` or `monkeypatch.delenv` inside the test) is added. A's aside "it removes `CC_CLAUDE_FLAGS` and adds it to the excluded names" is not carried (the tuple already holds it, diff-analysis C-004). A-007 agreed: a bad exported `CCSESSION_PERMISSIONS` makes `test_install_ccsession.py:51-67`, `:224-238` and `tests/cli/test_update_command.py:198-208` fail (A R2 N1, B R2 NB-2; not re-read by the orchestrator); a valid `default` does not.
- **Integration point**: add one sentence to `recommended_change`: clear `CCSESSION_PERMISSIONS` (with `CC_CLAUDE_FLAGS`) in those three tests, or launch-scope the check under M-F5.
- **Risk**: Low — additive.

### Change 9: Task 3 control ambiguity — narrow the risk (base finding, debate correction)
- **Source**: Base F5; U-006 (A tie 58, B B 55 — not agreed; both agree the risk is low)
- **Target**: Base F5 → M-F9 (modify `claim`; keep class Drift, severity minor, remedy)
- **Rationale**: Both advocates agree PLAN:57 and PLAN:60 already point at `_launch` + `--tier` tests (for example `test_ccsession_tiers.py:525`) and that `:445` and `:500` are `ccsession-orca` launches without `--tier`, so a misreading needs both pointers ignored (A R1 W4, B R1 concession 4, B R2 response 4).
- **Integration point**: replace "can make the test unpassable" with "could make the test unpassable if an implementer copied the `ccsession-orca` tests at `:445` or `:500`, which the plan does not point to"; keep the one-line remedy naming `_launch(tmp_path, "work", "--tier", "tier0")`.
- **Risk**: Low.

### Change 10: Add A-F4 — D08 line 23's trailing clause (from Variant A), with INV-021 on the same line
- **Source**: Variant A F4 (U-002); `invariant-probe.md` INV-021 (LOW, folded in because it is the same line and the same one-line edit)
- **Target**: new finding M-F10, `plan_ref: Task 8`, class Drift, severity minor
- **Rationale**: U-002 is A-only and un-rebutted (credited by B R1 steelman and concession 5; A R2 found no other falsified doc). Re-read: `docs/testing/v5.0.0/user/D08-ccsession.md:23` reads "... unless `CC_CLAUDE_FLAGS` is set (`ccsession:78-83,93`): Claude Code then runs tools without asking." The trailing clause becomes false for an opted-in launch, against Task 8's own premise (PLAN:130, "docs that state the permission default must stay true"). INV-021: the same sentence cites `ccsession:78-83,93`, but the flags are now at `ccsession:109-114, 124` (re-read).
- **Integration point**: append after M-F9 with A-F4's claim and remedy verbatim ("tie the trailing clause to the default launch"), plus: update the line citation on the same line. Both fit PLAN:135's one-changed-line limit.
- **Concrete anchors preserved**: `D08-ccsession.md:23`; `E01-ccsession-tier-policy.md:21` (lacks the clause, so only D08 changes); PLAN:130, 135.
- **Risk**: Low — additive.

### Change 11: Move B-F7 out of the findings list (debate correction)
- **Source**: Base F7; U-007 (A: A 58; B: tie 55; both agree in R2 it is not a plan defect)
- **Target**: Base F7 → a YAML comment block in the card header: `# Coverage-slice note (not a plan finding): matrix rows INF-004 and INF-007 report "none", but the plan carries INF-004 (PLAN:20, 36) and INF-007 (PLAN:25); record both as covered-by-plan.`
- **Rationale**: B R2 response 2: "B-F7 belongs in the coverage slice, not in a plan-defect list"; A R2 U-007 row: "The omission costs a corrected plan nothing." The brief did ask for the audit (`reviewer-2.md:23`), so the content is kept, outside the findings.
- **Risk**: Low.

### Change 12: Carry INV-022 as the verdict rationale (Round 2.5 probe, fault-finder)
- **Source**: `invariant-probe.md` INV-022 (UNADDRESSED, MEDIUM)
- **Target**: card header comment above `verdict`
- **Rationale**: INV-022 is a sufficiency verdict, not a separate plan defect. Its gates were re-checked against the evidence re-read for Changes 1, 3, 5 and 6: G1 holds after M-F2 with the M-F3 caveat; G3 is falsified for the Goal wording (M-F6); G5 holds unless the check is moved (M-F5); G6 holds only with the sentinel coupling (M-F1). Its three required additions are each a finding: (a) M-F1, (b) M-F3, (c) M-F6.
- **Integration point**: `# Verdict rationale (Round 2.5 probe, fault-finder, INV-022): the debate's consensus edits are not sufficient on their own; M-F1, M-F3 and M-F6 close the three gaps.`
- **Risk**: Low.

### Change 13: Card-level fields
- **Target**: `verdict: FAIL` (both variants FAIL); `self_confidence: 0.85` (orchestrator-set, see above); header comment naming the merge: base B, incorporated A, probe additions, this plan.
- **not_checked** (union, minus items closed in the debate or probe):
  - keep from B: no command was run, all red-test and awk claims are reasoned from source; Coder #458 not checked; `CHANGELOG.md` read to line 45; whether any developer shell exports `CC_CLAUDE_FLAGS`.
  - keep from A, narrowed: the Makefile `sync-dev` and `verify-sync` targets; hook behaviour when a VALID `CCSESSION_PERMISSIONS=default` is inherited (the bad-value case was settled in X-001).
  - add: what the real `claude` does when M-F3's red run reaches it (not executed); whether `CCSESSION_PERMISSIONS` should be unset before `exec` or deliberately inherited (A-004, unresolved; owner decision; probe INV-001, INV-002).
  - drop as closed: A's `plugins/` mirror (diff-analysis U-009: no `plugins/**/ccsession*` exists); A's `-k permissions` collision check (INV-010 ADDRESSED); A's `case` / `:-` correctness (INV-005, INV-012, INV-013 ADDRESSED); A's "does `test_install_ccsession.py` pin header text" (B-F1 cites `:224-238`, a substring check); A's orca parametrize set (INV-015 ADDRESSED the shared `tmp_path`).
- **Risk**: Low.

## Threshold and anchor preservation

| Anchor | Source | Value | Target disposition |
|---|---|---|---|
| Bad-value exit status | PLAN:22, B-F3, A-F2 | 2 | preserved-exact (M-F4, M-F5) |
| Help stop-marker | B-F1, A-F1 | `ccsession:1652`, regex `^# The wrapper always runs`, sentinel line 109 | preserved-exact (M-F1) |
| Usage-entry location | A-F1 | next to `ccsession:96-97`, above line 109 | preserved-exact (M-F1) |
| Flag-default line | both | `ccsession:124` | preserved-exact |
| Env-file lines | A-F2 "846", B-F4 "846-849" | assigned `:846`, sourced `:847-849` | modified-with-rationale (C-005) |
| Launch lines | A-001 | `ccsession:1799, 1801, 1859, 1861, 1866, 1868` | preserved-exact (M-F6) |
| Add-on profile block | INV-003, INV-017 | `ccsession:819-836` | added (M-F5, M-F6) |
| Dispatch start | B-F3, A-F2 | `ccsession:1671` | preserved-exact (M-F4) |
| Guard-test tokens | A-F1, B-F1 | `set -e`, `CLAUDE_BIN=` (A) vs `CC_CLAUDE_FLAGS=` (B) | A's preserved-exact; B's dropped-with-rationale (C-002) |
| Substring help tests | B-F1 | `test_ccsession_tag.py:157-169, 2315-2323`; `test_ccsession_tiers.py:576-582`; `test_install_ccsession.py:224-238` | preserved-exact (M-F1) |
| Control invocation | B-F5 | `_launch(tmp_path, "work", "--tier", "tier0")`, `tiers:525` | preserved-exact (M-F9) |
| Unisolated test sites | A-007 | `test_install_ccsession.py:51-67, 224-238`; `tests/cli/test_update_command.py:198-208` | added (M-F8) |
| Confidence | A 0.88/0.82, B 0.78/0.87 | 0.85 | modified-with-rationale (orchestrator-set, not calibrated) |
| Severity counts | A 1 blocking / 3 minor; B 2 / 5 | 3 blocking / 7 minor | modified-with-rationale (M-F3 added as blocking; B-F7 removed) |

## Changes NOT Being Made (with rationale)

| Item | Source | Not carried | Rationale and debate evidence |
|---|---|---|---|
| B-F1 primary remedy | B | "update the awk stop-marker ... to match the rewritten sentence" as the fix | Leaves PLAN:100 failing (C-001, B R2 response 8) |
| B-F1 alternative | B | "move the permissions documentation above the marker" | Prints `ccsession:110-113` into `--help` (A R2 N3, B R2 response 8) |
| B-F1 guard token | B | `CC_CLAUDE_FLAGS=` | Can collide with a usage example (C-002, both advocates) |
| B-F3 impact wording | B | "breaks tab-title cleanup and name listing" | Replaced by the agreed silent / visible split (X-001 tie) |
| B-F3 subcommand list | B | the enumerated list as the scope statement | Incomplete (INV-011); "every invocation, including `--help`" replaces it |
| B-F7 as a finding | B | finding status | Not a plan defect (U-007, both R2); kept as a comment (Change 11) |
| A-F2 class | A | Necessary deviation | `SKILL.md:987` requires a documented rationale; none exists (X-002, both R2) |
| A-F2 line citation | A | "sourced (line 846)" | `:846` assigns, `:847-849` sources (C-005) |
| A-F2 "cosmetic" framing | A | "Optionally note the orca message wording as a known cosmetic effect" | Not cosmetic only: silent function loss on hooks and installer (X-001, A R2 N1, N4) |
| A-F3 aside | A | "it removes `CC_CLAUDE_FLAGS` and adds it to the excluded names" | The tuple already holds it (diff-analysis C-004; A R1 concession) |
| B R1 install.sh sites | B advocate | `test_install_ccsession.py:276-277, 302-303` | Withdrawn by B R2 NB-5: `install.sh:63` swallows the exit |
| A-004 inheritance sentence | B advocate (QUALIFY), probe INV-001 / INV-002 (LOW) | a Constraints sentence on deliberate inheritance | Unresolved in debate (A ACCEPT, B QUALIFY) and LOW in the probe; recorded in `not_checked` as an owner decision instead of a finding |
| INV-006 | probe (LOW) | whitespace-only `CC_CLAUDE_FLAGS` gives no flags | Pre-existing, unchanged by the plan, LOW |
| INV-014 | probe (LOW) | separate finding | Covered by Change 8 (A-007 sites) |
| INV-022 as a finding | probe (MEDIUM) | standalone finding | A sufficiency verdict; carried as the verdict rationale and through M-F1, M-F3, M-F6 (Change 12) |
| Probe MEDIUM findings dropped for bad evidence | probe | none | INV-007, INV-008, INV-016, INV-017 and INV-022 all re-checked against their cited lines and hold. INV-007 is narrowed (the stdin-hang half is less likely under pytest capture); nothing is dropped |

## Risk Summary

| Change # | Risk | Impact if failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | M-F1 remedy could lose B's evidence or A's sentinel clause, re-opening INV-008 | Restore base F1 and re-apply A-F1 `recommended_change` verbatim |
| 2 | Low | Label mismatch with the base | Restore `class: Drift` |
| 3 | Low | Additive | Remove M-F3 |
| 4 | Medium | Merged claim could reintroduce an overstatement or drop the orca trace | Restore base F3 and A-F2 as two findings |
| 5 | Low | Additive | Remove M-F5 |
| 6 | Low | Additive | Remove M-F6 |
| 7 | Low | Label change is an orchestrator consistency call, not a debate ruling | Restore `class: Drift`; keep the citation fix |
| 8 | Low | Additive | Remove the appended sentence |
| 9 | Low | Wording only | Restore base F5 claim |
| 10 | Low | Additive | Remove M-F10 |
| 11 | Low | Loses no content | Restore F7 as a finding |
| 12 | Low | Comment only | Remove the comment |
| 13 | Low | Card-level fields | Restore base values |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-05T18:27:31Z
- Review status: auto-approved
