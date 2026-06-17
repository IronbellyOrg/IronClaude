# R2 Research: swarm CLI thin-caller surface (`superclaude swarm run --lens bare-review`)

Status: Complete

Scope: Prove the `superclaude swarm run --lens bare-review` CLI surface can fully replace the
legacy sc-bare-review scripts (t2_preflight.sh / t2_dispatch.sh / t2_normalize.py) and document
the exact flag mapping. Every claim carries `file:line` evidence.

Repo root: `/config/workspace/IronClaude`. All paths absolute.

---

## TL;DR — Migration verdict

The `swarm run --lens bare-review` surface **CANNOT fully replace the legacy scripts as wired
today**. Two classes of blocker:

1. **CLI flag gaps (B-1..B-4):** four legacy `t2_preflight.sh` flags have **no `swarm run`
   equivalent**: `--reviewers` (worker count), `--timeout-sec`, `--target-line-cap`, `--label`.
   The lens defaults supply fixed values (3 workers, 4000 line-cap), so a thin caller cannot vary
   them from the CLI without writing a full spec file.
2. **Pipeline wiring gap (B-5, HEADLINE):** the inline (non-resume) `run_cmd` body is the T03.01
   reference body — it calls **only `dispatch_wave1`** and emits a **stdout stub line**. It does
   **NOT** call `normalize_wave2`, `reduce_wave3`, or `emit_contract`, and it dispatches with an
   **empty prompt** (`prompt=""`). So `swarm run --lens bare-review --target X --output Y` does
   **not** produce `merged.md`, `return-contract.yaml`, or normalized per-reviewer bodies. The
   `bare_review_v1` recipe (parity-faithful port of `t2_normalize.py`) **exists but is never
   invoked on the inline path**. Only the `--resume` branch runs the full Wave 2 + Wave 3 pipeline.

The lens registry + recipe (scope items 2 and 3) are **correct and complete**. The blocker is
purely the CLI plumbing in `commands.py::run_cmd`.

---

## 1. `run_cmd` option enumeration + legacy flag mapping

### Every option `run_cmd` accepts

Source: `src/superclaude/cli/swarm/commands.py`, decorator stack lines 1181-1303, signature
lines 1304-1315.

| Option | Click name | Type | Default | Evidence (file:line) |
|---|---|---|---|---|
| `SPEC_PATH` (positional) | `spec_path` | `Path` (exists, file) | `None` (required=False) | commands.py:1182-1191 |
| `--stdin` | `stdin_mode` | flag | `False` | commands.py:1192-1198 |
| `--lens` | `lens` | `str` | `None` | commands.py:1199-1213 |
| `--resume` | `resume_job_id` | `str` | `None` | commands.py:1214-1232 |
| `--target` | `target_path` | `Path` | `None` | commands.py:1233-1242 |
| `--output` | `output_dir` | `Path` (file_okay=False) | `None` | commands.py:1243-1254 |
| `--transport` | `transport_kind` | `Choice(openai_compat, stub)` | `None` | commands.py:1255-1266, choices `_TRANSPORT_KINDS` line 489 |
| `--force-relens` | `force_relens` | flag | `False` | commands.py:1267-1284 |
| `--detached` | `detached` | flag | `False` | commands.py:1285-1302 |
| `--auto-inject-guard` | `auto_inject_guard` | flag | `False` | `auto_inject_guard_option` decorator commands.py:154-167, attached line 1303 |

That is the **complete** set — nine options + one positional argument. There is **no**
`--reviewers`, `--workers`, `--timeout-sec`, `--target-line-cap`, `--line-cap`, or `--label`
option. Verified by negative grep: `grep -n '"--label"|"--timeout|"--reviewers"|"--workers"|"--target-line-cap"|"--line-cap"' commands.py` returns **zero** matches.

### Legacy `t2_preflight.sh` flag surface

Source: `src/superclaude/skills/sc-bare-review/scripts/t2_preflight.sh:29-50` (the `case "$1"`
arg parser) + usage banner lines 10-11.

| Legacy flag | Meaning | Required? | Evidence |
|---|---|---|---|
| `--target <path>` | file to review | yes | t2_preflight.sh:30, required check :45 |
| `--reviewers <2-4>` | worker count, validated to integer in [2,4] | yes | t2_preflight.sh:31, :46, :49-50 |
| `--output <dir>` | output directory | yes | t2_preflight.sh:32, :47 |
| `--target-line-cap <N>` | truncation cap | optional | t2_preflight.sh:33 |
| `--timeout-sec <N>` | per-worker timeout (or `T2Timeout` env) | optional | t2_preflight.sh:34, validated :75 |
| `--label <str>` | caller tag stamped on outputs | optional | t2_preflight.sh:35 |

