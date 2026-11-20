from meshweaver.tasks import (
    serialize_task,
    execute_payload,
    RemoteTaskError,
)

def square(x):
    return x * x

payload = serialize_task(
    square,
    (12,),
    {},
)

print(
    "result from B:",
    execute_payload(payload),
)

def explode():
    return 1 / 0

try:

    payload = serialize_task(
        explode,
        (),
        {},
    )

    execute_payload(
        payload
    )

except RemoteTaskError as exc:

    print(
        "remote error was reported:",
        exc,
    )