---
title: "Locked Detection Contract Setup Flow for /sc:reflect and /sc:pr-submit"
status: brainstorm-merged
domain: code
strategy: systematic
convergence_score: 0.87
created: 2026-07-01T14:26:34+00:00
---

# Locked Detection Contract Setup Flow for `/sc:reflect` and `/sc:pr-submit`

## 1. Recommended Product Behavior

Implement a shared, evidence-first contract setup helper and integrate it conservatively:

1. `/sc:pr-submit --monitor >=1` keeps the existing fail-closed arming gate. If no locked contract resolves, it stops before arming and prints a structured diagnosis plus the next safe setup command.
2. `/sc:reflect` gains a contract-readiness diagnostic/reporting path. In v1 it should diagnose and validate readiness; it should not write the local locked contract by default.
3. A shared helper under `src/superclaude/pr_submit/` owns contract diagnosis, probe evidence loading/capture, candidate derivation, classifier validation, validation reports, and local locked-contract writing.
4. The shipped detection contract remains `locked: false` and generic. Repo/operator-specific locked data lives only under `.dev/pr-monitor/`.
5. Contract creation never arms the monitor, posts comments, pushes, resolves threads, retries, retriggers, or resumes `/sc:pr-submit` without an explicit separate confirmation.

## 2. Ownership Boundary

### `/sc:pr-submit`

Owns:

- PR creation and monitor ordinal behavior.
- Monitor arming.
- Poll loop, FSM, retry/retrigger, validation, push/reply/resolve side effects.
- The fail-closed check that refuses to arm unless `DetectionContract.for_arming()` resolves a locked contract.

New behavior:

- On missing/unusable locked contract, call the shared diagnosis helper to render a better halt message.
- Offer a setup command or optional interactive setup entry, defaulting to stop.
- Do not continue into monitor arming after setup in v1; tell the operator to rerun `/sc:pr-submit --monitor >=1`.

### `/sc:reflect`

Owns:

- Readiness diagnostics.
- Optional validation reporting against existing probe evidence.
- Concise status output that does not dump raw GitHub payload bodies.

Does not own in v1:

- Default contract writing.
- Monitor arming.
- PR mutation or monitor resume.

### Shared helper

Owns:

- Contract state diagnosis.
- Probe payload loading and later optional capture.
- Candidate derivation from observed evidence.
- Validation through existing classifier/poll seam.
- Validation report and local lock writing.

## 3. UX States

The helper should classify contract readiness into explicit states:

| State | Meaning | Default action |
|---|---|---|
| `missing` | No local override exists; shipped fallback is unlocked | Print setup command and stop |
| `unlocked` | Local or shipped contract exists but `locked: false` | Validate candidate if evidence exists |
| `unparseable` | Contract file exists but YAML cannot parse | Preserve file; offer regenerate from evidence |
| `evidence_missing` | `locked: true` exists but `probe_evidence` missing/unreadable | Re-probe or revalidate before use |
| `validation_missing` | Evidence exists but no validation report | Run validation |
| `validation_failed` | Validation report exists but failed | Show blockers and alternatives |
| `stale` | Repo/PR/hash/freshness policy mismatch | Revalidate or recapture |
| `ready` | Local locked contract validates against evidence | `/sc:pr-submit --monitor >=1 --pr <number>` may proceed through existing gate when supplied the existing PR number |
| `declined_by_user` | User cancels setup | Leave existing contract untouched |

## 4. Proposed Question Sequence With Defaults

The setup flow should ask a bounded sequence. Defaults may be accepted only when evidence supports them.

1. **Repository** — “Use resolved repo `<owner/repo>`?”
   - Default: current resolved origin repo.
   - Required for provenance and all `gh` calls.
   - If unresolved, require explicit `owner/repo`.

2. **Probe PR** — “Which PR contains a recent Augment-authored payload?”
   - Default: current PR if known.
   - Required for evidence provenance.

3. **Operation** — “Diagnose only, validate existing evidence, or capture/validate/offer write?”
   - `/sc:reflect` default: diagnose only.
   - setup helper default: capture/validate/offer write.
   - `/sc:pr-submit` missing-contract halt default: print setup command and stop.

4. **Evidence source** — “Fetch current GitHub payloads or use existing captured JSON?”
   - V1 default: use existing captured JSON or file-based validation path.
   - V2 optional: fetch current state using pinned `--repo <owner/repo>`.

5. **Surfaces to inspect** — “PR reviews, issue comments, check runs, or all?”
   - Default: all supported surfaces.
   - Omitted surfaces are recorded in validation report.

6. **Detected Augment identity** — “Lock this observed bot/app identity?”
   - Default: exactly one observed Augment-authored identity.
   - If multiple candidates, require explicit selection.
   - If no observed identity, stop; do not lock.

7. **Author association values** — “Use these observed author associations?”
   - Default: observed values.
   - If absent, empty is allowed only if classifier validation does not require it.

8. **Emission shape** — “Which observed surface is primary?”
   - Options: `review`, `issue_comment`, `check_run`.
   - Default: surface with decisive observed findings/completion signal.
   - Cannot lock an unobserved surface.

