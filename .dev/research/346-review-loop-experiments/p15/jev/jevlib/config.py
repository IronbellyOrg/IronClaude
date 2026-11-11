"""Constants of the Jev adapter (contract J1.1). The only place these numbers live."""
import ipaddress
import os
from urllib.parse import urlsplit

API_URL = "https://api.typesafe.ai/v1/systemone"   # the vendor endpoint; the default
URL_ENV = "JEV_API_URL"         # optional override: the LiteLLM gateway route (see docs/docs-product/ops/jev-litellm-gateway-operational-guide.md)
MODEL = "jev-1.14.0"            # verified on the live models page 2026-11-10 (current; jev-1.13.0 also listed); aliases are never sent
KEY_ENV = "JEV_API_KEY"         # owner rule; the vendor's own key variable name is NOT used
PRICE_USD_PER_MTOK_INPUT = 0.042  # live models page 2026-11-10; output tokens free
LIMIT_REQUEST_TOKENS = 64_000   # per request (state + all questions)
LIMIT_QUESTION_TOKENS = 32_000  # state + any one question
SIZE_BYTES_PER_TOKEN = 3.0      # estimate for the local oversize refusal
RESERVE_BYTES_PER_TOKEN = 2.0   # conservative estimate for budget reservations (settled to usage afterwards)
ATTEMPT_TIMEOUT_S = 20.0
LOGICAL_DEADLINE_S = 45.0       # whole logical call incl. the retry; a liveness rule, not a cost rule
MAX_RETRIES = 1                 # at most one retry per logical call
BACKOFF_S = 2.0                 # wait before the retry; Retry-After honoured up to RETRY_AFTER_CAP_S
RETRY_AFTER_CAP_S = 20.0
PROB_SUM_TOL = 0.02             # |sum(choice probabilities) - 1| <= tol
ALLOWED_DATA_CLASSES = {"synthetic", "public", "s1_spec", "stage2_artifact"}
QNAME_RE = r"^[a-z][a-z0-9_]{0,63}$"


def _private_or_loopback(host) -> bool:
    """True only for an IP literal that is loopback or in a private range (never for a hostname)."""
    try:
        ip = ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        return False
    return ip.is_loopback or ip.is_private


def api_url(environ=None) -> str:
    """The endpoint to call: $JEV_API_URL when set, else the vendor URL.

    An override must be https, or http only when the host is a loopback or private-range IP literal (the internal
    gateway is plain http on a private address; a public host or a name must use https), carry no user info, query
    or fragment (a key or token in a URL ends up in logs), and have a host.  Anything else raises ValueError, never
    falls back: a typo must not silently send packets to the vendor or to an unintended host.
    The model id is NOT affected: the client still sends MODEL and still rejects a response with another model."""
    env = os.environ if environ is None else environ
    raw = env.get(URL_ENV)
    if raw is None or raw == "":
        return API_URL
    u = urlsplit(raw)
    if u.scheme != "https" and not (u.scheme == "http" and u.hostname and _private_or_loopback(u.hostname)):
        raise ValueError(f"{URL_ENV} must be an https URL (http only for a loopback or private-range IP address)")
    if not u.hostname:
        raise ValueError(f"{URL_ENV} has no host")
    if u.username is not None or u.password is not None or u.query or u.fragment:
        raise ValueError(f"{URL_ENV} must not contain user info, a query or a fragment")
    return raw
