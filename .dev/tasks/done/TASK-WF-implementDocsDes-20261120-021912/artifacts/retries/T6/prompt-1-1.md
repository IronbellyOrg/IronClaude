5e4b2501f15a1d96bb062b3cee6728e5d55b0b30
Review one task for spec compliance.

Task brief: ## Task 6: Add Wave 4R to the workflow skill

Depends on: Task 5, Task 7

Edit `src/superclaude/skills/sc-workflow-protocol/SKILL.md`: add `## Wave 4R — Remediate` between Wave 4 and Wave 5 that loads `refs/remediation.md`, reads `finding_counts` from the Wave 4 reflect contract, runs `remediate.py route`, and follows the chosen route; replace the sentence "Advisory and read-only: never edit, delete, or regenerate `<id>.md` from findings, and never change the workflow `status` because of them." in Wave 4 with the bounded rule (the plan is changed only by Wave 4R, only for blocking findings, only on a copy); keep "never overwrite an existing package"; update `## Will / Will Not` (the old "modify the plan from reflect findings" ban becomes "edit a plan in place"); add the Wave 4R file operations (`mktemp`, copy and move through `remediate.py` only); add the Agent tool (and the Task tool, the name other skills of this repo list) to the `allowed-tools` list of the skill and limit the "Task fan-out" ban in Will Not to everything except the Wave 4R reviser and re-reviewer sub-agents; change Wave 5 so it writes the package contract into the final placed package (never into an archived one) and so `report_path` and the printed plan path name the final placed plan, with the archived package's contract written only by `remediate.py archive` and `mark`. Wave 5 merges into the contract that `place` and `mark` already wrote and never replaces the file: it creates the contract when none exists (route `none`), sets `status`, `reflect_*`, `handoff_*` and `unresolved`, fills every stable 1.1 field still missing (`slug`, `plan_path`, `source_path`, `source_origin`, `strategy`, `depth`) and keeps every line of `supersedes`, `remediation_route`, `finding_counts`, `fix_cycles`, `review_verdict` and `open_blockers`; the rule of `refs/return-contract.md` that allows a later rewrite to `partial` follows the same merge rule (edit that rule in Task 7). Mirror `SKILL.md`, the new `refs/remediation.md` and the new `scripts/remediate.py` into `plugins/superclaude/skills/sc-workflow-protocol/` (create the `scripts/` folder there, as the implement protocol's plugin copy has one).

Acceptance criteria:
- Wave 4R sits between the Wave 4 and Wave 5 headings and says the route runs after Wave 4 by default.
- The Wave 4 text no longer contains "never edit, delete, or regenerate" and the Will Not list no longer contradicts Wave 4R.
- `diff -rq` between `src/superclaude/skills/sc-workflow-protocol` and `plugins/superclaude/skills/sc-workflow-protocol` shows no difference (new ref and script included); `make sync-dev` then `make verify-sync` is clean.
- The skill's `allowed-tools` lists the Agent tool, and Wave 5 states that the contract and the printed plan path belong to the final placed package and that Wave 5 merges into the existing contract (a test in `tests/skills/test_workflow_remediation.py` reads `SKILL.md` and `refs/return-contract.md` and asserts the merge wording and that `review_verdict` is named as a line Wave 5 keeps).
Global constraints: ## Constraints

- The design is `docs/designs/surgical-remediation.md`. Where it disagrees with `.dev/issues/624/accuracy-check.md` or `.dev/issues/624/analysis/analyze-sc-workflow-protocol.md`, those two files win: the reflect bump has consumers, the workflow package contract stays at `contract_version: "1.1"`, and seven packages (not four) are migrated. Anchor edits by text, not by the line numbers of the design (they moved).
- Edit only `src/superclaude/` sources, `tests/`, `scripts/`, `plugins/superclaude/` copies of the edited files (including the new `refs/remediation.md` and `scripts/remediate.py` of the workflow skill, which the plugin mirror must carry (the `diff -rq` checks of Task 6 require it), and `plugins/superclaude/commands/workflow.md`), `.dev/README.md` and the data migration. Never hand-edit the dev copies under the project `.claude/` folder; after each task that changes a primitive run `make sync-dev` and then `make verify-sync`.
- Installed primitives never point at a `src/superclaude/...` path. In every edited skill, command or core doc, name other primitives by their installed path (`~/.claude/skills/<name>/SKILL.md`) and name the project `.claude/` copy second.
- Where a file in `plugins/superclaude/` mirrors an edited file (the workflow and implement protocols and `commands/workflow.md`), keep the mirror byte-identical to the `src/` file (`diff -rq` shows no difference); a new file in an already mirrored folder is mirrored too. `remediate.py` uses only the Python standard library (installed skill scripts run under `uv run --no-project`) and edits archived contracts by appending lines, never by loading and re-writing the YAML.
- Decision made by this plan because the design leaves it open: `finding_counts.label_high` counts the Deviations-table label HIGH on the legacy reviewer path, and counts findings-v2 severity CRITICAL on the shadow-panel path (the panel has no HIGH label). `blocking`, `medium` and `note` count the grades `Blocking (...)`, `Medium:` and `Note:` (or the panel's `blocking` flag). On the panel path, `medium` counts findings-v2 severity MAJOR with `blocking` false and `note` counts severity MINOR.
- The workflow package contract adds only additive fields under `contract_version: "1.1"`: `remediation_route`, `supersedes`, `superseded_by`, `finding_counts`, `fix_cycles`, `review_verdict`, `open_blockers`. `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` and `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py` keep accepting only "1.1".
- Only blocking findings are ever repaired. No fix pass touches text for a Medium or Note finding.
- Out of scope: the wording of the review severity rule, reviewer models, `/sc:design`, `/sc:brainstorm`, `/sc:spec-panel`'s own loop, deleting archived packages, and `src/superclaude/rules/prompts/document_review_loop_prompts.md` (reused as written).
- Reflect's own `--remediate` plan route keeps calling `sc:workflow`; `src/superclaude/cli/reflect/runner.py` gets no code change (its fail-closed handling of a non-zero apply already covers a refused package).
Start sha: 5e4b2501f15a1d96bb062b3cee6728e5d55b0b30
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md b/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md
index 1a3675c76..f264428a5 100644
--- a/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md
+++ b/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md
@@ -1,7 +1,7 @@
 ---
 name: sc:workflow-protocol
 description: "Behavioral protocol for /sc:workflow — PRD/spec to phased tasklist (<id>.md)"
-allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill, mcp__codegraph__codegraph_status, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_callees, mcp__codegraph__codegraph_impact
+allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill, Agent, Task, mcp__codegraph__codegraph_status, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_callees, mcp__codegraph__codegraph_impact
 argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--handoff none|design|implement]"
 ---
 