9. **Findings locus** — “Use this observed field path?”
   - Defaults by surface are internal classifier paths such as `<review-findings-field>`, `<comment-findings-field>`, or `<check-run-findings-field>`; raw body-bearing JSON paths are never printed in readiness/status summaries.
   - Must resolve against captured payload when findings are present, while normal summaries report only path-resolution status/counts rather than the raw field path or payload body.

10. **Severity field path** — “Use this observed severity path or `null`?”
    - Default: observed machine-readable path if present, else `null`.
    - Absence is allowed, but report must record that severity was not field-backed.

11. **Review completeness signal** — “What observed signal means review is complete?”
    - Default: observed terminal review state, summary marker, or completed check-run conclusion/output marker.
    - Must distinguish complete from pending/polling.

12. **Decline detection fields** — “Use existing decline defaults and validate if evidence exists?”
    - Defaults: current regex/trigger values from the shipped contract.
    - V1 policy: lack of decline sample emits warning `decline_validation: not_exercised`; it does not block an otherwise validated lock.

13. **Expected classifier result** — “What should the captured payload classify as?”
    - Default from evidence: `findings`, `clean`, or `declined`.
    - `polling` is never lockable.

14. **Run validation** — “Dry-run existing classifier against captured payload and candidate?”
    - Default: yes.
    - Required before `locked: true`.

15. **Write local locked contract** — “Write `.dev/pr-monitor/detection-contract.locked.md`?”
    - Default: no.
    - Requires explicit confirmation after validation passes.
    - Does not arm monitor.

16. **Next step** — “Print rerun command?”
    - Default: yes.
    - Print absolute artifact paths and the recommended `/sc:pr-submit --monitor >=1 --pr <number>` command for an existing PR; do not execute it.

## 5. Contract Fields

Preserve the existing classifier-critical schema:

