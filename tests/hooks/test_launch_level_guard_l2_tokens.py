"""L1 guard tokens that protect the L2 pre-push hook (#441, FR-050..055, FR-104).

The #440-owned ``test_launch_level_guard.py`` is read only (NFR-009), so the
tamper tokens added for L2 are pinned here, reusing its helpers.
"""

from __future__ import annotations

import filecmp

import pytest

from tests.hooks import test_launch_level_pre_push as l2
from tests.hooks.test_launch_level_guard import (
    DESIGN,
    HOOK,
    LEVEL_FILES,
    LEVEL_ORDER,
    ROOT,
    _assert_decision,
    _bash,
    _bind,
    _edit,
    _run,
)

TAMPER = ("LL-TAMPER",) * 4
UNKNOWN = ("LL-UNKNOWN",) * 4
PUSH = ("LL-PUSH", "LL-PUSH", "LL-PUSH", "LL-PUSH-FORM")
PROTECTED = ("LL-PROTECTED",) * 4
ALLOWED = (None,) * 4


def _check(tmp_path, payload, level, msg_id, text):
    _bind(tmp_path, *LEVEL_FILES[level])
    result = _run(payload, tmp_path)
    _assert_decision(result, tmp_path, msg_id, level, text=text and msg_id is not None)


HOOK_FILES = ["/repo/.git/hooks/pre-push", "/repo/.git/hooks/pre-push.launch-level"]


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize("tool", ["Edit", "Write"])
@pytest.mark.parametrize("path", HOOK_FILES)
def test_hook_file_edit_is_tamper(tmp_path, path, tool, level):
    _check(tmp_path, _edit(tool, path), level, "LL-TAMPER", text=False)


# FR-050..052: hook files, hook-skipping flags and hook-moving config keys.
TAMPER_BASH = [
    "rm .git/hooks/pre-push",
    "chmod -x .git/hooks/pre-push",
    "rm .git/hooks/pre-push.launch-level",
    "git push --no-verify origin x",
    "git -c core.hooksPath=/dev/null push origin x",
    "git -c Core.HooksPath=/dev/null push origin x",
    "git --config-env=core.hooksPath=V push origin x",
    "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=/dev/null git push origin x",
    "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=hook.pre-push.command GIT_CONFIG_VALUE_0=true git push origin x",
    "git -c hook.pre-push.enabled=false push origin x",
    "git config core.hooksPath x",
    # --no-verify outside a push is still denied (FR-051).
    "git pull --no-verify origin x",
    # Accepted over-blocks (LIM-16): neither skips the pre-push hook.
    "git commit --no-verify -m m",
    "ls .git/hooks",
]


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize("command", TAMPER_BASH)
def test_tamper_bash(tmp_path, command, level):
    _check(tmp_path, _bash(command), level, "LL-TAMPER", text=True)


# Config transports that do not name a hook key keep their old ids (SD-2, FR-052).
TRANSPORT_ONLY = [
    ("X=commit git --config-env=alias.ci=X ci", UNKNOWN),
    ("GIT_CONFIG_COUNT=1 git push origin f", PUSH),
    ("git send-pack origin x", UNKNOWN),
    # include.path reaches the hook only indirectly: denied by L1, not TAMPER.
    ("git --config-env=include.path=V push origin x", UNKNOWN),
    (
        "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=include.path"
        " GIT_CONFIG_VALUE_0=/tmp/c git push origin x",
        UNKNOWN,
    ),
]


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize("command, ids", TRANSPORT_ONLY)
def test_transport_only_forms_keep_their_ids(tmp_path, command, ids, level):
    _check(tmp_path, _bash(command), level, ids[LEVEL_ORDER.index(level)], text=True)


# FR-104 combined L1+L2 table: the L1 decision at each level, and what L2 does
# with the same push by a governed actor (proven in test_launch_level_pre_push,
# whose pushes all run from a script L1 never sees).
REFUSED = "refused: test_t01_create_protected_ref"
COMBINED = [
    ("bash ./push.sh", ALLOWED, REFUSED),
    ("./push.sh", ALLOWED, REFUSED),
    ("make release", ALLOWED, REFUSED),
    ("git push origin main", PROTECTED, REFUSED),
    ("git push --no-verify origin main", TAMPER, "leak: LIM-4 --no-verify"),
    (
        "git -c core.hooksPath=/dev/null push origin main",
        TAMPER,
        "leak: LIM-4 -c core.hooksPath",
    ),
    (
        "env HP=/dev/null git --config-env=core.hooksPath=HP push origin main",
        TAMPER,
        "leak: LIM-4 --config-env",
    ),
    (
        "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=/dev/null git push origin main",
        TAMPER,
        "leak: LIM-4 GIT_CONFIG_COUNT",
    ),
    (
        "git send-pack origin refs/heads/feature:refs/heads/main",
        UNKNOWN,
        "leak: LIM-7 git send-pack",
    ),
]


@pytest.mark.parametrize("level", LEVEL_ORDER)
@pytest.mark.parametrize("command, ids, _l2", COMBINED)
def test_combined_l1_decision(tmp_path, command, ids, _l2, level):
    _check(tmp_path, _bash(command), level, ids[LEVEL_ORDER.index(level)], text=True)


@pytest.mark.parametrize("command, ids, outcome", COMBINED)
def test_combined_l2_outcome_is_pinned(command, ids, outcome):
    kind, ref = outcome.split(": ", 1)
    if kind == "leak":
        assert ref in l2.LEAKS, ref
    else:
        assert callable(getattr(l2, ref, None)), ref
    # A hidden push L1 lets through must be one L2 refuses.
    if ids == ALLOWED:
        assert kind == "refused", command


def test_guard_and_plugin_mirror_are_byte_identical():
    mirror = ROOT / "plugins/superclaude/hooks/scripts/launch-level-guard.sh"
    assert filecmp.cmp(HOOK, mirror, shallow=False)


def test_tamper_message_names_the_pre_push_hook():
    row = next(
        line
        for line in DESIGN.read_text().splitlines()
        if line.startswith("| LL-TAMPER |")
    )
    assert "the git pre-push hook" in row
