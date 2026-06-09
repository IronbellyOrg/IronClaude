# Research 03 — Template & Tests (Template-02 rules + pytest conventions for the prd CLI)

Status: Complete
Topic: MDTM template 02 PART 1 rules + pytest conventions for prd CLI tests.
Repo: /config/workspace/IronClaude

---

## 1. MDTM Template-02 PART 1 rules the builder MUST follow

Source: `.claude/templates/workflow/02_mdtm_template_complex_task.md` (PART 1 = lines 63–1141; PART 2 template body = lines 1143–1516).

### A3 — Complete Granular Breakdown (lines 108–112)
> "Break down EVERY workflow phase into atomic, verifiable checklist items / Create individual checklist items for EVERY file, component, or iteration / NO high-level or bulk operations allowed — everything must be granular / Include exact file paths, specific requirements, and measurable outcomes."

For this task: each `--file`-removal edit site in `process.py` (refs branch, spec branch, `_build_file_args` removal, dead constants, docstrings) and each `prompts.py` edit (`_authoritative_specs_block` upgrade) is its own checklist item with the exact line anchors from the spec §5. Each new/inverted test is its own item.

### B2 — Self-contained item (lines 159–166): every checklist item is ONE paragraph carrying all six elements
1. **Context Reference with WHY** — which file(s) to read and why.
2. **Action with WHY** — what to do and why.
3. **Output Specification** — exact output file path/name/content/template.
4. **Integrated Verification** — an "ensuring…" clause; NO separate verification items (B4 NOTE lines 177–179; C3 lines 236–240; I12 lines 609–614).
5. **Evidence on Failure Only** — log to a `### Phase N Findings` block in `## Task Log / Notes` ONLY on blocker; success is evidenced by the output file (B7.4 line 210).
6. **Explicit Completion Gate** — close with: "This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete." (line 165).

Pattern: ONE verbose paragraph, not bullets (B3 lines 167–170). Verification embedded as "ensuring…" clause (C2 lines 230–234). The CORRECT canonical example is at lines 172–175.

**B5 FORBIDDEN patterns (lines 181–201):** standalone "read context" items with no output; missing context reference; multi-line/bulleted items; separate verification/confirmation items; over-granular items ("create directory" alone); separate REMINDER blocks between items.

### Phase ordering / checklist structure (Section E, lines 291–405; E2/E3)
- Flat checkboxes only — NO nested/parent checkboxes (E1 lines 295–309). Use bold `**Step X.Y:**` headers for grouping, NOT checkboxes (E1, E4 lines 384–405).
- **FUNDAMENTAL RULE (E2 lines 312–315):** "Summary/parent checkboxes MUST come AFTER all their component items"; never place a parent/summary before its components.
- **Sequential, top-to-bottom only (E3 lines 367–383):** checkboxes appear in exact completion order; NEVER require marking items above the current position; "Each phase must complete ALL its checkboxes before moving to next phase." FORBIDDEN: "see checklist below", "return to phase and mark complete", any backward movement.
- Phases run in order (PART 2 skeleton, lines 1404–1421): Phase 1 Preparation/Setup → Phase 2 execution (Discovery → Build → Test → Assess, lines 1349–1363) → optional Phase Gate QA → Phase N Testing & Verification (lines 1404–1410) → Phase 3 Review → `## Post-Completion Actions`.
- **D3 CRITICAL RULE (lines 286–290):** NO checklist items may appear before Phase 1 begins. Frontmatter → (Workflow Compliance / Prerequisites, informational) → Phase 1 (first executable items).

### Anti-orphaning — completion items in the FINAL phase (`## Post-Completion Actions`, PART 2 lines 1423–1441)
The Post-Completion Actions sequence (template order, lines 1425–1441):
1. Glob-verify all output files exist (line 1425).
2. If source code modified, run the test suite to confirm no regressions (line 1427).
3. Post-completion lens-based QA placeholder (line 1435) and source-fidelity placeholder (line 1437) — per I17 lines 675–686 (see §1a note below on whether these apply).
4. **Task Summary** item — write `### Task Summary` at top of `## Task Log / Notes` (line 1439).
5. **LAST item = frontmatter Done-flip** — "Update `completion_date` and `updated_date` … update task status to '🟢 Done' … add an entry to the ### Execution Log" (line 1441).

