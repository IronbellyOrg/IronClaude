# Recommendation: Build Tasklist from checkout-v2-spec.md

## Recommended Command

`/sc:tasklist` — the deterministic roadmap-to-tasklist generator that produces Sprint CLI-compatible multi-file bundles with integrated roadmap validation and `/sc:task` compliance tier integration.

## Framing

A tasklist is derived from a **roadmap**, not directly from a spec. The canonical SuperClaude pipeline is:

```
spec.md  →  /sc:roadmap  →  roadmap artifacts  →  /sc:tasklist  →  tasklist bundle  →  /sc:task (or superclaude sprint run)
```

Going spec → tasklist directly skips the roadmap-validation gate that `/sc:tasklist` expects as input. So the correct two-step approach is:

1. Generate the roadmap from the spec.
2. Generate the tasklist from the roadmap.

## Paste-Ready Prompts

**Step 1 — Generate roadmap from the spec:**

```
/sc:roadmap docs/specs/checkout-v2-spec.md
```

**Step 2 — Generate tasklist from the roadmap output directory** (replace `<roadmap-output-dir>` with the path emitted by step 1, typically under `docs/generated/` or `.dev/releases/`):

```
/sc:tasklist <roadmap-output-dir>
```

**Optional pre-flight** — if the spec itself needs a sanity check before roadmap generation:

```
/sc:validate-roadmap <roadmap-output-dir>
```

## Why This Approach

- `/sc:tasklist` is the **purpose-built** command for this request. Its protocol explicitly consumes roadmap artifacts and emits Sprint CLI-compatible bundles with `/sc:task` compliance tiers baked in — exactly the artifact a downstream task-execution loop needs.
- `/sc:roadmap` is the **required upstream step**. Its skill description says it "generates roadmap pipeline artifacts from 1-3 specification, TDD, and PRD markdown inputs" — i.e. it's the spec-consuming end of the pipeline.
- Skipping the roadmap stage and using `/task-builder` or `/sc:workflow` instead would either (a) produce a single MDTM task rather than a multi-task sprint bundle, or (b) skip the roadmap-validation gate that catches spec gaps before they propagate into per-task work.
- The two-step `/sc:roadmap` → `/sc:tasklist` chain matches the documented SuperClaude pipeline in `CLAUDE.md` (`superclaude roadmap run` → `superclaude sprint run <tasklist-index.md>`).

## Alternatives Considered

| Command | Why not primary |
|---|---|
| `/task-builder` | Builds a **single** MDTM task file, not a multi-task tasklist bundle. Use it for one focused deliverable, not a whole spec. |
| `/sc:workflow` | Generates implementation **workflows** from PRDs — narrower output than a Sprint-compatible tasklist; no roadmap-validation gate. |
| `/sc:task` directly | Executes tasks; it does not generate the tasklist artifact from a spec. Runs **after** `/sc:tasklist`. |
| `/sc:implement` | Jumps straight to code. Skips planning, validation, and task decomposition entirely — wrong altitude for a spec-sized input. |

## Expected Outputs

- **From `/sc:roadmap`**: roadmap pipeline artifacts (roadmap.md, validation report, source-enrichment data) under a generated output directory.
- **From `/sc:tasklist`**: a Sprint CLI-compatible bundle containing `tasklist-index.md` plus per-task MDTM files, ready for `superclaude sprint run <tasklist-index.md>` or interactive `/sc:task` execution.
