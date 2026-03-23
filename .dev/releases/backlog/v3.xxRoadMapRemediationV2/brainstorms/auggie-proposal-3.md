# Auggie MCP Proposal 3: Codebase-Grounded Remediation Plans

## Adversarial Review Summary

**Reviewed**: 2026-03-23 | **Verdict**: CONDITIONALLY ACCEPTED with scope reduction

### What Changed and Why

1. **Removed "evidence-backed effort" replacing heuristic effort levels.** The original proposal claimed Auggie file counts could replace the existing TRIVIAL/SMALL/MEDIUM/LARGE heuristic. This is false confidence. Auggie returns files that *match keywords*, not files that *must change*. A semantic search for "JWT rotation" might return 8 files that reference tokens but only 2 that need modification. The file-count-to-effort mapping (e.g., "7+ files = LARGE") is itself a heuristic — just a different, less transparent one. **Kept**: Auggie results as *advisory context* alongside the existing heuristic. **Cut**: The replacement claim and the rigid file-count thresholds.

2. **Removed the secondary Phase 3.9 impact.** The original proposal suggested Auggie-grounded effort estimates could flow backward into Step 3.9 aggregate metrics. This violates Phase Sequencing (R11) in spirit — Phase 5 enrichment should not retroactively alter Phase 3 outputs. The consolidated report metrics should reflect document-level analysis; codebase context belongs in the remediation artifact only.

3. **Added NFR/abstract-requirement exclusion as a hard rule, not just a mitigation.** The original risks table acknowledged that Auggie returns noise for abstract requirements ("system shall be horizontally scalable") but only listed it as a MEDIUM risk with a mitigation. In practice, this is the dominant failure mode. Queries for abstract NFRs will pollute the remediation plan with irrelevant file listings. The refactored version makes this an explicit skip condition in the algorithm.

4. **Capped query count and added a bail-out.** The original mentioned "max 15 queries" in the risks table but not in the implementation sketch. The refactored version embeds the cap in the algorithm and adds a bail-out: if the first 3 queries return <50% relevant results (orchestrator judgment), skip remaining queries and fall back to heuristic. This prevents wasting the entire Phase 5 on bad Auggie responses.

5. **Removed `mcp__auggie-mcp__codebase-retrieval` from `allowed-tools`.** The skill's `allowed-tools` line controls what the skill's *agents* can use. Auggie queries happen in the orchestrator during Phase 5, not in spawned agents. Adding it to `allowed-tools` would permit agents in Phase 2 to call Auggie, which is out of scope and risks uncontrolled token spend. The orchestrator already has access to MCP tools; no metadata change is needed for `allowed-tools`.

6. **Narrowed the "Codebase impact" block format.** The original example included verification commands (`uv run pytest tests/auth/`) and specific code change descriptions ("TokenManager.refresh() needs rotation logic"). This crosses the "Will Not" boundary — the skill does not prescribe implementation. The refactored format lists affected files and packages but does not suggest *what* to change in those files. That is the tasklist generator's job.

7. **Acknowledged the overlap-with-existing-tools weakness.** For many gaps, `Grep` and `Glob` can find relevant files without Auggie. The refactored proposal clarifies when Auggie adds genuine value over basic search: semantic/architectural queries where keyword matching fails. For keyword-obvious gaps, the orchestrator should prefer `Grep`/`Glob` and reserve Auggie for ambiguous cases.

### Strengths Preserved

- The core insight is sound: remediation plans that reference real code structure are more actionable than abstract checklists.
- Graceful degradation (Auggie unavailable = no change) is well-designed and preserved.
- Scoping to Phase 5 only keeps Phases 0-4 clean as document-level analysis.
- Limiting queries to CRITICAL+HIGH gaps is correct token discipline.

---

## Problem Statement

Phase 5 (Remediation Plan) currently generates patch checklists in a vacuum. When the validator identifies a gap — say, "REQ-042: JWT rotation policy is MISSING from the roadmap" — the remediation entry says something like:

```
- Action: ADD
- Change: "Add task for JWT token rotation policy implementation"
- File: roadmap.md:~line 180
```

This tells the roadmap author *what* to add but not *where the work actually lands in the codebase* or *which modules are involved*. The author must then manually investigate the codebase to write a meaningful roadmap task. This creates two failure modes:

1. **Vague remediation items** that produce equally vague roadmap tasks, which then produce vague tasklist items — the gap propagates downstream.
2. **Effort misestimation** — a "SMALL" remediation might actually require touching many files across multiple packages, but the heuristic has no signal to detect this.

The remediation plan is the skill's most actionable output, yet it is the least grounded in implementation reality.

## Proposed Integration

Add an **optional** Auggie-powered enrichment step between Step 5.1 (ordering) and Step 5.2 (patch checklist generation). When Auggie MCP is available, the orchestrator queries it for qualifying gaps to retrieve codebase context about the components that would be affected.

For each qualifying gap, the orchestrator:

1. **Extracts implementation keywords** from the gap's spec requirement text and domain tag (e.g., "JWT rotation", "token refresh", "auth middleware").
2. **Evaluates whether keywords are concrete enough** to produce useful results. Abstract/architectural requirements (NFRs, constraints without file-level specificity) are skipped.
3. **Queries Auggie** with a semantic codebase retrieval for those keywords, requesting file paths and architectural context.
4. **Attaches a codebase context block** listing affected files and packages as advisory information alongside the existing heuristic effort level.

The enriched remediation entry becomes:

