# Tasklist (fixture) — serena-verify-drift-guard (FR-4.8 / M-COR2)

# The verify run emits build/test cache artifacts INTO the work-unit input tree.
# VERIFICATION_ARTIFACT_EXCLUDES must filter them at BOTH input-tree construction AND
# the Wave-5/Wave-7 recompute so input_tree_sha256 does NOT change → no spurious STOP.
- Task 1: `pytest` emits `.pytest_cache/`, `__pycache__/`, `*.pyc`, `.coverage`
- Task 2: confirm the run completes (status: success), no input_drift STOP
