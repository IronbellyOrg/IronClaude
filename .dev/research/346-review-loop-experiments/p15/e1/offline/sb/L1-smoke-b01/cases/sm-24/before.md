# Invoice Numbering

Status: Draft for review. Owner: Finance systems team.

## 1. Purpose

This document defines how invoice numbers are formed and assigned and how the finance team checks the numbers every night.

## Common conventions

- **DX-7 Health endpoint.** Each service exposes a health endpoint that answers within one second and reports the state of its dependencies.
- **DX-8 Canary releases.** A release is deployed to a canary group first and is widened only after 30 minutes without new errors.
- **DX-9 Feature flags.** A feature flag has an owner and a removal date, and flags older than 90 days are listed in a weekly report.
- **DX-10 Configuration.** Configuration values are read at start-up, and a change needs a restart unless the value is marked as reloadable.
- **DX-11 Error pages.** Error pages show a short message and a support code and never show stack traces or internal host names.
- **DX-12 Pagination.** List endpoints return at most 100 items per page together with a cursor that points at the next page.
- **DX-13 Search order.** Search results are ordered by relevance and then by recency, and an empty query returns no results.
- **DX-14 Image upload.** Uploaded images are scaled to a maximum width of 1600 pixels and stripped of embedded location data.

## 2. Format

- **IN-1 Prefix.** An invoice number starts with the letters `INV` followed by a hyphen and a running number of eight digits.
- **IN-2 Immutability.** Once an invoice has been issued, its number never changes and the invoice is never edited. A mistake is corrected with a credit note.
- **IN-8 Credit notes.** A credit note has its own number and names the invoice it corrects.

## 3. Numbering and checks

- **DX-15 Translations.** Every user-facing string comes from a translation file, and a missing translation falls back to English.
- **DX-16 Money format.** Monetary amounts are handled as integers in the smallest currency unit and are rounded half up for display.
- **DX-17 Metric names.** Metric names use lower-case words separated by underscores and end with the unit of the measured value.
- **DX-18 Library updates.** Third-party libraries are checked for published security advisories once a month by the owning team.
- **IN-3 Sequence.** Invoice numbers are taken from one sequence that is shared by all regions, in the order in which invoices are issued.
- **IN-4 Gap check.** The nightly reconciliation job reports every gap in the invoice sequence to the finance team.
- **IN-5 Duplicate check.** The reconciliation job does not look for duplicate invoice numbers.
- **DX-19 Interface docs.** Every public endpoint is described in the interface documentation before the release that contains it ships.
- **DX-20 Support hours.** The support team answers tickets on business days between 08:00 and 18:00 in the local time of the customer.
- **DX-21 Test data.** Test environments use generated data only and never contain copies of records that belong to real customers.
- **DX-22 Feedback form.** A feedback form is available on every page and sends its text to the product team without a reply address.
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

## Appendix: general requirements

- **DX-23 Cookies.** The site sets only the cookies that are needed for sign-in and for the language choice of the visitor.
- **DX-24 Print layout.** Pages that customers may print have a print stylesheet that hides the navigation and shows the address of the page.
- **DX-1 Keyboard access.** All interactive elements can be reached and used with the keyboard alone, and the element that has focus is always visible.
- **DX-2 Colour contrast.** Text and background colours keep a contrast ratio of at least 4.5 to 1 in every theme the product offers.
- **DX-3 Date display.** Dates are shown in the format of the user's locale and are stored in UTC.
- **DX-4 Time zones.** Scheduled times are entered in the user's time zone and converted to UTC before they are saved.
- **DX-5 Log format.** Every service writes one JSON object per log line with a timestamp, a severity and a request identifier.
- **DX-6 Log storage.** Application logs are kept for 14 days in hot storage and are then discarded by the logging platform.
