"""R-19 assertion engine (harness §1). FLAGS written by hand from reconcile §X-3."""

from __future__ import annotations

import ast
import json
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from tests.troubleshoot._procedures import (
    _MIDNIGHT,
    ENUM_TOKEN,
    _section,
    producer_rows,
    table_row_by_index,
    table_rows,
    timestamp_ok,
)

_ISO = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
_TS_LINE = re.compile(r"(?im)^.*\b(Timestamp|Date|pushed_at)\b.*$")
_HEADLINE_RC = re.compile(r"(?im)^\**Root cause\**:\s*(.+)$")
_CONF = re.compile(r"(?im)^\**confidence\**:\s*\**(\d+\.\d+)")
_CONF_KEY = re.compile(r"(?im)^\**confidence\**:\s*\S+")
_CAL = re.compile(r"(?i)\bcalibrated\b[^0-9\n]{0,40}(\d\.\d{1,2})")
_A5_PROSE = re.compile(
    r"(?i)evidence[_ ]class\**`?\s*[:=]?\s*`?\**\s*(none|source_static|doc_static)\b"
)
_FILE_SPLIT = re.compile(r"(?m)^--- file: (\S+) ---\n")
_JOB_LOG = re.compile(r"job-[^/]+\.log")
_C6_THRESH = re.compile(
    r"(?i)\b(above|below|over|under|more than|less than|at least|at most|>=?|<=?)\s*\d+"
    r"|\b\d+\s+(layers|messages|bytes|rows|items|retries|connections|files)\b"
)
_A5_ADV = re.compile(r"adversarial_invoked:\s*false|Adversarial:\s*not invoked")
CONTRACT_ENUM = {
    "pass",
    "blocked",
    "advisory",
    "not_applicable",
    "blocked-on-authorization",
}
_A8_PREFIX = "UNDETERMINED — CI verdict unobserved"
_STATIC_EV = {"source_static", "doc_static", "none"}
_DYNAMIC_CLAIM = {"runtime_behavior", "environment_dependent"}


@dataclass(frozen=True)
class Flag:
    id: str
    flag: str
    severity: str
    trigger: str


FLAGS: tuple[Flag, ...] = (
    Flag(
        "A1",
        "deduced_headline",
        "partial",
        "definite enum token in Summary/Diagnosis and (max calibrated < 0.50 or token in Grounding Gaps with unobserved/deduced/pending or token absent from captured failing-run output with run/arm provenance in observation_paths; generated reports, cards, producer tables and definitions never count as observations)",
    ),
    Flag(
        "A2",
        "instrumentation_without_falsifier",
        "partial",
        "diff touches a collector or invocation site and the report omits its linked measurement row, preregistered outcomes or pending reason, or omits the required Next Steps form `The report stays \\`partial\\` until <row>=<value>`; enabling tasks require linked row IDs and operational verification, not invented causal values; optional rows require informational publication but never a status prerequisite",
    ),
    Flag(
        "A3",
        "timestamp_invalid",
        "drop-line",
        "Timestamp/Date/pushed_at later than artifact mtime + 5 min or equal to T00:00:00Z",
    ),
    Flag(
        "A4",
        "verdict_not_in_contract",
        "partial",
        "pipeline_hardening_verdict not in {pass, blocked, advisory, not_applicable, blocked-on-authorization}",
    ),
    Flag(
        "A5",
        "consensus_on_unobserved",
        "partial",
        "candidate-fixes.md says consensus and adversarial_invoked is false and a card with evidence_class in {source_static, doc_static, none} makes a dynamic claim; or the calibration file states the evidence class is none/static",
    ),
    Flag(
        "A6",
        "reference_value_not_literal",
        "FAIL",
        "Reference-context value is not one literal: first exempt exact `n/a` only when that probe has `first_instrumented_run=true`; otherwise accept one numeric/boolean/null literal or one quoted string, and reject conditional prose, unquoted alternatives/lists, blank values and later-run `n/a`. Slashes/commas inside a quoted literal (e.g. a path) are data, not alternatives",
    ),
    Flag(
        "A7",
        "run_site_unresolved",
        "FAIL",
        "RUN-SITE is pending-producers at finalize while producers.md has at least one producer row",
    ),
    Flag(
        "A8",
        "ci_verdict_unobserved",
        "blocked",
        "OBSERVE-VIA is artifact-file and the captured job log is missing, AND the locus identifies the failing arm as a CI job whose harness result marker is absent at finalize",
    ),
    Flag(
        "A9",
        "probe_suspect",
        "probe-suspect",
        "A literal Reference-context value differs from an actually captured reference-arm observation, including on the first run; failing-arm output is not a reference observation. Skip comparison for evidenced first-run n/a or an unobserved reference cell; neither proves a control",
    ),
    Flag(
        "A10",
        "capability_block_unproven",
        "partial",
        "capability-verdict is blocked without an Emitter search block establishing usable-capture-routes: 0 with searched channels, truthful raw emitters-found/already-read-files counts and candidate exclusions; a viable permitted-site route must capture the actual datum, not merely name a sink or annotate expected data. Refused/unknown permission is separate from capability",
    ),
    Flag(
        "C1",
        "headline_definite_low_confidence",
        "verdict",
        "headline enum token and calibrated < 0.50",
    ),
    Flag(
        "C2",
        "unproven_exclusion:<token>",
        "dim",
        "card excludes an enum without a file:line for that enum's exit statement",
    ),
    Flag(
        "C3",
        "control_unproven",
        "dim",
        "control arm cited without `CONTROL-PROOF: yes: <file:line>`",
    ),
    Flag("C3b", "locus_unknown", "dim", "runs-in is unknown"),
    Flag(
        "C4",
        "no_prereg_falsifier",
        "dim",
        "measurement row missing either preregistered true/false prediction or its outcome mapping (equal predictions and explicitly justified unknown are valid, not proof); enabling task missing its linked measurement IDs or operational verification/rollback",
    ),
    Flag(
        "C5",
        "timestamp_invalid",
        "drop-line",
        "Timestamp later than card_mtime + 5 min or equal to T00:00:00Z",
    ),
    Flag(
        "C6",
        "bracket_unproven",
        "cap",
        "numeric threshold or bracket asserted in the headline without a bracket= line in bracket.md",
    ),
    Flag(
        "C7",
        "uncited",
        "cap",
        "card names an environment property without citing a 2x2 row",
    ),
    Flag(
        "C8",
        "behaviour-cite: missing",
        "cap",
        "behaviour-definition: row N missing or the row's Status is empty",
    ),
)
FLAG_BY_ID: dict[str, Flag] = {f.id: f for f in FLAGS}
VALIDATOR_IDS = ("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10")
CALIBRATOR_IDS = ("C1", "C2", "C3", "C3b", "C4", "C5", "C6", "C7", "C8")


