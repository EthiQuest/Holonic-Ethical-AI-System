import random
from typing import List, Dict, Any
from src.core.holon import Holon

class ExternalEvent:
    def __init__(self, event_type: str, target: str, duration: int, impact: Dict[str, Any]):
        self.event_type = event_type
        self.target = target
        self.duration = duration
        self.impact = impact
        self.start_cycle = None

    def __str__(self):
        return f"{self.event_type} affecting {self.target} for {self.duration} cycles"

class HardwareFailure(ExternalEvent):
    def __init__(self, target: str, duration: int):
        super().__init__("Hardware Failure", target, duration, {"operational": False})

class ResourceLimitation(ExternalEvent):
    def __init__(self, target: str, duration: int, resource_type: str, limit: float):
        super().__init__("Resource Limitation", target, duration, {resource_type: limit})

class ExternalEventGenerator:
    def __init__(self, holons: List[Holon], event_probability: float = 0.05):
        self.holons = holons
        self.event_probability = event_probability
        self.active_events: List[ExternalEvent] = []

    def generate_events(self, current_cycle: int) -> List[ExternalEvent]:
        new_events = []
        if random.random() < self.event_probability:
            event_type = random.choice(["hardware_failure", "resource_limitation"])
            target_holon = random.choice(self.holons)
            duration = random.randint(5, 20)

            if event_type == "hardware_failure":
                event = HardwareFailure(target_holon.name, duration)
            else:
                resource_type = random.choice(["cpu", "memory", "network"])
                limit = random.uniform(0.3, 0.7)
                event = ResourceLimitation(target_holon.name, duration, resource_type, limit)

            event.start_cycle = current_cycle
            new_events.append(event)
            self.active_events.append(event)
            print(f"New external event: {event}")

        return new_events

    def update_events(self, current_cycle: int) -> List[ExternalEvent]:
        resolved_events = []
        for event in self.active_events:
            if current_cycle - event.start_cycle >= event.duration:
                resolved_events.append(event)
                print(f"Resolved external event: {event}")

        self.active_events = [event for event in self.active_events if event not in resolved_events]
        return resolved_events

    def get_active_events(self) -> List[ExternalEvent]:
        return self.active_events

class ConstraintManager:
    @staticmethod
    def apply_constraints(holon: Holon, events: List[ExternalEvent]) -> None:
        for event in events:
            if event.target == holon.name:
                if isinstance(event, HardwareFailure):
                    holon.state['operational'] = event.impact['operational']
                elif isinstance(event, ResourceLimitation):
                    resource_type = list(event.impact.keys())[0]
                    holon.state[f'{resource_type}_limit'] = event.impact[resource_type]

    @staticmethod
    def remove_constraints(holon: Holon, events: List[ExternalEvent]) -> None:
        for event in events:
            if event.target == holon.name:
                if isinstance(event, HardwareFailure):
                    holon.state['operational'] = True
                elif isinstance(event, ResourceLimitation):
                    resource_type = list(event.impact.keys())[0]
                    holon.state.pop(f'{resource_type}_limit', None)