# Diff Analysis: sc:reflect UC-2 reviewer-card comparison (Mode A)

## Metadata
- Generated: 2026-10-20T05:26Z
- Variants compared: 3 (R1 analyzer/sonnet C=0.71, R2 QA/haiku-alias C=0.78, R3 refactorer/opus C=0.80; all blind-calibrated by opus, diversity=degraded)
- Inputs: `reviewer-cards/reviewer-{1,2,3}-calibrated.md` (read-only); copied to `variant-{1,2,3}-original.md`
- Total differences found: 14 (structural 2, content 5, contradictions 3, unique 4) + shared assumptions 3 (UNSTATED promoted: 2)
- Similarity check: variants are partitioned by task (R1=T2/T4/T5, R2=T1/T3/T6, R3=T7) and give materially different D1 dispositions; diff ratio far above 10% — debate NOT skipped.
- Coordinator source verification performed 2026-10-20 against current worktree (line anchors below are coordinator-verified unless marked [card-only]).

## Structural Differences

| # | Area | V1 (R1) | V2 (R2) | V3 (R3) | Severity | Taxonomy |
|---|------|---------|---------|---------|----------|----------|
| S-001 | Task partition | T2/T4/T5 (22 ACs) with explicit unread fixture regions | T1/T3/T6 (20 ACs) summarized, fixtures described | T7 (7 ACs) + cross-cutting canonical-deviation hunt | Low | L2 |
| S-002 | Deviation taxonomy use | split disposition (refuted slice + MEDIUM regression candidate) | 4-class only, advisories separated | adds "newly alleged canonical deviation" section + ordering section | Medium | L2 |

## Content Differences

| # | Topic | V1 (R1) | V2 (R2) | V3 (R3) | Severity | Taxonomy |
|---|-------|---------|---------|---------|----------|----------|
| C-001 (D1) | Menu option 0 whole-selection rejection at project/local scope or non-Linux | explicit-mixed slice refuted; menu-0 slice = MEDIUM regression candidate, "spec-conflicted/debate-open" | regression refuted; whole-selection validation is the contract; lack of a menu-zero test is not a contract | regression refuted; necessary consequence of source.md:78+:80+Task4; documentation gap | High | L3 (validation rule / guard) |
| C-002 (D2) | Permission predicate split: discovery/reuse (`install_codebase_memory.py:545-552`) vs proof/removal (`:85-99`,`:102-116`); proof after upstream (`:682-683`); caller fails (`install_mcp.py:846-848`); retry reuses without receipt (`:597-605`) | "conditional drift candidate" (fatal provenance not in spec failure list) | "advisory sibling-contract mismatch", no regression | "no-spec advisory correctness gap" | Medium | L3 (guard / state) |
| C-003 (D3) | HOME-ancestor symlink fails closed (`:55` absolute, `:88`,`:489`,`:539-544` resolve mismatch) | refuted; advisory compatibility limit; generic message omits path (`install_mcp.py:577-579`) | refuted | no confirmed regression; advisory availability limit | Low | L3 (guard) |
| C-004 (D5) | Linux-only automation (macOS excluded) vs source.md:90 "Linux and macOS" | "authorized, not a separate defect" | labelled **necessary** (operator direction) | authorized by operator direction "plus source.md:90" | Medium | L2 (scope policy) |
| C-005 (D7) | Verification/fixture coverage claims | T2 fixtures, T5 `native_phase_guard` unread; mock fidelity unverified | fixtures described; mcp_cli canned values noted; 242-pass historical | no fresh execution; Click reachability degrade noted | Medium | L2 |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact | Taxonomy |
|---|-------------------|----|----|----|--------|----------|
| X-001 (D1) | Is menu option 0 at project/local scope or non-Linux a Regression? | Yes-candidate (MEDIUM) | No | No (Necessary) | High | L3 |
| X-002 (D2) | Taxonomy label for the predicate mismatch | Drift candidate (conditional) | Advisory, not a deviation class | Advisory correctness gap, no spec anchor | Medium | L3 |
| X-003 (D5) | Label for macOS exclusion | Authorized | Necessary | Authorized (cites source.md:90, which actually lists macOS as supported) | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value | Taxonomy |
|---|---------|-------------|-------|----------|
| U-001 (D4) | V3 | NEW LOW drift: `main.py:326-330` rejects `--list` with `--dry-run` or non-user `--scope`; source.md:76 limits list rejection to *mutation modes*; baseline (source.md:31) accepted `--list/--scope/--dry-run` on the flat command; guide:50 discloses but is not authorization | High | L3 (validation rule) |
| U-002 (D6) | V3 | Doc disclosure gaps: guide:46/73 do not state option 0 fails whole-selection at unsupported native scope/platform; guide:25/223 do not state the group-writable-directory proof rule | Medium | L1 (docs/presentation) |
| U-003 | V1 | Prior entry's secret values may travel in `add-json` argv during restore (`install_mcp.py:887`, `_restore_user_native_entry`); tests check captured output only (`test_install_mcp_tavily.py:736-757` [card-only]) | Low | L3 |
| U-004 | V2 | Click decorator oracle DEGRADE (not UNREACHED) for two callbacks; 3 cross-reference risk flags; T3/T4 overlap benign | Low | L2 |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|-----------|----------------|----------|
| A-001 | C-002 (all three treat D2 as conditional) | Real host `~/.local/bin` mode under released ccsession `mkdir` (`install_ccsession.py:37`, process umask) and whether upstream `install.sh --dir` preserves it are **unknown**; no fixture sets umask/0o775 (coordinator grep: zero matches for `umask|0o022|0o775` in `tests/cli/test_install_codebase_memory.py`) | UNSTATED (all rely on it, none proves it) | Yes — L3 |
| A-002 | C-001/X-001 (all three accept whole-selection validation is spec-consistent) | source.md:67 "Keep ... all existing installation invocations working" is subordinate to :78/:80 whole-selection rules; none of the cards tests this ordering against a "regression = observable prior-behavior loss" definition | UNSTATED | Yes — L3 |
| A-003 | C-005 | Historical 242-pass run (`t6-cli-regressions.txt:49-53`) remains representative of the current tree | STATED (R2 says "not fresh") | No |

## Summary
- Total structural differences: 2
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, X-001
- Debate points (denominator for convergence): S-001, S-002, C-001..C-005, X-001..X-003, A-001, A-002 = **12**
- Taxonomy coverage: L1 (U-002 feeds C-005/S-002 docs slice), L2 (S-001, S-002, C-004, C-005, X-003), L3 (C-001, C-002, C-003, X-001, X-002, A-001, A-002)
