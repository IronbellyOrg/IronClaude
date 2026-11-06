# Grounding hunks (Wave 1A)

### .dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:1-1
```text
Write the P1 STATIC plan for the Orca worker contract, per .dev/orca-command-refactor/specs/orca-worker-contract-spec.md section 6 (row P1), section 7.1 and 7.3 (P1 checks) and the section 3 rows of the P1 commands, applying decisions/APPROVED.md. Static plan only: the edits and the checks that need no live Orca run. The live plan is written later.
```

### .dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:5-5
```text
Phase P1 scope (spec section 6, table row P1; section 7.3 per-phase checks; section 3 command rows): the WC-4 contract, the report-directory rule, the flag parse rule and the person-mode refusal (section 2.1) for the P1 commands only; --unattended is added to a command only in the phase that converts its gates; output flags for commands that lack one; the small fixes to ready commands. P1 commands, 16 of which accept --unattended after P1: adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow (ready, no gate change) and analyze, build, business-panel, design, document, explain, index, test (no gate). /sc:load gets its usage-line fix only and never gains the flag.
```

### .dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:9-9
```text
The plan must have, per step: the exact files to edit (installed-path rules apply: never hardcode src/superclaude/ paths inside installed primitives; edit the src/superclaude/ sources and run make sync-dev), acceptance criteria that are observable (a command, a grep, a test), and the tests to add or extend (tests/skills/test_worker_contract.py and the per-command tests). Include the static checks of section 7.1 and 7.3 that apply to P1 (AC-1.1, AC-1.4, AC-C1 to AC-C6), make lint, the ruff format check, make verify-sync, and the pre-existing tests that read the edited files.
```

