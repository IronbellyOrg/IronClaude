# Order Refund Policy

Status: Draft for review. Owner: Payments team.

## 1. Purpose

This policy describes how the shop refunds customers for orders that are cancelled or returned. It is written for the engineers who build the refund service and for the support staff who use it.

## 2. General rules

- **RF-1 Scope.** The policy applies to orders placed in the web shop and in the mobile app. Orders placed through marketplaces follow the marketplace rules.
- **RF-2 Cancellation window.** A customer can cancel an order until the carrier has scanned the parcel for the first time. After that the return process applies.
- **RF-6 Return window.** A customer can return an item within 30 days after delivery, provided the item is unused and in its original packaging.
- **RF-7 Order lookup.** Support staff identify an order by its order number and the name of the customer, and they see the payment method that was used.

## 3. Refunds

- **RF-3 Refund obligation.** A customer who cancels an order or returns an item within the allowed window is refunded the full price paid for it, including shipping when the whole order is cancelled.
- **RF-4 Refund method.** Refunds return to the original payment method. Store credit is issued only when the customer chooses it. This revision keeps every refund obligation intact.
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
