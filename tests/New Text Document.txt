from meshweaver.tasks import (
    serialize_task,
    execute_payload,
)

def square(x):
    return x * x

def test_execute():

    payload = serialize_task(
        square,
        (12,),
        {},
    )

    assert execute_payload(
        payload
    ) == 144

import pytest

from meshweaver.tasks import (
    serialize_task,
    execute_payload,
    RemoteTaskError,
)

def bad():
    return 1 / 0

def test_remote_error():

    payload = serialize_task(
        bad,
        (),
        {},
    )

    with pytest.raises(
        RemoteTaskError
    ):
        execute_payload(
            payload
        )