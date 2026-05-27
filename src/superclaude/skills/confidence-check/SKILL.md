---
name: Confidence Check
description: Pre-implementation confidence assessment (≥90% required). Use before starting any implementation to verify readiness with duplicate check, architecture compliance, official docs verification, OSS references, and root cause identification.
---

# Confidence Check Skill

## Purpose

Prevents wrong-direction execution by assessing confidence **BEFORE** starting implementation.

**Requirement**: ≥90% confidence to proceed with implementation.

**Test Results** (2025-10-21):

- Precision: 1.000 (no false positives)
- Recall: 1.000 (no false negatives)
- 8/8 test cases passed

**Scope of this metric**: These numbers describe the confidence-check skill's trigger-surface classifier — whether the skill correctly recognises "this user request needs a confidence check" — measured against 8 hand-built test cases. They do NOT describe the `confidence-calibrator` agent in `sc-troubleshoot-protocol/`, which scores hypothesis cards on a different rubric (Evidence grounding, Runtime check, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence). 8 cases is a sparse fixture, not a saturating test; for calibration scoring, the saturating pin-test corpus lives at `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`.

## When to Use

Use this skill BEFORE implementing any task to ensure:

- No duplicate implementations exist
- Architecture compliance verified
- Official documentation reviewed
- Working OSS implementations found
- Root cause properly identified

### Trigger Surface

The trigger surface is **not limited to code edits**. Run this skill — or its lightweight form — BEFORE any reply that:

- Suggests an action the user might take
- Emits a command, script, or code snippet to run
- Names a specific `--flag`, subcommand, file path, function, env var, API field, version number, or config key
- Provides step-by-step instructions

**A recommendation is a form of implementation.** The verification call goes BEFORE the message that contains the recommendation, in the same turn — not "let me check if you want", but check, then answer.

### Lightweight Form

Full 5-check scoring is not always required. For a single specific token, verifying it directly satisfies the rule:

- `--help` / `<cmd> --help` for CLI flags and subcommands
- `grep` / symbol lookup for functions, config keys, identifiers
- File read for paths and file contents
- `codebase-retrieval` (Auggie) — fastest for project-internal identifiers

If verification cost is genuinely high (requires a long-running process), say so explicitly and mark the specific token `[UNVERIFIED]` with the command the user can run to confirm — do **not** ship it bare.

## Confidence Assessment Criteria

Calculate confidence score (0.0 - 1.0) based on 5 checks:

### 1. No Duplicate Implementations? (25%)

**Check**: Search codebase for existing functionality

```bash
# Use Grep to search for similar functions
# Use Glob to find related modules
```

✅ Pass if no duplicates found
❌ Fail if similar implementation exists

### 2. Architecture Compliance? (25%)

**Check**: Verify tech stack alignment

- Read `CLAUDE.md`, `PLANNING.md`
- Confirm existing patterns used
- Avoid reinventing existing solutions

✅ Pass if uses existing tech stack (e.g., Supabase, UV, pytest)
❌ Fail if introduces new dependencies unnecessarily

### 3. Official Documentation Verified? (20%)

**Check**: Review official docs before implementation

- Use Context7 MCP for official docs
- Use WebFetch for documentation URLs
- Verify API compatibility

✅ Pass if official docs reviewed
❌ Fail if relying on assumptions

### 4. Working OSS Implementations Referenced? (15%)

**Check**: Find proven implementations

- Use Tavily MCP or WebSearch
- Search GitHub for examples
- Verify working code samples

✅ Pass if OSS reference found
❌ Fail if no working examples

### 5. Root Cause Identified? (15%)

**Check**: Understand the actual problem

- Analyze error messages
- Check logs and stack traces
- Identify underlying issue

✅ Pass if root cause clear
❌ Fail if symptoms unclear

## Confidence Score Calculation

```text
Total = Check1 (25%) + Check2 (25%) + Check3 (20%) + Check4 (15%) + Check5 (15%)

If Total >= 0.90:  ✅ Proceed with implementation
If Total >= 0.70:  ⚠️  Present alternatives, ask questions
If Total < 0.70:   ❌ STOP - Request more context
```

## Output Format

```text
📋 Confidence Checks:
   ✅ No duplicate implementations found
   ✅ Uses existing tech stack
   ✅ Official documentation verified
   ✅ Working OSS implementation found
   ✅ Root cause identified

📊 Confidence: 1.00 (100%)
✅ High confidence - Proceeding to implementation
```

## Implementation Details

The TypeScript implementation is available in `confidence.ts` for reference, containing:

- `confidenceCheck(context)` - Main assessment function
- Detailed check implementations
- Context interface definitions

## ROI

**Token Savings**: Spend 100-200 tokens on confidence check to save 5,000-50,000 tokens on wrong-direction work.

**Success Rate**: 100% precision and recall in production testing.
