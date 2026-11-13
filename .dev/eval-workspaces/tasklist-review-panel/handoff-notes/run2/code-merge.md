# Code notes: review findings/merge/ledger (run 2)

Source root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/src/superclaude/cli/review/
All line numbers verified by Read on 2026-11-13 (findings.py 457 lines, merge_cmd.py 118, ledger.py 494, ledger_cmd.py 137).
Abbreviations: F = findings.py, M = merge_cmd.py, L = ledger.py, LC = ledger_cmd.py.
Independence: no file under /tmp/handoff-notes/ and no HANDOFF-review-panel-unification*.md was opened.

## 1. Reviewer finding format the parser accepts (findings-v1)

Constants and regexes:
- F:14 `SEVERITIES = ("CRITICAL", "MAJOR", "MINOR")` (no MEDIUM/LOW; case-sensitive).
- F:15-22 `CATEGORIES = ("contradiction","unpassable-check","data-loss","safety","missing-requirement","other")`.
- F:23 `PRIOR_STATUSES = ("resolved","open","regressed")`; F:24 `ACTIONS = ("applied","rejected")` (fix map).
- F:26 `_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$")` -> id max 16 chars.
- F:27 `_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})\s*([^`\s]*)\s*$")` -> info string is a single token; label compared by exact equality to "findings-v1" (F:73).
- F:28 `_HEADING`; F:29 `_REF_TOKEN = re.compile(r"\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b")`; F:30 `_SECTION_REF = ^\d+(?:\.\d+)*$`.
- F:31 `_HEAD_FINDINGS = re.compile(r"^#{1,6}\s+Findings block\s*$", re.M | re.I)` (any heading level, case-insensitive; first match used, F:45).

Block location (F:38-76): find first "Findings block" heading, then scan every fence from the next line to end of text; collect bodies of fences whose info == "findings-v1". Closing fence = same char, >= length, no info string (F:63-68). `closed=False` if EOF reached (truncation).

parse_block (F:124-196):
- No heading -> ok False, error "heading '## Findings block' is missing" (F:128-133).
- Heading but no findings-v1 fence -> ok False (F:134-142).
- >1 block -> ok False, LAST block used (F:143-150).
- Unclosed block -> ok False but its lines are still parsed (F:151-158).
- Each non-blank line must be a JSON object (F:163-174).
- Line with key "prior" -> prior line; needs non-empty str prior id and status in PRIOR_STATUSES (F:175-187). Other keys on that line ignored.
- Otherwise a finding, checked by _check_finding (F:90-121):
  - id matches _ID, unique within the block (F:91-95)
  - severity in SEVERITIES (F:96-97)
  - blocking is a bool (F:98-99)
  - blocking && MINOR rejected (F:100-101)
  - category in CATEGORIES (F:102-103)
  - anchor: string, 12..200 chars after whitespace flattening (F:104-106 via _check_flat F:79-87)
  - anchor2 optional; if present and not null, 12..200 (F:107-110)
  - refs: list of <= 8 strings, default [] (F:111-117, F:194)
  - claim: string, <= 300 flat chars, no minimum (empty claim accepted) (F:118-120)
- Unknown extra keys accepted silently (no whitelist in _check_finding).
- Confidence: NOT a reviewer field. Computed by the ledger: "overlap" if >= 2 distinct reviewer ids reported the row in any single round, else "single" (L:86-90). A reviewer-supplied "confidence" key is ignored.

Annotation (F:346-360): locate anchor in the doc after whitespace flattening (F:276-304); span = FIRST occurrence (F:352); span2 likewise; section = nearest heading's leading number or slug, "none" if anchor missing (F:307-318, F:358); refs_norm = _REF_TOKEN matches scraped from anchor, anchor2, claim and refs, uppercased, plus refs entries that are pure section numbers, minus anything starting "SHA-" (F:321-337); fp = sha256("v1|section|refs")[:16] (F:340-343).

Prompt contract cross-check (src/superclaude/rules/prompts/document_review_loop_prompts.md:58-61): states severity set, categories, anchor 12-200 chars, refs meaning. It does NOT state the 16-char id limit, the 300-char claim limit, the 8-ref limit, or that blocking MINOR is rejected.

## 2. Every rule that rejects or drops a finding

All per-line rejections drop ONLY that line (`continue`) and set the whole reviewer `ok=False`:

