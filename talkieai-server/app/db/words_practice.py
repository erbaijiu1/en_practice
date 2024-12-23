import datetime

from sqlalchemy import Column, String, DateTime, Integer, Index, Text
from app.db import Base, engine


# 聊天话题组表
class WordsPracticeEntity(Base):
    __tablename__ = "t_words_practice"

    # columns id, list_id, main_words, details, create_time, update_time
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    list_id = Column("list_id", Integer, nullable=False)
    main_words = Column("main_words", String(1024), nullable=False)
    details = Column("details", Text, nullable=False)
    create_time = Column("create_time", DateTime, default=datetime.datetime.now)
    update_time = Column("update_time", DateTime, default=datetime.datetime.now)


# 数据库未创建表的话自动创建表
Base.metadata.create_all(engine)
