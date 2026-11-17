# 03 Tavily research: blocker classification for review gates

Provenance: researched by the `deep-research-agent` (Tavily backend) on 2026-11-15; that agent had no file-write tool, so the orchestrator saved its returned report here unchanged apart from replacing a few symbols (kappa, the greater-or-equal signs, the multiplication sign) with ASCII. Sources are cited by key. "Snippet" means only the Tavily search excerpt was read, not the full page. Fetch date for every source: 2026-11-15.

Status: Complete

## Source key
**TypeSafe**
- T1 https://docs.typesafe.ai/llms.txt
- T2 https://docs.typesafe.ai/primitives/noul.md
- T3 https://docs.typesafe.ai/primitives/score.md
- T4 https://docs.typesafe.ai/primitives/advanced.md
- T5 https://docs.typesafe.ai/confidence.md
- T6 https://docs.typesafe.ai/model-jaggedness.md
- T7 https://docs.typesafe.ai/models.md
- T8 https://docs.typesafe.ai/api/errors.md
- T9 https://docs.typesafe.ai/introduction/quickstart.md
- T10 https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md
- T11 https://github.com/typesafe-ai/skills
- T12 https://docs.typesafe.ai/patterns/probability-routing.md
- T13 https://docs.typesafe.ai/cookbooks/llm_guardrails.md (partial page)
- T14 https://docs.typesafe.ai/cookbooks/entity_alignment.md (partial page)
- T15 https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook.md (consistency_choice_cookbook seen as snippet)
- T16 https://docs.typesafe.ai/sdk/python/api/constants.md
- T17 https://docs.typesafe.ai/sdk/python.md
- T18 https://docs.typesafe.ai/introduction/machine-learning-primer.md (partial)
- T19 https://docs.typesafe.ai/concepts/how-to-build-with-system-one.md (partial)
- T20 https://typesafe.ai
- T21 https://docs.typesafe.ai/cookbooks/parallel_questions.md (snippet)
- T22 https://docs.typesafe.ai/introduction.md (partial)
- T23 https://vandatateam.com/blog/jev-api-getting-started (third party, snippet)
- T24 https://flaviocopes.com/jev-api-key (third party)
- T25 https://www.lindy.ai/blog/jev-ai (third party, snippet)

**Review and severity practice**
- G1 https://google.github.io/eng-practices/review/reviewer/standard.html
- G2 https://google.github.io/eng-practices/review/reviewer/pushback.html
- G3 https://google.github.io/eng-practices/review/reviewer/looking-for.html
- C1 https://conventionalcomments.org
- M1 https://learn.microsoft.com/en-us/azure/devops/repos/git/review-pull-requests?view=azure-devops (snippet)
- M2 https://learn.microsoft.com/en-us/azure/devops/repos/git/copilot-code-reviews?view=azure-devops (snippet)
- CH1 https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/release_blockers.md
- CH2 https://www.chromium.org/issue-tracking/release-block-guidelines (snippet)
- K1 https://kubernetes.io/releases/release (snippet)
- IE1 https://dokumen.pub/ieee-std-1028-2008-standard-for-software-reviews-and-audits-978-0-7381-5768-9-978-0-7381-5769-6.html (unofficial copy of IEEE 1028-2008)
- IE2 https://www.ctestlabs.org/neoacm/1044_2009.pdf (copy of IEEE 1044, snippet)
- IE3 https://standards.ieee.org/standard/1028-2008.html (official page, scope only)
- CV1 https://www.first.org/cvss/specification-document (snippet)
- CV2 https://nvd.nist.gov/vuln-metrics/cvss (snippet)
- SV1 https://www.qamadness.com/bug-severity-vs-priority-defect-management (snippet)
- SV2 https://marker.io/blog/bug-severity-vs-priority (snippet)
- SV3 https://community.atlassian.com/forums/discussion/965968/severity-vs-priority (forum, snippet)

