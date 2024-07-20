import random
from typing import List, Dict, Any
from src.core.communication import Priority
import numpy as np

class TaskPattern:
    def __init__(self, task_type: str, frequency: float, priority_distribution: Dict[Priority, float],
                 complexity_range: tuple, dependencies: List[str] = None):
        self.task_type = task_type
        self.frequency = frequency
        self.priority_distribution = priority_distribution
        self.complexity_range = complexity_range
        self.dependencies = dependencies or []

class TaskGenerator:
    def __init__(self, patterns: List[TaskPattern]):
        self.patterns = patterns
        self.current_time = 0
        self.task_queue = []

    def generate_tasks(self, time_step: int) -> List[Dict[str, Any]]:
        self.current_time += time_step
        new_tasks = []

        for pattern in self.patterns:
            if random.random() < pattern.frequency * time_step:
                task = self._create_task(pattern)
                new_tasks.append(task)
                self.task_queue.append(task)

        # Process task queue for dependencies
        ready_tasks = [task for task in self.task_queue if self._dependencies_met(task)]
        self.task_queue = [task for task in self.task_queue if task not in ready_tasks]

        return ready_tasks

    def _create_task(self, pattern: TaskPattern) -> Dict[str, Any]:
        priority = random.choices(list(pattern.priority_distribution.keys()),
                                  weights=list(pattern.priority_distribution.values()))[0]
        complexity = random.uniform(*pattern.complexity_range)
        return {
            "type": pattern.task_type,
            "priority": priority,
            "complexity": complexity,
            "dependencies": pattern.dependencies.copy(),
            "created_at": self.current_time
        }

    def _dependencies_met(self, task: Dict[str, Any]) -> bool:
        return all(dep not in [t["type"] for t in self.task_queue] for dep in task["dependencies"])

class RealWorldScenarioGenerator:
    @staticmethod
    def create_data_processing_scenario() -> TaskGenerator:
        patterns = [
            TaskPattern("data_collection", 0.8, {Priority.LOW: 0.6, Priority.MEDIUM: 0.3, Priority.HIGH: 0.1},
                        (1, 5)),
            TaskPattern("data_cleaning", 0.6, {Priority.MEDIUM: 0.7, Priority.HIGH: 0.3},
                        (2, 8), ["data_collection"]),
            TaskPattern("data_analysis", 0.4, {Priority.MEDIUM: 0.4, Priority.HIGH: 0.6},
                        (5, 15), ["data_cleaning"]),
            TaskPattern("report_generation", 0.2, {Priority.HIGH: 1.0},
                        (3, 10), ["data_analysis"])
        ]
        return TaskGenerator(patterns)

    @staticmethod
    def create_manufacturing_scenario() -> TaskGenerator:
        patterns = [
            TaskPattern("supply_chain_management", 0.5, {Priority.MEDIUM: 0.7, Priority.HIGH: 0.3},
                        (2, 8)),
            TaskPattern("production_planning", 0.4, {Priority.HIGH: 1.0},
                        (5, 12), ["supply_chain_management"]),
            TaskPattern("quality_control", 0.7, {Priority.MEDIUM: 0.4, Priority.HIGH: 0.6},
                        (1, 5), ["production_planning"]),
            TaskPattern("maintenance", 0.3, {Priority.LOW: 0.3, Priority.MEDIUM: 0.5, Priority.HIGH: 0.2},
                        (2, 10)),
            TaskPattern("inventory_management", 0.6, {Priority.LOW: 0.2, Priority.MEDIUM: 0.6, Priority.HIGH: 0.2},
                        (1, 6), ["production_planning", "quality_control"])
        ]
        return TaskGenerator(patterns)

    @staticmethod
    def create_emergency_response_scenario() -> TaskGenerator:
        patterns = [
            TaskPattern("emergency_detection", 0.2, {Priority.HIGH: 1.0},
                        (1, 3)),
            TaskPattern("resource_allocation", 0.6, {Priority.HIGH: 1.0},
                        (3, 8), ["emergency_detection"]),
            TaskPattern("communication_coordination", 0.8, {Priority.MEDIUM: 0.3, Priority.HIGH: 0.7},
                        (2, 6), ["emergency_detection"]),
            TaskPattern("situation_assessment", 0.5, {Priority.HIGH: 1.0},
                        (4, 10), ["emergency_detection", "resource_allocation"]),
            TaskPattern("rescue_operation", 0.4, {Priority.HIGH: 1.0},
                        (5, 15), ["resource_allocation", "situation_assessment"])
        ]
        return TaskGenerator(patterns)

    @staticmethod
    def create_dynamic_scenario(duration: int) -> TaskGenerator:
        base_patterns = [
            TaskPattern("routine_task", 0.5, {Priority.LOW: 0.4, Priority.MEDIUM: 0.5, Priority.HIGH: 0.1},
                        (1, 5)),
            TaskPattern("urgent_task", 0.2, {Priority.HIGH: 1.0},
                        (3, 8))
        ]
        
        task_generator = TaskGenerator(base_patterns)
        
        def add_crisis_tasks(time: int):
            if 100 <= time < 150:
                crisis_pattern = TaskPattern("crisis_response", 0.8, {Priority.HIGH: 1.0}, (5, 10))
                task_generator.patterns.append(crisis_pattern)
            elif time >= 150:
                task_generator.patterns = [p for p in task_generator.patterns if p.task_type != "crisis_response"]
                recovery_pattern = TaskPattern("recovery_task", 0.4, {Priority.MEDIUM: 0.7, Priority.HIGH: 0.3}, (3, 7))
                task_generator.patterns.append(recovery_pattern)
        
        original_generate = task_generator.generate_tasks
        def new_generate(time_step: int):
            add_crisis_tasks(task_generator.current_time)
            return original_generate(time_step)
        
        task_generator.generate_tasks = new_generate
        return task_generator

# Usage example:
# scenario_generator = RealWorldScenarioGenerator()
# task_generator = scenario_generator.create_data_processing_scenario()
# tasks = task_generator.generate_tasks(1)  # Generate tasks for 1 time step