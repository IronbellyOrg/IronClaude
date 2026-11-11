# Task: score ONE revised spec against a validated defect ledger

Directory: P17=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p17

Files (read only these; do not look anywhere else, do not search for other runs or other revisions, do not try to find out where the revised spec came from):
- Original spec: `$P17/in/spec-original.md`
- Revised spec to score: `$P17/score/in/__SID__.md`
- Unified diff original → revised: `$P17/score/in/__SID__.diff`
- Ledger: `$P17/score/ledger-blind.json` (44 defects D01–D44 in the ORIGINAL spec; 7 introduced-defect patterns I01–I07; 5 candidate defects N01–N05)

The revised spec is the result of an automated review-and-revise process applied to the original. Your job is to decide, for every ledger defect, what the revised spec does with it.

## Procedure
1. Read the original spec, the diff and the revised spec fully (line numbers in the ledger refer to the ORIGINAL; use the diff to map them).
2. For each defect D01–D44, apply its `is_fixed_when` test literally to the REVISED spec, reading the revised text in every place the defect touches (the diff shows where the text changed; also re-read the rows and acceptance criteria the defect names, because a fix in one place can be contradicted in another). Choose exactly one status:
   - `FIXED`: the revised spec meets `is_fixed_when`, with no remaining contradiction elsewhere.
   - `DELETED_OK`: the obligation or check that caused the defect was removed or narrowed AND every place that referred to it was updated consistently AND the ledger entry has `deletion_ok: true`.
   - `PARTIAL`: the revision addresses part of the defect (some commands, some places, or some of the conditions) but `is_fixed_when` is not fully met.
   - `PRESENT`: the revised text still has the defect (unchanged or changed without resolving it). Includes the case where the obligation was removed but `deletion_ok` is false (say so in the evidence).
   - `WORSE`: the revision made this defect more severe or created a new instance of it.
   - `MOOT_BAD`: the obligation was removed in one place but still required in another, so the spec now contradicts itself.
   Give `evidence`: 1–2 sentences naming the revised text with its line number in the revised file and a short verbatim quote (copy from the file; verify with `grep -nF`). If the status is `PRESENT`, quote the text that still has the defect. Do not give a status without evidence. Do not use the ledger's severity to bias the status.
3. For each introduced-defect pattern I01–I07: `PRESENT` or `ABSENT` in the revised spec, with the verbatim quote and revised line number when present.
4. For each candidate N01–N05: `PRESENT` / `FIXED` / `ABSENT_NOT_APPLICABLE` (the revised spec no longer has the clause the candidate is about), with a quote when you say PRESENT.
5. List `other_new_defects`: genuinely new blocking-level flaws you notice in the CHANGED text (the diff) that are not covered by D, I or N. Blocking-level = the spec as written cannot be implemented or cannot pass its own acceptance checks, or it permits an unsafe outcome. Maximum 5, each with a verbatim quote, the revised line number and one sentence on what goes wrong. If none, an empty list. Do not pad this list; do not re-report ledger defects here.
6. If a ledger defect's `is_fixed_when` is ambiguous for this revision, pick the status you can defend and add `"ambiguous": true` with a one-line note on that entry.
7. When an entry depends on a shell behaviour (a grep, a `test -s`, a YAML parse), run the command in a scratch directory under `$P17/score/scratch/__SID__/` to check rather than reasoning from memory.

## Output
Write valid JSON to `__OUT__` with this shape:
{"sid": "__SID__",
 "defects": [{"id": "D01", "status": "...", "evidence": "...", "ambiguous": false}, ... all 44 ...],
 "introduced": [{"id": "I01", "status": "PRESENT|ABSENT", "evidence": "..."}, ... all 7 ...],
 "candidates": [{"id": "N01", "status": "...", "evidence": "..."}, ... all 5 ...],
 "other_new_defects": [{"quote": "...", "revised_line": 0, "what_goes_wrong": "..."}]}
Validate it parses and has all 44 + 7 + 5 ids. Final reply: `DONE <path>` and one line with counts of statuses. Nothing else.
