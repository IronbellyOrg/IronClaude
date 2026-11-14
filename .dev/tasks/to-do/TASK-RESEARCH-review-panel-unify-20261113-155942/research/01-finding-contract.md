# Research: Finding contract unification

**Investigation type:** Code Tracer + Integration Mapper
**Scope:** `src/superclaude/cli/review/findings.py`, `src/superclaude/cli/review/findings_v2.py`, `src/superclaude/cli/review/card_convert.py`, `src/superclaude/pr_submit/models.py` (`Finding`), `src/superclaude/skills/sc-auggie-review-protocol/refs/{auggie-prompts.md,severity-rubric.md}`, `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/agents/reflect-reviewer.md`, `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`, `src/superclaude/rules/prompts/document_review_loop_prompts.md`, `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py` (row/finding schema only)
**Status:** Complete
**Date:** 2026-11-13

---

Reading order followed: scope `00-handoff-copy.md` §2.4 and §5.2, `02-review-cli-code.md` §2 and §5, `03-reflect-side.md` §3, `05-master-loop-and-consumers.md` §4, then every source file below. Scope-slice claims reused here were re-checked against source; where a slice and the code differ, the code wins and the difference is noted.

Effort tags: [E1] = reflect Tier 2 panel kernel / shadow mode on `ironbelly/shadow-runs` (findings-v2, card_convert, cluster); [E2] = tasklist review-panel study at `4a22d742`; [E3] = #346 review loop on master (findings-v1, ledger, merge, spec-panel Review Loop, sc-review-ledger experiment). Code that E1 imports from E3 is tagged [E3][E1]. Consumers outside all three efforts (pr_submit, Auggie, rf-qa) are tagged [ext].

## 1. `src/superclaude/cli/review/findings.py` — findings-v1 (457 lines) [E3] (also the format E2 drove)

Purpose: parse the reviewer's `findings-v1` block, the reviser's `fixmap-v1` block, locate anchors in a document, fingerprint and cluster findings, map spans between versions (docstring :1-4). Standard library only (:8-12). It imports nothing from the package; v2 and `cluster.py` import from it.

### 1.1 Constants and the container
- `SEVERITIES = ("CRITICAL", "MAJOR", "MINOR")` :14; `CATEGORIES` :15-22 = `contradiction, unpassable-check, data-loss, safety, missing-requirement, other`; `PRIOR_STATUSES` :23 `resolved, open, regressed`; `ACTIONS` :24 `applied, rejected`.
- `_ID` :26 `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` (max 16 chars).
- `_REF_TOKEN` :29 `\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b`. D7: `T01.02` has no hyphen and does not match. Also (new observation) `P[0-9]\b` means `P10` does not match at all (no word boundary between `1` and `0`).
- `_HEAD_FINDINGS` :31 any heading level 1-6, case-insensitive, text exactly `Findings block`.
- `_blocks_after` :38-76 returns every fence with the given info string after the FIRST matching heading; `closed=False` = truncated.

### 1.2 Validator `_check_finding` :90-121 — rejection rules in order (first failure wins; ONE message per line)
| # | Rule | Line |
|---|---|---|
| v1-1 | `id` string matching `_ID` | :91-93 |
| v1-2 | id unique within block | :94-95 |
| v1-3 | `severity` in CRITICAL/MAJOR/MINOR | :96-97 |
| v1-4 | `blocking` real bool | :98-99 |
| v1-5 | MINOR cannot be blocking | :100-101 |
| v1-6 | `category` in the 6 CATEGORIES (message does not name the bad value) | :102-103 |
| v1-7 | `anchor` REQUIRED, string, 12-200 chars after whitespace flattening | :104-106 |
| v1-8 | `anchor2` optional, 12-200 | :107-110 |
| v1-9 | `refs` list of <=8 strings (absent = `[]`) | :111-117 |
| v1-10 | `claim` string <=300 (no minimum) | :118-120 |

Unknown keys are NOT rejected (no allowlist in :90-121) [CODE-VERIFIED]: v1 silently passes through `citations`, `lens`, `path`, `line`, `in_diff`. There is no confidence field.

### 1.3 Parse loop `parse_block` :124-196
- Missing heading / missing block -> `ok=False`, one error, no findings (:128-142). Several blocks -> last used, `ok=False` (:143-150). Unclosed block -> `ok=False` but the lines read are still parsed and returned (:151-158, loop :160).
- Bad JSON / non-object -> error, skip (:163-174). Prior line `{"prior", "status"}` -> `priors`, never `findings` (:175-187).
- :188-192: a `_check_finding` error -> `ok=False`, `{line,msg}` appended, line skipped; remaining valid lines still returned (:193-195). v1 is per-line lossy but block-tolerant.
- Empty closed block -> `ok=True`, zero findings (nothing in :159-196 errors on an empty body) [CODE-VERIFIED].

### 1.4 Fix map, anchors, sections, refs (:199-360)
- `parse_fixmap` :205-266: `{id, action applied|rejected, reason}`; when heading/block is missing it FALLS BACK to scraping `| id | applied` table rows (:199-202, :219-222) — a lenient path the findings block lacks.
- `flat` :272-273; `locate` :276-304 finds every occurrence of a flattened quote in ONE flattened document -> 0-based half-open line ranges.
- `section_of` :307-318: nearest heading at/above the line; numbered -> number, else slug, none -> `top`.
- `refs_norm` :321-337 scans `anchor`, `anchor2`, `claim`, `refs` for `_REF_TOKEN` plus bare section numbers in `refs`; drops `SHA-*`. Imported by `cluster.py:64` [E3][E1].
- `annotate` :346-360: `anchor_status found|missing`, `anchor_ambiguous`, `span`, `span2`, `section` (`none` if missing), `fp` = sha256(`v1|section|refs`)[:16] (:340-343). **D5**: missing anchor -> only `anchor_status="missing"`, `span=None`, `section="none"` (:349-358); no warning, finding stays [CODE-VERIFIED]. A missing anchor gives `fp` over (`none`, refs), so two hallucinated anchors with the same refs share a fingerprint and `same_defect` (:371-372) clusters them.

Key Takeaways
- [E3] findings-v1 has 10 ordered rejection rules; only the first failure per line is reported.
- [E3] Location = one exact quote in one document. No path, line, diff flag or second document.
- [E3] Unknown keys pass silently: forward-compatible as a parser, blind to misspelt optional fields.
- [E3] Truncation and bad lines keep the other lines; an empty block is valid.

## 2. `src/superclaude/cli/review/findings_v2.py` — findings-v2 (304 lines) [E1, importing E3]

Imports `_HEAD_FINDINGS, _ID, CATEGORIES, SEVERITIES, _blocks_after, _check_flat` from v1 (:15-22) [CODE-VERIFIED]: same heading, fence scanner, severity and category tuples; info string `findings-v2` (:24).

