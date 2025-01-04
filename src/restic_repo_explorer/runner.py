from textual import work
from textual.app import App, ComposeResult
from textual.theme import Theme
from textual.widgets import Static, Input, Button, Footer, Label, ListView, ListItem, Tree
from textual.css.query import NoMatches
from textual.containers import Horizontal, Vertical
from textual.binding import Binding, BindingType
import humanize

from .settings import SettingsModal
from .forget import ForgetModal
from .config import config
from .restic_api.access import RepoAccess

class ThreePaneApp(App):
    repo_access = None
    available_snapshots = []  # Store snapshots data
    current_snapshot = None
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="t", action="settings", description="Settings"),
        Binding(key="l", action="load", description="Load snapshots"),
        Binding(key="f", action="forget", description="Forget snapshot"),
    ]

    def on_mount(self):
        # Register the theme: only used *for app-specific themes*.
        # self.app.register_theme(arctic_theme)

        # Set the app's theme
        self.theme = "flexoki" # "arctic"

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
        with Horizontal(classes="pane bottom-pane"):
            yield Static("Details", id="details_pane", classes="left")
            yield Tree("Summary", id="summary_tree", classes="right")
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
    async def action_forget(self) -> None:
        """Handle the forget action."""
        print(f'self.app.available_snapshots (action_forget): {len(self.available_snapshots)}; current_snapshot: {self.current_snapshot}')
        if self.current_snapshot is None:
            self.notify("Please select a snapshot.")
        else:
            result = await self.push_screen_wait(ForgetModal())
            if result == "forget":
                self._forget_snapshot()
            elif result == "prune":
                self.notify("Prune operation would happen here")

    @work
    async def action_load(self):
        self.repo_access = RepoAccess(config.repository_path, config.password_file_path)
        self.available_snapshots = self.repo_access.get_snapshots()  # Store for later use
        snapshots_pane = self.query_one("#snapshots_pane", ListView)
        snapshots_pane.clear()
        for snapshot in self.available_snapshots:
            snapshots_pane.append(ListItem(Label(self._get_snapshot_header(snapshot))))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle selection of a snapshot."""
        if not self.available_snapshots:
            return
            
        # Remove current-snapshot class from all items
        for item in event.list_view.query("ListItem"):
            item.remove_class("current-snapshot")
            
        selected_index = event.list_view.index
        if 0 <= selected_index < len(self.available_snapshots):
            # Add class to newly selected item
            event.item.add_class("current-snapshot")
            
            self.current_snapshot = self.available_snapshots[selected_index]
            details = f"Details for {self.current_snapshot.get('short_id')}:\n\n{self._get_snapshot_details(self.current_snapshot)}"

            details_pane = self.query_one("#details_pane", Static)
            details_pane.update(details)

            # Get data for individual snapshot.
            single_snapshot = self.repo_access.get_snapshot(self.current_snapshot['id'])

            # Show JSON summary for this snapshot.
            summary_tree = self.query_one("#summary_tree", Tree)
            summary_tree.clear()
            summary_tree.add_json(single_snapshot[0]) # Always returned as a single-item list.
            summary_tree.root.label = f"Summary for {self.current_snapshot['short_id']}"
            summary_tree.root.expand_all()

    def _get_snapshot_header(self, snapshot) -> str:
        """
        Return a formatted string of header-specific values for this snapshot.
        """

        # return f'[{snapshot["short_id"]}] {snapshot["time"]} {snapshot["hostname"]}'
        return f'{snapshot["short_id"]}: {snapshot["time"]} {snapshot["hostname"]}'

    def _get_snapshot_details(self, snapshot) -> str:
        """
        Build a human-readable string of the available information.  Only display what is available from the summary.
        """
        details = [
            f"ID: {snapshot['id']}",
            f"Time: {snapshot['time']}",
            f"Tags: {snapshot.get('tags', [])}",
            f"Paths:",
            ""
        ]
        for path in snapshot.get('paths', []):
            details.extend([f"- {path}"])

        finegrained_details = self._get_finegrained_details(snapshot)
        if len(finegrained_details) > 0:
            details.extend(['', 'Changes', ''])
            details.extend([f"- {x}" for x in finegrained_details])
        else:
            details.extend(['', 'No changes detected'])

        return '\n'.join(details)

    def _get_finegrained_details(self, snapshot) -> list:
        """
        Get newer (>=v0.17) details.
        """

        details = []
        if "summary" in snapshot:
            summary = snapshot["summary"]
            files_new = summary.get('files_new', 0)
            files_changed = summary.get('files_changed', 0)

            keys_and_titles = (
                ['files_new', 'New files'],
                ['files_changed', 'Changed files'],
                ['dirs_new', 'New directories'],
                ['dirs_changed', 'Changed directories']
            )

            for line in keys_and_titles:
                if summary.get(line[0]):
                    details.append(f"{line[1]}: {summary[line[0]]}")

            if summary.get('data_added'):
                details.append(f"Data added (raw): {humanize.naturalsize(summary['data_added'], gnu=True)}")
                details.append(f"Data added (packed): {humanize.naturalsize(summary['data_added_packed'], gnu=True)}")

        return details


    def _forget_snapshot(self):
        if self.repo_access is None:
            self.notify("No repo loaded.")
        elif self.current_snapshot is None:
            self.notify("No snapshot selected.")
        else:
            result = self.repo_access.forget_snapshot(self.current_snapshot['id'])
            self.log('self.repo_access.forget_snapshot', self.current_snapshot['short_id'], result)
            notice = f"Snapshot {self.current_snapshot['short_id']} forgotten."
            if config.dry_run:
                notice += " Dry-run activated; no changes made."
            else:
                notice += " Please reload the list to continue."
            self.notify(notice)
            self.current_snapshot = None


def run_app():
    app = ThreePaneApp()
    app.run()

if __name__ == "__main__":
    run_app()
