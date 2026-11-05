# Conflict Intent (C-initial, Tier 2 only) — resolving text conflicts by stated intent

> **Tier 2 only. Off by default.** This ref applies only when the run was started with `--conflict-max-tier 2`, at `--monitor 3` (L3), inside the Tier 2 merge cycle at `C-initial`. With a cap below 2 (the default is `--conflict-max-tier 0`) or below L3 it is never loaded and no text conflict is ever resolved: Tier 2 is reported, not acted on.

`refs/conflict-mechanical.md` owns the merge cycle (steps 0 to 13). This ref is its Tier 2 part: step 5 (resolve the `text:*` paths) and step 6 (the resolution record and its grounding check), plus the Tier 2 commit message and what follows the merge push. The core decides (`superclaude.pr_submit.conflicts`); this ref guides the judgment.

## 1. Scope

- Tier 2 only, L3 only, `--conflict-max-tier 2` only. Any other tier or ordinal never reaches this ref.
- The attended main session does the judgment (J-39, R-173): no new agent resolves a file and no second model client is used. The only agent spawned is the read-only `evidence-validator` of section 7.
- "Ours" is this PR (stage 2, the PR head). "Theirs" is the recorded base tip `base_sha` (stage 3). Stage 1 is the merge base (S-09).
- Escalation is monotone: any stop condition below aborts the merge (the ownership-checked abort of `refs/conflict-mechanical.md` section 9) and halts `sync_tier3` with the Tier 3 template. Nothing is retried in the same run.

## 2. Evidence, one file at a time (J-40)

Take the `text:*` paths in plan order (`plan.text_paths`). Finish one path (evidence, checklist, edit, stage) before you open the next. For path number `<n>` (1-based), with `<merge_base>` taken from the step 2 probe JSON and `<cycle_dir>` the attempt directory of `refs/conflict-mechanical.md` step 3 (`<output-dir>/sync/<cycle_id>/a<attempt>/`, new for every restart of the cycle):

```bash
scripts/collect-conflict-evidence.sh --path <p> --out <cycle_dir><n>/ --base-sha <base_sha> --merge-base <merge_base>
```

