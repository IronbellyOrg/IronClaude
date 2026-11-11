**F-07. Two ready-today commands can stall with no `worker_done`.**
§3.1 (line 81) says the ready commands "run as workers now if the brief uses the stated flags". Two rows depend on prompts that the stated flags do not stop:
- tdd (line 90): the nested `/task` "ask the user" lines are unflagged until P2 (the row says so). `/task` asks when several task files match (INV-B:219, citing sk/task/SKILL.md:49). The brief's precise prompt and `--output` do not prevent this.
- troubleshoot (line 91): the `--depth deep` short-input STOP that asks the user is unflagged until P2 (INV-B:239, citing sk/sc-troubleshoot-protocol/SKILL.md:57). A brief that uses `--depth deep` with a short input stalls.
An implementer who follows §3.1 dispatches these and gets a silent stall, which WC-2 says must not happen and which the coordinator sees only through `agentWait` (§7.2 step 2).
Fix: list the triggering inputs in the "Brief must pass" column (for tdd, a specific component with a known task file; for troubleshoot, no `--depth deep`), or move both rows out of ready-today until P2.
