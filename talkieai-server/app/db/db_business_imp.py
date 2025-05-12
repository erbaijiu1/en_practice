from sqlalchemy.orm import Session

from app.api.session_routes import get_session
from app.db import get_db
from app.db.chat_entities import BusPromptConfig
from app.utils.logger_config import logger


def get_prompt_conf(business_name: str) -> BusPromptConfig|None:
    try:
        # 使用上下文管理器来获取数据库会话
        db: Session = next(get_db())
        result = db.query(BusPromptConfig).filter(BusPromptConfig.business_name == business_name).first()
        return result
    except Exception as e:
        logger.error(f"Error occurred while querying promote conf: {e}")
        raise

