# Research: Pattern Templates

Status: Complete
Date: 2026-06-03

---

## Summary (read first)

Five reusable code patterns the new sc-recommend lookup-cache module must mirror, each with
verbatim excerpts + file:line:

1. **Atomic registry skeleton** — `DeviationRegistry` in `cli/roadmap/convergence.py`:
   `load_or_create` (104-136, hash-reset-on-mismatch), `save` (304-317, tmp+`os.replace`),
   `schema_version`, SHA256 helper (63-71). **YAML adaptation derived**: swap `json.dumps` →
   `yaml.safe_dump(sort_keys=False, default_flow_style=False, allow_unicode=True)`, `spec_hash` →
   `surface_hash` as reset key, `schema_version: 2`, `rows` as `list[dict]`.
2. **Plugin-eval hard block** — `cli/install_mcp.py`: `check_mcp_server_installed` (470-489, substring
   match over `claude mcp list`) + `check_binary_available` (156-164, `<bin> --version`). Reuse
   directly; both fail-closed to `False`.
3. **YAML I/O precedent** — cleanest writer is `cli/eval/run_report.py:358-363`
   (`safe_dump(sort_keys=False, default_flow_style=False, allow_unicode=True)`); cleanest reader is
   `cli/audit/wiring_config.py:92-98` (`safe_load` + `YAMLError` guard + `isinstance` check).
   `safe_*` only — `roadmap/semantic_layer.py:680`'s bare `yaml.dump` is the anti-pattern.
4. **Closed-enum classifier** — `core/ORCHESTRATOR.md` decision tree (closed enum, weighted scoring,
   `within 0.1` top-2 resolution, `< 0.7` prompt) + `sc-task-protocol/SKILL.md:56-78` keyword tables
   & confidence display. The `within 0.1` rule IS the precedent for `confidence_top2_delta < 10%`;
   delta computed in one pass, no extra LLM call.
5. **Agent spawn + model override** — `task-builder/SKILL.md:787-791` `Agent:` block
   (`subagent_type`/`mode`/`prompt`); add `model: "haiku"` field. Alias validation per
   `sc-adversarial-protocol/refs/agent-specs.md:62-73`.

---

This document captures the exact, reusable code patterns the new sc-recommend
lookup-cache module must mirror. Every excerpt is verbatim with file:line anchors.

---

## 1. Atomic file-backed registry — `DeviationRegistry` (the cache's skeleton)

File: `src/superclaude/cli/roadmap/convergence.py`

This is the canonical "load-or-create + atomic-save + schema-version + hash-reset-on-mismatch"
pattern the YAML cache (`LookupCache`) must mirror. The cache stores `rows` keyed by
`classification_key` instead of `findings` keyed by `stable_id`, and emits YAML instead of JSON,
but the structural skeleton is identical.

### 1a. Module imports + dataclass header (lines 8-22, 90-102)

```python
from __future__ import annotations

import atexit
import hashlib
import json
import logging
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable
```

```python
@dataclass
class DeviationRegistry:
    """File-backed deviation registry with stable finding IDs.

    Implements FR-6 (persistent registry), FR-10 (run-to-run memory).
    Status values: ACTIVE, FIXED, FAILED, SKIPPED.
    """

    path: Path
    release_id: str
    spec_hash: str
    runs: list[dict] = field(default_factory=list)
    findings: dict[str, dict] = field(default_factory=dict)
```

### 1b. `load_or_create` — hash-reset-on-mismatch (lines 104-136), VERBATIM

