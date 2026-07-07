# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design included four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`.

The `Owner` class stores the owner’s information and manages a list of pets. The `Pet` class stores each pet’s information and that pet’s tasks. The `Task` class represents one pet care activity, such as feeding, walking, medication, grooming, or an appointment. Each task includes a description, due date, due time, priority, completion status, recurrence, and task type.

The `Scheduler` class is responsible for organizing tasks across multiple pets. It handles sorting, filtering, conflict detection, recurring tasks, priority scheduling, and finding the next available time slot.

**b. Design changes**

Yes, my design changed during implementation. At first, it seemed like each `Pet` could manage most of its own scheduling logic. However, that would make it harder to compare tasks across multiple pets.

I changed the design so that `Pet` stores and manages its own task list, while `Scheduler` handles cross-pet scheduling logic. This made the system cleaner because each class has a clearer responsibility.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers due date, due time, pet name, task completion status, task type, priority, and recurrence.

I decided that due date and due time mattered most because the schedule needs to be shown in chronological order. Priority also matters because tasks like feeding or medication can be more important than lower-priority tasks. The scheduler uses these constraints to sort tasks, filter tasks, detect conflicts, and handle recurring tasks.

**b. Tradeoffs**

One tradeoff is that conflict detection only checks for tasks with the exact same due date and due time. It does not check whether tasks overlap based on duration.

This is reasonable for this project because exact-time conflict detection is simple, clear, and easy to test. A future version could add task duration and detect overlapping time blocks more realistically.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to help with design brainstorming, class structure, scheduler logic, test planning, and documentation.

AI was helpful for breaking the project into the required classes: `Owner`, `Pet`, `Task`, and `Scheduler`. It also helped me think through useful scheduling features like sorting by time, filtering by pet/status, detecting conflicts, handling recurring tasks, and writing pytest tests.

The most helpful prompts were specific ones, such as asking how a `Scheduler` should retrieve tasks across multiple pets, how to sort task objects by time, and what edge cases should be tested.

**b. Judgment and verification**

I did not accept every AI suggestion automatically. One important design decision was keeping cross-pet scheduling logic inside the `Scheduler` class instead of putting too much logic inside `Pet` or `Owner`. This made the design easier to explain and test.

I verified the AI-assisted code by running `python main.py` and `python -m pytest`.

When I first ran pytest in my forked repo, it collected 0 tests because the `tests/` folder had not been copied correctly. I fixed the repo structure by adding `tests/test_pawpal.py`, reran pytest, and confirmed that all 7 tests passed.

---

## 4. Testing and Verification

**a. What you tested**

I tested the main behaviors of the system:

- Marking a task complete
- Adding a task to a pet
- Sorting tasks by due date and time
- Filtering tasks by pet, status, or task type
- Detecting scheduling conflicts
- Creating the next occurrence of a daily recurring task
- Saving and loading data using JSON

These tests were important because they verify both the object-oriented structure and the scheduler’s algorithmic behavior.

**b. Confidence**

I am about 4 out of 5 confident that the scheduler works correctly.

The CLI demo runs successfully, and all 7 pytest tests pass. If I had more time, I would test invalid dates, invalid times, pets with no tasks, an owner with no pets, weekly recurrence, and overlapping task durations.

---

## 5. Reflection

**a. What went well**

The part I am most satisfied with is the separation of responsibilities between the classes. `Owner`, `Pet`, and `Task` store the main data, while `Scheduler` handles the scheduling logic.

I am also satisfied that the CLI demo clearly shows the system workflow: creating pets, adding tasks, sorting the schedule, filtering tasks, detecting conflicts, completing a recurring task, finding the next available slot, and saving data.

**b. What you would improve**

If I had another iteration, I would improve the Streamlit UI so users could access more scheduler features visually. I would also add task duration and stronger conflict detection for overlapping time blocks.

I would also add better input validation for dates, times, and recurrence values.

**c. Key takeaway**

One important thing I learned is that AI can help generate ideas and code quickly, but I still need to act as the lead architect. I had to understand the rubric, check whether the design made sense, run the code, fix the repo structure, and verify the tests myself.