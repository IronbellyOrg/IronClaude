# Corpus selection criteria (a form to fill in)

**This is a form to be completed by a person before any arm runs. It is not evidence until it is filled in, and it holds no prompt, label or
answer.**

Fill it in before the corpus is frozen with `gate.py freeze-corpus`. Prompts are public only.

## Public sources

List every public source before any prompt is taken from it (a name and a URL, why it was chosen, the date it was read):

- `<fill in>`

## Counts per label

About 30 prompts in total. Write the target and the final count for each label:

| Label | Target | Final count |
|---|---|---|
| bug | `<fill in>` | `<fill in>` |
| build | `<fill in>` | `<fill in>` |
| performance | `<fill in>` | `<fill in>` |
| deployment | `<fill in>` | `<fill in>` |
| security | `<fill in>` | `<fill in>` |
| test | `<fill in>` | `<fill in>` |
| ambiguous | `<fill in>` | `<fill in>` |
| none-fit | `<fill in>` | `<fill in>` |

## Shortfall

A label with fewer prompts than its target is reported here, with the reason. It is never padded with a prompt that does not belong:
`<fill in>`

## Prompts the privacy screen refuses

A prompt that the privacy screen (`jevlib.manifest.privacy_violation`, run by `gate.py freeze-corpus`) would refuse is replaced by another
public prompt. It is never edited to get past the screen. List each replacement by id and reason, never by the refused text:
`<fill in>`
