import board
import digitalio
import time
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
from analogio import AnalogIn

ANALOG_MIN = 0
ANALOG_MAX = 65536

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
analog_in = AnalogIn(board.A1)


def init_button(pin, note):
    newButton = digitalio.DigitalInOut(pin)
    newButton.direction = digitalio.Direction.INPUT
    newButton.pull = digitalio.Pull.UP

    return {
        "button": newButton,
        "value": True,
        "debounceTime": 0,
        "note": note
    }


buttons = [
    init_button(board.GP26, 60),
    init_button(board.GP22, 62),
    init_button(board.GP20, 64),
    init_button(board.GP21, 65),
    init_button(board.GP18, 67),
    init_button(board.GP19, 69),
    init_button(board.GP16, 71),
    init_button(board.GP17, 72),
]

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)


def sendNote(note):
    led.value = 1
    midi.send(NoteOn(note, 120))
    a_pitch_bend = PitchBend(int((analog_in.value - ANALOG_MIN) / ANALOG_MAX * 16383))
    midi.send(a_pitch_bend)
    time.sleep(0.1)
    midi.send(NoteOff(note, 120))
    led.value = 0

t = 0

while True:
    for button in buttons:
        if time.monotonic() - button["debounceTime"] > 0.1:
            if button["button"].value != button["value"]:
                button["value"] = button["button"].value
                button["debounceTime"] = time.monotonic()
                if button["value"]:
                    sendNote(button["note"])
