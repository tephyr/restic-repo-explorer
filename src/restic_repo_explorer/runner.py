from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Button, Footer, Label
from textual.css.query import NoMatches
from textual.containers import Horizontal, Vertical
from .settings import SettingsModal
from textual.binding import Binding, BindingType
from .config import config

class ThreePaneApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="t", action="settings", description="Settings")
    ]

    def compose(self) -> ComposeResult:        
        with Vertical(classes="pane top-pane"):
            yield Static("Repository Configuration", id="title")
            with Horizontal():
                yield Label("Repository:", id="repository_label")
                yield Label(config.repository_path, id="repository_text")
            with Horizontal():
                yield Label("Password file:", id="password_file_label")
                yield Label(config.password_file_path, id="password_file_text")
        yield Static("Pane 2", classes="pane")
        yield Static("Pane 3", classes="pane")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Footer).add_button("Settings", "settings", "Show Settings")

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
