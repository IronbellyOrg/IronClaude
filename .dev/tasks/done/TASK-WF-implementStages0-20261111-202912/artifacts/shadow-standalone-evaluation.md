# Shadow run as a standalone piece: evaluation

Read-only evaluation, 2026-11-12, branch ironbelly/brainstorm-reflect-panel.

## 1. Reflect-specific vs generic

Key fact first: the shadow run is not a program. The agent carries it out from the prose steps 1-10 of SKILL.md §4.3a
(SKILL.md:338-349). A grep for `t2_engine|t2-engine` over `src/superclaude/cli` finds only `review/manifest.py` and
`review/manifest_cmd.py`; the Python reflect wrapper (`cli/reflect/`) has no shadow code. The other part of the
shadow work is the "variant under test" (the panel kernel: resolve, findings-v2, cluster, pre-check), not the harness.

| Component | Class | Why | Evidence |
|---|---|---|---|
| Shadow authority rule (legacy writes the stable files, shadow writes only to `<out>/panel/` and `telemetry:`, failure gives `panel_fallback_reason` and the run continues as legacy) | generic idea, reflect wording | The pattern works for any skill; the text names Waves 3-5, the debate and contract 1.8.0 | SKILL.md:338, :349 |
| Shadow steps 1-10 | reflect-specific | `@reflect-pre`/`@reflect-pre-x2`, executor class, personas, Wave 3C calibrator line, evidence validator, judge identity | SKILL.md:340-348 |
| `review/manifest.py`: hashes, ordered stages, idempotent attempts, resume, atomic save | generic mechanism | Frozen inputs + policy hash + ordered-stage commit + (stage, unit, attempt) identity apply to any pipeline | manifest.py:13-18, :156-163, :277-328, :402-419 |
| `review/manifest.py`: constants and keys | reflect-specific | stage names `frozen..published`, `t2_engine_*` keys, `reviewers_*` counts, `REPORT.md`/`return-contract.yaml`/`audit.log`, template/tiers/brief hashes | manifest.py:39-63, :126-127, :143-145, :201-203 |
| `manifest.py` shadow publish guard + `hash_published_files` | generic idea | Refuses to write the authoritative files in shadow mode and only records their hashes, which proves non-interference | manifest.py:496-500, :527-534 |
| `review/manifest_cmd.py` | partly | Fixed path `panel/manifest.json`, `input_tree_sha256` read from reflect's input snapshot, `--t2-engine-*` options | manifest_cmd.py:20, :37-45, :77-78 |
| `review/panel.py` + `panel_cmd.py` (resolve) | generic, with a reflect profile | Generic tier/template resolver also used by the spec-panel loop; `reflect-*` templates get extra rules | panel.py:1-9, :71-73; rules/prompts/document_review_loop_prompts.md:70 |
| `review/findings_v2.py` | partly | Shared finding format, but lenses and categories are reflect + spec only | findings_v2.py:36, :41-48 |
| `review/cluster.py`, `cluster_cmd.py` | partly | Deterministic clustering is generic; primary roles are keyed by reflect lenses; output under `panel/` | cluster.py:67-71; cluster_cmd.py:1-12 |
| `review/verify_cmd.py` | partly | Citation pre-check is generic; writes `<out>/panel/precheck.json` and feeds reflect's evidence validator | verify_cmd.py:1-12 |
| `review/card_convert.py` | reflect-specific | Converts recorded reflect reviewer cards | card_convert.py:1 |
| `review/telemetry.py` (review-telemetry/1) | generic store, not used by shadow | Append-only JSONL + SQLite loader, but its fields are reviewer/panel records; §4.3a never calls it (shadow records go to the contract's `telemetry:` block) | telemetry.py:1-3, :30-81; SKILL.md:969-988 |
| `cli/reflect/panel_lint.py` | reflect-specific | Lints against the frozen 1.8.0 stable field list | panel_lint.py:1-7, :33 |
| `scripts/reflect_shadow_exit.py` | skeleton generic, checks reflect | Counting published/failed/incomplete runs, INSUFFICIENT-RUNS, exit codes 0/1/3/2 are generic; `pre-*` glob, personas, parity, MALFORMED, EV-1, lint, replay are reflect | reflect_shadow_exit.py:7-10, :33-34, :55-56, :209, :240 |
| `scripts/reflect_verdict_replay.py` | partly | Pair-by-directory and "new degraded reason" comparison is generic; the verdict function is reflect's `derive_verdict` on 1.8.0 | reflect_verdict_replay.py:28-31, :50, :54-55 |
| Brief line for shadow | reflect-specific | One extra findings-block line only when the engine is `shadow` | reviewer-spec.md:39 |

## 2. Minimal generic shadow-run contract

What the code really does, stated as a contract any skill could follow:

1. **Variant under test.** A named variant (reflect: `shadow` engine + template id) whose definition is frozen as
   hashes before work starts (manifest.py:97-108 policy hash; :55-63 frozen fields). A changed input or policy starts a
   new invocation, never a silent reuse (manifest.py:422-470).
2. **Authoritative path.** The existing pipeline runs unchanged and alone writes the stable outputs. The variant writes
   only under its own subdirectory and a namespaced `telemetry:` block (SKILL.md:338, :969). At the end the manifest
   records the hashes of the authoritative outputs and rewrites nothing (manifest.py:496-500, :527-534). A variant step
   that cannot run records a fallback reason and the run goes on (SKILL.md:338, rule D4 at :320).
3. **Recording.** An ordered, skill-declared stage list committed one at a time with payload/output hashes, plus
   per-unit attempts keyed (stage, unit, attempt) that never add a second vote (manifest.py:13-18, :331-386). Only a
   manifest in the last stage counts (manifest.py:176-186).
4. **Comparison.** Per run, a skill-supplied comparator. Reflect has two: parity of the variant's resolved setup with
   what legacy actually ran (reflect_shadow_exit.py:117-177) and a verdict replay against a legacy baseline of other
   runs (reflect_verdict_replay.py:28-31). Note: reflect's shadow variant produces no verdict of its own; it reuses the
   legacy reviewers' dispatch (SKILL.md:342), so it measures side signals (agreement, compliance, parity), not quality.
5. **Exit measurement.** N required runs, hard-fail checks per run, aggregate rates against a baseline, and a
   PASS / FAIL / INSUFFICIENT-RUNS verdict with fixed exit codes (reflect_shadow_exit.py:26-34, :376-386).

Skills that could plausibly use it (at most 4):

- `/sc:spec-panel` loop: already calls `superclaude review panel resolve` and `review merge`
  (rules/prompts/document_review_loop_prompts.md:70); its variants (stoprule, ledger, diffgate) are alternative-variable
  experiments. The variant skills are not in this checkout's `src/superclaude/skills`: UNVERIFIED.
- `sc-troubleshoot-protocol`: same T1 then T2 parallel hypotheses + adversarial debate shape (its SKILL.md:3, :46).
  Code beyond those lines not read: UNVERIFIED fit.
- `sc-workflow-protocol`: its Wave 4 runs `/sc:reflect --mode pre` with defaults (its SKILL.md:89), so plan-generation
  variants could be shadowed with reflect as the judge. UNVERIFIED whether that is wanted.
- Overlap, not a consumer: `sc-cli-eval` / `src/superclaude/cli/eval/` and `scripts/eval_runner.py`,
  `scripts/ab_test_workflows.py` already run variants and record results offline. Their features were not read:
  UNVERIFIED how much they already cover.

## 3. Complexity

**Medium** for the harness alone (manifest profile + exit-aggregator skeleton + one shared protocol ref).
**Large** if "shadow the whole pipeline with alternative variables" means the variant must produce its own full,
comparable output: that doubles model spend and needs a per-skill comparator and ground truth, which reflect itself
declined for quality measurement (pilot-design.md:50: arm C uses `--t2-engine panel`, not `shadow`, because shadow
keeps the legacy writers authoritative). Size estimate, not measured: about 1,700 lines are in play (manifest 534,
manifest_cmd 240, exit 410, replay 184, lint 366 per `wc -l`), of which roughly a third becomes shared code.

Main cost drivers:
- Manifest constants: `STATES`, `PER_REVIEWER_STAGES`, `PUBLISH_FILES`, `FROZEN_FIELDS`, `ENGINES` are module tuples
  (manifest.py:39-63) and the serialized keys are `t2_engine_requested/effective` and `reviewers_*`
  (manifest.py:126-145). They must become a profile while reflect's file stays byte-identical
  (schema `review-panel-manifest/1`, manifest.py:38), or recorded manifests stop validating.
- CLI paths and inputs: `panel/manifest.json` and the `input_tree_sha256` of reflect's input snapshot are hard-coded
  (manifest_cmd.py:20, :37-45).
- Every consumer needs prose steps in its own SKILL.md, because no runtime exists to call; compliance is the agent's.
- Exit aggregator: split into a skeleton plus a reflect plugin (personas, `pre-*` glob, lint, EV-1, replay:
  reflect_shadow_exit.py:55-56, :209, :225-250).

Main risks:
- Test pins: `tests/review/test_review_manifest.py:49, :80` iterate `mf.STATES` and expect the full reflect list;
  `test_shadow_skill_contract.py:66` allows SKILL.md edits only in §3.1, §4.3a, §5.4, §9.2, `:42-49` pins the §9.1
  block and 1.8.0 byte-for-byte, and `:104` runs the manifest recipe exactly as written in the skill.
- Contract 1.8.0 coupling lives in the reflect side (panel_lint.py:33; reflect_verdict_replay.py:54); it must not leak
  into the shared piece, and the shared piece must not force a contract bump.
- Template ids (`@reflect-pre`, `@reflect-pre-x2`, SKILL.md:340) and the `reflect-` profile (panel.py:71-73) belong to
  the variant, not the harness; moving them would be scope creep.
- The mechanism has never run for real: `test_shadow_exit_script.py:292-302` asserts "shadow runs counted: 0 of 20".
  Generalizing an unexercised stage list freezes guesses into a shared API.
- Installed-path rule: a shared protocol ref must be referenced by its `~/.claude/...` path with the project `.claude/`
  fallback, never `src/superclaude/...` (project CLAUDE.md, "Never Hardcode src/superclaude/ Paths").

## 4. Plan

Extraction (a):
1. Gate: start only after the 20 real reflect shadow runs give a PASS from `scripts/reflect_shadow_exit.py`; freeze
   the stage list and telemetry fields that survived.
2. Add a run-manifest module parametrized by a profile (schema id, stages, per-unit stages, publish files, frozen
   fields, engine key names, subdirectory), moving the logic of `review/manifest.py` unchanged.
3. Define the reflect profile with today's exact constants and key names; `review/manifest.py` re-exports it, so
   `mf.STATES` and every import keep working.
4. Add a profile-aware CLI (`init|advance|validate --profile`); `superclaude review manifest` stays as the reflect
   alias with identical options and output.
5. Split `reflect_shadow_exit.py` into a generic aggregator (discovery, count, required N, verdict, exit codes) and a
   reflect check plugin; keep the script name, CLI and report text.
6. Write the shared protocol ref (authority rule, subdirectory, stage advance, `telemetry:` namespace, fallback reason)
   in a skill's `refs/`, referenced by installed path; run `make sync-dev` and `make verify-sync`.

Re-integration into reflect (b) and proof of no change:
7. In SKILL.md §4.3a only, replace the generic wording of the shadow preamble with a pointer to the shared ref; steps
   1-10 and every command line stay as written (test_shadow_skill_contract.py:66, :104).
8. Golden check: run the §4.3a manifest recipe with the old and new code on the same fixture and compare
   `panel/manifest.json` byte for byte; replay the recorded `.dev/reflect/pre-*` runs through the verdict replay.
9. Keep green: `tests/review/test_review_manifest.py`, `test_review_cli.py`, `test_review_cluster.py`,
   `test_review_cluster_cmd.py`, `test_review_verify_citations.py`, `test_review_findings_v2.py`,
   `test_review_panel*.py`, `test_review_reflect_templates.py`; `tests/cli/reflect/test_shadow_skill_contract.py`,
   `test_shadow_exit_script.py`, `test_verdict_replay_script.py`, `test_panel_contract_lint.py`; then `make test`.
10. Only then wire one second consumer that the owner names, with its own profile and comparator.

## 5. Recommendation

**After the 20 real reflect shadow runs.** Today zero shadow runs exist (test_shadow_exit_script.py:292-302), so the
stage list, telemetry fields and comparator have never met a real run; extracting now would freeze guesses into a
shared API and double the churn when the runs force changes. No second consumer is committed either, and existing eval
tooling (`cli/eval`, `scripts/eval_runner.py`) may already cover "run variants and record results" (UNVERIFIED).
Do the extraction only if, after the runs, the owner names a second skill; until then the reusable parts
(manifest mechanism, authority rule, exit skeleton) cost nothing to leave where they are.
