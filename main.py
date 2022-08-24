import glob
import json
from datetime import datetime
from pathlib import Path
import random
import time
from tkinter import Button
from hoverable import HoverBehavior
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, uname, pw):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pw:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_fail.text = "Wrong username or password"
        
    def go_to_forgot_password(self):
        self.manager.current = "forgot_password"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pw):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pw,
                        'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        with open("users.json", "w") as file:
            json.dump(users, file)

        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]
        
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt",encoding='UTF-8') as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try to enter a feeling"

class ForgotPassword(Screen):
    def change_password(self,user_name, new_pass):
        with open("users.json") as file:
            users = json.load(file)       
        users[user_name] = {'username':user_name, 'password':new_pass, 'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        if users[user_name]['username'] == user_name:
            with open("users.json", "w") as file:
                users[user_name]['password'] = new_pass
                json.dump(users, file)
            self.ids.password_status.text = "Password changed successfully"
            time.sleep(1)
            self.manager.transition.direction = "right"
            self.manager.current = "login_screen"
        else:
            self.ids.password_status.text = "Try Again"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()