**LLM judge**
- J1 https://arxiv.org/abs/2306.05685 (snippet)
- J2 https://www.alphaxiv.org/abs/2306.05685 (summary, snippet)
- J3 https://arxiv.org/html/2606.19544v1 (snippet)
- J4 https://mlflow.org/articles/judge-consistency-llm
- J5 https://arxiv.org/abs/2404.18796 and https://www.alphaxiv.org/abs/2404.18796 (snippet)
- J6 https://arxiv.org/html/2508.06225v2 (snippet)
- J7 https://www.langchain.com/resources/llm-as-a-judge (snippet)
- J8 https://futureagi.com/blog/llm-as-judge-best-practices-2026 (snippet)
- J9 https://tailoredai.substack.com/p/judging-llm-as-a-judge-with-mt-bench (snippet)

**Deferral**
- D1 https://sre.google/workbook/postmortem-culture (snippet)
- D2 https://sre.google/static/pdf/login_spring17_09_lunney.pdf (snippet)
- D3 https://www.atlassian.com/agile/software-development/technical-debt (snippet)
- D4 https://www.ltvco.com/engineering/building-technical-debt-backlog (snippet)
- D5 https://docs.coderabbit.ai/issues/creation (snippet)
- D6 https://docs.coderabbit.ai/changelog (snippet)
- D7 https://jacobtomlinson.dev/posts/2024/most-stale-bots-are-anti-user-and-anti-contributor-but-they-dont-have-to-be (snippet)
- D8 https://fvsch.com/stale-bots (snippet)
- D9 https://incident.io/blog/sre-incident-postmortem-best-practices (vendor blog, snippet)
- D10 https://www.itoc360.com/postmortem-action-items (vendor blog, snippet)
- D11 https://mairieli.com/files/papers/BotSE2019.pdf (snippet)
- D12 https://github.com/orgs/community/discussions/166504 (snippet)

---

## 1. TypeSafe / Jev

**1.1 Expressing a rule set as criteria**
- A Noul takes `instructions` (a yes/no question or statement) and optional `criteria` with `true` and `false` descriptions of what yes and no mean. [T2]
- Structured `criteria.true` and `criteria.false` accept objects, so a definition plus examples can sit on each side. [T4]
- A Score takes an ordered `criteria` array of 2 to 10 level descriptions. A Choice takes a dictionary of option descriptions. [T3, T9]
- Instructions and criteria can be a string, object or array. Use the same field names on every level, for example `what` and `examples`. [T3, T4]
- Each level is judged on its own. The model does not see level numbers or neighbouring levels. [T3]
  - Numbers-only levels gave score 0.55 at confidence 0.33 on a clear cosmetic bug. The descriptive levels gave 0.0 at confidence 1.0. [T3]
- Examples help only when they resemble the input. For the Safari bug, a matching example moved confidence from 0.35 to 0.96. An unrelated example changed nothing. [T3]
- The SKILL says to ask one judgment per question and beware "or" and "and". A list of rules should become one question per rule. [T10]
- It also says to describe a Noul's `false` case as a concrete situation, and to name the specific confusing case in the criteria. [T10]
- The jaggedness page says `instructions` and `criteria` must not contradict each other. A Noul where `true` maps to no performs worse. [T6]
- **Applies here:** each blocker characteristic becomes one Noul with a true and a false description, plus 1 to 2 examples drawn from real past gate halts. Do not ask Jev "is this a blocker?". [T10] says that question is at the wrong layer.

**1.2 Scoring severity on levels**
- The docs' own Score example is `bug_severity` with three levels: cosmetic, broken with a workaround, blocking with no workaround. [T3]
- `score` is the sum of level number times level probability. It can fall between levels. `probabilities` and `legend` are returned. [T3]
- A fractional score is a position, usable for ranking or for rounding to the nearest level. It does not measure "the fraction of customers without a workaround". [T3]
- Different distributions can give the same score. Read `probabilities` and `confidence` alongside it. [T3, T5]
- The Composite scoring pattern splits a judgment into several Scores, divides each by `len(criteria)-1`, then combines them with weights set in code. [T3]
- Do not interpolate between levels to recover an exact number. [T6]
- Give a rare extreme case its own level. [T3]
- **Applies here:** severity is a later phase and only for confirmed blockers. Use 3 to 4 situation-described levels, one dimension per Score. Keep severity separate from priority (see 2.5).

