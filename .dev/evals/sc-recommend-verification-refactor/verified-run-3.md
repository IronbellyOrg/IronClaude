# verified-run-3

- **Run label:** verified-run-3
- **Timestamp:** 2026-04-15T17:29:24+00:00
- **Query:** `generate a prompt that uses /sc:adversarial to validate the claim that microservices architecture is always preferable to monoliths for new startup projects`

---

## Header

- **Project Analysis:** Meta-request — user wants a crafted prompt (not direct execution) that drives `/sc:adversarial` to stress-test an architectural claim. Category match: `api_category` (microservices/architecture keywords) + `improve_category` (validate/critique). Domain is architectural decision validation.
- **Language Detected:** English (auto)
- **Expertise Level:** Intermediate (balanced, technical phrasing; assumes familiarity with adversarial debate artifacts)
- **Primary Persona:** `--persona-architect` (systems design, trade-off analysis)
- **Supporting Personas:** `--persona-analyzer` (claim decomposition), `--persona-scribe` (prompt authoring)
- **Context Retrieval & Verification:** Read `src/superclaude/commands/adversarial.md`. Flag set below is restricted to verified options from that file; unverifiable candidates were dropped silently. Debate mechanics (step breakdown, scoring, round counts) are intentionally omitted — they live in the adversarial protocol and must not be duplicated here.

---

## Main Recommendation

### Primary Command — the generated prompt

The recommended prompt is a Mode B invocation. The claim under test is comparative and absolute ("always preferable"), so the cleanest adversarial setup is: author a neutral source brief, generate opposing architectural recommendation variants from it with distinct personas, and let `/sc:adversarial` drive the structured comparison.

**Step 1 — Author the source brief** (`claim-source.md`):

```markdown
# Claim Under Test
"Microservices architecture is always preferable to monoliths for new startup projects."

# Context
- Audience: 2-10 person early-stage startup, pre-product-market-fit
- Evaluation horizon: 0-24 months from founding
- Constraints to weigh: team size, deploy cadence, operational overhead,
  cost, iteration speed, hiring, failure modes, refactor cost, time-to-first-revenue
- Deliverable per agent: an architectural recommendation document that
  takes an explicit position on the claim and defends it with evidence
```

**Step 2 — Invoke /sc:adversarial (the generated prompt to hand to Claude):**

```bash
/sc:adversarial \
  --source claim-source.md \
  --generate design \
  --agents opus:architect:"steelman the pro-microservices position for startups; defend the 'always preferable' claim with concrete evidence",opus:architect:"steelman the pro-monolith position for startups; attack the 'always' universal claim and defend modular-monolith-first",sonnet:analyzer:"take a contingent/it-depends position; identify the decision boundaries that flip the answer" \
  --depth deep \
  --focus tradeoffs,operational-cost,team-size,iteration-speed,failure-modes \
  --convergence 0.85 \
  --blind \
  --output .dev/evals/microservices-vs-monolith-startup/
```

**Why this shape:**
- `--source` + `--generate design` + `--agents` is Mode B, which is the verified path for "make opposing artifacts, then debate them."
- Three agents (not two) because the claim uses the universal quantifier "always"; a contingent third position is needed to surface the boundary conditions that falsify a universal claim.
- `--depth deep` is verified and appropriate for architectural trade-offs where shallow debate would miss operational cost curves.
- `--focus` is narrowed to the axes that actually decide this claim in startup contexts; leaving it unset would debate everything.
- `--blind` removes model/persona identity before comparison so the merge isn't swayed by which agent "sounds like the architect."
- `--convergence 0.85` is slightly above default (0.80) because a universal-quantifier claim rarely deserves the benefit of the doubt — we want the merged verdict to only assert "always" if agents genuinely align near-unanimously.
- `--output` is set so the six standard artifacts land in an eval-scoped directory.

### Additional Recommendations

- **Add `--interactive`** if you want to inspect the debate transcript before the merge step commits to a verdict — useful when the claim is politically charged and you want a human checkpoint.
- **Add `--auto-stop-plateau`** if you plan to re-run with pipeline mode later; it halts cleanly when agents stop moving.
- **Do not** pass flags like `--rounds`, `--evidence-required`, `--verdict-per-claim`, or `--measure-first` — these are not part of `/sc:adversarial`'s interface. Debate structure, evidence requirements, and per-claim verdicts are already handled internally by the adversarial protocol; re-specifying them inline is both unsupported and redundant.

### Quick-Start (copy-paste ready)

1. Create `claim-source.md` with the brief from Step 1.
2. Run the `/sc:adversarial` command from Step 2.
3. Read `.dev/evals/microservices-vs-monolith-startup/debate-transcript.md` and `base-selection.md` to see which position survived.
4. Treat the merged output as the validated (or invalidated) answer to the "always preferable" claim.

---

## Enhanced Details

### Smart Flag Rationale (verified flags only)

| Flag | Value | Why |
|------|-------|-----|
| `--source` | `claim-source.md` | Mode B entry point; gives every agent the same framing |
| `--generate` | `design` | The artifact type matching architectural recommendations |
| `--agents` | 3 specs (pro / con / contingent) | Universal-quantifier claim needs a boundary-finder, not just two sides |
| `--depth` | `deep` | Trade-off claims lose fidelity at `quick` or `standard` |
| `--focus` | `tradeoffs,operational-cost,team-size,iteration-speed,failure-modes` | Confines debate to the axes that actually decide startup architecture |
| `--convergence` | `0.85` | Raises bar above default 0.80; a universal claim shouldn't pass on weak alignment |
| `--blind` | on | Prevents persona-identity bias in the merge |
| `--output` | `.dev/evals/microservices-vs-monolith-startup/` | Keeps the 6 standard artifacts scoped to this eval |

### Expected Artifacts (produced by /sc:adversarial, not by this recommendation)

`/sc:adversarial` will emit its standard artifact set into the `--output` directory. This recommendation does not replicate or prescribe the internal steps — consult `/sc:adversarial` documentation for artifact semantics.

### Expertise-Level Note (intermediate)

The prompt above is written for someone comfortable reading a debate transcript and interpreting a convergence score. If you want a beginner-friendly version, add `--interactive` and `--depth standard`, and drop the third contingent agent — the trade is slower signal for easier review.

### Boundaries of This Recommendation

- This recommendation produces the **prompt**. It does not execute `/sc:adversarial`.
- Domain correctness of the merged verdict is `/sc:adversarial`'s concern for structure, and the calling user's concern for substance — `/sc:recommend` takes no position on whether microservices actually are or aren't preferable.
- Flags cited here were verified against `src/superclaude/commands/adversarial.md` at the timestamp above. Any flag not appearing in that file is intentionally absent.
