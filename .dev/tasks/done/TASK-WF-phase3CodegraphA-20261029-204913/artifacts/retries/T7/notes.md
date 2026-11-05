197babbd1a149091d4375f09540e1b01da8e2d1d
A1 r1-1 F1.1 note src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:4 chk=n,n,n,y(anchor not in plan Constraints or task instruction; read-back failed) The skill allowlist names mcp__codegraph__codegraph_node, which its body never calls (source §1.1 ALLOW row).
A1 r1-1 F1.2 minor src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:220 chk=n,n,n,n The needs-grounding step lists auggie, codegraph or Grep with "or"; read literally an empty codegraph answer could drop a finding before Grep is tried.
A1 r1-1 F1.3 minor .dev/codegraph-migration/progress/P3-C.md:16 chk=n,n,n,n Comment C's extra-run claim (1044 passed) has no saved log in the package artifacts.
A1 r1-1 F1.4 note tests/skills/test_codegraph_adoption.py:54 chk=n,n,n,n Only some tests are parametrized, by file rather than (file, token) pairs; every required assertion is present.
