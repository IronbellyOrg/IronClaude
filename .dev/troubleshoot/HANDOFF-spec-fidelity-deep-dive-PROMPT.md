# Handoff Prompt — Spec-Fidelity Deep Dive

Paste the fenced block below as the first message to a fresh-context agent. The agent will be running in `/config/workspace/IronClaude/` (this repo) with read access to `/config/workspace/TUIBBS-scp/` for the failing artifacts. All output goes under `IronClaude/.dev/troubleshoot/`.

---

````
You are picking up an unresolved investigation: PERSISTENT, SHAPE-SHIFTING spec-fidelity convergence failures in the IronClaude `superclaude roadmap` pipeline. The user has been fighting this across many releases — fixes either don't address the structural issue or surface new failures elsewhere. Latest concrete halt symptom: `Convergence not reached after 3 runs. Remaining active HIGHs: 54. TurnLedger: available=31, consumed=46`.

## Your operating context

- **Your cwd**: `/config/workspace/IronClaude/` (this is the IronClaude `superclaude` source repo)
- **Cross-project read access**: you can READ files under `/config/workspace/TUIBBS-scp/` (the project that triggered the failure — its merged roadmap is the input the pipeline was trying to validate against its spec). Do NOT write there.
- **All output artifacts**: write under `/config/workspace/IronClaude/.dev/troubleshoot/spec-fidelity-deep-dive-{YYYYMMDDHHMMSS}/`. Pick the timestamp at the start of your run and reuse it for every artifact you write.
- **Mode**: diagnosis-only. Do NOT modify any source code in IronClaude or TUIBBS-scp.

## Phases

This handoff has TWO mandatory phases. PHASE 0 comes BEFORE the troubleshoot invocation. Skipping it produces a shallow analysis that misses the historical pattern.

### PHASE 0 — Historical archaeology via Auggie MCP (15-25 min)

Goal: understand what's been tried, what worked, what failed, and what's NEVER been tried for spec-fidelity / convergence failures across past IronClaude releases.

Issue THREE `mcp__auggie__codebase-retrieval` queries in PARALLEL (single message, three tool calls). All three use `directory_path=/config/workspace/IronClaude`:

1. **Query A — prior remediation attempts** (`information_request`):
   "Find all past work in /config/workspace/IronClaude/.dev/releases/complete/ that addressed spec-fidelity convergence failures in the superclaude roadmap pipeline. For each release: list the commit/PR, the diagnosed root cause, the chosen fix, and any retrospective notes on whether the fix held. Specifically look at v1.4-roadmap-gen, v1.7-adversarial, unified-audit-gating-v1.2.1, unified-audit-gating-v2, obligation-vocab-alignment, and any release containing 'fidelity', 'convergence', 'remediate', or 'HIGH findings' artifacts (74 such artifacts exist under .dev/releases/complete/)."

2. **Query B — convergence engine evolution** (`information_request`):
   "Trace the evolution of the convergence engine across releases: cli/roadmap/convergence.py, fidelity_checker.py, obligation_scanner.py, remediate_executor.py, semantic_layer.py. What is the current 3-run convergence loop trying to do? Why does it cap at 3 runs and how is TurnLedger computed? Surface every code change related to the convergence loop and the rationale (commit messages, eval artifacts, release notes). Particular attention to: how 'active HIGHs' are counted, what 'remaining' means after each run, and why the loop might fail to converge in practice rather than in theory."

3. **Query C — what's NEVER been tried** (`information_request`):
   "Across all /config/workspace/IronClaude/.dev/releases/complete/ artifacts AND open tasks in .dev/tasks/to-do/, what spec-fidelity remediation strategies have been DISCUSSED but never implemented? Look for: rejected proposals in adversarial debate transcripts, open follow-up tasks related to fidelity/convergence, retrospective 'we should try X' notes that never became PRs, design alternatives in TDD/PRD documents marked as deferred. Specifically NOT what was tried — what was AVOIDED, and why."

Synthesize all three into `/config/workspace/IronClaude/.dev/troubleshoot/spec-fidelity-deep-dive-{TIMESTAMP}/historical-context.md` with sections:

