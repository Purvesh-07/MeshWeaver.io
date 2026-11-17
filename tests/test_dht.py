from meshweaver.dht import xor_distance


def test_xor_distance():

    assert xor_distance(1, 3) == 2

from meshweaver.dht import DHT


def test_store():

    dht = DHT(100)

    dht.store(
        "hello",
        "world",
    )

    assert (
        dht.find_value("hello")
        == "world"
    )

from meshweaver.dht import (
    Peer,
    RoutingTable,
)


def test_remove_peer():

    table = RoutingTable(1)

    peer = Peer(
        2,
        "abc",
        "127.0.0.1",
        9002,
    )

    table.add_peer(peer)

    table.remove_peer(2)

    assert len(table.peers) == 0