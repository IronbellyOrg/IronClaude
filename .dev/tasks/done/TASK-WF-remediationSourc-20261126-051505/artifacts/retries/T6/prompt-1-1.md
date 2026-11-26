2aab5a6c5929cd103f6e1043773364232a5bf8a5
Review one task for spec compliance.

Task brief: ## Task 6: Create tests/skills/test_implement_launch_alias.py

Depends on: Task 1, Task 2, Task 3

Create `tests/skills/test_implement_launch_alias.py`, following the style of `tests/skills/test_implement_adviser_family.py` (module docstring, a `Path(__file__).resolve().parents[2]` root, the text of the source `retry.md` read once at import). It holds these checks.

- Alias set: `AGENT_ALIASES = frozenset({"opus", "sonnet", "haiku", "fable"})`, hard-coded, with a comment warning not to reuse `ALIASES` from `tests/skills/test_model_alias_policy.py`, which includes `inherit` and lacks `fable`. A doc pin reads the one line of `docs/reference/model-aliases.md` that contains "takes the aliases", collects its backticked words, drops `model` and `inherit`, and asserts equality with `AGENT_ALIASES`.
- Paragraph: the section between `### Model ladder` and `### Cost and caps` contains a line starting `**Launch alias.**`; that paragraph does not contain a line starting `GPT spawn path: `; it contains the phrases "takes only `opus`, `sonnet`, `haiku` or `fable`" and "never a full model id", the exact phrase "is `opus` for every adviser" (M-1), the backticked `family-fallback: <reason>` and the `launch: <alias>` header form. Also assert that the two stale phrases quoted in Task 3 are absent from the section and that the section still contains `T2bModel01`, `T2Model02`, `T1Model02` and `T1Model01`. These pins make a prose rewrite that drops the rule, or that names a GPT model as a startable spawn, fail.
- Launch rule and reworded lines (M-1): in the Launch alias paragraph, `sonnet`, `haiku` and `fable` each occur only inside the sentence "takes only `opus`, `sonnet`, `haiku` or `fable`" (the test counts each word in the paragraph and in that sentence and compares). The test takes the region from the `**Escalation rule.**` line of `retry.md` to the lead-in "Worked example with the fallback ladder:" and asserts each of those two anchors occurs exactly once. That region contains, as a literal embedded in the test, the Task 3 sentence "Every adviser on the primary ladder is launched on `opus`, and a pick whose id does not start with `claude-` carries `family-fallback`." (the test does not read `./artifacts/t3-wording.md`). Neither the Launch alias paragraph nor that region contains a model-id literal (`gpt-` or `glm-` followed by a digit, or `claude-` plus a name plus a digit). The `**Resolving adviser B.**` line (line 181 of the pre-change `retry.md`) does not contain "strongest reachable model" and does contain `opus` and "the header form given under Launch alias below".
- Mutation checks (M-1): the test copies the changed `retry.md` text in memory, applies one change per copy, and runs every pin against each copy. The changes are: `opus` to `sonnet` inside "is `opus` for every adviser"; the same change inside the Task 3 sentence; an added "except adviser B" clause inside the Task 3 sentence; an added sentence in the region that spawns adviser B on `gpt-6.1-sol`; and "strongest reachable model" restored on line 181. The test lists, for each change, the pin it is meant to fail, and each copy must fail exactly that pin (the first change also moves the `sonnet` count pin, so the test lists both for it); the failure message names the pin.
- Worked table: parse the four rows after "Worked example with the fallback ladder:"; every cell of the adviser A, adviser B and escalation 2 columns is either an alias word in backticks (with its count and any short parenthetical) or names a non-launchable pick together with `family-fallback`; no cell contains a string that starts with `gpt-`, `glm-` or `claude-`.
- Resolver: a pure function `plan(executor_tier, env)` that returns, for the five roles (escalation 1 adviser A, escalation 1 adviser B, the critique adviser, escalation 2 first adviser, escalation 2 second adviser), a record with the picked id, a `source` field (the variable name or alias the pick came from; M-2), the launch value and a `family_fallback` flag, following the selection rules in the Model ladder section: the active ladder is the primary ladder only when `T2bModel01`, `T2Model02`, `T1Model02` and `T1Model01` are all set and non-empty, otherwise the fallback ladder (`haiku`, `sonnet`, `opus`); the family of an id is read from its `claude-` or `gpt-` prefix after stripping a trailing bracketed suffix; adviser A is one rung up in the executor's family (the top rung when the executor is on top or the tier is unknown); adviser B is the other family (the first of `T1Model01`, `T1Model02` whose id starts with `gpt-` for a Claude executor, the Claude top rung for a GPT executor); the critique adviser uses adviser A's pick; both escalation-2 advisers use the top rung; `T2Model01` is never picked. The launch value comes only from the documented rule: the rung's own alias on the fallback ladder, `opus` for every pick on the primary ladder, and a pick that is not a `claude-` id (or has no reachable id) is launched on `opus` with `family_fallback` true.
- Environments, as plain dicts that never read `os.environ`: the observed values (`T2bModel01` `gpt-6.1-terra`, `T2Model02` `glm-5.3`, `T1Model02` `gpt-6.1-sol`, `T1Model01` `claude-opus-5-5`, `T2Model01` `gpt-6.1-sol`); a swapped environment (`T1Model01` a `gpt-` id and `T1Model02` a `claude-` id); an all-claude environment; the observed values with a trailing `[1m]` on every id; a partial environment with `T1Model01` set to the empty string (forces the fallback ladder); and a fallback environment whose `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL` hold tier-style ids.
- Sweep: for every environment, every executor tier of the active ladder plus `unknown`, and the five roles, assert that the launch value is in `AGENT_ALIASES` and contains no `[`, that a non-`claude-` primary-ladder pick has `family_fallback` true and launch `opus`, that the fallback ladder passes the rung's own alias, and that no record's `source` is `T2Model01` (M-2; the check never compares ids, because `T2Model01` and `T1Model02` both hold `gpt-6.1-sol` in the observed environment). Header check: the test builds line 1 for each role as `model: <id> family: <family> rung: <rung> launch: <alias>` and asserts that it never states a served family.
- Negative controls: run the same checks against a resolver that returns the raw picked id as the launch value, and against a resolver that never sets `family_fallback`, and against a resolver that picks `T2Model01` as "one rung up" for a `T2Model02` executor (M-2; the source check must flag it); each must be flagged (the test asserts that the checks report at least one violation for each).

