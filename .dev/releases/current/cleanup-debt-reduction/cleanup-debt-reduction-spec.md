---
title: "Cleanup Debt Reduction"
version: "1.0.0"
status: reviewed
feature_id: CLEANUP-DR
parent_feature: null
spec_type: refactoring
complexity_score: 0.62
complexity_class: MEDIUM
target_release: cleanup-debt-reduction
release_version_policy: "Planning codename only; no package bump or tag authorized."
created: 2026-10-19
baseline_commit: cdc70cd6a731d94c546e76256d11e12215cd7880
worktree: .dev/worktrees/cleanup-release
branch: feature/cleanup-release-spec
source: "Repository-wide cleanup audit, adversarial merits debate, independent deletion-risk review, and targeted source refresh from the preceding session."
---

# Cleanup Debt Reduction — Release Specification

## 1. Problem and release objective

The repository retains disconnected implementations, duplicated concrete utilities, an orphan publishing wrapper, and obsolete packaging/formatter configuration. Reduce their maintenance cost without changing supported runtime behavior, weakening requirement coverage, or introducing a general-purpose abstraction layer.

This is a scoped refinement of an existing evidence-backed audit, not a new feature proposal. The initial estimate is **488 source/configuration lines and one direct development dependency** across ten candidates. These are planning estimates, not quotas or guaranteed patch results. Documentation, test migration, shared-helper imports and lockfile changes affect the eventual diff. No requirement may be sacrificed to reach a line-count target.

### 1.1 Evidence and provenance

Paths in this document are relative to the cleanup worktree root. Symbol names are authoritative; baseline line numbers are navigation aids and must be refreshed before edits.

| Candidate | Baseline source and evidence | Estimated net lines |
|---|---|---:|
| C01 | `src/superclaude/cli/cli_portify/monitor.py`: EventRecord, EventLogger, classify_failure, generate_diagnostic_report; audited runtime consumers use OutputMonitor/TimingCapture and separate logging/diagnostics | 139 |
| C02 | `scripts/publish.sh`: delegates to absent `scripts/build_and_upload.py`; live instructions remain in scripts README and cleanup script | 95 |
| C03 | Four `src/superclaude/cli/swarm/recipes/*_v1.py` modules copy timestamp, YAML scalar, frontmatter and selected section/confidence primitives | 60 |
| C04 | `src/superclaude/cli/cli_portify/failures.py`: handle_non_writable_output, handle_missing_skills, get_failure_handler_name have dedicated test consumers but no audited production callers | 54 |
| C05 | `setup.py`, `MANIFEST.in`: setuptools surfaces while `pyproject.toml` selects Hatchling and explicit wheel/sdist payloads | 44 |
| C06 | `cli/tasklist/executor.py` and `cli/roadmap/validate_executor.py`: duplicate _embed_inputs and _sanitize_output | 30 |
| C07 | `cli/swarm/normalize.py` _atomic_write_text and `cli/swarm/reduce.py` _atomic_write_bytes: same write transaction except encoding | 22 |
| C08 | `pyproject.toml`: Black development dependency and tool.black section; active formatting uses Ruff | 17 |
| C09 | `cli/swarm/normalize.py` _PassthroughFallback duplicates concrete recipes.passthrough.Passthrough | 14 |
| C10 | `cli/roadmap/executor.py` apply_decomposition_pass only delegates to pipeline.deliverables.decompose_deliverables | 13 |

Source paths abbreviated to `cli/` in this table are beneath `src/superclaude/`. The previous independent reviews established repository-local evidence, not proof that no external Python import consumer ever existed. Implementation must repeat caller/registration/documentation checks at its actual starting revision.

### 1.2 Scope fence

**In scope:** precisely C01–C10, their necessary imports/docs/tests/lock metadata, existing requirement coverage preserved at real runtime boundaries, and release evidence.

**Held and untouched:** roadmap `generate_degraded_report`, `build_remediate_metadata`, `derive_pipeline_status` and their NFR-007/SC-008 compatibility/integration coverage; root `package.json` and framework-version readers; complete validator runner extraction.

**Rejected and untouched:** Reporter renderer-callback bypass (would stop honoring overridden public emitter methods); alternate fidelity-batch-runner deletion (release sets/cooldowns/batching differ); removal of registry None-sentinel support; preflight atomic-writer consolidation.

