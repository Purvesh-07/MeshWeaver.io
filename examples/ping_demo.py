import asyncio
import time

from meshweaver.config import Config
from meshweaver.node import Node


async def handle_ping(message, addr):
    return "pong", message.get("body", {})


async def main():
    config1 = Config(host="127.0.0.1", port=9001)
    config2 = Config(host="127.0.0.1", port=9002)

    node1 = Node(config1)
    node2 = Node(config2)

    node2.on("ping", handle_ping)

    await node1.start()
    await node2.start()

    # Measure successful ping response time
    start_time = time.perf_counter()
    res = await node1.request(("127.0.0.1", 9002), "ping", {"hello": "world"})
    elapsed = (time.perf_counter() - start_time) * 1000

    if res:
        print(f"\nping rtt: {elapsed:.3f} ms")

    # Ping an unassigned port to test timeout behavior
    dead_res = await node1.request(("127.0.0.1", 9999), "ping", {})
    print(f"ping to a dead port: {dead_res}")

    await node1.stop()
    await node2.stop()


if __name__ == "__main__":
    asyncio.run(main())