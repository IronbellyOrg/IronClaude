"""Reflect-wrapper thin orchestrator + atomic race-safe frontmatter write-back.

``ReflectRunner.run`` is the THIN orchestration path (NFR-1, no reflect-logic
duplication): derive -> preflight -> build prompt + ``ClaudeProcess`` -> launch
-> parse contract -> derive verdict (delegated to ``contract.py``) -> atomic
race-safe frontmatter write-back (FR-6) + ``wrapper-result.yaml`` sidecar (FR-7).

Isolation guardrails:
- No imports from ``superclaude.cli.sprint`` or ``superclaude.cli.roadmap``.
- Zero ``async def`` / ``await``.
- The only reflect-launch path is ``ClaudeProcess`` (subprocess) -- never an
  Agent/Task surface (NFR-7).

The ``_IndentDumper`` is copied locally (lower coupling than importing the
private symbol from ``recommend.cache``); the atomic writer uses a randomized
same-dir temp name so parallel sessions never collide on a deterministic
``.tmp`` suffix.
"""

from __future__ import annotations

import os
import re
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

import yaml

from superclaude.cli.pipeline.process import ClaudeProcess

from .contract import derive_verdict, parse_contract
from .models import ReflectConfig, ReflectResult, Verdict

# The three model-class aliases reflect resolves at Wave 0 for Tier-2 topology.
_MODEL_ALIAS_ENV_VARS = (
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
)

# First ``---...---`` frontmatter block (preamble-tolerant, non-greedy).
_FRONTMATTER_RE = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*$", re.MULTILINE | re.DOTALL)
# Top-level ``reflect_post:`` key line (column-0, no indent).
_REFLECT_POST_KEY_RE = re.compile(r"^reflect_post\s*:")


class _IndentDumper(yaml.SafeDumper):
    """SafeDumper that indents block sequences under their key (yamllint-conformant).

    PyYAML's default places a block sequence's ``-`` at the parent key's indent,
    which the repo yamllint config (``indent-sequences: true``) rejects.
    Overriding ``increase_indent`` to never go indentless emits ``key:\\n  - item``.
    """

    def increase_indent(self, flow=False, indentless=False):  # noqa: N802 (PyYAML API)
        return super().increase_indent(flow, False)


def _atomic_write_text(path: Path, text: str) -> None:
    """Atomically write ``text`` to ``path`` (randomized same-dir temp + os.replace).

    Uses a randomized same-directory temp name (NOT a deterministic ``.tmp``
    suffix, which collides under parallel sessions) so ``os.replace`` stays
    atomic and the worktree-concurrency last-write-wins window is bounded. A
    ``finally`` block removes a leftover temp file if ``os.replace`` never ran.
    """
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    tmp = parent / f".{path.name}.tmp.{os.getpid()}.{uuid.uuid4().hex}"
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def _build_reflect_post_value(
    result: ReflectResult, *, head: str, reviewed_at: str
) -> dict:
    """Build the §6 structured ``reflect_post`` mapping (field order is fixed)."""
    run_id = reviewed_at
    if result.contract_path:
        run_id = Path(result.contract_path).parent.name or reviewed_at
    deviations = result.deviations or {}
    return {
        "verdict": result.verdict.value,
        "status": result.status,
        "run_id": run_id,
        "tier_reached": result.tier_reached,
        "report": result.report_path,
        "contract": result.contract_path,
        "reason": result.reason,
        "deviations": {
            "authorized": int(deviations.get("authorized", 0) or 0),
            "necessary": int(deviations.get("necessary", 0) or 0),
            "drift": int(deviations.get("drift", 0) or 0),
            "regression": int(deviations.get("regression", 0) or 0),
        },
        "head": head,
        "reviewed_at": reviewed_at,
    }


