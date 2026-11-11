## Label A
blocking: yes
sentence: An implementer who follows R13 and R14 builds a system where card numbers are never stored beyond the last four digits yet support staff can view the full card number; both cannot hold and satisfying R14 requires storing the full number, breaking the security rule.
evidence: document.md:27 'R13. Card numbers are never written to the ledger or to logs; only the last four digits may be stored.'; :28 'R14. Support staff may view the full card number of a charge...'
confidence: high

## Label B
blocking: no
sentence: An implementer who follows R13 keeps card numbers out of the ledger and logs, and R14 lets support staff view the full number on screen; R13 restricts writing to ledger and logs, not display, so the full-number screen only needs the added assumption that the number is stored locally.
evidence: Line 27 (R13): 'Card numbers are never written to the ledger or to logs; only the last four digits may be stored.' Line 28 (R14): 'Support staff may view the full card number of a charge when a customer asks for it by phone.'
confidence: high
