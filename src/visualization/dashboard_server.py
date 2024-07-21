from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import threading
import time
import numpy as np

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

class DashboardServer:
    def __init__(self, holon_manager):
        self.holon_manager = holon_manager
        self.thread = None
        self.thread_lock = threading.Lock()
        self.holon_performance_history = {holon.name: [] for holon in holon_manager.holons}

    # ... (previous methods remain the same)

    
    def start(self):
        with self.thread_lock:
            if self.thread is None:
                self.thread = socketio.start_background_task(self.background_task)

    def background_task(self):
        while True:
            data = self.get_system_data()
            socketio.emit('system_update', data)
            socketio.sleep(1)

    def get_system_data(self):
        return {
            'holons': [self.holon_to_dict(h) for h in self.holon_manager.holons],
            'performance': self.holon_manager.restructuring_manager.evaluate_system_performance(),
            'active_events': [str(e) for e in self.holon_manager.event_generator.get_active_events()],
            'current_scenario': self.holon_manager.current_scenario,
            'current_cycle': self.holon_manager.current_cycle,
            'holon_performance': self.get_holon_performance(),
            'holon_network': self.get_holon_network()
        }

    def get_holon_network(self):
        nodes = []
        links = []
        for holon in self.holon_manager.holons:
            nodes.append({
                'id': holon.id,
                'name': holon.name,
                'capabilities': holon.capabilities
            })
            if holon.parent:
                links.append({
                    'source': holon.parent.id,
                    'target': holon.id
                })
        return {'nodes': nodes, 'links': links}

    def holon_to_dict(self, holon):
        return {
            'id': holon.id,
            'name': holon.name,
            'capabilities': holon.capabilities,
            'parent': holon.parent.name if holon.parent else None,
            'children': [child.name for child in holon.children],
            'pending_tasks': holon.state.get('pending_tasks', []),
            'operational': holon.state.get('operational', True),
            'resource_limits': {k: v for k, v in holon.state.items() if k.endswith('_limit')}
        }

    def get_holon_performance(self):
        performance_data = {}
        for holon in self.holon_manager.holons:
            tasks_completed = len(self.holon_manager.performance_metrics.task_success_rates.get(holon.name, []))
            success_rate = np.mean(self.holon_manager.performance_metrics.task_success_rates.get(holon.name, []))
            avg_completion_time = np.mean(self.holon_manager.performance_metrics.task_completion_times.get(holon.name, []))
            resource_utilization = self.holon_manager.performance_metrics.get_average_resource_utilization(holon.id)
            
            performance_data[holon.name] = {
                'tasks_completed': tasks_completed,
                'success_rate': success_rate,
                'avg_completion_time': avg_completion_time,
                'resource_utilization': resource_utilization
            }
            
            # Store historical data
            self.holon_performance_history[holon.name].append({
                'cycle': self.holon_manager.current_cycle,
                'success_rate': success_rate,
                'resource_utilization': resource_utilization
            })
        
        return performance_data

@app.route('/holon_network')
def holon_network():
    return jsonify(dashboard_server.get_holon_network())
    
@app.route('/system_data')
def system_data():
    return jsonify(dashboard_server.get_system_data())

@app.route('/holon_performance_history')
def holon_performance_history():
    return jsonify(dashboard_server.holon_performance_history)

@socketio.on('intervene')
def handle_intervention(data):
    intervention_type = data['type']
    target = data['target']
    if intervention_type == 'add_capability':
        holon = next((h for h in dashboard_server.holon_manager.holons if h.name == target), None)
        if holon:
            holon.capabilities.append(data['capability'])
    elif intervention_type == 'remove_capability':
        holon = next((h for h in dashboard_server.holon_manager.holons if h.name == target), None)
        if holon and data['capability'] in holon.capabilities:
            holon.capabilities.remove(data['capability'])
    elif intervention_type == 'trigger_restructuring':
        dashboard_server.holon_manager.restructuring_manager.restructure()
    
    socketio.emit('system_update', dashboard_server.get_system_data())

dashboard_server = None

def run_dashboard(holon_manager):
    global dashboard_server
    dashboard_server = DashboardServer(holon_manager)
    dashboard_server.start()
    socketio.run(app, debug=True, use_reloader=False)

if __name__ == '__main__':
    # This part is for testing the server independently
    class MockHolonManager:
        def __init__(self):
            self.holons = [Holon(f"Holon{i}", ["capability1", "capability2"], None) for i in range(5)]
            self.restructuring_manager = MockRestructuringManager()
            self.event_generator = MockEventGenerator()
            self.current_scenario = "Test Scenario"
            self.current_cycle = 0
            self.performance_metrics = MockPerformanceMetrics()

    class MockRestructuringManager:
        def evaluate_system_performance(self):
            return 0.75

    class MockEventGenerator:
        def get_active_events(self):
            return ["Mock Event 1", "Mock Event 2"]

    class MockPerformanceMetrics:
        def __init__(self):
            self.task_success_rates = {f"Holon{i}": [True, False, True] for i in range(5)}
            self.task_completion_times = {f"Holon{i}": [1.0, 2.0, 1.5] for i in range(5)}

        def get_average_resource_utilization(self, holon_id):
            return 0.6

    run_dashboard(MockHolonManager())
