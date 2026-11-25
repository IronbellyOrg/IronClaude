start=56f171c140f4a92de9d2342f644276d8438e8920 tree=5f8f27378ec16dbd849792d23d88ff791d59e8f3
## First reviewer response, verbatim

**Earlier blocking findings:** none were supplied (first review), so there are no status lines.

**AC marks**

- T5.AC1 met: `docs/swarm/monitoring-patterns.md:6-12` and `:40-52`.
  - Pattern 1 now covers foreground, resumed and detached-child completion, and requires a fresh per-job output directory.
  - It does not promise a marker on opt-out, early error or persistence failure, and it points to state, contract and log inspection for those cases.
  - The ordering (contract, then terminal state, then marker) matches `src/superclaude/cli/swarm/commands.py:2167-2186` and `:2608-2616`.
  - The detached claim matches the launcher passing `--output` at `commands.py:1303`.
  - No new polling feature was added.
- T5.AC2 met: `docs/swarm/observability-procedure.md:23-32`, `:51`, `:98-118`, `:133-161`, `:220-224`, `:271-273`.
  - Default inline absence is no longer called expected, and marker verdict reading is no longer limited to detached or resumed jobs.
  - Terminal completion is still distinguished from success (`:106`).
  - The killed marker's empty `contract_path` is kept distinct from a result-contract path (`:117-118`, `:140`), matching `commands.py:3554-3556`.
- T5.AC3 met: `docs/swarm/operator-runbook.md:218-226`.
  - The "resume emits more than a fresh run" claim is gone, replaced by "same result artifacts as a fresh completed reduction".
  - The original-runtime-override limitation is stated as in Tasks 2 and 4.
  - The effective-policy wording matches `commands.py:2610`, and no persistence code changed.
- T5.AC4 met: `docs/swarm/monitoring-patterns.md`, `observability-procedure.md`, `operator-runbook.md`, `README.md`, `command-reference.md`, `user-guide.md`.
  - My grep of the six documents for only-kill, default-inline-never and `test_quickstart_does_not_emit_done_sentinel` claims found nothing stale.
  - The only citation now is the positive `test_quickstart_emits_done_sentinel`, which exists at `tests/swarm/test_e2e_user_guide.py:117`.
  - The inline mentions that remain are `--detached` flag text and an inline-run example in `monitoring-patterns.md:61`.
  - Search hits and link checks are in `artifacts/monitoring-doc-check.txt:1-221`.
- T5.AC5 met: `artifacts/monitoring-doc-check.txt:222-229`.
  - It records the UV pytest command, `29 passed` and `EXIT: 0`.
  - Field names (`atomic_write`, `terminal_status`, `contract_path`), status values and policy conditions match `src/superclaude/cli/swarm/reduce.py:383-434`. I read the file's contents; I did not re-run the tests.

**Findings**

No blocking findings. This is one note, which does not block.

- Note: `docs/swarm/observability-procedure.md:223` says "any run also publishes done.json.terminal_status". That is slightly broader than the policy and completion conditions stated elsewhere in the same file (`:101-102`, `:108-110`). It is a wording issue only, and no check or recipe depends on it.

**Coverage**

I read the live source at `commands.py:2120-2210`, `:2560-2625` and `:3543-3569`, and `reduce.py:383-434`. I also read the three edited documents in full, and grepped the other swarm documents and `monitoring-doc-check.txt`. I did not read the retry folders or the troubleshoot package.

Parent: the note has no required finding line or four checklist answers, so this is paperwork-only, not a failed task. A fresh reviewer was respawned once with the same saved input, as qa.md requires.

## Fresh paperwork-respawn response, verbatim

**Earlier blocking findings:** none were supplied for this review.

**AC marks**

