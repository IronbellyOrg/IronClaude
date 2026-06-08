# HUMAN DECISION REQUIRED — Python-vs-skill-prose boundary (HARD-HALT)

**Status:** ✅ **RESOLVED: Option P (Python-heavy / thin Haiku)** — operator selection on 2026-06-03.
**Gates:** Phase 4 (hot/cold dispatch wiring) and Phase 5 (`--eval` pipeline + plugin eval gate) are now UNBLOCKED and implemented per Option P. See `boundary-resolved.md` for the concrete layering.
**Task:** TASK-RF-20260603-032936
**Date raised:** 2026-06-03

---

## The question

Which layer owns the **classify → dispatch → validate → commit** flow of the
sc-recommend lookup-cache hot/cold path — **skill prose** (`sc-recommend/SKILL.md`,
orchestrating via the Agent tool) or the **Python CLI module**
(`src/superclaude/cli/recommend/`)?

The dispatch-wiring (Phase 4) and `--eval` (Phase 5) phases **cannot be written
coherently** without this answer, because the *location* of dispatch logic
determines what code is written and where.

## Why it is genuinely undecided (the crux)

Per `research/04 §4.4` and `research/07 D2`, the spec contains a real internal tension:

- **Spec line 113** inlines the cache table *into the Haiku prompt* → leans toward
  the Haiku subagent doing the table scan / key-match / top-2-delta in-context (prose).
- **Spec line 414** frames dispatch as **~150 LoC parent code** → leans toward a
  Python dispatch layer.

Three hard constraints (research/07 D2) make "the parent does it" non-trivial:

- **Constraint A:** the `anthropic` SDK is **BANNED** (`pyproject.toml:208-211`, ruff
  `flake8-tidy-imports.banned-api`) → no in-process model calls; all model runs are
  subprocess/Agent-based.
- **Constraint B:** Agent-tool spawning (`model: haiku`) is **Claude-session-only**
  (skill prose) — the CLI cannot spawn Agent subagents.
- **Constraint C:** atomic YAML write + sha256 + JSONL append + eval aggregation are
  **deterministic Python**; "Haiku cannot write files" is stated **twice** in the spec
  (lines 133, 170) → the parent (Claude session) must commit via the CLI helpers.

So "the parent" cannot trivially be *both* the Agent-spawner (Claude) *and* the
file-committer (CLI). The operator must pick the layering.

---

## Option H — Haiku-heavy / thin parent

`SKILL.md` orchestrates everything via the Agent tool. The `cli/recommend/` module is
a **thin library of pure deterministic helpers** (cache read/write, sha256, telemetry,
eval aggregate) that the *skill* invokes via
`Bash(uv run python -m superclaude.cli.recommend ...)` between Agent calls. Dispatch
logic (classify → scan → match → delta → native-decision → prompt-build) lives in
**skill prose**, with the cache table inlined into the Haiku prompt.

- **Spec mapping:** line 113 ("inline table into Haiku prompt").
- **Pros:** lowest LoC; faithful to sc-recommend's prose-driven skill nature; the
  table-scan + delta-gate are zero-marginal-cost in-prompt once the table is inlined.
- **Risk:** sha256 validation must still be parent-side (Haiku cannot be trusted to
  hash), so hot-path step 6 splits awkwardly across the Haiku/parent boundary mid-flow.

## Option P — Python-heavy / thin Haiku

A `cli/recommend/` CLI subcommand owns **classify-dispatch-validate-commit as ~150 LoC**.
The skill is a thin wrapper that shells to it and only spawns Agents for the cold-path
LLM work (and, given Constraint B, for classification — since the CLI itself cannot
spawn the Haiku classifier).

- **Spec mapping:** line 414 ("~150 LoC parent code").
- **Pros:** cleaner determinism; easiest to unit-test; matches the ~700 LoC framing.
- **Risk:** the table is then NOT needed inlined in the hot-path classifier prompt
  (contradicts line 113); you pay a parent↔Haiku round-trip to get the key before
  scanning; and Constraint B means the CLI still cannot own the Agent spawn, so the
  "CLI owns dispatch" framing is partly fictional under the anthropic ban.

## Option Hybrid — skill owns orchestration + dispatch; CLI owns deterministic ops (RECOMMENDED)

The skill owns **Agent orchestration + dispatch decisions**; the CLI owns **ONLY the
deterministic file/eval operations** as discrete subcommands (`cache get/put`,
`telemetry append`, `eval run`). This is the most faithful reading of "Haiku cannot
write files" + the anthropic-SDK ban (Constraints A–C).

- **Spec mapping:** not explicitly stated — but it is the only option that simultaneously
  honors line-113 inlining (dispatch in prose), Constraint B (skill owns the Agent spawn),
  and Constraint C (CLI owns the writes). The Phase-1 `commands.py` already lays down
  exactly this deterministic-helper surface (`cache get/put`, `telemetry append`,
  `eval run`).
- **Pros:** each layer does what only it can; deterministic ops remain unit-testable;
  no fictional "CLI spawns Agents" requirement.
- **Risk:** the seam between prose dispatch and CLI helpers must be specified carefully
  (which calls shell out, in what order) — but this is a documentation discipline, not
  an architectural contradiction.

---

## Recommendation

**Option Hybrid** — it is the evidence-favored reading given that "Haiku cannot write
files" is stated twice AND the anthropic SDK is banned (so the CLI cannot be the
Agent-spawner). The Phase-1 deterministic-helper surface already matches it. **However,
the spec does not state Option Hybrid explicitly**, so this item HALTS for human
confirmation rather than auto-applying the recommendation.

## What this item did and did NOT do

- **DID:** document the decision + all three options with their spec-line evidence and
  risks; add a PENDING entry to the task file's `### Open Questions / Human Decisions`
  section; set frontmatter `status: "⚪ Blocked"` + `blocker_reason`.
- **Did NOT:** implement any option. No dispatch code was written. Phases 4 & 5 remain
  blocked until the operator selects an option and returns the status to `"🟠 Doing"`.

## How the operator resolves this

1. Choose **Option H**, **Option P**, or **Option Hybrid**.
2. Edit this file's **Status** line and the task file's `### Open Questions / Human
   Decisions` Boundary-Decision entry to record the chosen option (e.g.
   `RESOLVED: Option Hybrid`).
3. Return the task frontmatter `status` to `"🟠 Doing"` (and clear/annotate
   `blocker_reason`).
4. Re-run `/task .dev/tasks/to-do/TASK-RF-20260603-032936/TASK-RF-20260603-032936.md`
   — execution resumes at Phase 4 Step 4.1, which reads this marker, writes
   `boundary-resolved.md`, and implements the chosen layering.