```python
    @classmethod
    def load_or_create(
        cls, path: Path, release_id: str, spec_hash: str
    ) -> DeviationRegistry:
        """Load existing registry or create fresh one.

        If spec_hash differs from saved -> reset (new spec version, FR-6).
        Pre-v3.05 registries: findings missing source_layer default to "structural".
        """
        if path.exists():
            try:
                data = json.loads(path.read_text())
                if data.get("spec_hash") == spec_hash:
                    findings = data.get("findings", {})
                    # Backward compat: default source_layer for pre-v3.05 registries
                    for fid, finding in findings.items():
                        if "source_layer" not in finding:
                            finding["source_layer"] = "structural"
                        if "first_seen_run" not in finding:
                            finding["first_seen_run"] = 1
                        if "last_seen_run" not in finding:
                            finding["last_seen_run"] = 1
                    return cls(
                        path=path,
                        release_id=release_id,
                        spec_hash=spec_hash,
                        runs=data.get("runs", []),
                        findings=findings,
                    )
                logger.info("Spec hash changed; resetting deviation registry")
            except (json.JSONDecodeError, KeyError):
                logger.warning("Corrupted registry at %s; creating fresh", path)
        return cls(path=path, release_id=release_id, spec_hash=spec_hash)
```

Three load-bearing behaviours to replicate:

1. **Guard `path.exists()`** before reading.
2. **`spec_hash` equality check** decides reset. For the cache, the equivalent field is
   `surface_hash` — if the stored `surface_hash != current surface hash`, the cache is stale
   (surface changed: command/skill/agent added/renamed/deleted) and rows must be discarded
   (or at minimum flagged for revalidation). Round-2 design (merged-requirements "Invalidation
   Strategy") puts `surface_hash` at the YAML top exactly so this comparison is one cheap read.
3. **`try/except` over parse errors** -> log + fall through to fresh-create. The cache adapts
   `json.JSONDecodeError` -> `yaml.YAMLError`.

### 1c. `save()` — atomic tmp + os.replace() (lines 304-317), VERBATIM

```python
    def save(self) -> None:
        """Atomic write: tmp + os.replace()."""
        import os

        data = {
            "schema_version": 1,
            "release_id": self.release_id,
            "spec_hash": self.spec_hash,
            "runs": self.runs,
            "findings": self.findings,
        }
        tmp_path = self.path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(data, indent=2))
        os.replace(str(tmp_path), str(self.path))
```

The atomic-write contract (write tmp -> `os.replace`) is what the merged-requirements Cold-Path
step 4 explicitly cites: *"Parent commits the update ... via atomic write (`tmp + os.replace()`
per `convergence.py:DeviationRegistry.save()`)"*. `os.replace` is atomic on POSIX and Windows;
concurrent readers never see a half-written file.

### 1d. Schema version + hash helper (lines 63-71), VERBATIM

```python
def compute_stable_id(
    dimension: str,
    rule_id: str,
    spec_location: str,
    mismatch_type: str,
) -> str:
    """Deterministic finding ID from structural properties."""
    key = f"{dimension}:{rule_id}:{spec_location}:{mismatch_type}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]
```

This is the SHA256 idiom the cache reuses two ways:

- **`surface_hash`**: `hashlib.sha256(<sorted Glob output joined>).hexdigest()` (full digest, not
  truncated) — merged-requirements specifies `sha256:<hash of sorted Glob output>`.
- **`source_hash` per row**: `hashlib.sha256(candidate_source_bytes).hexdigest()` — the hot-path
  step-6 validation Read computes this and compares against `row.source_hash`.

Note: `compute_stable_id` truncates to `[:16]` for a compact ID; for content-integrity hashes the
cache should keep the **full digest** (the requirements write `sha256:abc123...` as the stored
form, and integrity hashes should not be truncated).

### 1e. THE YAML ADAPTATION (derived — user did not specify)

The cache mirrors `save()` / `load_or_create()` but swaps the JSON codec for YAML. The minimal,
faithful adaptation:

```python
import os
import yaml

def save(self) -> None:
    """Atomic write: tmp + os.replace(), YAML body."""
    data = {
        "schema_version": 2,                      # round-3 bumped 1 -> 2 (best_model + eval_history)
        "surface_hash": self.surface_hash,        # replaces spec_hash as the reset key
        "generated": self.generated,
        "generator": "sc-recommend-cache/v0.2",
        "rows": self.rows,                        # list[dict] keyed-by-`key` semantics
    }
    tmp_path = self.path.with_suffix(".tmp")
    tmp_path.write_text(
        yaml.safe_dump(data, sort_keys=False, default_flow_style=False, allow_unicode=True)
    )
    os.replace(str(tmp_path), str(self.path))
```

