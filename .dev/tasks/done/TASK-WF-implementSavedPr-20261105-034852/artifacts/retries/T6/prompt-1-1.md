339e7e4ae63fc7970b5f7f8d60ad3be7fbab61b5
Review one task for spec compliance.

Task brief: T6 (AC ids in order of the "Acceptance criteria:" bullets: T6.AC1,T6.AC2,T6.AC3,T6.AC4). Plan file: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/TASK-WF-implementSavedPr-20261105-034852.md, lines 92-102:
## Task 6: Check the nine earlier prompts with a script that sees the defect, and add the note file

Depends on: Task 5

Write `./artifacts/prompt-check.py` (run with `PYTHONDONTWRITEBYTECODE=1 uv run python -I`). It takes the reviewer template from `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (the fenced block under "## Subagent prompt (when not inline)" that begins "Review one task for spec compliance.") and a prompt path. Line 1 of every saved prompt is the task's start sha: the script checks that line 1 is 40 hex characters (or `nogit`) and equals the value of the "Start sha:" slot, then drops it; a prompt whose line 1 fails that check prints `differs`. It then locates the seven slot labels ("Task brief:", "Global constraints:", "Start sha:", "Diff against the start snapshot:", "Delta diff from the previous reviewed tree (empty on the first review):", "Earlier blocking findings of this start (empty on the first review):", "Saved-probe re-check hit locations (may be empty):") in order, each as the first line after the previous label that starts with that label, and removes the slot contents: a slot is the text after its label on the label line plus the following lines up to the last non-blank line before the next label, and the last slot ends at the last non-blank line before the line "Do not trust the implementer's report.", so the blank lines before that line are outside the slot. It compares everything else on the template and on the prompt, including both junctions (the template's first line, then a blank line, then "Task brief:"; and the last slot label line, then a blank line, then "Do not trust the implementer's report." to the end). It prints one line per prompt: `match` when the remainder is byte-equal to the template's, `blank-line-only` when it is equal after dropping blank lines and trailing whitespace but not byte-equal, otherwise `differs`. Run it on each of `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1/prompt-1-1.md` through `.../T9/prompt-1-1.md` and save the output as `./artifacts/t6-prompt-check.txt`. Run it also on four self-test prompts kept under `./artifacts/` and save the outputs as `./artifacts/t6-selftest.txt`: a synthetic template-exact prompt with a start-sha line 1 and the seven slots filled (expected `match`); the same prompt with the blank line before "Do not trust the implementer's report." removed (expected `blank-line-only`); a copy of the T1 prompt with one non-blank template line changed (expected `differs`); a copy of the T1 prompt with line 1 replaced by a non-sha line (expected `differs`). Before writing the note file save `git ls-files -s -- .dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403` as `./artifacts/t6-index-before.txt`. Then add `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/prompt-template-check.md` stating the result per prompt, that under rule A (`refs/qa.md`, "## FINAL derived test") a blank-line-only difference is a note, and where the evidence is: this package's `./artifacts/prompt-check.py` and `./artifacts/t6-prompt-check.txt` by their package-relative paths, saying this package lives under `.dev/tasks/to-do/` until archived and under `.dev/tasks/done/` after. Run `git add .dev/tasks` and save `git ls-files -s -- .dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403` as `./artifacts/t6-index-after.txt`.

Acceptance criteria:
- `./artifacts/t6-prompt-check.txt` has nine lines, one per T1 to T9 prompt, each `blank-line-only`; if a prompt prints anything else, the note file reports that actual result and the difference found.
- `./artifacts/t6-selftest.txt` shows, in order, `match`, `blank-line-only`, `differs` and `differs` for the four self-test prompts.
- `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/prompt-template-check.md` exists, states the per-prompt results matching `./artifacts/t6-prompt-check.txt`, and names the evidence by package-relative path with the to-do and done note.
- `diff ./artifacts/t6-index-before.txt ./artifacts/t6-index-after.txt`, saved as `./artifacts/t6-index-diff.txt`, shows only the one added line for `artifacts/prompt-template-check.md`.

Global constraints: (plan ## Constraints, .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/TASK-WF-implementSavedPr-20261105-034852.md lines 17-27)
## Constraints

- Rule changes go only in `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, `src/superclaude/skills/sc-implement-protocol/refs/ledger.md` and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`, each with a byte-identical copy at the same relative path under `plugins/superclaude/skills/sc-implement-protocol/`. No other skill, command, agent or core file changes, and the reviewer template block (the fenced block that begins "Review one task for spec compliance." under "## Subagent prompt (when not inline)" in `refs/qa.md`) and the `ledger-grammar-block` fenced blocks in `refs/ledger.md` do not change.
- `tests/skills/test_implement_severity_static.py` is not modified. Its classification test fails on any line in the protocol files that matches the words `Ruling` (capital R), `halt`, `halts`, `halted`, `halting`, `E-HALT-QA` or `E-ARCHIVE-BLOCKED` and is not already listed there, so every new or rewritten line in the three refs avoids those words (say "a user-accepted gap" and "stop"), and additions to step 6 of `refs/managed-workspace.md` stay inside the existing single step-6 line. The existing wording "`issues` → STOP `E-ARCHIVE-BLOCKED`" stays verbatim.
- A prompt-builder script, any other lesson in `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md`, and the globally installed copy of this skill (it changes when the user runs `superclaude install`) are out of scope.
- Never stage `.claude/` contents. `make sync-dev` copies `src/superclaude/` into `.claude/` only and does not touch `plugins/`, so each task copies its edited ref into the `plugins/` twin by hand, and Task 5 runs `make sync-dev` once after all edits to `src/superclaude/`.
- Installed primitives (the three refs above) must not tell an agent to read anything through a `src/superclaude/...` path.
- In `.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/`, only the new file `artifacts/prompt-template-check.md` is added; its prompts, ledger and every other file stay byte-unchanged.
- Scripts and evidence for this plan go under this package's `./artifacts/`.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `artifacts/` included. Staging is not committing; commit only when the user asks.


Start sha: 339e7e4ae63fc7970b5f7f8d60ad3be7fbab61b5
Diff against the start snapshot: (git diff 339e7e4ae63fc7970b5f7f8d60ad3be7fbab61b5 -- .dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/prompt-template-check.md, plus the task's new artifact files under .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/ listed after the diff)
diff --git a/.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/prompt-template-check.md b/.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/prompt-template-check.md
new file mode 100644
index 00000000..698efb39
--- /dev/null
+++ b/.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/prompt-template-check.md
@@ -0,0 +1,33 @@
+# Saved reviewer prompts of this package compared with the reviewer template
+
+This note was added after the package was archived. It changes nothing else in the package: the prompts, the ledger and every other file are byte-unchanged.
+
+## Result
+
+The first-round prompt of each task (`artifacts/retries/T1/prompt-1-1.md` to `artifacts/retries/T9/prompt-1-1.md`) was compared with the reviewer template in `refs/qa.md` ("## Subagent prompt (when not inline)"). The check drops line 1 (the start sha, checked against the "Start sha:" slot), cuts out the seven slots and compares the rest with the template.
+
+| Prompt | Result |
+|---|---|
+| T1 `prompt-1-1.md` | blank-line-only |
+| T2 `prompt-1-1.md` | blank-line-only |
+| T3 `prompt-1-1.md` | blank-line-only |
+| T4 `prompt-1-1.md` | blank-line-only |
+| T5 `prompt-1-1.md` | blank-line-only |
+| T6 `prompt-1-1.md` | blank-line-only |
+| T7 `prompt-1-1.md` | blank-line-only |
+| T8 `prompt-1-1.md` | blank-line-only |
+| T9 `prompt-1-1.md` | blank-line-only |
+
+All nine match the template outside the slots on every non-blank line. They differ only in blank lines: each has blank lines between the slot labels where the template has none, and the blank line before "Do not trust the implementer's report." is missing.
+
+## What this means
+
+Under rule A (`refs/qa.md`, "## FINAL derived test"), a difference only in blank lines or trailing whitespace is a note, not `issues`. No non-blank line of any of the nine prompts differs from the template.
+
+## Evidence
+
+The evidence is in the package `TASK-WF-implementSavedPr-20261105-034852`. That package lives under `.dev/tasks/to-do/` until it is archived and under `.dev/tasks/done/` afterwards:
+
+- `artifacts/prompt-check.py`: the comparison script.
+- `artifacts/t6-prompt-check.txt`: its output for the nine prompts above.
+- `artifacts/t6-selftest.txt`: its output for four self-test prompts (`match`, `blank-line-only`, `differs`, `differs`), which show that the script tells these cases apart.

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/prompt-check.py ===
"""Compare saved /sc:implement reviewer prompts with the reviewer template.

Usage (from the repository root):
    PYTHONDONTWRITEBYTECODE=1 uv run python -I <this file> <prompt path> [<prompt path> ...]

Prints one line per prompt: "<path> <class>", where class is
    match            the prompt equals the template outside the slots, byte for byte
    blank-line-only  it equals the template after dropping blank lines and trailing
                     whitespace, but not byte for byte
    differs          anything else (also: line 1 is not the start sha, a slot label is
                     missing or out of order, or the closing line is missing)

Rules follow refs/qa.md "## FINAL derived test" (saved prompts): line 1 of a saved
prompt is the task's start sha and is dropped after it is checked against the
"Start sha:" slot; the slots are cut out; the rest is compared with the template.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

QA = Path("src/superclaude/skills/sc-implement-protocol/refs/qa.md")
HEADING = "## Subagent prompt (when not inline)"
FIRST_LINE = "Review one task for spec compliance."
CLOSING = "Do not trust the implementer's report."
LABELS = (
    "Task brief:",
    "Global constraints:",
    "Start sha:",
    "Diff against the start snapshot:",
    "Delta diff from the previous reviewed tree (empty on the first review):",
    "Earlier blocking findings of this start (empty on the first review):",
    "Saved-probe re-check hit locations (may be empty):",
)
SHA_RE = re.compile(r"^(?:[0-9a-f]{40}|nogit)$")


def template_lines() -> list[str]:
    lines = QA.read_text(encoding="utf-8").splitlines()
    h = lines.index(HEADING)
    fences = [i for i in range(h + 1, len(lines)) if lines[i].startswith("```")]
    block = lines[fences[0] + 1 : fences[1]]
    if not block or block[0] != FIRST_LINE:
        raise SystemExit(f"template block does not begin with {FIRST_LINE!r}")
    return block


