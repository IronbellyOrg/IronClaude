"""Finalize an explicitly incomplete advisory review, never an invented merge."""
import datetime, hashlib, json, re
from pathlib import Path
O=Path(__file__).parent
R=Path('/config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP')
def load(p): return json.loads((O/p).read_text())
def save(p,v): (O/p).write_text(json.dumps(v,indent=2)+'\n')
V=load('artifacts/evidence-validation.yaml')
M=load('artifacts/coverage-matrix.yaml')
S=load('artifacts/input-snapshot.yaml')
D=load('artifacts/input-recheck.yaml')
now=datetime.datetime.now(datetime.timezone.utc)
iso=now.isoformat()
base='.dev/tasks/to-do/TASK-WF-spec-20261019-204314/'
hashes={x['path']:x['sha256'] for x in S['file_list']}
cards=sorted(str(p) for p in (O/'reviewer-cards').glob('reviewer-*-card.yaml'))
assert not D['input_drift_detected']
assert not D['quote_mismatches']
assert V['citations_dropped']==0, 'Apply validator drops before finalization'
C={
 'contract_version':'1.7.0','status':'partial','mode':'pre','tier_reached':2,
 'report_path':str(O/'REPORT.md'),'audit_log_path':str(O/'audit.log'),
 'confidence_calibrated':0.73,'confidence_scope':'initial T1 blind calibration only; no final merged confidence',
 'escalation_rule_matched':4,'onboarding_ran':False,
 'coverage_pct':None,'coverage_pct_union':M['coverage_pct_union'],'coverage_undefined':False,'coverage_degraded':'parsed-sparse',
 'unmapped_requirements':[],'unmapped_requirements_union':M['unmapped_requirements_union'],
 'best_practice_grade':None,'best_practice_grade_reason':'No completed calibrated/adversarial grade; structural design observations only',
 'implementation_coverage_pct':None,'missing_implementations':[],'hierarchy_slice_path':None,'hierarchy_coverage_pct':None,
 'tasklist_completion_pct':None,'deviation_count_by_class':dict(authorized=0,necessary=0,drift=0,regression=0),
 'deviation_register_path':None,'grounding_gaps_path':str(O/'grounding-gaps.yaml'),
 'third_party_api_grounding':[],'third_party_api_verified':False,'serena_summary_corroboration':'unavailable',
 'verification_ran':False,'verification_invocations':0,'verification_failures':0,'verification_regressions_detected':0,
 'verification_skip_reason':None,'verification_not_applicable_reason':'UC-1 PRE; user also forbids tests/builds',
 'input_sha256':{'tasklist':hashes[base+'TASK-WF-spec-20261019-204314.md'],'spec':hashes[base+'source.md']},
 'input_tree_sha256':S['input_tree_sha256'],'input_tree_file_count':S['file_count'],'input_tree_snapshot_path':str(O/'artifacts/input-snapshot.yaml'),
 'input_drift_detected':D['input_drift_detected'],'input_drift_diff':None,
 'citations_total':V['citations_total'],'citations_revalidated':V['citations_revalidated'],'citations_dropped':V['citations_dropped'],
 'citations_dropped_extrapolated':0,'citations_inferred':V['citations_inferred'],'citation_budget_policy':'full_reread','evidence_validator_ran':True,
 'citation_revalidation_at_promotion':False,'reviewer_cards':cards,'adversarial_artifacts_dir':None,'adversarial_convergence_score':None,
 'adversarial_unavailable':False,'adversarial_not_run':True,
 't2_model_class_diversity':'full' if len(cards)==3 else 'degraded','t2_vendor_diversity':'multi' if len(cards)==3 else 'single',
 't2_effective_diversity':'full' if len(cards)==3 else 'model-only','calibrator_diversity':'degraded',
 'remediation_offered':False,'remediation_accepted':None,'task_file_path':None,'remediation_task_path':None,'handoff_memory_key':None,
 'cannot_validate_without_user_input':False,'regression_present':False,'unauthorized_deviation_present':False,'blocked_by_low_confidence':False,
 'spec_is_wrong':False,'user_decision_required':False,'needs_human_decision':True,
 'needs_human_decision_note':'Protocol §10.6 mechanically requires true for nonempty grounding gaps; no immediate plan-edit/user decision requested',
 'per_task_verdicts':[],'interaction_effects_scanned':False,'interaction_effects_findings':0,
 'budget_forced_tier_downgrade':False,'budget_forced_stop':False,'budget_check_skipped':True,'forced_tier':None,
 'promotion_action':'not-applicable','promotion_adapter':None,'promotion_source':None,'promotion_destination':None,'promotion_log_path':None,
 'promotion_gate_passed':None,'promotion_skip_reason':None,'promotion_fail_reason':None,'promotion_override_used':None,'promotion_rollback_command':None,
 'promotion_checkpoint_path':None,'promotion_cross_fs':False,'promotion_pending':False,
 'contract_complete':False,'missing_mandatory_fields':['merge_method'],
 'missing_mandatory_fields_reason':'No adversarial merge or legitimate unavailable/failed-merge fallback occurred. Omitting merge_method rather than fabricating adversarial or single-reviewer-fallback.',
 'incomplete_stages':['worktree-correct Serena grounding and checkpoints','independent Tier-2 per-card blind calibration','full sc-adversarial debate/scoring/merge','Wave-0 audit opened retrospectively, not at run start'],
 'executor_class_source':'unknown','executor_class_resolved':False,'executor_exclusion_degraded':False,
 'serena_version':'unknown','serena_active_context':'unknown','serena_active_modes':[],'serena_config_snapshot_path':None,
 'onboarding_status':'unknown','onboarding_ran':False,'onboarding_skipped_reason':'--onboard not provided; wrong active project',
 'memory_persist_failed':True,'memory_persist_reason':'Suppressed: read-only artifacts-only authorization and wrong Serena root',
 'degraded_components':['serena:wrong-active-project','get_current_config','serena:activation-unavailable','serena:symbolic-chain-unavailable','serena:checkpoints-unavailable','serena:memory-unavailable','executor-class-unknown','calibrator-model-collision','coverage:parsed-sparse','coverage:extraction-not-exhaustive','t2:per-card-calibration-unfinished','adversarial:unfinished','audit:retrospective'],
 'plan_modified':False,'parent_must_not_modify_plan':True,'reviewer_briefs_materialized':3,
 'reviewer_isolation':'disabled','reviewer_grounding_root':str(R),'completed_at':iso
}
save('return-contract.yaml',C)
steps=[
 (0,'0.1','ok','run-header.yaml'),(0,'0.2','ok','artifacts/input-snapshot.yaml'),(0,'0.3','ok',None),
 (0,'0.4','ok','artifacts/input-snapshot.yaml'),(0,'0.5','ok','artifacts/environment.json'),(0,'0.5b','warn','artifacts/environment.json'),
 (0,'0.5c','warn','grounding-gaps.yaml'),(0,'0.5d','warn','run-header.yaml'),(0,'0.5e','skip',None),(0,'0.6','ok','artifacts/environment.json'),
 (0,'0.7','warn','grounding-gaps.yaml'),(0,'0.7b','skip',None),(0,'0.8','warn','run-header.yaml'),(0,'0.9','skip',None),
 (1,'1A','warn','grounding-gaps.yaml'),(1,'1A.checkpoint','skip','serena-checkpoints.log'),
 (1,'1B.0','warn','artifacts/coverage-matrix.yaml'),(1,'1B.1','ok','artifacts/coverage-matrix.yaml'),
 (1,'1B.2','ok','artifacts/coverage-matrix.yaml'),(1,'1B.2b','warn','artifacts/tier_decision.yaml'),(1,'1B.3','skip',None),
 (1,'1C','ok','t1-card.md'),(1,'1C.checkpoint','skip','serena-checkpoints.log'),(1,'1D','ok','artifacts/t1-calibration.yaml'),
 (2,'routing','ok','artifacts/tier_decision.yaml'),(3,'3A','warn','artifacts/tier_decision.yaml'),(3,'3B.0','ok','reviewer-briefs'),
 (3,'3B','ok','reviewer-cards'),(3,'3C','skip','return-contract.yaml'),(3,'3D','skip','return-contract.yaml'),
 (4,'merge','skip','return-contract.yaml'),(5,'5.0','skip','return-contract.yaml'),(5,'input-drift-check','ok','artifacts/input-recheck.yaml'),
 (5,'synthesis','warn','REPORT.md'),(5,'evidence-validator','ok','artifacts/evidence-validation.yaml'),(5,'zero-drop-flag','warn','artifacts/evidence-validation.yaml'),
 (5,'done-checkpoint','skip','serena-checkpoints.log'),(5,'memory-persist','skip','grounding-gaps.yaml'),(6,'remediation','skip',None),(7,'promotion','skip',None)]
