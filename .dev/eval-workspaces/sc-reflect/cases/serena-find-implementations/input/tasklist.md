# STUB — V3-Serena eval scaffold (FR-RV3-LOW.1, UC-1). Body fleshed out in a later iteration.
# Tasklist DELIBERATELY omits the AdyenHandler implementor (R-004) to create an
# interface-coverage gap: find_implementations enumerates 3 implementors of PaymentHandler but
# only 2 are wired by tasks → missing_implementations = [AdyenHandler] → Drift.

- Task 1: Implement PaymentHandler interface with authorize()/capture(). (covers R-001)
- Task 2: Implement StripeHandler. (covers R-002)
- Task 3: Implement PaypalHandler. (covers R-003)
# R-004 (AdyenHandler) deliberately NOT covered → coverage gap for the find_implementations audit.
- Task 4: Define RetryPolicy trait (LSP kind=Class — C3 misreported trait). (covers R-005)
- Task 5: Implement ExponentialBackoff. (covers R-006)
- Task 6: Define Serializer Protocol on the LSP-unsupported backend (FR-1.4 degraded path). (covers R-007)
