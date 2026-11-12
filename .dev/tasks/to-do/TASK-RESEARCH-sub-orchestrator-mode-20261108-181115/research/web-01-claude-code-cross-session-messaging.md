# External Research: Claude Code Cross-Session Messaging

**Date:** 2026-11-09
**Status:** Complete (scoped source/web research; independent Phase4 QA pending)
**Template:** tech-research Web Research Agent Prompt and task Step4.1
**Delivery:** User-approved parent persistence of complete inline findings.

## Scope and Method
Complete exact findings: [returned/web-01-returned-findings.json](returned/web-01-returned-findings.json), text field. Required downstream with this substantive index, including full option-implication, hook-type, delivery and uncertainty tables. Agent ae9b2ca9e891fa528 performed external research/read-only source verification; parent persistence under approved adaptation, independent Phase4 QA pending.
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
No Tavily tools/aliases in agent inventory; permitted WebSearch/WebFetch fallback. Generic queries only, no private issue/code text sent externally. Official docs primary, longer-page relevant sections fetched after initially truncated extraction. Historical hooks page redirected and current destination fetched. Source/normative text verified by researcher, not live behavior. No settings/model/source/runtime/API mutations or messaging experiments. Documentation describes product features, not this installed deployment. Source reliability refers to cited content, not runtime certification.

## Issue Questions and Current Source Baseline
Source: https://github.com/IronbellyOrg/IronClaude/issues/339#issuecomment-6659559030 (HIGH relevance/HIGH primary-record reliability; proposal wording not behavior verification).
> 1. How does a sender mark itself as bypassing prompts so the receiver delivers its messages? Not documented on the page read.
> 2. Can a hook check or reject inbound cross-session messages?
Historical incident/effective launch modes not independently observed.

Researcher's directly read local-source aliases in full return: G=src/superclaude/hooks/scripts/launch-level-guard.sh; H=src/superclaude/hooks/hooks.json; K=src/superclaude/core/WORKER-CONTRACT.md; C=src/superclaude/skills/ccsession-tag/ccsession; F=src/superclaude/core/CLAUDE.md.
| Baseline | Status and direct-read anchors |
|---|---|
| Worker/ownership authority | [CODE-VERIFIED instruction text]K:60 internal Agent helpers distinct from top lifecycle; K:62 worker fan-out prohibited, K:69 person-opened coordinator; F:55-59 ownership phrase not grant. |
| Bound-session messaging/recognition | [CODE-VERIFIED]G:390-395 bound scope; G:686-687 SendMessage ESCAPE; G:737 denied; G:450/458 literal orca matcher not universal spelling proof. |
| Required probes | [CODE-VERIFIED]K:107,110,151 versus G:475-477 required worker-list/worktree ps/worker-read not exceptions; correction remains. |
| Prompt-hook registration/context | [CODE-VERIFIED]H:63-70 registers UserPromptSubmit5sec; H:115-123 includes SendMessage; G:185-203 local event/session/prompt fields, not authenticated external parent/grant. |
| Launcher defaults | [CODE-VERIFIED]C:135-141 CCSESSION_PERMISSIONS unset selects bypass flags, default omits, other values rejected; CC_CLAUDE_FLAGS override. Not historical/current effective mode proof. |
| Follow-up and admission | [CODE-VERIFIED instruction text]K:61 applied/queued/refused; K:103-108 Delivery/sender/completion handling; K:138 acknowledgement not answer correctness; K:101,105-106 vocabulary/unknown types and sender identity. |
| Human/progress/need | [CODE-VERIFIED instruction text]K:57 human Rulings; K:41-44 narrow outward grant; K:110-113/151/157 semantic progress/probes, not heartbeat alone; K:246 unforeseen follow-up timing duty. |
| Origin/timeout integration | [UNVERIFIED live]G:341-361 plan-approval text recognition plus no authenticated peer-origin parse merits origin separation check; no proven laundering. H lacks onFailure:block, internal G:142-161 trap not host-timeout proof. |
External corroboration/contrast: https://code.claude.com/docs/en/hooks#userpromptsubmit ; https://code.claude.com/docs/en/cross-session-messaging#how-a-session-treats-an-incoming-message