### 2.1 New vocabularies
- `V1_FIELDS` :25-34; `ROLES` :35 `plan, spec, source, test, diff, artifact`; `LENSES` :36 `spec, reflect-pre, reflect-post`; `CHANNELS` :37 `defect, grounding-gap, advisory`; `DEVIATION_CLASSES` :38 `authorized, necessary, drift, regression, none`; `COMPLETION_STATES` :40 (`failed`, `timed_out` for callers, comment :39).
- `REFLECT_CATEGORIES` :41-48 (the prompt's ":43-44" is part of it): `ordering->other`, `acceptance->unpassable-check`, `coverage->missing-requirement`, `contradiction->contradiction`, `risk->safety|other`, `deviation->other`.

### 2.2 Validator `check_finding` :84-187 — rejection rules in order
| # | Rule | Line |
|---|---|---|
| v2-0 | `calibrated_confidence` key present -> reject | :96-97 |
| v2-1..6 | id, unique, severity, bool blocking, MINOR not blocking, category (= v1-1..6) | :98-110 |
| v2-7 | `claim` <=300 (checked BEFORE anchor, unlike v1) | :111-113 |
| v2-8 | `refs` <=8 strings | :114-120 |
| v2-9 | no `citations` -> `anchor` required, 12-200 | :122-126 |
| v2-10 | `citations` -> list of 1-8; each object; `role` in ROLES; non-empty repo-relative `path` (no absolute, drive, leading slash or `..`); int `1<=line_start<=line_end`; optional `quote` 12-200 | :127-130; `_check_citation` :59-81 |
| v2-11 | citations AND anchor -> anchor still 12-200 | :131-132 |
| v2-12 | `anchor2` 12-200 | :135-138 |
| v2-13 | line lens == caller's block lens | :140-142 |
| v2-14 | effective lens in LENSES | :143-145 |
| v2-15 | `deviation_class` required when lens `reflect-post` | :147-149 |
| v2-16 | `deviation_class` in 5 values | :150-153 |
| v2-17 | `reflect_category` in 6 keys | :156-158 |
| v2-18 | `category` in the reflect_category's mapped set | :159-160 |
| v2-19 | **blocking label rule**: with `reflect_category`, `blocking == (severity != MINOR)` | :161-162 |
| v2-20 | `reflect_category: deviation` needs `deviation_class` | :163-164 |
| v2-21 | `coverage_rows` list of strings; non-empty needs caller `assigned_rows`; each row inside it | :166-176 |
| v2-22 | `self_confidence` number 0-1, not bool | :178-182 |
| v2-23 | `channel` in CHANNELS | :184-186 |

Still no unknown-key rejection (:84-187) [CODE-VERIFIED]. `channel_of` :190-193 maps absent/unknown channel to `defect`.

Absent rules [CODE-VERIFIED by reading :84-187]: nothing forces `channel: advisory`/`grounding-gap` to be non-blocking; nothing forces `deviation_class: regression` to be blocking or `authorized`/`necessary` to be non-blocking. The only severity-to-blocking coupling is v2-19 and only when `reflect_category` is set.

### 2.3 Parse loop `parse_block` :215-304
- Heading / block / several blocks / unclosed -> errors (:234-261). Bad JSON / non-object -> error, skip (:264-278). **Prior lines rejected** (:279-283).
- :284-290 `check_finding` error -> error, line skipped; valid lines still appended.
- Empty-block rule :291-298: a closed error-free empty block is complete ONLY when `assigned_rows` is non-empty and all assigned rows are in `observed_rows`.
- :299-303: `truncated` if not closed, else `invalid` if ANY error, else `complete`; `ok` only when complete.
- Consumer effect [CODE-VERIFIED]: `cluster.py:221` sets `valid = block.get("state") == "complete"` and `cluster.py:256-257` skips every finding of a non-valid reviewer. So ONE bad line in a native v2 block removes ALL of that reviewer's findings from clustering (they remain in `parse_block`'s `findings` but are unused). This is a stricter loss than v1, where the ledger keeps the other lines (scope 02 §5 D1).

### 2.4 Question 5 — is the docstring claim at :3 true?
- :3 is a LINE-level claim ("A line that findings-v1 accepts and whose keys are all in V1_FIELDS passes check_finding unchanged") and :5 itself carves out prior lines. For a line with only V1 keys under `lens=None`, `spec` or `reflect-pre`, it holds: v2-1..12 are v1-1..10 reordered with the same limits; v2-13..23 fire only on keys v1 lines lack [CODE-VERIFIED].
- FALSE under `lens="reflect-post"`: a pure-v1 line lacks `deviation_class` and fails v2-15 (:147-149). The docstring omits this.
- FALSE at the block level: (a) priors accepted in v1 (findings.py:175-187), rejected in v2 (:279-283); (b) empty block `ok=True` in v1, `invalid` in v2 without full coverage (:291-298); (c) any bad line -> `invalid` in v2 (:301-302), and the consumer then drops the whole reviewer (cluster.py:256-257), while v1 consumers keep valid lines.
- The info string differs, so v2 `parse_block` does not even find a `findings-v1` block (:233).

Key Takeaways
- [E1] findings-v2 alone has a lens namespace, a channel (defect / grounding-gap / advisory), multi-document role-tagged `citations`, `coverage_rows`, and a self-confidence slot while forbidding calibrated confidence in the reviewer line.
- [E3][E1] It inherits every v1 literal limit and adds more (citation quote 12-200, 1-8 citations): D1 is wider in v2.
- [E1] The block-state rule plus `cluster.py:256-257` turns one bad line into the loss of a whole reviewer.
- [E1] The :3 claim holds per line except under reflect-post; it does not hold for blocks.

## 3. `src/superclaude/cli/review/card_convert.py` — legacy reflect cards to findings-v2 (517 lines) [E1]

Purpose: convert recorded reflect reviewer cards (which follow no single schema) into findings-v2 lines with a deterministic, quote-free rule, and report a conversion share (docstring :1-47). Imports `_ID, flat` from v1 (:57) and `DEVIATION_CLASSES, REFLECT_CATEGORIES, _check_citation, check_finding` from v2 (:58-63); uses `yaml` (:55).

### 3.1 The four card shapes (`SHAPES` :65)
| Shape | Recognised when | Code |
|---|---|---|
| `yaml-blocking-minor` | YAML mapping with a list under `findings`, `returned_findings` or `deviations` (first wins, `FINDING_KEYS` :66) and every entry's severity word is `blocking` or `minor` | `_yaml_findings` :232-242; shape choice :374, :392 |
| `yaml-other-severity` | same container, any other severity word, or `priority` P1-P3, or none | :373-374, :392 |
| `markdown-table` | pipe table whose header has an `evidence` cell and a `sev`/`severity` cell | `_md_rows` :253-277 |
| `unlisted` | anything else (non-YAML, YAML without the list, other suffix, unreadable file) | `_unlisted` :322-330; :357-362, :395-405, :491-492 |

Fields read: claim from `claim, finding, title, summary, headline` (`CLAIM_KEYS` :68; markdown: header containing `finding`, `diverged` or `claim` :415-417); refs from `evidence, location, citation, file_line, spec_ref` (`REF_KEYS` :67; markdown: `evidence` and `location` columns :418); category from `category, kind, type, class, classification` (:69); deviation class from `deviation_class, class, classification` (:70); id from `id` or `n` (:381) or markdown `#`/`id` (:411); markdown uses ONE column for both category and class (:407, :413-414).

### 3.2 Severity mapping (`BLOCKING_WORDS` :71-80, `MINOR_WORDS` :81-83, applied :193-198)
- `blocking, blocker, major, high, must-fix, p1` -> MAJOR + blocking; `critical, p0` -> CRITICAL + blocking.
- `minor, medium, low, should-fix, important, nit, info, p2, p3` -> MINOR, not blocking.
- Any other word -> `severity=None, blocking=None` -> `check_finding` rejects (v2-3) -> unconverted.
- Consequences [CODE-VERIFIED]: reflect `HIGH` -> MAJOR blocking; reflect `MEDIUM` ("unjustified drift with real impact", reflect-reviewer.md, see §6) -> MINOR non-blocking; and the word `important` -> MINOR non-blocking, while rf-qa's `IMPORTANT` is a BLOCKING level (§8). If card_convert were reused for rf-qa reports it would invert IMPORTANT. Auggie/PR `Medium` and `Low` both collapse to MINOR.

### 3.3 Role mapping and citations (:111-165)
- `_resolve` :119-132: token `plan` -> role `plan` on the plan path; `source.md` or `spec` -> role `spec` on the spec path (:124-125); any other path-shaped token -> role `source` on that literal path. Roles `test`, `diff`, `artifact` are never produced.
- A token with no plan/spec path, or one `_check_citation` rejects, becomes `{role: "unresolved", ref, reason}` (:107-108, :128-132); a non-blank string with no `path:N` token becomes one unresolved citation (:162-163). `role: "unresolved"` is not in `ROLES`, so these lines are not valid v2; they are kept in `findings` but listed in `problems` (:222-227, :350-353).
- No citation carries a `quote` and no line carries `anchor` (:209-217), so anchor/quote limits never fire here.

