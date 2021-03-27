from MidiPacket import MidiPacket


class StopNote(MidiPacket):

    def __init__(self, note, velocity=127):
        self._note = note
        self._velocity = velocity

    def __bytes__(self):
        return bytes([0x80, self._note, self._velocity])
