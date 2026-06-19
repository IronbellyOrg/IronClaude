# sc-swarm-wizard-protocol — Eval Run (with_skill)

## Plain-language summary (what the wizard would tell the user)

You wanted to find weird inputs or states that would crash or break your parser
(`/tmp/swarm-wizard-probe/demo.py`). That maps to the **edge-case-hunt** lens —
the one whose whole job is "what inputs/states break my code?" It fans the file
across **4 independent reviewers** (this lens's default is 4, not the usual 3,
because edge-case hunting benefits from broader coverage).

You asked for a **practice run first**, so I ran it with the **stub transport** —
deterministic, no credentials, no network, and done in well under a second. It is
the mandatory dry-run that every wizard run does before any real run.

**The practice run worked — the pipeline is healthy (exit 0, 4/4 reviewers
finished, terminal state reached, contract written).** Important caveat: a stub
run produces **placeholder text, not a real review**. It only proves the
machinery end-to-end. To get actual edge-case findings you'd run the same plan
with `--transport openai_compat` against your configured T2 proxy — but that is a
separate, explicit go-ahead, which this practice run did not authorize.

## Resolved plan

| Field | Value |
|---|---|
| lens | `edge-case-hunt` |
| transport | `stub` (mandatory dry-run; practice run requested) |
| target | `/tmp/swarm-wizard-probe/demo.py` (195 non-ws bytes — clears the IMM-4 50-byte floor) |
| reviewers | 4 (lens default for edge-case-hunt) |
| output_dir | `.dev/swarm-runs/edge-case-hunt-20260619T060941` |
| dry_run_passed | yes |

## Verification evidence

- Pre-flight: target exists; 195 non-whitespace bytes ≥ 50 (IMM-4 floor cleared).
- `swarm validate-lenses` → `registry OK (8 entries inspected, 7 validated)`, exit 0.
- Live `run --help` cross-checked vs `refs/cli-contract.md` flag table — match
  (including the noted stale `--transport` help text that says "openai_compat
  default" while the `--lens` expansion default is actually `stub`).
- Dry-run stdout: `swarm run: dispatched job (mode=lens, workers=4, results=4)`, exit 0.
- `.swarm-state.json` → `state: "terminal"` (job_id `lens-edge-case-hunt-d584e59b`).
- `return-contract.yaml` present → `status: success`, `workers_requested: 4`,
  `workers_succeeded: 4`, `workers_failed: 0`.
- Artifacts written: 4× `*.final.md` + 4× `*.meta.json`, `merged.md`,
  `return-contract.yaml`, `manifest.json`, `execution-log.{jsonl,md}`.
  (`done.json` correctly absent on an inline run.)

## Return Contract (typed)

- status: `cancelled` (green dry-run; no real run authorized — practice run only)
- lens: `edge-case-hunt`
- transport: `stub`
- target: `/tmp/swarm-wizard-probe/demo.py`
- output_dir: `.dev/swarm-runs/edge-case-hunt-20260619T060941`
- dry_run_passed: `true`
- contract_path: `.dev/swarm-runs/edge-case-hunt-20260619T060941/return-contract.yaml`
- workers_requested: 4
- workers_succeeded: 4
- workers_failed: 0
- merged_path: `.dev/swarm-runs/edge-case-hunt-20260619T060941/merged.md`
- recommended_next_command: `/sc:adversarial --compare <existing-review>,<the 4 .final.md files>`
  (rendered verbatim by the contract; for a stub run the inputs are placeholder
  text, so the meaningful hand-off only applies after a real run)

## Recommended next step

To get real edge-case findings, re-run the validated plan against your proxy
(requires `T2ProxyUrl` / `T2ProxyKey` / `T2Model01` from `~/.aienv`):

```
uv run superclaude swarm run --lens edge-case-hunt --target /tmp/swarm-wizard-probe/demo.py --output .dev/swarm-runs/edge-case-hunt-real-$(date +%Y%m%dT%H%M%S) --transport openai_compat --tui
```

(`--tui` gives a live dashboard on a real terminal; drop it for plain output.)
After a real run, the contract's `recommended_next_command` hands off to
`/sc:adversarial` to reconcile the 4 reviewers' findings.

---

## RESULT
- LENS: edge-case-hunt
- REVIEWERS_DEFAULT: 4 (lens default for edge-case-hunt; range [2,4])
- TRANSPORT: stub
- DRYRUN_CMD: uv run superclaude swarm run --lens edge-case-hunt --target /tmp/swarm-wizard-probe/demo.py --output .dev/swarm-runs/edge-case-hunt-20260619T060941 --transport stub
- DRYRUN_VERIFIED: yes — exit 0; stdout "dispatched job (mode=lens, workers=4, results=4)"; .swarm-state.json state=="terminal"; return-contract.yaml present with status: success, workers_succeeded 4/4
- NEXT_CMD: uv run superclaude swarm run --lens edge-case-hunt --target /tmp/swarm-wizard-probe/demo.py --output .dev/swarm-runs/edge-case-hunt-real-<ts> --transport openai_compat --tui
- NOTES: Goal "inputs that break my parser" maps cleanly to edge-case-hunt (the lens's literal purpose). Lens default reviewers=4 (not 3). Practice-run-only request → stopped at green dry-run, no real run launched (Return Contract status=cancelled). Ref vs live --help agree; confirmed the documented stale --transport help text (help says openai_compat default, lens-expansion default is stub). done.json correctly absent on inline run.
