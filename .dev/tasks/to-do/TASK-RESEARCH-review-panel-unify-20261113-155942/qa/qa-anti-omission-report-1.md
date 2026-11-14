## Anti-Omission Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/RESEARCH-REPORT-review-panel-unification.md` (4283 lines)
**Input files checked:** `research/01-finding-contract.md` (474 lines), `research/02-ledger-merge-verdict.md` (329), `research/03-clustering.md` (396), `research/04-panel-resolution-identity.md` (318), `synthesis/synth-01-problem-current-state.md` (388), `research/scope/00-handoff-copy.md` (315); total findings enumerated: 462 (A = file 01: 107, B = file 02: 76, C = file 03: 56, D = file 04: 54, S = synth-01: 27, H = hand-off copy: 169)
**Date:** 2026-11-14
**Agent:** anti-omission agent 1 of 4 (report-only; `fix_authorization: false`; no file edited except this report)

**Method.** All six inputs were read in full. Coverage was judged by meaning, never by ID citation. For each enumerated item I searched the final report by wording variants and read the surrounding rows: Section 2 (current state, lines 105-480), Section 4 gap rows D1-D16, BL, MS, ENS, DOC (lines 578-735), the conflict sections C-01 to C-20 (lines 1190-2515), Section 7 (2624-2915), the Section 8.1 value inventory V-001 to V-6xx (lines 2921-3631) and Section 9 (3933-4197). Where a detail appears in the report only as part of a broader row, I counted it REPRESENTED and cite the row. Where an item is a micro-detail whose substance appears nowhere, I marked OMITTED and rated it. Rows marked COVERED-BY-DEDUP name the report item that absorbed them.

**Report-wide observation.** Synth-01 is carried into report Sections 1 and 2 almost verbatim (all 40 sub-headings present). Section 8.1 holds one row for every hand-off item that carries a finding, lesson, strategy, defect, script, test or artifact. The only hand-off parts without a row are navigation or provenance text (section 9 "Where to start" and the evidence trail, the header metadata, the method note); they are listed as MINOR below.

---

## Enumeration: `research/01-finding-contract.md`

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| A-01 | findings-v1 constants: SEVERITIES, 6 CATEGORIES, PRIOR_STATUSES, ACTIONS | 01 §1.1 | REPRESENTED | V-121 (l.3059); MS-01 (l.627) |
| A-02 | `_ID` pattern, max 16 characters | 01 §1.1 | REPRESENTED | V-121 (l.3059) |
| A-03 | `_REF_TOKEN` regex; `T01.02` does not match; `P10` does not match | 01 §1.1 | REPRESENTED | D7 (l.594); V-071 (l.3009); l.367 |
| A-04 | `_HEAD_FINDINGS` heading regex and `_blocks_after` fence scanner (first matching heading; `closed=False` = truncated) | 01 §1.1 | REPRESENTED | V-217 (l.3155); V-273 (exact heading `c2e3347d3`) |
| A-05 | 10 ordered v1 rejection rules; first failure per line wins; one message per line | 01 §1.2 | REPRESENTED | Section 2.3 component table (l.249, "ten ordered rejection rules per line"); l.326 (v2 "23 ordered rules") |
| A-06 | v1-6 category message does not name the bad value | 01 §1.2 | REPRESENTED | D10 (l.597); V-074 (l.3012) |
| A-07 | v1 accepts unknown keys silently (`citations`, `lens`, `path`, `line`, `in_diff`) | 01 §1.2 | REPRESENTED | MS-01 (l.627); V-475 (l.3413) |
| A-08 | v1 reviewer line has no confidence field | 01 §1.2 | COVERED-BY-DEDUP | V-139 (l.3077), V-223 (l.3161): calibrated confidence stays forbidden in reviewer lines |
| A-09 | `parse_block` outcomes: missing heading or block, several blocks (last used), unclosed block still parsed, bad JSON skipped, prior lines to `priors`, per-line lossy but block-tolerant, empty closed block is `ok=True` | 01 §1.3 | REPRESENTED | V-217, V-218, V-219 (l.3155-3157); divergence table (l.345-347) |
| A-10 | `parse_fixmap` falls back to scraping `\| id \| applied` table rows when the heading or block is missing (a lenient path the findings block lacks) | 01 §1.4 | OMITTED | not found; V-122 (l.3060) lists only the fixmap-v1 JSON shape |
| A-11 | `flat`, `locate` (0-based half-open ranges), `section_of`, `refs_norm` (scans anchor, anchor2, claim, refs; drops `SHA-*`) | 01 §1.4 | REPRESENTED | V-225 to V-227 (l.3163-3165); V-001 (l.2939); D7 (l.594) |
| A-12 | `annotate`: `anchor_status`, span, section; fp = sha256(`v1\|section\|refs`)[:16]; D5 missing anchor kept with `section="none"` | 01 §1.4 | REPRESENTED | D5 (l.592); V-069 (l.3007); stack A diagram (l.302) |
| A-13 | A missing anchor gives fp over (`none`, refs), so two hallucinated anchors with the same refs share a fingerprint and `same_defect` clusters them | 01 §1.4 | OMITTED | not found (D5 row and C-02 mention only that a hallucinated anchor can open a blocking row) |
| A-14 | v1 key takeaway: location is one exact quote in one document; no path, line, diff flag or second document | 01 §1 KT | REPRESENTED | BL-04 (l.607); V-474 (l.3412) |
| A-15 | v2 imports `_HEAD_FINDINGS, _ID, CATEGORIES, SEVERITIES, _blocks_after, _check_flat` from v1; info string `findings-v2` | 01 §2 | REPRESENTED | Section 2.4 text (l.200, private v1 names); V-217 |
| A-16 | v2 vocabularies: `V1_FIELDS`, `ROLES`, `LENSES`, `CHANNELS`, `DEVIATION_CLASSES`, `COMPLETION_STATES`, `REFLECT_CATEGORIES` | 01 §2.1 | REPRESENTED | V-210 (l.3148); V-222, V-223; BL-01 (l.604) |
| A-17 | `check_finding`: 24 ordered rules (v2-0 forbids `calibrated_confidence`; v2-1..6 = v1-1..6) | 01 §2.2 | REPRESENTED | Section 2.4 stack B diagram (l.326, "23 ordered rules per line"); V-223 |
| A-18 | v2 checks `claim` length before the anchor (order differs from v1) | 01 §2.2 | OMITTED | not found (micro-detail of rule order) |
| A-19 | v2-9..12 citations: 1-8 objects, role in ROLES, repo-relative non-empty path (no absolute, drive, leading slash, `..`), int `1<=line_start<=line_end`, quote 12-200; anchor still 12-200 when present | 01 §2.2 | REPRESENTED | V-222 (l.3160); V-221; BL-04 (l.607) |
| A-20 | v2-13..16 lens consistency, effective lens in LENSES, `deviation_class` required for `reflect-post`, 5 values | 01 §2.2 | REPRESENTED | MS-01 (l.627); l.355; V-223 |
| A-21 | v2-17/18 `reflect_category` must be one of 6 keys; `category` in the mapped set | 01 §2.2 | REPRESENTED | V-210 (l.3148); BL-02 (l.605) |
| A-22 | v2-19 blocking label rule: with `reflect_category`, `blocking == (severity != MINOR)` | 01 §2.2 | REPRESENTED | V-220 (l.3158); D9 (l.596); V-436 (l.3374) |
| A-23 | v2-20 `reflect_category: deviation` needs `deviation_class` | 01 §2.2 | COVERED-BY-DEDUP | V-210 / V-223 (v2 rule group) |
| A-24 | v2-21 `coverage_rows` list of strings, needs caller `assigned_rows`, each row inside it | 01 §2.2 | REPRESENTED | V-223 (l.3161); V-218 (empty-block rule tied to assigned rows) |
| A-25 | v2-22 `self_confidence` number 0-1 not bool; v2-23 `channel` values; `channel_of` defaults absent/unknown to `defect` | 01 §2.2 | REPRESENTED | V-223; V-293 (l.3231) |
| A-26 | Absent rules: `advisory`/`grounding-gap` not forced non-blocking; `regression` not forced blocking; `authorized`/`necessary` not forced non-blocking | 01 §2.2 | REPRESENTED | V-223 (l.3161); V-294 (l.3232); V-297 (l.3235) |
| A-27 | v2 `parse_block`: heading/block/several/unclosed errors; prior lines rejected; empty-block rule; state complete/truncated/invalid; `ok` only when complete | 01 §2.3 | REPRESENTED | V-218, V-219; divergence table (l.345-347) |
| A-28 | Consumer effect: one bad line in a native v2 block removes ALL of that reviewer's findings from clustering (`cluster.py:221, 256-257`) | 01 §2.3 | REPRESENTED | D1 (l.588); V-219; V-487 (l.3425) |
| A-29 | Q5: docstring `findings_v2.py:3` holds per line except under `reflect-post`; false at block level (priors, empty block, bad line); info string differs | 01 §2.4 | REPRESENTED | l.355 (divergence table); DOC-02 (l.663); MS-01 (l.627); V-224 (l.3162) |
| A-30 | card_convert purpose, imports, conversion share report | 01 §3 | REPRESENTED | V-211 (l.3149); V-328 (l.3266) |
| A-31 | Four card shapes and how each is recognised | 01 §3.1 | REPRESENTED | V-211; V-288 (l.3226); MS-01 (l.627) |
| A-32 | Field keys read per shape (claim, refs, category, class, id keys; markdown columns share one column for category and class) | 01 §3.1 | COVERED-BY-DEDUP | V-211 (converter row) |
| A-33 | Severity word table: blocking/major/high/must-fix/p1 to MAJOR blocking; critical/p0 to CRITICAL; minor/medium/low/important/nit/info/p2/p3 to MINOR; other words unconverted | 01 §3.2 | REPRESENTED | V-296 (l.3234); V-471 (l.3409); BL-03 (l.606) |
| A-34 | Collisions: reflect MEDIUM becomes MINOR non-blocking; `important` becomes MINOR against rf-qa IMPORTANT blocking; Auggie Medium and Low both collapse | 01 §3.2 | REPRESENTED | V-471; V-470 (l.3408); l.574 and l.910 (external-context rows); BL-03 |
| A-35 | card_convert role mapping: only `plan`, `spec`, `source` are produced (never `test`, `diff`, `artifact`); no quote and no anchor emitted | 01 §3.3 | OMITTED | not found |
| A-36 | Unresolvable evidence becomes role `unresolved`, which is not in `ROLES`, so those lines are not valid v2 but stay in `findings` and `problems` | 01 §3.3 | OMITTED | not found |
| A-37 | Limits truncate rather than reject; `MAX_REF_TEXT=200`, `MAX_CLAIM=300`; NO counter; premise "truncate with a counter as card_convert does" is CODE-CONTRADICTED | 01 §3.4 | REPRESENTED | D1 (l.588); l.139 (component table); DOC-01 (l.662); V-211; V-471 |
| A-38 | Category derivation: `risk` to `safety` when the claim matches `_SAFETY`, else `other`; reflect category maps to first v1 category; v2-19 always holds for converted lines | 01 §3.4 | OMITTED | not found (only "coerces unknown to other" at D10, l.597) |
| A-39 | Deviation class taken only if exactly one of the five words; two-word labels do not match; such rows fail v2-20 when category word is `deviation` | 01 §3.4 | REPRESENTED | V-295 (l.3233); l.669 (DOC row) |
| A-40 | Converted lines carry no `lens`, so `check_finding` runs with `lens=None` and v2-15 never fires; a converted UC-2 card is not checked as `reflect-post` | 01 §3.4 | OMITTED | not found |
| A-41 | Ids: `_new_id` keeps a valid unique id else `F<index>`; `seen.add` runs even for unconverted lines | 01 §3.4 | OMITTED | not found (micro-detail) |
| A-42 | An entry with no claim key gives an empty claim, which passes v2-7 (no minimum) and converts | 01 §3.4 | OMITTED | not found |
| A-43 | Summary outputs: `share = converted/units`; an unlisted card counts as one unconverted unit | 01 §3.5 | REPRESENTED | V-328 (l.3266); Section 2.1 table (67.28%) |
| A-44 | card_convert key takeaway: only place mapping a free severity vocabulary to CRITICAL/MAJOR/MINOR; collides with rf-qa; drops MEDIUM | 01 §3 KT | REPRESENTED | V-471; V-296 |
| A-45 | PR `Severity` enum (5 tiers), `Finding` dataclass fields, `fix_key`, no validation, no id, `SkillResult.findings` | 01 §4 | REPRESENTED | V-451 (l.3389); BL-18 (l.621); BL-06 (l.609) |
| A-46 | `fix_key` is a third fingerprint scheme (path+line+body) a unified contract must keep or replace | 01 §4 | REPRESENTED | BL-06 (l.609); BL-18 (l.621); V-451 |
| A-47 | PR finding rejections: no id, 5-level severity, category, no blocking bool, path+line but no anchor, `line: None`, body over 300, extra fields, role `diff` / no `in_diff` | 01 §4 | REPRESENTED | BL-02, BL-03, BL-04, BL-18 (l.605-621); V-470 (l.3408); V-455 |
| A-48 | Prompts file placeholders `CANDIDATE, BASELINE, PRIOR, N, IDS`; no source placeholder (D8) | 01 §5 | REPRESENTED | D8 (l.595); V-006 (l.2944); V-514 (l.3452) |
| A-49 | Grading check: blocking by consequence sentence; "Medium" is a prose-only fourth grade; D9 cross-stack conflict | 01 §5 | REPRESENTED | D9 (l.596); V-128 (l.3066); V-073 (l.3011); V-514 |
| A-50 | The loop brief does not state the 300-character claim limit or the 8-ref limit | 01 §5 | REPRESENTED | MS-05 (l.631); V-221 (l.3159); G-16 |
| A-51 | Empty block valid in v1, invalid in v2; prior lines v1 only; merge refuses a round with no valid block (D3 is documented behaviour) | 01 §5 | REPRESENTED | V-218 (l.3156); V-429 (l.3367); D3 (l.590) |
| A-52 | `unpassable-ac` is an E2 harness brief error, not a product brief error | 01 §5 | REPRESENTED | D10 (l.597); V-074 |
| A-53 | reflect-reviewer: four deviation classes with two-word labels for the first two | 01 §6 | REPRESENTED | V-254 (l.3192); V-295 |
| A-54 | Advisory Correctness-gaps table; non-gating; never a 5th class | 01 §6 | REPRESENTED | V-297 (l.3235); V-289 (l.3227) |
| A-55 | Reflect severity scale HIGH/MEDIUM/LOW tied to class | 01 §6 | REPRESENTED | V-296 (l.3234); V-460 (l.3398) |
| A-56 | Correctness-gaps table has no severity column so `card_convert` never converts advisory rows | 01 §6 | REPRESENTED | V-297; l.641 row; l.669 DOC row |
| A-57 | `bar.py@base:17` evidence form is not matched as a path, so the finding becomes unconverted | 01 §6 | REPRESENTED | l.669 (DOC row) |
| A-58 | The card has no `blocking` concept; blocking comes only from the severity word | 01 §6 | REPRESENTED | V-296; V-500 (l.3438) |
| A-59 | Shadow brief (`reviewer-spec.md:39`): only findings-v2 text, UC-1 roles plan/spec; `reviewer_model_self_report` line | 01 §7 | REPRESENTED | V-273 (l.3211); V-291 (l.3229) |
| A-60 | Shadow brief omits citation quote 12-200 and refs 8 limits | 01 §7 | REPRESENTED | DOC-07 (l.668); MS-05 (l.631) |
| A-61 | Shadow brief example is MAJOR + `blocking:false` with no `reflect_category` (never exercises the label rule); brief does not ask for `reflect_category`, `channel`, `coverage_rows`, `self_confidence`, so those v2 fields are unreachable from shadow reviewers | 01 §7 | OMITTED | not found |
| A-62 | Reflect brief has three sections; source document reaches only the `qa` persona | 01 §7 | REPRESENTED | V-252 (l.3190); V-134; V-516 (l.3454); D8 |
| A-63 | Auggie output contract: JSON object, finding fields (18 categories, `severity_hint`, `evidence`, `confidence`, `in_diff`), `cross_cutting_observations` | 01 §8.1 | REPRESENTED | V-449 (l.3387); BL-04 (l.607) |
| A-64 | Auggie has two location kinds (line-anchored and multi-file); no id, no blocking flag, no length limit; `evidence` allowed null | 01 §8.1 | REPRESENTED | V-449; BL-04; BL-18 |
| A-65 | Severity rubric: five tiers, remap algorithm | 01 §8.2 | REPRESENTED | V-450 (l.3388) |
| A-66 | Router code: category table incl. `security-latent`; unknown hint to Medium; route Critical/High deep fix, Medium fix, Low/Nit report-only | 01 §8.2 | REPRESENTED | V-452 (l.3390); V-476 (l.3414) |
| A-67 | Two rubric-versus-code mismatches (`in_diff:false` drop; low-confidence Critical drop) | 01 §8.2 | REPRESENTED | BL-17 (l.620); V-549 (l.3487) |
| A-68 | Blocking is derived, never reviewer-supplied, in the PR stack | 01 §8.2 | REPRESENTED | V-455 (l.3393); BL-23 (l.626) |
| A-69 | rf-qa "Review severity rule" (blocking vs minor by definition; CRITICAL/IMPORTANT blocking) | 01 §9 | REPRESENTED | V-456 (l.3394); BL-03; BL-23 |
| A-70 | rf-qa report table columns (`# \| Severity \| Location \| Issue \| Required Fix`); no id, blocking, category, quote or line | 01 §9 | REPRESENTED | V-442 (l.3380); BL-03 |
| A-71 | rf-qa-qualitative `Items Reviewed` table with axis AX-1..AX-5 (checklist dimension on a check row) | 01 §9 | REPRESENTED | V-443 (l.3381); BL-21 (l.624) |
| A-72 | rf-qa synthetic-dnsp finding: severity HIGH, 7 fields, own dedup key and counter | 01 §9 | REPRESENTED | BL-03 (l.606); V-461 (l.3399) (the HIGH word; the dedup-key detail is not carried, which is rf-qa-internal) |
| A-73 | rf-qa verdict: any CRITICAL or IMPORTANT is FAIL | 01 §9 | REPRESENTED | V-456; BL-13 (l.616) |
| A-74 | Rejections an rf-qa finding would hit (IMPORTANT, id, blocking, category, `[file:section]`, long issue text) | 01 §9 | REPRESENTED | BL-03; BL-04; V-470 |
| A-75 | Master ledger row built from v1; fields; stores no rejected-line ids and only `block_ok` | 01 §10.1 | REPRESENTED | V-123 (l.3061); D1 (l.588) |
| A-76 | Experiment ledger input: key allowlist, grades, `anchor`/`finding` required, no length limits, all-or-nothing validation | 01 §10.2 | REPRESENTED | V-417 (l.3355); V-475 (l.3413); C-02 Option C (l.1289) |
| A-77 | Blocking computed by `_blocking_spec_panel`; `make_row` forces non-blocking out of scope or in a sweep; `PROFILES` is a pluggable pattern | 01 §10.2 | REPRESENTED | V-417; V-474 (l.3412); M1-04 (l.3646) |
| A-78 | `check_anchors` refuses missing (`E-ANCHOR`) and ambiguous anchors; three anchor policies exist | 01 §10.2 | REPRESENTED | l.264; V-472 (l.3410); D5 (l.592) |
| A-79 | Experiment row fields (`R<N>`, label, round_found, at, at_snapshot, origin, scope, caused_by, status, mappings, claims, history); no category, refs, fingerprint or reviewer identity | 01 §10.2 | OMITTED | not found (row-schema detail; the report carries only the verified invariants) |
| A-80 | E2 harness `BLOCK_OK` is a fence grep only: a third meaning of "block ok" | 01 §11 | REPRESENTED | Section 2.2 harness defects (l.207); V-552 (l.3490) |
| A-81 | `COMBO-REPORT.md:292` loss figures; `.catfix.md` copies needed for `unpassable-ac` reports | 01 §11 | REPRESENTED | figures: V-057, V-065, D1 (l.588). The `.catfix.md` copies: OMITTED (MINOR, effect detail of D10; see Omissions table) |
| A-82 | `COMBO-REPORT.md:371` recommendation (truncate or instruct and re-validate); `source.md` shipped next to the candidate | 01 §11 | REPRESENTED | l.1258 (C-02); V-169 (l.3107) |
| A-83 | Q1 field-by-field superset table across 7 shapes | 01 §12 | REPRESENTED | MS-01 (l.627); V-469 (l.3407); V-474 |
| A-84 | Q1 takeaway: only severity word, claim and a location are common; blocking reviewer-written only in v1/v2; v2 covers most of the superset | 01 §12 KT | REPRESENTED | V-469; l.1241 |
| A-85 | Q2 table of every validator rule rejecting a code-review or rf-qa finding | 01 §13 | REPRESENTED | BL-02/03/04/18 (l.605-621); V-470 |
| A-86 | Q3 limit literals in nine places plus two named constants; no shared constant | 01 §14.1 | REPRESENTED | MS-01 (l.627); V-221 (l.3159) |
| A-87 | Surfacing: v1 parser keeps `{line,msg}`; master merge keeps only the count and first message; card_convert keeps a per-finding reason in `problems` (best surfacing) | 01 §14.2 | REPRESENTED | D1 (l.588); V-065. The `problems` field detail: OMITTED (MINOR, see Omissions table) |
| A-88 | Briefs do not state every limit (product, E2, shadow) | 01 §14.2 | REPRESENTED | MS-05 (l.631); DOC-07 (l.668) |
| A-89 | Limit policies compared: reject / truncate with counter / no limits, with effect on the D1 data and risk | 01 §14.3 | REPRESENTED | C-02 Options A-C (l.1253-1318) |
| A-90 | Design input: keep first 200 characters (a head-truncated quote stays locatable); reject only structural errors; persist per-line rejections | 01 §14.3 | REPRESENTED | V-473 (l.3411); C-02 Option B (l.1275) |
| A-91 | Long anchors make `same_defect` span overlap more likely, widening D6 over-merge | 01 §14.3 | REPRESENTED | l.1301 |
| A-92 | Q4 D5 policies (v1 keep, E1 flag and keep, experiment refuse) | 01 §15 | REPRESENTED | V-472; D5 (l.592) |
| A-93 | Q4 D9: same category has three blocking rules across stacks | 01 §15 | REPRESENTED | D9 (l.596); V-436; C-16 |
| A-94 | Q4 D10: v1/v2 reject, card_convert coerces to `other`; neither names the bad value | 01 §15 | REPRESENTED | D10 (l.597); V-472 |
| A-95 | Q6: five severity vocabularies and where each is enforced; only two enforced in Python | 01 §16 | REPRESENTED | BL-23 (l.626); V-460 (l.3398), V-461 (l.3399) |
| A-96 | Q7: exact-quote anchor stays first-class for single-document lenses; is the largest source of D1 loss; cannot express multi-file evidence | 01 §17 | REPRESENTED | V-473 (l.3411); BL-04 (l.607); C-01 |
| A-97 | Q7 design input: three optional location kinds; each lens declares its primary kind | 01 §17 | REPRESENTED | BL-04 target; 7.1.3 (l.2760-2765); V-474 |
| A-98 | Q8 design input 1-9 (container, core fields, pluggable lens, blocking ownership with recorded effective blocking, namespaced categories, channel rule, rejection policy, unknown-key decision, re-review protocol) | 01 §18 | REPRESENTED | V-474; M1-04 (l.3646); 7.1.3 (l.2765); l.2045 |
| A-99 | Gap: whether `cluster_cmd`/`verify_cmd` persist per-line v2 errors | 01 Gaps | REPRESENTED | closed by R03: l.346 and l.1270 (`cards[].errors`, `cluster_cmd.py:161`); V-row l.3528 |
| A-100 | Gap: whether `verify_cmd` checks `line_end` inside the cited file | 01 Gaps | REPRESENTED | l.141 (out-of-range, `verify_cmd.py:66-67`) |
| A-101 | Gap: rf-qa DNSP "fixed-field emitter rejection" is prose, no Python implementation found | 01 Gaps | REPRESENTED | Q-42 (l.3986, G-17: rf-qa "fixed-field emitter rejection" has no located Python implementation) |
| A-102 | Gap: whether `remap_severity(deep=True)` has a caller | 01 Gaps | REPRESENTED | BL-16 (l.619) (no caller passes `deep=True`) |
| A-103 | Gap: `security-latent` emitter not traced | 01 Gaps | REPRESENTED | V-476 (l.3414); closed item C-03 |
| A-104 | Gaps: reflect Correctness-gaps table never converted; two-word labels unmapped; no brief states every limit | 01 Gaps | REPRESENTED | l.669; V-297; MS-05 |
| A-105 | Questions: blocking reviewer-written or computed per lens; which re-review protocol; `P10`/`T01.02` acceptability | 01 Gaps | REPRESENTED | C-16 (l.2187); l.2045 (one re-review protocol); D7 (l.594) |
| A-106 | Stale documentation list (docstring :3, rubric :90/:95, prompt :58-62, shadow brief :39, reflect-reviewer labels, slice wording) | 01 Stale | REPRESENTED | DOC rows (l.660-690); l.355, l.668, l.669 |
| A-107 | Summary: seven shapes, two enforced; nine-place limits; D1/D5/D9/D10 confirmed; design input findings-v2 superset | 01 Summary | REPRESENTED | V-469 (l.3407); l.1241 |

