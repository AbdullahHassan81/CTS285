# M3 Product Owner Decision Record

## Scenario
StudyTrack release planning under constrained capacity.

## Round 1 — Capacity 13
- ST-01: Create a study task (3 pts)
- ST-02: Mark a study task complete (2 pts)
- ST-03: Recover a missed task (3 pts)
- ST-07: AI study recommendations (5 pts)

**Why this release slice was defensible:**
Mines is defensible because it has everything you need to study by yourself if you are disciplined enough

**One intentional deferral and why:**
Parent progress dashboard because it does not help the student study or have anything to do with the student studying. The parent cant force their kid to study if he dosent want to, at the end of the day they have to choose to study.

## Complication
Capacity dropped from 13 to 10 points. Keyboard accessibility testing revealed that task entry cannot reliably be completed with keyboard navigation, so ST-04 became release-critical.

## Revised Release Slice — Capacity 10
- ST-01: Create a study task (3 pts)
- ST-04: Keyboard-accessible task entry (2 pts)
- ST-07: AI study recommendations (5 pts)

### Removed after complication
- ST-02: Mark a study task complete
- ST-03: Recover a missed task

### Added after complication
- ST-04: Keyboard-accessible task entry

**What changed and why:**
I cut off what I thought was not important enough and I had to prioritize

**Tradeoff accepted:**
I removed recover missed task complete to keep the AI recommendations

## Transfer to DataMan
Before finalizing your DataMan backlog, review whether any item is high value but not ready, depends on unresolved work, consumes disproportionate effort, or should move because it reduces risk or unlocks other work.
