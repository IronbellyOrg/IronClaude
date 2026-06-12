# Gap-Fill Research: O2 Viability + 6 Research-Gate Gaps

**Status: Complete**
**Branch:** reflect/wrapper-gate-wiring
**Scope:** Close the 6 gaps surfaced by the research gate with hard, file:line-cited evidence from the landed wrapper engine (PR #159), the Sprint executor, the sc-tasklist + task-builder SKILLs, and the authoritative interface contract.

## Evidence base (read this turn)

- Wrapper engine: `src/superclaude/cli/reflect/{commands,runner,config,contract}.py`
- Contract (authoritative): `/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md`
- sc-tasklist gate template: `src/superclaude/skills/sc-tasklist-protocol/{SKILL.md,templates/phase-template.md}`
- task-builder O1 template: `src/superclaude/skills/task-builder/SKILL.md`
- Sibling tests: `tests/cli/reflect/{test_promote_plumbing.py,test_cli_smoke.py,test_no_nesting_guard.py}`

---

## GAP-1 — O2 `--base` per-phase start-SHA resolution at execution time

**VERDICT: RESOLVED (no fabricated SHA; two sanctioned mechanisms, neither is a mechanical CLI substitution).**

### Finding: there is NO programmatic `<phase-commit-range>` placeholder substitution in the Sprint CLI.

A full grep of `src/superclaude/cli/sprint/` for `phase-commit-range`, `phase_commit_range`, `substitut`, `placeholder` finds NO code that rewrites `<phase-commit-range>` into a SHA. The only `placeholder` hits are the tmux summary pane (`tmux.py:47`) and the `TASKLIST_ROOT/` prefix strip in `checkpoints.py:115` — neither resolves git ranges. The Sprint executor (`executor.py`) performs no `<phase-*>` token substitution.

### How the EXISTING per-phase reflect task resolves it: an in-task `[VERIFICATION]` STEP, run by the executing agent.

`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1067`:
> `1. **[VERIFICATION]** Resolve \`<phase-commit-range>\` = the git range covering all of Phase <PP>'s task commits.`

(mirrored in `templates/phase-template.md:158`). The narrative gloss "resolved by the Sprint executor at run time" (`SKILL.md:1038`, `phase-template.md:129`) is misleading shorthand: the resolver is the **agent executing the reflect task under the sprint**, performing the Step-1 `[VERIFICATION]` git computation — NOT a mechanical string-substitution pass in the `superclaude sprint` Python. So `<phase-commit-range>` is a HUMAN/AGENT-resolved placeholder, never a generation-time fabricated SHA, and never a CLI-substituted token.

### What the authoritative contract mandates for O2 `--base` (this overrides the old range form).

`reflect-wrapper-contract.md` §2 (lines 47-51):
> `superclaude reflect run <ABS_PHASE_FILE_PATH> --depth deep --fix --no-promote --base <PHASE_N_START_SHA>`
> `--base <PHASE_N_START_SHA>` pins the audit to phase-N work ONLY (single ref vs working tree — NOT a `<base>..HEAD` range).

§6 (lines 164-173) gives the precedence chain and the TWO equivalent emission mechanisms:
- Canonical: **explicit `--base <PHASE_N_START_SHA>` on the gate line** (generator records each phase's start SHA and passes it).
- Equivalent: write a **per-phase `start_commit` to that phase file's frontmatter**; the wrapper resolves it (precedence `--base` > frontmatter `start_commit` > `git merge-base HEAD master`).

This is corroborated in the engine: `config.py:_resolve_base` (lines 81-105) implements EXACTLY that precedence — `base_override` (the `--base` value, `commands.py:139-147`) first, then frontmatter `start_commit` (`config.py:51,99-101`), then `git merge-base HEAD <base_branch=master>` (`config.py:103`).

### CAN O2 emit `--base <phase-N-start-sha>` as the same CLASS of runtime placeholder?

YES — but the "runtime resolver" is the **executing reflect-task agent** via a `[VERIFICATION]` step, identical to how the legacy `<phase-commit-range>` was resolved. There is no Sprint-CLI substitution to piggyback on, because none ever existed. So the gate line emits a LITERAL placeholder token (e.g. `<PHASE_N_START_SHA>` or `<phase-N-start-sha>`) and the task's Step-1 `[VERIFICATION]` instructs the agent to resolve it to the real SHA (e.g. the first commit of the phase, or `git rev-parse` of the phase's start tag) before invoking the gate. This is mechanically consistent with the existing template and violates no "no-fabricated-SHA" rule — generation time writes only the placeholder + the resolution instruction.

**EITHER (preferred, matches contract canonical path):** gate line carries `--base <PHASE_N_START_SHA>` placeholder + a Step-1 `[VERIFICATION]` "Resolve `<PHASE_N_START_SHA>` = the SHA of the commit immediately preceding Phase <PP>'s first task commit (e.g. `git rev-parse <phase-(N-1)-end>` or the recorded phase-start SHA)."
**OR (equivalent):** persist per-phase `start_commit` in that phase file's frontmatter and DROP `--base` (wrapper falls back to frontmatter `start_commit`). NOTE: this collides with GAP-2 — phase files have NO frontmatter today, so the frontmatter route REQUIRES seeding frontmatter anyway.

**No `needs_human_decision` required for the resolution MECHANISM.** (The depth/placeholder *wording* is a builder detail.)

---

## GAP-2 — `reflect_post` writeback into phase files that have NO frontmatter today

**VERDICT: RESOLVED → Option 2A (pre-seed minimal frontmatter + amend struct check #5). The wrapper does NOT create a frontmatter block; it fail-skips when none exists, and O2's `--no-promote` posture means that skip would NOT fail-close — so the silent-no-writeback footgun is real and must be pre-empted by seeding frontmatter.**

### Exactly how the wrapper writes `reflect_post:` back.

`runner.py:write_reflect_post` (lines 117-185):
1. Reads bytes, finds the FIRST `---...---` frontmatter block via `_FRONTMATTER_RE` (`runner.py:44`).
2. **`runner.py:146-148`:** `fm_match = _FRONTMATTER_RE.search(text); if fm_match is None: return "frontmatter-missing"`.
   → If there is NO frontmatter block, the function RETURNS EARLY with status `"frontmatter-missing"` and writes NOTHING. It does **(c) error/skip** — it does NOT (b) create a frontmatter block.
3. When frontmatter EXISTS but has no `reflect_post:` key, it APPENDS the block inside the existing frontmatter (`runner.py:168-170`: "No existing reflect_post: key -- append the block to the frontmatter.").

So writeback is VIABLE **only if a frontmatter block already exists.**

### Does the missing-frontmatter skip fail closed? NO — and that is the load-bearing risk for O2.

`runner.py:586-590`:
```
result.write_status = write_status
# FR-6: an unwritable/stale frontmatter must fail-closed (non-zero exit).
if write_status != "written" and result.verdict is Verdict.PASS:
    result.verdict = Verdict.BLOCKED
    result.reason = write_status or "frontmatter-unwritable"
```
The fail-close to BLOCKED fires ONLY when `result.verdict is Verdict.PASS`. So a clean PASS audit on a no-frontmatter phase file → `write_status="frontmatter-missing"` → verdict flips to BLOCKED (exit 2) → **the O2 gate FAILS even though the audit passed.** That is a guaranteed false-FAIL for every clean phase, because phase files have no frontmatter (struct check #5 below).

### Phase files have NO frontmatter today (struct check #5 mandates `# Phase N` as the literal first line).

`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1128` (Sprint Compatibility Self-Check #5):
> `5. Every phase file starts with \`# Phase N -- <Name>\` (level 1 heading, em-dash separator)`

A leading `---\n…\n---` YAML frontmatter block would push `# Phase N` off line 1, tripping check #5. So today phase files cannot carry frontmatter, and `reflect_post` writeback is structurally IMPOSSIBLE for O2 without a change.

### The contract's stance.

`reflect-wrapper-contract.md` §6 line 174-175:
> `reflect_post:` is written BACK by the wrapper — generators must leave room for it (do not hand-author or lock it).

"Leave room" presupposes a frontmatter block EXISTS for the wrapper to splice into. Combined with §6's requirement that O2 persist a per-phase `start_commit` and `executor_model_class` in frontmatter (lines 165-166, §8 lines 196-197), the contract already DEMANDS phase-file frontmatter. The wrapper-create path does not exist (`runner.py:147-148`), so the generator MUST seed it.

### Resolution — Option 2A (and it subsumes 2B/2C).

- **Option 2A (CORRECT): pre-seed a minimal YAML frontmatter into each phase file AND amend struct check #5.** Seed e.g.:
  ```
  ---
  start_commit: <PHASE_N_START_SHA>          # GAP-1 equivalent route, optional if --base on gate line
  executor_model_class: <EXECUTOR_CLASS>     # §6 required, O1+O2
  # reflect_post written back by the wrapper — leave room
  ---
  # Phase N -- <Name>
  ```
  Then amend `SKILL.md:1128` (struct check #5) + the parallel checks in `templates/` and the validation prose to read: "Every phase file starts with an OPTIONAL YAML frontmatter block, immediately followed by `# Phase N -- <Name>`." The `_FRONTMATTER_RE` is preamble-tolerant only for matching, but the FIRST content must still be a clean `---` block; the struct-check is the gate that must move.
  - This single seed ALSO supplies `executor_model_class` (so reflect's `--executor-model` resolves via `config.py:53,201-205`) AND optionally `start_commit` (GAP-1 frontmatter route).

- **Option 2B (INSUFFICIENT alone): pass `--executor-model` via frontmatter only / rely on wrapper to CREATE frontmatter for `reflect_post`.** REJECTED on evidence: `runner.py:147-148` proves the wrapper does NOT create a frontmatter block; it returns `"frontmatter-missing"` and (for a PASS) BLOCKS. 2B's premise ("rely on the wrapper to create frontmatter") is false. Note: `--executor-model` is NOT a wrapper CLI flag at all (it's reflect-native; the wrapper sources `executor_model` from `EXECUTOR_MODEL_CLASS` env or frontmatter `executor_model_class`, `config.py:56,201-205`, then forwards it into the inner reflect prompt at `runner.py:363-364`). So there is no `--executor-model` to put on the O2 gate line; it MUST come from env or frontmatter → reinforces 2A.

- **Option 2C (writeback target differs): REJECTED.** `commands.py:77-80` + `config.py:165-167` bind the writeback target to the single positional `tasklist` argument (the audited file). For O2 that IS the phase file. There is no alternate writeback sink — the `reflect_post` block goes into the audited file's own frontmatter (`runner.py:117,138,184`) and the sidecar `wrapper-result.yaml` goes to `--output` (`runner.py:224`). So O2's writeback target IS the phase file; 2C does not apply.

**CONCLUSION: Option 2A is mechanically forced.** Phase files MUST be pre-seeded with a minimal frontmatter block (carrying `executor_model_class`, optionally `start_commit`, leaving room for `reflect_post`), and struct check #5 (SKILL.md:1128 + template/validation mirrors) MUST be amended to allow optional frontmatter before `# Phase N`. Without 2A, every clean O2 phase audit false-FAILs at exit 2 (`runner.py:588-590`).


---

## GAP-3 — `--output` for O2 (default vs declared `validation/reflect-post/phase-<PP>/`)

**VERDICT: RESOLVED → add `--output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/` to the O2 gate line. The default does NOT match the declared path or the report-existence Acceptance Criterion.**

### The wrapper's default output dir.

`config.py:207-213`:
```
if output_dir:
    resolved_output = Path(output_dir).resolve()
else:
    resolved_output = (resolved_tasklist.parent / "reflect" / "post" / head[:12]).resolve()
```
i.e. default = `<phase-file-dir>/reflect/post/<head-12-sha>/`. For a phase file at `TASKLIST_ROOT/phase-<PP>-tasklist.md`, that is `TASKLIST_ROOT/reflect/post/<sha>/` — NOT `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/`.

### What lands in `--output`.

The sidecar `wrapper-result.yaml` (`runner.py:224`), `reflect-stdout.json`/`reflect-stderr.log` (`runner.py:407-408`), the `.reflect-exitcode` sentinel (`commands.py:270-276`), and the reflect run's own `--output` (forwarded into the inner prompt at `runner.py:365`) all go to `config.output_dir`. The human-facing `REPORT.md` that reflect authors lands under that same reflect `--output`.

### Existing declared path + Acceptance Criterion.

`SKILL.md:1060` declares `**Reflect Report Path:** TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md` and `SKILL.md:1072` makes its existence an Acceptance Criterion ("File `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md` exists…"). The legacy template ALREADY passes `--output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/` on its `/sc:reflect` spawn line (`SKILL.md:1063`).

**RECOMMENDED O2 `--output` value (exact):** `--output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/`
This keeps the declared `**Reflect Report Path:**` and the report-existence Acceptance Criterion valid, and matches the legacy spawn line so the migration to `superclaude reflect run` is path-stable. (The default is NOT acceptable — it would write to `TASKLIST_ROOT/reflect/post/<sha>/`, orphaning the declared path + AC.) `TASKLIST_ROOT` itself is resolved the same way as every other path in the phase file (literal `TASKLIST_ROOT/` prefix — see GAP-4).

---

## GAP-4 — Absolute-path emission for `<ABS_TASKLIST_PATH>` (O1) and `<ABS_PHASE_FILE_PATH>` (O2)

**VERDICT: RESOLVED. The wrapper resolves whatever path string it is given to an absolute path itself (`resolve_path=True`), so the generators do NOT need to fabricate an abspath at emit time — they emit the SAME path token the rest of the file uses, and an in-task `[VERIFICATION]`/runtime resolution supplies the real abspath.**

### The wrapper already absolutizes its positional argument.

`commands.py:77-80`:
```
@click.argument("tasklist", type=click.Path(exists=True, dir_okay=False, resolve_path=True))
```
`resolve_path=True` makes Click resolve the given path to an absolute, symlink-resolved path BEFORE the command body runs. `config.py:165` re-resolves defensively (`Path(tasklist_path).resolve()`). So the wrapper does not require the caller to pass an already-absolute string — a relative path resolves against the process cwd.

### Concrete emission mechanism per site.

- **O1 (task-builder, whole tasklist):** the legacy template uses `{TASK_FILE}` (`SKILL.md:2195`) — a token the builder substitutes with the generated task file's path at emit time, and the executor invokes from the repo root. The `<ABS_TASKLIST_PATH>` the contract names (§2 line 39) is satisfied by emitting `{TASK_FILE}` (which the builder already knows as an absolute or repo-relative path) OR a Step that resolves it via `$(git rev-parse --show-toplevel)/<rel>`/`realpath`. Because `resolve_path=True` absolutizes a repo-relative path against cwd, a repo-relative `{TASK_FILE}` is sufficient when the gate runs from the repo root; for safety the gate line SHOULD carry an absolute token resolved by the executor.
- **O2 (sc:tasklist, phase file):** the phase file references itself today as `TASKLIST_ROOT/phase-<PP>-tasklist.md` — a LITERAL `TASKLIST_ROOT/` prefix placeholder (`SKILL.md:1063`, `1060`, `1072`; `phase-template.md:151,154,163`), NOT an absolute path and NOT a `$(pwd)`-relative form. `TASKLIST_ROOT` is computed by the generator per `SKILL.md:67-74` (e.g. `.dev/releases/current/<segment>/`). The contract's `<ABS_PHASE_FILE_PATH>` (§2 line 47) is satisfied either by (a) emitting `TASKLIST_ROOT/phase-<PP>-tasklist.md` and relying on `resolve_path=True` + repo-root cwd, or (b) a Step-1 `[VERIFICATION]` that resolves `TASKLIST_ROOT` to an abspath (`$(git rev-parse --show-toplevel)/.dev/releases/current/<segment>` or `realpath`).

**Concrete recommendation:** Neither generator should fabricate a literal SHA-pinned abspath at generation time. O1 emits its existing `{TASK_FILE}` token; O2 emits its existing `TASKLIST_ROOT/phase-<PP>-tasklist.md` token. Both rely on the wrapper's `resolve_path=True` (`commands.py:79`) to absolutize. If the contract's `<ABS_*>` must be a hard absolute (not cwd-relative), add a Step-1 `[VERIFICATION]` resolving the token via `realpath`/`git rev-parse --show-toplevel` — same class as GAP-1's range resolution, no new mechanism.

---

## GAP-5 — Sibling tests assert the wrapper's INTERNAL prompt, not SKILL text

**VERDICT: RESOLVED. CONFIRMED by reading both files: builder MUST NOT touch them; they stay green after SKILL edits.**

- `tests/cli/reflect/test_promote_plumbing.py:30-35` (`test_o2_no_promote_prompt_contains_no_promote`): builds `ReflectRunner(config)._build_prompt()` (the wrapper's INTERNAL `/sc:reflect --mode post … --no-promote` stdin prompt, `runner.py:341-366`) and asserts `--no-promote` is in it. The line:51 reference in the task is inside `test_default_promote_is_on_regression_guard` (lines 38-52), which invokes `reflect_group … --print-command` and asserts the PRINTED prompt contains `/sc:reflect --mode post` and NOT `--no-promote`. Both assert the wrapper engine's own composed prompt/argv — NOT any task-builder or sc-tasklist SKILL string.
- `tests/cli/reflect/test_cli_smoke.py:57-68` (`test_print_command_prints_and_never_launches`, the line:66 reference): asserts `--print-command` output contains `/sc:reflect --mode post` and `claude --print`, via `cli_runner.invoke(reflect_group, …)`. Again the wrapper's own output, not SKILL text.

Neither test reads `task-builder/SKILL.md` or `sc-tasklist-protocol/SKILL.md`. Editing the SKILL gate-emission blocks cannot change `ReflectRunner._build_prompt()` or `_claude_argv_preview()` output. **EXPLICIT: the builder must NOT modify `test_promote_plumbing.py` or `test_cli_smoke.py`. They are decoupled and remain green.**

(Cross-reference: the ONE test that DOES read the task-builder SKILL is `test_no_nesting_guard.py::test_layer_a_wrapper_branch_is_bash_shellout`, lines 49-84 — currently `@pytest.mark.xfail(strict=False)` because the generator-side Mode-2 block is absent on this base. See GAP-6.)

---

## GAP-6 — Robust test anchor for the O1 emission block inside the ```markdown fence

**VERDICT: RESOLVED. Recommend a UNIQUE bold-marker anchor + "next-heading-or-fence-close" slice bound, mirroring the EXISTING `_extract_wrapper_branch` idiom (`text.index(unique_marker)` is fence-agnostic, so `---` rules inside the fence are irrelevant). Do NOT anchor on `#### POST reflect gate (O1` — no such heading exists today.**

### Fence geometry (the O1 emission block lives inside a fenced ```markdown example).

`task-builder/SKILL.md`: the "Output Structure" fenced example opens ` ```markdown ` at **line 2136** and closes ` ``` ` at **line 2219**. Inside it: a YAML frontmatter block (`---` at 2137 and 2156), and section separators (`---` at 2175, 2189, 2207). The O1 reflect item is the bullet `- [ ] **N.{X-1} -- Independent post-execution reflection gate (run via subagent)**` at **lines 2193-2198**, immediately followed by `- [ ] **N.X — Update task status to Done**` (lines 2200-2205) and the closing fence at 2219. NOTE: today this item emits the `/sc:reflect …` form (line 2195), NOT `superclaude reflect run` — the builder edit will swap it to the wrapper shell-out form. The proposed `#### POST reflect gate (O1…` heading does NOT exist in the SKILL today (grep confirms zero hits); it is a NET-NEW anchor the builder would introduce.

### The existing, proven extractor idiom (use this shape).

`tests/cli/reflect/test_no_nesting_guard.py:49-60` `_extract_wrapper_branch`:
```
marker = "**Mode `2` / `auto-resolved-2` (§6.3, DEFAULT) — wrapper shell-out, remediate:**"
start = text.index(marker)
end = text.index("**Mode `halt`", start)
return text[start:end]
```
This is **fence-agnostic by construction**: `str.index` matches a unique literal substring regardless of any ` ``` ` fences or `---` lines around it. So "the `---` rules inside the fence" pose NO problem for a substring-anchored slicer — they only break parsers that treat `---` as a structural delimiter, which this does not.

### Recommended anchor + slice bound for the O1 block.

Two robust options, in order of preference:

1. **Anchor on the unique bold item heading; bound at the next `- [ ] **` bullet.** Start at the literal `- [ ] **N.{X-1} -- Independent post-execution reflection gate` (or, post-edit, the new bold marker the builder writes, e.g. `**POST reflect gate (O1) — wrapper shell-out:**`), end at the next `- [ ] **N.X` ("Update task status to Done") bullet or, failing that, the closing fence. Concretely:
   ```
   start = text.index("**N.{X-1} -- Independent post-execution reflection gate")
   end   = text.index("- [ ] **N.X", start)   # next checklist item; or text.index("\n```", start)
   block = text[start:end]
   ```
2. **If the builder adds a `#### POST reflect gate (O1` heading INSIDE or just before the fence:** start at that exact heading literal and end at the NEXT `#### ` heading at the same level, OR the closing ` ``` ` fence, whichever comes first:
   ```
   start = text.index("#### POST reflect gate (O1")
   end_candidates = [i for i in (text.find("\n#### ", start+1), text.find("\n```", start+1)) if i != -1]
   end = min(end_candidates)
   block = text[start:end]
   ```

Either is unambiguous because the anchor is a UNIQUE literal substring and the bound is the next sibling delimiter. Avoid bounding on bare `---` (ambiguous: 5 such lines inside the fence at 2137/2156/2175/2189/2207). Avoid bounding on the closing fence ALONE if a second fenced block could follow. The next-`- [ ] **`-bullet bound (option 1) is the tightest and the most robust given the current geometry.

**Cited fence range:** ` ```markdown ` opens at `task-builder/SKILL.md:2136`, closes at `:2219`; O1 item at `:2193-2198`; trailing `- [ ] **N.X` item at `:2200`.

---

## Per-Gap Summary

1. **GAP-1 (O2 --base resolution): RESOLVED** — No Sprint-CLI substitution exists (grep `cli/sprint/` clean). The existing per-phase reflect task resolves its range via an in-task `[VERIFICATION]` STEP run by the executing agent (`SKILL.md:1067`), NOT mechanical substitution. Contract §2/§6 mandate emitting explicit `--base <PHASE_N_START_SHA>` (resolved by an analogous `[VERIFICATION]` step) OR a per-phase frontmatter `start_commit` (engine precedence `config.py:81-105`). Emit the placeholder + resolution step; never a generation-time SHA.
2. **GAP-2 (reflect_post writeback): RESOLVED → Option 2A.** `runner.py:147-148` proves the wrapper does NOT create frontmatter (returns `"frontmatter-missing"`); a clean PASS then flips to BLOCKED/exit-2 (`runner.py:588-590`) → false-FAIL on every frontmatter-less phase. Phase files have none today (struct check #5, `SKILL.md:1128`). MUST pre-seed minimal frontmatter (`executor_model_class`, optional `start_commit`, room for `reflect_post`) AND amend struct check #5 to allow frontmatter-before-`# Phase N`. 2B/2C rejected on evidence.
3. **GAP-3 (--output): RESOLVED** — default `<phase-dir>/reflect/post/<sha>/` (`config.py:211-213`) does NOT match the declared `validation/reflect-post/phase-<PP>/` path or its Acceptance Criterion (`SKILL.md:1060,1072`). ADD `--output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/` to the O2 line (matches legacy `SKILL.md:1063`).
4. **GAP-4 (absolute path): RESOLVED** — wrapper absolutizes its positional arg via `resolve_path=True` (`commands.py:79`) + `.resolve()` (`config.py:165`). O1 emits its existing `{TASK_FILE}` token; O2 emits its existing literal `TASKLIST_ROOT/phase-<PP>-tasklist.md` prefix (`SKILL.md:1063`). For a hard-abspath guarantee, add a Step-1 `[VERIFICATION]` resolving via `git rev-parse --show-toplevel`/`realpath` — same class as GAP-1, no new mechanism.
5. **GAP-5 (sibling tests): RESOLVED/CONFIRMED** — `test_promote_plumbing.py:30-52` and `test_cli_smoke.py:57-68` assert the wrapper's INTERNAL `_build_prompt()`/`--print-command` output, NOT SKILL text. Builder MUST NOT touch them; they stay green after SKILL edits.
6. **GAP-6 (test anchor in fence): RESOLVED** — Use a UNIQUE bold/heading literal anchor + next-sibling-delimiter bound, mirroring the proven `_extract_wrapper_branch` `text.index()` idiom (`test_no_nesting_guard.py:49-60`), which is fence-agnostic so the 5 `---` lines inside the ```markdown fence (`SKILL.md:2136-2219`) are irrelevant. Prefer: start at `**N.{X-1} -- Independent post-execution reflection gate` (or the new wrapper-form bold marker), end at the next `- [ ] **N.X` bullet. Do NOT anchor on `#### POST reflect gate (O1` unless the builder first introduces that heading (none exists today).

**Status: Complete**
