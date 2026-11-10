# Revise 1

Candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place). Blocking ids: L1, L2, L13 (review/round1.md:337-341). No self-awarded PASS.

## Byte accounting
- Before: 57763 bytes. After: 60863 bytes. Net +3100.
- Per finding id (gross bytes of replacement text added / bytes of replaced text deleted; each addition in the spec carries its id):

| id | added | deleted |
|---|---|---|
| L1 | 3045 | 1504 |
| L2 | 2328 | 1012 |
| L13 | 680 | 437 |

Additions exceed deletions because each fix states a missing rule the finding calls for; no new section or table was added (L13 adds one fenced block under 7.1, replacing a table cell that could not hold the command).

## Per-finding rows
| id | result | where (spec lines after edit; find with the id tag) |
|---|---|---|
| L1 (contract path and P0 inconsistencies) | applied | 3.1 intro (P0 runs without `--unattended`, flag arrives in P1; covers brainstorm/init-lite); adversarial row now states `<output>/adversarial/return-contract.yaml`; WC-4 adds adversarial, file-output (tdd/init-lite), workflow-generated and no-output-location rules, four-value `status` beside existing values, and replaces "Orca does not check the file" with UNVERIFIED (`inventory/orca-capabilities.md:79`); WC-5 maps missing/unknown/unparseable status to failed and adds `--retry-request` (`orca-capabilities.md:117`); WC-6 allows implicit resume and a brief-passed fresh directory; 2.3 requires fresh directory per Task and retry, no dependents before the contract is read, no re-dispatch of blocked Tasks without a new answer; AC-0.4 uses the existing report file and no `--unattended`, and the step-5 check now covers the Agent-tool wrapper; P1 and AC-1.1 exclude load (its row says it writes no report, `commands-b.md:57-65` via spec row); AC-1.4 matches the adversarial path. |
| L2 | applied | WC-1 numeric 30 s fallback (`EVIDENCE.md:45,56` as cited in WC-1); WC-2 scope (WC-2..12 only under `--unattended`), tool-permission prompts, `--unattended` plus `--interactive`, flag only on the command line; WC-3 answer flag rule and ask-versus-blocked outcome; E2 same-tool-set wording; WC-10 heartbeat role UNVERIFIED and Agent-tool wait; WC-11 scoped to unattended and one Task per worktree for fixed-output commands (index-repo `commands-a.md:53`, release-split `commands-b.md:37`, cleanup-audit); 2.3 worktree placement rule; SA-4 override statement and SA-3 precedence; index row; AC-2.2 runs with no `ask`. |
| L13 | applied | AC-C1 moved to a fenced block with an unescaped `|` alternation and scanning commands, skills and agents only; SA-2 now lets core files describe Orca, consistent with P0 adding an Orca section to HOW-WE-WORK.md. |

Not touched: all non-blocking findings (L3-L12, L14-L23). Sub-points of L1/L2 that depend on facts outside the workspace (Orca runtime behaviour of the breaker, `agentWait`) are carried as stated in the capabilities inventory and remain UNVERIFIED where it marks them.

## Fix map
```fixmap-v1
{"id": "L1", "action": "applied", "reason": "Aligned P0 smoke checks, contract path rules, outcome mapping and retry/fresh-directory rules so AC-0.4, AC-1.1 and WC-4 to WC-6 can pass together."}
{"id": "L2", "action": "applied", "reason": "Scoped WC-2 to WC-12 to unattended mode and closed the permission-prompt, ask-versus-blocked, fallback-number and shared-output gaps with narrow additions."}
{"id": "L13", "action": "applied", "reason": "Rewrote AC-C1 with a working alternation and a scope that matches SA-2."}
```
