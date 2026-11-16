# Open questions and decisions, tasklist review panel evaluation (as of 2026-11-15 14:00 UTC)

> **Status box added 2026-11-16 (evening) by the Sweep Sheet session; the rows below are the 2026-11-15 14:00 UTC state.** Sweep Sheet: stopped by the owner after its recall gate failed twice. Recipe Ledger: stopped as a build, but its experiment was then run on the owner's order: 9 replicates x 3 arms x 3 study packages. RL found 2.00 of 14 per replicate against 0.67 (Z0) and 0.56 (K), but ran 1.46 x and 1.60 x Z0's time on two packages (cap 1.35) and depends on the format allowances (strict reading would fail 58% of reports). Exploratory only. See `20261114-recipe-ledger/results/derivation-3x/SUMMARY-9reps.md` and the update boxes of `OPEN-QUESTIONS-20261115.md`. **Q3 is answered by that run** (study packages, derivation check only). **Q6 (small allowances) was built for RL and its result depends on it.** The owner's 2026-11-16 answers (model-usage infractions warn and report, do not halt; workflow/implement are the current workflow; `/sc:task` and task-builder to be retired; evaluate only the Sprint run CLI tool suite) are recorded in `OPEN-QUESTIONS-20261115.md` and `../../brainstorms/20261114-jev-model-validation-hook/OPEN-QUESTIONS.md`. Q1, Q2, Q4, Q5, Q7 to Q13 are not answered by anything recorded so far.

## Read this first (context for a reader who has seen nothing else)

**What this is.** A multi-day evaluation of how well cheap reviewer-model panels find real defects in tasks lists and plans produced by `/sc:workflow` (the "Review Panel" of this repository, code in `src/superclaude/cli/review/`). Three panels are compared: ember + 2x luna, haiku + 2x luna, sonnet + 2x luna (ember = `muse-ember-1.0`, luna = `gpt-6-luna`). A blind Opus judge scores each run against hidden ground truth. Opus is used only to judge; everything else uses Sonnet, Haiku, ember or luna.

**Where things are.** Everything is under `.dev/eval-workspaces/tasklist-review-panel/` on branch `ironbelly/eval-tasklist-review-panel`, remote `origin` = `IronbellyOrg/IronClaude` only (never `SuperClaude-Org`).
- `20261111-a1/`: the original study and its tools. `HANDOFF-review-panel-unification*.md`: the two hand-off reports.
- `20261113-collab/`: five reviewer-to-reviewer collaboration designs and their counted results. `RESULTS-20261114.md` is the write-up; `counted-results.md` is the central table. Conclusion: no reliable gain from collaboration; stop that line.
- `20261114-severity/`: a plan to lower how often the panel calls an issue blocking (narrowed rule for "contradiction"). Measured, not yet applied to product files.
- `20261114-sweep-sheet/` (session SS) and `20261114-recipe-ledger/` (session RL): the two "process redesigns" from the second brainstorm (`.dev/brainstorms/20261113-223124-panel-process-redesign/merged-requirements.md`). Redesign 1, Sweep Sheet: a script extracts at most 12 typed items and cheap models judge one at a time. Redesign 2, Recipe Ledger: written class recipes plus a forced enumerate-then-judge ledger, no pre-pass.
- `20261114-collab-process/PROCESS.md`: the agreed (by the two sessions; confirmed by the owner) rules for how SS and RL work together. `with-slot.sh` there is the shared lock (max 2 model launches at once).

**Who is who.** Owner = the human user. SS and RL = two Claude Code sessions working in this worktree, named `eval-tasklist-review-1111-172932-0b98` (both carry the same name; message them as `[ea7e02]` = SS and `[9e8671]` = RL). Sessions can propose; only the owner decides documents, freezes, adoption, pushes and models.

**Standing rules.** UV for Python (`uv run ...`). Never stage `.claude/`. Do not change existing `.dev/tasks/` packages. No PR. No reading of ground-truth files by build or reviewer sessions. Keep intermediates (rename, never delete). Raw model transcripts are not committed.

## State in one paragraph per session

**RL (Recipe Ledger).** Built (20 of 20 plan tasks; 503 fast tests pass, 1 skipped, 3 `freeze` tests deliberately not run because they need the real answer files or a person). Second-author recipe review done by a fresh Sonnet session (all 8 recipes PASS after the owner approved rewording of C2, C4, C5, C6, C8, recorded as `override` in `recipes/recipes.json`). Compliance spike attempt 1 FAILED its gate (2 of 14 reports without a valid ledger = 14.3%, limit 10%); on the owner's order the check now forgives a small prefix or suffix around the row id (`C4.1`, e.g. `R-C4.1`) and a heading between the ledger and the findings block, and the spike is being rerun (attempt 2, 5 runs). Timing spike and every experiment arm have not run. Details: `20261114-recipe-ledger/IMPLEMENTATION-REPORT.md`, `results/spikes/`.

**SS (Sweep Sheet).** Built (33 of 33 plan tasks, 749 tests pass, 4 deselected). No live panel run yet. Owner adopted its three defaults (selection floor 0.45, eight act bands, CB-2 wording, K-arm lead-in). Freeze not done: needs people (see questions).

## Questions and decisions still open

Each row says who must answer and what happens when it is answered.

