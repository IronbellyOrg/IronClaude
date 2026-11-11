"""Deterministic package assertions, not another specification review."""
from pathlib import Path
import collections
import difflib
import hashlib
import json
import math
import re
import sys

HERE=Path(__file__).resolve().parent
OUT=HERE.parent
ROOT=HERE.parents[5]
checks=[]
def check(name, condition):
    checks.append({'check':name,'passed':bool(condition)})

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

m=json.loads((OUT/'metrics.json').read_text())
manifest=json.loads((HERE/'sources.json').read_text())
sessions=json.loads((HERE/'session-metrics.json').read_text())
recount=json.loads((HERE/'report-recount.json').read_text())
check('four required outputs exist',all((OUT/n).exists() for n in ['metrics.json','validity.md','comparison.md','reviews']))
check('all preserved source-copy hashes match captured manifest',all(digest(HERE/e['copy'])==e['sha256'] for e in manifest))
critical=[e for e in manifest if '/.dev/orca-command-refactor/' in e['source']]
check('all loop/frozen sources remain byte-identical to preserved copies',all(digest(Path(e['source']))==e['sha256'] for e in critical))
check('manifest source pointers exist',all(Path(e['source']).exists() for e in manifest))
check('all session pointers exist',all(Path(s['source']).exists() for s in sessions.values()))
for i,version in enumerate(['spec-v1-draft.md','spec-v2-after-round1.md','spec-v3-after-round2.md'],1):
    a=(HERE/version).read_bytes()
    check(f'frozen version {i} matches loop document',a==(HERE/f'diffgate-loop/doc-r{i}.md').read_bytes())
    check(f'frozen version {i} newline count',a.count(b'\n')==285)
for n,(r,counted) in enumerate(zip(m['rounds'],recount),1):
    c=collections.Counter(x['severity'] for x in counted['records'])
    check(f'round {n} numbered-new severity count',r['M2']['findings_total']==sum(c.values()) and r['M2']['critical_plus_major']==c['critical']+c['major'] and r['M2']['minor']==c['minor'])
    result=json.loads((HERE/f'diffgate-loop/result-r{n}.json').read_text())
    check(f'round {n} unresolved-prior separation',r['M2']['unresolved_priors_total']==len(counted['unresolved_priors']))
    check(f'round {n} open blocker count',r['script']['confirmed_blockers']==r['M2']['endpoint_open_critical_plus_major']==result['blocking'])
    check(f'round {n} script proxy_all separate from all findings',r['script']['proxy_all']==result['proxy_all'] and r['M2']['findings_total']!=result['proxy_all'])
    name=['spec-panel.md','spec-panel-round2.md','spec-panel-round3.md'][n-1]
    checked=(HERE/f'diffgate-loop/report-r{n}.md').read_bytes()
    closed=(HERE/f'diffgate-loop/close-r{n}.md').read_bytes()
    final=(HERE/name).read_bytes()
    check(f'round {n} final equals checked snapshot plus coordinator closing block',final==checked+b'\n'+closed)
    check(f'round {n} retains final FAIL',final.decode().strip().endswith('verdict: FAIL'))
    check(f'round {n} actual Skill invocation and loaded body',any(s['input']['skill']=='sc:spec-panel-diffgate' for s in sessions[f'R{n}-review']['skill_calls']) and sessions[f'R{n}-review']['loaded_command_evidence'][0]['body_found_verbatim'])
    for kind in ['review','revise']:
        key=f'R{n}-{kind}'
        if key not in sessions: continue
        a=r['M5'][kind+'_session']; b=sessions[key]
        check(f'{key} tools and all token classes',all(a[t]==b[t] for t in ['tool_calls','output_tokens','input_tokens_uncached','cache_creation_tokens','cache_read_tokens']))
        check(f'{key} fresh distinct Opus window',b['models']==['claude-opus-5-5'] and b['agent_calls']==[])
    if n>1:
        before=(HERE/f'diffgate-loop/doc-r{n-1}.md').read_text().splitlines()
        after=(HERE/f'diffgate-loop/doc-r{n}.md').read_text().splitlines()
        changed=set()
        for tag,a,b,c,d in difflib.SequenceMatcher(None,before,after,autojunk=False).get_opcodes():
            if tag!='equal': changed.update(range(c+1,d+1))
        anchors=[int(re.search(r' at=(\d+)',x['text'])[1]) for x in counted['records']]
        scope=r['M3']['scope_anchor_counts']
        check(f'round {n} changed-line containment independently re-derived',sum(a in changed for a in anchors)==scope['inside_changed_lines'])
