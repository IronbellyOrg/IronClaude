"""T03.21 -- T2 proxy env contract reader (R-085 / AC-017).

Pins the public surface of
:func:`superclaude.cli.swarm.transports.openai_compat.read_env` so the
INV-007 empty-pool failure path (T02.11) has a single, structured
diagnostic to consume at Wave 0.

The companion suite in ``test_openai_compat.py`` already exercises the
happy/error matrix at the *transport* layer; this file is the
contract-focused twin called out by the phase-3 tasklist
(``test_t2_env_contract.py``). It re-asserts the same guarantees with a
contract-narrow framing so a reader landing here from the roadmap can
see the AC-017 surface without scrolling through the wider HTTP-outcome
tests:

* All three env-var families (``T2ProxyUrl`` / ``T2ProxyKey`` /
  ``T2Model0N``) are enumerated by :func:`read_env`.
* A populated env yields a :class:`TransportConfig` with a dense,
  slot-ordered ``models`` tuple.
* Whitespace-only values are treated as absent.
* Missing values raise :class:`TransportEnvError` with the missing
  variable names in :attr:`TransportEnvError.missing` so dispatch can
  surface them verbatim.
* The slot probe is bounded by
  :data:`superclaude.cli.swarm.config.T2_MODEL_MAX_SLOTS`.
"""

from __future__ import annotations

import pytest

from superclaude.cli.swarm.config import (
    T2_MODEL_ENV_PREFIX,
    T2_MODEL_MAX_SLOTS,
    T2_PROXY_KEY_ENV,
    T2_PROXY_URL_ENV,
)
from superclaude.cli.swarm.transports.openai_compat import (
    TransportConfig,
    TransportEnvError,
    read_env,
)


# ---------------------------------------------------------------------------
# Constants -- sanity-check the env-var spelling against the contract.
# ---------------------------------------------------------------------------


def test_env_var_names_match_spec() -> None:
    """AC-017 -- env-var names are exactly ``T2ProxyUrl`` / ``T2ProxyKey`` /
    ``T2Model0N``.

    A typo here (e.g. ``T2_PROXY_URL`` snake-case drift) silently breaks
    the proxy contract because dispatch reads ``os.environ`` by name.
    Pinning the strings keeps the spec and the code in sync.
    """
    assert T2_PROXY_URL_ENV == "T2ProxyUrl"
    assert T2_PROXY_KEY_ENV == "T2ProxyKey"
    assert T2_MODEL_ENV_PREFIX == "T2Model0"
    assert T2_MODEL_MAX_SLOTS == 9


# ---------------------------------------------------------------------------
# Happy path -- populated env yields a structured TransportConfig.
# ---------------------------------------------------------------------------


def test_read_env_returns_transport_config() -> None:
    env = {
        "T2ProxyUrl": "https://proxy.example/v1",
        "T2ProxyKey": "k-xyz",
        "T2Model01": "m-alpha",
    }
    config = read_env(env)
    assert isinstance(config, TransportConfig)
    assert config.base_url == "https://proxy.example/v1"
    assert config.api_key == "k-xyz"
    assert config.models == ("m-alpha",)


def test_read_env_models_dense_and_ordered_by_slot() -> None:
    """Empty slots are skipped; surviving slots stay in slot-index order."""
    env = {
        "T2ProxyUrl": "u",
        "T2ProxyKey": "k",
        "T2Model01": "m1",
        "T2Model02": "",  # empty -- skipped
        "T2Model03": "m3",
        "T2Model05": "m5",  # leaves slot 4 empty
    }
    config = read_env(env)
    assert config.models == ("m1", "m3", "m5")


def test_read_env_collects_up_to_max_slots() -> None:
    """All slots 1..T2_MODEL_MAX_SLOTS are probed."""
    env = {
        "T2ProxyUrl": "u",
        "T2ProxyKey": "k",
    }
    for index in range(1, T2_MODEL_MAX_SLOTS + 1):
        env[f"{T2_MODEL_ENV_PREFIX}{index}"] = f"m{index}"

    config = read_env(env)
    assert len(config.models) == T2_MODEL_MAX_SLOTS
    assert config.models[0] == "m1"
    assert config.models[-1] == f"m{T2_MODEL_MAX_SLOTS}"


