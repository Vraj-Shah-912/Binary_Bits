from flask import Flask, session, render_template, request, redirect, flash
import pyrebase
import mysql.connector
import db
from sendemail import sendemail
from flaskext.mysql import MySQL
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_email_list(mysheet):

    row = mysheet.col_values(2)
    email_list = row[1:]
    return email_list


def compare_emails(l1, l2):
    set1 = set(l1)
    set2 = set(l2)
    not_common_emails = list(set1.symmetric_difference(set2))
    return not_common_emails


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
            user = auth.sign_in_with_email_and_password(email, password)

            str1 = "select * from faculty where email='"
            cursor.execute(str1+email+"'")
            result = cursor.fetchone()
            session['user'] = result
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
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        if (password == cpassword):
            try:
                user = auth.create_user_with_email_and_password(
                    email, password)

                str1 = "insert into faculty values('"
                str2 = "','"
                str3 = "')"
                str = str1+name+str2+email+str2+password+str3

                cursor.execute(str)
                conn.commit()

                flash("signup successfully", "success")
                return redirect('/login')
            except:
                flash("User already exists", "warning")
                return redirect('/signup')
        else:
            flash("password and confirm paswsword not match", "warning")
            return redirect('/signup')
    else:
        return render_template('signup.html')


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


@app.route('/sendmail', methods=['POST', 'GET'])
def sendmail():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            formlink = request.form.get('link')
            msg = request.form.get('msg')
            department = request.form.get('department')
            semester = request.form.get('semester')
            batch = request.form.get('batch')
            name = session['user']
            cursor = conn.cursor()

            str1 = "select email from student where department = '"
            str3 = "' and semester = "
            str5 = " and batch = '"
            str10 = str1+department+str3+str(semester)+str5+batch+"'"
            cursor.execute(str10)
            items = cursor.fetchall()
            list = []
            for item in items:
                # int(item[0])
                list.append(item[0])
            for i in list:
                sendemail(i, 'New Form', formlink, msg, name[0])

            sql = "insert into sentmail values('"+department+"'," + \
                semester+",'"+batch+"','"+formlink+"','"+title+"')"
            cursor.execute(sql)
            conn.commit()
        except:
            flash("something went wrong", "danger")
            return redirect('/sendmail')
        flash("email sent successfully", "success")
        return redirect('/')
    else:
        return render_template('sendmail.html')


@app.route('/reminder', methods=['POST', 'GET'])
def sendreminder():
    print("in reminder")
    if request.method == 'POST':
        # if request.form.get("reminder"):
        print("in if")
        try:
            print("in try")
            name = session['user']
            googlesheet = request.form.get('googlesheet')
            subsheet = request.form.get('subsheet')
            msg = request.form.get('msg')
            title = request.form.get('title')
            print(title+msg)
            myscope = ['https://spreadsheets.google.com/feeds',
                        'https://www.googleapis.com/auth/drive']

            mycreds = ServiceAccountCredentials.from_json_keyfile_name(
                'secret-medium-385219-771c7ef500e1.json', myscope)

            myclient = gspread.authorize(mycreds)

            sh1 = googlesheet
            sh2 = subsheet

            mysheet = myclient.open(sh1).worksheet(sh2)
            # l1 = ["e1@example.com", "e2@example.com", "e3@example.com"]
            l2 = get_email_list(mysheet)

            cursor = conn.cursor()

            s1 = "select * from sentmail where title='"
            cursor.execute(s1+title+"'")
            result = cursor.fetchone()
            str1 = "select email from student where department = '"
            str3 = "' and semester = "
            str5 = " and batch = '"
            str10 = str1+result[0]+str3+str(result[1])+str5+result[2]+"'"
            print(result)
            cursor.execute(str10)
            items = cursor.fetchall()
            l1 = []
            for item in items:
                # int(item[0])
                l1.append(item[0])
            l3 = compare_emails(l1, l2)
            for i in l3:
                sendemail(i, 'Reminder', result[3], msg, name[0])

            print(l3)
            flash("reminder mail has send ", "success")
            return render_template('sendreminder.html',l3=l3)    
        
        except:
            flash("Somthing went wrong !!", "danger")
            return redirect('/reminder')
    

        # if request.form.get("followup"):
        #     try:
        #         googlesheet = request.form.get('googlesheet')
        #         subsheet = request.form.get('subsheet')
        #         msg = request.form.get('msg')
        #         title = request.form.get('title')
        #         print(title)
        #         s1 = "select * from sentmail where title='"
        #         cursor.execute(s1+title+"'")
        #         result = cursor.fetchall()
        #         print(result)
        #         str1 = "select email from student where department = '"
        #         str3 = "' and semester = "
        #         str5 = " and batch = '"
        #         str10 = str1+result[0]+str3+str(result[1])+str5+result[2]+"'"
        #         cursor.execute(str10)
        #         items = cursor.fetchall()
        #         print(str10)
        #         # print(items)
        #         return render_template('followup.html', items=items)
        #     except:
        #         flash("somthing went wrong", "danger")
        #         return redirect('/reminder')
        # else:
        #     return render_template('followup.html')
    
    cursor1 = conn.cursor()
    sq = "SELECT title FROM sentmail"
    cursor1.execute(sq)
    result = cursor1.fetchall()
    return render_template('sendreminder.html', result=result)


@app.route('/followup', methods=['POST', 'GET'])
def followup():
    if request.method == 'POST':
        try:
            googlesheet = request.form.get('googlesheet')
            subsheet = request.form.get('subsheet')
            msg = request.form.get('msg')
            title = request.form.get('title')
            print(title)
            s1 = "select * from sentmail where title='"
            cursor.execute(s1+title+"'")
            result = cursor.fetchall()
            print(result)
            str1 = "select email from student where department = '"
            str3 = "' and semester = "
            str5 = " and batch = '"
            str10 = str1+result[0]+str3+str(result[1])+str5+result[2]+"'"
            cursor.execute(str10)
            items = cursor.fetchall()
            print(str10)
            # print(items)
            return render_template('followup.html', items=items)

        except:
            flash("somthing went wrong", "danger")
            return redirect('/reminder')
    else:
        return render_template('followup.html')


app.run(debug=True, port=5001)
