# Corpus selection criteria

**This is the selection record for the 30 candidate prompts. It was completed by the selecting session before any arm ran; the labels are in `labelling-record.md`.** It holds no prompt text, no label and no answer.

Filled in on 2026-11-26 by the build agent (an AI session collected candidates and ran the privacy screen; the labels are written by the labeller named in `labelling-record.md`). Prompts are public only.

## Public sources

All 30 prompts are the opening text of public GitHub issues, read on 2026-11-26 with the GitHub search of the `gh` command line (public data, no private repository, no personal data requested). Chosen because maintainers of large public projects describe real problems in their own words, and their issue labels give a spread of problem kinds without using the table's cue words. Repositories (the exact issue links are in `corpus.jsonl`):

- `github.com/microsoft/AL-Go`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/microsoft/vscode`: 3 issues (issue links are in `corpus.jsonl`)
- `github.com/microsoft/power-platform-skills`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/microsoft/apm`: 2 issues (issue links are in `corpus.jsonl`)
- `github.com/google/xls`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/microsoft/STL`: 2 issues (issue links are in `corpus.jsonl`)
- `github.com/google/heir`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/google/ksp`: 2 issues (issue links are in `corpus.jsonl`)
- `github.com/pytorch/tensordict`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/python/cpython`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/scikit-learn/scikit-learn`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/microsoft/AzureTRE`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/google/timesketch`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/microsoft/chat-copilot`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/nodejs/node`: 2 issues (issue links are in `corpus.jsonl`)
- `github.com/python/pythondotorg`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/google/stellar-engine`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/docker/docker-agent`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/microsoft/aspire`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/microsoft/TypeScript`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/google/xmc`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/microsoft/Windows-Containers`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/microsoft/vscode-pylint`: 1 issue (issue links are in `corpus.jsonl`)
- `github.com/huggingface/transformers`: 1 issue (issue links are in `corpus.jsonl`)

## How they were chosen

1. For each of seven maintainer labels (`bug`, `build`, `performance`, `deployment`, `security`, `flaky-test`, `question`) the closed issues of ten large public organisations were searched, never by the words of the keyword table.
2. Kept only issues whose cleaned text is at least 100 characters, readable on its own, in English, and passes the privacy screen. Links, addresses, user names, template tags such as `[Bug]` and boilerplate headings were removed; the text was cut at a sentence end near 300 characters.
3. At most the first reasonable issue per repository per label was taken, so no single project dominates.
4. The maintainers' labels are only a sampling stratum. They are not the labels of this experiment: the labeller (see `labelling-record.md`) labels every prompt without seeing them (the labelling sheet does not show them), and `ambiguous` and `none-fit` prompts were included on purpose (the `ambiguous` ones were picked for fitting two kinds of problem; the `none-fit` ones for being questions or requests).

## Counts per label

About 30 prompts in total. The target is what was sampled per stratum; the final count is what the human labels give once they are written.

| Label | Target | Final count |
|---|---|---|
| bug | 4 | 3 |
| build | 4 | 4 |
| performance | 4 | 5 |
| deployment | 3 | 3 |
| security | 4 | 5 |
| test | 4 | 5 |
| ambiguous | 3 | 3 |
| none-fit | 4 | 2 |

## Shortfall

At selection every stratum reached its target. After labelling two labels have fewer prompts than their target: bug (3 against a target of 4) and none-fit (2 against a target of 4). They are reported here and not padded with a prompt that does not belong; all eight labels are present, which `load_corpus` requires. Three labels have more than their target (performance 5, security 5, test 5) because the labeller placed a prompt there that was sampled under another stratum.

## Prompts the privacy screen refuses

None. All 30 prompts passed the screen (`jevlib.manifest.privacy_violation`, data class `public`) before they were kept; `gate.py freeze-corpus` runs it again. A prompt that it would refuse is replaced by another public prompt and never edited to get past the screen.
