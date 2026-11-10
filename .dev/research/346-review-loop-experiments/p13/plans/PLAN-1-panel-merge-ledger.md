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

---

# Appendix: SHARED CONTRACT (verbatim copy of `$SP/p13/plans/SHARED-CONTRACT.md`; binding)

# SHARED CONTRACT v1 (frozen 2026-11-10; plans PN1, PN2, PN3)

This contract is embedded verbatim in every plan. If your plan and this contract disagree, this contract wins. Do not change anything here; if something here cannot be built as written, build the nearest thing, and list the deviation in your READY report under "Contract deviations".

## C0. Names, paths, refs

```bash
export SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
export TASKS_GLOB='/tmp/claude-0/-home-user-IronClaude/*/tasks/*.output'   # worker transcripts (JSONL)
```

| Item | Value |
|---|---|
| Base branch / commit (= Stage 2 arm 3 design, PR #484) | `346Claude-p8a-first-review-grading` at `69ac8b3335564fb5551980e984c5d9b763039cc1` (`BASE_REF`) |
| Plan PN1 (S1 panel + merge + ledger + telemetry) | branch `346Claude-pn1-panel-merge-ledger`, clone `$SP/p13/clones/pn1`, experiment dir `$SP/p13/ab1` |
| Plan PN2 (S2 mechanical lint) | branch `346Claude-pn2-mechanical-lint`, clone `$SP/p13/clones/pn2`, experiment dir `$SP/p13/ab2` |
| Plan PN3 (S3 capture-recapture) | branch `346Claude-pn3-capture-recapture`, clone `$SP/p13/clones/pn3`, experiment dir `$SP/p13/ab3` |
| Spec under review (original) | `$SP/exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 57,763 bytes, 285 lines, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (`SPEC_SHA`) |
| Sandbox seed (overlay) | `$SP/exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay` (README.md, inventory/commands-a.md, inventory/commands-b.md, inventory/orca-capabilities.md, specs/orca-worker-contract-spec.md) |
| Frozen audit command | `git show 69ac8b33:src/superclaude/commands/spec-panel.md`, sha256 `e62e70b98e878cb4b60ba8f95f1cc3442a25e815828a3ef3d17a95b65ea97494` (`AUD_CMD_SHA`) |
| Frozen audit rules file | `$SP/p11/rules.md` (= `git show 69ac8b33:src/superclaude/rules/prompts/document_review_loop_prompts.md`), sha256 `3eb772f944491720af24133267681e170510ba49949af1b08db913e9eeaddfb8` (`AUD_RULES_SHA`) |
| Stage 2 data (read-only, never edit) | `$SP/p11/` (`harness.py`, `advance.py`, `rules.md`, `runs/a{1,2,3}-r*/`) |
| Second audits of the baseline finals (read-only) | `$SP/p12/baseline-audit2/a3-r{1..6}/ws/.dev/orca-command-refactor/review/audit.md`, summary `$SP/p12/baseline-audit2/results.json` |
| Shared defect catalog (built by PN3, read by PN1/PN2 if present) | `$SP/p13/catalog/catalog.json` (schema C9.4) |

Python package for all new product code: `src/superclaude/cli/review/`. File ownership (a plan creates only its own files, plus the shared files with the exact bytes given here):

| File | Owner |
|---|---|
| `src/superclaude/cli/review/__init__.py` (exact text in C0.1) | shared, identical in all three branches |
| `src/superclaude/cli/main.py`: the 3-line registration in C0.2, nothing else | shared, identical in all three branches |
| `panel.py`, `panel_cmd.py`, `data/review-panel.default.json`, `data/review-tiers.default.json`, `findings.py`, `ledger.py`, `merge_cmd.py`, `ledger_cmd.py`, `telemetry.py`, `telemetry_cmd.py` | PN1 |
| `lint.py`, `lint_cmd.py` | PN2 |
| `estimate.py`, `estimate_cmd.py` | PN3 |
| Tests: `tests/review/test_review_<topic>.py` (no `__init__.py` in `tests/review/`; every basename starts `test_review_`) | each plan its own files |
| `src/superclaude/rules/prompts/document_review_loop_prompts.md` | PN1 inserts the C4.3 text plus its own `### Review panel` section between C4.3 Insertion D and `## Never` (PLAN-1); PN2 inserts its own lines right after the line starting ``Write `review: 1 of 3` once`` and right after the line starting `Follow the re-review core below in order` (PLAN-2); PN3 changes nothing |

### C0.1 `src/superclaude/cli/review/__init__.py` (exact bytes; same in every branch)

```python
"""superclaude review: deterministic helpers for document review loops.

Subcommand modules are optional, so branches that add different subcommands
merge without touching this file.
"""

from __future__ import annotations

import importlib

import click


@click.group(name="review")
def review_group() -> None:
    """Deterministic helpers for document review loops."""


for _name in ("panel_cmd", "merge_cmd", "ledger_cmd", "telemetry_cmd", "lint_cmd", "estimate_cmd"):
    try:
        _module = importlib.import_module(f"{__name__}.{_name}")
    except ModuleNotFoundError as _exc:
        if _exc.name != f"{__name__}.{_name}":
            raise
        continue
    review_group.add_command(_module.command)
```

Every `*_cmd.py` defines a module-level `command` (a `click.Command` or `click.Group`) named `panel`, `merge`, `ledger`, `telemetry`, `lint`, `estimate` respectively. If `ruff` flags this file, fix only with `# noqa` comments the same way in every branch and list it under "Contract deviations".

### C0.2 `src/superclaude/cli/main.py` (insert immediately before the final `if __name__ == "__main__":` line, after the `issue-watch` registration)

```python
from superclaude.cli.review import review_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports

main.add_command(review_group, name="review")

```

## C1. Panel template (`review-panel/1`)

Owner definition (binding, 2026-11-10): a tier is an ALIAS for an ordered model list; the alias defaults to the first model, the others are fallbacks tried in list order when an earlier one is unavailable. Panel slots name a tier alias and a strategy; the model lists live only in the tier file (C2), so one edit there rolls out to every panel using the alias.

Default file `src/superclaude/cli/review/data/review-panel.default.json` (exact content):

```json
{
  "schema": "review-panel/1",
  "template_id": "default",
  "version": "1.0.0",
  "description": "Production review panel: 2x Tier 3 + 1x Tier 2 + 1x Tier 1b parallel independent reviewers; Tier 1b is the fixed anchor.",
  "distinct_across_slots": true,
  "apply_to": ["first"],
  "slots": [
    {"slot_id": "t1b", "tier": "tier1b", "count": 1, "strategy": "fixed"},
    {"slot_id": "t2", "tier": "tier2", "count": 1, "strategy": "random"},
    {"slot_id": "t3", "tier": "tier3", "count": 2, "strategy": "random"}
  ]
}
```

Schema rules (`panel.validate_panel(obj, tiers=None) -> list[str]`; empty list = valid): `schema == "review-panel/1"`; `template_id` matches `^[a-z0-9][a-z0-9-]{0,31}$`; `version` is `MAJOR.MINOR.PATCH`; `distinct_across_slots` bool; `apply_to` is a non-empty subset of `["first", "re-review"]` (which review kinds use the panel; the other kinds use one reviewer, the `fixed` slot's model); `slots` non-empty; `slot_id` unique, `^[a-z0-9]{1,8}$`; `tier` matches `^tier[0-9]{1,2}[a-z]?$` and, when `tiers` is given, names an alias defined there; `count` int 1..4; `strategy` is `fixed`, `random` (optional int `seed`) or `round_robin`; total reviewers 1..8; exactly one slot is `fixed` (the anchor); no keys beyond those named here plus `description`. Unknown keys are errors.

Reviewer instance ids: `<slot_id>-<i>`, `i` from 1 (`t1b-1`, `t2-1`, `t3-1`, `t3-2`).

Lookup precedence (first that exists wins; whole-file replacement): `--template PATH`; `$SUPERCLAUDE_REVIEW_PANEL`; `<project>/.superclaude/review-panel.json`; `~/.superclaude/review-panel.json`; packaged default. `<project>` = `git rev-parse --show-toplevel`, else the current directory.

## C2. Tier aliases and environment overrides (`review-tiers/1`)

Default file `src/superclaude/cli/review/data/review-tiers.default.json` (exact content; the model ids are the gateway ids of `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md`, the names are the owner's):

```json
{
  "schema": "review-tiers/1",
  "version": "1.0.0",
  "aliases": {
    "tier1a": {"alias": "claude-gw-tier1a[1m]", "models": ["claude-opus-5-5", "claude-sonnet-5-5"]},
    "tier1b": {"alias": "claude-gw-tier1b[1m]", "models": ["claude-sonnet-5-5", "gpt-6.1-sol", "muse-wonder-full-1.0"]},
    "tier2": {"alias": "claude-gw-tier2[1m]", "models": ["gpt-6.1-sol", "glm-5.3", "grok-4.7", "Qwen3.8-max", "muse-wonder-1.0", "muse-spark-1.3"]},
    "tier3": {"alias": "claude-gw-tier3[1m]", "models": ["gpt-6.1-terra", "glm-5.3", "grok-4.7", "Qwen3.8-max", "muse-wonder-1.0", "muse-spark-1.3"]},
    "tier4": {"alias": "claude-gw-tier4[1m]", "models": ["gpt-6-luna"]}
  },
  "names": {
    "claude-opus-5-5": "Claude Opus 5.5", "claude-sonnet-5-5": "Claude Sonnet 5.5", "claude-haiku-5-5": "Claude Haiku 5.5",
    "claude-fable-5-1": "Claude Fable 5.1", "gpt-6.1-sol": "GPT 6.1 Sol", "gpt-6.1-terra": "GPT 6.1 Terra", "gpt-6-luna": "GPT 6 Luna",
    "muse-wonder-full-1.0": "Muse Wonder Full 1.0", "muse-wonder-1.0": "Muse Wonder 1.0", "muse-spark-1.3": "Muse Spark 1.3",
    "glm-5.3": "GLM 5.3", "grok-4.7": "Grok 4.7", "Qwen3.8-max": "Qwen 3.8 Max"
  },
  "environments": {
    "gateway": {
      "note": "Company gateway: every listed model is served; dispatch mechanism per model not defined yet.",
      "available": "all",
      "stand_ins": {},
      "launch": {}
    },
    "anthropic-only": {
      "note": "This experiment environment. Tier 2 and Tier 3 contain no Anthropic model; owner decision 2026-11-10: Claude Haiku 5.5 stands in for both. Tier 1b resolves to Sonnet 5.5, the Stage 2 reviewer model.",
      "available": ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5", "claude-fable-5-1"],
      "stand_ins": {"tier2": ["claude-haiku-5-5"], "tier3": ["claude-haiku-5-5"], "tier4": ["claude-haiku-5-5"]},
      "launch": {"claude-opus-5-5": "opus", "claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", "claude-fable-5-1": "fable"}
    }
  }
}
```

Schema rules (`panel.validate_tiers(obj) -> list[str]`): `schema == "review-tiers/1"`; `version` semver; `aliases` maps tier names (C1 grammar) to `{"alias": str matching ^[A-Za-z0-9._/:\-\[\]]{1,128}$, "models": non-empty list of unique model ids with the same grammar}`; `names` maps model ids to display strings (optional per id); each environment (`^[a-z0-9][a-z0-9-]{0,31}$`) has `available` (`"all"` or a non-empty list of ids), `stand_ins` (tier name -> non-empty ordered list of ids, every id in `available` unless `available` is `"all"`; a tier named here must exist in `aliases`), `launch` (id -> launcher string, may be empty) and optional `note`. Adding, removing or reordering a model is a data edit only. An empty `launch` means the dispatch mechanism is undefined for that environment; `resolve` then prints `"launch": null`.

Environment selection: `--env NAME`; else `$SUPERCLAUDE_REVIEW_ENV`; else `gateway` when the variable `T3Model01` (Coder workspace tier slot) is set and non-empty; else `anthropic-only`. Lookup precedence for the tier file: `--tiers PATH`; `$SUPERCLAUDE_REVIEW_TIERS`; `<project>/.superclaude/review-tiers.json`; `~/.superclaude/review-tiers.json`; packaged default.

## C3. Resolution (pure, deterministic)

`panel.resolve_slot(models, strategy, seed, available, stand_ins, exclude=()) -> {"model", "fallback_depth", "stand_in", "fallbacks"}` is a pure function:

1. `candidates` = the alias `models` that are in `available` (all of them when `available == "all"`), in list order. If empty, `candidates` = the environment's `stand_ins` for that tier (in order) that are available, and `stand_in = true`; if still empty, raise `NoModelAvailable(tier)`.
2. `fixed`: the first candidate. `random`: `rng = random.Random(seed)`; pool = candidates minus `exclude` if that leaves at least one, else all candidates; model = `rng.choice(pool)`. `round_robin`: model = `candidates[seed % len(candidates)]` (here `seed` carries the sequence number).
3. `fallback_depth` = index of the model in the list it came from (the alias list, or the stand-in list when `stand_in`); `fallbacks` = the remaining candidates in list order starting after the chosen one and wrapping around (the order a launcher tries when the chosen model is unavailable at launch; a launcher that falls back records the new model and its depth).

`panel.resolve(panel, tiers, env, run_id, review_kind="first", seed=None, sequence=None) -> dict`: if `review_kind` is not in `apply_to`, only the `fixed` slot is resolved (one reviewer). Otherwise process the `fixed` slot first, then the other slots in file order, instances `i = 1..count`. Per instance seed for `random`: slot `seed` if present, else the `seed` argument, else `int(sha256(run_id).hexdigest()[:8], 16)`; the value passed to `resolve_slot` is `f"{base}|{slot_id}|{i}"`. For `round_robin` pass `(sequence if given else date.today().toordinal()) + i - 1`. `exclude` = models already chosen when `distinct_across_slots`. Output (`review-panel-resolution/1`): `{"schema", "template_id", "template_version", "template_sha256", "tiers_version", "tiers_sha256", "environment", "run_id", "review_kind", "reviewers": [{"reviewer_id", "slot_id", "tier", "alias", "strategy", "seed", "model", "model_name", "fallback_depth", "stand_in", "fallbacks", "launch"}]}`; `*_sha256` = sha256 of the JSON dumped with `sort_keys=True, separators=(",", ":")`. Equal inputs give byte-identical output.

In `anthropic-only` the default template resolves, for every run id, to `t1b-1 = claude-sonnet-5-5` (launch `sonnet`, depth 0, `stand_in` false), and `t2-1`, `t3-1`, `t3-2 = claude-haiku-5-5` (launch `haiku`, depth 0 in the stand-in list, `stand_in` true). Required unit tests (real alias lists): Tier 3 with only haiku available resolves through the stand-in with `stand_in` true; Tier 1b with `claude-sonnet-5-5` removed from `available` falls back to `gpt-6.1-sol` at depth 1 (environment `available: ["gpt-6.1-sol"]`), and with only `muse-wonder-full-1.0` available resolves at depth 2; `random` with a fixed seed returns the same model every call and never one outside the candidates; `distinct_across_slots` excludes an already chosen model when another candidate exists; reordering an alias list in a tmp tier file changes the `fixed` result with no code change.

## C4. Findings block (`findings-v1`) and fix map (`fixmap-v1`)

### C4.1 Findings block format

The last section of a review report is the heading `## Findings block` followed by one fenced code block whose info string is exactly `findings-v1`; each non-empty line inside is one JSON object; an empty block means no findings.

- Finding line keys: `id` (`^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$`, unique in the report), `severity` (`CRITICAL`|`MAJOR`|`MINOR`), `blocking` (bool; `true` with `MINOR` is an error), `category` (`contradiction`|`unpassable-check`|`data-loss`|`safety`|`missing-requirement`|`other`), `anchor` (string, 12..200 characters after whitespace flattening, copied verbatim from the candidate), optional `anchor2` (same rules; the other side of a contradiction), `refs` (list of at most 8 strings), `claim` (string, at most 300 characters).
- Prior line keys (re-reviews only): `prior` (a ledger id such as `L3`), `status` (`resolved`|`open`|`regressed`).
- Parser `findings.parse_block(report_text) -> {"ok": bool, "findings": [...], "priors": [...], "errors": [{"line": n, "msg": str}]}`. `ok` is false when the heading or fenced block is missing, or any line errors; good lines are still returned. If more than one `findings-v1` block exists, the last one is used and an error is recorded.

### C4.2 Fix map format

The reviser's output ends with `## Fix map` and one fenced block with info string `fixmap-v1`: one JSON object per line, `{"id": "L3", "action": "applied"|"rejected", "reason": "<one sentence>"}`. Parser `findings.parse_fixmap(text)` returns the same shape as C4.1 with `items`. Fallback when the block is missing: ids taken from table rows `| <id> | applied ... |` (case-insensitive `applied`), `ok = false`.

### C4.3 Rules-file text (PN1 inserts it in its branch; PN3's harness inserts it into experiment copies only)

Insertion A: a new line immediately after the line that starts `- First-review brief: "`:

```text
- **Findings block**: end the report with the findings block described under "Findings block" below, one line per finding, blocking or not.
```

Insertion B: a new line immediately after the line that starts `- Re-review brief: "`:

```text
- **Findings block**: end the report with the findings block described under "Findings block" below: one line per finding you report and one prior line per prior blocking finding.
```

Insertion C: a new line immediately after the line that starts `- Revise brief: "`:

```text
- **Fix map**: end your output with the fix map described under "Fix map" below.
```

Insertion D: the following block, inserted immediately before the line `## Never` (with one blank line before and after):

```text
### Findings block

The last section of every review report is `## Findings block`: one fenced code block whose info string is `findings-v1`, holding one JSON object per line and nothing else. A report with no finding has an empty block.

- Finding line: `{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "<text copied exactly from the candidate>", "anchor2": "<optional second exact quote>", "refs": ["AC-0.4"], "claim": "<one sentence naming the wrong outcome>"}`. `severity` is CRITICAL, MAJOR or MINOR. `blocking` is true only for a finding that passes the grading check. `category` is one of contradiction, unpassable-check, data-loss, safety, missing-requirement, other. `anchor` is 12 to 200 characters copied exactly from the candidate: the text that is wrong; for a contradiction `anchor2` is the other side. `refs` lists the requirement ids and section numbers the finding rests on.
- Prior line, re-reviews only: `{"prior": "L3", "status": "resolved"}`, with status resolved, open or regressed, one line per prior blocking finding id.
- The block restates the findings discussed above it and adds none. The verdict line stays the reviewer's verdict.

### Fix map

The reviser ends its output with `## Fix map`: one fenced code block whose info string is `fixmap-v1`, one JSON object per line, `{"id": "L3", "action": "applied", "reason": "<one sentence>"}`, with action applied or rejected, one line per blocking id in the brief.
```

## C5. Anchors, sections, refs, fingerprint, same-defect

- `flat(s)` = `" ".join(s.split())`. `locate(text, quote)` = every occurrence of `flat(quote)` in the whitespace-flattened `text`, returned as half-open 0-based line ranges `(start, end)` (algorithm: the `locate()` of the #346 ledger prototype, `$SP/exp346/.dev/experiments/346-validation/phase5/final-bundle/builds/ledger/repo-files/src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py` lines 134-171; reimplement, do not import). First occurrence is used; more than one occurrence sets `anchor_ambiguous`; none sets `anchor_status = "missing"` (the finding is kept, with no span).
- `section_of(text, line)`: the nearest heading at or above `line` (`^#{1,6}\s+(.*)$`); if its text starts with a number `^(\d+(?:\.\d+)*)`, that number, else the heading text lowercased with runs of non-alphanumerics replaced by `-`; `"top"` before any heading.
- `refs_norm(finding)`: uppercase, unique, sorted matches of `\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b` over `anchor`, `anchor2`, `claim` and each `refs` entry, plus each `refs` entry that matches `^\d+(?:\.\d+)*$` (section numbers); drop tokens starting `SHA-`.
- Fingerprint: `fp = sha256("v1|" + section_of(anchor line) + "|" + ",".join(refs_norm)).hexdigest()[:16]` (section `"none"` when the anchor is missing).
- `same_defect(a, b)` on the same document version: `a.fp == b.fp`; or both have spans, some span of `a` (anchor or anchor2) and some span of `b` are within 3 lines of each other (`a.start <= b.end + 3 and b.start <= a.end + 3`), and (`refs_norm` intersect, or both are empty).
- Clusters: union-find over findings in input order (reviewer order = resolution order, then report order); cluster order = order of first member.
- Span mapping old -> new version: `difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False).get_opcodes()`; an `equal` line maps 1:1; a line inside a `replace`/`delete` opcode maps to the start of that opcode's new range. A hunk "touches" a span when its old range overlaps the span (zero-width hunks at position p touch spans with `start <= p <= end`).

## C6. Ledger (`review-ledger/1`)

File (default `<review dir>/ledger.json`), written atomically (temp file + `os.replace`), only by the script:

```json
{"schema": "review-ledger/1", "doc": "<path>", "cap_reviews": 3,
 "rounds": [{"n": 1, "doc_sha256": "...", "reviewers": [{"reviewer_id": "t1b-1", "model": "claude-sonnet-5-5", "report": "<path>", "report_sha256": "...", "block_ok": true}], "verdict": "FAIL", "decision": "REVISE"}],
 "rows": [{"lid": "L1", "fp": "...", "blocking": true, "severity_max": "CRITICAL", "category": "contradiction",
           "confidence": "overlap", "status": "open", "anchor": "...", "anchor2": null, "span": [s, e], "span2": null, "refs": ["AC-0.4"],
           "members": [{"round": 1, "reviewer_id": "t1b-1", "fid": "F1", "blocking": true}],
           "history": [{"round": 1, "event": "opened"}]}]}
```

- Row = one cluster. `blocking` = any member blocking. `confidence` = `overlap` when members come from at least 2 distinct reviewers of one round, else `single`. Representative anchor/span = the first member's; spans are kept current by span mapping after each revision.
- Statuses: `open`, `resolved_check`, `resolved`, `regressed`, `deferred`. Only the script changes them:
  - new cluster matching no row (same_defect against each row's current anchor/span/refs) -> new row `open`, event `opened`;
  - cluster matching a row in `resolved_check` or `resolved` -> `regressed`, event `refound`;
  - cluster matching an `open`/`regressed` row -> status unchanged, event `refound`;
  - after a revision: a row named `applied` in the fix map whose span or span2 is touched by a hunk -> `resolved_check` (event `resolved_check`); named but not touched -> stays, event `named_not_touched`; `rejected` -> stays, event `rejected_by_reviser`;
  - after the next review round, a `resolved_check` row that no cluster matched -> `resolved`, event `cleared`;
  - `defer` (human command) -> `deferred`.
- Verdict of a round: `FAIL` when any `blocking` row is `open` or `regressed`, else `PASS`. Decision: `PASS` -> `PASS`; `FAIL` with round `< cap_reviews` -> `REVISE` (brief ids = blocking rows `open`/`regressed`, ledger order); `FAIL` at `cap_reviews` -> `ESCALATE`. Reviewers' prior lines are recorded (`members`/`history` notes) but never change a status.

## C7. Capture matrix (`review-capture/1`), PN1 exports, PN3 consumes

```json
{"schema": "review-capture/1", "source": "<ledger path or catalog path>", "round": 1, "doc_sha256": "...",
 "occasions": ["t1b-1", "t2-1", "t3-1", "t3-2"],
 "defects": [{"key": "L1", "blocking": true, "captured_by": ["t1b-1", "t3-2"]}]}
```

`captured_by` lists occasions in which a member of that row was reported in that round (any severity). Consumers filter on `blocking` themselves. Only whole-document reviews of one document version (first reviews and audits) are valid capture occasions; scoped re-reviews are not.

## C8. Telemetry (`review-telemetry/1`)

Directory (in the project repo, committed and pushed): `.dev/benchmarks/review-telemetry/` (override `--dir` or `$SUPERCLAUDE_REVIEW_TELEMETRY_DIR`). Files: `records/<YYYY>/<MM>/<run_id>.jsonl` (reviewer records) and `records/<YYYY>/<MM>/<run_id>.outcomes.jsonl` (outcome records); `YYYY/MM` from the first record's UTC time. Append-only: a writer opens with `"a"`, writes one line per record, never rewrites or deletes a line; a correction is a new record with `supersedes: <record_id>`. One `run_id` per review loop (`^[A-Za-z0-9._-]{1,64}$`). No document text, quotes, anchors or claims ever enter a record (the test in PN1 checks that no 40-character substring of the reviewed document appears in any record).

Reviewer record (`kind: "reviewer_run"`), all keys required (use `null` when unknown):

```json
{"schema_version": "review-telemetry/1", "kind": "reviewer_run", "record_id": "<uuid4 hex>", "ts_utc": "2026-11-10T12:00:00Z",
 "run_id": "b1-r1", "step": "R1", "round": 1, "reviewer_id": "t3-1",
 "panel": {"template_id": "default", "template_version": "1.0.0", "template_sha256": "...", "tiers_version": "1.0.0", "tiers_sha256": "...", "environment": "anthropic-only", "panel_size": 4},
 "slot": {"slot_id": "t3", "tier": "tier3", "alias": "claude-gw-tier3[1m]", "strategy": "random", "seed": "123|t3|1", "fallback_depth": 0, "stand_in": true},
 "model": {"resolved": "claude-haiku-5-5", "launch": "haiku", "observed": "claude-haiku-5-5"},
 "task": {"doc_sha256": "...", "doc_bytes": 57763, "doc_lines": 285, "language": "en", "doc_format": "markdown", "specialization": "software-spec",
          "sections": 0, "max_heading_depth": 0, "tables": 0, "table_rows": 0, "ids_defined": 0, "cross_refs": 0, "rfc2119": 0, "review_kind": "first"},
 "output": {"block_ok": true, "findings": 0, "blocking": 0, "by_severity": {"CRITICAL": 0, "MAJOR": 0, "MINOR": 0}, "verdict": "FAIL", "verdict_mismatch": false},
 "cost": {"tokens_in": 0, "tokens_cache_read": 0, "tokens_cache_write": 0, "tokens_out": 0, "wall_s": 0.0},
 "context": {"experiment": "pn1", "arm": "b1", "replicate": 1}}
```

Task variables (`telemetry.task_variables(text, specialization="unspecified", review_kind="first")`): `sections` = lines matching `^#{1,6}\s`; `max_heading_depth` = most `#`; `tables` = blocks of consecutive lines starting `|` that contain a separator line `^\|\s*:?-{3,}`; `table_rows` = table lines minus header and separator lines; `ids_defined` = distinct tokens of the C5 id regex that appear as the first cell of a table row or right after `**` at a line start; `cross_refs` = all occurrences of the C5 id regex plus `\bsection\s+\d+(?:\.\d+)*` (case-insensitive) minus `ids_defined` occurrences; `rfc2119` = occurrences of `\b(?:MUST|MUST NOT|SHALL|SHOULD|MAY|REQUIRED)\b`; `language` = `"en"` when at least 2% of the words are in `{the, and, of, to, is, a, in, that, for}`, else `"unknown"`; `review_kind` = `first` | `re-review` | `audit`.

Outcome record (`kind: "outcome"`), appended later when audits/adjudication exist:

```json
{"schema_version": "review-telemetry/1", "kind": "outcome", "record_id": "...", "ts_utc": "...", "run_id": "b1-r1", "reviewer_record_id": "<record_id of the reviewer_run>",
 "truth_basis": "catalog-v1|theme-v1|adjudicated-v1", "confirmed_tp": 0, "false_pos": null, "unconfirmed": 0, "unique_tp": 0,
 "overlap_mean_jaccard": null, "recall_vs_confirmed": null, "precision": null, "cost_per_confirmed_tp": null, "supersedes": null}
```

`confirmed_tp` = the reviewer's blocking findings that map to a confirmed defect; `false_pos` = blocking findings an adjudicator rejected (null when not adjudicated); `unconfirmed` = blocking findings neither confirmed nor rejected; `unique_tp` = confirmed defects no other reviewer of the same round found; `overlap_mean_jaccard` = mean Jaccard of this reviewer's confirmed-defect set with each other reviewer's of the round; `precision` = `confirmed_tp / (confirmed_tp + false_pos)` (null if the denominator is 0 or unknown); `recall_vs_confirmed` = confirmed defects found / confirmed defects present in the reviewed version; `cost_per_confirmed_tp` = `tokens_out / confirmed_tp` (null if 0).

`slot.stand_in` is true whenever the model came from an environment stand-in list; such records are never scores for the tier they stand in for. `model.observed` is the model the transcript reports (`message.model`), `null` if unknown; when it differs from `resolved`, the record keeps both.

Loader `telemetry.load(dir, db_path)`: reads every `*.jsonl` under `dir/records/`, validates, inserts into SQLite tables `reviewer_runs` (one column per leaf key, dotted names joined by `_`, e.g. `model_observed`, `slot_stand_in`, `task_doc_bytes`, `cost_tokens_out`) and `outcomes`, primary key `record_id`, idempotent (re-loading inserts nothing new); creates view `model_scores` = per `model_observed`, `slot_tier` and `slot_stand_in`: `n_runs`, `sum(confirmed_tp)`, `sum(false_pos)`, mean `precision`, mean `recall_vs_confirmed`, `sum(unique_tp)`, `sum(cost_tokens_out) / nullif(sum(confirmed_tp), 0)`; superseded records are excluded from the view. Invalid lines are reported (path:line) and skipped, never fatal.

## C9. Experiment conventions shared by all plans

### C9.1 Token counting (binding)

Output tokens of a worker = sum of `message.usage.output_tokens` over assistant lines of its transcript, counting each `message.id` ONCE (a message is logged once per content block; summing lines double-counts). A transcript belongs to `(run, step)` when one of its first 6 lines contains the absolute path of that step's `PROMPT-<step>.md`. If several transcripts match one step, keep the one whose assistant `model` is the expected model and that has the most output tokens, and print a WARN. Measured baseline with this method (Stage 2 arm 3, n=6, coordinator figures): loop ~100,000 output tokens per replicate, one audit ~69,000, loop plus one audit ~169,000 (`B_TOK`); arm 1 loop plus one audit ~562,000 (3.3 x `B_TOK`). Per-step arm-3 means (planner recount, same method): R1 50,576; V1 14,255; R2 29,993; AUD 69,043. Every plan's harness has `harness.py basetokens`, which recomputes `B_TOK` this way from the p11 transcripts and prints per-run values; analyses use the recomputed value, and every token criterion is a ratio to `B_TOK`. Older figures (0.33M, 243,056, 381,702) are double-counted: never use them.

### C9.2 Frozen audit (identical in every plan, run TWICE per final spec)

`AUD` and `AUD2` are the Stage 2 audit exactly: fresh sandbox `runs/<run>/aud` (or `aud2`) = overlay copy + the run's final spec + `command.md` from `BASE_REF` (assert `AUD_CMD_SHA`) + `home/.claude/rules/prompts/document_review_loop_prompts.md` copied from `$SP/p11/rules.md` (assert `AUD_RULES_SHA`); prompt = p11 `WRAP` with `CMDPART` and the p11 AUD brief unchanged (see `$SP/p11/runs/a3-r1/PROMPT-AUD.md`); worker model `sonnet`; output `aud*/ws/.dev/orca-command-refactor/review/audit.md`. The audit is never given a findings block instruction. Primary quality metric `BLK` = mean number of blocking ids per audit, ids parsed by C9.3 `parse_ids(ids_from(path))` when the verdict is FAIL, else 0, over both audits of every completed run. Baseline `B_BLK` = 1.50 over the 12 baseline audits (6 first + 6 second, each 9/6); recompute it with the same functions and report any difference.

### C9.3 Prose parsing of Stage 2 style reports (for audits and old reports)

```python
THEMES = [("T3", r"AC-0\.4|\bP0\b|Phase 0"),
          ("T2", r"WC-4|contract (?:file )?(?:path|location)|--output"),
          ("T1", r"AC-1\.[12]|/sc:load|\bP1\b|Phase 1|command counts?|\b36\b")]   # re.I; first match wins
EXCL = {"FR", "AC", "SHA", "WC", "INV", "SPEC", "CMD", "P", "GC", "SA", "NFR", "D"}
ID_TOKEN = r"\b(?:R\d-)?[A-Z]{1,4}-?\d+\b"
IDS_LINE = r"(?im)^\W*(?:\*\*)?(?:Reviser brief\W*)?Blocking (?:finding )?ids?\b[^:\n]{0,60}:\s*(.+)$"
CITE = (r"(?i)(?:\b(?:spec(?:\.md)?|S)\s*:\s*|\blines?\s+|\bL(?=\d))"
        r"(\d{1,3}(?:\s*[-–]\s*\d{1,3})?(?:\s*(?:,|and)\s*\d{1,3}(?:\s*[-–]\s*\d{1,3})?)*)(?![\d.])")
```

- `ids_from(path)`: p11 `ids_from` with its first regex replaced by `IDS_LINE`.
- `parse_ids(raw)`: `None` or `(?i)^\W*none\b` gives `[]`; cut `raw` at the first match of `\.\s|\.$|\(|;|\n`; delete `*`; return `ID_TOKEN` matches in order, deduplicated, dropping tokens whose leading letters are in `EXCL`.
- `find_section(text, fid)`: try line prefixes heading `^\s*#{2,6}\s*(?:\*\*)?`, bold `^\s*(?:[-*]\s*)?\*\*`, table row `^\s*\|\s*(?:\*\*)?`, each followed by `re.escape(fid) + r"(?![\w-])"`; body = following lines up to the next heading or bold id line (table row: empty body).
- `tag(heading, body)`: `THEMES` on the heading, else on the first non-empty body line, else `other`.
- `cited(text)`: line numbers from `CITE` (ranges expanded when `0 <= b - a <= 30`), kept in 1..400.

Theme meanings: T1 = Phase 1 / AC-1.1 scope versus `/sc:load` rows and command counts; T2 = WC-4 contract path `<output-dir>/return-contract.yaml` versus file-valued `--output` or missing output flags; T3 = AC-0.4 needs the WC-4 contract status in Phase 0, before any contract exists. Expected tags (from the previous planning round, keyword proxy; verify and correct with an overrides file, never by editing regexes to fit):

| run | R1 blocking (id theme) | first audit blocking (id theme) |
|---|---|---|
| a3-r1 | F1 T3, F2 T1 | B1 T1, B2 T2 |
| a3-r2 | R1-B1 T1, R1-B2 T2 | F-01 T3, F-02 T1 |
| a3-r3 | F1 T1, F2 T1, F3 T3 | F-1 T1, F-2 T2 |
| a3-r4 | F-01 T1 | A-01 other, A-02 T2 |
| a3-r5 | F-1 T1, F-2 T3, F-3 other | PASS |
| a3-r6 | REQ-1 T2, REQ-2 T1, ARCH-1 T2 | F-01 T2 |
| a2-r1 | B-1 T3, B-2 T1 | F-1 T1, F-2 T2 |
| a2-r2 | B1 T1, B2 T2 | F-01 T2, F-02 T3 |
| a2-r3 | PASS | REQ-1 T1, REQ-2 T1, ARCH-1 T2 |
| a2-r4 | B-1 T1 | F-1 T1, F-2 T2, F-3 other |
| a2-r5 | B-1 T2, B-2 T3 | F-1 T1 |
| a2-r6 | F-01 T1 | PASS |

### C9.4 Defect catalog (`defect-catalog/1`, built by PN3 Phase O1; PN1/PN2 read it if present, else fall back to theme-v1 truth)

```json
{"schema": "defect-catalog/1", "doc_sha256": "<SPEC_SHA>", "built_by": "pn3", "sources": ["a3-r1/R1", "a3-r1/AUD", "a3-r1/AUD2", "..."],
 "clusters": [{"cid": "D1", "theme": "T1", "label": "<short>", "anchor": "<quote from the original spec>", "orig_span": [s, e],
               "members": [{"source": "a3-r1/R1", "fid": "F2", "blocking": true, "quote": "<quote>", "doc": "original|final"}],
               "n_sources": 3, "confirmed": true}],
 "revision_introduced": [{"source": "a3-r4/AUD", "fid": "A-01", "quote": "..."}],
 "unanchored": [{"source": "...", "fid": "...", "reason": "..."}],
 "overrides": [{"action": "merge|split|move", "cids": ["D3", "D4"], "reason": "...", "quote": "..."}],
 "residual": {"a3-r1": {"present": ["D1", "D2"], "audit_hits": {"AUD": ["D1"], "AUD2": ["D2"]}}}}
```

A cluster is `confirmed` when at least 2 independent sources report it as blocking (each worker is one source; the two audits of a run are two sources). Truth labels used by any analysis are named in its output: `catalog-v1` (this file), `theme-v1` (C9.3 tags only) or `adjudicated-v1` (a blind adjudicator's verdicts).

### C9.5 Worker launch convention

Each harness's `advance.py` prints one line per prompt to launch: `LAUNCH <model-alias> <absolute PROMPT path>`. The coordinator (or the implementer, if it has an Agent tool) launches one subagent per line with that `model` and the message `Read <absolute PROMPT path> and follow it exactly. Touch nothing outside the sandbox directory it names.` At most 6 workers of one plan run at once (`advance.py` never prints more than `6 - running`). Workers are never told which arm, model or slot they are.