**Also out of scope:** rescued worktrees, archival release evidence, required plugin/dev mirrors, public PM/execution APIs, CLI additions, bug fixes unrelated to these refactorings, new runtime dependencies, package renaming, version bump, tag, publication, commit, push, PR, merge, and task execution during this planning session.

## 2. Solution and architectural decisions

Delete only disconnected implementations after their coverage obligations are reconciled. Reuse concrete functions for genuinely identical behavior; do not add a recipe superclass, renderer strategy, generic process runner, callback framework, configurable persistence layer, or new configuration knobs.

| Decision | Required choice | Rationale |
|---|---|---|
| Utility placement | Prefer existing appropriate lower-layer helpers; otherwise small leaf modules with only the needed concrete functions | Reuse must not invert dependency direction or introduce cycles |
| Validation helpers | Tasklist and roadmap validation may depend on shared lower-layer utilities; pipeline must never import roadmap | Existing architecture tests prohibit reverse dependencies |
| Recipe policy | Preserve module exports, lookup/patch seams, recipe-specific defaults/caps and parsing differences | Shared primitives are not shared policy |
| Persistence | Share only normalize/reduce byte-writing mechanics | Preflight has distinct exception semantics and remains separate |
| Removal evidence | Refresh exact and dynamic references, registrations, docs, entry points and requirement tests before each deletion | Test-only usage is not sufficient to retire a promised behavior |
| Release identity | Descriptive codename until normal release management assigns a version | No fabricated version or implicit publication authorization |

Runtime data flow remains unchanged:

```text
N validation inputs -> ordered embedded text -> existing separate validator runners -> unchanged tool-write phase
N worker results -> recipe normalization -> N normalized results (same order/status/salvage policy)
text (C code points) -> UTF-8 encoding (B bytes) -> atomic write -> B persisted bytes; return B
```

No refactoring may score, deduplicate, filter, reorder or synthesize worker results. Empty collections remain empty. Character count and UTF-8 byte count are not interchangeable.

## 3. Functional requirements and acceptance criteria

### FR-01 — Remove only disconnected monitor helpers (C01)

Remove EventRecord, EventLogger, classify_failure and generate_diagnostic_report, unused imports and stale module claims **only after FR-11 passes for this candidate**.

Acceptance:
- OutputMonitor, TimingCapture, PhaseTiming and their real consumers retain current signatures and behavior, including timing, eight-field monitoring, stall/growth/convergence/findings/placeholder behavior.
- ExecutionLog and DiagnosticsCollector behavior and event/report contracts remain covered through live consumers.
- Classify affected tests as helper-only versus requirement-bearing. Migrate relevant requirement assertions to real logging/diagnostic/executor boundaries before removing obsolete assertions. Do not delete the entire monitor test file or fabricate wiring to justify deletion.

### FR-02 — Retire the orphan local publishing wrapper (C02)

Remove `scripts/publish.sh` and all active instructions advertising it or its absent build/upload target from `scripts/README.md` and `scripts/cleanup.sh`.

Acceptance:
- No active operator instruction or executable reference advertises the deleted wrapper or absent target; historical archives may retain clearly historical references.
- Preserve `.github/workflows/publish-pypi.yml`; document the surviving publication route accurately without claiming parity with every retired local mode.
- Verification must not upload, publish, obtain publishing credentials, or run an upload-capable legacy helper.

### FR-03 — Share identical recipe primitives only (C03)

Consolidate byte-for-byte-equivalent timestamp/YAML/frontmatter utilities and equivalent section/confidence primitives among bare_review_v1, findings_table_v1, hypothesis_table_v1 and verdict_only_v1.

