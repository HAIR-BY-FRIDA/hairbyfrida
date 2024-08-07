from tkinter import *
from tkinter import messagebox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User, Appointment
import bcrypt

engine = create_engine('sqlite:///HairbyFrida.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class HairbyFridaAPP:
    # __init__ is used to initialize the main application and set up variables.
    def __init__(self, root):
        self.root = root
        self.root.title("HairbyFrida")  # this sets the title for the main window

    self.root.geometry("400x400")  # the dimension of the main window is set to 400x400 pixels
    self.username_var = StringVar()
    self.password_var = StringVar()
    self.create_login_screen()  # called to set up login screen


# To create Login screen
def create_login_screen(self):
    Label(self.root, text="Username").pack(pady=10)
    Entry(self.root, textvariable=self.username_var).pack(pady=5)
    Label(self.root, text="Password").pack(pady=10)
    Entry(self.root, textvariable=self.password_var, show='*').pack(pady=5)
    Button(self.root, text="Login", command=self.login).pack(pady=20)
    Button(self.root, text="Register", command=self.register).pack(pady=10)


def login(self):
    username = self.username_var.get()
    password = self.password_var.get()
    user = session.query(User).filter_by(username=username).first()
    if user and bcrypt.checkpw((password.encode('utf8'), user.password.encode('utf8'))):
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")


def register(self):
    register_window = Toplevel(self.root)
    register_window.title("Register")
    register_window.geometry("400x600")
    username_var = StringVar
    password_var = StringVar
    role_var = StringVar(value="customer")
    name_var = StringVar
    phone_var = StringVar()
    email_var = StringVar()
    gender_var = StringVar()

    Label(self.root, text="Username").pack(pady=10)
    Entry(self.root, textvariable=username_var).pack(pady=5)
    Label(self.root, text="Password").pack(pady=10)
    Entry(self.root, textvariable=password_var, show='*').pack(pady=5)
    Label(register_window, text="Role").pack(pady=10)
    OptionMenu(register_window, role_var, "customer", "staff", "admin").pack(pady=5)
    Label(self.root, text="Name").pack(pady=10)
    Entry(register_window, textvariable=name_var).pack(pady=5)
    Label(self.root, text="Phone Number").pack(pady=10)
    Entry(register_window, textvariable=phone_var).pack(pady=5)
    Label(self.root, text="Email").pack(pady=10)
    Entry(register_window, textvariable=email_var).pack(pady=5)
    Label(self.root, text="Gender").pack(pady=10)
    OptionMenu(register_window, gender_var, "Male", "Female", "Other").pack(pady=5)
    Button(register_window, text="Register", command=self.login).pack(pady=20)
    Button(self.root, text="Register",
           command=lambda: self.save_user(username_var, password_var, role_var, name_var, phone_var, email_var,
                                          gender_var)).pack(pady=20)


def save_user(self, username_var, password_var, role_var, name_var, phone_var, email_var, gender_var):
    username = username_var.get()
    password = password_var.get()
    role = role_var.get()
    name = name_var.get()
    phone = phone_var.get()
    email = email_var.get()
    gender = gender_var.get()

    if session.query(User).filter_by(username=username).first():
        messagebox.showerror("Registration Error", "Username already exists")
        return
    hashed_password = bcrypt.hashpw(password.encode('utf8').bcrypt.gensalt())
    new_user = User(username=username, password=hashed_password.decode('utf8'), role=role, name=name, phone=phone,
                    email=email, gender=gender)
    session.add(new_user)
    session.commit()

    messagebox.showinfo("Registration Success", f"User {username} has been registered successfully!")
