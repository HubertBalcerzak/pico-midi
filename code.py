import board
import digitalio
import time
import usb_midi
from analogio import AnalogIn
from MidiDevice import MidiDevice
from StartNote import StartNote
from StopNote import StopNote
from PitchBend import PitchBend
from Record import Record

ANALOG_MIN = 0
ANALOG_MAX = 65536
PITCH_BEND_SEND_INTERVAL = 0.05

last_pitch_bend = time.monotonic()
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
analog_in = AnalogIn(board.A2)

record_button = {
    "button": digitalio.DigitalInOut(board.GP14),
    "value": True,
    "debounceTime": 0,
}
record_button["button"].direction = digitalio.Direction.INPUT
record_button["button"].pull = digitalio.Pull.UP


class PressedEvent:
    def __init__(self, note):
        self.note = note
        self.last_played = time.monotonic()

    def playback(self):
        midi.send(StartNote(self.note, 127))
        self.last_played = time.monotonic()


class ReleasedEvent:
    def __init__(self, note):
        self.note = note
        self.last_played = time.monotonic()
        self.time_offset = None

    def playback(self):
        midi.send(StopNote(self.note, 127))
        self.last_played = time.monotonic()


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
    init_button(board.GP27, 60),
    init_button(board.GP26, 62),
    init_button(board.GP21, 64),
    init_button(board.GP22, 65),
    init_button(board.GP19, 67),
    init_button(board.GP20, 69),
    init_button(board.GP17, 71),
    init_button(board.GP18, 72),
]

record = Record()

midi = MidiDevice(usb_midi.ports[1])


def start_note(note):
    midi.send(StartNote(note, 127))


def stop_note(note):
    midi.send(StopNote(note, 127))


def send_pitch_bend():
    global last_pitch_bend
    if time.monotonic() - last_pitch_bend > PITCH_BEND_SEND_INTERVAL:
        pitch_value = int((analog_in.value - ANALOG_MIN) / ANALOG_MAX * 16383)
        midi.send(PitchBend(pitch_value))
        last_pitch_bend = time.monotonic()


def try_record(note, pressed):
    if not record_button["value"]:
        if pressed:
            record.record_event(PressedEvent(note))
        else:
            record.record_event(ReleasedEvent(note))


def handle_buttons():
    for button in buttons:
        if time.monotonic() - button["debounceTime"] > 0.1:
            if button["button"].value != button["value"]:
                button["value"] = button["button"].value
                button["debounceTime"] = time.monotonic()
                if button["value"]:
                    stop_note(button["note"])
                    try_record(button["note"], False)
                else:
                    start_note(button["note"])
                    try_record(button["note"], True)


def handle_record_button():
    if time.monotonic() - record_button["debounceTime"] > 0.1:
        if record_button["button"].value != record_button["value"]:
            record_button["value"] = record_button["button"].value
            record_button["debounceTime"] = time.monotonic()
            if not record_button["value"]:
                record.reset()
            else:
                record.start_playback()

    if record_button["value"]:
        led.value = 0
        record.try_playback_event()
    else:
        led.value = 1


while True:
    send_pitch_bend()
    handle_buttons()
    handle_record_button()
