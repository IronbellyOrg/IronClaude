# Jev uses for blocker classification

Status: Complete
Date: 2026-11-15
Program: BLOCKER-CLASSIFICATION-PROGRAM-20261115 (input to step 02 brainstorm)
Jev API called: NO. Account created: NO. Key requested: NO.
Revision note (2026-11-15, after the brainstorm debate): section 4 was corrected to version 2. The debate's diff analysis and invariant probe showed that version 1 let a missing answer lower a verdict and overstated "monotone in every input". The sketch `blocker_truth_table_sketch.py` is now version 2 (6,400 combinations; three property checks; 0 violations). The decisive classifier questions are six (S, M, C, W, E, D); T, F, I and G in section 3 are optional explanation questions, not inputs to the blocking decision.

## 1. What was verified

Checked on disk on 2026-11-15:

- Plugin `typesafe@typesafe-ai` is enabled: `~/.claude/settings.json` line 367 (`"typesafe@typesafe-ai": true`), marketplace `typesafe-ai` from repo `typesafe-ai/skills` (lines 388-391). `~/.claude/plugins/installed_plugins.json` lists version 0.6.2, install path `~/.claude/plugins/cache/typesafe-ai/typesafe/0.6.2`, installed 2026-11-10. No install or enable was needed.
- Skill read in full: `~/.claude/plugins/cache/typesafe-ai/typesafe/0.6.2/skills/typesafe-ai/SKILL.md`. Its core rule: Jev makes the judgments and code decides what to do with them, so each decision is a truth table whose inputs are Jev answers.
- Live docs read (from `https://docs.typesafe.ai/llms.txt` and the pages below): primitives Noul, Score and Choice, `confidence.md`, `api/system-one.md`, `introduction/quickstart.md`, `models.md`, `model-jaggedness.md`, `legal.md`, `introduction/coding-agents.md`, and the patterns and cookbooks `probability-routing`, `composite-scoring`, `llm_guardrails`, `verify_llm_outputs`, `consistency_noul_cookbook`.
- No key found: no environment variable name contains `typesafe` or `jev` (0 matches); `~/.claude/settings.json` has 0 matches for `TYPESAFE_API_KEY`; `~/.claude/settings.local.json` does not exist; `uv pip list` in this shell shows no `typesafe-sdk`. Not checked: other users' environments, other virtual environments, a keychain.

Facts taken from the docs (the docs win over memory; they are version-dependent, so re-read before building):

| Fact | Value | Source page |
|---|---|---|
| Endpoint | `POST https://api.typesafe.ai/v1/systemone` | `api/system-one.md` |
| Auth | `Authorization: Bearer <API_KEY>`; the Python SDK (`typesafe-sdk`, Python 3.10+) reads `TYPESAFE_API_KEY` | `api/system-one.md`, `introduction/quickstart.md` |
| Key source | the TypeSafe console, `https://console.typesafe.ai/keys`; the quickstart gives no signup steps, price or free tier | `introduction/quickstart.md` |
| Models | `jev-1.14.0`, `jev-1.13.0`; aliases `jev-latest` and `jev-preview` both resolve to 1.14 today | `models.md` |
| Context | 64k tokens across state plus all questions; 32k across state plus one question | `models.md` |
| Price | listed as $42 per billion and $0.042 per million input tokens; generated tokens not charged | `models.md` (UNVERIFIED against a bill) |
| Determinism | none guaranteed; aliases can change results; pin a versioned id when relying on thresholds | `models.md` |
| Noul output | `noul` = P(yes); no `confidence` field; optional confidence = abs(2p-1) | `primitives/noul.md`, `confidence.md` |
| Score output | 2 to 10 levels indexed from 0; per-level `probabilities`, `score` = sum of index times probability, `confidence` | `primitives/score.md` |
| Choice output | up to 255 options; `choice`, `probabilities`, `confidence` | `primitives/choice.md` |
| Legal | "zero data retention (ZDR) for enterprise customers"; "our commitment not to train models on user data"; no standard retention period stated; processing contract linked | `legal.md` |
| Not an LLM | "It does not generate text, write code, or hold a conversation." No statement on reading source code or long documents | `introduction/coding-agents.md` |