## Enumeration: `research/02-ledger-merge-verdict.md`

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| B-01 | ledger.py imports only the v1 contract (no `findings_v2`, no `cluster`); schema constants; `new_ledger` sets `cap_reviews`; `load` checks only `schema`; `save` is atomic | 02 §1.1 | REPRESENTED | V-002 (l.2940); V-123 (l.3061); Section 2.3 module table |
| B-02 | `merge_round` round check: `n == len(rounds)+1`; no comparison with `cap_reviews` | 02 §1.2 | REPRESENTED | D16 (l.603); V-080 (l.3018) |
| B-03 | Duplicate reviewer id check (`ledger.py:119-121`) | 02 §1.2 | OMITTED | not found (micro-detail) |
| B-04 | Per reviewer: `parse_block`, `block_ok`, ONE warning with error count and only the first message, findings annotated whether or not the block is ok, entry stores only `block_ok` | 02 §1.2 | REPRESENTED | D1 (l.588); V-065 (l.3003) |
| B-05 | No-valid-block refusal only when NO reviewer is valid | 02 §1.2 | REPRESENTED | D3 (l.590); V-067 (l.3005) |
| B-06 | Row match: a group matches the FIRST existing row for which any member is `same_defect` | 02 §1.2 | OMITTED | not found (the matching rule is described in R03 terms only; first-match-wins is absent) |
| B-07 | New row: blocking = any member; category, anchor, span, claim, fp from `group[0]`; confidence via `_confidence` | 02 §1.2 | REPRESENTED | D6 (l.593); D4 (l.591); V-070 (l.3008) |
| B-08 | Matched row: blocking overwritten by the current round's members (`refound` rule), re-anchor on first member with span, `resolved_check`/`resolved` to `regressed`, claim and category never updated | 02 §1.2 | REPRESENTED | D4 (l.591, "one non-blocking re-report can also un-block"); D6; V-228 (l.3166); V-430 (l.3368) |
| B-09 | Clearing loop: every `resolved_check` row nobody re-reported becomes `resolved`; `block_ok` never consulted (D2); docstring :112 contradicted | 02 §1.2/1.4 | REPRESENTED | D2 (l.589); V-066 (l.3004); l.258 |
| B-10 | Prior lines become `prior_note` history events; unknown prior id is a warning | 02 §1.2 | REPRESENTED | V-430 (l.3368) |
| B-11 | Verdict = FAIL iff brief non-empty; decision PASS/REVISE/ESCALATE; round record fields; result dict | 02 §1.2 | REPRESENTED | stack A diagram (Section 2.4, from l.292); V-433 (l.3371); l.258 |
| B-12 | Helpers: `_confidence` overlap/single, `_decision`, `_brief_ids` read only blocking and status | 02 §1.3 | REPRESENTED | D4 (l.591); D16 (l.603) |
| B-13 | `verdict()` returns the stored verdict of the last round and never recomputes | 02 §1.3 | OMITTED | not found (relevant to `defer` rewriting the stored verdict; V-119 asks for one shared `decide()` but does not state this fact) |
| B-14 | `apply_revision`: applied and touched by a diff hunk moves open/regressed to `resolved_check`; spans mapped through the diff | 02 §1.3 | REPRESENTED | V-432 (l.3370); V-118 (l.3056) |
| B-15 | `apply_revision` also refuses when `--old` sha256 differs from the last round's `doc_sha256`; reports `named_not_touched` and `rejected_by_reviser` | 02 §1.3 | OMITTED | not found (V-432 names only the success path) |
| B-16 | `defer` sets `deferred`, removes the lid from `brief_ids`, and rewrites the stored verdict and decision to PASS when empty | 02 §1.3 | REPRESENTED | V-119 (l.3057) |
| B-17 | `capture` builds the `review-capture/1` matrix | 02 §1.3 | REPRESENTED | V-125 (l.3063) |
| B-18 | `render_merged_report`: `review: n of cap`, per-reviewer `block ok`, table prints `confidence`, blocking findings with current members, `## Escalation` instead of Reviser brief when ESCALATE | 02 §1.3 | REPRESENTED | V-127 (l.3065); D4 (l.591, "printed `:435,:473`") |
| B-19 | D2 re-read at current lines (hand-off claim CODE-VERIFIED; docstring contradicted) | 02 §1.4 | REPRESENTED | D2 (l.589); DOC row for ledger docstring |
| B-20 | D3: a round PASSES with one valid reviewer; pinned by `test_review_ledger.py:376` | 02 §1.4 | REPRESENTED | D3 (l.590) |
| B-21 | D4: blocking half verified; "confidence never used" partly CONTRADICTED (display only); one non-blocking re-report can UN-block | 02 §1.4 | REPRESENTED | D4 (l.591); V-068 (l.3006) |
| B-22 | D16a: round 4 accepted; `merge_cmd.py:40-41` help text "1, 2 or 3" stale | 02 §1.4 | REPRESENTED | D16 (l.603); DOC-13 (l.674) |
| B-23 | D16b: `--cap` ignored on an existing ledger (documented in help but silent, no warning) | 02 §1.4 | REPRESENTED | D16 (l.603); V-080 |
| B-24 | D16c: verify-only is not a code mode; no `verify` symbol in ledger.py | 02 §1.4 | REPRESENTED | D16 (l.603); V-435 (l.3373) |
| B-25 | `merge_round` mutates `ledger["rows"]` in place before the round record is appended; `merge_cmd` saves only after rendering | 02 §1.4 | OMITTED | not found (micro-detail) |
| B-26 | `members_by_lid` includes members whose own line was valid even if the reviewer's block was not ok: an invalid reviewer can prevent clearing by re-reporting, its absence never blocks clearing | 02 §1.4 | COVERED-BY-DEDUP | D2 (l.589) (the clearing-ignores-`block_ok` finding) |
| B-27 | `render_merged_report` at round 4 with cap 3 would print "review: 4 of 3" (inference) | 02 §1.4 | OMITTED | not found (MINOR) |
| B-28 | KT: ledger is a deterministic any-reviewer-blocks model; absence of re-report clears; cap and round limit are labels only; adopting it as the shared core imports D2/D3/D4/D16 into reflect | 02 §1 KT | REPRESENTED | V-477 (l.3415); V-234 (l.3172) |
| B-29 | `merge_cmd`: options, flow, `--resolution` used only to look up model per reviewer, always exits 0 on a successful merge, no telemetry call | 02 §2.1 | REPRESENTED | V-002; V-478 (l.3416); l.2439 (exit codes); D15 (l.602) |
| B-30 | `ledger_cmd`: `EXIT_BY_DECISION` 0/10/11, `revise` adds `fixmap_ok`, `defer` human command, `verdict`, `capture` | 02 §2.2 | REPRESENTED | V-433 (l.3371); V-002; V-119 |
| B-31 | KT: CLI is a thin wrapper, keep the shape and replace the merge core; `--resolution` couples merge to the panel resolution file (E2 reused the schema) | 02 §2 KT | REPRESENTED | V-478 (l.3416); V-180 (l.3118) |
| B-32 | Test `:376-385` pins D3 AND D2 (final assertion `:385`); scope slice listed it only under D3 | 02 §3 | REPRESENTED | D2 (l.589, "final assertion `:385` expects `resolved`"); V-244 (l.3182) |
| B-33 | Test `:408-417` pins D5 (missing anchor kept, blocking) | 02 §3 | REPRESENTED | D5 (l.592); V-244 |
| B-34 | Test `:518-544` pins the single-reviewer un-block side of D4 | 02 §3 | REPRESENTED | V-479 (l.3417); V-236 (l.3174) |
| B-35 | Test `:547-566` (a late non-blocking cluster cannot mask a blocking one) is a correct invariant to keep | 02 §3 | OMITTED | not found as a keep-decision (the flip list in V-236 does not mention it; see Omissions table) |
| B-36 | Tests to keep: verdict and decision at rounds 1-3, escalate prints `verdict: FAIL`, no-valid-block refused, round sequencing, `test_review_cli.py:236` output shape | 02 §3 | COVERED-BY-DEDUP | V-236 (gate G2: only the listed lines flip); V-127 (final `verdict:` line pinned) |
| B-37 | No test covers `--cap` on an existing ledger or round 4; no test outside the two review test files references `merge_round` | 02 §3 | REPRESENTED | D16 (l.603, "No test"); V-479 |
| B-38 | KT: three tests encode "one reviewer decides" and must change on purpose for quorum, calibration or a grader | 02 §3 KT | REPRESENTED | V-479 (l.3417); V-236 |
| B-39 | Audit D scripts: `audit.py` checks, `audit2.py` re-implements the product rules and flags verdict flips, `anch.py`, `bok.py` | 02 §4.1 | REPRESENTED | V-057 (l.2995); V-536 (l.3474); DOC-17 (l.678) for `anch.py`. `bok.py` purpose (tests the old `unpassable-ac` category hypothesis): OMITTED (MINOR) |
| B-40 | 49 blocking findings lost: 24 anchor, 14 anchor2, 10 claim, 1 refs; none by category or severity | 02 §4.2 | REPRESENTED | D1 (l.588); V-065; V-480 (l.3418) |
| B-41 | All dropped findings 92 (56/18/14/3/1); per-model counts (luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1) are all drops, not blocking | 02 §4.2 | REPRESENTED | V-167 (l.3105); V-037 (l.2975) |
| B-42 | Verdict flips: audit D names 3 (not 4); 4 EXCLUDE flag lines because one merge lost two blocking findings | 02 §4.2 | REPRESENTED | V-168 (l.3106); l.672; l.1163 |
| B-43 | Total-loss merges: 5 reviewer-level cases, not verdict flips | 02 §4.2 | REPRESENTED | l.672; l.1163 ("3 named flips plus total-loss merges") |
| B-44 | Unexplained count gap: haiku 1085/1108 and grok 205/207 against reason tally 7 and 1 | 02 §4.2 | REPRESENTED | G-24 (l.3978) |
| B-45 | Loss trace in five steps; 45 merges kept no `merge-stdout.txt` | 02 §4.3 | REPRESENTED | D1 (l.588); V-178 (l.3116); V-480 |
| B-46 | The loss is D1 made verdict-changing by D3 and by the absence of any record; 13 blocking rows with null span show non-existence tolerated while length is punished | 02 §4.3 | REPRESENTED | D3 (l.590); V-176 (l.3114); C-02 (l.1253) |
| B-47 | X1 chaining: 195 chained rows among 1398 (all rows), 83 mega-rows, row keeps first member only, overlap confidence inflated | 02 §4.4 | REPRESENTED | D6 (l.593); V-057; V-486 (l.3424) |
| B-48 | X5: row blocking == any member, FAIL iff blocking row, 0 violations over 264 merges (rules faithful, defects are in the rules) | 02 §4.4 | REPRESENTED | V-177 (l.3115) |
| B-49 | X6: "current call only" re-merge rule irrelevant at round 1, so E2 gives no evidence on rounds 2-3, D2 or D16 | 02 §4.4 | REPRESENTED | V-061 (l.2999); G-22 |
| B-50 | C5: `report_sha256` detected 16 stale merges; a reusable integrity field for the run manifest | 02 §4.4 | REPRESENTED | V-053 (l.2991); V-057; V-480; l.453 |
| B-51 | KT: merge must record every rejected line (id, reason, blocking flag) and must not compute PASS while a rejected line was blocking | 02 §4 KT | REPRESENTED | V-480 (l.3418); C-02; C-15 |
| B-52 | Why `merge_round` cannot take v2: v1-only parser, `annotate` needs `anchor`, single-span row view, single-document revision mapping | 02 §5.1 | REPRESENTED | V-481 (l.3419); MS-03 (l.629); BL-04 (l.607) |
| B-53 | v2 replacements for `annotate`: `cluster.annotate`, `PRIMARY_ROLES`, `same_defect_v2` (multi-file), unresolved citations kept, `cluster_v2` support/representative/chained | 02 §5.2 | REPRESENTED | V-212 (l.3150); V-481; MS-02 (l.628); C-12 |
| B-54 | A v2-capable merge needs five things (parse v2 and keep errors; replace annotate plus line-range check; ledger rows keyed by citation sets with per-path diff map; row match by `same_defect_v2`; anchor-to-citation step) | 02 §5.3 | REPRESENTED | V-481; V-225 (l.3163); MS-02 (l.628, anchor-to-citation); M1 steps |
| B-55 | Stricter v2 loss mode: one bad anchor removes all of a reviewer's findings; applied to E2's 80 reviewer cases they would all become total-loss | 02 §5.4 | REPRESENTED | D1 (l.588); V-219; C-15 Option B (l.2146) |
| B-56 | Experiment ledger model: find once at review 1, one input per find, no clustering; the installed command's "panel" means expert personas in one session | 02 §6.1 | REPRESENTED | l.264; V-413 (l.3351); Section 2.3 note (l.267) |
| B-57 | Verify-only at reviews 2-3: answers plus new rows; evidence quote must occur in the new snapshot; `resolved` only when the anchor maps; new rows only in changed hunks | 02 §6.1 | REPRESENTED | l.264 (answers-only, evidence quote); C-13 Option B (l.2013) |
| B-58 | Verify-only mechanics: `FROZEN_FIELDS`, `E-ILLEGAL`, `E-INCOMPLETE`, new-row scope `in`/`outside` with `caused_by`, lock file and `--dry-run`, `decide()` formula with `U` and X items, sweep `would_block`/`challenges`, `E-TAMPERED` | 02 §6.1 | OMITTED | partly (body-sha tamper check and one sweep are named at l.264); the remaining mechanics are not carried (MINOR; the report carries the verified invariants, see Omissions table) |
| B-59 | Blocking is computed by `make_row`; reviewer input has no `blocking` key; `PROFILES` has one entry `spec-panel`; two places outside `PROFILES` still name grades | 02 §6.1 | REPRESENTED | l.264; V-417 (l.3355); M1-04 (l.3646). The "two places outside PROFILES" detail is OMITTED (MINOR) |
| B-60 | Row schema validation: unknown keys refused, no length limits, all-or-nothing, `check_anchors` refuses missing and ambiguous anchors | 02 §6.1 | REPRESENTED | l.264; A-76/A-78 rows; C-02 Option C (l.1289) |
| B-61 | Cap enforced by refusal (`E-CAP`; no fourth review, no third fix cycle) | 02 §6.1 | REPRESENTED | l.264; D16 (l.603); V-417 |
| B-62 | Comparison table: master vs experiment vs reflect v2 (rounds, multi-reviewer, blocking decider, bad line, anchor not found, anchor length, cap, clearing, exit codes) | 02 §6.2 | REPRESENTED | C-13 (l.1991-2055); C-15 (l.2122); l.2439; BL-13 (l.616) |
| B-63 | KT: experiment fixes D2, D4, D16a, D16c but has no multi-reviewer merge (D3 and clustering unaddressed); refusal needs a retry loop; `PROFILES` is the extension point | 02 §6 KT | REPRESENTED | l.2043; V-482 (l.3420); V-417 |
| B-64 | Stoprule flow: sealed claim ledger, `begin` refuses at cap, `seal` with one repair, `grade-prep` batches with canaries, `apply-grades`, claim statuses, pure `compute_verdict`, "silence never passes" | 02 §7.1 | REPRESENTED | l.265 (summary: sealed ledger, canaries, blind grader, `compute_verdict`, silence); V-419 (l.3357). The step-level mechanics (EXIT_REPAIR, claim status order) are part of the MINOR mechanics omission B-58 |
| B-65 | Rubric v1: B1-B3, explicit non-reasons (agreement, importance, lateness, GAP row), Q2 recorded never demotes | 02 §7.2 | REPRESENTED | l.265; V-506 (l.3444); V-421 (l.3359) |
| B-66 | `finding-grader.md`: tools Read, model sonnet, `maxTurns: 10`, `permissionMode: plan`, blind to spec, JSON-lines reply | 02 §7.2 | REPRESENTED | V-421 (l.3359); l.265 |
| B-67 | The reviewer proposes, a blind second model decides blocking; limits: one grader per batch, grader model fixed in frontmatter, no multi-reviewer clustering | 02 §7.2 | REPRESENTED | V-483 (l.3421); C-05 Option D (l.1498) |
| B-68 | Relation table: three mechanisms compared on blocking decider, late finding, PASS condition, cap, silence | 02 §7.3 | REPRESENTED | l.446; C-13; V-483 |
| B-69 | KT: none of the three ledgers combines multi-reviewer clustering with an independent blocking decision | 02 §7.3 KT | REPRESENTED | l.370; V-484 (l.3422) |
| B-70 | Phase-5 bundle: SNAPSHOT-STATE "in progress, not a final success report"; FINAL-REPORT :42 and :75; per-variant numbers; :109 six MAJOR labels vs four blocking grades | 02 §8 | REPRESENTED | l.272; V-418 (l.3356) |
| B-71 | Consequence: experiments are designs with partial runs; carry verified invariants, not claimed outcomes | 02 §8 | REPRESENTED | V-418; V-482; l.272 |
| B-72 | Synthesis table: best existing piece per concern (contract, cluster, partial-keep, rejected-line record, blocking decider, verify-only, cap by refusal, silence never passes, integrity, exit codes) | 02 §9 | REPRESENTED | V-484 (l.3422); 7.1.3 core components (l.2760-2781) |
| B-73 | Five conflicts to log: bad-line policy, missing anchor, blocking decider, round model, exit-code vocabularies | 02 §9 | REPRESENTED | C-15 (l.2122); C-02 (l.1253); C-05 (l.1448); C-13 (l.1991); C-19 (l.2394, l.2439) |
| B-74 | Gaps 1-13 (docstring contradicted; D4 partly contradicted; 3 vs 4 flips; :385 pins D2; haiku/grok count gap; verdict-flip inference; 65 vs 38 UNVERIFIED; verify-citations check; re-ask compliance; no rounds 2-3 evidence; grader_model grep-only; per-consumer decider question; anchor-only singletons) | 02 Gaps | REPRESENTED | DOC rows (l.660-690); D2/D4 rows; G-22, G-23, G-24, G-25 (l.3978 region); C-05; V-419 |
| B-75 | Stale docs: `merge_cmd.py:41`, `ledger.py:112`, hand-off "4 verdicts", `AD/summary.md:2`, hand-off D14 incomplete about installed copies | 02 Stale | REPRESENTED | DOC-13 (l.674); DOC-14 (l.675); l.672; V-425 (l.3363) |
| B-76 | Summary: faithful implementation of a weak rule set; v1-only merge; experiments supply missing invariants; no valid-success verdict exists | 02 Summary | REPRESENTED | V-477, V-481, V-482, V-418 |

