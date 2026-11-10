"""Reproducible recorder extraction. Reads sources; writes only beside this file."""
import collections
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[5]
SOURCE = ROOT / '.dev/orca-command-refactor'
BASE = Path('/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation')
PJ = Path('/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-exp346-v-diffgate')
TMP = Path('/tmp/impl/s1v')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2) + '\n')

def stamp(s):
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))

expected = ['d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d', '6c68d0ece899759096d1d8e35226720deeb59e96e771d6f47232364e4a628d17', '75a628e35b00eb23bde80d0190f6cf735f3b298c8f3b228caf05f65ee094ac9a']
versions = ['spec-v1-draft.md', 'spec-v2-after-round1.md', 'spec-v3-after-round2.md']
for n, h in zip(versions, expected):
    assert sha(SOURCE / 'specs/history' / n) == h, n

manifest = []
def copy(p, name):
    dest = OUT / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dest)
    assert sha(dest) == sha(p)
    manifest.append({'source': str(p), 'copy': name, 'sha256': sha(p), 'bytes': p.stat().st_size, 'lines': p.read_bytes().count(b'\n'), 'source_mtime_utc': dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc).isoformat()})

for name in ['spec-panel.md', 'spec-panel-round2.md', 'spec-panel-round3.md', 'disposition.md', 'disposition-round2.md', 'blindness-audit-frozen.md', 'blindness-audit.md']:
    copy(SOURCE / 'review' / name, name)
for name in versions:
    copy(SOURCE / 'specs/history' / name, name)
copy(SOURCE / 'specs/history/spec-v3-after-round2.md', 'spec-final-frozen.md')
for p in sorted((SOURCE / 'review/diffgate-loop').iterdir()):
    if p.is_file():
        copy(p, 'diffgate-loop/' + p.name)
for name in ['T05-R1-reviewer.txt', 'T06-R1-reviser.txt', 'T07-R2-reviewer.filled.txt', 'T08-R2-reviser.filled.txt', 'T09-R3-reviewer.filled.txt', 'T11-blindness-audit.txt', 'T11-frozen-audit.txt']:
    copy(TMP / 'briefs/diffgate' / name, 'briefs/' + name)
copy(Path('/tmp/impl/exp/spec-recorder3.txt'), 'governing-template.txt')
for path in ['DECISIONS.md', 'phase2/S1/REPLAY.md', 'phase2/S1/baseline-metrics.json', 'phase5/s1v-log.md', 'phase5/install-log.md', 'phase4/install-watch.log']:
    copy(BASE / path, 'provenance/' + path)
copy(TMP / 'dg.sh', 'provenance/dg.sh')
save('sources.json', manifest)
(OUT / 'SHA256SUMS').write_text(''.join(f"{m['sha256']}  {m['copy']}\n" for m in manifest))
(OUT / 'sizes.txt').write_text('lines bytes copy\n' + ''.join(f"{m['lines']} {m['bytes']} {m['copy']}\n" for m in manifest))

steps = [
 ('R1-review','0e40ed15-dbb8-4e40-a1be-b66c11092ca3','task_13951bf9c994','ctx_bd531e8de74c','T05-R1-reviewer.txt'),
 ('R1-revise','3b1f3d8e-7043-4f34-bca9-bb84411c4687','task_1e91e91a298a','ctx_4c990b0ce43a','T06-R1-reviser.txt'),
 ('R2-review','ba3e4a04-d331-47b7-b73c-02f7d972fca2','task_85fee554b945','ctx_a260ae0a556b','T07-R2-reviewer.filled.txt'),
 ('R2-revise','efdd7e2a-ba9c-4bf8-81b7-56268fc538d2','task_b0537130e666','ctx_e07b01555683','T08-R2-reviser.filled.txt'),
 ('R3-review','816a3832-d65a-462c-9c98-580c6c2177d2','task_3f014eb4ecc8','ctx_0290dab9c753','T09-R3-reviewer.filled.txt'),
 ('retired-audit','f7f8a82c-03c5-416a-92e9-2219db4ef5d3','task_98f502fbd638','ctx_bc6d2dd56116','T11-blindness-audit.txt'),
 ('frozen-audit','4ea38812-79e0-439d-9b9c-e1b846bddae4','task_02f7207bc676','ctx_11b8559abe85','T11-frozen-audit.txt')]
