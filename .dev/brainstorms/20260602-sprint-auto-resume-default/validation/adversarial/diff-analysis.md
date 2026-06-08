# Diff Analysis: DD-1 Resume-Cursor Decision Comparison

## Metadata
- Generated: 2026-06-02
- Variants compared: 2 (A=derive-only as written; B=atomic breadcrumb alternative)
- Total differences found: 9
- Categories: structural (1), content (3), contradictions (2), unique (1), shared assumptions (2)

## Structural Differences
| # | Area | Variant A (derive-only) | Variant B (breadcrumb) | Severity |
|---|------|-------------------------|------------------------|----------|
| S-001 | Cursor source of truth | Single ledger (`execution-log.jsonl`), scanned + paired | Dedicated `resume-cursor.json` authoritative; ledger refines only | Medium |

## Content Differences
| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Crash durability of cursor | Relies on append-mode JSONL line being intact | tmp+rename `os.replace` → atomic, torn-line-immune | **High** |
| C-002 | Write-path surface added | Zero (NG1 honored; only DD-4 sha field) | +1 file + 1 atomic write per phase | Medium |
| C-003 | Fallback when cursor unreadable | "first phase without result.json" | absent breadcrumb ⇒ fall back to ledger derivation | Low |

## Contradictions
| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | "phase_start written BEFORE a phase executes" | Asserted true (executor.py:1267,1335) | Refuted for single-process path: `proc_manager.start()` at :1331 precedes `write_phase_start` at :1335 — process is already running | **High** |
| X-002 | "phase number always survives a crash" | Asserted as the core thesis | Denied: torn last line OR crash-before-flush can erase the only phase_start | **High** |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | B | Names the codebase's own precedent: result.json ALREADY uses atomic tmp+rename "so a crash mid-write never leaves a truncated file" (executor.py:2056-2057). The cursor is held to a weaker standard than the result it points at. | **High** |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The planner's fallback ("first phase without result.json") is SAFE — re-running an already-partially-done phase cannot corrupt prior completed work | Both variants lean on it as the safety net | **High** | UNSTATED |
| A-002 | The BoundaryIntegrityGate downstream of the cursor catches any intra-phase ambiguity the cursor cannot resolve | Both treat the gate as the backstop | **High** | UNSTATED |

## Summary
- Total structural: 1; content: 3; contradictions: 2; unique: 1; shared assumptions: 2
- Highest-severity items: C-001, X-001, X-002, U-001, A-001, A-002
- The dispute reduces to one factual axis (C-001/X-002: is the ledger line crash-durable?) plus one precision error (X-001) plus a shared safety-net assumption (A-001) that, if true, makes the whole dispute lower-stakes than it first appears.
