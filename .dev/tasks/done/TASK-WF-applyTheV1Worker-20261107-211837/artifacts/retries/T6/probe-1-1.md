d092fde2ee5f864f21bb35318b3f177ce6820954
family: ladder-caps
defect form: a rung row of the response ladder whose Cap cell does not match design section 8.1 (merged-requirements.md:434-439); the L1 row says "None" where the design caps costly probes at 2 per triggered worker per sweep.
command: grep -n -F -e "| L" src/superclaude/core/WORKER-CONTRACT.md
before (ladder rows; state-table rows 118-129 also match the pattern and carry no Cap cell):
150:| L0 observe | Watch only | Always | None |
151:| L1 probe | Read-only: `worker-show`, `worker-read --source transcript`, a screen read, the contract `stat` | A trigger fired | None |
152:| L2 nudge | Typed with `--wait-submit`; the S6 variant is an interrupt plus a handoff request | L1 confirms S3, S9 or S6 at an identified prompt | 1 per incident, 2 per lineage; a nudge with no turn start still counts |
153:| L3 ask | Typed: "Reply with `status`: current step, what you are waiting for" | L2 failed once and the state is still ambiguous | 1 per incident |
154:| L4 restart with resume note | Reconcile, stop the worker, settle it, set the old Task `failed --result cancelled`, create a new Task | Only with an Orca stall proof, or a person-directed cancellation with confirmed quiescence (WC-6), and only within the restart budget | 1 per rolling 60 minutes, 2 per lineage; WC-6's three-failed-starts rule also applies, whichever is stricter |
155:| L5 report to the person | Report the state, its evidence and what was tried | Any person-only state, or any cap reached | S4 is re-reported every 15 minutes |
coupled sites:
- src/superclaude/core/WORKER-CONTRACT.md:110 sweep paragraph ("Costly probes (transcript tail, screen read) run only for workers a trigger fired for in this sweep."): defines the term the new cap uses; unchanged.
- src/superclaude/core/WORKER-CONTRACT.md:150, :152-155 L0 and L2-L5 caps: match design 8.1 (reviewer confirmed); unchanged.
- tests/skills/test_worker_contract.py:226 pin `liveness-ladder-and-restart`: gains the new cap phrase.
after:
151:| L1 probe | Read-only: `worker-show`, `worker-read --source transcript`, a screen read, the contract `stat` | A trigger fired | Every sweep; at most 2 costly probes per triggered worker per sweep |
