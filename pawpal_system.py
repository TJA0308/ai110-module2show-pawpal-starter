"""Core backend logic for PawPal+.

This module contains the object-oriented logic layer for a CLI-first pet care
scheduler. The classes model owners, pets, tasks, and cross-pet scheduling
algorithms such as sorting, filtering, conflict detection, recurring tasks,
priority ordering, next available slot suggestions, and JSON persistence.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date, datetime, timedelta
from pathlib import Path
import json
from typing import Any


PRIORITY_RANK = {"High": 0, "Medium": 1, "Low": 2}


@dataclass
class Task:
    """Represents one pet care activity such as feeding, walking, or medication."""

    description: str
    due_date: date
    due_time: str
    frequency: str = "Once"
    completed: bool = False
    priority: str = "Medium"
    task_type: str = "General"

    def __post_init__(self) -> None:
        """Validate task fields after object creation."""
        self.due_time = self._validate_time(self.due_time)
        self.frequency = self.frequency.title()
        self.priority = self.priority.title()

        if self.frequency not in {"Once", "Daily", "Weekly"}:
            raise ValueError("frequency must be 'Once', 'Daily', or 'Weekly'")

        if self.priority not in PRIORITY_RANK:
            raise ValueError("priority must be 'Low', 'Medium', or 'High'")

    @staticmethod
    def _validate_time(time_text: str) -> str:
        """Validate and normalize a time string in HH:MM 24-hour format."""
        try:
            parsed = datetime.strptime(time_text, "%H:%M")
        except ValueError as exc:
            raise ValueError("due_time must use HH:MM 24-hour format") from exc
        return parsed.strftime("%H:%M")

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True

    def create_next_occurrence(self) -> "Task | None":
        """Create the next task if this task is recurring."""
        if self.frequency == "Daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "Weekly":
            next_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            description=self.description,
            due_date=next_date,
            due_time=self.due_time,
            frequency=self.frequency,
            completed=False,
            priority=self.priority,
            task_type=self.task_type,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert a Task object into a JSON-safe dictionary."""
        data = asdict(self)
        data["due_date"] = self.due_date.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Create a Task object from a dictionary loaded from JSON."""
        copied = dict(data)
        copied["due_date"] = date.fromisoformat(copied["due_date"])
        return cls(**copied)


@dataclass
class Pet:
    """Stores identifying pet information and that pet's care tasks."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def list_tasks(self) -> list[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks

    def get_pending_tasks(self) -> list[Task]:
        """Return incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]

    def mark_task_complete(self, description: str) -> Task | None:
        """Mark the first matching incomplete task complete by description."""
        for task in self.tasks:
            if task.description == description and not task.completed:
                task.mark_complete()
                next_task = task.create_next_occurrence()
                if next_task is not None:
                    self.add_task(next_task)
                return task
        return None

    def to_dict(self) -> dict[str, Any]:
        """Convert a Pet object into a JSON-safe dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Pet":
        """Create a Pet object from a dictionary loaded from JSON."""
        pet = cls(name=data["name"], species=data["species"], age=data["age"])
        pet.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
        return pet


