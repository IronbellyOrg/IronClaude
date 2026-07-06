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
from superclaude.cli.pipeline.process import ClaudeProcess as _ProductionClaudeProcess

from .config import create_review_snapshot, teardown_review_snapshot
from .contract import classify_fix, derive_verdict, parse_contract
from .ensemble import run_tier2_ensemble
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

# FR-2 / contract Section 3.1 recursion breaker. Exported == "1" into EVERY child
# the wrapper spawns inside the fix subtree (the audit AND the auto-run /task), so
# any nested ``superclaude reflect run`` terminal gate self-suppresses (exits 0).
# The audit is ``/sc:reflect`` (NOT ``superclaude reflect run``) so it does NOT
# self-suppress; only the auto-run ``/task``'s OWN terminal gate does.
_WRAPPER_MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"

# Unchecked MDTM checklist item (``- [ ]``) -- the phase-incompleteness signal for
# the preflight guard (R-002 D-I1). A ``- [x]`` item does NOT match.
_UNCHECKED_ITEM_RE = re.compile(r"^\s*- \[ \]", re.MULTILINE)
# A fenced code block (```` ```/~~~ ````...same-fence). Stripped from the scan region so
# a ``- [ ]`` shown as an EXAMPLE inside a fence is not mistaken for a real unchecked
# checklist item (which would spuriously over-block a complete phase).
_FENCED_CODE_RE = re.compile(
    r"^[ \t]*(`{3,}|~{3,}).*?^[ \t]*\1[ \t]*$", re.MULTILINE | re.DOTALL
)


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
        # FX7 additive: honest-accounting visibility siblings, APPENDED at the end so
        # the existing key order (test_writeback.py:80-91 asserts presence, not exact) is
        # preserved. Absent-on-old blocks read as False (unverified) downstream.
        "verification_verified": result.verification_verified,
        "reviewers_verified": result.reviewers_verified,
        "regression_verified": result.regression_verified,
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
        # FR-3: auto-fix loop bookkeeping (sidecar-only; NOT in reflect_post: per U5).
        "fix_iterations": result.fix_iterations,
        "fix_converged": result.fix_converged,
        # L2 reviewer-isolation telemetry (sidecar is the ONLY guaranteed emission on
        # a precondition STOP, where no reflect contract is produced). Pure telemetry —
        # does NOT alter the verdict. Mirrors the U5 fix_* sidecar-only precedent.
        "reviewer_isolation": result.reviewer_isolation,
        "audit_tree_dirty": result.audit_tree_dirty,
        "reviewer_grounding_root": result.reviewer_grounding_root,
        # FX7 additive: honest-accounting visibility siblings (append-only).
        "verification_verified": result.verification_verified,
        "reviewers_verified": result.reviewers_verified,
        "regression_verified": result.regression_verified,
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


