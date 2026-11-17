from dataclasses import dataclass


@dataclass(slots=True)
class Peer:
    node_id: int
    hex_id: str
    host: str
    port: int

    @property
    def address(self):
        return (self.host, self.port)


def xor_distance(a: int, b: int) -> int:
    return a ^ b


class RoutingTable:

    def __init__(self, owner_id: int):
        self.owner_id = owner_id
        self.peers = {}

    def add_peer(self, peer: Peer):
        self.peers[peer.node_id] = peer

    def remove_peer(self, node_id: int):
        self.peers.pop(node_id, None)

    def nearest(
        self,
        target_id: int,
        limit: int = 3,
    ):
        sorted_peers = sorted(
            self.peers.values(),
            key=lambda peer: xor_distance(
                peer.node_id,
                target_id,
            ),
        )

        return sorted_peers[:limit]


class DHT:

    def __init__(self, owner_id: int):
        self.owner_id = owner_id

        self.routing = RoutingTable(
            owner_id
        )

        self.storage = {}

    def store(
        self,
        key: str,
        value,
    ):
        self.storage[key] = value

    def find_value(
        self,
        key: str,
    ):
        return self.storage.get(key)

    def find_node(
        self,
        target_id: int,
        limit: int = 3,
    ):
        return self.routing.nearest(
            target_id,
            limit,
        )
