### Variant 3 Advocate rebuttal (opus, refactorer)

**Response to criticisms.**
- (a) C-009: conceded and already blocking in Round 1. No `dont_write_bytecode` / `PYTHONDONTWRITEBYTECODE` in pyproject.toml, Makefile, CI workflows or tests/conftest.py; plan:104 grep then matches the .pyc.
- (b) C-008 substring half: conceded (Round 1); the path-order ambiguity is real; minor.
- (c) C-011: mostly conceded. Audit scans skills/commands/agents (test_worker_contract.py:1940-1944); spec-panel.md has no git/gh write verbs; plan:124 catches new hits. Small gaps: Task 4 (plan:106) does not run the test, so a SKILL.md hit is found one task late; plan:119 read literally blocks a failure the task could fix in its own text. Minor.
- (d) C-002: conceded; V2 wins.

**Updated assessment.** V1: X-002 drop and C-012 narrowing right; plan:52 column-0 anchor is new support for C-013 (not checked by V3). V2: rebuttal (d) is the strongest new point — plan:117 already adds an owner-decision sentence to the literal block, so the C-002 fix is one sentence plus one pin. All three agree on every inclusion level and on A-001's filing.

**New evidence.** test_worker_contract.py:832-836 builds the set of commands with `## Unattended mode`; the variant removes that heading (plan:115), so that check does not fail. No `__pycache__` suppression exists anywhere in repo config.

**Position changes:** none.
