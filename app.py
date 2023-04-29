from flask import Flask, session, render_template, request, redirect, flash
import pyrebase
import mysql.connector
import db
from sendemail import sendemail
from flaskext.mysql import MySQL

app = Flask(__name__)
config = {
    'apiKey': "AIzaSyAM48Oj4_x2H7p-aKiJwsVfWqeh7BhUHYA",
    'authDomain': "binarybeats-4559e.firebaseapp.com",
    'projectId': "binarybeats-4559e",
    'storageBucket': "binarybeats-4559e.appspot.com",
    'messagingSenderId': "29750487982",
    'appId': "1:29750487982:web:8ac3adc27833f72ba1363f",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'binarybits'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

app.secret_key = 'secret'

@app.route('/', methods=['POST', 'GET'])
def index():
    if ('user' in session):
        return render_template('index.html')
    else:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if ('user' in session):
        return redirect('/')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            auth.sign_in_with_email_and_password(email, password)
            
            str1="select * from faculty where email='"
            cursor.execute(str1+email+"'")
            result = cursor.fetchone()
            session['user'] = result
            flash("Logged in successfully", "success")
            return redirect('/')
        except:
            flash("Incorect Email or password", "danger")
            return redirect('/login')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if ('user' in session):
        return redirect('/')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        if (password == cpassword):
            try:
                user = auth.create_user_with_email_and_password(email, password)
                print(email)

                str1 = "insert into user values('"
                str2 = "','"
                str3 = "')"
                str = str1+email+str2+password+str3

                print(str)

                cursor.execute(str)
                conn.commit()

                flash("signup successfully","success")
                return redirect('/login')
            except:
                flash("User already exists", "warning")
                return redirect('/signup')
        else:
            flash("password and confirm paswsword not match", "warning")
            return redirect('/signup')
    else:
        return render_template('signup.html')


@app.route('/aleart')
def aleart():
    return render_template('aleart.html')


@app.route('/logout')
def logout():
    if ('user' in session):
        session.pop('user')
        flash("logout successfully", "success")
        return redirect('/login')
    else:
        return redirect('/login')


@app.route('/forgot', methods=['POST', 'GET'])
def forgot():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            user = auth.send_password_reset_email(email)
        except:
            flash("user not found", "danger")
            return redirect('/forgot')
        flash("reset email has send ", "success")
        return redirect('/')
    else:
        return render_template('forgot.html')

@app.route('/sendmail',methods=['POST','GET'])
def sendmail():
    if request.method == 'POST':
        try:
            formlink = request.form.get('link')
            msg = request.form.get('msg')
            department = request.form.get('department')
            semester = request.form.get('semester')
            batch = request.form.get('batch')
            name=session['user']
            cursor= conn.cursor()

            str1 = "select email from student where department = '"
            str3 = "' and semester = "
            str5 = " and batch = '"
            str10 = str1+department+str3+str(semester)+str5+batch+"'"
            cursor.execute(str10)
            items = cursor.fetchall()
            list=[]
            for item in items:
                #int(item[0])
                list.append(item[0])
            for i in list:
                sendemail(i,'New Form',formlink,msg,name[0])

        except:
            flash("something went wrong","danger")
            return redirect('/sendmail')
        flash("email sent successfully" ,"success")
        return redirect('/')
    else:
        return render_template('sendmail.html')

    
@app.route('/reminder',methods=['POST','GET'])
def sendreminder():
    if request.method == 'POST':
        try:
            googlesheet = request.form.get('googlesheet')
            subsheet = request.form.get('subsheet')
            link = request.form.get('link')
            msg = request.form.get('msg')
            department = request.form.get('department')
            semester = request.form.get('semester')
            batch = request.form.get('batch')

            print(batch)
            
        except:
            flash("user not found","danger")
            return redirect('/forgot')
        flash("reset email has send " ,"success")
        return redirect('/')
    else:
        return render_template('sendmail.html')


app.run(debug=True, port=5001)
