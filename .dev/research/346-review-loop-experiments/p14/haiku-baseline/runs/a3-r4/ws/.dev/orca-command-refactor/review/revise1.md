# /sc:spec-panel revise, round 1

- Candidate revised: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (edited in place)
- Source review: `.dev/orca-command-refactor/review/round1.md` (`review: 1 of 3`, verdict FAIL, Reviser brief names `Blocking ids for revision: B1`)
- IDS: B1 only. Medium (M1 to M12) and minor (N1 to N6) findings were not in the brief and were left alone.
- Revise prompt: `~/.claude/rules/prompts/document_review_loop_prompts.md`, REVISE section.

## Byte accounting

Whole file, measured with `wc -c`:

| State | Bytes |
|---|---|
| Before | 57763 |
| After | 57870 |
| Net | +107 |

Per finding id:

| Finding id | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| B1 | 198 | 91 | +107 |

The deleted text is the 91-byte phrase "the exact command line including `--unattended` and every flag section 3 lists as required;" from the old line 73. The 198-byte phrase that replaces it is the only addition. Nothing else in the file changed.

## Finding rows

| Finding | Disposition | Where applied | Reason and citation |
|---|---|---|---|
| B1 | Applied | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:73` (section 2.3) | Round 1 B1 says section 2.3 requires `--unattended` in every Task brief (`:73`), while P0 makes "no command edits" (`:158`) and adds the flag only in P1 (`:159`). Section 2.3 now states that the command line carries `--unattended` from Phase 1 on, and that Phase 0 briefs omit it because no command accepts the flag before P1. This matches the ready-today table (`:79`, `:81-92`), which lists no `--unattended` in its brief column. AC-0.4 (`:194`) and the live check (`:180`) build their briefs "per section 2.3", so they now agree with P0. |

## Notes

- The revision edits one sentence. It adds no rule, mechanism, or section, and it changes no other requirement.
- The residual point in B1 that a P0 smoke run does not exercise the unattended contract is not changed here. The revision makes the two rules agree, which is the fix the review's recommendation allowed. Phase 0 still tests the direct-route worker run, as stated at `:158` and `:194`.
- Line 73 is the only changed line. The shared file path used for evidence is repo-relative, and it was read from the workspace copy.
- Evidence check: the citations `:158`, `:159`, `:73`, `:79`, `:81-92`, `:180`, and `:194` were read in the workspace spec. The inventories under `.dev/orca-command-refactor/inventory/` were not needed for this single-sentence fix and were not cited.
- Verdict: not awarded. The revise prompt says not to award a PASS.
