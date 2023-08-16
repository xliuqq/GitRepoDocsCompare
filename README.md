# 开源项目版本发布通知

原理：通过将相关仓库 git clone，查看相应的 tag 信息，发现新的版本，通过 git diff 记录文档差异，并通过 diff2html
工具转换成 html 界面。

TODO
- 如果单次执行（作为Github Action），每次都要 clone 仓库，效率太慢
- 针对 Hadoop 这种仓库，其文档分散在多个目录下，需要进一步支持
- 针对 once 运行，需要将产生的结果文件，推送到其它服务（如推送到其它github仓库，该仓库对外提供界面）

## 使用
假设用户为 lighthouse

### 源码下载
```shell
# 将源码仓库 clone 到 ~/repos/ 下面
cd ~
mkdir repos
cd repos
git clone https://gitee.com/luckyQQQ/git-repo-docs-compare
chmod +x git-repo-docs-compare/bin/*.sh
cd ~
```

### 安装依赖
```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 安装 miniconda，按照提示输入相关信息
sh Miniconda3-latest-Linux-x86_64.sh

# 创建 env，并安装相关依赖
conda create -n git_docs_compare
conda activate git_docs_compare

conda install python
conda install nodejs

pip install flask requests

npm install -g diff2html-cli
```

### 运行

配置 `conf.py` 中的`repo`等字段。

#### Serverless 运行
- 执行 `python3 run.py once` 仅运行一次，用于调试或者 Serverless 运行的场景

#### 服务运行
后台启动 webserver，默认绑定 17777 端口，提供界面访问。
```shell
./bin/start_webserver.sh
```

后台启动进程，定时（默认一天）检查仓库变化，将文档差别的html文件写到 'templates' 目录下
```shell
./bin/start_timer_compare.sh
```

crontab 设置监控，防止服务重启
```
# 非root用户，执行以下命令，将
# * * */1 * * /home/lighthouse/repos/git-repo-docs-compare/bin/monitor.sh > /home/lighthouse/repos/git-repo-docs-compare/logs/monitor.log
# 复制进去，注意开头的#不要复制，路径可以实际安装路径修改
crontab -e
```