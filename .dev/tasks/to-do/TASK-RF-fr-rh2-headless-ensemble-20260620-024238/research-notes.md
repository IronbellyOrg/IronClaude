# Research Notes: Implement FR-RH2 (sc:reflect Tier-2 reviewer ensemble via swarm dispatch library)

**Date:** 2026-06-20
**Scenario:** A (explicit — spec + TDD provided as acceptance oracle + design)
**Depth Tier:** Deep (HIGH complexity 0.82; cross-subsystem cli/reflect + cli/swarm + tests; 9 FRs + 8 NFRs; strict §4.6 order with a BLOCKING gate)
**Track Count:** 1 (single cohesive feature with sequential §4.6 dependencies)
**Status:** Complete

**Driving documents:**
- SPEC (acceptance oracle, spec wins on wording conflict): `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md` (FR-RH2.1..FR-RH2.9, NFR-RH2.1..NFR-RH2.8, §4.6 impl order, §5.3 phase contracts + (M,N) guard table)
- TDD (governs file paths, signatures, §15 test matrix): `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md` (§6 architecture, §7 data models, §8 signatures + §8.3 OI-1 table, §15 test matrix, §22 open questions, §23.2 phases)

**Build constraints (from user GOAL):**
- Tasks MUST cite spec-literal acceptance criteria + the §5.3 (M,N) table / phase contracts verbatim.
- Spec wins on any wording conflict; TDD governs file paths, signatures, §15 test matrix.
- Follow §4.6 implementation order.
- Resolve §22 Q1 (OI-1 BLOCKING) and Q6 (ensemble-empty vs FR-RH2.7) BEFORE FR-RH2.3 code.

---

## EXISTING_FILES

**Reflect package (`src/superclaude/cli/reflect/`) — verified present, exactly 6 files (ensemble.py ABSENT → NET-NEW):**
- `runner.py` — `_audit_once` (TDD: L392-428; seam L405-419; `expected_tier` L403), `_build_prompt` (L341-366), `run()` fix-loop, `write_reflect_post` (FR-6 fail-closed L588-590), `write_sidecar`
- `contract.py` — `derive_verdict` (ordering blocked→degraded→halted→pass), `_degraded_reason` (trigger 7 diversity L267-269, 8 vendor L272-273, 9 adversarial-unavailable L276-277, 10 single-reviewer-fallback L280-281, 11 null-convergence L284-285, 12 verification, 13 citations, 14 input-drift), `_halted_reason`, Stage-1 BLOCKED guards (contract_version L166-181, child_rc L148-159), `parse_contract` (L65), `_make_result` (L104-127)
- `config.py` — `resolve_config` (L123-240); needs `--transport`/`--reviewers` resolution
- `models.py` — `ReflectConfig` (L57-91; `contract_path` property L88-91), `ReflectResult` (L94-121), `Verdict` enum (PASS=0/HALTED=10/DEGRADED=11/BLOCKED=2)
- `commands.py` — `reflect run` Click group (docstring L49-61 "so Tier 2 fans out"); `--depth` exists (L101-106); `_DEFAULT_MODEL="claude-opus-4-8"`
- `__init__.py`

