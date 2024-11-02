from review_app.utils.github_api_utils import (
    all_files_from_repo,
    make_api_url
)
from review_app.utils.groq_api_utils import client


async def get_content_dict(repo_url: str) -> dict:
    base_url = make_api_url(repo_url)
    return all_files_from_repo(base_url)


def content_from_dict_to_str(content_dict: dict) -> str:
    return "\n".join(
        f"file: {file}\ncode: {code}"
        for file, code in content_dict.items()
    )


async def get_review(
        content_dict: dict,
        assigment_description: str,
        candidate_level: str
) -> dict:
    content = content_from_dict_to_str(content_dict)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content":
                    f"""
                    Make review for this code.
                    Candidate_level: {candidate_level}
                    {content}
                    Assigment description: {assigment_description}
                    Divide your answer into 2 parts:
                    rating each file separately and
                    rating the candidate as a whole.
                    First part must looks like:
                    [file_name] - review
                    (only review, don`t put rating and
                    description in first part)
                    Second part must looks like:
                    Rating: rating/5
                    description candidate skills
                """,
            }
        ],
        model="llama3-8b-8192",
    )

    return {"message": response.choices[0].message.content}
