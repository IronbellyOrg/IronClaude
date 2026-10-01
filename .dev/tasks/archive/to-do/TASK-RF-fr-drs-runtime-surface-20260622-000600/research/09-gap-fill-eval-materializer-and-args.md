# Research: Gap-Fill Round 1 — Eval Materializer + run_sweep Arg Construction

**Status:** Complete
**Date:** 2026-06-22
**Round:** Gap-fill round 1 (targeted; resolves the 5 gaps flagged by the research quality gate)

**Summary (5 gaps resolved):**
- **GAP 1 (CRITICAL):** The `evals.json → eval_metadata.json` materializer EXISTS on disk (untracked) — `scaffold_iteration.py` (flatten/scaffold; `eval_metadata.json` write :65) + `produce_iteration.py` (`materialize()` :87, `shutil.copy2` contract alias :172, `eval_metadata.json` write :216). Phase 3 = PROMOTE/ADAPT into tracked `.dev/eval-workspaces/sc-reflect/` + insert `run_sweep` upstream of `grader.py`; no new assertion type (reuse `check_yaml_field` grader.py:174 / `check_yaml_list_len_eq` :191); C-6 `target`-key constraint already satisfied.
- **GAP 2 (IMPORTANT):** `ReflectConfig` has NO `availability_surface`/Wave-0 probe (models.py:57-98, config.py:123-256). v1 decision: pass `availability_surface={}` (force-floor) + `lsp=None` → deterministic floor-only sweep (D3/R4: rg/AST floor is ground truth, LSP optional).
- **GAP 3 (IMPORTANT):** No `diff`-text / `scope_worktree` field on config; no diff computed in `_audit_once` (runner.py:394-453 forwards single-ref `--diff config.base`, runner.py:356). Decided construction: `diff = git diff <config.base>` (de-ranged), `scope_worktree = git toplevel of config.tasklist_path.parent` (git_cwd precedent config.py:185). All 6 args mapped.
- **GAP 4 (IMPORTANT):** OQ-DRS.1/.2/.3 + Q4 release-ratification block (tdd.md:1416, §22 recommendations :1321-1324, ratify-at-implementation) + per-phase exit criteria quoted (Phase1 :1361, Phase2 :1374, Phase3 :1384, Phase4 :1393).
- **GAP 5 (MINOR):** NFR-003 no-network-I/O verification item; ensemble.py line re-anchor — `REFLECT_CONTRACT_VERSION` decl ensemble.py:59, usage CURRENTLY at **ensemble.py:502** (prior :378/:500/:501 drifted); materializer remediation = 2 atomic Phase-3 items (a: promote/adapt scaffold, b: insert run_sweep upstream of grading).

**In-place corrections made:** research/01 line 139 — appended `[CODE-CONTRADICTED]` note (only base_ref/tasklist/output_dir are config fields; diff/scope_worktree/availability_surface are constructed). research/04 frontmatter — `Status: In Progress` → `Status: Complete`.
**Evidence tags:** `[CODE-VERIFIED]` = file opened + line re-read this session (2026-06-22); `[CODE-CONTRADICTED]` = source refutes a prior research claim; `[UNVERIFIED]` = inference, no direct source.

---

## GAP 1 (CRITICAL) — The eval materializer EXISTS on disk; Phase 3 is PROMOTE/ADAPT, not build-from-scratch

**Headline correction** `[CODE-CONTRADICTED]`: R5's research file 05 concluded the `evals.json → eval_metadata.json` materializer is "not located / must build from scratch." That is **FALSE**. Two scripts on disk already perform the full flatten + materialize + contract-copy pipeline. They are **untracked** (`git status` shows `??` on the parent dir — verified: `?? .dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/phase-outputs/plans/`), so "not git-tracked" is true while "must build from scratch" is **false**. The corrected Phase-3 recommendation is **PROMOTE/ADAPT**, not author-anew.

### Script A — `scaffold_iteration.py` (the flatten + scaffold half)

Path: `.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/phase-outputs/plans/scaffold_iteration.py`