| Rule | Line | Effect |
|---|---|---|
| not JSON | F:163-168 | line dropped, error |
| not object | F:169-174 | dropped |
| bad prior line | F:176-185 | dropped |
| bad/too-long id (>16) | F:92-93 | finding dropped |
| duplicate id | F:94-95 | second finding dropped |
| bad severity (e.g. "MEDIUM", "major") | F:96-97 | dropped |
| blocking not bool (e.g. "true") | F:98-99 | dropped |
| MINOR + blocking | F:100-101 | dropped (not downgraded) |
| bad category | F:102-103 | dropped |
| anchor <12 or >200 flat chars / not str | F:104-106 | dropped |
| anchor2 <12 or >200 | F:107-110 | dropped |
| refs not list / >8 / non-str | F:112-117 | dropped |
| claim >300 or not str | F:118-120 | dropped |

Not rejected but degraded silently:
- Anchor not found in the doc: finding kept, anchor_status "missing", span None, section "none" (F:349-358). No warning anywhere. anchor_status / anchor_ambiguous (F:350-351) are never read by any code (grep of src/ and tests/ finds them only in findings.py and tests).
- Anchor found more than once: first occurrence used (F:352), no warning.

What happens to the reviewer and the verdict (L:127-157):
- block_ok[reviewer] = parsed["ok"] (L:129). Warning records only the error count and the FIRST error message (L:130-134).
- Valid findings of a reviewer with a bad block are still merged (L:135-138).
- Merge is refused only when NO reviewer has ok=True (L:150-157).
- Warnings go only to stdout JSON (M:117-118); render_merged_report does not print them, only "block ok false" per reviewer (L:421-424). The round entry stores block_ok (L:147).
- block_ok has NO effect on clearing or verdict. Docstring L:112 "A reviewer with an invalid block is skipped for clearing" is false: the clearing loop L:254-258 never consults block_ok.

## 3. `superclaude review merge` end to end

Inputs (M:21-70): --ledger (created at round 1), --doc (candidate text), --round N (IntRange min 1, no max although help says "1, 2 or 3", M:40-41), --report REVIEWER_ID=PATH (repeatable), --resolution (optional panel JSON; only reviewers[].reviewer_id and .model are read, M:74-83), --out (merged report), --cap (default 3, used only when round 1 creates the ledger, M:64-70, M:104).

Flow (M:71-118):
1. Resolution -> reviewer->model map; reviewer missing from it gets model None silently (M:94).
2. Split each --report on "=" (M:86-90), read text.
3. Load ledger if file exists; else create only if round==1 (M:101-108).
4. led.merge_round (L:107-298):
   - Round must equal len(rounds)+1 (L:114-118); duplicate reviewer ids refused (L:119-121).
   - Parse and annotate each reviewer's block; collect findings and prior lines.
   - Refuse if all blocks invalid (L:150-157).
   - Cluster ALL findings from ALL reviewers by union-find (F:382-407) using same_defect (F:367-379):
     a) same fp AND non-empty refs_norm -> same; else
     b) if refs_norm sets intersect OR both empty: any span/span2 pair within 3 lines of each other -> same.
     Transitive (A~B, B~C merges A,C). Findings of the same reviewer can merge with each other.
   - Each cluster is matched to the FIRST existing ledger row (pre-round snapshot, creation order) for which any member is same_defect with the row view {fp, span, span2, refs} (L:77-83, L:165-171).
   - No match -> new row L{k}: fp/anchor/span/claim/category from first member, refs = union of members' refs_norm, blocking = any member blocking, severity_max = max (L:181-206).
   - Match -> members appended; blocking = this round's cluster (OR'd if several clusters of this round hit the row) (L:213-218); severity_max = max ever (L:219-222); re-anchor to first member with a span (L:226-231); event refound; resolved_check/resolved -> regressed (L:235-238). fp, refs, claim, category NOT updated.
   - After clustering: any resolved_check row not refound this round -> resolved, event cleared (L:254-258).
   - Prior lines -> history "prior_note" only; unknown prior id -> warning (L:259-272). Reviewers cannot change a status.
   - brief_ids = rows with blocking AND status open/regressed (L:99-104); verdict FAIL if any else PASS (L:273-274); decision PASS / REVISE if N < cap / ESCALATE (L:93-96).
   - Round entry appended: n, doc_sha256, reviewers[{reviewer_id, model, report, report_sha256, block_ok}], verdict, decision, brief_ids (L:276-285).
