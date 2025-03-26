
from pydantic import BaseModel
from typing import Any, Optional

class ResponseModel(BaseModel):
    status_code: int
    status: str  # 状态值，通常是 "success" 或 "error"
    message: Optional[str] = None  # 可选的消息字段，用于描述操作的结果
    data: Optional[Any] = None  # 返回的具体数据，可以是任何类型
    class Config:
        # 允许 Pydantic 处理从 ORM 模型转化为 Pydantic 模型
        orm_mode = True
