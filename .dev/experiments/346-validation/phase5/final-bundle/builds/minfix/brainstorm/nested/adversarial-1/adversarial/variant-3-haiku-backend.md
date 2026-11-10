# Minfix: bounded, attributable revision transactions

## 1. Problem and evidence

**Decision:** treat a revision as a bounded transaction against a saved document, not permission to improve the document. A standard-library checker independently reconstructs the proposed document from a per-finding edit ledger, measures the changes and refuses admission to re-review unless it matches exactly and stays within budget. Keep PR 427's grading, changed-line review, seven bullets and three-review cap. Deliver only an additive `/sc:spec-panel-minfix` command and helper skill; do not change the original command.

Evidence read on 2026-11-08:

| Evidence | Observation | Consequence for this design |
|---|---|---|
| `exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md` | Control R3 critical+major mean 6.0; 427 mean 5.5. Growth after two cycles fell from 63.5% to 29.7%; no PASS. New treatment findings were 89% and 100% `origin=changed` in R2/R3. | Reporting size and asking for narrow edits reduced growth, not convergence. Measure introduced text, not just final size. |
| Same experiment's `phase4/ARMB-REPORT.md` | With 427's re-review flags: R3 proxy 6 and 1, mean 3.5; actual blocking 4 and 1; growth 27.8% and 32.1%. Still no PASS and the proxy bar failed. | Keep the flags, but do not credit them with a proven convergence effect. |
| `exp346-ab-flg-r2/.dev/orca-command-refactor/review/disposition.md` | The reviser applied all 13 blocking findings **and eight non-blocking findings**. F1 added `worker_status` and a mapping; F2-F4 added a path table and fallback. | Minor fixes need a zero-edit gate, not another reminder. Sharing a fix across findings must not multiply its budget. |
| Same run's `review/spec-panel-round2.md` and `review/disposition-round2.md` | All 13 old blockers resolved, six new blockers introduced. N1 arose from the Skill target fix; N2 from contract shape; N3 from path roots. The second reviser applied all 15 finding/citation rows, despite only six being blocking. | Attribution and low growth do not prove semantic correctness. Explicitly preserve the review of wrong outcomes. |
| Saved histories, independently inspected with `wc` and line-location diffs | Flagged r2: 57,763 / 70,255 / 76,328 bytes and 8,148 / 9,980 / 10,841 whitespace words. Control r1: 71,528 then 91,102 bytes. Many edits occupy one very long paragraph-line. | Count within edit spans; line count is not a size budget. Whitespace word counts here are evidence only, not the checker's token algorithm. |
| `docs/designs/spec-panel-review-loop.md`, section 5 design notes | The size limit was rejected because it conflicted with FR-8/FR-9 gap filling and “nothing could check it from text”. | A real checker answers the checkability objection; an explicit bounded override answers the gap-fill objection. |

The aim is a clean PASS, or an evidence-backed escalation with unchanged outstanding obligations, by review 3. An escalation is a safe stopping outcome, **not** an experimental clean pass. Predictions below are hypotheses, not measured results. This is a design, not an implemented or tested checker.

## 2. Mechanism (each loop step, in order)

### Step 1 — review and freeze the input

The coordinator saves the exact text being reviewed using 427's saved-copy convention. Never substitute a git ref: the specification may be untracked. The first review runs normally. A FAIL report before review 3 carries the Reviser brief and exactly one fenced `minfix-v1` JSON block before the final verdict. Its payload is:

```json
{
  "schema_version": 1,
  "review": 1,
  "findings": [
    {
      "id": "F1",
      "severity": "MAJOR",
      "blocking": true,
      "hard_gate": null,
      "wrong_outcome": "A consumer reads a status value the producer cannot emit.",
      "targets": [{"quote": "Exact existing sentence, table row or code line named by this finding."}]
    }
  ]
}
```

Include all findings, including minor ones, so an id cannot disappear by being omitted from the ledger. `severity` is exactly `CRITICAL|MAJOR|MINOR`; `hard_gate` is `null|FR-8|FR-9`. A CRITICAL or hard-gate finding must be blocking; a MINOR must not be blocking. A blocking MAJOR needs a nonempty `wrong_outcome`. The checker validates these structural rules, not the truth of the wrong outcome. IDs are unique within a report; identity is `(raw report SHA-256, finding id)`, not the id alone across rounds.

Each target quote is a verbatim sentence or smallest useful Markdown unit, not a whole section. A table row or code line may be used where sentence boundaries are meaningless. The helper finds each quote's one exact occurrence in the baseline and records UTF-8 byte offsets; zero matches or multiple matches stop preparation. For a repeated sentence the reviewer supplies a longer, unique quoted context. Gap filling names the existing incomplete row or guard sentence; adding text uses replacement of that anchor, not an unattributed free insertion.

Use the helper's `freeze` operation to register the saved copy, review report and targets **before dispatching the reviser**. It creates `cycle-1/state.json` exclusively, hashing raw baseline bytes and raw review bytes. If the baseline is not already saved, `freeze` can create it exclusively from the currently reviewed specification; if it exists, it must be byte-identical to that specification. Existing state with exactly the same inputs is an idempotent success; different contents are a conflict, not permission to overwrite. `state.json` holds `schema_version`, `policy_version` (`minfix-1`), `review`, `baseline_sha256`, `baseline_bytes`, `review_sha256`, and normalized findings with `targets[{start_byte,end_byte,quote}]`. Paths are explicit CLI arguments, not executable fields in JSON. A failed partial preparation leaves no valid state; re-running may reuse the identical saved copy, never a different one.

