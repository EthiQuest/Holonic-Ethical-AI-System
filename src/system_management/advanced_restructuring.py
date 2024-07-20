from typing import List, Dict, Any
from src.core.holon import Holon
from src.core.communication import MessageType, Priority
import numpy as np
from sklearn.cluster import KMeans

class AdvancedRestructuringManager:
    def __init__(self, holons: List[Holon], performance_metrics):
        self.holons = holons
        self.performance_metrics = performance_metrics
        self.last_restructure_time = 0
        self.restructure_cooldown = 10
        self.performance_history = []

    def evaluate_system_performance(self) -> float:
        completion_time_score = self._evaluate_completion_time()
        energy_score = self._evaluate_energy_efficiency()
        success_rate_score = self._evaluate_success_rate()
        communication_score = self._evaluate_communication_efficiency()
        utilization_score = self._evaluate_resource_utilization()
        
        performance = (0.25 * completion_time_score + 
                       0.2 * energy_score + 
                       0.25 * success_rate_score + 
                       0.15 * communication_score + 
                       0.15 * utilization_score)
        
        self.performance_history.append(performance)
        return performance

    def needs_restructuring(self) -> bool:
        if len(self.performance_history) < 20:
            return False
        recent_performance = np.mean(self.performance_history[-10:])
        overall_performance = np.mean(self.performance_history)
        return recent_performance < 0.9 * overall_performance

    def restructure(self):
        print("Initiating advanced system restructuring...")
        self._optimize_capabilities()
        self._adjust_hierarchy()
        self._balance_workload()
        self._notify_restructuring()

    def _optimize_capabilities(self):
        for holon in self.holons:
            task_performances = {task: self.performance_metrics.get_task_success_rate(task) 
                                 for task in holon.capabilities}
            best_tasks = sorted(task_performances, key=task_performances.get, reverse=True)[:3]
            worst_task = min(task_performances, key=task_performances.get)
            
            if len(holon.capabilities) > 3 and task_performances[worst_task] < 0.5:
                holon.capabilities.remove(worst_task)
                print(f"Removed underperforming capability {worst_task} from {holon.name}")
            
            for task in best_tasks:
                if task not in holon.capabilities:
                    holon.capabilities.append(task)
                    print(f"Added high-performing capability {task} to {holon.name}")

    def _adjust_hierarchy(self):
        # Create feature vectors for each holon
        features = []
        for holon in self.holons:
            feature_vector = [
                self.performance_metrics.get_average_completion_time(task) for task in holon.capabilities
            ] + [
                self.performance_metrics.get_energy_efficiency(holon.id),
                self.performance_metrics.get_average_resource_utilization(holon.id)
            ]
            features.append(feature_vector)
        
        # Perform K-means clustering
        n_clusters = min(len(self.holons) // 2, 5)
        kmeans = KMeans(n_clusters=n_clusters)
        cluster_labels = kmeans.fit_predict(features)
        
        # Reorganize hierarchy based on clusters
        clusters = {}
        for i, label in enumerate(cluster_labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(self.holons[i])
        
        for cluster in clusters.values():
            leader = max(cluster, key=lambda h: sum(self.performance_metrics.get_task_success_rate(task) for task in h.capabilities))
            for holon in cluster:
                if holon != leader:
                    if holon.parent:
                        holon.parent.remove_child(holon)
                    leader.add_child(holon)
                    print(f"Moved {holon.name} under {leader.name} based on clustering")

    def _balance_workload(self):
        workloads = [len(h.state.get('pending_tasks', [])) for h in self.holons]
        avg_workload = np.mean(workloads)
        for i, holon in enumerate(self.holons):
            if workloads[i] > 1.5 * avg_workload:
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