```python
@classmethod
def load_or_create(cls, path: Path, surface_hash: str) -> "LookupCache":
    if path.exists():
        try:
            data = yaml.safe_load(path.read_text()) or {}
            if data.get("surface_hash") == surface_hash:
                return cls(
                    path=path,
                    surface_hash=surface_hash,
                    generated=data.get("generated"),
                    rows=data.get("rows", []),
                )
            logger.info("Surface hash changed; resetting lookup cache")
        except yaml.YAMLError:
            logger.warning("Corrupted cache at %s; creating fresh", path)
    return cls(path=path, surface_hash=surface_hash, rows=[])
```

Adaptation rationale (each point is a deliberate divergence from the JSON original):

- **`yaml.safe_dump`, not `json.dumps`** — the requirements store human-editable YAML so a
  maintainer can read/diff rows. `safe_load`/`safe_dump` (never `yaml.load`/`yaml.dump`) is the
  established project convention (see Section 3).
- **`sort_keys=False`** — preserve the authored field order (`key`, `candidate`, `flags`,
  `prompt_envelope_template`, ...). JSON had implicit insertion order via dict; YAML's default
  alphabetizes, which scrambles the schema. This is the single most important dump option.
- **`default_flow_style=False`** — force block style (multi-line `key: value`) instead of inline
  `{a: 1, b: 2}`. Required for the multi-line `prompt_envelope_template` literal block to render
  cleanly and for readable diffs.
- **`allow_unicode=True`** — `prompt_envelope_template` and rationale fields contain arbitrary
  prose; without this, non-ASCII gets `\uXXXX`-escaped.
- **`surface_hash` replaces `spec_hash`** as the reset key (point 1b).
- **`schema_version: 2`** — round-3 bumped from 1 (adds `best_model` + `eval_history`). On a
  version mismatch the loader may choose to migrate or reset; the requirements treat schema bump
  as additive (new optional fields), so a forward-compatible loader that tolerates missing
  `best_model`/`eval_history` (like the `load_or_create` backward-compat block in 1b) is sufficient.
- **`rows` is a `list[dict]`** (per the requirements YAML), scanned by `key`, not a `dict[str, dict]`
  like `findings`. The hot-path step-5 "table scan: find row where `key == classification_key`" is
  a linear scan over `rows`; at ~30 rows this is trivially cheap. (A loader could index into a dict
  on load for O(1), but the on-disk form is a list to keep authoring/diffing natural.)

---

## 2. Plugin-eval HARD-BLOCK precondition — MCP detection

File: `src/superclaude/cli/install_mcp.py`

These two functions are the precondition gate for plugin-mode eval: before running a
with-resource-installed eval run, the orchestrator must confirm the MCP server / binary is
actually present locally. The merged-requirements Plugin lifecycle phase 4 cites *"detection via
a `which`-style check"* and the plugin eval requires the resource installed before the
with-resource runs.

### 2a. `check_mcp_server_installed` (lines 470-489), VERBATIM

```python
def check_mcp_server_installed(server_name: str) -> bool:
    """Check if an MCP server is already installed."""
    try:
        result = _run_command(
            ["claude", "mcp", "list"], capture_output=True, text=True, timeout=60
        )

        if result is None or result.returncode != 0:
            return False

        # Handle case where stdout might be None
        output = result.stdout
        if output is None:
            return False

        # Parse output to check if server is installed
        return server_name.lower() in output.lower()

    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        return False
```

How it parses `claude mcp list`: it does **not** structurally parse the output — it does a
case-insensitive substring containment check (`server_name.lower() in output.lower()`). Simple and
robust to formatting changes in `claude mcp list`. Failure modes all return `False` (server treated
as not-installed): non-zero exit, `None` result, `None` stdout, timeout (60s), or any
`SubprocessError`. For the plugin-eval hard block, "can't confirm installed" == "blocked", which is
the correct conservative default.

### 2b. `check_binary_available` (lines 156-164), VERBATIM

