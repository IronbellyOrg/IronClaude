# GATE-0 — Phase 0 Aggregate Freeze

Output root: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z`

## Decision

`halt=false`

Evidence is sufficient to freeze both BASE_COMMIT and the canonical escape set for the troubleshoot meta-investigation.

## BASE_COMMIT

`94d5baa05f6319b8ff6f2e1db8e8b7737465daaf`

Rationale:
- `timeline.md` identifies `94d5baa05f6319b8ff6f2e1db8e8b7737465daaf` as the first-parent commit immediately before PR #151's fix/merge.
- `defect-escape-table.md` repeats the same BASE_COMMIT.
- `git-log-prd-reflect.txt` shows PR #151 merge `7601ad25` and fix commit `235f59ee` immediately after `94d5baa0` on the relevant first-parent sequence.

## Canonical escape set

| ID | Symptom | Fix ref | Missed / unmasked | Pipeline should have caught | Evidence |
|---|---|---|---|---|---|
| E1 — PRD cloud `--file` misuse | Headless `superclaude prd run --spec` crashlooped at `scope-discovery` because PRD passed local filesystem paths to Claude CLI `--file`, which is a cloud-download/session-token mechanism. | PR #151 / merge `7601ad2548e232ce89219908f726d4e35fe41412`; fix commit `235f59ee101032606cccb315105191c428621531`. | Missed runtime-entrypoint verification and sibling-pipeline contract sweep; roadmap/tasklist/validate already forbade `--file` while PRD still emitted it. Tests inspected command construction without exercising the headless subprocess path. | Headless PRD `--spec` e2e with no session token; cross-pipeline grep/contract guard proving no local file path is delivered via `claude --file`. | `defect-escape-table.md` row PRD-E04; `pr-targets-summary.txt` lines 1-16; `pr-broader-summary.txt` lines 49-63; `timeline.md` line 19; `pipeline-artifact-audit.md` rows E3 and findings lines 38-45. |
| E2 — final completion phase false positive | STRICT `parallel_instructions` gate halted a live heavyweight PRD build-task-file run because final sequential completion/presentation Phase 7 lacked parallel keywords. | PR #154 / merge `e97aa4fd2a9d317abdc19f6ce2b5ccd35497df0e`. | Missed executable-work-phase vs setup/completion-bookend contract; implementation checked every phase >=2 despite the intended middle-work-phase scope. | Live/generated 7-phase PRD task-file gate fixture with sequential final completion phase; invariant test aligning parser scope with heavyweight template phase semantics. | `defect-escape-table.md` row PRD-E05; `pr-targets-summary.txt` lines 60-70; `pr-broader-summary.txt` lines 81-96; `timeline.md` line 21. |
| E3 — Task-Log findings-heading sibling false positive | After #154, the same STRICT parallel gate halted again because loose phase-heading matching consumed Task-Log placeholder headings such as `### Phase 2 - Codebase Research Findings` and failed on empty placeholder content. | PR #155 / merge `eb9a2633bfc49b96f2a677fd907a68976f2a5fd9`. | #154 fixed only the observed final-phase case and did not unmask-and-sweep all generated heading surfaces; hard gate severity made parser false positives expensive. | Parser-focused sweep over full generated MDTM task files including Task Log headings; adversarial false-positive suite for headings outside the executable phase plan; hard-vs-advisory severity review. | `defect-escape-table.md` row PRD-E06; `pr-targets-summary.txt` lines 81-99; `pr-broader-summary.txt` lines 97-112; `timeline.md` line 22. |
| E4 — PRD/generic/trailing evaluator divergence | PR #155 intended `parallel_instructions` to warn instead of halt, but normal PRD runtime uses `PrdExecutor._evaluate_gate`, not generic `pipeline.gates.gate_passed`; the PRD evaluator still treats any non-True semantic check result as fatal and ignores `SemanticCheck.advisory`. | PR #155 / merge `eb9a2633bfc49b96f2a677fd907a68976f2a5fd9`; unresolved/off-path divergence documented by the A2 contract report. | Missed contract-implementation enumeration and runtime-entrypoint verification; semantic checks are consumed by generic blocking gates, PRD runtime gates, trailing gates, and generic cosmetic remediation dispatch. | Runtime call-graph proof for `superclaude prd run`; sweep of every `semantic_checks` consumer whenever `SemanticCheck` contract changes; PRD-specific regression proving advisory failure does not HALT the real PRD evaluator. | `contract-implementations.md` executive finding lines 14-19; runtime call chain lines 20-29; implementation inventory lines 41-78; concrete candidates lines 141-145. |
| E5 — POST-reflect wrong diff base | Generated POST-reflect item used `/sc:reflect --mode post --diff <start_commit>..HEAD`; when task changes were uncommitted it audited none of the actual work, and when unrelated commits landed it audited foreign work. | PR #153 / merge `10723863389b8fce9cf9474b3f628c963725daf8`. | Reflect was wired into task-builder/sc:tasklist, but not verified against actual `/task` runtime semantics where work is commonly uncommitted. Off-path review existed but could point at the wrong diff. | Dogfood task-builder/self-run POST-reflect e2e that edits the working tree without committing and verifies the effective diff includes task files while excluding foreign commits. | `defect-escape-table.md` row REFLECT-E01; `pr-broader-summary.txt` lines 65-80; `timeline.md` line 20; `pipeline-artifact-audit.md` lines 42-45. |

## Gate-0 rationale

The required inclusions are evidenced and present:

- `--file` misuse: E1.
- completion-phase false positive: E2.
- unmasked findings-heading sibling: E3.
- dual/triple evaluator divergence: E4.

E5 is included because it is repeatedly evidenced as a meta-pipeline escape in the supplied Phase 0 artifacts and directly affects the reliability of off-path review evidence used during the PRD saga.

## Warnings

- This aggregation is evidence-freezing only. It does not attempt a product/source fix.
- E4 is an active-looking divergence in the current code path per `contract-implementations.md`; it is included as a canonical escape because the PRD runtime entrypoint and generic gate evaluator disagree on the advisory contract.
- Artifact line numbers are cited from the Phase 0 agent artifacts read for this aggregation.
