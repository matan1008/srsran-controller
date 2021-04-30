from contextlib import contextmanager


@contextmanager
def shutdown_on_error(instance):
    try:
        yield instance
    except Exception:
        instance.shutdown()
        raise
