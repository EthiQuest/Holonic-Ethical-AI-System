import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any

class PerformanceAnalyzer:
    def __init__(self):
        self.scenario_performance = {}
        self.task_type_performance = {}
        self.holon_performance = {}
        self.restructuring_events = []

    def log_performance(self, cycle: int, scenario: str, overall_performance: float, 
                        task_performances: Dict[str, float], holon_performances: Dict[str, float]):
        if scenario not in self.scenario_performance:
            self.scenario_performance[scenario] = []
        self.scenario_performance[scenario].append((cycle, overall_performance))

        for task_type, performance in task_performances.items():
            if task_type not in self.task_type_performance:
                self.task_type_performance[task_type] = []
            self.task_type_performance[task_type].append((cycle, performance))

        for holon_name, performance in holon_performances.items():
            if holon_name not in self.holon_performance:
                self.holon_performance[holon_name] = []
            self.holon_performance[holon_name].append((cycle, performance))

    def log_restructuring(self, cycle: int):
        self.restructuring_events.append(cycle)

    def analyze(self):
        print("\nPerformance Analysis:")
        self._analyze_scenarios()
        self._analyze_task_types()
        self._analyze_holons()
        self._analyze_restructuring_impact()

    def _analyze_scenarios(self):
        print("\nScenario Analysis:")
        for scenario, performances in self.scenario_performance.items():
            avg_performance = np.mean([p for _, p in performances])
            print(f"{scenario}: Average Performance = {avg_performance:.2f}")

    def _analyze_task_types(self):
        print("\nTask Type Analysis:")
        for task_type, performances in self.task_type_performance.items():
            avg_performance = np.mean([p for _, p in performances])
            print(f"{task_type}: Average Performance = {avg_performance:.2f}")

    def _analyze_holons(self):
        print("\nHolon Analysis:")
        for holon, performances in self.holon_performance.items():
            avg_performance = np.mean([p for _, p in performances])
            print(f"{holon}: Average Performance = {avg_performance:.2f}")

    def _analyze_restructuring_impact(self):
        print("\nRestructuring Impact Analysis:")
        for event in self.restructuring_events:
            before = np.mean([p for c, p in self.scenario_performance[list(self.scenario_performance.keys())[-1]] if c < event and c >= event - 10])
            after = np.mean([p for c, p in self.scenario_performance[list(self.scenario_performance.keys())[-1]] if c > event and c <= event + 10])
            print(f"Restructuring at cycle {event}: Performance change = {after - before:.2f}")

    def plot_performance_over_time(self):
        plt.figure(figsize=(12, 6))
        for scenario, performances in self.scenario_performance.items():
            cycles, perf = zip(*performances)
            plt.plot(cycles, perf, label=scenario)
        plt.xlabel('Cycle')
        plt.ylabel('Performance')
        plt.title('System Performance Across Scenarios')
        plt.legend()
        for event in self.restructuring_events:
            plt.axvline(x=event, color='r', linestyle='--', alpha=0.5)
        plt.show()

    def plot_task_type_performance(self):
        plt.figure(figsize=(12, 6))
        for task_type, performances in self.task_type_performance.items():
            cycles, perf = zip(*performances)
            plt.plot(cycles, perf, label=task_type)
        plt.xlabel('Cycle')
        plt.ylabel('Performance')
        plt.title('Task Type Performance Over Time')
        plt.legend()
        plt.show()

    def plot_holon_performance(self):
        plt.figure(figsize=(12, 6))
        for holon, performances in self.holon_performance.items():
            cycles, perf = zip(*performances)
            plt.plot(cycles, perf, label=holon)
        plt.xlabel('Cycle')
        plt.ylabel('Performance')
        plt.title('Holon Performance Over Time')
        plt.legend()
        plt.show()