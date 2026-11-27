d6d39a5a21f486256e8fb4a481adf7410a06bcfc
Review one task for spec compliance.

Task brief: ## Task 8: Write the README

Depends on: Task 5, Task 6, Task 7

Create `.dev/research/jev-vs-keyword-table-611/README.md` and `.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py`.

`README.md` explains:
- what the experiment decides and what it does not;
- the folder layout of the design (one job per file, including `spend.py`);
- the offline test command;
- the order of work, with the command of each step: rule AGREED, the six question definitions read once by a person and recorded with `events.py owner-input --evidence <questions.py path> --note "<who read the six definitions>"` (finding M-2), corpus and labels frozen with `gate.py freeze-corpus`, `gate.py gate1`, the table answers and `gate.py freeze-table`, the owner's answers to the open rule fields recorded with `events.py owner-input`, `gate.py freeze-rule`, the re-confirmed price recorded with `events.py price`, the harness tests recorded with `gate.py record-tests`, the lead's go recorded with `events.py go`, `gate.py gate2`, `runner.py rehearse`, the coordinator's live `runner.py run --live` with `keyscan.py` run with explicit paths and the real key sourced inside one subshell command only as rule J2 describes (the keyscan command, like the live run, sets `JEV_API_KEY` from `TYPESAFE_API_KEY` inside the same single subshell command, for example `export JEV_API_KEY="$TYPESAFE_API_KEY"` inside one `bash -c '...'`, never prints or echoes it, never puts it on a command line and never writes it to a file) (finding M-11), and `scorer.py score`;
- how to rescore: `scorer.py score --run-id ID --rescore NAME --rule PATH` writes only under `rescores/NAME/`, is labelled non-decisional and never changes the root report, the decision record or an event;
- the open items and who answers each: the Noul band operators, the unresolved-failure count, who labels, who applies the table, the live route through the vendor URL or the gateway (the ops guide `docs/docs-product/ops/jev-litellm-gateway-operational-guide.md` says the vendor key is held by the gateway), the price to re-confirm before Gate 2, and where the prompts come from;
- a "Delivery status" section listing parts A to E of section 8 of the design, who does each and whether it is done, and the sentence the pull request must carry: `Refs #611`, with parts B to E listed as left;
- the rule that an implementer session never calls the live API.

`test_readme.py` reads the subcommand names from the argument parsers of `gate.py`, `events.py`, `runner.py` and `scorer.py` and checks that each appears in the README next to its script name.

Acceptance criteria:
- `README.md` contains the exact test command `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v` and the live-run steps in the order above, and `test_readme.py` passes, showing every subcommand of the four command lines is named in the README.
- `README.md` has a "how to rescore" section, a "Delivery status" section with the `Refs #611` sentence and the list of parts B to E, and names every open item above with the person or session that answers it.
- The README names the reading step immediately before `gate.py freeze-corpus`, and `table-procedure.md` names the same step (finding M-2).
- Running the full test command from the repository root passes with all tests from Tasks 1 to 8.
- The README's `keyscan.py` step names the mapping of `JEV_API_KEY` from `TYPESAFE_API_KEY` inside the same single subshell command (finding M-11).
- `git status --short` with every entry under `.dev/research/jev-vs-keyword-table-611/` removed equals `./artifacts/baseline-status.txt`, and no path under `src/`, `tests/`, `.claude/` or `.dev/research/346-review-loop-experiments/` appears in `git status --short`.
- A test runs each of `gate.py`, `events.py`, `runner.py` and `scorer.py` as a script with `--help` from an unrelated working directory and sees it start (finding M-12).

Acceptance criterion ids (in source order):
T8.AC1: `README.md` contains the exact test command `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v` and the live-run steps in the order above, and `test_readme.py` passes, showing every subcommand of the four command lines is named in the README.
T8.AC2: `README.md` has a "how to rescore" section, a "Delivery status" section with the `Refs #611` sentence and the list of parts B to E, and names every open item above with the person or session that answers it.
T8.AC3: The README names the reading step immediately before `gate.py freeze-corpus`, and `table-procedure.md` names the same step (finding M-2).
T8.AC4: Running the full test command from the repository root passes with all tests from Tasks 1 to 8.
T8.AC5: The README's `keyscan.py` step names the mapping of `JEV_API_KEY` from `TYPESAFE_API_KEY` inside the same single subshell command (finding M-11).
T8.AC6: `git status --short` with every entry under `.dev/research/jev-vs-keyword-table-611/` removed equals `./artifacts/baseline-status.txt`, and no path under `src/`, `tests/`, `.claude/` or `.dev/research/346-review-loop-experiments/` appears in `git status --short`.
T8.AC7: A test runs each of `gate.py`, `events.py`, `runner.py` and `scorer.py` as a script with `--help` from an unrelated working directory and sees it start (finding M-12).
Global constraints: ## Constraints

