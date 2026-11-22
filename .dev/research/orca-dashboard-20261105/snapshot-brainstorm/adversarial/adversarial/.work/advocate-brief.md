# Advocate Brief (shared by all advocates, Rounds 1 and 2)

Artifacts directory (ART):
/home/coder/workspaces/IronClaude/.dev/research/orca-dashboard-20261105/snapshot-brainstorm/adversarial/adversarial/

Inputs (read from disk, do not rely on summaries):
- V1: ART/variant-1-opus-architect.md (opus:architect)
- V2: ART/variant-2-sonnet-analyzer.md (sonnet:analyzer)
- V3: ART/variant-3-haiku-backend.md (haiku:backend)
- Diff analysis: ART/diff-analysis.md (diff points S-001..S-012,
  C-001..C-020, X-001..X-010, A-001..A-004; 46 scored points)
- Seed brief (the source all variants answer):
  /home/coder/workspaces/IronClaude/.dev/research/orca-dashboard-20261105/snapshot-brainstorm/seed-brief.md

Task context: a design-only spec for static ASCII five-minute chat
snapshots of an attention-first Orca multi-agent dashboard. No external
research, no product code. Do not edit any variant or any file other
than your own assigned output file.

## Advocate rules (from the sc:adversarial protocol)

1. Argue for your variant's strengths with EVIDENCE (cite sections, quotes).
2. STEELMAN opposing variants BEFORE critiquing them: state the strongest
   version of their argument, identify what they genuinely get right, only
   then critique with counter-evidence.
3. Cite specific sections, quotes, or content as evidence for every claim.
4. Acknowledge genuine weaknesses in your variant honestly.
5. Focus areas: All.
6. For each [SHARED-ASSUMPTION] point respond with exactly one of
   ACCEPT (valid, may stay implicit), REJECT (incorrect, give
   counter-evidence) or QUALIFY (partially valid, state the conditions).
   Shared assumptions to address:
   - A-001 Heartbeat or routine messages are reliably distinguishable from
     decision requests at collection time.
   - A-002 The chat reader is the acting owner of all human-required items.
   - A-003 A 40-60 line, 80-column paste fits the chat platform's
     per-message size limit and keeps the fence intact.
   - A-004 Readers act on the latest paste near its as-of time and older
     pastes remain distinguishable.
   WARNING: omitting a response for any A-NNN point will be flagged in the
   transcript as [OMISSION].

Persona activation:
- architect: structure, dependencies, long-term impact
- analyzer: evidence quality, logical consistency
- backend: data integrity, scalability, fault tolerance

## Per-point verdict table (MANDATORY in every round)

The orchestrator computes convergence from this table, so it must list
all 46 points exactly once, in this order: S-001..S-012, C-001..C-020,
X-001..X-010, A-001..A-004. Format:

| Point | Superior | Reason (one line, with a section citation) |
|-------|----------|--------------------------------------------|
| S-001 | V1 | ... |

`Superior` must be exactly one of V1, V2, V3: the variant whose approach
on that point should prevail in a merged spec. Be honest: voting for
another variant where it is genuinely better is expected and is not a
concession of the whole debate. For single-variant internal
contradictions (X-005..X-010) name the variant whose handling of that
topic should prevail. For A-001..A-004 name the variant whose treatment
of that assumption is closest to correct (or least exposed).

## Writing procedure (stub-first)

1. Write your output file immediately with all section headings and
   `<!-- TODO -->` placeholders.
2. Fill each section in place with Edit as you complete it.
3. Final file must contain no `<!-- TODO -->` markers.
4. Your final message: just the output path and one line saying whether
   all 46 table rows and all 4 A-NNN responses are present.