@dataclass
class ValidatorInputs:
    report: str
    calibration_texts: list[str] = field(default_factory=list)
    diff_text: str = ""
    artifact_mtimes: dict[str, datetime] = field(default_factory=dict)
    producers_text: str = ""
    tasklist_text: str = ""
    locus_text: str = ""
    observation_text: str = ""
    candidate_fixes_text: str = ""
    card_texts: list[str] = field(default_factory=list)
    files_present: tuple[str, ...] | None = None
    # Caller-selected raw failing-run captures, never generated analysis.
    # None is omitted; [] is a verified empty corpus.
    artifact_texts: list[str] | None = None
    # Probe ID -> {"value": bool | None, "provenance": "file:line"}.
    first_instrumented_run: dict[str, dict[str, object]] = field(default_factory=dict)


@dataclass
class CalibratorInputs:
    card: str
    calibrated: float | None = None
    card_mtime: datetime | None = None
    locus_text: str = ""
    bracket_text: str | None = None
    behaviour_text: str = ""
    tasklist_text: str = ""


@dataclass
class CalibratorResult:
    flags: set[str]
    ids: set[str]
    dims: dict[str, float]
    cap: float | None
    verdict: str | None


@dataclass
class ValidatorResult:
    flags: set[str]
    ids: set[str]
    status: str | None
    dropped_lines: list[str]
    suspect_probes: list[str]
    headline_prefix: str | None


@dataclass
class Fixture:
    path: Path
    meta: dict[str, object]
    files: dict[str, str]


def _card_fm(card: str, key: str) -> str | None:
    m = re.search(rf"(?im)^\**{re.escape(key)}\**:\s*`?([\w-]+)`?", card)
    return m.group(1) if m else None


def _headline(report: str) -> str:
    m = re.search(r"(?im)^root_cause_summary:\s*(.+)$", report)
    if m:
        return m.group(1)
    m = _HEADLINE_RC.search(report)
    if m:
        return m.group(1)
    summary = _section(report, "Summary").strip()
    if summary:
        return summary
    for line in _section(report, "Diagnosis").splitlines():
        if line.strip():
            return line.strip()
    return ""


