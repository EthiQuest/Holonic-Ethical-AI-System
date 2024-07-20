from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import threading
import time
from src.core.holon import Holon
from src.system_management.advanced_restructuring import AdvancedRestructuringManager
from src.task_management.advanced_allocator import AdvancedTaskAllocator

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

class DashboardServer:
    def __init__(self, holon_manager):
        self.holon_manager = holon_manager
        self.thread = None
        self.thread_lock = threading.Lock()

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
            'current_cycle': self.holon_manager.current_cycle
        }

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

@app.route('/system_data')
def system_data():
    return jsonify(dashboard_server.get_system_data())

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
    # Add more intervention types as needed

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
            self.restructuring_manager = AdvancedRestructuringManager(self.holons, None)
            self.event_generator = MockEventGenerator()
            self.current_scenario = "Test Scenario"
            self.current_cycle = 0

    class MockEventGenerator:
        def get_active_events(self):
            return ["Mock Event 1", "Mock Event 2"]

    run_dashboard(MockHolonManager())