```yaml
augment_bot_login: "<observed>"
augment_author_association: ["<observed>"]
augment_app_slug: "<observed-or-null>"
emission_shape: "<review|issue_comment|check_run>"
findings_locus: "<observed-json-path>"
severity_field_path: "<observed-json-path-or-null>"
review_completeness_signal: "<observed-terminal-signal>"
probe_evidence: "<path-to-captured-payload>"
decline_phrase_regex: 'abnormally\s+large'
decline_retrigger_regex: 'comment\s+["''`*_]*(augment|auggie|augmentcode)\s+review["''`*_]*'
accepted_trigger_phrases: ["auggie review", "augment review", "augmentcode review"]
locked: true
```

Recommended v1 metadata extension, ignored by the classifier:

```yaml
metadata:
  schema_version: "1.0"
  generated_by: "superclaude.pr_submit.contract_setup"
  generated_at: "<ISO-8601>"
  repo: "<owner/repo>"
  pr_number: <number>
  evidence_sha256: "<sha256>"
  validation_report: "<path>"
  validation_result: "passed"
  validation_classifier_result: "<clean|findings|declined>"
  validated_surfaces: ["reviews", "comments", "check_runs"]
  decline_validation: "passed|not_exercised|failed"
```

## 6. Safe Locking Policy

A contract may be written with `locked: true` only when all are true:

1. Evidence payload exists and is readable.
2. Evidence is tied to the resolved repo.
3. PR identity is recorded; cross-PR evidence is explicit and can validate shape only, not current review state.
4. An Augment-authored actor/app identity is observed in payload metadata, not prose alone.
5. Selected emission shape is observed.
6. Required findings or completion signal paths resolve against evidence.
7. Expected classifier result is `clean`, `findings`, or `declined`, never `polling`.
8. Existing classifier/poll seam returns the expected result with the candidate contract.
9. Non-Augment or empty-payload negative controls do not falsely classify as reviewed.
10. Validation report is written and references evidence hash.
11. User explicitly confirms writing the local lock.
12. Target path is `.dev/pr-monitor/detection-contract.locked.md`, never the shipped ref and never `.claude/` mirrors.

Defaults that are acceptable only as suggestions:

- Common bot login display.
- Common app slug.
- Common findings path names.
- Decline regex defaults.
- Freshness threshold.

Values that must never be guessed for `locked: true`:

- `augment_bot_login` / app identity.
- `emission_shape`.
- `findings_locus` when findings exist.
- `review_completeness_signal`.
- `probe_evidence`.
- Repo binding.

## 7. Validation Checklist

### Structure

- YAML parses.
- Required fields exist.
- No placeholders remain in required fields.
- Candidate loads through existing `DetectionContract.from_yaml()`.
- Shipped contract remains `locked: false`.

### Evidence

- Payload file exists under `.dev/pr-monitor/probes/` or is copied there.
- Evidence hash is recorded.
- Repo and PR are recorded.
- Capture time is recorded.
- Surfaces inspected are recorded.
- Pagination/incompleteness is diagnosed when known.

### Identity

- Selected actor/app appears in payload metadata.
- Similar human-authored or copied text is ignored.
- Multiple candidates require explicit selection.

### Surface and path

- Selected surface exists in payload.
- Findings locus resolves when findings exist.
- Completion signal resolves for clean/no-findings evidence.
- Severity path resolves if non-null.
- Check-run status is terminal before using it as completion.

### Classifier dry run

- Candidate + payload returns expected non-`polling` state.
- Empty payload does not classify as reviewed.
- Non-Augment-authored payload does not classify as reviewed.
- Decline evidence, when present, returns `declined` and remains distinct from `clean` and `polling`.

### Freshness

- Repo mismatch blocks lock.
- Missing evidence file/hash blocks lock.
- Same PR is preferred.
- Cross-PR evidence requires explicit confirmation and only validates contract shape.
- Age warning defaults to 30 days in v1 unless project policy tightens it.

## 8. Output Artifacts

All generated artifacts go under:

```text
/config/workspace/IronClaude/.dev/pr-monitor/
```

Recommended layout:

```text
/config/workspace/IronClaude/.dev/pr-monitor/
  detection-contract.locked.md
  probes/
    <YYYYMMDD-HHMMSS>-pr-<number>/
      gh-reviews.json
      gh-comments.json
      gh-check-runs.json
      combined-payload.json
      candidate.detection-contract.md
      validation-report.yaml
      validation-summary.md
```

Normal `/sc:reflect` and `/sc:pr-submit` summaries should display status, artifact paths, hashes, path-resolution counts, and blockers, not raw payload bodies or body-bearing classifier paths.

## 9. `/sc:pr-submit` Integration

When `--monitor >=1` and no locked contract resolves:

1. Preserve current halt.
2. Run diagnosis helper.
3. Print checked paths and status.
4. Print setup/diagnose command.
5. State: “No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.”

Example next step text:

```text
Next safe step:
  superclaude reflect contract-status --repo <owner/repo> --pr <number>

Or validate captured evidence with:
  superclaude reflect contract-status --validate --repo <owner/repo> --pr <number>
```

After a lock is written, `/sc:pr-submit --monitor >=1` should simply rerun the existing `DetectionContract.for_arming()` path.

## 10. `/sc:reflect` Integration

Add a narrow readiness path:

```text
superclaude reflect contract-status --repo <owner/repo> --pr <number>
superclaude reflect contract-status --validate --repo <owner/repo> --pr <number>
```

In v1:

- Diagnose contract state.
- Validate existing evidence if requested.
- Print readiness and blockers.
- Recommend helper command.
- Do not write local lock by default.
- Do not arm monitor.

## 11. Minimal Implementation Plan

1. **Add structured diagnosis helper** near `src/superclaude/pr_submit/detection.py` without changing `for_arming()` semantics.
2. **Improve `/sc:pr-submit` halt message** using diagnosis output; keep monitor unarmed.
3. **Add file-based probe validation** that consumes captured JSON fixtures and writes validation reports under `.dev/pr-monitor/probes/`.
4. **Add candidate contract builder** that records field provenance and refuses required unobserved fields.
5. **Validate through existing classifier** with expected result and negative controls.
6. **Add safe writer** for `.dev/pr-monitor/detection-contract.locked.md`, explicit confirmation required.
7. **Add `/sc:reflect` contract status reporting** as diagnose/validate-first, not write-first.
8. **Add optional GitHub capture** after file-based validation is tested; all capture commands must pin `--repo <owner/repo>`.
9. **Add regression tests** for T-210, local override preference, wrong/stale evidence, non-Augment copied text, and no monitor side effects.

## 12. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Arming gate weakened | Do not change `DetectionContract.for_arming()` semantics; add regression tests |
| Skill markdown duplicates classifier | Keep derivation/validation in Python helper; skills render results |
| Defaults become accidental guesses | Field provenance; lock requires observed/validated status |
| `/sc:reflect` scope creep | Diagnose/validate-first v1; no default writes or monitor side effects |
| Live `gh` assumptions wrong | File-based validation first; live capture second |
| Stale/wrong evidence locks contract | Repo/hash mismatch blocks; cross-PR explicit and shape-only |
| Operator confuses lock with monitor armed | Always print “No monitor was armed” after setup |
| Probe payload leakage | Summaries show paths/hashes/status and path-resolution counts, not raw payload bodies or body-bearing classifier paths |

## 13. Acceptance Criteria

1. `/sc:pr-submit --monitor >=1` still halts with only shipped `locked:false` contract.
2. Halt message is actionable and names the local override and setup/diagnose path.
3. `/sc:pr-submit --monitor 0` remains unaffected.
4. Defaults alone cannot produce `locked: true`.
5. Candidate with classifier result `polling` cannot lock.
6. Wrong-repo evidence cannot lock.
7. Cross-PR evidence is explicit and cannot assert current PR review completion.
8. Non-Augment-authored copied text is ignored.
9. Decline, no-findings, and no-evidence are distinguished when fixtures exist.
10. `/sc:reflect` reports readiness without dumping raw payloads.
11. Local locked contract is written only under `.dev/pr-monitor/` after confirmation.
12. Shipped contract remains unlocked and generic.
