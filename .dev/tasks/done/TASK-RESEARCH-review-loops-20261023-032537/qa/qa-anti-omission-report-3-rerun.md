# Anti-Omission Report: Partition 3 (Rerun)

**Report reviewed:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md` (1,313 lines; sha256 `a10cef088fb1be687fc65a72553910a8a522b4ef8eccb8081e4e2e48972469c7`, re-measured this step)
**Input files checked (Partition 3):** `research/evidence-deck.md` (900), `research/web-01-gap-applicability.md` (182), `synthesis/synth-01-problem-current-state.md` (222), `synthesis/synth-02-target-gaps.md` (116), `synthesis/synth-03-external-findings.md` (104). 5 files, 1,524 lines.
**Date:** 2026-10-24
**Method:** item-level enumeration by meaning. synth-01/02/03 are the source of report Sections 1-5; I ran a `grep -v -x -F` line-diff of each synth body range against its assembled report range and inspected every non-matching line (all were report-added qualifiers or expected table edits, no dropped synth content). The deck is the only Partition-3 input carrying distinct findings not already in a synth component; I enumerated it row by row. Known user-accepted defects J1, L1, L2, L3 are noted, not counted as new omissions.

**Verdict: FAIL**

---

## Verdict basis (one genuine omission)

The report presents the credential-FINAL rubric change as primary Option C (V3) evidence and even adds new git-provenance detail, but it conveys the revised rubric's content **only** through the single "moved line alone is not an issue" clause. The deck records that the captured revised rubric (`agent-a4bfff371c63a6c39.jsonl` record 18) also contained the clause **"Acceptance-recording rules also change"** (`evidence-deck.md:708`). The report nowhere states that the rubric revision altered acceptance-recording rules. The report's only acceptance-recording discussion treats the missing ruling-ledger line as a *bookkeeping omission* (Report:348, Report:893, `evidence-deck.md:565`), a different fact; it does not tie an acceptance-recording-rule change to the rubric revision. A reader of the report cannot learn that the observed rubric change extended to acceptance-recording rules. That is a distinct, specifically-captured historical rule-change finding, silently dropped. Under the gate's "any gap regardless of severity = FAIL" rule this fails.

---

## Enumeration table

Scope per Step 6.36 and the teammate brief: every matrix finding, counting rule, causal distinction, counterevidence, limit, gap, source tension, rubric clause difference and external-applicability conclusion in the Partition-3 inputs. Case-chronology event rows (deck D4) and the 30 screening-slot dispositions (deck D2) are P1/P2-owned restatements per `anti-omission-input-map.md:188-195`; I confirmed their families are represented and do not re-enumerate P1/P2-owned rows here. Status key: R = REPRESENTED (report anchor), D = COVERED-BY-DEDUP (family represented / documented compression), O = OMITTED.

### Block A — Deck D1 Method and counting rules (deck:14-64)

| # | Distinct finding | Status | Report anchor / note |
|---|---|---|---|
| E1 | Population = latest 30 top-level JSONL by mtime at 2026-10-23T03:25:59Z; freezes membership not bytes | R | Report:98, 2.1 |
| E2 | Session = one top-level JSONL; nested logs support, not sampled | R | Report:98, 2.1 table |
| E3 | Incident = a plan-review stage/task/package-final gate; shared package holds several | R | Report:2.1 counting table |
| E4 | Review-stage result unit; multiple advocates/rounds ≠ extra results | R | Report:102, 136 |
| E5 | Finding unit; duplicates/non-defects/rejected/optional ≠ confirmed bugs | R | Report:136, 2.4, 7.3 |
| E6 | Repair-to-review transition unit; proposal/blocked edit/acceptance ≠ transition | R | Report:127-134, 559 |
| E7 | Policy-only re-review kept separate from repair transitions | R | Report:133, 386, 7.4 |
| E8 | Acceptance closure ≠ compliant verdict / ≠ repair | R | Report:148, 7.4, 2.4 |
| E9 | Quoted protocol/injected/compacted/proposed ≠ observed execution | R | Report:104, 2.1 |
| E10 | Six later-finding classifications (introduced / preexisting-missed / unresolved / changed-criteria / unsupported / unknown) | R | Report:311, Options A-E, 2.4 |
| E11 | Before/after evidence required to attribute introduction; sequence alone insufficient | R | Report:240, 311, 2.4 |
| E12 | Subclaims may carry different classifications | R | Report:311 ("Mixed findings retain separate subclaims") |
| E13 | Strict subset: oracle T12, monitor T12, credential follow-up FINAL | R | Report:118 |
| E14 | Repeated verification blocker: manual-page T6 | R | Report:119 |
| E15 | Repeated unsuccessful planning reviews: Orca planning, CI (keep partial/not-ready) | R | Report:120 |
| E16 | Successful one-repair/operational controls retained as counterevidence | R | Report:121, 174-183 |
| E17 | Descriptive classifications, not prevalence/controlled/fleet rate | R | Report:153, 2.1, Gap row |

### Block B — Deck D3 incident dedup & denominators (deck:115-164)

| # | Distinct finding | Status | Report anchor / note |
|---|---|---|---|
| E18 | Six primary-log path register | R | Report:161 (points to deck:117-143) |
| E19 | Six incident dedup keys + boundaries | R | Report:2.2 rows + evidence anchors |
| E20 | Per-incident review/repair denominators (3/2, 3/2, 2/1, 2/1, 7/5, 3/2) | R | Report:127-134 table |
| E21 | Finding counts not summed across incidents (20 Orca / 18 CI / 16 CI / 4 oracle / monitor families) | R | Report:136 |
| E22 | Six incidents ≠ six repositories/uniform procedures | R | Report:153, 2.1 |
| E23 | Review counts ≠ unique reviewer-agent counts | R | Report:136 |
| E24 | Monitor migration re-review and acceptance closures outside repair counts | R | Report:133, 7.4 |

### Block C — Deck D5 cross-case transition matrix (deck:372-408)

| # | Transition / distinction | Status | Report anchor / note |
|---|---|---|---|
| E25 | "Strong" vs "bounded" strength definitions | R | Report:528, Option strength rows; Options Comparison |
| E26 | Orca plan r1→v2: release eligibility/old-value/test-dep/extraction changes; mixed | R | Report:550, Option B Support |
| E27 | Orca plan r2→v3 targeted: secondary paths; unsafe wording, ill-defined mutation | R | Report:550 ("v3 unsafe bad-value wording and ill-defined mutation") |
| E28 | Oracle r1→r2: three fixes work; authority excludes 4th | R | Report:Option E Support, 2.2 oracle |
| E29 | Oracle r2→pass: one-field fixture correction, re-freeze | R | Report:2.2 oracle, Option E |
| E30 | Doc r1→r2: static proof, no renderer/source change | R | Report:Option E/D, 2.2 doc |
| E31 | CI r1→regenerated: exemption status-not-hash; old search weakness; graph repointing loses ancestors | R | Report:550, 592, Option A/B |
| E32 | Monitor r1→r2: PR-list substitution; equal-tag new; older-pin already observed | R | Report:Option B Support, 2.2 monitor |
| E33 | Monitor r2→compliant: range/PR-list corrections accepted | R | Report:2.2 monitor, 7.4 |
| E34 | Monitor compliant→fresh-missing: migration, no repair | R | Report:386(deck)/Report 2.2, 7.4 |
| E35 | Monitor fresh failures after r3/r4: transport repair exposes old output limits | R | Report:733, Option B |
| E36 | Monitor r6→r7: outage/fallback/newline gaps; stdout trap finally reproduced | R | Report:Option B Support (759-762/1240), 7.4 |
| E37 | Credential initial FINAL→pass control: durable proof restored | R | Report:178, Option D Support |
| E38 | Credential follow-up r1→r2: accepted lint exception + pointer repairs leave blank T10; one range incomplete | R | Report:604, Option D Support |
| E39 | Credential r2→pass: evidence + changed policy, confounded | R | Report:731, 2.5 |
| E40 | Non-review stop: Orca v4 authorized, no later review | R | Report:2.2 Orca, 7.4 |
| E41 | Non-review stop: manual-page scoped acceptance, FINAL pass ≠ rendering | R | Report:148, Option E |
| E42 | Non-review stop: monitor accepts 4 defects, `misunderstood` | R | Report:2.2 monitor, 7.4 |
| E43 | Non-review stop: CI partial/not-ready asks user | R | Report:2.2 CI |
| E44 | Non-review stop: oracle archive blocker ≠ another review | R | Report:130 boundary |

### Block D — Deck D6 causal classes + per-finding matrix (deck:411-575)

| # | Finding | Status | Report anchor / note |
|---|---|---|---|
| E45 | Six causal-class admission rules + opposition/limits | R | Report:2.4, 311, Options |
| E46-E75 | Orca planning 30 later-finding/targeted rows (deck:430-459): release predicate; lock-digest→provenance; inventory-before-registration; renderer-test boundary; wrong fetch remote; validation-after-use; candidate/pinned-output checks; dispatch flags untested; repo-failure-vs-outage joint fixture; release-pruning creds; manual upstream metadata cases; current-pin patch-check path; shape-check mechanism; toolchain/diagnosis not tested; rollback comparison direction; concurrency key (withdrawn); base-result capture gap; logs-could-be-staged; PR-head-by-mode; sufficiency duplicate; secondary collector tags; bad-value error echo; annotated-tag URL (source contradiction); missing fetch-level malformed rollback case; missing guard mutations; downstream dependency explanation; state-removal mutation; pin/rollback no-op output state; up-to-date-week live check; repository self-check after fetch | D | Family represented (Report Option A/B Support, 2.2 Orca, Gap 2); report documents per-row Orca detail "remains in the case/deck" (Report:271, 379). Canonical source tensions 441/459 elevated at Report 2.5 and Q6. Annotated-tag (deck:452) and validation-ordering (deck:435) are facets of the before-use-validation family represented at Report:523/586; not elevated but within documented compression |
| E76-E91 | Orca 16 original accepted repairs (deck:465-483) | R | Report:312 ("fourteen accepted original amendments and two partial"); 7.7, deck:461-484 cited |
| E92 | Oracle: unverified guard/producer rejection predicate | R | Report:523, Option A/E, 2.2 |
| E93 | Oracle: provenance family changes wrong causal factor | R | Report:Option A Support, 2.6 oracle |
| E94 | Oracle: missing-abstraction import-cycle omission | R | Report "missing-abstraction" (line ~523/2.6) |
| E95 | Oracle: default-path false fixture retained | R | Report:523, Option E Support, 2.2 |
| E96 | Oracle test counts 67/78→74/85; historical, not run here; assertion strengthened w/o added test | R | Report:238, Option A/2.4 |
| E97-E114 | CI retained/introduced/optional/corrected 18 rows (deck:501-518): tooling-exemption-misses-hashes; PR search filters/order; dependency ancestors lost; stub confinement; half-edited advisory passes; rename/copy handling; research-file immutability check; job-name substring; decision serialization; angle-bracket check; boundary whole-doc comparison; directory-wide allowlist; literal advisory-word requirement; nonempty-render accepts failure; status flags inconsistent; leftover line-number frame; coverage-matrix omissions; proposed renumbering conflicts | D | Family represented (Report Option A/B Support, Gap 2/7, 2.2 CI); report documents 18/16/8 "overlapping inventories … not added together" and detail "remains in case" (Report:274, 382). Specific rows (half-edited advisory :505, dependency ancestors) cited explicitly at Report:343-344 |
| E115 | CI four retained low findings + two withdrawn claims (README line 30, path-filter) don't increase 16 | R/D | Report:Gap 7, 7.3; "path-filter" at Report:1289; README-line-30 within documented case detail |
| E116 | CI original 18 received substantial plan-text repairs | R | Report:2.2 CI ("substantial applied repairs"), 382 |
| E117-E138 | Monitor finding families (deck:528-549): older-pin/equal-tag; failed-PR-listing swallowed; missing detect summary; blank-notes/compat; missing upper tag; carriage-return quote escape; unused helper/reversed rollback; incomplete rerun log; early pin-gate/token/checkout summary; collector JSON arg-limit; Electron field callout; rename overlap; detect checkout summary; provenance hash fields; capitalized security term; security output unbounded; very-large tag-list ceiling (weak); selected-release-as-outage; links-only fallback unbounded; error-annotation-as-pin-value (introduced trap); newline-suffixed validators; cosmetics/uncapped fields | D | Family represented (Report Option A/B Support, 2.2 monitor, Gap 1/2); report documents monitor detail/thresholds "remain in case," fixture-specific not universal (Report:275, 383). Trap 759-762/1240, unbounded output (733), arg-limit explicit at Report Option B |
| E139 | Monitor reviewer identities/dispatch records mapping | D | P2-owned (05-session); Report 2.2 "five reviewer identities" |
| E140-E150 | Credential 11 finding rows (deck:557-567): README-separator lint; T6 softens literal lint; T8 one-line shift; T7 wrong section; T17 incomplete proof; T10 blank line; first T7 repair misses last row; T10 repair exceeds authorization; second FINAL absent from ledger; third FINAL different rubric; narrow manpage task-body omission | R | Report:577, 604, 348, 350, Option C/D Support, 2.2/2.6 credential; "last row"/Task 8 present |
| E151 | Credential eight observations ≠ eight defects; obs 4/7/8 (overwrite wording, no ruling line, restart remark) accurate/non-defect | D | Report:276 ("eight final observations are not eight delivery defects"); obs-4/7/8 specifics within documented case detail; ruling-line represented at Report:348/893 |

### Block E — Deck D7 why-earlier-reviews-missed (deck:579-604)

| # | Miss mechanism | Status | Report anchor |
|---|---|---|---|
| E152 | Text coverage credited without state wiring (Orca) | R | Report:343, 530, Option A |
| E153 | Temporal requirement reduced to validation presence | R | Report:523, 586(deck)/Option A |
| E154 | Source test table weaker than behavioral contract | R | Report:2.4, Option A |
| E155 | Labels/cardinality instead of required meaning (oracle) | R | Report:523, 2.4 |
| E156 | Exec name/exit status treated as renderer availability | R | Report:Option E Support, 2.4 |
| E157 | Wrong initial state corrupts attribution (T2) | R | Report:604, Option D |
| E158 | Remedy targets one op not sibling (CI search) | R | Report:591(deck)/Option A, Gap 2 |
| E159 | One of two independent checks repaired (CI status/hash) | R | Report:592(deck)/Option A, 2.2 CI |
| E160 | Path-specific error handling leaves other boundaries (monitor) | R | Report:Option B/A, Gap 2 |
| E161 | Later limit masked by earlier failure | R | Report:733, Option B |
| E162 | Temporary proof lost during ledger handoff | R | Report:346, Option D |
| E163 | Criterion knowingly softened | R | Report:577, Gap 3 |
| E164 | Later defect did not yet exist (introduced) | R | Report:240, Option B |
| E165 | Earlier miss remains unobservable/unknown | R | Report:Q2, 946 (deck:598), 2.7 |

### Block F — Deck D8 unsupported findings & disagreements (deck:608-639)

| # | Adjudicated claim | Status | Report anchor |
|---|---|---|---|
| E166 | 20 Orca items ≠ 20 fresh defects (duplicate + concurrency non-defect) | R | Report:349, 2.2 Orca |
| E167 | "13 fixed, 3 partial" incorrect → 14/2 | R | Report:253, Gap 8, 2.5 |
| E168 | Pin-equals-current no-op permitted (withdrawn) | R/D | Report "no-op" contradiction 2.5; subclaim within documented Orca detail |
| E169 | Concurrency key removal withdrawn | R | Report:525 ("concurrency note… not a defect") |
| E170 | Every absent mutation ≠ functional defect | D | Within documented Orca/CI detail; family at Report Gap 7 |
| E171 | Missing dependency prose ≠ unguarded jobs | R | Report:503(deck)/Option A/B |
| E172 | T2 unrelated header/key-fanout = false attribution | R | Report:604, Option D |
| E173 | T6 unverified ≠ malformed page | R | Report:Option E Opp, 2.2 doc |
| E174 | Oracle 2nd reviewer invented default-path = false | R | Report:620(deck)/Option A/E ("default-path security property") |
| E175 | CI boundary-file overclaim → optional hardening | R | Report:2.2 CI, Option C Support |
| E176 | CI directory-wide overclaim → downgraded | R/D | Report "allowlist" (1288-area)/documented CI detail |
| E177 | Rename path-order advice wrong, corrected | D | Within documented CI detail; Report Gap 7 ("corrects rename advice") |
| E178 | CI literal advisory-word check rejected | D | Within documented CI detail |
| E179 | CI matrix corrections ≠ implementation work | R | Report:Gap 7 ("separates matrix defects from task defects") |
| E180 | File-backed monitor JSON ≠ cause of oversized output | R | Report:733, 2.2 monitor |
| E181 | Not every monitor late finding violates original AC | R | Report:275, Option A Opp |
| E182 | Monitor incomplete log ≠ checks never ran | R | Report:Option B (535 deck), Gap-area |
| E183 | Latest credential PASS ≠ unchanged-rubric convergence | R | Report:629(deck)/7.3, 731 |
| E184 | Ledger verdict count ≠ every review | R | Report:350, 259, Gap 8 |
| E185 | `head-moved` ≠ HEAD actually moved | R | Report:351, 603-604(deck)/2.5, Option D |

### Block G — Deck D9 counterexamples/controls (deck:643-668)

| # | Control | Status | Report anchor |
|---|---|---|---|
| E186 | Oracle repairs 1-3 work | R | Report:176, 366 |
| E187 | Monitor Tasks 10/11 converge | R | Report:177, 367 |
| E188 | Initial credential final gate one-repair | R | Report:178, 368 |
| E189 | Session 10 Task 4 | R | Report:179, 7.7 |
| E190 | Session 17 Task 8 | R | Report:180, 7.7 |
| E191 | Session 17 FINAL (restore-basename bug) | R | Report:181, 369, 7.7 |
| E192 | Session 09 FINAL never ran | R | Report:182, 7.7 (not-placed) |
| E193 | Session 19 nine compliant | R | Report:183, 7.7 |
| E194 | Sessions 13/14 plan corrections w/o re-review | R | Report:551, 7.7 |
| E195 | Oracle valid pre-freeze design | R | Report:Option E Opp, 2.2 |
| E196 | Monitor output limits exposed not created | R | Report:733 |
| E197 | Credential pass: accepted gap + narrow omission remain | R | Report:2.2 credential, 276 |
| E198 | Sample clustered, mtime-selected; no fleet rate | R | Report:153, Gap row, 7.3 |

### Block H — Deck D10 current-vs-historical rule map (deck:672-738)

| # | Rule finding | Status | Report anchor |
|---|---|---|---|
| E199 | Seven source/installed pairs matched at inspection; not enforcement proof | R | Report:229, 2.3, 7.5, 258 |
| E200 | Workflow generation vs advisory reflection; no auto-edit | R | Report:193, 2.3, Option A |
| E201 | Generation checks ≠ semantic proof | R | Report:530, 2.3 |
| E202 | Task review inputs (brief/AC/constraints/diff) | R | Report:194, 2.3, 557 |
| E203 | Retry ladder bounded ≠ lifetime cap; monitor no ladder/adviser/revert observed | R | Report:195, 2.3, 2.7, Option A |
| E204 | Ledger append-only; scoped acceptance; fresh FINAL after terminal | R | Report:198, 2.3 |
| E205 | Managed FINAL pinned plan/source, state digest, stop-on-issues | R | Report:196-197, 2.3 |
| E206 | Monitor one-fix→migration/fresh-review change | R | Report:229, Option C, 2.3 |
| E207 | Credential FINAL earlier rubric: "missing/stale/unverifiable evidence is issues" (deck:707) | D | Semantically covered by current-FINAL rule "unmet or unverified criteria … are [issues]" (Report:196) and after-load=current qa.md:82 tie (Report:584) |
| E208 | Credential FINAL revised rubric: moved-line-alone not issues; current evidence & scoped acceptance govern (deck:708) | R | Report:196, 584, 744; scoped acceptance Report:197 |
| E209 | Credential FINAL revised rubric: **"Acceptance-recording rules also change"** (deck:708) | **O** | **IMPORTANT. Not represented. See omissions table O1.** |
| E210 | Checkpoint-absent→moved category (deck:709) | R | Report:351, 2.5, Option D |
| E211 | Captured before/after rubric hashes (0b533765 / faff03b7) | R | Report:206-207, 229 |
| E212 | Rubric updater unknown; separate effect on pass unknown | R | Report:Q3, 947, 744 |
| E213 | Ladder bounded vs operator-resume fresh reviews (design boundary) | R | Report:2.3, 726(deck)/7.5 |
| E214 | Criterion softened without acceptance = exec/authority problem | R | Report:577, Gap 3 |
| E215 | Plan/source pinned = frozen-repair authority relevance | R | Report:197, Option E current-rule |
| E216 | Missing checkpoint halts escalation = guard outcome not movement | R | Report:351, Option D |
| E217 | Changed FINAL policy = actual historical input change | R | Report:229, Option C |
| E218 | No stable finding-resolution registry binding later reviewers | R | Report:198, 584, 731(deck) |

### Block I — Deck D11 source inventory & observation boundaries (deck:741-810)

| # | Finding | Status | Report anchor |
|---|---|---|---|
| E219 | Research-components inventory (22 rows) | R | Report:10.2-10.3 |
| E220 | Primary identifier joins (6 cases) | R | Report:2.2 transitions, 10.2 |
| E221 | Manifest = membership freeze not byte freeze | R | Report:98, 147, 2.1 |
| E222 | Orca four versions reconstructed; v4 unreviewed | R | Report:165, 846, 2.2 |
| E223 | CI initial inspection 03:41:52Z, 1,000 rows, probe running | R | Report:143, 2.1 |
| E224 | CI supplement 04:02:04Z, 1,086 rows | R | Report:143, 2.1 |
| E225 | Monitor original prefix 1-1247 ends 03:31:57Z | R | Report:144, 2.1 |
| E226 | Monitor supplement 04:03:52Z, 1,437 rows | R | Report:144, 2.1 |
| E227 | Recovered-screening Unicode-split corrected by physical-newline anchors | R | Report:10.3, 1053 |
| E228 | Historical rules = exact loaded, not reconstructed from today | R | Report:229, 2.3, Option C |
| E229 | Earlier captures not rewritten; later supplements qualify endpoints | R | Report:2.5, 10.3 |

### Block J — Deck D13 gaps / D14 stale / D15 accounting (deck:827-880)

| # | Finding | Status | Report anchor |
|---|---|---|---|
| E230-E244 | 15 gap questions (deck:831-845): reviewer-miss; rubric author; unchanged-rubric pass; Orca v4 quality; CI exec failure; runner behavior; manual render; monitor defects repaired; size thresholds; oracle effectiveness; historical oracle bytes; excluded-session nested activity; durable-pointer semantics; helper enforcement; live-source identity | R | Report Section 9 Q2,3,4,5,7,8,9,10,11,12,13,14,15,16,17 |
| E245 | No missing history filled with generic explanation | R | Report:941, 2.5, 7.3 |
| E246-E254 | 9 stale items (deck:853-863): moved/wrong ledger citations; blank lint line; temp proof not preserved; inconsistent closure summaries; condensed findings omit detail; ledger omits 2nd FINAL; shared ledger later events; provisional screens resolved later; different rules same path | R | Report:2.5 exceptions table (253-261), 350, Option C/D |
| E255 | Stale ≠ blanket current-doc-defect claim | R | Report:263, Boundaries of Gap Inventory |
| E256-E262 | 7 research-gate accounting bullets (deck:874-880): Orca 16 repairs/14-2; CI 8 reviewer entries dispositions; monitor membership≠content freeze; credential 2nd FINAL preserved; earlier misses unknown; screening corrections; workflow-status not completion | R | Report:2.2/2.5/Gap 7/8, 10.8, header gate-qualification |
| E263 | Deck claims assembly-only, no gate verdict | R | Report:5, 10, 10.8 (gate qualification) |

### Block K — web-01 external-applicability (whole file)

| # | Conclusion | Status | Report anchor |
|---|---|---|---|
| E264 | Decision: external research N/A, reasoned not skipped | R | Report:395-397, 5.1 |
| E265-E282 | 18-row gap-applicability inventory, each N/A with handling | R | Report:5.1 table + 406/407 additions; Report:414 ("all fifteen deck questions plus specification/sampling/freshness") |
| E283 | Provider record: zero queries/sources/findings; none invoked; no outage | R | Report:5.2, 968 |
| E284 | Earlier failed doc-package lookups attributed correctly | R | Report:5.5, 10.3 (deck/qa-phase-3-fix-log) |
| E285 | Missing path ≠ event never happened; recovered nav/hashes narrower | R | Report:5.5, 466-468 |
| E286 | No external recommendation; preserve local conclusions + unknowns | R | Report:5.3, 5.5 |
| E287 | Not authorization to add case/repair/execute/rank/probabilities | R | Report:462, 5.5, Section 8 |

### Block L — synth-01/02/03 unique content (report Sections 1-5)

| # | Finding | Status | Note |
|---|---|---|---|
| E288 | synth-01 Sections 1-2 full content | R | Report Sections 1-2 byte-diff: no dropped lines (report adds qualifiers, out-of-window disclosure, counting table) |
| E289 | synth-02 Sections 3-4 full content (8 success criteria, 6 constraints, 12 gap rows, boundaries, coverage, 4 controls) | R | Report Sections 3-4 byte-diff: all present |
| E290 | synth-03 Section 5 full content (5.1 inventory, 5.2 provider, 5.3 local findings, 5.4/5.5) | R | Report Section 5 byte-diff: all present |

---

## Omissions table

| # | Source finding | Source file:line | Status | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| O1 | The captured revised credential-FINAL rubric clause **"Acceptance-recording rules also change."** The report presents the rubric revision (even adding git provenance and hashes) but conveys its content only via the "moved line alone is not an issue" clause; it never states that the rubric change altered acceptance-recording rules. The report's acceptance-recording discussion attributes the missing ruling-ledger line to a *bookkeeping omission* (Report:348, 893), a distinct fact, not to a rubric-rule change. | `research/evidence-deck.md:708` | OMITTED | n/a | IMPORTANT |

---

## Summary

- **Findings enumerated:** 290 (E1-E290). Row count note: Blocks A(17), B(7), C(20), D(107: E45 + E46-E75=30 + E76-E91=16 + E92-E96=5 + E97-E116=20 + E117-E139=23 + E140-E151=12), E(14), F(20), G(13), H(20), I(11), J(34: E230-E244=15 + E245 + E246-E254=9 + E255 + E256-E262=7 + E263), K(24: E264 + E265-E282=18 + E283-E287=5), L(3). Mechanical sum: 17+7+20+107+14+20+13+20+11+34+24+3 = **290**.
- **Represented:** 256
- **Covered-by-dedup:** 33
- **Omitted:** 1
- **Reconciliation:** 256 + 33 + 1 = 290 = enumerated. ✓
- **Verdict:** FAIL (1 omitted).

The COVERED-BY-DEDUP rows (E46-E75 Orca per-finding matrix; E97-E116 CI per-finding matrix; E117-E139 monitor per-finding matrix; E151 credential eight-observation detail; E168/E170/E176-E178 adjudication sub-rows; E207 earlier-rubric clause) are all specific per-finding case-matrix rows whose *family* is represented in the report and whose per-row detail the report **explicitly and transparently declares retained in the case/deck and deliberately not reproduced** (Report:271, 274, 275, 276, 379, 382, 383). That is documented compression, not silent dropping, so it is not an omission. Only O1 is a distinct finding the report both fails to state and does not declare as deliberately excluded.

## Limitations

- Deck D4 case chronologies (deck:168-371) and D2 screening-slot dispositions (deck:68-105) originate in Partitions 2 and 1 respectively (`anti-omission-input-map.md:188-195`); I confirmed their families are represented in the report but did not re-enumerate P1/P2-owned rows, per partition ownership.
- synth-01/02/03 representation was confirmed by `grep -v -x -F` line-diff of each synth body range against its assembled report range plus manual inspection of every non-matching line; all differences were report-added qualifiers/table edits, no dropped source content.
- Report line numbers cited are from the full read of the 1,313-line report this turn (sha256 re-verified). The report header records that fidelity and anti-omission gates had not yet passed; that status does not affect omission judgments, which are by meaning against the sources.