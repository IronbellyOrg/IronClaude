# PLAN PN2 (S2): mechanical pre-check suite (requirements lint)

You build and measure ONE design from research report 2, section 3.2 (table row 3): a deterministic, stdlib-only `superclaude review lint` that extracts ids, references, counts, named values, phase rows and path templates from a markdown spec and reports mechanical inconsistencies as evidence for the reviewer. First you measure every check offline on all documents on disk (no workers); only if a check proves useful you stage a 6-replicate live loop where the lint output is given to the reviewers. The appendix holds the SHARED CONTRACT (C0-C9): binding, wins over this text. PN2 uses C0, C9 and, if present, the C9.4 catalog; it needs no panel, ledger or telemetry.

## 0. Read this first

Read the whole file before running anything. Do not open the other plans.

Hard rules (from `/home/user/IronClaude/CLAUDE.md`, binding):
- Python only through UV (`uv run ...`; scratch scripts `uv run --no-project python <file>`; their tests `uv run --no-project --with pytest pytest <dir>`). Never `pip`, `python -m`, bare `python`.
- Never stage or commit anything under `.claude/`; `git add -f` is the violation siren. Edit only `src/superclaude/` and `tests/`, then `make sync-dev` and `make verify-sync`.
- Do not edit `src/superclaude/commands/spec-panel.md` (490 lines; cap 500). The rules file never names a `src/superclaude/...` path; it reaches the lint only as `superclaude review lint`.
- Work only in your full clone `$CLONE`; never edit `$SP/p11/`, `$SP/p12/`, `$SP/p5/`, `$SP/exp346/`.
- Push your branch to `origin` (`https://github.com/IronbellyOrg/IronClaude`); no pull request; never touch `SuperClaude-Org/SuperClaude_Framework`.
- The lint must not trip the finding-quota scan of `tests/skills/test_review_prompt_overrides.py`: never write phrases like "find at least N" in the rules file.
- You cannot spawn sub-workers. Implement, measure offline (Phase O), build the harness, push, STOP with the READY report. With an Agent tool you may run the live phase yourself, at most 6 concurrent workers.

```bash
export SP=/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad
export CLONE=$SP/p13/clones/pn2 AB=$SP/p13/ab2 BR=346Claude-pn2-mechanical-lint
```

## 1. Background

The loop, baseline and harness are those of Stage 2 arm 3 (read `$SP/p11/harness.py`, `$SP/p11/advance.py`, `$SP/p11/runs/a3-r1/PROMPT-{R1,V1,R2,AUD}.md`, `$SP/p11/runs/a3-r6/PROMPT-R3.md`). Baseline: 6/6 PASS, 2.17 reviews, growth +1.41%, `B_TOK` ~169,000 output tokens per replicate (each message id counted once, C9.1), `B_BLK` 1.50 over 12 audits.

