# Implementer claims

Built a test-only fixture (29 S-cases, 76 T-check map, 47 Appendix C rows) and static tests in tests/recommend/test_routing_refresh.py, plus one T47 assertion and one README-mirror parity test.
Every case received unavailable-plugin and seeded-wrong-cache variants; the wrong-cache expectation was written uniformly as "guide route matched; cache not consulted".
A2 fix pass recorded the test log under artifacts, extended competitor checks to repeat routes, required conditional wording where a shared row names a competitor, and required concrete Appendix D rows.
Believed AC1-AC5 met; the independent A2 review found AC2 unmet: S23-S27 route through the Other-commands block (unmatched), so their seeded cache row is consulted and must be rejected by verification, not bypassed.
Static checks only; observed generation remains Task 8.
