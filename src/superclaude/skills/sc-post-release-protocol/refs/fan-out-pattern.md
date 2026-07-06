# Fan-Out / Agent-Team Pattern

Every workstream uses the same three-role team: **scanners → consolidator → writers.** This pattern exists to solve two problems at once — going *deep* across a large surface without any single agent drowning in context, and *gating* all file creation behind a reviewed plan so nothing gets written from a half-formed picture.

## The three roles

### 1. Scanners (read-only, parallel)

Partition the workstream's surface into non-overlapping slices — by directory (`docs/user-guide/`, `docs/reference/`, …) or by feature area (the `sprint` command, the `roadmap` pipeline, …). Spawn one scanner per slice, **in a single message**, so they run concurrently.

- **Tooling:** read/grep/glob only. Scanners must not write source, docs, or scripts. Read-only is what makes parallelism safe — no two scanners can conflict, and none can mutate the repo you're still auditing.
- **Output:** each scanner returns a structured inventory of its slice — what exists, what each artifact covers, and where a claim diverges from the code (with file:line evidence). Have scanners write their inventory to a working file (e.g. under the run's scratch dir) rather than only returning it in context, so findings survive compaction.
- **Count:** scale to the surface. A handful of docs → 2–3 scanners; a large multi-subtree surface → 5–8. Each scanner is told what the others cover so they don't overlap.

### 2. Consolidator

One agent (or the orchestrator inline, for small surfaces) merges the scanner inventories into the two artifacts that gate everything downstream:

- **Coverage matrix** — rows are the release's features/capabilities, columns are the artifacts that should cover them (doc / guide / script). Each cell: `present-and-current`, `present-but-stale`, or `missing`.
- **Gap list** — every `missing` / `present-but-stale` cell, each with the evidence for its verdict and (where useful) a proposed remedy.

The consolidator dedups (two scanners may both mention a shared file) and resolves conflicts (one says current, one says stale → re-check against code). **Nothing is created or edited until this consolidation exists** — it's the plan the writers work from.

### 3. Writers / creators

Each writer takes **one** consolidated, approved item (update this stale doc; create this missing guide) and produces exactly that artifact. Writers can run in parallel too, but only after the plan is set.

- For **light** workstreams (a few edits), the orchestrator can write directly.
- For **heavy / creation-dense** workstreams (many new guides or docs), route the writers through an itemized tasklist and execution loop (the project's task tooling if it has one) instead of free-handing them. That gives each created artifact its own checklist item, research backing, and QA gate — the same evidence discipline the rest of the skill runs on. See the controller-behavior section in SKILL.md.

## Isolation & safety

- Scanners parallelize freely (read-only, no conflicts).
- Writers that touch **different** files parallelize freely. Writers that might touch the **same** file (e.g. two features documented in one README) must be serialized, or given disjoint sections, to avoid clobbering each other. When in doubt, serialize edits to a shared file.
- If a workstream's writers run as parallel repo-mutating agents and could collide, prefer a git worktree per writer (in whatever location the host repo uses for worktrees) or serialize them.

## Why not just do it in one pass?

A single agent scanning-and-writing the whole surface will (a) run out of context and start summarizing instead of reading, (b) begin writing before it has the full picture, and (c) produce no reviewable plan between "what's there" and "what I changed." The three-role split keeps each agent's job small enough to do from real evidence, and puts a human-inspectable coverage matrix + gap list at the exact seam where mistakes would otherwise slip through.
