# Phase 4 -- Frontend and Logout

**Phase Goal:** Deliver the React v1.0 login/register/profile/password UI surface with secure HttpOnly refresh-cookie + in-memory access-token pattern, silent refresh interceptor, 401 auto-retry, a11y + error UX, and logout endpoint/control -- completing the client-facing half of M4.

**Task Count:** 18 (T04.01 - T04.18)

---

## T04.01 -- COMP-001 LoginPage React component

- **Roadmap Item IDs:** R-056
- **Why:** Primary user-facing login surface; wires POST /auth/login and handles 401/423 error copy.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0057
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0057/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0057 `frontend/src/pages/LoginPage.tsx` + test + styles; posts to /auth/login and routes to /profile on success.

**Steps:**
1. **[PLANNING]** Confirm frontend framework is React + Vite per repo convention.
2. **[EXECUTION]** Implement form with React Hook Form + Zod.
3. **[EXECUTION]** Handle 200, 401, 423 responses with localized strings.
4. **[EXECUTION]** Store access token in memory and refresh cookie via /auth endpoint.
5. **[VERIFICATION]** Component test covers submit + error states.
6. **[COMPLETION]** Update router registration.

**Acceptance Criteria:**
- Happy path navigates to /profile on 200.
- 401 surfaces generic error; 423 surfaces lockout copy.
- No password retained in component state after submit.
- Access token stored in memory only.

**Validation:**
- Manual check: component test suite covering all status codes.
- Evidence: linkable artifact produced (vitest run log).

**Dependencies:** T02.08, T04.08
**Rollback:** Remove route entry.
**Notes:** Uses fetch client with credentials include.

---

## T04.02 -- COMP-002 RegisterPage React component

- **Roadmap Item IDs:** R-057
- **Why:** Registration UI + consent checkbox; completes CONFLICT-2 UI redirect to /login on 201.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth, compliance
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0058
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0058/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0058 `frontend/src/pages/RegisterPage.tsx` with ToS + consent checkbox and 409 handling.

**Steps:**
1. **[PLANNING]** Align copy with Legal for consent text.
2. **[EXECUTION]** Implement form + Zod schema including consent_flag.
3. **[EXECUTION]** Submit to /auth/register; on 201 redirect /login.
4. **[EXECUTION]** On 409 highlight email field with "already registered".
5. **[VERIFICATION]** Component + integration tests (T04.13, T04.16).

**Acceptance Criteria:**
- 201 response triggers redirect to /login.
- 409 displays inline email error.
- Consent checkbox mandatory; 400 if unchecked.
- No tokens stored on register.

**Validation:**
- Manual check: run component tests.
- Evidence: linkable artifact produced (vitest log).

**Dependencies:** T01.10
**Rollback:** Unregister route.
**Notes:** Consent copy flagged for Legal review.

---

## T04.03 -- COMP-003 ProfilePage React component

- **Roadmap Item IDs:** R-058
- **Why:** View/edit profile; uses GET/PUT /profile endpoints.
- **Effort:** M
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0059
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0059/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0059 `frontend/src/pages/ProfilePage.tsx` with display_name edit, save button, success toast.

**Steps:**
1. **[PLANNING]** Fetch profile on mount with auth interceptor.
2. **[EXECUTION]** Implement display_name edit + save.
3. **[VERIFICATION]** Component test loading/empty/error states.

**Acceptance Criteria:**
- Loads profile on mount when authenticated.
- Save persists display_name.
- Error toast on 4xx.
- 401 triggers silent refresh via T04.09.

**Validation:**
- Manual check: component test suite.
- Evidence: linkable artifact produced (vitest log).

**Dependencies:** T03.01, T03.02
**Rollback:** Unregister route.
**Notes:** Reuses shared API client.

---

## T04.04 -- COMP-004 PasswordChangeForm

- **Roadmap Item IDs:** R-059
- **Why:** Inline form invoking /auth/password/change; logs user out on success.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** auth, security
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0060
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0060/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0060 `frontend/src/components/PasswordChangeForm.tsx` with strength meter and logout redirect on success.

**Steps:**
1. **[PLANNING]** Align complexity rules with backend validator.
2. **[EXECUTION]** Implement form with strength indicator.
3. **[EXECUTION]** On 204 redirect to /login (because tokens revoked).
4. **[VERIFICATION]** Component tests.

**Acceptance Criteria:**
- Success triggers redirect to login.
- Weak-password path surfaces inline error.
- Old password required.
- Component test suite green.

