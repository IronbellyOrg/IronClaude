# auggie-run-3

- **Run label:** auggie-run-3
- **Timestamp:** 2026-04-15 (black-box re-eval of refactored sc:recommend-protocol)
- **Query:** `generate a prompt that uses /sc:adversarial to validate the claim that microservices architecture is always preferable to monoliths for new startup projects`
- **Protocol version:** `src/superclaude/skills/sc-recommend-protocol/SKILL.md` (refactored — Step 1 direct read + Step 2 mandatory Auggie enrichment per shortlisted candidate)

> **Header Notice (graceful degradation):** Auggie enrichment unavailable in this sub-agent's tool surface — `mcp__auggie-mcp__codebase-retrieval` is declared in the skill's `allowed-tools` frontmatter and the workspace `.mcp.json` does register `auggie-mcp` at project scope, but the MCP tool was not exposed to this Task agent's tool set at invocation time. Recommendation cites verified flags (Step 1 complete for all candidates) but omits repo-specific usage nuance that Step 2 would have populated. See `## Auggie Enrichment Log` for details.

---

## Header

- **Project Analysis:** Meta-request. User is asking for a crafted prompt that will drive `/sc:adversarial` to stress-test a universal-quantifier architectural claim ("microservices always > monoliths for new startups"). Category match by keywords: `api_category` (microservices/architecture), `improve_category` (validate), `create_category` (generate a prompt). Domain: architectural decision validation; failure mode to avoid: writing the prompt as if `/sc:recommend` itself owns the debate logic (it does not — `/sc:adversarial`'s protocol does).
- **Language Detected:** English (auto, no Turkish diacritics, dominant English tokens).
- **Expertise Level:** Intermediate. The user already knows `/sc:adversarial` exists and names it directly; phrasing assumes familiarity with prompt engineering but not with the adversarial command's internal mechanics.
- **Primary Persona:** `--persona-architect` (systems design, trade-off reasoning).
- **Supporting Personas:** `--persona-analyzer` (claim decomposition under the "always" quantifier), `--persona-scribe` (prompt authoring clarity).
- **Verified candidates (Step 1 resolved):**
  - `sc:adversarial` — `src/superclaude/commands/adversarial.md` (Mode A/B/Pipeline; delegates via `Skill sc:adversarial-protocol`, so Rule 3 "no protocol reimplementation" applies).
  - `sc:research` — `src/superclaude/commands/research.md` (no skill delegation; CRITICAL BOUNDARIES: "STOP AFTER RESEARCH REPORT"; explicitly will not implement findings).
  - `sc:reflect` — `src/superclaude/commands/reflect.md` (Serena-backed; no skill delegation; used for post-task validation, not pre-prompt crafting).
- **Dropped candidates:** none this run — all three shortlisted files resolved via Step 1.

---

## Main Recommendation

### Primary Command — the generated prompt

The recommended shape is a **Mode B** `/sc:adversarial` invocation: hand the command a neutral source brief, ask it to generate opposing architectural recommendation variants under distinct personas, and let `/sc:adversarial`'s own protocol drive the structured comparison. The claim is comparative ("preferable") and universal ("always"), which is the exact shape adversarial debate is built to stress.

**Step 1 — Author a neutral source brief** (`claim-source.md`):

```markdown
# Claim Under Test
"Microservices architecture is always preferable to monoliths for new startup projects."

# Context
- Audience: 2-10 person early-stage startup, pre-product-market-fit
- Evaluation horizon: 0-24 months from founding
- Constraints to weigh: team size, deploy cadence, operational overhead,
  cost, iteration speed, hiring pipeline, failure modes, refactor cost,
  time-to-first-revenue
- Deliverable per agent: a self-contained architectural recommendation
  document that takes an explicit position on the claim and defends it
  with concrete evidence, not just assertion
```

**Step 2 — The generated prompt (hand this to Claude verbatim):**

```bash
/sc:adversarial \
  --source claim-source.md \
  --generate design \
  --agents opus:architect:"steelman the pro-microservices position for startups; defend the 'always preferable' universal claim with concrete operational evidence",opus:architect:"steelman the pro-monolith position for startups; attack the universal 'always' claim and defend modular-monolith-first",sonnet:analyzer:"take an explicit contingent/it-depends position; surface the decision boundaries (team size, deploy cadence, domain complexity) that flip the answer" \
  --depth deep \
  --focus tradeoffs,operational-cost,team-size,iteration-speed,failure-modes \
  --convergence 0.85 \
  --blind \
  --output .dev/evals/microservices-vs-monolith-startup/
```

**Why this shape (flag-by-flag, verified-only):**

- `--source claim-source.md` + `--generate design` + `--agents ...` is Mode B — the verified "generate variants from a common source, then compare" path.
- **Three agents, not two**, because the claim's universal quantifier ("always") is specifically falsified by a single counter-example. A contingent third position is needed to surface the boundary conditions; two agents would produce a symmetric debate that can plateau without ever attacking the universal.
- `--depth deep` — architectural trade-off claims lose fidelity at `quick` or `standard`; the operational cost curves and hiring-pipeline effects only show up under deep debate.
- `--focus` is narrowed to the axes that actually decide this claim in an early-stage startup context. Leaving it unset debates everything and dilutes signal.
- `--convergence 0.85` is raised above the 0.80 default because a universal-quantifier claim should only be affirmed under near-unanimous alignment; borderline consensus is not enough to keep "always."
- `--blind` strips model/persona identity before the merge step so the verdict isn't anchored to which agent "sounds architect-shaped."
- `--output` is scoped to an eval directory so the six standard artifacts (`diff-analysis.md`, `debate-transcript.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, merged output) don't pollute the repo root.

### Additional Recommendations

- **Add `--interactive`** if you want a human checkpoint to inspect `debate-transcript.md` before the merge step commits to a verdict. Politically charged universal claims benefit from this.
- **Add `--auto-stop-plateau`** if you intend to re-run the debate in pipeline mode later; it halts cleanly when agents stop moving instead of burning rounds at a fixed-point.
- **Do NOT** pass flags like `--rounds`, `--evidence-required`, `--verdict-per-claim`, `--measure-first`, `--steelman`, `--counter-rounds`. These are not part of `/sc:adversarial`'s verified interface. Debate round logic, evidence gating, and per-claim verdicts are owned by `sc:adversarial-protocol`; specifying them inline is fabrication (Rule 1) and protocol duplication (Rule 3).

### Quick-Start

1. Create `claim-source.md` using the brief from Step 1.
2. Run the `/sc:adversarial` command from Step 2 exactly as written.
3. Read `.dev/evals/microservices-vs-monolith-startup/debate-transcript.md` and `base-selection.md` to see which position survived, and what boundary conditions the analyzer pinned down.
4. Treat the merged output as the validated (or falsified) answer to the universal claim. Expect the merge to show the "always" quantifier does not hold under startup constraints.

---

## Enhanced Details

### Smart Flag Rationale (verified flags only — Rule 1)

| Flag | Value | Justification |
|------|-------|---------------|
| `--source` | `claim-source.md` | Mode B entry; single shared framing for all agents |
| `--generate` | `design` | Artifact type that matches architectural recommendation deliverables |
| `--agents` | 3 specs (pro / con / contingent) | Universal-quantifier claim requires a boundary-finder, not just a symmetric two-sided debate |
| `--depth` | `deep` | Trade-off claims collapse to platitudes at `quick`/`standard` |
| `--focus` | `tradeoffs,operational-cost,team-size,iteration-speed,failure-modes` | Confines debate to axes that actually decide startup architecture |
| `--convergence` | `0.85` | Raised above default 0.80; a universal claim shouldn't pass on weak alignment |
| `--blind` | on | Removes persona-identity bias from the merge step |
| `--output` | `.dev/evals/microservices-vs-monolith-startup/` | Eval-scoped artifact directory |

Every flag above was cross-checked against the Options table in `src/superclaude/commands/adversarial.md`. No other flags were introduced.

### Expected Artifacts

`/sc:adversarial` will emit its six standard artifacts into `--output`. This recommendation does not restate their internal semantics — that is owned by `sc:adversarial-protocol` (Rule 3: invoke, don't reimplement).

### Why `/sc:research` and `/sc:reflect` were resolved but not promoted

- **`/sc:research`** — Resolved cleanly via Step 1. Would be useful *upstream* if the user wanted to gather external evidence on the claim before running the debate, but it carries an explicit "STOP AFTER RESEARCH REPORT" boundary (see lines 105-123 of `research.md`). Chaining it into the prompt would violate its own boundaries; surfacing it would dilute the main recommendation. Deferred to an optional upstream step.
- **`/sc:reflect`** — Resolved cleanly via Step 1. Serena-backed, operates on in-session task state, designed for post-completion validation of work done. It does not help craft the `/sc:adversarial` prompt and cannot validate the claim itself. Not promoted.

### Alternatives (unused this run)

- **Mode A** (`--compare`): possible if the user already had two existing architecture documents to pit against each other. They don't — the claim is abstract, so Mode B (generate first, then compare) is the correct entry.
- **Pipeline Mode** (`--pipeline`): overkill for a single comparison; appropriate if the user later wants to chain `generate -> compare -> generate again`. Noted for future escalation.

### Expertise-Level Note

The prompt above targets an intermediate user. For a beginner-friendly variant:
- Drop the third (contingent) agent — two sides is easier to read.
- Use `--depth standard` instead of `deep`.
- Add `--interactive` for a human checkpoint before the merge.
Trade: faster to review, but the universal quantifier may survive on symmetric convergence without ever being cornered.

### Boundaries of This Recommendation

- Produces the **prompt**. Does not execute `/sc:adversarial`.
- Takes no position on whether microservices actually are or aren't preferable — that's the adversarial run's output, not `/sc:recommend`'s.
- All flags cited are verified against `src/superclaude/commands/adversarial.md` as of this run. Anything not in that file's Options table is intentionally absent.

---

## Auggie Enrichment Log

**Protocol requirement:** Step 2 (`mcp__auggie-mcp__codebase-retrieval`) must be issued once per shortlisted candidate (≤3 total per run).

**Actual state this run:** Auggie MCP tool was **not exposed to this agent's tool set**, despite being:
1. Declared in the skill's `allowed-tools` frontmatter (`src/superclaude/skills/sc-recommend-protocol/SKILL.md` line 4).
2. Registered at project scope in `/config/workspace/IronClaude/.mcp.json` (stdio, `npx -y auggie-mcp`).

The Task sub-agent's available tool list at invocation time included Bash, Read, Glob, Grep, Edit, Write, WebFetch, WebSearch, TaskCreate/Get/List/Update, Skill, NotebookEdit, CronCreate/Delete/List, EnterWorktree/ExitWorktree, Monitor, RemoteTrigger, ScheduleWakeup — **no `mcp__auggie-mcp__codebase-retrieval` entry**. No in-band invocation path was available. (Bash cannot call MCP tools; MCP is a harness-level surface.)

### Queries I would have issued, per candidate

The protocol specifies the query shape: "shaped by the user's original request, covering invocation examples, common flag combinations, related skills, known caveats, and eval artifacts." Had Auggie been exposed, I would have issued exactly these three queries (one per shortlisted candidate):

1. **For `sc:adversarial`:**
   > "How is `/sc:adversarial` actually invoked across this codebase? Return real invocation examples, common Mode B `--agents` spec patterns, `--depth` + `--convergence` combinations used in practice, related skills routinely paired with it (e.g. `sc:roadmap`, `sc:reflect`, `sc:spec-panel`), any known caveats about pipeline mode or blind evaluation, and eval artifacts demonstrating successful or failed debate runs — in the context of: generating a prompt that uses `/sc:adversarial` to validate a universal-quantifier architectural claim (microservices vs. monoliths for startups)."

2. **For `sc:research`:**
   > "How is `/sc:research` used across this codebase? Return real invocation examples, depth/strategy combinations, whether it is ever chained before `/sc:adversarial` or `/sc:design`, and any caveats about its STOP-AFTER-REPORT boundary in practice — in the context of: gathering external evidence before validating an architectural claim."

3. **For `sc:reflect`:**
   > "How is `/sc:reflect` used across this codebase? Return invocation examples, typical `--type` choices, whether it is used pre-prompt-crafting (unlikely) or post-task-completion, and any caveats about Serena MCP dependency — in the context of: validating whether an adversarial debate's merged verdict should be trusted."

### What this gap changed in the output

Because Step 2 could not run, the following fields in the verified-interface records for all three candidates were filled with the graceful-degradation sentinel "unavailable":
- `usage_notes` — I have no repo-grounded data on which flag combinations are load-bearing in practice vs. theoretically correct.
- `related_skills` — I inferred `sc:reflect` as a follow-up candidate from the command map only, not from observed repo co-usage.
- `known_caveats` — No eval-history lessons were pulled in. If there is a known pitfall about e.g. `--blind` interacting weirdly with Mode B agent specs, I would not have surfaced it.
- `invocation_examples` — I cite only the examples in `adversarial.md` itself (lines 74-128), not real uses elsewhere in the repo.

### Honest assessment of the resulting recommendation

Without Auggie enrichment, the recommendation is **flag-correct** (every flag cited exists in the Options table) and **Rule-3 compliant** (no protocol reimplementation — the prompt hands off to `/sc:adversarial` and trusts the skill). But it is **thin on repo-specific nuance**: I cannot say whether three-agent setups are common in this repo, whether `--convergence 0.85` is a standard bar or an outlier, or whether prior eval runs have already shown that `--blind` changes outcomes meaningfully for Mode B. A reader who wants "what actually works here" vs. "what the interface permits" is getting the second answer only.

This is the exact failure mode the refactor was meant to close. It did not close in this run — not because the skill was ignored, but because the MCP tool it depends on was not plumbed through to the sub-agent's tool surface.

---

## Tool Invocation Trace

Ordered list of every tool I actually called during this run (for reviewer verification of the Step 1 → Step 2 path):

1. **Skill** `sc:recommend-protocol` — load the protocol (returned legacy-summary variant, insufficient for refactor compliance).
2. **Read** `/config/workspace/IronClaude/src/superclaude/skills/sc-recommend-protocol/SKILL.md` — fetch the refactored protocol from source of truth. Confirmed Step 1 + Step 2 mandate at lines 66-97.
3. **Bash** `ls /config/workspace/IronClaude/.dev/evals/sc-recommend-verification-refactor/` — verify output directory exists (it does, alongside prior baseline-run-{1,2,3}.md and verified-run-{1,2,3}.md).
4. **Glob** `src/superclaude/commands/adversarial.md` — Step 1 path check for candidate 1.
5. **Glob** `src/superclaude/commands/research.md` — Step 1 path check for candidate 2.
6. **Glob** `src/superclaude/commands/reflect.md` — Step 1 path check for candidate 3.
7. **Read** `/config/workspace/IronClaude/src/superclaude/commands/adversarial.md` — Step 1 canonical interface for `sc:adversarial`. Extracted flag table (lines 52-68), activation block (lines 130-136, `skill-indirected` → `sc:adversarial-protocol`), related commands (lines 161-167).
8. **Read** `/config/workspace/IronClaude/src/superclaude/commands/research.md` — Step 1 canonical interface for `sc:research`. No protocol skill delegation; CRITICAL BOUNDARIES section at lines 105-123 flags STOP-AFTER-REPORT.
9. **Read** `/config/workspace/IronClaude/src/superclaude/commands/reflect.md` — Step 1 canonical interface for `sc:reflect`. No protocol skill delegation; Serena-bound.
10. **Bash** `cat /config/workspace/IronClaude/.mcp.json` — sanity check that Auggie is configured in the workspace (it is: `auggie-mcp` stdio via `npx -y auggie-mcp`).
11. **Read** `/config/workspace/IronClaude/.dev/evals/sc-recommend-verification-refactor/verified-run-3.md` — quick scan of an existing verified-run artifact for format/tone alignment before writing this run's output.
12. **Write** `/config/workspace/IronClaude/.dev/evals/sc-recommend-verification-refactor/auggie-run-3.md` — this file.

**Tool NOT called (but required by refactored protocol):** `mcp__auggie-mcp__codebase-retrieval` — not exposed to this sub-agent's tool surface. Graceful degradation path taken per `SKILL.md` lines 141-146 ("Auggie MCP not configured | Proceed with Step 1 only. Emit header notice.").
