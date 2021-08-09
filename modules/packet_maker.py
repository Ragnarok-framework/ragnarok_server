import array
import socket
import struct
import argparse
def chksum(packet: bytes) -> int:
    """ Generation of starting checksum """
    if len(packet) % 2 != 0:
        packet += b'\0'

    res = sum(array.array("H", packet))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16

    return (~res) & 0xffff


class TCPPacket:
    """ Class desined for generation packages with specific data """
    def __init__(self,
                 src_host:  str,
                 src_port:  int,
                 dst_host:  str,
                 dst_port:  int,
                 flags:     int = 0):
        self.src_host, self.src_port = src_host, src_port
        self.dst_host, self.dst_port = dst_host, dst_port
        self.flags = flags

    def build(self) -> bytes:
        packet = struct.pack(
            '!HHIIBBHHH',
            self.src_port,  # Source Port
            self.dst_port,  # Destination Port
            0,              # Sequence Number
            0,              # Acknoledgement Number
            5 << 4,         # Data Offset
            self.flags,     # Flags
            8192,           # Window
            0,              # Checksum (initial value)
            0               # Urgent pointer
        )

        pseudo_hdr = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.src_host),    # Source Address
            socket.inet_aton(self.dst_host),    # Destination Address
            socket.IPPROTO_TCP,                 # PTCL
            len(packet)                         # TCP Length
        )

        checksum = chksum(pseudo_hdr + packet)
        packet = packet[:16] + struct.pack('H', checksum) + packet[18:]
        print(packet)
        return packet


#if __name__ == '__main__':
#    parser = argparse.ArgumentParser(description = "TCP")
#    parser.add_argument("dst")
#    args = parser.parse_args()
#    dst = args.dst
#    pak = TCPPacket(
#        '192.168.1.42',
#        20,
#        dst,
#        666,
#        0b000101001
#    )
#
#    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
#
#    s.sendto(pak.build(), (dst, 0))
