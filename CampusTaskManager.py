import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"


# ------------- Utility Functions -------------
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


# ------------- Core Features -------------
def add_task(tasks):
    print("\n--- Add New Task ---")
    title = input("Task title: ").strip()
    category = input("Category (Assignment/Exam/Project/Personal): ").strip()
    deadline = input("Deadline (YYYY-MM-DD): ").strip()

    # Validate date
    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format!")
        return

    new_task = {
        "title": title,
        "category": category,
        "deadline": deadline,
        "status": "Pending"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added successfully!\n")


def view_tasks(tasks):
    print("\n--- All Tasks ---")
    if not tasks:
        print("No tasks available.\n")
        return

    for i, t in enumerate(tasks, start=1):
        print(f"{i}. {t['title']} | {t['category']} | Deadline: {t['deadline']} | Status: {t['status']}")
    print()


def tasks_due_soon(tasks):
    print("\n--- Tasks Due Soon (in 2 days) ---")
    today = datetime.now().date()
    found = False

    for t in tasks:
        deadline_date = datetime.strptime(t["deadline"], "%Y-%m-%d").date()
        diff = (deadline_date - today).days

        if diff <= 2 and t["status"] == "Pending":
            print(f"⚠ {t['title']} → Due in {diff} days")
            found = True

    if not found:
        print("No tasks due soon.\n")


def mark_task_completed(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter task number to mark completed: ")) - 1
        if index < 0 or index >= len(tasks):
            print("Invalid selection!")
            return

        tasks[index]["status"] = "Completed"
        save_tasks(tasks)
        print("Task marked as completed!\n")

    except ValueError:
        print("Invalid input!")


def edit_task(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter task number to edit: ")) - 1
        if index < 0 or index >= len(tasks):
            print("Invalid selection!")
            return

        print("Leave blank to keep old value.")
        new_title = input("New title: ").strip()
        new_deadline = input("New deadline (YYYY-MM-DD): ").strip()

        if new_title:
            tasks[index]["title"] = new_title
        if new_deadline:
            try:
                datetime.strptime(new_deadline, "%Y-%m-%d")
                tasks[index]["deadline"] = new_deadline
            except ValueError:
                print("Invalid date format!")

        save_tasks(tasks)
        print("Task updated successfully!\n")

    except ValueError:
        print("Invalid input!")


def delete_task(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter task number to delete: ")) - 1
        if index < 0 or index >= len(tasks):
            print("Invalid selection!")
            return

        tasks.pop(index)
        save_tasks(tasks)
        print("Task deleted!\n")

    except ValueError:
        print("Invalid input!")


# ------------- Main Program -------------
def main():
    tasks = load_tasks()

    while True:
        print("=========== Campus Task Manager ===========")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Tasks Due Soon")
        print("4. Mark Task Completed")
        print("5. Edit Task")
        print("6. Delete Task")
        print("7. Exit")
        print("===========================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            tasks_due_soon(tasks)
        elif choice == "4":
            mark_task_completed(tasks)
        elif choice == "5":
            edit_task(tasks)
        elif choice == "6":
            delete_task(tasks)
        elif choice == "7":
            print("Exiting program... Goodbye!")
            break
        else:
            print("Invalid option. Try again.\n")


if __name__ == "__main__":
    main()