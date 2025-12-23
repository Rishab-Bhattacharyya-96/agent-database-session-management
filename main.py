
import asyncio

from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService

from memory_agent.agent import memory_agent
from utils import call_agent_async

load_dotenv()

async def main():
    DB_URL = "sqlite:///./my_agent_data.db"

    session_service = DatabaseSessionService(db_url=DB_URL)

    initial_state = {
        "username": "User",
        "reminders": [],
    }

    app_name = "ReminderApp"
    user_id = "user_123"

    list_response = await session_service.list_sessions(
        app_name=app_name,
        user_id=user_id,
    )

    existing_session = list_response.sessions

    if existing_session:

        session = existing_session[0]
        session_id = session.id
        print(f"Resuming existing session: {session_id}")
    else:
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            state=initial_state,
        )
        session_id = session.id
        print(f"Created new session: {session_id}")

    runner = Runner(
        agent=memory_agent,
        session_service=session_service,
        app_name=app_name,
    )

    print("\n Reminder Agent Chat (Type 'exit' or 'quit' to end) \n")
    print("----------------------------------------------------")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break

        await call_agent_async(
            runner,
            user_id,
            session_id,
            user_input,
        )

if __name__ == "__main__":
    asyncio.run(main())