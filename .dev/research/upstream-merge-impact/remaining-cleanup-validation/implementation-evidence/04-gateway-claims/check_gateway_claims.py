"""Static boundary/preservation check for plan 04 (gateway claims).

Usage (from the repo root):
    uv run python <this file> baseline   # before edits: write baseline.json
    uv run python <this file> check      # after edits: verify, exit 1 on failure

Read-only except for baseline.json. No network, Docker, installer or test run.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASELINE = HERE / "baseline.json"
START = "**Recommended**: Use **airis-mcp-gateway**"
END = "**Individual servers (not in the gateway;"
PROTECTED_FILES = [
    "src/superclaude/cli/install_mcp.py",
    "src/superclaude/core/CLAUDE.md",
    "tests/cli/test_install_codebase_memory.py",
]
PROTECTED_DIRS = ["src/superclaude/mcp"]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], check=True, capture_output=True, text=True
    ).stdout


def split_claude() -> tuple[str, str, str]:
    text = Path("CLAUDE.md").read_text(encoding="utf-8")
    assert text.count(START) == 1 and text.count(END) == 1, "anchors not unique"
    i, j = text.index(START), text.index(END)
    assert i < j, "anchors out of order"
    return text[:i], text[i:j], text[j:]


def protected_hashes() -> dict[str, str]:
    paths = list(PROTECTED_FILES)
    for d in PROTECTED_DIRS:
        paths += [str(p) for p in sorted(Path(d).rglob("*")) if p.is_file()]
    return {p: sha(Path(p).read_bytes()) for p in paths}


def product_status() -> list[str]:
    """Porcelain lines outside .dev/ (task evidence/ledgers live there)."""
    return [
        ln
        for ln in git("status", "--porcelain", "--untracked-files=all").splitlines()
        if not ln[3:].startswith(".dev/")
    ]


def baseline() -> None:
    pre, para, post = split_claude()
    data = {
        "branch": git("rev-parse", "--abbrev-ref", "HEAD").strip(),
        "head": git("rev-parse", "HEAD").strip(),
        "product_status": product_status(),
        "protected": protected_hashes(),
        "prefix_sha": sha(pre.encode()),
        "suffix_sha": sha(post.encode()),
        "paragraph": para,
    }
    BASELINE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"baseline written: head={data['head']} protected={len(data['protected'])}")


def check() -> int:
    base = json.loads(BASELINE.read_text())
    pre, para, post = split_claude()
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        print(("PASS " if cond else "FAIL ") + msg)
        if not cond:
            fails.append(msg)

    ok(git("rev-parse", "HEAD").strip() == base["head"], "HEAD unchanged")
    ok(
        product_status() == [" M CLAUDE.md"],
        f"only product change is CLAUDE.md (status={product_status()})",
    )
    ok(sha(pre.encode()) == base["prefix_sha"], "CLAUDE.md text before paragraph identical")
    ok(sha(post.encode()) == base["suffix_sha"], "CLAUDE.md text after paragraph identical")
    ok(para != base["paragraph"], "gateway paragraph changed")
    cur = protected_hashes()
    ok(cur == base["protected"], f"{len(cur)} protected files byte-identical")

    # Preserved inside the paragraph: recommendation, Auggie rule, default command.
    for keep in [
        START,
        "**HIGHEST PRIORITY SERVER**",
        "Auggie MCP should be used whenever broader codebase context",
        "superclaude mcp  # Interactive install, gateway is default (requires Docker)",
    ]:
        ok(keep in para, f"kept: {keep[:50]}")

    # Required disclosures.
    low = para.lower()
    for need in ["fresh", "mindbase", "airis-agent", "enabled", "already-existing", "reused", "minimal default config",
                 "manual", "clone", "unverified"]:
        ok(need in low, f"paragraph mentions '{need}'")
    ok("not included in the distribution compose" in low or
       "not in the distribution compose" in low, "states reason: containers not in distribution Compose")
    # Forbidden claims.
    for need in ["non-zero", "empty config", "as-is", "successful fresh-template path"]:
        ok(need in low, f"paragraph mentions '{need}'")
    for bad in ["disproved", "always disabled", "cross-session learning",
                "are not enabled by the built-in install", "gateway's own advertised"]:
        ok(bad not in low, f"paragraph lacks '{bad}'")
    ok("(included in gateway)" not in low, "no unqualified 'included in gateway' list header")

    # Compare the description against the source branches (static, no network).
    src = Path("src/superclaude/cli/install_mcp.py").read_text(encoding="utf-8")
    for needle in [
        'servers_to_disable = ["airis-agent", "mindbase"]',
        'config["mcpServers"][server_name]["enabled"] = False',
        "if not mcp_config_file.exists():",
        "MCP server configuration already exists",
        "Created minimal default mcp-config.json",
        "Could not parse mcp-config.json, using as-is",
        "not in docker-compose.dist.yml",
        "mcp_config_file.write_text('{\"mcpServers\": {}}')",
    ]:
        ok(needle in src, f"source branch present: {needle[:55]}")

    print("RESULT:", "FAIL" if fails else "PASS")
    return 1 if fails else 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "baseline":
        baseline()
    elif mode == "check":
        sys.exit(check())
    else:
        sys.exit("usage: baseline|check")