- **T5.AC1: met.**
  - `docs/swarm/monitoring-patterns.md:6-12` and `:40-52` scope polling to completed reductions with the policy enabled and a fresh output directory.
  - They say opt-out and early failure can leave no marker, and point to state, contract and log inspection for those cases.
  - No new polling feature was added. The Pattern 1 commands at `:56-78` are unchanged.
  - This matches the source: the foreground path emits the marker only when `result_contract is not None`, a state directory exists and the policy is on (`src/superclaude/cli/swarm/commands.py:2176-2186`). The resume path emits only when the policy is on (`commands.py:2610-2616`).
- **T5.AC2: met.**
  - `docs/swarm/observability-procedure.md:23-32` and `:98-118` drop the "default inline `swarm run` never emits it" claim and the detached-only restriction on reading the marker.
  - `:104-105` and `:138-140` keep the split between terminal completion and success. `:117-118`, `:140` and `:273` keep the killed marker's empty contract path separate from a result contract path.
  - Recipe 0, Recipe 2 and Recipe 4, and the use-case map at `:271-273`, are updated consistently.
  - The marker fields match `DoneSentinel` and `emit_done_sentinel` (`src/superclaude/cli/swarm/reduce.py:431-439`).
- **T5.AC3: met.**
  - `docs/swarm/operator-runbook.md:218-225` replaces "Resume emits more than a fresh run" with a statement that resume regenerates the same result artifacts as a fresh completed reduction.
  - The limit on original runtime overrides is stated the same way as in `docs/swarm/command-reference.md:282-284`.
  - It matches the code, which uses `rehydrated_spec.runtime...` (`commands.py:2610`). No persistence behavior was changed.
- **T5.AC4: met.**
  - A grep of `docs/swarm` finds no `test_quickstart_does_not_emit_done_sentinel`. The only citation is the positive `test_quickstart_emits_done_sentinel` at `docs/swarm/observability-procedure.md:28`, and that test exists at `tests/swarm/test_e2e_user_guide.py:117`.
  - No "only kill" or "default inline never" claims remain in the six completion documents.
  - `.dev/tasks/to-do/TASK-WF-createACheckedFi-20261123-195635/artifacts/monitoring-doc-check.txt:1-221` holds the hits and `LINK OK` lines for README, command-reference, user-guide, monitoring-patterns, observability-procedure and operator-runbook.
- **T5.AC5: met, with a form note (F1.1).**
  - `monitoring-doc-check.txt:224-229` shows 29 tests passed, exit 0.
  - `:222` records the captured marker fields, status and path matching the documentation.

**Findings**

F1.1 ac=T5.AC5 at=.dev/tasks/to-do/TASK-WF-createACheckedFi-20261123-195635/artifacts/monitoring-doc-check.txt:224 anchor="Run `uv run pytest tests/swarm/test_e2e_user_guide.py tests/swarm/test_tmux_fallback.py`" chk=n,n,n,n family=evidence-form fix=optionally record the literal `uv run pytest` invocation; no blocking effect: The recorded command is `uv run --no-project --python <tool-python> pytest ... -o addopts= -p no:cacheprovider` with `PYTHONPATH=src`, not the literal command in the AC. It still runs both files through UV, and the result is 29 passed, exit 0. This is a Note.

F1.2 ac=T5.AC4 at=.dev/tasks/to-do/TASK-WF-createACheckedFi-20261123-195635/artifacts/monitoring-doc-check.txt:3-221 anchor="inspect hits in context" chk=n,n,n,n family=evidence-form fix=optionally add a one-line verdict per document; no blocking effect: The artifact lists the hits and ends with `CHECK: PASS`, but it has no per-hit in-context verdict. I read the hits in the live docs and found no stale only-kill or default-inline-never claim, so this is a Note.

Not verified: I did not re-run the tests or the detached-child live path. I took Task 3's detached handoff as given and read only the Task 5 documentation and the foreground and resume source.

Parent: both findings have all four answers no, are optional evidence-form suggestions and derive note (first=A1, origin=new). They do not make an AC unmet. Each AC carries an actual source/log citation. Current machine log outcomes at :223 and :227 verify claims/links/captured fields and the two requested test modules. Verdict compliant. Final whole-list review will independently check Task 3 rather than relying on this Task 5 reviewer for detached acceptance.
