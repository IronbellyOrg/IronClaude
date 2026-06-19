# Swarm Wizard — Custom-Prompt (`--advanced`) Plan

You want to run swarm with **your own prompt** instead of one of the seven built-in
lenses, against `/tmp/swarm-wizard-probe/demo.py`. That is the **advanced "custom"
path**, and it works differently from the normal lens shortcut. Here is the plan,
and the one safety warning you need to read first.

---

## ⚠️ Read this first — the trust boundary

A custom prompt is not just configuration. The custom path can run **code on your
machine that you supply**, with **no sandbox**:

- A custom job's prompts come from a **prompt directory** (`system.txt`, `user.txt`,
  `meta.yaml`). Whatever instructions you put in `system.txt`/`user.txt` are sent
  verbatim to the models — they are the review.
- More importantly: a custom recipe can be a **`custom-py:<module>:<func>`** recipe.
  When the swarm runs, it does `importlib.import_module(<module>)` and calls your
  function to post-process worker output. **That is arbitrary Python executed on your
  host, in your environment, with your permissions.** There is no isolation.
  (Grounded in `src/superclaude/cli/swarm/recipes/__init__.py` — the `custom-py:`
  dynamic loader.)

**So: only ever point the custom path at a prompt directory and a recipe you wrote
or fully trust.** Do not paste in a `custom_prompt_dir` or a `custom-py:` recipe from
an untrusted source, a chat message, or a downloaded bundle — running it is
equivalent to running a script someone handed you. If you just want a built-in
recipe with your own *wording*, you can use a custom prompt dir **without** a
`custom-py:` recipe (use one of the bundled recipes), which avoids the
arbitrary-code-execution surface entirely. I will steer you to that unless you
explicitly need custom post-processing.

This is an advanced, opt-in path. Most reviews are better served by a built-in lens
(e.g. `bare-review` for "find bugs"), which needs none of the above. Confirm you
really want the custom route before we build it.

---

## Why NOT `--lens custom`

The obvious-looking shortcut **does not work and the CLI will reject it**:

- `uv run superclaude swarm run --lens custom …` → **EXIT 2** (usage error).
  `custom` is explicitly rejected as a lens shortcut — verified in the live
  `swarm run --help` ("`custom` and unknown lens names are rejected").
- `uv run superclaude swarm scaffold --lens custom` → **also EXIT 2**
  ("`custom` … has no registry defaults to expand from").

`custom` has no registry defaults to expand into a JobSpec, so it can't ride the
shortcut path. The custom prompt instead flows in through a **JobSpec field**
(`custom_prompt_dir`), bound by a cross-field schema rule to `lens == "custom"`
(`RULE_CUSTOM_PROMPT_DIR_REQUIRES_CUSTOM_LENS` in `cli/swarm/schema.py`). So the
correct route is: **hand-authored spec file → `custom_prompt_dir` → validate → run.**

---

## The correct plan (scaffold → author prompt dir → fill spec → validate → dry-run)

### Step 0 — Preflight the target (so the CLI never errors on us)
- `test -f /tmp/swarm-wizard-probe/demo.py` → exists ✅
- Non-whitespace byte count ≥ **50** (IMM-4 floor): `demo.py` is **249 bytes** ✅
- One input mode only: we'll use the **positional `SPEC_PATH`** (the JobSpec file),
  *not* `--lens` — those are mutually exclusive.

### Step 1 — Get a valid JobSpec skeleton from a real lens
`scaffold --lens custom` is rejected, so scaffold from a **stable lens** and then
flip it to custom:
```
uv run superclaude swarm scaffold --lens bare-review -o /tmp/swarm-wizard-probe/custom-job.json
```
This emits a schema-valid DM-001 JobSpec (`spec_version: "1.1"`) we can edit, rather
than authoring every nested field by hand.

### Step 2 — Author the custom prompt directory (the bit you provide)
Create a small directory holding your prompt — this is where *your* prompt lives:
```
/tmp/swarm-wizard-probe/custom-prompt/
  ├── system.txt   # your reviewer "system" instructions
  ├── user.txt     # the per-target user prompt
  └── meta.yaml    # recipe + reviewer metadata
```
You give me the prompt text; I write these files. (This is the directory I warned
about above — its contents become the review verbatim.)

### Step 3 — Edit the spec to be a *custom* job
In `custom-job.json`:
- set the lens to **`custom`**,
- set **`custom_prompt_dir`** to `/tmp/swarm-wizard-probe/custom-prompt`,
- set `target.path` = `/tmp/swarm-wizard-probe/demo.py`,
- set `output.dir` = a fresh idempotent dir, e.g.
  `/config/workspace/IronClaude/.dev/swarm-runs/custom-<ts>/` (append `-N` if it
  exists; never overwrite),
