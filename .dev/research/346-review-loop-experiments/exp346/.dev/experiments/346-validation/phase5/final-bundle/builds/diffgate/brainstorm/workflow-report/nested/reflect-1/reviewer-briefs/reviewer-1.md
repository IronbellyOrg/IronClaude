# Reviewer 1 brief (persona: analyzer; model class: sonnet)

Mode: UC-1 pre-execution reflection. Audit the PLAN (.dev/tasks/to-do/TASK-WF-spec-20261108-181640/TASK-WF-spec-20261108-181640.md) against its SPEC (.dev/tasks/to-do/TASK-WF-spec-20261108-181640/source.md). You are read-only: return findings only, run nothing. Classify each finding as Authorized expansion / Necessary deviation / Drift / Regression (UC-1: a plan step that contradicts the spec is Regression-risk; a spec requirement no task delivers is a coverage gap), give severity (HIGH/MEDIUM/LOW), a file:line citation you re-Read, and a one-line fix. Owner rulings recorded in the plan's Constraints (plan lines 26-30) are authoritative and override the spec where they say so. Return a YAML card: findings[], verdict (approve|refactor), self_confidence 0-1.

## T1 card excerpt

## Root-cause / deviation section

- D1 (Authorized, owner ruling plan line 29): source.md:99 asks for a byte-identical `## Unattended mode`; the plan omits the section. Residual: the parent's Usage line 23 (src/superclaude/commands/spec-panel.md:23) still advertises `[--unattended] [--report-dir <dir>]`, and the SPEC's Review Loop bullet 1 and Diffgate bullet 1 (source.md:77 and source.md:91) still describe an `--unattended` default. The variant will advertise a mode it no longer documents; the plan records this as a residual instead of resolving it.
- D2 (Grounding gap): T10 (R3 reviser brief) is not covered by source.md section 4, which names only the two fix-cycle reviser briefs (source.md:189). Plan line 172 copies T10 unchanged and hands the decision to the coordinator.
- D3 (Necessary): Task 4 adds a `proxy_all` field the SPEC's subcommand table (source.md:108) does not list; it implements the owner counting decision and the SPEC's own fixture expectation "label proxy 5" (source.md:154).

## Structural / tech-debt section

- S1: Task 4 acceptance (plan line 77) hardens the SPEC's estimate "about 35 script tests" (source.md:242) into a floor of 35; a reviewer may treat this as over-specification.
- S2: Task 5 acceptance (plan line 87) calls `list_available_skills()` from `superclaude.cli.install_skill`; the import exists at src/superclaude/cli/install_skills.py:28.
- S3: Task 1 allows subcommand bodies to raise "not implemented" until Task 4; the interim state is scaffolding inside one plan, closed by Task 4's acceptance criteria.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T18:26:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/bs346-diffgate projectPath=/home/coder/workspaces/worktrees/IronClaude/bs346-diffgate

### .dev/tasks/to-do/TASK-WF-spec-20261108-181640/TASK-WF-spec-20261108-181640.md:1-31

```markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-spec-20261108-181640
version: "1"
priority: Medium
created_date: "2026-11-08"
---

# diffgate: computed re-review surface for /sc:spec-panel (issue #346), Stage A and Stage B plus experiment kit

Source: ./source.md
Goal: An additive `/sc:spec-panel-diffgate` command, the infrastructure skill `sc-diffgate` with its stdlib script `diffgate.py`, their regression tests, a design note, the `make sync-dev` mirror, and the S1 experiment kit (`.dev/brainstorms/346-diffgate/INSTALL.md` and brief templates under `.dev/brainstorms/346-diffgate/briefs/`) exist in this worktree, exactly as source.md sections 3 and 4 describe, with `/sc:spec-panel` unchanged.

## Constraints

- Scope is source.md section 3 ("Exact changes") and section 4 ("Variant command name and install note") only. Section 3.6 (later adopters), the S1 runs of section 5, and the open questions of section 7 are not built; section 5 only feeds the counting field (Task 2, Task 4) and the brief templates (Task 12).
- Never edit `src/superclaude/commands/spec-panel.md`, `plugins/superclaude/commands/spec-panel.md`, `src/superclaude/core/HOW-WE-WORK.md`, `src/superclaude/core/WORKER-CONTRACT.md` or the installer code under `src/superclaude/cli/` (source.md section 3, first paragraph). No plugin mirror and no HOW-WE-WORK row (source.md 3.5).
- No `src/superclaude` string may appear in `src/superclaude/commands/spec-panel-diffgate.md` or anywhere under `src/superclaude/skills/sc-diffgate/` (project CLAUDE.md rule on installed primitives). Installed lookups name `~/.claude/skills/sc-diffgate` first, then the project `.claude/skills/sc-diffgate` copy.
- `diffgate.py` uses the Python standard library only. Run every Python command through `uv run` (`uv run pytest ...`); the command text tells agents to run the script with `uv run --no-project python ...`.
- Never stage anything under `.claude/` (only `.claude/settings.json` is tracked). `.dev/tasks/` is always staged (`git add .dev/tasks`). Staging is not committing: commit only when asked.
- Do not write to `~/.claude`. Installing for the experiment is a later, separate step that INSTALL.md (Task 11) documents.
- Text in the new files must keep `tests/skills/test_review_severity_rule.py` green: keep the canonical cap text, avoid its banned any-severity phrases, and never describe the fixcheck retry limit with a digit pattern `CAP_REGRESSION` catches (write "three failing `fixcheck` runs in one fix cycle", never "up to 3 fix attempts").
- Owner decision (counting): findings the script defers, demotes or withdraws stay in the review-3 critical+major count. `diffgate.py check` therefore reports a `proxy_all` count that includes them (Task 2, Task 4), and the brief kit's scoring note states this rule (Task 12).
- Owner decision (review-3 brief): the S1 review-3 brief text stays verbatim, including the sentence "any finding of any severity is FAIL". The coordinator ruled (2026-11-08) that only the command token and its `--diffgate-dir` and `--expect-round` arguments are substituted in the review briefs of reviews 1, 2 and 3; that substitution is not an edit of the brief text.
- Owner decision (consent): a flag in a brief counts as explicit consent for one scripted edit or revert. diffgate never writes the specification (source.md section 2), so no task relies on it.
- Owner ruling (2026-11-08, no Unattended section): the variant is a copy of the current `src/superclaude/commands/spec-panel.md` WITHOUT its `## Unattended mode` section, because the earlier S1 arms ran a spec-panel file with no such section and the S1 briefs never pass `--unattended`. This overrides source.md 3.1 item 6 and the `tests/skills/test_worker_contract.py` edit of source.md 3.4: that test file stays unedited and its 31-command set holds. Every other parent line (including Usage line 23 and the `--unattended` clauses inside the SPEC's Review Loop bullet 1 and Diffgate bullet 1) is kept as source.md 3.1 gives it; the residual is that `--unattended` must not be passed to the variant (the WORKER-CONTRACT brief guard refuses a flag for a command without the section). The design note (Task 9) and INSTALL.md (Task 11) state that the section is deliberately missing.
- Owner ruling (2026-11-08, S1 briefs): the verbatim S1 briefs may be READ (read-only, the one allowed exception to the rule about experiment folders) from the folder `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/briefs/task-text/` (forensic source location, quoted): `T05-R1-reviewer-L11-699ae853.txt`, `T06-R1-reviser-L10-3bb70411.txt`, `T07-R2-reviewer-L11-aff19d65.txt`, `T08-R2-reviser-L10-66468bab.txt`, `T09-R3-reviewer-L11-1c9a7ec8.txt`, `T10-R3-reviser-L10-458bdc00.txt`. Never edit the originals; the old repo-root path `OrcaCLICommandRefactor-Specs` inside them is left as is (the coordinator substitutes it at dispatch time).
- No line in this plan or in any file it creates under `.dev/tasks/` may start with a checkbox or a numbered-list marker.
```

### .dev/tasks/to-do/TASK-WF-spec-20261108-181640/TASK-WF-spec-20261108-181640.md:91-124

```markdown
## Phase 3: Variant command (Stage B)

