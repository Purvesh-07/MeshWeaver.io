from meshweaver.protocol import (
    create_message,
    verify_message,
)


SECRET = "test-key"


def test_valid_message():
    msg = create_message(
        "PING",
        "nodeA",
        {},
        SECRET,
    )

    assert verify_message(msg, SECRET)


def test_tamper_detection():
    msg = create_message(
        "PING",
        "nodeA",
        {},
        SECRET,
    )

    msg["body"] = {"hacked": True}

    assert not verify_message(msg, SECRET)