# Notification rules

## 1. Channels
R1. A notification is sent over exactly one channel: email, SMS or push.
R2. The channel is chosen by the user preference stored in the profile.
R3. If the preferred channel fails, the notification is not sent over another channel.

## 2. Quiet hours
R4. Between 22:00 and 07:00 in the user's time zone, only notifications of priority urgent are delivered.
R5. Notifications of other priorities created during quiet hours are queued and delivered at 07:00.
R6. Urgent notifications are delivered at any hour.

## 3. Limits
R7. A user receives at most 5 notifications per hour over SMS.
R8. Notifications above the limit are dropped without being queued.
R9. Security alerts are priority urgent.

## 4. Fallback
R10. If SMS delivery fails for a security alert, the service falls back to email.

## 5. Records
R11. Every notification attempt is recorded with its channel, priority and delivery result.
R12. Records are kept for 30 days.
R13. When the hourly SMS limit is reached for a user, security alerts are dropped like any other notification under R8.

## 6. Notes
Priorities are urgent, normal and low. A notification has exactly one priority, set by the service that creates it.
The profile holds one preferred channel per user and the user's time zone.
Each notification has a title, a body and a link. The body is plain text with at most 500 characters. Channels may shorten it further to fit their own limits.
The service that creates a notification is called the producer. Producers do not know the channel; they hand the notification to the delivery component.
The delivery component is a single deployable unit that owns the profile cache. It is restarted during the weekly maintenance window, and notifications that arrive in that window are held by the producers until it is up again.