The coordinator keeps the state hash outside the reviser's allowed write set and passes it as a literal `--state-sha256`. The reviser may write only the candidate specification and its ledger. Baseline and state are made read-only as defense in depth; both hashes are checked again after revision and before the next review. Read-only mode does not protect against a same-user process that changes permissions: the independently recorded hash is the integrity check. A damaged or missing baseline stops the cycle; never recreate it from the candidate. This is detection, not protection against a malicious coordinator controlling every file and prompt.

### Step 2 — compute the budget, do not let the reviser choose it

The helper derives the class from the frozen finding. FR-8/FR-9 retain blocking status; they do **not** automatically get a larger budget.

| Class | Gross added words | Gross added UTF-8 bytes | Gross removed words | New headings | New requirement-id strings | Added normative tokens |
|---|---:|---:|---:|---:|---:|---:|
| MINOR, or non-blocking MAJOR | 0 edits | 0 | 0 | 0 | 0 | 0 |
| Blocking MAJOR, including FR-8/FR-9 | 60 | 512 | 120 | 0 | 0 | 2 |
| CRITICAL | 120 | 1,024 | 240 | 0 | 0 | 3 |
| One explicitly approved larger fix | at most 240 | at most 2,048 | at most 480 | at most 1 | at most 2 | at most 6 |

Additionally, the whole cycle permits at most **600 gross added words and 6,144 gross added bytes**, including overrides. These are initial engineering choices, not empirically optimized limits. Limits are ceilings, not targets. No budget banking between findings or cycles; splitting one finding into five edits retains one total allowance. Deletions cannot purchase additions. A shared edit has one owning finding id; optional `also_answers` links do not pool allowances. Even a zero-growth rewrite consumes gross insertions and removals. Minor corrections wait for a separate, authorized task; “this only fixes a wrong statement” is not an exemption.

### Step 3 — delete or narrow before adding; write a ledger

For each blocker, the reviser first considers removing the inaccurate claim, then narrowing it to what is supported, then replacing the smallest named unit. Addition is last. The ledger records why deletion and narrowing do not remove the wrong outcome when an edit adds words. This order is a prose judgment; the checker requires the record but cannot prove the consideration occurred.

`cycle-1/ledger.json` is one UTF-8 JSON object, no JSONL, comments, trailing commas or duplicate keys:

```json
{
  "schema_version": 1,
  "state_sha256": "<64 lowercase hex characters>",
  "dispositions": [
    {"finding_id": "F1", "action": "fix", "reason": "Narrow the status claim.",
     "delete_rejected_because": "The consumer still needs a status.",
     "narrow_rejected_because": "The replacement itself is the narrowed statement."}
  ],
  "edits": [
    {"finding_id": "F1", "also_answers": [],
     "start_byte": 120, "end_byte": 169,
     "before": "Exact original sentence, including its punctuation.",
     "after": "Exact replacement sentence, including its punctuation."}
  ]
}
```

The sample offsets and hashes are illustrative, not runnable S1 data. Every frozen finding has exactly one disposition: `fix|defer_minor|escalate`. `escalate` requires a reason naming the unmet obligation and needed decision; `defer_minor` is required for non-blockers. `fix` requires at least one real edit; `escalate` and `defer_minor` allow none. `also_answers` may name only blocking findings with `fix` dispositions. A finding answered only by another finding's edit may therefore have `fix` with an incoming `also_answers` link instead of its own edit. Validate that every such linked finding is actually named and receives coverage; semantic adequacy remains for the reviewer.

Offsets are zero-based half-open **baseline** byte ranges, never candidate offsets. Each edit must be contained within a target registered for its owner; `before` must equal those exact baseline bytes decoded as UTF-8 and quote the old sentence or named Markdown unit. Multiple edits cannot overlap; equal-position free insertions are unsupported. Reconstruct in ascending baseline order, copying every untouched byte verbatim. Compare the reconstruction with the supplied candidate byte-for-byte. Any discrepancy is `UNATTRIBUTED_CHANGE`; even formatting churn fails. The checker does not trust reported sizes or an LLM's diff. The document does not need finding-id decorations: the ledger supplies 427's paragraph/table attribution without growing the normative document.

### Step 4 — check, cut down once, or escalate

The coordinator runs `check` after the reviser and reads the JSON report. It measures every edit, aggregates by owner id, checks the cycle ceiling, and checks global additions of headings and ids so an insertion at a boundary cannot hide a new structure. The candidate is never automatically rewritten by the checker.

For a policy failure, return the offending edits and computed counters to the same reviser for **one cut-down attempt in that fix cycle**. It reconstructs again from the same frozen baseline, not by stacking repairs on an already failed candidate. Rejected edit bytes stay only in the failed ledger/report artifacts. Preserve `attempt-1` and `attempt-2` ledgers/reports; no renaming a failed attempt as a fresh cycle. Valid edits may remain; cut or remove failing edits and mark those obligations `escalate`. If the second check fails, admit nothing, retain the last accepted specification and escalate. A cut-down is not another review and does not reset 427's count. Never consume a re-review just to ask it to overlook a failed mechanical gate.

A finding needing more space gets `escalate`, never an invented larger fix. A checker-admitted candidate with escalated blockers may be reviewed once more to verify any other useful fixes, within the cap; its report must carry those blockers as open until independently resolved. If no edits are admitted, stop with the open obligations rather than rerunning an empty diff to manufacture progress. At review 3 there is no reviser dispatch, override or third fix cycle.

### Step 5 — a necessary larger fix requires a separate authorization

