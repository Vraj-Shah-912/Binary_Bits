from flask import Flask, session, render_template, request, redirect, flash
import pyrebase

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
db=firebase.database()

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
            session['user'] = user
            flash("Logged in successfully","success")
            return redirect('/')
        except:
             flash("Incorect Email or password","danger")
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
                flash("signup successfully","success")
                return redirect('/login')
            except:
                flash("User already exists","warning")
                return redirect('/signup')
        else:
            flash("password and confirm paswsword not match","warning")
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
        flash("logout successfully","success")
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
            flash("user not found","danger")
            return redirect('/forgot')
        flash("reset email has send " ,"success")
        return redirect('/')
    else:
        return render_template('forgot.html')

app.run(debug=True)
