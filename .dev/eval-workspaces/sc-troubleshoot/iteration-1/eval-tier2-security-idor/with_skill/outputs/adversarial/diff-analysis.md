# Diff Analysis — Fix 1 vs Fix 2

## Shared diagnosis

Both proposals agree:

- The SAST finding is correct: this is a real IDOR.
- The root cause is missing authorization after `@login_required` authentication.
- PII disclosure scope (every user) makes this high-severity.

## Where they differ

| Axis | Fix 1 (authz check) | Fix 2 (redesign) |
|------|---------------------|-------------------|
| Mechanism | Add 2 lines to existing function | New endpoint, deprecate old one |
| Blast radius | One function | API contract + mobile app |
| Time-to-ship | Today | 1–2 release cycles |
| Bug-class elimination | No — bug *prevented*, not *impossible* | Yes — parameter removed, IDOR class impossible |
| Mobile-app coordination | None | Required |
| Other-client risk | None | Requires audit of all clients |
| Testing burden | 3 tests (positive + 2 negative) | 1 test (positive only) |
| Reversibility | Trivial (`git revert`) | Painful once mobile app ships the new URL |
| DB query cost | Same (1 query) | Eliminated (uses `current_user`) |

## Critical observation

These proposals are **not mutually exclusive**. Fix 1 can ship today as the immediate IDOR closure. Fix 2 can ship over the next release window as the structural improvement. The debate is really about *whether to bundle them* or *whether to skip Fix 1 and go straight to Fix 2*.

Skipping Fix 1 means the IDOR remains open for 1–2 release cycles. For a vulnerability that exposes all users' email/phone/address/DOB, that is unacceptable.
