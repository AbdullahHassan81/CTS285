##DataMan Product Backlog

##Sources
This backlog uses the updated docs/requirements.md, the DataMan manual, the M3 Backlog Triage Decision Record, and the M3 Product Owner Decision Record. The manual supports answer checking, retry attempts, score displays, 
and the Memory Bank feature for storing up to ten practice problems. Progress persistence, activity summaries, advanced analytics, and decorative themes are modernization candidates rather than features established by the original manual.

##Priority Order
1. US-01 — Immediate answer feedback
2. US-02 — Retry after an incorrect response
3. US-03 — Preserve learner progress between sessions
4. US-04 — Parent/teacher activity summary
5. US-05 — Advanced analytics dashboard
6. US-06 — Decorative theme selector

##Stories

US-01 — Immediate answer feedback
Requirement ID: FR-01; NFR-02 (proposed response-time target; confirm before finalizing)
User Story: As a learner, I want to know whether my answer is correct so that I can understand how I am doing while practicing.
Acceptance Criteria:
- Given a learner has entered an answer to a practice problem, when the answer is checked, then the system indicates whether the answer is correct or incorrect.
- Given the learner submits an answer, when the system displays correctness feedback, then the feedback appears within one second under the agreed test conditions (only after the team confirms the proposed NFR-02 target).
Relative Effort: S — The triage record rates this as small effort compared with progress persistence and analytics.
Dependency / Constraint: None identified in the triage record. The one-second target is proposed and must be confirmed.
Priority: 1
Readiness: Move Forward
Priority Rationale: High value, small effort, low risk, and explicitly required for the first usable release.
US-02 — Retry after an incorrect response
Requirement ID: FR-02
User Story: As a learner, I want another attempt after an incorrect answer so that I can try to solve the same problem without being shown the answer immediately.
Acceptance Criteria:
- Given a learner is answering a practice problem, when the learner submits an incorrect answer and an attempt remains, then the system allows another attempt without revealing the correct answer.
- Given another attempt is available, when the learner submits a new response to the same problem, then the system checks that response.
- Given the learner has used two attempts without a correct answer, when the second incorrect response is checked, then the system displays the correct result, matching the manual's Answer Checker behavior.
Relative Effort: S — The triage record rates this as small effort, comparable to immediate feedback.
Dependency / Constraint: Depends on the answer-checking flow. The manual describes two attempts before the correct result is shown.
Priority: 2
Readiness: Move Forward
Priority Rationale: High learner value, small effort, low risk, and a clear dependency on answer checking.
US-03 — Preserve learner progress between sessions
Requirement ID: Proposed FR-05 — add this requirement to docs/requirements.md before submission.
User Story: As a returning learner, I want my previously completed progress to remain available so that I can continue instead of starting the activity over.
Acceptance Criteria:
- Given a learner has completed part of an activity and progress has been saved, when the learner returns in a later session using the agreed identity/session approach, then the previously completed progress is available.
- Given previously completed progress is available, when the learner resumes the activity, then the learner can continue from that progress rather than starting over.
Relative Effort: L — The triage record rates this as large effort, greater than the small and medium items.
Dependency / Constraint: The identity/session approach must be decided first. This is not a capability documented in the original manual; it is a proposed modernization feature.
Priority: 3
Readiness: Refine
Priority Rationale: High value, but large effort and unresolved identity/session decisions create uncertainty. Refine before committing implementation details.
US-04 — Parent/teacher activity summary
Requirement ID: Proposed FR-06 — add this requirement to docs/requirements.md before submission.
User Story: As a parent or teacher, I want to review a learner's activity summary so that I can understand the learner's recorded activity and progress.
Acceptance Criteria:
- Given activity data has been recorded for a learner and the viewer is authorized, when a parent or teacher opens the activity summary, then the system displays a summary based only on the available recorded data.
- Given no activity data is available for the selected learner, when the summary is opened, then the system communicates that no activity data is available instead of presenting invented results.
Relative Effort: M — The triage record rates this as medium effort, between small items and large progress/analytics work.
Dependency / Constraint: Depends on activity data being available and on decisions about which fields appear and who may view them.
Priority: 4
Readiness: Move Forward
Priority Rationale: Medium value and effort. It is carried forward because the Product Owner reflection specifically identifies it as an item to bring into the DataMan backlog, but its scope and access rules remain open.
US-05 — Advanced analytics dashboard
Requirement ID: No existing requirement ID — deferred candidate; do not treat as an approved requirement yet.
User Story: As a person reviewing learner activity, I want to examine broader patterns in available activity data so that I can understand trends in learner practice.
Acceptance Criteria:
- Given the reporting model and required data have been approved, when an authorized user opens the analytics view, then any displayed summaries are derived from the available recorded data.
- Given the reporting model has not been approved, when the analytics view is considered for release, then the team keeps this story deferred rather than presenting unsupported analytics.
Relative Effort: L — The triage record rates this as large effort.
Dependency / Constraint: Requires a defined reporting model and sufficient activity data; the triage record identifies high risk.
Priority: 5
Readiness: Defer
Priority Rationale: Medium value but large effort, high risk, and unresolved reporting dependencies. Defer until the reporting approach is defined.
US-06 — Decorative theme selector
Requirement ID: No existing requirement ID — deferred candidate; no supporting requirement is currently defined.
User Story: As a learner, I want to choose a decorative theme so that I can personalize the appearance of the learning activity.
Acceptance Criteria:
- Given a theme selector is approved for development, when a learner chooses a theme, then the selected theme is applied to the activity's appearance.
- Given a learner has selected a theme, when the learner continues using that activity, then the selected theme remains active for that activity.
Relative Effort: S — The triage record rates this as small effort.
Dependency / Constraint: None identified in the triage record. No requirement currently supports this feature.
Priority: 6
Readiness: Defer
Priority Rationale: Low value despite small effort and low risk. Defer it so core learning capabilities take precedence.
Open Questions Carried Forward
- Q-01 — Activity summary: Which activity fields should appear in the parent/teacher summary, and who is authorized to view each learner's records? US-04 needs these decisions before acceptance criteria are finalized.
- Q-02 — Response time: Is the proposed one-second feedback target appropriate for expected devices and test conditions? Confirm NFR-02 before treating it as final.
- Identity/session approach: What approach will identify a returning learner and associate saved progress with the correct learner? US-03 remains Refine until this is decided.
- Reporting model: What reporting model and activity data would support advanced analytics? US-05 remains Defer.
- Theme selector: Is personalization a stakeholder need worth adding to the requirements register? US-06 remains Defer unless evidence supports it.

