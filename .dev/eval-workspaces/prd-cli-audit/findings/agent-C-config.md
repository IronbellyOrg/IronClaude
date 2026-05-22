# Agent C — Config, CLI surface, tier propagation

Scope: `src/superclaude/cli/prd/{commands.py,config.py,models.py}` + `prd` registration in `src/superclaude/cli/main.py`. Cross-references to `executor.py`, `gates.py`, `prompts.py`, `process.py`, `inventory.py` noted but not deep-read.

---

### F-C-1: `--tier` reaches `config.tier` but is NEVER consulted at gate construction; `_tier_min_lines` is dead code
**Severity (preliminary)**: CRITICAL
**Pattern tags**: P2, P7
**File:line**: `src/superclaude/cli/prd/gates.py:281-292, 295-505`; `src/superclaude/cli/prd/executor.py:530, 596-607, 685`

**Evidence**:
```python
# gates.py:281
def _tier_min_lines(tier: str) -> int:
    return {"lightweight": 200, "standard": 400, "heavyweight": 600}.get(tier, 400)

# gates.py:359 (build-task-file)
"build-task-file": GateCriteria(
    ...
    min_lines=400,  # default standard tier; callers override per tier
    enforcement_tier="STRICT",

# executor.py:530 (only call site for the table)
gate = GATE_CRITERIA.get(step_id)
# ...
# executor.py:596
if gate.min_lines > 0:
    if line_count < gate.min_lines:
```

**Trace**:
- Writer: `commands.py:53-56` declares `--tier` (Click choice, default "standard"). `commands.py:104-114` passes it into `resolve_config(... tier=tier ...)`. `config.py:84-90, 136` validates and stores into `PrdConfig.tier`. `models.py:185` defines the field.
- Reader chain in `executor.py`: `config.tier` is read at `executor.py:717-720, 735-738` to set step counts for investigation/web-research — that wiring works.
- **Chain break**: `gates.py:_tier_min_lines` and `_tier_min_lines_assembly` are defined but `grep -r "_tier_min_lines"` returns only the definition lines. No call site anywhere. The comment "callers override per tier" at `gates.py:367, 459` is aspirational. `GATE_CRITERIA` is a module-level constant frozen at import time at the standard-tier baseline; `executor.py:530, 685` looks the gate up via `.get(step_id)` and consumes `gate.min_lines` directly without ever passing `config.tier` through a transform.

Result: `--tier lightweight` still demands ≥400 lines on build-task-file and ≥800 on assembly (heavyweight users would lose the higher bound). The knob is wired *to* `config.tier` but unwired *from* the gate decision. This is the upstream cause of Bug 3 — the value `lightweight` arrived correctly; the consumer simply never asked for it. Reclassifies Bug 3 from "knob unwired in argparse" to **"knob fully wired through config but ignored by GateCriteria construction"**.

**Reproduction sketch**: `superclaude prd run "tiny feature" --tier lightweight --dry-run` shows `Tier: lightweight`. A real run halts at build-task-file with "Min lines: <400" against `min_lines=400` even though the lightweight contract is 200.

**Confidence (own)**: 0.97 — Verified by `grep` across `src/`; the helper functions have zero call sites. The `# callers override per tier` comment in two places is unambiguous evidence the override path was intended and not built.

---

### F-C-2: `--where` flag is stored on `PrdConfig` and never read by any consumer
**Severity (preliminary)**: HIGH
**Pattern tags**: P2
**File:line**: `commands.py:41-45, 82, 107`; `config.py:50, 64, 134`; `models.py:182`; `prompts.py:54-101`

**Evidence**:
```python
# commands.py:41
@click.option("--where", "-w", multiple=True, help="Source directories to focus on (repeatable).")
# ...
where=where if where else None,
# config.py:134
where=list(where) if where else [],
# models.py:182
where: list[str] = field(default_factory=list)
```
And `grep -rn "config\.where\|cfg\.where\|self\._config\.where" src/` returns no hits.

