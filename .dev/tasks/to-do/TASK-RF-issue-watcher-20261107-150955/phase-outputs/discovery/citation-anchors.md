# Citation anchors (Step 1.5), re-verified 2026-11-07 from the file contents

| Anchor | Expected content | Status | Current lines |
|---|---|---|---|
| `src/superclaude/cli/main.py:559` | reflect import line with `# noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports` | CONFIRMED | 559 |
| `src/superclaude/cli/main.py:561` | `main.add_command(reflect_group, name="reflect")` | CONFIRMED | 561 |
| `src/superclaude/cli/main.py:564` | `if __name__ == "__main__":` | CONFIRMED | 564 |
| `src/superclaude/cli/swarm/atomic.py:14` | `def write_prepared_bytes(path: Path, data: bytes) -> int:` | CONFIRMED | 14 |
| `src/superclaude/cli/swarm/atomic.py:33` | `except Exception:` cleanup | CONFIRMED | 33 |
| `src/superclaude/cli/install_user_setup.py:35` | `_ORCA_CLIS = ("orca-ide", "orca")` | CONFIRMED | 35 |
| `src/superclaude/cli/install_user_setup.py:198-221` | `_find_orca() -> str \| None` (ends with `return None`) | CONFIRMED | 198-221 |
| `origin_repo.py:65-69` | `_NAME` and `_ORIGIN_PATTERNS` (two compiled patterns, github.com https and ssh) | CONFIRMED | 65-69 |
| `origin_repo.py:86-99` | `parse_origin_url` | CONFIRMED | 86-99 |
| `refs/claim.md:29` | marker `<!-- sc:issue:claim -->` | CONFIRMED | 29 |
| `templates/claim-comment.md:23` | `<!-- sc:issue:claim -->` | CONFIRMED | 23 |
| `.github/workflows/test.yml:22` | `python-version: "3.10"` | CONFIRMED | 22 |
| `.github/workflows/test.yml:29` | `uv pip install -e ".[dev]" "pytest-xdist>=3.5,<4"` | CONFIRMED | 29 |
| `.github/workflows/test.yml:47` | `pytest ... -n auto --maxfail=3 ...` | CONFIRMED | 47 |
| `pyproject.toml:16` | `requires-python = ">=3.10"` | CONFIRMED | 16 |
| `pyproject.toml:114` | `--strict-markers` | CONFIRMED | 114 |
| `pyproject.toml:135` | `property_based` marker text mentioning hypothesis | CONFIRMED | 135 |
| `pyproject.toml:174-184` | ruff `line-length = 88`, `target-version = "py310"`, excludes, `select = ["E","F","I","N","W","TID"]` | CONFIRMED | 174-184 |
| `src/superclaude/cli/issue_watch/` | does not exist | CONFIRMED absent | n/a |
| `tests/issue_watch/` | does not exist | CONFIRMED absent | n/a |
