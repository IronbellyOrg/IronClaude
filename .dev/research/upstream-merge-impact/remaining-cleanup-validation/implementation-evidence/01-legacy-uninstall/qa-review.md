# QA Report: Independent legacy-uninstall retirement review

**Topic:** Retire the optional legacy-uninstall facility
**Date:** 2026-10-23
**Phase:** Single independent per-task/final review
**Fix cycle:** Not applicable; no fixes authorized or made
**Template:** /config/.claude/templates/documents/agent_template_qa.md, Output Format (All Phases)
**Delivery provenance:** The independent reviewer could return findings but was prohibited by their developer instructions from writing a Markdown report. The coordinator transcribed that review here without independently grading it. The reviewer subsequently read the saved transcription and confirmed its PASS/compliant verdict and all six findings without substantive corrections; see review-confirmation.json.

---

## Overall Verdict

**PASS**

**Closed spec verdict:** `compliant`
**extra_scope:** `[]`
**misunderstood:** `[]`

The independent reviewer returned this verdict after checking current files and the snapshot diff, then confirmed the saved transcription. Only confirmation-status wording was updated afterward; the acceptance findings and verdict are unchanged.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| T1.AC1 | Only the three allowed product paths changed; script deleted without replacement | **met** | Independent live diff against the execution snapshot contained exactly two modifications and one deletion. It matched `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/01-legacy-uninstall/product-final.diff:1-51` byte for byte. No outside-owned additions were found. |
| T1.AC2 | No active tracked legacy caller or recommendation remains outside historical artifacts | **met** | Independent tracked search returned **1**, with empty stdout/stderr. The check correctly rejects every other return code at `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/01-legacy-uninstall/check_retirement.py:154-173`. Target/help removals appear in the exact diff at `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/01-legacy-uninstall/product-final.diff:5-22`. |
| T1.AC3 | Unrelated Make definitions, installation/native helpers and pre-existing work preserved | **met** | Independently reconstructed the allowed removals from original snapshot contents, then compared the complete resulting files. All other bytes were retained. Independently rehashed **19,266 non-product baseline paths**, including file modes and gitlink state; no differences or outside-owned additions were found. User staging remained empty and matched its baseline. Current help remains intact at `/config/workspace/IronClaude/.dev/worktrees/ci-followup/Makefile:529-560`. |
| T1.AC4 | Package uninstall and separately installed home-folder assets remain accurately distinguished | **met** | Package uninstall remains at `/config/workspace/IronClaude/.dev/worktrees/ci-followup/docs/getting-started/installation.md:339-345`; surviving home-folder assets and manual review remain at `:353-361`; install/update and backup warnings remain at `:363-365`. Only the retired invocation and facility description were removed. |
| T1.AC5 | Runnable UV check succeeds, outcomes recorded, forbidden operations excluded | **met** | Independently reran the task check through UV: exit **0**. Inspected its complete source before execution; its checking branch performs local reads and Git inspections, not cleanup or installation. Exact comparisons, staging preservation, symlink absence and baseline preservation are enforced at `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/01-legacy-uninstall/check_retirement.py:129-173`. Recorded command/outcome and isolated-index boundary are in `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/01-legacy-uninstall/execution.json:23-29,71-81`. |
| T1.AC6 | Fresh independent review covers every criterion and explicitly limits compatibility claims | **met** | This review independently checked current files, actual snapshot diff, baseline originals/hashes, caller-search outcome, runnable check and recorded evidence. External callers/future runtime are explicitly unverified at `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/01-legacy-uninstall/check_retirement.py:180-181` and `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/research/upstream-merge-impact/remaining-cleanup-validation/implementation-evidence/01-legacy-uninstall/execution.json:78-81`. |

## Summary

- Checks passed: **6 / 6**
- Checks failed: **0**
- Critical issues: **0**
- Important issues: **0**
- Minor issues: **0**
- Issues fixed in-place: **0**
- Product, source plan, baseline and ledger changes by reviewer: **none**

## Issues Found

None.

## Actions Taken

- Compared baseline product originals with snapshot blobs and recorded SHA-256 values.
- Compared the actual product diff with the saved final diff.
- Independently reconstructed the permitted Makefile and documentation removals without importing the implementation checker.
- Verified script absence using `lexists`, covering dangling symlinks.
- Independently checked all non-product baseline fingerprints, additions and user staging.
- Reran the task-owned static check successfully through UV.
- Parsed the captured PR comparison: **38 changed files**, no shared product paths and no legacy names in captured patches. The hook-installer change only removes a dead comment reference.
- Executed no legacy script/target, installer, home cleanup, staging, commit, push, rebase or remote operation.

**Recovered verification attempts:** Reading the PR capture directly exceeded the tool limit. The first mechanical parser then rejected it as one JSON document because it contains sequential JSON values. A streaming decoder successfully parsed the complete capture and completed the comparison. These were reviewer-side inspection failures, not product defects; no source or evidence was modified by the reviewer.

## Recommendations

No product changes are needed for this plan.

## Confidence Gate

- **Confidence:** Verified: **6/6** | Unverifiable: **0 acceptance criteria** | Unchecked: **0** | Confidence: **100.0%**
- **Tool engagement:** Read: **18 attempted, 16 substantive** | Grep tool: **0** (Git searches executed through Bash) | Glob: **0** | Bash: **4**
- **Limits:** Ignored paths were inventoried, not content-hashed. External callers and future runtime remain **UNVERIFIED**. No installation or cleanup runtime behavior is certified.

## Self-Audit

I actively looked for scope creep, incomplete deletion, broken caller searches, symlink remnants, accidental Make/help changes, lost documentation warnings, baseline drift, changed staging and overlapping PR work. Exact whole-file reconstruction and independent fingerprint comparison found no hidden edits; the live tracked caller search returned the required no-match status; the reviewed checker fails on search errors rather than masking them. These concrete checks support the zero-finding verdict.

## QA Complete

**Product/spec review: PASS, `compliant`.** The reviewer returned the report without writing it. The coordinator recovered the complete original from the reviewer's saved transcript and transcribed it into this template. The reviewer read and confirmed that saved transcription. Reviewed and final report hashes are recorded in review-confirmation.json.
