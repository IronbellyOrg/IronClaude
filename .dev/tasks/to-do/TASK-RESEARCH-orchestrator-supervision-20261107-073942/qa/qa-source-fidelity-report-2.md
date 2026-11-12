# QA Report — Source-Document Fidelity (orchestrator mode Phase 1, issue #339)

**Topic:** Orchestrator mode Phase 1, source fidelity of RESEARCH-REPORT-orchestrator-mode.md against the crash-recovery skill, ccsession and Orca captures
**Date:** 2026-11-07
**Phase:** source-fidelity
**Fix cycle:** N/A
**Fix authorization:** false (report only)

---

## Source-Document Fidelity Report

### Fidelity Findings

| # | Type | Source File | Report Section | Finding | Severity |
|---|------|-------------|----------------|---------|----------|
| F1 | Detail distortion | `sc-crash-recovery/scripts/bootstrap_scan.sh:136` (also `:80`, `:107`, `:143-170`) | §2.3 CODE-CONTRADICTED table, report line 160 | The report says `:136` "escapes only partly". In fact `:136` (`awk ... printf "%s\"%s\""`) does no escaping at all. The partial escaping (only `"`) is at `:80` and `:107`, and the heredoc at `:143-170` is also unescaped. This contradicts the report's own line 1026 ("builds JSON by hand without escaping (`:136`)"). The conclusion is still true (a `"` or `\` in a path gives malformed JSON), so this is wording or citation, not a false claim. Fix: change line 160 to "`:136` does not escape; `:80`/`:107` escape only `"`". | MINOR |
| F2 | Coverage gap | `sc-crash-recovery/refs/pipelines.md:190`, `:198`, `:199` | §2.3 crash-recovery reuse; worktree-removable rule (report line 395) | pipelines.md defines three TASK-WF state rules: (a) a package in `to-do/` with every task complete is **archive-blocked**, not finished (`:190`); (b) a package in both `to-do/` and `done/` is a conflict (`:198`); (c) a `.archiving` marker means "never infer the owner is dead from `FINAL:`/`ARCHIVE:` lines" (`:199`). The report's ledger, finished and worktree-removable rules (line 395, five refusal conditions) do not carry (a) or (c). A coordinator that follows only the report could treat an archive-blocked or mid-archive package as finished. No report statement contradicts the source, so this is an omission rather than a false claim. Recommend adding `.archiving` present and archive-blocked as refusal conditions. | MINOR |
| F3 | Citation drift | captures `lc16-show-4.json`, `lc17-show-1.json`, `lc01-show-1.json` | §2.2 row 102 | Row 102 cites `lc16:152-159` and `lc17:152-166` for attention categories including `root_completion`. Neither `lc16:156-159` nor `lc17:161-166` (category `failure`, `requiresAction: true`) holds `root_completion`; `root_completion` appears only at `lc01-show-1.json:163`. Every value is real; one value has the wrong citation. Fix: add `lc01:163`. | MINOR |
| F4 | Citation drift | `lc16-show-4.json:115` | Worker-show field list, report line 349 | Line 349 cites `parent` within `lc16:127-185`. `parent` is `projection.parent` at `lc16:115`, outside that range. The field exists, so only the line range is wrong. | MINOR |
| F5 | Tag mixing | `orca-capabilities.md:129`; `lc16:180`, `:185` | §2.2 row 104 | The tag "[CODE-VERIFIED as help text]" joins a verified tag with a help-text source. The three-state agentWait semantics (object / null / absent) come from CLI help text recorded in the inventory (`:129`). Every capture shows only `null`, so captures confirm the null state only. The row already marks the non-null shape [UNVERIFIED] (GQ-36), so no unverified shape is shown as verified. Recommend "[help text; null state CODE-VERIFIED]". | MINOR |
| F6 | Unsupported inference | captures (no version field); `orca-capabilities.md:8` | §2.2, report line 88 | "taken ... on a CLI version between those two" is an inference: neither the captures nor the inventory records the capture-time version. The same sentence says "which the files do not record (GQ-41)", so the gap is disclosed. "Between" should read "an unrecorded version". | MINOR |
| F7 | Over-generalization | `bootstrap_scan.sh:31`; `ccsession-tag/ccsession:162-165` | §2.3 CODE-CONTRADICTED table, report line 158 | "Claude Code replaces every non-alphanumeric character" is broader than the evidence. On the host, `.` is confirmed encoded as `-` (`~/.claude/projects/-home-coder-workspaces-IronClaude--dev-worktrees-...`); `_` was not checked. The report also does not mention that ccsession's `slugify` (`:162-165`, commented "Claude Code's path encoding") makes the same `/`-only assumption, which is a second instance of the defect in a component the report reuses. The bug claim for `:31` holds. | MINOR |
| F8 | Characterization (cross-source) | `orca-capabilities.md:68`, `:177` | Report line 594 (S-05) | S-05 states the ask timeout as "600000 ms default, range 1 to 1800000" with no UNVERIFIED tag, while the inventory marks the default ask timeout UNVERIFIED (`:68`, `:177`). The report's source is research file 06 `:180`, which is outside my assigned sources, so I cannot confirm whether that research file observed it live. Flagged so the merge step can check it against partition 1. | MINOR |

