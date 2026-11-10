import json,glob,collections,sys,os
os.chdir('score'); sys.argv=['x','out']; sys.path.insert(0,'.')
import aggregate as A
os.chdir('..')
rows=A.rows
arms=collections.defaultdict(list)
for r in rows.values(): arms[r['arm']].append(r)
mean=lambda v:sum(v)/len(v)
L=json.load(open('ledger.json'))
sev=collections.Counter(d['severity'] for d in L['defects'])
tok={'base-fresh':53623,'stage2':100424,'ab1':122146,'ab2':43152+31000,'ab3':91552+31000,'ab4':106519,'pn1':408316,'pn2':47033}
perm={'stage2':.432,'ab1':.079,'ab2':.945,'ab3':.022,'ab4':.027,'pn1':.003,'pn2':.227}
P=[].append
out=[]; P=out.append
P('# #346 defect-ledger rescoring (2026-11-10)\n')
P('Method: all 511 blocking findings (first reviews and frozen audits, 13 arms, 140 audits) were clustered into 20 chunks; 20 validator agents (11 Opus, 9 Sonnet) merged them into defects and checked each against the original spec; one Opus reconciler deduplicated them into a ledger of **%d defects (%s)**, 7 introduced-defect patterns, 5 unvalidated candidates, 9 rejected and 2 unverifiable. Then each of the 70 final specs was scored blind (arm names removed, order shuffled) by one Sonnet agent against every ledger defect: FIXED / DELETED_OK / PARTIAL / PRESENT / WORSE / MOOT_BAD. Six specs were scored again by Opus as a calibration.\n'%(len(L['defects']),', '.join(f'{v} {k}' for k,v in sev.items())))
P('Calibration (6 specs, Sonnet vs Opus): exact status agreement 96.2%, fixed-vs-residual agreement 98.1%; Opus is slightly stricter (5 FIXED to PARTIAL, 4 PRESENT to PARTIAL), by about the same amount on a baseline spec and on an ab3 spec, so arm comparisons are not affected.\n')
P('## Results: residual ledger defects per final spec (lower is better)\n')
P('`resid_blk` = blocking defects still present (PRESENT, PARTIAL, WORSE, MOOT_BAD) out of 20; `weighted` = 3 x blocking + 2 x medium + 1 x minor residual; `fixed` = defects FIXED or DELETED_OK out of 44; p = two-sided permutation test (20,000 shuffles) on the weighted score vs the fresh Sonnet baseline (Haiku arms vs the Haiku baseline). Loop tokens are output tokens per run, loop steps only (no audits). ab2 and ab3 have no R1 step in their recount, so ~31k (baseline R1) was added: marked ~.\n')
P('| arm | n | resid_blk /20 | weighted | fixed /44 | p vs baseline | introduced patterns | loop tokens | x fresh |')
P('|---|---|---|---|---|---|---|---|---|')
names=[('base-fresh','FRESH baseline'),('stage2','stored baseline (stale)'),('ab1','ab1 k=3 union+verify'),('ab2','ab2 verify gate k=1'),('ab3','ab3 final whole-doc gate'),('ab4','ab4 lint + k=2 + verify'),('pn1','PN1 panel+merge+ledger'),('pn2','PN2 mechanical lint')]
for a,n in names:
    v=arms[a]; t=tok[a]; ts=('~' if a in('ab2','ab3') else '')+f'{t:,}'
    P(f"| {n} | {len(v)} | {mean([x['resid_blk'] for x in v]):.1f} | {mean([x['resid_w'] for x in v]):.1f} | {mean([x['fixed'] for x in v]):.1f} | {'-' if a=='base-fresh' else '%.3f'%perm[a]} | {mean([x['intro'] for x in v]):.1f} | {ts} | {t/53623:.2f}x |")
