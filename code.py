import board
import digitalio
import time
import usb_midi
from analogio import AnalogIn
from MidiDevice import MidiDevice
from StartNote import StartNote
from StopNote import StopNote
from PitchBend import PitchBend

ANALOG_MIN = 0
ANALOG_MAX = 65536
PITCH_BEND_SEND_INTERVAL = 0.05

last_pitch_bend = time.monotonic()
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

midi = MidiDevice(usb_midi.ports[1])


def start_note(note):
    led.value = 1
    midi.send(StartNote(note, 120))


def stop_note(note):
    led.value = 0
    midi.send(StopNote(note, 120))


def send_pitch_bend():
    global last_pitch_bend
    if time.monotonic() - last_pitch_bend > PITCH_BEND_SEND_INTERVAL:
        pitch_value = int((analog_in.value - ANALOG_MIN) / ANALOG_MAX * 16383)
        midi.send(PitchBend(pitch_value))
        last_pitch_bend = time.monotonic()


t = 0

while True:
    send_pitch_bend()
    for button in buttons:
        if time.monotonic() - button["debounceTime"] > 0.1:
            if button["button"].value != button["value"]:
                button["value"] = button["button"].value
                button["debounceTime"] = time.monotonic()
                if button["value"]:
                    stop_note(button["note"])
                else:
                    start_note(button["note"])
