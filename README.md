# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

The project includes:

- An object-oriented backend using `Owner`, `Pet`, `Task`, and `Scheduler`
- A CLI demo in `main.py`
- A Streamlit UI in `app.py`
- A Mermaid UML diagram in `diagrams/uml_final.mmd`
- Automated tests in `tests/test_pawpal.py`
- Documentation and reflection files

The main classes are:

- `Owner`: stores owner information and manages multiple pets
- `Pet`: stores pet information and that pet's care tasks
- `Task`: stores one care activity with description, due date, due time, priority, status, recurrence, and task type
- `Scheduler`: organizes tasks across multiple pets and provides sorting, filtering, conflict detection, recurrence, and other scheduling features

## Getting started

### Setup

```bash
python -m pip install -r requirements.txt
```

### Run the CLI demo

```bash
python main.py
```

### Run the tests

```bash
python -m pytest
```

## 🖥️ Sample Output

```text
Today's Schedule
----------------------------------------------------------------------------------------
Date         Time   Pet        Task                   Priority Status     Type        
----------------------------------------------------------------------------------------
2026-07-06   07:30  Milo       Breakfast              High     ⏳ Pending  Feeding     
2026-07-06   08:30  Luna       Morning walk           High     ⏳ Pending  Exercise    
2026-07-06   08:30  Milo       Give medicine          High     ⏳ Pending  Medication  
2026-07-06   14:00  Luna       Vet checkup            Medium   ⏳ Pending  Appointment 

Pending tasks for Luna:
Luna Pending Tasks
----------------------------------------------------------------------------------------
Date         Time   Pet        Task                   Priority Status     Type        
----------------------------------------------------------------------------------------
2026-07-06   08:30  Luna       Morning walk           High     ⏳ Pending  Exercise    
2026-07-06   14:00  Luna       Vet checkup            Medium   ⏳ Pending  Appointment 

Priority-based schedule:
Priority Schedule
----------------------------------------------------------------------------------------
Date         Time   Pet        Task                   Priority Status     Type        
----------------------------------------------------------------------------------------
2026-07-06   07:30  Milo       Breakfast              High     ⏳ Pending  Feeding     
2026-07-06   08:30  Luna       Morning walk           High     ⏳ Pending  Exercise    
2026-07-06   08:30  Milo       Give medicine          High     ⏳ Pending  Medication  
2026-07-06   14:00  Luna       Vet checkup            Medium   ⏳ Pending  Appointment 

Conflict warnings:
⚠️  Conflict on 2026-07-06 at 08:30: Luna: Morning walk | Milo: Give medicine

Completing Luna's daily walk...
Schedule After Recurrence
----------------------------------------------------------------------------------------
Date         Time   Pet        Task                   Priority Status     Type        
----------------------------------------------------------------------------------------
2026-07-06   07:30  Milo       Breakfast              High     ⏳ Pending  Feeding     
2026-07-06   08:30  Luna       Morning walk           High     ✅ Done     Exercise    
2026-07-06   08:30  Milo       Give medicine          High     ⏳ Pending  Medication  
2026-07-06   14:00  Luna       Vet checkup            Medium   ⏳ Pending  Appointment 
2026-07-07   08:30  Luna       Morning walk           High     ⏳ Pending  Exercise    

Next available slot today between 07:30 and 09:00: 08:00

Saved demo data to pawpal_data.json
```

## 🧪 Testing PawPal+

Run:

```bash
python -m pytest
```

Sample test output:

```text
================================= test session starts ==================================
platform win32 -- Python 3.13.6, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\lenovo\OneDrive\ドキュメント\GitHub\ai110-module2show-pawpal-starter
plugins: anyio-4.11.0
collected 7 items                                                                       

tests\test_pawpal.py .......                                                      [100%]

================================== 7 passed in 0.08s ===================================
```

The tests cover:

- Marking a task complete
- Adding a task to a pet
- Sorting tasks by due date and time
- Filtering tasks by pet, status, or task type
- Detecting scheduling conflicts
- Creating recurring daily tasks
- Saving and loading data with JSON persistence

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks across all pets by due date and time |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks by pet name, completion status, or task type |
| Conflict handling | `Scheduler.detect_conflicts()` | Detects tasks scheduled for the exact same date and time |
| Recurring tasks | `Scheduler.complete_task()` | Marks a task complete and creates the next daily/weekly occurrence |
| Priority scheduling | `Scheduler.sort_by_priority_then_time()` | Sorts high-priority tasks before medium and low-  priority tasks |
| Next available slot | `Scheduler.next_available_slot()` | Finds an open time slot within a given time window |
| JSON persistence | `Scheduler.save_to_json(), Scheduler.load_from_json()` | Saves and reloads owner, pet, and task data between runs |

## 📸 Demo Walkthrough

1. The demo creates one owner.
2. It creates two pets: Luna and Milo.
3. Several tasks are added for both pets.
4. The scheduler prints today's schedule in chronological order.
5. The scheduler filters and displays Luna's pending tasks.
6. The scheduler displays a priority-based schedule.
7. The scheduler detects a conflict at 08:30 between Luna's walk and Milo's medicine task.
8. Luna's daily walk is marked complete.
9. The system automatically creates the next daily walk for the following day.
10. The scheduler finds the next available slot between 07:30 and 09:00.
11. The demo saves owner, pet, and task data to JSON.

## UML Diagram

The final Mermaid UML source file is located at:

```text
diagrams/uml_final.mmd
```

The UML includes the four required classes:

- `Owner`
- `Pet`
- `Task`
- `Scheduler`

It also shows the core relationships:

- An owner has multiple pets.
- Each pet has multiple tasks.
- The scheduler manages tasks across the owner's pets.