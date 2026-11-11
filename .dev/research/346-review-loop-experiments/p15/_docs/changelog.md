> ## Documentation Index
> Fetch the complete documentation index at: https://docs.typesafe.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Model changelog

> The principal changes in each Jev release.

Each entry lists what changed in a Jev release. For the models you can call today, their prices and context limits, see [Models](https://docs.typesafe.ai/models.md). For the shortcomings that remain, see [Model jaggedness](https://docs.typesafe.ai/model-jaggedness.md).

**Jev 1.14**

October 14, 2026

* Model ID `jev-1.14.0`.
* Better multilingual support.
* New [Box](https://docs.typesafe.ai/primitives/box.md) question type, which finds where something is in an image and answers with a bounding box. Box questions need Jev 1.14.
* [Images](https://docs.typesafe.ai/images.md) can go in the `state`, `instructions`, or `criteria` of a request. This also works on Jev 1.13.
* [Long context](https://docs.typesafe.ai/models.md#long-context) raises both context limits to 262k tokens for requests that send the long-context header. This also works on Jev 1.13.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.