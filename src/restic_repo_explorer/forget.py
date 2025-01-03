from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Static

class ForgetModal(ModalScreen):
    """Modal for forget/prune operations."""

    def compose(self) -> ComposeResult:
        with Vertical(id="modal-container"):
            yield Static("Are you sure you want to forget this snapshot?\nThis operation cannot be undone.", id="modal-title")
            with Horizontal():
                yield Button("Forget", variant="error", id="forget-button")
                yield Button("Prune", variant="warning", id="prune-button") 
                yield Button("Cancel", variant="primary", id="cancel-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-button":
            self.dismiss(False)
        elif event.button.id == "forget-button":
            self.dismiss("forget")
        elif event.button.id == "prune-button":
            self.dismiss("prune")

