# Tier 2 Hypothesis Card — root-cause-analyst

## Claim

The FAIL originates inside `seed_checkout_assert` at exactly the outcome-derived checks; every other check in the live seed `ws_ssh` is proven passing under sysbox-runc by the two control runs (DinD-public for shared bytes, **sysx-blank for the same runtime**). The §8 outcome recorded in-workspace was `clone-failed` — a fast-failing `git clone` — and every alternative enum is excluded by source logic plus the observed 13.9s startup duration: `timed-out` requires burning the 120000ms budget (startup.sh:569), `runner-unavailable` spin the same budget (:707-712), `auth-*` requires git to prompt (a public anonymous clone never invokes askpass) and would burn ≥15s (:568), `checkout-unverified`/`cloned` are byte-deterministic and DinD-identical, `skipped`/`rejected-input`/`destination-conflict` are excluded by identical REPO_URL admission and fresh volume. The rerun FAIL is strictly collateral, provable from ordering: `set -euo pipefail` + `seed_checkout_assert public cloned` at test-startup-boot.sh:1962 runs before the orchestrator rerun at :1968, so the orchestrator never re-ran and the "idempotency violated (NFR18)" label is a misnomer for this run.

## Evidence

**Enumeration of the live seed ws_ssh (test-startup-boot.sh:1941-1947), in order — DinD-public-proven vs runtime-dependent:**

| # | Check | Class | Why |
|---|-------|-------|-----|
| 1 | `AIDEV_PROFILE` match (:1942) | runtime-independent | coder_env bridge identical both arms (dotfiles.tf); **proven under sysx by sysx-blank PASS** (same check ran there) |
| 2 | DOCKER_HOST⇄RUNTIME consistency (:1943) | self-consistent per arm | `coder_env "docker_host"` is count-guarded dind-only (dotfiles.tf:154-160); under sysx DOCKER_HOST is absent → asserts sysbox-runc; **proven under sysx by sysx-blank PASS** |
| 3 | aidev-startup SHA256 (:1944) | runtime-independent | image bytes identical; sysx-blank proves the stat/sha view under sysbox matches |
| 4 | askpass SHA256 (:1945) | runtime-independent | same |
| 5 | modes 0:0:755 (:1946) | runtime-independent | same; sysx userns presents baked root files as container-root 0 |
| 6a | PAT guard (:382) `[[ -z GH_PAT && -z DOTFILES_PAT ]]` | runtime-independent | workflow passes `--parameter=gh_pat=` / `--parameter=dotfiles_pat=` to BOTH arms (coder-ci-validate.yml:443-444); env delivery is `coder_env` → agent → `coder ssh` shell (ws_ssh :365-376, script piped to `coder ssh ... bash`), no sysbox-specific injection path exists in the template (only env asymmetry between arms is DOCKER_HOST, not a PAT); **decisively proven under sysx: the guard at :382 precedes the blank branch, and sysx-blank PASSED** |
| 6b | `seed-repo-outcome == cloned` (:383) | **RUNTIME-DEPENDENT** | content produced by §8 in-workspace (startup.sh:770-772) — the discriminant |
| 6c | `section.8.outcome=cloned` (:384) | **RUNTIME-DEPENDENT** | same value, second surface (startup.sh:2005) |
| 6d | `REPO_URL == octocat` (:390) | runtime-independent | parameter, identical both arms |
| 6e | outcome ∈ {cloned, preserved-valid} (:391) | **RUNTIME-DEPENDENT** | same root as 6b |
| 6f-6m | tree checks `.git`/toplevel/HEAD/HEAD:README/origin/ls-files/hash-object (:392-399) | byte-deterministic **iff tree exists** | IF §8 recorded `cloned`, these inspect identical octocat bytes and DinD-public proves them; under a failed clone the dest is absent → fail |
| 6n | `section.8.status=pass` (:401) | **RUNTIME-DEPENDENT** | derived from the same outcome (startup.sh:2006-2010: only cloned/preserved-valid → pass) |

Therefore: failure ⟺ §8 outcome ≠ `cloned` under sysbox. One root, no second defect upstream of it.

