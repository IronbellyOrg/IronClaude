589aaf641b8e29f30a3356244084f3cb1a8402a7
Review one task for spec compliance.

Task brief: ## Task 7: Write the table procedure and the corpus and provenance templates

Depends on: Task 4

Create `.dev/research/jev-vs-keyword-table-611/table/table-procedure.md`, `.dev/research/jev-vs-keyword-table-611/table/table-provenance.md`, `.dev/research/jev-vs-keyword-table-611/corpus/selection-criteria.md` and `.dev/research/jev-vs-keyword-table-611/corpus/labelling-record.md`.

`table-procedure.md` states how the Wave 0 table in `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` is applied as written: the six cue rows quoted from lines 153 to 158 and the ambiguity rule of line 159, "no cue matched" gives an unset answer, cues from two or more rows give an unset answer, "leak" stays in both performance and security, no first-match parser and no extra inference. It requires the applier to receive prompts only, never the labels or any Jev answer, to be a different person or session from the labeller, to record per prompt the cues and rows matched, and to store all answers before any Jev call and only after `gate.py gate1` passes. It defines the `table-answers.jsonl` row (`prompt_id`, `answer` or null, `cues`, `rows`, `method`) and ends with the command `gate.py freeze-table`. `table-procedure.md` also names a step a person does before `gate.py freeze-corpus`: the person reads the six definitions in `questions.py` once and records that with `events.py owner-input --evidence <questions.py path> --note "<who read the six definitions>"` (finding M-2). `table-provenance.md` is a form to fill: method (a person reading the prose, or executing the skill), the source revision (the commit and the blob of the table file at the time), who applied it, the date, and, for a skill execution, evidence of which copy ran (the lesson recorded in `docs/memory/reflect/deviation-patterns-issue-610.md`). `selection-criteria.md` is a form for the public sources listed before any arm runs, the counts per label, any shortfall reported rather than padded, and the rule that a prompt the privacy screen would refuse is replaced, never edited. `labelling-record.md` is a form for the named labeller, the date, the labelling instructions, and the basis for each label, with the rule that the basis for an `ambiguous` or `none-fit` label is written before any arm runs and is not taken from the table's own two-row rule.

Acceptance criteria:
- Each of the four files exists, states at its top that it is a form or procedure to be completed by a person or session and is not evidence, and has no filled-in prompt, label or answer.
- `table-procedure.md` quotes the six cue rows exactly as they stand in lines 153 to 158 of `SKILL.md` and the ambiguity rule of line 159 (checked by comparing the quoted text to those lines).
- `table-procedure.md` names `.dev/research/jev-vs-keyword-table-611/table/table-answers.jsonl` and its row fields, states the Gate 1 ordering and the prompts-only rule, and names `gate.py gate1` and `gate.py freeze-table`.
- The files contain no real prompt text and no key.