## Task 6: Create the additive `/sc:spec-panel-diffgate` command

Depends on: Task 5

Create `src/superclaude/commands/spec-panel-diffgate.md` as a full copy of the current `src/superclaude/commands/spec-panel.md` (486 lines, read in this worktree; title at line 10, Usage at line 22, `## Tool Coordination` at line 218 with the `**Read**` bullet at line 220, `## Review Loop` at line 256, `## Output Formats` at line 266, `## Unattended mode` at line 451) with every `/sc:spec-panel` renamed to `/sc:spec-panel-diffgate` and only the edits in source.md 3.1: frontmatter `name: spec-panel-diffgate` and the description suffix "with a computed re-review surface (diffgate variant)"; title `# /sc:spec-panel-diffgate - Expert Specification Review Panel (diffgate variant)`; the Usage token `[--re-review <prior-findings-file> --baseline <saved-copy>]` replaced by `[--diffgate-dir <dir> [--expect-round N]]`; the `**Read**` bullet reduced to `- **Read**: Specification content analysis and parsing` (the clause naming the release-spec template path removed with no replacement); the seven `## Review Loop` bullets set to the exact text of source.md 3.1 item 4 (bullets 2 and 7 keep the 427 text plus the shown additions; bullets 1, 3, 4, 5, 6 replaced), each bullet one physical line; the new `## Diffgate` section with the six bullets of source.md 3.1 item 5 placed between `## Review Loop` and `## Output Formats`, one physical line each; the parent's `## Unattended mode` section (from its heading up to, not including, `## Boundaries`) is left out entirely, per the owner ruling in Constraints (this replaces source.md 3.1 item 6). Do not modify `src/superclaude/commands/spec-panel.md`.

