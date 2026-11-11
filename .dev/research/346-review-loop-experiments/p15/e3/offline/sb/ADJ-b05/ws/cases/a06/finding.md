**F1. CRITICAL (blocking). Expert: Whittaker (Contradiction Attack). Card numbers are both never stored and viewable in full**

- Grading sentence: an implementer who follows the stated text as written builds a ledger and logs that never hold a card number (`Card numbers are never written to the ledger or to logs; only the last four digits may be stored.`, S:27) and a support screen that shows the full card number (`Support staff may view the full card number of a charge when a customer asks for it by phone.`, S:28). Both cannot hold, so the full number must be stored somewhere and the security rule is broken, which is wrong because the storage rule is a security boundary.
- Recommendation: state that support staff see only the last four digits
- Priority: High. Quality impact: card numbers are both never stored and viewable in full