**Enum exclusion (startup.sh §8, :750-761 entry + :567-748 attempt):**
- [repo] startup.sh:569 — `seed_c=${AIDEV_CLONE_TIMEOUT_MS-120000}`: AIDEV_CLONE_TIMEOUT_MS is never set in live CI (only test-51 fixtures set it), so the clone budget is 120s, anchored when §8 starts (:580), not at boot — cold-boot slowness cannot eat it.
- [repo] startup.sh:656-668 — clone success+verified→`cloned`; success+unverified→`checkout-unverified`; clone nonzero→`clone-failed`, refined to auth classes ONLY if `$dir/auth-status` holds a category. For a public anonymous HTTPS clone git never prompts, askpass is never invoked, FD9 stays empty (startup-git-askpass.sh:16-30 writes a category only on a failed lookup request) → auth-* is unreachable for this fixture even if egress is broken.
- [repo] startup.sh:719/:734 — `timed-out` fires only at the 120s deadline; `runner-unavailable` from the ownership-wait loop (:707-712) also spins to the deadline.
- [run] Job 105657435166 startup-run.json: exit 0, `returned-success`, **duration 13.9s** (the aidev-startup agent-script timing, test-startup-boot.sh:909). Any deadline- or curl-timeout-driven enum needs ≥15-120s inside §8 alone — incompatible with a 13.9s total boot that also includes §2 dockerd wait. Only a fast-failing `git clone` (DNS failure / connection refused: sub-second) fits. → `clone-failed`.
- [repo] startup.sh:753-758 — `skipped` needs empty REPO_URL (set), `rejected-input` needs `aidev_seed_admit` failure (:509-534, pure string parsing, runtime-independent — same URL admitted under DinD), `destination-conflict` needs a pre-existing `/config/workspace/Hello-World` (fresh volume both arms, main.tf:480-483 identical). All excluded.

**Rerun collateral proof:**
- [repo] test-startup-boot.sh:1959 — sentinel append succeeded (independent ws_ssh; otherwise the failure would read "could not append idempotency sentinel").
- [repo] test-startup-boot.sh:1960-1962 — RERUN_SCRIPT is `set -euo pipefail` then `seed_checkout_assert public cloned` FIRST; with outcome ≠ cloned it returns 1 and the script exits before :1968 (`/usr/local/bin/aidev-startup`) ever runs. No execution path exists where the seed assert fails and the rerun step passes → strictly collateral, zero independent idempotency signal; the :1988 "idempotency violated — NFR18" message mislabels an unexecuted rerun.

## Consistency with docs
not_applicable (no doc describes seed-clone network behavior under sysbox-runc; run-2 doc-context carried over).

## Proposed fix (one)
Adopt the read-only SEED_OUTCOME projection in test-startup-boot.sh (Fable 6ced457 hunk): a `ws_ssh 'cat ~/.aidev/status/seed-repo-outcome; grep ^section.8 ~/.aidev/status/startup-summary'` row projected through the existing allowlist, assertions unchanged. The enum is already written by the production script (startup.sh:770-772, :2004-2010) — this only surfaces it, converting the next sysx run from binary FAIL into named-enum evidence (expected: `clone-failed`), with zero template/production change and no assertion weakening.

## Confidence
Self-reported 0.87 — decomposition: "failure is confined to the outcome-derived checks of seed_checkout_assert (one root)" 0.95 (both controls eliminate every other check); "enum = clone-failed (fast egress failure), not timed-out/auth-*" 0.78 (source-logic exclusion is airtight given the 13.9s duration; the duration figure is run evidence from tier-1's startup-run.json citation, not independently re-read); "underlying host-side network cause (DNS vs refused vs MTU)" unknown by design — unobservable from repo.

## Risks
- The 13.9s duration is inherited evidence; if it is wrong or measured a different script instance, the fast-fail deduction weakens and `timed-out` reopens (the enum projection would still name it).
- If the clone actually succeeds under sysbox and a tree check fails on a sysbox-specific fs quirk (e.g. `-L` on a shiftfs-backed path), 6f-6m become the discriminant — but DinD-public passing the identical checks makes this a low-probability residual.
- Verbatim-adoption risk of 6ced457 on this branch (base drift) — re-ground rather than cherry-pick blindly.

## If I'm wrong it's probably because...
the startup-run.json timing does not cover the moment §8 ran (e.g. the recorded run is a later re-execution), letting a 120s--budget `timed-out` or an auth-classified failure hide inside an unobserved earlier invocation — the SEED_OUTCOME projection distinguishes this immediately; or `checkout-unverified` via a sysbox-local git anomaly, which the same projection plus the section.8 rows would also expose.
