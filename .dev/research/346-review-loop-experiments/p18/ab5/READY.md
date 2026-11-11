# ab5 READY (design d5: ab4 + the PN1 panel; two arms from one harness)

Root: `$SP/p18/ab5` (SP = /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad). Python: `python3`, standard library only. No git, no repo clone, no network, nothing launched. p16/ab4 and p13/ab1 are read only (not modified).

Two arms, selected at build time by `--variant` (owner change 2026-11-10):

| variant | runs | first review | merge | after merge |
|---|---|---|---|---|
| `panel` (BRIEF.md) | d5-r1..r6 | panel R1.t1b-1 / t2-1 / t3-1 / t4-1 (one per tier), lint-1, AC sweep on t1b-1 only | ab4 deterministic MERGE over the 4 reports, cleaned blocks | ADJ (beside VF1), VF1 -> V1 -> R2 (lint-2) -> VF2 -> V2 -> R3 (lint-3) -> VF3 -> AUD + AUD2 |
| `full` | d5f-r1..r6 | same panel, but on the PN1 product rules file (+ lint bullets) | PN1 merge with the typed ledger (`review/ledger.json`, rendered `round<n>.md`) | ADJ over all ledger rows (beside VF1), VF1 over ledger brief rows -> V1 -> ledger revise L1 -> R2 in PN1 sandbox -> M2 -> VF2 -> V2 -> L2 -> R3 -> M3 -> VF3 -> AUD + AUD2 |

Both: Sonnet stratum only, 3 reviews / 2 fix cycles, AUD/AUD2 frozen and always Sonnet, every state record and ledger line carries `stratum` and `model`.

## Files
| file | role | source |
|---|---|---|
| `harness.py` | build / prep / ingest / merge / verify / ADJ / tokens / lanes / analyze | copy of `p16/ab4/harness.py`, modified (all ab5 changes marked "ab5" in comments) |
| `advance.py` | state machine, `--dry-run`, `--variant panel\|full` filter; launch ledger `launch-ledger.jsonl` | copy of `p16/ab4/advance.py`, modified |
| `full.py` | variant `full`: ledger merge (M<n>), ledger revise (L<n>), VF over ledger rows, ADJ over ledger rows, PN1 re-review sandbox, PN1 telemetry record | new; logic from `p13/ab1/harness.py` (run_merge, run_ledger_revise, prep_adj, prep_reviewer, append_telemetry) |
| `score_themes.py` | `ids_from` (ab4 improved), `finding_block`, `clean_body`, `cut_block` | **byte copy** of `p16/ab4/score_themes.py` (copied so ab5 runs standalone; test asserts identity) |
| `reqlint.py` | PN2 lint | **byte copy** of `p16/ab4/reqlint.py` (= p13/clones/pn2 lint.py) |
| `pn1_panel.py` | PN1 panel resolver | **byte copy** of `p13/clones/pn1/src/superclaude/cli/review/panel.py` (standard library; loaded by path, hash-checked) |
| `vendor/superclaude/cli/review/{findings,ledger,merge_cmd,ledger_cmd}.py` | PN1 product review code | **byte copies** from the pn1 clone; `__init__.py` is an ab5 shim (the original imports click and registers commands). `merge_cmd.py` / `ledger_cmd.py` are reference only: `full.py` calls `ledger.merge_round` / `render_merged_report` / `save` / `apply_revision` / `defer` and `findings.parse_block` / `parse_fixmap` exactly as those two click commands do |
| `make_rules.py` | builds `frozen/rules.md` (panel) and `frozen/rules-full.md` (full) | ab4's make_rules + `full_rules()` |
| `decision.json` | all constants as data: D2/D3/D4/D6 rules (ab4 values), variants, panel, lanes, live_alias_map, reviewer_models.stand_in, FORBIDDEN_MODELS, frozen hashes, MAX_CONCURRENT_RUNS | ab4 decision.json + ab5 keys |
| `frozen/` | `review-panel.ab5.json` (ab5 template t1b, t2, t3, t4), `command.md` (sha e62e70b9..., = frozen audit command), `audit-rules.md` (3eb772f9...), `rules-ab1.md`, `rules-pn2.md` (as ab4), `rules.md` (panel, 99a3ccac...), `rules-pn1.md` (the file PN1 reviewers read, 3ce0c804...), `rules-full.md` (b3516c75...), `review-panel.default.json` / `review-tiers.default.json` (PN1 template, kept for the equality test, + MODEL-TIERS table) | all hash-pinned in decision.json `frozen` |
| `tests/test_ab5.py`, `tests/fixtures/` | 17 tests; fixtures = the 27 ab4 fixtures (real p12/ab1 reports) + 8 real ab4 run reports (`ab4-d4-*`) + 13 real PN1 reports (`pn1-b1-*`) | |
| `.drive-head` | `60`: how many filtered lines `drive.sh` shows for this dir | |
| `drive.sh.orig` | the drive.sh before the ab5 edit (backup) | |

