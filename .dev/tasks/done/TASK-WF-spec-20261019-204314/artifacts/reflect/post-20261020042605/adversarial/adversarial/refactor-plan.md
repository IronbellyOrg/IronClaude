# Refactoring Plan: Merge into Base (Variant 3)

This plan merges ANALYSIS (reviewer findings), not code. No production/test/doc edits are proposed for execution here.

## Overview
- Base: Variant 3 (R3 refactorer/opus, final score 0.860)
- Incorporating strengths from: Variant 2 (structure, D2 exposition, T1/T3/T6 anchors, fixture caveats), Variant 1 (split-slice D1 framing, D2 chain, T2/T4/T5 anchors, unread-region discipline, argv advisory), debate outcomes (forced-round labels), invariant probe (INV-001..010)
- Planned changes: 9
- Risk level: Low (all additive or relabel; provenance tags required)

## Planned Changes

### Change 1: Adopt V2's four-class frame with separated advisory and errata sections (from Variant 2)
- **Source**: Variant 2, sections "Candidate dispositions" / "Canonical deviation / advisory separation" / "Evidence limits and errata"
- **Target**: Base, whole-document structure (restructure)
- **Rationale**: S-002 resolved 3/3 for V2's structure + V3 content (R2 votes). Required output sections: Verdict summary; Per-task T1..T7 status; Canonical deviations (four classes only); Correctness advisories / evidence gaps; Rejected candidates; Verifiers and limits; Provenance.
- **Risk**: Low — restructure of headings, content preserved.

### Change 2: Relabel D1 per forced round (from debate; V1 split framing)
- **Source**: V1 "W1-D1 split disposition"; forced-round tally; INV-001
- **Target**: Base "W1-D1" section (replace label + add slices)
- **Rationale**: Final majority: **Drift (LOW-MEDIUM), menu option-0 slice only** (V1 50%, V2 64%); dissent V3 Regression-LOW 55%. Explicit native-plus-other selections at project/local or non-Linux remain **Necessary deviation** (tests `tests/cli/test_install_codebase_memory.py:964-988`). Anchors: `install_mcp.py:1284-1285`, `:1311-1314`, `:486-496`; spec source.md:67, :78, :80, :143, :144; compliant alternative = visible skip of native only. Doc note: guide:46/73 imply but never name option 0 (LOW clarity). Test gap: no option-0 project/Darwin case (only `:944-952`). Must state the decision is 50-64% confidence and spec-interpretation dependent; must NOT present as settled.
- **Risk**: Low.

### Change 3: Relabel D2 per forced round (from Variant 2 mechanism + V1 chain)
- **Source**: V2 "W1-D2"; V1 "W1-D2"; INV-002, INV-003
- **Target**: Base "W1-D2" (replace label; append gate enumeration)
- **Rationale**: Final majority **Drift, conditional on A-001** (V2, V3 55%); dissent V1 advisory 55%. Anchors: predicate split `install_codebase_memory.py:545-552` vs `:85-99`,`:102-116`; proof after upstream `:682-683`; failure `:693-700` → `install_mcp.py:846-848`; retry reuse `:597-605`; removal ambiguous `:257-264`,`:305-311`; spec :109 (stop only for external/custom), :111, :146. Include INV-002's 8-gate enumeration (ccsession only via `install`, `main.py:224`→`:255`; `mkdir` umask; both dirs tested `:87`; binary mode `:114`; stale receipt `:159`; `os.link` `:192`; verification `:674` no mode check; `install.sh --dir` behavior unknown). Keep the explicit statement: no umask/0775 fixture; real host/upstream modes unobserved; umask-002 recollection must not be stated as fact.
- **Risk**: Low.

### Change 4: Relabel D3 per forced round (from debate; V1 message detail)
- **Source**: V1 "W1-D3" (message omits path `install_mcp.py:577-579`); INV-004
- **Target**: Base "W1-D3" (replace label)
- **Rationale**: Final majority **Drift (LOW), conditional on a symlinked-HOME host** (V2; V3 50%); dissent V1 advisory 60%. Anchors `:54-55`, `:88`, `:489`, `:539-544`; `install_mcp.py:572-579`; spec :56 (no-op) vs :114 (uninstall-section fail-closed). No symlinked-HOME fixture.
- **Risk**: Low.

### Change 5: Correct the Linux-only authority anchor and state the cost (from Variant 1 label; INV-009)
- **Source**: V1 "authorized"; operator-direction.md:5-7 exact quote; INV-009
- **Target**: Base "Linux-only" sentences in T7/D1 sections (replace)
- **Rationale**: Unanimous **Authorized** (C-004/X-003, 88%). Remove source.md:90 as support (it lists macOS). Quote: "there is absolutely no reason to overcomplicate anything in order to preserve macOS portability" and "automated macOS support may be excluded and documented". State the cost: every `superclaude install` on macOS exits 1 (`main.py:255-275`); disclosed guide:9.
- **Risk**: Low.

