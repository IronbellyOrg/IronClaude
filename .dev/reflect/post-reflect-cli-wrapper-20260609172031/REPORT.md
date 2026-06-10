# Reflect Report — POST (UC-2) — `superclaude reflect run` CLI wrapper

- **Mode:** post · **Tier reached:** 2 (forced by `--depth deep`; regression candidate also forced T2 per §5.3 rule 3)
- **Diff:** `b05e0fe1..HEAD` → single commit `015e7285` (23 files, +2409/-1)
- **Tasklist:** `TASK-RF-20260608-185553` (`.dev/tasks/to-do/`, frontmatter `status: 🟢 Done`)
- **Spec:** `merged-requirements.md` (FR-1..FR-12, NFR-1..NFR-8, §6, §8, §11)
- **Status:** `partial` · **Calibrated confidence:** 0.82 · **needs_human_decision:** true
- **Promotion:** skipped (gate-failed — status≠success, regression>0)
- **Evidence-validator:** ran (14/14 citations re-Read, 0 dropped)

---

## Verdict

The implementation is **high quality and largely conformant** — the verification triangle reproduces every claim in the task log (35 tests pass, ruff check + format clean on the package, `verify-sync` clean, 152 prd tests no-regression, real CLI registration works end-to-end), and the central fail-closed machinery is genuinely present and correct on every path the three reviewers stress-tested. The thinness/no-reflect-logic-duplication property (NFR-1) holds, the §8 prompt is faithful, and the no-nesting guarantee (FR-1/NFR-7) is real.

**However, one HIGH fail-closed gap and one MEDIUM cross-artifact softness require a human decision before this gate can be called green.** Per §11.2 this is the expected outcome of a genuine audit — the headline finding was caught only by the third (correctness) reviewer and independently re-verified against the spec text and source, not assumed.

---

## Findings (full register: `deviation-register.yaml`)

### 🔴 F0 — HIGH (regression vs §6) · needs human decision

**A non-zero child exit (≠124) with a present `status:success`/tier-2 contract can reach PASS (exit 0).**

- `contract.py:128-136` routes a non-zero `child_rc` to `blocked` **only** when `contract is None`; the timeout case (124) is blocked unconditionally, but any *other* non-zero exit with a parseable contract flows through to the PASS clause (`contract.py:193`). `runner.py:443-453` passes `rc` straight in with no pre-filter.
- **Spec conflict:** §6 row 1 (line 79) lists "**child crash** → blocked exit 2"; the impl honors it only with no contract. FR-5 ("contract-driven verdict", line 25) pulls the other way. The asymmetry is the tell — the author already lets exit-code 124 veto a present contract, but no other crash code.
- **Why it matters:** this is precisely the *silently-degraded-audit-reaches-green* failure the spec's §11 invariant probe exists to prevent. Reachability is bounded (needs a complete success contract to coexist with a crash exit), but the consequence is the worst the gate can produce.
- **Fix (recommended, fail-closed):** mirror the 124 handling —
  `if child_rc != 0: return _make_result(Verdict.BLOCKED, reason="child-crash", contract=contract, child_rc=child_rc)` immediately after the timeout check. If the contract-driven reading is *intended*, make that explicit in §6 and document why a present success contract overrides a crash exit.

### 🟠 F3 — MEDIUM (design-acknowledged softness) · needs human decision

**task-builder omits `start_commit` + `executor_model_class` from generated frontmatter → the wrapper arm's executor-disjoint guarantee is soft.**

- The frontmatter template writes only `spec_path:` (`SKILL.md:1948`). The wrapper reads `executor_model_class` from frontmatter (env-first, `config.py:50-56`), so in the common path `--executor-model` is **omitted** unless `EXECUTOR_MODEL_CLASS` env is set. Reflect then emits `executor_class_resolved: false` + a "anti-self-confirmation weakened" WARN — and that field is **not** in the wrapper's FR-11 degraded set, so a wrapper-arm POST gate can pass green while reflect ran with a weakened executor-disjoint guarantee (the spec's central thesis, §1/§11).
- FR-3 designs both keys as optional-with-fallback (OQ1/OQ2), so this is **not a spec violation** — but it is a genuine end-to-end softness worth closing.
- **Fix:** either (a) persist `executor_model_class:` (and optionally `start_commit:`) in generated frontmatter, or (b) add `executor_class_resolved==false` to the wrapper's FR-11 degraded set.

