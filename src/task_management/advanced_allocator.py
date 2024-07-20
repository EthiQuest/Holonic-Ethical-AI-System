from typing import List, Dict, Any
from src.core.holon import Holon
from src.core.communication import MessageType, Priority
import numpy as np

class AdvancedTaskAllocator:
    def __init__(self, holons: List[Holon], performance_metrics):
        self.holons = holons
        self.performance_metrics = performance_metrics

    def allocate_task(self, task: Dict[str, Any]) -> Holon:
        capable_holons = [h for h in self.holons if task['type'] in h.capabilities]
        if not capable_holons:
            return None

        scores = self._calculate_allocation_scores(capable_holons, task)
        chosen_holon = capable_holons[np.argmax(scores)]
        return chosen_holon

    def _calculate_allocation_scores(self, holons: List[Holon], task: Dict[str, Any]) -> List[float]:
        scores = []
        for holon in holons:
            workload_score = self._calculate_workload_score(holon)
            performance_score = self._calculate_performance_score(holon, task['type'])
            priority_score = self._calculate_priority_score(task['priority'])
            energy_score = self._calculate_energy_score(holon)
            
            # Weighted sum of scores
            total_score = (0.3 * workload_score + 
                           0.3 * performance_score + 
                           0.2 * priority_score + 
                           0.2 * energy_score)
            scores.append(total_score)
        
        return scores

    def _calculate_workload_score(self, holon: Holon) -> float:
        pending_tasks = len(holon.state.get('pending_tasks', []))
        return 1 / (1 + pending_tasks)  # Higher score for fewer pending tasks

    def _calculate_performance_score(self, holon: Holon, task_type: str) -> float:
        return self.performance_metrics.get_task_success_rate(task_type)

    def _calculate_priority_score(self, priority: Priority) -> float:
        return {Priority.LOW: 0.33, Priority.MEDIUM: 0.66, Priority.HIGH: 1.0}[priority]

    def _calculate_energy_score(self, holon: Holon) -> float:
        energy_consumption = self.performance_metrics.get_energy_efficiency(holon.id)
        return 1 / (1 + energy_consumption)  # Higher score for lower energy consumption