```python
def check_binary_available(binary_name: str) -> bool:
    """Check if a binary is available on PATH."""
    try:
        result = _run_command(
            [binary_name, "--version"], capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False
```

The `which`-style check for a CLI binary: invoke `<binary> --version`, success == exit 0.
`FileNotFoundError` (binary not on PATH) -> `False`; 10s timeout. This is the pattern for any
community-skill/plugin that ships a CLI entry point.

### 2c. `_run_command` cross-platform shell wrapper (lines ~111-142), context

Both checks route through `_run_command`, which both functions depend on. It UTF-8 encodes
(`errors="replace"`), and on POSIX runs via the user's `$SHELL` (so aliases resolve), on Windows
wraps in `cmd /c`:

```python
    if platform.system() == "Windows":
        cmd = ["cmd", "/c"] + cmd
        return subprocess.run(cmd, **kwargs)
    else:
        cmd_str = " ".join(shlex.quote(str(arg)) for arg in cmd)
        user_shell = os.environ.get("SHELL", "/bin/bash")
        return subprocess.run(
            cmd_str, shell=True, env=os.environ, executable=user_shell, **kwargs
        )
```

The cache's plugin-eval precondition should reuse `check_mcp_server_installed` /
`check_binary_available` directly (import from `superclaude.cli.install_mcp`) rather than reimplement
the subprocess plumbing — they already handle the cross-platform + None-safety edge cases.

---

## 3. YAML read/write precedent in the CLI

The project has a clear, consistent house style for YAML I/O. Cross-referencing the three named
files plus the broader `src/superclaude/cli/` tree:

### 3a. READ precedent — `yaml.safe_load` + typed-error guard

All readers use `yaml.safe_load` (never `yaml.load`) wrapped in a `try/except yaml.YAMLError`.

**`src/superclaude/cli/audit/wiring_config.py:92-98`** (cleanest read precedent — graceful):

```python
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        if rollout_mode == "shadow":
            logger.warning("Malformed whitelist YAML at %s: %s", path, exc)
            return []
        raise WiringConfigError(f"Malformed whitelist YAML at {path}: {exc}") from exc

    if not isinstance(raw, dict):
        ...
```

Note three reusable habits: (a) `read_text(encoding="utf-8")`, (b) `except yaml.YAMLError`,
(c) `isinstance(raw, dict)` top-level-mapping validation after decode. The same three appear in
`eval/loader.py:241-256` (`decoded = yaml.safe_load(raw)` then `isinstance(decoded, Mapping)`).

**`src/superclaude/cli/roadmap/spec_parser.py:115-129`** — frontmatter parsing (the
`---\n...\n---` envelope split, relevant because cache YAML files and the plugin/skill SKILL.md
share the frontmatter convention):

```python
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return {}

    yaml_text = match.group(1)

    # Try proper YAML parsing first
    try:
        import yaml

        result = yaml.safe_load(yaml_text)
        if isinstance(result, dict):
            return result
    except Exception:
        pass
```

The regex `^---\s*\n(.*?)\n---\s*\n` with `re.DOTALL` is the canonical frontmatter extractor used
across the codebase (also at `spec_parser.py:510`). Reuse this exact regex if the cache needs to
split frontmatter from a body.

### 3b. WRITE precedent — `yaml.safe_dump(sort_keys=False, default_flow_style=False, allow_unicode=True)`

The CLEANEST writer precedent for the cache is the **eval module**, which writes the exact triplet
of options the cache needs. Two near-identical call sites:

**`src/superclaude/cli/eval/run_report.py:358-363`** (PICK THIS as the cache writer template):

```python
    return yaml.safe_dump(
        payload,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )
```

Its docstring (lines 348-353) states the rationale verbatim:
> *"Uses `yaml.safe_dump` with `sort_keys=False` so the output preserves the DM-004 field
> declaration order ... `default_flow_style=False` keeps the result in canonical block style
> (one key per line)."*

**`src/superclaude/cli/eval/commands.py:1187-1192`** — identical option set, docstring at
1181-1184 reiterates: *"`sort_keys=False` preserves the manifest field ordering ...
`default_flow_style=False` keeps block-style for human review."*