**Trace**:
- Writer: argparse → `resolve_config(where=...)` → `PrdConfig.where`.
- Reader: none. The parse-request prompt (`prompts.py:54-101`) asks the LLM to extract `WHERE` from the natural-language `user_message` itself, and scope-discovery (`prompts.py:104-122`) then reads `parsed-request.json["WHERE"]`. The CLI-provided `--where` list is never injected into the parse-request prompt nor written into `parsed-request.json` as a seed.

**Reproduction sketch**: `superclaude prd run "Add search" --where src/api --where src/search`. The two paths are silently dropped; if the user's NL string doesn't also name them, scope discovery roams the whole repo. The `--help` text and the docstring example at `commands.py:25` actively misrepresent the behavior.

**Confidence (own)**: 0.95 — Negative result from grep is conclusive within `src/`. Could only be wrong if a consumer accesses `where` via getattr/string lookup, which I did not find.

---

### F-C-3: `prd resume` subcommand drops `--tier`, `--product`, `--output`, `--where`; the documented resume command will fail or silently lie
**Severity (preliminary)**: HIGH
**Pattern tags**: P2, P5, P7
**File:line**: `commands.py:135-191`; `models.py:260-271`

**Evidence**:
```python
# commands.py:153
def resume(step_id: str, max_turns: int, model: str, debug: bool) -> None:
    ...
    config = resolve_config(
        request="",
        max_turns=max_turns,
        model=model,
        debug=debug,
        resume_from=step_id,
    )

# models.py:260
def resume_command(self) -> str:
    parts = ["superclaude", "prd", "resume", self.halt_step]
    if self.config.product_name:
        parts.extend(["--product", self.config.product_name])
    if self.config.model:
        parts.extend(["--model", self.config.model])
    if self.config.tier != "standard":
        parts.extend(["--tier", self.config.tier])
    return " ".join(parts)
```

**Trace**:
- `PrdPipelineResult.resume_command()` *emits* `--product` and `--tier` for the user to copy-paste.
- `prd resume` only declares `--max-turns`, `--model`, `--debug`. Click will reject unknown options with `Error: No such option: --product`. Even if it didn't, `resolve_config(... resume_from=...)` is called with `product=None`, `output=None`, `tier=None`, `where=None` — so on resume `task_dir` is recomputed to `<sandbox>/prd-task` (no slug), `tier` defaults to `"standard"`, and any non-default knob from the original run is lost. P5 path-resolution: the original `task_dir` from the halted run cannot be reattached because there is no `--task-dir`/`--product` to reconstruct the slug.

**Reproduction sketch**: Any `prd run --product foo --tier heavyweight` that halts mid-pipeline writes a `resume_command` of `superclaude prd resume <step> --product foo --tier heavyweight`. Running that verbatim crashes with `Error: No such option: --product`. Stripping the unknown options runs but in a fresh `prd-task/` directory at standard tier, so no prior artifacts are loaded.

**Confidence (own)**: 0.98 — argparse/Click surface in `commands.py:137-152` is exhaustive; the resume entrypoint flatly omits the flags `resume_command` advertises.

---

### F-C-4: `output_path` is a file vs directory pun — CLI treats `--output` as a directory; prompts present it to the LLM as the final file
**Severity (preliminary)**: HIGH
**Pattern tags**: P5, P7
**File:line**: `config.py:102-117, 125`; `models.py:184`; `prompts.py:919, 1093, 986, 1042`

