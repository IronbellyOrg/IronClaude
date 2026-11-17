## 6. Options Analysis (conflict log)

**Scope of this section.** This is required report content (c): the conflict log. It records every place where the three studied efforts, or the code and its own documents, disagree; for each it gives the positions, two or more options, the evidence, a status and a recommended resolution. It is a report section only: it contains no roadmap and does not start any workflow run (owner scope change of 2026-11-13).

**Efforts and tags.** E1 = this session's reflect Tier 2 panel kernel, shadow mode and model-combination experiment on branch `ironbelly/shadow-runs`. E2 = the other session's tasklist review-panel evaluation study, taken at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only (no product-code change; `CR` below = that study's `COMBO-REPORT.md` at that commit, `PR` = its `PILOT-REPORT.md`, `AD` = its `analysis/audits/audit-D/` at that commit). E3 = the #346 review loop on master plus the experiment variants that are installed in `~/.claude/` and in the phase-5 bundle but are not in `src/` (the hand-off's "only in the bundle" is [CODE-CONTRADICTED]; see gaps log D-15). `[ext]` = a consumer outside all three efforts (PR review, Auggie, rf-qa). `[web]` = external context from the Phase 4 web research, always with its source URL.

**Evidence rules used.** Only `[CODE-VERIFIED]` statements support a current-state claim. E2 headline numbers come from the study's own report text (read at the commit above, raw `score.json`/`cost.json` files not re-aggregated, gaps log G-82); they are marked `[DOC-SOURCED]` and are used as supporting evidence only, never as the sole basis of a decision. `[UNVERIFIED]` claims decide nothing. Model-behaviour evidence carries its date: E2 runs 2026-11-11 to 2026-11-13 (one gateway), E1 shadow runs 2026-11-12 22:22 UTC to 2026-11-13 02:42 UTC, E1 combo runs 2026-11-13, E3 bundle 2026-11-08/09. Citations such as `01 §14` mean `research/01-finding-contract.md` section 14; `G-nn` and `D-nn` are rows of `gaps-and-questions.md`. Effort sizes: XS < S < M < L < XL; risk: Low / Medium / High.

**Known-contradicted claims not built on.** The experiment variants exist only in the bundle (they are also installed in `~/.claude/`); audits B, C, E and F have summaries (only A and D do); "4 verdicts flipped" (audit D names 3 flipped merges plus total-loss merges); "alias GT3 found once" (the once-found issue is alias GT1, B6); the hand-off's line numbers for D7, D11 and D12 (moved); the `ledger.merge_round` docstring on clearing (`ledger.py:112`; the code at `:254-258` never reads `block_ok`).

### 6.0 Conflict index

| ID | Conflict | Slug | E1 position | E2 position | E3 position | Status | Recommended resolution (one line) | Adversarial result |
|---|---|---|---|---|---|---|---|---|
| C01 | Finding schema and severity scale | `finding-schema-severities` | findings-v2 superset (lens, channel, role-tagged citations, deviation class), CRITICAL/MAJOR/MINOR kept | Drove findings-v1 unchanged through the product loop | findings-v1; experiment ledger has per-profile grades and computed blocking | DECIDED-BY-EVIDENCE | v2 container as the base, v1 a strict subset, per-lens vocabularies with the native value preserved | n/a |
| C02 | Anchor handling at merge, including the 200-character anchor drop | `anchor-handling-merge` | v2 keeps the 12-200 limits; unresolved citations kept and flagged; card claims truncated silently | Measured 49 blocking findings lost to length limits; recommended truncate or instruct and re-validate | v1 rejects over-length and keeps missing anchors silently; experiment ledger has no length limit but refuses missing anchors | DECIDED-BY-EVIDENCE | Truncate-prefix with a counter for length, persist every rejected line, flag a missing anchor instead of letting it block silently | n/a |
| C03 | Model and tier configuration (gateway versus anthropic-only) | `model-tier-config` | anthropic-only reflect gate, class launch values | Raw gateway model ids, bash fallback ladder | Tier file with gateway `launch: {}` and anthropic-only stand-ins | UNDECIDED-BY-EVIDENCE, resolved by adversarial debate | Option A: anthropic-only with class launch values, plus B's launch grammar, provenance and `panel verify`; gateway `launch` entries not adopted now; O-2 stays open | winner A (partial: INV-013 and INV-009 unaddressed, 4 diff points unresolved); `reviews/adversarial/model-tier-config/` |
| C04 | Distinctness: strict versus soft | `distinctness` | Opt-in strict distinctness and class exclusion; class-disjoint calibrator in prose | One deliberate repeat (second luna) is the only doubling effect that survived testing | Soft default that silently re-admits duplicates (D11) | DECIDED-BY-EVIDENCE | Declared per-slot distinctness and no silent re-admission (decided); intended replicas an optional design option resting on one uncorrected E2 p-value | n/a |
| C05 | Who decides blocking: veto, quorum, calibrator, blind grader or debate | `who-judges-blocking` | Debate plus card-level calibrator; cluster support computed but not used; single-reviewer merge degraded | Measured the single-reviewer veto: 65 judge-blocking versus 38 real | Veto in the master ledger; rule predicate and blind grader in unmeasured experiments | UNDECIDED-BY-EVIDENCE, resolved by adversarial debate | Option D: blind grader after clustering, in shadow first and live per lens after a paired replay; hardened single-reviewer veto is the live decider and control until then | winner B by tiebreaker (partial: 11 HIGH invariants unaddressed, 3 diff points unresolved); `reviews/adversarial/who-judges-blocking/` |
| C06 | Calibration as a panel role and its rubric | `calibration` | Blind per-card calibrator reused from troubleshoot; 0 of 689 legacy numbers, 142 of 142 shadow numbers when asked | Not tested (no calibrator in the study) | None on master; grader is a different mechanism | DECIDED-BY-EVIDENCE | Optional finding-level calibrator with its own rubric and explicit rubric path; routing and telemetry signal, not a decider | n/a |
| C07 | How runs are recorded | `run-recording` | Hash-chained stage manifest plus agent-written telemetry block | `meta.json`, `cost.json`, `fallback.log` and after-the-fact audits A and D | Rich review-telemetry/1 schema that nothing writes | DECIDED-BY-EVIDENCE | One manifest per run, attempt payloads in the telemetry groups, audits turned into built-in checks | n/a |
| C08 | Identity check: observed versus pinned | `identity-check` | Pinned; `identity_source: observed` has no code; parity compares records | Observed served model as a hard gate, but `expected_model` rewritten on fallback | Schema with resolved, launch and observed fields, no writer | DECIDED-BY-EVIDENCE | Record requested, launch and served separately; observe where the adapter can; redefine parity | n/a |
| C09 | Dispatch of reviewers | `dispatch` | In-session Agent calls by class; resolution does not drive dispatch; collapse to one model seen | One `claude -p` process per reviewer on a raw model id | Prompt says "fresh context"; code-driven swarm engine is a third path | DECIDED-BY-EVIDENCE | One dispatcher interface with adapters per environment; the pin is enforced and the served model recorded | n/a |
| C10 | Brief and driving-document input contract | `brief-input-contract` | Orchestrator-written three-section brief; spec body only for the qa persona | Brief names only the candidate; source file shipped beside it; 156 of 665 runs never referenced it | Five placeholders, none for a source | DECIDED-BY-EVIDENCE | One code-rendered brief template with source, spec and grounding slots; record what was injected and read | n/a |
| C11 | Reflect merge path and contract bump | `merge-path-contract-bump` | Debate kept, contract 1.8.0 frozen, deterministic merge deferred to 2.0.0 | Deterministic merge only; no debate or calibrator | Deterministic ledger merge; code-driven engine is a third merge path | DECIDED-BY-EVIDENCE | Keep the debate and 1.8.0; merge step writes its own verdict file; one code contract writer; bump only after C05 | n/a |
| C12 | Clustering algorithm | `clustering` | Path-aware cluster_v2, chain flag, AI-labelled 0.84 / 0.95 sample | Measured v1 over-merge: 195 chained rows, 83 mega-rows | v1 union-find on section, ids and spans | DECIDED-BY-EVIDENCE | One clusterer on the v2 location model with complete-link admission, anchor-to-citation step and per-target ids | n/a |
| C13 | Ledger model: re-find and cluster versus find-once verify-only | `ledger-model` | No ledger for reflect (single pass) | First reviews only; no evidence on rounds 2-3 | Re-find ledger on master; verify-only ledger and stoprule in unmeasured experiments | UNDECIDED-BY-EVIDENCE, resolved by adversarial debate | Option B (find once, then verify-only) via a staged hybrid: Stage 0 applies A's cap, quorum and atomic-refusal fixes to the master ledger; a decision gate then picks "A plus fixes" or the verify-only port after a pre-registered falsifier run | winner B, narrowly (partial: 10 HIGH invariants unaddressed, 4 diff points unresolved); `reviews/adversarial/ledger-model/` |
| C14 | Panel size versus cost: fewer reviewers or fix the rubric first | `panel-size-cost` | Cap of 3 reviewers; Tier 2 paid on 37 of 38 recorded pre runs (MR:142; recount 38 of 39); H-A unmeasured; O-8 rubric lever | Ceiling about 2-2.5 of 14 per run; no panel significantly better; more reviewers add wrong blockers | Default template has 4 reviewers, live7 has 7 | UNDECIDED-BY-EVIDENCE, resolved by adversarial debate | Option B as merged (Step A: record escalation rows first, pre-filter unchanged unless the keys show it decisive; cap at 3; Step C: count after H-A) plus A's skill-path default of two as owner-gated Decision D-1; Phase 1 (flag advisory) conditional | winner B by tiebreaker (partial: 3 HIGH invariants unaddressed, 6 diff points unresolved); `reviews/adversarial/panel-size-cost/` |
| C15 | Bad-line and invalid-block policy | `invalid-block-policy` | One bad line invalidates the block and the whole reviewer is dropped from clustering | 80 reviewer-level invalid blocks measured | v1 keeps the valid lines; experiment ledger refuses the whole input | DECIDED-BY-EVIDENCE | Keep valid lines, mark the reviewer partial, persist every rejection | n/a |
| C16 | Blocking predicate per lens (label rule, consequence rule, deviation class) | `blocking-predicate-per-lens` | Label rule with `reflect_category`; halt on Drift or Regression counts | Product brief (consequence rule) used as shipped | Consequence rule in prose; computed predicate in the experiment ledger | DECIDED-BY-EVIDENCE | Per-lens predicate in data; reviewer flag kept as input; effective blocking recorded | n/a |
| C17 | Fate of the code-driven Tier 2 engine behind the tasklist post gate | `ensemble-engine-fate` | UC-2 panel deferred to Stage 5; engine is a reflect code path on master | Not studied | Master consumer of the reflect wrapper | DECIDED-BY-EVIDENCE | Fix in place first (honest labels, real deviation flags); replace later at UC-2 Stage 5 | n/a |
| C18 | Read-only enforcement for reviewers | `reviewer-read-only` | Tool allowlist agent, plan permission mode | Deny list on Edit/Write with Bash auto-approved | Prose rule; re-review step needs shell commands | DECIDED-BY-EVIDENCE | Allowlist everywhere; shell evidence computed by the orchestrator and injected as hunks | n/a |
| C19 | One verdict contract and exit-code vocabulary | `verdict-contract` | Four-verdict reflect map (PASS, DEGRADED, HALTED, BLOCKED) | Not studied | Ledger PASS/REVISE/ESCALATE (exit 0/10/11); experiment CONTINUE/PENDING | DECIDED-BY-EVIDENCE | Core returns one machine verdict; each module maps it to advisory or blocking and to its own format | n/a |
| C20 | Rollout and evaluation: shadow mode versus ground-truth benchmark | `rollout-evaluation` | Shadow mode and exit script; measures side signals, never quality | Ground-truth packages and a blind judge; measures quality, no shadow mechanism | Pre-registered screen and evidence checker; no valid success | DECIDED-BY-EVIDENCE | Use both: shadow for rollout safety, ground-truth benchmark for quality regression | n/a |

### C-01: Finding schema and severity scale (slug: finding-schema-severities)

| Effort | Position | Evidence |
|---|---|---|
| E1 | findings-v2: same container and CRITICAL/MAJOR/MINOR scale as v1, plus lens, channel, role-tagged citations, deviation class, coverage rows and a self-confidence slot; reviewer-line `calibrated_confidence` is rejected | `findings_v2.py:36-38,84-187`; 01 §2 [CODE-VERIFIED] |
| E2 | Drove the product findings-v1 format unchanged (`/sc:spec-panel --mode critique`); its brief repeats the product grading line and the v1 field list | E2 `run-reviewer.sh:13-17`; 01 §11 [CODE-VERIFIED via `git show`] |
| E3 | findings-v1 (10 ordered rejection rules, 6 categories); the installed experiment ledger has per-profile grade vocabularies and a computed blocking predicate and no category | `findings.py:14-22,90-121`; `review_ledger.py:38,41-59`; 01 §1, §10.2 [CODE-VERIFIED] |

#### Option A: findings-v2 as the single contract, v1 a strict subset

