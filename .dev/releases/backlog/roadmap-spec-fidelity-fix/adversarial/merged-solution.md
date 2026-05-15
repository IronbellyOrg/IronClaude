# Merged Solution — Roadmap Spec-Fidelity Convergence Fix

<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant S2 (route-findings-to-roadmap-target) -->
<!-- Incorporated: S1 (sanitize-file-path-extraction), S5 (context-aware-nfr-severity) -->
<!-- Merge date: 2026-05-15T14:07:30Z -->

## Problem Statement
<!-- Source: Base (S2), preamble -->
The roadmap pipeline halts at `spec-fidelity` because the 3-run convergence loop cannot reach 0 ACTIVE HIGHs. The 10 surviving HIGHs share two pathologies that compound:

1. **No remediation target** — every finding has `files_affected=[]`. Agents have no file to edit; they fall back to rewriting the TDD spec (an immutable input), producing 71.3% / 38.1% diffs that the 30% guard rejects.
2. **Findings include parser noise** — 4 of 10 are URL fragments, brace expansions, and backtick-line-number artifacts that should never have been emitted as findings. The other 4 are NFR keyword mismatches that aren't really HIGH-severity defects.

## Solution Overview

Three coordinated changes, layered:

| Order | Change | What it does | HIGHs resolved |
|-------|--------|--------------|----------------|
| 1 | **S1: Sanitize parser** | Filter out URL fragments, brace expansions, line refs at extraction time | 4 phantoms removed |
| 2 | **S2: Route + actionable guidance** | Give every finding a `files_affected` target (roadmap.md) and per-mismatch `fix_guidance` so agents make small additive edits | 2 legit manifest gaps become remediable |
| 3 | **S5: Context-aware NFR severity** | Iterate `check_nfrs` per section, preserve `heading_path`, demote NFR softs to MEDIUM unless under a strong-NFR heading | 4 NFR softs demoted (gate is HIGH-only) |

Expected outcome: **10 HIGHs → 0 HIGHs in Run 1, no Run 2/3 needed.**

## Detailed Changes
<!-- Source: Variant S1, refactored, with full content elided — see solutions/S1-sanitize-file-path-extraction.md -->
<!-- Source: Variant S2 base, with full content elided — see solutions/S2-route-findings-to-roadmap-target.md -->
<!-- Source: Variant S5, refactored, with full content elided — see solutions/S5-severity-reclassification.md -->

(Full per-solution content is preserved in the individual `solutions/Sx-*.md` files. The implementation tasklist at `TASKLIST.md` extracts the actionable steps.)

## Deferred (Not Merged)
- **S3** (tiered diff-relax) — fixes a different failure shape; reconsider if 30% rejections recur with correctly-routed agents.
- **S4** (budget overhaul) — falsified its own premise during debate; observability cleanup deferred to follow-up.
- **S6** (MANUAL_TRIAGE halt) — defensive safety net; reconsider only if S1+S2+S5 fails to converge.

## Backup / Workaround (in case the merged fix still fails)

See `BACKUP-WORKAROUND.md` (created alongside this document). Short version: temporarily set `--max-runs 5` and `--allow-regeneration` on the CLI to force-progress through the spec-fidelity gate, accept the resulting tasklist as draft, and triage by hand. This is the escape valve while a real fix is being merged.
