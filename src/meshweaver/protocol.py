import json
import uuid
import hmac
import hashlib


def sign_message(payload: dict, secret: str) -> str:
    raw = json.dumps(payload, sort_keys=True).encode()

    return hmac.new(
        secret.encode(),
        raw,
        hashlib.sha256
    ).hexdigest()


def create_message(
    message_type: str,
    sender: str,
    body: dict,
    secret: str,
):
    msg = {
        "id": str(uuid.uuid4()),
        "type": message_type,
        "sender": sender,
        "body": body,
    }

    msg["signature"] = sign_message(msg, secret)

    return msg


def verify_message(message: dict, secret: str) -> bool:
    signature = message.get("signature")

    if not signature:
        return False

    unsigned = dict(message)
    unsigned.pop("signature")

    expected = sign_message(unsigned, secret)

    return hmac.compare_digest(
        signature,
        expected
    )