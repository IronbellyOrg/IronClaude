# Jev against the keyword table (issue 611)

This folder holds the offline measuring harness for step 2 of the Jev preflight (issue 611, part of issue 609): does the Jev model beat the
keyword table in the troubleshoot skill at choosing the problem type of a prompt, by a margin larger than the noise on about 30 labelled
prompts, and fast enough to sit in front of `/sc:troubleshoot`?

**What it decides:** one of three verdicts, by a rule written down before any prompt is sent: `JEV_BEATS_TABLE`, `NOT_CLEARLY`, or
`RUN_INVALID` (with the reason). The build-or-close decision on issue 612 is made only from a valid run.
**What it does not decide:** it does not choose or label the prompts, apply the table, or call the live API. People and the coordinator do
those steps (see the order of work and the Delivery status below). Building and testing this harness sends nothing anywhere.

**Rule for implementer sessions:** an implementer session never calls the live API and never reads the key. The live run is a coordinator
action under rule J2 of `.dev/research/346-review-loop-experiments/p15/plans/SHARED-CONTRACT.md`.

## Folder layout (one job per file)

| File | Its one job |
|---|---|
| `decision-rule.md` | Every policy value of the experiment, with the verbatim agreement and the three values set after it |
| `questions.py` | The only place Jev question wording lives |
| `harness/loader.py` | Where every file lives, hashing, and reading the rule file, corpus and table answers |
| `harness/spend.py` | The only code that estimates tokens or turns a price and a cap into a ceiling |
| `harness/events.py` | The append-only event log, and the commands that record owner input, the price and the lead's go |
| `harness/gate.py` | The manifest (write-once hashes) and the two gates that keep every live call closed |
| `harness/runner.py` | One live run on `JevClient`, and a rehearsal that never posts |
| `harness/scorer.py` | The decision rule as pure functions, the scoring pipeline, the verdict, the report and the decision record |
| `harness/tests/` | The offline tests (mock transport, a socket guard, a temporary root for every file written) |
| `corpus/` | `selection-criteria.md` and `labelling-record.md` (forms), then `corpus.jsonl` once a person has made it |
| `table/` | `table-procedure.md` (how the table is applied), `table-provenance.md` (a form), then `table-answers.jsonl` |
| `manifest.json`, `events.jsonl`, `ledger/`, `runs/<run-id>/` | Written by the commands below, never by hand |
| `report.md`, `decision-record.md`, `rescores/` | Written by `scorer.py` |

## Offline test command