for i in range(2):
    r=m['rounds'][i]; a=r['M4']['bytes_at_review_start']; b=r['M4']['bytes_after_revise']
    check(f'fix cycle {i+1} exact growth arithmetic',math.isclose(r['M4']['growth_percent_this_round'],100*(b-a)/a,abs_tol=1e-10))
g=m['growth_summary']; growth=(g['after_cycle_2_endpoint_bytes']-g['start_bytes'])/g['start_bytes']*100
check('exact cumulative byte growth',math.isclose(growth,g['after_two_fix_cycles_percent'],abs_tol=1e-10))
a=m['independent_audit']
check('independent audit is four unique blocking MAJOR findings',len(re.findall(r'^#### [1-4]\. ',(HERE/'blindness-audit-frozen.md').read_text(),re.M))==a['findings_total']==a['blocking']==a['major']==4)
check('audit union arithmetic and explicit bounds',a['deduplicated_union']==a['endpoint_loop_blockers']+a['findings_total']-a['deduplicated_overlap']==6 and a['union_lower_bound']==a['union_upper_bound']==6)
check('owner cumulative addition zero is kept separate',m['deferred_demoted_withdrawn']['cumulative_distinct_critical_plus_major']==0 and all(r['script']['deferred']==r['script']['demoted']==r['script']['withdrawn']==0 for r in m['rounds']))
for name in ['ctl-r1','ctl-r2','flg-r1','flg-r2']:
    c=json.loads((HERE/f'comparators/{name}-metrics.json').read_text())
    check(f'{name} comparator values unchanged',m['comparators'][name]['critical_plus_major']==[r['M2']['critical_plus_major'] for r in c['rounds']] and m['comparators'][name]['findings_total']==[r['M2']['findings_total'] for r in c['rounds']])
f=m['comparators']['fixed_thresholds']; ar=m['comparators']['arithmetic']
check('fixed control arithmetic',f['control_mean_R3_proxy']==(8+4)/2 and f['growth_limit_percent']==round(f['control_mean_growth_percent']*.7,3) and f['arm_B_mean_R3_proxy']==(6+1)/2)
check('comparison arithmetic in metrics',math.isclose(ar['growth_below_limit_pp'],f['growth_limit_percent']-growth,abs_tol=1e-9) and math.isclose(ar['growth_reduction_percent'],100*(f['control_mean_growth_percent']-growth)/f['control_mean_growth_percent'],abs_tol=1e-9))
check('loop total accounting',m['session_accounting']['loop']['tool_calls']==sum(r['M5']['round_total']['tool_calls'] for r in m['rounds']) and m['session_accounting']['loop']['output_tokens']==sum(r['M5']['round_total']['output_tokens'] for r in m['rounds']))
check('all delivered briefs match saved source and logged root substitution',all(s['brief']['equals_source_after_root_substitution'] for s in sessions.values()))
if '--allow-pending' not in sys.argv:
    check('no report placeholders',all('RF_PLACEHOLDER' not in (OUT/n).read_text() for n in ['metrics.json','validity.md','comparison.md']))
    check('binary package verdict at end', (OUT/'comparison.md').read_text().strip().endswith('**PASS** (evidence-package quality only, not variant success or experimental-validity approval).'))
failed=[c['check'] for c in checks if not c['passed']]
result={'status':'PASS' if not failed else 'FAIL','checks':checks,'failed':failed,'scope':'Deterministic package consistency checks, not a new live-model review or implementation test.'}
(HERE/'package-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks),'failed':failed},indent=2))
raise SystemExit(bool(failed))
