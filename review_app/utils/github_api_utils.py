import base64
import json
from fnmatch import fnmatch

import requests

from settings import settings

headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}

analysis_ignore = [  # Ignoring files pattern
    "*.png",
    "*.jpeg",
    "*.git*",
    ".flake*"
]


def make_api_url(repo_url: str) -> str:
    repo_url = repo_url.split("github.com/")[1].replace(".git", "")
    return f"https://api.github.com/repos/{repo_url}/contents/"


def get_file_content(file_url: str) -> str:
    response = requests.get(file_url)

    try:
        content = response.content.decode("utf-8")
        content = json.loads(content)["content"]
        content = base64.b64decode(content)
    except UnicodeDecodeError:

        return "Can`t decode this file. Maybe this is binary file."

    return content


def all_files_from_repo(url: str) -> dict:
    response = requests.get(url, headers=headers)
    data = response.json()

    repo_content = {}

    if isinstance(data, list):
        for file in data:
            if any(
                    fnmatch(file["path"], pattern)
                    for pattern in analysis_ignore
            ):
                continue
            if file["type"] == "dir":
                all_files_from_repo(f"{url}/" + file["path"])
            else:
                file_content = get_file_content(file["url"])
                repo_content[file["path"]] = file_content
    else:
        file_content = get_file_content(data["url"])
        repo_content[data["url"]] = file_content

    return repo_content