exposure = re.compile(r'origin/master|WORKER-CONTRACT\.md|(?:commands/|sc:)(?:graph|impact|issue)(?:\.md|\b)', re.I)
sessions = {}
for step, sid, task, dispatch, brief in steps:
    p = PJ / (sid + '.jsonl')
    rows = [(i,json.loads(s)) for i,s in enumerate(p.open(),1)]
    tools = []
    for i,r in rows:
        if r.get('type') == 'assistant':
            for c in r.get('message',{}).get('content',[]):
                if isinstance(c,dict) and c.get('type') == 'tool_use':
                    tools.append((i,r.get('timestamp'),c))
    done = [(i,t,c) for i,t,c in tools if c['name']=='Bash' and '--type worker_done' in c.get('input',{}).get('command','') and task in c['input']['command'] and dispatch in c['input']['command']]
    assert len(done)==1, (step, len(done))
    endline,endts,_ = done[0]
    # Primary metrics end at matching worker_done invocation; complete-session totals separately.
    def account(limit):
        a = [r for i,r in rows if i<=limit and r.get('type')=='assistant']
        last = {r.get('message',{}).get('id'):r for r in a}
        tc = [c for i,t,c in tools if i<=limit]
        keys = {'output_tokens':'output_tokens','input_tokens_uncached':'input_tokens','cache_creation_tokens':'cache_creation_input_tokens','cache_read_tokens':'cache_read_input_tokens'}
        sums = {k:sum((r.get('message',{}).get('usage') or {}).get(v,0) or 0 for r in last.values()) for k,v in keys.items()}
        times = [r['timestamp'] for i,r in rows if i<=limit and r.get('timestamp')]
        return dict(tool_calls=len(tc), unique_tool_call_ids=len({c['id'] for c in tc}), assistant_turns=len(last), **sums, first_ts=min(times), last_ts=max(times), wall_minutes=(stamp(max(times))-stamp(min(times))).total_seconds()/60)
    a = account(endline)
    a.update(session=sid,task=task,dispatch=dispatch,source=str(p),end_line=endline,worker_done_ts=endts,whole_session=account(len(rows)))
    scoped = [(i,t,c) for i,t,c in tools if i<=endline]
    a['models'] = sorted({r['message'].get('model') for i,r in rows if i<=endline and r.get('type')=='assistant' and r['message'].get('model')!='<synthetic>'})
    a['versions'] = sorted({r['version'] for i,r in rows if i<=endline and r.get('version')})
    a['skill_calls'] = [{'line':i,'time':t,'input':c['input']} for i,t,c in scoped if c['name']=='Skill']
    a['agent_calls'] = [{'line':i,'time':t,'type':c['input'].get('subagent_type'),'description':c['input'].get('description')} for i,t,c in scoped if c['name']=='Agent']
    hits = []
    for i,t,c in scoped:
        inp = c.get('input',{})
        # Search only tool arguments, never tool results containing quoted old claims.
        if c['name'] in ['Read','Grep','Glob','Bash'] and exposure.search(json.dumps(inp)):
            hits.append({'line':i,'timestamp':t,'tool':c['name'],'input':inp})
    a['answer_key_tool_hits'] = hits
    a['command_reads'] = [{'line':i,'time':t,'tool':c['name'],'input':c['input']} for i,t,c in scoped if c['name'] in ['Read','Bash','Grep'] and re.search(r'(?:commands/(?:sc/)?spec-panel[^ /"\\]*\.md)',json.dumps(c['input']))]
    firstuser = next((i,r) for i,r in rows if r.get('type')=='user' and isinstance(r.get('message',{}).get('content'),str))
    text = firstuser[1]['message']['content']
    tasktext = text.split('=== TASK ===',1)[1].split('</pasted_content',1)[0].strip()
    originalbrief = (TMP / 'briefs/diffgate' / brief).read_text()
    origroot='/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs'
    expectedbrief=originalbrief.replace(origroot,str(ROOT)).strip()
    (OUT / 'briefs' / (step+'-delivered.txt')).write_text(tasktext+'\n')
    a['brief']={'source':str(TMP/'briefs/diffgate'/brief),'source_sha256':sha(TMP/'briefs/diffgate'/brief),'delivered_sha256':hashlib.sha256((tasktext+'\n').encode()).hexdigest(),'first_user_line':firstuser[0],'equals_source_after_root_substitution':tasktext==expectedbrief,'root_substitutions':originalbrief.count(origroot)}
    # The log need not contain an entire harness prompt. Report observed strings only.
    attached = [(i,json.dumps(r)) for i,r in rows if i<=endline and r.get('type') in ['attachment','system']]
    a['instruction_evidence']={s:[i for i,v in attached if s.lower() in v.lower()] for s in ['minor findings never fail','at most 2 fix cycles','3 reviews','blocking/minor']}
    a['later_user_messages']=[{'line':i,'timestamp':r.get('timestamp'),'text':r['message']['content'][:1600]} for i,r in rows if i>endline and r.get('type')=='user' and isinstance(r.get('message',{}).get('content'),str)]
    a['error_records']=[{'line':i,'timestamp':r.get('timestamp'),'excerpt':json.dumps(r)[:1600]} for i,r in rows if i<=endline and (r.get('isApiErrorMessage') or r.get('type')=='system' and re.search(r'429|rate.limit|cooldown',json.dumps(r),re.I))]
    a['explicit_user_resumes']=[{'line':i,'timestamp':r.get('timestamp'),'text':r['message']['content'][:600]} for i,r in rows if i<=endline and r.get('type')=='user' and isinstance(r.get('message',{}).get('content'),str) and ('Resume the same assigned' in r['message']['content'] or r['message']['content']=='resume')]
    # Bound evidence snippets to relevant messages; source itself remains read-only.
    save(step+'-session.json',a)
    sessions[step]=a
