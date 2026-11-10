# Revise 1 (REVISE prompt, document_review_loop_prompts.md)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place)
baseline (before revision): sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
prior report: .dev/orca-command-refactor/review/round1.md (review: 1 of 3, verdict FAIL)
IDS revised: M2, M4, M6, M8, M9, M10, M11, M12

## Byte accounting

- Size before: 57763 bytes
- Size after: 61053 bytes (sha256 0e53b436d774ed5d6bf97ec9ffac93472d2f0ec0eb53b20ecebda159b8c5d3e2)
- Net: +3290 bytes

Per finding id (bytes deleted / added / net; a shared edit is counted under the id named in its own text):

| Id | Edits | Deleted | Added | Net |
|---|---|---|---|---|
| M2 | 2 | 112 | 256 | +144 |
| M4 | 1 | 129 | 329 | +200 |
| M6 | 1 | 182 | 677 | +495 |
| M8 | 2 | 101 | 384 | +283 |
| M9 | 2 | 61 | 1129 | +1068 |
| M10 | 1 | 339 | 852 | +513 |
| M11 | 1 | 111 | 398 | +287 |
| M12 | 1 | 71 | 371 | +300 |
| Total | 11 | 1106 | 4396 | +3290 |

Check: 57763 + 3290 = 61053.

## Findings

| Id | Disposition | Where applied in the spec (section, step, row) | Bytes (-/+) |
|---|---|---|---|
| M2 | applied | Section 2.2 WC-4: the contract directory is now defined for file-valued outputs (sibling of the file). Section 3 intro: the new per-command contract path list gives `--output-dir` for cleanup-audit and index-repo (P1) and research (P2). Section 3.2 research row: "fresh file \| none" now reads "add `--output-dir` (M2)". | 112 / 256 (WC-4 wording; research row) |
| M4 | applied | Section 7.2 step 6: pass condition now also allows product files the brief authorizes, and names the six commands (cleanup, improve, task, document inline, implement, cli-portify) whose happy path edits product files. | 129 / 329 |
| M6 | applied | Section 7.3 AC-0.4: P0 briefs omit `--unattended`; steps 1, 2, 5, 6, 7 pass as written; step 5 adds a no-Agent-tool check; step 3 uses each command's existing report file; step 4 becomes `test -s` on the existing report, with the YAML key check only for workflow's existing contract (`INV-B:272` checked: `status`, `plan_path`, `reflect_report_path`, no `command` key). | 182 / 677 |
| M8 | applied | Section 3.1 intro (the "only command changes" sentence) now says every 3.1 command gains the flag and section, and that brainstorm and init-lite change only by the flag and section. Section 6 P1 row: brainstorm and init-lite added to the Commands column. | 101 / 384 |
| M9 | applied | Section 3 intro: new "Contract path per command" paragraph lists one path per command (adversarial, brainstorm, reflect, release-split, auggie-review, cleanup-audit, index-repo, research, tdd, init-lite, spec-panel, workflow, troubleshoot, load). Section 3.2 spec-panel row: "add `--output`" now reads "add `--report-dir` (M9)". Spec-panel's `--report-dir` evidence is outside this workspace and is marked UNVERIFIED in the paragraph. | 61 / 1129 (includes the M2-shared paragraph text, counted here as the M9 insert) |
| M10 | applied | Section 7.3 AC-2.2: the gate-trigger check is split by WC-2 resolution. Blocked gates (WC-2 (c)) expect `failed` and a non-empty `blocked_question`; default or flag gates (WC-2 (a) or (b): cleanup, improve, reflect, research, tasklist, auggie-review) expect `succeeded` with no `blocked_question`. Both keep "step 2 never shows agentWait". | 339 / 852 |
| M11 | applied | Section 7.3 AC-2.3: cli-portify is excluded from the happy-path check; its run expects `--outcome failed` at the first approval gate (section 3.2 row), with the artifact named in the contract. The spec defines no cli-portify happy path. | 111 / 398 |
| M12 | applied | Section 1.4 gap 1: the PR #329 nested-route statement now cites the `skill-direct` contract from E3 as partial direct-route evidence for `/sc:adversarial` only, says what it does not show, and marks its content UNVERIFIED (outside this workspace). E3 is unchanged. | 71 / 371 |

## Notes for the coordinator

- The M2 and M9 contract-path rules are one paragraph in section 3. The bytes for that paragraph are counted under M9 in the table above; M2's own text is in the WC-4 edit and the research row.
- Two citations depend on files outside this workspace and are marked UNVERIFIED in the spec: the spec-panel `--report-dir` evidence (M9) and the `skill-direct` return contract (M12).
- Rejected or minor findings (M1, M3, M5, M7 and the follow-up candidates) were not touched.
- Each added sentence carries its finding id in parentheses.
- This revision returns the candidate once. It does not award a PASS; the next review is review 2 of 3, which must run the VERIFY step first.