### 3.4 Limits: truncate, not reject — but with NO counter (D1 policy input)
- `MAX_REF_TEXT = 200` :85 truncates the stored text of an unresolved ref (:108). `MAX_CLAIM = 300` :86; claim flattened then cut to 297 chars + `...` (:199-201).
- [CODE-CONTRADICTED] The research prompt describes this as "truncate with a counter as card_convert already does for claims". The code keeps no truncation counter: `counts` (:303-311) has `units, converted, unconverted, refs, refs_resolved, refs_unresolved, share` and nothing for truncated claims or refs, and `summarize` (:496-517) adds the same keys. Truncation is silent; only the trailing `...` in the claim text shows it.
- Category: `risk` -> `safety` when the claim matches `_SAFETY` (:96-100, :204-205), else `other`; with a reflect category the first mapped v1 category (:207); else `other`. Because `reflect_category` is set whenever a reflect category word is found (:218-219) and the severity map always gives MAJOR/CRITICAL+blocking or MINOR+non-blocking, v2-19 always holds for converted lines.
- Deviation class: first of the class keys that is EXACTLY one of `authorized, necessary, drift, regression, none` after lowercasing (:103-104, :203). The agent's labels `Authorized expansion` / `Necessary deviation` (reflect-reviewer.md, §6) do not match, so those rows carry no `deviation_class` — and if their category word is `deviation` the line fails v2-20 and is unconverted [CODE-VERIFIED by tracing :202-203 into findings_v2.py:163-164].
- Converted lines carry no `lens` (:209-221), so `check_finding` is called with `lens=None` (:226) and v2-15 never fires; a UC-2 card converted here is not checked as `reflect-post`.
- Ids: `_new_id` :168-176 keeps a valid unique id, else `F<index>` / `F<index>-<k>`; `seen.add` runs even for unconverted lines (:228).
- Empty claim: an entry with no claim key gives `""` (:199, :375-377), which passes v2-7 (no minimum). A finding with an empty claim converts.

### 3.5 Summary outputs
`_result` :284-312 per card; `summarize` :496-517 totals plus `by_shape`. `share = converted/units`, None when units is 0. An unlisted card counts as one unconverted unit (:322-330), a non-mapping entry as one unconverted finding (:368-372).

Key Takeaways
- [E1] card_convert is the only place in either stack that maps a free-form severity vocabulary onto CRITICAL/MAJOR/MINOR; its word table already collides with rf-qa (`important` -> MINOR) and drops reflect MEDIUM to non-blocking.
- [E1] It truncates claims and unresolved ref text silently: no counter exists, contrary to the research prompt's premise.
- [E1] It produces only roles plan/spec/source and never sets `lens`, so converted UC-2 cards escape the reflect-post rule.
- [E1] The two-word deviation labels the reviewer agent is told to write are not recognised.

## 4. `src/superclaude/pr_submit/models.py` — `Finding` (PR code review) [ext]

- `Severity` enum :106-113: `Critical, High, Medium, Low, Nit` (docstring: "the rubric's 5-tier scheme (reused from auggie-review)") [CODE-VERIFIED].
- `@dataclass Finding` :168-207. Fields: `path: str` (required), `line: int | None` (required positional), `body: str` (required), `severity_hint: str|None`, `category: str|None`, `confidence: str|None`, `in_diff: bool = True`, `comment_id`, `remapped_severity: Severity|None` (filled by the router, docstring :173-174), `verification_status: str = "unverified"` (`unverified`/`verified`/`report_only`, docstring :174-175), `needs_human_decision: bool`, `thread_id`, `review_id`, `original_line`, `is_outdated`, `reviewer: str = "augment"` (`augment` or `codex`, :176).
- `fix_key` :196-207 = sha256(`path\nline\nbody`), comment-id independent (INV-009). This is the PR-side fingerprint: it keys on exact body text, unlike v1 `fp` (section+refs) or v2 fp (role+path+section+refs+class).
- No validation exists in the dataclass (no `__post_init__` in :168-207): free-text severity hint, category and confidence; no length limits; no id field (identity = `comment_id`/`thread_id`, or `fix_key`).
- `SkillResult.findings: list[Finding]` :227 is the only aggregate.

Rejections a PR finding would hit in the review CLI [CODE-VERIFIED against §1.2/§2.2]:
| PR field | findings-v1 | findings-v2 |
|---|---|---|
| no `id` (comment id is an int, not a string) | v1-1 rejects (`findings.py:91-93`) | v2-1 (`findings_v2.py:98-100`) |
| severity `Critical/High/Medium/Low/Nit` (title case, 5 levels) | v1-3 rejects every value — even `Critical` (case-sensitive tuple `findings.py:14`, check :96) | v2-3 (:103-104) |
| `category` e.g. `security`, `error-handling` | v1-6 (`findings.py:102-103`) | v2-6 (:109-110) |
| no `blocking` bool (blocking is derived by the router from severity) | v1-4 (:98-99) | v2-4 (:105-106) |
| `path`+`line` but no `anchor` quote | v1-7 `anchor must be a string` (:104) | v2-9 unless the location is rewritten as `citations` (:122-126) |
| `line: None` (file-level comment) | n/a | a citation needs int `line_start>=1` (:76-78) — rejected |
| `body` > 300 chars (typical bot comment) | v1-10 (:118) | v2-7 (:111) |
| `in_diff`, `confidence` (`high/medium/low` strings), `reviewer`, `verification_status` | ignored (no allowlist) | ignored; `self_confidence` must be a number (:178-182), so a string confidence under that name would be rejected |
| role `diff` | n/a | allowed (`ROLES` :35), but `in_diff=False` has no representation |

Key Takeaways
- [ext] The PR `Finding` is a location-first record (path, line, in_diff) with free-text classification and a derived severity; it has no id, no blocking flag and no length limit.
- [ext] Every PR finding fails both review validators at the first or third rule; the closest fit is v2 `citations` with role `diff`/`source`, plus a new severity namespace and a new `in_diff` field.
- [ext] `fix_key` is a third fingerprint scheme a unified contract has to keep or replace.

## 5. `src/superclaude/rules/prompts/document_review_loop_prompts.md` — reviewer/reviser brief for findings-v1 [E3] (driven by E2)

- Placeholders :17-21: `CANDIDATE, BASELINE, PRIOR, N, IDS`; no source/spec-of-the-candidate placeholder (D8) [CODE-VERIFIED by reading the file].
- Grading check :31: blocking only when "two stated texts contradict", "a stated text causes data loss or breaks a security or safety boundary", or "a stated text that an acceptance criterion cannot pass". Grade **Medium** when the sentence needs a guess "or when the finding is a requirement the document never states (a missing restriction, an undefined state, an unspecified edge case)". "A Medium finding goes under follow-up candidates even when its label is MAJOR." So "Medium" = a MAJOR (or any) label with `blocking:false`; it is a fourth grade that exists only in prose, not in `SEVERITIES`.
- **D9 [CODE-VERIFIED both sides]**: the brief makes an unstated requirement Medium (:31), i.e. never blocking, while `missing-requirement` is an allowed category (`findings.py:20`) with no per-category blocking rule (`findings.py:96-103`). A reviewer that writes `{"category":"missing-requirement","severity":"MAJOR","blocking":true}` passes the validator against the brief's intent. In v2 with `reflect_category: coverage` the opposite rule applies: MAJOR coverage MUST be blocking (`findings_v2.py:44`, :161-162). Same category, opposite blocking rule in the two stacks.
- Findings block spec :58-62: names the 6 categories, `anchor` 12-200, optional `anchor2`, `refs`. It does **NOT** state the 300-char `claim` limit (only "one sentence", :60) or the 8-ref limit. Reviewers are not told two of the limits that reject their lines — a direct contributor to D1 [CODE-VERIFIED: no "300" or "8" in :56-62].
- "A report with no finding has an empty block" (:58) — valid in v1, would be `invalid` in v2 (§2.4).
- Prior lines :61 — v1 only.
- Review panel :70: merge "refuses a round in which no reviewer produced a valid findings block" — the single-valid-reviewer pass (D3) is the documented behaviour.
- Category `unpassable-ac` does not appear in this file; the brief says `unpassable-check` (:60). **D10** was an E2 harness brief error (hand-off §2.4 D10, `tools/run-reviewer.sh`), not a product-brief error; the validator rejects it at `findings.py:102-103` (`category is not one of the allowed values`, without naming the value).

Key Takeaways
- [E3][E2] The product brief defines blocking by a consequence sentence, adds a prose-only "Medium" grade, and omits the claim and refs limits that the validator enforces.
- [E3] D9 is real and is a cross-stack conflict: v1 lets missing-requirement block against the brief; v2 reflect forces MAJOR coverage to block.
- [E2] D10 came from a harness brief; a validator message that names the rejected value would have made it obvious.

