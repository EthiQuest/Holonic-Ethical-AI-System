from typing import List, Dict, Any
from src.core.holon import Holon
from src.core.communication import MessageType, Priority

class Task:
    def __init__(self, task_type: str, content: Dict[str, Any], priority: Priority = Priority.MEDIUM):
        self.type = task_type
        self.content = content
        self.priority = priority

class TaskAllocator:
    def __init__(self):
        self.task_queue: List[Task] = []

    def add_task(self, task: Task):
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda x: x.priority.value, reverse=True)

    def allocate_tasks(self, holons: List[Holon]):
        allocated_tasks = 0
        for task in self.task_queue[:]:
            allocated = self._allocate_single_task(task, holons)
            if allocated:
                self.task_queue.remove(task)
                allocated_tasks += 1
        return allocated_tasks

    def _allocate_single_task(self, task: Task, holons: List[Holon]) -> bool:
        capable_holons = [h for h in holons if task.type in h.capabilities]
        if not capable_holons:
            return False

        # Simple load balancing: choose the holon with the least pending tasks
        chosen_holon = min(capable_holons, key=lambda h: len(h.state.get('pending_tasks', [])))

        # Allocate the task
        chosen_holon.send_message(chosen_holon.id, MessageType.TASK, {
            'type': task.type,
            'content': task.content,
            'priority': task.priority
        })

        # Update holon state
        if 'pending_tasks' not in chosen_holon.state:
            chosen_holon.state['pending_tasks'] = []
        chosen_holon.state['pending_tasks'].append(task.type)

        print(f"Allocated task {task.type} to {chosen_holon.name}")
        return True

class HolonManager:
    def __init__(self, comm_protocol):
        self.holons: List[Holon] = []
        self.task_allocator = TaskAllocator()
        self.comm_protocol = comm_protocol

    def add_holon(self, holon: Holon):
        self.holons.append(holon)

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
                if message.type == MessageType.TASK:
                    result = holon.execute_task(message.content)
                    holon.send_message(message.sender_id, MessageType.RESULT, result)
                    # Update holon state
                    holon.state['pending_tasks'].remove(message.content['type'])
                elif message.type == MessageType.RESULT:
                    print(f"{holon.name} received result: {message.content}")

        # Check for completed tasks and system status
        self._check_system_status()

    def _check_system_status(self):
        for holon in self.holons:
            pending_tasks = len(holon.state.get('pending_tasks', []))
            print(f"{holon.name} has {pending_tasks} pending tasks")