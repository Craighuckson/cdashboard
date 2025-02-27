import flet as ft

def main(page: ft.Page):
    page.title = "Mini Dashboard"
    tasks = []  # list to store tasks

    # UI elements to display the current task and upcoming tasks
    current_task_display = ft.Text("No current task", style="headlineSmall")
    upcoming_tasks_column = ft.Column()

    def refresh_ui():
        """Refresh the UI to show the updated tasks list."""
        if tasks:
            current_task_display.value = tasks[0]
        else:
            current_task_display.value = "No current task"
        upcoming_tasks_column.controls.clear()
        # Display upcoming tasks (all tasks except the first)
        for i, task in enumerate(tasks[1:], start=1):
            # Create arrow buttons to move tasks up or down
            up_button = ft.IconButton(
                icon=ft.Icons.ARROW_UPWARD,
                disabled=(i == 1),  # disable up for the first upcoming task
                on_click=lambda e, index=i: move_up(index)
            )
            down_button = ft.IconButton(
                icon=ft.Icons.ARROW_DOWNWARD,
                disabled=(i == len(tasks)-1),  # disable down for the last task
                on_click=lambda e, index=i: move_down(index)
            )
            remove_button = ft.IconButton(
                icon=ft.icons.DELETE,
                on_click=lambda e, index=i: remove_task(index)
            )
            upcoming_tasks_column.controls.append(
                ft.Row(controls=[up_button, down_button, remove_button, ft.Text(task)])
            )
        page.update()

    def add_task(e):
        """Add a new task from the input field."""
        new_task = task_input.value.strip()
        if new_task:
            tasks.append(new_task)
            task_input.value = ""
            refresh_ui()

    def move_up(index):
        """Move a task up in the list."""
        if index > 0:
            tasks[index-1], tasks[index] = tasks[index], tasks[index-1]
            refresh_ui()

    def move_down(index):
        """Move a task down in the list."""
        if index < len(tasks) - 1:
            tasks[index], tasks[index+1] = tasks[index+1], tasks[index]
            refresh_ui()

    def sort_tasks(e):
        """Sort all tasks alphabetically (ignoring case)."""
        tasks.sort(key=lambda t: t.lower())
        refresh_ui()

    def remove_task(index):
        """Remove a task from the list."""
        if 0 <= index < len(tasks):
            del tasks[index]
            refresh_ui()

    def complete_current_task(e):
        """Mark the current task as completed and remove it."""
        if tasks:
            tasks.pop(0)
            refresh_ui()

    # Input field and buttons
    task_input = ft.TextField(hint_text="Enter new task")
    add_button = ft.ElevatedButton(text="Add Task", on_click=add_task)
    sort_button = ft.ElevatedButton(text="Sort Tasks", on_click=sort_tasks)
    complete_button = ft.ElevatedButton(text="Complete Current Task", on_click=complete_current_task)

    # Build the app layout
    page.add(
        ft.Row(controls=[task_input, add_button, sort_button]),
        ft.Divider(),
        ft.Text("Current Task:", weight="bold"),
        current_task_display,
        complete_button,
        ft.Divider(),
        ft.Text("Upcoming Tasks:", weight="bold"),
        upcoming_tasks_column,
    )

ft.app(target=main)
