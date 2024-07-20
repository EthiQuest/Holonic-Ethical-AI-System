from typing import List, Dict, Any, Tuple
from src.core.holon import Holon
from src.core.communication import MessageType, Priority
import random
import time
import numpy as np
from sklearn.cluster import KMeans

class AdvancedPerformanceMetrics:
    def __init__(self):
        self.task_completion_times: Dict[str, List[float]] = {}
        self.energy_consumption: Dict[str, List[float]] = {}
        self.task_success_rates: Dict[str, List[bool]] = {}
        self.communication_overhead: Dict[Tuple[str, str], int] = {}
        self.resource_utilization: Dict[str, List[float]] = {}

    def update_task_completion_time(self, task_type: str, completion_time: float):
        if task_type not in self.task_completion_times:
            self.task_completion_times[task_type] = []
        self.task_completion_times[task_type].append(completion_time)

    def update_energy_consumption(self, holon_id: str, energy: float):
        if holon_id not in self.energy_consumption:
            self.energy_consumption[holon_id] = []
        self.energy_consumption[holon_id].append(energy)

    def update_task_success(self, task_type: str, success: bool):
        if task_type not in self.task_success_rates:
            self.task_success_rates[task_type] = []
        self.task_success_rates[task_type].append(success)

    def update_communication_overhead(self, sender_id: str, receiver_id: str):
        self.communication_overhead[(sender_id, receiver_id)] = self.communication_overhead.get((sender_id, receiver_id), 0) + 1

    def update_resource_utilization(self, holon_id: str, utilization: float):
        if holon_id not in self.resource_utilization:
            self.resource_utilization[holon_id] = []
        self.resource_utilization[holon_id].append(utilization)

    def get_average_completion_time(self, task_type: str) -> float:
        times = self.task_completion_times.get(task_type, [])
        return np.mean(times) if times else 0

    def get_energy_efficiency(self, holon_id: str) -> float:
        energy = self.energy_consumption.get(holon_id, [])
        return np.mean(energy) if energy else 0

    def get_task_success_rate(self, task_type: str) -> float:
        successes = self.task_success_rates.get(task_type, [])
        return np.mean(successes) if successes else 0

    def get_communication_efficiency(self) -> float:
        total_messages = sum(self.communication_overhead.values())
        unique_paths = len(self.communication_overhead)
        return unique_paths / total_messages if total_messages > 0 else 1

    def get_average_resource_utilization(self, holon_id: str) -> float:
        utilization = self.resource_utilization.get(holon_id, [])
        return np.mean(utilization) if utilization else 0