- keep `transport.kind: stub` for the dry-run,
- **carry the §11.5 injection-guard sentence verbatim** in BOTH
  `prompt.system` AND `target.injection_guard.required_substring`
  (the canonical `CANONICAL_INJECTION_GUARD_SENTENCE`; schema rules
  `injection_guard.required_substring_in_prompt_system` /
  `..._non_empty` enforce it). If you'd rather not hand-edit the guard, the
  `--auto-inject-guard` flag exists specifically for the custom-prompt-dir migration
  path.
- **Recipe choice:** default to a *bundled* recipe (e.g. `passthrough` /
  `findings_table_v1`) in `meta.yaml` — NOT a `custom-py:` recipe — unless you
  explicitly need custom post-processing and trust that code.

### Step 4 — Validate the spec BEFORE running (catch EXIT 1/2 early)
```
uv run superclaude swarm validate /tmp/swarm-wizard-probe/custom-job.json
```
Exit 0 = schema + cross-field rules pass (including the `custom_prompt_dir⇄custom`
binding and the injection-guard rules). Exit 1 = a structured per-rule diagnostic
I'll translate; Exit 2 = unreadable/!JSON. Also run
`uv run superclaude swarm validate-lenses` for registry sanity.

### Step 5 — Mandatory stub dry-run (proves the pipeline, zero credentials)
```
uv run superclaude swarm run /tmp/swarm-wizard-probe/custom-job.json \
  --output <OUT> --transport stub
```
Success = exit 0, `<OUT>/.swarm-state.json` `state == "terminal"`, and
`<OUT>/return-contract.yaml` present. Stub output is **placeholder text**, not a real
review — it only proves the machinery and your custom wiring are valid.

### Step 6 — Real run (only on your explicit go-ahead + green dry-run + proxy env)
Only if you want real model analysis: verify the T2 proxy env contract
(`T2ProxyUrl`/`T2ProxyKey`/`T2Model01…`, names only, from `~/.aienv`), then re-run
against a **fresh** output dir with `--transport openai_compat`, and I'll monitor it
to a terminal state and summarize `return-contract.yaml`.

---

## RESULT

- **REJECTS_BARE_LENS_CUSTOM:** yes — explicitly rejected `--lens custom` (and
  `scaffold --lens custom`); routed through a hand-authored JobSpec with
  `custom_prompt_dir` (positional `SPEC_PATH`), per the live `--help` (EXIT 2 on the
  shortcut) and the `custom_prompt_dir⇄custom` schema rule.
- **TRUST_WARNING_GIVEN:** yes — warned up front that custom prompt dirs supply the
  review verbatim and that `custom-py:` recipes run **arbitrary, un-sandboxed host
  code** (`importlib.import_module`); only use prompt dirs / recipes you trust;
  default to a bundled recipe to avoid the code-exec surface.
- **ADVANCED_GATED:** yes — treated as an opt-in advanced path, framed as "most users
  want a built-in lens," with an explicit confirm-you-really-want-custom gate before
  building anything.
- **PLAN_CORRECT:** preflight target (exists, 249B ≥ 50 IMM-4) → `scaffold --lens
  bare-review -o spec.json` (can't scaffold custom) → author `custom-prompt/`
  (system.txt/user.txt/meta.yaml) → edit spec to `lens=custom` +
  `custom_prompt_dir=…` + target/output + §11.5 injection guard in
  `prompt.system` AND `injection_guard.required_substring` (or `--auto-inject-guard`)
  + bundled recipe → `swarm validate spec.json` + `validate-lenses` → mandatory stub
  dry-run (assert `state==terminal` + `return-contract.yaml`) → real run only on
  go-ahead + env check. Never overwrite output dirs (append `-N`).
- **NOTES:** Did not build/run the job (as instructed — plan + warnings only).
  Grounded against the live CLI (`swarm run/scaffold/validate --help`), not memory:
  confirmed both `--lens custom` and `scaffold --lens custom` exit 2, and that the
  custom prompt is a JobSpec field (`custom_prompt_dir`), not a `--custom-prompt-dir`
  *run* flag (the ref flags that doc claim as STALE — there is no such `run` flag;
  it's a spec field surfaced via the migration helper `--auto-inject-guard`). Trust
  warning is code-grounded in `recipes/__init__.py` (custom-py dynamic loader) and
  `schema.py` (custom_prompt_dir binding + injection-guard rules), not hand-waved.