**Description:** Keep the `## Findings block` fenced JSON-lines container and the `findings-v2` info string; accept `findings-v1` lines as a subset; add severity vocabulary, category set and blocking predicate per lens as data.
**How it works:** `findings_v2.check_finding` becomes the only validator; a lens module declares its severity words, categories, primary location kind and blocking predicate (the experiment ledger's `PROFILES` table and `cluster.PRIMARY_ROLES` are the precedents); each finding keeps the native severity word next to the comparable one.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | Medium |
| Reuse of existing code | High: `findings_v2.py`, `cluster.py` roles, `PROFILES` pattern, `card_convert` word map |
| Files/systems affected | `findings.py`, `findings_v2.py`, `card_convert.py`, `cluster.py`, brief files, reflect shadow brief line, `document_review_loop_prompts.md`, tests that pin the v1 text |
| Pros | Covers the largest share of the field superset already; one validator; v2 already separates reviewer confidence from calibrated confidence |
| Cons | The v2 docstring claim of v1 compatibility is false for blocks and under `reflect-post` (01 §2.4), so "strict subset" needs code and tests, not only wording |

#### Option B: keep v1 for document lenses and v2 for reflect, joined by adapters

**Description:** Leave both stacks; convert between them with `card_convert`-style adapters.
**How it works:** document loops keep findings-v1 and the ledger; reflect keeps findings-v2 and the cluster path; new consumers pick one and write an adapter.

| Aspect | Assessment |
|---|---|
| Effort | S |
| Risk | Medium (drift between the two stacks grows) |
| Reuse of existing code | Complete |
| Files/systems affected | One adapter per new consumer |
| Pros | No change to either stack or to the 651 `tests/review` tests |
| Cons | The same four limits stay hard-coded in nine places (01 §14.1); v2 imports private v1 names so v1 edits leak into v2; every adapter repeats the severity-word guesses that already invert rf-qa `IMPORTANT` |

#### Option C: new five-tier core scale with a separate obligation field

**Description:** Replace the three-value scale with critical/high/medium/low/info plus a separate blocking obligation and SARIF-style export.
**How it works:** all lenses map their words onto five tiers; blocking is computed per lens.

| Aspect | Assessment |
|---|---|
| Effort | XL |
| Risk | High |
| Reuse of existing code | Low: touches `SEVERITIES` in findings, telemetry strata and the experiment ledger grades |
| Files/systems affected | `findings.py`, `findings_v2.py`, `card_convert.py`, `telemetry.py`, the PR severity router and rubric, all briefs |
| Pros | Matches the PR five-tier vocabulary and external practice; keeps the middle tier |
| Cons | The case for it rests on external sources only; no effort measured a benefit; breaks the most pinned text |

**Evidence:**
- Only two of seven finding shapes are enforced by a Python validator (v1, v2); every other shape derives blocking from a level or a definition (01 Summary) [E3][E1] [CODE-VERIFIED].
- A code-review finding fails v1/v2 at id, severity, blocking and category before location is checked; an rf-qa finding fails at `IMPORTANT` (01 §13) [ext] [CODE-VERIFIED]. `card_convert` maps `important` to MINOR non-blocking and reflect MEDIUM to non-blocking (`card_convert.py:71-83`), the reverse of rf-qa's own rule (01 §3.2) [E1].
- v2 already covers lens, channel, citations with roles, coverage and self-confidence; the missing pieces are `in_diff`, multi-file observations, file+section locations, a consequence sentence and non-spec namespaces (01 §12 Key Takeaways) [E1].
- The experiment ledger's `PROFILES` shows per-profile grades plus blocking predicate plus cap as a working pattern (`review_ledger.py:53-59`) [E3] [CODE-VERIFIED]; it has one profile only (02 §6.1).
- External context [web]: SARIF converter guidance keeps the native value under its native name next to a comparable core value (https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html; microsoft/sarif-tools issue 43); every examined 3-to-5 mapping loses a tier at the extremes (web-02 §7.3); a five-tier core is web-02 recommendation 1. These support A's "native value preserved" rule and are the only support for C.

**Status:** DECIDED-BY-EVIDENCE: the code evidence (01 §12, §13, §16) shows v2 is the base that already carries the most fields and that per-lens vocabularies are needed; the number of core tiers is not needed to choose A.

**Recommended resolution:** Option A. Make findings-v2 the single contract with findings-v1 accepted as a strict subset, and give each lens its own severity vocabulary, category namespace and blocking predicate as data, keeping the native word next to the comparable one. Treat the five-tier core ordinal as a later design choice backed only by external context. Reject B because it leaves the nine literal copies and the opposite per-stack rules (D1, D5, D9) in place.

**Adversarial result:** n/a

### C-02: Anchor handling at merge, including the 200-character anchor drop (slug: anchor-handling-merge)

| Effort | Position | Evidence |
|---|---|---|
| E1 | v2 repeats the 12-200 limits for `anchor`, `anchor2` and citation `quote`; a citation whose path is not in the snapshot is kept as `unresolved`; `card_convert` truncates claims silently (no counter); an anchor-only finding is always a singleton cluster | `findings_v2.py:80,126,132,136`; `cluster.py:104-116,128-147`; `card_convert.py:85-86,199-201,303-311`; 01 §3.4, 03 §2.9 [CODE-VERIFIED] |
| E2 | Measured the loss and recommended "raise or truncate the 200-character anchor limit at merge, or instruct reviewers and re-validate" | E2 CR:292 and CR:371; 01 §11 [DOC-SOURCED; report text read at the commit] |
| E3 | v1 rejects anchor over 200, anchor2 over 200 and claim over 300; a missing anchor is kept with `span=None` and can open a blocking row; the installed experiment ledger has no length limits but refuses the whole input on a missing or ambiguous anchor | `findings.py:104,108,118,349-358`; `ledger.py:135-138,184-202`; `review_ledger.py:826-834,851-881`; 01 §10.2, §15 [CODE-VERIFIED] |

#### Option A: keep rejecting over-length fields, record every rejection, state the limits in every brief

**Description:** Leave the limits as hard errors; fix the surfacing and the briefs.
**How it works:** the merge stores, per reviewer, each rejected finding's id, line, reason and whether it was blocking; a PASS cannot be computed while a rejected line was blocking; the four limits come from one named constant and appear in every brief.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Low |
| Reuse of existing code | High: `parse_block` already keeps `{line,msg}` for every error (`findings.py:191`); `cluster_cmd` already persists `cards[].errors` (`cluster_cmd.py:161`) |
| Files/systems affected | `ledger.py` round entry and warning, `merge_cmd.py` output, brief files, tests `test_review_findings.py:113,117` stay green |
| Pros | Smallest change; keeps rejection semantics pinned by tests |
| Cons | Models measured to write long anchors (luna, ember, wonder) keep losing findings; depends on reviewers obeying a limit they have so far not been told |

#### Option B: truncate-prefix with a counter for length, reject only structural errors, flag missing anchors

**Description:** Over-length `claim`, `anchor`, `anchor2` and citation `quote` are cut to the limit (keeping the first characters so the quote stays locatable) and counted; types, enums, paths and ids stay hard errors; a missing anchor is kept but flagged and cannot block until verified.
**How it works:** `parse_block` returns `truncated: [{id, field, original_len}]` and the merge stores it beside the rejection record of Option A; a verification step (citation or anchor re-read) must confirm a finding before it can open a blocking row.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium (a truncated anchor is no longer an exact quote of the rest of the sentence; spans can widen clusters) |
| Reuse of existing code | High: `card_convert` already truncates claims (without a counter); `verify_cmd` already flags `quote-not-found` and `out-of-range` |
| Files/systems affected | `findings.py`, `findings_v2.py`, `card_convert.py` counters, `ledger.py`, `merge_cmd.py`; tests `test_review_findings.py:113,117` and `test_review_findings_v2.py:192-208,241-251` must change on purpose |
| Pros | Recovers all 48 length-rejected blocking findings in the measured set; loss becomes visible; keeps the exact-quote check for what is kept |
| Cons | Truncating the head only is safe for locating; truncating anywhere else is not; a limit-equality test is new work |

#### Option C: no length limits; refuse the whole input on any missing or ambiguous anchor

**Description:** The installed experiment ledger's policy: every input line is validated, any problem refuses the input and writes nothing.
**How it works:** `check_anchors` returns `E-ANCHOR` or `E-ANCHOR-AMBIGUOUS`; the caller re-asks the model.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | High (needs a retry loop with the model) |
| Reuse of existing code | Medium: `review_ledger.py:851-881` is installed only, not in `src/` |
| Files/systems affected | New retry step in every consumer; ledger input path |
| Pros | Nothing is silently lost or half-written; stops hallucinated anchors from blocking |
| Cons | Whether the long-anchor models would comply with a re-ask is untested (G-23); long anchors also make `same_defect` span overlap more likely (`findings.py:377`), widening D6 over-merge (01 §14.3) |

**Evidence:**
- All 49 lost blocking findings were rejected by D1 limits: 24 anchor over 200, 14 anchor2 over 200, 10 claim over 300, 1 refs; none by category or severity (`AD/flags.tsv` re-counted, 02 §4.2) [E2][E3] [CODE-VERIFIED against the committed outputs]. All dropped findings, blocking or not: anchor 56, anchor2 18, claim 14, bad severity 3, refs 1 (02 §4.2); per-model counts (luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1) are all findings, not blocking ones.
- Audit D names 3 flipped merges (not 4) plus 5 total-loss reviewer cases (02 §4.2) [E2] [DOC-SOURCED, outputs re-read]. The loss path runs through D3 (one valid reviewer is enough) because the round entry stores only `block_ok` and the first error message (`ledger.py:130-134,141-149`) [E3] [CODE-VERIFIED].
- No brief states all limits: the product brief omits the 300-character claim limit and the 8-ref limit (`document_review_loop_prompts.md:58-62`), the shadow brief omits quote 12-200 and refs 8 (`reviewer-spec.md:39`) (01 §5, §7, G-16) [CODE-VERIFIED].
- `card_convert` truncates without a counter, contradicting the research premise (D-01) [E1] [CODE-VERIFIED].
- A missing anchor is kept silently in v1 (D5, pinned by `test_review_ledger.py:408-417`), kept as an unresolved citation in v2, refused by the experiment ledger: three policies (01 §10.2 Key Takeaways).
- Truncating the head of an anchor keeps it a substring of the document; truncating elsewhere does not (01 §14.3) [CODE-VERIFIED reasoning over `locate`, `findings.py:276-304`].
- External context [web]: CodeQL's `primaryLocationLineHash` covers a fixed 100-character window of whitespace- and line-ending-normalised text (https://github.com/github/codeql-action/blob/main/src/fingerprints.ts) and web-04 recommendation R3 proposes truncate-to-window instead of reject; this is design support only.

**Status:** DECIDED-BY-EVIDENCE: the measured loss is almost entirely length rejection that no brief announced, which rules out silent dropping and favours Option B plus the rejection record of Option A over a refuse-and-re-ask loop whose compliance is untested.

**Recommended resolution:** Option B combined with Option A's persisted rejection record. Truncate-prefix with a counter for `claim`, `anchor`, `anchor2` and `quote`; keep structural rejections; persist id, reason and blocking flag for every rejected line; flag a missing anchor and keep it from blocking until a verification step confirms it; generate every brief's limit text from one constant.

**Adversarial result:** n/a

### C-03: Model and tier configuration, including gateway versus anthropic-only (slug: model-tier-config)

| Effort | Position | Evidence |
|---|---|---|
| E1 | Reflect's Stage 3 gate is an anthropic-only environment; reflect templates are checked by a code profile (no Fable, no tier0, at most 3 reviewers, `launch` must be sonnet, opus or haiku); resolution step passes `--env anthropic-only` explicitly | `panel.py:71-157`; reflect `SKILL.md:320,340`; 04 §1, §4.1 [CODE-VERIFIED]; the "Stage 3 gate" itself is MR:411 [DOC-SOURCED, scope slice 04 §0.1] |
| E2 | Raw gateway model ids passed per `claude -p` process; fallback ladder and exclusion list in bash; its default panel member `muse-ember-1.0` is not in the packaged tier file | E2 `run-reviewer.sh:5,23-43,69`; 04 §5, §4 [CODE-VERIFIED via `git show` and tier file] |
| E3 | Tier file with six gateway aliases, `classes` map and two environments; `gateway` has `launch: {}`; environment auto-selection reads `T3Model01` only | `review-tiers.default.json:4-36`; `panel.py:485-494`; 04 §4 [CODE-VERIFIED] |

#### Option A: the central panel targets anthropic-only (class launch values)

**Description:** Keep the reflect gate as the one supported cell; every consumer launches by class name (sonnet, opus, haiku).
**How it works:** `launch` stays a class name passed to the Agent tool; gateway templates run the legacy rotation with a recorded fallback reason (reflect rule D4).

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | Medium (the label is not true at serving time on this machine) |
| Reuse of existing code | Complete |
| Files/systems affected | None new |
| Pros | Works today for reflect; no fallbacks to debug |
| Cons | A "haiku" slot was served by `gpt-6.1-sol` on 2026-11-13 because `ANTHROPIC_DEFAULT_HAIKU_MODEL` points at the tier2 gateway alias; E2's best panels cannot be expressed; no fallback list exists in this environment |

#### Option B: the central panel targets the gateway with launch adapters and dated tier data

**Description:** Give the gateway environment real launch entries (raw id, alias or class) and treat tier lists as dated data.
**How it works:** `launch` becomes an adapter name plus argument; tier data carries a version, a date and the gateway it came from; missing models (`muse-ember-1.0`) are added or the E2 panels are declared out of scope.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | High (alias routing is runtime behaviour that changes with Coder and ccsession configuration) |
| Reuse of existing code | Medium: `select_env`, tier file schema, E2 ladder knowledge |
| Files/systems affected | `review-tiers.default.json`, `panel.py`, `panel_cmd.py`, golden fixtures, `ccsession-models.json` coupling |
| Pros | Lets the study's best-measured panels run; reflect templates can resolve in the gateway |
| Cons | Valid-era E2 evidence is one gateway on 2026-11-12/13 with documented misroutes; any tier-file byte change regenerates the packaged-tier golden |

#### Option C: environments as data, with the launch adapter and the allowed environments declared per consumer or template

**Description:** Both environments stay; each template or consumer states which environments it supports and which adapter launches each model.
**How it works:** the reflect profile becomes a data profile (max reviewers, forbidden classes, required classes, launch kinds); reflect declares anthropic-only; evaluation and tasklist templates may declare gateway; resolver validates that every alias a template needs exists.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium |
| Reuse of existing code | High: reflect profile (`panel.py:80-157`) generalises; D12 check is a small addition |
| Files/systems affected | `panel.py`, `panel_cmd.py`, tier file schema, templates, reflect tests `test_review_panel_reflect_profile.py` |
| Pros | Removes the hard-coded prefix rule; lets consumers differ; makes the D12 alias check possible |
| Cons | Does not by itself say which environment the first central consumers use |

**Evidence:**
- `superclaude review panel resolve --template @reflect-pre --env gateway` fails with "launch None is not one of sonnet, opus, haiku" (run 2026-11-13); no reflect template can resolve in the gateway (04 §4.1) [E1][E3] [CODE-VERIFIED by run].
- On this machine `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2[1m]` and tier2's first model is `gpt-6.1-sol`; combo runs A1-A2 and B1-B3 served the haiku slot with `gpt-6.1-sol` (04 §7.2; combo `results.md:33-38`, runs 2026-11-13) [E1] [CODE-VERIFIED for the tier list; routing is observed runtime behaviour].
- Anthropic-only has at most one model per tier, so every `fallbacks` list is empty there (04 §4.1) [CODE-VERIFIED by run].
- E2's replicated best panels use `muse-ember-1.0`, which appears in no alias, name or class (`review-tiers.default.json:4-23`) and would fail the reflect class rule (04 §4, §8) [E2][E3] [CODE-VERIFIED]. E2 default `ember + 2x luna` and its dated tier knowledge (2026-11-12/13) are [DOC-SOURCED].
- The packaged tier lists contradict E2's dated findings (Qwen and glm as tier3's only models; E2 excludes both from its ladder, `run-reviewer.sh:69`) (04 §8) [E2][E3].
- The environment gate and the owner's target environment are open owner items (O-2, G-32, G-33): runtime routing "can change with Coder/ccsession config" and must be re-probed [UNVERIFIED as stable].

