restic-repo-explorer
====================
A TUI (Text User Interface) for exploring and administering a restic backup repository.

Development
+++++++++++
With `Textual:Devtools <https://textual.textualize.io/guide/devtools/>`__ & ``uv``::

    # Make 2 consoles.
    # 1. Show logging.
    uv run textual console 
    # 2. Run the application in dev mode, via a module import.
    uv run textual run --dev restic_repo_explorer:run
