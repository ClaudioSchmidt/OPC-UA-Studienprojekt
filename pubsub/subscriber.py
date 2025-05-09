import socket
import threading
from typing import Optional, Dict, Any
from .decoder import Decoder
from .registry import MachineRegistry

class SubscriberClient:
    def __init__(self, multicast_ip: str, port: int, local_ip: str):
        self.multicast_ip = multicast_ip
        self.port = port
        self.local_ip = local_ip

        self. decoder = Decoder()
        self.registry = MachineRegistry()

        self._running = False
        self._thread: Optional[threading.Thread] = None

        # UDP socket setup
        # AF_INET: IPv4, SOCK_DGRAM: UDP, IPPROTO_UDP: UDP protocol
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # SO_REUSEADDR: allows the socket to be bound to an address that is already in use
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # binds all local ip addresses to the given port
        self.sock.bind(('', port))

        # Join the multicast group
        # inet_aton: converts the IP address from string format to binary format
        multicast_request = socket.inet_aton(multicast_ip) + socket.inet_aton(local_ip)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, multicast_request)

        self.sock.settimeout(0.1) 

    def start_listening(self):
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()

    def _listen_loop(self):
        while self._running:
            try:
                data, addr = self.sock.recvfrom(65536) # max size of UDP packet
                machine_id, decoded = self.decoder.decode_packet(data)
                self.on_machine_update(machine_id, decoded)
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[SubscriberClient] Error: {e}")

    def on_machine_update(self, machine_id: int, data: Dict[str, Any]):
        self.registry.update_machine(machine_id, data)

    def stop_listening(self):
        if not self._running:
            return
        
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
            self._thread = None

        self.sock.close()