Run from the repository root (the repository's `testpaths` is `tests`, so tests under `.dev/` are collected only when this path is given):

```bash
uv run pytest .dev/research/jev-vs-keyword-table-611/harness/tests -v
```

## Order of work

Every command is run from the repository root. Write `GATE`, `EVENTS`, `RUNNER` and `SCORER` for
`uv run python .dev/research/jev-vs-keyword-table-611/harness/gate.py`, `.../events.py`, `.../runner.py` and `.../scorer.py`. Each command
takes `--root` (the experiment folder by default).

1. **Rule AGREED.** `decision-rule.md` holds the agreed rule (26 Nov 2026); the three values the agreement left open were set on 26 Nov 2026 (see Open items).
2. **Read the six definitions once** (a person), then record it. This step comes immediately before `gate.py freeze-corpus`:
   `events.py owner-input --evidence .dev/research/jev-vs-keyword-table-611/questions.py --note "<who read the six definitions>"`
3. **Corpus and labels frozen** (a named human labeller has filled `corpus/corpus.jsonl`, `corpus/selection-criteria.md` and
   `corpus/labelling-record.md`): `gate.py freeze-corpus`. It runs the privacy screen and refuses on any failure.
4. **Gate 1:** `gate.py gate1`. It accepts `UNSET` rule values and hashes files only.
5. **Table answers** are applied as `table/table-procedure.md` says (prompts only, after Gate 1), then frozen: `gate.py freeze-table`. It refuses a table that does not have exactly one row for every corpus prompt, each with an explicit `answer` (null or one of the six types) and the `cues`, `rows` and `method` the table procedure records.
6. **The answers to the open rule fields** (set in `decision-rule.md`, see Open items; the owner or the lead may still change them before the next step) are recorded:
   `events.py owner-input --evidence .dev/research/jev-vs-keyword-table-611/decision-rule.md --note "<who answered, and the three values>"`
7. **Freeze the rule:** `gate.py freeze-rule`. It refuses any `UNSET` value.
8. **Re-confirm the price** on the vendor page and record it: `events.py price --usd-per-mtok <value> --source "<where it was read>"`.
9. **Record the offline test run:** `gate.py record-tests` (it runs the test command above and stores the hash of every code file). When a run is scored, the code is compared with the record made before the run's first request; a record made after the run began is not used.
10. **The lead's go**, naming the rule file's hash: `events.py go --words "<the lead's words>"`.
11. **Gate 2:** `gate.py gate2`. It fails on any missing step, any changed frozen file, a spend bound that does not fit, or a run already started.
12. **Rehearse** (posts nothing, needs no gate and no key): `runner.py rehearse --out <a folder outside ledger/ and runs/>`.
13. **The coordinator's live run:** `runner.py run --run-id <ID> --live`. It refuses a `--root` other than the experiment folder the code was loaded from (the files it hashes must be the code that runs), checks both gates itself and reads no environment variable before
    they pass. The key is mapped from `TYPESAFE_API_KEY` to `JEV_API_KEY` inside one subshell command only (rule J2), never printed, never put on a
    command line and never written to a file. The key scan sets `JEV_API_KEY` from `TYPESAFE_API_KEY` inside the same single subshell command and
    names its paths explicitly:

    ```bash
    bash -c 'export JEV_API_KEY="$TYPESAFE_API_KEY"; uv run python .dev/research/346-review-loop-experiments/p15/jev/keyscan.py .dev/research/jev-vs-keyword-table-611/runs/<ID> .dev/research/jev-vs-keyword-table-611/events.jsonl .dev/research/jev-vs-keyword-table-611/manifest.json .dev/research/jev-vs-keyword-table-611/ledger/spend.json'
    ```

    It must print `KEYSCAN OK`. The live run command has the same form: `bash -c 'cd <repo> && uv run python .../runner.py run --run-id <ID> --live'`
    in a shell where `TYPESAFE_API_KEY` is available to that one command.
14. **Score:** `scorer.py score --run-id <ID>`. It refuses while any rule value is `UNSET`, writes `report.md` and `decision-record.md` for every
    verdict, appends the `scoring` and `verdict` events, and never overwrites an existing report. Run the key scan again over the two new files.

## How to rescore

`scorer.py score --run-id ID --rescore NAME --rule PATH` scores the same run under another rule file. It writes only
`rescores/NAME/report.md`, labels it non-decisional, and never changes the root report, the decision record or an event. It refuses a
name that already exists.

## Open items and who answers each

| Item | Who answers | Decided (26 Nov 2026, by the build agent under Clay's standing rule) |
|---|---|---|
| `noul_low_operator` (`lt` or `le`) | The owner, through the lead | `le`: it changes only the reason label of an unset answer, not the score. Set in `decision-rule.md`. |
| `noul_high_operator` (`gt` or `ge`) | The owner, through the lead | `gt`: Jev answers only when its Noul value is above 0.7, so the band 0.3 to 0.7 is all abstention. Set in `decision-rule.md`. |
| `unresolved_failure_invalid_count` | The owner, through the lead | `3` (about a tenth of 30 prompts). The scorer reads it as the count at which a run becomes invalid: a run with that many prompts that failed twice, or more, is `RUN_INVALID`. Set in `decision-rule.md`. |
| Who labels the prompts | The lead names a human labeller | Clay, the issue owner, as the named human: the plan requires a named person, the labels are the ground truth both arms are scored against, so neither an AI session nor the table applier labels. If Clay hands it on, the person is named in `corpus/labelling-record.md`. |
| Who applies the table | The lead names a session or person that sees prompts only and is not the labeller | A separate session given the prompts only (no label, no Jev answer), after Gate 1, as `table/table-procedure.md` says. |
| The live route: the vendor URL, or the LiteLLM gateway through `JEV_API_URL` | The lead and the coordinator | The vendor URL directly (leave `JEV_API_URL` unset) with `TYPESAFE_API_KEY`: the lead's decision names that key and the runner maps exactly that variable. The gateway guide (`docs/docs-product/ops/jev-litellm-gateway-operational-guide.md`) keeps the vendor key on the gateway and issues workspaces a virtual key, so a gateway route would use a different key, put a second spend limit outside the 1 dollar ledger and add a hop to the measured latency. If `TYPESAFE_API_KEY` is not available to the coordinator's one command, the run refuses and the lead supplies it. |
| The price to re-confirm before Gate 2 | The coordinator | 0.042 USD per million input tokens, re-confirmed on 26 Nov 2026 on the vendor's models page (https://docs.typesafe.ai/models, Jev 1.14, output tokens free); it matches the `jevlib` constant read on 2026-11-10. Recorded before Gate 2 with `events.py price --usd-per-mtok 0.042 --source "docs.typesafe.ai/models, read 2026-11-26"`. |
| Where the prompts come from (public sources only) | The person who selects them, listed in `corpus/selection-criteria.md` | Public issue trackers and forums, listed there before any arm runs; an AI session may collect candidates and run the privacy screen, the named human labels. |

The lead's go names the hash of `decision-rule.md` as it stands when `gate.py freeze-rule` is run; if any value above is changed first, the hash changes and the go names the new one.

## Delivery status

Parts A to E of section 8 of the design (`.dev/brainstorms/20261126-jev-vs-keyword-table-611/design-spec.md`):

| Part | Who | Done? |
|---|---|---|
| A. Harness: loader, gate, scorer, runner, events, tests, the rule file with the AGREED rule, this README | Implementer, offline | Yes, delivered by this pull request, with the table and corpus templates |
| B. Corpus and labels: about 30 public prompts, provenance, human labels, label basis, freeze | A named human labeller | No, left |
| C. Table answers | A separate session or person given prompts only, after Gate 1 | No, left |
| D. Live run, key scan, scoring, report | The coordinator, after Gate 2 and the lead's go | No, left |
| E. Issue updates on 611, 609 and 612 | The coordinator | No, left |

The pull request that delivers this carries the sentence: `Refs #611`, with parts B, C, D and E listed as left.