What it does `[CODE-VERIFIED]`:
- Reads the registry `evals/evals.json` (`REGISTRY = WORKSPACE / "evals" / "evals.json"`, scaffold_iteration.py:31; loaded scaffold_iteration.py:39; indexed by id at :40).
- For each requested eval id, creates the per-case scaffold dirs: `with_skill/outputs/artifacts/` (scaffold_iteration.py:54) and `old_skill/outputs/artifacts/` (:55) — confirms the `with_skill/outputs/artifacts/` dir construction the gap asked about.
- Writes `eval_metadata.json` per case with `{eval_id, eval_name, case_dir, mode, use_case, assertions}` — the assertions are copied verbatim from the registry entry (`metadata` dict built scaffold_iteration.py:57-64; **written at scaffold_iteration.py:65** — exactly the cited line).
- Partitions assertion `target`s into `with_skill/` vs `old_skill/` drop targets (scaffold_iteration.py:69-74) and prints what the producer must fill.

Reuse role: this is the **flatten/scaffold** half (registry → flat per-case dirs + `eval_metadata.json` the grader consumes). For FR-DRS it ports directly — its only coupling to UC-2 is `DEFAULT_IDS` (scaffold_iteration.py:32) and the hardcoded `WORKSPACE` path (:28-30), both trivially re-pointed.

### Script B — `produce_iteration.py` (the materialize + run + contract-copy half)

Path: `.dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/phase-outputs/plans/produce_iteration.py`

What it does `[CODE-VERIFIED]`:
- **`materialize()`** — reconstructs the post-image of every file in the case `input/diff.patch` and writes it into a scratch `fixture/` tree so the reflect reachability sweep has real symbols to walk (**def at produce_iteration.py:87**; body :94-104; patch read :96; post-image written :99-103). This is the exact function cited at :87.
- **return-contract.yaml → contract.yaml copy** — `alias_contract()` copies `return-contract.yaml` to `contract.yaml` (the filename the grader assertions target) via **`shutil.copy2(rc, cy)` at produce_iteration.py:172** (guarded by `if rc.exists() and not cy.exists()`, :171). `shutil` imported produce_iteration.py:29. This is the cited :172 copy. (`alias_contract` is invoked after the run at produce_iteration.py:243.)
- **eval_metadata.json write** — writes `{eval_id, eval_name, case_dir, mode, use_case, assertions}` (assertions copied verbatim from the registry) at **produce_iteration.py:216** (dict :217-224). Exactly the cited :216 write.
- Also builds `with_skill/outputs/` (produce_iteration.py:207-208), `old_skill/outputs/` (:211), and invokes `grader.py` over the iteration dir when `--grade` (:261-263).
- Default mode is DRY-RUN (materializes + prints the `claude` commands it WOULD run); `--run` actually invokes claude (produce_iteration.py:18-19, :237-244).

### Corrected Phase-3 recommendation for the FR-DRS eval-wire

`[CODE-VERIFIED for the seam facts; recommendation is the builder-decided synthesis]`

The FR-DRS eval-wire (Phase 3) **PROMOTES/ADAPTS** these existing scripts rather than authoring from scratch:

1. **Promote to a tracked home.** Both scripts currently live under an untracked task `phase-outputs/plans/` dir. The tracked home is **`.dev/eval-workspaces/sc-reflect/`** — alongside `grader.py` (verified present: `.dev/eval-workspaces/sc-reflect/grader.py`, 22039 bytes) and its siblings `aggregate_iteration.py`, `evals/`, `cases/`, `iterations/`, `SPEC.md`. The scripts already hardcode `WORKSPACE`/`WS` to this exact directory (scaffold_iteration.py:28-30; produce_iteration.py:34-36), so moving them there makes those constants self-consistent. `[CODE-VERIFIED]`
2. **Insert the `run_sweep` oracle call** so the six contract fields are **deterministically materialized upstream of grading.** Today `produce_iteration.py` relies on the (LLM) reflect run to emit `return-contract.yaml`, then aliases it to `contract.yaml` (:168-172). For FR-DRS the deterministic half must call `run_sweep(...)` and merge-overwrite the six `runtime_surface_*` keys into `contract.yaml` **before** `grader.py` reads it — making the sweep's outputs ground truth independent of any LLM step (consistent with the §8 "scalars merge-overwrite the six keys before any consumer parses" wiring).
3. **No new assertion type needed.** The grader already ships `check_yaml_field` (grader.py:174, reads `assertion["target"]` + `yaml.safe_load`) and `check_yaml_list_len_eq` (grader.py:191, same shape). Pointing these existing assertions at the deterministically-written `contract.yaml` requires **zero** new assertion machinery. `[CODE-VERIFIED]`
4. **C-6 constraint still applies.** Every grader assertion dereferences `assertion["target"]` (grader.py:154, :164, :174, :192, :276, :321) — so any new oracle assertion the FR-DRS evals add **MUST carry a `target` key** or the grader raises/misses. The reused `yaml_field`/`yaml_list_len_eq` assertions against `contract.yaml` already satisfy this (their `target` is `with_skill/outputs/contract.yaml`). `[CODE-VERIFIED]`

