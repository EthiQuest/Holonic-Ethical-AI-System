import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Dict
from src.core.holon import Holon

class SystemVisualizer:
    def __init__(self):
        self.performance_history = []
        self.structure_history = []

    def update(self, holons: List[Holon], performance: float):
        self.performance_history.append(performance)
        self.structure_history.append(self._capture_structure(holons))

    def _capture_structure(self, holons: List[Holon]) -> Dict:
        return {
            holon.id: {
                'name': holon.name,
                'capabilities': holon.capabilities,
                'parent': holon.parent.id if holon.parent else None,
                'children': [child.id for child in holon.children]
            }
            for holon in holons
        }

    def plot_performance(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.performance_history)
        plt.title('System Performance Over Time')
        plt.xlabel('Cycle')
        plt.ylabel('Performance Score')
        plt.ylim(0, 1)
        plt.show()

    def plot_structure(self, cycle: int):
        structure = self.structure_history[cycle]
        G = nx.Graph()
        
        for holon_id, data in structure.items():
            G.add_node(holon_id, name=data['name'], capabilities=', '.join(data['capabilities']))
            if data['parent']:
                G.add_edge(data['parent'], holon_id)
        
        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=False, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
        
        nx.draw_networkx_labels(G, pos, {node: f"{data['name']}\n{', '.join(data['capabilities'])}" 
                                         for node, data in structure.items()})
        
        plt.title(f'System Structure at Cycle {cycle}')
        plt.axis('off')
        plt.show()

    def animate_structure_changes(self):
        # This method would create an animation of structure changes over time
        # For simplicity, we'll just plot the initial and final structures
        self.plot_structure(0)
        self.plot_structure(-1)

# Usage in main script:
# visualizer = SystemVisualizer()
# In each cycle:
# visualizer.update(holon_manager.holons, performance)
# After all cycles:
# visualizer.plot_performance()
# visualizer.animate_structure_changes()