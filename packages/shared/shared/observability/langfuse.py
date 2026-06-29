from langfuse import Langfuse

from shared.settings import settings

_langfuse: Langfuse | None = None


def initialize_langfuse() -> Langfuse:
    """
    Initialize the global Langfuse client.

    Should be called exactly once during application startup.
    """

    global _langfuse

    if _langfuse is not None:
        return _langfuse

    client = Langfuse(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        host=settings.langfuse_host,
    )

    if not client.auth_check():
        raise RuntimeError(
            "Failed to authenticate with Langfuse."
        )

    _langfuse = client

    return _langfuse


def get_langfuse() -> Langfuse:

    if _langfuse is None:
        raise RuntimeError(
            "Langfuse has not been initialized."
        )

    return _langfuse