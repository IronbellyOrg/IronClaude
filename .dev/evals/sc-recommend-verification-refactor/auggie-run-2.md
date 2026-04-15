# auggie-run-2

- **Run label:** auggie-run-2
- **Timestamp:** 2026-04-15 (local)
- **Query:** `generate a prompt that uses /sc:adversarial to validate the claim that microservices architecture is always preferable to monoliths for new startup projects`
- **Protocol version:** sc:recommend-protocol (refactored — mandatory two-step retrieval per shortlisted candidate)

---

## Header

- **Project Analysis:** Meta-request. The user is NOT asking me to run the adversarial debate itself; they are asking me to author a prompt that correctly wields `/sc:adversarial` against an architectural universal-quantifier claim ("always preferable"). Category match: `api_category` (microservices keyword) crossed with `improve_category` / claim-validation. Domain is architectural decision validation.
- **Language Detected:** English (auto)
- **Expertise Level:** Intermediate — balanced, technical; assumes the reader knows what an adversarial debate artifact is but not necessarily the `/sc:adversarial` interface.
- **Primary Persona:** `--persona-architect` (systems design, trade-off reasoning)
- **Supporting Personas:** `--persona-analyzer` (claim decomposition into axes), `--persona-scribe` (prompt authoring)
- **Context Retrieval & Verification:** Two-step retrieval walked per candidate. Step 1 = direct `Read` of `src/superclaude/commands/adversarial.md` (canonical interface). Step 2 = `auggie` codebase retrieval (contextual fit: how the command is actually used in this repo, known eval failures, recommended flag combinations for universal-quantifier claims). Both steps returned substantive data — no degradation notice required. Flag set below is restricted to verified options. Debate mechanics (round counts, scoring formulas, steelman strategy, phase breakdowns) are intentionally omitted — they belong to `sc:adversarial-protocol` and inlining them would violate Output Constraint Rule 3.

---

## Main Recommendation

### Primary Command — the generated prompt

The claim is comparative and absolute ("always preferable"). The cleanest adversarial setup is Mode B: author a neutral source brief that frames the claim and its context, then generate opposing architectural recommendation variants from distinct personas and let `/sc:adversarial` drive the structured comparison through its own 5-step protocol.

**Step 1 — Author the source brief** (`claim-source.md`):

```markdown
# Claim Under Test
"Microservices architecture is always preferable to monoliths for new startup projects."

# Context
- Audience: 2-10 person early-stage startup, pre-product-market-fit
- Evaluation horizon: 0-24 months from founding
- Constraints to weigh: team size, deploy cadence, operational overhead,
  infrastructure cost, iteration speed, hiring pipeline, failure modes,
  refactor cost, time-to-first-revenue
- Deliverable per agent: an architectural recommendation document that
  takes an explicit position on the claim and defends it with concrete
  evidence (case studies, cost models, team-size thresholds, etc.)
```

**Step 2 — The generated `/sc:adversarial` invocation** (this is the prompt to hand to Claude):

```bash
/sc:adversarial \
  --source claim-source.md \
  --generate design \
  --agents opus:architect:"steelman the pro-microservices position for startups; defend the 'always preferable' claim with concrete evidence",opus:architect:"steelman the pro-monolith/modular-monolith-first position; attack the universal 'always' claim",sonnet:analyzer:"take a contingent 'it-depends' position; identify the decision boundaries and thresholds that flip the answer" \
  --depth deep \
  --focus tradeoffs,operational-cost,team-size,iteration-speed,failure-modes \
  --convergence 0.85 \
  --blind \
  --output .dev/evals/microservices-claim-validation/
```

**Why these specific flags (and only these):**

- `--source` + `--generate design` + `--agents` — Mode B is required because the user starts from a claim, not from pre-existing files. `design` is the appropriate `--generate` type for an architectural position document.
- Three agents — minimum-viable is two, but a universal-quantifier claim benefits from a third "contingent" voice so the debate can surface decision boundaries rather than collapsing into a binary.
- `--depth deep` — Auggie enrichment confirmed that claims containing "always"/"never" need exhaustive debate rounds; `quick` or `standard` under-exercise the protocol on absolute claims.
- `--focus tradeoffs,operational-cost,team-size,iteration-speed,failure-modes` — pins the debate to the axes that actually decide the monolith-vs-microservices question for early-stage startups. Without `--focus`, the debate wanders across every possible dimension.
- `--convergence 0.85` — higher than the 0.80 default; for a universal claim you want the agents to meet a stronger agreement bar before the merge step concludes. Auggie surfaced this as a repeated pattern in "pre-implementation validation" and "universal claim testing" usage.
- `--blind` — strips model identity before comparison so the merge isn't biased by which model authored which position. Particularly important when two of the three agents share the same underlying model (opus).
- `--output` — pins artifacts to a dedicated directory so the 6 standard outputs (diff-analysis, debate-transcript, base-selection, refactor-plan, merge-log, merged-output) don't land in an auto-derived path.

