"""Constants of the Jev adapter (contract J1.1). The only place these numbers live."""
API_URL = "https://api.typesafe.ai/v1/systemone"
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
