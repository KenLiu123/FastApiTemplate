from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging
from sqlalchemy.ext.declarative import declarative_base

# 创建基础模型  
Base = declarative_base()



# 创建异步数据库连接
engine = create_async_engine(DATABASE_URL, 
        echo=True,
        pool_size=DATABASE_POOL_SIZE,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True
        )
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 依赖注入
async def get_db():
    async with AsyncSessionLocal() as session:
        try:    
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logging.error(f"数据库操作失败: {e}")
            raise e
        finally:
            await session.close()


# 事务管理函数：用于显式地管理事务
async def execute_transaction(session: AsyncSession, transaction_func):
    try:
        # 执行事务操作
        await transaction_func(session)
        await session.commit()
    except SQLAlchemyError as e:
        # 事务失败时回滚
        await session.rollback()
        logging.error(f"事务失败: {e}")
        raise

async def init_database():
    pass

async def close_database():
    pass