**1.3 Calibrated probabilities and turning Noul answers into a decision**
- A Noul returns one number, the probability that the answer is yes. It has no `confidence` field. A value near 0.5 means the state does not settle the question. [T2, T5]
- Start with thresholds of 0.7 for yes and 0.3 for no. Give the band between them its own outcome, such as sending it to a person. [T2, T5, T10]
- Raise the yes threshold when a false yes is expensive. Lower it when a missed yes is expensive. Avoid fitting thresholds to a handful of cases. [T2]
- The docs show a two-Noul decision in code with three outcomes. `NO &lt; p &lt; YES` on either question goes to review. [T2]
- The SKILL says to treat each decision as a truth table: Jev supplies the judgments, code holds the logic. Give every combination of answers an outcome, including "between thresholds". [T10]
- For a Choice, threshold the probability of the option you act on. For a Score tied to one level, threshold that level's probability. `confidence` is rarely the gate. [T5, T10, T12]
- The confidence formulas are published:
  - Noul: `|2p-1|`.
  - Choice: `(pmax-1/n)/(1-1/n)`.
  - Score: distance-weighted, floored at 0. [T5]
- "Calibrated" is defined as grouped rates: outcomes given 0.8 occur about 80% of the time, which is not a guarantee for one answer. [T18]
  - It is vendor-asserted (the model is trained with "RLCD"). I found no independent calibration evidence.
- **Applies here:** blocker confidence is the Noul probability itself. Three outcomes per characteristic: confirmed (>=0.7), rejected (<=0.3), uncertain (between).

**1.4 Published examples close to our use**
- The LLM guardrails cookbook is the closest analogue. [T13]
  - Hazard Nouls each have an `action_threshold` (act) and a lower `review_threshold` (send to a human).
  - A separate severity Score has its own threshold and can turn a review into a block.
  - Named policies (`strict`: review 0.35, action 0.70; `permissive`: review 0.70, action 0.85) show the same probabilities routed differently.
  - Action precedence is ordered: support, block, review, pass.
- The entity alignment cookbook uses one Score whose levels are the outcomes: leave unlinked, send for review, merge. Cut points sit between levels. [T14]
- No published Jev example of classifying review findings or issues by rules was found. The nearest are `bug_severity`, the support-ticket triage composite [T3] and T13.
- **Applies here:** copy the structure of T13 (Nouls, then a severity Score, then per-gate named policies). Per-gate policies suit our case, since spec, tasklist and research gates carry different risk.

**1.5 Evaluating accuracy**
- The docs say to test thresholds by plotting confidence against accuracy on your own data. [T19]
- The SKILL's test advice: [T10]
  - Use representative, hard and negative cases.
  - Compare wordings as separate questions in one request, over the same state.
  - Keep the exact payload for each case.
  - Check each change on cases not used for tuning.
  - Yellow flags: criteria that gain a clause per failing case, fitted thresholds, tests that assert an exact probability.
- The self-consistency cookbooks measure how often a decision flips when the same input is asked again, with no answer key needed. Setup: 15 repeats x 40 claim versions. [T15]
  - Vendor-run on `jev-1.14.0`, 2026-11-02. Jev: 3.8% (Noul) and 4.0% (Choice) average flip. LLMs: 14.2% to 43.5%. [T15]
- The parallel questions cookbook used 5 repeats and found 7 of 13 answers identical across all 5. Jev is therefore not fully deterministic. [T21, snippet]
- I found no built-in evaluation harness or test-set feature in the docs.
- **Applies here:** the 5-run test fits the flip-rate method. Add a labelled gold set, because flip rate says nothing about correctness. [T15 says so itself]

**1.6 Limits and jaggedness**
- Context: 64k per request and 32k per question by default. [T7]
  - A `TypeSafe-Danger-Zone-Long-Context: true` header raises both to 262k, at the same price per token but slower and less accurate. [T7]
  - Request body <=32 MiB; <=64 nesting levels; finite numbers only; UTF-8 JSON. [T8]
- Rate limits are per organisation, in tokens/s and requests/s, shown in the console. A 429 or 529 means retry with exponential backoff, and the SDKs do this by default. [T7, T8]
  - A third party reported 100,000 tokens/s and 80 requests/s, "can change without notice". [T25, not official]
