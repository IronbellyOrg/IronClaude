# Deviation Report Format Reference

> **Canonical Contract** — This document defines the authoritative schema for deviation reports consumed by all pipeline gates, CLI commands, and prompt builders. All consumers MUST conform to this schema.

| Field | Value |
|---|---|
| Schema Version | 1.0 |
| Source Decision | D-0003 (OQ-006) |
| Effective Release | v2.20 WorkflowEvolution |

## YAML Frontmatter

Every deviation report begins with YAML frontmatter:

```yaml
---
source_pair: "<upstream_file> → <downstream_file>"
upstream_file: "<path to upstream document>"
downstream_file: "<path to downstream document>"
high_severity_count: <integer>
medium_severity_count: <integer>
low_severity_count: <integer>
total_deviations: <integer>
validation_complete: <boolean>
fidelity_check_attempted: <boolean>
tasklist_ready: <boolean>
---
```

### Frontmatter Field Definitions

| Field | Type | Required | Description |
|---|---|---|---|
| `source_pair` | String | Yes | Human-readable label: `"<upstream> → <downstream>"` |
| `upstream_file` | String | Yes | Relative path to the upstream (source/spec) document |
| `downstream_file` | String | Yes | Relative path to the downstream (generated) document |
| `high_severity_count` | Integer | Yes | Count of HIGH-severity deviations (≥0) |
| `medium_severity_count` | Integer | Yes | Count of MEDIUM-severity deviations (≥0) |
| `low_severity_count` | Integer | Yes | Count of LOW-severity deviations (≥0) |
| `total_deviations` | Integer | Yes | Total deviation count (must equal sum of severity counts) |
| `validation_complete` | Boolean | Yes | `true` if the fidelity check completed without errors |
| `fidelity_check_attempted` | Boolean | Yes | `true` if the fidelity check was invoked |
| `tasklist_ready` | Boolean | Yes | `true` only if `high_severity_count == 0` AND `validation_complete == true` |

## Deviation Table Schema (7 Columns)

The deviation table uses standard Markdown table format:

| # | Column | Type | Constraints | Description |
|---|---|---|---|---|
| 1 | ID | String | Format: `DEV-NNN` | Unique deviation identifier, zero-padded 3-digit |
| 2 | Severity | Enum | `HIGH` \| `MEDIUM` \| `LOW` | Classification level |
| 3 | Deviation | String | Non-empty | Concise description of what differs |
| 4 | Upstream Quote | String | Non-empty | Verbatim quote from upstream document |
| 5 | Downstream Quote | String | Non-empty or `[MISSING]` | Verbatim quote from downstream document |
| 6 | Impact | String | Non-empty | Assessment of how deviation affects correctness |
| 7 | Recommended Correction | String | Non-empty | Specific action to resolve the deviation |

## Column Name Rationale

Generic names `Upstream Quote` / `Downstream Quote` are used instead of `Spec Quote` / `Roadmap Quote` because the fidelity check is reusable across document pairs (spec→roadmap, roadmap→tasklist). The frontmatter `source_pair` field provides specific document context.

## Gate Interactions

| Gate Check | Field Used | Logic | Blocking in v2.20 |
|---|---|---|---|
| `_high_severity_count_zero()` | `high_severity_count` | `True` if value is `0`; `False` if missing or >0 | Yes |
| `_tasklist_ready_consistent()` | `tasklist_ready`, `high_severity_count`, `validation_complete` | `True` if consistent | Yes |
| Count cross-validation | All severity counts vs table rows | Warning log on mismatch | No (warning only) |

## Example

```markdown
---
source_pair: "spec.md → roadmap.md"
upstream_file: "spec.md"
downstream_file: "roadmap.md"
high_severity_count: 1
medium_severity_count: 2
low_severity_count: 0
total_deviations: 3
validation_complete: true
fidelity_check_attempted: true
tasklist_ready: false
---

# Deviation Report: spec.md → roadmap.md

| ID | Severity | Deviation | Upstream Quote | Downstream Quote | Impact | Recommended Correction |
|---|---|---|---|---|---|---|
| DEV-001 | HIGH | Missing FR-019 | "Cross-references must be validated" | [MISSING] | No cross-ref integrity | Add FR-019 to Phase 2 |
| DEV-002 | MEDIUM | NFR timeout relaxed | "120s hard limit" | "120s target, 600s timeout" | Less strict measurement | Clarify per OQ-008 |
| DEV-003 | MEDIUM | Parameter renamed | "spec_file" | "source_file" | Import paths affected | Rename for consistency |
```

## Versioning

Schema version 1.0, effective for v2.20. Schema changes require a new decision document and version increment.

| Property | Value |
|----------|-------|
| Version | 1.0 |
| Status | Finalized |
| Review Date | 2026-03-09 |
| Defined by | Prompt builders `build_spec_fidelity_prompt` in `src/superclaude/cli/roadmap/prompts.py` and `build_tasklist_fidelity_prompt` in `src/superclaude/cli/tasklist/prompts.py`; no dataclass models the table |
| Checked by | `_high_severity_count_zero` and `_tasklist_ready_consistent` in `src/superclaude/cli/roadmap/gates.py` (reused by `src/superclaude/cli/tasklist/gates.py`) |
| Column names | The roadmap-to-tasklist prompt uses `Upstream Quote` / `Downstream Quote`; the spec-to-roadmap prompt labels columns 4 and 5 `Source Quote` / `Roadmap Quote` |
