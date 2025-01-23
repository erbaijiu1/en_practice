from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.words_practice import WordsPracticeEntity


class PracticeService:
    def __init__(self, db: Session):
        self.db = db

    def get_word_list(self, page: int, page_size: int, list_id: int = 1):
        """
        分页查询 WordsPracticeEntity 数据

        # :param list_id: 过滤的 list_id
        :param page: 当前页码（从1开始）
        :param page_size: 每页的记录数
        :return: 分页查询结果
        """
        # 计算偏移量
        offset = (page - 1) * page_size

        # 查询并分页
        query = self.db.query(WordsPracticeEntity) \
            .filter(WordsPracticeEntity.list_id == list_id) \
            .order_by(WordsPracticeEntity.id) \
            .offset(offset) \
            .limit(page_size)

        # 执行查询并返回结果
        return query.all()

    def get_total_words_count(self, list_id: int):
        """
        获取指定 list_id 的总记录数

        :param list_id: 过滤的 list_id
        :return: 总记录数
        """
        return self.db.query(WordsPracticeEntity) \
            .filter(WordsPracticeEntity.list_id == list_id) \
            .count()