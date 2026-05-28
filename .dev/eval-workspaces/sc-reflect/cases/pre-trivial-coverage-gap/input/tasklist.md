# STUB — iteration-1 follow-up fleshes out content. Spec §12.3 row 1.

# Tasklist (deliberately omits R-007 and R-008 → coverage_pct = 6/8 = 0.75)

- Task 1: Implement `/signup` endpoint accepting email + password (covers R-001).
- Task 2: Wire RFC-5322 email validator (covers R-002).
- Task 3: Add MX-record DNS lookup with timeout (covers R-003).
- Task 4: Wire bcrypt password hashing with cost factor 12 (covers R-004).
- Task 5: Implement transactional confirmation-email sender with retry queue (covers R-005).
- Task 6: Add per-IP token-bucket rate limiter at 5 req/min on `/signup` (covers R-006).
