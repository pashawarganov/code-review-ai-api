from review_app.crud import content_from_dict_to_str


def test_content_from_dict_to_str():
    content_dict = {
        'README.md': 'test_content',
        'checklist.md': 'test_content',
        'requirements.txt': 'test_content'
    }
    expected_content = "file: README.md\ncode: test_content\nfile: checklist.md\ncode: test_content\nfile: requirements.txt\ncode: test_content"

    assert content_from_dict_to_str(content_dict) == expected_content