- Jaggedness, with the workaround for each: [T6]
  - Literal reading: write the exact condition.
  - Math and counting: do it in code.
  - Dates: extract in the model, compare in code.
  - Indirection and double negatives: write directly.
  - Large state full of irrelevant detail: filter first. Accuracy falls as the state grows ("context rot").
  - Adversarial content: text that argues for its own classification can move the answer.
  - Contradictory criteria.
  - Choice option order: Jev leans to the first option, so reorder and recheck.
  - Generation: not supported.
- **Applies here:**
  - Send only the finding text plus the cited excerpt, not the whole spec or report.
  - A reviewer's finding can assert "this is a blocker", which is exactly the adversarial case. Strip or ignore that assertion before classifying. [INFERENCE]

**1.7 Key, pricing, free tier (reported, nothing created)**
- Get a key at https://console.typesafe.ai/keys. [T9]
- The Python SDK reads the `TYPESAFE_API_KEY` environment variable. The base URL and default model variables are `TYPESAFE_BASE_URL` and `TYPESAFE_DEFAULT_MODEL`. [T16, T17]
  - `TypeSafeClient()` picks up the key. An `api_key=` argument also exists. [T17, T21]
- HTTP: `POST https://api.typesafe.ai/v1/systemone` with `Authorization: Bearer <key>`. [T9]
- Install: `uv add typesafe-sdk` or `pip install typesafe-sdk`. Python 3.10 or later. Default timeout 10 s. [T9, T16, T17]
- Pricing: $42 per billion input tokens ($0.042 per million). Output tokens are free. `jev-1.14.0` and `jev-1.13.0` cost the same. [T7, T20]
- `jev-latest` points to `jev-1.14.0`, and an alias moves when a new release ships. Pin the versioned ID once thresholds are tuned. [T7]
- Free tier or trial: the official docs I read state none.
  - A third party says new users get a $5 credit (about 119M input tokens). [T23]
  - Another says signups were paused after 2026-09-20, with the Vercel AI Gateway as an alternative. [T24]
  - Neither is confirmed on TypeSafe's own pages.
- Data: Jev is not trained on customer requests. Zero data retention is for enterprise customers. [T7]
- The agent skill: MIT licence, 3 commits, installed with `claude plugin marketplace add typesafe-ai/skills`, then `claude plugin install typesafe@typesafe-ai`. [T11]
  - It says to ask the user's permission before live API tests, agree a budget, and disclose what data will be sent. [T10]
- **Applies here:** review text would leave the machine, so the owner must approve that. Keep the key in an environment variable, and never in the repo.

## 2. Severity and blocker practice

**2.1 Google engineering practices**
- Approve once the change "definitely improves the overall code health", even if it is not perfect. This is "the senior principle". [G1]
- If a comment is "not very important", prefix it "Nit:". It is polish the author may ignore. Purely educational comments get the same label. [G1]
- Reviewers should not block on personal style preference. [G1]
- Exception: never approve a change that definitely worsens code health, except in an emergency. [G1]
- **Applies here:** the gate test is "would the artifact, as it stands, make the downstream decision worse", not "is it perfect".

**2.2 Conventional Comments**
- Labels such as `issue`, `suggestion`, `nitpick` and `question`. `nitpick` is "trivial, preference-based" and "non-blocking by nature". [C1]
- Decorations: `(blocking)`, `(non-blocking)`, `(if-minor)`. A decoration overrides whichever default a team has. [C1]
- Comments are "parseable by machines". [C1]
- **Applies here:** this is a ready finding schema. Reviewers emit a label plus an explicit blocking decoration, and the classifier then checks that decoration.

**2.3 Microsoft Azure DevOps**
- Votes: Approve, Approve with suggestions, Wait for author, Reject. Wait and Reject block only when a required reviewer sets them. [M1, snippet]
- Copilot review "always leaves a Comment review" and never blocks merging. [M2, snippet]
- **Applies here:** blocking is a separate, explicit act from commenting. Snippet only.

**2.4 Chromium and Kubernetes release blocking**
- Chromium: do not use a block label unless "we genuinely believe we cannot ship" with the issue present. Do not mark an issue a blocker "to ensure someone looks at it"; use priority and milestone labels for that. [CH1]
- The Chromium block level comes from a matrix of severity (impact on an affected user) times prevalence (how many users). [CH1]
- Uncertainty is assessed explicitly:
  - Bias upward for a possible "tip of an iceberg".
  - Bias downward for a bug that has been live for months.
  - State this reasoning in the bug update. [CH1]