def _calibrated(texts: list[str]) -> float | None:
    best: float | None = None
    for t in texts:
        for m in _CAL.finditer(t):
            v = float(m.group(1))
            best = v if best is None else max(best, v)
    return best


def _confidence(report: str) -> float | None:
    m = _CONF.search(report)
    if m:
        return float(m.group(1))
    if _CONF_KEY.search(report):
        return 0.0
    return None


def _ts_violations(text: str, mtime: datetime | None) -> list[str]:
    out: list[str] = []
    for m in _TS_LINE.finditer(text or ""):
        line = m.group(0)
        iso = _ISO.search(line)
        if _MIDNIGHT.search(line):
            out.append(line)
            continue
        if iso is None or mtime is None:
            continue
        if not timestamp_ok(iso.group(0), mtime):
            out.append(line)
    return out


def _parse_iso(raw: object) -> datetime | None:
    if not raw:
        return None
    return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).astimezone(
        timezone.utc
    )


def _parse_list(raw: str) -> list[str]:
    inner = raw.strip()
    if inner.startswith("["):
        inner = inner[1:]
    if inner.endswith("]"):
        inner = inner[:-1]
    if not inner.strip():
        return []
    return [p.strip().strip("'\"") for p in inner.split(",") if p.strip().strip("'\"")]


def _parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    block = text[4:end]
    rest = text[end + 4 :]
    if rest.startswith("\n"):
        rest = rest[1:]
    meta: dict[str, object] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if val.startswith("["):
            meta[key] = _parse_list(val)
        elif key in {"calibrated"}:
            meta[key] = float(val)
        else:
            meta[key] = val
    return meta, rest


def _a5_unobserved(texts: list[str]) -> bool:
    for t in texts:
        ev = _card_fm(t, "evidence_class")
        if ev is None:
            m = _A5_PROSE.search(t)
            ev = m.group(1).lower() if m else None
        if ev not in _STATIC_EV:
            continue
        claim = _card_fm(t, "claim_class") or "runtime_behavior"
        if claim in _DYNAMIC_CLAIM:
            return True
    return False


def _c2_tokens(card: str) -> set[str]:
    bad: set[str] = set()
    for line in card.splitlines():
        if not re.search(r"(?i)\bexcluded\b", line):
            continue
        for tok in ENUM_TOKEN.findall(line):
            ok = re.search(
                rf"`{re.escape(tok)}`[^\n]*exit statement[^\n]*\b[\w./-]+:\d+",
                card,
            )
            if not ok:
                bad.add(tok)
    return bad


def _pred_a1(inp: ValidatorInputs) -> bool:
    toks = ENUM_TOKEN.findall(_headline(inp.report))
    if not toks:
        return False
    cal = _calibrated(inp.calibration_texts)
    conf = cal if cal is not None else _confidence(inp.report)
    gaps = _section(inp.report, "Grounding Gaps")
    artifacts = inp.artifact_texts or []
    corpus_supplied = inp.artifact_texts is not None
    if conf is not None and conf < 0.5:
        return True
    for t in toks:
        if re.search(rf"`{re.escape(t)}`[^\n]*\b(unobserved|deduced|pending)\b", gaps):
            return True
        if corpus_supplied and not any(
            re.search(rf"(?<![\w-]){re.escape(t)}(?![\w-])", a) for a in artifacts
        ):
            return True
    return False


def _pred_a2(inp: ValidatorInputs) -> bool:
    return bool(
        re.search(r"(?m)^\+.*\b(echo|printf|print|log|tee|write|>>)\b", inp.diff_text)
        and not re.search(r"The report stays `partial` until \S+=\S+", inp.report)
    )


def _pred_a3(inp: ValidatorInputs) -> list[str]:
    dropped = _ts_violations(inp.report, inp.artifact_mtimes.get("REPORT.md"))
    cal_m = inp.artifact_mtimes.get("calibration")
    for t in inp.calibration_texts:
        dropped.extend(_ts_violations(t, cal_m))
    return dropped


def _pred_a4(inp: ValidatorInputs) -> bool:
    body = _section(inp.report, "Pipeline Hardening Closure") or inp.report
    m = re.search(
        r"(?i)(?:pipeline_hardening_verdict|\bVerdict)\**:\s*\**([a-z_-]+)",
        body,
    )
    return bool(m and m.group(1).lower() not in CONTRACT_ENUM)


