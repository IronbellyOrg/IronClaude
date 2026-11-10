# Revise 2

Candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place). Blocking ids: L1, L2 (review/round2.md "Reviser brief"). No self-awarded PASS. Prompt: ~/.claude/rules/prompts/document_review_loop_prompts.md, REVISE. Sub-claims of the reviewer rows R1 to R9 are cited from review/round2-t1b-1.md:90-104.

## Byte accounting
- Before: 60863 bytes. After: 62044 bytes. Net +1181.
- Gross bytes of replacement text added / replaced text deleted per finding id (each addition in the spec carries its id tag):

| id | added | deleted |
|---|---|---|
| L1 | 1849 | 754 |
| L2 | 174 | 88 |

Additions exceed deletions because each fix states the missing choice the finding calls for; no section, table or row was added.

## Per-finding rows
| id | result | where (spec text found by the id tag) |
|---|---|---|
| L1 R1 (no output location vs index-repo) | applied | WC-4 limits the stop-and-fail rule to commands with an output flag and fixes the contract location for commands without one (index-repo: repo root; research: beside the generated file); 3.1 index-repo row states the root (`inventory/commands-a.md:53`; round2-t1b-1.md:90) |
| L1 R3 (WC scope vs AC-0.4) | applied | WC-2 now splits command-side rules (unattended only) from worker-session rules (every worker run), so AC-0.4 steps 3 and 5 sit under WC-5 and WC-7 |
| L1 R4 (second status key) | applied | WC-4 names the field `worker_status` for a command whose `status` key has other values; WC-5/7.2 read it (workflow key: round2-t1b-1.md:93 citing INV-B:272) |
| L1 R5 (partial releases dependents) | applied | 2.3 now bars dependents from any Task until its report file is read |
| L1 R6 (fresh dir vs resume, workflow, file flags) | applied | 2.3 fresh directory per Task; a retry reuses the directory only when the command resumes; workflow and tdd/init-lite follow WC-4 with one Task per output file |
| L1 R8 (YAML check on REPORT.md) | applied | AC-0.4 replaces step 4 with `test -s` plus a manual status check for non-YAML reports |
| L1 R9 (retry request id) | applied | WC-5 says `--retry-request <id>` reusing the first call's id (`inventory/orca-capabilities.md:117`) |
| L2 R7 (Agent-tool call vs 4-minute split) | applied | WC-10 excludes a command's own Agent-tool fan-out, which WC-7 covers; the heartbeat role stays UNVERIFIED (`inventory/orca-capabilities.md:130`) |

Not touched: all non-blocking findings (L3 to L25). Orca runtime facts stay as the capabilities inventory marks them; none were re-checked (no Orca in this sandbox).

## Fix map
```fixmap-v1
{"id": "L1", "action": "applied", "reason": "Narrowed or specified each sub-point (output location, rule scope, status key, dependents, fresh directory, step 4 check, retry id) with short tagged edits."}
{"id": "L2", "action": "applied", "reason": "WC-10 now excludes the command's own Agent-tool fan-out so it no longer collides with WC-7."}
```