##Revisions After Triage and Release Planning
- US-01 — Immediate answer feedback: Kept at priority 1 and Move Forward because the instructor requires it for the first usable release.
- US-02 — Retry: Kept at priority 2 and Move Forward because it is high-value, small-effort, and supported by the manual and FR-02.
- US-03 — Progress persistence: Set to Refine because identity/session decisions are unresolved, despite its high value.
- US-04 — Parent/teacher summary: Kept as Move Forward based on the Product Owner reflection, with activity scope and permissions still to be defined.
- US-05 — Advanced analytics: Kept Deferred because effort and risk are high and the reporting model is unresolved.
- US-06 — Decorative theme: Kept Deferred because value is low relative to core learning needs.
- StudyTrack capacity exercise: Used as a prioritization lesson only. Its task IDs and point estimates were not copied into DataMan because they belong to a different scenario.

##Before You Submit
- [ ] Save this file as docs/product-backlog.md.
- [ ] Add proposed FR-05 and FR-06 to docs/requirements.md, or remove/renumber the related stories if your instructor does not allow proposed requirements.
- [ ] Confirm NFR-02's one-second target before treating it as final.
- [ ] Confirm every Requirement ID used here exists in docs/requirements.md; US-05 and US-06 are explicitly deferred candidates, not approved requirements.
- [ ] Confirm each acceptance criterion is observable and testable.
- [ ] Keep stories in the same order as the Priority Order list.
- [ ] Commit the change with a message describing the backlog update.