Acceptance:
- Preserve existing module-level import names and `__all__`; preserve effective lookup/monkeypatch behavior used by supported callers/tests, using tiny local adapters only where required.
- Retain independent recipe parsers/renderers, caps, salvage rules, ordering, fields and AC-011 no-judging behavior. Do not standardize differing policy.
- Bare-review parse_conf with no digits remains empty; hypothesis/verdict parse_confidence preserves collapsed qualitative text. Numeric extraction/clamping remains unchanged, including current treatment of signed-looking text (do not invent new numeric parsing).
- Fixed-clock golden/parity cases cover empty and whitespace-only text, Unicode, YAML quotes/backslashes, leading/absent/malformed frontmatter, absent/empty/repeated sections, qualitative confidence, numeric boundary inputs and every existing cap. Identical cases produce identical serialized output before/after; legitimately nondeterministic timestamps use an identical frozen clock.
- Pin current primitive boundaries, not improved parsing: confidence uses the first digit run (`-1` -> `1`, `101` -> `100`); no-digit ` high  confidence ` -> empty for bare review and `high confidence` for hypothesis/verdict confidence helpers. Section extraction takes the first matching case-insensitive heading, ends at the next heading, collapses whitespace then slices by code points; do not merge repeated same-name sections. Frontmatter stripping uses leading-whitespace detection plus at most two literal `---` splits; fewer than two literal delimiters leaves input unchanged, but no YAML-validity or standalone-line requirement is added. Preserve cap-minus-one/cap/cap-plus-one cases for bare claims 120, verdict 300, notes 200; findings cells 200 and fallback notes 300; hypothesis cause/next-step 240, evidence 320 and fallback notes 300; verdict label 32, rationale 300, notes 600 and its initial verdict-section extraction 600. Existing parser and salvage/fallback policy branches remain local.

### FR-04 — Remove only disconnected failure helpers (C04)

Remove handle_non_writable_output, handle_missing_skills and get_failure_handler_name after FR-11 passes for this candidate.

Acceptance:
- Preserve FailureHandlerResult, all registered handlers, has_handler, the seven-classification registry, timeout constants, review-owned rejection and executor-owned gate failure handling.
- Preserve actual unwritable-output validation and missing-skill fallback behavior at live config/executor boundaries; reconcile NFR-009 assertions before deleting helper-only tests.
- Do not infer handler execution from code that merely logs a registered callable's name. Do not add registration/wiring or change failure policy in this release.

### FR-05 — Retire inactive setuptools packaging surfaces (C05)

Remove root `setup.py` and `MANIFEST.in`; keep Hatchling configuration and today's distribution scope unchanged.

Acceptance:
- Before other refactors or dependency/lock edits, perform a packaging-only paired comparison: identical source/dependency snapshot and recorded build-tool versions, differing only by removal of `setup.py`/`MANIFEST.in`. Capture baseline and paired-post wheel/sdist normalized member manifests and payload hashes. Use the safely serialized working tree before other edits or isolated copies, never revert unrelated concurrent work to create the pair. Require unchanged payload/resource hashes except the two retired files if actually packaged and individually justified archive/generated metadata differences. A missing pair or unexplained difference blocks C05.
- At final-release verification, compare final manifests/hashes with the baseline using an explicit per-path delta ledger for authorized C01–C10 source/test/config changes (including packaged duplicate source copies where applicable), the three permitted file retirements if present in baseline archives, archive container metadata and attributable generated metadata such as Black requirement changes. Each difference needs its candidate/reason; unchanged unrelated resources must retain hashes and no unexplained missing member or blanket source/resource exclusion is allowed. Final-release parity does not mean the intentionally changed source bytes must remain identical.
- Build a wheel from the resulting sdist and compare its normalized payload/resources with the post-change direct wheel using the same per-path justification rules, then install the sdist-derived wheel into an isolated environment. Verify both CLI entry points (`superclaude`, `ic`), pytest plugin discovery and installed framework/plugin/component/template resource lookup.
- Do not bulk-copy legacy MANIFEST inclusions into Hatchling: current Hatchling outputs, not the unused setuptools manifest, define the parity baseline.
- State in release notes that legacy direct setuptools invocation is retired. If an actual supported consumer is found, stop this candidate rather than assume compatibility.

### FR-06 — Share validation text helpers, not runners (C06)

Keep one implementation each of _embed_inputs and _sanitize_output for tasklist and roadmap validation. Preserve existing module import seams where tests/callers use those helper names.

Acceptance:
- Embed preserves empty result, input ordering, fenced labels/content, UTF-8 reads and read-error propagation.
- Sanitize returns 0 without writing for a missing file, any `content.lstrip().startswith('---')` (even malformed or unclosed frontmatter), or no match of multiline `^---[ \t]*$`. Otherwise choose the first matching standalone delimiter, retain that delimiter and its suffix, and return the UTF-8 byte count of the removed prefix. Do not require a closing YAML delimiter or treat embedded/indented delimiters as standalone matches. Preserve current UTF-8 text read/write and newline semantics, the fixed sibling `<suffix>.tmp` write then replace, read errors other than FileNotFoundError, write/replace error propagation and success-only logging through the existing caller logger; sanitizer failure cleanup is not upgraded into the separate FR-07 transaction.
- Preserve each runner's dry-run, cancellation, timeout, exit handling, timestamps, subprocess options and sanitization-before-tool-write order. Main roadmap executor's distinct sanitizer and richer labeled embedding stay untouched.
- No import from pipeline to roadmap, no import cycle, no process/callback framework. Exercise both real validator integration paths, not just the shared utility in isolation.