The reviser can request but cannot grant an override. The coordinator may authorize **one blocking finding per cycle**, only from a logged user approval or a finding's explicit reviewer recommendation for a necessary larger fix. The approval names why deletion/narrowing is insufficient and the concrete wrong outcome, not merely “important” or “FR-8”. FR-8/FR-9 are common legitimate reasons to request one; neither automatically qualifies.

`cycle-1/authorizations.json` is coordinator-owned, absent means no grants:

```json
{
  "schema_version": 1,
  "state_sha256": "<state hash>",
  "grants": [
    {"finding_id": "F1", "edits_sha256": "<hash of this finding's exact edits>",
     "approved_by": "coordinator", "approval_ref": "review-report:explicit-large-fix-F1",
     "reason": "The existing incomplete guard needs two specified branches.",
     "wrong_outcome": "The implementer chooses incompatible behavior for an empty input.",
     "narrower_fix_rejected_because": "Removing this mandatory guard leaves the same FR-9 gap.",
     "limits": {"added_words": 180, "added_bytes": 1500, "removed_words": 240,
                "new_headings": 0, "new_ids": 0, "normative_added": 4}}
  ]
}
```

Pin its coordinator-recorded SHA-256 on the checker invocation when supplied. The per-finding edit digest uses canonical JSON (`sort_keys=True`, compact separators, UTF-8 with `ensure_ascii=False`) of that finding's edit array in baseline-offset order. Any changed edit invalidates the grant. Nonempty approval fields are mechanically enforced; whether the external approval is real is a coordinator trust boundary. Self-authored ledger “reasons” do not count as approval. Grants can increase numeric ceilings only within the hard override row and cycle ceiling; they cannot authorize minor edits, baseline changes, changed finding grades, unknown ids, missing attribution, arbitrary scope, or a cap extension. More than one grant, an unused grant or a grant to a non-blocker fails closed. Larger needs go to the user as a separate design decision, not repeated automatic exceptions.

### Step 6 — re-review the accepted candidate, not its explanation

Only exit 0 plus matching current input hashes permits re-review. The coordinator passes 427's `--re-review` and `--baseline`. The variant resolves its gate inputs by convention: beside the prior review report, `minfix-cycle-N/` (N is that report's review number) contains `state.json`, `freeze-receipt.json`, `ledger.json` and `check.json`. `freeze` writes its identical stdout receipt to the exclusive `freeze-receipt.json` beside state; the coordinator records that receipt's state hash independently in its log before revision. The next reviewer uses that recorded receipt as its state pin; the receipt and state are outside reviser write scope. For nonstandard layouts, optional `--fix-ledger <ledger> --fix-check <report> --fix-state <state>` must be supplied all together; the receipt remains beside state. If any physical input is missing, malformed or stale, stop with an input error, never fall back to a first review. Re-run the checker and compare its inputs to the supplied report before reviewing, so an old PASS cannot admit a later candidate. This convention lets the experiment keep Arm B's briefs unchanged apart from the command name; the freeze/check actions are part of the variant contract, not extra instructions pasted into briefs.

The next reviewer first performs 427's prior-blocking outcome check against the actual candidate and source evidence, then reads the ledger/check report to locate changed spans, escalations and overrides. Ledger `fix` is a claim, not `resolved`; the report's `budget_ok` is not semantic PASS. Keep `origin=changed|unchanged`, the changed-line boundary-table scope and the final `verdict: PASS|FAIL`. A compliant small edit can still create a blocker; this mechanism does not suppress it.

## 3. Causes removed and causes left

| Measured cause | What the mechanism actually removes | What it leaves |
|---|---|---|
| Fix-induced `origin=changed` findings | Rejects large or unattributed changes before they enlarge the next review surface; one owner per edit prevents budget pooling. | A tiny wrong replacement can still cause a critical finding. Share of changed-origin findings may remain near 100% even when their absolute number falls; measure both. |
| Upward severity drift between rounds | Frozen grades prevent a reviser from increasing its own budget by relabeling a finding. | A new reviewer can legitimately or inconsistently increase severity. No frozen rubric or independent severity arbiter is added here. This is a residual cause, not solved by word counts. |
| Mechanism/section additions for minor findings | Minor and non-blocking MAJOR findings have zero edits; ledger reconstruction catches their edits even when described as harmless corrections. New headings and ids are zero by default even for blockers. | An invented mechanism can fit in 60 words and avoid headings, ids and the listed normative tokens. Detecting it remains semantic review. |
| No mechanical stop | Exit codes, a hashed baseline, exact reconstruction, fixed limits and a pre-review recheck provide a real stop when invoked. Missing or malformed inputs are errors, not defaults. | This is not a harness-enforced hook. A coordinator can skip the tool or ignore a nonzero exit. Static command tests cannot prove actual compliance; an experiment must show the checker receipt for each admitted candidate. |

“Delete or narrow before adding”, a truthful wrong-outcome description, a correctly scoped quoted target, a genuine external override approval and semantic finding resolution remain prose/human judgments. Required fields prove only that a model supplied text. The proposed runtime tests prove accounting and rejection behavior, not those judgments. Nothing here changes 427's severity model, FR-8/FR-9 obligations, or the requirement to escalate rather than silently drop a blocker.

## 4. Exact changes (file by file, with the new text or script outline)

### Maintainer change set

Paths in this table are repository editing destinations, not runtime lookups. Everything not listed remains unchanged.