Evidence for the red-then-green requirement: write to `./artifacts/t6-red-check.txt` the result of running the paragraph pin against the pre-change file read with `git show HEAD:src/superclaude/skills/sc-implement-protocol/refs/retry.md` (it must fail there) and the result of the full test file on the changed tree (it must pass).

Acceptance criteria:
- `uv run pytest tests/skills/test_implement_launch_alias.py -q` passes on the changed tree, and the paragraph-presence check fails when applied to the `retry.md` that `git show HEAD:...` prints (recorded in `./artifacts/t6-red-check.txt`).
- Every M-1 pin passes on the changed `retry.md` and fails on the `retry.md` that `git show HEAD:...` prints; every M-1 mutation fails its listed pin and the failure names it.
- Each of the three negative controls (M-2) is flagged, and the sweep covers every environment, every executor tier and all five roles.
- The test file does not read `os.environ`, does not import `ALIASES` from `tests/skills/test_model_alias_policy.py`, and passes `uv run ruff check tests/skills/test_implement_launch_alias.py` and `uv run ruff format --check tests/skills/test_implement_launch_alias.py`.
- `uv run mypy tests/skills/test_implement_launch_alias.py` reports no new diagnostics (M-3); the resolver record is typed (a TypedDict or dataclass) and any regex match is checked not None before use.
- `uv run pytest tests/skills/test_implement_adviser_family.py tests/skills/test_model_alias_policy.py tests/skills/test_implement_severity_static.py tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py tests/skills/test_implement_retry_citation.py tests/skills/test_implement_retry_revert.py tests/skills/test_worker_contract.py tests/commands/test_workflow_command.py tests/hooks/test_launch_level_guard.py tests/unit/test_cli_install.py -q` passes.
AC ids in source order (the bullets under Acceptance criteria): T6.AC1 T6.AC2 T6.AC3 T6.AC4 T6.AC5 T6.AC6
Global constraints: ## Constraints