- Bugs behind a disabled flag never block. A regression is not a blocker just for being a regression. They track introduced versus escaped regressions. [CH1]
- Anyone may add or remove a block label under the guidelines. [CH1]
- Kubernetes: `priority/critical-urgent` is release blocking and "would require a patch release if left undiscovered". `priority/important-soon` is not blocking and moves out of the milestone at code freeze after a grace period. [K1, snippet]
- **Applies here:** "cannot ship / would need rework if found later" plus "reach" are the two cleanest blocker tests. The "attention" misuse is exactly our problem.

**2.5 Severity versus priority**
- Severity is impact. Priority is the fix order. [SV1, SV2]
- A forum answer says "severity is objective, priority is subjective" (low authority). [SV3]
- Common S1 to S5 scales: blocker (crash, testing blocked), critical, major (feature broken, workaround exists), minor, trivial. [SV1, SV2]
- **Applies here:** three separate outputs: blocker (gate), severity (impact), priority (order of follow-up).

**2.6 IEEE, CVSS, ISO**
- IEEE 1028-2008 section 6.8.3 ranks anomalies by potential impact: [IE1, unofficial copy]
  - Catastrophic: mitigation not possible.
  - Critical: partial to complete mitigation possible.
  - Marginal: minor consequences.
  - Negligible: no failure.
- For audits, an observation is major "if the non-conformity will likely have a significant effect on product quality, project cost, or project schedule". Otherwise it is minor. [IE1]
- IEEE 1028 does not specify the disposition of results. [IE3]
- IEEE 1044 severities are Blocking, Critical, Major, Minor and Inconsequential. [IE2, snippet]
- CVSS maps a numeric score to bands: None 0, Low 0.1 to 3.9, Medium 4.0 to 6.9, High 7.0 to 8.9, Critical 9.0 to 10. NVD says "CVSS is not a measure of risk". [CV1, CV2, snippets]
- **Applies here:** CVSS composes atomic metrics into a score and then bands it, which matches the Jev composite pattern. IEEE's "major = significant effect on quality, cost or schedule" is a usable blocker definition.
- ISO/IEC 25010 was not read (see "not confirmed").

**2.7 Generic blocker characteristics distilled from these sources [INFERENCE]**
1. Decision-changing: leaving it unfixed makes a consumer decide or act differently, or a downstream step wrong. [G1, IE1, CH1]
2. Concrete and evidenced: it points to a location and a wrong result, not a preference or a lesson. [G1, C1, CH1]
3. Costly if found later, or cannot be mitigated downstream. [K1, IE1]
4. Reach: it affects the artifact's core purpose or many consumers. [CH1]
5. Not nit, style or education. [G1, C1]

## 3. LLM-as-judge for severity and rubric scoring

- Strong judges such as GPT-4 reach over 80% agreement with human preferences, the same as human-to-human. Biases named: position, verbosity, self-enhancement. [J1]
- Under order swapping, GPT-4 was consistent in 65.0% of cases on deliberately similar answers, which is a stress test. [J2]
- The remedy is to swap order and only call a win if it holds in both orders. [J9]
- A 2026 study of 21 judges (about 541,000 judgments): [J3, snippet; full paper not read]
  - Raw agreement overstates Cohen's kappa by 33 to 41 points.
  - Test-retest above 0.95 can coexist with position bias above 0.10 (the "consistency-bias paradox").
  - Verbosity bias was below 0.011 for all 21, against 20 to 40% in older work.
- A practitioner protocol: [J4]
  - At least 3 replicates, run AB and BA orders.
  - Report Cohen's kappa (headline target above 0.61) next to raw agreement.
  - Flag a judge with test-retest above 0.95 and position bias above 0.10.
  - Revalidate on a fixed calibration set after any model, prompt or rubric change.
  - Bootstrap confidence intervals.