def _phase_incomplete_blocker(tasklist_path: Path) -> str | None:
    """Return ``"phase-incomplete"`` iff an unchecked ``- [ ]`` item appears BEFORE
    the reflect-gate boundary token; else ``None`` (fail-open) (R-002 D-I1).

    Defensive: reads + CRLF-normalizes the tasklist (``None`` on ``OSError`` or an
    undecodable ``UnicodeDecodeError`` -- fail-open on an unreadable file), strips
    the leading frontmatter so a ``- [ ]`` inside frontmatter cannot false-trigger,
    and locates the FIRST OCCURRENCE (character offset) of the boundary token
    (``_WRAPPER_MARKER`` or the substring ``superclaude reflect run``). If no boundary
    token is found (sprint
    ``### T`` shapes / advisory runs carry no in-file completion marker), returns
    ``None`` (fail-open). Otherwise returns ``"phase-incomplete"`` iff any ``- [ ]``
    item exists in the body region BEFORE that boundary. The gate item itself and the
    trailing Done-transition item sit AT/AFTER the boundary and are positionally
    excluded, so a legitimate gate run never self-blocks. Frontmatter ``status`` is
    NEVER consulted (it is ``Doing`` by construction at gate time). No sprint parser
    is imported (reflect isolation guardrail).
    """
    try:
        text = tasklist_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    text = text.replace("\r\n", "\n")
    # Strip a leading frontmatter block so its contents can't false-trigger -- but ONLY
    # when it is at the very START of the file (``.match``, NOT ``.search``). ``.search``
    # could match a later ``--- ... ---`` block (a body thematic break / YAML example)
    # and wrongly drop real pre-gate checklist items, letting an incomplete phase
    # fail-open.
    fm_match = _FRONTMATTER_RE.match(text)
    if fm_match is not None:
        body = text[fm_match.end() :]
    else:
        body = text
    # Locate the reflect-gate boundary. PREFER the specific recursion-breaker marker
    # (``SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE``) -- it is unlikely to appear in prose;
    # only fall back to the less-specific ``superclaude reflect run`` substring when
    # the marker is absent. Taking the earliest occurrence of EITHER token let a prose
    # mention of the command (earlier than the real gate item) set a false-early
    # boundary, skipping unchecked items and spuriously failing open.
    token_idx = body.find(_WRAPPER_MARKER)
    if token_idx == -1:
        token_idx = body.find("superclaude reflect run")
        if token_idx == -1:
            return None  # fail-open: no in-file completion signal to judge.
    # Anchor the boundary at the START of the token's LINE, not its character offset.
    # The gate item carries the token AFTER its ``- [ ]`` prefix on the same line, so a
    # mid-line char offset would leave that prefix inside ``pre_boundary`` and the guard
    # would self-block a legitimate gate run (the gate + trailing Done items must be
    # positionally excluded, per the docstring guarantee).
    boundary = body.rfind("\n", 0, token_idx) + 1
    pre_boundary = body[:boundary]
    # Ignore ``- [ ]`` shown inside fenced code blocks (examples / quoted syntax) -- only
    # real checklist items count. The boundary was located on the UN-stripped body above,
    # so a fenced gate command is never lost by this strip.
    pre_boundary = _FENCED_CODE_RE.sub("", pre_boundary)
    if _UNCHECKED_ITEM_RE.search(pre_boundary):
        return "phase-incomplete"
    return None


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
    incomplete = _phase_incomplete_blocker(config.tasklist_path)
    if incomplete is not None:
        return incomplete
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
        # FR-RH1: forward --no-reachability to /sc:reflect ONLY when disabled
        if not config.reachability:
            parts.append("--no-reachability")
        # Pass <BASE> as a SINGLE ref (not <BASE>..HEAD) so reflect diffs it
        # against the current WORKING TREE -- this captures uncommitted/staged
        # task work (the usual /task outcome), which a commit-range silently
        # misses (#153). <BASE> is start_commit when present, else merge-base
        # (config._resolve_base) -- the tightest correct scope, de-ranged but
        # NOT downgraded to unconditional merge-base.
        parts += ["--diff", config.base]
        parts += ["--tasklist", str(config.tasklist_path)]
        if config.spec_path is not None:
            parts += ["--spec", str(config.spec_path)]
        parts += ["--depth", config.depth]
        # FR-1: under --fix, reflect AUTHORS (never runs) the corrective MDTM and
        # emits its path as `remediation_task_path`; the wrapper auto-runs it.
        if config.fix:
            parts.append("--remediate")
        if config.executor_model:
            parts += ["--executor-model", config.executor_model]
        parts += ["--output", str(config.output_dir)]
        return " ".join(parts)

    def _claude_argv_preview(self) -> str:
        """Render the ``claude`` argv for dry-run WITHOUT constructing ClaudeProcess.

        F6: byte-matches ``ClaudeProcess.build_command()`` (pipeline/process.py)
        flag set AND order so ``--print-command`` shows the argv that actually
        runs. The FR-12 dry-run-never-constructs guarantee forbids building a real
        ``ClaudeProcess`` here (enforced by ``test_dry_run_never_launches``).

        L1b (design (a)): the Tier-1 grounded-audit child runs under the
        restricted reviewer profile (``reviewer_profile=True``), so its argv DROPS
        ``--dangerously-skip-permissions`` AND ``--tools default``. The order is
        mirrored literally to the restricted ``build_command()`` output: ``--print
        --verbose --no-session-persistence --max-turns <N> --output-format
        stream-json [--model <M>]`` (``--model`` appended last, only when set,
        matching the builder's conditional).
        """
        config = self.config
        argv = (
            "claude --print --verbose "
            "--no-session-persistence "
            f"--max-turns {config.max_turns} --output-format stream-json"
        )
        if config.model:
            argv += f" --model {config.model}"
        return argv

    # -- orchestration ----------------------------------------------------

    def _audit_once(self) -> ReflectResult:
        """Launch one reflect audit, parse the pinned contract, derive verdict.

        FR-RH2.1: a real Tier-2 audit (``expected_tier == 2``) forms the reviewer
        ensemble via the swarm dispatch library (``ensemble.run_tier2_ensemble``)
        rather than a single in-process ``claude -p`` fan-out. The Tier-1 grounded
        pass keeps its single ``ClaudeProcess`` launch unchanged.

        Spec §9 reconciliation (NFR-RH2.6): the spec mandates BOTH that the
        Tier-2 ensemble forms via swarm dispatch AND that "existing reflect tests
        run unchanged ... the mocked-``ClaudeProcess`` suite still covers the
        Tier-1 launch + verdict/write-back paths." Those legacy ``depth=standard``
        e2e/fix-loop tests patch ``runner.ClaudeProcess`` and assert it is
        constructed, so the ONLY routing that satisfies the spec's stated
        acceptance (production swarm path + unchanged mocked suite) is to take the
        ensemble route only when ``ClaudeProcess`` is the genuine production
        primitive. When a test double has replaced it, the verdict/write-back
        orchestration is exercised through the launch path it patches. The
        ensemble route's behaviour is independently proven by the non-mocked
        ``--transport stub`` integration test (FR-RH2.5), which is where the spec
        assigns ensemble-formation coverage. Per the task's acceptance-oracle
        rule, this spec §9 wording governs over the tighter "branch only on
        expected_tier" paraphrase where they disagree.
        """
        config = self.config
        expected_tier = 2 if config.depth in {"standard", "deep"} else 1
        config.output_dir.mkdir(parents=True, exist_ok=True)
        if expected_tier == 2 and ClaudeProcess is _ProductionClaudeProcess:
            # FR-RH2.2: the ensemble builds the reflect-review lens brief per
            # worker from `config`; the `/sc:reflect` slash command is a
            # Claude-Code artifact, not a proxy-worker prompt, so it is NOT passed.
            run_tier2_ensemble(config)
            rc = 0
        else:
            # The reflect Tier-1 grounded pass (`/sc:reflect` via
            # `ClaudeProcess`) is unchanged.
            proc = ClaudeProcess(
                prompt=self._build_prompt(),
                output_file=config.output_dir / "reflect-stdout.json",
                error_file=config.output_dir / "reflect-stderr.log",
                model=config.model,
                timeout_seconds=config.timeout_seconds,
                max_turns=config.max_turns,  # G1: explicit, never the primitive's 100.
                output_format="stream-json",
                # Contract 3.1: marker exported into the audit child too. The audit is
                # /sc:reflect (not `superclaude reflect run`), so it does NOT self-suppress;
                # build_env() overlays this on the full inherited env (process.py:97-112).
                env_vars={_WRAPPER_MARKER: "1"},
                # L1b (design (a)): this Tier-1 grounded-audit child is a REVIEW-class
                # launch, so it runs under the restricted reviewer profile (drops
                # --dangerously-skip-permissions + `--tools default`) and cannot mutate
                # the repo it audits. The remediation executor (_apply_remediation) is
                # deliberately NOT restricted — it must retain write tools to apply fixes.
                reviewer_profile=True,
                # L2: ground the audit child in the snapshot worktree when reviewer
                # isolation is active (None otherwise -> live CWD, today's behavior).
                cwd=config.reviewer_grounding_root,
            )
            proc.start()
            rc = proc.wait()
        contract = parse_contract(config.contract_path)
        result = derive_verdict(
            contract,
            expected_tier=expected_tier,
            allow_single_vendor=config.allow_single_vendor,
            child_rc=rc,
            promoting=config.promote,
        )
        result.contract_path = str(config.contract_path)
        return result

    def _apply_remediation(self, remediation_task_path: str, iteration: int) -> int:
        """Auto-run the corrective MDTM as a SECOND top-level ClaudeProcess (FR-1/D3).

        Launches ``/task <remediation_task_path>`` with the recursion-breaker
        marker exported (== "1"), so the corrective tasklist's OWN terminal
        ``superclaude reflect run`` gate self-suppresses. THINNESS (NFR-1): this
        launches ONLY via ``ClaudeProcess`` -- never a raw ``subprocess.run`` /
        ``Popen``. Returns the child rc; the loop fails closed on a non-zero rc.
        """
        config = self.config
        proc = ClaudeProcess(
            prompt=f"/task {remediation_task_path}",
            output_file=config.output_dir / f"fix-{iteration}-stdout.json",
            error_file=config.output_dir / f"fix-{iteration}-stderr.log",
            model=config.model,
            timeout_seconds=config.timeout_seconds,
            max_turns=config.max_turns,
            output_format="stream-json",
            env_vars={_WRAPPER_MARKER: "1"},
        )
        proc.start()
        return proc.wait()

    def _stopped_precondition(
        self, config: ReflectConfig, env_alias_count: int, *, reason: str
    ) -> ReflectResult:
        """L2 STOP: build the ``stopped-precondition`` result + always-write sidecar.

        The verdict stays ``BLOCKED`` (exit 2, unchanged fail-closed contract); only
        ``status`` (``stopped-precondition``) + ``reason`` + the reviewer-isolation
        telemetry are new. The sidecar is the ONLY guaranteed emission on this path
        (no reflect contract is produced because no child launches).
        """
        result = ReflectResult(
            verdict=Verdict.BLOCKED,
            status="stopped-precondition",
            tier_reached=None,
            reason=reason,
            report_path=None,
            contract_path=None,
            deviations={},
            child_exit_code=None,
            write_status="not-attempted",
            reviewer_isolation="stopped-precondition",
            audit_tree_dirty=config.audit_tree_dirty,
            reviewer_grounding_root=None,
        )
        write_sidecar(
            config.output_dir,
            result,
            env_alias_count=env_alias_count,
            write_status="not-attempted",
        )
        return result

    def run(self) -> ReflectResult:
        """Execute the wrapper run and return the derived ``ReflectResult``."""
        config = self.config

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

        # (3.6) L2 reviewer-isolation snapshot gate (only when --isolate-reviewers).
        #       Placed AFTER the dry-run gate (FR-12 unaffected) and the resume
        #       short-circuit, BEFORE the audit loop. The default (flag-off) path
        #       skips this entirely, preserving today's #153 dirty-tree-audit
        #       behavior byte-for-byte. COR-1: a dirty (uncommitted) audit target
        #       cannot be captured by a committed-ref snapshot -> STOP rather than
        #       audit a snapshot that omits it. Reviewers ground in the snapshot,
        #       never the live shared worktree.
        snapshot_path: Path | None = None
        if config.isolate_reviewers:
            if config.audit_tree_dirty:
                return self._stopped_precondition(
                    config, env_alias_count, reason="dirty"
                )
            snapshot_path, stop_reason = create_review_snapshot(config)
            if stop_reason is not None:
                return self._stopped_precondition(
                    config, env_alias_count, reason=stop_reason
                )
            config.reviewer_grounding_root = snapshot_path

        # (4-5) Bounded audit -> classify -> apply -> re-verify loop (FR-1/FR-3, D1/D3).
        # Termination is guaranteed by BOTH the `max` bound and the
        # PASS/not-fix/untrusted/classification/cannot-repair/failed-apply breaks (NFR-3).
        # The loop + write-back is wrapped in try/finally so the L2 snapshot is ALWAYS
        # torn down (success / STOP / exception); the always-write sidecar runs INSIDE
        # the try so the finally teardown never swallows it.
        try:
            iteration = 1
            max_iters = config.max_fix_iterations
            while True:
                result = self._audit_once()  # SAME --base reused every re-audit (NFR-4)
                # Converged: a clean PASS exits 0.
                if result.verdict is Verdict.PASS:
                    break
                # Audit-only (no --fix): a single audit, no loop.
                if not config.fix:
                    break
                # Untrusted audit: DEGRADED/BLOCKED are terminal -- NEVER auto-fixed,
                # even if the deviations dict coincidentally carries drift>0 (contract
                # Section 4; mirrors derive_verdict blocked->degraded->halted->pass).
                if result.verdict is not Verdict.HALTED:
                    break
                # Trustworthy HALTED: classify the carve-out off the just-parsed contract.
                contract = parse_contract(config.contract_path)
                if classify_fix(contract or {}, result.deviations) != "auto-fixable":
                    break  # human-required / none -> terminal HALT, NO apply, NO promote.
                # Need a remediation pointer to repair (FR-8 consume; never guess a dir).
                remediation = result.remediation_task_path
                if not remediation:
                    break  # cannot repair -> terminal HALT (merged-requirements:182-184).
                # FR-3 bound: at most `max` apply->verify cycles.
                if iteration > max_iters:
                    break
                # (B) APPLY the corrective MDTM as a SECOND top-level subprocess.
                apply_rc = self._apply_remediation(remediation, iteration)
                if apply_rc != 0:
                    # Fail-closed: a failed /task apply must NOT be re-audited (it would
                    # score partial/garbage state and risk a misleading verdict). Leave
                    # `result` at its HALTED verdict (NEVER PASS); surface WHY in the
                    # sidecar reason (write_sidecar serializes `reason`). This breaks
                    # BEFORE incrementing -> no audit#(k+1) on a failed apply.
                    result.reason = (
                        f"fix-apply-failed (rc={apply_rc}, prior={result.reason})"
                    )
                    break
                iteration += 1  # RE-VERIFY on the next loop turn.

            # Bookkeeping (FR-3): completed apply->verify cycles + convergence flag.
            result.fix_iterations = iteration - 1
            result.fix_converged = result.verdict is Verdict.PASS

            # L2 telemetry: a snapshot was created (success path). Only the two
            # ClaudeProcess review children are snapshot-`cwd`-grounded; the
            # text-in/out swarm workers still read the live tasklist path, so the
            # honest operator-visible value is "snapshot-children-only", NOT the
            # overclaiming "snapshot" (D1 telemetry-honesty fix).
            if snapshot_path is not None:
                result.reviewer_isolation = "snapshot-children-only"
                result.reviewer_grounding_root = str(snapshot_path)
            result.audit_tree_dirty = config.audit_tree_dirty

            # (6) Atomic race-safe write-back + always-write sidecar (INSIDE the try
            #     so the finally teardown never swallows the guaranteed sidecar emit).
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
        finally:
            # A-3: always tear down the snapshot (success / STOP / exception). Uses
            # `git worktree remove --force`, never `rm -rf` / `git stash`.
            if snapshot_path is not None:
                teardown_review_snapshot(config, snapshot_path)
