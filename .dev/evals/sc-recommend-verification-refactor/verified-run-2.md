---
run_label: verified-run-2
timestamp: 2026-04-15T17:29:23+00:00
query: "generate a prompt that uses /sc:adversarial to validate the claim that microservices architecture is always preferable to monoliths for new startup projects"
---

# /sc:recommend — Recommendation Output

## 1. Header

- **Project Analysis**: Prompt engineering task — user wants a ready-to-run `/sc:adversarial` invocation that stress-tests an architectural claim ("microservices are always preferable to monoliths for new startup projects"). This is a single-artifact architectural-debate scenario, not a codebase modification.
- **Language Detected**: English (auto)
- **Expertise Level**: Intermediate (default — user phrased request in domain-technical terms but did not specify level)
- **Primary Category**: `api_category` (microservices/monolith architectural comparison) with secondary `improve_category` signal (critical evaluation / refactoring of a claim)
- **Persona**: `--persona-architect` (primary, systems-design + scalability tradeoffs), `--persona-analyzer` (secondary, claim validation + evidence)
- **Context Retrieval & Verification**: `src/superclaude/commands/adversarial.md` was read to confirm real flags before recommending. Only verified flags are cited below; unverifiable candidates were dropped silently. The `/sc:adversarial` protocol is NOT reimplemented here — the command's own protocol owns debate mechanics, scoring, and merge logic.

---

## 2. Main Recommendation

### Primary Command

The user's request is to *generate a prompt*, not to execute it. The deliverable is the prompt text below. Because `/sc:adversarial` requires **2–10 artifacts** to compare (it cannot debate a single claim in isolation), the prompt must stage two opposing position artifacts first, then invoke `--compare`.

**Recommended prompt (copy-paste ready):**

```
I want to rigorously validate the claim:
  "Microservices architecture is always preferable to monoliths
   for new startup projects."

Step 1 — Produce two position artifacts in the current working dir:
  - pro-microservices.md: strongest good-faith case FOR the claim
    (include scaling, team autonomy, deploy independence, polyglot,
     failure isolation, hiring signal). Cite concrete scenarios.
  - pro-monolith.md: strongest good-faith case AGAINST the claim
    (include operational overhead, distributed-systems tax, latency,
     observability cost, team size, time-to-market, Fowler's
     "monolith-first"). Cite concrete scenarios.
  Each file: ~600-900 words, same structure, no strawmen.

Step 2 — Run structured adversarial debate:
  /sc:adversarial --compare pro-microservices.md,pro-monolith.md \
    --depth deep \
    --focus tradeoffs,evidence,context-fit,failure-modes \
    --convergence 0.85 \
    --blind \
    --output .dev/adversarial/microservices-vs-monolith/

Step 3 — Read the generated artifacts in the output dir
  (diff-analysis, debate-transcript, base-selection, refactor-plan,
   merge-log, merged output) and report whether the claim survives
   as stated, survives with qualifications, or fails.
```

### Why this shape

- `--compare` is the only mode that fits a binary claim-vs-counterclaim evaluation with existing files.
- `--depth deep` because "always preferable" is a universal quantifier — it needs the strongest interrogation tier.
- `--focus tradeoffs,evidence,context-fit,failure-modes` narrows the debate to the axes that actually decide the claim (startup context, empirical evidence, failure modes) instead of diffusing across all dimensions.
- `--convergence 0.85` raises the alignment bar above the 0.80 default; a universal claim should not pass on a loose threshold.
- `--blind` strips authorship markers so the debate scores positions, not provenance.
- `--output` routes all 6 artifacts to a dedicated directory for later review.

### Additional (Secondary) Recommendations

1. **Multi-perspective generation first** (optional upgrade, if the user wants more than two voices before debating):
   ```
   /sc:adversarial --source claim-brief.md --generate position-paper \
     --agents opus:architect,opus:analyzer,sonnet:backend \
     --depth deep --blind \
     --output .dev/adversarial/microservices-vs-monolith/
   ```
   Use when the user wants three model/persona variants instead of two hand-written files.

2. **Pre-debate research pass** to harden both position artifacts with citations:
   ```
   /sc:research "microservices vs monolith startup outcomes" --depth deep
   ```
   Feed the findings into `pro-microservices.md` and `pro-monolith.md` before `--compare`.

3. **Post-debate validation** of the merged verdict:
   ```
   /sc:reflect --on .dev/adversarial/microservices-vs-monolith/merge-log.md
   ```
   Confirms the base-selection rationale holds up on re-read.

### Quick Start (minimum viable flow)

```
# 1. Write the two position artifacts (manually or via /sc:research + /sc:document)
# 2. Execute:
/sc:adversarial --compare pro-microservices.md,pro-monolith.md \
  --depth deep --focus tradeoffs,evidence,context-fit,failure-modes \
  --convergence 0.85 --blind
# 3. Read the merged artifact and debate transcript.
```

---

## 3. Enhanced Details

### Smart Flags (verified against `src/superclaude/commands/adversarial.md`)

| Flag | Value | Rationale |
|------|-------|-----------|
| `--compare` | `pro-microservices.md,pro-monolith.md` | Only mode that fits a 2-artifact claim evaluation |
| `--depth` | `deep` | Universal-quantifier claim ("always") demands deepest tier |
| `--focus` | `tradeoffs,evidence,context-fit,failure-modes` | Narrow to axes that decide the claim |
| `--convergence` | `0.85` | Stricter than 0.80 default for a universal claim |
| `--blind` | enabled | Score positions, not authors |
| `--output` | `.dev/adversarial/microservices-vs-monolith/` | Keep all 6 artifacts together |
| `--interactive` | *(optional)* | Add if the user wants to gate each debate step |
| `--auto-stop-plateau` | *(optional)* | Useful only if this becomes a pipeline; leave off for single compare |

Flags NOT recommended (and why):
- `--pipeline` / `--pipeline-parallel` / `--pipeline-resume` / `--pipeline-on-error`: single-compare scenario, no DAG needed.
- `--source` / `--generate` / `--agents`: only if the user opts into the Mode B upgrade above.

### Time Estimate (intermediate, medium scope)

- Drafting the two position artifacts: 45–90 min
- `/sc:adversarial` deep debate execution + review: 30–60 min
- Merge-log reading + verdict writeup: 15–30 min
- **Total**: ~1.5–3 hours

### Alternatives

| Approach | When to pick it | Tradeoff |
|----------|-----------------|----------|
| Two hand-written positions + `--compare` (recommended) | Want tight control over the steelman on each side | More manual drafting time |
| Mode B with `--source` + `--generate` + `--agents` | Want model/persona diversity without hand-drafting | Less control over what each position emphasizes |
| `/sc:spec-panel` instead | Want expert-voice breakdown rather than head-to-head debate | Produces commentary, not an adversarial verdict |

### Notes

- The claim contains "always" — a universal quantifier. The debate only needs one well-supported counterexample category (e.g., 2-engineer startup shipping an MVP in 8 weeks) to falsify it. Keep that standard in mind when reading `merge-log.md`.
- `/sc:adversarial` will not itself declare the real-world claim true or false; it produces a merged artifact with provenance. The user makes the final call from the transcript + merge log.
- Protocol mechanics (debate steps, scoring, refactor-plan generation) are owned by `/sc:adversarial` and are intentionally not restated here.
