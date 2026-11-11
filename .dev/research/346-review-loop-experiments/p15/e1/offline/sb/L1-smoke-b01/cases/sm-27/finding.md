### R1-1 Refund method forces store credit
The refund method rule says that every refund is paid out as store credit. That conflicts with the purpose of the policy, which is to give customers their money back. Cited: spec lines 33-34 (before version).
An implementer who follows RF-4 builds a refund service that never returns money to the payment method of the customer.
Protected requirement: line 33 (the refund obligation must hold).