def _pred_a5(inp: ValidatorInputs) -> bool:
    return bool(
        re.search(r"\bconsensus\b", inp.candidate_fixes_text)
        and _A5_ADV.search(inp.report)
        and _a5_unobserved(inp.card_texts + inp.calibration_texts)
    )


def _pred_a6(inp: ValidatorInputs) -> bool:
    for text in (inp.report, inp.observation_text, inp.tasklist_text):
        probe = ""
        for line in text.splitlines():
            identity = re.fullmatch(r"(?:#+ Discriminator|Probe):[ \t]*(\S+)", line)
            if identity:
                probe = identity.group(1)
            elif line.startswith("#"):
                probe = ""
            if not line.startswith("Reference-context value:"):
                continue
            val = line.partition(":")[2].strip()
            first_run = inp.first_instrumented_run.get(probe, {})
            if (
                val == "n/a"
                and first_run.get("value") is True
                and isinstance(first_run.get("provenance"), str)
                and first_run["provenance"].strip()
            ):
                continue
            if val in {"true", "false", "null"}:
                continue
            try:
                literal = ast.literal_eval(val)
            except (ValueError, SyntaxError):
                return True
            if type(literal) in {int, float}:
                if isinstance(literal, float) and not math.isfinite(literal):
                    return True
            elif not (
                isinstance(literal, str)
                and re.fullmatch(r"""(?:'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")""", val)
            ):
                return True
    return False


def _pred_a7(inp: ValidatorInputs) -> bool:
    return bool(
        re.search(r"(?m)^RUN-SITE:\s*pending-producers", inp.locus_text)
        and producer_rows(inp.producers_text) >= 1
    )


def _pred_a8(inp: ValidatorInputs) -> bool:
    if inp.files_present is None:
        return False
    return bool(
        re.search(r"(?m)^OBSERVE-VIA:[ \t]*artifact-file[ \t]*$", inp.locus_text)
        # ponytail: explicit CI labels only; extend from real locus examples, not prose inference.
        and re.search(
            r"(?im)^(?:PRINT-SITE|RUN-SITE):[^\n]*"
            r"(?:\bGitHub Actions\b[^\n]*\bjob\b|\bCI job\b|\bci-runner\b)",
            inp.locus_text,
        )
        and not any(
            re.search(r"(?m)^RESULT:[ \t]*(?:PASS|FAIL)[ \t]*$", text)
            for text in inp.artifact_texts or []
        )
        and not any(_JOB_LOG.fullmatch(Path(f).name) for f in inp.files_present)
    )


def _pred_a9(inp: ValidatorInputs) -> bool:
    blob = inp.report + "\n" + inp.observation_text
    ref_m = re.search(r"(?m)^Reference-context value:\s*(.+)$", blob)
    obs_m = re.search(r"(?m)^Observable that differs:\s*`?([\w-]+)", blob)
    if not ref_m or not obs_m:
        return False
    ref = ref_m.group(1).strip()
    if ref not in {"true", "false"}:
        return False
    obsv = re.search(
        rf"(?m)^(?:reference|control)[^\n]*?\b{re.escape(obs_m.group(1))}=(true|false)",
        inp.observation_text,
    )
    return bool(obsv and obsv.group(1) != ref)


def _pred_a10(inp: ValidatorInputs) -> bool:
    tl = inp.tasklist_text
    blocked = re.search(
        r"(?i)capability-verdict\**:\s*\**blocked(?![\w-])|\bblocked on capability\b",
        tl,
    )
    if not blocked:
        return False
    search = _section(tl, "Emitter search")
    counts = {}
    for key in ("emitters-found", "already-read-files", "usable-capture-routes"):
        values = re.findall(rf"(?m)^{key}:[ \t]*([^\n]*)$", search)
        if len(values) != 1 or not re.fullmatch(r"0|[1-9][0-9]*", values[0].strip()):
            return True
        counts[key] = int(values[0].strip())
    required = ["channels searched", "channel exclusions"]
    if counts["emitters-found"] or counts["already-read-files"]:
        required.append("candidate exclusions")
    # Mechanical presence only: truth/completeness of discovery and exclusion
    # prose still requires evidence review; regex cannot establish datum access.
    proven = counts["usable-capture-routes"] == 0 and all(
        re.search(rf"(?m)^{key}:[ \t]*\S[^\n]*$", search) for key in required
    )
    return not proven


def _pred_c1(inp: CalibratorInputs) -> bool:
    conf = inp.calibrated if inp.calibrated is not None else 0.0
    return bool(ENUM_TOKEN.search(_headline(inp.card)) and conf < 0.5)


