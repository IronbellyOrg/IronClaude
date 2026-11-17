# Reviewer 3 brief (persona: refactorer)

You audit a PLAN (not code) before it is executed (UC-1, pre-execution). Read-only: do not run commands, edit files or write files; RETURN your findings as your final message. Audit ONLY the supplied hunks and matrices (plus what you can Read, Grep or Glob from the repo). For every finding give: id (F1..), severity (CRITICAL|MAJOR|MINOR), blocking (true|false), category, claim (one line), and citations as repo-relative path:line-range with a short verbatim quote. Tag a claim you cannot cite as [INFERRED]. Then give 'calibration_self: <0-1>' and 'reviewer_model_self_report: <model you run as>'. Blocking means: correcting the text would change a named decision or required behaviour the plan rests on, a required deliverable is absent, or following the plan loses data or breaks a safety boundary. Wording and style are not blocking.

## T1 card excerpt

## Coverage (Step 1B.0: Pass 1 found no labeled IDs; Pass 2 inferred rows, every quote contiguous in source.md)

| Row | Verbatim quote (source.md) | Citation | Plan task | Result |
|-----|----------------------------|----------|-----------|--------|
| INF-001 | "add wonsol as a new packaged panel template" | source.md:3 | Task 2 | covered |
| INF-002 | "make it the product default for ALL runs" | source.md:3 | Task 4 | covered |
| INF-003 | "the product default must not be hard coded" | source.md:3 | Task 4 (pointer file + default_template_name) | covered |
| INF-004 | "precedence must keep working" | source.md:3 | Task 4 acceptance | covered |
| INF-005 | "confirm the product default can support a 3 reviewer panel" | source.md:3 | Task 2, Task 4, Task 5 acceptance | covered |
| INF-006 | "wonsol needs three single-model tier aliases" | source.md:5 | Task 1 | covered |
| INF-007 | "exactly one slot must be fixed" | source.md:5 | Task 2 | covered |
| INF-008 | "so new tiers must get stand-ins" | source.md:5 | Task 1 | covered |
| INF-009 | "the template id must not start with reflect-" | source.md:5 | Constraints, Task 2 | covered |
| INF-010 | "keep it as a packaged template, for example classic" | source.md:5 | Task 3 | covered |
| INF-011 | "decide whether recorded template_id default" | source.md:5 | Task 5 (goldens), Task 3 (id `classic`) | partial: telemetry and manifest fixtures other than the two golden JSONs are not enumerated |
| INF-012 | "every consumer of the default" | source.md:5 | Tasks 4, 5, 6 | covered |
| INF-013 | "a regression test that the default resolves to a template by reference" | source.md:5 | Task 5 | covered |
| INF-014 | "the change must be made on a new branch from origin/master" | source.md:6 | Constraints (process; not a task) | covered |

parsed_count 0, inferred_count 14, coverage_pct (parsed) null, coverage_pct_union 13.5/14 = 0.96, coverage_degraded: parsed-sparse (Step 1B.2b: inferred_count > parsed_count; forbids the Tier 1 stop).

## Grounded observations (cited, Read in this run)

- The hard-coded fallback is `_default("review-panel.default.json")` in `load_panel` (`src/superclaude/cli/review/panel.py:459`); `find_path` (`panel.py:397`) holds the lookup precedence. Task 4 names both.
- `resolve_slot` (`panel.py:536-547`): `fixed` takes `candidates[0]`; `random` picks among all available candidates. Task 1 relies on this and was verified by draft resolve runs for both environments.
- `validate_panel` (`panel.py:160-256`) requires exactly one `fixed` slot and 1..8 reviewers: the 3-reviewer default is legal.
- `tests/review/test_review_panel_live7.py:42` asserts `default["template_id"] == "default"` and 4 reviewers; `tests/review/test_review_panel.py:360` asserts `"default"`; `:401` asserts the file `review-panel.default.json` exists. Task 5 and Task 3 change these.
- The one real consumer of the default is `src/superclaude/rules/prompts/document_review_loop_prompts.md:70`.