def test_read_env_strips_whitespace() -> None:
    env = {
        "T2ProxyUrl": "  https://proxy.example/v1  ",
        "T2ProxyKey": "\tk\n",
        "T2Model01": "  m  ",
    }
    config = read_env(env)
    assert config.base_url == "https://proxy.example/v1"
    assert config.api_key == "k"
    assert config.models == ("m",)


def test_read_env_whitespace_only_treated_as_missing() -> None:
    env = {
        "T2ProxyUrl": "   ",
        "T2ProxyKey": "   ",
        "T2Model01": "   ",
    }
    with pytest.raises(TransportEnvError) as exc:
        read_env(env)
    assert T2_PROXY_URL_ENV in exc.value.missing
    assert T2_PROXY_KEY_ENV in exc.value.missing
    assert any("T2Model0" in name for name in exc.value.missing)


def test_read_env_immutable_transport_config() -> None:
    """``TransportConfig`` is frozen so Wave-0 resolution cannot drift."""
    config = read_env(
        {
            "T2ProxyUrl": "u",
            "T2ProxyKey": "k",
            "T2Model01": "m",
        }
    )
    with pytest.raises(Exception):  # FrozenInstanceError on dataclasses
        config.base_url = "tampered"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Failure path -- missing vars surface a structured diagnostic.
# ---------------------------------------------------------------------------


def test_read_env_missing_url() -> None:
    env = {"T2ProxyKey": "k", "T2Model01": "m"}
    with pytest.raises(TransportEnvError) as exc:
        read_env(env)
    assert exc.value.missing == (T2_PROXY_URL_ENV,)
    assert "T2ProxyUrl" in str(exc.value)


def test_read_env_missing_key() -> None:
    env = {"T2ProxyUrl": "u", "T2Model01": "m"}
    with pytest.raises(TransportEnvError) as exc:
        read_env(env)
    assert exc.value.missing == (T2_PROXY_KEY_ENV,)
    assert "T2ProxyKey" in str(exc.value)


def test_read_env_missing_all_models() -> None:
    env = {"T2ProxyUrl": "u", "T2ProxyKey": "k"}
    with pytest.raises(TransportEnvError) as exc:
        read_env(env)
    assert len(exc.value.missing) == 1
    assert "T2Model0" in exc.value.missing[0]


def test_read_env_missing_everything() -> None:
    with pytest.raises(TransportEnvError) as exc:
        read_env({})
    assert T2_PROXY_URL_ENV in exc.value.missing
    assert T2_PROXY_KEY_ENV in exc.value.missing
    assert any("T2Model0" in name for name in exc.value.missing)


def test_transport_env_error_message_lists_missing_names() -> None:
    """The error message names every missing var so operators can fix in
    one pass instead of trial-and-error."""
    with pytest.raises(TransportEnvError) as exc:
        read_env({"T2ProxyUrl": "u"})
    message = str(exc.value)
    assert "T2ProxyKey" in message
    assert "T2Model0" in message


# ---------------------------------------------------------------------------
# Default-arg behaviour -- ``read_env()`` reads ``os.environ`` when no env
# mapping is passed. We exercise this via ``monkeypatch`` rather than
# leaking state.
# ---------------------------------------------------------------------------


def test_read_env_default_reads_os_environ(monkeypatch: pytest.MonkeyPatch) -> None:
    # Clear any inherited T2 vars so the test is deterministic regardless
    # of operator environment.
    for index in range(1, T2_MODEL_MAX_SLOTS + 1):
        monkeypatch.delenv(f"{T2_MODEL_ENV_PREFIX}{index}", raising=False)
    monkeypatch.delenv(T2_PROXY_URL_ENV, raising=False)
    monkeypatch.delenv(T2_PROXY_KEY_ENV, raising=False)

    monkeypatch.setenv(T2_PROXY_URL_ENV, "https://proxy.example/v1")
    monkeypatch.setenv(T2_PROXY_KEY_ENV, "k")
    monkeypatch.setenv(f"{T2_MODEL_ENV_PREFIX}1", "m-default")

    config = read_env()
    assert config.base_url == "https://proxy.example/v1"
    assert config.api_key == "k"
    assert config.models == ("m-default",)
