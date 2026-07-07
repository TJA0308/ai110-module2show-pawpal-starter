# AI Interactions

## Design Prompt

**Prompt/task:**  
Design a pet care scheduler using four classes: `Owner`, `Pet`, `Task`, and `Scheduler`. Suggest attributes, methods, and Mermaid UML relationships.

**Useful output:**  
The AI helped identify the core relationships: one owner has many pets, each pet has many tasks, and the scheduler manages tasks across the owner.

**Final decision:**  
I used the four-class design but kept the class responsibilities simple and readable.

## Agent Workflow

**Files modified:**  
- `pawpal_system.py`
- `main.py`
- `tests/test_pawpal.py`
- `README.md`
- `diagrams/uml_final.mmd`

**Task requested of the agent:**  
Generate a clean OOP implementation for PawPal+ with scheduling algorithms, tests, and documentation support.

**What the agent completed:**  
The agent helped scaffold the classes, suggest algorithmic methods, and draft tests for sorting, recurrence, conflict detection, and persistence.

**Manual corrections made:**  
I reviewed the design to make sure `Scheduler` operated across multiple pets. I also kept conflict detection lightweight by checking exact time collisions instead of adding duration overlap logic.

## Test Generation Prompt

**Prompt/task:**  
Create pytest tests for a pet scheduler that verifies task completion, task addition, sorting correctness, recurrence, conflict detection, next available slots, and JSON persistence.

**Rationale for edge cases:**  
- Sorting verifies that tasks added out of order are returned correctly.
- Conflict detection checks duplicate times across multiple pets.
- Recurrence verifies that completing a daily task creates tomorrow's task.
- Persistence verifies that nested objects survive save/load.

## Prompt Comparison

| Model/Strategy | Prompt/Task | Useful Output | Problem With Output | Final Decision |
|---|---|---|---|---|
| Strategy A: simple class generation | Generate four OOP classes for a pet scheduler | Good starting structure | Scheduler was too passive at first | Modified Scheduler to include cross-pet algorithms |
| Strategy B: algorithm-focused prompt | Add sorting, filtering, recurrence, and conflicts | Better scheduling methods | Suggested some features beyond project scope | Kept sorting, filtering, recurrence, conflicts, priority, and next slot |

## AI Suggestion Accepted

I accepted the suggestion to use Python dataclasses for `Task`, `Pet`, and `Owner` because it made the code cleaner and easier to read.

## AI Suggestion Rejected

I rejected making the project too complex with full calendar overlap detection and a database-backed UI. For this assignment, exact-time conflict detection and JSON persistence were more appropriate and easier to verify.
