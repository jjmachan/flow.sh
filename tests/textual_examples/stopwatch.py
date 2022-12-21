from __future__ import annotations

from time import monotonic
from typing import List

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static


class TimeDisplay(Static):
    """Widget to display elaspsed time."""

    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update the time to the current time."""
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        "Called when the time attribute changes"
        mins, secs = divmod(time, 60)
        hours, mins = divmod(mins, 60)
        self.update(f"{hours:02.0f}:{mins:02.0f}:{secs:05.2f}")

    def start(self) -> None:
        "Method to start (or resume) time updating"
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        "Method to stop the time display updating."
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        "Method to reset the time display to zero."
        self.total = 0
        self.time = 0


class Stopwatch(Static):
    """Stopwatch Widget"""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == "start":
            self.add_class("started")
            time_display.start()
        elif button_id == "stop":
            self.remove_class("started")
            time_display.stop()
        elif button_id == "reset":
            time_display.reset()

    def compose(self) -> ComposeResult:
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.00")


class Timers(Static):
    """
    Collection of stopwatches
    """

    stopwatches: List[Stopwatch] = []
    currently_selected = reactive(0)

    def on_mount(self):
        current_stopwatch = self.add_new_stopwatch()
        current_stopwatch.add_class("selected")

    def add_new_stopwatch(self) -> Stopwatch:
        new_stopwatch = Stopwatch()
        self.mount(new_stopwatch)
        self.stopwatches.append(new_stopwatch)
        new_stopwatch.scroll_visible()

        return new_stopwatch

    def select_one_down(self):
        if len(self.stopwatches) != self.currently_selected + 1:
            self.stopwatches[self.currently_selected].remove_class("selected")
            self.currently_selected += 1
            self.stopwatches[self.currently_selected].add_class("selected")

    def select_one_up(self):
        if self.currently_selected != 0:
            self.stopwatches[self.currently_selected].remove_class("selected")
            self.currently_selected -= 1
            self.stopwatches[self.currently_selected].add_class("selected")


class StopwatchApp(App):

    CSS_PATH = "stopwatch.css"
    BINDINGS = [
        ("a", "add_stopwatch", "Add"),
        ("d", "delete_stopwatch", "Delete"),
        ("j", "move_down", "Down"),
        ("k", "move_up", "Up"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Timers(id="timers")

    def action_add_stopwatch(self) -> None:
        self.query_one("#timers").add_new_stopwatch()

    def action_remove_stopwatch(self) -> None:
        timers = self.query("Stopwatch")
        if timers:
            timers.last().remove()

    def action_move_down(self) -> None:
        self.query_one("#timers").select_one_down()

    def action_move_up(self) -> None:
        self.query_one("#timers").select_one_up()


if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