def cut_slots(lines: list[str]) -> tuple[list[str], str] | None:
    """Return (lines with slot contents removed, value of the 'Start sha:' slot)."""
    positions: list[int] = []
    at = 0
    for label in LABELS:
        found = next((i for i in range(at, len(lines)) if lines[i].startswith(label)), None)
        if found is None:
            return None
        positions.append(found)
        at = found + 1
    closing = next((i for i in range(positions[-1] + 1, len(lines)) if lines[i] == CLOSING), None)
    if closing is None:
        return None
    out = list(lines[: positions[0]])
    sha_value = ""
    for n, label in enumerate(LABELS):
        limit = positions[n + 1] if n + 1 < len(LABELS) else closing
        end = max(i for i in range(positions[n], limit) if lines[i].strip())
        if label == "Start sha:":
            sha_value = lines[positions[n]][len(label) :].strip()
        out.append(label)
        out.extend(lines[end + 1 : limit])
    out.extend(lines[closing:])
    return out, sha_value


def classify(prompt: Path, template: list[str]) -> str:
    text = prompt.read_text(encoding="utf-8").removesuffix("\n")
    lines = text.split("\n")
    first, rest = lines[0], lines[1:]
    cut = cut_slots(rest)
    if cut is None or not SHA_RE.match(first):
        return "differs"
    remainder, sha_value = cut
    if first != sha_value:
        return "differs"
    expected = cut_slots(template)
    if expected is None:
        raise SystemExit("template has no complete slot layout")
    want = expected[0]
    if remainder == want:
        return "match"
    squeeze = lambda ls: [x.rstrip() for x in ls if x.strip()]  # noqa: E731
    return "blank-line-only" if squeeze(remainder) == squeeze(want) else "differs"