## 6. `src/superclaude/agents/reflect-reviewer.md` — legacy UC-2 card format [E1]

- Taxonomy :21-26: **Authorized expansion**, **Necessary deviation**, **Drift**, **Regression** (two-word labels for the first two).
- Advisory channel :30, :101-115: "Correctness gaps" table, advisory / non-gating, must not set `regression_present`, never a 5th class.
- Severity scale :71: **HIGH** = regression or load-bearing-invariant break; **MEDIUM** = unjustified drift with real impact; **LOW** = cosmetic / minor drift.
- Returned format :73-99: header fields (persona, grounding root, diff scope, timestamp, total), `## Deviations` table `# | Category | Location | What diverged | Evidence (file:line) | Severity` (:84), `## Adherence summary` counts, `## Notes`. Correctness-gap table :110 `# | Correctness gap | Location | Sibling disagreement | Evidence (file:line)` — it has NO severity column, so `card_convert._md_rows` (needs `sev`/`severity`, card_convert.py:264-266) does not pick it up: advisory rows are silently not converted [CODE-VERIFIED by comparing :110 with card_convert.py:264-266].
- Mapping through card_convert [CODE-VERIFIED]: `Category` column -> both category and class words (card_convert.py:407, :413-414); `Drift` -> `drift`, `Regression` -> `regression` (match `DEVIATION_CLASSES`), but neither is a `REFLECT_CATEGORIES` key, so `reflect_category` is unset and `category` becomes `other`; `Authorized expansion` and `Necessary deviation` match nothing. `Location` and `Evidence` columns -> citations; `bar.py@base:17` (:87) is not matched by `_TOKEN` as a path (the `@base` makes the token `bar.py@base`, which has no extension at the end and no `/`), so it becomes unresolved -> the finding is unconverted.
- There is no `blocking` concept in the card; blocking comes only from the severity word (HIGH -> blocking, MEDIUM/LOW -> not).

Key Takeaways
- [E1] The legacy card has a 4-class taxonomy with two-word labels, a 3-level HIGH/MEDIUM/LOW scale tied to class, and a separate advisory table without severity.
- [E1] card_convert loses: the two-word classes, MEDIUM drift's blocking weight, every advisory correctness gap, and any `file@rev:line` evidence.

## 7. `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md` — shadow findings-v2 brief [E1]

- The only findings-v2 brief text is the appended instruction at :39 (shadow engine only): exact heading `## Findings block`; fields `id`, `severity` CRITICAL/MAJOR/MINOR, `blocking` (MINOR never blocking), the 6 categories, `lens "reflect-pre"`, `claim` "at most 300 characters", `refs`, `citations` "1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote"; then a `reviewer_model_self_report` line [CODE-VERIFIED by reading :39].
- Not stated in the brief but enforced by the validator: citation `quote` 12-200 (`findings_v2.py:79-80`), `refs` <= 8 (:114-120), id pattern/length (:98-100). The example (:39) is `MAJOR` + `blocking:false` with no `reflect_category`, which is valid (v2-19 does not fire) — so the shadow brief never exercises the reflect blocking-label rule.
- Brief does not ask for `reflect_category`, `channel`, `coverage_rows` or `self_confidence`; those v2 fields are unreachable from shadow reviewers as briefed.
- Reflect brief has three sections (`## T1 card excerpt`, `## Grounding hunks`, `## Coverage slice`, :33-74); the source document reaches only the `qa` persona (D13 spec-body hunks :55). So D8's "brief never names the source" is partly answered in reflect (qa persona only) and not at all in the E3 brief.

Key Takeaways
- [E1] The shadow brief teaches a subset of v2 (UC-1, roles plan/spec only) and omits the quote and refs limits.
- [E1] The richer v2 fields (channel, reflect_category, coverage_rows, self_confidence) exist in the validator but no brief asks for them yet.

## 8. Auggie review schema and severity rubric [ext]

### 8.1 `sc-auggie-review-protocol/refs/auggie-prompts.md` — output contract :41-85
- One JSON object `{findings[], cross_cutting_observations[], notes_for_orchestrator}` (:45-74), fenced or not (:43).
- Finding fields (:47-59): `title` (one line), `category` (:49, 18 values: `security, data-integrity, correctness, concurrency, resource-leak, error-handling, api-contract, performance, architecture, layering, coupling, anti-pattern, dead-code, tests, docs, logging, naming, style`), `severity_hint` (`critical|high|medium|low|nit`, lower case, "the orchestrator may remap", :50), `file` (repo-relative), `line` (int at HEAD), `line_range_end` (int or null), `in_diff` (bool), `evidence` (verbatim code excerpt, or null with `confidence: low`, :55), `why` (2-4 sentences), `recommendation` (1-3 sentences), `cross_references` (list of `path:line`), `confidence` (`high|medium|low`).
- `cross_cutting_observations` (:62-71): no line; `affected_files` list instead. Architecture/layering findings go here (:83). So Auggie already has TWO location kinds: line-anchored and multi-file.
- No id, no blocking flag, no length limit; `why` alone is 2-4 sentences, so any 300-char claim limit would reject most bodies.
- `evidence` = an exact quote at the cited line: the same idea as v1 `anchor` and v2 citation `quote`, but bound to a path+line, and allowed to be null.

### 8.2 `severity-rubric.md` and its code (`pr_submit/severity_router.py`)
- Five tiers in decision terms (:11-61): Critical = block merge; High = should fix before merge; Medium = fix if cheap else follow-up; Low = nice-to-have; Nit = never blocks (:61).
- Remap algorithm (:63-101): start from hint; clamp to per-category floor/ceiling (:70-87); low confidence drops a tier (:89-92); `in_diff:false` and pre-existing drops a tier (:93-96); deep single-source drops a tier (:97-99).
- Code [CODE-VERIFIED]: `_CATEGORY_TABLE` severity_router.py:34-52 (adds `security-latent`, a value the Auggie prompt does not list at auggie-prompts.md:49); unknown/absent hint -> Medium (:122-133); `remap_severity` :151-200; `route` :203-214: Critical/High -> `--depth deep --fix`, Medium -> `--fix`, Low/Nit -> report-only.
- [CODE-CONTRADICTED] rubric :95 says `in_diff:false` on "a callsite affected by the diff" -> no change; code :178-189 drops one tier for every `in_diff is False` (no callsite test). Rubric :90 says a Critical with low confidence drops only if grounding also flagged uncertainty; code :174-175 always drops (the re-clamp at :197 restores only categories with a Critical floor, i.e. `security`).
- Blocking is derived, never reviewer-supplied: Critical blocks merge per rubric; the code's operational meaning is the route.

Key Takeaways
- [ext] Code review findings are location-first (file, line, line_range_end, in_diff), with multi-file observations as a second kind, and a reviewer hint that a deterministic remap overrides.
- [ext] Severity is a 5-level ordinal with category floors/ceilings; blocking is a function of the remapped level, not a reviewer field.
- [ext] Two rubric-vs-code mismatches exist in the remap; a unified contract that adopts this remap must pick one.

## 9. rf-qa and rf-qa-qualitative report format [ext]

- Both agents share the "Review severity rule" (rf-qa.md:106-111; same text rf-qa-qualitative.md:111 per grep): grade every finding blocking or minor; blocking = wrong behaviour, false claim, missing deliverable, security or data-loss risk; minor = cosmetic, wording, format, citation format, nit, moved line number on a true claim (:108). "On a CRITICAL / IMPORTANT / MINOR scale, CRITICAL and IMPORTANT findings are blocking and MINOR findings are minor; grade by the definition above, not by the label" (:111). This is the "pragmatic blocking/minor" vocabulary with a label scale on top.
- Report table rf-qa.md:447-450 and rf-qa-qualitative.md:882-885: `# | Severity | Location | Issue | Required Fix`, severity `CRITICAL / IMPORTANT / MINOR`, Location `[file:section]`. No id, no blocking column, no category, no exact quote, no line number.
- rf-qa-qualitative adds an `Items Reviewed` table (:846-848) `# | Check | axis | Result | Evidence` with axis in `{AX-1..AX-5, none}` (AX-1 Drift, AX-2 Contradictions, AX-3 Omissions, AX-4 Weakened criteria, AX-5 Invented content; :595-650), required only in the task-qualitative phase (:852-869). Axis is a checklist dimension on a check row, not on an issue row.
- rf-qa synthetic finding (rf-qa.md:84): DNSP emission `severity: HIGH` (a fourth word on that scale), `source: synthetic-dnsp`, `affected_range`, `evidence`, `recommendation`, `dedup_key` 2-tuple, `found_n_times` — a 7-field record with its own dedup key and counter.
- Verdict: any CRITICAL or IMPORTANT -> FAIL (rf-qa.md:170, :182-183).

