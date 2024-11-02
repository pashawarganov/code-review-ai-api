from fastapi import APIRouter

from review_app import crud
from review_app import schemas

router = APIRouter()


@router.post("/review/")
async def get_review(request: schemas.ReviewBase):
    content = await crud.get_content_dict(request.github_repo_url)
    answer = await crud.get_review(
        content,
        request.assigment_description,
        request.candidate_level
    )

    return answer
