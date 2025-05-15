import time
import socket
from pubsub.subscriber import SubscriberClient
from pubsub.registry import MachineRegistry
from flaskserver.server import FlaskServer
from flaskserver.sessionmanager import SessionManager
from gui.manager import GUIManager

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def main():
    local_ip = get_local_ip()

    registry = MachineRegistry()
    sessions = SessionManager()
    gui = GUIManager(flask_ip=f"http://{local_ip}:8000", registry=registry)

    subscriber = SubscriberClient(
        multicast_ip="239.0.0.1",
        port=4840,
        local_ip=local_ip,
        registry=registry
    )

    flask_server = FlaskServer(
        registry=registry,
        session_manager=sessions
    )

    subscriber.start_listening()
    flask_server.run()
    gui.show()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        subscriber.stop_listening()

if __name__ == "__main__":
    main()
