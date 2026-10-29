# Option C: byte proxy as the gate, session measurement as recorded evidence

Method: run Option A as the pass/fail gate (delta <= 6000 bytes, explore hidden and blocked). Then, when a logged-in `claude` is available, also run Option B's two headless runs and record the token delta in the same evidence file. If B runs and its delta exceeds 2000 tokens while A passed, B wins (value becomes `status` only) and the executor logs it; if B cannot run, A's result stands and the evidence says "session measurement: not run".

Pros:
- Never blocks the unattended executor (A always runs).
- Uses the real measurement whenever it is available, so the heuristic is cross-checked.
- One harness proves explore hidden and blocked.

Cons:
- Two methods to script and explain; slightly more spec text.
- B's UNVERIFIED flags/fields still apply when it runs.
- A disagreement rule is needed (defined above: the real measurement wins).
