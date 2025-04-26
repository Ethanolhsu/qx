import os
import requests
from github import Github

# 配置部分
REPO_NAME = "your_username/your_repo_name"  # 替换为你的 GitHub 用户名和仓库名
FILE_PATH = "QuantumultX.conf"             # GitHub 中的目标文件路径
URL = "https://raw.githubusercontent.com/ddgksf2013/Profile/master/QuantumultX.conf"  # 远程文件 URL

# 获取远程文件内容
def fetch_remote_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching remote content: {e}")
        return None

# 获取 GitHub 文件内容
def fetch_github_content(repo, file_path):
    try:
        contents = repo.get_contents(file_path)
        return contents.decoded_content.decode("utf-8"), contents.sha
    except Exception as e:
        print(f"File not found in GitHub repository: {e}")
        return None, None

# 更新或创建 GitHub 文件
def update_github_file(repo, file_path, new_content, sha=None):
    commit_message = "Auto-update QuantumultX.conf"
    if sha:
        print("Updating existing file...")
        repo.update_file(file_path, commit_message, new_content, sha)
    else:
        print("Creating new file...")
        repo.create_file(file_path, commit_message, new_content)

# 修改文件内容
def modify_content(content):
    # 替换 "Color" 为 "mini"
    modified_content = content.replace("Color", "mini")

    # 替换 "Orz-3/mini/master/" 为 "Koolson/Qure/master/IconSet/"
    modified_content = modified_content.replace("Orz-3/mini/master/", "Koolson/Qure/master/IconSet/")

    # 在 "wifi2: all_direct" 下一行插入 "ssid_suspended_list=Live_5G"
    lines = modified_content.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "wifi2: all_direct":
            lines.insert(i + 1, "ssid_suspended_list=Live_5G")
            break
    return "\n".join(lines)

# 主逻辑
def main():
    # 初始化 GitHub 客户端
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        return

    g = Github(github_token)
    repo = g.get_repo(REPO_NAME)

    # 获取远程文件内容
    remote_content = fetch_remote_content(URL)
    if not remote_content:
        print("Failed to fetch remote content. Exiting.")
        return

    # 获取 GitHub 文件内容
    github_content, sha = fetch_github_content(repo, FILE_PATH)

    # 如果文件内容不同，则更新
    if github_content != remote_content:
        print("File content is different. Updating...")

        # 修改文件内容
        final_content = modify_content(remote_content)

        # 更新 GitHub 文件
        update_github_file(repo, FILE_PATH, final_content, sha)
    else:
        print("File content is up-to-date.")

if __name__ == "__main__":
    main()
