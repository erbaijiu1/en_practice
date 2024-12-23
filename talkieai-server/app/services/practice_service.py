import json

from sqlalchemy.orm import Session
from app.core.utils import *
from app.db.words_practice import WordsPracticeEntity
from app.models.topic_models import *
from app.db.topic_entities import *
from app.db.chat_entities import *
from app.db.account_entities import *
from app.ai.models import *
from app.core.logging import logging
from app.ai import chat_ai
from app.core.azure_voice import *
from app.models.chat_models import *


class PracticeService:
    def __init__(self, db: Session):
        self.db = db

    def get_word_list(self, size: int, page_number: int):
        """获取单词列表，支持分页"""
        offset = (page_number - 1) * size
        return self.db.query(WordsPracticeEntity).limit(size).offset(offset).all()

    def get_word_list(self, page_id: int, size: int, page_number: int):
        """获取单词列表，支持分页"""
        offset = (page_number - 1) * size
        return self.db.query(WordsPracticeEntity).filter_by(page_id=page_id).limit(size).offset(offset).all()
