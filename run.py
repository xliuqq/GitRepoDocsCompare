import datetime
import json
import os
import sys
from threading import Timer

import requests
from flask import Flask, Response

from HudiRepo import HudiRepo
from Repo import Repo
from diff import get_out_diff_html_path

app = Flask(__name__)

repos = {
    "Hudi": HudiRepo(initial_version="0.10.1", store_dir="projects", git_url="https://gitee.com/apache/Hudi.git",
                     docs_branch="asf-site", docs_dir="website/versioned_docs", version_format="version-{}"),
    "spark": Repo(initial_version="3.2.0", store_dir="projects", git_url="https://gitee.com/apache/spark.git",
                  compare_dir="docs", tag_version_format="v{}"),
    "kubebuilder": Repo(initial_version="3.4.1", store_dir="projects",
                        git_url="https://gitee.com/import-github/kubebuilder.git",
                        compare_dir="docs/book/src", tag_version_format="v{}"),
    "sealer": Repo(initial_version="0.8.4", store_dir="projects",
                   git_url="https://github.com/sealerio/sealer.git",
                   compare_dir="docs", tag_version_format="v{}"),
    "presto": Repo(initial_version="0.273", store_dir="projects",
                   git_url="https://github.com/prestodb/presto.git",
                   compare_dir="presto-docs/src/main/sphinx", tag_version_format="{}")
}


def get_repo_diffs(address):
    dingtalk_webhook = "https://oapi.dingtalk.com/robot/send?access_token=6a9c771f84445fdbbeed1d98bb0fba9ce60641e2eddf046d529a7456aad74f38"
    for name in repos:
        print(f"{datetime.datetime.now()}: get repo [{name}]")
        repo = repos.get(name)
        (new_version, old_version, out_html_file) = repo.get_diffs()
        if out_html_file is None:
            continue
        # DingTalk
        code_result = f'#### [{name}-新版本-{new_version}-通知](http://{address}/diff/{name}/{new_version}/{old_version}) \n\n 新版本:{new_version}, 旧版本:{old_version}'
        pagrem = {
            "msgtype": "markdown",
            "markdown": {
                'title': f"Track: {name}-新版本-{new_version}-通知",
                "text": code_result
            },
            "at": {
                "isAtAll": True
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(dingtalk_webhook, data=json.dumps(pagrem), headers=headers)
        print(r.text)  # 请求返回内容
        print(r.status_code)  # 请求返回状态

    t = Timer(3600 * 24, get_repo_diffs, (address,))
    t.start()


# 设置工作环境为python脚本所在的文件
current_work_path = os.getcwd()
current_script_path = sys.path[0]
os.chdir(current_script_path)
print("Current work path is ", os.getcwd())


@app.route('/diff/<name>/<newversion>/<oldversion>')
def get_diff(name, newversion, oldversion):
    file = get_out_diff_html_path(name, oldversion, newversion)
    image = open(file, mode='rb')
    response = Response(image, mimetype="text/html")
    return response


if __name__ == '__main__':
    address = "172.16.1.217:17777"
    host = address.split(":")[0]
    port = int(address.split(":")[1])
    t = Timer(1, get_repo_diffs, (address,))
    t.start()

    app.run(host=host, port=port)
