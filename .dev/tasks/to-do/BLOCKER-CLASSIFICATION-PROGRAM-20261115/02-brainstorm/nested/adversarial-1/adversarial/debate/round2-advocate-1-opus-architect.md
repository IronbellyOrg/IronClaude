# Round 2 advocate: Variant 1 (opus, architect)

- Round: 2 of 2 (rebuttals; this advocate goes first). Variant defended: `variant-1-opus-architect.md` (V1). Others: V2 = sonnet analyzer, V3 = haiku backend, DA = `diff-analysis.md`, A2 and A3 = the other two Round 1 advocate files.
- Status: complete. Nothing else was edited. Paths are relative to the repo root.
- New live checks this round are N1 to N7 (section 3). Older check ids (V-nn, L-nn) are from DA and my Round 1.

## 1. Responses to criticisms of Variant 1

Each criticism is listed with who raised it, then my answer. "Conceded" means the final spec should not keep V1's text.

| # | Criticism (raised by) | Answer |
|---|---|---|
| K1 | NEW-1 and NEW-2 shown as NOTE examples (A2 5.1; DA) | Conceded (already in R1). `gate1-cycle-control.md:9`: the Destination cell reads wrong, so V2 case 6's consumer test is the right wording. |
| K2 | `min(pW, pD)` used as a confirm score (A2 5.2; A3) | Conceded. `jev-uses.md:194` calls the min an upper bound; V3's `max(0, pW + pD - 1)` is the honest lower bound, reported with V2's ordinal bands until calibrated. |
| K3 | T6 "monotone in every input" (A2 5.3; A3 weakness 3) | Conceded. N4: the sketch's own check skips UNSET moves at lines 67 to 69. T6 becomes "monotone on N, U, Y" plus a separate missing-input test. |
| K4 | V1 leaves "highest severity wins" in place (A2 5.4) | Conceded, and the gap is larger than A2 said: N2 finds a third line, `task/SKILL.md:361`, beside `task/SKILL.md:252` and `tech-reference/SKILL.md:513`. V2's L1 and its pin T5 must cover all three. |
| K5 | Extension contracts are speculative scope (A2 5.8) | Partly conceded. V1 8.2 to 8.4 describe parts v1 already has (four judges, five deliverable kinds, eleven scale families: V1 5.1, 5.3, 7.5), so they are not hypothetical. But they must cost no code: a short "how to add" paragraph beside `refs/registry.yaml`, not a spec section a plan turns into work. |
| K6 | V1's M3 target of 5 percent is untestable at its sample size (A2 4.5) | Conceded (R1). V2's RT2 Wilson lower bound replaces V1 revert trigger 2. V1 trigger 1 (one safety escape reverts) stays: a single event needs no interval. |
| K7 | V1 moves to the new default before `rests_on` evidence exists (A2 4.8) | Partly rejected on the facts, conceded on the gap. V1 stage 1 edits no carrier and changes no gate (`variant-1:437`: "no existing carrier edited", "none at any gate"), so the old rule also decides in V1 stage 1. What V1 lacks is V2's paired data: reviewers emitting `rests_on` while the old rule decides. Adopt V2 stage 1 for that. |
| K8 | V1 repeats "about 25 minutes" (A2 4.4) | Conceded (R1). DA V-23 gives about 22 minutes for the whole loop after consolidation; V1 M1's "45 percent" is one sample and must say so beside the figure. |
| K9 | V1 stage 4 pre-commits an auto-downgrade path (A2 and A3, X-005) | Conceded. Stage 4 leaves the rollout table. Any classifier authority is a separate owner decision with V2's precondition (two consecutive clear audit windows) and V3's wording that it is "never implied by completion of stage 4" (`variant-3:552`). |
| K10 | V1 calls the sketch's UNSET handling "the more useful behaviour" (A3 weakness 3; DA C-014) | Conceded. Sketch line 44 lifts only `s == U`; with S = UNSET, 216 of 1,024 states give FOLLOW_UP or NOTE (V-17). S = UNSET must route to SHOW_USER. |
| K11 | V1 D1 sends excerpts to the fallback LLM when TypeSafe privacy is denied (A3 weakness 4) | Conceded. A privacy denial covers every external judge not separately approved, including `LlmJudge` (V3 5.4). |
| K12 | V1 filing has no recovery after a lost reply (A3 weakness 1) | Conceded. `/sc:issue` posts directly with no preview (V-26); V3's batch marker and `prepared`, `posting`, `reconcile`, `filed` states go into the ledger's Filings table. |
| K13 | V1 7.4 "ledger: unavailable" weakens the record guarantee (A3 weakness 5) | Partly conceded. V1 already writes a marker (`variant-1:284`) but nothing surfaces it to a coordinator. Adopt V3's `capture_state: incomplete` in the ledger header and `follow_up_capture_state` in the worker return. The gate result stays unaffected (V3 4.1 step 6 agrees). |
| K14 | V1 fixes the classifier's production path too early (A3 table, S-007) | Rejected. The repo CLAUDE.md forbids installed primitives from naming `src/superclaude/` paths, so a primitive reaches classifier code only through the `superclaude` CLI; the `review` click group exists (V-29). Fixing the boundary now keeps primitives path-clean. V3's request and response contract (5.2) should be the judge interface inside it. |
| K15 | V1's five-row ledger path table is heavier than one rule (A3 table, C-009) | Conceded, with new evidence (N3): V1's pr-submit path `.dev/pr-monitor/...` is gitignored and `WORKER-CONTRACT.md:34` bars gitignored paths from `artifacts`. Harmless today (pr-submit is never a worker, line 23), but V3's one rule plus two exceptions (implement indexes `notes.md`; pr-submit keeps its own list, per V2) is cleaner. |
| K16 | V1 runs ten classifier questions (A2 4.6; A3 concession 8) | Conceded. N4: `verdict(s, m, c, w, e, d)` at sketch line 35 takes six inputs; T, F, I, G reach no cell. |
| K17 | V1's offer lacks consent binding (A3 table, C-006) | Conceded. V3's exact ids and `set_digest` per offer; keep V1's no-question one-liner when there are 0 follow-ups and few notes. |

