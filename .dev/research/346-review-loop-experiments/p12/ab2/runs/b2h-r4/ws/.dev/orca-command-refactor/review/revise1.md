# Revise 1 of the Orca worker-contract spec

Brief: REVISE prompt (`~/.claude/rules/prompts/document_review_loop_prompts.md`, REVISE prompt section). Repair only the confirmed blocking ids B-1, B-3, B-5 (from `review/verify-1.md`, `confirmed: B-1, B-3, B-5`). Leave Medium and minor findings alone.

- Candidate: `specs/orca-worker-contract-spec.md`
- Pre-revision sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (identical to `specs/history/spec-v1.md`)
- Revised sha256: `97f56a6e69838dc9f80dfae9d1e8e0aa95413656b2559e687870566b2996ca6a`

## Byte accounting

| Measure | Bytes |
|---|---|
| Before | 57763 |
| After | 58887 |
| Net | +1124 |
| Added, total | 2120 |
| Deleted, total | 996 |

Per finding id (added / deleted; 2120 - 996 = 1124 net, which matches):

| Id | Added | Deleted | Net | Edits (spec lines after revision) |
|---|---|---|---|---|
| B-1 | 216 | 64 | +152 | spec:79 |
| B-3 | 1403 | 689 | +714 | spec:62, :73, :76, :83, :87, :90, :92, :198 |
| B-5 | 501 | 243 | +258 | spec:63, :200 |

The BEFORE/AFTER text for each edit is in the spec diff against `specs/history/spec-v1.md`. The cited B-5 wording in the WC-5 row is also the basis of the B-3 workflow row (spec:92): the pre-creation STOP is named under both ids.

## Findings

| Id | Disposition | Where (spec, after revision) | Reason and evidence |
|---|---|---|---|
| B-1 | Applied | spec:79 | Section 3.1 said "The only command changes are the small fixes in the last column", which contradicts P1 (spec:159, "accepted by every command in sections 3.1 and 3.2") and AC-1.1 (spec:195, a `## Unattended mode` section in every 3.1 command). The chosen rule is the one P1 already states: every 3.1 command gets the flag and section, a no-op where it has no gate. Brainstorm and init-lite (no fix, spec:84 and :87 before revision) now carry it through that sentence. The rule is stated once and nothing else is added. Verifier: `review/verify-1.md`, row B-1 (confirmed). |
| B-3 | Applied | WC-4 at spec:62; section 2.3 at spec:73; section 3 intro at spec:76; adversarial row at spec:83; init-lite row at spec:87; tdd row at spec:90; workflow row at spec:92; AC-1.4 at spec:198 | WC-4 required `<output-dir>/return-contract.yaml` for every command, but three rows broke that path. Adversarial (spec:83) asked for `<output>/adversarial/return-contract.yaml`. Workflow (spec:92) writes into `.dev/tasks/to-do/<id>/`. Tdd (spec:90) and init-lite (spec:87) take `--output <file>`, not a directory. The rule now has three parts: a directory output gives `<output-dir>/return-contract.yaml`; a file output gives `<file's directory>/<command>-return-contract.yaml`; workflow is the named exception, because its package id exists only after the command creates it, so the coordinator learns the path from `worker_done --report-path`. Adversarial moves to the directory rule (spec:83), and tdd and init-lite name their file-rule paths. Evidence: adversarial's real runs wrote the contract in two places (`inventory/commands-a.md:60`); workflow's contract is `.dev/tasks/to-do/<id>/return-contract.yaml` (`inventory/commands-b.md:272`). Verifier: `review/verify-1.md`, row B-3 (confirmed). |
| B-5 | Applied | WC-5 at spec:63; AC-2.2 at spec:200 | WC-5 sent `--outcome succeeded` "otherwise", so an empty, truncated, unparseable or unknown-status contract settled the Task `completed` and started dependents (`inventory/orca-capabilities.md:76-77`, `:84-88`; the Task settles on the outcome). WC-5 now sends `failed` for any contract that is missing, zero bytes, truncated, unparseable, lacks `status`, or has a status outside the four values in spec:262. It sends `succeeded` only for a parsed `succeeded` or `partial`. AC-2.2 gains the three fixture cases. Verifier: `review/verify-1.md`, row B-5 (confirmed). |

## Rejected or not revised (noted, unactioned)

| Id | Disposition | Reason |
|---|---|---|
| B-2 | Not revised; noted, unactioned | Verifier rejected it (`review/verify-1.md`, row B-2): the quoted text exists, but the failure needs `REPORT.md` to be something other than a YAML mapping with `status` and `command`, and the candidate never states `REPORT.md`'s format. The premise rests on `inventory/commands-b.md:49`, which is not in the workspace (UNVERIFIED here). |
| B-4 | Not revised; noted, unactioned | Verifier rejected it (`review/verify-1.md`, row B-4): the wrong outcome needs the content of the headless auto-accept rule, which is defined in `remediation-handoff.md`, not in the workspace. The verifier also noted that SA-6 (spec:151) was misstated in the finding. |

## Checks run

- The 13 replacements each matched exactly once in the pre-revision text (asserted before writing).
- Byte totals reconcile: 57763 - 996 + 2120 = 58887.
- Edits are confined to the spec. No other file was written.
- No text in the spec, outside the cited edits, was altered. The diff against `specs/history/spec-v1.md` shows only the lines listed above.
- Not run: the self-check and spec-panel. The brief did not ask for them, and the REVISE prompt does not run a review.

## Citation status

- `inventory/commands-a.md:60`, `inventory/commands-b.md:272`, `inventory/orca-capabilities.md:73-80` were read in this workspace and match the claims above.
- Claims that rely on `src/superclaude/...`, `.dev/codegraph-migration/...` or `~/.claude/...` files are not in the workspace and are UNVERIFIED here. The revisions do not add any new such claims.