### FR-07 — Share normalize/reduce atomic-write mechanics (C07)

Retain one concrete byte-writing implementation and a thin UTF-8 text adapter; preserve existing helper entry points as needed by callers/tests. Text encoding must not be evaluated as a shared-writer call argument before baseline parent setup; small wrappers may preserve that ordering without callbacks or a framework, even if savings are below estimate. Do not touch preflight's writer.

Acceptance:
- Preserve parent creation timing, same-directory temporary file, binary write, flush, file fsync, atomic replace, cleanup on failure, original exception propagation and byte-count return.
- On injected fdopen/write/flush/fsync/replace failure before successful replacement, pre-existing destination bytes remain unchanged. Preserve baseline `except Exception`: attempt temporary unlink, suppress only cleanup OSError, then re-raise the original exception; a failed unlink may leave a temporary sibling and is not a successful write. Parent creation failure and mkstemp failure propagate without partial destination; the text adapter must still create the parent before UTF-8 encoding, so an encoding error may leave the parent but no temporary file/destination change. SIGKILL/BaseException is not caught cleanup and may leave a temporary sibling; do not promise kill-time cleanup or new crash durability. No new directory-fsync policy or other error swallowing is introduced.
- Empty payload writes zero bytes successfully; Unicode returns encoded byte length; repeated writes preserve each complete successful payload.
- Preserve caller-level confinement and emission gates for normalized artifacts, metadata, contracts, merged output and done sentinels. Do not bypass symlink/output-root rejection or broaden writable paths.
- Update structural tests that legitimately relied on os.replace residing in a particular module to trace/assert the shared transaction; never weaken the atomicity requirement into a name-only check.

### FR-08 — Remove unused Black development configuration (C08)

Remove the direct Black development requirement and tool.black section, update lock metadata consistently, and correct the stale formatter attribution comment.

Acceptance:
- Preserve Ruff's pin, formatting/lint policies and active Make/pre-commit/CI commands. No unrelated dependency upgrade or lockfile churn.
- Preserve Black's allowance in `scripts/dependency_baseline.txt`; the dependency checker is an allow-list, not an exact required-installed set. Do not uninstall packages from the operator's environment.
- A clean locked development resolution no longer requires Black through the removed direct extra; any remaining transitive occurrence is reported with its dependency reason, not forcibly removed.

### FR-09 — Reuse concrete passthrough while preserving dispatch (C09)

Replace _PassthroughFallback with a concrete recipes.passthrough.Passthrough instance in the registered-None branch; update registry/fallback documentation.

Acceptance:
- Registered None still returns unchanged raw text, salvaged false and error None; empty, Unicode and whitespace-only values retain their exact contents.
- Unknown name still raises KeyError; invalid non-None object still raises TypeError; a valid registered Recipe remains itself. Preserve registry extension and contents.
- Do not resolve fallback through mutable REGISTRY['passthrough'], register the fallback implicitly, or promote parse errors into successful normalized output.

### FR-10 — Remove the unused decomposition wrapper (C10)

Remove only roadmap.executor.apply_decomposition_pass and now-unused imports. Retarget its behavioral tests to pipeline.deliverables.decompose_deliverables; only the delegation-specific assertion is obsolete.

Acceptance:
- Preserve Implement/Verify pairing, nonbehavioral behavior, empty inputs, ordering and idempotence through the actual decomposition function.
- Do not remove or modify held roadmap metadata/status/report helpers, their compatibility tests, state readers/writers or other certification/convergence behavior.

### FR-11 — Evidence and requirement-preservation gate

Before any C01/C04/C05/C10 deletion, record a candidate-specific eligibility row: current revision, exact/dynamic caller and registry/entry-point/doc searches, affected requirement assertions, surviving live owner, test migration/retirement rationale and validation evidence.