Rejections an rf-qa finding would hit [CODE-VERIFIED against §1.2/§2.2]: severity `IMPORTANT` (and `HIGH`) fails v1-3 / v2-3; no `id` fails v1-1; no `blocking` fails v1-4; no `category` fails v1-6; `Location [file:section]` is neither an `anchor` (exact quote) nor a citation (needs integer lines) -> v1-7 / v2-9/10; `Issue` text longer than 300 -> v1-10 / v2-7. Through `card_convert`, `IMPORTANT` would map to MINOR non-blocking (card_convert.py:82), inverting rf-qa's own rule.

Key Takeaways
- [ext] rf-qa decides blocking by definition and uses labels only as a hint; its location is a file + section, not a quote or line.
- [ext] rf-qa-qualitative's axis is a second lens-like namespace (AX-1..5) that fits a pluggable category namespace, not the 6 v1 categories.
- [ext] Replacing rf-qa needs a severity namespace that keeps IMPORTANT blocking and a location kind `file + section`.

## 10. Ledger row shapes [E3]

### 10.1 Master ledger `src/superclaude/cli/review/ledger.py` (row built from findings-v1)
- `merge_round` parses each reviewer with `fnd.parse_block` (:128), records `block_ok` (:129, :147), warns once per bad reviewer with the error COUNT and only the FIRST message (:130-134) [CODE-VERIFIED, D1]. Valid lines of a bad reviewer are still annotated and merged (:135-138) — v1 consumers keep the good lines.
- Raises only when NO reviewer is valid (:150-157) (D3).
- New row :184-202: `lid`, `fp`, `blocking` (= any member blocking, :187), `severity_max`, `category` (first member's, :191), `confidence`, `status`, `anchor`, `anchor2`, `span`, `span2`, `refs`, `claim` (first member's, :199), `members[{round, reviewer_id, fid, blocking}]` (:172-180), `history`. (Scope slice 00 §5.2 lists "anchors, spans" in plural; the code has singular `anchor`/`anchor2`/`span`/`span2` — wording only.)
- The ledger stores no rejected-line ids and no reason list per reviewer: only `block_ok` (:141-149).

### 10.2 Experiment `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py` (installed only in ~/.claude, row/finding schema only)
- Input row keys allowlisted: `ROW_INPUT_KEYS = {grade, rule, wrong_outcome, anchor, finding, label}` (:64); unknown keys are an error (:809-817) — the ONLY contract in scope that rejects unknown keys.
- `grade` in `GRADES_SPEC_PANEL = CRITICAL, MAJOR, MINOR` (:38, :818-825); `anchor` and `finding` non-empty strings (:826-834); `rule`, `wrong_outcome`, `label` string or null (:835-843). **No length limits** on anchor or finding.
- Blocking is COMPUTED, not reviewer-supplied: `_blocking_spec_panel` :41-49 = `grade == CRITICAL or rule in {FR-8, FR-9} or (grade == MAJOR and wrong_outcome non-empty)`; `make_row` :889 also forces non-blocking out of scope or in a sweep round. Per-profile table `PROFILES` :53-59 (one profile, `spec-panel`): grade vocabulary + blocking predicate + cap — a ready-made pattern for pluggable severity namespaces.
- Validation is all-or-nothing: any problem refuses the whole input, "nothing was written" (:844-847).
- Anchors: `check_anchors` :851-881 REFUSES the input when an anchor is not found (`E-ANCHOR`) or found more than once (`E-ANCHOR-AMBIGUOUS`) — the opposite of master's D5 (missing kept silently) and of v1 `annotate` (ambiguous allowed, first span used, findings.py:351-352).
- Row :890-909: `id` `R<N>`, `label`, `round_found`, `grade`, `rule`, `wrong_outcome`, `blocking`, `anchor`, `at` (span), `at_snapshot`, `origin`, `scope`, `caused_by`, `finding`, `status` (`open` if blocking else `deferred`), `mappings`, `claims`, `history`. No category, no refs, no fingerprint, no reviewer identity on the row.

Key Takeaways
- [E3] The master ledger keeps valid lines of a bad reviewer but records only `block_ok` and one first message: D1's "dropped ids not stored" is confirmed at ledger.py:141-149.
- [E3] The experiment ledger has three properties no other contract has: an unknown-key allowlist, computed blocking per profile, and hard refusal of missing or ambiguous anchors — with no length limits at all.
- [E3] Three anchor policies now exist: keep missing silently (master), flag but keep unresolved citations (E1 cluster), refuse the whole input (experiment).

## 11. E2 harness evidence on the contract (read-only via `git show 4a22d742...:<path>`) [E2]

Evidence dated by the study folder `20261111-a1` (runs up to 2026-11-11/12).
- `tools/run-reviewer.sh:17` (E2 brief) repeats the product grading check and lists the findings-v1 fields: "id, severity CRITICAL|MAJOR|MINOR, blocking, category contradiction|unpassable-check|...|other, anchor = 12 to 200 chars copied exactly from the candidate, optional anchor2, refs, claim". Like the product brief (§5), it does not state the 300-char claim limit or the 8-ref limit.
- `tools/run-reviewer.sh:57`: the harness's own `BLOCK_OK` is `grep -q '^```findings-v1'` — fence present, not validator-valid. A third meaning of "block ok" beside v1 `ok` and v2 `state`.
- `COMBO-REPORT.md:292` (model-behaviour evidence, 2026-11-11/12 runs): "anchors over 200 characters (56), anchor2 over 200 (18), claims over 300 (14), bad severity, bad refs are discarded with no error. 80 reviewer-level cases, 49 blocking findings lost". `COMBO-REPORT.md:11`, `:72`: `unpassable-ac` reports needed `.catfix.md` copies (files listed in the tree, e.g. `TASK-WF-design-20261108-041415/reviews/t1b-1.md.catfix.md`).
- `COMBO-REPORT.md:371` recommendation (1): "raise or truncate the 200-character anchor limit at merge, or instruct reviewers and re-validate".
- `tools/run-reviewer.sh:9-11` ships `source.md` next to the candidate; the brief text at :15 still names only the candidate (consistent with D8).

Key Takeaways
- [E2] The study's loss figures come from the v1 limits that neither brief states; the study itself recommended truncation or instruction plus re-validation.
- [E2] The harness measured "block ok" by fence presence, so its per-reviewer validity is not the product's.

## 12. Q1 — Field-by-field superset table

Legend: R = required, O = optional, D = derived by code (not reviewer-written), — = absent. "Cards" = the 4 reflect legacy shapes read by card_convert (keys per card_convert.py:66-70; markdown columns per reflect-reviewer.md:84). "Ledger" = master `ledger.py` row (M) / experiment `review_ledger.py` input+row (X). All cells cite sections above.