5. render_merged_report (L:408-494): header "review: N of cap", reviewer list with block ok, full ledger table (all rows ever), "Blocking findings" per brief id with each current-round member's claim+anchor (or the stored row claim for a row open from earlier), "Other findings" = rows with blocking False (any status), then "Escalation" (decision ESCALATE, no brief) or "Reviser brief" + REVISER_RULES; last line "verdict: PASS|FAIL".
6. Write --out (non-atomic, M:113-115), then save ledger atomically (L:52-67, M:116). Print result JSON minus "_members" (M:117-118). Exit code always 0 regardless of verdict (no sys.exit in merge_cmd).

Severity vs blocking: severity is only recorded (severity_max) and gates one rule (MINOR cannot be blocking). The verdict uses only the reviewer-declared `blocking` bool. A MAJOR or CRITICAL non-blocking finding never fails a round. One blocking finding from one reviewer is enough to FAIL (no quorum).

Resolution file: read-only input; nothing is written back. The ledger records model per reviewer per round.

## 4. Ledger state machine

Schema "review-ledger/1" (L:17); top level {schema, doc (path string), cap_reviews, rounds[], rows[]} (L:37-38).
Row: lid, fp, blocking, severity_max, category, confidence, status, anchor, anchor2, span, span2, refs, claim, members[{round, reviewer_id, fid, blocking}], history[{round, event, ...}] (L:184-202).
Stable ids: lid = "L" + (row count + 1) (L:185); rows are never deleted, so ids are stable and monotonic. Reviewer finding ids (fid) are kept only in members.
Statuses (L:19): open, resolved_check, resolved, regressed, deferred.
Transitions:
- (new) -> open: merge, no matching row (L:193).
- open/regressed -> resolved_check: `ledger revise`, fix map says applied AND a diff hunk touches span or span2 (L:330-336).
- open/regressed unchanged with history named_not_touched (L:337-339) or rejected_by_reviser (L:340-342).
- resolved_check -> resolved: next merge, not refound (L:254-258).
- resolved_check/resolved -> regressed: next merge, refound (L:235-238).
- any -> deferred: `ledger defer` (L:350-360); no status precondition.
- deferred refound: stays deferred (only resolved_check/resolved are promoted), blocking updated.
- open/regressed refound: status unchanged.
Revise (L:301-347; LC:36-71): requires a merged round; --old must sha256-match last round's doc (L:308-314); parse fix map (fixmap-v1, or a "| id | applied" table fallback, F:199-223); apply transitions; then map every row's span/span2 through difflib opcodes old->new (L:343-346, F:413-439). Revise is not recorded as a round; history uses last round n.
Defer (L:350-360): status deferred, history with reason, removes lid from last round's brief_ids; if brief empty, sets last round verdict and decision to PASS (rewrites stored history).
Verdict (L:363-372; LC:94-109): returns the LAST round's stored verdict/decision/brief_ids; CLI exit 0 PASS, 10 REVISE, 11 ESCALATE (LC:13).
Capture (L:375-401; LC:112-137): review-capture/1 for round n: occasions = reviewer ids of that round, one defect per row with a member in round n, blocking = any member blocking in that round, captured_by in occasion order.
Persistence: atomic temp file + fsync + os.replace (L:52-67). No locking.

## 5. Defects, silent failures, surprises, limits

