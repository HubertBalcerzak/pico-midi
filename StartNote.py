from MidiPacket import MidiPacket


class StartNote(MidiPacket):

    def __init__(self, note, velocity=127):
        self._note = note
        self._velocity = velocity

    def __bytes__(self):
        return bytes([0x90, self._note, self._velocity])
