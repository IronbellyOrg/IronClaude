---
spec_type: skill-creation-brief
target_skill: sc:debate
status: ready-for-skill-creator
parent_panel: panel-transcript-round-1.md
date: 2026-05-25
schema_version: 1
---

# Candidate Spec — `/sc:debate` v1

> **Status**: brainstorm + resolved-open-questions output from /sc:spec-panel. Ready as a brief for `/skill-creator`. All 5 prior open questions are closed below in the **Resolutions** section before the FR list.
>
> **Companion file**: `panel-transcript-round-1.md` (full expert discussion)

## Purpose

Lightweight, conversational sibling to `/sc:adversarial`. Provides on-demand adversarial reasoning for impromptu decisions, design critique, and option brainstorming **without** the file-input ceremony, multi-step audit-trail pipeline, or scoring algorithm of `/sc:adversarial`. Optimized for chat-rendered synthesis with a single artifact.

**Key differentiator vs `/sc:adversarial`**: zero file inputs required, no debate-orchestrator agent, no quantitative/qualitative scoring, single artifact, ~30-60s response time. Trades audit-trail depth for conversational fit.

## Resolutions of Round-1 Open Questions

| # | Question | Resolution | Rationale |
|---|----------|-----------|-----------|
| 1 | `--depth` flag in v1? | **DEFER to v2.** Single depth in v1. | Fowler: premature. Re-evaluate after usage data shows demand for `--quick` (single advocate) or `--deep` (3 advocates + extra round). |
| 2 | Skill name | **`/sc:debate`** | Covers all three modes. `/sc:redteam` would be critique-only; `/sc:weigh` reads decision-only. `/sc:debate` is mode-neutral. |
| 3 | Artifact path | **`.dev/research/debates/<YYYY-MM-DD-HHMMSS>-<short-slug>/debate-summary.md`** | `.dev/research/` is the documented home for "decision memos and analysis artefacts that inform design decisions" per `.dev/README.md`. Debates are decision memos. No new top-level dir, no overlap with `.dev/releases/` (debates are not releases). |
| 4 | Reuse `refs/debate-protocol.md` from `/sc:adversarial` | **Read-only import for v1.** SKILL.md cites the specific section (steelman-then-attack rules) by file path. If a third consumer ever emerges, extract to `src/superclaude/skills/_shared/refs/`. | Reuse-once is fine; extract-on-third-use avoids speculative abstraction. |
| 5 | AskUserQuestion timeout in Brainstorm Mode opt-out | **AskUserQuestion is synchronous and blocking with no timeout primitive.** Spec language changed: opt-out is a single AskUserQuestion call; on user-confirm → proceed; on user-deny → abort with no artifact written; user "walking away" simply means the skill blocks until they return — acceptable for a conversational skill. **No timeout-and-abort is implementable.** | Honest spec language matches tool reality. Avoids designing for a primitive that doesn't exist. |

These resolutions are reflected in the FRs and NFRs below.

## Use Cases (Cockburn-style, primary actor = user mid-conversation)

| ID | Use Case | Primary Goal | Input | Output |
|----|----------|--------------|-------|--------|
| UC-1 | **Decision** | Pick between user-stated options | 2+ positions stated in prompt | Recommendation + rationale + confidence |
| UC-2 | **Critique** | Red-team a single proposal | 1 proposal (inline / @file / context) | Attacks + refactored proposal |
| UC-3 | **Brainstorm** | Generate then debate options | 1 question, 0 positions | 2-3 options + UC-1 output |

## Functional Requirements

### Input & Mode Routing

- **FR-001 Mode router precedence** (Whittaker / Newman): mode SHALL be determined by explicit flag first, structural signals second, never by lexical keyword matching in the question text. Precedence:
  1. `--critique` / `--decide` / `--brainstorm` flag (if present)
  2. Presence of `@<path>` → Critique Mode
  3. ≥2 "vs" / "or" tokens or explicit positions listed → Decision Mode
  4. Otherwise → Brainstorm Mode
- **FR-002 Empty-input refusal**: invocations with no question and no flag SHALL refuse with a one-line clarification prompt; the skill MUST NOT silently fall back.
- **FR-003 Context-reference resolution**: when the user refers to recent context ("the design we just discussed"), the skill SHALL search the last 3 user messages for plausible candidates. If zero or multiple candidates match, the skill SHALL ask the user to disambiguate rather than guess.
- **FR-004 Position cap**: regardless of how many positions the user states, the skill SHALL cap advocate count at 3. Advocates are role-based (pro / contra / synthesizer), not position-1-to-1.

### Mode-Specific Acceptance Criteria

