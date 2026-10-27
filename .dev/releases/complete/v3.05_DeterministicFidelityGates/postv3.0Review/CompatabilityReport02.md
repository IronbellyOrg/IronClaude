Executive summary                                                                                                         
                                                                                                                            
  Your core discovery is correct: v3.05 is not a greenfield spec. Several modules and fields it treats as “new” were already
   added by v3.0 commit f4d9035, including:                                                                                 
                                                                                                                            
  - src/superclaude/cli/roadmap/convergence.py                    
  - src/superclaude/cli/roadmap/semantic_layer.py
  - src/superclaude/cli/roadmap/remediate_executor.py
                                                                                                                            
  And v3.0 also already amended:
                                                                                                                            
  - src/superclaude/cli/roadmap/models.py                                                                                   
  - src/superclaude/cli/roadmap/gates.py
  - src/superclaude/cli/roadmap/executor.py                                                                                 
  - src/superclaude/cli/roadmap/commands.py                                                                                 
  - src/superclaude/cli/roadmap/prompts.py                                                                                  
                                                                                                                            
  So the v3.05 spec needs a rewrite from “create these modules” to “extend/complete/integrate existing modules.”            
                                                                                                                            
  ---                                                                                                                       
  Highest-confidence findings                                     
                             
  1. “New module” claims already conflict with the repo
                                                                                                                            
  Verified from git diff of f4d9035:                                                                                        
                                                                                                                            
  - src/superclaude/cli/roadmap/convergence.py — ADDED                                                                      
  - src/superclaude/cli/roadmap/semantic_layer.py — ADDED         
  - src/superclaude/cli/roadmap/remediate_executor.py — ADDED                                                               
                                                                                                                            
  This is the biggest rewrite driver.                                                                                       
                                                                                                                            
  2. Several v3.05 model/config changes already exist                                                                       
                                                                  
  Verified in src/superclaude/cli/roadmap/models.py:                                                                        
                                                                  
  - VALID_FINDING_STATUSES already includes ACTIVE                                                                          
  - Finding.source_layer already exists                           
  - RoadmapConfig.convergence_enabled already exists                                                                        
  - RoadmapConfig.allow_regeneration already exists                                                                         
                                                                                                                            
  So FR text that says to add these should be rewritten to say they are already present.                                    
                                                                                                                            
  3. Gate authority mutual exclusion is already implemented                                                                 
                                                                  
  Verified in src/superclaude/cli/roadmap/executor.py:                                                                      
                                                                  
  spec-fidelity step already uses:                                                                                          
                                                                  
  - gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE                                                         
                                                                  
  That matches FR-7’s authority model:                                                                                      
  - convergence mode → registry/convergence engine authoritative  
  - legacy mode → SPEC_FIDELITY_GATE authoritative                                                                          
                                                                  
  4. Wiring step from v3.0 already exists and is positioned                                                                 
                                                                                                                            
  Verified in src/superclaude/cli/roadmap/executor.py and gates.py:                                                         
                                                                                                                            
  - wiring-verification step already exists                                                                                 
  - it is after spec-fidelity                                     
  - WIRING_GATE is already registered in ALL_GATES                                                                          
                                                                                                                            
  So v3.05 must treat wiring as existing context, not new surrounding infrastructure.                                       
                                                                                                                            
  ---                                                                                                                       
  Per-domain synthesis                                            
                                                                                                                            
  1) convergence.py                                               
                                                                                                                            
  Verified from file reads:                                                                                                 
                                                                                                                            
  src/superclaude/cli/roadmap/convergence.py already contains:                                                              
  - compute_stable_id()                                           
  - RunMetadata                                                                                                             
  - DeviationRegistry                                             
  - ConvergenceResult                                                                                                       
  - _check_regression()                                                                                                     
  - _create_validation_dirs()                                                                                               
  - _cleanup_validation_dirs()                                                                                              
  - _atexit_cleanup()                                                                                                       
                                                                                                                            
  What already aligns with FR-7 / FR-8                                                                                      
                                                                                                                            
  - Registry-backed run tracking exists                                                                                     
  - split structural vs semantic HIGH counting exists                                                                       
  - structural-only regression check exists                                                                                 
  - temp-dir isolation exists for parallel validation                                                                       
  - atexit/finally-style cleanup support exists                                                                             
                                                                                                                            
  Main conflict                                                                                                             
                                                                                                                            
  v3.05 frames convergence/regression infrastructure as if it still needs to be created. It mostly already exists.          
                                                                  
  Rewrite action                                                                                                            
                                                                  
  Change FR-7/FR-8 language from:                                                                                           
  - “create convergence engine / registry / temp-dir isolation”   
  to:                                                                                                                       
  - “audit and complete existing convergence.py implementation”   
  - “fill missing integration points and acceptance coverage”                                                               
                                                                                                                            
  Risk                                                                                                                      
                                                                                                                            
  HIGH — because the spec currently misstates repo reality.                                                                 
                                                                                                                            
  ---                                                                                                                       
  2) semantic_layer.py                                            
                                                                                                                            
  Verified from file and grep:                                    
                                                                                                                            
  src/superclaude/cli/roadmap/semantic_layer.py already contains:                                                           
  - RubricScores                                                                                                            
  - SemanticCheckRequest                                                                                                    
  - _truncate_to_budget()                                         
  - build_semantic_prompt()                                                                                                 
  - score_argument()                                                                                                        
  - judge_verdict()                                                                                                         
  - wire_debate_verdict()                                                                                                   
                                                                                                                            
  Important constants already exist:                                                                                        
  - MAX_PROMPT_BYTES = 30_720                                                                                               
  - budget split constants                                                                                                  
  - debate rubric weights                                                                                                   
  - verdict margin threshold                                                                                                
                                                                                                                            
  What already aligns with FR-4 / FR-4.1 / FR-4.2                                                                           
                                                                                                                            
  - prompt budget enforcement exists                                                                                        
  - chunked prompt builder exists                                                                                           
  - deterministic rubric scoring exists                                                                                     
  - deterministic judge exists                                                                                              
  - registry verdict wiring exists                                                                                          
                                                                                                                            
  Main gaps                                                                                                                 
                                                                                                                            
  The agent audit appears directionally right here: the module has most primitives, but the orchestration entrypoint implied
   by FR-4 is not obvious from the file surface.                  
                                                                                                                            
  Notably, grep showed references in docstrings to validate_semantic_high(), but no function definition was found.          
  
  Rewrite action                                                                                                            
                                                                  
  Change FR-4 from “build semantic layer module” to:                                                                        
  - “complete existing semantic layer by adding missing orchestration/integration entrypoints”
  - explicitly call out whether validate_semantic_high() must be added                                                      
  - clarify where prosecutor/defender execution lives                 
                                                                                                                            
  Risk                                                                                                                      
                                                                                                                            
  HIGH — because the module already exists and the spec should now describe completion work, not creation work.             
                                                                  
  ---                                                                                                                       
  3) models.py + gates.py                                         
                                                                                                                            
  Verified:                                                       
                                                                                                                            
  Already exists in models.py                                                                                               
                                                                                                                            
  - ACTIVE                                                                                                                  
  - source_layer                                                  
  - convergence_enabled                                                                                                     
  - allow_regeneration                                                                                                      
                                                                                                                            
  Already exists in gates.py                                                                                                
                                                                                                                            
  - SPEC_FIDELITY_GATE                                                                                                      
  - ALL_GATES                                                     
  - WIRING_GATE registration                                                                                                
                                                                                                                            
  Caution                                                                                                                   
                                                                                                                            
  One spawned audit reported gate_passed() as missing from roadmap/gates.py. That’s not necessarily a problem in itself     
  because the v3.0 roadmap doc references gate_passed() as part of broader gate infrastructure, not necessarily as a local
  function in this file. I would not treat that sub-finding as decisive without a broader search.                           
                                                                  
  Rewrite action                                                                                                            
  
  FR text should stop saying these fields are to be added. They’re already there.                                           
                                                                  
  Risk                                                                                                                      
                                                                  
  HIGH for stale spec wording, LOW for code change itself.                                                                  
                                                                  
  ---                                                                                                                       
  4) executor.py                                                  
                                                                                                                            
  Verified from file and diff:                                    
                                                                                                                            
  Current pipeline                                                                                                          
                                                                                                                            
  - extract                                                                                                                 
  - generate-* parallel                                           
  - diff                                                                                                                    
  - debate                                                                                                                  
  - score                                                                                                                   
  - merge                                                                                                                   
  - test-strategy                                                                                                           
  - spec-fidelity                                                                                                           
  - wiring-verification                                                                                                     
                                                                                                                            
  Important existing logic                                                                                                  
                                                                                                                            
  In src/superclaude/cli/roadmap/executor.py:                                                                               
  - _build_steps() already conditionally ungates spec-fidelity in convergence mode
  - roadmap_run_step() already special-cases wiring-verification                                                            
  - _get_all_step_ids() already includes wiring-verification      
                                                                                                                            
  Meaning for v3.05                                                                                                         
                                                                                                                            
  The insertion point is not “invent where convergence mode should go.” It is already conceptually attached to step 8.      
                                                                                                                            
  Rewrite action                                                                                                            
                                                                  
  FR-7 should describe convergence as altering existing step-8 authority and behavior, not adding a brand new pipeline      
  phase.                                                          
                                                                                                                            
  Risk                                                                                                                      
  
  HIGH if spec remains written as if the pipeline has not already been modified.                                            
                                                                  
  ---                                                                                                                       
  5) remediate_executor.py + commands.py                          
                                                                                                                            
  Verified from file reads:
                                                                                                                            
  commands.py                                                                                                               
                                                                                                                            
  src/superclaude/cli/roadmap/commands.py already has:                                                                      
  - --allow-regeneration as is_flag=True                          
  - it passes allow_regeneration into RoadmapConfig                                                                         
                                                                  
  So FR-9.1 is already implemented at CLI/config surface.                                                                   
                                                                                                                            
  remediate_executor.py                                                                                                     
                                                                                                                            
  Already contains:                                                                                                         
  - snapshot creation/restore/cleanup                             
  - allowlist enforcement                                                                                                   
  - parallel remediation execution                                
  - retry/rollback handling                                                                                                 
  - diff-size guard                                                                                                         
  - execute_remediation(...)                                                                                                
                                                                                                                            
  Major conflict                                                                                                            
                                                                                                                            
  FR-9 says diff-size threshold is 30%.                                                                                     
  Current code uses:                                                                                                        
                                                                                                                            
  - _DIFF_SIZE_THRESHOLD_PCT = 50                                                                                           
                                                                                                                            
  in src/superclaude/cli/roadmap/remediate_executor.py:45                                                                   
                                                                  
  That is a real spec/code mismatch.                                                                                        
                                                                  
  Additional nuance                                                                                                         
                                                                  
  The implementation is not MorphLLM-specific in the way the spec describes. It uses ClaudeProcess with remediation prompts 
  and then a post-hoc diff-size check. So FR-9’s “MorphLLM-compatible lazy edit snippets” appears to describe an intended
  design that is not what this code currently does.                                                                         
                                                                  
  Rewrite action                                                                                                            
  
  Split FR-9 into:                                                                                                          
  - already implemented: snapshots, rollback, allowlist, parallel execution, CLI flag
  - conflicting behavior: diff threshold 50% vs spec 30%                                                                    
  - missing/unclear behavior: MorphLLM-compatible patch object model
                                                                                                                            
  Risk                                                                                                                      
                                                                                                                            
  HIGH — this is one of the clearest behavior-level mismatches.                                                             
                                                                                                                            
  ---                                                                                                                       
  6) fidelity.py + spec_patch.py                                  
                                                                                                                            
  Verified:                                                       
                                                                                                                            
  fidelity.py                                                                                                               
                                                                                                                            
  src/superclaude/cli/roadmap/fidelity.py is a small data-model module:                                                     
  - Severity                                                      
  - FidelityDeviation                                                                                                       
                                                                  
  This is not a full “monolithic fidelity engine” by itself. It’s more of a schema module.                                  
                                                                                                                            
  spec_patch.py                                                                                                             
                                                                                                                            
  src/superclaude/cli/roadmap/spec_patch.py clearly implements a spec-change acceptance workflow:                           
  - DeviationRecord                                               
  - scan_accepted_deviation_records()                                                                                       
  - update_spec_hash()                                            
  - prompt_accept_spec_change()                                                                                             
  - _extract_frontmatter()                                                                                                  
                                                                                                                            
  This is not mentioned in v3.05, but it is clearly relevant to spec drift / accepted deviations.                           
                                                                                                                            
  Synthesis                                                                                                                 
                                                                                                                            
  - fidelity.py is probably legacy-supporting data model, not the main thing FR-9 replaces                                  
  - spec_patch.py is active overlap-adjacent functionality that the v3.05 spec ignores
  - the spec should account for accept-spec-change and accepted-deviation workflows, or explicitly scope them out           
                                                                                                                            
  Risk                                                                                                                      
                                                                                                                            
  MEDIUM — more omission/overlap than direct contradiction.                                                                 
                                                                  
  ---                                                                                                                       
  7) v3.0 roadmap doc vs v3.05 spec doc                           
                                                                                                                            
  From the document cross-reference and verified v3.0 roadmap read:
                                                                                                                            
  v3.0 roadmap is heavily centered on:                                                                                      
  - wiring gate infrastructure                                                                                              
  - GateCriteria, Step, GateMode                                                                                            
  - report emission and gate integration                          
  - roadmap executor step insertion                                                                                         
                                                                                                                            
  v3.05 spec builds on the same execution/gating substrate, but currently describes some extensions as if those extension   
  surfaces don’t yet exist.                                                                                                 
                                                                                                                            
  Shared-symbol relationship summary                                                                                        
                                                                  
  - GateCriteria — EXTEND                                                                                                   
  - GateMode — EXTEND                                             
  - Step — EXTEND, not replace                                                                                              
  - WIRING_GATE — existing environmental context                                                                            
  - SPEC_FIDELITY_GATE — existing and now conditionally excluded in convergence mode                                        
  - RoadmapConfig — EXTEND existing                                                                                         
  - Finding — EXTEND existing                                                                                               
  - convergence_enabled — already implemented, not speculative                                                              
                                                                                                                            
  Rewrite action                                                                                                            
                                                                                                                            
  The v3.05 doc should explicitly include a “pre-existing implementation baseline” section.                                 
                                                                  
  ---                                                                                                                       
  Final conflict matrix                                           
                                                                                                                            
  Spec says create, code already exists                           
                                                                                                                            
  Rewrite priority: HIGH                                                                                                    
  - src/superclaude/cli/roadmap/convergence.py                                                                              
  - src/superclaude/cli/roadmap/semantic_layer.py                                                                           
  - src/superclaude/cli/roadmap/remediate_executor.py             
                                                                                                                            
  Spec says add fields, code already has them                                                                               
                                                                                                                            
  Rewrite priority: HIGH                                                                                                    
  - Finding.source_layer                                                                                                    
  - VALID_FINDING_STATUSES += ACTIVE                                                                                        
  - RoadmapConfig.convergence_enabled                             
  - RoadmapConfig.allow_regeneration                                                                                        
                                                                                                                            
  Spec and code align                                                                                                       
                                                                                                                            
  Keep, but rewrite as “already implemented”                                                                                
  - step-8 gate authority mutual exclusion                                                                                  
  - wiring step placement after spec-fidelity                                                                               
  - --allow-regeneration CLI flag existence                       
  - prompt budget constants and semantic rubric primitives                                                                  
                                                                                                                            
  Spec and code materially conflict                                                                                         
                                                                                                                            
  Implementation/spec decision needed                                                                                       
  - diff-size threshold: spec 30% vs code 50%                                                                               
  - FR-9 MorphLLM lazy-patch model vs current ClaudeProcess-based remediation flow                                          
  - semantic layer orchestration entrypoint appears incomplete or underspecified  
  - spec omission of spec_patch.py accepted-deviation workflow                                                              
                                                                                                                            
  ---                                                                                                                       
  Recommended rewrite queue for v3.05                                                                                       
                                                                                                                            
  Priority 1                                                                                                                
                                                                                                                            
  Revise FR sections to stop claiming greenfield creation of existing modules:                                              
  - FR-4                                                                                                                    
  - FR-7                                                                                                                    
  - FR-8                                                          
  - FR-9                                                                                                                    
                                                                                                                            
  Priority 2                                                                                                                
                                                                                                                            
  Add an explicit “existing baseline from v3.0” section listing:                                                            
  - pre-existing modules                                                                                                    
  - pre-existing fields                                                                                                     
  - pre-existing pipeline wiring                                  
                                                                                                                            
  Priority 3                                                                                                                
                                                                                                                            
  Resolve real behavior mismatches:                                                                                         
  - choose 30% or 50% diff threshold                                                                                        
  - decide whether FR-9 truly requires MorphLLM patch objects or whether current executor model is acceptable               
  - define the missing semantic orchestration entrypoint clearly                                             
                                                                                                                            
  Priority 4                                                                                                                
                                                                                                                            
  Mention spec_patch.py explicitly, either:                                                                                 
  - as preserved legacy/support flow, or                                                                                    
  - as part of accepted-deviation handling that coexists with v3.05                                                         
                                                                   
  ---                                                                                                                       
  Bottom line                                                                                                               
                                                                                                                            
  The v3.05 spec currently reads like a greenfield design doc, but the repo is already in a post-v3.0 partially implemented 
  state. The right move is not to implement v3.05 as written. The right move is to rewrite the spec against current reality 
  first.                                                          
                                                                                                                            
  If you want, I can turn this into a clean spec rewrite checklist by FR section or produce a single markdown compatibility 
  audit artifact in the repo.