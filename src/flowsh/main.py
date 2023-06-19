from __future__ import annotations

import typing as t

from textual.app import App
from textual.containers import Container, Horizontal
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
    ...


class Music(Static):
    ...


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

    def compose(self) -> ComposeResult:
        yield Container(TimerBar(), Footer())


def main():
    app = FlowshApp()
    app.run()
