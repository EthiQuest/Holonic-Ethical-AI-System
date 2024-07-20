from src.core.holon import Holon
from src.core.communication import CommunicationProtocol, Priority
from src.core.ethics import EthicalHolon
from src.task_management.allocator import HolonManager

def main():
    comm_protocol = CommunicationProtocol()
    holon_manager = HolonManager(comm_protocol)

    # Create a simple swarm
    leader = EthicalHolon(Holon("Leader", ["coordinate", "delegate"], comm_protocol))
    worker1 = EthicalHolon(Holon("Worker1", ["process_data"], comm_protocol))
    worker2 = EthicalHolon(Holon("Worker2", ["make_decision"], comm_protocol))

    holon_manager.add_holon(leader.base_holon)
    holon_manager.add_holon(worker1.base_holon)
    holon_manager.add_holon(worker2.base_holon)

    # Submit some tasks
    holon_manager.submit_task("process_data", {"data": "sample_data_1"}, Priority.HIGH)
    holon_manager.submit_task("make_decision", {"options": ["A", "B", "C"]}, Priority.MEDIUM)
    holon_manager.submit_task("process_data", {"data": "sample_data_2"}, Priority.LOW)
    holon_manager.submit_task("coordinate", {"action": "sync_workers"}, Priority.HIGH)
    holon_manager.submit_task("harm_human", {"target": "John Doe"}, Priority.LOW)  # This should be rejected

    # Run the system for a few cycles
    for _ in range(5):
        print("\nProcessing cycle:")
        holon_manager.process_cycle()

if __name__ == "__main__":
    main()