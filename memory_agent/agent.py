from google.adk.agents.llm_agent import Agent

def add_reminder(reminder_text: str, tool_context):
    state = tool_context.state
    reminder = state.get("reminders", [])
    reminder.append(reminder_text)
    state["reminders"] = reminder

    return {
        "action": "add_reminder",
        "reminder": reminder_text,
        "message": f"Reminder '{reminder_text}' added successfully.",
    }

def view_reminders(tool_context):
    state = tool_context.state
    reminders = state.get("reminders", [])

    if not reminders:
        return {
            "action": "view_reminders",
            "reminders": reminders,
            "message": "You have no reminders.",
        }

    reminders_list = "\n".join(f"- {rem}" for rem in reminders)
    return {
        "action": "view_reminders",
        "reminders": reminders,
        "count": len(reminders),
        "message": f"Your reminders are:\n{reminders_list}",
    }

def delete_reminder(index: int, tool_context):
    state = tool_context.state
    reminders = state.get("reminders", [])

    if index < 0 or index >= len(reminders):
        return {
            "action": "delete_reminder",
            "message": "Invalid reminder index.",
        }
    else:
        removed = reminders.pop(index)
        state["reminders"] = reminders
        return {
            "action": "delete_reminder",
            "removed": removed,
            "message": f"Reminder '{removed}' deleted successfully.",
        }

def update_username(new_name: str, tool_context):
    state = tool_context.state
    old_name = state.get("username", "User")
    state["username"] = new_name

    return {
        "action": "update_username",
        "old_name": old_name,
        "new_name": new_name,
        "message": f"Username updated from '{old_name}' to '{new_name}'.",
    }

memory_agent = Agent(
    model='gemini-2.5-flash',
    name='memory_agent',
    description='A reminder assistant that remembers user\'s tasks and reminders.',
    instruction="""
You are a friendly reminder assistant.

You use and update session state:
- username: {username?}
- reminders: {reminders?}

Your tools are:
- add_reminder(reminder_text: str) -> Adds a new reminder.
- view_reminders() -> Views all current reminders.
- delete_reminder(index: int) -> Deletes a reminder by its index.
- update_username(new_name: str) -> Updates the username in session state.

Always:
- Be conversational and polite.
- Confirm actions you perform.
- When relevant, show the current reminder list.
""",
    tools=[add_reminder, view_reminders, delete_reminder],
)
