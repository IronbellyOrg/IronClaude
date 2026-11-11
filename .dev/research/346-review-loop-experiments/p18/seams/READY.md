# ab6 offline replay of the Jev seams A1, A2, A3: READY (mock-verified, nothing live has run)

SP = /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad ; build root = $SP/p18/seams.  Python stdlib only.
Tests: `cd $SP/p18/seams && uv run --no-project --with pytest pytest tests -q` -> **40 passed** (about 40 s).  No Jev call was ever made, the key was never read,
no model (Fable, Opus, Sonnet) was used by any of this code.  All tests use the mock transport; one test rehearses the `--live` branch with a patched network
layer and a fake key.

## Files
| file | role |
|---|---|
| `seamlib.py` | shared glue: spec parsing on the PN2 lint parser, `scrub` (the privacy guard refuses owner names, home paths, repo URLs), mock transport (modes ok, insufficient, malformed, timeout, http500, wrongmodel, mixed), `Runner` (J-budget pre-flight, reserve, journal, cache), answer validation (`outcome`: anything but a valid non-`insufficient` option is a fallback) |
| `a2_observability.py` | A2: row extraction (32 rows on the original), widened lint, D20/D21 regexes, scratch execution with mutation probes, Jev question `observability`, 8-line UNVERIFIED output, control packets |
| `a1_support.py` | A1: obligation / criterion extraction, capped deterministic prefilter, Jev question `support`, 12-hint rendering, keyword-prefilter control, control packets |
| `a3_novelty.py` | A3: V1-diff analysis (`named_not_touched`, overlap), Jev question `v1_attempt`, flag lines, V2 hint merge (cap 15), PN1 survivor-case loader, blind label packets |
| `replay.py` | driver: dry run (default), `--mock`, `--live`, `--control-export`; per-spec JSON `ab6-replay/1` |
| `score_gates.py` | kill-rule metrics against the ledger: A1, A2, A3 separation test, triage (a/b/c) |
| `decision.toml` | ceilings ($5 / 30M tokens offline, J4), caps (60 pairs, 12 hints, 8 lines, 15 merged), packet limit 12,000 bytes, the judges' thresholds |
| `tests/test_seams.py`, `tests/conftest.py` | 40 tests |
| `out/` | clean: dry-run packets (`*.dry.json`, `preflight.json`), **control packets + Sonnet judge prompts** (`out/a1/control`, `out/a2/control`), A3 `cases.json` and blind label packets (`out/a3/label-packets`), and the finished code-only `out/triage/` |
| `out-mock-sample/` | a full mock run of everything (every file says `"mode": "mock"`; the gates say MOCK). Plumbing only, not evidence; do not read results from it |

## How the coordinator runs each step
```bash
export SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad ; cd $SP/p18/seams
# 0. dry run: builds every packet, checks privacy/size, prints the reservation; no key, no network object
python3 replay.py --seam all
# 1. conventional controls (no Jev; can start now): one Sonnet worker per spec and seam on the IDENTICAL packets.
#    prompts: out/a1/control/PROMPT-<sid>.md and out/a2/control/PROMPT-<sid>.md (13 + 13 workers); each writes out/<seam>/control/<sid>.answers.json
#    (re-export with: python3 replay.py --seam all --control-export; A3 has no judge arm: its controls are code facts)
# 2. live replay, cheapest first (key only inside the single command, contract J2):
bash -c 'set -a; . "$SP/.jev.env"; set +a; cd $SP/p18/seams && python3 replay.py --seam a3 --live'   # 10 calls
bash -c 'set -a; . "$SP/.jev.env"; set +a; cd $SP/p18/seams && python3 replay.py --seam a2 --live'   # 352 calls
bash -c 'set -a; . "$SP/.jev.env"; set +a; cd $SP/p18/seams && python3 replay.py --seam a1 --live'   # 780 calls
# 3. key scan after every live run (contract J2); add $SP/p18 to the default paths
bash -c 'set -a; . "$SP/.jev.env"; set +a; cd $SP/p15/jev && python3 keyscan.py $SP/p18 $SP/p15 $SP/central'
# 4. gates (A1/A2 pick up out/<seam>/control/<sid>.answers.json automatically, or pass --judge-dir)
python3 score_gates.py --seam all           # writes out/<seam>/gates.json and GATES.md
```
`--live` pre-flights every request with `live=False`, reserves estimate x 1.2 before the first paid call (does not fit: `BLOCKED-BUDGET-<seam>.json`, exit 5, no call),
journals to `journal/jev-<seam>.jsonl`, caches validated answers in `cache/` (a re-run costs nothing), writes `manifest-<seam>.json`, and exits 3 when the key is missing
(before any network) or rejected.  A draw that fails after the reservation is a recorded `refused/budget_exhausted` fallback, never a stop (D6).  A3 optional: have a
blind labeller answer `out/a3/label-packets/<case>.md` and save `{case_id: label}` as `out/a3/labels.json` (the table then shows it).