Other writers in the tree confirm the convention but are less complete:

- `audit/wiring_gate.py:818` — `yaml.safe_dump(fm, default_flow_style=False, sort_keys=False)`
  (frontmatter re-serialization; explicitly chosen "to prevent YAML injection", per the comment at
  line 744). No `allow_unicode`.
- `cli_portify/executor.py:371` — `yaml.safe_dump(contract, fh, default_flow_style=False)`
  (streams to a file handle; omits `sort_keys`, so it alphabetizes — NOT a good template).
- `roadmap/semantic_layer.py:680` — `yaml.dump(...)` (the one non-`safe` writer; the cache MUST
  NOT copy this — use `safe_dump`).

**Verdict for the cache writer:** copy `eval/run_report.py:358-363` exactly
(`safe_dump(payload, sort_keys=False, default_flow_style=False, allow_unicode=True)`), and wrap it
in the atomic tmp+`os.replace` envelope from Section 1c/1e. `sort_keys=False` is non-negotiable —
it is what preserves the authored row-field order (`key`, `candidate`, `flags`,
`prompt_envelope_template`, `best_model`, `eval_history`). `allow_unicode=True` matters because
`prompt_envelope_template` / `rationale` carry free prose.

Note: `safe_dump` terminates output with a trailing newline (per the comment at
`eval/commands.py:1286`), so no manual `+ "\n"` is needed when writing the tmp file.

---

## 4. Closed-enum classifier — the structure the Haiku classifier prompt must mirror

Files: `src/superclaude/core/ORCHESTRATOR.md` (Tier Classification Routing, ~lines 162-235) and
`src/superclaude/skills/sc-task-protocol/SKILL.md` (lines 56-78).

This is the pattern the merged-requirements "Haiku Invocation Pattern" step-2 cites:
*"Haiku classifies request -> `{classification_key, native_likely, confidence_top2_delta}`.
Pattern: the `sc:task` compliance-tier classifier."* The cache classifier mirrors FIVE structural
elements:

### 4a. Closed-enum keyword tables (the discrete output set)

`sc-task-protocol/SKILL.md:58-61` — the keyword-per-tier tables. ONLY four tier values are valid
(closed enum); the SKILL header (line 9) is explicit: *"using ONLY the tier values STRICT,
STANDARD, LIGHT, or EXEMPT (no other values are valid)."*

```text
- STRICT:   security, authentication, database, migration, refactor, breaking change, encrypt, token, session, oauth
- EXEMPT:   explain, search, commit, push, plan, discuss, brainstorm
- LIGHT:    typo, comment, whitespace, lint, docstring, formatting, minor
- STANDARD: implement, add, create, update, fix, build, modify, change (default)
```

**Cache adaptation:** the cache classifier's closed enum is the set of `classification_key`s
present in the lookup table's `rows[].key` (e.g., `spec-generation`, `tasklist-generation`, ...),
PLUS a synthetic `native` bucket (for `native_likely == true`) and an implicit `unknown`/no-match
(`cache_miss: no_key`). The Haiku prompt must be handed the current key set inline (the keys ARE
the closed enum), exactly as the tier classifier hardcodes its four tiers.

### 4b. Scoring (sum of weighted keyword matches + context boosts)

`ORCHESTRATOR.md` Classification Decision Tree (`step_3_keywords`), VERBATIM:

```yaml
  step_3_keywords:
    action: "score all keywords, apply context boosters"
    scoring: "sum(keyword_matches * weight) + context_boosts"
```

Context Boosters table (`ORCHESTRATOR.md` ~lines 201-210) shows the additive-boost shape — a
`Signal -> Tier Boost -> Amount` table (e.g., `estimated_files > 2 -> STRICT +0.3`,
`is_read_only -> EXEMPT +0.4`). The cache classifier's analogue is a per-key score from semantic
match strength; `native_likely` is itself a boost-style signal (small-task heuristics: single-line
edit, file-read-and-explain, ~40-line refactor → push toward the `native` bucket, per
merged-requirements Hot-Path step 3).

