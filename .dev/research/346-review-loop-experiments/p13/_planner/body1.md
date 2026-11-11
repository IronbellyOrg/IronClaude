# PLAN PN1 (S1): independent reviewer panel + deterministic merge + typed finding ledger, with panel template and telemetry

You build, test offline and stage for a live A/B test ONE design from research report 2, section 3.1 (table rows 1 and 2): the first review of the `/sc:spec-panel` review loop is run by a panel of independent reviewers (the owner's production composition 2x Tier 3 + 1x Tier 2 + 1x Tier 1b, mapped to this environment's models; re-reviews keep one reviewer, the Tier 1b anchor, per the coordinator's cost instruction), a Python script merges their findings by fingerprint into a ledger whose statuses only the script changes (open, resolved_check, resolved, regressed, deferred), and the script computes the verdict. You also build the panel template, tier map and telemetry layer (shared infrastructure; PN3 reuses their formats). The appendix holds the SHARED CONTRACT (C0-C9): it is binding and wins over this text.

## 0. Read this first

Read the whole file before running anything. Do not open the other plans.

Hard rules (from `/home/user/IronClaude/CLAUDE.md`, binding):
- Python only through UV: `uv run ...`, `uv pip ...`; scratch scripts outside the repo run as `uv run --no-project python <file>`, their tests as `uv run --no-project --with pytest pytest <dir>`. Never `pip`, `python -m`, or bare `python x.py`.
- Never stage or commit anything under `.claude/`. If `git add` ever needs `-f`, stop: that is the violation. Edit only `src/superclaude/`, `tests/`; then `make sync-dev` and `make verify-sync`.
- `src/superclaude/commands/spec-panel.md` stays at or below 500 lines (490 now); this plan does not edit it.
- Installed primitives (the rules file `src/superclaude/rules/prompts/document_review_loop_prompts.md` included) never name a `src/superclaude/...` path; they reach package code only through the `superclaude` CLI.
- Work only in your own full clone `$CLONE` (below), never in `/home/user/IronClaude` (shared; do not switch its branch). Never edit `$SP/p11/` or `$SP/p12/`.
- Commit and push your branch to `origin` = `https://github.com/IronbellyOrg/IronClaude`. No pull request. Never add a remote for, fetch from, push to or call gh against `SuperClaude-Org/SuperClaude_Framework`.
- You cannot spawn sub-workers. Implement, test offline, run the offline phase yourself, build the harness, push, then STOP with the READY report (section 9). If you do have an Agent tool, you may run the live phase yourself with at most 6 concurrent workers.

```bash
export SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
export CLONE=$SP/p13/clones/pn1 AB=$SP/p13/ab1 BR=346Claude-pn1-panel-merge-ledger
```

## 1. Background

**The loop under test (baseline = Stage 2 arm 3).** `/sc:spec-panel --mode critique` reviews a spec; a coordinator runs at most 3 reviews and 2 fix cycles: R1 (whole-document first review), V1 (revise only the blocking ids, in place), R2 (scoped re-review: changed lines plus prior blockers), V2, R3; a review PASS ends the loop; FAIL at review 3 escalates. Briefs are short pointers to prompts in the rules file. Stage 2 ran each step as a Sonnet subagent inside a sandbox `runs/<run>/` (`ws/` = overlay copy, `home/.claude/rules/prompts/<rules file>`, `command.md`, `state.json`) with a fixed wrapper `WRAP`; read `$SP/p11/harness.py`, `$SP/p11/advance.py` and the prompts `$SP/p11/runs/a3-r1/PROMPT-{R1,V1,R2,AUD}.md` and `$SP/p11/runs/a3-r6/PROMPT-R3.md` now.

**Baseline numbers (arm 3, n=6).** 6/6 loops PASS (5 at R2, 1 at R3), mean 2.17 reviews, mean growth +1.41%, `B_TOK` ~169,000 output tokens per replicate (loop ~100,000 + one audit ~69,000, each message id counted once, C9.1), `B_BLK` = 1.50 blocking findings per audit over 12 audits (first audits 2,2,2,2,0,1; second audits 2,1,2,1,1,2). A single audit is noisy (the one first-audit PASS, a3-r5, did not repeat), hence two audits per final spec.

**What the baseline residual is made of (theme-level, C9.3 tags, UNVERIFIED keyword proxy).** Of the 9 first-audit blocking findings, about 4 are themes the run's own R1 had already found and the loop then passed (T1 in a3-r1, r2, r3; T2 in a3-r6: "found, then survived the fix") and about 5 were never found by that run's R1 (T2 in a3-r1, r3, r4; T3 in a3-r2; one other in a3-r4: "never found"). A bigger panel can only remove the second kind; the ledger's regression rule can only help with the first kind if a re-review panel re-finds it. Pre-registered prediction: `BLK_T` between 0.7 and 1.2. You will recompute this decomposition (section 7).

**Model mapping in this environment (C1-C3, owner decisions of 2026-11-10).** Tiers are aliases for ordered model lists (first model = default, the rest = fallbacks). Tier 1b's first model is Claude Sonnet 5.5, so `t1b-1` = `claude-sonnet-5-5` (`sonnet`), the Stage 2 reviewer model: the like-for-like anchor to the baseline. Tier 2 and Tier 3 hold no Anthropic model, so the `anthropic-only` environment substitutes Claude Haiku 5.5 for all three: `t2-1`, `t3-1`, `t3-2` = `claude-haiku-5-5` (`haiku`), recorded `stand_in: true`. The three haiku reviewers are the same model: their independence comes only from separate fresh contexts, so correlated blindness is expected and is measured, not assumed away (section 7). Re-reviews (R2, R3) use one reviewer, the anchor (`apply_to: ["first"]`). Revisers and audits stay `sonnet` as in Stage 2. The blind adjudicator (ADJ, section 5) is `fable` (outside the panel; if a `fable` launch is refused, use `opus` and record it).

## 2. Goal, arm, pre-registered criteria

**Goal.** Decide whether the panel + merge + ledger loop should replace the single-reviewer loop. **Arm** `b1` (`b1-r1..b1-r6`, n=6) versus the reused baseline (`a3-r1..a3-r6`). Everything except the factor under test matches Stage 2 arm 3: same spec and overlay, same `WRAP`, `CMDPART` and pointer briefs (byte-identical apart from sandbox paths), same spec-panel command, sonnet revisers, same REVISE contract, cap 3, the frozen audit twice per final spec (C9.2).

Definitions: `BLK_T` = C9.2 metric over the 12 test audits; `PASS_T` = runs whose ledger decision is PASS within 3 reviews; `GROWTH_T` = mean (final bytes / 57,763 - 1); `TOK_T` = mean output tokens per replicate of loop steps plus AUD (not AUD2, not ADJ), C9.1 method; `R_TOK = TOK_T / B_TOK`; `BLOCK_OK` = share of reviewer reports whose findings block parsed (`ok` true).

| Rule | Condition (pre-registered) | With baseline numbers |
|---|---|---|
| DROP-1 no gain | `BLK_T > 0.8 * B_BLK` | > 1.20 |
| DROP-2 cost | `R_TOK > 3.3` (arm-1 cost level, the report's own "below the old baseline" ceiling) | > ~560,000 |
| COST-HOLD | `2.0 < R_TOK <= 3.3`: the report's pre-registered "token cost <= 2x" fails; the result can be at best INCONCLUSIVE | 338,000 to 560,000 |
| DROP-3 harm | `PASS_T < 4/6` or `GROWTH_T > 3 * 1.41%` | < 4/6; > 4.23% |
| ADOPT | no DROP, no COST-HOLD, `BLK_T <= 0.5 * B_BLK`, `PASS_T >= 5/6`, `GROWTH_T <= 2.82%`, `BLOCK_OK >= 0.90` | <= 0.75; `R_TOK <= 2.0` |
| INCONCLUSIVE | anything else; or fewer than 5 completed runs; or the arm means of AUD and AUD2 differ by more than 0.75 | |

Also report (not a decision rule): the report's literal criterion "median residual 0 with lower quartile 0" (per-run residual = mean of its two audits). Expected cost (C9.1 method): R1 panel ~50,600 (sonnet) + 3 x haiku (unknown; assume at most ~50,000 each) + V1 ~14,300 + R2 ~30,000 + occasional R3/V2 ~10,000 averaged = loop ~250,000, plus AUD ~69,000: `TOK_T` ~320,000, `R_TOK` ~1.9 (upper estimate; haiku volumes are the main unknown).

## 3. Part A: product change (tests first)

### A1. Clone and branch

```bash
mkdir -p $SP/p13/clones $AB
git clone /home/user/IronClaude $CLONE && cd $CLONE
git remote set-url origin https://github.com/IronbellyOrg/IronClaude
git fetch origin 346Claude-p8a-first-review-grading || echo "FETCH FAILED: continuing on the local copy of the branch"
git checkout -b $BR origin/346Claude-p8a-first-review-grading
test "$(git rev-parse HEAD)" = 69ac8b3335564fb5551980e984c5d9b763039cc1 && echo BASE-OK \
  || { echo "origin moved past 69ac8b33: staying on 69ac8b33"; git checkout -B $BR 69ac8b3335564fb5551980e984c5d9b763039cc1; }
git remote -v                     # exactly one remote: origin -> IronbellyOrg/IronClaude
uv venv && make install
uv run pytest -q tests/skills/test_review_brief_placement.py tests/skills/test_spec_panel_review_loop.py \
  tests/skills/test_review_loop_extension.py tests/skills/test_review_severity_mapping.py \
  tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_rule.py tests/cli/test_cli_registration.py
```

Record the pass count of the last command as `PINNED_BEFORE`. Read those test files: they pin the rules-file labels (`- First-review brief: "` etc.), the role table and Step 1 tokens, forbid `src/superclaude` in the rules file, and scan for finding quotas ("find at least N ..."); your inserted text must keep them green unchanged.

### A2. Tests first (write them, watch them fail, then implement)

Create these files under `tests/review/` (no `__init__.py`; C0):

1. `test_review_panel.py`: both packaged defaults validate, and the panel validates against the tier file; each schema error is caught (unknown key, a tier not defined in `aliases`, `count` 0 or 5, two `fixed` slots, duplicate `slot_id`, total reviewers 9, a stand-in id not in `available`, a duplicate model in an alias list, a bad `apply_to`); every unit test C3 requires (stand-in Tier 3 with `stand_in` true; Tier 1b fallback to depth 1 and depth 2; seeded `random` reproducible and inside the candidates; `distinct_across_slots`; reordering an alias list changes the `fixed` result); `anthropic-only` resolution equals C3's last paragraph for three run ids; `--kind re-review` resolves only `t1b-1`; output byte-identical for equal inputs; `gateway` selected when `T3Model01` is set (monkeypatch); precedence `--template` > `$SUPERCLAUDE_REVIEW_PANEL` > project file > user file (monkeypatch `HOME`) > default; adding a model family is a data edit only (a tmp tier file adds `acme-1` to `tier3` and an environment that has it; it resolves with no code change).
2. `test_review_findings.py`: C4.1 parse (good block; missing heading; missing block; a bad JSON line keeps the good lines and sets `ok` false; `MINOR` + `blocking` is an error; last of two blocks wins; prior lines); C4.2 fix map parse and its table fallback; C5 `locate` across a line wrap, `section_of`, `refs_norm`, fingerprint stable when only `claim` wording changes, `same_defect` within and beyond 3 lines, deterministic clusters.
3. `test_review_ledger.py` (fixtures: copy `$SP/p5/docs/clean.md` and `$SP/p5/docs/seeded.md` into `tests/review/fixtures/`; write small findings blocks by hand): every C6 transition and event; verdict/decision at rounds 1-3; a re-found resolved row becomes `regressed` and the verdict FAIL; `named_not_touched`; `cleared`; `defer`; capture export (C7); atomic write (no temp file left behind).
4. `test_review_telemetry.py`: a valid record passes and each missing key fails; two appends leave the first line byte-identical; no 40-character substring of the reviewed document appears in any record; `task_variables` on `fixtures/clean.md` (pin the numbers you compute by hand and check them by reading the file); loader is idempotent; `model_scores` arithmetic on 3 synthetic records; superseded records leave the view.
5. `test_review_cli.py` (Click `CliRunner` on `superclaude.cli.main.main`): `review --help` lists `panel`, `merge`, `ledger`, `telemetry`; `review panel resolve --env anthropic-only --run-id x` prints C3 JSON; `review merge` then `review ledger revise` then `review ledger verdict` round trip on tmp files; exit codes.
6. `test_review_rules_text.py`: the rules file contains C4.3 Insertions A-D and section E (A3) exactly once each, in the stated places, D and E before `## Never`; it still contains every token `test_review_brief_placement.py` checks; no `src/superclaude`.

### A3. Implementation (files and interfaces)

Create `src/superclaude/cli/review/` with the C0.1 `__init__.py` (exact bytes), `data/review-panel.default.json` and `data/review-tiers.default.json` (exact C1/C2 content; load with `importlib.resources.files("superclaude.cli.review") / "data" / ...`), and:

- `panel.py`: `load_panel(path=None)`, `load_tiers(path=None)`, `validate_panel`, `validate_tiers`, `select_env(env=None, environ=os.environ)`, `resolve_slot(...)` (pure) and `resolve(...)` exactly as C1-C3; `NoModelAvailable`. No third-party imports (stdlib + click only).
- `panel_cmd.py`: group `panel` with `resolve [--template P] [--tiers P] [--env E] --run-id ID [--kind first|re-review] [--seed N] [--sequence N]` (prints C3 JSON) and `validate PATH [--kind panel|tiers]` (prints errors; exit 0 valid, 1 invalid).
- `findings.py`: C4/C5 functions (`parse_block`, `parse_fixmap`, `flat`, `locate`, `section_of`, `refs_norm`, `fingerprint`, `same_defect`, `cluster`, `map_span`, `hunks_touch`).
- `ledger.py`: C6 (`new_ledger`, `merge_round`, `apply_revision`, `defer`, `verdict`, `capture`, `render_merged_report`, atomic `save`).
- `merge_cmd.py`: command `merge --ledger L --doc CANDIDATE --round N --report REVIEWER_ID=PATH [--report ...] [--resolution PANEL.json] --out MERGED.md`. Round 1 creates the ledger. Prints one JSON object `{"verdict", "decision", "brief_ids", "new", "refound", "regressed", "cleared", "clusters", "block_ok": {reviewer: bool}}`; exit 0.
- `ledger_cmd.py`: group `ledger` with `revise --ledger L --old OLD --new NEW --fixmap REVISE.md`, `defer --ledger L --lid L3 --reason TEXT`, `verdict --ledger L` (exit 0 PASS, 10 REVISE, 11 ESCALATE), `capture --ledger L --round N`.
- `telemetry.py` / `telemetry_cmd.py`: group `telemetry` with `taskvars DOC [--specialization S] [--kind first|re-review|audit]`, `append --dir D --record FILE.json` (validates C8, appends to the right file), `load --dir D --db OUT.sqlite`.

**Merged report** (`render_merged_report`, written to `--out`): line 1 `review: N of 3`; `# Merged review N (coordinator script; panel of K reviewers)`; `candidate: <path> sha256 <sha>`; `reviewers:` one line per reviewer (id, report path, block ok); `## Ledger` table `| lid | status | blocking | confidence | severity | refs | reviewers |`; `## Blocking findings` with, per brief id, `### L<k>` then for each member `#### L<k>.<reviewer_id> (<fid>)`, its `claim`, `anchor` and `anchor2` quoted; `## Other findings` (non-blocking rows, one line each); `## Reviser brief` with `Blocking finding ids: L1, L3.` (or `Blocking finding ids: none.`) and the line `Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.`; last line `verdict: PASS` or `verdict: FAIL` (`ESCALATE` decisions still print `verdict: FAIL`).

**Rules file** `src/superclaude/rules/prompts/document_review_loop_prompts.md`: insert C4.3 Insertions A, B, C, D exactly, then insert section E immediately after D's `### Fix map` paragraph and before `## Never` (one blank line around it):

```text
### Review panel

Run each review with the reviewers that `superclaude review panel resolve --run-id <loop id> --kind <first or re-review>` prints (a panel for a first review, one reviewer for a re-review by default): each in a fresh context with the same brief, none seeing another's report or transcript. Merge the reports with `superclaude review merge`, also for a single reviewer; its merged report and the ledger it keeps give the verdict and the Reviser brief ids, and only that script changes a finding's status. If the `superclaude` command is not installed, run one reviewer and say so in the loop summary.
```

Nothing else changes: not `spec-panel.md`, not `HOW-WE-WORK.md` (either copy), not the installer (the rules file is already shipped).

### A4. Verify, commit, push

```bash
cd $CLONE
uv run pytest -q tests/review                                   # all new tests pass
uv run pytest -q tests/skills tests/cli tests/unit              # compare with PINNED_BEFORE; no new failure
wc -l src/superclaude/commands/spec-panel.md                    # <= 500 (unchanged)
grep -rn 'src/superclaude' src/superclaude/rules/prompts/document_review_loop_prompts.md   # no output
uv run superclaude review --help && uv run superclaude review panel resolve --env anthropic-only --run-id smoke
make lint && make sync-dev && make verify-sync
git status --short                                              # only src/superclaude/cli/review/**, cli/main.py, rules file, tests/review/**
git add src/superclaude/cli/review src/superclaude/cli/main.py src/superclaude/rules/prompts/document_review_loop_prompts.md tests/review
git commit -F - <<'EOF'
experiment(review): reviewer panel template, deterministic merge, typed finding ledger and telemetry (PN1, refs #346)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Y28dBfZHbPhB1U1EM1XTUj
EOF
git push -u origin $BR || echo "PUSH FAILED: report it"
git rev-parse HEAD                                              # PRODUCT_REF
```

A failure outside your files: check it on the base (`git stash -u; uv run pytest -q <test>; git stash pop`); report pre-existing failures, never "fix" unrelated tests.

## 4. Part B: offline phase (you run it; no workers; numbers go in the READY report)

Work in `$AB/offline/`. Scripts run with `uv run --no-project python`, and call product code through `uv run --project $CLONE superclaude review ...`.

- **O1. Replay fixtures.** For each baseline run `a3-r1..a3-r6`, write findings-v1 lines by hand for every blocking finding of `round1.md`, `round2.md` and (a3-r6) `round3.md` in `$SP/p11/runs/<run>/ws/.dev/orca-command-refactor/review/`, into `$AB/fixtures/<run>/round<n>.findings` (JSON lines only). Anchor = the shortest exact span (12-200 chars) of the spec version that report reviewed that the finding quotes or cites (R1: the original; R2: the spec after V1 = `specs/history/spec-v2.md` if it exists, else the run's final spec; R3: the final spec); verify every anchor with `locate` (at least one hit) and print the check. Re-review fixtures get prior lines with the report's stated status. Fix maps: from `revise<n>.md`, mapping report ids to the ledger ids the replay printed. Record your authoring decisions in `$AB/fixtures/NOTES.md`.
- **O2. Replay with k=1 (report migration step 1).** `replay.py` drives `merge`/`ledger revise` through each run with the real spec versions (R1 on the original, revise original -> spec after V1, etc.). Compare the ledger decisions with the baseline verdict sequence (r1-r5: FAIL, PASS; r6: FAIL, FAIL, PASS). Also run k=2 with the same report twice: decisions must be identical to k=1 and every row `confidence: overlap`.
- **O3. Panel merge on recorded data.** Merge the R1 fixtures of a3-r1, a3-r3, a3-r6 as a 3-reviewer round: every input finding appears exactly once as a member; print clusters with themes.
- **O4. Same-model union baseline.** From the C9.3 R1 tags of the 12 arm-2/3 runs, compute for k = 1..4 over all C(12,k) subsets the mean number of distinct themes among {T1,T2,T3} found and the share of subsets finding each theme. If `$SP/p13/catalog/catalog.json` exists, repeat at cluster level (confirmed clusters). This is the "same model, bigger panel" counterfactual used in section 7.

**Offline gate (recommend the live phase only if all hold):** all product tests green; replay runs without error; O2 decisions match the baseline in at least 5 of 6 runs, or every mismatch is explained in the READY report with quotes (for example a fail-closed `named_not_touched`); k=2 equals k=1; O3 drops no member.

## 5. Part C: harness `$AB` (copy of the Stage 2 tooling, modified)

```bash
mkdir -p $AB/runs $AB/tests && cp $SP/p11/harness.py $SP/p11/advance.py $AB/
```

Edit only the copies. Keep byte-for-byte from p11: `S1`, `D`, `SPEC`, `FLAGS`, `AUD_OUT`, `WRAP`, `CMDPART`, `section()`, `git_show()`, the arm-3 branches of `new_brief()` (generalized only by passing `out`, `prior`, `base`, `rep` as arguments; the strings may not change) and the AUD brief text.

1. Constants: `P13 = SP/"p13"; AB = P13/"ab1"; RUNS = AB/"runs"; REPO = str(P13/"clones/pn1")`; `BASE_REF`, `SPEC_SHA`, `AUD_CMD_SHA`, `AUD_RULES_SHA` (C0); `PRODUCT_REF = "<sha from A4>"`; `TASKS_GLOB` (C0); `MAX_CONCURRENT = 6`; `DESIGN = "b1"`; `CLI = ["uv", "run", "--project", REPO, "superclaude", "review"]`; `TELEMETRY_DIR = P13/"clones/pn1/.dev/benchmarks/review-telemetry"`. `arm_of()` returns 3 for every run. `P11` stays read-only for `rules.md`, baseline runs and audits.
2. `build()`: runs `b1-r1..b1-r6`, each like p11 arm 3 except `command.md` = `git_show(PRODUCT_REF, "src/superclaude/commands/spec-panel.md")` (assert sha = `AUD_CMD_SHA`: spec-panel is unchanged) and the rules file from `PRODUCT_REF`. Assert the spec sha. Resolve the reviewers once per run and kind: `CLI + ["panel", "resolve", "--env", "anthropic-only", "--run-id", run, "--kind", "first"]` saved as `runs/<run>/panel.json`, and the same with `--kind re-review` as `runs/<run>/panel-rr.json` (one reviewer, `t1b-1`); keep both in `state["panel"]`.
3. Steps: `R1.<rid>` (4, from `panel.json` in resolution order), `M1` (script), `ADJ` (after M1, parallel to V1), `V1`, `L1` (script), `R2.t1b-1`, `M2`, `V2`, `L2`, `R3.t1b-1`, `M3`, `AUD`, `AUD2`. Re-reviews are single-reviewer (from `panel-rr.json`) but still go through `merge` and the ledger, so the regression rule applies.
4. **Reviewer sandboxes** `runs/<run>/r<n>-<rid>/`: an arm-3 sandbox (overlay copy, `home/.claude/rules/prompts/` with the product rules file, `command.md`) whose `ws/` holds the current spec, and for n >= 2 also `specs/history/spec-v<n-1>.md` and the merged prior `review/round<n-1>.md`. The prompt is the arm-3 R1/R2/R3 prompt with `sb` = that sandbox and the baseline output path (`.dev/orca-command-refactor/review/round<n>.md`), so it is byte-identical to the baseline prompt after replacing the sandbox path. Launch with the reviewer's `launch` alias (C3).
5. **Ingest of a reviewer**: copy its report to the main `ws/.dev/orca-command-refactor/review/round<n>-<rid>.md`; record verdict (p11 regex), `parse_block` result, output tokens (C9.1, expected model = the reviewer's model), observed model (`message.model` of its transcript), wall time (first to last transcript timestamp); append a C8 `reviewer_run` record with `CLI + ["telemetry", "append", ...]` (`task` from `telemetry taskvars` on the reviewed spec, `specialization` `software-spec`, `context` `{"experiment": "pn1", "arm": "b1", "replicate": k}`). Verdict `INCOMPLETE`/`NONE` or a missing report: print `MANUAL`, relaunch once (`harness.py unlaunch RUN STEP`), then mark the reviewer `lost`; the merge proceeds without a lost reviewer, and a run with 2 or more lost reviewers in one round is `lost`.
6. **M<n>** (when all reviewers of round n are ingested or lost): `CLI + ["merge", "--ledger", <ws review>/ledger.json, "--doc", <ws spec>, "--round", n, "--report", "<rid>=<path>", ..., "--resolution", panel.json, "--out", <ws review>/round<n>.md]`; store its JSON in `state["log"]["M<n>"]`. Decision PASS -> AUD and AUD2; REVISE -> V<n> with `IDS = ", ".join(brief_ids)` (snapshot `spec-v<n>.md` first, as p11); ESCALATE -> AUD and AUD2.
7. **V<n>**: the unchanged arm-3 revise prompt (`rep` = merged `round<n>.md`), model `sonnet`. **L<n>**: `CLI + ["ledger", "revise", "--ledger", ..., "--old", "specs/history/spec-v<n>.md", "--new", <spec>, "--fixmap", "review/revise<n>.md"]`; then R<n+1> reviewers.
8. **ADJ** (blind adjudication of round-1 rows, model `fable`): sandbox `runs/<run>/adj/` = overlay README, inventory and the original spec, plus `ws/.dev/orca-command-refactor/review/adj-input.md`: one `### X<k>` per round-1 ledger row, in an order shuffled with `random.Random(run)`, showing only `anchor`, `anchor2`, `refs` and the first member's `claim` (no reviewer, model, severity or count). Prompt = `WRAP` (no CMDPART) with this brief: `Read .dev/orca-command-refactor/README.md and the spec .dev/orca-command-refactor/specs/orca-worker-contract-spec.md. For each finding X<k> in .dev/orca-command-refactor/review/adj-input.md decide whether it is a real defect that blocks implementation: write the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." and confirm it only if that sentence holds with no further assumption. Write .dev/orca-command-refactor/review/adj.md ending with a fenced block with info string adj-v1 holding one JSON line per finding: {"x": "X1", "verdict": "confirmed" or "rejected" or "unsure", "reason": "<one sentence>"}. Do not edit anything else.` Map `X<k>` back to `L<k>` from the shuffle you saved.
9. Audits: `prep_audit(run, k)` per C9.2 (`aud`, `aud2`), launched together.
10. Tokens and done detection: replace p11's line-summing with C9.1 (dedupe by message id). A step is done when its output exists and its transcript has a `SubagentHandback` or final text containing `DONE`, or no transcript is found and the output has not changed for 180 s; no output after 60 min prints `WARN stale`. `advance.py` keeps a launch ledger (`state["launched"]`), prints `LAUNCH <alias> <path>` lines (C9.5) for at most `6 - running` prompts in run order then step order, and accepts `--dry-run`.
11. `harness.py basetokens` (C9.1; prints per-run loop and audit totals for a3-r1..r6 and `B_TOK`), `harness.py status`, `harness.py outcomes` (section 7), `harness.py analyze` (writes `RESULTS.md`).

## 6. Part D: harness tests (`$AB/tests/test_ab1.py`; `uv run --no-project --with pytest pytest -q $AB/tests`)

Point `harness.RUNS` at `tmp_path`; fake finished workers by writing outputs (real Stage 2 reports, with a findings block appended from your O1 fixtures) and back-dating mtimes. Required: (1) prompt identity for R1/R2/R3 reviewer prompts, V1, AUD, AUD2 against the a3-r1/a3-r6 files after path substitution; (2) `basetokens` reproduces per-run arm-3 loop totals within 1% of: a3-r1 70,694; a3-r2 109,207; a3-r3 95,213; a3-r4 81,415; a3-r5 94,998; a3-r6 151,017 (skip if transcripts are unreadable); (3) build: spec sha, `command.md` sha = `AUD_CMD_SHA`, rules file contains C4.3 Insertion D, `panel.json` equals C3's resolution; (4) a full fake run: four R1 fakes -> M1 -> V1 -> L1 -> one R2 fake with PASS -> AUD+AUD2 printed together; (5) a regressed fake: R2 re-finds a `resolved_check` row -> decision REVISE; (6) ESCALATE at round 3; (7) a lost reviewer: merge with 3 reports; (8) concurrency: six fresh runs print exactly 6 LAUNCH lines (run 1's four reviewers and two of run 2), `--dry-run` records nothing; (9) telemetry: one record per ingested reviewer, valid per C8, `model.observed` from the transcript; (10) ADJ input holds no reviewer id, model or severity.

## 7. Part E: live phase, measurement, analysis

**Run only if the offline gate passed and the coordinator says go.** Workers per run: 4 (R1) + 1 (ADJ) + 1 (V1) + 1 (R2) + 2 (AUD, AUD2) = 9, plus 2 per extra round (V2, R3); 6 runs = 54 to about 60 workers, at most 6 at once, about 10 waves. Token estimate (C9.1 method, from arm-3 per-step means; haiku volume unknown): loop ~250,000, AUD ~69,000, AUD2 ~69,000, ADJ ~30,000: about 0.42M per run, about 2.5M output tokens in total; `R_TOK` about 1.9 (upper estimate).

Coordinator loop: `cd $AB && uv run --no-project python advance.py` -> launch every `LAUNCH` line -> when workers finish, run `advance.py` again; repeat until `harness.py status` shows every run complete or lost.

**`harness.py outcomes`** (after all runs): truth = `catalog-v1` if `$SP/p13/catalog/catalog.json` exists (map each round-1 row to a cluster when its anchor span is within 3 lines of the cluster's `orig_span` and refs or theme agree; unmatched rows become new clusters `N<k>`), else `theme-v1` (C9.3 tags of the member claims); plus `adjudicated-v1` from ADJ. Append one C8 `outcome` record per round-1 reviewer record for each truth basis, then `CLI + ["telemetry", "load", "--dir", TELEMETRY_DIR, "--db", "$AB/telemetry.sqlite"]`.

**`harness.py analyze`** writes `$AB/RESULTS.md` with: the section 2 decision table filled; per-run table (reviews, decision, final bytes, growth, loop tokens, AUD tokens, AUD/AUD2 blocking ids with C9.3 themes); state-machine events (`named_not_touched`, `regressed`, `cleared`, extra rounds caused by a regression); `BLOCK_OK` per model; and:
- **Separating size, model and resampling (no extra arm), on round-1 data, recall of confirmed defects:** (a) **anchor check**: `t1b-1` (sonnet, k=1) versus the 12 baseline sonnet R1s (arms 2 and 3; same model, same prompt plus the findings-block line): blocking count, themes, recall, tokens; a difference means the panel harness or the findings-block line changed the anchor's behavior (or drift since Stage 2), and is reported before any other comparison. (b) **different model versus resampling**: mean pairwise Jaccard of confirmed-defect sets haiku-haiku (3 pairs per run) versus sonnet-haiku (3 pairs per run), and the recall of `t1b-1 ∪ t2-1` (sonnet + haiku, k=2) versus the mean of the three haiku-haiku pairs and versus O4's mean of 2 random baseline sonnet R1s (sonnet resampled, k=2). If a sonnet+haiku pair beats both same-model pairs, a different model buys coverage over resampling. (c) **marginal value**: the union of all four, and each leave-one-out union of three; marginal value of a reviewer = union(4) - its leave-one-out union; with O4's 4-sonnet union as the same-size same-model counterfactual (size effect = O4(k=4) - O4(k=1); mix effect = union(4) - O4(k=4)). Also per-reviewer unique confirmed finds and adjudicated precision (ADJ). Haiku records are stand-ins: no conclusion is drawn about real Tier 2/Tier 3 models.
- **Residual decomposition.** Each test-audit blocking finding mapped to the truth basis and classified "never found by the run's R1 union" or "found, then survived"; same for the baseline 12 audits; compare.
- **Drift check.** Part of (a): if T1 is missing from more than 2 of the 6 `t1b-1` R1 reports (baseline: present in every arm-3 R1 by C9.3 tags), report possible drift since Stage 2.
- The pre-written conclusion: one of ADOPT / DROP-n / INCONCLUSIVE from the rules, quoted, with the numbers; no other wording decides.

Finally commit the telemetry records (not the SQLite file) on your branch: `cd $CLONE && git add .dev/benchmarks/review-telemetry && git commit` (same trailers) `&& git push`.

## 8. Self-check before you start

- [ ] `$SP/p11/runs/a3-r1..a3-r6` and `$SP/p12/baseline-audit2/a3-r*/ws/.dev/orca-command-refactor/review/audit.md` exist and are readable.
- [ ] `sha256sum` of the overlay spec, `$SP/p11/rules.md` and `git -C /home/user/IronClaude show 69ac8b33:src/superclaude/commands/spec-panel.md` equal `SPEC_SHA`, `AUD_RULES_SHA`, `AUD_CMD_SHA`.
- [ ] `src/superclaude/cli/review/` does not exist on the base (it does not on 69ac8b33); nothing in the repo is called `review ledger` yet (the #346 ledger/diffgate prototypes under `$SP/exp346/.../builds/` are reading material only).
- [ ] `uv --version` works; `make install` succeeded in `$CLONE`.
- [ ] You know the C9.1 token rule (dedupe by message id) and the C9.2 audit (twice, frozen).

## 9. Report formats

**READY report** (your final message when you stop before or after the live phase):

```text
PN1 READY | branch 346Claude-pn1-panel-merge-ledger | PRODUCT_REF <sha> | pushed yes/no
Tests: tests/review <n> passed; pinned before/after <a>/<b>; lint, sync-dev, verify-sync ok
Offline: O2 replay decisions match <m>/6 (mismatches: <run: reason>); k=2==k=1 yes/no; O3 members <x>/<x>
O4 same-model union (themes T1,T2,T3 found, mean over subsets): k=1 <..> k=2 <..> k=3 <..> k=4 <..>
B_TOK recomputed: <n> (per run: ...)
Offline gate: PASS/FAIL (<why>)
Harness: $AB, tests <n> passed; first launch: cd $AB && uv run --no-project python advance.py --dry-run
Contract deviations: <none | list>
Open issues: <list>
```

**RESULTS.md** (`$AB/RESULTS.md`): title; decision line `DECISION: ADOPT | DROP-n | INCONCLUSIVE` with the rule text; section 2 table with baseline and test values; per-run table; size-versus-mix table; residual decomposition; telemetry summary (`model_scores` view rows); validity notes (lost reviewers, relaunches, manual steps, drift check, audit agreement); token table (C9.1 method stated).
