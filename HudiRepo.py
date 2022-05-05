import re
import subprocess
from pathlib import Path

from diff import js_show_diff, get_checkout_branch, compare_with_diff, temp_change_work_dir, compare_version


class HudiRepo(object):

    def __init__(self, initial_version, store_dirs, git_url, docs_branch, docs_dir, version_format):
        """
        :param initial_version: 初始版本
        :param git_url: git repo 地址
        :param tag_version_regex: 版本的格式的正则匹配
        :param compare_dir: 比较的目录
        :param version_format: 版本的格式，如 version-1.2.3形式，则用 version-{} 替代
        """
        self._initial_version = initial_version
        self._name = git_url.split("/")[-1].split(".git")[0]
        self._store_dirs = store_dirs
        self._url = git_url
        self._docs_branch = docs_branch
        self._docs_dir = docs_dir
        self._metadata_filename = self._name + ".meta"
        self._version_format = version_format
        self._regex = re.compile(self._version_format.replace("{}", "(.*)"))

    def _get_old_version(self):
        import pickle
        file = Path(self._metadata_filename)
        if file.exists():
            with file.open("rb") as f:
                version = pickle.load(f)
                return version
        return self._initial_version

    def _get_newer_version(self, old_version):
        with temp_change_work_dir(self._get_repo_path()) as old_dir:
            cmd = ["git", "pull"]
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            out = p.stdout.readlines()
            print(f"git pull:{out}")

        import os
        files = os.listdir(f"{self._get_repo_path()}/{self._docs_dir}")
        newer_version = []
        for file in files:
            version = self._regex.findall(file)[0]
            if version is not None and compare_version(version, old_version) > 0 :
                newer_version.append(version)
        return newer_version

    def _write_metadata(self, version):
        import pickle
        with open(self._metadata_filename, "wb") as file:
            pickle.dump(version, file)

    def get_diffs(self):
        # check git directory is exist, if not exist, git clone
        self._mk_git_dir()
        #
        old_version = self._get_old_version()
        new_version = self._get_newer_version(old_version)

        if len(new_version) == 0:
            print(f"The newest version is current {old_version}")
            return

        if len(new_version) > 1:
            print(f"Exist multiple newer version: {new_version} than {old_version}")
            return
        new_version = new_version[0]

        print(f"get diff between {new_version} and {old_version}")
        self._get_diff(self._name, self._docs_branch, self._get_repo_path(),
                       new_docs_version=self._version_format.format(new_version),
                       old_docs_version=self._version_format.format(old_version))

        self._write_metadata(new_version)

    def _get_repo_path(self):
        return self._store_dirs + "/" + self._name

    def _get_diff(self, repo_name, branch_name, repo_path, new_docs_version, old_docs_version):
        # check the branch is exist or not
        get_checkout_branch(branch_name, repo_path=repo_path)

        # compare the different doc dirs
        compare_with_diff(repo_name, new_version=new_docs_version, old_version=old_docs_version,
                          docs_dir=self._docs_dir, repo_path=repo_path)

        js_show_diff(repo_name, old_docs_version, new_docs_version)

    def _mk_git_dir(self):
        Path(self._store_dirs).mkdir(exist_ok=True)

        store_path = Path(self._get_repo_path())
        if store_path.exists() and store_path.is_dir():
            return
        if store_path.is_file():
            store_path.unlink()

        with temp_change_work_dir(self._store_dirs):
            self._git_clone()

    def _git_clone(self):
        cmd = ["git", "clone", self._url]
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out = p.stdout.readlines()
        print(f"git clone result:{out}")



if __name__ == '__main__':
    repo = HudiRepo(initial_version="0.11.0", store_dirs="projects", git_url="https://gitee.com/apache/Hudi.git",
                    docs_branch="asf-site", docs_dir="website/versioned_docs", version_format="version-{}")
    repo.get_diffs()
