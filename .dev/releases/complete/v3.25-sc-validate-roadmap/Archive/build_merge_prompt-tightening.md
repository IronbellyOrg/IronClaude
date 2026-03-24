  Proposed build_merge_prompt() tightening steps                                
                                                                  
  Do not implement yet.
                                                                                
  Prompt changes to add
                                                                                
  1. Add an explicit canonical output instruction near the top:   
    - “Your final deliverable is the text printed in your final assistant
  response.”                                                                    
    - “Do not create files for the final report.”
  2. Add an explicit prohibition:                                               
    - “Do NOT use Write, Edit, or any file-creation tool to produce the         
  validation report.”                                                           
  3. Add a completion rule:                                                     
    - “The task is not complete until the full report appears in your final     
  assistant text output.”                                                       
  4. Reinforce frontmatter position:                                            
    - “Your final assistant response must begin immediately with YAML           
  frontmatter.”                                                                 
  5. Reinforce no trailing tool-only completion:                                
    - “Do not end your work on a tool call. End with the full final report as   
  plain text.”                                                                  
  6. Add canonical artifact wording:                                            
    - “The canonical validation artifact is the final emitted report text, not  
  any side-effect file.”                                                        
  7. Keep the existing format contract, but make it final-message specific:     
    - agreement table                                                           
    - consolidated findings                                                     
    - summary                                                                   
    - required frontmatter fields      