## Forecast for the 13-spec replay
| seam | requests | input tokens (bytes/3, the adapter's own estimate) | $ at 0.042/Mtok | reservation (bytes/2 x 1.2) |
|---|---|---|---|---|
| A1 (60 pairs x 13 specs) | 780 | 612,262 | 0.026 | 1,101,817 ($0.046) |
| A2 (27 +/- 1 rows past the code stage x 13) | 352 | 225,889 | 0.010 | 406,499 ($0.017) |
| A3 (10 PN1 survivors, 5 specs) | 10 | 19,297 | 0.001 | 34,730 ($0.0015) |
| **total** | **1,142** (+ at most one retry per transient failure) | **857,448** | **about $0.036** (bytes/4 gives 642k tokens, $0.027) | **1,543,046 ($0.065)** of the $5 / 30M ceiling |

Judges expected about 1,300 calls and about $0.03: we are at 1,142 calls and $0.03 to $0.04.  Probe latency was 160-375 ms per call, so a sequential run takes roughly 4-8 minutes.
Control arm: 26 Sonnet workers read the same 1,132 packets (about 0.6-0.9M input tokens, small output).  Offline labelling of A3 cases: 10 short packets.

## Results that already exist (code only, valid without Jev)
* **Triage (Opus J1), `out/triage/`**: the 117 residual T1 (defect, spec) cells of the 12 finals are 5 (a) in the reviser's brief, 6 (b) raised but rejected (ab4 VF), **106 (c) never raised
  as a blocking first-review finding** (ab4 56 c / 4 a / 6 b; PN1 50 c / 1 a / 0 b).  Blocking defects only: 42 (c), 5 (a), 4 (b); (c) blocking is **3.5 per spec** (ab4 20 over 6 specs, PN1 22 over 6),
  so by Opus J1's own rule A1 is not a shadow-only candidate on headroom grounds.  4 of the 106 (c) cells were raised by that run's frozen audits.
* **A2 controls**: the D20 and D21 regexes agree with the scorer's status on all 13 specs (D20: flagged on the 12 PRESENT specs, not on the one FIXED; D21: flagged on all 13, residual in all 13).
  On the original, the code stage alone flags 5 of 32 rows: AC-C1, AC-C4 (D21 plus a planted-violation probe showing the table-source copy behaves differently), AC-C5, AC-0.3 (D20, D21, and the
  deleted-bullet probe is not caught), AC-0.4 (widened lint PHASE = D11, and the step-4 YAML assertion exits 1 on a markdown report = D12).  27 rows go to Jev.  Widened lint flags lines 83, 92, 194 only.
* **A1 prefilter (code only)**, T1 class, residual cells (106 pairable cells): pair-level recall **28.2%** of 412 relevant pairs; defect-cell recall (at least one relevant pair emitted) **67.9%**
  (T1+T2: 27.5% / 71.2%; all 44: 25.1% / 63.2%).  Against the 70% gate: **pair-level FAILS, defect-cell level FAILS narrowly (67.9%)**.  Recall rises with the cap: 90 pairs 36.9% / 73.6%,
  120 pairs 40.5% / 73.6%, 250 pairs 51.2% / 75.5%, 400 pairs 57.8% / 82.1% (`recall_curve_T1_residual` in `out/a1/gates.json`, regenerate with score_gates).  Unpairable defects (a side
  of the pair is not an id in the defect text): D13, D14, D31, D40.  This agrees with the advocate's own estimate (61%).  The raw space is 70 obligations x 37 criteria = 2,590 pairs; 562 are eligible on the original.
* **A3 reconstruction**: all 10 survivor cases rebuilt, 2 resolved (b1-r4-L2, b1-r6-L2) and 8 failed; all 10 were touched by V1 (so `named_not_touched` computed on V1 is 0 of 10 by construction);
  the advocate's "five named_not_touched" is the post-V2 ledger event (b1-r1 L1 and L9, b1-r4 L1 and L5, b1-r5 L1), which is not known before V2: it is kept as a control (`v2_named_not_touched`), flattering to the control.

Everything about Jev's answers (false flags, beyond-control catches, tail catches, A3 separation, ties with the judge) needs the live replay plus the Sonnet answers; the mock numbers in
`out-mock-sample/` are random.

## Definitions I had to choose
1. **Relevant pairs of a defect (A1)**: obligation ids x criterion ids named in the SAME sentence/clause of the defect text (title, quote, each sentence of what_goes_wrong / is_fixed_when); obligations = WC-n, SA-n,
   open decisions D1-D5, command names (`/sc:x`, backticked, or distinctive bare names); criteria = AC ids, "step n" (= 7.2 live-check step n), "Pn gate/scope/Commands/row" (= phase gate Pn); only ids that exist in the
   scored spec.  The first run used the LOOSE definition (every named obligation x every named criterion of the whole text): pair recall was 22.8%, defect-cell 67.5%; the loose numbers stay in `gates.json` beside the primary ones.
2. **Recall**: pooled over the residual cells (defect not FIXED/DELETED_OK in that spec) of the strict T1 class (15 defects from the A1 advocate: D01 D03 D04 D05 D11 D12 D13 D14 D26 D27 D28 D38 D39 D40 D44), pair level and defect-cell level both reported.  The original has no scorer output: every defect counts PRESENT.
3. **T1 residual cells = 117** (checked: 66 ab4 + 51 PN1).  The design file calls them "117 residual blocking cells"; they include non-blocking T1 defects (blocking only: 51 cells).
4. **Flag classes**: true / false / unmapped (see `score_gates.py` docstring).  "False flag" is exactly the judges' rule (a hint on a defect the ledger marks FIXED/absent in that spec); unmapped flags (no ledger defect maps) are reported as a worst-case bound (`max_incl_unmapped_bound`), not counted false.  In practice many A1 flags will be unmapped because the ledger names only 44 defects.
5. **Beyond-control catch (A1)**: a residual BLOCKING defect that a shown Jev hint maps to and that neither the widened lint (line overlap) nor the keyword prefilter (phase mismatch or deferral lexicon) maps to.  Note: A2's regexes (D20, D21) are not in A1's control set as the brief defines it, so D20 can count as an A1 catch.
6. **Row to defect mapping (A2)** is by line (defect lines mapped orig -> scored spec with difflib; a replaced block maps proportionally), as the advocates did.  It credits the controls generously (a lint flag on AC-0.4 counts as catching D11, D12 and D14 alike).
7. **A2 tail catch**: distinct tail defects (D14-D19, D23, D37-D40, D44) that are residual in some spec, whose rows carry a Jev `cannot_pass`/`cannot_discriminate` and NO control flag on any mapped row.  The second kill clause (flag on a row "labelled passable") needs independent row labels, which do not exist: the proxy is "Jev-flagged rows with no residual mapped defect", an upper bound on false flags.
8. **A2 UNVERIFIED lines exclude lint flags** (they are already in lint-N.md through the free widening F1); one line per row, code flags (execution, D20/D21) before Jev `cannot_pass` before `cannot_discriminate`, cap 8.
9. **Rows past the code stage**: a row goes to Jev only when lint, D20, D21 and every execution probe raised nothing; rows whose commands cannot run offline (make, uv run pytest, ORCA, gh, placeholders) pass the code stage and go to Jev.  Execution is limited to grep / test / cmp / read-only git and the YAML snippet, in a fresh scratch fixture per row (deleted afterwards), never in the repo.
10. **A1 packet** = one (obligation, criterion) pair, texts clipped to 900 chars, code signals, and the obligation's own phase-gate row; one question per request.  **A2 packet** = the row, up to 4 cited rows (WC/SA/AC/7.2 step), and the code-stage facts.  **A3 packet** = up to 4 V1 hunks around the quoted lines, the R2 re-raise, and code facts; the R3 outcome is never in any packet.
11. **A3 survivor** = blocker in the round-1 AND round-2 brief of a PN1 run that reached V2.  Outcome = absent from the round-3 brief (resolved) or present (failed).  Separation = among cases the controls do not mark (post-V2 `named_not_touched` false), the set of Jev labels of the resolved cases is disjoint from the set for the failed cases, both non-empty and all answered; Fisher exact p for three one-predictor tables is printed.
12. **Option answer** is the argmax `choice` only; probabilities and confidence are recorded, never gate (J7).  Choice questions with an `insufficient` option follow the brief; J7 prefers Noul plus companion, so this is a stated deviation from the contract's preference (the debate fixed the option sets).
13. **Data classes**: spec rows `s1_spec`, R2 reports / diffs `stage2_artifact`.  Every packet passes `scrub()` (owner/repo names, absolute paths, URLs, e-mail-like strings replaced by `<fork-repo>`, `<abs-path>`, ...) so the guard does not refuse AC-2.4 / AC-4.x rows.  Zero privacy refusals in the dry run.
14. **Triage classes** (a) VF-confirmed in the ab4 reviser brief / in the PN1 round-1 brief, (b) raised as a blocking first-review finding but rejected, (c) not raised as a blocking first-review finding of that run (findings keyed by (arm, run): run names repeat across arms).
15. **Python**: `python3` (brief); the modules also run under `uv run --no-project python`.  A2's YAML execution picks the first interpreter with PyYAML (sys.executable, python3, /usr/bin/python3) and records "not executed" if none has it.

## What I could not reconstruct or did not do
* **Triage**: only first-review BLOCKING findings are in `p17/findings.jsonl`.  Non-blocking mentions and the R2/R3 reviews have no finding-to-defect mapping, so (c) overstates "never raised" (4 of the 106 (c) cells were raised by the run's frozen audits).  The finding-to-defect link is the p17 reconciler's clustering (`sources` of each ledger defect) and a finding can map to several defects.  PN1's tier provenance and the ADJ decision per finding are not separable from the merged ledger rows; (b) for PN1 is "blocking in the merged table but not in the round-1 brief".
* **A3 cases**: all 10 PN1 survivors, from `p13/ab1/runs/b1-r{1,2,4,5,6}` (b1-r3 passed at R2 and has none).  Not available: any ab4 case (no ab4 run reached V2), the "extra V1-to-V2 pairs from the 69 FAIL reports of p12/ab1 and p13/ab2" the advocate mentions (no ledger or history there that I could rebuild), and any blind relabel (needs workers).  With n=10 and 5 control-undecided cases the separation test has almost no power.
* **Conventional same-packet judge results** and **independent row labels for A2** do not exist yet; the tie/kill clauses that depend on them print `null` until the coordinator runs the judges.
* **"VF-accepted findings" for A1** in the replay: none is supplied by default (the replay scores the final spec, there is no VF stage), so no pair is dropped as covered; the mechanism is tested (`--accepted-dir <dir>/<sid>.json`).  This makes the replayed hint load an upper bound.
* The seams re-run before R2/R3 (second pass on changed rows) is not replayed; only the first pass on each spec is.
* A prefilter variant (risk-weighted, at most 2 pairs per row, `phase_equal` worth nothing) was built once after the first recall number and was WORSE (pair 17.5%, defect-cell 58.5%); it was reverted.  The shipped prefilter is the first version.  Its parameters (cap 60, WC quota 24, token threshold 3.0) were fixed before any recall was measured, but the recall of any version is measured on the same ledger the design was reasoned from.

## Open questions for the coordinator
1. **A1 recall gate**: the strict pair-level gate (70%) fails at 28%, the defect-cell level narrowly (67.9%).  Which one is the judges' gate?  The brief says "share of relevant pairs" (pair level), under which A1 is dead before any Jev call; at cap 90 the defect-cell level passes (73.6%) at +50% calls (about 1,170 A1 calls, +$0.013).  Do you want the live A1 run at cap 60 only, or also at cap 90?
2. Should the A1 live run wait for the Sonnet judge answers (the "not tied" test needs them), or run Jev first and judge after?  The judge prompts are ready.
3. A2's second kill clause needs independent row labels (about 7 labellers per the advocate, 274 unique rows); worth ordering now, or accept the proxy (flags on rows with no residual defect)?
4. A1 hints on a spec with no VF stage: confirm that scoring the final specs without an accepted-findings list is the intended replay.
5. Mixed-model answers: Jev `confidence` and probabilities are stored; if you want a probability floor for showing a hint (J7 forbids using confidence as a gate), say so before the live run, not after.
