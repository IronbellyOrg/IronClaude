# R3: Acceptance Test Rewrite + Canonical Skip-Guard / Shell-Out Shape

Status: Complete

Branch: `reflect/wrapper-gate-wiring`
Worktree: `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring`

Topic: The ACCEPTANCE TEST rewrite target — Layer A of
`tests/cli/reflect/test_no_nesting_guard.py` — and the canonical skip-guard /
shell-out shape from the reflect-wrapper interface contract.

Decision of record (Option A): REWRITE `test_layer_a_wrapper_branch_is_bash_shellout`
+ helper `_extract_wrapper_branch` to assert the FLAT O1 contract shape
(`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip-guard + `superclaude reflect run …
--depth deep --fix --promote`) against the NEW O1 emission in
`task-builder/SKILL.md`. Layer B + package-wide thinness tests are UNCHANGED.

---

## 1. VERBATIM current Layer A (the rewrite target) + module constants

File: `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py`
(135 lines total.)

### 1a. Module-level constants / regexes the tests use (lines 18-46)

These are SHARED by Layer A and Layer B. Of these, ONLY `_SKILL_SRC` (line 20)
and `_NESTING_TOKENS` (line 46) are consumed by Layer A. The rewrite MUST NOT
alter the other constants (Layer B / thinness tests depend on them).

```python
18	# Repo root = four parents up from this file (tests/cli/reflect/<file>).
19	_REPO_ROOT = Path(__file__).resolve().parents[3]
20	_SKILL_SRC = _REPO_ROOT / "src/superclaude/skills/task-builder/SKILL.md"
21	_REFLECT_PKG = _REPO_ROOT / "src/superclaude/cli/reflect"
22	_RUNNER_SRC = _REFLECT_PKG / "runner.py"
23	# Every reflect-wrapper source module (thinness guards apply package-wide).
24	_REFLECT_PY = sorted(p for p in _REFLECT_PKG.glob("*.py") if p.name != "__init__.py")
25	
26	# Import statements pulling in the heavy sibling subcommand packages (NFR-1).
27	# Anchored on `from`/`import` so the guardrail DOCSTRING prose
28	# ("No imports from ``superclaude.cli.sprint``") never false-positives.
29	_SPRINT_ROADMAP_IMPORT_RE = re.compile(
30	    r"^\s*(?:from|import)\s+\S*(?:sprint|roadmap)", re.MULTILINE
31	)
32	# Real async/await CODE (anchored), not the docstring word "async def".
33	_ASYNC_DEF_RE = re.compile(r"^\s*async\s+def\b", re.MULTILINE)
34	_AWAIT_RE = re.compile(r"^\s*await\s", re.MULTILINE)
35	# Real raw-subprocess CALLS (identifier.method followed by `(`) + import lines.
36	# Anchored so the _apply_remediation docstring prose ("never a raw
37	# ``subprocess.run`` / ``Popen``") does NOT false-positive (it has no `(`).
38	_RAW_SUBPROCESS_CALL_RE = re.compile(r"\b(?:subprocess\.(?:run|Popen)|Popen)\s*\(")
39	_IMPORT_SUBPROCESS_RE = re.compile(
40	    r"^\s*(?:import\s+subprocess|from\s+subprocess\b)", re.MULTILINE
41	)
42	
43	# Actual agent-routing tokens (a real Agent/Task invocation). Prose tokens like
44	# "via Agent" are intentionally NOT included: the Mode-2 Action legitimately reads
45	# "NEVER via Agent/Task" as a prohibition, which must not trip the no-nesting guard.
46	_NESTING_TOKENS = ("Task(", "subagent_type")
```

### 1b. `_extract_wrapper_branch` helper (lines 49-60) — TO BE REWRITTEN

```python
49	def _extract_wrapper_branch(text: str) -> str:
50	    """Return the text of the Mode-2 wrapper block in the Phase-N template.
51	
52	    The ``--reflect`` dial replaced the legacy ``Wrapper arm
53	    (POST_REFLECT_MODE: wrapper)`` heading with the per-mode ``Mode 2`` template;
54	    the Bash ``superclaude reflect run`` shell-out behaviour is unchanged.
55	    """
56	    marker = "**Mode `2` / `auto-resolved-2` (§6.3, DEFAULT) — wrapper shell-out, remediate:**"
57	    start = text.index(marker)
58	    # The Mode-2 block ends where the next mode (halt) heading begins.
59	    end = text.index("**Mode `halt`", start)
60	    return text[start:end]
```

The `marker` (line 56) and the `end` anchor `"**Mode \`halt\`"` (line 59) are the
STALE, abandoned-dial markers. They reference the Mode taxonomy (`Mode 2` /
`auto-resolved-2` / `§6.3`) that the contract explicitly abandons (contract §intro
line 16: "The `--reflect` dial is ABANDONED (PR #157 closed)"). These markers
exist nowhere in any current SKILL/spec on this base.

### 1c. The `@pytest.mark.xfail(...)` decorator + test body (lines 63-84) — TO BE REWRITTEN

```python
63	@pytest.mark.xfail(
64	    reason=(
65	        "Cross-component: this Layer-A guard asserts the task-builder SKILL Mode-2 "
66	        "wrapper shell-out block (marker `auto-resolved-2`), which is GENERATOR-side "
67	        "content emitted by the companion worktree (reflect/f3-hygiene-stage105-e2e). "
68	        "It is absent on this wrapper-only canonical base (and on origin/master). "
69	        "Adding it here would couple the wrapper to unmerged generator work, which "
70	        "NFR-5 forbids. XPASSes (auto-recovers) once the generator's task-builder "
71	        "Mode-2 block lands. Out of scope for TASK-RF-reflect-wrapper-autofix."
72	    ),
73	    strict=False,
74	)
75	def test_layer_a_wrapper_branch_is_bash_shellout() -> None:
76	    """The wrapper arm is a Bash CLI shell-out with the TCS depth baked (G3)."""
77	    text = _SKILL_SRC.read_text(encoding="utf-8")
78	    branch = _extract_wrapper_branch(text)
79	    # POSITIVE: invokes the CLI as a shell command with the depth passthrough.
80	    assert "superclaude reflect run" in branch
81	    assert "--depth" in branch
82	    # NEGATIVE: must NOT route through the Agent/Task tool surface (NFR-7).
83	    for token in _NESTING_TOKENS:
84	        assert token not in branch, f"NFR-7 violation: nesting token {token!r}"
```

---

## 2. EVERY other test/function in the file — DO NOT MODIFY

The builder must edit ONLY the Layer A surface in §1 (lines 49-84 helper +
decorator + test). Everything below is OUT OF SCOPE and MUST be left byte-identical.

| Lines | Symbol | Layer | DO NOT MODIFY — why |
|-------|--------|-------|---------------------|
| 1-9 | module docstring | — | Describes Layer A + Layer B intent. MAY need a one-line prose refresh if dropping the stale `POST_REFLECT_MODE: wrapper` wording, but this is cosmetic + OPTIONAL; assertions live in the test body, not here. Treat as DO-NOT-MODIFY unless explicitly refreshing the Layer-A description. |
| 11-16 | imports (`__future__`, `re`, `Path`, `pytest`) | — | DO NOT MODIFY — all four still needed by rewritten Layer A (`re` by Layer B regexes; `pytest` by the marker; `Path` by `_SKILL_SRC`). |
| 18-24 | `_REPO_ROOT`, `_SKILL_SRC`, `_REFLECT_PKG`, `_RUNNER_SRC`, `_REFLECT_PY` | shared | DO NOT MODIFY — Layer B + thinness tests resolve paths through these. `_SKILL_SRC` reused by rewritten Layer A. |
| 26-41 | `_SPRINT_ROADMAP_IMPORT_RE`, `_ASYNC_DEF_RE`, `_AWAIT_RE`, `_RAW_SUBPROCESS_CALL_RE`, `_IMPORT_SUBPROCESS_RE` | thinness | DO NOT MODIFY — consumed only by package-wide thinness tests. Untouched by Layer A. |
| 43-46 | `_NESTING_TOKENS` | shared | DO NOT MODIFY — rewritten Layer-A negative NFR-7 assertion reuses this tuple verbatim. |
| 87-94 | `test_layer_b_wrapper_module_has_no_agent_imports` | **Layer B** | DO NOT MODIFY — asserts `runner.py` uses `ClaudeProcess` and bans `import anthropic` / `from anthropic` / `subagent` / `Task(`. Independent of the SKILL. |
| 97-105 | `test_no_sprint_or_roadmap_import_anywhere_in_reflect_pkg` | thinness | DO NOT MODIFY — AC-8 / NFR-1: no sprint/roadmap import in any `cli/reflect/*.py`. |
| 108-117 | `test_no_async_await_anywhere_in_reflect_pkg` | thinness | DO NOT MODIFY — AC-8 / NFR-1: zero `async def` / `await` in the package. |
| 120-134 | `test_apply_remediation_launches_only_via_claudeprocess` | thinness | DO NOT MODIFY — AC-8: `_apply_remediation` launches via `ClaudeProcess` `/task`, never raw subprocess. |

Net: only lines **49-84** are in scope (helper + decorator + Layer-A test).
Optionally the module docstring lines 1-9 if a prose refresh is desired.

---

## 3. PROPOSED rewritten Layer A

### 3a. The anchor problem

The current helper delimits the wrapper block with the abandoned-Mode marker.
The rewrite needs a STABLE, greppable anchor that the O1 emission block in
`task-builder/SKILL.md` (researcher R1's surface) can actually CARRY —
**generic/flat, NOT** `Mode 2` / `auto-resolved-2` / `§6.3`.

**Proposed anchor (coordinate with R1):** a flat heading that introduces the O1
terminal-gate block, e.g.

```
#### POST reflect gate (O1 — terminal, whole tasklist)
```

…immediately followed by a fenced ```bash block carrying the skip-guard + the
`superclaude reflect run … --depth deep --fix --promote` shell-out. Two viable
delimiting strategies for `_extract_wrapper_branch`:

- **Option (i) — heading-anchored slice (recommended).** Find the heading
  `#### POST reflect gate (O1` and slice from there to the next `####`/`---`
  boundary. Robust to bash-block reflow; the heading is human-meaningful and
  greppable. Requires R1 to emit that exact heading prefix.
- **Option (ii) — fenced-bash sentinel.** Slice the first ```` ```bash ```` …
  ```` ``` ```` fence that contains `superclaude reflect run`. Tighter (asserts
  against the literal command block) but couples the test to the fence being the
  FIRST such block. Acceptable if R1 guarantees a single O1 bash block.

Recommendation: **Option (i)** — anchor on the flat heading prefix
`#### POST reflect gate (O1`, fall back to scanning to the next `####` or `---`.
This keeps the helper resilient and the anchor name carries no Mode taxonomy.
The exact heading text is an R1/R3 coordination point — propose R1 emit a heading
beginning literally `#### POST reflect gate (O1`.

### 3b. Proposed `_extract_wrapper_branch` (heading-anchored)

```python
def _extract_wrapper_branch(text: str) -> str:
    """Return the O1 terminal reflect-gate block from the task-builder SKILL.

    The block is delimited by the flat ``#### POST reflect gate (O1`` heading
    (no Mode taxonomy) and runs to the next ``####`` sub-heading or ``---`` rule.
    Carries the SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE skip-guard + the
    ``superclaude reflect run … --depth deep --fix --promote`` Bash shell-out.
    """
    anchor = "#### POST reflect gate (O1"
    start = text.index(anchor)
    rest = text[start + len(anchor):]
    # End at the next sub-heading or horizontal rule, whichever comes first.
    candidates = [i for i in (rest.find("\n#### "), rest.find("\n---")) if i != -1]
    end = (start + len(anchor) + min(candidates)) if candidates else len(text)
    return text[start:end]
```

(If R1 prefers the fenced-bash sentinel, swap to Option (ii) — but heading-anchored
is the safer default and tolerates the bash block being multi-line.)

### 3c. Proposed rewritten Layer-A test body

```python
def test_layer_a_o1_gate_is_guarded_bash_shellout() -> None:
    """O1 terminal gate is a guarded Bash CLI shell-out (contract §2 / §3.2)."""
    text = _SKILL_SRC.read_text(encoding="utf-8")
    branch = _extract_wrapper_branch(text)
    # POSITIVE — the flat O1 shell-out (contract §2):
    assert "superclaude reflect run" in branch
    assert "--depth deep" in branch
    assert "--fix" in branch
    assert "--promote" in branch
    # POSITIVE — the recursion-breaker skip-guard marker (contract §3.2):
    assert "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE" in branch
    # NEGATIVE — must NOT route through the Agent/Task tool surface (NFR-7):
    for token in _NESTING_TOKENS:
        assert token not in branch, f"NFR-7 violation: nesting token {token!r}"
```

Notes:
- `--depth deep` (not bare `--depth`) — the contract O1 line is exactly
  `--depth deep` (contract §2 line 38). Asserting the literal `deep` is stronger
  and matches the real emission.
- Negative checks reuse the existing `_NESTING_TOKENS` tuple (`"Task("`,
  `"subagent_type"`) — unchanged, per task scope ("SAME NFR-7 negative checks").
- Renaming the test from `..._wrapper_branch_is_bash_shellout` to
  `..._o1_gate_is_guarded_bash_shellout` is OPTIONAL but clarifying. For minimal
  churn / preserved test-id, KEEP the old name
  `test_layer_a_wrapper_branch_is_bash_shellout`. Minor open choice — flag to user.

### 3d. xfail decorator disposition — OPEN QUESTION (user decides)

The current decorator (lines 63-74) xfails because the Mode-2 block is
generator-side content absent on this base. After the rewrite, the O1 block is
emitted by THIS task's R1 surface in `task-builder/SKILL.md` **in this worktree**,
so the test SHOULD pass on this base.

Options:

- **(a) Keep `@pytest.mark.xfail(..., strict=False)`** → if the O1 block lands,
  the test XPASSes (reported, non-failing); if R1's emission is missing/wrong, it
  stays xfail (silent). Pro: never red on a half-wired tree. Con: a genuinely
  broken O1 emission is masked as "expected fail" — the gate provides NO real
  signal. This re-creates the exact blind spot the rewrite is meant to remove.
- **(b) Remove the decorator → plain PASS test.** Pro: real green/red signal —
  the test genuinely guards the O1 shape and fails loudly if R1's emission drifts
  or the guard/flags are missing. Con: requires R1's O1 block present in THIS
  worktree's `task-builder/SKILL.md` when the test runs (it will be, since R1
  emits it as part of the same task).

**Recommendation: (b) remove the decorator → plain PASS test.** Rationale: the
whole point of Option A is that this worktree now OWNS the O1 emission (R1) AND
the acceptance test (R3) together — they land in the same task, on the same base.
An xfail would defeat the acceptance signal. Keep (b) UNLESS the user wants the
O1 SKILL emission deferred to a later task, in which case (a) `strict=False` is
the bridge. **Mark as Open Question for the user** — the right answer depends on
whether R1's O1 block is in-scope for THIS task (it is, per the task framing) or
deferred.

---

## 4. VERBATIM contract — §3.2 safe-emission guard + §2 exit-code table

These are the EXACT text the SKILL O1/O2 blocks must contain. Source:
`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md`

### 4a. §3.2 safe emission shape (contract lines 99-104)

````
```bash
if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then
  echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0
fi
superclaude reflect run <FILE> --depth deep --fix [--promote|--no-promote --base <SHA>]
```
````

Marker semantics (contract lines 78, 106-108):
- **Marker:** env var `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`.
- "Truthy value is exactly the string `"1"`. Absent/empty/any-other-value ⇒ not
  suppressed (normal run)."
- Generators MUST NOT clear/unset/overwrite it, MUST NOT introduce a second
  marker or rename it (contract lines 95, 106).

This marker name matches the CLI exactly: `commands.py:44`
`_WRAPPER_MARKER_ENV = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"`, and the truthiness
check at `commands.py:69` is `os.environ.get(_WRAPPER_MARKER_ENV, "").strip() == "1"`.

### 4b. §2 O1 invocation shape (contract lines 37-39)

````
```bash
superclaude reflect run <ABS_TASKLIST_PATH> --depth deep --fix --promote
```
````

§2 O2 invocation shape (contract lines 49-51, for R2's surface, cross-reference):

````
```bash
superclaude reflect run <ABS_PHASE_FILE_PATH> --depth deep --fix --no-promote --base <PHASE_N_START_SHA>
```
````

### 4c. §2 exit-code table (contract lines 65-73)

```
| Exit | Verdict | Gate meaning |
|------|---------|--------------|
| 0 | pass | clean OR auto-fixed-and-verified (and promoted if O1) → gate PASSES |
| 10 | halted | deviations a human must resolve, or fix loop did not converge → gate FAILS, surface |
| 11 | degraded | audit untrustworthy (lost chain-critical capability) → gate FAILS |
| 2 | blocked | child crash / timeout / missing-or-bad contract → gate FAILS |
```

"Only exit 0 may let the tasklist/phase complete." (contract line 73)

The exit-code semantics match the CLI: `commands.py:36` `_BLOCKED_EXIT = 2`, and
`commands.py:235` `exit_code = result.verdict.exit_code` (pass 0 / halted 10 /
degraded 11 / blocked 2, per the `run` docstring lines 165-167).

---

## 5. OTHER on-disk copies of this test in sibling worktrees — DO NOT TOUCH

`tests/cli/reflect/test_no_nesting_guard.py` exists in three worktrees:

| Worktree | Path | md5 | State |
|----------|------|-----|-------|
| **ReflectGateWiring** (THIS) | `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py` | `124549e67dd25258c7739371b4a89cb2` | **THE rewrite target.** Has the xfail decorator + stale Mode-2 marker (135 lines). |
| reflectWrapper | `/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/tests/cli/reflect/test_no_nesting_guard.py` | `124549e67dd25258c7739371b4a89cb2` | **BYTE-IDENTICAL** to THIS worktree (same md5). Same xfail + stale marker. |
| wrapper-onto-master | `/config/workspace/IronClaude/.claude/worktrees/wrapper-onto-master/tests/cli/reflect/test_no_nesting_guard.py` | `9017231d8ff5c59ac0b6e879310c34a7` | **STALE / un-xfailed.** No xfail decorator; Layer A helper starts at line 26 (vs 49 here). Older shape — asserts the stale `auto-resolved-2` marker but as a hard PASS test. |

**THE TASK MUST NOT TOUCH OTHER WORKTREES.** Edit ONLY this worktree's file:
`/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/tests/cli/reflect/test_no_nesting_guard.py`.
Per memory `feedback_worktree_discipline`, all artifact paths resolve to THIS
worktree. The `reflectWrapper` and `wrapper-onto-master` copies are independent
checkouts on their own branches; reconciling them is out of scope (and would be a
cross-worktree edit, forbidden). Do NOT `cd` into them, do NOT edit them, do NOT
reference their paths as edit targets.

---

## 6. CLI `run` flag names — CONFIRMED verbatim from commands.py

Source: `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/src/superclaude/cli/reflect/commands.py`
(the `run` command, lines 76-162). The test asserts REAL tokens:

| Flag (verbatim) | commands.py line | Definition |
|-----------------|------------------|------------|
| `--depth` | 101-106 | `click.Choice(["standard", "deep"], case_sensitive=False)`, default `"standard"`. So `--depth deep` is valid; `deep` is a real choice. |
| `--fix` / `--no-fix` | 127-132 | `--fix/--no-fix` boolean, var `fix`, default `False`. O1/O2 emit `--fix`. |
| `--promote` / `--no-promote` | 89-94 | `--promote/--no-promote` boolean, var `promote`, default `True`. O1 emits `--promote` (or omits — default True); O2 emits `--no-promote`. |
| `--base` | 139-147 | `--base`, var `base_override`, default `None`. "Explicit audit base ref (single ref vs working tree)." O2 emits `--base <SHA>`. |

Supporting real flags (present, not asserted by Layer A but real): `--tmux`
(82-83), `--print-command` (84-88), `--timeout` (95-100), `--output` (107-111),
`--allow-single-vendor` (112-116), `--dry-run` (117-121), `--resume` (122-126),
`--max-fix-iterations` (133-138).

All contract-critical flags (`--depth deep`, `--fix`, `--promote`,
`--no-promote`, `--base`) are REAL Click options on `run` — the rewritten Layer-A
positive assertions reference tokens that genuinely exist in the CLI surface.

Recursion-breaker confirmation (commands.py): `_WRAPPER_MARKER_ENV =
"SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` (line 44); group-callback guard at lines
69-73 exits 0 when the env var `.strip() == "1"`. The SKILL skip-guard in §4a
mirrors this exactly — same env name, same `"1"` truthiness.

---

## Summary (5 lines)

1. Rewrite target is lines **49-84** ONLY (`_extract_wrapper_branch` + xfail
   decorator + `test_layer_a_wrapper_branch_is_bash_shellout`); all other functions
   (Layer B 87-94, thinness 97-134) + constants are DO-NOT-MODIFY.
2. New anchor must be FLAT/generic — proposed `#### POST reflect gate (O1` heading
   (no `Mode 2`/`auto-resolved-2`/`§6.3`); helper slices to next `####`/`---`.
   Coordinate the exact heading with R1's `task-builder/SKILL.md` O1 emission.
3. New assertions — POSITIVE: `superclaude reflect run`, `--depth deep`, `--fix`,
   `--promote`, `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`; NEGATIVE: reuse
   `_NESTING_TOKENS` (`Task(`, `subagent_type`). All flags confirmed real in
   commands.py (`--depth`/`--fix`/`--promote`/`--no-promote`/`--base`).
4. xfail disposition is an OPEN QUESTION — recommend **(b) remove decorator →
   plain PASS** (this worktree owns both O1 emission + the test); fallback
   (a) `strict=False`/XPASS only if O1 SKILL emission is deferred to a later task.
5. Edit ONLY this worktree's file; `reflectWrapper` is byte-identical
   (md5 `124549e6…`) and `wrapper-onto-master` is stale/un-xfailed
   (md5 `9017231d…`) — both MUST NOT be touched. §3.2 guard + §2 exit-code table
   quoted verbatim in §4 as the literal text the SKILL O1/O2 blocks must carry.
