# Frozen review target for the bare-review CLI-vs-golden parity gate.
# Committed so its sha256 is stable: the golden `target_checksum` is the
# sha256 of THIS file's bytes, and the gate passes this path to
# `swarm run --lens bare-review --target <this>`. Do not edit without
# regenerating the golden (SWARM_REGEN_GOLDEN=1) — see golden/README.md.
def hello(name: str) -> str:
    return f"hello {name}"


def add(a: int, b: int) -> int:
    return a + b


# padding so the target clears the IMM-4 non-whitespace byte floor cleanly