- A panel of diverse smaller models beat a single large judge, with less intra-model bias, at about 7x lower cost. kappa: 0.763 NQ, 0.906 TriviaQA, 0.867 HotpotQA. [J5, summary]
- LLM judges are overconfident: stated confidence exceeds accuracy. An ensemble "fuser" improved accuracy by up to 47.14% and cut ECE by 53.73% on JudgeBench. [J6, snippet]
- Binary or low-precision rubrics are more reliable than fine numeric scales. [J7, vendor docs]
- kappa of 0.6 as a common bar, and monthly recalibration against a gold set. [J8, blog]
- Replicate counts seen: at least 3 [J4], 5 [T21], 15 [T15].
- **Applies here:**
  - Position bias maps to Jev's Choice-order lean [T6]. A Noul-per-characteristic design has no option order.
  - Verbosity maps to long, forceful findings; test it by padding a finding and checking the probability does not rise (INFERENCE).
  - Use few levels and a gold set.
  - Report kappa, not raw agreement.
  - A model that states its own confidence in words is not enough. Jev's probabilities still need our own calibration check.

## 4. Deferring non-blocking findings

- Google, against "clean it up later": experience shows deferred cleanup usually never happens, and letting it slide is "a common way for codebases to degenerate". [G2]
  - The same page says that if a change exposes surrounding problems that cannot be fixed now, the developer files a bug for the cleanup and assigns it to themselves so it does not get lost. [G2]
- Google SRE postmortems: [D1, D2]
  - Action items are filed as bugs in the central tracker with an owner and a tracking number.
  - Each has a priority and a verifiable end state.
  - Closure is monitored, with a burndown of follow-through.
  - Priority P0 and P1 are defined by recurrence risk.
  - "The surest way for an action item never to be completed is to leave it without an owner." [D2]
- Vendor blogs give a rule of thumb: completion below 50% means the process is theatre. Track items in the same backlog as planned work, and write fewer, better-prioritised items. [D9, D10]
- Atlassian says to prioritise tech debt like feature work and not hide it in a separate backlog. It also notes "zero open bugs" is usually reached by deferring the rest. [D3]
- LTV: tag, prioritise and date debt tickets and re-check them on a schedule. [D4]
- CodeRabbit creates GitHub, GitLab, Jira or Linear issues from review conversations when asked (`@coderabbitai`). Its changelog pitches it for "Want to defer the suggestion? Ask the bot to create an issue". [D5, D6]
  - This is on request, not automatic.
  - Copilot review does not follow reply threads, per a community answer. [D12, weak]
- Stale bots that auto-close are criticised: a clear actionable task should not close from inactivity, and a human should decide. [D7, D8]
  - A study says the bot is recommended with exemptions, such as bug reports. [D11]
- Kubernetes moves `important-soon` items out of the milestone after a grace period, which is deferral with a defined escalation. [K1]
- Risks:
  - Hidden defects, if a decision-changing finding is deferred by mistake.
  - Backlog rot.
  - Flooding the backlog.
  - Closing silently.
- Mitigations seen: owner, priority, verifiable end state, closure tracking, scheduled review, human-only closure.
- **Applies here:** the offer must carry an owner, priority, link and end state, and it must never expire silently.

## Not confirmed
1. Whether Jev has a free tier or trial. The official docs I read do not say. The $5 credit [T23] and the paused signups [T24] are third-party.
2. Whether signup works today, and our organisation's rate limits (only visible in the console, which I did not enter).
3. How accurate or well calibrated Jev is for classifying review findings. Calibration and all Jev consistency figures are vendor claims.
4. Any published Jev example classifying review findings or issues by rules. None found.
5. Whether Jev's Noul answers vary on repeat. The "Is Jev deterministic?" FAQ on the home page was collapsed. [T21] shows some answers varied across 5 repeats.
6. How Jev handles long, structured finding text. The jaggedness page warns about large irrelevant state.
7. What "the 5-run test" means. I assumed five repeated runs of the classifier over a labelled set. This needs the owner's definition.
8. ISO/IEC 25010, GitHub's own review guidance, Atlassian code review guidance and Microsoft engineering-playbook guidance were not read. Microsoft claims are snippet-only.
9. IEEE 1028 and 1044 text came from unofficial copies. The official pages are paywalled.
10. J3, J5, J6, J1, K1, CV1 and CV2 were read as search snippets only. The papers' full methods were not read.
11. Vendor-blog numbers (D9, D10, J7, J8) are practitioner opinion, not studies.
12. A dedicated "ship with known issues" policy source was not found beyond D3.
13. The "Jev choice up to 255 options" figure is second-hand (dev.to) and was not checked.

