import array
import socket
import struct

<<<<<<< HEAD
class TCPPacket:
    """ Class desined for generating packages with specific data """

    def chksum(packet: bytes) -> int:
        """ Generation of starting checksum """
        if len(packet) % 2 != 0:
            packet += b'\0'

        res = sum(array.array("H", packet))
        res = (res >> 16) + (res & 0xffff)
        res += res >> 16

        return (~res) & 0xffff

=======

class TCPPacket:
    """ Class desined for generation packages with specific data """

    def chksum(packet: bytes) -> int:
        """ Generation of starting checksum """
        if len(packet) % 2 != 0:
            packet += b'\0'

        res = sum(array.array("H", packet))
        res = (res >> 16) + (res & 0xffff)
        res += res >> 16

        return (~res) & 0xffff

>>>>>>> 91416013f9ef4e59fff312d3e0921a6cab98dd12
    def __init__(self,
                 src_host:  str,
                 src_port:  int,
                 dst_host:  str,
                 dst_port:  int,
                 flags:     int = 0):
        """ Initiation of the tcp maker struct """
        self.src_host, self.src_port = src_host, src_port
        self.dst_host, self.dst_port = dst_host, dst_port
        self.flags = flags

    def build(self) -> bytes:
        """ Assembler of the packet information """
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

        checksum = TCPPacket().chksum(pseudo_hdr + packet)
        packet = packet[:16] + struct.pack('H', checksum) + packet[18:]
        print(packet)
        return packet