### Flag mapping (legacy → `swarm run`)

| Legacy flag | `swarm run` equivalent | Status |
|---|---|---|
| `--target <path>` | `--target <path>` | DIRECT — commands.py:1233-1242, applied to `spec_dict.target.path` at commands.py:1449-1450 |
| `--output <dir>` | `--output <dir>` | DIRECT — commands.py:1243-1254, applied to `spec_dict.output.dir` at commands.py:1451-1452 |
| `--reviewers <2-4>` | *(none)* | **BLOCKER B-1** — no CLI option. Worker count comes only from `lens.default_workers=3` (bare_review.py:61) via `_build_spec_from_lens` (commands.py:767: `workers_count = max(1, int(entry.default_workers or 1))`). A thin caller cannot request 2 or 4 reviewers from the CLI; it is pinned at 3. Note legacy `[2,4]` validity range vs the lens default of 3. |
| `--target-line-cap <N>` | *(none)* | **BLOCKER B-2** — no CLI option. Line-cap comes only from `lens.default_target_line_cap=4000` (bare_review.py:62) via commands.py:817 (`"line_cap": entry.default_target_line_cap`). Preflight overrides a 4000/≤0 cap with the lens default (preflight.py:527-528), so even a spec value of 4000 is replaced — only a non-4000 spec value survives. CLI cannot set it at all. |
| `--timeout-sec <N>` | *(none)* | **BLOCKER B-3** — no CLI option. The lens spec hardcodes `workers.timeout_sec=180` (commands.py:789). Furthermore the inline dispatch path passes **no `worker_spec`** (see §4), so the timeout is not even threaded into dispatch on the inline path. |
| `--label <str>` | *(none)* | **BLOCKER B-4** — no CLI option. The lens spec hardcodes `caller.invocation_label=f"swarm-run-lens-{lens_name}"` (commands.py:775). The recipe consumes `caller_label` from `args` (bare_review_v1.py:235, :255) but there is no CLI surface to set it. Legacy stamped `--label` into per-reviewer frontmatter. |

**Migration-blocker summary for §1:** 4 of 6 legacy flags (`--reviewers`, `--target-line-cap`,
`--timeout-sec`, `--label`) have **no `swarm run` CLI equivalent**. The only escape hatch is
spec-file mode (`SPEC_PATH` / `--stdin`), which defeats the "thin caller passes flags" model — a
thin caller would have to synthesize a full DM-001 JobSpec JSON.

---

## 2. `bare-review` LensEntry — fields + registration

Source: `src/superclaude/cli/swarm/lenses/bare_review.py:40-75` (the `LENS` constant).

Confirmed `LensEntry` field values:

| Field | Value | Evidence |
|---|---|---|
| `name` | `"bare-review"` | bare_review.py:41 |
| `recipe_name` | `"bare-review-v1"` | bare_review.py:59 |
| `normalizer_strategy` | `"bare-review-v1"` | bare_review.py:60 |
| `default_workers` | `3` | bare_review.py:61 |
| `default_target_line_cap` | `4000` | bare_review.py:62 |
| `suspect` | `True` | bare_review.py:63 |
| `tier` | `"T2"` | bare_review.py:64 |
| `stability` | `"stable"` (the only stable lens) | bare_review.py:74; lenses/__init__.py:22-23 |
| `system_prompt_fragment` | bare-review framing + appended `CANONICAL_INJECTION_GUARD_SENTENCE` | bare_review.py:47-52 |
| `user_template` | findings-table prompt w/ `{target_content}` + `<<<TARGET>>>` delimiters | bare_review.py:53-57 |
| `output_template_path` | resolved `templates/bare-review-output.md` | bare_review.py:35-37, :58 |
| `recommended_next_command_template` | `/sc:adversarial --compare {compare_files} --suspect-source {suspect_files}` | bare_review.py:65-68 |

`LensEntry` dataclass field definitions confirmed at `models.py:707-720` (field set matches:
`name, description, system_prompt_fragment, user_template, output_template_path, recipe_name,
normalizer_strategy, default_workers, default_target_line_cap, suspect, tier,
recommended_next_command_template, acceptance_notes, stability`).

