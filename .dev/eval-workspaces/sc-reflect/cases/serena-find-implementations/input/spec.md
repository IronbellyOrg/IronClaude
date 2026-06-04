# STUB — V3-Serena eval scaffold (FR-RV3-LOW.1, UC-1). Body fleshed out in a later iteration.
# UC-1 coverage audit of an ABSTRACT symbol whose polymorphic surface find_implementations must enumerate.
# Discriminating signals: (a) an abstract symbol with multiple implementors, some unwired by the
# tasklist (coverage gap → interface-coverage Drift); (b) a misreported-trait case (LSP reports
# kind=Class for a Rust/TS trait — C3 guard must still fire on Class); (c) an LSP-error scenario for
# the FR-1.4 degraded path (find_implementations:lsp_unsupported).

## Requirements

- R-001: System SHALL define a `PaymentHandler` interface (abstract) with `authorize()` / `capture()`.
- R-002: System SHALL provide a `StripeHandler` implementation of `PaymentHandler`.
- R-003: System SHALL provide a `PaypalHandler` implementation of `PaymentHandler`.
- R-004: System SHALL provide an `AdyenHandler` implementation of `PaymentHandler`.
- R-005: System SHALL define a `RetryPolicy` trait (Rust) — note: the LSP reports its kind as `Class`
  (misreported trait, C3); find_implementations MUST still be invoked on it.
- R-006: System SHALL provide a `ExponentialBackoff` implementation of `RetryPolicy`.
- R-007: System SHALL define a `Serializer` Protocol whose backend is on an LSP that returns a
  tool-unsupported error for find_implementations (FR-1.4 degraded-path fixture).
