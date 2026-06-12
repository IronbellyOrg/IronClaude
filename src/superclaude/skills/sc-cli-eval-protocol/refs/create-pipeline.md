# Ref: CREATE Pipeline (full step detail)

Load this in the create branch after Wave 0. Pair with `refs/integration-map.md` (exact invocation
syntax) and `templates/suite-manifest.yaml` (schema-valid skeleton). All design artifacts go under
`.dev/eval-workspaces/cli-eval/design/`.

## W1 — Draft the design spec

Write `.dev/eval-workspaces/cli-eval/design/<stem>-spec.md` answering:

- **Guard target**: what behavior/contract does this suite protect? Why does it need a recurring eval?
- **Scenarios → evals**: each eval's id (FR-SCH2), title, the Claude prompt that drives it, and the
  `expects` assertions (stdout contains/not_contains, exit_code equals).
- **Isolation**: `ephemeral` (default), `shared` (eval must see the working tree, e.g. `make
  verify-sync`), or `seeded` (+ `seed_state` files).
- **Capabilities**: `required_binaries` (hard gates) and `optional_capabilities` (soft gates).
- **Cadence** (operator metadata, not enforced): on-PR, nightly, manual.
- **PTY**: PTY-driven evals carry `no_pty: skip`.
Ground every flag/schema claim in the Wave-0 digest, not memory.

## W2 — Critique (REUSE /sc:spec-panel)

Invoke the `/sc:spec-panel` command: `@<stem>-spec.md --mode critique --focus requirements,architecture`
(spec-panel is command-only — no `sc:spec-panel` skill; invoke the command, not a `Skill` call).
Fold findings into the spec. Record the panel output in the design dir. Do NOT build a review panel.

## W3 — Competing designs + debate/merge (REUSE /sc:adversarial)

Produce 2-3 genuinely different designs (vary scenarios / fixtures / assertion strategy / isolation /
cadence). Merge via `Skill sc:adversarial-protocol`:

- **Mode-B** (generate + merge): `--source <stem>-spec.md --generate eval-suite --agents <agents>`.
- **Mode-A** (you wrote the variants): `--compare designA.md,designB.md,designC.md`.
Keep the merged design + debate transcript. The merged design is the input to W4.

## W4 — Author schema-first (DELEGATE eval-suite-author)

Task the `eval-suite-author` agent with the merged design + the Wave-0 digest. It writes
`src/superclaude/cli/eval/suites/<stem>.yaml` in the house style and self-validates. Constraints it
must honor: stem == `name:`, snake_case, `.yaml`; only schema-known keys; meaningful assertions (not
just `exit_code: 0`); fixtures / `<stem>_callbacks.py` only if genuinely needed.

## W5 — Validate (done-ness gate)

```bash
uv run superclaude eval describe --suite <stem>   # loader exit 0 == schema-valid
uv run superclaude eval list --json | jq '.[] | select(.name=="<stem>")'   # discovered
```

On non-zero exit, hand the loader error back to W4 (max 3 fix loops), then report blocked. A suite is
NOT done until `eval describe` is green.

## W6 — Document (REUSE /sc:document)

- `docs/eval/suites-guide.md`: add the new suite to the inventory table (stem, eval_count, purpose).
- `src/superclaude/cli/eval/suites/README.md`: add a row to "What lives in this directory".
Use the `/sc:document` command or the `technical-writer` agent (document is command-only — invoke the
command, not a `Skill` call). Optionally run `evidence-validator` over the edits so every cite
resolves. Keep markdownlint (MD025) + yamllint (indent-sequences) happy.

## Completion criteria

- `eval describe --suite <stem>` exit 0 AND the suite appears in `eval list --json`.
- Docs updated in both inventory locations.
- Design artifacts + validation record under `.dev/eval-workspaces/cli-eval/`.
