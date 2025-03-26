```
my_fastapi_project/
├── app/                 # 主应用目录
│   ├── api/             # 路由（API 层）
│   ├── core/            # 配置 & 中间件
│   ├── models/          # 数据模型（数据库映射）
│   ├── services/        # 业务逻辑
│   ├── db/              # 数据库连接（CRUD操作）
│   ├── schemas/         # 前端数据结构
│   ├── middleware/      # 中间件（JWT、CORS）
│   ├── utils/           # 工具函数
│   ├── tests/           # 单元测试
├── config/              # 配置文件（YAML / .env）
├── logs/                # 日志文件
├── migrations/          # 数据库迁移
├── scripts/             # 启动/运维脚本
├── .gitignore           # Git 忽略文件
├── README.md            # 项目说明
├── requirements.txt     # 依赖库
└── Dockerfile           # Docker 配置（可选）
```