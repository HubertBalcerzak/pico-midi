from MidiPacket import MidiPacket


class MidiDevice:

    def __init__(self, out):
        self._out = out

    def send(self, packet: MidiPacket):
        data = bytes(packet)
        self._out.write(data, len(data))
