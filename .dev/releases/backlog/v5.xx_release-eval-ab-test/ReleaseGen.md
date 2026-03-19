/sc:spawn "Analyze all eval system materials and synthesize
  into a concrete feature release spec" --strategy parallel    
                                                             
  ## Context                                                   
                                                             
  We just completed v3.0 (Unified Audit Gating). The next      
  deliverable is a CLI-based post-release eval generator and 
  executor that accompanies every release. Three key input     
  documents exist:                                           

  1. **Conversation Decisions from previous planning sessions before v3.0 release** (architecture, data model,     
  build approach): .dev/releases/backlog/v5.xx_release-eval-ab-test/conversation-decisions.md                               
  2. **6-Prompt Eval Strategy** (operational workflow): .dev/releases/backlog/v5.xx_release-eval-ab-test/6PromptV3-Eval.md  
  3. **Refactored Eval Prompts** (detailed prompt designs):
  /config/workspace/IronClaude/.dev/releases/backlog/v5.xx_release-eval-ab-test/eval-prompts     
                                                             
  Additional context:                                          
  - Release spec template:                                   
  src/superclaude/examples/release-spec-template.md            
  - Existing roadmap CLI infrastructure:                     
  src/superclaude/cli/roadmap/                                 
  - Existing audit CLI infrastructure:
  src/superclaude/cli/audit/                                   
  - Sprint CLI infrastructure: src/superclaude/cli/sprint/   
  - Eval runner prototype: scripts/eval_runner.py              
  - A/B testing backlog spec:                                  
  .dev/releases/backlog/v3.1-ab-testing/release-plan.md     
  - THE PROMPTS FOR ALL PARALLEL AGENTS MUST BE EXACTLY AS WRITTEN BELOW AND MUST ALWAYS BEGIN WITH THE CUSTOM COMMAND SPECIFIED BELOW
  - Where possible make use of Auggie MCP And Serena MCP
                                                               
  ## Phase 1: Spawn 4 parallel analysis agents                 
                                                             
  ### Agent 1 — Architecture Extraction                        
  /sc:analyze @.dev/releases/backlog/v5.xx_release-eval-ab-test
  /conversation-decisions.md                                   
  @src/superclaude/cli/roadmap/executor.py                   
  @src/superclaude/cli/roadmap/commands.py                     
  @src/superclaude/cli/sprint/executor.py --depth deep       

  Extract from conversation-decisions.md:                      
  1. All locked architecture decisions (§2-§3) — list each with
   rationale                                                   
  2. The complete data model (§6) — Score, RunResult,        
  TestVerdict, EvalReport                                      
  3. The shared library structure (§5) — src/superclaude/eval/
  module layout                                                
  4. The 7-slice incremental delivery plan (§7)              
  5. All acceptance criteria for both sc:ab-test (§9) and      
  sc:release-eval (§10)                                        
  6. All 13 open decisions (§13) that the spec must resolve    
                                                               
  Cross-reference against the existing CLI infrastructure:     
  - How does the eval executor pattern compare to              
  roadmap/executor.py?                                         
  - How does the eval runner pattern compare to              
  sprint/executor.py?                                          
  - What existing infrastructure (models, gates, convergence)
  can be reused vs must be built new?                          
  
  Write extraction to: .dev/releases/backlog/v5.xx_release-eval
  -ab-test/spec-synthesis/architecture-extraction.md         
                                                               
  ### Agent 2 — Operational Workflow Analysis                  
  /sc:analyze @.dev/releases/backlog/v5.xx_release-eval-ab-test
  /6PromptV3-Eval.md                                           
  @.dev/releases/backlog/v5xx-ab-testing/eval-prompts.md     
  --depth deep                                                 
                                                             
  Analyze the 6-prompt eval workflow:                          
  1. Map each prompt to its SuperClaude commands and their
  sequencing                                                   
  2. Identify which prompts are human-driven (require operator
  judgment) vs automatable (can be CLI steps)                  
  3. Extract the eval pipeline stages implied by the 6 prompts
  — these become CLI steps                                     
  4. Identify the scoring framework requirements embedded in 
  Prompt 5-6                                                   
  5. Extract all validation criteria from Prompt 4 (the 7    
  criteria with PASS/FAIL gates)                               
  6. Map the 13 roadmap pipeline stages to eval coverage —   
  which stages get tested how?                                 
                                                             
  Produce a pipeline stage map: what the CLI eval pipeline     
  looks like when the 6-prompt workflow is codified.         
                                                               
  Write analysis to: .dev/releases/backlog/v5.xx_release-eval-a
  b-test/spec-synthesis/workflow-analysis.md
                                                               
  ### Agent 3 — Infrastructure Gap Analysis                    
  /sc:analyze @src/superclaude/cli/roadmap/executor.py
  @src/superclaude/cli/roadmap/models.py                       
  @src/superclaude/cli/roadmap/gates.py                      
  @src/superclaude/cli/sprint/executor.py                      
  @src/superclaude/cli/sprint/models.py @scripts/eval_runner.py
   --depth deep

  Identify what exists vs what must be built:                  
  1. Existing patterns that the eval CLI should follow (step
  execution, gate checking, convergence, reporting)            
  2. Existing code that can be directly reused (subprocess   
  management, artifact collection, timing)                     
  3. New modules required for src/superclaude/eval/ — for each,
   describe interface and responsibility                       
  4. Integration points: how does `superclaude release-eval  
  run` fit alongside `superclaude roadmap run` and `superclaude
   sprint run`?                                              
  5. The isolation mechanism (.claude/ toggling) — does        
  anything like this exist? What's the implementation          
  complexity?
  6. Judge agent integration — how does this fit the existing  
  Claude subprocess pattern?                                   
  
  Write gap analysis to: .dev/releases/backlog/v5.xx_release-ev
  al-ab-test/spec-synthesis/infrastructure-gaps.md           
                                                               
  ### Agent 4 — Requirements Consolidation                     
  /sc:brainstorm "Consolidate all requirements for the eval CLI
   tool from three source documents" --codebase --depth deep   
                                                             
  Read all three input documents and:                          
  1. Extract every functional requirement (explicit and      
  implied) — deduplicate across documents                      
  2. Extract every non-functional requirement                
  3. Identify contradictions between documents —               
  conversation-decisions.md says X, eval-prompts.md implies Y  
  4. Resolve the 13 open decisions from                        
  conversation-decisions.md §13 with concrete recommendations  
  5. Determine the correct release scope: is this one release
  or should it be split (v1.0 sc:ab-test then v2.0             
  sc:release-eval)?                                          
  6. Produce a consolidated requirements matrix: FR-ID |       
  Description | Source | Priority | Slice                      
  
  Write consolidation to: .dev/releases/backlog/v5.xx_release-e
  val-ab-test/spec-synthesis/requirements-consolidated.md    
                                                               
  ## Phase 2: After all 4 agents complete, synthesize          
  
  Read all 4 agent outputs from .dev/releases/backlog/v5.xx_rel
  ease-eval-ab-test/spec-synthesis/                          
                                                               
  Then invoke:                                                 
  /sc:adversarial --depth quick "Debate whether the 4 analyses
  are internally consistent and surface any contradictions or  
  gaps"                                                      
                                                               
  Provide the adversarial agent with all 4 synthesis documents.
   It must check:
  1. Do the architecture decisions support the operational     
  workflow?                                                    
  2. Does the infrastructure gap analysis account for
  everything the requirements need?                            
  3. Are there requirements that no architecture component   
  addresses?                                                   
  4. Is the delivery slicing consistent across all 4 analyses?
                                                               
  Write debate to: .dev/releases/backlog/v5.xx_release-eval-ab-
  test/spec-synthesis/consistency-debate.md                    
                                                               
  ## Phase 3: Generate the spec                                
  
  After the adversarial debate, invoke:                        
  /sc:design "Write the complete release specification for the
  Post-Release Eval CLI Tool" --type spec --format detailed    
                                                             
  The spec must:                                               
  1. Conform to the template at                              
  src/superclaude/examples/release-spec-template.md            
  2. Incorporate all resolved requirements from Phase 1
  3. Address all contradictions surfaced in Phase 2            
  4. Include the complete data model, CLI surface, pipeline    
  stages, gate definitions                                     
  5. Include the 4-layer failure model (structural → functional
   → quality → regression)                                     
  6. Include the judge agent design and scoring rubric       
  7. Include the isolation mechanism design                    
  8. Include acceptance criteria for the first release scope   
  (sc:ab-test OR sc:release-eval — per Agent 4's               
  recommendation)                                              
  9. Resolve all 13 open decisions with concrete choices and   
  rationale                                                    
  
  Write the spec to: .dev/releases/backlog/v5.xx_release-eval-a
  b-test/release-eval-spec.md                                
                                                               
  After writing, invoke:                                     
  /sc:spec-panel --focus completeness,feasibility,testability
  --mode critique                                              
  
  Apply critical findings and write the final spec. 