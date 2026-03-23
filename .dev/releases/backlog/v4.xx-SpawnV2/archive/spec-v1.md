 /sc:spawn Refactor — Architecture & Component Design                                                                                                                                                                    
                                                                                                                                                                                                                          
  1. Naming & File Layout                                                                                                                                                                                                 
                                                                                                                                                                                                                          
  Following the mandatory -protocol suffix convention (prevents re-entry deadlock):                                                                                                                                       
                                                                                                                                                                                                                          
  ┌─────────────────────┬────────────────────┬─────────────────────────────────────────────────────────────────────────┐                                                                                                  
  │      Component      │        Name        │                                  Path                                   │
  ├─────────────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────┤                                                                                                  
  │ Command             │ spawn              │ src/superclaude/commands/spawn.md                                       │
  ├─────────────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Skill directory     │ sc-spawn-protocol/ │ src/superclaude/skills/sc-spawn-protocol/                               │                                                                                                  
  ├─────────────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────┤                                                                                                  
  │ Skill manifest      │ sc:spawn-protocol  │ src/superclaude/skills/sc-spawn-protocol/SKILL.md                       │                                                                                                  
  ├─────────────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────┤                                                                                                  
  │ Ref: decomposition  │ —                  │ src/superclaude/skills/sc-spawn-protocol/refs/decomposition-patterns.md │
  ├─────────────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────┤                                                                                                  
  │ Ref: delegation     │ —                  │ src/superclaude/skills/sc-spawn-protocol/refs/delegation-matrix.md      │
  ├─────────────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────┤                                                                                                  
  │ Ref: prompt rules   │ —                  │ src/superclaude/skills/sc-spawn-protocol/refs/prompt-construction.md    │
  ├─────────────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────┤                                                                                                  
  │ Agent: orchestrator │ spawn-orchestrator │ src/superclaude/agents/spawn-orchestrator.md                            │
  ├─────────────────────┼────────────────────┼─────────────────────────────────────────────────────────────────────────┤                                                                                                  
  │ Agent: planner      │ spawn-planner      │ src/superclaude/agents/spawn-planner.md                                 │
  └─────────────────────┴────────────────────┴─────────────────────────────────────────────────────────────────────────┘                                                                                                  
                                                                  
  Design decision: Prompt Construction Rules (currently 30 lines in the command) move to refs/prompt-construction.md because they're loaded only during Wave 3 (delegation) and keeping the command thin is the priority. 
  The command file stays under 80 lines.                          
                                                                                                                                                                                                                          
  2. Component Specifications                                     

  2.1 Command: spawn.md (Thin Entry — ~75 lines)                                                                                                                                                                          
  
  ---                                                                                                                                                                                                                     
  name: spawn                                                     
  description: "Meta-system task orchestration with intelligent breakdown and active delegation"
  category: special                                                                                                                                                                                                       
  complexity: high
  allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write, Skill                                                                                                                    
  mcp-servers: [sequential, serena]                                                                                                                                                                                       
  personas: [architect, analyzer]                                                                                                                                                                                         
  ---                                                                                                                                                                                                                     
                                                                                                                                                                                                                          
  # /sc:spawn - Meta-System Task Orchestration                    

  ## Triggers                                                                                                                                                                                                             
  - Complex multi-domain operations requiring intelligent task breakdown
  - Large-scale system operations spanning multiple technical areas                                                                                                                                                       
  - Operations requiring parallel coordination and dependency management                                                                                                                                                  
  - Meta-level orchestration beyond standard command capabilities                                                                                                                                                         
                                                                                                                                                                                                                          
  ## Usage                                                                                                                                                                                                                
  /sc:spawn [complex-task] [--strategy sequential|parallel|adaptive|wave]                                                                                                                                                 
                           [--depth shallow|normal|deep]                                                                                                                                                                  
                           [--no-delegate] [--dry-run] [--resume]
                                                                                                                                                                                                                          
  ## Options                                                                                                                                                                                                              
                                                                                                                                                                                                                          
  | Flag | Default | Description |                                                                                                                                                                                        
  |------|---------|-------------|                                
  | `--strategy` | `adaptive` | Coordination strategy for task execution |
  | `--depth` | `normal` | Decomposition granularity |                                                                                                                                                                    
  | `--no-delegate` | `false` | Plan-only mode: produce hierarchy without spawning agents |                                                                                                                               
  | `--dry-run` | `false` | Preview decomposition without creating tasks |                                                                                                                                                
  | `--resume` | `false` | Resume from Serena checkpoint |                                                                                                                                                                
                                                                                                                                                                                                                          
  ## Behavioral Summary                                                                                                                                                                                                   
                                                                                                                                                                                                                          
  Decomposes complex multi-domain operations into Epic→Story→Task hierarchies with implicit DAG-based dependency resolution, then actively delegates to specialist sub-agents via the Task tool. Uses Auggie MCP for      
  codebase-aware domain detection, Serena for symbol-level dependency mapping and session persistence, and Sequential MCP for complex DAG reasoning.
                                                                                                                                                                                                                          
  ## Activation                                                   

  **MANDATORY**: Before executing any protocol steps, invoke:                                                                                                                                                             
  > Skill sc:spawn-protocol
                                                                                                                                                                                                                          
  Do NOT proceed with protocol execution using only this command file.                                                                                                                                                    
  The full behavioral specification is in the protocol skill.                                                                                                                                                             
                                                                                                                                                                                                                          
  ## Examples                                                     
                                                                                                                                                                                                                          
  ### Complex Feature Implementation                              
  /sc:spawn "implement user authentication system"
  Domains detected: database, backend-api, frontend-ui, testing                                                                                                                                                           
                                                               
  Delegates: /sc:design (schema) → /sc:implement (API) → /sc:build (UI) → /sc:test                                                                                                                                        
                                                                                                                                                                                                                          
                                                                                                                                                                                                                          
  ### Large-Scale Migration (Deep Analysis)                                                                                                                                                                               
  /sc:spawn "migrate legacy monolith to microservices" --strategy wave --depth deep                                                                                                                                       
  5-wave orchestration with Serena checkpoints at each wave boundary               
                                                                                                                                                                                                                          
                                                                                                                                                                                                                          
  ### Plan-Only Preview                                                                                                                                                                                                   
  /sc:spawn "establish CI/CD pipeline with security scanning" --no-delegate                                                                                                                                               
  Produces hierarchy document without spawning agents                                                                                                                                                                     
                                                                                                                                                                                                                          
                                                                  
  ### Dry Run
  /sc:spawn "refactor payment module" --dry-run                                                                                                                                                                           
  Shows decomposition + delegation map without creating tasks
                                                                                                                                                                                                                          
                                                                  
  ## Boundaries
                                                                                                                                                                                                                          
  **Will:**                                                                              
  - Decompose complex operations into coordinated task hierarchies with dependency graphs                                                                                                                                 
  - Actively delegate tasks to sub-agents via Task tool (default behavior)                                                                                                                                                
  - Track delegation progress and aggregate results                                                                                                                                                                       
                                                                                                                                                                                                                          
  **Will Not:**                                                                                                                                                                                                           
  - Execute leaf-level implementation tasks directly                                                                                                                                                                      
  - Write or modify application code                                                                                                                                                                                      
  - Replace domain-specific commands for simple operations                                                                                                                                                                
  - Override user coordination preferences                                                                                                                                                                                
                                                                                                                                                                                                                          
  Key differences from current: Frontmatter now declares MCP servers, personas, and allowed-tools. Body reduced to ~75 lines. All protocol logic moved to skill. Active delegation is the default (not "STOP AFTER        
  DECOMPOSITION").                                                                                                                                                                                                        
                                                                  
  ---
  2.2 Skill: sc-spawn-protocol/SKILL.md (~400-450 lines)
                                                                                                                                                                                                                          
  ---
  name: sc:spawn-protocol                                                                                                                                                                                                 
  description: "Full behavioral protocol for sc:spawn — meta-system task orchestration
    with codebase-aware decomposition, DAG-based dependency resolution, and active delegation"                                                                                                                            
  allowed-tools: Read, Glob, Grep, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Write                                                                                                                           
  ---                                                                                                                                                                                                                     
                                                                                                                                                                                                                          
  # /sc:spawn — Meta-System Orchestration Protocol                                                                                                                                                                        
                                                                  
  <!-- Extended metadata (for documentation, not parsed):                                                                                                                                                                 
  category: special                                               
  complexity: high                                                                                                                                                                                                        
  mcp-servers: [sequential, serena]                                                                                                                                                                                       
  personas: [architect, analyzer]                                                                                                                                                                                         
  -->                                                                                                                                                                                                                     
                                                                                                                                                                                                                          
  ## Triggers                                                                                                                                                                                                             
                                                                  
  sc:spawn-protocol is invoked ONLY by the `sc:spawn` command via                                                                                                                                                         
  `Skill sc:spawn-protocol` in the `## Activation` section.       
  It is never invoked directly by users.                                                                                                                                                                                  
                                                                                                                                                                                                                          
  ## Classification (MANDATORY FIRST OUTPUT)                                                                                                                                                                              
                                                                                                                                                                                                                          
  Emit this EXACT header format as your first output:                                                                                                                                                                     
                                                                  
  <!-- SC:SPAWN:CLASSIFICATION                                                                                                                                                                                            
  strategy: [sequential|parallel|adaptive|wave]                   
  depth: [shallow|normal|deep]                                                                                                                                                                                            
  domains_detected: [N]                                           
  estimated_tasks: [N]                                                                                                                                                                                                    
  delegation_mode: [active|plan-only|dry-run]                     
  -->                                                                                                                                                                                                                     
                                                                  
  ## 4-Wave Execution Protocol                                                                                                                                                                                            
                                                                  
  ### Wave 0: Prerequisites                                                                                                                                                                                               
                                                                  
  **Preconditions**: User has provided a task description.                                                                                                                                                                
  **STOP if**: No task description provided. Emit usage hint and exit.
                                                                                                                                                                                                                          
  1. Parse flags: `--strategy`, `--depth`, `--no-delegate`, `--dry-run`, `--resume`                                                                                                                                       
  2. If `--resume`: Load Serena memory checkpoint, skip to last incomplete wave                                                                                                                                           
  3. Load codebase context (parallel):                                                                                                                                                                                    
     - **Query 1** (Auggie): "{task_description} — find relevant code, existing
       implementations, module boundaries, and integration points"                                                                                                                                                        
     - **Query 2** (Auggie): "Project architecture, directory structure, domain                                                                                                                                           
       boundaries, and conventions"                                                                                                                                                                                       
  4. If Auggie unavailable: WARN, fall back to Serena `get_symbols_overview`                                                                                                                                              
     on top-level directories (depth: 1). If Serena also unavailable, fall back                                                                                                                                           
     to Glob pattern matching + Grep keyword search.                                                                                                                                                                      
                                                                                                                                                                                                                          
  **Postconditions**: Codebase context loaded. Flags parsed. Ready for analysis.                                                                                                                                          
  **Checkpoint**: Save wave-0 state to Serena memory.                                                                                                                                                                     
                                                                                                                                                                                                                          
  ### Wave 1: Scope Analysis                                      
                                                                                                                                                                                                                          
  **Preconditions**: Wave 0 complete. Codebase context available.                                                                                                                                                         
  
  1. **Domain Detection**: From codebase context, identify distinct technical domains                                                                                                                                     
     touched by the task. Classify each as one of:                
     - `database` | `backend-api` | `frontend-ui` | `infrastructure` |                                                                                                                                                    
       `security` | `testing` | `documentation` | `devops` | `data-pipeline`                                                                                                                                              
  2. **Module Mapping**: For each detected domain, identify:                                                                                                                                                              
     - Primary directories/files affected                                                                                                                                                                                 
     - Key symbols (classes, functions, endpoints) via Serena `find_symbol`                                                                                                                                               
     - External dependencies and integration points                                                                                                                                                                       
  3. **Dependency Detection**: Use Serena `find_referencing_symbols` to trace                                                                                                                                             
     cross-module dependencies. Build adjacency list of domain→domain                                                                                                                                                     
     dependencies.                                                                                                                                                                                                        
  4. **Complexity Assessment**: Score overall complexity (0.0-1.0):                                                                                                                                                       
     - domain_count > 3: +0.3                                                                                                                                                                                             
     - cross-module_dependencies > 5: +0.2                                                                                                                                                                                
     - estimated_files > 20: +0.2                                                                                                                                                                                         
     - security_domain_involved: +0.2                                                                                                                                                                                     
     - If complexity > 0.7 AND `--strategy auto`: auto-upgrade to `wave` strategy                                                                                                                                         
                                                                                                                                                                                                                          
  **Postconditions**: Domain list, module map, dependency adjacency list, complexity score.                                                                                                                               
  **Checkpoint**: Save wave-1 state to Serena memory.                                                                                                                                                                     
                                                                                                                                                                                                                          
  ### Wave 2: Decomposition                                                                                                                                                                                               
                                                                                                                                                                                                                          
  **Preconditions**: Wave 1 complete. Domain and dependency data available.                                                                                                                                               
  **Load ref**: `refs/decomposition-patterns.md`                  
                                                                                                                                                                                                                          
  1. **Epic Construction**: One Epic per detected domain (or logical grouping                                                                                                                                             
     if domains overlap heavily).                                                                                                                                                                                         
  2. **Story Decomposition**: Break each Epic into Stories representing                                                                                                                                                   
     coherent units of work. Apply granularity rules from ref:                                                                                                                                                            
     - `shallow`: 1-2 Stories per Epic (high-level only)                                                                                                                                                                  
     - `normal`: 2-5 Stories per Epic                                                                                                                                                                                     
     - `deep`: 3-8 Stories per Epic with subtask decomposition                                                                                                                                                            
  3. **Task Assignment**: Each Story becomes one or more Tasks. Each Task                                                                                                                                                 
     maps to exactly one `/sc:*` command for delegation.                                                                                                                                                                  
  4. **DAG Construction**: Using the dependency adjacency list from Wave 1:                                                                                                                                               
     - Tasks with no cross-domain dependencies → parallel group                                                                                                                                                           
     - Tasks depending on outputs from other domains → sequential with                                                                                                                                                    
       explicit `depends_on` edges                                                                                                                                                                                        
     - Detect parallel groups (tasks safe to run concurrently)                                                                                                                                                            
     - Use Sequential MCP for complex dependency reasoning if                                                                                                                                                             
       cross-module_dependencies > 5                                                                                                                                                                                      
  5. **Strategy Application**:                                                                                                                                                                                            
     - `sequential`: All tasks in linear dependency order                                                                                                                                                                 
     - `parallel`: Maximum parallelism, only hard dependencies enforced                                                                                                                                                   
     - `adaptive`: Hybrid — parallelize where safe, sequence where required                                                                                                                                               
     - `wave`: Group into 3-5 execution waves with checkpoints between                                                                                                                                                    
                                                                                                                                                                                                                          
  **Postconditions**: Complete task hierarchy with DAG edges and parallel groups.                                                                                                                                         
  **Checkpoint**: Save wave-2 state to Serena memory.                                                                                                                                                                     
                                                                                                                                                                                                                          
  ### Wave 3: Delegation                                          
                                                                                                                                                                                                                          
  **Preconditions**: Wave 2 complete. Task hierarchy with DAG available.                                                                                                                                                  
  **Load ref**: `refs/delegation-matrix.md`, `refs/prompt-construction.md`
                                                                                                                                                                                                                          
  **If `--dry-run`**: Output the task hierarchy document and STOP. Do not                                                                                                                                                 
  create tasks or spawn agents.
                                                                                                                                                                                                                          
  **If `--no-delegate`**: Create TaskCreate entries for tracking but do NOT                                                                                                                                               
  spawn sub-agents. Output hierarchy document with delegation map.                                                                                                                                                        
                                                                                                                                                                                                                          
  **Default (active delegation)**:                                                                                                                                                                                        
                                                                                                                                                                                                                          
  1. **Task Creation**: For each Task in the hierarchy:                                                                                                                                                                   
     - `TaskCreate` with description, status `pending`, dependencies noted
  2. **Prompt Construction**: For each delegated task, apply prompt                                                                                                                                                       
     construction rules (from ref):                                                                                                                                                                                       
     - Rule 1: Resolve file paths before delegation (Glob/Read)                                                                                                                                                           
     - Rule 2: Inject tiered evidence requirements (verification vs discovery)                                                                                                                                            
     - Rule 3: Inject cross-reference counts when available                                                                                                                                                               
     - Do NOT override delegated command's output structure                                                                                                                                                               
  3. **Agent Dispatch**: For each parallel group, dispatch tasks via Task tool:                                                                                                                                           
     - Read the appropriate agent `.md` file from `src/superclaude/agents/`                                                                                                                                               
     - Inject agent definition + enriched prompt into Task prompt                                                                                                                                                         
     - Dispatch parallel groups concurrently                                                                                                                                                                              
     - Wait for group completion before dispatching dependent groups                                                                                                                                                      
  4. **Progress Tracking**:                                                                                                                                                                                               
     - `TaskUpdate` as each sub-agent completes                                                                                                                                                                           
     - `TaskList`/`TaskGet` for status monitoring                                                                                                                                                                         
     - If a sub-agent fails: retry once, then mark as `manual` and continue                                                                                                                                               
  5. **Result Aggregation**: Collect outputs from all completed tasks.                                                                                                                                                    
     Compile summary with per-task status.                                                                                                                                                                                
                                                                                                                                                                                                                          
  **Postconditions**: All tasks delegated (or documented). Results aggregated.                                                                                                                                            
                                                                                                                                                                                                                          
  ## Return Contract                                                                                                                                                                                                      
                                                                  
  | Field | Type | Description |                                                                                                                                                                                          
  |-------|------|-------------|                                  
  | `status` | string | `success` \| `partial` \| `failed` |                                                                                                                                                              
  | `task_hierarchy_path` | string | Path to written hierarchy document |                                                                                                                                                 
  | `tasks_created` | int | Number of TaskCreate entries |                                                                                                                                                                
  | `delegation_map` | object | Task ID → delegated `/sc:*` command |                                                                                                                                                     
  | `parallel_groups` | list | Groups of tasks safe to run concurrently |                                                                                                                                                 
  | `completion_summary` | object | Per-task status (completed/failed/manual) |                                                                                                                                           
                                                                                                                                                                                                                          
  ## Agent Delegation                                                                                                                                                                                                     
                                                                                                                                                                                                                          
  | Agent | Role | Dispatched By | When |                                                                                                                                                                                 
  |-------|------|--------------|------|                          
  | `spawn-planner` | Deep codebase analysis for domain/dependency detection | This skill (Wave 1) | Always for `--depth deep`, or when domain_count > 4 |                                                                
  | `spawn-orchestrator` | Progress tracking and result aggregation | This skill (Wave 3) | When tasks_created > 8 |                                                                                                      
                                                                                                                                                                                                                          
  **Dispatch protocol**: Read agent `.md` via Read tool → inject into Task prompt                                                                                                                                         
  (per v2.01 convention: `subagent_type` is dead metadata; agent context is                                                                                                                                               
  injected via prompt).                                                                                                                                                                                                   
                                                                  
  ## Error Handling                                                                                                                                                                                                       
                                                                  
  | Scenario | Behavior | Fallback |                                                                                                                                                                                      
  |----------|----------|----------|                              
  | Missing task description | STOP with usage hint | None |                                                                                                                                                              
  | Auggie unavailable | WARN, use Serena `get_symbols_overview` | Glob + Grep |                                                                                                                                          
  | Serena unavailable | WARN, use Grep for dependency detection | Native file analysis |                                                                                                                                 
  | Sequential unavailable | WARN, use native reasoning for DAG | Simpler parallel groups |                                                                                                                               
  | Sub-agent delegation fails | Retry once, mark as `manual` | Continue with N-1 tasks |                                                                                                                                 
  | Depth exceeds token budget | Auto-downgrade to `normal` | WARN user |                                                                                                                                                 
  | `--resume` but no checkpoint | WARN, start from Wave 0 | Full restart |                                                                                                                                               
                                                                                                                                                                                                                          
  ## Will Do                                                                                                                                                                                                              
  - Decompose complex operations into DAG-structured task hierarchies                                                                                                                                                     
  - Actively delegate to sub-agents with enriched prompts                                                                                                                                                                 
  - Track progress and aggregate results across parallel groups   
  - Persist state at wave boundaries for session resumability                                                                                                                                                             
                                                                                                                                                                                                                          
  ## Will Not Do                                                                                                                                                                                                          
  - Execute leaf-level implementation tasks directly                                                                                                                                                                      
  - Write or modify application code                              
  - Override delegated command protocols or output formats
  - Skip dependency analysis for parallel safety                                                                                                                                                                          
                                                                                                                                                                                                                          
  ---                                                                                                                                                                                                                     
  2.3 Ref: refs/decomposition-patterns.md (~150 lines)                                                                                                                                                                    
                                                                                                                                                                                                                          
  Loaded: Wave 2 only.
                                                                                                                                                                                                                          
  # Decomposition Patterns Reference                                                                                                                                                                                      
                                                                                                                                                                                                                          
  ## Epic Construction Rules                                                                                                                                                                                              
                                                                  
  ### Domain-to-Epic Mapping                                                                                                                                                                                              
  Each detected domain typically maps to one Epic. Merge domains when:
  - Two domains share >60% of the same files                                                                                                                                                                              
  - One domain has only 1-2 files (absorb into nearest domain)                                                                                                                                                            
                                                                                                                                                                                                                          
  ### Naming Convention                                                                                                                                                                                                   
  Epic names follow: `[DOMAIN] — [Outcome Description]`                                                                                                                                                                   
  Examples:                                                                                                                                                                                                               
  - `DATABASE — Design and implement user schema`                                                                                                                                                                         
  - `BACKEND-API — Build authentication endpoints`                                                                                                                                                                        
  - `TESTING — Establish integration test coverage`                                                                                                                                                                       
                                                                                                                                                                                                                          
  ## Story Granularity by Depth                                                                                                                                                                                           
                                                                                                                                                                                                                          
  ### Shallow (--depth shallow)                                                                                                                                                                                           
  - 1-2 Stories per Epic                                          
  - Each Story represents a complete domain deliverable
  - No subtask decomposition                                                                                                                                                                                              
  - Best for: High-level planning, estimation, overview                                                                                                                                                                   
                                                                                                                                                                                                                          
  ### Normal (--depth normal)                                                                                                                                                                                             
  - 2-5 Stories per Epic                                                                                                                                                                                                  
  - Stories represent coherent feature slices                     
  - Light subtask notes (bullet points, not formal tasks)
  - Best for: Sprint planning, team coordination                                                                                                                                                                          
                                                                                                                                                                                                                          
  ### Deep (--depth deep)                                                                                                                                                                                                 
  - 3-8 Stories per Epic                                                                                                                                                                                                  
  - Stories decomposed into formal subtasks                                                                                                                                                                               
  - Each subtask has: description, estimated complexity, tool hints                                                                                                                                                       
  - Best for: Solo execution, detailed delegation, complex migrations                                                                                                                                                     
                                                                                                                                                                                                                          
  ## Task-to-Command Mapping Rules                                                                                                                                                                                        
                                                                                                                                                                                                                          
  Each Task maps to exactly ONE `/sc:*` command. Selection criteria:                                                                                                                                                      
                                                                  
  | Task Type | Primary Command | Fallback |                                                                                                                                                                              
  |-----------|----------------|----------|                       
  | Schema/model design | `/sc:design --type database` | `/sc:design --type component` |                                                                                                                                  
  | API design | `/sc:design --type api` | `/sc:design --type architecture` |                                                                                                                                             
  | Architecture decisions | `/sc:design --type architecture` | — |                                                                                                                                                       
  | Feature implementation | `/sc:implement` | `/sc:build` |                                                                                                                                                              
  | Bug fix | `/sc:task "fix ..."` | `/sc:troubleshoot` |                                                                                                                                                                 
  | Test creation | `/sc:test` | `/sc:task "test ..."` |                                                                                                                                                                  
  | Documentation | `/sc:document` | — |                                                                                                                                                                                  
  | Code cleanup | `/sc:cleanup` | `/sc:improve` |                                                                                                                                                                        
  | Security hardening | `/sc:task --force-strict` | `/sc:analyze --focus security` |                                                                                                                                     
  | Infrastructure/DevOps | `/sc:task` with devops persona | `/sc:implement` |                                                                                                                                            
  | Research/investigation | `/sc:research` | `/sc:analyze` |                                                                                                                                                             
                                                                                                                                                                                                                          
  ## DAG Edge Rules                                                                                                                                                                                                       
                                                                                                                                                                                                                          
  ### Hard Dependencies (sequential)                                                                                                                                                                                      
  - Schema design MUST complete before API implementation         
  - API implementation MUST complete before frontend integration                                                                                                                                                          
  - Core module changes MUST complete before dependent module changes
  - Security audit SHOULD complete before deployment tasks                                                                                                                                                                
                                                                  
  ### Soft Dependencies (parallel-safe with coordination)                                                                                                                                                                 
  - Tests can start in parallel with implementation (test-first)  
  - Documentation can start in parallel with implementation                                                                                                                                                               
  - Independent domain Epics with no shared files                 
                                                                                                                                                                                                                          
  ### Parallel Group Assignment                                   
  Tasks in the same parallel group:                                                                                                                                                                                       
  - Share no file dependencies                                                                                                                                                                                            
  - Have no data-flow dependencies                                                                                                                                                                                        
  - Can be dispatched as concurrent Task tool calls                                                                                                                                                                       
                                                                                                                                                                                                                          
  ---                                                                                                                                                                                                                     
  2.4 Ref: refs/delegation-matrix.md (~120 lines)                                                                                                                                                                         
                                                                  
  Loaded: Wave 3 only.
                                                                                                                                                                                                                          
  # Delegation Matrix Reference
                                                                                                                                                                                                                          
  ## Command Delegation Targets                                                                                                                                                                                           
                                                                                                                                                                                                                          
  ### Implementation Commands                                                                                                                                                                                             
  | Command | When to Delegate | Persona | MCP Hint |             
  |---------|-----------------|---------|----------|                                                                                                                                                                      
  | `/sc:implement` | New feature, endpoint, module | backend, frontend | --c7 |
  | `/sc:build` | Compile, package, scaffold | devops | -- |                                                                                                                                                              
  | `/sc:task` | General task, compound operations | auto-detect | --seq |                                                                                                                                                
  | `/sc:task --force-strict` | Security, auth, database changes | security | --seq |                                                                                                                                     
                                                                                                                                                                                                                          
  ### Design Commands                                                                                                                                                                                                     
  | Command | When to Delegate | Persona | MCP Hint |                                                                                                                                                                     
  |---------|-----------------|---------|----------|                                                                                                                                                                      
  | `/sc:design --type architecture` | System structure, patterns | architect | --seq |
  | `/sc:design --type api` | Endpoint contracts, schemas | backend | --c7 |                                                                                                                                              
  | `/sc:design --type database` | Schema, migrations, models | backend | --c7 |                                                                                                                                          
  | `/sc:design --type component` | UI component interfaces | frontend | --magic |                                                                                                                                        
                                                                                                                                                                                                                          
  ### Quality Commands                                            
  | Command | When to Delegate | Persona | MCP Hint |                                                                                                                                                                     
  |---------|-----------------|---------|----------|              
  | `/sc:test` | Test creation, coverage analysis | qa | --play |                                                                                                                                                         
  | `/sc:analyze` | Code review, quality assessment | analyzer | --seq |                                                                                                                                                  
  | `/sc:cleanup` | Dead code, structure optimization | refactorer | --seq |                                                                                                                                              
                                                                                                                                                                                                                          
  ### Research Commands                                                                                                                                                                                                   
  | Command | When to Delegate | Persona | MCP Hint |                                                                                                                                                                     
  |---------|-----------------|---------|----------|                                                                                                                                                                      
  | `/sc:research` | External knowledge, library docs | — | --tavily |
  | `/sc:explain` | Understanding existing code | mentor | --c7 |                                                                                                                                                         
                                                                                                                                                                                                                          
  ## Agent Selection for Task Dispatch                                                                                                                                                                                    
                                                                                                                                                                                                                          
  When dispatching via the Task tool, select the Claude Code agent type                                                                                                                                                   
  based on the delegated command:                                 
                                                                                                                                                                                                                          
  | Delegated Command | Agent Type | Model Hint |                                                                                                                                                                         
  |-------------------|-----------|------------|                                                                                                                                                                          
  | `/sc:design` | system-architect | opus |                                                                                                                                                                              
  | `/sc:implement` | general-purpose | opus |                                                                                                                                                                            
  | `/sc:build` | devops-architect | sonnet |                                                                                                                                                                             
  | `/sc:test` | quality-engineer | sonnet |                                                                                                                                                                              
  | `/sc:analyze` | general-purpose | opus |                      
  | `/sc:cleanup` | refactoring-expert | sonnet |                                                                                                                                                                         
  | `/sc:research` | deep-research-agent | opus |                 
  | `/sc:task` | general-purpose | opus |                                                                                                                                                                                 
                                                                                                                                                                                                                          
  ## Dispatch Template                                                                                                                                                                                                    
                                                                                                                                                                                                                          
  When constructing a Task tool dispatch:                                                                                                                                                                                 
                                                                  
  Agent prompt template:                                                                                                                                                                                                  
  
  You are executing a delegated task from /sc:spawn orchestration.                                                                                                                                                        
                                                                  
  Task                                                                                                                                                                                                                    
                                                                  
  {enriched_task_description}                                                                                                                                                                                             
                                                                  
  Files                                                                                                                                                                                                                   
  
  {resolved_absolute_paths}                                                                                                                                                                                               
                                                                  
  Evidence Standard                                                                                                                                                                                                       
                                                                  
  {tiered_evidence_requirement}

  Cross-References                                                                                                                                                                                                        
  
  {injected_counts_if_available}                                                                                                                                                                                          
                                                                  
  Delegated Command                                                                                                                                                                                                       
                                                                  
  Execute this as: {delegated_sc_command}                                                                                                                                                                                 
  
  Output                                                                                                                                                                                                                  
                                                                  
  Write results to: {output_path}                                                                                                                                                                                         
                                                                  
                                                                                                                                                                                                                          
                                                                  
  ---                                                                                                                                                                                                                     
  2.5 Ref: refs/prompt-construction.md (~80 lines)                
                                                  
  Loaded: Wave 3 only. Moved from current spawn.md lines 37-67.
                                                                                                                                                                                                                          
  # Prompt Construction Rules
                                                                                                                                                                                                                          
  When constructing prompts for delegated agents, sc:spawn MUST enrich                                                                                                                                                    
  the user's intent with operational specificity. Passing a bare goal
  to a delegated command produces structurally sound but evidence-thin                                                                                                                                                    
  output. However, do NOT override the delegated command's own output                                                                                                                                                     
  structure — delegated protocols produce better analytical organization                                                                                                                                                  
  than orchestrator-imposed templates.                                                                                                                                                                                    
                                                                                                                                                                                                                          
  ## Rule 1: Resolve File Paths Before Delegation                                                                                                                                                                         
                                                                                                                                                                                                                          
  Before spawning synchronous agents, resolve all input file paths                                                                                                                                                        
  using Glob/Read. Each agent prompt MUST include absolute paths to
  every file the agent needs to read. Never delegate path discovery                                                                                                                                                       
  to the sub-agent.                                                                                                                                                                                                       
                                                                                                                                                                                                                          
  For async task hierarchies where agents run later or in separate                                                                                                                                                        
  contexts, include path hints (directory + glob pattern) rather than                                                                                                                                                     
  requiring pre-resolution of every path.                                                                                                                                                                                 
                                                                                                                                                                                                                          
  ## Rule 2: Inject Tiered Evidence Requirements                                                                                                                                                                          
                                                                                                                                                                                                                          
  Delegated prompts that produce analytical output MUST include an                                                                                                                                                        
  evidence standard, but the tier depends on the task type:
                                                                                                                                                                                                                          
  **Verification tasks** (coverage checks, dependency validation,                                                                                                                                                         
  consistency audits):                                                                                                                                                                                                    
  Evidence standard: cite specific line numbers, task IDs, section                                                                                                                                                        
  references, or direct quotes from source documents for every finding.                                                                                                                                                   
  Unsupported assertions must be flagged as LOW CONFIDENCE.                                                                                                                                                               
                                                                                                                                                                                                                          
  **Discovery tasks** (gap detection, risk assessment, open-ended                                                                                                                                                         
  reflection):                                                                                                                                                                                                            
  Evidence standard: support findings with specific references where                                                                                                                                                      
  possible. Findings based on inference or absence of evidence should                                                                                                                                                     
  be flagged as INFERENTIAL and include the reasoning chain. Do not                                                                                                                                                       
  let citation requirements constrain exploratory analysis.                                                                                                                                                               
                                                                                                                                                                                                                          
  ## Rule 3: Inject Cross-Reference Counts (When Available)                                                                                                                                                               
                                                                                                                                                                                                                          
  When Rule 1 has already read a source document and the delegated task                                                                                                                                                   
  involves coverage verification, extract and inject the known count
  (e.g., "The merged plan contains 20 edits — verify all 20 are                                                                                                                                                           
  covered"). Do NOT pre-read documents solely for counting — this rule                                                                                                                                                    
  applies opportunistically when path resolution has already loaded                                                                                                                                                       
  the file.                                                                                                                                                                                                               
                                                                                                                                                                                                                          
  ---                                                                                                                                                                                                                     
  2.6 Agent: spawn-orchestrator.md (~70 lines)                    
                                                                                                                                                                                                                          
  ---
  name: spawn-orchestrator                                                                                                                                                                                                
  description: Progress tracking and result aggregation for sc:spawn multi-task orchestrations
  category: meta                                                                                                                                                                                                          
  ---                                                                                                                                                                                                                     
                                                                                                                                                                                                                          
  # Spawn Orchestrator                                                                                                                                                                                                    
                                                                  
  ## Triggers
  - Invoked by `sc:spawn-protocol` skill during Wave 3 when tasks_created > 8
  - Large-scale delegations requiring dedicated progress management                                                                                                                                                       
  - Multi-group parallel dispatches requiring coordination across groups                                                                                                                                                  
                                                                                                                                                                                                                          
  ## Behavioral Mindset                                                                                                                                                                                                   
  Track progress across all delegated tasks with precision. Focus on status                                                                                                                                               
  accuracy, failure detection, and comprehensive result aggregation. Never                                                                                                                                                
  execute leaf tasks — only monitor and report.                                                                                                                                                                           
                                                                                                                                                                                                                          
  ## Model Preference                                                                                                                                                                                                     
  High-capability model (opus preferred). Requires strong reasoning for                                                                                                                                                   
  coordinating many concurrent agents and synthesizing diverse outputs.                                                                                                                                                   
                                                                                                                                                                                                                          
  ## Tools                                                                                                                                                                                                                
  - **TaskCreate**: Create tracked tasks for each delegation                                                                                                                                                              
  - **TaskUpdate**: Update status as sub-agents complete or fail                                                                                                                                                          
  - **TaskList**: Monitor overall progress across all tasks       
  - **TaskGet**: Retrieve detailed status for specific tasks                                                                                                                                                              
  - **Task**: Dispatch sub-agents for delegated commands                                                                                                                                                                  
  - **Read**: Load agent definitions for prompt injection                                                                                                                                                                 
  - **Write**: Produce orchestration summary and hierarchy document                                                                                                                                                       
  - **Glob**: Discover output artifacts from completed tasks                                                                                                                                                              
                                                                                                                                                                                                                          
  ## Responsibilities                                                                                                                                                                                                     
                                                                                                                                                                                                                          
  1. **Create task entries**: One TaskCreate per delegated task from the hierarchy                                                                                                                                        
  2. **Dispatch parallel groups**: Launch concurrent Task agents for each
     parallel group, respecting DAG ordering between groups                                                                                                                                                               
  3. **Monitor completion**: Poll TaskList/TaskGet for status updates
  4. **Handle failures**: Retry failed tasks once, then mark as `manual`                                                                                                                                                  
     and continue with remaining tasks                                                                                                                                                                                    
  5. **Aggregate results**: Collect outputs from all completed tasks,                                                                                                                                                     
     compile summary with per-task status and artifact paths                                                                                                                                                              
  6. **Produce orchestration report**: Write hierarchy document with final                                                                                                                                                
     status, delegation map, and completion summary                                                                                                                                                                       
                                                                                                                                                                                                                          
  ## Outputs                                                                                                                                                                                                              
  - **spawn-hierarchy.md**: Full task hierarchy with DAG, delegation map,                                                                                                                                                 
    and per-task completion status                                                                                                                                                                                        
  - **Return contract fields**: status, tasks_created, delegation_map,                                                                                                                                                    
    parallel_groups, completion_summary                                                                                                                                                                                   
                                                                                                                                                                                                                          
  ## Does NOT                                                                                                                                                                                                             
  - Execute leaf-level implementation work
  - Write or modify application code                                                                                                                                                                                      
  - Make architectural decisions about task decomposition         
  - Override the delegation matrix from the skill protocol                                                                                                                                                                
                                                                                                                                                                                                                          
  ## Boundaries                                                                                                                                                                                                           
                                                                                                                                                                                                                          
  **Will:**                                                       
  - Track and aggregate results from arbitrarily many concurrent delegations
  - Apply retry-once policy for failed tasks with clear escalation path                                                                                                                                                   
  - Report progress at group-completion boundaries                                                                                                                                                                        
                                                                                                                                                                                                                          
  **Will Not:**                                                                                                                                                                                                           
  - Modify task decomposition produced by Wave 2                                                                                                                                                                          
  - Skip tasks or reorder DAG dependencies                                                                                                                                                                                
  - Proceed past a group boundary if a hard-dependency task failed                                                                                                                                                        
                                                                                                                                                                                                                          
  ---                                                                                                                                                                                                                     
  2.7 Agent: spawn-planner.md (~65 lines)                                                                                                                                                                                 
                                                                                                                                                                                                                          
  ---
  name: spawn-planner                                                                                                                                                                                                     
  description: Deep codebase analysis for domain detection and dependency mapping in sc:spawn orchestrations
  category: analysis                                                                                                                                                                                                      
  ---                                                                                                                                                                                                                     
                                                                                                                                                                                                                          
  # Spawn Planner                                                                                                                                                                                                         
                                                                  
  ## Triggers
  - Invoked by `sc:spawn-protocol` skill during Wave 1 when `--depth deep`
    or when domain_count > 4                                                                                                                                                                                              
  - Complex codebases requiring thorough module boundary and dependency analysis
  - Tasks involving unfamiliar or large-scale codebases                                                                                                                                                                   
                                                                                                                                                                                                                          
  ## Behavioral Mindset                                                                                                                                                                                                   
  Investigate the codebase systematically to produce accurate domain maps                                                                                                                                                 
  and dependency graphs. Prioritize precision over speed — missed dependencies                                                                                                                                            
  cause delegation failures. Use semantic tools (Auggie, Serena) first,                                                                                                                                                   
  fall back to pattern-based tools only when semantic tools are unavailable.                                                                                                                                              
                                                                                                                                                                                                                          
  ## Model Preference                                                                                                                                                                                                     
  High-capability model (opus preferred). Deep codebase analysis requires                                                                                                                                                 
  strong reasoning about code relationships and architectural boundaries.
                                                                                                                                                                                                                          
  ## Tools
  - **mcp__auggie-mcp__codebase-retrieval**: Semantic codebase search for                                                                                                                                                 
    domain detection and architecture understanding                                                                                                                                                                       
  - **Serena tools** (get_symbols_overview, find_symbol, find_referencing_symbols):                                                                                                                                       
    Symbol-level navigation for dependency tracing                                                                                                                                                                        
  - **Read**: Load specific files identified by semantic search                                                                                                                                                           
  - **Glob**: Discover file patterns within detected domains                                                                                                                                                              
  - **Grep**: Keyword search for cross-module references                                                                                                                                                                  
                                                                                                                                                                                                                          
  ## Responsibilities                                                                                                                                                                                                     
                                                                                                                                                                                                                          
  1. **Domain detection**: Identify distinct technical domains affected by
     the task using Auggie retrieval + directory structure analysis
  2. **Module boundary mapping**: For each domain, identify primary                                                                                                                                                       
     directories, entry points, and key symbols                                                                                                                                                                           
  3. **Dependency tracing**: Use Serena `find_referencing_symbols` to build                                                                                                                                               
     cross-module dependency adjacency list                                                                                                                                                                               
  4. **Complexity scoring**: Assess overall complexity based on domain count,                                                                                                                                             
     dependency density, file count, and security involvement     
  5. **Produce structured analysis**: Output domain map, dependency graph,                                                                                                                                                
     and complexity score in structured format for Wave 2 consumption
                                                                                                                                                                                                                          
  ## Outputs                                                      
  - **Domain map**: List of domains with primary directories and key symbols                                                                                                                                              
  - **Dependency graph**: Adjacency list of domain→domain dependencies with                                                                                                                                               
    evidence (specific symbols/files that create the dependency)                                                                                                                                                          
  - **Complexity score**: 0.0-1.0 with factor breakdown                                                                                                                                                                   
                                                                                                                                                                                                                          
  ## Does NOT                                                                                                                                                                                                             
  - Decompose tasks into Epics or Stories (that's Wave 2)                                                                                                                                                                 
  - Make delegation decisions (that's Wave 3)                                                                                                                                                                             
  - Modify any files                                                                                                                                                                                                      
  - Execute any implementation work                                                                                                                                                                                       
                                                                                                                                                                                                                          
  ## Boundaries                                                                                                                                                                                                           
                                                                                                                                                                                                                          
  **Will:**                                                                                                                                                                                                               
  - Produce accurate, evidence-backed domain maps and dependency graphs
  - Use the best available tools (Auggie → Serena → Glob/Grep fallback chain)                                                                                                                                             
  - Flag LOW CONFIDENCE findings when dependency evidence is inferential                                                                                                                                                  
                                                                                                                                                                                                                          
  **Will Not:**                                                                                                                                                                                                           
  - Guess at dependencies without evidence from code analysis                                                                                                                                                             
  - Proceed without investigating all domains detected in initial scan                                                                                                                                                    
  - Modify the codebase or produce implementation artifacts                                                                                                                                                               
                                                                                                                                                                                                                          
  ---                                                                                                                                                                                                                     
  3. Data Flow Diagram                                                                                                                                                                                                    
                                                                                                                                                                                                                          
  User: /sc:spawn "implement user auth system" --depth deep
                                                                                                                                                                                                                          
  ┌─────────────────────────────────────────────┐                 
  │  spawn.md (Thin Entry)                      │                                                                                                                                                                         
  │  Parse flags → Skill sc:spawn-protocol      │                                                                                                                                                                         
  └──────────────────┬──────────────────────────┘                                                                                                                                                                         
                     │                                                                                                                                                                                                    
  ┌──────────────────▼──────────────────────────┐                                                                                                                                                                         
  │  SKILL.md — Wave 0: Prerequisites           │                                                                                                                                                                         
  │  ├─ Validate input (STOP if missing)        │                                                                                                                                                                         
  │  ├─ Parse flags                             │                                                                                                                                                                         
  │  ├─ Auggie Query 1 (task-specific) ─┐       │                                                                                                                                                                         
  │  └─ Auggie Query 2 (architecture)  ─┤parallel│                                                                                                                                                                        
  │                                      │       │                                                                                                                                                                        
  │  Checkpoint → Serena memory                  │                                                                                                                                                                        
  └──────────────────┬──────────────────────────┘                                                                                                                                                                         
                     │                                                                                                                                                                                                    
  ┌──────────────────▼──────────────────────────┐                                                                                                                                                                         
  │  SKILL.md — Wave 1: Scope Analysis          │                                                                                                                                                                         
  │  ├─ Domain detection                        │                 
  │  ├─ [If deep/complex] Task: spawn-planner   │                                                                                                                                                                         
  │  │   └─ Returns: domain_map, dep_graph,     │                                                                                                                                                                         
  │  │                complexity_score           │                                                                                                                                                                        
  │  ├─ Module mapping (Serena find_symbol)      │                                                                                                                                                                        
  │  └─ Dependency detection (find_referencing)  │                                                                                                                                                                        
  │                                              │                                                                                                                                                                        
  │  Checkpoint → Serena memory                  │                                                                                                                                                                        
  └──────────────────┬──────────────────────────┘                                                                                                                                                                         
                     │                                            
  ┌──────────────────▼──────────────────────────┐                                                                                                                                                                         
  │  SKILL.md — Wave 2: Decomposition           │                                                                                                                                                                         
  │  Load: refs/decomposition-patterns.md       │                                                                                                                                                                         
  │  ├─ Epic construction (1 per domain)        │                                                                                                                                                                         
  │  ├─ Story decomposition (by depth)          │                                                                                                                                                                         
  │  ├─ Task→Command mapping                    │                                                                                                                                                                         
  │  └─ DAG construction (parallel groups)      │                                                                                                                                                                         
  │      [If deps > 5] Sequential MCP reasoning │                                                                                                                                                                         
  │                                              │                                                                                                                                                                        
  │  Checkpoint → Serena memory                  │                
  └──────────────────┬──────────────────────────┘                                                                                                                                                                         
                     │                                                                                                                                                                                                    
         ┌───────────┼───────────┐                                                                                                                                                                                        
         │ --dry-run  │ default   │ --no-delegate                                                                                                                                                                         
         ▼           ▼           ▼                                                                                                                                                                                        
      Output      Active       TaskCreate                                                                                                                                                                                 
      hierarchy   delegation   only + output                                                                                                                                                                              
      + STOP      continues    hierarchy                                                                                                                                                                                  
                     │                                            
  ┌──────────────────▼──────────────────────────┐                                                                                                                                                                         
  │  SKILL.md — Wave 3: Delegation              │                 
  │  Load: refs/delegation-matrix.md            │                                                                                                                                                                         
  │  Load: refs/prompt-construction.md          │                                                                                                                                                                         
  │  ├─ TaskCreate for each task                │                                                                                                                                                                         
  │  ├─ Prompt enrichment (Rules 1-3)           │                                                                                                                                                                         
  │  ├─ [If tasks > 8] Task: spawn-orchestrator │                                                                                                                                                                         
  │  │   └─ Handles dispatch + tracking         │                                                                                                                                                                         
  │  ├─ [If tasks ≤ 8] Direct dispatch:         │                                                                                                                                                                         
  │  │   ├─ Parallel Group 1 → [Task, Task]     │                                                                                                                                                                         
  │  │   ├─ Wait for completion                 │                                                                                                                                                                         
  │  │   ├─ Parallel Group 2 → [Task, Task]     │                                                                                                                                                                         
  │  │   └─ ...                                 │                                                                                                                                                                         
  │  └─ Result aggregation + return contract    │                                                                                                                                                                         
  └─────────────────────────────────────────────┘                                                                                                                                                                         
                                                                                                                                                                                                                          
  4. Framework Registration Changes                               
                                                                                                                                                                                                                          
  These files need updates (not designed here — noted for implementation):                                                                                                                                                
  
  ┌─────────────────┬─────────────────────────────────────────────────────────────────────┐                                                                                                                               
  │      File       │                               Change                                │
  ├─────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ COMMANDS.md     │ Add/update spawn entry with new MCP servers, personas, tools        │
  ├─────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ ORCHESTRATOR.md │ Update routing table entry for spawn with new complexity/confidence │                                                                                                                               
  ├─────────────────┼─────────────────────────────────────────────────────────────────────┤                                                                                                                               
  │ FLAGS.md        │ Add --no-delegate, --dry-run, --resume flag definitions             │                                                                                                                               
  └─────────────────┴─────────────────────────────────────────────────────────────────────┘                                                                                                                               
                                                                  
  5. Migration Checklist                                                                                                                                                                                                  
                                                                  
  - Create src/superclaude/skills/sc-spawn-protocol/SKILL.md                                                                                                                                                              
  - Create src/superclaude/skills/sc-spawn-protocol/refs/decomposition-patterns.md
  - Create src/superclaude/skills/sc-spawn-protocol/refs/delegation-matrix.md                                                                                                                                             
  - Create src/superclaude/skills/sc-spawn-protocol/refs/prompt-construction.md                                                                                                                                           
  - Create src/superclaude/agents/spawn-orchestrator.md
  - Create src/superclaude/agents/spawn-planner.md                                                                                                                                                                        
  - Rewrite src/superclaude/commands/spawn.md as thin entry                                                                                                                                                               
  - Remove all TodoWrite references (replace with Task tool family)                                                                                                                                                       
  - Update COMMANDS.md, ORCHESTRATOR.md, FLAGS.md                                                                                                                                                                         
  - make sync-dev && make verify-sync                                                                                                                                                                                     
  - Manual validation: invoke /sc:spawn "test task" --dry-run      