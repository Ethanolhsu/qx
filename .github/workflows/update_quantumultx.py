import os
import requests
from github import Github

# GitHub 仓库信息
REPO_NAME = "your_username/your_repo_name"  # 替换为你的用户名和仓库名
FILE_PATH = "QuantumultX.conf"
URL = "https://raw.githubusercontent.com/ddgksf2013/Profile/master/QuantumultX.conf"

# 获取远程文件内容
remote_content = requests.get(URL).text

# 初始化 GitHub 客户端
g = Github(os.environ["GITHUB_TOKEN"])
repo = g.get_repo(REPO_NAME)

# 获取 GitHub 文件内容
try:
    contents = repo.get_contents(FILE_PATH)
    github_content = contents.decoded_content.decode("utf-8")
except Exception:
    github_content = None

# 如果文件内容不同，则更新
if github_content != remote_content:
    print("File content is different. Updating...")

    # 替换 "Color" 为 "mini"
    updated_content = remote_content.replace("Color", "mini")

    # 插入新代码
    lines = updated_content.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "wifi2: all_direct":
            lines.insert(i + 1, "ssid_suspended_list=Live_5G")
            break
    final_content = "\n".join(lines)

    # 更新 GitHub 文件
    if github_content:
        repo.update_file(FILE_PATH, "Auto-update QuantumultX.conf", final_content, contents.sha)
    else:
        repo.create_file(FILE_PATH, "Add QuantumultX.conf", final_content)
else:
    print("File content is up-to-date.")