**Registration confirmed:** `bare-review` is imported as `_BARE_REVIEW_LENS`
(lenses/__init__.py:49) and registered first in the `LENSES` dict (lenses/__init__.py:106) and
first in `LENS_NAMES` (lenses/__init__.py:74). It is therefore resolvable by
`_resolve_input_mode` → `_build_spec_from_lens` (commands.py:984 membership check against
`LENSES`, then commands.py:766 `LENSES[lens_name]`).

`swarm validate-lenses` (commands.py:402-443) validates it via `validate_all(LENSES)`; it is the
canonical stable lens (lenses/__init__.py:22-23).

---

## 3. `bare_review_v1` recipe — exists, normalization vs legacy

Source: `src/superclaude/cli/swarm/recipes/bare_review_v1.py`.

- Recipe class `BareReviewV1` exists at bare_review_v1.py:212-309, implementing the `Recipe`
  protocol (`normalize(raw_output, args) -> NormalizedResult`, bare_review_v1.py:246).
- It is an **intentional byte-identical port** of the per-reviewer transform from the legacy
  `t2_normalize.py` (bare_review_v1.py:1-29 module docstring; constants/helpers "mirror
  t2_normalize.py verbatim" — `SEV_ALIASES` :93, `EMPTY_CITE` :100, `FINDING_ID` :101,
  `strip_frontmatter` :119, `normalize_sev` :127, `normalize_cite` :131, `parse_conf` :135,
  `parse_findings` :142, `extract_section` :163, `render_markdown` :175).
- **Scope split vs legacy:** the recipe owns ONLY the per-reviewer shape transform (frontmatter
  strip → findings-table parse → verdict/notes extraction → compressed-markdown render,
  bare_review_v1.py:272-308). It does **NOT** own the aggregator-level contract emission or file
  lifecycle (raw read, atomic `final_path` write, meta sidecar, timeout/proxy_error
  short-circuit) — those belong to the Wave-2 dispatcher `normalize.normalize_wave2`
  (bare_review_v1.py:5-12). The legacy `t2_normalize.py` owned both halves.
- §7.4 salvage semantics preserved: `parse_error` + recoverable content → `salvaged=True`
  (bare_review_v1.py:278-286); nothing recoverable → stays failed (bare_review_v1.py:280-285).
