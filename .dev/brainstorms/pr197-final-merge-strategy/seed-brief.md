---
topic: "Plan the merge of open PR #197 (feat/rf-harness-sync) into master of IronbellyOrg/IronClaude"
domain: process
strategy: systematic
depth: deep
proposals_target: 5
handoff_target: none
created: 2026-06-28T17:50:00Z
---

# Seed Brief: PR #197 final merge strategy

## Problem Statement
PR #197 is git-clean (rebased onto master HEAD, MERGEABLE, 5 ahead / 0 behind, 18 files, +7920/-664) but was authored against an older reflect contract ("1.5.1" wording) while master has since advanced to 1.7.0 with a different anti-self-confirmation model. The task is product adjudication, not conflict resolution: keep #197's net-new value, keep master canonical where stronger, reduce #197 to the minimum value-adding set.

## Known Context (verified ground truth)
- master HEAD `cda6e2d`; PR #197 HEAD `b01b33e`; merge-base = master HEAD (zero-conflict confirmed).
- Master canonical: contract 1.7.0 (FR-RH1 reachability_* + FR-RSR runtime_surface_*), FR-RH2 `run_tier2_ensemble`, reviewer-isolation (`--isolate-reviewers` + read-only `reflect-reviewer`), executor-class EXCLUSION (§7.1), strict no-nesting guard.
- #197 net delta: (1) keeps contract_version 1.7.0 (changelog comment only); (2) replaces exclusion with instance-level independence; (3) re-adds runner `inline_directive` + loosens the no-nesting guard; (4) net-new value: EV-1…EV-4 on-disk verification gates, `reflect_post_mode`/`--cli`, 3 doc skills, tech-* rewrites, `/task` lens QA, rf-agent fixes.

## Constraints
- SoT = `src/superclaude/` then `make sync-dev`; never stage `.claude/` mirrors.
- PR target = fork `IronbellyOrg/IronClaude` only; `--repo` on every gh invocation.
- Terminal can't paste multi-line commands.
- No "security" framing (reliability/correctness/data-loss only).
- Produce strategy artifact only — no code edits, no PR.

## Success Criteria
- 8 required sections, each grounded in the live diff + master files.
- Two decisions adjudicated with cases for each + recommended default + exact files.
- Sequenced, validated, fork-safe merge plan.

## Open Questions (resolved during grounding)
- Which side is the structural fix for single-reviewer degradation? → master's `run_tier2_ensemble` (Decision B determinate).
- Is the directive reachable on master's ensemble route? → No; only on Tier-1, where its instructed waves don't run.
- Does EV-1/EV-2's `§7.1 N=2 floor` reference survive on master's exclusion text? → Yes (master §7.1:620).
- Is Decision A determinate? → No; near-even adversarial split → needs user sign-off.

## Enrichment Context
Codebase enrichment performed inline at higher fidelity than a generic agent: `gh pr diff 197`, `git diff origin/master..HEAD` (per-file), `git show origin/master:<path>` for all reflect files, and a 3-agent grounded adversarial panel. Research: none (`--research none`).
