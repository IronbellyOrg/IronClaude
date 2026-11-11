### Variant 2 Advocate (opus, qa)

**Position summary.** V2's unique blocking finding C-002 holds: source.md:46 requires "An exit 2 from the reviewer's own call is corrected once and re-run"; the literal `## Fix Budget` reviewer paragraph (source.md:120) handles only exits 3, 4, 5 and 70; the exit-2 retry exists only in the reviser brief (source.md:127); plan Task 5 Region 4 (plan:117) copies the block and adds only the owner sentence; coverage-matrix.json:269-272 credits INF-028 to "Task 8", which writes INSTALL.md and brief copies. V2's weakness is coverage: it missed C-001 and C-009.

**Steelman V1.** Broadest card; 486 - 12 + 26 = 500 at the `-gt 500` limit (Makefile:399-403); found test_routing_refresh.py breakage (:33, :647-648); C-006 real (plan:64 never defines gross, net, add-only); highest calibration 0.81.
**Steelman V3.** Most concrete fixes; C-001 names the exact set edit and precedent comment (:29-32) and flags missing permission; C-009 catches an AC that may never pass; C-011 grounded at test_worker_contract.py:1940-1950.

**Strengths claimed.** C-002 holds in all three places; fix is one sentence in Region 4 plus a pin; Task 7 inherits via byte identity (plan:147). C-003 is a literal departure (source.md:90 vs plan:119, :124).

**Weaknesses in others.** V1 and V3 accept the literal block as complete (A-002) and miss C-002. V3 grades C-009 minor although no dont_write_bytecode setting exists (Grep: none); V3's "can never fail as substring" (C-008) is wrong. V1 adds test_model_alias_policy.py without evidence (X-002); V1's own C-004 arithmetic passes `-gt 500`, so it is a risk, not a failure.

**Concessions.** V2 missed C-001 (real blocking) and C-009; its 0.96 self-confidence was overstated. C-003 is weaker than filed: before Task 5 the command does not exist.

**Shared assumptions.** A-001: QUALIFY — C-001 is blocking either way (silent breakage, or Task 5 stops blocked under plan:119 with no permitted edit). A-002: REJECT — verified false; spec-internal contradiction copied by the plan; coverage matrix claims coverage falsely.

**Per-point positions.**
- S-001 n/a — V1; S-002 n/a — tie V1/V3
- C-001 include-blocking — V3 (V1 equal on facts)
- C-002 include-blocking — V2
- C-003 include-minor — V2
- C-004 include-minor — V1 (500 passes `-gt 500`)
- C-005 include-minor — V1
- C-006 include-minor — V1
- C-007 include-minor — V1
- C-008 include-minor — V3
- C-009 include-blocking — V3 (calibrator grade; importlib writes .pyc with absolute path; grep prints "Binary file matches"; reasoned, not run)
- C-010 include-minor — V3
- C-011 include-minor — V3 (already caught by plan:124 run)
- C-012 include-minor — V1
- C-013 include-minor — V1
- X-001 include-minor — V2 fact / V3 impact
- X-002 exclude — V3
- A-001 exclude as separate item — tie (C-001 blocking either way)
- A-002 include-blocking (merged with C-002) — V2