### 🟡 MEDIUM / LOW (robustness + hygiene — fix in remediation, none block on their own)

| ID | Sev | Finding | File |
|----|-----|---------|------|
| F1 | MEDIUM | CRLF tasklist false-negative: write-back `_FRONTMATTER_RE` doesn't normalize `\r\n` (canonical `extract_frontmatter` does) → clean PASS downgraded to BLOCKED on a CRLF file. Fail-closed; LF-only generators make real-world hit low. | `runner.py:44,131-135,465-467` |
| F2 | MED-LOW | Malformed-but-truthy load-bearing booleans (`regression_present: "true"`) bypass `is True` triggers → could reach PASS. Real producer emits proper bools, so low likelihood. | `contract.py:234,259,269-276` |
| F4 | LOW | FR-7 "sidecar always written" violated on the config/preflight-STOP path (`sys.exit(2)` with no `wrapper-result.yaml`). | `commands.py:145-148` |
| F5 | LOW | `status:failed` → halted with misleading reason `tier-mismatch` (exit code correct/fail-closed; only the slug misleads). | `contract.py:265-282` |
| F6 | LOW | Dry-run `claude` argv preview drifts from real `build_command()` (missing `--no-session-persistence`/`--tools default`, reorder). Preview-only; prompt string is accurate. | `runner.py:340-347` |

### ✅ Refuted (false positive caught by the ensemble)

- **R1 — strict tier equality (`tier_reached==expected_tier`) rejecting clean `tier_reached:3`:** raised by the QA lens, **refuted** by the correctness lens. The wrapper never sends `--remediate`, so reflect Tier-3 cannot fire; `tier_reached` is only ever 1/2. A hypothetical T3 contract HALTs (fail-closed), not a pass-leak. `>= expected_tier` hardening is optional.

---

## Coverage — FR/NFR → evidence (all verified)

- **FR-1 / NFR-7 (top-level launch, no nesting):** ✅ sole launch path is `ClaudeProcess` (`runner.py:432-443`), `env_vars=None`; zero async, zero Agent/Task surface; two-layer no-nesting guard test present + green.
- **FR-2 / NFR-1 (thinness, no reflect-logic duplication):** ✅ wrapper reads contract fields only; 1368 raw LOC is docstrings/comments + the FR-11 field-reading table, not duplicated reflect logic (verified by spec-conformance lens).
- **FR-3 (input derivation):** ✅ base chain (`start_commit`→`merge-base HEAD master`→fail), depth-floor quick→standard, spec only-when-one-file, executor-model env-first. (See F3 for the builder-side persistence gap.)
- **FR-4 (pinned output + `.claude` STOP):** ✅ `config.py:96-103,199-203`.
- **FR-5 / §6 (contract-driven 4-state verdict):** ✅ ordering blocked→degraded→halted→pass; version gating (unknown major→blocked); **except F0** (child-crash row).
- **FR-6 (atomic race-safe write-back):** ✅ splice preserves body + sibling keys byte-for-byte (QA lens ran 9 input shapes), randomized same-dir temp + `os.replace`, compare-before-write race guard; **except F1** (CRLF).
- **FR-7 (dual gate signal):** ✅ exit code + `reflect_post` + sidecar; **except F4** (config-STOP path).
- **FR-8 (fail-closed HALT):** ✅ only PASS exits 0; halted 10 / degraded 11 / blocked 2; PASS→BLOCKED downgrade on unwritable frontmatter (`runner.py:465-467`).
- **FR-9 (audit-only default):** ✅ `--no-promote` is a hard prompt flag (`runner.py:328-329`).
- **FR-10 (headless env parity):** ✅ bare `ClaudeProcess.build_env()` real-env overlay (pops nested-session vars, preserves MCP + `ANTHROPIC_DEFAULT_*`); not `HomeIsolation`.
- **FR-11 (fail-closed degradation, 14 triggers):** ✅ all present; exact-membership chain-critical set; `serena_summary_corroboration: unavailable` correctly NOT a halt; T1-null guards correct. (See F3 for the `executor_class_resolved` gap relative to the central thesis.)
- **FR-12 (dry-run):** ✅ ClaudeProcess never constructed in the dry-run/print path.
- **§11 invariant probe:** ✅ the gate VERIFIES non-degraded Tier-2 from the contract (tier==2, model-diversity==full, non-null adversarial merge, verification_ran) rather than assuming sufficiency from "subprocess launched" — **except the F0 child-crash hole, which is one path that can bypass it.**
- **task-builder (NFR-3 reversibility):** ✅ strictly additive; halt arm byte-identical when `POST_REFLECT_MODE` unset.

