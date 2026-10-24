# Implementer claims

Restored attempt-3 files byte-for-byte after the registered revert, then applied brief 4 (advice-4-b) only.
Fixture: S28 now expects --level basic; S23-S27 seeded-wrong-cache expectations cover both outcomes: if dispatch hits the seeded key the hint is rejected (miss_validation_stale), on a miss (unknown -> no_key, or no row) the row is unused; either way live discovery selects the Other-commands target, no hit telemetry, cached candidate never emitted.
Tests: Other-commands branch now uses a helper tied to each row key and target, with a negative check that the old unconditional wording fails; flag test checks values against enumerated [--flag a|b|c] declarations, with a negative check for --level beginner.
Observed: 355 passed, 4 failed (all Task 7 mirror/copy parity). Static checks only; generation remains Task 8.
Independent A4 review: AC1 unmet; S24 repeat (coordinated documentation) recorded on Other commands although the document-built row matches it, so the unmatched cache expectation does not fit; LOW: S12 continuation repeat omits the required release spec path; S18/S19 omit full-spec row mandatory spec-panel flags.
