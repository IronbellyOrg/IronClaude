# Code Review: PR #202 — Tavily 0.2.x upgrade

**Target**: PR #202 — `feat(mcp): pin Tavily to tavily-mcp@0.2.20 + adopt 0.2.x map/crawl across 8 clusters`
**Reviewer**: /sc:auggie-review (depth=standard, focus=all)
**Generated**: 2026-06-23 17:55 UTC
**Source PR**: https://github.com/IronbellyOrg/IronClaude/pull/202
**Base ↔ Head**: `master` (530505a0) ↔ `TavilyUpgrade` (6fa2a730)
**Stats**: 60 files changed (30 reviewable + 30 `.dev/` artifacts), 1578 reviewable diff lines, **8 findings** (4 Auggie findings dropped during grounding)

---

## Summary

**Recommendation: Approve with comments.** No Critical or High findings. The code is correct and the implementation matches the PR's stated invariants (verified: 0.2.20 pin consistency, X7 frontmatter↔prose parity, X3/M4 DEFAULT_PARAMETERS split, deleted-config cleanliness, no leaked secrets). The single substantive item is a **Medium test-robustness gap**: several drift-guard tests iterate file collections without asserting the collection is non-empty — the *exact* vacuous-pass bug class this PR was already bitten by and fixed once (per the PR body), yet the belt-and-suspenders `assert count > 0` was not added, and the sibling test `test_rf_fallback_provenance_present` shows the author already knows the pattern. The remaining items are Low/Nit hardening (one untested branch, one unguarded X5 consumer, a repeated version literal, a stale Node-version doc note).

Two Auggie-reported "security" findings were **dropped after grounding** because their premises were false (see Audit) — a good illustration of why the file:line validation gate exists.

## Findings

### 🔴 Critical (block merge)

_None._

### 🟠 High (should fix before merge)

_None._

### 🟡 Medium (fix in this PR if cheap, otherwise file follow-up)

#### M1. Drift-guard tests lack a non-empty-collection assertion (vacuous-pass risk)
- **File**: `tests/docs/test_tavily_doc_alignment.py:65` (and `:75`, `:87`, `:97`); `tests/agents/test_tavily_tool_parity.py:47` (and `:62`, `:82`)
- **Category**: tests
- **Source**: auggie + grounded
- **Evidence** (`test_tavily_doc_alignment.py:65-72`):
  ```python
  def test_tavily_version_single_pin():
      bad = []
      for p in _iter_text_files(_ROOTS):
          for m in _VERSION_RE.finditer(_read(p)):
              if m.group(1) != "0.2.20":
                  bad.append((str(p.relative_to(_REPO)), m.group(1)))
      assert not bad, f"tavily-mcp pinned to a version other than 0.2.20: {bad}"
  ```
