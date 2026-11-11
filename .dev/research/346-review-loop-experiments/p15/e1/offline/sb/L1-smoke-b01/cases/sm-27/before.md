# Order Refund Policy

Status: Draft for review. Owner: Payments team.

## 1. Purpose

This policy describes how the shop refunds customers for orders that are cancelled or returned. It is written for the engineers who build the refund service and for the support staff who use it.

## Common conventions

- **DX-1 Keyboard access.** All interactive elements can be reached and used with the keyboard alone, and the element that has focus is always visible.
- **DX-2 Colour contrast.** Text and background colours keep a contrast ratio of at least 4.5 to 1 in every theme the product offers.
- **DX-3 Date display.** Dates are shown in the format of the user's locale and are stored in UTC.
- **DX-4 Time zones.** Scheduled times are entered in the user's time zone and converted to UTC before they are saved.
- **DX-5 Log format.** Every service writes one JSON object per log line with a timestamp, a severity and a request identifier.
- **DX-6 Log storage.** Application logs are kept for 14 days in hot storage and are then discarded by the logging platform.
- **DX-7 Health endpoint.** Each service exposes a health endpoint that answers within one second and reports the state of its dependencies.
- **DX-8 Canary releases.** A release is deployed to a canary group first and is widened only after 30 minutes without new errors.

## 2. General rules

- **RF-1 Scope.** The policy applies to orders placed in the web shop and in the mobile app. Orders placed through marketplaces follow the marketplace rules.
- **RF-2 Cancellation window.** A customer can cancel an order until the carrier has scanned the parcel for the first time. After that the return process applies.
- **RF-6 Return window.** A customer can return an item within 30 days after delivery, provided the item is unused and in its original packaging.
- **RF-7 Order lookup.** Support staff identify an order by its order number and the name of the customer, and they see the payment method that was used.

## 3. Refunds

- **DX-9 Feature flags.** A feature flag has an owner and a removal date, and flags older than 90 days are listed in a weekly report.
- **DX-10 Configuration.** Configuration values are read at start-up, and a change needs a restart unless the value is marked as reloadable.
- **DX-11 Error pages.** Error pages show a short message and a support code and never show stack traces or internal host names.
- **DX-12 Pagination.** List endpoints return at most 100 items per page together with a cursor that points at the next page.
- **RF-3 Refund obligation.** A customer who cancels an order or returns an item within the allowed window is refunded the full price paid for it, including shipping when the whole order is cancelled.
- **RF-4 Refund method.** All refunds are issued as store credit.
- **DX-13 Search order.** Search results are ordered by relevance and then by recency, and an empty query returns no results.
- **DX-14 Image upload.** Uploaded images are scaled to a maximum width of 1600 pixels and stripped of embedded location data.
- **DX-15 Translations.** Every user-facing string comes from a translation file, and a missing translation falls back to English.
- **DX-16 Money format.** Monetary amounts are handled as integers in the smallest currency unit and are rounded half up for display.
- **RF-5 Processing time.** A refund is issued within 5 business days after the cancellation is confirmed or the returned item is received.
- **RF-8 Partial returns.** When only some items of an order are returned, only the price of those items is refunded. Shipping is not refunded for partial returns.

## 4. Support and reporting

- **RF-9 Refund log.** Every refund is recorded with the order number, the amount, the method and the staff member or system that issued it.
- **RF-10 Monthly report.** Finance receives a monthly report of the total value refunded, grouped by reason.
- **RF-11 Fraud review.** A customer with more than five refunds in 90 days is flagged for manual review before the next refund is issued.

## 5. Acceptance criteria

1. Cancelling an unshipped order refunds the full price plus shipping.
2. Returning one item of a three-item order refunds only that item.
3. Every refund appears in the refund log with the method used.

## Appendix: general requirements

- **DX-17 Metric names.** Metric names use lower-case words separated by underscores and end with the unit of the measured value.
- **DX-18 Library updates.** Third-party libraries are checked for published security advisories once a month by the owning team.
- **DX-19 Interface docs.** Every public endpoint is described in the interface documentation before the release that contains it ships.
- **DX-20 Support hours.** The support team answers tickets on business days between 08:00 and 18:00 in the local time of the customer.
- **DX-21 Test data.** Test environments use generated data only and never contain copies of records that belong to real customers.
- **DX-22 Feedback form.** A feedback form is available on every page and sends its text to the product team without a reply address.
- **DX-23 Cookies.** The site sets only the cookies that are needed for sign-in and for the language choice of the visitor.
- **DX-24 Print layout.** Pages that customers may print have a print stylesheet that hides the navigation and shows the address of the page.