## External Findings
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
All external rows are documentation findings, not proof of installed behavior. Full exact return preserves the distinctions and sources beyond this index.
| # | Finding | Relevance | Reliability | Relationship | Source |
|---|---|---|---|---|---|
|1|Default receipt compares bypass/nonbypass classes, not mode-name equality. auto/acceptEdits/dontAsk prompting; interactive terminal plan with bypass available is bypass class. Prompting receiver holds bypass sender, bypass receiver holds nonbypass sender; same class ordinarily delivers subject to other controls.|HIGH|HIGH official|extends/qualifies sketch|https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages |
|2|Held means not in Claude context. Delivered/Held/Refused distinct; default interactive approval5min, denial/dismissal drops; noninteractive cannot showdialog and may expire; explicit hold does not expire and can later release on accept; heldqueue100 dropsoldest.|HIGH|HIGH official|supports hold mechanism, extends unattended risk|https://code.claude.com/docs/en/cross-session-messaging#non-interactive-sessions ; https://code.claude.com/docs/en/settings-reference#dialogexpiry |
|3|Actual supported mode controls documented, but sender class representation/validation/per-send assertion API not established. Bypass availability not actual activation; no message-text assertion grants identity.|HIGH|HIGH interface, internal UNVERIFIED|partially answers question1|https://code.claude.com/docs/en/permission-modes ; https://code.claude.com/docs/en/cli-reference#cli-flags ; https://code.claude.com/docs/en/tools-reference |
|4|crossSessionInbound accept/hold/refuse separates inbound policy from toolmode. Managed then --settings then user first applicable; project/local only tighten. No documented parent-only trustlist. isolatePeerMachines true at anyscope requires beyond-machine approval including bypass.|HIGH|HIGH official|extends alternatives to all-bypass|https://code.claude.com/docs/en/settings-reference#crosssessioninbound ; https://code.claude.com/docs/en/settings-reference#isolatepeermachines |
|5|UserPromptSubmit explicitly includes another session's message to main conversation, prompt text inspectable, decision:block/exit2 prevents receipt. Documented yes to question2, not universal active/idle/remote/nested runtime proof.|HIGH|HIGH official|extends, answers feature-level uncertainty|https://code.claude.com/docs/en/hooks#userpromptsubmit |
|6|Common session_id/permission_mode/agent_id/agent_type describe receiving execution context, transcript_path asynchronous and may lag; prompt/session_title not authenticated peer identity/parent/grant. Additional trusted origin fields unverified, not proved absent.|HIGH|HIGH documentedfields|supports trusted-origin gap|https://code.claude.com/docs/en/hooks#common-input-fields ; https://code.claude.com/docs/en/hooks#userpromptsubmit-input |
|7|Prompt-hook default30sec timeout ordinarily discards output/continues; command/HTTP onFailure:block differs, SDK callback timeout blocks. Current source guard5sec registration lacks it; internal trap not host-timeout guarantee. PreToolUse sendercheck vs inbound; PostToolUse cannot unsend; PermissionRequest not allincoming; Notification cannot block/modify.|HIGH|HIGH official/source|extends fail-closed/ordering requirements|https://code.claude.com/docs/en/hooks#userpromptsubmit ; https://code.claude.com/docs/en/hooks#pretooluse ; https://code.claude.com/docs/en/hooks#notification |
|8|Independent peer delivery between toolcalls, idle starts turn, active toolnotinterrupted; sender refusals/Not sent, recipientqueue/rate/duplicate/relay drops, holds/expiry exist. No universal send-success read/apply/completion guarantee. Team sent specifically means mailbox-file write succeeded; final subagent warning-prefixed handback is distinct. Do not transfer guarantees across channels.|HIGH|HIGH official|supports separate transport/application/admission evidence|https://code.claude.com/docs/en/cross-session-messaging#message-delivery ; https://code.claude.com/docs/en/errors#cross-session-message-was-dropped-at-the-recipient-sessions-inbox ; https://code.claude.com/docs/en/agent-teams#architecture ; https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode |
|9|Independent peers plain text; structured team protocols remain in team; mentions attachnothing and slashcommands are text, not automaticexecution. Typed envelope not identity/authorization/replay/lifecycle protection or guaranteed free-text noninfluence.|HIGH|HIGH official|qualifies typed-message sketch|https://code.claude.com/docs/en/cross-session-messaging#limitations ; https://code.claude.com/docs/en/cross-session-messaging#how-a-session-treats-an-incoming-message |
|10|Idle subscription one-shot/main conversations/same machine; finished emptyqueue or exit, inboundcontrols,12h expiry. Not success, admitted report, settledsubtree/cleanworktree/closurepermission.|MEDIUM|HIGH official|extends observations not supervision replacement|https://code.claude.com/docs/en/cross-session-messaging#get-a-notice-when-another-session-goes-idle |
|11|Peer message cannot approve pendingpermission, supply humanconsent, change permissions/CLAUDE/config or route denied work aroundsenderboundaries. Auto outbound SendMessage canblock beforedelivery, distinct from flaggedfinalreport handback. Bypass not prompt-injection defense/isolation.|HIGH|HIGH official|supports human-only authority, contradicts trustless modealignment|https://code.claude.com/docs/en/cross-session-messaging#how-a-session-treats-an-incoming-message ; https://code.claude.com/docs/en/agent-teams#messages-between-agents ; https://code.claude.com/docs/en/permission-modes |
|12|Current subagents boundednesting vs experimental teams no nestedteams vs independentpeertext all different. Child permission constrained by mainmode, not arbitrary elevation; do not infer independentOrcasession inheritance.|HIGH|HIGH currentdocs, installed UNVERIFIED|supports internal/external distinction|https://code.claude.com/docs/en/sub-agents ; https://code.claude.com/docs/en/agent-teams#limitations ; https://code.claude.com/docs/en/cross-session-messaging |
|13|Official SDK generic hooks example not authenticated receivingpeervalidator. Community guide puts planwithbypassavailable in prompting unlikecurrentofficialpage; officialmatrixwins, no newauthority discovered.|MEDIUM example/LOW community|HIGH primaryexample; MEDIUM community|extends context, illustrates docdrift|https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/hooks.py ; https://cc.bruniaux.com/guide/workflows/cross-session-messaging/ ; https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages |

### Decision implications
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
All eight original implication rows retained in complete return. Current flat policy still has bound-supervision probe compatibility question; permitted internal helpers keep top lifecycle; person-opened peers need ownership/admission and are not automatically unbound; supervised middle needs explicit policy/scope/aggregate/recovery; handoff owner needs eligibility/trusted parent/outward ownership/admission. All-bypass does not add least privilege/delivery/trust/authority; approved inbound accept is broader than parenttrust; files/schema need producerbinding/freshness/safe admission. Sources: findings4/5/8/9/11/12 URLs. These are decision prerequisites, not an implementation sequence.

## Gaps and Questions
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
All12 original groups retained; exact return contains per-row source URLs/status language.
| Gap | Disposition / evidence |
|---|---|
| Native sender-class representation/verification | [UNVERIFIED]question1 partiallyopen; no per-send API/wirecontract established; https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages |
| Historical incident configuration | [UNVERIFIED]sender mode/receiver settings not observed; https://github.com/IronbellyOrg/IronClaude/issues/339#issuecomment-6659559030 |
| Installed feature/version equivalence | [UNVERIFIED]no runtimecapability test; documented Linux minimum2.1.224 not installed-version assertion; https://code.claude.com/docs/en/cross-session-messaging#availability |
| Full inbound-route coverage | [UNVERIFIED live]docs mainconversation yes; active/idle/remote/nested envelopes not exercised; https://code.claude.com/docs/en/hooks#userpromptsubmit |
| Authenticated sender metadata | [UNVERIFIED]documented fields not verifiedsender; possibleadditionalruntimefields unestablished; https://code.claude.com/docs/en/hooks#common-input-fields |
| Per-parent trust | [UNVERIFIED]broad accept not named-parent interface; https://code.claude.com/docs/en/settings-reference#crosssessioninbound |
| Fail-closed installation/timeout/ordering | [UNVERIFIED live]source registration no onFailure:block; installation/order not exercised; https://code.claude.com/docs/en/hooks#userpromptsubmit |
| Human vs peer approval envelope | [UNVERIFIED]local approvaltext parser/inboundevent warrants verification, no exploit demonstrated; https://code.claude.com/docs/en/hooks#userpromptsubmit ; https://code.claude.com/docs/en/cross-session-messaging#how-a-session-treats-an-incoming-message |
| Exact mode equality required | External-doc contradiction to this interpretation (raw return labels CODE-CONTRADICTED); two classes/special plan case, not localruntime proof; https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages |
| All executable forms blocked/all reads exempt | [CODE-CONTRADICTED blanketclaim]G:450-478/K:107,110,151 preserve narrower corrections, no alternate-spelling test; localbaseline plus https://code.claude.com/docs/en/cross-session-messaging#message-delivery |
| Complete typed/grant/file protocol | [UNVERIFIED]schema/replay/identity/safe parsing not supplied by texttransport; https://code.claude.com/docs/en/cross-session-messaging#limitations |
| End-to-end hierarchy/recovery | [UNVERIFIED]eligibility/scopedfanout/parentfailure/admission/humanescalation remain; https://code.claude.com/docs/en/cross-session-messaging#how-a-session-treats-an-incoming-message |

