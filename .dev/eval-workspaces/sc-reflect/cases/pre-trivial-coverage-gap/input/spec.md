# STUB — iteration-1 follow-up fleshes out content. Spec §12.3 row 1.

# Trivial Feature Spec — Coverage-Gap Fixture

## Requirements

- R-001: System SHALL accept user-supplied email addresses via the `/signup` endpoint.
- R-002: System SHALL validate email addresses against RFC 5322 syntax.
- R-003: System SHALL reject email addresses whose domain part lacks an MX record.
- R-004: System SHALL hash user passwords with bcrypt cost factor ≥ 12.
- R-005: System SHALL emit a confirmation email within 30 seconds of successful signup.
- R-006: System SHALL rate-limit `/signup` to 5 requests per IP per minute.
- R-007: System SHALL log all failed signup attempts with timestamp + IP + failure reason.
- R-008: System SHALL allow an administrator to revoke an account via the `/admin/revoke` endpoint.
