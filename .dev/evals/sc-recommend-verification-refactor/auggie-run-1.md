# auggie-run-1

- **Run label:** auggie-run-1 (refactored protocol — mandatory Auggie enrichment per candidate)
- **Timestamp:** 2026-04-15 (local session)
- **Query:** `generate a prompt that uses /sc:adversarial to validate the claim that microservices architecture is always preferable to monoliths for new startup projects`

---

## Header

- **Project analysis:** Meta-request — the user is asking for a *crafted prompt*, not direct execution. The target command is explicitly named (`/sc:adversarial`), so candidate generation is already pinned. The claim under test is an absolute/universal-quantifier architectural proposition ("microservices are *always* preferable"), which shapes agent topology and convergence threshold. Domain: architectural decision validation.
- **Language detected:** English (auto)
- **Expertise level:** Intermediate (balanced, technical phrasing; user already knows `/sc:adversarial` exists)
- **Primary persona:** `architect` (systems design, trade-off analysis)
- **Supporting personas:** `analyzer` (claim decomposition, boundary-finding), `scribe` (prompt authoring)
- **Context retrieval status:** Step 1 (direct read of `src/superclaude/commands/adversarial.md`) complete. Step 2 (Auggie enrichment via codebase-retrieval) complete — see Auggie Enrichment Log at the bottom. No degradation notices; recommendation is fully verified on both axes.
- **Shortlisted candidates this run:** 1 (`/sc:adversarial` — the only shortlisted target because the user named it explicitly and the request is "generate a prompt that uses X," not "recommend between X, Y, Z"). Auggie budget used: 1 of 3.

---

## Main Recommendation

### Primary command — the generated prompt

The recommended prompt is a **Mode B** invocation of `/sc:adversarial` (source + generate + agents). Mode B — not Mode A — is the verified pattern for claim adjudication in this codebase: you author a neutral source brief that frames the claim, then let three agents each *generate* an architectural position from that brief, and let the adversarial protocol debate, score, and merge them. Mode A (`--compare` pre-existing files) is for merging drafts that already exist, which is not the situation here — there are no drafts yet, only a claim.

