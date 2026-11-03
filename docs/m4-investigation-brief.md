# M4 Investigation Brief

## Product Slice
ST-01: Guess the Secret Number Using Range Hints

## Trace to Product Work
Given the system has picked a secret number between 9 and 100, when the learner enters a guess, then the system displays two numbers and the secret number is between them

## Initial Design Question
**Question type:** Data / State

After each guess, how does the system decide the two numbers it displays, and what state must it remember between guesses so the secret number always stays between them?

## Why This Question Matters
f I code ST-01 before settling how the displayed range is decided and updated, I would be guessing at the core rule. The manual says the secret number is “always somewhere between the two numbers” shown, but it never explains how those two numbers are chosen or whether they narrow after each guess. If I guess wrong, the system could show a range that doesn’t actually contain the secret number, which breaks the one promise this feature makes.

The rule also decides where state lives. If the system must remember the current lower and upper bounds between guesses, that state has to be stored somewhere outside the screen. If I put it in the wrong place, I would have to move it later, and I would also have to rewrite any tests and acceptance criteria that assumed the old place. Settling the rule first is cheaper than reworking code that is already built on a guess.

## Planned Evidence
- Field or state table
- Acceptance-criteria trace

## Why This Evidence Is a Reasonable Starting Point
My question is about what state the system must remember between guesses so the displayed range always contains the secret number. A field/state table shows exactly what must be stored and how it changes after each guess. An acceptance-criteria trace checks that every field supports AC-1 and shows any gap the manual leaves open. An ERD isn’t a good fit because ST-01 has no relationships between separate records, so I may change my plan if the studio shows otherwise.

## Studio Check
During the DataMan Design Studio, record whether the evidence actually answered the question, whether you needed different evidence, and what new question emerged.
