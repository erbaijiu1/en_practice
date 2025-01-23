from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core import get_current_account
from app.db import get_db
from app.models.response import ApiResponse
from app.services.account_service import AccountService
from app.services.practice_service import PracticeService

router = APIRouter()


@router.get("/practice/list", name="get practice list")
def get_word_list(
    page: int = 1,
    page_size: int = 10,
    list_id: int = 1,
    db: Session = Depends(get_db),
):
    """
    分页获取单词列表
    :param list_id: 过滤的 list_id
    :param page: 当前页码（从1开始）
    :param page_size: 每页的记录数
    :param db: 数据库会话
    :return: 分页查询结果
    """
    practice_service = PracticeService(db)
    data = practice_service.get_word_list(page, page_size, list_id)
    # total = practice_service.get_total_words_count()

    return ApiResponse(
        data={
            "items": data,
            # "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


