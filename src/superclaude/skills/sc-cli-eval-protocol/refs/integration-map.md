# Ref: Integration Map (exact reuse-invocation syntax)

The create pipeline REUSES three existing components. Do not reimplement them. Confirm the exact flag
spelling against each command's own file if anything below looks stale (they are the source of truth):
`src/superclaude/commands/{spec-panel,adversarial,document}.md`.

**Invocation form matters.** `adversarial` has a backing protocol skill, so invoke it via the **Skill**
tool (`Skill sc:adversarial-protocol`). `spec-panel` and `document` are **command-only** (their
protocol is inline in the command file — there is no `sc:spec-panel` / `sc:document` skill), so invoke
them as **commands** (`/sc:spec-panel …`, `/sc:document …`), NOT via the `Skill` tool.

## /sc:spec-panel — multi-expert critique (create W2)

```text
/sc:spec-panel @<design-spec>.md --mode critique --focus requirements,architecture
```

- `--mode`: `discussion | critique | socratic` (use `critique` to pressure-test the eval design).
- `--focus`: comma-separated areas, e.g. `requirements,architecture,testing,correctness`.
- Accepts `@file`. Returns an improved/annotated spec — fold it back into `<stem>-spec.md`.

## /sc:adversarial — debate / merge (create W3)

Backed by `Skill sc:adversarial-protocol`, agents `debate-orchestrator` + `merge-executor`.

**Mode A — compare existing variants you wrote:**

```text
Skill sc:adversarial-protocol
  --compare designA.md,designB.md,designC.md [--depth standard|deep] [--focus ...]
```

2-10 files. Produces diff-analysis, debate-transcript, base-selection, refactor-plan, merge-log,
merged-output.

**Mode B — generate variants from the spec, then merge:**

```text
Skill sc:adversarial-protocol
  --source <stem>-spec.md --generate eval-suite --agents opus,sonnet,haiku
```

`--agents` are `model[:persona[:"instruction"]]` specs. Use Mode B when you want the harness to
generate the competing designs; Mode A when you already have them.

## /sc:document — docs update (create W6)

```text
/sc:document docs/eval/suites-guide.md --type guide
```

Or delegate to the `technical-writer` agent for the inventory-table edits. Targets:

- `docs/eval/suites-guide.md` inventory table.
- `src/superclaude/cli/eval/suites/README.md` "What lives in this directory" table.

## evidence-validator (create W6, optional)

Task the `evidence-validator` agent over the doc edits to confirm every `file:line` cite resolves and
no unfounded claim slipped in. Read-only; drops/【flags unfounded items.

## Notes on nesting (important when testing in a subagent)

`/sc:spec-panel` and `/sc:adversarial` themselves fan out to sub-agents. An Agent-tool subagent
generally cannot nest that fan-out — if this protocol runs inside a subagent, those steps degrade to
"describe what would run" rather than truly executing. Run the create pipeline top-level (in the main
session) for the full effect; the run pipeline's CLI subprocesses work fine inside a subagent.
