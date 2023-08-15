from HudiRepo import HudiRepo
from Repo import Repo

repos = {
    # TODO 如何处理向 Hadoop 这种多个 docs 目录

    "Hudi": HudiRepo(initial_version="0.13.0", store_dir="projects", git_url="https://gitee.com/apache/Hudi.git",
                     docs_branch="asf-site", docs_dir="website/versioned_docs", version_format="version-{}"),
    "spark": Repo(initial_version="3.4.0", store_dir="projects", git_url="https://gitee.com/apache/spark.git",
                  compare_dir="docs", tag_version_format="v{}"),
    "kubebuilder": Repo(initial_version="3.4.1", store_dir="projects",
                        git_url="https://gitee.com/import-github/kubebuilder.git",
                        compare_dir="docs/book/src", tag_version_format="v{}"),
    "sealer": Repo(initial_version="0.8.4", store_dir="projects",
                   git_url="https://github.com/sealerio/sealer.git",
                   compare_dir="docs", tag_version_format="v{}"),
    "presto": Repo(initial_version="0.273", store_dir="projects",
                   git_url="https://github.com/prestodb/presto.git",
                   compare_dir="presto-docs/src/main/sphinx", tag_version_format="{}"),
    "flink": Repo(initial_version="1.14.4", store_dir="projects",
                  git_url="https://github.com/apache/flink.git",
                  compare_dir="docs", tag_version_format="release-{}")
}


dingtalk_webhook = "https://oapi.dingtalk.com/robot/send?access_token=" \
                   "27a336572a201f25b1aed157726dec58b372aafcf3d9820ee31434293940962f"