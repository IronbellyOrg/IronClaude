# Implementer claims

Restored attempt-2 files byte-for-byte after the registered revert, then applied brief 3 only.
Fixture: S23-S27 (Other-commands, unmatched) seeded-wrong-cache expectations now say the hint is consulted, rejected by current verification and binding, live discovery selects the Other-commands target, no hit telemetry, cached candidate never emitted; routing-row cases unchanged.
Tests: wrong-cache assertion branches on guide block; new guard test ties bypass wording to matched rows; Step 0 check adds the no_match limit and the continue-to-cache rule; new hot-path check pins hint-only and reject-to-live-discovery wording; anchored conditional-step guard replaces the substring check, with a negative self-check.
Observed: 353 passed, 4 failed (all Task 7 mirror/copy parity). Static checks only; generation remains Task 8.
Independent A3 review: AC1 unmet (S28 --level beginner is not a declared explain value; flag test checks only the flag name) and AC2 unmet (S23/S25/S26 seeded keys are not keys the classifier would return for those requests, so the hint-consulted expectation is not reachable; key check is membership only).
