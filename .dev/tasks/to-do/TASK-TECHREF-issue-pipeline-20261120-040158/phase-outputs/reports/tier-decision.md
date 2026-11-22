# Tier decision

- **Depth Tier:** Standard. Six research agents (top of the Standard band, 4-6) because the scope is cross-cutting. Target about 1,300 lines plus the removed-code appendix. This is a deliberate tier decision recorded in research-notes.md (requested by team-lead), not a downgrade.
- **QA intensity:** standard.
  - Gate 1 (research completeness): 1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative = 3 agents.
  - Gate 2 (synthesis quality): the same three lenses, each in 2 partitions (synth-01..03 and synth-04..06) = 6 report agents.
  - Gate 3 (final document lens QA): 3 rf-qa structural + 3 rf-qa-qualitative content + 1 domain lens (code-example-accuracy) = 7 agents.
  - Gate 4 (source fidelity): 2 rf-qa fidelity agents (semantic-coverage, detail-preservation).
  - Verification rounds: 2 agents (1 rf-qa + 1 rf-qa-qualitative). Max 2 fix cycles per gate, then HALT and message team-lead.
- **Phase 4 web research:** skipped; rationale recorded in Phase 4 (repo-internal subject; external sources cannot change verified code findings; no repository details go to outside services).
- Source: BUILD-REQUEST.md and research-notes.md (Depth Tier line and TEMPLATE_NOTES); no new decision added.
