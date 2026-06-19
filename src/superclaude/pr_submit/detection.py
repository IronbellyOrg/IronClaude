"""Detection-contract loader + poll surface for the ``sc:pr-submit`` core.

Exposes :func:`poll_augment_review` (returns one of ``"polling"`` / ``"clean"`` /
``"findings"`` / ``"declined"``) and :class:`DetectionContract` (the probe-locked
constant from spec §7). The loader raises :class:`DetectionContractLocked` when ``locked`` is
``false`` or absent — the **T-210** arm gate ("probe first").

NFR-6 core purity: the real review fetch is performed by the bash poller
(``scripts/poll-augment-review.sh``); this module consumes an already-fetched
payload (or a test-injected one). It contains no review-fetch command tokens.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .classifier import classify

# Location of the SHIPPED detection-contract ref, relative to this package. This
# stays ``locked: false`` in source (generic + distributable; the T-210 test asserts
# it HALTs). The operator's REAL locked contract lives in a gitignored local override
# (below) that is opted into ONLY at arm time via ``prefer_local_override=True``.
_CONTRACT_PATH = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "sc-pr-submit-protocol"
    / "refs"
    / "detection-contract.md"
)

# Operator-local locked contract (gitignored). Populated by the R1 probe with the
# target repo's REAL Augment values; NEVER committed. The arm path prefers it when
# present. Resolved RELATIVE TO THE CWD (the repo root the operator runs sc:pr-submit
# from) — NOT a hardcoded absolute path — so the monitor works in any checkout. A
# module-level ``_LOCAL_OVERRIDE_PATH`` override wins when set (the monkeypatch seam).
_LOCAL_OVERRIDE_REL = Path(".dev/pr-monitor/detection-contract.locked.md")
_LOCAL_OVERRIDE_PATH: Path | None = None


def _local_override_path() -> Path:
    """Return the operator-local locked-contract path (indirection for testability).

    Honors a module-level ``_LOCAL_OVERRIDE_PATH`` when set (the test monkeypatch seam);
    otherwise resolves ``<cwd>/.dev/pr-monitor/detection-contract.locked.md`` fresh on
    each call, so the path tracks the repo the operator is actually working in.
    """
    if _LOCAL_OVERRIDE_PATH is not None:
        return Path(_LOCAL_OVERRIDE_PATH)
    return Path.cwd() / _LOCAL_OVERRIDE_REL


def _as_str_list(value, default: list[str]) -> list[str]:
    """Coerce a YAML field to a list of strings without char-splitting a scalar.

    ``list("auggie review")`` yields ``['a','u','g',...]`` — so a YAML field mistyped as
    a scalar string (``accepted_trigger_phrases: auggie review``) would silently shred a
    trigger phrase into characters. Treat a bare string as a one-element list; fall back
    to ``default`` when the value is falsy/absent.
    """
    if not value:
        return list(default)
    if isinstance(value, str):
        return [value]
    return list(value)


class DetectionContractLocked(RuntimeError):
    """Raised when the detection contract is not locked (``locked != true``).

    This is the **T-210** mechanical gate: the skill refuses to arm against an
    unlocked or absent contract and HALTs with a "probe first" instruction.
    """


@dataclass
class DetectionContract:
    """The probe-locked detection constant (spec §7).

    Construct directly (with ``locked=True`` and a synthetic ``augment_bot_login``)
    for pure classifier tests, or load the shipped ref via :meth:`load` (which
    enforces the lock gate).
    """

    augment_bot_login: str | None = None
    augment_author_association: list[str] = field(default_factory=list)
    augment_app_slug: str | None = None
    emission_shape: str | None = None
    findings_locus: str | None = None
    severity_field_path: str | None = None
    review_completeness_signal: str | None = None
    probe_evidence: str | None = None
    locked: bool = False
    # --- V1.1 decline-detection fields (addendum §6.2 / FR-9.1) ---
    # Baked defaults so an unprobed contract still classifies declines. Both
    # regexes must match (case-insensitively) an Augment-authored comment for it to
    # be a decline; ``accepted_trigger_phrases`` is the canonical operator re-trigger
    # token set (NOT the App's bait — see memory reference_augment_review_triggers).
    # NOTE (necessary deviation from spec §6.2 literal default): the retrigger char
    # class includes the backtick ``` ` ``` in addition to ``"``/``'`` because the
    # real Augment decline renders the trigger as ``Comment `augment review` `` with
    # markdown backticks; the spec's literal ``["']?`` would miss the most common
    # real shape (Phase 3 QA domain-accuracy finding F1).
    decline_phrase_regex: str = r"abnormally\s+large"
    decline_retrigger_regex: str = (
        "comment\\s+[\"'`*_]*(augment|auggie|augmentcode)\\s+review[\"'`*_]*"
    )
    accepted_trigger_phrases: list[str] = field(
        default_factory=lambda: [
            "auggie review",
            "augment review",
            "augmentcode review",
        ]
    )

    @classmethod
    def from_yaml(cls, data: dict) -> "DetectionContract":
        """Build a contract from a parsed YAML mapping (no lock enforcement)."""
        return cls(
            augment_bot_login=data.get("augment_bot_login"),
            augment_author_association=_as_str_list(
                data.get("augment_author_association"), []
            ),
            augment_app_slug=data.get("augment_app_slug"),
            emission_shape=data.get("emission_shape"),
            findings_locus=data.get("findings_locus"),
            severity_field_path=data.get("severity_field_path"),
            review_completeness_signal=data.get("review_completeness_signal"),
            probe_evidence=data.get("probe_evidence"),
            locked=bool(data.get("locked", False)),
            decline_phrase_regex=data.get(
                "decline_phrase_regex", r"abnormally\s+large"
            ),
            decline_retrigger_regex=data.get(
                "decline_retrigger_regex",
                "comment\\s+[\"'`*_]*(augment|auggie|augmentcode)\\s+review[\"'`*_]*",
            ),
            accepted_trigger_phrases=_as_str_list(
                data.get("accepted_trigger_phrases"),
                ["auggie review", "augment review", "augmentcode review"],
            ),
        )

    @classmethod
    def load(
        cls,
        path: str | Path | None = None,
        *,
        require_locked: bool = True,
        prefer_local_override: bool = False,
    ) -> "DetectionContract":
        """Load the contract from its markdown ref, extracting the fenced YAML block.

        Resolution order: an explicit ``path`` wins; else if ``prefer_local_override``
        and the gitignored operator-local locked contract exists, that is used (the
        ARM path); else the SHIPPED ref (``locked: false`` in source). Raises
        :class:`DetectionContractLocked` when ``require_locked`` and the resolved
        contract is not ``locked: true`` (the T-210 arm gate). The default
        ``prefer_local_override=False`` keeps the shipped-source behavior deterministic
        for the T-210 regression test regardless of any operator-local override.
        """
        if path is not None:
            ref = Path(path)
        elif prefer_local_override and _local_override_path().exists():
            ref = _local_override_path()
        else:
            ref = _CONTRACT_PATH
        if not ref.exists():
            raise DetectionContractLocked(
                f"detection contract absent at {ref} — run the R1 probe first (T-210)"
            )
        text = ref.read_text(encoding="utf-8")
        block = _extract_yaml_block(text)
        data = yaml.safe_load(block) if block else None
        if not isinstance(data, dict):
            raise DetectionContractLocked(
                f"detection contract at {ref} has no parseable YAML — run the R1 probe first (T-210)"
            )
        contract = cls.from_yaml(data)
        if require_locked and not contract.locked:
            raise DetectionContractLocked(
                "detection contract is locked:false (or absent) — run the R1 probe "
                "first and flip locked:true before arming (T-210)"
            )
        return contract

    @classmethod
    def for_arming(cls) -> "DetectionContract":
        """Load the contract for ARMING — prefers the operator-local locked override.

        This is the surface the SKILL's arm step uses (T-210 gate): it returns the
        gitignored local locked contract when present, else HALTs on the shipped
        ``locked: false`` source. Equivalent to
        ``load(prefer_local_override=True)``.
        """
        return cls.load(prefer_local_override=True)


def _extract_yaml_block(markdown_text: str) -> str | None:
    """Return the first fenced ```yaml block body from a markdown ref, or None."""
    match = re.search(r"```ya?ml\s*\n(.*?)\n```", markdown_text, re.DOTALL)
    return match.group(1) if match else None


# --- poll seam (NFR-6) -----------------------------------------------------
# The real fetch lives in the bash poller. In-process callers inject a payload;
# tests monkeypatch ``_fetch_payload`` via the ``mock_gh`` fixture. With no
# review data available, the observed state is "polling".


def _fetch_payload(pr_num: int) -> dict:
    """Default no-data fetcher — overridden by tests/mocks. Yields no reviews."""
    return {"reviews": [], "comments": []}


def poll_augment_review(
    pr_num: int,
    payload: dict | None = None,
    contract: DetectionContract | None = None,
) -> str:
    """Classify the current review state for ``pr_num``.

    Returns ``"polling"`` (no Augment review yet), ``"clean"`` (Augment reviewed,
    no findings), ``"findings"`` (Augment reviewed with findings), or ``"declined"``
    (Augment posted an "abnormally large" decline; FR-9.1). When no
    ``payload`` is supplied, the seam :func:`_fetch_payload` provides it (tests
    inject fixtures via ``mock_gh``). Classification is delegated to the pure
    :func:`~superclaude.pr_submit.classifier.classify` against the contract.

    This is a classification CONVENIENCE over an injected payload/contract — it is
    NOT the arm gate. Arming proper is gated by :meth:`DetectionContract.load`
    (T-210), which HALTs on ``locked:false``. When no ``contract`` is supplied here,
    a neutral UNLOCKED placeholder (no bot login) is used, so classification is the
    fail-safe ``"polling"`` / "review not detected" state (NFR-4) — no login is
    guessed and nothing is auto-locked.
    """
    if payload is None:
        payload = _fetch_payload(pr_num)
    if contract is None:
        # No contract supplied: use a neutral UNLOCKED placeholder (no bot login)
        # so classification is the fail-safe "polling" / "review not detected"
        # state (NFR-4) — augment_bot_login=None makes the classifier match no
        # entries for ANY payload. No login is guessed and nothing is auto-locked.
        # Arming proper is gated by DetectionContract.load() (T-210), which HALTs
        # on locked:false.
        contract = DetectionContract()
    return classify(payload, contract)