Acceptance:
- A candidate with a live consumer, unknown requirement owner, promised compatibility conflict, missing baseline or failing migration test is **BLOCKED**. Its deletion must not proceed. Retain it and surface the blocker; do not silently skip it and claim the full release complete.
- No broad test-file removal or requirement waiver. Obsolete helper-mechanics tests may be retired with explicit rationale; surviving behavior is tested at its real boundary. Newly discovered unrelated bugs are reported separately, not repaired opportunistically.
- Intentional retirement of an internal/test-only helper import is recorded; no claim is made that repository search proves all external consumers absent. Supported public-contract conflicts require a scope decision, not an automatic shim or waiver.

### FR-12 — Verification, documentation and bounded release handoff

Produce a traceability/evidence record linking FR-01–FR-12 and NFR-01–NFR-06 to tasks, acceptance cases and observed results. Report each candidate completed or blocked, actual source/config net change, docs/test changes separately, and dependency delta.

Acceptance:
- Run targeted tests for each changed behavior, architecture/lint/format checks, full suite, packaging verification and relevant CLI/plugin smoke checks before release readiness. Existing baseline failures are recorded with identical before/after reproduction; new failures block readiness and no skipped gate is called PASS.
- Preserve held/rejected surfaces explicitly in diff review. No new runtime dependency or speculative abstraction; legitimate evidence-backed correction to a line estimate is not a failure.
- Future component edits use canonical src first and required dev sync/verification; never stage generated .claude contents. Commit/push/PR/publication remain separate user authorization.
- This planning handoff stops after a complete spec, generated MDTM tasklist and pre-reflection report. All implementation checklist items remain unchecked.

## 4. File architecture and implementation order

### 4.1 File changes

Production modifications are limited to sources listed in C01–C10, their necessary imports and existing tests; docs collateral is scripts README/cleanup instructions and release notes. New source files are allowed only as small leaf utility modules required by C03/C06/C07 after checking existing reusable helpers. Their precise names/placement are chosen from the researched dependency graph during task construction, not invented as a reusable platform.

Removed files: only `scripts/publish.sh`, `setup.py` and `MANIFEST.in`, subject to their gates. All other removals are named symbols/configuration sections, not entire modules.

```text
recipe modules -> shared concrete recipe primitives (stdlib only)
tasklist/roadmap validation -> lower-layer text utilities (no reverse roadmap import)
normalize/reduce -> shared concrete byte writer (no pipeline/preflight redesign)
```

### 4.2 Dependency-respecting phases

1. Establish baselines, caller/requirement ownership maps, golden and negative cases, distribution payload manifests and held-surface snapshot. Complete the FR-05 packaging-only paired baseline before any C01–C04/C06–C10 source/test/dependency edits, or use isolated identical snapshots differing only in the two packaging retirements; record the source/dependency snapshot and build-tool versions for both arms.
2. Apply independent scoped changes with per-item verification. Serialize edits sharing normalize.py, recipe modules, pyproject/lock or test files; parallelize only genuinely disjoint files after baselines exist.
3. Run integration/architecture/resource parity checks, full regression and scope review; document candidate outcomes and measured savings.
4. Perform independent final QA and post-execution reflection during future execution. This session performs only the preceding plan's pre-execution reflection.

## 5. Preserved interface and state contracts

No new CLI flags, schemas, data models or environment variables. Existing command/process behavior remains unchanged. The named helper removals intentionally retire disconnected module symbols only after FR-11; existing recipe exports and Reporter.to_* override dispatch remain supported.

### 5.1 State variable registry (preserved, not new application state)

| Variable Name | Type | Initial Value | Invariant | Read Operations | Write Operations |
|---|---|---|---|---|---|
| registry entry | Recipe or None or absent | Existing REGISTRY contents | None differs from absent/invalid; registry is not mutated by fallback | _resolve_recipe | Existing external extension only; no new writes |
| destination bytes | bytes or absent | Existing file state | Complete old or complete successful new payload, never partial | Artifact consumers | Atomic replace only after successful write/fsync |
| temporary path | path or absent | Absent | Same parent as destination; baseline cleanup on failure | Writer and cleanup | mkstemp/create/unlink/replace |
| encoded count | integer >= 0 or not yet computed | Not yet computed until encoding succeeds | Successful writer returns/persists B bytes, not character count C; no success count on exception | Writer result consumers | Compute from supplied bytes after successful encoding; no new persistent field |
| candidate outcome | planning evidence enum: Pending, Complete, Blocked | Pending | Complete requires eligibility+verification; blocked is not complete; failed/skipped checks are evidence results, never completion | Executor/release reviewer | Evidence capture, scoped verification |
| ordered worker records | existing ordered input/output lists | Caller-provided N records; output not yet constructed | On successful return N outputs in the same order; preserve existing failure/salvage transitions and do not mutate inputs | Normalizer and downstream consumers | Existing fresh output construction only |
| sanitizer prefix count and temporary sibling | integer >= 0; path or absent | 0 on no-op; otherwise UTF-8 prefix length and existing sibling filesystem state | Return count/log only after successful replace; fixed .tmp behavior is distinct from atomic writer's unique temporary path | Validator runners and existing caller logger | Existing helper read/write/replace; propagate errors without adding cleanup policy |