### 4c. Top-2 confidence delta + tie resolution (THE load-bearing element)

`ORCHESTRATOR.md` `step_4_resolve`, VERBATIM:

```yaml
  step_4_resolve:
    condition: "scores within 0.1 of each other"
    action: "escalate to higher priority tier"
    priority: "STRICT > EXEMPT > LIGHT > STANDARD"
```

This `within 0.1 of each other` is the EXACT precedent for the cache's
`confidence_top2_delta < 10%` ambiguity gate (merged-requirements Hot-Path step 4). The tier
classifier *escalates* on a close top-2; the cache instead *treats it as a miss*
(`cache_miss: low_confidence`, fall to cold path). The key shared mechanic: **the delta between the
top-2 scores is the ambiguity signal, and it is computed inside the single classification pass — no
extra LLM call** (merged-requirements step 4 emphasises: *"the delta is already in step-2 output"*).
The Haiku classifier prompt must therefore return BOTH the winning key AND the runner-up score (or
the delta directly) in one JSON object.

### 4d. The `< 0.7` low-confidence prompt

`ORCHESTRATOR.md` `step_5_confidence`, VERBATIM:

```yaml
  step_5_confidence:
    condition: "confidence < 0.7"
    action: "prompt user for confirmation"
```

`sc-task-protocol/SKILL.md:76`: *"If confidence <70%, add prompt: '⚠️ Low confidence. Override
with: `--compliance [strict|standard|light|exempt]`'"*. The cache analogue: below-threshold
classification confidence is one of the cold-path fall reasons / surfaced as a low-confidence
recommendation; the structure (a single numeric threshold gating a user-confirmation branch) is
mirrored directly.

### 4e. Machine + human confidence display

`sc-task-protocol/SKILL.md:66-74` — the human-readable confidence block the classifier emits:

```text
**Tier: STANDARD** [████████░░] 80%

Classified as STANDARD:
- Keywords matched: add, implement
- Confidence score: 0.78
- Considered alternatives: STRICT (0.35)
```

Note the **"Considered alternatives: STRICT (0.35)"** line — this is the top-2 runner-up made
visible, the same datum the delta gate (4c) consumes. The cache's telemetry event
(`classification_key`, `cache_result`) is the machine-readable sibling; this human block is the
template for surfacing the chosen key + runner-up to the user.

**Summary of the classifier STRUCTURE the Haiku prompt mirrors** (5 elements):
closed enum of valid outputs → weighted keyword/signal scoring → top-2 delta computed in one pass →
`< 0.7` low-confidence branch → machine+human confidence emission. The cache swaps the 4 fixed
tiers for the dynamic `rows[].key` set + `native` + `unknown`, and swaps "escalate on close top-2"
for "miss to cold-path on close top-2."

---

## 5. Agent-tool spawn shape with model override (`model: haiku` subagent)

File: `src/superclaude/skills/task-builder/SKILL.md` (A.9, lines 781-811) — the canonical
`Agent:` block shape; plus the model-alias convention from
`src/superclaude/skills/sc-adversarial-protocol/refs/agent-specs.md`.

### 5a. The base Agent-tool block (task-builder A.9, lines 787-791), VERBATIM

```text
Agent:
  subagent_type: "rf-task-builder"
  mode: "bypassPermissions"
  prompt: |
    BUILD_REQUEST:
    ==============
    GOAL: [GOAL — what the task file should accomplish when executed]
    ...
```

The three load-bearing keys: `subagent_type` (which agent), `mode` (permission mode,
`bypassPermissions` for autonomous file-writing agents), `prompt` (a YAML literal block `|`
carrying the structured request). This is the shape the cache parent uses to spawn its Haiku
workers.

### 5b. Adding the `model:` override — the derived shape for `model: haiku`

The merged-requirements "Haiku Invocation Pattern" mandates *"the Agent tool with `model: haiku`"*
for BOTH hot-path and cold-path workers. Composing the A.9 block with a model field:

