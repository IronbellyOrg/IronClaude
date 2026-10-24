Rip out the framework sync workflow and the Codecov upload in the IronbellyOrg/IronClaude fork. Delete
  .github/workflows/pull-sync-framework.yml, scripts/sync_from_framework.py and docs/.framework-sync-commit. Remove the 'Upload coverage to
  Codecov' step from .github/workflows/test.yml but keep pytest's own coverage measurement. In .github/workflows/README.md remove the
  pull-sync-framework entry (section 4), the Codecov list item, the Codecov text in the Coverage Reporting section, and the Codecov bullets
  in 'Coverage upload fails' (remove that whole section if nothing is left). Do not touch
  src/superclaude/templates/documents/readme_template.md, which is a generic example badge. Do not revert any content that earlier syncs
  brought in from upstream; that is decided separately. Do not close PR 283 or delete the sync/framework branch on origin; list both in the
  final report for my approval. Final check: no tracked file outside .dev/ still mentions pull-sync-framework, sync_from_framework,
  framework-sync-commit or codecov (except the template above). Work on a feature branch; any PR goes to IronbellyOrg/IronClaude only.
