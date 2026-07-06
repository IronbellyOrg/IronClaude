---
topic: "Update /sc:reflect and related monitor workflows to guide creation of locked Augment detection contracts when missing"
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-07-01T14:26:34+00:00
---

# Seed Brief: reflect-detection-contract-flow

## Problem Statement

`/sc:pr-submit --monitor >=1` correctly fails closed when no locked Augment detection contract exists, but the current operator experience ends at an abrupt "probe first" halt. The desired improvement is a structured, safe contract-creation path that can diagnose contract state, gather or accept real probe evidence, propose defaults, validate them against captured GitHub review payloads, and only then write a project-local locked contract for monitor workflows.

## Known Context

- `sc:pr-submit` currently loads `DetectionContract.for_arming()` at monitor ordinal L1+ and refuses to arm unless a locked contract resolves.
- The arming resolution prefers the operator-local gitignored override at `.dev/pr-monitor/detection-contract.locked.md` and falls back to the shipped `refs/detection-contract.md`, which remains `locked: false`.
- The shipped contract schema includes Augment identity fields, emission shape, findings locus, severity path, review completeness signal, probe evidence, decline-detection fields, and `locked`.
- Detection is intentionally configuration, not control-flow logic: Augment bot login and shape must not be hard-coded in classifier logic.
- `/sc:reflect` already functions as a structurally independent audit/gate workflow and has both command and protocol surfaces; `/sc:pr-submit` owns PR creation, monitor arming, poll loops, retry/retrigger behavior, and side effects.
- The repository convention keeps operator/run artifacts under `.dev/`, never under `.claude/` mirrors.

## Constraints

- No bot identity, app slug, emission shape, findings locus, severity path, or completeness signal may be guessed and locked without evidence.
- Defaults may be offered as suggestions, but `locked: true` requires observed evidence from a recent Augment-authored GitHub payload.
- Contract creation must not arm a monitor, post comments, push commits, or resume `/sc:pr-submit --monitor` without explicit user confirmation.
- The shipped distributable contract must remain unlocked; repo/operator-specific locked data belongs in the gitignored local override.
- The flow must tolerate multiple review surfaces: PR review bodies, issue comments, and check-run output.
- The UX should improve the missing-contract path without weakening T-210 fail-closed behavior.
- Any command/path guidance must pin the resolved repo rather than relying on bare GitHub CLI defaults.

## Success Criteria

- Missing, unlocked, stale, or evidence-less contracts produce clear diagnosis and a safe next step instead of only an abrupt halt.
- The flow asks a bounded sequence of questions with sensible defaults, while marking evidence-required fields as un-lockable until verified.
- Generated contracts validate by dry-running the classifier against captured `gh` JSON before `locked: true` is allowed.
- Contract artifacts include a provenance link to probe evidence and a validation result that can be audited later.
- `/sc:pr-submit --monitor >=1` can reuse the validated local locked contract without changing its fail-closed arming gate.
- `/sc:reflect` can report contract status without exposing full payload contents or leaking irrelevant PR data in normal summaries.

## Open Questions

- Should orchestration live in `/sc:reflect`, `/sc:pr-submit`, a shared helper, or a new dedicated command, and which surface should own writes?
- Should `/sc:reflect` ever write the locked contract itself, or only diagnose and dispatch/recommend the shared helper?
- What exact evidence freshness threshold should define stale: time-based, repo/PR identity mismatch, commit mismatch, or app identity drift?
- Should the first implementation be interactive-only, automated-probe-only, or support both with separate modes?
- What is the minimal validation harness needed to avoid duplicating `sc:pr-submit` classifier logic?

## Enrichment Context

- Codebase retrieval confirms `src/superclaude/pr_submit/detection.py` defines `DetectionContract`, lock enforcement, local override preference, and a pure `poll_augment_review` seam over injected payloads.
- `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` Wave 1 explicitly loads `DetectionContract.for_arming()` and halts at L1+ when no locked contract exists.
- `src/superclaude/skills/sc-pr-submit-protocol/refs/detection-contract.md` is the shipped unlocked schema and documents the evidence-first R1 probe requirement.
- `src/superclaude/commands/reflect.md` delegates full behavior to `sc-reflect-protocol`; any new `/sc:reflect` behavior should be expressed in source command/skill files first and synced to `.claude/` later if implemented.
- Current architecture suggests a shared helper can prevent `/sc:reflect` and `/sc:pr-submit` from duplicating contract loading, diagnosis, evidence parsing, and classifier dry-run behavior.

Full codebase enrichment is saved in `enrichment/codebase-context.md`.
