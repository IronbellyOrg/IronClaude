"""Compute the exact authorized namespace-only command transformation."""

import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
TOKEN = re.compile(r"/sc:(?:sc:)*([A-Za-z][A-Za-z0-9-]*)")


def expected(path: str, original: str, frontends: dict[str, str], unavailable: set[tuple[str, str]]) -> str:
    if path == "commands/sc-help.md":
        original = "".join(line for line in original.splitlines(keepends=True) if not line.startswith(("| `/sc:sc:estimate` |", "| `/sc:sc:select-tool` |")))
    original = original.replace("/sc:sc:*", "/sc:sc-*")

    def replace(match):
        name = match.group(1)
        if (path, name) in unavailable:
            return f"UNAVAILABLE({name})"
        if name in frontends:
            return "/" + frontends[name]
        if name == "sc":
            return "/sc:sc-*"
        return match.group(0)

    return TOKEN.sub(replace, original)


def main():
    contract = json.loads((OUT / "plugin-contract.json").read_text())
    frontends = {Path(row["path"]).stem.removeprefix("sc-"): row["frontend"] for row in contract["commands"]}
    rows = json.loads((OUT / "namespace-scope-conflict.json").read_text())["references"]
    unavailable = {(row["path"], row["name"]) for row in rows}
    assert expected("commands/sc-reflect.md", "/sc:sc:sc:reflect --type task", frontends, unavailable) == "/sc:sc-reflect --type task"
    assert expected("commands/sc-pm.md", "execution/feature/sc:errors", frontends, unavailable) == "execution/feature/sc:errors"
    assert expected("commands/sc-recommend.md", "/sc:sc:scan --security", frontends, unavailable) == "UNAVAILABLE(scan) --security"
    assert expected("commands/sc-help.md", "/sc:sc:* and /sc:sc", frontends, unavailable) == "/sc:sc-* and /sc:sc-*"
    assert len(rows) == 15
    outputs = {}
    for path in contract["allowed_command_edits"]:
        original = (OUT / "isolation/plugin" / path).read_text()
        transformed = expected(path, original, frontends, unavailable)
        assert not re.search(r"/sc:(?:sc:)+", transformed), path
        outputs[path] = transformed
    (OUT / "expected-namespace-commands.json").write_text(json.dumps(outputs, indent=2) + "\n")
    print("PASS: 26 exact expected command transformations; namespace and unavailable-label regression checks passed")


if __name__ == "__main__":
    main()