**Net:** Phase 3 = (a) `git mv`/copy the two scripts into `.dev/eval-workspaces/sc-reflect/` (tracked), re-point `DEFAULT_IDS`/`--cases` to the FR-DRS eval ids; (b) insert the `run_sweep` call + six-field merge-overwrite upstream of `grader.py`. NOT a from-scratch authoring task.

---

## GAP 2 (IMPORTANT) — `availability_surface` source for the runner-driven path: force-the-floor (v1)

**TDD claim refuted** `[CODE-CONTRADICTED]`: TDD §8.1.2 says `run_sweep` takes `availability_surface: dict` "from the Wave-0 availability probe already on the config." There is **no such field on `ReflectConfig` and no Wave-0 probe in the Python runner.**

Evidence `[CODE-VERIFIED]`:
- `ReflectConfig` (models.py:57-98) fields are exactly: `tasklist_path, base, head, spec_path, depth, executor_model, output_dir, model, timeout_seconds, max_turns, promote, allow_single_vendor, tmux, dry_run, print_command, resume, base_override, fix, max_fix_iterations, transport, reviewers` (+ the `contract_path`/`is_promotable` properties). **No `availability_surface`, no `availability`, no `surface`, no Wave-0 probe field.**
- `resolve_config` (config.py:123-256) constructs `ReflectConfig` from CLI args + frontmatter + git state only (the full kwarg set, config.py:234-256). It runs **no** tool-availability probe (no `rg`/`pyright`/LSP detection); the only subprocess calls are `git merge-base`/`rev-parse` (config.py:103, :190 via `_git`).
- The Wave-0 §0.5d availability surface is derived **inside the LLM skill** (the `/sc:reflect` slash-command prompt), not in the Python runner — the runner only forwards `--diff/--tasklist/--spec/--depth/--output` to the skill (`_build_prompt`, runner.py:343-368). Nothing parses or stores a returned availability surface.

**v1 decision the builder must encode — FORCE THE FLOOR:**
The runner-driven path passes a **floor-forcing value** for `availability_surface` so `run_sweep` DEGRADEs-to-floor deterministically. Recommended concrete form: an **empty dict `{}`** (or, equivalently, an explicit `"all-degraded-to-floor"` sentinel) AND `lsp=None`. Rationale:
- The sweep must be **deterministic regardless of tool availability** (AC-2: zero variance across ≥3 runs). Absent a probe, force the floor so the result never depends on whether an LSP server happens to be installed in the runtime environment.
- This is consistent with **D3/R4: the `rg`/AST floor is ground truth; LSP is an optional precision overlay.** With `availability_surface={}` and `lsp=None`, `run_sweep` runs the floor-only path → the same UNREACHED/DEGRADE verdicts every run.
- `run_sweep`'s signature already accepts this: per research file 01 (lines 124-126) the signature is `run_sweep(..., availability_surface: dict, ..., lsp: LspOverlay | None = None)` — an empty dict for `availability_surface` and `None` for `lsp` are both valid inputs that select the floor path. `[UNVERIFIED — run_sweep is the module to be built (confirmed: `def run_sweep` exists NOWHERE in src/), so this is a signature-contract decision for the builder, not yet code]`