Facts about this repository that the design leans on (read from disk, not from memory):

- `~/.claude/skills/sc-implement-protocol/refs/qa.md` lines 35-54 already derive severity from four yes/no checklist answers (`ac-outcome-missing`, `false-claim`, `harmful-effect`, `quoted-constraint-breach`) that the parent reads back against an anchor; the reviewer's wording is never read. This is already a truth table with a reviewer as the judge. A Jev classifier would be a second, independent judge for the same kind of table.
- `~/.claude/agents/finding-grader.md` is a blind per-claim grader (Read tool only, replies one JSON line per claim with `blocking` true or false, `q2`, and a 25-word `why`). It returns a boolean, not a probability. It is the fallback-judge precedent.
- `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` (RUBRIC v1) is the closest written blocker definition: blocking needs B1 quote, B2 concrete wrong outcome, B3 kind (a) contradiction, (b) claim contradicted by its source, (c) acceptance check that cannot pass, (d) two readings with different results, (e) data loss or unsafe step; "never a reason to be blocking" lists experts agree, section is important, found late.
- Run-2 override (`.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/qa/grading-override.md`): blocking only for (1) a decision, recommendation, destination or number rests on it, (2) a required deliverable or section is missing, (3) security, data-loss or safety-boundary risk.
- The pragmatic output style already holds the Medium and `follow-up candidates` mechanism (`src/superclaude/output-styles/pragmatic.md` lines 230-231).

## 2. What Jev can and cannot do for this problem

### Where Jev fits