@@ -90,18 +90,26 @@ Final step of plan generation; runs only after Wave 3 passed, and **before** the
 
 Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) that call passes `--unattended --output <report-dir>/nested/reflect-<n>/` (reflect's own directory flag; workflow's `--output` stays retired; `<n>` counts from 1 and is never reused), still without `--remediate`, and the nested contract is listed in `artifacts`, also when the call failed.
 
-Advisory and read-only: never edit, delete, or regenerate `<id>.md` from findings, and never change the workflow `status` because of them. Reflect unavailable or `failed` → `reflect_status: skipped|failed`, `reflect_report_path: null`, one `unresolved` line; still proceed to Wave 5.
+This call itself is advisory: the plan is changed only by Wave 4R, only for blocking findings and only on a copy, never in place, and findings never change the workflow `status`. Never overwrite an existing package. Reflect unavailable or `failed` → `reflect_status: skipped|failed`, `reflect_report_path: null`, one `unresolved` line; still proceed to Wave 5.
+
+## Wave 4R — Remediate
+
+**Ref:** `refs/remediation.md`
+
+Runs after Wave 4 by default (`--remediate none` records the counts and the chosen route and changes nothing; `--remediate surgical|regenerate` forces a route; `--revise <package-dir> --review <REPORT.md>` runs it for a package reviewed outside workflow). Read `finding_counts` from the Wave 4 reflect contract, run `remediate.py route` (`~/.claude/skills/sc-workflow-protocol/scripts/remediate.py`, project copy `.claude/skills/sc-workflow-protocol/scripts/remediate.py` second) and follow the chosen route of the ref: `none` changes nothing; `surgical` repairs a copy and places it as a new package after archiving the original; `regenerate` runs Waves 0 to 3 once more (at most once per run); `escalate` stops and marks the package `review_verdict: FAIL`. Only blocking findings are repaired, at most 2 fix cycles.
+
+File operations of this wave: `mktemp -d /tmp/sc-workflow-revise.XXXXXXXX`, and every copy and move through `remediate.py` only (no `mv`, `cp` or `rm` by hand). The reviser and the re-reviewer are sub-agents started with the Agent tool (Task is the same tool under its other name).
 
 ## Wave 5 — Contract
 
 **Refs:** `refs/return-contract.md`, `refs/overlap-routing.md`
 
-Write `<pkg>/return-contract.yaml` (contract 1.1: stable `slug`, `./<id>.md`, `./source.md`, `reflect_*`) **before** any `implement` handoff. Apply handoff; a failed `implement` handoff on a valid plan is `partial`, a failed generation is `failed`.
+Write `return-contract.yaml` (contract 1.1: stable `slug`, `./<id>.md`, `./source.md`, `reflect_*`) into the **final placed package** (never into an archived one) **before** any `implement` handoff. Wave 5 merges into the contract that `place` and `mark` already wrote and never replaces the file: it creates the contract when none exists (route `none`), sets `status`, `reflect_*`, `handoff_*` and `unresolved`, fills every stable 1.1 field still missing (`slug`, `plan_path`, `source_path`, `source_origin`, `strategy`, `depth`) and keeps every line of `supersedes`, `remediation_route`, `finding_counts`, `fix_cycles`, `review_verdict` and `open_blockers`. `report_path` and the printed plan path name the final placed plan. The archived package's contract is written only by `remediate.py archive` and `mark`. Apply handoff; a failed `implement` handoff on a valid plan is `partial`, a failed generation is `failed`.
 
 After an `implement` handoff the package may have moved to `done/` (executor-owned archive). Resolve the actual location by id (`.dev/tasks/to-do/<id>` vs `.dev/tasks/done/<id>`, `test -e || test -L`): only if the package still exists at `to-do/` may you rewrite the contract (e.g. to `partial`), and never recreate a directory or write into a path whose package is absent. Only `done/` exists → leave the archived contract untouched, report the failure/outcome in chat, print the actual `done/` plan path. Both exist → mutate neither and report the conflict. Print the plan path at its actual location.
 
 ## Will / Will Not
 
-**Will:** one new package `.dev/tasks/to-do/<id>/` with `<id>.md`, `source.md`, `return-contract.yaml`; ground the plan in the real code through codegraph when the index is fresh. Never overwrites or reuses an existing package. Run `/sc:reflect --mode pre` (advisory) on the gated plan as the final generation step, before any handoff.
+**Will:** one new package `.dev/tasks/to-do/<id>/` with `<id>.md`, `source.md`, `return-contract.yaml`; ground the plan in the real code through codegraph when the index is fresh. Never overwrites or reuses an existing package. Run `/sc:reflect --mode pre` (advisory) on the gated plan as the final generation step, before any handoff. Then Wave 4R: repair blocking findings on a copy and place it as a new package, archiving the one it replaces.
 