```text
Agent:
  subagent_type: "general-purpose"      # or a dedicated sc-recommend-worker agent
  mode: "bypassPermissions"
  model: "haiku"                         # <-- the override; forces the cheap model
  prompt: |
    <ROLE>
    You are the sc-recommend worker. Produce a refined paste-ready prompt.
    Parent surfaces your output verbatim — no conversational addressing.
    Respect rules R1/R2/R3 from sc-recommend SKILL.md.
    </ROLE>
    <REQUEST>
    User request: "<verbatim>"
    Mode: local | plugin
    Worktree root: <cwd>
    Eval mode (R3): none | quick | normal | deep
    </REQUEST>
    <TABLE>
    <inlined YAML>   OR   <EMPTY — run cold-path>
    </TABLE>
    <INSTRUCTIONS>
    [hot-path lookup runbook OR cold-path condensed pipeline]
    </INSTRUCTIONS>
    <RETURN>
    JSON: {status, mode, recommendation_kind, prompt_block, verified_sources,
           native_likely, confidence_top2_delta, best_model_hint?,
           cache_miss?, cache_update?}
    </RETURN>
```

The `prompt` body above is lifted verbatim from merged-requirements "Haiku Invocation Pattern".

### 5c. Model-alias convention (the values `model:` accepts)

`sc-adversarial-protocol/refs/agent-specs.md:62-73` defines how models are named and validated.
Models are resolved from aliases (`opus`, `sonnet`, `haiku`) — `agent-spec-builder.md:30-36`:
*"Active model aliases (resolved from `~/.bashrc`)"*, default rotation `opus,sonnet,haiku`.
Validation (agent-specs.md:67,71): *"Model must be a recognized model name or alias"*; unknown ->
*"STOP with error: 'Unknown model: <model>'"*. So `model: "haiku"` is a recognized alias.

Two spawn conventions coexist in the codebase — the cache should pick by mechanism:

1. **Direct Agent-tool block with `model:` field** (5b) — used when the parent itself spawns ONE
   worker on a specific model. This is what the cache hot/cold paths want: parent spawns one Haiku
   subagent via the Agent tool. Matches merged-requirements verbatim ("Agent tool with `model:
   haiku`").
2. **`model:persona[:instruction]` agent-spec string** routed through `/sc:adversarial --agents`
   (agent-specs.md:78-90, e.g. `--agents opus:architect,sonnet:security,haiku:qa`) — used for
   multi-model fan-out debates. RELEVANT TO `--eval`: the per-row eval pipeline
   (merged-requirements `--eval` section) spawns N parallel subagents per model across
   `[opus, sonnet, haiku]` — that fan-out is naturally expressed as the agent-spec string list, or
   as N parallel Agent-tool blocks each with a different `model:` value.

**Recommendation for the builder:** for the two hot/cold-path workers, use the direct Agent-tool
block (5b) with `model: "haiku"`. For the `--eval` fan-out, spawn N parallel Agent-tool blocks,
one per `(model, run)` pair, each setting `model:` to the panel model — this reuses the same block
shape and keeps the parent's "spawn, surface, commit" role (merged-requirements: *"Parent does not
classify, scan, repair ... for the work itself"*).

---

## Cross-cutting notes for the builder

- **Reuse, don't reimplement:** import `check_mcp_server_installed` / `check_binary_available` from
  `superclaude.cli.install_mcp`; copy the atomic-save envelope from `convergence.py`; copy the
  `safe_dump(sort_keys=False, default_flow_style=False, allow_unicode=True)` call from
  `eval/run_report.py`.
- **`safe_load`/`safe_dump` only** — `roadmap/semantic_layer.py:680` uses bare `yaml.dump`; do NOT
  follow that one. Every other CLI reader/writer uses the `safe_` variants.
- **Full digest for integrity hashes** — `compute_stable_id` truncates `[:16]` for compact IDs, but
  `surface_hash` / `source_hash` should keep the full `hexdigest()`.
- **`sort_keys=False` is mandatory** for the cache writer — it is the only thing preserving the
  authored row-field order across read→modify→write cycles.
