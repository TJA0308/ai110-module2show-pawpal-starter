# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested the main behaviors of the system:

Marking a task complete
Adding a task to a pet
Sorting tasks by due date and time
Filtering tasks by pet, status, or task type
Detecting scheduling conflicts
Creating the next occurrence of a daily recurring task
Saving and loading data using JSON

These tests were important because they verify both the object-oriented structure and the scheduler’s algorithmic behavior.

b. Confidence

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I am about 4 out of 5 confident that the scheduler works correctly.

The CLI demo runs successfully, and all 7 pytest tests pass. If I had more time, I would test invalid dates, invalid times, pets with no tasks, an owner with no pets, weekly recurrence, and overlapping task durations.

---

## 5. Reflection

**a. What went well**

-The part I am most satisfied with is the separation of responsibilities between the classes. Owner, Pet, and Task store the main data, while Scheduler handles the scheduling logic.

I am also satisfied that the CLI demo clearly shows the system workflow: creating pets, adding tasks, sorting the schedule, filtering tasks, detecting conflicts, completing a recurring task, finding the next available slot, and saving data.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would improve the Streamlit UI so users could access more scheduler features visually. I would also add task duration and stronger conflict detection for overlapping time blocks.

I would also add better input validation for dates, times, and recurrence values.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important thing I learned is that AI can help generate ideas and code quickly, but I still need to act as the lead architect. I had to understand the rubric, check whether the design made sense, run the code, fix the repo structure, and verify the tests myself.