- A/B parity gate referenced: `tests/swarm/test_recipe_bare_review.py` (bare_review_v1.py:14-22)
  — (R3's domain to confirm it passes).

**Recipe registration:** `recipe_name="bare-review-v1"` (bare_review.py:59) resolves against the
recipe REGISTRY in `recipes/__init__.py` — referenced by `normalize_wave2` (commands.py:1952-1955
resume path raises `KeyError` if `recipe_name` not registered). The recipe file exists and is the
only `bare_review`-named recipe in `recipes/` (verified by directory listing).

**Conclusion for §3:** the recipe is present and is a faithful normalization replacement for the
legacy `t2_normalize.py` per-reviewer transform. The gap is not the recipe — it is that the inline
run path never calls it (see §4 / B-5).

---

## 4. End-to-end emission of `swarm run --lens bare-review --target X --output Y`

### What the inline run path actually does

Trace through `run_cmd` (commands.py:1304-1578) for the non-resume, non-detached lens-shortcut
invocation:

1. `--resume` not set → skip resume branch (commands.py:1368-1396).
2. `--force-relens` not set → skip guard (commands.py:1402-1408).
3. `_resolve_input_mode(None, False, "bare-review")` → `("lens", _build_spec_from_lens("bare-review"))`
   (commands.py:1410; builds full JobSpec dict at commands.py:728-868).
4. `--detached` not set → skip detached branch (commands.py:1418-1436).
5. Apply `--target`/`--output`/`--transport` overrides on the dict (commands.py:1449-1454).
6. `run_preflight(spec_dict, output_dir=..., auto_inject_guard=False)` (commands.py:1456-1461).
   On success this writes `manifest.json` and mkdir's the output dir.
7. If `manifest_path` set: instantiate dual-format `Logger` (`execution-log.jsonl` +
   `execution-log.md`, commands.py:1487-1500) and write `.swarm-state.json` = `preflight_ok`
   (commands.py:1505-1509).
8. Build the per-slot transport factory (commands.py:1531-1535).
9. Write `.swarm-state.json` = `dispatching` (commands.py:1547-1552).
10. `dispatch_wave1(preflight_result, transport_for_slot=..., logger=logger)` (commands.py:1554-1556).
    **NO `prompt=` arg is passed**, so dispatch sends `prompt=""` (default, dispatch.py:339).
    **NO `worker_spec=` arg is passed**, so no timeout policy is threaded (dispatch.py:341).
11. Write `.swarm-state.json` = `terminal` (commands.py:1562-1567).
12. Emit a **stdout stub line**: `swarm run: dispatched job (mode=lens, workers=N, results=M)`
    (commands.py:1573-1577), exit 0 (commands.py:1578).

### Files actually emitted on the inline path

- `manifest.json` — via `run_preflight` (commands.py:1456).
- `execution-log.jsonl` + `execution-log.md` — via the dual Logger (commands.py:1492-1500),
  populated by dispatch wave_transition / worker events (dispatch.py:431-490).
- `.swarm-state.json` — transitions preflight_ok → dispatching → terminal (commands.py:1505, 1548, 1562).
- Per-worker raw artefacts — whatever `dispatch_wave1` writes per slot.

### Files NOT emitted on the inline path (the gap)

- **`return-contract.yaml`** — NOT written. `emit_contract` (reduce.py:369-385,
  `CONTRACT_FILENAME = "return-contract.yaml"` reduce.py:139) is never called on the inline path.
  The stdout line at commands.py:1569-1577 is explicitly labeled a "Return-contract emission stub
  -- M5 replaces this with the real ResultContract writer (DM-012)".
- **`merged.md`** — NOT written. `reduce_wave3` (reduce.py:555) / merge are never called inline.
- **Normalized per-reviewer `.final.md` bodies** — NOT produced inline. `normalize_wave2` is never
  called on the inline path; `bare_review_v1.BareReviewV1.normalize` therefore never runs.

### Evidence that normalize/reduce are inline-absent

`grep -n 'normalize_wave2|reduce_wave3|emit_contract|dispatch_wave1' commands.py`:
- `dispatch_wave1` — called inline at commands.py:1554 AND in resume at :1930.
- `normalize_wave2` — imported/called **only** in `_run_resume_branch` (commands.py:1781, :1952).
- `reduce_wave3` — imported/called **only** in `_run_resume_branch` (commands.py:1788, :1977).
- `emit_contract` — **never** called from commands.py at all.

`dispatch_wave1` itself defers normalization explicitly: "is a Wave-2 normalize concern (COMP-008,
M4)" (dispatch.py:79); "M4 normalize / M5 reduce will [...]" (dispatch.py:491). The inline
no-`prompt` call means workers receive an empty prompt body (dispatch.py:382-386 default
`prompt: str = ""`).

### Contrast: the resume path IS fully wired

`_run_resume_branch` (commands.py:1714-end) runs dispatch (:1930) → `normalize_wave2` (:1952) →
`reduce_wave3(resume=True)` (:1977), which writes `merged.md` and `return-contract.yaml`
(reduce.py:594, :369). So the full pipeline exists and is reachable — just not from the inline
first-run path the thin caller would use.

---

## Net findings for the corrective tasklist (R2 scope)

**B-1 (CLI):** add `--reviewers`/`--workers <N>` to `run_cmd`, applied to `spec_dict.workers.count`
(override `lens.default_workers`). Mirror legacy [2,4] validation or document the divergence.
Anchor: commands.py:1304-1454; bare_review.py:61.

**B-2 (CLI):** add `--target-line-cap <N>`, applied to `spec_dict.target.truncation.line_cap`.
Beware preflight's 4000/≤0 override (preflight.py:527-528). Anchor: commands.py:817.

**B-3 (CLI):** add `--timeout-sec <N>`, applied to `spec_dict.workers.timeout_sec` AND threaded
into `dispatch_wave1(worker_spec=...)`. Anchor: commands.py:789, dispatch.py:341, :393.

**B-4 (CLI):** add `--label <str>`, applied to `spec_dict.caller.invocation_label` and surfaced as
`caller_label` in recipe args. Anchor: commands.py:775, bare_review_v1.py:255.

**B-5 (PIPELINE, HEADLINE):** wire the inline `run_cmd` path to run the full Wave 1→2→3 pipeline:
pass an assembled `prompt` + `worker_spec` to `dispatch_wave1`, then call `normalize_wave2` (recipe
`bare-review-v1`) and `reduce_wave3` → `emit_contract`, so `merged.md` + `return-contract.yaml` +
normalized bodies actually land. Without this, `swarm run --lens bare-review` is NOT a functional
replacement for `t2_dispatch.sh` + `t2_normalize.py`. Anchor: commands.py:1554-1578 (the stub);
working reference: commands.py:1930-1977 (resume path).

The lens entry (§2) and recipe (§3) are correct and need no change.
