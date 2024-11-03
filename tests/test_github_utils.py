from unittest import mock

from review_app.utils.github_api_utils import (
    all_files_from_repo,
    make_api_url,
    get_file_content,
    headers
)


def test_make_api_url():
    url = "https://github.com/test_owner/test_repo.git"
    expected_result = "https://api.github.com/repos/test_owner/test_repo/contents/"
    result_url = make_api_url(url)

    assert result_url == expected_result


@mock.patch("requests.get")
def test_get_file_content(mocked_request):
    mocked_request.return_value.content = b'{"name":"requirements.txt","content":"Zmxha2U4PT01LjAuNApmbGFrZTgtYW5ub3RhdGlvbnM9PTIuOS4xCmZsYWtl\\nOC1xdW90ZXM9PTMuMy4xCmZsYWtlOC12YXJpYWJsZXMtbmFtZXM9PTAuMC41\\nCnBlcDgtbmFtaW5nPT0wLjEzLjIKcHl0ZXN0PT03LjEuMwo=\\n"}'
    url = "https://api.github.com/repos/pashawarganov/py-car-wash-station/contents/README.md?ref=master"
    expected_result = b'flake8==5.0.4\nflake8-annotations==2.9.1\nflake8-quotes==3.3.1\nflake8-variables-names==0.0.5\npep8-naming==0.13.2\npytest==7.1.3\n'

    content = get_file_content(url)
    mocked_request.assert_called_once_with(url)
    assert content == expected_result


@mock.patch("review_app.utils.github_api_utils.get_file_content")
@mock.patch("requests.get")
def test_all_files_from_repo(mocked_request, mocked_get_content):
    mocked_response = mock.Mock()
    mocked_response.json.return_value = [
        {'name': 'README.md', 'path': 'README.md',
         'url': 'https://api.github.com/repos/test_owner/test_repo/contents/README.md?ref=master', 'type': 'file', },
        {'name': 'checklist.md', 'path': 'checklist.md',
         'url': 'https://api.github.com/repos/test_owner/test_repo/contents/checklist.md?ref=master', 'type': 'file'},
        {'name': 'requirements.txt', 'path': 'requirements.txt',
         'url': 'https://api.github.com/repos/test_owner/test_repo/contents/requirements.txt?ref=master',
         'type': 'file'},
    ]
    mocked_request.return_value = mocked_response
    mocked_get_content.return_value = "test_content"
    url = "https://api.github.com/repos/test_owner/test_repo/contents/"
    expected_content = {
        'README.md': 'test_content',
        'checklist.md': 'test_content',
        'requirements.txt': 'test_content'
    }

    repo_content = all_files_from_repo(url)
    mocked_request.assert_called_once_with(url, headers=headers)
    expected_calls = [mock.call(file["url"]) for file in mocked_response.json.return_value]
    mocked_get_content.assert_has_calls(expected_calls, any_order=True)

    assert repo_content == expected_content