- Success prints one JSON line `{"dir": "<out>", "files": [...], "missing": [...], "truncated": <bool>}`. The files are `stage1`, `stage2`, `stage3` (each stage the index lists for the path; an absent stage is named in `missing`, for example `stage1` for an add-add), `worktree` (the file with its zdiff3 conflict markers), `log.txt` (the left-right log of the merge) and `diff-ours.txt`, `diff-theirs.txt` (each side's diff from the merge base). A file cut at the byte limit ends with `[sc:pr-submit: truncated at <N> bytes]`.
- Read the three stage files as three sides. Compare each side with the base (stage 1) to tell which side changed a line and which merely carries it (S-12, S-13, S-14, S-17). Then read `log.txt` and both merge-base diffs (R-112).
- To find callers of a symbol a side changed, a read-only search is allowed (R-181):

```bash
git grep -n -F -- <symbol>
```

- `EVIDENCE_FAIL` of any kind (`usage`, `foreign_merge`, `out_not_empty`, `unreadable`, `timeout`), or a file you cannot read, escalates the cycle to Tier 3: abort, `sync_tier3` (R-84). When `truncated` is true and the part you need was cut, you cannot state the intents from the evidence: section 5 applies (Tier 3).

## 3. High-suspicion checklist (R-180, R-251, S-26)

Before editing a file, answer each high-suspicion question from the evidence:

- Does either side change a function signature, a type or schema, a dependency, a constant or environment variable, or a public API while the other side adds or changes callers of it?
- Does one side remove an old API, field or column while consumers of it remain (on either side, or found by the search above)?

Any yes: the file's kind is `semantic`. A `semantic` file is never resolved here; the cycle escalates to Tier 3 (abort, `sync_tier3`).

## 4. Kind and rule per kind

Give the file exactly one kind, name its structural root cause in one phrase (R-146), and apply that kind's rule:

| Kind | Rule |
|---|---|
| `trivial` | Adjacent edits split artificially: combine both (R-150). One side changed one part of a line and the other another part: combine both changes into the line (S-18). |
| `additive` | Keep both, in a stated order (R-151); the order goes into the resolution as `keep_both(<order>)`. |
| `competing` | Pick or synthesize by intent, subject to section 5 (R-152). |
| `structural` | A move or rename against an edit: apply the edit at the moved or renamed location (R-153). |
| `modify-delete` | Decide which intent supersedes. The deletion wins only when the edit is shown obsolete; otherwise restore the file and keep the edit (R-154, S-39). |
| `add-add` | Merge the two files' contents; never keep one and drop the other silently (S-40). |

## 5. Intent rules

- Edit a file only when each side's intent can be stated in one sentence. If either cannot, stop: Tier 3 (R-18, R-05).
- Never invent a behaviour that neither side wrote (S-26).
- Before staging, write one sentence describing the behaviour after the merge. If you cannot, you do not understand the resolution yet: stop, Tier 3 (R-156).
- When a side's behaviour is dropped, say which behaviour and why in `dropped` (S-29); never drop one silently.
- Remove every conflict marker. Then stage the finished file at once (J-56), naming only that path:

```bash
git add -- <path>
git rm -- <path>
```

Use `git rm -- <path>` only when the resolution is a deletion. Never stage everything, never take one side for the whole tree, never stash, never skip hooks, never amend.

## 6. The resolution record

Write `<cycle_dir>resolution.md` after the last `text:*` path is staged. It holds one section per `text:*` path and nothing else: no title, no prose, no bullets, no other heading. Blank lines are allowed. Each section is these lines, in this order, each field on one line as `<field>: <value>`:

1. `## <path>`: the path exactly as it appears in `plan.text_paths`. Every `text:*` path appears exactly once; no other path (a `regen:*` path has no entry).
2. `kind:` one of `trivial`, `additive`, `competing`, `structural`, `modify-delete`, `add-add` (`semantic` never appears: it is Tier 3).
3. `root_cause:` the structural root cause in one phrase.
4. `ours_intent:` this PR's intent, in exactly one sentence.
5. `theirs_intent:` the base side's intent, in exactly one sentence.
6. `resolution:` one of `keep_both(<order>)`, `take_ours`, `take_theirs`, `synthesized`.
7. `behavior_after:` the behaviour after the merge, in exactly one sentence.
8. `dropped:` `none`, or the dropped behaviour and why.
9. `evidence:` the stage files and commits consulted.

"Exactly one sentence" means one line that ends in `.`, `!` or `?`, with no other `.`, `!` or `?` followed by a space (write "for example", not an abbreviation with a full stop). Every value is non-empty. Example section (each line without the leading `> `):

> ## app/config.py
> kind: additive
> root_cause: both sides appended a setting to the end of the same settings block
> ours_intent: This PR adds a retry limit setting for the HTTP client.
> theirs_intent: The base adds a request timeout setting for the HTTP client.
> resolution: keep_both(ours then theirs)
> behavior_after: The settings block defines both the retry limit and the request timeout.
> dropped: none
> evidence: stage1, stage2, stage3, diff-ours.txt, diff-theirs.txt, log.txt, commits 1a2b3c4 and 5d6e7f8

The core checks it: `resolution_record_ok(parse_resolution_record(text), plan.text_paths)` must return `[]`. A parse error or any listed problem means no commit: abort, `sync_tier3`. Every attempt's record and evidence directories stay in the output dir after an abort.

## 7. Grounding check

Spawn `evidence-validator` (read-only: Read, Grep, Glob) once for the whole record, not once per file. Pass `resolution.md` as the draft (`report_draft_path`), `<cycle_dir>` (this attempt only) as `output_dir`, and `allow_command_reexec: false`. Ask it to check, for each section, that both intents and `behavior_after` are grounded in that path's stage files and merge-base diffs, and to list each unsupported section.

- Every section supported: continue to VAL (`refs/conflict-mechanical.md` section 6).
- One revision pass: re-read the evidence for each flagged section, correct the file and the record where needed (re-stage the path, re-run `resolution_record_ok`), then ask the same validator (no new spawn) to re-check only the revised sections.
- Still unsupported after the one revision pass, or the validator cannot run: abort, Tier 3 (`sync_tier3`).

The grounding check is mandatory for Tier 2 in this release (OQ-12).

## 8. Commit message

Step 9 writes the message file from `merge_commit_message(base_ref=..., head_branch=HEAD_BRANCH, tier=2, record=<the parsed record>)`: the subject `Merge <base_ref> into <head_branch> (sc:pr-submit sync, tier 2)`, then one line per path, `<path>: kind <kind>, resolution <resolution>, dropped <dropped>`. Append the session's attribution lines (OQ-13). The message carries intents and labels, never file content, so keep `dropped` to a short phrase.

## 9. After the merge push

- S6 and RESOLVING run with zero threads (there are no findings yet).
- S5a re-triggers because the push kind is `merge`: `should_retrigger(0, "merge")` is true.
- At `C-initial` no reviewer has been observed yet, so the re-trigger targets the configured reviewers: each reviewer `r` with a non-blank identity in the detection contract (`reviewer_identities(contract, r)` non-empty). Post only to `pending_retriggers(<events>, cycle_id, <configured reviewers>)`, through the S5a procedure of `refs/review-retrigger.md`.
- Each POST's watermark starts that reviewer's S5 attribution, so a review of the pre-merge head is never attributed (INV-030).
- The S5 wait is the run's first review wait; its attributed outcome ticks `round_counter` once.

## 10. Findings after a merge (INV-031)

Once, right after the merge push, read the paths the PR's own diff touches:

```bash
git diff --name-only origin/<base>...HEAD
```

For the rest of the run, a review finding on a path not in that list is `REPORT_ONLY` with reason `base_authored` at Wave 3: it came from the base side of the merge, it is reported, never fixed, and it consumes no round.