| File | Exact responsibility |
|---|---|
| `src/superclaude/commands/spec-panel-minfix.md` — new | Copy the current `spec-panel.md`; change frontmatter `name`, title and command invocations to `spec-panel-minfix`. Keep all seven Review Loop bullet names and original cap/grading text. Add the three re-review inputs, replace bullet 6 below, append the admission rule to bullet 5, and add a `## Minimal fix gate` section containing the coordinator/helper lookup contract. |
| `plugins/superclaude/commands/spec-panel-minfix.md` — new | Same additive variant, copied from the new canonical variant; do not alter either existing `spec-panel.md` copy. |
| `src/superclaude/skills/sc-spec-panel-minfix-protocol/SKILL.md` — new | Operational contract from section 2, exact schemas, limits, coordinator ownership, helper lookup, examples and error decisions. No new reviewer or reviser agent. The command explicitly tells the coordinator and reviser to read this helper contract; the original panel behavior stays in the copied command, not in a second panel implementation. |
| `src/superclaude/skills/sc-spec-panel-minfix-protocol/scripts/fixcheck.py` — new | One dependency-free executable with `freeze` and `check` operations below. It never imports the package or invokes git, a network client or an LLM. |
| `plugins/superclaude/skills/sc-spec-panel-minfix-protocol/SKILL.md` and `plugins/superclaude/skills/sc-spec-panel-minfix-protocol/scripts/fixcheck.py` — new | Byte-equal packaged mirrors of the helper skill and script. |
| `tests/skills/test_spec_panel_minfix.py` — new | Static pins for the variant and mirror: seven one-line bullets, unchanged cap/grading and precedence literals, installed lookup order, usage flags, brief contents and no new source-path lookup. Check that the original command files are unchanged in the implementation diff. |
| `tests/skills/test_spec_panel_minfix_checker.py` — new | Runtime tests of actual CLI execution with temporary files, including data-integrity and rejection cases below. Fixtures are inline/generated in pytest temporary directories; no extra fixture files required. |
| `docs/designs/spec-panel-minfix.md` — new | This design's budgets, format definitions, installation note, experiment rules and limitations. It records a proposal, never a claimed measured success. |

Development copies under project `.claude/` are generated through the existing sync process and never staged. No CLI registration, package dependency, global rule, routing guide, `/sc:reflect`, rf-qa agent or `/sc:implement` change is part of this variant. Existing `tests/skills/test_spec_panel_review_loop.py` and severity pins stay unchanged and must remain green. They cover the original command; the new variant tests add coverage rather than weakening them.

The copied command currently contains a maintainer-source example-template lookup in Tool Coordination. In the **new variant only**, replace that source-path lookup with “use a caller-supplied release template; if none is supplied, use the inline output schema”. Do not introduce a runtime lookup of package examples under `src/`; the minfix helper and all new cross-primitive lookups use installed surfaces. This small compatibility correction is disclosed as part of the copy, not silently carried into the original command.

### Literal Review Loop amendment

Replace only bullet 6 in the new variant with this **single line**:

```text
6. **Reviser contract**: the report carries a `Reviser brief` just above the final `verdict:` line, listing only blocking finding ids and restating this bullet (the reviser reads the report, not the command), and omits it at `review: 3`, where the run escalates instead; revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; delete or narrow before adding; minor findings permit zero edits; each added paragraph or table cites its finding id in the external fix ledger, which quotes the exact old text and replacement; the reviser reports the byte size before and after; obey minfix-1 per-finding and cycle budgets, and run the helper checker before re-review; one cut-down attempt is allowed, then escalate the remaining blockers without expanding scope; a larger fix requires a separate, reasoned, hash-bound coordinator authorization within the hard ceilings; the Reviser brief names the frozen baseline, state, ledger and checker-report paths and repeats the helper-contract lookup.
```

Append these sentences to bullet 5, still on its existing single line, leaving its 427 content intact:

```text
For this variant a re-review requires the frozen state, freeze receipt, fix ledger and checker report from the helper's minfix-cycle-N convention beside the prior report, or the complete --fix-ledger, --fix-check and --fix-state override set; read the helper contract, rerun its checker against these exact inputs, and stop on missing, malformed, stale or nonzero results rather than falling back to a first review. Check prior blocking outcomes against the specification before reading the ledger's claimed dispositions; checker acceptance permits review but never proves a finding resolved, and escalated blockers remain open.
```

Append `[--fix-ledger <ledger.json> --fix-check <check.json> --fix-state <state.json>]` to the first variant Usage line. Add the JSON review block specification before the output formats without changing the last-line verdict. In `## Minimal fix gate`, include the exact helper lookup sentence:

```text
Read `~/.claude/skills/sc-spec-panel-minfix-protocol/SKILL.md` first, else the project `.claude/skills/sc-spec-panel-minfix-protocol/SKILL.md`; resolve the script relative to that same skill directory as `scripts/fixcheck.py`; if neither copy exists, stop and report the missing helper, never silently omit the gate.
```

The Reviser brief repeats that sentence because a reviser receiving only a report otherwise never learns the schemas. The section also restates freeze-before-dispatch and no successful checker receipt, no next review. This is the only added command contract, not an eighth Review Loop bullet.

### Helper CLI contract and script outline

Proposed invocation forms (new interfaces to implement, not existing commands):

```text
uv run --no-project python "<skill base>/scripts/fixcheck.py" freeze --spec "<reviewed spec>" --review "<review report>" --baseline "<saved copy>" --state "<state.json>"
uv run --no-project python "<skill base>/scripts/fixcheck.py" check --baseline "<saved copy>" --review "<review report>" --candidate "<revised spec>" --state "<state.json>" --state-sha256 "<coordinator pin>" --ledger "<ledger.json>" --output "<check.json>"
```

