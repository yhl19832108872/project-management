from flask import Flask, render_template, request, flash,redirect
from flask_sqlalchemy import SQLAlchemy
import os
base_dir = os.path.abspath(os.path.dirname(__file__))
PEOPLE_FOLDER = os.path.join('static','people_photo')
app = Flask(__name__)
app.secret_key="dasdas"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config ['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = False

db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'users'
    user_name = db.Column(db.String(64),)
    user_email=db.Column(db.String(30), primary_key=True)
    user_password = db.Column(db.String(30))



@app.route('/',methods=['GET','POST'])
def index():

    if request.method=='POST':
        username=request.form.get('username')
        useremail=request.form.get('email')
        password=request.form.get('password')

        login_email=request.form.get('login_email')
        login_password=request.form.get('login_password')
        print(type(username))
        print(type(useremail))
        if not username and not useremail and not password :

            for user in User.query.all():
                if login_email==user.user_email and login_password==user.user_password:

                    return redirect('/analise')
            else:
                return redirect('/fail')
        else:
            if not all([username, useremail, password]):
                # flash('参数不完整')
                print('参数不完整')
                return render_template('index.html', Users=User.query.all())
            elif len(username)<5 or len(username)>10 or len(password)<6 or len(password)>16:
                return render_template('index.html', Users=User.query.all())
            else:
                user = User(user_name=username, user_email=useremail, user_password=password)
                db.session.add(user)
                db.session.commit()
                return render_template('index.html')

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'bg.jpg')
    return render_template('index.html',Users=User.query.all(),user_image=full_filename)

@app.route('/analise',methods=['GET','POST'])
def analise():
    if request.method=='POST':
        number=request.form.get('number')
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'img.png')
    return render_template('analise.html',user_image=full_filename)

@app.route('/fail',methods=['GET','POST'])
def fail():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'],'error.svg')
    return render_template('fail2.html',user_image = full_filename)
if __name__ == '__main__':
    app.run()
    db.create_all()
    #
    # for user in User.query.all():
    #     print(user.user_name,user.user_email,user.user_password)

