#encoding:utf-8

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import process
from werkzeug.utils import secure_filename
from visualization import visualize3
from pypinyin import lazy_pinyin
import dash_bio
from dash import Dash
import dash_html_components as html
from werkzeug.middleware.dispatcher import DispatcherMiddleware

base_dir = os.path.abspath(os.path.dirname(__file__))
PEOPLE_FOLDER = os.path.join('static', 'people_photo')
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'uploads')
app = Flask(__name__)
app.secret_key="dasdas"

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite') # 配置数据库的地址
app.config ['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = False

db = SQLAlchemy(app)

class User(db.Model):
    # 定义表名
    __tablename__ = 'users'
    # 定义字段
    user_name = db.Column(db.String(64),)
    user_email=db.Column(db.String(30), primary_key=True)
    user_password = db.Column(db.String(30))

# 首页
@app.route('/')
def welcome():
    return render_template('welcome.html')

# 注册登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        useremail=request.form.get('email')
        password=request.form.get('password')

        login_email=request.form.get('login_email')
        login_password=request.form.get('login_password')
        if not username and not useremail and not password:
            for user in User.query.all():
                if login_email==user.user_email and login_password==user.user_password:
                    return redirect('/submit')
            else:
                return redirect('/fail')
        else:
            if not all([username, useremail, password]):
                return render_template('login.html', Users=User.query.all())
            elif len(username)<5 or len(username)>10 or len(password)<6 or len(password)>16:
                return render_template('login.html', Users=User.query.all())
            else:
                user = User(user_name=username, user_email=useremail, user_password=password)
                db.session.add(user)
                db.session.commit()
                print('保存成功')
                return render_template('login.html')

    return render_template('login.html')

# 输入序列 上传文件
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        seqId = request.form.get('seqid')
        seq = request.files.get('seq')
        # 用户输入序列号
        if seqId:
            process.write_gbk(seqId)
            print(seqId)
            strand, seq, position = process.main(seqId)
            # img_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'visualize.png')
            return render_template('result.html', strand=strand, seq=seq, position=position)
        # 用户输入文件
        elif seq:
            filename = secure_filename(''.join(lazy_pinyin(seq.filename)))
            print(filename)
            filepath = os.path.join(UPLOAD_PATH, filename)
            seq.save(filepath)
            print('文件上传成功')
            if filename.lower().endswith('.gbk') or filename.lower().endswith('.gb'):
                print('gbk文件可视化')
                visualize3(filepath)
                return render_template('result1.html') # 待修改
            elif filename.lower().endswith('.fasta') or filename.lower().endswith('.fa') or filename.lower().endswith('.txt'):
                print("单基因序列文件可视化")
                f = open(os.path.join(UPLOAD_PATH, 'fastas.txt'), 'w')
                filetext = open(filepath).read()
                # f.truncate()
                f.write(filetext)
                f.close()
                return redirect(url_for('visual_fa'))
    return render_template('submit.html')

filepath = os.path.join(UPLOAD_PATH, 'fastas.txt')
data = open(filepath, 'r').read()
style = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
dash_app = Dash(__name__, server=app, url_base_pathname='/visual_fa/', external_stylesheets=style)
dash_app.layout = html.Div([
dash_bio.AlignmentChart(id="my_alignemnt", data=data),
    html.Div(id='alignment-Viewer-output')])
application = DispatcherMiddleware(app, {'/dash': dash_app.server})
@app.route('/visual_fa')
def visual_fa():
    return redirect('/dash')

# 注册/登录失败
@app.route('/fail',methods=['GET','POST'])
def fail():
    # full_filename = os.path.join(app.config['UPLOAD_FOLDER'],'error.svg')
    return render_template('fail.html')

if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()

