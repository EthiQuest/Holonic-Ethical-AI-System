from src.core.holon import Holon
from src.core.communication import CommunicationProtocol, Priority
from src.core.ethics import EthicalHolon
from src.system_management.advanced_restructuring import AdvancedRestructuringManager
from src.task_management.advanced_allocator import AdvancedTaskAllocator
from src.visualization.system_visualizer import SystemVisualizer
from src.task_management.task_generator import RealWorldScenarioGenerator
from src.analysis.performance_analyzer import PerformanceAnalyzer
import random

class AdvancedAdaptiveHolonManager:
    def __init__(self, comm_protocol):
        self.holons: List[Holon] = []
        self.comm_protocol = comm_protocol
        self.performance_metrics = AdvancedPerformanceMetrics()
        self.restructuring_manager = None
        self.task_allocator = None
        self.visualizer = SystemVisualizer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.current_cycle = 0
        self.current_scenario = ""

    def add_holon(self, holon: Holon):
        self.holons.append(holon)
        if len(self.holons) > 1:
            if not self.restructuring_manager:
                self.restructuring_manager = AdvancedRestructuringManager(self.holons, self.performance_metrics)
            if not self.task_allocator:
                self.task_allocator = AdvancedTaskAllocator(self.holons, self.performance_metrics)

    def submit_task(self, task_type: str, content: Dict[str, Any], priority: Priority = Priority.MEDIUM):
        task = {"type": task_type, "content": content, "priority": priority}
        chosen_holon = self.task_allocator.allocate_task(task)
        if chosen_holon:
            chosen_holon.state.setdefault('pending_tasks', []).append(task_type)
            chosen_holon.send_message(chosen_holon.id, MessageType.TASK, task, priority)
        else:
            print(f"No suitable holon found for task {task_type}")

    def process_cycle(self):
        for holon in self.holons:
            while True:
                message = holon.receive_message()
                if not message:
                    break
                self._process_message(holon, message)

        performance = self.restructuring_manager.evaluate_system_performance()
        self.visualizer.update(self.holons, performance)
        
        task_performances = {task_type: self.performance_metrics.get_task_success_rate(task_type)
                             for task_type in self.performance_metrics.task_success_rates}
        holon_performances = {holon.name: self.performance_metrics.get_average_resource_utilization(holon.id) 
                              for holon in self.holons}
        self.performance_analyzer.log_performance(self.current_cycle, self.current_scenario, 
                                                  performance, task_performances, holon_performances)

        if self.restructuring_manager.needs_restructuring():
            self.restructuring_manager.restructure()
            self.performance_analyzer.log_restructuring(self.current_cycle)

    def _process_message(self, holon: Holon, message):
        if message.type == MessageType.TASK:
            result = holon.execute_task(message.content)
            holon.send_message(message.sender_id, MessageType.RESULT, result)
            task_completion_time = random.uniform(0.5, 2.0)  # Simulated task completion time
            self.performance_metrics.update_task_completion_time(message.content['type'], task_completion_time)
            self.performance_metrics.update_task_success(message.content['type'], result['status'] == 'success')
            holon.state['pending_tasks'].remove(message.content['type'])
        elif message.type == MessageType.RESULT:
            print(f"{holon.name} received result: {message.content}")
        elif message.type == MessageType.RESTRUCTURE:
            print(f"{holon.name} restructured: {message.content}")
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
    scenarios = ["Data Processing", "Manufacturing", "Emergency Response", "Dynamic Scenario"]
    scenario_duration = 50
    for cycle in range(200):
        holon_manager.current_cycle = cycle