The **Done-flip frontmatter item is the absolute last item** (anti-orphaning: completion items live in the final phase, nothing after the Done item). F5 (lines 464–469): status → "🟠 Doing" + start_date is the FIRST action; status → "🟢 Done" + completion_date on completion.

### Where the POST reflect item sits — PENULTIMATE, immediately before Update-status-to-Done
PART 1 of template 02 does **not** itself contain a "POST reflect" placement rule; the rule is injected by the **task-builder skill** (`src/superclaude/skills/task-builder/SKILL.md`), which the template frontmatter accommodates via `reflect_post: ""` (line 32: "POST reflect verdict; recorded by the executor after the final-phase reflect subagent runs") and `reflect_pre:` (lines 24–31).

The authoritative POST-placement wording is task-builder **Critical Rule #19**, verified verbatim from a recent generated task that implemented it (`.dev/tasks/to-do/TASK-RF-20260604-042055/TASK-RF-20260604-042055.md:192`):
> "when `POST_REFLECT_GATE: ENABLED`, the builder MUST emit, **as the penultimate item of the final phase (immediately before the Update-status-to-Done item, preserving anti-orphaning)**, a fresh-session reflect handoff item that writes `reflect_post: PENDING` and HALTs; a generated task file that omits the POST reflect item when POST_REFLECT_GATE is ENABLED is a MALFORMED output."

So: **… → Task Summary item → [POST reflect handoff item — penultimate, writes `reflect_post: PENDING`, HALTs] → Update-status-to-Done item (last).** The POST item uses `/sc:reflect --mode post …` (NEVER `/sc:task`), depth floored at `standard` (O4), command shape (from same example file `:200`): `/sc:reflect --mode post --remediate --diff <BASE>..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}`. A `start_commit` frontmatter key captures `<BASE>` (set as a Phase-1 item; see example `:158`).

### I18 — Testing requirements for code-modifying tasks (lines 688–697)
Because this task modifies source code (`process.py`, `prompts.py`), the builder MUST include ≥1 testing item that (1) specifies the test command, (2) defines pass criteria, (3) specifies where results are captured (`phase-outputs/test-results/`), (4) follows B2. Use the L3 (Test/Execute) pattern. The template's canonical pytest-capture item is at lines 961 and 1359 (run command 2>&1, write raw output `.txt` + structured `.md` summary).

### 1a. QA-gate note (single-track scope guidance)
Template I15 (lines 635–651) and I17 (lines 675–686) mandate multi-agent lens-based QA gates for tasks producing **documents**. This task's outputs are **source-code edits + unit tests** verified deterministically by `uv run pytest` + `grep` guard + `make verify-sync`. The strongest deterministic verification here is the test/grep/sync chain, not document lens-QA. The builder should treat the pytest/grep/verify-sync items as the mandatory verification (I18), and may keep the Post-Completion QA placeholders minimal or note "lens-based QA not applicable — code task verified by pytest + grep guard + verify-sync" if the builder's own rules permit (mirror how the model task at `TASK-RF-20260604-042055` used FINAL_ONLY regression gating rather than per-phase rf-qa spawns — see that file `:138`).

---

## 2. pytest conventions in `tests/cli/prd/`

