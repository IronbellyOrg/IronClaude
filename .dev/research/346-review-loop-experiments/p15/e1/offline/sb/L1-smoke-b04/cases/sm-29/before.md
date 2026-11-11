# Password Reset Flow

Status: Draft for review. Owner: Identity team.

## 1. Purpose

This document specifies how a customer who has forgotten a password can set a new one, and how the reset link is protected against misuse.

## 2. Request

- **PR-1 Request.** A customer asks for a reset on the sign-in page by giving the address of the account. The page answers in the same way whether the account exists or not.
- **PR-2 Delivery.** If the account exists, the service sends one message with a reset link to the address of the account.
- **PR-6 Throttle.** At most three reset requests per account are accepted per hour.

## 3. The link

- **PR-3 One-time use.** A password reset link can be used once. After a successful reset the link stops working.
- **PR-4 Link lifetime.** A password reset link expires 30 minutes after it is sent.
- **PR-5 Token.** The link carries a random token of at least 32 bytes. Only a hash of the token is stored by the service.

## 4. After the reset

- **PR-7 Sessions.** A successful reset ends all sessions of the account.
- **PR-8 Notice.** The customer receives a message that says the password was changed, without the new password.
- **PR-9 Password rules.** The new password must follow the password rules of the account policy and must differ from the last five passwords.
- **PR-10 Support.** Support staff can see that a reset was requested and when, but never see the link, the token or the new password of the customer.
- **PR-11 Locked accounts.** A reset link for an account that is locked by the fraud team is not sent. The page gives the same answer as for an account that does not exist.

## 5. Acceptance criteria

1. A used link cannot be used a second time.
2. A link older than its lifetime is refused.
3. A successful reset ends the other sessions of the account.
