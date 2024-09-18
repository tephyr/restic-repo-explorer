from textual import on
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

    @on(Button.Pressed, "#save-button")
    def handle_save(self):
        config.repository_path = self.query_one("#repository").value
        config.password_file_path = self.query_one("#password_file").value
        self.dismiss(True)

    @on(Button.Pressed, "#cancel-button")
    def handle_cancel(self):
        self.dismiss(False)
