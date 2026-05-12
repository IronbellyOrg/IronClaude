/sc:cli-portify is helpful but not sufficient by itself. You need a    
  design decision first, then cli-portify can implement the chosen shape.              
                                                                                       
  Current reality                        
                                                                                       
  Today there are two different validation systems:                                 
                                                                                       
  1. Python CLI runtime                                                                
  superclaude roadmap validate               
    - implemented in src/superclaude/cli/roadmap/commands.py:241                       
    - executed by src/superclaude/cli/roadmap/validate_executor.py:369               
    - auto-invoked from src/superclaude/cli/roadmap/executor.py:1979                   
    - narrow inputs: roadmap.md, test-strategy.md, extraction.md                     
  2. Slash command / skill spec                                                        
  /sc:validate-roadmap + sc-validate-roadmap-protocol                                  
    - richer, multi-phase, spec+roadmap fidelity validator                             
    - designed as the desired future system                                            
    - currently mostly docs/spec, not runtime                                          
                                                                                       
  That split is the core problem.                                                      
                                                                                       
  ---                                                                                  
  Best architecture                                                                    
                                                                                       
  Recommended model                                                                    
                                                                                       
  Make the CLI runner the source of execution truth, and make the slash command a thin 
  adapter to that runner.                                                              
                                                
  Even though you previously preferred “custom command invokes CLI runner,” the        
  maintainable version of that idea is:                                                
                                                                                       
  - Behavioral/spec ownership: sc-validate-roadmap-protocol                            
  - Execution ownership: superclaude roadmap validate-roadmap runner                   
  - Entry points:                               
    - /sc:validate-roadmap → parses UX args, calls the runner                          
    - superclaude roadmap run → calls the same runner internally                       
  - No duplicated validation logic in the skill body or roadmap pipeline
                                                                                       
  Why this is best                                                                     
                                                                                       
  Because you want:                                                                    
  - changes to /sc:validate-roadmap to propagate into pipeline behavior                
  - no duplicate Python reimplementation of skill logic                                
  - maintainability in CLI pipeline land                                               
                                                                                       
  The only sustainable way is:                                                       
  1. define a stable runner contract                                                   
  2. have both the slash command and roadmap pipeline call that contract             
  3. keep the skill as the spec and UX surface, not the executor                       
                                                                                       
  Ownership boundaries                                                                 
                                                                                       
  Skill / command own:                                                                 
                                                                                       
  - user-facing contract                                                               
  - semantics                                                                          
  - phase definitions                                                                  
  - artifact schema                                                                    
  - flags and behaviors                                                                
  - quality rules / boundaries                                                       
                                                                                       
  CLI runner owns:                                                                     
                                                                                       
  - actual execution                                                                   
  - orchestration                                                                      
  - filesystem IO                                                                      
  - subprocess / MCP / agent wiring                                                    
  - reuse from roadmap run                                                             
                                                                                     
  roadmap run owns:                                                                    
                                                                                       
  - when validation is invoked                                                         
  - how its outputs are passed to the runner                                           
  - migration from old spec-fidelity phase                                             
                                                                                       
  ---                                                                                  
  What roadmap run should do                                                         
                                                                                       
  Target state                                                                         
                                                                                       
  Replace the current:                                                                 
  - step-8 spec fidelity / convergence system                                          
  - plus current post-run execute_validate(...)                                      
                                                                                       
  with:                                                                                
                                                                                       
  New flow                                                                             
                                                                                     
  roadmap run                                                                          
  1. generate roadmap artifacts                                                        
  2. call validate-roadmap runner                                                      
  3. runner produces validation bundle                                                 
  4. roadmap pipeline consumes verdict / report path / blocking status                 
                                                                                     
  So instead of:                                                                       
  - old spec fidelity inside roadmap executor                                        
  - plus old validate subsystem after run                                              
                                                                                       
  you get:                                                                             
  - one validation authority                                                           
  - backed by validate-roadmap                                                         
                                                                                       
  Integration point                                                                    
                                                                                       
  The most obvious hook is where auto-validation currently happens:                    
  - src/superclaude/cli/roadmap/executor.py:1979                                       
                                                                                       
  But if your intent is to replace spec-fidelity phase, then the bigger change is:     
  - src/superclaude/cli/roadmap/executor.py:539 (_run_convergence_spec_fidelity)       
  - and wherever step 8 is wired into roadmap generation                               
                                                                                       
  That means this is not just “swap auto-invoke validate.”                           
  It is a pipeline architecture change.                                                
                                                                                       
  ---                                                                                  
  Best migration strategy                                                              
                                                                                       
  Phase 1 — Introduce shared runner                                                    
                                                                                       
  Create a new Python runtime surface, something like:                                 
                                                                                       
  - superclaude roadmap validate-roadmap ...                                         
  or                                                                                   
  - superclaude roadmap validate2 ...                                                  
                                                                                       
  This runner should accept:                                                           
  - roadmap path                                                                     
  - spec paths                                                                         
  - output dir                                                                         
  - depth                                                                              
  - exclusions                                                                         
  - max agents                                                                         
  - skip adversarial                                                                 
  - skip remediation                                                                   
  - prior taxonomy                                                                     
  - optional MCP toggles / availability handling                                       
                                                                                       
  This runner should implement the validate-roadmap protocol contract, not the old     
  3-file validate contract.                                                            
                                                                                       
  Phase 2 — Make slash command call runner                                             
                                                                                       
  Change /sc:validate-roadmap so it becomes:                                           
  - command/skill for UX + contract                                                    
  - actual execution delegated to runner                                               
                                                                                     
  That preserves propagation:                                                          
  - command changes shape the runner contract                                        
  - runner is the executable implementation                                            
  - slash command is not a dead-end docs-only layer                                  
                                                                                       
  Phase 3 — Let roadmap run call same runner                                           
                                                                                       
  Replace:                                                                             
  - old post-pipeline execute_validate(...)                                            
  with:                                                                                
  - new validate-roadmap runner invocation                                             
                                                                                       
  Initially this can be post-run only.                                                 
                                                                                     
  Phase 4 — Replace spec-fidelity phase         
                                             
  Once stable, replace the current step-8 fidelity path:                               
  - _run_convergence_spec_fidelity(...)      
  - current fidelity_checker.py                                                        
  - convergence/remediation coupling as needed                                       
                                                                                       
  At that point, validate-roadmap becomes the real fidelity authority.               
                                                                                       
  Phase 5 — Delete old path                                                          
                                                                                       
  After parity:                                                                        
  - retire old roadmap validate narrow implementation                                  
  - or keep it as legacy alias to the new runner                                       
                                                                                       
  ---                                                                                  
  Work involved                                                                      
                                                                                       
  Workstream 1 — Define the runner contract                                          
                                                                                       
  You need a new config/model layer equivalent to ValidateConfig, but for              
  validate-roadmap.                                                                    
                                                                                       
  Current ValidateConfig is too narrow:                                                
  - src/superclaude/cli/roadmap/models.py:116                                          
                                                                                       
  Needed:                                                                              
  - roadmap path                                                                       
  - spec paths                               
  - output dir                                                                         
  - depth                                                                            
  - exclusions                                                                         
  - prior taxonomy                                                                     
  - agent config                                                                       
  - skip flags                                                                         
  - MCP feature toggles / fail-open behavior                                           
                                                                                       
  This is foundational.                                                                
                                                                                       
  Workstream 2 — Port protocol into executable runner                                  
                                                                                       
  Translate the skill protocol into runtime code:                                      
  - Phase 0 ingestion / requirement universe                                           
  - Phase 1 decomposition                                                              
  - Phase 2 agent dispatch                                                             
  - Phase 3 consolidation                                                              
  - Phase 4 adversarial pass                                                         
  - Phase 5 remediation plan                                                           
  - Phase 6 summary                                                                  
                                                                                       
  This is the biggest piece.                    
                                                                                       
  Important: don’t port markdown prose literally.                                      
  Port the contract:                                                                   
  - inputs                                                                             
  - outputs                                                                            
  - artifacts                                                                          
  - rules                                                                              
  - sequencing                                                                         
                                                                                       
  Workstream 3 — Artifact model redesign                                               
                                                                                       
  Current runtime validate expects:                                                    
  - roadmap.md                                                                         
  - test-strategy.md                                                                   
  - extraction.md                                                                      
                                                                                       
  Validate-roadmap wants a richer bundle:                                              
  - 00-requirement-universe.md                                                         
  - 00-roadmap-structure.md                                                          
  - 00-domain-taxonomy.md                                                              
  - 00-decomposition-plan.md                                                           
  - 01-agent-*.md                                                                      
  - 02-unified-coverage-matrix.md                                                      
  - 02-consolidated-report.md                                                          
  - 03-adversarial-review.md                                                           
  - 04-remediation-plan.md                                                             
  - 05-validation-summary.md                                                           
                                                                                       
  That means:                                                                          
  - new artifact schemas                                                               
  - new gates                                                                          
  - maybe new resume model                                                             
                                                                                       
  Workstream 4 — Pipeline integration                                                  
                                                                                       
  You’ll need to rewire roadmap run:                                                   
  - current spec-fidelity phase                                                        
  - current post-run auto-validate                                                     
  - remediation/resume behavior                                                        
  - pass/fail status persistence in .roadmap-state.json                                
                                                                                       
  This is where migration risk is highest.                                             
                                                                                     
  Workstream 5 — MCP boundary design                                                   
                                                                                       
  You already hit this in the tasklist:                                                
  - what is orchestrator-only                                                          
  - what is exposed in allowed-tools                                                   
  - how Auggie/Serena fail open                                                        
  - whether command docs and runtime stay aligned                                      
                                                                                     
  This needs explicit architectural policy before implementation.                      
                                                                                     
  Workstream 6 — Compatibility strategy                                                
                                                                                       
  You need a choice:                                                                   
  - replace in place roadmap validate                                                  
  - or add new runner and migrate gradually                                            
                                                                                       
  I strongly recommend:                                                                
  - add new runner first                                                             
  - keep old validate alive during parity period                                       
                                                                                     
  Workstream 7 — Tests                                                                 
                                                                                       
  You need three test layers:                                                          
  1. runner unit/integration tests                                                     
  2. roadmap run integration tests                                                     
  3. slash-command/skill invocation contract tests                                     
                                                                                       
  Right now you mostly have old runtime coverage, not the new command/skill path.      
                                                                                       
  ---                                                                                
  Key risks / tradeoffs                                                                
                                                                                       
  1. Dual-authority drift                                                              
                                                                                       
  Biggest risk.                                                                        
  If the skill says one thing and Python runtime does another, you recreate the current
   problem.                                                                          
                                                                                       
  Mitigation                                                                           
                                                                                       
  Treat the skill as spec, runner as implementation, and add parity tests.             
                                                                                     
  2. Over-porting the prompt                                                           
                                                                                     
  If you blindly convert every instruction line into Python behavior, you’ll overbuild.
                                                                                     
  Mitigation                                                                           
                                                                                     
  Port only:                                                                           
  - contracts                                                                        
  - artifacts                                                                          
  - gates                                                                            
  - decision points                                                                    
  - invariants                                                                       
                                                                                       
  Not every wording detail.                                                          
                                                                                       
  3. Replacing step-8 fidelity too early                                               
                                                                                       
  Current fidelity/convergence path is real code:                                      
  - src/superclaude/cli/roadmap/executor.py:539                                        
  - src/superclaude/cli/roadmap/convergence.py:386                                     
  - src/superclaude/cli/roadmap/fidelity_checker.py:331                                
                                                                                       
  If you rip it out too early, roadmap run may regress badly.                        
                                                                                       
  Mitigation                                                                         
                                                                                       
  Do staged replacement:                                                               
  - parallel path first                                                                
  - compare outputs                                                                    
  - switch authority later                                                             
                                                                                       
  4. MCP/tool surface creep                                                          
                                                                                       
  Auggie/Serena integration can turn into orchestration sprawl.                      
                                                                                       
  Mitigation                                                                           
                                                                                       
  Define:                                                                              
  - orchestrator-only capabilities                                                     
  - explicit fail-open rules                                                           
  - depth gating                                                                     
  - call caps                                                                          
                                                                                     
  5. Resume/state complexity                                                           
                                                                                     
  The new validation bundle is richer than current state handling.                     
                                                                                       
  Mitigation                                                                           
                                                                                       
  Design state persistence intentionally, not as an afterthought.                      
                                                                                       
  ---                                                                                  
  Is /sc:cli-portify sufficient?                                                     
                                                                                       
  My answer                                                                          
                                                                                       
  Not by itself.                                                                     
                                                                                       
  What it is good for                                                                
                                                                                       
  /sc:cli-portify is good for:                                                         
  - turning the command/skill workflow into a deterministic CLI runner skeleton        
  - identifying phases                                                                 
  - mapping steps to Python orchestration                                            
  - generating a supervised pipeline structure                                         
                                                                                     
  What it is not sufficient for                                                        
                                                                                     
  It does not replace the need to decide:                                              
  - source of truth between skill and runner                                           
  - migration strategy from old fidelity path                                          
  - how step 8 is replaced                                                             
  - artifact compatibility and state model                                             
  - whether this is a new runner or a rewrite of existing validate                     
                                                                                       
  So:                                                                                
                                                                                       
  Use cli-portify for:                                                                 
                                                                                       
  - runner scaffolding                                                                 
  - phase mapping                                                                      
  - initial task decomposition                                                         
  - implementation plan                                                                
                                                                                       
  But first do design work for:                                                      
                                                                                       
  - ownership model                                                                    
  - migration plan                                                                     
  - compatibility strategy                                                             
                                                                                       
  ---                                                                                  
  Recommendation                                                                     
                                                                                       
  Best next move                                                                       
                                                                                       
  Use two-step approach:                                                               
                                                                                     
  Step A — design first                         
                                                                                       
  Create a short architecture spec that answers:                                       
  1. Is validate-roadmap a new runner or replacement of roadmap validate?              
  2. Does roadmap run call it post-run first, or replace step 8 immediately?           
  3. What is the runner’s config contract?                                           
  4. What artifacts are authoritative?                                                 
  5. What parts remain orchestrator-only vs tool-exposed?                            
                                                                                       
  Step B — then use /sc:cli-portify                                                  
                                                                                       
  Once that spec exists, cli-portify becomes very effective.                           
                                                                                       
  ---                                                                                  
  Concrete recommendation                                                              
                                                                                       
  If you want the safest maintainable path:                                            
                                                                                       
  1. Do not replace step 8 yet                                                       
  2. Build new CLI runner for validate-roadmap                                         
  3. Make /sc:validate-roadmap call that runner                                      
  4. Add optional roadmap-run integration behind a flag                                
  5. Compare against current fidelity path                                             
  6. Only then replace current spec-fidelity phase                                     
                                                                                       
  That gives you:                                                                      
  - propagation from command behavior into pipeline                                    
  - one executable implementation                                                      
  - controlled migration                                                               
  - lower regression risk                                                              
                                                                                       
  If you want, I can turn this into:                                                   
  1. a design brief, or                                                              
  2. a cli-portify-ready implementation spec.     