## Enumeration: `research/03-clustering.md`

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| C-01 | v1 `_REF_TOKEN`: 1-4 capital letters, hyphen, digits, optional `.digits`, or `P` plus ONE digit | 03 §1.1 | REPRESENTED | D7 (l.594); V-071 (l.3009); l.367 |
| C-02 | `_SECTION_REF`: a bare section number counts only as a whole entry of the `refs` list, never from prose | 03 §1.1 | OMITTED | not found (MINOR) |
| C-03 | `section_of` returns the heading number, else a slug, else `top`; `none` when the anchor is missing | 03 §1.2 | REPRESENTED | D5 (l.592); V-132 (l.3070) (numbered-heading naming) |
| C-04 | `refs_norm` scans anchor, anchor2, claim and refs; refs are harvested from free prose, so any `XX-n` token in a claim becomes a clustering key; drops `SHA-*` | 03 §1.3 | REPRESENTED | V-485 (l.3423); BL-07 (l.610, "declared refs preferred over prose harvesting"); V-334 (l.3272) |
| C-05 | `fingerprint` = sha256(`v1\|section\|refs`)[:16]; `annotate` takes the FIRST match as span, flags `anchor_ambiguous`, spans are 0-based half-open | 03 §1.4 | REPRESENTED | V-226 (l.3164); D5 (l.592); l.353 |
| C-06 | `same_defect` in three ordered rules: equal fp with non-empty refs; else (refs intersect or both empty) and spans within 3 lines; else no; rule 2 has no category, severity or claim check; any single shared ref; `anchor2` spans count; missing anchors can merge only by rule 1 | 03 §1.5 | REPRESENTED | l.305; l.1933 (C-12 current state); BL-06 (l.609); D6 (l.593) |
| C-07 | Mixed-ref asymmetry: a finding with refs `{AC-1}` and one with `{}` NEVER merge even on the same line (v1 `:374`, v2 `:167-169`); a reviewer who writes an id and one who does not are never clustered together | 03 §5.3 | OMITTED | not derivable as a stated finding: l.1933 gives the rule ("shared or empty refs") but never states the mixed case (MINOR) |
| C-08 | `cluster`: O(n^2) pairwise loop, union-find with path halving, smaller root wins, no size cap, no chain detection, no same-reviewer guard | 03 §1.6 | REPRESENTED | D6 (l.593); V-227 (l.3165); C-12 (l.1927) |
| C-09 | v1 cluster to ledger row: parsable findings of an invalid block are clustered; row `fp` from member 0's own refs while row `refs` is the union; matched row's claim and category never updated | 03 §1.7 | REPRESENTED | D6 (l.593); V-228 (l.3166); l.2527. The "fp from one member's refs, row refs is the union" nuance is OMITTED (MINOR) |
| C-10 | Span mapping across versions (`opcodes`, `map_span`, `hunks_touch`) and sha-checked `apply_revision`: the only existing answer to "a finding moves between versions" | 03 §1.8 | REPRESENTED | l.249; BL-06 (l.609, "v1 diff mapping covers one document only"); C-12 Option B (version pin, diff mapping) |
| C-11 | Only spans are moved on revision; `fp` is NOT recomputed, so a renumbered section heading changes the next round's fp and re-match then depends on the span rule alone | 03 §1.8 | OMITTED | not found (MINOR; matters when the unified ledger re-matches across rounds) |
| C-12 | KT v1: clusters on section+refs or shared/no refs plus spans, transitively; refs from prose; row keeps member 0 forever; real cross-version machinery that v2 lacks | 03 §1 KT | REPRESENTED | D6 (l.593); l.1933; BL-06 |
| C-13 | v2 `cluster.py`: pure function over `(rid, ordinal, block, calibration)` records and a snapshot path list; imports `refs_norm` and `_check_citation`; `PRIMARY_ROLES`, `SPAN_TOLERANCE = 3` | 03 §2 | REPRESENTED | V-212 (l.3150); l.140; l.1931 |
| C-14 | `_records`: malformed records dropped and reported; a bare list is valid, a dict only when `state == "complete"`; sorted by ordinal; duplicate reviewer ids skipped | 03 §2.1 | REPRESENTED | D1 (l.588); V-219 (l.3157); l.2128 |
| C-15 | `_members`: every finding of a non-complete reviewer is skipped (Q5 answer yes); such a reviewer is in `invalid_reviewers`, excluded from `complete_reviewers` and from the support denominator and the "fewer than 2 reviewers" agreement rule | 03 §2.2 | REPRESENTED | D1 (l.588); V-487 (l.3425); l.2128 ("removes it from the support denominator") |
| C-16 | `verify_cmd` checks citations of findings regardless of block state, so findings that `cluster` drops can still appear in `precheck.json` | 03 §2.2/§4 | REPRESENTED | l.2128 ("`verify_cmd` still reads findings of invalid blocks") |
| C-17 | Per-finding: no string id or duplicate id skipped with a problem; calibration taken only when a finite number in [0,1] and not a bool | 03 §2.2 | OMITTED | not found (micro-detail; MINOR) |
| C-18 | `annotate`: citations classed `malformed` / `unresolved` (path not in snapshot by exact string equality) / `resolved`; unresolved never take part in matching | 03 §2.3 | REPRESENTED | D5 (l.592); BL-04 (l.607); V-213 (l.3151) |
| C-19 | Primary citation = first citation whose role matches the finding's OWN `lens` via `PRIMARY_ROLES`, else the first; `cluster_cmd` calls `parse_block` without a lens, so with no per-line `lens` the first citation is always primary (the per-lens primary role is inert on the CLI path) | 03 §2.3 | OMITTED | not found; the report cites `PRIMARY_ROLES` as a registry precedent (l.627, l.2644, l.2765, M1-04 l.3646) without this fact. MINOR: M1-04 adds a lens input to `review cluster` and `review merge` |
| C-20 | v2 fp = sha256(`v2\|role\|path\|\|refs\|class`), full digest, only when the primary citation is resolved; section always empty; includes `deviation_class` | 03 §2.3 | REPRESENTED | l.350 (divergence table); l.1931; D6 (l.593) |
| C-21 | `same_defect_v2`: equal fp with refs; compatible deviation classes; refs intersect or both empty; resolved citations on the same path within 3 lines (any citation, role ignored) | 03 §2.4 | REPRESENTED | l.1931; V-212 |
| C-22 | Union-find and chain detection: `chained` if any pair fails `same_defect_v2`; chained cluster kept whole; no size cap, no split, no same-reviewer guard | 03 §2.5 | REPRESENTED | D6 (l.593); V-227 (l.3165) |
| C-23 | Support, representative (highest calibrated confidence, ties by resolution order), `disputed` conditions, `blocking_any`/`blocking_all` | 03 §2.5 | REPRESENTED | V-228 (l.3166); V-508 (l.3446); l.1931 |
| C-24 | `cluster_v2` result: per-reviewer weight; `total` None unless all calibrated; `cluster_agreement` None with under 2 complete reviewers, 1.0 with no blocking cluster, else mean support over non-chained blocking clusters; citation counts | 03 §2.6 | REPRESENTED | l.162; l.680 (DOC row); V-329 (l.3267) |
| C-25 | `clusters_kept`: re-run on kept ids after the evidence validator; block validity unchanged | 03 §2.7 | REPRESENTED | l.140; l.151; V-284 (l.3222) |
| C-26 | Q4: with an always-empty section, equal non-empty refs on one file merge at any distance; an all-fp cluster is never labelled `chained` even when members are far apart | 03 §2.8 | REPRESENTED | D6 (l.593, merge at any distance); C-12 current state and evidence (l.1947, l.1979: "an all-fp cluster is never flagged chained") |
| C-27 | Q6: an anchor-only finding is always a singleton cluster; its anchor feeds only `refs_norm` | 03 §2.9 | REPRESENTED | MS-02 (l.628); V-229 (l.3167) |
| C-28 | KT v2: new location unit, class compatibility, chain flag, calibrated support, representative; stricter on invalid blocks; coarser fingerprint; anchor-only never agrees; telemetry only | 03 §2 KT | REPRESENTED | V-487 (l.3425); l.1931; l.332 |
| C-29 | `cluster_cmd`: CLI shape, card order by file name gives ordinal (alphabetical, not panel order), sidecar calibration overrides embedded, card text never modified, per-line errors persisted | 03 §3 | REPRESENTED | l.346; l.1270; MS-02 (l.628, member 0 by input order `cluster_cmd.py:138`); V-283 (l.3221) |
| C-30 | `verify_cmd`: flags missing-file, out-of-range, quote-not-found; `precheck.json` reread_set; drops nothing; a moved quote is flagged never re-located | 03 §4 | REPRESENTED | l.141; V-213; l.543; l.1284 |
| C-31 | D7 probe table (`T01.02`, `AC-0.4`, `AC-T01.02-3`, `ABCDE-1`, `D-P1`, `P1`/`P12`, `R1-F1`, `S-3 and S-6`, prose section numbers, lower case) | 03 §5.2 | REPRESENTED | D7 (l.594); l.530; V-071; V-334 |
| C-32 | Effect on tasklists: findings with no refs cluster by span alone; two no-ref findings never merge by fp; prose ids create false bridges | 03 §5.3 | REPRESENTED | D7 (l.594); BL-07 (l.610); V-334 (W-2). The mixed-ref half is C-07 |
| C-33 | The same regex is copied in `telemetry.py:23` (not imported); a fix touches two places; the scope prompt's `:22` was off by one | 03 §5.1 | REPRESENTED | D7 (l.594); V-071; l.367 |
| C-34 | KT regex: letters-hyphen-digits and P1-P9 only; misses sc:tasklist `T01.02`; misses 5+ letter prefixes and lower case; over-extracts `P1` from compound ids | 03 §5 KT | REPRESENTED | D7 (l.594); V-071 |
| C-35 | Stage 0a replay: zero dispatch, inputs are converted legacy cards, 8 of 43 runs without a usable snapshot | 03 §6.1 | REPRESENTED | V-260 (l.3198); V-374 (l.3312); V-328 (l.3266) |
| C-36 | Replay totals: 689 findings, 461 clusters, 392 singletons, 55 multi-reviewer clusters (29 not chained), 29 chained; citations 1178/623/283 | 03 §6.1 | REPRESENTED | V-329 (l.3267) |
| C-37 | Per-run table shows heavy merging in some runs (27 findings to 7 clusters; 22 to 8) and all-singleton runs with no resolved citations | 03 §6.1 | OMITTED | not found (MINOR; totals are carried, the per-run examples are not) |
| C-38 | `cluster_agreement` is 1.0000 in runs with no blocking cluster and null elsewhere; scope 04's "null for every listed run" is stale | 03 §6.1 | REPRESENTED | l.162; l.680; l.468 |
| C-39 | Agreement with recorded merged verdicts 24/358 = 6.70%, descriptive only | 03 §6.1 | REPRESENTED | V-330 (l.3268) (DROP with reason) |
| C-40 | 50-pair sheet and scorer: pair pool excludes chained-cluster pairs and same-reviewer pairs, stratified 25+25, seeded; score TP/FP/FN/TN | 03 §6.2 | REPRESENTED | V-258 (l.3196); V-335 (l.3273); l.158 |
| C-41 | Q7: precision 0.84 / recall 0.95 are AI-labelled sample figures from 3 same-family labelers; human labels (#525-#530) pending; exclude chained and same-reviewer pairs; recall is not population recall; inputs are converted legacy cards | 03 §6.3 | REPRESENTED | l.158; l.1931; V-335; V-488 (l.3426) |
| C-42 | Known weaknesses W-1..W-4 with verification tags | 03 §6.4 | REPRESENTED | V-334 (l.3272) |
| C-43 | Tests pinning current behaviour (span tolerance, chain a-b-c, unresolved paths, class compatibility, empty-section fp, anchor-only singleton, chained excluded from agreement, invalid-block not clustered) | 03 §6.5 | REPRESENTED | V-240 (l.3178); l.1959; l.2772 |
| C-44 | The chain fixture (`src/a.py` lines 10, 13, 16) is the simplest demonstration that a run of findings each 3 lines apart can grow without limit | 03 §6.5 | REPRESENTED | V-240 (l.3178); 8.3 gate row (l.3851): the fixture's findings at lines 10, 13 and 16 stop forming one chained cluster under complete-link |
| C-45 | E2 `anch.py` is not chaining evidence (measures anchor presence) and hard-codes another worktree's path | 03 §7.1 | REPRESENTED | DOC-17 (l.678); DOC-14 (l.675) |
| C-46 | E2 `audit2.py` is a line-for-line copy of `findings.py` clustering; counts 195 chained rows among 1398 rows in total; mega-row = 8+ members or 4+ sections; example L1 with 19 members across 8 sections | 03 §7.2 | REPRESENTED | V-057 (l.2995); V-486 (l.3424); l.1932; D6 (l.593) |
| C-47 | X2: 46 rows with null span (13 blocking) cannot span-cluster, so duplicates stay separate | 03 §7.2 | REPRESENTED | V-176 (l.3114) |
| C-48 | `COMBO-REPORT.md:292` item 2: 83 merged rows lump unrelated findings; the effect on ground-truth matching is not quantified | 03 §7.3 | REPRESENTED | D6 (l.593); V-057; C-12 evidence (l.1982, "not quantified") |
| C-49 | KT: E2 is the only effort that measured v1 over-merge; its replay describes the shipped clusterer; v2 expected to share the failure class; under v2's invalid-block rule the 80 E2 invalid blocks would lose ALL findings (inference) | 03 §7 KT | REPRESENTED | V-486; D6; D1 (l.588); C-15 Option B (l.2146) |
| C-50 | Q1: 13-row step-by-step comparison of the two algorithms | 03 §8 Q1 | REPRESENTED | divergence table (l.345-355); V-225 to V-229 |
| C-51 | Q2 (D6), Q3 (D7), Q4, Q5, Q6 answers | 03 §8 | REPRESENTED | D6, D7 (l.593-594); MS-02 (l.628); D1 (l.588) |
| C-52 | Q8: a code finding that moves between commits: snapshot keys on path only (no commit id or hash), joins only within 3 lines or by equal non-empty refs; no rounds in v2; v1 diff mapping covers one document; E2 says nothing about code | 03 §8 Q8 | REPRESENTED | BL-06 (l.609); C-12 Option B (version pin) |
| C-53 | Q9 design inputs 1-8 (one location model with anchor-to-citation, version pinning, section or symbol back in the fingerprint, per-target id grammar, chain control, one invalid-block policy, representative from highest confidence, measurement extension) | 03 §8 Q9 | REPRESENTED | C-12 (l.1927-1990); MS-02 (l.628); V-474; l.2772 |
| C-54 | Gaps 1-13: W-3 UNVERIFIED; D7 effect on real tasklists UNVERIFIED; population precision pending; shadow agreement 1.000; v2 invalid-block loss on E2 data is an inference; `anch.py` mis-described; 195/1398; agreement null; ambiguous replay total; line-number convention; no symbol for v2; question for E3 owners; ordering dependence | 03 Gaps | REPRESENTED | DOC rows (l.660-690); l.162, l.353, l.628; C-15 (l.2122); V-334. The "which of the 29 chained clusters are multi-reviewer is not derivable" gap is OMITTED (MINOR) |
| C-55 | Stale docs: telemetry `:22`, `anch.py` as chaining evidence, "195 of 1398 with 3+ members", agreement null, `/tmp` paths | 03 Stale | REPRESENTED | DOC rows (l.660-690): DOC-14 (l.675), DOC-17 (l.678), l.680 |
| C-56 | Summary: shared weak parts; v2 adds a coarser over-merge path, drops invalid reviewers, anchor-only singletons; quality figures are AI-labelled; unified clusterer recommendations | 03 Summary | REPRESENTED | D6; MS-02; C-12 |

## Enumeration: `research/04-panel-resolution-identity.md`

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| D-01 | `panel.py` owns three schemas (`review-panel/1`, `review-tiers/1`, `review-panel-resolution/1`); design idea: a tier is an alias for an ordered model list, a model change is a tier-file data edit only | 04 §1 | REPRESENTED | V-003 (l.2941); V-129 (l.3067); V-216 (l.3154) |
| D-02 | Template top-level keys are a closed set; any other key is an error | 04 §1 | COVERED-BY-DEDUP | V-490 (l.3428) / BL-08 (l.611) (closed schema) |
| D-03 | Slot keys are closed to `slot_id, tier, count, strategy, seed`; a template cannot bind a slot to a role, lens, persona, prompt or agent | 04 §1 | REPRESENTED | BL-08 (l.611); V-490 (l.3428) |
| D-04 | `_STRATEGIES` (fixed, random, round_robin) and `_KINDS` (first, re-review); no other review kind | 04 §1 | REPRESENTED | BL-09 (l.612); V-490 |
| D-05 | Template limits: exactly one `fixed` slot, `count` 1..4, total 1..8 reviewers, `seed` only with `random`, slot-id regex `^[a-z0-9]{1,8}$`, tier-name regex (`tier0` is syntactically legal) | 04 §1 | OMITTED | not found (MINOR schema detail; only "slot keys closed" is carried) |
| D-06 | The reflect profile runs inside `validate_panel` only when a tier file is passed and the id starts with `reflect-`; `load_panel` and `panel validate` skip it; only `resolve` applies it | 04 §1/§3 | REPRESENTED | MS-06 (l.632); V-233 (l.3171); V-281 (l.3219) |
| D-07 | Reflect profile rules: no `tier0` slot, tier0 rule inert with packaged data, every reachable model needs a class, no Fable, at most 3 reviewers, `round_robin` needs a recorded `--sequence` | 04 §1 | REPRESENTED | V-233 (l.3171); V-491 (l.3429); MS-06 (l.632); G-36 |
| D-08 | `_check_reflect_resolution` re-checks count, classes of model and fallbacks, no Fable, `launch` in sonnet/opus/haiku; it does NOT check duplicates | 04 §1 | REPRESENTED | l.1369 (launch check); V-233. The "does not check duplicates" fact is OMITTED (MINOR; the reflect-lite duplicate itself is carried at V-215) |
| D-09 | Tier file validation: placeholder tier must have empty `models` and resolves to its stand-in or fails closed; `classes` lowercase; environment keys; an empty `launch` dict is valid | 04 §1 | REPRESENTED | `launch: {}` at V-216 (l.3154), l.632. Placeholder-tier semantics, lowercase classes and environment key whitelist: OMITTED (MINOR) |
| D-10 | Provenance by `git log -S`: `placeholder` and `T3Model01` came in `9163bd1c7`; `classes`, `strict_distinct`, reflect profile in `d2d8a2d16`; `d2d8a2d16` is an ancestor of `origin/master`; the local `master` ref is stale and has no `cli/review/` | 04 §1 | REPRESENTED | l.132, l.648 (kernel is master code after #519); V-360 (l.3298); l.241. The "local master ref is stale" caution is OMITTED (MINOR) |
| D-11 | `find_path` lookup precedence and `@name` templates are CODE-VERIFIED | 04 §1 | REPRESENTED | DOC-26 (l.687); V-640 (l.3578) |
| D-12 | `select_env`: `--env`, `$SUPERCLAUDE_REVIEW_ENV`, `gateway` when `$T3Model01` is non-empty else `anthropic-only`; only `T3Model01` is read (D12) | 04 §1 | REPRESENTED | D12 (l.599); V-230 (l.3168); V-076 (l.3014) |
| D-13 | KT §1: no field for role, lens, persona or prompt; kinds closed; reflect profile is code keyed on a template-id prefix; `load_panel` never applies it; env selection keys on one variable | 04 §1 KT | REPRESENTED | V-490, V-491, V-492 (l.3428-3430) |
| D-14 | `resolve_slot`: `hard` set, candidates, stand-ins, `fixed` takes `candidates[0]` and never consults `exclude`, pool exhaustion re-admits silently unless `hard` is non-empty (`if hard:`), fallbacks rotated but not filtered by `exclude` in soft mode; the two error kinds | 04 §2 | REPRESENTED | D11 (l.598); V-232 (l.3170); V-493 (l.3431); C-04 (l.1384). The names `ExclusionExhausted` / `NoModelAvailable` are OMITTED (MINOR; their effect "fixed anchor exhaustion fatal" is carried at V-232) |
| D-15 | `resolve`: fixed slots first, re-review resolves only fixed slots with count 1, seeds (random `seed\|slot\|i`, round_robin date ordinal), `exclude = chosen`, skipped vs fatal exhaustion, reflect post-check | 04 §2 | REPRESENTED | V-231 (l.3169); V-427 (l.3365); V-232 |
| D-16 | Per-reviewer record fields and top-level fields; no duplicate flag, class, role or intended-versus-served field; `skipped_slots` and `excluded` only when used | 04 §2 | REPRESENTED | V-124 (l.3062); V-493 |
| D-17 | D11 soft versus `--hard-exclude-class` versus `--strict-distinct` compared (fixed slot, random pool, fallbacks, visibility, anchor exhaustion) | 04 §2 | REPRESENTED | C-04 Options A-C (l.1384-1447); V-232 |
| D-18 | KT §2: D11 lines moved; strict mode changes panel size; the replica case is inexpressible; any `--hard-exclude-class` switches off re-admission; record lacks class, role, identity | 04 §2 KT | REPRESENTED | D11 (l.598); V-075 (l.3013); V-493; V-124 |
| D-19 | `panel_cmd`: options; class names expanded through `classes`; resolver writes no file and no telemetry; `panel validate` omits tiers; no include-class, allow-repeat, role or adapter option | 04 §3 | REPRESENTED | D15 (l.602); MS-06 (l.632); BL-08; V-233 |
| D-20 | KT §3: the resolver is a pure stdout tool (persisting is the caller's job); validate and resolve disagree for `reflect-*`; `--kind` has two values | 04 §3 KT | REPRESENTED | MS-06 (l.632); BL-09 (l.612); l.151 |
| D-21 | Tier file: six aliases and their model lists; no `tier0`; `muse-ember-1.0` appears in no alias, name or class | 04 §4 | REPRESENTED | V-129 (l.3067); V-216 (l.3154); V-407 (l.3345); V-032 (l.2970) |
| D-22 | `environments.gateway` has `launch: {}` and a "not defined yet" note; `anthropic-only` has available list, stand-ins, `launch` ids, note dated 2026-11-10 | 04 §4 | REPRESENTED | V-216; MS-06 (l.632, "undated except a 2026-11-10 note"); K-10 (l.562) |
| D-23 | The 8 packaged templates and what each resolves to (default, live7, reflect-pre, -pre-x2, -post, -post-x2, -enterprise, -lite) | 04 §4 | REPRESENTED | V-005 (l.2943); V-215 (l.3153); C-04 evidence (l.1404); l.2532 |
| D-24 | Personas and lenses live only in template `description` prose; the code has no persona field | 04 §4 | REPRESENTED | BL-08 (l.611) |
| D-25 | Gateway `launch: {}` makes every gateway reviewer `launch: null`; no reflect template resolves in gateway (error text reproduced) | 04 §4.1 | REPRESENTED | l.1369; MS-06 (l.632); K-10 (l.562) |
| D-26 | In this session `select_env` picks `gateway`, so reflect must pass `--env anthropic-only`; generic gateway templates resolve but carry no dispatch instruction | 04 §4.1 | REPRESENTED | C-03 (l.1318-1383); l.1369 |
| D-27 | In anthropic-only every tier has at most one model, so `fallbacks` lists are empty | 04 §4.1 | REPRESENTED | K-10 (l.562) (corrected: only tier1a has one fallback); MS-06 (l.632) |
| D-28 | `launch` in anthropic-only is a class name; `ANTHROPIC_DEFAULT_*_MODEL` decide what serves; haiku routes to the tier2 alias whose first model is `gpt-6.1-sol`; "anthropic-only" is not true at serving time | 04 §4.1 | REPRESENTED | l.1338, l.1370; V-354 (l.3292); l.2834 |
| D-29 | `T2bModel01` is set but never read; the resolver does not check that the gateway serves the aliases a template needs; E2 used raw ids because aliases serve only a tier's first model | 04 §4.2 | REPRESENTED | D12 (l.599); V-076; V-099 (l.3037) |
| D-30 | Classes exist for every alias model; the no-Fable rule never triggers with packaged data; tier0 inert; the max-3 rule | 04 §4.3 | REPRESENTED | MS-06 (l.632); V-233; V-318 (l.3256). The "no-Fable rule never triggers with packaged data" remark is OMITTED (MINOR) |
| D-31 | KT §4: gateway plus reflect is a hard error; anthropic-only has no fallbacks and a re-routed class; `live7` duplicate reproduced; `reflect-lite` soft duplicate; strict `live7` collapses to 2 with 5 skipped slots; strict fallbacks not distinct; `--hard-exclude-class` skips; ember absent | 04 §4 KT | REPRESENTED | V-492, V-493 (l.3430-3431); C-04 (l.1404); V-215; V-407 |
| D-32 | E2 runner dispatch (`claude -p --model <raw id>`, bypassPermissions, Edit/Write/NotebookEdit denied, Bash allowed), inputs, observed identity rule (`OBS`, `MODEL_OK`, `-build`, auxiliary `modelUsage`), fallback ladder with guards, `expected_model` overwrite | 04 §5 | REPRESENTED | V-020 (l.2958); V-172, V-173, V-174 (l.3110-3112); V-185 (l.3123); V-552 (l.3490) |
| D-33 | Additional runner defects: attempt files overwritten across ladder hops, cost sums wrong, `APIERR` loop condition mismatch | 04 §5 | REPRESENTED | V-175 (l.3113); V-552; l.1787 |
| D-34 | KT §5: E2's identity is a hard observed check from a subprocess transcript, unavailable to an in-session Agent dispatch; E2 bypassed `panel resolve`; intended, served and ladder model must be three fields; runner knowledge is dated and lives in bash | 04 §5 KT | REPRESENTED | V-494 (l.3432); V-184 (l.3122) |
| D-35 | Reflect legacy rotation (§7.1): class names not model ids, fixed `reflect-reviewer` agent type, executor-class exclusion, N=2 floor, unknown executor fail-open, served model from `ANTHROPIC_DEFAULT_*`, Wave 0 step 0.5 counts distinct models | 04 §6 | REPRESENTED | V-276 (l.3214); V-138 (l.3076); V-322 (l.3260) |
| D-36 | "qwen \| kimi \| deepseek if alias available": no alias variable, no tier-file class, no launch path | 04 §6 | REPRESENTED | V-153 (l.3091); V-138 |
| D-37 | `reflect-reviewer`, `confidence-calibrator`, `evidence-validator` all carry `model: sonnet`, the default when no `model` is passed (dispatch collapse) | 04 §6 | REPRESENTED | V-254 (l.3192); V-346 (l.3284); l.1784 |
| D-38 | Shadow step 1 command, unknown executor omits exclusion, anchor exhaustion re-resolves with `@reflect-pre-x2` and `anchor_replaced`, resolution written verbatim; rule D4 unsupported cells; rule D5 `N_eff` has no code; step 3 dispatch is the legacy dispatch (resolution never drives dispatch) | 04 §6 | REPRESENTED | V-281 (l.3219); V-346; V-495 (l.3433); G-37 (l.3979) |
| D-39 | `9874d63fb` copies the pin into card `model:` and adds `model_observed:`; `recompute_parity` compares strings, refuses on `tiers_sha256` mismatch, never reads `model_observed` | 04 §6 | REPRESENTED | V-269 (l.3207); V-495; l.3475 |
| D-40 | `identity_source: observed` has no implementation; §9.2 telemetry has no served-model field; `reviewer_models` are the legacy rotation; grep evidence | 04 §6 | REPRESENTED | MS-11 (l.637); V-285 (l.3223); V-388 (l.3326) |
| D-41 | E3 telemetry `REVIEWER_GROUPS` already separate `resolved` / `launch` / `observed`, `slot` and `cost` groups; `model_scores` keys on `model_observed`; `STRATA` restriction | 04 §6 | REPRESENTED | V-004 (l.2942); V-126 (l.3064); D15 (l.602); V-496 (l.3434) |
| D-42 | KT §6: resolver is a parallel non-dispatching record; parity can pass while the served model differs; `identity_source: observed` unimplemented; telemetry is the home for the identity triple; the qwen/kimi/deepseek branch has no data | 04 §6 KT | REPRESENTED | V-495, V-499 (l.3433, 3437); V-153 |
| D-43 | Two offline ways to observe served model (E2 top-level events; E1 `extract.py` by `parent_tool_use_id`); `--forward-subagent-text` need is UNVERIFIED | 04 §7.1 | REPRESENTED | V-538 (l.3476); V-358 (l.3296); G-38 (l.3979) |
| D-44 | Combo evidence: 15 runs resolved identically; "haiku" slot served by `gpt-6.1-sol`; dispatch collapse (A3, 6 of 9 pilot runs); calibrators with no class; parity cannot see served models (E1-E3 parity True with 2 distinct models; D luna in the opus slot parity True); best panel E achieved by setting two aliases to one model | 04 §7.2 | REPRESENTED | l.166-168; l.1688; l.1784; V-347 (l.3285); V-351 (l.3289) |
| D-45 | §7.3: the harness reports an alias, not a served id, so `model_observed:` cannot reveal a swap; both E1 (pin copy) and E2 (`expected_model` rewrite) overwrite the intended field | 04 §7.3 | COVERED-BY-DEDUP | V-269 + V-173 (each half); V-495 |
| D-46 | KT §7: observed identity only from Claude Code JSON events; unified record needs `requested`, `launch`, `served`, `identity_source` plus `fallback_chain`; dispatch must pass `model` on every Agent call; redefine or retire `panel_parity` | 04 §7 KT | REPRESENTED | V-496 (l.3434); V-346; C-08 (l.1668); C-09 (l.1732) |
| D-47 | E2's best panels: valid era, final guidance (ember + 2x luna default; sonnet + 2x luna; haiku + 2x luna), surviving statistics, ceiling about 2.5/14; every recommended panel mixes vendors | 04 §8 | REPRESENTED | V-032, V-033, V-102 (l.2970, 2971, 3040); V-030. The "mixes vendors" observation is OMITTED (MINOR) |
| D-48 | Compatibility of E2 panels with the resolver (ember not expressible; haiku + 2x luna only by accident; sonnet + 2x luna no form; repeats only via soft re-admission) | 04 §8 | REPRESENTED | C-04 Option A cons (l.1404); V-497 (l.3435); V-032 |
| D-49 | KT §8: second luna is a deliberate repeat; distinctness as per-consumer policy (`none \| model \| class` plus replicas); tier lists contradict E2's dated evidence; reflect max-3 fits E2's panels | 04 §8 KT | REPRESENTED | V-497; V-143 (l.3081); V-130 (l.3068); V-318 |
| D-50 | §9 roles, lenses, kinds: where each lives; E3 loop prompt DOES call the resolver (corrects scope 02 D14); lens is a finding-contract concept; agent type per consumer; PR and rf-qa gap; `kind` vs a separate consumer axis | 04 §9 | REPRESENTED | D14 (l.601); BL-08, BL-09 (l.611-612); V-545 (l.3483); V-498 (l.3436) |
| D-51 | §10 design inputs 1-9 (keep pure resolver, declared distinctness, fallbacks as chain, environments describe dispatch, identity triple, enforced pin, role/lens/agent plus consumer axis, dated tier data, `panel validate` runs profile rules) | 04 §10 | REPRESENTED | V-499 (l.3437); C-03, C-04, C-08, C-09 (l.1318-1795); 7.1.3 (l.2760); V-281 |
| D-52 | Gaps 1-14 (qwen/kimi/deepseek branch; observed adapter; `model_observed` consumer; `tier0`; rule D5; `--forward-subagent-text`; gateway routing is runtime; E2 cost under fallback; APIERR frequency; sonnet-alone 2/16 UNVERIFIED; `manifest.md:11`; distinctness correctness-vs-knob question; `kind` verify-only; scope 02 D14 incomplete) | 04 Gaps | REPRESENTED | G-34 to G-38 (l.3979); V-153; MS-11; V-349; V-345 (l.3283); C-04 (l.1384); BL-09; D14 |
| D-53 | Stale docs: hand-off D11/D12/`§5.2`/`§5.3` line moves, gateway note, `live7` description hides a duplicate, `SKILL.md:655`, `PLAN.md` header "not run", scope 02 §4.2 now verified, CR:292 "Four" | 04 Stale | REPRESENTED | DOC rows (l.660-690), incl. DOC-26 (l.687) and the live7 row (l.684); V-640 |
| D-54 | Summary: pure sha256-frozen resolver shared in form not practice; D11 reproduced; gateway `launch: {}`; identity pinned not observed; unified resolver needs declared policy, launch adapters, enforced pin, identity triple, optional role/lens/agent, dated tiers | 04 Summary | REPRESENTED | V-499; MS-06 (l.632) |

## Enumeration: `synthesis/synth-01-problem-current-state.md`

Synth-01 is the source of report Sections 1 and 2. The enumeration is by block; each block was matched to the report text by phrase search (all 40 sub-headings and bold lead-ins of synth-01 are present) and the changes the QA gates made (corrected counts, the parsed-sparse recount, the Section 4 re-rating wording) were checked as corrections, not omissions.

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| S-01 | Citation key (R01-R13, S00-S05, GQ, BR, git-show form), effort tags E1/E2/E3/ext, verification tags, dated-evidence caveat | synth-01 header | REPRESENTED | l.107-126 (key extended with CR, PR, AD, HO, MR) |
| S-02 | Problem statement: three efforts to compare, one unified design serving reflect, workflow tasklist review, spec review, later PR review and rf-qa replacement | synth-01 §1 | REPRESENTED | l.92 |
| S-03 | Why it matters: identity in three places, shape in two, merge in two plus the code-driven third path; one in-repo caller of the #346 CLI; each effort measured a third of a run; E2 ceiling and 49 lost findings; Stage 2 exit FAIL; no valid-success variant verdict; 94 open gaps | synth-01 §1 | REPRESENTED | l.93-100 (the last bullet re-worded by the report-validation gate: 15 rows re-rated Critical = 11 distinct gaps plus 4 restatements) |
| S-04 | Trigger: owner scope (all value, overlap, conflicts, future use cases); report-only change of 2026-11-13; later merge through `/sc:adversarial --compare --merge`; `feat/review-panel` branch constraint; E2 at one commit | synth-01 §1 | REPRESENTED | l.101 |
| S-05 | E1: kernel already on `origin/master` (`d2d8a2d16`); branch three commits ahead; two skill-fix commits touch four files | synth-01 §2.1 | REPRESENTED | l.132 |
| S-06 | E1 key-files table: findings-v2, card converter, clustering, citation pre-check, manifest, resolver extensions, contract lint, replay and exit scripts, reflect protocol and agents, wrapper | synth-01 §2.1 | REPRESENTED | l.136-146 |
| S-07 | E1 authoritative legacy path (rotation, briefs, per-card calibrator, Mode A merge, evidence validator, 1.8.0 contract, wrapper degrade rules) | synth-01 §2.1 | REPRESENTED | l.149 |
| S-08 | E1 shadow mode: ten steps, prose recipe, changes no verdict | synth-01 §2.1 | REPRESENTED | l.151 |
| S-09 | E1 measurements table (conversion share, pair quality, per-finding calibration legacy vs shadow, Stage 2 exit, `cluster_agreement`, Tier 2 typical path with the recount, H-A unmeasured) | synth-01 §2.1 | REPRESENTED | l.155-165 (l.161-163) |
| S-10 | Identity and dispatch: spike S-ID, `identity_source: observed` unimplemented, `model_observed:` unread, collapse to Sonnet, gateway `launch: {}` | synth-01 §2.1 | REPRESENTED | l.166 |
| S-11 | 5x3 model-combination experiment (leads, no quality answer, GLM/Qwen orchestrator, stale `combos.json`, `base-e8db2fe6` folder, per-run cost only in `extract.py`) | synth-01 §2.1 | REPRESENTED | l.168 |
| S-12 | Defects and constraints: contract 1.8.0 frozen, EV-1 self-attested, calibrator 6-dimension vs claimed 5, drift halts vs MINOR-never-blocks, `unauthorized_deviation_present` no producer rule, pins C1/C6/C14 HEAD-relative | synth-01 §2.1 | REPRESENTED | l.170 |
| S-13 | E1 evidence line | synth-01 §2.1 | REPRESENTED | l.172 |
| S-14 | E2: harness not product code; ~106 runs, 62 sets, 3 packages, 16 known defects; first reviews only | synth-01 §2.2 | REPRESENTED | l.176 |
| S-15 | E2 key-files table (runner, judge, aggregation, audits, ground truth, helper scripts, reports) | synth-01 §2.2 | REPRESENTED | l.180-190 |
| S-16 | E2 reported results table (ceiling, never found with the GT1 correction, default panel, surviving statistics, 65 vs 38, source-blind 156 of 665, 49 lost and 3 flips, chaining) | synth-01 §2.2 | REPRESENTED | l.193-201 |
| S-17 | E2 model-by-role observations | synth-01 §2.2 | REPRESENTED | l.203 |
| S-18 | E2 strategies that worked and failed | synth-01 §2.2 | REPRESENTED | l.205 |
| S-19 | E2 harness defects (expected_model overwrite, cost glob, BLOCK_OK, Bash not denied, judge sees panel name, silent drop, audit filter, `three-way.py:4`, hard-coded paths; D11 duplicates contradict the hand-off) | synth-01 §2.2 | REPRESENTED | l.207 |
| S-20 | Product-code defects E2 reported, with the corrected line numbers | synth-01 §2.2 | REPRESENTED | l.209 |
| S-21 | E2 data-flow diagram (reviewer output to scored result) | synth-01 §2.2 | REPRESENTED | l.211 ("Today's data flow of the E2 harness") with its diagram |
| S-22 | Open E2 decisions (seven) | synth-01 §2.2 | REPRESENTED | l.235 |
| S-23 | E3: what it is, master components table, how the loop runs, ledger behaviour at current lines, installed-only variants table (ledger, stoprule, diffgate, ponytail/fix-audit, armb), experiment outcomes and caveat, constraints on plugging in | synth-01 §2.3 | REPRESENTED | l.241-276 (l.256, l.258, l.264-272, l.274) |
| S-24 | Shared CLI package: shape, module table, stack A and stack B data flows, divergence table, D1-D16 table, test surface | synth-01 §2.4 | REPRESENTED | l.278-384 (l.292, l.320, l.342, l.357, l.380) |
| S-25 | Consumers today: flow diagram, consumer table, third merge path (`ensemble.py`) with property table, callers of the review CLI, known gaps in the PR and rf-qa consumers | synth-01 §2.5 | REPRESENTED | l.384-434 (l.413, l.429, l.431) |
| S-26 | Component overlap matrix (18 rows), "Reading the matrix", contradictions table (11 rows), "Excluded or routed elsewhere" coverage note | synth-01 §2.6 | REPRESENTED | l.435-480 (l.460, l.462, l.478) |
| S-27 | Header lines: task id, "report sections 1 and 2", owner scope (2026-11-13: report only, no `/sc:workflow`, no roadmap, merge with the other session's second report) | synth-01 header | REPRESENTED | l.101; Section 8 preamble (l.2917) |

## Enumeration: `research/scope/00-handoff-copy.md` (the hand-off copy)

Section 8.1 (value inventory) was checked row by row against the hand-off. A hand-off item counts as represented when it has a V-row with a destination or a DROP reason, or its substance appears elsewhere. V-row line numbers: V-001 is l.2939 and the rows run one per line, so V-n is at line 2938+n.

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| H-01 | Header: date, branch `ironbelly/eval-tasklist-review-panel`, last study commits `b4db265a8` and `2d06a4382`, hand-off commit | hand-off l.3 | OMITTED | the two study commit hashes appear nowhere (the report cites only the E2 commit `4a22d742...`); MINOR provenance metadata |
| H-02 | Reader assumption (no session context) and abbreviation table (EVAL, CR, PR, SPEC, RV) | hand-off l.4-5 | REPRESENTED | citation key l.115-118; V-table abbreviations (l.2925-2933) |
| H-03 | Method note: not produced through the task-file machinery, three read-only investigation agents, nothing cross-checked by a QA pass | hand-off l.6 | COVERED-BY-DEDUP | V-164 (l.3102) (hand-off not run through a QA fleet; claims re-checked in scope/01 and scope/02) |
| H-04 | One-paragraph summary (106 runs, 62 sets, 2-2.5 of 14, no panel better except cost, 4 of 16 never found, levers are harness and product defects, no product code changed) | hand-off §0 | REPRESENTED | V-030, V-031, V-060, V-064 (l.2968-2969, 2998, 3002); l.176 |
| H-05 | Inventory 1.1: `findings.py` (457 lines) | hand-off §1.1 | REPRESENTED | V-001 |
| H-06 | `merge_cmd.py`, `ledger.py`, `ledger_cmd.py` | hand-off §1.1 | REPRESENTED | V-002 |
| H-07 | `panel.py`, `panel_cmd.py` | hand-off §1.1 | REPRESENTED | V-003 |
| H-08 | `telemetry.py`, `telemetry_cmd.py` | hand-off §1.1 | REPRESENTED | V-004 |
| H-09 | Packaged data (`review-panel.default/live7.json`, `review-tiers.default.json`), model ids time-bound | hand-off §1.1 | REPRESENTED | V-005 |
| H-10 | `document_review_loop_prompts.md` (the only reviewer brief in `src`) | hand-off §1.1 | REPRESENTED | V-006 |
| H-11 | Tests: 111 functions plus 5 skill test files | hand-off §1.1 | REPRESENTED | V-007 (count corrected to 651/1182) |
| H-12 | `PILOT-REPORT.md` | hand-off §1.2 | REPRESENTED | V-008 |
| H-13 | `COMBO-REPORT.md` (only lines 289-373, 385-419, 421-428, 430+ current) | hand-off §1.2 | REPRESENTED | V-009 |
| H-14 | `combos/SPEC.md` | hand-off §1.2 | REPRESENTED | V-010 |
| H-15 | `manifest.md` | hand-off §1.2 | REPRESENTED | V-011 |
| H-16 | `analysis/audits/audit-A..F/` | hand-off §1.2 | REPRESENTED | V-012 |
| H-17 | `analysis/issue-table/`, `analysis/allsets/` | hand-off §1.2 | REPRESENTED | V-013 |
| H-18 | `analysis/*.py` (`final-table.py`, `three-way.py`, `doubles.py`, `untried.py`), `merge-b7..b11.sh`, `b7..b11-launch.sh`, judge tsv and logs | hand-off §1.2 | REPRESENTED | V-014, V-015, V-016, V-022, V-023 |
| H-19 | `analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md` | hand-off §1.2 | REPRESENTED | V-017 |
| H-20 | Per-package `reviews/`, `combos/<row>/`, `arms/scoring/**/score.json` | hand-off §1.2 | REPRESENTED | V-018 |
| H-21 | `<pkg>/ground-truth.json`, `candidate.md`, `resolution-*.json` | hand-off §1.2 | REPRESENTED | V-019 |
| H-22 | `tools/run-reviewer.sh` (old copies `.bad-launch`, `.unpassable-ac`) | hand-off §1.3 | REPRESENTED | V-020; the old copies appear at V-074 |
| H-23 | `tools/tmp-scripts/` (54 scripts plus README, 220 KB) | hand-off §1.3 | REPRESENTED | V-021, V-022, V-023 |
| H-24 | `analysis/*.py` aggregation scripts mostly study specific | hand-off §1.3 | REPRESENTED | V-014, V-015 |
| H-25 | `/tmp` held 70 `.sh`; scripts not copied (`checks-gate8.sh`, `r2terra-hb.sh`, ...); `checks-gate8` named as part of the study | hand-off §1.3 | REPRESENTED | V-024 |
| H-26 | Left out by owner order: 3,041 untracked files, 1.48 GB, final `meta.json`/`cost.json` committed | hand-off §1.4 | REPRESENTED | V-017; V-105; V-112 |
| H-27 | Study design: 3 packages (10/5, 4/3, control 2/0), ground truth from past `/sc:implement` runs | hand-off §2.1 | REPRESENTED | V-025 |
| H-28 | Unit of run, blind Opus judge, anonymisation, `score.json` fields | hand-off §2.1 | REPRESENTED | V-026 |
| H-29 | Metrics: found /14, real blocking /8, wrong blockers (structural bias) | hand-off §2.1 | REPRESENTED | V-027 |
| H-30 | Eras: `source.md` first shipped 2026-11-12 12:59:34; pre-source data invalid | hand-off §2.1 | REPRESENTED | V-028; V-100 |
| H-31 | Scale: 71 rows, 213 row-packages, 62 sets, 106 runs | hand-off §2.1 | REPRESENTED | V-029 |
| H-32 | R1: every panel 1.6-2.5 of 14, no significant difference except cost | hand-off §2.2 | REPRESENTED | V-030 |
| H-33 | R2: four of 16 never found; B3, I2, I8 carry catches | hand-off §2.2 | REPRESENTED | V-031 (with the GT1 correction) |
| H-34 | R3: default recommendation ember + 2x luna; quality tier; best real blocking | hand-off §2.2 | REPRESENTED | V-032; V-102 |
| H-35 | R4: surviving statistics and the retracted "adds nothing" | hand-off §2.2 | REPRESENTED | V-033; V-051 |
| H-36 | R5: pilot arms 2/16, 3/16, 4/16; sonnet alone passed | hand-off §2.2 | REPRESENTED | V-034 |
| H-37 | R6: single-run high scores never replicated | hand-off §2.2 | REPRESENTED | V-035 (DROP with reason) |
| H-38 | Model: claude-sonnet-5-5 | hand-off §2.3 | REPRESENTED | V-036 |
| H-39 | Model: gpt-6-luna | hand-off §2.3 | REPRESENTED | V-037 |
| H-40 | Model: muse-ember-1.0 | hand-off §2.3 | REPRESENTED | V-038 |
| H-41 | Model: claude-haiku-5-5 | hand-off §2.3 | REPRESENTED | V-039 |
| H-42 | Model: grok-4.7 | hand-off §2.3 | REPRESENTED | V-040 |
| H-43 | Model: gpt-6.1-terra / sol | hand-off §2.3 | REPRESENTED | V-041 |
| H-44 | Model: glm-5.3 | hand-off §2.3 | REPRESENTED | V-042 |
| H-45 | Model: Qwen3.8-max | hand-off §2.3 | REPRESENTED | V-043 |
| H-46 | Model: muse-wonder-1.0 | hand-off §2.3 | REPRESENTED | V-044 |
| H-47 | Models never run in the valid era (spark, wonder-full, opus) | hand-off §2.3 | REPRESENTED | V-045 (DROP with reason) |
| H-48 | D1 over-length findings dropped; surfacing; 49 lost | hand-off §2.4 | REPRESENTED | D1 (l.588); V-065 |
| H-49 | D2 dropped re-report clears a blocking row | hand-off §2.4 | REPRESENTED | D2 (l.589); V-066 |
| H-50 | D3 merge passes with one valid reviewer | hand-off §2.4 | REPRESENTED | D3 (l.590); V-067 |
| H-51 | D4 one reviewer's blocking flag decides | hand-off §2.4 | REPRESENTED | D4 (l.591); V-068 |
| H-52 | D5 missing anchors kept silently | hand-off §2.4 | REPRESENTED | D5 (l.592); V-069 |
| H-53 | D6 clustering over- and under-merges | hand-off §2.4 | REPRESENTED | D6 (l.593); V-070 |
| H-54 | D7 reference-id regex misses tasklist ids | hand-off §2.4 | REPRESENTED | D7 (l.594); V-071 |
| H-55 | D8 reviewer brief never names the source | hand-off §2.4 | REPRESENTED | D8 (l.595); V-072 |
| H-56 | D9 `missing-requirement` Medium vs schema | hand-off §2.4 | REPRESENTED | D9 (l.596); V-073 |
| H-57 | D10 `unpassable-ac` rejected | hand-off §2.4 | REPRESENTED | D10 (l.597); V-074 |
| H-58 | D11 `distinct_across_slots` silent duplicates | hand-off §2.4 | REPRESENTED | D11 (l.598); V-075 |
| H-59 | D12 environment select keys on `$T3Model01` | hand-off §2.4 | REPRESENTED | D12 (l.599); V-076 |
| H-60 | D13 `lint_cmd` / `estimate_cmd` missing | hand-off §2.4 | REPRESENTED | D13 (l.600); V-077 |
| H-61 | D14 no tasklist review step; experiment copies | hand-off §2.4 | REPRESENTED | D14 (l.601); V-078 |
| H-62 | D15 telemetry strata only sonnet/haiku | hand-off §2.4 | REPRESENTED | D15 (l.602); V-079 |
| H-63 | D16 round 4 accepted; `--cap` ignored; verify-only prompt-only | hand-off §2.4 | REPRESENTED | D16 (l.603); V-080 |
| H-64 | Note on D1 precision (one warning with the first error, not "no error") | hand-off §2.4 | REPRESENTED | D1 (l.588, "warns with the error count and only `errors[0]`"); l.1259 |
| H-65 | Harness incident: blocking-count parser without space | hand-off §2.5 | REPRESENTED | V-046 (DROP) |
| H-66 | Cyclic fallback ladder incident | hand-off §2.5 | REPRESENTED | V-047 |
| H-67 | 12 concurrent workers, gateway identity bleed | hand-off §2.5 | REPRESENTED | V-048 |
| H-68 | `claude` binary replaced mid-run | hand-off §2.5 | REPRESENTED | V-049 |
| H-69 | Batch 10 dropped; interrupted quarantine | hand-off §2.5 | REPRESENTED | V-050 (DROP) |
| H-70 | `attrib.py` credited every member | hand-off §2.5 | REPRESENTED | V-051 (DROP); V-089 |
| H-71 | Judge "blocking" mixes definitions (65 vs 38) | hand-off §2.5 | REPRESENTED | V-052 |
| H-72 | Merge silently drops over-length findings; stale merges | hand-off §2.5 | REPRESENTED | V-053 |
| H-73 | Audit A identity | hand-off §2.6 | REPRESENTED | V-054 |
| H-74 | Audit B report validity (51 incomplete) | hand-off §2.6 | REPRESENTED | V-055 (DROP with reason) |
| H-75 | Audit C inputs and timing | hand-off §2.6 | REPRESENTED | V-056 |
| H-76 | Audit D merges | hand-off §2.6 | REPRESENTED | V-057 |
| H-77 | Audit E scoring integrity (12/12 re-judge) | hand-off §2.6 | REPRESENTED | V-058 |
| H-78 | Audit F aggregation; audits were read-only by the same session, one judge per row-package | hand-off §2.6 | REPRESENTED | V-059 |
| H-79 | Not shown: no panel better or worse on quality | hand-off §2.7 | REPRESENTED | V-060 |
| H-80 | Not shown: rounds 2-3, reviser, loop verdict | hand-off §2.7 | REPRESENTED | V-061 |
| H-81 | Not shown: other repositories or plans | hand-off §2.7 | REPRESENTED | V-062 |
| H-82 | Not shown: ground truth counts only blocking-in-implement defects; novel finds count as wrong blockers | hand-off §2.7 | REPRESENTED | V-063 |
| H-83 | Not shown: D1 and D8 distort every number | hand-off §2.7 | REPRESENTED | V-064 |
| H-84 | Lesson (worked) 1: blind scoring, anonymised reports, re-judge | hand-off §3 | REPRESENTED | V-081 |
| H-85 | Lesson (worked) 2: ground truth from real failures | hand-off §3 | REPRESENTED | V-082 |
| H-86 | Lesson (worked) 3: six integrity audits | hand-off §3 | REPRESENTED | V-083 |
| H-87 | Lesson (worked) 4: replicates and permutation tests | hand-off §3 | REPRESENTED | V-084 |
| H-88 | Lesson (worked) 5: model-identity check, quarantine-not-delete | hand-off §3 | REPRESENTED | V-085 |
| H-89 | Lesson (worked) 6: `NOFALLBACK=1`, cancel files | hand-off §3 | REPRESENTED | V-086 |
| H-90 | Lesson (worked) 7: agents plus direct script cell by cell | hand-off §3 | REPRESENTED | V-087 |
| H-91 | Lesson (failed) 1: single-run judgement | hand-off §3 | REPRESENTED | V-088 |
| H-92 | Lesson (failed) 2: attribution of a merged row to every member | hand-off §3 | REPRESENTED | V-089 |
| H-93 | Lesson (failed) 3: judge `gt_covered_blocking` as real blocking | hand-off §3 | REPRESENTED | V-090 |
| H-94 | Lesson (failed) 4: many workers on the gateway; long sleep chains | hand-off §3 | REPRESENTED | V-091 |
| H-95 | Lesson (failed) 5: grepping JSON, binary self-update, cyclic ladder | hand-off §3 | REPRESENTED | V-092 |
| H-96 | Lesson (failed) 6: not shipping `source.md` at the start | hand-off §3 | REPRESENTED | V-093 |
| H-97 | Do differently 1: fix D1 and D8, re-run one replicated comparison | hand-off §3 | REPRESENTED | V-094 |
| H-98 | Do differently 2: dropped-findings counter in merge output | hand-off §3 | REPRESENTED | V-095 |
| H-99 | Do differently 3: one canonical scoring script in the repo | hand-off §3 | REPRESENTED | V-096 |
| H-100 | Do differently 4: pre-register the decision rule | hand-off §3 | REPRESENTED | V-097 |
| H-101 | Decision: Qwen3.8-max excluded everywhere | hand-off §4.1 | REPRESENTED | V-098 |
| H-102 | Decision: raw gateway model ids, not tier aliases | hand-off §4.1 | REPRESENTED | V-099 |
| H-103 | Decision: valid era starts when `source.md` shipped | hand-off §4.1 | REPRESENTED | V-100 |
| H-104 | Decision: batch 10 dropped; testing closed | hand-off §4.1 | REPRESENTED | V-101 (DROP) |
| H-105 | Decision: default panel, quality tier, best real-blocking, panels to avoid | hand-off §4.1 | REPRESENTED | V-102 |
| H-106 | Decision: "decision update" (sonnet + 2x luna standard) rejected | hand-off §4.1 | REPRESENTED | V-103 (DROP) |
| H-107 | Decision: no PR, push the research branch only | hand-off §4.1 | REPRESENTED | V-104 (DROP) |
| H-108 | Decision: raw transcripts left out | hand-off §4.1 | REPRESENTED | V-105 (DROP) |
| H-109 | Decision: never stage `.claude/`, change nothing under `.dev/tasks/` | hand-off §4.1 | REPRESENTED | V-106 (DROP; standing rule) |
| H-110 | Open decision 1: fix D1 | hand-off §4.2 | REPRESENTED | V-107 |
| H-111 | Open decision 2: fix D8 | hand-off §4.2 | REPRESENTED | V-108 |
| H-112 | Open decision 3: default model set; time-bound config or code | hand-off §4.2 | REPRESENTED | V-109 |
| H-113 | Open decision 4: tasklist review inside `/sc:workflow` or separate command | hand-off §4.2 | REPRESENTED | V-110 |
| H-114 | Open decision 5: one reviewer's flag vs quorum or calibrated rule | hand-off §4.2 | REPRESENTED | V-111 |
| H-115 | Open decision 6: commit raw transcripts | hand-off §4.2 | REPRESENTED | V-112 (DROP) |
| H-116 | Open decision 7: re-run the comparison after D1 and D8 | hand-off §4.2 | REPRESENTED | V-113 |
| H-117 | Role: Reviewer | hand-off §5.1 | REPRESENTED | V-114 |
| H-118 | Role: Merge / "judge" in product | hand-off §5.1 | REPRESENTED | V-115 |
| H-119 | Role: Calibrator | hand-off §5.1 | REPRESENTED | V-116 |
| H-120 | Role: Orchestrator | hand-off §5.1 | REPRESENTED | V-117 |
| H-121 | Role: Reviser | hand-off §5.1 | REPRESENTED | V-118 |
| H-122 | Role: Human (`ledger defer`) | hand-off §5.1 | REPRESENTED | V-119 |
| H-123 | Role: Eval judge | hand-off §5.1 | REPRESENTED | V-120 |
| H-124 | Contract findings-v1 | hand-off §5.2 | REPRESENTED | V-121 |
| H-125 | Contract fixmap-v1 | hand-off §5.2 | REPRESENTED | V-122 |
| H-126 | Contract review-ledger/1 | hand-off §5.2 | REPRESENTED | V-123 |
| H-127 | Contract review-panel-resolution/1 | hand-off §5.2 | REPRESENTED | V-124 |
| H-128 | Contract review-capture/1 | hand-off §5.2 | REPRESENTED | V-125 |
| H-129 | Contract review-telemetry/1 | hand-off §5.2 | REPRESENTED | V-126 |
| H-130 | Merged report format | hand-off §5.2 | REPRESENTED | V-127 |
| H-131 | Severity semantics (blocking by grading sentence; `spec-panel.md:259`) | hand-off §5.2 | REPRESENTED | V-128 |
| H-132 | Tier configuration (tier table, environments, packaged panels, re-review anchor) | hand-off §5.3 | REPRESENTED | V-129 |
| H-133 | What the study found about the configuration (unusable models listed, useful ones missing; no result validates `@default` or `@live7`) | hand-off §5.3 | REPRESENTED | V-130 |
| H-134 | How results are recorded in the study | hand-off §5.4 | REPRESENTED | V-131 |
| H-135 | Tasklist-specific vs target-agnostic | hand-off §5.5 | REPRESENTED | V-132 |
| H-136 | Contrast: reviewers | hand-off §5.6 | REPRESENTED | V-133 |
| H-137 | Contrast: input | hand-off §5.6 | REPRESENTED | V-134 |
| H-138 | Contrast: output | hand-off §5.6 | REPRESENTED | V-135 |
| H-139 | Contrast: calibration | hand-off §5.6 | REPRESENTED | V-136 |
| H-140 | Contrast: merge | hand-off §5.6 | REPRESENTED | V-137 |
| H-141 | Contrast: config | hand-off §5.6 | REPRESENTED | V-138 |
| H-142 | Must meet 1: accept both finding shapes or map | hand-off §6 | REPRESENTED | V-139 |
| H-143 | Must meet 2: no silent loss | hand-off §6 | REPRESENTED | V-140 |
| H-144 | Must meet 3: reviewer input includes the driving document | hand-off §6 | REPRESENTED | V-141 |
| H-145 | Must meet 4: a defined blocking rule and a real-blocking metric | hand-off §6 | REPRESENTED | V-142 |
| H-146 | Must meet 5: evidence-based model resolution with enforced identity | hand-off §6 | REPRESENTED | V-143 |
| H-147 | Must meet 6: cost and time recording by default | hand-off §6 | REPRESENTED | V-144 |
| H-148 | Must meet 7: re-review semantics preserved | hand-off §6 | REPRESENTED | V-145 |
| H-149 | Must meet 8: a runnable regression suite | hand-off §6 | REPRESENTED | V-146 |
| H-150 | Must meet 9: reviewer isolation | hand-off §6 | REPRESENTED | V-147 |
| H-151 | Must meet 10: a place for tasklist review in the workflow and tasklist skills | hand-off §6 | REPRESENTED | V-148 |
| H-152 | Question 1: does workflow or tasklist invoke any panel outside `src` | hand-off §7 | REPRESENTED | V-149 |
| H-153 | Question 2: which finding format; mapping of reflect categories | hand-off §7 | REPRESENTED | V-150 |
| H-154 | Question 3: does the calibrator apply to anchors; class disjointness vs `distinct_across_slots` | hand-off §7 | REPRESENTED | V-151 |
| H-155 | Question 4: what reflect gives reviewers for the driving spec | hand-off §7 | REPRESENTED | V-152 |
| H-156 | Question 5: is the reflect rotation table valid given Qwen was disqualified | hand-off §7 | REPRESENTED | V-153 |
| H-157 | Question 6: who owns the model and tier lists | hand-off §7 | REPRESENTED | V-154 |
| H-158 | Question 7: where the stoprule/ledger experiment stands | hand-off §7 | REPRESENTED | V-155 |
| H-159 | Merge risk: findings drops on the reflect side | hand-off §7 | REPRESENTED | V-156 |
| H-160 | Merge risk: different notions of "blocking" | hand-off §7 | REPRESENTED | V-157 |
| H-161 | Merge risk: `@live7` time-bound model lists | hand-off §7 | REPRESENTED | V-158 |
| H-162 | Merge risk: numbers depressed by D1 and D8 | hand-off §7 | REPRESENTED | V-159 |
| H-163 | Merge risk: ground truth from 3 packages in one repository | hand-off §7 | REPRESENTED | V-160 |
| H-164 | Merge risk: untracked raw data | hand-off §7 | REPRESENTED | V-161 (DROP) |
| H-165 | Test status: 299 passed; covered limits, `@live7`, ledger rounds 1-3 | hand-off §8 | REPRESENTED | V-162 |
| H-166 | Test status: NOT covered list | hand-off §8 | REPRESENTED | V-163 |
| H-167 | Study verification (six audits, cross-checked cells, 12/12 re-judge) and "not verified here" | hand-off §8 | REPRESENTED | V-164 |
| H-168 | "Where to start" reading order (report, `CR:289-373`, audit D and C summaries, `findings.py:90-121`, `ledger.py:107-298`, `run-reviewer.sh:13-17`, `judge-one.sh`, `SPEC.md`) | hand-off §9 | OMITTED | navigation guidance; no V-row (MINOR) |
| H-169 | Evidence trail: files read in the hand-off session, including the investigation notes `/tmp/handoff-notes/code-merge.md`, `code-panel.md`, `tests-tools.md` | hand-off §9 | OMITTED | provenance only; the three notes exist only in `/tmp` of the author's machine and have no row (MINOR) |

---

### Omissions Found

Rating rule used: CRITICAL = a distinct foundational finding or discipline dropped; IMPORTANT = a distinct secondary finding dropped that a report decision or claim depends on; MINOR = a micro-detail or a detail already implied by a carried statement. The report's design recommendations (one clusterer on the v2 location model with complete-link admission and a per-lens id grammar, a code-rendered brief generated from the contract constants, truncate-prefix with a counter, a lens registry, a run manifest with built-in audits) replace or fix every mechanism whose current-state detail was dropped below, so no recommendation depends on a dropped fact.

| # | Source finding | Source file | Status (OMITTED / COVERED-BY-DEDUP) | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| A-10 | `parse_fixmap` falls back to scraping `\| id \| applied` table rows (a lenient path the findings block lacks) | 01 §1.4 | OMITTED | n/a | MINOR |
| A-13 | Two hallucinated (missing) anchors with equal refs share a fingerprint and `same_defect` clusters them | 01 §1.4 | OMITTED | n/a | MINOR |
| A-18 | v2 checks `claim` length before the anchor (v1 checks it last) | 01 §2.2 | OMITTED | n/a | MINOR |
| A-35 | card_convert produces only roles `plan`/`spec`/`source` (never `test`/`diff`/`artifact`) and emits no quote or anchor | 01 §3.3 | OMITTED | n/a | MINOR |
| A-36 | role `unresolved` is not in `ROLES`, so such lines are not valid v2 but stay in `findings` and `problems` | 01 §3.3 | OMITTED | n/a | MINOR |
| A-38 | card_convert category derivation: `risk` to `safety` via `_SAFETY`, first mapped v1 category for a reflect category, v2-19 always holds for converted lines | 01 §3.4 | OMITTED | n/a | MINOR |
| A-40 | Converted lines carry no `lens`, so v2-15 never fires and a converted UC-2 card is not checked as `reflect-post` | 01 §3.4 | OMITTED | n/a | MINOR (the converter is telemetry-only and the report retires its blocking mapping, V-296, V-471; strongest A-file candidate for IMPORTANT, rated MINOR because no decision rests on it) |
| A-41 | card_convert ids: `_new_id` falls back to `F<index>`; `seen.add` runs for unconverted lines too | 01 §3.4 | OMITTED | n/a | MINOR |
| A-42 | card_convert: an entry with no claim key yields an empty claim that passes v2-7 and converts | 01 §3.4 | OMITTED | n/a | MINOR |
| A-61 | The shadow brief's example is MAJOR + `blocking:false` with no `reflect_category` (never exercises the label rule) and the brief does not ask for `reflect_category`, `channel`, `coverage_rows` or `self_confidence`, so those v2 fields are unreachable from shadow reviewers | 01 §7 | OMITTED | n/a | MINOR (the report replaces the brief by a code-rendered one generated from the contract constants, C-10; flagged because it limits what the shadow data can show) |
| A-79 | Experiment-ledger row fields (`R<N>`, label, `round_found`, `at`, `at_snapshot`, origin, scope, `caused_by`, status, mappings, claims, history) and the absence of category, refs, fingerprint and reviewer identity | 01 §10.2 | OMITTED | n/a | MINOR |
| B-03 | Duplicate reviewer id check in `merge_round` (`ledger.py:119-121`) | 02 §1.2 | OMITTED | n/a | MINOR |
| B-06 | Row match: a cluster joins the FIRST existing row for which any member is `same_defect` | 02 §1.2 | OMITTED | n/a | MINOR |
| B-13 | `verdict()` returns the stored verdict and never recomputes (which is why `defer` has to rewrite it) | 02 §1.3 | OMITTED | n/a | MINOR (V-119 already asks for one shared `decide()`) |
| B-15 | `apply_revision` refuses an `--old` text whose sha256 differs from the reviewed round; reports `named_not_touched` and `rejected_by_reviser` | 02 §1.3 | OMITTED | n/a | MINOR |
| B-25 | `merge_round` mutates ledger rows in place before the round record is appended (disk-safe, memory-unsafe) | 02 §1.4 | OMITTED | n/a | MINOR |
| B-27 | `render_merged_report` would print "review: 4 of 3" at round 4 with cap 3 (inference, not run) | 02 §1.4 | OMITTED | n/a | MINOR |
| B-35 | `test_a_late_nonblocking_cluster_cannot_mask_a_blocking_one` (`test_review_ledger.py:547-566`) is a correct invariant to keep | 02 §3 | OMITTED | n/a | MINOR |
| B-58 | Experiment-ledger and stoprule mechanics beyond the carried invariants: `FROZEN_FIELDS`, `E-ILLEGAL`/`E-INCOMPLETE`, new-row scope `in`/`outside` with `caused_by`, lock file and `--dry-run`, `decide()` with `U`, sweep `would_block`/`challenges`, `EXIT_REPAIR` and claim-status order | 02 §6.1/§7.1 | OMITTED | n/a | MINOR (the verified invariants are carried at l.264-265 and V-417/V-419) |
| C-02 | `_SECTION_REF`: bare section numbers count only as a whole entry of `refs`, never from prose | 03 §1.1 | OMITTED | n/a | MINOR |
| C-07 | Mixed-ref asymmetry: a finding with refs and one without never merge, even on the same line (`findings.py:374`, `cluster.py:167-169`); a reviewer who writes ids and one who does not are never clustered | 03 §5.3 | OMITTED | n/a | MINOR (strongest C-file candidate for IMPORTANT: it is the only concrete under-merge mechanism, and D6 names "under-merges" without it; rated MINOR because l.1933 states the rule it follows from and the recommended clusterer replaces the rule; the gate owner may promote it) |
| C-11 | `fp` is not recomputed when spans move across versions, so a renumbered heading changes the next round's fp and re-match then rests on the span rule alone | 03 §1.8 | OMITTED | n/a | MINOR |
| C-17 | `_members` skips findings with no string id or a duplicate id; calibration is accepted only as a finite number in [0,1], not a bool | 03 §2.2 | OMITTED | n/a | MINOR |
| C-19 | The per-lens primary-role choice (`PRIMARY_ROLES`) is inert on the CLI path: `cluster_cmd` calls `parse_block` with no lens and `annotate` reads a per-line `lens`, so the first citation is always primary | 03 §2.3 | OMITTED | n/a | MINOR (the report cites `PRIMARY_ROLES` as a registry precedent at l.627, l.2644, l.2765 and M1-04 adds a `--lens-dir`/lens input to `review cluster`; the current-state fact is not stated) |
| C-37 | Replay per-run table: heavy merging in some runs (27 findings to 7 clusters, 22 to 8) and all-singleton runs with no resolved citations | 03 §6.1 | OMITTED | n/a | MINOR (totals are carried at V-329) |
| D-05 | Template schema limits: exactly one `fixed` slot, `count` 1..4, total 1..8, `seed` only with `random`, slot-id regex, tier-name regex (`tier0` syntactically legal) | 04 §1 | OMITTED | n/a | MINOR |
| H-01 | Hand-off header: date, branch, last study commits `b4db265a8` and `2d06a4382` | hand-off l.3 | OMITTED | n/a | MINOR |
| H-168 | Hand-off section 9 "Where to start" reading order | hand-off §9 | OMITTED | n/a | MINOR |
| H-169 | Hand-off section 9 evidence trail, including the three `/tmp/handoff-notes/*.md` investigation notes that exist only on the author's machine | hand-off §9 | OMITTED | n/a | MINOR |

Partial omissions inside rows counted REPRESENTED (all MINOR, listed so the fix agent may fold them in with one sentence each): A-81 (the 9 pilot `.catfix.md` copies, a D10 effect); A-87 (card_convert `problems` field is the best rejection surfacing of the three); B-39 (`audit-D/bok.py` tests the old `unpassable-ac` hypothesis); B-59 (two places outside `PROFILES` still name grades); C-09 (v1 row `fp` comes from one member's refs while the row `refs` is the union); C-54 (how many of the 29 chained replay clusters are multi-reviewer is not derivable); D-08 (`_check_reflect_resolution` does not check duplicates); D-09 (placeholder-tier semantics, lower-case `classes`, environment key whitelist); D-10 (the local `master` ref is stale and has no `cli/review/`); D-14 (the error names `ExclusionExhausted` and `NoModelAvailable`); D-30 (the no-Fable rule never triggers with packaged data); D-47 (every recommended E2 panel mixes vendors).

COVERED-BY-DEDUP rows (not omissions):

| # | Source finding | Source file | Status | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| A-08 | v1 reviewer line has no confidence field | 01 §1.2 | COVERED-BY-DEDUP | V-139, V-223 (calibrated confidence forbidden in reviewer lines; calibration is downstream) | n/a |
| A-23 | v2-20 `reflect_category: deviation` needs `deviation_class` | 01 §2.2 | COVERED-BY-DEDUP | V-210 / V-223 (v2 rule group) | n/a |
| A-32 | card field keys per shape | 01 §3.1 | COVERED-BY-DEDUP | V-211 | n/a |
| B-26 | `members_by_lid` includes members of invalid-block reviewers | 02 §1.4 | COVERED-BY-DEDUP | D2 (l.589) | n/a |
| B-36 | Tests to keep (verdict/decision rounds 1-3, escalate prints `verdict: FAIL`, no-valid-block refusal, sequencing, CLI output shape) | 02 §3 | COVERED-BY-DEDUP | V-236, V-127 | n/a |
| D-02 | closed template top-level keys | 04 §1 | COVERED-BY-DEDUP | V-490 / BL-08 | n/a |
| D-45 | both E1 and E2 overwrite the stored "intended" field | 04 §7.3 | COVERED-BY-DEDUP | V-269 + V-173 | n/a |
| H-03 | Hand-off method note | hand-off l.6 | COVERED-BY-DEDUP | V-164 | n/a |

### Summary

- **Findings enumerated:** 462 (A = 107, B = 76, C = 56, D = 54, S = 27, H = 169)
- **Represented:** 425
- **Covered-by-dedup:** 8
- **Omitted:** 29 (CRITICAL 0, IMPORTANT 0, MINOR 29)
- **Partial MINOR omissions inside represented rows:** 12 (listed above, not counted in Omitted)
- **Strongest candidates for promotion, if the gate owner disagrees with the rating:** C-07 (mixed-ref asymmetry, the only concrete under-merge mechanism behind D6), C-19 (`PRIMARY_ROLES` inert on the CLI path), A-40 and A-61 (what the converter and the shadow brief leave unchecked or unasked), C-11 (`fp` not recomputed across revisions). Each can be closed with one sentence in the Section 4 rows D6 / MS-02 / MS-01 / MS-05.
- **Checks that found coverage where a first search found none (so the report is more complete than a keyword search suggests):** the all-fp cluster that is never flagged chained (l.1947, l.1979); the unquantified chaining effect on the E2 catch numbers (l.1982); the rf-qa emitter prose gap (Q-42, l.3986); the 10/13/16 chain fixture (l.3851).

**Verdict: PASS (0 omitted at CRITICAL or IMPORTANT)**