with (O/'audit.log').open('w') as f:
 for wave,step,outcome,ref in steps:
  f.write(json.dumps({'wave':wave,'step':step,'timestamp':iso,'outcome':outcome,'evidence_ref':str(O/ref) if ref else None})+'\n')
save('run-header.yaml',{'skill':'sc-reflect-protocol','args':'--mode pre --spec .dev/tasks/to-do/TASK-WF-spec-20261019-204314/source.md --tasklist .dev/tasks/to-do/TASK-WF-spec-20261019-204314/TASK-WF-spec-20261019-204314.md','grounding_root':str(R),'started_at':'2026-10-19T20:47:36Z','completed_at':iso,'audit_emission':'retrospective; row timestamps denote record creation, not actual step execution time','serena_availability':{'backend':'none','execute_shell_command_available':False,'onboarding_available':False,'read_only':True},'serena_read_only_note':'Review policy: true; actual project config not probed because active project differs. This is not an observed Serena config value.','adversarial_skill_probe':'Installed source read; no no-op Skill invocation or F1/F2/F3 failure path claimed','estimated_token_usage':None,'exact_wave_durations':None})
(O/'serena-checkpoints.log').write_text('think_about_collected_information: skipped (tool unavailable; wrong active project)\nthink_about_task_adherence: skipped (tool unavailable)\nthink_about_whether_you_are_done: skipped (tool unavailable)\n')
wall=int((now-datetime.datetime(2026,10,19,20,47,36,tzinfo=datetime.timezone.utc)).total_seconds()*1000)
metrics={'metrics_schema_version':'1.0','run_id':'20261019204736-'+S['input_tree_sha256'][:8],'skill':'sc-reflect','skill_version':'1.7.0','mode':'pre','tier_reached':2,'status':'partial','wall_clock_ms':wall,'wave_durations_ms':None,'token_usage':None,'calibration':{'calibrator_diversity':'degraded','calibrated_confidence_initial':0.73,'calibrated_confidence_final':None,'calibration_delta':None},'ensemble':{'reviewer_count':len(cards),'executor_class_resolved':False},'evidence_validator':{'ran':True,'citations_total':V['citations_total'],'citations_revalidated':V['citations_revalidated'],'citations_dropped':V['citations_dropped'],'budget_policy':'full_reread'},'adversarial':{'convergence_score':None,'adversarial_unavailable':False,'ran':False,'fallback_path':None},'promotion':{'action':'not-applicable'},'degraded_components':C['degraded_components'],'input_drift_detected':False,'needs_human_decision':True,'metrics_complete':False,'unknown_measurements_policy':'null, never fabricated zero estimates'}
save('metrics.json',metrics)
with (R/'.dev/reflect/runs.jsonl').open('a') as f:
 f.write(json.dumps({'run_id':metrics['run_id'],'timestamp':iso,'skill_version':'1.7.0','mode':'pre','tier_reached':2,'status':'partial','wall_clock_ms':wall,'token_usage_total':None,'calibration_delta':None,'convergence_score':None,'evidence_validator_drop_rate':0.0,'deviation_counts_regression':0,'promotion_action':'not-applicable'})+'\n')
# No evidence claims are changed; add actual validator counters to the existing header only.
report=O/'REPORT.md'
text=report.read_text()
text=text.replace('citation_budget_policy: full_reread\n',f"citation_budget_policy: full_reread\ncitations_total: {V['citations_total']}\ncitations_revalidated: {V['citations_revalidated']}\ncitations_dropped: {V['citations_dropped']}\ncitations_inferred: {V['citations_inferred']}\nevidence_validator_ran: true\n",1)
report.write_text(text)
print(json.dumps({'report_path':C['report_path'],'return_contract_path':str(O/'return-contract.yaml'),'status':'partial','reviewer_cards':len(cards),'citations_total':V['citations_total'],'citations_dropped':V['citations_dropped'],'input_drift_detected':False,'contract_complete':False}))
