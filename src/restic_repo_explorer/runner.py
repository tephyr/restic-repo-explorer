from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Button
from textual.css.query import NoMatches
from textual.containers import Vertical

class ThreePaneApp(App):
    CSS_PATH = "styles.tcss"
    def compose(self) -> ComposeResult:
        with Vertical(classes="pane top-pane"):
            yield Static("Repository Configuration", id="title")
            yield Input(placeholder="Repository", id="repository")
            yield Input(placeholder="Password file", id="password_file")
            yield Input(placeholder="Additional field", id="additional_field")
            yield Button("OK", id="ok_button")
        yield Static("Pane 2", classes="pane")
        yield Static("Pane 3", classes="pane")

def run_app():
    app = ThreePaneApp()
    app.run()

if __name__ == "__main__":
    run_app()
