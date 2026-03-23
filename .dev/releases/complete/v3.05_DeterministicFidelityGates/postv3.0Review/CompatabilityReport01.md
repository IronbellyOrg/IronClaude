  v3.05 Compatibility Audit — Consolidated Report

  Executive Summary

  The v3.05 spec (Deterministic Fidelity Gates) is architecturally stale — it was written before v3.0 shipped. v3.0 pre-implemented ~60% of the v3.05 infrastructure. The spec must be
  rewritten from "greenfield build" to "extend existing code."

  By the numbers:
  - 16 spec requirements already fully satisfied (zero work needed)
  - 3 HIGH conflict files where spec says CREATE but code already exists
  - 4 modifications needed on existing code (threshold, rollback, orchestrators)
  - 2 genuinely new modules to build (spec_parser.py, structural_checkers.py)
  - 1 dead code file to remove (fidelity.py)

  ---
  1. Module Existence Conflicts (CRITICAL)

  ┌────────────────────────┬────────────┬────────────────────────────────────┬───────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
  │         Module         │ Spec Says  │              Reality               │ Lines │                                          Resolution                                          │
  ├────────────────────────┼────────────┼────────────────────────────────────┼───────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
  │ convergence.py         │ CREATE new │ Already exists (v3.0)              │ 323   │ Reclassify → MODIFY. Extend with execute_fidelity_with_convergence() and handle_regression() │
  ├────────────────────────┼────────────┼────────────────────────────────────┼───────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
  │ semantic_layer.py      │ CREATE new │ Already exists (v3.0)              │ 336   │ Reclassify → MODIFY. Add validate_semantic_high() and run_semantic_layer() orchestrators     │
  ├────────────────────────┼────────────┼────────────────────────────────────┼───────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
  │ remediate_executor.py  │ CREATE new │ Already exists (v3.0)              │ 563   │ Reclassify → MODIFY. Add MorphLLM patch format, change threshold 50→30, per-file rollback    │
  ├────────────────────────┼────────────┼────────────────────────────────────┼───────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
  │ deviation_registry.py  │ CREATE new │ Class exists inside convergence.py │ —     │ Either extract to own file or update spec to accept current location                         │
  ├────────────────────────┼────────────┼────────────────────────────────────┼───────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
  │ spec_parser.py         │ CREATE new │ Does not exist                     │ —     │ Safe to create                                                                               │
  ├────────────────────────┼────────────┼────────────────────────────────────┼───────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
  │ structural_checkers.py │ CREATE new │ Does not exist                     │ —     │ Safe to create                                                                               │
  └────────────────────────┴────────────┴────────────────────────────────────┴───────┴──────────────────────────────────────────────────────────────────────────────────────────────┘

  2. Already-Implemented Spec Requirements (No Work Needed)

  ┌──────────────────────────────────────────────────────────────┬──────────────────────────────┬────────┐
  │                         Requirement                          │           Location           │ Status │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ ACTIVE in VALID_FINDING_STATUSES (FR-6/BF-1)                 │ models.py:16                 │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ Finding.source_layer field (FR-6/BF-3)                       │ models.py:44                 │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ RoadmapConfig.convergence_enabled (FR-7)                     │ models.py:107                │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ RoadmapConfig.allow_regeneration (FR-9.1)                    │ models.py:108                │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ --allow-regeneration CLI flag                                │ commands.py:89-94            │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ WIRING_GATE registered in ALL_GATES                          │ gates.py:944                 │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ SPEC_FIDELITY_GATE conditional bypass                        │ executor.py:521              │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ DeviationRegistry full lifecycle (load/save/merge)           │ convergence.py:50-225        │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ compute_stable_id()                                          │ convergence.py:24-32         │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ ConvergenceResult dataclass                                  │ convergence.py:228-237       │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ _check_regression() structural-only (BF-3)                   │ convergence.py:240-272       │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ Temp dir isolation + atexit cleanup (FR-8)                   │ convergence.py:278-323       │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ All prompt budget constants (FR-4.2)                         │ semantic_layer.py constants  │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ build_semantic_prompt() with budget enforcement              │ semantic_layer.py            │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ Debate scoring (RubricScores, score_argument, judge_verdict) │ semantic_layer.py            │ Done   │
  ├──────────────────────────────────────────────────────────────┼──────────────────────────────┼────────┤
  │ Snapshot create/restore/cleanup                              │ remediate_executor.py:53-101 │ Done   │
  └──────────────────────────────────────────────────────────────┴──────────────────────────────┴────────┘

  3. Modifications Needed on Existing Code                                                                                                                                                   
   
  ┌───────────────────────┬──────────────────────┬─────────────────────┬───────────────────────┐                                                                                             
  │         What          │       Current        │    Spec Requires    │         File          │
  ├───────────────────────┼──────────────────────┼─────────────────────┼───────────────────────┤                                                                                             
  │ Diff-size threshold   │ 50%                  │ 30%                 │ remediate_executor.py │
  ├───────────────────────┼──────────────────────┼─────────────────────┼───────────────────────┤
  │ Diff-size granularity │ Per-file             │ Per-patch           │ remediate_executor.py │                                                                                             
  ├───────────────────────┼──────────────────────┼─────────────────────┼───────────────────────┤                                                                                             
  │ Rollback scope        │ All-or-nothing       │ Per-file            │ remediate_executor.py │                                                                                             
  ├───────────────────────┼──────────────────────┼─────────────────────┼───────────────────────┤                                                                                             
  │ TRUNCATION_MARKER     │ Missing heading name │ Include '<heading>' │ semantic_layer.py     │
  └───────────────────────┴──────────────────────┴─────────────────────┴───────────────────────┘                                                                                             
   
  4. Genuinely New Code to Build                                                                                                                                                             
                                                                  
  ┌───────────────────────────────────────────────────────────────┬──────────┬───────────────────────────────────────────────────────────────┐                                               
  │                           Component                           │ Spec Ref │                          Description                          │
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤                                               
  │ spec_parser.py                                                │ FR-2     │ Spec & roadmap structural data extraction                     │
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤
  │ structural_checkers.py                                        │ FR-1     │ 5 deterministic dimension checkers (no LLM)                   │                                               
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤                                               
  │ validate_semantic_high()                                      │ FR-4.1   │ Orchestrator: parallel prosecutor/defender via ClaudeProcess  │                                               
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤                                               
  │ run_semantic_layer()                                          │ FR-4     │ Top-level semantic layer entry point                          │
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤                                               
  │ execute_fidelity_with_convergence()                           │ FR-7     │ 3-run convergence loop orchestrator                           │
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤                                               
  │ handle_regression()                                           │ FR-8     │ Full regression flow (spawn agents, validate, debate, update) │
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤                                               
  │ RemediationPatch dataclass                                    │ FR-9     │ MorphLLM lazy edit snippet model                              │
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤                                               
  │ apply_patches()                                               │ FR-9     │ Sequential per-file, per-patch diff guard                     │
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤                                               
  │ fallback_apply()                                              │ FR-9     │ Deterministic text replacement (anchor matching)              │
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤                                               
  │ check_morphllm_available()                                    │ FR-9     │ MCP runtime probe                                             │
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤                                               
  │ roadmap_run_step() convergence branch                         │ FR-7     │ Bypass Claude subprocess, delegate to convergence engine      │
  ├───────────────────────────────────────────────────────────────┼──────────┼───────────────────────────────────────────────────────────────┤                                               
  │ Finding fields: rule_id, spec_quote, roadmap_quote, stable_id │ FR-6     │ Extend dataclass in models.py                                 │
  └───────────────────────────────────────────────────────────────┴──────────┴───────────────────────────────────────────────────────────────┘                                               
                                                                  
  5. Dead Code                                                                                                                                                                               
                                                                  
  ┌────────────────────────────┬──────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐          
  │            File            │     Verdict      │                                                           Rationale                                                           │
  ├────────────────────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤          
  │ fidelity.py (66 lines)     │ DEAD — remove    │ Zero production imports. Severity enum and FidelityDeviation dataclass never wired. Superseded by Finding + DeviationRegistry │
  ├────────────────────────────┼──────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ convergence.py:RunMetadata │ Dead within file │ Dataclass exists but begin_run() uses raw dicts, never instantiates it                                                        │          
  └────────────────────────────┴──────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘          
                                                                                                                                                                                             
  6. Files That Must Be Kept (Not Dead)                                                                                                                                                      
                                                                  
  ┌─────────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐            
  │                  File                   │                                                                Why                                                                │
  ├─────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ spec_patch.py                           │ Active call sites in executor.py and commands.py. Handles spec-hash reconciliation, NOT remediation patches. No overlap with FR-9 │
  ├─────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ prompts.py:build_spec_fidelity_prompt() │ Used in legacy mode (convergence_enabled=false). Still generates human-readable report even in convergence mode                   │            
  └─────────────────────────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘            
                                                                                                                                                                                             
  7. Architectural Tensions                                                                                                                                                                  
                                                                  
  7a. Convergence Loop vs Linear Pipeline                                                                                                                                                    
                                                                  
  The pipeline is single-pass. v3.05's convergence engine needs up to 3 runs within step 8. The loop must be self-contained — not re-running the full pipeline. Pattern exists:              
  wiring-verification bypass (executor.py:244-259).               
                                                                                                                                                                                             
  7b. Remediation Ownership                                                                                                                                                                  
   
  Current remediation is post-pipeline. v3.05 needs remediation within the convergence loop (between runs). Tension with _check_remediation_budget() and _print_terminal_halt() which assume 
  remediation is external.                                        
                                                                                                                                                                                             
  7c. SPEC_FIDELITY_GATE + Wiring Step Ordering                                                                                                                                              
   
  v3.0 places wiring-verification after spec-fidelity, assuming spec-fidelity always runs. When convergence_enabled=true, spec-fidelity gate is None. Wiring step still works (no dependency 
  on spec-fidelity output), but step ordering semantics need documenting.
                                                                                                                                                                                             
  8. Spec Rewrite Requirements                                                                                                                                                               
   
  The v3.05 spec needs these corrections before implementation:                                                                                                                              
                                                                  
  1. Reclassify convergence.py, semantic_layer.py, remediate_executor.py from "New Modules" to "Modified Modules"                                                                            
  2. Remove deviation_registry.py from new modules list (or add extraction task from convergence.py)
  3. Document the 16 already-implemented requirements as "pre-implemented by v3.0"                                                                                                           
  4. Add Finding field extensions (rule_id, spec_quote, roadmap_quote, stable_id) to models.py modification list                                                                             
  5. Update architecture Sec 2.1 module map to reflect actual file locations                                                                                                                 
  6. Add --convergence-enabled CLI flag decision (config field exists, no CLI exposure)                                                                                                      
  7. Document wiring step interaction when convergence mode is active                 