import time
import socket
from pubsub.subscriber import SubscriberClient
from pubsub.registry import MachineRegistry
from flaskserver.server import FlaskServer
from flaskserver.sessionmanager import SessionManager

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def main():
    registry = MachineRegistry()
    sessions = SessionManager()

    subscriber = SubscriberClient(
        multicast_ip="239.0.0.1",
        port=4840,
        local_ip=get_local_ip()
    )
    subscriber.registry = registry

    flask_server = FlaskServer(
        registry=registry,
        session_manager=sessions
    )

    subscriber.start_listening()
    flask_server.run()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Main] Shutting down...")
        subscriber.stop_listening()
        print("[Main] Sessions saved.")

if __name__ == "__main__":
    main()
