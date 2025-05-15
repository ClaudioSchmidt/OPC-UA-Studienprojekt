import socket
import struct
import time

MULTICAST_IP = "239.0.0.1"
PORT = 4840
PUBLISHER_ID = 1001
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
        True,   # app_btn
        1,      # app_led
        True,   # process_btn
        2,      # process_led
        True,   # fault_ack_btn
        3,      # fault_ack_led
        False,  # emergency_btn
        1.25,   # belt_speed
        2,      # belt_speed_level
        True,   # is_running
        False,  # is_reverse
        False,  # switch
        False,  # start_sensor
        False,  # id_sensor
        1,      # color_channel
        True,   # inductive_sensor
        False,  # switch_sensor
        False   # storage_sensor
    )

def build_uadp_packet(publisher_id: int, seq_num: int) -> bytes:
    header = bytearray()
    version = 1
    flags = 0x03
    version_flags = (version << 4) | flags
    header.append(version_flags)

    header += struct.pack("<H", publisher_id) # "<" little endian
    header += struct.pack("<I", seq_num) 

    payload = build_payload()
    return bytes(header + payload)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    print("[Publisher] Sending packets for 2 machines...")

    seq = SEQUENCE_NUMBER
    try:
        while True:
            #  First machine (1001)
            packet1 = build_uadp_packet(1001, seq)
            sock.sendto(packet1, (MULTICAST_IP, PORT))

            #  Second machine (1002)
            #packet2 = build_uadp_packet(1002, seq)
            #sock.sendto(packet2, (MULTICAST_IP, PORT))

            #  Third machine (1003)
            #packet2 = build_uadp_packet(1003, seq)
            #sock.sendto(packet2, (MULTICAST_IP, PORT))

            #  Fourth machine (1004)
            #packet2 = build_uadp_packet(1004, seq)
            #sock.sendto(packet2, (MULTICAST_IP, PORT))

            print(f"[Publisher] Sent packets #{seq} for machines 1001")
            seq += 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()