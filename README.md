# Replicated Log — Iteration 1

This is my implementation of the first iteration of the Replicated Log task.

The project is written in Python using FastAPI.

## What is implemented

- one Master node
- two Secondary nodes
- `POST /messages` on Master
- `GET /messages` on Master
- `GET /messages` on Secondary
- replication from Master to all Secondaries
- ACK using HTTP `200 OK`
- parallel replication
- artificial delay on Secondaries
- logging
- Docker containers
- simple integration test

Messages are stored only in memory, so they are lost after restarting the application.

## Project structure

```text
replicated-log/
│
├── Dockerfile
├── Dockerfile.secondary
├── master.py
├── secondary.py
├── requirements.txt
├── test_iteration1.py
└── README.md
```

## How it works

A client sends a message to the Master.

The Master stores the message in its local list and sends it to all Secondary nodes in parallel.

The Master returns a successful response only after all Secondaries return an ACK.

For testing, the Secondary nodes can have different delays.

For example:

```text
Secondary 1: 5 seconds
Secondary 2: 7 seconds
```

The Master response takes about 7 seconds, not 12 seconds, which shows that replication is running in parallel.

## Docker setup

The containers use the same Docker network:

```text
replicated-network
```

Master:

```text
http://127.0.0.1:8000
```

Secondary 1:

```text
http://127.0.0.1:8001
```

Secondary 2:

```text
http://127.0.0.1:8002
```

Swagger is available on `/docs`.

Example:

```text
http://127.0.0.1:8000/docs
```

## Integration test

Run:

```powershell
py test_iteration1.py
```

Example result:

```text
Response: {'status': 'ok'}
Duration: 7.17 seconds
```

This confirms that the Master waits for ACKs from all Secondaries and that replication runs in parallel.