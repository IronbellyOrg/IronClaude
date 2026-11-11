**M10. The count of "27 needing a change" includes `/sc:pr-submit`, which D3 recommends keeping coordinator-only.** Expert: Wiegers (internal consistency).
- The 27 includes pr-submit (SPEC:114, SPEC:76). D3 recommends coordinator-only (SPEC:239-242). Section 4 says pr-submit is a worker candidate "only if the user accepts open decision D3" (SPEC:139).
- Recommendation: move pr-submit to a conditional row with the count stated as 26 plus one conditional.
- Priority: Low to medium.