**Builder item:** the runner-side arg-construction site passes `availability_surface={}` (force-floor) + `lsp=None` until/unless a real Wave-0 probe is added to `ReflectConfig` in a future increment. Add a code comment anchoring this v1 decision to D3/R4 so a later reader does not mistake the empty dict for a bug.

---

## GAP 3 (IMPORTANT) — `diff` + `scope_worktree` construction (completes R2's half-resolved finding)

**Reconfirmed from source** `[CODE-VERIFIED]`: `ReflectConfig` has **no diff-text field** and **no `scope_worktree` field**. The config-resident inputs relevant to `run_sweep` are only `base` (a single ref string, models.py:68), `tasklist_path` (Path, :66), and `output_dir` (Path, :73). There is no `diff`, `diff_text`, `scope`, `scope_worktree`, `worktree`, or `repo_root` field (full field list re-read at models.py:57-98).

**No existing diff-text computation in the runner to reuse** `[CODE-VERIFIED]`: `_audit_once` (runner.py:394-453) does **not** compute a git diff. It calls `_build_prompt()` (runner.py:431, :486) which simply forwards `config.base` as a single ref to the slash command — `parts += ["--diff", config.base]` (runner.py:356). The comment there (runner.py:350-355) makes explicit that `--diff <BASE>` is a *single ref handed to the reflect skill so the skill diffs it against the working tree* — the Python runner never materializes diff text. So for the runner-driven `run_sweep` path there is **nothing to reuse**; the diff hunks must be computed fresh.

**Builder-decided construction for the runner path:**

