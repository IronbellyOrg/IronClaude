# Labelling record

**This is the record completed by the labeller before any arm ran. It holds no prompt text and no table or Jev answer.**

- Labeller: Claude (the IronFlow session), a session and not a person, because the owner changed the labeller from Clay to this session. Clay's words, as relayed by the IronFlow session on 27 Nov 2026: "why dont you do it?". The earlier decision (26 Nov 2026) named Clay; the plan asked for a named human; the owner's change overrides it and is recorded in the story's Decided block and in the pull request.
- Independence, stated by the labeller: it did not write the keyword table or the Jev questions and has not seen the answers of either side. The labeller is an AI session, which is a limit of this measurement and is carried into the report.
- Date labelled (UTC): 2026-11-27
- The labelling instructions the labeller was given (the sheet `labelling-sheet.md`, section "What to do"):

  1. Read the six definitions below once (this counts as the reading step; write `read` on the line after them).
  2. For each prompt, replace the blank after `Label:` with exactly one of: `bug`, `build`, `performance`, `deployment`, `security`, `test`, `ambiguous`, `none-fit`.
  3. After `Basis:` write a few words of your own: why that label. For `ambiguous` and `none-fit` the basis is required and must be your own reasoning, not a rule about keywords.
  4. Tell the E2 lead when done. Do not edit the prompt text.

## Basis for each label

One line per corpus prompt, by id: the label and the basis for it, in the labeller's own words (the same text is in `corpus.jsonl`).

- `p01`: `deployment` because publishing to the sandbox and production environments fails with a 400; the project itself is fine.
- `p02`: `bug` because a link the program makes to the new session cannot be opened, while the session itself works: the program's own link is wrong.
- `p03`: `deployment` because the upgrade fails while installing its tooling into a clean destination (npm dependency conflict at install time).
- `p04`: `bug` because a regression in v0.39 skips tools in the home directory and prints a wrong error message: the program's own logic is wrong.
- `p05`: `build` because every build fails while fetching a dependency archive whose checksum does not match.
- `p06`: `build` because compiling the library for Windows on ARM stops with a compiler error.
- `p07`: `build` because builds from scratch break because a dependency's download host is down.
- `p08`: `build` because a deprecated setting becomes a build error in Kotlin 2.4.0, so the build cannot be upgraded until it is removed.
- `p09`: `performance` because the call works but reads every entry of the group twice: wasted work, not a wrong result.
- `p10`: `performance` because asks to avoid a temporary object on a hot path; the result is already correct.
- `p11`: `performance` because asks to avoid an unnecessary copy of a data frame; the behaviour is already correct.
- `p12`: `performance` because a no-op install meets or misses a CPU-time bar; it works, the cost is the problem.
- `p13`: `deployment` because bootstrapping the management environment fails on a transient permission error reading Terraform state; a retry on the same code succeeds.
- `p14`: `security` because the container runs as root, which widens what an attacker could do if the service were compromised.
- `p15`: `ambiguous` because the release package leaves out required files (a build output problem), which only shows up as a failure when deployed to Azure; build and deployment fit equally.
- `p16`: `security` because a crafted link can make the editor run code: remote code execution.
- `p17`: `security` because an antivirus flags the program's behaviour as malicious; the user is reporting a possible security threat.
- `p18`: `security` because use of mark_safe on form input may allow cross-site scripting.
- `p19`: `security` because a privileged owner-role service account stays enabled after the lockdown step that should disable it.
- `p20`: `test` because a named test fails on main in the race-test job.
- `p21`: `test` because a named test is flaky on Windows because of an extra stderr notice.
- `p22`: `test` because screenshot fixtures produce nondeterministic output and show as changed on unrelated pull requests.
- `p23`: `test` because a named test fails often on one platform's test job.
- `p24`: `performance` because proposes a faster sort algorithm (3x to 4x); the current one works.
- `p25`: `none-fit` because a question about licence wording in third-party notices; no failure of the program.
- `p26`: `none-fit` because a how-to question about authenticating local clients; nothing is broken.
- `p27`: `ambiguous` because a question asking when an image will be rebuilt for a compromised certificate authority: it is about a security fix, but it is a scheduling question rather than a weakness in the program.
- `p28`: `ambiguous` because the integration test suite takes an hour and should be split: it is about the tests, but nothing fails; it is a time cost, so test and performance fit about equally.
- `p29`: `test` because the Python 3.15 test matrix fails because the bundled linter predates 3.15 fixes.
- `p30`: `bug` because converting a model gives outputs that do not match the reference (difference NaN): a wrong result.

## Rules for the basis

- The basis for an `ambiguous` or `none-fit` label was written before any arm ran.
- That basis is not taken from the table's own two-row rule (the cues of two rows, or no cue), because that would make the table right by construction.
- The labeller did not see the table answers or any Jev answer.