- **Tried and worked**: list with provenance (release, PR/commit)
- **Tried and failed (or only partially worked)**: list with provenance + failure mode
- **Tried and reverted**: list with provenance + reason for revert
- **Discussed but never tried**: list with provenance
- **Pattern recognition**: 2-5 bullets — what does this history TELL us about the STRUCTURAL nature of the failure?

DO NOT proceed to Phase 1 until `historical-context.md` is written and has all five sections populated. If Auggie returns thin results for any branch, fall back to `Grep`/`Glob` over `.dev/releases/complete/` directly and note the degradation in the doc.

### PHASE 1 — Deepest-dive troubleshoot via /sc:troubleshoot --depth deep (20-40 min)

With `historical-context.md` written, invoke `/sc:troubleshoot` via the Skill tool. Reference the historical-context path inside the issue description so the skill's Wave 1.5 doc-grounding incorporates it.

Run this EXACT command (substituting your chosen `{TIMESTAMP}`):

```
/sc:troubleshoot "Persistent spec-fidelity convergence failure in the superclaude roadmap pipeline. Latest concrete halt: 'Convergence not reached after 3 runs. Remaining active HIGHs: 54. TurnLedger: available=31, consumed=46'. State file: /config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/.roadmap-state.json. Failing artifact: /config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/spec-fidelity.md. Merged roadmap (input to spec-fidelity): /config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/roadmap.md (passed all upstream gates: extract → opus/haiku architects → diff → debate → score → merge → anti-instinct → test-strategy → wiring-verification). Failure is RECURRING across many releases despite multiple fixes — see historical context at /config/workspace/IronClaude/.dev/troubleshoot/spec-fidelity-deep-dive-{TIMESTAMP}/historical-context.md (Phase 0 deliverable). Convergence engine source: /config/workspace/IronClaude/src/superclaude/cli/roadmap/{convergence.py, fidelity_checker.py, obligation_scanner.py, remediate_executor.py, semantic_layer.py}. Diagnose the STRUCTURAL reason this fails repeatedly — not just the immediate cause. I want maximum specialist diversity (no --type), forced Tier 2 + adversarial debate (--depth deep), and offer of remediation chain (--fix)." --depth deep --scope /config/workspace/IronClaude/src/superclaude/cli/roadmap/ --fix --output-dir /config/workspace/IronClaude/.dev/troubleshoot/spec-fidelity-deep-dive-{TIMESTAMP}/
```

**Flag rationale** (all flags verified against `/config/workspace/IronClaude/src/superclaude/commands/troubleshoot.md`):

- `--depth deep` forces Tier 2 escalation regardless of confidence (escalation-rubric.md rule 2). Tier 2 fans out 2-4 specialist agents in parallel, each produces a hypothesis card, competing fixes are debated via `sc:adversarial-protocol` in Wave 4.
- **No `--type`** (omitted, not "auto") — when signals point in multiple directions the protocol spawns from the UNION of relevant rows, capping at 4. This gives MAXIMUM specialist diversity (root-cause-analyst, devops-architect, refactoring-expert, system-architect, quality-engineer all candidates). Forcing `--type build` would narrow to 3.
- `--scope /config/workspace/IronClaude/src/superclaude/cli/roadmap/` focuses auggie+serena queries on the convergence engine source without restricting the diagnosis surface.
- `--fix` enables Tier 3 (task-builder remediation chain) — user-gated, won't auto-execute.
- `--output-dir /config/workspace/IronClaude/.dev/troubleshoot/spec-fidelity-deep-dive-{TIMESTAMP}/` pins all artifacts (hypothesis cards, fix proposals, adversarial debate transcripts, evidence validation) to a single known path so the user can audit afterward. SAME directory as Phase 0's `historical-context.md`.

**Optional intensification** (use only if cost is not a concern — adds ~30-50k Claude tokens):
- `--models tier1:opus,hypothesis:opus` biases EVERY reasoning agent to opus, increasing diagnostic depth.

**Do NOT add**: `--no-doc-discovery`, `--no-mcp`, `--no-escalate`, `--type` — each would NARROW the dive (opposite of intent).