-**Will Not:** product code, new agents, Task fan-out; modify the plan from reflect findings.
+**Will Not:** product code, new agents, Task fan-out (except the Wave 4R reviser and re-reviewer sub-agents); edit a plan in place, or change a plan for a Medium or Note finding.
diff --git a/plugins/superclaude/skills/sc-workflow-protocol/scripts/remediate.py b/plugins/superclaude/skills/sc-workflow-protocol/scripts/remediate.py
new file mode 100644
index 000000000..b4ea7f811
--- /dev/null
+++ b/plugins/superclaude/skills/sc-workflow-protocol/scripts/remediate.py
@@ -0,0 +1,689 @@
+#!/usr/bin/env python3
+"""Surgical-remediation helper for /sc:workflow (standard library only).
+
+Subcommands (all but ``route`` take ``--root <checkout>``; failures print
+``E-REMEDIATE-*`` (or the helper's ``E-ARCHIVE-*``) on stderr and exit 1):
+
+  route      print the remediation route as JSON
+  reserve    pick a new package id and create the empty leaf in to-do/
+  prepare    private copy of the old plan + source under /tmp
+  archive    move a superseded package to archive/ and mark its contract
+  place      fill the reserved leaf with the repaired package (surgical route)
+  restore    undo ``archive`` (package back to to-do/, contract as before)
+  mark       the one writer of review_verdict/open_blockers/superseded_by/...
+  release    remove the reserved leaf when it is empty or holds only place output
+
+Every move uses ``rename_noreplace`` of the sibling sc-implement-protocol
+skill (loaded by file path); contracts are edited as text, never as YAML.
+"""
+
+import argparse
+import datetime
+import difflib
+import hashlib
+import importlib.util
+import json
+import os
+import re
+import sys
+import tempfile
+from pathlib import Path
+
+ROUTES = ("none", "surgical", "regenerate")
+
+ID_RE = re.compile(r"^TASK-WF-([a-z][A-Za-z0-9]{0,15})-(\d{8}-\d{6})(?:-[2-9])?$")
+COUNT_KEYS = ("blocking", "label_high", "medium", "note")
+HELPER_PATH = (
+    Path(__file__).resolve().parent.parent.parent
+    / "sc-implement-protocol"
+    / "scripts"
+    / "archive_workspace.py"
+)
+UNDO_NAME = "archive-undo.txt"
+# files `place` writes (relative to the new package); release removes only these
+PLACE_FILES = (
+    "{id}.md",
+    "source.md",
+    "return-contract.yaml",
+    "artifacts/plan.diff",
+    "artifacts/prior-findings.md",
+    "artifacts/old-plan.md",
+    "artifacts/revision-log.md",
+)
+
+
+class RemediateError(Exception):
+    def __init__(self, code, msg):
+        super().__init__(msg)
+        self.code, self.msg = code, msg
+
+
+# --------------------------------------------------------------------- route
+def route(blocking, label_high, medium, regenerated_already=False, forced=None):
+    """Return (route, forced). Rows in order, first match wins."""
+    for name, v in (("blocking", blocking), ("label_high", label_high), ("medium", medium)):
+        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
+            raise ValueError(f"{name} must be a non-negative integer, got {v!r}")
+    if forced is not None and forced not in ROUTES:
+        raise ValueError(f"forced must be one of {ROUTES}, got {forced!r}")
+    if forced is not None:
+        result = forced
+    elif blocking == 0:
+        result = "none"
+    elif blocking <= 3 and label_high <= 5 and medium <= 9:
+        result = "surgical"
+    else:
+        result = "regenerate"
+    if result == "regenerate" and regenerated_already:
+        result = "escalate"
+    return result, forced is not None
+
+
+def _count(text):
+    try:
+        v = int(text)
+    except ValueError:
+        raise argparse.ArgumentTypeError(f"not an integer: {text!r}")
+    if v < 0:
+        raise argparse.ArgumentTypeError(f"negative count: {v}")
+    return v
+
+
+def _cmd_route(args):
+    r, forced = route(
+        args.blocking, args.label_high, args.medium, args.regenerated_already, args.forced
+    )
+    print(json.dumps({"route": r, "forced": forced}))
+    return 0
+
+
+# ------------------------------------------------------------------- helpers
+def _fail(code, msg):
+    raise RemediateError(code, msg)
+
+
+def _check_id(value, what):
+    if not isinstance(value, str) or not ID_RE.match(value):
+        _fail("E-REMEDIATE-ID", f"{what} is not a TASK-WF package id: {value!r}")
+    return value
+
+
+def _tasks(root):
+    root = Path(os.path.realpath(root))
+    if not os.path.lexists(root / ".git"):
+        _fail("E-REMEDIATE-ROOT", f"{root} is not a checkout root (.git missing)")
+    return root, root / ".dev" / "tasks"
+
+
+def _real_dir(p):
+    return os.path.isdir(p) and not os.path.islink(p)
+
+
+def _load_helper():
+    if not HELPER_PATH.is_file():
+        _fail(
+            "E-REMEDIATE-HELPER",
+            f"sibling helper missing, nothing moved: {HELPER_PATH}",
+        )
+    spec = importlib.util.spec_from_file_location("archive_workspace_helper", HELPER_PATH)
+    mod = importlib.util.module_from_spec(spec)
+    try:
+        spec.loader.exec_module(mod)
+    except Exception as exc:  # fail closed on any load problem
+        _fail("E-REMEDIATE-HELPER", f"cannot load {HELPER_PATH}: {exc}")
+    if not hasattr(mod, "rename_noreplace"):
+        _fail("E-REMEDIATE-HELPER", f"{HELPER_PATH} has no rename_noreplace")
+    return mod
+
+
+def _move(helper, src, dst):
+    try:
+        helper.rename_noreplace(str(src), str(dst))
+    except RemediateError:
+        raise
+    except Exception as exc:
+        code = getattr(exc, "code", "E-REMEDIATE-MOVE")
+        _fail(code, getattr(exc, "msg", str(exc)))
+
+
+def _sha(path):
+    h = hashlib.sha256()
+    with open(path, "rb") as f:
+        for chunk in iter(lambda: f.read(1 << 20), b""):
+            h.update(chunk)
+    return h.hexdigest()
+
+
+def _write_atomic(path, text):
+    tmp = f"{path}.tmp-{os.getpid()}"
+    with open(tmp, "w", encoding="utf-8") as f:
+        f.write(text)
+    os.replace(tmp, path)
+
+
+def _write_new(path, data):
+    """Exclusive create (never overwrites)."""
+    if isinstance(data, bytes):
+        with open(path, "xb") as f:
+            f.write(data)
+    else:
+        with open(path, "x", encoding="utf-8") as f:
+            f.write(data)
+
+
+def _parse_counts(text):
+    try:
+        obj = json.loads(text)
+    except ValueError as exc:
+        _fail("E-REMEDIATE-COUNTS", f"--finding-counts is not JSON: {exc}")
+    if (
+        not isinstance(obj, dict)
+        or set(obj) != set(COUNT_KEYS)
+        or any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in obj.values())
+    ):
+        _fail(
+            "E-REMEDIATE-COUNTS",
+            f"--finding-counts needs exactly {COUNT_KEYS} as non-negative integers",
+        )
+    return "{" + ", ".join(f'"{k}": {obj[k]}' for k in COUNT_KEYS) + "}"
+
+
+# ------------------------------------------------------ contract text edits
+def _key_idx(lines, key):
+    rx = re.compile(rf"^{re.escape(key)}:(\s|$)")
+    return [i for i, ln in enumerate(lines) if rx.match(ln)]
+
+
+def _block_end(lines, i):
+    """Index after the block lines (indented or '- ') that follow top-level line i."""
+    j = i + 1
+    last = i
+    while j < len(lines):
+        ln = lines[j]
+        if ln.strip() == "":
+            j += 1
+            continue
+        if ln[0] in " \t" or ln.startswith("- "):
+            last = j
+            j += 1
+            continue
+        break
+    return last + 1
+
+
+def _ins(lines, ops, idx, line):
+    lines.insert(idx, line)
+    ops.append(["ins", idx, line])
+
+
+def _rep(lines, ops, idx, new):
+    ops.append(["rep", idx, new, lines[idx]])
+    lines[idx] = new
+
+
+def _del(lines, ops, idx):
+    ops.append(["del", idx, lines[idx]])
+    del lines[idx]
+
+
+def _append_idx(lines):
+    return len(lines) - 1 if lines and lines[-1] == "" else len(lines)
+
+
+def _set_key(lines, ops, key, value):
+    """Replace the line of an existing key (dropping its block), else append once."""
+    hits = _key_idx(lines, key)
+    if len(hits) > 1:
+        _fail("E-REMEDIATE-CONTRACT", f"key {key} already appears {len(hits)} times")
+    new = f"{key}: {value}"
+    if hits:
+        i = hits[0]
+        for _ in range(_block_end(lines, i) - i - 1):
+            _del(lines, ops, i + 1)
+        _rep(lines, ops, i, new)
+    else:
+        _ins(lines, ops, _append_idx(lines), new)
+
+
+def _add_unresolved(lines, ops, item):
+    q = json.dumps(item)
+    hits = _key_idx(lines, "unresolved")
+    if len(hits) > 1:
+        _fail("E-REMEDIATE-CONTRACT", "key unresolved appears more than once")
+    if not hits:
+        at = _append_idx(lines)
+        _ins(lines, ops, at, "unresolved:")
+        _ins(lines, ops, at + 1, f"  - {q}")
+        return
+    i = hits[0]
+    rest = lines[i].split(":", 1)[1].strip()
+    if rest in ("", "~", "null", "[]"):
+        if rest:
+            _rep(lines, ops, i, "unresolved:")
+            end = i + 1
+        else:
+            end = _block_end(lines, i)
+        indent = "  "
+        for ln in lines[i + 1 : end]:
+            m = re.match(r"^(\s*)- ", ln)
+            if m:
+                indent = m.group(1)
+                break
+        _ins(lines, ops, end, f"{indent}- {q}")
+    elif rest.startswith("[") and rest.endswith("]"):
+        _rep(lines, ops, i, lines[i][: lines[i].rindex("]")] + f", {q}]")
+    else:
+        _fail("E-REMEDIATE-CONTRACT", f"cannot edit unresolved value: {rest!r}")
+
+
+def _undo_ops(lines, ops):
+    """Reverse `ops` (recorded by the helpers above) on `lines`; raise on mismatch."""
+    for op in reversed(ops):
+        kind = op[0]
+        if kind == "ins":
+            _, idx, line = op
+            if idx >= len(lines) or lines[idx] != line:
+                _fail("E-REMEDIATE-RESTORE", f"contract changed since archive (line {idx})")
+            del lines[idx]
+        elif kind == "rep":
+            _, idx, new, orig = op
+            if idx >= len(lines) or lines[idx] != new:
+                _fail("E-REMEDIATE-RESTORE", f"contract changed since archive (line {idx})")
+            lines[idx] = orig
+        elif kind == "del":
+            _, idx, orig = op
+            lines.insert(idx, orig)
+        else:
+            _fail("E-REMEDIATE-RESTORE", f"unknown undo op {kind!r}")
+
+
+# ------------------------------------------------------------------- reserve
+def reserve(root, old_id, now=None):
+    _check_id(old_id, "--old-id")
+    root, tasks = _tasks(root)
+    if not _real_dir(tasks / "to-do" / old_id):
+        _fail("E-REMEDIATE-SOURCE", f"{tasks / 'to-do' / old_id} is not a real directory")
+    subject = ID_RE.match(old_id).group(1)
+    stamp = now or datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")
+    base = f"TASK-WF-{subject}-{stamp}"
+    _check_id(base, "computed id")
+    todo = tasks / "to-do"
+    for suffix in [""] + [f"-{n}" for n in range(2, 10)]:
+        cand = base + suffix
+        if any(os.path.lexists(tasks / d / cand) for d in ("to-do", "done", "archive")):
+            continue
+        try:
+            os.mkdir(todo / cand)  # plain exclusive mkdir, never -p
+        except FileExistsError:
+            continue
+        return cand
+    _fail("E-PACKAGE-COLLISION", f"{base} and suffixes -2..-9 are all taken")
+
+
+# ------------------------------------------------------------------- prepare
+def prepare(root, old_id, new_id):
+    _check_id(old_id, "--old-id")
+    _check_id(new_id, "--new-id")
+    root, tasks = _tasks(root)
+    old = tasks / "to-do" / old_id
+    if not _real_dir(tasks / "to-do" / new_id):
+        _fail("E-REMEDIATE-LEAF", f"reserved leaf missing: {tasks / 'to-do' / new_id}")
+    plan, source = old / f"{old_id}.md", old / "source.md"
+    for f in (plan, source):
+        if os.path.islink(f) or not f.is_file():
+            _fail("E-REMEDIATE-SOURCE", f"{f} must be a regular file")
+    text = plan.read_text(encoding="utf-8")
+    m = re.match(r"^(---\n)(.*?)(\n---\n)", text, re.S)
+    if not m or not re.search(r"^slug:.*$", m.group(2), re.M):
+        _fail("E-REMEDIATE-SOURCE", "plan has no front-matter slug line")
+    front = re.sub(r"^slug:.*$", f"slug: {new_id}", m.group(2), count=1, flags=re.M)
+    new_text = m.group(1) + front + m.group(3) + text[m.end():]
+    tmp = tempfile.mkdtemp(prefix="sc-workflow-revise.", dir="/tmp")  # mktemp -d semantics
+    copy = Path(tmp) / new_id
+    copy.mkdir()
+    (copy / f"{new_id}.md").write_text(new_text, encoding="utf-8")
+    (copy / "source.md").write_bytes(source.read_bytes())
+    return {"tmp_dir": tmp, "copy_dir": str(copy), "old_plan_sha256": _sha(plan)}
+
+
+# ------------------------------------------------------------------- archive
+def _contract_edit(text, key_values, item=None):
+    lines = text.split("\n")
+    ops = []
+    if item is not None:
+        _add_unresolved(lines, ops, item)
+    for k, v in key_values:
+        _set_key(lines, ops, k, v)
+    return "\n".join(lines), ops
+
+
+def archive(root, package, superseded_by):
+    root, tasks = _tasks(root)
+    pkg = Path(os.path.abspath(package))
+    old_id = _check_id(pkg.name, "package")
+    if os.path.realpath(pkg.parent) != str(tasks / "to-do"):
+        _fail("E-REMEDIATE-SOURCE", f"{pkg} is not a direct child of to-do/ in {root}")
+    if superseded_by != "none":
+        _check_id(superseded_by, "--superseded-by")
+    src, dst = tasks / "to-do" / old_id, tasks / "archive" / old_id
+    if not _real_dir(src):
+        _fail("E-REMEDIATE-SOURCE", f"{src} is not a real directory")
+    if os.path.lexists(dst):
+        _fail("E-REMEDIATE-CONFLICT", f"archive destination exists: {dst}; nothing changed")
+    helper = _load_helper()
+    contract = src / "return-contract.yaml"
+    undo_ops = []
+    created = not os.path.lexists(contract)
+    if created:
+        text = (
+            'contract_version: "1.1"\nstatus: partial\n'
+            f"slug: {old_id}\nplan_path: ./{old_id}.md\nsource_path: ./source.md\n"
+        )
+    else:
+        if os.path.islink(contract) or not contract.is_file():
+            _fail("E-REMEDIATE-CONTRACT", f"{contract} must be a regular file")
+        text = contract.read_text(encoding="utf-8")
+    had_marker = re.search("superseded", text, re.I) is not None
+    item = None
+    if not had_marker:
+        item = (
+            f"SUPERSEDED by {superseded_by}: do not run /sc:implement on this package."
+            if superseded_by != "none"
+            else "SUPERSEDED: replaced by a newer package; the replacement id is unrecorded."
+        )
+    kvs = [("superseded_by", superseded_by)] if superseded_by != "none" else []
+    new_text, undo_ops = _contract_edit(text, kvs, item)
+    made_artifacts = not os.path.lexists(src / "artifacts")
+    if not made_artifacts and not _real_dir(src / "artifacts"):
+        _fail("E-REMEDIATE-SOURCE", "artifacts must be a real directory")
+    os.makedirs(dst.parent, exist_ok=True)
+    _move(helper, src, dst)  # first mutation; fails closed with nothing moved
+    try:
+        if made_artifacts:
+            os.mkdir(dst / "artifacts")
+        record = {"created_contract": created, "made_artifacts": made_artifacts, "ops": undo_ops}
+        _write_new(dst / "artifacts" / UNDO_NAME, json.dumps(record) + "\n")
+        _write_atomic(dst / "return-contract.yaml", new_text)
+    except Exception as exc:
+        try:  # best effort: put the package back untouched
+            if made_artifacts and os.path.lexists(dst / "artifacts"):
+                for n in os.listdir(dst / "artifacts"):
+                    os.unlink(dst / "artifacts" / n)
+                os.rmdir(dst / "artifacts")
+            elif os.path.lexists(dst / "artifacts" / UNDO_NAME):
+                os.unlink(dst / "artifacts" / UNDO_NAME)
+            if created and os.path.lexists(dst / "return-contract.yaml"):
+                os.unlink(dst / "return-contract.yaml")
+            _move(helper, dst, src)
+        except Exception as back:
+            _fail("E-REMEDIATE-ARCHIVE", f"{exc}; rollback failed ({back}); package is at {dst}")
+        _fail("E-REMEDIATE-ARCHIVE", f"{exc}; rolled back, package is in to-do/")
+    return {"status": "archived", "path": str(dst), "added_unresolved": item is not None}
+
+
+def restore(root, old_id):
+    _check_id(old_id, "--old-id")
+    root, tasks = _tasks(root)
+    src, dst = tasks / "archive" / old_id, tasks / "to-do" / old_id
+    if not _real_dir(src):
+        _fail("E-REMEDIATE-SOURCE", f"{src} is not a real directory")
+    if os.path.lexists(dst):
+        _fail("E-REMEDIATE-CONFLICT", f"{dst} exists; nothing changed")
+    undo = src / "artifacts" / UNDO_NAME
+    if not undo.is_file():
+        _fail("E-REMEDIATE-RESTORE", f"{undo} missing; cannot undo archive")
+    try:
+        rec = json.loads(undo.read_text(encoding="utf-8"))
+    except ValueError as exc:
+        _fail("E-REMEDIATE-RESTORE", f"{undo} unreadable: {exc}")
+    contract = src / "return-contract.yaml"
+    restored = None
+    if not rec["created_contract"]:
+        lines = contract.read_text(encoding="utf-8").split("\n")
+        _undo_ops(lines, rec["ops"])
+        restored = "\n".join(lines)
+    helper = _load_helper()
+    _move(helper, src, dst)
+    pkg = dst
+    try:
+        if rec["created_contract"]:
+            os.unlink(pkg / "return-contract.yaml")
+        else:
+            _write_atomic(pkg / "return-contract.yaml", restored)
+        os.unlink(pkg / "artifacts" / UNDO_NAME)
+        if rec["made_artifacts"]:
+            os.rmdir(pkg / "artifacts")
+    except OSError as exc:
+        _fail("E-REMEDIATE-RESTORE", f"moved back to {pkg} but cleanup failed: {exc}")
+    return {"status": "restored", "path": str(pkg)}
+
+
+# ---------------------------------------------------------------------- mark
+def mark(package, review_fail=False, open_blockers=None, superseded_by=None,
+         fix_cycles=None, supersedes=None, route_name=None, finding_counts=None):
+    pkg = Path(package)
+    contract = pkg / "return-contract.yaml"
+    if os.path.islink(contract) or not contract.is_file():
+        _fail("E-REMEDIATE-CONTRACT", f"{contract} must be an existing regular file")
+    kvs = []
+    if review_fail:
+        ids = [x.strip() for x in (open_blockers or "").split(",") if x.strip()]
+        if not ids:
+            _fail("E-REMEDIATE-ARGS", "--review-fail needs --open-blockers <ids>")
+        kvs.append(("review_verdict", "FAIL"))
+        kvs.append(("open_blockers", json.dumps(ids)))
+    elif open_blockers is not None:
+        _fail("E-REMEDIATE-ARGS", "--open-blockers needs --review-fail")
+    if superseded_by is not None:
+        kvs.append(("superseded_by", _check_id(superseded_by, "--superseded-by")))
+    if fix_cycles is not None:
+        kvs.append(("fix_cycles", str(fix_cycles)))
+    if supersedes is not None or route_name is not None or finding_counts is not None:
+        if supersedes is None or route_name != "regenerate" or finding_counts is None:
+            _fail(
+                "E-REMEDIATE-ARGS",
+                "--supersedes, --route regenerate and --finding-counts go together",
+            )
+        kvs.append(("supersedes", _check_id(supersedes, "--supersedes")))
+        kvs.append(("remediation_route", route_name))
+        kvs.append(("finding_counts", _parse_counts(finding_counts)))
+    if not kvs:
+        _fail("E-REMEDIATE-ARGS", "mark has nothing to write")
+    new_text, _ = _contract_edit(contract.read_text(encoding="utf-8"), kvs)
+    _write_atomic(contract, new_text)
+    return {"status": "marked", "keys": [k for k, _ in kvs]}
+
+
+# --------------------------------------------------------------------- place
+def _diff_w(old_text, new_text):
+    a, b = old_text.splitlines(), new_text.splitlines()
+    na, nb = ["".join(x.split()) for x in a], ["".join(x.split()) for x in b]
+    sm = difflib.SequenceMatcher(None, na, nb, autojunk=False)
+    out = ["--- old-plan", "+++ new-plan"]
+    for group in sm.get_grouped_opcodes(3):
+        i1, i2, j1, j2 = group[0][1], group[-1][2], group[0][3], group[-1][4]
+        out.append(f"@@ -{i1 + 1},{i2 - i1} +{j1 + 1},{j2 - j1} @@")
+        for tag, a1, a2, b1, b2 in group:
+            if tag == "equal":
+                out += [" " + x for x in a[a1:a2]]
+            else:
+                out += ["-" + x for x in a[a1:a2]] + ["+" + x for x in b[b1:b2]]
+    return "\n".join(out) + ("\n" if len(out) > 2 else "")
+
+
+def place(root, old_id, new_id, copy_dir, finding_counts, review):
+    _check_id(old_id, "--old-id")
+    _check_id(new_id, "--new-id")
+    counts = _parse_counts(finding_counts)
+    root, tasks = _tasks(root)
+    leaf, old = tasks / "to-do" / new_id, tasks / "archive" / old_id
+    if not _real_dir(leaf):
+        _fail("E-REMEDIATE-LEAF", f"reserved leaf missing: {leaf}")
+    if os.listdir(leaf):
+        _fail("E-REMEDIATE-LEAF", f"reserved leaf is not empty: {leaf}")
+    if os.path.lexists(tasks / "to-do" / old_id) or not _real_dir(old):
+        _fail("E-REMEDIATE-SOURCE", f"{old_id} must be archived before place")
+    copy, rev = Path(copy_dir), Path(review)
+    new_plan, new_source = copy / f"{new_id}.md", copy / "source.md"
+    old_plan, old_source = old / f"{old_id}.md", old / "source.md"
+    for f in (new_plan, new_source, old_plan, old_source, rev):
+        if os.path.islink(f) or not f.is_file():
+            _fail("E-REMEDIATE-SOURCE", f"{f} must be a regular file")
+    new_text = new_plan.read_text(encoding="utf-8")
+    if not re.search(rf"^slug: {re.escape(new_id)}\s*$", new_text, re.M):
+        _fail("E-REMEDIATE-SOURCE", f"{new_plan} slug is not {new_id}")
+    old_text = old_plan.read_text(encoding="utf-8")
+    src_text = old_source.read_text(encoding="utf-8")
+    n = len(re.findall(r"^## Revision \d+", src_text, re.M)) + 1
+    fixmap = copy / "fixmap.md"
+    fix_text = fixmap.read_text(encoding="utf-8") if fixmap.is_file() else ""
+
+    _write_new(leaf / f"{new_id}.md", new_text)
+    revision = (
+        ("" if src_text.endswith("\n") else "\n")
+        + f"\n## Revision {n}\n\n"
+        f"- Replaces package: {old_id} (archived under .dev/tasks/archive/{old_id}/)\n"
+        f"- Review report: {rev}\n"
+        "- Fix map: ./artifacts/revision-log.md (diff: ./artifacts/plan.diff)\n"
+    )
+    _write_new(leaf / "source.md", src_text + revision)
+    (leaf / "artifacts").mkdir()
+    _write_new(leaf / "artifacts" / "plan.diff", _diff_w(old_text, new_text))
+    _write_new(leaf / "artifacts" / "prior-findings.md", rev.read_bytes())
+    _write_new(leaf / "artifacts" / "old-plan.md", old_plan.read_bytes())
+    log = (
+        f"# Revision {n} log\n\n- old package: {old_id}\n- new package: {new_id}\n"
+        f"- old plan sha256: {_sha(old_plan)}\n- review report: {rev}\n"
+        f"- finding_counts: {counts}\n"
+    )
+    if fix_text:
+        log += "\n## Fix map\n\n" + fix_text + ("" if fix_text.endswith("\n") else "\n")
+    _write_new(leaf / "artifacts" / "revision-log.md", log)
+    _write_new(
+        leaf / "return-contract.yaml",
+        'contract_version: "1.1"\n'
+        f"supersedes: {old_id}\nremediation_route: surgical\nfinding_counts: {counts}\n",
+    )
+    return {"status": "placed", "path": str(leaf)}
+
+
+def release(root, new_id):
+    _check_id(new_id, "--new-id")
+    root, tasks = _tasks(root)
+    leaf = tasks / "to-do" / new_id
+    if not os.path.lexists(leaf):
+        return {"status": "absent"}
+    if not _real_dir(leaf):
+        _fail("E-REMEDIATE-RELEASE", f"{leaf} is not a real directory")
+    allowed = {f.format(id=new_id) for f in PLACE_FILES}
+    files, dirs = [], []
+    for dp, dn, fn in os.walk(leaf, followlinks=False):
+        rel = Path(dp).relative_to(leaf)
+        for d in dn:
+            r = str(rel / d)
+            if r != "artifacts" or os.path.islink(Path(dp) / d):
+                _fail("E-REMEDIATE-RELEASE", f"{leaf / r} was not written by place; left alone")
+            dirs.append(Path(dp) / d)
+        for f in fn:
+            if str(rel / f) not in allowed:
+                _fail("E-REMEDIATE-RELEASE", f"{Path(dp) / f} was not written by place; left alone")
+            files.append(Path(dp) / f)
+    for f in files:
+        os.unlink(f)
+    for d in dirs:
+        os.rmdir(d)
+    os.rmdir(leaf)
+    return {"status": "released", "path": str(leaf)}
+
+
+# ----------------------------------------------------------------------- CLI
+def _cmd_reserve(a):
+    print(reserve(a.root, a.old_id))
+    return 0
+
+
+def _json(fn):
+    def run(a):
+        print(json.dumps(fn(a)))
+        return 0
+
+    return run
+
+
+def main(argv=None):
+    p = argparse.ArgumentParser(prog="remediate.py")
+    sub = p.add_subparsers(dest="command", required=True)
+
+    def add(name, fn, root=True):
+        s = sub.add_parser(name)
+        if root:
+            s.add_argument("--root", default=".", help="checkout root (default: cwd)")
+        s.set_defaults(func=fn)
+        return s
+
+    r = add("route", _cmd_route, root=False)
+    r.add_argument("--blocking", type=_count, required=True)
+    r.add_argument("--label-high", type=_count, required=True)
+    r.add_argument("--medium", type=_count, required=True)
+    r.add_argument("--regenerated-already", action="store_true")
+    r.add_argument("--forced", choices=ROUTES, default=None)
+
+    s = add("reserve", _cmd_reserve)
+    s.add_argument("--old-id", required=True)
+
+    s = add("prepare", _json(lambda a: prepare(a.root, a.old_id, a.new_id)))
+    s.add_argument("--old-id", required=True)
+    s.add_argument("--new-id", required=True)
+
+    s = add("archive", _json(lambda a: archive(a.root, a.package, a.superseded_by)))
+    s.add_argument("--package", required=True)
+    s.add_argument("--superseded-by", required=True, help="<new-id> or none")
+
+    s = add(
+        "place",
+        _json(lambda a: place(a.root, a.old_id, a.new_id, a.copy_dir, a.finding_counts, a.review)),
+    )
+    s.add_argument("--old-id", required=True)
+    s.add_argument("--new-id", required=True)
+    s.add_argument("--copy-dir", required=True)
+    s.add_argument("--finding-counts", required=True)
+    s.add_argument("--review", required=True)
+
+    s = add("restore", _json(lambda a: restore(a.root, a.old_id)))
+    s.add_argument("--old-id", required=True)
+
+    s = add(
+        "mark",
+        _json(
+            lambda a: mark(
+                a.package, a.review_fail, a.open_blockers, a.superseded_by,
+                a.fix_cycles, a.supersedes, a.route, a.finding_counts,
+            )
+        ),
+        root=False,
+    )
+    s.add_argument("--package", required=True)
+    s.add_argument("--review-fail", action="store_true")
+    s.add_argument("--open-blockers")
+    s.add_argument("--superseded-by")
+    s.add_argument("--fix-cycles", type=_count)
+    s.add_argument("--supersedes")
+    s.add_argument("--route", choices=("regenerate",))
+    s.add_argument("--finding-counts")
+
+    s = add("release", _json(lambda a: release(a.root, a.new_id)))
+    s.add_argument("--new-id", required=True)
+
+    args = p.parse_args(argv)
+    try:
+        return args.func(args)
+    except RemediateError as exc:
+        print(f"{exc.code}: {exc.msg}", file=sys.stderr)
+        return 1
+    except OSError as exc:
+        print(f"E-REMEDIATE-IO: {type(exc).__name__}: {exc}", file=sys.stderr)
+        return 1
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/src/superclaude/skills/sc-workflow-protocol/SKILL.md b/src/superclaude/skills/sc-workflow-protocol/SKILL.md
index 1a3675c76..f264428a5 100644
--- a/src/superclaude/skills/sc-workflow-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-workflow-protocol/SKILL.md
@@ -1,7 +1,7 @@
 ---
 name: sc:workflow-protocol
 description: "Behavioral protocol for /sc:workflow — PRD/spec to phased tasklist (<id>.md)"
-allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill, mcp__codegraph__codegraph_status, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_callees, mcp__codegraph__codegraph_impact
+allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Skill, Agent, Task, mcp__codegraph__codegraph_status, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_callees, mcp__codegraph__codegraph_impact
 argument-hint: "<path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--handoff none|design|implement]"
 ---
 
@@ -90,18 +90,26 @@ Final step of plan generation; runs only after Wave 3 passed, and **before** the
 
 Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) that call passes `--unattended --output <report-dir>/nested/reflect-<n>/` (reflect's own directory flag; workflow's `--output` stays retired; `<n>` counts from 1 and is never reused), still without `--remediate`, and the nested contract is listed in `artifacts`, also when the call failed.
 
-Advisory and read-only: never edit, delete, or regenerate `<id>.md` from findings, and never change the workflow `status` because of them. Reflect unavailable or `failed` → `reflect_status: skipped|failed`, `reflect_report_path: null`, one `unresolved` line; still proceed to Wave 5.
+This call itself is advisory: the plan is changed only by Wave 4R, only for blocking findings and only on a copy, never in place, and findings never change the workflow `status`. Never overwrite an existing package. Reflect unavailable or `failed` → `reflect_status: skipped|failed`, `reflect_report_path: null`, one `unresolved` line; still proceed to Wave 5.
+
+## Wave 4R — Remediate
+
+**Ref:** `refs/remediation.md`
+
+Runs after Wave 4 by default (`--remediate none` records the counts and the chosen route and changes nothing; `--remediate surgical|regenerate` forces a route; `--revise <package-dir> --review <REPORT.md>` runs it for a package reviewed outside workflow). Read `finding_counts` from the Wave 4 reflect contract, run `remediate.py route` (`~/.claude/skills/sc-workflow-protocol/scripts/remediate.py`, project copy `.claude/skills/sc-workflow-protocol/scripts/remediate.py` second) and follow the chosen route of the ref: `none` changes nothing; `surgical` repairs a copy and places it as a new package after archiving the original; `regenerate` runs Waves 0 to 3 once more (at most once per run); `escalate` stops and marks the package `review_verdict: FAIL`. Only blocking findings are repaired, at most 2 fix cycles.
+
+File operations of this wave: `mktemp -d /tmp/sc-workflow-revise.XXXXXXXX`, and every copy and move through `remediate.py` only (no `mv`, `cp` or `rm` by hand). The reviser and the re-reviewer are sub-agents started with the Agent tool (Task is the same tool under its other name).
 
 ## Wave 5 — Contract
 
 **Refs:** `refs/return-contract.md`, `refs/overlap-routing.md`
 