def write_reflect_post(
    tasklist_path: Path,
    result: ReflectResult,
    *,
    head: str,
    reviewed_at: str,
) -> str:
    """Atomically replace ONLY the ``reflect_post:`` frontmatter block (FR-6).

    Reads the tasklist bytes once, string-splices the new ``reflect_post:``
    block in place (preserving every other byte of the frontmatter AND the
    entire markdown body), then applies the compare-before-write race guard:
    if the on-disk bytes changed since the read, does NOT overwrite and returns
    ``"frontmatter-stale"`` (the caller writes the sidecar and exits non-zero).
    Otherwise atomically writes and returns ``"written"``.

    Only the ``reflect_post:`` block is re-serialized (with ``_IndentDumper``,
    block style per OQ5) -- sibling frontmatter keys are never re-dumped, so
    they stay byte-for-byte identical. ``extract_frontmatter`` is deliberately
    NOT used (it drops the nested ``deviations`` mapping).
    """
    raw = tasklist_path.read_bytes()
    # F1: normalize CRLF -> LF for matching + splice-index computation, mirroring
    # the canonical ``extract_frontmatter`` parser (frontmatter.py). ``raw`` (the
    # ORIGINAL bytes) is preserved for the race guard below. FR-6 byte-preservation
    # is about not corrupting/reordering body CONTENT, not preserving CR bytes:
    # we normalize the whole working text to LF and write LF-consistent output.
    text = raw.decode("utf-8").replace("\r\n", "\n")

    fm_match = _FRONTMATTER_RE.search(text)
    if fm_match is None:
        return "frontmatter-missing"

    value = _build_reflect_post_value(result, head=head, reviewed_at=reviewed_at)
    dumped = yaml.dump(
        {"reflect_post": value},
        Dumper=_IndentDumper,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )
    dumped_lines = dumped.rstrip("\n").split("\n")

    body = fm_match.group(1)
    lines = body.split("\n")
    start_idx: int | None = None
    for i, line in enumerate(lines):
        if _REFLECT_POST_KEY_RE.match(line):
            start_idx = i
            break

    if start_idx is None:
        # No existing reflect_post: key -- append the block to the frontmatter.
        new_lines = lines + dumped_lines
    else:
        end_idx = start_idx + 1
        while end_idx < len(lines) and lines[end_idx].startswith((" ", "\t")):
            end_idx += 1
        new_lines = lines[:start_idx] + dumped_lines + lines[end_idx:]

    new_body = "\n".join(new_lines)
    new_text = text[: fm_match.start(1)] + new_body + text[fm_match.end(1) :]

    # RACE GUARD: do not overwrite if the file changed since we read it.
    if tasklist_path.read_bytes() != raw:
        return "frontmatter-stale"

    _atomic_write_text(tasklist_path, new_text)
    return "written"


def write_sidecar(
    output_dir: Path,
    result: ReflectResult,
    *,
    env_alias_count: int,
    write_status: str,
) -> Path:
    """Write the ``wrapper-result.yaml`` sidecar (FR-7) -- ALWAYS, any verdict.

    The sidecar is the dual gate signal that survives even when the frontmatter
    write fails: it records the derived verdict, raw status, tier, reason,
    report/contract paths, deviations, the child exit code, the preflight
    ``env_alias_count`` (number of ``ANTHROPIC_DEFAULT_*`` aliases in the exact
    child env), and the frontmatter ``write_status``. Returns the sidecar path.
    """
    deviations = result.deviations or {}
    data = {
        "verdict": result.verdict.value,
        "status": result.status,
        "tier_reached": result.tier_reached,
        "reason": result.reason,
        "report": result.report_path,
        "contract": result.contract_path,
        "deviations": {
            "authorized": int(deviations.get("authorized", 0) or 0),
            "necessary": int(deviations.get("necessary", 0) or 0),
            "drift": int(deviations.get("drift", 0) or 0),
            "regression": int(deviations.get("regression", 0) or 0),
        },
        "child_exit_code": result.child_exit_code,
        "env_alias_count": env_alias_count,
        "write_status": write_status,
    }
    sidecar_path = output_dir / "wrapper-result.yaml"
    _atomic_write_text(
        sidecar_path,
        yaml.dump(
            data,
            Dumper=_IndentDumper,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
        ),
    )
    return sidecar_path


def _child_env() -> dict[str, str]:
    """Reconstruct the EXACT env the child reflect will see (FR-10/FR-11).

    Builds a throwaway ``ClaudeProcess`` and calls its public, side-effect-free
    ``build_env()`` so the alias count matches what the child sees. Do NOT scrub
    env by hand -- ``build_env`` already pops ``CLAUDECODE`` /
    ``CLAUDE_CODE_ENTRYPOINT`` and preserves HOME/MCP/``ANTHROPIC_DEFAULT_*``.
    """
    probe = ClaudeProcess(
        prompt="",
        output_file=Path(os.devnull),
        error_file=Path(os.devnull),
    )
    return probe.build_env()


def count_model_aliases(env: dict[str, str]) -> int:
    """Count present-and-non-empty ``ANTHROPIC_DEFAULT_*_MODEL`` aliases in ``env``.

    ≥3 distinct classes -> full Tier-2 diversity; 2 -> degraded; 0-1 -> T1-only
    (research 08 §4). The count is recorded in the sidecar; low counts surface
    as a ``degraded`` verdict via the contract, not as a preflight blocker.
    """
    return sum(1 for var in _MODEL_ALIAS_ENV_VARS if (env.get(var) or "").strip())


