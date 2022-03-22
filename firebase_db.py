from re import S
import pyrebase
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
            user = auth.sign_in_with_email_and_password("altamash.ar96@gmail.com", "ab8127743728")
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
