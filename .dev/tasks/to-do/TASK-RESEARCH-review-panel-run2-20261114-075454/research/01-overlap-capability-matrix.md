# Research: Overlap capability matrix across E1, E2 and E3
**Investigation type:** Architecture Analyst
**Scope:** E1 (reflect Tier 2 panel kernel, shadow mode, model-combination experiment), E2 (tasklist review-panel branch `origin/ironbelly/eval-tasklist-review-panel` @ 6c0984326cbb8fb06c4a36065de58b171d3f8175), E3 (#346 review loop and installed-only variants); code at HEAD 50d4d2b9d, branch ironbelly/shadow-runs
**Status:** Complete
**Date:** 2026-11-14
---

Legend. E1 = reflect Tier 2 panel kernel + shadow mode + model-combination experiment (merged as d2d8a2d16 / #519, plus evidence/docs commits on `ironbelly/shadow-runs`). E2 = tasklist review-panel study, collaboration designs and process-redesign brainstorms on `origin/ironbelly/eval-tasklist-review-panel` tip 6c0984326cbb8fb06c4a36065de58b171d3f8175. E3 = #346 review loop (`cli/review` v1 path, spec-panel Review Loop, prompts) plus the installed-only variants under `~/.claude`. Tags: [CODE-VERIFIED] read or executed by me this session; [CODE-CONTRADICTED]; [UNVERIFIED] (taken from a scope slice, not re-derived). `RV` = `src/superclaude/cli/review`. Matrix classifications are defined in section 3.

## 1. Open items (b), (c), (d1): resolved with commands run this session

### 1.1 Item (b): do the E2 commits after the hand-off change product code? [CODE-VERIFIED]
- `git diff --stat 4a22d74213f93837d00c2c314075dd967b9a98e3 6c0984326cbb8fb06c4a36065de58b171d3f8175 -- src tests` printed nothing (exit 0): from run-1 commit 4a22d7421 to the tip, zero `src/` and `tests/` files differ.
- `git diff --stat ec259f1b718ccdb9f08bba0237bfa47b2b7601a2 6c0984326cbb8fb06c4a36065de58b171d3f8175 -- src tests` also printed nothing (merge-base with master to tip): E2 never changed product code on its whole branch.
- Per commit (`git diff-tree --no-commit-id --name-only -r <c> -- src tests | wc -l`): c2ddeb1b4 = 0, fd69a006d = 0, d561461fa = 0, 6c0984326 = 0 files. `git log 4a22d74..6c09843 -- ':!.dev/tasks'` lists exactly these four commits (c2ddeb1b4 2026-11-13 16:17:36 UTC; fd69a006d 2026-11-13 20:25:07; d561461fa 2026-11-14 04:37:57; 6c0984326 2026-11-14 04:38:11).
- Verdict: scope slice 01 gap G6 CLOSED. All of E2 is evidence, harness scripts, design documents and out-of-tree prototype code under `.dev/eval-workspaces/`; it adds no product module. E2's contribution to a unified core is data, requirements and designs, not code to merge.

### 1.2 Item (c): does E2 `snap.py` write into E1's evidence tree? [CODE-VERIFIED]
- YES, as a write path. `git show 6c0984326:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/tools/tmp-scripts/snap.py` line 4: `open("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboD-r1/artifacts/input-snapshot.yaml","w").write(...)` (mode `"w"` overwrites). The target is inside E1's model-combination evidence tree.
- Evidence it ran: that file exists at HEAD with `input_tree_sha256: 17ff5b8a...c4e9`, two `file_list` entries and `file_count: 2` (read from the working tree). A read-only `uv run python` recomputation of the script's formula (`sha256(json.dumps(sorted([(name, sha), ...])))` with the two hashes printed in the file) gives the identical `17ff5b8a9589047325faa3eb2755996d61f4a54fe77a0336166ecbaf42cec4e9`. The file was committed by E1 commit 792cf8c52 (2026-11-13 15:11:22 UTC). That the E2 script, rather than another process, wrote it is an inference from format and hash identity [UNVERIFIED as to who ran it].
- Siblings in the same E2 folder that also point into this worktree: `drift-b3.py:2` (reads `.../shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`; read-only; hashes with `separators=(",",":")`, unlike `snap.py`'s default separators) and `rlog-r3.sh:3` (appends to `.../pre-TASK-WF-designSpec-20261107-075614-comboE-r3/audit.log`; a write path into E1's tree). `git grep` at the tip finds exactly these three files referencing `brainstorm-reflect-panel`, matching slice 01 C4.
- Consequence: E1 and E2 evidence trees were touched by each other's session tooling. The provenance of those E1 artifacts is not purely E1-session-generated; the owner decision to remove the three E2 files is still open (slice 02 H19).

### 1.3 Item (d1): which files do #519 and #518 change under `RV` and `tests/review`? [CODE-VERIFIED]
Commands: `git log -1 --format=... <c>`, `git diff-tree --no-commit-id --name-status -r <c> -- src/superclaude/cli/review` and `-- tests/review`.
- #519 = d2d8a2d166c945f556d921b31530a3673f00df89, 2026-11-12 14:47:10 -0500, "feat(reflect): Stage 0-2 of the Tier 2 review panel (measurement, dormant kernel, shadow mode) (#519)". Under `RV`: 17 files. Modified (4): `__init__.py`, `data/review-tiers.default.json`, `panel.py`, `panel_cmd.py`. Added (13): `card_convert.py`, `cluster.py`, `cluster_cmd.py`, `findings_v2.py`, `manifest.py`, `manifest_cmd.py`, `verify_cmd.py`, and six `data/review-panel.reflect-{enterprise,lite,post-x2,post,pre-x2,pre}.json`. Under `tests/review`: 22 files (21 added: 9 fixtures incl. `panel-golden-default-live7.json`, `panel-golden-packaged-tiers.json`, `review-tiers.frozen-1.0.0.json` and six `reflect_cards/*`; 12 new `test_*.py`; 1 modified `test_review_cli.py`).
- #518 = 167184c6ba449ab49b7f2af1dc9f4c9080006bd3, 2026-11-12 09:47:09 -0500, "feat(ccsession): apply the 2026-11-12 owner decisions for tiers (issue #488) (#518)". Under `RV`: 0 files. Under `tests/review`: 1 file, modified `tests/review/test_review_panel_live7.py`.
- Verdict: E2 run-2 and `HANDOFF-run1-vs-run2.md:22` attribute the `cli/review` changes to "#519 + #518". [CODE-CONTRADICTED] for #518: it changes no `RV` file and one test file; the `cli/review` change is #519 alone. File count check: 17 + 22 (#519) + 0 + 1 (#518) = 40, equal to the "40 files" E2 states (the +8,026 line figure is [UNVERIFIED] by me, reproduced by slice 01).

**Key Takeaways (section 1)**
- E2 changed no product code at any point; E2 = data, harness, designs. A unified core merges E1 and E3 code and imports E2 evidence and requirements.
- E2's `snap.py` and `rlog-r3.sh` are live write paths into E1's evidence tree; the E1 input snapshot for comboD-r1 was produced by the same formula (hash identical).
- `cli/review` changes come from #519 only; #518 is a ccsession tier change (one test file under `tests/review`).

## 2. Item (d2): E2's reflect contrast ("reflect has no panel/tier code") against the code at HEAD

What E2 actually wrote (read from `git show 6c0984326:.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md` lines 406-461): section 5.6 is headed "Contrast with reflect Tier 2 (from code-panel.md:143-163; not re-read here)", i.e. taken from the notes at branch base ec259f1b7 and not re-read. Its "Model selection" row says reflect uses `ANTHROPIC_DEFAULT_*_MODEL` aliases (skill) and `T2Model0N`/`T1Model0N` (CLI), against "tier JSON plus templates (a third registry)" for the panel; Q4 asks how reflect dispatches non-Claude models; Q9 asks which of the three registries wins. The literal words "reflect has no panel/tier code" are the task's paraphrase; E2's text says reflect selects models through a different registry and (Q1-Q3) does not yet know what master's #519 code does.

Re-derived at HEAD 50d4d2b9d:
1. [CODE-VERIFIED] The reflect Python package consumes no tier JSON and no panel code. `Grep` for `review-tiers|tiers.json|load_tiers|superclaude.cli.review|cli.review` over `src/superclaude` excluding `cli/review/**` returns exactly one hit: `src/superclaude/cli/main.py:568` (the `review_group` registration). `Grep` for `t2.engine|review panel|panel resolve|manifest advance|merged-verdict|review-panel|@reflect` in `src/superclaude/cli/reflect` hits only `panel_lint.py:5,11,271,297` (a read-only lint of `merged-verdict.yaml`) and two unrelated `commands.py` lines (82, 222: the `contract-status` and `run` command decorators). `Grep` for `T2Model0|T1Model0|ANTHROPIC_DEFAULT` in `cli/reflect` hits 16 times in `commands.py`, `ensemble.py`, `runner.py`, `models.py`. So E2's "model selection" row is still true for the code-driven path (`superclaude reflect run`), and Q9's "three registries" description still holds for code.
2. [CODE-VERIFIED] But the prompt layer does use the tier JSON at HEAD. `src/superclaude/skills/sc-reflect-protocol/SKILL.md:87` adds `--t2-engine legacy | shadow` (default `legacy`, `panel` rejected with "ships in Stage 3"); `:309-311` states with `legacy` "the panel code is never called"; `:338-349` define 10 shadow steps; step 1 (`:340`) runs `superclaude review panel resolve --template @reflect-pre --run-id <reflect run id> --kind first --env anthropic-only --hard-exclude-class <executor class> --strict-distinct`, then `superclaude review manifest init ...`; step 6 (`:345`) runs `superclaude review cluster` and `superclaude review verify-citations`; step 7 (`:346`) writes `adversarial/merged-verdict.yaml`; step 10 (`:349`) publishes. So at HEAD reflect's SKILL.md consumes the tier JSON registry, templates `@reflect-pre`/`@reflect-pre-x2` and the manifest, but only for UC-1 and only in `shadow` mode (measurement; "the legacy rotation and the Wave 4 debate stay authoritative", `:311`, `:338`). A `Grep` for `review (panel|manifest|cluster|verify-citations|merge|ledger)` over skills, commands, agents, rules and `scripts/*.py` finds 6 occurrences in `SKILL.md`, 1 in `document_review_loop_prompts.md`, and 2 in `sc-cli-eval-protocol` files; no other consumer.
3. [CODE-VERIFIED] Scope slices 01 and 02 said the reflect shadow engine "resolves its panel through the tier JSON (reported at SKILL.md:87 and :340-349)": correct for the SKILL.md prose; but slice 10's statement that `cli/reflect/*.py` contain no shadow logic is also correct (point 1). The two statements are compatible: the shadow engine is prose plus `superclaude review ...` CLI calls, not Python in `cli/reflect/`.
4. Verdict on the contested claim: E2's contrast is [CODE-CONTRADICTED] if read as "reflect has no panel/tier code" (the kernel in `cli/review` was built for reflect: six `review-panel.reflect-*.json` templates, `validate_reflect_profile` at `panel.py:80`, `findings_v2.py` lenses `reflect-pre`/`reflect-post`, `card_convert.py`, `manifest.py`) and [CODE-VERIFIED] if read as "the code-driven reflect gate (`superclaude reflect run`: runner, ensemble, contract) has no panel/tier code" (point 1). Q4 is partly answered: the prompt-layer shadow path can only dispatch Claude classes (reflect profile accepts `launch` values sonnet/opus/haiku only, `panel.py:72,153-155`; gateway has `"launch": {}`, `review-tiers.default.json:29`), so non-Claude dispatch does not exist in the product shadow path; the code-driven ensemble dispatches external models via `T2Model0N` (slice 10 S6.2, [UNVERIFIED] by me beyond the grep count).
5. Relevant to the matrix: E1 contains TWO Tier 2 execution paths that share nothing: (a) prompt path (SKILL.md Wave 3-5 with legacy rotation and optional shadow panel) and (b) code path (`ReflectRunner` -> `run_tier2_ensemble` -> `contract.derive_verdict`). The panel kernel is wired only to (a); `scripts/reflect_shadow_exit.py` (imports `superclaude.cli.review.manifest` and `panel`, slice 09 A) measures (a). `panel_lint.py` L1/L2 would fail a contract emitted by (b) (it carries `contract_version: 1.0`, slice 10 S6.2 probe, [UNVERIFIED] by me).

**Key Takeaways (section 2)**
- Item (d2) resolved: `cli/reflect` has no panel code; SKILL.md has the shadow engine; the kernel in `cli/review` is reflect-shaped. E2's row is right about the code path, wrong about the product as a whole.
- Panel code is not wired to the code-driven reflect gate; unification must decide which of E1's two paths the shared core serves.

## 3. Code probes I executed this session (read-only; `PYTHONDONTWRITEBYTECODE=1 uv run python`, no files written)
| # | Probe | Result | Meaning |
|---|---|---|---|
| P-a | `findings.annotate()` on a citations-only finding (no `anchor`) | `KeyError: 'anchor'` (`findings.py:349` `locate(text, finding["anchor"])`) | a findings-v2 citation-only finding cannot enter the v1 ledger path (`ledger.merge_round` calls `fnd.annotate` at `ledger.py:136`) |
| P-b | `findings_v2.check_finding` vs `findings._check_finding` on a line carrying `calibrated_confidence` | v2: "calibrated_confidence is not allowed in a findings-v2 line"; v1: `None` (accepted) | schema conflict: a line valid in v1 can be invalid in v2 |
| P-c | `check_finding` with anchor 201 chars, claim 301 chars, citation quote 201 chars | all three rejected ("at most 200/300/200 characters") | the whole-finding drop limits exist in v2 as in v1 (D1 limit inherited) |
| P-d | `findings.refs_norm({'anchor':'Task T01.02 does x','claim':'T01.02 bad','refs':['T01.02','AC-0.4','1.2']})` | `['1.2', 'AC-0.4']` (T01.02 lost) | tasklist task ids are not refs; `cluster.py:64,141` imports and uses `refs_norm`, so E1's v2 clustering inherits the gap |
| P-e | sha256 of `json.dumps(sorted([(name, sha), ...]))` using `snap.py`'s two hashes | `17ff5b8a9589047325faa3eb2755996d61f4a54fe77a0336166ecbaf42cec4e9` = value in E1's `input-snapshot.yaml` | see 1.2 |

**Anchor verification (known anchors from the assignment)**
- `findings.py:29` `_REF_TOKEN = re.compile(r"\b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b")` [CODE-VERIFIED]: letters-hyphen-digits or `P<digit>` only.
- `findings_v2.py:15-22` imports `_HEAD_FINDINGS, _ID, CATEGORIES, SEVERITIES, _blocks_after, _check_flat` from `findings.py` [CODE-VERIFIED]. The slice phrase "200/300-character limits inherited through `_check_flat`" is imprecise: the length MECHANISM (`_check_flat`: flatten whitespace, then compare) is inherited; the numbers are restated as literals in `findings_v2.py`: citation quote `12, 200` at `:80`; claim `None, 300` at `:111`; anchor `12, 200` at `:126` (no citations) and `:132` (with citations); anchor2 `12, 200` at `:136`; refs at most 8 at `:117`; citations 1..8 at `:128`. Probe P-c confirms behaviour. Same numbers as v1 (`findings.py:104,108,118`, refs at `:114`).

**Key Takeaways (section 3)**
- The two finding grammars cannot flow through each other's downstream code: v2 citation-only findings crash v1 `annotate` (P-a); v1 anchor-only findings can be parsed by v2 `parse_block` (anchor OR citations accepted, `findings_v2.py:122-125`) but get no primary citation, hence `fp = None` and no cluster by path in `cluster.annotate` (`cluster.py:133-147`), so they only ever form singleton clusters.
- The 200/300-character whole-finding drop is present in both parsers; the `T01.02` gap is present in both clustering paths.

## 4. The matrix (item a)

### 4.1 Classification rules (applied per cell, against the other two programs)
- **identical**: the cell has the same mechanism or the same code as another program's cell (the other program is named). Shared code counts as identical.
- **superset**: the cell does everything the named comparator cell does and adds at least one more capability (the addition is named).
- **conflicting**: the cell does the same job in an incompatible way (different vocabulary, schema, rule or semantics) so both cannot be a shared-core default without a decision (the conflict is named and listed in section 5).
- **unique**: no other program has this mechanism; no incompatibility with the others is implied.
- **absent**: the program has no mechanism for this capability (negative evidence given). This is a fifth label added by me because an absent cell cannot be identical, superset, conflicting or unique; it is recorded so every cell still carries a classification.
- E3 is split: E3s = shipped source (`src/superclaude/cli/review` v1 path, `spec-panel.md` Review Loop, loop prompts); E3i = installed-only variants (`~/.claude/skills/sc-review-ledger`, `sc-spec-panel-stoprule-protocol`, `sc-diffgate`, `sc-fix-audit`, `agents/finding-grader.md`, five `commands/sc/spec-panel-*.md`).
- Tags: [CV] = I read or executed it this session at the cited place; [UV] = taken from a scope slice or another document and not re-derived by me (the slice and section are named); every figure, commit id and line number I did not re-derive is [UV].

### 4.2 Summary grid (one cell = classification; detail and evidence in 4.3)
| # | Capability | E1 | E2 | E3s | E3i |
|---|---|---|---|---|---|
| 1 | Finding schema | superset of E3s | identical to E3s (+ design-only extras) | identical to E2 / subset of E1 | conflicting (three more grammars) |
| 2 | Ids, identity, hash | conflicting (v2 fp) | unique (observed-model check) | identical to E1 (id regex) / conflicting (fp) | conflicting (`R<N>.<j>`, int schema) |
| 3 | Merge and dedupe | unique (LLM debate, clustering is telemetry-only) | identical to E3s (uses it unchanged) | unique (deterministic union + ledger) | conflicting (sealed claim, computed surface) |
| 4 | Clustering | superset of E3s (shares `refs_norm` gap) | absent (data only) | unique-base (v1 union-find) | absent |
| 5 | Citation verification | unique (file:line precheck) | absent (measured only) | unique (document-anchor locate) | superset of E3s (script-read-back evidence) [UV] |
| 6 | Verdict | conflicting (convergence thresholds, degrade map) | absent (judge scoring is evaluation) | unique (any blocking row fails) | conflicting (script-computed) |
| 7 | Ledger and rounds | absent in `cli/review` for the finding ledger and rounds (manifest is a run state machine); the reflect code wrapper has a `--fix` loop that is dormant, see s4.3 row 7 and research/06 s4.2 | absent (designs only) | unique (`review-ledger/1`, cap 3) | conflicting (second ledger, second statuses) |
| 8 | Panel, tier, profile | superset of E3s (same engine + reflect profile) | conflicting (hard-coded ladder, own panels) | identical engine, subset of E1 | absent |
| 9 | Dispatch | conflicting inside E1 (prompt path vs code path) | unique (raw `claude -p`, bypasses tiers) | absent in code (prompt text only) | absent |
| 10 | Brief | conflicting (three-section brief, v2 line) | identical to E3s (wrapper) + unique phase-2 frames | unique (`document_review_loop_prompts.md`) | conflicting (per-variant briefs) |
| 11 | Calibration | unique (blind calibrator, per-finding) | absent | absent | unique-adjacent (blind finding-grader) |
| 12 | Telemetry, manifest, run record | unique (manifest + contract telemetry + shadow exit) | conflicting (meta/cost/score files) | unique (`review-telemetry/1`, no producer) | unique (per-variant state files) |
| 13 | Memory | unique (per-project expiring files) | absent | absent | absent |
| 14 | Eval harness | unique (shadow-exit, 5x3 combos) | unique + superset on ground truth (GT, blind judge) | absent in src (tests only) | unique (#346 phase-5 bundle, archived) |
| 15 | Collaboration | absent (independent reviewers + legacy debate) | unique (r1-r5 designs, brainstorms) | absent | unique-adjacent (reviser/disputes) |

### 4.3 Detail per capability (each row: cell content, class, tag, citation)

#### 1. Finding schema
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | findings-v2: v1 fields plus `citations` (role, path, line_start, line_end, optional quote), `lens`, `channel`, `deviation_class`, `reflect_category`, `coverage_rows`, `self_confidence`; no `prior` lines; rejects `calibrated_confidence`; anchor OR citations required | superset of E3s line grammar (adds 7 fields), with conflicts C-1 (`calibrated_confidence`, `prior`) and C-2 (blocking rule) | [CV] | `findings_v2.py:24-48, 84-187`; probe P-b; no `prior` handling: slice 09 D1 [UV] |
| E2 | No schema in product code. Study and designs use findings-v1 unchanged, and rely on unknown-key acceptance for extra keys `class`, `probe`, `src` (`merged-requirements.md` section 3.0.6 near lines 322-323) and for `origin: own|peer` (r3 design); redesigns 1/2 add a separate `ledger-v1` fence (own info string) so the single-`findings-v1`-block rule is not broken | identical to E3s (shipped part); unique for `ledger-v1` and `origin` (design only) | [CV] for acceptance of unknown keys (`findings.py:90-121` has no key whitelist; v2 `check_finding` rejects only `calibrated_confidence`); [UV] for the E2 design text beyond the sampled lines | `git show 6c0984326:.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md` lines 149, 270, 295, 322-323 (printed above) |
| E3s | findings-v1: `SEVERITIES`, 6 `CATEGORIES`, `PRIOR_STATUSES`, `ACTIONS`; id regex; anchor 12..200, anchor2, refs <= 8, claim <= 300; `prior` lines; fixmap-v1 | identical to E2; subset of E1 | [CV] | `findings.py:14-31, 90-121`; prompts lines 56-66 (read) |
| E3i | ledger: row/claim records with anchor-occurs-once; stoprule: `claim` kind (claimed severity, `quote` 20-300 unique, `span`, `outcome` >= 8 words, `evidence`); diffgate: line grammar `PRIOR`/`FINDING`/`FINDINGS none` with `at=`, `hunk=`, `via=`, `fr=`; none uses `findings-v1` | conflicting with E3s and E1 (three further incompatible grammars; `finding-grader` replies JSON lines) | [UV] slice 12 section C1-C4 | variant scripts exist (sizes re-measured [CV]: 2668, 2050, 1740, 1131 lines); grammar details not re-read |

#### 2. Ids, identity and hash
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | finding id regex reused (`_ID`); v2 fingerprint `sha256("v2|role|path||refs|class")` (full hex, section always empty); cluster ids `C<i>`; manifest freezes template, tiers, brief-template, schema ids and input-tree hashes; card header `model:` pinned from `resolution.json`, `model_observed:` extra line; `identity_source` observed vs `requested-pinned` (prompt-level) | identical to E3s for ids; conflicting with E3s for fingerprint (v1 is `sha256("v1|section|refs")[:16]`) | [CV] | `findings_v2.py:99-100`; `cluster.py:119-123`; `findings.py:340-343`; `SKILL.md:341, 348` (read); manifest functions `manifest.py:97, 111` (def lines) |
| E2 | Harness checks the SERVED model: `OBS` = unique `.message.model` of top-level assistant messages; `MODEL_OK` when it equals the requested model (or `-build` suffix); every attempt writes `meta.json` with expected/observed model; known bug H2: `expected_model` is overwritten with the fallback model after a ladder step | unique (mechanical served-model audit); not wired into product | [CV] | `run-reviewer.sh:51-58, 76` |
| E3s | `review-ledger/1` row ids `L<k>`; reviewer `model` copied from resolution only (`ledger.py:144`); spec-panel header records candidate/baseline SHA-256 and "the reviewer model actually used" (`spec-panel.md:258`, prompt-level); telemetry has `model_observed` with no producer (`telemetry.py:49`; sole `append_record` caller is the manual CLI, `telemetry_cmd.py:67`) | identical to E1 (id regex); conflicting (fp) | [CV] | files cited |
| E3i | diffgate ids `R<N>.<j>`; ledger `SCHEMA = 1` (integer) and `body_sha256` tamper check; stoprule seal hash and hash chain | conflicting (second id and schema space) | `SCHEMA = 1` [CV] (`review_ledger.py:34`); rest [UV] slice 12 | |

#### 3. Merge and dedupe
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | Shadow: the merge is the LEGACY `sc-adversarial` Mode A debate; the panel's `cluster` and `verify-citations` are telemetry/flagging only ("Neither drops anything and neither feeds the debate"); `merged-verdict.yaml` is copied from the debate output | unique (LLM debate merge; no deterministic merge in shadow) | [CV] | `SKILL.md:338, 345-346` |
| E2 | Runs `superclaude review merge` unchanged in every study row; audit-D measured its drops (92 dropped findings, 49 blocking; luna 30, ember 33, ...) | identical to E3s (same code) | merge usage [UV] (slice 02/03); drop counts [UV] (audit-D via slice 01 C15) | |
| E3s | `merge_round`: parse each report (v1), keep parsable findings of invalid blocks, refuse only when NO reviewer block is valid, cluster all findings (union-find), match each cluster to the FIRST existing row (`break`), new row keeps first member's anchor/claim/category, `blocking = any`, severity max | unique (deterministic union with status ledger) | [CV] for `merge_round` (def at `ledger.py:107`, parse/refuse lines read at 127-157) and cluster function (`findings.py:382-407`); first-row `break` [UV] slice 01 D10 | |
| E3i | ledger `find/answer/verify/close/sweep`; stoprule `seal/grade-prep/apply-grades/finalize`; diffgate `begin/check/fixcheck` | conflicting with E3s (different merge unit and different owner of the verdict) | [UV] slice 12 | |

#### 4. Clustering
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | `cluster_v2`/`same_defect_v2`: citation role/path/line ranges with `SPAN_TOLERANCE = 3`, deviation-class compatibility, `refs_norm` from v1, `chained` flag, reviewer support weights, `disputed`, `cluster_agreement`; only RESOLVED citations (path in snapshot list) can match by span; anchor-only findings never cluster | superset of E3s (adds path/role, chain detection, agreement); identical to E3s in sharing `refs_norm` and its `T01.02` gap | [CV] | `cluster.py:64-72, 119-181`; `chained` at `cluster.py:324, 370`; probe P-d |
| E2 | none in code; evidence: 83 mega-clusters and 195 of 1,398 rows chained (audit-D) | absent | [UV] slice 01 section 3.5 | |
| E3s | `same_defect` (fp equal + refs, or refs intersect/both empty + spans within 3 lines, 3 inline at `findings.py:377`) and union-find `cluster` with no chain guard, no reviewer filter | unique-base (E1 clone is the successor) | [CV] | `findings.py:367-407` |
| E3i | no clustering (ledger row identity by anchor; diffgate by `at=`/`hunk=`) | absent | [UV] | |

#### 5. Citation and anchor verification
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | `verify-citations`: `review-precheck/1` with flags missing-file, out-of-range, quote-not-found (advisory), `reread_set`, never drops; citation path rules (repo-relative, no `..`); plus legacy Wave-5 evidence-validator that does drop | unique (file:line precheck for code/plan targets) | schema id [CV] (`verify_cmd.py:25`); path rules [CV] (`findings_v2.py:59-81`); flags [UV] slice 09 D4 | |
| E2 | measured anchor fidelity (R16, 91.4%) and found anchors missing in 46 rows / 13 blocking (audit-D); no verifier | absent (measurement only) | [UV] slice 01 section 3.5 and R16 | |
| E3s | `locate` whitespace-flattened exact substring, `annotate` takes the FIRST occurrence; a missing anchor keeps the finding with `span None`, `section "none"`; `anchor_status`/`anchor_ambiguous` are computed and read by nothing | unique (document-anchor locate); conflicting with E1's location type (quoted text vs file:line) | [CV] for `annotate` (`findings.py:346-360`); "read by nothing" [UV] slice 01 D6 | |
| E3i | ledger anchor must occur exactly once in the round snapshot; stoprule evidence `verified` = script read-back vs `unverified` reviewer assertion | superset of E3s (uniqueness and script read-back) | [UV] slice 12 C1-C2 | |

#### 6. Verdict
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | Prompt path: convergence routing >=0.75 PASS, >=0.60 PARTIAL, <0.60 FAIL (`SKILL.md:703`); code path: `contract.derive_verdict`, a 4-way blocked/degraded/halted/pass map that degrades a present Tier-2 score below 0.80 (`contract.py:310, 321`); shadow mode changes no verdict. Panel `cluster_agreement` is recorded, "never compared with the convergence thresholds" (`SKILL.md:345`) | conflicting with E3s (convergence score and degrade map vs "any open blocking row fails"); internal conflict 0.75 vs 0.80 (C-6) | [CV] | lines cited |
| E2 | no product verdict; the study's blind Opus judge scores ground-truth coverage (evaluation); requirement U-list names a verdict rule as an open decision | absent | [UV] slice 03 section 3 | |
| E3s | `FAIL` iff any row is `blocking` and status open/regressed (`_brief_ids` `ledger.py:99-104`); decision PASS / REVISE if `n < cap` / ESCALATE (`ledger.py:93-96`); `verdict:` last line of the report (`spec-panel.md:260`); exit codes 0/10/11 (`ledger_cmd.py:13`, `:109`, [CV]) | unique (consequence-graded boolean) | [CV] | |
| E3i | verdict computed by script from a sealed claim ledger (stoprule `finalize`), diffgate `check`, ledger `close`; reviewer forbidden to type it in stoprule | conflicting with E3s (who owns the verdict) | [UV] slice 12 C1-C3 | |

#### 7. Ledger and rounds
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | No finding ledger, no rounds, no reviser: new `cli/review` modules contain no `verdict`/`ledger`/`round` code (my Grep hits only `CHANNELS` text "grounding-gap"); the `cli/review` kernel has no ledger, rounds or reviser; the code wrapper `superclaude reflect run --fix` has a bounded audit/classify/apply/re-verify loop (`src/superclaude/cli/reflect/runner.py:748-793`: `while True:`, `if not config.fix: break`, `classify_fix(...) != "auto-fixable"`, `_apply_remediation(...)`, `iteration > max_iters`; `--remediate` built into the prompt under `config.fix` at `runner.py:474-478`) that is structurally dormant because engine A emits no `remediation_*` pointer (research/06 s4.2) [CODE-VERIFIED, fix cycle 1: re-read `runner.py:474-478, 748-793`; the earlier text "reflect has no fix loop" is [CODE-CONTRADICTED]]. Per-RUN state machine instead: manifest states frozen -> published | absent for ledger; manifest is unique | [CV] | Grep of `cluster.py, cluster_cmd.py, manifest.py, manifest_cmd.py, verify_cmd.py, findings_v2.py, card_convert.py`; `manifest.py:38-54` |
| E2 | no ledger in product; designs `ledger-v1` = enumeration rows, "NOT a status ledger"; audit found 13 merge/ledger defects D1-D13 | absent | [UV] slice 06 section 22; slice 01 section 4.1 (most re-derived there at HEAD) | |
| E3s | `review-ledger/1`, statuses open/resolved_check/resolved/regressed/deferred (`ledger.py:17-19`), cap 3 at `new_ledger` (`:37-38`), revise (`:301`), defer (`:350`), verdict (`:363`), capture (`:375`) | unique | [CV] | |
| E3i | `review_ledger.py` `SCHEMA = 1`, `CAP_REVIEWS = 3` (`:34-35`), statuses open/fixed/verified/reopened/deferred, phases find/revise/verify/terminal/swept, sweep after every loop; stoprule and diffgate keep their own ledgers | conflicting: second ledger with a different name for the same schema field and different statuses; same cap constant 3 (identical) | `SCHEMA`, `CAP_REVIEWS` [CV]; statuses [UV] slice 12 B15 | |

#### 8. Panel, tier, profile
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | Same engine as E3s plus: `classes` map, `validate_reflect_profile` (`panel.py:80`), `_check_reflect_resolution` (`:137`), `_REFLECT_LAUNCH` sonnet/opus/haiku (`:72`), `hard_exclude`/`strict_distinct` in `resolve_slot` (`:500`), six `reflect-*` templates, total reviewers <= 3 | superset of E3s | [CV] for def lines and `_REFLECT_LAUNCH`; limits [UV] slice 09 C1 | |
| E2 | no product code; own panels EL2/SL2/HL2 in r3 `config/panels.json`; default `EXCLUDE_MODELS="glm-5.3 Qwen3.8-max"` and a cross-tier ladder in the script, while `review-tiers.default.json` still lists both models in tier2/tier2b/tier3 (lines 7-9) and has no `muse-ember` | conflicting (exclusion and fallback live in a script, not in data) | [CV] | `run-reviewer.sh:23-43, 69`; tiers file read |
| E3s | tier file with six aliases, environments `gateway` (`launch: {}`) and `anthropic-only` (stand-in haiku for tiers 2, 2b, 3, 4); templates `@default` (4 reviewers) and `@live7` (7); `distinct_across_slots` silently re-admits duplicates when exclusion empties the pool unless `hard_exclude`/`strict_distinct` is passed | identical engine to E1 (same file); subset of E1 | [CV] for tiers file; `distinct_across_slots` re-admit [UV] slice 01 P1 (executed there) | `review-tiers.default.json:5-10, 24-37` |
| E3i | none (variants use fixed profiles in their scripts: `PROFILES["spec-panel"]`; reviewers from the command text) | absent | [UV] slice 12 | |

#### 9. Dispatch
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | Two paths: (a) prompt path: shadow dispatch "is the legacy dispatch" via Agent calls to `reflect-reviewer` (frontmatter `model: sonnet`), model pins copied from `resolution.json`; the reflect profile refuses any resolution whose `launch` is not sonnet/opus/haiku, so `--env gateway` is refused; (b) code path: swarm ensemble binds each worker to `T2Model0N` external models | conflicting inside E1 (two dispatch mechanisms, one registry each) | (a) [CV] `SKILL.md:342`, `panel.py:72, 153-155`, tiers `:29`; `reflect-reviewer.md` model [UV] slice 10; (b) [UV] slice 10 S6.2 | |
| E2 | `claude -p --model <raw gateway id> --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit` in `/tmp/evalsb/repo` with a 3000 s timeout, 2 attempts per model then a ladder; "tier aliases serve only the first model of a tier, so they are NOT used"; r3 design resumes the session for phase 2 | unique (non-Claude dispatch that works today); conflicts with E1 shadow (Claude classes only) and with tier resolution | script [CV] `run-reviewer.sh:45-83`; alias statement [UV] slice 03 section 2 (manifest.md:11) | |
| E3s | product code does not dispatch; loop prompts tell the coordinator to run the reviewers `panel resolve` prints, each in a fresh context, then `review merge` (`document_review_loop_prompts.md:68-70`); the resolution carries a `launch` value per reviewer (null for gateway) | absent in code | [CV] | |
| E3i | variants are driven by the command text and coordinator steps; none dispatches in code | absent | [UV] | |

#### 10. Brief
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | `refs/reviewer-spec.md`: exactly three sections `## T1 card excerpt`, `## Grounding hunks`, `## Coverage slice`; in shadow one findings-block instruction line is appended inside the first; reflect-reviewer's declared output is a deviation table, not a findings block | conflicting with E3s (E3's brief ends with `## Findings block` as LAST section, `findings-v1`; E1 asks `findings-v2` inside the card excerpt) | line `SKILL.md:342` [CV]; reviewer-spec and agent output shape [UV] slice 10 S9.1/S9.3 | |
| E2 | the E3 loop brief wrapped in `/sc:spec-panel @<candidate> --mode critique` (`run-reviewer.sh:13-17`): names the candidate and its hash, not the source document ("against the requirements it states"); designs add phase-2 frames, reask frames, flag cards | identical to E3s; unique for collaboration frames (design only) | [CV] for the wrapper; frames [UV] slice 08 | |
| E3s | `document_review_loop_prompts.md` (74 lines): roles CANDIDATE/BASELINE/PRIOR, grading check sentence, findings block rule, fix map, review panel paragraph; hard gate in `spec-panel.md:266-268` | unique | [CV] | |
| E3i | per-variant commands (`spec-panel-ledger|stoprule|diffgate|ponytail|armb.md`), all built on the pre-#478/#479 base; none contains `follow-up candidates` or the hard-gate section | conflicting (stale fork of the loop contract) | [UV] slice 12 C8 | |

#### 11. Calibration
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | `confidence-calibrator` blind per card (agent `model: sonnet`, tools Read), rubric mismatch between the agent (6 dimensions) and reflect (5 dimensions); per-finding confidences requested by one appended brief line; reviewers may not self-supply `calibrated_confidence`; cluster support weights use best calibrated confidence | unique | brief line `SKILL.md:344` and `findings_v2.py:96-97` [CV]; agent and rubric details [UV] slice 10 S9.2 | |
| E2 | none; E2 study finding "no calibrator in this panel"; calibrator is an open decision (DO3) | absent | [UV] slice 01 section 3.7 | |
| E3s | none: `_confidence` single/overlap counts reviewers, never used for the verdict (`ledger.py:86-90, 99-104`) | absent | [CV] | |
| E3i | stoprule's blind `finding-grader` (model sonnet, tool Read, maxTurns 10) decides only whether a claim is blocking under rubric B1-B3 | unique-adjacent (blind second opinion, but decides blocking, not confidence) | file existence and line count [CV] (35 lines); settings [UV] slice 12 A7 | |

#### 12. Telemetry, manifest and run record
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | `review-panel-manifest/1` (9 states + `failed`, idempotent stage advance, per-attempt records, resume, publish refusal in `shadow`), contract `telemetry:` block, `panel_lint.py`, `scripts/reflect_shadow_exit.py` (Stage 2 gate, exit 0/1/3), `results.jsonl` | unique | schema and function def lines [CV]; contract block and exit script [UV] slice 10 S5/S10 | `manifest.py:38-54, 277, 331, 422, 476` |
| E2 | per-attempt `meta.json` (expected/observed model, tokens, wall), `cost.json`, `score.json`, free-text `manifest.md`; designs add `results.jsonl` rows and `pins.json` sha pins | conflicting (different schema and fields; no shared id) | `run-reviewer.sh:58, 85-87` [CV]; designs [UV] | |
| E3s | `review-telemetry/1` JSONL + SQLite (`SCHEMA_VERSION = "review-telemetry/1"` `telemetry.py:17`, strata hard-coded `sonnet`/`haiku` at `:112`, fields incl. `model.observed` at `:49`), `review-capture/1`; only caller of `append_record` is the manual CLI | unique; conflicting with E1 manifest (two run-record formats) | [CV] | |
| E3i | per-variant state (`ledger.json`, `state.json`, `ledger.json` in `--dir`), hash chains | unique | [UV] | |

#### 13. Memory
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | per-project expiring memory under `<project>/.superclaude/memory/reflect/` (hydrate at Wave 0, handoff files for Tier 3); shadow runs append to `docs/memory/reflect/deviation-patterns-*.md` (contamination channel) | unique | [CV] for `SKILL.md:140-147, 376, 585-590` (grep lines); contamination [UV] slice 11 section 2.6 | |
| E2 | none in product; hand-off notes are documents | absent | [UV] | |
| E3s | none: Grep for `memory` in `cli/review/*.py`, `spec-panel.md` and the loop prompts finds no memory mechanism (one unrelated word in prompts line 44) | absent | [CV] | |
| E3i | none (state files are per loop) | absent | [UV] | |

#### 14. Eval harness
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | `.dev/eval-workspaces/shadow-model-combos/` (5 combos x 3 runs = 15, PLAN/combos/results/FINDINGS, extract.py), `scripts/reflect_shadow_exit.py`, `reflect_stage0a_replay.py`, `reflect_verdict_replay.py`, `tests/cli/reflect` (352 passed in slice 10); no ground-truth scoring was done; the input package is E2's `TASK-WF-designSpec-20261107-075614` | unique; shares E2's input fixture (identical tasklist sha 044809e3...) | sha in `snap.py:2` [CV]; the rest [UV] slice 10/11 | |
| E2 | 3 packages with ground truth (10, 4, 2 defects), blind Opus judge per package/label, arms A/B/C pilot, ~96 combo row folders, 6 audits, 665 valid-era runs, `run-reviewer.sh`, 5 collaboration harness packages with their own tests (py file counts: r1 27, r2 28, r3 31, r4 17, r5 14 [CV via `git ls-tree`]) | unique; superset of E1 on scoring (ground truth + blind judge exist only here) | `git ls-tree` at the tip: 96 directories directly under `combos/` and 19 `RESULT.md` files [CV] (slice 03's "95 combo row dirs + SPEC.md" is off by one against this count; slice 01's 96 is right); py counts [CV]; study figures [UV] slice 01/03 | |
| E3s | tests only: `tests/review` (19 modules at HEAD) and 4 skill tests; presence/wording tests of the loop, not behaviour of a consumer | absent as a harness | [UV] slice 09 A / slice 12 A9 | |
| E3i | #346 phase-5 bundle: arms control/exact-427/flagged/variants, FINAL-REPORT (no completed loop reached a clean PASS), 7,909 lines of variant tests archived under `.dev/experiments/346-validation/phase5/final-bundle/builds/` | unique | [UV] slice 12 A9, D1 | |

#### 15. Collaboration
| Program | Content | Class | Tag | Evidence |
|---|---|---|---|---|
| E1 | none among reviewers (independent, heterogeneous; sc-adversarial debate only at merge); recorded overlap is sparse (7 unchained multi-reviewer clusters of 216 in the 15 combo runs, 3.2%) | absent | [UV] slice 11 section 2.6 | |
| E2 | five parallel-collaboration redesigns (F1 axis-flip challenge, F3 move radar, F4 idle-shift sweeper, F6 coverage deflection, F7 flag-and-adjudicate) with `PANEL_COLLAB=0/1` switch and frozen pins; two process redesigns (Sweep Sheet, Recipe Ledger) as requirements with 46 REQs; no collaboration arm ever produced a measured result in the sampled slices | unique | package dirs [CV] (`git ls-tree` at tip); design facts and "nothing was run" [UV] slices 05, 06, 08 | |
| E3s | none; sequential reviewer -> reviser -> re-reviewer loop (Reviser brief, fixmap) | unique-adjacent (sequential hand-off, not peer exchange) | [CV] `spec-panel.md:263`; prompts line 64-66 | |
| E3i | ledger `answer` (reviser disputes), stoprule grader loop | unique-adjacent | [UV] slice 12 | |

**Key Takeaways (section 4)**
- Identical cells are few and are all at the E3s/E2 and E3s/E1 seam: the id regex, finding-v1 grammar, the cap constant 3, and E2's use of E3's merge unchanged. These are the shared core.
- E1 is a strict superset of E3s for panel resolution and for the line grammar, but conflicts with it on the finding location type (file:line citations vs quoted text anchors), the blocking rule when `reflect_category` is set, the fingerprint, the verdict model and the run record. Those are the decisions the unified design must take (section 5).
- E3i (installed-only) is a second, incompatible implementation of the whole loop (ledger, grammar, verdict) that shares no code with `cli/review` (stdlib-only; confirmed below) and is not installable by `superclaude install`.
- E2 is the only source of ground truth, of the non-Claude dispatch that works, and of collaboration designs; it contributes zero product code.

## 5. Conflict register (every cell classified "conflicting" above, with evidence)
| ID | Conflict | Side A | Side B | Evidence | Tag |
|---|---|---|---|---|---|
| C-1 | Line grammar versions | E3s v1 accepts unknown keys incl. `calibrated_confidence`; carries `prior` lines needed by the re-review loop | E1 v2 rejects `calibrated_confidence` and rejects `prior` lines (module docstring `findings_v2.py:3-5`) | probe P-b; `findings_v2.py:96-97` | [CV] |
| C-2 | Blocking rule | E3: MAJOR/FR-8/FR-9 blocking only with a concrete wrong outcome (`spec-panel.md:259`); schema allows MAJOR non-blocking | E1 v2 with `reflect_category` set forces `blocking == (severity != MINOR)` (`findings_v2.py:161-162`) | both read | [CV] |
| C-3 | Location type | E3: quoted text `anchor` (12..200 chars) located in the document; `annotate` needs `anchor` | E1: file:line `citations` checked against a snapshot list; anchor optional | probe P-a; `cluster.py:133-147` | [CV] |
| C-4 | Fingerprint | v1 `sha256("v1|section|refs")[:16]` | v2 `sha256("v2|role|path||refs|class")` full hex, section empty | `findings.py:340-343`; `cluster.py:119-123` | [CV] |
| C-5 | Two ledgers | `review-ledger/1`, statuses open/resolved_check/resolved/regressed/deferred | installed `review_ledger.py` `SCHEMA = 1`, statuses open/fixed/verified/reopened/deferred | `ledger.py:17-19`; `review_ledger.py:34-35`; statuses [UV] slice 12 B15 | [CV] / [UV] |
| C-6 | Convergence threshold | SKILL.md routes >=0.75 PASS | `contract.py` degrades a present Tier-2 score below 0.80 | `SKILL.md:703`; `contract.py:310, 321` | [CV] |
| C-7 | Exclusion and fallback location | E2 script: `EXCLUDE_MODELS="glm-5.3 Qwen3.8-max"` and a cross-tier ladder | product: tier lists still contain both models; exclusion only via `--hard-exclude-class` flags that the default path does not pass; stand-ins only for `anthropic-only` | `run-reviewer.sh:23-43, 69`; `review-tiers.default.json:7-9, 34`; `panel_cmd.py:54, 60` | [CV] |
| C-8 | Dispatch | E2: raw model ids via `claude -p` | E1 shadow: Claude classes only (`launch` sonnet/opus/haiku); gateway `launch: {}` | `run-reviewer.sh:48`; `panel.py:72, 153-155`; tiers `:29` | [CV] |
| C-9 | Report ending and brief shape | E3: `## Findings block` last section, `findings-v1`; spec-panel Reviser brief above the final `verdict:` line | E1: `findings-v2` appended inside `## T1 card excerpt`; reviewer agent emits a deviation table | `document_review_loop_prompts.md:58`; `spec-panel.md:260, 263`; `SKILL.md:342` | [CV] (agent table [UV]) |
| C-10 | Run record | `review-telemetry/1` (strata sonnet/haiku, no automatic writer) | `review-panel-manifest/1` (states frozen..published) and contract `telemetry:` block; E2 `meta.json`/`cost.json` | `telemetry.py:17, 49, 112`; `manifest.py:38-54`; `run-reviewer.sh:58, 87` | [CV] |
| C-11 | Loop contract vintage | shipped `spec-panel.md` Review Loop (#478/#479 clauses, hard gate) | five installed variants built on the PR #427 base: none contains `follow-up candidates` or the hard-gate section | slice 12 C8 | [UV] |
| C-12 | Cap constant | 3 in `new_ledger` (`ledger.py:37-38`), `CAP_REVIEWS = 3` in ledger and diffgate scripts (`review_ledger.py:35`, `diffgate.py:23`) | none | identical, listed here only because it is a shared constant | [CV] |

Shared defects (not conflicts, but they travel with any core built from E1 + E3s): the whole-finding drop at anchor/claim over 200/300 characters exists in both parsers (probe P-c); the `T01.02` task-id gap exists in both `refs_norm` users (probe P-d; `telemetry.py` has a copy of the regex, slice 02 R-3 [UV]); `lint_cmd` and `estimate_cmd` are registered in `__init__.py` but absent (slice 02 H15 [UV]).

## 6. Resolution record for the open items
| Item | Result | Where |
|---|---|---|
| (a) classify every cell | done: 15 capabilities x 4 columns, each with class, tag and citation | section 4 |
| (b) E2 commits after hand-off change no `src/` or `tests/` | confirmed (0 files in each of c2ddeb1b4, fd69a006d, d561461fa, 6c0984326; branch-wide diff empty) | section 1.1 |
| (c) `snap.py` writes into E1's evidence tree | confirmed as a write path with matching hash evidence; `rlog-r3.sh` also writes into E1's `audit.log` path | section 1.2 |
| (d1) #519/#518 attribution | E2 attribution to #518 [CODE-CONTRADICTED]; #519 changes 17 `RV` files and 22 `tests/review` files, #518 changes 0 and 1 | section 1.3 |
| (d2) reflect contrast | E2 row true for the code-driven path, false for the product (SKILL.md shadow engine + kernel); `cli/reflect` has no panel code | section 2 |
| Slice 09 gap: do the installed variants re-implement or import `cli/review`? | They re-implement: all four scripts import only the standard library and contain zero references to `superclaude.cli.review` or `superclaude review` (Grep count 0 each) [CV]; sizes 2668 / 2050 / 1740 / 1131 lines re-measured [CV]; installed commands `spec-panel-{armb,diffgate,ledger,ponytail,stoprule}.md` and agent `finding-grader.md` present [CV]; `src/superclaude/skills` has only `sc-bare-review` among the names searched and `src/superclaude/agents` has no grader [CV] | `ls`, `wc -l`, `grep -cE` this session |

## Gaps and Questions
1. [UNVERIFIED] The E3i cells (grammars, statuses, rubric, exit codes) rest on scope slice 12; I re-measured only file existence, sizes, `SCHEMA`/`CAP_REVIEWS` constants and imports. Searches tried: `grep -nE '^(import|from) '`, `grep -cE 'superclaude\.cli\.review|superclaude review'`, `wc -l`, `ls ~/.claude/commands/sc`.
2. [UNVERIFIED] The E1 code-driven path (ensemble dispatch via `T2Model0N`, `contract_version: 1.0`, 10 unknown keys, `panel_lint` L1/L2 failure) rests on slice 10; I verified only that `cli/reflect` has no panel/tier import (Grep) and the 0.80 threshold line. Needed for deciding which of E1's two paths the core serves.
3. [UNVERIFIED] The 40 files / +8,026 line figure and the `@live7` duplicate counts (slice 01 got 30/40, slice 02 got 26/40, E2 states 26 of 40, run-id sets differ) were not re-derived; my file-count split (17 + 22 + 0 + 1 = 40) agrees with the file count only.
4. [UNVERIFIED] Who ran `snap.py`: the hash identity shows the E1 file equals the script's output, not that the E2 script produced it (a different process could compute the same formula). No timestamps were compared (searched `git log` for the file: one commit, 792cf8c52).
5. [UNVERIFIED] E2 study figures (found/14, real blocking/8, 49 blocking dropped, 156 of 665 source-blind, 91.4% anchor fidelity) are not reproduced; they appear only as pointers to slices 01 and 03.
6. [UNVERIFIED] Whether any E2 collaboration harness (r1-r5) has been run end to end: slice 08 says r3 and others have unmet acceptance criteria and no results; slice 05 says the brainstorm specs are requirements-only. I counted files only.
7. Slice 03 says `combos/` has 95 row dirs plus `SPEC.md`; `git ls-tree -d` at the tip gives 96 directories directly under `combos/` (my count), matching slice 01.
8. Negative evidence recorded: no ledger/verdict/round code in the new E1 modules (Grep); no memory mechanism in `cli/review`, `spec-panel.md` or the loop prompts (Grep, one unrelated word); no tier JSON or `cli/review` import in `cli/reflect` (Grep); no `src/`/`tests/` change on the E2 branch (`git diff --stat` x2, `git diff-tree` x4); no E3i import of `cli/review` (Grep); no `muse-ember` in the tier file (read).
9. Design questions this matrix raises for the unified core (not answered here): which finding location type is the default (quoted anchor vs file:line citation) or whether both are first-class; whether v2 gains `prior` lines or the loop moves to a v2-native re-review contract; who owns the verdict (reviewer line, ledger boolean, computed script, convergence score); one ledger schema and status vocabulary; whether E2's raw-model dispatch becomes a `launch` entry for the gateway environment.
10. I added the label "absent" to the four requested classes (section 4.1) so absent cells still carry a classification.

## Stale Documentation Found
- **[STALE DOC] / [CODE-CONTRADICTED]** E2 run-2 and `HANDOFF-run1-vs-run2.md:22` attribute the `cli/review` change to "#519 + #518"; #518 changes no `cli/review` file (section 1.3).
- **[STALE DOC]** E2 run-2 section 5.6 "Contrast with reflect Tier 2" was taken from base-commit notes and not re-read; it predates the SKILL.md shadow engine (`SKILL.md:87, 309-349`) and the reflect-shaped kernel (section 2). Its `SKILL.md:592` cite for `reflect-reviewer` is now `:640` (slice 01 section 4.6 [UV]).
- **[STALE DOC]** E2 run-1/run-2 line cites for `panel.py`, `panel_cmd.py`, `review-tiers.default.json` are stale at HEAD (panel.py 525 -> 707 lines per slice 01 [UV]; the tiers file is 38 lines at HEAD, read in full this session).
- **[STALE DOC]** `manifest.md:5` of the E2 eval says the branch is "local, never pushed"; it is on origin (slice 03 [UV]).
- **[STALE DOC]** E1 `.dev/eval-workspaces/shadow-model-combos/PLAN.md:1,3` and `combos.json:4` still say "designed, NOT run" although 15 runs exist (slice 11 [UV]).
- **[STALE DOC]** `src/superclaude/cli/reflect/__init__.py` docstring describes the wrapper as a `claude --print` fan-out and omits `ensemble`, `fallback`, `_diversity`, `panel_lint` (slice 10 [UV]).
- **[STALE DOC]** `plugins/superclaude/commands/spec-panel.md` lacks `--unattended`/`--report-dir`/`--improve` and softens the hard-gate sentence (slice 12 A1 [UV]).
- **[STALE DOC]** the five installed `spec-panel-*.md` variants are built on the PR #427 base (slice 12 C8 [UV]).
- Imprecise scope-slice statement corrected here: "`findings_v2.py:15-22` limits inherited through `_check_flat`" is true for the mechanism only; the limits are restated as literals (section 3).

## Summary
At HEAD the three programs overlap in four places only: the finding id regex and the findings-v1 grammar (shared by E3 and used unchanged by E2), the shared `cli/review` panel engine (E1 is a strict superset of E3 there), the constant review cap of 3, and E2's unchanged use of E3's merge. E1 and E3 conflict on the finding location type (file:line citations vs quoted anchors, with v2 citation-only findings crashing the v1 ledger path), the blocking rule, the fingerprint, the verdict model and the run record, while the installed-only E3 variants are a second, stdlib-only, stale-based implementation of the whole loop that shares no code with the package. E2 contributes no product code at any commit (confirmed for the post-hand-off commits and the whole branch) but is the only source of ground truth, working non-Claude dispatch, and collaboration designs; its snap.py/rlog scripts are write paths into E1's evidence tree. Two E2 claims are resolved: the `cli/review` change belongs to #519 alone (#518 is one test file), and "reflect has no panel/tier code" holds only for the code-driven `cli/reflect` gate, not for the product, where SKILL.md's shadow engine consumes the tier JSON and the kernel was built for reflect.
