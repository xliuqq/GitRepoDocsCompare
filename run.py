import datetime
import json
import os
import sys
from threading import Timer

import requests

from conf import settings
from diff import get_out_diff_html_name


def notify_dingding(address, name, old_version, new_version):
    html_file = get_out_diff_html_name(name, old_version, new_version).lstrip()
    # DingTalk
    code_result = f'#### [{name}-新版本-{new_version}-通知]({address}/{html_file}) \n\n 新版本:{new_version}, ' \
                  f'旧版本:{old_version}'
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
    r = requests.post(settings["dingtalk_webhook"], data=json.dumps(pagrem), headers=headers)
    print(r.text)  # 请求返回内容
    print(r.status_code)  # 请求返回状态


class Run(object):
    def __init__(self, address: str):
        self._address = address

    def get_repo_diffs(self):
        repos = settings["repos"]
        for name in repos:
            print(f"{datetime.datetime.now()}: get repo [{name}]")
            repo = repos.get(name)
            (new_version, old_version, out_html_file) = repo.get_diffs()
            if out_html_file is None:
                continue
            notify_dingding(self._address, name, old_version, new_version)

    def start(self):
        pass


class TimerRun(Run):
    """
        定时运行，配合Web服务，对外提供界面展示版本文档差异界面内，并配置钉钉通知。
    """

    def __init__(self, address: str, interval: int = 3600 * 24):
        super().__init__(address)
        self._interval = interval

    def start(self):
        self.timer()

    def timer(self):
        self.get_repo_diffs()
        t = Timer(self._interval, self.timer)
        t.start()


class OnceRun(Run):
    def __init__(self, address: str):
        super().__init__(address)

    def start(self):
        self.get_repo_diffs()


if __name__ == '__main__':
    # 设置工作环境为python脚本所在的文件
    current_work_path = os.getcwd()
    current_script_path = sys.path[0]
    os.chdir(current_script_path)
    print("Current work path is ", os.getcwd())

    list_of_arguments = sys.argv

    notify_address = f"http://{settings['webserver_ip']}:{settings['webserver_port']}"

    if len(list_of_arguments) == 1 or list_of_arguments[1] == "timer":
        TimerRun(f"{notify_address}").start()
    elif list_of_arguments[1] == "once":
        OnceRun(f"{notify_address}").start()
