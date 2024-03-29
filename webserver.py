"""
提供 Web 服务
"""

import os
import sys

from flask import Flask, Response

from conf import settings

app = Flask(__name__)

# 设置工作环境为python脚本所在的文件
current_work_path = os.getcwd()
current_script_path = sys.path[0]
os.chdir(current_script_path)
print("Current work path is ", os.getcwd())

html_dirs = "templates"


@app.route('/')
def list_files():
    files = os.listdir(f"{html_dirs}/")
    files.remove(".git_keep")

    links = ["<a href='" + x + "' >" + x + "</a>"  for x in files]

    response = Response("<br><br>".join(links), mimetype="text/html")
    return response


@app.route('/<file_name>')
def get_diff(file_name):
    image = open(f"{html_dirs}/{file_name}", mode='rb')
    response = Response(image, mimetype="text/html")
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=settings["webserver_port"])
