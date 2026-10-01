"""Coder tier env change (2026-10): pools, window lines, vendor diversity.

The Coder workspace env now carries context windows next to each tier model
(``T2Model01_WINDOW``) and per tier (``T2_WINDOW``). Every reader builds exact
slot names, so these must never be taken as models; the pools themselves
change to the new tier contents.
"""

from __future__ import annotations

import pytest

from superclaude.cli.reflect._diversity import (
    _vendor_from_model_id,
    compute_vendor_diversity,
)
from superclaude.cli.reflect.runner import count_model_aliases
from superclaude.cli.swarm.config import SwarmConfig
from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.transports.openai_compat import read_env_for_pool

CODER_ENV = {
    "T2ProxyUrl": "https://gateway.invalid/cli/v1",
    "T2ProxyKey": "test-key",
    "T1ProxyUrl": "https://gateway.invalid/cli/v1",
    "T1ProxyKey": "test-key",
    "T1_WINDOW": "850000",
    "T1Model01": "claude-opus-5-5",
    "T1Model01_WINDOW": "1000000",
    "T1Model02": "gpt-6.1-sol",
    "T1Model02_WINDOW": "850000",
    "T1Model03": "claude-sonnet-5-5",
    "T1Model03_WINDOW": "1000000",
    "T2_WINDOW": "500000",
    "T2Model01": "muse-spark-1.3",
    "T2Model01_WINDOW": "950000",
    "T2Model02": "grok-4.7",
    "T2Model02_WINDOW": "500000",
    "T2Model03": "Qwen3.8-max",
    "T2Model03_WINDOW": "1000000",
    "T2Model04": "glm-5.3",
    "T2Model04_WINDOW": "1000000",
    "CCSESSION_DEFAULT_TIER": "tier2",
}
T2_POOL = ("muse-spark-1.3", "grok-4.7", "Qwen3.8-max", "glm-5.3")
T1_POOL = ("claude-opus-5-5", "gpt-6.1-sol", "claude-sonnet-5-5")


@pytest.mark.unit
def test_swarm_pools_ignore_window_lines() -> None:
    config = SwarmConfig.from_env(env=CODER_ENV)
    assert config.t2_models == T2_POOL
    assert config.t1_models == T1_POOL


@pytest.mark.unit
def test_transport_pools_ignore_window_lines() -> None:
    t2 = read_env_for_pool(
        model_prefix="T2Model0",
        max_slots=9,
        proxy_url_env="T2ProxyUrl",
        proxy_key_env="T2ProxyKey",
        env=CODER_ENV,
    )
    t1 = read_env_for_pool(
        model_prefix="T1Model0",
        max_slots=9,
        proxy_url_env="T1ProxyUrl",
        proxy_key_env="T1ProxyKey",
        env=CODER_ENV,
    )
    assert t2.models == T2_POOL
    # reflect's fallback ladder (T1Model01 -> T1Model02): Opus 5.5, then GPT 6.1 Sol.
    assert t1.models[:2] == ("claude-opus-5-5", "gpt-6.1-sol")


@pytest.mark.unit
@pytest.mark.parametrize(
    ("model_id", "vendor"),
    [
        ("muse-spark-1.3", "muse"),
        ("grok-4.7", "xai"),
        ("Qwen3.8-max", "qwen"),
        ("glm-5.3", "zhipu"),
        ("glm-5-turbo", "zhipu"),
        ("kimi-k3", "moonshot"),
        ("claude-opus-5-5", "anthropic"),
        ("gpt-6.1-sol", "openai"),
    ],
)
def test_tier_models_map_to_their_vendor(model_id: str, vendor: str) -> None:
    assert _vendor_from_model_id(model_id) == vendor


@pytest.mark.unit
def test_new_tier_mix_is_multi_vendor_and_glm_versions_are_one_vendor() -> None:
    def ok(model_id: str) -> WorkerResult:
        return WorkerResult(model_id=model_id, status="success")

    workers = [ok(m) for m in T2_POOL + T1_POOL[:2]]
    assert compute_vendor_diversity(workers) == "multi"
    assert compute_vendor_diversity([ok("glm-5.3"), ok("glm-5-turbo")]) == "single"


@pytest.mark.unit
def test_alias_count_survives_removal_of_the_anthropic_default_vars() -> None:
    """Coder #270 removes ANTHROPIC_DEFAULT_*; Claude Code's own aliases remain."""
    assert count_model_aliases({}) == 3
    assert count_model_aliases(CODER_ENV) == 3
    today = {
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "muse-spark-1.3[1m]",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-5-5",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "gpt-6-sol",
    }
    assert count_model_aliases(today) == 3
    same = dict.fromkeys(today, "claude-opus-5-5")
    assert count_model_aliases(same) == 1
