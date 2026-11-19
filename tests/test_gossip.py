
from meshweaver.gossip import Gossip


def test_ranking():
    g = Gossip()

    g.update("A", "127.0.0.1", 50, 50)
    g.update("B", "127.0.0.1", 10, 10)

    best = g.ranked()[0]

    assert best["cpu"] == 10


def test_mark_dead():
    g = Gossip()

    g.update("A", "127.0.0.1", 20, 20)

    g.mark_dead("A")

    assert len(g.peers) == 0