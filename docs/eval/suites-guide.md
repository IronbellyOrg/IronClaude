# cliEval Suites — User Guide

This guide documents every eval suite created in this session — what each
tests, when to run it, the exact CLI invocation, and known caveats. It is
written for an operator new to the cliEval framework.

## What is a "suite"?

A **suite** is a YAML manifest under `src/superclaude/cli/eval/suites/`
that the cliEval CLI discovers, validates against `suite.schema.json`, and
runs through the vendored PTY harness. Each suite contains one or more
**evals**; each eval spawns its own Claude Code process inside a
per-eval isolated HOME, drives it through a series of prompts, and asserts
on output files / stdout / exit code.

See `docs/eval/runtime.md` for the 10-minute baseline budget and
`src/superclaude/cli/eval/suites/README.md` for filename rules.

## Quick start — three commands you need

```bash
# 1. Discover all suites the CLI sees (validates schema on the way)
uv run superclaude eval list --json

# 2. Inspect a specific suite's structure before running it
uv run superclaude eval describe --suite <name>

# 3. Run a suite. --no-pty + --no-mcp is the safest dry-run shape
uv run superclaude eval run --suite <name> --no-pty --no-mcp --json
```

**Important preflight:** the FR-G5 coverage gate checks
`~/.claude/settings.json` matchers against the running suite. If a suite
doesn't cover every PostToolUse / PreToolUse matcher in your home
settings, the gate exits 2 with `coverage gate FAILED`. Workarounds for
each suite below; see also §"Troubleshooting".

## Inventory at a glance

| # | Suite | Evals | Cadence | On disk? | Purpose |
|---|---|---|---|---|---|
| 1 | `model_capability_matrix` | 8 | Recurring nightly | ✓ | Compare model capability across 8 task categories |
| 2 | `frontier_vs_cheap_combo` | 4 | One-off / on-demand | ✓ | Frontier-vs-combo cost-quality A/B |
| 3 | `adversarial_merge_consistency` | 3 | Recurring weekly | ✓ | Inter-judge determinism of `/sc:adversarial` |
| 4 | `freshness_blocks_unread_edit` | 3 | One-off baseline | stash@{0} | Pre-edit freshness gate end-to-end |
| 5 | `task_classification_contract` | 2 | One-off baseline | stash@{0} | `/sc:task` first-output HTML marker |
| 6 | `audit_wiring_guard` | 2 | One-off baseline | stash@{0} | Audit pipeline never deletes wired files |
| 7 | `tasklist_deterministic_shape` | 1 | One-off baseline | stash@{0} | `/sc:tasklist` shape contract + renumbering |
| 8 | `eval_smoke` | 3 | One-off / smoke | stash@{0} | Meta-canary for the eval CLI itself |
| 9 | `installer_sync_drift` | 1 | Recurring CI/nightly | stash@{0} | `make verify-sync` doesn't regress |
| 10 | `hook_latency_drift` | 3 | Recurring nightly | stash@{0} | Hook telemetry schema + latency budgets |
| 11 | `agent_grounding_drift` | 2 | Recurring nightly | stash@{0} | Grounding agents drop bad citations |
| 12 | `eval_cli_doc_parity` | 3 | On-PR + nightly | ✓ | Documented `eval run` flags stay in sync with `--help` |
| 13 | `cli_eval_skill_contract` | 2 | On-PR + nightly | ✓ | `/sc:cli-eval` command + skill + agents stay wired |
| 14 | `suite_schema_guard` | 2 | On-PR + nightly | ✓ | Every `suites/*.yaml` still loads + schema-validates |