Acceptance criterion ids (in source order):
T7.AC1: Each of the four files exists, states at its top that it is a form or procedure to be completed by a person or session and is not evidence, and has no filled-in prompt, label or answer.
T7.AC2: `table-procedure.md` quotes the six cue rows exactly as they stand in lines 153 to 158 of `SKILL.md` and the ambiguity rule of line 159 (checked by comparing the quoted text to those lines).
T7.AC3: `table-procedure.md` names `.dev/research/jev-vs-keyword-table-611/table/table-answers.jsonl` and its row fields, states the Gate 1 ordering and the prompts-only rule, and names `gate.py gate1` and `gate.py freeze-table`.
T7.AC4: The files contain no real prompt text and no key.
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
Start sha: 589aaf641b8e29f30a3356244084f3cb1a8402a7
Diff against the start snapshot: diff --git a/.dev/research/jev-vs-keyword-table-611/table/table-procedure.md b/.dev/research/jev-vs-keyword-table-611/table/table-procedure.md
new file mode 100644
index 000000000..560170998
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/table/table-procedure.md
@@ -0,0 +1,63 @@
+# Table procedure: how the keyword table is applied (issue 611)
+
+**This is a procedure to be followed by a person or session. It is not evidence, and it holds no filled-in prompt, label or answer.**
+The evidence it produces is `.dev/research/jev-vs-keyword-table-611/table/table-answers.jsonl` and the filled
+`.dev/research/jev-vs-keyword-table-611/table/table-provenance.md`.
+
+## The table, as it stands
+
+The keyword table is step 2 of the Steps of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`. Its six cue rows (lines 153 to 158 of that
+file) and its ambiguity rule (line 159) are quoted here exactly:
+
+```text
+   - Stack trace, exception name, `undefined`/`null`/`NameError` → `bug`
+   - "tsc", "ts(", "compiled", "lint", "build", `make`, CI log fragments → `build`
+   - "slow", "latency", "p99", "memory", "leak", "too long to load", "takes forever", "hangs", profiler output → `performance`
+   - "production", "deploy", "container", "env var", "service won't start" → `deployment`
+   - "auth", "token", "leak", "exposed", "CVE", "vulnerab" → `security`
+   - "pytest", "jest", "flake", "intermittent", "passing locally" → `test`
+   - On ambiguity, leave `--type` unset and treat all agent specialties as candidates for Tier 2. Keep "leak" in both rows: it can mean resource leakage or sensitive-data disclosure, so ambiguous leak reports must not discard security candidates.
+```
+
+The right-hand word of each cue row is the type (`bug`, `build`, `performance`, `deployment`, `security`, `test`).
+
+## How it is applied: as written, nothing more
+
+1. A row matches a prompt when the prompt holds at least one cue of that row as written. The structural cues (a stack trace, an exception
+   name, CI log fragments, profiler output) match when the prompt visibly holds one.
+2. Exactly one row matches: the answer is that row's type.
+3. No cue of any row matches: the answer is unset (`null`).
+4. Cues from two or more rows match: the answer is unset (`null`). The word "leak" stays in both the `performance` row and the `security`
+   row, so a prompt whose only cue is "leak" matches two rows and is unset.
+5. There is no first-match parser: the order of the rows decides nothing.
+6. There is no extra inference: nothing outside the quoted cues, no guess about what the prompt "really" means.
+
+## Before the table is applied
+
+1. **Reading step, before `gate.py freeze-corpus`.** A person reads the six definitions in `.dev/research/jev-vs-keyword-table-611/questions.py`
+   once and records that with:
+   `uv run python .dev/research/jev-vs-keyword-table-611/harness/events.py owner-input --evidence .dev/research/jev-vs-keyword-table-611/questions.py --note "<who read the six definitions>"`
+2. **Gate 1 first.** The corpus and its labels are frozen (`uv run python .dev/research/jev-vs-keyword-table-611/harness/gate.py freeze-corpus`) and `uv run python .dev/research/jev-vs-keyword-table-611/harness/gate.py gate1` prints `PASS`. The table is applied
+   only after that, and every answer is stored before any call to Jev is made.
+3. **Prompts only.** The applier receives each prompt's id and text and nothing else: never a label, never the labeller's notes, never any
+   Jev answer.
+4. **A different applier.** The applier is a different person or session from the labeller.
+
+## What is recorded
+
+One JSON object per line in `.dev/research/jev-vs-keyword-table-611/table/table-answers.jsonl`, one line per corpus prompt:
+
+| Field | Holds |
+|---|---|
+| `prompt_id` | the `id` of the corpus row |
+| `answer` | one of the six types, or `null` for an unset answer |
+| `cues` | the cue phrases found in the prompt (a list, empty when none) |
+| `rows` | the names of the rows those cues belong to (a list, empty when none) |
+| `method` | how the table was applied: `person reading the prose` or `skill execution` |
+
+Then fill `.dev/research/jev-vs-keyword-table-611/table/table-provenance.md`.
+
+## Freezing
+
+Run `uv run python .dev/research/jev-vs-keyword-table-611/harness/gate.py freeze-table`. It refuses unless Gate 1 passes at that moment and both the answers file and the provenance file exist, and it
+refuses to replace a frozen table.
diff --git a/.dev/research/jev-vs-keyword-table-611/table/table-provenance.md b/.dev/research/jev-vs-keyword-table-611/table/table-provenance.md
new file mode 100644
index 000000000..74afa10a2
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/table/table-provenance.md
@@ -0,0 +1,24 @@
+# Table provenance (a form to fill in)
+
+**This is a form to be completed by the person or session that applied the table. It is not evidence until it is filled in, and it holds no
+prompt, label or answer.**
+
+Fill every line. Leave nothing blank; write `none` or `not applicable` where that is the truth.
+
+- Method (one of: a person reading the prose, or executing the skill): `<fill in>`
+- Source revision, the commit (`git rev-parse HEAD`): `<fill in>`
+- Source revision, the blob of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` at that time (`git hash-object <that file>`): `<fill in>`
+- Who applied the table (a name, or a session id): `<fill in>`
+- Date applied (UTC): `<fill in>`
+- The applier was a different person or session from the labeller (yes or no): `<fill in>`
+- The applier received prompts only, with no label and no Jev answer (yes or no): `<fill in>`
+- Gate 1 had passed before the table was applied (yes or no, and the time of the `gate1` event): `<fill in>`
+
+## Only when the method was executing the skill
+
+A source-table assertion is not proof of what ran. Record which copy of the skill executed (the lesson in
+`docs/memory/reflect/deviation-patterns-issue-610.md`):
+
+- The copy that was loaded (the installed `~/.claude/skills/...` path or the project `.claude/skills/...` path): `<fill in>`
+- The SHA-256 of that copy: `<fill in>`
+- The actual tool-loading trace or transcript that shows it loaded (a path): `<fill in>`
diff --git a/.dev/research/jev-vs-keyword-table-611/corpus/selection-criteria.md b/.dev/research/jev-vs-keyword-table-611/corpus/selection-criteria.md
new file mode 100644
index 000000000..7127825c6
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/corpus/selection-criteria.md
@@ -0,0 +1,38 @@
+# Corpus selection criteria (a form to fill in)
+
+**This is a form to be completed by a person before any arm runs. It is not evidence until it is filled in, and it holds no prompt, label or
+answer.**
+
+Fill it in before the corpus is frozen with `gate.py freeze-corpus`. Prompts are public only.
+
+## Public sources
+
+List every public source before any prompt is taken from it (a name and a URL, why it was chosen, the date it was read):
+
+- `<fill in>`
+
+## Counts per label
+
+About 30 prompts in total. Write the target and the final count for each label:
+
+| Label | Target | Final count |
+|---|---|---|
+| bug | `<fill in>` | `<fill in>` |
+| build | `<fill in>` | `<fill in>` |
+| performance | `<fill in>` | `<fill in>` |
+| deployment | `<fill in>` | `<fill in>` |
+| security | `<fill in>` | `<fill in>` |
+| test | `<fill in>` | `<fill in>` |
+| ambiguous | `<fill in>` | `<fill in>` |
+| none-fit | `<fill in>` | `<fill in>` |
+
+## Shortfall
+
+A label with fewer prompts than its target is reported here, with the reason. It is never padded with a prompt that does not belong:
+`<fill in>`
+
+## Prompts the privacy screen refuses
+
+A prompt that the privacy screen (`jevlib.manifest.privacy_violation`, run by `gate.py freeze-corpus`) would refuse is replaced by another
+public prompt. It is never edited to get past the screen. List each replacement by id and reason, never by the refused text:
+`<fill in>`
diff --git a/.dev/research/jev-vs-keyword-table-611/corpus/labelling-record.md b/.dev/research/jev-vs-keyword-table-611/corpus/labelling-record.md
new file mode 100644
index 000000000..8712cbbbc
--- /dev/null
+++ b/.dev/research/jev-vs-keyword-table-611/corpus/labelling-record.md
@@ -0,0 +1,21 @@
+# Labelling record (a form to fill in)
+
+**This is a form to be completed by the named labeller before any arm runs. It is not evidence until it is filled in, and it holds no
+prompt, label or answer.**
+
+- Labeller (a named person, not a session): `<fill in>`
+- Date labelled (UTC): `<fill in>`
+- The labelling instructions the labeller was given (paste or link them): `<fill in>`
+
+## Basis for each label
+
+One line per corpus prompt, by id: the label and the basis for it, in the labeller's own words.
+
+- `<prompt id>`: `<label>` because `<fill in>`
+
+## Rules for the basis
+
+- The basis for an `ambiguous` or `none-fit` label is written before any arm runs.
+- That basis is not taken from the table's own two-row rule (the cues of two rows, or no cue), because that would make the table right by
+  construction.
+- The labeller does not see the table answers or any Jev answer.


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