-Write `<pkg>/return-contract.yaml` (contract 1.1: stable `slug`, `./<id>.md`, `./source.md`, `reflect_*`) **before** any `implement` handoff. Apply handoff; a failed `implement` handoff on a valid plan is `partial`, a failed generation is `failed`.
+Write `return-contract.yaml` (contract 1.1: stable `slug`, `./<id>.md`, `./source.md`, `reflect_*`) into the **final placed package** (never into an archived one) **before** any `implement` handoff. Wave 5 merges into the contract that `place` and `mark` already wrote and never replaces the file: it creates the contract when none exists (route `none`), sets `status`, `reflect_*`, `handoff_*` and `unresolved`, fills every stable 1.1 field still missing (`slug`, `plan_path`, `source_path`, `source_origin`, `strategy`, `depth`) and keeps every line of `supersedes`, `remediation_route`, `finding_counts`, `fix_cycles`, `review_verdict` and `open_blockers`. `report_path` and the printed plan path name the final placed plan. The archived package's contract is written only by `remediate.py archive` and `mark`. Apply handoff; a failed `implement` handoff on a valid plan is `partial`, a failed generation is `failed`.
 
 After an `implement` handoff the package may have moved to `done/` (executor-owned archive). Resolve the actual location by id (`.dev/tasks/to-do/<id>` vs `.dev/tasks/done/<id>`, `test -e || test -L`): only if the package still exists at `to-do/` may you rewrite the contract (e.g. to `partial`), and never recreate a directory or write into a path whose package is absent. Only `done/` exists → leave the archived contract untouched, report the failure/outcome in chat, print the actual `done/` plan path. Both exist → mutate neither and report the conflict. Print the plan path at its actual location.
 
 ## Will / Will Not
 
