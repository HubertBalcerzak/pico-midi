import time


class Record:

    def __init__(self):
        self.start_time = time.monotonic()
        self.events = []
        self.record_length = 0

    def record_event(self, event):
        if len(self.events) == 0:
            self.start_time = time.monotonic()
        self.events.append(event)

    def try_playback_event(self):
        if len(self.events) == 0:
            return
        next_event = self.events[0]
        if next_event.last_played + self.record_length < time.monotonic():
            next_event.playback()
            self.events.append(next_event)
            self.events.pop(0)

    def start_playback(self):
        self.record_length = time.monotonic() - self.start_time

    def reset(self):
        self.events = []
        self.start_time = time.monotonic()
