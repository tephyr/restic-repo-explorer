from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Button, Footer
from textual.css.query import NoMatches
from textual.containers import Vertical
from .settings import SettingsModal
from textual.binding import Binding, BindingType

class ThreePaneApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="t", action="settings", description="Settings")
    ]

    def compose(self) -> ComposeResult:        
        with Vertical(classes="pane top-pane"):
            yield Static("Repository Configuration", id="title")
            # yield Input(placeholder="Repository", id="repository")
            # yield Input(placeholder="Password file", id="password_file")
            # yield Input(placeholder="Additional field", id="additional_field")
            # yield Button("OK", id="ok_button")
        yield Static("Pane 2", classes="pane")
        yield Static("Pane 3", classes="pane")
        yield Footer()

    def on_footer_button_pressed(self, event: BindingType) -> None:
        if event.button.id == "settings":
            self.push_screen(SettingsModal())
        yield Footer()

    def action_settings(self):
        self.push_screen(SettingsModal())

def run_app():
    app = ThreePaneApp()
    app.run()

if __name__ == "__main__":
    run_app()
