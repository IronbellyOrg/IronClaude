"""Jev budget: pre-flight reservations, fcntl-locked ledger (contract J4, D6-compatible)."""
import contextlib
import fcntl
import json
import os
import pathlib

from .config import PRICE_USD_PER_MTOK_INPUT


class BudgetExhausted(Exception):
    pass


def usd(tokens) -> float:
    return tokens * PRICE_USD_PER_MTOK_INPUT / 1e6


class Budget:
    def __init__(self, path, *, ceiling_usd: float, ceiling_input_tokens: int):
        self.path = pathlib.Path(path)
        self.ceiling_usd = float(ceiling_usd)
        self.ceiling_tokens = int(ceiling_input_tokens)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._tx() as led:
            led["experiment"] = led.get("experiment") or self.path.stem
            led["ceiling_usd"] = self.ceiling_usd
            led["ceiling_input_tokens"] = self.ceiling_tokens

    # ---- ledger io
    @contextlib.contextmanager
    def _tx(self):
        lock = str(self.path) + ".lock"
        with open(lock, "w") as lf:
            fcntl.flock(lf, fcntl.LOCK_EX)
            try:
                if self.path.exists() and self.path.stat().st_size:
                    led = json.loads(self.path.read_text())
                else:
                    led = {"experiment": self.path.stem, "ceiling_usd": self.ceiling_usd,
                           "ceiling_input_tokens": self.ceiling_tokens, "spent_tokens": 0, "spent_usd": 0.0,
                           "reserved": {}, "draws": {}}
                yield led
                tmp = str(self.path) + f".tmp{os.getpid()}"
                with open(tmp, "w") as f:
                    json.dump(led, f, indent=1)
                os.replace(tmp, self.path)
            finally:
                fcntl.flock(lf, fcntl.LOCK_UN)

    @staticmethod
    def _committed(led):
        pending = sum(d["est"] for d in led["draws"].values() if d.get("actual") is None)
        undrawn = sum(max(r["tokens"] - r["drawn"], 0) for r in led["reserved"].values())
        return led["spent_tokens"] + pending + undrawn, undrawn

    def _fits(self, led, extra_tokens):
        committed, _ = self._committed(led)
        total = committed + extra_tokens
        return total <= led["ceiling_input_tokens"] and usd(total) <= led["ceiling_usd"] + 1e-12

    # ---- api
    def reserve_phase(self, phase: str, est_input_tokens: int) -> None:
        est = int(est_input_tokens)
        with self._tx() as led:
            if not self._fits(led, est):
                raise BudgetExhausted(f"reserve {phase}: {est} tokens does not fit "
                                      f"(committed {self._committed(led)[0]}, ceiling {led['ceiling_input_tokens']} tokens / ${led['ceiling_usd']})")
            r = led["reserved"].setdefault(phase, {"tokens": 0, "drawn": 0})
            r["tokens"] += est

    def draw(self, phase: str, est_tokens: int) -> str:
        est = int(est_tokens)
        with self._tx() as led:
            r = led["reserved"].get(phase)
            undrawn = max(r["tokens"] - r["drawn"], 0) if r else 0
            if undrawn < est and not self._fits(led, est - undrawn):
                raise BudgetExhausted(f"draw {phase}: {est} tokens (undrawn {undrawn}) exceeds the ceiling")
            did = f"d{len(led['draws']) + 1:06d}"
            led["draws"][did] = {"phase": phase, "est": est, "actual": None, "usage_missing": False}
            if r is not None:
                r["drawn"] += est
            return did

    def settle(self, draw_id: str, actual_input_tokens) -> None:
        with self._tx() as led:
            d = led["draws"][draw_id]
            if d.get("actual") is not None:
                return
            if actual_input_tokens is None:
                d["actual"] = d["est"]
                d["usage_missing"] = True
            else:
                d["actual"] = int(actual_input_tokens)
            led["spent_tokens"] += d["actual"]
            led["spent_usd"] = usd(led["spent_tokens"])

    def release_phase(self, phase: str) -> None:
        with self._tx() as led:
            led["reserved"].pop(phase, None)

    def state(self) -> dict:
        with self._tx() as led:
            committed, undrawn = self._committed(led)
            return {"ceiling_usd": led["ceiling_usd"], "ceiling_input_tokens": led["ceiling_input_tokens"],
                    "spent_usd": led["spent_usd"], "spent_tokens": led["spent_tokens"],
                    "committed_tokens": committed, "undrawn_reserved_tokens": undrawn,
                    "reserved": json.loads(json.dumps(led["reserved"]))}