| Field (meaning) | findings-v1 [E3] | findings-v2 [E1] | Reflect cards (4 shapes) [E1] | Ledger rows M / X [E3] | pr_submit `Finding` [ext] | Auggie [ext] | rf-qa / rf-qa-qual [ext] |
|---|---|---|---|---|---|---|---|
| Finding id | R `_ID` <=16 chars | R same | O `id`/`n`/`#`; else `F<i>` D | M `lid` D (`L<n>`), member `fid`; X `id` D (`R<n>`) | — (comment_id / thread_id) | — | `#` row number |
| Severity | R CRITICAL/MAJOR/MINOR | R same | O free word (blocking, high, medium, P1...) mapped D | M `severity_max` D; X `grade` R C/M/M | `severity_hint` O str; `remapped_severity` D 5-level | `severity_hint` R critical..nit | R CRITICAL/IMPORTANT/MINOR (+HIGH DNSP) |
| Blocking | R bool; MINOR never | R bool; + v2-19 rule | D from severity word | M D any-member; X D `_blocking_spec_panel` | D via route | — (Critical "blocks merge" in rubric) | D by definition (C/I blocking) |
| Category | R 6 values | R 6 values | `category/kind/type/class/...` -> reflect_category -> v1 D | M first member's; X — | O free str | R 18 values | — (qual: `axis` AX-1..5 on check rows) |
| Lens / review kind | — | O spec/reflect-pre/reflect-post | — (implied UC) | — | — | — (pr / snapshot mode) | `Phase` header |
| Deviation class | — | O 5 values; R under reflect-post | Category column 4 two-word labels / `deviation_class` | — | — | — | — |
| Reflect category | — | O 6 values | D from category words | — | — | — | — |
| Channel | — | O defect/grounding-gap/advisory | separate Correctness-gaps table | — | — | `findings` vs `cross_cutting_observations` | `Items Reviewed` vs `Issues Found` |
| Claim / body | R <=300 | R <=300 | claim/finding/title/summary/headline, truncated 297+... D | M `claim` first member; X `finding` R no limit | `body` R no limit | `title` + `why` + `recommendation` | `Issue` + `Required Fix` |
| Exact quote, single document | `anchor` R 12-200 | `anchor` O 12-200 (R w/o citations) | — | M `anchor`; X `anchor` R, must be unique | — | `evidence` O (null allowed) | — |
| Second quote | `anchor2` O | `anchor2` O | — | M `anchor2` | — | — | — |
| Requirement refs | `refs` O <=8 | `refs` O <=8 | `refs: []` D | M `refs` union; X `rule` O (FR-8/FR-9) | — | — | — |
| Path + line range | — | `citations[]` 1-8 `{role,path,line_start,line_end,quote?}` | evidence/location `path:N` -> citations D | M `span`/`span2` D (0-based, one doc); X `at` D | `path` R, `line` R (nullable), `original_line` | `file`, `line`, `line_range_end`, `cross_references[]`, `affected_files[]` | `Location [file:section]` |
| Citation role | — | plan/spec/source/test/diff/artifact | plan/spec/source D (+`unresolved`) | — | — | — | — |
| In-diff flag | — | — (role `diff` only) | — | — | `in_diff` bool | `in_diff` bool | — |
| Self confidence | — | `self_confidence` 0-1 | — | M `confidence` single/overlap D | `confidence` str | `confidence` high/medium/low | — |
| Calibrated confidence | — | forbidden in line; sidecar map | — | — | — | — | — |
| Coverage rows | — | `coverage_rows` | — (Adherence summary counts) | — | — | — | — |
| Re-review prior status | prior line resolved/open/regressed | rejected | — | M `status` 5 values; X `status`, answers fixed/not-fixed/disputed | `verification_status`, `is_outdated` | — | fix-cycle phase |
| Consequence sentence | — (prompt only) | — | — | X `wrong_outcome` | — | `why` | — |
| Reviewer identity | — (from `--resolution`) | — (card file name) | `persona:`/`model:` header in shadow | M members `reviewer_id` | `reviewer` augment/codex | — | — |
| Fingerprint | D `fp` v1 (section+refs) | D v2 fp in cluster (role+path+refs+class) | — | M `fp` | D `fix_key` (path+line+body) | — | X DNSP `dedup_key` |
| Unknown keys | ignored | ignored | ignored | X rejected | n/a (dataclass) | n/a | n/a |

Key Takeaways
- [E3][E1][ext] Only three fields are common to nearly every shape: a severity word, a free-text claim, and some location. Blocking is reviewer-written in v1/v2 only; everywhere else it is derived.
- [E1] findings-v2 already covers the largest share of the superset (lens, channel, citations with roles, coverage, self-confidence); the missing pieces are `in_diff`, multi-file observations, file+section locations, a consequence sentence, and non-spec severity/category namespaces.

## 13. Q2 — Every validator rule that would reject a code-review or rf-qa finding