**Status:** UNDECIDED-BY-EVIDENCE, resolved by adversarial debate (the underlying owner decision O-2 on the target environment stays open; the debate settled the design shape, not the owner's choice). Original reason: which environment the central panel must serve is an owner decision (O-2) that depends on runtime routing facts the code cannot settle, and the E2 results that favour the gateway were measured on one gateway on 2026-11-12/13 only.

**Recommended resolution:** Option A, anthropic-only with class launch values: the central panel launches reviewers by class name (sonnet, opus, haiku), because that is the only launch path an in-session Agent call can use today; gateway models are reached by binding a class to a model before the session starts, and the binding is recorded (`launch_binding`) in the run manifest. Taken from Option B into the merge: the launch grammar, minimal provenance with a coupling test, a command-layer slot with a drift check, a read-only `panel verify` (V3 warn-only), the completeness and backward-compatibility tests, and staged delivery. Gateway `launch` entries (B's headline) are NOT adopted now: B's own risk R1 concedes they describe a route no code runs. Merged text: `reviews/adversarial/model-tier-config/proposal-merged.md`. Not taken by this document: O-2 (the owner's target environment) and the open decisions listed below.

**Adversarial result:** winner A (Option A, central panel on anthropic-only with class launch); status `partial`, not a clean convergence. Reasons: base score 0.917 against B's 0.880 (margin 3.7%, inside the 5% tiebreaker band), so the debate decided it: A won 10 diff points outright and B none (7 merged, 4 ties, 4 unresolved); flipping the four position-bias disagreements ties the qualitative totals 24/24 and A still wins the tiebreaker; the debate confirmed three contradictions inside B and none inside A; A's class-launch path is the only one an in-session Agent call can use. Convergence 0.86 (25 of 29 diff points agreed) but BLOCKED_BY_INVARIANTS. Residual risks: INV-013 (HIGH, unaddressed): the default-environment flip alone does not change what the loop dispatches, because the loop prompt (`document_review_loop_prompts.md:70`) has no instruction to pass `model` from `launch` and reflect passes `--env anthropic-only` itself; INV-009 (HIGH, unaddressed): the rule "every Agent call carries `model == launch`" collides with reflect's shadow mode (dispatch is the legacy dispatch, so `panel_parity` would become true by construction); the merge proposes an engine-mode split that was NOT debated. Unresolved diff points: S-007, C-001, C-006, X-003. Open decisions in the merge: the payload rule for runs started before `launch_binding` existed; which count `reviewers_requested` records and which reviewers drop when fewer are effective than resolved; whether to confirm the INV-009 engine-mode split; O-2. Shared blind spots: both advocates used the same documentation fetches, E2 results were not re-read, and no in-session dispatch was observed. Process notes: diff analysis written in one write, no separate reviewer of the refactor plan (the merge-executor logged 10 plan inconsistencies PI-1..PI-10 in `merge-log.md`). Output: `reviews/adversarial/model-tier-config/adversarial/return-contract.yaml` and `reviews/adversarial/model-tier-config/proposal-merged.md`.

### C-04: Distinctness, strict versus soft (slug: distinctness)

| Effort | Position | Evidence |
|---|---|---|
| E1 | Opt-in `--strict-distinct` and `--hard-exclude-class` (drop a slot instead of repeating a model); reflect runs strict; the calibrator must come from a class disjoint from executor and reviewers (prose); `reflect-lite` documents a soft duplicate | `panel.py:519-543,631-635`; `review-panel.reflect-lite.json:5`; reflect `SKILL.md:1244-1258`; 04 §2, 05 §12 [CODE-VERIFIED] |
| E2 | One deliberate repeat is the only doubling effect that survived its tests ("second luna raises control found +0.83", Welch p 0.004, permutation p 0.048); the retracted stale text said a second run adds nothing; panels chosen by hand | E2 CR:297-298, CR:428; 04 §8 [DOC-SOURCED] |
| E3 | Default `distinct_across_slots: true` still re-admits the whole pool when a random slot is exhausted (D11); the golden fixtures pin the duplicates | `panel.py:536-543`; `test_review_panel_exclusion.py:56-72,208-213`; 04 §2, 12 §3.3 [CODE-VERIFIED by run and test] |

#### Option A: strict distinctness by default

**Description:** Make E1's `--strict-distinct` the default for every template.
**How it works:** `strict_distinct` is folded into `hard`, so an exhausted pool skips the slot and records `skipped_slots`.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium |
| Reuse of existing code | High: already implemented |
| Files/systems affected | `panel.py`; about 25 collected tests plus both goldens (`panel-golden-default-live7.json` 16 cases, `panel-golden-packaged-tiers.json` 2 cases) must change (12 §3.3, §9) |
| Pros | No silent repeats; matches reflect's anti-self-confirmation goal |
| Cons | `live7` collapses from 7 to 2 reviewers in anthropic-only with 5 skipped slots; E2's useful second `luna` is forbidden; strict mode still leaves fallbacks that other slots chose (04 §4 Key Takeaways) |

#### Option B: keep soft distinctness and only flag duplicates

**Description:** Models stay unchanged; the resolution record gains a duplicate flag.
**How it works:** `res["duplicates"]` lists repeated model ids with reviewer ids; only goldens and the "no extra keys" assertion (`test_review_panel_exclusion.py:72`) change.

| Aspect | Assessment |
|---|---|
| Effort | S |
| Risk | Low |
| Reuse of existing code | High |
| Files/systems affected | `panel.py` record, goldens |
| Pros | Smallest change; makes D11 visible |
| Cons | A repeat is still an accident of pool exhaustion, never an intended replica; a consumer cannot ask for "luna twice" |

#### Option C: declared per-slot distinctness policy with intended replicas

**Description:** A template states `distinct: none | model | class` per slot or per panel, plus an explicit `replicas` count; the record shows intended repeats separately from accidental ones; the decider or calibrator slot is always class-disjoint from the finders.
**How it works:** silent re-admission is removed (pool exhaustion either skips the slot or fails, per policy); fallbacks are filtered by the final chosen set; the reflect profile keeps `class` for deciders and strict for its finders.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium |
| Reuse of existing code | High: `resolve_slot`, `skipped_slots`, `excluded.classes` |
| Files/systems affected | `panel.py`, `panel_cmd.py`, template schema (`review-panel/1` slot keys are closed, `panel.py:46`), goldens and the tests of Option A |
| Pros | Expresses both E1's goal and E2's measured repeat; removes D11 as an accident; per-consumer defaults |
| Cons | Template schema gains optional keys; default policy per consumer is still an owner choice |

**Evidence:**
- D11 is reproduced: gateway `live7` gives `Qwen3.8-max` to both `t2b-1` and `t3-2`; anthropic-only `live7` gives six identical haiku reviewers (run 2026-11-13); `reflect-lite` soft gives sonnet, haiku, haiku (04 §4) [E3][E1] [CODE-VERIFIED by run]. The gateway `live7` golden holds `glm-5.3` twice (12 §5).
- Neither mode can express an intended replica: the record carries no duplicate flag, class or intended-versus-served field (`panel.py:666-681`) (04 §2) [CODE-VERIFIED].
- The control package's own resolution files contain duplicate models (Qwen3.8-max twice and glm-5.3 twice in live7), contradicting "duplicates not observed in the eval" (D-56) [E2] [CODE-VERIFIED via `git show`].
- E2 also measured a harm of more reviewers under a veto: `2x luna + 2x ember` adds 2.75-3.25 wrong blockers (p 0.005-0.03) (CR:298; 05 §11) [E2] [DOC-SOURCED, n=4-6]. Multiplicity caveat: the second-luna gain and this harm are two of 28 uncorrected p-values in the study (synth-01 Section 2), so neither is a sole basis for a decision.
- Class-disjointness is prose only in reflect; `panel.py` has no calibrator role and no class-distinct check on reviewers (05 §12) [CODE-VERIFIED].
- External context [web]: a panel of N LLM judges behaved like about 2 effective votes in one study, so label diversity does not guarantee independent errors (https://arxiv.org/html/2605.29800v1, preprint, May 2026); the Apollo Research finding that same-vendor judgments are highly correlated favours vendor- over class-level separation for the decider (web-03 §Key External Findings 3).

**Status:** split decision. (1) "Remove silent re-admission and declare distinctness per slot" is DECIDED-BY-EVIDENCE by code evidence alone (D11 reproduced; no duplicate flag in the record, `panel.py:666-681`). (2) "Declared intended replicas" is a design option, not a decided one: its only measured support is one E2 effect (second luna, Welch p 0.004, permutation p 0.048, n=4 to 6) among 28 uncorrected p-values in the study, so it rests on one uncorrected p-value pending replication (the evidence rule at the head of this file: a doc-sourced E2 number is never the sole basis of a decision); the code evidence shows only that the record cannot express a replica. The default per consumer stays an owner decision (G-11).

**Recommended resolution:** Option C. Declare distinctness per slot and remove silent re-admission (decided); record intended replicas as an optional slot field (design option, resting on one uncorrected p-value; the schema key is additive and costs little, and no replica is enabled by default); apply class-disjointness to the decider (calibrator or grader), not necessarily to the finders; choose strict for reflect finders and allow replicas for evaluation panels; add the missing optional slot keys as an additive schema change.

**Adversarial result:** n/a

### C-05: Who decides blocking: single veto, quorum, calibrator, blind grader or debate (slug: who-judges-blocking)

| Effort | Position | Evidence |
|---|---|---|
| E1 | Reflect decides by deviation class at contract level (Regression or Drift count above zero halts; Authorized and Necessary never do), degrades a single-reviewer merge and a convergence score below 0.80, and keeps the debate as merge; `cluster_v2` computes `support`, `disputed` and `blocking_any` but its cluster-level blocking is still a single-member veto | `contract.py:295-296,317-326,377-381`; `cluster.py:46-47,345-351,375-376`; 05 §1, §9 [CODE-VERIFIED] |
| E2 | Measured the single-reviewer veto: 65 judge-blocking catches against 38 real over 71 valid-era rows; `2x luna + 2x ember` gave 2.75-3.25 more wrong blockers (p 0.005-0.03); pilot arms had 0 of 8 blocking recall and a single reviewer passed both defect-rich packages | E2 CR:291, CR:298; E2 PR:71; 05 §11 [DOC-SOURCED: report text read at the commit; raw scores not re-aggregated, G-82] |
| E3 | Master ledger: any member's `blocking` flag sets the row and the verdict (`ledger.py:187,213-218,274`); installed experiments: a profile predicate (`review_ledger.py:41-49`) and a blind grader with canary claims under rubric B1-B3 that rejects "experts agree" as a reason (`stoprule.py:657-899`, `rubric.md:13`); the phase-5 bundle states no valid-success verdict | 02 §1.4, §6, §7; 05 §6 [CODE-VERIFIED for code; bundle outcome DOC-SOURCED] |

#### Option A: single-reviewer veto (current master and cluster behaviour)

**Description:** A cluster or row is blocking when any member is flagged blocking; the verdict is FAIL while one blocking row is open.
**How it works:** `blocking = any(m["blocking"])`; one non-blocking re-report can also un-block a matched row (`ledger.py:216-218`).

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | High (measured false blockers) |
| Reuse of existing code | Complete |
| Files/systems affected | None |
| Pros | Maximum recall; simple and deterministic; 0 invariant violations over 264 E2 merges (the rules are implemented faithfully) |
| Cons | 65 versus 38; adds blockers with each added reviewer; contradicts reflect's own rule that a single-reviewer outcome is degraded |

#### Option B: quorum (k of n distinct reviewers must flag the cluster)

**Description:** Count distinct reviewers per cluster and require k to flag it blocking.
**How it works:** `ledger._confidence` already computes overlap versus single; the verdict would read it; or use `cluster_v2.blocking_all`.

| Aspect | Assessment |
|---|---|
| Effort | S |
| Risk | High (may drop the few real blockers) |
| Reuse of existing code | High |
| Files/systems affected | `ledger.py` row decision, `test_review_ledger.py:128-129,277-304` |
| Pros | Directly removes uncorroborated blockers; no new model call |
| Cons | A few defects carry nearly all catches (B3 in 95 of 106 runs, I8 76, I2 71: CR:502), so a quorum may remove real singletons; 83 chained rows make counts noisy; the stoprule rubric states agreement is never a reason to block |

#### Option C: calibrator-weighted (block when `blocking_any` and support at or above a threshold)

**Description:** Use the blind calibrator's per-finding number and the cluster `support` as the decider.
**How it works:** a few lines on top of `_cluster`; threshold θ chosen from data.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium-High (no ground truth for any θ) |
| Reuse of existing code | High: per-finding calibration (142 of 142 in 13 shadow runs when the brief asks), `support`, `disputed` |
| Files/systems affected | `cluster.py`, calibrator agent and rubric, brief |
| Pros | All plumbing exists; one precedent threshold (Reuse-Miss needs confidence 0.85 and S_reuse 0.82, `SKILL.md:1176`) |
| Cons | Calibrator is a troubleshoot 6-dimension agent with no reflect rubric override; 0 of 689 legacy numbers; always `degraded` in anthropic-only; external evidence that verbalized confidence is weakly discriminative |

#### Option D: blind grader after clustering (a different model decides blocking per cluster under a frozen per-lens rubric)

**Description:** Reviewers propose; a separate blind agent decides blocking from quote, outcome and evidence only.
**How it works:** the installed `finding-grader` and stoprule batch logic are the template; the rubric is per lens (B1-B3 for spec text; deviation class for reflect-post).

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | Medium (accuracy unmeasured; rubric is spec-specific) |
| Reuse of existing code | Medium: the code is installed only in `~/.claude/` and the bundle, not in `src/` |
| Files/systems affected | New decider stage, rubric files, contract fields (a new `merge_method`/bump if used for reflect), `finding-grader` agent promoted into `src/` |
| Pros | Separates finding from deciding; explicit frozen criteria; canary claims detect a grader that ignores the rubric; production review systems separate finders from a coordinator that applies a rubric (external) |
| Cons | No accuracy measurement exists; under B1-B3 a pure Drift finding is not blocking while reflect halts on any Drift; validators are agreeable (true-negative rate below 25% in one external study) |

#### Option E: debate (sc-adversarial Mode A) with convergence routing

**Description:** Reflect's current merge: a debate over 2-3 cards, convergence 0.75 PASS, 0.60 PARTIAL, below FAIL.
**How it works:** `contract.py` degrades convergence below 0.80.

| Aspect | Assessment |
|---|---|
| Effort | L (already built; cost is run time) |
| Risk | Medium |
| Reuse of existing code | Complete for reflect |
| Files/systems affected | None for reflect; not reusable for ledger consumers |
| Pros | Legal under contract 1.8.0; convergence is surfaced, never PASS silently |
| Cons | Convergence was 1.0 in 9 of 14 recorded runs; whether that equals `cluster_agreement` shows nothing either way, because `cluster_agreement` is mostly the no-blocking-cluster default (1.0 in 11 of 14 recorded shadow runs for that reason, two null, shadow09 0.9328; synth-02 DOC-19), so the two figures are not shown to carry the same information; 6 of 14 merges were judged inline by the orchestrator and one had no debate artifacts; external study found debate amplified judge bias after the first round |

**Evidence:**
- The only decider with ground-truth evidence is the veto, and that evidence is negative on precision (65 versus 38; +2.75-3.25 wrong blockers) and gives no recall guarantee (0 of 8 in the pilot, 2026-11-11) (05 §11, §14) [E2] [DOC-SOURCED]. Wrong blockers on defect-rich packages include novel real finds, so those counts are an upper bound; the control package is the cleaner measure (05 §11) [E2].
- No ground truth exists for quorum, calibrated weighting, the grader or the debate. The Stage 0 "6.70%" is a descriptive overlap figure (24 of 358), not a correctness measure (05 §14; G-02 and closed item C-08 of the gaps log) [E1] [CODE-VERIFIED by re-reading `stage0a-report.md:293-297`]. Shadow runs have no ground truth: blocking findings scored higher (mean 0.80 versus 0.66, n=16 versus 126) but that is an association (05 §5.3) [E1].
- Three blocking rules coexist on master (reviewer consequence rule, label rule with `reflect_category`, deviation-class halting) and each lens uses a different one (05 §10, §13) [CODE-VERIFIED]; see C16 for the per-lens predicate.
- The experiment ledger's `PROFILES` and the stoprule grader are designs with partial runs: every completed loop in the phase-5 bundle ended FAIL or ESCALATE; no variant has a valid, repeated convergence result (02 §8; FINAL-REPORT.md:75,:103-107, dated 2026-11-08/09) [E3] [DOC-SOURCED].
- The recorded debate evidence: convergence 1.0 in 9 of 14 runs; 6 of 14 merges "inline orchestrator"; shadow09 had no debate artifacts and its convergence value equals its cluster agreement (07 §7) [E1] [CODE-VERIFIED in run files, 2026-11-13]. The earlier "`cluster_agreement` 1.0 in 10 of 11" is not used: the populations differ (11 runs in `stage0a-report.md:247-291`; 11 of 14 current shadow run files), and the 1.0 is mostly the no-blocking-cluster default, so equality of the two figures is uninformative either way (synth-02 DOC-19; `cluster.py:407-408`) [CODE-VERIFIED].
- External context [web]: union voting gave recall 82.7% at 85.0% false-positive rate against 37.7% recall for weighted voting (https://arxiv.org/html/2602.17875v1, preprint); a minority veto tuned on human labels was the best validator rule, and validators confirm far more than they reject (https://arxiv.org/html/2510.11822v2); 56.8% of confirmed defects were found by exactly one of fifteen model versions, so a hard quorum would drop real defects (https://zenodo.org/records/21328807, self-published, reliability low to medium); debate raised judge biases after the first round while a meta-judge resisted (https://arxiv.org/html/2505.19477v3, EMNLP 2025 Findings). Cloudflare and LinkedIn engineering posts describe a coordinator that deduplicates, verifies against source and applies a severity rubric before anything blocks (https://blog.cloudflare.com/ai-code-review; https://www.linkedin.com/blog/engineering/ai/high-signal-ai-code-review-that-adapts-to-your-codebase-at-scale). No external study of heterogeneous panels for defect-finding or specification review was found (web-03 §6.5).

**Status:** UNDECIDED-BY-EVIDENCE, resolved by adversarial debate (partial; the grader's accuracy is still unmeasured and 11 HIGH invariants remain open, so the merged proposal must not be built from yet). Original reason: only the veto was measured against ground truth, every alternative decider is unmeasured, and the external evidence points in several directions.

**Recommended resolution:** Option D, a blind grader after clustering, staged behind a replay gate: reviewers only propose, deterministic evidence checks run, and a blind grader decides blocking per cluster under a frozen per-lens rubric. It is introduced in shadow mode (it records its verdict next to the live decider) and goes live per lens only after a paired replay on the E2 ground-truth packages (3 packages, 16 defects) beats the veto on a threshold fixed before the run. The single-reviewer veto, with the hardening from A (a degraded marker on a PASS with fewer than two valid blocks and a singleton-blocker count, no contract bump), is the live decider until then and stays recorded as the control. The hardened veto is a target, not today's behaviour: what runs today is the unhardened veto. Reflect gets telemetry-only grading under contract 1.8.0 until a version bump. Reviewer overlap routes singletons to verification instead of dropping them. Merged text: `reviews/adversarial/who-judges-blocking/proposal-merged.md` (long; 23.5k words). Not decided by this document: the numeric replay threshold; which reflect-post predicate applies; whether a reflect-pre rubric ships; the claim-shape or `outcome` field; whether the other copies of the blocking rule (`diffgate`, `stoprule`) are in scope.

**Adversarial result:** winner B (Option D, blind grader after clustering, staged behind a replay gate); status `partial`. Reasons: A led the combined score (0.9091 against 0.8810), inside the 5% band, so the tiebreaker decided: B won 6 debate points to A's 2. The margin is narrow: on correctness criteria A scored 3/5 and B 1/5, so a reader who weights correctness higher would pick A. The debate settled that the unhardened veto is what runs today and the hardened veto is only a target; that the grader runs in shadow and goes live per lens after a paired replay (B already contained that rollout); and it overturned A's claim that no decider can add recall and B's claim that the design is fail-closed by construction. Convergence 0.909 (30 of 33 points with an agreed outcome; threshold 0.80) but blocked by the invariant probe; Round 3 does not run at standard depth. Unresolved diff points: C-005, C-012, X-002; shared assumptions A-001, A-003, A-007 are carried as accepted only with conditions. Unaddressed HIGH invariants (11): INV-001, 004, 005, 011, 014, 019, 020, 021, 023, 024, 025 (the probe also left 10 MEDIUM and 2 LOW). Residual risks: nobody has measured the grader's accuracy; an always-demoting grader would pass the replay's criterion and the replay has low power (INV-019, 022); the replay never exercises rounds 2 and 3 (INV-020); a PASS from a one-reviewer re-review is labelled certified by inheritance (INV-004). Not re-read by the debate: most cited code (about 20 line references spot-checked); the control-package numbers are advocate-computed and not re-aggregated. Process: the refactor plan had an independent reviewer (22 findings, all applied); Round 1 statements of the named advocates were extracted from their agent transcripts because they replied by mailbox. Output: `reviews/adversarial/who-judges-blocking/adversarial/return-contract.yaml` and `reviews/adversarial/who-judges-blocking/proposal-merged.md`.

### C-06: Calibration as a panel role and its rubric (slug: calibration)

| Effort | Position | Evidence |
|---|---|---|
| E1 | Each reviewer card is blind-calibrated by the `confidence-calibrator` agent; reflect says it re-grades "per the 5-dimension reflection rubric"; legacy cards carry 0 of 689 per-finding numbers; shadow cards carry 142 of 142 when the brief line asks for them | `SKILL.md:416,631,1240-1262,344`; `confidence-calibrator.md:48,61,67`; `stage0a-report.md:368-376`; 05 §2.5, §4, §5 [CODE-VERIFIED] |
| E2 | Not tested: the study ran reviewers and a deterministic merge only (no calibrator, debate or orchestrator) | 11 §6 last paragraph [DOC-SOURCED] |
| E3 | None in the master loop; the blind grader is a different mechanism (binary, per claim) | 05 §6 [CODE-VERIFIED for the installed agent] |

#### Option A: mandatory per-card blind calibrator as today

**Description:** Keep the calibrator as a required step for every reviewer card, with the existing agent.
**How it works:** class-disjoint calibrator per `SKILL.md` §11.3; one card-level number; per-finding numbers only when the brief asks.

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | Medium |
| Reuse of existing code | Complete |
| Files/systems affected | None |
| Pros | Plumbing works; blind and class-disjoint intent |
| Cons | The agent implements a 6-dimension troubleshoot rubric with a gated-minimum formula while reflect states a 5-dimension mean, with no `rubric_path` override anywhere in the reflect skill (D-28, [CODE-CONTRADICTED]); the disjoint set is empty in anthropic-only so the calibrator is always `degraded`, and `contract.py` never reads `calibrator_diversity` |

#### Option B: optional finding-level calibrator with its own rubric and explicit rubric path

**Description:** Keep calibration as an optional panel role whose output is a per-finding number used as a routing and telemetry signal (cluster `support`), not as the blocking decider.
**How it works:** a finding-level rubric file is passed by explicit path; the brief always asks for per-finding numbers; `review cluster` keeps reporting `calibration_coverage`; raw outputs are logged for later fitting; the decider role is settled in C05.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Low |
| Reuse of existing code | High: `cluster.py` support, `calibration_coverage`, agent frontmatter |
| Files/systems affected | `confidence-calibrator.md` or a new calibrator agent, reflect rubric text, shadow brief line, `SKILL.md` §11.3 class list (kimi and deepseek have no models) |
| Pros | Fixes the rubric mismatch; keeps the 142-of-142 coverage; no new claim of accuracy |
| Cons | Does not by itself improve blocking accuracy; the layout of the calibration block still varies (4 of 14 shadow runs unfenced) |

#### Option C: drop calibration and rely on agreement, deterministic evidence checks and a blind grader

**Description:** Remove the calibrator from the core.
**How it works:** support = number of distinct reviewers; evidence gate = citation and quote re-read; decision = per-lens decider (C05).

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium |
| Reuse of existing code | Medium |
| Files/systems affected | Reflect Waves 1D and 3C, `SKILL.md`, `reflect-reviewer`, `confidence-calibrator` |
| Pros | Removes a call per card; no dependence on weak verbalized confidence |
| Cons | Discards plumbing that works; reflect's tier routing (`C >= 0.90`, `C >= 0.85`) uses the number (`SKILL.md:431-437`) and would need a replacement |

**Evidence:**
- The rubric mismatch is code-visible: `confidence-calibrator.md:3,48,61,67` implements six troubleshoot dimensions and a gated-minimum formula; `reflection-rubric.md:11` is a five-dimension mean; dimension 3 uses an older class vocabulary (`reflection-rubric.md:39`) [E1] [CODE-VERIFIED] (05 §3, §4). Which rubric the recorded calibrators actually applied was never sampled (G-09).
- Calibrated `C` is a tier-routing input, not a per-finding gate; `calibrator_diversity: degraded` changes no verdict in code (05 §2.4, §2.6) [CODE-VERIFIED].
- 142 of 142 shadow findings were calibrated in 13 runs dated 2026-11-12/13; blocking findings scored mean 0.80 against 0.66 for non-blocking, but with no ground truth this is association, not accuracy (05 §5.2-5.3) [E1] [CODE-VERIFIED in run files].
- `confidence-calibrator.md:159` carries a placebo warning: a calibrated value within 0.05 of the inline one means the agent is not earning its overhead [E1].
- External context [web]: verbalized numeric confidence is overconfident and top-skewed, so a numeric per-finding calibrator should not be a required role; prefer agreement, deterministic evidence checks and a binary decision, with the calibrator optional and logging raw outputs (web-03 §Key External Findings 5 and Recommendation 1; Xiong et al., ICLR 2024; Ferrer et al., arXiv 2603.29559). The study found no evidence base for defect-finding panels, so this is extrapolation (web-03 §6.5).

**Status:** DECIDED-BY-EVIDENCE: the code shows the current calibrator is mis-specified for reflect and cannot decide blocking, while per-finding calibration is achievable and costs little; both facts favour Option B without needing the decider question settled.

**Recommended resolution:** Option B. Give the calibrator a finding-level rubric passed by explicit path, always request per-finding numbers in the brief, keep `support` and `calibration_coverage` as telemetry and routing signals, apply class-disjointness to the calibrator, and leave its use as a decider to C05.

**Adversarial result:** n/a

### C-07: How runs are recorded: manifest, telemetry, per-run files and audits (slug: run-recording)

| Effort | Position | Evidence |
|---|---|---|
| E1 | `review-panel-manifest/1`: nine ordered stages plus failed, hash chain, idempotent attempts, resume, publish commit point; attempt payloads stored only as a hash; agent-written `telemetry:` block in the contract; exit script as built-in checks; per-run USD only in an offline extractor | `manifest.py:38-53,331-386,402-470`; `reflect_shadow_exit.py:203-387`; `extract.py:42-81`; 08 §1, §9, §10 [CODE-VERIFIED] |
| E2 | Per-attempt `meta.json` (served model, `model_ok`, wall, output tokens), `cost.json`, free-text `fallback.log`, six after-the-fact audits of which A and D have summaries; audit A cannot be re-run from the committed tree | E2 `run-reviewer.sh:58,75-76,87`; `audit-A/summary.md:2`; 08 §7, §8 [CODE-VERIFIED via `git show`]; D-45, D-14 |
| E3 | `review-telemetry/1`: per-reviewer policy hashes, slot and fallback depth, three model identities, task descriptors, output counts, tokens and wall time, plus outcome scoring; no caller in `src`; strata fixed to sonnet and haiku | `telemetry.py:17-115,267-268`; 08 §3 [CODE-VERIFIED] |

#### Option A: the E1 manifest as the single run record, attempt payloads in E3's telemetry groups, E2 audits as built-in checks

**Description:** One manifest per run with a profile-specific stage list; each attempt stores model (resolved, launch, observed), slot, cost and exit; telemetry records are a projection of the committed manifest; audit checks run before `published`.
**How it works:** fallback hops become superseding attempts (`superseded_by` already exists); per-reviewer `findings_raw`, `findings_kept`, rejected ids and `report_sha256` are stored at merge; checks (observed equals launch, merged set equals resolved set, report hash unchanged, no silent blocking rejection, chain-size flag, cost sum) are evaluated before publish.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | Medium |
| Reuse of existing code | High: `manifest.py`, `telemetry.py` groups, `cluster.py` chain flag, audit A and D logic |
| Files/systems affected | `manifest.py` stage constants (fixed tuple, pinned by tests), `telemetry.py` strata, `merge_cmd.py`, reflect shadow steps, `reflect_shadow_exit.py` |
| Pros | Each effort supplies a missing third of the record; fixes the E2 `expected_model` overwrite and the first-error-only warning |
| Cons | `STATES` is pinned by tests and the reflect exit script; a failed manifest cannot be retried in the same `--out` today (`manifest.py:449-450`) |

#### Option B: keep three records and join them offline

**Description:** Leave E1 manifest, E2 files and E3 telemetry as they are; analysis scripts join them.
**How it works:** extractor scripts like `extract.py` read the outer session log and the run directory.

| Aspect | Assessment |
|---|---|
| Effort | S |
| Risk | Medium |
| Reuse of existing code | Complete |
| Files/systems affected | One extractor per consumer |
| Pros | No product change |
| Cons | Served model, per-reviewer cost and rejected finding ids stay outside the product record; per-reviewer cost cannot be separated when reviewers share a gateway alias (`extract.py:70-73`); audits stay hard-coded to `/tmp` paths |

#### Option C: adopt review-telemetry/1 as the only record and drop the manifest

**Description:** Write one telemetry record per reviewer run and per outcome; no stage manifest.
**How it works:** `telemetry append` after each merge.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | High |
| Reuse of existing code | Medium |
| Files/systems affected | `telemetry.py` (strata, money field, rejection counts, fallback chain, completion state, run link all missing), reflect shadow steps, exit script |
| Pros | Richest per-reviewer schema; separates intended from served model |
| Cons | Has no run-state, resume, publish guard or hash chain, which the shadow mode relies on; schema lacks money cost, dropped-finding ids and attempt count (08 §3 Key Takeaways) |

**Evidence:**
- No product record stores served model, per-reviewer cost or the ids of rejected findings: the manifest keeps attempt payloads only as a hash (`manifest.py:353`), the ledger keeps the intended model and a first-error warning (`ledger.py:130-134,141-149`), E2's records lose the intended model and miscount cost on fallback (`run-reviewer.sh:58,76,87`) (08 Summary) [CODE-VERIFIED].
- Audit D could only be built by replaying the parser because 45 merges' stdout was not kept (`AD/summary.md:26`, 02 §4.3) and audit A depends on attempt files that are not committed (G-39) [E2].
- The exit aggregator already is E1's built-in check set (parity recompute, MALFORMED rows, lint, manifest validation, EV-1 rate, verdict replay) but ignores cost, time and served identity (08 §9) [E1] [CODE-VERIFIED].
- `report_sha256` and `doc_sha256` in the ledger let audit D find 16 stale merges (02 §4.4) [E2][E3].
- Most audit checks need only data the product has or nearly has (08 §8.3 table) [CODE-VERIFIED reading]. The reflect `telemetry:` block is agent-written and values such as `cluster_agreement` are copies of code outputs that can drift (G-74).

**Status:** DECIDED-BY-EVIDENCE: the three records are each missing what another holds, and the code shows how the manifest, the telemetry groups and the audit checks fit together; no alternative covers the gaps.

**Recommended resolution:** Option A. Use the manifest as the run record with profile-declared stages and attempt payloads in the telemetry `model`, `slot` and `cost` groups, turn audits A and D and the shadow-exit checks into checks evaluated before publish (decision on warn versus fail per profile is G-76), emit telemetry from the committed manifest, and let the CLI, not the agent, copy summary fields into the contract.

**Adversarial result:** n/a

### C-08: Identity check, observed versus pinned (slug: identity-check)

| Effort | Position | Evidence |
|---|---|---|
| E1 | Identity is pinned: commit `9874d63fb` makes the card `model:` header copy the resolved pin and puts the harness model on an optional `model_observed:` line; `identity_source: observed` has no code; parity compares the recorded class lists with each other; served model is read only offline from the outer stream log | `SKILL.md:341,348`; `reflect_shadow_exit.py:117-177`; `extract.py:42-81`; 04 §6, §7 [CODE-VERIFIED] |
| E2 | Served model observed per reviewer from the top-level assistant events of the reviewer's own `claude -p` JSON transcript; `model_ok` is a hard gate with retries and a ladder; on fallback `expected_model` is overwritten with the ladder model and the ladder variable is never written | E2 `run-reviewer.sh:51-59,73-76`; 04 §5 [CODE-VERIFIED via `git show`] |
| E3 | `review-telemetry/1` already separates `resolved`, `launch` and `observed` and keys its scoring view on `observed`; nothing writes it | `telemetry.py:49,313-319,364-378`; 04 §6 [CODE-VERIFIED] |

#### Option A: pinned identity only (requested model plus self-report)

**Description:** Keep the resolver pin as the identity of record and compare self-reports.
**How it works:** card `model:` equals the pin by instruction; `panel_parity` compares records.

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | High (cannot see a swap) |
| Reuse of existing code | Complete |
| Files/systems affected | None |
| Pros | No transcript access needed |
| Cons | In the combo experiment (2026-11-13) a haiku slot served by `gpt-6.1-sol` and a collapse to one model were visible only in transcripts; parity was `True` in all three E-combo runs although only two distinct models served; self-reports named aliases 0 of 3 times |

#### Option B: observed identity as a hard gate (E2 style)

**Description:** Every reviewer must be observed serving the requested model or the run fails or retries.
**How it works:** needs `claude -p --output-format json` or stream-json access to each reviewer's transcript.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium |
| Reuse of existing code | Medium: logic exists in a bash runner; the E1 offline extractor does the sub-agent variant |
| Files/systems affected | Dispatcher, manifest attempts, exit script |
| Pros | Catches misroutes (E2 recorded muse misroutes on 2026-11-11 and 2026-11-12 and a glm misroute on 2026-11-12) |
| Cons | An in-session orchestrator has no tool that returns the served model of an Agent call (04 §7 Key Takeaways); whether `--forward-subagent-text` is required for sub-agent `message.model` to reach the parent stream is untested (G-38) |

#### Option C: record requested, launch and served separately; observe where the adapter can; redefine parity

**Description:** Store three fields per reviewer plus `identity_source` and a `fallback_chain`; the dispatcher enforces the pin; served model is `unknown` when no transcript is available; parity is retired or redefined as a record-versus-reality check where observed data exists.
**How it works:** fields go into the telemetry `model` group of C07; each fallback hop is a superseding attempt; the card `model:` header keeps the pin and `model_observed:` is consumed by a check.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Low |
| Reuse of existing code | High: telemetry group, manifest `superseded_by`, extraction code from both E1 and E2 (same method: assistant `message.model` from a stream transcript) |
| Files/systems affected | `manifest.py` attempts, `telemetry.py`, reflect shadow step 9, `reflect_shadow_exit.py` parity recompute, `SKILL.md` §4.3a |
| Pros | Honest about what is known; works for both dispatch modes; fixes the E2 overwrite |
| Cons | `unknown` served model weakens the independence claim until an adapter provides transcripts |

**Evidence:**
- Both E1 and E2 derive served identity the same way (assistant `message.model` from a stream transcript, top-level for `claude -p`, per parent tool-use id for sub-agents), so one method serves the core (08 §10 Key Takeaways; 04 §7.1) [CODE-VERIFIED].
- What the harness reports to an orchestrator is a gateway alias, not a served model id, so `model_observed:` usually holds an alias string and cannot reveal a Sol-for-Haiku swap (04 §7.3, troubleshoot report `REPORT.md:14`) [E1].
- Observed identity has no implementation in product code: `model_observed` occurs only in `SKILL.md:341` and `telemetry.py`; `reviewer_model_self_report` only in `SKILL.md` and `reviewer-spec.md:39` (04 §6) [CODE-CONTRADICTED for any reading that shadow observes identity] (D-20).
- Served-model drift hit all three efforts: E1 haiku slot to `gpt-6.1-sol` (2026-11-13); E2 misroutes (SPEC:82, :88, :117, 2026-11-11/12) [DOC-SOURCED]; E3 bundle: ponytail final review requested `claude-opus-5-5`, recorded `gpt-6.1-sol` (FINAL-REPORT.md:199, 2026-11-09) (11 §11) [DOC-SOURCED].
- Both E1 and E2 have a path where the stored "intended" value is rewritten to agree with something else (E1 card header := pin by instruction; E2 `expected_model` := ladder model by code) (04 §7.3) [CODE-VERIFIED].
- External context [web]: blinding must cover panel identity and file names, not only reviewer ids (arXiv 2611.01829 preprint; web-03 Key External Findings 2); vendor separation beats class separation for judges (web-03 finding 3).

**Status:** DECIDED-BY-EVIDENCE: pinned identity provably cannot detect the served-model changes seen in all three efforts, and a hard observed gate is not available to in-session dispatch; recording the three fields and observing where possible is the only option consistent with both dispatch modes.

**Recommended resolution:** Option C. Record requested, launch, served and identity source per attempt; enforce the pin at dispatch; observe from transcripts wherever the adapter provides them; redefine or retire `panel_parity` so it checks record against observation where available; keep fallback hops as attempts and never overwrite the requested model.

**Adversarial result:** n/a

### C-09: Dispatch of reviewers (slug: dispatch)

| Effort | Position | Evidence |
|---|---|---|
| E1 | Reviewers are in-session Agent-tool subagents of one fixed agent type (`reflect-reviewer`, frontmatter `model: sonnet`); the resolution is recorded but "dispatch is the legacy dispatch"; omitting `model` silently runs Sonnet; 6 of 9 tier3-orchestrated pilot runs collapsed to the Sonnet alias and combo A3 collapsed every reviewer and calibrator | `SKILL.md:342,646`; `reflect-reviewer.md:6`; combo `results.md:35`, `PLAN.md:66-69`; 04 §6, §7.2 [CODE-VERIFIED for the files; the pilot count is DOC-SOURCED from `PLAN.md`] |
| E2 | One fresh `claude -p --model <raw id>` process per reviewer in a sandbox, JSON transcript saved, fallback ladder in bash, no tier or class concept; Bash allowed under bypassPermissions | E2 `run-reviewer.sh:5,48,76`; 04 §5 [CODE-VERIFIED via `git show`] |
| E3 | The loop prompt says each reviewer runs in "a fresh context with the same brief" and gives no dispatch mechanism; a third, code-driven path exists in `ensemble.py` (in-process swarm calls over external `T2Model0N` models; tool-less reviewers that see only the tasklist text) | `document_review_loop_prompts.md:70`; `ensemble.py:154-182,619-630`; 13 §1.4, §10 [CODE-VERIFIED] |

#### Option A: in-session Agent dispatch with an enforced `model` argument

**Description:** Keep the Agent-tool route but make a missing or mismatching `model` a dispatch error.
**How it works:** the orchestrator must pass the resolver's `launch` value on every Agent call, for reviewers and calibrators.

| Aspect | Assessment |
|---|---|
| Effort | S |
| Risk | Medium |
| Reuse of existing code | High |
| Files/systems affected | reflect `SKILL.md` §4.3a, reviewer and calibrator agent definitions, a lint |
| Pros | Fixes the frontmatter-default collapse; read-only allowlist agents already exist |
| Cons | Cannot pass a raw gateway model id per reviewer; served model still only observable offline; enforcement remains prose followed by a model |

#### Option B: headless subprocess per reviewer (`claude -p`) with an allowlist and transcript identity

**Description:** Adopt E2's per-reviewer process as the standard.
**How it works:** raw id per process, JSON transcript, observed-model gate, allowlisted tools.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | Medium |
| Reuse of existing code | Medium: bash runner must be ported; the `cli/eval` harness has isolation, timeout and retry machinery (11 §7, [UNVERIFIED] for identity checks) |
| Files/systems affected | New runner module, sandbox creation, manifest attempts |
| Pros | Pins raw ids; transcript gives observed identity; clean isolation |
| Cons | Does not fit reflect's in-session consumers; E2's runner has defects to fix (attempt-file overwrite, `APIERR` loop condition, hard-coded paths) |

#### Option C: one dispatcher interface with adapters per environment

**Description:** The resolution `launch` names an adapter and an argument (`agent-class`, `cli-model`, `swarm`); the dispatcher enforces the pin and returns a transcript pointer when the adapter can.
**How it works:** reflect uses the agent-class adapter, the evaluation harness the cli-model adapter, the code-driven post-gate engine the swarm adapter until C17 replaces it.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | Medium |
| Reuse of existing code | High: resolver, E2 runner logic, swarm transports |
| Files/systems affected | `panel.py` launch schema (C03), a new dispatch module, reflect and tasklist skill text |
| Pros | Covers all three observed dispatch paths; makes the resolution the source of dispatch |
| Cons | Largest design surface; adapter default per consumer still depends on C03 |

**Evidence:**
- Resolution never drives dispatch on the skill path: step 3 says "dispatch is the legacy dispatch" (`SKILL.md:342`) and the resolver is a stdout tool that writes no file (`panel_cmd.py:108`) (04 §3, §6) [CODE-VERIFIED]. E2 bypassed the resolver entirely (04 §5); E3 follows it through prompt text only (04 §9). The highest-risk gap for any consumer is that "the resolution is not what runs" (04 §10 Key Takeaways).
- Dispatch collapse: a missing `model` makes the agent frontmatter default win (`reflect-reviewer.md:6`); combo A3 (2026-11-13): reviewers and calibrators all `(None, claude-sonnet-5-5)` (04 §7.2) [CODE-VERIFIED in `results.md`]. Whether the orchestrator model is the cause is a hypothesis (n tiny, `PLAN.md:66-69`).
- The recorded orchestrator for combo A was served by `glm-5.3` and `qwen3.8-max` on 2026-11-13, not by a Claude model, which also explains the speed and compliance leads better than "tier3" (11 §9) [E1] [CODE-VERIFIED in `logs/*.jsonl`].
- The third path, `ensemble.py`, is a tool-less swarm over `T2Model0N` models that ignores `executor_model_class` (13 §10 D3) [CODE-VERIFIED].
- E2 runner defects: attempt files overwrite across ladder hops; the `APIERR` loop condition differs between `:66` and `:73` (04 §5, G-39) [CODE-VERIFIED].

**Status:** DECIDED-BY-EVIDENCE: each mode has verified failures and each serves a different consumer or environment, so neither can be the single mechanism; the common requirement (the pin is enforced and the served model recorded) holds for all of them.

**Recommended resolution:** Option C as the target interface, with Option A's enforced `model` argument as the first step for reflect; the adapter default per consumer follows the C03 decision.

**Adversarial result:** n/a

### C-10: Brief and driving-document input contract (slug: brief-input-contract)

| Effort | Position | Evidence |
|---|---|---|
| E1 | The orchestrator writes a three-section brief (T1 excerpt, grounding hunks, coverage slice); the full spec body goes only to the `qa` persona; workflow sources are often one-line `source.md` files that delegate to another document, so `spec:N` citations point into the wrong text (W-3); 23 of 45 recorded briefs break the three-section shape and 0 of 45 carry the verbatim shadow line | `reviewer-spec.md:33-74`; 06 §2.1-2.4 [CODE-VERIFIED in the brief files, 2026-11-13] |
| E2 | The brief is a filled copy of the product first-review prompt and names only the candidate; `source.md` is shipped beside the candidate; 156 of 665 valid-era runs never referenced it (ember 81 of 209, luna 49 of 222, sonnet 1 of 63, terra 0 of 44); the causal link is an inference | E2 `run-reviewer.sh:9-17`; CR:373; 06 §3 [DOC-SOURCED for 156/665; brief text CODE-VERIFIED] |
| E3 | Five placeholders (`{{CANDIDATE}}`, `{{BASELINE}}`, `{{PRIOR}}`, `{{N}}`, `{{IDS}}`), none for a source; first review is "against the requirements it states"; the re-review step needs `diff -w` and `grep -nF` shell commands | `document_review_loop_prompts.md:17-21,32,44,46`; 06 §1 [CODE-VERIFIED] |

#### Option A: add `{{SOURCE}}` to the product prompt only

**Description:** Extend the E3 prompt's placeholder list and first-review sentence; leave reflect and E2 briefs alone.
**How it works:** the source clause goes inside the quoted brief line so `test_insertions_a_b_c_follow_their_brief_lines` (`test_review_rules_text.py:34-42`) still holds.

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | Low |
| Reuse of existing code | Complete |
| Files/systems affected | `document_review_loop_prompts.md`, `test_review_rules_text.py` placeholder pins |
| Pros | Fixes D8 for the spec loop and for the study's harness |
| Cons | Reflect and any other consumer stay with their own orchestrator-written briefs, which break the template in 23 of 45 recorded cases |

#### Option B: one code-rendered brief template with source, spec and grounding slots

**Description:** A single template rendered by code: Task, Inputs (role, path, sha256, line count, "injected" or "read it yourself"), Grounding hunks, Lens, Output contract (one constant for the findings-block line).
**How it works:** `{{SOURCE}}` (producer's snapshot), `{{SPEC}}` (referenced requirements document, resolved by the orchestrator) and `{{GROUNDING}}` (diff evidence, verification results, source hunks) are rendered; source is injected for every reviewer under a size cap (reflect's 400-line whole-file threshold is the precedent); `source_injected` and `source_read` are recorded per reviewer; shell evidence (diff, quote self-check) moves into the orchestrator.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | Medium |
| Reuse of existing code | High: reflect hunk shape, FR-4 verification-hunk pattern, `source`/`spec` roles already legal in the parser |
| Files/systems affected | `document_review_loop_prompts.md`, `reviewer-spec.md`, `reflect-reviewer.md` input list, `sc-workflow-protocol` Wave 4 (passes `source.md` as `--spec`), reflect C7 and C8 tests (`test_shadow_skill_contract.py:146-238`) |
| Pros | Removes the dependence on reviewer behaviour that 156 of 665 runs showed; the same brief serves reflect, tasklist, spec, PR and rf-qa consumers; source and spec become separate roles |
| Cons | Injection into every reviewer multiplies the source tokens by the reviewer count (reflect accepts roughly spec-length tokens for one reviewer, `SKILL.md:1717`); the cost was never measured (G-47); the C7 "exactly three sections" test must be retired in the same change |

#### Option C: keep per-consumer briefs and add a lint

**Description:** Leave briefs to each consumer; add a brief lint that requires a named source.
**How it works:** extend `BRIEF_SOURCES` in `test_review_prompt_overrides.py:61-63` to the reflect and tasklist briefs.

| Aspect | Assessment |
|---|---|
| Effort | S |
| Risk | Medium |
| Reuse of existing code | High |
| Files/systems affected | Lint tests |
| Pros | Cheap; catches template drift in tests |
| Cons | No code checks a produced brief today (grep found none), so a lint of template text cannot catch the orchestrator paraphrasing it |

**Evidence:**
- No brief in any effort names a driving document as a required input (06 Summary); every candidate carries `source: ./source.md` in frontmatter and body, yet the pointer plus a file on disk was not enough (06 §3.2) [CODE-VERIFIED for candidate lines; run counts DOC-SOURCED].
- The E2 judge never receives `source.md` (`judge-one.sh:13-16`) and the judge brief carries the combo name (`:21`), so it is blind to reviewer ids only (D-55) [E2] [CODE-VERIFIED via `git show`].
- Recorded E1 briefs show the shadow line moved to a fourth section in shadow10 and never verbatim in 45 briefs; a `gh issue view 357` execution instruction in shadow09 violates the live-execution prohibition `SKILL.md:305` (06 §2.4) [E1] [CODE-VERIFIED; briefs dated 2026-11-12 20:02 to 2026-11-13 02:35 UTC].
- Tier 2 was selected in 38 of 39 recorded non-shadow pre runs (11 §12), so the Tier 2 source-exposure rule applies to nearly every recorded run; the parsed-sparse flag was set in 35 of 39 and was not shown to be the cause (C-14 recount: decisive in 0 for certain and at most 1); R06 §2.3 marks its own count UNVERIFIED [E1] [CODE-VERIFIED in data for the counts].
- The E3 re-review prompt requires shell commands while reflect reviewers have no Bash; the diff evidence must be computed by the orchestrator (06 §4.2) [E3][E1] [CODE-VERIFIED].
- The reflect brief's role list says "plan or spec" while the parser has six roles including `source` (D-32) [E1] [CODE-VERIFIED].

**Status:** DECIDED-BY-EVIDENCE: the recorded briefs show that orchestrator-written text drifts from any template and that a pointer to the source is not an input contract; only a code-rendered template with recorded injection and reads removes the dependency. The all-reviewer injection default is a cost trade-off to measure (G-47).

**Recommended resolution:** Option B, with Option A's `{{SOURCE}}` change as its first deliverable. Separate the roles `source` and `spec`, add a grading clause for requirements the source states and the candidate drops, inject the source into every reviewer below a size cap, record `source_injected` and `source_read`, and move shell evidence into the orchestrator.

**Adversarial result:** n/a

### C-11: Reflect merge path and contract bump (slug: merge-path-contract-bump)

| Effort | Position | Evidence |
|---|---|---|
| E1 | Keep the `/sc:adversarial` debate as the reflect decider, contract 1.8.0 unchanged through Stage 4, a deterministic merge deferred to contract 2.0.0 ("E-prime"); the core may own resolution, cards, clustering, citation checks and manifests | Decision recorded as MR (merged requirements) via scope slice 04 §4.1 [DOC-SOURCED, not re-read, G-51]; `SKILL.md:87,311,837` [CODE-VERIFIED text] |
| E2 | Used the deterministic `superclaude review merge` only; no calibrator, debate or orchestrator was tested | 11 §6 [DOC-SOURCED] |
| E3 | Deterministic ledger merge with PASS/FAIL; plus a third code-driven reflect merge path, `ensemble.py`, that writes its own version-"1.0" contract | `ledger.py:107-298`; `ensemble.py:773,886-895`; 07 §8a, 13 §5.3 [CODE-VERIFIED] |

#### Option A: keep the debate for reflect, share everything else, make the merge step write its own verdict file

**Description:** No `merge_method` or contract change; the core owns resolution, cards, clustering, citation pre-check, calibration coverage and the manifest.
**How it works:** `sc-adversarial` or a small script writes `merged-verdict.yaml` with its own `merge_method`, read from the debate output and not assumed; this narrows the self-attestation but EV-1 remains an on-disk presence check (the writer can verify that the debate artifact files and at least 2 reviewer cards exist; 6 of 14 recorded debates were judged inline and shadow09 has no debate artifacts, so it is not proof that a debate ran in separate agents; open item Q-56 in synth-07); one code writer (a YAML serializer) writes the contract so `[1m]` aliases cannot break the parse; panel-only fields stay in the nested `telemetry:` block that the lint does not inspect.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Low |
| Reuse of existing code | High |
| Files/systems affected | reflect shadow step 7, `panel_lint._ev1`, contract writer, `reflect_shadow_exit.py` |
| Pros | Stays inside every constraint (C1-C4, C16); fixes three unparseable shadow contracts and narrows the self-attested EV-1 (it stays an on-disk presence check, Q-56) |
| Cons | Does not change how blocking is decided (C05); the debate stays as costly and as inline as recorded |

#### Option B: a script or grader merge with a new `merge_method` and a contract bump

**Description:** Replace the debate with the core's merge and decider.
**How it works:** a new legal `merge_method`, a version bump, new lint constants and wrapper logic, and a defined replacement for `convergence_score` and `user_decision_required` (both are defined on the debate's score).

| Aspect | Assessment |
|---|---|
| Effort | XL |
| Risk | High |
| Reuse of existing code | Medium |
| Files/systems affected | `SKILL.md` §9.1, `panel_lint.py` (L2, L3, bump rule B), `contract.py` version gate, `reflect_shadow_exit.py`, `reflect_verdict_replay.py` (both bound to "1.8.0"), tests `test_panel_contract_lint.py:184-201` |
| Pros | Removes the inline-orchestrator debate; one decider across consumers |
| Cons | A minor bump fails the lint, a major bump BLOCKS the wrapper (`contract.py:187-194`); a paired evidence run does not exist; the verdict replay compares reason sets, not paired verdicts |

#### Option C: deterministic merge now under contract 2.0.0

**Description:** E-prime from the staged plan, done immediately.
**How it works:** as B with a major version.

| Aspect | Assessment |
|---|---|
| Effort | XL |
| Risk | High |
| Reuse of existing code | Low |
| Files/systems affected | as B plus every consumer of the contract |
| Pros | Clean break |
| Cons | Every wrapper run BLOCKS until `contract.py` changes (`:187-194`); no measured quality case |

**Evidence:**
- A script merge is illegal for reflect under 1.8.0: "Reflect MUST NOT synthesize its own merge" (`SKILL.md:837`); EV-2 allows only `adversarial` and `single-reviewer-fallback`; `panel_lint` L3 and bump rule B turn any new value or top-level key into a failure (`panel_lint.py:184,326-334,360-365`) (07 §10 Q1-Q2) [CODE-VERIFIED]. The wrapper itself does not validate `merge_method` values (`contract.py:274-296`), so the rule lives in text and lint only (07 §3).
- EV-1 checks a file the orchestrator writes: `merged-verdict.yaml` is written in shadow step 7 (`SKILL.md:346`), while the installed `sc-adversarial` contract has no `merge_method` and no such file (07 §7.4-7.5) [CODE-VERIFIED against the installed skill text]. 6 of 14 recorded debates were judged inline by the orchestrator and shadow09 had no debate artifacts (07 §7) [E1] [CODE-VERIFIED in run files, 2026-11-13].
- Recorded debate convergence was 1.0 in 9 of 14 runs and the cluster number never varied, so the data cannot show the debate adds information over the script, nor that the script is as good (07 §10 Q1) [E1].
- Three shadow contracts (shadow04, 08, 09) are unparseable YAML because unquoted `[1m]` aliases break flow lists; the exit script counts them as "no contract" and EV-1 failures (07 §7.1) [E1] [CODE-VERIFIED by parsing].
- C1, C6 and C14 compare with HEAD, so they protect the contract only against uncommitted edits (07 §10 Q5); the gate procedure must run them before commit (12 §8 note) [CODE-VERIFIED].
- A third merge path exists: `ensemble.py` sets `merge_method` from the reviewer count (`ensemble.py:773`) (see C17).

**Status:** DECIDED-BY-EVIDENCE: the contract, lint and wrapper make Option A the only no-bump path, and nothing measured supports the quality of a replacement; replacing the merge is gated on the C05 decision and a paired evidence run, not on this conflict.

**Recommended resolution:** Option A. Keep the debate and contract 1.8.0; let the merge step write its own verdict file and `merge_method`; use one code contract writer with a YAML serializer; keep panel-only fields in the nested `telemetry:` block; run the HEAD-relative pins before committing; plan a contract bump only after C05 selects a decider and a paired legacy-versus-panel run scored against ground truth exists (G-57).

**Adversarial result:** n/a

### C-12: Clustering algorithm (slug: clustering)

| Effort | Position | Evidence |
|---|---|---|
| E1 | `cluster_v2`: path-aware citations resolved against a snapshot path list, fingerprint `v2\|role\|path\|\|refs\|class` with an always-empty section, `same_defect_v2`, transitive union-find, `chained` flag and calibrated `support`, telemetry only; AI-labelled pair sample precision 0.84 (21/25) and recall 0.95 (21/22) that excludes chained clusters and same-reviewer pairs | `cluster.py:104-181,302-378,381-433`; 03 §2, §6.3 [CODE-VERIFIED]; labels are AI labels, human labels pending (issues #525-#530) |
| E2 | Replayed v1 on real multi-reviewer output: 195 chained rows among 1,398 ledger rows in total, 144 of them wider than 60 lines, 83 mega-rows (8 or more members or 4 or more sections), up to 19 members across 8 sections | `AD/audit2.py:139-155`; `AD/summary.md:29`; 03 §7 [E2 replay is a line-for-line copy of `findings.py`, CODE-VERIFIED; the "of 1398" denominator is all rows (D-18)] |
| E3 | v1 `cluster`: fingerprint on section and refs, else shared or empty refs plus spans within 3 lines, transitive union-find, row keeps member 0's claim and category forever | `findings.py:340-407`; `ledger.py:181-238`; 03 §1 [CODE-VERIFIED] |

#### Option A: keep both clusterers (v1 for document loops, v2 for reflect)

**Description:** Status quo; each stack keeps its own location unit and rules.
**How it works:** v1 over one document text with diff-mapped spans across versions; v2 over citations in a snapshot.

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | Medium |
| Reuse of existing code | Complete |
| Files/systems affected | None |
| Pros | Each stack's tests stay green |
| Cons | Same transitive-closure weakness in both; opposite invalid-block policy; v2 is coarser than v1 (empty section merges equal-ref findings at any distance, and an all-fp cluster is never flagged chained); anchor-only findings can never cluster in v2 |

#### Option B: one clusterer on the v2 location model with complete-link admission

**Description:** One location type (list of role, path, lines, optional quote); an anchor-only finding is converted to a citation by locating its anchor in the role's snapshot file; a section or symbol is added to the fingerprint; ids come from a per-target grammar; a finding joins a cluster only if it matches every current member (or the representative).
**How it works:** reuse `findings.locate`, `findings.section_of`, `cluster._citation`; keep `chained` as a diagnostic; require stronger evidence for same-reviewer merges; no match on an empty location component.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | Medium |
| Reuse of existing code | High |
| Files/systems affected | `findings.py` (`refs_norm`, `_REF_TOKEN`), `cluster.py`, `telemetry.py:23-24` (copy of the same regex), `ledger.py`, tests pinned at `test_review_cluster.py:279-293,556,784-795` and `test_reflect_cluster_pairs.py:158-177` |
| Pros | Removes the measured over-merge class; fixes D7 for `T01.02` and the `D-P1` to `P1` extraction (W-2); gives v1 consumers multi-file citations |
| Cons | The `test_module_does_not_import_v1_cluster` pin breaks if `refs_norm` moves; no human-labelled pair set exists yet to score the change |

#### Option C: the same location model with centre-based assignment and a size cap with threshold escalation

**Description:** Instead of complete-link, a finding joins a cluster only if it matches the cluster representative; an oversized component is repartitioned by raising the match threshold.
**How it works:** v2 already computes a representative; the cap is derived from reviewers times lenses plus an allowance.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | Medium |
| Reuse of existing code | High |
| Files/systems affected | as Option B |
| Pros | Bounded growth even for a bad edge; cheap |
| Cons | A cap below the real maximum cluster size silently splits true clusters (one external preprint's K=5 failure); threshold escalation needs tuning data that does not exist |

**Evidence:**
- The two clusterers share transitive union-find and prose-harvested refs and differ in location model, invalid-block policy, fingerprint grain and representative choice (03 Key Takeaways, §8 Q1) [CODE-VERIFIED].
- v2's "section always empty" merge: equal non-empty ref set, same class and same primary path merge at any line distance, and such a cluster is never labelled chained (03 §2.8) [CODE-VERIFIED]. An anchor-only finding is always a singleton (`cluster.py:128-147`; pinned by `test_review_cluster.py:279-293`) [CODE-VERIFIED].
- `_REF_TOKEN` matches letters-hyphen-digits and `P1`-`P9` only: `T01.02` and `AC-T01.02-3` give no refs, `D-P1` yields `P1`, `P12` yields nothing (probe run 2026-11-13, 03 §5.2) [CODE-VERIFIED by execution]; the same pattern is copied at `telemetry.py:23` (03 §5.1).
- The 0.84 / 0.95 figures are AI-labelled, from the same model family as the clusterer, and exclude the chained and same-reviewer pairs that were the dominant failure in E2 (03 §6.3) [E1]; the 6.70% figure is an overlap figure only (closed item C-08).
- E2's replay counted 83 mega-rows under v1; the numbers describe v1 and are the expected failure class of v2, which flags but keeps chains (03 §7 Key Takeaways) [E2][E1]. How far the study's per-panel catch numbers moved because of chaining was not quantified (03 §7.3).
- External context [web]: single-linkage chaining is a documented general failure and complete linkage, centre-based assignment, size cap with threshold escalation and correlation clustering are the documented remedies; the transitive-closure baseline had 64% precision against 97% for pairwise matching in one entity-resolution paper (different domain) (web-04 §C1-C3; https://pmc.ncbi.nlm.nih.gov/articles/PMC4849582; http://www.vldb.org/pvldb/vol2/vldb09-1025.pdf); mature trackers gate matching on equal rule or category and refuse to merge on an empty location (web-04 R4, R5).

**Status:** DECIDED-BY-EVIDENCE: the measured over-merge (83 mega-rows) and the verified v2 gaps rule out Option A, and the options that remain differ only in the remedy used against chaining, which is a tuning step with a stated acceptance metric rather than a disagreement between the efforts.

**Recommended resolution:** Option B as the baseline: one clusterer on the v2 location model, an anchor-to-citation step, section or symbol in the fingerprint, a per-target id grammar imported once, no merge on an empty location, same-reviewer merges needing stronger evidence, and complete-link admission; adopt Option C's cap only as a safety net sized from reviewers times lenses. Accept it when the 83-mega-row count falls and the human pair labels (issues #525-#530) confirm precision, including chained and same-reviewer pairs.

**Adversarial result:** n/a

### C-13: Ledger model, re-find and cluster versus find-once verify-only (slug: ledger-model)

| Effort | Position | Evidence |
|---|---|---|
| E1 | No ledger for reflect: reflect is single-pass, the ledger is path-blind (bare span, one `doc_sha256` per round) and `--cap 1` would record ESCALATE every blocking round | MR:273 [DOC-SOURCED via scope slice 04 §0.1] |
| E2 | First reviews only: no evidence about rounds 2-3, D2 or D16; the merge worked as designed (blocking equals any member, 0 violations over 264 merges) | `AD/summary.md:3,33,34`; 02 §4.4 [DOC-SOURCED, outputs re-read] |
| E3 | Master ledger re-parses and re-clusters every reviewer report every round (`ledger.py:127-171`); installed experiment: find once at review 1, then reviewers answer a plan of existing rows and add new rows only in changed hunks, clearing needs an evidenced `resolved` answer, caps refuse (`review_ledger.py:912-937,1300-1311,1633-1795`); installed stoprule: sealed claim ledger, priors and baseline, "silence never passes" | 02 §1, §6, §7 [CODE-VERIFIED for code] |

#### Option A: re-find and cluster every round (master ledger) with D2, D3 and D16 fixed

**Description:** Keep `merge_round` as the engine; fix clearing, minimum valid reviewers and the cap.
**How it works:** invalid reviewers cannot clear a `resolved_check` row; a round refuses when no quorum of valid blocks exists; round above the cap is refused; `--cap` on an existing ledger is an error.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium |
| Reuse of existing code | High: `ledger.py`, `merge_cmd.py`, `ledger_cmd.py`, exit codes 0/10/11 |
| Files/systems affected | `ledger.py`, `merge_cmd.py`, `test_review_ledger.py:376-385,408-417,518-544` |
| Pros | Works with multi-reviewer panels and the v2 clusterer; code and tests already exist |
| Cons | Every round re-finds, so late findings can keep a loop open (E3 bundle: every loop ended FAIL or ESCALATE, 2026-11-08/09, n=1-2 per arm); the loop prompt's "verify-only" is prompt text, not a code mode (D16c) |

#### Option B: find once, then verify-only (the experiment ledger design)

**Description:** One panel finds at review 1; later reviews only answer the plan and report new defects inside changed text.
**How it works:** frozen fields, `E-INCOMPLETE` if a plan row is unanswered, evidence quotes must occur in the new snapshot, out-of-hunk new rows are stored deferred.

| Aspect | Assessment |
|---|---|
| Effort | XL |
| Risk | High |
| Reuse of existing code | Medium: `review_ledger.py` (2,668 lines) is installed only, not in `src/`, and has no multi-reviewer merge or clustering |
| Files/systems affected | New code in `src/`, `ledger_cmd.py`, the spec-panel prompts and their text pins (`test_review_loop_extension.py:120-127`) |
| Pros | Fixes D2 (positive clearing), D16a (refusal) and D16c (code mode) by design; late findings cannot reopen a loop |
| Cons | Single-input design; whether models comply with a plan-answer protocol on rounds 2-3 is untested; the bundle shows no valid-success verdict |

#### Option C: hybrid, multi-reviewer find in round 1 with the unified clusterer, verify-only later rounds with evidenced clearing and refused caps

**Description:** Combine A's panel merge for the first review with B's verify-only protocol and refusal semantics for rounds 2-3.
**How it works:** round 1 uses the unified clusterer and the C05 decider; later rounds use one anchor reviewer (the packaged templates already resolve one fixed reviewer for a re-review, `panel.py:600-605`) answering the plan; one re-review protocol (prior lines or answers, G-18) is kept.

| Aspect | Assessment |
|---|---|
| Effort | XL |
| Risk | High |
| Reuse of existing code | Medium |
| Files/systems affected | as A and B |
| Pros | Uses each design where its evidence is strongest (E2 measured round 1 multi-reviewer; the experiment designs rounds 2-3) |
| Cons | Largest design; both halves unmeasured in combination |

**Evidence:**
- D2, D3, D16 confirmed at current lines: clearing never reads `block_ok` (`ledger.py:254-258`, docstring `:112` contradicted); a round passes on one valid reviewer (`:150-157,273-274`); round 4 is accepted and `--cap` is ignored on an existing ledger (`:114-118`; `merge_cmd.py:101-104`); `test_review_ledger.py:376-385` pins D2 and D3 together (02 §1.4, §3) [E3] [CODE-VERIFIED].
- The experiment fixes D2, D4, D16a and D16c by design but has no multi-reviewer merge at all, and its all-or-nothing input refusal needs a retry loop (02 §6.2 Key Takeaways) [E3] [CODE-VERIFIED].
- No effort has evidence for rounds 2-3 under a multi-reviewer ledger: E2 ran round 1 only; the #346 loops were single-session; the bundle states "Convergence not proven; no validated winner" and every completed loop ended FAIL or ESCALATE (FINAL-REPORT.md:42,75,103-107, dated 2026-11-08/09) (02 §8, G-22) [E2][E3] [DOC-SOURCED].
- Only one re-review protocol is in code per stack: v1 prior lines (`findings.py:175-187`; rejected by v2 at `findings_v2.py:279-283`) versus the experiment's `fixed/not-fixed/disputed` answers (`review_ledger.py:65`) (01 §18 item 9) [CODE-VERIFIED].
- rf-qa adds monotonicity and regression halts that the ledger stop rule lacks (`rf-qa.md:403-418` against `ledger.py:93-104`) (10 §6) [ext] [CODE-VERIFIED].
- External context [web]: LinkedIn verifies singleton findings instead of dropping them; Cursor's pipeline also dedupes against bugs posted in earlier runs, the same job as cross-round row matching (web-01 §3.1, §3.3). These support carrying rows across rounds but do not choose between A, B and C.

**Status:** UNDECIDED-BY-EVIDENCE, resolved by adversarial debate (partial and narrow; no measured evidence separates the two designs, and ten HIGH invariants were never debated). Original reason: the deciding behaviour (rounds 2-3 with several reviewers) was never run by any effort, and the only loop-level evidence shows every variant ended without a clean PASS.

**Recommended resolution:** Option B, find once then verify-only (the experiment ledger design: only round 1 searches the whole candidate; rounds 2 and 3 answer the plan rows with an evidence quote from the new text and report new defects only in changed hunks), reached through a staged hybrid that both advocates ended on: Stage 0 applies Option A's fixes to the master ledger first (cap by refusal, `--cap` conflict error, quorum of valid blocks, atomic refusal); a decision gate then chooses between "A plus fixes" and the verify-only port, using a pre-registered falsifier run of B against A. The merged text argues both sides at the gate. Merged text: `reviews/adversarial/ledger-model/proposal-merged.md` (about 24,000 words; start at its "Open decisions and unresolved conflicts" section). Not decided by this document: the gate's choice; OD-1 to OD-11 in the merged proposal; one flagged-but-unapplied item (where `refusals[]` lives when a round-1 refusal happens before any ledger exists).

**Adversarial result:** winner B (Option B, find once then verify-only), narrowly; status `partial`. Combined score B 0.9804 against A 0.9724 (margin 0.8 points), decided by the tiebreaker, 14 debate points won against 10; counting only the 32 non-structural points it flips to A 10, B 9, so the selection is narrow. Reasons: B's evidenced clearing, frozen blocking and row identity beat A on the correctness points, and A's advocate conceded those (a lone reviewer's silence clears a row in A, and A's own cap and quorum fixes do not change that); A won on shippability and compatibility (the cap and `--cap` fixes, `review merge` compatibility, late findings kept visible) and B's advocate conceded those; both advocates ended on the staged hybrid. Convergence 0.89 (33 of 37 points agreed, only 24 on a single variant), BLOCKED by the invariant gate. Unresolved diff points: S-006, C-013, A-002, A-004 (the merge keeps both advocates' final positions for each). Unaddressed HIGH invariants (10, INV-001 to INV-010; never debated because depth standard has no Round 3): `defer` rewrites a FAIL to PASS (`ledger.py:350-360`, INV-001); a refusal that records nothing cannot also bound retries (INV-002); a `prior` line of status `open` would clear a row (INV-003); a second `ledger revise` corrupts spans (INV-006); a spanless row can never clear (INV-008); the numbering is that of `reviews/adversarial/ledger-model/adversarial/invariant-probe.md`. No measured evidence separates the two designs. Process: the first Variant A Round 1 advocate never returned and was replaced once (its statement reached the main session and was relayed through a file); the plan reviewer's 21 findings were all applied; `fallback_mode` false. Output: `reviews/adversarial/ledger-model/adversarial/return-contract.yaml` and `reviews/adversarial/ledger-model/proposal-merged.md`.

### C-14: Panel size versus cost: fewer reviewers by default, or fix the rubric first (slug: panel-size-cost)

| Effort | Position | Evidence |
|---|---|---|
| E1 | Reflect templates are capped at 3 reviewers (`_REFLECT_MAX_REVIEWERS = 3`); raising the cap needs Tier 2 recall at least 15 percentage points above Tier 1 (H-A); Tier 2 is the typical path: MR:142 says 37 of 38 recorded pre runs escalated, 34 by the parsed-sparse pre-filter; the 2026-11-13 recount over the 39 non-shadow `tier_decision.yaml` files found 38 of 39 selected Tier 2, the flag set in 35 of 39 (34 of the 38 Tier 2 runs) and decisive in 0 for certain and at most 1, so the cost driver is not established (the "34 by the pre-filter" attribution is superseded); H-A is unmeasured (pilot designed, not run); open item O-8 says the rubric may be the cheaper lever | `panel.py:73`; MR:142, MR:527, MR:556 [DOC-SOURCED, via scope slice 04 §0.1]; recount [CODE-VERIFIED in data] (11 §12) |
| E2 | Every replicated panel found about 1.6-2.5 of 14 known defects per run as scored ("all panels sit at about 2-2.5 of 14", CR:428); no panel was significantly better (three-way permutation p 0.54-1.0) while tokens differ (p 0.002-0.009); `2x luna + 2x ember` added 2.75-3.25 wrong blockers; two-reviewer panels (ember + sonnet 2.50, ember + luna 2.25, n=4 each) scored as high as three-reviewer panels; the pilot line "sonnet alone gives the most catches per token" was one run per package on 2026-11-11 | E2 CR:298, CR:315-333, CR:381, CR:428; E2 PR:48-50; 11 §6, §12 [DOC-SOURCED; raw scores not re-aggregated, G-82] |
| E3 | The packaged default template has four reviewers (t1b one, t2 one, t3 two) and `live7` has seven; the review loop prompt says one reviewer for a re-review | `review-panel.default.json:9-11`; `review-panel.live7.json:9-13`; 04 §4 [CODE-VERIFIED] |

#### Option A: default to fewer reviewers (two) now

**Description:** Set the default panel to two reviewers for reflect Tier 2 and the new consumers.
**How it works:** templates with two slots (a fixed anchor plus one diverse reviewer).

| Aspect | Assessment |
|---|---|
| Effort | S |
| Risk | High (unmeasured in reflect) |
| Reuse of existing code | High: templates are data |
| Files/systems affected | Reflect templates, `reflect_shadow_exit.py` shortfall rule (`reviewers_resolved == 3 and reviewers_complete == 2`), `SKILL.md` §7.1 rotation (N=2 is already a hard floor, `:648`) |
| Pros | Cheapest per run; E2's two-reviewer panels matched three-reviewer ones in its setting |
| Cons | The study never ran reflect, a calibrator or a debate, so its ceiling is not the Tier 2 ceiling; 2 versus 3 reviewers inside reflect is not measured anywhere; the second reviewer is the largest coverage step in one external corpus |

#### Option B: fix the rubric first (O-8), keep the cap at 3, decide the count after H-A

**Description:** As drafted for the debate: stop the parsed-sparse pre-filter from forcing Tier 2 for workflow packages that carry no labelled requirement ids; keep three reviewers when Tier 2 runs; measure before changing the count. (After the recount the rubric edit is a hypothesis, not the measured cost lever: the flag was decisive in 0 for certain and at most 1 of 39 runs. The merged design records the escalation rows first and keeps the pre-filter unchanged unless those keys show it decisive; see the Recommended resolution.)
**How it works:** change the escalation inputs (`SKILL.md:284,443`) so format alone does not escalate; run the seeded-defect pilot (H-A) and a rubric-change miss-rate check using the E2 harness as the instrument.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium (missed defects after the rubric change are unmeasured) |
| Reuse of existing code | High |
| Files/systems affected | reflect `SKILL.md` §5.3 and Step 1B.2b, `tier_decision` fields, consumers that reach Tier 2 by default (workflow Wave 4, tasklist Stage 10.5) |
| Pros | Needs no reviewer-count decision; consistent with the cap of 3; the cost lever is a hypothesis to test (the flag was set in 35 of 39 runs but decisive in 0 for certain and at most 1; 29 of the 34 flagged Tier 2 runs also have a recorded escalate row 4, 5 or 6) |
| Cons | The rubric edit would change the tier of at most 1 of 39 recorded runs, so the saving is small or nil; how many plans would then be wrongly stopped at Tier 1 is not measured |

#### Option C: keep the status quo (Tier 2 almost always, three reviewers) until H-A is measured

**Description:** Change nothing; wait for the pilot.
**How it works:** none.

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | Medium (continued cost) |
| Reuse of existing code | Complete |
| Files/systems affected | None |
| Pros | No unmeasured change |
| Cons | Pays Tier 2 on 38 of 39 recorded plans; the cause is not established (the parsed-sparse flag was set in 35 of 39 but decisive in 0 for certain and at most 1; rows 4, 5 and 6 are recorded for 29 of the 34 flagged Tier 2 runs); the shadow Stage 2 exit is already FAIL |

**Evidence:**
- Tier 2 is almost always selected, and the cause is not established: 38 of 39 recorded non-shadow pre runs selected Tier 2; the parsed-sparse flag was set in 35 of 39 (34 of the 38 Tier 2 runs) and was decisive in 0 for certain and at most 1; 29 of the 34 flagged Tier 2 runs also have a recorded escalate row 4, 5 or 6 (debate recount of 2026-11-14, `reviews/adversarial/panel-size-cost/adversarial/return-contract.yaml`; the counts supersede MR:142's 37 of 38 and 34, and the older "driven by the flag" conclusion is not carried, D-59) [E1] [CODE-VERIFIED in data, model-written fields] (11 §12; `reviews/adversarial/panel-size-cost/proposal-merged.md` E-5).
- Beyond three reviewers there is no recall gain and more wrong blockers in E2's setting (CR:298, CR:381; one gateway, n=4-6 per panel, 2026-11-12/13); a replicated two-reviewer panel matches the three-reviewer ones there (11 §12) [E2] [DOC-SOURCED].
- Not measured anywhere: Tier 2 versus Tier 1 recall (H-A), two versus three reflect reviewers, and the miss rate after a rubric change (11 §12 items 3-4; G-57, G-59) [E1][E2].
- "Sonnet alone gives most catches per token" holds only for the pilot comparison (arm A 2/16 at 93,098 tokens, one run per package, pre-source era, 2026-11-11); valid-era tables show cheaper panels with more catches per 100k tokens (ember + luna 4.29, ember + 2x luna 2.88), so it must not be carried as a current fact (D-57) [E2] [DOC-SOURCED].
- Reflect's own reviewer-count conflict: `--reviewers` accepts up to 4 (`config.py:335`) against constraint C11 (at most 3) (G-67) [CODE-VERIFIED].
- Shadow-run cost is only estimated: combo runs spent 185,086-367,381 output tokens per whole run for combos B-E (results.md:8-19, 2026-11-13); estimates, "do not compare" (11 §12 table) [E1].
- External context [web]: a self-published corpus found the second reviewer is the largest coverage step and returns diminish after two to three (https://zenodo.org/records/21328807, reliability low to medium); one study of nine judges found about 2 effective votes (https://arxiv.org/html/2605.29800v1); web-01 recommendation 9 states three heterogeneous reviewers plus one adjudicator as the evidence-supported size.

**Status:** UNDECIDED-BY-EVIDENCE, resolved by adversarial debate (partial; the quality side of every option stays unmeasured). Original reason (as drafted before the recount; the recount removes the cost-side claim, because the flag was decisive in 0 for certain and at most 1 of 39 runs): the quality side of every option (T1 versus T2 recall, 2 versus 3 reflect reviewers, miss rate after a rubric change) was never measured, and E2's ceiling comes from a setting without calibration or debate.

**Recommended resolution:** Option B as merged, in three steps (`reviews/adversarial/panel-size-cost/proposal-merged.md`). Step A (no behaviour change, no model cost): record the escalation rows and the calibrated confidence at decision time (audit-only keys in `tier_decision.yaml`) and run a read-only recompute check; the parsed-sparse pre-filter stays unchanged unless those keys show it decisive (Conditional item CI-1, not committed scope, because the flag was decisive in 0 for certain and at most 1 of 39 runs). Step B (owner-gated): Decision D-1, a skill-path default of two reviewers (9 of 38 recorded Tier 2 runs already ran two cards), carried from Option A as a narrowed "A-min", with the cap kept at 3. Step C (measurement): decide the count after H-A, with three pinned arms and a symmetric pre-registered rule. B's recount and exposure map also survive; B's Phase 1 (making the parsed-sparse flag advisory) is demoted to CI-1. The earlier recommendation "fix the rubric first" is not carried. Not decided by this document: D-1 itself, the tripwire numbers, the task-builder gate option, the H-A pilot owner.

**Adversarial result:** winner B (Option B, fix the rubric first), by tiebreaker only: B 0.9256 against A 0.9194 (inside the 5% band), debate points won B 6 to A 4. Status `partial`: convergence 0.80 (24 of 30 diff points, exactly at the threshold) BLOCKED by three HIGH unaddressed invariants. Both advocates' Round 2 consensus favoured a narrowed "A-min" base, which the merged proposal carries as owner-gated Decision D-1. Escalation figure after the check (the debate recounted the 39 `tier_decision.yaml` files with its own script): the parsed-sparse flag was set in 35 of 39 non-shadow runs (34 of the 38 Tier 2 runs) and was decisive in 0 for certain, at most 1; A's "35 of 39 escalate because of the flag" and B's "1 certain, at most 5" are both overstated; 29 of the 34 flagged Tier 2 runs have a recorded escalate row 4, 5 or 6, and B's clear-cut flag-only run has its own calibrated C of 0.68, so it escalates through row 6 anyway. Residual risks: INV-009 (HIGH): the rollback tripwire cannot observe the legacy path; INV-012 (HIGH): the task-builder default POST gate is a blocking consumer that passes no `--reviewers`; INV-013 (HIGH): the prospective audit keys are model-written; seven MEDIUM invariants unaddressed (INV-001, -002, -004, -006, -008, -010, -011); nothing measures two against three reviewers inside reflect; E2 does not transfer; N=2 loses PASS-eligible slack. Unresolved diff points: S-002, S-006, C-003, C-010, C-013, C-016. Open owner decisions: accept D-1 before H-A; tripwire numbers; task-builder gate option (a) pass `--reviewers 3` (the debate's recommendation) or (b); the H-A pilot owner (G-59); who closes G-67 (C17); the margin of the count rule; whether a fourth reviewer class is added instead of cutting N. Not checked by the debate: recall at two versus three reviewers, token savings, why 5 of the 9 two-card runs had two cards; only 7 of 39 `tier_decision.yaml` files record `S_domains`; no Round 3 at depth standard. Output: `reviews/adversarial/panel-size-cost/adversarial/return-contract.yaml` and `reviews/adversarial/panel-size-cost/proposal-merged.md`.

### C-15: Bad-line and invalid-block policy (slug: invalid-block-policy)

This conflict was not on the owner's list; the research shows two stacks taking opposite positions on the same input, so it is logged here (ID C15).

| Effort | Position | Evidence |
|---|---|---|
| E1 | One bad line makes the whole v2 block `invalid`; `cluster_v2` then drops every finding of that reviewer and removes it from the support denominator; `verify_cmd` still reads findings of invalid blocks | `findings_v2.py:299-303`; `cluster.py:220-221,256-257,386,405`; `verify_cmd.py:139-157`; 03 §2.2 [CODE-VERIFIED]; pinned by `test_review_cluster.py:556` |
| E2 | Counted 80 reviewer-level cases with an invalid block in the study's merges; under the v2 rule all their findings, not only the 92 bad lines, would be lost (an inference, not replayed on E2 data, G-27) | `AD/summary.md:7-8,16-18`; 03 §7 Key Takeaways [DOC-SOURCED] |
| E3 | v1 keeps the parsable lines of an invalid block and merges them (`findings.py:188-192`; `ledger.py:135-138`) while `ledger.py:112` claims such a reviewer is "skipped for clearing" (contradicted by `:254-258`); the installed experiment ledger refuses the whole input | 02 §1.4, §6.1 [CODE-VERIFIED] |

#### Option A: keep the valid lines, mark the reviewer partial, persist every rejection, exclude it from agreement denominators

**Description:** One explicit policy: per-line validity with a reviewer-level `partial` state.
**How it works:** `parse_block` keeps its per-line error list in the result; the merge stores the rejected ids and reasons (as `cluster_cmd.py:161` already does for cards); clustering uses the valid lines; a partial reviewer counts as an abstention for any quorum rule, not as "no findings".

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Low |
| Reuse of existing code | High |
| Files/systems affected | `findings_v2.py` state values, `cluster.py` `_members`, `ledger.py`, tests `test_review_findings_v2.py:106-113,150-153` and `test_review_cluster.py:556` |
| Pros | No finding is lost to a neighbour's error; consistent with C02 |
| Cons | Changes two pinned behaviours on purpose; a partial block may hide a truncated tail (the unclosed case stays `truncated`) |

#### Option B: whole-reviewer invalid (the v2 rule everywhere)

**Description:** Treat any error as invalidating the reviewer's block.
**How it works:** extend `findings_v2` behaviour to the document loop.

| Aspect | Assessment |
|---|---|
| Effort | S |
| Risk | High |
| Reuse of existing code | High |
| Files/systems affected | `ledger.py` and every v1 consumer |
| Pros | Simple and strict; a block with errors is not trusted |
| Cons | The E2 loss would grow from one line per error to the whole reviewer; luna, ember and wonder write long anchors systematically |

#### Option C: refuse the whole input and re-ask (experiment ledger)

**Description:** Any problem refuses the input; nothing is written.
**How it works:** `validate_rows` and `check_anchors` return a refusal; the caller retries.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | High |
| Reuse of existing code | Medium (installed only) |
| Files/systems affected | A retry step in every consumer |
| Pros | No half-written state |
| Cons | Compliance on a re-ask is untested (G-23) |

**Evidence:**
- The two stacks take opposite positions on the same input: v1 keeps and clusters parsable lines, v2 drops all (03 §2.2 "OPPOSITE positions") [CODE-VERIFIED].
- Rejection reasons are better surfaced on the E1 card side (`cards[].errors`) than in the master ledger, which keeps one warning with the error count and the first message only (03 §3; 01 §14.2) [CODE-VERIFIED].
- The docstring/behaviour contradiction on clearing is real (`ledger.py:112` against `:254-258`); `test_review_ledger.py:385` pins the code (D-09) [CODE-VERIFIED].
- A hand-written reflect contract with an unquoted `[1m]` alias already shows what whole-file invalidation does to a run: three unparseable shadow contracts counted as "no contract" (07 §7.1) [E1].
- External context [web]: missing votes must not default to an answer; treating a missing validator vote as a default changed results (https://arxiv.org/html/2510.11822v2, preprint); the "abstention" reading of an invalid block is web-01 recommendation 4 (an inference by that report, not a sourced claim).

**Status:** DECIDED-BY-EVIDENCE: the E2 loss and the code both show that dropping a whole reviewer or refusing the input costs findings the models did produce, and per-line keep with persisted rejections is the only option that loses none.

**Recommended resolution:** Option A. Keep the valid lines, mark the reviewer `partial`, persist id, line and reason for every rejection, count a partial reviewer as an abstention when a quorum is computed, and never let an invalid reviewer clear a row.

**Adversarial result:** n/a

### C-16: Blocking predicate per lens (slug: blocking-predicate-per-lens)

This conflict was not on the owner's list; it is the concrete form of the three blocking rules that coexist in code (C05 decides who applies the predicate, this conflict decides what the predicate is per lens).

| Effort | Position | Evidence |
|---|---|---|
| E1 | The parser's label rule applies only when `reflect_category` is set and then requires `blocking == (severity != MINOR)`; reflect halts on any Drift or Regression count; `card_convert` maps MEDIUM drift to non-blocking MINOR and drops the two-word class labels; `unauthorized_deviation_present` is a halt flag with no producer rule; `channel: advisory` may carry `blocking: true` | `findings_v2.py:107-108,161-162`; `contract.py:371-381`; `card_convert.py:71-83,203`; `SKILL.md:854`; 05 §1.4, §7, §8 [CODE-VERIFIED] |
| E2 | Used the product first-review brief as shipped, whose consequence rule makes a requirement the document never states "Medium" (MAJOR with `blocking: false`); that "Medium" exists only in prose | E2 `run-reviewer.sh:17`; `document_review_loop_prompts.md:31`; 01 §5 [CODE-VERIFIED] |
| E3 | Consequence rule in prose (`spec-panel.md:259`): a MAJOR blocks only if it names a concrete wrong outcome; the experiment ledger computes blocking per profile from grade, rule and wrong outcome (`review_ledger.py:41-49`); rf-qa defines blocking by definition (CRITICAL and IMPORTANT block) and PR review derives it from the remapped tier | 05 §10; 01 §9, §16 [CODE-VERIFIED] |

#### Option A: reviewer-written boolean plus one generic label rule (status quo, with the conflict left)

**Description:** The reviewer writes `blocking`; the parser enforces only "MINOR never blocks" and, with `reflect_category`, the label rule.
**How it works:** as today.

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | High |
| Reuse of existing code | Complete |
| Files/systems affected | None |
| Pros | No change |
| Cons | The same `missing-requirement` finding is non-blocking by the brief (D9) and blocking by the v2 label rule; 26 of 42 MAJOR findings in 13 shadow runs were `blocking: false` because `reflect_category` was absent; converted cards understate blocking for the class that reflect halts on |

#### Option B: a per-lens predicate in data, reviewer flag kept as an input, effective blocking recorded

**Description:** Each lens declares how blocking is derived: spec = consequence rule; reflect-post = `deviation_class` plus `channel`; PR = remapped tier; rf-qa = CRITICAL and IMPORTANT.
**How it works:** a `PROFILES`-style table (grades, predicate, cap) in code or data; the finding keeps the reviewer's flag and the effective flag; `channel: advisory` and `grounding-gap` can never block (grounding gaps route through `needs_human_decision`); `card_convert` re-derives blocking from `deviation_class` and normalises "authorized expansion" and "necessary deviation".

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium |
| Reuse of existing code | High: `PROFILES` pattern, `contract.py` halting rules |
| Files/systems affected | `findings_v2.py`, `card_convert.py`, lens modules, `document_review_loop_prompts.md` grading line, tests `test_review_severity_mapping.py`, `test_review_card_convert.py` |
| Pros | One rule per lens; resolves D9 and the MEDIUM-drift gap; matches how every non-v1/v2 vocabulary already works |
| Cons | Two policy questions stay with the owner: whether MINOR drift halts (`contract.py:380-381` against `findings_v2.py:107-108`) and who produces `unauthorized_deviation_present` |

#### Option C: compute blocking from severity everywhere

**Description:** Drop the reviewer's flag; `CRITICAL` and `MAJOR` block, `MINOR` never.
**How it works:** a single function on severity.

| Aspect | Assessment |
|---|---|
| Effort | S |
| Risk | High |
| Reuse of existing code | High |
| Files/systems affected | `findings.py`, `findings_v2.py`, briefs |
| Pros | Simplest rule |
| Cons | Removes "Medium" (MAJOR non-blocking) that the loop brief relies on; cannot express reflect's class-based halting or rf-qa's definition-over-label rule |

**Evidence:**
- Rule A (consequence sentence, reviewer applies it to its own findings) and Rule B (label rule with `reflect_category`) conflict on "MAJOR but not blocking"; they do not collide today only because no spec-lens producer sets `reflect_category` (05 §10.3) [CODE-VERIFIED].
- `findings_v2.check_finding` has no rule tying `deviation_class` or `channel` to `blocking`: a regression can be non-blocking and an advisory finding blocking (05 §7) [CODE-VERIFIED by reading `:84-187`].
- For reflect-post the per-finding rule follows from `deviation_class` and `channel`, except two owner decisions (MINOR drift; the producer of `unauthorized_deviation_present`) (05 §13 Key Takeaways; G-03, G-04) [E1].
- `SKILL.md` §10.10 (static analysis never sets `regression_present`) and `deviation-taxonomy.md:123` (static unreachability is a Regression) conflict (G-05); which governs is unresolved.
- In 13 shadow runs (2026-11-12/13) 16 findings were `blocking: true`, 26 MAJOR findings were `blocking: false` (05 §5.3) [E1] [CODE-VERIFIED in run files].
- Severity vocabularies: only v1/v2 and the PR `Severity` are enforced in Python; every vocabulary except v1/v2 derives blocking from a level or definition (01 §16) [CODE-VERIFIED].
- External context [web]: GitHub, Conventional Comments and Google keep obligation separate from severity and let policy set the gate (web-02 §Key External Findings 2, 6; https://conventionalcomments.org); OWASP and Semgrep derive severity from impact and likelihood (web-02 §6.4).

**Status:** DECIDED-BY-EVIDENCE: the code shows the same category with opposite rules in two stacks and every other vocabulary already deriving blocking per consumer, so a per-lens predicate is the only option consistent with all of them; the two policy questions inside the reflect-post lens are owner decisions listed as open questions.

**Recommended resolution:** Option B. Define one predicate per lens as data, keep the reviewer's flag as an input, record the effective flag, forbid blocking on advisory and grounding-gap findings, re-derive blocking in `card_convert` from the deviation class, and carry G-03, G-04 and G-05 as owner decisions.

**Adversarial result:** n/a

### C-17: Fate of the code-driven Tier 2 engine behind the tasklist post gate (slug: ensemble-engine-fate)

This conflict was found by the gap-fill research (file 13) and was not on the owner's list: the blocking per-phase gate of sc:tasklist does not run the reflect skill that E1 studied.

| Effort | Position | Evidence |
|---|---|---|
| E1 | The UC-2 (post-execution) panel is deferred: the skill path accepts and ignores `--t2-engine` in UC-2 runs until Stage 5; `reflect-post` templates and a parser lens exist but no brief line, reviewer format, blocking rule or recorded post card with a findings block exists (0 of 48 recorded post run directories) | `SKILL.md:311`; 07 §8 [CODE-VERIFIED] |
| E2 | Not studied (a first-review study of tasklist plans; no post gate) | G-81 [DOC-SOURCED] |
| E3 | Master consumer: `sc-tasklist-protocol` runs `superclaude reflect run --depth deep` per phase and blocks on its exit code; the code always routes `--depth deep` to `ensemble.py`, written on master before the E1 work | `SKILL.md:1157-1165`; `runner.py:538-545`; 13 §1.7, §2.1 [CODE-VERIFIED]; tagged E1 only because it is reflect code |

#### Option A: fix the engine in place first (honest labels, real deviation flags, executor exclusion)

**Description:** Interim repair of `ensemble.py` so the gate can halt on a found deviation.
**How it works:** extract deviations from reviewer output into the contract fields; set `merge_method` and `adversarial_unavailable` from what actually happened; apply `executor_model_class` to the reviewer pool; write one contract schema.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | Medium |
| Reuse of existing code | High: `ensemble.py`, `contract.py`, tests `test_ensemble_*` (2,036 lines) |
| Files/systems affected | `ensemble.py`, `runner.py`, `config.py`, contract writer, gate acceptance criteria in `sc-tasklist-protocol/SKILL.md` |
| Pros | Removes the critical false-green: today reviewer findings never reach the verdict and the gate can PASS, DEGRADE or BLOCK but never HALT on a deviation |
| Cons | Keeps a third merge path alive; reviewers still see only the tasklist text and base ref unless grounding in the diff is added |

#### Option B: replace the engine with the unified panel at UC-2 Stage 5

**Description:** The unified panel becomes the post-gate producer.
**How it works:** needs a UC-2 findings-v2 brief line, a per-class blocking rule (C16), a mapping to `deviation_count_by_class` and `per_task_verdicts`, a reviewer pool that satisfies constraint C12, a Stage 5 decision under C5, and the same CLI line, exit codes and output files the gate reads.

| Aspect | Assessment |
|---|---|
| Effort | XL |
| Risk | High |
| Reuse of existing code | Medium |
| Files/systems affected | `runner.py:538-545`, `ensemble.py`, panel templates, reflect post brief, the gate's contract keys (about 30), C5/C11/C12 constraints |
| Pros | One merge path; grounded reviewers; shared evidence checks |
| Cons | No producer exists yet; the gate's exit codes and keys must stay unchanged; `--reviewers` clamp (up to 4) conflicts with C11 |

#### Option C: leave the engine as is

**Description:** No change.
**How it works:** none.

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | High |
| Reuse of existing code | Complete |
| Files/systems affected | None |
| Pros | No work |
| Cons | The gate is a reviewer-agreement and diversity check, not a deviation audit; three of five acceptance criteria (`REPORT.md`, executor-disjoint reviewers, per-task verdict matrix) are not produced by code |

**Evidence:**
- `superclaude reflect run --depth deep` always calls `run_tier2_ensemble` and sets `rc = 0` (`runner.py:538-545`); the skill, its 1.8.0 contract, `panel_lint` and the shadow kernel are never involved (13 Summary) [CODE-VERIFIED].
- Defect grades (13 §10): D1 reviewer findings never reach the verdict (Critical); D2 reviewers see only tasklist text and base ref, no diff, no evidence validation (Critical); D3 `executor_model_class` ignored (High); D4 `merge_method: adversarial` written from the reviewer count even when the adversarial step failed (`ensemble.py:773`) (Medium, masked today by the `null-convergence` degrade) [CODE-VERIFIED].
- The engine writes a version-"1.0" contract with 11 keys outside the 1.8.0 lists, so two incompatible reflect contracts share one file name and one reader (13 §4; G-66) [CODE-VERIFIED].
- It shares only the `/sc:adversarial` child (used score-only) and the `contract.py` verdict map with the skill path, and nothing with `cli/review/` (13 §5.3) [CODE-VERIFIED by grep].
- Enabling the panel for this gate needs a code change at `runner.py:538-545` and `ensemble.py`; the "reflect flag change" wording elsewhere applies to skill-path consumers only, and only `--t2-engine shadow` is passable today (G-93) [CODE-VERIFIED].

**Status:** DECIDED-BY-EVIDENCE: the false-green defects are verified in code, and replacement is impossible today because no UC-2 producer, brief line or blocking rule exists on the panel side; only the fix-in-place-then-replace sequence is feasible.

**Recommended resolution:** Option A now, Option B at UC-2 Stage 5. Whether the unified panel replaces `ensemble.py` or `ensemble.py` is repaired permanently is the owner's UC-2 decision (G-65).

**Adversarial result:** n/a

### C-18: Read-only enforcement for reviewers (slug: reviewer-read-only)

This conflict was not on the owner's list; the three efforts enforce "the reviewer must not edit" in three different ways.

| Effort | Position | Evidence |
|---|---|---|
| E1 | The `reflect-reviewer` agent has an allowlist (Read, Grep, Glob and search tools; no Bash, Edit, Write or Task) and `permissionMode: plan`; pinned by tests against a mutator set | `reflect-reviewer.md:5-8,36-40`; `test_reviewer_readonly_tools.py:30,78` [CODE-VERIFIED] |
| E2 | A deny list `--disallowedTools Edit Write NotebookEdit` under `bypassPermissions`; Bash stays available and auto-approved; the judge has no deny list at all; safeguards are a `/tmp` sandbox and an after-the-fact audit | E2 `run-reviewer.sh:48`; `judge-one.sh:25-27`; 06 §3.1, §4 [CODE-VERIFIED via `git show`] |
| E3 | Only prose ("do not edit the candidate"); the re-review step requires running `diff -w` and `grep -nF` | `document_review_loop_prompts.md:32,44,46`; 06 §1.3 [CODE-VERIFIED] |

#### Option A: allowlist everywhere; shell evidence computed by the orchestrator and injected as hunks

**Description:** Every reviewer is an allowlisted read-only agent (or `claude -p --allowedTools`); diff evidence and quote self-checks are computed outside the reviewer.
**How it works:** the orchestrator renders the diff and the quote check into `## Grounding hunks` (the FR-4 pattern, `reviewer-spec.md:53`).

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Low |
| Reuse of existing code | High |
| Files/systems affected | Brief template (C10), re-review prompt, E2-style runner |
| Pros | Mechanical guarantee; no Bash for reviewers |
| Cons | `claude -p` allowlist behaviour under `bypassPermissions` was not tested (G-45) |

#### Option B: deny list plus an after-the-fact audit (E2 style)

**Description:** Block known mutators and audit the output.
**How it works:** `--disallowedTools` and an audit that no candidate was written.

| Aspect | Assessment |
|---|---|
| Effort | S |
| Risk | Medium |
| Reuse of existing code | Medium |
| Files/systems affected | Runner |
| Pros | Allows the slash-command route |
| Cons | Bash can still write through redirects, `sed -i` or git |

#### Option C: prose rule only

**Description:** Tell the reviewer not to edit.
**How it works:** brief text.

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | High |
| Reuse of existing code | Complete |
| Files/systems affected | Briefs |
| Pros | None beyond cost |
| Cons | No enforcement; the re-review step then asks the reviewer to run shell commands |

**Evidence:**
- Allowlist enforcement exists and is tested for one agent; the agent file calls its prose the backstop to the mechanical allowlist (`reflect-reviewer.md:40`) (06 §4.1) [CODE-VERIFIED].
- E2's deny list leaves Bash approved under `bypassPermissions` (`run-reviewer.sh:48`), and the judge has no deny list (`judge-one.sh:25-27`) (06 §3.3, §4.2) [CODE-VERIFIED].
- The E3 re-review evidence step conflicts with a no-Bash reviewer; the diff must come from the orchestrator (06 §4.2 conflict) [CODE-VERIFIED].
- Neither path verifies that a reviewer read a required file, though both save a transcript from which it could be checked (06 §4 Key Takeaways).
- rf-qa and rf-analyst run with write tools and `bypassPermissions`, so their bodies cannot be reused as read-only reviewers without a new agent definition (10 §6) [ext] [CODE-VERIFIED].

**Status:** DECIDED-BY-EVIDENCE: only the allowlist is mechanical; the deny list leaves a documented write path and the prose rule is unenforced.

**Recommended resolution:** Option A. Use allowlisted reviewer agents or an equivalent `claude -p` allowlist, move every shell step into orchestrator-made hunks, and test the `claude -p` allowlist behaviour before relying on it (G-45).

**Adversarial result:** n/a

### C-19: One verdict contract and exit-code vocabulary (slug: verdict-contract)

This conflict was not on the owner's list; the future-consumer research found several verdict formats that need one owner.

| Effort | Position | Evidence |
|---|---|---|
| E1 | Four reflect verdicts (PASS, DEGRADED, HALTED, BLOCKED) derived by `derive_verdict`, with exit codes 0/10/11/2 for the wrapper | `contract.py:138-260`; `models.py:39-49`; 05 §1.2, 13 §9.1 [CODE-VERIFIED] |
| E2 | Not studied (round 1 only; deterministic merge printed FAIL or PASS from the ledger) | 02 §4.4 [DOC-SOURCED] |
| E3 | Ledger verdict PASS/FAIL with decision PASS/REVISE/ESCALATE and exit 0/10/11 (`ledger_cmd.py:13`); installed experiment ledger CONTINUE and PENDING with exit 0/10/11/12 (`review_ledger.py:63`); stoprule process codes 0/3/4/5/6 (`stoprule.py:8`); rf-qa and rf-qa-qualitative write `## Overall Verdict: [PASS / FAIL]`; task-builder reads a `VERDICT:` line | 02 §9 item 5; 10 §3 [CODE-VERIFIED] |

#### Option A: the core returns one machine verdict; each module maps it to advisory or blocking and to its native format

**Description:** One verdict and one exit-code set in the core (PASS/REVISE/ESCALATE as today, with an optional PENDING); modules decide gate strength and render their own report line.
**How it works:** `ledger verdict` stays the machine surface; reflect keeps its four-verdict map as a module-side mapping; rf-qa and task-builder lines are generated from the core result.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Low |
| Reuse of existing code | High |
| Files/systems affected | Core verdict module, consumer skill text, tests that pin exit codes |
| Pros | Verdict ownership in one place; advisory versus blocking stays a module choice (workflow Wave 4 advisory, post gate blocking) |
| Cons | Reflect's contract fields (`tier_reached`, `adversarial_convergence_score`, deviation counts) must stay readable by the gate |

#### Option B: Option A plus rf-qa's monotonicity and regression halts in the core stop rule

**Description:** Also adopt "open blocking count must strictly shrink" and "any PASS to FAIL regression halts" (`rf-qa.md:403-418`).
**How it works:** extra checks in the decision step.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium |
| Reuse of existing code | Medium |
| Files/systems affected | `ledger.py` decision code, rf-qa replacement module |
| Pros | Protects an rf-qa replacement from non-convergence |
| Cons | Untested against the ledger loop; may conflict with the cap-by-refusal rule in C13 |

#### Option C: leave the contracts as they are

**Description:** Three verdict formats and several exit-code sets.
**How it works:** none.

| Aspect | Assessment |
|---|---|
| Effort | XS |
| Risk | Medium |
| Reuse of existing code | Complete |
| Files/systems affected | None |
| Pros | No change |
| Cons | Each new consumer re-invents the mapping; the three formats need "one owner" and have none |

**Evidence:**
- Exit-code vocabularies differ: master `merge` always exits 0, `ledger verdict` exits 0/10/11, the experiment ledger 0/10/11/12 and other process codes, stoprule 0/3/4/5/6 (02 §2, §9 item 5) [CODE-VERIFIED].
- Verdict ownership differs per consumer: spec-panel blocks through the ledger verdict, the tasklist post gate through reflect contract fields, workflow and Stage 10.5 are advisory (09 §8 item 3) [CODE-VERIFIED].
- rf-qa halts on non-monotonic open blocking counts and on regression; the ledger stop rule has neither (`ledger.py:93-104`) (10 §6) [ext][E3] [CODE-VERIFIED]. The benefit of adopting it was not tested.
- Of 43 rf-* spawning call sites, 32 depend on an in-place fix step that a read-only panel cannot do; the common shape lens, consolidate, one fix agent, verify matches the review loop (10 §3 Key Takeaways) [ext].

**Status:** DECIDED-BY-EVIDENCE: the divergence among at least three formats and four exit-code sets is verified and a single machine verdict with module-side mapping is the only option that keeps the existing consumers working; adopting rf-qa's extra halts is a separate, untested add-on.

**Recommended resolution:** Option A; evaluate Option B's halts on the E2 ground-truth packages before adopting them.

**Adversarial result:** n/a

### C-20: Rollout and evaluation, shadow mode versus ground-truth benchmark (slug: rollout-evaluation)

This conflict was not on the owner's list; the efforts built two complementary evaluation mechanisms that were never combined.

| Effort | Position | Evidence |
|---|---|---|
| E1 | Shadow mode: the new path runs beside the authoritative legacy path and writes side artifacts only; an exit script requires 20 runs; it measures non-interference and side signals, "not quality"; Stage 2 exit is FAIL on 2026-11-13 (13 of 20 runs counted; EV-1 rate 8/13 = 0.615 against legacy 3/39 = 0.077; 6 parity and 9 lint or manifest failures); extraction of a generic harness is gated on 20 passing runs and a named second consumer | `shadow-standalone-evaluation.md:47-48,100-132`; `reflect_shadow_exit.py:203-387`; 07 §5; 11 §7 [CODE-VERIFIED for the script and run output; document statements DOC-SOURCED] |
| E2 | Ground truth per package (3 packages, 16 known defects), blind judge over anonymised merged reports, permutation tests, six audits; it measures quality; it has no shadow mechanism or run manifest; the judge is blind to reviewer ids only and never receives `source.md`; `source.md` and raw judge outputs are not committed; many paths live in `/tmp` | E2 `judge-one.sh:12-21`; 11 §2-§4; G-83 [CODE-VERIFIED via `git show`] |
| E3 | Pre-registered screen with fixed limits and an evidence-consistency checker (`final_report_check.py`, no model calls); the bundle reports convergence not proven and no valid-success verdict | FINAL-REPORT.md:42,75,87,250; 11 §11 [DOC-SOURCED, dated 2026-11-08/09] |

#### Option A: shadow mode per consumer only (E1 pattern)

**Description:** Roll out each consumer with its own shadow variant and exit script.
**How it works:** variant runs beside legacy; an aggregator counts clean runs.

| Aspect | Assessment |
|---|---|
| Effort | M per consumer |
| Risk | Medium |
| Reuse of existing code | High |
| Files/systems affected | Per-consumer scripts, `manifest.py` constants pinned by tests |
| Pros | Safe non-interference proof |
| Cons | Measures side signals, never quality; the shadow variant reuses legacy dispatch so it cannot show the panel finds more |

#### Option B: ground-truth benchmark only (E2 pattern)

**Description:** Score panels against known defects with a blind judge.
**How it works:** fixed packages, anonymised outputs, permutation tests.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | Medium |
| Reuse of existing code | Medium: the harness is bash with hard-coded paths, uncommitted inputs and a runner that overwrites attempts |
| Files/systems affected | New portable runner, judge brief with a source slot, committed packages |
| Pros | Measures quality (the only way to compare deciders, C05) |
| Cons | No rollout safety mechanism; three packages and 16 defects only; about 115,000 judge tokens per scoring (document-sourced) |

#### Option C: both, the shadow harness for rollout safety and the ground-truth benchmark as the quality regression set

**Description:** Extract the generic shadow harness (manifest profile plus exit-aggregator skeleton) and port the E2 benchmark behind a portable runner; use both for each consumer.
**How it works:** the exit script is split into a generic aggregator and per-consumer check plugins; the benchmark is hosted where real-`claude` spawning with isolation, timeouts and reporting already exist (`src/superclaude/cli/eval/` is the likely host; this is an inference, not a designed plan).

| Aspect | Assessment |
|---|---|
| Effort | XL |
| Risk | Medium |
| Reuse of existing code | High: extraction plan in `shadow-standalone-evaluation.md:100-123`; `cli/eval` runner |
| Files/systems affected | `manifest.py`, `reflect_shadow_exit.py`, `reflect_verdict_replay.py` (both bound to "1.8.0"), a new benchmark module |
| Pros | Covers both safety and quality; gives C05, C13 and C14 their missing measurements |
| Cons | Largest scope; the benchmark's judge must be made source-aware and fully blind first |

**Evidence:**
- The two harnesses are complementary, not overlapping: E1 has no ground truth and no quality score, E2 has no shadow or authority mechanism and no run manifest (11 §7 assessment) [CODE-VERIFIED reading of both].
- The judge brief carries the combo name (`judge-one.sh:21`) and folder path (`:6`), contradicting the "blind" claim for panel identity (D-55) [E2] [CODE-VERIFIED via `git show`].
- Shadow Stage 2 failures are orchestrator contract-writing and file-placement lapses, not merge quality: three unparseable contracts (`[1m]`), header copied from the harness, `merged-verdict.yaml` at the nested path, extra top-level keys (07 §5.1) [E1] [CODE-VERIFIED]; even the "clean" runs 10, 11, 12 and 14 broke shadow rules in places (G-60).
- No effort can say which model mix finds more real defects for reflect: blind scoring of the 15 combo runs was planned as a separately approved step and was not run (11 §9) [E1].
- The bundle's reusable parts are a fixed pre-registered screen, frozen endpoint hashes and a no-model evidence checker (11 §11 Key Takeaways) [E3].
- External context [web]: the only judge-quality evidence is for answer-correctness scoring; defect-finding panels have no controlled external study, so the project's own labelled packages are the validation set (web-03 §6.5; web-03 Recommendation 4, 7: a bias battery per judge, a judge from a different vendor than every scored reviewer).

**Status:** DECIDED-BY-EVIDENCE: each harness measures what the other cannot and several conflicts above (C05, C13, C14) cannot be resolved without the quality benchmark, so using both is the only option that supplies both safety and measurement; the hosting choice is an inference and is not part of the decision.

**Recommended resolution:** Option C. Treat the shadow harness as the rollout-safety gate and the E2-style benchmark as the quality regression set; first make the benchmark portable (committed `source.md`, source-aware judge brief, panel-blind labels, no `/tmp` paths) and name an owner for the benchmark port (G-59).

**Adversarial result:** n/a

### 6.D Defects D1-D16

The sixteen product defects come from the other session's hand-off and were re-checked against current code by the research files. Line numbers below are the current ones read on 2026-11-13/14 on branch `ironbelly/shadow-runs` (HEAD `792cf8c52`); the hand-off's line numbers for D7, D11 and D12 are stale (D-21) and are not used. "Tests that must change" lists existing tests that pass because the defect exists; "add" means a new test is needed (12 §9). Statuses: "decided" = settled by the conflict named; "open" = the choice is inside an undecided conflict; the minimum fix is still stated.

| Defect | Current behaviour (file:line) | Options | Recommended fix | Tests that must change | Status |
|---|---|---|---|---|---|
| D1 Over-length findings are dropped and the loss is not recorded | `anchor`, `anchor2` over 200 and `claim` over 300 are rejected (`findings.py:104,108,118`; v2 `findings_v2.py:80,111,126,132,136`); the merge stores `block_ok` and a warning with the count and only `errors[0]` (`ledger.py:130-134,141-149`); 48 of the 49 blocking findings lost in E2 were length rejections, 1 was refs (02 §4.2) | reject plus record; truncate-prefix with counter; no limits and refuse input | Truncate-prefix with a counter for claim, anchor, anchor2 and quote; keep structural rejections; persist id, reason and blocking flag for every rejected line; one constant for the limits in every brief | `test_review_findings.py:113,117` and `test_review_findings_v2.py:192-208,241-251` if truncation; `:106-113,150-153` if one bad line stops invalidating the block; add: ledger entry lists dropped ids, warning carries every error, limit-equality test across v1, v2 and `card_convert` (12 §9) | Decided (C02, C15) |
| D2 A dropped re-report can clear a blocking row | `resolved_check` becomes `resolved` whenever no cluster re-reports it; `block_ok` is never read after `:150` (`ledger.py:254-258`); the docstring at `:112` says the opposite and is [CODE-CONTRADICTED] | invalid reviewer cannot clear; evidenced clearing (verify-only); leave | An invalid or partial reviewer never clears a row; clearing needs a positive answer in the verify-only protocol | `test_review_ledger.py:376-385`, final assertion `:385` becomes `resolved_check` (D2 is pinned, not uncovered, D-12); keep `:193-217` as the positive case | Open: minimum fix decided (C15); the round model rides on C13 |
| D3 A round passes with one valid reviewer | Refusal only when no reviewer has a valid block (`ledger.py:150-157`); PASS from `:273-274`; reflect already degrades a single-reviewer merge (`contract.py:295-296`) | refuse below a quorum of valid blocks; mark the round degraded; leave | A first review needs at least two valid blocks for PASS; an invalid reviewer counts as an abstention; a re-review by one anchor reviewer is the existing design and rides on C13 | `test_review_ledger.py:376-385`; add quorum-boundary and CLI exit-code tests (`test_review_cli.py:425` twin) | Open: an invalid reviewer abstains (decided, C15); the quorum number rides on C05 and C13 |
| D4 One reviewer's `blocking` flag decides the row and the verdict | `any(...)` at `ledger.py:187`, matched rows recompute from the current round (`:213-218`), brief ids read only `blocking` and `status` (`:99-104`), verdict `:274`; `confidence` is displayed (`:435,473`) but read by no decision (hand-off wording "never used" is only partly true, D-10); `cluster.py:375` keeps the same veto | veto; quorum; calibrator-weighted; blind grader; debate | See C05: split candidate from decision and let a per-lens decider decide; record `disputed` and support | `test_review_ledger.py:128-129` (`brief_ids == ["L1","L2","L4"]`), `:277-304`, `:518-544`; add a test that `confidence` or support is consumed | Open: C05 (undecided there) |
| D5 Missing anchors are kept silently | `annotate` sets `anchor_status "missing"`, `span None`, `section "none"`, no warning (`findings.py:349-358`); the row opens with the reviewer's `blocking` (`ledger.py:135-138,184-202`); a hallucinated anchor can open a blocking row | refuse input (experiment); keep and flag (v2 unresolved); keep silently | Keep the finding, record a warning with its id, and do not let it open a blocking row until a verification step confirms it | `test_review_ledger.py:408-417` (`:417` status open and blocking true) changes if demoted; add: warning names the finding id and "anchor not found" | Decided (C02) |
| D6 Clustering over-merges and keeps only the first member | Transitive union-find; fingerprint on section and refs, or refs and spans within 3 lines (`findings.py:367-407`); row claim, category and fp from member 0 and never updated on re-find (`ledger.py:191,199,207-238`); E2 replay: 195 chained rows among 1,398 rows in total, 83 mega-rows | keep both; one clusterer with complete-link; centre and cap | One clusterer on the v2 location model with complete-link admission, row fields from the highest-confidence member recomputed on re-find | `test_review_findings.py:235-317`, `test_review_ledger.py:139-150` if clusters split; `test_review_cluster.py:279-293,556,784-795`; adopt `test_reflect_cluster_pairs.py` labelled cases | Decided (C12) |
| D7 The reference-id regex misses tasklist ids | `_REF_TOKEN` accepts letters-hyphen-digits and `P1`-`P9` only (`findings.py:29`); `T01.02` and `AC-T01.02-3` give no refs, `D-P1` yields `P1`, `P12` nothing (probe 2026-11-13, 03 §5.2); the pattern is copied at `telemetry.py:23-24`; whether real tasklist findings carried `AC-` or `FR-` ids often enough was not measured (G-19) | widen the regex; per-target id grammar; declared refs only | A per-target id grammar defined once and imported by `findings.py` and `telemetry.py`; whole-token matches only | None existing; add: `refs_norm({"claim": "T01.02 breaks AC-3"})` contains both; keep `test_review_findings.py:210,212` and `test_review_cluster.py:221-230` green; `test_review_cluster.py:784-795` breaks if `refs_norm` moves | Decided (C12) |
| D8 The reviewer brief never names the source document | The product first-review prompt has five placeholders and reviews "against the requirements it states" (`document_review_loop_prompts.md:17-21,32`); the E2 brief is a filled copy (`run-reviewer.sh:13-17`); 156 of 665 valid-era runs never referenced `source.md` (E2 CR:373, DOC-SOURCED; the causal link is an inference, G-42) | `{{SOURCE}}` in the prompt; code-rendered template; lint only | One code-rendered brief with source, spec and grounding slots; source injected for every reviewer under a size cap; record `source_injected` and `source_read` | None if the source clause stays inside the brief line (`test_review_rules_text.py:34-42` forbids a new line between brief and findings-block bullet); add placeholder and source-grading-clause tests; retire reflect C7 test `test_shadow_skill_contract.py:146-165` in the same change | Decided (C10) |
| D9 The brief grades missing requirements Medium while the schema lets them block | `document_review_loop_prompts.md:31` makes a requirement the document never states Medium (non-blocking); `missing-requirement` has no per-category blocking rule (`findings.py:15-22,96-103`); the v2 label rule forces MAJOR coverage findings to block (`findings_v2.py:44,161-162`) | per-lens predicate; generic label rule; computed from severity | Per-lens blocking predicate in data; a source-omission grading clause once a source exists | `test_review_severity_mapping.py` grading bullets if the rule text moves; add: brief rule and schema agree per category | Decided (C16) |
| D10 `unpassable-ac` is rejected and the message does not name the value | `findings.py:17,102-103` (only `unpassable-check`); same in v2 (`findings_v2.py:109-110`); `card_convert` coerces unknown words to `other` (`:207`); the bad label came from the E2 harness brief, not the product brief (01 §5, §11) | reject with the value named; coerce; per-lens category namespace | Name the rejected value in every message; generate briefs' category lists from the constant; keep one policy (reject with the value named) | None; add: `parse_block` accepts `unpassable-check` and rejects `unpassable-ac` with the value in the message | Decided (C01, C02) |
| D11 Distinctness silently allows duplicates | Random or round-robin pool exhausted by `exclude` re-admits the whole pool unless a hard set exists (`panel.py:536-543`); record has no duplicate flag (`:666-699`); gateway `live7` repeats `Qwen3.8-max`, anthropic-only `live7` returns six haiku (run 2026-11-13) | strict by default; flag only; declared policy with replicas | Declared per-slot policy and no silent re-admission (decided); intended replicas recorded as an optional design option; fallbacks filtered by the chosen set | `test_review_panel_exclusion.py:97-98,208-213` and the 16-case golden `:56-72`; `test_review_panel_reflect_profile.py:74-90`; `test_review_panel_live7.py:48-60`; `test_review_panel.py:265-281`; `test_review_cli.py:52-80`; regenerate `panel-golden-default-live7.json` and `panel-golden-packaged-tiers.json` (12 §3.3, §5) | Decided (C04) |
| D12 Environment selection reads one variable and checks no alias | `select_env` reads `T3Model01` only (`panel.py:485-494`); `T2bModel01` is never read, so nothing checks that a template's `tier2b` alias exists; observed `T2bModel01=gpt-6.1-terra` on 2026-11-13 | check every alias a template needs; detect by more variables; leave | Validate alias existence per template and environment; do not key detection on one ccsession variable | None; add: `T2bModel01` unset with `tier2b` in a template gives an error or explicit warning (`test_review_cli.py:83-88` only pins `T3Model01`) | Open: the check is decided (C03 option C); the default environment rides on C03 |
| D13 The loader silently skips missing modules | `__init__.py:19-36` swallows `ModuleNotFoundError`; `lint_cmd` and `estimate_cmd` are names of unmerged experiment branches PN2 and PN3, not typos; the registered set has only a partial pin (4 of 7 subcommands, `test_review_cli.py:44-49`) | explicit imports for core commands; keep optional loader for experiment names; leave | Explicit imports for the core set plus a test pinning the set; drop ghost names until their branches merge | `test_review_cli.py:44-49` if `lint` or `estimate` are added; add: every listed module imports and `review --help` lists exactly the set | Decided (no conflict; design input 09 §8 item 6) |
| D14 No tasklist review step and the loop lives in one prompt paragraph | The #346 merge and ledger CLI has one in-repo caller (`document_review_loop_prompts.md:70`); `panel resolve`, `cluster`, `verify-citations` and `manifest` are called only by reflect shadow steps (`SKILL.md:338-349`); workflow Wave 4 and tasklist Stage 10.5 reach review through `/sc:reflect` (advisory), the per-phase post gate through `superclaude reflect run` (blocking); the hand-off wording "only as experiment copies" is [CODE-CONTRADICTED] (installed in `~/.claude/`) (09 §7, D-15, D-27) | thin consumer modules over a shared brief and dispatch reference; per-consumer CLI calls; leave | One shared panel protocol reference plus thin per-consumer modules; each module states advisory or blocking | None; add a skill-text test that the workflow and tasklist skills name the review step and its rules file | Decided (C09, C10, C11, C19) |
| D15 Telemetry strata allow only sonnet or haiku and nothing writes telemetry | `STRATA = ("sonnet","haiku")` (`telemetry.py:112-115`, check `:267-268`); no caller in `src`; `merge_cmd.py:71-118` and `panel_cmd.py` write no telemetry (08 §3.4; C-18 closed item) | strata from the tier file `classes` map; telemetry as a projection of the manifest | Data-driven strata; emit telemetry from the committed manifest (C07) | `test_review_telemetry.py:324-327` (`stratum="gpt"` is rejected today) | Decided (C07) |
| D16 Round 4 accepted, `--cap` ignored on an existing ledger, verify-only is prompt-only | `_decision` is a label (`ledger.py:93-96`); `merge_round` requires only `n == len(rounds)+1` (`:114-118`); `--cap` reaches the ledger only on round 1 (`merge_cmd.py:101-104`); `--round` help says "1, 2 or 3" while the type is `IntRange(min=1)` (`:40-41`); no verify mode in `ledger.py`; the experiment ledger refuses at the cap (`review_ledger.py:1300-1311`) | refuse above the cap; error on `--cap` for an existing ledger; verify-only code mode | Refuse a round above the cap and error on a conflicting `--cap`; verify-only mode rides on C13 | None existing; add: `merge_round(..., 4, ...)` raises when `cap_reviews == 3`; `--cap` on an existing ledger errors or applies | Open: cap refusal is in the minimum fixes of C13; the verify-only mode rides on C13 |

### 6.X Overall design options

These are whole-design options drawn from the SOLUTION_RESEARCH section of the research notes (approaches 1-6). They combine the conflict resolutions above; they are not a roadmap and they do not choose a branch structure. Options A and B are stages of one unification path (A is B's first stage); Option C (keep both stacks) is the only alternative to that path.

```
                 +-----------------------------------------------------------+
 Option B shape: |  shared core                                              |
                 |  finding contract (v2 + lens registry) | panel resolver   |
                 |  dispatcher + adapters | run manifest   | clusterer       |
                 |  citation checks | decider hook | telemetry | verdict     |
                 +--------+----------+-----------+-----------+---------------+
                          |          |           |           |
                    reflect pre/  workflow    spec review   PR code review,
                    post module   tasklist    (brainstorm,  rf-qa replacement
                                  module      design)       (future modules)
```

#### Option A: findings-v2 as the single contract, v1 as a strict subset, on the existing two code stacks

**Description:** Keep the package layout; make findings-v2 the contract that every consumer writes; accept findings-v1 lines as a subset; fix D1-D16 in place; add lenses by editing the closed tuples.
**How it works:** `findings_v2.py` gains the v1 compatibility the docstring claims (blocks, empty block, prior lines, `reflect-post`); `LENSES` and the category sets grow by code change; the ledger parses v2; reflect keeps the debate and 1.8.0; the cluster path stays telemetry for reflect.

| Aspect | Assessment |
|---|---|
| Effort | L |
| Risk | Medium |
| Reuse of existing code | High: everything stays; `findings_v2`, `cluster`, `panel`, `manifest`, ledger |
| Files/systems affected | `findings.py`, `findings_v2.py`, `ledger.py`, `merge_cmd.py`, `cluster.py`, briefs, tests that pin v1 text |
| Pros | Smallest path to one contract; E1 and E3 code both survive |
| Cons | Every new lens or category is a code change (`LENSES` and `CATEGORIES` are closed tuples); a code-review or rf-qa finding still needs new severity and location kinds; `merge_round` stays single-document |

#### Option B: a new superset core with pluggable lens and category namespaces and several location types

**Description:** Build the shared core as data-driven registries: lens (candidate kind, severity vocabulary, categories, primary location kind, blocking predicate, id grammar), location union (anchor, citations with role, file and section, multi-file observation with `in_diff`), launch adapters per environment, review kinds beyond first and re-review, and fix and verdict contracts as data; findings-v1 and findings-v2 become profiles of the core.
**How it works:** start from the Option A code (v2 is the natural base, 01 §18), then move the closed tuples into registries; thin modules (reflect pre and post, workflow tasklist, spec review, PR review, rf-qa replacement) declare only their lens, brief slots and gate strength; the core exposes the 13 exposures X1-X13 of research 10 §5.

| Aspect | Assessment |
|---|---|
| Effort | XL |
| Risk | Medium-High |
| Reuse of existing code | High (v2 code, `PROFILES` pattern, reflect profile generalised) but a new registry layer |
| Files/systems affected | the whole `cli/review/` package, reflect skill and templates, `pr_submit` severity router and rubric (one table both sides read), rf-qa agents, telemetry, tier file |
| Pros | New consumers need no core change (the future-use exposure list); one rule per lens (C16); covers PR location kinds and rf-qa file-and-section locations |
| Cons | Largest design surface; the registry layer is untested; PR and rf-qa seams have open owner choices (finder versus S2b verifier, G-80; rubric versus router authority, G-78) |

#### Option C: keep both stacks and add adapters

**Description:** Do not unify; add `card_convert`-style adapters from each producer to each consumer and share only the panel resolver and the manifest.
**How it works:** document loops keep v1 and the ledger; reflect keeps v2 and the cluster path; PR review and rf-qa get their own adapters.

| Aspect | Assessment |
|---|---|
| Effort | M |
| Risk | Medium |
| Reuse of existing code | Complete |
| Files/systems affected | New adapters only |
| Pros | Fastest; no regression exposure on the 1,182 gate items (12 §8) |
| Cons | The four limits stay in nine places; D1, D5, D9 and the two invalid-block policies remain; every adapter repeats severity-word guesses (rf-qa `IMPORTANT` inverts under `card_convert`); two merge-ledger implementations and a third reflect merge path stay |

**Evidence:**
- The package already holds two stacks with different jobs: v1 decides (findings, ledger, merge, verdict), v2 only flags and records (findings_v2, card_convert, cluster, verify-citations, manifest); v2 imports private v1 names, so v1 edits propagate (research notes PATTERNS; 01 §2) [CODE-VERIFIED].
- Today no consumer exercises the E1 kernel in production and the #346 merge and ledger CLI has exactly one in-repo caller (09 §5, §7) [CODE-VERIFIED]; migrating consumers is therefore not blocked by existing production callers except the tasklist post gate through `ensemble.py` (C17).
- The core would have to expose open lenses, per-lens categories and severities, a location union, multi-artifact candidates with a pluggable clustering key, roles separate from models, more review kinds, fix and verdict contracts as data, provenance for grading, and model-role mapping and strata as data (10 §5 X1-X13) [CODE-VERIFIED reading]; today's closed `LENSES`, spec-only `CATEGORIES`, three-level severity, single-document anchor clustering, model-only templates, `--kind first|re-review` and sonnet/haiku strata each block at least one future consumer (10 §6).
- Reflect's frozen contract 1.8.0 permits sharing resolution, cards, clustering, citation checks, calibration coverage and manifests, but not the merge decision or contract writer (07 §10 Q8) [CODE-VERIFIED].
- External context [web]: production AI review systems separate finders from a coordinator that deduplicates, verifies against source and applies a severity rubric, and dedup on typed location and category rather than text similarity (https://blog.cloudflare.com/ai-code-review; web-04 D1, D2); SARIF models location as a union of physical, logical and snippet-hash kinds (web-04 R1).

**Assessment summary:** Options A and B are two stages of one unification path (B starts from A's code, so A is B's first stage), and Option C is the only real alternative to that path and the only choice that leaves the measured defect classes unchanged; the comparison is therefore between "unify, in stages" and "do not unify", not three independent designs. The conflict resolutions above are consistent with building toward Option B through Option A. Decided by evidence: C01, C02, C04, C06 to C12, C15 to C20. Resolved by adversarial debate and left `partial`: C03, C05, C13 and C14. Option B depends on those four: the launch adapters and the class-launch grammar on C03 (owner item O-2, the target environment), the decider the registry carries on C05, the ledger rounds model on C13, and the template and reviewer-count defaults on C14 (Decision D-1).

### Options Comparison

| Criterion | Option A: findings-v2 single contract, v1 subset | Option B: new superset core, pluggable lenses and location types | Option C: keep both stacks with adapters |
|---|---|---|---|
| Effort | L | XL | M |
| Risk | Medium | Medium-High (new registry layer, wider blast radius) | Medium (drift grows) |
| Maintainability | Good for existing lenses; every new lens is a code change in closed tuples | Best long term: lenses, categories, severities and predicates are data; one validator | Poor: limits and rules duplicated in nine places; two ledger paths and a third reflect merge path stay |
| Integration complexity | Medium: v1 consumers move to v2 parsing; ledger gains citations | High: touches package, skills, PR router, rf-qa agents, telemetry | Low per adapter, rising with each consumer |
| Reuse potential | High for reflect and document loops; low for PR and rf-qa without new kinds | High for all consumers by design (X1-X13) | Low: each consumer gets its own mapping |
| Future-consumer fit: PR code review | Weak: needs `in_diff`, five-tier severity, `line: null`, multi-file observations, closed PR reviewer set | Strong: location union and per-lens severity and predicate; seam choice (finder or S2b verifier) still open | Weak to medium: adapter can map fields but not the severity and merge semantics |
| Future-consumer fit: rf-qa replacement | Weak: `file:section` locations, IMPORTANT-as-blocking and fix-agent hand-off are missing | Strong for the review half; the 32 call sites that need an in-place fix keep a separate fix agent (Reviser) | Weak: severity words invert under today's word map |

**Recommended design (not a roadmap):** build toward Option B through Option A's code. Start from findings-v2 as the single contract (C01), keep the debate and contract 1.8.0 for reflect (C11), and move the closed tuples into lens registries as new consumers need them. Option C is rejected because it leaves D1, D5, D9, the opposite invalid-block policies and the third merge path in place.

