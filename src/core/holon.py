import uuid
from typing import List, Dict, Any

class Holon:
    def __init__(self, name: str, capabilities: List[str]):
        self.id = str(uuid.uuid4())
        self.name = name
        self.capabilities = capabilities
        self.parent = None
        self.children: List[Holon] = []
        self.state: Dict[str, Any] = {}

    def add_child(self, child: 'Holon'):
        self.children.append(child)
        child.parent = self

    def remove_child(self, child: 'Holon'):
        self.children.remove(child)
        child.parent = None

    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # Basic task execution logic
        if task['type'] in self.capabilities:
            # Simulate task execution
            result = f"Executed task {task['type']} successfully"
            return {"status": "success", "result": result}
        else:
            # If not capable, try to delegate to children
            for child in self.children:
                result = child.execute_task(task)
                if result['status'] == 'success':
                    return result
            return {"status": "failure", "result": "No capable holon found for the task"}

    def update_state(self, new_state: Dict[str, Any]):
        self.state.update(new_state)

    def get_state(self) -> Dict[str, Any]:
        return self.state

    def __str__(self):
        return f"Holon(id={self.id}, name={self.name}, capabilities={self.capabilities})"
