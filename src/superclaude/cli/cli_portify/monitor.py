"""Output monitoring and timing capture.

Implements:
- OutputMonitor tracking 8 metrics (NFR-009, T03.11)
- Stall accounting on growth_rate_bps drop (R-001); callers decide on action
- TimingCapture for per-phase and per-step timing
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

from superclaude.cli.cli_portify.contract import StepTiming
from superclaude.cli.cli_portify.models import MonitorState

# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------


@dataclass
class PhaseTiming:
    phase: int
    step_timings: list[StepTiming] = field(default_factory=list)

    @property
    def total_duration(self) -> float:
        return sum(s.duration_seconds for s in self.step_timings)


class TimingCapture:
    """Captures per-phase and per-step timing."""

    def __init__(self) -> None:
        self._step_timings: dict[str, StepTiming] = {}
        self._phase_timings: dict[int, PhaseTiming] = {}
        self._pipeline_start: float = 0.0
        self._pipeline_end: float = 0.0

    def start_pipeline(self) -> None:
        self._pipeline_start = time.monotonic()

    def end_pipeline(self) -> None:
        self._pipeline_end = time.monotonic()

    @property
    def total_duration(self) -> float:
        return self._pipeline_end - self._pipeline_start

    def start_step(self, step: str, phase: int = 0) -> None:
        st = StepTiming(step=step, phase=phase, start_time=time.monotonic())
        self._step_timings[step] = st
        if phase not in self._phase_timings:
            self._phase_timings[phase] = PhaseTiming(phase=phase)

    def end_step(self, step: str) -> None:
        if step in self._step_timings:
            st = self._step_timings[step]
            st.end_time = time.monotonic()
            st.duration_seconds = st.end_time - st.start_time
            phase = st.phase
            if phase in self._phase_timings:
                self._phase_timings[phase].step_timings.append(st)

    def get_step_timing(self, step: str) -> Optional[StepTiming]:
        return self._step_timings.get(step)

    def get_phase_timing(self, phase: int) -> Optional[PhaseTiming]:
        return self._phase_timings.get(phase)

    @property
    def step_timings(self) -> list[StepTiming]:
        return list(self._step_timings.values())


# ---------------------------------------------------------------------------
# OutputMonitor (NFR-009, R-001)
# ---------------------------------------------------------------------------


class OutputMonitor:
    """Tracks 8 output metrics and detects stalls via growth_rate_bps.

    Stall detection: if growth_rate_bps drops below stall_threshold_bps for
    stall_timeout_seconds, the stall_seconds counter accumulates. Callers
    should check state.stall_seconds to decide on action.
    """

    def __init__(
        self,
        stall_threshold_bps: float = 1.0,
        stall_timeout_seconds: float = 60.0,
    ) -> None:
        self.state = MonitorState()
        self._stall_threshold_bps = stall_threshold_bps
        self._stall_timeout_seconds = stall_timeout_seconds
        self._last_update_time: float = time.monotonic()
        self._last_bytes: int = 0

    def update(self, new_bytes: int, new_lines: int = 0) -> None:
        """Update metrics with fresh byte/line count."""
        now = time.monotonic()
        elapsed = now - self._last_update_time
        delta_bytes = new_bytes - self._last_bytes

        if elapsed > 0:
            self.state.growth_rate_bps = delta_bytes / elapsed
        else:
            self.state.growth_rate_bps = float(delta_bytes)

        self.state.output_bytes = new_bytes
        self.state.line_count += new_lines
        self.state.events += 1

        if self.state.growth_rate_bps < self._stall_threshold_bps:
            self.state.stall_seconds += elapsed
        else:
            self.state.stall_seconds = 0.0

        self._last_bytes = new_bytes
        self._last_update_time = now

    def set_convergence_iteration(self, n: int) -> None:
        """Set the current convergence iteration number."""
        self.state.convergence_iteration = n

    def increment_findings(self, n: int) -> None:
        """Increment the findings count by n."""
        self.state.findings_count += n

    def set_placeholder_count(self, n: int) -> None:
        """Set the current placeholder sentinel count."""
        self.state.placeholder_count = n
