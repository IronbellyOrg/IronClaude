> ## Documentation Index
> Fetch the complete documentation index at: https://docs.typesafe.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Answers and responses

> Read answers, confidence scores, token usage, and available models returned by the TypeSafe API.

## Response

## typesafe\_sdk.SystemOneResponse

`pydantic-model`

Bases: `Response`

Answers grouped by question type with model and usage metadata.

See [System One](https://docs.typesafe.ai/go/system-one.md) for details.

> [!NOTE]
>
> **Show JSON schema:**
>
> > [accordion] Details
> >
> > ```json theme={null}
> > {
> >   "$defs": {
> >     "BoxAnswer": {
> >       "description": "A located box with its confidence.",
> >       "properties": {
> >         "type": {
> >           "const": "box",
> >           "default": "box",
> >           "title": "Type",
> >           "type": "string"
> >         },
> >         "box": {
> >           "$ref": "#/$defs/BoxCoordinates"
> >         },
> >         "confidence": {
> >           "anyOf": [
> >             {
> >               "type": "number"
> >             },
> >             {
> >               "type": "null"
> >             }
> >           ],
> >           "title": "Confidence"
> >         }
> >       },
> >       "required": [
> >         "box",
> >         "confidence"
> >       ],
> >       "title": "BoxAnswer",
> >       "type": "object"
> >     },
> >     "BoxCoordinates": {
> >       "description": "A box's edges as fractions of the image's height (`top`, `bottom`) and width (`left`, `right`).",
> >       "properties": {
> >         "top": {
> >           "description": "Top edge of the box, as a fraction of image height from the top (0-1).",
> >           "examples": [
> >             0.2
> >           ],
> >           "title": "Top",
> >           "type": "number"
> >         },
> >         "bottom": {
> >           "description": "Bottom edge of the box, as a fraction of image height from the top (0-1).",
> >           "examples": [
> >             0.66
> >           ],
> >           "title": "Bottom",
> >           "type": "number"
> >         },
> >         "left": {
> >           "description": "Left edge of the box, as a fraction of image width from the left (0-1).",
> >           "examples": [
> >             0.19
> >           ],
> >           "title": "Left",
> >           "type": "number"
> >         },
> >         "right": {
> >           "description": "Right edge of the box, as a fraction of image width from the left (0-1).",
> >           "examples": [
> >             0.68
> >           ],
> >           "title": "Right",
> >           "type": "number"
> >         }
> >       },
> >       "required": [
> >         "top",
> >         "bottom",
> >         "left",
> >         "right"
> >       ],
> >       "title": "BoxCoordinates",
> >       "type": "object"
> >     },
> >     "ChoiceAnswer": {
> >       "description": "A selected label and its probabilities.\n\nSee the [choice primitive](https://docs.typesafe.ai/go/choice) for details.",
> >       "properties": {
> >         "type": {
> >           "const": "choice",
> >           "default": "choice",
> >           "title": "Type",
> >           "type": "string"
> >         },
> >         "choice": {
> >           "description": "The name of the choice with the highest probability among the question's criteria.",
> >           "examples": [
> >             "angry"
> >           ],
> >           "title": "Choice",
> >           "type": "string"
> >         },
> >         "confidence": {
> >           "description": "Confidence in the selected choice, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain selections for review.",
> >           "examples": [
> >             0.9
> >           ],
> >           "title": "Confidence",
> >           "type": "number"
> >         },
> >         "probabilities": {
> >           "additionalProperties": {
> >             "type": "number"
> >           },
> >           "description": "Probability of each choice in criteria, keyed by choice name, from 0 to 1. Shows how likely the alternatives are; values sum to approximately 1.",
> >           "examples": [
> >             {
> >               "angry": 0.8,
> >               "calm": 0.1,
> >               "excited": 0.1
> >             }
> >           ],
> >           "title": "Probabilities",
> >           "type": "object"
> >         }
> >       },
> >       "required": [
> >         "choice",
> >         "confidence",
> >         "probabilities"
> >       ],
> >       "title": "ChoiceAnswer",
> >       "type": "object"
> >     },
> >     "NoulAnswer": {
> >       "description": "A yes/no answer.\n\nSee the [noul primitive](https://docs.typesafe.ai/go/noul) for details.",
> >       "properties": {
> >         "type": {
> >           "const": "noul",
> >           "default": "noul",
> >           "title": "Type",
> >           "type": "string"
> >         },
> >         "noul": {
> >           "description": "Probability of a yes answer or a true statement, from 0 to 1. Values near 1 favor yes or true, values near 0 favor no or false, and values near 0.5 indicate uncertainty.",
> >           "examples": [
> >             0.98
> >           ],
> >           "title": "Noul",
> >           "type": "number"
> >         }
> >       },
> >       "required": [
> >         "noul"
> >       ],
> >       "title": "NoulAnswer",
> >       "type": "object"
> >     },
> >     "ScoreAnswer": {
> >       "description": "An expected score with its rubric and probabilities.\n\nSee the [score primitive](https://docs.typesafe.ai/go/score) for details.",
> >       "properties": {
> >         "type": {
> >           "const": "score",
> >           "default": "score",
> >           "title": "Type",
> >           "type": "string"
> >         },
> >         "score": {
> >           "description": "Expected score: the probability-weighted average of the rubric levels. May fall between integer levels.",
> >           "examples": [
> >             1.7
> >           ],
> >           "title": "Score",
> >           "type": "number"
> >         },
> >         "confidence": {
> >           "description": "Confidence in the score, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain ratings for review.",
> >           "examples": [
> >             0.9
> >           ],
> >           "title": "Confidence",
> >           "type": "number"
> >         },
> >         "legend": {
> >           "additionalProperties": {
> >             "anyOf": [
> >               {
> >                 "type": "string"
> >               },
> >               {
> >                 "additionalProperties": true,
> >                 "type": "object"
> >               },
> >               {
> >                 "items": {},
> >                 "type": "array"
> >               }
> >             ]
> >           },
> >           "title": "Legend",
> >           "type": "object"
> >         },
> >         "probabilities": {
> >           "additionalProperties": {
> >             "type": "number"
> >           },
> >           "title": "Probabilities",
> >           "type": "object"
> >         }
> >       },
> >       "required": [
> >         "score",
> >         "confidence",
> >         "legend",
> >         "probabilities"
> >       ],
> >       "title": "ScoreAnswer",
> >       "type": "object"
> >     },
> >     "Usage": {
> >       "description": "Token counts for a request, when reported by the API.",
> >       "properties": {
> >         "input_tokens": {
> >           "anyOf": [
> >             {
> >               "type": "integer"
> >             },
> >             {
> >               "type": "null"
> >             }
> >           ],
> >           "default": null,
> >           "title": "Input Tokens"
> >         },
> >         "output_tokens": {
> >           "anyOf": [
> >             {
> >               "type": "integer"
> >             },
> >             {
> >               "type": "null"
> >             }
> >           ],
> >           "default": null,
> >           "title": "Output Tokens"
> >         }
> >       },
> >       "title": "Usage",
> >       "type": "object"
> >     }
> >   },
> >   "description": "Answers grouped by question type with model and usage metadata.\n\nSee [System One](https://docs.typesafe.ai/go/system-one) for details.",
> >   "properties": {
> >     "model": {
> >       "title": "Model",
> >       "type": "string"
> >     },
> >     "usage": {
> >       "$ref": "#/$defs/Usage"
> >     },
> >     "answers": {
> >       "additionalProperties": {
> >         "discriminator": {
> >           "mapping": {
> >             "box": "#/$defs/BoxAnswer",
> >             "choice": "#/$defs/ChoiceAnswer",
> >             "noul": "#/$defs/NoulAnswer",
> >             "score": "#/$defs/ScoreAnswer"
> >           },
> >           "propertyName": "type"
> >         },
> >         "oneOf": [
> >           {
> >             "$ref": "#/$defs/NoulAnswer"
> >           },
> >           {
> >             "$ref": "#/$defs/ChoiceAnswer"
> >           },
> >           {
> >             "$ref": "#/$defs/ScoreAnswer"
> >           },
> >           {
> >             "$ref": "#/$defs/BoxAnswer"
> >           }
> >         ]
> >       },
> >       "title": "Answers",
> >       "type": "object"
> >     }
> >   },
> >   "required": [
> >     "model",
> >     "usage"
> >   ],
> >   "title": "SystemOneResponse",
> >   "type": "object"
> > }
> > ```

Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `model` (`str`)
* `usage` (`Usage`)
* `answers` (`dict[str, Answer]`)

### request\_id

`cached` `property`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`request\_id

  :

  &#x20;

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)\`
</pre>

The `x-typesafe-request-id` response header.

### raw\_http\_response

`property`

```python theme={null}
raw_http_response: httpx2.Response
```

The underlying `httpx2.Response`, exposing status, headers, and body.

### model\_config

`class-attribute` `instance-attribute`

```python theme={null}
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

### model

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`model

  :

  &#x20;

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)\`
</pre>

The model used to answer the request.

### usage

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`usage

  :

  &#x20;

  [Usage](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.Usage)\`
</pre>

Token usage for the request.

### answers

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`answers

  :

  &#x20;

  [dict](https://docs.python.org/3/builtins/stdtypes.html#dict)

  \[

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)

  ,

  &#x20;

  [Answer](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.Answer)

  ]\`
</pre>

All answer objects keyed by question name.

### nouls

`cached` `property`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`nouls

  :

  &#x20;

  [dict](https://docs.python.org/3/builtins/stdtypes.html#dict)

  \[

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)

  ,

  &#x20;

  [NoulAnswer](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.NoulAnswer)

  ]\`
</pre>

Yes/no answers keyed by question name.

### choices

`cached` `property`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`choices

  :

  &#x20;

  [dict](https://docs.python.org/3/builtins/stdtypes.html#dict)

  \[

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)

  ,

  &#x20;

  [ChoiceAnswer](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.ChoiceAnswer)

  ]\`
</pre>

Choice answers keyed by question name.

### scores

`cached` `property`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`scores

  :

  &#x20;

  [dict](https://docs.python.org/3/builtins/stdtypes.html#dict)

  \[

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)

  ,

  &#x20;

  [ScoreAnswer](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.ScoreAnswer)

  ]\`
</pre>

Score answers keyed by question name.

### boxes

`cached` `property`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`boxes

  :

  &#x20;

  [dict](https://docs.python.org/3/builtins/stdtypes.html#dict)

  \[

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)

  ,

  &#x20;

  [BoxAnswer](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.BoxAnswer)

  ]\`
</pre>

Box answers keyed by question name.

## typesafe\_sdk.Usage

`pydantic-model`

Bases: `wire.Usage`

Token counts for a request, when reported by the API.

> [!NOTE]
>
> **Show JSON schema:**
>
> > [accordion] Details
> >
> > ```json theme={null}
> > {
> >   "description": "Token counts for a request, when reported by the API.",
> >   "properties": {
> >     "input_tokens": {
> >       "anyOf": [
> >         {
> >           "type": "integer"
> >         },
> >         {
> >           "type": "null"
> >         }
> >       ],
> >       "default": null,
> >       "title": "Input Tokens"
> >     },
> >     "output_tokens": {
> >       "anyOf": [
> >         {
> >           "type": "integer"
> >         },
> >         {
> >           "type": "null"
> >         }
> >       ],
> >       "default": null,
> >       "title": "Output Tokens"
> >     }
> >   },
> >   "title": "Usage",
> >   "type": "object"
> > }
> > ```

Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `input_tokens` (`int | None`)
* `output_tokens` (`int | None`)

### model\_config

`class-attribute` `instance-attribute`

```python theme={null}
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

### input\_tokens

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`input\_tokens

  :

  &#x20;

  [int](https://docs.python.org/3/builtins/functions.html#int)

  &#x20;

  |

  &#x20;

  None

  &#x20;

  \=

  &#x20;

  None\`
</pre>

Number of input tokens used, or `None` when the API did not report it.

### output\_tokens

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`output\_tokens

  :

  &#x20;

  [int](https://docs.python.org/3/builtins/functions.html#int)

  &#x20;

  |

  &#x20;

  None

  &#x20;

  \=

  &#x20;

  None\`
</pre>

Number of output tokens used, or `None` when the API did not report it.

## Answers

## typesafe\_sdk.NoulAnswer

`pydantic-model`

Bases: `wire.NoulAnswer`

A yes/no answer.

See the [noul primitive](https://docs.typesafe.ai/go/noul.md) for details.

> [!NOTE]
>
> **Show JSON schema:**
>
> > [accordion] Details
> >
> > ```json theme={null}
> > {
> >   "description": "A yes/no answer.\n\nSee the [noul primitive](https://docs.typesafe.ai/go/noul) for details.",
> >   "properties": {
> >     "type": {
> >       "const": "noul",
> >       "default": "noul",
> >       "title": "Type",
> >       "type": "string"
> >     },
> >     "noul": {
> >       "description": "Probability of a yes answer or a true statement, from 0 to 1. Values near 1 favor yes or true, values near 0 favor no or false, and values near 0.5 indicate uncertainty.",
> >       "examples": [
> >         0.98
> >       ],
> >       "title": "Noul",
> >       "type": "number"
> >     }
> >   },
> >   "required": [
> >     "noul"
> >   ],
> >   "title": "NoulAnswer",
> >   "type": "object"
> > }
> > ```

Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `noul` (`float`)
* `type` (`Literal['noul']`)

### noul

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`noul

  :

  &#x20;

  [float](https://docs.python.org/3/builtins/functions.html#float)\`
</pre>

Probability of a yes answer or a true statement, from 0 to 1. Values near 1 favor yes or true, values near 0 favor no or false, and values near 0.5 indicate uncertainty.

### model\_config

`class-attribute` `instance-attribute`

```python theme={null}
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

## typesafe\_sdk.ChoiceAnswer

`pydantic-model`

Bases: `wire.ChoiceAnswer`

A selected label and its probabilities.

See the [choice primitive](https://docs.typesafe.ai/go/choice.md) for details.

> [!NOTE]
>
> **Show JSON schema:**
>
> > [accordion] Details
> >
> > ```json theme={null}
> > {
> >   "description": "A selected label and its probabilities.\n\nSee the [choice primitive](https://docs.typesafe.ai/go/choice) for details.",
> >   "properties": {
> >     "type": {
> >       "const": "choice",
> >       "default": "choice",
> >       "title": "Type",
> >       "type": "string"
> >     },
> >     "choice": {
> >       "description": "The name of the choice with the highest probability among the question's criteria.",
> >       "examples": [
> >         "angry"
> >       ],
> >       "title": "Choice",
> >       "type": "string"
> >     },
> >     "confidence": {
> >       "description": "Confidence in the selected choice, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain selections for review.",
> >       "examples": [
> >         0.9
> >       ],
> >       "title": "Confidence",
> >       "type": "number"
> >     },
> >     "probabilities": {
> >       "additionalProperties": {
> >         "type": "number"
> >       },
> >       "description": "Probability of each choice in criteria, keyed by choice name, from 0 to 1. Shows how likely the alternatives are; values sum to approximately 1.",
> >       "examples": [
> >         {
> >           "angry": 0.8,
> >           "calm": 0.1,
> >           "excited": 0.1
> >         }
> >       ],
> >       "title": "Probabilities",
> >       "type": "object"
> >     }
> >   },
> >   "required": [
> >     "choice",
> >     "confidence",
> >     "probabilities"
> >   ],
> >   "title": "ChoiceAnswer",
> >   "type": "object"
> > }
> > ```

Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `choice` (`str`)
* `confidence` (`float`)
* `probabilities` (`dict[str, float]`)
* `type` (`Literal['choice']`)

### choice

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`choice

  :

  &#x20;

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)\`
</pre>

The name of the choice with the highest probability among the question's criteria.

### confidence

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`confidence

  :

  &#x20;

  [float](https://docs.python.org/3/builtins/functions.html#float)\`
</pre>

Confidence in the selected choice, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain selections for review.

### probabilities

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`probabilities

  :

  &#x20;

  [dict](https://docs.python.org/3/builtins/stdtypes.html#dict)

  \[

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)

  ,

  &#x20;

  [float](https://docs.python.org/3/builtins/functions.html#float)

  ]\`
</pre>

Probability of each choice in criteria, keyed by choice name, from 0 to 1. Shows how likely the alternatives are; values sum to approximately 1.

### model\_config

`class-attribute` `instance-attribute`

```python theme={null}
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

## typesafe\_sdk.ScoreAnswer

`pydantic-model`

Bases: `wire.ScoreAnswer`

An expected score with its rubric and probabilities.

See the [score primitive](https://docs.typesafe.ai/go/score.md) for details.

> [!NOTE]
>
> **Show JSON schema:**
>
> > [accordion] Details
> >
> > ```json theme={null}
> > {
> >   "description": "An expected score with its rubric and probabilities.\n\nSee the [score primitive](https://docs.typesafe.ai/go/score) for details.",
> >   "properties": {
> >     "type": {
> >       "const": "score",
> >       "default": "score",
> >       "title": "Type",
> >       "type": "string"
> >     },
> >     "score": {
> >       "description": "Expected score: the probability-weighted average of the rubric levels. May fall between integer levels.",
> >       "examples": [
> >         1.7
> >       ],
> >       "title": "Score",
> >       "type": "number"
> >     },
> >     "confidence": {
> >       "description": "Confidence in the score, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain ratings for review.",
> >       "examples": [
> >         0.9
> >       ],
> >       "title": "Confidence",
> >       "type": "number"
> >     },
> >     "legend": {
> >       "additionalProperties": {
> >         "anyOf": [
> >           {
> >             "type": "string"
> >           },
> >           {
> >             "additionalProperties": true,
> >             "type": "object"
> >           },
> >           {
> >             "items": {},
> >             "type": "array"
> >           }
> >         ]
> >       },
> >       "title": "Legend",
> >       "type": "object"
> >     },
> >     "probabilities": {
> >       "additionalProperties": {
> >         "type": "number"
> >       },
> >       "title": "Probabilities",
> >       "type": "object"
> >     }
> >   },
> >   "required": [
> >     "score",
> >     "confidence",
> >     "legend",
> >     "probabilities"
> >   ],
> >   "title": "ScoreAnswer",
> >   "type": "object"
> > }
> > ```

Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `score` (`float`)
* `confidence` (`float`)
* `type` (`Literal['score']`)
* `legend` (`dict[int, str | dict[str, Any] | list[Any]]`)
* `probabilities` (`dict[int, float]`)

### score

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`score

  :

  &#x20;

  [float](https://docs.python.org/3/builtins/functions.html#float)\`
</pre>

Expected score: the probability-weighted average of the rubric levels. May fall between integer levels.

### confidence

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`confidence

  :

  &#x20;

  [float](https://docs.python.org/3/builtins/functions.html#float)\`
</pre>

Confidence in the score, from 0 to 1. Higher values indicate greater certainty; use lower values to flag uncertain ratings for review.

### model\_config

`class-attribute` `instance-attribute`

```python theme={null}
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

### legend

`pydantic-field`

Copy signature
<pre tabIndex="0" aria-label="SDK signature">`legend: [dict](https://docs.python.org/3/builtins/stdtypes.html#dict)\[
&#x20;   [int](https://docs.python.org/3/builtins/functions.html#int), [str](https://docs.python.org/3/builtins/stdtypes.html#str) | [dict](https://docs.python.org/3/builtins/stdtypes.html#dict)\[[str](https://docs.python.org/3/builtins/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)] | [list](https://docs.python.org/3/builtins/stdtypes.html#list)\[[Any](https://docs.python.org/3/library/typing.html#typing.Any)]
]`</pre>

Rubric descriptions keyed by integer score.

### probabilities

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`probabilities

  :

  &#x20;

  [dict](https://docs.python.org/3/builtins/stdtypes.html#dict)

  \[

  [int](https://docs.python.org/3/builtins/functions.html#int)

  ,

  &#x20;

  [float](https://docs.python.org/3/builtins/functions.html#float)

  ]\`
</pre>

Probabilities keyed by integer score.

## typesafe\_sdk.BoxAnswer

`pydantic-model`

Bases: `wire.BoxAnswer`

A located box with its confidence.

> [!NOTE]
>
> **Show JSON schema:**
>
> > [accordion] Details
> >
> > ```json theme={null}
> > {
> >   "$defs": {
> >     "BoxCoordinates": {
> >       "description": "A box's edges as fractions of the image's height (`top`, `bottom`) and width (`left`, `right`).",
> >       "properties": {
> >         "top": {
> >           "description": "Top edge of the box, as a fraction of image height from the top (0-1).",
> >           "examples": [
> >             0.2
> >           ],
> >           "title": "Top",
> >           "type": "number"
> >         },
> >         "bottom": {
> >           "description": "Bottom edge of the box, as a fraction of image height from the top (0-1).",
> >           "examples": [
> >             0.66
> >           ],
> >           "title": "Bottom",
> >           "type": "number"
> >         },
> >         "left": {
> >           "description": "Left edge of the box, as a fraction of image width from the left (0-1).",
> >           "examples": [
> >             0.19
> >           ],
> >           "title": "Left",
> >           "type": "number"
> >         },
> >         "right": {
> >           "description": "Right edge of the box, as a fraction of image width from the left (0-1).",
> >           "examples": [
> >             0.68
> >           ],
> >           "title": "Right",
> >           "type": "number"
> >         }
> >       },
> >       "required": [
> >         "top",
> >         "bottom",
> >         "left",
> >         "right"
> >       ],
> >       "title": "BoxCoordinates",
> >       "type": "object"
> >     }
> >   },
> >   "description": "A located box with its confidence.",
> >   "properties": {
> >     "type": {
> >       "const": "box",
> >       "default": "box",
> >       "title": "Type",
> >       "type": "string"
> >     },
> >     "box": {
> >       "$ref": "#/$defs/BoxCoordinates"
> >     },
> >     "confidence": {
> >       "anyOf": [
> >         {
> >           "type": "number"
> >         },
> >         {
> >           "type": "null"
> >         }
> >       ],
> >       "title": "Confidence"
> >     }
> >   },
> >   "required": [
> >     "box",
> >     "confidence"
> >   ],
> >   "title": "BoxAnswer",
> >   "type": "object"
> > }
> > ```

Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `type` (`Literal['box']`)
* `box` (`BoxCoordinates`)
* `confidence` (`float | None`)

### model\_config

`class-attribute` `instance-attribute`

```python theme={null}
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

### box

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`box

  :

  &#x20;

  [BoxCoordinates](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.BoxCoordinates)\`
</pre>

The box's edges as fractions of the image's height and width, from 0 to 1.

### confidence

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`confidence

  :

  &#x20;

  [float](https://docs.python.org/3/builtins/functions.html#float)

  &#x20;

  |

  &#x20;

  None\`
</pre>

Confidence for the box, from 0 to 1, or `None` when the model does not provide it.

## typesafe\_sdk.BoxCoordinates

`pydantic-model`

Bases: `wire.BoxCoordinates`

A box's edges as fractions of the image's height (`top`, `bottom`) and width (`left`, `right`).

> [!NOTE]
>
> **Show JSON schema:**
>
> > [accordion] Details
> >
> > ```json theme={null}
> > {
> >   "description": "A box's edges as fractions of the image's height (`top`, `bottom`) and width (`left`, `right`).",
> >   "properties": {
> >     "top": {
> >       "description": "Top edge of the box, as a fraction of image height from the top (0-1).",
> >       "examples": [
> >         0.2
> >       ],
> >       "title": "Top",
> >       "type": "number"
> >     },
> >     "bottom": {
> >       "description": "Bottom edge of the box, as a fraction of image height from the top (0-1).",
> >       "examples": [
> >         0.66
> >       ],
> >       "title": "Bottom",
> >       "type": "number"
> >     },
> >     "left": {
> >       "description": "Left edge of the box, as a fraction of image width from the left (0-1).",
> >       "examples": [
> >         0.19
> >       ],
> >       "title": "Left",
> >       "type": "number"
> >     },
> >     "right": {
> >       "description": "Right edge of the box, as a fraction of image width from the left (0-1).",
> >       "examples": [
> >         0.68
> >       ],
> >       "title": "Right",
> >       "type": "number"
> >     }
> >   },
> >   "required": [
> >     "top",
> >     "bottom",
> >     "left",
> >     "right"
> >   ],
> >   "title": "BoxCoordinates",
> >   "type": "object"
> > }
> > ```

Config:

* `extra`: `ignore`
* `frozen`: `True`
* `strict`: `True`

Fields:

* `top` (`float`)
* `bottom` (`float`)
* `left` (`float`)
* `right` (`float`)

### top

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`top

  :

  &#x20;

  [float](https://docs.python.org/3/builtins/functions.html#float)\`
</pre>

Top edge of the box, as a fraction of image height from the top (0-1).

### bottom

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`bottom

  :

  &#x20;

  [float](https://docs.python.org/3/builtins/functions.html#float)\`
</pre>

Bottom edge of the box, as a fraction of image height from the top (0-1).

### left

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`left

  :

  &#x20;

  [float](https://docs.python.org/3/builtins/functions.html#float)\`
</pre>

Left edge of the box, as a fraction of image width from the left (0-1).

### right

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`right

  :

  &#x20;

  [float](https://docs.python.org/3/builtins/functions.html#float)\`
</pre>

Right edge of the box, as a fraction of image width from the left (0-1).

### model\_config

`class-attribute` `instance-attribute`

```python theme={null}
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

## typesafe\_sdk.Answer

`module-attribute`

Copy signature
<pre tabIndex="0" aria-label="SDK signature">`Answer: [TypeAlias](https://docs.python.org/3/library/typing.html#typing.TypeAlias) = [Annotated](https://docs.python.org/3/library/typing.html#typing.Annotated)\[
&#x20;   [NoulAnswer](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.NoulAnswer)
&#x20;   | [ChoiceAnswer](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.ChoiceAnswer)
&#x20;   | [ScoreAnswer](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.ScoreAnswer)
&#x20;   | [BoxAnswer](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.BoxAnswer),
&#x20;   Field(discriminator="type"),
]`</pre>

An answer to a single question, identified by its `type`.

## Available models

## typesafe\_sdk.ListModelsResponse

`pydantic-model`

Bases: `Response`

The models available to the account.

> [!NOTE]
>
> **Show JSON schema:**
>
> > [accordion] Details
> >
> > ```json theme={null}
> > {
> >   "$defs": {
> >     "ModelMetadata": {
> >       "description": "Metadata describing a single available model.",
> >       "properties": {
> >         "name": {
> >           "title": "Name",
> >           "type": "string"
> >         },
> >         "description": {
> >           "title": "Description",
> >           "type": "string"
> >         },
> >         "release_date": {
> >           "title": "Release Date",
> >           "type": "string"
> >         }
> >       },
> >       "required": [
> >         "name",
> >         "description",
> >         "release_date"
> >       ],
> >       "title": "ModelMetadata",
> >       "type": "object"
> >     }
> >   },
> >   "description": "The models available to the account.",
> >   "properties": {
> >     "models": {
> >       "items": {
> >         "$ref": "#/$defs/ModelMetadata"
> >       },
> >       "title": "Models",
> >       "type": "array"
> >     }
> >   },
> >   "required": [
> >     "models"
> >   ],
> >   "title": "ListModelsResponse",
> >   "type": "object"
> > }
> > ```

Fields:

* `models` (`tuple[ModelMetadata, ...]`)

### request\_id

`cached` `property`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`request\_id

  :

  &#x20;

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)\`
</pre>

The `x-typesafe-request-id` response header.

### raw\_http\_response

`property`

```python theme={null}
raw_http_response: httpx2.Response
```

The underlying `httpx2.Response`, exposing status, headers, and body.

### model\_config

`class-attribute` `instance-attribute`

```python theme={null}
model_config = ConfigDict(
    extra="ignore", frozen=True, strict=True
)
```

### models

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`models

  :

  &#x20;

  [tuple](https://docs.python.org/3/builtins/stdtypes.html#tuple)

  \[

  [ModelMetadata](https://docs.typesafe.ai/sdk/python/api/types/responses.md#typesafe_sdk.ModelMetadata)

  ,

  &#x20;

  ...

  ]\`
</pre>

The available models.

## typesafe\_sdk.ModelMetadata

`pydantic-model`

Bases: `Schema`

Metadata describing a single available model.

> [!NOTE]
>
> **Show JSON schema:**
>
> > [accordion] Details
> >
> > ```json theme={null}
> > {
> >   "description": "Metadata describing a single available model.",
> >   "properties": {
> >     "name": {
> >       "title": "Name",
> >       "type": "string"
> >     },
> >     "description": {
> >       "title": "Description",
> >       "type": "string"
> >     },
> >     "release_date": {
> >       "title": "Release Date",
> >       "type": "string"
> >     }
> >   },
> >   "required": [
> >     "name",
> >     "description",
> >     "release_date"
> >   ],
> >   "title": "ModelMetadata",
> >   "type": "object"
> > }
> > ```

Fields:

* `name` (`str`)
* `description` (`str`)
* `release_date` (`str`)

### name

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`name

  :

  &#x20;

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)\`
</pre>

Model name or alias accepted by a request's model field.

### description

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`description

  :

  &#x20;

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)\`
</pre>

Human-readable description of the model and its capabilities.

### release\_date

`pydantic-field`

Copy signature

<pre tabIndex="0" aria-label="SDK signature">
  \`release\_date

  :

  &#x20;

  [str](https://docs.python.org/3/builtins/stdtypes.html#str)\`
</pre>

Model release date, formatted as YYYY-MM-DD.


This documentation is built and hosted on [Mintlify](https://mintlify.com), a developer documentation platform.