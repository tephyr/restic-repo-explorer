from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Button, Footer, Label, ListView, ListItem
from textual.css.query import NoMatches
from textual.containers import Horizontal, Vertical
from .settings import SettingsModal
from textual.binding import Binding, BindingType
from .config import config
from .restic_api.access import Snapshots

class ThreePaneApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="t", action="settings", description="Settings"),
        Binding(key="l", action="load", description="Load snapshots"),
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
        yield ListView(classes="pane", id="snapshots_pane")
        yield Static("Pane 3", classes="pane")
        yield Footer()

    @work
    async def action_settings(self):
        if await self.push_screen_wait(SettingsModal()):
            self.notify("Settings OK")
            repo_text = self.query_one("#repository_text")
            repo_text.update(config.repository_path)
            self.query_one("#password_file_text").update(config.password_file_path)
        else:
            self.notify("Settings cancelled", severity="warn")

    @work
    async def action_load(self):
        snapshots = Snapshots(config.repository_path, config.password_file_path)
        available_snapshots = snapshots.get_snapshots()
        snapshots_pane = self.query_one("#snapshots_pane", ListView)
        snapshots_pane.clear()
        for snapshot in available_snapshots:
            snapshots_pane.append(ListItem(Label(str(snapshot))))

def run_app():
    app = ThreePaneApp()
    app.run()

if __name__ == "__main__":
    run_app()
