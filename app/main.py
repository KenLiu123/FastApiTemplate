from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import user, auth  # 导入路由
from app.core.database import init_database, close_database


app = FastAPI(title="My Backend API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 注册路由
app.include_router(auth.app, prefix="/users", tags=["Auth"])
app.include_router(user.app, prefix="/users", tags=["User"])


@app.on_event("startup")
async def startup_event():
    await init_database()

@app.on_event("shutdown")
async def shutdown_event():
    await close_database()  


# 运行 FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
