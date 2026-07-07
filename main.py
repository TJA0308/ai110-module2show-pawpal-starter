"""CLI demo for PawPal+."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_scheduler() -> Scheduler:

    """Create a demo owner with pets and tasks."""
    today = date.today()

    owner = Owner("Jordan Lee", "jordan@example.com")

    luna = Pet("Luna", "Dog", 4)
    milo = Pet("Milo", "Cat", 2)

    luna.add_task(Task("Morning walk", today, "08:30", "Daily", priority="High", task_type="Exercise"))
    luna.add_task(Task("Vet checkup", today, "14:00", "Once", priority="Medium", task_type="Appointment"))
    milo.add_task(Task("Breakfast", today, "07:30", "Daily", priority="High", task_type="Feeding"))
    milo.add_task(Task("Give medicine", today, "08:30", "Daily", priority="High", task_type="Medication"))

    owner.add_pet(luna)
    owner.add_pet(milo)

    return Scheduler(owner)


def main() -> None:
    """Run the PawPal+ CLI demonstration."""
    scheduler = build_demo_scheduler()

    print(scheduler.format_schedule(title="Today's Schedule"))

    print("\nPending tasks for Luna:")
    print(scheduler.format_schedule(scheduler.filter_tasks(pet_name="Luna", completed=False), title="Luna Pending Tasks"))

    print("\nPriority-based schedule:")
    print(scheduler.format_schedule(scheduler.sort_by_priority_then_time(), title="Priority Schedule"))

    print("\nConflict warnings:")
    for warning in scheduler.detect_conflicts():
        print(f"WARNING: {warning}")

    print("\nCompleting Luna's daily walk...")
    scheduler.complete_task("Luna", "Morning walk")
    print(scheduler.format_schedule(title="Schedule After Recurrence"))

    next_slot = scheduler.next_available_slot(date.today(), start_time="07:30", end_time="09:00")
    print(f"\nNext available slot today between 07:30 and 09:00: {next_slot}")

    scheduler.save_to_json("pawpal_data.json")
    print("\nSaved demo data to pawpal_data.json")


if __name__ == "__main__":
    main()
