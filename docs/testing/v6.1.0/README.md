# IronClaude 6.1.0 post-release record

This folder is the output of `/sc:post-release v6.1.0`: the record of bringing the documentation and the install path in line with the tagged 6.1.0 release, and of running the install for real.

Scope of this run (owner decision 6.1.0-5, the same as 6.0.0): workstreams A (user documentation), B (technical documentation) and C (install and deploy, proven by a real run). Workstreams D and E (human-run test guides) were skipped, so this folder has no `user/` or `sysop/` guides. The 5.0.0 guides in `docs/testing/v5.0.0/` and the 6.0.0 record in `docs/testing/v6.0.0/` are unchanged.

| File | What it is |
|---|---|
| `post-release-report.md` | What was scanned, updated and created; the install run; the regression gate; the honest gap list |
| `post-release-manifest.json` | Machine-readable record the next run diffs against (additive mode; evolved from the 6.0.0 manifest) |
| `audit.log` | The `SC:POST-RELEASE:RUN` and `RESULT` headers of this run |
| `c-e2e-run.sh` | The end-to-end install script: new user, upgrade from a genuine 6.0.0, `./update.sh` from a clone, all in throwaway homes |
| `c-e2e-transcript.txt` | Output of the full run of that script (paths normalised, no secrets) |

To repeat the install run, from the repository root with the `v6.1.0` and `v6.0.0` tags present and a virtualenv at `.venv`:

```bash
bash docs/testing/v6.1.0/c-e2e-run.sh > /tmp/c-e2e-transcript.txt 2>&1
```

To check that the script itself turns a failing step into a red result (it touches nothing and needs no network):

```bash
bash docs/testing/v6.1.0/c-e2e-run.sh --selftest-red; echo "exit=$?"               # RESULT: RED, exit 1
bash docs/testing/v6.1.0/c-e2e-run.sh --selftest-expected-nonzero; echo "exit=$?"  # RESULT: GREEN, exit 0
bash docs/testing/v6.1.0/c-e2e-run.sh --selftest-realstate; echo "exit=$?"         # fake HOME: every one-byte change must change the real-home fingerprint; GREEN, exit 0
```

The script never touches the real `~/.claude`, `~/.local`, `~/.codegraph` or pipx, and it deletes nothing: it prints the throwaway root (`ROOT=/tmp/ic6-e2e.<random>`) for you to remove by hand.