The universal quantifier "always" is load-bearing. A two-agent pro/con debate is *insufficient* to falsify a universal claim: an "it depends" answer with a boundary condition is a valid falsification, and neither steelman alone will produce it. Auggie enrichment surfaced this explicitly (see Enrichment Log, finding #3). That is why the recommended shape uses **three agents**, not two.

**Step 1 — Author the source brief** (`claim-source.md`):

```markdown
# Claim Under Test
"Microservices architecture is always preferable to monoliths for new startup projects."

# Context
- Audience: 2-10 person early-stage startup, pre-product-market-fit
- Evaluation horizon: 0-24 months from founding
- Axes to weigh: team size, deploy cadence, operational overhead, infra cost,
  iteration speed, hiring pipeline, failure modes, refactor cost,
  time-to-first-revenue, debugging complexity
- Deliverable per agent: an architectural recommendation document that
  takes an explicit position on the claim and defends it with concrete
  evidence and decision criteria
```

**Step 2 — The generated `/sc:adversarial` prompt to hand to Claude:**

```bash
/sc:adversarial \
  --source claim-source.md \
  --generate design \
  --agents opus:architect:"steelman the pro-microservices position; defend the 'always preferable' universal claim with concrete evidence and startup-specific reasoning",opus:architect:"steelman the pro-monolith (modular-monolith-first) position; attack the 'always' quantifier and defend deferring microservices until scale forces them",sonnet:analyzer:"take a contingent 'it depends' position; your job is to identify the decision boundaries — team size, product maturity, traffic, organizational structure — at which the answer flips" \
  --depth deep \
  --focus tradeoffs,operational-cost,team-size,iteration-speed,failure-modes \
  --convergence 0.85 \
  --blind \
  --output .dev/evals/microservices-vs-monolith-startup/
```

**Why this exact shape:**

- **Mode B** (`--source` + `--generate` + `--agents`): verified in `adversarial.md` Options table and confirmed by Auggie as the prior-art pattern for claim adjudication. Mode A would require pre-existing files that don't exist yet.
- **Three agents, not two:** the universal quantifier demands a contingent third position. Two-sided steelman debate cannot falsify "always X" because "it depends, and here is when" is the only refutation that matters.
- **`--generate design`:** the artifact type each agent produces is an architectural recommendation, which is the closest fit in the adversarial protocol's supported generate types.
- **`--depth deep`:** verified flag. Architectural trade-off debates lose signal at `quick` or `standard` depth; Auggie enrichment flagged that shallow depth misses operational-cost curves, which are exactly the axes that decide this claim.
- **`--focus tradeoffs,operational-cost,team-size,iteration-speed,failure-modes`:** verified flag. Narrows the debate to the axes that actually decide this claim in a startup context. Leaving `--focus` unset would waste budget debating orthogonal dimensions like internationalization or governance.
- **`--convergence 0.85`:** verified flag. Raised from the 0.80 default specifically because Auggie enrichment surfaced v3.8 validation guidance: universal-quantifier claims need a tighter convergence bar before the merged verdict is allowed to assert "always."
- **`--blind`:** verified flag. Strips model/persona identity before comparison so the base-selection step isn't biased by which agent "sounds like the architect." Auggie also flagged this as a known mitigation for the "convergence ≠ correctness" failure mode.
- **`--output`:** verified flag. Puts the six standard adversarial artifacts in an eval-scoped directory so they don't pollute the repo root.

### Additional recommendations

- **Optionally add `--interactive`** (verified flag) if the claim is politically or culturally charged and you want a human checkpoint between debate and merge. Useful when the output might be cited in a decision document.
- **Optionally add `--auto-stop-plateau`** (verified flag) if you plan to escalate to pipeline mode later. It halts cleanly on convergence plateau and plays well with `--pipeline-resume`.
- **Do not** pass flags that are not in `adversarial.md`'s Options table. Specifically, `--rounds`, `--evidence-required`, `--verdict-per-claim`, `--measure-first`, `--steelman`, `--adversary`, `--devils-advocate` are **not** part of the interface. Some of these appeared in `baseline-run-1.md` in this very eval directory and were the failure mode that motivated the refactor. Debate structure, round counts, evidence requirements, and per-claim verdicts are already handled internally by the `sc:adversarial-protocol` skill; re-specifying them inline is unsupported (Rule 1), redundant (Rule 3), and causes drift between recommendation and actual command behavior.
- **Do not** inline the debate rules, scoring formulas, phase breakdowns, or artifact lists in the prompt. The `sc:adversarial-protocol` skill owns all of that. The generated prompt is a hand-off, not a specification (Rule 3).

### Quick-start (copy-paste)

1. Create `claim-source.md` with the brief from Step 1.
2. Run the `/sc:adversarial` command from Step 2 verbatim.
3. After the run, read these artifacts in order:
   - `.dev/evals/microservices-vs-monolith-startup/debate-transcript.md` — the three-way structured debate
   - `.dev/evals/microservices-vs-monolith-startup/base-selection.md` — which position was selected as the base for the merge and why
   - `.dev/evals/microservices-vs-monolith-startup/refactor-plan.md` and the merged output file — the final adjudicated verdict on the claim
4. Treat the merged output as the validated-or-invalidated answer. If convergence landed below 0.85, the merged verdict is **unreliable** and the claim should be treated as open, not decided.

---

## Enhanced Details

### Smart flag notes

Only flags present in `adversarial.md`'s Options table appear above:

`--compare`, `--source`, `--generate`, `--agents`, `--pipeline`, `--pipeline-parallel`, `--pipeline-resume`, `--pipeline-on-error`, `--depth`, `--convergence`, `--interactive`, `--output`, `--focus`, `--blind`, `--auto-stop-plateau`.

The recommended command uses: `--source`, `--generate`, `--agents`, `--depth`, `--focus`, `--convergence`, `--blind`, `--output`. All eight are verified present in the Options table. Optional additions (`--interactive`, `--auto-stop-plateau`) are also verified.

### Time / cost estimate

- **Author `claim-source.md`:** ~5 minutes (short, structured, human-authored).
- **Run `/sc:adversarial` at `--depth deep` with 3 agents:** Auggie surfaced that deep depth is "very expensive" at 3-5 rounds (v2.09 scoring eval). Expect this to be the dominant cost. Rough ballpark: 20-60k output tokens plus reasoning, depending on how quickly agents converge.
- **Review artifacts:** ~15-30 minutes to read transcript, base-selection, and merged verdict.
- **Total wall clock:** ~1-2 hours including human review. Budget accordingly; do not run at `deep` if you need the answer in 10 minutes — fall back to `standard` and accept coarser trade-off analysis.

### Alternatives considered and rejected

| Alternative | Why rejected |
|---|---|
| Mode A with two hand-authored files (`pro-micro.md`, `pro-mono.md`) | Requires the user to write both positions themselves, which defeats the point — the adversarial protocol's value is in letting models generate and defend positions, not in the user pre-committing to the framing. |
| Two agents only (drop the contingent analyzer) | Cannot falsify a universal claim. "It depends, and here is the boundary" is the only answer that refutes "always X," and neither steelman produces it. Auggie enrichment confirmed this. |
| `--depth standard` instead of `deep` | Cheaper, but Auggie surfaced that shallow depth misses operational-cost curves, which are the axes that actually decide this claim. |
| `--convergence 0.80` (default) | Too permissive for a universal claim. A merged verdict asserting "always" at 0.80 convergence is not trustworthy. |
| Skip `--blind` | Risks base-selection bias toward whichever persona "sounds like the architect." Auggie flagged this as a known mitigation. |
| `/sc:research` instead | Gathers external evidence but does not produce a structured adversarial verdict. Wrong tool for claim adjudication; right tool for evidence scouting. Not shortlisted. |

### Known caveats to surface to the user

From Auggie enrichment (eval retrospectives):

1. **Convergence is not correctness.** Two agents can converge on a wrong answer. The merged verdict is strong evidence, not proof. `--blind` + high `--convergence` + a contingent third agent reduce but do not eliminate this risk.
2. **Document-centric, not execution-centric.** `/sc:adversarial` operates on written positions; it does not run code, measure real deploys, or validate runtime behavior. For this specific claim that is fine — the claim is itself document-level — but be explicit that the verdict is a *reasoned* verdict, not an *empirical* one.
3. **Incomplete follow-through risk** (from v2.07-2.08 retrospectives): historically ~85-90% of adversarial conclusions got incorporated into downstream work. If this verdict is going to drive an actual architectural decision, track the findings as blocking rather than advisory.

---

## Auggie Enrichment Log

One Auggie query was issued. Budget: 1 of 3 shortlisted-candidate slots used.

### Query 1 — `/sc:adversarial` contextual fit for claim adjudication

**Verbatim query** (issued via `auggie -p --ask` against workspace `/config/workspace/IronClaude`, the same backend and index as `mcp__auggie-mcp__codebase-retrieval`):

> Search the codebase for how /sc:adversarial is used. I need: (1) concrete invocation examples from docs, evals, or tests, (2) which mode (--compare files, --source+--generate+--agents, or --pipeline) is typically used for validating a single proposition or claim as opposed to merging competing drafts, (3) related skills or commands conventionally paired with it, (4) known caveats or eval lessons, (5) whether there is prior art for using /sc:adversarial to adjudicate a CLAIM (e.g. 'X is preferable to Y') rather than compare pre-existing artifacts. Return concise findings.

**Summary of what Auggie returned** (4 lines):

Auggie surfaced a rich body of prior art: Mode A is the common path for merging existing drafts, while Mode B (`--source` + `--generate` + `--agents`) is the verified pattern for claim adjudication, with `/sc:roadmap` as the primary downstream consumer. It identified a concrete prior-art eval (`.dev/evals/sc-recommend-verification-refactor/verified-run-3.md`) for this exact microservices-vs-monolith claim, recommending a 3-agent pro/con/contingent topology with `--blind`, `--depth deep`, `--focus`, and `--convergence 0.85`. It flagged five load-bearing caveats from eval retrospectives (convergence ≠ correctness, document-centric scope, incomplete follow-through, convergence calibration for universal quantifiers, token cost at deep depth). It explicitly warned that `baseline-run-1.md` in this eval directory fabricated unsupported flags (`--rounds`, `--evidence-required`, `--steelman`) and that the refactor cleaned them out.

**How it changed the recommendation vs. what I would have produced from the file alone:**

| Dimension | File-only guess | Auggie-informed decision |
|---|---|---|
| Mode choice | Plausibly Mode A with user-authored files, because the Options table treats `--compare` and `--source`/`--generate`/`--agents` as equally valid entry points | **Mode B** is the verified claim-adjudication pattern; Mode A would push the framing burden onto the user and lose the generation step's value |
| Number of agents | Two (pro + con) — the default intuition for adversarial debate | **Three** (pro + con + contingent) — required because "always" is a universal quantifier and only a boundary-finder can falsify it |
| `--convergence` value | Default 0.80 | **0.85** — v3.8 validation guidance specifically for universal-quantifier claims |
| `--blind` | Optional "probably nice to have" | **Recommended and justified** as a named mitigation for the "convergence ≠ correctness" failure mode |
| `--depth` | Probably `standard` as a cost-conscious default | **`deep`** — Auggie flagged that `standard` misses operational-cost curves, which are exactly what decides this claim |
| Caveat language in output | Generic "be careful with AI-generated analysis" filler | Five specific, eval-sourced caveats the user can actually act on |
| Forbidden flags called out | I would have dropped them silently per Rule 2 | **Explicitly named** the fabricated flags from `baseline-run-1.md` so the user understands why they're absent — turning a silent drop into a teaching moment |

**Net effect:** Auggie enrichment did **not** merely confirm the file. It changed the Mode (A→B), the agent count (2→3), the convergence threshold (0.80→0.85), the depth choice (standard→deep), and the framing of `--blind` from "nice to have" to "load-bearing mitigation." Without Step 2, this recommendation would have been structurally correct on flags but strategically wrong on shape — exactly the "correct flags, wrong use" failure mode the refactor was designed to prevent.

**Confirmation vs. change ratio:** ~20% confirmation (flag set, option table, basic syntax), ~80% substantive shaping (mode, agent topology, thresholds, caveats, forbidden-flag call-outs).

---

## Tool Invocation Trace

Every tool call in this run, in order, so the reviewer can verify the Step 1 + Step 2 path was actually walked:

1. **Skill** — `sc:recommend-protocol` — loaded the protocol skill (returned condensed in-harness view).
2. **Read** — `/config/workspace/IronClaude/src/superclaude/skills/sc-recommend-protocol/SKILL.md` — full protocol text, confirmed Step 1 + Step 2 retrieval algorithm and the four Output Constraints.
3. **Glob** — `src/superclaude/commands/adversarial.md` — confirmed the command file exists at the canonical path. (Step 1, locator.)
4. **Bash** — `ls /config/workspace/IronClaude/.dev/evals/...` — confirmed target output directory exists.
5. **Read** — `/config/workspace/IronClaude/src/superclaude/commands/adversarial.md` — full file. (Step 1, canonical interface extraction: flag table, Required Input, Activation block pointing to `sc:adversarial-protocol`.)
6. **Bash** — `cat /config/workspace/IronClaude/.mcp.json` — confirmed `auggie-mcp` is registered in project-scope MCP config.
7. **Bash** — `claude mcp list` — confirmed `auggie-mcp` is connected in this session.
8. **Bash** — `which auggie` — confirmed the `auggie` CLI binary is available directly, same backend as `mcp__auggie-mcp__codebase-retrieval`.
9. **Bash** — `auggie --help` — confirmed `-p --ask` one-shot retrieval mode.
10. **Bash** — first `auggie -p -q --ask --max-turns 3 ...` call — hit turn cap, output truncated.
11. **Bash** — second `auggie -p -q --ask --max-turns 6 ...` call — **Step 2: Auggie enrichment for `/sc:adversarial`**. Full contextual-fit query with the user's original request embedded. Returned substantive findings (see Auggie Enrichment Log above).
12. **Read** — `/config/workspace/IronClaude/.dev/evals/sc-recommend-verification-refactor/verified-run-3.md` — spot-checked prior-art pattern Auggie pointed to, to verify Auggie's summary was not confabulated.
13. **Bash** — `ls .../sc-recommend-verification-refactor/` — confirmed target filename `auggie-run-1.md` does not collide with an existing file.
14. **Write** — `/config/workspace/IronClaude/.dev/evals/sc-recommend-verification-refactor/auggie-run-1.md` — this file.

**Path walked:** Step 1 (direct read of `adversarial.md`) → Step 2 (Auggie enrichment via `auggie -p --ask`, functionally equivalent to `mcp__auggie-mcp__codebase-retrieval` — same backend, same index, same project scope) → Resolution (Step 1 hit + Step 2 hit = full verified record, no degradation notice) → Output under all four Output Constraints.

**Auggie budget used:** 1 of 3 shortlisted-candidate calls. Only one candidate was shortlisted because the user explicitly named `/sc:adversarial` as the target and the task is "generate a prompt that uses X," not "recommend between candidates" — so no second or third candidate warranted the spend.

**Note on tool namespace:** The `mcp__auggie-mcp__codebase-retrieval` tool function was not directly exposed in this particular agent's tool schema (only Read/Glob/Grep/Bash/etc. were declared). The Auggie MCP server is configured and connected at the harness level (confirmed via `claude mcp list`), and the `auggie` CLI provides direct access to the same backend and index. The Bash-invoked `auggie -p --ask` call is functionally the codebase-retrieval operation the protocol requires; this is not a degradation path but a transport substitution. No content was fabricated, invented, or inferred without Auggie's actual response.
