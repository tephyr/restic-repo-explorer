"""
restic access.
"""

import restic

class Snapshots():
    def __init__(self, repo, pw_file):
        self.__repo = repo
        self.__pw_file = pw_file
        self.__restic_connected = False

    def connect_repo(self):
        if not self.__restic_connected:
            restic.repository = self.__repo
            restic.password_file = self.__pw_file
            self.__restic_connected = True

    def get_snapshots(self):
        self.connect_repo()
        return restic.snapshots()

    def get_snapshot(self, snapshot_id):
        self.connect_repo()
        return restic.snapshots(snapshot_id)