### .dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md:24-24
```text
- Section skeleton. Every `## Unattended mode` section is a level-2 heading written exactly like that, placed immediately before the file's final boundaries heading (`## Boundaries`, or `## CRITICAL BOUNDARIES` in business-panel.md; in index-repo.md after `## Output Format`), and holds only the command's own resolutions. It contains, in this order: an opening sentence that names `~/.claude/WORKER-CONTRACT.md` as the home of the shared rules and tells the reader to read it first; the switch (applies only when `--unattended` is a standalone argument token outside any quoted argument, otherwise nothing in the section applies and no contract is written: spec SA-1 and SA-3); the report directory (exactly one of `--report-dir <dir>` or the command's own directory flag, named per task; if the command has none, `--report-dir` only); the contract (`<report-dir>/return-contract.yaml` written on ev
```

### .dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md:39-40
```text
- Check ADDITIVE (spec AC-C5 / SA-4). For every command file a task edits, `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/commands/<name>.md | awk '$2 != 0'` prints nothing. Edits to command files are added lines; an existing line is never reworded. The only two command files exempt are `business-panel.md` (the frontmatter move deletes the fence lines) and `load.md` (the usage-line fix replaces one line); their tasks say so. Skill and test files have no such rule.
- Check WRITEVERB (spec AC-0.9). New text in any command or skill file must not contain the audit's write-verb phrases: `git add`, `git commit`, `git push`, `git merge`, `git stash`, `git update-ref`, `git worktree add` or `remove`, `gh pr`, `gh api`. The test `tests/skills/test_worker_contract.py::test_every_write_verb_hit_is_classified` and `::test_classification_table_has_no_stale_entries` must still pass, so no classified line is edited. The one classified P1 line is the `.dev/tasks/` staging sentence in `src/superclaude/skills/sc-workflow-protocol/SKILL.md` (category `deferred:P1`); it stays word for word.
```

### .dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md:43-43
```text
- Decisions this plan makes where the spec is silent or ambiguous (each is also reported to the coordinator). D-P1-1: graph and impact already write a `command` key holding the short name (`graph`, `impact`) in their own contract; the spec's worker field `command` has the same key. The existing key is kept as is (spec WC-4: an existing contract keeps every existing field), counts as the worker `command` field, and no second key is added. D-P1-2: for the seven report-style no-gate commands (analyze, build, design, explain, index, test, business-panel) `--output <file>` is new and optional; under `--unattended` without it the report goes to `<report-dir>/<name>-report.md`, so the contract always has a `report_path`. D-P1-3: brainstorm's own status `dry-run` maps to `worker_status: succeeded` with `report_path: null` (the spec's mapping list lacks it). D-P1-4: the nested propagation rule (s
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:58-58
```text
- **Report directory**: the directory that holds the worker contract (WC-4). Under `--unattended` the brief passes exactly one: either the command's own existing directory-valued output flag (`--output <dir>` or `--output-dir <dir>`), or the new flag `--report-dir <dir>` (for a command without such a flag, or a brief that does not pass it). An output flag a section 3 row adds is file-valued, so those commands always take `--report-dir`. Passing neither, or both, is refused before any work (WC-4, last sentences).
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:62-62
```text
- **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). The caller lists the nested contract in its `artifacts`; only the top-level contract drives WC-5. When the invoked command does not accept the flag yet, that step must be gate-free per its section 3 row, or the caller skips it under `--unattended` and records the skip in its contract. Each command's `## Unattended mode` section names its nested invocations.
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:221-221
```text
| **P1. Report files and commands with no gate** | The WC-4 contract, the report-directory rule, the flag parse rule and the person-mode refusal (section 2.1) for the P1 commands only; `--unattended` is added to a command only in the phase that converts its gates, so no command accepts the flag while it can still prompt; output flags for commands that lack one; the small fixes to ready commands. | `--unattended` added to: adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow (ready, no gate change) and analyze, build, business-panel, design, document, explain, index, test (no gate). Also: load usage line only. | No person gate is involved, so each change is mechanical and gives every later phase a report file to check. |
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:317-317
```text
| P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command listed for P1 in the section 6 table of commands accepting `--unattended` has a `## Unattended mode` section naming `return-contract.yaml`, `~/.claude/WORKER-CONTRACT.md` and its report directory flag, and that no other command has one yet (load, pr-submit under D3 (a), the section 4 commands, and the P2-P4 commands until their phase). Each later phase extends the list to its own commands. The test also asserts that `WORKER-CONTRACT.md` states the brief guard (its four refusal conditions, the three exact reason texts, and the `guard refused:` prefix for case 3), the never-as-worker list and the nested propagation rule; that the brief template carries the guard line before the `Command:` lines; and that brainstorm's `## Unattended mode` section turns automatic research enrichment o
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:320-320
```text
| P1 | AC-1.4 | `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | adversarial names `<output>/adversarial/return-contract.yaml` as its own contract, and its `## Unattended mode` section names `<output>/return-contract.yaml` as the worker contract that lists that file in `artifacts` (WC-4); workflow states that under `--unattended` the worker contract is written in `--report-dir` for pre-creation STOPs |
```

### .dev/orca-command-refactor/specs/orca-worker-contract-spec.md:236-238
```text
`/sc:load` never gains the flag (it is used inside another worker's brief, section 3.2), and under D3 (a) neither does pr-submit, so 37 + load + pr-submit = 39 = the 12 + 27 commands of sections 3.1-3.2.

Each phase is one written plan executed under the repo's level-3 route (`/sc:workflow`, then `/sc:implement` when execution is requested), because each touches more than one source file (hard limit at `src/superclaude/core/CLAUDE.md:66` and `src/superclaude/core/HOW-WE-WORK.md:22`). Because the 7.2 live checks need the owner's commit and install approvals, and `/sc:implement` may not prompt the user outside its halt paths (`sk/sc-implement-protocol/refs/qa.md:288`), each phase's plan comes in two parts. The static plan holds the edits and the checks that need no live Orca run. The live plan holds the 7.2 live checks and the phase report. Between them, the coordinator session asks the owner, commits and installs as 7.2 states, outside any plan run. The live plan is written after the static plan's checks pass, and the phase passes only when both plans' checks pass.
```

### tests/skills/test_worker_contract.py:253-255
```python
# Commands with an `## Unattended mode` section after P0 (./source.md section 6
# table: none). Later phases extend this set.
UNATTENDED_COMMANDS: frozenset = frozenset()
```

### tests/skills/test_worker_contract.py:340-348
```python
def _check_no_unattended_sections() -> None:
    have = sorted(
        p.stem
        for p in Path(_THIS.COMMANDS_DIR).glob("*.md")
        if re.search(r"^## Unattended mode\s*$", p.read_text(encoding="utf-8"), re.M)
    )
    assert set(have) == set(UNATTENDED_COMMANDS), (
        f"unexpected `## Unattended mode` sections: {have}"
    )
```

### tests/skills/test_worker_contract.py:1415-1422
```python
    (
        "src/superclaude/skills/sc-workflow-protocol/SKILL.md",
        "git add",
        '`.dev/tasks/` is always staged (`git add .dev/tasks`): the package and its `artifacts/` included. Never gitignore it, never leave it untracked, and never write "never stage" about it in a generated plan (Constraints included). Staging is not committing.',
    ): (
        "deferred:P1",
        "/sc:workflow is converted in P1; under --unattended its .dev/tasks staging defers to the coordinator (WC-9)",
    ),
```

### tests/commands/test_workflow_command.py:115-127
```python
def test_output_flag_is_retired_everywhere():
    assert "--output" not in re.search(
        r"^argument-hint:.*$", _CMD.read_text(encoding="utf-8"), re.M
    ).group(0)
    skill = (_SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "--output" not in re.search(r"^argument-hint:.*$", skill, re.M).group(0)
    for name, text in _workflow_texts():
        for line in text.splitlines():
            if "--output" in line:
                assert re.search(r"retired|E-LEGACY|Never", line), (name, line)
    parse = _ref("input-parse.md")
    assert re.search(r"`E-LEGACY`\s*\|[^|]*`--output`", parse)
    assert "E-OUTPUT-PATH" not in parse and "E-MISSING-DIR" not in parse
```

### tests/commands/test_graph_command.py:126-131
```python
def test_graph_command_allowed_tools_exact():
    assert _allowed(_COMMAND) == {
        "Skill",
        "Bash(codegraph init --yes *)",
        "Bash(codegraph init -i)",
    }
```

### tests/commands/test_graph_command.py:140-152
```python
def test_graph_init_only_in_command():
    assert not _MUTATING.findall(_text(_SKILL)), (
        "the skill must never name a build or write verb"
    )
    hits = _MUTATING.findall(_text(_COMMAND))
    assert hits and all(h == "codegraph init" for h in hits)


def test_graph_init_user_typed_guard():
    init = _section(_text(_COMMAND), "## Init (user-typed only)")
    assert "/sc:graph init" in init
    assert "user's own message starts with `/sc:graph init`" in init

```

### src/superclaude/commands/README.md:9-9
```text
3. If you changed `help.md`, `recommend.md`, `workflow.md` or `implement.md`, copy it byte-for-byte to `plugins/superclaude/commands/` (parity tests check these four).
```

### src/superclaude/commands/graph.md:44-53
```text
## Init (user-typed only)

These steps run only for `init`, after the skill's preflight returned `init.form` (`default` or `worktree_local`) and no refusal:

1. **Guard.** Continue only if the user's own message starts with `/sc:graph init`. Otherwise print "init runs only when you type it" and stop. A skill, an agent or another command never reaches the steps below.
2. **Run once** (timeout 600000 ms), exactly one of:
   - `form: default` → `codegraph init --yes <worktree_root>`
   - `form: worktree_local` → `codegraph init -i`, run in `worktree_root` (the skill refused with `cwd_mismatch` if the session is elsewhere). In codegraph 1.6.2 `-i` is a deprecated alias that is still accepted, and init inside a nested worktree builds its own `.codegraph/` (Phase 3 experiment E-2).
   Record the exit code. Never prefix the call with environment variables.
3. **Verify.** Invoke `> Skill sc:graph-protocol` again with `status --post-init <exit-code>`, plus the user's `--output-dir` if given. The skill re-checks the index once and reports `success`, `partial` or `failed`.
```

### src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:183-186
```text
   | `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | Invoke `/sc:analyze <relevant-paths> --focus quality --depth quick` OR `mcp__auggie__codebase-retrieval` for quick scan | `enrichment/codebase-context.md` |
   | `--codebase` (forced) | Same as above regardless of domain | Same |
   | `--research light` OR (auto: topic mentions framework/library names not in project) | Invoke `Skill sc-research-protocol` with `--depth quick` (or `/sc:research` if standalone) | `enrichment/research-light.md` |
   | `--research deep` OR (auto: `--strategy enterprise` + novel topic) | Invoke `Skill tech-research` with topic | `enrichment/research-deep.md` |
```

### src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:265-273
```text
1. **Build adversarial invocation arguments**:

   ```
   --source <output>/seed-brief.md
   --generate spec
   --agents <composed-spec-from-Wave-2B>
   --depth <passthrough>
   --convergence <passthrough, default 0.75>
   --output <output>/adversarial/
```

### src/superclaude/skills/sc-adversarial-protocol/SKILL.md:425-436
```text
## Return Contract (MANDATORY)

**This is the final pipeline step.** sc:adversarial MUST write this return contract on every invocation, including failures. When a field's value cannot be determined (pipeline aborted before reaching that step), use `null`.

When invoked by another command, sc:adversarial returns:

```yaml
return_contract:
  merged_output_path: "<path to merged file>"       # null if merge not reached
  convergence_score: 0.75                            # float 0.0-1.0, null if debate not reached
  artifacts_dir: "<path to adversarial/ directory>"  # always set (created at pipeline start)
  status: "success"                                  # success | partial | failed
```

### src/superclaude/skills/sc-workflow-protocol/SKILL.md:28-28
```text
`.dev/tasks/` is always staged (`git add .dev/tasks`): the package and its `artifacts/` included. Never gitignore it, never leave it untracked, and never write "never stage" about it in a generated plan (Constraints included). Staging is not committing.
```

### src/superclaude/skills/sc-init-lite-protocol/SKILL.md:61-66
```text
1. **Read-only context inputs** — never modify `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**`, `.claude/skills/**`, or `.claude/agents/**` under ANY flag combination.
2. **Dry-run writes nothing** — and does not create `.dev/superclaude/`.
3. **Default = report only** — the only write is the marked report at `output`.
4. **Scaffold is opt-in and scoped** — exactly two files under `.dev/superclaude/project-guidance/`.
5. **`--force` is scope-limited** — marker-less overwrites are allowed only for init-lite-owned targets under `.dev/superclaude/`; never for files elsewhere, and never for a context input.
6. **No marker, no `--force`** — if `output` exists without the generated marker, fail with a clear error rather than overwrite. Marked reports may be overwritten on re-run at the default path or at an explicit `--output` path.
```

### src/superclaude/commands/business-panel.md:1-11
```text
# /sc:business-panel - Business Panel Analysis System

```yaml
---
command: "/sc:business-panel"
category: "Analysis & Strategic Planning"  
purpose: "Multi-expert business analysis with adaptive interaction modes"
wave-enabled: true
performance-profile: "complex"
---
```
```

