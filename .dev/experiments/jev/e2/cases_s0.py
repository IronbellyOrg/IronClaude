"""E2 Stage 0 cases (24).  `uv run --no-project python cases_s0.py` writes offline/docs/*.md and offline/cases/s0/*.json.

6 real-theme cases on the ORIGINAL S1 spec (T1, T2, T3 and the three largest "other" catalog clusters), 6 seeded S1 variants,
8 synthetic mini-specs with one seeded defect each, 4 synthetic clean controls.  Every case is authored as a proposed defect
plus 2-3 proposed evidence quotes (exact substrings, each resolving to exactly one extracted passage).  The labelers (contract
J8) see the document, the proposed defect and the quotes; `author_intent` is never shown to them and is not truth.
Case ids are opaque (`s0-NN`, shuffled with a fixed seed) so ids and file names reveal nothing about a case.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import random
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
JEV = HERE.parent / "jev"
if str(JEV) not in sys.path:
    sys.path.insert(0, str(JEV))

import extract as X                      # noqa: E402
import synth_docs                        # noqa: E402
from p15common import datasets           # noqa: E402

SP = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad")
S1_SPEC = (SP / "exp346/.dev/experiments/346-validation/phase2/S1/inputs/repo-overlay/.dev/orca-command-refactor/specs/"
           "orca-worker-contract-spec.md")
S1_SHA = "d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d"
CASE_SEED = 20260   # shuffles case numbers (decision.toml [stage0] case_seed)
DOCS_DIR = HERE / "offline" / "docs"
CASES_DIR = HERE / "offline" / "cases" / "s0"


def load_s1() -> str:
    b = S1_SPEC.read_bytes()
    assert hashlib.sha256(b).hexdigest() == S1_SHA, "S1 spec sha mismatch"
    return b.decode("utf-8")


def _replace_once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"edit anchor must occur exactly once: {old[:60]!r} x{text.count(old)}"
    return text.replace(old, new)


def _insert_after_line(text: str, anchor_line_prefix: str, new_line: str) -> str:
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if l.startswith(anchor_line_prefix)]
    assert len(hits) == 1, f"anchor line must occur once: {anchor_line_prefix[:50]!r} x{len(hits)}"
    lines.insert(hits[0] + 1, new_line)
    return "\n".join(lines)


# ------------------------------------------------------------------ seeded S1 variants (edits of the original text)
def v_outcome_contradiction(t):      # contradiction between distant sections (WC-5 vs AC-2.2)
    return _replace_once(t, "| `worker_done --outcome failed`; contract `status: blocked` with a non-empty",
                         "| `worker_done --outcome succeeded`; contract `status: blocked` with a non-empty")


def v_command_runs_orca(t):          # contradiction between distant sections (WC-3 vs SA-2)
    return _replace_once(t, "the session may instead ask the coordinator once with the preamble's `ask` command, wait,",
                         "the command itself runs `orca-ide orchestration ask` to ask the coordinator once, wait,")


def v_impossible_check(t):           # impossible acceptance check (AC-1.2 vs 7.2 step 4)
    return _replace_once(t, "`--unattended --output <dir>` | all steps pass |",
                         "`--unattended --output <dir>` | all steps pass, and at step 4 the contract's `status` is `running` |")


def v_chain_wait(t):                 # reference chain AC-4.4 -> WC-13 -> WC-10
    t = _insert_after_line(t, "| WC-12 |", "| WC-13 | **Heartbeat gap bound.** A worker's longest single wait obeys the splitting rule of WC-10. "
                           "| Command (wait size) | `CAPS:130` |")
    return _insert_after_line(t, "| P4 | AC-4.3 |", "| P4 | AC-4.4 | Wait-size check on `/sc:cli-eval run --unattended`: `worker-read` transcript "
                              "inspected for the longest single tool call | no single tool call exceeds 360 s (WC-13) |")


def v_chain_memory(t):               # reference chain AC-3.5 -> WC-11 -> AC-3.4
    return _insert_after_line(t, "| P3 | AC-3.4 |", "| P3 | AC-3.5 | Run `/sc:save --unattended` twice in one worktree and compare "
                              "`.superclaude/memory/pm_context.md` | the second run overwrites `pm_context.md` with the new "
                              "session's content (WC-11) |")


def v_path_collision(t):             # global path rule vs a per-row fixed path, no shared basename
    return _insert_after_line(t, "| SA-6 |", "| SA-7 | In unattended mode every command writes its report under "
                              "`.dev/worker-reports/<slug>/`, whatever its output flag says. | One place for the coordinator to "
                              "look in a worktree. | `.dev/orca-command-refactor/README.md:31` |")


# ------------------------------------------------------------------ case specs
def specs():
    S = []

    def add(layer, category, family, group, doc_key, defect, quotes, expect, **kw):
        S.append(dict(layer=layer, category=category, family=family, group=group, doc_key=doc_key, defect=defect,
                      quotes=quotes, expect=expect, **kw))

    # ---- 6 real-theme cases on the original S1 spec
    add("real", "theme-T1", "s1-original", "s1-original", "s1:orig",
        "Acceptance check AC-1.1 requires every command in sections 3.1-3.2 to have a `## Unattended mode` section naming "
        "`return-contract.yaml`, but the `load` row says load has no report and is not used as its own Task.",
        ["every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`",
         "| load | no gate | none (see note) | n/a |"], "defect", theme="T1", cluster="D12")
    add("real", "theme-T2", "s1-original", "s1-original", "s1:orig",
        "WC-4 puts the contract at `<output-dir>/return-contract.yaml` in the directory the coordinator passed, but the adversarial "
        "row puts it in a subdirectory `<output>/adversarial/`, so the coordinator cannot know the path from the brief alone.",
        ["the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed",
         "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"], "defect", theme="T2", cluster="D1")
    add("real", "theme-T3", "s1-original", "s1-original", "s1:orig",
        "AC-0.4 requires steps 1-3 of the live check to pass in Phase 0, but step 3 needs the WC-4 contract path, which only "
        "Phase 1 introduces; Phase 0 makes no command edits.",
        ["steps 1-3 and 5-7 pass; step 4 uses the command's existing report file",
         "its report path is the WC-4 contract path",
         "| The WC-4 contract in unattended mode;"], "defect", theme="T3", cluster="D19")
    add("real", "other-D16", "s1-original", "s1-original", "s1:orig",
        "The additive-edits check AC-C5 greps for lines matching `^-[^-]`, which cannot see a deleted markdown bullet (it appears "
        "in a zero-context diff as `-- item`), so SA-4's claim that edits are additive is not proved.",
        ["Command-file edits in Phases 1-3 are additive", "prints nothing: edits are additive"], "defect", theme="other", cluster="D16")
    add("real", "other-D7", "s1-original", "s1-original", "s1:orig",
        "WC-10 requires splitting only for single waits longer than 5 minutes but sets the split size at 4 minutes, so a "
        "4.5-minute wait is allowed by WC-10 yet fails the 240 s limit in AC-4.3.",
        ["must be split into waits of at most 4 minutes", "no single tool call exceeds 240 s"], "defect", theme="other", cluster="D7")
    add("real", "other-D8", "s1-original", "s1-original", "s1:orig",
        "WC-9 and decision D4 make outward actions depend on a coordinator quoting the user's instruction in the brief, which no "
        "command can check, so nothing in the spec enforces that authorization.",
        ["It turns on only through the command's own explicit flag written in the brief.",
         "The coordinator quotes the instruction in the brief and passes the command's explicit flag"], "defect",
        theme="other", cluster="D8")

    # ---- 6 seeded S1 variants
    add("seeded", "seed-contradiction", "s1-edit-outcome", "s1-edit-outcome", "s1:outcome",
        "WC-5 maps a `blocked` report to `worker_done --outcome failed`, but AC-2.2 expects `worker_done --outcome succeeded` "
        "for a run whose contract says `status: blocked`.",
        ["`--outcome failed` when the report says `failed` or `blocked`",
         "| `worker_done --outcome succeeded`; contract `status: blocked`"], "defect")
    add("seeded", "seed-contradiction", "s1-edit-orca", "s1-edit-orca", "s1:orca",
        "WC-3 has the command itself run an `orca-ide orchestration ask` command, but SA-2 says no command, skill or agent file "
        "runs an `orca` or `orca-ide` command.",
        ["the command itself runs `orca-ide orchestration ask` to ask the coordinator once",
         "No command, skill or agent file runs an `orca` or `orca-ide` command"], "defect")
    add("seeded", "seed-impossible-check", "s1-edit-check", "s1-edit-check", "s1:check",
        "AC-1.2 passes only if all steps of the 7.2 live check pass and the contract's `status` is `running` at step 4, but step 4 "
        "asserts that `status` is one of succeeded, partial, failed or blocked.",
        ["all steps pass, and at step 4 the contract's `status` is `running`",
         "assert d['status'] in {'succeeded','partial','failed','blocked'}"], "defect")
    add("seeded", "seed-chain", "s1-edit-wait", "s1-edit-wait", "s1:wait",
        "AC-4.4 allows single waits up to 360 s and cites WC-13, WC-13 defers to the splitting rule of WC-10, and WC-10 requires "
        "waits of at most 4 minutes (240 s); only the chain shows that AC-4.4 passes runs that WC-10 forbids.",
        ["no single tool call exceeds 360 s (WC-13)", "obeys the splitting rule of WC-10",
         "must be split into waits of at most 4 minutes"], "defect")
    add("seeded", "seed-chain", "s1-edit-memory", "s1-edit-memory", "s1:memory",
        "AC-3.5 expects the second `/sc:save --unattended` run to overwrite `pm_context.md` (citing WC-11); WC-11 says memory keys "
        "overwritten whole are not written in unattended mode, and AC-3.4 lists `pm_context.md` among the single-owner files "
        "whose hashes must stay unchanged; only the chain shows the two checks cannot both pass.",
        ["the second run overwrites `pm_context.md` with the new session's content (WC-11)",
         "single-owner shared files (for example memory keys overwritten whole) are not written in unattended mode",
         "two new per-session files; the single-owner files' hashes unchanged"], "defect")
    add("seeded", "seed-path-collision", "s1-edit-path", "s1-edit-path", "s1:path",
        "SA-7 says every command writes its report under `.dev/worker-reports/<slug>/` whatever its output flag says, but the "
        "cleanup-audit row fixes its report at `.claude-audit/pass<N>-summary.md` with a fixed output directory.",
        ["every command writes its report under `.dev/worker-reports/<slug>/`, whatever its output flag says",
         "`.claude-audit/pass<N>-summary.md`"], "defect")

    # ---- 8 synthetic mini-specs with one seeded defect each
    add("synthetic", "synth-novel", "uploader", "fam-uploader", "syn:uploader",
        "UP-6 loads the whole archive into memory before sending, archives reach 500 MB, and UP-1 forbids holding more than 20 MB "
        "in RAM, so the uploader cannot satisfy UP-1 on a large archive.",
        ["The uploader must never hold more than 20 MB of its working data in RAM at any moment",
         "The uploader loads the complete archive into memory, then signs it and sends it",
         "archives of monorepo projects range up to 500 MB"], "defect")
    add("synthetic", "synth-novel", "export", "fam-export", "syn:export",
        "SEC-1 expires a session token after 15 minutes without user input, but a full export runs up to 2 hours with no user input "
        "and the page authenticates every poll with that token, so the page loses access before the export finishes.",
        ["A session token expires after 15 minutes without user input",
         "The page polls the job endpoint every 10 seconds and authenticates each poll with the user's session token",
         "A full-project export can run for up to 2 hours"], "defect")
    add("synthetic", "synth-novel", "digest", "fam-digest", "syn:digest",
        "DIG-1 sends the digest at 08:00 in each user's local morning, but PRIV-2 says the service holds no information about "
        "where a user is, including the time zone, so local morning cannot be known.",
        ["The service holds no information about where a user is, including the user's time zone",
         "Each user's digest is sent at 08:00 in that user's local morning"], "defect")
    add("synthetic", "synth-exception", "retention", "fam-retention", "syn:retention",
        "RET-1 requires every deleted record to be purged within 30 days with no exceptions, but RET-5 keeps a deleted record "
        "until its support ticket closes, which can be longer than 30 days.",
        ["Every deleted record is purged from all stores within 30 days of deletion, with no exceptions",
         "A deleted record that is referenced by an open support ticket is kept until the ticket closes"], "defect")
    add("synthetic", "synth-exception", "ratelimit", "fam-ratelimit", "syn:ratelimit",
        "RL-1 limits every key to 100 requests per minute and says the limit cannot be raised for any key, but RL-6 allows "
        "enterprise keys 1,000 requests per minute.",
        ["Every API key is limited to 100 requests per minute. This limit is fixed and cannot be raised for any key",
         "Enterprise keys are allowed 1,000 requests per minute"], "defect")
    add("synthetic", "synth-chain", "payments", "fam-payments", "syn:payments",
        "PAY-2 retries a timed-out capture three times following RTY-1, RTY-1 takes the retry budget from TIER-1, and TIER-1 gives "
        "capture a budget of 0 because a repeat could charge the customer twice.",
        ["A capture that times out is retried three times following RTY-1",
         "The number of retries for a call is the retry budget listed for its call type in TIER-1",
         "| TIER-1 | capture | 0 |"], "defect")
    add("synthetic", "synth-chain", "locks", "fam-locks", "syn:locks",
        "PAY-3 has the worker hold its lock for a 2-second capture (citing LOCK-2), LOCK-2 limits a lock to 5 ticks, and CFG-1 "
        "defines a tick as 100 milliseconds, so the lock lasts 500 ms and expires during the capture.",
        ["A payment capture takes 2 seconds, and the worker holds its lock for the whole capture (LOCK-2)",
         "A lock is held for at most 5 ticks (see CFG-1 for the tick)",
         "One tick is 100 milliseconds"], "defect")
    add("synthetic", "synth-unit", "gateway", "fam-gateway", "syn:gateway",
        "GW-2 limits request bodies to 10 MB, but NGX-1 makes the proxy in front of the gateway reject bodies larger than 10 Mbit "
        "(1.25 MB), so bodies the gateway accepts never arrive.",
        ["Request bodies are limited to 10 MB", "The proxy in front of the gateway rejects bodies larger than 10 Mbit"], "defect")

    # ---- 4 synthetic clean controls (apparent overlap, resolved in the document)
    add("control", "control-conditions", "logs_tier", "fam-logs", "syn:logs_tier",
        "LOG-1 says logs are kept for 7 days but LOG-2 says logs are kept for 30 days.",
        ["Projects on the free tier keep logs for 7 days", "Projects on the paid tier keep logs for 30 days"], "clean")
    add("control", "control-exception", "passwords", "fam-passwords", "syn:passwords",
        "AUTH-3 says passwords expire after 90 days, but AUTH-7 says service-account credentials are rotated every 24 hours "
        "instead.",
        ["Passwords expire after 90 days", "Service accounts are exempt from AUTH-3"], "clean")
    add("control", "control-conditions", "multipart", "fam-multipart", "syn:multipart",
        "STO-1 requires uploads over 5 GB to use multipart upload, but STO-2 rejects uploads over 5 GB.",
        ["Uploads over 5 GB must use multipart upload", "Uploads over 5 GB are rejected on the free plan"], "clean")
    add("control", "control-exception", "freeze", "fam-freeze", "syn:freeze",
        "REL-4 forbids deployments during the last week of each quarter, but REL-9 allows security patches to be deployed "
        "during that week.",
        ["No deployments during the last week of each quarter",
         "Security patches may be deployed at any time, including during the freeze in REL-4"], "clean")
    return S


def documents() -> dict:
    s1 = load_s1()
    d = {"s1:orig": s1, "s1:outcome": v_outcome_contradiction(s1), "s1:orca": v_command_runs_orca(s1),
         "s1:check": v_impossible_check(s1), "s1:wait": v_chain_wait(s1), "s1:memory": v_chain_memory(s1),
         "s1:path": v_path_collision(s1)}
    for k, v in synth_docs.DOCS.items():
        d["syn:" + k] = v
    return d


def doc_name(text: str) -> str:
    return "doc-" + hashlib.sha256(text.encode("utf-8")).hexdigest()[:10] + ".md"


def build(write: bool = True, check: bool = True) -> list:
    docs = documents()
    sp = specs()
    order = list(range(len(sp)))
    random.Random(CASE_SEED).shuffle(order)
    cases = []
    for num, idx in enumerate(order, start=1):
        s = sp[idx]
        text = docs[s["doc_key"]]
        rel = "offline/docs/" + doc_name(text)
        passages = X.extract(text)
        pids = []
        for q in s["quotes"]:
            hits = X.find_quote(passages, q)
            if check:
                assert len(hits) == 1, f"{s['category']} {s['doc_key']}: quote must resolve to exactly one passage ({len(hits)}): {q[:70]!r}"
            if hits and hits[0].pid not in pids:
                pids.append(hits[0].pid)
        cid = f"s0-{num:02d}"
        data_class = "s1_spec" if s["doc_key"].startswith("s1:") else "synthetic"
        case = {
            "case_id": cid, "group": s["group"], "family": s["family"], "category": s["category"], "variant": s["layer"],
            "split": "s0", "data_classes": [data_class],
            "source": {"kind": "s1" if data_class == "s1_spec" else "synthetic", "paths": [rel], "url": None},
            "packet": {"doc": rel, "doc_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(), "defect": s["defect"],
                       "evidence_quotes": s["quotes"], "evidence_set": pids},
            "author_intent": {"expect": s["expect"], "layer": s["layer"], "category": s["category"],
                              **{k: s[k] for k in ("theme", "cluster") if k in s}},
        }
        cases.append(case)
    if write:
        DOCS_DIR.mkdir(parents=True, exist_ok=True)
        CASES_DIR.mkdir(parents=True, exist_ok=True)
        for p in CASES_DIR.glob("*.json"):
            p.unlink()
        for k, text in docs.items():
            (DOCS_DIR / doc_name(text)).write_text(text, encoding="utf-8")
        for c in cases:
            datasets.write_case(CASES_DIR / f"{c['case_id']}.json", c)
    return cases


if __name__ == "__main__":
    cs = build()
    import collections
    print(len(cs), "cases;", dict(collections.Counter(c["author_intent"]["layer"] for c in cs)))
    for c in cs:
        print(c["case_id"], c["author_intent"]["layer"], c["category"], c["packet"]["evidence_set"])
