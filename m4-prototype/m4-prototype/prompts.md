# Prompts Used

AI tool used: Claude (Anthropic), Claude.ai.

## Prompt 1

Attached: my M4 Design Investigation Record (`m4-design-investigation-record.md`).

> Design and Test a Text-Only Prototype
> Use the Module 4 investigation file I just gave to create a minimal text-only prototype. The goal is not to build the finished application. The goal is to test whether your design decisions hold up when they must actually run.
> Keep the scope small. Build one complete product-slice path well enough to test behavior, state, data responsibility, and separation of concerns. Flask and the first framework-based application begin in Module 5.
>
> Required structure — Your prototype must contain three distinguishable layers:
> 1. Text interface layer — receives input and displays output.
> 2. Business logic layer — contains reusable rules and decisions that do not depend on one interface.
> 3. Stubbed data layer — provides or preserves only the data/state needed to test the selected product slice without requiring the final database implementation.
>
> Build from the evidence you already created. Use your investigation brief, Lab Evidence Record, Design Studio work, requirements, backlog evidence, and acceptance criteria. Your prototype should test the design question you carried forward rather than start a new feature from scratch.
> If running the prototype exposes a contradiction, missing state, weak assumption, or misplaced responsibility, revise the design or record the unresolved issue. That discovery is part of the work.
>
> Minimum prototype evidence:
> - One complete path through the selected product slice runs from the text interface. (app.py or equivalent)
> - The business rule or rules for that path can operate independently of the interface. (dataman/logic.py or equivalent)
> - The data boundary is stubbed or replaceable rather than hard-coded throughout the interface. (dataman/store.py or equivalent)
> - State required by the selected behavior is represented deliberately.
> - At least one acceptance criterion can be demonstrated through the prototype.
> - README notes or code comments identify intentionally stubbed work, unresolved uncertainty, and any revision caused by testing the prototype. (For instance, a planning.md or readme.md)
> - prompts.md containing your prompts if you use AI tools; the file can just say "no tools used" if you do not.

## What the AI did

- Read the investigation record and the Number Guesser sections of the DataMan manual.
- Wrote `app.py`, `dataman/logic.py`, `dataman/store.py`, and `tests/test_logic.py`.
- Ran the tests and two scripted games to check the acceptance criterion.
- Drafted `README.md`, including the revisions found while building. The biggest one: the two-try/reveal rule in my investigation belongs to Answer Checker, not to Number Guesser.

<!-- Add any follow-up prompts you use below. -->