With an override, `check` also requires `--authorizations <file> --authorizations-sha256 <coordinator pin>` as a pair. Freeze uses the raw SHA-256 of its written state in its JSON receipt; the coordinator records that value independently. The existing issue-protocol script demonstrates the intended style: module docstring documenting CLI and errors, `argparse`, small pure validation functions, JSON output, `main(argv) -> int` and `sys.exit(main())`. No package reinstall or import is needed.

`check` reads inputs once as bytes, validates UTF-8 without newline normalization, rejects duplicate JSON keys and unknown schema fields, verifies all hashes and parses exactly one `minfix-v1` fenced block from the report. It cross-checks its round with the Markdown `review: N of 3` header and requires FAIL for a fix cycle. Only rounds 1 and 2 can be frozen for revision. It rejects empty files, unsupported schemas, duplicate ids, unknown referenced ids, absent dispositions, out-of-range or non-boundary byte offsets, overlapping targets with conflicting ownership, overlapping edits, no-op edits, unsupported free insertions, and mismatching quotes. Targets may overlap for related findings only if the resulting edit has one owner and explicitly links the others; otherwise preparation asks the coordinator to resolve the ambiguity. A `fix` disposition must be covered by an owned edit or incoming `also_answers` link.

Outline:

```text
freeze: validate source/report -> locate unique target quotes -> hash raw bytes
        -> create/validate saved copy -> create immutable normalized state -> receipt
check:  parse/validate -> verify pins -> reconstruct candidate from baseline + edits
        -> require exact candidate equality -> measure edits -> enforce limits/grants
        -> recheck source hashes -> atomic JSON report -> return defined exit code
```

Counting is deliberately lexical, specified rather than left to a model:

- Use `re.findall(r"\s+|\w+(?:[-'’/]\w+)*|[^\w\s]", text)` as lossless tokens; word tokens are those matching the middle alternative in full. No case folding, Unicode normalization or sentence splitter. An emoji or punctuation costs bytes but is not a word.
- Use `difflib.SequenceMatcher(None, before_tokens, after_tokens, autojunk=False)` for each ledger edit. Insert/replace output spans contribute gross inserted words and **all** their UTF-8 bytes, including whitespace and punctuation; delete/replace input spans contribute gross removed words. Identical tokens cost nothing. Sum all edits owned by one id before comparing with its allowance. Report gross removed bytes too, for diagnosis; the word removal ceiling limits destructive rewrites.
- Count added normative word tokens `MUST`, `SHALL`, `must`, `never`, `always` in inserted/replacement output spans, not net document totals. Moving or rephrasing may be charged again. A deletion elsewhere cannot offset them. This is a detector for these literal tokens, not a requirement-language parser.
- Scan Markdown ATX headings and setext headings outside fenced code blocks, comparing heading-text multisets baseline/candidate. Charge each new occurrence to the edit producing its heading line; an unassignable structural addition fails attribution. New-heading counts cannot be offset by deleting a different heading. Include a rename as a newly introduced heading text. Numeric section labels without Markdown markup are not detected as headings.
- New requirement-id strings match `\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+(?:[.-]\d+)*\b`, for example `WC-13`, `FR-9`, `AC-1.2`. A token absent anywhere in the baseline is new; count each added occurrence of such a token and charge it to the producing edit. Also report the sorted distinct new strings. Existing id references do not become newly invented ids. Snake-case fields and unlabelled new requirements are outside this detector and remain review concerns.
- Store both whole-document net sizes and gross edit counters. Report offsets and candidate line spans for each edit; retain the exact ledger text as the quote source. Enforce limits at equality-inclusive boundaries.

Resources are bounded: at most 2 MiB per specification/report/JSON input, 256 findings and 256 edits, and 8,192 tokens per individual edit side. Reject larger inputs as unsupported input, not partial success. S1's observed files fit the byte limit. Oversized quoted spans should be narrowed, not silently truncated. No arbitrary directory walking or file execution is allowed. Reject symlink input/output paths and any output aliasing an input inode; `freeze` also requires distinct source, baseline and state. Do not follow paths embedded in report text.

`check.json` is the authoritative machine result; stdout prints the same canonical JSON object plus newline. All fields below are always present; absent measurements are null or empty collections on errors:

```json
{
  "schema_version": 1,
  "policy_version": "minfix-1",
  "status": "ACCEPT",
  "exit_code": 0,
  "review": 1,
  "inputs": {
    "baseline_sha256": "<hash>", "review_sha256": "<hash>",
    "candidate_sha256": "<hash>", "state_sha256": "<hash>",
    "ledger_sha256": "<hash>", "authorizations_sha256": null
  },
  "totals": {
    "baseline_bytes": 57763, "candidate_bytes": 57800,
    "baseline_words": 8148, "candidate_words": 8154,
    "added_bytes": 90, "removed_bytes": 53,
    "added_words": 12, "removed_words": 6,
    "new_headings": 0, "new_ids": [], "normative_added": 0
  },
  "findings": [
    {"finding_id": "F1", "class": "blocking_major", "action": "fix",
     "budget_ok": true, "override_applied": false,
     "measured": {"added_words": 12, "added_bytes": 90, "removed_words": 6,
                  "removed_bytes": 53, "new_headings": 0, "new_ids": 0,
                  "normative_added": 0},
     "limits": {"added_words": 60, "added_bytes": 512, "removed_words": 120,
                "new_headings": 0, "new_ids": 0, "normative_added": 2},
     "edit_indices": [0], "violations": []}
  ],
  "edits": [{"index": 0, "finding_id": "F1", "baseline_range": [120,169],
             "candidate_lines": [4,4]}],
  "escalated_ids": [],
  "unattributed_ranges": [],
  "errors": []
}
```