## drive.sh (one minimal change)
Dispatch is unchanged (`cd $SP/$d && uv run --no-project python advance.py`). The filter ended in `| head -14`: with 6 runs x 4 panel reviewers ab5 prints 24 LAUNCH lines on the first call, and lines cut by `head` would be marked launched but never shown, so those agents would never start. Now `head -"$(cat $SP/$d/.drive-head 2>/dev/null || echo 14)"`: every other directory still gets 14; `p18/ab5/.drive-head` says 60.

## Design items
1. **Panel (owner correction 2026-11-10).** ab5 template `frozen/review-panel.ab5.json`: one reviewer per tier, t1b-1 (tier1b, fixed), t2-1 (tier2), t3-1 (tier3), t4-1 (tier4), aliases `claude-gw-tier1b[1m]` / `-tier2` / `-tier3` / `-tier4`; no tier1a slot (Opus is not in the panel). PN1's default template was t1b, t2, t3, t3. Each run's panel is resolved with the PN1 resolver (`pn1_panel.resolve`, byte copy) and the PN1 tier table, environment anthropic-only, as `superclaude review panel resolve`; test: the same code with PN1's template reproduces PN1's real `panel.json` / `panel-rr.json` of b1-r1 and b1-r4. **Mock (current)**: t1b-1 = Sonnet 5.5 (real), t2-1 / t3-1 / t4-1 = Haiku 5.5 stand-ins with `stand_in: true` in panel.json, state and telemetry. This is the same compute as PN1's panel (1 Sonnet + 3 Haiku); only the slot labels change, so comparability with PN1 is kept (test `test_panel_template_one_reviewer_per_tier`). Re-review panel: t1b-1 only (PN1).
2. **Reviewer models by gateway alias.** `decision.json live_alias_map` (data; no model name in logic, lanes or tests): tier1b -> Sonnet 5.5 (failover GPT-6.1 Sol, Muse Wonder Full 1.0), tier2 -> GPT-6.1 Sol, tier3 -> `terra_or_glm5_3` (GPT-6.1 Terra, likely GLM-5.3), tier4 -> GPT-6 Luna (`gpt-6-luna`, MODEL-TIERS "Budget", intelligence 38.1, notably weaker than the others); tier1a -> Opus 5.5 documented only, unused. `reviewer_models.stand_in` true = mock (PN1 resolution kept; each reviewer also records `live_model` / `live_name`); false = live (model, model_name, launch from the map; stand_in false). Mock -> live is this map + that flag, nothing else (test `test_mock_live_switch_changes_only_models_and_labels`). `build` asserts `stand_in == (model != live_model)` for every slot.
3. **Briefs.** Every panel reviewer gets ab4's R1a brief (= PN1's R1 brief + `, lint=<review>/lint-1.md`), lint-1 placed in its own sandbox `r1-<rid>/ws`. **The AC-sweep sentence goes on R1.t1b-1 only** (the Sonnet reviewer, R1b's role in ab4); t2-1, t3-1, t4-1 get the plain brief (test: t1b-1 = the other briefs + exactly that sentence). R2/R3 use ab4's `brief_re` (PN1 re-review brief + lint value), VF the Verify brief from `frozen/rules.md`, V the ab4/PN1 revise brief (identical text), ADJ PN1's `ADJ_BRIEF` verbatim, AUD the frozen audit brief.
4. **Rules files (wording changes; minimal diffs).** panel: `rules.md` = rules-ab1 + the two PN2 lint bullets (as ab4) + "three" -> "four" in the same 5 places ab4 changed to "two" (`diff frozen/rules-ab1.md frozen/rules.md`: 2 added lines, 4 changed lines). full: `rules-full.md` = rules-pn1 + the same two lint bullets at the same two anchor lines (`diff frozen/rules-pn1.md frozen/rules-full.md`: 2 added lines). The full arm's reviewers therefore write PN1's `## Findings block` (the ledger's input) and revisers write PN1's `## Fix map`.
5. **Merge.** panel: ab4's `merge()` generalised from 2 to the panel's reports (every reviewer not lost), same dedup rule (same theme and cited-line Jaccard >= 0.5), cleaned blocks (`blocking_findings(cut=True)` + `clean_body`), sub-entries `#### Mn.a (round1-<rid>.md <id>)`. full: PN1 `merge_round` + `render_merged_report` on the 4 findings blocks into `review/ledger.json` / `review/round1.md` (M1 log = PN1's printed result: verdict, decision, brief_ids, new, refound, regressed, cleared, clusters, block_ok, warnings).
6. **ADJ.** Runs beside VF1 once M1 exists (PN1 ran it beside V1); it feeds no loop decision (measurement, as PN1), but a run is complete only when ADJ is done or lost. panel: input = the merged findings (cleaned blocks), Mn relabelled X<k> in `random.Random(run)` order, reviewer/source lines dropped, contamination check applied. full: PN1 `prep_adj` logic over ALL ledger rows (anchor / anchor2 / refs / claim). Parse = PN1's adj-v1 JSON-line reading. RESULTS has an ADJ vs VF1 agreement table. `decision.json ADJ_GATES_VF1` (false) makes VF1 wait for ADJ if you want the strict panel -> merge -> ADJ -> VF order; it only changes wall time.
7. **VF.** ab4's clean verifier unchanged (VF1 over merged list, VF2/VF3 over the re-review's blocking findings; full: over the ledger's brief rows, cut from the rendered round<n>.md with `finding_block(clean=True)`). `check_findings_text` runs on every list; a contaminated list raises and advance prints `MANUAL <run> VFn not prepared` instead of launching. `reconcile_confirmed` (confirmed line authoritative) unchanged, used by both arms.
8. **Full arm interlock (where ab4 VERIFY and PN1 ledger overlap; both kept).** Order: panel -> M1 (merge + ledger) -> ADJ (beside) + VF1 -> V1 -> L1 (ledger revise) -> R2 -> M2 -> VF2 -> V2 -> L2 -> R3 -> M3 -> VF3 -> AUD/AUD2. Choices made: (a) M<n> decision PASS ends the loop (PASS) without a VF. (b) VF<n> verifies exactly the ledger's brief_ids. (c) A row the verifier rejects is parked with PN1's own `ledger.defer(lid, "verifier rejected (VF<n>): ...")`, so it leaves brief_ids and is not re-opened if a later reviewer refinds it (status stays deferred; recorded as noted, unactioned) - the ledger analogue of ab4's "not prior blocking findings". (d) The confirmed rows are V<n>'s IDS; round<n>.md gets ab4's VERIFY block and its "Blocking finding ids" line narrowed to them; the R<n+1> reviewer reads that file as prior. (e) No row confirmed -> VERIFIED-PASS; VF3 with a confirmed row -> ESCALATED (M3 = ESCALATE whenever rows are still open, even if the reviewer wrote PASS: the ledger decides, as in PN1). (f) The ab4 `ids_from` parse is recorded per report as a cross-check (`blocking_ids`); the full arm's decisions come from the findings block / ledger. (g) PN1's "no reviewer's findings block parsed -> relaunch once" applies to the panel round and to R2/R3.
9. **Lost reviewers / steps.** A worker without output is relaunched once (ab4). Second failure: a panel reviewer is lost and the merge runs over the others; two lost reviewers lose the run (PN1 `advance_run`); a lost ADJ is recorded and the run continues (PN1); any other step loses the run (ab4).
10. **Tokens.** ab4 `scan_by_prompt` / `transcript_info` / `pick` unchanged (output tokens, max per message id, each id once; pasted, wrapped and short `Read <path>/PROMPT.md and follow it exactly` launches). Only change: the PROMPT step-name pattern accepts `.` and `-` (`PROMPT-R1.t1b-1.md`; ab4 had `(\w+)`) and sandbox names `r1-<rid>`, `r2-t1b-1`, `r3-t1b-1`, `adj` resolve to steps. The transcript's model is stored as `observed_model`.
11. **Lanes (coordinator 2026-11-10, corrected).** `decision.json lanes` (data), by panel SLOT for R1 steps (slot = reviewer id before `-<i>`) and by step otherwise: **primary (Sonnet)** = slot t1b + ADJ + VF1-3 + V1/V2 + R2/R3; **parallel other-provider** = slots t2, t3, t4, reported per slot with the live model name beside the model actually used (e.g. "t4-1 live GPT-6 Luna; used claude-haiku-5-5 (stand-in)"); audits AUD/AUD2 separately, excluded from every loop total. ADJ (the adjudicator, on Sonnet) sits in the primary lane but has its own column so it stays visible. Each step's model in RESULTS comes from telemetry: the transcript's observed model, else the launch ledger, else the step record, never the step name. RESULTS shows per run and as means: primary, of which ADJ, parallel lane (+ each slot), LOOP, audits, and the three headline ratios vs the fresh-baseline loop 53,623 (`FRESH_LOOP_BASE`): total loop, primary lane only (without ADJ), primary + adjudicator; plus a per-step table "tokens / resolved model".
12. **Concurrency.** `MAX_CONCURRENT_RUNS = 6` runs with workers in flight; inside an admitted run every prepared step launches at once (4 panel reviewers; ADJ + VF1; AUD + AUD2). Runs are ordered d5-r1, d5f-r1, d5-r2, d5f-r2, ... so both arms get slots at the same time (first call: 3 runs of each arm, 24 agents). `AB_MAX` env overrides.
13. **analyze** writes `RESULTS.md` (one section per variant) and `metrics.json` (`{"panel": ..., "full": ...}`): run table with audit 1/2 BLK counts and audit findings (ab4 scoring), lanes, step-group tokens (panel / merge (0) / ADJ / VF / revise / re-review), per-step tokens with model, ab4 metrics and decide(), final spec path per run (`runs/<run>/aud/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`), panel per-theme capture (each reviewer + union), merge counts, ADJ vs VF1, verifier, noted vs audits.

## OWNER RULES recorded
- **No Fable / Tier 0, ever; no Opus step in ab5 (Opus is not in the panel; tier1a is a documented, unused alias).** ADJ runs on **Sonnet 5.5** in the Sonnet stratum (Haiku in the unbuilt Haiku stratum). **Deliberate deviation from PN1**: PN1's historical runs used a Fable adjudicator, so ab5's ADJ-on-Sonnet is a changed condition; ADJ results are not comparable with PN1's ADJ. `decision.json FORBIDDEN_MODELS` (fable, tier0, opus); `expected_model()` raises and `build()` asserts on any match. The frozen PN1 tier table still lists a Fable model as "available" (PN1 data, hash-pinned, not edited); no slot can resolve to it (t1b is fixed, t2/t3/t4 have only Haiku stand-ins in anthropic-only), and the guard would refuse it. Tests `test_no_forbidden_or_above_opus_model_anywhere`, `test_mock_live_switch_changes_only_models_and_labels`.
- Model names live only in `decision.json` / the frozen tier table; tests read them from there.

## Where D2 / D3 / D4 / D6 are encoded
- D2: `decision.json` A_BASE / AUD_BASE / B_BASE, `LOOP_INCLUDES_ADJ: true` (PN1 convention: adjudication counts in the loop; RESULTS also shows LOOP without ADJ); `decide()` unchanged from ab4 (R_LOOP decides, R_B reported). Message ids counted once (`transcript_info`).
- D3: `decision.json` N_HAIKU / haiku / HAIKU_ENABLED=false; `build --stratum haiku` refuses with a message; names d5h-/d5fh-, Haiku models (`expected_model`), `haiku_stratum()` kept; AUD/AUD2 always Sonnet (`expected_model` + assert in advance); stratum + model on every record and ledger line.
- D4: `decision.json` N_EXTEND / MIN_COMPLETED; `build --extend --variant X` once per arm, only if `metrics.json[X].sonnet` records n=6 + extension_eligible.
- D6: `rules.DROP2_RLOOP_LIMIT = 2.69` (ab4); cost enters only `decide()`; no token check, kill or abort in advance/harness/full (test greps).

## Tests
`cd $SP/p18/ab5 && python3 tests/test_ab5.py` -> **18/18 passed** (mutation check: removing the VF-reject `ledger.defer` fails 2 tests; putting the sweep on every reviewer fails 3). Covered: panel template has exactly one reviewer per tier t1b, t2, t3, t4 and the same compute as PN1's; byte identity of every copied file and the frozen hashes; rules wording (rebuildable); resolver + PN1 template = PN1's real panels; no Tier 0 / no Opus anywhere (steps, panels, ledger, code); mock -> live switch changes only model fields and lane labels; panel briefs (4 reviewers, tiers, models, stand_in, lint value + file in each sandbox, AC sweep only on t1b-1, no t1a); names / strata / Haiku refusal / interleaving / D4 extension; ids parsing on real ab4 run reports and PN1 reports (8 of 12 PN1 round-1 reports agree with their findings block; the 4 known disagreements are listed); merge over 4 reports (clean, sources, dedup into one M1 with 4 sub-entries, one lost reviewer); ADJ prep (panel blind input + mapping; full over all ledger rows); VF contamination guard (prep refuses, advance does not launch); confirmed-line authority (parse and ingest); token matcher (pasted, wrapped, short path, sandbox-dir path, dotted step names, wrong model ignored, max per id); lanes from data and models from telemetry; D2/D6 constants; a full fake loop R1 -> merge -> ADJ + VF1 -> V1 -> R2 -> VF2 -> V2 -> R3 -> VF3 -> AUD/AUD2 -> analyze for the **panel** arm, and for the **full** arm (M1 ledger REVISE, VF1 rejects 2 rows -> deferred, fix map -> L1 resolved_check, R2 in PN1 sandbox with prior/base/lint-2, M2 clears/keeps/opens rows, L2, R3, M3 ESCALATE -> VF3 -> VERIFIED-PASS, telemetry records, analyze lanes).

## Dry run (real directory; nothing launched, no launch ledger written)
```
python3 harness.py build --stratum sonnet --variant panel   # built d5-r1..r6
python3 harness.py build --stratum sonnet --variant full    # built d5f-r1..r6
python3 harness.py build --stratum haiku                    # refused (Sonnet stratum only)
python3 advance.py --dry-run                                # PROMPT-R1.<rid>.md x4 + lint-1.md in all 12 runs; state.launched {} everywhere
```
First LAUNCH lines `./drive.sh p18/ab5` will print (24, 6 runs; paths relative to $SP):
```
LAUNCH p18/ab5/runs/d5-r1/PROMPT-R1.t1b-1.md model=sonnet
LAUNCH p18/ab5/runs/d5-r1/PROMPT-R1.t2-1.md model=haiku
LAUNCH p18/ab5/runs/d5-r1/PROMPT-R1.t3-1.md model=haiku
LAUNCH p18/ab5/runs/d5-r1/PROMPT-R1.t4-1.md model=haiku
LAUNCH p18/ab5/runs/d5f-r1/PROMPT-R1.t1b-1.md model=sonnet
LAUNCH p18/ab5/runs/d5f-r1/PROMPT-R1.t2-1.md model=haiku
LAUNCH p18/ab5/runs/d5f-r1/PROMPT-R1.t3-1.md model=haiku
LAUNCH p18/ab5/runs/d5f-r1/PROMPT-R1.t4-1.md model=haiku
... then d5-r2, d5f-r2, d5-r3, d5f-r3 (4 each)
```
Per arm: `python3 advance.py --dry-run --variant panel` starts with the d5-r1 lines above; `--variant full` with the d5f-r1 lines. Lint-1 has 0 findings (REF check) on the original spec in every run, as in ab4.

## Deviations from the sources (all)
0. Panel template: t1b, t2, t3, t4 (one per tier) instead of PN1's t1b, t2, t3, t3 (owner correction); same compute in the mock.
1. Rules: panel arm "three" -> "four" (5 places) instead of ab4's "two"; full arm = PN1 product rules + PN2 lint bullets (item 4).
2. Merge (panel arm) is ab4's markdown merge over 4 reports, not PN1's ledger merge (BRIEF: "PN1's merge ... with ab4's cleaned finding_block/clean_body"); PN1's merge needs findings blocks that the ab1-lineage rules do not ask for. The full arm has PN1's real ledger merge.
3. ADJ on Sonnet, not Fable (OWNER RULE): changed condition vs PN1.
4. Panel arm ADJ input = cleaned merged blocks, not ledger anchors/claims (no ledger in that arm). Full arm = PN1 prep_adj logic.
5. VF-rejected rows are parked with `ledger.defer` in the full arm (PN1 has defer only as a human command).
6. `resolve_short` / prompt table step-name pattern widened to `[\w.-]+`; DIR_STEP extended (item 10).
7. `unlaunch` keeps a step's `finding_ids` / ADJ map when it drops the log (ab4 dropped them, so a relaunched VF would have verified an empty list).
8. Lost-step rules: PN1's per-reviewer rule for the panel, ADJ loss does not lose the run (item 9).
9. Concurrency: run-level cap (6 runs) instead of ab4's 6 launches; arms interleaved.
10. PN1 telemetry: the full arm writes PN1's `review-telemetry/1` reviewer record (`telemetry-<step>.json`) next to the run but does not append to the PN1 clone's shared telemetry dir, and `task` (from `telemetry taskvars`) is not computed. The panel arm records reviewer/slot/model on the step record only.
11. PN1 vendored package `__init__.py` replaced by an empty shim; product code called in-process instead of through `uv run superclaude review ...`.
12. `analyze` writes `RESULTS.md` (ab4 wrote `RESULTS-tables.md`), one section per arm; ab4's "d4 vs ab1" pointer dropped.
13. `drive.sh`: per-directory head limit (item above).

## Open questions
1. Concurrency reading: "6 runs at a time" implemented as 6 runs in flight (up to 24 agents on the first call). If ab4's cap of 6 concurrent launches was meant instead, a launch cap has to be added (`AB_MAX` only lowers the run cap).
2. ADJ order in the full arm: parallel with VF1 (default) or strictly before it (`ADJ_GATES_VF1: true`)?
3. VF-rejected ledger rows stay `deferred` even if R2/R3 refind them (item 8c). Alternative: un-defer on refind (PN1 marks only resolved rows regressed).
4. `ids_from` misreads 4 of 12 PN1-format reports (Medium ids from "(M1-M5)" prose, or none). Harmless in the full arm (findings block decides) and the panel arm's ab1-lineage reports are ab4-format; kept byte-identical as instructed.
5. Rules wording still says the panel is resolved by `superclaude review panel resolve` (full arm, PN1 text) and "four first reviews" (panel arm); neither names tiers, so the t4 change needs no rules edit.
6. In live mode the transcript model of a GPT/GLM reviewer is unknown; `pick()` matches the expected launch alias as a substring of the transcript model, which may need a per-alias match string in live_alias_map.
7. D4: as in ab4, `analyze` with fewer than 5 completed runs records INCONCLUSIVE + extension_eligible, so do not run `analyze` before the runs finish (or `build --extend` would be allowed early).
8. The baseline second audit / Haiku baseline paths are ab4's; absent -> PROVISIONAL / pending, as ab4.
