# MeshWeaver Architecture

Layers

- CLI / Dashboard
- Task Router
- Gossip Engine
- Kademlia DHT
- Security Layer
- UDP Control Plane
- TCP Task Plane

Task Flow

1. Submit task
2. Choose worker
3. TASK_OFFER
4. TASK_ACCEPT
5. Execute remotely
6. Return result
7. Retry if worker fails