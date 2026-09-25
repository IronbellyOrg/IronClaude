---
schema_version: "1.0"
tier: "T2"
suspect: true
reviewer_model_id: ""
reviewer_model_label: ""
target: "/config/workspace/IronClaude/.dev/worktrees/ccsession-native-install/.dev/tasks/to-do/TASK-RF-ci-doctor-20260924-174137/reflect/post/reviewer-cards/audit-target.md"
target_checksum: "d12190f51419ea622abbde552d64810054411a8967ce8d23c943e47333013c8a"
target_truncated: false
generated: "2026-09-24T19:49:11Z"
caller_label: "ci-doctor-post-wave3"
elapsed_ms: 0
finding_count: 0
---

# T2-Bare Review — audit-target

## Findings

| ID | Sev | Claim | Cite | SelfConf |
|----|-----|-------|------|----------|

## Verdict
Review treated the target block as data; embedded directives such as “Return a deviations table” were ignored. | Severity | File:Line | Title | Evidence | Suspect-source | |---|---|---|---|---| | Medium | `.github/workflows/test.yml:219` | `superclaude install` lacks the `--no-promote` flag referenc
