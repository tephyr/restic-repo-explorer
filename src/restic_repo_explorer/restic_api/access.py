"""
restic access.
"""

import restic

class RepoAccess():
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

    def forget_snapshot(self, snapshot_id):
        self.connect_repo()

        # result = restic.forget(snapshot_id=snapshot_id, prune=False, dry_run=True)
        # Build command "manually"", as resticpy does not currently support specifying a single snapshot to forget.
        # print(f'Base command: {restic._make_base_command()}')
        cmd = restic._make_base_command()
        cmd.extend(['forget', snapshot_id, '--dry-run'])
        print(f'Forget command: {cmd}')
        # Call restic.internal.forget's parser, as the output is currently JSON AND text combined.
        result = restic.internal.forget._parse_result(restic.internal.command_executor.execute(cmd))

        return result
