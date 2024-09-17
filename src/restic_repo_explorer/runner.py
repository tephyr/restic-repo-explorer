from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.css.query import NoMatches

class ThreePaneApp(App):
    CSS_PATH = "styles.css"
    def compose(self) -> ComposeResult:
        yield Static("Pane 1", classes="pane")
        yield Static("Pane 2", classes="pane")
        yield Static("Pane 3", classes="pane")

def run_app():
    app = ThreePaneApp()
    app.run()

if __name__ == "__main__":
    run_app()