## 2. Updated assessment of Variants 2 and 3

Changed my mind:
- V2 on rollout order (S-009). Its stage 1 ("rule unchanged", reviewers also emit `rests_on`, `variant-2:558`) is the only stage in any variant that measures whether reviewers can name consumers before that ability carries weight. V1 had the safe ordering but not the measurement.
- V2 on question count (C-012). The sketch settles it (N4); A3 conceded the same.
- V3 on unknown consequence (X-003). V1 and V3 say nearly the same thing, but V3 states it as a rule over every input, reviewer and classifier ("Unknown is not no", `variant-3:75-76`), and V1's own risk K2 rates "most findings go to SHOW_USER" as high likelihood at first, so V1's at-the-gate prompt would flood upstream gates.
- V3 on ledger path (C-009) and offer consent (C-006), for the reasons in K15 and K17.

Did not change my mind:
- Location (X-001, S-005). Both rivals conceded it in Round 1 (A2 concession 5, A3 concession 1). N5 adds that `verify-sync` runs `diff -rq` over the whole skill folder, so `refs/registry.yaml` and every ref are drift-checked, not only `SKILL.md`.
- Inline text plus a pointer (X-002). A3's preference for references alone is contradicted by N1: the plugin tree has no "pragmatic" match, so plugin-only installs get no broadcast and only text inside each carrier reaches them.
- V2's `consumer-unknown` as an unconditional non-blocking class. A2's case 14 shows it doing real work, but A3 is right that a later sweep is a mitigation, not evidence at the present gate. Section 4 keeps it only where a later sweep is guaranteed.
- V3's four tables as a default. A2's scope objection holds for Offers and Filings when no offer or filing happens; A3 conceded empty tables must not force work (A3 concession 7).

## 3. New evidence (live this round)