Acceptance criteria:
- `src/superclaude/commands/spec-panel-diffgate.md` exists; `git diff --exit-code -- src/superclaude/commands/spec-panel.md plugins/superclaude/commands/spec-panel.md` exits 0.
- `grep -c '^## Unattended mode' src/superclaude/commands/spec-panel-diffgate.md` prints 0, the file still has a `## Boundaries` section, and `uv run pytest tests/skills/test_worker_contract.py -q` passes with that test file unedited.
- `grep -n 'src/superclaude' src/superclaude/commands/spec-panel-diffgate.md` prints nothing; the `## Usage` block contains `--diffgate-dir` and no `--re-review` or `--baseline`.
- The Review Loop bullets and the `## Diffgate` bullets match source.md 3.1 items 4 and 5 character for character (checked by Task 7's test).
- The command's text keeps the canonical cap sentence `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings`, and `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_spec_panel_review_loop.py -v` passes.

## Task 7: Add the variant command regression test

Depends on: Task 6

Create `tests/skills/test_spec_panel_diffgate_command.py` with the checks of source.md 3.4 (row `tests/skills/test_spec_panel_diffgate_command.py`): frontmatter name is `spec-panel-diffgate`; Usage names `--diffgate-dir` and not `--re-review`; the seven Review Loop bullets are present in order, one line each, equal to source.md 3.1 item 4 (the expected text lives in the test file, not read from `.dev/`); `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` imported from `tests/skills/test_review_severity_rule.py` are present; `## Diffgate` sits between `## Review Loop` and `## Output Formats` and names `~/.claude/skills/sc-diffgate` before `.claude/skills/sc-diffgate`; no `src/superclaude` string in the command or anywhere under `src/superclaude/skills/sc-diffgate/`; drift guard: every other `## ` section equals `src/superclaude/commands/spec-panel.md`'s after the name swap, except the parent's `## Unattended mode`, which must be absent from the variant (owner ruling in Constraints), and `## Tool Coordination` is equal after removing the clause that names the release-spec template from the parent's `**Read**` bullet; `spec-panel.md` still carries its 427 Usage flags `--re-review` and `--baseline`; an isolated temporary-HOME install (copy the command to `<tmp>/.claude/commands/sc/` and the skill folder to `<tmp>/.claude/skills/sc-diffgate/`, as the `cp` lines of source.md section 4 do) runs the installed `diffgate.py --help` with `sys.executable` from a working directory outside the repository and exits 0, and a sentinel `<tmp>/.claude/commands/sc/spec-panel.md` is byte-unchanged afterwards.

Acceptance criteria:
- `uv run pytest tests/skills/test_spec_panel_diffgate_command.py -v` passes.
- A negative test case feeds the bullet check a temporary copy of the command (under `tmp_path`, never the real file) with one character of Review Loop bullet 3 changed and asserts the check reports that bullet.

## Task 8: Update the routing-refresh test the new command file breaks

Depends on: Task 6

Edit `tests/recommend/test_routing_refresh.py` line 33 to `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue", "spec-panel-diffgate"}` and extend its comment by one clause naming issue #346; the assertion near line 648 (shipped commands minus this set equal the frozen inventory) stays as is. Source: source.md 3.4 (row `tests/recommend/test_routing_refresh.py`). The source.md 3.4 edit of `tests/skills/test_worker_contract.py` is NOT made: the variant has no `## Unattended mode` section (owner ruling in Constraints), so that test's 31-command set already holds.

Acceptance criteria:
- `uv run pytest tests/recommend/test_routing_refresh.py tests/skills/test_worker_contract.py -v` passes.
- `git diff --exit-code -- tests/skills/test_worker_contract.py` exits 0 (file unedited).
```

### .dev/tasks/to-do/TASK-WF-spec-20261108-181640/TASK-WF-spec-20261108-181640.md:158-179

```markdown
- `.dev/brainstorms/346-diffgate/INSTALL.md` exists and contains a table with one row per created or edited file listed above, each with its repo path and its `~/.claude/` destination or "not installed", and a sentence that the variant has no `## Unattended mode` section on purpose.
- It contains the exact substitution line and the exact reviser line from source.md section 4, the three `sha256sum`/`cp`/`mkdir -p` install lines, and the string `superclaude install --force` inside a "never run" warning.
- Every repo path in the table exists on disk, except the `.dev/brainstorms/346-diffgate/briefs/` row that Task 12 creates (checked with `test -e` for each; output saved to `./artifacts/t11-paths.log`).

## Task 12: Create the S1 brief templates and scoring note under `briefs/`

Depends on: Task 11

Inputs: the six original S1 briefs named in the Constraints owner ruling (read-only; each is one line of 1,014 to 1,894 bytes). Base: the originals (control briefs), not the filled Arm B versions, because source.md section 4 removes any `--re-review ... --baseline ...` clause anyway and section 5 says "the same verbatim briefs with only the section 4 substitutions".

Create, under `.dev/brainstorms/346-diffgate/briefs/`:
- `source/` holding byte copies of the six originals under their original file names (`T05-R1-reviewer-L11-699ae853.txt` ... `T10-R3-reviser-L10-458bdc00.txt`), so every template can be diffed inside this worktree.
- `T05-R1-reviewer.txt`, `T07-R2-reviewer.txt`, `T09-R3-reviewer.txt`: verbatim copies of T05, T07, T09 where the one command token `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` becomes `/sc:spec-panel-diffgate @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --diffgate-dir <one directory per replicate> --expect-round 1` (2 for T07, 3 for T09), per source.md section 4. The originals carry no `--re-review` or `--baseline` clause, so nothing is removed. Every other byte stays, including both occurrences of "any finding of any severity is FAIL" (T07 and T09; the owner decision keeps the review-3 brief text verbatim) and the old repo-root path.
- `T06-R1-reviser.txt`, `T08-R2-reviser.txt`: verbatim copies of T06 and T08 with the one reviser line of source.md section 4 appended after one space, with `<N>` filled as 1 and 2 and `<spec>` filled as `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `<DIR>` stays a placeholder.
- `T10-R3-reviser.txt`: a byte copy of T10. source.md section 4 adds the reviser line to the two fix-cycle briefs only and section 2 writes no reviser brief at review 3, so T10 gets no change; README flags this as a coordinator decision (whether T10 runs in the diffgate arm, given that source.md section 5 measures growth "after fix cycle 2").
- `T11-blindness-audit.txt`: the inserted task source.md section 5 makes mandatory for every arm, written in the style of T05: run after the arm's last task in a new session with no diffgate directory, `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (the plain command, no `--unattended`, as the S1 briefs never pass it), save to `.dev/orca-command-refactor/review/blindness-audit.md` with a numbered findings list (finding, severity, spec section, evidence path:line), and classify each blocking finding as either fix-written text the loop closed (text that differs from the original spec at base commit `2cb683f5`) or text present since the original; same repo-root, ownership, citation and `worker_done` sentences as T05.
- `README.md`: one row per template with its source file and its exact change; the rule that `<one directory per replicate>` and `<DIR>` are the same directory, unique per replicate; the T10 coordinator decision above; and the scoring note: `R3-proxy-all` per source.md section 5 with the owner decision that deferred, demoted and withdrawn critical+major findings stay counted, read for the treatment arm from `proxy_all` in `<DIR>/result-r3.json` and recomputed by hand for the control and Arm B from their reports; plus the blindness-audit classification rule.

Acceptance criteria:
- The six files under `.dev/brainstorms/346-diffgate/briefs/source/` are byte-identical to the originals (`cmp` each; output saved to `./artifacts/t12-cmp.log`), and the originals are unmodified.
- `diff` of each template against its source shows exactly: one changed command token with `-diffgate` and the two added arguments (T05, T07, T09); one appended reviser line (T06, T08); no change (T10). The diffs are saved to `./artifacts/t12-brief-diffs.log`.
- `grep -o 'any finding of any severity is FAIL' .dev/brainstorms/346-diffgate/briefs/T09-R3-reviewer.txt | wc -l` equals the same count on the T09 original, and likewise for T07.
```

### src/superclaude/commands/spec-panel.md:19-24

```markdown
## Usage

```text
/sc:spec-panel [specification_content|@file] [--mode discussion|critique|socratic] [--experts "name1,name2"] [--focus area1,area2,...] [--iterations N] [--format standard|structured|detailed] [--re-review <prior-findings-file> --baseline <saved-copy>]
/sc:spec-panel [specification_content|@file] [--target-release <release>] [--output <file>] [--unattended] [--report-dir <dir>] [--improve]
```
```

### src/superclaude/cli/install_skills.py:40-60

```python
def _has_corresponding_command(skill_name: str) -> bool:
    """Check if an sc-* skill is fully served by a matching slash command.

    For example, a bare skill "sc-foo" has a command if
    src/superclaude/commands/foo.md exists. A command that activates the skill
    by name is only an entry point, so the backing skill must remain installed.

    Note: this strips ONLY the "sc-" prefix. Protocol skills named
    "sc-<command>-protocol" therefore do NOT match commands/<command>.md and
    are correctly installed standalone (their /sc: command activates them by
    name). Do NOT add "-protocol" stripping here — see module docstring.
    """
    if not skill_name.startswith("sc-"):
        return False
    cmd_name = skill_name[3:]  # strip "sc-" prefix only (NOT a "-protocol" suffix)
    package_root = Path(__file__).resolve().parent.parent
    command_path = package_root / "commands" / f"{cmd_name}.md"
    return command_path.exists() and skill_name not in skill_activation_targets(
        command_path
    )

```

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-008..INF-014 variant command edits (source.md:70-99) | Task 6 | covered; INF-014 departs by owner ruling | plan:97-102 |
| INF-023 UNATTENDED_VARIANTS test edit (source.md:157) | Task 8 | not done by owner ruling | plan:118-124 |
| INF-028..INF-033 install note and briefs (source.md:170-201) | Tasks 11, 12 | covered | plan:146-179 |