class AdvancedRestructuringManager:
    def __init__(self, holons: List[Holon]):
        self.holons = holons
        self.metrics = AdvancedPerformanceMetrics()
        self.last_restructure_time = 0
        self.restructure_cooldown = 5
        self.performance_history: List[float] = []

    def evaluate_system_performance(self) -> float:
        completion_time_score = self._evaluate_completion_time()
        energy_score = self._evaluate_energy_efficiency()
        success_rate_score = self._evaluate_success_rate()
        communication_score = self._evaluate_communication_efficiency()
        utilization_score = self._evaluate_resource_utilization()
        
        # Weighted average of scores
        performance = (0.25 * completion_time_score + 
                       0.2 * energy_score + 
                       0.25 * success_rate_score + 
                       0.15 * communication_score + 
                       0.15 * utilization_score)
        
        self.performance_history.append(performance)
        return performance

    def _evaluate_completion_time(self) -> float:
        avg_times = [self.metrics.get_average_completion_time(task_type) 
                     for task_type in self.metrics.task_completion_times]
        return 1 / (1 + np.mean(avg_times)) if avg_times else 1

    def _evaluate_energy_efficiency(self) -> float:
        efficiencies = [self.metrics.get_energy_efficiency(holon.id) for holon in self.holons]
        return 1 / (1 + np.mean(efficiencies)) if efficiencies else 1

    def _evaluate_success_rate(self) -> float:
        success_rates = [self.metrics.get_task_success_rate(task_type) 
                         for task_type in self.metrics.task_success_rates]
        return np.mean(success_rates) if success_rates else 1

    def _evaluate_communication_efficiency(self) -> float:
        return self.metrics.get_communication_efficiency()

    def _evaluate_resource_utilization(self) -> float:
        utilizations = [self.metrics.get_average_resource_utilization(holon.id) for holon in self.holons]
        return np.mean(utilizations) if utilizations else 0

    def needs_restructuring(self) -> bool:
        if time.time() - self.last_restructure_time < self.restructure_cooldown:
            return False
        if len(self.performance_history) < 10:
            return False
        recent_performance = np.mean(self.performance_history[-5:])
        overall_performance = np.mean(self.performance_history)
        return recent_performance < 0.9 * overall_performance

    def restructure(self):
        print("Initiating advanced system restructuring...")
        self.last_restructure_time = time.time()
        
        self._optimize_task_allocation()
        self._adjust_hierarchy_using_clustering()
        self._load_balancing()
        
        self._notify_restructuring()

    def _optimize_task_allocation(self):
        for holon in self.holons:
            best_tasks = self._identify_best_tasks(holon)
            current_capabilities = set(holon.capabilities)
            optimal_capabilities = set(best_tasks)
            
            # Add new optimal capabilities
            for task in optimal_capabilities - current_capabilities:
                holon.capabilities.append(task)
                print(f"Added capability {task} to {holon.name} for optimization")
            
            # Remove underperforming capabilities
            for task in current_capabilities - optimal_capabilities:
                if task in holon.capabilities:
                    holon.capabilities.remove(task)
                    print(f"Removed underperforming capability {task} from {holon.name}")

    def _identify_best_tasks(self, holon: Holon) -> List[str]:
        holon_tasks = set(holon.capabilities) | set(holon.state.get('pending_tasks', []))
        task_scores = {}
        for task in holon_tasks:
            completion_time = self.metrics.get_average_completion_time(task)
            success_rate = self.metrics.get_task_success_rate(task)
            task_scores[task] = success_rate / (1 + completion_time)
        return sorted(task_scores, key=task_scores.get, reverse=True)[:3]

    def _adjust_hierarchy_using_clustering(self):
        # Create feature vectors for each holon based on their performance metrics
        features = []
        for holon in self.holons:
            feature_vector = [
                self.metrics.get_average_completion_time(task) for task in holon.capabilities
            ] + [
                self.metrics.get_energy_efficiency(holon.id),
                self.metrics.get_average_resource_utilization(holon.id)
            ]
            features.append(feature_vector)
        
        # Perform K-means clustering
        n_clusters = min(len(self.holons) // 2, 5)  # Adjust the number of clusters as needed
        kmeans = KMeans(n_clusters=n_clusters)
        cluster_labels = kmeans.fit_predict(features)
        
        # Reorganize hierarchy based on clusters
        clusters = {}
        for i, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(self.holons[i])
        
        # Assign cluster leaders and reorganize
        for cluster in clusters.values():
            leader = max(cluster, key=lambda h: sum(self.metrics.get_task_success_rate(task) for task in h.capabilities))
            for holon in cluster:
                if holon != leader:
                    if holon.parent:
                        holon.parent.remove_child(holon)
                    leader.add_child(holon)
                    print(f"Moved {holon.name} under {leader.name} based on clustering")

    def _load_balancing(self):
        workloads = [len(h.state.get('pending_tasks', [])) for h in self.holons]
        avg_workload = np.mean(workloads)
        for i, holon in enumerate(self.holons):
            if workloads[i] > 1.5 * avg_workload:
                # Offload tasks to less busy holons
                tasks_to_offload = holon.state.get('pending_tasks', [])[:int(workloads[i] - avg_workload)]
                for task in tasks_to_offload:
                    target_holon = min(self.holons, key=lambda h: len(h.state.get('pending_tasks', [])))
                    if target_holon != holon:
                        holon.state['pending_tasks'].remove(task)
                        target_holon.state.setdefault('pending_tasks', []).append(task)
                        print(f"Offloaded task {task} from {holon.name} to {target_holon.name}")

    def _notify_restructuring(self):
        for holon in self.holons:
            holon.send_message(holon.id, MessageType.RESTRUCTURE, {
                "new_capabilities": holon.capabilities,
                "new_parent": holon.parent.id if holon.parent else None,
                "new_children": [child.id for child in holon.children]
            }, Priority.HIGH)

# The AdaptiveHolonManager class would need to be updated to use AdvancedRestructuringManager
# and AdvancedPerformanceMetrics instead of their previous versions.