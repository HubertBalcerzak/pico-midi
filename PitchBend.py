from MidiPacket import MidiPacket


class PitchBend(MidiPacket):

    def __init__(self, pitch):
        self._pitch = pitch

    def __bytes__(self):
        return bytes([0xe0, self._pitch & 0x7f, (self._pitch >> 7) & 0x7f])
