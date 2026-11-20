import cloudpickle


class RemoteTaskError(Exception):
    pass


def serialize_task(
    func,
    args,
    kwargs,
):
    return cloudpickle.dumps(
        (
            func,
            args,
            kwargs,
        )
    )


def deserialize_task(
    payload,
):
    return cloudpickle.loads(
        payload
    )


def execute_payload(
    payload,
):
    try:

        func, args, kwargs = deserialize_task(
            payload
        )

        return func(
            *args,
            **kwargs,
        )

    except Exception as exc:

        raise RemoteTaskError(
            f"{type(exc).__name__}: {exc}"
        )