**Validation:**
- Manual check: component tests.
- Evidence: linkable artifact produced (vitest log).

**Dependencies:** T03.09
**Rollback:** Unmount component.
**Notes:** UX explicit about session revocation.

---

## T04.05 -- COMP-005 PasswordResetForm two-step flow

- **Roadmap Item IDs:** R-060
- **Why:** UI for reset-request and reset-confirm with single-use token.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth, security
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0061
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0061/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0061 `frontend/src/pages/PasswordResetFlow.tsx` + token-in-query detection.

**Steps:**
1. **[PLANNING]** Two routes /auth/reset and /auth/reset/confirm?token=...
2. **[EXECUTION]** Request form posts email; confirm form reads query token.
3. **[VERIFICATION]** Component tests for both steps.

**Acceptance Criteria:**
- Reset-request step returns generic success copy.
- Confirm step posts token + new password; on 204 redirect /login.
- Invalid token shows contextual error copy.
- Flow is a11y-audited by T04.12.

**Validation:**
- Manual check: component tests for both steps.
- Evidence: linkable artifact produced (vitest log).

**Dependencies:** T03.10, T03.11
**Rollback:** Unregister routes.
**Notes:** Shares API client with profile pages.

---

Checkpoint: Phase 4 / Tasks 1-5

- **Purpose:** Confirm primary UI surface renders and happy-path flows work before security/interceptor work.
- **Verification:**
  - Login/Register/Profile/PasswordChange/Reset pages render and submit.
  - Component test suite green.
  - OpenAPI types current.
- **Exit Criteria:**
  - No UI page missing tests.
  - Redirect behaviors match backend contracts.
  - No dev-only console warnings.

---

## T04.06 -- COMP-006 AuthGuard router component

- **Roadmap Item IDs:** R-061
- **Why:** Route guard gating protected UI areas behind valid session.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0062
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0062/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0062 `frontend/src/router/AuthGuard.tsx` wrapping routes and redirecting to /login when no session.

**Steps:**
1. **[PLANNING]** Define session predicate (memory access token presence).
2. **[EXECUTION]** Wrap protected routes in <AuthGuard>.
3. **[EXECUTION]** Redirect to /login preserving returnTo query.
4. **[VERIFICATION]** Component + integration tests.

**Acceptance Criteria:**
- Protected routes redirect to /login when unauthenticated.
- returnTo query preserved across redirect.
- Authenticated users not redirected on refresh.
- Component tests cover guard + silent refresh path.

**Validation:**
- Manual check: protected route without token -> /login.
- Evidence: linkable artifact produced (test log).

**Dependencies:** T04.08, T04.09
**Rollback:** Remove guard wrap.
**Notes:** Silent refresh (T04.09) resolves transient 401.

---

## T04.07 -- SEC-HTTPONLY Refresh cookie pattern

- **Roadmap Item IDs:** R-062
- **Why:** HttpOnly + SameSite refresh cookie reduces XSS risk; backend writes cookie on login.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** security, auth
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`, `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0063
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0063/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0063 Backend /auth/login and /auth/refresh set `refresh_token` HttpOnly; SameSite=Strict; Secure; Path=/auth/refresh.

**Steps:**
1. **[PLANNING]** Confirm cookie domain and path strategy.
2. **[EXECUTION]** Issue cookie on /auth/login response.
3. **[EXECUTION]** Verify cookie used on /auth/refresh; reject body-only refresh in v1.
4. **[VERIFICATION]** Integration test asserts cookie flags.

**Acceptance Criteria:**
- Cookie flags HttpOnly, Secure, SameSite=Strict, Path=/auth/refresh.
- Refresh handler reads from cookie.
- Cookie cleared on logout.
- Integration test asserts presence via Set-Cookie header.

**Validation:**
- Manual check: inspect Set-Cookie on /auth/login.
- Evidence: linkable artifact produced (integration log).

**Dependencies:** T02.06, T02.07
**Rollback:** Revert cookie issuance.
**Notes:** Client uses credentials: 'include' on fetch.

---

## T04.08 -- SEC-MEMSTORE In-memory access token