| Input property | Rejecting rule (v1) | Rejecting rule (v2) | Other |
|---|---|---|---|
| No string `id` (PR comment id is int; Auggie/rf-qa have none) | findings.py:91-93 | findings_v2.py:98-100 | card_convert invents `F<i>` (:168-176) |
| 5-level severity (`Critical`, `High`, `Medium`, `Low`, `Nit`, or lower-case hints) | findings.py:96-97 (tuple :14, case-sensitive) | findings_v2.py:103-104 | card_convert maps high->MAJOR, medium/low/nit->MINOR, `Critical`->CRITICAL after lowercasing (:71-83, :103-104) |
| rf-qa `IMPORTANT` / DNSP `HIGH` | findings.py:96-97 | findings_v2.py:103-104 | card_convert `important`->MINOR non-blocking (:82) |
| No `blocking` bool | findings.py:98-99 | findings_v2.py:105-106 | X ledger computes it (review_ledger.py:41-49) |
| Category `security`, `error-handling`, `correctness`, ... (none of Auggie's 18 equals one of the 6) | findings.py:102-103 | findings_v2.py:109-110 | X ledger has no category |
| `path`+`line` only, no exact quote | findings.py:104 (anchor must be a string) | findings_v2.py:124-125 unless rewritten as `citations` | |
| `line: null` (file-level) or `line_range_end: null` | n/a | findings_v2.py:76-78 (int, >=1) if put in a citation | |
| rf-qa `Location [file:section]` | findings.py:104 | findings_v2.py:76-78 (no integer lines) | |
| Absolute path or `..` (Auggie asks repo-relative; PR paths are repo-relative) | n/a | findings_v2.py:67-75 | |
| Body/`why`/`Issue` > 300 chars | findings.py:118 | findings_v2.py:111 | card_convert truncates (:199-201) |
| > 8 `cross_references` as refs | findings.py:111-117 | findings_v2.py:114-120 | |
| > 8 locations (`affected_files`) as citations | n/a | findings_v2.py:128-129 | |
| `evidence` excerpt used as quote > 200 or < 12 chars | findings.py:104 | findings_v2.py:79-80 / :126 | |
| String confidence placed in `self_confidence` | n/a | findings_v2.py:178-182 | |
| Any one bad line | that line only (findings.py:188-192) | whole block `invalid` (findings_v2.py:301-302) -> whole reviewer dropped (cluster.py:221, :256-257) | |
| Unknown keys (`in_diff`, `why`, `recommendation`, `title`) | accepted silently | accepted silently | X ledger rejects (review_ledger.py:809-817) |

Key Takeaways
- [ext] A code-review finding fails at id, severity, blocking and category before location is even checked; an rf-qa finding fails at severity (IMPORTANT) first.
- [E1] The v2 block rule converts any single rejection into the loss of the whole reviewer in the E1 clustering path.

## 14. Q3 — Defect D1: literals, surfacing, policies

### 14.1 Every limit literal (grep of `cli/review/*.py`, 2026-11-13) [CODE-VERIFIED]
| Literal | v1 (`findings.py`) | v2 (`findings_v2.py`) | card_convert |
|---|---|---|---|
| anchor 12-200 | :104 | :126, :132 | — (no anchor emitted) |
| anchor2 12-200 | :108 | :136 | — |
| citation quote 12-200 | — | :80 | — (no quote emitted) |
| claim <=300 | :118 | :111 | `MAX_CLAIM = 300` :86, truncation :199-201 |
| refs <=8 | :114, :117 | :117, :120 | refs always `[]` (:215) |
| citations 1-8 | — | :128-129 | not enforced before check (unbounded extraction, then v2 rejects >8) |
| unresolved ref text 200 | — | — | `MAX_REF_TEXT = 200` :85, :108 |
| id <=16 chars | `_ID` :26 | imported :17 | imported :57 |
None of these is a named shared constant except card_convert's two; v2 repeats v1's numbers as literals. No limits in `ledger.py`, `cluster.py`, `telemetry.py`; none in the experiment ledger (§10.2).

### 14.2 How a rejection is surfaced [CODE-VERIFIED]
- v1 parser: every error kept as `{line,msg}` (findings.py:191) — the parser does not lose them.
- Master ledger: one warning per bad reviewer with the error count and ONLY `errors[0]["msg"]` (ledger.py:130-134); the stored entry is `block_ok` only (:141-149). Rejected finding ids, lines and reasons beyond the first are not persisted. The rejected line's id is not even in the message (the message is the rule text, e.g. "claim must have at most 300 characters"; findings.py:86).
- v2 parser: every error kept (findings_v2.py:286). What `cluster_cmd`/`verify_cmd` persist from `errors` was not read in this slice [UNVERIFIED] (see Gaps).
- card_convert: rejection reason per finding in `problems` (card_convert.py:353) — the best surfacing of the three, but truncations are not counted (§3.4).
- Briefs: neither the product brief (document_review_loop_prompts.md:60) nor the E2 brief (run-reviewer.sh:17) nor the shadow brief (reviewer-spec.md:39, which does state 300 for claim but not quote 12-200 or refs 8) states all limits.

### 14.3 Limit policies compared
| Policy | Where it exists today | Effect on the D1 data (COMBO-REPORT.md:292: 56 anchor, 18 anchor2, 14 claim over-length; 49 blocking findings lost) | Risk |
|---|---|---|---|
| Reject (today) | v1 :104/:108/:118; v2 same + :80, :128 | all 49 lost; verdicts flipped FAIL->PASS (hand-off §2.4 D1) | silent recall loss, model-biased (luna/ember/wonder) |
| Truncate with a counter | card_convert truncates claims WITHOUT a counter (:199-201, counts :303-311) — the counter would be new | claim and quote text kept up to the limit; an over-length anchor truncated is no longer an exact quote and may then fail `locate` (findings.py:276-304) -> D5 path (missing anchor) | an anchor cut to 200 chars is still a substring of the document only if cut at the start; truncating the head keeps it locatable, so the policy must be "keep the first 200 chars" for quotes |
| No limits | experiment ledger (review_ledger.py:794-848) | nothing lost to length | report/table rendering and prompt size; long anchors make `same_defect` span overlap more likely (findings.py:377), widening D6 over-merge |
Design input (not a decision): length is a presentation concern for `claim` and a correctness concern for `anchor`/`quote` only via exact-match locating. A truncate-prefix-plus-counter rule keeps quotes locatable and makes the loss visible; rejection should be kept for structural errors (types, enums, paths) only. Either way the merge must persist per-line rejections (id, line, reason) instead of `errors[0]`.

Key Takeaways
- [E3][E1] The same four numbers are hard-coded in 9 places across v1 and v2 plus 2 named constants in card_convert; no single source of truth.
- [E3] Only the first rejection message per reviewer survives the master merge; ids are never stored.
- [E1] card_convert's truncation is silent, not counted — the premise "truncate with a counter as card_convert already does" is [CODE-CONTRADICTED].
- [E2] The study's 49 lost blocking findings are all length or format rejections that briefs never warned about.

## 15. Q4 — D5, D9, D10

- **D5 (missing anchors kept silently)** [CODE-VERIFIED]: findings.py:349-358 marks `anchor_status: missing`, sets `span None`, `section none`; ledger.py:135-138 merges it; ledger.py:184-202 opens a row with `blocking` from the reviewer. No warning anywhere in `merge_round` for a missing anchor (only :132-134 for block errors). A hallucinated quote can therefore open a blocking row. Contrast: experiment ledger refuses missing and ambiguous anchors (review_ledger.py:851-881) [E3]; E1 marks citations with unknown paths `unresolved` and counts malformed ones (cluster.py docstring :21-23; scope 02 §5 D5 row) without dropping [E1]. v2 does not check that `line_end` is within the file [UNVERIFIED whether `verify_cmd` does].
- **D9 (missing-requirement Medium vs schema blocking)** [CODE-VERIFIED]: prompt :31 grades an unstated requirement Medium (non-blocking); `missing-requirement` (findings.py:20) has no per-category blocking constraint (:96-103). v2 with `reflect_category: coverage` forces MAJOR -> blocking (findings_v2.py:44, :161-162). The experiment ledger has no category and decides blocking from grade/rule/wrong_outcome (review_ledger.py:41-49). Three rules for the same kind of finding [E3][E1].
- **D10 (`unpassable-ac` rejected)** [CODE-VERIFIED]: findings.py:17 has `unpassable-check`; :102-103 rejects anything else with a message that does not name the value. The bad label came from the E2 harness brief, not the product prompt (§5, §11) [E2]. Same rejection in v2 (findings_v2.py:109-110). card_convert would not reject it: an unknown category word maps to `other` (:207) — a third policy (coerce) [E1].

Key Takeaways
- [E3] D5: no product path warns on a missing anchor; the experiment refuses; E1 flags and keeps.
- [E3][E1] D9: the same category has opposite blocking rules in the E3 brief and the E1 reflect rule.
- [E2][E3] D10: reject (v1/v2) vs coerce-to-other (card_convert); neither names the bad value.

## 16. Q6 — The five severity vocabularies and where each is enforced

| Vocabulary | Levels | Enforced in code at | Prose-only definition at | Blocking derived how |
|---|---|---|---|---|
| findings-v1/v2 [E3][E1] | CRITICAL / MAJOR / MINOR (+ prose "Medium" = non-blocking MAJOR) | findings.py:14, :96-101; findings_v2.py:103-108, :161-162; telemetry and experiment ledger (review_ledger.py:38) | document_review_loop_prompts.md:31 | reviewer-written bool; MINOR never; v2 reflect rule severity!=MINOR; experiment computed |
| reflect legacy [E1] | HIGH / MEDIUM / LOW + 4 deviation classes (Authorized expansion, Necessary deviation, Drift, Regression) | only via card_convert word map (:71-83) and v2 `DEVIATION_CLASSES` (:38, lower-case single words) | reflect-reviewer.md:21-26, :71 | none in the card; converter: HIGH blocking, MEDIUM/LOW not |
| rf-qa [ext] | CRITICAL / IMPORTANT / MINOR (+ HIGH for DNSP) | nowhere in Python (agent prose); DNSP "fixed-field emitter rejection" is prose (rf-qa.md:84) [UNVERIFIED as code] | rf-qa.md:106-111, :450; rf-qa-qualitative.md:111, :885 | by definition; C and I blocking |
| Auggie / PR [ext] | Critical / High / Medium / Low / Nit | `Severity` models.py:106-113; `severity_router.py:34-52, :122-214` | severity-rubric.md:11-101 | derived from remapped level -> route |
| pragmatic [ext] | blocking / minor | none in code | rf-qa.md:108-109 (and the same rule in RULES-type prose) | by definition |

Key Takeaways
- [E3][E1][ext] Only two vocabularies are enforced in Python (v1/v2 and PR `Severity`); rf-qa and reflect legacy exist only in agent prose plus card_convert's lossy word map.
- [ext] Every vocabulary except v1/v2 derives blocking from level or definition; v1/v2 alone trust a reviewer-written flag.

## 17. Q7 — Should the exact-quote anchor stay a first-class location?

Evidence for keeping it:
- It is the only location that works for a single document without line numbers and survives edits: span mapping across versions is built on it (findings.py:413-457; ledger re-anchoring ledger.py:224 onward) [E3]; the experiment ledger's whole re-review flow binds rows by anchor (review_ledger.py:851-881, row `at`/`at_snapshot` :899-900) [E3].
- It is the check that catches hallucinated locations when enforced (experiment refuses missing anchors) [E3]; Auggie's `evidence` and v2's citation `quote` are the same idea attached to a path+line [ext][E1].
Evidence against it as the ONLY location:
- It cannot express multi-file evidence (reflect-post needs source+diff+spec; v2 `citations` exist for that, findings_v2.py:35, :127-130) [E1], `in_diff` (PR), file-level comments (`line: null`), multi-file observations (`affected_files`), or rf-qa's `file:section`.
- It is the largest single source of D1 loss (56 anchor + 18 anchor2 of the over-length cases, COMBO-REPORT.md:292) [E2].
Design input: keep three location kinds side by side, each optional, at least one required — (a) `anchor` (+`anchor2`) exact quote in the reviewed document, (b) `citations[]` path + line range + role + optional quote, (c) a new code-review kind carrying `in_diff` and allowing `line: null` / `affected_files` — and let each lens module declare which kind is primary (E1 already does this for clustering: `PRIMARY_ROLES` cluster.py:67-70).

Key Takeaways
- [E3] Anchor is the re-review backbone for document review and should stay first-class for single-document lenses.
- [E1][ext] It must be one of several location kinds, not the required one.

## 18. Q8 — Design input for a superset contract with pluggable lens and category namespaces

Observed building blocks (all verified above), offered as input, not as decisions:
1. **Container**: keep the `## Findings block` + fenced JSON-lines container (v1/v2 share it, findings.py:31, :38-76; findings_v2.py:24); version it by info string. [E3][E1]
2. **Core fields**: `id`, `claim`, `severity` (namespaced), at least one location kind (§17), optional `refs`, `self_confidence`; `calibrated_confidence` stays forbidden in the reviewer line (findings_v2.py:96-97). [E1]
3. **Pluggable lens**: extend `LENSES` (findings_v2.py:36) beyond `spec, reflect-pre, reflect-post` with e.g. tasklist, code-review, qa; each lens module supplies: allowed severity vocabulary, allowed categories, primary location kind/role (`PRIMARY_ROLES` cluster.py:67-70 is the precedent), required fields (v2-15 is the precedent), and a blocking predicate. The experiment's `PROFILES` table (review_ledger.py:53-59: grades + blocking predicate + cap) is a ready pattern for this. [E1][E3]
4. **Blocking ownership**: every non-v1/v2 vocabulary derives blocking (§16). A unified contract could keep the reviewer's `blocking` as an input signal and compute the effective blocking per lens predicate, recording both — this also resolves D9 (one rule per lens) and the reflect MEDIUM-drift gap (scope 03 §3.3). [E1][E3][ext]
5. **Category namespaces**: v1's 6 categories (findings.py:15-22), reflect categories (findings_v2.py:41-48), Auggie's 18 (auggie-prompts.md:49), rf-qa-qualitative's AX-1..5 (rf-qa-qualitative.md:650) do not overlap; `REFLECT_CATEGORIES` already shows a namespace-to-core mapping. A namespaced `category` (`lens:value`) with a per-lens map to a small core set keeps clustering and telemetry comparable. [E1][ext]
6. **Channel** (findings_v2.py:37) generalises: defect / grounding-gap / advisory covers reflect correctness gaps, Auggie cross-cutting observations and rf-qa notes; a rule "advisory never blocks" is missing today (§2.2). [E1]
7. **Rejection policy**: structural rejections per line, persisted with id, line and reason; length handled by truncate-prefix-plus-counter; block validity not tied to "any error" for findings that individually pass (§2.3, §14.3). [E1][E3][E2]
8. **Unknown keys**: decide explicitly; today v1/v2 accept silently and the experiment rejects (§10.2). [E3]
9. **Re-review**: v1 prior lines (findings.py:175-187) and the experiment's answer actions (`fixed/not-fixed/disputed`, review_ledger.py:65) are two re-review protocols; v2 has none (findings_v2.py:279-283). [E3][E1]

Key Takeaways
- [E1] findings-v2 is the natural base: it already has lens, channel, roles and the reviewer/calibration split.
- [E3] The experiment ledger contributes the per-profile blocking predicate, the unknown-key allowlist and the strict anchor check.
- [ext] PR and rf-qa need new namespaces and a location kind, not changes to the core fields.

## Gaps and Questions

- [UNVERIFIED] Whether `cluster_cmd` / `verify_cmd` persist the per-line `errors` from `findings_v2.parse_block` (affects D1 surfacing on the E1 side). Not read in this slice.
- [UNVERIFIED] Whether `verify_cmd` checks that `line_end` is within the cited file (v2 checks only `1 <= start <= end`, findings_v2.py:76-78).
- [UNVERIFIED] rf-qa DNSP "fixed-field emitter rejection" (rf-qa.md:84) — described as an emitter rule; no Python implementation located in this slice.
- [UNVERIFIED] Whether `remap_severity(..., deep=True)` is called only for single-source findings (severity_router.py:192-193 drops a tier whenever `deep` is true; the caller was not read).
- [CODE-CONTRADICTED] Research-prompt premise "truncate with a counter as card_convert already does for claims": card_convert truncates (card_convert.py:199-201) but keeps no counter (:303-311, :496-517).
- [CODE-CONTRADICTED] findings_v2.py:3 compatibility claim, as read for blocks or under lens `reflect-post`: false (§2.4). True per line otherwise.
- [CODE-CONTRADICTED] severity-rubric.md:95 (in_diff:false on an affected callsite -> no change) vs severity_router.py:178-189 (always drops a tier); severity-rubric.md:90 (Critical low-confidence drop is conditional) vs severity_router.py:174-175 (unconditional).
- [CODE-CONTRADICTED] (minor) scope slice 00 §5.2 lists ledger row fields "anchors, spans"; code has `anchor`, `anchor2`, `span`, `span2` (ledger.py:194-197).
- Gap: Auggie prompt lists 18 categories (auggie-prompts.md:49) but the router table has 19 incl. `security-latent` (severity_router.py:36); who emits `security-latent` was not traced.
- Gap: reflect-reviewer's Correctness-gaps table has no severity column, so card_convert never converts it (card_convert.py:264-266); advisory findings from legacy cards are invisible to the v2 stack.
- Gap: reflect-reviewer's two-word labels (reflect-reviewer.md:23-24) are not mapped by card_convert (:203); `file@rev:line` evidence (reflect-reviewer.md:87) becomes unresolved.
- Gap: no brief (product, E2, shadow) states every validator limit; the claim and refs limits are missing from the E3 and E2 briefs, the quote and refs limits from the shadow brief.
- Question: should blocking stay reviewer-written (v1/v2) or become computed per lens (every other vocabulary)? Owner decision.
- Question: which re-review protocol (v1 prior lines vs experiment answers) does the unified contract keep?
- Question: is `_REF_TOKEN`'s failure on `P10` and `T01.02` (findings.py:29) acceptable for tasklist ids? (D7 extension.)

## Stale Documentation Found

- **[STALE DOC]** `findings_v2.py:3` docstring omits that a pure-v1 line fails under lens `reflect-post` (`deviation_class` required, :147-149) and is silent on the block-level differences (empty block, priors handled at :5 only).
- **[STALE DOC]** `severity-rubric.md:90` and `:95` describe conditional tier drops that `severity_router.py:174-175` and `:178-189` apply unconditionally.
- **[STALE DOC]** `document_review_loop_prompts.md:58-62` describes the findings line without the 300-char claim limit and the 8-ref limit that `findings.py:111-120` enforces.
- **[STALE DOC]** `reviewer-spec.md:39` (shadow brief) omits the citation quote 12-200 limit (`findings_v2.py:79-80`) and the refs <= 8 limit (:114-120).
- **[STALE DOC]** `reflect-reviewer.md:23-24, :84-87` prescribe labels and an evidence form (`bar.py@base:17`) that the converter (`card_convert.py:203`, `_TOKEN` :88-90) does not accept.
- Scope slice wording (not product docs): `00-handoff-copy.md` §5.2 "anchors, spans" (code singular); research prompt "category maps :43-44" (map spans :41-48); research prompt premise on a card_convert truncation counter (none exists).

## Summary

Seven finding shapes are in scope and only two (findings-v1 [E3] and findings-v2 [E1]) are enforced by a Python validator; they share a container, the CRITICAL/MAJOR/MINOR scale, six categories and the same hard-coded 12/200/300/8 limits in nine places, and v2 adds lens, channel, deviation class, role-tagged citations and coverage while making any single bad line invalidate — and, through `cluster.py:256-257`, discard — a whole reviewer. Every other shape (reflect legacy cards, the experiment ledger, PR `Finding`, Auggie JSON, rf-qa tables) derives blocking from a level or a definition instead of trusting a reviewer flag, and none of them passes either validator: a code-review finding fails at id, severity, blocking and category, an rf-qa finding at `IMPORTANT`. D1 is confirmed on both stacks (only the first rejection message survives the master merge, no ids stored), D5, D9 and D10 are confirmed with three different policies across efforts, and card_convert truncates claims silently rather than with a counter. The design input is a findings-v2-based superset with pluggable per-lens severity, category and blocking predicates (the experiment ledger's `PROFILES` table is the precedent), three optional location kinds with the exact-quote anchor kept first-class for single-document lenses, and per-line rejection records with truncate-and-count for length.
