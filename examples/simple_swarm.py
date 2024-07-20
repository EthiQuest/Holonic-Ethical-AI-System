from src.core.holon import Holon
from src.core.communication import CommunicationProtocol
from src.core.ethics import EthicalHolon

def main():
    # Create a simple swarm
    leader = EthicalHolon(Holon("Leader", ["coordinate", "delegate"]))
    worker1 = EthicalHolon(Holon("Worker1", ["process_data"]))
    worker2 = EthicalHolon(Holon("Worker2", ["make_decision"]))

    leader.base_holon.add_child(worker1.base_holon)
    leader.base_holon.add_child(worker2.base_holon)

    # Simulate some tasks
    tasks = [
        {"type": "process_data", "data": "sample_data"},
        {"type": "make_decision", "options": ["A", "B", "C"]},
        {"type": "harm_human", "target": "John Doe"}  # This should be rejected
    ]

    for task in tasks:
        print(f"\nExecuting task: {task}")
        result = leader.execute_task(task)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
