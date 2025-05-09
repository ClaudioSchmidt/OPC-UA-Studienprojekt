import struct
from typing import Tuple, Dict, Any

class Decoder:

    def decode_packet(self, data: bytes) -> Tuple[int, Dict[str, Any]]:
        version_flags = data[0]
        version = (version_flags >> 4) & 0x0F
        flags = version_flags & 0x0F

        offset = 1
        publisher_id = None
        sequence_number = None

        if flags & 0x01:
            publisher_id = struct.unpack('<H', data[offset:offset + 2])[0]
            offset += 2

        if flags & 0x02:
            sequence_number = struct.unpack('<I', data[offset:offset + 4])[0]
            offset += 4

        payload = data[offset:]
        decoded_data = self._decode_payload(payload)

        return publisher_id, decoded_data
    
    def _decode_payload(self, payload: bytes) -> Dict[str, Any]:
        data = {}
        offset = 0

        for name, type_code in self.FIELD_SCHEMA:
            size = struct.calcsize(type_code)
            value = struct.unpack_from(f"<{type_code}", payload, offset)[0]
            data[name] = value
            offset += size

        return data


    # Field schema for decoding
    # "?" = [bool]   Boolean, 1 byte
    # "B" = [uint8]  unsigned byte, 1 byte
    # "h" = [int16]  short integer, 2 bytes
    # "I" = [uint32] unsigned int, 4 bytes
    # "d" = [double] double, 8 bytes
    FIELD_SCHEMA = [
        ("sorting_state", "B"),
        ("remote_control_is_enabled", "?"),
        ("status_code", "h"),
        ("sorting_criterion", "B"),
        ("workpiece_counter_slide_a", "I"),
        ("workpiece_counter_slide_b", "I"),
        ("app_btn", "?"),
        ("app_led", "B"),
        ("process_btn", "?"),
        ("process_led", "B"),
        ("fault_ack_btn", "?"),
        ("fault_ack_led", "B"),
        ("emergency_btn", "?"),
        ("belt_speed", "d"),
        ("belt_speed_level", "B"),
        ("is_running", "?"),
        ("is_reverse", "?"),
        ("switch", "?"),
        ("start_sensor", "?"),
        ("id_sensor", "?"),
        ("color_channel", "B"),
        ("inductive_sensor", "?"),
        ("switch_sensor", "?"),
        ("storage_sensor", "?")
    ]