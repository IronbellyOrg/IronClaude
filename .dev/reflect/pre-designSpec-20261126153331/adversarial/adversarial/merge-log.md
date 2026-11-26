# Merge Log

Merge applied from `refactor-plan.md` to `../merged-verdict.yaml` by a script run by the orchestrator, not by the merge-executor agent: the plan is a mechanical list of 21 findings and a script copies each field exactly, which avoids transcription errors. This is a departure from the pipeline's step 5 and is recorded here.

| Plan item | Applied | Note |
|---|---|---|
| 1 to 3 (M-1 to M-3, Blocking) | yes | grades and reasons copied |
| 4 to 14 (M-4 to M-14, Medium) | yes | |
| 15 to 21 (M-15 to M-21, Note) | yes | |

Result: 3 Blocking, 0 label_high, 11 Medium, 7 Note. Fields copied verbatim from the plan; evidence is the cards' own citations. Unverified until the Wave 5 evidence validator re-reads them.
