# Structural QA reviewer card

Verdict: PARTIAL — high-confidence structural issues remain.

Findings:

1. Proof-bar contradiction: real boot is called the only proof path (`merged-requirements.md:126-128`), but static binding absence plus oracle mismatch is also allowed to become Regression (`merged-requirements.md:92`, `merged-requirements.md:130-132`).
2. Contract-versioning violation: new stable fields are proposed (`merged-requirements.md:151-162`) but fixtures keep `contract_version: "1.5.0"` (`merged-requirements.md:269-274`), while the current protocol says 1.5.0 is D13-only (`SKILL.md:660-663`) and new top-level fields require a minor bump (`SKILL.md:870-878`).
3. Disable path is underspecified across CLI surfaces: slash docs only (`merged-requirements.md:189-191`) vs no wrapper option (`commands.py:80-147`) and no prompt forwarding (`runner.py:341-366`).