- **Roadmap Item IDs:** R-063
- **Why:** Access token held in memory only; prevents localStorage XSS exfiltration.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** security, auth
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `security/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0064
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0064/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0064 `frontend/src/auth/token-store.ts` module-private access token with getter/setter and no persistence.

**Steps:**
1. **[PLANNING]** Confirm no localStorage or sessionStorage usage.
2. **[EXECUTION]** Implement module-scope variable with getters.
3. **[VERIFICATION]** Test asserts token undefined after page reload.

**Acceptance Criteria:**
- Access token never written to storage APIs.
- Reload clears memory store.
- Clear on logout.
- No token leaked to Redux devtools logs.

**Validation:**
- Manual check: reload and inspect storage.
- Evidence: linkable artifact produced (browser capture).

**Dependencies:** T04.01
**Rollback:** Revert to previous store implementation.
**Notes:** Key input to silent refresh flow (T04.09).

---

## T04.09 -- FEAT-SILENTREF Silent refresh interceptor

- **Roadmap Item IDs:** R-064
- **Why:** Automatically refreshes access token before expiry so users avoid re-login during 15m window.
- **Effort:** M
- **Risk:** Medium
- **Risk Drivers:** auth, security
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0065
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0065/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0065 `frontend/src/auth/silent-refresh.ts` timer scheduler refreshing access token at 80% TTL.

**Steps:**
1. **[PLANNING]** Decode token expiry without storing claims.
2. **[EXECUTION]** Schedule setTimeout at exp - 180s.
3. **[EXECUTION]** On fire, POST /auth/refresh; update in-memory token.
4. **[VERIFICATION]** Playwright scenario T04.14 proves seamless refresh.

**Acceptance Criteria:**
- Refresh fires before expiry every session.
- Failed refresh clears token and redirects to /login.
- No duplicate refresh under concurrency.
- Covered by E2E-REFRESH.

**Validation:**
- Manual check: observe network tab for /auth/refresh before 15m.
- Evidence: linkable artifact produced (Playwright trace).

**Dependencies:** T04.08, T02.07
**Rollback:** Disable scheduler via feature flag.
**Notes:** Concurrency guard to avoid multi-refresh.

---

## T04.10 -- FEAT-401INT axios 401 response interceptor

- **Roadmap Item IDs:** R-065
- **Why:** On 401, attempt refresh then retry original request; only redirects if refresh fails.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** auth, security
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0066
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0066/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0066 `frontend/src/api/client.ts` axios interceptor retrying once after refresh.

**Steps:**
1. **[PLANNING]** Ensure interceptor avoids infinite retry loop.
2. **[EXECUTION]** On 401, pause request queue, attempt refresh, resume or reject.
3. **[VERIFICATION]** Unit test interceptor retry behavior.

**Acceptance Criteria:**
- 401 triggers refresh once and retries original request.
- Second 401 after refresh logs user out.
- Concurrent 401s share single refresh call.
- Unit tests cover success/failure.

**Validation:**
- Manual check: simulate 401 via mock server.
- Evidence: linkable artifact produced (vitest log).

**Dependencies:** T04.09
**Rollback:** Remove interceptor.
**Notes:** Keeps UX smooth during key rotation.

---

Checkpoint: Phase 4 / Tasks 6-10

- **Purpose:** Confirm frontend security primitives before UX + analytics polish.
- **Verification:**
  - AuthGuard redirects unauthenticated users.
  - HttpOnly cookie issued on login.
  - Silent refresh + 401 interceptor rotate tokens transparently.
- **Exit Criteria:**
  - Tests for T04.06-T04.10 green.
  - No tokens persisted to storage APIs.
  - All STRICT UI primitives verified.

---

## T04.11 -- UI-ERR ErrorBoundary + toast system

- **Roadmap Item IDs:** R-066
- **Why:** Centralized error display (boundary + toasts) for network/auth errors.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential, Context7
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0067
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0067/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0067 `frontend/src/ui/ErrorBoundary.tsx` + `toast.ts` helpers; wired into root App.

**Steps:**
1. **[PLANNING]** Align with existing design system.
2. **[EXECUTION]** Implement boundary with fallback copy and reload CTA.
3. **[EXECUTION]** Toast helper dispatches global events.
4. **[VERIFICATION]** Storybook + component tests.

**Acceptance Criteria:**
- Uncaught render error shows fallback UI.
- Toast helper emits assertive role for a11y.
- Toasts dismissible via keyboard.
- Storybook entries included.

**Validation:**
- Manual check: run Storybook + component tests.
- Evidence: linkable artifact produced (vitest + SB build log).

**Dependencies:** T04.01
**Rollback:** Remove boundary wrap.
**Notes:** Re-used by Phase 5 admin UI.

---

## T04.12 -- UI-A11Y WCAG 2.1 AA audit pass

- **Roadmap Item IDs:** R-067
- **Why:** Accessibility gate for auth pages (tab order, contrast, ARIA, errors).
- **Effort:** M
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0068
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0068/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0068 axe-core + Playwright a11y audit report with zero serious/critical findings.

**Steps:**
1. **[PLANNING]** Identify target pages (login, register, profile, password, reset).
2. **[EXECUTION]** Run axe-core through Playwright.
3. **[EXECUTION]** Fix flagged issues.
4. **[VERIFICATION]** Re-run and capture report.

**Acceptance Criteria:**
- Zero serious/critical axe findings.
- Keyboard tab order matches visual order.
- Color contrast >=4.5:1 on primary text.
- Report committed at evidence path.

**Validation:**
- Manual check: run axe-core CLI against staging.
- Evidence: linkable artifact produced (a11y report html).

**Dependencies:** T04.01-T04.05
**Rollback:** Revert failing page commits.
**Notes:** Covers all auth pages + logout control.

---

## T04.13 -- TEST-006 Frontend component test suite

- **Roadmap Item IDs:** R-068
- **Why:** Vitest + Testing Library coverage >=80% for auth components.
- **Effort:** M
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0069
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0069/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0069 Component tests for LoginPage, RegisterPage, ProfilePage, PasswordChangeForm, PasswordResetFlow, AuthGuard, LogoutControl.

**Steps:**
1. **[PLANNING]** Enumerate per-component test matrix.
2. **[EXECUTION]** Author tests with Testing Library semantic queries.
3. **[VERIFICATION]** Coverage threshold >=80% enforced.

**Acceptance Criteria:**
- Coverage >=80% for auth namespace.
- Error + loading + happy path tested per component.
- CI enforces threshold.
- Report path recorded.

**Validation:**
- Manual check: run `vitest --coverage`.
- Evidence: linkable artifact produced (coverage report).

**Dependencies:** T04.01-T04.06, T04.18
**Rollback:** Lower threshold only with approval.
**Notes:** CI gate in pipeline.

---

## T04.14 -- E2E-REFRESH Playwright silent refresh scenario

- **Roadmap Item IDs:** R-069
- **Why:** Asserts silent refresh sustains session during 20-minute browser-run scenario.
- **Effort:** M
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [████████--] 80%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0070
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0070/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0070 `frontend/e2e/refresh.spec.ts` Playwright scenario observing at least one /auth/refresh round-trip in 20m.

**Steps:**
1. **[PLANNING]** Use time-travel helper to fast-forward clock.
2. **[EXECUTION]** Login, idle 14m, observe refresh, continue navigation.
3. **[VERIFICATION]** Assert /auth/refresh response 200.

**Acceptance Criteria:**
- Scenario green with recorded refresh request.
- No unexpected logout observed.
- Network HAR file captured at evidence path.
- Test runtime < 10 min in CI.

**Validation:**
- Manual check: `playwright test refresh.spec.ts`.
- Evidence: linkable artifact produced (Playwright trace).

**Dependencies:** T04.09
**Rollback:** Remove spec.
**Notes:** Uses fake timers to keep CI budget sane.

---

## T04.15 -- E2E-LOGOUT Playwright logout scenario

- **Roadmap Item IDs:** R-070
- **Why:** Verifies /auth/logout clears refresh cookie and access token.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [████████--] 80%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0071
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0071/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0071 `frontend/e2e/logout.spec.ts` asserting cookie + memory token cleared on logout.

**Steps:**
1. **[PLANNING]** Seed user; login via UI.
2. **[EXECUTION]** Click LogoutControl; verify redirect to /login.
3. **[EXECUTION]** Assert refresh cookie cleared via response headers.
4. **[VERIFICATION]** Attempt reload and confirm /login remains.

**Acceptance Criteria:**
- Logout button visible post-login.
- Click triggers POST /auth/logout 204.
- Refresh cookie expired on response.
- Reload stays on /login.

**Validation:**
- Manual check: `playwright test logout.spec.ts`.
- Evidence: linkable artifact produced (Playwright trace).

**Dependencies:** T04.17, T04.18
**Rollback:** Remove spec.
**Notes:** Pair with T04.14.

---

Checkpoint: Phase 4 / Tasks 11-15

- **Purpose:** Validate UX, a11y, and test coverage before logout + analytics.
- **Verification:**
  - A11y audit zero serious/critical findings.
  - Component coverage >=80%.
  - Silent refresh + logout E2E pass.
- **Exit Criteria:**
  - No open STANDARD defect.
  - Playwright traces stored.
  - Error boundary tested.

---

## T04.16 -- FUNNEL-REG Registration funnel analytics

- **Roadmap Item IDs:** R-071
- **Why:** Emits analytics events (started/submitted/succeeded/failed) to measure registration conversion.
- **Effort:** S
- **Risk:** Low
- **Risk Drivers:** (none matched)
- **Tier:** STANDARD
- **Confidence:** [███████---] 75%
- **Requires Confirmation:** No
- **Critical Path Override:** No
- **Verification Method:** Direct test execution (30s)
- **MCP Required:** None
- **MCP Preferred:** Sequential
- **Fallback Allowed:** Yes
- **Sub-Agent Delegation:** None
- **Deliverable IDs:** D-0072
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0072/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0072 Analytics events emitted at RegisterPage lifecycle; consent-gated per GDPR.

**Steps:**
1. **[PLANNING]** Confirm analytics SDK and consent check.
2. **[EXECUTION]** Emit events with user-less props only.
3. **[VERIFICATION]** Test fires events through mocked SDK.

**Acceptance Criteria:**
- Four events emitted: started, submitted, succeeded, failed.
- No PII in event payload.
- Events suppressed if consent not granted.
- Event names documented in notes.md.

**Validation:**
- Manual check: unit test verifies emission sequence.
- Evidence: linkable artifact produced (unit log).

**Dependencies:** T04.02
**Rollback:** Strip emitter calls.
**Notes:** Enables success-metric dashboards.

---

## T04.17 -- API-007 POST /auth/logout endpoint

- **Roadmap Item IDs:** R-072
- **Why:** Backend endpoint invalidates refresh cookie and optionally individual refresh token family.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** auth, security
- **Tier:** STRICT
- **Confidence:** [█████████-] 90%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0073
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0073/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0073 `/auth/logout` handler revoking refresh token and clearing cookie; 204 on success.

**Steps:**
1. **[PLANNING]** Decide all-sessions vs single-session default (committed default: single session).
2. **[EXECUTION]** Read refresh token from cookie; revoke via TokenManager.revokeByFamily.
3. **[EXECUTION]** Clear Set-Cookie with expired date.
4. **[VERIFICATION]** Contract test 204.

**Acceptance Criteria:**
- 204 on success.
- Refresh cookie cleared via Set-Cookie.
- Redis entry revoked.
- Audit event logout emitted.

**Validation:**
- Manual check: run contract test.
- Evidence: linkable artifact produced (contract log).

**Dependencies:** T02.04, T04.07
**Rollback:** Unregister route.
**Notes:** Logout-all-sessions is roadmap follow-up.

---

## T04.18 -- COMP-016 LogoutControl React component

- **Roadmap Item IDs:** R-073
- **Why:** UI button + menu item triggering /auth/logout and redirect to /login.
- **Effort:** S
- **Risk:** Medium
- **Risk Drivers:** auth
- **Tier:** STRICT
- **Confidence:** [████████--] 85%
- **Requires Confirmation:** No
- **Critical Path Override:** Yes (paths contain `auth/`)
- **Verification Method:** Sub-agent (quality-engineer, 60s)
- **MCP Required:** Sequential, Serena
- **MCP Preferred:** Context7
- **Fallback Allowed:** No
- **Sub-Agent Delegation:** Required
- **Deliverable IDs:** D-0074
- **Artifacts:** TASKLIST_ROOT/artifacts/D-0074/spec.md, notes.md, evidence.md

**Deliverables:**
1. D-0074 `frontend/src/components/LogoutControl.tsx` with accessible label and keyboard support.

**Steps:**
1. **[PLANNING]** Ensure consistent copy with header component.
2. **[EXECUTION]** Implement button posting to /auth/logout + token clearing.
3. **[EXECUTION]** Redirect to /login on success.
4. **[VERIFICATION]** Component test covers keyboard activation.

**Acceptance Criteria:**
- Accessible label "Log out".
- Keyboard Enter/Space triggers action.
- On success redirect to /login.
- 5xx shows toast + retries manually.

**Validation:**
- Manual check: component test + a11y audit.
- Evidence: linkable artifact produced (vitest log).

**Dependencies:** T04.17, T04.11
**Rollback:** Unmount component.
**Notes:** Keyboard and screen-reader behavior covered in a11y suite.

---

Checkpoint: End of Phase 4

- **Purpose:** Confirm user-facing half of M4 is demo-ready.
- **Verification:**
  - All frontend E2E pass.
  - Logout clears cookie + token store.
  - A11y + coverage green.
- **Exit Criteria:**
  - User can self-service login/register/profile/password/reset/logout.
  - No STRICT UI defect.
  - Phase 5 admin + observability ready to start.