## Implications for the design

1. **[INFERENCE]** Define a blocker with five generic characteristics: decision-changing, concrete and evidenced, costly if found later, in reach of the artifact's purpose, and not nit, style or education (see 2.7). Basis: [G1, C1, CH1, K1, IE1]. Require the first two plus at least one of the next two.
2. **[SOURCED]** Make reviewers emit Conventional Comments-style labels plus an explicit `(blocking)` or `(non-blocking)` decoration, so the classifier has structured input. [C1] Add a "decision this changes" field. A blocker claim without it is downgraded.
3. **[SOURCED]** Adopt Chromium's rule that "blocker" is for "cannot ship", never "to get attention". Route attention through priority or follow-up instead. [CH1]
4. **[SOURCED]** Build the classifier as one Noul per characteristic, and put the decision in a code truth table. Never ask Jev "is this a blocker?". [T10, T2] Run deterministic checks first, such as the reviewer's own decoration and whether the finding cites a location, because dates, counts and exact checks belong in code. [T6]
5. **[SOURCED]** Use 0.7 and 0.3 as starting thresholds per Noul, with three outcomes: confirmed, rejected, uncertain. [T2, T5] Treat a missed real blocker as costlier than a false halt, so set the "reject" side conservatively. For uncertain cases, re-ask once with the state or wording varied, then send them to the orchestrator or owner. Keep per-gate policies, as in the guardrails cookbook. [T13]
6. **[INFERENCE]** Derive the blocker confidence score from the Noul probabilities. Report the minimum of the required characteristics rather than a product, since independence is not established. Log every characteristic probability so a halt can be explained.
7. **[SOURCED]** For severity (phase 2, blockers only), use a Score with 3 or 4 situation-described levels, one dimension per Score, and read per-level probabilities rather than the position alone. [T3, T5] Keep severity separate from priority. [SV1, SV2] IEEE's mitigation-possible ranks are a model for the levels. [IE1]
8. **[SOURCED]** Pin `jev-1.14.0` rather than `jev-latest`, and log the `model` field and the exact payload per call. [T7] Keep the key in `TYPESAFE_API_KEY` [T16], get owner approval before sending review text off the machine and agree a budget [T10], and use `uv add typesafe-sdk` to match the repo rule. [T17]
9. **[SOURCED]** Send Jev only the finding, its cited excerpt and the artifact type, not the whole document. Reviewer-written text can argue for its own severity, which is the adversarial case. [T6] Strip "this is a blocker" assertions before classifying. [INFERENCE]
10. **[SOURCED]** Make the 5-run test a gold-set test, not only a repeat test. [T15, J4, T10]
    - Gold set: past gate halts labelled by the owner, ideally two labellers with kappa reported between them.
    - Include negatives and borderline cases.
    - Hold out cases not used for tuning.
    - Replicate each case at least 3 times (5 matches TypeSafe's own cookbook).
    - Report flip rate, kappa against gold, and above all the count of real blockers wrongly deferred.
    - Compare rule wordings as separate questions in one request, and never assert an exact probability in a test.
    - Re-run after any rule, threshold or model change.
11. **[SOURCED]** Make record-and-offer concrete. Every deferred finding becomes an entry with an owner, a priority, a link to the source finding and a verifiable end state. [D1, D2, G2] Offer the batch to the user once at the end of the gate, and create issues only when the user says yes (the CodeRabbit pattern). [D5, D6] Never auto-close or expire entries. [D7] Report the open count and closure rate at later gates. [D2]
12. **[INFERENCE]** Guard against hidden defects. At each gate, audit all "uncertain" cases and a random sample of "deferred" ones. Promote a deferred finding to blocker if independent reviewers raise it again or a later gate trips on it. Track escaped blockers the way Chromium tracks escaped regressions. [CH1] Sample size and cadence are open.

Sources are listed in the Source key above.
