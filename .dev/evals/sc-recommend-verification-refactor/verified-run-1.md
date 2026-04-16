---
run_label: verified-run-1
timestamp: 2026-04-15T17:29:11+00:00
query: "generate a prompt that uses /sc:adversarial to validate the claim that microservices architecture is always preferable to monoliths for new startup projects"
---

# /sc:recommend — Recommendation Output

## 1. Header

- **Project Analysis**: Architectural decision validation — adversarial debate framing of an absolutist claim ("microservices always preferable to monoliths for new startups")
- **Language Detected**: English (auto)
- **Expertise Level**: Intermediate (architectural reasoning task; no beginner/expert override supplied)
- **Primary Category**: api_category (architecture/microservices keywords) with create_category overlay (the request is to *generate a prompt*)
- **Recommended Persona**: `--persona-architect` (primary), `--persona-analyzer` (secondary)
- **Context Verification**: `/sc:adversarial` command file inspected at `src/superclaude/commands/adversarial.md`; flag set confirmed against authoritative source before recommendation issued.

## 2. Main Recommendation

### Primary Command

The user's request is to *produce a prompt* that invokes `/sc:adversarial` against a specific claim. The recommendation therefore has two layers: (a) the `/sc:adversarial` invocation the generated prompt should expand to, and (b) the supporting SuperClaude commands for drafting and validating that prompt.

**Generated Prompt (the artifact the user asked for)**

```
/sc:adversarial --source claim-microservices-vs-monolith.md \
  --generate architecture-assessment \
  --agents opus:architect,opus:analyzer,sonnet:architect \
  --depth deep \
  --focus tradeoffs,scalability,operational-cost,team-size-fit \
  --convergence 0.85 \
  --blind \
  --interactive \
  --output .dev/releases/current/microservices-claim-review/
```

Rationale for each flag (all verified against the authoritative command file):

- `--source` — points at a short markdown file stating the absolutist claim plus startup context (team size, runway, domain). Required input for Mode B.
- `--generate architecture-assessment` — tells the pipeline what kind of artifact each agent should produce from the source claim.
- `--agents opus:architect,opus:analyzer,sonnet:architect` — three variant generators with distinct persona lenses. Three agents is the minimum that produces meaningful triangulation without inflating cost.
- `--depth deep` — the claim is absolutist ("always"), so the debate needs the most thorough depth tier to surface edge cases and counterexamples.
- `--focus tradeoffs,scalability,operational-cost,team-size-fit` — constrains the debate to the axes on which the microservices-vs-monolith claim actually turns, preventing drift into tangential concerns.
- `--convergence 0.85` — slightly above default (0.80). For a claim framed as universal, the bar for declaring alignment should be higher so dissenting evidence is not smoothed over.
- `--blind` — strips model identity before comparison so the merge decision is driven by argument quality, not brand bias.
- `--interactive` — pauses at decision points so the human reviewer can inject startup-specific constraints the agents cannot know.
- `--output` — routes the six standard artifacts (diff-analysis, debate-transcript, base-selection, refactor-plan, merge-log, merged output) into a dedicated review directory.

### Supporting Commands (to produce and validate the prompt itself)

1. `/sc:design --seq --ultrathink` — draft the source claim file and debate framing before handing to `/sc:adversarial`.
2. `/sc:adversarial ...` (as above) — execute the adversarial validation run.
3. `/sc:reflect` — post-run validation of the merged conclusion against the original absolutist framing.

### Quick Start

Step 1. Create `claim-microservices-vs-monolith.md` containing the claim verbatim and 4–6 lines of startup context (team size, runway, expected load, domain).
Step 2. Run the `/sc:adversarial` command shown above.
Step 3. Review the debate transcript and merged architecture-assessment artifact in the output directory.

## 3. Enhanced Section

### Smart Flag Recommendations

- Claim is universal/absolutist → `--depth deep` and raised `--convergence 0.85` rather than defaults.
- Cross-model evaluation desired → `--blind` to neutralise model-identity bias.
- Human-in-the-loop warranted (startup context varies) → `--interactive`.
- Scoped debate axes → `--focus tradeoffs,scalability,operational-cost,team-size-fit`.

Flags deliberately omitted: `--compare` (Mode A is not applicable — we are generating variants, not comparing pre-existing files), `--pipeline` / `--pipeline-parallel` / `--pipeline-resume` / `--pipeline-on-error` (single-phase generate+compare is sufficient for one claim), `--auto-stop-plateau` (the claim is narrow enough that plateau detection is not needed).

### Time Estimate (no `--estimate` flag passed, indicative only)

- Source file drafting: 15–30 minutes
- Adversarial run at `--depth deep` with three agents: typically the longest single phase; budget accordingly
- Human review at interactive decision points: 20–40 minutes
- Reflection pass: 10–15 minutes

### Alternatives (no `--alternatives` flag passed, surfaced briefly)

- Swap `--agents` to include a `sonnet:analyzer` for a fourth lens if convergence stalls.
- Drop `--blind` if you want persona attribution visible in the transcript for teaching purposes.
- Lower `--depth` to `standard` if the claim needs a faster first pass before committing to `deep`.

### Community Data

Not available — `--community` flag not passed and no synthetic metrics will be fabricated.

## 4. Notes on Protocol Fidelity

- This recommendation cites only flags present in `src/superclaude/commands/adversarial.md`.
- Candidate flags considered but dropped because they could not be verified against the command file: none surfaced during verification — all flags used above appear in the options table of the authoritative file.
- The `/sc:adversarial` protocol is not reimplemented here: no debate rules, round counts, steelman strategy, scoring formula, or phase-by-phase breakdown is embedded. Those belong to `/sc:adversarial` itself and will expand when the user runs the generated command.
