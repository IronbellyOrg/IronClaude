# /sc:reflect — Post-Execution Deviation Audit (UC-2, Tier 2)

**Task:** TASK-RF-tavily-mcp-0-2-x-20260623-010952 — Tavily MCP Upgrade to `tavily-mcp@0.2.20` across 8 clusters
**Mode:** post · **Tier:** 2 (forced by `--depth deep`) · **Executor class:** sonnet (excluded from reviewer pool)
**Audit base:** `530505a0` (== HEAD; work is **uncommitted in the working tree**)
**Verdict:** ✅ **PASS** · **Calibrated confidence:** 0.93 · **Convergence:** 0.92
**Deviations:** `{authorized: 0, necessary: 2, drift: 0, regression: 0}` — **0 blocking**

---

## 1. Diff-scope resolution (Wave 0 footgun guard)

The `--diff 530505a0...` ref is a single commit SHA, and `HEAD == 530505a0`, so `530505a0..HEAD` is **empty**. The entire Tavily upgrade is **uncommitted in the working tree** (`dirty=22M`). The audited delta is therefore `git diff 530505a0` (working tree), matching the executor's intended `start_commit`-vs-worktree base.

- **Implementation scope** = `src/ docs/ tests/ plugins/` = **29 files** (924 insertions, 54 deletions).
- ~90 additional `.dev/` files in the worktree (brainstorms, tasklists, research, qa, phase-outputs) are process artifacts, **not** implementation, and are excluded from deviation analysis.

## 2. Cross-cluster invariant conformance (X1–X7)

All seven invariants **HOLD**, independently grep- and test-verified against the live working tree (not just the diff):

| Inv | Statement | Verdict | Evidence |
|-----|-----------|---------|----------|
| **X1** | Version pin `tavily-mcp@0.2.20` everywhere in scope | ✅ HOLD | Live grep `src/`+`docs/`: exactly 4 `tavily-mcp@` occurrences, all `0.2.20` (`install_mcp.py:81`, `MCP_Tavily.md:5`, `real.yaml:1630`, `mcp-servers.md:274`). Zero `0.1.2`/`@latest`. |
| **X2** | Single config source; orphan `tavily.json` DELETED | ✅ HOLD | Both `src/superclaude/mcp/configs/tavily.json` AND `plugins/superclaude/mcp/configs/tavily.json` deleted (git `D`). `find` → empty. Inventory ref removed from `comprehensive-features.md`. |
| **X3** | `DEFAULT_PARAMETERS={"search_depth":"basic","max_results":10}` injected server-level | ✅ HOLD | `install_mcp.py:85` registry field; `:561-565` compact-JSON injection via `json.dumps(..., separators=(",",":"))`. |
| **X4** | Eval token `mcp_server.tavily` (not stale `mcp.tavily`) | ✅ HOLD | `capabilities.py` registers it; `real.yaml:41`; `models.py` docstrings + `docs/eval/retry.md` fixed. Live grep for stale token (excl. `.com`) → empty. |
| **X5** | map/crawl ONLY in deep-research engine | ✅ HOLD | map/crawl in 6 research-engine files only; **ZERO** in rf-* agents, troubleshoot/reflect/brainstorm/recommend skills. |
| **X6** | Docs POINT to canonical sources, never duplicate param tables | ✅ HOLD | Canonical value lives only at `install_mcp.py:85` + `MCP_Tavily.md`. Consumer docs (`FLAGS.md:72`, `research.md`, `mcp-servers.md`, `comprehensive-features.md`) point, don't restate. |
| **X7** | Frontmatter↔prose parity for every `mcp__tavily__*` id | ✅ HOLD | Both deep-research agents: all 4 ids in both `tools:` frontmatter AND prose. Parity test passes. |

## 3. Verification triangle (independent of executor self-report)

Re-run by the auditor, not trusted from the task log:

- **`pytest` on all 8 Tavily test files:** **27 passed, 1 skipped** (live smoke, expected) — exit 0.
- **`make verify-sync`:** exit 0 (sync discipline holds; `src/` is sole edit surface, `.claude/` regenerated not hand-edited).
- **`superclaude eval describe --suite real`** (per task log) + independent re-check: `E16` + `mcp_server.tavily` capability render; SKIP cleanly without key.
- **Exit-code taxonomy:** 0 non-zero exits classified as Regression → `verification_regressions_detected: 0`.

## 4. Deviation classification (4-category taxonomy)

### D1 — Eval id `E-tavily-search` → `E16` · class: **NECESSARY** · non-blocking

The tasklist (Step 4.2) specified eval id `E-tavily-search`; the executor shipped `E16`. Independently verified all three sub-claims:

