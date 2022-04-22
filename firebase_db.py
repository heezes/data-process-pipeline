from re import S
import pyrebase
import os
import json

config = {
  "apiKey": "AIzaSyAN2YrJvol6VejknFOX5EN1sBAMbBz3kQM",
  "authDomain": "vecmocon-app.firebaseapp.com",
  "databaseURL": "https://vecmocon-app.firebaseio.com",
  "storageBucket": "vecmocon-app.appspot.com"
}

class rtdb():
    def __init__(self):
        self.connected = False
        self.db = None

    def connect(self):
        try:
            firebase = pyrebase.initialize_app(config)
            auth = firebase.auth()
            email =  os.environ["FIREBASE_EMAIL"]
            password =  os.environ["FIREBASE_PASSWORD"]
            user = auth.sign_in_with_email_and_password(email, password)
            self.db = firebase.database()
            self.connected = True
        except:
            self.connected = False


    def updateDevice(self, deviceId, data):
        if self.connected:
            try:
                return self.db.child("devices").child(str(deviceId)).update(data)
            except:
                return False
        else:
            self.connect()
            return False