save('session-metrics.json',sessions)

# Per-finding recount is made from report text, not machine totals.
parsed=[]
for n,name in enumerate(['spec-panel.md','spec-panel-round2.md','spec-panel-round3.md'],1):
    lines=(OUT/name).read_text().splitlines()
    records=[]
    for i,line in enumerate(lines,1):
        m=re.match(r'FINDING (\S+) sev=(critical|major|minor)\b',line)
        if m:
            records.append({'id':m[1],'severity':m[2],'line':i,'text':line})
    table=[line for line in lines if re.match(r'\| \d+ \(R\d+\.\d+\)',line)]
    assert len(table)==len(records), (n,len(table),len(records))
    for rec,row in zip(records,table):
        assert rec['id'] in row and rec['severity'].upper() in row
    priors=[]
    for i,line in enumerate(lines,1):
        m=re.match(r'PRIOR (\S+) (resolved|open|regressed)\b',line)
        if m:
            priors.append({'id':m[1],'status':m[2],'line':i})
    result=json.loads((OUT/f'diffgate-loop/result-r{n}.json').read_text())
    assert [(r['id'],r['severity']) for r in records]==[(r['id'],r['sev']) for r in result['findings']]
    c=collections.Counter(r['severity'] for r in records)
    openprior=[r for r in priors if r['status'] in ['open','regressed']]
    report=lines
    parsed.append({'round':f'R{n}','records':records,'counts':dict(c),'priors':priors,'unresolved_priors':openprior,'script':{k:result.get(k) for k in ['blocking','blocking_ids','proxy_all','proxy_ids','deferred','held','scoped','verdict','halt']},'markers':{'header':[i for i,l in enumerate(report,1) if l==f'review: {n} of 3'],'reviser_heading':[i for i,l in enumerate(report,1) if l=='## Reviser brief'],'reviser_inline':[i for i,l in enumerate(report,1) if l.startswith('Reviser brief:')],'last_nonblank':next(l for l in reversed(report) if l.strip())}})
save('report-recount.json',parsed)

# Preserve runtime instrument bytes and compare loaded bodies without trusting an install narrative.
instruments = {}
for rel in ['commands/sc/spec-panel-diffgate.md','commands/sc/spec-panel-armb.md','commands/sc/spec-panel.md','skills/sc-diffgate/SKILL.md','skills/sc-diffgate/scripts/diffgate.py']:
    p=Path('/home/coder/.claude')/rel
    copy(p,'instruments/'+rel)
    instruments[rel]={'sha256':sha(p),'bytes':p.stat().st_size}
