---
topic: "Jev preflight step 2: compare Jev against the keyword table on about 30 labelled prompts @.dev/issues/611/issue-summary.md"
domain: research
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-11-26T14:08:00+00:00
---

# Seed Brief: jev-vs-keyword-table-611

Dialogue mode: non-interactive. The Clarify and Validate questions (research domain, standard depth) were answered from the claimed issue summary `.dev/issues/611/issue-summary.md`, the accuracy check `.dev/issues/611/accuracy-check.md` and the existing analysis `.dev/issues/611/analysis/analyze-sc-troubleshoot-protocol.md`. Nothing below was invented: where the sources are silent the item sits under Open Questions.

## Problem Statement

`/sc:troubleshoot` picks one of six problem types (`bug`, `build`, `performance`, `deployment`, `security`, `test`) with a prose keyword table (Wave 0 of `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`, lines 152 to 159, repaired by pull request 871 on 2026-11-26). The decision to build a Jev-based preflight classifier (issue 612) depends on whether Jev (TypeSafe model `jev-1.14.0`) clearly beats that table. No measurement exists yet. The decision this research informs: build issue 612, or close it as not justified, recorded on issues 611 and 609.

## Known Context

- Evidence to produce: about 30 past public `/sc:troubleshoot` prompts, covering all six types plus ambiguous and none-fit cases, labelled by a person and frozen before either side runs.
- Candidates: (a) the corrected keyword table applied as written, keeping its ambiguity rule (unset when unclear, "leak" deliberately in both performance and security); (b) Jev, one request per prompt: a Choice over the six types plus a companion Noul question asking whether any type fits. Noul values between 0.3 and 0.7 mean "not settled" and leave the type unset. Failed calls are errors, never "no". All question wording lives in one file.
- Per prompt record: label, table answer, Jev answer, Jev probability, latency. Report: accuracy, abstention rate, cost, median and slowest latency, disagreements.
- Out of scope: a production preflight command or hook, gateway rewrite, depth or scope comparison, private repositories (issue 552), any edit to the table.
- Owner decision already typed in by the lead on 2026-11-26: yes to sending about 30 public prompts to TypeSafe on the `TYPESAFE_API_KEY` key, with a 1 dollar spend cap, public prompts only. The key is never printed or stored.
- Baseline revision: `origin/integration` at `37765a800d0b232cc231cf58b796fec23b26f8a8`; table file blob `76bcb3d94182371250ffe99a7b60b9124b05c368`.
- Existing evidence is about the table only (pull request 871: four namespaced Wave 0 observations, 404 related tests passing). No Jev measurement exists; Jev latency and accuracy are UNVERIFIED.
- Enrichment: skipped. Codebase enrichment is not triggered for a research topic and the analysis file already covers the source; research enrichment is not triggered because Jev is already present in this project (issues 574 and 575, earlier brainstorm folder `20261114-jev-model-validation-hook`); service details are to be validated only at authorised execution time.

## Constraints

- No prompt is sent to TypeSafe, and no comparison is run, until Clay's two pre-run numbers are typed into the terminal by the lead. Both are PENDING: the margin Jev must win by, and the acceptable median latency. The requirements must make that a hard gate, not a note.
- Spend cap is 1 dollar; the issue quotes about 0.00004 dollars per call, so about 30 calls is far under the cap. A run must stop before exceeding the cap.
- Public prompts only; each prompt needs recorded public provenance.
- Labels frozen before either side runs; the decision rule is fixed before the run and not changed after seeing results.
- The table arm must be applied as written (structural cues and ambiguity rule preserved), not replaced by a better classifier or a first-match parser.
- Pinned model `jev-1.14.0`, never an alias.
- Output lives under `.dev/` (corpus, question file, rule, results, decision record); no change under `src/`.
- Tests for any scoring code must run offline with no live API.

## Success Criteria

- A frozen, labelled corpus of about 30 public prompts with provenance exists before any run, covering all six types and ambiguous or none-fit cases.
- A written decision rule (margin and acceptable median latency, both from Clay) exists and is dated before the first live call.
- Per-prompt records and the aggregate report (accuracy, abstention, cost, median and slowest latency, disagreements) exist for both arms.
- The verdict (Jev clearly beats the table, or not) follows mechanically from the pre-fixed rule and is recorded on issues 611 and 609, and issue 612 is updated (build, or close as not justified).
- Total spend stays at or under 1 dollar and the key never appears in any file, log or pull request text.

## Open Questions

- The margin Jev must win by (a count of prompts, or a share, larger than the disagreement noise on 30 prompts): PENDING from Clay. No value may be assumed.
- The acceptable median latency for a pre-step: PENDING from Clay. No value may be assumed.
- Exact treatment of Noul values at exactly 0.3 and exactly 0.7, and how a failed call is scored against accuracy (the issue says error, not "no"): to be written down before scoring.
- How the table arm is applied reproducibly: by a person reading the prose table, or by running the actual skill's Wave 0 (execution provenance matters, see `docs/memory/reflect/deviation-patterns-issue-610.md`).
- How "about 30" public prompts are sourced and labelled (who labels, how ambiguous and none-fit cases are chosen), and the experiment folder name under `.dev/`.
- Whether the live run is a script in the repository or a manual sequence, given the key must never be printed or stored.
