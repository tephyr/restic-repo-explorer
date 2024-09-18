from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Static
from textual.containers import Vertical

class SettingsModal(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Settings", id="modal-title"),
            Input(placeholder="Repository", id="repository"),
            Input(placeholder="Password file", id="password_file"),
            Input(placeholder="Other", id="other"),
            Button("Save", id="save-button"),
            Button("Cancel", id="cancel-button"),
            id="modal-container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-button":
            # Handle save logic here
            self.app.pop_screen()
        elif event.button.id == "cancel-button":
            self.app.pop_screen()
