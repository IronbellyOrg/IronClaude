---
schema_version: "1.0"
tier: "T2"
suspect: true
reviewer_model_id: ""
reviewer_model_label: ""
target: "<<TARGET>>"
target_checksum: "c8ce0d9b805943cb7aa8b27f36d4c951a92f37648fde216bc89084abc67cecba"
target_truncated: false
generated: "2026-06-01T17:59:55Z"
caller_label: ""
elapsed_ms: 0
finding_count: 5
---

# T2-Bare Review — _review_target

## Findings

| ID | Sev | Claim | Cite | SelfConf |
|----|-----|-------|------|----------|
| F-01 | crit | password hash uses md5 instead of bcrypt | auth/login.py:42 | 95 |
| F-02 | high | session token never rotated after privilege change | auth/session.py:118 | 80 |
| F-03 | med | rate-limit window is per-process not cluster-wide | auth/rate_limit.py:55 | 65 |
| F-04 | low | comment in `validate_email` references removed API | auth/login.py:201 | 40 |
| F-05 | nit | trailing whitespace in 3 docstrings | none | 15 |

## Verdict
Two real bugs (md5 hash, session-token rotation); rate-limit caveat worth confirming on cluster deploy; remaining items cosmetic.

## Notes
Did not have time to trace OAuth fallback path; recommend a follow-up pass on auth/oauth.py.