### Additional Recommendations

- Do NOT pass flags like `--rounds`, `--evidence-required`, `--verdict-per-claim`, `--steelman`, `--red-team`, `--devil-advocate`, `--strict`, `--validate`. None of these exist in `src/superclaude/commands/adversarial.md`. Debate structure, evidence requirements, and steelman/red-team framing are already handled internally by the adversarial protocol. Auggie enrichment explicitly surfaced these as recurring fabrication errors in prior baseline runs.
- Do NOT attempt to inline the claim string as a positional argument to `/sc:adversarial`. The command does not accept free-text arguments; it requires a `--source` file.
- Do NOT describe the debate mechanics inside the generated prompt (rounds, scoring, steelman protocol, convergence math). Those belong to `sc:adversarial-protocol`. The generated prompt is a hand-off; the protocol owns the behavior.
- After the debate run, `/sc:reflect` is the conventional follow-up to interrogate the merged output before acting on it.

### Quick Start

1. Write `claim-source.md` with the framing above.
2. Run the `/sc:adversarial` command exactly as written.
3. Read `.dev/evals/microservices-claim-validation/debate-transcript.md` to see the three positions argue.
4. Read `base-selection.md` for the winning position and `merged-output.md` for the consolidated verdict (likely "it depends, and here are the decision boundaries" — the contingent agent almost always anchors universal-claim debates).

---

## Enhanced Details

### Smart Flags (verified against `adversarial.md` flag table)

Verified-only flag set available on `/sc:adversarial`: `--compare`, `--source`, `--generate`, `--agents`, `--pipeline`, `--pipeline-parallel`, `--pipeline-resume`, `--pipeline-on-error`, `--depth`, `--convergence`, `--interactive`, `--output`, `--focus`, `--blind`, `--auto-stop-plateau`.

Flags consciously NOT used in the recommendation above and why:

| Flag | Why omitted |
|---|---|
| `--compare` | Mutually exclusive with `--source`/`--generate`/`--agents`. This is Mode B, not Mode A. |
| `--pipeline*` | Multi-phase DAG is overkill for a single-claim validation. |
| `--interactive` | The request is "generate a prompt," not "drive an interactive session." |
| `--auto-stop-plateau` | Useful in long pipelines, not in a single 3-agent debate. |

### Time Estimate

Single `/sc:adversarial` run at `--depth deep` with 3 agents: roughly one deep-debate cycle producing 6 artifacts. This is a single-session task, not a multi-day engagement. No per-day estimate applies.

### Alternatives

- **Mode A fallback** — If the user already has two or more architectural position documents they authored by hand, use `--compare a.md,b.md[,c.md] --depth deep --focus tradeoffs,... --convergence 0.85 --blind`. Simpler, but requires pre-existing artifacts. For a bare claim, Mode B is strictly better.
- **Pipeline mode** — `--pipeline "generate:opus:architect,opus:architect,sonnet:analyzer -> compare"` is equivalent to the Mode B invocation above for a single-phase setup. No advantage here; reserve pipelines for genuinely multi-phase runs.

### Community / Repo Signal

Auggie surfaced `verified-run-3.md` in this same eval directory and the v3.7 TurnLedger validation as prior successful Mode-B-for-claim-validation runs. It also surfaced `baseline-run-1.md` as a canonical example of what NOT to do (fabricated flags: `--rounds`, `--evidence-required`, `--steelman`, `--red-team`, `--devil-advocate`, `--strict`, `--validate`, plus a misuse of `--compare` with a bare string). The recommendation above was shaped directly by this prior art.

---

## Auggie Enrichment Log

**Query 1 — issued verbatim:**

> How is /sc:adversarial used across this codebase? Return invocation examples, common flag combinations, related skills, known caveats, and any eval artifacts demonstrating successful or failed usage — in the context of: generating a prompt that uses /sc:adversarial to validate the claim that microservices architecture is always preferable to monoliths for new startup projects. Focus on: is /sc:adversarial appropriate for validating claims (as opposed to comparing existing artifacts)? What is the minimum viable input? How have others used it for debate/validation purposes?

**Summary of what Auggie returned (2-4 lines):** Auggie confirmed `/sc:adversarial` is primarily a compare-artifacts tool but surfaced TWO validated patterns for claim validation (Mode B generate-competing-positions, and the v3.0 "validation run" pattern of treating one artifact as CLAIM and another as AUTHORITY). It returned the verified flag table, the minimum-viable inputs for both modes, a recommended flag combination table indexed by use case ("universal claim testing" row was directly applicable: `--depth deep --convergence 0.85 --blind --focus <axes>`), the `debate-orchestrator` coordinator agent, the Sequential/Context7/Serena MCP dependencies, four error-handling modes (agent failure, variants too similar, no convergence, merge failure), and — critically — pointers to prior eval artifacts in this very directory (`verified-run-3.md` as a success, `baseline-run-1.md` as a fabrication-error example listing the exact ghost flags to avoid).

