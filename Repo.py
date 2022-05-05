import re
import subprocess
from pathlib import Path
import logging
from diff import git_checkout_version, compare_with_git, js_show_diff, compare_version


class Repo(object):

    def __init__(self, name, url, tag_version_regex, compare_dir):
        """
        :param url: git repo 地址
        :param tag_version_regex: 版本的格式的正则匹配
        :param compare_dir: 比较的目录
        """
        self._name = name
        self._url = url
        self._regex = re.compile(tag_version_regex)
        self._compare_dir = compare_dir

    def get_diffs(self):
        # check git directory is exist, if not exist, git clone
        self._mk_git_dir()
        #
        new_version = _get_new_version()
        old_version = _get_old_version()

        new_version_nums = self._regex.findall(new_version)[0]
        old_version_nums = self._regex.findall(old_version)[0]

        if compare_version(new_version_nums, old_version_nums) < 1:
            return

        self._get_diff(self._name, old_version, new_version, self._name, compare_component=self._compare_dir)

    def _get_diff(self, repo_name, old_release, new_release, repo_path, compare_component):
        git_checkout_version(old_release, new_release, repo_path=repo_path)

        compare_with_git(repo_name, old_release, new_release, compare_component, repo_path=repo_path)

        js_show_diff(repo_name, old_release, new_release)

        logging.info("{} compare with git finished!", repo_name)

    def _mk_git_dir(self):
        my_file = Path(self._name)
        if my_file.exists() and my_file.is_dir():
            return
        if my_file.is_file():
            my_file.unlink()

        my_file.mkdir()
        self.git_clone()

    def git_clone(self):
        cmd = ["git", "clone", self._url]
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out = p.stdout.readlines()
        logging.info("git clone result:{}", out)


