import time
import threading
from typing import List, Dict, Any
from src.core.holon import Holon
from src.core.communication import CommunicationProtocol, Priority, MessageType
from src.core.ethics import EthicalHolon, SixPillarsEthicalFramework
from src.system_management.advanced_restructuring import AdvancedRestructuringManager
from src.task_management.advanced_allocator import AdvancedTaskAllocator
from src.task_management.task_generator import RealWorldScenarioGenerator
from src.events.external_events import ExternalEventGenerator, ConstraintManager
from src.visualization.dashboard_server import run_dashboard
from src.analysis.performance_analyzer import PerformanceAnalyzer

class AdvancedAdaptiveHolonManager:
    def __init__(self, comm_protocol: CommunicationProtocol):
        self.holons: List[Holon] = []
        self.comm_protocol = comm_protocol
        self.ethical_framework = SixPillarsEthicalFramework()
        self.performance_metrics = AdvancedPerformanceMetrics()
        self.restructuring_manager = None
        self.task_allocator = None
        self.event_generator = None
        self.constraint_manager = ConstraintManager()
        self.performance_analyzer = PerformanceAnalyzer()
        self.current_cycle = 0
        self.current_scenario = ""

    def add_holon(self, holon: Holon):
        ethical_holon = EthicalHolon(holon, self.ethical_framework)
        self.holons.append(ethical_holon)
        if len(self.holons) > 1:
            if not self.restructuring_manager:
                self.restructuring_manager = AdvancedRestructuringManager(self.holons, self.performance_metrics)
            if not self.task_allocator:
                self.task_allocator = AdvancedTaskAllocator(self.holons, self.performance_metrics)
            if not self.event_generator:
                self.event_generator = ExternalEventGenerator(self.holons)

    def submit_task(self, task_type: str, content: Dict[str, Any], priority: Priority = Priority.MEDIUM):
        task = {"type": task_type, "content": content, "priority": priority}
        ethical_assessment = self.ethical_framework.assess_task(task)
        if ethical_assessment['approved']:
            chosen_holon = self.task_allocator.allocate_task(task)
            if chosen_holon:
                chosen_holon.state.setdefault('pending_tasks', []).append(task_type)
                chosen_holon.send_message(chosen_holon.id, MessageType.TASK, task, priority)
            else:
                print(f"No suitable holon found for task {task_type}")
        else:
            print(f"Task {task_type} rejected due to ethical concerns: {ethical_assessment['reason']}")

    def process_cycle(self):
        # Generate and apply new events
        new_events = self.event_generator.generate_events(self.current_cycle)
        for event in new_events:
            for holon in self.holons:
                self.constraint_manager.apply_constraints(holon, [event])

        # Process messages and tasks
        for holon in self.holons:
            if holon.state.get('operational', True):  # Only process if the holon is operational
                while True:
                    message = holon.receive_message()
                    if not message:
                        break
                    self._process_message(holon, message)

        # Update and remove resolved events
        resolved_events = self.event_generator.update_events(self.current_cycle)
        for event in resolved_events:
            for holon in self.holons:
                self.constraint_manager.remove_constraints(holon, [event])

        performance = self.restructuring_manager.evaluate_system_performance()
        
        task_performances = {task_type: self.performance_metrics.get_task_success_rate(task_type)
                             for task_type in self.performance_metrics.task_success_rates}
        holon_performances = {holon.name: self.performance_metrics.get_average_resource_utilization(holon.id) 
                              for holon in self.holons}
        self.performance_analyzer.log_performance(self.current_cycle, self.current_scenario, 
                                                  performance, task_performances, holon_performances)

        if self.restructuring_manager.needs_restructuring():
            self.restructuring_manager.restructure()
            self.performance_analyzer.log_restructuring(self.current_cycle)

        self.current_cycle += 1

    def _process_message(self, holon: Holon, message):
        if message.type == MessageType.TASK:
            ethical_assessment = self.ethical_framework.assess_task(message.content)
            if ethical_assessment['approved']:
                result = holon.execute_task(message.content)
                holon.send_message(message.sender_id, MessageType.RESULT, result)
                task_completion_time = time.time() - message.timestamp
                self.performance_metrics.update_task_completion_time(message.content['type'], task_completion_time)
                self.performance_metrics.update_task_success(message.content['type'], result['status'] == 'success')
                holon.state['pending_tasks'].remove(message.content['type'])
            else:
                print(f"Holon {holon.name} rejected task due to ethical concerns: {ethical_assessment['reason']}")
        elif message.type == MessageType.RESULT:
            print(f"{holon.name} received result: {message.content}")
        elif message.type == MessageType.RESTRUCTURE:
            print(f"{holon.name} restructured: {message.content}")
            holon.capabilities = message.content['new_capabilities']
            # Handle parent and children updates here

def main():
    comm_protocol = CommunicationProtocol()
    holon_manager = AdvancedAdaptiveHolonManager(comm_protocol)

    # Create a diverse swarm with capabilities matching our scenarios
    leader = Holon("Leader", ["coordinate", "delegate", "situation_assessment"], comm_protocol)
    worker1 = Holon("Worker1", ["data_collection", "data_cleaning", "supply_chain_management"], comm_protocol)
    worker2 = Holon("Worker2", ["data_analysis", "report_generation", "production_planning"], comm_protocol)
    worker3 = Holon("Worker3", ["quality_control", "maintenance", "emergency_detection"], comm_protocol)
    worker4 = Holon("Worker4", ["inventory_management", "resource_allocation", "rescue_operation"], comm_protocol)
    worker5 = Holon("Worker5", ["communication_coordination", "routine_task", "urgent_task"], comm_protocol)

    for holon in [leader, worker1, worker2, worker3, worker4, worker5]:
        holon_manager.add_holon(holon)

    # Set up initial hierarchy
    leader.add_child(worker1)
    leader.add_child(worker2)
    worker1.add_child(worker3)
    worker2.add_child(worker4)
    worker2.add_child(worker5)

    # Create task generators for different scenarios
    scenario_generator = RealWorldScenarioGenerator()
    data_processing_generator = scenario_generator.create_data_processing_scenario()
    manufacturing_generator = scenario_generator.create_manufacturing_scenario()
    emergency_response_generator = scenario_generator.create_emergency_response_scenario()
    dynamic_generator = scenario_generator.create_dynamic_scenario(200)

    # Start the dashboard server in a separate thread
    dashboard_thread = threading.Thread(target=run_dashboard, args=(holon_manager,))
    dashboard_thread.start()

    # Run the system for several cycles with varying workloads and task types
    scenarios = ["Data Processing", "Manufacturing", "Emergency Response", "Dynamic Scenario"]
    scenario_duration = 50
    for cycle in range(200):
        holon_manager.current_cycle = cycle
        holon_manager.current_scenario = scenarios[cycle // scenario_duration]

        print(f"\nCycle {cycle + 1} - Scenario: {holon_manager.current_scenario}")
        
        # Generate tasks based on the current scenario
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

        # Add a small delay to slow down the simulation for better visualization
        time.sleep(0.5)

    # After all cycles, analyze and visualize the results
    holon_manager.performance_analyzer.analyze()
    holon_manager.performance_analyzer.plot_performance_over_time()
    holon_manager.performance_analyzer.plot_task_type_performance()
    holon_manager.performance_analyzer.plot_holon_performance()

    # Wait for the dashboard thread to finish
    dashboard_thread.join()

if __name__ == "__main__":
    main()