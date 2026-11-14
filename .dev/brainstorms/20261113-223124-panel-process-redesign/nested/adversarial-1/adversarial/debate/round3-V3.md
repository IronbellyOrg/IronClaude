INV-001 | ACCEPT | Pre-register selection-recall floors, log candidates; ranking must beat random offline.
INV-002 | QUALIFY | Require final-message ledger; earlier text cannot affect promotion or ledger_missing.
INV-003 | ACCEPT | Publish break-evens: 14-second pre-pass and 2.75 seconds/item at b=100; measure panel means and medians.
INV-004 | ACCEPT | Expect consistency only for C4/C5/C8; pre-register act-rate tolerances.
INV-005 | QUALIFY | Copy PROBLEM verbatim; validate unique legal IDs ≤16, plan anchors 12–200, claims ≤300, category, MINOR/non-blocking; insert inside one findings block, otherwise log/skip.
INV-006 | ACCEPT | Recompute consensus-only matrices with selection factors; discard original averages.
INV-007 | ACCEPT | Parse JSON-lines ledger-v1; normalize whitespace for matching and report format-induced demotions.
INV-008 | ACCEPT | Guard at 1.5×(baseline+overhead) from reviewer launch; report kills/retries and intention-to-treat totals.
INV-009 | ACCEPT | Full-size planted hold-outs need ≥8 candidates/class and clean twins.
INV-010 | QUALIFY | Budget rows per recipe; replicate only with attached evidence and spare capacity; log missing ledgers.
INV-011 | QUALIFY | Assign within 24-slot capacity, reducing replicas without attached output; failures never increase survivors’ loads.
INV-012 | ACCEPT | Specify serial pre-pass only; parallel is a separate arm.
INV-013 | ACCEPT | Missing source disables C2; record no_source, non-applicability, and working-tree snapshot identity.
INV-014 | ACCEPT | Measure displacement, plan 0.1–0.9, reserve half-time free review, retain blocking non-regression gate.

(a) Accept final-only fenced ledger parsing and promotion, with concatenation diagnostic only.
(b) Accept serial-only mode.
(c) Accept offline recall and above-random derivation gates before model arms.
(d) Accept the narrowed claim and consensus-only, selection-adjusted tables.
(e) Accept min(15s,0.10×b), pre-pass-start clock, no luna re-ask, six/luna plus ember remainder, and unattached-output replica 1.
(f) Accept zero findings for killed or retried reviewers.

INV-005: Choose V2’s copying because rewriting introduces harness-authored claims.
INV-002: Choose V2’s final-only promotion because earlier text is outside the retained report.
