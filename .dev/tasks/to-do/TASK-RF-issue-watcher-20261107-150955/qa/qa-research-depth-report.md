# QA Report: research-depth (rf-qa-qualitative), issue-watcher task-builder research

**Date:** 2026-11-07. **Lens:** research-depth. **fix_authorization:** false.
**Provenance note:** the reviewing agent is barred from writing report files and returned this report in its message; the orchestrator saved it here verbatim in substance (condensed table text, same findings and verdict).

## Overall Verdict: FAIL

The research is accurate and detailed on the API of each file, on conventions and on gate facts, but it is not yet usable as the sole input for per-file items. Six blocking defects: four cross-file contradictions or gaps, one unreachable test hook, one gate that cannot see the work.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Explains how components work, not only what they are | PASS | File 05 section 1 gives frozen-dataclass fields, signatures, allowed imports, tests, traps per module |
| 2 | Data flows traced end to end | PARTIAL, MINOR | Research cites design 6.2 steps 1 to 15 by number only; design lines 304-389 are authoritative and can be cited in item Context |
| 3 | Edge cases and failure modes (C1 to C5, rate limit, truncation, unknown outcome) | FAIL (issue 5) | C1 to C5 injection recipe missing |
| 4 | Replicable patterns (exact main.py lines, PATH-stub snippet) | PARTIAL | main.py:559-565 and stub step-1 snippet match; no full e2e stub or scenario-protocol snippet |
| 5 | Per-file items buildable without re-reading source | FAIL (issues 3, 4, 6) | see "Still to look up" |
| 6 | QA-gate placement advice (file 04) realistic | FAIL (issues 1, 2) | |
| 7 | Phase plan (file 05) realistic | PARTIAL | order correct; P7 and P8 overloaded; no gate map |
| 8 | Factual accuracy | PASS | 13 claims spot-checked against code |

## Issues Found (blocking = IMPORTANT)

| # | Sev | Location | Issue | Required fix |
|---|---|---|---|---|
| 1 | IMPORTANT | 04 B.2; research-notes | POST reflect item uses `--diff {BASE}..HEAD`, but the task has no commit step and creates about 50 untracked files; the diff would be empty and nothing audited | Resolve: owner-authorized local commit item before POST, or another resolution; record as a decision |
| 2 | IMPORTANT | 04 D.6, B.5 vs SKILL.md lines 1186-1188, 1243, 2140, 2299 | File 04 recommends 3-agent intermediate gates; the skill rejects any QA gate under 6 agents (final) or 5 (intermediate) | Recommend fewer, bigger gates (3 or 4 intermediate at 6 agents plus the 7-agent final); add a gate map to file 05 |
| 3 | IMPORTANT | 05 section 6, 04 D.5 vs 03 section 6 | Gate commands contradict: bare `uv run ruff format --check` resolves to ruff 0.17.3 not the pinned 0.15.20; `pytest -n auto` needs xdist (CI only); whole-suite `make test` runs a test that rewrites real source files | Use `uvx --offline ruff@0.15.20 format --check` and `check` on explicit files; `uv run --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/`; replace whole-suite `make test` with the named affected subset |
| 4 | IMPORTANT | 05 sections 1.8, 1.9, P8 vs 01 F2 | File 05 says `--help` lists six verbs; Click registers five commands (`reset` is one command) | Change to five commands: once, status, check-config, init-state, reset |
| 5 | IMPORTANT | 03 7.4, 05 3.7, 02 X14; design 296 vs 779 | No recipe for triggering crash points C1 to C5 at the Store/Launcher seams; design is internally inconsistent (k-th write vs `crash_at`); C2 is not reachable through the Store seam | Add a recipe table (C1 before save 1; C3 after save 1; C4 before save 2 after launcher ran; C5 after save 2; C2 patch `os.replace` narrowly or plant an orphan tmp file); each followed by 5 reruns per NFR-005 |
| 6 | IMPORTANT | 02 G vs 05 section 7, research-notes "Ambiguities: None" | No merged decision register. Missing from file 05: G3 (no reason in the closed list for a failed marker or edit-timestamp read; `audit.line` raises on any reason outside `REASONS`), G4 (`marker_time` undefined; use `max(created_at, updated_at)`), G8 (migration save in dry-run), G12 (jq null versus missing), G13 (page longer than 100), G14 (commas in label names); G-01 (`cwd` on `Runner.run`) departs from the NFR-014 signature; gap ids collide with the design's G1 to G7 | One de-duplicated register with unique ids, a recommended default and a disposition per item, each stating whether it deviates from the design |

Minor notes: M1 no step-to-function table for `run_cycle` (design 6.2 is the source); M2 GraphQL query texts (`EDITS_QUERY`, `PROJECT_ITEMS_QUERY`) exist nowhere, `$after` must be a nullable variable; M3 e2e stub scenario protocol and git stub-or-real-repo decision open; M4 `REASONS` has 52 names (spec lines 334-358, spec untracked so tests embed literals); M5 P7 and P8 overloaded, about 50 deliverables, about 140+ items; M6 design names `RecordingLauncher` and `FakeClock(start, step)` (lines 297-298) versus file 05's `FakeLauncher`, `FakeClock(now, mono)`.

## Still to look up (item author)

Design tables read by section (6.2 steps, 7.4 transitions T-1 to T-13, 8.2 classify, 8.4 outcome map, 10.1 audit schema, 14 defaults); the 52 reasons with kind and exit from the spec; the two GraphQL query texts; the stub scenario protocol and git decision; crash-hook mapping; gate command forms; POST `{BASE}` resolution.

**VERDICT: FAIL**
