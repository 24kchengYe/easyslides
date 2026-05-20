# Academic Orchestration

Use this reference before planning with `academic_general` or `academic_scqa`.

The principle is adapted from LearnPrompt's Humanize PPT / AST framing:
a deck is not an information container; it is an audience-state transfer
artifact. EasySlides keeps that idea as a planning contract, then renders the
deck through its own SVG-to-PPTX path.

## Audience-State-Transfer

Before choosing slides, answer:

| AST item | Academic planning question |
|---|---|
| Audience | Who is listening, what do they already know, and what do they resist or overlook? |
| Initial state | What would they believe, miss, or be unsure about before the deck? |
| Desired state | What should they understand, trust, or decide after the deck? |
| Core tension | What gap, puzzle, limitation, or disagreement makes the talk worth hearing? |
| Transfer path | How does each slide move the audience one step from initial state to desired state? |

Every content slide should create one audience-state shift. If a page only
stores information, split, remove, or rewrite it until it advances the path.

## SCQA For Academic Decks

SCQA is the default narrative spine for general academic material:

| Phase | Academic role |
|---|---|
| Situation | Establish shared context: field state, research object, known method, dataset, or practical need. |
| Complication | Name the gap: unresolved mechanism, limitation, contradiction, missing evidence, or operational bottleneck. |
| Question | Condense the scientific or technical question into a testable decision point. |
| Answer | Present method, evidence, result, implication, and next step. |

SCQA is a spine, not a table of contents. A phase may span several pages, and
the Answer phase usually needs the most space. For source-faithful academic
work, keep the source's claims and evidence intact while using SCQA only to
arrange the audience path.

## Human-Facing Language

Slide text faces the audience, not the generator. Avoid developer-facing
language such as template, slot, placeholder, executor, renderer, generation,
pipeline, or implementation unless the talk is explicitly about software
development.

Rule phrase for downstream checks: avoid developer-facing language in visible
slide text and speaker-facing plans.

Use:
- claim titles instead of topic labels;
- evidence captions instead of internal notes;
- speaker-intent notes instead of process traces;
- concrete nouns and verbs instead of filler summary voice.

## Template Roles

`academic_general` is the neutral general academic base. It should handle broad
academic talks, course reports, research progress, thesis-adjacent summaries,
and scholarly exchanges when no stronger scenario template is selected.

`academic_scqa` is the structured argument variant. Use it when the material
benefits from visible SCQA progression, technical-report density, method/result
evidence blocks, or a more institutional blue-cyan identity.

Both templates must preserve source faithfulness for papers, theses, and mature
reports. External material can support missing context only when the user asks
for research or supplementation.
