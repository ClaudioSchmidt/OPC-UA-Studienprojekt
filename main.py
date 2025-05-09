import time, socket
from pubsub import SubscriberClient

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    multicast_ip = "239.0.0.1"
    port = 4840
    local_ip = get_local_ip()

    subscriber = SubscriberClient(multicast_ip, port, local_ip)
    subscriber.start_listening()

    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print("\n[Main] Interrupted by user.")
    
    print("[Main] Stopping subscriber...")
    subscriber.stop_listening()

    print("[Main] Final machine states:")
    for machine in subscriber.registry.get_all_machines():
        print(machine)

