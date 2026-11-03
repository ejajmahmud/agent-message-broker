"""Command-line interface for Agent Message Broker."""
import argparse
from .broker import MessageBroker

def main():
    parser = argparse.ArgumentParser(description="Agent Message Broker CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate priority queueing and DLQ")
    args = parser.parse_args()

    broker = MessageBroker()
    broker.publish("tasks", "Low priority cleanup", priority=1)
    broker.publish("tasks", "CRITICAL SECURITY HOTFIX", priority=10)

    first = broker.pop("tasks")
    print("First popped message (Priority):", first["priority"], "->", first["payload"])
    second = broker.pop("tasks")
    print("Second popped message (Priority):", second["priority"], "->", second["payload"])

if __name__ == "__main__":
    main()
