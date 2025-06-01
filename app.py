from flask import Flask, render_template, request, redirect, session, url_for
import pymysql

app = Flask(__name__)
app.secret_key = '123456'

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Plx20041012@',
    'db': 'dinner_system',
    'charset': 'utf8mb4'
}

# 登录页面
@app.route('/')
def login():
    return render_template('login.html')

# 注册页面
@app.route('/register')
def register():
    return render_template('register.html')

# 登录逻辑
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM 用户 WHERE 用户名 = %s AND 密码 = %s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
            
            if result:
                # 登录成功
                session['user_id'] = result[0]
                session['username'] = result[1]
                return redirect(url_for('home'))
            else:
                # 登录失败
                return render_template('login.html', error='用户名或密码错误')
    finally:
        conn.close()

# 注册逻辑
@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    password = request.form['password']
    phone = request.form['phone']
    email = request.form['email']
    
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            # 检查用户名是否已存在
            sql_check = "SELECT * FROM 用户 WHERE 用户名 = %s"
            cursor.execute(sql_check, (username,))
            if cursor.fetchone():
                return render_template('register.html', error='用户名已存在')
            
            # 注册新用户
            sql_insert = "INSERT INTO 用户 (用户名, 密码, 手机号, 邮箱, 用户状态, 用户类型, 注册时间) VALUES (%s, %s, %s, %s, 'active', 'student', NOW())"
            cursor.execute(sql_insert, (username, password, phone, email))
            conn.commit()
            
            return redirect(url_for('login'))
    finally:
        conn.close()

# 主页
@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)