from typing import List, Dict, Any
from src.core.holon import Holon
from src.core.communication import MessageType, Priority
import random

class RestructuringManager:
    def __init__(self, holons: List[Holon]):
        self.holons = holons
        self.performance_threshold = 0.7  # Threshold for triggering restructuring

    def evaluate_system_performance(self) -> float:
        # Simplified performance evaluation
        total_tasks = sum(len(h.state.get('pending_tasks', [])) for h in self.holons)
        total_capabilities = sum(len(h.capabilities) for h in self.holons)
        return 1 - (total_tasks / (total_capabilities + 1))  # +1 to avoid division by zero

    def needs_restructuring(self) -> bool:
        return self.evaluate_system_performance() < self.performance_threshold

    def restructure(self):
        print("Initiating system restructuring...")
        
        # 1. Identify overloaded and underutilized holons
        overloaded, underutilized = self._identify_workload_imbalance()
        
        # 2. Redistribute capabilities
        self._redistribute_capabilities(overloaded, underutilized)
        
        # 3. Adjust hierarchy
        self._adjust_hierarchy()
        
        # 4. Notify holons of changes
        self._notify_restructuring()

    def _identify_workload_imbalance(self):
        avg_workload = sum(len(h.state.get('pending_tasks', [])) for h in self.holons) / len(self.holons)
        overloaded = [h for h in self.holons if len(h.state.get('pending_tasks', [])) > avg_workload * 1.5]
        underutilized = [h for h in self.holons if len(h.state.get('pending_tasks', [])) < avg_workload * 0.5]
        return overloaded, underutilized

    def _redistribute_capabilities(self, overloaded: List[Holon], underutilized: List[Holon]):
        for over_h in overloaded:
            if underutilized:
                under_h = random.choice(underutilized)
                if over_h.capabilities:
                    capability = random.choice(over_h.capabilities)
                    over_h.capabilities.remove(capability)
                    under_h.capabilities.append(capability)
                    print(f"Moved capability {capability} from {over_h.name} to {under_h.name}")

    def _adjust_hierarchy(self):
        # Simplified hierarchy adjustment: randomly reassign some children
        for holon in self.holons:
            if holon.children and random.random() < 0.3:  # 30% chance to reassign a child
                child = random.choice(holon.children)
                new_parent = random.choice([h for h in self.holons if h != holon and h != child])
                holon.remove_child(child)
                new_parent.add_child(child)
                print(f"Moved {child.name} from {holon.name} to {new_parent.name}")

    def _notify_restructuring(self):
        for holon in self.holons:
            holon.send_message(holon.id, MessageType.RESTRUCTURE, {
                "new_capabilities": holon.capabilities,
                "new_parent": holon.parent.id if holon.parent else None,
                "new_children": [child.id for child in holon.children]
            }, Priority.HIGH)

class AdaptiveHolonManager:
    def __init__(self, comm_protocol):
        self.holons: List[Holon] = []
        self.task_allocator = TaskAllocator()
        self.comm_protocol = comm_protocol
        self.restructuring_manager = None

    def add_holon(self, holon: Holon):
        self.holons.append(holon)
        if len(self.holons) > 1 and not self.restructuring_manager:
            self.restructuring_manager = RestructuringManager(self.holons)

    def submit_task(self, task_type: str, content: Dict[str, Any], priority: Priority = Priority.MEDIUM):
        task = Task(task_type, content, priority)
        self.task_allocator.add_task(task)

    def process_cycle(self):
        # Allocate tasks
        allocated_tasks = self.task_allocator.allocate_tasks(self.holons)
        print(f"Allocated {allocated_tasks} tasks")

        # Process messages for each holon
        for holon in self.holons:
            while True:
                message = holon.receive_message()
                if not message:
                    break
                self._process_message(holon, message)

        # Check for completed tasks and system status
        self._check_system_status()

        # Check if restructuring is needed
        if self.restructuring_manager and self.restructuring_manager.needs_restructuring():
            self.restructuring_manager.restructure()

    def _process_message(self, holon: Holon, message):
        if message.type == MessageType.TASK:
            result = holon.execute_task(message.content)
            holon.send_message(message.sender_id, MessageType.RESULT, result)
            # Update holon state
            holon.state['pending_tasks'].remove(message.content['type'])
        elif message.type == MessageType.RESULT:
            print(f"{holon.name} received result: {message.content}")
        elif message.type == MessageType.RESTRUCTURE:
            print(f"{holon.name} restructured: {message.content}")
            # Update holon based on restructuring message
            holon.capabilities = message.content['new_capabilities']
            # Parent and children updates would be handled here in a full implementation

    def _check_system_status(self):
        for holon in self.holons:
            pending_tasks = len(holon.state.get('pending_tasks', []))
            print(f"{holon.name} has {pending_tasks} pending tasks")