-**Will:** one new package `.dev/tasks/to-do/<id>/` with `<id>.md`, `source.md`, `return-contract.yaml`; ground the plan in the real code through codegraph when the index is fresh. Never overwrites or reuses an existing package. Run `/sc:reflect --mode pre` (advisory) on the gated plan as the final generation step, before any handoff.
+**Will:** one new package `.dev/tasks/to-do/<id>/` with `<id>.md`, `source.md`, `return-contract.yaml`; ground the plan in the real code through codegraph when the index is fresh. Never overwrites or reuses an existing package. Run `/sc:reflect --mode pre` (advisory) on the gated plan as the final generation step, before any handoff. Then Wave 4R: repair blocking findings on a copy and place it as a new package, archiving the one it replaces.
 
-**Will Not:** product code, new agents, Task fan-out; modify the plan from reflect findings.
+**Will Not:** product code, new agents, Task fan-out (except the Wave 4R reviser and re-reviewer sub-agents); edit a plan in place, or change a plan for a Medium or Note finding.
diff --git a/tests/skills/test_workflow_remediation.py b/tests/skills/test_workflow_remediation.py
index c3f4d1ba0..6b6838872 100644
--- a/tests/skills/test_workflow_remediation.py
+++ b/tests/skills/test_workflow_remediation.py
@@ -461,3 +461,23 @@ def test_cli_reserve_prepare_archive_flow(repo):
     assert a.returncode == 0 and json.loads(a.stdout)["status"] == "archived"
     bad = _run("archive", "--root", str(repo), "--package", str(pkg), "--superseded-by", "none")
     assert bad.returncode == 1 and "E-REMEDIATE" in bad.stderr
