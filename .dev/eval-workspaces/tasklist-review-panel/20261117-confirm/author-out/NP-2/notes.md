# Notes for NP-2 (TASK-WF-detachTheCcsessi-20261102-034618)

## Dropped findings

- M3 (os.setsid() unconditional, hand-started non-leader shim loses Ctrl-C): report tags it [INFERRED]; the plan follows remediation-source.md item 2 literally, so the gap is in the source design, not in the plan text.
- M4 (off-path PR review and /sc:reflect post not a plan task): scope remark; the source scope is 'exactly these, nothing else'.
- M9 (already-running shims keep old code, no rollout note): the plan forbids install/update by design and follows the source scope; the CHANGELOG sentence was added during implementation. Judged a scope remark, not a plan defect.
- M10 (reparented shim goes to nearest subreaper): report tags it [INFERRED] and says it was not confirmed.
- Informational: stale line anchors (plan:64 lines 801-804, plan:21 ccsession:722): report says they matched the source when the plan ran and rejected them as a defect.

## Verification and caveats

- Base: the first 'start sha=' value in progress.md (6aa687ed...) is a tree hash that is not in the object database. The HEAD commit recorded at task start in artifacts/retries/T1/q0-head (f90877be1db0fc68c40205a763bd6b7d874aa0db) is a real commit (2026-10-31) and is used as base. Files the plan edits exist at base (ccsession, local-gateway-alias-proxy.py, tests/unit/test_ccsession_tiers.py, CHANGELOG.md, Makefile); test anchors (StandInGateway 488, shim fixture 575, _real_launch 1344, busy-shim test 1379) and the setup_shim start statement exist at base.
- Not at base: the untracked .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/ folder (remediation-source.md and the live-check scripts) that the plan cites. The sandbox will not have it; none of the 9 items needs it except GT3 (source wording 'ends with message_stop', verified in the working tree copy).
- Plan text verified: sha256 of the done-folder plan equals the PLAN: hash in progress.md (15b1a9a4...), git history shows a single commit for the file, and every plan line cited by the report (19,20,21,23,29,32,34,38,40,44,50,56,64,69,70,82) says what the report says. Line anchors drifted against HEAD only in repo files, not in the plan.
- No blocking items: the report verdict is PASS with 3 medium and 8 minor findings; no implementation-time review record exists for this package (artifacts/retries holds only prompts).
