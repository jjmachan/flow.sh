from __future__ import annotations

import typing as t
from time import monotonic

from textual.app import App
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static

if t.TYPE_CHECKING:
    from textual.app import ComposeResult

EMOJI_MAP = {
    "unmute": "🔊",
    "mute": "🔇",
    "play": "▶️",
    "pause": "⏸️",
}


class Timer(Static):
    """
    Displays elapsed time
    """

    is_paused = True
    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)
    emoji = EMOJI_MAP["pause" if is_paused else "play"]

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(1, self.update_time, pause=True)

    def update_time(self) -> None:
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{self.emoji}  {hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}")

    def start(self) -> None:
        self.emoji = EMOJI_MAP["pause"]
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        self.emoji = EMOJI_MAP["play"]
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        self.total = 0.0
        self.time = 0.0

    def toggle_pause(self) -> None:
        if self.is_paused:
            self.start()
        else:
            self.stop()

        self.is_paused = not self.is_paused


class Music(Static):
    muted: bool = False

    def toggle_mute(self) -> None:
        self.muted = not self.muted
        self.update(
            f"{EMOJI_MAP['mute'] if self.muted else EMOJI_MAP['unmute']}  LofiGirl"
        )


class TimerBar(Static):
    def compose(self) -> ComposeResult:
        yield Horizontal(Music("🔊  LofiGirl"), Timer("▶️  00:00:00"))


class FlowshApp(App):
    CSS_PATH = "./css/flowsh.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("m", "mute", "Mute/Unmute the music"),
        ("space", "pause", "Pause/Play the timer"),
    ]

    def action_mute(self) -> None:
        music = self.query_one("Music")
        if music:
            music.toggle_mute()

    def action_pause(self) -> None:
        timer = self.query_one("Timer")
        if timer:
            timer.toggle_pause()

    def compose(self) -> ComposeResult:
        yield Container(TimerBar(), Footer())


def main():
    app = FlowshApp()
    app.run()
