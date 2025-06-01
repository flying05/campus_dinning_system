import pymysql

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',  # MySQL 服务器地址
    'user': 'root',       # MySQL 用户名
    'password': 'Plx20041012@',  # MySQL 密码
    'charset': 'utf8mb4'  # 字符编码
}

# 连接到 MySQL 服务器
try:
    connection = pymysql.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        charset=DB_CONFIG['charset']
    )

    # 创建游标对象
    cursor = connection.cursor()

    # 创建数据库
    database_name = 'dinner_system'  # 替换为你想创建的数据库名
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

    print(f"数据库 '{database_name}' 创建成功！")

except pymysql.MySQLError as e:
    print(f"创建数据库时出错: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()