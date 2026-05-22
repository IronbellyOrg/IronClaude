"""Contrived test snippet for sc:troubleshoot eval.

Triggers NameError at line 47: `datetime.utcnow()` is called but `datetime`
is never imported. Imports cover only typing.Optional, decimal.Decimal,
StripeGateway, Refund, RefundStatus.
"""
from typing import Optional
from decimal import Decimal

from payments.gateway import StripeGateway
from payments.models import Refund, RefundStatus


class RefundHandler:
    """Processes refund requests through the configured gateway."""

    def __init__(self, gateway: StripeGateway) -> None:
        self.gateway = gateway

    def process(
        self,
        charge_id: str,
        amount: Decimal,
        reason: Optional[str] = None,
    ) -> Refund:
        """Issue a refund and persist the resulting record.

        Args:
            charge_id: The Stripe charge identifier.
            amount: Refund amount as a Decimal.
            reason: Optional human-readable reason string.

        Returns:
            A persisted Refund record.
        """
        if amount <= Decimal("0"):
            raise ValueError("Refund amount must be positive")

        gateway_response = self.gateway.create_refund(
            charge_id=charge_id,
            amount=amount,
            reason=reason,
        )

        refund = Refund.from_gateway(gateway_response)
        refund.status = RefundStatus.SUCCEEDED
        refund.processed_at = datetime.utcnow()
        refund.save()

        return refund