@dataclass
class Owner:
    """Represents a pet owner who can manage multiple pets."""

    name: str
    email: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def list_pets(self) -> list[Pet]:
        """Return all pets owned by this owner."""
        return self.pets

    def find_pet(self, pet_name: str) -> Pet | None:
        """Find a pet by name, ignoring case."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet
        return None

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all tasks across all pets as pet-task pairs."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]

    def to_dict(self) -> dict[str, Any]:
        """Convert an Owner object into a JSON-safe dictionary."""
        return {
            "name": self.name,
            "email": self.email,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Owner":
        """Create an Owner object from a dictionary loaded from JSON."""
        owner = cls(name=data["name"], email=data["email"])
        owner.pets = [Pet.from_dict(pet_data) for pet_data in data.get("pets", [])]
        return owner


class Scheduler:
    """Organizes and manages care tasks across all pets belonging to an owner."""

    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with an owner."""
        self.owner = owner

    def all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return all pet-task pairs across the owner."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: list[tuple[Pet, Task]] | None = None) -> list[tuple[Pet, Task]]:
        """Sort pet-task pairs chronologically by due date and due time."""
        task_pairs = self.all_tasks() if tasks is None else tasks
        return sorted(task_pairs, key=lambda pair: (pair[1].due_date, pair[1].due_time))

    def sort_by_priority_then_time(
        self, tasks: list[tuple[Pet, Task]] | None = None
    ) -> list[tuple[Pet, Task]]:
        """Sort task pairs by priority first, then date and time."""
        task_pairs = self.all_tasks() if tasks is None else tasks
        return sorted(
            task_pairs,
            key=lambda pair: (
                PRIORITY_RANK[pair[1].priority],
                pair[1].due_date,
                pair[1].due_time,
            ),
        )

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
        task_type: str | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Filter tasks by pet name, completion status, and/or task type."""
        results = self.all_tasks()

        if pet_name is not None:
            results = [pair for pair in results if pair[0].name.lower() == pet_name.lower()]

        if completed is not None:
            results = [pair for pair in results if pair[1].completed == completed]

        if task_type is not None:
            results = [pair for pair in results if pair[1].task_type.lower() == task_type.lower()]

        return results

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for tasks scheduled at the same date and time."""
        seen: dict[tuple[date, str], list[str]] = {}

        for pet, task in self.all_tasks():
            if task.completed:
                continue
            key = (task.due_date, task.due_time)
            seen.setdefault(key, []).append(f"{pet.name}: {task.description}")

        warnings = []
        for (due_date, due_time), items in seen.items():
            if len(items) > 1:
                warnings.append(
                    f"Conflict on {due_date.isoformat()} at {due_time}: "
                    + " | ".join(items)
                )

        return warnings

    def complete_task(self, pet_name: str, description: str) -> Task | None:
        """Mark a pet's matching task complete and create recurrence if needed."""
        pet = self.owner.find_pet(pet_name)
        if pet is None:
            return None
        return pet.mark_task_complete(description)

    def next_available_slot(
        self,
        due_date: date,
        start_time: str = "08:00",
        end_time: str = "21:00",
        interval_minutes: int = 30,
    ) -> str | None:
        """Find the next open time slot on a date using fixed time intervals."""
        start = datetime.combine(due_date, datetime.strptime(start_time, "%H:%M").time())
        end = datetime.combine(due_date, datetime.strptime(end_time, "%H:%M").time())
        occupied = {
            task.due_time
            for _, task in self.all_tasks()
            if task.due_date == due_date and not task.completed
        }

        current = start
        while current <= end:
            candidate = current.strftime("%H:%M")
            if candidate not in occupied:
                return candidate
            current += timedelta(minutes=interval_minutes)

        return None

    def format_schedule(
        self,
        tasks: list[tuple[Pet, Task]] | None = None,
        title: str = "PawPal+ Schedule",
    ) -> str:
        """Return a readable table-like schedule for CLI output."""
        task_pairs = self.sort_by_time(tasks)
        if not task_pairs:
            return f"{title}\nNo tasks found."

        lines = [
            title,
            "-" * 88,
            f"{'Date':<12} {'Time':<6} {'Pet':<10} {'Task':<22} {'Priority':<8} {'Status':<10} {'Type':<12}",
            "-" * 88,
        ]

        for pet, task in task_pairs:
            status = "Done" if task.completed else " Pending"
            lines.append(
                f"{task.due_date.isoformat():<12} {task.due_time:<6} "
                f"{pet.name:<10} {task.description:<22} {task.priority:<8} "
                f"{status:<10} {task.task_type:<12}"
            )

        return "\n".join(lines)

    def save_to_json(self, file_path: str | Path) -> None:
        """Save owner, pets, and tasks to a JSON file."""
        path = Path(file_path)
        path.write_text(json.dumps(self.owner.to_dict(), indent=2), encoding="utf-8")

    @staticmethod
    def load_from_json(file_path: str | Path) -> "Scheduler":
        """Load owner, pets, and tasks from a JSON file and return a Scheduler."""
        path = Path(file_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        return Scheduler(Owner.from_dict(data))