P('')
P('| Haiku arm | n | resid_blk /20 | weighted | fixed /44 | p vs Haiku baseline | loop tokens |')
P('|---|---|---|---|---|---|---|')
htok={'haiku-base':167382,'ab1h':419037,'ab2h':235803,'ab3h':319005,'ab4h':254000}
hp={'ab1h':.081,'ab2h':.730,'ab3h':.034,'ab4h':.025}
for a,n in [('haiku-base','Haiku baseline'),('ab1h','ab1 (Haiku)'),('ab2h','ab2 (Haiku)'),('ab3h','ab3 (Haiku)'),('ab4h','ab4 (Haiku)')]:
    v=arms[a]; P(f"| {n} | {len(v)} | {mean([x['resid_blk'] for x in v]):.1f} | {mean([x['resid_w'] for x in v]):.1f} | {mean([x['fixed'] for x in v]):.1f} | {'-' if a=='haiku-base' else '%.3f'%hp[a]} | {htok[a]:,} |")
P('')
P('## Marginal cost of each fix (Sonnet arms, vs the fresh baseline)\n')
P('| arm | extra fixed defects | extra loop tokens | fixes per 100k extra tokens |'); P('|---|---|---|---|')
b=mean([x['fixed'] for x in arms['base-fresh']])
for a in ['ab1','ab3','ab4','pn1']:
    df=mean([x['fixed'] for x in arms[a]])-b; dt=tok[a]-53623; P(f'| {a} | {df:.1f} | {dt:,} | {100000*df/dt:.1f} |')
P('')
P('## What this shows\n')
P('1. **The loop does not converge, and the audits were hiding that.** The unchanged design fixes about 3 of 44 ledger defects (17 of 20 blocking defects remain in its final spec). A frozen audit reports about 1.2 blocking findings per spec, i.e. it samples roughly 7% of the blocking defects actually present. That sampling is why n=6 audit scores could not separate anything.')
P('2. **With the ledger the instrument is far tighter** (residual blocking sd about 2 per spec on a mean of 17, against roughly 60% relative noise for the audit count) and **three designs differ from baseline at p<0.05: PN1 (p=0.003), ab3 (0.022) and ab4 (0.027); ab1 is at p=0.08.** The same pattern holds on Haiku (ab3h p=0.034, ab4h p=0.025, ab1h p=0.08).')
P('3. **PN1 has by far the largest effect** (15.5 fixed against 2.8; 10 of 20 blocking left against 17) but needs about 408k loop tokens in its complete runs (r4-r6), 7.6x the baseline, spread over Fable, Sonnet and Haiku tiers. The earlier 66,240 figure for PN1 was wrong (it lacked most of the R1 panel steps) and is withdrawn. Runs r1 and r2 still have unmatched panel steps, so their totals are undercounts.')
P('4. **ab4 is the most economical improvement** (6.6 extra fixes per 100k tokens, about 2x baseline cost); ab3 and ab1 land near it. **PN2 (mechanical lint alone) and ab2 (verify gate alone) do nothing for the final spec**, though PN2 is the cheapest arm.')
P('5. **No design makes the loop converge.** Even PN1 leaves half the blocking defects. The ones that survive in almost every arm are the P1 scope and AC-0.4 step-3 defects (per-defect table: `score/perdefect.md`): reviewers raise them but the revise step does not resolve them.')
P('')
P('## Checks done and limits\n')
P('- **Circularity.** The ledger comes from findings of the same runs, so an arm whose reviewers found more could look better. Leave-source-out check: restricting to defects supported by 2 or by 3 or more arm families leaves the ranking and significance unchanged (PN1 p=0.003, ab3 0.022, ab4 0.027/0.049, ab1 0.079/0.047). 14 of 44 defects were raised by one arm family only (ab4, pn1, ab3).')
P('- **Fix by deletion.** DELETED_OK occurs 0-2 times per arm in total; PN1 specs stay about the size of the original (290 vs 285 lines) with 54 changed diff lines per spec on average; WORSE or MOOT_BAD occurs 3 times across the 6 PN1 specs and 0 times in the baseline.')
P('- **New defects.** Introduced-pattern hits are 0.3-1.3 per spec in every arm with no trend; unvalidated "other new defects" are 0.2-0.8 per spec (PN1 0.8, baseline 0.2).')
P('- **Ledger completeness is unknown.** 5 candidate defects found only while reconciling were present in nearly every spec; 14 defects have a single source arm family. A defect nobody found is invisible to this method.')
P('- n=6 per Sonnet arm (4 per Haiku arm). The ledger scorer is Sonnet; Opus agrees with it on 96% of 264 judgements.')
open('LEDGER-RESULTS.md','w').write('\n'.join(out)+'\n')
