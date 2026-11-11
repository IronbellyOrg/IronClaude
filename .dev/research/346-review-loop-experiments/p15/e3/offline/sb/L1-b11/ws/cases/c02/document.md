# Access control requirements

## 1. Roles
R1. The system has three roles: viewer, editor and admin.
R2. A viewer can read documents but cannot change them.
R3. An editor can create and change documents but cannot delete them.
R4. An admin can do everything an editor can do and can also delete documents and manage users.

## 2. Sessions
R5. A session expires after 30 minutes without activity.
R6. After expiry the user must sign in again before any further request is accepted.
R7. Admin sessions expire after 15 minutes without activity.

## 3. Sharing
R8. A document can be shared by link with people outside the organization only by an admin.
R9. A shared link grants the viewer role on that single document.
R10. Editors may share a document by link with anyone, to speed up collaboration.
R11. Editors may delete documents that they created themselves.

## 4. User management
R12. Only an admin can create, disable or delete a user.
R13. Disabling a user ends all of that user's sessions immediately.
R14. The last remaining admin cannot be disabled or deleted.
R15. When a user is deleted, the documents they own are deleted with them.

## 5. Notes
A document has exactly one owner, the user who created it. Teams share documents by adding people to the document, not by sharing a folder.
Roles are assigned per user for the whole organization; there are no per-document roles.
The role names above are fixed by this document. A user has exactly one role at a time and a new user starts as a viewer.
Requests that arrive without a valid session are answered with an authentication error and nothing else. This document does not cover the content of that error.
The audit trail of role changes is out of scope for this document and is described in the security overview.