import time


class Gossip:
    def __init__(self):
        self.peers = {}

    def update(self, node_id, address, cpu, memory):
        self.peers[node_id] = {
            "address": address,
            "cpu": cpu,
            "memory": memory,
            "timestamp": time.time(),
        }

    def mark_dead(self, node_id):
        self.peers.pop(node_id, None)

    def ranked(self, excluded=None, inflight=None):
        excluded = excluded or set()

        candidates = [
            data
            for node_id, data in self.peers.items()
            if node_id not in excluded
        ]

        return sorted(
            candidates,
            key=lambda x: (x["cpu"], x["memory"])
        )