```markdown
- [ ] **GAP-C01** (CRITICAL, MEDIUM): Add JWT token rotation policy task
  - File: roadmap.md:180-195
  - Action: ADD
  - Change: "Add task for JWT token rotation implementation"
  - Codebase context: (auggie-grounded, advisory)
    - src/auth/token_manager.py — token lifecycle management
    - src/auth/middleware.py — token validation
    - src/config/auth_settings.py — auth configuration
    - Affected scope: 3 existing files, 2 packages
  - Verification: re-read roadmap.md:180-195 after edit to confirm requirement addressed
  - Dependencies: [GAP-H03]
```

This provides codebase orientation to the roadmap author without prescribing implementation details.

## Phase(s) Affected

**Primary**: Phase 5 (Remediation Plan) — new sub-step 5.1b "Codebase Context Lookup" between ordering and patch checklist generation.

No changes to Phases 0-4. No changes to Phase 3 metrics. The codebase context is scoped strictly to the remediation artifact.

## Expected Value

1. **Oriented remediation**: Roadmap authors can see which codebase areas a gap touches, helping them write specific, file-aware tasks instead of vague "add support for X" entries.

2. **Effort calibration signal**: When a gap's codebase context reveals many affected files across multiple packages, it signals that the heuristic effort level may underestimate. The author can adjust accordingly.

3. **Reduced fix-and-revalidate cycles**: When remediation items reference real code structure, the roadmap author gets the fix right on the first pass instead of writing another vague task that fails re-validation.

4. **Graceful degradation**: When Auggie is unavailable (no MCP server configured, pre-code project, spec-only validation), the skill falls back to current behavior with zero impact. The enrichment is additive.

## Implementation Sketch

### New sub-step in Phase 5

```
Step 5.1b — Codebase Context Lookup (optional, requires auggie-mcp)

IF auggie-mcp is available AND project has existing codebase:

  query_count = 0
  relevance_misses = 0
  MAX_QUERIES = 10

  FOR each gap WHERE severity IN (CRITICAL, HIGH):
    IF gap.type IN (NFR, CONSTRAINT) AND gap.spec_text lacks file/module references:
      SKIP — abstract requirements produce noise, not signal.

    IF query_count >= MAX_QUERIES:
      BREAK — token budget cap reached.

    1. Extract search terms from gap.spec_text + gap.domain
    2. IF search terms are concrete keywords (function names, file paths, module names):
       PREFER Grep/Glob over Auggie — cheaper and more precise.
       ELSE:
       Call mcp__auggie-mcp__codebase-retrieval with:
         - query: "{requirement description} implementation"
         - context: "{domain} {related file paths from spec if any}"
    3. query_count += 1
    4. Evaluate response relevance (orchestrator judgment).
       IF response is irrelevant or empty:
         relevance_misses += 1
         IF relevance_misses >= 3 out of first 3 queries:
           BAIL OUT — Auggie context not useful for this codebase/spec pair.
           Add note: "Codebase context lookup abandoned — low relevance."
           BREAK
       ELSE:
         From response, extract:
           - affected_files: [path, brief description of role]
           - affected_packages: [unique parent dirs]
         Attach codebase_context block to gap record.

  FOR gaps WHERE severity IN (MEDIUM, LOW):
    Use current heuristic effort estimation only (no codebase lookup).

ELSE:
  Proceed to Step 5.2 with current heuristic effort levels.
  Add note to report: "Codebase context lookup skipped — auggie-mcp not available."
```

### Artifact changes

`04-remediation-plan.md` gains a new optional section per qualifying gap:

```markdown
  - Codebase context: (auggie-grounded, advisory)
    - {file_path} — {brief role description}
    - ...
    - Affected scope: {N} files, {N} packages
```

The existing `effort` field (TRIVIAL/SMALL/MEDIUM/LARGE) remains heuristic-based. The codebase context is supplementary information, not a replacement.

### Skill metadata update

```yaml
mcp-servers: [sequential, auggie]  # auggie added as optional
```

No change to `allowed-tools` — the orchestrator calls Auggie directly during Phase 5. Spawned agents in Phase 2 do not use Auggie.

## Risks & Tradeoffs

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Auggie returns irrelevant results** for abstract/architectural requirements | HIGH | Hard skip: NFR/CONSTRAINT-type gaps without file-level specificity are excluded from queries. Bail-out after 3 consecutive irrelevant results. |
| **Over-specificity** — grounding in current code could bias toward incremental changes when redesign is warranted | MEDIUM | Codebase context is labeled "advisory" and does not replace the gap's remediation action (ADD/EDIT/MOVE/SPLIT). The format deliberately avoids prescribing code changes. |
| **Overlap with Grep/Glob** — many gaps can be located with basic keyword search | MEDIUM | Algorithm prefers Grep/Glob for concrete keywords. Auggie reserved for semantic/architectural queries where keyword matching is insufficient. |
| **Stale codebase index** — Auggie's index may not reflect recent changes | LOW | Auggie indexes on-demand. Add freshness note: "Codebase context based on index at {timestamp}." |
| **Pre-code projects have no codebase** — greenfield specs validated before any code exists | LOW | Graceful degradation: if Auggie returns no results, fall back to heuristic. Note "no existing codebase context available." |
| **Coupling between validation and implementation** — the skill is designed as a document-level audit; adding code awareness blurs the boundary | LOW | Scoped strictly to Phase 5 output enrichment. Phases 0-4 remain document-only. Codebase context is advisory annotation, not validation input. The "Will Not" boundary is preserved. |