def preflight(config: ReflectConfig) -> str | None:
    """Validate launch prerequisites; return a blocker slug or ``None``.

    Asserts the ``claude`` binary is present (before launch) and the resolved
    inputs are sane (tasklist present, base/head resolved). Returns a short slug
    the caller routes to ``blocked`` (e.g. ``"claude-binary-missing"``,
    ``"base-unresolved"``), or ``None`` on success.

    This function does NOT construct ``ClaudeProcess`` so it is safe in the
    FR-12 dry-run/print path; the exact-child-env alias count is taken via
    ``_child_env()`` on the real launch path only. No env scrubbing is performed
    (FR-10 -- the default ``ClaudeProcess(env_vars=None)`` already provides the
    bare real-env overlay).
    """
    if shutil.which("claude") is None:
        return "claude-binary-missing"
    if not config.tasklist_path.is_file():
        return "tasklist-missing"
    if not config.base:
        return "base-unresolved"
    if not config.head:
        return "head-unresolved"
    return None


def _read_existing_reflect_post(tasklist_path: Path) -> dict | None:
    """Parse the existing ``reflect_post`` mapping from the frontmatter (G2).

    Parses the ``reflect_post:`` block directly (NOT via ``extract_frontmatter``,
    which drops the nested mapping). Returns the mapping (or ``None`` when no
    parseable block is present / the value is not a mapping, e.g. ``PENDING``).
    """
    try:
        text = tasklist_path.read_text(encoding="utf-8")
    except OSError:
        return None
    # F1: normalize CRLF -> LF before matching (mirror extract_frontmatter) so a
    # CRLF-saved tasklist's reflect_post block parses (read-only path, no write).
    text = text.replace("\r\n", "\n")
    fm_match = _FRONTMATTER_RE.search(text)
    if fm_match is None:
        return None
    lines = fm_match.group(1).split("\n")
    start_idx: int | None = None
    for i, line in enumerate(lines):
        if _REFLECT_POST_KEY_RE.match(line):
            start_idx = i
            break
    if start_idx is None:
        return None
    end_idx = start_idx + 1
    while end_idx < len(lines) and lines[end_idx].startswith((" ", "\t")):
        end_idx += 1
    block = "\n".join(lines[start_idx:end_idx])
    try:
        parsed = yaml.safe_load(block)
    except yaml.YAMLError:
        return None
    if isinstance(parsed, dict):
        value = parsed.get("reflect_post")
        return value if isinstance(value, dict) else None
    return None