**Swarm package (`src/superclaude/cli/swarm/`) — verified present:**
- `dispatch.py` — `dispatch_wave1` (L334-343; kw-only after `transport`; returns `list[WorkerResult]` len N; `transport_for_slot` precedence L453-457; synthesized proxy_error backstop L484-490; early exits L409-414; `executor.quiet=True` L425)
- `commands.py` — `_resolve_run_transport_factory` (L612-707; PRIVATE symbol — Q7 coupling smell), `ModelPoolTooSmallError` (L589-609, L687-688), `read_env` pool binding slot i→pool[i%len]
- `reduce.py` — `reduce_wave3` (L555; M=`workers_succeeded` L648, N=`effective_n` L650-653, `determine_status` IMM-5 floor=2), `emit_contract` (L369-394), `emit_done_sentinel` (L402-459)
- `merge.py` — `mechanical_merge` (L50, 7 LOC, ≤30 ceiling; DISALLOWED sort/rank/score/judge/dedup L9-30)
- `models.py` — `WorkerResult` (DM-013, L1027, 12 fields, `WorkerStatus` enum L69, `__post_init__` L1130-1136), `ResultContract` (DM-012, frozen L877), `DoneSentinel` (DM-017, L1424), `LensEntry` (DM-010, L637, 14 fields)
- `lenses/bare_review.py` — LENS precedent (suspect=True, tier="T2", `/sc:adversarial` next-command, `{suspect_files}`)
- `lenses/__init__.py` — registry (3 edit points per TDD L49-67/L73-82/L105-114)
- `lenses/_validate.py` — lens validator (assertions 2=recipe∈REGISTRY, 6=normalizer_strategy∈STRATEGIES)
- `lenses/templates/feasibility-probe-output.md`, `bare-review-output.md` — template precedents
- `recipes/__init__.py` — `REGISTRY` (L181, has `bare-review-v1`), `STRATEGIES` (L208, has `bare-review-v1`)
- `schema.py` — `CANONICAL_INJECTION_GUARD_SENTENCE`
- `transports/stub.py` — `StubTransport` (network-free, stdlib hashlib/threading, `del timeout`, always success L122-159)
- `transports/openai_compat.py` — `read_env` (L159), `send` status mapping (L329-382), `/chat/completions` append (L122), `TransportEnvError` (L187-196)

**Test infrastructure (`tests/cli/reflect/`, `tests/swarm/`) — verified present:**
- `tests/cli/reflect/conftest.py` — `make_claude_process_stub` (L98-138; THE MOCK GAP — copies canned fixture)
- `tests/cli/reflect/fixtures/pass.yaml` (L4 `tier_reached: 2` hard-coded constant)
- `tests/cli/reflect/test_no_nesting_guard.py` — Layer A (skill shell-out) + Layer B (runner imports L95-102)
- `tests/cli/reflect/test_verdict_mapping.py` (B1, 276 L), `test_runner_e2e.py` (B2, 220 L), `test_writeback.py` (B3, 172 L)
- `tests/swarm/test_commands_run.py` — stub-integration precedent (L507-568 `test_run_cmd_stub_transport_dispatches_workers_not_noop`)
- `tests/swarm/test_merge_mechanical_only.py`, `test_merge_loc_ceiling.py` (TDD references — confirm exact names), `test_inv005_pool_guard.py`, `test_bundled_lenses.py`, `test_lensentry.py`

## PATTERNS_AND_CONVENTIONS
- UV-only Python; `uv run pytest`, `uv run ruff format --check src/ tests/`
- Source-of-truth: lens/skill changes in `src/superclaude/`; `make sync-dev` → `.claude/`; `make verify-sync` before commit
- Reflect package isolation guardrails (`runner.py` L8-12): NO `async`/`await`, NO `Task(`/`subagent_type`, NO raw `subprocess.run`/`Popen`, NO `cli.sprint`/`cli.roadmap` import. ONLY launch = `ClaudeProcess`/subprocess (NFR-7).
- Swarm reuse-by-import: all three seam symbols are plain synchronous `def`s routing through `ParallelExecutor`+`Transport`.
- Verdict identity checks use strict `is True`/`is False` (not truthiness); first-match-wins ordering.
- New `ReflectConfig` fields append at the dataclass tail after `max_fix_iterations` (3-file chain: models.py → config.py → commands.py).

## GAPS_AND_QUESTIONS (to be ground-verified by researchers)
- Confirm exact line anchors the TDD cites still match shipped source (TDD claims "Last Verified 2026-06-20"; today = 2026-06-20, fresh — but VERIFY, do not trust).
- Q1 (OI-1 BLOCKING): the §8.3 swarm→reflect field-correspondence table is PRODUCED but must be VALIDATED against shipped diff before FR-RH2.3 code. Confirm which reflect verdict-driver fields are truly absent from swarm DM-012.
- Q6 (human-decision): `ensemble-empty` slug does NOT exist in `contract.py` today (grep returns 0). Option A (add new BLOCKED branch — amends FR-RH2.7 "derive_verdict unchanged") vs Option B (map onto existing BLOCKED trigger — preserves FR-RH2.7 literally). TDD: "Must be explicitly chosen and recorded." → human-decision item, HALT, do not auto-apply.
- Q7: `_resolve_run_transport_factory` is private; confirm import-shape stability concern.
- Q8: `--reviewers 1` must pass-through-to-degrade (NOT clamp to 2); branch the `1` sentinel BEFORE the `max(2,min(4,n))` clamp.
- Exact swarm merge boundary test filenames (`test_merge_mechanical_only.py` confirmed; verify `test_merge_loc_ceiling.py`).

