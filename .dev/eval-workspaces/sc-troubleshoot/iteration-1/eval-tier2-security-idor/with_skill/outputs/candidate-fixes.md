# Tier 2 Candidate Fixes — Distillation

All three hypothesis cards converge on the diagnosis (this IS a real IDOR — the SAST finding is correct). They differ on the *fix mechanism*.

## Fix A — Inline authorization check

**Champion**: security-engineer (primary), root-cause-analyst (variant with helper extraction), quality-engineer (as bridge)

Add `if user_id != current_user.id: abort(403)` immediately after `def get_user_profile(user_id: int):`, *before* the `User.query.get(user_id)` call.

- **Mechanism**: minimal patch, 2 lines of code (or +3 lines if extracted to a helper per root-cause-analyst).
- **Blast radius**: one function in one file.
- **Mobile app impact**: zero — URL contract unchanged, valid requests still succeed.
- **Time-to-ship**: today.

## Fix B — Redesign to `/api/users/me/profile`

**Champion**: quality-engineer (primary), security-engineer (as follow-up), root-cause-analyst (as follow-up)

Remove the URL parameter entirely. New endpoint reads from `current_user` directly. The IDOR bug class becomes structurally impossible.

- **Mechanism**: new endpoint + deprecation of old endpoint + mobile app release.
- **Blast radius**: API contract change, requires mobile-app coordinated release.
- **Mobile app impact**: yes — URL changes in the next release.
- **Time-to-ship**: 1–2 release cycles.

## Fix C — Role-based (`if user_id != current_user.id and not current_user.is_admin: abort(403)`)

**Champion**: root-cause-analyst (alternative only)

Same as Fix A but admits an admin-bypass. Considered an OUTLIER for this issue because no admin/staff requirement was stated. Drop from the debate to avoid scope creep.

## Verdict

**Status: COMPETING (between A and B), with B as a follow-up to A.**

- All 3 agents agree Fix A closes the IDOR. None oppose it.
- All 3 agents prefer Fix B as the eventual architecture. None oppose it.
- The debate is about ordering and *whether* to ship A as the *primary* answer vs treat B as the answer and skip A.

This warrants the adversarial debate (Wave 4) to decide:

- Should we ship A now and B later? (security-engineer's framing)
- Should we ship A as a bridge to B? (quality-engineer's framing — same outcome, different emphasis)
- Should we extract a helper as we patch (root-cause-analyst's variant)?

Proceed to `sc:adversarial-protocol --depth quick` (both proposals share a diagnosis, only the mechanism differs).
