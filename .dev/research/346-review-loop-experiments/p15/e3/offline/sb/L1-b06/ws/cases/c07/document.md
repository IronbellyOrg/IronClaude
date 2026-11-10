# Payments service requirements

## 1. Scope
The payments service charges customers, issues refunds and records every money movement in the ledger. Terms: a charge is one attempt to collect money for one order; a capture is the point at which the money is taken.

## 2. Charges
R1. A charge is created in state pending and moves to captured only after the card network confirms the authorization.
R2. A captured charge is never modified; a correction is made by a new refund entry.
R3. The service retries a failed capture up to 3 times, with 10 minutes between attempts.
R4. After the third failed attempt the charge moves to state failed and the customer is notified by email.

## 3. Refunds
R5. A refund may be issued for any captured charge within 90 days of the capture date.
R6. The refund amount may not exceed the captured amount minus refunds already issued for that charge.
R7. A refund request older than 30 days after capture is rejected with the error code REFUND_EXPIRED.
R8. Every refund creates one ledger entry of type refund in the same transaction as the state change.

## 4. Ledger
R9. Ledger entries are append-only and carry the charge identifier, the amount in minor units and the UTC timestamp.
R10. The ledger is the source of truth for balances; the daily report is derived from it.

## 5. Reports
R11. The daily report lists every captured charge and every refund of the previous UTC day.
R12. The daily report is delivered to the finance mailbox by 06:00 UTC.

## 6. Security
R13. Card numbers are never written to the ledger or to logs; only the last four digits may be stored.
R14. Support staff may view the full card number of a charge when a customer asks for it by phone.

## 7. Notes
Amounts are integers in minor units, for example cents. All timestamps are UTC. A requirement marked R is mandatory; this document has no optional requirements.
Open items are listed by the product owner in the tracker and are not part of this document.