**Evidence**:
```python
# config.py:103
if output:
    output_path = Path(output).resolve()
else:
    sandbox = Path(".dev/eval-workspaces").resolve()
    if sandbox.parent.is_dir():
        sandbox.mkdir(parents=True, exist_ok=True)
        output_path = sandbox          # ← always a directory
    else:
        output_path = Path(".").resolve()
# ...
task_dir = output_path / task_dir_name  # ← treats as parent dir, will mkdir under it

# prompts.py:919
Output path: {config.output_path}      # ← presented to LLM as if it were a file
# prompts.py:1093
Final PRD: {config.output_path}
```
CLI help (`commands.py:50`): `"Output path for final PRD (default: current directory)."` — ambiguous; "current directory" implies dir, "for final PRD" implies file.

**Trace**:
- Writer: `--output` → `Path(output).resolve()` with no isfile/isdir check. Default branch hard-codes `.dev/eval-workspaces/` (a directory).
- Reader A (`config.py:125`): `task_dir = output_path / task_dir_name` — treats it as a directory parent.
- Reader B (`prompts.py:919, 986, 1042, 1093`): renders it into prompts as a single path the LLM is told to "Write to" or "Report path".
- Chain break: If a user passes `--output ./out.md`, the executor will `mkdir -p ./out.md/prd-<slug>/...`, masking the user's filename. If they pass `--output ./outdir/`, the LLM sees a directory path where the prompt says "Final PRD:", and may or may not append a filename.

**Reproduction sketch**: `superclaude prd run "x" --output prd.md --product foo --dry-run` prints `Output: /…/prd.md`. A non-dry run would `mkdir prd.md/prd-foo/...` — a directory named `prd.md`. The "Final PRD:" line in the completion prompt then reads as a directory.

**Confidence (own)**: 0.9 — Code paths are unambiguous; "what the LLM does with it" depends on prompt content I only spot-read. The pun itself (writer treats as dir, prompt label treats as file) is fully evidenced.

---

### F-C-5: `product_slug = ""` when `--product` omitted produces malformed artifact paths and frontmatter IDs
**Severity (preliminary)**: HIGH
**Pattern tags**: P5, P7
**File:line**: `config.py:120-125`; `prompts.py:381, 384, 405, 464`

**Evidence**:
```python
# config.py:120
product_name = product or ""
product_slug = _slugify(product_name) if product_name else ""
task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"
task_dir = output_path / task_dir_name

# prompts.py:381 (build-task-file prompt; concatenation, not f-string interpolation guard)
Write the task file to: {config.task_dir / ("TASK-PRD-" + config.product_slug + ".md")}
- id: TASK-PRD-{config.product_slug}
```

**Trace**:
- Writer: `_slugify` is gated on `product_name` truthiness; no fallback derives a slug from `request`, repo name, or timestamp.
- Reader: `prompts.py:381` interpolates `product_slug` into the literal Write path. When the slug is empty, the LLM is told to "Write the task file to: …/prd-task/TASK-PRD-.md" and "id: TASK-PRD-". `prompts.py:405, 464` later glob `config.task_dir.glob("TASK-PRD-*.md")` and pick `task_files[0]` — works by accident even with empty slug, but the canonical filename `TASK-PRD-{slug}.md` becomes `TASK-PRD-.md`, and the MDTM `id` frontmatter field becomes `TASK-PRD-` (an invalid identifier).
- Chain break with Bug 2: a static `_STEP_ARTIFACT_FILES["build-task-file"] = "TASK-PRD-{slug}.md"` cannot be expressed because the dict carries plain strings, not patterns; and `_resolve_step_content` uses `base_name = Path(artifact_name).name` then `root.rglob(base_name)` — there's no glob/format substitution. Adding the entry needs both slug interpolation at lookup time *or* a pattern-mode in `_resolve_step_content`. (P3.)

**Reproduction sketch**: `superclaude prd run "Build auth" --tier lightweight` (no `--product`). Generated path: `…/prd-task/TASK-PRD-.md`. Frontmatter id `TASK-PRD-`. Downstream gate matching depends on whether the consumer normalizes; the brittleness is the finding.

