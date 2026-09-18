"""Load packaged execution policies for generated prompts."""

from importlib import resources

_POLICY_NAME = "BASH_INSPECTION_POLICY.md"


def load_bash_inspection_policy() -> str:
    """Return the canonical Bash inspection policy from the installed package."""
    resource = resources.files("superclaude").joinpath("core").joinpath(_POLICY_NAME)
    try:
        return resource.read_text(encoding="utf-8").strip()
    except (FileNotFoundError, OSError) as exc:
        raise RuntimeError(f"Packaged policy missing: {_POLICY_NAME}") from exc


BASH_INSPECTION_POLICY = load_bash_inspection_policy()
