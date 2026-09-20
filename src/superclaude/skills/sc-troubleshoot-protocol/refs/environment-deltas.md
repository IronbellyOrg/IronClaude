# Environment deltas (optional ref)

Loaded by Wave 1 step 1b only when the execution-locus card derives `SAME-ENV ≠ yes`. Absent ⇒ audit line `optional_ref_absent: refs/environment-deltas.md`, no Grounding Gap. This is a prompt list, never a decision input: each delta you cannot prove identical between PRINT-SITE and RUN-SITE becomes a candidate `## Discriminator rows` entry (Wave 1.6 S1.6.4) and a candidate `runs-in=` qualifier on Wave 1.7 cards. Concrete, incident-derived probes live only in `refs/probe-packs/<kind>.md`.

Spec names (aliases allowed in parentheses): `host`, `process`, `user` (identity), `filesystem-view`, `network-view`, `clock`, `permissions`, `installed-versions`, `working-dir`, `env-vars` (config-source).

If the Wave 1 step 1b execution gate forbids a row, write `unknown — could-not-run: <gate reason>` and do not issue a command. Blank is illegal.

| Delta | How to check (one read-only property at RUN-SITE; record exit status or one `key=value` line) |
| --- | --- |
| host | machine identity at RUN-SITE vs PRINT-SITE; equal? |
| process | process identity of the producer line vs the assumed process |
| user | effective user identity at RUN-SITE vs the arm where it passes |
| filesystem-view | type/size/mount of the node the producer reads at RUN-SITE vs the same node on a passing arm |
| network-view | resolve and reach the producer endpoint from RUN-SITE; result code only, no payload |
| clock | monotonic and wall clocks once via the producer's idiom, then once by bulk read; same value and format? |
| permissions | permission bits of the producer path at RUN-SITE vs the passing arm |
| installed-versions | version of the interpreter / shell / binary that executes the producer line at RUN-SITE |
| working-dir | working directory of the producer process at RUN-SITE vs the passing arm |
| env-vars | config files and environment variables the producer line reads and their effective values at RUN-SITE, not at PRINT-SITE |

Rows are unordered; check first the ones whose kind (per `refs/primitive-differential.md`) matches a `surviving=yes` producer. Any row you cannot run is `unknown — could-not-run: <reason>`, never blank.
