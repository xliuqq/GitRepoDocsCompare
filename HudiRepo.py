import re
import subprocess
from pathlib import Path

from IRepo import IRepo
from diff import js_show_diff, get_checkout_branch, compare_with_diff, temp_change_work_dir, compare_version


class HudiRepo(IRepo):

    def __init__(self, initial_version, store_dir, git_url, docs_branch, docs_dir, version_format):
        """
        :param initial_version: 初始版本
        :param git_url: git repo 地址
        :param tag_version_regex: 版本的格式的正则匹配
        :param compare_dir: 比较的目录
        :param version_format: 版本的格式，如 version-1.2.3形式，则用 version-{} 替代
        """
        super().__init__(initial_version, git_url, store_dir, version_format)
        self._docs_branch = docs_branch
        self._docs_dir = docs_dir

    def _get_newer_version(self, old_version):
        # check the branch is exist or not
        get_checkout_branch(self._docs_branch, repo_path=self._get_repo_path())

        self._git_pull()

        import os
        files = os.listdir(f"{self._get_repo_path()}/{self._docs_dir}")
        newer_version = old_version
        for file in files:
            version = self._regex.findall(file)[0]
            if version is not None and compare_version(version, newer_version) > 0:
                newer_version = version
        return newer_version

    def _get_diff(self, old_version, new_version):
        # compare the different doc dirs
        repo_name = self._name
        repo_path = self._get_repo_path()
        new_docs_version = self._version_format.format(new_version)
        old_docs_version = self._version_format.format(old_version)
        diff_file = compare_with_diff(repo_name, old_version=old_version, new_version=new_version,
                                      new_docs_dir=f"{self._docs_dir}/{new_docs_version}",
                                      old_docs_dir=f"{self._docs_dir}/{old_docs_version}", repo_path=repo_path)
        if diff_file is not None:
            return js_show_diff(diff_file, repo_name, old_version, new_version)