D1 (HIGH) Partial-panel failure is invisible to the verdict. One reviewer's report can lack its block, be truncated, or have its blocking finding dropped by a length rule, and the round still merges and can PASS if another reviewer's block is valid (L:150 refuses only when all fail). The dropped finding leaves only a stdout warning with the first error (L:130-134); the merged report shows "block ok false" (L:423) with no reason. With a single reviewer the same failure refuses the merge, so behaviour depends on panel size.
D2 (HIGH) Docstring L:112 says an invalid-block reviewer is "skipped for clearing", but the clearing loop L:254-258 ignores block_ok. A resolved_check row that only the failed reviewer would have refound is cleared to resolved.
D3 (HIGH) Ref mismatch blocks span merging. The span path of same_defect requires refs to intersect or both be empty (F:374). refs_norm scrapes tokens from free-text claim/anchor (F:324-333), so one reviewer writing "AC-0.4" (or incidental tokens like "UTF-8", "ISO-8601", "CVE-2024") in a claim and another writing none produces two rows for the same lines. Inflates rows, lowers "overlap" confidence, and on later rounds a re-reported defect can open a NEW row instead of regressing the old one.
D4 (HIGH) A blocking finding whose anchor is not found in the doc (paraphrased quote) gets span None (F:352) and, with no refs, can never be refound (no fp path, no spans) nor become resolved_check (hunks_touch(None) is False, F:446-447). It stays open and blocking until a human defers it, forcing ESCALATE at the cap. No warning for a missing anchor; anchor_status/anchor_ambiguous (F:350-351) are computed and never used.
D5 (MEDIUM) Over-merging: +/-3 line tolerance (F:377) plus transitive union-find (F:393-398) chains distinct adjacent defects (dense lists, tables, task lines) into one row when refs are empty or shared; same-reviewer findings merge too. The row keeps only the first member's claim/anchor (L:194-199).
D6 (MEDIUM) A cluster matches only the first existing row (L:167-171 `break`). A cluster overlapping two rows refinds one; the other, if resolved_check, is cleared to resolved (L:254-258) although re-reported.
D7 (MEDIUM) `ledger revise` can be run twice for one round: the sha guard checks --old against the round's doc (L:308-314), which still matches, so spans are mapped through the diff a second time and corrupted. Nothing records that a revision was applied.
D8 (MEDIUM) No check that round N+1's --doc equals the --new given to revise: the new text's sha is not stored, so spans mapped for one text are matched against another.
D9 (MEDIUM) Whole finding dropped for limits the reviewer prompt does not state (claim >300 F:118, id >16 F:26, refs >8 F:114, MINOR+blocking F:100). The prompt (document_review_loop_prompts.md:60) states only the anchor 12-200 range. A severity spelled "MEDIUM" (the prompt's own grading word, prompts.md:31) is rejected.
D10 (MEDIUM) Row fp/refs/claim/category are never updated after opening (L:207-238); after revisions move sections, the fp path compares against a stale section.
D11 (LOW) `merge` exit code is always 0 (M:117-118); only `ledger verdict` maps decisions to exit codes (LC:13, LC:109).
D12 (LOW) --round accepts any N >= 1 (M:40) though help says 1-3; rounds past the cap keep merging, each ESCALATE.
D13 (LOW) --cap is silently ignored when the ledger exists (M:101-104).
D14 (LOW) Reviewers in the resolution without a --report are not detected; reviewers absent from the resolution get model None (M:94).
D15 (LOW) Defer has no status precondition and rewrites the stored last-round verdict/decision to PASS (L:358-360); no undefer.
D16 (LOW) Fix-map items for rows not open/regressed are skipped with no output entry (L:328-329). The table fallback (F:199-202, F:219-222) treats any table row whose second cell starts "applied" as applied; fixmap_ok is reported but not enforced (LC:70).
D17 (LOW) "Other findings" lists only non-blocking rows (L:468); a blocking row that is resolved or deferred appears in neither prose section, only in the ledger table.
D18 (LOW) Line-model mismatch: locate counts "\n" (F:295) and _blocks_after counts "\n" for the heading line (F:48), while lines/section_of/opcodes use str.splitlines (F:49, F:309, F:415), which also splits on lone \r, \x0b, \x0c, \x1c-\x1e, \x85,  / . Such characters shift spans/sections or the block-scan start.
D19 (LOW) A fence opener with a two-token info string ("```json findings-v1") does not match _FENCE (F:27); the block is not found ("no fenced block" error).
D20 (LOW) Heading regex accepts any level/case (F:31) but the error names "## Findings block" (F:131). A quoted example findings-v1 block in the report plus the real one triggers "more than one block" and ok False (F:143-150).
D21 (LOW) merge --out and capture --out writes are not atomic; capture does not create parent dirs (LC:134-136). Ledger save has no lock: concurrent merges/revises race, last writer wins.
D22 (LOW) Empty claim "" accepted (F:118, lo=None).
D23 (INFO) _REF_TOKEN is case-sensitive (F:29, no re.I), so lowercase ids like "ac-1" are not recognised although matches are later uppercased (F:333).

## 6. Tasklist-specific versus generic

Nothing in these four files is tasklist-specific: grep for "tasklist" in src/superclaude/cli/review/ returns no hits. All logic is generic to any markdown document under review:
- Anchors are exact quotes in any text (F:276-304); sections come from markdown headings (F:307-318).
- Ref tokens are generic requirement-id shapes (XX-n.n, P0-P9) and numeric section refs (F:29-30). Tasklist ids like "T01.02" would not match _REF_TOKEN (no hyphen); whether the tasklist eval documents use that id form is UNVERIFIED.
- Categories (F:15-22) and REVISER_RULES (L:22-26) speak of documents/requirements generally; "unpassable-check" fits acceptance criteria in any spec or tasklist.
- Cap/round/escalate mirrors the generic document review loop prompt (prompts.md:11-13).
The only coupling is to the findings-v1/fixmap-v1 contract in src/superclaude/rules/prompts/document_review_loop_prompts.md:58-66.
