import socket
import struct
import time

MULTICAST_IP = "239.0.0.1"
PORT = 4840
PUBLISHER_ID = 1001  # = machine_id
SEQUENCE_NUMBER = 1

def build_payload() -> bytes:
    return struct.pack(
        "<B?hBII?B?B?B?dB?????B???",
        1,      # sorting_state
        True,   # remote_control_is_enabled
        0,      # status_code (int16)
        2,      # sorting_criterion
        5,      # workpiece_counter_slide_a
        7,      # workpiece_counter_slide_b
        False,  # app_btn
        1,      # app_led
        False,  # process_btn
        2,      # process_led
        True,   # fault_ack_btn
        3,      # fault_ack_led
        False,  # emergency_btn
        1.25,   # belt_speed
        2,      # belt_speed_level
        True,   # is_running
        False,  # is_reverse
        True,   # switch
        True,   # start_sensor
        True,   # id_sensor
        1,      # color_channel
        False,  # inductive_sensor
        False,  # switch_sensor
        True    # storage_sensor
    )

def build_uadp_packet(seq_num: int) -> bytes:
    header = bytearray()
    version = 1
    flags = 0x03
    version_flags = (version << 4) | flags
    header.append(version_flags)

    header += struct.pack("<H", PUBLISHER_ID)
    header += struct.pack("<I", seq_num)

    payload = build_payload()
    return bytes(header + payload)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    print("[Publisher] Sending packets...")

    seq = SEQUENCE_NUMBER
    try:
        while True:
            packet = build_uadp_packet(seq)
            sock.sendto(packet, (MULTICAST_IP, PORT))
            print(f"[Publisher] Sent packet #{seq}")
            seq += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