- **Why this matters**: These guards exist **solely** to fail when drift is introduced. If `_iter_text_files()` ever yields 0 files (root rename, a regression in the `relative_to(root).parts` exclusion logic, an env where the dirs don't exist), `bad` stays empty and `assert not bad` passes **silently** — the worst failure mode for a safety net. This PR's own history proves the risk is real: the PR body documents a CRITICAL caught in QA where this same file scanned **0 files** (its dir-exclusion matched a `.dev` ancestor) and passed vacuously. The fix corrected the immediate cause (line 51, `p.relative_to(root).parts`) but did **not** add a positive scan-count assertion, and the same latent gap exists in the two `test_tavily_tool_parity.py` parity tests (which are *additionally* vacuous if zero Tavily refs remain). The fix is known to the author: the sibling `test_rf_fallback_provenance_present` already does `assert rf_files, "expected rf-* agent files to exist"` (`test_tavily_tool_parity.py:96`).
- **Recommendation**: Add one module-level sanity test per file — e.g. `def test_iter_yields_files(): assert sum(1 for _ in _iter_text_files(_ROOTS)) > 100` and `assert _md_files()` — or an inline `assert files, "guard scanned 0 files (vacuous)"` at the top of each guard. Cheap, and it permanently closes the class of bug that already bit this PR once.

### 🟢 Low (nice-to-have)

#### L1. DEFAULT_PARAMETERS injection branch (no API key) is untested
- **File**: `src/superclaude/cli/install_mcp.py:561-565`; `tests/cli/test_install_mcp_tavily.py:71-96`
- **Category**: tests
- **Source**: auggie + grounded
- **Why this matters**: `env_args.extend(["-e", f"DEFAULT_PARAMETERS=..."])` (line 565) fires whether or not the user supplies an API key — `env_args` is pre-initialized to `[]` at line 544, so there is **no crash** on the no-key path (an Auggie hint that this could `UnboundLocalError` was checked and is wrong). But the only propagation test, `test_default_parameters_propagated`, monkeypatches `prompt_for_api_key` to return `"dummy-key-abc123"` (line 76) — the api-key-absent branch (where `env_args` starts empty and DEFAULT_PARAMETERS is the *only* `-e` pair) is a real, newly-added path with no coverage.
- **Recommendation**: Add `test_default_parameters_without_api_key` that patches `prompt_for_api_key` to return `None` and asserts the `DEFAULT_PARAMETERS=...` token still appears in the captured argv.

#### L2. X5 map/crawl confinement is unguarded for `sc-brainstorm-protocol`
- **File**: `tests/skills/test_tier2_tavily_consistency.py:20`; `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
- **Category**: tests
- **Source**: auggie + grounded
- **Why this matters**: Invariant X5 (map/crawl confined to the deep-research engine) is enforced for rf-* agents (`test_rf_no_map_crawl`) and for troubleshoot/reflect (`test_tier2_tool_id_parity`, whose `_ALL_FOUR` list at line 20 is troubleshoot-cmd/skill + reflect-cmd/skill only). `sc-brainstorm-protocol/SKILL.md` **is changed in this PR** but no test asserts it stays free of `tavily-map`/`tavily-crawl`. Current state is correct (manually + grep confirmed it references only search via `/sc:research` delegation), so this is a coverage gap, not a defect.
- **Recommendation**: Add the brainstorm SKILL to a forbidden-token scan (extend `_ALL_FOUR`, or add a dedicated brainstorm X5 test).

#### L3. Version pin `0.2.20` is a repeated literal (shotgun-surgery on bump)
- **File**: `src/superclaude/cli/install_mcp.py:81`; also `src/superclaude/cli/eval/suites/real.yaml:1630`, `tests/cli/test_install_mcp_tavily.py:23,30`, docs
- **Category**: anti-pattern
- **Source**: auggie + grounded
- **Why this matters**: Bumping to `0.2.21` requires editing the literal in ≥4 places. The risk is **mitigated** by `test_tavily_version_single_pin` (which fails on any non-0.2.20 pin in src/+docs), so this is genuinely Low — but a single `TAVILY_MCP_VERSION = "0.2.20"` constant referenced via f-string in the registry command would remove the manual-sync burden for the Python side.
- **Recommendation**: Optional. Extract `TAVILY_MCP_VERSION` in `install_mcp.py` and reference it in both the `command` field and the test assertion; leave docs/YAML guarded by the existing drift test.

#### L4. Stale "Node v16+" guidance contradicts the new Tavily/Auggie 18+ requirement
- **File**: `docs/user-guide/mcp-servers.md:316` (`need v16+`) and `:328` (`Should show v16+`)
- **Category**: docs
- **Source**: auggie (line citation corrected during grounding: Auggie cited `:149`; the real sites are `:139`/`:316`/`:328`)
- **Why this matters**: This PR raises the Tavily requirement to **Node.js 18+** (`:139`, added by this PR; Auggie's "18+" finding was real but mis-cited). The general Troubleshooting/Quick-Fix guidance still tells users `v16+` is sufficient — a user on Node 16 following the troubleshooting steps would believe they're fine while Tavily (and the pre-existing Auggie 18+ entry at `:157`) fail.
- **Recommendation**: Update lines 316 and 328 to note "v18+ required for Tavily/Auggie; v16+ for the rest" (or set 18+ as the documented global minimum).

### 💬 Nits (style / robustness — non-blocking)

- `tests/cli/eval/test_tavily_eval_capability.py:53` — `cap = next(c for c ... )` has no default; if the capability were absent this raises `StopIteration` (a less-legible error than the `assert` on the next line would give). Not vacuous — it still fails. Use `next(..., None)` + `assert cap is not None`.
- `tests/commands/test_research_command.py:42-46` — the per-tier regex assertions would benefit from a leading `assert '| Profile |' in config` table-marker sanity check for clearer diagnostics if the table format changes.
- `tests/core/test_research_config.py:40-43` — `assert len(depth_vals) >= 2` keys on literal `basic`/`advanced` cell matches; a comment documenting the expected table shape (or a header-based check) would make the fragility explicit.

## Architectural / Cross-Cutting Observations

**Verified clean (positive confirmations, grounded):**
- **Single-pin SoT**: `tavily-mcp@0.2.20` is consistent across `install_mcp.py:81`, `real.yaml`, tests, and docs; no lingering `0.1.2` / `@latest` / unpinned for the Tavily server (other servers' `@latest` is intentional). Enforced by `test_tavily_version_single_pin`.
- **X7 parity**: `deep-research-agent.md` / `deep-research.md` declare all four Tavily tools in frontmatter and reference them in prose; enforced bidirectionally by `test_documenting_files_have_exact_parity`.
- **X3/M4 split**: server-level `DEFAULT_PARAMETERS` baseline (`{"search_depth":"basic","max_results":10}`) is injected at install (`install_mcp.py:561-565`) and the per-call `search_depth: advanced` override is confined to troubleshoot Tier-2; both tested.
- **Deleted-config cleanliness**: both `tavily.json` files removed with no dangling references (cross-checked; guarded by `test_no_tavily_json_references`).
- **No secret leakage**: `.secrets.baseline` diff is 9 `line_number` shifts + 1 `generated_at` timestamp, **0 new `hashed_secret`**. API-key masking in echoed install commands is implemented and tested (`test_api_key_never_in_logged_command`).

**Theme**: the only systemic gap is **guard robustness** (M1, L1, L2) — the PR adds a strong drift-guard test suite, but the suite's own non-empty/coverage invariants are applied inconsistently (some tests guard, sibling tests don't). Closing M1 + L2 would make the safety net self-protecting.

## Audit

- Auggie chunks: 3 (code, tests, content) — all succeeded, exit 0, no retries, all JSON unwrapped cleanly.
- Auggie raw findings: 17 findings + 8 cross-cutting. After grounding: **8 kept** (1 Medium, 4 Low, 3 Nit), **4 dropped**, remainder were positive "clean" confirmations folded into the section above.
- **Dropped during grounding** (why):
  1. *DEFAULT_PARAMETERS shell-injection (Auggie: Medium/security)* — **premise refuted**. `_run_command` applies `shlex.quote(str(arg))` to every arg on the POSIX/`shell=True` path (`install_mcp.py:138`); the Windows path passes a list with no `shell=True`; and `default_parameters` is a hardcoded registry dict, not external input. No injection vector. Auggie's own xref (`:138`) contradicts its claim.
  2. *API-key masking is echo-only (Auggie: Low/security)* — **by design and tested**. Masking is explicitly scoped to echoed commands (M1; comments at `install_mcp.py:559-560,629-630`), and `test_api_key_never_in_logged_command` asserts the key is masked in the echo while DEFAULT_PARAMETERS shows in full. Passing a secret to the actual `claude mcp add -e` subprocess is unavoidable and not a defect.
  3. *retry.md blockquote `-`→`>` (Auggie: Trivial)* — cosmetic normalization the PR intentionally made; Auggie itself concluded "Accept." Not a defect.
  4. *comprehensive-features.md tavily.json list (Auggie: Low)* — Auggie concluded the deletion is correct; HEAD shows no `tavily.json` in the cited User-Guides list. Non-finding.
- Persona cross-check: disabled (standard depth).
- Token cost: Auggie ≈ 3 deep passes (offloaded); Claude ≈ orchestration + grounding Reads only.

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 0 medium: 1 low: 4 nit: 3
dropped: 4
auggie_chunks: 3
-->
