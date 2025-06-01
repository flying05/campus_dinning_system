import pymysql

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',  # MySQL服务器地址
    'user': 'root',       # MySQL用户名
    'password': 'Plx20041012@',  # MySQL密码
    'db': 'dinner_system',   # 数据库名称
    'charset': 'utf8mb4'  # 字符编码
}

# 创建表的SQL语句
create_tables_sql = [
    """
    CREATE TABLE IF NOT EXISTS 用户 (
        用户ID INT PRIMARY KEY AUTO_INCREMENT,
        用户名 VARCHAR(50) NOT NULL,
        密码 VARCHAR(255) NOT NULL,
        手机号 VARCHAR(20),
        邮箱 VARCHAR(100),
        用户状态 ENUM('active', 'inactive') NOT NULL,
        用户类型 ENUM('student', 'staff', 'admin') NOT NULL,
        注册时间 DATETIME NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS 区域 (
        区域ID INT PRIMARY KEY AUTO_INCREMENT,
        区域名称 VARCHAR(100) NOT NULL,
        描述 TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS 餐饮点 (
        餐饮点ID INT PRIMARY KEY AUTO_INCREMENT,
        名称 VARCHAR(100) NOT NULL,
        地址 VARCHAR(255),
        营业时间 TIME,
        电话 VARCHAR(20),
        营业状态 ENUM('open', 'closed') NOT NULL,
        区域ID INT,
        FOREIGN KEY (区域ID) REFERENCES 区域(区域ID)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS 菜品 (
        菜品ID INT PRIMARY KEY AUTO_INCREMENT,
        名称 VARCHAR(100) NOT NULL,
        描述 TEXT,
        图片 BLOB,
        是否特色 BOOLEAN NOT NULL,
        餐饮点ID INT,
        FOREIGN KEY (餐饮点ID) REFERENCES 餐饮点(餐饮点ID)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS 收藏 (
        用户ID INT,
        菜品ID INT,
        PRIMARY KEY (用户ID, 菜品ID),
        FOREIGN KEY (用户ID) REFERENCES 用户(用户ID),
        FOREIGN KEY (菜品ID) REFERENCES 菜品(菜品ID)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS 评分 (
        评分ID INT PRIMARY KEY AUTO_INCREMENT,
        用户ID INT,
        菜品ID INT,
        评分值 DECIMAL(3, 2),
        评分日期 DATETIME NOT NULL,
        内容 TEXT,
        消费金额 DECIMAL(10, 2),
        FOREIGN KEY (用户ID) REFERENCES 用户(用户ID),
        FOREIGN KEY (菜品ID) REFERENCES 菜品(菜品ID)
    )
    """
]

try:
    # 连接到MySQL数据库
    connection = pymysql.connect(**DB_CONFIG)

    # 创建游标对象
    cursor = connection.cursor()

    # 执行每个创建表的SQL语句
    for sql in create_tables_sql:
        cursor.execute(sql)
        print(f"执行SQL语句成功：{sql.split(' ')[2].strip()}")
        print("-" * 50)

    print("所有表创建成功！")

except pymysql.MySQLError as e:
    print(f"创建表时出错: {e}")

finally:
    # 关闭游标和连接
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()