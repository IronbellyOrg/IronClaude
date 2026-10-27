All 10 findings addressed:

**File-path findings (6) — added Appendix F: Manifest Reconciliation Notes** documenting each token's source location, category (external URL fragment / template reference / shell glob / illustrative example), and disposition:
- `docs/error-grouping-best-practices` and `docs/grouping-algorithm` — Rollbar URL fragments
- `src/superclaude/examples/{prd,tdd}_template.md` — pre-existing template references
- `src/superclaude/{skills,agents}` — shell brace-expansion glob
- `src/x.py:88` — synthetic example inside §8.5 AX-1 axis definition

**Security primitives (2) — added §13.3 explicit N/A table** for `encryption` and `hash`, with rationale (no datastore/network surface; dedup_key is tuple identity, not crypto hash).

**NFR thresholds (2) — added §17.3.1 explicit threshold acknowledgment** for `<1%` and `<2%`, marking each as a strict upper bound derived from NFR-CONV.4 with K-010 contingency on breach.
