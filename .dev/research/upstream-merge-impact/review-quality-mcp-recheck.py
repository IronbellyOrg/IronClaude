"""Retain independent correction recheck evidence without replacing the first audit."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

os.environ['GIT_OPTIONAL_LOCKS']='0'
out=Path('.dev/research/upstream-merge-impact')
text=(out/'mcp-installation.md').read_text()
rename=subprocess.check_output(['git','diff','--summary','ab0bb0f5^','ab0bb0f5','--','docs/User-Guide/mcp-installation.md','docs/user-guide/mcp-installation.md'],text=True)
unchanged=subprocess.run(['git','diff','--exit-code','HEAD','--','src/superclaude/cli/install_mcp.py','src/superclaude/mcp/MCP_Airis-Agent.md','src/superclaude/mcp/MCP_Mindbase.md','CLAUDE.md','docs/user-guide/mcp-installation.md'],capture_output=True)
result={
 'snapshot':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 'revised_report_sha256':hashlib.sha256(text.encode()).hexdigest(),
 'no_placeholders':'{{RF_PLACEHOLDER:' not in text,
 'manual_automatic_distinction':'does not contradict those separate manual-deployment guides' in text,
 'manual_service_availability_unverified':'Actual service availability in the external manual deployment' in text,
 'mismatch_anchored_repository_instructions':'repository `CLAUDE.md:353-368` directly recommends' in text,
 'december_manual_guidance_kept':'**keep** manual guidance, deprecation and transport corrections' in text,
 'january_instruction_partial':'**partial**: keep supported gateway implementation; correct current repository instructions only' in text,
 'exact_rename_described':'Historical source endpoint renamed 100%' in text,
 'obsolete_duplicate_description_absent':'Uppercase duplicate documentation removed' not in text,
 'all_nine_records_named':all(sha in text for sha in ['5a685958','67449770','1b14d065','202660b5','6ae5e998','04c9b85c','3294a0ad','55c658c7','0ceb2955']),
 'rename_summary':rename.strip(),
 'primary_sources_unchanged':unchanged.returncode==0,
}
assert all(result[key] for key in result if isinstance(result[key],bool))
assert '(100%)' in rename
(out/'review-quality-mcp-recheck.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
