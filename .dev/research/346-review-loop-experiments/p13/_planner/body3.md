# PLAN PN3 (S3): capture-recapture estimate of remaining defects as a stop rule

You test ONE idea from research report 2, Part C: treat independent whole-document reviewers as capture occasions, deduplicate their findings into defects, and estimate how many blocking defects nobody has found yet (Lincoln-Petersen for 2 lists, Chao2 and the first-order jackknife (Mh) for k lists); stop the loop only when the estimated remainder is indistinguishable from zero. The report's "cheapest falsifying experiment" needs no new model run: about 15 independent first reviews of the SAME original spec already exist. You (1) build the shared defect catalog from those reports with a dedupe that is verified against quotes, (2) run the falsification offline, (3) ship a pure estimator `superclaude review estimate`, (4) prepare a shadow analysis of PN1's live panel data and, only if the gates pass, a live arm. The appendix holds the SHARED CONTRACT (C0-C9): binding, wins over this text.

## 0. Read this first

Read the whole file before running anything. Do not open the other plans.

Hard rules (from `/home/user/IronClaude/CLAUDE.md`, binding):
- Python only through UV (`uv run ...`; scratch scripts `uv run --no-project python <file>`; their tests `uv run --no-project --with pytest pytest <dir>`). Never `pip`, `python -m`, bare `python`.
- Never stage or commit anything under `.claude/` (`git add -f` = violation). Edit only `src/superclaude/` and `tests/`; then `make sync-dev`, `make verify-sync`.
- PN3 does not change the rules file, `spec-panel.md` or any installed primitive. The stop rule is not adopted into the prompts before it passes its tests.
- Work only in your full clone `$CLONE`; never edit `$SP/p11/`, `$SP/p12/`, `$SP/p13/ab1/`, `$SP/p13/clones/pn1/`.
- Push to `origin` (`https://github.com/IronbellyOrg/IronClaude`); no pull request; never touch `SuperClaude-Org/SuperClaude_Framework`.
- You cannot spawn sub-workers. Do Phases O1-O3 yourself and report the numbers; build the shadow script and the (gated) live harness; push; STOP with the READY report.

```bash
export SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
export CLONE=$SP/p13/clones/pn3 AB=$SP/p13/ab3 BR=346Claude-pn3-capture-recapture CAT=$SP/p13/catalog
```

## 1. Background and the data you have

Baseline loop and harness: Stage 2 arm 3 (read `$SP/p11/harness.py`, `$SP/p11/advance.py`, `$SP/p11/runs/a3-r1/PROMPT-{R1,V1,R2,AUD}.md`). Baseline: 6/6 PASS, 2.17 reviews, growth +1.41%, `B_TOK` ~169,000 output tokens per replicate (C9.1, each message id once), `B_BLK` 1.50 over 12 audits.

