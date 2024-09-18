from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Input, Button, Static
from textual.containers import Vertical
from .config import config

class SettingsModal(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Settings", id="modal-title"),
            Input(placeholder="Repository", id="repository", value=config.repository_path),
            Input(placeholder="Password file", id="password_file", value=config.password_file_path),
            Button("Save", id="save-button"),
            Button("Cancel", id="cancel-button"),
            id="modal-container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-button":
            config.repository_path = self.query_one("#repository").value
            config.password_file_path = self.query_one("#password_file").value
            self.app.query_one("#repository_text").update(config.repository_path)
            self.app.query_one("#password_file_text").update(config.password_file_path)
            self.app.pop_screen()
        elif event.button.id == "cancel-button":
            self.app.pop_screen()
