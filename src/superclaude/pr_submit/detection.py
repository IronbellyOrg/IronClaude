"""Detection-contract loader + poll surface for the ``sc:pr-submit`` core.

Exposes :func:`poll_augment_review` (returns one of ``"polling"`` / ``"clean"`` /
``"findings"`` / ``"declined"``) and :class:`DetectionContract` (the probe-locked
constant from spec §7). The loader raises :class:`DetectionContractLocked` when the resolved file is
absent or unparseable — not because ``locked`` is false.

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

# Location of the SHIPPED detection-contract ref, relative to this package.
# Ships with baked Augment identity so any project can arm without a probe.
# An optional gitignored local override (below) is preferred at arm time when
# present.
_CONTRACT_PATH = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "sc-pr-submit-protocol"
    / "refs"
    / "detection-contract.md"
)

# Optional operator-local contract (gitignored). Preferred at arm time when
# present; NEVER required. Resolved RELATIVE TO THE CWD (the repo root the
# operator runs sc:pr-submit from). A module-level ``_LOCAL_OVERRIDE_PATH``
# override wins when set (the monkeypatch seam).
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


def _has_identity(contract: "DetectionContract") -> bool:
    """True when the contract has a non-placeholder bot login or app slug."""
    for value in (contract.augment_bot_login, contract.augment_app_slug):
        stripped = str(value).strip() if value is not None else ""
        if stripped and not stripped.startswith("<"):
            return True
    return False


class DetectionContractLocked(RuntimeError):
    """Raised when the detection contract file is absent or unparseable.

    The ``locked`` YAML flag is not an arming gate.
    """


@dataclass
class DetectionContract:
    """Detection config for the Augment classifier (spec §7).

    Construct directly (synthetic ``augment_bot_login``) for pure classifier
    tests, or load the shipped ref via :meth:`load` / :meth:`for_arming`.
    Direct construction leaves identity empty so :func:`poll_augment_review`
    stays fail-safe when no contract is supplied.
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
        prefer_local_override: bool = False,
    ) -> "DetectionContract":
        """Load the contract from its markdown ref, extracting the fenced YAML block.

        Resolution order: an explicit ``path`` wins; else if ``prefer_local_override``
        and the gitignored operator-local override exists AND carries a usable
        identity, that is used; else the SHIPPED ref (baked Augment identity).
        An override with placeholder/empty identity falls through to shipped.
        Raises :class:`DetectionContractLocked` when the resolved file is absent
        or unparseable. The ``locked`` flag is not checked.
        """
        if path is not None:
            return cls._read(Path(path))
        if prefer_local_override and _local_override_path().exists():
            try:
                override = cls._read(_local_override_path())
            except DetectionContractLocked:
                override = None
            if override is not None and _has_identity(override):
                return override
        return cls._read(_CONTRACT_PATH)

    @classmethod
    def _read(cls, ref: Path) -> "DetectionContract":
        if not ref.exists():
            raise DetectionContractLocked(f"detection contract absent at {ref}")
        text = ref.read_text(encoding="utf-8")
        block = _extract_yaml_block(text)
        try:
            data = yaml.safe_load(block) if block else None
        except yaml.YAMLError as exc:
            raise DetectionContractLocked(
                f"detection contract at {ref} has malformed YAML: {exc}"
            ) from exc
        if not isinstance(data, dict):
            raise DetectionContractLocked(
                f"detection contract at {ref} has no parseable YAML"
            )
        return cls.from_yaml(data)

    @classmethod
    def for_arming(cls) -> "DetectionContract":
        """Load the contract for ARMING — prefers an optional local override.

        Returns the gitignored local override when it has a usable identity,
        else the shipped baked-identity contract. A missing, unparseable, or
        placeholder override is not a halt.
        Equivalent to ``load(prefer_local_override=True)``.
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
    NOT the arm path. When no ``contract`` is supplied here, a neutral placeholder
    (no bot login) is used, so classification is the fail-safe ``"polling"`` /
    "review not detected" state (NFR-4). Arming uses :meth:`DetectionContract.for_arming`.
    """
    if payload is None:
        payload = _fetch_payload(pr_num)
    if contract is None:
        # No contract supplied: empty identity so classification is fail-safe
        # "polling" / "review not detected" (NFR-4). Arming uses for_arming().
        contract = DetectionContract()
    return classify(payload, contract)