## Risks seen by Tier 1 (for the reviewers)

- R-A: Task 3 deletes `review-panel.default.json`; `test_review_panel_exclusion.py` and the golden `panel-golden-default-live7.json` may resolve the default by template id `default` (UNVERIFIED which).
- R-B: Task 1 changes `review-tiers.default.json`; `test_review_panel_reflect_profile.py` notes `tiers_sha256` depends on `classes` (UNVERIFIED how the frozen tier copy interacts).
- R-C: the plan ships a default the owner chose against the pre-registered result; the plan states that in Constraints and Task 6.
- R-D: an existing user's `~/.superclaude/review-panel.json` or `SUPERCLAUDE_REVIEW_PANEL` silently keeps the old behaviour (intended precedence), not mentioned for users in docs.

Calibrated confidence: see `artifacts/t1-calibration.md`.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-17T13:04:46Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel

### src/superclaude/cli/review/panel.py:397-468

```python
def find_path(
    kind: str, explicit: str | None = None, environ: Mapping[str, str] | None = None
) -> Path | None:
    """First existing file of the lookup precedence, or None for the packaged default.

    kind is 'panel' or 'tiers'. Precedence: explicit path; the environment variable
    (SUPERCLAUDE_REVIEW_PANEL / SUPERCLAUDE_REVIEW_TIERS); <project>/.superclaude/review-<kind>.json;
    ~/.superclaude/review-<kind>.json.
    """
    env = os.environ if environ is None else environ
    if explicit:
        return Path(explicit)
    var = env.get(
        "SUPERCLAUDE_REVIEW_PANEL" if kind == "panel" else "SUPERCLAUDE_REVIEW_TIERS"
    )
    if var:
        return Path(var)
    fname = "review-panel.json" if kind == "panel" else "review-tiers.json"
    for base in (_project_root() / ".superclaude", Path.home() / ".superclaude"):
        candidate = base / fname
        if candidate.is_file():
            return candidate
    return None


def _default(name: str) -> dict:
    ref = resources.files("superclaude.cli.review") / "data" / name
    return json.loads(ref.read_text(encoding="utf-8"))


_PACKAGED_NAME = re.compile(r"^[a-z0-9][a-z0-9-]{0,31}$")


def packaged_panel(name: str) -> dict:
    """A panel template shipped in the package: review-panel.<name>.json (use '@<name>' on the CLI)."""
    if not _PACKAGED_NAME.match(name):
        raise ValueError(f"invalid packaged panel name {name!r}")
    try:
        return _default(f"review-panel.{name}.json")
    except (FileNotFoundError, OSError) as exc:
        known = sorted(
            p.name[len("review-panel.") : -len(".json")]
            for p in (resources.files("superclaude.cli.review") / "data").iterdir()
            if p.name.startswith("review-panel.") and p.name.endswith(".json")
        )
        raise ValueError(
            f"no packaged panel template '{name}' (known: {', '.join(known)})"
        ) from exc


def load_panel(path: str | None = None) -> dict:
    ref = path or os.environ.get("SUPERCLAUDE_REVIEW_PANEL") or ""
    if ref.startswith("@"):
        obj = packaged_panel(ref[1:])
        errors = validate_panel(obj)
        if errors:
            raise ValueError(f"invalid packaged panel {ref}: " + "; ".join(errors))
        return obj
    found = find_path("panel", path)
    obj = (
        json.loads(found.read_text(encoding="utf-8"))
        if found
        else _default("review-panel.default.json")
    )
    errors = validate_panel(obj)
    if errors:
        raise ValueError(
            f"invalid panel template{f' {found}' if found else ''}: "
            + "; ".join(errors)
        )
    return obj

```

### src/superclaude/cli/review/panel.py:536-556

