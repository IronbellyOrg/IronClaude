# Requirements Patch Verdict (C-006)

Phase 2 stale-string audit of `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/`. Patch strategy: **companion amendment** `FR-RH1-v1-amendment.md` (authoritative R1–R9) supersedes stale clauses in `merged-requirements.md`; the historical artifact is intentionally left intact (non-destructive). Authoritative source for implementation = `FR-RH1-v1-amendment.md` + `REPORT`.

**Verdict basis:** a search is PASS when every occurrence is EITHER (a) inside `FR-RH1-v1-amendment.md` as corrective/override prose, OR (b) inside `merged-requirements.md` but explicitly superseded by the amendment's §6 override table (i.e., historical/negative prose, NOT an implementation requirement). FAIL would be an unjustified live implementation requirement.

| # | Search string | Matches | Where | Verdict | Justification |
|---|---|---:|---|---|---|
| 1 | `binding unambiguously absent` | 5 | MR:92, MR:131, MR:235; AMD:93, AMD:94 | **PASS** | MR occurrences are the stale non-real-boot Regression path → superseded by R1 (AMD §6 rows `:92`, `:130-132`, `:235`). AMD occurrences are the override prose itself. No live requirement permits this path. |
| 2 | `records the skip in Grounding Gaps` | 4 | MR:138, MR:191; AMD:96, AMD:97 | **PASS** | MR occurrences are the stale `--no-reachability` Grounding-Gap behavior → superseded by R2 (AMD §6 rows `:138`, `:191`). AMD occurrences are override prose. |
| 3 | `spec … absent` variants | 7 | MR:93, MR:161, MR:236 (+AMD R3/override/closure) | **PASS** | MR:93/236 stale spec-absent→`unproven`→Grounding-Gap+`needs_human_decision` → each explicitly superseded by R3 (AMD §6 rows `:93` and `:236`, added in the Phase-2 gate fix cycle, alongside `:133-138`). MR:161 is the `reachability_skip_reason` enum listing `spec-and-tasklist-absent` as a valid telemetry reason — consistent with R3, not stale. AMD occurrences define the corrected telemetry-only rule. |
| 4 | `contract_version: "1.5.0"` | 3 | MR:274, MR:309; AMD:101 | **PASS** | MR:274/309 are the stale fixtures carrying reachability fields under 1.5.0 → superseded by R4 (AMD §6 row `:270,:274,:309`). AMD occurrence is override prose. Implementation MUST use `1.6.0`. |
| 5 | `reachability_gate_added_tokens: 0` | 3 | MR:257; AMD:81, AMD:99 | **PASS** | MR:257 stale zero-cost claim → superseded by R8 (AMD §6 row `:257-258`). AMD occurrences are the "must not remain" rule + override. |
| 6 | `reachability_gate_added_turns: 0` | 1 | MR:258 | **PASS** | Stale zero-cost claim → superseded by R8 (AMD §6 row `:257-258`). |
| 7 | `semantic classification` | 2 | MR:67; AMD:100 | **PASS** | MR:67 stale semantic-fallback-as-blocking-trigger → superseded by R9 (AMD §6 row `:67-69`): advisory telemetry only, no `unproven`/gap/status. AMD occurrence is override prose. |
| 8 | `runtime_surface_` | 0 | — | **PASS (clean)** | Zero matches anywhere in the FR-RH1 brainstorm dir → no FR-RSR `runtime_surface_*` schema leakage into FR-RH1 requirements. |

## Overall verdict: **PASS**

All 8 searches PASS. Every stale clause in `merged-requirements.md` is explicitly overridden by `FR-RH1-v1-amendment.md` §6 and is now historical/negative prose, not an implementation requirement. The amendment encodes the corrected R1–R9 (AMD §"Authoritative R1–R9"):
- **R1** real-boot-only Regression (AMD:24-31) — no clause permits static-binding-absence + oracle-mismatch ⇒ Regression (AMD:30, AMD:113-115).
- **R2/R3** telemetry-only skips (AMD:33-46).
- **R4** contract `1.6.0` (AMD:48-52).
- **R5** wrapper plumbing (AMD:54-59).
- **R6** producer eval fixture (AMD:61-70).
- **R7** field presence/consistency (AMD:72-79).
- **R8** bounded cost (AMD:81-86).
- **R9** advisory-only semantic fallback (AMD:88-91).

No FAIL findings. Phase 3 may proceed on the amendment, not on the stale `merged-requirements.md` clauses.