**Total: 37 evals across 14 suites.** (Suites #12–#14 ship with the `/sc:cli-eval` skill.)

### Restoring stashed suites

Eight suites (#4–#11) were generated on branch `chore/task-graduation` and
are preserved in `stash@{0}` (commit message
`pre-PR75-review WIP`). To bring them into the current working tree:

```bash
git stash apply stash@{0} -- src/superclaude/cli/eval/suites/
# OR (less surgical, brings everything in the stash):
git stash apply stash@{0}
```

`git stash apply` is non-destructive (the stash entry is preserved). Use
`git stash pop stash@{0}` only when you're done with the stash entry.

---

## Suite-by-suite reference

### 1. `model_capability_matrix.yaml` — nightly model-drift watchdog

**Hypothesis:** for any fixed task spec, the standardized hybrid scoring
in `/sc:adversarial` produces stable quant_score / qual_score across
model trios; meaningful changes indicate gateway regressions or model
swaps upstream.

**8 evals, one per capability category:**

| ID  | Category        | Seeded source                                              | Generate type |
|-----|-----------------|------------------------------------------------------------|---------------|
| MC1 | PLANNING        | URL shortener mini-spec                                    | roadmap       |
| MC2 | ARCHITECTURE    | Async job queue requirements                               | design        |
| MC3 | CODE_EXECUTION  | `parse_duration` signature + 3 tests                       | code          |
| MC4 | QA_DEBUGGING    | Threaded cache + average snippet (planted bugs)            | bug-report    |
| MC5 | BUG_FIXING      | Broken `safe_divide` + failing test                        | patch         |
| MC6 | REFACTORING     | Ugly order processor                                       | refactor      |
| MC7 | DOC_WRITING     | RateLimiter tech spec                                      | docs          |
| MC8 | TEST_DESIGN     | `merge_intervals` signature                                | tests         |

Each eval invokes `/sc:adversarial --source <seeded>.md --generate <type>
--agents opus,sonnet,haiku --output <home>/adv/ --depth standard` and
asserts on the five canonical adversarial artifacts (`diff-analysis.md`,
`debate-transcript.md`, `base-selection.md`, `refactor-plan.md`,
`merge-log.md`) plus the `quant_score` substring in `base-selection.md`.

**Sample invocation:**

```bash
# Full nightly run
uv run superclaude eval run --suite model_capability_matrix --no-mcp --json

# Just one category (e.g. only the code-execution eval)
uv run superclaude eval run --suite model_capability_matrix --eval MC3 --no-mcp

# Swap the model trio without editing the YAML
ANTHROPIC_DEFAULT_OPUS_MODEL=kimi-k2.5 \
ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-reasoner \
ANTHROPIC_DEFAULT_HAIKU_MODEL=qwen3-coder-plus \
  uv run superclaude eval run --suite model_capability_matrix --eval MC1 --no-mcp
```

**Cadence:** nightly drift watch. Each eval has `timeout_sec: 1800`; full
suite walltime ~8×30min = up to 4h serial, ~30min at `--parallel 8`.

---

### 2. `frontier_vs_cheap_combo.yaml` — on-demand cost-quality A/B

**Hypothesis:** for many tasks, three cheaper models merged via
`/sc:adversarial` reach equivalent or higher quant_score than a single
frontier model — at a fraction of the cost.

**4 evals, each runs TWO adversarial pipelines back-to-back:**

| ID  | Category       | RUN A (frontier)              | RUN B (cheap combo)              |
|-----|----------------|-------------------------------|----------------------------------|
| FC1 | PLANNING       | `--agents opus,opus,opus`     | `--agents sonnet,haiku,sonnet`   |
| FC2 | ARCHITECTURE   | `--agents opus,opus,opus`     | `--agents sonnet,haiku,sonnet`   |
| FC3 | CODE_QUALITY   | `--agents opus,opus,opus`     | `--agents sonnet,haiku,sonnet`   |
| FC4 | QA_DEBUGGING   | `--agents opus,opus,opus`     | `--agents sonnet,haiku,sonnet`   |

After both runs, a third prompt instructs Claude to read both
`base-selection.md` files and emit `comparison.md` containing both
`quant_score` and `qual_score` figures side-by-side.

**Sample invocation:**

```bash
# Run the whole quartet (long — ~50 min/eval, two adversarial pipelines each)
uv run superclaude eval run --suite frontier_vs_cheap_combo --no-mcp --json

# Just PLANNING — the cheapest entry
uv run superclaude eval run --suite frontier_vs_cheap_combo --eval FC1 --no-mcp
```

**Cadence:** on-demand. Run when re-evaluating the model rotation policy
or after major upstream model releases. `timeout_sec: 3000` per eval.

---

### 3. `adversarial_merge_consistency.yaml` — judge-determinism check

**Hypothesis:** given the same pair of divergent variants, three judging
trios (opus×3 / sonnet×3 / haiku×3) should select the same base variant
and produce quant_scores within a tight band.

**3 evals, each runs `/sc:adversarial --compare` 3 times** (varying the
judge model trio) and emits a `consistency-report.md`:

| ID  | Variant pair                                                           | Divergence axis tested |
|-----|------------------------------------------------------------------------|------------------------|
| AC1 | PLANNING — formal FR-IDs+tables vs prose narrative                     | RC, SR, SC             |
| AC2 | ARCH — concrete tech-stack tables vs abstract microservices prose      | DC, Risk, Structure    |
| AC3 | CODE — surgical file:line refactor vs sweeping pattern-language        | SR, Correctness        |

**Sample invocation:**

```bash
# Single-eval run on PLANNING variants — ~1h walltime
uv run superclaude eval run --suite adversarial_merge_consistency --eval AC1 --no-mcp

# Full weekly run (3h+ at --parallel 1, ~1.5h at --parallel 3)
uv run superclaude eval run --suite adversarial_merge_consistency --no-mcp --parallel 3
```

**Cadence:** weekly + on edits to `.claude/skills/sc-adversarial-protocol/**`.
`timeout_sec: 3600` per eval (three adversarial pipelines back-to-back).

---

### 4. `freshness_blocks_unread_edit.yaml` — pre-edit freshness gate

**Hypothesis:** `freshness-pre-edit.sh` denies Edit/Write on existing
files when no prior Read happened in the session, but allows new-file
Write and Edit-after-Read.

**3 evals:**

| ID | Title                                                       | Expected outcome |
|----|-------------------------------------------------------------|------------------|
| E1 | seeded existing file Edit without prior Read                | BLOCK (telemetry: decision=block, reason=no_prior_read) |
| E2 | Write to non-existent path                                  | ALLOW (telemetry: reason=create_allowed) |
| E3 | Read-then-Edit on seeded file                               | ALLOW (telemetry: reason=recent_read) |

Each asserts on the per-HOME `logs/freshness-hook.jsonl` file produced
by `freshness-pre-edit.sh:108-119`.

**Sample invocation:**

```bash
git stash apply stash@{0} -- src/superclaude/cli/eval/suites/freshness_blocks_unread_edit.yaml
uv run superclaude eval run --suite freshness_blocks_unread_edit --no-mcp
```

**Cadence:** one-off baseline. Re-run after touching
`src/superclaude/hooks/scripts/freshness-pre-edit.sh`.

---

### 5. `task_classification_contract.yaml` — `/sc:task` HTML marker

**Hypothesis:** `/sc:task <prompt>` emits the mandatory
`<!-- SC:TASK-UNIFIED:CLASSIFICATION -->` block as first output with a
valid TIER enum (STRICT for security-critical inputs, EXEMPT for
informational requests).

**2 evals:**

| ID | Input                                                    | Expected TIER |
|----|----------------------------------------------------------|---------------|
| E1 | `/sc:task "fix security vulnerability in auth module"`   | STRICT        |
| E2 | `/sc:task "explain how routing works"`                   | EXEMPT        |

Both assert on PTY-captured stdout containing the HTML marker and the
tier line.

**Sample invocation:**

```bash
git stash apply stash@{0} -- src/superclaude/cli/eval/suites/task_classification_contract.yaml
uv run superclaude eval run --suite task_classification_contract --no-mcp
```

**Cadence:** one-off baseline; re-run on edits to
`.claude/commands/sc/task.md` or `.claude/skills/sc-task-protocol/**`.

---

### 6. `audit_wiring_guard.yaml` — DELETE guard for live-wired code

**Hypothesis:** the audit pipeline (scanner → analyzer → validator →
consolidator) NEVER classifies a live-wired Python file as DELETE; it
must escalate to `REVIEW:wiring` and the analyzer profile must include
the 9th mandatory `Wiring path` field.

**2 evals:**

| ID | Pass                       | Asserted artifact                            |
|----|----------------------------|----------------------------------------------|
| E1 | Pass 1 — scanner           | `.claude-audit/pass1-summary.md` contains `wiring` for the fixture file (no DELETE) |
| E2 | Pass 2 — analyzer/validator | `.claude-audit/pass2-summary.md` contains `Wiring path` field |

Fixture seeded into HOME: a provider dir + `*_REGISTRY` dict + `Optional[Callable]=None` + live import chain (`app.py → registry.py → json_handler.py`).

**Sample invocation:**

```bash
git stash apply stash@{0} -- src/superclaude/cli/eval/suites/audit_wiring_guard.yaml
uv run superclaude eval run --suite audit_wiring_guard --no-mcp
```

**Cadence:** one-off; re-run after touching any audit agent prompt.
`timeout_sec: 300` per eval.

---

### 7. `tasklist_deterministic_shape.yaml` — `/sc:tasklist` shape contract

**Hypothesis:** the same seeded roadmap (with a deliberate Phase 1 → Phase 3
gap) produces a canonical Sprint-compatible bundle: `tasklist-index.md` +
sequentially-renumbered `phase-1-tasklist.md`, `phase-2-tasklist.md`
(NOT `phase-3-tasklist.md`), each ending with `Checkpoint: End of Phase`.

**1 eval (E1):** invokes `/sc:tasklist @<seeded>/roadmap.md` and asserts
on 8 file-shape predicates plus exit 0.

**Sample invocation:**

```bash
git stash apply stash@{0} -- src/superclaude/cli/eval/suites/tasklist_deterministic_shape.yaml
uv run superclaude eval run --suite tasklist_deterministic_shape --no-mcp
```

**Cadence:** one-off baseline; re-run on edits to
`.claude/skills/sc-tasklist-protocol/**`. `timeout_sec: 600` (LLM-heavy).

---

### 8. `eval_smoke.yaml` — meta-canary for the eval CLI itself

**Hypothesis:** the cliEval CLI's own `doctor` / `list` / `run` commands
work end-to-end and the report-artifact contract (summary.{md,json,yaml},
junit.xml) is preserved.

**3 evals:**

| ID  | Subcommand under test                                              |
|-----|---------------------------------------------------------------------|
| ES1 | `superclaude eval doctor --json --no-mcp`                          |
| ES2 | `superclaude eval list --json`                                     |
| ES3 | `superclaude eval run --suite real --no-pty --no-mcp --junit --json` |

All three evals carry `no_pty: skip` so the suite short-circuits cleanly
when run with `--no-pty` — useful as a CI canary that detects whether
the harness itself is broken before paying for a full run.

**Sample invocation (the E2E test from this session):**

```bash
git stash apply stash@{0} -- src/superclaude/cli/eval/suites/eval_smoke.yaml

# This is the actual E2E test that passed earlier — exit 0, 3 SKIPPED
TMPHOME=$(mktemp -d) && HOME=$TMPHOME uv run superclaude eval run \
  --suite eval_smoke --no-pty --no-mcp --json; \
  rm -rf "$TMPHOME"
```

The `TMPHOME` trick bypasses the FR-G5 coverage gate (see §"Troubleshooting"
below).

**Cadence:** one-off; CI smoke. `timeout_sec: 60-120` per eval.

---

### 9. `installer_sync_drift.yaml` — `make verify-sync` watch

**Hypothesis:** `make verify-sync` always exits 0 — meaning `src/` SoT and
`.claude/` generated copies remain aligned, the hook registration list
tracks scripts, and hooks.json matcher coverage stays current.

**1 eval (S1):** invokes `make verify-sync` via Bash. Assertions:
exit_code == 0 and stdout does NOT contain `drift detected` / `MISSING` /
`STALE` / `❌ DRIFT`.

Uses `home_strategy: shared` because verify-sync reads the actual repo
tree — ephemeral HOME would have no `src/` to compare against.

**Sample invocation:**

```bash
git stash apply stash@{0} -- src/superclaude/cli/eval/suites/installer_sync_drift.yaml
uv run superclaude eval run --suite installer_sync_drift --no-mcp
```

**Cadence:** on-PR (CI) + nightly. Lightweight enough to run frequently.

---

### 10. `hook_latency_drift.yaml` — hook telemetry schema watchdog

**Hypothesis:** for each wired hook in `src/superclaude/hooks/hooks.json`,
the live JSONL telemetry schema matches what the script emits today
(`event`, `tool`, `decision`, `session_id`, `ts_unix`, `tool_call_idx`,
`path`), and every hook completes within its declared timeout (binary
proxy: file presence + non-empty body).

**3 evals — one per hook family:**

| ID  | Hook family             | Asserted file                       |
|-----|-------------------------|--------------------------------------|
| HL1 | PreToolUse Edit/Write   | `logs/freshness-hook.jsonl`         |
| HL2 | PostToolUse Read async  | `state/reads.jsonl`                 |
| HL3 | UserPromptSubmit        | `logs/freshness-hook.jsonl`         |

**Differs from real.yaml E6/E9** — this suite asserts the
**currently-shipped** schema; real.yaml's E6-E11 assert the OQ-2-frozen
**future** contract. The drift between them is the early-warning signal.

**Sample invocation:**

```bash
git stash apply stash@{0} -- src/superclaude/cli/eval/suites/hook_latency_drift.yaml
uv run superclaude eval run --suite hook_latency_drift --no-mcp
```

**Cadence:** continuous (CI) + nightly cron.

---

### 11. `agent_grounding_drift.yaml` — grounding-agent meta-eval

**Hypothesis:** `evidence-validator` and `confidence-calibrator`
independently re-verify file:line citations; bad/fabricated citations
get dropped and the suggested status drops to `partial`.

**2 evals:**

| ID | Fixture                                              | Expected behavior |
|----|------------------------------------------------------|-------------------|
| G1 | Clean fixture (all citations resolve to real files) | `Dropped**: 0`; status hint present |
| G2 | Poisoned fixture (2 real + 3 fabricated paths)      | `file-missing` verdict; status `partial`; `## Dropped citations` section |

**Sample invocation:**

```bash
git stash apply stash@{0} -- src/superclaude/cli/eval/suites/agent_grounding_drift.yaml
uv run superclaude eval run --suite agent_grounding_drift --no-mcp
```

**Cadence:** nightly + on edits to `.claude/agents/evidence-validator.md`
or `.claude/agents/confidence-calibrator.md`.

---

## Cross-cutting workflows

### How to run any one eval, isolated

```bash
# --eval accepts the post-expansion id (e.g. MC3, E2.1, S1)
uv run superclaude eval run --suite <name> --eval <id> --no-mcp
```

Unknown ids exit 2 with `EvalNotFound`.

### How to swap models without editing YAML

The `opus`/`sonnet`/`haiku` aliases used in every suite that calls
`/sc:adversarial --agents ...` resolve through three env vars:

```bash
ANTHROPIC_DEFAULT_OPUS_MODEL=kimi-k2.5 \
ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-reasoner \
ANTHROPIC_DEFAULT_HAIKU_MODEL=qwen3-coder-plus \
  uv run superclaude eval run --suite model_capability_matrix --no-mcp
```

11 of the 12 models listed in `~/.bashrc` route successfully through the
LiteLLM gateway at `$ANTHROPIC_BASE_URL` (validated 2026-05-22). Two
exceptions:

- `gemini-3.1-pro-preview` — not registered on the gateway (HTTP 502
  `unknown provider`)
- `claude-opus-4-7[1m]` — the `[1m]` suffix is a Claude-Code-only
  client-side directive; pass bare `claude-opus-4-7` instead when used
  via raw `--agents`.

### Smaller / faster models per provider (haiku-tier alternatives)

The gateway exposes additional small/fast models from each provider —
useful as `haiku-equivalent` slots in the cost-quality comparison
suites (#1, #2, #3), as cheap drop-ins for `ANTHROPIC_DEFAULT_HAIKU_MODEL`,
or as raw `--agents <model>:<persona>` entries. Discoverable via:

```bash
curl -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  "$ANTHROPIC_BASE_URL/v1/models" | jq '.data[].id'
```

| Provider     | Haiku-tier model name                  | Notes |
|--------------|-----------------------------------------|-------|
| Anthropic    | `claude-haiku-4-5-20251001`            | Current Anthropic Haiku snapshot — natural drop-in for the `haiku` alias |
| OpenAI       | `gpt-5.4-mini`                         | Mini variant of GPT-5.4; fast text-only |
| Z.ai         | `glm-5-turbo`                          | Turbo / smaller GLM via Z.ai's Anthropic-compatible adapter |
| Mistral      | `mistralai/Mistral-Nemo-Instruct-2407` | Small Mistral Nemo via Deep Infra |
| Moonshot     | `kimi-k2.6`                            | Smaller / newer Kimi snapshot vs the `kimi-k2.5` in bashrc |
| QWEN Coder   | `qwen3-coder-next`                     | Coder-optimised next-gen Qwen smaller variant |
| Cerebras     | `llama3.1`                             | Cerebras-hosted Llama 3.1 — extremely fast inference, latency-sensitive evals |
| OpenAI (alt) | `gpt-codex-spark`                      | Codex spark variant — small, code-focused |

**Validation status:** these 8 are present in the gateway's
`/v1/models` enumeration (verified 2026-05-22) but were NOT individually
curl-tested in this session — unlike the 12 bashrc models. Before
including them in a recurring suite, smoke-test each:

```bash
for m in claude-haiku-4-5-20251001 gpt-5.4-mini glm-5-turbo \
         mistralai/Mistral-Nemo-Instruct-2407 kimi-k2.6 \
         qwen3-coder-next llama3.1 gpt-codex-spark; do
  echo "=== $m ==="
  curl -sS -m 30 -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
    "$ANTHROPIC_BASE_URL/v1/messages" \
    -d "{\"model\":\"$m\",\"max_tokens\":40,\"messages\":[{\"role\":\"user\",\"content\":\"Reply with just: HI\"}]}" \
    | jq -c '{model,stop_reason,error,text:.content[-1].text}'
done
```

If a model returns `stop_reason: max_tokens` with `text: null`, it is a
reasoning/thinking-tier model that consumes its budget on hidden
reasoning before emitting text — raise `max_tokens` to ~200 to see
output. Use only when reasoning depth (not latency) is the test goal.

**Example combos for `frontier_vs_cheap_combo`:**

```bash
# Anthropic-only tier (frontier vs all-haiku cheap combo):
ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-7 \
ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-6 \
ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5-20251001 \
  uv run superclaude eval run --suite frontier_vs_cheap_combo --eval FC1

# Cross-vendor cheap combo (Kimi + Mistral + Qwen):
ANTHROPIC_DEFAULT_OPUS_MODEL=kimi-k2.6 \
ANTHROPIC_DEFAULT_SONNET_MODEL=mistralai/Mistral-Nemo-Instruct-2407 \
ANTHROPIC_DEFAULT_HAIKU_MODEL=qwen3-coder-next \
  uv run superclaude eval run --suite frontier_vs_cheap_combo --eval FC1

# Latency-extreme: Cerebras llama3.1 as the haiku slot
ANTHROPIC_DEFAULT_HAIKU_MODEL=llama3.1 \
  uv run superclaude eval run --suite model_capability_matrix --eval MC3
```

### Where run artifacts land

`.dev/eval-runs/<YYYY-MM-DD>/<HHMMSSZ>-<run-id>/` contains:

- `summary.md` — operator-readable table
- `summary.json` — machine-readable, includes per-eval status/duration/skip_reason
- `summary.yaml` — same data, YAML form
- `junit.xml` — emitted only with `--junit`
- per-eval HOME directories (preserved on PASS only when
  `--keep-home` is set; preserved on FAIL by default for forensic
  inspection)

---

## Troubleshooting

### "coverage gate FAILED — uncovered matcher patterns" (exit 2)

The FR-G5 doctor preflight checks every PostToolUse / PreToolUse matcher
in your `~/.claude/settings.json` against the running suite's evals. If
the suite doesn't fire every matcher, exit 2.

Two workarounds:

```bash
# (a) Run with an empty HOME so settings.json has no matchers
TMPHOME=$(mktemp -d) && HOME=$TMPHOME uv run superclaude eval run \
  --suite <name> --no-mcp; rm -rf "$TMPHOME"

# (b) Compose your suite with real.yaml via --eval filtering
uv run superclaude eval run --suite real --eval E1,E2.1,E2.2,E2.3
```

Suites #5–#11 above (the targeted ones) all hit this gate when run
standalone against a populated home. `real.yaml` is the only suite that
covers every shipped matcher today.

### "--no-pty" skipped the whole suite

Every eval in suites #4–#11 carries `no_pty: skip` because they drive
Claude Code through the PTY. Running with `--no-pty` short-circuits all
of them to SKIPPED with `skip_reason="--no-pty"` and exit 0 — that's
expected behavior used by `eval_smoke` (#8) as a CI canary.

To actually exercise the evals, omit `--no-pty`.

### "Unknown model: `<name>`" from /sc:adversarial

The adversarial parser stops with this error when the model name doesn't
resolve. Three failure modes (in order of likelihood):

1. **Typo / unregistered alias** — check `~/.bashrc` and confirm
   `ANTHROPIC_DEFAULT_*_MODEL` is set to a model the gateway exposes
2. **Gateway doesn't have the model** — query
   `curl -sS -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN"
   "$ANTHROPIC_BASE_URL/v1/models" | jq '.data[].id'`
3. **Claude Code suffix** — `[1m]` doesn't survive past the CLI's local
   handler; strip it for raw `--agents` usage

### Eval timing out

Adversarial evals (#1, #2, #3) are LLM-heavy; bumping concurrency does
NOT speed them up because each `/sc:adversarial` invocation is itself
parallel internally. To debug:

```bash
# Bump per-eval timeout 2× without editing the YAML
uv run superclaude eval run --suite <name> --eval <id> --timeout-mult 2.0
```

If a single LLM call exceeds the per-eval budget, the per-eval HOME is
preserved on FAIL — `cd .dev/eval-runs/<run>/E<id>-HOME/` to inspect
the partial artifacts.

---

## Reference

- `docs/eval/runtime.md` — full-suite 600s budget contract (NFR-PERF3)
- `docs/eval/retry.md` — bounded retry policy for failing evals
- `docs/eval/validation-commands.md` — every CLI flag and exit code
- `src/superclaude/cli/eval/suites/README.md` — filename / `name:`
  rules and the planned `quick.yaml` follow-up
- `src/superclaude/cli/eval/suites/suite.schema.json` — full JSON schema
- `.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` —
  the hybrid quant_score formula used by suites #1–#3
- `.dev/eval-proposals/` — the 18 original proposals and the
  adversarial-debate ranking that selected suites #4–#11
