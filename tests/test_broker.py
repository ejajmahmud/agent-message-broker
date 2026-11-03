"""Unit tests for MessageBroker."""
import unittest
from agent_message_broker.broker import MessageBroker

class TestMessageBroker(unittest.TestCase):
    def test_priority_ordering(self):
        b = MessageBroker()
        b.publish("t", "low", priority=1)
        b.publish("t", "high", priority=10)
        self.assertEqual(b.pop("t")["payload"], "high")
        self.assertEqual(b.pop("t")["payload"], "low")

    def test_dead_letter_queue(self):
        b = MessageBroker()
        b.publish("t", "bad_msg")
        m = b.pop("t")
        for _ in range(4):
            b.nack(m, max_retries=2)
            m = b.pop("t")
            if not m:
                break
        self.assertEqual(len(b.get_dlq()), 1)

if __name__ == "__main__":
    unittest.main()
