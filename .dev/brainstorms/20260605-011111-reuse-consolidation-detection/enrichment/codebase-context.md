# Enrichment: Codebase Context (VERIFIED)

> Quality tier: **primary** (auggie `codebase-retrieval` + direct `Read` of
> cited line ranges + `grep`). Every claim below was independently
> re-verified this session — not taken from the prompt on faith.

## A. The concrete duplication case — CONFIRMED

### A.0 The new component (the duplicate that was built)

`src/superclaude/cli/prd/executor.py` (uncommitted `prd --spec` work in the
main tree, NOT yet at this worktree's HEAD):

- `_bind_specs(self, parsed: dict) -> dict` — **line 1196**
- `_persist_bound_specs(self) -> None` — **line 1245**, called at **line 480**
- Shape (verified at lines 1234, 1255, 1260): reads the persisted
  `parsed-request.json` artifact (`read_text`), **idempotently** prepends
  spec parent dirs (the inline comment at 1234 literally says
  *"dedup, order-preserving, idempotent"*), then rewrites
  (`write_text(json.dumps(bound, …))`).
- **This is the post-LLM artifact-injection pattern**: read persisted
  artifact → idempotency-check → inject what the LLM can't be trusted to
  produce (the bound spec paths) → rewrite.

### A.1 Prior art #1 — sibling pipeline (roadmap), SAME pattern

`src/superclaude/cli/roadmap/executor.py:678-752` — confirmed verbatim:

- `_inject_pipeline_diagnostics(output_file, started_at, finished_at)` —
  **line 678**. Body: `read_text` → `lstrip("\n\r\t ")` →
  `startswith("---")` guard → `find("\n---", 3)` → **idempotency check**
  (`if "pipeline_diagnostics:" in frontmatter: return`) → inject →
  `write_text`.
- `_inject_provenance_fields(output_file, spec_source)` — **line 715**.
  Identical skeleton, per-field idempotency
  (`if "spec_source:" not in frontmatter …`).
- **Note: these are already TWO copies of the same idiom in ONE file** —
  i.e. the duplication the heuristic must catch already exists *within*
  roadmap, before prd ever copied a third variant. This is itself an
  N=2-in-one-module consolidation candidate.
- Docstrings both state the rationale verbatim: *"The LLM cannot reliably
  produce … so the executor injects these fields post-subprocess."* —
  the shared capability is unmistakable.

### A.2 Prior art #2 — prd's OWN module, the file-binding mechanism

`src/superclaude/cli/prd/process.py:92-190` — confirmed verbatim:

- `_PHASE_ALLOWED_REFS: dict[str, list[str]]` — **line 95** (phase→refs map)
- `_FILE_SIZE_THRESHOLD = 50_000  # 50KB: inline vs --file cutoff` —
  **line 115**
- `PrdClaudeProcess._build_file_args(config, step_id)` — **line 163**:
  normalizes step_id, looks up allowed refs, passes files >50KB as
  `--file` args, inlines smaller ones.
- This is a **deterministic file-binding mechanism**. The planned Phase-2
  "inline-with-cap" work for `prd --spec` would reinvent the
  inline-vs-`--file` size cutoff that already lives here.

### A.3 The subtle constraint — CONFIRMED real, not laziness

`NFR-PRD.7` is enforced as a module-docstring invariant across the prd
package — confirmed present in **8 files**:
`prd/{executor,process,prompts,models,config,monitor,tui,diagnostics,logging_}.py`,
each carrying:

> `NFR-PRD.7: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.`

**Implication for the detector:** the roadmap `_inject_*` functions are
the closest prior art for `_bind_specs`, but prd **cannot import them**.
So the correct reuse verdict here is NOT "import roadmap's helper" — it is
either **mirror-shape** (name + structure `_bind_specs` after the
`_inject_*` family for cross-pipeline consistency) or **extract-shared**
(promote the read→idempotency→inject→rewrite skeleton into a
boundary-neutral module both pipelines may depend on, e.g.
`superclaude.cli.pipeline.*`). The detector MUST distinguish
`reuse-by-import` (forbidden here) from `mirror-shape` from
`extract-shared`.

## B. Integration surfaces — sc-reflect-protocol/SKILL.md (1797 lines)

| Anchor | Lines | Why it matters for this design |
|---|---|---|
| §6.1 Mandatory evidence-gathering chain (Wave 1A) | ~444-473 | Already an **auggie + serena symbolic chain**. The neighbour-search step is a natural *addition to this existing chain*, not a new system — dogfood the very heuristic. |
| §6.2 Citation-grounding via re-Read | ~492 | Anti-staleness re-Read already mandated → reuse for "X already does this at file:line" evidence. |
| §5 Tier-Decision Rubric | ~351-420 | Rule 3 already ESCALATES (blocks/debates) on a `Regression` candidate. A high-confidence Reuse Miss can hook the SAME escalation machinery. |
| §10 Deviation Taxonomy | 860-966 | §10.1 Authorized expansion / §10.2 Necessary deviation / §10.3 Drift / §10.4 Regression / §10.5 precedence / §10.6 Grounding Gaps / §10.7 Reporting. A **"Reuse Miss"** finding must slot in here (extend taxonomy or map onto Drift) rather than invent a parallel scheme (seed C6). |
| §14.5 promotion gate | ~1309 | `drift==0 AND regression==0` blocks promotion. Determines whether a Reuse Miss is blocking vs advisory. |
| §9 Output Contract (1.2.0) | ~633-650 | New finding type needs a contract field. |
| `--mode pre` vs `--mode post` | §3.2, lines 92-109 | pre = validate proposed strategy/tasklist (pre-build); post = audit completed work (pre/post split for seed SC5). |

**auggie is already an allowed tool** in sc-reflect (`allowed-tools` line 5
lists `mcp__auggie__codebase-retrieval`) → no new capability grant needed
for the mandatory neighbour-search step.

## C. Integration surfaces — tdd/SKILL.md (432 lines)

- **Phase structure** (lines 141-147): Phase 1 Preparation → Phase 2 Deep
  Investigation (parallel subagents read real source) → Phase 3
  Completeness Verification → Phase 4 Web Research → Phase 5 Synthesis →
  Phase 6 Assembly → Phase 7 Present.
- **`/tdd` is design-time / pre-build by nature.** Its agents already
  "read actual source files, trace actual architectures, document actual
  implementation patterns" (line 16) — so a **reuse audit** is an
  *extension of Phase 2's existing codebase investigation*, surfaced as a
  dedicated section in the Phase 5 synthesized TDD. Pre-stage = catch the
  duplicate *before* it is written.
- `/tdd` delegates to the `/task` MDTM loop; artifacts land in
  `.dev/tasks/to-do/TASK-TDD-*/`. A reuse-audit checklist item is the
  natural carrier.

## D. Design takeaways (for the 5 proposal agents)

1. **Pre vs post split is structural, not cosmetic.** `/tdd` and
   `sc:reflect --mode pre` operate on *intentions* (a proposed
   component/design) → evidence is "a neighbour already does this; model
   after it / don't build it." `sc:reflect --mode post` operates on
   *shipped code* → evidence is "this new symbol duplicates `file:line`;
   classify the deviation."
2. **Reuse verdict vocabulary** must be 4-valued:
   `reuse-by-import` | `mirror-shape` | `extract-shared` | `distinct` —
   and honour import bans (NFR-PRD.7-class constraints).
3. **The duplication is already N≥2 even inside roadmap** (`_inject_*` ×2)
   plus the prd third copy → a live test case for the consolidation
   threshold (OQ2).
4. **Reuse the existing chains** — auggie (§6.1) + re-Read (§6.2) in
   reflect; Phase-2 investigation in tdd — rather than bolting on a
   parallel search subsystem. Building a *new* detection subsystem when
   the search substrate already exists would itself be the anti-pattern
   this work exists to stop.
5. **False-positive guard** must be a real similarity signal
   (capability-tag + signature/skeleton shape + auggie semantic rank),
   not a name match — `validate_x` vs `validate_y` sharing a verb is
   `distinct`.
