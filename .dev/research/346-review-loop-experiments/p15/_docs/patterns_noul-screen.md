> ## Documentation Index
> Fetch the complete documentation index at: https://docs.typesafe.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Screen with a Noul first

> Ask one yes/no question first, and run the expensive step only when the answer is a clear yes.

Not every input needs your expensive step. Ask one Noul question first, with a small state such as the input on its own, and run the expensive step only when the answer is a clear yes. A clear no gets cheaper handling, and an answer it can't settle gets a rule of its own, so every input ends up handled.

![An inbox of messages flows toward one Noul question. Each message is held while the question is answered, then takes one of three exits: a clear no is filed away, an unsettled answer is set aside for a quick look, and a clear yes continues into the full triage request with its customer record attached.](https://mintcdn.com/ts-docs/0mdJYbuyjcLi9rbO/patterns/noul-screen-hero-light.gif?s=156a517da1ccc828140f49adf6c59fcd)

## When to screen first

Jev answers all the questions in a request in parallel and reads the state once, so you pay for the state once. If the later questions would use the same state, don't split them off: send them all in one request and let your code ignore the answers that don't apply, we call this pattern [speculative fan-out](https://docs.typesafe.ai/patterns/fan-out.md). Asking first is worth the extra request when the later step costs something the first question doesn't:

* **A bigger state.** The next step needs the customer record, the full thread, or an attachment that code has to fetch first.
* **A slower model.** The next step is an LLM call.
* **A person.** The next step needs someone to look at the item.

## Example: triaging a shared inbox

Say you're building a shared-inbox tool. Everything arrives in one stream: customers asking about orders, newsletters, payment receipts, thank-you notes, and the occasional "just so you know". Full triage means fetching the sender's account and order history, then asking several questions about the message. A Noul question that sees only the message, as it arrived, can decide which messages get full triage.

### Ask whether the sender expects a reply

We ask one thing the message alone can settle: is the sender waiting for a reply? Instead of saying "not waiting", the `false` criterion lists the kinds of message with nothing to answer, including a note from a person that needs no reply.

Try it in the Playground →

Tom's message reports a problem but asks for nothing: the desk is already built, and the message doesn't say whether Tom wants to hear back. The answer is neither a clear yes nor a clear no:

```json theme={null}
{
  "model": "jev-1.14.0",
  "answers": {
    "expects_reply": {
      "type": "noul",
      "noul": 0.44
    }
  },
  "usage": {
    "input_tokens": 414,
    "output_tokens": 21
  }
}
```

Jev's answers to the same question for five different messages:

| Message | `expects_reply` |
| - | - |
| "I ordered a standing desk two weeks ago and the tracking hasn't updated... I'm moving on the 30th and need it before then." | 0.98 |
| "Just so you know, the desk arrived with one of the cross-bar screws missing. I had a spare so it's built now." | 0.44 |
| "Thanks, the desk arrived yesterday and it's great." | 0.10 |
| "20% off every desk and chair until Sunday. Unsubscribe \| View in browser" | 0.02 |
| "Your payment of \$129.00 was successful... replies to this address are not monitored." | 0.02 |

### Handle yes, no and unsure

Compare the Noul with two thresholds: above 0.7 counts as yes, and below 0.3 counts as no. Both are good starting points. An answer between them means the message doesn't settle the question, so give it its own outcome instead of rounding it to yes or no.

```python title="screen.py" theme={null}
YES_ABOVE = 0.7
NO_BELOW = 0.3


def handle(message_id, screen_response):
    expects_reply = screen_response.answers["expects_reply"].noul

    if expects_reply < NO_BELOW:
        # Newsletters, receipts, notifications. Nothing to answer.
        file_away(message_id)

    elif expects_reply > YES_ABOVE:
        # A person is waiting. Fetch what triage needs and run the full request.
        customer = fetch_customer(message_id)
        triage(message_id, customer)

    else:
        # Something to look at, but maybe nothing to answer. One glance settles it.
        queue_for_quick_look(message_id)
```

Of the five messages above, one leads to a triage request: the standing desk that hasn't arrived. The thank-you note and the two automated messages are filed away, and the missing-screw note goes to a person for a quick look.

### Triage only the messages that need a reply

Fetch the customer record only for messages with a clear yes. The triage request sends the record with the message and asks questions that each check one thing: `repeat_contact` reads `customer.previous_contacts`, and `urgency` counts from `message.received`. A real triage stage would ask more questions than this.

Try it in the Playground →

Jev's response:

```json theme={null}
{
  "model": "jev-1.14.0",
  "answers": {
    "request": {
      "type": "choice",
      "choice": "order_status",
      "confidence": 1.0,
      "probabilities": {
        "order_status": 1.0,
        "return_or_refund": 0.0,
        "product_question": 0.0,
        "complaint": 0.0
      }
    },
    "urgency": {
      "type": "score",
      "score": 1.99,
      "confidence": 0.98,
      "legend": {
        "0": "No deadline is mentioned",
        "1": "The sender wants an answer soon but gives no date",
        "2": "The sender names a date or event within a week"
      },
      "probabilities": {
        "0": 0.0,
        "1": 0.01,
        "2": 0.99
      }
    },
    "repeat_contact": {
      "type": "noul",
      "noul": 0.99
    }
  },
  "usage": {
    "input_tokens": 803,
    "output_tokens": 84
  }
}
```

The `repeat_contact` answer comes from the record: with no previous contacts on file, the same message got 0.05.

From here, your routing code acts on the answers. Dana's urgent, repeated order-status request could go to the front of the queue.

## Other ways to screen

* **Check a cheap step first.** Run the cheap step, ask a Noul whether its output is right, and send only the outputs that fail that check to the expensive model.
* **Several screens.** A content pipeline might check first for "written in English" and then for "about our product". Each check removes inputs before the next, more expensive step.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.