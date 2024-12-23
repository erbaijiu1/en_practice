from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core import get_current_account
from app.db import get_db
from app.models.response import ApiResponse
from app.services.account_service import AccountService
from app.services.practice_service import PracticeService

router = APIRouter()


@router.get("/practice/list", name="get practice list")
def get_account_info(
        db: Session = Depends(get_db), account_id: str = Depends(get_current_account)
):

    # 拉取单词列表
    words_service = PracticeService(db)
    return ApiResponse(data=words_service.get_word_list(size=10, page_number=1))


