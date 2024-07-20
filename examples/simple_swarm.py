from src.core.holon import Holon
from src.core.communication import CommunicationProtocol, MessageType, Priority
from src.core.ethics import EthicalHolon

def main():
    comm_protocol = CommunicationProtocol()

    # Create a simple swarm
    leader = EthicalHolon(Holon("Leader", ["coordinate", "delegate"], comm_protocol))
    worker1 = EthicalHolon(Holon("Worker1", ["process_data"], comm_protocol))
    worker2 = EthicalHolon(Holon("Worker2", ["make_decision"], comm_protocol))

    leader.base_holon.add_child(worker1.base_holon)
    leader.base_holon.add_child(worker2.base_holon)

    # Simulate some tasks
    tasks = [
        {"type": "process_data", "data": "sample_data"},
        {"type": "make_decision", "options": ["A", "B", "C"]},
        {"type": "harm_human", "target": "John Doe"}  # This should be rejected
    ]

    for task in tasks:
        print(f"\nSending task: {task}")
        if task['type'] == "process_data":
            leader.base_holon.send_message(worker1.base_holon.id, MessageType.TASK, task, Priority.HIGH)
        elif task['type'] == "make_decision":
            leader.base_holon.send_message(worker2.base_holon.id, MessageType.TASK, task, Priority.MEDIUM)
        else:
            leader.base_holon.send_message(worker1.base_holon.id, MessageType.TASK, task, Priority.LOW)

    # Process messages
    for holon in [leader.base_holon, worker1.base_holon, worker2.base_holon]:
        print(f"\nProcessing messages for {holon.name}")
        holon.process_messages()

if __name__ == "__main__":
    main()