def main(paths: list[str]) -> int:
    template = template_lines()
    for p in paths:
        print(f"{p} {classify(Path(p), template)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/make-selftests.py ===
"""Write the four self-test prompts for prompt-check.py into this folder.

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 uv run python -I <this file>
"""

from __future__ import annotations

from pathlib import Path

HERE = Path(".dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts")
QA = Path("src/superclaude/skills/sc-implement-protocol/refs/qa.md")
T1 = Path(".dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1/prompt-1-1.md")
SHA = "0123456789abcdef0123456789abcdef01234567"


def template() -> list[str]:
    lines = QA.read_text(encoding="utf-8").splitlines()
    h = lines.index("## Subagent prompt (when not inline)")
    f = [i for i in range(h + 1, len(lines)) if lines[i].startswith("```")]
    return lines[f[0] + 1 : f[1]]


SLOTS = {
    "{task_brief}": "T1 (AC ids: T1.AC1)\n## Task 1: synthetic\n\nAcceptance criteria:\n- synthetic",
    "{global_constraints}": "(synthetic)\n- a synthetic constraint",
    "{start_sha}": SHA,
    "{diff}": "(synthetic diff)\n+added line\n\n+another added line",
    "{delta_diff}": "",
    "{prior_findings}": "",
    "{recheck_list}": "",
}


def exact() -> str:
    out: list[str] = []
    for line in template():
        for key, value in SLOTS.items():
            if key in line:
                line = line.replace(key, value)
        out.append(line)
    return SHA + "\n" + "\n".join(out) + "\n"


def main() -> None:
    body = exact()
    (HERE / "selftest-1-exact.md").write_text(body, encoding="utf-8")

    closing = "Do not trust the implementer's report."
    lines = body.split("\n")
    i = lines.index(closing)
    assert lines[i - 1] == ""
    (HERE / "selftest-2-blank-line-removed.md").write_text("\n".join(lines[: i - 1] + lines[i:]), encoding="utf-8")

    t1 = T1.read_text(encoding="utf-8")
    old = "Anchor rule: cite exactly one anchor per yes."
    assert t1.count(old) == 1
    (HERE / "selftest-3-changed-line.md").write_text(t1.replace(old, "Anchor rule: cite one anchor per yes."), encoding="utf-8")

    rest = t1.split("\n", 1)[1]
    (HERE / "selftest-4-no-sha-line.md").write_text("this is not a start sha\n" + rest, encoding="utf-8")


if __name__ == "__main__":
    main()

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t6-prompt-check.txt ===
.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1/prompt-1-1.md blank-line-only
.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T2/prompt-1-1.md blank-line-only
.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T3/prompt-1-1.md blank-line-only
.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T4/prompt-1-1.md blank-line-only
.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T5/prompt-1-1.md blank-line-only
.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T6/prompt-1-1.md blank-line-only
.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T7/prompt-1-1.md blank-line-only
.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T8/prompt-1-1.md blank-line-only
.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T9/prompt-1-1.md blank-line-only

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t6-selftest.txt ===
.dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/selftest-1-exact.md match
.dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/selftest-2-blank-line-removed.md blank-line-only
.dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/selftest-3-changed-line.md differs
.dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/selftest-4-no-sha-line.md differs

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t6-index-before.txt ===
100644 a6326c63d742bdd5259955ddb8807b88cbe27725 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md
100644 e7f1013b189a1b7879d334b06f2b457c0cf6eb83 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1/notes.md
100644 3a34d6a202fcc139ddfa6ab3e56208c3ee761d4d 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1/q0-head
100644 9f6ebdbaaa7653029316fd26968ad40e37faf9d3 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T2/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T2/q0-head
100644 a078a936d6a788f4a5a6d5f32b2e60d42c88daea 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T3/notes.md
100644 3378da671a53ae9ea43dc65578b81ac9db453e45 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T3/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T3/q0-head
100644 353393ab2c3b68c22076eac2d61e5be3e91074a5 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T4/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T4/q0-head
100644 3293496623578daed9921aba217eec526f848e37 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T5/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T5/q0-head
100644 a5ee0ba521ac4267d493dc3f6ae446e950197d5e 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T6/notes.md
100644 cb228396c148ce1dd5474bdc058ee569b49ead83 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T6/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T6/q0-head
100644 64122b954b01ad8ff4f5f735dd4d3ccf5fc1c1ab 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T7/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T7/q0-head
100644 5e2272ffbac9f53bb198fe44d76ac12769e26860 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T8/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T8/q0-head
100644 604d2c79cacd6d48b26dd0bd719af790a4849306 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T9/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T9/q0-head
100644 3538faea9e78fd1661558e78c5af7cb21c6e0aef 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t1-ask-check.txt
100644 c4cf95af7224adde032c2746c13ac61737f4c405 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t1-extras-tests-docs.log
100644 bb5318617ba330d4d9965c19005950e7dab87bd1 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t2-core-evidence.txt
100644 ea8bb760820845a819c522a701633a2ed534084a 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t3-ready-table.txt
100644 e759f5b89f8b6fedd71e7de2012c28d7b409d225 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t4-ask-check.txt
100644 e47eec170ef535dea1266f141c6ae7dfa6849fe4 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t6-test-identifiers.txt
100644 1ed3f42b9fcc6d5342f0b470cac9db7f149cefaf 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-changed-files.txt
100644 0c799cedff0158fc93e54bee360503378bb2c40a 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check-before.txt
100644 65a2c4446771b6290b08d110b46d304a4ba44cc4 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.py
100644 f207b6038306f7af1a09ce32a7ff6b3b89b13f44 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.txt
100644 a97a8c969cd69e233f56e41193a618c1f3163100 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-stale-fences.txt
100644 35124a11b1b98c31d0a57ae3627f08b25f538ccf 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-ask-check.txt
100644 e343e024f47a152b8b36f574bad36c8092d9597a 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-changed-files.txt
100644 a02837766a3af469c141b81db039bfd69931fe28 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-dash-check.txt
100644 62d1a1f6da7f78d83698fd4421bc35429542d933 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-one-home.txt
100644 0c9a90951e67c7c5c74282ba4f57cc4f787895fd 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-pytest-core.txt
100644 b4104bc28ba93b376681ebc841ede835ee41767f 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-pytest.txt
100644 39c1e8e99d9c05ef7d58a4ec3f6204be0748bab4 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/progress.md
100644 72539e83a49e70ec5accdd7435c7967a2e66a590 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/return-contract.yaml
100644 02b9ede85f840862c753895804ef266bb3ea3b1b 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/source.md

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t6-index-after.txt ===
100644 a6326c63d742bdd5259955ddb8807b88cbe27725 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/TASK-WF-devGuideRefactor-20261104-135403.md
100644 698efb39e204844e20d8b3454e5d5caac151ffba 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/prompt-template-check.md
100644 e7f1013b189a1b7879d334b06f2b457c0cf6eb83 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1/notes.md
100644 3a34d6a202fcc139ddfa6ab3e56208c3ee761d4d 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T1/q0-head
100644 9f6ebdbaaa7653029316fd26968ad40e37faf9d3 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T2/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T2/q0-head
100644 a078a936d6a788f4a5a6d5f32b2e60d42c88daea 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T3/notes.md
100644 3378da671a53ae9ea43dc65578b81ac9db453e45 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T3/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T3/q0-head
100644 353393ab2c3b68c22076eac2d61e5be3e91074a5 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T4/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T4/q0-head
100644 3293496623578daed9921aba217eec526f848e37 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T5/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T5/q0-head
100644 a5ee0ba521ac4267d493dc3f6ae446e950197d5e 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T6/notes.md
100644 cb228396c148ce1dd5474bdc058ee569b49ead83 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T6/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T6/q0-head
100644 64122b954b01ad8ff4f5f735dd4d3ccf5fc1c1ab 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T7/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T7/q0-head
100644 5e2272ffbac9f53bb198fe44d76ac12769e26860 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T8/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T8/q0-head
100644 604d2c79cacd6d48b26dd0bd719af790a4849306 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T9/prompt-1-1.md
100644 e84378295b120cbe679ed4328c325ab184b10d57 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/retries/T9/q0-head
100644 3538faea9e78fd1661558e78c5af7cb21c6e0aef 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t1-ask-check.txt
100644 c4cf95af7224adde032c2746c13ac61737f4c405 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t1-extras-tests-docs.log
100644 bb5318617ba330d4d9965c19005950e7dab87bd1 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t2-core-evidence.txt
100644 ea8bb760820845a819c522a701633a2ed534084a 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t3-ready-table.txt
100644 e759f5b89f8b6fedd71e7de2012c28d7b409d225 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t4-ask-check.txt
100644 e47eec170ef535dea1266f141c6ae7dfa6849fe4 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t6-test-identifiers.txt
100644 1ed3f42b9fcc6d5342f0b470cac9db7f149cefaf 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-changed-files.txt
100644 0c799cedff0158fc93e54bee360503378bb2c40a 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check-before.txt
100644 65a2c4446771b6290b08d110b46d304a4ba44cc4 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.py
100644 f207b6038306f7af1a09ce32a7ff6b3b89b13f44 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-fence-check.txt
100644 a97a8c969cd69e233f56e41193a618c1f3163100 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t8-stale-fences.txt
100644 35124a11b1b98c31d0a57ae3627f08b25f538ccf 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-ask-check.txt
100644 e343e024f47a152b8b36f574bad36c8092d9597a 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-changed-files.txt
100644 a02837766a3af469c141b81db039bfd69931fe28 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-dash-check.txt
100644 62d1a1f6da7f78d83698fd4421bc35429542d933 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-one-home.txt
100644 0c9a90951e67c7c5c74282ba4f57cc4f787895fd 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-pytest-core.txt
100644 b4104bc28ba93b376681ebc841ede835ee41767f 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/t9-pytest.txt
100644 39c1e8e99d9c05ef7d58a4ec3f6204be0748bab4 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/progress.md
100644 72539e83a49e70ec5accdd7435c7967a2e66a590 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/return-contract.yaml
100644 02b9ede85f840862c753895804ef266bb3ea3b1b 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/source.md

=== new untracked file in the touched set: .dev/tasks/to-do/TASK-WF-implementSavedPr-20261105-034852/artifacts/t6-index-diff.txt ===
1a2
> 100644 698efb39e204844e20d8b3454e5d5caac151ffba 0	.dev/tasks/done/TASK-WF-devGuideRefactor-20261104-135403/artifacts/prompt-template-check.md

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
