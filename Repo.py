from IRepo import IRepo
from diff import compare_with_git, js_show_diff, compare_version, get_tags


class Repo(IRepo):

    def __init__(self, initial_version, store_dir, git_url, compare_dir, tag_version_format):
        """
        :param git_url: git repo 地址
        :param tag_version_format: 版本的格式
        :param compare_dir: 比较的目录
        """
        super().__init__(initial_version, git_url, store_dir, tag_version_format)
        self._compare_dir = compare_dir

    def _get_newer_version(self, old_version):
        self._git_pull()

        tags = get_tags(self._get_repo_path())
        newer_version = old_version
        for tag in tags:
            match_tag = self._regex.findall(tag)
            if len(match_tag) == 0:
                continue
            version = match_tag[0]
            if compare_version(version, newer_version) > 0:
                newer_version = version
        return newer_version

    def _get_diff(self, old_version, new_version):
        repo_name = self._name
        repo_path = self._get_repo_path()
        new_docs_version = self._version_format.format(new_version)
        old_docs_version = self._version_format.format(old_version)
        diff_file = compare_with_git(repo_name, old_version=old_version, new_version=new_version,
                                     new_tag=new_docs_version, old_tag=old_docs_version,
                                     directory_or_file=self._compare_dir, repo_path=repo_path)
        if diff_file is not None:
            return js_show_diff(diff_file, repo_name, old_version, new_version)
