"""Topic-based priority message broker with dead-letter queue support."""
import heapq
import time
from typing import Dict, List, Any, Optional


class MessageBroker:
    def __init__(self):
        # topic -> priority heap of (negative_priority, timestamp, message)
        self._queues: Dict[str, List[Any]] = {}
        self._dlq: List[Dict[str, Any]] = []
        self._counter = 0

    def publish(self, topic: str, payload: Any, priority: int = 5) -> None:
        if topic not in self._queues:
            self._queues[topic] = []
        self._counter += 1
        # Store with negative priority for max-heap behavior
        heapq.heappush(self._queues[topic], (-priority, self._counter, {
            "payload": payload,
            "topic": topic,
            "priority": priority,
            "published_at": time.time(),
            "retries": 0
        }))

    def pop(self, topic: str) -> Optional[Dict[str, Any]]:
        q = self._queues.get(topic)
        if not q:
            return None
        _, _, msg = heapq.heappop(q)
        return msg

    def nack(self, msg: Dict[str, Any], max_retries: int = 3) -> None:
        if msg["retries"] >= max_retries:
            self._dlq.append(msg)
        else:
            msg["retries"] += 1
            topic = msg["topic"]
            self._counter += 1
            heapq.heappush(self._queues[topic], (-msg["priority"], self._counter, msg))

    def get_dlq(self) -> List[Dict[str, Any]]:
        return list(self._dlq)