- **FR-005 Decision Mode (UC-1)**: output MUST contain:
  - A pro/con table with ≥3 rows per position
  - A recommended position (exactly one)
  - Confidence band {high, medium, low} with a one-line justification
  - A dissenting view section when confidence ≠ high
- **FR-006 Critique Mode (UC-2)**: output MUST contain:
  - A numbered list of ≥3 attacks, each tagged severity {CRITICAL | MAJOR | MINOR}
  - Each attack MUST cite ≥1 concrete consequence per FR-010 (not abstract)
  - A refactored-proposal section addressing all CRITICAL and MAJOR attacks
  - Each refactor change MUST annotate which attack(s) it addresses
- **FR-007 Brainstorm Mode (UC-3)**: output MUST contain:
  - An option-generation phase producing 2-3 distinct options BEFORE debate begins
  - An `AskUserQuestion` opt-out checkpoint: user confirms options before advocate Tasks spawn
  - On user confirmation, proceeds to FR-005 Decision Mode output
  - On user denial, aborts with no artifact written
  - **Per Resolution #5**: no timeout behavior is specified — AskUserQuestion blocks until user responds; that is acceptable for a conversational skill.

### Execution Model

- **FR-008 Parallel advocate spawn**: skill SHALL spawn 2-3 advocate Tasks in parallel (single-message multi-Task block). No `debate-orchestrator` agent is spawned.
- **FR-009 Steelman-then-attack template** (Whittaker / shared with `/sc:adversarial`): every advocate Task prompt MUST instruct the advocate to (a) steelman the opposing position in one paragraph BEFORE (b) attacking it. This is the durable shared dependency on the steelman-then-attack section of `src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md` (per Resolution #4: read-only import; no shared refs/ extraction until a third consumer exists).
- **FR-010 Contentful-critique gate**: synthesizer MUST refuse to recommend any position unless ≥1 advocate produced a concrete-consequence critique (one with a falsifiable failure condition: "breaks when N>100", "fails on cold start"). Abstract critiques ("is fragile", "is cleaner") do not satisfy the gate. If the gate fails, the skill SHALL render "No defensible recommendation — debate produced only abstract critiques. Suggest re-running with more context or escalating to `/sc:adversarial`."

### Failure Modes (Nygard)

- **FR-011 Advocate timeout / partial return**: if k of N advocate Tasks return within timeout, k<N, the skill SHALL proceed with the k returned outputs AND render a `DEGRADED (k/N advocates returned)` banner at the top of the chat output and in `debate-summary.md`. No silent degradation. If k=0, abort with explanatory message.
- **FR-012 Empty advocate output**: if any advocate returns <100 chars or output without a critique structure (no severity tags, no consequence citations), the skill SHALL retry that advocate exactly once. On second failure, treat as timeout per FR-011.
- **FR-013 Option collapse in Brainstorm Mode**: if the option-generation phase produces only 1 distinct viable option, the skill SHALL report this and exit early WITHOUT fabricating a strawman second option. Exit message: "Only one viable option surfaced — debate skipped. Reasoning: [...]".
- **FR-014 Strict no-auto-escalation**: `/sc:debate` MUST NOT invoke `/sc:adversarial`. It MAY suggest the heavier pipeline in its closing line ("for a full audit-trail debate with scoring, run `/sc:adversarial --compare ...`"). Suggestion is text-only.

### Output

- **FR-015 Chat synthesis**: bounded to ≤80 lines of rendered output. Sections: header (mode + advocate count + degraded banner if any), pro/con or attack table, recommendation/refactor, confidence + dissent.
- **FR-016 Artifact**: a single `debate-summary.md` SHALL be written to **`.dev/research/debates/<YYYY-MM-DD-HHMMSS>-<short-slug>/debate-summary.md`** (per Resolution #3). The directory is created on first artifact write; the slug is derived from the first 4 lowercase-alphanum words of the input question.
- **FR-017 Schema versioning**: `debate-summary.md` SHALL begin with YAML frontmatter:

  ```yaml
  ---
  schema_version: 1
  mode: <decide|critique|brainstorm>
  advocate_count: <N>
  degraded: <true|false>
  confidence: <high|medium|low>
  generated_by: sc:debate
  generated_at: <ISO-8601 timestamp>
  ---
  ```

  This enables future programmatic consumers without breaking changes.

## Non-Functional Requirements

- **NFR-001 Latency target**: end-to-end response (input → chat synthesis rendered) ≤90s p50, ≤180s p95. Failing NFR-001 means we are not lighter than `/sc:adversarial` and the value proposition collapses.
- **NFR-002 Footprint**: SKILL.md ≤600 lines (compared to /sc:adversarial's ~3000). The lightness must be reflected in skill source weight, not just runtime.
- **NFR-003 No new sub-agents**: skill MUST NOT introduce new persistent agent files in `src/superclaude/agents/`. Advocate prompts are inline in SKILL.md or in one shared `refs/advocate-prompts.md` within the skill package.

## Boundaries

**Will:**
- Run impromptu adversarial debates in 3 modes (Decision, Critique, Brainstorm)
- Spawn 2-3 parallel advocate Tasks with mandatory steelman-then-attack template
- Produce chat synthesis + one `debate-summary.md` artifact
- Suggest `/sc:adversarial` for heavier needs at the close of output

**Will Not:**
- Accept file artifacts as the only input (must accept inline / context-reference)
- Run quantitative + qualitative scoring or position-bias mitigation
- Auto-escalate to `/sc:adversarial`
- Spawn the `debate-orchestrator` agent
- Write multiple artifacts under `.dev/releases/`
- Fabricate strawman options to satisfy debate format (FR-013)

## Test Plan (Crispin)

| Layer | What it covers | FR coverage |
|-------|----------------|-------------|
| Unit | Mode router branches (FR-001) including sentinel-collision regression: `/sc:debate "should we critique this more aggressively?"` MUST NOT route to Critique Mode | FR-001, FR-002 |
| Unit | Empty-input refusal (FR-002) and context-resolution disambiguation (FR-003) | FR-002, FR-003 |
| Integration | Faked slow advocate (one of two Tasks delays past timeout) → degraded banner appears (FR-011) | FR-008, FR-011 |
| Integration | Advocate returns 50-char output → retried once → second failure → degraded (FR-012) | FR-012 |
| Integration | Contentful-critique gate failure path (FR-010): all advocates produce only abstract critiques → no recommendation, suggestive message | FR-010 |
| Integration | Brainstorm Mode option-collapse (FR-013): force option-gen to surface only 1 viable option → early exit, no strawman | FR-013 |
| E2E golden | One scenario per UC with frozen advocate outputs → frozen `debate-summary.md` byte-comparison | FR-005, FR-006, FR-007, FR-015, FR-017 |

All AC entries map cleanly to YAML for `/sc:validate-tests` consumption.

## Brief for `/skill-creator`

When invoked as:

```
/skill-creator @candidate-spec-v1.md
```

`/skill-creator` should produce:

1. `src/superclaude/skills/sc-debate/SKILL.md` (≤600 lines per NFR-002)
2. `src/superclaude/skills/sc-debate/refs/advocate-prompts.md` (the 3 advocate-role prompt templates: pro / contra / synthesizer, each implementing FR-009 steelman-then-attack)
3. `src/superclaude/commands/debate.md` (the `/sc:debate` slash-command stub that invokes `Skill sc:debate`)
4. Test scaffolding under `tests/skills/sc_debate/` matching the test plan table
5. Eval workspace under `.dev/eval-workspaces/sc-debate/` (per the `.dev/README.md` override rule — NOT under `.claude/skills/sc-debate-workspace/`)

## Sync & Install (post-skill-creator)

After `/skill-creator` produces the package:

1. `make sync-dev` to mirror `src/superclaude/skills/sc-debate/` → `.claude/skills/sc-debate/`
2. `make verify-sync` to confirm
3. `uv run pytest tests/skills/sc_debate/ -v` to run the test scaffolding
4. Smoke-test `/sc:debate "should we use Pydantic v1 or v2?"` in a fresh session

## Acceptance for v1 Ship

- All FR-001 through FR-017 pass their mapped test
- NFR-001 latency target observed on at least 5 real invocations (p50 ≤90s)
- NFR-002 SKILL.md ≤600 lines confirmed by `wc -l`
- NFR-003 no new agent files in `src/superclaude/agents/` confirmed
- `make verify-sync` green
- Documentation update: `.dev/README.md` "Where things go" table gets one new row: "An ad-hoc debate output → `.dev/research/debates/<timestamp>-<slug>/`"

## Deferred to v2 (not in scope)

- `--depth quick|standard|deep` flag (per Resolution #1)
- Sharing `refs/debate-protocol.md` extraction into `src/superclaude/skills/_shared/` (per Resolution #4 — defer until third consumer)
- Integration with `/sc:roadmap` (none planned; `/sc:debate` is conversational, not pipeline-stage)
- Multi-round debate (Round 2 rebuttals); v1 is one-shot advocate Task + synthesizer pass
- Position-bias mitigation (deliberately omitted — that's `/sc:adversarial`'s job)