**What exists on disk (the report's "12 clean final documents" and "3 originals" corrected).** No real spec on disk is clean: 12 of the 15 Stage 2 finals converged (arms 2 and 3) but 10 of their 12 first audits FAIL. There is ONE original spec (C0) and three reference snapshots of an older #346 loop (`spec-v2-after-round1.md`, `spec-v3-after-round2.md`, `spec-v4-after-round3.md` under `$SP/exp346/.dev/experiments/346-validation/phase2/S1/inputs/reference-snapshots/`). The only clean-by-construction documents are the synthetic `$SP/p5/docs/clean.md` and `minor.md` (typos only); `seeded.md`, `cand_deletion.md`, `cand_regression.md` carry known defects listed in `$SP/p5/docs/truth.json` (retry count 8 vs 5, log deletion vs 30-day retention, secret logged; removed FR-5 still referenced; retry regression). So "false positives on clean documents" is measured on 2 synthetic documents (small), and mechanical precision is measured by adjudicating every flag on the real documents.

**Targets.** The recurring audit themes (C9.3): T1 Phase 1 / AC-1.1 scope versus `/sc:load` rows and command counts (counts in the original: section 3 says 43 commands = 21 + 22, split 10 + 27 + 6; headings `### 3.1 Ready today (10)`, `### 3.2 Needs a change (27)`); T2 WC-4 path `<output-dir>/return-contract.yaml` versus per-command report paths and file-valued `--output`; T3 AC-0.4 (Phase 0) requires the WC-4 contract status of 7.2 step 3, which Phase 1 introduces. A count check can reach T1, a path-template check T2, a phase-order check T3. Whether they do is what Phase O measures.

## 2. Pre-registered criteria

**Offline gates** (Phase O; computed by `$AB/offline/score.py`):
- `MP(c)` = mechanical precision of check c = flags adjudicated true-mechanical / all adjudicated flags (the inconsistency the flag states really exists in the text, shown by quoting both sides).
- `HIT(c, T)` = share of audited documents whose audits report theme T as blocking in which c flags a line within 3 lines of a line the audit finding cites, or flags a quote matching T's C9.3 regex.
- `CLEAN(c)` = flags of c on `clean.md` plus `minor.md`.
- G1 (live phase worth running): some check with `MP >= 0.8` and `CLEAN = 0` has `HIT >= 0.5` for at least one of T1, T2, T3.
- Live check set = checks with `MP >= 0.8` and `CLEAN = 0`. Other checks stay in the tool but are not shown to live reviewers.
- ADOPT-TOOL (independent of the live phase): a check with `MP >= 0.9`, `CLEAN = 0` and at least one positive control caught is recommended as an informational tool.

**Live decision** (arm `l2`, n=6, only if G1 holds and the coordinator says go). `BLK_T`, `PASS_T`, `GROWTH_T` as in Stage 2; `R_TOK = TOK_T / B_TOK` (loop + AUD, C9.1); `THEME_T` = share of test audits reporting a theme in the live check set's hit themes, versus the same share over the 12 baseline audits (`THEME_B`, computed by `analyze`).

| Rule | Condition |
|---|---|
| DROP | `BLK_T >= B_BLK` (1.50), or `R_TOK > 1.25`, or `PASS_T < 5/6`, or `GROWTH_T > 2.82%` |
| ADOPT | no DROP, `BLK_T <= B_BLK - 0.5` (1.00), `THEME_T <= 0.5 * THEME_B`, `R_TOK <= 1.15` |
| INCONCLUSIVE | anything else; fewer than 5 completed runs; arm means of AUD and AUD2 differ by more than 0.75 |

A lint costs no model tokens, so the expected effect is small; this is why ADOPT asks for a 0.5 drop, not a halving. Report also the R1 output tokens versus baseline (the report's "fewer rounds rediscovering mechanical facts").

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
git remote -v
uv venv && make install
uv run pytest -q tests/skills/test_review_brief_placement.py tests/skills/test_spec_panel_review_loop.py \
  tests/skills/test_review_loop_extension.py tests/skills/test_review_severity_mapping.py \
  tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_rule.py tests/cli/test_cli_registration.py
```

Record the pass count as `PINNED_BEFORE`.

### A2. The checks (`src/superclaude/cli/review/lint.py`, stdlib only, pure functions, input text -> result)

Parse once: lines, headings (number and title), tables (header, rows, cells, line numbers), backticked spans, bold line starts. Ids use the C5 regex `\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b`.

| Check | What it flags | Class |
|---|---|---|
| `REF` dangling reference | an id or `section N.N` / `N.N step K` referenced but never defined (defined = a heading number, a table row's first cell, or an id in bold at a line start) | fact |
| `COUNT` count mismatch | (a) a heading ending `(N)` whose first table below has a different number of data rows; (b) a sentence `N <noun> ... (A in X, B in Y)` or `split into A ..., B ... and C ...` whose parts do not sum to N; (c) `all N` / `the N <noun>` next to a list or table with a different item count | fact |
| `KV` conflicting value | the same backticked key bound to two different values (`` `key` = v ``, `` `key`: v ``, `` | `key` | v | ``) in different sections; and the same quantity (same unit word among times, attempts, retries, seconds, minutes, hours, days, KiB, MB, and the same head-word stem within the 3 preceding words) with different numbers in different sections | possible |
| `PHASE` phase order | an acceptance row of phase Pk (a table row holding `Pk` and an `AC-k.x` id) that references an id or section whose first appearance in the phased-rollout table is in a phase after Pk (section refs expand to the ids defined in that section) | fact |
| `PATH` path template | a backticked path template with a `<placeholder>` defined in a requirement row, versus backticked paths in table rows with the same basename that do not match it (`fnmatch`, placeholder -> `*`) | possible |
| `RFC` census | counts of MUST/SHALL/SHOULD/MAY per section (information only, never a flag) | info |

Output schema `review-lint/1`: `{"schema": "review-lint/1", "doc_sha256", "doc_bytes", "checks": ["REF", ...], "findings": [{"lint_id": "LINT-REF-1", "check": "REF", "class": "fact|possible", "lines": [a, b], "quote": "<at most 200 chars>", "other_lines": [c, d] or null, "message": "<one sentence>"}], "census": {...}}`, findings ordered by line then check; ids numbered per check in that order. Same input gives byte-identical output.

CLI `src/superclaude/cli/review/lint_cmd.py`, command `lint DOC [--format json|md] [--out PATH] [--checks REF,COUNT,...]`: exit 0 always (informational); exit 2 for an unreadable file or one over 2 MB. The md format: line 1 `lint: superclaude review lint, review-lint/1, sha256 <sha>`, then one `### LINT-...` block per finding with check, class, lines, the quote and the message, then the census table. Also add the C0.1 `__init__.py` (exact bytes) and the C0.2 `main.py` lines.

### A3. Rules file (PN2 insertion points; do not touch any other line)

Insertion P (a new line immediately after the line that starts ``Write `review: 1 of 3` once``):

```text
- **Lint evidence**: before each review the coordinator runs `superclaude review lint <candidate> --format md --out <review dir>/lint-<N>.md` and passes the file as the value lint. When the brief gives lint, read that file first and address each lint id in the report: confirm it as a finding graded with the grading check, or dismiss it with the quote that shows it is not a defect. A lint id never fails the review by itself.
```

Insertion Q (a new line immediately after the line that starts `Follow the re-review core below in order`):

```text
- **Lint evidence**: when the brief gives lint, the file was produced on the revised candidate; address each lint id whose lines the diff touches and each lint id that is new since the prior review, as in the first review.
```

### A4. Tests first (`tests/review/test_review_lint.py`, `tests/review/test_review_lint_rules_text.py`)

Write before the code: per check, one small positive and one negative inline markdown sample (for example a heading `### Ready (3)` over a 2-row table flags COUNT; over a 3-row table does not; `AC-0.1` in a P0 row citing `WC-9` that first appears in the P2 row flags PHASE); schema keys and ordering; byte-identical output twice; md format first line; exit codes; `--checks` filter; a file over 2 MB gives exit 2; the CLI is reachable as `superclaude review lint`. Rules text test: Insertions P and Q present exactly once at their places, every token of `test_review_brief_placement.py` still present, no `src/superclaude`. After Phase O, add pinned regression tests on the p5 documents for what Phase O actually found (copy `clean.md`, `minor.md`, `seeded.md`, `cand_deletion.md` into `tests/review/fixtures/`): pin the true behavior, including a known false positive if one exists (name it in the test).

### A5. Verify, commit, push

```bash
cd $CLONE
uv run pytest -q tests/review && uv run pytest -q tests/skills tests/cli tests/unit   # compare with PINNED_BEFORE
grep -rn 'src/superclaude' src/superclaude/rules/prompts/document_review_loop_prompts.md   # no output
uv run superclaude review lint $SP/p5/docs/seeded.md --format md | head -40
make lint && make sync-dev && make verify-sync
git status --short        # only src/superclaude/cli/review/{__init__,lint,lint_cmd}.py, cli/main.py, rules file, tests/review/**
git add src/superclaude/cli/review src/superclaude/cli/main.py src/superclaude/rules/prompts/document_review_loop_prompts.md tests/review
git commit -F - <<'EOF'
experiment(review): mechanical requirements lint as reviewer evidence (PN2, refs #346)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Y28dBfZHbPhB1U1EM1XTUj
EOF
git push -u origin $BR || echo "PUSH FAILED: report it"
git rev-parse HEAD        # PRODUCT_REF
```

Pre-existing failures elsewhere: verify with `git stash -u` on the base, report, do not fix.

## 4. Phase O: offline measurement (you run it; zero workers)

Work in `$AB/offline/`; call the lint as `uv run --project $CLONE superclaude review lint <doc> --format json`.

**O1. Corpus** (`corpus.py` writes `corpus.json`: path, sha256, bytes, group; documents with equal sha256 are linted once and listed with all their paths):
- `orig`: the original spec.
- `final`: `$SP/p11/runs/*/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (15; group by arm).
- `hist`: `$SP/p11/runs/*/ws/.dev/orca-command-refactor/specs/history/spec-v*.md` (spec-v1 equals the original; keep the distinct ones).
- `ref`: the three reference snapshots.
- `pos`: `$SP/p5/docs/seeded.md`, `cand_deletion.md`, `cand_regression.md` (truth in `truth.json`).
- `clean`: `$SP/p5/docs/clean.md`, `minor.md`.
- `other`: the 10 largest tracked markdown files under `docs/` of `$CLONE` that contain at least 3 numbered headings (`git -C $CLONE ls-files 'docs/*.md' 'docs/**/*.md'`); unlabelled, for mechanical precision only.

**O2. Truth labels.** For each `final` document: its audit reports (`$SP/p11/runs/<run>/aud/ws/.dev/orca-command-refactor/review/audit.md`, and for a3 runs also `$SP/p12/baseline-audit2/<run>/ws/.dev/orca-command-refactor/review/audit.md`); blocking findings by C9.3 (`parse_ids(ids_from())`, `find_section`, `tag`, `cited`). For `orig`: the blocking findings of the 12 arm-2/3 R1 reports (`round1.md`) and 3 arm-1 R1 reports (`spec-panel.md`). If `$SP/p13/catalog/catalog.json` exists, also use its confirmed clusters (`orig_span`, `residual`). Write `truth.json` (per document: theme -> list of cited line sets).

**O3. Adjudication.** Run the lint over the corpus. For every flag on `orig`, `final`, `hist`, `ref`, `other` decide true-mechanical or false-mechanical by reading both cited places, and write `adjudication.jsonl` lines `{"doc_sha", "lint_id", "verdict": "true|false", "evidence": "<quote A> || <quote B>"}`. If a check has more than 60 distinct flags (dedupe identical flags across documents with equal text by quote + message), adjudicate a sample of 30 drawn with `random.Random(0)` and report the sample size. Also mark each true flag `audit-relevant` when it falls on a line an audit or R1 blocking finding cites (C9.3 `cited`, within 3 lines).

**O4. Scores** (`score.py`, prints and writes `offline-results.md`): per check `MP`, flags per document group, `HIT(c, T)` for T1/T2/T3 on `final` and on `orig`, catalog-level recall if the catalog exists, `CLEAN(c)`, positive controls caught (seeded S1/S2/S3, deletion FR-5, regression), census summary; then G1, the live check set and ADOPT-TOOL per section 2. Expected honestly: `REF` and `COUNT` are near-pure syntax facts; `KV`, `PATH` are "possible" checks and may have low MP.

## 5. Part C: harness `$AB` (only if G1 holds; build it anyway so the coordinator can decide)

```bash
mkdir -p $AB/runs $AB/tests && cp $SP/p11/harness.py $SP/p11/advance.py $AB/
```

Edit only the copies. Keep byte-for-byte from p11: `S1`, `D`, `SPEC`, `FLAGS`, `AUD_OUT`, `WRAP`, `CMDPART`, `section()`, `git_show()`, the arm-3 `new_brief()` strings and the AUD brief.

1. Constants: `P13 = SP/"p13"; AB = P13/"ab2"; RUNS = AB/"runs"; REPO = str(P13/"clones/pn2")`; `BASE_REF`, `SPEC_SHA`, `AUD_CMD_SHA`, `AUD_RULES_SHA`, `TASKS_GLOB` (C0); `PRODUCT_REF`; `DESIGN = "l2"`; `LINT_CHECKS = "<comma list = the live check set from O4>"`; `arm_of()` returns 3.
2. `build()`: `l2-r1..l2-r6` exactly like p11 arm 3, with `command.md` from `PRODUCT_REF` (assert sha = `AUD_CMD_SHA`) and the rules file from `PRODUCT_REF`.
3. **Lint step (deterministic, by the harness):** before preparing R1, R2 and R3, run `uv run --project REPO superclaude review lint ws/<SPEC> --format md --checks LINT_CHECKS --out ws/.dev/orca-command-refactor/review/lint-<n>.md` and record the finding count and sha in `state["log"]["LINT<n>"]`.
4. **Briefs:** the arm-3 review briefs with one change: the values sentence ends `Values: candidate=<SPEC>, lint=.dev/orca-command-refactor/review/lint-<n>.md.` instead of `Values: candidate=<SPEC>.` (re-review: `..., prior=<prior>, lint=.dev/orca-command-refactor/review/lint-<n>.md.`). Revise and audit prompts unchanged (the audit is frozen, C9.2, and gets no lint).
5. Steps `R1, V1, R2, V2, R3, AUD, AUD2` with the p11 stop rules; `AUD` and `AUD2` per C9.2, launched together. All workers `sonnet`.
6. Tokens and done detection per C9.1 (dedupe by message id), launch ledger, `LAUNCH sonnet <path>` lines, at most `6 - running`, `--dry-run`, `MANUAL`/relaunch-once/`lost` handling, `harness.py basetokens`, `status`, `analyze` (writes `RESULTS.md`).

## 6. Part D: harness tests (`$AB/tests/test_ab2.py`)

(1) Prompt identity: `PROMPT-R1.md` equals `$SP/p11/runs/a3-r1/PROMPT-R1.md` after replacing the sandbox path and the values sentence; same for R2 and R3 (a3-r6), V1 (IDS `F1, F2`), AUD, AUD2. (2) `basetokens` reproduces arm-3 per-run loop totals within 1%: a3-r1 70,694; a3-r2 109,207; a3-r3 95,213; a3-r4 81,415; a3-r5 94,998; a3-r6 151,017 (skip without transcripts). (3) The lint step writes `lint-1.md` with the expected first line and only `LINT_CHECKS` ids. (4) Happy path with fakes (a3-r1 reports): R1 FAIL -> V1 -> LINT2 -> R2 PASS -> AUD and AUD2 together. (5) Concurrency: six fresh runs print 6 LAUNCH lines; `--dry-run` records nothing.

## 7. Part E: live phase and analysis

Workers: 6 runs x (R1, V1, R2, AUD, AUD2) = 30, plus 2 per extra round; at most 6 at once, about 6 waves. Tokens (C9.1 method): loop ~105,000 (baseline ~100,000 plus reading the lint file), AUD ~69,000, AUD2 ~69,000: about 0.25M per run, 1.5M in total.

`harness.py analyze` writes `$AB/RESULTS.md`: decision line; the section 2 table with baseline and test values; per-run table (reviews, verdicts, growth, loop and audit tokens, AUD/AUD2 blocking ids and themes, lint counts per round); how reviewers handled lint ids (confirmed / dismissed / ignored, counted by grepping `LINT-` ids in each review report); theme rates `THEME_T` versus `THEME_B`; R1 tokens versus baseline; validity notes (audit agreement, manual steps, lost runs). The decision is the rule table's output only.

## 8. Self-check before you start

- [ ] All corpus paths in O1 exist (`ls`), `truth.json` of p5 reads as described, and the two audits per a3 final exist.
- [ ] `sha256sum` of the overlay spec, `$SP/p11/rules.md` and the base spec-panel equal `SPEC_SHA`, `AUD_RULES_SHA`, `AUD_CMD_SHA`.
- [ ] No `superclaude review` command exists on the base (`uv run superclaude review --help` fails before your change).
- [ ] You will adjudicate flags yourself and record a quote for each verdict; you will not tune a check on the documents and then report its precision on the same flags without saying so (tuning after a first scoring pass is allowed once; report both passes).

## 9. Report formats

**READY report:**

```text
PN2 READY | branch 346Claude-pn2-mechanical-lint | PRODUCT_REF <sha> | pushed yes/no
Tests: tests/review <n> passed; pinned before/after <a>/<b>; lint, sync-dev, verify-sync ok
Corpus: <n> distinct documents (orig 1, final <n>, hist <n>, ref 3, pos 3, clean 2, other <n>)
Per check: MP | flags (final/orig/other) | HIT T1/T2/T3 | CLEAN | positive controls
  REF ... / COUNT ... / KV ... / PHASE ... / PATH ...
G1: PASS/FAIL; live check set: <list>; ADOPT-TOOL: <list>
Tuning passes: <1|2> (pass-1 numbers: ...)
Harness: $AB, tests <n> passed; launch: cd $AB && uv run --no-project python advance.py --dry-run
Contract deviations: <none | list>
```

**RESULTS.md** (`$AB/RESULTS.md`): `DECISION: ADOPT | DROP | INCONCLUSIVE | NOT RUN (G1 failed)` with the rule; offline table (copy of `offline-results.md`); live tables if run; validity notes; token method stated (C9.1).
