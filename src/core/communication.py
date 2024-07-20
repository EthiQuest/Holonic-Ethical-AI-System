from enum import Enum, auto
from typing import Dict, Any, List, Optional
from queue import PriorityQueue
import uuid

class MessageType(Enum):
    TASK = auto()
    RESULT = auto()
    STATUS_UPDATE = auto()
    RESTRUCTURE = auto()
    QUERY = auto()

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class Message:
    def __init__(self, sender_id: str, receiver_id: str, msg_type: MessageType, 
                 content: Dict[str, Any], priority: Priority = Priority.MEDIUM):
        self.id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.type = msg_type
        self.content = content
        self.priority = priority

    def __lt__(self, other):
        return self.priority.value < other.priority.value

class MessageBus:
    def __init__(self):
        self.queues: Dict[str, PriorityQueue] = {}

    def register_holon(self, holon_id: str):
        if holon_id not in self.queues:
            self.queues[holon_id] = PriorityQueue()

    def send_message(self, message: Message):
        if message.receiver_id in self.queues:
            self.queues[message.receiver_id].put((-message.priority.value, message))
        else:
            print(f"Error: Receiver {message.receiver_id} not registered")

    def get_message(self, receiver_id: str) -> Optional[Message]:
        if receiver_id in self.queues and not self.queues[receiver_id].empty():
            return self.queues[receiver_id].get()[1]
        return None

class CommunicationProtocol:
    def __init__(self):
        self.message_bus = MessageBus()

    def register_holon(self, holon: 'Holon'):
        self.message_bus.register_holon(holon.id)

    def send_message(self, sender: 'Holon', receiver_id: str, msg_type: MessageType, 
                     content: Dict[str, Any], priority: Priority = Priority.MEDIUM):
        message = Message(sender.id, receiver_id, msg_type, content, priority)
        self.message_bus.send_message(message)
        print(f"Sent {msg_type.name} from {sender.name} to {receiver_id}: {content}")

    def receive_message(self, receiver: 'Holon') -> Optional[Message]:
        message = self.message_bus.get_message(receiver.id)
        if message:
            print(f"{receiver.name} received {message.type.name}: {message.content}")
        return message

    def broadcast(self, sender: 'Holon', receivers: List['Holon'], msg_type: MessageType, 
                  content: Dict[str, Any], priority: Priority = Priority.MEDIUM):
        for receiver in receivers:
            self.send_message(sender, receiver.id, msg_type, content, priority)

    def route_message(self, message: Message, holons: List['Holon']):
        for holon in holons:
            if holon.id == message.receiver_id:
                self.message_bus.send_message(message)
                return
            if message.receiver_id in [child.id for child in holon.children]:
                self.route_message(message, holon.children)
                return
        print(f"Error: Unable to route message to {message.receiver_id}")

# Example usage
if __name__ == "__main__":
    from src.core.holon import Holon

    comm_protocol = CommunicationProtocol()

    # Create some test holons
    holon1 = Holon("Holon1", ["capability1"])
    holon2 = Holon("Holon2", ["capability2"])
    comm_protocol.register_holon(holon1)
    comm_protocol.register_holon(holon2)

    # Send a message
    comm_protocol.send_message(holon1, holon2.id, MessageType.TASK, 
                               {"task": "do_something"}, Priority.HIGH)

    # Receive the message
    received_message = comm_protocol.receive_message(holon2)
    if received_message:
        print(f"Received message type: {received_message.type}")
        print(f"Message content: {received_message.content}")
        print(f"Message priority: {received_message.priority}")