All 15 Stage 2 runs started from the same original spec (`SPEC_SHA`), so their first reviews are independent captures of one document:
- 12 primary occasions, same instrument (sonnet + FIRST-REVIEW prompt): `$SP/p11/runs/a2-r{1..6}/ws/.dev/orca-command-refactor/review/round1.md` and `$SP/p11/runs/a3-r{1..6}/ws/.dev/orca-command-refactor/review/round1.md` (a2-r3's R1 is a PASS with no blocking finding: a valid empty capture).
- 3 sensitivity occasions, a different instrument (master command, original briefs that called every finding blocking): `$SP/p11/runs/a1-r{1,2,3}/ws/.dev/orca-command-refactor/review/spec-panel.md`.
- Validation only (they reviewed revised finals, not the original): 15 first audits `$SP/p11/runs/*/aud/ws/.dev/orca-command-refactor/review/audit.md` and 6 second audits `$SP/p12/baseline-audit2/a3-r*/ws/.dev/orca-command-refactor/review/audit.md`; the finals themselves `$SP/p11/runs/*/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` and history `specs/history/spec-v*.md`.

Things that make this hard (say them in RESULTS.md): the 12 primary occasions are one model with one prompt, so detection is correlated across occasions and every estimator here is a lower bound (Kim et al. 2025, report-cited, UNVERIFIED); defects have very unequal detection probability (by C9.3 tags T1 is in nearly every R1, T2 in about a third), which is why Mh estimators are used; a re-review is scoped to changed lines, so only whole-document reviews are valid occasions (C7); and the "truth" is itself made of the same kind of review.

## 2. Pre-registered criteria

Definitions over the catalog (O1): a capture = a primary-occasion blocking finding mapped to a cluster; `S_obs(k)` = distinct clusters captured by a set of k occasions; `S_ref` = distinct clusters in the whole catalog that are not revision-introduced (all 36 sources: 15 R1 + 21 audits); `S_conf` = confirmed clusters (C9.4). For a k-subset, an estimator gives `N_hat` and a 95% interval.

**F1, held-out prediction (primary falsification test).** For k = 2, 3, 4, 6, over all k-subsets of the 12 primary occasions (or 500 subsets drawn with `random.Random(k)` when there are more): `MAE_obs(k)` = mean |S_obs - S_ref|; `MAE_est(k)` = mean |N_hat - S_ref| for Chao2 and for Jackknife-1 (and Chapman's Lincoln-Petersen at k = 2); `COVER(k)` = share of subsets whose interval contains `S_ref`.
- FALSIFIED at k = 4 if, for both Chao2 and Jackknife-1, `MAE_est(4) >= MAE_obs(4)` or `COVER(4) < 0.5`.
- SUPPORTED at k = 4 if an estimator has `MAE_est(4) <= 0.7 * MAE_obs(4)` and `COVER(4) >= 0.7`.
- Otherwise WEAK. Repeat with `S_conf` as the reference (secondary).
- Because `S_ref` is itself a lower bound, also report the full-data estimate on all 12 occasions with its interval; an estimate far above `S_ref` is not by itself a failure.

**F2, the report's per-run test (secondary, reported, not decisive).** For each of the 12 arm-2/3 runs: predicted residual = `N_hat` from the other 11 occasions (leave-one-out, Jackknife-1) minus clusters the run fixed (its R1 blocking clusters whose original span a hunk of V1 or V2 touched, C5 span mapping); observed residual = distinct non-revision-introduced clusters among its audits' blocking findings. Spearman rho with ties. Read: rho <= 0 is consistent with falsification. Why it is weak: with a leave-one-out `N_hat` almost equal for every run, the prediction varies only with the number fixed, so it tests "more fixed means fewer left", not the estimator.

**F3, shadow calibration on PN1's live panel (free, when `$SP/p13/ab1/runs/b1-r*/` completed).** Per run, the round-1 capture matrix of its 4 reviewers (blocking only) gives Chao2 / Jackknife-1 `unseen_upper95`; observed residual as in F2 (PN1 audits). CALIBRATED if observed residual <= predicted upper remaining (`unseen_upper95` plus clusters not fixed) in at least 5 of the completed runs (at least 5 required). Note: three of the four reviewers are the same model (haiku stand-ins), so underestimation is expected.

**Gate for the live arm `c3`:** F1 SUPPORTED, and F3 CALIBRATED if PN1's data exists (if it does not, F1 alone, and say so). Otherwise the live arm is not run and the result is the offline decision.

**Live decision (arm `c3`, n=6):** `BLK_T`, `PASS_T` (ESCALATE counts as not PASS), `GROWTH_T`, `R_TOK = TOK_T / B_TOK` (loop + AUD, C9.1).

| Rule | Condition |
|---|---|
| DROP | `BLK_T > 0.8 * B_BLK` (1.20), or `R_TOK > 3.3`, or `PASS_T < 4/6` |
| ADOPT | no DROP, `BLK_T <= 0.5 * B_BLK` (0.75), `PASS_T >= 5/6`, `R_TOK <= 2.5`, `GROWTH_T <= 2.82%` |
| INCONCLUSIVE | anything else; fewer than 5 completed runs; arm means of AUD and AUD2 differ by more than 0.75 |

Pre-registered prediction: the stop rule will often demand another whole-document panel round, and with the cap of 3 many runs will ESCALATE; `R_TOK` about 3.3. Write this prediction into RESULTS.md before analyzing.

## 3. Phase O1: the defect catalog (shared deliverable, C9.4), verified against quotes

Scripts in `$AB/offline/`, output `$CAT/catalog.json` (create `$CAT`), plus `$CAT/catalog.md` (human-readable) and `$CAT/BUILD-NOTES.md`.

1. **Extract** (`extract.py`, mechanical): for each source report, blocking findings by C9.3 (`parse_ids(ids_from(path))` when the verdict is FAIL; `find_section`; `tag`; `cited`). For each finding collect candidate quotes: backticked spans and double-quoted spans of at least 12 characters in its heading and body. Write `findings_raw.jsonl`: source (`<run>/R1`, `<run>/AUD`, `<run>/AUD2`), fid, heading, theme, cited lines, quotes.
2. **Anchor** (`anchor.py`): the reviewed document = the original for R1 sources, the run's final spec for audits. For each quote, `locate` (C5) in the reviewed document; then locate the same quote in the original. Original span = the first located quote's span in the original; if no quote locates in the original but one locates in the final, map its final span to the original with C5 span mapping (`difflib` opcodes final -> original) only when the mapped lines are `equal` lines, else mark the finding `revision_introduced`; R1 findings with no locatable quote use their cited lines as the span when the cited lines exist in the original; anything left is `unanchored` (with the reason). Print, per source, how many findings anchored by quote, by cited line, or not at all.
3. **Cluster** (`cluster.py`, mechanical): union-find over anchored findings: join when themes are equal and not `other` and original spans are within 3 lines; or when the Jaccard of their original line sets is at least 0.5. Cluster order = first member order; ids `D1..Dn`.
4. **Adjudicate** (you, by reading): for every cluster, read the members' headings and bodies; split a cluster whose members name different wrong outcomes, merge clusters that name the same wrong outcome, move misplaced members. Every override goes into `overrides` with a one-line reason and a quote from the original that shows it. Each cluster gets a `label` (the wrong outcome, at most 12 words) and an `anchor` (an exact quote from the original that `locate` finds; assert it).
5. **Confirm and residual:** `n_sources` = distinct sources among members; `confirmed` = at least 2 (C9.4). For each run, `residual.present` = clusters whose anchor still locates in its final spec or that its audits report; `audit_hits` = clusters per audit.
6. **Report** in `BUILD-NOTES.md`: counts of findings, anchored (quote / cited / none), revision-introduced, clusters before and after adjudication, overrides, confirmed clusters, and a 20% random sample (`random.Random(0)`) of cluster memberships you re-checked a second time with the result. PN1 and PN2 read this file if it exists; write it atomically (temp file + `os.replace`) and never change it after publishing except by a new version `catalog-v2.json`.

## 4. Phase O2: estimators (product code) and Phase O3: falsification runs

### O2. `src/superclaude/cli/review/estimate.py` (stdlib only, pure) and `estimate_cmd.py`

Input: a C7 capture file. With `k` occasions and per-defect capture counts, let `Q_j` = number of defects captured by exactly j occasions, `S_obs` = defects captured at least once, `q_i` = defects captured only by occasion i, `A = (k - 1) / k`.
- Chapman-Lincoln-Petersen (k = 2 only): `N = (n1 + 1)(n2 + 1)/(m + 1) - 1`, `var = (n1 + 1)(n2 + 1)(n1 - m)(n2 - m) / ((m + 1)^2 (m + 2))`, normal interval.
- Chao2 (bias-corrected): `f0 = A * Q1^2 / (2 Q2)` if `Q2 > 0`, else `A * Q1 (Q1 - 1) / 2`; `N = S_obs + f0`. Variance for `Q2 > 0`: `Q2 * (A/2 * r^2 + A^2 * r^3 + A^2/4 * r^4)` with `r = Q1/Q2`; for `Q2 = 0`: `A*Q1(Q1-1)/2 + A^2*Q1(2Q1-1)^2/4 - A^2*Q1^4/(4 N)`. Interval: log-normal, `T = N - S_obs`, `C = exp(1.96 * sqrt(ln(1 + var / T^2)))`, `[S_obs + T/C, S_obs + T*C]`; `T = 0` gives `[S_obs, S_obs]`.
- Jackknife-1 (Mh, Burnham-Overton): `N = S_obs + A * Q1`; `var = A * (sum_i q_i^2 - Q1^2 / k)`; normal interval clipped below at `S_obs`.
- Jackknife-2: `N = S_obs + Q1 (2k - 3)/k - Q2 (k - 2)^2 / (k (k - 1))` (point estimate only).
- `unseen_upper95` = max over Chao2 and Jackknife-1 of (interval upper - `S_obs`). Stop rule: `stop = open_blocking == 0 and unseen_upper95 < 1.0`; `k < 2` gives `stop = null` and the reason `insufficient occasions`.

These formulas follow Chao (1987), Burnham and Overton (1978) and the EstimateS user guide as the planner recalls them: UNVERIFIED. If you can reach the web, check each against a primary or library source (for example scikit-bio's `chao1` for the abundance analogue) and record the check; otherwise record "not verified against a reference" in the READY report. Tests pin hand-computed values for at least 5 small matrices (including `Q2 = 0`, all defects captured once, all captured by every occasion, k = 2).

CLI: `superclaude review estimate CAPTURE.json [--blocking-only] [--open-blocking N]` prints `{"schema": "review-estimate/1", "k", "S_obs", "Q": {...}, "chapman": {...} or null, "chao2": {"N", "f0", "var", "ci95"}, "jackknife1": {...}, "jackknife2": {"N"}, "unseen_upper95", "stop", "reason", "rule": "<the stop rule text>"}`; exit 0, exit 2 on an invalid capture file. Add the C0.1 `__init__.py` and C0.2 `main.py` lines. Tests (write first): `tests/review/test_review_estimate.py` (formulas, rule, edge cases, invalid input, determinism, CLI via `CliRunner`).

### A. Clone, verify, commit, push

```bash
mkdir -p $SP/p13/clones $AB $CAT
git clone /home/user/IronClaude $CLONE && cd $CLONE
git remote set-url origin https://github.com/IronbellyOrg/IronClaude
git fetch origin 346Claude-p8a-first-review-grading || echo "FETCH FAILED: continuing on the local copy of the branch"
git checkout -b $BR origin/346Claude-p8a-first-review-grading
test "$(git rev-parse HEAD)" = 69ac8b3335564fb5551980e984c5d9b763039cc1 && echo BASE-OK \
  || { echo "origin moved past 69ac8b33: staying on 69ac8b33"; git checkout -B $BR 69ac8b3335564fb5551980e984c5d9b763039cc1; }
git remote -v && uv venv && make install
uv run pytest -q tests/cli/test_cli_registration.py                     # PINNED_BEFORE
# ... write tests, implement ...
uv run pytest -q tests/review && uv run pytest -q tests/skills tests/cli tests/unit
make lint && make sync-dev && make verify-sync
git status --short        # only src/superclaude/cli/review/{__init__,estimate,estimate_cmd}.py, cli/main.py, tests/review/**
git add src/superclaude/cli/review src/superclaude/cli/main.py tests/review
git commit -F - <<'EOF'
experiment(review): capture-recapture estimator for remaining review defects (PN3, refs #346)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Y28dBfZHbPhB1U1EM1XTUj
EOF
git push -u origin $BR || echo "PUSH FAILED: report it"
git rev-parse HEAD        # PRODUCT_REF
```

### O3. Falsification runs (`$AB/offline/falsify.py`; calls `uv run --project $CLONE superclaude review estimate`)

1. Build the 12-occasion capture matrix from the catalog (blocking captures of the primary R1 sources; C7 format, `occasions` = the 12 run names) and the 15-occasion matrix (adding arm 1). Print the per-cluster capture counts (the heterogeneity profile) and pairwise Jaccard of the occasions' cluster sets (the correlation profile).
2. F1 with `S_ref` and with `S_conf`; a table of `MAE_obs`, `MAE_est`, `COVER` per k and estimator; the full-data estimates (12 and 15 occasions).
3. F2 (Spearman rho, per-run table).
4. Sensitivity: F1 when the adjudication overrides are ignored (mechanical clusters only); report whether the verdict changes.
5. Write `$AB/offline/falsification.md` with the F1 verdict (FALSIFIED / WEAK / SUPPORTED) quoted from section 2.

## 5. Phase S: shadow analysis of PN1's live data (`$AB/shadow.py`, zero workers)

Runs when at least 5 runs under `$SP/p13/ab1/runs/b1-r*/` have both audits ingested (`state.json` `done` contains `AUD` and `AUD2`). Read each run's `ws/.dev/orca-command-refactor/review/ledger.json` (C6) directly; build the round-1 capture matrix (C7: occasions = round-1 reviewer ids; a row is captured by the reviewers among its round-1 members; blocking only); estimate; map round-1 rows to catalog clusters (anchor span within 3 lines of `orig_span` and theme or refs agree; others are new clusters); compute observed residual from PN1's audits (C9.3 parsing, mapped to clusters) and the F3 verdict. Also report the haiku-only versus sonnet-plus-haiku occasion overlap (correlated blindness). Write `$AB/shadow.md`. Never write into `$SP/p13/ab1`.

## 6. Part C: live arm `c3` harness (build and test it; launch only if the gate in section 2 passes)

```bash
mkdir -p $AB/runs $AB/tests && cp $SP/p11/harness.py $SP/p11/advance.py $AB/
```

Keep byte-for-byte from p11: `S1`, `D`, `SPEC`, `FLAGS`, `AUD_OUT`, `WRAP`, `CMDPART`, `section()`, `git_show()`, the arm-3 `new_brief()` strings, the AUD brief. Constants: `AB = SP/"p13"/"ab3"`, `REPO = str(SP/"p13"/"clones/pn3")`, C0 shas, `DESIGN = "c3"`, `arm_of()` returns 3.

1. **Rules file for c3 sandboxes (experiment-only):** the base rules file with C4.3 Insertions A-D applied by the harness (`apply_c43(text)`; assert each anchor line exists exactly once). Never commit this to the product.
2. **Panel** (same as PN1, C1-C3, `anthropic-only`): `t1b-1` sonnet, `t2-1`, `t3-1`, `t3-2` haiku (`stand_in` true). Implement C3 resolution in `$AB/panel_lite.py` from the contract, or call `uv run --project $SP/p13/clones/pn1 superclaude review panel resolve ...` if that clone exists and its tests pass; record which.
3. **Ledger:** `$AB/ledger_lite.py` implements C5 and C6 from the contract (findings parse, fingerprint, same-defect, clusters, statuses, verdict). If the PN1 clone exists, also run its `superclaude review merge` on the same inputs in a test and report any difference (do not depend on it).
4. **Steps:** `P1.<rid>` (4 whole-document first reviews, arm-3 R1 prompt, each in its own sandbox, output `review/round1.md`) -> `M1` (merge + estimate on round 1) -> if blocking rows are open: `V1` (sonnet, arm-3 revise prompt with ledger ids) -> `R2` (one sonnet scoped re-review, arm-3 R2 prompt, prior = merged report) -> `M2` -> ... When the ledger verdict is PASS: `stop` from the latest whole-document panel round; `stop == true` -> PASS, audits; `stop == false` and reviews used < 3 -> a new whole-document panel round `P<n>.<rid>` on the current spec (first-review prompt, `review: 1 of 3` header kept as the prompt says; the harness counts it as review n) -> merge (new clusters open) -> estimate on that round; at review 3 with open blocking rows or `stop == false` -> ESCALATE, audits. `AUD`, `AUD2` per C9.2.
5. Telemetry: one C8 `reviewer_run` record per panel reviewer, written by `$AB/telemetry_lite.py` (C8 keys, `stand_in` true for the haiku reviewers, `context.experiment` `pn3`) into `$AB/telemetry/records/...`; validate every record against the C8 key list in a test.
6. Tokens per C9.1 (dedupe by message id); done detection, launch ledger, `LAUNCH <alias> <path>`, at most `6 - running`, `--dry-run`, relaunch once then `lost`; `harness.py basetokens`, `status`, `analyze`.

Harness tests (`$AB/tests/test_ab3.py`): prompt identity of P1 reviewer prompts with `a3-r1/PROMPT-R1.md` after path substitution (the rules file differs, the prompt does not), V1, R2, AUD, AUD2; `basetokens` per-run arm-3 loop totals within 1% (a3-r1 70,694; a3-r2 109,207; a3-r3 95,213; a3-r4 81,415; a3-r5 94,998; a3-r6 151,017; skip without transcripts); `apply_c43` result contains Insertion D once; a fake run where `stop` is false after R2 PASS triggers `P3.*`; a fake ESCALATE; concurrency (6 fresh runs print 6 LAUNCH lines); telemetry records valid.

Live cost if launched: per run about 4 + 1 + 1 + 4 + 1 + 1 + 2 = 14 workers (84 for 6 runs, at most 6 at once, about 14 waves); tokens (C9.1 method; haiku volume unknown) about 200,000 per panel round x 2 + revises and re-reviews ~90,000 + AUD and AUD2 ~138,000: about 0.63M per run, 3.8M in total.

## 7. Analysis (`harness.py analyze` -> `$AB/RESULTS.md`)

Always: the O1 catalog summary, F1/F2 tables and verdict, sensitivity, the heterogeneity and correlation profiles. If Phase S ran: F3 table. If c3 ran: the section 2 decision table, per-run table (rounds, panel rounds, stop decisions with `unseen_upper95`, decision, growth, tokens, AUD/AUD2 blocking ids and themes), and the residual decomposition (residual clusters never captured by any panel round versus captured then surviving). The decision line is the rule table's output only.

## 8. Self-check before you start

- [ ] The 12 primary R1 reports, 3 arm-1 R1 reports, 15 first audits and 6 second audits all exist (`ls`); a2-r3 R1 verdict is PASS.
- [ ] `sha256sum` of the overlay spec equals `SPEC_SHA`; the finals' sizes match `state.json` `spec_after.bytes` of their last revise step.
- [ ] You understand that only whole-document reviews of one version are capture occasions (C7).
- [ ] `$CAT/catalog.json` does not exist yet, or you are deliberately producing `catalog-v2.json`.

## 9. Report formats

**READY report:**

```text
PN3 READY | branch 346Claude-pn3-capture-recapture | PRODUCT_REF <sha> | pushed yes/no
Tests: tests/review <n> passed; lint, sync-dev, verify-sync ok; formulas verified against: <source | not verified>
Catalog: findings <n> (anchored quote/cited/none <a>/<b>/<c>), revision-introduced <n>, clusters <mech> -> <adj>, overrides <n>, confirmed <n>; S_ref <n>, S_conf <n>; recheck sample agreement <x>/<y>
Capture profile: Q1..Q12 = ...; mean pairwise Jaccard <x>
F1 (k=4): MAE_obs <x>; Chao2 MAE <x> COVER <y>; Jack1 MAE <x> COVER <y> -> FALSIFIED|WEAK|SUPPORTED (S_conf: ...)
Full-data: Chao2 N <x> [<lo>, <hi>]; Jack1 N <x> [<lo>, <hi>]
F2: Spearman rho <x> (n=12)
Shadow (F3): not yet run | CALIBRATED/NOT (<m>/<n>)
Gate for c3: PASS/FAIL
Harness: $AB, tests <n> passed; launch: cd $AB && uv run --no-project python advance.py --dry-run
Contract deviations: <none | list>
```

**RESULTS.md**: `DECISION: <offline verdict> ; live: ADOPT | DROP | INCONCLUSIVE | NOT RUN (gate)`, then the tables of section 7, validity notes (same-model correlation, truth built from the same kind of review, dedupe overrides and their sensitivity), token method (C9.1).