---

## Verification triangle (auditor-reproduced — not task-log self-report)

| Check | Result |
|-------|--------|
| `pytest tests/cli/reflect/` | **35 passed** |
| `ruff check` (package + tests) | All checks passed |
| `ruff format --check` (package + tests) | 14 files already formatted |
| `pytest tests/cli/prd/` (registration regression) | **152 passed** |
| `superclaude reflect run --help` (real CLI registration) | all §9 options present; `reflect` under `superclaude --help` |
| ClaudeProcess / extract_frontmatter integration seams | confirmed (kwargs-only ctor accepts every kwarg used; `extract_frontmatter` returns scalars → runner's own nested parser is consistent) |

**Branch note (Necessary / documentation):** full-tree `ruff format --check src/ tests/` is RED on **2 pre-existing files** (`tests/cli/prd/test_executor.py`, `tests/cli/prd/test_resolve_step_content.py`, committed in #147) — confirmed **not** in this diff. The task log already flagged this as a non-blocking follow-up. CI format-check on this branch will fail until those 2 files are formatted, independent of this work.

---

## Deviation classification (§10)

- **Authorized:** 0
- **Necessary:** 2 (documented executor build-time deviations — FR-12 alias-count relocation; the `ANTHROPIC_MODEL` model-source seam — both verified sound; plus the within-scope robustness gaps F1/F2/F4/F5/F6 surfaced as recommendations)
- **Drift:** 0 (every diff hunk maps to the spec/tasklist; no unauthorized silent scope)
- **Regression:** 1 (F0 — contradicts §6 row 1 for the child-crash case)

---

## Tier-2 ensemble & calibration

- Reviewers (executor=opus excluded per §7.1): **3 heterogeneous lenses** — correctness/verdict-map, edge-case/atomicity, spec-conformance/thinness. Vendor diversity: multi (claude + gpt-5.5 + qwen aliases). `t2_model_class_diversity: degraded` recorded honestly — per-subagent resolved model class was not independently verified; heterogeneity is by agent-persona/lens.
- Blind calibration (independent `confidence-calibrator`, class disjoint from reviewers): overall 0.81; flagged F6→inflated (downgraded to LOW follow-up). Headline F0 independently re-verified by the auditor against source + §6 text.
- Merge: orchestrator inline-synthesis across 3 cards + 1 calibrator (the formal `sc-adversarial` skill was not invoked; recorded in the contract).

---

## Bottom line

Ship-quality wrapper with a real, well-tested fail-closed spine. **Two items need a human decision** (F0 child-crash semantics; F3 executor-model persistence), and five LOW/MEDIUM robustness items are worth folding into the same remediation pass. Recommend addressing F0 + F3 before flipping the wrapper template to `POST_REFLECT_MODE: wrapper` as a default, since both touch the executor-disjoint / fail-closed guarantees that are the wrapper's entire reason to exist.