def _pred_c3(inp: CalibratorInputs) -> bool:
    if not re.search(r"(?i)\bcontrol (run|arm)s?\b", inp.card):
        return False
    return not re.search(r"(?m)^CONTROL-PROOF:\s*yes:\s*\S+:\d+", inp.locus_text)


def _pred_c3b(inp: CalibratorInputs) -> bool:
    return bool(re.search(r"(?m)^runs-in[=:]\s*unknown\b", inp.card))


def _pred_c4(inp: CalibratorInputs) -> bool:
    rows = table_rows(
        _section(inp.card, "Proposed instrumentation")
        or _section(inp.tasklist_text, "Discriminator rows")
    )
    if not rows:
        return False
    return any(len(r) < 3 or not r[1].strip() or not r[2].strip() for r in rows)


def _pred_c5(inp: CalibratorInputs) -> bool:
    return bool(_ts_violations(inp.card, inp.card_mtime))


def _pred_c6(inp: CalibratorInputs) -> bool:
    if inp.bracket_text is None:
        return False
    return bool(
        _C6_THRESH.search(_headline(inp.card))
        and not re.search(r"(?m)^bracket=\[\d+,\d+\] width=\d+", inp.bracket_text)
    )


def _pred_c7(inp: CalibratorInputs) -> bool:
    named = _card_fm(inp.card, "claim_class") == "environment_dependent" or re.search(
        r"(?m)^environment-property:", inp.card
    )
    if not named:
        return False
    return not re.search(r"(?i)2[x×]2 row|## Discriminator rows", inp.card)


def _pred_c8(inp: CalibratorInputs) -> bool:
    if not inp.behaviour_text:
        return False
    m = re.search(r"behaviour-definition:\s*row\s*(\d+)", inp.card)
    if not m:
        return True
    row = table_row_by_index(inp.behaviour_text, int(m.group(1)))
    return row is None or not row[-1].strip()


def evaluate_validator(inp: ValidatorInputs) -> ValidatorResult:
    ids: set[str] = set()
    flags: set[str] = set()
    dropped = _pred_a3(inp)
    suspects: list[str] = []
    preds = {
        "A1": _pred_a1,
        "A2": _pred_a2,
        "A4": _pred_a4,
        "A5": _pred_a5,
        "A6": _pred_a6,
        "A7": _pred_a7,
        "A8": _pred_a8,
        "A9": _pred_a9,
        "A10": _pred_a10,
    }
    if dropped:
        ids.add("A3")
        flags.add(FLAG_BY_ID["A3"].flag)
    for aid, pred in preds.items():
        if pred(inp):
            ids.add(aid)
            flags.add(FLAG_BY_ID[aid].flag)
            if aid == "A9":
                suspects.append(FLAG_BY_ID[aid].flag)
    status: str | None = None
    if ids & {"A6", "A7"}:
        status = "FAIL"
    elif "A8" in ids:
        status = "blocked"
    elif ids & {"A1", "A2", "A4", "A5", "A10"}:
        status = "partial"
    return ValidatorResult(
        flags=flags,
        ids=ids,
        status=status,
        dropped_lines=dropped,
        suspect_probes=suspects,
        headline_prefix=_A8_PREFIX if "A8" in ids else None,
    )


def evaluate_calibrator(inp: CalibratorInputs) -> CalibratorResult:
    ids: set[str] = set()
    flags: set[str] = set()
    dims: dict[str, float] = {}
    caps: list[float] = []
    if _pred_c1(inp):
        ids.add("C1")
        flags.add(FLAG_BY_ID["C1"].flag)
    bad = _c2_tokens(inp.card)
    if bad:
        ids.add("C2")
        flags.update(f"unproven_exclusion:{t}" for t in bad)
        dims["Runtime check"] = 0.0
    if _pred_c3(inp):
        ids.add("C3")
        flags.add(FLAG_BY_ID["C3"].flag)
        dims["Symptom coverage"] = 0.5
    if _pred_c3b(inp):
        ids.add("C3b")
        flags.add(FLAG_BY_ID["C3b"].flag)
        dims["Runtime check"] = min(dims.get("Runtime check", 0.5), 0.5)
    if _pred_c4(inp):
        ids.add("C4")
        flags.add(FLAG_BY_ID["C4"].flag)
        dims["Fix directness"] = 0.5
    if _pred_c5(inp):
        ids.add("C5")
        flags.add(FLAG_BY_ID["C5"].flag)
    if _pred_c6(inp):
        ids.add("C6")
        flags.add(FLAG_BY_ID["C6"].flag)
        caps.append(0.3)
    if _pred_c7(inp):
        ids.add("C7")
        flags.add(FLAG_BY_ID["C7"].flag)
        caps.append(0.5)
    if _pred_c8(inp):
        ids.add("C8")
        flags.add(FLAG_BY_ID["C8"].flag)
        caps.append(0.5)
    return CalibratorResult(
        flags=flags,
        ids=ids,
        dims=dims,
        cap=min(caps) if caps else None,
        verdict="ESCALATE" if "C1" in ids else None,
    )