### Layout, imports, no local conftest
- There is **NO** `tests/cli/prd/conftest.py` (verified — `ls` returns "NO prd conftest"). The only `conftest.py` in scope is the repo-wide `tests/conftest.py` (a session-scoped autouse `_pollution_snapshot` guard, `tests/conftest.py:30`), so prd tests rely on built-in pytest fixtures (`tmp_path`, `monkeypatch`, `capsys`) only.
- Tests use a **mix of classes and plain functions**. Classes group related cases (e.g. `class TestSpecFileAttach:` `tests/cli/prd/test_spec_flag.py:477`, `class TestPrdCliSmoke:` `tests/cli/prd/test_cli_smoke.py:18`). Plain module-level functions are also used (e.g. `def test_resolve_config_defaults_output_to_dev_eval_workspaces(...)` `tests/cli/prd/test_config.py:21`).
- Every file opens with `from __future__ import annotations` and imports directly from the package, e.g. `from superclaude.cli.prd.config import resolve_config` (`test_config.py:18`), `from superclaude.cli.prd.models import PrdConfig` (`test_spec_flag.py:33`), `from superclaude.cli.prd.process import PrdClaudeProcess` (`test_spec_flag.py:34`), `from superclaude.cli.prd.commands import prd_group` (`test_cli_smoke.py:12`).
- Test command is UV-only: `uv run pytest tests/cli/prd/ -v` (per CLAUDE.md + spec §7/§10).

### Concrete fixture-usage examples (file:line)
- **`tmp_path`** for scratch spec files: `test_spec_flag.py:85-89` (`a = tmp_path / "a.md"; a.write_text("# A\n", encoding="utf-8")`); `test_spec_flag.py:478-483`.
- **`monkeypatch.chdir`** to simulate repo CWD before `resolve_config`: `test_config.py:30` (`monkeypatch.chdir(tmp_path)`), `test_spec_flag.py:121-123`.
- **`capsys`** for stderr assertions: `test_spec_flag.py:378` (`def test_warn_emitted_to_stderr(self, tmp_path, capsys)`), reads `capsys.readouterr().err` at `:385`.
- **`CliRunner`** (Click) for command-surface tests: `test_cli_smoke.py:21` (`_runner().invoke(prd_group, ["--help"])`); `test_spec_flag.py:81` (`CliRunner().invoke(prd_group, ["run", "--help"])`).

### Existing tests that construct `PrdClaudeProcess` / `PrdConfig`
- **`PrdConfig` is constructed directly** (a dataclass). Two helper patterns in `test_spec_flag.py`:
  - `_scope_config` (`test_spec_flag.py:63-71`): `PrdConfig(user_message=..., product_name="TestProduct", product_slug="test-product", tier="standard", task_dir=task_dir)`.
  - `_spec_config` (`test_spec_flag.py:465-474`): `PrdConfig(user_message="x", product_name="P", product_slug="p", tier="standard", task_dir=tmp_path / "prd-p", skill_refs_dir=tmp_path / "refs", spec_files=spec_files)`.
  - Model-default tests instantiate the bare dataclass: `PrdConfig()` then assert `.spec_files == []` (`test_spec_flag.py:146-147, 149-153`).
  - Config-mode threading sets extra attrs post-construction: `cfg.work_dir = tmp_path` (`test_spec_flag.py:360`).
  - `resolve_config(...)` is the other construction path (returns a `PrdConfig`): `test_config.py:33`, `test_spec_flag.py:128, 136, 162`.
- **`PrdClaudeProcess` is NOT instantiated**; the relevant method `_build_file_args` is called as a **staticmethod on the class**: `PrdClaudeProcess._build_file_args(cfg, "scope-discovery")` (`test_spec_flag.py:485, 495, 506, 510, 515`). No `build_command` helper is referenced anywhere in `tests/cli/prd/` (grep returned zero hits for `build_command`).