### Change 6: Keep D4 as LOW drift candidate, interpretation open (base content, modified)
- **Source**: Base "Newly alleged canonical deviation"; R2/forced votes
- **Target**: Base D4 section (modify wording)
- **Rationale**: Majority label Drift (V2 74%, V1 45%); V3 downgraded to candidate 45%. Anchors `main.py:326-330`; source.md:76, :31, :117; guide:50. State: `--list --dry-run` arguably redundant under :117; `--scope` half stronger; baseline code unread by anyone.
- **Risk**: Low.

### Change 7: Per-task T1..T7 status table with AC counts and anchors (from Variants 1 and 2)
- **Source**: V1 §Assigned completion (T2 7 ACs, T4 8, T5 7); V2 §Assigned completion (T1/T3/T6 20 ACs); V3 §T7 (7 ACs)
- **Target**: Base, new "Per-task status" section (insert)
- **Rationale**: Required by the parent. Carry each card's current-line anchors verbatim; mark T2/T5 fixture regions now READ by the coordinator (`test_install_mcp_tavily.py:382-462` isolates HOME + CLAUDE_CONFIG_DIR, stubs discovery, `pytest.fail` on `_run_bounded`; `test_update_command.py:31-76` autouse guard stubs the shared phase and fails on real CLI/native). Per INV-005: state "49 ACs" is the tasklist's decomposition of source.md:138-149 (12 bullets); conformance is **mock-conformant; source.md:151 live gate unverified**. T4 status must carry the D1 Drift finding; T2/T3 carry the conditional D2 Drift; T7 carries doc clarity notes.
- **Risk**: Low.

### Change 8: Advisory / evidence-gap section (from Variants 1 and 2; probe)
- **Source**: V1 (add-json argv secret exposure; `AcquisitionResult.acquired` consumed only in tests — coordinator grep: `tests/cli/test_install_codebase_memory.py:54,105,254,306`); V2 (canned `mcp_cli` fixture `:821-835`; Click decorator DEGRADE; cross-ref risk flags); INV-002, INV-005, INV-006, INV-010; grounding-gaps.yaml (Serena execute_shell_command not exposed; dynamic Click reachability)
- **Target**: Base, new "Correctness advisories and evidence gaps" section (insert)
- **Rationale**: Keeps non-deviation findings out of the four classes (V2 discipline). Includes: `claude --version` runs twice on user/Linux (`install_mcp.py:513`, `:830`); option 0 never reaches `check_prerequisites` at project scope; error `:488` does not name option 0.
- **Risk**: Low.

### Change 9: Provenance + verifiers/limits block (from all)
- **Source**: V3 "Ordering and limitations" + recommendations; V1/V2 next-step lists
- **Target**: Base end (append)
- **Rationale**: Strongest verifiers: isolated option-0 project/Darwin case; 0775 canonical-dir case covering first attempt/retry/removal; HOME-ancestor alias case; `--list --scope project` contract decision. Limits: no fresh tests run; no live upstream smoke; Serena exec not exposed; Click reachability degraded; input C mean 0.763 reused, no new calibration.
- **Risk**: Low.

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale for Keeping Base / Rejecting |
|---|---|---|
| C-001 (V1 original) | D1 as MEDIUM "regression candidate / debate-open" | Withdrawn by V1 in R1; final majority Drift. V3's LOW Regression kept as recorded dissent only. |
| C-001 (V2 R1) | D1 as "Not a deviation" | Withdrawn by V2 in R2; observable baseline loss. |
| C-001 (R2 consensus) | D1 as "Necessary deviation" | Falsified by INV-001; all three withdrew the "only compliant reading" premise. |
| X-003 (V2 original) | Linux-only as "Necessary" | Conceded; operator text is permissive. |
| X-003 (V3 original) | source.md:90 as support | Conceded; :90 lists macOS. |
| D1 docs (V3 original) | "documentation gap" | Downgraded by V3 to LOW clarity note (guide:46 + :73 imply the result). |
| U-003 argv advisory | Promote to deviation | No spec anchor; tests check output not process table; kept advisory. |
| INV-007/008 | Add as findings | ADDRESSED LOW; mention only in advisories if space. |

## Risk Summary
| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Low | Section order differs from V2 frame | Re-order headings |
| 2-4 | Low | Label misreported | Restore forced-round tally wording verbatim |
| 5 | Low | Wrong authority anchor | Quote operator-direction.md:5-7 |
| 6-9 | Low | Omitted content | Re-append from source variant |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto (debate-orchestrator)
- Approval timestamp: 2026-10-20T05:50Z