No CRITICAL or IMPORTANT finding. The adversarial target of 5 distortions was met with 8 findings, but none changes a value, invents a field, or shows a guide statement as verified.

### Phantom-claim checks (claims verified against the cited files)

| # | Report claim | Cited source | Result |
|---|--------------|--------------|--------|
| V1 | Row 100: liveness `verdict: live`, `source: agent_status`; values beyond `live` [UNVERIFIED], guide text | `lc16:135-139`; `orca-capabilities.md:122-126` | Match. Only `live` captured (in lc17 too, despite failed dispatch); the other values are tagged as guide text |
| V2 | Row 101: outcome `in_progress` / `failed` / `succeeded` | `lc16:134`, `lc17:134`, `lc01:134` | Match |
| V3 | Row 103: `resource.terminalState` is `retained` on a working worker, `reclaimable` after failure or success | `lc16:150`, `lc17:150`, `lc01:150` | Match |
| V4 | Row 105: `stage.activity` [CODE-CONTRADICTED], still `working` on a settled or finished worker | `lc17:131-132`, `lc01:132` | Match |
| V5 | lc17 nextAction argv `[orchestration, worker-release, --dispatch, ctx_5fac5090b848]` | `lc17:152-160` | Match, verbatim |
| V6 | Row 106: `projection.parent` null | `lc16:115` | Match |
| V7 | Line 110: `worker-list reclaimable` returns `workers: []` with `counts {released:1}`, `page {limit 100, total 0, hasMore false, nextCursor null}` | `lc01-step7.txt:28` and following | Match |
| V8 | `bootstrap_scan.sh:73` tests `[[ -d "$ABS_PROJECT/.git" ]]` and so skips worktrees | script `:73`; this worktree's `.git` is a regular file | Match (host-verified) |
| V9 | `bootstrap_scan.sh:31` encodes only `/` | script `:31` (`sed 's|^/||; s|/|-|g'`) | Match; `.` bug host-verified |
| V10 | `parse_session_log.py` keeps role, ts, text and tool_calls only, with no stop or exit signal | script `:31-40`, `:85-93` | Match |
| V11 | ccsession pane-key `:` written as `+`; tab file content order session, folder, handle; `--list` removes other tab files | ccsession `:567-571`, `:590`, `:594-600` | Match |
| V12 | Crash-recovery SKILL.md citations (`:4` allowed-tools, `:13`, `:25-27`, `:36`, `:49-50`, `:53`, `:91`, `:93-97`, `:134`, `:137`, `:139-150`, `:155`) | SKILL.md | All match: read-only enforcement, SAFE/REVIEW labels, propose-never-execute, `unscanned:` markers and "What I could not determine" (`report-template.md:127-129`) |
| V13 | Guide-sourced Orca behaviour (stall proof, depth-1 nesting, reclaimable failed start, heartbeat age) tagged [UNVERIFIED — Orca guide] | `orca-capabilities.md:97-102`, `:112`, `:122-126`, `:130`; report lines 693, 703, 721, 757, 818 | Match; each is tagged as guide text, not verified |

### Checklist Results

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Semantic coverage of the components used | PASS (with note F2) | All assigned sources are represented in §2.2/§2.3 and the risk table. Only gap: pipelines.md archive-blocked and `.archiving` rules (F2) |
| 2 | Detail preservation (liveness, projection, agentWait, scanner lines, ccsession) | PASS (with notes F1, F3, F4) | V1-V11: every value and field name matches the captures and scripts; three citation or wording slips, no wrong value |
| 3 | Phantom findings (at least 5 claims) | PASS | 13 claims checked (V1-V13); 0 phantom fields, values or behaviours |
| 4 | Characterization: guide statements not shown as verified | PASS (with notes F5, F8) | V13 and row 100 tag guide text as UNVERIFIED; F5 is a tag-wording mix with the unverified part already tagged; F8 traces to a source outside this partition |
| 5 | No aspirational claims | PASS (with notes F6, F7) | No capability is claimed that the sources lack; F6 and F7 are small inferences beyond the evidence, the first already disclosed (GQ-41) |

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

### Confidence

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 20 | Grep: 7 | Glob: 0 | Bash: 3
- Unverifiable sub-item: F8's upstream (research file 06 `:180`) is outside the assigned sources; recorded as a MINOR note, not counted against the checklist.

## Summary

- Checks passed: 5 / 5
- Findings: 8 (CRITICAL: 0, IMPORTANT: 0, MINOR: 8)
- Fixes applied: 0 (fix authorization false)
- The report reproduces capture fields and values, scanner bugs and ccsession behaviours faithfully. Guide-sourced Orca behaviour is tagged UNVERIFIED. The defects are one misplaced escaping description (F1), one omitted pipelines.md rule set (F2), two citation-range slips (F3, F4), one mixed tag (F5) and three small inferences or cross-source tags (F6-F8). All are notes.

Verdict: PASS