- **(a)** The FR-SCH2 eval-id regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$` **empirically rejects** `E-tavily-search` and **accepts** `E16` (hyphens forbidden; `validate_eval_id` raises `InvalidEvalId` → exit 2). Step 4.5's mandatory `eval describe` would have been impossible with the hyphenated id — the spec asked for an id the schema rejects.
- **(b)** `E16` is correctly wired: `real.yaml:1621-1644` — `requires: [mcp_server.tavily]`, `expect_tool_call: mcp__tavily__tavily-search`, exit 0; descriptive name preserved in `title`.
- **(c)** Rationale documented inline: `real.yaml:1635-1638` 4-line comment naming the regex + exit-2 failure mode.

Classified **NECESSARY** (forced by a real schema constraint, documented inline, contradicts no acceptance criterion — the criterion was "a capability-gated tavily-search verification eval that SKIPs without a key," fully satisfied; the literal id string was not an invariant). The task log records user approval via AskUserQuestion → were that corroborated by an independent transcript it would be **AUTHORIZED**; the class change has **no gate effect** (both non-blocking). The adversarial reviewer's conservative downgrade is adopted.

### D2 — `tests/cli/eval/test_capability_gates.py` roster expectation updated · class: **NECESSARY** · non-blocking

The M2 mandatory registration of `mcp_server.tavily` in `_DEFAULT_CAPABILITY_SPECS` necessarily broke the pre-existing frozen-roster set-assertion. The fix adds `mcp_server.tavily` to the expected set and updates the `3 MCP`→`4 MCP` docstring. **Strengthens** the regression test (updates ground truth; does not no-op the assertion). Documented; contradicts nothing.

### Drift / Regression hunt

- **Drift: 0.** Every one of the 29 implementation files maps to an explicit tasklist item or is a NECESSARY consequence (D2). No unmapped, unrationalized change found.
- **Regression: 0.** The only regression-shaped event — the C8 drift-guard `test_tavily_doc_alignment.py` scanning **0 files** because `_iter_text_files` excluded on the *absolute* path's `.dev` ancestor (the worktree itself lives under `.dev/worktrees/`) — was **self-caught by the executor's own QA lens via mutation testing (Step 7.2) and remediated in Step 7.3** (`p.relative_to(root).parts`). Independently re-verified: the function now scans 911 files; full suite 45 passed / 1 skipped; a reverted `@0.1.2` now correctly FAILS the test. The vacuous-green state never shipped → does not block.

## 5. Evidence-validator gate

- **Citations:** 18 total, 18 re-validated, **0 dropped**, 0 inferred, `full_reread`.
- Zero-drop is normally an audit flag (§11.2), but here mitigated: every load-bearing citation (X1–X7 greps, M1 masking `install_mcp.py:631-638`, M4 doc `MCP_Tavily.md:68-79`, E16 block, regex behavior) was **re-executed/re-Read directly by the orchestrator**, not trusted from reviewer cards.

## 6. Tier-2 ensemble (heterogeneous reviewers)

| Reviewer | Class | Lens | Verdict |
|----------|-------|------|---------|
| rf-qa | haiku | test-assertion strength + completion | PASS |
| root-cause-analyst | opus | invariant conformance + deviation classification | PASS |
| rf-qa-qualitative | opus | X6 anti-duplication + M4 override coherence | PASS |

A 4th reviewer on **fable-5** failed with a 503 auth error (model unavailable); the lens it carried (docs/X6/M4) was re-covered on opus. `t2_model_class_diversity: degraded` (2 distinct classes), `calibrator_diversity: degraded` (inline). Executor class **sonnet excluded** from the pool per the §7.1 anti-self-confirmation rule. All three cards converge on PASS with the same deviation tally → `merge_method: convergent-synthesis`, no adversarial debate required.

## 7. Promotion gate (Wave 7) — **HELD** (default-on, gate-failed)

Adapter `task`. 7 of 9 conditions pass; **2 fail**, both because the task is **legitimately still in its closure phase**:

| Cond | Check | Result |
|------|-------|--------|
| 3 | `tasklist_completion_pct == 1.0` | ❌ 0.95 — Steps 7.4 (this reflect gate) + 7.5 (mark Done) unchecked |
| 5b | frontmatter status == done | ❌ `🟠 Doing`, not `🟢 Done` |
| 1,2,4,5a,6a,6b,7,8,9 | all others | ✅ pass |

**This is NOT executor drift** — the frontmatter accurately reflects in-progress status, and Step 7.4 *is* this audit. Promotion is correctly withheld. Once the operator completes Step 7.5 (`status → 🟢 Done`), all 9 conditions pass and `.dev/tasks/to-do/…` → `.dev/tasks/done/…` becomes eligible.

## 8. Remediation (`--remediate`)

The audit is **clean** — 0 Drift, 0 Regression, 0 grounding gaps. **No remediation task is warranted.** `remediation_task_path: null`.

## 9. Advisory (non-blocking, non-gating)

Three MINOR test-hardening opportunities surfaced by the QA reviewer (defensive only — the tests catch the regressions they were designed for):

1. `test_tavily_eval_capability.py` — assert exactly one `expect_tool_call` in E16 inputs.
2. `test_research_config.py::test_map_and_crawl_tool_ids_present` — assert map/crawl ids sit within the Discovery Routing table, not just present somewhere.
3. `test_tavily_doc_alignment.py` — add a `len(list(_iter_text_files(...))) > 0` guard so a future root-path change can't make the scan vacuously green again.

Out-of-scope/environmental noise confirmed unrelated to this task: broad-tree `ruff check` findings in `swarm/**` (worktree `.venv` ruff vs CI mismatch — memory `reference_ruff_version_mismatch_worktree.md`), and 6 `tests/cli/eval/` failures from missing `.dev/releases/current/cliEval/...` fixtures.

## 10. Bottom line

The Tavily 0.2.x upgrade implementation is **complete, correct, and clean**: all 7 invariants hold, the verification triangle is green, both deviations are documented and non-blocking, and there is no drift or regression. The work is ready for closure — the operator should mark **Step 7.5 (status → 🟢 Done)**, after which the promotion gate passes.
