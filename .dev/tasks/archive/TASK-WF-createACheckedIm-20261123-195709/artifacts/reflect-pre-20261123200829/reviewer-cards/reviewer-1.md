# Analyzer review card

## Scope and evidence

Requested model: sonnet. Persona: analyzer. Full candidate/source/coverage matrix and historical report read, plus current help producers (commands.py:420-445 and 3773-3802), public registration, command reference, schema, root CliRunner tests and related suites. All source requirements checked against real code; no commands or file writes.

Verified no defect: two stale help producers are the bounded scope; correct JobSpec field guidance is documented; parser guard is valid; custom behavior and historical blockers are preserved. Red/green dependency order is coherent, with red failures required to be content failures rather than collection/import errors. Existing tests do not pin stale wording within the reviewer's search scope. No exhaustive repository claim.

## Findings

### F1: Help-token normalization ambiguity

- Label: MEDIUM. Grade: Medium, nonblocking. Follow-up candidate.
- Location: candidate Task 1/2 acceptance, lines 36 and 50.
- Claim: whitespace normalization followed by an exact option-token absence assertion could miss a token split at a hyphen by Click wrapping (`--custom- prompt-dir`). A partial fix that retains the wrapped stale option while adding correct field text could satisfy that negative assertion.
- Consequence: narrow false-pass risk for the negative guard, not the current red witness (positive JobSpec/custom_prompt_dir checks still fail). Task 4 additionally requires real public outputs without the option.
- Reviewer grounding: swarm max_content_width 100 at __init__.py:71 and textwrap's default hyphen behavior; live wrapping of eventual wording not observed.
- Remedy proposed by reviewer: remove all whitespace before the absence check, or explicitly handle wrapped forms. No plan edit is requested by this card's nonblocking grade.

### F2: Exact review-report filename

- Label: LOW. Grade: Note.
- Rejected as a blocking defect: Task 4 and Constraints already require a persisted independent applied-fix report under ./artifacts/ checking exact diff/public surfaces and unchanged inline/guard/metadata behavior. A fixed basename changes form, not the deliverable.

### F3: Excluded path placeholder

- Label: LOW. Grade: Note.
- Rejected as a defect: run help's `<custom-prompt-dir>/system.txt` is not the rejected CLI option and is outside these two public help surfaces. Historic report and plan explicitly exclude it. Loose standalone `custom` text is not a defect because positive JobSpec/custom_prompt_dir assertions carry the discrimination.

## Verdict

PASS: zero blocking findings, one Medium follow-up candidate and two Notes. No correctness gap established. Coverage-tool availability and final live wrapping remain future implementation observations; the plan requires honest failure reporting. No applied fix or test result claimed.

## Calibration

Independent fresh-context calibration: C=0.81; scores [0.85, 0.85, 0.75, 0.80, 0.80], five-dimension arithmetic mean. See ../reviewer-calibrations/reviewer-1.md. Calibrator model-class diversity degraded; calibration is not independent by class.
