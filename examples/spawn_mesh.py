import asyncio

from meshweaver.config import Config
from meshweaver.node import Node
from meshweaver.dht import DHT, Peer


async def main():

    nodes = []

    for i in range(10):

        port = 9000 + i

        node = Node(
            Config(port=port)
        )

        dht = DHT(port)

        node.register_dht_handlers(dht)

        nodes.append(
            (node, dht)
        )

    # start nodes

    for node, _ in nodes:
        await node.start()

    # bootstrap

    for i, (node, dht) in enumerate(nodes):

        bootstrap_peers = []

        for j in range(i):

            bootstrap_peers.append(
                Peer(
                    node_id=j,
                    hex_id=f"node-{j}",
                    host="127.0.0.1",
                    port=9000 + j,
                )
            )

        dht.bootstrap(
            bootstrap_peers
        )

    # show discovery

    for idx, (_, dht) in enumerate(nodes):

        print(
            f"Node {idx} knows "
            f"{len(dht.routing.peers)} peers"
        )

    # store value

    for _, dht in nodes:

        dht.store(
            "project",
            "meshweaver"
        )

    value = nodes[7][1].find_value(
        "project"
    )

    print(
        "Retrieved:",
        value,
    )

    if value == "meshweaver":
        print("AUDIT PASSED")
    else:
        print("AUDIT FAILED")

    # cleanup

    for node, _ in nodes:
        await node.stop()


if __name__ == "__main__":
    asyncio.run(main())