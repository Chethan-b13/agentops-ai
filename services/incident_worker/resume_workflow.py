from langgraph.types import Command

from shared.database.session import SessionLocal

from workflows.factory import create_workflow


def main():

    db = SessionLocal()

    try:

        with create_workflow(db) as graph:

            thread_id = input("Thread ID: ")

            state = graph.invoke(
                Command(
                    resume="approved",
                ),
                config={
                    "configurable": {
                        "thread_id": thread_id,
                    }
                },
            )

            print(state)

    finally:
        db.close()


if __name__ == "__main__":
    main()