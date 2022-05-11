import subprocess
from pathlib import Path
import re

from diff import temp_change_work_dir


class IRepo(object):
    def __init__(self, initial_version, git_url, store_dir, tag_version_format):

        self._initial_version = initial_version
        self._name = git_url.split("/")[-1].split(".git")[0]
        self._url = git_url
        self._store_dir = store_dir
        self._metadata_filename = f"meta/{self._name}.meta"
        self._version_format = tag_version_format
        self._regex = re.compile(r"^" + self._version_format.replace("{}", r"([.\d]*)") + r"$")

    def _get_old_version(self):
        import pickle
        file = Path(self._metadata_filename)
        if file.exists():
            with file.open("rb") as f:
                version = pickle.load(f)
                return version
        return self._initial_version

    def _mk_git_dir(self):
        Path(self._store_dir).mkdir(exist_ok=True)

        store_path = Path(self._get_repo_path())
        if store_path.exists() and store_path.is_dir():
            return
        if store_path.is_file():
            store_path.unlink()

        with temp_change_work_dir(self._store_dir):
            self._git_clone()

    def _git_pull(self):
        with temp_change_work_dir(self._get_repo_path()) as old_dir:
            cmd = "git pull"
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            out = p.stdout.readlines()
            print(f"git pull:{out}")

    def _get_repo_path(self):
        return self._store_dir + "/" + self._name

    def _git_clone(self):
        cmd = f"git clone {self._url}"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out = p.stdout.readlines()
        print(f"git clone [{cmd}] result:{out}")

    def _write_metadata(self, version):
        import pickle
        with open(self._metadata_filename, "wb") as file:
            pickle.dump(version, file)

    def get_diffs(self):
        # check git directory is exist, if not exist, git clone
        self._mk_git_dir()

        old_version = self._get_old_version()
        new_version = self._get_newer_version(old_version)

        if new_version == old_version:
            print(f"The newest version is current {old_version}")
            return new_version, old_version, None

        print(f"get diff between {new_version} and {old_version}")

        out_html_file = self._get_diff(old_version, new_version)

        if out_html_file is not None:
            self._write_metadata(new_version)

        return new_version, old_version, out_html_file

    def _get_newer_version(self, old_version):
        pass

    def _get_diff(self, old_version, new_version):
        pass
