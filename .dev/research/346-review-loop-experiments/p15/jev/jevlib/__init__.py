"""jevlib: stdlib-only adapter for the TypeSafe System One (Jev) API, built for the p15 experiments.

Never call the live API from an implementer session; the coordinator runs live scripts (contract J2).
"""
from .config import MODEL, API_URL, KEY_ENV  # noqa: F401
