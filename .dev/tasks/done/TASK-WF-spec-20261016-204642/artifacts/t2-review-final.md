# Task 2 independent re-QA

Verdict: compliant. All five task AC and the source's supplied-thread-ID requirement are met after one fix pass; no extra scope or remaining reproduced gap.

- T2.AC1: complete guarded REST and GraphQL pagination; malformed/error/partial data produces false source flags.
- T2.AC2: raw nullable locations, root/thread/review identities, author/body, resolution and outdated flags survive file-backed assembly.
- T2.AC3: root-only comments(first:1), all REST/GraphQL targets pinned to the resolved repository.
- T2.AC4: supplied --thread-id selects only the intended PR thread and must match root --comment-id before skip or write; omission retains paginated root lookup. Missing/conflicting identities never fall back. Resolved threads are skipped before replying.
- T2.AC5: independent re-QA reran103 adapter/static tests and both shell syntax checks successfully. Open-thread writes preserve reply-before-resolve and validate responses.

Snapshot head-race flags, observed_at, finite pagination guards and ARG_MAX-safe staging remain present. No real external mutations were performed by reviewer tests.
