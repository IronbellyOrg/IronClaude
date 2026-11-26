<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (flags-user.md) -->
<!-- Merge date: 2026-11-26 -->
# Flags decision

<!-- Source: Base (original) -->
- Decided by: user (taken as given), confirmed by issue-worker-t1 (independent variant agrees on every value)
- Depth: deep

| Field | Value | Reason |
|---|---|---|
| Mode | bug | passed as `--mode bug`; the independent variant also picks bug (a reported crash) |
| Type | skill | passed as `--type skill`; the independent variant also picks skill (sc-issue-protocol) |
| Issue type | Bug | derived from the mode and the area by the rule in `refs/labels.md` |
| Complexity | Complex | follows depth (quick = simple, standard = medium, deep = complex) |

<!-- Source: Variant 2 (flags-t1.md), Mode row reason — merged per Change #1 -->
Verification note (for the body draft, not the flags): `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` does not exist in this checkout, and the command already STOPs on an empty `--create` description before Activation (`commands/sc/issue.md:56`).
