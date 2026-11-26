# /sc:analyze .github/workflows --focus architecture --depth quick (item #807)
Master f2894fc44. Read-only; no source changed.
- F1: test.yml already runs ruff check (line 102), ruff format --check src/ tests/ (106), make verify-deps (123), verify-sync (131), lint-architecture (135) on every PR.
- F2: contract3-generator-constraint-lint.yml already requires the '## Generator-Constraint Considered' section for PRs touching gates.py, structural_checkers.py, *_validator.py.
- F3: .github/PULL_REQUEST_TEMPLATE.md has no ledger, implement or e2e line, so only the ledger link and the e2e paste (S14-F1, S14-F3) are new.

Codegraph: index_state=fresh, checked_at=2026-11-24T22:21:17Z; degraded: none