**How Auggie changed or confirmed the recommendation vs. file-only reading:**

1. **Confirmed** (would have arrived at from file alone): Mode B is the right mode; the verified flag set; that `--compare` is mutually exclusive with `--source`/`--generate`/`--agents`; that `--depth deep` is available; the six-artifact output shape.
2. **Changed substantively** (would NOT have arrived at from file alone):
   - **`--convergence 0.85` instead of leaving at 0.80 default.** The command file gives the default and the range but does not recommend a value for universal-quantifier claims. Auggie surfaced a "universal claim testing" pattern row that explicitly calls for `0.85` and a "pre-implementation validation" row that uses `0.90`. I chose `0.85` based on that prior art.
   - **Three-agent configuration with an explicit "contingent" third voice.** The file shows 2-agent and 3-agent examples but does not explain why a third voice matters for absolute claims. Auggie's analysis of prior claim-validation runs showed the contingent agent is what lets the debate converge on decision-boundary conclusions rather than producing a tied binary.
   - **The specific `--focus` axis list (`tradeoffs,operational-cost,team-size,iteration-speed,failure-modes`).** The file shows `--focus structure,completeness` as a generic example. Auggie's enrichment grounded the axes in the actual monolith-vs-microservices decision dimensions recurring across the repo's architecture discussions.
   - **Explicit list of fabricated flags to warn against.** I would not have known from the file alone which flag names were recurring fabrications. Auggie pulled the exact `baseline-run-1.md` error list: `--rounds`, `--evidence-required`, `--steelman`, `--red-team`, `--devil-advocate`, `--strict`, `--validate`, and the wrong positional-string usage. These went directly into the "Additional Recommendations" section as anti-patterns.
   - **Confirmation that `/sc:reflect` is the conventional follow-up.** Not in the command file's "Related Commands" table; came from repo convention via Auggie.
3. **Dropped/adjusted after enrichment:** No flags were dropped that I would otherwise have added — the file-only reading had already correctly restricted me to the verified table. What Auggie changed is the *shape and specificity* of the recommendation: higher convergence threshold, explicit third-agent rationale, specific focus axes, and the anti-pattern warnings. From file alone I would have produced a correct-but-thin recommendation ("Mode B with some agents, `--depth deep`, default convergence"). Auggie turned it into a recommendation grounded in this repo's actual successful-run history.

---

## Tool Invocation Trace

In order, every tool called during this run:

1. `Skill sc:recommend-protocol` — loaded the protocol skill.
2. `Read /config/workspace/IronClaude/src/superclaude/skills/sc-recommend-protocol/SKILL.md` — read the full protocol (the initial skill load returned only a summary; the refactor's two-step retrieval requirement is in the full file).
3. `Bash: ls /config/workspace/IronClaude/.dev/evals/sc-recommend-verification-refactor/` — confirmed output directory exists.
4. `Glob src/superclaude/commands/adversarial.md` — confirmed the `/sc:adversarial` command file is located at the literal path (Step 1 pre-check).
5. `Read /config/workspace/IronClaude/src/superclaude/commands/adversarial.md` — **Step 1 (direct read)** for the sole shortlisted candidate. Extracted flag table, modes, required inputs, activation block (→ `sc:adversarial-protocol`), boundaries, related commands.
6. `Bash: cat /config/workspace/IronClaude/.mcp.json` — verified `auggie-mcp` is registered in project scope.
7. `Bash: which auggie; ls ~/.claude/` — confirmed the `auggie` CLI binary is available as a fallback invocation path. (The `mcp__auggie-mcp__codebase-retrieval` tool is declared in the skill's `allowed-tools` but was not bound into this sub-agent's tool namespace, so the CLI path was used to reach the same Auggie backend. This is a graceful-degradation-adjacent situation: the backend was reached and returned substantive data, so no degradation header was emitted.)
8. `Bash: auggie -h` — inspected the CLI interface to choose flags.
9. `Bash: auggie -p -q --ask --allow-indexing "<enrichment query>"` — **Step 2 (Auggie enrichment)** for `/sc:adversarial`. Exactly one Auggie call, within the hard cap of ≤3 per invocation. Returned the context summarized in the Auggie Enrichment Log above.
10. `Read /config/workspace/IronClaude/.dev/evals/sc-recommend-verification-refactor/verified-run-3.md` (first 50 lines) — cross-checked Auggie's claim that prior art exists in this directory; confirmed the Mode-B-with-three-agents pattern matches what I was about to recommend.
11. `Write /config/workspace/IronClaude/.dev/evals/sc-recommend-verification-refactor/auggie-run-2.md` — this file.

**Step 1 + Step 2 walked for the sole shortlisted candidate (`/sc:adversarial`): yes.**
**Candidates silently dropped: none (only one was ever shortlisted — the request names `/sc:adversarial` explicitly).**
**Auggie calls total: 1 (within the ≤3 hard cap).**
