import sys

from HudiRepo import HudiRepo
from diff import *

# 设置工作环境为python脚本所在的文件
current_work_path = os.getcwd()
current_script_path = sys.path[0]
os.chdir(current_script_path)
print("Current work path is ", os.getcwd())

# get_diff("Spark", "v2.4.5", "v3.1.2", "D:\\repos\\spark", "docs")
#
# get_diff("Hadoop-yarn-site", "rel/release-3.2.1", "rel/release-3.3.1", "D:\\repos\\hadoop",
#          "hadoop-yarn-project/hadoop-yarn/hadoop-yarn-site/src/site/markdown")
#
# get_diff("Hadoop-hdfs-site", "rel/release-3.2.1", "rel/release-3.3.1", "D:\\repos\\hadoop",
#          "hadoop-hdfs-project/hadoop-hdfs/src/site/markdown")
#
# get_diff("MLflow", "v1.10.0", "v1.19.0", "D:\\repos\\mlflow", "docs/source")


# TODO: 定时更新

repo = HudiRepo(initial_version="0.11.0", store_dirs="projects", git_url="https://gitee.com/apache/Hudi.git",
                docs_branch="asf-site", docs_dir="website/versioned_docs", version_format="version-{}")
repo.get_diffs()
