from dataclasses import dataclass

@dataclass
class Config:
    repository_path: str = ""
    password_file_path: str = ""

# Create a global instance of the Config class
config = Config()
