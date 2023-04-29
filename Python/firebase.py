import pyrebase 

config = {
    'apiKey': "AIzaSyAM48Oj4_x2H7p-aKiJwsVfWqeh7BhUHYA",
    'authDomain': "binarybeats-4559e.firebaseapp.com",
    'projectId': "binarybeats-4559e",
    'storageBucket': "binarybeats-4559e.appspot.com",
    'messagingSenderId': "29750487982",
    'appId': "1:29750487982:web:8ac3adc27833f72ba1363f",
    'databaseURL' : ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()
# email = 'yashpatel78156@gmail.com'
# password = 'abcd1234'

# auth.send_password_reset_email(email)
title="heloo"
db.child("todo").push(title)

# auth.send_email_verification(user['idToken'])

# auth.send_password_reset_email(email)