instruments['WORKER-CONTRACT.md']={'sha256':sha(Path('/home/coder/.claude/WORKER-CONTRACT.md')),'present_at_recording':True}
for step,sid,task,dispatch,brief in steps:
    rows=[(i,json.loads(s)) for i,s in enumerate((PJ/(sid+'.jsonl')).open(),1)]
    loaded=[]
    for i,r in rows:
        if i>sessions[step]['end_line'] or r.get('type')!='user':
            continue
        content=r.get('message',{}).get('content')
        if isinstance(content,list):
            for c in content:
                text=c.get('text','') if isinstance(c,dict) else ''
                if text.startswith('# /sc:spec-panel'):
                    cmd='commands/sc/'+('spec-panel-armb.md' if step=='frozen-audit' else 'spec-panel-diffgate.md' if 'spec-panel-diffgate' in text[:100] else 'spec-panel.md')
                    source=(Path('/home/coder/.claude')/cmd).read_text()
                    body=source.split('---',2)[-1].lstrip('\n') if source.startswith('---') else source
                    loaded.append({'line':i,'command':cmd,'sha256':hashlib.sha256(text.encode()).hexdigest(),'chars':len(text),'body_found_verbatim':body.rstrip() in text,'loaded_found_in_current_file':text.rstrip() in source,'first_difference':next(({'tag':tag,'source_excerpt':body[a:b][:150],'loaded_excerpt':text[c:d][:150]} for tag,a,b,c,d in difflib.SequenceMatcher(None,body,text).get_opcodes() if tag!='equal'),None)})
    sessions[step]['loaded_command_evidence']=loaded
save('instrument-hashes.json',instruments)
save('session-metrics.json',sessions)
for k,v in sessions.items():
    save(k+'-session.json',v)
# Baseline-to-dispatched task substitutions, exact token deltas and copied sources.
briefdeltas=[]
for step,sid,task,dispatch,brief in steps[:5]:
    prefix={'R1-review':'T05','R1-revise':'T06','R2-review':'T07','R2-revise':'T08','R3-review':'T09'}[step]
    original=next((BASE/'phase2/S1/briefs/task-text').glob(prefix+'-*.txt'))
    copy(original,'briefs/original-'+original.name)
    a=original.read_text().split(); b=(TMP/'briefs/diffgate'/brief).read_text().split()
    edits=[{'operation':tag,'original':' '.join(a[i:j]),'variant':' '.join(b[k:l])} for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b).get_opcodes() if tag!='equal']
    briefdeltas.append({'step':step,'original_source':str(original),'variant_source':str(TMP/'briefs/diffgate'/brief),'token_deltas':edits})
save('briefs/substitutions.json',briefdeltas)
# Reference metrics are copied, not re-reviewed or re-counted.
comparators={}
for name in ['ctl-r1','ctl-r2','flg-r1','flg-r2']:
    p=Path('/home/coder/workspaces/worktrees/IronClaude')/('exp346-ab-'+name)/'.dev/experiments/346-validation/phase4'/name/'metrics.json'
    copy(p,'comparators/'+name+'-metrics.json')
    obj=json.loads(p.read_text())
    comparators[name]={'source':str(p),'sha256':sha(p),'rounds':[{k:r.get(k) for k in ['round','M2','M3','M4']} for r in obj['rounds']]}
save('comparator-extracts.json',comparators)
# Observed no-progress intervals: error -> next successful real assistant message.
interruptions={}
for step,sid,task,dispatch,brief in steps:
    rows=[(i,json.loads(s)) for i,s in enumerate((PJ/(sid+'.jsonl')).open(),1)]
    spans=[]; start=None
    for i,r in rows:
        if i>sessions[step]['end_line']:
            break
        if r.get('isApiErrorMessage') and start is None:
            start=(i,r['timestamp'])
        elif start and r.get('type')=='assistant' and r.get('message',{}).get('model') not in [None,'<synthetic>']:
            spans.append({'start_line':start[0],'start':start[1],'end_line':i,'end':r['timestamp'],'minutes':(stamp(r['timestamp'])-stamp(start[1])).total_seconds()/60})
            start=None
    interruptions[step]={'observed_error_to_next_response':spans,'minutes':sum(s['minutes'] for s in spans),'work_minutes_after_subtraction':sessions[step]['wall_minutes']-sum(s['minutes'] for s in spans),'note':'Wall-time residual, not CPU or exclusive model work; failed-request waiting before first terminal error is not recoverable.'}
save('interruptions.json',interruptions)
save('sources.json',manifest)
(OUT/'SHA256SUMS').write_text(''.join(f"{m['sha256']}  {m['copy']}\n" for m in manifest))
(OUT/'sizes.txt').write_text('lines bytes copy\n'+''.join(f"{m['lines']} {m['bytes']} {m['copy']}\n" for m in manifest))
print(json.dumps({'snapshots':[{'file':v,'bytes':(OUT/v).stat().st_size} for v in versions],'step_metrics':{k:{x:v[x] for x in ['tool_calls','assistant_turns','output_tokens','wall_minutes','models','brief','instruction_evidence']} for k,v in sessions.items()},'report_counts':[{'round':r['round'],'counts':r['counts'],'openprior':r['unresolved_priors']} for r in parsed]},indent=2))
