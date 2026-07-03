"""Tests for sprint monitor — signal extraction from output files."""

import time
from pathlib import Path

import pytest

from superclaude.cli.sprint.monitor import (
    FILES_CHANGED_PATTERN,
    TASK_ID_PATTERN,
    TOOL_PATTERN,
    OutputMonitor,
    ProviderFailure,
    ProviderFailureSignal,
    _provider_failure_from_text,
    count_turns_from_output,
    detect_error_max_turns,
    detect_provider_failure,
)

_FIXTURES = Path(__file__).resolve().parent / "fixtures" / "exhaustion"


class TestPatterns:
    """Test regex patterns for signal extraction."""

    def test_task_id_pattern(self):
        text = "Working on T02.05 now"
        matches = TASK_ID_PATTERN.findall(text)
        assert "T02.05" in matches

    def test_task_id_multiple(self):
        text = "T01.01 done, starting T01.02"
        matches = TASK_ID_PATTERN.findall(text)
        assert matches == ["T01.01", "T01.02"]

    def test_tool_pattern(self):
        text = "Using Read tool to examine file"
        matches = TOOL_PATTERN.findall(text)
        assert "Read" in matches

    def test_tool_pattern_multiple(self):
        text = "Read the file, then Edit it, then Bash to test"
        matches = TOOL_PATTERN.findall(text)
        assert "Read" in matches
        assert "Edit" in matches
        assert "Bash" in matches

    def test_files_changed_pattern(self):
        text = "modified `src/main.py`"
        matches = FILES_CHANGED_PATTERN.findall(text)
        assert "src/main.py" in matches

    def test_files_changed_multiple_verbs(self):
        text = "created foo.py, edited bar.ts, wrote config.json"
        matches = FILES_CHANGED_PATTERN.findall(text)
        assert "foo.py" in matches
        assert "bar.ts" in matches
        assert "config.json" in matches


class TestOutputMonitor:
    """Test the background output monitor."""

    def test_initial_state(self, tmp_path):
        output_file = tmp_path / "output.txt"
        monitor = OutputMonitor(output_file)
        assert monitor.state.output_bytes == 0
        assert monitor.state.last_task_id == ""

    def test_detects_new_content(self, tmp_path):
        output_file = tmp_path / "output.txt"
        output_file.write_text("Working on T01.01\n")

        monitor = OutputMonitor(output_file, poll_interval=0.1)
        monitor.start()
        time.sleep(0.3)  # Give monitor time to poll
        monitor.stop()

        assert monitor.state.output_bytes > 0
        assert monitor.state.last_task_id == "T01.01"

    def test_detects_tool_usage(self, tmp_path):
        output_file = tmp_path / "output.txt"
        output_file.write_text("Using Edit tool\n")

        monitor = OutputMonitor(output_file, poll_interval=0.1)
        monitor.start()
        time.sleep(0.3)
        monitor.stop()

        assert monitor.state.last_tool_used == "Edit"

    def test_stop_terminates_thread(self, tmp_path):
        output_file = tmp_path / "output.txt"
        output_file.write_text("")

        monitor = OutputMonitor(output_file, poll_interval=0.1)
        monitor.start()
        monitor.stop()
        assert not monitor._thread.is_alive()

    def test_reset_clears_state(self, tmp_path):
        output_file = tmp_path / "output.txt"
        output_file.write_text("T01.01 Read\n")

        monitor = OutputMonitor(output_file, poll_interval=0.1)
        monitor.start()
        time.sleep(0.3)
        monitor.stop()

        # Reset
        new_output = tmp_path / "output2.txt"
        monitor.reset(new_output)
        assert monitor.state.output_bytes == 0
        assert monitor.state.last_task_id == ""

    def test_handles_missing_file(self, tmp_path):
        output_file = tmp_path / "nonexistent.txt"
        monitor = OutputMonitor(output_file, poll_interval=0.1)
        monitor.start()
        time.sleep(0.3)
        monitor.stop()
        # Should not crash, just return 0 bytes
        assert monitor.state.output_bytes == 0

    def test_incremental_read(self, tmp_path):
        output_file = tmp_path / "output.txt"
        output_file.write_text("Line 1\n")

        monitor = OutputMonitor(output_file, poll_interval=0.1)
        monitor.start()
        time.sleep(0.3)

        # Append more data
        with open(output_file, "a") as f:
            f.write("T02.03 using Grep\n")

        time.sleep(0.3)
        monitor.stop()

        assert monitor.state.last_task_id == "T02.03"
        assert monitor.state.last_tool_used == "Grep"


