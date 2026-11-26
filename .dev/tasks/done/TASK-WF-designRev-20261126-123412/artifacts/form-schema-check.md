# T4 form schema check

Method: the public GitHub issue-form JSON schema fetched from https://www.schemastore.org/github-issue-forms.json (after a redirect from json.schemastore.org) on 2026-11-26T12:48:53Z, validated with Python jsonschema (Draft 7) after yaml.safe_load.

- form: `.github/ISSUE_TEMPLATE/feature_request.yml`
- yaml.safe_load: ok (7 body elements)
- body ids in order: ['problem', 'proposal', 'alternatives', 'primitive', 'reuse_search', 'affected_callers']
- required flags: {'problem': True, 'proposal': True, 'alternatives': False, 'primitive': False, 'reuse_search': False, 'affected_callers': False}
- unique ids: True
- ids equal expected ['problem', 'proposal', 'alternatives', 'primitive', 'reuse_search', 'affected_callers']: True
- type: 'Feature'; labels: ['enhancement']; name: 'Feature request'
- JSON Schema errors: 0
- result exit code: 0

## git diff against base (deleted line count and the deleted line)
27	1	.github/ISSUE_TEMPLATE/feature_request.yml
-      description: Describe the change you want to see

## base form for comparison (type/labels/required of the original ids)
Feature ['enhancement'] {'problem': True, 'proposal': True, 'alternatives': False}
