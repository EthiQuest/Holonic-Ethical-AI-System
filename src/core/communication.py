from typing import Dict, Any

class Message:
    def __init__(self, sender_id: str, receiver_id: str, content: Dict[str, Any]):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content

class CommunicationProtocol:
    @staticmethod
    def send_message(sender: 'Holon', receiver: 'Holon', content: Dict[str, Any]) -> None:
        message = Message(sender.id, receiver.id, content)
        # In a real system, this would involve network communication
        print(f"Sending message from {sender.name} to {receiver.name}: {content}")
        receiver.receive_message(message)

    @staticmethod
    def receive_message(receiver: 'Holon', message: Message) -> None:
        print(f"{receiver.name} received message: {message.content}")
        # Process the message based on its content
        if 'task' in message.content:
            result = receiver.execute_task(message.content['task'])
            # Send back the result
            CommunicationProtocol.send_message(receiver, sender, {'result': result})