- N1. `src/superclaude/hooks/hooks.json:173` registers `pragmatic-subagent.js`; Grep for "pragmatic" under `plugins/superclaude` returns no files. Plugin-only installs receive no broadcast, so every plugin carrier must hold the digest inline (A-007, X-002). (A2 also saw this; it is new against V3's reference-only stance.)
- N2. "Preserve the highest severity" matches three lines: `src/superclaude/skills/task/SKILL.md:252` and `:361` (final QA consolidation), and `src/superclaude/skills/tech-reference/SKILL.md:513`. A2 named two (C-017).
- N3. `.gitignore:250` ignores `.dev/pr-monitor/`; `src/superclaude/core/WORKER-CONTRACT.md:34` leaves gitignored paths out of `artifacts`; line 23 keeps `/sc:pr-submit` off workers "while the answer to decision D3 keeps it off workers" (C-009).
- N4. `blocker_truth_table_sketch.py:35` `def verdict(s, m, c, w, e, d)`: six inputs. Line 44 lifts only `s == U`; lines 67 to 69 skip UNSET moves in the monotonicity check (C-012, X-007, X-008).
- N5. `Makefile:112-125` (sync-dev) copies every file of each skill folder that has a `SKILL.md`; `Makefile:178` (verify-sync) runs `diff -rq` over the whole folder; `Makefile:148-157` also syncs `templates/` (X-001).
- N6. Grep of `WORKER-CONTRACT.md` for "unknown", "optional" and "tolerate" finds no rule that consumers tolerate unknown return keys; line 33 lists the top-level keys explicitly. V1 4.4's claim (sourced to enrichment) is UNVERIFIED in the contract itself, so the new keys need an explicit contract edit (C-010).
- N7. `src/superclaude/commands/spec-panel.md:268` is the fail-closed pointer precedent ("if it cannot be read, return `incomplete` and review nothing"). Grading must not need the pointer, but the ledger-writing step should report incomplete capture in that spirit (K13).

## 4. Convergence proposal (one position per open topic)

1. **Rule location and copies.** One delegate-only skill `src/superclaude/skills/sc-review-severity/` (V1; all three advocates agree). `refs/rule.md` holds the full rule and, between version-marked HTML comment fences (V1), the digest, whose text is V2's single quotable paragraph (4.1) plus V3's "name the affected action" and "unknown is not no" sentences. Each carrier holds the fenced digest inline plus one pointer line naming `~/.claude/skills/sc-review-severity/refs/rule.md`, then `.claude/skills/...`; never a `src/` path. `refs/registry.yaml` lists every carrier with kind, stage and digest version; drift tests are parametrized over it and reverse-scan `src/` and `plugins/` (V1). A carrier at the wrong version keeps its old gate and reports a mismatch, and a running loop pins its rule version in the ledger header (V3). Plugin carriers get a hand mirror plus a parity test at the propagate stage (V1 D9), required by N1.
2. **Unknown consequence and UNSET answers.** Classifier: an UNSET or unsettled decisive input (S, M, C, or the wrong-by-D path) never yields FOLLOW_UP or NOTE; it yields SHOW_USER when attended and "reviewer label stands, row tagged `unsettled`" when unattended (V3 policy, V1 unattended rule). UNDETERMINED is a judge-chain failure outside the table that advances to the next judge (A-009). Reviewer: a finding whose consumer cannot be named may be recorded as Medium tagged `consumer-unknown` only when the deliverable is intermediate and a later gate is guaranteed to run V2's GR7 final-gate sweep; at the last gate, or with no sweep, it keeps today's label (V3). Never for conditions 2 or 3. V2's consumer line per phase output (L4) shrinks the set; V2 M6 and RT7 measure it.
3. **Ledger contract.** One `follow-ups.md` per run at V3's path rule, with the two exceptions in K15. Header: V3's metadata (`schema_version`, `run_id`, `owner`, `rule_version`, `revision`, `capture_state`). Items: V3's columns plus V2's `rests_on` and `tags`; V3's `nonblocking_basis` replaces V1's `why_not_blocking`. Observations always (idempotent import on resume); Offers and Filings created on the first offer or filing. Single writer, atomic replace, stale-writer re-read (V3). Escaping fixed now: `|` written as `\|`, a newline as `<br>`, with a value round-trip test and V2's pipe-count check run on the ledger itself. Schema defined once in `refs/follow-up-ledger.md` and checked by V1's T5. Worker keys: V3's six with V1's `show_user` count folded in, added to `WORKER-CONTRACT.md` explicitly (N6).
4. **Classifier question count.** Six decisive questions S, M, C, W, E, D (V2; N4) with V2's reworded S. T, F, I, G are optional explanation fields, run only in shadow until a measured benefit exists, and never cancel S, M or C (V3). Question text in `refs/classifier-questions.md`, versioned (V1).
5. **Guardrail measurement.** V2's design: blind auditor shown no rule text, strata with oversampling of `consumer-unknown` and consolidation-lowered rows, seeded-defect recall, the stage 0b retrospective escape test, triggers as 95 percent Wilson bounds (RT2). Add V3's "review every protected-risk disagreement, not a sample", V1's single-event safety revert and V2's GR7 sweep. Report V1 M1 and M2 per gate family with the sample size beside each figure.
6. **Rollout stages.** 0 Measure: V2 0a, 0b, 0c; if the scored table is late, small or blocking-only (A-005), stages 1 to 4 may proceed on 0b and 0c evidence and only classifier authority waits. 1 Offline contract and scaffold: skill folder, registry with every carrier at `legacy`, ledger adapters, FixtureJudge tests, V3's identity, crash and reconcile cases; no carrier edited. 2 Shadow with the old rule deciding: ledger, offer, `rests_on` and the shadow classifier on task and tech-research gates (V2 stage 1). 3 Default pilot: `pragmatic.md` and the rf-qa family move to v2 in the registry; V2's L1 (all three N2 lines) and L2 fix-pass checks take effect. 4 Propagate: remaining carriers, plugin mirror, strict reverse scan. Own-scale primitives and any classifier authority are separate owner decisions, not stages (V2 stage 4, V3 stage 5). Each stage's revert is a registry edit (V1).

## 5. Updated point table

Asterisk = preference changed from my Round 1. Confidence is in the design preference, not a measured probability.

| Point | Preferred | Confidence | One-line evidence |
|---|---|---|---|
| S-001 | V1 | 55 | V1 weights sections 7, 8, 9, 11 a plan executes; graft V2 sections 2 and 5 and V3 section 12. |
| S-002 | V2 | 80 | Per-statement labels would have exposed V1's 81 count and N6's unsourced key-tolerance claim. |
| S-003 | V2 | 88 | RC2 is wider than stated: three merge lines (N2). |
| S-004 | V2 | 80 | 14 graded cases including the correct NEW-1 consumer test. |
| S-005 | V1 | 85 | Skill folder synced and `diff -rq` checked whole (N5); both rivals conceded in R1. |
| S-006 | V3 | 60 | Identity and consent tables; Offers and Filings created only on use (section 4.3). |
| S-007 | V1 | 70 | CLI boundary required by the no-`src/`-path rule (K14); V3's contract becomes the judge interface. |
| S-008 | V1 | 60 | Documents parts v1 already has (K5); lowered because it must stay text, not code. |
| S-009 | V2* | 62 | Changed: V2 stage 1 collects `rests_on` while the old rule decides (`variant-2:558`); V1 registry stages grafted. |
| S-010 | V1 | 55 | Registry-parametrized T1 to T8 plus V3's crash, stale-write and reconcile cases. |
| S-011 | V2 | 88 | RT2 Wilson lower bound is the only trigger testable at n = 60. |
| S-012 | V2 | 55 | Evidence column per risk; V3's required responses grafted. |
| C-001 | V2 | 70 | Named consumer, acceptance check, stated reasons count. |
| C-002 | V3 | 72 | "Name the affected action"; unverified protected risk is not a note (`variant-3:65-66`). |
| C-003 | V2 | 60 | Keeping "Medium" avoids churn in pinned tests; the classifier enum stays FOLLOW_UP. |
| C-004 | V2 | 70 | `rests_on` names a checkable consumer; V3's `nonblocking_basis` beside it. |
| C-005 | V1 | 80 | Registry rows replace the hard-coded tuple and `[:6]` slice (L5). |
| C-006 | V3* | 55 | Changed: offer bound to exact ids and `set_digest` (K17); V1's no-question one-liner kept. |
| C-007 | V2 | 60 | Fix pass runs mechanical checks and stops if an item proves decision-bearing. |
| C-008 | V3 | 82 | Run-scoped ids, identity tuple, revision, atomic replace. |
| C-009 | V3* | 60 | Changed: V1's pr-submit path is gitignored and barred from `artifacts` (N3); one rule plus two exceptions. |
| C-010 | V3 | 62 | Capture state visible (K13); keys need an explicit contract edit (N6). |
| C-011 | V3 | 85 | `/sc:issue` posts with no dry-run (V-26). |
| C-012 | V2* | 78 | Changed: `verdict()` takes six inputs (N4, sketch line 35); T, F, I, G reach no cell. |
| C-013 | V2 | 70 | Three basis sources; admits upstream inputs have none today. |
| C-014 | V3 | 88 | Sketch line 44 lifts only `s == U` (N4); 216 S-UNSET states fall to FOLLOW_UP or NOTE. |
| C-015 | V3 | 70 | Time budgets, circuit breaker, labels hidden; add V2's field-order replicates. |
| C-016 | V2 | 75 | Blind audit, seeded recall, GR7; plus V3's every-protected-risk review. |
| C-017 | V2 | 88 | L1 is needed and must cover `task/SKILL.md:252,361` and `tech-reference/SKILL.md:513` (N2). |
| C-018 | V1 | 55 | Scale map with T4 over eleven families; V3's tasklist adapter caution. |
| C-019 | V1 | 55 | Files tied to stages; add V3's 120 lines versus 139 occurrences and the N2 line. |
| C-020 | V1 | 55 | Lists `test_review_rules_text.py:92`; union with V3's transitive module is 10. |
| C-021 | V2 | 88 | `stat` times give about 22 minutes (V-23). |
| C-022 | V3 | 62 | Loops pin a rule version; installers skip existing files (L9). |
| X-001 | V1 | 85 | All three advocates agree; N5 shows whole-folder drift checking. |
| X-002 | V1 | 75 | Plugin gets no broadcast (N1), so inline text is required; digest text is V2's paragraph. |
| X-003 | V3* | 62 | Changed: V3 states "unknown is not no" for all inputs; V1's gate prompt floods (V1 K2); V2's tag only before a guaranteed sweep. |
| X-004 | V2 | 60 | Once per run plus at an escalation halt. |
| X-005 | V3 | 70 | Authority is a separate owner decision (K9, `variant-3:552`). |
| X-006 | V3 | 85 | `jev-uses.md:194`: the min is an upper bound. |
| X-007 | V3 | 90 | Sketch line 44 lifts U, not UNSET (N4). |
| X-008 | V2 | 80 | Sketch lines 67 to 69 skip UNSET moves (N4); 432 lowering moves. |
| X-009 | V3 | 85 | Denial must cover every unapproved external judge (K11). |
| X-010 | V2 | 88 | File times undercut 25 minutes (V-23). |
| X-011 | V2 | 85 | Destination cell wrong (`gate1-cycle-control.md:9`). |
| X-012 | V1 | 52 | Unattended SHOW_USER rows need a recorded `unsettled` row; kept outside the offer set (V3). |
| X-013 | V1 | 55 | The correct answer is the union of 10 modules (V-20, V-21). |
| A-001 | QUALIFY | 80 | `pragmatic.md:221` brief hunts "false claims" and must change with the definition. |
| A-002 | QUALIFY | 78 | Condition 1 needs a decision basis upstream gates lack; consumer line plus GR7. |
| A-003 | ACCEPT | 90 | `CANONICAL_CAP_TEXT` pinned (L5). |
| A-004 | QUALIFY | 78 | The coordinator must read counts and `capture_state` (K13). |
| A-005 | QUALIFY | 82 | Only classifier authority waits on the table (section 4, item 6). |
| A-006 | QUALIFY | 80 | Escaping fixed as `\|` and `<br>` with a round-trip test (section 4, item 3). |
| A-007 | QUALIFY | 80 | Registered at `hooks.json:173`, absent from the plugin tree (N1). |
| A-008 | QUALIFY | 65 | UNVERIFIED; absent lists make M and D UNSET, which routes to SHOW_USER. |
| A-009 | REJECT | 88 | `ORDER` at sketch line 5 has no UNDETERMINED; define it as a judge-chain failure. |
| A-010 | ACCEPT | 90 | `pragmatic.md:228` exemption. |
| A-011 | ACCEPT | 85 | No key, no call; shadow with fixtures or approved judges only. |
| A-012 | QUALIFY | 78 | Needs the GR7 sweep plus the sampled audit. |
| A-013 | QUALIFY | 80 | No dry-run (V-26); needs V3's batch marker and reconcile. |
| A-014 | REJECT | 85 | `install_core.py:70` and `install_skills.py:102` skip existing files unless forced (L9). |
