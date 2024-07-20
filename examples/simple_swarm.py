from src.core.holon import Holon
from src.core.communication import CommunicationProtocol, Priority
from src.core.ethics import EthicalHolon
from src.system_management.restructuring import AdaptiveHolonManager

def main():
    comm_protocol = CommunicationProtocol()
    holon_manager = AdaptiveHolonManager(comm_protocol)

    # Create a simple swarm
    leader = EthicalHolon(Holon("Leader", ["coordinate", "delegate"], comm_protocol))
    worker1 = EthicalHolon(Holon("Worker1", ["process_data"], comm_protocol))
    worker2 = EthicalHolon(Holon("Worker2", ["make_decision"], comm_protocol))
    worker3 = EthicalHolon(Holon("Worker3", ["analyze"], comm_protocol))

    holon_manager.add_holon(leader.base_holon)
    holon_manager.add_holon(worker1.base_holon)
    holon_manager.add_holon(worker2.base_holon)
    holon_manager.add_holon(worker3.base_holon)

    # Set up initial hierarchy
    leader.base_holon.add_child(worker1.base_holon)
    leader.base_holon.add_child(worker2.base_holon)
    worker2.base_holon.add_child(worker3.base_holon)

    # Run the system for several cycles with varying workloads
    for cycle in range(10):
        print(f"\nCycle {cycle + 1}:")
        
        # Submit tasks (varying workload to trigger restructuring)
        if cycle < 3:
            holon_manager.submit_task("process_data", {"data": f"sample_data_{cycle}"}, Priority.MEDIUM)
        elif cycle < 6:
            holon_manager.submit_task("make_decision", {"options": ["A", "B", "C"]}, Priority.HIGH)
            holon_manager.submit_task("analyze", {"data": f"analysis_data_{cycle}"}, Priority.LOW)
        else:
            holon_manager.submit_task("coordinate", {"action": "sync_workers"}, Priority.MEDIUM)
            holon_manager.submit_task("process_data", {"data": f"sample_data_{cycle}"}, Priority.HIGH)
            holon_manager.submit_task("make_decision", {"options": ["X", "Y", "Z"]}, Priority.LOW)

        holon_manager.process_cycle()

        # Print current system structure
        print("\nCurrent System Structure:")
        for holon in holon_manager.holons:
            print(f"{holon.name}: Capabilities={holon.capabilities}, "
                  f"Parent={holon.parent.name if holon.parent else 'None'}, "
                  f"Children={[child.name for child in holon.children]}")

if __name__ == "__main__":
    main()