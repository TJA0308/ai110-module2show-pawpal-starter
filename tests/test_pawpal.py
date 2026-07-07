"""Tests for the PawPal+ backend system."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_scheduler() -> Scheduler:
    """Create a small scheduler fixture."""
    owner = Owner("Test Owner", "test@example.com")
    dog = Pet("Buddy", "Dog", 3)
    cat = Pet("Nala", "Cat", 5)

    dog.add_task(Task("Walk", date(2026, 7, 6), "09:00", "Daily", priority="High"))
    dog.add_task(Task("Brush", date(2026, 7, 6), "08:00", "Once", priority="Low"))
    cat.add_task(Task("Feed", date(2026, 7, 6), "09:00", "Daily", priority="Medium"))

    owner.add_pet(dog)
    owner.add_pet(cat)
    return Scheduler(owner)


def test_mark_complete_changes_status():
    """Task completion should switch completed from False to True."""
    task = Task("Feed", date(2026, 7, 6), "07:30")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_pet_add_task_increases_count():
    """Adding a task should increase the pet's task count."""
    pet = Pet("Luna", "Dog", 4)
    assert len(pet.tasks) == 0

    pet.add_task(Task("Walk", date(2026, 7, 6), "08:30"))

    assert len(pet.tasks) == 1


def test_sort_by_time_returns_chronological_order():
    """Scheduler should return tasks in chronological order."""
    scheduler = make_scheduler()

    sorted_tasks = scheduler.sort_by_time()
    times = [task.due_time for _, task in sorted_tasks]

    assert times == ["08:00", "09:00", "09:00"]


def test_conflict_detection_flags_duplicate_time():
    """Scheduler should flag multiple pending tasks at the same date and time."""
    scheduler = make_scheduler()

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "09:00" in conflicts[0]
    assert "Buddy: Walk" in conflicts[0]
    assert "Nala: Feed" in conflicts[0]


def test_daily_recurrence_creates_tomorrow_task():
    """Completing a daily task should create the next day's occurrence."""
    scheduler = make_scheduler()

    completed = scheduler.complete_task("Buddy", "Walk")

    assert completed is not None
    buddy = scheduler.owner.find_pet("Buddy")
    assert buddy is not None
    recurrence_tasks = [
        task for task in buddy.tasks
        if task.description == "Walk" and task.due_date == date(2026, 7, 7)
    ]
    assert len(recurrence_tasks) == 1
    assert recurrence_tasks[0].completed is False


def test_next_available_slot_skips_occupied_time():
    """Next available slot should skip occupied 08:00 and return 08:30."""
    scheduler = make_scheduler()

    slot = scheduler.next_available_slot(date(2026, 7, 6), start_time="08:00", end_time="09:00")

    assert slot == "08:30"


def test_json_persistence_round_trip(tmp_path):
    """Saving and loading JSON should preserve owner, pets, and tasks."""
    scheduler = make_scheduler()
    file_path = tmp_path / "pawpal_data.json"

    scheduler.save_to_json(file_path)
    loaded_scheduler = Scheduler.load_from_json(file_path)

    assert loaded_scheduler.owner.name == "Test Owner"
    assert len(loaded_scheduler.owner.pets) == 2
    assert len(loaded_scheduler.all_tasks()) == 3