Applicability: these are existing runtime transients plus planning evidence, not newly introduced application state, schemas, persisted counters or a state-machine framework. Existing confinement/salvage/contract/sentinel state and held roadmap state readers/writers are preserved, not redesigned. Requirement-bearing helper tests must be mapped to an actual live owner and the migrated assertions must pass before C01/C04/C10 deletion; naming a prospective owner alone does not satisfy FR-11.

### 5.2 Guard boundary obligations

The panel review must enumerate six named guard families in a seven-column boundary table with at least six concrete rows each: G1 deletion eligibility (FR-11), G2 recipe resolution (FR-09), G3 sanitizer no-op/delimiter selection (FR-06), G4 atomic transaction outcome (FR-07), G5 recipe confidence/section/cap policy (FR-03), G6 distribution parity/release readiness (FR-05/FR-12). Cover zero/empty, minimal, typical, maximum/overflow, sentinel and legitimate edge inputs. Every row needs a specified outcome; GAP or blank behavior is at least MAJOR and blocks final synthesis until resolved. These are grouped guard families, not permission to omit an individual branch within a family.

## 6. Non-functional requirements

| ID | Requirement | Target | Measurement |
|---|---|---|---|
| NFR-01 | Supported behavior and serialized-output parity | No unexplained difference for deterministic cases; no weakening of held contracts | Fixed-clock differential/golden tests and integration assertions |
| NFR-02 | Persistence/confinement | Existing atomicity, error propagation and output-root boundaries preserved | Failure injection, atomicity/confinement tests |
| NFR-03 | Architectural simplicity | Zero new runtime dependencies, no new framework/config knobs, no cycles/reverse pipeline import | Diff/import/architecture review |
| NFR-04 | Requirement coverage | Every affected requirement retained on a live owner or deletion blocked | Candidate eligibility matrix and targeted tests |
| NFR-05 | Distribution parity | Packaging-only paired scope/payload parity; final-release deltas individually attributed to authorized candidates/metadata, unrelated resources unchanged; installed resources/entry points preserved | Paired baseline/post and final delta manifests/hashes, direct-versus-sdist-wheel comparison and isolated install |
| NFR-06 | Honest release evidence | All checks have command/context/result; blocked/skipped/failed are distinct from PASS | Traceability and final independent review |

## 7. Risk assessment

| Risk | Impact | Mitigation |
|---|---|---|
| Test-only helpers encode requirements not actually covered elsewhere | High | FR-11 blocks deletion until assertion ownership/migration is demonstrated; no blanket deletion |
| Public imports or monkeypatch seams change through consolidation | High | Retain existing recipe/helper names and effective seams; tiny adapters only where needed |
| Shared utility introduces reverse import/cycle | Medium | Leaf placement and architecture test; no pipeline import of roadmap |
| Atomicity assertion depends on source location rather than transaction | High | Preserve mechanical guarantees and update assertion to trace shared implementation, not weaken it |
| Packaging silently loses non-Python assets | High | Before/after payload hashes plus wheel-from-sdist isolated install and resource checks |
| Lock refresh upgrades unrelated packages | Medium | Minimal lock delta; preserve Ruff pin and report unavoidable metadata changes |
| Savings target drives unsafe scope growth | High | Estimates are informational; no extra deletion to compensate for lower measured savings |

## 8. Test plan and acceptance evidence

The implementation tasklist must name concrete cases, expected results and evidence paths per item. Existing test files below are starting points, not claims that every required case already exists or has passed.