+
+
+_SKILL_DIR = _SCRIPT.parents[1]
+
+
+def test_wave5_merges_into_existing_contract_and_keeps_review_verdict():
+    skill = (_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
+    contract = (_SKILL_DIR / "refs/return-contract.md").read_text(encoding="utf-8")
+    wave5 = skill.split("## Wave 5", 1)[1].split("## Will / Will Not", 1)[0]
+    assert "merges into the contract that `place` and `mark` already wrote" in wave5
+    assert "never replaces the file" in wave5
+    assert "final placed package" in wave5
+    assert "`review_verdict`" in wave5.split("keeps every line of", 1)[1]
+    assert "every rewrite merges into the existing file" in contract
+    assert "`review_verdict`" in contract.split("keeps every other line", 1)[1]
+    assert skill.index("## Wave 4R") < skill.index("## Wave 5")
+    assert skill.index("## Wave 4 ") < skill.index("## Wave 4R")
+    assert "never edit, delete, or regenerate" not in skill
+    head = skill.split("---", 2)[1]
+    assert "Agent" in head and "Task" in head


Codegraph context: index_state: fresh; checked_at: 2026-11-20T02:48:46Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-624; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-624
call codegraph only when index_state: fresh, never to widen scope
(Q2b dependents not in the diff: none recorded; Grep/Read floor used.)
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
