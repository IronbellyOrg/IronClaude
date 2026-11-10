# Invoice Numbering

Status: Draft for review. Owner: Finance systems team.

## 1. Purpose

This document defines how invoice numbers are formed and assigned and how the finance team checks the numbers every night.

## 2. Format

- **IN-1 Prefix.** An invoice number starts with the letters `INV` followed by a hyphen and a running number of eight digits.
- **IN-2 Immutability.** Once an invoice has been issued, its number never changes and the invoice is never edited. A mistake is corrected with a credit note.
- **IN-8 Credit notes.** A credit note has its own number and names the invoice it corrects.

## 3. Numbering and checks

- **IN-3 Sequence.** Every region numbers its invoices from a sequence of its own, and the region code is part of each number.
- **IN-4 Gap check.** The nightly reconciliation job reports every gap in the invoice sequence to the finance team.
- **IN-5 Duplicate check.** The reconciliation job lists each number that occurs twice in the sequence that all regions share.
- **IN-6 Time of assignment.** A number is assigned at the moment the invoice is issued, not when the draft is created.

## 4. Archive

- **IN-7 Archive.** Issued invoices are archived as PDF files for ten years and can be found by invoice number.
- **IN-9 Export.** Finance can export all invoices of a month as one file for the accounting system.
- **IN-10 Currency.** An invoice shows amounts in the currency of the customer and states the exchange rate when it differs from the base currency.
- **IN-11 Delivery.** An issued invoice is sent to the billing contact of the customer within one hour and is also available for download from the customer portal.
- **IN-12 Late payment.** An invoice that is unpaid 30 days after its issue date is marked overdue, and the customer receives one reminder with a copy of the invoice.

## 5. Acceptance criteria

1. Two invoices issued in the same second receive different numbers.
2. The nightly job reports a missing number to finance.
3. A credit note names the invoice it corrects.