## RECOMMENDED_OUTPUTS
6 researcher files in `research/`, each ground-verifying a slice with file:line evidence:
- `01-reflect-package-runner-config-models.md`
- `02-contract-derive-verdict-triggers.md`
- `03-swarm-seam-dispatch-commands-reduce.md`
- `04-swarm-lens-precedent-registry-recipes.md`
- `05-transports-proxy-contract.md`
- `06-test-infrastructure-mock-gap.md`

## SUGGESTED_PHASES (researcher assignments)
- R1 (File Inventory + Patterns): reflect package — runner.py seam/_audit_once/_build_prompt/run/write-back, config.py resolve_config, models.py ReflectConfig/ReflectResult/Verdict, commands.py Click surface. Verify all line anchors. Output 01.
- R2 (Integration Points): contract.py — derive_verdict ordering + every _degraded_reason/_halted_reason trigger + Stage-1 BLOCKED guards + parse_contract/_make_result; grep `ensemble-empty` (Q6). The OI-1 left-column fields. Output 02.
- R3 (Data Flow Tracer): swarm seam — dispatch_wave1/_resolve_run_transport_factory(+ModelPoolTooSmallError)/reduce_wave3 signatures + mechanical_merge boundary + models.py DM-012/DM-013/DM-017/DM-010. Output 03.
- R4 (Template & Examples): bare_review.py lens + lenses/__init__.py registry edit points + recipes REGISTRY/STRATEGIES + _validate.py validator (assertions 2&6) + CANONICAL_INJECTION_GUARD_SENTENCE + feasibility-probe-output.md template. Output 04.
- R5 (Integration Points): transports — stub.py + openai_compat.py (read_env, send status mapping, /chat/completions, TransportEnvError) + Transport base; NFR-RH2.8 no-forbidden-literal grep. Output 05.
- R6 (Test & Verification): conftest mock gap + pass.yaml + test_no_nesting_guard.py Layer A/B + B1/B2/B3 regression floor + tests/swarm/test_commands_run.py stub precedent + merge boundary tests + inv005 pool guard. Output 06.

## TEMPLATE_NOTES
- MDTM Template 02 (Complex): discovery-resolved-gates → build → test → QA → reflect phases; conditional flows (Q6 human-decision HALT); per-phase verification.
- Tier: Deep.
- QA_GATE_REQUIREMENTS: PER_PHASE (multi-phase infra build).
- TESTING_REQUIREMENTS: UNIT + INTEGRATION (the §15 matrix is the test contract; U1-U9 unit, I1-I9 integration, B1-B3 backward-compat).
- POST_REFLECT_GATE: ENABLED (flat wrapper shell-out, penultimate final-phase item).
- spec_path: `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md` (threaded into PRE reflect gate).

## AMBIGUITIES_FOR_USER
- Q6 (ensemble-empty slug) is a genuine human-decision with FR-RH2.7 scope impact. Per project policy (human-decision items must HALT, not auto-default), the task file will encode Q6 resolution as a BLOCKING decision item that writes PENDING and halts FR-RH2.3/FR-RH2.9 wiring until resolved — it will NOT silently pick Option B. The TDD leans toward Option B (preserves FR-RH2.7 literally) but states "Must be explicitly chosen and recorded."
- Q1 (OI-1) resolution is substantively produced (§8.3 table); remaining action is validation against shipped diff — encoded as a verification gate, not a decision.
- Otherwise intent is clear from the spec + TDD.