```python
    if strategy == "fixed":
        model = candidates[0]
    elif strategy in ("random", "round_robin"):
        pool = [m for m in candidates if m not in set(exclude)]
        if not pool:
            if hard:
                raise ExclusionExhausted(",".join(models))
            pool = candidates
        if strategy == "random":
            model = random.Random(seed).choice(pool)
        else:
            model = pool[int(seed) % len(pool)]
    else:
        raise ValueError(f"unknown strategy {strategy!r}")
    k = candidates.index(model)
    return {
        "model": model,
        "fallback_depth": source.index(model),
        "stand_in": stand,
        "fallbacks": candidates[k + 1 :] + candidates[:k],
    }
```

### tests/review/test_review_panel_live7.py:42-45

```python
def test_default_panel_is_unchanged_by_live7(tiers):
    default = pnl.load_panel()
    assert default["template_id"] == "default"
    assert sum(s["count"] for s in default["slots"]) == 4
```

### tests/review/test_review_panel.py:344-372

```python
def test_template_lookup_precedence(tmp_path, monkeypatch):
    home = tmp_path / "home"
    proj = tmp_path / "proj"
    for d in (home / ".superclaude", proj / ".superclaude"):
        d.mkdir(parents=True)
    base = pnl.load_panel()

    def write(path, tid):
        obj = copy.deepcopy(base)
        obj["template_id"] = tid
        path.write_text(json.dumps(obj))
        return path

    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("SUPERCLAUDE_REVIEW_PANEL", raising=False)
    monkeypatch.chdir(proj)
    assert pnl.load_panel()["template_id"] == "default"
    write(home / ".superclaude" / "review-panel.json", "from-user")
    assert pnl.load_panel()["template_id"] == "from-user"
    write(proj / ".superclaude" / "review-panel.json", "from-project")
    assert pnl.load_panel()["template_id"] == "from-project"
    env_file = write(tmp_path / "env.json", "from-env")
    monkeypatch.setenv("SUPERCLAUDE_REVIEW_PANEL", str(env_file))
    assert pnl.load_panel()["template_id"] == "from-env"
    explicit = write(tmp_path / "explicit.json", "from-flag")
    assert pnl.load_panel(str(explicit))["template_id"] == "from-flag"


def test_tier_file_lookup_precedence(tmp_path, monkeypatch):
```

### src/superclaude/cli/review/data/review-panel.default.json:1-20

```json
{
  "schema": "review-panel/1",
  "template_id": "default",
  "version": "1.0.0",
  "description": "Production review panel: 2x Tier 3 + 1x Tier 2 + 1x Tier 1b parallel independent reviewers; Tier 1b is the fixed anchor.",
  "distinct_across_slots": true,
  "apply_to": ["first"],
  "slots": [
    {"slot_id": "t1b", "tier": "tier1b", "count": 1, "strategy": "fixed"},
    {"slot_id": "t2", "tier": "tier2", "count": 1, "strategy": "random"},
    {"slot_id": "t3", "tier": "tier3", "count": 2, "strategy": "random"}
  ]
}
```

### .dev/tasks/to-do/TASK-WF-makeTheWonsolRev-20261117-130446/TASK-WF-makeTheWonsolRev-20261117-130446.md:1-100

```markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-makeTheWonsolRev-20261117-130446
version: "1"
priority: Medium
created_date: "2026-11-17"
---

# Make the wonsol reviewer panel the product default, selected by template reference

Source: ./source.md
Goal: `superclaude review panel resolve` with no template argument resolves the new 3-reviewer `wonsol` panel (wonder anchor, sol, ember) by reading a pointer to a packaged template, not by a hard-coded file name; the old 4-reviewer default stays available as a packaged template; every existing lookup precedence (explicit path, `SUPERCLAUDE_REVIEW_PANEL`, project and user `review-panel.json`) still works and a 3-reviewer default is shown to resolve in both environments.

## Constraints

- Work on a new branch cut from `origin/master`, never on the evaluation branch that holds the answer key; open the PR only with `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`; never stage anything under `.claude/`.
- Edit only under `src/superclaude/cli/review/`, `src/superclaude/skills/`, `src/superclaude/rules/`, `tests/` and `docs/`; run `make sync-dev` after skill or rule edits.
- The product panel chooses models only. The seat lenses, table caps and briefs of the evaluation harness (S = wonder with lenses C5 C6 C8 C2 and cap 8; L1 = sol; L2 = ember) are not part of this change, so only the model mix transfers. The confirming test did not meet its registered bar (found fraction +0.099 and +0.109, lower bounds -0.004 and -0.006; 1.56 times the control's panel time); the owner has ordered the default change as provisional, and the plan must say so in the docs it touches.
- `validate_panel` in `src/superclaude/cli/review/panel.py` already allows 1 to 8 reviewers and requires exactly one `fixed` slot; do not change those rules. A template id must not start with `reflect-` (that prefix turns on the reflect profile).
- Keep the strategy and tier-name rules: tier names match `^tier[0-9]{1,2}[a-z]?$`.

## Phase 1: Tier data for the three wonsol seats

## Task 1: Add three seat tiers and the ember model to the packaged tier file

Edit `src/superclaude/cli/review/data/review-tiers.default.json`. Add three aliases: `tier5a` (gateway alias `claude-gw-tier5a[1m]`, models `muse-wonder-1.0` then `claude-sonnet-5-5`), `tier5b` (`claude-gw-tier5b[1m]`, models `["gpt-6.1-sol"]` only) and `tier5c` (`claude-gw-tier5c[1m]`, models `["muse-ember-1.0"]` only). The list shapes matter and were checked against `resolve_slot` in `src/superclaude/cli/review/panel.py`: a `fixed` slot takes the first available model of its list (so `tier5a` falls back from wonder to Sonnet), but a `random` slot picks at random among every available model of its list, so `tier5b` and `tier5c` must hold exactly one model each to make the seats deterministic (a two-model list returned the fallback model in a draft run). In the `anthropic-only` environment add `stand_ins` entries `tier5b` and `tier5c`, each `["claude-haiku-5-5"]` (that environment lists only Anthropic models, and a tier with none available raises `NoModelAvailable` without a stand-in). Add `muse-ember-1.0` to `names` ("Muse Ember 1.0") and to `classes` (class `muse`, as the other Muse models). Bump the tier file `version` by one minor step.

Acceptance criteria:
- `validate_tiers` returns no errors for the edited file, and `pnl.load_tiers()["aliases"]` has `tier5a`, `tier5b` and `tier5c` with the models above.
- Resolving a draft template with the three slots of Task 2 for run ids `t1`, `t2` and `t3`: in `anthropic-only` it prints `claude-sonnet-5-5`, then two `claude-haiku-5-5` marked `stand_in` true, every time; in `gateway` it prints `muse-wonder-1.0`, `gpt-6.1-sol`, `muse-ember-1.0` every time.
- No existing alias (`tier1a` to `tier4`) changes its models, so `live7` and the old default resolve to the same models as before.

## Phase 2: The wonsol template and the preserved 4-reviewer default

## Task 2: Add the wonsol panel template

Depends on: Task 1

Create `src/superclaude/cli/review/data/review-panel.wonsol.json` with `schema` `review-panel/1`, `template_id` `wonsol`, `version` `1.0.0`, a description that states the three models and that the choice is provisional, `distinct_across_slots` true, `apply_to` `["first"]` as in the existing default, and three slots: `t5a` (tier `tier5a`, count 1, strategy `fixed`, the anchor), `t5b` (tier `tier5b`, count 1, strategy `random`), `t5c` (tier `tier5c`, count 1, strategy `random`). It is loaded with `@wonsol` through `packaged_panel` in `src/superclaude/cli/review/panel.py`.

Acceptance criteria:
- `pnl.load_panel("@wonsol")` returns the template and `pnl.validate_panel(it, pnl.load_tiers()) == []`; the slot counts sum to 3 and exactly one slot is `fixed`.
- `uv run superclaude review panel resolve --template @wonsol --run-id t1 --env anthropic-only` and `--env gateway` both exit 0 and list three reviewers with ids `t5a-1`, `t5b-1`, `t5c-1`; in `anthropic-only` the anchor is `claude-sonnet-5-5` and the other two are Haiku stand-ins (so that environment does not run wonder, sol or ember).
- `--kind re-review` resolves only the anchor `t5a-1`, the same rule that `live7` follows in `tests/review/test_review_panel_live7.py` (`test_re_review_resolves_only_the_anchor`).

## Task 3: Keep the current 4-reviewer default as the packaged template `classic`

Create `src/superclaude/cli/review/data/review-panel.classic.json` with the exact slots, `distinct_across_slots` and `apply_to` of the current `src/superclaude/cli/review/data/review-panel.default.json`, `template_id` `classic`, and a description saying it is the previous production default. Then delete `src/superclaude/cli/review/data/review-panel.default.json` (the default is selected by the pointer of Task 4, so no template keeps the id `default`).

Acceptance criteria:
- `pnl.load_panel("@classic")` has four reviewers (`t1b` 1, `t2` 1, `t3` 2) and resolves in `anthropic-only` to `claude-sonnet-5-5` plus three `claude-haiku-5-5`, exactly as the old default did.
- `grep -rn "review-panel.default" src tests docs scripts` finds no remaining reference except the ones Task 5 and Task 6 rewrite.

## Phase 3: The default selected by reference

## Task 4: Select the default through a pointer file instead of a hard-coded file name

Depends on: Task 2, Task 3

Add `src/superclaude/cli/review/data/review-default.json` with content `{"schema": "review-default/1", "template": "wonsol"}`. In `load_panel` of `src/superclaude/cli/review/panel.py` (the `else _default("review-panel.default.json")` branch, line 459 at planning time) replace the hard-coded file name with a new function `default_template_name()` that reads the pointer file through `_default`, checks `schema` and that `template` matches `_PACKAGED_NAME`, and then returns `packaged_panel(name)` validated by `validate_panel` as the `@name` branch does. A pointer with a bad schema, a bad name or a name with no packaged template raises `ValueError` that names the pointer file. The lookup order of `find_path` stays untouched: explicit path, `SUPERCLAUDE_REVIEW_PANEL`, `.superclaude/review-panel.json` of the project, then of the home directory, then the packaged default. Callers that must keep working: `resolve_cmd` in `src/superclaude/cli/review/panel_cmd.py`, `scripts/reflect_shadow_exit.py` (it uses `load_tiers`, so it needs no code change but its tests must pass), and the `load_panel` callers in `tests/review/test_review_panel.py`, `tests/review/test_review_panel_live7.py` and `tests/review/test_review_reflect_templates.py`.

Acceptance criteria:
- With no flag, no environment variable and no `.superclaude/review-panel.json`, `pnl.load_panel()["template_id"] == "wonsol"` and the file `src/superclaude/cli/review/data/review-default.json` is the only place that names it; changing its `template` to `classic` makes `pnl.load_panel()["template_id"] == "classic"` with no code change.
- A pointer naming an unknown template, a malformed name or a wrong schema raises `ValueError` mentioning `review-default.json`.
- `find_path` precedence is unchanged: a project `review-panel.json`, a home one, `SUPERCLAUDE_REVIEW_PANEL` and an explicit path still override the pointer (`test_template_lookup_precedence` keeps its order of assertions).
- `uv run superclaude review panel resolve --run-id t1 --env anthropic-only` prints three reviewers (Sonnet plus two Haiku stand-ins); with `--env gateway` it prints the three wonsol models.

## Phase 4: Tests, goldens and documentation

## Task 5: Update the tests and golden files that pin the old default and add the regression tests

Depends on: Task 4

Edit these existing tests: `tests/review/test_review_panel.py` (the `assert pnl.load_panel()["template_id"] == "default"` line of `test_template_lookup_precedence` becomes `"wonsol"`; `test_packaged_defaults_are_read_through_importlib_resources` checks the pointer file and the tier file instead of `review-panel.default.json`), `tests/review/test_review_panel_live7.py` (`test_default_panel_is_unchanged_by_live7` becomes a test that the default is `wonsol` with 3 reviewers and that `@classic` still has 4 reviewers and `live7` still has 7), and re-pin `tests/review/fixtures/panel-golden-default-live7.json` and `tests/review/fixtures/panel-golden-packaged-tiers.json` only where the tier file bump of Task 1 changes `tiers_sha256`, keeping the frozen-tier copy `tests/review/fixtures/review-tiers.frozen-1.0.0.json` byte-identical so `tests/review/test_review_panel_exclusion.py` still proves that the old resolutions did not move. Add `tests/review/test_review_default_template.py` with these tests: the default resolves to a template by reference (`default_template_name()` returns the pointer's value); a three-reviewer default resolves in `anthropic-only` and in `gateway`; a pointer edited in a temporary copy of the data folder switches the default to `classic` with no code change; a bad pointer is rejected. Check that `tests/review/test_review_panel_reflect_profile.py`, `tests/review/test_review_reflect_templates.py` and `tests/cli/reflect/test_shadow_skill_contract.py` still pass (they read `load_tiers` and `classes`; the new `classes` entry for ember must not break the reflect profile rules).

Acceptance criteria:
- `uv run pytest tests/review tests/cli/reflect tests/unit/test_ccsession_tiers.py -q` passes with no test skipped for this change; `tests/unit/test_ccsession_tiers.py` is run only to show it is not affected (it matched a search for `muse-ember-1.0`; if it reads `review-tiers.default.json`, update it in this task).
- The new test file fails if `load_panel` goes back to a hard-coded file name (the pointer-switch test is the check) and if the default is changed to a template with 4 reviewers while the 3-reviewer assertion remains.
- `git diff --stat` shows no change to `tests/review/fixtures/review-tiers.frozen-1.0.0.json`.

## Task 6: Update the documentation and rule text that describe the default panel

Depends on: Task 5

Edit `docs/reference/review-panel-live7.md` so it no longer says the default is the 4-reviewer panel and describes the pointer file, the `@wonsol` and `@classic` templates, the new tiers, the `anthropic-only` resolution and the provisional status with the confirming-test numbers of the Constraints section. Read `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, `src/superclaude/rules/prompts/document_review_loop_prompts.md` and `tests/review/test_review_rules_text.py` for statements about the default panel size or composition (the Task 4 grep found `review panel resolve` and `review-panel.json` text there) and change only the statements that are now false; keep `tests/review/test_review_rules_text.py` passing. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- `grep -rn "2x Tier 3\|Tier 1b is the fixed anchor\|four reviewers\|4 reviewers" src docs tests` finds no sentence that calls the 4-reviewer panel the product default.
- `uv run pytest tests/review/test_review_rules_text.py -q` passes and `make verify-sync` exits 0; no file under `.claude/` is staged.
- The sentence in `src/superclaude/rules/prompts/document_review_loop_prompts.md` that tells the review loop to run the reviewers `superclaude review panel resolve` prints (the one real consumer of the default panel found by search) stays true, and the docs of Task 6 state that the re-review reviewer is the anchor, which changes from the Tier 1b model (Sonnet) to `muse-wonder-1.0` in the `gateway` environment and stays `claude-sonnet-5-5` in `anthropic-only`.
- The PR description names the confirming-test result (not confirmed by the registered rule) and that the model mix, not the evaluation seat lenses, is what ships.
```

## Coverage slice

All 14 rows of the T1 card coverage table (see T1 card excerpt). Persona focus: structure, tech debt and data-file design (Tasks 1, 3, 4)