class ReflectRunner:
    """Thin orchestrator: derive -> preflight -> launch -> parse -> write-back.

    Constructed from a resolved ``ReflectConfig``. ``run()`` is the single
    entrypoint. It never classifies deviations or applies a tier rubric -- all
    verdict logic is delegated to ``contract.derive_verdict`` (NFR-1 thinness).
    """

    def __init__(self, config: ReflectConfig) -> None:
        self.config = config

    # -- prompt + dry-run preview -----------------------------------------

    def _build_prompt(self) -> str:
        """Compose the §8 ``/sc:reflect`` stdin prompt (real reflect flags only)."""
        config = self.config
        parts = ["/sc:reflect", "--mode", "post"]
        # FR-9: --no-promote is the hard default; dropped only on --promote.
        if not config.promote:
            parts.append("--no-promote")
        parts += ["--diff", f"{config.base}..HEAD"]
        parts += ["--tasklist", str(config.tasklist_path)]
        if config.spec_path is not None:
            parts += ["--spec", str(config.spec_path)]
        parts += ["--depth", config.depth]
        if config.executor_model:
            parts += ["--executor-model", config.executor_model]
        parts += ["--output", str(config.output_dir)]
        return " ".join(parts)

    def _claude_argv_preview(self) -> str:
        """Render the ``claude`` argv for dry-run WITHOUT constructing ClaudeProcess.

        F6: byte-matches ``ClaudeProcess.build_command()`` (pipeline/process.py)
        flag set AND order so ``--print-command`` shows the argv that actually
        runs. The FR-12 dry-run-never-constructs guarantee forbids building a real
        ``ClaudeProcess`` here (enforced by ``test_dry_run_never_launches``), so
        the order is mirrored literally: ``--print --verbose
        --dangerously-skip-permissions --no-session-persistence --tools default
        --max-turns <N> --output-format stream-json [--model <M>]`` (``--model``
        appended last, only when set, matching the builder's conditional).
        """
        config = self.config
        argv = (
            "claude --print --verbose --dangerously-skip-permissions "
            "--no-session-persistence --tools default "
            f"--max-turns {config.max_turns} --output-format stream-json"
        )
        if config.model:
            argv += f" --model {config.model}"
        return argv

    # -- orchestration ----------------------------------------------------

    def run(self) -> ReflectResult:
        """Execute the wrapper run and return the derived ``ReflectResult``."""
        config = self.config
        expected_tier = 2 if config.depth in {"standard", "deep"} else 1

        # (1) Preflight (no ClaudeProcess construction -- FR-12 safe).
        blocker = preflight(config)

        # (2) Build the slash prompt.
        prompt = self._build_prompt()

        # (3) Dry-run / print-command: print and return WITHOUT launching.
        #     ClaudeProcess is never constructed in this path (FR-12).
        if config.print_command or config.dry_run:
            print(self._claude_argv_preview())
            print(prompt)
            return ReflectResult(
                verdict=Verdict.PASS,
                status=None,
                tier_reached=None,
                reason="dry-run",
                report_path=None,
                contract_path=None,
                deviations={},
                child_exit_code=None,
                write_status="dry-run",
            )

        # Past the dry-run gate: now safe to touch the exact child env.
        env_alias_count = count_model_aliases(_child_env())

        # Preflight blocker -> blocked verdict + sidecar.
        if blocker is not None:
            result = ReflectResult(
                verdict=Verdict.BLOCKED,
                status=None,
                tier_reached=None,
                reason=blocker,
                report_path=None,
                contract_path=None,
                deviations={},
                child_exit_code=None,
                write_status="not-attempted",
            )
            write_sidecar(
                config.output_dir,
                result,
                env_alias_count=env_alias_count,
                write_status="not-attempted",
            )
            return result

        # (3.5) Resume short-circuit (G2): skip a still-clean HEAD.
        if config.resume:
            prior = _read_existing_reflect_post(config.tasklist_path)
            if (
                isinstance(prior, dict)
                and prior.get("head") == config.head
                and prior.get("verdict") == "pass"
            ):
                result = ReflectResult(
                    verdict=Verdict.PASS,
                    status=prior.get("status"),
                    tier_reached=prior.get("tier_reached"),
                    reason="resume-clean-head",
                    report_path=prior.get("report"),
                    contract_path=prior.get("contract"),
                    deviations=prior.get("deviations") or {},
                    child_exit_code=None,
                    write_status="resume-skipped-clean-head",
                )
                write_sidecar(
                    config.output_dir,
                    result,
                    env_alias_count=env_alias_count,
                    write_status="resume-skipped-clean-head",
                )
                return result

        # (4) Launch reflect as a top-level claude --print subprocess (FR-1).
        config.output_dir.mkdir(parents=True, exist_ok=True)
        proc = ClaudeProcess(
            prompt=prompt,
            output_file=config.output_dir / "reflect-stdout.json",
            error_file=config.output_dir / "reflect-stderr.log",
            model=config.model,
            timeout_seconds=config.timeout_seconds,
            max_turns=config.max_turns,  # G1: explicit, never the primitive's 100.
            output_format="stream-json",
            env_vars=None,  # FR-10: bare real-env overlay (no custom scrub).
        )
        proc.start()
        rc = proc.wait()

        # (5) Parse the pinned contract and derive the verdict.
        contract = parse_contract(config.contract_path)
        result = derive_verdict(
            contract,
            expected_tier=expected_tier,
            allow_single_vendor=config.allow_single_vendor,
            child_rc=rc,
        )
        result.contract_path = str(config.contract_path)

        # (6) Atomic race-safe write-back + always-write sidecar.
        reviewed_at = datetime.now(timezone.utc).isoformat()
        write_status = write_reflect_post(
            config.tasklist_path,
            result,
            head=config.head,
            reviewed_at=reviewed_at,
        )
        result.write_status = write_status
        # FR-6: an unwritable/stale frontmatter must fail-closed (non-zero exit).
        if write_status != "written" and result.verdict is Verdict.PASS:
            result.verdict = Verdict.BLOCKED
            result.reason = write_status or "frontmatter-unwritable"
        write_sidecar(
            config.output_dir,
            result,
            env_alias_count=env_alias_count,
            write_status=write_status,
        )
        return result
