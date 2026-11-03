# M4 Design Investigation Record

## Product Slice
ST-01: Guess the Secret Number Using Range Hints

## Initial Question
After each guess, how does the system decide the two numbers it displays, and what state must it remember between guesses so the secret number always stays between them?

## Planned Evidence
Field or state table + acceptance-criteria trace

## Evidence Actually Used
- Use-case boundary / actor-goal framing
- Behavior/state flow and two-attempt simulation
- Data-model/schema and Memory Bank constraint stress tests
- Interface/wireframe comparison and state audit
- Design complication and critique

## Findings
### Use-Case Boundary / Question Framing
Learner → guess the secret number using range hints.
Question: After each guess, what must the system tell the learner about the range so the secret number is always between the two numbers shown, and what must it remember between guesses to keep that true?

### Behavior / State
The evidence answered: The order of steps shows that the system has to record the try number for each submitted answer before it decides whether the answer is correct. The right response to a wrong answer depends on that count: on try 1 it shows EEE and allows a retry, and on try 2 it shows EEE and then reveals the answer. Revealing the answer is therefore gated on “wrong and try 2,” not on “wrong.” This matches Answer Checker (Operating Notes), where the correct result is shown only after two wrong tries.

### Data / Persistence
What the model made visible that a screen sketch would not: A screen sketch shows one moment, such as a problem on screen, an EEE, or a score. The data model shows what has to be remembered between moments, and who owns each rule. Stress-testing it brought out four things a sketch would hide: Attempts are separate events, Set membership is a relationship, The 10-problem limit belongs below the screen, Results must outlive the session

### Memory Bank Constraint
The 10-problem limit is a business rule, not an interface check, so it has to live in the logic layer, and ideally the data layer should enforce it too. If only the text screen checked the count, any other entry point could skip the check, including a Flask route, a test, or a script, and create an invalid 11-item set. Moving the rule down means every path that adds a problem goes through the same function, such as add_problem_to_set(set_id, problem_id), and that function rejects the 11th item no matter who calls it

**Constraint boundary selected:** both

### Interaction
Repairing the event sequence (two tries, reveal after the second miss) showed that each problem has two possible outcomes worth telling apart: right on the first try, or right only on the second. A session summary like “8 10” erases that difference, so Path 2 loses information the product itself produces. The manual’s purpose for the Memory Bank decided between Paths 2 and 3. Memory Bank (Story) says it exists for problems “you may have trouble with.” A curator can only pick those problems if they can see which ones the learner missed and how many tries each took. Path 2 keeps the score but loses the missed problems, so it doesn’t support the curator’s real job.

## Layer Boundary Notes
**Business behavior that should remain outside the interface:**
Checking the answer: deciding whether a submitted answer is correct.
Counting tries: recording the try number for each submission and resetting it to 0 when a new problem starts.
Choosing the outcome: given “wrong” plus the try number, deciding whether the result is retry (try 1) or reveal (try 2). The logic returns that decision as data, such as {"correct": False, "try": 2, "outcome": "reveal", "answer": 13}.
Keeping score: counting right answers out of problems tried.
For ST-01, managing the range: picking the secret number between 9 and 100, holding the current low and high bounds, updating them after each guess, and keeping them containing the secret number.

**Data that can be stubbed now:**
For the minimal text prototype, I can stub problems, practice sets and their membership, attempts, results, and the current play state in memory. Play state means the try count, plus ST-01’s secret number and current low and high bounds. They can live in plain Python dicts and lists behind a store interface, with methods like add_problem_to_set(), count_set_problems(), save_attempt(), and save_result(). The logic layer calls only those methods and never touches the data directly. Later, a JSON or database store can implement the same methods without changing the logic or the interface. The rules don’t get stubbed: the 10-problem limit, the retry and reveal decision, and the range update stay in business logic. The trade-off is that in-memory data is lost when the program exits. That’s acceptable for now because the store boundary is where persistent storage plugs in later.

## New Complication
**Response:** Revise state boundary

Reporting is already a requirement. The curator must be able to review a learner’s results later, and the previous round settled on the learner → session → attempts structure. A try-1 miss followed by closing the program is exactly the kind of history that structure is meant to keep. If try state lives only in the interface, that attempt disappears, and the curator never sees that the learner struggled with the problem.The event sequence showed that try number drives the outcome. Try 1 wrong gives EEE and a retry; try 2 wrong gives EEE and a reveal. The repaired event order made try number a decision input, not just something shown on screen, so it belongs in state the logic owns.

## Build-Readiness Decision
**Disposition:** Split / defer part

**Design decision:**
Split the slice. Build the evidence-backed core now and defer cross-session resume as a separate story with an explicit dependency.

## Revision From Initial Thinking
Where state lives. My first design kept try state inside the interface. The early-close scenario showed that this erases the try-1 miss, so state now lives outside the interface in a store, and each attempt is saved when it happens.What drives the design. My original question was about what the system shows the learner right now. It is now about what the system must remember and enforce for any interface and any later reader. The learner’s screen is just one consumer of that state.

## Tradeoff Accepted
I’m accepting more structure up front (Attempt, PracticeSetProblem, and Session/Result records behind a store boundary) in exchange for supporting later curator review and a clean move to Flask and persistent storage. This takes more work than a live-only score panel or a single session summary, but those simpler designs would lose the missed-problem and try history the curator needs. They would also have to be rebuilt once Flask or real storage arrives.

## Unresolved Uncertainty
Cross-session resume, What a curator review shows and What the timer measures

## Next Question
Next question: How should the system represent a session that was never finished?

## Three-Layer Prototype Bridge
Text Interface: only input and output, Business Logic: owns every rule and decision, Stubbed Data Layer: stores and retrieves, and decides nothing

## Trace Back to Product Work
Given the system has picked a secret number between 9 and 100, when the learner enters a guess, then the system displays two numbers and the secret number is between them.
