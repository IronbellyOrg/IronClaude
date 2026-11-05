# Reflect Report: issue #330 Ponytail (lite) plan, pre-execution

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.77
citations_total: 59
citations_revalidated: 58
citations_dropped: 1
citations_inferred: 5
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 58` of 59.
> - `citations_dropped: 1` (sample count; this gates promotion).
> - `citations_dropped_extrapolated: 1`.
> The extrapolated value is telemetry, not a verdict.

- Plan: `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/TASK-WF-closeIronbellyOr-20261104-124207.md`
- Spec: `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/source.md`
- Tier 2: three read-only reviewers (sonnet/analyzer, glm-5.3/qa, opus/refactorer), blind calibration (0.76, 0.76, 0.79), adversarial merge (`adversarial/merged-verdict.yaml`, merge_method adversarial, convergence 1.0, invariant gate blocked by INV-001, carried as finding M-2).
- Status is `partial` because one citation was dropped (M-2's `mode-tracker.js:143-148` does not support the "other sessions" sub-claim). This reflect run is advisory: the plan is not edited; every finding below is an instruction for the implementer.

## Verdict

**needs_revision.** The plan delivers the spec structurally (scope, files, tests, checks), but Task 3 would ship two false sentences about Ponytail's mode switching. Both must be corrected while implementing Task 3.

## Findings

### Deviation D-001: bare `/ponytail` does not switch to `full` under lite (blocking)

- **Location:** TASK-WF-closeIronbellyOr-20261104-124207.md:80
- **Mapped tasklist item:** Task 3
- **Spec section:** source.md:1 ("Docs must say how to change the mode")
- **Evidence:** `/tmp/ponytail-src-t14b/mode-tracker.js:109-119`; line 117 `mode = getDefaultMode() === 'off' ? 'full' : getDefaultMode()`; lines 113-115 report-only when already on.
- **Classification:** drift (off-era brainstorm text carried into a lite plan, merged-requirements.md:140,171)
- **Default remediation:** In the docs write: bare `/ponytail` reports the current level when Ponytail is on, and switches it on at the default level (lite) when it is off (`full` if the default is `off`).

### Deviation D-002: mode-switch scope is wrong (blocking)

- **Location:** TASK-WF-closeIronbellyOr-20261104-124207.md:80
- **Mapped tasklist item:** Task 3
- **Spec section:** source.md:1
- **Evidence:** `/tmp/ponytail-src-t14b/hooks_claude-codex-hooks.json:5` (SessionStart matcher `startup|resume|clear|compact`); `hooks_ponytail-activate.js:193,55` (every non-compact start writes the default); `runtime.js:51-66,75-78` (one flag per project directory, keyed by CLAUDE_PROJECT_DIR).
- **Classification:** drift
- **Default remediation:** Say a switch is stored per project directory (each worktree separately), and any new session, `/clear` or resume in that directory resets it to the default for every session there.
- **[INFERRED] notes:** [INFERRED] Other running sessions see a switch only through their subagents (its citation was dropped; `hooks_ponytail-subagent.js:17-26` would support the subagent half).

### Minor findings (instructions for implementation)

- **R3-1** Run the manual proof as `env -u CLAUDE_CONFIG_DIR -u XDG_CONFIG_HOME -u PONYTAIL_DEFAULT_MODE -u PONYTAIL_MAP -u PONYTAIL_SUBAGENT_MATCHER HOME=<throwaway> ...` (`src/superclaude/cli/install_mcp.py:721-726`; `hooks_ponytail-config.js:55-56,71-74`). Not blocking: [INFERRED] both config variables were unset in this worker at 12:48Z.
- **R3-2** Read Task 2's cap as `git diff --numstat` at most 5 insertions and 5 deletions, all inside `install_plugins` (minimal fix is 4 + 3; `install_user_setup.py:292,303,305`).
- **R3-4** After Task 3 run `uv run pytest tests/docs -v` (`tests/docs/test_retired_docs_absent.py:39-44`, `tests/docs/test_tavily_doc_alignment.py:117`) and markdownlint on `docs/getting-started/installation.md` (`.pre-commit-config.yaml:73-88`).
- **R3-5** Source or drop the two claims outside the lite facts: "a project `.claude/settings.json` wins" (plan:81) and "do not only run `claude plugin uninstall`".
- **R3-6** Use the expanded JSON form matching `user_settings_defaults.json:36-48`.
- **R3-7** CHANGELOG links the installation guide file; no new heading.
- **R3-8** In the proof, record whether Orca was on PATH and the time it used (`install_user_setup.py:34-35`).
- **R3-9** `./artifacts/` means the plan package's `artifacts/` folder.
- **M-3** Describe lite accurately: it injects Ponytail's whole rule set plus the lite row (`instructions.js:19-40`, `skill.md:15-44`), including "end your reply with one or two lines"; Ponytail's files follow `CLAUDE_CONFIG_DIR` while the installer writes `$HOME/.claude`; the statusline note goes to whichever session starts first; "stop ponytail" / "normal mode" also turn it off; `PONYTAIL_SUBAGENT_MATCHER` fails open; name the `ledger` option only as Ponytail's option with its upstream default unless the setting location is verified.
- **M-4** The Known Limitation should say the extra marketplace clone can also push the other default plugins past the 30 s budget (`install_user_setup.py:272-284`).
- **R3-3** Informational: Task 2 does not truly depend on Task 1; sequential order is safe.
- **Note (A-001):** docs and CHANGELOG say behaviour was checked against Ponytail v5.3.3; the proof records the installed version.

## Coverage

- Requirement extraction: parsed 0, inferred 17 (`artifacts/coverage-matrix.json`); `coverage_pct_union` 0.5294 by containment matching; `coverage_degraded: parsed-sparse` forced Tier 2.
- All three reviewers and the merge agree the eight containment-unmapped rows (INF-001, -002, -003, -005, -007, -014, -015, -017) are owned by plan elements outside a single task's wording (header, Constraints, Tasks 1-4). No requirement is missing from the plan.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote (abridged) | Citation | Match result |
|---|---|---|---|
| INF-001 | implementing .../merged-requirements.md | source.md:1 | none (plan header) |
| INF-002 | env.PONYTAIL_DEFAULT_MODE='lite' ... filled only when the user has not set it | source.md:1 | none (Task 1 + Constraints) |
| INF-003 | every place the brainstorm says 'off' ... is rewritten to lite | source.md:1 | none (Tasks 1, 3, 4) |
| INF-004 | no pluginConfigs entry; ... ledger is on | source.md:1 | Task 3 |
| INF-005 | SessionStart writes the mode flag ... | source.md:1 | none (lite block, Task 3) |
| INF-006 | appends a codebase map ... SubagentStart injects | source.md:1 | Task 3 |
| INF-007 | lite DOES emit a one-time 'STATUSLINE SETUP NEEDED' nudge | source.md:1 | none (lite block, Task 3) |
| INF-008 | /ponytail default <mode> has no effect while the env key is set | source.md:1 | Task 3 |
| INF-009 | Docs must say how to change the mode ... and how to opt out | source.md:1 | Task 3 |
| INF-010 | user_settings_defaults.json (three entries ...) | source.md:1 | Task 1 |
| INF-011 | install_user_setup.py (FR-005 ... at most 5 changed lines) | source.md:1 | Task 2 |
| INF-012 | tests/cli/test_install_user_setup.py (T1, T2, T3/T4, T5, T5c ...) | source.md:1 | Task 1 |
| INF-013 | docs/getting-started/installation.md ... CHANGELOG.md [Unreleased] | source.md:1 | Task 3 |
| INF-014 | No change to main.py, update.sh, doctor.py, output styles, primitives or .claude/. | source.md:1 | none (Constraints) |
| INF-015 | Checks: uv run pytest ... make verify-sync, grep ... | source.md:1 | none (Tasks 2, 3, 4) |
| INF-016 | Manual AC-M1 ... non-blocking ... never touch ~/.claude | source.md:1 | Task 4 |
| INF-017 | The earlier plan package ... is superseded; leave it untouched. | source.md:1 | none (Constraints) |

Postscript: no INF row dropped (each quote was asserted verbatim against source.md by the extraction script).

## Inferred-claim audit

- `citations_inferred: 5`
- Inferred-fraction: 5 / 59 = 0.08

## Recommendations

### Recommendation R-001: Correct the bare `/ponytail` sentence

- **File:** docs/getting-started/installation.md (Task 3), CHANGELOG.md (Task 4)
- **Change:** State the report-when-on / default-when-off behaviour (full only when the default is off).
- **Verifier:** `grep -n "bare" docs/getting-started/installation.md` shows the corrected sentence; no sentence says bare `/ponytail` switches to `full` unconditionally.
- **Linked deviation(s):** D-001
- **Priority:** P0

### Recommendation R-002: Correct the mode-switch scope

- **File:** docs/getting-started/installation.md (Task 3)
- **Change:** Per project directory; reset by any new session, `/clear` or resume in that directory.
- **Verifier:** Re-read the paragraph against `hooks_claude-codex-hooks.json:5` and `hooks_ponytail-activate.js:193`.
- **Linked deviation(s):** D-002
- **Priority:** P0

### Recommendation R-003: Add the docs checks

- **File:** n/a (verification run)
- **Change:** Run `uv run pytest tests/docs -v` and markdownlint on installation.md after Task 3.
- **Verifier:** both exit 0.
- **Linked deviation(s):** none
- **Priority:** P1

### Recommendation R-004: Harden the manual proof environment

- **File:** n/a (Task 4 proof)
- **Change:** Use the `env -u ...` prefix above; record Orca presence, time used and the installed Ponytail version.
- **Verifier:** the proof log shows no `CLAUDE_CONFIG_DIR`, `XDG_CONFIG_HOME` or `PONYTAIL_*` inside the isolated run.
- **Linked deviation(s):** none
- **Priority:** P1
