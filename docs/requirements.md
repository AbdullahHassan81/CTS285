# DataMan Requirements Register

> Replace all bracketed prompts with your own project evidence and requirements. Delete the prompts before submitting.

## Project Context

[The modernization goal for Dataman is to make it a bit modern by adding new features so that children todays day and age can use. The users would be educators and children, the primary problem the projects trying to solve is to make it modernized.]

## Evidence Notes

Use at least four concise evidence statements. Label the source of each.

- **E-01 — Source:** [The Story of DataMan manual]  
  **Evidence:** [DataMan checks a learner's math answer and provides feedback. Correct answers are indicated through the display, while incorrect answers trigger an error indication. The learner can try again before the correct result is revealed]

- **E-02 — Source:** [The Story of DataMan manual]  
  **Evidence:** [DataMan tracks correct answers and attempted problems and displays a score after ten problems. The manual also describes how division answers are entered using a quotient and remainder]

- **E-03 — Source:** [The Story of DataMan manual]  
  **Evidence:** [A parent, teacher, or friend can store up to ten practice problems for a learner. The learner can retrieve and answer the stored problems, receive retry opportunities, and see a score after completing the set]

- **E-04 — Source:** [The Story of DataMan manual]  
  **Evidence:** [Immediate answer feedback, retry after an incorrect response, and preserving learner progress between sessions were identified as valuable capabilities. Persistent progress depends on an unresolved identity/session approach. The advanced analytics dashboard was deferred because it requires substantial effort and an unresolved reporting model]

[Add additional evidence notes if needed.]

## Functional Requirements

Write at least four functional requirements. Each requirement should describe a capability or behavior the system must provide.

### FR-01
**Requirement:** The system must [indicate whether a learner's submitted answer to a practice problem is correct or incorrect.].  
**Source/Rationale:** [E-01 documents the original DataMan answer-checking behavior. The M3 triage decision also identifies immediate answer feedback as a requirement for the first usable release.]

### FR-02
**Requirement:** The system must [allow a learner to submit another response to the same practice problem after an incorrect answer without immediately revealing the correct answer after the first incorrect attempt.].  
**Source/Rationale:** [E-01 documents retry behavior in the original DataMan. The M3 triage record identifies retry after an incorrect response as a high-value feature.]

### FR-03
**Requirement:** The system must [display the learner's number of correct answers and attempted problems at the end of a practice set.].  
**Source/Rationale:** [E-02 documents the original device's scoring behavior. The modernization should preserve a clear way for learners to review their practice results.]

### FR-04
**Requirement:** The system must [allow an authorized parent or teacher to prepare a set of math practice problems for a learner to complete.].  
**Source/Rationale:** [E-03 documents the Memory Bank capability, which allows an adult to store practice problems for a learner. The exact modern interface, authorization rules, and problem-set limits remain to be determined.]

[Add additional functional requirements if needed.]

## Non-Functional Requirements

Write at least three non-functional requirements. Each requirement should describe a measurable quality, constraint, or condition the system must satisfy.

### NFR-01
**Requirement:** The system must [enter and submit a practice response in the first usable release must be reachable and operable using keyboard navigation alone.].  
**Source/Rationale:** [E-05 identifies a failure in keyboard-based task entry. The requirement can be verified by completing the practice-entry flow without using a mouse.]

### NFR-02
**Requirement:** The system must [display correct/incorrect feedback within one second of answer submission under the agreed first-release test conditions.].  
**Source/Rationale:** [E-01 and the M3 triage record support the need for answer feedback. The one-second threshold is a proposed modernization target, not a timing requirement documented in the original manual. The project team must confirm this target before treating it as final.]

### NFR-03
**Requirement:** The system must [Each first-release acceptance criterion must describe an observable outcome that can be evaluated as pass or fail.].  
**Source/Rationale:** [The M3 acceptance-criteria exercises emphasize observable behavior and testability while avoiding unnecessary technical implementation details. This requirement supports consistent verification of the product backlog.]

[Add additional non-functional requirements if needed.]

## Open Questions / Assumptions

Do not turn an unsupported idea into a confirmed requirement. Record unresolved items here until evidence supports a decision.

- **Q-01:** [Which activity fields should appear in the parent/teacher activity summary? The project must also define who is authorized to view each learner's records.]
- **Q-02:** [Is the proposed one-second response target appropriate for the expected devices and testing conditions?]

[Add or remove items as appropriate.]

## Final Quality Check

Before submitting, confirm that each requirement is:

- [ ] Clear enough for another team member to interpret consistently.
- [ ] Supported by evidence, a stakeholder need, or a confirmed project constraint.
- [ ] Testable or verifiable later.
- [ ] Solution-neutral enough for this stage of the project.
- [ ] Focused on one main capability or quality.
- [ ] Classified correctly as functional or non-functional.

Also confirm:

- [ ] At least four functional requirements are included.
- [ ] At least three non-functional requirements are included.
- [ ] Every confirmed requirement has a source/rationale.
- [ ] Open questions and assumptions are separated from confirmed requirements.
- [ ] The simulation decision record is saved at `docs/decisions/m2-elicitation-decision-record.md`.
- [ ] This file is saved as `docs/requirements.md`, committed, and synced to GitHub.
