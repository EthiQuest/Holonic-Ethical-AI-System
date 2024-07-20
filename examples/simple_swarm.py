from src.core.holon import Holon
from src.core.communication import CommunicationProtocol, Priority
from src.core.ethics import EthicalHolon
from src.system_management.restructuring import AdvancedRestructuringManager, AdvancedPerformanceMetrics
from src.visualization.system_visualizer import SystemVisualizer
from src.task_management.task_generator import RealWorldScenarioGenerator
import random

class AdvancedAdaptiveHolonManager:
    def __init__(self, comm_protocol):
        self.holons: List[Holon] = []
        self.comm_protocol = comm_protocol
        self.performance_metrics = AdvancedPerformanceMetrics()
        self.restructuring_manager = None
        self.visualizer = SystemVisualizer()

    def add_holon(self, holon: Holon):
        self.holons.append(holon)
        if len(self.holons) > 1 and not self.restructuring_manager:
            self.restructuring_manager = AdvancedRestructuringManager(self.holons)

    def submit_task(self, task_type: str, content: Dict[str, Any], priority: Priority = Priority.MEDIUM):
        capable_holons = [h for h in self.holons if task_type in h.capabilities]
        if capable_holons:
            chosen_holon = min(capable_holons, key=lambda h: len(h.state.get('pending_tasks', [])))
            chosen_holon.state.setdefault('pending_tasks', []).append(task_type)
            chosen_holon.send_message(chosen_holon.id, MessageType.TASK, {"type": task_type, "content": content}, priority)

    def process_cycle(self):
        cycle_start_time = time.time()
        
        # Process messages for each holon
        for holon in self.holons:
            while True:
                message = holon.receive_message()
                if not message:
                    break
                self._process_message(holon, message, cycle_start_time)

        # Update performance metrics
        performance = self.restructuring_manager.evaluate_system_performance()
        self.visualizer.update(self.holons, performance)

        # Check if restructuring is needed
        if self.restructuring_manager.needs_restructuring():
            self.restructuring_manager.restructure()

        # Update energy consumption (simplified model)
        cycle_duration = time.time() - cycle_start_time
        for holon in self.holons:
            energy_consumed = len(holon.state.get('pending_tasks', [])) * cycle_duration
            self.performance_metrics.update_energy_consumption(holon.id, energy_consumed)
            self.performance_metrics.update_resource_utilization(holon.id, len(holon.state.get('pending_tasks', [])) / 10)  # Simplified utilization metric

    def _process_message(self, holon: Holon, message, cycle_start_time):
        if message.type == MessageType.TASK:
            result = holon.execute_task(message.content)
            holon.send_message(message.sender_id, MessageType.RESULT, result)
            # Update performance metrics
            task_completion_time = time.time() - cycle_start_time
            self.performance_metrics.update_task_completion_time(message.content['type'], task_completion_time)
            self.performance_metrics.update_task_success(message.content['type'], result['status'] == 'success')
            # Update holon state
            holon.state['pending_tasks'].remove(message.content['type'])
        elif message.type == MessageType.RESULT:
            print(f"{holon.name} received result: {message.content}")
        elif message.type == MessageType.RESTRUCTURE:
            print(f"{holon.name} restructured: {message.content}")
            # Update holon based on restructuring message
            holon.capabilities = message.content['new_capabilities']
            # Parent and children updates would be handled here in a full implementation

def main():
    comm_protocol = CommunicationProtocol()
    holon_manager = AdvancedAdaptiveHolonManager(comm_protocol)

    # Create a more diverse swarm with capabilities matching our scenarios
    leader = EthicalHolon(Holon("Leader", ["coordinate", "delegate", "situation_assessment"], comm_protocol))
    worker1 = EthicalHolon(Holon("Worker1", ["data_collection", "data_cleaning", "supply_chain_management"], comm_protocol))
    worker2 = EthicalHolon(Holon("Worker2", ["data_analysis", "report_generation", "production_planning"], comm_protocol))
    worker3 = EthicalHolon(Holon("Worker3", ["quality_control", "maintenance", "emergency_detection"], comm_protocol))
    worker4 = EthicalHolon(Holon("Worker4", ["inventory_management", "resource_allocation", "rescue_operation"], comm_protocol))
    worker5 = EthicalHolon(Holon("Worker5", ["communication_coordination", "routine_task", "urgent_task"], comm_protocol))

    for holon in [leader, worker1, worker2, worker3, worker4, worker5]:
        holon_manager.add_holon(holon.base_holon)

    # Set up initial hierarchy
    leader.base_holon.add_child(worker1.base_holon)
    leader.base_holon.add_child(worker2.base_holon)
    worker1.base_holon.add_child(worker3.base_holon)
    worker2.base_holon.add_child(worker4.base_holon)
    worker2.base_holon.add_child(worker5.base_holon)

    # Create task generators for different scenarios
    scenario_generator = RealWorldScenarioGenerator()
    data_processing_generator = scenario_generator.create_data_processing_scenario()
    manufacturing_generator = scenario_generator.create_manufacturing_scenario()
    emergency_response_generator = scenario_generator.create_emergency_response_scenario()
    dynamic_generator = scenario_generator.create_dynamic_scenario(200)

    # Run the system for several cycles with varying workloads and task types
    for cycle in range(200):
        print(f"\nCycle {cycle + 1}:")
        
        # Generate tasks from different scenarios
        if cycle < 50:
            tasks = data_processing_generator.generate_tasks(1)
        elif cycle < 100:
            tasks = manufacturing_generator.generate_tasks(1)
        elif cycle < 150:
            tasks = emergency_response_generator.generate_tasks(1)
        else:
            tasks = dynamic_generator.generate_tasks(1)

        # Submit generated tasks
        for task in tasks:
            holon_manager.submit_task(task["type"], task, task["priority"])

        holon_manager.process_cycle()

        # Print current system structure and performance every 20 cycles
        if cycle % 20 == 0:
            print("\nCurrent System Structure and Performance:")
            for holon in holon_manager.holons:
                print(f"{holon.name}: Capabilities={holon.capabilities}, "
                      f"Parent={holon.parent.name if holon.parent else 'None'}, "
                      f"Children={[child.name for child in holon.children]}")
            
            performance = holon_manager.restructuring_manager.evaluate_system_performance()
            print(f"Overall System Performance: {performance:.2f}")

    # After all cycles, visualize the results
    holon_manager.visualizer.plot_performance()
    holon_manager.visualizer.animate_structure_changes()

if __name__ == "__main__":
    main()