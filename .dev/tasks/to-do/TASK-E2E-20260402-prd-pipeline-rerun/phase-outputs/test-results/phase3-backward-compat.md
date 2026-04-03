[roadmap] Input type: spec (spec=.dev/test-fixtures/test-spec-user-auth.md, tdd=None, prd=None)
Step 1: extract
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/extraction.md
  Timeout: 300s
  Gate tier: STRICT
  Gate min_lines: 50
  Gate frontmatter: spec_source, generated, generator, functional_requirements, nonfunctional_requirements, total_requirements, complexity_score, complexity_class, domains_detected, risks_identified, dependencies_identified, success_criteria_count, extraction_mode
  Semantic checks: complexity_class_valid, extraction_mode_valid

Step 2 (parallel): generate-opus-architect
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/roadmap-opus-architect.md
  Timeout: 900s
  Model: opus
  Gate tier: STRICT
  Gate min_lines: 100
  Gate frontmatter: spec_source, complexity_score, primary_persona
  Semantic checks: frontmatter_values_non_empty, has_actionable_content

Step 3 (parallel): generate-haiku-architect
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/roadmap-haiku-architect.md
  Timeout: 900s
  Model: haiku
  Gate tier: STRICT
  Gate min_lines: 100
  Gate frontmatter: spec_source, complexity_score, primary_persona
  Semantic checks: frontmatter_values_non_empty, has_actionable_content

Step 4: diff
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/diff-analysis.md
  Timeout: 300s
  Gate tier: STANDARD
  Gate min_lines: 30
  Gate frontmatter: total_diff_points, shared_assumptions_count

Step 5: debate
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/debate-transcript.md
  Timeout: 600s
  Gate tier: STRICT
  Gate min_lines: 50
  Gate frontmatter: convergence_score, rounds_completed
  Semantic checks: convergence_score_valid

Step 6: score
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/base-selection.md
  Timeout: 300s
  Gate tier: STANDARD
  Gate min_lines: 20
  Gate frontmatter: base_variant, variant_scores

Step 7: merge
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/roadmap.md
  Timeout: 600s
  Gate tier: STRICT
  Gate min_lines: 150
  Gate frontmatter: spec_source, complexity_score, adversarial
  Semantic checks: no_heading_gaps, cross_refs_resolve, no_duplicate_headings

Step 8: anti-instinct
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/anti-instinct-audit.md
  Timeout: 30s
  Gate tier: STRICT
  Gate min_lines: 10
  Gate frontmatter: undischarged_obligations, uncovered_contracts, fingerprint_coverage
  Semantic checks: no_undischarged_obligations, integration_contracts_covered, fingerprint_coverage_check

Step 9: test-strategy
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/test-strategy.md
  Timeout: 300s
  Gate tier: STRICT
  Gate min_lines: 40
  Gate frontmatter: spec_source, generated, generator, complexity_class, validation_philosophy, validation_milestones, work_milestones, interleave_ratio, major_issue_policy
  Semantic checks: complexity_class_valid, interleave_ratio_consistent, milestone_counts_positive, validation_philosophy_correct, major_issue_policy_correct

Step 10: spec-fidelity
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/spec-fidelity.md
  Timeout: 600s
  Gate tier: STRICT
  Gate min_lines: 20
  Gate frontmatter: high_severity_count, medium_severity_count, low_severity_count, total_deviations, validation_complete, tasklist_ready
  Semantic checks: high_severity_count_zero, tasklist_ready_consistent

Step 11: wiring-verification
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/wiring-verification.md
  Timeout: 60s
  Gate tier: STRICT
  Gate min_lines: 10
  Gate frontmatter: gate, target_dir, files_analyzed, rollout_mode, analysis_complete, unwired_callable_count, orphan_module_count, unwired_registry_count, critical_count, major_count, info_count, total_findings, blocking_findings, whitelist_entries_applied, files_skipped, audit_artifacts_used
  Semantic checks: analysis_complete_true, recognized_rollout_mode, finding_counts_consistent, severity_summary_consistent, zero_blocking_findings_for_mode

Step 12: deviation-analysis
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/spec-deviations.md
  Timeout: 300s
  Gate tier: STRICT
  Gate min_lines: 20
  Gate frontmatter: schema_version, total_analyzed, slip_count, intentional_count, pre_approved_count, ambiguous_count, routing_fix_roadmap, routing_no_action, analysis_complete
  Semantic checks: no_ambiguous_deviations, validation_complete_true, routing_ids_valid, slip_count_matches_routing, pre_approved_not_in_fix_roadmap, total_analyzed_consistent, deviation_counts_reconciled

Step 13: remediate
  Output: /Users/cmerritt/GFxAI/IronClaude/.dev/test-fixtures/remediation-tasklist.md
  Timeout: 600s
  Gate tier: STRICT
  Gate min_lines: 10
  Gate frontmatter: type, source_report, source_report_hash, total_findings, actionable, skipped
  Semantic checks: frontmatter_values_non_empty, all_actionable_have_status