| # | Question or decision | Who answers | Why it matters / what it unblocks |
|---|---|---|---|
| Q1 | **Who is the second author** of the Sweep Sheet class cards (`swap_test` records, 8 cards), **who plants the test plans** (a person who has not read the extractors), and **who writes the hold-out ground truth** and attests it? | Owner (asked in the SS session) | SS freeze and every experiment run. The spec wants people who have not seen the answers or the extractors. |
| Q2 | **The hold-out document list.** The owner chose "hold-out documents" (sets HO-1 to HO-6 of the requirements section 5.1) but no list of actual documents exists yet. | Owner, with the ground-truth author | Parity test, shared control, Stage 1 runs. |
| Q3 | **Did the owner still want "3 tests each" on the 3 study packages?** That was the original request; the requirements say the 3 study packages are only a derivation check and never evidence for adoption. | Owner | Whether to spend 9 panel runs on the derivation check after the freezes. |
| Q4 | **Freeze go for RL** (given) and **SS** (given). Both freezes are blocked by Q1 and by RL's compliance gate (below). | Owner confirms when people tasks are done | Freeze tag and hash list; then the parity test. |
| Q5 | **Shared control (Z0) for both redesigns** (approved, gated by a parity check). Parity covers: Z0 brief, sandbox build, model and flags, retry and fallback rules, judge script, anonymiser, merge command; any difference for any document means each session runs its own. | Nothing now; runs after both freezes | Saves 3 to 9 panel runs. |
| Q6 | **"Small allowances across the board" (owner message 2026-11-15).** Make the other format checks forgive small, harmless deviations as the row-id check now does (see section below). Needs the owner to approve the list before it is built, because each allowance changes a pass/fail rule. | Owner | RL compliance gate and the other checks of both redesigns. |
| Q7 | **Does the RL compliance gate (at most 10% reports without a valid ledger) stay at 10%?** The requirements say RL does not run if it fails. Attempt 2 decides. | Owner if attempt 2 also fails | Whether RL continues. |
| Q8 | **Model labels.** SS saw the haiku alias resolve to `gpt-6.1-sol` in its advocate transcripts (gateway). RL launches use raw model ids and record the observed model, and 98 recorded haiku reviewer runs resolved correctly; 8 have no record (killed, no output). Should any run whose observed model differs from the label be dropped or only flagged? | Owner | Validity of every haiku row in the redesign experiments. |
| Q9 | **Recipe review by a model, not a person** (owner chose a Sonnet session). Recorded as such in `recipes/REVIEWS.md`. Is that acceptable for the freeze, or must a person re-sign? | Owner | RL freeze. |
| Q10 | **The 3 maintainer-only tests** (real-answer lint of the recipes and cards; review record) need a person who may read the real ground truth to run them at the freeze. Who? | Owner | RL and SS freeze. |
| Q11 | **Severity change (older).** The measured plan to narrow the "contradiction" blocking clause is in `20261114-severity/PLAN.md`; edits to the 11 pinned product files and their tests are not applied. Apply now, after the redesign experiments, or never? | Owner | Product change in `src/superclaude/`. |
| Q12 | **Three foreign scripts** (`snap.py`, `drift-b3.py`, `rlog-r3.sh`) sit in `20261111-a1/tools/tmp-scripts/`; they are not from this evaluation. Delete or keep? | Owner | Repository tidiness only. |
| Q13 | **Push policy.** Commit and push were ordered for these `.md` files on 2026-11-15. Everything else stays local until the owner says. Only one session pushes, to `origin` only. | Owner | Avoids two sessions pushing overlapping work. |

## Small allowances across the board (proposal for Q6)

Principle (from the owner): when a reviewer's output is correct in substance and wrong only by a small, unambiguous format slip, accept it and record that it was accepted, instead of counting it as a failure. Already built in RL (2026-11-15, owner-approved): (a) a row id with a prefix or suffix of at most 6 characters around `C<n>.<m>` is read as the canonical id (`R-C4.1`, `C4.1:`, `C4.1a`; a third number such as `C4.1.1` is not forgiven); the raw id is kept as `item_raw`; (b) a heading between the ledger block and the findings block no longer makes the ledger missing; it sets `loose_layout` so reports can count it.

Candidates to add after the spike attempt finishes (each would be one small rule plus a test; none is built yet): finding `probe` ids use the same prefix and suffix rule (already built); verdict words in lower case (already normalised); a ledger heading written as `### Ledger` or `Ledger:`; a fenced block language written in capitals; extra whitespace or a trailing comma on a JSON line; quote matching that ignores line wraps and doubled spaces (partly present). Not proposed: anything that would let a missing ledger, a wrong class, a quote not found in the plan, or an over-budget row pass. The same principle should be applied to Sweep Sheet's sheet and ledger parsers by SS, with the owner's approval of its own list.

## Where each open item is recorded

- Decisions table for the two sessions: `20261114-collab-process/PROCESS.md` section 8 (D1 to D5) and section 10.
- RL specifics: `20261114-recipe-ledger/IMPLEMENTATION-REPORT.md` section 5 (requirements not met), `recipes/REVIEWS.md`, `results/spikes/`.
- SS specifics: `20261114-sweep-sheet/results/owner-decisions.md` and its `bin/open-manual-checks.sh` (19 open items at last report).
- Earlier results: `20261113-collab/RESULTS-20261114.md`.

## How to resume if you arrive with no context

1. Read the preamble above and `PROCESS.md` sections 1 to 4.
2. Run `bash .dev/eval-workspaces/tasklist-review-panel/20261114-collab-process/with-slot.sh --status` to see running model sessions.
3. Do not start a live run until the owner has answered Q1 and Q2 and both freezes exist; the exception is RL's own spikes, which the owner approved.
4. Ask the owner exactly one question at a time, with a recommendation.
