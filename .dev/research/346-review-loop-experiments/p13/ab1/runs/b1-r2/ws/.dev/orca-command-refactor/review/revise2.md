# Revise 2

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place). Blocking id: L1 (`review/round2.md` Reviser brief; sub-findings L1.t1b-1 and N1-N4, N6, N7). Minor and Medium findings (L2-L30) untouched. No self-awarded PASS. Line numbers are spec lines after edit; the review's evidence was read in the spec itself, so no inventory citation was needed (none added).

## Byte accounting

Size before: 60598 bytes. Size after: 61628 bytes. Net +1030. Added 1069, deleted 39 (byte-level diff of the whole file).

| id | bytes added | bytes deleted |
|---|---|---|
| L1 | 1069 | 39 |

Per sub-finding (approximate, added): AC-1.1 exemption about 90; N1 (AC-1.2) about 215; N2 (WC-6, section 2.3) about 260; N3 (WC-4) about 200; N4 (section 2.3) about 70 added, 39 deleted ("verdict" check narrowed); N6 (WC-5, AC-0.4) about 190; N7 (WC-4) about 170. Every addition carries `[L1]` plus its sub-finding tag in the spec.

## One row per finding id

| id | disposition | where applied and why |
|---|---|---|
| L1 | applied | AC-1.1 (line 195): exempts `/sc:load` and asserts load has no section, matching section 3 intro and section 6 P1 row (load "usage line only"). AC-1.2 (line 196, N1): excludes load and passes only the output flag the command's section 3 row gives, none for workflow, cleanup-audit, index-repo. WC-4 (line 62, N3): fixed-output commands put the contract in their fixed location (cleanup-audit `.claude-audit/`, index-repo beside `PROJECT_INDEX.md`), report-path-only commands (troubleshoot `REPORT.md`) beside the report. WC-4 (N7): a workflow stop before its package exists carries the question in the first sentence of the `worker_done` body, with no `--report-path`. WC-5 (line 63, N6) and AC-0.4: a non-empty Markdown report with no `status` field counts as succeeded, which defines the troubleshoot outcome match. WC-6 and section 2.3 (lines 64, 73, N2): a new output directory only where the command has an output flag; fixed-output commands have the old `return-contract.yaml` deleted before a retry. Section 2.3 (N4): the coordinator checks the contract `status` and reads the verdict from `report_path`, instead of requiring a verdict field the contract lacks (text narrowed, not a new field). |

## Fix map

```fixmap-v1
{"id": "L1", "action": "applied", "reason": "AC-1.1/AC-1.2 exempt load and use each row's real output flag; WC-4 states fixed-output and report-only locations and the workflow pre-package question channel; WC-5/AC-0.4 define status-less Markdown reports; WC-6/2.3 handle fixed-output retry and narrow the verdict check."}
```
