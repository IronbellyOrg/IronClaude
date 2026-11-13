# Notes: review findings/merge/ledger code
Base: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/src/superclaude/cli/review/ (F=findings.py, M=merge_cmd.py, L=ledger.py, C=ledger_cmd.py). All lines read in this session.

## 1. Accepted finding format (F)
- Heading: `_HEAD_FINDINGS = ^#{1,6}\s+Findings block\s*$` (re.M|re.I) F:31; first match only (`heading.search`, F:45). Fixmap heading F:32 `Fix map`.
- Block: a fenced block with info string exactly `findings-v1` AFTER the heading (F:126). `_FENCE = ^\s{0,3}(`{3,}|~{3,})\s*([^`\s]*)\s*$` F:27. Scan does not stop at the next heading: every fence after the heading to EOF is inspected (F:52-75), only info==findings-v1 collected.
- Block missing heading / no block -> ok False (F:128-142). >1 block -> ok False but LAST block used (F:143-150). Unclosed (truncated) -> ok False, lines still parsed (F:151-158).
- One JSON object per line (F:160-174); blank lines skipped; non-JSON or non-dict line -> error, ok False, line skipped.
- Finding line (F:90-121): `id` regex `_ID = ^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` (F:26,92), unique within block (F:94); `severity` in CRITICAL|MAJOR|MINOR (F:14,96); `blocking` must be a real bool (F:98); MINOR+blocking rejected (F:100); `category` in contradiction|unpassable-check|data-loss|safety|missing-requirement|other (F:15-22,102); `anchor` string, 12..200 chars after whitespace flattening (F:104); optional `anchor2` (None allowed) 12..200 (F:107-110); `refs` optional list of <=8 strings (F:111-117); `claim` string, <=300 flattened chars, no minimum (F:118). `refs` defaults to [] (F:194). Extra keys are kept untouched.
- LABEL: the code only knows `unpassable-check` (F:17). `unpassable-ac` appears nowhere in src/superclaude (grep). Prompt doc src/superclaude/rules/prompts/document_review_loop_prompts.md:60 also says `unpassable-check`. A reviewer writing `unpassable-ac` is rejected: "category is not one of the allowed values" (F:102-103).
- Prior line (F:175-187): `{"prior": "<lid>", "status": resolved|open|regressed}`; else error.
- Confidence: no per-finding confidence field in the reviewer format. Ledger "confidence" is derived: `overlap` if >=2 distinct reviewers hit the row in one round, else `single` (L:86-90).
- Anchors: matched against the doc by whitespace-flattened exact substring (`locate` F:276-304). Not found -> `anchor_status "missing"`, span None, section "none" (F:350-358); NOT rejected, NOT warned, finding stays (see defects).
- refs_norm (F:321-337): tokens `_REF_TOKEN = \b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b` (F:29) from anchor, anchor2, claim, refs; uppercased; plus pure numeric refs `_SECTION_REF` (F:30); `SHA-*` dropped.

## 2. Drop rules (answer to "silent drop")
- Not silent in code, but easy to miss. Anchor >200 (F:104), anchor2 >200 (F:108), claim >300 (F:118) (also anchor/anchor2 <12) make `_check_finding` return an error string; parse_block (F:188-192) appends `{line,msg}` to errors, sets ok False, `continue`s: the finding is NOT added, nothing else in the block is affected, seen-id set not updated (F:193).
- Block ok False for the whole reviewer if ANY line errors (F:190). Other valid findings from that block ARE kept (L:135-138 iterates parsed["findings"] regardless of ok; docstring L:111-113).
- Surfacing: merge_round adds ONE warning per reviewer with count of errors and ONLY the first error message (L:130-134). Warnings are returned in the printed JSON (M:117-118, key `warnings`, `block_ok`), and merged report shows `block ok false` (L:423) but never the dropped finding ids/reasons. Ledger stores only `block_ok` per reviewer (L:147), not errors/dropped count. No counter of dropped findings anywhere.
- Hard failure only if NO reviewer has ok True (L:150-157): LedgerError, ledger unchanged, nothing written (M:111-112 turns it into a ClickException; `--out` not written since merged built before write).
- `block ok` semantics: true iff heading found, exactly one findings-v1 block, closed, every non-blank line valid JSON and valid finding/prior. An empty closed block is ok True (zero findings).
- Consequence: a reviewer whose only blocking finding is dropped for length gets block_ok False yet, if another reviewer is ok, the merge proceeds and the verdict can be PASS (L:273-274) with just a warning.

## 3. `superclaude review merge` end to end (M, L)
- Options (M:21-70): --ledger (required; created if round 1), --doc (exists), --round (int>=1), --report ID=PATH repeatable (required), --resolution (optional JSON), --out (required), --cap (default 3; used only when round 1 creates ledger, M:104 - ignored on existing ledger).
- resolution: only read; builds {reviewer_id: model} from `["reviewers"][i]["reviewer_id","model"]` (M:76-79). Reviewer not in it -> model None silently (M:94). The command does NOT write resolution.json (written elsewhere, panel_cmd, not read by me: UNVERIFIED). Ledger records only reviewer_id, model, report path, report_sha256, block_ok per reviewer per round (L:141-149).
- Reviewer id: split on first `=` (M:86); no format validation; duplicates in one round -> LedgerError (L:120-121).
- Flow: read texts (newline="" so CRLF preserved) -> load or create ledger (M:101-108; round>1 w/o ledger errors) -> merge_round -> render_merged_report -> write --out -> save ledger (M:113-116). Output written before ledger saved; a crash between leaves merged report w/o ledger update.
- merge_round (L:107-298): round must equal len(rounds)+1 (L:114). Parse each report; annotate each finding vs current doc (spans, section, fp). `cluster()` (F:382-407) = union-find with `same_defect` (F:367-379): same fp AND non-empty refs_norm -> same; else refs intersect (or both empty) AND spans (span/span2) within 3 lines overlap -> same. Transitive. Cluster order = first member.
  - Each cluster matched against existing ledger rows via `same_defect(member, row view)` (L:166-171, view L:77-83: fp, span, span2, refs); first matching row wins.
  - New row: lid `L{len(rows)+1}` (L:185), fp, blocking=any member blocking (L:187), severity_max = max over members (L:188), category/anchor/claim from FIRST member (L:190-199), confidence derived, status open, members list [{round,reviewer_id,fid,blocking}], history opened.
  - Existing row: members extended; blocking = current round's any-blocking (combined across clusters hitting same row, L:213-218) - a reviewer downgrading to non-blocking un-blocks the row; severity_max only grows; row re-anchored to first member with a span (L:226-231); history refound; if status resolved_check/resolved -> regressed (L:235-238).
  - Severity/blocking decision: purely reviewer's `blocking` flag (any reviewer blocking => row blocking). Severity does not affect verdict. No quorum / no adjudication.
  - Rows in resolved_check not touched by any member this round -> resolved/"cleared" (L:254-258).
  - prior lines: only appended as history `prior_note`; never change status; unknown id -> warning (L:259-272).
  - brief_ids = rows blocking AND status in (open, regressed) (L:99-104). verdict = FAIL if any else PASS (L:274). decision: PASS; else REVISE if n < cap_reviews else ESCALATE (L:93-96). Round appended with doc sha256, reviewers, verdict, decision, brief_ids (L:276-285).
  - Output JSON: verdict, decision, brief_ids, new, refound, regressed, cleared, clusters, block_ok, warnings (M:117-118; `_members` stripped).
- Merged report (L:408-494): header `review: n of cap`, reviewers w/ `block ok`, ledger table, `## Blocking findings` (per member claim+JSON-quoted anchors, or the stored claim if open from earlier round), `## Other findings` (all non-blocking rows incl. resolved/deferred), then `## Escalation` (no reviser brief) if ESCALATE else `## Reviser brief` + REVISER_RULES (L:22-27); ends `verdict: X`.

## 4. Ledger state machine (L, C)
- Schema `review-ledger/1` {schema, doc, cap_reviews, rounds[], rows[]} (L:17,37-38). Persisted as indented JSON, atomic temp+fsync+os.replace (L:52-67); no locking.
- Statuses open, resolved_check, resolved, regressed, deferred (L:19).
- Transitions: open --(revise applied AND a diff hunk touches span/span2)--> resolved_check (L:330-337). resolved_check --(next merge, row not re-reported)--> resolved (L:254-257); --(re-reported)--> regressed (L:235-237). resolved --(re-reported)--> regressed. regressed treated like open for brief and revise (L:328). Any --defer (human) --> deferred (L:350-360). `named_not_touched`, `rejected_by_reviser` are history events only (status stays).
- Rounds: sequential n=1,2,3...; no enforcement n<=cap: round 4 is accepted and gets ESCALATE (n>=cap) (L:93-96,114). "Verify-only" rounds 2-3 are NOT a code mode: there is no flag; any report in any round can open new rows (L:181-206). Verify-only behaviour must come from the reviewer prompt (UNVERIFIED, not checked).
- Stable ids: `L<N>` = row count+1, rows never deleted so stable. Finding ids F* are per-report only (kept in members as fid).
- apply_revision (L:301-347; C:36-71 `ledger revise --old --new --fixmap`): requires old text sha256 == last round's doc_sha256 (L:308-314); difflib opcodes (F:413-416); span mapping for all rows afterwards (L:343-346). Fixmap: `fixmap-v1` JSON lines {id, action applied|rejected, reason}; fallback table regex only yields `applied` rows when block missing (F:199-223).
- defer (L:350-360): sets deferred, removes from last round's brief_ids; if brief empty, stored verdict/decision forced PASS. verdict (L:363-372; C:94-109) exits 0/10/11 for PASS/REVISE/ESCALATE (C:13). capture (L:375-401) builds review-capture/1 matrix per round.

## 5. Defects / surprises (severity guess)
1. HIGH L:254-257: a resolved_check row is marked `resolved` whenever no cluster matched it this round, regardless of whether the reviewer's block was valid (block_ok False, findings dropped for >200/>300 chars or bad category) or whether the reviewer looked at it. A dropped re-report (e.g. anchor now >200, `unpassable-ac` label) therefore silently CLEARS a blocking finding. Verdict can then be PASS.
2. HIGH F:104/108/118 + L:130-134,150: dropped findings (length, label, <12-char anchor, 9+ refs, MINOR+blocking) only produce a one-line first-error warning in CLI JSON; merge succeeds if any other reviewer is ok; dropped count/ids not persisted in ledger or merged report. Silent-in-effect.
3. MED F:350-358: finding whose anchor is not found in the doc is kept (status "missing", section "none"); not warned, not counted. Two such findings with same refs share fp (section "none") and merge (F:371). A hallucinated anchor still blocks.
4. MED F:371/F:374: dedup heuristics: same-fp+refs merges distinct defects in one section sharing a ref (e.g. an AC id); both-empty-refs + spans within 3 lines merges neighbours; union-find is transitive (F:393-398). Row keeps first member's category/claim only (L:190-199), later merged reviewers' claims are lost from the Ledger rows (they appear only in per-round blocking sections).
5. MED L:216-218 + L:213: blocking of a refound row is set by the current round only, so a reviewer re-reporting the same defect as non-blocking un-blocks it (documented in comment L:210-212).
6. MED L:93-96,114: no check n<=cap; --cap ignored on existing ledger (M:68-69,104); doc path stored as given (L:38), may be relative.
7. MED F:143-150 / F:52-75: multiple findings-v1 blocks: last one used, first silently ignored apart from ok False; scan runs to EOF and does not stop at next heading, so a fence in a later section with info `findings-v1` is picked up.
8. MED F:29: `_REF_TOKEN` needs `LETTERS-DIGITS` or `P<digit>`; ids like `T01.01` or `R01.02` (no hyphen) are not extracted. UNVERIFIED which id format tasklists use; if no hyphen, tasklist refs vanish and clustering falls back to span proximity only.
9. LOW L:328: fixmap items for rows not open/regressed are silently skipped (no output key); apply_revision proceeds even when fixmap parse failed (C:64-70 reports only `fixmap_ok`). Rows with span None can never reach resolved_check (L:331-333).
10. LOW M:113-116: --out written before ledger saved; M:94 unknown model -> None silently; reviewer ids not validated.
11. LOW L:355-360 defer forces PASS on last round, without re-evaluating other rows beyond brief_ids (consistent) but no audit of who deferred.
12. LOW F:79-87: anchor length counted after whitespace flattening, so a 200+ raw anchor with heavy whitespace passes; conversely quote with markdown differences fails locate.
13. LOW F:161: line-per-object: pretty-printed multi-line JSON fails every line.

## 6. Tasklist-specific vs generic
- All four files are generic (no mention of tasklist; grep for tasklist/review_ledger in these files: no matches). Generic to any markdown candidate document.
- Spec-oriented assumptions: REVISER_RULES text "Review Loop's Reviser contract" (L:22-27); category names (`unpassable-check`, `missing-requirement`); requirement-id regex (F:29, AC-/FR- style, P1) and numbered-heading section naming (F:307-318, slug fallback). Tasklist specialization, if any, lives in prompts/panel code (not read: UNVERIFIED).
