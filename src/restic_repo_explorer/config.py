import os
from dataclasses import dataclass

@dataclass
class Config:
    repository_path: str = ""
    password_file_path: str = ""
    dry_run: bool = True

    def load_from_env(self):
        self.repository_path = os.environ.get("RESTIC_REPOSITORY", "")
        self.password_file_path = os.environ.get("RESTIC_PASSWORD_FILE", "")

# Create a global instance of the Config class and load from environment
config = Config()
config.load_from_env()