Numbers above illustrate fields only; they are not internally measured S1 receipts. `status` is `ACCEPT|REJECT|ERROR`. Each violation/error is `{code, finding_id, edit_index, message}` with nullable id/index for global failures. Typical codes are `OVER_ADDED_WORDS`, `OVER_ADDED_BYTES`, `NEW_HEADING`, `NEW_ID`, `NORMATIVE_ADDITION`, `MINOR_EDIT`, `UNATTRIBUTED_CHANGE`, `STALE_INPUT`, `BAD_SCHEMA`, `AMBIGUOUS_QUOTE`, `OUTPUT_ERROR`. A report with `ACCEPT` and nonempty `escalated_ids` means accounting passed and unresolved obligations remain; it is not a review PASS.

| Exit | Meaning | Coordinator action |
|---:|---|---|
| 0 | Valid freeze receipt or accepted check; may include declared escalations | Continue only with matching hashes; retain escalations as open. |
| 1 | Valid inputs, policy/attribution failure | One cut-down attempt, then escalate; do not review the rejected candidate. |
| 2 | Bad CLI usage, `argparse` | Correct invocation; no revision or review consumed. No report is guaranteed. |
| 3 | Missing, empty, malformed, unsupported or unreadable input; missing parent directory | Stop with the named input error; do not substitute a default. |
| 4 | Baseline/state/review hash conflict, stale candidate during check, or conflicting existing freeze state | Stop; recover the original evidence or escalate. Never repin the candidate as baseline. |
| 5 | Unable to write/replace output safely | Stop; no usable admission receipt, even if all counters passed. |
| 70 | Unexpected internal failure | Stop and retain inputs for diagnosis; never convert to acceptance. |

For exits 1/3/4/70, attempt to emit an `errors`-bearing report when `--output` is usable. Exit 5 goes to stderr with no acceptance JSON on stdout. Diagnostics use stderr; do not put warnings before the JSON. Writes use an exclusive same-directory temporary file, flush/fsync, then atomic replacement for reports; cleanup failure is surfaced. Baseline/state creation is exclusive and never overwritten; partial writes cannot masquerade as complete state because hashes/schema are required. Freeze receipts use `{schema_version,status,exit_code,state_sha256,baseline_sha256,review_sha256,errors}`. Resolve parent directories beforehand; do not create speculative output trees.

No timestamps, random ids or absolute-path spellings enter the deterministic check report. Same bytes, policy and pins produce byte-identical JSON and the same exit code, even when `check` is run repeatedly. Checks do not advance review counts, mutate the specification, append ledger entries or alter baseline/state. Read the candidate hashes again before publishing the report; next-review rechecking still protects the later handoff window. Only the coordinator promotes an accepted candidate; a second SHA mismatch aborts promotion. Tool invocation is an accounting boundary, not an operating-system lock against concurrent writers.

### Required runtime tests

Test at least: identical-input idempotence; a zero-edit ledger with explicit escalations; a valid 60-word boundary and 61-word rejection; multibyte UTF-8 and byte-offset boundaries; punctuation/whitespace-only additions; gross rewrite despite zero net growth; no deletion credit; split edits sharing one cap; minor edits rejected; unknown ids; missing disposition; shared-owner accounting; exact reconstruction catching one unattributed byte; duplicate/ambiguous quotes; duplicate JSON keys; malformed/empty/missing files; unsupported schema; baseline/state/report tampering; stale receipt; input/output alias and symlink rejection; one valid override and changed-edit invalidation; excessive/multiple/minor/unused overrides; whole-cycle ceiling despite grants; heading rename/setext/fenced-code cases; new-id and normative-token counters; output failure; interrupted freeze and identical retry; CLI exit/status agreement. Tests run using UV and temporary directories only. Static pins and runtime checker tests are separate evidence.

## 5. Variant command name and install note

**Command name: `/sc:spec-panel-minfix`.** It installs beside `~/.claude/commands/sc/spec-panel.md`, never over it. The exact one-line experiment-brief substitution is:

```text
Replace each command invocation `/sc:spec-panel` with `/sc:spec-panel-minfix`; leave every other character and flag in the Arm B briefs unchanged.
```

This is an instruction to make a literal command-token replacement, not a request to rewrite prose or alter `/sc:spec-panel-*` names. Use Arm B's briefs, which already pass `--re-review` and `--baseline` for R2/R3; do not pretend that the original unflagged briefs exercise 427's re-review contract. New gate paths use the convention in section 2, so the three optional layout flags need not be added to those briefs. The first report's Reviser brief carries the ledger rule to the otherwise unchanged reviser brief. Coordinator freeze/check work is an explicitly measured part of the treatment.

D9 establishes that workers on this machine load commands from the personal command directory rather than the worktree's same-named copy. Therefore `make sync-dev` alone cannot deploy this experiment. After implementation and separate owner authorization, the experiment coordinator installs **only** the new command file and the new helper skill directory into their personal installed destinations. Do not run a broad force install, replace the original command, upgrade the package, or edit old experiment worktrees. Record full hashes of the original command before/after and of the new command, SKILL.md and checker; refuse collisions with a different pre-existing variant. An identical installation is a no-op; a differing file requires an explicit update decision, not silent replacement.

A fresh worker at repository base `2cb683f5` needs no new repository code: the additive command loads from the personal command directory and resolves the stdlib script inside `~/.claude/skills/sc-spec-panel-minfix-protocol/`. The project `.claude/skills/sc-spec-panel-minfix-protocol/` is only the second lookup surface for developer environments; it is not expected on that old base. Run the helper through `uv run --no-project python`, so the old checkout's package/dependency graph cannot control its imports. Before a measured loop, show that a fresh worker loaded the new command and executed the installed checker on a tiny valid and invalid fixture; merely reading a command file is not proof of invocation. If the helper is absent, halt rather than reinstalling from inside a worker.

