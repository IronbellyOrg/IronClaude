# Option A: draft PR with a label (the Coder pattern)

- Push the bump branch, open a DRAFT PR titled "... [proof failed]" with label `needs-codegraph-proof`, the failed stage and the tail of the proof log in the body.
- Integrity failures (class 1) are treated the same way.
- Rationale: one artifact holds the diff and the evidence; draft cannot be merged; proven in Coder.
- Cost: an integrity failure (possible tampering) still pushes a branch whose pin points at unverified bytes; the draft looks like routine work in the PR list.
