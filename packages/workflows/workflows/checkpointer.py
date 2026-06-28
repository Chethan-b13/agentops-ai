from contextlib import contextmanager

from langgraph.checkpoint.postgres import PostgresSaver

from shared.settings import settings


@contextmanager
def create_checkpointer():

    conn_string = settings.postgres_url.replace(
        "+psycopg",
        "",
    )

    with PostgresSaver.from_conn_string(
        conn_string,
    ) as checkpointer:

        checkpointer.setup()

        yield checkpointer