- Scope is build and test only. No task sends a prompt to TypeSafe, reads `TYPESAFE_API_KEY` or `JEV_API_KEY` from the real environment, or opens a network connection. Tests use `MockTransport` and a socket guard, set a fake key with `monkeypatch.setenv`, and use a temporary experiment root for every file the gates, events, runner and scorer write. The live run is a coordinator action under rule J2 of `.dev/research/346-review-loop-experiments/p15/plans/SHARED-CONTRACT.md` (lines 145 to 165).
- Left for a person or the coordinator, not in this plan: choosing and labelling about 30 public prompts (a named human labeller is required), applying the keyword table to them (a session or person who sees prompts only, after Gate 1), the live run with `keyscan.py`, scoring and the report, and the updates on issues 611, 609 and 612. Tasks 7 and 8 produce the procedures, templates and instructions those steps need. The pull request that delivers this plan says `Refs #611` and lists parts B to E of section 8 of the design as left (Task 8 puts that sentence in the README).
- Nothing under `src/`, `tests/`, `.claude/` or the existing `.dev/research/346-review-loop-experiments/p15/jev/jevlib/` folder is changed. `jevlib` is imported read-only, and only from its submodules (`client`, `budget`, `journal`, `transport`, `questions`, `manifest`, `config`), because `jevlib/__init__.py` exports only `MODEL`, `API_URL` and `KEY_ENV`.
- Spend cap is 1 dollar in total; public prompts only; the key is never printed, logged, written to a file, put on a command line or put in a pull request. The runner copies `TYPESAFE_API_KEY` into `JEV_API_KEY` inside its own process only, because `jevlib.config.KEY_ENV` is `JEV_API_KEY`.
- Agreed decision rule (AGREED 2026-11-26 by the IronFlow session and the build agent, relayed by the lead; Clay's own words as quoted by the IronFlow session, not typed by Clay: "you and the agent debate whats correct way to handle this and do it").
- Margin: an exact one-sided sign test on the prompts where only one arm is right. b is the count right only for Jev; c is the count right only for the table. Jev passes when 20 times the sum of comb(b+c, k) for k from b to b+c is below 2 to the power b+c, in integer arithmetic. Checked cases: 5-0 passes, 4-0 fails, 7-1 passes, 6-1 fails, 8-2 fails (56/1024 is 0.0547), 9-2 passes, and b+c of 0 is not clearly.
- Right: a typed label is right when the answer is that type; an `ambiguous` or `none-fit` label is right when the answer is unset. Same for both arms. An unset answer on a typed label is not right.
- Latency: measured on the client from sending the request to receiving the full response, per attempt. The median over each prompt's final answered attempt must be 2 seconds or less. The slowest over all attempts, with a timeout counted at its timeout value, must be 5 seconds or less. Per-call timeout is 10 seconds. The 90th percentile by nearest rank is reported.
- Failures: one rerun per failed prompt, never a rerun of the whole run. Both attempts are logged and counted against the cap. A prompt that fails twice is an `error`, is not right for Jev, and is never scored as a "no".
- Verdict: `JEV_BEATS_TABLE` only when the run is valid, the margin test passes and both latency limits hold. `NOT_CLEARLY` for a valid run that does not. `RUN_INVALID` with a reason otherwise. `RUN_INVALID` makes no build or close decision on issue 612.
- Still open, so written as `UNSET` in the rule file: the operators at exactly 0.3 and 0.7 for the Noul band, and the count of unresolved failures that makes a run invalid. Gate 1 accepts `UNSET` and does not freeze the rule file's hash. The scorer, the `freeze-rule` command and Gate 2 refuse any `UNSET` value, and `freeze-rule` is the step that freezes the rule file's hash after the owner has filled the fields.
- The real client behaves differently from a mock-backed dry run: `JevClient` with `live=False` builds, screens and budgets the request, then returns `refused` with error `dry_run` before any transport call. So the runner has two subcommands: `run` needs `--live`, both gates and the key; `rehearse` never posts and needs no gate and no key. Tests that need the transport path use `live=True`, an injected `MockTransport` and a fake `JEV_API_KEY`.
- Test run command, recorded by `gate.py record-tests`: `uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v`. The repository's `testpaths` is `tests`, so tests under `.dev/` are only collected when this path is given.
- Each of the four command-line modules (`gate.py`, `events.py`, `runner.py` and `scorer.py`) inserts the existing `jevlib` folder and the experiment folder into `sys.path` itself, as `.dev/research/346-review-loop-experiments/p15/jev/probe.py` does (read-only reference), because only `conftest.py` does so for tests (finding M-12).
Start sha: d6d39a5a21f486256e8fb4a481adf7410a06bcfc
Diff against the start snapshot: diff --git a/.dev/research/jev-vs-keyword-table-611/README.md b/.dev/research/jev-vs-keyword-table-611/README.md
new file mode 100644
index 000000000..277b0cf38
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/README.md
@@ -0,0 +1,110 @@
+# Jev against the keyword table (issue 611)
+
+This folder holds the offline measuring harness for step 2 of the Jev preflight (issue 611, part of issue 609): does the Jev model beat the
+keyword table in the troubleshoot skill at choosing the problem type of a prompt, by a margin larger than the noise on about 30 labelled
+prompts, and fast enough to sit in front of `/sc:troubleshoot`?
+
+**What it decides:** one of three verdicts, by a rule written down before any prompt is sent: `JEV_BEATS_TABLE`, `NOT_CLEARLY`, or
+`RUN_INVALID` (with the reason). The build-or-close decision on issue 612 is made only from a valid run.
+**What it does not decide:** it does not choose or label the prompts, apply the table, or call the live API. People and the coordinator do
+those steps (see the order of work and the Delivery status below). Building and testing this harness sends nothing anywhere.
+
+**Rule for implementer sessions:** an implementer session never calls the live API and never reads the key. The live run is a coordinator
+action under rule J2 of `.dev/research/346-review-loop-experiments/p15/plans/SHARED-CONTRACT.md`.
+
+## Folder layout (one job per file)
+
+| File | Its one job |
+|---|---|
+| `decision-rule.md` | Every policy value of the experiment, with the verbatim agreement; three values are still `UNSET` |
+| `questions.py` | The only place Jev question wording lives |
+| `harness/loader.py` | Where every file lives, hashing, and reading the rule file, corpus and table answers |
+| `harness/spend.py` | The only code that estimates tokens or turns a price and a cap into a ceiling |
+| `harness/events.py` | The append-only event log, and the commands that record owner input, the price and the lead's go |
+| `harness/gate.py` | The manifest (write-once hashes) and the two gates that keep every live call closed |
+| `harness/runner.py` | One live run on `JevClient`, and a rehearsal that never posts |
+| `harness/scorer.py` | The decision rule as pure functions, the scoring pipeline, the verdict, the report and the decision record |
+| `harness/tests/` | The offline tests (mock transport, a socket guard, a temporary root for every file written) |
+| `corpus/` | `selection-criteria.md` and `labelling-record.md` (forms), then `corpus.jsonl` once a person has made it |
+| `table/` | `table-procedure.md` (how the table is applied), `table-provenance.md` (a form), then `table-answers.jsonl` |
+| `manifest.json`, `events.jsonl`, `ledger/`, `runs/<run-id>/` | Written by the commands below, never by hand |
+| `report.md`, `decision-record.md`, `rescores/` | Written by `scorer.py` |
+
+## Offline test command
+
+Run from the repository root (the repository's `testpaths` is `tests`, so tests under `.dev/` are collected only when this path is given):
+
+```bash
+uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v
+```
+
+## Order of work
+
+Every command is run from the repository root. Write `GATE`, `EVENTS`, `RUNNER` and `SCORER` for
+`uv run python .dev/research/jev-vs-keyword-table-611/harness/gate.py`, `.../events.py`, `.../runner.py` and `.../scorer.py`. Each command
+takes `--root` (the experiment folder by default).
+
+1. **Rule AGREED.** `decision-rule.md` holds the agreed rule (26 Nov 2026), with three values still `UNSET` (see Open items).
+2. **Read the six definitions once** (a person), then record it. This step comes immediately before `gate.py freeze-corpus`:
+   `events.py owner-input --evidence .dev/research/jev-vs-keyword-table-611/questions.py --note "<who read the six definitions>"`
+3. **Corpus and labels frozen** (a named human labeller has filled `corpus/corpus.jsonl`, `corpus/selection-criteria.md` and
+   `corpus/labelling-record.md`): `gate.py freeze-corpus`. It runs the privacy screen and refuses on any failure.
+4. **Gate 1:** `gate.py gate1`. It accepts `UNSET` rule values and hashes files only.
+5. **Table answers** are applied as `table/table-procedure.md` says (prompts only, after Gate 1), then frozen: `gate.py freeze-table`.
+6. **The owner's answers to the open rule fields** are written into `decision-rule.md` and recorded:
+   `events.py owner-input --evidence .dev/research/jev-vs-keyword-table-611/decision-rule.md --note "<who answered, and the three values>"`
+7. **Freeze the rule:** `gate.py freeze-rule`. It refuses any `UNSET` value.
+8. **Re-confirm the price** on the vendor page and record it: `events.py price --usd-per-mtok <value> --source "<where it was read>"`.
+9. **Record the offline test run:** `gate.py record-tests` (it runs the test command above and stores the hash of every code file).
+10. **The lead's go**, naming the rule file's hash: `events.py go --words "<the lead's words>"`.
+11. **Gate 2:** `gate.py gate2`. It fails on any missing step, any changed frozen file, a spend bound that does not fit, or a run already started.
+12. **Rehearse** (posts nothing, needs no gate and no key): `runner.py rehearse --out <a folder outside ledger/ and runs/>`.
+13. **The coordinator's live run:** `runner.py run --run-id <ID> --live`. It checks both gates itself and reads no environment variable before
+    they pass. The key is mapped from `TYPESAFE_API_KEY` to `JEV_API_KEY` inside one subshell command only (rule J2), never printed, never put on a
+    command line and never written to a file. The key scan sets `JEV_API_KEY` from `TYPESAFE_API_KEY` inside the same single subshell command and
+    names its paths explicitly:
+
+    ```bash
+    bash -c 'export JEV_API_KEY="$TYPESAFE_API_KEY"; uv run python .dev/research/346-review-loop-experiments/p15/jev/keyscan.py .dev/research/jev-vs-keyword-table-611/runs/<ID> .dev/research/jev-vs-keyword-table-611/events.jsonl .dev/research/jev-vs-keyword-table-611/manifest.json .dev/research/jev-vs-keyword-table-611/ledger/spend.json'
+    ```
+
+    It must print `KEYSCAN OK`. The live run command has the same form: `bash -c 'cd <repo> && uv run python .../runner.py run --run-id <ID> --live'`
+    in a shell where `TYPESAFE_API_KEY` is available to that one command.
+14. **Score:** `scorer.py score --run-id <ID>`. It refuses while any rule value is `UNSET`, writes `report.md` and `decision-record.md` for every
+    verdict, appends the `scoring` and `verdict` events, and never overwrites an existing report. Run the key scan again over the two new files.
+
+## How to rescore
+
+`scorer.py score --run-id ID --rescore NAME --rule PATH` scores the same run under another rule file. It writes only
+`rescores/NAME/report.md`, labels it non-decisional, and never changes the root report, the decision record or an event. It refuses a
+name that already exists.
+
+## Open items and who answers each
+
+| Item | Who answers | Recommendation of the build agent |
+|---|---|---|
+| `noul_low_operator` (`lt` or `le`) | The owner, through the lead | `le`. It changes only the reason label of an unset answer, not the score. |
+| `noul_high_operator` (`gt` or `ge`) | The owner, through the lead | `gt`: Jev answers only when its Noul value is above 0.7, so the band 0.3 to 0.7 is all abstention. |
+| `unresolved_failure_invalid_count` | The owner, through the lead | `3` (about a tenth of 30 prompts). The scorer reads it as the count at which a run becomes invalid: a run with that many prompts that failed twice, or more, is `RUN_INVALID`. A value of 0 would make every run invalid. |
+| Who labels the prompts | The lead names a human labeller | none: a named person is required |
+| Who applies the table | The lead names a session or person that sees prompts only and is not the labeller | none |
+| The live route: the vendor URL, or the LiteLLM gateway through `JEV_API_URL` | The lead and the coordinator | none: `docs/docs-product/ops/jev-litellm-gateway-operational-guide.md` says the vendor key is held by the gateway, so check which route `TYPESAFE_API_KEY` belongs to first |
+| The price to re-confirm before Gate 2 (the `jevlib` constant is 0.042 USD per million input tokens, read 2026-11-10) | The coordinator | none |
+| Where the prompts come from (public sources only) | The person who selects them, listed in `corpus/selection-criteria.md` | none |
+
+The rule file stays `UNSET` in the repository until the owner answers; the recommendations above are the build agent's, recorded in the
+story's Decided block and the pull request. The lead's go names the hash of the rule file as it stands when the values are filled in.
+
+## Delivery status
+
+Parts A to E of section 8 of the design (`.dev/brainstorms/20261126-jev-vs-keyword-table-611/design-spec.md`):
+
+| Part | Who | Done? |
+|---|---|---|
+| A. Harness: loader, gate, scorer, runner, events, tests, the rule file with the AGREED rule, this README | Implementer, offline | Yes, delivered by this pull request, with the table and corpus templates |
+| B. Corpus and labels: about 30 public prompts, provenance, human labels, label basis, freeze | A named human labeller | No, left |
+| C. Table answers | A separate session or person given prompts only, after Gate 1 | No, left |
+| D. Live run, key scan, scoring, report | The coordinator, after Gate 2 and the lead's go | No, left |
+| E. Issue updates on 611, 609 and 612 | The coordinator | No, left |
+
+The pull request that delivers this carries the sentence: `Refs #611`, with parts B, C, D and E listed as left.
diff --git a/.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py
new file mode 100644
index 000000000..85f495f01
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py
@@ -0,0 +1,105 @@
+import contextlib
+import io
+import re
+import subprocess
+import sys
+
+import pytest
+from harness import events, gate, loader, runner, scorer
+
+EXP = loader.EXPERIMENT
+REPO = EXP.parents[2]
+README = (EXP / "README.md").read_text(encoding="utf-8")
+PROCEDURE = (EXP / "table" / "table-procedure.md").read_text(encoding="utf-8")
+SCRIPTS = {"gate": gate, "events": events, "runner": runner, "scorer": scorer}
+READING = "owner-input --evidence .dev/research/jev-vs-keyword-table-611/questions.py"
+
+
+def subcommands(module):
+    """The subcommand names, read from the module's own argument parser through its ``--help`` output."""
+    out = io.StringIO()
+    with contextlib.redirect_stdout(out), pytest.raises(SystemExit):
+        module.main(["--help"])
+    found = re.search(r"\{([a-z0-9,-]+)\}", out.getvalue())
+    assert found, f"{module.__name__} shows no subcommand list"
+    return found.group(1).split(",")
+
+
+def order_of_work():
+    section = README.split("## Order of work")[1].split("## How to rescore")[0]
+    return re.split(r"(?m)^(?=\d+\. )", section)[1:]
+
+
+@pytest.mark.parametrize("script", sorted(SCRIPTS))
+def test_every_subcommand_is_named_in_the_readme_next_to_its_script(script):
+    names = subcommands(SCRIPTS[script])
+    assert names
+    for sub in names:
+        assert f"{script}.py {sub}" in README, f"{script}.py {sub} is not in the README"
+
+
+def test_the_readme_has_the_exact_test_command():
+    assert "uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v" in README
+
+
+def test_the_live_run_steps_are_in_the_order_the_story_names():
+    expected = ["decision-rule.md", READING, "gate.py freeze-corpus", "gate.py gate1", "gate.py freeze-table",
+                "owner-input --evidence .dev/research/jev-vs-keyword-table-611/decision-rule.md", "gate.py freeze-rule",
+                "events.py price", "gate.py record-tests", "events.py go", "gate.py gate2", "runner.py rehearse", "runner.py run",
+                "scorer.py score"]
+    steps = order_of_work()
+    assert len(steps) == len(expected)
+    for number, (step, token) in enumerate(zip(steps, expected), 1):
+        assert token in step, f"step {number} does not hold {token}"
+    assert "keyscan.py" in steps[12]
+
+
+def test_the_reading_step_comes_right_before_freeze_corpus_in_the_readme_and_the_procedure():
+    steps = order_of_work()
+    assert READING in steps[1] and "six definitions" in steps[1] and "immediately before `gate.py freeze-corpus`" in steps[1]
+    assert "gate.py freeze-corpus" in steps[2] and READING not in steps[2]
+    assert "Reading step, before `gate.py freeze-corpus`" in PROCEDURE and READING in PROCEDURE
+    assert PROCEDURE.index("Reading step") < PROCEDURE.index("Gate 1 first")
+
+
+def test_the_keyscan_step_maps_the_key_inside_the_same_single_subshell_command():
+    block = next(b for b in re.findall(r"```bash\n(.*?)```", README, re.S) if "keyscan.py" in b)
+    assert block.count("bash -c") == 1 and 'export JEV_API_KEY="$TYPESAFE_API_KEY"' in block
+    assert block.index("bash -c") < block.index("export JEV_API_KEY") < block.index("keyscan.py")
+    assert not re.search(r"JEV_API_KEY=[^\"$ ]", README)
+
+
+def test_the_readme_has_the_rescore_section_the_delivery_status_and_every_open_item():
+    assert "## How to rescore" in README and "scorer.py score --run-id ID --rescore NAME --rule PATH" in README
+    status = README.split("## Delivery status")[1]
+    assert "`Refs #611`" in status
+    for part in ("B.", "C.", "D.", "E."):
+        assert re.search(rf"\| {re.escape(part)} .*\| No, left", status), part
+    for item in ("noul_low_operator", "noul_high_operator", "unresolved_failure_invalid_count", "Who labels", "Who applies the table",
+                 "JEV_API_URL", "jev-litellm-gateway-operational-guide.md", "price to re-confirm", "Where the prompts come from"):
+        assert item in README, item
+    assert "never calls the live API" in README
+
+
+def test_the_procedure_quotes_the_table_exactly_as_the_skill_file_has_it():
+    skill = (REPO / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / "SKILL.md").read_text(encoding="utf-8").splitlines()
+    start = next(i for i, line in enumerate(skill) if line.startswith("   - Stack trace, exception name"))
+    quoted = "\n".join(skill[start:start + 7])                     # the six cue rows and the ambiguity rule
+    assert skill[start + 6].lstrip().startswith("- On ambiguity")
+    assert quoted in PROCEDURE
+
+
+@pytest.mark.parametrize("script", sorted(SCRIPTS))
+def test_each_command_line_module_starts_as_a_script_from_an_unrelated_folder(script, tmp_path):
+    path = EXP / "harness" / f"{script}.py"
+    res = subprocess.run([sys.executable, "-I", str(path), "--help"], cwd=tmp_path, capture_output=True, text=True,
+                         env={"PATH": "/usr/bin:/bin", "PYTHONDONTWRITEBYTECODE": "1"})
+    assert res.returncode == 0 and "usage:" in res.stdout, res.stderr
+
+
+def test_no_readme_or_template_holds_a_vendor_url_or_a_key_shaped_string():
+    for f in [EXP / "README.md", *sorted((EXP / "table").glob("*.md")), *sorted((EXP / "corpus").glob("*.md"))]:
+        t = f.read_text(encoding="utf-8")
+        assert "api.typesafe.ai" not in t and "sk-" not in t, f
+        prose = re.sub(r"`[^`]*`", " ", re.sub(r"```.*?```", " ", t, flags=re.S))      # a long word outside code spans looks like a key
+        assert not re.search(r"\b[A-Za-z0-9_-]{32,}\b", prose), f
diff --git a/.dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t8-test.log b/.dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t8-test.log
new file mode 100644
index 000000000..e6885b1aa
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t8-test.log
@@ -0,0 +1,202 @@
+============================= test session starts ==============================
+platform linux -- Python 3.10.20, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-611/.venv/bin/python
+SuperClaude: 6.1.0
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-611
+configfile: pyproject.toml
+plugins: anyio-4.16.0, superclaude-6.1.0
+collecting ... collected 190 items
+
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate1_passes_after_the_corpus_is_frozen_and_accepts_unset_values PASSED [  0%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate1_refuses_before_anything_is_frozen PASSED [  1%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate1_refuses_each_rule_file_defect[<lambda>-rule_status0] PASSED [  1%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate1_refuses_each_rule_file_defect[<lambda>-rule_status1] PASSED [  2%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate1_refuses_each_rule_file_defect[<lambda>-rule_provenance_empty0] PASSED [  2%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate1_refuses_each_rule_file_defect[<lambda>-rule_provenance_empty1] PASSED [  3%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate1_refuses_each_rule_file_defect[<lambda>-rule_provenance_empty2] PASSED [  3%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate1_refuses_each_rule_file_defect[<lambda>-rule_provenance_empty3] PASSED [  4%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate1_refuses_a_missing_rule_file PASSED [  4%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_either_gate_refuses_a_changed_corpus_side_file[corpus-hash_corpus] PASSED [  5%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_either_gate_refuses_a_changed_corpus_side_file[selection_criteria-hash_selection_criteria] PASSED [  5%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_either_gate_refuses_a_changed_corpus_side_file[labelling_record-hash_labelling_record] PASSED [  6%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_either_gate_refuses_a_changed_corpus_side_file[questions_py-hash_questions] PASSED [  6%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate2_passes_on_a_complete_synthetic_setup PASSED [  7%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate2_refuses_a_missing_step[go-go_missing] PASSED [  7%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate2_refuses_a_missing_step[tests-tests_not_recorded] PASSED [  8%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate2_refuses_a_missing_step[rule-rule_not_frozen] PASSED [  8%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate2_refuses_a_missing_step[price-price_not_confirmed] PASSED [  9%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate2_refuses_a_missing_step[table-hash_table_answers] PASSED [ 10%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate2_refuses_a_go_that_names_an_old_rule_hash PASSED [ 10%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate2_refuses_an_unset_value PASSED [ 11%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate2_refuses_a_changed_rule_table_answers_provenance_code_or_jevlib_file PASSED [ 11%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate2_refuses_when_a_run_already_started_or_ended[first_request] PASSED [ 12%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gate2_refuses_when_a_run_already_started_or_ended[run_end] PASSED [ 12%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_spend_bound_fails_when_each_request_fits_but_the_whole_run_does_not PASSED [ 13%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_spend_bound_fails_when_the_worst_case_at_a_high_price_is_above_the_cap PASSED [ 13%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_gates_hash_files_only_and_never_call_the_corpus_loader PASSED [ 14%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_the_manifest_is_unchanged_by_either_gate PASSED [ 14%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_a_second_freeze_of_each_kind_is_refused_and_keeps_the_frozen_value PASSED [ 15%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_the_manifest_holds_the_hashes_and_the_model_pin PASSED [ 15%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_freeze_rule_refuses_an_unset_value PASSED [ 16%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_freeze_table_refuses_until_gate1_passes_and_when_a_file_is_missing PASSED [ 16%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_freeze_corpus_refuses_a_corpus_the_screen_refuses PASSED [ 17%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_record_tests_refuses_a_failing_or_empty_run[result0-failed] PASSED [ 17%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_record_tests_refuses_a_failing_or_empty_run[result1-no tests] PASSED [ 18%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_record_tests_records_the_command_count_and_hashes PASSED [ 18%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_the_recorded_test_command_is_the_repo_relative_form_the_plan_names PASSED [ 19%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_the_gate_command_line_returns_one_on_a_failure_and_zero_on_a_pass PASSED [ 20%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_events_are_appended_never_rewritten_and_carry_time_path_and_hash PASSED [ 20%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_every_event_kind_the_setup_writes_carries_a_time_a_path_and_a_hash PASSED [ 21%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_an_evidence_path_that_is_not_a_file_is_refused PASSED [ 21%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_events_refuse_an_unknown_name_and_a_reserved_field PASSED [ 22%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_the_three_event_commands_write_their_events PASSED [ 22%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_the_price_command_refuses_a_price_of_zero PASSED [ 23%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_spend_estimates_follow_the_client_formula PASSED [ 23%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_gate_events.py::test_spend_ceiling_and_worst_case_follow_the_price PASSED [ 24%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_committed_rule_loads_and_only_the_three_open_fields_may_be_unset PASSED [ 24%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_committed_rule_holds_the_verbatim_agreement_and_marks_the_owner_words_relayed PASSED [ 25%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_rule_refuses_a_status_other_than_agreed[PROPOSED] PASSED [ 25%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_rule_refuses_a_status_other_than_agreed[PENDING] PASSED [ 26%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_rule_refuses_an_empty_agreement_text PASSED [ 26%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_rule_refuses_an_empty_who_when_or_words[agreed_by] PASSED [ 27%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_rule_refuses_an_empty_who_when_or_words[agreed_at] PASSED [ 27%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_rule_refuses_an_empty_who_when_or_words[relayed_owner_words] PASSED [ 28%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_rule_refuses_a_missing_key_and_a_missing_file PASSED [ 28%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_rule_refuses_scoring_while_a_value_is_unset_and_accepts_it_when_all_are_set PASSED [ 29%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_rule_refuses_an_operator_that_does_not_fit_its_edge PASSED [ 30%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_a_valid_corpus_loads PASSED [ 30%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_corpus_rejects_each_rule_break[<lambda>-no public source] PASSED [ 31%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_corpus_rejects_each_rule_break[<lambda>-duplicate corpus id] PASSED [ 31%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_corpus_rejects_each_rule_break[<lambda>-same text] PASSED [ 32%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_corpus_rejects_each_rule_break[<lambda>-outside the allowed set] PASSED [ 32%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_corpus_rejects_each_rule_break[<lambda>-no row labelled deployment] PASSED [ 33%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_corpus_rejects_each_rule_break[<lambda>-no row labelled ambiguous] PASSED [ 33%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_corpus_rejects_each_rule_break[<lambda>-no row labelled none-fit] PASSED [ 34%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_corpus_refuses_a_prompt_the_privacy_screen_refuses_without_echoing_it[see https://github.com/example/project/issues/4 for details-github_url] PASSED [ 34%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_corpus_refuses_a_prompt_the_privacy_screen_refuses_without_echoing_it[the file is at /home/someone/project/main.py-path_home] PASSED [ 35%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_table_answers_load_and_need_a_prompt_id PASSED [ 35%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_paths_on_a_temporary_root_stay_under_it_except_jevlib PASSED [ 36%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_jevlib_files_are_the_top_level_py_files_only PASSED [ 36%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_loader.py::test_sha256_file_is_the_sha256_of_the_bytes PASSED [ 37%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py::test_request_builds_and_is_stable PASSED [ 37%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py::test_choice_has_exactly_the_six_types PASSED [ 38%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py::test_noul_has_true_and_false_criteria PASSED [ 38%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py::test_only_two_questions_in_a_fixed_order PASSED [ 39%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py::test_questions_file_copies_none_of_the_tables_cue_phrases PASSED [ 40%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py::test_socket_guard_fails_a_connection_attempt PASSED [ 40%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_questions.py::test_real_state_snapshot_reports_an_edit_of_an_existing_nested_file PASSED [ 41%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_every_subcommand_is_named_in_the_readme_next_to_its_script[events] PASSED [ 41%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_every_subcommand_is_named_in_the_readme_next_to_its_script[gate] PASSED [ 42%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_every_subcommand_is_named_in_the_readme_next_to_its_script[runner] PASSED [ 42%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_every_subcommand_is_named_in_the_readme_next_to_its_script[scorer] PASSED [ 43%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_the_readme_has_the_exact_test_command PASSED [ 43%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_the_live_run_steps_are_in_the_order_the_story_names PASSED [ 44%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_the_reading_step_comes_right_before_freeze_corpus_in_the_readme_and_the_procedure PASSED [ 44%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_the_keyscan_step_maps_the_key_inside_the_same_single_subshell_command PASSED [ 45%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_the_readme_has_the_rescore_section_the_delivery_status_and_every_open_item PASSED [ 45%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_the_procedure_quotes_the_table_exactly_as_the_skill_file_has_it PASSED [ 46%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_each_command_line_module_starts_as_a_script_from_an_unrelated_folder[events] PASSED [ 46%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_each_command_line_module_starts_as_a_script_from_an_unrelated_folder[gate] PASSED [ 47%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_each_command_line_module_starts_as_a_script_from_an_unrelated_folder[runner] PASSED [ 47%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_each_command_line_module_starts_as_a_script_from_an_unrelated_folder[scorer] PASSED [ 48%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_readme.py::test_no_readme_or_template_holds_a_vendor_url_or_a_key_shaped_string PASSED [ 48%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_a_failed_first_attempt_gets_exactly_one_rerun PASSED [ 49%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_a_prompt_that_fails_twice_is_an_error_with_exactly_two_posts PASSED [ 50%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_a_timeout_is_rerun_and_is_not_a_stop PASSED [ 50%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_a_missing_key_ends_the_run_with_zero_posts PASSED [ 51%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_a_rejected_key_ends_the_run_after_one_post PASSED [ 51%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_a_returned_model_other_than_the_pin_ends_the_run_after_one_post PASSED [ 52%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_a_budget_exhausted_result_stops_the_run_with_no_rerun PASSED [ 52%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_a_ledger_where_every_request_fits_but_the_whole_run_does_not_gives_zero_posts PASSED [ 53%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_a_completed_run_leaves_nothing_reserved_and_spend_carries_across_runs PASSED [ 53%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_a_higher_confirmed_price_lowers_the_token_ceiling PASSED [ 54%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_limits_set_and_restore_the_client_settings_also_after_an_exception PASSED [ 54%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_a_failing_gate_leaves_the_key_and_url_variables_unread PASSED [ 55%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_run_without_live_exits_two_before_any_gate PASSED [ 55%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_run_refuses_an_existing_run_folder PASSED [ 56%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_run_passes_the_gates_then_copies_the_key_and_never_prints_it PASSED [ 56%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_run_without_a_key_refuses_after_the_gates PASSED [ 57%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_rehearse_never_posts_and_leaves_the_real_files_alone PASSED [ 57%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_rehearse_refuses_a_folder_under_the_ledger_or_runs PASSED [ 58%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_rehearse_through_the_command_line_needs_no_gate_and_no_key PASSED [ 58%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_no_written_file_holds_the_key_even_when_an_error_body_quotes_it PASSED [ 59%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_the_run_record_exists_after_a_completed_and_after_a_stopped_run PASSED [ 60%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_an_unexpected_error_still_writes_the_run_record_and_the_run_end_event PASSED [ 60%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_runner.py::test_runner_holds_no_url_literal_and_posts_only_through_the_client PASSED [ 61%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_right_for_a_typed_label PASSED [ 61%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_right_for_an_unset_label_needs_an_unset_answer[ambiguous] PASSED [ 62%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_right_for_an_unset_label_needs_an_unset_answer[none-fit] PASSED [ 62%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_right_refuses_an_unknown_label PASSED [ 63%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_sign_test_passes_for_the_agreed_cases[5-0] PASSED [ 63%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_sign_test_passes_for_the_agreed_cases[7-1] PASSED [ 64%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_sign_test_passes_for_the_agreed_cases[9-2] PASSED [ 64%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_sign_test_fails_for_the_agreed_cases[4-0] PASSED [ 65%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_sign_test_fails_for_the_agreed_cases[6-1] PASSED [ 65%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_sign_test_fails_for_the_agreed_cases[8-2] PASSED [ 66%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_sign_test_fails_for_the_agreed_cases[0-0] PASSED [ 66%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_sign_test_fails_for_the_agreed_cases[0-7] PASSED [ 67%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_sign_test_fails_for_the_agreed_cases[3-9] PASSED [ 67%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_smallest_passing_b_for_each_c_from_0_to_6 PASSED [ 68%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_sign_test_agrees_with_an_exact_fraction_reference_up_to_30 PASSED [ 68%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_sign_test_reads_the_factor_from_the_rule PASSED [ 69%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_jev_answer_at_and_around_both_edges[gt-lt] PASSED [ 70%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_jev_answer_at_and_around_both_edges[gt-le] PASSED [ 70%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_jev_answer_at_and_around_both_edges[ge-lt] PASSED [ 71%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_jev_answer_at_and_around_both_edges[ge-le] PASSED [ 71%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_jev_answer_refuses_an_unset_or_misplaced_operator[UNSET-ge] PASSED [ 72%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_jev_answer_refuses_an_unset_or_misplaced_operator[le-UNSET] PASSED [ 72%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_jev_answer_refuses_an_unset_or_misplaced_operator[gt-ge] PASSED [ 73%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_jev_answer_refuses_an_unset_or_misplaced_operator[le-lt] PASSED [ 73%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_median_of_odd_and_even_counts_and_empty PASSED [ 74%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_nearest_rank_percentile PASSED [ 74%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_timeout_counts_at_the_cap_in_the_slowest_and_is_left_out_of_the_median PASSED [ 75%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_a_prompt_that_never_answered_is_not_in_the_answered_only_population PASSED [ 75%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_the_include_timeouts_population_counts_a_timeout_at_the_cap PASSED [ 76%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_latency_stats_on_no_attempts_are_none_and_an_unknown_population_is_refused PASSED [ 76%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_core.py::test_scorer_has_no_floating_point_comparison_at_the_agreed_line PASSED [ 77%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_jev_beats_the_table_when_margin_and_latency_hold PASSED [ 77%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_margin_boundary_five_nil_passes_and_four_nil_fails PASSED [ 78%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_median_limit_boundary[1.5-JEV_BEATS_TABLE] PASSED [ 78%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_median_limit_boundary[1.6-NOT_CLEARLY] PASSED [ 79%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_slowest_limit_boundary_counts_every_attempt[4.5-JEV_BEATS_TABLE] PASSED [ 80%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_slowest_limit_boundary_counts_every_attempt[4.6-NOT_CLEARLY] PASSED [ 80%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_a_timeout_counts_at_its_cap_in_the_slowest PASSED [ 81%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_not_clearly_names_every_failed_test PASSED [ 81%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_each_meta_reason_makes_the_run_invalid[change0-gate_result_missing] PASSED [ 82%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_each_meta_reason_makes_the_run_invalid[change1-gate_result_missing] PASSED [ 82%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_each_meta_reason_makes_the_run_invalid[change2-second_live_run] PASSED [ 83%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_each_meta_reason_makes_the_run_invalid[change3-table_answers_changed] PASSED [ 83%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_each_meta_reason_makes_the_run_invalid[change4-frozen_file_changed] PASSED [ 84%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_each_meta_reason_makes_the_run_invalid[change5-frozen_file_changed] PASSED [ 84%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_each_meta_reason_makes_the_run_invalid[change6-table_provenance_missing] PASSED [ 85%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_each_meta_reason_makes_the_run_invalid[change7-key_rejected] PASSED [ 85%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_each_meta_reason_makes_the_run_invalid[change8-model_mismatch] PASSED [ 86%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_each_meta_reason_makes_the_run_invalid[change9-stopped_before_all_prompts] PASSED [ 86%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_each_meta_reason_makes_the_run_invalid[change10-stopped_before_all_prompts] PASSED [ 87%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_a_returned_model_other_than_the_pin_is_a_model_mismatch PASSED [ 87%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_fewer_rows_than_prompts_is_stopped_before_all_prompts PASSED [ 88%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_a_run_with_no_answered_prompt_is_invalid PASSED [ 88%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_unresolved_failures_at_the_limit_make_the_run_invalid PASSED [ 89%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_the_first_failed_check_wins_and_every_reason_is_reachable PASSED [ 90%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_paired_breakdown_and_disagreements_match_a_hand_count PASSED [ 90%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_typed_and_unset_label_split PASSED [ 91%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_a_pass_resting_only_on_the_unset_label_prompts_is_flagged PASSED [ 91%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_accuracy_with_and_without_the_prompts_the_table_saw PASSED [ 92%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_a_twice_failed_prompt_is_not_right_and_stays_in_the_denominator PASSED [ 92%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_a_rerun_that_answers_is_counted_as_recovered PASSED [ 93%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_an_unset_operator_is_refused_by_the_scorer PASSED [ 93%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_render_report_is_deterministic_and_names_the_verdict PASSED [ 94%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_the_decision_record_names_the_issues_the_rule_hash_and_the_612_statement_for_each_verdict PASSED [ 94%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_no_stand_in_value_of_these_tests_is_in_the_committed_rule_file PASSED [ 95%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_score_writes_the_report_and_the_decision_record_and_the_two_events PASSED [ 95%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_a_second_score_run_refuses_to_overwrite_the_root_report PASSED [ 96%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_score_refuses_and_writes_no_verdict_while_a_rule_value_is_unset PASSED [ 96%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_a_run_that_cannot_be_scored_is_refused_without_a_report PASSED [ 97%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_a_changed_table_answers_file_gives_a_report_with_run_invalid PASSED [ 97%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_run_meta_reads_the_events_and_the_manifest PASSED [ 98%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_a_rescore_writes_only_under_rescores_and_changes_nothing_else PASSED [ 98%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_rescore_needs_both_flags_and_a_plain_name PASSED [ 99%]
+.dev/research/jev-vs-keyword-table-611/harness/tests/test_scorer_report.py::test_the_report_text_for_the_real_paths_is_free_of_a_key_or_prompt_text PASSED [100%]
+
+============================= 190 passed in 1.72s ==============================
+--- ruff
+All checks passed!
diff --git a/.dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t8-status-check.txt b/.dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t8-status-check.txt
new file mode 100644
index 000000000..43dd4e343
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t8-status-check.txt
@@ -0,0 +1,15 @@
+# Task 8 status check (run by the implementer after the final test run)
+
+## git status --short with every entry under .dev/research/jev-vs-keyword-table-611/ removed, compared with ./artifacts/baseline-status.txt (diff of baseline against current; lines starting > are new)
+24a25,31
+> ?? .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t1-test.log
+> ?? .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t2-test.log
+> ?? .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t3-test.log
+> ?? .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t4-test.log
+> ?? .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t5-test.log
+> ?? .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t6-test.log
+> ?? .dev/tasks/to-do/TASK-WF-designSpec-20261126-162725/artifacts/t8-test.log
+## the same comparison with every .dev/tasks/ entry also removed from both sides (the plan's own package files and logs change by design)
+IDENTICAL
+## entries under src/, tests/, .claude/ or .dev/research/346-review-loop-experiments/ in git status --short
+none


Codegraph context
index_state: fresh
checked_at: 2026-11-26T16:38:23Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-611
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-611
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: the files of this task are new or only used by later tasks; no dependent outside the touched files.
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
