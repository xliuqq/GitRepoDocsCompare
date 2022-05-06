# -*- coding: utf-8 -*-

"""
    脚本的目的是为了比较不同文件的差异，并且以可视化的形式展现
    1）支持递归对文件夹内的文件进行差异比较显示；
    2）当前支持的是对git repo的分支进行比较；

    github的compare只支持分支比较，不能通过URL具体得到不同分支的不同路径的diff结果。
    因此只能本地下载代码，通过 git diff --output <out> <branch1> <branch2> <dir> 将diff的结果保存成文件。
    然后，通过diff2html的js框架，进行结果展示，js获取文件


    https://diffy.org 通过上传diff文件，在线的可视化展示
"""
import os
from contextlib import contextmanager


def check_requirement():
    # check git
    # check diff2html-cli  (npm install -g diff2html-cli)
    return True


@contextmanager
def temp_change_work_dir(temp_work_dir):
    """
    change work directory temporally

    :param temp_work_dir:
    :return: current work directory
    """
    current_work_dir = os.getcwd()
    try:
        os.chdir(temp_work_dir)
        yield current_work_dir
    finally:
        os.chdir(current_work_dir)


# TODO: templates 可以自定义，并且不需要事先创建
def get_out_diff_path(name, old_release, new_release):
    old_release = old_release.replace("/", "_")
    new_release = new_release.replace("/", "_")
    return f"templates/{name}-{old_release}-{new_release}.out"


def get_out_diff_html_path(name, old_release, new_release):
    old_release = old_release.replace("/", "_")
    new_release = new_release.replace("/", "_")
    return f"templates/{name}-{old_release}-{new_release}.html"


# 比较的内容载在一个分支内
def compare_with_diff(name, old_version, new_version, new_docs_dir, old_docs_dir, repo_path):
    diff_file = get_out_diff_path(name, old_version, new_version)
    if not os.path.exists(diff_file):
        with temp_change_work_dir(repo_path) as current_work_dir:
            # 获取diff old new 的结果
            diff_cmd = f"diff -u {old_docs_dir} {new_docs_dir} > {current_work_dir}/{diff_file}"
            f = os.popen(diff_cmd)
            return_code = f.close()
            print(f"generate diff file from {repo_path}-{return_code}: {diff_cmd}")
            return diff_file
    else:
        print(f"read diff file from existing {diff_file}")
        return diff_file


# 基于git的版本控制，通过指定版本号，进行对比
def compare_with_git(name, old_version, new_version, new_tag, old_tag, directory_or_file, repo_path):
    diff_file = get_out_diff_path(name, old_version, new_version)
    if not os.path.exists(diff_file):
        with temp_change_work_dir(repo_path) as current_work_dir:
            # 获取git diff的结果
            print(f"generate diff file from {repo_path}")
            diff_cmd = f"git diff --output {current_work_dir}/{diff_file} {old_tag} {new_tag} {directory_or_file} "
            f = os.popen(diff_cmd)
            if f.close() == 1:
                print(f"Error when executing command {diff_cmd}")
                os.remove(diff_file)
            return diff_file
    else:
        print(f"read diff file from existing {diff_file}")
        return diff_file


def js_show_diff(diff_file, name, old_release, new_release, style="line"):
    diff_file_html = get_out_diff_html_path(name, old_release, new_release)
    if not os.path.exists(diff_file_html):
        # diff结果的可视化，采用diff2html的
        show_cmd = f"diff2html -F {diff_file_html} -f html -s {style} -i file -- {diff_file}"
        print(show_cmd)
        os.system(show_cmd)
        os.remove(diff_file)
    else:
        print(f"diff html file exists {diff_file_html}")

    return diff_file_html


def get_checkout_branch(branch_name, repo_path):
    with temp_change_work_dir(repo_path):
        cmd = f"git checkout {branch_name}"
        f = os.popen(cmd)
        content = set(f.read().splitlines())
        print(f"checkout {content}!")
        if f.close() == 1:
            print(f"Error when executing command '{cmd}'")


def get_tags(repo_path):
    with temp_change_work_dir(repo_path):
        cmd = "git tag -l"
        f = os.popen(cmd)
        content = set(f.read().splitlines())
        return content


def compare_version(new_version, old_version):
    """
    版本号比较
    :param new_version: a.b.c 格式
    :param old_version: a.b.c 格式
    :return: 1 表示 new > old, -1 表示 new < old
    """
    new_version_nums = new_version.split(".")
    old_version_nums = old_version.split(".")
    length = len(new_version_nums)
    for i in range(length):
        if int(new_version_nums[i]) > int(old_version_nums[i]):
            return 1
        elif int(new_version_nums[i]) < int(old_version_nums[i]):
            return -1

    return 0


if __name__ == '__main__':
    assert  compare_version("1.22.2", "1.22.3") == -1
    assert  compare_version("0.5.0", "0.10.3") == -1
    assert  compare_version("2.22.3", "1.22.3") == 1
    assert  compare_version("1.22.2", "1.22.2") == 0