The `/sc:troubleshoot` command is `skill-indirected` (delegates to `sc:troubleshoot-protocol`). Do NOT reimplement the protocol's phases inline; trust the skill. It will run Wave 1 real-code grounding, Wave 1.5 doc-grounding (3 parallel auggie branches across release docs / architectural docs / semantic restrictions — this is where it picks up your `historical-context.md`), Wave 1.7 single hypothesis + confidence-calibrator, Wave 2 confidence gate (will force-escalate per `--depth deep`), Wave 3 parallel hypothesis agents (2-4) with per-card confidence-calibrator, Wave 4 adversarial debate via `sc:adversarial-protocol` (when ≥2 competing fixes exist), Wave 5 evidence-validator agent before REPORT.md ships, Wave 6 Tier 3 remediation-chain offer (gated on user accept).

## PHASE 2 — Surface results to the user (5 min)

After `/sc:troubleshoot` returns, produce a short summary message containing:

1. **Path to REPORT.md** (inside the output dir).
2. **Diagnostic conclusion** (1 paragraph) — the structural root cause, not just the immediate trigger.
3. **The N debated fix proposals** (one line each, with their adversarial-debate verdict — winner / loser / score).
4. **The chosen fix** (verbatim from `adversarial/merged-output.md` in the output dir).
5. **Tier 3 remediation-chain offer** — since `--fix` was set, the skill offered the chain. Surface the literal `/task <path>` command the user will run, but do NOT execute it (user-gated per protocol).
6. **Pointer back to `historical-context.md`** so the user can audit how Phase 0 grounded the diagnosis.

## Hard constraints

- Phase 0 is BLOCKING. Phase 1's `/sc:troubleshoot` invocation REQUIRES `historical-context.md` to exist and be referenced in the issue description.
- All output artifacts go under `/config/workspace/IronClaude/.dev/troubleshoot/spec-fidelity-deep-dive-{TIMESTAMP}/`. Pick ONE timestamp at the start; reuse it.
- Diagnosis-only. Do NOT modify any code in IronClaude or TUIBBS-scp. The Tier 3 remediation chain is user-gated — surface the offer, do NOT execute `/task` yourself.
- Trust the `/sc:troubleshoot` skill — do not reimplement its waves inline. The skill knows how to do Wave 4 adversarial debate; you don't need to spawn debate agents yourself.
- Time budget total: 35-65 minutes. Phase 0 is the biggest variable.
- If `/sc:troubleshoot --depth deep` errors out (MCP unavailable, agent crash), retry once with the same flags. If still failing, report the failure verbatim — do NOT degrade silently.
- Hallucination contract: every claim in your final summary message MUST cite a real `file:line` or a real diagnostic command output. Findings that cannot be grounded are dropped, not downgraded.
````

---

## Why this shape

- **IronClaude-cwd**: all output paths use `/config/workspace/IronClaude/.dev/troubleshoot/...` per the user's directive. TUIBBS-scp paths appear ONLY as read-only references to the failing-state artifacts (state file, spec-fidelity.md, roadmap.md).
- **Phase 0 archaeology**: 3 parallel Auggie queries cover the three orthogonal axes (what was tried, how the engine evolved, what was AVOIDED). The synthesized `historical-context.md` lives in the same output dir as Phase 1's troubleshoot artifacts so they're co-located for audit.
- **`--depth deep` + omitted `--type`**: per the verified protocol, omitting `--type` when signals diverge maximizes specialist diversity (up to 4 agents instead of 2-3). This is the highest-leverage flag choice for "maximum amount of proposed-and-debated solutions" — more hypothesis cards → more candidate fixes → richer Wave 4 adversarial debate.
- **Wave 1.5 picks up `historical-context.md` naturally**: the skill's doc-grounding fan-out queries release artifacts; pointing it at the IronClaude tree means it discovers the Phase 0 synthesis without you having to manually feed it.
- **All flags verified** against `troubleshoot.md` (Rule 1, no fabrication). Trusted hand-off, not protocol reimplementation (Rule 3).