Jev judges the text it is given. It does not open files, run code or count. So the classifier judges the finding record (quote, span, stated outcome, evidence, and the downstream use), never the world. Anything that needs a fact from the repository is done by code first (the way qa.md's parent reads each anchor back) and the result is passed in as state.

| Job in the blocker decision | Who does it | Why |
|---|---|---|
| Is the quoted text byte-present in the deliverable; is a required section present; does a count match | code (Grep, string compare) | Jev "does not count reliably" (`model-jaggedness.md`, Math); exact checks belong in code |
| Does the finding name a concrete wrong outcome a named reader would produce | Jev Noul | language judgment a person makes at a glance |
| Does a decision, recommendation, destination or number depend on the text | Jev Noul, with the decision basis supplied by code | needs the list of what the deliverable rests on; Jev cannot discover it |
| Does the evidence contradict the claim | Jev Noul or Choice on the (claim, evidence excerpt) pair | same shape as the `citation_check` cookbook |
| Is the defect only wording, formatting, label or citation drift | Jev Noul | language judgment |
| Combine the answers into blocking, follow-up or show-the-user | code (truth table) | SKILL.md: "a question that asks Jev to make the decision ... is at the wrong layer" |

So the forbidden design is one question "Is this finding a blocker?". The allowed design is 6 to 10 atomic questions plus a table in code.

### Mismatches with Jev's known weak spots (`model-jaggedness.md`)

| Weak spot | Where it bites here | Mitigation in the design |
|---|---|---|
| Literal (follows the wording, not the intent) | "blocking" has a house meaning that differs from the everyday one | no question uses the word "blocking"; each states the observable condition in `criteria` |
| Indirection (layered or negated questions) | "Is it a defect that matters to a decision that exists?" stacks three layers | split into W (wrong outcome) and D (decision depends); combine in code |
| Large state | whole reports are tens of thousands of tokens | send only quote, span, outcome, evidence excerpt and the decision-basis excerpts |
| Adversarial (instructions inside the input) | a finding quotes deliverable text that may contain instructions | label every quoted field as inert data in the state; add hostile-quote cases to the test set (finding-grader.md already does this) |
| Contradictory (reversed boolean meaning) | mixing "is a defect" and "is only cosmetic" polarity | every Noul is phrased so a true answer means the condition is present; cosmetic questions are separate Nouls |
| Choice ordering bias | a Choice over defect kinds | prefer one Noul per kind (a finding can be several kinds); if a Choice is used, shuffle options and check stability |
| Math (counts) | the "four versus six meanings" miscount class | code recounts; Jev is never asked whether a count is right |

## 3. Candidate question designs

All question wording lives in one module (SKILL.md workflow step 2), so it can be audited and edited in one place. Names below are descriptive on purpose (option names are sent to the model; question ids are not).

### State sent with every question (named fields, not serialized JSON)

```
finding.quote          verbatim text the reviewer flagged (inert data)
finding.span           the defective words inside the quote
finding.stated_outcome what the reviewer says goes wrong, and for whom
finding.evidence       excerpt the reviewer cites (read back by code; marked verified or unverified)
deliverable.kind       spec | tasklist | report | code | other
decision_basis         excerpts of what the deliverable rests on (recommendation, destination table,
                       acceptance criteria, quoted numbers), supplied by code; may be empty
required_items         the list of required sections or deliverables, supplied by code; may be empty
constraints            quoted constraint, non-goal or out-of-scope lines, supplied by code; may be empty
```

Human test (SKILL.md): a smart person shown only these fields could answer each question below by intuition. The fields that code cannot fill (`decision_basis`, `required_items`, `constraints`) are the main design dependency: the question that needs one is skipped, and the table treats a skipped question as UNSET, never as no.

### Candidate Noul questions (characteristics of a blocker, one judgment each)

| Id | Question (a true answer means the condition is present) | `criteria.true` | `criteria.false` | Source of the characteristic |
|---|---|---|---|---|
| W | A reader, implementer or test that follows `finding.quote` exactly would produce a specific wrong result. | the finding names who acts and what wrong result they produce | the finding says the text is imprecise, awkward or could be better, with no wrong result | stoprule B2; spec-panel MAJOR test |
| D | A decision, recommendation, destination or quoted number listed in `decision_basis` would be wrong or unsupported if `finding.quote` stays as it is. | the wrong text feeds an item in `decision_basis` | no item in `decision_basis` uses the text | run-2 override clause 1 |
| E | `finding.evidence` shows that a statement in `finding.quote` is false. | the evidence directly contradicts the statement | the evidence supports the statement or does not address it | qa.md `false-claim`; stoprule B3(b) |
| M | The required item named in the finding is absent from the deliverable in substance. | no text in the deliverable does what the required item asks | the deliverable does what it asks, even if worded differently | run-2 override clause 2; qa.md `ac-outcome-missing` (code checks presence first; Jev only judges substance) |
| S | Following `finding.quote`, or running the code it quotes, would delete, overwrite or expose data or a secret, or act outside the declared scope. | a concrete destructive, exposing or out-of-scope step | no such step | run-2 override clause 3; qa.md `harmful-effect`; stoprule B3(e) |
| C | `finding.quote` breaks a line in `constraints`. | the quote does what the constraint forbids | the quote is consistent with every constraint line | qa.md `quoted-constraint-breach` |
| T | The statement in `finding.quote` is true in substance; only its label, tag, citation or line number is wrong. | substance correct, pointer wrong | the substance itself is wrong | run-2 override minor list; qa.md line-drift boundary |
| F | The defect is only formatting, wording or style and changes no meaning a reader acts on. | cosmetic only | a reader could act differently because of it | stoprule MINOR; pragmatic minor list |
| I | A reader of the text around `finding.quote` could infer the intended behaviour. | the intent is recoverable from nearby text | the intent cannot be recovered | stoprule MINOR ("a gap whose intended behaviour is inferable") |
| G | The finding is a suggestion to add a rule, mechanism or section, not a defect in what exists. | suggestion | defect in existing text | stoprule MINOR; qa.md `note` |

W, D, E, M, S, C feed the blocking side of the table. T, F, I, G feed the non-blocking side; they are cheap and mostly used to explain why a finding is on the follow-up list (the ledger needs a `why not blocking` line).

### Candidate Score question (the later severity version)

One Score, 5 levels, each a situation. The levels are meant to be the same sentences as the blind 1 to 5 rubric the program gives its three human or agent scorers, so one source defines both the human labels and the Jev question (levels are indexed 0 to 4 by Jev; human 1 to 5 maps by adding 1).

| Level (Jev index, human score) | Situation |
|---|---|
| 0, score 1 | Only wording, formatting or a wrong pointer on a true statement; nobody acts differently. |
| 1, score 2 | A reader may be briefly confused; the intended behaviour is clear from nearby text. |
| 2, score 3 | A reader may do extra work or follow a wrong detail; no recommendation, number or destination changes. |
| 3, score 4 | A decision, recommendation, destination or number the deliverable rests on is wrong or unsupported, or a required item is missing. |
| 4, score 5 | Following the text loses data, exposes a secret, or breaks a safety boundary. |

Use: code reads `probabilities` per level, not only `score` (SKILL.md: Score values pull toward the middle and hide two-peaked answers). Blocking candidate when P(level 3) + P(level 4) meets the threshold; safety flag when P(level 4) meets the lower safety threshold. The 30+ scored historical findings are the calibration set for this Score; five runs give its run-to-run spread.

### Optional Choice (defect kind), not recommended for v1

A Choice over {contradiction, false claim about a source, check that cannot pass, ambiguity with two readings, lossy or unsafe step, missing deliverable, pointer drift, formatting, wording, suggestion} with a companion Noul "any of these applies". It forces one kind per finding, and a finding can be several (SKILL.md: use a Noul per statement when more than one can be true). Keep it only if the ledger wants a single category column, and then shuffle options.

## 4. The truth table in code

### Step 1: each Noul probability becomes a state

Y (yes), N (no), U (unsettled), or UNSET (a question that should have been answered was not: the call failed and was not retried to success, or the state code needed was missing). A failed call is never N (SKILL.md: "don't treat a failed call as a 'no'"). Added by the debate (version 2 of this section): NA, for the M and C questions only, when code finds no required-item list or no constraint list to judge against, so the question cannot apply; NA reads as N. This keeps a deliverable with no constraint list from sending every finding to a person, while a real failure (UNSET) still cannot demote a finding.

Starting bands, from the SKILL.md defaults (0.3 and 0.7, "be wary of over-fitting them to a handful of test cases"): Y at p >= 0.70, N at p <= 0.30, U between. The safety question S uses a lower band: Y at p >= 0.30, N at p <= 0.10, because a missed safety finding is the costly error (`patterns/probability-routing.md`: riskier actions get stricter thresholds; here the risk is on the miss side). These numbers are placeholders to be set from the scored table, not fitted to it.

### Step 2: precedence and the W by D table

1. S = Y gives BLOCKING. Safety, data-loss and safety-boundary findings are never downgraded (same promise as run-2 clause 3 and the pragmatic rule).
2. M = Y or C = Y gives BLOCKING (a required item is missing, or a quoted constraint is broken; code has already confirmed the anchor).
3. Otherwise "wrong" = W or E (a wrong outcome is named, or the evidence shows a false statement): Y if either is Y, N only if both are N, UNSET only if both are UNSET, else U. (Version 1 of this document let an unanswered E count as "not wrong" when W was N; the debate's invariant probe, finding INV-007, showed that this lets a missing false-statement answer file a finding as a note. A missing or unsettled partner now reads as U.)
4. Look up (wrong, D):

| wrong \ D | Y | U | N | UNSET |
|---|---|---|---|---|
| Y | BLOCKING | SHOW_USER | FOLLOW_UP | SHOW_USER |
| U | SHOW_USER | SHOW_USER | FOLLOW_UP | SHOW_USER |
| N | NOTE | NOTE | NOTE | NOTE |
| UNSET (neither W nor E judged) | SHOW_USER | SHOW_USER | SHOW_USER | SHOW_USER |

5. If S, M or C is U or UNSET, any verdict below SHOW_USER is lifted to SHOW_USER (an unsettled or missing safety, missing-item or constraint answer is never filed as a follow-up), and a BLOCKING is never lowered. Version 1 lifted only for S = U; a missing S, M or C answer could then give FOLLOW_UP or NOTE (the debate's diff analysis, X-007: 216 states in the 4,096-state check).

Verdict meanings: BLOCKING (halts, fix cycle); FOLLOW_UP (the Medium class: real weakness, no decision rests on it, goes to the follow-up ledger and the offer); NOTE (minor, ledger line only); SHOW_USER (the classifier will not decide; a person decides, or in an unattended run the reviewer's own label stands and the ledger row is flagged `unsettled`); UNDETERMINED (no usable answer at all: go to the fallback judge, section 6).

The cell (wrong N, D Y) is a disagreement worth logging: the text feeds a decision but nothing is wrong with it, so the finding is a note and the cell is counted in the metrics as a possible mis-answer.

### Step 3: design sketch that was run (not framework code)

The sketch is `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/blocker_truth_table_sketch.py` (a design artifact, not framework code; run with `uv run python <path>`). Version 2 (after the debate) was run with `uv run python`: all 6,400 combinations (S, W, E, D each in Y, N, U, UNSET; M and C each in Y, N, U, UNSET, NA) return exactly one verdict; a monotonicity check over answered states (raising an answered input from N to U to Y never lowers the verdict, on the order NOTE < FOLLOW_UP < SHOW_USER < BLOCKING) found 0 violations; and a no-silent-demotion check (a verdict below SHOW_USER must mean that no way of filling the UNSET answers could produce BLOCKING) found 0 violations. Two earlier defects: draft 1 let S = U return SHOW_USER ahead of an M = Y blocking verdict (511 violations of a monotonicity check that skipped UNSET); version 1 of this document claimed "monotone in every input" although moving an input from UNSET to an answer could lower the verdict (the debate found 432 such moves of 18,432), and it let a missing S, M, C or E answer file a finding as a note. Lesson for the spec: the truth table needs property tests (every combination has an outcome; monotone over answered states; no silent demotion from a missing answer), not only example rows. "Monotone in every input" is true only over answered states and must not be claimed more widely.

```python
def verdict(s, m, c, w, e, d):            # each argument is Y, N, U, UNSET (m and c may also be NA)
    if s == Y:
        return "BLOCKING"
    if m == Y or c == Y:
        base = "BLOCKING"
    else:
        wr = wrong(w, e)                  # Y if either Y; N only if both N; UNSET only if both UNSET; else U
        base = "SHOW_USER" if wr == UNSET else WD[(wr, d)]
    if any(x in (U, UNSET) for x in (s, m, c)) and ORDER[base] < ORDER["SHOW_USER"]:
        return "SHOW_USER"                # unsettled or missing safety, item or constraint answer: never a follow-up
    return base
```

The table `WD` is the 3 by 4 grid above. The wording lives in the question module; thresholds live in one small config; the table lives in code with its property test.

### What the table does not decide

- It does not decide that a finding is true. A reviewer can invent a wrong outcome (W = Y on a made-up narrative). The anchor read-back (quote byte-present, evidence excerpt read) happens in code before Jev, as in qa.md.
- It does not replace `/sc:implement` qa.md's own severity model. Inside that protocol the four checklist answers could be filled by Jev instead of the reviewer, with the parent's mechanical derivation unchanged; that is an option for the owner (section 8), not a requirement.

## 5. How confidence is derived

Jev's own numbers are inputs, not the verdict's confidence:

- A Noul returns only P(yes). It has no `confidence` field; the optional value is abs(2p-1) (`confidence.md`).
- Choice and Score return `confidence`, but it measures how concentrated the distribution is, "not the same as how likely the answer is to be correct" (SKILL.md, "Confidence is rarely the gate"). So the design gates on probabilities in code, never on the returned `confidence`.
- The docs call the probabilities calibrated. That claim is about TypeSafe's own benchmarks. Whether Jev's probabilities are calibrated for the question "does this finding name a wrong outcome" is UNVERIFIED and is exactly what the program's five runs against the scored table measure.

### Verdict confidence (code-computed, weakest link)

Let pS, pM, pC, pW (use max of pW and pE), pD be the Noul probabilities of the decisive questions (skipped questions contribute 0).

| Verdict | Verdict confidence c | Reading |
|---|---|---|
| BLOCKING by S, M or C | that question's p | one question carries it |
| BLOCKING by W and D | min(pW, pD) | both must hold; the min is an upper bound under any correlation (the product would assume independence, which is false because both read the same state) |
| FOLLOW_UP or NOTE | 1 minus flip, where flip = min(1, pS + pM + pC + min(pW, pD)) | the chance that a blocking path completes; the union bound is the safe choice for the costly error (auto-downgrading a real blocker). The cheaper "max" version is a variant to test, since the sum is pessimistic. |
| SHOW_USER | not defined | the table already says the classifier will not decide |

Routing by confidence (placeholders, from `patterns/probability-routing.md`: stricter for the riskier action):

| Action | Needs c at least | Else |
|---|---|---|
| Auto-downgrade to FOLLOW_UP or NOTE | tau_down (start 0.85) | SHOW_USER |
| Auto-confirm BLOCKING | tau_block (start 0.70) | SHOW_USER |

The riskier action is the downgrade, so it carries the higher bar. The classifier may downgrade only when confident; when it is not, the reviewer's own label stands and the ledger row says so. It never silently upgrades a non-blocking label to blocking (it can send the item to SHOW_USER).

### Stability (replicates)

No determinism is guaranteed and aliases change (`models.md`). Bundle all questions for one finding into one request (they run in parallel; `patterns/fan-out.md`) and send that request k = 3 times as separate requests (the vendor's repeatability cookbook changes a random identifier between requests to defeat caching, so an identical repeated request may return a cached answer; whether it does is UNVERIFIED). Pin the model id (`jev-1.14.0`, not `jev-latest`), take the median p, and treat a spread (max minus min) above 0.20 as U. The 0.20 is a guess. For scale: the vendor's repeatability cookbook reports an average absolute difference of 3.8 percent between repeats (8.4 percent on its worst claim) on insurance-claim checks, and says that average does not tell you the disagreement inside the 0.3 to 0.7 band. So band reliability for this task is unknown until measured. Our five runs of the scored table are themselves a repeatability test: report per-finding flip rate across runs next to agreement.

### Calibration step

After the five runs, bin verdict confidence c into 0.1-wide bins and report, for each bin, how often the classifier's blocking label matched the validated label. Set tau_down and tau_block from that reliability table on a training half of the rows and check them on a held-out half (SKILL.md yellow flag: "thresholds fitted to particular cases"). With 30 to 40 rows the held-out half is small, so report counts, not percentages alone.

### Cost for scale

A finding record is about 1 to 3 thousand tokens. At the listed $0.042 per million input tokens, 3,000 tokens is about $0.000126 per bundled request. Five runs of 40 findings with k = 3 replicates is 600 requests, about $0.08 (UNVERIFIED: price from the docs, no bill seen; rate limits are not stated in the docs, 429 is retried by the SDK).

## 6. The API key dependency and what works without it

### The dependency

Every Jev call needs an API key sent as a Bearer token (`TYPESAFE_API_KEY` for the SDK), issued from the TypeSafe console. None exists in this environment (section 1). This work did not create an account, did not request a key and did not call the API. Using a key later needs three owner actions the skill itself requires before live testing: permission to send data, a small experiment budget, and disclosure of what is sent ("point out any personal or private data").

What would be sent: the finding record fields listed in section 3. In this repository that is text from a private fork (specs, task files, code excerpts). The docs read give no standard retention period; they state zero data retention only "for enterprise customers" and a commitment not to train on user data (`legal.md`); they say nothing on confidentiality or data location. Whether the owner's account tier is enterprise is unknown. So the decision "may finding text leave this machine for TypeSafe" is the owner's and comes before any key is used.

Key handling if one is ever issued: environment variable only; never in the repository, a prompt, a settings file that is committed, a ledger or a payload log (log the request body, not the Authorization header); SKILL.md says "Keep API keys on the server", and here the local CLI process is the nearest equivalent.

### What can be done without a key

| Work | Needs key | Notes |
|---|---|---|
| Write the question module (wording, criteria, state fields) and the threshold config | no | the audited artifact; reviewable now |
| Write the truth table with its property tests (every combination has an outcome; monotone over answered states; no silent demotion from a missing answer) | no | sketch version 2 passes all three over 6,400 combinations |
| Build the `Judge` interface with four implementations: `JevJudge`, `LlmJudge`, `ReviewerJudge`, `FixtureJudge` | only `JevJudge` | the classifier code is the same for all four |
| Pre-write the exact request payloads for every scored finding as JSON files | no | a later run with a key is one command and reproducible ("keep the exact request payload for each case") |
| Run the five test runs against the scored table with `LlmJudge` | no | validates the characteristics, the table and the thresholds; does not validate Jev |
| Run the five runs with `JevJudge` | yes | the only way to measure Jev's agreement, flip rate and calibration |
| Cost estimate, risks, privacy decision | no | this document |

`LlmJudge` (the fallback judge): the same ten Noul questions and the same state, answered by a model that returns a probability per question. The repo precedent is `finding-grader` (blind, tool-less beyond Read, one JSON line per claim), which returns a boolean; the fallback would extend its reply to a probability plus a one-line reason. Differences from Jev to state plainly: an LLM's stated probability is not calibrated by construction; repeated sampling gives an empirical probability at higher cost and latency; and the model that wrote a finding must not also be the judge (use a different model class, as the reflect protocol does with heterogeneous reviewers).

`ReviewerJudge` is the status quo: the reviewer's own labels, as 0 or 1 probabilities. It is the baseline the other judges must beat or match.

Verdict-source field: every classifier result records which judge produced it (`jev-1.14.0`, `llm:<model>`, `reviewer`, `fixture`), because results from different judges are not comparable.

### When Jev is unavailable at run time

Order: `JevJudge`, then `LlmJudge`, then `ReviewerJudge`. If the last is the only one left, the reviewer's own label stands (today's behaviour, so there is no regression) and the ledger row records `classifier=unavailable`. A call error is never read as N.

## 7. Risks

| # | Risk | Evidence | Mitigation |
|---|---|---|---|
| 1 | Garbage in: the classifier judges the reviewer's description of the defect. A reviewer who writes a vivid wrong outcome gets W = Y. | Jev reads only supplied state (SKILL.md "Design the state") | code reads back the anchor (quote byte-present, evidence excerpt read) before any Jev call; unverified evidence is marked and lowers the verdict to SHOW_USER for blocking claims resting on it |
| 2 | A second reviewer in disguise: the classifier downgrades real defects and hides them in a follow-up list. | The run-2 override measured 11 to 6 blocking on one sample and that was a judgment call, not a count by a reviewer | S never downgraded; downgrade needs tau_down; shadow mode first (records the verdict beside the reviewer's label, gates nothing); sampled audit of FOLLOW_UP and NOTE rows by a fresh reviewer; a blocking finding re-grade is still allowed to override |
| 3 | The "decision basis" is not available for many deliverables. D is skipped, and every wrong-outcome finding falls to SHOW_USER. | D needs `decision_basis` from code; no such field exists today in review output (this document did not verify every deliverable kind) | the spec must name where `decision_basis` comes from per deliverable kind (a spec: requirements and acceptance table; a tasklist: acceptance criteria; a report: recommendation and quoted numbers) or accept that D is partial |
| 4 | Overfitting to 30 to 40 scored findings. | SKILL.md yellow flags: criteria naming test items, clauses added per failing case, thresholds fitted to cases | wording written once from the characteristics, not from the table; held-out half for thresholds; no per-case clause |
| 5 | Adversarial text in quotes (a finding quotes a deliverable that contains instructions). | `model-jaggedness.md`, Adversarial | label every quote as inert data; include hostile-quote cases; instruct nothing in the state |
| 6 | Alias drift and no determinism guarantee. | `models.md` | pin `jev-1.14.0`; record the model id in every result; rerun the table on a model change |
| 7 | Band reliability unknown (0.3 to 0.7). | `consistency_noul_cookbook`: average repeat difference 3.8 percent over 0 to 1 thresholds; says nothing specific to the band | replicates and spread rule; measure flip rate in the five runs |
| 8 | Privacy: finding text leaves the machine. | `legal.md`: ZDR only for enterprise; no confidentiality or location text | owner decision before any key is used; send excerpts only; redact secrets before sending |
| 9 | Vendor availability, key loss, price change, terms change. | none checked beyond the docs | the `Judge` interface and fallbacks; classifier is advisory in shadow mode, so an outage costs nothing |
| 10 | The validated table's labels are the ground truth, and they are human-and-agent judgments (1 to 5, averaged). Agreement with them measures consistency with the panel, not truth. | the program definition | report agreement with the label and the spread of the three scorers; do not claim accuracy |
| 11 | Jev cannot judge code. The docs give no statement on source code or long documents. | `introduction/coding-agents.md` (excerpt silent) | for findings about code, send the quoted lines and the stated outcome, test on code-type findings separately, expect weaker results |
| 12 | A truth table that is silent on a combination. | draft 1 of the sketch had a precedence bug (511 monotonicity violations) and version 1 of this document let a missing answer lower a verdict (found by the debate) | property tests for exhaustiveness, monotonicity over answered states and no silent demotion, in the plan |
| 13 | Scope creep: a classifier that calls Jev in every review loop adds latency and a network dependency to every gate. | none measured | classifier runs per finding once, caches by (finding hash, model id, question-module version), and never blocks on a call: timeout then fallback |

## 8. Recommendation and open points for the owner

### Recommendation

1. Build the classifier as questions plus a table in code with a `Judge` interface now (no key needed). Treat Jev as the preferred engine behind that interface, not as a dependency of the design.
2. Run the five test runs first with the fallback judge, and add a sixth set of five with `JevJudge` only after the owner has decided the privacy question and supplied a key. Report both against the same validated table. Jev earns its place only if it matches or beats the fallback on agreement and flip rate at lower cost and latency; the docs give no accuracy figure for this kind of task, so no superiority is assumed.
3. Ship in shadow mode (records beside the reviewer's label, gates nothing) before any gating, per the preamble's rollout.
4. Share the severity rubric: one set of 5 situations is the human 1 to 5 scoring rubric and the Jev Score levels.

### Owner decisions this document surfaces (each with a recommendation)

| # | Decision | Recommendation |
|---|---|---|
| J1 | May finding text (excerpts from the private fork) be sent to TypeSafe's API? | Decide before any key is requested. Recommended: yes for the five-run experiment only if the account has zero data retention or the processing contract is accepted; otherwise run the fallback judge only. |
| J2 | Request a TypeSafe key and a small experiment budget, or stay on the fallback judge? | Request one only after J1 is yes; the cost is about $0.08 for the five runs at the listed price (unverified). |
| J3 | Is the classifier allowed to feed `/sc:implement` qa.md's four checklist answers, or does qa.md keep its reviewer-answered model unchanged? | Keep qa.md unchanged in v1 (it already derives severity mechanically); revisit after shadow mode. |
| J4 | Is the fallback of last resort "the reviewer's label stands"? | Yes (no regression from today's behaviour). |

### Not verified

- No Jev call was made, so nothing here claims Jev's accuracy, calibration, or latency for blocker findings.
- Pricing, rate limits and retention beyond the pages read were not checked.
- The `decision_basis`, `required_items` and `constraints` fields do not exist in any review output read in this work; whether each deliverable kind can supply them is open (risk 3).
- The characteristics in section 3 come from four written rules (run-2 override, stoprule rubric, qa.md checklist, spec-panel severity text). The program's own derivation from 30 or more scored findings (step 01 inventory was still empty on 2026-11-15) may change, add or drop questions.

Status: Complete (design only; no Jev API call).