**Confidence (own)**: 0.93 — All four interpolation sites in prompts.py confirm slug is concatenated as-is. The `_STEP_ARTIFACT_FILES` shape (str → str) is read-only confirmed for Agent A's slice.

---

### F-C-6: `--product`-derived `product_slug` competes with LLM-emitted `PRODUCT_SLUG` from parse-request; no reconciliation
**Severity (preliminary)**: MEDIUM
**Pattern tags**: P2, P7
**File:line**: `config.py:120-125`; `prompts.py:65-101`

**Evidence**:
```python
# prompts.py:73 (parse-request prompt asks the LLM to emit its own slug)
{
  "PRODUCT_NAME": "...",
  "PRODUCT_SLUG": "<kebab-case identifier>",
  ...
}
```
But `config.product_slug` was already computed at CLI time and is what `task_dir` was built from, what build-task-file's `Write to: …` instruction interpolates, and what `inventory.py:46-84` matches against.

**Trace**:
- Writer A: CLI `--product` → `_slugify` → `config.product_slug` → `task_dir` name → build-task-file Write target.
- Writer B: parse-request LLM step writes `parsed-request.json` containing `PRODUCT_SLUG`. `parsed-request.json` is read by scope-discovery (`prompts.py:110`) and likely other downstream steps.
- No reconciler. If they diverge (user passes `--product "User Auth"` → slug `user-auth`; LLM emits `auth` or `userauth`), some prompts cite the CLI slug, others cite the parsed slug, downstream gates/inventory rely on whichever the consumer happens to read.

**Reproduction sketch**: `superclaude prd run "Build auth for v2" --product "User Auth Module"`. Inspect `parsed-request.json` after step 2 — observe `PRODUCT_SLUG` value vs `config.product_slug = "user-auth-module"`.

**Confidence (own)**: 0.8 — Divergence path is real; impact depends on downstream readers I did not exhaustively trace (Agent A/B may have additional ground truth).

---

### F-C-7: `--max-turns` reaches subprocesses correctly; flag is wired end-to-end
**Severity (preliminary)**: LOW (positive-result finding)
**Pattern tags**: (none — clean)
**File:line**: `commands.py:58-63`; `config.py:139`; `models.py:189`; `executor.py:333`; `process.py:155`

**Evidence**:
```python
# commands.py
@click.option("--max-turns", type=int, default=300, ...)
# config.py:139
max_turns=max_turns or 300,
# executor.py:333
self._ledger = TurnLedger(total_budget=config.max_turns)
# process.py:155
max_turns=config.max_turns,
```

**Trace**: clean argparse → resolve_config → PrdConfig → TurnLedger + subprocess `max_turns=`. No silent default override on the consumer side. The `or 300` in resolve_config is redundant given Click's default, but harmless.

**Confidence (own)**: 0.95 — Single consumer chain, all explicit.

---

### F-C-8: `--tier` default duplicated in Click and `resolve_config` — two sources of truth for the same default
**Severity (preliminary)**: LOW
**Pattern tags**: P7
**File:line**: `commands.py:55` (`default="standard"`); `config.py:85` (`(tier or "standard").lower()`)

**Evidence**: Click defaults to `"standard"`, so `tier` is never `None` when called from CLI; `config.py:85`'s `tier or "standard"` only fires when `resolve_config` is invoked programmatically (e.g. from tests). Two defaults that could drift independently.

**Trace**: Writer A = Click. Writer B = resolve_config default. Both currently `"standard"`. If one is changed without the other, programmatic callers vs CLI callers get different defaults silently.

**Confidence (own)**: 0.9 — Pattern is real but consequence is latent.

---

### F-C-9: `output_path` default resolves `.dev/eval-workspaces` at CWD without verifying it's the project root
**Severity (preliminary)**: MEDIUM
**Pattern tags**: P5, P7
**File:line**: `config.py:108-117`

