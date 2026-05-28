# Discovery 02 — audit.log Writer Pattern in sc-troubleshoot-protocol SKILL.md

**Source:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**Date:** 2026-05-27
**Grep command:** `grep -nE 'audit(\.log)?' src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`

## Enumerated references

| Line | Wave/Section | Verbatim phrasing |
|------|--------------|-------------------|
| 46 | Output Contract | `` `audit_log_path` `` field, "Absolute path to `audit.log`" |
| 50 | Output Contract | `test_file_path` description references "repo root recorded in the audit log" |
| 108 | Wave 0 Step 5 | **"Open audit log; emit machine-readable header:"** |
| 123 | Wave 0 Exit criteria | "audit log opened" |
| 140 | Wave 1 (auggie/serena fallback) | "fall back to `Glob` + `Grep` on the issue keywords; **note the fallback in the audit log**" |
| 146 | Wave 1 Exit criteria | "auggie + serena results **captured in audit log**, or `Glob`/`Grep` fallback **noted** ... 'no repro available' **recorded in audit**" |
| 168 | Wave 1.5 Step 5 | "**emit** `doc_context_card_path: <output-dir>/doc-context.md` **in the audit log** so Wave 5 can wire it into the report" |
| 186 | Wave 1.5 token-budget | "If it goes over 3k Claude tokens, **audit-log the overrun**" |
| 200 | Wave 1.7 (calibrator fallback) | "fall back to inline orchestrator calibration against the rubric and **mark `calibration: inline-fallback` in the audit log**" |
| 202 | Wave 1.7 Exit criteria | "calibration report at `<output-dir>/tier1-calibration.md` (or `calibration: inline-fallback` **in audit**), and the calibrated confidence **in the audit log**" |
| 226 | Wave 2 On-escalate | "**record the `escalation_reason` in the audit log** and proceed to Wave 3" |
| 275 | Wave 3 Failure handling | "Continue with remaining agents; **record failure in audit**" |
| 276 | Wave 3 Failure handling | "Fall back to `Grep`/`Glob`; **note in audit**" |
| 277 | Wave 3 Failure handling | "Continue without external docs; **note in audit**" |
| 279 | Wave 3 Failure handling | "Proceed to Wave 4; **warn in audit** that no fix is strongly supported" |
| 304 | Wave 4 Step 4 | "**Record the result in the audit log**. If self-review flags a blocker..." |
| 333 | Wave 5 Step 4 | "**Append the machine-readable footer to the audit log**:" |
| 355 | Wave 5 Exit criteria | "`REPORT.md` written, **audit log finalized**, user notified" |
| 420 | Error Handling | "Fall back to `Grep` + `Glob` for grounding; **mark in audit**" |
| 426 | Error Handling | "Pick the highest-confidence Tier 2 fix proposal as the chosen fix; **note in audit** and report header" |
| 432 | Error Handling | "Fall back to inline orchestrator calibration for that card; **mark the card with `calibration: inline-fallback` in the audit log**" |

## Inferred convention

The audit-log writer is **NOT specified as a particular tool**. Every reference is **free-form English prose** instructing the orchestrator to append/note/mark/record/emit/capture something in `audit.log`. The skill body does NOT name a literal Bash command (e.g., `printf >> audit.log`), nor does it name an Edit-tool pattern, nor does it specify a structured schema for inter-wave entries.

**Structured entries** (HTML-comment-fenced blocks) appear ONLY twice:
- **Opening header** (Wave 0 L108, format shown L110-121): `<!-- SC:TROUBLESHOOT:TARGET ... -->`
- **Closing footer** (Wave 5 L333, format shown L335-346): `<!-- SC:TROUBLESHOOT:SUMMARY ... -->`

Everything between header and footer is **free-form prose append**. The closest pattern to Change F's new entries is the existing `calibration: inline-fallback` marker (L200, L202, L432), which uses a `<event>: <state>` key-prefix idiom.

## Recommended phrasing for Change F's three new audit-log entries

Aligning with the observed `<event>: <state>` idiom from `calibration: inline-fallback`:

| Event | Recommended audit-log line | Modelled on |
|-------|---------------------------|-------------|
| Missing/malformed sibling | `calibration: missing card=<absolute card path>` | `calibration: inline-fallback` (L200, L432) |
| One-shot retry attempted | `calibration: retry card=<path> timeout=120s` | Same `calibration:` namespace |
| Force-degrade applied | `calibration: force_degraded card=<path> self_reported=<x> floored=0.65 calibration_status=failed_to_calibrate` | Same `calibration:` namespace |

For the inserted gate text in SKILL.md, the instruction should use English-prose append language matching the existing convention, e.g.:

> "Log `calibration: missing` for each missing sibling **in `audit.log`** with the absolute card path."

(Verbs to mirror existing pattern: **log**, **note**, **mark**, **record**, **emit**, **append**.)

The free-form append nature means Change F's gate text does NOT need to name a tool (Bash, Edit, Write) — the orchestrator picks the same mechanism it already uses for the other 21 audit-log references.

## Confirmation

All 21 lines verbatim-quoted from grep output. No paraphrasing. No fabricated phrasings.