## Key External Findings
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
- HIGH/HIGH/extends: question2 documented yes, hook covers another session's mainconversation message and can block. Deployment/trusted metadata not proved. https://code.claude.com/docs/en/hooks#userpromptsubmit
- HIGH/HIGHinterface/extends: question1 supported controls known, exact class-identification protocol unresolved. https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages
- HIGH/HIGH/qualifies: classes not exact mode equality, interactive planwithbypassavailable exception. Same source as above.
- HIGH/HIGH/extends: inbound handling separate fromtoolmode, not parent-specificgrant. https://code.claude.com/docs/en/settings-reference#crosssessioninbound
- HIGH/HIGH/supports: team sent=successfulmailboxwrite; peerhold/drop/expire differs, neither application/taskcompletion. https://code.claude.com/docs/en/agent-teams#architecture ; https://code.claude.com/docs/en/cross-session-messaging#message-delivery
- HIGH/HIGH/supports: acceptance/modealignment/signing not humanconsent or routearounddenials. https://code.claude.com/docs/en/cross-session-messaging#how-a-session-treats-an-incoming-message
- HIGH/HIGH/supports: internal subagents, teams and independent peers not same hierarchy protocol. https://code.claude.com/docs/en/sub-agents ; https://code.claude.com/docs/en/agent-teams#limitations

## Recommendations from External Research
<!-- web-provenance: provider=WebSearch reason=tavily-unavailable -->
1. Do not make all sessions bypass bydefault tofixholds; inbound choice only under explicit approvedsettings/securityscope, no changes here. HIGH relevance, HIGH sourcebasis, extends. https://code.claude.com/docs/en/settings-reference#crosssessioninbound ; https://code.claude.com/docs/en/permission-modes
2. Update decisionevidence: inboundhook documentedyes/deploymentsecurityunverified, sendercontrols known/internalprotocol unresolved. HIGH/HIGH/extends. https://code.claude.com/docs/en/hooks#userpromptsubmit ; https://code.claude.com/docs/en/cross-session-messaging#control-inbound-messages
3. Keep external-middle authority gated: trustedparent/scope, failclosedvalidation, aggregateadmission, parentfailureownership and human-onlydecisions remain. HIGH/HIGH/supports. https://code.claude.com/docs/en/cross-session-messaging#how-a-session-treats-an-incoming-message
4. Separate send/receive/apply/complete evidence; idle/sent not admission. HIGH/HIGH/supports. https://code.claude.com/docs/en/agent-teams#architecture ; https://code.claude.com/docs/en/cross-session-messaging#message-delivery ; https://code.claude.com/docs/en/cross-session-messaging#get-a-notice-when-another-session-goes-idle
5. Preserve guard recognition/required-probe corrections: launch, communication and supervision separate; no universal executable claim or permission inference. HIGH/directlocalverification/supports. https://code.claude.com/docs/en/cross-session-messaging#message-delivery
No implementation, permission/hook change, worker launch or live trial follows. Full raw findings remain mandatory evidence, including all detailed mechanism guarantees and uncertainty qualifiers.