| Requirement | Existing test locations / required verification |
|---|---|
| FR-01 | tests/cli_portify/test_monitor.py (retain timing/output/convergence classes), test_logging.py, test_diagnostics.py, test_executor.py; explicit requirement-ownership migration |
| FR-02 | Read-only reference search over active scripts/docs/automation and preserved publishing workflow; no publishing invocation |
| FR-03 | tests/swarm/test_recipe_bare_review.py, test_recipe_findings_table.py, test_recipe_hypothesis_table.py, test_recipe_verdict_only.py, test_recipe_no_judging.py, test_bare_review_parity.py, test_bare_review_golden_regen.py |
| FR-04 | tests/cli_portify/test_failures.py (retain registered handlers/timeouts/registry/NFR assertions), test_validate_config.py, test_config.py, test_brainstorm_gaps.py; live boundary cases |
| FR-05 | Baseline/post normalized archive payload manifests/hashes; isolated wheel-from-sdist install, both entry points, pytest plugin, installer/component resources |
| FR-06 | tests/roadmap/test_embed_inputs.py, test_executor.py, test_validate_executor.py, test_nfr_compliance.py; tests/tasklist/test_tasklist_fidelity.py, test_tasklist_cli.py; byte-count/no-op/error/logging cases |
| FR-07 | tests/swarm/test_imm6_atomic_write.py, test_nfr002_atomicity.py, test_output_confinement.py, test_normalize.py, test_reduce.py, test_contract_emission.py, test_done_sentinel.py, test_three_layer_artifacts.py; injected failure cases |
| FR-08 | Locked dev resolution, minimal lock diff and unchanged Ruff checks; baseline allowance retained |
| FR-09 | tests/swarm/test_normalize.py, test_recipe_passthrough.py, test_recipe_registry.py, test_parse_error_salvage.py |
| FR-10 | tests/pipeline/test_integration_decompose.py retargeted to actual decomposition function; empty/nonbehavioral/order/idempotence preserved |
| FR-11–12 | Eligibility/traceability matrix, architecture review, full pytest run, Ruff lint/format, packaging evidence, explicit held-surface diff check, final independent review |

All Python tooling uses UV. Commands must be verified against current tool help/config before execution. No real model/API calls or publishing are required to prove these refactorings; retain isolated/mocked boundaries where applicable. Any proposed live service/network action beyond dependency/build isolation requires separate authorization.

## 9. Migration, rollback and release readiness

The supported runtime behavior is unchanged; discontinued disconnected helper imports and the inactive local publishing/setuptools entry surfaces are documented explicitly. Do not claim universal backward compatibility for intentionally retired entry points.

For each candidate, retain pre-change baseline evidence before editing. If parity/coverage checks fail, stop that candidate and report it; restore only that candidate's edits if a rollback is authorized, never reset unrelated work. No blanket git reset/clean, artifact purge or worktree deletion is part of the task.

Release readiness requires all in-scope requirements demonstrated, independent review complete, no new regression and all exceptions explicit. A blocked candidate means the specified release is not ready; a scope reduction needs an explicit decision. Publishing or semantic-version assignment is not implied.

## 10. Downstream plan contract

Use `/task-builder` to create a single MDTM tasklist package for this specification, with per-file/component checklist granularity and a dependency-respecting phase sequence. The generated tasklist must carry the spec path, worktree root, baseline commit, held/rejected fences, acceptance cases, UV-only tooling and candidate eligibility gates. Encode required QA and post-execution reflection without running them during planning.

Then invoke `/sc:reflect --mode pre` with this spec and the actual generated tasklist. Correct planning artifacts for verified pre-review gaps and rerun bounded validation as required. Do not execute implementation tasks. A pre-review PASS means plan coverage, not a claim that the release has shipped or runtime tests have passed.

## 11. Open decisions and scope policy

No unresolved product decision is required to construct the plan. The release uses a codename because the user did not specify a semantic version. Eligibility, packaging parity and supported-consumer checks are explicit implementation gates, not assumptions that evidence already passed. Held proposals stay held until a separately authorized follow-up resolves their contracts.

## 12. Review status

Reviewed by the eleven simulated expert perspectives in sibling `spec-panel-review.md`; guard families G1–G6, state applicability and quantity-flow obligations are documented there. Status: **ready for task planning; implementation eligibility and release verification pending**. Narrow ambiguities were corrected and re-reviewed; no unresolved planning blocker was identified in this bounded pass. No tests/builds or implementation tasks were run and no deletion is proven safe by this review. All implementation checklist items remain unchecked; future candidate blockers must be surfaced under FR-11 rather than treated as PASS.