- **`diff`** — compute fresh via `git diff <config.base>` (working-tree diff against the single base ref), matching the semantics the reflect skill already uses for `--diff config.base` (runner.py:350-356: single-ref diff vs working tree captures uncommitted/staged `/task` work; a commit *range* would miss it, ref #153). Run it with the same `_git`-style subprocess shape already in `config.py` (`_git(cwd, "diff", config.base)`, config.py:64-78) so error handling stays uniform. **Do NOT** pass `config.base..HEAD` (F3 de-range invariant, config.py:97-98 / `_resolve_base` docstring). `[CODE-VERIFIED for the seam + de-range rule; the `git diff` call itself is new code]`
- **`scope_worktree`** — the repo/worktree root. Recommended source: derive from `config.output_dir`'s enclosing git repo root, or equivalently `config.tasklist_path.parent` resolved to the git toplevel (the same `git_cwd` that `resolve_config` already uses, config.py:185 — `git_cwd = resolved_tasklist.parent`, then `git -C` discovers the repo root). Cleanest concrete form: `Path(_git(git_cwd, "rev-parse", "--show-toplevel"))`. `Path.cwd()` is an acceptable fallback but is less robust under worktrees, so prefer the git-toplevel derivation. `[UNVERIFIED — construction decision; `_git rev-parse --show-toplevel` is a standard call, the `git_cwd` precedent is CODE-VERIFIED at config.py:185]`

**Concrete decided construction for all 6 `run_sweep` args (runner-driven path):**

| `run_sweep` arg | Source | Status |
|---|---|---|
| `base_ref` | `config.base` (single ref; models.py:68) | clean — config field `[CODE-VERIFIED]` |
| `tasklist` | `config.tasklist_path` (models.py:66) | clean — config field `[CODE-VERIFIED]` |
| `output_dir` | `config.output_dir` (models.py:73; backs `contract_path`, models.py:96) | clean — config field `[CODE-VERIFIED]` |
| `diff` | `git diff <config.base>` (working-tree diff vs single base ref) | construct — `_git(git_cwd, "diff", config.base)` |
| `scope_worktree` | git toplevel of `git_cwd` (`_git(git_cwd, "rev-parse", "--show-toplevel")`); `git_cwd = config.tasklist_path.parent` | construct |
| `availability_surface` | `{}` (force-floor, GAP 2) + `lsp=None` | construct — v1 force-floor |

This gives the builder a fully-decided arg-construction recipe for the `_audit_once` seam (runner.py:394-453): three args map straight to config fields; three are constructed with the subprocess + force-floor decisions above.

---

## GAP 4 (IMPORTANT) — OQ-ratification block + per-phase exit-criteria mapping

TDD source: `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md` (all line cites below `[CODE-VERIFIED]` against that file).

### 4a. Open-Questions block the generated tasklist MUST carry (ratify-at-implementation)

§24.2:1416 makes **"OQ-DRS.1/.2/.3 + Q4 ratified (recommendation accepted or amended) and recorded"** a RELEASE criterion (tdd.md:1416). §22 posture (tdd.md:1317) is explicit: these are *spec-level, recommendation-recorded, ratification-at-implementation* — no user decision blocks PROCEED, but the tasklist must carry an OQ block and the release gate must record the ratification. Builder-consumable items (recommendations quoted from tdd.md §22 table, lines 1321-1324):

- **OQ-DRS.1 — Referrer engine.** Recommended resolution: **ripgrep/AST as the determinism-safe floor; LSP/Serena as an OPTIONAL precision overlay that DEGRADEs-to-floor on any unavailability signal** (tdd.md:1321; reinforced §6.4 D3 tdd.md:462, §18.1 tdd.md:881/1143). Mark *ratify-at-implementation*.
- **OQ-DRS.2 — Invocation site / bare-path coverage.** Recommended resolution: **importable pure-Python module called from `runner._audit_once` for the CLI path, PLUS a Wave-1A skill shell-out to the same module for the bare `claude -p /sc:reflect` path**; `commands.py` rejected (runner clobbers a contract written there) (tdd.md:1322; §6.4 D2 tdd.md:461; R2 tdd.md:1223). The tasklist must state explicitly which paths get deterministic fields vs remain LLM-emitted. Mark *ratify-at-implementation*.
- **OQ-DRS.3 — Contract version.** Recommended resolution: **no version bump** — FR-DRS changes the PRODUCER of the six `runtime_surface_*` fields, not the field set; FR-RSR already shipped them as additive `1.6.0`; major stays `"1"` so the consumer gate (`contract.py` checks `major == "1"`) passes unchanged (tdd.md:1323; §19.2 tdd.md:1199). Mark *ratify-at-implementation*.
- **Q4 — Stale ensemble version constant.** Recommended resolution: **reconcile when the ensemble path emits the six fields** (tied to OQ-DRS.3) — bump `REFLECT_CONTRACT_VERSION` (`ensemble.py:59`) to match `1.6.0`, or document the wrapper's version as intentionally independent; not breaking today (consumer gates `major == "1"` only) but an internal inconsistency to resolve (tdd.md:1324; §19.2 tdd.md:1200). Mark *ratify-at-implementation*. (See GAP 5 for the corrected ensemble.py usage line.)

### 4b. Per-phase EXIT CRITERIA (§23.2) — each phase's verify item binds to a concrete gate

Quoted verbatim from tdd.md §23.2 (lines 1361, 1374, 1384, 1393):

- **Phase 1 — Module + tests** (Exit Criteria, tdd.md:1361): *"module importable; `len(unreached_surfaces) == runtime_surface_unreached` holds in tests; floor-only path deterministic across repeated runs; C-5 materializer located (or AC-2 grader-determinism flagged conditional)."*
  → Phase-1 verify item binds to: (i) module imports; (ii) the count invariant `len(unreached_surfaces) == runtime_surface_unreached`; (iii) floor-only determinism across repeated runs; (iv) **materializer LOCATED** — and per GAP 1 it IS located (the two `phase-outputs/plans/` scripts), so this sub-gate resolves GREEN, not "conditional."
- **Phase 2 — Product wire** (Exit Criteria, tdd.md:1374): *"deterministic six fields present on every runner-driven UC-2 run (REACHED/DEGRADE/UNREACHED alike); the §5.3 forbid-STOP pre-filter gates on the DERIVED `surface_unreached` field … so the pre-filter reads `surface_unreached`, never the integer directly (AC-4, in-scope). The `sprint run` executor read is NOT an exit criterion of this phase."*
  → Phase-2 verify item binds to: six fields on every runner-driven UC-2 run + §5.3 forbid-STOP gating on the derived `surface_unreached` (NOT the raw integer). Sprint-executor read is explicitly OUT (deferred FR-006a).
- **Phase 3 — Eval wire** (Exit Criteria, tdd.md:1384): *"AC-2 green with no variance across ≥3 runs."*
  → Phase-3 verify item binds to: AC-2 GREEN, zero variance across ≥3 grader runs.
- **Phase 4 — Prose demotion** (Exit Criteria, tdd.md:1393): *"AC-1 satisfied end-to-end; prose no longer the structured-emission producer where the sweep ran."*
  → Phase-4 verify item binds to: AC-1 end-to-end + the SKILL.md 4b/4b′ demotion (conditional LLM-fallback branch for the bare path) + `make sync-dev`/`make verify-sync` clean (the §23.2 Phase-4 sizing note, tdd.md:1344, and §24.2 release list reference sync/verify-sync).

> Note: tdd.md:1372 also carries a Phase-2 sub-item "(Per OQ-DRS.2) Wave-1A skill shell-out wiring for the bare `claude -p` path" — this is the bare-path coverage the tasklist must either schedule or explicitly defer with the OQ-DRS.2 ratification.

---

## GAP 5 (MINOR) — builder notes

### 5a. NFR-003 — no-network-I/O verification item

Add a Phase-1 (or test-phase) verification item asserting the FR-DRS module performs **no network I/O**: a static check that the module source contains **zero** `socket`, `http`/`urllib`/`requests`, or MCP-client calls. This is the determinism + offline-floor invariant (NFR-001/NFR-003; D3 floor must run regardless of tool availability, tdd.md:462/881). Concrete form: a unit test that `grep`/AST-scans the module's imports + call sites for `socket|urllib|http|requests|httpx|aiohttp` and the MCP client surface, asserting none present (the floor uses only `rg`/AST + filesystem). `[UNVERIFIED — module not yet written; this is a verification-item spec for the builder]`

### 5b. ensemble.py line drift — RE-ANCHORED

`[CODE-VERIFIED]` `REFLECT_CONTRACT_VERSION = "1.0"` is declared at **ensemble.py:59**. The emit usage — `"contract_version": REFLECT_CONTRACT_VERSION,` — is **CURRENTLY at ensemble.py:502** (re-read 2026-06-22). Prior research citing :500/:501/:502 (and the TDD's §19.2 cite of `:378`, tdd.md:1200) are **drifted**. The current, correct usage line is **ensemble.py:502**.

Instruct the builder to **re-anchor at write time**: the line will drift again as `ensemble.py` evolves, so the tasklist's Q4-reconciliation item must `grep -n 'contract_version.*REFLECT_CONTRACT_VERSION' src/superclaude/cli/reflect/ensemble.py` immediately before editing, rather than trusting any baked-in line number. `[CODE-VERIFIED: declaration ensemble.py:59; usage ensemble.py:502 as of 2026-06-22]`

### 5c. Materializer remediation = TWO atomic Phase-3 items (A3 granularity)

Per A3 granularity, the GAP-1 materializer remediation splits into two atomic Phase-3 items:
- **(a) Promote/adapt the flatten+copy scaffold** — `git mv`/copy `scaffold_iteration.py` + `produce_iteration.py` into the tracked home `.dev/eval-workspaces/sc-reflect/`; re-point `DEFAULT_IDS`/`--cases` to the FR-DRS eval ids; verify they still flatten `evals.json` → per-case `eval_metadata.json` + `with_skill/outputs/` and copy `return-contract.yaml` → `contract.yaml` (`shutil.copy2`, produce_iteration.py:172).
- **(b) Insert the `run_sweep` oracle call upstream of grading** — call `run_sweep(...)` and merge-overwrite the six `runtime_surface_*` keys into `contract.yaml` BEFORE `grader.py` reads it, so the eval is deterministic and free of LLM variance (AC-2). Reuse existing `yaml_field`/`yaml_list_len_eq` assertions against the deterministically-written `contract.yaml` — no new assertion type; the `target` key (C-6) is satisfied by `with_skill/outputs/contract.yaml`.