class TestDetectErrorMaxTurns:
    """Tests for error_max_turns NDJSON detection."""

    def test_detects_error_max_turns_last_line(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text(
            '{"type":"result","subtype":"success"}\n'
            '{"type":"result","subtype":"error_max_turns"}\n'
        )
        assert detect_error_max_turns(output) is True

    def test_no_false_positive_on_success(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text('{"type":"result","subtype":"success"}\n')
        assert detect_error_max_turns(output) is False

    def test_no_false_positive_on_other_error(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text('{"type":"result","subtype":"error_timeout"}\n')
        assert detect_error_max_turns(output) is False

    def test_empty_output(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text("")
        assert detect_error_max_turns(output) is False

    def test_missing_file(self, tmp_path):
        output = tmp_path / "nonexistent.txt"
        assert detect_error_max_turns(output) is False

    def test_truncated_ndjson(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text('{"type":"result","sub')
        assert detect_error_max_turns(output) is False

    def test_multiple_lines_only_checks_last(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text(
            '{"type":"result","subtype":"error_max_turns"}\n'
            '{"type":"result","subtype":"success"}\n'
        )
        assert detect_error_max_turns(output) is False

    def test_trailing_whitespace(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text('{"type":"result","subtype":"error_max_turns"}\n\n\n')
        assert detect_error_max_turns(output) is True


class TestCountTurnsFromOutput:
    """Tests for turn counting from NDJSON subprocess output."""

    def test_counts_assistant_turns(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text(
            '{"type":"assistant","text":"Hello"}\n'
            '{"type":"tool_use","name":"Read"}\n'
            '{"type":"tool_result","content":"file content"}\n'
            '{"type":"assistant","text":"I see the file"}\n'
            '{"type":"result","subtype":"success"}\n'
        )
        assert count_turns_from_output(output) == 2

    def test_zero_turns_on_empty(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text("")
        assert count_turns_from_output(output) == 0

    def test_zero_turns_missing_file(self, tmp_path):
        output = tmp_path / "nonexistent.txt"
        assert count_turns_from_output(output) == 0

    def test_no_assistant_messages(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text(
            '{"type":"tool_use","name":"Read"}\n'
            '{"type":"tool_result","content":"data"}\n'
        )
        assert count_turns_from_output(output) == 0

    def test_many_turns(self, tmp_path):
        output = tmp_path / "output.txt"
        lines = [f'{{"type":"assistant","text":"turn {i}"}}\n' for i in range(10)]
        output.write_text("".join(lines))
        assert count_turns_from_output(output) == 10

    def test_handles_malformed_json_lines(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text(
            '{"type":"assistant","text":"Hello"}\n'
            "not valid json\n"
            '{"type":"assistant","text":"World"}\n'
        )
        # Should still count the valid assistant lines
        assert count_turns_from_output(output) == 2


class TestDetectProviderFailure:
    """Tests for provider/account-exhaustion detection (P1, spec §2/§4).

    Covers the four-way discrimination over the six exhaustion fixtures plus the
    OSError/parse-tolerance edges, the subtype-trap, the conservative default,
    and the shared-core equivalence between the text core and the path wrapper.
    """

    # --- fixture-driven four-way discrimination ----------------------------

    @pytest.mark.unit
    def test_single_account_429(self):
        sig = detect_provider_failure(_FIXTURES / "single_account_429.jsonl")
        assert sig.kind is ProviderFailure.SINGLE_ACCOUNT_LIMIT

    @pytest.mark.unit
    def test_all_account_cooldown_captures_model(self):
        sig = detect_provider_failure(_FIXTURES / "all_account_cooldown.jsonl")
        assert sig.kind is ProviderFailure.ALL_ACCOUNT_COOLDOWN
        assert sig.resolved_model == "claude-opus-4-8"

    @pytest.mark.unit
    def test_operation_timeout(self):
        sig = detect_provider_failure(_FIXTURES / "operation_timeout.jsonl")
        assert sig.kind is ProviderFailure.OPERATION_TIMEOUT

    @pytest.mark.unit
    def test_task_failure_real_is_none(self):
        sig = detect_provider_failure(_FIXTURES / "task_failure_real.jsonl")
        assert sig.kind is ProviderFailure.NONE

    @pytest.mark.unit
    def test_clean_pass_is_none(self):
        sig = detect_provider_failure(_FIXTURES / "clean_pass.jsonl")
        assert sig.kind is ProviderFailure.NONE

    @pytest.mark.unit
    def test_api_retry_maxed_still_single_account(self):
        # attempt==max_retries==10 is only corroborating; the LAST result event
        # is the load-bearing classification (edge case #6).
        sig = detect_provider_failure(_FIXTURES / "api_retry_maxed.jsonl")
        assert sig.kind is ProviderFailure.SINGLE_ACCOUNT_LIMIT

    # --- OSError / parse tolerance edges -----------------------------------

    @pytest.mark.unit
    def test_truncated_ndjson_is_none(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text('{"type":"result","sub')
        assert detect_provider_failure(output).kind is ProviderFailure.NONE

    @pytest.mark.unit
    def test_empty_output_is_none(self, tmp_path):
        output = tmp_path / "output.txt"
        output.write_text("")
        assert detect_provider_failure(output).kind is ProviderFailure.NONE

    @pytest.mark.unit
    def test_missing_file_is_none(self, tmp_path):
        output = tmp_path / "nonexistent.txt"
        assert detect_provider_failure(output).kind is ProviderFailure.NONE

    # --- subtype-trap + conservative default -------------------------------

    @pytest.mark.unit
    def test_subtype_trap_keys_on_is_error_not_subtype(self, tmp_path):
        # subtype is "success" EVEN THOUGH is_error is true on a 429 — a detector
        # that keyed on subtype would return NONE here (the trap).
        output = tmp_path / "output.txt"
        output.write_text(
            '{"type":"result","subtype":"success","is_error":true,'
            '"api_error_status":429,'
            '"result":"API Error: Request rejected (429) · This request would '
            "exceed your account's rate limit. Please try again later.\"}\n"
        )
        assert (
            detect_provider_failure(output).kind is ProviderFailure.SINGLE_ACCOUNT_LIMIT
        )

    @pytest.mark.unit
    def test_429_with_neither_body_conservative_default(self, tmp_path):
        # 429 with no recognizable body → conservative SINGLE_ACCOUNT_LIMIT.
        output = tmp_path / "output.txt"
        output.write_text(
            '{"type":"result","subtype":"success","is_error":true,'
            '"api_error_status":429,"result":"API Error: Request rejected (429)"}\n'
        )
        assert (
            detect_provider_failure(output).kind is ProviderFailure.SINGLE_ACCOUNT_LIMIT
        )

    # --- shared-core equivalence -------------------------------------------

    @pytest.mark.unit
    def test_text_core_matches_path_wrapper(self):
        path = _FIXTURES / "all_account_cooldown.jsonl"
        from_text = _provider_failure_from_text(path.read_text())
        from_path = detect_provider_failure(path)
        assert from_text == from_path
        assert isinstance(from_text, ProviderFailureSignal)
        assert from_text.kind is ProviderFailure.ALL_ACCOUNT_COOLDOWN

    # --- 12-row detection-contract table (spec §6.2; research/04 matrix) ----

    @pytest.mark.unit
    @pytest.mark.parametrize(
        "source, expected_kind, expected_model",
        [
            pytest.param(
                ("fixture", "all_account_cooldown.jsonl"),
                ProviderFailure.ALL_ACCOUNT_COOLDOWN,
                "claude-opus-4-8",
                id="shape1-all-account",
            ),
            pytest.param(
                ("fixture", "single_account_429.jsonl"),
                ProviderFailure.SINGLE_ACCOUNT_LIMIT,
                None,
                id="shape1-single",
            ),
            pytest.param(
                ("fixture", "api_retry_maxed.jsonl"),
                ProviderFailure.SINGLE_ACCOUNT_LIMIT,
                None,
                id="shape1-retry-maxed",
            ),
            pytest.param(
                ("fixture", "all_account_cooldown_apierror429.jsonl"),
                ProviderFailure.ALL_ACCOUNT_COOLDOWN,
                "gpt-5.5",
                id="shape2-all-account-gpt55",
            ),
            pytest.param(
                (
                    "inline",
                    '{"type":"result","subtype":"success","is_error":true,'
                    '"api_error_status":429,'
                    '"result":"API Error: Request rejected (429) · All '
                    'credentials for model claude-opus-4-8 are cooling down"}\n',
                ),
                ProviderFailure.ALL_ACCOUNT_COOLDOWN,
                "claude-opus-4-8",
                id="all-account-no-viaprovider-aes",
            ),
            pytest.param(
                (
                    "inline",
                    '{"type":"result","subtype":"success","is_error":true,'
                    '"result":"API Error: 429 rate_limit_error · All '
                    "credentials for model claude-opus-4-8 are cooling down "
                    'via provider claude"}\n',
                ),
                ProviderFailure.ALL_ACCOUNT_COOLDOWN,
                "claude-opus-4-8",
                id="shape1-all-account-no-aes",
            ),
            pytest.param(
                ("fixture", "single_account_apierror429_SYNTHESIZED.jsonl"),
                ProviderFailure.SINGLE_ACCOUNT_LIMIT,
                None,
                # SYNTHESIZED: documented ASSUMPTION — no verbatim Shape-2
                # single-account capture exists (OQ2). xfail(strict=False)
                # advertises it: RED pre-fix (gate closed), xpass post-fix.
                marks=pytest.mark.xfail(
                    reason="synthesized — no verbatim Shape-2 single-account "
                    "capture; flip to a real fixture when captured",
                    strict=False,
                ),
                id="shape2-single-SYNTHESIZED",
            ),
            pytest.param(
                (
                    "inline",
                    '{"type":"result","subtype":"success","is_error":true,'
                    '"result":"API Error: 429 rate_limit_error unspecified '
                    'upstream throttle"}\n',
                ),
                ProviderFailure.SINGLE_ACCOUNT_LIMIT,
                None,
                id="rate_limit_error-neither-body",
            ),
            pytest.param(
                ("fixture", "provider_429_incidental_ratelimit_text.jsonl"),
                ProviderFailure.NONE,
                None,
                id="fp-incidental-429",
            ),
            pytest.param(
                ("fixture", "operation_timeout.jsonl"),
                ProviderFailure.OPERATION_TIMEOUT,
                None,
                id="timeout",
            ),
            pytest.param(
                ("fixture", "task_failure_real.jsonl"),
                ProviderFailure.NONE,
                None,
                id="real-task-failure",
            ),
            pytest.param(
                ("fixture", "clean_pass.jsonl"),
                ProviderFailure.NONE,
                None,
                id="clean-pass",
            ),
        ],
    )
    def test_detection_contract_row(
        self, tmp_path, source, expected_kind, expected_model
    ):
        # Maps transcript -> (kind, resolved_model) for every meaningful case
        # (spec §6.2). Asserts BOTH kind (identity) and resolved_model
        # (equality, incl. == None on the 8 non-cooldown rows, OQ4). Does NOT
        # call SessionResetPolicy.decide / assert any Action.* value (C3).
        source_kind, source_value = source
        if source_kind == "fixture":
            path = _FIXTURES / source_value
        else:
            path = tmp_path / "output.txt"
            path.write_text(source_value)
        sig = detect_provider_failure(path)
        assert sig.kind is expected_kind
        assert sig.resolved_model == expected_model

    # --- parity 7a: shared-inner text-core == path-wrapper on Shape-2 -------

    @pytest.mark.unit
    def test_shape2_text_core_matches_path_wrapper(self):
        # Parity §6.3.1: the text core and the path wrapper must agree on the
        # new load-bearing Shape-2 fixture (NOT the Shape-1 all_account_cooldown).
        # ProviderFailureSignal is a dataclass, so == compares (kind, model).
        path = _FIXTURES / "all_account_cooldown_apierror429.jsonl"
        from_text = _provider_failure_from_text(path.read_text())
        from_path = detect_provider_failure(path)
        assert from_text == from_path
        assert isinstance(from_text, ProviderFailureSignal)
        assert from_text.kind is ProviderFailure.ALL_ACCOUNT_COOLDOWN
        assert from_text.resolved_model == "gpt-5.5"

    # --- F5 timeout mutual-exclusivity guard (two directional assertions) ---

    @pytest.mark.unit
    def test_f5_timeout_mutual_exclusivity_guard(self):
        # F5 (research/04 R-GC): the timeout branch and the widened 429 gate stay
        # mutually exclusive — a "both signals in one body" fixture is impossible
        # (timeout requires body == "API Error: The operation timed out."; the
        # 429 gate requires "rate_limit_error" in body). Two directional asserts:
        # F5.a — timeout NOT swallowed: the timeout body has no rate_limit_error
        # and api_error_status is None, so both new C1 disjuncts are False →
        # control reaches the timeout branch.
        assert (
            detect_provider_failure(_FIXTURES / "operation_timeout.jsonl").kind
            is ProviderFailure.OPERATION_TIMEOUT
        )
        # F5.b — 429 returns BEFORE the timeout branch: the 429 block returns at
        # :323-333, so a Shape-2 cooldown never falls through to OPERATION_TIMEOUT.
        assert (
            detect_provider_failure(
                _FIXTURES / "all_account_cooldown_apierror429.jsonl"
            ).kind
            is ProviderFailure.ALL_ACCOUNT_COOLDOWN
        )

    # --- INV-004: result-body scoping keys only on the LAST result event ----

    @pytest.mark.unit
    def test_inv004_result_body_scoping_last_event_only(self, tmp_path):
        # INV-004 (C5 result-body scoping, spec §7): the widened
        # "rate_limit_error" in body gate must scan ONLY the last
        # {"type":"result"} event's result field, never bleed transcript-wide.
        # An earlier non-terminal event carries incidental rate_limit_error prose;
        # the terminal result is a real NON-provider failure with no
        # rate_limit_error token. A transcript-wide scan would wrongly trip this to
        # SINGLE_ACCOUNT_LIMIT via the neither-body default. GREEN pre- AND
        # post-fix (invariant guard, NOT part of the RED set). Distinct from
        # contract row 11 (which lacks the earlier-event bleed vector).
        output = tmp_path / "output.txt"
        output.write_text(
            '{"type":"assistant","message":{"content":"retrying after a '
            'rate_limit_error from upstream"}}\n'
            '{"type":"result","subtype":"success","is_error":true,'
            '"result":"error_during_execution: pytest exited 1"}\n'
        )
        sig = detect_provider_failure(output)
        assert sig.kind is ProviderFailure.NONE
        assert sig.resolved_model is None