- Scope: change only the files named in the tasks below (`src/superclaude/skills/sc-implement-protocol/refs/retry.md`, `src/superclaude/skills/sc-implement-protocol/SKILL.md`, their two copies under `plugins/superclaude/skills/sc-implement-protocol/`, `tests/skills/test_task_workspace_lifecycle.py` and the new `tests/skills/test_implement_launch_alias.py`). Edit nothing under `.claude/` or `.dev/issues/`.
- The rule being written: on the fallback ladder the Agent call's `model` is the rung's own alias; on the primary ladder it is `opus` for every adviser (adviser A, adviser B, the critique adviser and both escalation-2 advisers); an adviser whose picked id does not start with `claude-` is still launched on `opus` and its line 1 carries `family-fallback: <reason>`; this never STOPs and never prompts the user.
- The new text in `retry.md` must not start any line with `GPT spawn path: ` (a test requires exactly one such line, at the pinned line 183), and must keep the backticked phrase `family-fallback: <reason>` and the phrase "never STOPs and never prompts the user" (`tests/skills/test_implement_adviser_family.py`, lines 73 to 85).
- The new text must not contain the words `halt`, `Ruling` or `E-HALT-QA` outside the lines a test already allow-lists (`tests/skills/test_implement_severity_static.py`, lines 296 to 299 and 420 to 434), must not contain the string `claude-gw-tier` (`tests/skills/test_model_alias_policy.py`, lines 104 to 119), and must not put a full model id after `--model` or `--models` (same file, lines 164 to 173).
- The new text must not add a fenced block containing a line that begins with `T` and a digit and has no angle bracket (`tests/skills/test_implement_severity_static.py`, lines 225 to 250), and must not add a table row whose first cell is a backticked lowercase key and whose last cell is only the digits 2 to 5 (`tests/skills/test_workflow_archive.py`, lines 1042 to 1076).
- `retry.md` must keep the four rung names `T2bModel01`, `T2Model02`, `T1Model02` and `T1Model01`, and must not contain any `T`-digit-underscore-`Model` spelling (`tests/skills/test_model_alias_policy.py`, lines 219 to 228).
- Add no flag, no stop reason, no halt reason and no extra adviser spawn (the cap of six stays); do not change the `tier=` ledger token (its value class is letters, digits and underscore) or `src/superclaude/skills/sc-implement-protocol/refs/ledger.md`.
- In table cells and prose copied from the existing worked table, use the multiplication sign `×` and not the letter `x` (the pinned test rows use `1×`).
- Out of scope, separate defects: the executor-tier tie when `T2Model01` and `T1Model02` hold the same id, and family inference from gateway ids such as `claude-gw-tier2`.
- Decided for this work (iteration 3): nothing to decide; build what the issue asks for, within its own scope.
- Observed workspace values the wording must stay true to: `T2bModel01` is `gpt-6.1-terra`, `T2Model02` is `glm-5.3`, `T1Model02` is `gpt-6.1-sol`, `T1Model01` is `claude-opus-5-5`; the three aliases `opus`, `sonnet` and `haiku` resolve to tier ids through `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL`.
Start sha: 2aab5a6c5929cd103f6e1043773364232a5bf8a5
Diff against the start snapshot: new file tests/skills/test_implement_launch_alias.py (full contents):
+++ b/tests/skills/test_implement_launch_alias.py
@@ -0,0 +1,469 @@
+"""Launch alias of the retry-ladder advisers of sc-implement-protocol (issue 393).
+
+Enforcement type: STATIC. The Agent call's `model` takes only an alias, never a model id,
+so every adviser launch value must be an alias. This file pins the prose of
+`refs/retry.md` that states that rule (`PINS`, each also run against five in-memory
+mutations of the text) and checks a pure reference resolver, `plan`, over hermetic
+environments given as plain dicts (the file never reads the process environment).
+
+Known limit: the resolver reads the ladder prose as a reference model, not the prose
+itself, so a wrong sentence outside the pins is caught only by a reviewer. A controlled
+launch per alias stays a follow-up.
+"""
+
+from __future__ import annotations
+
+import re
+from collections.abc import Callable, Mapping
+from pathlib import Path
+from typing import TypedDict
+
+import pytest
+
+_ROOT = Path(__file__).resolve().parents[2]
+_RETRY = (
+    _ROOT / "src/superclaude/skills/sc-implement-protocol/refs/retry.md"
+).read_text(encoding="utf-8")
+_ALIAS_DOC = (_ROOT / "docs/reference/model-aliases.md").read_text(encoding="utf-8")
+
+# Hard-coded on purpose: do not reuse `ALIASES` of test_model_alias_policy.py, which
+# includes `inherit` (not allowed on the Agent call) and lacks `fable`.
+AGENT_ALIASES = frozenset({"opus", "sonnet", "haiku", "fable"})
+
+TAKES_ONLY = "takes only `opus`, `sonnet`, `haiku` or `fable`"
+RULE_PHRASE = "is `opus` for every adviser"
+HEADER_FORM = "model: <id> family: <claude|gpt> rung: <T1|top> launch: <alias>"
+T3_SENTENCE = (
+    "Every adviser on the primary ladder is launched on `opus`, and a pick whose id "
+    "does not start with `claude-` carries `family-fallback`."
+)
+ANCHOR_START = "**Escalation rule.**"
+ANCHOR_END = "Worked example with the fallback ladder:"
+STALE = (
+    "an executor on `T2Model02` or `T2Model01` gets adviser A on `T1Model02`",
+    "adviser A is the GPT T1 model (`T1Model01` when the executor is not already on it",
+)
+RUNG_NAMES = ("T2bModel01", "T2Model02", "T1Model02", "T1Model01")
+MODEL_ID = re.compile(r"\b(?:gpt|glm)-\d|claude-[a-z]+-\d")
+
+
+def _between(text: str, start: str, end: str, include_end: bool = False) -> str:
+    i = text.find(start)
+    if i < 0:
+        return ""
+    j = text.find(end, i + len(start))
+    if j < 0:
+        return ""
+    return text[i : j + len(end)] if include_end else text[i:j]
+
+
+def _launch(text: str) -> str:
+    return _between(text, "**Launch alias.**", "### Cost and caps")
+
+
+def _region(text: str) -> str:
+    return _between(text, ANCHOR_START, ANCHOR_END, include_end=True)
+
+
+def _section(text: str) -> str:
+    return _between(text, "### Model ladder", "### Cost and caps")
+
+
+def _table_ok(text: str) -> bool:
+    i = text.find(ANCHOR_END)
+    if i < 0:
+        return False
+    rows: list[str] = []
+    for ln in text[i + len(ANCHOR_END) :].splitlines():
+        if ln.startswith("|"):
+            rows.append(ln)
+        elif rows:
+            break
+    body = rows[2:]  # drop the header and the separator
+    if len(body) != 4:
+        return False
+    for row in body:
+        cells = [c.strip() for c in row.strip().strip("|").split("|")]
+        for cell in cells[1:4]:
+            m = re.match(r"^\d+× `(\w+)`(?: \(([^)]*)\))?$", cell)
+            if m is None or m.group(1) not in AGENT_ALIASES:
+                return False
+            if "launchable" in (m.group(2) or "") and "family-fallback" not in cell:
+                return False
+            if re.search(r"\b(?:gpt|glm|claude)-", cell):
+                return False
+    return True
+
+
+def _line_resolving_b(text: str) -> str:
+    return next(
+        (ln for ln in text.splitlines() if ln.startswith("**Resolving adviser B.**")),
+        "",
+    )
+
+
+def _count(word: str, text: str) -> int:
+    return len(re.findall(rf"\b{word}\b", text))
+
+
+def _alias_count_ok(p: str) -> bool:
+    inside = p.count(TAKES_ONLY)
+    return bool(p) and all(
+        _count(w, p) == _count(w, TAKES_ONLY) * inside
+        for w in ("sonnet", "haiku", "fable")
+    )
+
+
+PINS: dict[str, Callable[[str], bool]] = {
+    "launch-rule": lambda t: RULE_PHRASE in _launch(t),
+    "takes-only": lambda t: TAKES_ONLY in _launch(t),
+    "never-full-id": lambda t: "never a full model id" in _launch(t),
+    "family-fallback-token": lambda t: "`family-fallback: <reason>`" in _launch(t),
+    "launch-header": lambda t: HEADER_FORM in _launch(t),
+    "no-spawn-line": lambda t: (
+        bool(_launch(t))
+        and not any(ln.startswith("GPT spawn path: ") for ln in _launch(t).splitlines())
+    ),
+    "alias-count": lambda t: _alias_count_ok(_launch(t)),
+    "anchors-once": lambda t: t.count(ANCHOR_START) == 1 and t.count(ANCHOR_END) == 1,
+    "region-sentence": lambda t: _region(t).count(T3_SENTENCE) == 1,
+    "no-model-ids": lambda t: (
+        bool(_launch(t))
+        and bool(_region(t))
+        and not MODEL_ID.search(_launch(t))
+        and not MODEL_ID.search(_region(t))
+    ),
+    "line-181": lambda t: (
+        bool(_line_resolving_b(t))
+        and "strongest reachable model" not in _line_resolving_b(t)
+        and "`opus`" in _line_resolving_b(t)
+        and "the header form given under Launch alias below" in _line_resolving_b(t)
+    ),
+    "stale-absent": lambda t: (
+        bool(_section(t))
+        and not any(s in _section(t) for s in STALE)
+        and all(n in _section(t) for n in RUNG_NAMES)
+    ),
+    "table": _table_ok,
+}
+
+
+def failed_pins(text: str) -> list[str]:
+    return [name for name, check in PINS.items() if not check(text)]
+
+
+def _mutate(text: str, old: str, new: str) -> str:
+    assert text.count(old) == 1, f"mutation anchor not unique: {old!r}"
+    return text.replace(old, new)
+
+
+# (label, old, new, the pins the change must fail, and only those)
+MUTATIONS: list[tuple[str, str, str, frozenset[str]]] = [
+    (
+        "rule opus to sonnet",
+        RULE_PHRASE,
+        "is `sonnet` for every adviser",
+        frozenset({"launch-rule", "alias-count"}),
+    ),
+    (
+        "sentence opus to sonnet",
+        "is launched on `opus`, and a pick whose id",
+        "is launched on `sonnet`, and a pick whose id",
+        frozenset({"region-sentence"}),
+    ),
+    (
+        "except adviser B",
+        "Every adviser on the primary ladder is launched",
+        "Every adviser on the primary ladder, except adviser B, is launched",
+        frozenset({"region-sentence"}),
+    ),
+    (
+        "gpt spawn sentence",
+        " " + ANCHOR_END,
+        " Adviser B is spawned on `gpt-6.1-sol`. " + ANCHOR_END,
+        frozenset({"no-model-ids"}),
+    ),
+    (
+        "strongest reachable model",
+        "and writes it on line 1",
+        "and writes the strongest reachable model on line 1",
+        frozenset({"line-181"}),
+    ),
+]
+
+
+def test_alias_set_matches_doc() -> None:
+    lines = [ln for ln in _ALIAS_DOC.splitlines() if "takes the aliases" in ln]
+    assert len(lines) == 1
+    words = set(re.findall(r"`([^`]+)`", lines[0])) - {"model", "inherit"}
+    assert words == AGENT_ALIASES
+
+
+def test_every_pin_passes_on_the_changed_text() -> None:
+    assert failed_pins(_RETRY) == []
+
+
+@pytest.mark.parametrize("m", MUTATIONS, ids=[m[0] for m in MUTATIONS])
+def test_mutation_fails_exactly_its_pins(
+    m: tuple[str, str, str, frozenset[str]],
+) -> None:
+    label, old, new, expected = m
+    failed = set(failed_pins(_mutate(_RETRY, old, new)))
+    assert failed == expected, (
+        f"{label}: expected pins {sorted(expected)}, got {sorted(failed)}"
+    )
+
+
+# ---------------------------------------------------------------- resolver
+
+
+class Pick(TypedDict):
+    id: str
+    source: str  # the variable or alias the pick came from, or "unreachable"
+    rung: str  # "T1", "top" or "other"
+    launch: str
+    family_fallback: bool
+
+
+Env = Mapping[str, str]
+Planner = Callable[[str, Env], dict[str, Pick]]
+
+PRIMARY = RUNG_NAMES
+FALLBACK = ("haiku", "sonnet", "opus")
+T1_VARS = ("T1Model01", "T1Model02")
+ROLES = ("esc1_a", "esc1_b", "critique", "esc2_1", "esc2_2")
+_ALIAS_VAR = {
+    "haiku": "ANTHROPIC_DEFAULT_HAIKU_MODEL",
+    "sonnet": "ANTHROPIC_DEFAULT_SONNET_MODEL",
+    "opus": "ANTHROPIC_DEFAULT_OPUS_MODEL",
+}
+
+
+def _strip(model_id: str) -> str:
+    return model_id.split("[", 1)[0]
+
+
+def _family(model_id: str) -> str | None:
+    m = _strip(model_id)
+    return (
+        "claude" if m.startswith("claude-") else "gpt" if m.startswith("gpt-") else None
+    )
+
+
+def ladder(env: Env) -> tuple[str, tuple[str, ...]]:
+    """The primary ladder only when all four rung variables are set and non-empty."""
+    if all(env.get(v) for v in PRIMARY):
+        return "primary", PRIMARY
+    return "fallback", FALLBACK
+
+
+def plan(executor_tier: str, env: Env) -> dict[str, Pick]:
+    kind, rungs = ladder(env)
+    top = rungs[-1]
+    idx = rungs.index(executor_tier) if executor_tier in rungs else None
+    ids = {
+        r: _strip(env[r])
+        if kind == "primary"
+        else _strip(env.get(_ALIAS_VAR[r]) or f"claude-{r}-5-5")
+        for r in rungs
+    }
+
+    def make(name: str | None) -> Pick:
+        if name is None:  # no model of the wanted family can be reached
+            return Pick(
+                id="",
+                source="unreachable",
+                rung="T1",
+                launch="opus",
+                family_fallback=True,
+            )
+        rung = "top" if name == top else "T1" if name in T1_VARS else "other"
+        if kind == "primary":
+            return Pick(
+                id=ids[name],
+                source=name,
+                rung=rung,
+                launch="opus",
+                family_fallback=_family(ids[name]) != "claude",
+            )
+        return Pick(
+            id=ids[name], source=name, rung=rung, launch=name, family_fallback=False
+        )
+
+    def gpt_t1(own: str | None) -> str | None:
+        cands = [v for v in T1_VARS if _family(ids[v]) == "gpt"]
+        others = [v for v in cands if ids[v] != own]
+        return next(iter(others or cands), None)
+
+    def claude_top() -> str | None:
+        return next((r for r in reversed(rungs) if _family(ids[r]) == "claude"), None)
+
+    if kind == "fallback":  # Claude rungs only; a GPT T1 model is not launchable
+        a: str | None = top if idx is None else rungs[min(idx + 1, len(rungs) - 1)]
+        b: str | None = None
+    else:
+        fam = _family(ids[rungs[idx]]) if idx is not None else None
+        if idx is None:
+            a = top
+        elif fam == "gpt":
+            a = gpt_t1(ids[rungs[idx]])
+        elif fam == "claude":
+            a = (
+                top
+                if idx == len(rungs) - 1
+                else next(
+                    (r for r in rungs[idx + 1 :] if _family(ids[r]) == "claude"), top
+                )
+            )
+        else:
+            a = top
+        afam = _family(ids[a]) if a else None
+        if fam == "claude":
+            b = gpt_t1(None)
+        elif fam == "gpt":
+            b = claude_top()
+        else:
+            b = gpt_t1(None) if afam == "claude" else claude_top()
+    return {
+        "esc1_a": make(a),
+        "esc1_b": make(b),
+        "critique": make(a),
+        "esc2_1": make(top),
+        "esc2_2": make(top),
+    }
+
+
+# ------------------------------------------------------------ environments
+
+_OBSERVED = {
+    "T2bModel01": "gpt-6.1-terra",
+    "T2Model02": "glm-5.3",
+    "T1Model02": "gpt-6.1-sol",
+    "T1Model01": "claude-opus-5-5",
+    "T2Model01": "gpt-6.1-sol",
+}
+ENVS: dict[str, dict[str, str]] = {
+    "observed": dict(_OBSERVED),
+    "swapped": {
+        **_OBSERVED,
+        "T1Model01": "gpt-6.1-sol",
+        "T1Model02": "claude-opus-5-5",
+    },
+    "all-claude": {
+        "T2bModel01": "claude-haiku-5-5",
+        "T2Model02": "claude-sonnet-5-5",
+        "T1Model02": "claude-opus-5-5",
+        "T1Model01": "claude-fable-5-2",
+    },
+    "suffixed": {k: v + "[1m]" for k, v in _OBSERVED.items()},
+    "partial": {**_OBSERVED, "T1Model01": ""},
+    "fallback-tier-ids": {
+        "ANTHROPIC_DEFAULT_OPUS_MODEL": "gpt-6.1-sol[1m]",
+        "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5.3",
+        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "gpt-6.1-terra",
+    },
+}
+
+
+def violations(name: str, env: Env, tier: str, recs: Mapping[str, Pick]) -> list[str]:
+    kind, _ = ladder(env)
+    out: list[str] = []
+    for role in ROLES:
+        r = recs[role]
+        where = f"{name}/{tier}/{role}"
+        if r["launch"] not in AGENT_ALIASES or "[" in r["launch"]:
+            out.append(f"{where}: launch {r['launch']!r} is not a bare alias")
+        if r["source"] == "T2Model01":
+            out.append(f"{where}: picked T2Model01, which is never an adviser")
+        if kind == "primary":
+            if r["launch"] != "opus":
+                out.append(
+                    f"{where}: primary ladder launch is {r['launch']!r}, not opus"
+                )
+            if _family(r["id"]) != "claude" and not r["family_fallback"]:
+                out.append(
+                    f"{where}: non-claude pick {r['id']!r} lacks family-fallback"
+                )
+        elif r["source"] != "unreachable" and r["launch"] != r["source"]:
+            out.append(
+                f"{where}: fallback launch {r['launch']!r} is not its rung alias"
+            )
+    return out
+
+
+def sweep(planner: Planner) -> list[str]:
+    out: list[str] = []
+    for name, env in ENVS.items():
+        _, rungs = ladder(env)
+        for tier in (*rungs, "unknown"):
+            recs = planner(tier, env)
+            assert set(recs) == set(ROLES)
+            out += violations(name, env, tier, recs)
+    return out
+
+
+def test_sweep_is_clean_and_covers_both_ladders() -> None:
+    assert sweep(plan) == []
+    kinds = {ladder(env)[0] for env in ENVS.values()}
+    assert kinds == {"primary", "fallback"}
+    assert len(ENVS) == 6
+
+
+def _header(r: Pick) -> str:
+    fam = _family(r["id"]) or ""
+    line = f"model: {r['id']} family: {fam} rung: {r['rung']} launch: {r['launch']}"
+    return line + " family-fallback: no claude id" if r["family_fallback"] else line
+
+
+def test_header_never_states_a_served_family() -> None:
+    checked = 0
+    for name, env in ENVS.items():
+        _, rungs = ladder(env)
+        for tier in (*rungs, "unknown"):
+            for role, r in plan(tier, env).items():
+                if not r["id"] or r["rung"] not in ("T1", "top"):
+                    continue
+                if _family(r["id"]) is None:
+                    continue
+                m = re.match(
+                    r"^model: (\S+) family: (claude|gpt) rung: (T1|top) launch: (\w+)"
+                    r"(?: family-fallback: .+)?$",
+                    _header(r),
+                )
+                assert m is not None, (name, tier, role)
+                assert m.group(2) == _family(
+                    r["id"]
+                )  # the pick's family, never launch's
+                assert "served" not in _header(r)
+                checked += 1
+    assert checked > 0
+
+
+def _raw_id_launch(tier: str, env: Env) -> dict[str, Pick]:
+    return {k: {**v, "launch": v["id"]} for k, v in plan(tier, env).items()}
+
+
+def _never_family_fallback(tier: str, env: Env) -> dict[str, Pick]:
+    return {k: {**v, "family_fallback": False} for k, v in plan(tier, env).items()}
+
+
+def _t2model01_one_rung_up(tier: str, env: Env) -> dict[str, Pick]:
+    recs = plan(tier, env)
+    if tier == "T2Model02" and env.get("T2Model01"):
+        recs["esc1_a"] = Pick(
+            id=_strip(env["T2Model01"]),
+            source="T2Model01",
+            rung="other",
+            launch="opus",
+            family_fallback=True,
+        )
+    return recs
+
+
+@pytest.mark.parametrize(
+    "planner",
+    [_raw_id_launch, _never_family_fallback, _t2model01_one_rung_up],
+    ids=["raw-id", "no-family-fallback", "t2model01-one-rung-up"],
+)
+def test_negative_control_is_flagged(planner: Planner) -> None:
+    assert sweep(planner), "the checks missed a deliberately wrong resolver"
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