def load_fixture(path: Path) -> Fixture:
    meta, body = _parse_frontmatter(path.read_text())
    parts = _FILE_SPLIT.split(body)
    files: dict[str, str] = {}
    idx = 1 if parts and not parts[0].strip() else 0
    if idx == 0 and parts and not parts[0].startswith("--- file:"):
        idx = 1
    while idx + 1 < len(parts):
        files[parts[idx]] = parts[idx + 1]
        idx += 2
    if "expected_flags" not in meta:
        meta["expected_flags"] = []
    elif isinstance(meta["expected_flags"], str):
        meta["expected_flags"] = _parse_list(str(meta["expected_flags"]))
    return Fixture(path=path, meta=meta, files=files)


def _mtime(fx: Fixture) -> datetime | None:
    return _parse_iso(fx.meta.get("artifact_mtime"))


def validator_inputs(fx: Fixture) -> ValidatorInputs:
    files = fx.files
    present = fx.meta.get("files_present")
    if isinstance(present, str):
        present = _parse_list(present)
    names = list(present) if present is not None else None
    job_bodies: list[str] = []
    for name, text in files.items():
        if _JOB_LOG.fullmatch(Path(name).name):
            job_bodies.append(text)
            if names is not None and name not in names:
                names.append(name)
    mt = _mtime(fx)
    mtimes: dict[str, datetime] = {}
    if mt:
        mtimes["REPORT.md"] = mt
        mtimes["calibration"] = mt
    cards = [
        text
        for name, text in files.items()
        if re.search(r"hypothesis|card", name, re.I)
    ]
    cals = [
        text for name, text in files.items() if name.lower().startswith("calibration")
    ]
    return ValidatorInputs(
        report=files.get("REPORT.md", ""),
        calibration_texts=cals,
        diff_text=files.get("diff.patch", ""),
        artifact_mtimes=mtimes,
        producers_text=files.get("producers.md", ""),
        tasklist_text=files.get("diagnosability-tasklist.md", ""),
        locus_text=files.get("execution-locus.md", ""),
        observation_text=files.get("tier1-observation.md", ""),
        candidate_fixes_text=files.get("candidate-fixes.md", ""),
        card_texts=cards,
        files_present=tuple(names) if names is not None else None,
        artifact_texts=job_bodies,
        first_instrumented_run=json.loads(
            files.get("first-instrumented-run.json", "{}")
        ),
    )


def calibrator_inputs(fx: Fixture) -> CalibratorInputs:
    files = fx.files
    card = files.get("card.md", "")
    if not card:
        for name, text in files.items():
            if re.search(r"hypothesis|card", name, re.I):
                card = text
                break
    cal: float | None = None
    if "calibrated" in fx.meta:
        cal = float(fx.meta["calibrated"])  # type: ignore[arg-type]
    cals = [
        text for name, text in files.items() if name.lower().startswith("calibration")
    ]
    if cal is None and cals:
        cal = _calibrated(cals)
    bracket: str | None
    if "bracket.md" in files:
        bracket = files["bracket.md"]
    else:
        bracket = None
    return CalibratorInputs(
        card=card,
        calibrated=cal,
        card_mtime=_mtime(fx),
        locus_text=files.get("execution-locus.md", ""),
        bracket_text=bracket,
        behaviour_text=files.get("behaviour-definitions.md", ""),
        tasklist_text=files.get("diagnosability-tasklist.md", ""),
    )


def fired_ids(fx: Fixture) -> set[str]:
    aid = str(fx.meta.get("assertion", ""))
    if aid.startswith("A"):
        return evaluate_validator(validator_inputs(fx)).ids
    return evaluate_calibrator(calibrator_inputs(fx)).ids


def fired_flags(fx: Fixture) -> set[str]:
    aid = str(fx.meta.get("assertion", ""))
    if aid.startswith("A"):
        return evaluate_validator(validator_inputs(fx)).flags
    return evaluate_calibrator(calibrator_inputs(fx)).flags