### CRITICAL — the tests that the fix must INVERT
`tests/cli/prd/test_spec_flag.py` is the **only** test file referencing `_build_file_args` / `--file` (verified by grep across `tests/cli/prd/`). Its `class TestSpecFileAttach` (`test_spec_flag.py:459-515`) currently **asserts `--file` IS emitted** — these are the assertions the spec removes/inverts:
- `:485-487` `test_scope_discovery_attaches_each_spec` → asserts `args == ["--file", str(a), "--file", str(b)]`. Post-fix: must assert **no** `"--file"` (spec §7.1).
- `:489-498` `test_investigation_numbered_step_attaches_specs` → asserts `"--file" in args`. Post-fix: invert.
- `:500-506` `test_parse_request_does_not_attach_specs` → already asserts `== []` (stays valid).
- `:508-510` `test_no_specs_no_args` → asserts `== []` (stays valid).
- `:512-515` `test_missing_spec_file_skipped` → asserts `== []` (stays valid).
- Section banner `:459-462` ("spec content delivered via the existing --file mechanism") and helper comment `:472` ("intentionally absent → no ref args") describe the now-wrong behavior and need updating.
- If `_build_file_args` is removed entirely (spec §5.1 option), these tests must be deleted/rewritten to target the argv via whatever surface remains (e.g. assert `"--file"` not in the process's extra_args, or a repo-level grep guard per spec §7.4). The builder must decide based on R1's findings on whether `_build_file_args` stays returning `[]` or is deleted.

New tests the fix ADDS (spec §7.1–7.4), all constructible with the existing `PrdConfig` + `tmp_path` patterns above:
- §7.1 no `--file` emitted (scope-discovery + investigation, incl. >50 KB ref).
- §7.2 `_authoritative_specs_block([tmp_spec])` returns block containing the spec **content** + MUST-Read instruction; >50 KB spec truncated with `_TRUNCATION_MARKER` (import from `superclaude.cli.prd.prompts`; existing test already imports `_authoritative_specs_block` at `test_spec_flag.py:36`).
- §7.3 no-spec parity: `_authoritative_specs_block(None)`/`([])` → `""` (existing `test_helper_empty_returns_empty_string` `:310-312` already covers this — extend, do not duplicate).
- §7.4 repo-level grep guard: `"--file"` absent from `prd/process.py`.

---

## 3. `make sync-dev` / `make verify-sync` behavior for a cli-only change

Source: `Makefile` (`sync-dev:` line 109; `verify-sync:` line 166).

### What `sync-dev` copies (Makefile:109–164)
`sync-dev` copies ONLY these `src/superclaude/` subtrees into `.claude/`:
1. **skills** → `.claude/skills/` (loops `src/superclaude/skills/*/`, line 112).
2. **agents** → `.claude/agents/` (line 130).
3. **commands** → `.claude/commands/sc/` (line 137).
4. **hooks** → `.claude/hooks/` (`src/superclaude/hooks/scripts/*.sh` + `scripts/session-init.sh`, lines 144–153).
5. **templates** → `.claude/templates/` (line 154).

It does **NOT** touch `src/superclaude/cli/` (no cli/ loop exists). The summary echo (lines 159–164) reports counts for Skills/Agents/Commands/Hooks/Templates only.

### What `verify-sync` checks (Makefile:166–~260)
`verify-sync` diffs only: `=== Skills ===` (line 170), `=== Agents ===` (line 202), `=== Commands ===` (line 228), `=== Hooks ===` (line 254), and templates (further down). It does **NOT** check `src/superclaude/cli/`.

### Conclusion for this task
The fix touches **only** `src/superclaude/cli/prd/{process.py,prompts.py}` + `tests/cli/prd/` — **no skills/agents/commands/hooks/templates**. Therefore:
- `make sync-dev` is **functionally a no-op** for the code change (it will copy nothing new from cli/; cli/ is shipped via the Python package install, not the `.claude/` mirror).
- `make verify-sync` will report **clean** regardless, because it never inspects cli/.

The spec's acceptance criterion (§8: "`make sync-dev && make verify-sync` clean", §10 rollout) is satisfied by running the chain and confirming a clean exit — it is a **guard / regression confirmation that nothing unintended drifted in the synced surfaces**, NOT a required propagation step for the cli edit. The task should still run both (they are cheap and the spec lists them), but the builder should NOT add items that expect cli files to appear under `.claude/`. The substantive verification for a cli-only change is `uv run pytest` + the `grep -rn '"--file"' src/superclaude/cli/prd/` → 0 guard (spec §3, §7.4, §8).

---

## 4. Recent realistic example task to mirror

**Primary model:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260604-042055/TASK-RF-20260604-042055.md`

Why it is the best mirror for this build:
- Same shape: **source-tree edits under `src/superclaude/` + SoT-sync + regression pytest + verify-sync**, finishing with a **penultimate fresh-session POST reflect handoff** item before the Done-flip.
- Frontmatter to copy (verified `:1-61`): id/title/description, `status: "🟢 Done"`→ generate as "🟡 To Do", `assigned_to: "rf-task-executor"`, `autogen_method: "task-builder"`, `coordinator: orchestrator`, `related_docs:` list pointing at the spec + each research file, `template_schema_doc: "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md"`, `spec_path:`, `reflect_pre: ""`, `reflect_post:` (sign-off sub-block, `:50-54`), `start_commit:` (`:55`), `task_type: static`.
- Phase headers to mirror (verified via grep):
  - `### Phase 1: Preparation, Setup, and Anchor Re-Verification` (`:144`) — includes the `git rev-parse HEAD` → `start_commit` + baseline-pytest capture item (`:158`).
  - `### Phase 2: Implement Proposal 1 — …` (`:166`) — one self-contained B2 item per edit site (`:172, 176, 180, 184, 188, 192, 196, 200`), each ~one paragraph with read-anchor → action → ensuring-clause → blocker-log → "Once done, mark this item as complete."
  - A final verification phase + `## Post-Completion Actions` whose **penultimate** item is the `/sc:reflect --mode post` handoff (`:200` shows the command shape) and whose **last** item flips status to Done.
- Key-constraints prose block at `:138` is a good template for stating this task's constraints (REGRESSION + new-unit-tests, run pytest + grep guard + verify-sync, never stage the synced mirror, edits surgical/additive where possible).

**Secondary references (same directory):** `TASK-RF-20260603-024610/`, `TASK-RF-20260602-135209/` — other recent single-track RF tasks following the same frontmatter + phase skeleton.

---

## Summary

- **Template-02 rules:** A3 = atomic per-file/per-edit items; B2 = each item is ONE self-contained paragraph (context+WHY / action+WHY / output spec / "ensuring…" verification / blocker-log-on-failure-only / explicit completion gate) — no separate verification items (B4/C3/I12). Phases flat + strictly forward (E2/E3), no items before Phase 1 (D3). Anti-orphaning: `## Post-Completion Actions` ends with the Done-flip frontmatter item as the absolute last item. I18 mandates ≥1 pytest item for code changes. The **POST reflect item is task-builder Rule #19, not a template-02 rule** — it sits PENULTIMATE (immediately before Update-status-to-Done), writes `reflect_post: PENDING`, HALTs, uses `/sc:reflect --mode post --diff <BASE>..HEAD …` (never `/sc:task`); `<BASE>` captured into `start_commit` in Phase 1.
- **pytest conventions:** no prd-local conftest; built-in `tmp_path`/`monkeypatch`/`capsys`/Click `CliRunner` only; mix of classes + plain functions; direct imports from `superclaude.cli.prd.*`. `PrdConfig` constructed directly as a dataclass (helpers `_scope_config` `test_spec_flag.py:63`, `_spec_config` `:465` show fields user_message/product_name/product_slug/tier/task_dir/skill_refs_dir/spec_files) or via `resolve_config`. `PrdClaudeProcess` is never instantiated — `_build_file_args` is called as a staticmethod. **`test_spec_flag.py:459-515` (`TestSpecFileAttach`) is the only `--file` test and must be inverted/deleted.**
- **sync:** `make sync-dev`/`verify-sync` cover skills/agents/commands/hooks/templates ONLY — never `cli/`. A cli-only change makes `sync-dev` a no-op and `verify-sync` clean regardless; running them satisfies spec §8 as a drift guard, not a propagation step. Real verification = `uv run pytest` + `grep -rn '"--file"' src/superclaude/cli/prd/` → 0.
- **Example to mirror:** `.dev/tasks/to-do/TASK-RF-20260604-042055/TASK-RF-20260604-042055.md` — same source-edit + sync + regression + penultimate POST-reflect shape; copy its frontmatter and phase skeleton.