**Evidence**:
```python
sandbox = Path(".dev/eval-workspaces").resolve()
if sandbox.parent.is_dir():            # i.e. .dev/ exists as a dir
    sandbox.mkdir(parents=True, exist_ok=True)
    output_path = sandbox
```

**Trace**: The CWD-relative `.dev/eval-workspaces` triggers whenever any `.dev/` directory exists in CWD. If the user is in a subdirectory or an unrelated project that happens to have a `.dev/` (the convention is not unique to this repo), the PRD pipeline writes outside what the user expected and never asked permission. Compounded by F-C-4: this is *only* a directory branch — never a file. So callers who passed `-o report.md` and callers who passed nothing end up with very different `output_path` shapes.

**Reproduction sketch**: From any CWD containing a `.dev/` directory: `superclaude prd run "x"` silently creates `<cwd>/.dev/eval-workspaces/prd-task/`. No `--output` advisory in the dry-run output (commands.py:123 just echoes the resolved path).

**Confidence (own)**: 0.85 — Behavior is verified; severity depends on house convention.

---

### F-C-10: `resume_from` validation regex hard-codes step ID alphabet — adding a new step requires editing config.py
**Severity (preliminary)**: LOW
**Pattern tags**: P1
**File:line**: `config.py:26-33`

**Evidence**:
```python
_STEP_ID_PATTERN = re.compile(
    r"^(check-existing|parse-request|scope-discovery|research-notes"
    r"|sufficiency-review|template-triage|build-task-file|verify-task-file"
    r"|preparation|investigation-\d+|web-research-\d+"
    r"|analyst-completeness|qa-research-gate"
    r"|synthesis-\d+|analyst-synthesis|qa-synthesis-gate"
    r"|assembly|structural-qa|qualitative-qa|completion)$"
)
```

**Trace**: Writer: hand-maintained regex. Reader: `config.py:95`. The canonical step list lives in `executor.py:_STAGE_A_STEPS` and friends, plus `GATE_CRITERIA` keys in `gates.py`. Three independent source-of-truth lists for step IDs; nothing enforces synchrony.

**Reproduction sketch**: Add a new step `taxonomy-review` to `_STAGE_A_STEPS` and ship it. `superclaude prd resume taxonomy-review` fails with "Unrecognised resume step ID" until someone remembers to edit the regex. Classic P1.

**Confidence (own)**: 0.95.

---

## Considered and rejected

- **`--debug` flag wiring**: Click → resolve_config → `PrdConfig.debug`. I did not trace every consumer of `debug` (out of slice; cosmetic if missed). Not flagged.
- **`--model` flag wiring**: cleanly threaded through to `process.py:156`. No finding.
- **`--dry-run` flag**: handled at the CLI layer in `commands.py:119-125`, never reaches `PrdConfig.dry_run` consumers because the executor never runs in dry mode. The `PrdConfig.dry_run` field at `models.py` is therefore dead, but cosmetic — the CLI short-circuits before executor construction. Not flagging as a separate critical finding; mentioning for completeness.
- **`PrdConfig.dry_run` field unused** (related to above): writer-only field, no reader; would be P2 in isolation but the CLI's early `return` makes the dataclass field a vestige rather than a bug. Borderline; left out.
- **`scenario` / `prd_scope` / `why` / `template_path` / `stall_*` / `max_*_fix_cycles` / `*_partition_threshold` fields**: declared on `PrdConfig` with defaults; none are exposed via CLI flags. By Agent C's slice ("every CLI flag → downstream reader"), these fall outside scope. Some may be readers-only (set by executor mid-run) or also dead — Agent A's executor sweep should cover.
- **`product_name` vs `PRODUCT_NAME` from parse-request JSON**: same shape as F-C-6 for slug; mentioned in passing rather than as a separate finding to avoid double-counting.
- **NFR-PRD.1 / NFR-PRD.7 enforcement claims in docstrings**: the modules I read contained no `async`/`await` and no sprint/roadmap imports. Verified by inspection but not a finding.
