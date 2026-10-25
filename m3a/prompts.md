# AI helper log — M3A Cryo Wake

I used Claude as an AI helper. I had no other player, so I used the Prompt 2N route: the AI asked me the interview questions and I answered as the player. I passed the planning gate myself.

## Stage: plan
Prompt: Interview me as the player (Prompt 2N). Ask the 5 brief questions plus one of your own.
What the AI gave me (one line): Six questions. Its own question (E-06) asked whether I like picking up an item early that I need later.
What I kept, changed, or threw away: [I kept everything it gave me]

## Stage: plan
Prompt: From my answers E-01 to E-06, write user stories in the "As a / I want / so that" shape. Use only things in my answers.
What the AI gave me (one line): Six stories (US1–US6), each tied to one answer, plus two stories for the cut list (US7, US8).
What I kept, changed, or threw away: [I kept everything it gave me]

## Stage: plan
Prompt: Write one yes/no acceptance check for each story that I can test by playing.
What the AI gave me (one line): Six checks based on things I can count or search for (clicks to an ending, links on a page, the word "copy").
What I kept, changed, or threw away: [I kept everything it gave me]

## Stage: plan
Prompt: Draw a Mermaid story map for 8 to 12 passages with at least 2 endings, using my stories.
What the AI gave me (one line): An 11-passage map (8 passages, 3 endings) for a story called Cryo Wake, plus the passage table.
What I kept, changed, or threw away: [I kept everything it gave me]. I said yes at the planning gate.

## Stage: build
Prompt: Part 6: answer my question about the keycard with a state table and the map.
What the AI gave me (one line): A `$hasCard` table and the finding that Bridge without the card gives no clue about where to go. Decision: Revise (add a hint and a Bridge → Locker link).
What I kept, changed, or threw away: [I kept everything it gave me]

## Stage: build
Prompt: Write cryo_wake.twee in Twee 3 / Harlowe 3 from the revised map. Then run story_check.py.
What the AI gave me (one line): The full .twee file. The checker reported 11 passages, 19 links, and no findings.
What I kept, changed, or threw away: [I kept everything it gave me]

## Stage: check
Prompt: Build a playable HTML with Harlowe 3.3.9 and play every path in a browser to test the acceptance checks.
What the AI gave me (one line): `cryo_wake.html` and a run of 6 paths. All checks passed and Harlowe showed 0 errors.
What I kept, changed, or threw away: [I kept everything it gave me]
