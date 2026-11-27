"""Spend estimates: the only code that estimates tokens or turns a price and a cap into a ceiling.

Pure.  The per-request estimate is the formula ``JevClient.ask`` uses to size a draw, so a whole-run reservation made from these
numbers covers exactly what the client will draw.
"""
import math

from jevlib.config import RESERVE_BYTES_PER_TOKEN
from jevlib.questions import canonical_bytes


def estimate_request_tokens(req):
    """Input tokens reserved for one request: ``ceil(len(canonical request bytes) / RESERVE_BYTES_PER_TOKEN)``."""
    return int(math.ceil(len(canonical_bytes(req)) / RESERVE_BYTES_PER_TOKEN))


def estimate_run_tokens(requests):
    """Worst case for a whole run: every request, times two for the one allowed rerun of a failed prompt."""
    return 2 * sum(estimate_request_tokens(r) for r in requests)


def ceiling_tokens(cap_usd, price_usd_per_mtok):
    """The token ceiling that keeps spend at or below ``cap_usd`` at the given price per million input tokens."""
    return int(cap_usd / price_usd_per_mtok * 1e6)


def worst_case_usd(tokens, price_usd_per_mtok):
    return tokens * price_usd_per_mtok / 1e6