Maintain an install watcher for all treatment files and the original command. A file change during a loop invalidates treatment delivery, even if tests later pass. Rollback removes only the additive files installed by this experiment after checking their hashes and ownership; the original command never needs restoration because this variant never changes it. No installation is performed by this design-writing task.

Later adoption is feasible but separate: `/sc:reflect`, rf-qa's Fix Cycle and `/sc:implement`'s final review can supply the same `(baseline, review findings, ledger, candidate)` contract, with an adapter for their severity names and their own caps. Do not inherit this command's three-review count into another protocol or let accounting widen `/sc:implement` acceptance criteria. Baseline/checker reuse is plausible; actual convergence benefits in those tools are UNVERIFIED.

## 6. Measurement plan and predicted numbers

Run S1, the same Orca worker-contract specification, from the byte-exact 57,763-byte draft on base `2cb683f5`, with the same overlay, model, briefs, worker setup and three-review/two-fix maximum as Arm B. Only replace the review command name as specified above; the additional coordinator gate actions are the treatment, not an undeclared brief change. Use two fresh independent replicates. Compare to D10 controls (R3 proxy 8 and 4, mean 6.0; growth 57.7% and 69.3%, mean 63.5%), and report Arm B's 6/1 and 27.8%/32.1% as a secondary comparator. Reused controls are not concurrent; explicitly retain that limitation. Do not selectively remove the contaminated low control after seeing results.

Retain D5 metrics unchanged:

- **M1:** reviews until clean PASS, cap or escalation; distinguish these terminal states.
- **M2:** findings per round, both the critical+major proxy and 427's actual blocking grade. An accounting escalation stays open; it never disappears from this count.
- **M3:** `origin=changed` share and absolute count; do not claim cross-arm comparability where origin was analyst-derived rather than reviewer-tagged.
- **M4:** bytes and lines at start and after each accepted fix cycle; growth `(accepted bytes - 57,763) / 57,763`. Record rejected candidates separately, never substitute their sizes or count a failed candidate as delivered.
- **M5:** tool calls/tokens if recoverable, plus wall-clock time, including helper calls, cut-downs and pre-review rechecks.

Add process diagnostics without replacing M1-M5: gross added/removed words and bytes per finding/cycle; new heading/id/normative counts; minor-edit rejection count; proportion of findings escalated rather than fixed; overrides requested/granted; cut-down rate; checker input failures and false positives; and any rejected candidate accidentally reviewed. Show the SHA-linked evidence chain for every accepted cycle: saved copy -> review -> state/receipt -> ledger/grant -> candidate -> checker report -> next review. Keep the experiment's origin/master-peek covariate, install watcher and no-human-edit window.

**Pre-run predictions, UNVERIFIED:**

| Metric | Control | Predicted minfix r1 / r2 | Mean prediction | Required bar |
|---|---:|---:|---:|---:|
| R3 open critical+major proxy | mean 6.0, spread 4 | 1 / 1 | 1.0 | at most 3; each replicate below both controls |
| Spec growth after two accepted cycles | mean 63.5%, spread 11.6 points | 12% / 18% | 15% | at most 44.4%; each replicate below both controls |
| Actual clean PASS by review 3 | 0/2 | 1/2 expected | not guaranteed | report separately; escalation is not PASS |

These are deliberately testable forecasts, not confidence intervals or arithmetic consequences of 427. At the hard cycle byte ceiling, two accepted cycles can add at most 12,288 gross bytes, so net growth is at most approximately **21.3%** of S1's original size even with overrides. The 44.4% growth bar should therefore be mechanically easy to meet if the gate is honored; it is insufficient evidence of convergence. The difficult prediction is reducing the next review's blocking defects without simply refusing useful work.

Keep all D10/D11 conditions: proxy mean at most 3 (or earlier clean pass), growth at most 44.4%, each treatment replicate on the better side of every control, and effects exceeding the larger within-arm spread. The predicted proxy reduction 5 exceeds control spread 4; predicted growth reduction 48.5 points exceeds control spread 11.6 and predicted treatment spread 6. Do not round the published 44.4% bar upward because one report printed 44.5%.

For an early justified escalation, record the terminal open proxy and actual blocking counts, not a fictional R3 review. For fixed-horizon display carry those outstanding obligations forward, explicitly marked as carried, never as independently reviewed or resolved. Carry the last accepted specification size forward for the two-cycle growth comparison. If both replicates halt through escalation with no clean PASS, report a safer bounded loop, **not proven convergence**, even if growth is low. Log the rejected fix and exact unmet decision so the owner can judge whether escalation was justified.

## 7. Risks, costs and what would falsify it

**Cost estimate, UNVERIFIED until a live loop:** zero mandatory additional agent sessions. Per fix cycle, one freeze invocation, one checker invocation, one receipt/report read and one pre-review checker re-run: about four extra tool calls, plus one ledger write and any authorization bookkeeping. Across two cycles, roughly 10 extra calls beyond the existing review/reviser file work. A cut-down adds a message, candidate/ledger edits and another check/read: approximately 4-6 calls per affected cycle. Worst allowed two-cycle treatment is therefore roughly 18-22 added calls, not “one free checker call”. Reusing existing disposition-writing calls may lower this; report observed counts rather than subtracting them optimistically.

