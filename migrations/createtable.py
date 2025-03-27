import mysql.connector
from mysql.connector import errorcode

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',   # 你的数据库地址
    'user': 'root',        # 你的数据库用户名
    'password': 'Aa123456',  # 你的数据库密码
    'database': 'rbac_system'  # 你的数据库名
}

# 需要创建的表
TABLES = {
    'Users': """
    CREATE TABLE Users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        telephone VARCHAR(11) NOT NULL,
        avatar VARCHAR(255),
        is_active BOOLEAN DEFAULT TRUE, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    'Roles': """
    CREATE TABLE Roles (
        role_id INT AUTO_INCREMENT PRIMARY KEY,
        role_name VARCHAR(50) NOT NULL UNIQUE,
        description TEXT DEFAULT NULL
    );
    """,
    'Permissions': """
    CREATE TABLE Permissions (
        permission_id INT AUTO_INCREMENT PRIMARY KEY,
        permission_name VARCHAR(50) NOT NULL UNIQUE,
        description TEXT DEFAULT NULL
    );
    """,
    'Role_Permissions': """
    CREATE TABLE Role_Permissions (
        role_id INT NOT NULL,
        permission_id INT NOT NULL,
        granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (role_id, permission_id),
        FOREIGN KEY (role_id) REFERENCES Roles(role_id) ON DELETE CASCADE,
        FOREIGN KEY (permission_id) REFERENCES Permissions(permission_id) ON DELETE CASCADE
    );
    """,
    'User_Roles': """
    CREATE TABLE User_Roles (
        user_id INT NOT NULL,
        role_id INT NOT NULL,
        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, role_id),
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES Roles(role_id) ON DELETE CASCADE
    );
    """
}

try:
    # 连接数据库
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("✅ 数据库连接成功！")

    # 查询已存在的表
    cursor.execute("SHOW TABLES;")
    existing_tables = {table[0] for table in cursor.fetchall()}

    # 创建表
    for table_name, table_sql in TABLES.items():
        if table_name in existing_tables:
            print(f"⚠️ 表 {table_name} 已存在，跳过创建。")
        else:
            cursor.execute(table_sql)
            print(f"✅ 表 {table_name} 创建成功！")

    # 预置角色（避免重复插入）
    roles = [
        ("Admin", "系统管理员，可以管理所有数据"),
        ("Manager", "领导， 负责团队管理、审批流程，可能拥有一定的管理权限，但低于管理员。"),
        ("User", "只能访问自身权限范围内的功能，如查看和编辑个人信息。")
    ]
    cursor.executemany("INSERT IGNORE INTO Roles (role_name, description) VALUES (%s, %s);", roles)

    # 预置权限（避免重复插入）
    permissions = [
        ("read", "允许读取数据"),
        ("write", "允许修改数据"),
        ("delete", "允许删除数据"),
        ("manage_users", "管理用户权限")
    ]
    cursor.executemany("INSERT IGNORE INTO Permissions (permission_name, description) VALUES (%s, %s);", permissions)

    # 提交数据
    conn.commit()
    print("✅ 预设角色和权限数据插入成功！")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("❌ 用户名或密码错误！")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("❌ 数据库不存在！请手动创建数据库")
    else:
        print(f"❌ 发生错误: {err}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    print("🔌 数据库连接已关闭。")
