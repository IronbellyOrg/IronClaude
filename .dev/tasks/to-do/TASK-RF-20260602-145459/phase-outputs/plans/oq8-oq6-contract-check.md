# OQ-M8 + OQ-M6 Contract-Location & Bump-Target Determination

**Date:** 2026-06-03
**Step:** Phase 1, Step 1.3

## Command outputs (captured verbatim)

### PROBE 1 — return-contract.yaml existence
```
$ ls src/superclaude/skills/sc-reflect-protocol/refs/return-contract.yaml 2>/dev/null && echo "EDIT YAML" || echo "EDIT SKILL.md inline"
EDIT SKILL.md inline
```
The file `refs/return-contract.yaml` is **CONFIRMED ABSENT**.

### PROBE 2 — contract_version literals in SKILL.md
```
$ grep -nE "contract_version" src/superclaude/skills/sc-reflect-protocol/SKILL.md
545:### 9.1 Stable contract (contract_version: 1.1.0)
548:contract_version: "1.1.0"
714:The return contract is versioned via `contract_version: "<major>.<minor>.<patch>"`. Changes are governed by:
1365:  "skill_version": "<contract_version from §9.1>",
1579:| §9.1 versioned return contract stability | `yaml_field` | `return-contract.yaml contract_version == "1.1.0"` |
```

### Ancillary — skill_version literals (runs.jsonl mirror)
```
$ grep -nE '"skill_version"' src/superclaude/skills/sc-reflect-protocol/SKILL.md
1365:  "skill_version": "<contract_version from §9.1>",   # symbolic — auto-tracks, DO NOT edit
1448:{"run_id": "...", ..., "skill_version": "1.0", ...}   # literal example — mirror to bump target
```

## Determination

### (a) Contract location — OQ-M8 [RESOLVED]
ALL §9.1 contract-field additions and the version bump target **SKILL.md §9 inline**. The YAML file
is confirmed absent. The spec §4.2 `refs/return-contract.yaml *(if present)*` row is a **NO-OP / strike it**
(corroborated by research-06 §OQ-M8, CODE-VERIFIED). Route every contract edit to SKILL.md §9.1 (stable,
bump-bearing) or §9.2 (telemetry, no bump).

### (b) Current value & bump target — OQ-M6 [RESOLVED conditionally → resolved concretely]
- **CURRENT `contract_version` literal = `"1.1.0"`** (the low-spec FR-RV3-LOW.7 sibling landed 1.1.0).
- Therefore **bump target = next minor = `"1.2.0"`** (per spec line 454/532 and research-06 §OQ-M6:
  "if the low-spec lands 1.1.0 first, the medium must bump to 1.2.0").

## Canonical sites to update (ONE atomic multi-site edit in Phase 2 Step 2.9)

| # | Line (approx, RE-READ at edit time) | Literal today | Action |
|---|---|---|---|
| 1 | 545 | `### 9.1 Stable contract (contract_version: 1.1.0)` | → `1.2.0` |
| 2 | 548 | `contract_version: "1.1.0"` | → `"1.2.0"` |
| 3 | 1579 | self-check assertion row `... contract_version == "1.1.0"` | → `"1.2.0"` |
| 4 | 1448 | runs.jsonl example `"skill_version": "1.0"` | → `"1.2.0"` (mirror) |

### NOT sites (do NOT edit)
- **714**: `contract_version: "<major>.<minor>.<patch>"` — this is the §9.4 FORMAT-declaration rule
  (already 3-segment), not a version literal. Leave intact. (Check at edit time for any adjacent
  `Contract version is v<v>.` trailer prose; none found by this grep — if present at edit time, include it.)
- **1365**: `"skill_version": "<contract_version from §9.1>"` — symbolic reference, **auto-tracks**, DO NOT edit.
- §9.4 rule-bullet examples (`1.0.x` / `1.x.0` / `X.0.0`) — illustrative, NOT sites.

### Namespace guard
Do NOT touch `checkpoint_version`, `promotion_log_version`, or `metrics_schema_version` — distinct namespaces.

## Timing
The bump is applied as ONE atomic multi-site item in **Phase 2 Step 2.9** (FR-4 is the first contract-bearing FR to land).

## Anomaly check
YAML file does NOT unexpectedly exist — no anomaly. Determination matches actual command output with no assumption.