Expected script CPU time for S1 is under a few seconds per invocation, but that is UNVERIFIED. Target quoting, ledger authoring and receipt handling likely add 2-6 minutes per cycle; a cut-down adds another 2-5 minutes. The total may add 4-12 minutes normally or 8-22 minutes with both cut-downs, plus one-time deployment/probing. No new reviewer sessions are required; a user escalation can add unbounded human waiting time and must be reported separately rather than hidden in script runtime. The implementation and experiment are not executed in this document.

| Failure mode | Consequence and containment |
|---|---|
| Under-fixing a real blocker | A 60-word ceiling can leave a cross-cutting consistency problem unresolved. Do not mislabel it minor; record escalation and let the next review check the actual wrong outcome. This can make convergence worse. |
| Escalation replaces work | An all-escalation zero-edit ledger trivially passes accounting. It retains all blockers and cannot count as clean PASS. Report escalation frequency and count early terminal obligations conservatively. |
| Counter gaming | Rewording may preserve matched tokens while introducing a new rule; synonyms avoid normative-token detection; a new field need not look like an id. Byte/word caps limit scale, not intent. Semantic review remains mandatory. |
| Oversized anchors | A whole long row can contain unrelated material. Freeze's target validation proves location, not relevance. The reviewer must name the smallest useful unit; the checker cannot prove that choice was minimal. |
| Coupled fixes | A single wrong outcome can require consistent changes in several distant statements. Aggregated per-finding budgets may punish the correct fix. One bounded, edit-hash-specific override is the release valve; if insufficient, escalate rather than split ids for more allowance. |
| Legitimate structure or terminology | Setext-like prose, a renamed heading, a cited new requirement id or a code example using `must` can trigger rejection. Show exact counters/locations; one cut-down or a justified override is available. Do not add heuristic exemptions after seeing treatment results. |
| Lexical diff oddities | SequenceMatcher alignment and whitespace tokens can charge a harmless move twice. Stable tokenization and regression fixtures make the rule reproducible, not semantically perfect. Never describe the counters as true semantic novelty. |
| Deletion removes required behavior | Narrowing/deletion may “fix” ambiguity by eliminating an obligation. Removal caps reduce the damage but do not establish scope preservation. The next review must recheck the original wrong outcome and FR-8/FR-9. |
| Approval becomes a loophole | A coordinator can rubber-stamp every request over time. One grant/cycle, hard maxima, no pooled budgets and digest binding restrict volume. Truthful approval provenance is still a trust/prose boundary; record it and audit grant frequency. |
| Fragile machine input from the reviewer | Malformed JSON, duplicate quotes or wrong byte anchors can stop a valid fix before it begins. `freeze` resolves unique literal quotes rather than asking the reviewer to invent offsets. Input correction is not a new review, but its calls/time count. |
| Concurrent change or damaged baseline | Fail closed on hashes. Do not auto-reset state, auto-revert another writer's changes or rebuild the saved copy from a candidate. The last accepted copy remains recoverable; the coordinator owns any explicit restore. |
| Checker or installation is skipped | The stop is mechanical only when executed. Receipt absence invalidates the treatment; original/variant hash drift invalidates delivery. No claim of a harness-level security barrier is made. |
| More artifact handling than the benefit justifies | JSON and hashes add cognitive load and tokens; tiny documents may be cheaper to review directly. This experiment is limited to the known large S1 failure, not a universal default. |

**Falsification:** the convergence hypothesis fails this screen if R3 proxy mean is above 3, either replicate is not below both controls, or the proxy effect does not exceed the larger within-arm spread, even if growth is tiny. The growth hypothesis fails if mean growth exceeds 44.4% or fails the spread/every-control comparison. Any unattributed or unapproved over-budget change reaching review falsifies enforcement. A baseline overwritten or a stale/malformed input producing exit 0 is an integrity defect and blocks release. Both runs ending only in escalation, or fewer introduced findings purchased by leaving more original blockers open, is a safer stop but not demonstrated convergence. A failed validity probe means no conclusion about the idea; do not relabel it a successful treatment.

The smaller alternative is another prose-only Reviser brief with size reporting; it already resembles 427 and cannot provide the requested stop. Skip a package CLI, database, automatic patch engine, extra reviewer agent, generic policy configuration system and harness hook. They add scope without being necessary to test this mechanism.

## 8. Open questions

1. **Are 60/120-word base budgets too restrictive?** Initial policy is fixed as `minfix-1`; do not tune it during the measured arm. Rejected-fix and escalation counts should drive a separately versioned follow-up, not silent exceptions.
2. **Does smaller text actually reduce new blocking outcomes?** This is the main experiment. Growth cannot answer it: the hard ceiling largely guarantees the size bar. Upward severity drift and small semantic defects remain live alternatives.
3. **Will the reviewer reliably supply unique, narrow quotes and machine-valid findings?** The checker can reject malformed output but not make the initial review insightful. Measure preparation failures; if high, improve the authoring helper in a separate iteration rather than weaken validation.
4. **How often are genuine large gap fills needed?** One override per cycle is deliberately restrictive. If S1 regularly needs several justified grants, report that this budget policy under-fits the task instead of expanding the grant mechanism mid-run.
5. **Should later versions enforce dispatch at harness level?** Not in this variant. A hook could make checker skipping harder, but requires a separate threat model and configuration change. Present receipt compliance is observed, not guaranteed by the harness.
6. **Which downstream protocol adopts it first?** No adopter is selected now. Reuse in reflect, rf-qa or implement needs its own severity mapping and evidence; S1 alone cannot justify a framework-wide rollout.

No schema, exit code, retry limit, ownership rule or baseline behavior is intentionally left open. Implementation must follow a checked plan after this design is selected; this variant authoring task makes no code, installation, Git or experiment changes.
