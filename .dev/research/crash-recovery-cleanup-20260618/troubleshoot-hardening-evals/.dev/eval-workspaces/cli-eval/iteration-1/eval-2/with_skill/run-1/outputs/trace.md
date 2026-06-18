# Trace — create `eval_cli_doc_parity` suite (with_skill)

Pipeline: `/sc:cli-eval create` (skill `sc:cli-eval-protocol`). Subagent run; the
nesting-limited steps (`/sc:spec-panel`, `/sc:adversarial`) are described, not
executed (cannot fan out further from a subagent).

## Wave 0 — Mandatory fresh-context load (CITED)

Re-read the live contract surface before authoring (no reasoning from memory):

1. `src/superclaude/commands/cli-eval.md` — command shape, create pipeline steps,
   `--name` must equal `name:`.
2. `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md` — W1..W6 create flow;
   done-ness = `eval describe` exit 0 + appears in `eval list --json`; only
   schema-known keys; meaningful assertions (not just exit_code 0).
3. `refs/create-pipeline.md` — per-step detail; design artifacts under
   `.dev/eval-workspaces/cli-eval/design/`.
4. `refs/eval-contracts.md` — reading-aid map (digest is authority).
5. `src/superclaude/cli/eval/suites/suite.schema.json` — top-level required:
   name, version, description, defaults, required_binaries, optional_capabilities,
   evals; `additionalProperties:false`. eval entry requires `id`+`title`; optional
   `category/requires/timeout_sec/isolation/inputs/expects/parameterize/no_pty`.
   id regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`; version regex
   `^[0-9]+\.[0-9]+(\.[0-9]+)?$`; `no_pty` enum only `"skip"`;
   `isolation.home_strategy` ∈ {ephemeral,seeded,shared}.
6. `src/superclaude/cli/eval/suites/eval_smoke.yaml` — house style: `inputs[].prompt`
   carries the Claude prompt; `expects[]` is a list of single-key objects
   (`{stdout:{contains:...}}`, `{exit_code:{equals:0}}`); `# yaml-language-server`
   schema header line; `no_pty: skip` per entry.
7. `src/superclaude/cli/eval/suites/installer_sync_drift.yaml` — house style:
   `inputs[].prompt` + optional `expect_tool_call: Bash`; `expects[]` supports
   `{stdout:{not_contains:...}}`; CADENCE/WHAT/WHY comment headers.
8. `src/superclaude/cli/eval/suites/README.md` — filename rules: `.yaml`,
   snake_case stem, stem == `name:`.

### Live CLI surface (load-bearing — the parity contract guards THIS)

Command: `timeout 180 uv run superclaude eval run --help`  → **EXIT=0**
Enumerated exactly twelve options (the documented FR-CLI1 set):
`--suite` (required), `--parallel`, `--eval`, `--no-mcp`, `--no-pty`,
`--output-dir`, `--keep-home`, `--timeout-mult`, `--max-disk-mb`, `--json`,
`--verbose`, `--junit`. Docstring text: "the twelve FR-CLI1 flags". `--suite`
rendered with the `[required]` marker.

Command: `grep ... commands.py` (option block) — confirmed the options are real
Click options on the `eval run` group, not prose.

Supporting docs grep: `docs/eval/suites-guide.md` references the same flags
(`--suite`, `--no-pty`, `--no-mcp`, `--json`, `--keep-home`, `--timeout-mult`,
`--max-disk-mb`, `--eval`, `--parallel`) — confirms these are the *documented*
surface the eval must keep in sync.

## W1 — Design spec
Wrote `.dev/eval-workspaces/cli-eval/design/eval_cli_doc_parity-spec.md` (guard
target, scenarios→evals DP1/DP2/DP3, ephemeral isolation, capabilities, cadence,
assertion strategy, Wave-0 citations).

## W2 — Critique (DESCRIBED — nesting limit)
Would invoke: `Skill sc:spec-panel @eval_cli_doc_parity-spec.md --mode critique
--focus requirements,architecture`. Expected critique + folded resolution:
substring-on-long-name could match prose → mitigated by DP3's `[required]` guard
(only appears on a genuine required option); DP1/DP2 split kept for failure
localization; substring on `--flag` tokens is stable across Click/rich-click
reflows. Folded in: keep split + DP3.

## W3 — Competing designs + debate/merge (DESCRIBED — nesting limit)
Would invoke: `Skill sc:adversarial-protocol --source eval_cli_doc_parity-spec.md
--generate eval-suite --agents opus,sonnet,haiku`. Three variants:
(A) single eval, all 12 flags in one contains chain — loses localization;
(B) 3-eval split DP1/DP2/DP3 — failure-localizing + `[required]` contract guard;
(C) parameterize one-eval-per-flag (12 expanded) — verbose, FR-SCH2 id-regex risk
on generated ids. Merge verdict: **B** (chosen). Proceeded with B.

## W4 — Author schema-first
Wrote `src/superclaude/cli/eval/suites/eval_cli_doc_parity.yaml`. stem == `name:`
== `eval_cli_doc_parity`. Only schema-known keys. Three evals (DP1/DP2/DP3) each
drive `superclaude eval run --help` via Bash and assert documented flags present;
`expect_tool_call: Bash`; `no_pty: skip`; `home_strategy: ephemeral`.

## W5 — Validate (done-ness gate)

Command: `timeout 180 uv run superclaude eval describe --suite eval_cli_doc_parity`
→ **EXIT=0** (rendered the full validated manifest; loader accepted it).

Command: `timeout 180 uv run superclaude eval list --json | <filter>`
→ **EXIT=0**, suite discovered: `{"name":"eval_cli_doc_parity","version":"1.0","eval_count":3}`.

Both halves of the done-ness gate pass. No fix loop needed (validated on first
author pass).

## W6 — Document (NOT executed)
Out of scope for this subagent run (task said: do not touch other source files;
deliverable is the suite + validation). Docs inventory updates
(`docs/eval/suites-guide.md`, `suites/README.md`) noted as the follow-up the full
create pipeline performs.

## Outputs written
- `eval_cli_doc_parity.yaml` (copy of the authored manifest)
- `trace.md` (this file)
- `report.md` (final answer)
- Source deliverable: `src/superclaude/cli/eval/suites/eval_cli_doc_parity.yaml`
- Design spec: `.dev/eval-workspaces/cli-eval/design/eval_cli_doc_parity-spec.md`
