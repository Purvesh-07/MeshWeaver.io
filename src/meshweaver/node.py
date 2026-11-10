import asyncio
import hashlib

from meshweaver.protocol import (
    create_message,
    decode_message,
    encode_message,
    verify_message,
)


class UDPProtocol(asyncio.DatagramProtocol):
    def __init__(self, node):
        self.node = node

    def datagram_received(self, data, addr):
        asyncio.create_task(
            self.node._handle_message(
                data,
                addr,
            )
        )


class Node:
    def __init__(self, config):
        self.config = config
        self.transport = None
        self.handlers = {}
        self.pending = {}
        self.addr = (
            config.host,
            config.port,
        )
        self.hex_id = hashlib.sha1(
            f"{config.host}:{config.port}".encode()
        ).hexdigest()

    def on(self, message_type, handler):
        self.handlers[message_type] = handler

    async def start(self):
        loop = asyncio.get_running_loop()
        transport, _ = await loop.create_datagram_endpoint(
            lambda: UDPProtocol(self),
            local_addr=self.addr,
        )
        self.transport = transport
        print(f"Node started on {self.addr}")

    async def stop(self):
        if self.transport:
            self.transport.close()
        await asyncio.sleep(0)

    async def _handle_message(self, raw_data, addr):
        message = decode_message(raw_data)

        if not verify_message(
            message,
            self.config.secret_key,
        ):
            return

        message_id = message["id"]

        if message_id in self.pending:
            future = self.pending.pop(message_id)
            if not future.done():
                future.set_result(message)
            return

        msg_type = message["type"]
        handler = self.handlers.get(msg_type)

        if not handler:
            return

        reply_type, reply_body = await handler(
            message,
            addr,
        )

        reply = create_message(
            reply_type,
            self.hex_id,
            reply_body,
            self.config.secret_key,
        )

        reply["id"] = message["id"]

        self.transport.sendto(
            encode_message(reply),
            addr,
        )

    async def request(self, address, msg_type, body):
        message = create_message(
            msg_type,
            self.hex_id,
            body,
            self.config.secret_key,
        )

        message_id = message["id"]
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        self.pending[message_id] = future

        self.transport.sendto(
            encode_message(message),
            address,
        )

        try:
            result = await asyncio.wait_for(
                future,
                timeout=self.config.request_timeout,
            )
            return result
        except asyncio.TimeoutError:
            self.pending.pop(message_id, None)
            return None