# Codecov step note (Task 7)

Status: UNVERIFIED. The edited step in .github/workflows/test.yml (`files: ./coverage.xml`, `token: ${{ secrets.CODECOV_TOKEN }}`, `flags`, `name`, `fail_ci_if_error: false`, still `codecov/codecov-action@v4`) has been checked against the v4 documentation (./artifacts/t2-codecov-v4.md) and parsed with PyYAML (./artifacts/t7-checks.log), but the upload itself is unverified until a run on GitHub.

User prerequisite: the `CODECOV_TOKEN` repository secret must exist in IronbellyOrg/IronClaude (Settings, Secrets and variables, Actions). This plan cannot create it. Per the v4 README, tokenless uploads are unsupported except for pull requests from forks, so without the secret the upload step reports an error. Because `fail_ci_if_error` stays `false`, that error does not fail the test job.

No coverage threshold was added.
